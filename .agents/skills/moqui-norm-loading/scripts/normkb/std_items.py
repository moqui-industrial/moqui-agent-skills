"""Norm items of a standard read from PDF (Agreement model, PLAN-NORMS-AGREEMENT.md N1-N3, N7).

The PDF reader (pdfstd.py) gives one node per numbered clause, definition, annex, front section, figure and table,
with the own text of the clause. This module splits that text into its capoversi, following the rules of the
norm-loading skill:

- blocks are separated by blank lines; a block that does not end a sentence and is followed by a block starting in
  lower case is the same paragraph broken by the page layout;
- a) b) start points, 1) 2) sub-points of the last point, dash lines (⎯ — – •) list items of the paragraph or point
  before them; NOTE / NOTA and EXAMPLE / ESEMPIO blocks are notes and examples of the clause;
- a point whose own line does not end with punctuation is a heading point (ISO 12100 5.4 a): the paragraphs that
  follow belong to it until the next point; a closed point (ending with . ; :) leaves the following paragraphs to
  the clause;
- a clause with a single paragraph keeps the text itself.

A figure modelled in config/figures becomes an item whose text describes the diagram (steps, decisions and flows)
with one child item per box. The text of every clause is rebuilt from its items in `check_partition`: nothing lost,
nothing duplicated.
"""
import re
from collections import Counter

from .items import Item, ItemRef
from .pdf_tables import row_text, words

LETTER = re.compile(r'^([a-z])\)\s+(.*)$', re.S)
NUMBER = re.compile(r'^(\d{1,2})\)\s+(.*)$', re.S)
DASH = re.compile(r'^[⎯—–•]\s*(.*)$', re.S)
ROMAN = re.compile(r'^(i|ii|iii|iv|v|vi|vii|viii|ix|x)\)\s+(.*)$', re.S)
CLAUSE_ENTRY = re.compile(r'^(?:\d{1,2}(?:\.\d{1,2})*(?:\s+[a-z]\))?,?\s*)+:\s+\S')
DOTNUM = re.compile(r'^(\d{1,2})\.\s+(\S.*)$', re.S)
NOTE = re.compile(r'^(NOTE|NOTA)(\s+\d+)?\b')
EXAMPLE = re.compile(r'^(EXAMPLE|ESEMPIO)(\s+\d+)?\b')
SENTENCE_END = re.compile(r'[.;:!?)\]]\s*$')
# a caption: "Table B.1", "Table B.1 (continued)", "Figure 3 — Elements of risk"; not a sentence starting with
# "Table B.2 is a subset of ..."
CAPTION = re.compile(r'^(Figure|Table|Figura|Tabella)\s+(\d{1,2}|[A-Z]{1,2}\.\d{1,2})\s*'
                     r'(\((continued|segue|\d+\s+(?:di|of)\s+\d+)\)\s*$|[—–-]{1,2}\s*\S|$)')
# words of the text the reader writes itself (figure boxes, table columns), in the language of the edition
GEN_WORDS = {'en': {'step': 'Step', 'block': 'Block', 'decision': 'Decision', 'end': 'End', 'next': 'next',
                    'columns': 'Columns', 'labels': 'Drawing labels'},
             'it': {'step': 'Passo', 'block': 'Blocco', 'decision': 'Decisione', 'end': 'Fine', 'next': 'segue',
                    'columns': 'Colonne', 'labels': 'Etichette del disegno'}}
BOX_PREFIX = re.compile(r'^(' + '|'.join(w for g in GEN_WORDS.values() for k, w in g.items()
                                         if k in ('step', 'block', 'decision', 'end')) + r'): ')
KIND_TYPE = {'clause': 'AitArticle', 'definition': 'AitArticle', 'annex': 'AitAnnex', 'preamble': 'AitPreamble',
             'bibliography': 'AitSection', 'figure': 'AitFigure', 'table': 'AitTable', 'document': None}


def seq_id(node):
    """Item id of a node: clause and definition numbers as printed, annexes ANX<letter>, figures FIG<n>."""
    path = node.nodeId.split(':', 1)[1]
    if node.kind in ('clause', 'definition'):
        return node.number or path
    if node.kind == 'annex':
        return f'ANX{node.number}'
    dup = f'-{node.attrs["duplicate"]}' if node.attrs.get('duplicate') else ''
    if node.kind == 'figure':
        return f'FIG{node.number}{dup}'
    if node.kind == 'table':
        return f'TAB{node.number}{dup}'
    if node.kind in ('flowStep', 'flowDecision', 'flowTerminal'):
        fig, box = path.split('.N_', 1)
        return f'FIG{fig.split("_", 1)[1]}.{box}'
    return path.replace('~', '-')


