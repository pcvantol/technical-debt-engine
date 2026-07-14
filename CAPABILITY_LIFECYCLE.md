# Capability lifecycle

Capabilities evolve independently through these states:

| State | Meaning |
| --- | --- |
| `PLANNED` | Contract intent exists; no implemented behavior is claimed. |
| `IMPLEMENTED` | Behavior exists but is not yet validated. |
| `VALIDATED` | Declared validation has passed. |
| `QUALIFIED` | Compatible evidence has passed an explicit qualification policy. |
| `DEPRECATED` | Still recognized with replacement/migration guidance. |
| `REMOVED` | No longer available for new execution; historic evidence remains interpretable. |

Lifecycle state does not imply the state of another capability, runtime, adapter, schema, consumer, or release. A transition requires registry update, compatibility statement, evidence where applicable, and a focused engineering increment.
