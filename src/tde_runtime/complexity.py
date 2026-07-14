"""Python cyclomatic-complexity adapter backed by the installed Radon CLI."""

from __future__ import annotations

import fnmatch
import json
import re
import shutil
import subprocess
from hashlib import sha256
from pathlib import Path
from typing import Any, Mapping

CAPABILITY_ID = "complexity"
CAPABILITY_VERSION = "0.1.0"
ADAPTER_ID = "complexity.radon"
ADAPTER_VERSION = "0.1.0"
MINIMUM_ANALYZER_VERSION = (6, 0)

def _items(value: object) -> tuple[str, ...]:
    if isinstance(value, str):
        return tuple(item.strip() for item in value.split(",") if item.strip())
    if isinstance(value, (list, tuple)) and all(isinstance(item, str) for item in value):
        return tuple(value)
    return ()

def _relative(root: Path, name: str) -> str:
    try:
        return Path(name).resolve().relative_to(root.resolve()).as_posix()
    except ValueError:
        return Path(name).as_posix()

def _thresholds(configuration: Mapping[str, Any]) -> dict[str, int]:
    supplied = configuration.get("thresholds", {})
    if not isinstance(supplied, Mapping): supplied = {}
    values = {"high": 11, "veryHigh": 21, "critical": 41}
    for key in values:
        if key in supplied:
            if not isinstance(supplied[key], int) or supplied[key] < 1:
                raise ValueError(f"complexity threshold {key} must be a positive integer")
            values[key] = supplied[key]
    if not values["high"] < values["veryHigh"] < values["critical"]:
        raise ValueError("complexity thresholds must satisfy high < veryHigh < critical")
    return values

def analyze(root: Path, timeout: int = 60, configuration: Mapping[str, Any] | None = None) -> dict[str, Any]:
    """Execute Radon deterministically and retain native output for evidence."""
    configuration = configuration or {}
    executable = shutil.which("radon")
    if not executable:
        return {"status":"BLOCKED", "limitations":[{"id":"analyzer.radon.unavailable","description":"radon is not on PATH; install Radon 6.0+.","cause":"analyzer unavailable"}]}
    try:
        version = subprocess.run([executable, "--version"], capture_output=True, text=True, timeout=timeout, check=True).stdout.strip()
        match = re.search(r"(\d+)\.(\d+)", version)
        if not match or tuple(map(int, match.groups())) < MINIMUM_ANALYZER_VERSION:
            return {"status":"BLOCKED", "limitations":[{"id":"analyzer.radon.unsupported_version","description":f"Radon 6.0+ is required; found {version or 'unknown'}.","cause":"unsupported analyzer version"}]}
        completed = subprocess.run([executable, "cc", "--json", str(root)], capture_output=True, text=True, timeout=timeout, check=True)
        raw, data = completed.stdout, json.loads(completed.stdout)
    except (FileNotFoundError, subprocess.TimeoutExpired, subprocess.CalledProcessError, json.JSONDecodeError) as error:
        return {"status":"BLOCKED", "limitations":[{"id":"analyzer.radon.failed","description":str(error),"cause":"analyzer execution failed"}]}
    try:
        thresholds = _thresholds(configuration)
    except ValueError as error:
        return {"status":"BLOCKED", "limitations":[{"id":"complexity.configuration.invalid","description":str(error),"cause":"invalid configuration"}]}
    defaults = (".git/**", ".tde/**", "build/**", "dist/**", "*.egg-info/**", ".venv/**", "venv/**", "__pycache__/**")
    ignored_paths, ignored_symbols = defaults + _items(configuration.get("ignoredPaths")), set(_items(configuration.get("ignoredSymbols")))
    symbols, skipped = [], 0
    for native_path, native_symbols in sorted(data.items()):
        path = _relative(root, native_path)
        if any(fnmatch.fnmatch(path, pattern) or path.startswith(pattern.rstrip("/")+"/") for pattern in ignored_paths):
            skipped += len(native_symbols); continue
        for native in sorted(native_symbols, key=lambda item: (item.get("lineno", 0), item.get("name", ""))):
            if native.get("name") in ignored_symbols:
                skipped += 1; continue
            symbols.append({"path":path,"language":"Python","name":native["name"],"type":native.get("type","symbol"),"line":native.get("lineno"),"endLine":native.get("endline"),"complexity":native["complexity"]})
    limitations=[]
    if skipped: limitations.append({"id":"complexity.configuration.ignored","description":f"{skipped} symbol(s) were excluded by Complexity configuration.","cause":"configured exclusion"})
    if not symbols: limitations.append({"id":"complexity.python.no_symbols","description":"Radon found no supported Python symbols after exclusions.","cause":"analyzer capability limitation"})
    return {"status":"VALID","adapter":{"id":ADAPTER_ID,"version":ADAPTER_VERSION},"analyzer":{"id":"radon","version":version},"rawOutput":raw,"rawOutputHash":"sha256:"+sha256(raw.encode()).hexdigest(),"symbols":symbols,"thresholds":thresholds,"limitations":limitations}
