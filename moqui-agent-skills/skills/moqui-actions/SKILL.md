---
name: moqui-actions
description: How to program Moqui artifacts with the xml-actions language — every element of xml-actions-3.xsd with attributes, real usage frequency in Mantle and a real example, the runtime contract the XSD does not state (service naming, entity-auto services, in-map, out-map, SECA/EECA, authz, expressions), the restricted profile for generated code, and validators for references, parameters and XSD. Use this skill whenever writing, reviewing or fixing a Moqui service, xml-actions block, SECA/EECA action, or screen/transition actions, and before running any generated Moqui code.
---

# moqui-actions: how Moqui artifacts are programmed

The framework is a black box. What you program against is the xml-actions language and its runtime contract. **What** you manipulate (entities, enums, statuses) is in the `moqui-model` skill: use both together.

## The language

`references/elements.md` is generated from `xml-actions-3.xsd` plus every actions block (`<actions>`, `<always-actions>`, `<pre-actions>`, `<row-actions>`) in the framework, moqui-runtime's tools and webroot, mantle-usl, SimpleScreens, MarbleERP, PopCommerce, HiveMind, moqui-sftp, moqui-math and moqui-device: about 28,900 element uses, 41 of the 52 elements, with a separate count for the uses inside screens. It is ordered by real usage. The usage summary at the top shows that ten elements cover about 84% of real code:

`set`, `if`, `econdition`, `service-call`, `entity-find`, `entity-find-one`, `iterate`, `return`, `script`, `field-map`

Read the summary once, then open an element section only when you need its attributes. Each section lists required attributes, defaults, allowed values and one real example from Mantle.

## Runtime contract (not in the XSD)

- **Service names come from the file path.** A service with `verb="create" noun="Request"` in `service/mantle/request/RequestServices.xml` is called `mantle.request.RequestServices.create#Request`. Find the service by grepping `verb="create" noun="Request"`, never by guessing.
- **Entity-auto services exist for every entity**: `create#`, `update#`, `store#`, `delete#` followed by the full entity name, for example `create#mantle.humanres.position.EmplPosition`. They accept the entity fields. Use them only for entities without a dedicated service and without status (see the profile below).
- **`<implements service="..."/>`** inherits the in-parameters of another service. A parameter you do not see in a service may come from its interface; `place#Order` and `approve#Order` take `orderId` this way.
- **Parameters.** `in-map="[orderId:orderId, quantity:item.quantity]"` is a Groovy map literal. Keys that are not declared in-parameters do not reach the service. `out-map="context"` puts the outputs straight into the context (420 uses in Mantle); a named out-map keeps them separate.
- **Attributes are Groovy expressions.** `from`, `condition`, `in-map` and the `${}` parts of `value` and `message` are evaluated in the current context. `from="item.amount"`, `condition="asset == null"` and `value="${projectId}-MS-1"` are all code.
- **Errors.** `<return error="true" message="..."/>` stops the service, adds the message to the errors and rolls back the transaction. Check every lookup and stop with a clear message rather than letting a null travel further.
- **SECAs and EECAs.** SECAs run when a named service runs, including entity-auto names such as `update#mantle.product.asset.Asset`; EECAs run when an entity is written. `references/ecas.md` lists all of them (60 SECAs, 27 EECAs) by service and by entity, with their condition and the services they call. Look up every service you call and every entity you write there: changing an asset status through the service triggers `AssetStatusNotAvailableReservations`, a direct entity update does not.
- **Status changes are checked only through entity-auto update.** When an update service changes `statusId`, the framework verifies that a `StatusFlowTransition` exists from the old status to the new one and that the user has its `userPermissionId`. A direct entity update skips the check entirely. This is the main reason for profile rule 2.
- **Authorization** is checked on every service and entity access for the current user. A denial is an answer ("this user cannot do this"), not an obstacle to route around.
- **Asynchronous calls.** A `service-call` with `async="true"`, and SECA actions marked `(async)` in `ecas.md`, run later in a separate transaction. Their effects are not visible in the calling service, and they are skipped in simulation.
- **Effective-dated entities** are read with `<date-filter/>` inside `entity-find`.
- **Constraints live in the service, not in the XSD.** Before calling a service, read its definition: required parameters, `<matches regexp=...>` checks, excluded fields and comments. `create#Project` limits the id to 8 letters or digits; `update#Asset` excludes `locationSeqId` and its comment says to use `move#Asset`.

## Profile for generated code

Generated code runs with the requesting user's permissions and must stay reviewable. The checker enforces these rules:

1. **No `<script>`.** The scanned components use `<script>` 1,238 times (686 in Mantle's services); do not copy those blocks. Express the logic with `set from=`, `if`, `iterate` and service calls.
2. **No direct writes on status-bearing entities.** No `entity-create`, `entity-update`, `entity-delete` or `entity-store` on an entity that has `statusId`. Call the owning service.
3. **No calls to services with `authenticate="false"` or `"anonymous-all"`.** They bypass the user's authorization.
4. **No new entities, no Groovy or Java classes.**
5. **Parametric code.** Inputs are business keys (names, pseudoIds, codes); resolve them to ids inside the service at runtime. Never hard-code ids you found while exploring the data.
6. **Ask, don't invent.** If the request is ambiguous or a referenced record does not exist, stop and say what is missing.

## Validate before running

Run both checks on every generated file. Fix and re-run until both pass.

```bash
# references, parameters and profile
python3 scripts/check_artifact.py generated/MyServices.xml \
  --src moqui-framework/framework --src mantle-udm --src mantle-usl --src moqui-math --src moqui-device

# XSD (xmllint cannot compile the Moqui XSDs; Xerces can with full-checking off)
java scripts/ValidateXsd.java moqui-framework/framework/xsd/service-definition-3.xsd generated/MyServices.xml
```

`check_artifact.py` reports:

- **`REF`:** a service, entity or field that does not exist.
- **`PARAM`:** a key passed in `in-map` that the target does not declare.
- **`PROF`:** a profile violation.

Calibration on all 89 service files of the components above leaves 18 distinct reports. Several are real problems in the source:

- calls to services that do not exist under that name: `ShipmentServices.get#ShipmentPickPackInfo` and `get#ShipmentContactInfo` (both defined in `ShipmentInfoServices`), and the old `TenantServices`;
- `moqui-device/service/moqui/device/DeviceServices.xml` orders an `EntityAuditLog` find by `parameterId`, a field that entity does not have (the parameter id is in `pkPrimaryValue`);
- parameters passed to services that no longer declare them (for example `cancelDate` to `cancel#AssetIssuance`).

The rest may be limits of the checker on complex view-entities. When the checker reports something on code you copied from the components, verify it in the source before trusting either side.

`references/ecas.md` was built from the same components; all SECAs and EECAs are in Mantle and the framework.