# a numbered requirement enhancement: "(1) Unique identification and authentication"
PAREN_NUMBER = re.compile(r'^\((\d{1,2})\)\s+(\S.*)$', re.S)

# a line of the legend of a formula: "NSCA is the number of ...", "T 1 is the proof test interval"
LEGEND = re.compile(r'^(?:\S{1,8}\s){1,2}\s*(?:is|are|è|sono)\s')


def blocks(text):
    """Paragraph blocks of a clause text, with paragraphs broken by the page layout joined again."""
    raw = [b.strip() for b in re.split(r'\n\s*\n', text or '') if b.strip()]
    out = []
    for b in raw:
        # a block can hold several list lines without blank lines between them (ISO 12100 5.4 first list)
        # a lettered list inside a note stays in the note: "i)" there is the letter after "h)", not a roman numeral
        parts = re.split(r'\n(?=[⎯—–•]\s)' if NOTE.match(b) or EXAMPLE.match(b) else
                         r'\n(?=[⎯—–•]\s|(?:i|ii|iii|iv|v|vi|vii|viii|ix|x)\)\s)', b)
        # a line starting with the next letter of the list the block starts ("d) ..." / "e) ...") is the next point
        # when the lines are too close for a blank line (IEC 60204-1 Annex B form)
        # a line "4.3.1: ..." or "6.3.3 b), 13.4.5 b): ..." after a finished sentence starts an entry of its own
        # (national deviations of a European edition: clause, colon, deviation)
        entries = []
        for p in parts:
            lines = p.split('\n')
            cur = [lines[0]]
            for line in lines[1:]:
                if CLAUSE_ENTRY.match(line.strip()) and re.search(r'[.;:)]\s*$', cur[-1]):
                    entries.append('\n'.join(cur))
                    cur = [line.strip()]
                else:
                    cur.append(line)
            entries.append('\n'.join(cur))
        parts = entries
        split = []
        for p in parts:
            while True:
                m = re.match(r'([a-y])\)\s', p)
                nxt = m and re.search(r'\n(?=' + chr(ord(m.group(1)) + 1) + r'\)\s)', p)
                if not nxt:
                    break
                split.append(p[:nxt.start()])
                p = p[nxt.start() + 1:]
            split.append(p)
        for p in split:
            marker = LETTER.match(p) or NUMBER.match(p) or DASH.match(p) or NOTE.match(p) or EXAMPLE.match(p) or \
                ROMAN.match(p)
            # a paragraph broken by the page goes on in a Latin lower-case letter; a Greek one starts a formula
            if out and not marker and not SENTENCE_END.search(out[-1]) and re.match(r'[a-zà-ÿ]', p) and \
                    not DASH.match(out[-1]):
                out[-1] = out[-1] + '\n' + p
            else:
                out.append(p)
    return out


