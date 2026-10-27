#!/usr/bin/env python3
"""The associative graph of the norms (NG_CMP_ASSOC), built from the seed data: the links written in the texts and the
associations an expert makes between partitions of different norms.

    python3 assoc.py                   # counts and a sample of every pass, nothing written
    python3 assoc.py --sample 20 --pass same-notion
    python3 assoc.py --write           # data/70_CmpAssociations.xml

Sources (in mantle-compliance): the Agreement seeds in data/ (40_ of the primary edition of each norm, 42_ cross references), the vocabulary
(data/norms/vocabulary) and the reviewed expert proposals in data/norms/associations/*.json. A vertex stands for
an AgreementItem (GraphVertex.agreementId / agreementItemSeqId); an edge has its kind (GraphEdgeType CmpGa*), a weight
(confidence 0-1), the pass that made it (CmpAssocPass) and its evidence in short (CmpAssocEvidence).

Passes (each over all loaded norms; an edge made by two passes is kept once, with both evidences):
  text                    citations written in the texts (AatReference to an item)                    CmpGaCites
  same-notion             a concept defined in two norms                                              CmpGaSameNotion
  essential-requirements  standard clauses giving conformity with essential requirements (Annex ZZ
                          tables and lists through the correlation table of Regulation 2023/1230;
                          CRA Annex I requirements and the IEC 62443 foundational requirements)      CmpGaCoversRequirement
  details                 a standard clause giving the method for a process or function a law asks   CmpGaDetails
  same-subject            requirements of two norms on the same precise product or function           CmpGaSameSubject
  derived-requirements    IEC 62443 system requirement -> component requirement -> device type       CmpGaDerivedRequirement
  design-principles       a design measure or recommendation of a standard for a requirement of a law
                          on the same product, function or characteristic                            CmpGaDetails
  mentions                an item naming a precise notion another norm defines, without a citation   CmpGaMentions
  expert                  associations proposed one by one (data/norms/associations/*.json)            any kind

The passes run in rounds until a round adds no edge (a pass may read the edges of the others).
"""
import argparse
import glob
import hashlib
import json
import random
import re
import sys
import xml.etree.ElementTree as ET
from collections import defaultdict
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent.parent / 'moqui-norm-hooks' / 'scripts'))
import vocab  # noqa: E402
from normkb import paths  # noqa: E402

DATA = paths.DATA

GRAPH = 'NG_CMP_ASSOC'
UNDIRECTED = {'CmpGaSameNotion', 'CmpGaSameSubject'}
LAWS = ('EU-REG-',)


def sid_hash(prefix, *parts):
    return prefix + hashlib.sha1('|'.join(parts).encode('utf-8')).hexdigest()[:30]


class Norms:
    """Items and references of the primary edition of every norm, from the seeds."""

    def __init__(self):
        cfg = json.loads(paths.CONFIG.read_text(encoding='utf-8'))
        self.primary = {}
        self.licensed = {n['normId'] for n in cfg['norms'] if n.get('licensed')}
        for n in cfg['norms']:
            lang = list(n['dirs'])[0] if n['reader'] == 'formex' else n['language']
            self.primary[n['normId']] = f"{n['normId']}-{lang.upper()}"
        self.items = {}            # (agreementId, seqId) -> dict
        self.refs = []             # (agreementId, seqId, toAgreementId, toSeqId, text)
        for nid, agr in self.primary.items():
            files = sorted(DATA.glob(f'40_Norm_{nid}_*.xml')) + sorted(DATA.glob(f'42_NormCrossRefs_{nid}.xml'))
            for f in files:
                for e in ET.parse(f).getroot():
                    if e.tag.endswith('.AgreementItem') and e.get('agreementId') == agr:
                        t = e.find('itemText')
                        self.items[(agr, e.get('agreementItemSeqId'))] = {
                            'parent': e.get('parentItemSeqId'), 'number': e.get('itemNumber'), 'title': e.get('itemTitle') or '',
                            'text': (t.text if t is not None else '') or '', 'type': e.get('agreementItemTypeEnumId')}
                    elif e.tag.endswith('.AgreementAssoc') and e.get('agreementAssocTypeEnumId') == 'AatReference' \
                            and e.get('agreementId') == agr and e.get('toAgreementItemSeqId'):
                        self.refs.append((agr, e.get('agreementItemSeqId'), e.get('toAgreementId'),
                                          e.get('toAgreementItemSeqId'), e.get('assocText') or ''))
        self.norm_of = {a: n for n, a in self.primary.items()}

    def has(self, agr, sid):
        return (agr, sid) in self.items

    def ancestors(self, agr, sid):
        out = []
        while (agr, sid) in self.items and self.items[(agr, sid)]['parent']:
            sid = self.items[(agr, sid)]['parent']
            out.append(sid)
        return out


