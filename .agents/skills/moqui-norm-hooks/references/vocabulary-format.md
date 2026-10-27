# Extraction: from the norms to the catalogue

The norms are Agreement seeds (`build_agreement.py` of `moqui-norm-loading`, `data/40_Norm_*.xml`), one item per article,
paragraph and point; their associations are one graph (`moqui-norm-associations`, `data/70_CmpAssociations.xml`). Extraction turns
their text into records the rest of Moqui can use. It has two layers:

1. **Vocabulary (substantive layer)**: one set of concepts shared by all norms. Done once for all loaded norms, and
   extended when a new norm arrives. File: `data/norms/vocabulary/VOCAB-*.json`, converter `vocab.py`, seed
   `data/60_CmpVocabulary.xml`.
2. **Application (procedural layer)**: the requirements of the norms on a bill of materials and its function levels,
   with the tasks that meet them (`mantle.compliance.NormProjectServices`, skill `moqui-norm-requirements`). A
   moqui-math `Category` per norm (requirement types, procedural steps) is planned in `handoff/PLAN-COMPLIANCE.md`
   and not written.

A proposal is written once by an LLM that reads the whole norm. A person reviews it; the review is a check, not a
rewrite. The converter is the only way a proposal reaches the database.

## Vocabulary proposal

```json
{"proposalId": "VOCAB-BASE", "version": 1, "status": "proposed",
 "norms": ["EU-REG-2023-1230", "ISO-12100-2010", "IEC-60204-1-2006"],
 "normAliases": {"R": "EU-REG-2023-1230", "I": "ISO-12100-2010", "E": "IEC-60204-1-2006"},
 "concepts": [
   {"key": "presence-sensing-device", "scheme": "product",
    "label": "Protective device detecting the presence of persons (SPE)",
    "broader": ["protective-device", "anx1-part-b", "anx2-safety-component"],
    "related": ["fn-presence-detection", "role-input"],
    "clauses": [["I@3.28.5", "d"], ["R@ANXI.B.pt15", "l"], ["R@ANXII.pt2", "l"]],
    "description": "In our own words.", "note": "Merge decisions, differences between norms."}]}
```

- `key`: kebab-case, stable. All record ids are derived from it, so renaming a key creates new records.
- **One concept per notion.** When several norms define the same notion (ISO 12100 3.12, IEC 60204-1 3.48 and
  Regulation Annex III A(e) all define *risk*), they are one concept citing three clauses. Differences between the
  definitions go in `note`.
- `clauses`: `[item reference, role]`. Role is `d` (defines), `s` (specifies requirements or measures on it), `l`
  (lists or names it: an enumeration, a table row, a chapter about it that binds others) or `x` (excludes it from
  the scope). An item reference is `<alias>@<agreementItemSeqId>` of the primary edition (`R@ANXIII.B.1.2.1`).
- `broader`: more general concepts. A product can have several (an Annex I category is also machinery or a safety
  component); a function or member role has at most one (it becomes an Enumeration with `parentEnumId`).
- `related`: association across schemes (device and its function, term and product).
- `description`: **own words**, at most 400 characters. The converter refuses a description that repeats eight or
  more consecutive words of a cited ISO/IEC clause; for public EU law it only warns.

### Schemes and the record each one creates

| scheme | Record | Id |
|---|---|---|
| `product` | `ProductCategory` (type `CmpPctNormClass`) + `ProductCategoryRollup` per broader | `CMP_PC_<KEY>` |
| `featureGroup` | `ProductFeatureGroup`; `featureType` gives the type of its features | `CMP_PFG_<KEY>` |
| `feature` | `ProductFeature` + `ProductFeatureGroupAppl` per broader group | `CMP_PF_<KEY>` |
| `function` | `Enumeration` of type `DevicePurpose` (purpose of a DeviceGroup realising the function) | `CmpDep<Key>` |
| `memberRole` | `Enumeration` of type `DevicePurpose` (purpose of a DeviceGroupMember) | `CmpDep<Key>` |
| `term`, `actor`, `process`, `document` | graph only | none |

A product lists in `featureGroups` the feature groups that apply to it (`ProductCategoryFeatGrpAppl`,
`PfatSelectable`). This tells the BOM classifier which features to look for.

### What the converter writes

Graph `NG_CMP_VOCABULARY`: one vertex per concept, with id `vertex_id('CMP-VOCAB:<key>')`; `CmpGetBroader` edges
(directed) and `CmpGetRelated` edges (undirected). Parameters on each vertex:

- `CmpConceptKey`, `CmpConceptScheme`, `CmpConceptLabel`, `CmpConceptDescription`, `CmpConceptNote`;
- `CmpConceptItem`: `agreementId` and `agreementItemSeqId` of the norm item (extend-entity of `Parameter`),
  `parameterEnumId` = role (`CmpCcr*`);
- `CmpConceptRecord`: `symbolicValue` = entity name, `textValue` = primary key of the record.

The vocabulary vertex is the hub, and it carries the id of its mantle record (`productCategoryId`,
`productFeatureId`, `productFeatureGroupId`, `enumId`). From an item you reach its concepts (`CmpConceptItem` by
`agreementId` and `agreementItemSeqId`); from a concept its items in every norm and its record; from a record (a
product classified in a category) the items through the concept.

## Run

```
python3 scripts/vocab.py --check     # validate only
python3 scripts/vocab.py             # validate and write data/60_CmpVocabulary.xml
(cd scripts && python3 -m unittest discover tests)
```

Item references (`R@ANXIII.B.1.2.1`) are checked against `build/norm-kb/items/<normId>.jsonl`, written by
`build_agreement.py` (not in git). Without them the check is skipped with a warning.

Loading: skill `moqui-seed-reload` (stop, back up, delete the graph `NG_CMP_VOCABULARY`, load
`10_ComplianceTypeData.xml` then `60_CmpVocabulary.xml` by absolute path, start, check). A load does not remove
concepts or links dropped from the proposals: delete the graph first. Rebuild the search index afterwards.

## Adding a norm

Load it as Agreement seeds (skill `moqui-norm-loading`), then give it a hooks file
`data/norms/vocabulary/HOOKS-<normId>.json` with its alias (skill `moqui-norm-hooks`). For each defined term and each product class
it introduces, either cite the new clause on an existing concept (same notion) or add a concept. Never create a
second concept for a notion that already exists. Bump `version`, regenerate, then review the diff of
`60_CmpVocabulary.xml`.
