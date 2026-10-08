---
name: moqui-datadocument
description: Moqui DataDocuments and DataFeeds — defining denormalized documents over the entity model, pushing them in real time to OpenSearch/ElasticSearch, and querying or aggregating them for search, reporting and BI instead of star schemas. Use this skill whenever the task involves analytics, dashboards, KPIs, reporting, search indexes, OpenSearch or ElasticSearch with Moqui, exporting nested business data, or designing what should be indexed for an AI agent to search.
---

# moqui-datadocument: BI with denormalized documents

Moqui does not build star schemas. It defines **DataDocuments**: a primary entity plus fields reached through relationship paths, produced as nested JSON documents. A **DataFeed** pushes them to OpenSearch/ElasticSearch whenever the underlying records change, and reports and dashboards aggregate over the index. The definition is data, so write it with the `moqui-data` skill and validate it with its `check_data.py`, which also checks every field path.

## Definition

All entities are in `moqui.entity.document` (framework `EntityEntities.xml`); `dataDocuments` is the short-alias of `DataDocument`.

```xml
<dataDocuments dataDocumentId="MantleInventoryOrderItem" indexName="mantle_inventory" documentName="OrderItem"
        primaryEntityName="mantle.order.OrderItem" documentTitle="${orderId}:${orderItemSeqId}">
    <fields fieldSeqId="05" fieldPath="quantity" fieldNameAlias="orderQuantity"/>
    <fields fieldSeqId="09" fieldPath="((orderQuantity ?: 1.0) * (unitAmount ?: 0.0))" fieldNameAlias="orderItemTotal" fieldType="double"/>
    <fields fieldSeqId="10" fieldPath="part:statusId" fieldNameAlias="partStatusId"/>
    <fields fieldSeqId="13" fieldPath="part:vendorRoles:roleTypeId" fieldNameAlias="vendorRoleTypeId"/>
    <fields fieldSeqId="21" fieldPath="reservations:quantity" fieldNameAlias="quantityReserved"/>
    <conditions conditionSeqId="01" fieldNameAlias="productId" operator="is-not-null" fieldValue=""/>
</dataDocuments>
```

(From Mantle's `MantleDocumentInventoryData.xml`.)

- **`dataDocumentId`** must be camel case starting with a capital letter, like an entity name.
- **`indexName` is an alias**, not the physical index: each document gets its own index under it. Documents sharing an `indexName` can be searched together.
- **`fieldPath`** is `relationship:relationship:field`. Relationship names are the ones in `moqui-model` (short-alias, or title plus related entity). In the produced document each relationship level is nested under the relationship name (a list for many-relationships such as `reservations`); `search#DataDocuments` flattens results by default (`flattenDocument`). A path can also be a Groovy expression over other fields; then a `fieldNameAlias` is required.
- **`fieldNameAlias`** renames the field in the output, and conditions refer to fields by this name.
- **`fieldType`** forces the index field type when the default from the entity field is wrong for analysis.
- **`DataDocumentCondition`** filters which records become documents (`operator` as in `econdition`, `postQuery="Y"` to filter after the query). **`DataDocumentRelAlias`** renames a relationship level in the output. **`DataDocumentLink`** attaches links to detail screens for search results.

## Feeding the index

```xml
<moqui.entity.feed.DataFeed dataFeedId="MantleInventoryData" dataFeedTypeEnumId="DTFDTP_RT_PUSH"
        feedName="Mantle Inventory Data" feedReceiveServiceName="org.moqui.search.SearchServices.index#DataDocuments"
        feedDeleteServiceName="org.moqui.search.SearchServices.delete#DataDocument">
    <documents dataDocumentId="MantleInventoryAsset"/>
    <documents dataDocumentId="MantleInventoryOrderItem"/>
</moqui.entity.feed.DataFeed>
```

- **`DTFDTP_RT_PUSH`**: when any entity in a document changes, the document is rebuilt and sent to the receive service.
- **`DTFDTP_MAN_PULL`**: documents are pulled through the API on demand.
- **`indexOnStartEmpty="Y"`** indexes on startup when the index does not exist, which is useful where the search data is not persisted.
- **Feeds as change notifications.** The receive service does not have to index anything: SimpleScreens' `MyAccountNotifications` feed sends task, event, request, communication and wiki documents to `mantle.party.PartyServices.send#DataDocumentNotifications`, which notifies the users involved. A feed with your own receive service is a ready-made "on change of this business document, do X" pipeline.
- **Feeds can be extended.** A feed id defined in one data file can receive more documents from another file: Mantle's `MantleSearch` feed gets its general documents from `MantleDocumentData.xml` and its project, task, event and request documents from `MantleDocumentWorkData.xml`.
- **Template documents.** A DataDocument without a DataFeed is never indexed. Mantle keeps some of those as templates to clone (`MantleDocumentData.xml`).

After changing a document definition, delete its indexes and reindex the feed; Mantle's files carry a comment with the exact steps.

## Existing documents

`references/documents.md` lists the 18 DataDocuments and 6 DataFeeds defined across the components, by index, with primary entity, field and condition counts, relationships used, feeds and source file. Built-in coverage includes general search (party, product, facility, communication, wiki, project, task, event, request), inventory (assets, order items, production runs, estimates), sales (order parts and items, invoices and items) and PopCommerce's product search. Reuse or clone one of these before writing a new one. Every one of them passes the `DOC` checks of `check_data.py`. Rebuild the list with `scripts/build_document_catalog.py`.

## Using the documents

- **Search:** `org.moqui.search.SearchServices.search#DataDocuments`, with `indexName`, `queryString` and optionally `documentType` (the dataDocumentId), `nestedQueryMap`, ordering and paging. Mantle's party and project searches use it.
- **Aggregations for BI:** `org.moqui.search.SearchServices.search#CountBySource` with `sourceMap` (or `sourceJson`) containing a query and `aggs`. The equivalent API is `ec.elastic.getDefault().search(index, searchMap)`. Mantle's `InventoryReportServices` computes projected inventory by summing quantities from five documents grouped by `productId`.
- **Without the search server:** `ec.entity.getDataDocuments(dataDocumentId, condition, fromUpdateStamp, thruUpdateStamp)` returns the same nested maps, useful for exports and integrations.

## Designing documents for analysis

- **Pick one grain per document.** One document per order item, per asset, per budget line: the grain is the primary entity.
- **Use the append-only facts.** `Measurement`, `AssetDetail`, `TimeEntry` and accounting entries are natural grains for analysis: one document per observation, change or posting.
- **Share keys across documents.** Mantle's inventory documents all carry `facilityId` and `productId`, so five different documents can be aggregated by product in one index.
- **Denormalize what you filter and group on.** Statuses, types, dates, organization, names for display. Each extra relationship level costs indexing time on every change of the related records.
- **Prefer plain fields over expressions.** Expression paths are Groovy; keep them to simple arithmetic, as in the example, and never put them in generated documents without review.
- **Authorization does not follow the data into the index.** The index service runs with `authenticate="false"`, and a search returns whatever is in the index. Decide who may query each index, and include the fields (organization, owner) that a query must filter on.

`assets/BudgetDocumentTemplate.xml` is a complete example: one document per budget line with GL account, budget type and status, and organization and period reached through `budget:timePeriod`, plus its real-time feed. It passes `check_data.py`.
