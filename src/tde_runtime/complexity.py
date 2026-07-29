"""Canonical, multi-language cyclomatic-complexity adapter orchestration."""

from __future__ import annotations

import csv
import fnmatch
import io
import json
import platform
import subprocess
import tempfile
from hashlib import sha256
from pathlib import Path
from typing import Any, Mapping

from .analyzer_discovery import discover
from .source_classification import classification, language_for, primary_languages

CAPABILITY_ID = "complexity"
CAPABILITY_VERSION = "1.1.0"
RADON_ADAPTER_ID = "complexity.radon"
LIZARD_ADAPTER_ID = "complexity.lizard"
ADAPTER_ID = RADON_ADAPTER_ID  # Compatibility import for existing Python consumers.
ADAPTER_VERSION = "1.1.0"
MINIMUM_RADON_VERSION = (6, 0)
MINIMUM_LIZARD_VERSION = (1, 23)
LIZARD_LANGUAGES = {"JavaScript": "javascript", "TypeScript": "typescript", "Swift": "swift", "C": "cpp", "C++": "cpp", "C#": "csharp"}


def _items(value: object) -> tuple[str, ...]:
    if isinstance(value, str):
        return tuple(item.strip() for item in value.split(",") if item.strip())
    if isinstance(value, (list, tuple)) and all(isinstance(item, str) for item in value):
        return tuple(value)
    return ()


def _relative(root: Path, name: str) -> str:
    path = Path(name)
    if not path.is_absolute():
        return path.as_posix()
    try:
        return path.resolve().relative_to(root.resolve()).as_posix()
    except ValueError:
        return path.name


def classify_path(path: str) -> str:
    """Compatibility entrypoint for shared canonical classification."""
    return classification(path)


def _thresholds(configuration: Mapping[str, Any]) -> dict[str, int]:
    supplied = configuration.get("thresholds", {})
    if not isinstance(supplied, Mapping):
        supplied = {}
    values = {"high": 11, "veryHigh": 21, "critical": 41}
    for key in values:
        if key in supplied:
            if not isinstance(supplied[key], int) or supplied[key] < 1:
                raise ValueError(f"complexity threshold {key} must be a positive integer")
            values[key] = supplied[key]
    if not values["high"] < values["veryHigh"] < values["critical"]:
        raise ValueError("complexity thresholds must satisfy high < veryHigh < critical")
    return values


def _included_paths(root: Path, languages: tuple[str, ...], configuration: Mapping[str, Any]) -> list[Path]:
    ignored = _items(configuration.get("ignoredPaths"))
    selected: list[Path] = []
    for path in sorted(root.rglob("*")):
        if not path.is_file():
            continue
        relative = path.relative_to(root).as_posix()
        language = language_for(relative)
        if language not in languages:
            continue
        if classification(relative) in {"DEPENDENCY", "GENERATED", "COVERAGE_ARTIFACT", "VERIFICATION", "SAMPLE"}:
            continue
        if any(fnmatch.fnmatch(relative, pattern) or relative.startswith(pattern.rstrip("/") + "/") for pattern in ignored):
            continue
        selected.append(path)
    return selected


def _portable_native_output(root: Path, data: Mapping[str, Any]) -> tuple[str, dict[str, Any]]:
    normalized = {_relative(root, path): symbols for path, symbols in data.items()}
    ordered = {path: normalized[path] for path in sorted(normalized)}
    return json.dumps(ordered, sort_keys=True, separators=(",", ":")), ordered


def _adapter(adapter_id: str, analyzer_id: str, discovery: Mapping[str, Any], language: str, raw: str) -> dict[str, Any]:
    return {
        "id": adapter_id, "version": ADAPTER_VERSION,
        "analyzer": {"id": analyzer_id, "version": discovery["version"], "executable": discovery["executable"],
                     "package": f"{analyzer_id}=={discovery['version']}", "platform": platform.system().lower()},
        "language": language, "rawOutput": raw, "rawOutputHash": "sha256:" + sha256(raw.encode()).hexdigest(),
    }


