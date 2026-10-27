---
name: moqui-norm-loading
description: Load legislation and technical standards (EU regulations from Formex XML, ISO/IEC/EN/CEI standards from PDF, national bilingual editions) into Moqui/Mantle Agreement seed data, one AgreementItem per article, paragraph (capoverso), point and sub-point, with references, translations, tables and figures as text, and verify the result against the source. Use this skill whenever a norm, a directive, a regulation or a standard has to be read into Moqui, a norm reader has to be changed, or a loaded norm has to be checked.
---

# moqui-norm-loading: norms as Agreement items

A norm is loaded faithfully, as it is printed, before anything is derived from it: the associative graph and the
hooks (categories, features, device purposes) come later and point at the items (see `moqui-norm-hooks`). Seed data
files are the source of truth; the database is only where they are tested (see `moqui-seed-reload`). Data rules and
the validator come from `moqui-data`; the Agreement model from `moqui-agreement`.

The tools are the scripts of this skill (`scripts/`: readers in `normkb/`, `build_agreement.py`, `build_norm.py`,
`check_words.py`, `check_formex_items.py`, `verify_norms.py`). What they read and write is in the `mantle-compliance`
component (`moqui-industrial/mantle-compliance`): the seeds in `data/`, their curated inputs in `data/norms/` (not
loaded by Moqui) and the intermediate files in `build/norm-kb/` (not committed); `scripts/normkb/paths.py` lists them.
The component is found from env `MANTLE_COMPLIANCE` or from the current directory upwards (run from the Moqui root).
The scripts of `moqui-norm-hooks` and `moqui-norm-associations` import `normkb` from here. They need Python 3,
`pdftotext` (poppler) and PyMuPDF (`pymupdf`, imported from user site-packages: do not run those scripts with
`python3 -I`).

## Model

| Record | Use |
| --- | --- |
| `Agreement` | One per norm and language edition, id `<normId>-<LANG>` (`EU-REG-2023-1230-EN`, `IEC-62061-2021-IT`), type `AgrLegislation` or `AgrStandard`, `locale` |
| `AgreementItem` | One per partition: book, title, chapter, section, article, paragraph, subparagraph, point, sub-point; annexes with parts; figures, tables and their rows. `parentItemSeqId` builds the tree, `itemNumber` keeps the number or letter as printed, `itemTitle`, `sequenceNum`, `sourceLocation` (page) |
| `AgreementAssoc` `AatReference` | A citation written in the text, at item level (`agreementItemSeqId`, `toAgreementItemSeqId`), `assocText` as written |
| `AgreementAssoc` `AatTranslation` | Another language edition of the same item (same `agreementItemSeqId`) |
| `AgreementAddendum`, `AgreementContent` | Amendments; images and documents |
| Stub `Agreement` | A cited document that is not loaded (`STUB-ISO-13850`): header only, so that references have a target |

The item fields and item types (`AitArticle`, `AitParagraph`, `AitPoint`, `AitSubPoint`, `AitNote`, `AitExample`,
`AitFigure`, `AitTable`, `AitAnnex` ...) are extensions of mantle-udm (moqui-industrial fork, branch
`agreement-structure`). A numbered clause of a technical standard at any level is an article.

## Item ids

Stable, readable paths of at most 40 characters: `ART3.pt12`, `ANXIII.B.1.2.1.p2.pta`, `5.5.3.5.p1.pta`,
`6.4.1.2.p3.li2`, `TABB.1.r4`, `FIG1.plc`. Points carry `pt`, paragraphs `p`, dash items `li`, notes `n`, examples
`x`, numbered sub-points `sp`, table rows `r`. A longer id is a reader error: never truncate. Ids change only when
the reading becomes more faithful; then migrate every reference to the old id by content (see `moqui-norm-hooks`).

## Capoverso rules

- Every paragraph of text is an item; a list belongs to the paragraph (or point, or note) that introduces it.
- A container with a single paragraph keeps the text itself; a block that holds only a list is not a paragraph.
- Section numbers come from the title, never from numbered paragraphs inside.
- A note that does not end its sentence introduces the list after it; a note between two dash items belongs to
  the item before it; a lettered list inside a note stays in the note.
