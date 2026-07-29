"""Canonical repository-source classification shared by analyzers.

The rules are intentionally path and filename based: they are portable,
deterministic and do not depend on consumer repository names.  They separate
real product source from material that must remain inspectable elsewhere (for
example a configured coverage artifact) without contributing to product
metrics.
"""

from __future__ import annotations

from pathlib import Path


EXCLUDED_DIRECTORIES = frozenset({
    ".git", ".tde", ".venv", "venv", "env", ".tox", ".nox", "__pycache__",
    "node_modules", "vendor", "vendors", "third_party", "third-party",
    "packages", "build", "dist", "bin", "obj", ".build", ".swiftpm", ".pio",
    ".xcode-derived", ".deriveddata", "deriveddata", "coverage", "coverage-html",
    "htmlcov", "artifacts", "reports", "report", "test-results", "test-results",
    "cache", ".cache", ".release", ".release-venv", ".public-release", "generated",
})

LANGUAGE_BY_EXTENSION = {
    ".py": "Python",
    ".js": "JavaScript", ".mjs": "JavaScript", ".cjs": "JavaScript", ".jsx": "JavaScript",
    ".ts": "TypeScript", ".tsx": "TypeScript",
    ".swift": "Swift",
    ".c": "C", ".h": "C", ".cc": "C++", ".cpp": "C++", ".cxx": "C++",
    ".hpp": "C++", ".hh": "C++", ".hxx": "C++",
    ".cs": "C#",
}


def normalise(path: str | Path) -> str:
    return str(path).replace("\\", "/").strip("/")


def _parts(path: str | Path) -> tuple[str, ...]:
    return tuple(part.lower() for part in normalise(path).split("/") if part)


def excluded_directory(path: str | Path) -> bool:
    return any(part in EXCLUDED_DIRECTORIES or part.startswith(".xcode-derived") for part in _parts(path)[:-1])


def classification(path: str | Path) -> str:
    """Return the canonical source class for a repository-relative path."""
    value = normalise(path).lower()
    parts = _parts(value)
    filename = parts[-1] if parts else value
    stem = filename.rsplit(".", 1)[0]
    if excluded_directory(value):
        if any(part in {"vendor", "vendors", "third_party", "third-party", "node_modules", "packages"} for part in parts):
            return "DEPENDENCY"
        if any(part in {"coverage", "coverage-html", "htmlcov", "artifacts", "reports", "report"} for part in parts):
            return "COVERAGE_ARTIFACT"
        return "GENERATED"
    if filename in {"coverage.xml", "coverage.json", "lcov.info", "cobertura.xml"} or stem.startswith(("coverage-", "coverage_")):
        return "COVERAGE_ARTIFACT"
    if any(part in {"fixture", "fixtures", "__fixtures__", "testdata", "test-data", "mock", "mocks", "__mocks__"} for part in parts):
        return "FIXTURE"
    if any(part in {"verification", "verify", "verification-output", "verification_output"} for part in parts) or stem.startswith(("validate_", "verify_", "check_")):
        return "VERIFICATION"
    if any(part in {"test", "tests", "spec", "specs", "__tests__"} for part in parts) or stem.startswith(("test_", "spec_")) or stem.endswith(("_test", "_spec", ".test", ".spec")):
        return "TEST"
    if any(part in {"sample", "samples", "example", "examples", "demo", "demos"} for part in parts):
        return "SAMPLE"
    return "PRODUCT_SOURCE"


def language_for(path: str | Path) -> str | None:
    return LANGUAGE_BY_EXTENSION.get(Path(normalise(path)).suffix.lower())


def is_analyzable_product(path: str | Path) -> bool:
    return classification(path) == "PRODUCT_SOURCE" and language_for(path) is not None


def primary_languages(root: Path) -> tuple[str, ...]:
    """Discover dominant product languages by nonblank source lines.

    Counting only recognised product files makes the decision independent of
    documentation, generated output and auxiliary tooling.  Ties deliberately
    retain every primary language instead of choosing arbitrarily.
    """
    counts: dict[str, int] = {}
    for path in sorted(root.rglob("*")):
        if not path.is_file():
            continue
        relative = path.relative_to(root)
        language = language_for(relative)
        if language is None or classification(relative) != "PRODUCT_SOURCE":
            continue
        try:
            lines = sum(1 for line in path.read_text(encoding="utf-8", errors="replace").splitlines() if line.strip())
        except OSError:
            continue
        counts[language] = counts.get(language, 0) + lines
    if not counts:
        return ()
    maximum = max(counts.values())
    return tuple(sorted(language for language, count in counts.items() if count == maximum))
