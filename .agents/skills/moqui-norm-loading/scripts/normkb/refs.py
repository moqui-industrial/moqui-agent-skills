"""Cross-reference extraction and resolution.

References are found in the primary-language text of each node. Internal references are resolved through an
address index built from the nodes of the same norm; references to other norms are normalized to a designator and,
when the norm is in the knowledge base, to its normId (resolution inside it happens when both are loaded).
"""
import re

from .ir import Reference

# norms of the knowledge base, by designator as written in other texts
KNOWN = [
    (re.compile(r'Regulation \(EU\) 2023/1230'), 'EU-REG-2023-1230'),
    (re.compile(r'Regulation \(EU\) 2024/2847'), 'EU-REG-2024-2847'),
    # EN prefixes and a designator without the part number ("IEC 60204") resolve to the one part in the knowledge
    # base; other parts ("IEC 60204-32") stay external.
    # ISO 12100-1 and ISO 12100-2 (2003) are the parts that ISO 12100:2010 replaced: other documents
    (re.compile(r'\b(?:EN\s+)?(?:ISO|EN)\s+12100\b(?!-\d)'), 'ISO-12100-2010'),
    (re.compile(r'\b(?:IEC|EN)\s+60204(?:-1)?\b(?!-\d)'), 'IEC-60204-1-2006'),
    (re.compile(r'\b(?:EN\s+)?(?:ISO|EN)\s+13849(?:-1)?\b(?!-\d)'), 'ISO-13849-1-2015'),
    (re.compile(r'\b(?:IEC|EN)\s+62061\b'), 'IEC-62061-2021'),
    (re.compile(r'\bIEC(?:/TR| TR)? 62443-3-1\b'), 'IEC-TR-62443-3-1-2009'),
    (re.compile(r'\bIEC 62443-3-2\b'), 'IEC-62443-3-2-2020'),
    (re.compile(r'\bIEC 62443-3-3\b'), 'IEC-62443-3-3-2013'),
    (re.compile(r'\bIEC 62443-4-1\b'), 'IEC-62443-4-1-2018'),
    (re.compile(r'\bIEC 62443-4-2\b'), 'IEC-62443-4-2-2019'),
]

# years of the edition loaded (IEC year and EN year): a dated citation of another year is another document
EDITION_YEARS = {'ISO-12100-2010': {'2010'}, 'IEC-60204-1-2006': {'2005', '2006'}, 'ISO-13849-1-2015': {'2015'},
                 'IEC-62061-2021': {'2021'}, 'IEC-62443-3-3-2013': {'2013', '2019'}, 'IEC-62443-4-1-2018': {'2018'},
                 'IEC-62443-4-2-2019': {'2019'},
                 'IEC-62443-3-2-2020': {'2020'}, 'IEC-TR-62443-3-1-2009': {'2009'}}


def known_norm(raw, patterns=None):
    """normId of the norm of the knowledge base a citation names, None when it names another document: an
    undated citation is the edition loaded, a dated one only when the year is the year of that edition."""
    nid = next((nid for p, nid in (patterns or KNOWN) if p.search(raw)), None)
    year = re.search(r':((?:19|20)\d{2})\b', raw)
    if nid and year and nid in EDITION_YEARS and year.group(1) not in EDITION_YEARS[nid]:
        return None
    return nid

EU_EXTERNAL = re.compile(
    r'\b(?:Regulation|Directive|Decision)\s+(?:\((?:EU|EC|EEC|Euratom)\)\s+)?(?:No\s+)?\d{1,4}/\d{1,4}(?:/(?:EU|EC|EEC))?')
STD_EXTERNAL = re.compile(r'\b(?:EN\s+)?(?:ISO/IEC|ISO/TR|ISO/TS|IEC/TS|IEC/TR|ISO|IEC|EN)\s+\d{3,5}(?:-\d+)*(?::\d{4})?')

