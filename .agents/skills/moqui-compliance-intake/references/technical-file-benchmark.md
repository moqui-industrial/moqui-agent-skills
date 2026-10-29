# Technical File & Machine Documentation Benchmark (Festo InfoPortal Pattern)

Every machine or plant loaded into Moqui should be guided toward a complete, multi-level **Technical File (*Fascicolo Tecnico*) and Machine Portal** structured into four pillars — modelled on the industrial mechatronics documentation standard (e.g. Festo Didactic InfoPortal MPS 405-1) and required by:
- **Machinery Regulation (EU) 2023/1230** (`ANXIV.A` technical documentation, `ANXIII` EHSR),
- **Cyber Resilience Act (EU) 2024/2847** (`ANXVII` technical documentation, `ANXII` user instructions, `ART13.5` third-party component due diligence),
- **IEC 60204-1:2016** (`17` technical documentation of electrical equipment),
- **IEC 62061:2021** (`4` / `5` / `6` safety-related control system specification and design documentation),
- **IEC 62443-3-2:2020** (`4.6.14.1` ZCR 5.13 assessment archive, `4.7.2.1` ZCR 6.1 CRS).

When a user's initial documentation is incomplete (for example, a flat ERP BOM or a single wiring PDF without functional groupings or network topology), use this benchmark to show what is missing and help the user construct each level step by step.

---

## 1. The Four-Pillar Machine Documentation Structure

For the root machine/system (`SUC`) and for each major station or sub-assembly in the hierarchy:

| Pillar | What it contains | Moqui records |
| --- | --- | --- |
| **1. Overview & Intended Purpose** | Functional description, process workflow, technical specifications (dimensions, supply voltage, pressure, operating environment), intended use and reasonably foreseeable misuse (`EU-REG-2023-1230` `ANXIII.A.pth`/`pti`, `EU-REG-2024-2847` `ART3.pt23`-`pt25`), system boundary and access points (`IEC-62443-3-2-2020-EN` `4.2.1.1`). | `Product.description` / `comments`, root wiki page (`Overview.md`), system manual attached as `ProductContent`. |
| **2. Elements (Hierarchical BOM, Functions & Zones)** | Multi-level engineering bill of materials (`System -> Station/Assembly -> Sub-Module -> Component`) with order codes, quantities, and schematic device tags (`-K1`, `-S1`, `-BG1`), plus explicit functional groupings (`CmpPtFunction` / `DeviceGroup`) for safety/protective functions and OT security zones/conduits. | `Product`, `ProductAssoc` (`PatEngBom`, `CmpPatFunction`, `CmpPatFunctionMember`), `ProductCategoryMember`, `ProductFeatureAppl`, and for installations `Asset`, `Device`, `PhysicalDevice`, `DeviceGroup`, `DeviceGroupMember`. |
| **3. Software & Digital Elements** | PLC projects (e.g. TIA Portal `.zap15`), robot controller programs, HMI projects, edge/MES software stacks (`docker-compose`, OPC UA / MQTT configurations), firmware versions of every programmable or network-connected device, and SBOM / vulnerability advisories (`EU-REG-2024-2847` `ANXVII`, `ANXII`). | `ProductContent` (standard catalog software/firmware baseline) or `DeviceContent` (site-specific / customer-commissioned program and configuration on an installed `Device`), `PhysicalDevice.firmwareVersion`. |
| **4. Documentation, Schematics & Compliance Reports** | Operating & installation manuals, electrical/pneumatic circuit diagrams (EPLAN PDFs), network topology diagrams (VLAN/IP plan, switches, routers, Wi-Fi, MES links), component datasheets, EU declarations of conformity, and the generated Markdown compliance reports (Machinery/Safety analysis, IEC 62443-3-2 Risk Assessment, CRS, CRA assessment). | `ProductContent` / `DeviceContent` / `WorkEffortContent` via `attach_content`, and versioned Markdown/FreeMarker pages in the machine's Wiki space / documentation site. |

---

## 2. Multi-Level BOM Hierarchy vs Flat Customer BOMs

Customer bills of materials exported from ERP or CAD are almost always **flat** or grouped only by mechanical assembly. Before generating norm requirements, guide the user to structure the hierarchy into four clear layers:

