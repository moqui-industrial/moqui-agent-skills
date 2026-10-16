---
name: moqui-model
description: The Moqui / Mantle data model as a searchable index — entities, view-entities, fields, relationships, enumerations, status items, status flows, role types and recurring data patterns from moqui-framework, mantle-udm, mantle-usl, moqui-math and moqui-device. Use this skill whenever a task touches Moqui business data — writing a service, screen, entity-find, query or SQL against a Moqui database, resolving what an ERP concept (order, budget, project, asset, party, position, request, invoice) is called in Moqui, or picking the right enumId, statusId or roleTypeId — even if the user only names the business concept and not the entity.
---

# moqui-model: what exists in the Moqui data model

This skill answers one question: **which concepts already exist, what are they called, and how are they related**. It does not explain how to program (see `moqui-actions`) or how to orchestrate services and screens.

## The one rule

**Never guess an entity name, field name, enumId, statusId or roleTypeId. Look it up first.** Names in Mantle are close to what you expect, but not equal (`Budget` has `description`, not `budgetName`; support requests are `requestTypeEnumId="RqtSupport"`; an asset on hold is `AstOnHold`). A guessed name compiles, then fails at runtime or silently matches nothing.

## Where to look

All files are generated from the sources by `scripts/build_model_index.py` and are made for `grep`: one line per item. The current index covers the framework (llm-client branch), moqui-runtime, mantle-udm, mantle-usl, SimpleScreens, MarbleERP, PopCommerce, HiveMind, moqui-sftp, moqui-math and moqui-device; the application components define no entities of their own, but their seed data is included. View lines show members joined through a relationship as `rel ALIAS:relationship`.

| File | Content | Typical grep |
| --- | --- | --- |
| `references/entities/INDEX.md` | Package groups with entity and view counts | read once to orient |
| `references/entities/<group>.md` | One line per entity (E) or view-entity (V): source, PK, fields with types, relationships; for views the members (`?` = optional join), alias-all and aliases | `grep -h '^- E mantle.other.budget.Budget ' references/entities/*.md` |
| `references/enums.md` | Enumerations grouped by `enumTypeId` | `grep -n -i 'support' references/enums.md` |
| `references/status.md` | Status items by `statusTypeId`, then allowed `StatusFlowTransition` moves | `grep 'AstAvailable ->' references/status.md` |
| `references/roles.md` | Role types | `grep -i manager references/roles.md` |
| `references/patterns.md` | Recurring field-level patterns with counts and examples | read when designing a query or a write |
| `references/masters.md` | Entity masters: Moqui's own declared aggregates (36), nested relationship trees | read first when a request is about a whole business document (order, shipment, invoice, party, product) |
| `references/item-types.md` | Every `ItemType` value with parent, usage groups (sales, purchase, adjust, product) and its GL accounts | read before creating any order, invoice, return, budget or payroll line |
| `references/structures.md` | How entities compose: aggregates, self hierarchies, hubs, group/member, assoc, enum hierarchies | read before any write that touches more than one entity |

Search by meaning, then confirm by name: grep the business word in `enums.md`, `roles.md` and in entity lines (field names often carry the concept), then open the exact entity line.

## Reading an entity line

```
- E mantle.other.budget.Budget | src: mantle-udm | pk: budgetId | fields: budgetTypeEnumId:id, timePeriodId:id, statusId:id, ... | rels: one>Enumeration[BudgetType], one>TimePeriod, one>StatusItem[Budget]
```

- `rels: one>Enumeration[BudgetType]` means `budgetTypeEnumId` points to an `Enumeration` with `enumTypeId="BudgetType"`: the allowed values are under `## BudgetType` in `enums.md`.
- `one>StatusItem[Budget]` means the status values are under `### Budget` in `status.md`, and the allowed moves under the status flows.
- A field that is in the PK is not repeated in `fields`.

View-entities live mostly in mantle-usl. Prefer an existing view over writing joins by hand: `PartyDetailAndRole` already joins Party, PartyRole, Person and Organization. A view line lists `alias-all` members: every field of that member is available on the view.

## Patterns that change how you write code

These come from `references/patterns.md`, computed over the whole model.

