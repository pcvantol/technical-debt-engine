"""Immutable canonical-evidence baselines and deterministic comparisons."""

from __future__ import annotations

from hashlib import sha256
import json
from pathlib import Path
from typing import Any, Mapping

from .models import utc_now


class BaselineError(ValueError):
    """Raised when a baseline cannot be created, loaded, or compared."""


class BaselineRepository:
    def __init__(self, location: str | Path) -> None:
        self.location = Path(location)

    def create(self, evidence: Mapping[str, Any], name: str | None = None) -> dict[str, Any]:
        self._validate_evidence(evidence)
        created_at = utc_now()
        digest = evidence["integrity"]["contentDigest"]
        identity = sha256(f"{digest}:{created_at}".encode()).hexdigest()[:16]
        baseline_id = name or f"baseline.{identity}"
        destination = self.location / f"{baseline_id}.json"
        if destination.exists():
            raise BaselineError(f"baseline already exists and is immutable: {baseline_id}")
        record = {"baselineId": baseline_id, "sourceEvidenceId": digest,
                  "repositoryId": evidence["repository"]["id"], "candidateId": evidence["candidate"]["id"],
                  "schemaVersion": evidence["schemaVersion"], "runtimeVersion": evidence["runtime"]["version"],
                  "createdAt": created_at,
                  "policyVersion": evidence.get("policyEvidence", {}).get("policy", {}).get("version"),
                  "integrityDigest": f"sha256:{sha256(json.dumps(evidence, sort_keys=True).encode()).hexdigest()}",
                  "evidence": evidence}
        self.location.mkdir(parents=True, exist_ok=True)
        destination.write_text(json.dumps(record, sort_keys=True, indent=2) + "\n", encoding="utf-8")
        return record

    def load(self, reference: str | Path) -> dict[str, Any]:
        path = Path(reference)
        path = path if path.is_absolute() or path.exists() else self.location / f"{reference}.json"
        try:
            value = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as error:
            raise BaselineError(f"cannot load baseline {reference}: {error}") from error
        if not isinstance(value, dict) or "evidence" not in value:
            raise BaselineError("baseline does not contain canonical evidence")
        self._validate_evidence(value["evidence"])
        return value

    @staticmethod
    def _validate_evidence(evidence: Mapping[str, Any]) -> None:
        if evidence.get("schemaId") != "tde.evidence" or evidence.get("validation", {}).get("status") != "VALID":
            raise BaselineError("baseline requires validated canonical evidence")


