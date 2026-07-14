"""Evidence-only, fail-closed assessment of Runtime analysis trustworthiness."""

from __future__ import annotations

from hashlib import sha256
from typing import Any, Mapping


class RuntimeQualificationEngine:
    levels = ("QUALIFIED", "PARTIALLY_QUALIFIED", "BLOCKED", "NOT_SUPPORTED")

    def qualify(self, evidence: Mapping[str, Any], capability: str | None = None) -> dict[str, Any]:
        limitations: list[str] = []
        missing_capabilities: list[str] = []
        missing_adapters: list[str] = []
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
        for identifier in planned:
            if identifier not in executed or not any(item.get("capabilityId") == identifier for item in results):
                missing_capabilities.append(identifier)
        planned_adapters = list(execution.get("plannedAdapters", []))
        executed_adapters = list(execution.get("executedAdapters", []))
        missing_adapters = [identifier for identifier in planned_adapters if identifier not in executed_adapters]
        if missing_adapters:
            limitations.append("required adapter evidence is missing")

        selected = [item for item in results if capability is None or item.get("capabilityId") == capability]
        if capability and not selected:
            missing_capabilities.append(capability)
            limitations.append("requested capability evidence is absent")
            level = "BLOCKED"
        else:
            blocked = [item for item in selected if item.get("status") in {"BLOCKED", "FAILED"}]
            partial = [item for item in selected if item.get("completeness", 1) < 1 or item.get("status") == "PARTIAL"]
            level = "BLOCKED" if limitations or missing_capabilities or blocked else "PARTIALLY_QUALIFIED" if partial else "QUALIFIED"
        confidence = 0.0 if level in {"BLOCKED", "NOT_SUPPORTED"} else 0.75 if level == "PARTIALLY_QUALIFIED" else 1.0
        identity = sha256(f"{evidence.get('integrity', {}).get('contentDigest')}:{capability}".encode()).hexdigest()[:16]
        return {"qualificationId": f"runtime-qualification.{identity}", "level": level,
                "confidence": {"analysis": confidence, "repository": confidence, "capability": confidence},
                "limitations": limitations, "missingCapabilities": sorted(set(missing_capabilities)),
                "missingAdapters": sorted(set(missing_adapters)), "unsupportedLanguages": [],
                "supportingEvidence": {"executionId": evidence.get("executionId"), "policy": evidence.get("policyEvidence", {}),
                                       "capabilityCount": len(selected), "executedCapabilityCount": len(executed),
                                       "executedAdapterCount": len(executed_adapters), "workItemCount": len(work_items)}}
