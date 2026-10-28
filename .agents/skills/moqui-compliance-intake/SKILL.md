---
name: moqui-compliance-intake
description: Take in what a user uploads for a compliance project - a bill of materials (EPLAN or other CSV export), electrical and network drawings, datasheets, certificates - and turn it into Moqui records the norm requirements can be derived from - Product records classified by the vocabulary hooks (ProductCategory, ProductFeature, ProductFeatureGroup, DevicePurpose), function levels for the safety, protective, stop and emergency functions and for security zones and conduits, and, for an installed plant, the Asset (serial number), Device and PhysicalDevice (vendor, model, firmware) of every unit and DeviceGroup records for zones, conduits and functions - asking the user, as the norms require, for every fact, function grouping and document that cannot be read from the files, and stopping instead of guessing. Use this skill whenever a bill of materials, a machine, a standard product (a boiler, a machine type) or a customer's plant has to be loaded for a CRA, machinery, functional safety or IEC 62443 assessment, or documents for the technical file have to be requested.
---

# moqui-compliance-intake: from the user's files to classified records

The intake decides what every later step can find: a product that is not classified gets no requirement, a function
that no level groups gets its requirements as "conditional", an installed device without its firmware version cannot
be checked against advisories. The norms decide what to ask; the files answer what they can; the user answers the rest.
**When a fact cannot be read from the files, stop and ask: never fill it with an assumption.**

Next steps: `moqui-norm-requirements` (plan and project), `moqui-ot-risk-assessment` (IEC 62443-3-2),
`moqui-compliance-report`.

## 1. Which case: a product type or an installation

Ask first, the two are modelled differently:

| | Standard product (type) | Installation of one customer |
| --- | --- | --- |
| Example | a boiler model, a machine type sold in series | a plant section, a machine as installed at a site |
| Who | manufacturer (CRA `ART3.pt13`; Machinery Regulation) | asset owner, integrator (IEC 62443-3-2 SUC `4.2.1.1`) |
| Uses | intended purpose and reasonably foreseeable use and misuse, standardised (CRA `ART3.pt23`-`pt25`; machinery `ANXIII.A.pth`, `pti`): e.g. the boiler connected to a home-automation system | the real scenarios, network and organisation of that customer |
| Records | Product, ProductAssoc (bill), hooks, function products | the same products, plus Asset (serial number), Device + PhysicalDevice (vendor, model, firmware), DeviceGroup |
| Zones, conduits, functions | function products (`CmpPtFunction` with `purposeEnumId`) of the type, standard for every unit | DeviceGroup (a DeviceGroup is a Device: `Device.purposeEnumId` is the hook, `DeviceGroupMember.purposeEnumId` the role) |

A product type never needs Device records. An installation always needs the product of each device too: requirements
of the type come from the product, the firmware and the serial number from the device.

**Why zones, conduits and functions are neither features nor categories.** A ProductFeature is a property of one
product (supply up to 1000 V, SIL 3, network connected); a ProductCategory classifies what a product is, shared by all
projects (its rollups are the vocabulary hierarchy). A zone or a function is a set of members with attributes of its
own (boundary, access points, SL-T; the safety integrity of the function): that is a record with members, i.e. a
function product with `ProductAssoc` `CmpPatFunctionMember` (type) or a DeviceGroup with DeviceGroupMember
(installation). Its classification is its purpose (`CmpDepSecurityZone`, `CmpDepSecConduit`, `CmpDepGuardInterlocking`,
...); features can be applied to it (the SL-T of a zone).

## 2. Read the files (in the sandbox, never whole into the conversation)

Files of any size go to the **compliance inbox** (a folder the user fills outside the chat), not into the conversation:
`get_inbox_files` lists it, `attach_content` (sourcePath, productId | deviceId | workEffortId) copies a file into the
content store and records it as ProductContent, DeviceContent or WorkEffortContent. The analysis sandbox mounts the
inbox and the store read only (`INBOX_DIR`, `CONTENT_DIR`) and has no network: its scripts read files
(`eplan_bom.py`, `pdf_pages.py`); the scripts that talk to Moqui (`hook_candidates.py`, `load_intake.py`,
`norm_documents.py`) run where Moqui is reachable, or the agent calls the MCP tools directly.

- **Any large PDF**: `scripts/pdf_pages.py info|grep|text|image FILE ...` reads it page by page: grep for what matters,
  print the few pages that hold it, render a page to look at it.

- **Bill of materials**: `scripts/eplan_bom.py <file.csv> --json bom.json` (EPLAN parts list, UTF-16, multilingual
  descriptions): one row per article with quantity and device tags. Other formats: convert to the same JSON.
