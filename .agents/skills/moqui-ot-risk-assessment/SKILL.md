---
name: moqui-ot-risk-assessment
description: Perform an OT / IACS cyber security risk assessment as the loaded norms require it - IEC 62443-3-2 ZCR 1 to 7 (system under consideration, initial worst-case risk, zones and conduits, tolerable risk, detailed per-threat assessment with unmitigated and residual risk and SL-T, cyber security requirements specification, asset owner approval), IEC 62443-3-3 system requirements by foundational requirement and security level, IEC 62443-4-2 and 4-1, and the Cyber Resilience Act for products with digital elements - reading every requirement from the norm items in the Moqui database, never from memory, a blog or a vendor method. Use it whenever a plant, machine, control system or bill of materials has to be assessed for OT cyber security, zones, conduits or SL-T have to be defined, a threat-intelligence or incident report has to become threats, countermeasures or requirements, or a third-party method has to be checked against IEC 62443-3-2.
---

# moqui-ot-risk-assessment: OT cyber security risk assessment from the norms

**The norms are the first and highest guide.** Every step, field and decision of an assessment comes from a norm item
read in the database (`moqui-norm-search`: `get_norm_tree`, `get_item_references`, `search_norms`). Methods from
elsewhere (NIST SP 800-30, STRIDE, MITRE ATT&CK, a consultancy template, a blog post) may be used only *inside* a step
the norm defines and only where the norm leaves the method open; they never add, drop or rename a step. When a source
and the norm disagree, the norm wins and the report says so.

Before writing anything about a clause, read it: `get_norm_tree` with the item id below. The ids are those of the
loaded editions (`IEC-62443-3-2-2020-EN`, `IEC-62443-3-3-2013-EN`, `IEC-62443-4-2-2019-EN`,
`IEC-62443-4-1-2018-EN`, `IEC-TR-62443-3-1-2009-EN`, `EU-REG-2024-2847-*`). The texts of IEC standards are licensed:
quote them only in internal reports; in anything shared outside, cite the item id and paraphrase.

## The workflow is the norm's (IEC 62443-3-2 clause 4, Figure 1 and Figure 2)

| ZCR | Item | What the organisation produces | Gate |
| --- | --- | --- | --- |
| 1.1 | `4.2.1.1` | the SUC: security perimeter and every access point | - |
| 2.1 | `4.3.1.1`, guidance `4.3.1.2` | initial assessment: worst-case **unmitigated** risk of the SUC to the mission-critical operations (PHA and functional safety results feed the worst case; threat intelligence is taken into account) | - |
| 3.1-3.6 | `4.4.2.1` ... `4.4.7.1` | zones and conduits grouped by risk; business assets separated from IACS assets; safety-related assets in their own zones (or the whole zone becomes safety-related); temporary, wireless and externally connected devices separated (3.4-3.6 are recommendations) | - |
| 4.1 | `4.5.2.1` | initial risk compared with the organisation's **tolerable risk** | only if it exceeds the tolerable risk does ZCR 5 follow |
| 5.1 | `4.6.2.1`, `4.6.2.2` | per zone or conduit: the list of threats; each with its source, the capability of the source, the vectors and the affected assets (grouping into classes is allowed) | - |
| 5.2 | `4.6.3.1` | known vulnerabilities of the assets, access points included | - |
| 5.3 | `4.6.4.1` | consequence and impact per threat scenario, worst case on safety, finance, business interruption, environment | - |
| 5.4 | `4.6.5.1`, `4.6.5.2` | **unmitigated** likelihood: existing cyber countermeasures hypothetically removed; inherent component protections and non-cyber protection layers (physical security, mechanical safeguards) may count | - |
| 5.5 | `4.6.6.1` | unmitigated risk = impact x unmitigated likelihood | - |
| 5.6 | `4.6.7.1`, `4.6.7.2` | **SL-T for each zone and conduit** (single value or a vector per foundational requirement; the norm prescribes no method, Annex A and Annex B give options) | - |
| 5.7 | `4.6.8.1` | unmitigated risk vs tolerable risk: accept, transfer or mitigate | mitigate -> 5.8-5.12, otherwise document (5.13) |
| 5.8 | `4.6.9.1` | existing countermeasures and their effectiveness | - |
| 5.9 | `4.6.10.1` | likelihood and impact re-evaluated with the countermeasures | - |
| 5.10 | `4.6.11.1` | **residual risk** per threat (mitigated likelihood x mitigated impact) | - |
| 5.11 | `4.6.12.1` | residual risk vs tolerable risk: accept, transfer or mitigate per the organisation's policy | - |
| 5.12 | `4.6.13.1` | additional countermeasures (technical, administrative, procedural) where residual risk is still too high | back to 5.9 |
| 5.13 | `4.6.14.1` | documented results: classification of the document, date of every session, names and titles of participants, archived inputs (architecture drawings, PHA, vulnerability and gap assessments, threat sources) | - |
| 6.1-6.9 | `4.7.2.1` ... `4.7.10.1` | the **CRS** (cyber security requirements specification), with at least: SUC description, zone and conduit drawings, zone and conduit characteristics (the list in `4.7.5.1`, SL-T included), operating environment, threat environment with its intelligence sources, organisational policies, tolerable risk, regulatory requirements | - |
| 7.1 | `4.8.2.1` | approval of the results by the asset owner management accountable for safety, integrity and reliability | end |

