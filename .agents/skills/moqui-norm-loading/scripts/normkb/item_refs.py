"""Canonical references of an EU act, resolved on norm items (AgreementAssoc rows, PLAN-NORMS-AGREEMENT.md N4).

The citation patterns are those of refs.py (proven on the norm graphs); here they resolve to item ids. A reference is
attached to the item whose own text (or title) contains it, so it is as precise as the capoverso.
"""
import os
import re

from .items import ItemRef, read_items_jsonl
from .refs import (EU_EXTERNAL, KNOWN, OF_OTHER_ACT, P_ANX, P_ART, P_PART_OF_ANX, P_POINT_OF_ANX, P_POINT_OF_ART,
                   STD_EXTERNAL, is_correlation_table)


class ItemIndex:
    def __init__(self, items):
        self.by_id = {i.seqId: i for i in items}
        self.children = {}
        for i in items:
            self.children.setdefault(i.parentSeqId, []).append(i)

    def descendants(self, sid):
        out = []
        seen = {sid}
        stack = list(self.children.get(sid, []))
        while stack:
            x = stack.pop(0)
            if x.seqId in seen:
                raise ValueError(f'cycle or duplicate id at {x.seqId}')
            seen.add(x.seqId)
            out.append(x)
            stack[0:0] = self.children.get(x.seqId, [])
        return out

    def find_number(self, root, number, types=None):
        """First item under root (document order) with this number."""
        for x in self.descendants(root):
            if x.number == number and (types is None or x.type in types):
                return x.seqId
        return None

    def article(self, art, par=None, pt=None):
        a = f'ART{art}'
        if a not in self.by_id:
            return None
        base = a
        if par:
            p = f'{a}.{par}'
            if p in self.by_id:
                base = p
            elif not pt:
                return a
        if pt:
            return self.find_number(base, pt, ('AitPoint', 'AitSubPoint')) or base
        return base

    def annex(self, anx, part=None, num=None):
        a = f'ANX{anx}'
        if a not in self.by_id:
            return None
        base = f'{a}.{part}' if part and f'{a}.{part}' in self.by_id else a
        if num:
            return self.find_number(base, num, ('AitSection',)) or self.find_number(base, num) or \
                (self.find_number(a, num) if base != a else None) or base
        return base


_LOADED = {}


def loaded_index(norm_id):
    """Item index of another norm already built (build/norm-kb/items), to resolve citations of its partitions."""
    if norm_id not in _LOADED:
        from normkb import paths
        path = paths.ITEMS / f'{norm_id}.jsonl'
        _LOADED[norm_id] = ItemIndex(read_items_jsonl(path)) if os.path.exists(path) else None
    return _LOADED[norm_id]


