---
name: moqui-norm-requirements
description: Turn a bill of materials into the project of the norm requirements that apply to it - from the products, components, devices and the functions they realise (safety functions, protective functions, security zones and conduits) to one Moqui Requirement per product and norm clause, with its task in a WorkEffort project built from the matches, never from a template; detect and propose the missing levels of the bill (a function the norms name that no level groups, an unclassified product), keep the project in step with later changes of the bill, and verify it. Use this skill whenever a bill of materials, a machine, an assembly or a product has to be assessed, analysed or certified against the loaded norms, requirements and tasks have to be derived from norms, or such a project has to be updated after the bill changed.
---

# moqui-norm-requirements: the requirements of a bill of materials

The norms are loaded as Agreement items (`moqui-norm-loading`), named by the vocabulary (`moqui-norm-hooks`), linked to
each other (`moqui-norm-associations`) and searchable (`moqui-norm-search`). This skill applies them to what the user
builds or sells: the bill of materials is the input, a project of requirements and tasks is the output. The structure
of the project comes from the bill and from what the norms say about each of its levels; nothing is copied from a
fixed template, because a template holds requirements a product does not have and misses the ones it has.

## Model (Mantle, mantle-compliance)

| Record | Use |
| --- | --- |
| `Product` + `ProductAssoc` `PatComponent` (`PatEngBom`, `PatMfgBom`) | the bill of materials, from its root (machine, assembly, product) |
| `ProductCategoryMember`, `ProductFeatureAppl` | the classification of each product: categories (what it is) and features with values (what it has); each is a hook of the vocabulary |
| `Product` of type `CmpPtFunction` with `purposeEnumId` | a **function level**: safety function, protective function, security zone or conduit, any `DevicePurpose` the norms name |
| `ProductAssoc` `CmpPatFunction` | assembly or machine -> its function |
| `ProductAssoc` `CmpPatFunctionMember` with `purposeEnumId` | function -> product that realises part of it, with its role (`CmpDepRoleInput`, `CmpDepRoleLogic`, `CmpDepRoleOutput`, `CmpDepRoleActuator`, `CmpDepRoleMember`) |
| `Requirement` type `RqTpNorm` | one per product (or function) and norm clause: `productId`, `agreementId` + `agreementItemSeqId`, the hook it matched by (`hookTypeEnumId`, `hookId`, `conceptKey`, `matchRoleEnumId`), `reason` (every source, conditions) |
| `WorkEffort` `WetProject` / `WetMilestone` / `WetTask` | the project of the root product (`sourceReferenceId` `cmp-norm-project:<root>`), a milestone per norm, a task per requirement (`WorkEffortProduct` to its product) |
| `WorkRequirementFulfillment` | requirement <-> task (`WrfImplements`, `WrfTests`); many to many: one test campaign can fulfil several requirements |
| `WorkEffortAssoc` `WeatDependsOn` | the task of a clause depends on the task of the clause it cites (Annex V of the CRA on Article 28) |
| `Requirement` status `RqmtStSatisfied` | met already when found, shown by a document of the product: its task is closed (`WeClosed`) with the evidence as `WorkEffortContent` |
| `WorkEffort` `WetTask` purpose `CmpWepAction` | one action fulfilling several requirements (update a firmware, change a default password, verify a wiring), under the project, `WorkRequirementFulfillment` to each |
| `WorkEffort` `WetTask` purpose `CmpWepRetrospective` | the retrospective of the project: lessons and the changes proposed to the skills |
| `ProductFeatureAppl` type `CmpPfatTarget` | the SL-T of a zone or conduit: the SL-C features `CMP_PF_<FR>_SL_<n>` applied as a target; selects its IEC 62443-3-3 SRs and REs |

The function level is the design-time counterpart of `Device.purposeEnumId` and `DeviceGroupMember.purposeEnumId`
of moqui-device: the same `DevicePurpose` values, on products instead of installed devices.

## Services and tools

| Service | REST (`/rest/s1/compliance`) | MCP tool | Writes |
| --- | --- | --- | --- |
| `plan#NormProject` (rootProductId or rootDeviceId, normIdList, actorKeyList) | GET `project` | `plan_norm_project` | no |
| `create#NormProject` (rootProductId or rootDeviceId, projectName, requirementKeys) | POST `project` | `create_norm_project` | yes |
| `add#FunctionProduct` (parentProductId, purposeEnumId, productName, memberList) | POST `project/function` | `add_function_product` | yes |
| `satisfy#NormRequirement` (requirementId, evidenceList, note) | - | `satisfy_norm_requirement` | yes |
| `add#NormActionTask` (workEffortId, workEffortName, requirementIdList, fulfillmentTypeEnumId, purposeEnumId, productId) | - | `add_norm_action_task` | yes |