def split_clause(node, lang, sid):
    """Child items of one clause (its own item is made by the caller). Returns (own text, children)."""
    bl = blocks(node.text.get(lang) or '')
    children = []
    counters = {}

    def add(parent, kind, prefix, number, text):
        key = (parent, prefix)
        counters[key] = counters.get(key, 0) + 1
        k = counters[key]
        seg = f'{prefix}{number if number else k}'
        it = Item(seqId=f'{parent}.{seg}', parentSeqId=parent, type=kind, number=number,
                  sequence=sum(1 for c in children if c.parentSeqId == parent) + 1, source=node.source.get('page', ''))
        it.text[lang] = text
        children.append(it)
        return it

    paragraphs = [b for b in bl if not (LETTER.match(b) or NUMBER.match(b) or DASH.match(b) or NOTE.match(b)
                                       or EXAMPLE.match(b) or DOTNUM.match(b))]
    has_lists = len(paragraphs) != len(bl)
    if len(paragraphs) <= 1 and not has_lists:
        return (bl[0] if bl else ''), []
    single = len(paragraphs) == 1 and bl and bl[0] is paragraphs[0]
    own = paragraphs[0] if single else ''
    last_par = sid                  # owner of a list that starts now: the clause or the paragraph before
    letter_parent = None            # parent of the open list a) b) ...
    last_point = None               # last item of that list
    dash_parent = None              # parent of the open dash list
    recent = None                   # most recent list item (point or dash) that numbered items 1) 2) hang from
    open_point = None               # heading point (no list follows it) that owns the following paragraphs
    last_dot = 0                    # last numbered section "1." "2." (IEC 60204-1 Annex B enquiry form)
    legend = False                  # inside the legend of a formula
    for i, b in enumerate(bl):
        if single and i == 0:
            continue
        # a legend goes on only from the block right before it: after a list or a note its lines are paragraphs
        in_legend, legend = legend, False
        m = DOTNUM.match(b)
        if m and int(m.group(1)) == last_dot + 1:
            # numbered section of a form: a point of the clause with its own lettered list
            last_dot = int(m.group(1))
            sec = add(sid, 'AitPoint', 'pt', m.group(1), m.group(2).strip())
            last_par, letter_parent, last_point, dash_parent, recent, open_point = sec.seqId, None, None, None, None, sec
            continue
        m = ROMAN.match(b)
        if m and recent is not None and re.search(r'\.(sp\d+|r[ivx]+)$', recent.seqId):
            owner = recent.seqId if re.search(r'\.sp\d+$', recent.seqId) else recent.parentSeqId
            recent = add(owner, 'AitSubPoint', 'r', m.group(1), m.group(2).strip())
            continue
        m = PAREN_NUMBER.match(b)
        # a title, not a sentence ("(1) Ritirata." in a bibliography is a note)
        if m and not re.search(r'\.\s*$', m.group(2)) and (last_point is None or PAREN_NUMBER.match(last_point.text[lang] or '') or
                  (last_point.number or '').isdigit()):
            # "(1) Unique identification and authentication": a numbered requirement enhancement (IEC 62443-4-2),
            # the heading of the text that follows it; "(1)" stays in the text as printed
            parent = letter_parent if last_point is not None else last_par
            last_point = recent = add(parent, 'AitPoint', 'pt', m.group(1), b)
            letter_parent, dash_parent, open_point = parent, None, last_point
            continue
        m = LETTER.match(b) or (NUMBER.match(b) if last_point is None and recent is None else None)
        if m:
            parent = letter_parent if last_point is not None else last_par
            last_point = recent = add(parent, 'AitPoint', 'pt', m.group(1), m.group(2).strip())
            letter_parent, dash_parent = parent, None
            # a point whose text does not end a sentence is a heading if a paragraph follows it (5.4 a); if a
            # list follows, it only introduces that list (6.4.4 c "for example,"); a point ending with "," or ";"
            # is part of a sentence that the paragraph after the list completes (IEC 60204-1 9.4.3.1 method c))
            open_point = last_point if not SENTENCE_END.search(last_point.text[lang]) and \
                not re.search(r'[,;]\s*$', last_point.text[lang]) else None
            continue
        m = NUMBER.match(b)
        if m and last_point is not None and recent is last_point and (last_point.number or '').isdigit() and \
                int(m.group(1)) == int(last_point.number) + 1:
            # a list numbered 1) 2) 3) is a list of points: 2) follows 1), it is not a sub-point of it (IEC
            # forewords)
            last_point = recent = add(letter_parent, 'AitPoint', 'pt', m.group(1), m.group(2).strip())
            open_point = last_point if not SENTENCE_END.search(last_point.text[lang]) and \
                not re.search(r'[,;]\s*$', last_point.text[lang]) else None
            continue
        if m:
            owner = recent if recent is not None else last_point
            # 2) is a sibling of 1): climb over numbered and roman items to the item that owns the numbered list
            while owner is not None and re.search(r'\.(sp\d+|r[ivx]+)$', owner.seqId):
                owner = next(c for c in children if c.seqId == owner.parentSeqId)
            if open_point is not None and owner is open_point:
                open_point = None
            recent = add(owner.seqId, 'AitSubPoint', 'sp', m.group(1), m.group(2).strip())
            continue
        m = DASH.match(b)
        if m:
            # dashes hang from the last list item when it does not end its sentence ("including", "such as"), else
            # from the paragraph that introduces them
            parent = dash_parent or (recent.seqId if recent is not None and not re.search(r'[.;]\s*$', recent.text[lang])
                                     else last_par)
            if open_point is not None and parent == open_point.seqId:
                open_point = None
            ptype = 'AitSubPoint' if re.search(r'\.(pt|sp|li)[0-9a-z]*$', parent) else 'AitPoint'
            recent = add(parent, ptype, 'li', None, b)
            dash_parent = parent
            continue
        if NOTE.match(b) or EXAMPLE.match(b):
            # a note inside an open list belongs to its last point (ISO 12100 5.2: the NOTE between c) and d))
            owner = open_point.seqId if open_point is not None else (last_point.seqId if last_point is not None
                                                                      else sid)
            # a note between two items of a list belongs to the item before it: two dash items (IEC 60204-1 clause
            # 1: NOTE 7 on sewing machines between "are sewing machines" and "are hoisting machines"), two numbered
            # sub-points, past the legends and the other notes in between (IEC 62443-4-1 Annex A: EXAMPLE 2 and
            # NOTE 2 inside b) 1), before b) 2)); a note that closes the list stays with the point that owns it
            nxt = next((x for x in bl[i + 1:] if not (NOTE.match(x) or EXAMPLE.match(x) or LEGEND.match(x)
                                                       or re.match(r'(?:where|dove)\s*$', x))), '')
            if dash_parent is not None and recent is not None and i + 1 < len(bl) and DASH.match(bl[i + 1]):
                owner = recent.seqId
            elif recent is not None and re.search(r'\.sp\d+$', recent.seqId) and NUMBER.match(nxt):
                owner = recent.seqId
            elif (dash_parent is not None and recent is not None and recent.parentSeqId == dash_parent
                  and last_point is not None and dash_parent != last_point.seqId):
                # after dash items of the paragraph (not of the open point) the note follows them, in the paragraph
                owner = dash_parent
            elif (last_par != sid and last_point is None and dash_parent is None and open_point is None
                  and re.search(r':\s*$', next(c for c in children if c.seqId == last_par).text[lang])
                  and i + 1 < len(bl) and (LETTER.match(bl[i + 1]) or DASH.match(bl[i + 1]))):
                # a note between a paragraph that introduces a list and the list belongs to that paragraph, before
                # its list (IEC 62443-4-1 Annex A: "... calculated as follows:" NOTE 1, then a) to d))
                owner = last_par
            note = add(owner, 'AitNote' if NOTE.match(b) else 'AitExample', 'n' if NOTE.match(b) else 'x', None, b)
            if i + 1 < len(bl) and DASH.match(bl[i + 1]) and not re.search(r'[.!?]\s*$', b):
                # a note that does not end its sentence introduces the list after it ("NOTE 2 The hazard envisaged
                # in this definition:" / "... either")
                last_par, dash_parent, recent = note.seqId, None, None
            continue
        if children and i and (re.search(r'\b(?:where|dove)\s*$', children[-1].text[lang]) or in_legend) and \
                (re.match(r'(?:where|dove)\s*$', b) or LEGEND.match(b)):
            # the legend of a formula ("where" and "NSCA is the number of ...") is part of the item that holds the
            # formula, not a paragraph that closes the lists
            children[-1].text[lang] += '\n' + b
            legend = True
            continue
        # a paragraph that introduces a new list a) ... closes the open list: it is not text of the last point
        # (IEC 62443-4-2 15.3.2: "b) VLAN", then "Layer 3 forwarding devices ...:" and a) b) c) again)
        nxt_letter = LETTER.match(bl[i + 1]) if i + 1 < len(bl) else None
        if open_point is not None and re.search(r':\s*$', b) and nxt_letter and nxt_letter.group(1) == 'a' and \
                re.fullmatch(r'[a-z]', open_point.number or ''):
            open_point = None
        # plain paragraph: inside a heading point, else of the clause; the lists before it are closed
        p = add(open_point.seqId if open_point is not None else sid, 'AitParagraph', 'p', None, b)
        if open_point is None:
            letter_parent = last_point = None
        dash_parent = recent = None
        last_par = p.seqId
    return own, children


