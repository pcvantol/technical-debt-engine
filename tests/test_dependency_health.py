from __future__ import annotations

from io import StringIO
import json
import os
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

from tde_cli.main import ExitCode, main


class DependencyHealthBlackBoxTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary = tempfile.TemporaryDirectory()
        self.root = Path(self.temporary.name)
        self.bin = self.root / "bin"
        self.bin.mkdir()

    def tearDown(self) -> None:
        self.temporary.cleanup()

    def npm(self, outdated: dict[str, object]) -> None:
        script = self.bin / "npm"
        script.write_text("#!/bin/sh\nif [ \"$1\" = \"--version\" ]; then echo 10.9.0; exit 0; fi\nprintf '%s\\n' '" + json.dumps(outdated) + "'\nexit 1\n", encoding="utf-8")
        script.chmod(0o755)

    def project(self, *, missing: bool = False) -> None:
        (self.root / "package.json").write_text(json.dumps({"name": "fixture", "dependencies": {"known": "1.0.0", "missing": "1.0.0"}, "devDependencies": {"dev": "1.0.0"}}), encoding="utf-8")
        packages: dict[str, object] = {"": {"name": "fixture"}, "node_modules/known": {"version": "1.0.0"}, "node_modules/dev": {"version": "1.0.0"}, "node_modules/transitive": {"version": "1.0.0"}}
        if not missing:
            packages["node_modules/missing"] = {"version": "1.0.0"}
        (self.root / "package-lock.json").write_text(json.dumps({"lockfileVersion": 3, "packages": packages}), encoding="utf-8")

    def invoke(self, *arguments: str) -> tuple[int, dict[str, object]]:
        stream = StringIO()
        with patch.dict(os.environ, {"PATH": str(self.bin) + os.pathsep + os.environ.get("PATH", "")}):
            code = main(("--format", "json", *arguments), stream)
        return code, json.loads(stream.getvalue())

    def assess(self, *extra: str) -> tuple[int, dict[str, object]]:
        return self.invoke("assess", "--capability", "dependency_health", *extra, str(self.root))

    def test_supported_npm_project_produces_canonical_evidence(self) -> None:
        self.project(); self.npm({"known": {"current": "1.0.0", "wanted": "2.0.0", "latest": "2.0.0"}})
        code, result = self.assess()
        self.assertEqual(ExitCode.SUCCESS, code)
        evidence = result["evidence"]
        adapter = evidence["adapterResults"][0]
        self.assertEqual("npm", adapter["evidence"]["ecosystem"])
        self.assertEqual("10.9.0", adapter["analyzer"]["version"])
        values = {item["metricKey"]: item["value"] for item in evidence["measurements"]}
        self.assertEqual(4, values["dependency_health.dependency_count"])
        self.assertEqual(3, values["dependency_health.direct_dependencies"])
        self.assertEqual(1, values["dependency_health.transitive_dependencies"])
        self.assertEqual(1, values["dependency_health.outdated_dependencies"])

    def test_unsupported_repository_remains_valid_with_unavailable_evidence(self) -> None:
        self.npm({})
        code, result = self.assess()
        self.assertEqual(ExitCode.SUCCESS, code)
        measurement = result["evidence"]["measurements"][-1]
        self.assertEqual("UNAVAILABLE", measurement["availability"])
        self.assertFalse(result["evidence"]["capabilityResults"][0]["qualificationApplicable"])

    def test_unknown_dependency_and_policy_are_evaluated(self) -> None:
        self.project(missing=True); self.npm({})
        policy = {"identifier": "dependency-policy", "version": "1.0.0", "scope": "repository", "owner": "tests", "description": "dependency threshold", "supportedCapabilities": ["dependency_health"], "supportedSchemas": ["1.0.0"], "supportedRuntimeVersions": ["0.2.0"], "rules": [{"id": "unknown", "type": "threshold", "capability": "dependency_health", "metric": "dependency_health.unknown_dependencies", "operator": "greater_than", "threshold": {"warning": 1, "blocking": 1}, "severity": {"warning": "WARNING", "blocking": "BLOCKING"}, "enabled": True, "rationale": "unknown dependencies"}]}
        path = self.root / "policy.json"; path.write_text(json.dumps(policy), encoding="utf-8")
        code, result = self.invoke("--policy", str(path), "assess", "--capability", "dependency_health", str(self.root))
        self.assertEqual(ExitCode.FAILED, code)
        self.assertEqual("FAIL", result["evidence"]["assessmentDecision"]["decision"])

    def test_differential_includes_dependency_health(self) -> None:
        self.project(); self.npm({})
        code, _ = self.invoke("baseline", "--name", "dependencies", "--capability", "dependency_health", str(self.root))
        self.assertEqual(ExitCode.SUCCESS, code)
        self.npm({"known": {"current": "1.0.0", "wanted": "2.0.0", "latest": "2.0.0"}})
        code, result = self.assess("--baseline", "dependencies")
        self.assertEqual(ExitCode.SUCCESS, code)
        self.assertEqual("dependency_health", result["differentialEvidence"]["capabilityDeltas"][0]["capabilityId"])