def eu_item_refs(items, lang, norm_id):
    idx = ItemIndex(items)
    skip = set()
    for i in items:
        if i.type == 'AitAnnex':
            class _A:      # is_correlation_table reads title / text dictionaries
                title = i.title
                text = {lang: ' '.join((x.text.get(lang) or '') for x in idx.descendants(i.seqId)[:3])}
            if is_correlation_table(_A, lang):
                skip.add(i.seqId)
                skip.update(x.seqId for x in idx.descendants(i.seqId))
    for it in items:
        it.refs = []
        if it.seqId in skip:
            continue
        text = (it.title.get(lang) or '') + '\n' + (it.text.get(lang) or '')
        seen = set()

        def add(raw, target=None, norm=None, external=None):
            raw = re.sub(r'\s+', ' ', raw.strip())
            key = (raw, target, norm, external)
            if key in seen or (target == it.seqId and (norm or norm_id) == norm_id):
                return
            seen.add(key)
            it.refs.append(ItemRef(raw=raw, toNormId=norm if norm else (None if external else norm_id),
                                   toSeqId=target, external=external))

        def other_act(m, annex_points=None):
            t = re.match(r'\s+(TFEU|TEU|TFUE|TUE)\b', text[m.end():m.end() + 8])
            if t:
                # "Article 218 TFEU": a partition of the Treaty named by its abbreviation
                add(m.group(0).strip() + ' ' + t.group(1), None, None, external=t.group(1))
                return True
            if re.match(r'\s+thereof\b', text[m.end():m.end() + 12]):
                # "Article 114 thereof": a partition of the act named just before
                before = [x for x in list(EU_EXTERNAL.finditer(text[:m.start()])) +
                          list(re.finditer(r'the Treaty on (?:the Functioning of )?(?:the )?European Union',
                                           text[:m.start()]))]
                if before:
                    act = re.sub(r'\s+', ' ', max(before, key=lambda x: x.start()).group(0))
                    add(m.group(0).strip() + ' of ' + act, None, None, external=act)
                    return True
            tail = text[m.end():m.end() + 120]
            # an annex belongs to its act with "to" as well ("Annex III to that Regulation")
            o = OF_OTHER_ACT.match(re.sub(r'^(,?\s+)to\s', r'\1of ', tail) if m.group(0).lstrip().startswith(
                ('Annex', 'point', 'section')) or ' of Annex' in m.group(0) else tail)
            if not o:
                return False
            act = re.sub(r'\s+', ' ', o.group(1))
            if re.match(r'that\s+(Regulation|Directive|Decision)', act):
                # "that Regulation": the act of that kind named last before the citation
                kind = act.split()[1]
                named = [x for x in EU_EXTERNAL.finditer(text[:m.start()]) if x.group(0).startswith(kind)]
                act = re.sub(r'\s+', ' ', named[-1].group(0)) if named else act
            if re.match(r'(that|this)\s', act):
                act_known = None
            else:
                act_known = next((nid for p, nid in KNOWN if p.search(act)), None)
            if act_known == norm_id:
                return False      # "Annex III of Regulation (EU) 2023/1230" in that Regulation: its own partition
            raw = m.group(0).strip() + ' of ' + act
            other = loaded_index(act_known) if act_known and act_known != norm_id else None
            if other and annex_points is not None:
                # "sections 1.1.9 and 1.2.1 of Annex III to that Regulation": the sections of the loaded act
                for num in annex_points[1]:
                    add(f'point {num} of Annex {annex_points[0]} of {act}', other.annex(annex_points[0], None, num),
                        act_known)
            elif act_known and act_known != norm_id:
                add(raw, None, act_known)
            elif not act_known and not re.match(r'(that|this)\s', act):
                add(raw, None, None, external=act)
            return True

        for m in P_POINT_OF_ART.finditer(text):
            if other_act(m):
                continue
            add(m.group(0), idx.article(m.group(2), m.group(3), m.group(1)))
        for m in P_ART.finditer(text):
            if other_act(m):
                continue
            art, par, pt, more = m.group(1), m.group(2), m.group(3), m.group(4)
            add(m.group(0), idx.article(art, par, pt))
            for extra in re.findall(r'(\d+)(?:\((\d+)\))?', more or ''):
                add(f'Article {extra[0]}' + (f'({extra[1]})' if extra[1] else ''), idx.article(extra[0], extra[1] or None))
        points, covered = [], []
        for m in P_POINT_OF_ANX.finditer(text):
            points.append(m.span())
            if other_act(m, (m.group(3), re.findall(r'\d+(?:\.\d+)*', m.group(0).split(' of ')[0]))):
                covered.append(m.span())      # its "Annex III" is the other act's annex
                continue
            part, anx = m.group(2), m.group(3)
            for num in re.findall(r'\d+(?:\.\d+)*', m.group(0).split(' of ')[0]):
                add(f'point {num} of ' + (f'Part {part} of ' if part else '') + f'Annex {anx}',
                    idx.annex(anx, part, num))
        for m in P_PART_OF_ANX.finditer(text):
            if any(a <= m.start() < b for a, b in points):
                continue      # "point 1.1 of Part B of Annex III": the point phrase holds it
            if other_act(m):
                covered.append(m.span())
                continue
            part, num, letter, anx = m.group(1), m.group(2), m.group(3), m.group(4)
            target = idx.annex(anx, part)
            if target and num:
                pt = idx.find_number(target, num, ('AitPoint',)) or target
                target = (idx.find_number(pt, letter) or pt) if letter and pt != target else pt
            add(m.group(0), target)
            covered.append(m.span())
        for m in P_ANX.finditer(text):
            if any(a <= m.start() < b for a, b in covered):
                continue
            if other_act(m):
                continue
            add(m.group(0), idx.annex(m.group(1), m.group(2), m.group(3)))
        for m in EU_EXTERNAL.finditer(text):
            known = next((nid for p, nid in KNOWN if p.search(m.group(0))), None)
            if known == norm_id:
                continue
            if known:
                add(m.group(0), None, known)
            else:
                add(m.group(0), None, None, external=re.sub(r'\s+', ' ', m.group(0)))
        for m in STD_EXTERNAL.finditer(text):
            known = next((nid for p, nid in KNOWN if p.search(m.group(0))), None)
            if known:
                add(m.group(0), None, known)
            else:
                add(m.group(0), None, None, external=re.sub(r'\s+', ' ', m.group(0)))
    return items


def unresolved(items, norm_id):
    """Citations of the act itself that did not resolve to an item: the quality signal of the reader."""
    return [(i.seqId, r.raw) for i in items for r in i.refs if r.toNormId == norm_id and not r.toSeqId]
