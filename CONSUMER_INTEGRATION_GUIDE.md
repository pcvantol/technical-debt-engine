# Consumer Integration Guide

1. Select a specific DJConnect repository through canonical repository ownership.
2. Pin one published TDE CLI version; do not use a workspace or branch checkout.
3. Invoke `tde` using canonical configuration and consume JSON evidence/exit codes.
4. Validate schema/runtime versions, candidate/repository IDs and evidence integrity.
5. Store source evidence immutably and project platform summaries without changing it.

`djconnect-pi` completed steps 1–5 in Observe mode with the exact published
`technical-debt-engine-runtime==0.2.0` distribution. Its retained evidence and
current limitations are recorded in
[the Phase 1 Observe record](docs/djconnect-observe-pilot.md). No other
consumer is selected by this guide.
