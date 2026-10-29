#!/usr/bin/env python3
"""Read a bill of materials exported by EPLAN (CSV of the parts list or of the device list) into one row per article.

    python3 -I eplan_bom.py QE4.CSV                    # table on stdout
    python3 -I eplan_bom.py QE4.CSV --json bom.json    # also the rows as JSON for hook_candidates.py / load_intake.py

The export is UTF-16 (or UTF-8) with ';' separators; the first row groups the columns (device, device/part), the
second holds the EPLAN property names (P_ARTICLEREF_PARTNO, P_ARTICLE_MANUFACTURER, P_FUNC_DEVICETAG_FULLNAME ...).
Descriptions are multilingual ("de_DE@...;en_US@...;"): the English text is taken, else Italian, else the first.
Rows without a part number (cable ducts placed as graphics, comments) are counted, not returned.
"""
import argparse
import collections
import csv
import io
import json
import os
import re
import sys

COLUMNS = {  # output field -> EPLAN property
    'partNo': 'P_ARTICLEREF_PARTNO', 'manufacturer': 'P_ARTICLE_MANUFACTURER', 'typeNr': 'P_ARTICLE_TYPENR',
    'orderNr': 'P_ARTICLE_ORDERNR', 'descr1': 'P_ARTICLE_DESCR1', 'descr2': 'P_ARTICLE_DESCR2',
    'productGroup': 'P_ARTICLE_PRODUCTGROUP', 'productSubGroup': 'P_ARTICLE_PRODUCTSUBGROUP',
    'supplier': 'P_ARTICLE_SUPPLIER', 'tag': 'P_FUNC_DEVICETAG_FULLNAME', 'location': 'P_DESIGNATION_FULLLOCATION',
    'plant': 'P_DESIGNATION_FULLPLANT', 'function': 'P_FUNC_TEXT_AUTOMATIC'}
LANGS = ('en_US', 'en_GB', 'it_IT')


def resolve(name):
    if os.path.isfile(name):
        return name
    clean = os.path.basename(name)
    matches = []
    for env in ('INBOX_DIR', 'UPLOADS_DIR', 'CONTENT_DIR'):
        base = os.environ.get(env)
        if not base or not os.path.isdir(base):
            continue
        direct = os.path.join(base, name.lstrip('/'))
        if os.path.isfile(direct):
            return direct
        for root, dirs, files in os.walk(base):
            dirs[:] = [d for d in dirs if d != 'temp']
            for fn in files:
                if fn == clean or fn.endswith('__' + clean):
                    p = os.path.join(root, fn)
                    matches.append((os.path.getmtime(p), p))
    if matches:
        return max(matches)[1]
    raise SystemExit(f'{name}: not found (give a path, or a name inside INBOX_DIR, UPLOADS_DIR or CONTENT_DIR)')


def read_text(path):
    path = resolve(path)
    raw = open(path, 'rb').read()
    for enc in ('utf-16', 'utf-8-sig', 'cp1252'):
        try:
            text = raw.decode(enc)
            if ';' in text[:2000]:
                return text
        except UnicodeDecodeError:
            continue
    raise SystemExit(f'{path}: not a ; separated text file in UTF-16, UTF-8 or cp1252')


def pick_language(value):
    parts = dict(p.split('@', 1) for p in value.split(';') if '@' in p)
    for lang in LANGS:
        if parts.get(lang, '').strip():
            return parts[lang].strip()
    first = next((v.strip() for v in parts.values() if v.strip()), value)
    return re.sub(r'^\{\{|\}\}$', '', first.strip()).strip()


def read_bom(path):
    rows = list(csv.reader(io.StringIO(read_text(path)), delimiter=';'))
    header_row = next((i for i, r in enumerate(rows[:5]) if any(c.startswith('P_') for c in r)), None)
    if header_row is None:
        raise SystemExit(f'{path}: no EPLAN property header (P_...) in the first rows')
    head = rows[header_row]
    ix = {k: head.index(v) for k, v in COLUMNS.items() if v in head}
    if 'partNo' not in ix:
        raise SystemExit(f'{path}: column P_ARTICLEREF_PARTNO missing; export the parts list with article data')
    get = lambda r, k: (r[ix[k]].strip() if k in ix and ix[k] < len(r) else '')
    articles, skipped = collections.OrderedDict(), 0
    for r in rows[header_row + 1:]:
        pn = get(r, 'partNo')
        if not pn:
            skipped += 1
            continue
        a = articles.get(pn)
        if a is None:
            a = articles[pn] = {'partNo': pn, 'manufacturer': get(r, 'manufacturer'), 'typeNr': get(r, 'typeNr'),
                                'orderNr': get(r, 'orderNr'), 'description': pick_language(get(r, 'descr1')),
                                'description2': pick_language(get(r, 'descr2')), 'productGroup':
                                f"{get(r, 'productGroup')}/{get(r, 'productSubGroup')}".strip('/'),
                                'quantity': 0, 'tags': [], 'locations': set(), 'functions': set()}
        a['quantity'] += 1
        if get(r, 'tag'):
            a['tags'].append(get(r, 'tag'))
        for k, dest in (('location', 'locations'), ('function', 'functions')):
            if get(r, k):
                a[dest].add(get(r, k))
    out = []
    for a in articles.values():
        a['tags'] = sorted(set(a['tags']))
        a['locations'], a['functions'] = sorted(a['locations']), sorted(a['functions'])[:10]
        out.append(a)
    return out, skipped


def main():
    ap = argparse.ArgumentParser(description=__doc__.split('\n')[0])
    ap.add_argument('csv')
    ap.add_argument('--json', help='write the articles to this JSON file')
    a = ap.parse_args()
    arts, skipped = read_bom(a.csv)
    print(f'# {len(arts)} articles, {sum(x["quantity"] for x in arts)} placements, {skipped} rows without part number')
    for x in arts:
        print(f"{x['quantity']:4} {x['manufacturer'][:6]:6} {x['partNo'][:28]:28} {x['description'][:60]:60} "
              f"{', '.join(x['tags'][:3])}{' ...' if len(x['tags']) > 3 else ''}")
    if a.json:
        json.dump(arts, open(a.json, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
        print(f'# written {a.json}', file=sys.stderr)


if __name__ == '__main__':
    main()
