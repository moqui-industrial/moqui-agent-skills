---
name: moqui-product
description: Modelling what a company makes, buys and owns in Moqui/Mantle — products, bills of materials and other product associations, variants and configurable products, product features (quantitative like rated voltage or I/O count, qualitative like CE marking), feature groups, category trees and the features that describe each category, and assets as product instances (bulk stock, serialized units, fixed assets) including devices with firmware and the as-built or current structure of an asset. Use this skill whenever the task touches the catalog, technical specifications, BOMs, inventory, equipment, installed base, serial numbers or the link between a physical device and the ERP.
---

# moqui-product: products, features, categories, assets

Names and values come from `moqui-model` (look them up in `enums.md`, never guess); data is written with `moqui-data` and validated with its `check_data.py`. `assets/ProductCatalogExample.xml` puts every concept below in one file that passes the checker.

## Products

`mantle.product.Product` is the definition of something: `productTypeEnumId` says what kind (`PtAsset` goods, `PtService`, `PtDigital`, `PtDigitalAsset`, `PtAssetUse` rental, `PtVirtual` with variants, `PtConfigurable`, `PtPickAssembly`), `assetTypeEnumId` and `assetClassEnumId` say what its instances become in inventory.

### Services are products too

A service sold or performed (installation, commissioning, a periodic inspection, a SaaS plan) is a `PtService` product with its prices, features and categories like any good. When the service is standardized, for example by a mandatory protocol such as a regulated leak check or a safety inspection, it can have its own bill of materials: `PatMfgBom` or `PatComponent` rows to the parts it consumes and to the sub-services it is made of, in the order and quantities the protocol requires. The way it is executed is a work effort template:

- `ProductAssoc.routingWorkEffortId` gives the routing for a component.
- `ProductMaintenance` ties a product to a maintenance type, a `templateWorkEffortId` with the steps to perform, and an interval in time or in meter readings (`intervalProductMeterId`). It is the place for a protocol that must be repeated on every installed unit.

Recurring and digital services are sold as subscriptions. `Subscription` and `SubscriptionResource` name the services that grant, renew, revoke and destroy access; see `moqui-instance` for one instance per subscriber.

## Product associations: BOMs and every other product-to-product link

`ProductAssoc` links `productId` to `toProductId` with a type, a validity period, `sequenceNum`, `quantity`, `scrapFactor`, `instruction` and `routingWorkEffortId`. The type decides the meaning:

- **Bills of materials:** `PatMfgBom` (manufacturing) and `PatEngBom` (engineering), both refinements of `PatComponent`. One row per component with its quantity; nested BOMs are simply components that have their own BOM rows. `routingWorkEffortId` points to the routing that uses the component.
- **Variants and configurations:** `PatVariant` from a `PtVirtual` product to each concrete variant; `PatConfigInstance` for instances of a `PtConfigurable` product; `PatUniqueItem`.
- **Lifecycle:** `PatRevision`, `PatReplacement`, `PatEquivalent`, `PatRefurbished`.
- **Commercial:** `PatAccessory`, `PatAddOn`, `PatCrossSell`, `PatUpsell`, `PatDownSell`, `PatAlsoBought`, `PatRequires`, `PatIncompatible`, `PatRepairService`, packaging types.

Mantle reads the BOM in `mantle.work.ManufacturingServices` (`get#ProductBomDetail`, and `recreate#ConsumeProductsFromProduce` to plan what a production run consumes).

## Features: technical and commercial attributes

`ProductFeature` is a reusable attribute value with a type (`productFeatureTypeEnumId`). It covers both kinds of specification:

- **Quantitative:** `numberSpecified` with `numberUomId`, for example rated voltage 400 V, rated power 7.5 kW, 16 digital inputs (a count needs no unit).
- **Qualitative:** the feature's presence on the product is the fact, for example "CE marked" with an abbreviation.

Mantle's feature types are mostly commercial (`PftColor`, `PftSize`, `PftBrand`, `PftWarranty`...). Technical types such as rated voltage, rated power, digital or analog I/O and certification are added as `ProductFeatureType` enumeration values in seed data, and missing units as `moqui.basic.Uom` (the framework has kW and A but no volt).

`ProductFeatureAppl` applies a feature to a product, dated, with `applTypeEnumId`:

