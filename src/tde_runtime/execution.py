"""Sequential, dependency-aware coordinator for registered capabilities."""
from __future__ import annotations
from time import perf_counter
from typing import Any
from .code_size import analyze, CAPABILITY_ID, CAPABILITY_VERSION
from .complexity import analyze as analyze_complexity
from .maintainability import derive as derive_maintainability
from .dependency_health import discover as discover_dependencies

class CapabilityExecutionEngine:
    states=("PLANNED","READY","RUNNING","COMPLETED","FAILED","BLOCKED","SKIPPED","NOT_SUPPORTED")
    def plan(self, context: Any) -> dict[str, Any]:
        requested=context.configuration.get("executionOptions",{}).get("capabilities",{})
        enabled=[key for key,value in requested.items() if value.get("enabled")]
        order=[item for item in ("code_size","complexity","maintainability","dependency_health") if item in enabled or (item in {"code_size","complexity"} and "maintainability" in enabled)]
        return {"state":"PLANNED","capabilities":order,"parallelReady":True,"retries":"NONE"}
    def execute(self, context: Any) -> dict[str, Any]:
        started=perf_counter(); plan=self.plan(context); requested=context.configuration.get("executionOptions",{}).get("capabilities",{})
        # Existing capability implementations remain isolated; only this engine coordinates them.
        if not plan["capabilities"]: result={"executedWorkItems":0,"measurements":[],"findings":[],"capabilityResults":[]}
        elif requested.get("dependency_health",{}).get("enabled"):
            item=discover_dependencies(context.repository_root); result={"executedWorkItems":1,"measurements":item["measurements"],"findings":item["findings"],"capabilityResults":[{"capabilityId":"dependency_health","capabilityVersion":"0.1.0","status":"VALID","completeness":1,"qualificationApplicable":True}]}
        elif requested.get("maintainability",{}).get("enabled"):
            code=self._code(context,analyze(context.repository_root)); complexity=analyze_complexity(context.repository_root); derived=derive_maintainability(code,{"measurements":complexity.get("measurements",[])})
            result={"executedWorkItems":3,"measurements":code["measurements"]+complexity.get("measurements",[])+derived.get("measurements",[]),"findings":code["findings"]+complexity.get("findings",[]),"capabilityResults":code["capabilityResults"]+[{"capabilityId":"complexity","status":complexity["status"],"completeness":1,"qualificationApplicable":True},{"capabilityId":"maintainability","status":derived["status"],"completeness":1,"qualificationApplicable":True}]}
        elif requested.get("complexity",{}).get("enabled"):
            item=analyze_complexity(context.repository_root); result={"executedWorkItems":1,"measurements":item.get("measurements",[]),"findings":item.get("findings",[]),"capabilityResults":[{"capabilityId":"complexity","status":item["status"],"completeness":1,"qualificationApplicable":True}]}
        else: result=self._code(context,analyze(context.repository_root))
        result["executionEvidence"]={"executionId":context.execution_id,"plannedCapabilities":plan["capabilities"],"executedCapabilities":[x["capabilityId"] for x in result["capabilityResults"]],"executionOrder":plan["capabilities"],"durationMs":int((perf_counter()-started)*1000),"state":"COMPLETED","limitations":[]}
        return result
    def _code(self,context:Any,result:dict[str,Any])->dict[str,Any]:
        if result["status"]!="VALID": return {"executedWorkItems":1,"measurements":[],"findings":[],"capabilityResults":[{"capabilityId":CAPABILITY_ID,"capabilityVersion":CAPABILITY_VERSION,"status":"BLOCKED","completeness":0,"qualificationApplicable":False,"limitations":result["limitations"]}]}
        metrics=[]; names={"files":"file_count","code":"code_lines","comment":"comment_lines","blank":"blank_lines","source":"source_lines","test":"test_lines","generated":"generated_lines","vendor":"vendor_lines","documentation":"documentation_lines"}
        for key,value in result["totals"].items():
            if key in names: metrics.append({"measurementId":f"code_size.repository.{key}","capabilityId":CAPABILITY_ID,"metricKey":f"code_size.{names[key]}","value":value,"unit":"files" if key=="files" else "lines","scope":"repository","targetEntityId":context.repository_id,"aggregation":"sum"})
        return {"executedWorkItems":1,"measurements":metrics,"findings":[],"capabilityResults":[{"capabilityId":CAPABILITY_ID,"capabilityVersion":CAPABILITY_VERSION,"status":"VALID","adapterIds":[result["adapter"]["id"]],"completeness":1,"qualificationApplicable":True}]}
