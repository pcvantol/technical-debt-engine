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

    states = ("PLANNED", "READY", "RUNNING", "COMPLETED", "FAILED", "BLOCKED", "SKIPPED", "NOT_SUPPORTED")

    def __init__(self, capability_registry: CapabilityRegistry | None = None,
                 adapter_registry: AdapterRegistry | None = None) -> None:
        self._capability_registry = capability_registry or CapabilityRegistry()
        self._adapter_registry = adapter_registry or AdapterRegistry()

    def plan(self, context: Any) -> dict[str, Any]:
        requested = context.execution_options.get("capabilities", {})
        available = {item["id"]: item for item in self._capability_registry.discover()}
        enabled = [identifier for identifier, settings in requested.items() if settings.get("enabled")]
        requested_plan = [identifier for identifier in enabled if identifier in available]
        planned = [identifier for identifier in (CAPABILITY_ID, COMPLEXITY_CAPABILITY_ID, MAINTAINABILITY_CAPABILITY_ID, DEPENDENCY_CAPABILITY_ID)
                   if identifier in requested_plan or (identifier in {CAPABILITY_ID, COMPLEXITY_CAPABILITY_ID} and MAINTAINABILITY_CAPABILITY_ID in requested_plan)]
        unsupported = [identifier for identifier in enabled if identifier not in available]
        adapters = {item["id"] for item in self._adapter_registry.discover()}
        planned_adapters = [adapter for identifier, adapter in ((CAPABILITY_ID, ADAPTER_ID), (COMPLEXITY_CAPABILITY_ID, COMPLEXITY_ADAPTER_ID))
                            if identifier in planned and adapter in adapters]
        return {
            "state": "PLANNED",
            "capabilities": planned,
            "unsupportedCapabilities": unsupported,
            "plannedAdapters": planned_adapters,
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
            normalized = self._dispatch(identifier, context, measurements)
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

        evidence["unsupportedCapabilities"].extend(plan["unsupportedCapabilities"])
        evidence["durationMs"] = int((perf_counter() - started) * 1000)
        evidence["state"] = "COMPLETED" if evidence["executedCapabilities"] else "BLOCKED"
        return {
            "executedWorkItems": len(evidence["workItems"]),
            "measurements": measurements,
            "findings": findings,
            "capabilityResults": capability_results,
            "adapterResults": adapter_results,
            "executionEvidence": evidence,
        }

    def _dispatch(self, identifier: str, context: Any, measurements: list[dict[str, Any]]) -> dict[str, Any]:
        started = perf_counter()
        timeout = int(context.execution_options.get("timeout", 60))
        if identifier == CAPABILITY_ID:
            result = analyze(context.repository_root, timeout)
            duration = int((perf_counter() - started) * 1000)
            return self._code_size_result(context, result, duration) if result["status"] == "VALID" else self._blocked(CAPABILITY_ID, CAPABILITY_VERSION, [ADAPTER_ID], result["limitations"], duration)
        if identifier == COMPLEXITY_CAPABILITY_ID:
            result = analyze_complexity(context.repository_root, timeout)
            duration = int((perf_counter() - started) * 1000)
            if result["status"] != "VALID":
                return self._blocked(COMPLEXITY_CAPABILITY_ID, COMPLEXITY_CAPABILITY_VERSION, [COMPLEXITY_ADAPTER_ID], result["limitations"], duration)
            capability = {"capabilityId": COMPLEXITY_CAPABILITY_ID, "capabilityVersion": COMPLEXITY_CAPABILITY_VERSION,
                          "status": "VALID", "adapterIds": [COMPLEXITY_ADAPTER_ID], "completeness": 1,
                          "qualificationApplicable": True, "executionTiming": {"durationMs": duration}}
            return {"measurements": result.get("measurements", []), "findings": result.get("findings", []), "capabilityResults": [capability]}
        if identifier == DEPENDENCY_CAPABILITY_ID:
            result = discover_dependencies(context.repository_root)
            duration = int((perf_counter() - started) * 1000)
            capability = {"capabilityId": DEPENDENCY_CAPABILITY_ID, "capabilityVersion": DEPENDENCY_CAPABILITY_VERSION,
                          "status": "VALID", "adapterIds": [], "completeness": 1, "qualificationApplicable": True,
                          "executionTiming": {"durationMs": duration}}
            return {"measurements": result["measurements"], "findings": result["findings"], "capabilityResults": [capability]}
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
    def _blocked(identifier: str, version: str, adapter_ids: list[str], limitations: list[dict[str, Any]], duration: int) -> dict[str, Any]:
        return {"measurements": [], "findings": [], "capabilityResults": [{"capabilityId": identifier, "capabilityVersion": version,
                "status": "BLOCKED", "adapterIds": adapter_ids, "completeness": 0, "qualificationApplicable": False,
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
