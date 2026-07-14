"""Python Complexity adapter backed by explicitly installed Radon."""
from __future__ import annotations
import json, subprocess, sys
from hashlib import sha256
from pathlib import Path
from statistics import median
from typing import Any

CAPABILITY_ID="complexity"; CAPABILITY_VERSION="0.1.0"; ADAPTER_ID="complexity.radon"; ADAPTER_VERSION="0.1.0"

def analyze(root: Path, timeout: int=60) -> dict[str, Any]:
    try:
        version=subprocess.run([sys.executable,"-m","radon","--version"],capture_output=True,text=True,timeout=timeout,check=True).stdout.strip()
        run=subprocess.run([sys.executable,"-m","radon","cc","-j",str(root)],capture_output=True,text=True,timeout=timeout,check=True)
        raw=run.stdout; data=json.loads(raw)
    except (subprocess.TimeoutExpired, subprocess.CalledProcessError, json.JSONDecodeError) as error:
        return {"status":"BLOCKED","limitations":[{"id":"analyzer.radon.failed","description":str(error),"cause":"analyzer unavailable or malformed output"}]}
    values=[]; findings=[]
    for name, symbols in sorted(data.items()):
        for symbol in symbols:
            value=symbol["complexity"]; values.append(value)
            if value >= 21: findings.append({"findingId":f"complexity.{Path(name).name}.{symbol['name']}","capabilityId":CAPABILITY_ID,"ruleId":"complexity.high","severity":"HIGH" if value<41 else "CRITICAL","category":"COMPLEXITY","title":"High Complexity","description":f"Cyclomatic complexity is {value}","affectedEntityId":name,"state":"OPEN","regression":"UNKNOWN","confidence":1,"suppressible":True})
    metrics=[]
    if values:
        for key,value,aggregation in (("average",sum(values)/len(values),"mean"),("median",median(values),"median"),("maximum",max(values),"maximum")):
            metrics.append({"measurementId":f"complexity.repository.{key}","capabilityId":CAPABILITY_ID,"metricKey":f"complexity.cyclomatic.{key}","value":value,"unit":"score","scope":"repository","targetEntityId":"repository","aggregation":aggregation,"sourceAdapterId":ADAPTER_ID,"sourceToolId":"radon"})
    return {"status":"VALID","adapter":{"id":ADAPTER_ID,"version":ADAPTER_VERSION},"analyzer":{"id":"radon","version":version},"rawOutputHash":"sha256:"+sha256(raw.encode()).hexdigest(),"measurements":metrics,"findings":findings,"limitations":[]}
