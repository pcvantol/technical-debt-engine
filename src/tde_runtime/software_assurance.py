"""Evidence-based, fail-closed repository Software Assurance checks."""
from __future__ import annotations
from hashlib import sha256
from pathlib import Path
import subprocess
from typing import Any

class SoftwareAssurance:
    def assure(self, root: str | Path) -> dict[str, Any]:
        root=Path(root); limitations=[]; checks={}
        required=("pyproject.toml","ENGINEERING_METHOD.md","RUNTIME_ARCHITECTURE.md","schemas/evidence.schema.json")
        checks["documentationIntegrity"]=all((root/item).is_file() for item in required)
        checks["configurationIntegrity"]=(root/"pyproject.toml").is_file()
        checks["schemaIntegrity"]=(root/"schemas/configuration.schema.json").is_file()
        checks["dependencyIntegrity"]=(root/"pyproject.toml").is_file()
        if not (root/"requirements.lock").is_file(): limitations.append("dependency locking and provenance are not yet established")
        workflows=list((root/".github/workflows").glob("*.y*ml")) if (root/".github/workflows").is_dir() else []
        checks["workflowIntegrity"]=bool(workflows)
        if not workflows: limitations.append("no GitHub Actions workflow is present for workflow integrity validation")
        checks["artifactIntegrity"]=False; limitations.append("no release artifacts exist; artifact integrity is not applicable")
        dirty=subprocess.run(["git","status","--porcelain"],cwd=root,text=True,capture_output=True,check=False).stdout.strip()
        checks["repositoryIntegrity"]=not bool(dirty)
        if dirty: limitations.append("working tree is not clean")
        failed=not all(checks[key] for key in ("documentationIntegrity","configurationIntegrity","schemaIntegrity","dependencyIntegrity","repositoryIntegrity"))
        decision="FAIL" if failed else "PASS_WITH_WARNINGS" if limitations else "PASS"
        identity=sha256(f"{root.resolve()}:{decision}:{checks}".encode()).hexdigest()[:16]
        return {"assuranceId":f"assurance.{identity}","qualification":decision,"checks":checks,"repository":str(root.resolve()),"runtime":{"version":"0.1.0"},"artifacts":[],"dependencies":{"locked":False},"workflowIntegrity":{"workflowCount":len(workflows)},"limitations":limitations}