class Concepts:
    """Vocabulary concepts with the items they are linked to, by role."""

    def __init__(self, norms):
        exts = sorted(glob.glob(str(paths.VOCABULARY / 'HOOKS-*.json')))
        v = vocab.Vocabulary(paths.VOCABULARY / 'VOCAB-BASE.json', paths.IR, exts)
        self.by_key = {c['key']: c for c in v.concepts}
        self.items = defaultdict(list)      # key -> [(agreementId, seqId, role)]
        for c in v.concepts:
            for ref, role in c.get('clauses', []):
                alias, sid = ref.split('@', 1)
                nid = v.aliases.get(alias)
                if nid and nid in norms.primary and norms.has(norms.primary[nid], sid):
                    self.items[c['key']].append((norms.primary[nid], sid, role))


def label(norms, agr, sid):
    """Norm, item and its title; the opening words of the text only for public acts (licensed texts stay out of the
    committed graph)."""
    it = norms.items.get((agr, sid), {})
    title = it.get('title') or ('' if norms.norm_of.get(agr) in norms.licensed else re.sub(r'\s+', ' ', it.get('text') or '')[:60])
    return f"{norms.norm_of.get(agr, agr)} {sid} {title}"[:63].strip()      # GraphVertex.label is text-short


class Edges:
    def __init__(self):
        self.edges = {}                     # (kind, from, to) -> dict

    def add(self, kind, a, b, pass_name, confidence, evidence):
        if a == b:
            return
        if kind in UNDIRECTED and b < a:
            a, b = b, a
        k = (kind, a, b)
        e = self.edges.get(k)
        if e is None:
            self.edges[k] = {'kind': kind, 'from': a, 'to': b, 'passes': [pass_name], 'confidence': confidence,
                             'evidence': [evidence]}
        else:
            if pass_name not in e['passes']:
                e['passes'].append(pass_name)
            if evidence not in e['evidence']:
                e['evidence'].append(evidence)
            e['confidence'] = max(e['confidence'], confidence)


# ---------- passes ----------

def pass_text(norms, concepts, edges):
    for agr, sid, to_agr, to_sid, text in norms.refs:
        if norms.has(to_agr, to_sid):
            edges.add('CmpGaCites', (agr, sid), (to_agr, to_sid), 'text', 1.0, f'cites "{text}"')


def pass_same_notion(norms, concepts, edges):
    """The defining items of one concept in different norms: the same notion, defined twice."""
    for key, its in concepts.items.items():
        defs = [(a, s) for a, s, r in its if r == 'd']
        c = concepts.by_key[key]
        for i, x in enumerate(defs):
            for y in defs[i + 1:]:
                if x[0] != y[0]:
                    edges.add('CmpGaSameNotion', x, y, 'same-notion', 0.9, f'both define {c["label"]} ({key})')


DIRECTIVE_TO_REG = 'EU-REG-2023-1230-EN'


def directive_section(norms, num, letters=True):
    """Annex I section of Directive 2006/42/EC (or 98/37/EC) -> item of Annex III of Regulation 2023/1230: the
    correlation table of the Regulation (Annex XXII) keeps the section numbers of Annex I in Annex III."""
    m = re.match(r'^(\d+(?:\.\d+)*)\s*(?:\(([a-z, ]+)\))?', num.strip())
    if not m:
        return []
    sec, letters, letters_ok = m.group(1), m.group(2), letters
    base = f'ANXIII.B.{sec}'
    if not norms.has(DIRECTIVE_TO_REG, base):
        return []
    if not letters or not letters_ok:
        return [base]
    out = []
    for L in re.findall(r'[a-z]', letters):
        # the point of that letter nearest to the section (1.7.4.2.pt1.spi, not a deeper i of another point)
        hit = sorted((s for (a, s), it in norms.items.items() if a == DIRECTIVE_TO_REG and s.startswith(base + '.')
                      and it['number'] == L), key=lambda s: s.count('.'))
        out += hit[:1] or [base]
    return out