Definitions to apply literally: `3.1.13` residual risk, `3.1.15` security level, `3.2` abbreviations (SL-T, SL-A,
SL-C), Annex A (the four security levels by the means, resources, skills and motivation of the attacker:
`ANXA.p1.li1` ... `li4`), Annex B (example risk matrices and scales: `TABB.1` ... `TABB.6`, informative).

## From SL-T to requirements

- Each zone or conduit gets an SL-T (ZCR 5.6); the CRS lists its applicable security requirements (`4.7.5.1.ptl`).
- System requirements: IEC 62443-3-3, one clause per foundational requirement FR 1 ... FR 7 (items `5` ... `11`),
  each SR with requirement enhancements by security level; read the SR and its REs with `get_norm_tree`.
- Component requirements: IEC 62443-4-2 (CR, by component type); product development: IEC 62443-4-1.
- The vocabulary already holds the SL-C capability features per FR (`iac-sl-1` ... `ra-sl-4`, groups `fg-fr1-iac`
  ... `fg-fr7-ra`): a component's achieved capability is a feature of its product; compare it with the zone's SL-T.
- Products with digital elements placed on the EU market: the CRA (Annex I essential requirements, Article 13
  obligations, Article 31 technical documentation); `find_norms_for_product` gives the items per product.

## Moqui records (what exists today)

| Notion | Record |
| --- | --- |
| SUC | the root `Product` of the bill (machine, cell, plant section), or the installed `Asset` / `Facility` |
| zone, conduit | `Product` of type `CmpPtFunction`, `purposeEnumId` `CmpDepSecurityZone` / `CmpDepSecConduit`, under the SUC with `ProductAssoc` `CmpPatFunction`; members with `CmpPatFunctionMember` (`add_function_product`) |
| requirements of the norms | `Requirement` `RqTpNorm` and tasks per ZCR and per SR, from `plan_norm_project` / `create_norm_project` (`moqui-norm-requirements`); each one cites its item |
| component capability (SL-C) | `ProductFeatureAppl` of the SL-C features on the component product (`PfatStandard`) |
| SL-T of a zone or conduit | the same features on the zone or conduit level with type `CmpPfatTarget`: the plan then selects the IEC 62443-3-3 SRs and REs from Table B.1 |
| installed zones, conduits, functions | `DeviceGroup` with `Device.purposeEnumId` (`moqui-compliance-intake`, installation) |
| the report (CRS, assessment results, threat environment) | wiki pages (`moqui-compliance-report`) |

Not modelled yet, keep in the report until a model is agreed: the threat register (5.1-5.12 rows) and the
tolerable-risk matrix of the organisation. Do not invent entities for them. Before an applicability decision or a
report leaves the company: `moqui-compliance-verify` (checks and verifier gate).

## Procedure

1. **Scope with the norm open.** Read ZCR 1 and ZCR 2 (`get_norm_tree` `4.2`, `4.3`). Define the SUC and list every
   access point (remote access, fieldbus gateways, engineering laptops, USB, wireless, vendor links). Ask the asset
   owner for: the tolerable risk (their risk matrix; Annex B is only an example), PHA / functional safety results,
   threat intelligence sources.
2. **Initial assessment (ZCR 2)**: worst case, no countermeasures. Output: a ranked list of SUC functions by impact.
3. **Zones and conduits (ZCR 3)**: apply 3.1-3.6 one by one and record which rule produced each zone. Load them as
   function levels; `plan_norm_project` then reports products that communicate but sit in no zone.
4. **Gate (ZCR 4)**: if the initial risk is within tolerable risk, stop and document; say so explicitly.
5. **Detailed assessment (ZCR 5) per zone and conduit**, threat by threat, in the norm's order: threats (with the four
   elements of `4.6.2.2`), vulnerabilities, consequence, **unmitigated** likelihood and risk, SL-T, decision,
   existing countermeasures, residual risk, decision, additional countermeasures. Never skip the unmitigated pass:
   a method that rates likelihood with the existing controls in place from the start does not meet 5.4-5.5.
6. **Requirements**: from the SL-T of each zone to the SRs and REs of IEC 62443-3-3 (and CRs of 4-2 for the
   components); create the norm project; every countermeasure of 5.12 traces to an SR/CR item.
7. **CRS (ZCR 6)** and **documentation (5.13)** as wiki pages with `moqui-compliance-report`; the zone and conduit
   characteristics table has exactly the fields of `4.7.5.1`.
