#!/usr/bin/env python3
"""Build the Agreement seed data of one norm (all its configured language editions): read the source into norm items,
extract the canonical references, check, write the items (build/norm-kb/items/) and the seeds.

    python3 build_agreement.py EU-REG-2023-1230     # data/40_Norm_<normId>_<LANG>.xml, data/39_NormStubs.xml
"""
import argparse
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

from normkb import paths                         # noqa: E402
from normkb.figures import add_figures                   # noqa: E402
from normkb.formex_items import FormexItemReader        # noqa: E402
from normkb.pdfstd import PdfStandardReader, std_references   # noqa: E402
from normkb.refs import KNOWN                           # noqa: E402
from normkb.pdf_tables import read_index, read_tables               # noqa: E402
from normkb.std_items import check_partition, nodes_to_items  # noqa: E402
from normkb.item_refs import eu_item_refs, unresolved   # noqa: E402
from normkb.items import AgreementWriter, check_items, tree_text, write_items_jsonl, write_stubs   # noqa: E402

LICENSED_NOTICE = ('Contains the text of a licensed standard: internal use only, never commit or publish '
                   '(excluded by .gitignore).')


def formex_source_chars(d):
    """Characters of the Formex text of one language (whitespace collapsed, footnotes and number tags excluded)."""
    import glob
    import xml.etree.ElementTree as ET
    total = 0
    for f in glob.glob(os.path.join(d, '*.xml')):
        if '.doc.' in f or '.toc.' in f:
            continue
        root = ET.parse(f).getroot()
        drop, parent = set(), {c: e for e in root.iter() for c in e}
        for e in root.iter():
            if e.tag in ('NOTE', 'BIB.INSTANCE', 'NO.P', 'NO.PARAG', 'NO.GR.SEQ', 'TI.ART'):
                drop.update(x for x in e.iter())
        # the tail of a dropped element is the text after it ("... Regulation (EU) 2019/1020 [note], which ..."):
        # it belongs to the parent, kept unless the parent is dropped too
        txt = ' '.join(t for e in root.iter()
                       for t in ((e.text if e not in drop else None),
                                 (e.tail if e not in drop or parent.get(e) not in drop else None)) if t)
        total += len(re.sub(r'\s+', ' ', txt).strip())
    return total


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('normId')
    ap.add_argument('--config', default=str(paths.CONFIG))
    ap.add_argument('--data-dir', default=str(paths.DATA))
    args = ap.parse_args()
    cfg = json.load(open(args.config, encoding='utf-8'))
    norm = next(n for n in cfg['norms'] if n['normId'] == args.normId)
    root = cfg['sourceRoot']
    editions = {n['normId']: list(n['dirs']) if n['reader'] == 'formex' else [n['language']] for n in cfg['norms']}
    if norm['reader'] == 'formex':
        dirs = {lg: os.path.join(root, d) for lg, d in norm['dirs'].items()}
        reader = FormexItemReader(norm['normId'], dirs, primary=list(dirs)[0])
        items = reader.read()
        langs = list(dirs)
        items = eu_item_refs(items, langs[0], norm['normId'])
        errors = check_items(items, langs)
        errors += [f'{sid}: citation "{raw}" of the act itself not resolved to an item'
                   for sid, raw in unresolved(items, norm['normId'])]
        source = ', '.join(norm['dirs'].values()) + ' (Formex 4)'
    else:
        lang = norm['language']
        langs = [lang]
        reader = PdfStandardReader(norm['normId'], os.path.join(root, norm['file']), language=lang,
                                   boilerplate=norm.get('boilerplate', []), title=norm['title'],
                                   bilingual=norm.get('bilingual', True), definitions_clause=norm.get('definitionsClause'),
                                   paragraph_gaps=norm.get('paragraphGaps', False),
                                   line_fixes=norm.get('lineFixes', []))
        nodes = std_references(reader.read(), KNOWN, lang)
        nodes = add_figures(nodes, paths.FIGURES / f'{norm["normId"]}.json', lang)
        tables = read_tables(os.path.join(root, norm['file']), [n.number for n in nodes if n.kind == 'table'],
                             'Tabella' if lang == 'it' else 'Table', pages_kept=reader.kept_pages)
        # tables printed as images, transcribed in config/tables (licensed, gitignored)
        tpath = paths.TABLES / f'{norm["normId"]}.json'
        transcribed = []
        if os.path.exists(tpath):
            from normkb.pdf_tables import words
            for t in json.load(open(tpath, encoding='utf-8'))['tables']:
                # a transcription replaces a table the PDF does not hold, or one whose grid is wrong ("override")
                if t.get('override') or not (tables.get(t['number']) or {}).get('rows'):
                    tables[t['number']] = {'header': t['header'], 'rows': t['rows'], 'pages': t['pages'],
                                           'words': words(' '.join(t['header'] + [c for r in t['rows'] for c in r]))}
                    transcribed.append(t['number'])
        indexes = {}
        for ix in norm.get('indexes', []):
            entries, notes, dropped = read_index(os.path.join(root, norm['file']), ix['pages'], ix['columns'])
            indexes[ix['annex']] = {'labels': ix['labels'], 'entries': entries, 'notes': notes, 'dropped': dropped}
        items = nodes_to_items(nodes, lang, tables, indexes)
        if norm.get('requirementSeries'):
            # citations by requirement identifier ("CR 1.1 (1)", "SR 1.1 RE 2"), within the series of standards
            from normkb.req_refs import requirement_refs
            n_req = requirement_refs(items, norm['normId'], list(norm['requirementSeries']),
                                     paths.ITEMS, norm['requirementSeries'], lang)
        errors = check_items(items, langs) + check_partition(nodes, items, lang)
        source = norm['file'] + ' (pdftotext -layout)'
    report = {'items': len(items), 'types': {}}
    if norm.get('requirementSeries'):
        report['requirementRefs'] = n_req
    for it in items:
        report['types'][it.type] = report['types'].get(it.type, 0) + 1
    if norm['reader'] == 'formex':
        for lg, d in dirs.items():
            src = formex_source_chars(d)
            got = tree_text(items, lg)
            report[f'coverage_{lg}'] = round(got / src, 3) if src else None
            if src and not 0.9 <= got / src <= 1.05:
                errors.append(f'{lg}: item texts are {got / src:.2f} of the Formex text')
    else:
        src = reader.report.get('sourceChars')
        report[f'coverage_{lang}'] = round(tree_text(items, lang) / src, 3) if src else None
        report['tocMissing'] = reader.report.get('tocMissing')
        if transcribed:
            report['transcribedTables'] = transcribed
        for k in ('languageCorrected', 'duplicateCaptions'):
            if reader.report.get(k):
                report[k] = reader.report[k]
    if errors:
        sys.exit('item errors:\n' + '\n'.join(errors[:60]))
    os.makedirs(paths.ITEMS, exist_ok=True)
    write_items_jsonl(items, paths.ITEMS / f'{norm["normId"]}.jsonl')
    stubs = {}
    for lg in langs:
        w = AgreementWriter(norm, lg, source, 'Public text.' if not norm.get('licensed') else LICENSED_NOTICE,
                            editions)
        out = os.path.join(args.data_dir, f'40_Norm_{norm["normId"]}_{lg.upper()}.xml')
        cross = os.path.join(args.data_dir, f'42_NormCrossRefs_{norm["normId"]}.xml') if lg == langs[0] else None
        r = w.write(items, out, cross)
        stubs.update(r['stubs'])
        report[f'seed_{lg}'] = {'file': os.path.basename(out), 'items': r['items'], 'assocs': r['assocs'],
                                'crossRefs': r['crossRefs']}
    report['stubs'] = write_stubs(os.path.join(args.data_dir, paths.STUBS), stubs,
                                  [n['normId'] for n in cfg['norms']])
    print(json.dumps(report, indent=1))


if __name__ == '__main__':
    main()