def pass_essential_requirements(norms, concepts, edges):
    # Annex ZZ table rows: "1.2.1 ... Clauses 4, 5, 6" (IEC 62061 Table ZZ.1)
    for (agr, sid), it in list(norms.items.items()):
        if not re.match(r'TABZ[AZ]\.\d+\.r\d+$', sid):
            continue
        text = it['text']
        cells = [c.split(':', 1)[-1].strip() for c in text.split('; ')]
        if len(cells) < 2:
            continue
        targets = [x for part in re.split(r',\s*(?=\d)', cells[0]) for x in directive_section(norms, part)]
        clauses = re.findall(r'\b(\d+(?:\.\d+)*)\b', cells[1])
        for cl in clauses:
            if norms.has(agr, cl):
                for t in targets:
                    edges.add('CmpGaCoversRequirement', (agr, cl), (DIRECTIVE_TO_REG, t), 'essential-requirements', 0.85,
                              f'{norms.norm_of[agr]} Table ZZ: clause {cl} gives conformity with Directive Annex I {cells[0]}'
                              f' = Regulation Annex III {t[9:]} (correlation table)')
    # Annex ZZ lists: "the standard covers only the following essential requirements: - 1.5.1 ..." (IEC 60204-1)
    for (agr, sid), it in list(norms.items.items()):
        if re.match(r'ANXZZ\.p\d+\.li\d+$', sid):
            # Directive 98/37/EC: the sections kept their numbers in 2006/42/EC, the lettered points did not
            for t in directive_section(norms, it['text'].lstrip('–- ').strip(), letters=False):
                edges.add('CmpGaCoversRequirement', (agr, sid), (DIRECTIVE_TO_REG, t), 'essential-requirements', 0.7,
                          f'{norms.norm_of[agr]} Annex ZZ lists Directive Annex I {it["text"].strip("–- ")} as covered '
                          f'= Regulation Annex III {t[9:]} (whole standard)')
    # CRA Annex I part I requirements and the IEC 62443 foundational requirements related to them
    for key, c in concepts.by_key.items():
        if not key.startswith('cn-'):
            continue
        reqs = [(a, s) for a, s, r in concepts.items.get(key, []) if r == 'd' and a.startswith(LAWS)]
        for rel in c.get('related', []):
            fr = concepts.by_key.get(rel)
            if not fr or not rel.startswith('fg-fr'):
                continue
            for a, s, r in concepts.items.get(rel, []):
                if r == 'd':
                    for q in reqs:
                        edges.add('CmpGaCoversRequirement', (a, s), q, 'essential-requirements', 0.7,
                                  f'{fr["label"]} of {norms.norm_of[a]} meets the CRA essential requirement {c["label"]}')


REQUIREMENT = re.compile(r'\b(shall|must|deve|devono|dovrà|dovranno)\b', re.I)


def is_clause(norms, agr, sid):
    return norms.items[(agr, sid)]['type'] in ('AitArticle', 'AitParagraph', 'AitPoint', 'AitSubPoint', 'AitSection',
                                                 'AitAnnexPart')


def pass_details(norms, concepts, edges):
    """A process or function a law asks for (s) and the clause of a standard that defines or specifies it."""
    for key, its in concepts.items.items():
        c = concepts.by_key[key]
        if c['scheme'] not in ('process', 'function'):
            continue
        laws = [(a, s) for a, s, r in its if r == 's' and a.startswith(LAWS) and is_clause(norms, a, s)]
        # the standard defines the notion or sets a requirement on it ("shall"), not a description that names it
        stds = [(a, s, r) for a, s, r in its if not a.startswith(LAWS) and is_clause(norms, a, s) and
                (r == 'd' or (r == 's' and REQUIREMENT.search(norms.items[(a, s)]['text'])))]
        per_norm = defaultdict(list)
        for a, s, r in stds:
            per_norm[a].append((s, r))
        for a, lst in per_norm.items():
            if len(lst) > 6 or len(laws) > 6:
                continue            # a broad notion: an expert does not associate every pair
            for s, r in lst:
                for q in laws:
                    edges.add('CmpGaDetails', (a, s), q, 'details', 0.6 if r == 's' else 0.7,
                              f'{c["label"]}: required by {norms.norm_of[q[0]]} {q[1]}, '
                              f'{"defined" if r == "d" else "specified"} by {norms.norm_of[a]} {s}')


