---
name: moqui-norm-search
description: Find the norm references that apply to a product once it is classified - from its hook records (ProductCategory, ProductFeature with thresholds, ProductFeatureGroup, DevicePurpose Enumeration) to the vocabulary concepts they realise, the norm items that define, specify, list or exclude them (with path, other language editions and text), the broader and related concepts, and the associations of the norms (essential requirement covered, method detailing a legal step, same subject, derived requirement, citation) - through denormalised Moqui DataDocuments indexed in OpenSearch, a database-only service, or SQL. Use this skill whenever an LLM or a user has to answer "which norms, articles, clauses apply to this product, device, function or feature", to classify a product description against the vocabulary, to search the loaded norms in full text, or to rebuild and check the search index after loading norm seeds.
---

# moqui-norm-search: the norm references of a classified product

The norms are Agreement items (`moqui-norm-loading`), linked to the vocabulary by hooks (`moqui-norm-hooks`) and to
each other by the associative graph (`moqui-norm-associations`). This skill reads all three from one entry point,
the record a product is classified into, and answers with the items an expert would open first and why.

## Documents (moqui-compliance `data/80_CmpNormSearch.xml`, index alias `compliance`)

| DataDocument | Entry point | Content |
| --- | --- | --- |
| `CmpHookCategory` | `productCategoryId` | the category, its concepts (names in every language, description, broader transitively, narrower, related, each with its own hook record), the items naming each concept by role, with path, text, other editions and associations; `norms`, `itemCount` |
| `CmpHookFeature` | `productFeatureId` | same, plus `numberSpecified`, `numberUomId` (a threshold: SIL 3, up to 1000 V) and the concept `comparison` (min, max, eq) |
| `CmpHookFeatureGroup` | `productFeatureGroupId` | same, for a dimension (functional safety, security level FR 1) |
| `CmpHookPurpose` | `enumId` (DevicePurpose) | same, for a function or the role of a device in a function |
| `CmpNormItem` | `agreementId`, `agreementItemSeqId` | one per item of every edition: text, title, path, norm, locale, other editions, concepts with role and hook ids, associations; a translation inherits concepts and associations of the primary edition |

The relationships of the DataDocument reach the hook and its concept vertices (`cmpConcepts`, extend-entity in
moqui-compliance); the manual data service `compliance.NormSearchServices.get#NormDocumentData` adds the rest. Item
lists are those of the concept itself: to see what applies through a broader concept (a PLC is a control system),
read the hook of the broader concept, whose id is in `broader[]`.

## Services and tools

| REST (`/rest/s1/compliance`) | Service | MCP tool (moqui-mcp) | Use |
| --- | --- | --- | --- |
| GET `norms` | `find#NormsForProduct` | `find_norms_for_product` | hook documents of a product or of hook ids (database only) |
| GET `search` | `search#Norms` | `search_norms` | full text over items or hooks (OpenSearch) |
| GET `tree` | `get#NormTree` | `get_norm_tree` | an item with ancestors and children to `depth`, or the table of contents |
| GET `references` | `get#ItemReferences` | `get_item_references` | citations out and in, concepts with hook and role, associations, editions of an item (and its children) |
| POST `index` | `index#NormSearch` | - | rebuild the search index |

The MCP tools come from the artifact group `MCP_SERVICE_TOOLS` in `data/80_CmpNormSearch.xml` (moqui-mcp offers each
listed service as a tool to the users authorized for it); the services and the REST path are granted to ADMIN by
`CMP_NORM_SEARCH`. `get#ItemLinks` is the internal service both the documents and `get#ItemReferences` read.

## Procedure

1. **Classify.** From a product description find its hook records: search the hooks with the words of the
   description in English and Italian (`norm_search.py search '<words>' --target hooks`), read the concept
   descriptions, and keep the records that fit: categories (what it is), features with their value (what it has:
   SIL 3, security level 2, supply voltage), purposes (what it does in a machine: emergency stop, isolation, safety
   logic). For a product in the database, its classification is `ProductCategoryMember` and `ProductFeatureAppl`.
2. **Fetch the references.** `GET /rest/s1/compliance/norms` with `productId` or the hook lists
   (`productCategoryIdList`, `productFeatureIdList`, `productFeatureGroupIdList`, `purposeEnumIdList`);
   `withText=false` for a first overview, then with text for the items to read
   (`norm_search.py product --category X --purpose Y [--text]`). It reads the database (EntityFacade
   `getDataDocuments`), so it works without the search engine.
3. **Widen by the vocabulary.** For every concept take the hooks of its `broader` concepts (general requirements:
   electrical equipment, control system, safety function) and look at the `related` ones as candidates that the
   product may also be (a supply disconnecting device is a disconnecting device and an isolator).