`get_norm_tree` and `get_item_references` (`moqui-norm-search`) read the clause a requirement points to.

## Procedure

0. **Product type or installation.** A type (a machine model, a boiler) is planned from its root product; an installation
   from its root device (`rootDeviceId`): every device is typed by the product of its asset and carries its hooks, the
   device groups with a DevicePurpose are the zones, conduits and functions, and each requirement is of a device
   (`Requirement.deviceId`, with the product of its type). An installed zone takes its SL-T from the zone product it is
   an instance of (Device.assetId -> Asset -> function product with `CmpPfatTarget` features).
0a. **Load the bill first** with `moqui-compliance-intake` (products, hooks, function levels, for an installation the
   assets, devices and groups); this skill starts from classified records.
1. **Read the bill.** Root product, its components (`PatComponent` and kinds, dated), their classification. Ask
   which organisation runs the project and in which role (`actorKeyList`: `manufacturer` by default; `importer`,
   `distributor`, `authorised-representative`, `system-integrator`, `asset-owner`): articles that bind other actors
   are left out. Ask which norms, or plan all loaded ones.
2. **Plan** (`plan_norm_project`), never write first. Read the result in this order:
   - `gaps`: show every gap to the user and **propose** what fills it; never fill it yourself:
     - `unclassified`: a product without hooks. Propose categories and features from the vocabulary
       (`search_norms` with `target=hooks` on its name and description), or a function level if the product is a
       grouping.
     - `missingFunction`: a product names a function (an emergency stop device names the emergency stop function, a
       motor above 0.5 kW the overheating protection) and no function level of the bill groups it; the gap says how
       many norm items wait for it. Propose the function product: its name, its purpose, the products that realise it
       **with their role** (the pushbutton as input, the safety logic as logic, the drive with STO as output), and the
       assembly it belongs to. A function often groups products the gap does not list: ask for them.
     - `roleWithoutFunction`: a product classified by a role (input, logic, output) that is in no function.
     - `emptyFunction`, `memberOutsideBom`: a function without members, a member outside the bill.
     - zones and conduits (IEC 62443-3-2): products that communicate (feature `cn-network-connected`, a fieldbus, a
       remote access) belong to a security zone, and links between zones to a conduit; when the bill has none,
       propose them as function levels (`CmpDepSecurityZone`, `CmpDepSecConduit`).
   - `conditional`: requirements of a norm about something no level is (IEC 62061 on a product in no safety
     function); they appear once the missing level exists.
   - `requirements` with `riskDependent`: a clause conditional on a hazard or a protective measure (Annex III 1.5.8
     noise: `hazards` `hz-noise`, `measures` the noise reduction system). The risk assessment decides; they are created
     as proposals with the condition in their reason.
   - `conditionalParts`: parts left out because they are about another kind of product (mobile, lifting, underground
     machinery; `conditionKind` `kind`) or bind another actor (`actor`). Show them when the user doubts the bill.
   - `exclusions`: items that exclude a concept of a product (electric motors under the Low Voltage Directive are
     excluded from the Machinery Regulation): ask whether the exclusion holds.
   - `scopeChecks`: the scope clauses of each norm reached: confirm the norm applies at all.
3. **Apply the user's decisions**: `add_function_product` for each accepted function, classification records for
   accepted categories and features (the user or a classification service writes them). Plan again; repeat until the
   user accepts the remaining gaps.
4. **Review the plan with the user**: requirements per product and norm, milestones, dependencies. The user may
   accept a subset: pass their keys (`productId|agreementId|agreementItemSeqId`) as `requirementKeys`.
5. **Create** (`create_norm_project`). Every requirement is born `RqmtStProposed`: a person approves or rejects it
   (`RqmtStApproved`, `RqmtStRejected`); never approve or reject one yourself. Propose rejections in the report, with
   the reason and the item.
5a. **Close what the documents already prove** (`satisfy_norm_requirement`): a requirement the product meets as its
   datasheet, certificate, EU declaration or test report shows becomes `RqmtStSatisfied`, its task closed, the document
   attached with the page or clause that shows it. Never without a document; never on the manufacturer's marketing
   text. Each one is checked at the verification gate (`moqui-compliance-verify`) before the report.