- **Electrical drawings** (PDF): `pdftotext -layout`, then grep for communication (Ethernet, PROFINET, Modbus,
  EIA-485, RJ45, IP addresses), safety devices (safety switch, emergency stop, STO, interlock), functions. Render the
  pages that matter (`pdftoppm -r 80 -f N -l N`) and look at them: wiring of a port or of STO is in the picture, not
  in the text. Cross references like `/122.7` are **sheet** numbers, not PDF pages: find the page by its sheet label.
- **Network drawings**: render and read them; check the title block. **Confirm the drawing belongs to this project**
  (customer, plant, revision): a drawing of another plant is at most a reference architecture, and the report says so.
- **Order codes**: read what the code is before naming it (a SCALANCE XB208 6GK5208-0BA00-2AB2 is a managed switch;
  "+B056" of an ABB drive is the enclosure class, not a fieldbus). Interfaces bought as options (a fieldbus adapter in
  a drive slot) are often missing from the bill: ask.
- **Market and customer**: the title block and the electrical data (UL 508A, 460 V/60 Hz) tell where the machine goes;
  CRA and Machinery Regulation apply to products made available on the Union market (`ART3.pt22`). Ask when unclear.

## 3. Classify (hooks)

1. For each article decide what it is from the order code and the datasheet, and write it in the norms' words in the
   field `kind` of `bom.json` ("programmable logic controller", "managed network switch", "frequency converter",
   "interlocking device"). Vendor names (SIMATIC, SCALANCE, ACH580) do not occur in the norms: searching with them gives
   wrong hooks.
2. `scripts/hook_candidates.py bom.json --out hooks.json`: candidate hooks per article from the search index.
3. Accept a hook only after reading the norm item it comes from (`get_norm_tree`) and checking the datasheet. Set
   `digital` (software, firmware, data or network interface: CRA `ART3.pt1`, `ART2.1`) on every product.
4. **A concept the norms name but the vocabulary lacks** (e.g. HMI, power drive system): do not force the nearest
   hook. Record it as a vocabulary gap for `moqui-norm-hooks` and ask the user whether to proceed without it.
5. Passive material (terminals, ducts, fuses) stays in the bill unclassified; the plan reports it as unclassified,
   which is expected.

## 4. Functions, zones and conduits

The norms name the functions; the bill shows the components; the drawings show how they are wired.
- For every function a norm item names for this kind of product (safety function, guard interlocking, emergency stop,
  stop functions, overtemperature or overpressure protection ...): find the group of components that realises it
  (input, logic, output) in the drawings. If no level of the bill groups them, create it: a function product with its
  members and roles (type) or a DeviceGroup (installation). If the wiring does not show it (e.g. a safety switch read by
  a standard PLC input: is the hazard also removed by hard wiring?), **ask**.
- Zones and conduits come from the network drawings (IEC 62443-3-2 ZCR 3): one zone per group of assets sharing
  security requirements, one conduit per channel between zones, with the separation rules 3.2-3.6. Products that
  communicate and are in no zone are reported by the plan as `missingFunction` security zone.
- `plan_norm_project` after loading lists the functions the norms still expect (`missingFunction` gaps): each one is a
  question for the user, never a level created without the members.

## 5. Load

Write `intake.json` (format: `references/intake-format.md`) and run:

```sh
python3 -I scripts/load_intake.py intake.json --check   # the open questions; nothing is written
python3 -I scripts/load_intake.py intake.json           # checks again, then loads
```

The checks block the load when: the case (type or installation) is not stated, a product has digital elements but no
category, a hook id does not exist, a function has no members or a member has no role, an asset has no serial number,
an installed digital device has no firmware version, a group member is not a device. Each failure is printed as the
question to ask. Ids: a short project prefix (`FMQ_`, `IMG_`) keeps test and customer records apart.

## 6. Documents to request

Ask only for what the norms list, citing the item: `scripts/norm_documents.py machinery cra cra-user iec62443`
prints the lists (Machinery Regulation Annex IV part A, CRA Annex VII and Annex II, IEC 62443-3-2 ZCR 5.13 and 6.1)
with their points. For each purchased digital component ask for its datasheet, EU declaration of conformity, security
advisories / support period (the manufacturer's due diligence, CRA `ART13.5`) and the installed firmware version.
Files are attached to the product (`ProductContent`) or device (`DeviceContent`); large files go through the shared
upload storage, not through the conversation.

## Lessons (from real cases; add to them after each project)

- A network drawing in the folder was of another customer's plant: check title blocks before using a drawing.
- A managed switch was called unmanaged from memory: read the order code.
- A fieldbus adapter in a drive's option slot was not in the bill and the EIA-485 port was not wired: the drawing
  page, not the bill, showed the real interface.
- Searching hooks with vendor descriptions returned a forensics tool for a PLC: write the `kind` first.
