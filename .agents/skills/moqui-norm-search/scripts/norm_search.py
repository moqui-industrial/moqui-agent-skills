#!/usr/bin/env python3
"""Norm references of a classified product, from the search documents of moqui-compliance (REST /rest/s1/compliance),
printed compactly for reading: per hook its concepts (names, broader, related) and the norm items with role, path,
other editions and associations; or a full-text search over the item or hook documents.

    norm_search.py product --category CMP_PC_SUPPLY_DISCONNECTING_DEVICE --purpose CmpDepEmergencyStop
    norm_search.py product --product DEMO_PLC --text          # the hooks of a product (categories, features)
    norm_search.py search 'emergency stop' --target hooks     # which hook records a description matches
    norm_search.py search 'concepts.key:"fn-emergency-stop" AND locale:it'
    norm_search.py product --feature CMP_PF_SIL_3 --json      # the documents as returned
    norm_search.py tree IEC-62443-3-2-2020-EN 4.4.5 --depth 2  # an item in its tree; no item: table of contents
    norm_search.py refs EU-REG-2023-1230-EN ANXIII.B.1.2.1    # citations, concepts, associations, editions

env MOQUI_URL (default http://localhost:8080), MOQUI_AUTH (user:password, default john.doe:moqui).
"""
import argparse
import base64
import json
import os
import sys
import urllib.parse
import urllib.request

URL = os.environ.get('MOQUI_URL', 'http://localhost:8080').rstrip('/') + '/rest/s1/compliance/'
AUTH = base64.b64encode(os.environ.get('MOQUI_AUTH', 'john.doe:moqui').encode()).decode()


def call(path, params):
    q = urllib.parse.urlencode([(k, v) for k, vs in params.items() for v in (vs if isinstance(vs, list) else [vs])
                                if v is not None])
    req = urllib.request.Request(URL + path + '?' + q, headers={'Authorization': 'Basic ' + AUTH})
    try:
        with urllib.request.urlopen(req, timeout=300) as r:
            return json.load(r)
    except urllib.error.HTTPError as e:
        sys.exit(f'{e.code} {e.read().decode(errors="replace")[:500]}')


def cut(s, n):
    s = ' '.join((s or '').split())
    return s if len(s) <= n else s[:n - 1] + '…'


def item_line(it, text):
    eds = ','.join(o['locale'] or o['agreementId'] for o in it.get('otherEditions') or [])
    role = f"{it['role']:9} " if it.get('role') else ''
    out = [f"    {role}{it['agreementId']} {it['agreementItemSeqId']}  {cut(it.get('itemTitle'), 50)}"
           f"{'  [' + eds + ']' if eds else ''}",
           f"              {cut(it.get('path'), 110)}"]
    if text and it.get('itemText'):
        out.append(f"              \"{cut(it['itemText'], 300)}\"")
    for a in it.get('associations') or []:
        out.append(f"              -> {a['kind']} {a['direction']} {a['weight']} {a['agreementId']} {a['agreementItemSeqId']}"
                   f": {cut(a.get('evidence'), 90)}")
    return out


def product(a):
    d = call('norms', {'productId': a.product, 'productCategoryIdList': a.category, 'productFeatureIdList': a.feature,
                       'productFeatureGroupIdList': a.group, 'purposeEnumIdList': a.purpose,
                       'withText': 'true' if a.text or a.json else 'false'})
    if a.json:
        print(json.dumps(d, ensure_ascii=False, indent=1))
        return
    print('norms:', ', '.join(d.get('normIdList') or []) or 'none')
    for h in d.get('hookList') or []:
        print(f"\n{h['hookType']} {h['hookId']}: {h.get('categoryName') or h.get('description')}  ({h.get('itemCount')} items)")
        for c in h.get('concepts') or []:
            labels = ' / '.join(f'{k}: {v}' for k, v in (c.get('labels') or {}).items())
            print(f"  concept {c['key']} [{c.get('scheme')}] {labels}")
            if c.get('description'):
                print(f"    {cut(c['description'], 200)}")
            for rel in ('broader', 'narrower', 'related'):
                if c.get(rel):
                    print(f"    {rel}: " + '; '.join(f"{b['key']} ({hook_of(b)})" for b in c[rel]))
            for it in c.get('items') or []:
                print('\n'.join(item_line(it, a.text)))


def hook_of(b):
    for k in ('productCategoryId', 'productFeatureId', 'productFeatureGroupId', 'enumId'):
        if b.get(k):
            return b[k]
    return '-'


