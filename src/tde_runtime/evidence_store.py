"""Storage-technology-independent immutable canonical evidence repository."""
from __future__ import annotations
import json
from pathlib import Path
from typing import Any, Mapping

class EvidenceStore:
    def __init__(self, location: str | Path) -> None: self.location = Path(location)
    def persist(self, evidence: Mapping[str, Any], kind: str = "evidence") -> dict[str, Any]:
        if evidence.get("schemaId") != "tde.evidence" or evidence.get("validation", {}).get("status") != "VALID": raise ValueError("store requires validated canonical evidence")
        identity = evidence["integrity"]["contentDigest"].removeprefix("sha256:")
        path = self.location / kind / f"{identity}.json"
        if path.exists(): return {"id": identity, "kind": kind, "path": str(path), "immutable": True, "existing": True}
        path.parent.mkdir(parents=True, exist_ok=True)
        record = {"kind": kind, "repository": evidence["repository"]["id"], "candidate": evidence["candidate"]["id"], "runtime": evidence["runtime"]["version"], "schema": evidence["schemaVersion"], "timestamp": evidence["timestamps"]["generatedAt"], "qualification": evidence.get("policyEvidence", {}).get("decision"), "evidence": evidence}
        path.write_text(json.dumps(record, sort_keys=True, indent=2) + "\n", encoding="utf-8")
        return {"id": identity, "kind": kind, "path": str(path), "immutable": True, "existing": False}
    def history(self, kind: str = "evidence") -> list[dict[str, Any]]:
        directory = self.location / kind
        records=[]
        for path in sorted(directory.glob("*.json")) if directory.is_dir() else []:
            records.append(json.loads(path.read_text(encoding="utf-8")))
        return sorted(records, key=lambda item: item["timestamp"])