- **`PfatStandard`:** the product has it.
- **`PfatDistinguishing`:** it is what tells a variant apart from the virtual product.
- **`PfatSelectable`:** the customer picks it, for configurable and virtual products.
- **`PfatOptional`:** it may be added, with `amount` as the price effect.

## Feature groups and categories: a schema per kind of product

- **`ProductFeatureGroup` with `ProductFeatureGroupAppl`** groups feature values, for example "motor nameplate data".
- **`ProductCategory`** has a type (`PctCatalog`, `PctMaterials`, `PctInternal`, `PctSearch`, `PctTax`...). It is arranged in a tree, or rather a graph, with dated `ProductCategoryRollup` rows (a category can have several parents), and products join it with dated `ProductCategoryMember` rows.
- **`ProductCategoryFeatGrpAppl`** attaches a feature group to a category, with an application type.

This is how a category says which features describe its products: the "Electric motors" category carries the motor nameplate group, and every motor in it is expected to have those features. When a catalog is built for engineering, design the category tree and its feature groups first, then the products.

## Assets: instances of products

`mantle.product.asset.Asset` is one instance of a product, and covers every case:

| Case | `assetTypeEnumId` | `hasQuantity` | Notes |
| --- | --- | --- | --- |
| Bulk stock | `AstTpInventory` | `Y` | Quantity from `AssetDetail` differences; one asset per receipt or lot and location |
| Serialized unit in stock | `AstTpInventory` | `N` | Always one unit, `serialNumber`, its own history |
| Fixed asset (equipment, vehicle, building) | `AstTpFixed` or a child (`AstTpEquipment`, `AstTpRental`, `AstTpRealEstate`) | usually `N` | Depreciation in the ledger, maintenance, location |
| Supplies, intangible, biological | `AstTpSupplies`, `AstTpIntangible`, `AstTpBiological` | as needed | |

`classEnumId` refines the kind (`AsClsInventoryRaw`, `AsClsInventorySub`, `AsClsInventoryFin`, `AsClsMfgEquip`, `AsClsCompressor`...). Quantities are never edited: they are the sum of `AssetDetail` rows, kept by an EECA (see `moqui-model`). Status follows the asset flow (`AstAvailable`, `AstOnHold`, `AstInUse`, `AstDefective`...). `parentAssetId` places an asset inside another one: a component installed in a machine.

## Devices: the digital side of an asset

A serialized asset with firmware or smart electronics also has an operational twin in moqui-device. In the moqui-industrial version, `Device` carries `assetId`: the device is the runtime face of that asset. The asset holds the business identity (product, owner, location, cost, maintenance, lots and serial numbers); the device holds the runtime identity (status flow, rules, parameters, events), and `PhysicalDevice` holds the hardware identity (vendor, model, firmware, hardware version, UUID).

Two things to keep in mind:

- **Group nodes may have no asset of their own.** `Device` also represents groups, subsystems, production cells, lines and plant nodes. When they are not separately owned things, `assetId` stays empty; when they are (a production line bought and depreciated as one asset), point them to that asset.
- **The public moqui-device does not have the field.** It depends only on moqui-math. Code meant for both versions must check whether `Device.assetId` exists before using it.

## As-built and current structure of an asset

The design structure is the BOM (`ProductAssoc` on the product). The structure of one physical unit is reconstructed from what actually happened:

- **As built.** The unit was produced by a work effort, which is its `Asset.acquireWorkEffortId` (also on its `AssetReceipt`). The components consumed by that work effort are the `AssetIssuance` rows with the same `workEffortId`: which assets (so which lots or serial numbers), how much, when, by whom. Compare them with the planned `WorkEffortProduct` rows of type `WeptConsume` to see deviations from the BOM.
- **Current.** Start from as built, then add the issuances made during the unit's maintenance (`AssetIssuance.assetMaintenanceId`, with `AssetMaintenance.assetId` being the unit) and remove the parts taken out. The `AssetDetail` history of the components gives the time line. Where serialized components are tracked one by one, also set their `parentAssetId` to the unit, so the current structure can be read directly.
- **Limit.** When one production run produces several units, issuances belong to the run, not to a unit. To attribute components to units, produce serialized units one per run, or record the installation with `parentAssetId`.

Query this through the entity engine, or index it with a DataDocument per issuance for analysis (`moqui-datadocument`).
