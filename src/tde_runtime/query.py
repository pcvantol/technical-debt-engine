"""Versioned, read-only query layer over canonical evidence."""
from __future__ import annotations
from hashlib import sha256
from time import perf_counter
from typing import Any, Mapping

QUERY_LANGUAGE_VERSION = "1.0.0"

class QueryEngine:
    def execute(self, evidence: Mapping[str, Any], query: Mapping[str, Any]) -> dict[str, Any]:
        started = perf_counter()
        resource = query.get("resource", "repositories")
        comparisons = list(query.get("comparisons", []))
        comparison_findings = [
            {"comparisonId": item.get("comparisonId"), **transition}
            for item in comparisons for transition in item.get("comparison", {}).get("findingTransitions", [])
        ]
        collections = {"repositories": [evidence.get("repository", {})], "capabilities": evidence.get("capabilityResults", []), "metrics": evidence.get("measurements", []), "findings": evidence.get("findings", []), "policies": [evidence.get("policyEvidence", {})], "qualification": [evidence.get("policyEvidence", {})], "baselines": query.get("baselines", []), "comparisons": comparisons, "comparison_findings": comparison_findings, "trends": query.get("trends", [])}
        if resource not in collections: raise ValueError(f"unsupported query resource: {resource}")
        rows = list(collections[resource])
        for key, expected in query.get("filter", {}).items(): rows = [row for row in rows if str(row.get(key)) == str(expected)]
        sort = query.get("sort")
        if sort: rows.sort(key=lambda row: str(row.get(sort, "")), reverse=query.get("descending", False))
        aggregate = query.get("aggregate")
        if aggregate == "count": rows = [{"count": len(rows)}]
        group = query.get("groupBy")
        if group:
            grouped: dict[str, int] = {}
            for row in rows: grouped[str(row.get(group, ""))] = grouped.get(str(row.get(group, "")), 0) + 1
            rows = [{group: key, "count": value} for key, value in sorted(grouped.items())]
        projection = query.get("projection")
        if projection: rows = [{key: row.get(key) for key in projection} for row in rows]
        offset, limit = int(query.get("offset", 0)), query.get("limit")
        rows = rows[offset: offset + int(limit) if limit is not None else None]
        identity = sha256(str(sorted(query.items())).encode()).hexdigest()[:16]
        return {"queryEvidence": {"queryId": f"query.{identity}", "languageVersion": QUERY_LANGUAGE_VERSION, "resource": resource, "execution": "READ_ONLY", "durationMs": int((perf_counter()-started)*1000), "resultCount": len(rows), "limitations": []}, "results": rows}
