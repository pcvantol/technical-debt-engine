"""Evidence-only operational release qualification."""
from __future__ import annotations

from hashlib import sha256
import json
from pathlib import Path
import subprocess
from typing import Any, Mapping

from .runtime import EVIDENCE_SCHEMA_VERSION, RUNTIME_VERSION
from .software_assurance import SoftwareAssurance
from .trusted_delivery import TrustedDelivery


def _git(root: Path, *args: str) -> str:
    return subprocess.run(["git", "-C", str(root), *args], text=True, capture_output=True, check=False).stdout.strip()


def _write(path: Path, value: Mapping[str, Any]) -> str:
    raw = (json.dumps(value, sort_keys=True, separators=(",", ":")) + "\n").encode()
    path.write_bytes(raw)
    return "sha256:" + sha256(raw).hexdigest()


class ReleaseQualification:
    """Compose existing assurance and delivery evidence; never publish."""

    def qualify(self, root: str | Path, runtime_evidence: Mapping[str, Any], artifact_directories: list[str | Path],
                manifest_output: str | Path) -> dict[str, Any]:
        root = Path(root).resolve(); output = Path(manifest_output).resolve(); output.parent.mkdir(parents=True, exist_ok=True)
        assurance = SoftwareAssurance().assure(root, artifact_directories)
        candidate = {"sha": _git(root, "rev-parse", "HEAD"), "repository": _git(root, "config", "--get", "remote.origin.url") or "local",
                     "branch": _git(root, "branch", "--show-current"), "runtimeVersion": RUNTIME_VERSION,
                     "schemaVersion": EVIDENCE_SCHEMA_VERSION, "capabilityVersions": ["code_size", "complexity"], "policyVersion": "1.0.0"}
        artifacts = [item for record in assurance["artifacts"]["records"] for item in record["artifacts"]]
        delivery_manifest = {"schemaId": "tde.trusted-delivery-manifest", "schemaVersion": "1.0.0",
                             "candidate": {key: candidate[key] for key in ("sha", "repository", "branch")}, "artifacts": artifacts}
        delivery_path = output.with_name(output.stem + ".trusted-delivery.json")
        _write(delivery_path, delivery_manifest)
        delivery = TrustedDelivery().validate(root, runtime_evidence, assurance, delivery_path)
        checks = {"candidateIdentity": bool(candidate["sha"]), "artifactIntegrity": assurance["checks"]["artifactIntegrity"],
                  "buildReproducibility": assurance["checks"]["buildProvenanceVerification"],
                  "softwareAssurance": assurance["decision"] == "PASS", "trustedDelivery": delivery["decision"] == "PASS",
                  "runtimeEvidence": runtime_evidence.get("validation", {}).get("status") == "VALID"}
        ready = all(checks.values()); decision = "RELEASE_QUALIFIED" if ready else "RELEASE_BLOCKED"
        manifest = {"schemaId": "tde.release-qualification-manifest", "schemaVersion": "1.0.0", "candidate": candidate,
                    "artifacts": artifacts, "softwareAssuranceId": assurance["assuranceId"], "trustedDeliveryId": delivery["trustedDeliveryId"],
                    "qualification": {"decision": decision, "checks": checks}}
        digest = _write(output, manifest)
        return {"schemaId": "tde.release-qualification", "schemaVersion": "1.0.0", "releaseCandidate": candidate,
                "manifest": {"path": str(output), "digest": digest, "integrity": True}, "artifacts": artifacts,
                "softwareAssurance": {"assuranceId": assurance["assuranceId"], "decision": assurance["decision"]},
                "trustedDelivery": {"trustedDeliveryId": delivery["trustedDeliveryId"], "decision": delivery["decision"]},
                "checks": checks, "releaseDecision": "READY" if ready else "NOT_READY", "decision": decision}
