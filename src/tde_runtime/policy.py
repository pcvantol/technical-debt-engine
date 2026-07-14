"""Configuration-driven, versioned policy evaluation for qualification."""

from __future__ import annotations

from copy import deepcopy
import json
from pathlib import Path
from typing import Any, Iterable, Mapping


POLICY_SCHEMA_VERSION = "1.0.0"


class PolicyError(ValueError):
    """Raised when a policy cannot be loaded or is incompatible."""


class PolicyEngine:
    """Loads and evaluates policies without knowledge of Runtime stages or adapters."""

    def __init__(self, policy_directories: Iterable[Path] | None = None) -> None:
        bundled = Path(__file__).with_name("policies")
        self._policy_directories = tuple(policy_directories or (bundled,))

    def discover(self, additional_directories: Iterable[Path] = ()) -> tuple[dict[str, str], ...]:
        entries: list[dict[str, str]] = []
        for path in self._policy_files((*self._policy_directories, *additional_directories)):
            policy = self._read(path)
            self.validate(policy)
            entries.append({"id": policy["identifier"], "version": policy["version"], "path": str(path)})
        return tuple(sorted(entries, key=lambda item: item["id"]))

    def load(self, configuration: Mapping[str, Any], repository_root: Path,
             runtime_version: str, schema_version: str) -> dict[str, Any]:
        settings = dict(configuration.get("executionOptions", {}).get("policy", configuration.get("policy", {})))
        directories = list(self._policy_directories)
        for setting in (settings.get("workspace"), settings.get("repository")):
            if setting:
                candidate = Path(setting)
                directories.append(candidate if candidate.is_absolute() else repository_root / candidate)
        policies = [self._read(path) for path in self._policy_files(directories)]
        if not policies:
            raise PolicyError("no policy is available")
        policy_id = settings.get("id")
        policy = next((item for item in policies if item["identifier"] == policy_id), policies[0])
        if policy_id and policy["identifier"] != policy_id:
            raise PolicyError(f"requested policy is not available: {policy_id}")
        self.validate(policy)
        self._validate_compatibility(policy, runtime_version, schema_version)
        resolved = deepcopy(policy)
        overrides = settings.get("overrides", {})
        if not isinstance(overrides, dict):
            raise PolicyError("policy.overrides must be an object")
        for rule in resolved.get("rules", []):
            configured = overrides.get(rule["id"], {})
            if not isinstance(configured, dict):
                raise PolicyError(f"override for {rule['id']} must be an object")
            rule.update({key: value for key, value in configured.items() if key in {"enabled", "warning", "blocking"}})
        return resolved

    def evaluate(self, policy: Mapping[str, Any], normalized: Mapping[str, Any],
                 configuration: Mapping[str, Any]) -> dict[str, Any]:
        measurements = normalized.get("measurements", [])
        findings = normalized.get("findings", [])
        limitations = [limitation for result in normalized.get("capabilityResults", [])
                       for limitation in result.get("limitations", [])]
        triggered: list[dict[str, Any]] = []
        for rule in policy.get("rules", []):
            if not rule.get("enabled", True):
                continue
            if rule.get("type") == "threshold":
                triggered.extend(self._threshold_matches(rule, measurements))
            elif rule.get("type") == "finding_severity":
                triggered.extend(self._finding_matches(rule, findings))
            elif rule.get("type") == "capability":
                triggered.extend(self._capability_matches(rule, normalized.get("capabilityResults", []), configuration))
        if any(item.get("blocking") is True for item in limitations):
            triggered.append({"ruleId": "limitation.blocking", "outcome": "BLOCKING", "reason": "blocking limitation"})
        outcomes = {item["outcome"] for item in triggered}
        decision = "BLOCKED" if "BLOCKING" in outcomes else "WARNING" if "WARNING" in outcomes else (
            "NOT_APPLICABLE" if not measurements and not findings else "PASS")
        return {
            "policy": {key: policy[key] for key in ("identifier", "version", "scope", "owner")},
            "decision": decision,
            "triggeredRules": triggered,
            "qualificationInputs": {"measurementCount": len(measurements), "findingCount": len(findings),
                                     "limitationCount": len(limitations), "configuration": dict(configuration)},
        }

    @staticmethod
    def validate(policy: Mapping[str, Any]) -> None:
        required = {"identifier", "version", "scope", "owner", "description", "supportedCapabilities",
                    "supportedSchemas", "supportedRuntimeVersions", "rules"}
        missing = required - set(policy)
        if missing:
            raise PolicyError(f"policy is missing required fields: {sorted(missing)}")
        if not isinstance(policy["rules"], list):
            raise PolicyError("policy.rules must be an array")
        for rule in policy["rules"]:
            if not isinstance(rule, dict) or "id" not in rule or rule.get("type") not in {"threshold", "finding_severity", "capability"}:
                raise PolicyError("every policy rule needs an id and supported type")

    @staticmethod
    def _policy_files(directories: Iterable[Path]) -> tuple[Path, ...]:
        return tuple(path for directory in directories if directory.is_dir() for path in sorted(directory.glob("*.json")))

    @staticmethod
    def _read(path: Path) -> dict[str, Any]:
        try:
            value = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as error:
            raise PolicyError(f"invalid policy {path}: {error}") from error
        if not isinstance(value, dict):
            raise PolicyError(f"policy {path} must be an object")
        return value

    @staticmethod
    def _validate_compatibility(policy: Mapping[str, Any], runtime_version: str, schema_version: str) -> None:
        if runtime_version not in policy["supportedRuntimeVersions"]:
            raise PolicyError("policy is incompatible with this runtime version")
        if schema_version not in policy["supportedSchemas"]:
            raise PolicyError("policy is incompatible with this schema version")

    @staticmethod
    def _threshold_matches(rule: Mapping[str, Any], measurements: list[Mapping[str, Any]]) -> list[dict[str, Any]]:
        matches: list[dict[str, Any]] = []
        for measurement in measurements:
            if measurement.get("metricKey") != rule.get("metricKey"):
                continue
            value = measurement.get("value")
            if not isinstance(value, (int, float)):
                continue
            direction = rule.get("direction", "greater_than")
            blocking = rule.get("blocking")
            warning = rule.get("warning")
            if blocking is not None and ((direction == "greater_than" and value >= blocking) or (direction == "less_than" and value <= blocking)):
                matches.append({"ruleId": rule["id"], "outcome": "BLOCKING", "metricKey": rule["metricKey"], "value": value, "threshold": blocking})
            elif warning is not None and ((direction == "greater_than" and value >= warning) or (direction == "less_than" and value <= warning)):
                matches.append({"ruleId": rule["id"], "outcome": "WARNING", "metricKey": rule["metricKey"], "value": value, "threshold": warning})
        return matches

    @staticmethod
    def _finding_matches(rule: Mapping[str, Any], findings: list[Mapping[str, Any]]) -> list[dict[str, Any]]:
        severity = rule.get("severity")
        outcome = rule.get("outcome", "WARNING")
        return [{"ruleId": rule["id"], "outcome": outcome, "findingId": finding.get("findingId"), "severity": severity}
                for finding in findings if finding.get("severity") == severity]

    @staticmethod
    def _capability_matches(rule: Mapping[str, Any], results: list[Mapping[str, Any]],
                            configuration: Mapping[str, Any]) -> list[dict[str, Any]]:
        capability_id = rule.get("capabilityId")
        configured = configuration.get("executionOptions", {}).get("capabilities", {}).get(capability_id, {})
        expected_enabled = rule.get("enabled")
        actual_enabled = configured.get("enabled", False)
        if expected_enabled is False or actual_enabled == expected_enabled:
            return []
        if any(result.get("capabilityId") == capability_id for result in results):
            return []
        return [{"ruleId": rule["id"], "outcome": rule.get("outcome", "BLOCKING"),
                 "capabilityId": capability_id, "reason": "required capability was not enabled"}]