- A numbered line whose text is a sentence is an untitled clause, and so are its siblings ("6.4.1.1 Drafting ...").
- `1.` `2.` sections of a form open their own lettered lists; national deviations (`clause: text`) are one
  paragraph each.

## Workflow

1. Configure the norm in `data/norms/norms.json`: reader (`formex` or `pdf-standard`), files per language,
   `agreementType`, `date`, `licensed`, `bilingual`, `definitionsClause`, `paragraphGaps`, `boilerplate` lines
   (page headers and footers), `indexes` (indexes printed in columns), `lineFixes` (regex and replacement pairs
   applied to the page text before reading, for defects of one conversion only: link anchors "139H" after contents
   entries and page numbers printed "1 2" in IEC/TR 62443-3-1; a rule that holds for more than one edition goes in
   the reader, not here).
2. Build into a scratch directory: `python3 build_agreement.py <normId> --data-dir <scratch>`. The build fails on
   duplicate ids, on a clause whose items do not rebuild its text (the error shows where the texts diverge), on an
   unresolved citation of the norm itself, on an unresolved index reference and, for Formex, on item texts outside
   0.9-1.05 of the source characters. That ratio is only a guard: when it fails, run the block check on the items
   before suspecting the reader (a counter that dropped the text after each footnote made a faithful act look 7 %
   too long).
3. Verify the content, part by part, before going on (counts and coverage ratios prove nothing):
   - Formex: `check_formex_items.py` (every leaf block of the source in exactly one item, 0 lost, 0 duplicated);
   - PDF: `check_words.py <normId> --lines` compares the words of the pages kept with the words of the items and
     lists the pages that lose words, then the lines of the PDF of which no three-word sequence is in an item. Word
     counts hide a paragraph cut at a page break or a page header kept as text (the same words occur elsewhere);
     the line list shows them. Explain every page: cover, contents, the EN cover in three languages, an index in
     the other language, table lines with empty middle cells are expected; a paragraph of the norm is a reader
     error. The build's character ratio is only a guard;
   - read sampled items side by side with the source: lists under the right paragraph, notes in order, definitions
     with their term, tables with labelled columns, figures as text.
4. Check the build report: `tocMissing` empty, `languageCorrected`, `duplicateCaptions`, `transcribedTables`.
5. Rebuild the norms already loaded and compare their ids and texts with the previous build: a reader change must
   not change them silently. When it does and the new reading is right, migrate the references.
6. Write to `data/` (`40_Norm_<normId>_<LANG>.xml`, `41_NormStubs.xml` shared by all norms, `42_NormCrossRefs_<normId>.xml`
   for references to other loaded norms, loaded after all of them), run `check_data.py` of `moqui-data` on every file
   with the component roots as sources (`--src framework --src runtime/component/mantle-udm --src
   runtime/component/mantle-compliance`; `entities=0` in its output means wrong sources), run the unit tests in
   `scripts/tests`, commit. Licensed texts (ISO, IEC, EN, CEI, UL) are gitignored; EU acts are committed.

## PDF readers

- Text from `pdftotext -layout`, geometry from PyMuPDF. Ruled tables are read again by rows (`pdf_tables.read_tables`;
  a table belongs to the caption line above it or continues from the previous page); a two-level header with a cell
  spanning the columns below it becomes one label per column. An index printed in columns without rules is read by
  word positions (`read_index`) into row items whose clause column becomes references.
- Captions, table cells and drawing labels move to their figure or table item. Caption variants of national
  editions are captions: `–Titolo`, `–- Titolo`, `H.4-Titolo`, `(2 di 2)`, `(segue)`.
- Bilingual CEI editions alternate languages page by page: the alternation found on the pages detected with
  confidence decides every page between the first and the last alternating pair (an Italian page listing English
  titles is still Italian); covers and trailing national indexes stay as detected.
