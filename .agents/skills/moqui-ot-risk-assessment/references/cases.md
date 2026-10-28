# Cases checked against the norms

Each case was read in full and checked with `method-check.md` against the IEC 62443-3-2 items in the database. Only
what passes is used as an example.

## Hardhat Security, "Practical guide to performing high and detailed level risk assessment as per IEC 62443-3-2 and NIST 800-30" (2024)

https://hardhatsecurity.com/2024/05/15/practical-guide-to-performing-high-and-detailed-level-risk-assessment-as-per-iec-62443-3-2-and-nist-800-30/

The article follows the four-step flow of NIST SP 800-30 (prepare, conduct, communicate, maintain) and puts the
IEC 62443-3-2 assessments inside the second step. Its tables and the worked values are images.

| Check | Result |
| --- | --- |
| 1 SUC and access points | partial: the SUC is scoped as a NIST preparation item; no security perimeter, no list of access points |
| 2 initial worst-case unmitigated risk | **passes**: the "high level" assessment is worst-case and ignores existing controls, as ZCR 2.1 |
| 3 zones and conduits | partial: "initial zones and conduits" are an output; the separation rules are not applied |
| 4 tolerable risk gate | **fails**: no tolerable risk, no ZCR 4 comparison |
| 5 threat description | partial: the EternalBlue + PsExec scenario on an engineering workstation gives vector and asset, not source and capability |
| 8 unmitigated then mitigated likelihood | **fails** in the detailed assessment: existing countermeasures are counted from the start |
| 9 SL-T | **fails**: SL-T is expanded as "service level target" (the norm: target security level, `3.2`); "residual SL-T" is not a notion of the norm (SL-T per zone and conduit, `4.6.7.1`; the residual is a risk, `4.6.11.1`) |
| 10-11 residual risk and countermeasures | partial: countermeasures listed (segmentation, anti-malware, authentication and access control, power backup, physical security), no residual-risk comparison |
| 12-14 documentation, CRS, approval | **fails**: executive summary, technical report and dashboard; no CRS, no session record, no approval |

Use as example: the worst-case framing of the initial assessment; the engineering-workstation scenario as a ZCR 5.1
threat once completed with source and capability; the countermeasure list mapped to SRs (segmentation SR 5.1/5.2,
anti-malware SR 3.2, authentication and access control SR 1.1/1.3/2.1). Do not use: its step structure, its SL-T
terms, its subjective-only ratings without an organisational scale.

## TRITON / TRISIS / HatMan: attack on a safety instrumented system (2017)

Sources read in full: Mandiant, "Attackers Deploy New ICS Attack Framework 'TRITON' and Cause Operational Disruption
to Critical Infrastructure" (14 Dec 2017,
https://cloud.google.com/blog/topics/threat-intelligence/attackers-deploy-new-ics-attack-framework-triton/); CISA
MAR-17-352-01 "HatMan - Safety System Targeted Malware" (update B, 27 Feb 2019).

Facts as stated: critical-infrastructure plant, unnamed; foothold on the DCS, then remote access to the SIS
engineering workstation (Windows); malware posing as a vendor log tool injected code into Triconex safety
controllers over the unauthenticated, reverse-engineered programming protocol, using a firmware zero-day (MP3008
firmware 10.0-10.4) to plant a memory-resident implant; implant commands accepted from any host of the safety network
whatever the key switch position; some controllers failed safe and shut the process down, which revealed the attack;
initial access unknown; nation-state sponsorship assessed with moderate confidence. Mandiant's threat model: use the
SIS to stop the process (financial loss), reprogram it to allow an unsafe state, or do that while the DCS creates the
hazard (harm to people, environment, equipment).

