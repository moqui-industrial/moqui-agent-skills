"""Reader for EU acts published by the Publications Office in Formex 4 XML.

The English files drive the structure and the ids; the files of other languages have the same element structure
(checked by `check_parallel`) and contribute titles and texts at the same element positions.
"""
import glob
import os
import re
import xml.etree.ElementTree as ET

from .ir import Node, clean_text, node_id

BLOCK_TAGS = {'P', 'ALINEA', 'NP', 'TXT', 'LIST', 'TI', 'STI', 'PARAG', 'GR.SEQ', 'ITEM', 'CONSID', 'TITLE', 'TBL',
              'ROW', 'CELL', 'FORMULA'}
SKIP_TAGS = {'NOTE', 'NO.P', 'NO.PARAG', 'TI.ART', 'STI.ART', 'BIB.INSTANCE', 'TITLE'}
STRUCT_TAGS = {'ACT', 'ANNEX', 'DIVISION', 'ARTICLE', 'PARAG', 'ALINEA', 'ITEM', 'LIST', 'NP', 'GR.SEQ', 'CONSID',
               'TITLE', 'TI', 'STI', 'TI.ART', 'STI.ART', 'CONTENTS', 'PREAMBLE', 'ENACTING.TERMS'}
ROMAN = re.compile(r'\b([IVXLC]+)\b')


def element_text(e, stop):
    """Text of e, leaving out the subtrees in `stop` (elements that become nodes of their own)."""
    parts = []

    def walk(x, top):
        if x is not top and (x in stop or x.tag in SKIP_TAGS):
            if x.tail:
                parts.append(x.tail)
            return
        if x.tag == 'QUOT.START' or x.tag == 'QUOT.END':
            code = x.get('CODE')
            if code:
                parts.append(chr(int(code, 16)))
        if x.text:
            parts.append(x.text)
        for c in x:
            walk(c, top)
        if x.tag in BLOCK_TAGS:
            parts.append('\n')
        if x is not top and x.tail:
            parts.append(x.tail)

    walk(e, e)
    return clean_text(''.join(parts))


def plain(e):
    return clean_text(element_text(e, set())) if e is not None else ''


def title_text(e):
    """Title of a partition, number included (section numbers sit in NO.P inside the title)."""
    if e is None:
        return ''
    return clean_text(' '.join(t.strip() for t in e.itertext() if t.strip()))


def struct_paths(root):
    """element -> path of (tag, ordinal among siblings with the same tag); insensitive to inline formatting."""
    out = {}
    def walk(e, p):
        out[e] = p
        count = {}
        for c in e:
            k = count.get(c.tag, 0)
            count[c.tag] = k + 1
            walk(c, p + ((c.tag, k),))
    walk(root, ())
    return out


def number_of(item):
    """'(a)' -> 'a', '(12)' -> '12', '3.' -> '3'."""
    no = item.find('NP/NO.P')
    if no is None:
        no = item.find('NO.P')
    if no is None or not (no.text or '').strip():
        return None
    return no.text.strip().strip('()').rstrip('.').strip()