- **Status-bearing entities** (`statusId`, 55 entities: Asset, Budget, OrderHeader, WorkEffort, Request...). Never change `statusId` with a direct entity update. Use the owning service so that status-flow checks and SECAs run (for example `update#Asset` triggers the reservation handling when an asset leaves `AstAvailable`). Check the allowed move in `status.md` first.
- **Effective dating** (`fromDate` in the PK, usually with `thruDate`, 63 entities: party assignments, position fulfillments, employment...). Query them with `<date-filter/>`, and end a relationship by setting `thruDate`, not by deleting.
- **Typed by Enumeration** (`*TypeEnumId`, 208 entities). The value must exist in `enums.md` under the matching type.
- **Party in role** (`partyId` + `roleTypeId` on a business object: WorkEffortParty, RequestParty, BudgetParty...). Assigning a person to something means creating that association with the right role from `roles.md`.
- **Lines** (parent PK + `*SeqId`, 47 entities: OrderItem, BudgetItem...). Lines are created after the header, usually through a service that assigns the sequence.
- **pseudoId** (Party, Product, Facility, EmplPosition...). Users speak in pseudoIds or names (`ZICORP`), the database joins on technical ids (`ORG_ZIZI_CORP`). Resolve at runtime, never hard-code ids found while exploring.

## Masters: declared business documents

Moqui lets an entity declare a `<master>`: the root plus the relationships that belong to it, nested. Moqui and Mantle declare 36 of them, and they are the authoritative answer to "what is an order". `references/masters.md` resolves each one to entities, for example:

```
OrderHeader: parts -> OrderPart -> items -> OrderItem -> reservations, issuances, receipts, billings
                                -> parties -> OrderPartParty, contactMechs, terms
```

The same definition drives the master REST API (`/rest/m1/...`) and data export with dependents. When a master exists, follow it; when it does not, use the computed structures below.

## Structures: how concepts are composed

`references/structures.md` is computed from the relationships, not written by hand. Read it before writing anything that touches more than one entity.

- **Aggregates.** Multi-level compositions such as OrderHeader → OrderPart and OrderItem → OrderItemBilling, Budget → BudgetItem → BudgetItemDetail, Shipment → ShipmentItem → ShipmentItemSource. Create from the root down, through the root's services. A line can also point to a sibling level: an OrderItem belongs to an OrderPart of the same order through `orderPartSeqId`, even though its PK does not include it.
- **Self hierarchies** (`parent*Id` on the same entity): WorkEffort under WorkEffort (project, milestone, task), OrderPart under OrderPart, OrderItem under OrderItem, Facility under Facility, GlAccount under GlAccount.
- **Hubs**, similar to fact tables in a star schema: OrderItem, Payment, Asset, AssetIssuance, AcctgTrans, AssetDetail. They tie many business objects together; start from them to trace what happened to an item or to build an analytical query.
- **Group and member**: FacilityGroupMember, ProductCategoryMember, GlAccountCategoryMember, ProductStoreGroupMember and others. Membership usually has a validity period: add with a new row, end with `thruDate`.
- **Assoc**: typed links between instances of the same entity (ProductAssoc, WorkEffortAssoc, AgreementAssoc, RequestItemAssoc). The link type is an enumeration.
- **Enumeration hierarchies**: many enum values have a `parentEnumId`, shown as `(parent: X)` in `enums.md`. A child refines its parent, so code that filters on the parent value must also accept the children.

## Products and assets

Products, BOMs and other product associations, features, feature groups, categories, assets and their link to devices have their own skill, `moqui-product`, because they are where most technical knowledge of a manufacturing company lives.

## Item types and the accounting they drive

Every line of an order, invoice, return, budget or payroll record carries `itemTypeEnumId`, from one enumeration (`ItemType`, 171 values) organized in a hierarchy (`ItemProduct` under `ItemSales`, adjustments under `ItemInvAdjust`...). Two seed files give it meaning, and `references/item-types.md` combines them:

- `ItemTypeData.xml` puts each type in usage groups: `EngItemsSales` for outgoing lines, `EngItemsPurchase` for incoming lines, `EngItemsAdjust` for invoice adjustments, `EngItemsProduct` for product lines. Use a type only where its group allows it.
- `ZaaGlAccountsInstallData.xml` is the accounting template: 487 GL accounts and, through `ItemTypeGlAccount`, the account each item type posts to by direction (`O` outgoing, `I` incoming, `E` either). It belongs to the template organization `DefaultSettings` and is copied to a real company by `init#PartyAccountingConfiguration`, together with the defaults by GL account type, asset type, payment type and invoice type.

When an invoice item is posted, Mantle looks for the account by product first (product category, product, asset type) for product item types, then by the exact `itemTypeEnumId`. The parent type is not used as a fallback, so a new item type without its own `ItemTypeGlAccount` finds no account and the invoice cannot be posted correctly.

## Work efforts: the backbone of human work