| Element of the case | Norm items in the database | Result |
| --- | --- | --- |
| DCS and SIS in one SUC | IEC 62443-3-2 `4.2.1.2.n1` | passes |
| integrated, bidirectional DCS-SIS networks; recommendation to segregate safety networks | ZCR 3.3 `4.4.4.1`, `4.4.4.2`; SR 5.1, SR 5.2 | passes: the norm requires it |
| engineering workstation able to program the SIS, not dual-homed | ZCR 3.3 (the workstation is a safety-related asset), `4.7.5.1` data flows and connected zones | passes, as a rule of this skill |
| unidirectional gateway for applications reading SIS data | IEC 62443-3-3 `9.4.2.p1` (boundary devices) | passes |
| programming protocol without authentication | SR 1.2; limited by `4.2.p2.li5` (authentication must not block the safety function) | passes, with the essential-function constraint |
| implant and logic changes | SR 3.4 `7.6.1` (unauthorized changes to software and information) | passes |
| whitelisting on hosts that reach the SIS | SR 3.2 guidance `7.4.2.p3` | passes |
| traffic monitoring | SR 6.2 | passes |
| key switch kept out of PROGRAM mode, change management and audit of its position | no loaded item names it; nearest SR 2.1, SR 3.4, CR 2.13; operations: IEC 62443-2-1 not loaded | **gap**: recorded, not forced onto an item |
| PHA of the process SIS | `4.3.1.2.p2` cites IEC 61511-2; IEC 61511 not loaded | **gap** for process plants |
| controller ACLs by IP and programming signatures bypassed from the workstation (CISA) | ZCR 5.8-5.9 effectiveness | example of a countermeasure rated low |
| attacker capability | Annex A `ANXA.p1.li4` (SL 4 profile) | input to SL-T |

What the case changed in the skill: the safety-and-security section (assets that can modify a safety function are
safety-related; essential functions of IEC 62443-3-3 `4.2`; SL vectors of `A.3.3`), the effectiveness rule for
controls anchored on the engineering workstation, and the rule for controls no loaded item covers.

## ESET Research, "DynoWiper update: Technical analysis and attribution" (2026)

https://www.welivesecurity.com/en/eset-research/dynowiper-update-technical-analysis-attribution/

An incident and malware analysis, not a risk-assessment method: an input to ZCR 5.1 (threats) and ZCR 6.6 (threat
environment). Facts as the article states them: energy company in Poland, December 2025; IT environment only, no OT
functionality observed; initial access unknown to the authors; attempted LSASS dump, attempted download of a
Kerberos attack tool and of a reverse SOCKS proxy; wiper staged on a domain share and run from there; endpoint
protection blocked execution; attribution to Sandworm with medium confidence.

| Use | How |
| --- | --- |
| ZCR 5.1 threat description (`4.6.2.2`) | source: state-sponsored actor; capability: extended resources, IACS-specific skills (the article recalls the actor's earlier grid attacks and Industroyer), high motivation -> the SL 4 threat profile of Annex A (`ANXA.p1.li4`); vectors: compromised domain credentials, domain-wide deployment from a share, external proxy; assets: Windows hosts of the business domain; unknown: initial access, persistence |
| ZCR 3.2 (`4.4.3.1`) | the incident stayed in the business domain; separation of IACS assets from business assets is the control that kept OT out of reach; the article also notes that separation reduces visibility for defenders |
| ZCR 6.6 (`4.7.7.1`) | a current threat with its intelligence source, cited with date |
| requirements | FR 1 / FR 2 (SR 1.1, 1.3, 1.5, 2.1: domain credentials and privileges), FR 3 (SR 3.2 malicious code protection, which is what limited the impact), FR 5 (SR 5.1, 5.2), FR 6 (SR 6.2), FR 7 (SR 7.3, 7.4 backup and recovery against wipers) |

Report structure worth reusing for threat-intelligence pages: key points; actor profile; history; technical analysis
per tool; deployment method; attribution with supporting and contradicting factors; conclusion; indicators;
technique table. ATT&CK ids are evidence labels next to the norm references.
