"""Code Size capability adapter backed by an explicitly installed cloc executable."""
from __future__ import annotations
import json, re, shutil, subprocess
from collections import defaultdict
from hashlib import sha256
from pathlib import Path
from typing import Any

CAPABILITY_ID = "code_size"
CAPABILITY_VERSION = "0.1.0"
ADAPTER_ID = "code_size.cloc"
ADAPTER_VERSION = "0.1.0"
MINIMUM_ANALYZER_VERSION = (2, 10)

def classify(path: str) -> str:
    value = path.replace("\\", "/").lower()
    if value.startswith(("vendor/", "third_party/", "node_modules/")) or any(part in value for part in ("/vendor/", "/third_party/", "/node_modules/")): return "VENDOR"
    if value.startswith(("generated/", "build/", "dist/")) or any(part in value for part in ("/generated/", "/build/", "/dist/")): return "GENERATED"
    if value.startswith(("tests/", "test/", "spec/")) or "/tests/" in value: return "TEST"
    if value.startswith(("docs/", "documentation/")) or value.endswith((".md", ".rst", ".txt")): return "DOCUMENTATION"
    if value.endswith((".yml", ".yaml", ".json", ".toml", ".ini")): return "CONFIGURATION"
    return "SOURCE"

def analyze(root: Path, timeout: int = 60) -> dict[str, Any]:
    executable = shutil.which("cloc")
    if not executable:
        return {"status":"BLOCKED", "limitations":[{"id":"analyzer.cloc.unavailable","description":"cloc is not on PATH; install cloc 2.10+.","cause":"analyzer unavailable"}]}
    try:
        version = subprocess.run([executable, "--version"], capture_output=True, text=True, timeout=timeout, check=True).stdout.strip()
        match = re.search(r"(\d+)\.(\d+)", version)
        if not match or tuple(map(int, match.groups())) < MINIMUM_ANALYZER_VERSION:
            return {"status":"BLOCKED", "limitations":[{"id":"analyzer.cloc.unsupported_version","description":f"cloc {MINIMUM_ANALYZER_VERSION[0]}.{MINIMUM_ANALYZER_VERSION[1]}+ is required; found {version or 'unknown'}.","cause":"unsupported analyzer version"}]}
        result = subprocess.run([executable, "--json", "--by-file", "--quiet", str(root)], capture_output=True, text=True, timeout=timeout, check=True)
        raw = result.stdout
        data = json.loads(raw)
    except (subprocess.TimeoutExpired, subprocess.CalledProcessError, json.JSONDecodeError) as error:
        return {"status":"BLOCKED", "limitations":[{"id":"analyzer.cloc.failed","description":str(error),"cause":"analyzer execution failed"}]}
    files, languages = [], defaultdict(lambda: {"files":0,"code":0,"comment":0,"blank":0})
    totals = defaultdict(int)
    entries = ((name, item) for name, item in data.items() if name not in {"header", "SUM"})
    for name, item in sorted(entries):
        relative = Path(name).resolve().relative_to(root.resolve()).as_posix()
        category, language = classify(relative), item.get("language", "Unknown")
        record = {"path":relative,"classification":category,"language":language,"physical":item["blank"]+item["comment"]+item["code"],"code":item["code"],"comment":item["comment"],"blank":item["blank"]}
        files.append(record); bucket = languages[language]; bucket["files"] += 1; bucket["code"] += item["code"]; bucket["comment"] += item["comment"]; bucket["blank"] += item["blank"]
        for key in ("code","comment","blank"): totals[key] += item[key]
        totals["files"] += 1; totals[category.lower()] += item["code"]
    source = totals["source"]; ratio = totals["test"] / source if source else 0
    return {"status":"VALID","adapter":{"id":ADAPTER_ID,"version":ADAPTER_VERSION},"analyzer":{"id":"cloc","version":version},"rawOutput":raw,"rawOutputHash":"sha256:"+sha256(raw.encode()).hexdigest(),"files":files,"languages":dict(sorted(languages.items())),"totals":dict(totals),"testToSourceRatio":ratio,"limitations":[{"id":"code_size.logical_lines.unavailable","description":"cloc does not provide logical line counts.","cause":"analyzer limitation"}]}
