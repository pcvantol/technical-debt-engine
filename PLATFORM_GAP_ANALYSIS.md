# Platform gap analysis

| Gap | Risk | Recommended next increment |
| --- | --- | --- |
| Query does not read persisted records | History consumers can bypass the Evidence Store | Evidence Store / Query integration |
| Empty evidence can be `QUALIFIED` | Confidence overstates analysis coverage | Qualification completeness hardening |
| Reporting is absent | No canonical report consumer yet | Reporting Runtime |
| Analyzer coverage is limited | Cross-platform/language confidence is bounded | Capability qualification expansion |
