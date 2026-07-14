# Adapter runtime

The runtime owns adapter planning and execution; adapters own measurement. Adapter planning determines selected adapters, execution ordering, shared-resource constraints, parallel opportunities, and unsupported adapter states.

An adapter receives a bounded request, invokes its authoritative native analyzer where appropriate, and returns raw observations plus tool identity and limitations. It does not normalize global results, qualify outcomes, report, dispatch another adapter, or communicate directly with another adapter.

Adapter lifecycle is **planned → implemented → validated → qualified → deprecated → removed**. Each adapter evolves independently and declares its tool/version compatibility, supported languages, and canonical mapping limitations.
