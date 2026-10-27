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

Tools: the scripts of this skill (`scripts/`: `vocab.py`, `check_hooks.py`, `dump_part.py`, `hooks_file.py`,
`term_pass.py`, `tests/test_hooks.py`; they import `normkb` of `moqui-norm-loading`); the prepared query is
`assets/hook-items.sql`; the file formats are in `references/vocabulary-format.md`. The hooks files are in the
`mantle-compliance` component, `data/norms/vocabulary/` (written `vocabulary/` below).

## Data, not drafts

- `vocabulary/VOCAB-BASE.json` is the base; each norm has its extension `vocabulary/HOOKS-<normId>.json` (`concepts`,
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
- Edit hooks files with `hooks_file.py` (`add` a part file, `unreview` stale reviews, `dedupe` links given twice,
  `format`): one key and one list element per line, so a pass is a small diff. Never re-indent a whole file.
- Names in other languages: `vocabulary/LABELS-<lang>.json`, per concept `[preferred label, other terms ...]`, required
  for every concept (vocab.py fails otherwise). They name the records in that language (`LocalizedEntityField`) and the
  graph (`CmpConceptLocalLabel`, `CmpConceptLocalAltLabel`), and `check_hooks.py --lang <lang>` matches them against
  an edition in that language. Leave out terms that are generic words in that language ("presa", "arresto"); a label
  that is itself generic goes to the `lexiconSkip` of the LABELS file. Check a fully hooked norm in the new language
  first (the Italian edition of the Regulation): its findings show noisy names and links the first language missed.
  A hooks file states its `language`; a review made for another language carries it as fourth element.
- Notions that are the subject of a whole norm (SCS and safety function in IEC 62061, electrical equipment in IEC
  60204-1) are linked at the clauses whose subject they are, not at every paragraph.

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
   sample of its links is read against the text: `term_pass.py <normId> <alias> --part N --out part.json [--lang it]
   [--exclude a,b] [--sample 25]` turns the TERM findings into a part (definitions, notes, lists, rows, front matter:
   `l`; requirement text: `s`) and prints the sample. Read it, fix false senses with `normLexiconSkip` (a name with
   another sense in that norm: "conduit" between zones, "guard" a security guard, "posture" of security, "catene"
   supply chains) or a review, correct roles of examples, then `add` and `dedupe`. Look at the counts per concept
   first: a concept with hundreds of TERM findings is the subject of the norm and goes at clause level instead.
6. New concepts are named in every language at once: `hooks_file.py labels vocabulary/LABELS-it.json new.json`
   (keeps the file layout; never rewrite the labels file with another indentation). Alternative names that are
   generic in that language ("zona", a label whose parentheses the check drops) make false findings in other norms:
   after adding concepts, check every norm.
7. In a technical report (IEC/TR 62443-3-1) nothing is required: role `s` only where the text recommends ("shall",
   "should", a "Recommendations and guidance" clause), else `l`; acronym lists are `l` in every norm. The
   technologies a product can implement (authentication methods, VLAN, VPN, encryption, logging, malware and
   intrusion detection) are features of one group (`fg-security-technology`), the security products themselves
   (tokens, scanners, IDS, management tools) are product concepts.
8. Role `s` only where the text sets requirements on the concept. A chapter that names the product as its subject
   but binds authorities (CRA chapters on notified bodies, market surveillance, delegated acts, penalties) is `l`.
   Link the actor an article binds (`importer` at the importers' obligations, `enisa` at the reporting platform,
   `member-state`): the norm project plan (`moqui-norm-requirements`) leaves out articles that bind other actors.
9. Record ids are at most 40 characters (`CMP_PC_` plus the key): give long listed products short readable keys.

## How the check reads

- Names of a concept: its label without parenthesised parts and the defined terms of its `d` items, except a term
  that is another concept's label. Plurals and names broken over lines match. An occurrence inside the name of a
  linked concept is not a finding ("guard" inside a linked "adjustable guard").
- Plurals of other languages are generated from the names, not listed: in Italian the words before the first
  preposition change their ending, and in a second form the adjectives after the complement agree too
  (`sistemi di controllo relativi alla sicurezza`). Plural matching finds links the first language missed (its
  plural is often a different word: "control position" and "postazioni di comando"); a plural that is another word
  ("condotti a mano", hand-guided) is reviewed in that language.
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
- Levels a product reaches (IEC 62443 SL-C per foundational requirement, SIL, maturity of a supplier process) are
  features with a number and `>=`, one feature group per dimension, defined at the item that describes the level,
  linked from every list or table row that assigns requirements to that level; the requirements are reached
  through the references of those items (`CR 1.1 (1)` resolved at loading).
- Requirements a product meets (CRA Annex I part I) are features of a group with a feature type of their own,
  related to the equivalent notions of other norms (access protection to FR 1 and FR 2 of IEC 62443).
- Lists of product categories in a regulation (CRA Annexes III and IV) give one product concept per point under a
  concept for the class; names from the act (public) and short keys.
- Obligations of operators and authorities (keeping documents 10 years, notification deadlines, fines) are reviews,
  or values of a process concept; only what a product record carries is a threshold feature (support period).
- Device roles from the functional chain: sensors `role-input`, logic `role-logic`, power control `role-output`.
  Zones of an assembly for stopping or isolation are device groups whose purpose is the function.

## The verification loop

Run it after every step, not only at the end: after each reader rule, configuration change, transcription, figure
model, hook part or vocabulary change, and before every commit and every load. It checks every norm, not only the one
you touched, because a change for one edition can move the items of another.

```sh
cd <moqui root>   # or set MANTLE_COMPLIANCE
python3 <skills>/moqui-norm-loading/scripts/verify_norms.py   # all norms; a normId builds only that one, --db for the instance
```

Per norm it builds into a scratch directory (build errors stop it), compares the new seeds with the seeds in `data/`
(items with every field, references), runs the content check (Formex blocks, or PDF words page by page) and `check_data.py`; then the unit tests,
`vocab.py --check`, `check_hooks.py` of every norm in each language it is loaded in (an Italian edition is checked
with the Italian names), and with `--db` the read-only SQL checks of `moqui-seed-reload`. It ends with a table and
`RESULT: PASS` or `FAIL`.

- Commit or load only on PASS. A FAIL is fixed at its cause (reader, configuration, hooks file), then the loop runs
  again: repeat until PASS.
- Every difference the loop shows must be explained before going on: an id or text that changed (a more faithful
  reading: migrate the references; otherwise a regression: fix the rule), a page that loses words (cover, contents,
  other-language index expected; a section of the norm is a reader error), a finding, a stale review.
- When the loop itself reports something that cannot be (`entities=0` in `check_data`, every file failing the same
  way), fix the loop first: a broken check that passes is worse than no check.
- Write in the session log what each loop run found and what was fixed.

## Suite and query

- `tests/test_hooks.py`: for important hooks the items they must reach and must not reach, feature groups of
  categories, feature types, values and units of thresholds. Run it and `vocab.py --check` before every commit.
  Every new norm adds its cases (each hook it defines, and a shared hook reaching items of several norms). One key
  per hook: a second entry with the same key in a dict literal silently replaces the first, so its cases never run.
- A threshold feature (SIL 3, PFH below 1e-7) is linked at its own table row, not only at the table: a query from
  the hook must land on the row that states it and not on the other rows.
- After a reload (`moqui-seed-reload`), run `assets/hook-items.sql` with the record id of a hook in place of `:hook`
  (`CMP_PC_SUPPLY_DISCONNECTING_DEVICE`): concept, broader concepts transitively, related concepts one step, and the
  items they reach with role and parent clause. Exclude generic roots (machinery, electrical equipment: concepts
  with more than about a hundred links) from the broader walk, or the answer drowns in them; show `self` first.
- From a level or a requirement-assigning hook, `assets/hook-requirements.sql` takes the second step: the
  requirements its items cite (`iac-sl-2` reaches the CRs, SRs and REs of security level 2).
- When a reader change moves item ids, migrate the links and reviews by content with `hooks_file.py migrate
  <alias> <old 40_ seed> <new 40_ seed> [--labels LABELS-xx.json] [--write] vocabulary/VOCAB-BASE.json
  vocabulary/HOOKS-*.json`: the item with the same text, the item that took the text in (a legend joined to its
  formula), the new rows an old block was split into that name the concept (dropped when none does), else the
  parent. It also moves links of ids that now hold another text (after a merge, `D.2.p7` is another paragraph):
  a link follows its text, not its id. Read every printed move, run it once per pair of seeds (old = the seeds in
  `data/`, new = the build), then `dedupe`, and write the new seeds only after the loop passes.
