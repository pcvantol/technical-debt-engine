"""Sequential, registry-driven coordinator for registered capability execution."""

from __future__ import annotations

from time import perf_counter
from typing import Any
from hashlib import sha256

from .code_size import ADAPTER_ID, CAPABILITY_ID, CAPABILITY_VERSION, analyze
from .complexity import ADAPTER_ID as COMPLEXITY_ADAPTER_ID, CAPABILITY_ID as COMPLEXITY_CAPABILITY_ID, CAPABILITY_VERSION as COMPLEXITY_CAPABILITY_VERSION, analyze as analyze_complexity
from .dependency_health import CAPABILITY_ID as DEPENDENCY_CAPABILITY_ID, CAPABILITY_VERSION as DEPENDENCY_CAPABILITY_VERSION, discover as discover_dependencies
from .maintainability import CAPABILITY_ID as MAINTAINABILITY_CAPABILITY_ID, CAPABILITY_VERSION as MAINTAINABILITY_CAPABILITY_VERSION, derive as derive_maintainability
from .registries import AdapterRegistry, CapabilityRegistry


class CapabilityExecutionEngine:
    """Plans and records capability work; Runtime only consumes its canonical output."""

    states = ("PLANNED", "READY", "RUNNING", "COMPLETED", "FAILED_CLOSED", "BLOCKED", "SKIPPED", "NOT_SUPPORTED", "ANALYZER_NOT_FOUND")

    def __init__(self, capability_registry: CapabilityRegistry | None = None,
                 adapter_registry: AdapterRegistry | None = None) -> None:
        self._capability_registry = capability_registry or CapabilityRegistry()
        self._adapter_registry = adapter_registry or AdapterRegistry()

    def plan(self, context: Any) -> dict[str, Any]:
        requested = context.execution_options.get("capabilities", {})
        registered = tuple(self._capability_registry.discover())
        available = {item["id"]: item for item in registered}
        enabled = [identifier for identifier, settings in requested.items() if settings.get("enabled")]
        requested_plan = set(identifier for identifier in enabled if identifier in available)
        # Registration order is the reproducible plan order.  The planner does
        # not encode any capability-specific execution sequence.
        planned = [item["id"] for item in registered if item["id"] in requested_plan]
        unsupported = [identifier for identifier in enabled if identifier not in available]
        selected = {identifier: self._adapter_registry.select(available[identifier]) for identifier in planned if "supportedAnalyzers" in available[identifier]}
        planned_adapters = [binding["id"] for binding in selected.values() if binding]
        return {
            "state": "PLANNED",
            "capabilities": planned,
            "unsupportedCapabilities": unsupported,
            "plannedAdapters": planned_adapters,
            "analyzerBindings": {identifier: binding["id"] if binding else None for identifier, binding in selected.items()},
            "parallelReady": True,
            "retries": "NONE",
        }

    def execute(self, context: Any) -> dict[str, Any]:
        started = perf_counter()
        plan = self.plan(context)
        evidence = self._execution_evidence(context, plan)
        measurements: list[dict[str, Any]] = []
        findings: list[dict[str, Any]] = []
        capability_results: list[dict[str, Any]] = []
        adapter_results: list[dict[str, Any]] = []

        for identifier in plan["capabilities"]:
            normalized = self._dispatch(identifier, plan.get("analyzerBindings", {}).get(identifier), context, measurements)
            measurements.extend(normalized["measurements"])
            findings.extend(normalized["findings"])
            capability_results.extend(normalized["capabilityResults"])
            adapter_results.extend(normalized.get("adapterResults", []))
            result = normalized["capabilityResults"][-1]
            adapter_ids = result.get("adapterIds", [])
            state = "COMPLETED" if result["status"] == "VALID" else "BLOCKED"
            if state == "COMPLETED":
                evidence["executedCapabilities"].append(identifier)
                evidence["executedAdapters"].extend(adapter_ids)
            else:
                evidence["blockedCapabilities"].append(identifier)
                evidence["limitations"].extend(result.get("limitations", []))
            evidence["workItems"].append({"capabilityId": identifier, "adapterId": adapter_ids[0] if adapter_ids else None,
                                            "state": state, "durationMs": result["executionTiming"]["durationMs"]})

        for identifier in plan["unsupportedCapabilities"]:
            limitation = {"id": "capability.unsupported", "description": f"capability '{identifier}' is not registered", "cause": "capability unavailable"}
            capability_results.append({"capabilityId": identifier, "capabilityVersion": None,
                                       "status": "NOT_SUPPORTED", "adapterIds": [], "completeness": 0,
                                       "qualificationApplicable": False, "limitations": [limitation],
                                       "executionTiming": {"durationMs": 0}})
            evidence["blockedCapabilities"].append(identifier)
            evidence["limitations"].append(limitation)
            evidence["workItems"].append({"capabilityId": identifier, "adapterId": None,
                                            "state": "NOT_SUPPORTED", "durationMs": 0})

        evidence["unsupportedCapabilities"].extend(plan["unsupportedCapabilities"])
        evidence["durationMs"] = int((perf_counter() - started) * 1000)
        evidence["state"] = "COMPLETED" if evidence["executedCapabilities"] else ("NOT_SUPPORTED" if plan["unsupportedCapabilities"] else "BLOCKED")
        return {
            "executedWorkItems": len(evidence["workItems"]),
            "measurements": measurements,
            "findings": findings,
            "capabilityResults": capability_results,
            "adapterResults": adapter_results,
            "executionEvidence": evidence,
        }

    def _dispatch(self, identifier: str, selected_adapter: str | None, context: Any, measurements: list[dict[str, Any]]) -> dict[str, Any]:
        started = perf_counter()
        # Repository-wide cloc scans can legitimately exceed one minute on a
        # public consumer checkout.  A bounded five-minute default remains
        # fail-closed while avoiding a size-dependent false failure.
        timeout = int(context.execution_options.get("timeout", 300))
        if identifier == CAPABILITY_ID and selected_adapter == ADAPTER_ID:
            result = analyze(context.repository_root, timeout)
            duration = int((perf_counter() - started) * 1000)
            return self._code_size_result(context, result, duration) if result["status"] == "VALID" else self._blocked(CAPABILITY_ID, CAPABILITY_VERSION, [ADAPTER_ID], result["limitations"], duration, result["status"])
        if identifier == COMPLEXITY_CAPABILITY_ID and selected_adapter == COMPLEXITY_ADAPTER_ID:
            settings = context.execution_options.get("capabilities", {}).get(COMPLEXITY_CAPABILITY_ID, {})
            result = analyze_complexity(context.repository_root, timeout, settings)
            duration = int((perf_counter() - started) * 1000)
            if result["status"] != "VALID":
                return self._blocked(COMPLEXITY_CAPABILITY_ID, COMPLEXITY_CAPABILITY_VERSION, [COMPLEXITY_ADAPTER_ID], result["limitations"], duration)
            return self._complexity_result(context, result, duration)
        if identifier == DEPENDENCY_CAPABILITY_ID:
            result = discover_dependencies(context.repository_root)
            duration = int((perf_counter() - started) * 1000)
            capability = {"capabilityId": DEPENDENCY_CAPABILITY_ID, "capabilityVersion": DEPENDENCY_CAPABILITY_VERSION,
                          "status": "VALID", "adapterIds": [], "completeness": 1, "qualificationApplicable": True,
                          "executionTiming": {"durationMs": duration}}
            return {"measurements": result["measurements"], "findings": result["findings"], "capabilityResults": [capability]}
        if identifier != MAINTAINABILITY_CAPABILITY_ID:
            return self._blocked(identifier, "0.1.0", [], [{"id": "adapter.selection.unavailable", "description": f"no selected adapter can execute {identifier}", "cause": "adapter selection"}], 0)
        code = {"measurements": measurements}
        complexity = {"measurements": [item for item in measurements if item.get("capabilityId") == COMPLEXITY_CAPABILITY_ID]}
        result = derive_maintainability(code, complexity)
        duration = int((perf_counter() - started) * 1000)
        if result["status"] != "VALID":
            return self._blocked(MAINTAINABILITY_CAPABILITY_ID, MAINTAINABILITY_CAPABILITY_VERSION, [], result["limitations"], duration)
        capability = {"capabilityId": MAINTAINABILITY_CAPABILITY_ID, "capabilityVersion": MAINTAINABILITY_CAPABILITY_VERSION,
                      "status": "VALID", "adapterIds": [], "completeness": 1, "qualificationApplicable": True,
                      "executionTiming": {"durationMs": duration}}
        return {"measurements": result["measurements"], "findings": result["findings"], "capabilityResults": [capability]}

    @staticmethod
    def _blocked(identifier: str, version: str, adapter_ids: list[str], limitations: list[dict[str, Any]], duration: int,
                 status: str = "BLOCKED") -> dict[str, Any]:
        return {"measurements": [], "findings": [], "capabilityResults": [{"capabilityId": identifier, "capabilityVersion": version,
                "status": status, "adapterIds": adapter_ids, "completeness": 0, "qualificationApplicable": False,
                "limitations": limitations, "executionTiming": {"durationMs": duration}}]}

    @staticmethod
    def _execution_evidence(context: Any, plan: dict[str, Any]) -> dict[str, Any]:
        return {
            "executionId": context.execution_id,
            "plannedCapabilities": plan["capabilities"],
            "executedCapabilities": [],
            "skippedCapabilities": [],
            "blockedCapabilities": [],
            "unsupportedCapabilities": [],
            "plannedAdapters": plan["plannedAdapters"],
            "analyzerBindings": plan["analyzerBindings"],
            "executedAdapters": [],
            "workItems": [],
            "executionGraph": {"nodes": plan["capabilities"], "edges": []},
            "durationMs": 0,
            "state": "PLANNED",
            "limitations": [],
        }

    @staticmethod
    def _code_size_result(context: Any, result: dict[str, Any], duration: int) -> dict[str, Any]:
        names = {"files": "file_count", "code": "code_lines", "comment": "comment_lines", "blank": "blank_lines",
                 "source": "source_lines", "test": "test_lines", "generated": "generated_lines",
                 "vendor": "vendor_lines", "documentation": "documentation_lines"}
        measurements = [
            {"measurementId": f"code_size.repository.{key}", "capabilityId": CAPABILITY_ID,
             "metricKey": f"code_size.{names[key]}", "value": value, "unit": "files" if key == "files" else "lines",
             "scope": "repository", "targetEntityId": context.repository_id, "aggregation": "sum",
             "sourceAdapterId": result["adapter"]["id"], "sourceToolId": "cloc"}
            for key, value in result["totals"].items() if key in names
        ]
        measurements.append({"measurementId": "code_size.repository.test_ratio", "capabilityId": CAPABILITY_ID,
                             "metricKey": "code_size.test_to_source_ratio", "value": result["testToSourceRatio"],
                             "unit": "ratio", "scope": "repository", "targetEntityId": context.repository_id,
                             "aggregation": "ratio", "sourceAdapterId": result["adapter"]["id"], "sourceToolId": "cloc"})
        for language, totals in result["languages"].items():
            language_id = f"language.{language.lower().replace(' ', '_')}"
            for key in ("files", "code", "comment", "blank"):
                measurements.append({"measurementId": f"code_size.{language_id}.{key}", "capabilityId": CAPABILITY_ID,
                                     "metricKey": f"code_size.language_{key}", "value": totals[key],
                                     "unit": "files" if key == "files" else "lines", "scope": "language",
                                     "targetEntityId": language_id, "aggregation": "sum",
                                     "sourceAdapterId": result["adapter"]["id"], "sourceToolId": "cloc"})
        for file in result["files"]:
            file_id = "file." + sha256(file["path"].encode()).hexdigest()[:16]
            for key in ("code", "comment", "blank"):
                measurements.append({"measurementId": f"code_size.{file_id}.{key}", "capabilityId": CAPABILITY_ID,
                                     "metricKey": f"code_size.file_{key}_lines", "value": file[key], "unit": "lines",
                                     "scope": "file", "targetEntityId": file_id, "aggregation": "sum",
                                     "sourceAdapterId": result["adapter"]["id"], "sourceToolId": "cloc"})
        adapter_result = {"adapter": result["adapter"], "analyzer": result["analyzer"], "execution": "SUCCESS",
                          "rawOutputHash": result["rawOutputHash"], "rawOutput": result["rawOutput"],
                          "measuredScope": ["repository", "language", "file"], "completeness": 1,
                          "draftMeasurements": measurements, "draftFindings": [], "warnings": [], "errors": [],
                          "limitations": result["limitations"], "executionTiming": {"durationMs": duration}}
        return {"measurements": measurements, "findings": [], "adapterResults": [adapter_result], "capabilityResults": [
            {"capabilityId": CAPABILITY_ID, "capabilityVersion": CAPABILITY_VERSION, "status": "VALID",
             "adapterIds": [result["adapter"]["id"]], "completeness": 1, "qualificationApplicable": True,
             "limitations": result["limitations"], "executionTiming": {"durationMs": duration}}
        ]}

    @staticmethod
    def _complexity_result(context: Any, result: dict[str, Any], duration: int) -> dict[str, Any]:
        symbols, measurements, findings = result["symbols"], [], []
        def measurement_id(scope: str, entity: str, metric: str) -> str:
            return f"complexity.{scope}.{sha256(entity.encode()).hexdigest()[:16]}.{metric}"
        def add_summary(scope: str, entity: str, values: list[int]) -> None:
            if not values: return
            for metric, value, aggregation in (("average", sum(values)/len(values), "mean"), ("maximum", max(values), "maximum")):
                measurements.append({"measurementId":measurement_id(scope,entity,metric),"capabilityId":COMPLEXITY_CAPABILITY_ID,"metricKey":f"complexity.cyclomatic.{metric}","value":value,"unit":"score","scope":scope,"targetEntityId":entity,"aggregation":aggregation,"sourceAdapterId":COMPLEXITY_ADAPTER_ID,"sourceToolId":"radon"})
            for lower, upper, band in ((1,10,"low"),(11,20,"high"),(21,40,"very_high"),(41,None,"critical")):
                measurements.append({"measurementId":measurement_id(scope,entity,f"distribution.{band}"),"capabilityId":COMPLEXITY_CAPABILITY_ID,"metricKey":"complexity.cyclomatic.distribution","value":sum(1 for value in values if value >= lower and (upper is None or value <= upper)),"unit":"symbols","scope":scope,"targetEntityId":f"{entity}.distribution.{band}","aggregation":"count","sourceAdapterId":COMPLEXITY_ADAPTER_ID,"sourceToolId":"radon"})
        add_summary("repository", context.repository_id, [symbol["complexity"] for symbol in symbols])
        by_language, by_file = {}, {}
        for symbol in symbols:
            by_language.setdefault(symbol["language"], []).append(symbol); by_file.setdefault(symbol["path"], []).append(symbol)
            entity = "symbol." + sha256(f"{symbol['path']}:{symbol['name']}:{symbol['line']}".encode()).hexdigest()[:16]
            evidence = measurement_id("symbol", entity, "value")
            measurements.append({"measurementId":evidence,"capabilityId":COMPLEXITY_CAPABILITY_ID,"metricKey":"complexity.cyclomatic.value","value":symbol["complexity"],"unit":"score","scope":"symbol","targetEntityId":entity,"aggregation":"value","sourceAdapterId":COMPLEXITY_ADAPTER_ID,"sourceToolId":"radon"})
            thresholds = result["thresholds"]
            if symbol["complexity"] >= thresholds["critical"]: rule, severity, title, threshold = "complexity.critical", "CRITICAL", "Critical Complexity", thresholds["critical"]
            elif symbol["complexity"] >= thresholds["veryHigh"]: rule, severity, title, threshold = "complexity.very_high", "HIGH", "Very High Complexity", thresholds["veryHigh"]
            elif symbol["complexity"] >= thresholds["high"]: rule, severity, title, threshold = "complexity.high", "HIGH", "High Complexity", thresholds["high"]
            else: continue
            findings.append({"findingId":f"{rule}.{entity}","capabilityId":COMPLEXITY_CAPABILITY_ID,"ruleId":rule,"severity":severity,"category":"COMPLEXITY","title":title,"description":f"Cyclomatic complexity is {symbol['complexity']} (threshold: {threshold}).","affectedEntityId":entity,"location":{"path":symbol["path"],"line":symbol["line"],"endLine":symbol["endLine"]},"evidenceReferences":[evidence],"state":"OPEN","regression":"UNKNOWN","confidence":1,"suppressible":True})
        for language, values in sorted(by_language.items()): add_summary("language", f"language.{language.lower()}", [item["complexity"] for item in values])
        for path, values in sorted(by_file.items()): add_summary("file", "file."+sha256(path.encode()).hexdigest()[:16], [item["complexity"] for item in values])
        if not symbols:
            findings.append({"findingId":"complexity.missing.repository","capabilityId":COMPLEXITY_CAPABILITY_ID,"ruleId":"complexity.missing","severity":"INFO","category":"COMPLEXITY","title":"Missing Complexity","description":"No supported symbols were measured.","affectedEntityId":context.repository_id,"evidenceReferences":[],"state":"OPEN","regression":"UNKNOWN","confidence":1,"suppressible":False})
        adapter = {"adapter":result["adapter"],"analyzer":result["analyzer"],"execution":"SUCCESS","rawOutputHash":result["rawOutputHash"],"rawOutput":result["rawOutput"],"measuredScope":["repository","language","file","symbol"],"completeness":1,"draftMeasurements":measurements,"draftFindings":findings,"warnings":[],"errors":[],"limitations":result["limitations"],"executionTiming":{"durationMs":duration}}
        capability = {"capabilityId":COMPLEXITY_CAPABILITY_ID,"capabilityVersion":COMPLEXITY_CAPABILITY_VERSION,"status":"VALID","adapterIds":[COMPLEXITY_ADAPTER_ID],"completeness":1,"qualificationApplicable":True,"limitations":result["limitations"],"executionTiming":{"durationMs":duration}}
        return {"measurements":measurements,"findings":findings,"adapterResults":[adapter],"capabilityResults":[capability]}