def pass_same_subject(norms, concepts, edges):
    """Requirements of two norms on the same precise product or function (few requirement items in each norm)."""
    for key, its in concepts.items.items():
        c = concepts.by_key[key]
        if c['scheme'] not in ('product', 'function', 'feature'):
            continue
        per_norm = defaultdict(list)
        for a, s, r in its:
            # requirements, not mentions: the item states what shall be done
            if r == 's' and is_clause(norms, a, s) and REQUIREMENT.search(norms.items[(a, s)]['text']):
                per_norm[a].append(s)
        if len(per_norm) < 2 or any(len(v) > 4 for v in per_norm.values()):
            continue
        norms_list = sorted(per_norm)
        for i, a in enumerate(norms_list):
            for b in norms_list[i + 1:]:
                for x in per_norm[a]:
                    for y in per_norm[b]:
                        edges.add('CmpGaSameSubject', (a, x), (b, y), 'same-subject', 0.5,
                                  f'both set requirements on {c["label"]} ({key})')


def pass_derived_requirements(norms, concepts, edges):
    """IEC 62443: a system requirement (3-3 SR x.y) and the component requirement with the same number and name
    (4-2 CR x.y); a component requirement and the device-type requirement that refines it (EDR/HDR/NDR/SAR x.y)."""
    def index(agr, prefixes):
        out = {}
        for (a, s), it in norms.items.items():
            if a != agr:
                continue
            m = re.match(r'^(' + prefixes + r') (\d+\.\d+)(?: RE (\d+))? [–-] (.+)$', it['title'])
            if m:
                out[(m.group(1), m.group(2), m.group(3))] = (s, m.group(4).strip().lower())
        return out
    sys33 = norms.primary.get('IEC-62443-3-3-2013')
    comp42 = norms.primary.get('IEC-62443-4-2-2019')
    if not (sys33 and comp42):
        return
    sr = index(sys33, 'SR')
    cr = index(comp42, 'CR|SAR|EDR|HDR|NDR')
    for (p, num, re_n), (s, title) in sr.items():
        hit = cr.get(('CR', num, re_n))
        if hit:
            same = hit[1] == title
            edges.add('CmpGaDerivedRequirement', (sys33, s), (comp42, hit[0]), 'derived-requirements', 0.95 if same else 0.8,
                      f'SR {num} of IEC 62443-3-3 and CR {num} of IEC 62443-4-2' + ('' if same else ' (titles differ)'))
    for (p, num, re_n), (s, title) in cr.items():
        if p != 'CR':
            base = cr.get(('CR', num, None))
            if base:
                edges.add('CmpGaDerivedRequirement', (comp42, base[0]), (comp42, s), 'derived-requirements', 0.9,
                          f'{p} {num} refines CR {num} for one device type')


# a design measure or recommendation: the standard says what the design should do, or the item sits under a clause of
# design measures, safeguarding or recommendations
DESIGN = re.compile(r'\b(shall|should|ought|avoid(?:ed|ing)?|recommended|preferabl[ey]|deve|devono|dovrebbe|dovrebbero|'
                    r'evitare|raccomandat[oaie])\b', re.I)
DESIGN_CLAUSE = re.compile(r'design|measure|safeguard|recommendation|guidance|protective|progettazione|misur[ae]|'
                           r'protezion[ei]|raccomandazion[ei]', re.I)


