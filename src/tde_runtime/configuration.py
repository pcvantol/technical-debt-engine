"""Canonical Runtime configuration loading and repository discovery."""

from __future__ import annotations

from dataclasses import dataclass
from hashlib import sha256
import json
from pathlib import Path
from typing import Any, Mapping


def _scalar(value: str) -> Any:
    value = value.strip()
    if value in {"true", "True"}:
        return True
    if value in {"false", "False"}:
        return False
    if value in {"null", "Null", "~"}:
        return None
    if value.startswith(("\"", "'")) and value.endswith(("\"", "'")):
        return value[1:-1]
    try:
        return int(value)
    except ValueError:
        return value


def _parse_yaml(contents: str) -> dict[str, Any]:
    """Parse the small mapping-only .tde.yml contract without a runtime dependency."""
    root: dict[str, Any] = {}
    stack: list[tuple[int, dict[str, Any]]] = [(-1, root)]
    for raw in contents.splitlines():
        if not raw.strip() or raw.lstrip().startswith("#"):
            continue
        indent = len(raw) - len(raw.lstrip(" "))
        key, separator, value = raw.strip().partition(":")
        if not separator or not key:
            raise ValueError(".tde.yml supports mappings only")
        while stack[-1][0] >= indent:
            stack.pop()
        parent = stack[-1][1]
        if value.strip():
            parent[key] = _scalar(value)
        else:
            nested: dict[str, Any] = {}
            parent[key] = nested
            stack.append((indent, nested))
    return root


@dataclass(frozen=True)
class RuntimeConfiguration:
    schema_version: str = "1.0.0"
    execution_options: dict[str, Any] | None = None

    @classmethod
    def load(cls, values: Mapping[str, Any] | None = None) -> "RuntimeConfiguration":
        values = {} if values is None else dict(values)
        allowed = {"schemaVersion", "executionOptions", "capabilities", "policy", "baseline", "trend"}
        unknown = set(values) - allowed
        if unknown:
            raise ValueError(f"unsupported runtime configuration: {sorted(unknown)}")
        schema_version = values.get("schemaVersion", "1.0.0")
        if schema_version != "1.0.0":
            raise ValueError("unsupported configuration schema version")
        options = values.get("executionOptions", {})
        if not isinstance(options, dict):
            raise ValueError("executionOptions must be an object")
        resolved: dict[str, Any] = dict(options)
        for key in ("capabilities", "policy", "baseline", "trend"):
            value = values.get(key, resolved.get(key, {}))
            if not isinstance(value, dict):
                raise ValueError(f"{key} must be an object")
            resolved[key] = value
        return cls(schema_version=schema_version, execution_options=resolved)

    @classmethod
    def discover(cls, repository_root: str | Path, explicit_path: str | Path | None = None) -> "RuntimeConfiguration":
        path = Path(explicit_path) if explicit_path else Path(repository_root) / ".tde.yml"
        if not path.is_file():
            if explicit_path:
                raise ValueError(f"configuration file does not exist: {path}")
            return cls.load()
        try:
            contents = path.read_text(encoding="utf-8")
            try:
                values = json.loads(contents)
            except json.JSONDecodeError:
                values = _parse_yaml(contents)
        except (OSError, ValueError) as error:
            raise ValueError(f"invalid configuration {path}: {error}") from error
        if not isinstance(values, dict):
            raise ValueError("configuration root must be an object")
        return cls.load(values)

    def with_capability(self, identifier: str, enabled: bool = True) -> "RuntimeConfiguration":
        values = self.as_dict()
        capabilities = dict(values["executionOptions"].get("capabilities", {}))
        existing = capabilities.get(identifier, {})
        if not isinstance(existing, dict):
            raise ValueError(f"capability configuration for {identifier} must be an object")
        capabilities[identifier] = {**existing, "enabled": enabled}
        values["capabilities"] = capabilities
        values["executionOptions"].pop("capabilities", None)
        return self.load(values)

    def as_dict(self) -> dict[str, Any]:
        return {"schemaVersion": self.schema_version, "executionOptions": self.execution_options or {}}

    def digest(self) -> str:
        canonical = json.dumps(self.as_dict(), sort_keys=True, separators=(",", ":"))
        return f"sha256:{sha256(canonical.encode()).hexdigest()}"