- A text without blank lines between paragraphs gets them from the page geometry (`paragraphGaps`: a line whose
  distance from the previous one exceeds 1.4 times its font size starts a paragraph).
- Titles wrapped on two lines are completed from the table of contents; a caption title continued on a line that
  starts in lower case is one title. A numbered line is a heading only if its title begins as the contents entry of
  that number ("5 Optimizing ..." in a table is not clause 5). An indented numbered line is a heading when the
  contents confirm it or when it is aligned with the text that follows it (a page whose table starts further left
  than its text). Captions continue as "(continued)", "(segue)", "(1 di 2)", "(2 of 4)".
- National and European wrappers: CEI cover and data pages, the EN cover in three languages, "European foreword"
  (its own front section), endorsement notice. Page headers in every form of the edition go in `boilerplate`
  ("IEC 62443-4-1:2018 © IEC 2018", "62443-3-3 © IEC:2013(E)", "Recepita come CEI ...").
- A rule line (`_____`) followed only by marked lines ("3 ...", "a ...", "( 1) Editor's Note ...") separates the
  footnotes of the page: the paragraph goes on on the next page and the footnotes come at the end of the clause. A
  rule followed by other text ends the document.
- Characters in the private use area are decoded by their font (PyMuPDF knows it, pdftotext does not): Symbol to
  Unicode (λ, ×, ∑, ≥; Greek capitals drawn like Latin letters as Latin, "MTTF"), Wingdings (✓ ✗ ●), the Adobe
  serif © of page headers. Tall brackets are pieces: the middle piece is the bracket.
- Formulas: a fraction printed on three lines is written numerator/denominator in its slot of the middle line (the
  inside of an empty bracket pair or a gap); the words of a numerator split where the middle line has a sign
  between them ("2 U0" over "≤ ×" is 2/3 × U0/Ia). The legend ("where"/"dove", "X is ...") joins its formula while
  contiguous; after a list or a note its lines are paragraphs. A Greek letter does not continue a paragraph broken
  by the page.
- A list item broken by the page or by a paragraph gap goes on in the next block when that block starts in lower
  case aligned with the text of the item; a block back at the marker column (or further left) completes the sentence
  that introduced the list and stays a paragraph ("sia tramite: • ...; o • ..." / "che tramite ...", IEC 62061
  6.7.3), and so does a block after an item closed by "," ";" or "and/or" (IEC 60204-1 11.5).
- Labels of a drawing are the blocks printed just before its caption; a bullet of the clause above the drawing is
  text, not a label: it ends with ";" or ":", or is a sentence ending with "." longer than a label, or cites the
  figure ("(Figure 3)"). "• Training, etc." inside the drawing of ISO 12100 Figure 2 is a label.
- A short line under the term of a definition is an admitted term only if definition text follows it; followed by
  "Note 1 to entry", an EXAMPLE or a source it is the definition itself (IEC 62443-3-2 3.1.11 likelihood).
- Lists: a note between two items belongs to the item before (dash items; numbered sub-points past legends and
  notes); a note between a paragraph that introduces a list and the list belongs to that paragraph; 1) 2) are
  sibling points; a paragraph ending ":" followed by a new a) closes the open list; a point ending "," or ";" is
  part of a sentence, not a heading; "(1) Title" requirement enhancements are numbered points owning the text after
  them ("(1)" stays in the text, the number in `itemNumber`).
- Tables: a table continues on the next page with "(continued)" or with its header row repeated, on pages of the
  edition's language only (the Italian page of a bilingual CEI edition is not a continuation); a one-row header is
  aligned to its value columns when the grid is finer than the table; header note letters are dropped only as
  superscripts (smaller and raised: "I a" is a subscript and stays, "10-5" and "mm2" are exponents and stay).

## Tables and figures that are images

