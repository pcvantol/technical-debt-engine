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
