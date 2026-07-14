# Persistence Architecture

## Purpose and status

This is the canonical product definition for Technical Debt Engine (TDE)
persistence. It defines how canonical engineering evidence is stored, indexed,
retained, retrieved, and evolved across product generations. It does not alter
Runtime Architecture, Evidence Store implementation, Query implementation, or
storage configuration.

Canonical Evidence is the source of truth. Persistence provides durable,
portable storage for that evidence; it never replaces, rewrites, or invents
canonical evidence.

## Persistence philosophy

Canonical engineering evidence remains immutable, portable, versioned,
schema-driven, and independently verifiable. A storage system may add location,
index, retention, and access metadata, but cannot change an evidence record's
meaning, identity, integrity, or schema compatibility.

```text
Canonical Evidence
        ↓
Persistence Adapter
        ↓
Storage Backend
        ↓
Query Engine
        ↓
Consumers
```

The Query Engine is the only supported read path for consumers. Consumers do
not query a filesystem, SQLite database, object store, or future service
directly. Persistence adapters write and retrieve immutable records behind the
storage boundary; they do not qualify, normalize, or modify evidence.

## Canonical storage hierarchy

```text
Canonical Evidence (JSON)
        ↓ derives indexes from
SQLite Index
        ↓ may project compatible metadata to
Future PostgreSQL Metadata
        ↓ may reference immutable payloads in
Future Object Storage
```

Every upper layer derives from lower authoritative evidence and can be rebuilt
from compatible canonical JSON. An index, metadata database, cache, or object
reference is never authoritative if it conflicts with verified canonical JSON.

## Generation model

| Generation | Supported persistence | Product responsibility |
| --- | --- | --- |
| Generation 1 | Canonical JSON Evidence, filesystem persistence, filesystem Evidence Store, immutable evidence records, persisted Query | Durable local evidence with integrity-verified retrieval and portable inspection. |
| Generation 2 | SQLite indexing, repository-local database, fast Query, indexed search, trend acceleration | Derived local indexes accelerate access; SQLite remains an implementation detail and JSON remains authoritative. |
| Generation 3 | PostgreSQL, object storage, distributed Evidence Store, organization persistence, cloud persistence | Optional evaluated targets that must remain compatible with local-first canonical evidence. |

Generation labels define product direction, not implementation completion or
publication. New backends require separate architecture, compatibility,
qualification, migration, and operational evidence before support is claimed.

## Storage responsibilities

| Layer | Responsibilities | Prohibitions |
| --- | --- | --- |
| Canonical JSON Evidence | Immutable record, schema/runtime/provenance identity, integrity verification, portable interchange. | Never mutate published evidence. |
| Persistence Adapter | Store/retrieve verified records, map locations, expose backend limitations. | Never alter evidence or become a consumer query API. |
| Filesystem Evidence Store | Human-readable records, portability, local inspection, backup-friendly layout. | Never infer or overwrite canonical evidence. |
| SQLite Index | Derived indexing, search, fast Query and trend acceleration. | Never redefine evidence, qualification, or schema meaning. |
| Future cloud backends | Optional shared metadata/payload durability and organization-scale operations. | Never require cloud access for local-first use or bypass Query. |
| Query Engine | Versioned, read-only projections from persisted canonical evidence. | Never invoke analyzers, mutate records, or expose backend-specific reads. |

## Filesystem and SQLite

Filesystem persistence remains the portable, human-readable and
backup-friendly baseline. Generation 1 uses immutable filesystem evidence
records and manual retention. Its role is durability and inspection, not a
different evidence representation.

SQLite is the Generation 2 repository-local acceleration layer. It may index
canonical evidence identity, repository/candidate metadata, measurements,
findings, qualification, and compatible trend keys. Indexes are disposable
derived state: an implementation must rebuild them from verified JSON rather
than treating SQLite rows as canonical evidence.

## Cloud and local-first evolution

PostgreSQL metadata, object storage, distributed Evidence Store, organization
persistence, and cloud persistence are Generation 3 evaluation targets. They
are optional extensions for compatible shared use cases. Local filesystem
evidence remains the default philosophy: a repository can create, verify,
retain, back up, and query its own evidence without cloud dependency.

Cloud persistence must preserve immutable identities, schema compatibility,
integrity verification, access boundaries, and the Query Engine-only consumer
read model. It must not turn an unavailable remote service into a new source of
truth or prevent local evidence operation.

## Retention lifecycle

| Generation | Retention approach |
| --- | --- |
| Generation 1 | Manual retention of immutable records; history listing; no automatic cleanup. |
| Generation 2 | Explicit retention policies, cleanup, and compaction of derived/index state without mutating canonical evidence. |
| Generation 3 | Organization retention, legal/operational controls, and optional distributed lifecycle management. |

Retention may delete copies only under an explicit policy and authority. It
must never silently modify a canonical record. Index compaction and cache
cleanup are not evidence mutation; source record preservation and provenance
rules remain explicit.

## Consumer model

| Consumer | Persistence access |
| --- | --- |
| CLI | Uses the Query Engine for persisted results and reports. |
| Query Engine | The sole versioned read-only projection surface. |
| Dashboard | Future consumer of Query results, never a backend reader. |
| Future REST API | Future Query-facing service contract, not direct database access. |
| Future Cloud | Uses compatible persistence adapters and Query contracts. |

## Evolution guardrails

- Canonical JSON remains authoritative across every backend.
- Evidence records are immutable; corrections create new records with
  provenance.
- Backends and indexes are replaceable implementation details behind persistence
  adapters.
- Consumers remain storage-independent and use only Query results.
- Schema/version compatibility and integrity validation occur before evidence is
  trusted or indexed.
- This product definition does not implement SQLite, cloud persistence,
  retention automation, migrations, or new Query APIs.
