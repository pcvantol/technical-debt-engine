# Evidence Examples

Code Size assessment emits canonical JSON through `tde --format json assess --capability code-size <repository>`.

```json
{
  "command": "assess",
  "evidenceId": "sha256:<digest>",
  "evidenceStore": {
    "id": "<digest>",
    "immutable": true
  },
  "runtimeQualification": {
    "level": "QUALIFIED"
  }
}
```

The persisted record binds repository and candidate identity, runtime and schema versions, configuration digest, capability and adapter versions, analyzer version, canonical measurements, limitations, validation, policy evidence, Runtime Qualification, timing, and evidence digest.

```sh
tde --format json query <repository> --resource metrics
tde --format markdown report --capability code-size <repository>
```

Both commands consume the persisted evidence record. If no record exists, they return a blocked result and instruct the caller to run `assess` first.

Complexity uses the same persisted-evidence flow:

```sh
tde --format json assess --capability complexity <repository>
tde --format json query <repository> --resource findings
tde --format markdown report --capability complexity <repository>
```

Its adapter evidence includes the validated Radon version, native JSON hash, canonical repository/language/file/symbol measurements, and thresholded findings with measurement evidence references.

Code Size cross-platform qualification uses the same installed-wheel persistence path. Its workflow records the isolated Python/TDE/schema/capability/adapter/`cloc` versions, verified evidence-store retrieval, persisted Query/report and a normalized analytical projection for each runner. Raw native output and its hash are retained in the individual evidence record but excluded from cross-platform comparison because they contain runner-specific paths.

Policy evidence is persisted in the same immutable record and is queried without Runtime memory:

```json
{
  "policy": {"identifier": "tde.generation-1.default", "version": "1.0.0"},
  "decision": "PASS_WITH_WARNINGS",
  "decisionReason": "threshold rules triggered",
  "triggeredRules": [{"ruleId": "code_size.repository_lines", "measuredValue": 6123, "threshold": 0}],
  "affectedCapabilities": ["code_size"],
  "qualificationReference": {"measurementIds": ["code_size.repository.code"]}
}
```

Use `tde --format json query <repository> --resource policies` after assessment to retrieve that persisted decision.
