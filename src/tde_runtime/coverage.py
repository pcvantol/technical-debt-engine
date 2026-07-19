"""Read-only Coverage capability adapters for existing repository artifacts."""

from __future__ import annotations

from hashlib import sha256
from pathlib import Path
import re
from typing import Any, Mapping
from xml.etree import ElementTree

CAPABILITY_ID = "coverage"
CAPABILITY_VERSION = "0.1.0"
ADAPTER_ID = "coverage.artifact"
ADAPTER_VERSION = "0.1.0"
PARSER_VERSION = "1.0.0"
DEFAULT_LOCATIONS = ("coverage.xml", "coverage/coverage.xml", "reports/coverage.xml", "lcov.info", "coverage/lcov.info", "coverage.info")


class CoverageArtifactError(ValueError):
    """An artifact cannot be trusted as canonical coverage evidence."""


def _paths(root: Path, settings: Mapping[str, Any]) -> tuple[Path, ...]:
    configured: list[str] = []
    for key in ("path", "artifact", "file"):
        value = settings.get(key)
        if isinstance(value, str) and value.strip():
            configured.append(value)
    values = settings.get("paths")
    if isinstance(values, (list, tuple)) and all(isinstance(value, str) and value.strip() for value in values):
        configured.extend(values)
    candidates = configured or list(DEFAULT_LOCATIONS)
    return tuple((Path(candidate) if Path(candidate).is_absolute() else root / candidate) for candidate in candidates)


def _metric(covered: int | None, total: int | None) -> dict[str, int | float | None]:
    if covered is None or total is None:
        return {"covered": None, "total": None, "percent": None}
    if covered < 0 or total < 0 or covered > total:
        raise CoverageArtifactError("coverage totals must be non-negative and covered must not exceed total")
    return {"covered": covered, "total": total, "percent": (covered / total * 100) if total else 100.0}


def _integer(value: str | None, label: str) -> int:
    try:
        number = int(value or "")
    except ValueError as error:
        raise CoverageArtifactError(f"{label} must be an integer") from error
    if number < 0:
        raise CoverageArtifactError(f"{label} must not be negative")
    return number


def _xml_metric(root: ElementTree.Element, names: tuple[str, ...], label: str) -> int | None:
    for name in names:
        if name in root.attrib:
            return _integer(root.attrib[name], label)
    return None


def _rate(root: ElementTree.Element, name: str) -> float | None:
    if name not in root.attrib:
        return None
    try:
        value = float(root.attrib[name])
    except ValueError as error:
        raise CoverageArtifactError(f"{name} must be numeric") from error
    if not 0 <= value <= 1:
        raise CoverageArtifactError(f"{name} must be between 0 and 1")
    return value


def _parse_xml(contents: bytes) -> tuple[str, dict[str, Any]]:
    try:
        root = ElementTree.fromstring(contents)
    except ElementTree.ParseError as error:
        raise CoverageArtifactError(f"invalid XML coverage artifact: {error}") from error
    if root.tag.rsplit("}", 1)[-1] != "coverage":
        raise CoverageArtifactError("XML coverage artifact must have a coverage root element")
    # Cobertura class elements own the repository line set.  Method elements
    # may repeat those same lines, so a broad ``.//line`` query double-counts
    # reports emitted by Istanbul and gcovr.
    lines = root.findall(".//class/lines/line")
    if not lines:
        raise CoverageArtifactError("XML coverage artifact contains no line data")
    line_hits: list[int] = []
    branches: list[tuple[int, int]] = []
    for line in lines:
        number = line.attrib.get("number")
        hits = _integer(line.attrib.get("hits"), "line hits")
        if not number:
            raise CoverageArtifactError("line coverage record has no line number")
        line_hits.append(hits)
        condition = line.attrib.get("condition-coverage")
        if condition:
            match = re.search(r"\((\d+)\s*/\s*(\d+)\)", condition)
            if not match:
                raise CoverageArtifactError("invalid branch condition coverage")
            branches.append((_integer(match.group(1), "covered branches"), _integer(match.group(2), "total branches")))
    derived_lines = (sum(hits > 0 for hits in line_hits), len(line_hits))
    declared_lines = (_xml_metric(root, ("lines-covered",), "lines covered"), _xml_metric(root, ("lines-valid",), "lines valid"))
    if all(value is not None for value in declared_lines) and declared_lines != derived_lines:
        raise CoverageArtifactError("declared XML line totals disagree with line data")
    derived_branches = (sum(value[0] for value in branches), sum(value[1] for value in branches)) if branches else (None, None)
    declared_branches = (_xml_metric(root, ("branches-covered",), "branches covered"), _xml_metric(root, ("branches-valid",), "branches valid"))
    # Coverage.py emits a zero/zero branch summary when branch collection was
    # not enabled.  It is unavailable branch coverage, not 100% coverage.
    if derived_branches[0] is None and declared_branches == (0, 0):
        declared_branches = (None, None)
    if all(value is not None for value in declared_branches) and derived_branches[0] is not None and declared_branches != derived_branches:
        raise CoverageArtifactError("declared XML branch totals disagree with line data")
    line = _metric(*(declared_lines if all(value is not None for value in declared_lines) else derived_lines))
    branch = _metric(*(declared_branches if all(value is not None for value in declared_branches) else derived_branches))
    for name, metric in (("line-rate", line), ("branch-rate", branch)):
        rate = _rate(root, name)
        if rate is not None and metric["percent"] is not None and abs(rate * 100 - float(metric["percent"])) > 0.01:
            raise CoverageArtifactError(f"{name} disagrees with coverage totals")
    # coverage.py emits lines-valid and a numeric major version. Other
    # Cobertura producers, including c8 and gcovr, use the same attributes.
    version = root.attrib.get("version", "")
    parser = "coverage.py-xml" if b"generated by coverage.py" in contents.lower() or ("lines-valid" in root.attrib and re.match(r"^[1-9]\d*(?:\.\d+)*$", version)) else "cobertura-xml"
    return parser, {"line": line, "branch": branch}