def figure_text(fig, boxes, lang, all_boxes=None):
    """Text of a diagram modelled in config/figures: one line per box with its flows (targets by their label)."""
    by_id = {b.nodeId: b for b in (all_boxes or boxes)}
    # a diagram without decisions or terminals is a block diagram: its boxes are blocks, not steps of a process
    fig_of = lambda b: b.nodeId.split('.N_', 1)[0]
    flowchart = {fig_of(b) for b in by_id.values() if b.kind in ('flowDecision', 'flowTerminal')}
    lines = []
    for b in boxes:
        label = b.title.get(lang) or ''
        g = GEN_WORDS.get(lang, GEN_WORDS['en'])
        kind = {'flowDecision': g['decision'], 'flowTerminal': g['end']}.get(
            b.kind, g['step'] if fig_of(b) in flowchart else g['block'])
        flows = []
        for f in b.flows:
            to = by_id.get(f['to'])
            target = (to.title.get(lang) if to else f['to'])
            cond = f.get('condition') or f.get('label')
            flows.append(f'{cond}: {target}' if cond else f'{g["next"]}: {target}')
        extra = ''.join(f' [{k}: {v}]' for k, v in sorted(b.attrs.items()) if k in ('riskLevel', 'footnote'))
        lines.append(f'{kind}: {label}' + (' -> ' + '; '.join(flows) if flows else '') + extra)
    return '\n'.join(lines)


