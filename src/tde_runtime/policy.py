"""Configuration-driven, versioned policy evaluation for qualification."""

from __future__ import annotations

from copy import deepcopy
from hashlib import sha256
import json
from pathlib import Path
from typing import Any, Iterable, Mapping


POLICY_SCHEMA_VERSION = "1.0.0"
POLICY_DECISIONS = ("PASS", "PASS_WITH_WARNINGS", "FAIL", "BLOCKED", "NOT_APPLICABLE")
SUPPORTED_POLICY_METRICS = {
    "code_size": {"code_size.code_lines"},
    "complexity": {"complexity.cyclomatic.maximum"},
}
POLICY_OPERATORS = {"greater_than", "less_than"}


class PolicyError(ValueError):
    """Raised when a policy cannot be loaded or is incompatible."""


class PolicyEngine:
    """Loads and evaluates policies without knowledge of Runtime stages or adapters."""

    def __init__(self, policy_directories: Iterable[Path] | None = None) -> None:
        bundled = Path(__file__).with_name("policies")
        self._policy_directories = tuple(policy_directories) if policy_directories is not None else (bundled,)

    def discover(self, additional_directories: Iterable[Path] = ()) -> tuple[dict[str, str], ...]:
        entries: list[dict[str, str]] = []
        for path in self._policy_files((*self._policy_directories, *additional_directories)):
            policy = self._read(path)
            self.validate(policy)
            entries.append({"id": policy["identifier"], "version": policy["version"], "path": str(path)})
        return tuple(entries)

    def load(self, configuration: Mapping[str, Any], repository_root: Path,
             runtime_version: str, schema_version: str) -> dict[str, Any]:
        settings = dict(configuration.get("executionOptions", {}).get("policy", configuration.get("policy", {})))
        explicit_file = settings.get("file")
        if explicit_file:
            path = Path(explicit_file)
            path = path if path.is_absolute() else repository_root / path
            if not path.is_file():
                raise PolicyError(f"policy configuration file does not exist: {path}")
            policy = self._with_configuration_identity(self._read(path), path)
            self.validate(policy, declarative_required=True)
            self._validate_compatibility(policy, runtime_version, schema_version)
            return self._resolve_overrides(policy, settings)
        directories = list(self._policy_directories)
        # Later directories have higher precedence: bundled < workspace < repository.
        for setting in (settings.get("workspace"), settings.get("repository")):
            if setting:
                candidate = Path(setting)
                directories.append(candidate if candidate.is_absolute() else repository_root / candidate)
        policies = [self._with_configuration_identity(self._read(path), path) for path in self._policy_files(directories)]
        for candidate in policies:
            self.validate(candidate)
        if not policies:
            raise PolicyError("no policy is available")
        policy_id = settings.get("id")
        candidates = [item for item in policies if not policy_id or item["identifier"] == policy_id]
        if not candidates:
            raise PolicyError(f"requested policy is not available: {policy_id}")
        policy = candidates[-1]
        self.validate(policy)
        self._validate_compatibility(policy, runtime_version, schema_version)
        return self._resolve_overrides(policy, settings)

    @staticmethod
    def _resolve_overrides(policy: Mapping[str, Any], settings: Mapping[str, Any]) -> dict[str, Any]:
        resolved = deepcopy(policy)
        overrides = settings.get("overrides", {})
        if not isinstance(overrides, dict):
            raise PolicyError("policy.overrides must be an object")
        for rule in resolved["rules"]:
            configured = overrides.get(rule["id"], {})
            if not isinstance(configured, dict):
                raise PolicyError(f"override for {rule['id']} must be an object")
            rule.update({key: value for key, value in configured.items()
                         if key in {"enabled", "warning", "blocking", "outcome", "threshold", "severity"}})
            if isinstance(rule.get("threshold"), dict):
                rule["threshold"].update({key: configured[key] for key in ("warning", "blocking") if key in configured})
        PolicyEngine.validate(resolved)
        identity = dict(resolved["_configuration"])
        identity["hash"] = PolicyEngine._configuration_hash(resolved)
        resolved["_configuration"] = identity
        return resolved

    def evaluate(self, policy: Mapping[str, Any], normalized: Mapping[str, Any],
                 configuration: Mapping[str, Any]) -> dict[str, Any]:
        measurements = list(normalized.get("measurements", []))
        findings = list(normalized.get("findings", []))
        results = list(normalized.get("capabilityResults", []))
        limitations = [limitation for result in results for limitation in result.get("limitations", [])]
        triggered: list[dict[str, Any]] = []
        for rule in policy["rules"]:
            if not rule.get("enabled", True):
                continue
            if rule["type"] == "threshold":
                triggered.extend(self._threshold_matches(rule, measurements))
            elif rule["type"] == "finding_severity":
                triggered.extend(self._finding_matches(rule, findings))
            elif rule["type"] == "capability":
                triggered.extend(self._capability_matches(rule, results, configuration))
            elif rule["type"] == "comparison_regression":
                triggered.extend({"ruleId": rule["id"], "outcome": self._outcome(rule.get("outcome", "FAIL")),
                                  "comparisonId": normalized.get("comparison", {}).get("comparisonId"),
                                  "findingId": item, "affectedEvidence": {"comparisonId": normalized.get("comparison", {}).get("comparisonId")}}
                                 for item in normalized.get("comparison", {}).get("regressions", []))
        if any(item.get("blocking") is True for item in limitations):
            triggered.append({"ruleId": "limitation.blocking", "outcome": "BLOCKED", "reason": "blocking limitation"})
        decision = self._decision(triggered, measurements, findings, results)
        return {
            "policy": {key: policy[key] for key in ("identifier", "version", "scope", "owner")},
            "policyConfiguration": dict(policy.get("_configuration", {
                "identifier": policy["identifier"], "version": policy["version"],
                "hash": self._configuration_hash(policy), "source": "in-memory",
            })),
            "decision": decision,
            "decisionReason": self._decision_reason(decision, triggered),
            "triggeredRules": triggered,
            "thresholds": {rule["id"]: self._threshold_definition(rule)
                           for rule in policy["rules"] if rule["type"] == "threshold"},
            "affectedCapabilities": sorted({item["capabilityId"] for item in triggered if item.get("capabilityId")} | {item["affectedCapability"] for item in triggered if item.get("affectedCapability")} ),
            "qualificationReference": {"measurementIds": sorted(str(item.get("measurementId")) for item in measurements),
                                         "findingIds": sorted(str(item.get("findingId")) for item in findings)},
            "qualificationInputs": {"measurementCount": len(measurements), "findingCount": len(findings),
                                     "capabilityResultCount": len(results), "limitationCount": len(limitations),
                                     "configuration": dict(configuration)},
        }

    @staticmethod
    def validate(policy: Mapping[str, Any], *, declarative_required: bool = False) -> None:
        required = {"identifier", "version", "scope", "owner", "description", "supportedCapabilities",
                    "supportedSchemas", "supportedRuntimeVersions", "rules"}
        missing = required - set(policy)
        if missing:
            raise PolicyError(f"policy is missing required fields: {sorted(missing)}")
        if not all(isinstance(policy[key], str) and policy[key] for key in ("identifier", "version", "scope", "owner", "description")):
            raise PolicyError("policy identity fields must be non-empty strings")
        if not all(isinstance(policy[key], list) and all(isinstance(item, str) for item in policy[key])
                   for key in ("supportedCapabilities", "supportedSchemas", "supportedRuntimeVersions")):
            raise PolicyError("policy compatibility fields must be string arrays")
        unknown_capabilities = set(policy["supportedCapabilities"]) - set(SUPPORTED_POLICY_METRICS)
        if unknown_capabilities:
            raise PolicyError(f"unknown policy capabilities: {sorted(unknown_capabilities)}")
        if not isinstance(policy["rules"], list):
            raise PolicyError("policy.rules must be an array")
        identifiers: set[str] = set()
        threshold_targets: set[tuple[str, str, str]] = set()
        for rule in policy["rules"]:
            if not isinstance(rule, dict) or not isinstance(rule.get("id"), str) or rule.get("type") not in {"threshold", "finding_severity", "capability", "comparison_regression"}:
                raise PolicyError("every policy rule needs an id and supported type")
            if rule["id"] in identifiers:
                raise PolicyError(f"policy rule identifiers must be unique: {rule['id']}")
            identifiers.add(rule["id"])
            if declarative_required and rule["type"] != "threshold":
                raise PolicyError(f"declarative policy {rule['id']} has unsupported type: {rule['type']}")
            if rule["type"] == "threshold" and (declarative_required or any(key in rule for key in ("capability", "metric", "operator", "threshold", "severity", "rationale"))):
                PolicyEngine._validate_declarative_threshold(rule, threshold_targets)

    @staticmethod
    def _validate_declarative_threshold(rule: Mapping[str, Any], targets: set[tuple[str, str, str]]) -> None:
        required = {"capability", "metric", "operator", "threshold", "severity", "enabled", "rationale"}
        missing = required - set(rule)
        if missing:
            raise PolicyError(f"declarative threshold policy {rule['id']} is missing required fields: {sorted(missing)}")
        capability, metric, operator = rule["capability"], rule["metric"], rule["operator"]
        if capability not in SUPPORTED_POLICY_METRICS:
            raise PolicyError(f"unknown policy capability: {capability}")
        if metric not in SUPPORTED_POLICY_METRICS[capability]:
            raise PolicyError(f"unknown metric for {capability}: {metric}")
        if operator not in POLICY_OPERATORS:
            raise PolicyError(f"invalid policy operator: {operator}")
        if not isinstance(rule["enabled"], bool):
            raise PolicyError(f"policy {rule['id']} enabled must be boolean")
        if not isinstance(rule["rationale"], str) or not rule["rationale"].strip():
            raise PolicyError(f"policy {rule['id']} rationale must be a non-empty string")
        if not isinstance(rule["threshold"], dict) or set(rule["threshold"]) != {"warning", "blocking"}:
            raise PolicyError(f"policy {rule['id']} threshold must contain warning and blocking values")
        if not isinstance(rule["severity"], dict) or set(rule["severity"]) != {"warning", "blocking"}:
            raise PolicyError(f"policy {rule['id']} severity must contain warning and blocking values")
        warning, blocking = rule["threshold"]["warning"], rule["threshold"]["blocking"]
        if not all(isinstance(value, (int, float)) and not isinstance(value, bool) for value in (warning, blocking)):
            raise PolicyError(f"policy {rule['id']} thresholds must be numeric")
        if (operator == "greater_than" and warning > blocking) or (operator == "less_than" and warning < blocking):
            raise PolicyError(f"policy {rule['id']} has conflicting thresholds")
        if tuple(rule["severity"].values()) != ("WARNING", "BLOCKING"):
            raise PolicyError(f"policy {rule['id']} severity must map warning and blocking")
        target = (capability, metric, operator)
        if rule["enabled"] and target in targets:
            raise PolicyError(f"conflicting enabled policies for {capability}.{metric}")
        if rule["enabled"]:
            targets.add(target)

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
    def _configuration_hash(policy: Mapping[str, Any]) -> str:
        payload = {key: value for key, value in policy.items() if key != "_configuration"}
        canonical = json.dumps(payload, sort_keys=True, separators=(",", ":"), ensure_ascii=True)
        return f"sha256:{sha256(canonical.encode()).hexdigest()}"

    @staticmethod
    def _with_configuration_identity(policy: dict[str, Any], path: Path) -> dict[str, Any]:
        resolved = deepcopy(policy)
        resolved["_configuration"] = {"identifier": policy.get("identifier"), "version": policy.get("version"),
                                       "hash": PolicyEngine._configuration_hash(policy), "source": path.name}
        return resolved

    @staticmethod
    def _threshold_definition(rule: Mapping[str, Any]) -> dict[str, Any]:
        threshold = rule.get("threshold")
        if isinstance(threshold, dict):
            return {"warning": threshold.get("warning"), "blocking": threshold.get("blocking"),
                    "direction": rule.get("operator", "greater_than")}
        return {key: rule[key] for key in ("warning", "blocking", "direction") if key in rule}

    @staticmethod
    def _validate_compatibility(policy: Mapping[str, Any], runtime_version: str, schema_version: str) -> None:
        if runtime_version not in policy["supportedRuntimeVersions"]:
            raise PolicyError("policy is incompatible with this runtime version")
        if schema_version not in policy["supportedSchemas"]:
            raise PolicyError("policy is incompatible with this schema version")

    @staticmethod
    def _outcome(value: str) -> str:
        aliases = {"WARNING": "PASS_WITH_WARNINGS", "BLOCKING": "FAIL"}
        outcome = aliases.get(value, value)
        if outcome not in POLICY_DECISIONS:
            raise PolicyError(f"unsupported policy outcome: {value}")
        return outcome

    def _threshold_matches(self, rule: Mapping[str, Any], measurements: list[Mapping[str, Any]]) -> list[dict[str, Any]]:
        matches: list[dict[str, Any]] = []
        for measurement in measurements:
            metric = rule.get("metric", rule.get("metricKey"))
            if measurement.get("metricKey") != metric or not isinstance(measurement.get("value"), (int, float)):
                continue
            value, direction = measurement["value"], rule.get("operator", rule.get("direction", "greater_than"))
            def reached(threshold: Any) -> bool:
                return threshold is not None and ((direction == "greater_than" and value >= threshold) or (direction == "less_than" and value <= threshold))
            configured = rule.get("threshold", {})
            warning = configured.get("warning", rule.get("warning")) if isinstance(configured, dict) else rule.get("warning")
            blocking = configured.get("blocking", rule.get("blocking")) if isinstance(configured, dict) else rule.get("blocking")
            threshold, outcome = (blocking, "FAIL") if reached(blocking) else (warning, "PASS_WITH_WARNINGS") if reached(warning) else (None, None)
            if outcome:
                matches.append({"ruleId": rule["id"], "outcome": outcome, "metricKey": metric, "measuredValue": value,
                                "threshold": threshold, "affectedCapability": measurement.get("capabilityId"),
                                "affectedEvidence": {"measurementId": measurement.get("measurementId"), "targetEntityId": measurement.get("targetEntityId")}})
        return matches

    def _finding_matches(self, rule: Mapping[str, Any], findings: list[Mapping[str, Any]]) -> list[dict[str, Any]]:
        outcome = self._outcome(rule.get("outcome", "PASS_WITH_WARNINGS"))
        return [{"ruleId": rule["id"], "outcome": outcome, "findingId": finding.get("findingId"), "severity": rule.get("severity"),
                 "affectedCapability": finding.get("capabilityId"), "affectedEvidence": {"findingId": finding.get("findingId")}}
                for finding in findings if finding.get("severity") == rule.get("severity")]

    def _capability_matches(self, rule: Mapping[str, Any], results: list[Mapping[str, Any]], configuration: Mapping[str, Any]) -> list[dict[str, Any]]:
        capability_id = rule.get("capabilityId")
        configured = configuration.get("executionOptions", {}).get("capabilities", {}).get(capability_id, {})
        present = any(result.get("capabilityId") == capability_id for result in results)
        required = rule.get("required", rule.get("enabled") is True)
        if not required or present:
            return []
        return [{"ruleId": rule["id"], "outcome": self._outcome(rule.get("outcome", "BLOCKED")), "capabilityId": capability_id,
                 "reason": "required capability evidence is missing", "affectedEvidence": {"capabilityId": capability_id, "configured": configured}}]

    @staticmethod
    def _decision(triggered: list[Mapping[str, Any]], measurements: list[Mapping[str, Any]], findings: list[Mapping[str, Any]], results: list[Mapping[str, Any]]) -> str:
        outcomes = {item["outcome"] for item in triggered}
        if "BLOCKED" in outcomes:
            return "BLOCKED"
        if "FAIL" in outcomes:
            return "FAIL"
        if "PASS_WITH_WARNINGS" in outcomes:
            return "PASS_WITH_WARNINGS"
        return "PASS" if measurements or findings or results else "NOT_APPLICABLE"

    @staticmethod
    def _decision_reason(decision: str, triggered: list[Mapping[str, Any]]) -> str:
        if not triggered:
            return "no policy rule was triggered" if decision == "PASS" else "no applicable capability evidence is available"
        return f"{len(triggered)} policy rule(s) triggered; highest outcome is {decision}"