def _radon(root: Path, paths: list[Path], timeout: int) -> dict[str, Any]:
    discovery = discover("radon", MINIMUM_RADON_VERSION, timeout)
    if discovery["status"] != "VALID":
        return {"status": discovery["status"], "limitations": [discovery["limitation"]]}
    try:
        completed = subprocess.run([discovery["executable"], "cc", "--json", *map(str, paths)], capture_output=True, text=True, timeout=timeout, check=True)
        raw, data = _portable_native_output(root, json.loads(completed.stdout))
    except (FileNotFoundError, subprocess.TimeoutExpired, subprocess.CalledProcessError, json.JSONDecodeError) as error:
        return {"status": "EXECUTION_FAILED", "limitations": [{"id": "analyzer.radon.failed", "description": str(error), "cause": "analyzer execution failed"}]}
    symbols = []
    for native_path, native_symbols in sorted(data.items()):
        path = _relative(root, native_path)
        for native in sorted(native_symbols, key=lambda item: (item.get("lineno", 0), item.get("name", ""))):
            if not native.get("name") or not isinstance(native.get("complexity"), int) or not native.get("lineno"):
                return {"status": "INVALID_EVIDENCE", "limitations": [{"id": "complexity.radon.malformed_output", "description": "Radon omitted required symbol fields.", "cause": "invalid analyzer evidence"}]}
            symbols.append({"path": path, "classification": classification(path), "language": "Python", "name": native["name"],
                            "type": native.get("type", "symbol"), "line": native["lineno"], "endLine": native.get("endline"),
                            "complexity": native["complexity"], "adapterId": RADON_ADAPTER_ID, "toolId": "radon"})
    return {"status": "VALID", "symbols": symbols, "adapter": _adapter(RADON_ADAPTER_ID, "radon", discovery, "Python", raw)}


def _lizard(root: Path, paths: list[Path], languages: tuple[str, ...], timeout: int) -> dict[str, Any]:
    discovery = discover("lizard", MINIMUM_LIZARD_VERSION, timeout)
    if discovery["status"] != "VALID":
        return {"status": discovery["status"], "limitations": [discovery["limitation"]]}
    input_file: str | None = None
    try:
        handle = tempfile.NamedTemporaryFile(mode="w", encoding="utf-8", suffix=".txt", delete=False)
        with handle:
            handle.write("\n".join(str(path) for path in paths))
            handle.write("\n")
        input_file = handle.name
        command = [discovery["executable"], "--csv", "-V", "-i", "-1", "-f", input_file]
        for language in sorted({LIZARD_LANGUAGES[language] for language in languages}):
            command.extend(["-l", language])
        completed = subprocess.run(command, capture_output=True, text=True, timeout=timeout, check=True)
        raw = completed.stdout
        rows = list(csv.reader(io.StringIO(raw)))
    except (FileNotFoundError, subprocess.TimeoutExpired, subprocess.CalledProcessError, csv.Error, OSError) as error:
        return {"status": "EXECUTION_FAILED", "limitations": [{"id": "analyzer.lizard.failed", "description": str(error), "cause": "analyzer execution failed"}]}
    finally:
        if input_file:
            Path(input_file).unlink(missing_ok=True)
    symbols = []
    for row in rows:
        if not row:
            continue
        if row[0] == "NLOC":
            continue
        if len(row) != 11:
            return {"status": "INVALID_EVIDENCE", "limitations": [{"id": "complexity.lizard.malformed_output", "description": "Lizard CSV did not contain eleven symbol fields.", "cause": "invalid analyzer evidence"}]}
        try:
            complexity, name, path, line, end_line = int(row[1]), row[7], _relative(root, row[6]), int(row[9]), int(row[10])
        except (ValueError, IndexError):
            return {"status": "INVALID_EVIDENCE", "limitations": [{"id": "complexity.lizard.malformed_output", "description": "Lizard CSV contained invalid symbol data.", "cause": "invalid analyzer evidence"}]}
        language = language_for(path)
        if not name or not path or language not in languages or line < 1:
            return {"status": "INVALID_EVIDENCE", "limitations": [{"id": "complexity.lizard.location_missing", "description": "Lizard omitted a required source location or language.", "cause": "invalid analyzer evidence"}]}
        symbols.append({"path": path, "classification": classification(path), "language": language, "name": name,
                        "type": "function", "line": line, "endLine": end_line or None, "complexity": complexity,
                        "adapterId": LIZARD_ADAPTER_ID, "toolId": "lizard"})
    return {"status": "VALID", "symbols": symbols, "adapter": _adapter(LIZARD_ADAPTER_ID, "lizard", discovery, ", ".join(languages), raw)}