5b. **Zones and conduits: set the SL-T** (IEC 62443-3-2 ZCR 5.6, decided with the asset owner) as `CmpPfatTarget`
   features on the zone and conduit levels, then plan and create again: the SRs and REs of IEC 62443-3-3 come from its
   Table B.1. Until then the plan reports `missingSlTarget`.
5c. **Actions**: every concrete action the analysis finds (firmware updates from advisories, hardening of default
   settings, wiring or document checks, certificates to request) becomes an action task (`add_norm_action_task`)
   linked to all the requirements it fulfils: `WrfImplements` if it meets them, `WrfTests` if it verifies them. The
   one-to-one tasks stay: traceability is per requirement, the action is how several are met.
6. **Report**: project id, milestones with the number of tasks, requirements per product, risk-dependent ones,
   remaining gaps, the checks of `assets/project-checks.sql`.
6a. **Retrospective** at the end of every real project: an action task with purpose `CmpWepRetrospective` holding
   what went wrong or was slow, and the changes proposed to the skills (diff), approved by a person before they are
   committed (`moqui-compliance-verify`, section Retrospective).
7. **When the bill changes**, run 3 to 6 again on the same root: new requirements are added, existing ones kept,
   requirements the plan no longer gives are rejected with the reason (`[bom sync]`, and where the clause went: a
   function level takes the clauses of its machine), and a requirement rejected by the synchronisation that comes
   back is reopened. A requirement a person rejected stays rejected. Nothing is deleted.

## How the plan decides (so you can explain it)

- **Match**: a product reaches the norm items that *specify* (role `s`) a concept of its hooks: categories, features,
  the purpose of a function, the role of a member. Definitions, notes, examples, informative text (informative
  annexes, rationale and guidance), abbreviations and conventions are not requirements; scope clauses are checks.
- **Unit**: the lowest numbered clause that holds the text. A matched chapter or annex is split into its articles,
  parts or sections, down to the clause whose children are only paragraphs, points, notes, or sub-clauses with
  generic titles (Requirement, Rationale, Requirement enhancements, Security levels). Two or more parts of one leaf
  clause on one product become the clause (7.3.1 p1 to p4 are 7.3.1). A clause absorbs its own parts.
- **Subject**: the concepts the scope clauses of a norm define or specify (machinery and related products for the
  Machinery Regulation, products with digital elements for the CRA, SCS and safety functions for IEC 62061,
  components for IEC 62443-4-2). A requirement found on a product that is not that subject goes to the nearest level of
  the bill that is (the drive's network connection gives Annex III 1.1.9 to the machine), listing every source; a
  function holds its requirements itself when it belongs to such a level; with no such level it is `conditional`.
- **Conditions** of a part reached by splitting: an actor or a kind of product (a direct specialisation of the
  subject, a use or worked material) the bill does not have leaves the part out; a hazard or a protective measure
  makes it risk-dependent. The context of a product is what it contains and what contains it.
- **Function precedence**: a clause required of a function and of the machine it belongs to stays on the function.
- **Dependencies**: the task of a clause depends on the task of a clause it cites, on the same product or the root.
- **Kinds are conditions, their umbrella groups are not**: a part about mobile, lifting or underground machinery
  applies only to a product of that kind; the group gathering such characteristics does not make a food dryer
  mobile. An item matched directly inside such a part inherits the part's condition; what the norm itself is about
  (the SCS of IEC 62061) is never a condition, the subject rule places it.
- **Overview clauses** introduce requirements and are not requirements themselves (IEC 62443 "Overview").
- **SL-T selects the system requirements**: the zone's target level per foundational requirement picks the rows of
  IEC 62443-3-3 Table B.1; a target feature is never a hook (it is what the zone must reach, not what it is).

## When the plan is wrong

A wrong requirement is fixed at its cause, never by editing the plan or the project by hand:
- a wrong or missing hook, a role `s` where the text binds someone else (CRA chapters IV to VIII bind authorities:
  role `l`), an article without the actor it binds -> the hooks files (`moqui-norm-hooks`), regenerate and reload the
  vocabulary, plan again;
- a wrong classification -> the product's categories and features;
- a wrong rule of the plan -> `NormProjectPlan.groovy` in mantle-compliance, with the case in its comment.

## Verification

- `assets/project-checks.sql` with `:project`: counts per status, and 0 tasks without requirement, 0 requirements
  without their norm item, 0 requirements twice for one product and clause, 0 open tasks of rejected requirements.
- After a create, plan again: the number of requirements of the plan equals the `RqmtStProposed` and
  `RqmtStApproved` ones of the project; a second create without changes creates, rejects and reopens nothing.
- Read a sample of requirements with `get_norm_tree`: the clause must be about the product it is on.
