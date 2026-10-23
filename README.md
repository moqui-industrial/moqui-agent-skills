# Moqui agent skills

Skills that teach a coding agent (Codex, Claude Code or similar) to read, write and validate Moqui/Mantle artifacts from the real sources. Each folder under `.agents/skills/` is one skill (the `.agents/skills/<name>/SKILL.md` layout used by `moqui/mr-moqui` and `moqui/moqui-plc`): `SKILL.md`, generated `references/`, `scripts/` (generators and validators), `assets/` (validated examples) and `agents/openai.yaml` for Codex.

| Skill | Purpose |
| --- | --- |
| `moqui-erp-setup` | Orchestrator: company setup sessions, step order, and the dispatch guide (which mechanism for which need) |
| `moqui-model` | The data model: entities, views, masters, structures, enums, statuses, roles, item types and GL mapping, work efforts, requests and requirements, party roles, agents as parties, DDD reading |
| `moqui-actions` | xml-actions language, runtime contract, SECA/EECA index, profile for generated code, artifact and XSD validators |
| `moqui-screen-xml` | XML screens, transitions, forms, reports and DbForm screens, checked against the XSDs and the SimpleScreens conventions |
| `moqui-data` | entity-facade-xml data files, nesting, services in data, data as a program, data catalog, data validator |
| `moqui-product` | Products, services as products, BOMs, features, categories, assets, devices, as-built structure |
| `moqui-agreement` | Contracts, framework agreements over a job order, terms, agreement prices, service thresholds |
| `moqui-datadocument` | DataDocuments and DataFeeds for search, BI and change notifications; catalog of existing documents |
| `moqui-dbform` | Forms and surveys as data |
| `moqui-systemmessage` | Stateful integration with external systems |
| `moqui-instance` | Application instance provisioning and lifecycle, SaaS per subscriber, scaling on top |
| `moqui-bi-analysis` | Authorized DataDocument SQL analysis through Moqui MCP, Markdown tables and validated inline Chart.js blocks |
| `moqui-norm-loading` | Legislation and technical standards as Agreement items (article, paragraph, point), with references, tables and figures as text, verified against the source |
| `moqui-norm-hooks` | Categories, features with thresholds, device purposes and groups linked to the norm items that name them; repeatable check, hook suite, prepared hook query |
| `moqui-seed-reload` | Seed files into a test instance: backup, clean delete, ordered load, read-only SQL checks |

## Install

Copy the folders under `.agents/skills/` into the skills directory your agent reads (moqui-plc keeps its skills under `.agents/skills/`). The scripts need only Python 3; `ValidateXsd.java` needs a JDK (run with `java ValidateXsd.java`).

## Target framework

These skills generate seed data and artifacts for the current Java/Groovy `moqui-framework`. Support for `moqui/mr-moqui` (Rust, JavaScript scripts) is future work and will be added as separate skills or an explicit target option, not by changing the current output.

## Keep the references current

The `references/` files are generated from the component sources. After changing entities, seed data, services or ECAs, or adding a component, run:

```sh
./rebuild-references.sh /path/to/moqui-framework
```

## Status

Built from moqui-framework (llm-client branch), moqui-runtime, mantle-udm, mantle-usl, SimpleScreens, MarbleERP, PopCommerce, HiveMind, moqui-sftp, moqui-math and moqui-device as of 2026-10-04. Validators are calibrated on all service and data files of those components; every example in `assets/` and `references/` passes them. Nothing has yet been loaded or executed in a running Moqui instance: that is the next test. Where the private moqui-industrial versions differ (for example `Device.assetId`), the skills say so.