def analyze(root: Path, timeout: int = 60, configuration: Mapping[str, Any] | None = None) -> dict[str, Any]:
    """Run every registered adapter applicable to discovered primary languages."""
    configuration = configuration or {}
    try:
        thresholds = _thresholds(configuration)
    except ValueError as error:
        return {"status": "BLOCKED", "limitations": [{"id": "complexity.configuration.invalid", "description": str(error), "cause": "invalid configuration"}]}
    primary = primary_languages(root)
    if not primary:
        return {"status": "NO_APPLICABLE_PRODUCT_SOURCE", "symbols": [], "adapters": [], "thresholds": thresholds,
                "primaryLanguages": [], "limitations": [{"id": "complexity.product_source.none", "description": "No supported product source files were discovered.", "cause": "no applicable product source"}]}
    symbols: list[dict[str, Any]] = []
    adapters: list[dict[str, Any]] = []
    limitations: list[dict[str, Any]] = []
    for language_group, runner in ((("Python",), _radon), (tuple(language for language in primary if language in LIZARD_LANGUAGES), _lizard)):
        languages = tuple(language for language in language_group if language in primary)
        if not languages:
            continue
        paths = _included_paths(root, languages, configuration)
        product_paths = [path for path in paths if classification(path.relative_to(root)) == "PRODUCT_SOURCE"]
        if not product_paths:
            return {"status": "NO_APPLICABLE_PRODUCT_SOURCE", "symbols": symbols, "adapters": adapters, "thresholds": thresholds,
                    "primaryLanguages": list(primary), "limitations": [{"id": "complexity.product_source.none", "description": f"No analysable product files were discovered for {', '.join(languages)}.", "cause": "no applicable product source"}]}
        result = runner(root, paths, timeout) if runner is _radon else runner(root, paths, languages, timeout)
        if result["status"] != "VALID":
            return {"status": result["status"], "symbols": symbols, "adapters": adapters, "thresholds": thresholds,
                    "primaryLanguages": list(primary), "limitations": result["limitations"]}
        if not result["symbols"]:
            return {"status": "INVALID_EVIDENCE", "symbols": symbols, "adapters": adapters, "thresholds": thresholds,
                    "primaryLanguages": list(primary), "limitations": [{"id": "complexity.analyzer.empty_output", "description": f"{result['adapter']['analyzer']['id']} emitted no symbols for applicable product source.", "cause": "invalid analyzer evidence"}]}
        symbols.extend(result["symbols"])
        adapters.append(result["adapter"])
    ignored_symbols = set(_items(configuration.get("ignoredSymbols")))
    symbols = [symbol for symbol in symbols if symbol["name"] not in ignored_symbols]
    identities = [(symbol["path"], symbol["name"], symbol["line"], symbol["adapterId"]) for symbol in symbols]
    if len(identities) != len(set(identities)):
        return {"status": "INVALID_EVIDENCE", "symbols": symbols, "adapters": adapters, "thresholds": thresholds,
                "primaryLanguages": list(primary), "limitations": [{"id": "complexity.symbol.duplicate", "description": "Analyzer results contain duplicate symbol identities.", "cause": "conflicting analyzer evidence"}]}
    symbols.sort(key=lambda item: (item["language"], item["path"], item["line"], item["name"]))
    return {"status": "VALID", "symbols": symbols, "adapters": adapters, "thresholds": thresholds,
            "primaryLanguages": list(primary), "limitations": limitations}