def search(a):
    d = call('search', {'queryString': a.query, 'target': a.target, 'pageSize': a.size, 'pageIndex': a.page})
    if a.json:
        print(json.dumps(d, ensure_ascii=False, indent=1))
        return
    print(f"{d.get('documentListCount')} documents")
    for x in d.get('documentList') or []:
        t = x.get('_type')
        if t == 'CmpNormItem':
            concepts = ', '.join(f"{c['key']}({c.get('role')})" for c in x.get('concepts') or [])
            print('\n'.join(item_line(x, a.text)) + (f"\n              concepts: {concepts}" if concepts else ''))
        else:
            hid = hook_of(x)
            print(f"  {t} {hid}: {x.get('categoryName') or x.get('description')}  ({x.get('itemCount')} items; "
                  f"norms {', '.join(x.get('norms') or [])})")


def tree(a):
    d = call('tree', {'agreementId': a.agreement, 'agreementItemSeqId': a.item, 'depth': a.depth,
                      'withText': 'true' if a.text else 'false'})
    if a.json:
        print(json.dumps(d, ensure_ascii=False, indent=1))
        return
    ag = d.get('agreement') or {}
    print(f"{ag.get('agreementId')} {ag.get('title') or ''}")
    for x in d.get('ancestors') or []:
        print(f"  > {x.get('itemNumber') or x['agreementItemSeqId']} {x.get('itemTitle') or ''}")
    if d.get('item'):
        it = d['item']
        print(f"  * {it['agreementItemSeqId']} {it.get('itemTitle') or ''}" + (f"\n      \"{cut(it.get('itemText'), 400)}\"" if a.text and it.get('itemText') else ''))

    def show(children, level):
        for c in children or []:
            more = f" (+{c['childCount']})" if c.get('childCount') else ''
            print(f"{'    ' * level}- {c['agreementItemSeqId']} [{c.get('itemType')}] {c.get('itemTitle') or ''}{more}" +
                  (f": {cut(c.get('itemText'), 160)}" if a.text and c.get('itemText') else ''))
            show(c.get('children'), level + 1)
    show(d.get('children'), 1)
    if d.get('truncated'):
        print('  ... truncated (maxItems)')


def refs(a):
    d = call('references', {'agreementId': a.agreement, 'agreementItemSeqId': a.item,
                            'includeChildren': 'true' if a.children else 'false'})
    if a.json:
        print(json.dumps(d, ensure_ascii=False, indent=1))
        return
    for it in d.get('itemList') or []:
        print(f"{it['agreementId']} {it['agreementItemSeqId']} {it.get('itemTitle') or ''}")
        for r in it.get('references') or []:
            print(f"   cites {r['toAgreementId']} {r.get('toAgreementItemSeqId') or ''} \"{r.get('assocText')}\" {cut(r.get('toTitle'), 60)}")
        for r in it.get('citedBy') or []:
            print(f"   cited by {r['agreementId']} {r['agreementItemSeqId']} {cut(r.get('title'), 60)}")
        for c in it.get('concepts') or []:
            print(f"   concept {c.get('key')} ({c.get('role')}) {c.get('label')} -> {hook_of(c)}")
        for x in it.get('associations') or []:
            print(f"   -> {x['kind']} {x['direction']} {x['weight']} {x['agreementId']} {x['agreementItemSeqId']}: {cut(x.get('evidence'), 90)}")
        for e in it.get('otherEditions') or []:
            print(f"   edition {e['agreementId']} {e.get('itemTitle') or ''}")


def main():
    ap = argparse.ArgumentParser(description=__doc__.split('\n')[0])
    sub = ap.add_subparsers(dest='cmd', required=True)
    p = sub.add_parser('product', help='norm references of hook records or of a classified product')
    p.add_argument('--product')
    p.add_argument('--category', action='append')
    p.add_argument('--feature', action='append')
    p.add_argument('--group', action='append')
    p.add_argument('--purpose', action='append')
    p.add_argument('--text', action='store_true', help='print the item texts (shortened)')
    p.add_argument('--json', action='store_true')
    s = sub.add_parser('search', help='full-text search (Lucene query string) over the search index "compliance"')
    s.add_argument('query')
    s.add_argument('--target', default='items', help='items, hooks, or a document id (CmpHookCategory, ...)')
    s.add_argument('--size', type=int, default=20)
    s.add_argument('--page', type=int, default=0)
    s.add_argument('--text', action='store_true')
    s.add_argument('--json', action='store_true')
    t = sub.add_parser('tree', help='an item with its ancestors and children, or the table of contents')
    t.add_argument('agreement', help='norm edition, e.g. IEC-62443-3-2-2020-EN')
    t.add_argument('item', nargs='?')
    t.add_argument('--depth', type=int, default=1)
    t.add_argument('--text', action='store_true')
    t.add_argument('--json', action='store_true')
    r = sub.add_parser('refs', help='citations, concepts, associations and editions of an item')
    r.add_argument('agreement')
    r.add_argument('item')
    r.add_argument('--children', action='store_true', help='also the items below it')
    r.add_argument('--json', action='store_true')
    a = ap.parse_args()
    {'product': product, 'search': search, 'tree': tree, 'refs': refs}[a.cmd](a)


if __name__ == '__main__':
    main()