def _parse_lcov(contents: bytes) -> tuple[str, dict[str, Any]]:
    try:
        rows = contents.decode("utf-8").splitlines()
    except UnicodeDecodeError as error:
        raise CoverageArtifactError("LCOV artifact is not UTF-8") from error
    lines: dict[tuple[str, str], int] = {}
    branches: dict[tuple[str, str, str, str], int] = {}
    source: str | None = None
    for raw in rows:
        row = raw.strip()
        if not row or row == "end_of_record":
            continue
        if row.startswith("SF:"):
            source = row[3:] or None
            if source is None:
                raise CoverageArtifactError("LCOV source file is empty")
        elif row.startswith("DA:"):
            if source is None:
                raise CoverageArtifactError("LCOV line record precedes source file")
            parts = row[3:].split(",")
            if len(parts) < 2:
                raise CoverageArtifactError("invalid LCOV line record")
            key = (source, parts[0]); hits = _integer(parts[1], "LCOV line hits")
            if key in lines and lines[key] != hits:
                raise CoverageArtifactError("duplicate LCOV line records disagree")
            lines[key] = hits
        elif row.startswith("BRDA:"):
            if source is None:
                raise CoverageArtifactError("LCOV branch record precedes source file")
            parts = row[5:].split(",")
            if len(parts) != 4:
                raise CoverageArtifactError("invalid LCOV branch record")
            key = (source, *parts[:3]); taken = 0 if parts[3] == "-" else _integer(parts[3], "LCOV branch hits")
            if key in branches and branches[key] != taken:
                raise CoverageArtifactError("duplicate LCOV branch records disagree")
            branches[key] = taken
    if not lines:
        raise CoverageArtifactError("LCOV artifact contains no line data")
    return "lcov", {"line": _metric(sum(value > 0 for value in lines.values()), len(lines)),
                     "branch": _metric(sum(value > 0 for value in branches.values()), len(branches)) if branches else _metric(None, None)}


def analyze(root: Path, settings: Mapping[str, Any] | None = None) -> dict[str, Any]:
    """Discover, validate, and normalize one pre-existing coverage artifact."""
    settings = settings or {}
    artifact = next((path for path in _paths(root, settings) if path.is_file()), None)
    if artifact is None:
        return {"status": "VALID", "available": False, "limitations": [{"id": "coverage.artifact.unavailable", "description": "No coverage artifact was found in configured or standard locations.", "cause": "artifact unavailable"}]}
    try:
        contents = artifact.read_bytes()
        parser, metrics = _parse_lcov(contents) if artifact.suffix.lower() in {".info", ".lcov"} or artifact.name == "lcov.info" else _parse_xml(contents)
    except (OSError, CoverageArtifactError) as error:
        return {"status": "FAILED_CLOSED", "limitations": [{"id": "coverage.artifact.invalid", "description": str(error), "cause": "invalid coverage artifact", "blocking": True}]}
    return {"status": "VALID", "available": True, "parser": parser, "parserVersion": PARSER_VERSION,
            "sourceFormat": "lcov" if parser == "lcov" else "xml", "artifact": artifact.relative_to(root).as_posix() if artifact.is_relative_to(root) else artifact.name,
            "rawOutput": contents.decode("utf-8", errors="replace"), "rawOutputHash": "sha256:" + sha256(contents).hexdigest(),
            "metrics": metrics, "limitations": []}