8. **Approval (ZCR 7)**: the asset owner approves; never mark it approved yourself.

## Safety and security together

A safety instrumented system or a safety-related control system is part of the SUC (`4.2.1.2.n1` names SIS among
the subsystems), and it is where the worst consequences sit:
- **Zones**: safety-related assets go in their own zones, or the whole zone becomes safety-related (ZCR 3.3,
  `4.4.4.1`); such zones usually need a higher protection level (`4.4.4.2`). Apply it as a rule on the Moqui model:
  every product that is a member of a safety function level (`moqui-norm-requirements`: function products with a
  safety purpose and their input / logic / output members) belongs to a safety-related zone, **and so does every
  asset able to change it** - the engineering workstation that programs the safety controller, its programming
  network, its laptops. A tool that can reprogram a safety zone from another zone is a conduit into it and must be
  assessed as one (data flows and connected zones of `4.7.5.1`).
- **Consequences**: take the worst case from the PHA and functional-safety results (`4.3.1.2.p2`). The design
  hazards and safety functions of the machine come from IEC 62061 / ISO 12100 in the database; the process-industry
  SIS norm (IEC 61511) is only cited, not loaded: say so when the SUC is a process plant.
- **Essential functions** (IEC 62443-3-3 `4.2`): no security measure may stop a safety function from acting.
  Identification, authentication and authorization must not prevent the initiation of a safety instrumented function
  (`4.2.p2.li5`), accounts of essential functions are never locked out (`4.2.p2.li2`), essential functions survive
  fail-close or island mode of the zone boundary (`4.2.p2.li7`), and a denial of service on the SIS network must not
  stop the safety function (`4.2.p2.li8`). Check every countermeasure of ZCR 5.12 against this list before proposing it.
- **SL vectors**: IEC 62443-3-3 `A.3.3` gives the vector notation with examples for a BPCS zone (SL-T) and a SIS
  engineering workstation (SL-C); use the vector, per FR, for safety zones rather than a single number.

## Effectiveness of countermeasures (ZCR 5.8-5.9)

Rate a countermeasure by what it still stops when the attacker already holds the trusted path. Controls anchored on
the engineering workstation (address-based access lists on the controller, programming signatures whose keys sit on
the workstation) do not stop an attacker who controls that workstation; they count for little in the re-evaluation
of likelihood. Physical program-enable switches, logic integrity checks (IEC 62443-3-3 SR 3.4, `7.6.1`), separation
of the programming network (SR 5.1, SR 5.2 with unidirectional gateways among the boundary devices, `9.4.2.p1`) and
monitoring (SR 6.2) act outside that path.

## When no loaded item covers a control

A source may recommend a control the loaded norms do not name (a physical key switch left out of program mode, change
management of the key position, operational procedures of the asset owner). Do not attach it to a loosely related
item to make it look normative. Record it as: the control, its source, the nearest loaded items (for a key switch:
SR 2.1 authorization enforcement, SR 3.4 integrity, component requirement CR 2.13 on physical diagnostic and test
interfaces), and the norm that would cover it if loaded (asset-owner security programme: IEC 62443-2-1, cited by five
loaded norms but not loaded). Missing norms are a finding of the assessment, not a reason to drop the control.

## Using threat intelligence and incident reports

An incident or malware analysis (for example an APT wiper report) is an input to ZCR 5.1 and ZCR 6.6, not a method:
1. Extract, per attack step, the threat source, its capability, the vector and the assets touched (`4.6.2.2`). Mark
   what the report does **not** know (initial access, persistence) instead of filling it in.
2. Map the source's capability to the Annex A level it would defeat (an actor with extended resources, IACS skills
   and high motivation is the SL 4 threat profile); this informs, not decides, the SL-T.
3. Map each technique to the foundational requirement whose SRs counter it (for example: credential dumping and
   domain-wide deployment -> FR 1 / FR 2, SR 1.1, 1.3, 1.5, 2.1; staging on a share and spreading -> FR 5, SR 5.1,
   5.2; malware execution -> FR 3, SR 3.2; destruction of data -> FR 7, SR 7.3, 7.4; detection -> FR 6, SR 6.2),
   reading each SR in the database before citing it.
4. Record whether the incident crossed the IT/OT boundary; a business-network incident tests ZCR 3.2.
5. ATT&CK ids are kept as evidence labels next to the norm references, never instead of them.

## Checking a third-party method or example against the norm

Before adopting a method, template or worked example, check it with `references/method-check.md`: every ZCR present
and in order, the unmitigated and residual passes kept apart, SL-T assigned per zone and conduit (not per asset, not
"residual"), tolerable risk explicit, documentation and approval present, terms as defined in `3.1` and `3.2`. A source
that fails a check can still give examples for the steps it gets right; `references/cases.md` records the checks of
the cases examined so far.