def split_blocks(text):
    """blocks() with a caption line inside a block made a block of its own (the caption of Figure 1 follows the
    footnote of its drawing in the same block)."""
    out = []
    for blk in blocks(text):
        lines = blk.split('\n')
        start = 0
        for k, line in enumerate(lines):
            if k < start:
                continue
            if CAPTION.match(line.strip()):
                if k > start:
                    out.append('\n'.join(lines[start:k]))
                # a caption title continued on the next line, which starts in lower case
                end = k + 1
                if re.search(r'[—–-]\s+\S', line) and end < len(lines) and re.match(r'[a-zà-ÿ]', lines[end].strip()):
                    end += 1
                out.append('\n'.join(lines[k:end]))
                start = end
        if start < len(lines):
            out.append('\n'.join(lines[start:]))
    return [b for b in out if b.strip()]


def separate(node, lang, tables, figures):
    """Blocks of a clause that are not its text: captions (titles of the figure or table items), the cells of its
    tables (read again by rows, pdf_tables) and the labels of a drawing printed just before its caption. Returns
    (remaining text, moved [(kind, number, block)])."""
    bl = split_blocks(node.text.get(lang) or '')
    keep, moved = [], []
    index = {}
    title = re.sub(r'\W+', '', (node.title.get(lang) or '').lower())
    k = -1000          # before every block of the text, in their order
    while bl and title and len(bl[0]) > 10 and re.sub(r'\W+', '', bl[0].lower()) in title:
        # the title printed again as the first lines of the text (front annexes: status, then title)
        k += 1
        moved.append(('title', None, bl[0]))
        index.setdefault(bl[0], []).append(k)
        bl = bl[1:]
    table_words = set().union(*(t['words'] for t in tables.values())) if tables else set()
    in_table = False
    for i, b in enumerate(bl):
        index.setdefault(b, []).append(i)
        m = CAPTION.match(b)
        if m and (m.group(2) in tables or m.group(2) in figures):
            kind = 'table' if m.group(1) in ('Table', 'Tabella') else 'figure'
            moved.append((kind, m.group(2), b))
            in_table = kind == 'table'
            if kind == 'figure':
                # labels of the drawing: the label-like blocks right before the caption
                # a question ends a decision box, not a sentence of the clause
                # a block ending with a footnote of the drawing ("a The first time ...") also belongs to the figure
                # a bullet of the clause is text, not a label: it ends with ";" or ":" as an item of a sentence, or is
                # a sentence ending with "." longer than a label, or cites the figure (IEC/TR 62443-3-1 6.2.2: "•
                # limiting data from/to the process control network;" above Figure 1; "• Training, etc." in the
                # drawing of ISO 12100 Figure 2 is a label)
                while keep and (re.match(r'^[a-e] [A-Z]', keep[-1]) or
                                re.match(r'^•', keep[-1]) and not re.search(r'[;:]\s*$', keep[-1]) and
                                not (re.search(r'\.\s*$', keep[-1]) and len(keep[-1]) > 40) and
                                not re.search(r'\((?:Figure|Figura)\s+' + re.escape(m.group(2)) + r'\)', keep[-1]) or
                                len(keep[-1]) < 600 and (
                        not re.search(r'[.;:!]\s*$', keep[-1]) or re.match(r'^[a-e] [A-Z]', keep[-1].split('\n')[-1]))):
                    moved.insert(len(moved) - 1, ('figure', m.group(2), keep.pop()))
            continue
        w = words(b)
        if in_table and w and len(w & table_words) / len(w) >= 0.7:
            moved.append(('table', None, b))
            continue
        in_table = False
        keep.append(b)
    # document order (the labels of a drawing were collected backwards from its caption)
    pos = {}
    order = []
    for kind, num, b in moved:
        k = pos.get(b, 0)
        pos[b] = k + 1
        order.append((index[b][k], (kind, num, b)))
    return '\n\n'.join(keep), [m for _, m in sorted(order, key=lambda x: x[0])]


