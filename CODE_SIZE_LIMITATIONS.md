# Code Size limitations

- `cloc` must be explicitly installed on PATH; TDE does not install it. The qualification workflow provisions checksum-verified `cloc 2.10` per runner, but this is not runtime installation behavior.
- Logical-line counting and language percentage are unavailable in this adapter version.
- Classification uses documented default path rules; custom configuration overrides are pending schema extension.
- Qualification covers `cloc 2.10` on GitHub-hosted Ubuntu, macOS and Windows runners only; other `cloc` versions, operating-system versions and self-hosted runners require their own evidence.
