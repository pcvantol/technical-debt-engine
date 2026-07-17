# Declarative assessment profiles

An assessment profile selects capabilities and the policy configuration used by
the public runtime. Run the registered default profile with:

```sh
tde assess /path/to/repository
```

Select a bundled profile explicitly:

```sh
tde assess --profile minimal /path/to/repository
tde assess --profile standard /path/to/repository
```

`minimal` runs `code_size`; `standard` runs `code_size`, `complexity`, and the
optional read-only `coverage` capability. Coverage looks for configured paths
(`path`, `artifact`, `file`, or `paths`) before its standard locations. It never
runs tests; no artifact yields explicit unavailable coverage metrics rather than
an assessment failure.
`--capability` remains available for focused development and debugging runs.

Profiles are JSON documents with an identifier, version, description,
capability entries, a policy file and metadata. Each capability selects exactly
one of `required` or `optional`.

```json
{
  "identifier": "example",
  "version": "1.0.0",
  "description": "Example assessment.",
  "capabilities": [
    {"identifier": "code_size", "required": true, "optional": false}
  ],
  "policy": {"file": "../policies/generation-1.json"},
  "metadata": {"default": false}
}
```

Pass an explicit profile document with `--profile profile.json`. TDE validates
the profile before capability planning. Unknown or duplicated capabilities,
missing policy files and invalid structure block the assessment. Assessment
evidence records the profile identifier, version and canonical profile hash.