def nodes_to_items(nodes, lang, tables=None, indexes=None):
    """Items of the nodes; `indexes` {annex letter: read_index result with column labels}: the annex is an index
    table, one row item per entry, the sentences under it stay paragraphs."""
    tables = tables or {}
    indexes = indexes or {}
    items = []
    by_node = {}
    kids = {}
    for n in nodes:
        kids.setdefault(n.parentId, []).append(n)
    seq = {}
    for n in nodes:
        if n.kind == 'document':
            continue
        typ = KIND_TYPE.get(n.kind)
        if n.kind in ('flowStep', 'flowDecision', 'flowTerminal'):
            typ = 'AitParagraph'
        sid = seq_id(n)
        parent = by_node[n.parentId].seqId if n.parentId in by_node else None
        it = Item(seqId=sid, parentSeqId=parent, type=typ, number=n.number, source=n.source.get('page', ''))
        title = n.title.get(lang) or ''
        if n.kind in ('flowStep', 'flowDecision', 'flowTerminal'):
            it.text[lang] = figure_text(None, [n], lang, [k for k in nodes if k.kind in ('flowStep', 'flowDecision',
                                                                                          'flowTerminal')])
            it.title[lang] = ''
        else:
            it.title[lang] = title
        if n.term.get(lang):
            it.term[lang] = n.term[lang]
        by_node[n.nodeId] = it
        items.append(it)
        if n.kind == 'figure':
            boxes = [k for k in nodes if k.parentId == n.nodeId or (k.parentId or '').startswith(n.nodeId + '.')]
            if boxes:
                it.text[lang] = figure_text(n, boxes, lang)
            continue
        if n.kind == 'table':
            t = tables.get(n.number)
            if t:
                it.text[lang] = GEN_WORDS.get(lang, GEN_WORDS['en'])['columns'] + ': ' + '; '.join(re.sub(r'(?<=[a-z])[ab]$', '', h) for h in t['header'] if h)
                for k, r in enumerate(t['rows'], 1):
                    row = Item(seqId=f'{sid}.r{k}', parentSeqId=sid, type='AitParagraph',
                               number=r[0] if r and re.match(r'^\d+$', r[0] or '') else None,
                               source=','.join(str(p) for p in t['pages']))
                    row.text[lang] = row_text(t['header'], r)
                    items.append(row)
            continue
        if n.kind in ('flowStep', 'flowDecision', 'flowTerminal'):
            continue
        text = n.text.get(lang) or ''
        ix = indexes.get(n.number) if n.kind == 'annex' else None
        if ix:
            it.text[lang] = GEN_WORDS.get(lang, GEN_WORDS['en'])['columns'] + ': ' + '; '.join(ix['labels'])
            for k, e in enumerate(ix['entries'], 1):
                row = Item(seqId=f'{sid}.r{k}', parentSeqId=sid, type='AitParagraph', source=it.source)
                row.text[lang] = row_text(ix['labels'], e)
                items.append(row)
            notes = set(ix['notes'])
            bl = split_blocks(text)
            kept = [b for b in bl if b.split('\n') and all(x.strip() in notes for x in b.split('\n'))]
            n.attrs['_moved'] = [('index', None, b) for b in bl if b not in kept]
            n.attrs['_index'] = ix
            clone = type(n)(**{**n.__dict__, 'text': {lang: '\n\n'.join(kept)}})
            own, children = split_clause(clone, lang, sid)
            if own:
                children.insert(0, Item(seqId=f'{sid}.p1', parentSeqId=sid, type='AitParagraph', source=it.source,
                                        text={lang: own}))
            items.extend(children)
            continue
        alts = [a['term'] for a in n.altTerms.get(lang, [])]
        if alts:
            # admitted terms and abbreviations are printed under the term: they stay in the text, as in the source
            text = '\n'.join(alts) + ('\n' + text if text else '')
        own_tables = {k.number: tables[k.number] for k in nodes if k.parentId == n.nodeId and k.kind == 'table'
                      and k.number in tables}
        own_figures = {k.number for k in nodes if k.parentId == n.nodeId and k.kind == 'figure'}
        clone = type(n)(**{**n.__dict__, 'text': {lang: text}})
        text, moved = separate(clone, lang, own_tables, own_figures)
        n.attrs['_moved'] = moved
        clone = type(n)(**{**n.__dict__, 'text': {lang: text}})
        own, children = split_clause(clone, lang, sid)
        it.text[lang] = own
        # children after the item, in document order; their sequence continues after the child clauses
        items.extend(children)
    # labels of drawings go to their figure (a figure item follows the clause that prints it)
    figs = [x for x in items if x.type == 'AitFigure']
    for n in nodes:
        for kind, num, b in n.attrs.get('_moved', []):
            # the figure with that number printed in this clause (a number can be printed twice, Figure H.4)
            fig = next((x for x in figs if x.number == num and x.parentSeqId == by_node.get(n.nodeId, Item('', '', '')).seqId),
                       next((x for x in figs if x.seqId == f'FIG{num}'), None))
            if kind == 'figure' and num and not CAPTION.match(b) and fig is not None:
                fig.text[lang] = ((fig.text.get(lang) or '') + '\n' + GEN_WORDS.get(lang, GEN_WORDS['en'])['labels'] + ': ' + ' / '.join(b.split('\n'))).strip()
    attach_refs(nodes, items, by_node, lang)
    for n in nodes:
        if n.attrs.get('_index'):
            norm_id = n.nodeId.split(':', 1)[0]
            ids = {x.seqId for x in items}
            for x in items:
                if x.parentSeqId == seq_id(n) and re.search(r'\.r\d+$', x.seqId):
                    cell = (n.attrs['_index']['entries'][int(x.seqId.rsplit('.r', 1)[1]) - 1] or [''])[-1]
                    refs, bad = index_refs(cell, ids)
                    x.refs = [ItemRef(raw=raw, toNormId=norm_id, toSeqId=sid) for raw, sid in refs]
                    n.attrs.setdefault('_unresolved', []).extend(bad)
    # order among siblings = document order (paragraphs of a clause come before its sub-clauses)
    for it in items:
        seq[it.parentSeqId] = seq.get(it.parentSeqId, 0) + 1
        it.sequence = seq[it.parentSeqId]
    return items


