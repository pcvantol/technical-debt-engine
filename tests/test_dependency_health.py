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

    def tool(self, name: str, body: str) -> None:
        script = self.bin / name
        script.write_text("#!/bin/sh\n" + body, encoding="utf-8")
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
        self.assertEqual("npm", adapter["evidence"]["ecosystems"][0]["ecosystem"])
        self.assertEqual("10.9.0", adapter["evidence"]["ecosystems"][0]["analyzer"]["version"])
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
        policy = {"identifier": "dependency-policy", "version": "1.0.0", "scope": "repository", "owner": "tests", "description": "dependency threshold", "supportedCapabilities": ["dependency_health"], "supportedSchemas": ["1.0.0"], "supportedRuntimeVersions": ["1.0.0rc3"], "rules": [{"id": "unknown", "type": "threshold", "capability": "dependency_health", "metric": "dependency_health.unknown_dependencies", "operator": "greater_than", "threshold": {"warning": 1, "blocking": 1}, "severity": {"warning": "WARNING", "blocking": "BLOCKING"}, "enabled": True, "rationale": "unknown dependencies"}]}
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

    def test_python_requirements_use_pip_for_pinned_outdated_evidence(self) -> None:
        (self.root / "requirements.txt").write_text("requests==2.0.0\n", encoding="utf-8")
        self.tool("pip", 'if [ "$1" = "--version" ]; then echo "pip 25"; else echo "Available versions: 3.0.0, 2.0.0"; fi\n')
        code, result = self.assess()
        self.assertEqual(ExitCode.SUCCESS, code)
        ecosystem = result["evidence"]["adapterResults"][0]["evidence"]["ecosystems"][0]
        self.assertEqual("PyPI", ecosystem["ecosystem"])
        self.assertEqual(["requests"], ecosystem["outdatedDependencies"])

    def test_nuget_uses_dotnet_outdated_evidence(self) -> None:
        (self.root / "app.csproj").write_text('<Project><ItemGroup><PackageReference Include="Example" Version="1.0.0" /></ItemGroup></Project>', encoding="utf-8")
        payload = {"projects": [{"frameworks": [{"topLevelPackages": [{"id": "Example", "latestVersion": "2.0.0"}], "transitivePackages": [{"id": "Transit", "latestVersion": "2.0.0"}]}]}]}
        self.tool("dotnet", 'if [ "$1" = "--version" ]; then echo "10.0"; else printf "%s\\n" \'' + json.dumps(payload) + '\'; fi\n')
        code, result = self.assess()
        self.assertEqual(ExitCode.SUCCESS, code)
        ecosystem = result["evidence"]["adapterResults"][0]["evidence"]["ecosystems"][0]
        self.assertEqual("NuGet", ecosystem["ecosystem"])
        self.assertEqual(["Example", "Transit"], ecosystem["outdatedDependencies"])

    def test_nuget_restore_failure_fails_closed(self) -> None:
        (self.root / "app.csproj").write_text('<Project><ItemGroup><PackageReference Include="Example" Version="1.0.0" /></ItemGroup></Project>', encoding="utf-8")
        payload = {"version": 1, "problems": [{"text": "Restore failed", "level": "error"}]}
        self.tool("dotnet", 'if [ "$1" = "--version" ]; then echo "10.0"; else printf "%s\\n" \'' + json.dumps(payload) + '\'; exit 1; fi\n')
        code, result = self.assess()
        self.assertEqual(ExitCode.BLOCKED, code)
        self.assertEqual("BLOCKED", result["status"])

    def test_platformio_uses_native_outdated_output(self) -> None:
        (self.root / "platformio.ini").write_text("[env:device]\nlib_deps =\n  vendor/OldLib@^1.0.0\n", encoding="utf-8")
        self.tool("pio", 'if [ "$1" = "--version" ]; then echo "PlatformIO 6"; else echo "OldLib  1.0.0  1.0.0  2.0.0"; fi\n')
        code, result = self.assess()
        self.assertEqual(ExitCode.SUCCESS, code)
        ecosystem = result["evidence"]["adapterResults"][0]["evidence"]["ecosystems"][0]
        self.assertEqual("PlatformIO", ecosystem["ecosystem"])
        self.assertEqual(["OldLib"], ecosystem["outdatedDependencies"])

    def test_swiftpm_without_external_packages_is_healthy(self) -> None:
        (self.root / "Package.swift").write_text('// swift-tools-version: 6.0\nimport PackageDescription\nlet package = Package(name: "Fixture")\n', encoding="utf-8")
        generated = self.root / ".xcode-derived" / "cache"
        generated.mkdir(parents=True)
        (generated / "requirements.txt").write_text("generated-package==1.0.0\n", encoding="utf-8")
        self.tool("swift", 'exit 97\n')
        code, result = self.assess()
        self.assertEqual(ExitCode.SUCCESS, code)
        ecosystems = result["evidence"]["adapterResults"][0]["evidence"]["ecosystems"]
        self.assertEqual(["SwiftPM"], [item["ecosystem"] for item in ecosystems])
        ecosystem = ecosystems[0]
        self.assertEqual("SwiftPM", ecosystem["ecosystem"])
        self.assertEqual([], ecosystem["outdatedDependencies"])
        self.assertEqual("NOT_REQUIRED", ecosystem["analyzer"]["version"])
