# Cyber security risk assessment - {SUC name}

| | |
|---|---|
| Classification | {information security classification of this document} |
| System under consideration | {SUC name, root product / asset id} |
| Norm | IEC 62443-3-2 (ZCR 1 to ZCR 5), items cited as `IEC-62443-3-2-2020-EN` item ids |
| Status | draft / for approval / approved by {name, title, date} (ZCR 7) |

## Sessions

| Date | Participants (name, title) | Zones / conduits covered |
|---|---|---|
| {yyyy-mm-dd} | {name, title}; {name, title} | {Z1, C1} |

## Inputs archived with this assessment

| Input | Location | Date |
|---|---|---|
| System architecture drawings | {link} | {date} |
| Process hazard analysis / functional safety assessment | {link} | {date} |
| Vulnerability assessment | {link} | {date} |
| Threat information sources | {link to the threat environment page} | {date} |

## 1. System under consideration (ZCR 1)

{Perimeter in one paragraph.}

| Access point | Kind (logical / physical) | Zone or conduit |
|---|---|---|
| {remote access gateway} | logical | {C2} |

## 2. Initial risk (ZCR 2, ZCR 4)

Worst case, without countermeasures. Tolerable risk: {the organisation's criterion, matrix reference}.

| Function of the SUC | Worst-case impact | Initial risk | Above tolerable? |
|---|---|---|---|
| {mission-critical function} | {safety / production / environment ...} | {rating} | yes / no |

{If no initial risk is above tolerable risk, the assessment ends here: say so.}

## 3. Zones and conduits (ZCR 3)

| Zone / conduit | Grouping rule that produced it (ZCR 3.1-3.6) | Safety related |
|---|---|---|
| {Z1} | {3.3 safety-related assets} | yes |

## 4. Detailed assessment of {zone or conduit} (ZCR 5)

SL-T: {value or vector per FR}, method: {Annex A / risk matrix / risk difference} (ZCR 5.6).

| Id | Threat source and capability | Vector | Assets | Vulnerabilities | Consequence (worst case) | Impact | Unmitigated likelihood | Unmitigated risk | Decision | Existing countermeasures | Mitigated likelihood / impact | Residual risk | Decision | Additional countermeasures (norm item) | Evidence (ATT&CK, CVE) |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| T1 | {who, skill level} | {how} | {which} | {known, incl. access points} | {safety / finance / interruption / environment} | {rating} | {rating, cyber countermeasures removed} | {rating} | mitigate / accept / transfer | {list} | {ratings} | {rating} | accept / transfer / mitigate | {SR 5.1 `IEC-62443-3-3-2013-EN` 9.3} | {T1003.001} |

{Repeat section 4 for every zone and conduit whose initial risk is above tolerable risk.}

## 5. Results and open decisions (ZCR 5.13)

{Residual risks above tolerable risk, who decides, by when. Requirements created in the norm project: link to the
project status page.}
