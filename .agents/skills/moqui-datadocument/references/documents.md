# DataDocuments and DataFeeds in the components (generated)

18 documents, 6 feeds. A document without a feed is never indexed automatically; Mantle keeps such documents as templates to clone.

## Documents by index

| Index | Document | Primary entity | Fields | Conditions | Relationships used | Feeds | Source |
| --- | --- | --- | --- | --- | --- | --- | --- |
| mantle | MantleCommunicationEvent | CommunicationEvent | 29 | 0 | fromUserAccounts, parties, purposes, status, toUserAccounts, type | MantleSearch, MyAccountNotifications | mantle-udm/MantleDocumentData.xml |
| mantle | MantleEvent | WorkEffort | 26 | 1 | assocs, facility, parties, purpose, resolution, status, toAssocs, type | MantleSearch, MyAccountNotifications | mantle-udm/MantleDocumentWorkData.xml |
| mantle | MantleFacility | Facility | 14 | 0 | contactMechs, ownerOrganization, status, type | MantleSearch | mantle-udm/MantleDocumentData.xml |
| mantle | MantleParty | Party | 57 | 0 | classifications, contactMechs, identifications, notes, organization, person, roles, settings, type, userAccounts | MantleSearch | mantle-udm/MantleDocumentData.xml |
| mantle | MantleProduct | Product | 51 | 0 | amountUom, assetClass, assetType, assocs, categories, class, dimensions, features, identifications, prices, toAssocs, type | MantleSearch | mantle-udm/MantleDocumentData.xml |
| mantle | MantleProject | WorkEffort | 12 | 1 | parties, purpose, status, type | MantleSearch | mantle-udm/MantleDocumentWorkData.xml |
| mantle | MantleRequest | Request | 32 | 0 | communicationEvents, facility, parties, resolution, status, store, type, workEfforts | MantleSearch, MyAccountNotifications | mantle-udm/MantleDocumentWorkData.xml |
| mantle | MantleTask | WorkEffort | 31 | 1 | assocs, communicationEvents, facility, parties, purpose, resolution, status, toAssocs, type | MantleSearch, MyAccountNotifications | mantle-udm/MantleDocumentWorkData.xml |
| mantle | MantleWikiPage | WikiPage | 8 | 0 | histories, space | MantleSearch, MyAccountNotifications | mantle-udm/MantleDocumentData.xml |
| mantle_inventory | MantleInventoryAsset | Asset | 11 | 1 |  | MantleInventoryData | mantle-udm/MantleDocumentInventoryData.xml |
| mantle_inventory | MantleInventoryOrderItem | OrderItem | 21 | 1 | header, part, reservations | MantleInventoryData | mantle-udm/MantleDocumentInventoryData.xml |
| mantle_inventory | MantleInventoryProdEstimate | ProductionEstimate | 5 | 0 |  | MantleInventoryData | mantle-udm/MantleDocumentInventoryData.xml |
| mantle_inventory | MantleInventoryRunConsume | WorkEffortProduct | 13 | 1 | issuances, workEffort | MantleInventoryData | mantle-udm/MantleDocumentInventoryData.xml |
| mantle_inventory | MantleInventoryRunProduce | WorkEffortProduct | 13 | 1 | receipts, workEffort | MantleInventoryData | mantle-udm/MantleDocumentInventoryData.xml |
| mantle_sales | MantleSalesInvoice | Invoice | 23 | 1 | fromRoles, paymentApplications, toClasses | MantleSales | mantle-udm/MantleDocumentSalesData.xml |
| mantle_sales | MantleSalesInvoiceItem | InvoiceItem | 45 | 1 | invoice, issuances, product | MantleSales | mantle-udm/MantleDocumentSalesData.xml |
| mantle_sales | MantleSalesOrderItem | OrderItem | 60 | 1 | header, issuances, part, product | MantleSales | mantle-udm/MantleDocumentSalesData.xml |
| mantle_sales | MantleSalesOrderPart | OrderPart | 31 | 1 | orderHeader, postalAddress, vendorRoles | MantleSales | mantle-udm/MantleDocumentSalesData.xml |

## Feeds

| Feed | Type | Name | Documents | Source |
| --- | --- | --- | --- | --- |
| MantleInventoryData | DTFDTP_RT_PUSH | Mantle Inventory Data | MantleInventoryAsset, MantleInventoryOrderItem, MantleInventoryRunConsume, MantleInventoryRunProduce, MantleInventoryProdEstimate | mantle-udm/MantleDocumentInventoryData.xml |
| MantleSales | DTFDTP_RT_PUSH | Mantle Sales Data | MantleSalesOrderPart, MantleSalesOrderItem, MantleSalesInvoice, MantleSalesInvoiceItem | mantle-udm/MantleDocumentSalesData.xml |
| MantleSearch |  |  | MantleProject, MantleTask, MantleEvent, MantleRequest | mantle-udm/MantleDocumentWorkData.xml |
| MantleSearch | DTFDTP_RT_PUSH | Mantle General Search | MantleParty, MantleCommunicationEvent, MantleProduct, MantleFacility, MantleWikiPage | mantle-udm/MantleDocumentData.xml |
| MyAccountNotifications | DTFDTP_RT_PUSH | MyAccount Notifications | MantleTask, MantleEvent, MantleCommunicationEvent, MantleRequest, MantleWikiPage | SimpleScreens/MyAccountDocumentData.xml |
| PopCommerceSearch | DTFDTP_RT_PUSH | PopCommerce Search | PopcProduct | PopCommerce/PopCommerceAabDocumentData.xml |
