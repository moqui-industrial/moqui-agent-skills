# Checking a risk-assessment method against IEC 62443-3-2

Read each cited item in the database first (`get_norm_tree`, agreement `IEC-62443-3-2-2020-EN`). A check passes only
when the method does what the item requires; "similar" is a fail with an explanation.

| # | Check | Items | Typical failure |
| --- | --- | --- | --- |
| 1 | The SUC is identified with its security perimeter and **all** access points | `4.2.1.1` | starts from an asset inventory without a perimeter |
| 2 | An initial assessment gives the worst-case unmitigated risk of the whole SUC | `4.3.1.1` | goes straight to per-asset scenarios |
| 3 | Zones and conduits come from the initial assessment and the separation rules 3.2-3.6 | `4.4.2.1` ... `4.4.7.1` | zones drawn from the network diagram only; safety zone not separated |
| 4 | Initial risk is compared with an explicit tolerable risk before the detailed assessment | `4.5.2.1`, `4.7.9.1` | no tolerable risk stated; every system assessed in detail by default |
| 5 | Each threat has source, capability, vectors and affected assets | `4.6.2.2` | a scenario names the exploit but not who would use it and with what skill |
| 6 | Vulnerabilities include the access points | `4.6.3.1` | only CVEs of hosts |
| 7 | Consequences are worst case on safety, financial, business interruption, environment | `4.6.4.1` | IT-only impact (data loss) |
| 8 | Likelihood is first **unmitigated** (cyber countermeasures removed), then re-evaluated with countermeasures | `4.6.5.2`, `4.6.10.1` | one likelihood, already counting the firewall |
| 9 | SL-T per zone and per conduit; method stated (Annex A, Annex B or risk difference) | `4.6.7.1`, `4.6.7.2` | SL-T per asset; "residual SL-T"; SL-T called a service level |
| 10 | Residual risk per threat, compared with tolerable risk; accept / transfer / mitigate per policy | `4.6.11.1`, `4.6.12.1` | residual expressed as a security level instead of a risk |
| 11 | Additional countermeasures are technical, administrative or procedural and loop back to re-evaluation | `4.6.13.1` | a list of controls with no re-evaluation |
| 12 | Results documented with classification, session dates, participants, archived inputs | `4.6.14.1` | report without dates or participants |
| 13 | A CRS with at least the content of ZCR 6.2-6.9; zone characteristics as in `4.7.5.1` | `4.7.2.1`, `4.7.5.1` | executive summary and dashboard only |
| 14 | Asset owner management approves | `4.8.2.1` | no approval step |
| 15 | Terms as defined: SL, SL-T, SL-A, SL-C, residual risk, conduit, zone | `3.1`, `3.2` | redefined terms |

Methods the norm leaves open (and where they may enter): the likelihood and consequence scales and the risk matrix
(the organisation's, Annex B as example: checks 4, 8, 10), the way threats are found (threat modelling, ATT&CK,
NIST SP 800-30 threat taxonomy: check 5), the SL-T method (check 9). Consequence-only methods are allowed
(`4.6.5.2.p5`).
