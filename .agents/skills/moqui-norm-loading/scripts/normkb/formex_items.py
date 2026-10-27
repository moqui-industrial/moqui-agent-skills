"""Reader of EU acts in Formex 4 XML into norm items (Agreement model, PLAN-NORMS-AGREEMENT.md N1-N3).

Every capoverso is an item: P, ALINEA, numbered NP; a LIST belongs to the capoverso that introduces it (Annex III
1.2.1 has three paragraphs, each with its own list a, b, c, ...). A container (article, paragraph, section, point)
with a single capoverso keeps its text; with more capoversi each becomes a child item.

The files of the primary language drive structure and ids; the files of other languages have the same element
structure (FormexReader.check_parallel) and give the texts of the same elements.
"""
import glob
import os
import re
import xml.etree.ElementTree as ET

from .formex import element_text, struct_paths, title_text
from .ir import clean_text
from .items import Item

NUMBER_TAGS = {'NO.P', 'NO.PARAG', 'NO.GR.SEQ'}
ROMAN = re.compile(r'\b([IVXLC]+)\b')
DEFINITION = re.compile(r'\s*[‘«“"]([^’»”"]{1,120})[’»”"]\s*(?:means\b|shall mean\b|:|,\s*\w|'
                        r'(?:indica|designa|si intende)\b)')


def no_text(e):
    """'(a)' -> 'a', '3.' -> '3', '1.2.1.' -> '1.2.1'."""
    if e is None or not (e.text or '').strip():
        return None
    return e.text.strip().strip('()').rstrip('.').strip()


def item_number(e):
    """Number of a numbered element (ITEM, NP, PARAG, GR.SEQ). A section takes it only from its own title or
    NO.GR.SEQ: the NP children of a section are its numbered paragraphs, not its number."""
    paths = ('NO.GR.SEQ', 'TITLE/TI/NP/NO.P', 'TITLE/TI/NO.P') if e.tag == 'GR.SEQ' else \
        ('NP/NO.P', 'NO.P', 'NO.PARAG')
    for p in paths:
        n = no_text(e.find(p))
        if n:
            return n
    return None


BLOCK_TAGS = {'P', 'ALINEA', 'TXT', 'NP', 'LIST', 'TBL', 'PARAG', 'GR.SEQ', 'FORMULA', 'CONSID'}


def has_blocks(e):
    """A block containing other blocks (an ALINEA or a P with a list inside) is a container, not a capoverso."""
    return any(c.tag in ('P', 'LIST', 'NP', 'TBL', 'ALINEA') for c in e)


