# Test Reality Report

The test runner is Python `unittest`. Audit execution: `PYTHONPATH=src python -m unittest discover -s tests -v`.

| Category | Tests | Reality |
| --- | ---: | --- |
| Unit / engine | 21 | Baseline, execution, query, runtime, qualification, store and trend mostly use fixtures or in-process objects. |
| CLI | 20 | Calls `main()` in-process. It does not prove installed console behavior or tool availability. |
| Real-analyzer | 2 | Code Size and Complexity exercise the adapters, but only with host-installed tools. |
| Schema / contract | 0 dedicated | Some runtime tests assert shape; no complete runtime schema suite was observed. |
| Integration / end-to-end | 0 | No installed-package CLI-to-real-analysis flow. |
| Packaging / release / dogfooding / governance | 0 | No test validates wheel installation, source distribution, release workflow or published artifact. |

**Totals: 41 passed, 0 failed, 0 skipped. Coverage was not configured or produced.**

Tests create a false impression of product maturity where they assert internal dispatch or fixture results while the installed CLI emits empty capability evidence. The `test_run_command_is_operational` and `test_cli_assess_emits_canonical_evidence_fields` prove command shape, not that an analyzer was executed through the public CLI.
