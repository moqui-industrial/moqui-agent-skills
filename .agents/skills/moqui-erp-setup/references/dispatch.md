# Dispatch guide: which Moqui mechanism for which need

Each section names the alternatives, the question that decides between them, and the default. When two answers seem to fit, pick the one that keeps a record of who, why and when; Moqui's mechanisms differ mostly in the state and history they keep.

## Contents

1. Exchange with something outside Moqui
2. Demand and change: Request, Requirement, Order, WorkEffort
3. Organizing work: which WorkEffort shape
4. Who is involved: parties, roles, relationships
4b. Describing products and things
4c. Contracts and service levels
5. Facts and history
6. Capturing input and showing data
7. Analytics and search
8. Where logic and configuration live

## 1. Exchange with something outside Moqui

| Need | Use | Why |
| --- | --- | --- |
| Business documents to or from another system (orders, invoices, shipment notices, bank files, EDI), possibly delayed, must not be lost or duplicated | **SystemMessage** (`moqui-systemmessage`) | Stored before sending or consuming, status lifecycle, retry jobs, acknowledgements, linked to the business record |
| Reading or writing process values of a machine, PLC, gateway or broker topic; subscriptions, cyclic reads, events, recipes, firmware | **DeviceRequest** with ordered DeviceRequestItems (moqui-device) | Typed by `DrtRead`, `DrtWrite`, `DrtCyclic`, `DrtEvent`, `DrtConfigWrite`..., routed by `DrrDirect`, `DrrMQTTBroker`, `DrrKafka`, `DrrMoquiDeviceGateway`..., with purpose `DrpControl`, `DrpMonitoring`, `DrpCommissioning`; values land in Parameters, not in documents |
| Another AI agent asks Moqui to perform a task, or Moqui delegates one | **A2A** (llm-client) with the agent as a party (see section 4) | Tasks and contexts are tracked per user; the agent's identity and permissions are those of its UserAccount |
| A synchronous question answered now, nothing to keep | **REST service call** (`/rest/s1`) | No state is needed; if the answer must be kept, it is a SystemMessage |
| Push business data to search or analytics on every change | **DataFeed** with DataDocuments (`moqui-datadocument`) | Real-time push of denormalized documents for search and analysis; it does not model a business exchange with a counterpart |

Decision questions, in order: Is it a machine signal rather than a business document? DeviceRequest. Is the counterpart an agent acting on its own? A2A. Must the exchange survive outages and be auditable? SystemMessage. Otherwise a service call.

## 2. Demand and change: Request, Requirement, Order, WorkEffort

| Need | Use | Why |
| --- | --- | --- |
| Someone asks for something: a customer, an employee, a partner, a user through an agent; it needs review, discussion and a response | **Request** | Requester and assignees in roles, type, category, priority, due date, resolution, flow Draft → Submitted → Reviewed → InProgress → Completed, notes, content |
| The organization itself needs something: material, work, a capability, with quantity, date and budget, to be planned and fulfilled | **Requirement** | Type (`RqTpInternal`, `RqTpWork`, `RqTpProduct`, `RqTpInventory`, `RqTpCustomer`), estimated budget, budget allocation, approval flow Proposed/Created → Approved → Ordered |
| A commitment with an external party to buy or sell | **Order** | Prices, terms, parts, reservations, invoices; fulfils request items (`RequestItemOrder`) and requirements (`RequirementOrderItem`) |
| Work to be done | **WorkEffort**, created to fulfil a Request (`RequestWorkEffort`) or a Requirement (`WorkRequirementFulfillment`) | Planning, assignment, time, status |

Rules:

- A request often produces requirements: a customer asks (Request), the company needs material and work to answer (Requirements, linked with `RequirementRequestItem`).
- Create a WorkEffort without a Request or Requirement only for work that is planned by the system itself (recurring maintenance from a product maintenance plan, a production run from an estimate).
- A change to a business object asked by a user (an agreement, a budget, a production estimate, a price, a configuration) is a Request fulfilled by a task linked to that object. A direct update leaves no trace of the ask.
- An agent acting for a user files the Request on the user's behalf and does the work as the task's assignee.

## 3. Organizing work: which WorkEffort shape

| Need | Use |
| --- | --- |
| A body of work with an end: commission, implementation, campaign | `WetProject` as root; everything else carries `rootWorkEffortId` |
| A breakdown of work | `WetTask` with `parentWorkEffortId` |
| A checkpoint that groups tasks | `WetMilestone` under the same root, tasks attached with `WorkEffortAssoc` `WeatMilestone` (not as parent) |
| Ordering between tasks | `WorkEffortAssoc` `WeatDependsOn` / `WeatIndependentOf` |
| Work on a specific asset | `AssetMaintenance` with its `taskWorkEffortId` |
| Making product | WorkEffort with purpose `WepProductionRun`, linked to estimates with `ProductionEstimateWorkEff` |
| Meetings, absences, availability | `WetEvent`, `WetTimeOff`, `WetAvailable` |
| A custom life cycle for one kind of work | `statusFlowId` on the work effort, with its own StatusFlow in seed data |