INDEX_REF = re.compile(r'^(?:(Clause|Annex|Table|Figure)\s+)?([A-Z]{1,2}|[A-Z]\.\d+(?:\.\d+)*|\d+(?:\.\d+)*)'
                       r'(?:\s+([a-z])\))?$')
INDEX_PREFIX = {'Annex': 'ANX', 'Table': 'TAB', 'Figure': 'FIG'}


def index_refs(cell, ids):
    """References of the clause column of an index: '3.29; 5.5.2.3.1 a); Clause 7 c); Annex B; Table B.1.1;
    3.30 to 3.34; Introduction'. Returns ([(raw, item id)], [unresolved raw]); 'numerous occurrences' is not a
    reference. A point is resolved to its item when the clause has one point with that letter, a table group
    (Table B.1.1) to its table."""
    refs, bad = [], []
    for raw in re.split(r'[;,]|\s+to\s+|\s+and\s+', cell):
        raw = raw.strip()
        if not raw or 'numerous' in raw or raw == 'occurrences' or raw.startswith('occurrences'):
            continue
        if raw == 'Introduction':
            refs.append((raw, 'INTRO'))
            continue
        # a stray full stop of the source ("3.21;.3.22") is not part of the number
        m = INDEX_REF.match(raw.lstrip('.'))
        if not m:
            bad.append(raw)
            continue
        kind, num, letter = m.groups()
        sid = INDEX_PREFIX.get(kind, '') + num
        while sid not in ids and '.' in sid and kind == 'Table':
            sid = sid.rsplit('.', 1)[0]
        if sid not in ids:
            bad.append(raw)
            continue
        if letter:
            pts = [i for i in ids if i.startswith(sid + '.') and i.endswith('.pt' + letter) and _clause_of(i, None) == sid]
            sid = pts[0] if len(pts) == 1 else sid
        refs.append((raw, sid))
    return refs, bad


