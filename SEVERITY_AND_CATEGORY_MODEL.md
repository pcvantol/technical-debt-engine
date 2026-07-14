# Severity and category model

Canonical severity is `INFO`, `LOW`, `MEDIUM`, `HIGH`, `CRITICAL`, or `UNKNOWN`. `UNKNOWN` is explicit for an unmappable native severity; it is not a silent downgrade. Adapter provenance may retain original tool severity.

Canonical extensible categories are `SIZE`, `COMPLEXITY`, `MAINTAINABILITY`, `DUPLICATION`, `DEPENDENCY`, `TEST`, `ARCHITECTURE`, `DOCUMENTATION`, `CONFIGURATION`, and `UNKNOWN`. Reserving a category does not introduce a Generation 1 capability.
