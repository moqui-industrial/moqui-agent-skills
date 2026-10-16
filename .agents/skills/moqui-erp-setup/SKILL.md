---
name: moqui-erp-setup
description: Orchestrates setting up a company in Moqui/Mantle end to end — company survey, organizations and divisions, contacts, accounting configuration and fiscal periods, people and users, warehouses, products, forms, extensions such as budgets — by coordinating the specialist Moqui skills and keeping session state on disk. Use this skill whenever the user wants to configure, set up, onboard or migrate a company, plant, division or warehouse into Moqui, or asks for "the setup data" of an organization, and as the entry point that decides which other Moqui skill to use.
---

# moqui-erp-setup: company setup orchestrator

This is the parent skill. It does not replace the specialists; it decides the order, asks the questions, keeps the session on disk and calls the right skill at each step.

| Skill | Used for |
| --- | --- |
| `moqui-model` | What exists: entities, masters, enums, statuses, roles, structures. Look up every name and value there. |
| `moqui-data` | Writing and validating the data files of every step. |
| `moqui-product` | Products, BOMs, features, categories, assets and devices. |
| `moqui-agreement` | Contracts, framework agreements over a job order, terms, agreement prices, service levels. |
| `moqui-instance` | Application instances: provisioning, lifecycle, per-customer SaaS, scaling built on top. |
| `moqui-dbform` | Questionnaires and extra fields as data. |
| `moqui-datadocument` | Search indexes and analytics documents pushed to OpenSearch. |
| `moqui-systemmessage` | Integrations with partners, banks, carriers and other systems. |
| `moqui-actions` | Only when a step needs a service that does not exist yet. |

## Dispatch: choosing the mechanism

This skill is where a need is routed to the right Moqui mechanism. Before writing anything, read `references/dispatch.md`. The decisions that matter most:

- **Exchange outside Moqui.** A machine signal is a DeviceRequest. An agent acting on its own talks through A2A. A business document that must survive outages and be auditable is a SystemMessage. A synchronous question with nothing to keep is a service call. Search and analytics feeds are DataFeeds.
- **Demand and change.** Someone asks: Request. The organization needs: Requirement. A commitment with an external party: Order. Work is a WorkEffort that fulfils one of these, not a starting point.
- **Work shape.** Projects as roots, tasks as children, milestones attached by association, maintenance through AssetMaintenance, production through production-run work efforts.
- **Parties.** Persons, organizations and automated agents are all parties, and their PartyRoles switch Mantle's flows on.
- **Contracts.** An Agreement is the umbrella of a job order and the source of payment terms, agreement prices and service thresholds.
- **Facts.** Measurement for observations, AssetDetail and AcctgTrans as ledgers, the audit log for field history.

## Source of truth

The setup is a set of data files, reviewed and loaded in order. They are the digital twin of the company's configuration: they can be reloaded into an empty database and reviewed line by line. Do not configure by writing directly into a database. If existing data must be imported, convert it into data files first and continue from those.

## Session

Every setup lives in a session directory so it can be resumed. Run from the root of the project you are working in; sessions go in its `codegen/sessions/`, apart from the skills:

```bash
python3 .agents/skills/moqui-erp-setup/scripts/init_session.py codegen/sessions acme
```

This creates `session.json` (step status), `survey-answers/`, `seed-data/`, `notes/` and `exports/`, or prints the status of an existing session. Update the step status in `session.json` as you go, and write in `notes/decisions.md` every choice that is not obvious from the data, with its reason.

## Steps

The order follows Mantle's own setup files: GL account templates (`ZaaGlAccountsInstallData`), then the organization (`ZbaOrganizationDemoData`), then products and facilities (`ZcaProductDemoData`). Write one data file per step in `seed-data/`, prefixed so that file-name order is load order (`A10_Organizations.xml`, `A20_Contacts.xml`...). Validate each file with `moqui-data`'s `check_data.py` before moving on.

1. **Survey.** Ask the questions in `references/company-survey.yaml`; save the answers in `survey-answers/company.yaml`. Do not invent missing answers: ask, or record the gap in the notes.
2. **Reference data.** Enumerations, status flows or role types the company needs and Mantle does not have. Check `moqui-model` first; most already exist.
3. **Organizations.** Main company and divisions: `Party` with `organization` and role `OrgInternal`; divisions roll up with a `PartyRelationship` of type `PrtOrgRollup`. `OrgInternal` is what makes Mantle treat a party as part of the company (purchase vs sales shipments, receivables vs payables, GL posting); never omit it.
4. **Contacts.** `ContactMech` with `PostalAddress` or `TelecomNumber`, linked by `PartyContactMech` with a purpose (`PostalPrimary`, `PostalBilling`, `PostalShippingOrigin`...).
5. **Accounting.** Call `mantle.ledger.LedgerServices.initPartyAccountingConfiguration` from the `DefaultSettings` template with the base currency and `startYear`. It copies the configuration, the GL accounts and the item type to GL account mappings, and creates fiscal year, quarter and month periods. Budgets and anything tied to a fiscal year need this step first. If the company needs its own chart of accounts or new item types, adapt them here (see `item-types.md` in `moqui-model`): every item type that is invoiced needs an `ItemTypeGlAccount`.
6. **People and agents.** `Party` with `person`, role `Employee`, a `PrtEmployee` relationship to the organization, a `UserAccount`, and the user groups that give application access. AI agents that will act in the system (the assistant, the executor, partner agents) are set up here too, as `PtyAutomatedAgent` parties with their own UserAccount and groups; `references/AgentPartyExample.xml` shows one, and it passes the data checker.
7. **Facilities.** `Facility` with `locations` and contacts.
8. **Products.** With `moqui-product`: feature types and units first, then the category tree with its feature groups, then products with their features, BOMs and `prices`, then initial inventory as `Asset` with an `AssetDetail` (bulk or serialized) and fixed assets.
9. **Forms.** Questionnaires and extra fields with `moqui-dbform`.
10. **Extensions.** Positions, budgets, rates, jobs, agreements with customers and suppliers (`moqui-agreement`), application instances (`moqui-instance`): anything the survey asked for, each in its own file. Analytics documents and their feeds go here too, with `moqui-datadocument`, and integrations with external systems with `moqui-systemmessage`.
11. **Load and verify.** Load the files into a scratch database in order, then read back the key records (the organization with its roles, the fiscal periods, a product with its price, a user that can log in) and record the result in `notes/`.

`references/ExampleSetupData.xml` shows steps 3 to 8 for a fictional company in Parma, in the same style as Mantle. It passes the data checker; its only warning is the nested `ContactMech`, which is the same pattern Mantle uses.

## After the setup

Once the company runs, changes to its configuration and to business objects (agreements, budgets, production estimates, assets, products) should enter as Requests or Requirements and be fulfilled by work efforts under a project, not as direct edits; see the section on requests and requirements in `moqui-model`. A setup session can open such a project itself, so later adjustments are traced from the start.

## Rules

- Ids are stable and readable, with the company prefix from the survey; user-facing codes go in `pseudoId`.
- Prefer a setup service, called from the data file, over writing its rows by hand (step 5).
- Every value of `*EnumId`, `statusId` and `roleTypeId` must exist or be defined in an earlier file.
- Demo data from Mantle is an example of style, never a source of ids or values for a real company.
