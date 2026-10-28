#!/usr/bin/env python3
"""Propose the hooks (vocabulary records) of each article of a bill: categories, features, feature groups, purposes.

    python3 -I hook_candidates.py bom.json --out hooks.json [--top 5] [--only-digital]

For each article the search index of the norms is queried with the article description (target=hooks): the result is a
ranked list of candidate hook records with their concept, which the agent reviews with the user. Nothing is written to
the database. Articles that look like passive material (terminals, ducts, rails, fuses, bars) are marked "passive" and
get no query unless --all is given: they carry no digital element and no norm function, but they stay in the bill.
The proposal is a starting point, never a classification: a hook is accepted only when the item it points to (read
with get_norm_tree) describes the article, and the datasheet confirms it.

Vendor descriptions ("CPU 1514SP-2 PN", "SCALANCE XB208") do not share words with the norms and give poor candidates:
first state what each article is in the norms' language, from the order code and the datasheet, in the field "kind" of
the row ("programmable logic controller", "managed network switch", "variable speed drive with Ethernet interface"),
then run this script: the kind is queried instead of the description.
"""
import argparse
import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from moqui_client import Moqui  # noqa: E402

PASSIVE = re.compile(r'(?i)\b(terminal|klemme|duct|kanal|din rail|rail|bar|barra|fuse holder|fuse|end bracket|'
                     r'cross-connect|marker|label|cable tie|gland|plate|cover|filter|bracket|jumper)\b')
HOOK_ID = ('productCategoryId', 'productFeatureId', 'productFeatureGroupId', 'enumId')


def candidates(m, text, top):
    res = m.search(text, target='hooks', page_size=top)
    out = []
    for d in res.get('documentList', []):
        hid = next((d[k] for k in HOOK_ID if d.get(k)), None)
        out.append({'hookType': d.get('_type'), 'hookId': hid,
                    'name': d.get('categoryName') or d.get('description'),
                    'concepts': [c.get('key') for c in (d.get('concepts') or [])][:3]})
    return out


def main():
    ap = argparse.ArgumentParser(description=__doc__.split('\n')[0])
    ap.add_argument('bom')
    ap.add_argument('--out', required=True)
    ap.add_argument('--top', type=int, default=5)
    ap.add_argument('--all', action='store_true', help='query passive articles too')
    a = ap.parse_args()
    m, rows = Moqui(), []
    for art in json.load(open(a.bom, encoding='utf-8')):
        text = ' '.join(x for x in (art.get('description'), art.get('description2')) if x)
        query = art.get('kind') or text
        passive = bool(PASSIVE.search(text)) and not a.all and not art.get('kind')
        row = {'partNo': art['partNo'], 'manufacturer': art.get('manufacturer'), 'description': text,
               'quantity': art.get('quantity'), 'tags': art.get('tags'), 'passive': passive,
               'kind': art.get('kind'), 'candidates': [] if passive else candidates(m, query, a.top)}
        rows.append(row)
        print(f"{'-' if passive else ('k' if art.get('kind') else '+')} {art['partNo'][:28]:28} {(art.get('kind') or text)[:50]:50} "
              + '; '.join(f"{c['hookId']}" for c in row['candidates'][:3]))
    json.dump(rows, open(a.out, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    nokind = sum(1 for r in rows if not r['passive'] and not r['kind'])
    if nokind:
        print(f'# {nokind} articles queried by vendor description: add "kind" to them for usable candidates', file=sys.stderr)
    print(f'# {sum(not r["passive"] for r in rows)} articles queried, {sum(r["passive"] for r in rows)} passive; '
          f'written {a.out}', file=sys.stderr)


if __name__ == '__main__':
    main()
