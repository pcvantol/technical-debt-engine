"""Generic executable discovery for Runtime analyzer adapters."""
from __future__ import annotations

import re
import shutil
import subprocess
import sys
from pathlib import Path
from typing import Any


def discover(executable_name: str, minimum_version: tuple[int, int], timeout: int) -> dict[str, Any]:
    executable = shutil.which(executable_name)
    # A public wheel installs analyzer console scripts into the active Python
    # environment. Invoking `tde` by absolute path does not necessarily prepend
    # that environment's bin/Scripts directory to PATH, so discover the sibling
    # script deterministically before declaring a bundled dependency missing.
    if not executable:
        # `sys.executable` can be a symlink to a base interpreter in a virtual
        # environment; `sys.prefix` remains the active environment identity.
        directories = (Path(sys.prefix) / ("Scripts" if sys.platform == "win32" else "bin"), Path(sys.executable).parent)
        candidates = tuple(candidate for directory in directories for candidate in (directory / executable_name, directory / f"{executable_name}.exe"))
        executable = next((str(candidate) for candidate in candidates if candidate.is_file()), None)
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
