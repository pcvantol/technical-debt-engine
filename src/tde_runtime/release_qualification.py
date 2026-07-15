"""Evidence-only release qualification with explicit capability selection."""
from __future__ import annotations

from hashlib import sha256
import json
from pathlib import Path
import subprocess
from typing import Any, Mapping, Sequence

from .runtime import EVIDENCE_SCHEMA_VERSION, RUNTIME_VERSION
from .software_assurance import SoftwareAssurance
from .trusted_delivery import TrustedDelivery


def _git(root: Path, *args: str) -> str:
    return subprocess.run(["git", "-C", str(root), *args], text=True, capture_output=True, check=False).stdout.strip()


def _canonical(value: Mapping[str, Any]) -> bytes:
    return (json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=True) + "\n").encode()


def _write(path: Path, value: Mapping[str, Any]) -> str:
    raw = _canonical(value)
    if path.exists() and path.read_bytes() != raw:
        raise ValueError(f"refusing to overwrite immutable release evidence: {path}")
    path.write_bytes(raw)
    return "sha256:" + sha256(raw).hexdigest()


class ReleaseQualification:
    """Compose already-generated evidence into a qualified, immutable release record."""

    def qualify(self, root: str | Path, runtime_evidence: Mapping[str, Any], artifact_directories: Sequence[str | Path],
                manifest_output: str | Path, selected_capabilities: Sequence[str] = ()) -> dict[str, Any]:
        root = Path(root).resolve()
        output = Path(manifest_output).resolve()
        output.parent.mkdir(parents=True, exist_ok=True)
        selection = sorted(set(selected_capabilities))
        assurance = SoftwareAssurance().assure(root, list(artifact_directories))
        candidate = {
            "sha": _git(root, "rev-parse", "HEAD"),
            "repository": _git(root, "config", "--get", "remote.origin.url") or "local",
            "branch": _git(root, "branch", "--show-current"),
            "runtimeVersion": RUNTIME_VERSION,
            "schemaVersion": EVIDENCE_SCHEMA_VERSION,
            "selectedCapabilities": selection,
            "policyVersion": runtime_evidence.get("policyEvidence", {}).get("policy", {}).get("version"),
        }
        artifacts = [item for record in assurance["artifacts"]["records"] for item in record["artifacts"]]
        delivery_manifest = {"schemaId": "tde.trusted-delivery-manifest", "schemaVersion": "1.0.0",
                             "candidate": {key: candidate[key] for key in ("sha", "repository", "branch")}, "artifacts": artifacts}
        delivery_path = output.with_name(output.stem + ".trusted-delivery.json")
        _write(delivery_path, delivery_manifest)
        delivery = TrustedDelivery().validate(root, runtime_evidence, assurance, delivery_path)
        qualification = runtime_evidence.get("runtimeQualification", {})
        policy = runtime_evidence.get("policyEvidence", {})
        executed = set(runtime_evidence.get("executionEvidence", {}).get("executedCapabilities", []))
        required_executed = bool(selection) and set(selection).issubset(executed)
        checks = {
            "candidateIdentity": bool(candidate["sha"]),
            "capabilitySelection": bool(selection),
            "artifactIntegrity": assurance["checks"]["artifactIntegrity"],
            "buildReproducibility": assurance["checks"]["buildProvenanceVerification"],
            "softwareAssurance": assurance["decision"] == "PASS",
            "trustedDelivery": delivery["decision"] == "PASS",
            "runtimeEvidence": runtime_evidence.get("validation", {}).get("status") == "VALID",
            "requiredCapabilitiesExecuted": required_executed,
            "runtimeQualification": qualification.get("level") == "QUALIFIED",
            "policyEvidence": policy.get("decision") in {"PASS", "PASS_WITH_WARNINGS"},
        }
        ready = all(checks.values())
        decision = "RELEASE_QUALIFIED" if ready else "RELEASE_BLOCKED"
        runtime_record = {
            "selection": selection,
            "evidenceId": runtime_evidence.get("integrity", {}).get("contentDigest"),
            "validation": runtime_evidence.get("validation", {}),
            "execution": runtime_evidence.get("executionEvidence", {}),
            "qualification": qualification,
        }
        policy_record = {"decision": policy.get("decision"), "policy": policy.get("policy"),
                         "triggeredRules": policy.get("triggeredRules", []), "evidenceId": runtime_record["evidenceId"]}
        release_evidence = {
            "schemaId": "tde.release-evidence", "schemaVersion": "1.0.0", "candidate": candidate,
            "artifacts": artifacts, "runtimeQualification": runtime_record, "policyEvidence": policy_record,
            "softwareAssurance": {"assuranceId": assurance["assuranceId"], "decision": assurance["decision"]},
            "trustedDelivery": {"trustedDeliveryId": delivery["trustedDeliveryId"], "decision": delivery["decision"]},
            "releaseQualification": {"decision": decision, "releaseDecision": "READY" if ready else "NOT_READY", "checks": checks},
        }
        release_evidence["releaseEvidenceId"] = "release-evidence.sha256." + sha256(_canonical(release_evidence)).hexdigest()
        evidence_path = output.with_name(output.stem + ".release-evidence.json")
        evidence_digest = _write(evidence_path, release_evidence)
        manifest = {
            "schemaId": "tde.release-qualification-manifest", "schemaVersion": "1.0.0", "candidate": candidate,
            "artifacts": artifacts, "softwareAssuranceId": assurance["assuranceId"], "trustedDeliveryId": delivery["trustedDeliveryId"],
            "releaseEvidence": {"path": str(evidence_path), "digest": evidence_digest, "id": release_evidence["releaseEvidenceId"], "integrity": True},
            "qualification": {"decision": decision, "checks": checks},
        }
        digest = _write(output, manifest)
        return {
            "schemaId": "tde.release-qualification", "schemaVersion": "1.0.0", "releaseCandidate": candidate,
            "manifest": {"path": str(output), "digest": digest, "integrity": True}, "artifacts": artifacts,
            "softwareAssurance": release_evidence["softwareAssurance"], "trustedDelivery": release_evidence["trustedDelivery"],
            "runtimeEvidence": {"validation": runtime_record["validation"], "policyDecision": policy_record["decision"],
                                "runtimeQualification": qualification.get("level"), "identity": runtime_record["evidenceId"]},
            "releaseEvidence": manifest["releaseEvidence"], "checks": checks,
            "releaseDecision": "READY" if ready else "NOT_READY", "decision": decision,
        }
