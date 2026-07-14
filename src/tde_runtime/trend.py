"""Normalized, read-only trends over validated baseline evidence."""

from __future__ import annotations

from hashlib import sha256
from pathlib import Path
from typing import Any, Mapping

from .baseline import BaselineRepository


class TrendEngine:
    """Aggregates canonical evidence history and deliberately makes no policy decision."""

    def build(self, current: Mapping[str, Any], location: str | Path, history_depth: int | None = None) -> dict[str, Any]:
        BaselineRepository._validate_evidence(current)
        repository = BaselineRepository(location)
        history = []
        for path in sorted(Path(location).glob("*.json")) if Path(location).is_dir() else []:
            history.append(repository.load(path))
        history.sort(key=lambda item: item["createdAt"])
        if history_depth is not None:
            history = history[-history_depth:]
        evidence = [item["evidence"] for item in history] + [current]
        metric_trends = self._metrics(evidence)
        capability_trends = self._capabilities(evidence)
        finding_trends = self._findings(evidence)
        qualification_history = [item.get("policyEvidence", {}).get("decision", "NOT_APPLICABLE") for item in evidence]
        return {"trendId": "trend." + sha256("|".join(item["integrity"]["contentDigest"] for item in evidence).encode()).hexdigest()[:16],
                "repositoryId": current["repository"]["id"], "history": [{"baselineId": item["baselineId"], "createdAt": item["createdAt"], "evidenceId": item["sourceEvidenceId"]} for item in history],
                "comparisonReferences": [item["baselineId"] for item in history], "repositoryTrend": self._repository(metric_trends),
                "capabilityTrends": capability_trends, "metricTrends": metric_trends, "findingTrends": finding_trends,
                "qualificationTrend": {"history": qualification_history, "direction": self._direction(qualification_history)},
                "window": "latest" if not history else "rolling", "limitations": []}

    @staticmethod
    def _metrics(evidence: list[Mapping[str, Any]]) -> list[dict[str, Any]]:
        series: dict[str, list[float]] = {}
        for snapshot in evidence:
            for metric in snapshot.get("measurements", []):
                if isinstance(metric.get("value"), (int, float)):
                    series.setdefault(metric["metricKey"], []).append(metric["value"])
        return [{"metricKey": key, "timeSeries": values, "delta": values[-1] - values[0],
                 "movingAverage": sum(values) / len(values), "direction": TrendEngine._numeric_direction(values)} for key, values in sorted(series.items())]

    @staticmethod
    def _capabilities(evidence: list[Mapping[str, Any]]) -> list[dict[str, Any]]:
        states: dict[str, list[str]] = {}
        for snapshot in evidence:
            for result in snapshot.get("capabilityResults", []):
                states.setdefault(result["capabilityId"], []).append(result.get("status", "UNKNOWN"))
        return [{"capabilityId": key, "history": values, "direction": "STABLE" if len(set(values)) == 1 else "CHANGED"} for key, values in sorted(states.items())]

    @staticmethod
    def _findings(evidence: list[Mapping[str, Any]]) -> list[dict[str, Any]]:
        seen: dict[str, int] = {}
        for snapshot in evidence:
            for finding in snapshot.get("findings", []):
                seen[finding["findingId"]] = seen.get(finding["findingId"], 0) + 1
        return [{"findingId": key, "occurrences": count, "state": "PERSISTENT" if count > 1 else "INTRODUCED"} for key, count in sorted(seen.items())]

    @staticmethod
    def _repository(metrics: list[Mapping[str, Any]]) -> dict[str, Any]:
        size = next((item for item in metrics if item["metricKey"] == "code_size.code_lines"), None)
        return {"growth": size["delta"] if size else None, "direction": size["direction"] if size else "NOT_APPLICABLE"}

    @staticmethod
    def _numeric_direction(values: list[float]) -> str:
        return "INCREASING" if values[-1] > values[0] else "DECREASING" if values[-1] < values[0] else "STABLE"

    @staticmethod
    def _direction(values: list[str]) -> str:
        return "STABLE" if len(set(values)) <= 1 else "CHANGED"