Phase 1 converts diagrams and images to text. When a table is an image, or its PDF grid puts values in other
columns (scan the rows whose values have no column label), render the page (`pdftoppm -r 110`, a crop at 220 dpi for
small numbers), read it and transcribe it in `config/tables/<normId>.json` (`header`, `rows`, `pages`, `source`;
`"override": true` replaces an extracted table). Transcriptions are licensed content: gitignored like the seeds.
Write a figure as a model in `config/figures/<normId>.json`: nodes (`flowStep`, `flowDecision`, `flowTerminal`) with
their labels in your own words in the language of the edition, flows with optional labels or Yes/No conditions,
`refs` to the clauses the boxes cite, groups and attributes for what the drawing says around the boxes. A diagram
without decisions is a block diagram. Keep the edition as printed: a caption number printed twice becomes a second
figure (`FIGH.4-2`), a translation slip stays, and the build report lists them.

## References

- Every citation of the act itself must resolve to an item, as precisely as it is written: "Part I, point (2)(c), of
  Annex I" reaches that sub-point, not the annex. "Article N thereof" belongs to the act named before, "Article 218
  TFEU" to the Treaty, "Annex III to that Regulation" to the act of that kind named last; the act cited by its own
  name ("Annex III of Regulation (EU) 2023/1230" inside that Regulation) is itself. Equation, figure and table
  numbers are not references.
- A series that names its requirements (IEC 62443: "CR 1.1", "SR 1.1 RE 2", "NDR 1.13 (1)", "SM-1", "ZCR 3.2") gets
  `requirementSeries` in `norms.json`: identifiers indexed from clause titles and numbered enhancements, a citation
  reaches its own item, else the part of the series that defines it. Build the parts it cites first.
- A citation of a partition of another loaded act reaches its item ("sections 1.1.9 and 1.2.1 of Annex III" of the
  Machinery Regulation from the Cyber Resilience Act): build the cited act first.
- Parts and classes keep the number as printed in their id (`ANXI.II`, `ANXIII.clI`), never a position (`g1`).
- A partition of another norm stays with its text ("ISO 14118:2000, Clause 5"); when that norm is loaded the
  reference reaches its item through the `42_` file.
- A part number is another document (ISO 12100-1 is not ISO 12100). A dated citation reaches a loaded norm only for
  the years of its edition (`refs.EDITION_YEARS`); an undated one reaches the edition loaded.

## The verification loop

Run it after every step, not only at the end: after each reader rule, configuration change, transcription, figure
model, hook part or vocabulary change, and before every commit and every load. It checks every norm, not only the one
you touched, because a change for one edition can move the items of another.

```sh
cd <moqui root>   # or set MANTLE_COMPLIANCE
python3 <skills>/moqui-norm-loading/scripts/verify_norms.py   # all norms; a normId builds only that one, --db for the instance
```

Per norm it builds into a scratch directory (build errors stop it), compares the new seeds with the seeds in `data/`
(every item with every field, every reference: the seeds are the value of the work, so they are the baseline, not an
intermediate file or the database), runs the content check (Formex blocks, or PDF words page by page) and
`check_data.py`; then the unit tests,
`vocab.py --check`, `check_hooks.py` of every norm in each language it is loaded in (an Italian edition is checked
with the Italian names), and with `--db` the read-only SQL checks of `moqui-seed-reload` and the database against the seeds (items and
associations per Agreement: rows of an older build stay after a load). It ends with a table and
`RESULT: PASS` or `FAIL`.

- Commit or load only on PASS. A FAIL is fixed at its cause (reader, configuration, hooks file), then the loop runs
  again: repeat until PASS.
- Every difference the loop shows must be explained before going on: an id, field or text that changed, a reference
  that moved (a reference rule is shared by every act of that reader), each either a more faithful reading (migrate
  the references to moved ids) or a regression (fix the rule); a page that loses words (cover, contents,
  other-language index expected; a section of the norm is a reader error), a finding, a stale review.
- When the loop itself reports something that cannot be (`entities=0` in `check_data`, every file failing the same
  way), fix the loop first: a broken check that passes is worse than no check.
- Write in the session log what each loop run found and what was fixed.

## Done

A norm is loaded when the verification loop reports PASS with every difference explained, sampled parts read like
the source, it is committed, and `verify_norms.py --db` after `moqui-seed-reload` shows it in the database with 0
orphan items and 0 dangling references.
