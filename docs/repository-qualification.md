# Repository Qualification

`tde qualify` runs a full profile-driven assessment and produces a separate,
immutable repository qualification result. It does not contain analyzer-specific
logic: the selected assessment profile continues to drive capability planning.

A repository can be supplied declaratively with `--repository-definition`:

```json
{
  "identifier": "example.service",
  "name": "Example Service",
  "repositoryRoot": "../service",
  "repositoryType": "source",
  "primaryLanguage": "Python",
  "defaultAssessmentProfile": "standard",
  "metadata": {"owner": "platform"}
}
```

All fields are required. Relative repository roots are resolved from the definition
file. The selected profile must be a registered declarative profile. If no definition
is supplied, the CLI creates an equivalent local definition from the requested target;
this is a convenience only and does not add repository-specific behavior to the
Runtime.

```sh
tde --repository-definition repository.json qualify
tde --repository-definition repository.json --profile minimal qualify
```

The result includes the repository identity, profile identity, Runtime and schema
versions, assessment decision, qualification status, duration, timestamp and a
reference to the immutable assessment evidence. It is written to
`.tde/qualifications` by default; use `--qualification-location` to store it outside
the assessed repository (for example when qualifying a read-only checkout).

`tde qualify` returns the normal public execution/policy exit code. A missing analyzer
is `ANALYZER_NOT_FOUND`; malformed definitions and schema failures are fail-closed.
