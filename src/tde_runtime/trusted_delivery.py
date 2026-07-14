"""Immutable-candidate and evidence validation for Trusted Delivery."""
from __future__ import annotations
from hashlib import sha256
from pathlib import Path
import subprocess
from typing import Any, Mapping

class TrustedDelivery:
    def validate(self, root: str | Path, runtime_evidence: Mapping[str, Any] | None = None) -> dict[str, Any]:
        root=Path(root); limitations=[]
        sha=subprocess.run(["git","rev-parse","HEAD"],cwd=root,text=True,capture_output=True,check=False).stdout.strip()
        clean=not subprocess.run(["git","status","--porcelain"],cwd=root,text=True,capture_output=True,check=False).stdout.strip()
        workflows=list((root/".github/workflows").glob("*.y*ml")) if (root/".github/workflows").is_dir() else []
        checks={"candidateIdentity":bool(sha),"repositoryIntegrity":clean,"workflowIntegrity":bool(workflows),"artifactIntegrity":False,"manifestIntegrity":(root/"RELEASE_MANIFEST.md").is_file(),"evidenceIntegrity":runtime_evidence is not None and runtime_evidence.get("validation",{}).get("status")=="VALID"}
        if not workflows: limitations.append("no immutable GitHub Actions workflow is available for validation")
        if not checks["artifactIntegrity"]: limitations.append("no release artifact exists for checksum or reproducibility validation")
        if not clean: limitations.append("candidate working tree is not clean")
        if not checks["evidenceIntegrity"]: limitations.append("validated runtime evidence is unavailable")
        decision="FAIL" if not checks["candidateIdentity"] or not checks["repositoryIntegrity"] or not checks["manifestIntegrity"] or not checks["evidenceIntegrity"] else "PASS_WITH_WARNINGS" if limitations else "PASS"
        identity=sha256(f"{sha}:{decision}".encode()).hexdigest()[:16]
        return {"trustedDeliveryId":f"trusted-delivery.{identity}","qualification":decision,"candidate":{"sha":sha,"repository":str(root.resolve())},"checks":checks,"artifacts":[],"runtimeEvidenceId":runtime_evidence.get("integrity",{}).get("contentDigest") if runtime_evidence else None,"limitations":limitations}
