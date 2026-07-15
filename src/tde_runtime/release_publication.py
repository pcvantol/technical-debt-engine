"""Read-only validation for publication of a certified release bundle."""
from __future__ import annotations

from hashlib import sha256
import json
from pathlib import Path
from typing import Any, Mapping

from .release_bundle import digest, verify


PUBLICATION_TARGETS = frozenset({"github_release", "pypi", "docker_hub"})
REQUIRED_CONTENT_KINDS = frozenset({
    "wheel", "source_distribution", "oci_archive", "docker_provenance",
    "release_manifest", "release_qualification", "release_certification", "release_evidence",
})


def canonical(value: Mapping[str, Any]) -> bytes:
    return (json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=True) + "\n").encode("utf-8")


def validate_authorization(value: object, candidate_sha: str, release_version: str,
                           bundle_id: str, bundle_checksum: str) -> list[str]:
    """Validate the shape and binding of an authorization assertion, not its approval."""
    if not isinstance(value, dict):
        return ["authorization must be a JSON object"]
    errors = []
    for key in ("authorizedBy", "authorizedAt", "candidateSha", "releaseVersion", "bundleId", "bundleChecksum", "targets"):
        if key not in value: errors.append(f"authorization is missing {key}")
    if errors: return errors
    if not isinstance(value["authorizedBy"], str) or not value["authorizedBy"].strip(): errors.append("authorization authorizedBy must be non-empty")
    if not isinstance(value["authorizedAt"], str) or not value["authorizedAt"].strip(): errors.append("authorization authorizedAt must be non-empty")
    expected = {"candidateSha": candidate_sha, "releaseVersion": release_version,
                "bundleId": bundle_id, "bundleChecksum": bundle_checksum}
    for key, expected_value in expected.items():
        if value[key] != expected_value: errors.append(f"authorization {key} does not bind the selected bundle")
    if not isinstance(value["targets"], list) or set(value["targets"]) != PUBLICATION_TARGETS or len(value["targets"]) != len(PUBLICATION_TARGETS):
        errors.append("authorization targets must be exactly github_release, pypi, and docker_hub")
    return errors


def _report(value: object) -> Mapping[str, Any]:
    if not isinstance(value, dict): raise ValueError("evidence must be a JSON object")
    return value.get("releaseQualificationEvidence", value) if isinstance(value.get("releaseQualificationEvidence", value), dict) else value


def verify_publication_bundle(root: str | Path, candidate_sha: str, release_version: str,
                              authorization: object) -> dict[str, Any]:
    """Validate existing bundle/evidence and return deterministic preflight evidence."""
    directory = Path(root)
    verified = verify(directory)
    bundle = verified["bundle"]
    errors: list[str] = []
    if not verified["integrity"]: errors.append("bundle checksum or required bundle files are invalid")
    if not verified["complete"]: errors.append("bundle is incomplete")
    if bundle.get("candidateSha") != candidate_sha: errors.append("bundle candidate SHA does not match workflow input")
    if bundle.get("bundleVersion") != release_version: errors.append("bundle version does not match workflow input")
    contents = bundle.get("contents", [])
    by_kind = {item.get("kind"): item for item in contents if isinstance(item, dict)} if isinstance(contents, list) else {}
    missing = sorted(REQUIRED_CONTENT_KINDS - set(by_kind))
    if missing: errors.append("bundle is missing required identities: " + ", ".join(missing))
    for kind, item in by_kind.items():
        filename, expected = item.get("filename"), item.get("digest")
        if not isinstance(filename, str) or not isinstance(expected, str) or not (directory / filename).is_file() or digest(directory / filename) != expected:
            errors.append(f"artifact identity is invalid: {kind}")
    qualification = certification = {}
    try:
        qualification = _report(json.loads((directory / by_kind["release_qualification"]["filename"]).read_text(encoding="utf-8")))
        certification = _report(json.loads((directory / by_kind["release_certification"]["filename"]).read_text(encoding="utf-8")))
        if qualification.get("decision") != "RELEASE_QUALIFIED" or qualification.get("releaseDecision") != "READY": errors.append("release qualification is not READY")
        qualified_sha = qualification.get("releaseCandidate", {}).get("sha")
        certified_sha = certification.get("candidate", {}).get("sha")
        if qualified_sha != candidate_sha or certified_sha != candidate_sha: errors.append("qualification or certification candidate identity does not match")
        if certification.get("decision") != "RELEASE_CERTIFIED": errors.append("release certification is not certified")
    except (OSError, KeyError, TypeError, ValueError, json.JSONDecodeError):
        errors.append("release qualification or certification evidence is unreadable")
    errors.extend(validate_authorization(authorization, candidate_sha, release_version,
                                         str(bundle.get("bundleId", "")), str(bundle.get("bundleChecksum", ""))))
    evidence = {"schemaId": "tde.internal-release-publication-preflight", "schemaVersion": "1.0.0",
                "candidateSha": candidate_sha, "releaseVersion": release_version,
                "bundleId": bundle.get("bundleId"), "bundleChecksum": bundle.get("bundleChecksum"),
                "bundleIntegrity": verified["integrity"], "bundleComplete": verified["complete"],
                "publicationTargets": sorted(PUBLICATION_TARGETS), "dryRun": True,
                "authorizationStructureValid": not validate_authorization(authorization, candidate_sha, release_version, str(bundle.get("bundleId", "")), str(bundle.get("bundleChecksum", ""))),
                "decision": "PUBLICATION_PREFLIGHT_READY" if not errors else "PUBLICATION_PREFLIGHT_BLOCKED", "errors": errors}
    unsigned = dict(evidence)
    evidence["publicationEvidenceId"] = "publication-preflight.sha256." + sha256(canonical(unsigned)).hexdigest()
    return evidence
