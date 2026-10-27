"""References by requirement identifier in a series of standards that names its requirements (IEC 62443: "CR 1.1",
"SR 1.1 RE 2", "NDR 1.13 (1)", "SM-1", "FR 3"), resolved on items.

The identifiers come from the clause titles of each norm ("5.3 CR 1.1 – Human user identification ..."), and the
numbered enhancements "(1)" under the "Requirement enhancements" clause of a requirement. A cited identifier reaches
the norm's own item; an identifier the norm does not define reaches the one norm of the series that defines it
(IEC 62443-4-2 cites "SR 1.1" of IEC 62443-3-3), or the norm named just before it ("IEC 62443-3-3 SR 7.8").
"""
import os
import re

from .items import ItemRef, read_items_jsonl

ID = r'(?:CCSC|ZCR|NDR|EDR|HDR|SAR|CR|SR|FR|SVV|SUM|SM|SD|SI|DM|SG)'
TITLE_ID = re.compile(r'^(' + ID + r')([ -])(\d+(?:\.\d+)?)(?: RE (\d+))?\b')
CITE = re.compile(r'\b(' + ID + r')([ -])(\d+(?:\.\d+)?)((?: RE ?\(?\d+\)?)|(?: ?\(\d+\))+)?(?![\d.]*\d)')


def key(prefix, sep, num, re_num=None):
    return f'{prefix}{sep}{num}' + (f' RE {re_num}' if re_num else '')


def requirement_index(items, lang='en'):
    """{"CR 1.1": seqId, "CR 1.1 RE 1": seqId, "SM-1": seqId, ...} of a norm."""
    by_id = {it.seqId: it for it in items}
    idx = {}
    for it in items:
        m = TITLE_ID.match((it.title.get(lang) or '').strip())
        if m:
            idx.setdefault(key(m.group(1), m.group(2), m.group(3), m.group(4)), it.seqId)
    # enhancements "(1) Title" under "<requirement>.3 Requirement enhancements" (IEC 62443-4-2)
    for it in items:
        if it.type == 'AitPoint' and (it.number or '').isdigit() and re.match(r'^\(\d+\)', it.text.get(lang) or ''):
            clause = by_id.get(it.parentSeqId)
            req = by_id.get(clause.parentSeqId) if clause else None
            m = req and TITLE_ID.match((req.title.get(lang) or '').strip())
            if m:
                idx.setdefault(key(m.group(1), m.group(2), m.group(3), it.number), it.seqId)
    return idx


def _series_index(norm_ids, work_dir):
    out = {}
    for nid in norm_ids:
        path = os.path.join(work_dir, f'{nid}.jsonl')
        if os.path.exists(path):
            out[nid] = requirement_index(read_items_jsonl(path))
    return out


def requirement_refs(items, norm_id, series, work_dir, designations, lang='en'):
    """Add the references by requirement identifier to the items. series: the other normIds of the series;
    designations: {normId: "IEC 62443-3-3"} to read an identifier named after its norm."""
    own = requirement_index(items, lang)
    others = _series_index([n for n in series if n != norm_id], work_dir)
    n_added = 0
    for it in items:
        text = it.text.get(lang) or ''
        seen = {(r.raw, r.toNormId, r.toSeqId) for r in it.refs}
        for m in CITE.finditer(text):
            prefix, sep, num, tail = m.group(1), m.group(2), m.group(3), m.group(4) or ''
            res = re.findall(r'\d+', tail)
            before = text[max(0, m.start() - 30):m.start()]
            named = next((nid for nid, d in designations.items() if nid != norm_id and d in before), None)
            if named and named in others:
                targets = [(named, others[named])]
            elif key(prefix, sep, num) in own:
                targets = [(norm_id, own)]
            else:
                targets = [(nid, ix) for nid, ix in others.items() if key(prefix, sep, num) in ix][:1]
            for nid, ix in targets:
                for raw, k in ([(f'{key(prefix, sep, num)} ({r})' if '(' in tail else key(prefix, sep, num, r),
                                 key(prefix, sep, num, r)) for r in res] or [(key(prefix, sep, num), key(prefix, sep, num))]):
                    target = ix.get(k) or ix.get(key(prefix, sep, num))
                    if not target or (nid == norm_id and target == it.seqId):
                        continue
                    if (raw, nid, target) not in seen:
                        seen.add((raw, nid, target))
                        it.refs.append(ItemRef(raw=raw, toNormId=nid, toSeqId=target))
                        n_added += 1
    return n_added
