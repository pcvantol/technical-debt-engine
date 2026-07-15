"""Canonical, evidence-only Internal Release certification."""
from __future__ import annotations

from hashlib import sha256
import json
from pathlib import Path
from typing import Any, Mapping


def _canonical(value: object) -> bytes:
    return (json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=True) + "\n").encode("utf-8")


def _read(path: str | Path) -> tuple[dict[str, Any] | None, str | None]:
    try:
        raw = Path(path).read_bytes()
        value = json.loads(raw)
        return (value if isinstance(value, dict) else None), "sha256:" + sha256(raw).hexdigest()
    except (OSError, ValueError, json.JSONDecodeError):
        return None, None


class ReleaseCertification:
    """Certify a qualified candidate by validating, never regenerating, evidence."""

    def certify(self, qualification_path: str | Path, report_output: str | Path) -> dict[str, Any]:
        qualification, digest = _read(qualification_path)
        limitations: list[str] = []
        if qualification is None:
            limitations.append("release qualification evidence is missing or invalid JSON")
            qualification = {}
        elif isinstance(qualification.get("releaseQualificationEvidence"), dict):
            qualification = qualification["releaseQualificationEvidence"]

        candidate = qualification.get("releaseCandidate", {})
        artifacts = qualification.get("artifacts", [])
        manifest = qualification.get("manifest", {})
        runtime = qualification.get("runtimeEvidence", {})
        checks = qualification.get("checks", {})
        release_evidence_reference, release_evidence_digest, release_evidence_integrity = _release_evidence_check(qualification, candidate, checks)
        evidence_checks = {
            "candidateIdentity": isinstance(candidate.get("sha"), str) and len(candidate["sha"]) == 40,
            "artifactIdentity": isinstance(artifacts, list) and bool(artifacts) and all(item.get("digest", "").startswith("sha256:") for item in artifacts if isinstance(item, dict)),
            "artifactIntegrity": bool(checks.get("artifactIntegrity")),
            "artifactReproducibility": bool(checks.get("buildReproducibility")),
            "workflowIntegrity": qualification.get("trustedDelivery", {}).get("decision") == "PASS",
            "softwareAssurance": qualification.get("softwareAssurance", {}).get("decision") == "PASS",
            "trustedDelivery": qualification.get("trustedDelivery", {}).get("decision") == "PASS",
            "releaseQualification": qualification.get("decision") == "RELEASE_QUALIFIED" and qualification.get("releaseDecision") == "READY",
            "buildProvenance": bool(checks.get("buildReproducibility")),
            "canonicalEvidence": bool(digest) and bool(manifest.get("integrity")),
            "releaseEvidence": release_evidence_integrity,
            "runtimeQualification": (runtime.get("validation", {}).get("status") == "VALID"
                                     and runtime.get("runtimeQualification") == "QUALIFIED"),
            "policyEvidence": runtime.get("policyDecision") in {"PASS", "PASS_WITH_WARNINGS"},
            "dockerArtifact": bool(checks.get("dockerArtifact", True)),
        }
        for name, valid in evidence_checks.items():
            if not valid:
                limitations.append(f"required {name} evidence is unavailable, invalid, or did not pass")
        decision = "RELEASE_CERTIFIED" if all(evidence_checks.values()) else "RELEASE_NOT_CERTIFIED"
        report = {
            "schemaId": "tde.release-certification", "schemaVersion": "1.0.0",
            "candidate": candidate, "repository": candidate.get("repository"),
            "certificationInputs": {"releaseQualification": {"path": str(qualification_path), "digest": digest},
                                    "softwareAssuranceId": qualification.get("softwareAssurance", {}).get("assuranceId"),
                                    "trustedDeliveryId": qualification.get("trustedDelivery", {}).get("trustedDeliveryId"),
                                    "manifest": manifest, "artifacts": artifacts, "runtimeEvidence": runtime,
                                    "releaseEvidence": {"reference": release_evidence_reference, "digest": release_evidence_digest}},
            "checks": evidence_checks, "decision": decision, "limitations": limitations,
            "decisionRationale": "All required canonical evidence passed." if decision == "RELEASE_CERTIFIED" else "Certification is fail-closed because required canonical evidence did not pass.",
        }
        report["certificationId"] = "release-certification.sha256." + sha256(_canonical(report)).hexdigest()
        output = Path(report_output).resolve(); output.parent.mkdir(parents=True, exist_ok=True); output.write_bytes(_canonical(report))
        return {**report, "report": {"path": str(output), "digest": "sha256:" + sha256(output.read_bytes()).hexdigest(), "integrity": True}}


def _release_evidence_check(qualification: Mapping[str, Any], candidate: Mapping[str, Any], checks: Mapping[str, Any]) -> tuple[dict[str, Any], str | None, bool]:
    reference = qualification.get("releaseEvidence", {})
    if not isinstance(reference, dict): return {}, None, False
    evidence, digest = _read(reference.get("path", ""))
    if not evidence: return reference, digest, False
    unsigned = {key: value for key, value in evidence.items() if key != "releaseEvidenceId"}
    expected = "release-evidence.sha256." + sha256(_canonical(unsigned)).hexdigest()
    valid = digest == reference.get("digest") and evidence.get("releaseEvidenceId") == reference.get("id")
    valid = valid and evidence.get("releaseEvidenceId") == expected and evidence.get("candidate") == candidate
    return reference, digest, valid and evidence.get("releaseQualification", {}).get("checks") == checks