`mantle.work.effort.WorkEffort` is one entity for every unit of planned or performed work, distinguished by `workEffortTypeEnumId`: `WetProject`, `WetMilestone`, `WetTask`, `WetEvent`, `WetRelease`, `WetComponent`, `WetTimeOff`, `WetAvailable`. Two self references organize them:

- **`rootWorkEffortId`** points every work effort of a project to the project itself. It is the aggregate key: "everything in project X" is one query on `rootWorkEffortId`, and the EECA `WorkEffortUpdateProject` rolls task time up to the root whenever a task with a root changes.
- **`parentWorkEffortId`** builds the breakdown: a task under a task, a sub-project under a project.

Milestones are not parents. A milestone is a work effort of type `WetMilestone` under the same root, and a task is attached to it with a `WorkEffortAssoc` of type `WeatMilestone` (what `create#Task` does with `milestoneWorkEffortId`). Other association types give the dependencies of a plan: `WeatDependsOn` (blocked by), `WeatIndependentOf`, `WeatDuplicates`, `WeatCausedBy`, all refinements of `WeatRelatesTo`.

Around the work effort: people in roles (`WorkEffortParty`, e.g. `Assignee`, `ProjectManager`), time (`TimeEntry`, rolled up as above), the requests that originated the work (`RequestWorkEffort`), assets, products, deliverables, notes and content. A work effort can also choose its own state machine with `statusFlowId`. Work efforts are usually the fulfilment of a Request or a Requirement (next section).

HiveMind is a project management application built on exactly this structure: projects, milestones and tasks are work efforts under one root, requests are linked to them, and its dashboards ("my tasks", "my milestones", "my projects", "my requests") list the work efforts and requests of the current user. When a human workflow must be organized (a project, a commissioning, a maintenance campaign, an approval chain), model it as work efforts under a root before inventing new entities.

## Party roles switch the flows on

A party is only a subject; what it is to the business is its `PartyRole`, and Mantle's services read those roles to decide what to do. `OrgInternal` alone is checked in 13 service files: on an order it tells whether the customer side is the company itself (a purchase), which sets the ship-to facility and makes the shipments created from the order `ShpTpPurchase` instead of `ShpTpSales`; on invoices and payments it tells which side is internal, hence receivable or payable, incoming or outgoing; and it decides whether an invoice is posted to the general ledger at all (`InvoiceAutoPostServices` looks for an `OrgInternal` party with accounting preferences). `Customer`, `CustomerBillTo`, `Supplier`, `Vendor`, `Employee`, `Carrier` and the others drive selections, defaults and screens in the same way. A party without the right role is a party the flows do not see.

- Give every party its roles when it is created: in setup data with nested `roles`, in services with `mantle.party.PartyServices.ensure#PartyRole` (it creates the role only if missing).
- The `*Party` association entities (`OrderPartParty`, `WorkEffortParty`, `RequestParty`, `BudgetParty`...) store a role for that object, but they have no foreign key to `PartyRole`: adding a party to an object does not give it the role. Ensure the role as well.
- Relations between parties are `PartyRelationship` records with a type and a role on each side: `PrtEmployee` (person to employer), `PrtOrgRollup` (division to parent), `PrtAgent` (acts for), `PrtRepresentative`, `PrtMember`.
- Role types are in `roles.md`; check there before inventing one.

## Automated agents as parties

