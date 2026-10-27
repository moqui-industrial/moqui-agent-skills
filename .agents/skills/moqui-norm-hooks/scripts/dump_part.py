#!/usr/bin/env python3
"""Items of the parts of a norm with the concepts already linked and the findings of check_hooks.py, for reading a
part during a hook pass (norm-hooks skill).

    python3 dump_part.py ISO-12100-2010 I 6.3 6.4            # all items of the parts
    python3 dump_part.py ISO-12100-2010 I 6.3 --findings     # only the items with findings
    python3 dump_part.py ISO-12100-2010 I --roots            # the top-level items (the parts of the whole norm)
"""
import argparse
import re
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent.parent / 'moqui-norm-loading' / 'scripts'))
sys.path.insert(0, str(HERE))

from normkb import paths                    # noqa: E402
from normkb.items import read_items_jsonl   # noqa: E402
import check_hooks                           # noqa: E402


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('normId')
    ap.add_argument('alias')
    ap.add_argument('parts', nargs='*')
    ap.add_argument('--findings', action='store_true')
    ap.add_argument('--roots', action='store_true')
    ap.add_argument('--width', type=int, default=240)
    a = ap.parse_args()
    items = read_items_jsonl(paths.ITEMS / f'{a.normId}.jsonl')
    if a.roots:
        print(' '.join(i.seqId for i in items if not i.parentSeqId))
        return 0
    by_id = {i.seqId: i for i in items}
    _, _, concepts, _, _, _, _, _ = check_hooks.load(a.normId, a.alias)
    links = {}
    for c in concepts.values():
        for ref, role in c.get('clauses', []):
            if ref.startswith(a.alias + '@'):
                links.setdefault(ref.split('@', 1)[1], []).append(f"{c['key']}/{role}")
    out = subprocess.run([sys.executable, str(HERE / 'check_hooks.py'), a.normId, *a.parts, '--alias', a.alias],
                         capture_output=True, text=True).stdout
    found = {}
    for line in out.splitlines():
        p = line.split('\t')
        if len(p) >= 2:
            found.setdefault(p[0], []).append(p[1])
    for it in items:
        if it.seqId not in a.parts and not set(check_hooks.ancestors(it.seqId, by_id)) & set(a.parts):
            continue
        if a.findings and it.seqId not in found:
            continue
        text = (it.title.get('en') or '') + ' | ' + re.sub(r'\s+', ' ', it.text.get('en') or '')
        print(f'{it.seqId} [{it.type[3:]}] {text[:a.width]}')
        if it.seqId in links:
            print('    LINK', ' '.join(links[it.seqId]))
        if it.seqId in found:
            print('    FIND', ' '.join(found[it.seqId]))
    return 0


if __name__ == '__main__':
    sys.exit(main())