4. **Widen by the associations.** On every item: `CoversRequirement` (a standard clause gives presumption of
   conformity with an essential requirement), `Details` (the method for what the law asks), `DerivedRequirement`
   (system -> component -> device type, IEC 62443), `SameSubject`, `Cites`. Weight is confidence (1 = written).
5. **Read in context.** `get_norm_tree` on an item gives the clause it belongs to (ancestors) and its paragraphs,
   points and notes (`depth` 2 or 3); `get_item_references` gives what it cites and what cites it, and the
   associations of the items below it with `includeChildren`. A requirement is read whole: its clause, its points,
   its notes, and the clauses it cites.
6. **Search what the vocabulary does not name.** Full text over the items: `norm_search.py search '<query>'` with
   Lucene syntax on the fields `itemText`, `itemTitle`, `path`, `normId`, `agreementId`, `locale`,
   `concepts.key`, e.g. `itemText:"supply disconnecting" AND normId:"IEC-60204-1-2006"`.
7. **Answer** per norm: the item (`agreementId` + `agreementItemSeqId`, number and path), the role (defines,
   specifies, lists, excludes), and why it applies (the hook and concept, or the association with its evidence).
   Rank: legislation and its essential requirements first, then the harmonised standards that cover them, then the
   rest. Quote text of EU acts freely; for ISO, IEC, EN texts cite the clause and summarise in own words, never copy
   long passages (licensed, held only in the local database).

## Without the search engine

- `find#NormsForProduct` (step 2) needs only the database.
- SQL through the SQL Runner (`moqui-seed-reload/scripts/sqlq.sh`): `moqui-norm-hooks/assets/hook-items.sql`
  (hook -> items via its concept, broader and related concepts), `moqui-norm-associations/assets/assoc-neighbours.sql`
  (associations of one item).
- PostgreSQL full text (not set up; the test instance runs H2): a GIN index on
  `to_tsvector(<config by Agreement.locale>, ITEM_TITLE || ' ' || ITEM_TEXT)` of `AGREEMENT_ITEM`, queried with
  `websearch_to_tsquery`.

## Index

- A seed load does not feed the data feed: after loading 60_/70_/80_ or norm seeds, rebuild with
  `POST /rest/s1/compliance/index` (`dataDocumentId` for one document; about 2 minutes for 17k documents). It empties
  each index first (`clear`, default true): reindexing only adds and updates, and the document of an item whose id
  changed would stay. The service runs in its own transaction (a REST request has a 60 s transaction; joining it rolls back the manual data).
- Check: `curl localhost:9200/_cat/indices/cmp_*` and `/<index>/_count` against the database (hook records with a
  concept, items of all editions); `_cat/aliases` shows the alias `compliance` over the five indices.
- Semantic search (not set up): OpenSearch has the ml-commons, knn and neural-search plugins; an embedding model
  registered with ML Commons, an ingest pipeline on `cmp_norm_item` (`itemTitle`, `path`, `itemText`) and a hybrid
  query (BM25 + neural) would find items by meaning across languages. Measure it against the full-text baseline
  before adopting it.
- The REST path `/compliance` is granted to the group ADMIN (`CMP_NORM_SEARCH` in 80_); grant other groups there.

## Baselines (10 norms, 12 editions)

| Query | Expected |
| --- | --- |
| category `CMP_PC_SUPPLY_DISCONNECTING_DEVICE` | 23 items; EU-REG-2023-1230 (Annex III 1.6.3), IEC-60204-1-2006 (5.3 ...), ISO-12100-2010; `hook-items.sql` gives the same 23 as `self` |
| feature `CMP_PF_SIL_3` | 44 items, IEC-62061-2021 |
| purpose `CmpDepEmergencyStop` | 33 items in 4 norms; Regulation Annex III 1.2.4.3 -> ISO 12100 3.40 (Details) |
| search hooks `safety PLC` | safety logic unit, logic role, programmable controller, control system among the first five |
| category `CMP_PC_FIREWALL` | IEC 62443-3-2, 3-3, 4-1, 4-2, IEC/TR 62443-3-1 and the CRA |
| `get_item_references` IEC-62443-3-2-2020-EN 4.4.4 | concepts scs and safety-instrumented-system (specifies); mentions of IEC 62061 3.2.3 |
| index counts | 300 categories, 259 features, 37 groups, 46 purposes, 16564 items (the items of all editions in the seeds) |

A changed count after a reload is explained by the seed change (verification loop of `moqui-norm-loading`) or it
is a fault.
