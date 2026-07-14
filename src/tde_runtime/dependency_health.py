"""Declarative dependency inventory adapter; does not execute package managers."""
from __future__ import annotations
import json, tomllib
from pathlib import Path
from typing import Any
CAPABILITY_ID="dependency_health"; CAPABILITY_VERSION="0.1.0"
def discover(root: Path) -> dict[str, Any]:
    inventory=[]
    requirements=root/"requirements.txt"
    if requirements.exists():
        for line in requirements.read_text().splitlines():
            name=line.split("==")[0].strip()
            if name and not name.startswith("#"): inventory.append({"identifier":f"pypi:{name}","displayName":name,"ecosystem":"Python","packageManager":"requirements.txt","declaredVersion":line.partition("==")[2] or None,"lockState":"DECLARED"})
    pyproject=root/"pyproject.toml"
    if pyproject.exists():
        data=tomllib.loads(pyproject.read_text()); deps=data.get("project",{}).get("dependencies",[])
        for dep in deps:
            name=dep.split()[0].split(">")[0].split("=")[0]; inventory.append({"identifier":f"pypi:{name}","displayName":name,"ecosystem":"Python","packageManager":"pyproject.toml","declaredVersion":dep,"lockState":"DECLARED"})
    package=root/"package.json"
    if package.exists():
        data=json.loads(package.read_text())
        for name,version in data.get("dependencies",{}).items(): inventory.append({"identifier":f"npm:{name}","displayName":name,"ecosystem":"JavaScript","packageManager":"package.json","declaredVersion":version,"lockState":"DECLARED"})
    return {"status":"VALID","inventory":inventory,"measurements":[{"measurementId":"dependency_health.repository.count","capabilityId":CAPABILITY_ID,"metricKey":"dependency.count","value":len(inventory),"unit":"packages","scope":"repository","targetEntityId":"repository","aggregation":"count","sourceAdapterId":"dependency_health.declarative","sourceToolId":"filesystem"}],"findings":[],"limitations":[]}