def attach_refs(nodes, items, by_node, lang):
    """References of a node go to the item of that clause whose text contains them."""
    for n in nodes:
        it = by_node.get(n.nodeId)
        if not it:
            continue
        cands = [it] + [c for c in items if c.seqId.startswith(it.seqId + '.') and
                        c.type in ('AitParagraph', 'AitPoint', 'AitSubPoint', 'AitNote', 'AitExample') and
                        _clause_of(c.seqId, by_node) == it.seqId]
        for r in n.references:
            raw = re.sub(r'\s+', ' ', r.raw)
            holder = next((c for c in cands if raw in re.sub(r'\s+', ' ', c.text.get(lang) or '')), it)
            if n.attrs.get('_index') and holder is it:
                # a clause number of the index columns: the rows carry their references (index_refs)
                continue
            target = by_node[r.targetNodeId].seqId if r.targetNodeId in by_node else None
            if r.targetNodeId and not target:
                target = r.targetNodeId.split(':', 1)[1]
            holder.refs.append(ItemRef(raw=r.raw, toNormId=r.targetNormId, toSeqId=target, external=r.external))


def _clause_of(seq_id_, by_node):
    """The clause item an inner item belongs to: its id up to the first inner segment (p, pt, sp, li, n, x)."""
    parts = seq_id_.split('.')
    for i, p in enumerate(parts):
        if re.match(r'^(p|pt|sp|li|n|x)[0-9a-z]+$', p) and i > 0:
            return '.'.join(parts[:i])
    return seq_id_


def check_partition(nodes, items, lang):
    """Every clause text equals the text of its items (whitespace aside): errors for lost or duplicated text."""
    errors = []
    by_parent = {}
    for it in items:
        by_parent.setdefault(it.parentSeqId, []).append(it)

    def gather(it):
        out = [it.text.get(lang) or '']
        for c in by_parent.get(it.seqId, []):
            if c.type not in ('AitArticle', 'AitAnnex', 'AitFigure', 'AitTable', 'AitSection', 'AitPreamble'):
                out.extend(gather(c))
        return out

    by_sid = {it.seqId: it for it in items}
    for n in nodes:
        if n.kind in ('document', 'figure', 'table', 'flowStep', 'flowDecision', 'flowTerminal'):
            continue
        sid = seq_id(n)
        src = (n.text.get(lang) or '')
        alts = [a['term'] for a in n.altTerms.get(lang, [])]
        src = '\n'.join(alts + [src]) if alts else src
        # the blocks moved to a figure or table item (captions, cells, drawing labels) are taken out in document
        # order, block by block: a caption "Table B.3" must not remove the words of "Table B.3 includes ..."
        bl = split_blocks(src)
        moved = [b for _, _, b in n.attrs.get('_moved', [])]
        kept = []
        for blk in bl:
            if moved and blk == moved[0]:
                moved.pop(0)
            else:
                kept.append(blk)
        if moved:
            errors.append(f'{sid}: {len(moved)} moved blocks not found in the clause, first {moved[0][:60]!r}')
        ix = n.attrs.get('_index')
        if n.attrs.get('_unresolved'):
            errors.append(f'{sid}: index references not resolved {n.attrs["_unresolved"][:8]}')
        if ix:
            # the index rows hold the words of the index blocks, column headings and letter headings aside
            have = Counter(w for b in (b for k, _, b in n.attrs['_moved'] if k == 'index') for w in b.split())
            rows = Counter(w for e in ix['entries'] for c in e for w in c.split())
            lost, extra = have - rows - Counter(ix['dropped']), rows - have
            if lost or extra:
                errors.append(f'{sid}: index rows differ from the annex text, lost {list(lost)[:8]}, '
                              f'extra {list(extra)[:8]}')
        # list markers a) 1) i) at the start of a block are kept in itemNumber, not in the item text (inside a block
        # "10)" can be the end of a wrapped reference: "IEC 60417-5019 (DB:2002-" / "10) or by ...")
        src = '\n\n'.join(re.sub(r'^\s*(?:(?:[a-z]|\d{1,2}|i|ii|iii|iv|v|vi|vii|viii|ix|x)\)|\d{1,2}\.)\s+', '', blk)
                          for blk in kept)
        want = re.sub(r'[\s⎯—–•]+', '', src)
        parts = gather(by_sid[sid])
        if ix:
            # the index annex: its own text names the columns, its rows were checked word by word above
            parts = [t for c in by_parent.get(sid, []) if not re.search(r'\.r\d+$', c.seqId) for t in gather(c)]
        got = re.sub(r'[\s⎯—–•]+', '', ''.join(parts))
        if want != got:
            k = next((i for i, (x, y) in enumerate(zip(want, got)) if x != y), min(len(want), len(got)))
            errors.append(f'{sid}: text of the items differs from the clause ({len(got)} vs {len(want)} characters); '
                          f'clause ...{want[max(0, k - 30):k + 30]!r}, items ...{got[max(0, k - 30):k + 30]!r}')
    return errors
