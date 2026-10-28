#!/usr/bin/env python3
"""The documents a norm requires, read from the norm itself: the checklist the agent asks the user to upload.

    python3 -I norm_documents.py machinery cra             # the technical documentation lists of these norms
    python3 -I norm_documents.py --item EU-REG-2024-2847-IT:ANXII --item IEC-62443-3-2-2020-EN:4.6.14.1
    python3 -I norm_documents.py cra --markdown > documents.md

Each named list is an item of a loaded norm that enumerates documents or information; the script prints the item and
every point below it, with its id, so each request to the user cites the norm. Nothing is added to what the norm lists.
Lists (an item id is the anchor, the text comes from the database):
  machinery  EU-REG-2023-1230-IT ANXIV.A      technical documentation of machinery and related products (Annex IV part A)
  cra        EU-REG-2024-2847-IT ANXVII       content of the technical documentation (Annex VII)
  cra-user   EU-REG-2024-2847-IT ANXII        information and instructions to the user (Annex II)
  iec62443   IEC-62443-3-2-2020-EN 4.6.14.1   documentation archived with a detailed risk assessment (ZCR 5.13)
             IEC-62443-3-2-2020-EN 4.7.2.1    minimum content of the cyber security requirements specification (ZCR 6.1)
Licensed standards (IEC, ISO) are printed for internal use only.
"""
import argparse
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from moqui_client import Moqui  # noqa: E402

LISTS = {
    'machinery': [('EU-REG-2023-1230-IT', 'ANXIV.A')],
    'cra': [('EU-REG-2024-2847-IT', 'ANXVII')],
    'cra-user': [('EU-REG-2024-2847-IT', 'ANXII')],
    'iec62443': [('IEC-62443-3-2-2020-EN', '4.6.14.1'), ('IEC-62443-3-2-2020-EN', '4.7.2.1')],
}
SKIP_TYPES = {'AitNote', 'AitExample'}


def walk(m, agr, sid, depth, out, max_depth):
    d = m.tree(agr, sid)
    it = d.get('item') or {}
    out.append((depth, agr, it.get('agreementItemSeqId', sid), it.get('itemTitle') or '', (it.get('itemText') or '').replace('\n', ' ')))
    if depth >= max_depth:
        return
    for c in d.get('children', []):
        if c.get('agreementItemTypeEnumId') in SKIP_TYPES or c.get('itemType') in ('Note', 'Example'):
            continue
        walk(m, agr, c['agreementItemSeqId'], depth + 1, out, max_depth)


def main():
    ap = argparse.ArgumentParser(description=__doc__.split('\n')[0])
    ap.add_argument('lists', nargs='*', choices=sorted(LISTS) + [[]], default=[])
    ap.add_argument('--item', action='append', default=[], help='agreementId:agreementItemSeqId')
    ap.add_argument('--depth', type=int, default=4)
    ap.add_argument('--markdown', action='store_true')
    a = ap.parse_args()
    anchors = [x for name in a.lists for x in LISTS[name]] + [tuple(i.split(':', 1)) for i in a.item]
    if not anchors:
        ap.error('name a list or give --item')
    m = Moqui()
    for agr, sid in anchors:
        out = []
        walk(m, agr, sid, 0, out, a.depth)
        for depth, ag, s, title, text in out:
            line = f"{title} {text}".strip()
            if a.markdown:
                print(('#### ' if depth == 0 else '  ' * (depth - 1) + '- [ ] ') + f"{line} (`{ag}` {s})")
            else:
                print('  ' * depth + f"[{s}] {line}")
        print()


if __name__ == '__main__':
    main()
