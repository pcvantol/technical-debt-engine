"""Patch-level parser repair requirements must be enforced at discovery."""
import unittest
from unittest.mock import patch
from tde_runtime.analyzer_discovery import discover


class AnalyzerPatchDiscoveryTests(unittest.TestCase):
    def test_patch_requirement_rejects_older_parser_and_accepts_exact_or_newer(self):
        for version, status in [('1.24.2', 'ANALYZER_NOT_FOUND'),
                                ('1.24', 'ANALYZER_NOT_FOUND'),
                                ('1.24.3', 'VALID'), ('1.25.0', 'VALID')]:
            with self.subTest(version=version), \
                 patch('tde_runtime.analyzer_discovery.shutil.which', return_value='/tools/lizard'), \
                 patch('tde_runtime.analyzer_discovery.subprocess.run') as run:
                run.return_value.stdout = version
                self.assertEqual(status, discover('lizard', (1, 24, 3), 10)['status'])

    def test_existing_two_component_minimum_accepts_patch_version(self):
        with patch('tde_runtime.analyzer_discovery.shutil.which', return_value='/tools/radon'), \
             patch('tde_runtime.analyzer_discovery.subprocess.run') as run:
            run.return_value.stdout = 'radon 6.0.1'
            self.assertEqual('VALID', discover('radon', (6, 0), 10)['status'])
