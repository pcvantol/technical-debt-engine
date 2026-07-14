"""Storage-technology-independent immutable canonical evidence repository."""
from __future__ import annotations
from hashlib import sha256
import json
from pathlib import Path
from typing import Any, Mapping

class EvidenceStore:
    def __init__(self, location: str | Path) -> None: self.location = Path(location)

    @staticmethod
    def _identity(evidence: Mapping[str, Any]) -> str:
        digest = evidence.get("integrity", {}).get("contentDigest", "")
        if not isinstance(digest, str) or not digest.startswith("sha256:"):
            raise ValueError("evidence integrity digest is missing")
        return digest.removeprefix("sha256:")

    @staticmethod
    def _calculated_identity(evidence: Mapping[str, Any]) -> str:
        stable_results = [{key: value for key, value in result.items() if key != "executionTiming"}
                          for result in evidence.get("capabilityResults", [])]
        seed = json.dumps({"repository": evidence.get("repository", {}).get("id"),
                           "candidate": evidence.get("candidate"),
                           "configuration": evidence.get("configurationDigest"),
                           "capabilityResults": stable_results,
                           "measurements": evidence.get("measurements", []),
                           "findings": evidence.get("findings", []),
                           "policy": evidence.get("policyEvidence", {})},
                          sort_keys=True, separators=(",", ":"), default=str)
        return sha256(seed.encode()).hexdigest()

    @classmethod
    def _validate(cls, evidence: Mapping[str, Any], identity: str | None = None) -> str:
        if evidence.get("schemaId") != "tde.evidence" or evidence.get("validation", {}).get("status") != "VALID":
            raise ValueError("store requires validated canonical evidence")
        actual = cls._identity(evidence)
        if identity and identity != actual:
            raise ValueError("persisted evidence identity does not match its record")
        if cls._calculated_identity(evidence) != actual:
            raise ValueError("persisted evidence integrity check failed")
        return actual

    def persist(self, evidence: Mapping[str, Any], kind: str = "evidence") -> dict[str, Any]:
        identity = self._validate(evidence)
        path = self.location / kind / f"{identity}.json"
        if path.exists(): return {"id": identity, "kind": kind, "path": str(path), "immutable": True, "existing": True}
        path.parent.mkdir(parents=True, exist_ok=True)
        record = {"kind": kind, "repository": evidence["repository"]["id"], "candidate": evidence["candidate"]["id"], "runtime": evidence["runtime"]["version"], "schema": evidence["schemaVersion"], "timestamp": evidence["timestamps"]["generatedAt"], "qualification": evidence.get("policyEvidence", {}).get("decision"), "evidence": evidence}
        path.write_text(json.dumps(record, sort_keys=True, indent=2) + "\n", encoding="utf-8")
        return {"id": identity, "kind": kind, "path": str(path), "immutable": True, "existing": False}

    def retrieve(self, identity: str, kind: str = "evidence") -> dict[str, Any]:
        path = self.location / kind / f"{identity}.json"
        try:
            record = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as error:
            raise ValueError(f"persisted evidence is unavailable: {identity}") from error
        if record.get("kind") != kind or not isinstance(record.get("evidence"), dict):
            raise ValueError("persisted evidence record is malformed")
        self._validate(record["evidence"], identity)
        return record

    def history(self, kind: str = "evidence") -> list[dict[str, Any]]:
        directory = self.location / kind
        records=[]
        for path in sorted(directory.glob("*.json")) if directory.is_dir() else []:
            identity = path.stem
            records.append(self.retrieve(identity, kind))
        return sorted(records, key=lambda item: item["timestamp"])