ROMAN = r'[IVXLC]+'
OF_OTHER_ACT = re.compile(r'^,?\s+of\s+(the Treaty on (?:the Functioning of )?(?:the )?European Union|the Treaty|Regulation\s+\((?:EU|EC|EEC)\)\s+(?:No\s+)?\d+/\d+|'
                          r'Directive\s+(?:\(EU\)\s+)?\d+/\d+(?:/(?:EU|EC|EEC))?|Decision\s+(?:No\s+)?\d+/\d+(?:/EC)?|'
                          r'that\s+Regulation|that\s+Directive|that\s+Decision|Implementing\s+Regulation[^,.;]*|'
                          r'Commission\s+[A-Z][^,.;]*)')
P_ART = re.compile(r'\bArticles?\s+(\d+)(?:\((\d+)\))?(?:\s*,?\s*(?:first|second|third)?\s*subparagraph)?'
                   r'(?:,?\s*points?\s*\(([a-z0-9]+)\))?((?:\s*(?:,|and|or|to)\s*\d+(?:\(\d+\))?)*)')
P_POINT_OF_ART = re.compile(r'\bpoints?\s*\(([a-z0-9]+)\)\s+of\s+Article\s+(\d+)(?:\((\d+)\))?')
P_ANX = re.compile(r'\bAnnex\s+(' + ROMAN + r')(?:,?\s+Part\s+([A-Z]))?(?:,?\s+(?:points?|sections?)\s+(\d+(?:\.\d+)*))?')
# "Part II of Annex I", "Part I, point (2)(c), of Annex I" (Regulation 2024/2847)
P_PART_OF_ANX = re.compile(r'\bPart\s+(' + ROMAN + r'|[A-Z])(?:,\s+points?\s+\((\d+)\)(?:\(([a-z])\))?,)?\s+of\s+Annex\s+('
                           + ROMAN + r')\b')
P_POINT_OF_ANX = re.compile(r'\b(?:points?|sections?)\s+(\d+(?:\.\d+)*)(?:\s*(?:,|and|to)\s*\d+(?:\.\d+)*)*'
                            r'\s+of\s+(?:Part\s+([A-Z])\s+of\s+)?Annex\s+(' + ROMAN + r')')


def build_address_index(nodes):
    """(kind, key...) -> nodeId for the partitions that the text cites."""
    idx = {}
    by_id = {n.nodeId: n for n in nodes}

    def ancestors(n):
        out = []
        while n.parentId:
            n = by_id[n.parentId]
            out.append(n)
        return out

    for n in nodes:
        if '~' in n.nodeId:
            continue
        if n.kind == 'article':
            idx[('art', n.number)] = n.nodeId
        elif n.kind == 'paragraph':
            art = by_id[n.parentId]
            idx[('art', art.number, n.number)] = n.nodeId
        elif n.kind in ('point', 'definition'):
            anc = ancestors(n)
            arts = [a for a in anc if a.kind == 'article']
            if arts and n.number:
                pars = [a for a in anc if a.kind == 'paragraph']
                key = ('art', arts[0].number, pars[0].number if pars else None, n.number)
                idx.setdefault(key, n.nodeId)
            anx = [a for a in anc if a.kind == 'annex']
            if anx and n.number:
                parts = [a for a in anc if a.kind == 'annexSection' and a.nodeId.split('.')[-1].startswith('PART_')]
                part = parts[0].number if parts else None
                idx.setdefault(('anx', anx[0].number, part, n.number), n.nodeId)
                idx.setdefault(('anx', anx[0].number, None, n.number), n.nodeId)
        elif n.kind == 'annex':
            idx[('anx', n.number)] = n.nodeId
        elif n.kind == 'annexSection' and n.number:
            anx = [a for a in ancestors(n) if a.kind == 'annex'][0]
            if n.nodeId.split('.')[-1].startswith('PART_'):
                idx[('anxpart', anx.number, n.number)] = n.nodeId
            else:
                idx.setdefault(('anx', anx.number, None, n.number), n.nodeId)
    return idx