class ComparisonEngine:
    """Compares canonical evidence; it never produces a qualification decision."""

    def compare(self, current: Mapping[str, Any], baseline: Mapping[str, Any]) -> dict[str, Any]:
        BaselineRepository._validate_evidence(current)
        previous = baseline["evidence"]
        compatible = self._compatible(current, previous)
        baseline_id = baseline["baselineId"]
        if not compatible:
            return self._blocked(current, baseline_id, "schema, runtime, or repository compatibility failed")
        metric_deltas, metric_limitations = self._metrics(current.get("measurements", []), previous.get("measurements", []))
        finding_transitions, regressions, improvements = self._findings(current.get("findings", []), previous.get("findings", []))
        return {"comparisonId": self._identity(current, baseline_id),
                "currentEvidenceId": current["integrity"]["contentDigest"], "baselineEvidenceId": previous["integrity"]["contentDigest"],
                "baselineId": baseline_id, "schemaCompatibility": "COMPATIBLE", "metricDeltas": metric_deltas,
                "findingTransitions": finding_transitions, "regressions": regressions, "improvements": improvements,
                "capabilityComparison": self._capabilities(current, previous), "limitations": metric_limitations, "status": "VALID"}

    @staticmethod
    def _compatible(current: Mapping[str, Any], baseline: Mapping[str, Any]) -> bool:
        return (current.get("schemaVersion") == baseline.get("schemaVersion") and
                current.get("runtime", {}).get("version") == baseline.get("runtime", {}).get("version") and
                current.get("repository", {}).get("id") == baseline.get("repository", {}).get("id"))

    def _blocked(self, current: Mapping[str, Any], baseline_id: str, reason: str) -> dict[str, Any]:
        return {"comparisonId": self._identity(current, baseline_id), "currentEvidenceId": current["integrity"]["contentDigest"],
                "baselineEvidenceId": "unknown", "baselineId": baseline_id, "schemaCompatibility": "INCOMPATIBLE",
                "metricDeltas": [], "findingTransitions": [], "regressions": [], "improvements": [], "capabilityComparison": [],
                "limitations": [{"reason": reason, "blocking": True}], "status": "BLOCKED"}

    @staticmethod
    def _metrics(current: list[Mapping[str, Any]], baseline: list[Mapping[str, Any]]) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
        key = lambda item: (item.get("metricKey"), item.get("scope"), item.get("targetEntityId"))
        old = {key(item): item for item in baseline if isinstance(item.get("value"), (int, float))}
        deltas: list[dict[str, Any]] = []
        limitations: list[dict[str, Any]] = []
        for item in current:
            if key(item) not in old or not isinstance(item.get("value"), (int, float)):
                continue
            previous = old[key(item)]["value"]
            value = item["value"]
            delta = value - previous
            percentage = None if previous == 0 else delta / previous
            if previous == 0:
                limitations.append({"reason": f"percentage delta unavailable for {item.get('metricKey')}", "blocking": False})
            deltas.append({"metricKey": item.get("metricKey"), "scope": item.get("scope"), "baseline": previous,
                           "current": value, "numericDelta": delta, "percentageDelta": percentage,
                           "ratioDelta": delta if item.get("unit") == "ratio" else None,
                           "distributionDelta": None, "trend": "INCREASED" if delta > 0 else "DECREASED" if delta < 0 else "UNCHANGED"})
        return deltas, limitations

    @staticmethod
    def _findings(current: list[Mapping[str, Any]], baseline: list[Mapping[str, Any]]) -> tuple[list[dict[str, Any]], list[str], list[str]]:
        old, new = ({item.get("findingId"): item for item in values} for values in (baseline, current))
        severity = {"INFO": 0, "LOW": 1, "MEDIUM": 2, "HIGH": 3, "CRITICAL": 4}
        transitions: list[dict[str, Any]] = []
        regressions: list[str] = []
        improvements: list[str] = []
        for finding_id in sorted(set(old) | set(new)):
            if finding_id not in old:
                transition = "INTRODUCED"; regressions.append(finding_id)
            elif finding_id not in new:
                transition = "RESOLVED"; improvements.append(finding_id)
            else:
                before, after = severity.get(old[finding_id].get("severity"), 0), severity.get(new[finding_id].get("severity"), 0)
                transition = "SEVERITY_INCREASED" if after > before else "SEVERITY_DECREASED" if after < before else "UNCHANGED"
                (regressions if after > before else improvements if after < before else []).append(finding_id)
            transitions.append({"findingId": finding_id, "transition": transition})
        return transitions, regressions, improvements

    @staticmethod
    def _capabilities(current: Mapping[str, Any], baseline: Mapping[str, Any]) -> list[dict[str, Any]]:
        old = {item["capabilityId"]: item for item in baseline.get("capabilityResults", [])}
        return [{"capabilityId": item["capabilityId"], "comparisonSupport": "SUPPORTED" if item["capabilityId"] in old else "UNSUPPORTED",
                 "limitations": [] if item["capabilityId"] in old else ["baseline has no compatible capability result"]}
                for item in current.get("capabilityResults", [])]

    @staticmethod
    def _identity(current: Mapping[str, Any], baseline_id: str) -> str:
        return "comparison." + sha256(f"{current['integrity']['contentDigest']}:{baseline_id}".encode()).hexdigest()[:16]
