"""Generic executable discovery for Runtime analyzer adapters."""
from __future__ import annotations

import re
import shutil
import subprocess
from typing import Any


def discover(executable_name: str, minimum_version: tuple[int, int], timeout: int) -> dict[str, Any]:
    executable = shutil.which(executable_name)
    if not executable:
        return {"status": "ANALYZER_NOT_FOUND", "limitation": {"id": f"analyzer.{executable_name}.unavailable", "description": f"{executable_name} is not on PATH.", "cause": "analyzer unavailable"}}
    try:
        version = subprocess.run([executable, "--version"], capture_output=True, text=True, timeout=timeout, check=True).stdout.strip()
    except (subprocess.TimeoutExpired, subprocess.CalledProcessError) as error:
        return {"status": "FAILED_CLOSED", "limitation": {"id": f"analyzer.{executable_name}.discovery_failed", "description": str(error), "cause": "analyzer discovery failed"}}
    match = re.search(r"(\d+)\.(\d+)", version)
    if not match or tuple(map(int, match.groups())) < minimum_version:
        return {"status": "ANALYZER_NOT_FOUND", "limitation": {"id": f"analyzer.{executable_name}.unsupported_version", "description": f"{executable_name} {minimum_version[0]}.{minimum_version[1]}+ is required; found {version or 'unknown'}.", "cause": "unsupported analyzer version"}}
    return {"status": "VALID", "executable": executable, "version": version}
