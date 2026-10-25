---
name: moqui-norm-associations
description: Build the associative graph of the loaded norms as moqui-math Graph seed data (NG_CMP_ASSOC) - the links written in the texts (citations between articles, paragraphs, points) and the associations an expert makes between partitions of different norms (same notion, standard clause covering an essential requirement, clause detailing a legal step, requirements on the same object, derived requirements) - each edge with kind, confidence, pass and evidence, verified by sample and loaded and checked by SQL. Use this skill whenever norms have to be connected to each other, an association pass has to be added or reviewed, or the graph has to be queried from one partition of a norm.
---

# moqui-norm-associations: the associative memory of the norms

The norms are loaded as Agreement items (`moqui-norm-loading`) and hooked to the vocabulary (`moqui-norm-hooks`).
This skill connects their partitions in one moqui-math `Graph`, `NG_CMP_ASSOC`, the way an expert remembers them:
what the text cites, and what belongs together although no text says so. The seed file `data/70_CmpAssociations.xml`
is the value of the work; the database is where it is tested (`moqui-seed-reload`).

## Model

| Record | Use |
| --- | --- |
| `Graph` `NG_CMP_ASSOC` | directed multigraph, weighted |
| `GraphVertex` | one per `AgreementItem` taking part in an association, primary edition of the norm; `agreementId`, `agreementItemSeqId` (extend-entity in moqui-compliance: moqui-math stays generic); `label` = norm, item, title (text-short: at most 63 characters; never text of a licensed norm) |
| `GraphEdge` | `edgeTypeEnumId` = kind, `weight` = confidence 0-1, `isDirected` |
| `Parameter` on the edge | `CmpAssocPass` (symbolicValue: the passes that made it), `CmpAssocEvidence` (textValue: why, in short, own words or the citation as written) |

| Kind (GraphEdgeType) | Direction | Meaning |
| --- | --- | --- |
| `CmpGaCites` | citing -> cited | a citation written in the text (every `AatReference` that reaches an item, in a norm and between norms) |
| `CmpGaSameNotion` | undirected | two norms define the same notion |
| `CmpGaCoversRequirement` | standard clause -> essential requirement | conformity with the clause gives conformity with the requirement |
| `CmpGaDetails` | method -> requirement | a clause gives the method for what a law or norm asks |
| `CmpGaSameSubject` | undirected | requirements of two norms on the same precise product or function |
| `CmpGaDerivedRequirement` | general -> specific | system to component requirement, component to device type |

## Tool and passes

`tools/assoc/assoc.py` in moqui-compliance reads the seeds in `data/` (40_ of the primary edition, 42_) and the
vocabulary; every pass runs over all loaded norms; an edge made by two passes is kept once with both evidences.

```sh
python3 tools/assoc/assoc.py                       # counts and a sample of every pass
python3 tools/assoc/assoc.py --pass details --sample 20
python3 tools/assoc/assoc.py --write               # data/70_CmpAssociations.xml
python3 tools/assoc/assoc.py --compare             # against data/70_ (the verification loop runs it)
```

1. `text`: citations as written (weight 1).
2. `same-notion`: the defining items (role `d`) of one concept in different norms.
3. `essential-requirements`: Annex ZZ / ZA tables and lists of the standards, mapped to the law in force through its
   correlation table (Directive 2006/42/EC Annex I sections keep their numbers in Annex III of Regulation 2023/1230;
   lettered points are trusted only where they were read to match: 2006/42 yes, 98/37 no); requirement features of a
   law related to the dimensions of a standard (CRA Annex I and the IEC 62443 FRs).
4. `details`: a process or function a law requires (role `s`) and the clause of a standard that defines it or sets a
   requirement on it ("shall"), not a description that names it; notions with more than six items per norm are
   too broad to pair.
5. `same-subject`: requirement items ("shall", "deve") of two norms on a precise product or function, at most four
   per norm.
6. `derived-requirements`: identifiers and titles (IEC 62443-3-3 SR x.y -> 4-2 CR x.y -> EDR/HDR/NDR/SAR x.y).
7. `expert`: associations read one by one, `tools/assoc/proposals/*.json` (`kind`, `from` and `to` as
   `<normId>@<itemSeqId>`, `confidence`, `evidence` in own words). Read both items before writing one; check the
   words that support it (Regulation 1.2.1 names "malicious attempts").

## Verification

- Every pass prints a random sample: read it against the items. A wrong association shows a too broad rule (fix the
  rule: requirement words, size limits) or a wrong hook upstream (fix the hooks file: "generatore di prova" is not a
  generator), never by deleting edges by hand.
- `verify_norms.py` compares the generated graph with `data/70_` (every changed row must be explained) and runs
  `check_data.py` on it (lengths included); with `--db`, `assets/assoc-checks.sql`: counts per kind, and 0 vertices
  without their AgreementItem, 0 edges without a vertex, 0 edges without evidence.
- After a reader change that moves item ids the graph follows by regeneration; the expert proposals use item ids and
  must be checked (assoc.py stops on an item that no longer exists).

## Query

`assets/assoc-neighbours.sql` with `:agreement` and `:item` (`EU-REG-2023-1230-EN`, `ANXIII.B.1.2.1`): the partitions
of all norms associated with one item, both directions, strongest first, with kind and evidence.
