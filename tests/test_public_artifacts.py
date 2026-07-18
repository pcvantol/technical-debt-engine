"""Black-box public CLI checks for the wheel and Docker artifacts.

The Docker test is opt-in because it downloads its pinned base image and cloc;
enable it in artifact-validation CI with TDE_RUN_DOCKER_INTEGRATION=1.
"""

from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest


REPOSITORY = Path(__file__).resolve().parents[1]


class PublicArtifactIntegrationTests(unittest.TestCase):
    def _sample_repository(self, directory: Path) -> Path:
        target = directory / "repository"
        target.mkdir()
        (target / "sample.py").write_text("# a public CLI fixture\nvalue = 1\n", encoding="utf-8")
        return target

    def _coverage_repository(self, directory: Path) -> Path:
        target = directory / "coverage-repository"
        target.mkdir()
        (target / "sample.py").write_text("value = 1\n", encoding="utf-8")
        (target / "coverage.xml").write_text('<coverage line-rate="0.5"><packages><package><classes><class><lines><line number="1" hits="1"/><line number="2" hits="0"/></lines></class></classes></package></packages></coverage>', encoding="utf-8")
        return target

    def _dependency_repository(self, directory: Path) -> Path:
        target = directory / "dependency-repository"
        target.mkdir()
        (target / "package.json").write_text('{"name":"fixture","dependencies":{"sample":"1.0.0"}}', encoding="utf-8")
        (target / "package-lock.json").write_text('{"lockfileVersion":3,"packages":{"":{"name":"fixture"},"node_modules/sample":{"version":"1.0.0"}}}', encoding="utf-8")
        tools = target / "bin"; tools.mkdir()
        npm = tools / "npm"; npm.write_text('#!/bin/sh\nif [ "$1" = "--version" ]; then echo "10.0.0"; else echo "{}"; fi\n', encoding="utf-8"); npm.chmod(0o755)
        return target

    def _wheel(self, directory: Path) -> Path:
        wheel_directory = directory / "wheel"
        subprocess.run([sys.executable, "-m", "pip", "wheel", "--no-deps", "--wheel-dir", str(wheel_directory), str(REPOSITORY)], check=True, capture_output=True, text=True)
        return next(wheel_directory.glob("technical_debt_engine_runtime-*.whl"))

    def test_wheel_public_cli_writes_qualified_canonical_evidence(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            wheel = self._wheel(root)
            environment = root / "venv"
            child_environment = {key: value for key, value in os.environ.items() if key != "PYTHONPATH"}
            subprocess.run([sys.executable, "-m", "venv", str(environment)], check=True, env=child_environment)
            commands = environment / ("Scripts" if os.name == "nt" else "bin")
            subprocess.run([str(commands / "pip"), "install", "--no-deps", str(wheel)], check=True, capture_output=True, text=True, env=child_environment)
            schemas = subprocess.run([str(commands / "tde"), "--format", "json", "schema"], capture_output=True,
                                     text=True, check=False, env=child_environment)
            self.assertEqual(0, schemas.returncode, schemas.stderr)
            self.assertEqual(6, len(json.loads(schemas.stdout)["schemas"]))
            target, evidence = self._sample_repository(root), root / "evidence"
            completed = subprocess.run([str(commands / "tde"), "--format", "json", "--store-location", str(evidence), "assess", "--capability", "code_size", str(target)], capture_output=True, text=True, check=False, env=child_environment)
            self.assertEqual(0, completed.returncode, completed.stderr)
            response = json.loads(completed.stdout)
            self.assertEqual("QUALIFIED", response["runtimeQualification"]["level"])
            self.assertEqual("code_size", response["evidence"]["capabilityResults"][0]["capabilityId"])
            self.assertEqual("cloc", response["evidence"]["adapterResults"][0]["analyzer"]["id"])
            self.assertEqual("tde.assessment-evidence", response["evidence"]["assessment"]["schema"]["name"])
            self.assertEqual("1", response["evidence"]["policyEvidence"]["schema"]["compatibilityVersion"])
            self.assertTrue(next((evidence / "evidence").glob("*.json")))

    def test_wheel_public_cli_consumes_coverage_artifact(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary); wheel = self._wheel(root); environment = root / "venv"
            child_environment = {key: value for key, value in os.environ.items() if key != "PYTHONPATH"}
            subprocess.run([sys.executable, "-m", "venv", str(environment)], check=True, env=child_environment)
            commands = environment / ("Scripts" if os.name == "nt" else "bin")
            subprocess.run([str(commands / "pip"), "install", "--no-deps", str(wheel)], check=True, capture_output=True, text=True, env=child_environment)
            completed = subprocess.run([str(commands / "tde"), "--format", "json", "assess", "--capability", "coverage", str(self._coverage_repository(root))], capture_output=True, text=True, check=False, env=child_environment)
            self.assertEqual(0, completed.returncode, completed.stderr)
            response = json.loads(completed.stdout)
            self.assertEqual("coverage", response["evidence"]["capabilityResults"][0]["capabilityId"])
            self.assertEqual("cobertura-xml", response["evidence"]["adapterResults"][0]["evidence"]["parser"])

    def test_wheel_public_cli_normalizes_dependency_health(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary); wheel = self._wheel(root); environment = root / "venv"
            child_environment = {key: value for key, value in os.environ.items() if key != "PYTHONPATH"}
            subprocess.run([sys.executable, "-m", "venv", str(environment)], check=True, env=child_environment)
            commands = environment / ("Scripts" if os.name == "nt" else "bin")
            subprocess.run([str(commands / "pip"), "install", "--no-deps", str(wheel)], check=True, capture_output=True, text=True, env=child_environment)
            target = self._dependency_repository(root)
            child_environment["PATH"] = str(target / "bin") + os.pathsep + child_environment.get("PATH", "")
            completed = subprocess.run([str(commands / "tde"), "--format", "json", "assess", "--capability", "dependency_health", str(target)], capture_output=True, text=True, check=False, env=child_environment)
            self.assertEqual(0, completed.returncode, completed.stderr)
            response = json.loads(completed.stdout)
            self.assertEqual("dependency_health", response["evidence"]["capabilityResults"][0]["capabilityId"])
            self.assertEqual("npm", response["evidence"]["adapterResults"][0]["evidence"]["ecosystems"][0]["ecosystem"])

    @unittest.skipUnless(os.environ.get("TDE_RUN_DOCKER_INTEGRATION") == "1" and shutil.which("docker"), "set TDE_RUN_DOCKER_INTEGRATION=1 to build and run the Docker artifact")
    def test_docker_public_cli_writes_qualified_canonical_evidence(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            wheel = self._wheel(root)
            context = root / "context"
            (context / "wheel").mkdir(parents=True)
            shutil.copy2(REPOSITORY / "Dockerfile", context / "Dockerfile")
            shutil.copy2(wheel, context / "wheel" / wheel.name)
            digest = hashlib.sha256(wheel.read_bytes()).hexdigest()
            image = "tde-public-cli-integration:local"
            subprocess.run(["docker", "build", "--tag", image,
                            "--build-arg", "CANDIDATE_SHA=local-test",
                            "--build-arg", "TDE_VERSION=0.1.0",
                            "--build-arg", f"WHEEL_FILE={wheel.name}",
                            "--build-arg", f"WHEEL_SHA256={digest}",
                            "--build-arg", "SOURCE_DATE_EPOCH=0",
                            "--build-arg", "CREATED=1970-01-01T00:00:00Z", str(context)], check=True)
            target, evidence = self._sample_repository(root), root / "evidence"
            evidence.mkdir(mode=0o777)
            os.chmod(evidence, 0o777)
            completed = subprocess.run(["docker", "run", "--rm", "--volume", f"{target}:/workspace/repository:ro", "--volume", f"{evidence}:/workspace/evidence", image, "--format", "json", "--store-location", "/workspace/evidence", "assess", "--capability", "code_size", "/workspace/repository"], capture_output=True, text=True, check=False)
            self.assertEqual(0, completed.returncode, completed.stderr)
            response = json.loads(completed.stdout)
            self.assertEqual("QUALIFIED", response["runtimeQualification"]["level"])
            self.assertEqual("tde.assessment-evidence", response["evidence"]["assessment"]["schema"]["name"])
            self.assertEqual("1", response["evidence"]["assessmentDecision"]["schema"]["compatibilityVersion"])
            self.assertTrue(next(evidence.glob("evidence/*.json")))
            coverage = subprocess.run(["docker", "run", "--rm", "--volume", f"{self._coverage_repository(root)}:/workspace/repository:ro", image, "--format", "json", "assess", "--capability", "coverage", "/workspace/repository"], capture_output=True, text=True, check=False)
            self.assertEqual(0, coverage.returncode, coverage.stderr)
            self.assertEqual("cobertura-xml", json.loads(coverage.stdout)["evidence"]["adapterResults"][0]["evidence"]["parser"])