def eu_references(nodes, primary='en'):
    """Fill Node.references for an EU act from its primary-language text."""
    idx = build_address_index(nodes)
    skip_internal = set()
    for n in nodes:
        if n.kind == 'annex' and is_correlation_table(n, primary):
            skip_internal.add(n.nodeId)
    by_id = {n.nodeId: n for n in nodes}

    def in_skipped(n):
        while n is not None:
            if n.nodeId in skip_internal:
                return True
            n = by_id.get(n.parentId) if n.parentId else None
        return False

    for n in nodes:
        text = (n.title.get(primary) or '') + '\n' + (n.text.get(primary) or '')
        if in_skipped(n):
            n.references = []
            continue
        refs = []
        seen = set()

        def add(raw, target):
            key = (raw, target)
            if key not in seen and target != n.nodeId:
                seen.add(key)
                refs.append(Reference(raw=raw, targetNormId=n.normId if target else None, targetNodeId=target))

        def other_act(m):
            o = OF_OTHER_ACT.match(text[m.end():m.end() + 120])
            if not o:
                return False
            act = re.sub(r'\s+', ' ', o.group(1))
            known = known_norm(act)
            raw = re.sub(r'\s+', ' ', m.group(0).strip()) + ' of ' + act
            if (raw, None) not in seen:
                seen.add((raw, None))
                refs.append(Reference(raw=raw, targetNormId=known if known != n.normId else None, targetNodeId=None,
                                      external=None if known else raw))
            return True

        for m in P_POINT_OF_ART.finditer(text):
            if other_act(m):
                continue
            pt, art, par = m.group(1), m.group(2), m.group(3)
            add(m.group(0), idx.get(('art', art, par, pt)) or idx.get(('art', art, par)) or idx.get(('art', art)))
        for m in P_ART.finditer(text):
            if other_act(m):
                continue
            art, par, pt, more = m.group(1), m.group(2), m.group(3), m.group(4)
            target = (idx.get(('art', art, par, pt)) if pt else None) or (idx.get(('art', art, par)) if par else None) \
                or idx.get(('art', art))
            add(m.group(0).strip(), target)
            for extra in re.findall(r'(\d+)(?:\((\d+)\))?', more or ''):
                t2 = (idx.get(('art', extra[0], extra[1])) if extra[1] else None) or idx.get(('art', extra[0]))
                add(f'Article {extra[0]}' + (f'({extra[1]})' if extra[1] else ''), t2)
        for m in P_POINT_OF_ANX.finditer(text):
            part, anx = m.group(2), m.group(3)
            nums = re.findall(r'\d+(?:\.\d+)*', m.group(0).split(' of ')[0])
            for num in nums:
                target = idx.get(('anx', anx, part, num)) or idx.get(('anx', anx, None, num)) or idx.get(('anx', anx))
                add(f'point {num} of ' + (f'Part {part} of ' if part else '') + f'Annex {anx}', target)
        for m in P_ANX.finditer(text):
            anx, part, num = m.group(1), m.group(2), m.group(3)
            target = None
            if num:
                target = idx.get(('anx', anx, part, num)) or idx.get(('anx', anx, None, num))
            if not target and part:
                target = idx.get(('anxpart', anx, part))
            target = target or idx.get(('anx', anx))
            add(m.group(0).strip(), target)
        for m in EU_EXTERNAL.finditer(text):
            raw = m.group(0)
            known = known_norm(raw)
            if known == n.normId:
                continue
            refs.append(Reference(raw=raw, targetNormId=known, targetNodeId=None,
                                  external=None if known else re.sub(r'\s+', ' ', raw)))
        for m in STD_EXTERNAL.finditer(text):
            raw = m.group(0)
            known = known_norm(raw)
            refs.append(Reference(raw=raw, targetNormId=known, targetNodeId=None,
                                  external=None if known else re.sub(r'\s+', ' ', raw)))
        n.references = refs
    return nodes


def is_correlation_table(annex, primary='en'):
    t = ((annex.title.get(primary) or '') + ' ' + (annex.text.get(primary) or '')[:300]).lower()
    return 'correlation table' in t or 'tavola di concordanza' in t


def unresolved(nodes):
    """References that look internal but did not resolve: the quality signal of a reader."""
    out = []
    for n in nodes:
        for r in n.references:
            if r.targetNormId is None and r.external is None:
                out.append((n.nodeId, r.raw))
    return out
