"""Canonical, evidence-only Trusted Delivery validation."""
from __future__ import annotations

from hashlib import sha256
import json
from pathlib import Path
import re
import subprocess
from typing import Any, Mapping

MANIFEST_SCHEMA_ID = "tde.trusted-delivery-manifest"
MANIFEST_SCHEMA_VERSION = "1.0.0"
_SHA256 = re.compile(r"^sha256:[0-9a-f]{64}$")
_GIT_SHA = re.compile(r"^[0-9a-f]{40}$")


def _canonical(value: object) -> bytes:
    return (json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=True) + "\n").encode("utf-8")


def _git(root: Path, *arguments: str) -> tuple[bool, str]:
    completed = subprocess.run(["git", "-C", str(root), *arguments], text=True, capture_output=True, check=False)
    return completed.returncode == 0, completed.stdout.strip()


class TrustedDelivery:
    """Bind a candidate to assurance, artifact, manifest, and workflow evidence.

    This layer deliberately consumes Software Assurance evidence instead of
    re-evaluating assurance rules or making a release/publication decision.
    """

    def validate(self, root: str | Path, runtime_evidence: Mapping[str, Any] | None,
                 assurance_evidence: Mapping[str, Any] | None = None, manifest: str | Path | None = None) -> dict[str, Any]:
        root = Path(root).resolve(); limitations: list[str] = []
        candidate = self._candidate(root, limitations)
        manifest_evidence = self._manifest(Path(manifest).resolve() if manifest else None, candidate, limitations)
        assurance = self._assurance(assurance_evidence, limitations)
        artifacts = self._artifacts(manifest_evidence, assurance, limitations)
        workflow = self._workflow(root, assurance, limitations)
        runtime_ok = runtime_evidence is not None and runtime_evidence.get("validation", {}).get("status") == "VALID"
        if not runtime_ok:
            limitations.append("validated Runtime evidence is unavailable")
        checks = {
            "candidateIntegrity": candidate["integrity"],
            "manifestIntegrity": manifest_evidence["integrity"],
            "artifactIntegrity": artifacts["integrity"],
            "workflowIntegrity": workflow["integrity"],
            "softwareAssuranceIntegrity": assurance["integrity"],
            "runtimeEvidenceIntegrity": runtime_ok,
            "buildProvenanceValidation": artifacts["provenanceValidated"],
        }
        # An omitted external delivery manifest/artifact is a bounded
        # pre-release limitation. An explicitly supplied invalid input fails
        # closed; candidate, Runtime, and assurance failures always fail.
        required = ("candidateIntegrity", "softwareAssuranceIntegrity", "runtimeEvidenceIntegrity")
        invalid_input = manifest is not None and (not checks["manifestIntegrity"] or not checks["artifactIntegrity"])
        decision = "FAIL" if not all(checks[name] for name in required) or invalid_input else "PASS_WITH_WARNINGS" if limitations else "PASS"
        evidence = {
            "schemaId": "tde.trusted-delivery", "schemaVersion": "1.0.0", "candidate": candidate,
            "manifest": manifest_evidence, "artifacts": artifacts, "workflow": workflow,
            "softwareAssurance": {"assuranceId": assurance.get("assuranceId"), "decision": assurance.get("decision")},
            "runtimeEvidenceId": runtime_evidence.get("integrity", {}).get("contentDigest") if runtime_evidence else None,
            "checks": checks, "limitations": limitations, "decision": decision, "qualification": decision,
        }
        evidence["trustedDeliveryId"] = "trusted-delivery.sha256." + sha256(_canonical(evidence)).hexdigest()
        return evidence

    @staticmethod
    def _candidate(root: Path, limitations: list[str]) -> dict[str, Any]:
        sha_ok, sha = _git(root, "rev-parse", "HEAD"); _, branch = _git(root, "branch", "--show-current")
        _, repository = _git(root, "config", "--get", "remote.origin.url"); status_ok, dirty = _git(root, "status", "--porcelain")
        integrity = sha_ok and bool(_GIT_SHA.fullmatch(sha)) and bool(branch) and status_ok and not dirty
        if not integrity:
            limitations.append("candidate SHA, repository branch, or clean working tree is invalid")
        return {"sha": sha or None, "candidateIdentity": "candidate.git." + sha if sha else None,
                "repository": repository or "local", "branch": branch or None, "workingTreeClean": not bool(dirty),
                "integrity": integrity}

    @staticmethod
    def _manifest(path: Path | None, candidate: Mapping[str, Any], limitations: list[str]) -> dict[str, Any]:
        if path is None:
            limitations.append("no delivery manifest was supplied; manifest and artifact references were not evaluated")
            return {"path": None, "identity": None, "integrity": False, "supplied": False, "artifacts": []}
        try:
            raw = path.read_bytes(); value = json.loads(raw)
            items = value["artifacts"]
            valid = (value.get("schemaId") == MANIFEST_SCHEMA_ID and value.get("schemaVersion") == MANIFEST_SCHEMA_VERSION
                     and value.get("candidate", {}).get("sha") == candidate["sha"]
                     and value.get("candidate", {}).get("repository") == candidate["repository"]
                     and value.get("candidate", {}).get("branch") == candidate["branch"]
                     and isinstance(items, list) and bool(items)
                     and all(isinstance(item, dict) and isinstance(item.get("filename"), str) and _SHA256.fullmatch(item.get("digest", "")) for item in items))
        except (OSError, ValueError, KeyError, TypeError, json.JSONDecodeError):
            raw = b""; value = {}; items = []; valid = False
        if not valid:
            limitations.append("supplied delivery manifest does not meet the canonical schema, candidate, or checksum requirements")
        return {"path": str(path), "identity": "manifest.sha256." + sha256(raw).hexdigest() if raw else None,
                "schemaId": value.get("schemaId"), "schemaVersion": value.get("schemaVersion"), "supplied": True,
                "candidate": value.get("candidate"), "artifacts": items, "integrity": valid}

    @staticmethod
    def _assurance(evidence: Mapping[str, Any] | None, limitations: list[str]) -> Mapping[str, Any]:
        valid = (evidence is not None and evidence.get("schemaId") == "tde.software-assurance"
                 and isinstance(evidence.get("assuranceId"), str) and evidence.get("decision") != "FAIL")
        if not valid:
            limitations.append("canonical Software Assurance evidence is unavailable or failed")
            return {"integrity": False}
        return {**evidence, "integrity": True}

    @staticmethod
    def _artifacts(manifest: Mapping[str, Any], assurance: Mapping[str, Any], limitations: list[str]) -> dict[str, Any]:
        records = [artifact for directory in assurance.get("artifacts", {}).get("records", []) for artifact in directory.get("artifacts", [])]
        supplied = bool(manifest.get("supplied"))
        if not supplied:
            return {"records": [], "integrity": False, "provenanceValidated": False}
        expected = {(item["filename"], item["digest"]) for item in manifest.get("artifacts", [])}
        actual = {(item.get("filename"), item.get("digest")) for item in records}
        integrity = bool(assurance.get("checks", {}).get("artifactIntegrity")) and expected == actual
        if not integrity:
            limitations.append("manifest artifact references do not match checksum-verified, reproducible assurance artifacts")
        return {"records": sorted(records, key=lambda item: item["filename"]), "integrity": integrity,
                "provenanceValidated": integrity and bool(assurance.get("checks", {}).get("buildProvenanceVerification"))}

    @staticmethod
    def _workflow(root: Path, assurance: Mapping[str, Any], limitations: list[str]) -> dict[str, Any]:
        directory = root / ".github" / "workflows"
        records = [{"path": str(item.relative_to(root)), "digest": "sha256:" + sha256(item.read_bytes()).hexdigest()}
                   for item in sorted(directory.glob("*.y*ml"))] if directory.is_dir() else []
        workflow = assurance.get("workflows", {})
        integrity = bool(workflow.get("immutableActions")) and bool(workflow.get("leastPrivilege")) and bool(records)
        if not integrity:
            limitations.append("workflow provenance, immutable actions, or least-privilege evidence is unavailable")
        return {"records": records, "immutableActions": bool(workflow.get("immutableActions")),
                "leastPrivilege": bool(workflow.get("leastPrivilege")), "integrity": integrity}