def pass_design_principles(norms, concepts, edges):
    """A design measure of a standard (ISO 12100 6.2 inherently safe design, a recommendation of IEC/TR 62443-3-1) and
    the requirement of a law on the same function or characteristic: the measure is a way to meet it. Products are
    left to same-subject (a design clause names many products in passing: engines, cabins). The law side is a
    requirement item, not a part or section heading. Few items on each side, or the notion is too broad to pair."""
    for key, its in concepts.items.items():
        c = concepts.by_key[key]
        # hazard origins and consequences, energy sources: classes of risk analysis named everywhere, not design
        # characteristics a measure is chosen for
        if c['scheme'] not in ('function', 'feature') or key.startswith(('hz', 'es-')):
            continue
        laws = [(a, s) for a, s, r in its if r == 's' and a.startswith(LAWS) and
                norms.items[(a, s)]['type'] in ('AitArticle', 'AitParagraph', 'AitPoint', 'AitSubPoint')
                and REQUIREMENT.search(norms.items[(a, s)]['text'])]
        per_norm = defaultdict(list)
        for a, s, r in its:
            if a.startswith(LAWS) or r not in ('s', 'l') or not is_clause(norms, a, s):
                continue
            titles = ' '.join(norms.items.get((a, x), {}).get('title', '') for x in [s] + norms.ancestors(a, s))
            if DESIGN.search(norms.items[(a, s)]['text']) and DESIGN_CLAUSE.search(titles):
                per_norm[a].append(s)
        if not laws or len(laws) > 4:
            continue
        for a, lst in per_norm.items():
            if len(lst) > 4:
                continue
            for s in lst:
                for q in laws:
                    edges.add('CmpGaDetails', (a, s), q, 'design-principles', 0.55,
                              f'{c["label"]}: design measure of {norms.norm_of[a]} {s} for the requirement of '
                              f'{norms.norm_of[q[0]]} {q[1]}')


MENTION_MAX = 8          # items of one norm naming the notion: more and it is a subject word, not a mention


def pass_mentions(norms, concepts, edges):
    """An item that names a notion another norm defines, without citing it: the reader of the item finds the meaning
    there. Precise notions only: defined in at most two norms, named by at most MENTION_MAX items of the mentioning
    norm, which does not define it itself."""
    for key, its in concepts.items.items():
        c = concepts.by_key[key]
        defs = [(a, s) for a, s, r in its if r == 'd']
        if not defs or len({a for a, _ in defs}) > 2 or len(its) > 100:
            continue
        per_norm = defaultdict(list)
        for a, s, r in its:
            if r in ('s', 'l') and is_clause(norms, a, s):
                per_norm[a].append(s)
        for a, lst in per_norm.items():
            if a in {x for x, _ in defs} or len(lst) > MENTION_MAX:
                continue
            for s in lst:
                for d in defs:
                    if not any(e[1] == (a, s) and e[2] == d for e in edges.edges):
                        edges.add('CmpGaMentions', (a, s), d, 'mentions', 0.4,
                                  f'names {c["label"]} ({key}), defined by {norms.norm_of[d[0]]} {d[1]}')


def pass_expert(norms, concepts, edges):
    for f in sorted(paths.ASSOCIATIONS.glob('*.json')):
        for a in json.loads(f.read_text(encoding='utf-8')).get('associations', []):
            fr, to = a['from'].split('@'), a['to'].split('@')
            x, y = (norms.primary[fr[0]], fr[1]), (norms.primary[to[0]], to[1])
            assert norms.has(*x) and norms.has(*y), a
            edges.add(a['kind'], x, y, 'expert', a.get('confidence', 0.8), a['evidence'])


PASSES = [('text', pass_text), ('same-notion', pass_same_notion), ('essential-requirements', pass_essential_requirements),
          ('details', pass_details), ('same-subject', pass_same_subject), ('derived-requirements', pass_derived_requirements),
          ('design-principles', pass_design_principles), ('mentions', pass_mentions), ('expert', pass_expert)]


