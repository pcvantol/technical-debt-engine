#!/usr/bin/env python3
"""Development-only deterministic validator for TDE JSON Schema fixtures.

It deliberately supports the JSON Schema keywords used by this repository and
resolves only local schema files. It is not a runtime component or adapter SDK.
"""
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCHEMAS = ROOT / "schemas"
FIXTURES = ROOT / "fixtures"

def load(path):
    with path.open(encoding="utf-8") as handle:
        return json.load(handle)

def resolve(ref, current):
    file_part, _, pointer = ref.partition("#")
    target = current if not file_part else SCHEMAS / file_part
    schema = load(target)
    if pointer:
        for part in pointer.removeprefix("/").split("/"):
            schema = schema[part.replace("~1", "/").replace("~0", "~")]
    return schema, target

def validate(value, schema, current, path="$", errors=None):
    errors = [] if errors is None else errors
    if "$ref" in schema:
        resolved, target = resolve(schema["$ref"], current)
        return validate(value, resolved, target, path, errors)
    if not _scalar_valid(value, schema, path, errors): return errors
    _validate_object(value, schema, current, path, errors)
    _validate_items(value, schema, current, path, errors)
    return errors

def _scalar_valid(value, schema, path, errors):
    if "const" in schema and value != schema["const"]: errors.append(f"{path}: expected constant {schema['const']!r}")
    if "enum" in schema and value not in schema["enum"]: errors.append(f"{path}: value is not an allowed enum")
    expected = schema.get("type")
    if expected and not any(_is_type(value, item) for item in (expected if isinstance(expected, list) else [expected])):
        errors.append(f"{path}: expected {expected}"); return False
    if isinstance(value, str) and "pattern" in schema:
        import re
        if not re.search(schema["pattern"], value): errors.append(f"{path}: pattern mismatch")
    if isinstance(value, (int, float)) and not isinstance(value, bool):
        if value < schema.get("minimum", value): errors.append(f"{path}: below minimum")
        if value > schema.get("maximum", value): errors.append(f"{path}: above maximum")
    return True

def _is_type(value, expected):
    return {"object": isinstance(value, dict), "array": isinstance(value, list), "string": isinstance(value, str),
            "number": isinstance(value, (int, float)) and not isinstance(value, bool), "integer": isinstance(value, int) and not isinstance(value, bool), "boolean": isinstance(value, bool)}.get(expected, False)

def _validate_object(value, schema, current, path, errors):
    if not isinstance(value, dict): return
    for key in schema.get("required", []):
        if key not in value: errors.append(f"{path}: missing required {key}")
    properties = schema.get("properties", {})
    for key, item in value.items():
        if key in properties: validate(item, properties[key], current, f"{path}.{key}", errors)
        elif schema.get("additionalProperties") is False: errors.append(f"{path}: unexpected property {key}")

def _validate_items(value, schema, current, path, errors):
    if isinstance(value, list) and "items" in schema:
        for index, item in enumerate(value): validate(item, schema["items"], current, f"{path}[{index}]", errors)

def main():
    schemas = sorted(SCHEMAS.glob("*.json"))
    for schema_file in schemas: load(schema_file)
    cases = {"minimal-evidence.json": "evidence.schema.json", "multi-language-evidence.json": "evidence.schema.json",
             "partial-capability.json": "evidence.schema.json", "qualification-pass.json": "qualification.schema.json",
             "qualification-fail.json": "qualification.schema.json", "baseline.json": "baseline.schema.json",
             "comparison.json": "comparison.schema.json", "suppression-config.json": "configuration.schema.json",
             "unsupported-capability.json": "evidence.schema.json", "adapter-result.json": "adapter.schema.json"}
    failures = []
    for fixture, schema_name in cases.items():
        failures.extend(f"{fixture}: {error}" for error in validate(load(FIXTURES / fixture), load(SCHEMAS / schema_name), SCHEMAS / schema_name))
    invalid_errors = validate(load(FIXTURES / "invalid-evidence.json"), load(SCHEMAS / "evidence.schema.json"), SCHEMAS / "evidence.schema.json")
    if not invalid_errors: failures.append("invalid-evidence.json: unexpectedly passed")
    if failures:
        print("\n".join(failures)); return 1
    print(f"validated {len(schemas)} schemas, {len(cases)} valid fixtures, and 1 invalid fixture")
    return 0

if __name__ == "__main__": sys.exit(main())