class FormexReader:
    def __init__(self, norm_id, files_by_lang, primary='en'):
        """files_by_lang: {'en': dir, 'it': dir}; each dir holds the unzipped Formex package of one language."""
        self.normId = norm_id
        self.primary = primary
        self.dirs = files_by_lang
        self.nodes = []
        self.seq = 0
        self.paths = {}   # nodeId -> (fileIndex, element index path) used to fetch other languages

    # ---------- parallel structure ----------
    def doc_files(self, lang):
        files = sorted(f for f in glob.glob(os.path.join(self.dirs[lang], '*.xml'))
                       if not f.endswith('.doc.xml') and not f.endswith('.toc.xml') and '.doc.' not in f
                       and '.toc.' not in f)
        return files

    def check_parallel(self):
        en = self.doc_files(self.primary)
        problems = []
        for lang in self.dirs:
            other = self.doc_files(lang)
            if len(other) != len(en):
                problems.append(f'{lang}: {len(other)} files, {self.primary}: {len(en)}')
                continue
            for a, b in zip(en, other):
                ta = [e.tag for e in ET.parse(a).getroot().iter() if e.tag in STRUCT_TAGS]
                tb = [e.tag for e in ET.parse(b).getroot().iter() if e.tag in STRUCT_TAGS]
                if ta != tb:
                    problems.append(f'{lang}: element structure differs in {os.path.basename(b)}')
        return problems

    # ---------- node creation ----------
    def add(self, path, parent, kind, elem, file_idx, number=None, title_elem=None, stop=frozenset(), extra=None):
        nid = node_id(self.normId, path)
        if nid in self.paths:
            k = 2
            while f'{nid}~{k}' in self.paths:
                k += 1
            nid = f'{nid}~{k}'
        self.seq += 1
        n = Node(nodeId=nid, normId=self.normId, parentId=parent, kind=kind, seq=self.seq, number=number)
        n.title[self.primary] = title_text(title_elem)
        n.text[self.primary] = element_text(elem, set(stop)) if elem is not None else ''
        n.source = {'file': os.path.basename(self.files[file_idx]), 'id': (elem.get('IDENTIFIER') or '') if elem is not None else ''}
        if extra:
            extra(n)
        self.nodes.append(n)
        self.paths[nid] = (file_idx, self.index_path(file_idx, elem), self.index_path(file_idx, title_elem),
                           tuple(self.index_path(file_idx, s) for s in stop))
        return nid

    def index_path(self, file_idx, elem):
        if elem is None:
            return None
        return self.idx[file_idx].get(elem)

    # ---------- reading ----------
    def read(self):
        self.files = self.doc_files(self.primary)
        self.roots = [ET.parse(f).getroot() for f in self.files]
        self.idx = [struct_paths(r) for r in self.roots]
        act_i = next(i for i, r in enumerate(self.roots) if r.tag == 'ACT')
        act = self.roots[act_i]
        doc = self.add('DOC', None, 'document', None, act_i, title_elem=act.find('TITLE'))
        self.read_preamble(act, doc, act_i)
        self.read_enacting(act.find('ENACTING.TERMS'), doc, act_i)
        for i, r in enumerate(self.roots):
            if r.tag == 'ANNEX':
                self.read_annex(r, doc, i)
        for lang in self.dirs:
            if lang != self.primary:
                self.fill_language(lang)
        return self.nodes

    def read_preamble(self, act, parent, fi):
        pre = act.find('PREAMBLE')
        if pre is None:
            return
        p = self.add('PRE', parent, 'preamble', None, fi)
        for c in pre.iter('CONSID'):
            num = number_of(c)
            self.add(f'PRE.REC_{num}', p, 'recital', c, fi, number=num)

    def read_enacting(self, et, parent, fi):
        for div in et.findall('DIVISION'):
            self.read_division(div, parent, fi, 'CHAP')

    def read_division(self, div, parent, fi, prefix):
        ti = title_text(div.find('TITLE/TI'))
        m = ROMAN.search(ti.split()[-1]) if ti else None
        num = m.group(1) if m else str(self.seq)
        path = f'{prefix}_{num}'
        nid = self.add(path, parent, 'chapter' if prefix == 'CHAP' else 'section', None, fi, number=ti,
                       title_elem=div.find('TITLE/STI'))
        for c in div:
            if c.tag == 'DIVISION':
                self.read_division(c, nid, fi, path + '.SEC')
            elif c.tag == 'ARTICLE':
                self.read_article(c, nid, fi)

    def read_article(self, art, parent, fi):
        num = str(int(art.get('IDENTIFIER')))
        path = f'ART_{num}'
        is_def = plain(art.find('STI.ART')).lower() in ('definitions', 'definizioni')
        stop = [c for c in art if c.tag == 'PARAG'] + self.items_below(art)
        nid = self.add(path, parent, 'article', art, fi, number=num, title_elem=art.find('STI.ART'), stop=stop)
        for c in art:
            if c.tag == 'PARAG':
                pnum = str(int(c.get('IDENTIFIER').split('.')[-1]))
                ppath = f'{path}.PAR_{pnum}'
                pid = self.add(ppath, nid, 'paragraph', c, fi, number=pnum, stop=self.items_below(c))
                self.read_items(c, pid, ppath, fi, False)
        self.read_items(art, nid, path, fi, is_def, skip=[c for c in art if c.tag == 'PARAG'])

    def items_below(self, e, skip=()):
        """ITEM elements whose nearest node-forming ancestor is e."""
        out = []
        def walk(x):
            for c in x:
                if c in skip or c.tag in ('PARAG', 'GR.SEQ'):
                    continue
                if c.tag == 'ITEM':
                    out.append(c)
                else:
                    walk(c)
        walk(e)
        return out

    def read_items(self, e, parent, path, fi, is_def, skip=()):
        for it in self.items_below(e, skip):
            num = number_of(it) or str(self.seq)
            ipath = f'{path}.PT_{num}'
            kind = 'definition' if is_def else 'point'
            def term(n, it=it):
                m = re.match(r'\s*[‘«“"]([^’»”"]+)[’»”"]', n.text[self.primary])
                if m:
                    n.term[self.primary] = m.group(1)
            iid = self.add(ipath, parent, kind, it, fi, number=num, stop=self.items_below(it),
                           extra=term if is_def else None)
            self.read_items(it, iid, ipath, fi, False)

    # ---------- annexes ----------
    def read_annex(self, ax, parent, fi):
        ti = title_text(ax.find('TITLE/TI'))
        m = ROMAN.search(ti)
        num = m.group(1) if m else str(self.seq)
        path = f'ANX_{num}'
        contents = ax.find('CONTENTS')
        stop = self.annex_children(contents) if contents is not None else []
        # the heading of an annex is the title of its first section; the annex TITLE only says "ANNEX I"
        head = contents.find('GR.SEQ/TITLE') if contents is not None else None
        nid = self.add(path, parent, 'annex', contents, fi, number=num,
                       title_elem=head if head is not None else ax.find('TITLE'), stop=stop)
        if contents is not None:
            self.read_annex_body(contents, nid, path, fi)

    def annex_children(self, e):
        """Child elements of e that become nodes: sections (GR.SEQ), numbered paragraphs (NP) and list items."""
        out = []
        for c in e:
            if c.tag == 'GR.SEQ':
                out.append(c)
            elif c.tag == 'NP' and number_of_np(c):
                out.append(c)
            elif c.tag == 'TITLE':
                continue
            else:
                out.extend(self.items_below(c) if c.tag != 'ITEM' else [c])
        return out

    def read_annex_body(self, e, parent, path, fi):
        for c in self.annex_children(e):
            if c.tag == 'GR.SEQ':
                title = title_text(c.find('TITLE'))
                m = re.match(r'^(PART\s+[A-Z]+|PARTE\s+[A-Z]+|\d+(?:\.\d+)*)\.?\s*(.*)$', title, re.S)
                if m and m.group(1)[0].isdigit():
                    num = m.group(1)
                    base = path.split('.SEC_')[0]
                    spath = f'{base}.SEC_{num}'
                elif m:
                    num = m.group(1).split()[-1]
                    spath = f'{path}.PART_{num}'
                else:
                    num = None
                    k = sum(1 for x in self.annex_children(e) if x.tag == 'GR.SEQ' and x is not c and
                            list(e).index(x) < list(e).index(c)) + 1
                    spath = f'{path}.S{k}'
                kind = 'annexSection'
                sid = self.add(spath, parent, kind, c, fi, number=num, title_elem=c.find('TITLE'),
                               stop=self.annex_children(c))
                self.read_annex_body(c, sid, spath, fi)
            else:
                num = number_of_np(c) if c.tag == 'NP' else number_of(c)
                num = num or str(len(self.nodes))
                ppath = f'{path}.PT_{num}'
                pid = self.add(ppath, parent, 'point', c, fi, number=num, stop=self.items_below(c))
                self.read_items(c, pid, ppath, fi, False)

    # ---------- other languages ----------
    def fill_language(self, lang):
        files = self.doc_files(lang)
        roots = [ET.parse(f).getroot() for f in files]
        rev = [{v: k for k, v in struct_paths(r).items()} for r in roots]

        def at(fi, p):
            if p is None:
                return None
            e = rev[fi].get(p)
            if e is None:
                raise ValueError(f'{lang}: no element at {p} in {os.path.basename(files[fi])}')
            return e

        for n in self.nodes:
            fi, ep, tp, stops = self.paths[n.nodeId]
            e, t = at(fi, ep), at(fi, tp)
            n.title[lang] = title_text(t)
            n.text[lang] = element_text(e, set(at(fi, s) for s in stops)) if e is not None else ''
            if n.kind == 'definition':
                m = re.match(r'\s*[‘«“"]([^’»”"]+)[’»”"]', n.text[lang])
                if m:
                    n.term[lang] = m.group(1)


def number_of_np(np):
    no = np.find('NO.P')
    if no is None or not (no.text or '').strip():
        return None
    return no.text.strip().strip('()').rstrip('.').strip()