def seed(norms, edges):
    out = ['<?xml version="1.0" encoding="UTF-8"?>',
           '<!-- Generated by assoc.py (skill moqui-norm-associations) from the Agreement seeds and the vocabulary. Do not edit '
           'by hand: regenerate. Associative graph of the norms: links written in the texts and associations of an '
           'expert, each with its kind, pass, confidence (weight) and evidence. -->',
           '<entity-facade-xml type="seed">',
           f'    <moqui.math.Graph graphId="{GRAPH}" graphTypeEnumId="GtDirectedMulti" name="Associative memory of the norms" '
           f'description="Links and associations between partitions of {", ".join(sorted(norms.primary))}" '
           f'loopsAllowed="N" isWeighted="Y"/>']
    vertices = sorted({v for e in edges.edges.values() for v in (e['from'], e['to'])})
    vid = {v: sid_hash('NA', *v) for v in vertices}
    q = lambda s: (s.replace('&', '&amp;').replace('"', '&quot;').replace('<', '&lt;').replace('>', '&gt;'))
    for v in vertices:
        out.append(f'    <moqui.math.GraphVertex graphVertexId="{vid[v]}" graphId="{GRAPH}" agreementId="{v[0]}" '
                   f'agreementItemSeqId="{v[1]}" label="{q(label(norms, *v))}"/>')
    for k in sorted(edges.edges):
        e = edges.edges[k]
        eid = sid_hash('NB', e['kind'], *e['from'], *e['to'])
        out.append(f'    <moqui.math.GraphEdge graphEdgeId="{eid}" graphId="{GRAPH}" edgeTypeEnumId="{e["kind"]}" '
                   f'fromVertexId="{vid[e["from"]]}" toVertexId="{vid[e["to"]]}" '
                   f'isDirected="{"N" if e["kind"] in UNDIRECTED else "Y"}" isLoop="N" weight="{e["confidence"]}" '
                   f'label="{e["kind"][5:]}"/>')
        out.append(f'    <moqui.math.Parameter parameterId="{sid_hash("NQ", eid, "pass")}" parameterDefId="CmpAssocPass" '
                   f'graphId="{GRAPH}" graphEdgeId="{eid}" symbolicValue="{",".join(e["passes"])}"/>')
        out.append(f'    <moqui.math.Parameter parameterId="{sid_hash("NQ", eid, "evidence")}" parameterDefId="CmpAssocEvidence" '
                   f'graphId="{GRAPH}" graphEdgeId="{eid}" textValue="{q(" | ".join(e["evidence"])[:4000])}"/>')
    out.append('</entity-facade-xml>')
    return '\n'.join(out) + '\n', len(vertices)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--write', action='store_true')
    ap.add_argument('--compare', action='store_true', help='compare with data/70_CmpAssociations.xml (rows by id and content)')
    ap.add_argument('--sample', type=int, default=6)
    ap.add_argument('--pass', dest='only')
    ap.add_argument('--seed', type=int, default=1)
    a = ap.parse_args()
    norms = Norms()
    concepts = Concepts(norms)
    edges = Edges()
    random.seed(a.seed)
    # rounds until nothing new: a pass may read the edges the others made
    new_by_pass = defaultdict(int)
    for rnd in range(1, 11):
        added = 0
        for name, fn in PASSES:
            before = set(edges.edges)
            fn(norms, concepts, edges)
            n_new = sum(1 for k in edges.edges if k not in before)
            new_by_pass[name] += n_new
            added += n_new
        if not added:
            break
    print(f'== rounds: {rnd} (the last added nothing)')
    for name, fn in PASSES:
        new = range(new_by_pass[name])
        made = [k for k, e in edges.edges.items() if name in e['passes']]
        kinds = defaultdict(int)
        for k in made:
            kinds[k[0]] += 1
        print(f'== {name}: {len(made)} edges ({len(new)} new) {dict(kinds)}')
        if a.only in (None, name):
            for k in random.sample(made, min(a.sample, len(made))):
                e = edges.edges[k]
                print(f'   {label(norms, *e["from"])[:70]}  ->  {label(norms, *e["to"])[:70]}\n      [{e["confidence"]}] '
                      f'{" | ".join(e["evidence"])[:220]}')
    text, n_v = seed(norms, edges)
    print(f'total: {len(edges.edges)} edges, {n_v} vertices')
    if a.compare:
        f = DATA / '70_CmpAssociations.xml'
        old = set(f.read_text(encoding='utf-8').splitlines()) if f.exists() else set()
        new = set(text.splitlines())
        rows = lambda ls: {l for l in ls if l.strip().startswith('<moqui.math.')}
        removed, added = rows(old) - rows(new), rows(new) - rows(old)
        print('ASSOC', 'same' if old and not (removed or added) else
              ('first build' if not old else f'-{len(removed)} +{len(added)} rows'))
        for sign, ls in (('-', removed), ('+', added)):
            for l in sorted(ls)[:10]:
                print(f'   {sign} {l.strip()[:200]}')
    if a.write:
        (DATA / '70_CmpAssociations.xml').write_text(text, encoding='utf-8')
        print('written data/70_CmpAssociations.xml')


if __name__ == '__main__':
    main()
