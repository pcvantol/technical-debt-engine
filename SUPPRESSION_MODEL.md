# Suppression model

Suppressions and waivers have stable ID, finding/rule scope, reason, owner, creation date, expiration or review trigger, policy reference, candidate/branch scope, and optional compensating control. They never delete findings from evidence; they affect qualification and reporting projections only.

Expired or ambiguous suppression affecting required qualification fails closed. See the configuration schema and [`fixtures/suppression-config.json`](fixtures/suppression-config.json).
