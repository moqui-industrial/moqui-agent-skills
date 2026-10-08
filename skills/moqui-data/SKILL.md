---
name: moqui-data
description: How to write Moqui entity-facade-xml data files — seed, seed-initial, install and demo data, nested records through relationships, service calls inside data, load order — and how to validate them against the real model. Use this skill whenever creating or reviewing Moqui seed data, setup data for a company, configuration records (enumerations, status flows, DbForms, users, permissions), demo data, or any XML that will be loaded with the Moqui data loader, even if the user just says "set up", "configure" or "load".
---

# moqui-data: writing Moqui data files

In Moqui much of what other systems put in code is data: enumerations, status machines, forms, permissions, a whole company setup. This skill is about writing that data correctly. Names and allowed values come from the `moqui-model` skill; never guess them.

## The file

```xml
<entity-facade-xml type="seed-initial">
    ...records...
</entity-facade-xml>
```

- **`type`** decides when the file is loaded: `seed` (framework and model configuration, always loaded), `seed-initial` (initial setup that must not be reloaded over user changes), `install` (reference data such as GL account templates and geo data), `demo` (example company, never in production). The loader includes a file only when its type is among the types requested.
- **Location and order.** Files in a component's `data/` directory are loaded in file-name order. That is why Mantle names them `ZaaGlAccountsInstallData.xml`, `ZbaOrganizationDemoData.xml`, `ZcaProductDemoData.xml`: the prefix fixes the order (GL accounts, then organization, then products). Components are loaded in dependency order. `<seed-data>` blocks inside entity definition files are another source of seed data, used for enumerations and statuses that belong with the entity.
- **Formats.** XML is the norm; the loader also accepts `.csv` and `.json` files.

## Records

A top-level element is one of three things:

1. **An entity**, by full name: `<mantle.party.Party partyId="ACME" partyTypeEnumId="PtyOrganization"/>`. Attributes are field values.
2. **An entity by its short-alias**, declared on the entity definition: `<dataDocuments .../>`, `<artifactGroups .../>`, `<userPermissions .../>`.
3. **A service call**, by service name written as `path.verbNoun`. The loader runs the service with the attributes as parameters. Mantle uses this for setup steps that are logic, not rows:

   ```xml
   <mantle.ledger.LedgerServices.initPartyAccountingConfiguration sourcePartyId="DefaultSettings"
           organizationPartyId="ORG_ZIZI_CORP" realTimeGlSummary="Y"/>
   ```

   This one copies the accounting configuration from the `DefaultSettings` template organization, and with `startYear` it also creates the fiscal year, quarter and month time periods. Prefer a service call over hand-written rows whenever a setup service exists.

Dates are written as epoch milliseconds (`fromDate="1265184000000"`) or as `"2013-01-01 00:00:00"`. A long text value can be given as a child element with the field name instead of an attribute.

## Nesting

Children are written inside their parent, and the loader fills the keys from the parent. This is the normal way to write a business object, and it follows the masters and aggregates described in `moqui-model`.

```xml
<mantle.product.Product productId="DEMO_1_1" productTypeEnumId="PtAsset" productName="Demo Product One-One"
        ownerPartyId="ORG_ZIZI_RETAIL">
    <prices productPriceId="DEMO_1_1_L" pricePurposeEnumId="PppPurchase" priceTypeEnumId="PptList"
            fromDate="1265184000000" minQuantity="1" price="19.99" priceUomId="USD"/>
    <categories productCategoryId="DEMO_ONE" fromDate="1265184000000" sequenceNum="1"/>
    <mantle.product.asset.Asset assetId="DEMO_1_1A" assetTypeEnumId="AstTpInventory" statusId="AstAvailable"
            facilityId="ZIRET_WH" locationSeqId="01010101" ownerPartyId="ORG_ZIZI_RETAIL">
        <mantle.product.asset.AssetDetail assetDetailId="DEMO_1_1A" effectiveDate="1265184000000"
                quantityOnHandDiff="100" availableToPromiseDiff="100"/>
    </mantle.product.asset.Asset>
</mantle.product.Product>
```

