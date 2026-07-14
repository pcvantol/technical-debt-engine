"""Derived Maintainability capability; consumes canonical Code Size and Complexity observations only."""
from __future__ import annotations
from typing import Any
CAPABILITY_ID="maintainability"; CAPABILITY_VERSION="0.1.0"
def derive(code_size: dict[str, Any], complexity: dict[str, Any]) -> dict[str, Any]:
    code=next((m["value"] for m in code_size.get("measurements",[]) if m["metricKey"]=="code_size.code_lines"),None)
    complexity_value=next((m["value"] for m in complexity.get("measurements",[]) if m["metricKey"]=="complexity.cyclomatic.average"),None)
    if code is None or complexity_value is None: return {"status":"BLOCKED","limitations":[{"id":"maintainability.dependencies","description":"Validated Code Size and Complexity evidence is required.","cause":"missing dependency evidence"}]}
    index=max(0.0, min(100.0, 100.0 - complexity_value * 3.0 - (code / 1000.0)))
    metric={"measurementId":"maintainability.repository.index","capabilityId":CAPABILITY_ID,"metricKey":"maintainability.index","value":index,"unit":"index","scope":"repository","targetEntityId":"repository","aggregation":"mean","sourceAdapterId":"derived.maintainability","sourceToolId":"canonical_evidence"}
    return {"status":"VALID","measurements":[metric],"findings":[],"limitations":[]}