Mantle already has a party type for non-human actors: `PtyAutomatedAgent`, and a role `Agent`. An AI agent that works with Moqui, inside (the assistant, the executor) or outside (a partner's agent calling through A2A), should be a party, so that its work is attributed and governed like anyone else's:

- **Identity.** A `Party` with `partyTypeEnumId="PtyAutomatedAgent"`, a readable `pseudoId`, and a `UserAccount` linked by `partyId`. Moqui's A2A contexts and tasks are recorded per `userId`, and authorization applies to that user, so the agent's permissions are exactly its user groups.
- **From the Agent Card.** The A2A Agent Card describes the agent: name, description, provider organization and URL, endpoint URL, version, skills, security schemes. A reasonable mapping, which is a convention and not defined by Mantle: name in `UserAccount.userFullName`; the endpoint as a `ContactMech` of type `CmtWebAddress` linked with `PartyContactMech`; the provider as an `Organization` party linked with a `PartyRelationship` of type `PrtAgent` (the agent acts for the provider); the card itself stored as `PartyContent`, with a content type you add in seed data; version and identifiers in `PartyIdentification` if they must be searchable. Skills of the card stay in the stored card; what the agent may actually do is decided by its user groups, not by what the card claims.
- **Roles.** `Agent`, plus the business roles it plays (`Supplier`, `Customer`, `Carrier`...), exactly as for a company or a person, because the flows read roles, not party types.
- **Work.** An agent files Requests on behalf of a user (the user in a requester role, the agent in its own role), and is the assignee (`WorkEffortParty`) of the tasks it performs, with `TimeEntry` if its work is accounted. Its exchanges with other systems are SystemMessages or A2A tasks linked to those records.

## Requests and requirements: how change and demand enter the system

Work in Mantle does not start from a work effort. It starts from a **Request** (something someone asks for) or a **Requirement** (an internal need), and is then fulfilled by work efforts, orders or both. This is the path for change management and for human handling of business activities in general: not only products and assets, but agreements, budgets, production estimates and any other business object.

**Request** (`mantle.request.Request`) carries `requestTypeEnumId` (`RqtSupport`, `RqtBugFix`, `RqtNewFeature`, `RqtProposal`, `RqtPurchase`, `RqtQuote`, `RqtInventory`, `RqtInformation`, `RqtContact`), a `RequestCategory` tree with a responsible party, priority, `responseRequiredDate`, a resolution (`RrCompleted`, `RrFixed`, `RrWontFix`, `RrDuplicate`, `RrRejected`...) and the status flow `ReqDraft → ReqSubmitted → ReqReviewed → ReqInProgress → ReqCompleted` (with cancel and re-open). Around it: people in roles (`RequestParty`), items with product, quantity, supplier and maximum amount (`RequestItem`), notes, content, emails, communication events and wiki pages. Its services are in `mantle.request.RequestServices` (`create#Request` takes `assignToPartyId` and `customerPartyId` directly).

**Requirement** (`mantle.request.requirement.Requirement`) is an internal need: `requirementTypeEnumId` (`RqTpInternal`, `RqTpWork`, `RqTpProduct`, `RqTpInventory`, `RqTpCustomer`), facility, deliverable, asset, product, quantity, `estimatedBudget`, required-by date, use case and reason, with the flow `RqmtStProposed`/`RqmtStCreated → RqmtStApproved → RqmtStOrdered` or `RqmtStRejected`. Mantle has no dedicated services for it: write it through the entity-auto services, which also enforce its status flow.

How they connect, and therefore how to trace any change from the ask to its effect:

- **Request → work:** `RequestWorkEffort` links the work efforts that handle the request, and `Request.rootWorkEffortId` places the request inside a project.
- **Request → purchase:** `RequestItemOrder` links request items to the order items that fulfil them.
- **Requirement → origin:** `RequirementRequestItem` ties a requirement to the request item that produced it.
- **Requirement → money:** `RequirementBudgetAllocation` funds it from a `BudgetItem`.
- **Requirement → purchase:** `RequirementOrderItem` links the purchase order items that fulfil it.
- **Requirement → work:** `WorkRequirementFulfillment` links the work efforts that fulfil it, typed `WrfImplements`, `WrfDelivers`, `WrfDeploys`, `WrfFixes` or `WrfTests`.
- **Work → the business object it changes:** an agreement through `AgreementItemWorkEffort`, a production estimate through `ProductionEstimateWorkEff`, a maintenance through `AssetMaintenance.taskWorkEffortId`, a production run as a work effort with purpose `WepProductionRun`, plus `WorkEffortProduct`, `WorkEffortAssetAssign`, `WorkEffortFacility` and `WorkEffortInvoice`.

The model has no direct link from Agreement, Budget or ProductionEstimate to Request: the trace always goes through the work effort, or for money through the requirement's budget allocation. When a user asks for a change to a business object, the faithful way to represent it is a Request (or a Requirement for an internal need), fulfilled by a task under the relevant project, with the task linked to the object it changes. A direct update leaves no record of who asked, why, or who did the work.

## Measurement: a generic fact table

`mantle.work.measurement.Measurement` records one observation: `measurementTypeId`, `measurementDate`, a numeric value with `measurementUomId` or a categorical value in `measurementEnumId`, and optional dimensions `workEffortId`, `assetId`, `facilityId`, `productId`, `productMeterId`, `assetMaintenanceId`, `reasonEnumId` and `userId`. `MeasurementType` declares whether a type has a value, which unit type or which enumeration it uses, and which product meter it feeds. It is append-only and dimensioned like a fact table: use it for quality checks, meter readings and process values instead of adding columns to business entities, and index it with a DataDocument for analysis.

## Reading Moqui in DDD terms

Domain-driven design vocabulary is a useful lens, as long as the differences are kept in mind:

- **Aggregates.** A `<master>` with its root entity is the closest thing to an aggregate and its root: OrderHeader with parts and items, WorkEffort with its root. But Moqui does not enforce aggregate boundaries; any service can write any entity. Consistency comes from the owning services, SECAs, EECAs and status flows, so the rule "change an aggregate only through its root's services" is a convention you must follow, not something the framework guarantees.
- **Subdomains and bounded contexts.** Mantle's packages and service namespaces (`mantle.order`, `mantle.account`, `mantle.work`, `mantle.humanres`...) correspond to subdomains, but they share one model and one database: the Universal Data Model is closer to a shared kernel than to separate bounded contexts. Separate contexts appear at component or system boundaries, where SystemMessage connects them.
- **Events.** SystemMessage is closer to the transactional outbox and inbox patterns than to event sourcing: messages are stored reliably for exchange, but the state of the system is not rebuilt from them. Moqui's real event-sourced parts are its ledgers: `AssetDetail` holds inventory changes as differences and an EECA keeps the `Asset` totals as a projection; `AcctgTrans` and its entries form an append-only accounting journal corrected by reversals; `Measurement` and `TimeEntry` are append-only facts; and fields marked `enable-audit-log` (58 in Mantle) keep a change history in `EntityAuditLog`.

## Status machines

Statuses are a small framework model in `moqui.basic`, and the same pattern is reused everywhere (Mantle, moqui-device, moqui-math):

- `StatusType` groups the values, `StatusItem` is a value (`statusId`, `sequenceNum`, localized `description`).
- `StatusFlow` is a named machine; `StatusFlowItem` lists its states and marks the initial ones (`isInitial`); `StatusFlowTransition` lists the allowed moves (`statusId` → `toStatusId`) with a `transitionName` and an optional `userPermissionId` that restricts who may make that move.
- Some entities choose their machine per record with a `statusFlowId` field: WorkEffort, Device, DeviceGroupMember, DeviceRule, MathModel. Mantle's invoice services pick `InvoicePayable` or `InvoiceReceivable` this way.

How it is enforced matters for generated code. The check runs in the entity-auto update service (`EntityAutoServiceRunner`): when an update changes `statusId`, it looks for a `StatusFlowTransition` from the old to the new status and checks its `userPermissionId`, otherwise it throws. A direct entity update performs no check at all. The check matches the transition in any flow, not only the record's `statusFlowId`, so read the flow you intend in `status.md` before relying on it.

To read statuses and enums at runtime, the framework provides services in `org.moqui.impl.BasicServices`: `find#StatusItem`, `find#StatusFlowTransitionToDetail` (allowed next statuses from a given one), `find#Enumeration` and `find#EnumerationByParent` (with `includeNested` for whole subtrees).

## Seed data is part of the model

Enumerations, status items, flows and role types are data, not definitions, and they are what make the model usable: the same `Budget` entity means an operating or a capital budget only through `budgetTypeEnumId`. Seed, seed-initial and install data are indexed here; demo data is not, because it describes one fictional company and must not leak into generated code. To see how a whole company is set up (organization, GL accounts, time periods, facilities), read `mantle-usl/data/ZbaOrganizationDemoData.xml` as an example, not as a source of ids.

## Vocabulary of the user

Users name concepts in their own language ("commessa", "ticket", "posizione"). If the instance has localized labels, `moqui.basic.LocalizedMessage` and `moqui.basic.LocalizedEntityField` give translated names of entities, fields and enum descriptions; query them before assuming a mapping. Otherwise map the word to a concept, then confirm the concept in the index.

## Checking against a running instance

The index is built from source. A running instance can confirm it, and the tools screens in moqui-runtime show the same information: `Tools/Entity/DataEdit/EntityDetail` (fields, relationships, dependents tree, EECAs and the SECAs on the entity-auto services of that entity), `Tools/Service/ServiceDetail` (in and out parameters with their entity field, SECAs), `Tools/StatusFlows`, and `Tools/AutoScreen` (master-based edit screens). Their actions use `ec.entity.getEntityDefinition(name)` (`getRelationshipsInfo`, `getDependentsTree`, `getMasterDefinitionMap`), `ec.entity.eecaRulesByEntityName`, `ec.service.getServiceDefinition(name)`, `ec.service.secaRulesByServiceName` and `ec.service.knownServiceNames`. Use them to explore and verify, for example in the Groovy shell tool. They are implementation APIs: never put them in generated code.

## Keeping the index current

Rebuild after any change to entities or seed data, including your own components:

```bash
python3 scripts/build_model_index.py references \
  moqui-framework/framework moqui-runtime/base-component/tools mantle-udm mantle-usl \
  SimpleScreens MarbleERP PopCommerce HiveMind moqui-sftp moqui-math moqui-device runtime/component/<yours>
```