A child element is resolved in this order:

- **Relationship short-alias** of the parent (`prices`, `categories`, `locations`, `roles`, `organization`, `contactMechs`): the most readable form, and the one Mantle uses most.
- **Full entity name** of an entity related to the parent (the Asset above gets `productId`, its AssetDetail gets `assetId`).
- **Any other entity**: the loader passes the parent's values down to fields with the same name. Mantle nests a `ContactMech` inside a `Party` so that the `PartyContactMech` inside it receives both `partyId` and `contactMechId`. It works, but it is implicit; the checker flags it as a warning.

## Data as a program: plans, flows and pipelines

`entity-facade-xml` is a nested data-loading language, but when the data model drives execution, writing data is writing the program. In this ecosystem that happens in several places:

- **State machines.** `StatusFlow`, `StatusFlowItem` and `StatusFlowTransition` define the allowed transitions that services enforce. In moqui-device they are the control FSM of a machine (`DeviceData.xml` has 7 flows and 149 transitions).
- **Ordered steps.** A `DeviceRequest` with `DeviceRequestItem` rows ordered by `sequenceNum` is a sequence of parameter reads or writes that a router executes. Rules (`DeviceRuleSet`, `DeviceRule` with `priority` and `isEnabled`) choose which configuration to apply.
- **Data pipelines.** A `DataDocument` with its `DataFeed` defines what is extracted, how it is denormalized and where it is pushed on every change (see `moqui-datadocument`).
- **Categorical plans.** moqui-harness authors compositions of morphisms as entity-facade-xml drafts, validated before they are published.
- **Setup logic.** Service calls inside a data file run in load order, between the rows they depend on.

For these files the static check is not enough: validate them with `check_data.py`, then run what they define (a flow transition, a request, a feed) in a test environment and check the outcome, as you would for code.

## Identity in data

Unlike generated service code, data defines identities, so explicit ids are expected. Use stable, readable ids with a company prefix (`ORG_ZIZI_CORP`, `ZIRET_WH`, `DEMO_1_1A`) and keep user-facing codes in `pseudoId` where the entity has one. Reference values (`*EnumId`, `statusId`, `roleTypeId`) must exist in seed data; when you need a new one, define the `Enumeration` or `StatusItem` in the same file, before it is used.

## Patterns to copy

`references/data-catalog.md` lists every data file of the framework, moqui-runtime's tools and webroot, mantle-udm, mantle-usl, SimpleScreens, MarbleERP, PopCommerce, HiveMind, moqui-sftp, moqui-math and moqui-device (82 files) with its type, size and main content, in load order. Use it to find a model for what you are writing: GL account templates, item types, geo data, document definitions, organization and product setups, device flows.

## Validate

```bash
python3 scripts/check_data.py my-data/AcmeSetupData.xml \
  --src moqui-framework/framework --src mantle-udm --src mantle-usl --src moqui-math --src moqui-device
```

It reports:

- **`REF`:** element that is neither an entity, an entity short-alias, nor a service.
- **`NEST`:** child that cannot be resolved.
- **`FIELD`:** attribute that is not a field of the entity, or not an in-parameter of the service; service parameters include those from `auto-parameters`.
- **`VALUE`:** an `*EnumId`, `statusId` or `roleTypeId` value that exists nowhere in seed data or in the file.
- **`DOC`:** a DataDocument whose primary entity does not exist, whose `fieldPath` does not resolve through relationships to a field, whose expression path has no alias, or whose condition names a field the document does not have.

Calibrated on every data file of those components, it reports one real error: in `moqui-device/data/TrajectoryPlannerData.xml`, `MathModelDefContent` is given `mathModelContentId`, but the field is `mathModelDefContentId`.

After the static check, load the file into a scratch database and read back what was written.
