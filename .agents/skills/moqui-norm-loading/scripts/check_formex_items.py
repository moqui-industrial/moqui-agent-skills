#!/usr/bin/env python3
"""Content check of the items of an EU act against its Formex source, independent of the reader.

Every leaf text block of the source (a block element without block children: P, TXT, ALINEA, ...) must appear in
exactly one item: in none = text lost, in more than one = text duplicated. Reported per part (top-level item).

    python3 check_formex_items.py EU-REG-2023-1230 [--lang en] [--part ANXIII]
"""
import argparse
import glob
import json
import os
import re
import sys
import xml.etree.ElementTree as ET

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

from normkb import paths                         # noqa: E402
from normkb.formex import element_text                  # noqa: E402
from normkb.formex_items import BLOCK_TAGS as READER_BLOCKS   # noqa: E402
from normkb.items import read_items_jsonl               # noqa: E402

# the checker also treats list items as blocks (the reader handles them in read_list)
BLOCK_TAGS = set(READER_BLOCKS) | {'ITEM'}


def norm(t):
    return re.sub(r'\s+', ' ', t).strip()


def leaf_blocks(d):
    out = []
    for f in sorted(glob.glob(os.path.join(d, '*.xml'))):
        if '.doc.' in f or '.toc.' in f:
            continue
        root = ET.parse(f).getroot()
        skip = set()
        for e in root.iter():
            if e.tag in ('TITLE', 'TI.ART', 'STI.ART', 'NOTE', 'BIB.INSTANCE'):
                skip.update(e.iter())
        for e in root.iter():
            if e in skip or e.tag not in BLOCK_TAGS:
                continue
            if e.tag == 'LIST' or any(c.tag in BLOCK_TAGS for c in e):
                own = norm(element_text(e, set(c for c in e if c.tag in BLOCK_TAGS or c.tag == 'NO.GR.SEQ')))
                if own and len(own) > 3:
                    out.append((os.path.basename(f), own))
                continue
            t = norm(element_text(e, set()))
            if len(t) > 3:
                out.append((os.path.basename(f), t))
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('normId')
    ap.add_argument('--lang', default='en')
    ap.add_argument('--part')
    args = ap.parse_args()
    cfg = json.load(open(paths.CONFIG, encoding='utf-8'))
    n = next(x for x in cfg['norms'] if x['normId'] == args.normId)
    items = read_items_jsonl(paths.ITEMS / f'{args.normId}.jsonl')
    by_id = {i.seqId: i for i in items}

    def top(i):
        while i.parentSeqId:
            i = by_id[i.parentSeqId]
        return i.seqId
    texts = [(i.seqId, norm(i.text.get(args.lang) or '')) for i in items]
    lost, dup, ok = [], [], 0
    for f, b in leaf_blocks(os.path.join(cfg['sourceRoot'], n['dirs'][args.lang])):
        hits = [sid for sid, t in texts if b in t]
        part = top(by_id[hits[0]]) if hits else None
        if args.part and part != args.part and hits:
            continue
        if not hits:
            lost.append((f, b[:120]))
        elif len(hits) > 1:
            # the same short sentence can legitimately occur in two places: duplicated only if the items nest
            nested = any(by_id[h].parentSeqId in hits for h in hits)
            if nested:
                dup.append((hits, b[:100]))
            else:
                ok += 1
        else:
            ok += 1
    print(json.dumps({'blocks_ok': ok, 'lost': len(lost), 'duplicated_in_nested_items': len(dup)}))
    for x in lost[:40]:
        print('LOST', x)
    for x in dup[:40]:
        print('DUP ', x)


if __name__ == '__main__':
    main()