1. **Level 0 — System / Line / Machine (`root`)**: the complete machine or production cell (e.g. complete mechatronics line).
2. **Level 1 — Stations / Major Assemblies**: autonomous stations or major subsystems (e.g. Distributing Station, Joining Station, Robot Assembly Cell, Measuring Station, Sorting Station, Supervisory MES/Network node).
3. **Level 2 — Functional Sub-Modules & Normative Function Groupings**:
   - **Physical sub-modules**: reusable mechanical/electrical assemblies (e.g. conveyor module, pick-and-place module, stacking magazine, IO-Link master interface box, control console).
   - **Safety & Protective Function levels (`CmpPtFunction` / `DeviceGroup`)**: e.g. safety door interlock with guard switch + safety relay/PLC + actuator cut-off (`CmpDepGuardInterlocking`), emergency stop chain across operator consoles (`CmpDepEmergencyStop`), safe torque off / robot stopping function (`CmpDepSafetyFunction`).
   - **OT Security Zones & Conduits (`CmpDepSecurityZone`, `CmpDepSecConduit`)**: e.g. Supervisory/MES Zone, Station Control PLC Zone, Robot Cell Safety Zone, Wireless/Engineering Access Conduit, Industrial Ethernet Backbone Conduit.
4. **Level 3 — Components (Digital & Passive)**:
   - **Digital / active components** (`"digital": true`): PLCs, robot controllers, teaching pendants, HMIs, managed/unmanaged switches, Wi-Fi routers, IO-Link gateways, RFID interfaces and read/write heads, smart sensors, drives, industrial PCs.
   - **Safety / electromechanical components**: safety interlock switches, emergency-stop pushbuttons, power supplies, motor controllers, valve terminals.
   - **Passive components** (`"passive": true`): profiles, mounting plates, pneumatic cylinders, one-way flow control valves, mechanical grippers, cables, terminal blocks.

---

## 3. `ProductContent` vs `DeviceContent`: Where Attachments Belong

Always distinguish between documents of the **standard product type** (`ProductContent`) and documents of a **specific physical installation** (`DeviceContent`):

| Attachment Type | Attach as `ProductContent` (`productId`) | Attach as `DeviceContent` (`deviceId`) |
| --- | --- | --- |
| **Operating, assembly & maintenance manuals** | Standard manufacturer manual for the machine, station, module or component. | Site-specific operating procedures or local modifications for a specific serial unit. |
| **Electrical, pneumatic & network drawings** | Standard circuit diagram (`CircuitDiagrams.pdf`) and reference network topology of the machine/station model. | As-built redline drawings, customer site IP/VLAN allocation table, site patch-panel schedule. |
| **Datasheets & certificates** | Component datasheet, EU Declaration of Conformity, UL/CE/TÜV certificate of the catalog product. | Calibration certificate, dielectric/continuity test protocol (`IEC-60204-1` `18`), or FAT/SAT sign-off of a specific serial number (`Asset.serialNumber`). |
| **PLC, Robot, HMI & Edge Software** | Standard baseline program released by the machine builder for that model/station (e.g. standard TIA Portal project or robot program archive for the catalog station). | Customer-customized PLC/robot project, commissioned parameter backup, or site-specific `docker-compose` / firewall configuration running on that installed `Device`. |
| **Compliance & Risk Assessment Reports (`.md`)** | Type-level Machinery Regulation / CRA / IEC 62443-4-2 assessment and standard CRS template of the machine model. | Plant-specific IEC 62443-3-2 risk assessment, ZCR 6 CRS, and ZCR 7 asset-owner approval for the installed SUC (`WorkEffortContent` on the project and/or `DeviceContent` on `rootDeviceId`). |

---

## 4. The Per-Machine Technical Documentation Portal (`moqui-site` Pattern)

For each machine model or installed plant, generate a standalone, static-hosted **Machine Technical Portal** based on the official `moqui-site` template:

1. **Static Architecture (`moqui-site`)**:
   - `index.html`: Hero banner, mechatronic station cards, compliance statistics (requirements, milestones, safety integrity levels, CRA scope).
   - `/docs/`: Markdown rendering engine (`marked.umd.min.js`, `dompurify.min.js`, `highlight.min.js`) consuming `/docs/manifest.json`.
   - `/docs/manifest.json`: Defines dedicated wiki spaces (`overview`, `stations`, `safety`, `cybersecurity`, `network`, `datasheets`).
   - `/docs/md/<space>/index.md`: Modular Markdown documents for each space, keeping documents human-readable and versioned in Git.
   - `serve.py`: Threading HTTP server with 404 fallback for instant local preview (`python3 serve.py`).

2. **Integration with Moqui Compliance**:
   - Every report rendered in the portal is simultaneously attached in Moqui as `ProductContent` (type level), `DeviceContent` (plant level), and `WorkEffortContent` (norm project level).
   - The navigation header links directly to the Moqui Compliance application (`/vapps/compliance`) for full traceability down to individual requirements, tasks, and audit logs.
