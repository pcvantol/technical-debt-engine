"""Evidence-only, fail-closed assessment of Runtime analysis trustworthiness."""

from __future__ import annotations

from hashlib import sha256
from typing import Any, Mapping


class RuntimeQualificationEngine:
    levels = ("QUALIFIED", "PARTIALLY_QUALIFIED", "BLOCKED", "NOT_SUPPORTED")

    def qualify(self, evidence: Mapping[str, Any], capability: str | None = None) -> dict[str, Any]:
        state = self._execution_state(evidence)
        selected = [item for item in evidence.get("capabilityResults", []) if capability is None or item.get("capabilityId") == capability]
        level = self._level(state, selected, capability)
        if capability and not selected:
            state["missingCapabilities"].append(capability)
            state["limitations"].append("requested capability evidence is absent")
        confidence = {"BLOCKED": 0.0, "NOT_SUPPORTED": 0.0, "PARTIALLY_QUALIFIED": 0.75}.get(level, 1.0)
        identity = sha256(f"{evidence.get('integrity', {}).get('contentDigest')}:{capability}".encode()).hexdigest()[:16]
        return {"qualificationId": f"runtime-qualification.{identity}", "level": level,
                "confidence": {"analysis": confidence, "repository": confidence, "capability": confidence},
                "limitations": state["limitations"], "missingCapabilities": sorted(set(state["missingCapabilities"])),
                "missingAdapters": sorted(set(state["missingAdapters"])), "unsupportedLanguages": [],
                "supportingEvidence": {"executionId": evidence.get("executionId"), "policy": evidence.get("policyEvidence", {}),
                                       "capabilityCount": len(selected), "executedCapabilityCount": len(state["executed"]),
                                       "executedAdapterCount": len(state["executedAdapters"]), "workItemCount": len(state["workItems"])}}

    @staticmethod
    def _execution_state(evidence: Mapping[str, Any]) -> dict[str, Any]:
        limitations: list[str] = []
        missing_capabilities: list[str] = []
        execution = evidence.get("executionEvidence")
        results = evidence.get("capabilityResults", [])
        if evidence.get("validation", {}).get("status") != "VALID":
            limitations.append("evidence validation failed")
        if not isinstance(execution, Mapping):
            limitations.append("execution evidence is missing")
            execution = {}
        planned = list(execution.get("plannedCapabilities", []))
        executed = list(execution.get("executedCapabilities", []))
        work_items = list(execution.get("workItems", []))
        if not work_items:
            limitations.append("execution work-item list is empty")
        if not executed:
            limitations.append("zero capabilities executed")
        missing_capabilities.extend(identifier for identifier in planned if identifier not in executed or not any(item.get("capabilityId") == identifier for item in results))
        planned_adapters = list(execution.get("plannedAdapters", []))
        executed_adapters = list(execution.get("executedAdapters", []))
        missing_adapters = [identifier for identifier in planned_adapters if identifier not in executed_adapters]
        if missing_adapters:
            limitations.append("required adapter evidence is missing")
        return {"limitations": limitations, "missingCapabilities": missing_capabilities, "missingAdapters": missing_adapters,
                "executed": executed, "executedAdapters": executed_adapters, "workItems": work_items}

    @staticmethod
    def _level(state: Mapping[str, Any], selected: list[Mapping[str, Any]], capability: str | None) -> str:
        if capability and not selected:
            return "BLOCKED"
        blocked = any(item.get("status") in {"BLOCKED", "FAILED"} for item in selected)
        if state["limitations"] or state["missingCapabilities"] or blocked:
            return "BLOCKED"
        return "PARTIALLY_QUALIFIED" if any(item.get("completeness", 1) < 1 or item.get("status") == "PARTIAL" for item in selected) else "QUALIFIED"
