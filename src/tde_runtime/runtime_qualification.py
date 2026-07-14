"""Evidence-only assessment of Runtime analysis trustworthiness."""
from __future__ import annotations
from hashlib import sha256
from typing import Any, Mapping

class RuntimeQualificationEngine:
    levels=("QUALIFIED","PARTIALLY_QUALIFIED","BLOCKED","NOT_SUPPORTED")
    def qualify(self,evidence:Mapping[str,Any],capability:str|None=None)->dict[str,Any]:
        limitations=[]; results=evidence.get("capabilityResults",[])
        if evidence.get("validation",{}).get("status")!="VALID": limitations.append("evidence validation failed")
        selected=[item for item in results if capability is None or item.get("capabilityId")==capability]
        if capability and not selected: level="NOT_SUPPORTED"; limitations.append("requested capability is absent")
        else:
            blocked=[item for item in selected if item.get("status") in {"BLOCKED","FAILED"}]
            partial=[item for item in selected if item.get("completeness",1)<1 or item.get("status")=="PARTIAL"]
            level="BLOCKED" if limitations or blocked else "PARTIALLY_QUALIFIED" if partial else "QUALIFIED"
        confidence=0 if level in {"BLOCKED","NOT_SUPPORTED"} else 0.75 if level=="PARTIALLY_QUALIFIED" else 1.0
        identity=sha256(f"{evidence.get('integrity',{}).get('contentDigest')}:{capability}".encode()).hexdigest()[:16]
        return {"qualificationId":f"runtime-qualification.{identity}","level":level,"confidence":{"analysis":confidence,"repository":confidence,"capability":confidence},"limitations":limitations,"missingCapabilities":[],"missingAdapters":[],"unsupportedLanguages":[],"supportingEvidence":{"executionId":evidence.get("executionId"),"policy":evidence.get("policyEvidence",{}),"capabilityCount":len(selected)}}
