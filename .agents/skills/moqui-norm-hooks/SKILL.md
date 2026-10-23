---
name: moqui-norm-hooks
description: Extract from loaded norms (Agreement items) the hooks a product structure is classified into — ProductCategory and rollups, ProductFeature with value, unit and comparison, feature groups, DevicePurpose values for safety functions and device roles, DeviceGroup zones — as a vocabulary graph linked to the items that name each hook, verify the pass with a repeatable check, keep a hook test suite, and query from a hook the pertinent norm items. Use this skill whenever categories, features, thresholds, device purposes or groups have to be derived from a norm, the compliance vocabulary has to change, or the norms that apply to a product, device or feature have to be found.
---

# moqui-norm-hooks: the vocabulary between products and norms

A hook is a record a BOM or PLM instance is classified into: `ProductCategory` (with `ProductCategoryRollup`),
`ProductFeature` with value, unit and comparison (with `ProductFeatureGroup`, `ProductFeatureGroupAppl`,
`ProductCategoryFeatGrpAppl`), `DevicePurpose` enumeration values used by `Device.purposeEnumId`, `DeviceGroup` and
`DeviceGroupMember.purposeEnumId` (safety functions, zones, conduits), and the communication records
(`DeviceConnection`, `DeviceRequest.routerEnumId` and `brokerUri`). Each hook is a concept of the vocabulary graph
(moqui-math `Graph` `NG_CMP_VOCABULARY`) linked to the Agreement items that name it with a role: `d` defines,
`s` specifies (a requirement on it), `l` lists (an example, a list, a table row), `x` excludes. The norms must be
loaded first (`moqui-norm-loading`).

Tools in the `moqui-compliance` component, `tools/extraction`: `vocab.py`, `check_hooks.py`, `dump_part.py`,
`hooks_file.py`, `tests/test_hooks.py`; the prepared query is `assets/hook-items.sql` here.

## Data, not proposals

- `proposals/VOCAB-BASE.json` is the base; each norm has its extension `proposals/HOOKS-<normId>.json` (`concepts`,
  `addClauses`, `addFeatureGroups`, `reviewed`, `lexiconSkip`, `normLexiconSkip`, `proceduralParts`,
  `referenceParts`, `parts`). `vocab.py` merges them (all concepts first, then all links, so one norm's file may
  link a concept defined in another) and is the only way to `data/60_CmpVocabulary.xml`.
- Item references are `<alias>@<itemSeqId>` (`R@ANXIII.B.1.6.3`, `I@6.3.5.4`, `E@5.3`, aliases in `normAliases`).
- A concept: `key`, `scheme` (`product`, `feature`, `featureGroup`, `function`, `memberRole`, `term`, `actor`,
  `process`, `document`), `label`, `broader`, `related`, `clauses`, `description` in your own words (`vocab.py`
  rejects descriptions copied from licensed text). Features with a threshold add `number`, `uom`, `comparison`
  (`>`, `>=`, `<`, `<=`, `=`) and belong to a feature group with a `featureType`. A missing unit goes into the
  component type data with its `Uom`, `UomConversion` and unit type; a new feature type into `ProductFeatureType`.
- Reuse a concept before adding one. A concept of the wrong scheme is fixed in place (a circuit the BOM carries is a
  `product`, not a `term`).
- Edit hooks files with `hooks_file.py` (`add` a part file, `unreview` stale reviews, `format`): one key and one list
  element per line, so a pass is a small diff. Never re-indent a whole file.

## The pass, part by part

1. Read every item of the part with its links: `dump_part.py <normId> <alias> <parts>` (`--findings` for the items
   with findings, `--roots` for the parts of the whole norm).
2. Add what the text names: product kinds and components, characteristics and thresholds, hazards (origin and
   consequence), functions, device roles, groups and zones, connections. Link at the most precise item.
3. Check: `check_hooks.py <normId> <parts> --alias <alias>` reports TERM (a known name not linked), NUMBER (a value
   with a unit and no threshold feature linked), WORD (a component word and no product concept on the item or its
   ancestors). Fix each finding, or declare it in `reviewed` with its reason. A part is done at 0 findings.
4. After adding concepts, check every norm again: new concepts reveal links in parts already done.
5. A rule-based pass (link the concept wherever the text names it, role by item kind) is allowed only when a random
   sample of its links is read against the text.

## How the check reads

- Names of a concept: its label without parenthesised parts and the defined terms of its `d` items, except a term
  that is another concept's label. Plurals and names broken over lines match. An occurrence inside the name of a
  linked concept is not a finding ("guard" inside a linked "adjustable guard").
- A modelled figure is checked by its boxes, and a box by its own label, not by the boxes its flows name.
- `lexiconSkip` (all norms): a label that matches figurative uses ("impact"), with its real uses linked by hand.
  `normLexiconSkip` (one norm): a name with another sense in that norm ("protective device" is an electrical
  protective device in IEC 60204-1). `proceduralParts`: procedures, publication data, recitals (only TERM is
  checked). `referenceParts`: lists of cited documents (not checked).
- A review whose finding no longer occurs is printed as `# stale review`: remove it.

## Where to link

- A hazard origin at the row of its type in the hazard table; its consequence (crushing, shock) as its own feature.
- A figure box for what the box itself names; a "next box" or a branch label never.
- An index row for the concepts its term names (the row carries the other languages and the clause list).
- A required content of the instructions as `s`: the manual must describe it.
- Threshold features for scope limits, conditions that trigger a requirement and limits on characteristics a device
  record carries (voltages, currents, power, conductor sizes, environment); installation dimensions, test values
  and table values are reviewed.
- Device roles from the functional chain: sensors `role-input`, logic `role-logic`, power control `role-output`.
  Zones of an assembly for stopping or isolation are device groups whose purpose is the function.

## Suite and query

- `tests/test_hooks.py`: for important hooks the items they must reach and must not reach, feature groups of
  categories, feature types, values and units of thresholds. Run it and `vocab.py --check` before every commit.
- After a reload (`moqui-seed-reload`), run `assets/hook-items.sql` with the record id of a hook in place of `:hook`
  (`CMP_PC_SUPPLY_DISCONNECTING_DEVICE`): concept, broader concepts transitively, related concepts one step, and the
  items they reach with role and parent clause. Exclude generic roots (machinery, electrical equipment: concepts
  with more than about a hundred links) from the broader walk, or the answer drowns in them; show `self` first.
- When a reader change moves item ids, migrate references by content: an old id maps to the new id with the same
  text in the same clause or table, else to its container; then remove duplicate links.
