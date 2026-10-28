# Threat intelligence - {actor or campaign}, {source}, {date}

Source: {publisher, title, URL, publication date}. Read in full on {date}. Feeds ZCR 5.1 (threats) and ZCR 6.6
(threat environment) of {SUC / CRS link}.

## Key points

- {sector, country, period}
- {IT only / OT reached}
- {impact, what limited it}

## Threat source (IEC 62443-3-2 4.6.2.2)

| Element | From the report | Unknown to the report |
|---|---|---|
| Source | {actor, attribution and its confidence} | |
| Capability | {resources, skills, motivation; Annex A level it matches} | |
| Vectors | {per attack step} | {initial access, persistence ...} |
| Affected assets | {hosts, services, OT components} | |

## Attack steps

| Step | What the report says | Technique (evidence label) | Foundational requirement and SR countering it |
|---|---|---|---|
| {credential access} | {attempted LSASS dump} | T1003.001 | FR 1 / FR 2: SR 1.1, SR 1.3, SR 2.1 |

## Relevance to our SUC

{Which zones or conduits expose the same assets or vectors; which threats of the risk assessment this updates.}

## Indicators

{Hashes, names, network indicators as published; not interpreted.}