class FormexItemReader:
    def __init__(self, norm_id, dirs, primary='en'):
        self.normId = norm_id
        self.dirs = dirs
        self.primary = primary
        self.items = []
        self.where = {}      # seqId -> (file index, [text element paths], [stop element paths], title path)
        self.seq = {}        # parent seqId -> last sequence

    def files(self, lang):
        return sorted(f for f in glob.glob(os.path.join(self.dirs[lang], '*.xml')) if '.doc.' not in f
                      and '.toc.' not in f and not f.endswith('.doc.xml'))

    # ---------- items ----------
    def add(self, seq_id, parent, typ, fi, number=None, texts=(), stops=(), title=None, source=None):
        k = self.seq.get(parent, 0) + 1
        self.seq[parent] = k
        it = Item(seqId=seq_id, parentSeqId=parent, type=typ, number=number, sequence=k,
                  source=source or os.path.basename(self.fnames[fi]))
        self.items.append(it)
        self.where[seq_id] = (fi, [self.idx[fi][t] for t in texts], [self.idx[fi][s] for s in stops],
                              self.idx[fi].get(title) if title is not None else None)
        return it

    def read(self):
        self.fnames = self.files(self.primary)
        self.roots = [ET.parse(f).getroot() for f in self.fnames]
        self.idx = [struct_paths(r) for r in self.roots]
        ai = next(i for i, r in enumerate(self.roots) if r.tag == 'ACT')
        act = self.roots[ai]
        pre = act.find('PREAMBLE')
        if pre is not None:
            consids = list(pre.iter('CONSID'))
            self.add('PRE', None, 'AitPreamble', ai, texts=[pre], stops=consids)
            for c in consids:
                self.add(f'REC{item_number(c)}', 'PRE', 'AitRecital', ai, number=item_number(c), texts=[c])
        for div in act.find('ENACTING.TERMS').findall('DIVISION'):
            self.read_division(div, None, ai, 'CHAP')
        final = act.find('FINAL')
        if final is not None:
            self.add('FINAL', None, 'AitParagraph', ai, texts=[final])
        for i, r in enumerate(self.roots):
            if r.tag == 'ANNEX':
                self.read_annex(r, i)
        for lang in self.dirs:
            self.fill(lang)
        return self.items

    def read_division(self, div, parent, fi, prefix):
        ti = title_text(div.find('TITLE/TI'))
        m = ROMAN.search(ti.split()[-1]) if ti else None
        num = m.group(1) if m else str(len(self.items))
        sid = f'{prefix}{num}' if parent is None else f'{parent}.SEC{num}'
        self.add(sid, parent, 'AitChapter' if parent is None else 'AitSection', fi, number=ti,
                 title=div.find('TITLE/STI'))
        for c in div:
            if c.tag == 'DIVISION':
                self.read_division(c, sid, fi, prefix)
            elif c.tag == 'ARTICLE':
                self.read_article(c, sid, fi)

    def read_article(self, art, parent, fi):
        num = str(int(art.get('IDENTIFIER')))
        sid = f'ART{num}'
        self.add(sid, parent, 'AitArticle', fi, number=num, title=art.find('STI.ART'))
        self.read_container(art, sid, fi, 'article')

    # ---------- the capoverso rule ----------
    def units(self, e):
        """Ordered units of e: its own inline text ('own', when it has any outside its blocks), then its blocks."""
        blocks = [c for c in e if c.tag in BLOCK_TAGS]
        not_own = blocks + [c for c in e if c.tag in NUMBER_TAGS]
        out = []
        if element_text(e, set(not_own)).strip():
            out.append(('own', e, not_own))
        for c in blocks:
            if c.tag == 'PARAG':
                out.append(('parag', c, None))
            elif c.tag == 'GR.SEQ':
                out.append(('seq', c, None))
            elif c.tag == 'LIST':
                out.append(('list', c, None))
            elif c.tag == 'TBL':
                out.append(('table', c, None))
            elif c.tag == 'NP' and item_number(c):
                out.append(('np', c, None))
            elif has_blocks(c):
                inner = self.units(c)
                if inner and all(u[0] == 'list' for u in inner):
                    # <P><LIST/></P>: the list belongs to the capoverso before it, not to an empty capoverso
                    out.extend(inner)
                else:
                    out.append(('alinea', c, None))
            else:
                out.append(('text', c, None))
        return out

    def read_container(self, e, sid, fi, kind):
        """Children of the item `sid` read from element e. kind: article, paragraph, section, annex, point,
        capoverso."""
        us = self.units(e)
        caps = [u for u in us if u[0] in ('text', 'alinea', 'own')]
        if len(caps) == 1 and caps[0][0] == 'alinea' and len(us) == 1:
            return self.read_container(caps[0][1], sid, fi, kind)
        single = len(caps) == 1 and caps[0][0] in ('text', 'own')
        if single:
            w = self.where[sid]
            typ, c, blocks = caps[0]
            self.where[sid] = (w[0], [self.idx[fi][c]], [self.idx[fi][b] for b in (blocks or [])], w[3])
        last_cap = sid
        k_par = 0
        k_tab = 0
        for typ, c, blocks in us:
            if typ in ('text', 'alinea', 'own') and not single:
                k_par += 1
                if kind == 'paragraph':
                    cid, ctype = f'{sid}.s{k_par}', 'AitSubparagraph'
                else:
                    cid, ctype = f'{sid}.p{k_par}', 'AitParagraph'
                if typ == 'text':
                    self.add(cid, sid, ctype, fi, texts=[c])
                elif typ == 'own':
                    self.add(cid, sid, ctype, fi, texts=[c], stops=blocks)
                else:
                    self.add(cid, sid, ctype, fi)
                    self.read_container(c, cid, fi, 'capoverso')
                last_cap = cid
            elif typ == 'list':
                self.read_list(c, last_cap, fi)
            elif typ == 'parag':
                pnum = str(int(c.get('IDENTIFIER').split('.')[-1]))
                pid = f'{sid}.{pnum}'
                self.add(pid, sid, 'AitParagraph', fi, number=pnum)
                self.read_container(c, pid, fi, 'paragraph')
                last_cap = pid
            elif typ == 'np':
                num = item_number(c)
                pid = f'{sid}.pt{num}'
                self.add(pid, sid, 'AitSubPoint' if kind == 'point' else 'AitPoint', fi, number=num)
                self.read_container(c, pid, fi, 'point')
                last_cap = pid
            elif typ == 'seq':
                self.read_section(c, sid, fi)
            elif typ == 'table':
                k_tab += 1
                self.add(f'{sid}.t{k_tab}', sid, 'AitTable', fi, texts=[c])

    def read_list(self, lst, parent, fi):
        ptype = next(i.type for i in reversed(self.items) if i.seqId == parent)
        sub = ptype in ('AitPoint', 'AitSubPoint')
        for k, item in enumerate([c for c in lst if c.tag == 'ITEM'], 1):
            num = item_number(item) or str(k)
            cid = f'{parent}.{"sp" if sub else "pt"}{num}'
            nested = [x for x in item.iter('LIST') if x is not item]
            top_lists = [x for x in nested if not any(x in y.iter() and x is not y for y in nested)]
            self.add(cid, parent, 'AitSubPoint' if sub else 'AitPoint', fi, number=num, texts=[item],
                     stops=[i for x in top_lists for i in x if i.tag == 'ITEM'])
            for x in top_lists:
                self.read_list(x, cid, fi)

    # ---------- annexes ----------
    def read_annex(self, ax, fi):
        ti = title_text(ax.find('TITLE/TI'))
        m = ROMAN.search(ti)
        num = m.group(1) if m else str(len(self.items))
        sid = f'ANX{num}'
        contents = ax.find('CONTENTS')
        first = contents.find('GR.SEQ') if contents is not None else None
        # the first section repeats the title of the annex: it is the annex itself, not a level
        flat = first is not None and len([c for c in contents if c.tag == 'GR.SEQ']) == 1 and \
            not [c for c in contents if c.tag not in ('GR.SEQ',)]
        self.add(sid, None, 'AitAnnex', fi, number=num, title=first.find('TITLE') if flat else ax.find('TITLE/STI'))
        self.read_container(first if flat else contents, sid, fi, 'annex')

    def read_section(self, seq, parent, fi):
        title = seq.find('TITLE')
        num = item_number(seq)
        tt = title_text(title)
        # "PART A" (Regulation 2023/1230), "Part I" (Regulation 2024/2847); classes of products "Class I"
        part = re.match(r'^(PART|PARTE)\s+([A-Z]+)\b', tt, re.I)
        cls = re.match(r'^(CLASS|CLASSE)\s+([IVX]+)\b', tt, re.I)
        annex = parent.split('.')[0]
        if part:
            sid, typ, num = f'{annex}.{part.group(2)}', 'AitAnnexPart', part.group(2)
        elif cls:
            sid, typ, num = f'{parent}.cl{cls.group(2)}', 'AitSection', cls.group(2)
        elif num and re.match(r'^\d+(\.\d+)*$', num):
            base = '.'.join(parent.split('.')[:2]) if parent.count('.') >= 1 and \
                re.match(r'^[A-Z]+$', parent.split('.')[1]) else annex
            sid, typ = f'{base}.{num}', 'AitSection'
        else:
            k = sum(1 for i in self.items if i.parentSeqId == parent and i.type == 'AitSection') + 1
            sid, typ = f'{parent}.g{k}', 'AitSection'
        it = self.add(sid, parent, typ, fi, number=num, title=title)
        self.read_container(seq, sid, fi, 'section')
        return it

    # ---------- texts of every language ----------
    def fill(self, lang):
        files = self.files(lang)
        roots = [ET.parse(f).getroot() for f in files]
        rev = [{v: k for k, v in struct_paths(r).items()} for r in roots]

        def at(fi, p):
            e = rev[fi].get(p)
            if e is None:
                raise ValueError(f'{lang}: no element at {p} in {os.path.basename(files[fi])}')
            return e

        for it in self.items:
            fi, texts, stops, title = self.where[it.seqId]
            stop = set(at(fi, s) for s in stops)
            # a container item never repeats the text of its child items
            child_elems = set()
            it.text[lang] = clean_text('\n'.join(element_text(at(fi, t), stop | child_elems) for t in texts))
            it.title[lang] = self.title_of(at(fi, title)) if title is not None else ''
            # a definition, wherever it is: "‘danger zone’ means ...", "«zona pericolosa»: ...", "si intende per"
            m = DEFINITION.match(it.text[lang]) if it.type in ('AitPoint', 'AitSubPoint', 'AitParagraph') else None
            if m:
                it.term[lang] = m.group(1)
                if not it.title.get(lang):
                    it.title[lang] = m.group(1)

    @staticmethod
    def title_of(t):
        """Title without its number (the number is in itemNumber)."""
        txt = t.find('TI/NP/TXT')
        if txt is not None:
            return clean_text(' '.join(x.strip() for x in txt.itertext() if x.strip()))
        sti = t.find('STI')
        if t.tag == 'TITLE' and sti is not None:
            return title_text(sti)
        return title_text(t)