## 4. Who is involved: parties, roles, relationships

| Need | Use |
| --- | --- |
| A human | Party `PtyPerson` with `person`, plus a UserAccount to log in |
| A company, division, team, supplier, customer | Party `PtyOrganization` with `organization` |
| An AI agent or other automated actor | Party `PtyAutomatedAgent` plus a UserAccount; see "Automated agents as parties" in `moqui-model` |
| What a party is to the business (internal org, customer, supplier, employee, carrier...) | **PartyRole**. Required: Mantle's services decide behaviour from it |
| How two parties relate (employs, rolls up to, acts as agent for, represents) | **PartyRelationship** with type `PrtEmployee`, `PrtOrgRollup`, `PrtAgent`, `PrtRepresentative`, `PrtMember`, each side with its role |
| A party's part in one business object | The object's `*Party` entity (`OrderPartParty`, `WorkEffortParty`, `RequestParty`, `BudgetParty`...) with a role; also ensure the PartyRole with `mantle.party.PartyServices.ensure#PartyRole` |

## 4b. Describing products and things

| Need | Use |
| --- | --- |
| A technical or commercial attribute shared by many products (rated voltage, I/O count, CE marking, colour) | **ProductFeature** applied with ProductFeatureAppl, not a new field on Product |
| Which attributes a kind of product must have | **ProductFeatureGroup** attached to the **ProductCategory** with ProductCategoryFeatGrpAppl |
| A one-off value about a single physical unit (a reading, a test result) | **Measurement** on the asset |
| What a product is made of | **ProductAssoc** `PatMfgBom` / `PatEngBom` |
| Variants of one product | `PtVirtual` product, `PatVariant` assocs, `PfatDistinguishing` features |
| Product grouping for catalog, purchasing, tax or reporting | **ProductCategory** of the matching type, with rollups |
| A physical thing the company holds | **Asset**: `AstTpInventory` bulk (`hasQuantity` Y) or serialized (N), `AstTpFixed` family for equipment |
| The firmware and runtime side of a serialized asset | moqui-device **Device** with `assetId`, plus **PhysicalDevice** for the hardware (see `moqui-product`) |
| A standardized service with mandatory steps and parts | `PtService` product with its BOM, plus `ProductMaintenance` with a template work effort for repeated protocols |
| What one unit is made of now | AssetIssuance to its producing work effort and its maintenances, plus `parentAssetId` |

## 4c. Contracts and service levels

| Need | Use |
| --- | --- |
| A contract that governs many orders (framework, construction, supply) | **Agreement** with items and terms, linked to the job order project with `AgreementItemWorkEffort`; orders tied to the project and priced with agreement prices (`moqui-agreement`) |
| Payment and delivery conditions | **AgreementTerm** with a **SettlementTerm** (Mantle uses it for invoice due dates) and Incoterm term types |
| A price valid for one customer or contract | **ProductPrice** with `agreementId` |
| Limits promised to a customer (availability, devices, users, volume) | **AgreementTerm** `TtThreshold`, compared with **Measurement** by a scheduled service that opens a Request when crossed |
| A customer gets its own running system | **Subscription** whose resource provisions an **AppInstance** (`moqui-instance`) |
| More or fewer running instances as load changes | A ServiceJob over `check#AppInstance` and measurements calling `provision#AppInstance` / `stop#AppInstance` |

## 5. Facts and history

| Need | Use |
| --- | --- |
| An observation (reading, quality check, process value) about an asset, product, facility or work | **Measurement**, not a new field |
| A change of inventory | **AssetDetail** (the Asset totals follow by EECA), never an update of the totals |
| A financial effect | **AcctgTrans** with entries, corrected by reversal |
| Time worked | **TimeEntry** on the work effort |
| Who changed a field and when | `enable-audit-log` on the field, read from `EntityAuditLog` |
| Device process values | moqui-device Parameters, not Measurement, unless the value becomes a business fact |

## 6. Capturing input and showing data

| Need | Use |
| --- | --- |
| A questionnaire, checklist or a few extra fields on an existing form | **DbForm** (`moqui-dbform`): data, no code |
| A permanent application screen | XML screen |
| A temporary read-only view or a form inside an assistant conversation | Generated UI rendered by the assistant, never a substitute for a screen users rely on |

## 7. Analytics and search

| Need | Use |
| --- | --- |
| Dashboards, KPIs, aggregations, full-text search across objects | **DataDocument** with DataFeed to OpenSearch |
| A join used by services and screens | view-entity |
| An exact operational lookup | entity-find through the entity engine (authorization applies) |

## 8. Where logic and configuration live

| Need | Use |
| --- | --- |
| Values, types, statuses, flows, forms, documents, permissions, company setup | Seed or setup data (`moqui-data`) |
| A setup step that is logic (copying a template, creating periods) | A service call inside the data file |
| Business behaviour reacting to a change | SECA on the service (or EECA on the entity) calling a service |
| Behaviour that runs later or elsewhere | Async service, ServiceJob, or SystemMessage when another system is involved |
