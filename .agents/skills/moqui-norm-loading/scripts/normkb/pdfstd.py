"""Reader for ISO/IEC/EN standards published as PDF with extractable text.

Text comes from `pdftotext -layout`, page by page. Pages of other languages (bilingual CEI editions alternate
English and Italian pages) and boilerplate lines are removed, then a line-based state machine finds clause, definition
and annex headings. A heading number is accepted only when it continues the numbering already seen, so list items and
values do not become clauses. The table of contents of the standard is parsed separately and used as a check.
"""
import re
import subprocess

from .ir import Node, Reference, clean_text, node_id
from .refs import known_norm

EN_WORDS = set('the of and shall be to is for in with this that are or which by on'.split())
IT_WORDS = set('il di e deve essere la per con questo che sono o del della dei delle le un una nel'.split())

COMMON_BOILERPLATE = [
    r'^\s*(\d+|[ivxlc]+)?\s*©\s*(ISO|IEC|CEN|BSI)\b.*$',
    r'^\s*(All rights reserved|Licen[cs]ed to:.*|Generated on .*|NO COPYING WITHOUT .*|raising standards worldwide.*)$',
    r'^\s*\d{1,3}\s*$',
    r'^\s*This page deliberately left blank\s*$',
]

HEADING = re.compile(r'^\s{0,3}(\d{1,2}(?:\.\d{1,2}){0,6})(?:\s{2,}|\s(?=[A-ZÀ-Ý]))(\S.{0,160}?)\s*$')
# a definition heading whose term starts in lower case ("3.2.3 sistema di controllo"), accepted only inside the
# terms-and-definitions clause
HEADING_TERM = re.compile(r'^\s{0,3}(\d{1,2}(?:\.\d{1,2}){1,6})\s+([a-zà-ÿ(].{0,160}?)\s*$')
NUMBER_ONLY = re.compile(r'^\s{0,3}(\d{1,2}(?:\.\d{1,2}){1,6})\s*$')
ANNEX_CLAUSE = re.compile(r'^\s{0,3}([A-Z]{1,2}\.\d{1,2}(?:\.\d{1,2}){0,5})(?:\s{2,}|\s(?=[A-ZÀ-Ý]))(\S.{0,160}?)\s*$')
# the same with a deeper indentation, accepted only when the table of contents confirms the heading
HEADING_LOOSE = re.compile(HEADING.pattern.replace(r'^\s{0,3}', r'^\s{0,8}', 1))
ANNEX_CLAUSE_LOOSE = re.compile(ANNEX_CLAUSE.pattern.replace(r'^\s{0,3}', r'^\s{0,8}', 1))
ANNEX_NUMBER_ONLY = re.compile(r'^\s{0,3}([A-Z]{1,2}\.\d{1,2}(?:\.\d{1,2}){0,5})\s*$')
LIST_ITEM = re.compile(r'^(?:[–—⎯•-]|[a-z]\)|\d{1,2}\))\s')
# a designation printed under the preferred term of a definition: at most four words, no punctuation
DESIGNATION = re.compile(r"^[\w()/'’-]+(?: [\w()/'’-]+){0,3}$")

# The words a standard prints for its structure, by language of the edition. Front sections map to (path, kind).
WORDS = {
    'en': {
        'annex': 'Annex', 'annexStatus': 'normative|informative', 'bibliography': 'Bibliography',
        'figure': 'Figure', 'table': 'Table', 'contents': 'Contents|CONTENTS', 'scope': 'Scope',
        'terms': 'Terms and definitions|Terms, definitions', 'note': 'NOTE',
        # WARNING: national deviations of the European edition ("differences exist in some countries")
        'front': {'European foreword': ('EUFOREWORD', 'preamble'),
                  'Foreword': ('FOREWORD', 'preamble'), 'Endorsement notice': ('ENDORSEMENT', 'preamble'),
                  'Introduction': ('INTRO', 'clause'), 'WARNING': ('DEVIATIONS', 'preamble')},
        # back matter that is not norm text: alphabetical index, other-language headings
        # back cover of the national edition (BSI) is not text of the standard
        'skip': 'Index|I\\s?n\\s?d\\s?e\\s?x|Indice analitico|Indice|Bibliografia|Alphabetical index|'
                'British Standards Institution \\(BSI\\)',
        # words before a bare subclause number that make it a reference ("see 5.3", "(5.4 and Annex B)")
        'refBefore': r'\b[Ss]ee\b|\balso\b|\bin\b|\bof\b|\bto\b|\band\b|\bor\b|\(|,|\bclauses?\b|\bsubclauses?\b|\bClauses?\b',
        'clause': 'Clause', 'of': r'of(?:\s+the)?',
    },
    'it': {
        'annex': 'Allegato', 'annexStatus': 'normativo|informativo', 'bibliography': 'Bibliografia',
        'figure': 'Figura', 'table': 'Tabella', 'contents': 'Indice|INDICE', 'scope': 'Campo di applicazione',
        'terms': 'Termini e definizioni|Termini, definizioni', 'note': 'NOTA',
        'front': {'Prefazione europea': ('EUFOREWORD', 'preamble'),
                  'Prefazione': ('FOREWORD', 'preamble'), 'Avviso di adozione': ('ENDORSEMENT', 'preamble'),
                  'Introduzione': ('INTRO', 'clause'), 'AVVERTENZA': ('DEVIATIONS', 'preamble')},
        'skip': 'Indice analitico|Index|Alphabetical index|Bibliography',
        'refBefore': r'\b[Vv]ed[ia]\b|\banche\b|\bin\b|\bdi\b|\ba(?:i|l|lla|lle|llo|gli)?\b|\be\b|\bed\b|\bo\b|\bde(?:l|lla|i|lle)\b|'
                     r'\bne(?:l|lla|i|lle)\b|\bdal(?:la)?\b|\bsecondo\b|\(|,|\b[Pp]aragraf[oi]\b|\b[Aa]rticol[oi]\b|'
                     r'\bpunt[oi]\b|\bsezion[ei]\b',
        'clause': 'Articolo', 'of': r"del(?:la|lo)?|dell['’]",
    },
}


def words_of(lang):
    if lang not in WORDS:
        raise ValueError(f'no structure words for language {lang!r}: add them to pdfstd.WORDS')
    return WORDS[lang]


def front_names(w):
    return '|'.join(sorted(set(w['front']) | {k.upper() for k in w['front']}, key=len, reverse=True))


class Patterns:
    """Language-dependent patterns of the reader."""
    def __init__(self, lang):
        w = self.words = words_of(lang)
        self.annex = re.compile(r'^\s{0,70}' + w['annex'] + r'\s+([A-Z]{1,2})\s*$')
        self.annex_status = re.compile(r'^\s*\((' + w['annexStatus'] + r')\)\s*$')
        self.biblio = re.compile(r'^\s{0,70}(?:' + w['bibliography'] + r')\s*$')
        self.skip = re.compile(r'^\s{0,70}(' + w['skip'] + r')\s*$|^\s*_{5,}\s*$')
        # caption of a figure or table: "Figure 1 — Title", "Table 4 – Title", or "Table B.1" alone
        self.caption = re.compile(r'^\s*(' + w['figure'] + '|' + w['table'] +
                                  r')\s+(\d{1,2}|[A-Z]{1,2}\.\d{1,2})(?:\s*[—–-]{1,2}\s*(\S.*?)|\s*\((?:continued|segue|\d+ (?:di|of) \d+)\))?\s*$')
        # front matter sections printed before "1 Scope" (the table of contents lists them with dots)
        self.front_section = re.compile(r'^\s{0,70}(' + front_names(w) + r')\s*$')
        self.front_end = re.compile(r'^\s{0,70}(' + w['contents'] + '|' + front_names(w) + r')\s*$|^\s{0,70}' +
                                    w['annex'] + r'\s+Z')
        # end of a European annex printed in the front matter: the next front heading, even with more on the line,
        # but not a sentence of the annex that starts with such a word ("WARNING — Other requirements ...")
        self.front_annex_end = re.compile(r'^\s*(' + w['contents'] + '|' + front_names(w) + '|' + w['annex'] +
                                          r'\s+Z)(?!\s*[—–-])')
        self.toc_line = re.compile(r'^\s*((?:\d{1,2}(?:\.\d{1,2}){0,5})|' + w['annex'] +
                                   r'\s+[A-Z]{1,2}|[A-Z]{1,2}\.\d{1,2}(?:\.\d{1,2}){0,4})\s+(.+?)\s*\.{3,}\s*\d+\s*$')
        self.toc_annex = re.compile(r'^' + w['annex'] + r'\s+')
        # first line of a wrapped table-of-contents entry
        self.toc_start = re.compile(r'^\s*(?:\d{1,2}(?:\.\d{1,2}){0,5}|' + w['annex'] + r'\s+[A-Z]{1,2}|[A-Z]{1,2}\.\d{1,2}(?:\.\d{1,2}){0,4})\s+\S')
        self.scope = re.compile(r'(?:' + w['scope'] + r')\b')
        self.terms = re.compile(r'(?:' + w['terms'] + r')')

    def front_key(self, name):
        return next(v for k, v in self.words['front'].items() if k.lower() == name.lower())


# English patterns, kept as module names for callers and tests
_EN = Patterns('en')
ANNEX, ANNEX_STATUS, BIBLIO, SKIP_START = _EN.annex, _EN.annex_status, _EN.biblio, _EN.skip
CAPTION, FRONT_SECTION, FRONT_END, TOC_LINE = _EN.caption, _EN.front_section, _EN.front_end, _EN.toc_line

def page_language(text):
    w = re.findall(r'[a-zà-ù]+', text.lower())
    e = sum(1 for x in w if x in EN_WORDS)
    i = sum(1 for x in w if x in IT_WORDS)
    if e + i < 15:
        return None
    if e > i * 1.5:
        return 'en'
    if i > e * 1.5:
        return 'it'
    return 'mix'


def split_designations(nodes, lang):
    """Move the admitted terms and abbreviations printed under the preferred term of a definition out of its text.

    In ISO and IEC standards the preferred term is the heading; the lines right under it, before the definition, are
    other designations of the same concept (\"danger zone\" under 3.11 hazard zone, \"SPE\" under 3.28.5). Such a
    line is short (at most four words), has no punctuation, and is followed by more definition text that is not a
    NOTE ("Note 1 to entry"), an example or a source reference (IEC 62443-3-2 3.1.11 "chance of something
    happening" is the definition). All capitals means abbreviation, otherwise admitted term."""
    note = words_of(lang)['note']
    for n in nodes:
        if n.kind != 'definition':
            continue
        lines = (n.text.get(lang) or '').split('\n')
        alts = []
        while True:
            idx = [k for k, l in enumerate(lines) if l.strip()]
            if len(idx) < 2:
                break
            first, nxt = lines[idx[0]].strip(), lines[idx[1]].strip()
            # a short line that introduces a list ("componente in cui" then "– i modi di guasto…") is definition text
            # the IEC form of a note to the definition ("Note 1 to entry: ...") and an example follow the definition
            if not DESIGNATION.match(first) or nxt.startswith((note, '[')) or LIST_ITEM.match(nxt) or \
                    re.match(r'(?:Note \d+ to entry|EXAMPLE|ESEMPIO)\b', nxt):
                break
            alts.append({'term': first, 'status': 'abbreviation' if first.isupper() else 'admitted'})
            lines = lines[idx[0] + 1:]
        if alts:
            n.altTerms[lang] = alts
            n.text[lang] = '\n'.join(lines).strip()
    return nodes


# characters of the Symbol font that pdftotext leaves in the private use area (U+F020-U+F0FF): the Adobe Symbol
# encoding gives their Unicode (U+F06C is lambda, U+F0B4 the multiplication sign); the pieces of tall brackets
# (U+F0E6-U+F0EF, U+F0F6-U+F0FE) stay for linearize_formulas
SYMBOL = dict(zip(range(0xF020, 0xF07F),
                  ' !∀#∃%&∋()*+,−./0123456789:;<=>?≅ΑΒΧΔΕΦΓΗΙϑΚΛΜΝΟΠΘΡΣΤΥςΩΞΨΖ[∴]⊥_‾αβχδεφγηιϕκλμνοπθρστυϖωξψζ{|}∼'))
SYMBOL.update(zip(range(0xF0A0, 0xF0E6),
                  '€ϒ′≤⁄∞ƒ♣♦♥♠↔←↑→↓°±″≥×∝∂•÷≠≡≈…⏐⎯↵ℵℑℜ℘⊗⊕∅∩∪⊃⊇⊄⊂⊆∈∉∠∇®©™∏√⋅¬∧∨⇔⇐⇑⇒⇓◊〈®©™∑'))
SYMBOL.update(zip(range(0xF0F1, 0xF0F6), '〉∫⌠⎮⌡'))
# Wingdings characters in the private use area (pdftotext keeps the code, not the font): IEC 62443-3-3 Table B.1
# marks the requirements of each level with U+F0FC, a check mark in Wingdings and a brace piece in Symbol
WINGDINGS = {0xF0FC: '✓', 0xF0FB: '✗', 0xF0FD: '☒', 0xF0FE: '☑', 0xF06C: '●', 0xF06E: '■', 0xF0A7: '▪',
             0xF0A8: '◻', 0xF06F: '❏', 0xF0D8: '➢', 0xF0E0: '➔', 0xF076: '❖', 0xF09F: '•'}


def page_private_fonts(page):
    """{private use character: font name} of a PyMuPDF page."""
    found = {}
    for b in page.get_text('dict')['blocks']:
        for ln in b.get('lines', []):
            for sp in ln['spans']:
                for c in sp['text']:
                    if 0xE000 <= ord(c) <= 0xF8FF:
                        found.setdefault(c, sp['font'])
    return found


def private_use_fonts(pdf):
    """{page number: {private use character: font name}} from the page geometry."""
    import pymupdf
    return {pno: f for pno, page in enumerate(pymupdf.open(pdf), 1) if (f := page_private_fonts(page))}


def dingbats(fonts):
    """translate table of the Wingdings characters of a page."""
    return {ord(c): WINGDINGS.get(ord(c), c) for c, f in fonts.items() if 'wingding' in f.lower()}


# serif copyright, registered and trademark signs of the Adobe private range (IEC page headers "© IEC 2019")
SYMBOL.update({0xF6D9: '©', 0xF6DA: '®', 0xF6DB: '™'})
# Greek capitals drawn like Latin ones are Latin in these texts ("MTTF" set in the Symbol font)
SYMBOL.update({0xF020 + ord(c) - 0x20: c for c in 'ABEZHIKMNOPTXY'})

# pieces of tall brackets (private use area, two fonts): the middle pieces stand for the bracket, the top and bottom
# pieces carry nothing more
BRACKET_MIDDLE = {'\uf8ec': '(', '\uf8f7': ')', '\uf8ef': '[', '\uf8fa': ']', '\uf8f2': '{', '\uf8fd': '}',
                  '\uf0e7': '(', '\uf0f7': ')', '\uf0ea': '[', '\uf0fa': ']', '\uf0ed': '{', '\uf0fd': '}'}
BRACKET_ENDS = re.compile('[\uf8eb\uf8ed\uf8ee\uf8f0\uf8f1\uf8f3\uf8f4\uf8f6\uf8f8\uf8f9\uf8fb\uf8fc\uf8fe'
                          '\uf0e6\uf0e8\uf0e9\uf0eb\uf0ec\uf0ee\uf0ef\uf0f6\uf0f8\uf0f9\uf0fb\uf0fc\uf0fe]')
MATH_OP = re.compile(r'[=×−+·\-/<>≤≥]')


def _groups(line, mid):
    """Words of a numerator or denominator line grouped into terms: two words are one term unless the middle line
    has a sign in the columns between them ("2 U0" over "Z s (m) ≤    ×" is 2 and U0)."""
    words = [(m.start(), m.end(), m.group(0)) for m in re.finditer(r'\S+', line)]
    out = []
    for w in words:
        between = mid[out[-1][1]:w[0]] if out else ''
        if out and w[0] - out[-1][1] <= 1 and not between.strip():
            out[-1] = (out[-1][0], w[1], out[-1][2] + ' ' + w[2])
        else:
            out.append(w)
    return out


def linearize_formulas(page):
    """Fractions printed on three lines ("NSCA" above, "EXAMPLE 2 1 − (    ) × 100", "NSR" below) written on one
    line as numerator/denominator in their slot of the middle line; tall brackets as ( ). Only a triple with bracket
    pieces or an operator next to the slot is a formula: a table column with an empty cell is not."""
    lines = page.split('\n')
    out, i = [], 0
    while i < len(lines):
        if i + 2 < len(lines) and lines[i + 1].strip():
            num, mid, den = lines[i], lines[i + 1], lines[i + 2]
            brackets = bool(BRACKET_ENDS.search(num + den)) or any(c in mid for c in BRACKET_MIDDLE)
            m_line = ''.join(BRACKET_MIDDLE.get(c, c) for c in mid)
            nt = _groups(BRACKET_ENDS.sub(' ', num), m_line)
            dt = _groups(BRACKET_ENDS.sub(' ', den), m_line)
            if nt and len(nt) == len(dt) and len(nt) <= 4 and \
                    all(len(t) <= 16 and len(b) <= 16 and a0 < b1 + 2 and b0 < a1 + 2
                        for (a0, a1, t), (b0, b1, b) in zip(nt, dt)):
                # slots: the inside of an empty bracket pair, a gap of two spaces or more, the end of the line
                end = len(m_line.rstrip())
                slots = [(g.start(), g.end()) for g in re.finditer(r'(?<=\() +(?=\))', m_line)] + \
                    [(g.start(), g.end()) for g in re.finditer(r'(?<![(\s]) {2,}(?![)\s])', m_line) if g.end() < end] + \
                    [(end, end + 1)]
                spots = []
                for (a0, a1, t), (b0, b1, b) in zip(nt, dt):
                    center = (min(a0, b0) + max(a1, b1)) / 2
                    g = min(slots, key=lambda g: abs((g[0] + g[1]) / 2 - center))
                    if abs((g[0] + g[1]) / 2 - center) > 4 or g in [x for x, _ in spots] or not (
                            brackets or MATH_OP.search(m_line[max(0, g[0] - 3):g[1] + 3])):
                        spots = None
                        break
                    spots.append((g, f'{t}/{b}' if ' ' not in t + b else f'({t})/({b})'))
                if spots:
                    for (g0, g1), frac in sorted(spots, key=lambda x: -x[0][0]):
                        m_line = m_line[:g0].rstrip() + ' ' + frac + ' ' + m_line[g1:].lstrip()
                    out.append(m_line.rstrip())
                    i += 3
                    continue
        out.append(lines[i])
        i += 1
    return '\n'.join(out)


# runs of bracket pieces left on one line ("⎡⎣ DC × T2 ... ⎤⎦" in IEC 62061 (H.9)) are one bracket each
PIECE_RUNS = [(re.compile(r'[\uf8eb\uf8ec\uf8ed\uf0e6\uf0e7\uf0e8]+'), '('),
              (re.compile(r'[\uf8f6\uf8f7\uf8f8\uf0f6\uf0f7\uf0f8]+'), ')'),
              (re.compile(r'[\uf8ee\uf8ef\uf8f0\uf0e9\uf0ea\uf0eb]+'), '['),
              (re.compile(r'[\uf8f9\uf8fa\uf8fb\uf0f9\uf0fa\uf0fb]+'), ']'),
              (re.compile(r'[\uf8f1\uf8f2\uf8f3\uf8f4\uf0ec\uf0ed\uf0ee\uf0ef]+'), '{'),
              (re.compile(r'[\uf8fc\uf8fd\uf8fe\uf0fc\uf0fd\uf0fe]+'), '}')]


def single_line_brackets(page):
    for pat, ch in PIECE_RUNS:
        page = pat.sub(ch, page)
    return page


PUBLISHER_PAGE = re.compile(r'THIS PUBLICATION IS COPYRIGHT PROTECTED|obtained this publication from an authori[sz]ed\s+distributor')


def publisher_page(page):
    """A page of the publisher, not of the norm: the copyright page and the cover of an IEC publication (IEC 62443
    parts reproduce them after Annex ZA of the CEI edition)."""
    return bool(PUBLISHER_PAGE.search(page))


def squash(text):
    """Text compared without case, spacing and punctuation (pdftotext splits words: "rigu arda")."""
    return re.sub(r'[\W_]+', '', text.lower())


def drop_title_tail(body, title):
    """Remove from the end of a front section the lines that repeat the title of the standard, printed above the
    first clause ("SICUREZZA DEL MACCHINARIO – …" before "1 Campo di applicazione")."""
    target = squash(title or '')
    if not target:
        return body
    k = len(body)
    while k > 0 and not body[k - 1][1].strip():
        k -= 1
    for start in range(max(0, k - 6), k):
        tail = squash(' '.join(l for _, l in body[start:k]))
        if len(tail) > 20 and tail in target:
            return body[:start]
    return body


def number_key(num):
    return tuple(int(x) if x.isdigit() else x for x in re.split(r'\.', num))


def plausible_next(prev_numbers, num):
    """True if num continues the numbering: a first child of the last heading, or a following sibling (within a
    small gap) of the last heading or of one of its ancestors."""
    parts = num.split('.')
    if not prev_numbers:
        return parts == ['1']
    last = prev_numbers[-1].split('.')
    if parts[:-1] == last and parts[-1] == '1':
        return True
    for depth in range(len(last), 0, -1):
        anc = last[:depth]
        if len(parts) == depth and parts[:-1] == anc[:-1] and parts[-1].isdigit() and anc[-1].isdigit():
            if 1 <= int(parts[-1]) - int(anc[-1]) <= 2:
                return True
    return False


LIST_MARK = re.compile(r'^(\s*[⎯—–•-]\s+)\S')


def join_list_continuations(buf):
    """Join a list item broken by the page or by a paragraph gap with its continuation: a line in lower case that is
    aligned with the text of the item, not with its marker, after blank lines (IEC/TR 62443-3-1 5.4.4 "... and
    compromising" / "the system." on the next page; IEC 62061 H.1). A line back at the marker or further left completes
    the sentence that introduced the list ("sia tramite: • ...; o • ..." / "che tramite controllo ...", IEC 62061
    6.7.3) and stays a paragraph. buf: [(page, line)], changed in place."""
    text_col = None
    k = 0
    while k < len(buf):
        line = buf[k][1]
        if not line.strip():
            k += 1
            continue
        m = LIST_MARK.match(line)
        if m:
            text_col = len(m.group(1))
        elif text_col is not None:
            indent = len(line) - len(line.lstrip())
            prev = max(j for j in range(k) if buf[j][1].strip())
            if indent < text_col - 1:
                text_col = None
            elif prev < k - 1 and re.match(r'[a-zà-ÿ]', line.lstrip()) and \
                    not re.search(r'[.;:,]\s*$|\b(?:and|or|e|o|oppure)\s*$', buf[prev][1]):
                del buf[prev + 1:k]
                k = prev + 1
        k += 1


class PdfStandardReader:
    def __init__(self, norm_id, pdf, language='en', boilerplate=(), title=None, first_page=1, bilingual=True,
                 definitions_clause=None, paragraph_gaps=False, line_fixes=()):
        """bilingual: the edition alternates pages of two languages and the pages of the other one are dropped; a
        monolingual edition keeps every page (a bibliography of English titles is still part of an Italian edition). definitions_clause: number of the terms-and-definitions
        clause when it is not a top-level clause ("3.2" in IEC 62061). paragraph_gaps: the text has no blank line
        between paragraphs (CEI EN 60204-1): a blank line is put before every line that the page geometry shows as
        the start of a paragraph. line_fixes: [pattern, replacement] pairs applied to every line of the text before it
        is read, for defects of a conversion (IEC/TR 62443-3-1: link anchors "139H" after the contents entries,
        page numbers printed "1 2")."""
        self.normId = norm_id
        self.pdf = pdf
        self.language = language
        self.p = Patterns(language)
        self.bilingual = bilingual
        self.definitions_clause = definitions_clause
        self.boiler = [re.compile(p) for p in list(COMMON_BOILERPLATE) + list(boilerplate)]
        self.title = title
        self.first_page = first_page
        self.nodes = []
        self.report = {}
        self.front_captions = set()
        self.paragraph_gaps = paragraph_gaps
        self.line_fixes = [(re.compile(a, re.M), b) for a, b in line_fixes]

    # ---------- text ----------
    @staticmethod
    def line_key(text):
        # the same alphabet on both sides: pdftotext lines carry the Symbol characters already mapped
        return re.sub(r'\s+', '', text.translate(SYMBOL))[:30]

    def paragraph_starts(self):
        """{page number: Counter of line keys} of the lines that start a paragraph: the space above the line is more
        than 1.4 times the font size of the line before it (lines of one paragraph are about 1.15 apart)."""
        import pymupdf
        from collections import Counter
        out = {}
        for pno, page in enumerate(pymupdf.open(self.pdf), 1):
            lines = []
            for b in page.get_text('dict')['blocks']:
                for ln in b.get('lines', []):
                    text = ''.join(sp['text'] for sp in ln['spans']).strip()
                    if text:
                        lines.append((ln['bbox'][1], ln['bbox'][0], max(sp['size'] for sp in ln['spans']), text))
            lines.sort()
            starts = Counter()
            prev = None
            for y, x, size, text in lines:
                if prev is not None and y - prev[0] > 1.4 * prev[2]:
                    starts[self.line_key(text)] += 1
                if prev is None or y - prev[0] > 0.5:
                    prev = (y, x, size)
            out[pno] = starts
        return out
    def pages(self):
        out = subprocess.run(['pdftotext', '-layout', self.pdf, '-'], capture_output=True, text=True, check=True)
        fonts = private_use_fonts(self.pdf)
        pages = [single_line_brackets(linearize_formulas(p.translate(dingbats(fonts.get(k + 1, {}))))).translate(SYMBOL)
                 for k, p in enumerate(out.stdout.split('\f'))]
        for pattern, repl in self.line_fixes:
            pages = [pattern.sub(repl, p) for p in pages]
        return pages

    def page_languages(self, pages):
        """Language of each page. A bilingual CEI edition alternates the two languages page by page from its first
        page of the other language: the alternation found on the pages detected with confidence decides every page
        (an Italian page listing English titles, as in the bibliography, is still an Italian page)."""
        langs = [page_language(p) for p in pages]
        if not self.bilingual:
            return langs
        other = next((k for k, lg in enumerate(langs) if lg not in (None, 'mix', self.language)), None)
        if other is None or other == 0:
            return langs
        start = other - 1
        votes = {0: {}, 1: {}}
        for k in range(start, len(langs)):
            if langs[k] not in (None, 'mix'):
                votes[k % 2][langs[k]] = votes[k % 2].get(langs[k], 0) + 1
        own = max((0, 1), key=lambda par: votes[par].get(self.language, 0) - votes[par].get('it' if self.language != 'it' else 'en', 0))
        # the alternation holds between the first and the last pair of pages detected as own language then other
        # language at the expected parity; the cover pages and a trailing national index stay as detected
        pairs = [k for k in range(len(langs) - 1) if k % 2 == own and langs[k] == self.language
                 and langs[k + 1] not in (None, 'mix', self.language)]
        if not pairs:
            return langs
        first, last = pairs[0], pairs[-1] + 1
        out = list(langs)
        for k in range(first, last + 1):
            out[k] = self.language if k % 2 == own else 'other'
        self.report['languageCorrected'] = [k + 1 for k in range(first, last + 1)
                                            if langs[k] not in (None, 'mix') and (langs[k] == self.language) != (out[k] == self.language)]
        return out

    def lines(self):
        result = []
        self.kept_pages = set()      # pages of the language of the edition (the table reader reads only these)
        starts_by_page = self.paragraph_starts() if self.paragraph_gaps else None
        kept, dropped = 0, 0
        pages = self.pages()
        langs = self.page_languages(pages)
        for pno, p in enumerate(pages, 1):
            if pno < self.first_page:
                continue
            lang = langs[pno - 1]
            if self.bilingual and lang is not None and lang != self.language:
                dropped += 1
                continue
            if publisher_page(p):
                # cover and copyright pages of the international publication reproduced inside a national edition
                dropped += 1
                continue
            kept += 1
            self.kept_pages.add(pno)
            self.report['sourceChars'] = self.report.get('sourceChars', 0) + len(re.sub(r'\s+', ' ', p))
            starts = starts_by_page.get(pno) if starts_by_page else None
            for line in p.split('\n'):
                line = line.rstrip()
                if any(b.match(line) for b in self.boiler):
                    continue
                key = self.line_key(line)
                if starts and key and starts[key] > 0 and result and result[-1][1].strip():
                    starts[key] -= 1
                    result.append((pno, ''))
                result.append((pno, line))
        self.report['pagesKept'], self.report['pagesDropped'] = kept, dropped
        return result

    # ---------- table of contents ----------
    def toc(self, lines):
        """Entries (number, title) of the table of contents. A long title wraps: its first line has no leader dots and
        the entry ends on the line that has them ("Allegato ZZ (informativo) Rapporto tra …" / "… soddisfare …. 149")."""
        entries = []
        pending = None
        for _, line in lines:
            m = self.p.toc_line.match(line)
            if not m and pending is not None and line.strip():
                m = self.p.toc_line.match(pending + ' ' + line.strip())
                if m:
                    pending = None
                elif re.search(r'\.{3,}', line) or len(pending) > 400:
                    pending = None
                else:
                    pending += ' ' + line.strip()
                    continue
            if m:
                pending = None
                num = self.p.toc_annex.sub('ANNEX ', m.group(1))
                entries.append((num, re.sub(r'\s+', ' ', m.group(2))))
            elif self.p.toc_start.match(line) and not re.search(r'\.{3,}', line):
                pending = line.strip()
        self.toc_titles = dict(entries)
        return entries

    # ---------- segmentation ----------
    def read(self):
        lines = self.lines()
        toc = self.toc(lines)
        self.report['tocEntries'] = len(toc)
        start = self.find_body_start(lines)
        doc = self.add('DOC', None, 'document', None, title=self.title or self.normId)
        self.read_front_annexes(lines[:start], doc)
        self.read_front_sections(lines[:start], doc)
        current = doc
        numbers = []          # clause numbers accepted so far (main body)
        untitled = set()      # clause numbers printed without a title
        annex_numbers = []    # clause numbers inside the current annex
        by_number = {}
        annex = None
        buf = []
        i = start
        in_defs = False
        captions = set(self.front_captions)   # (kind, number) of figures and tables already met (captions repeat)
        captions_title = {}                    # (kind, number) -> title of its first caption

        footnotes = []

        def flush():
            if current is not None and footnotes:
                buf.extend([(0, ''), *((0, f) for note in footnotes for f in (note, ''))])
            footnotes.clear()
            if buf and current is None:
                buf.clear()
                return
            if buf and current is not None:
                n = self.by_id[current]
                join_list_continuations(buf)
                txt = clean_text('\n'.join(l for _, l in buf))
                n.text[self.language] = (n.text.get(self.language, '') + '\n' + txt).strip()
            buf.clear()

        while i < len(lines):
            pno, line = lines[i]
            if not line.strip():
                buf.append((pno, ''))
                i += 1
                continue
            m = self.p.annex.match(line)
            nxt = self.next_text(lines, i)
            if m and nxt and self.p.annex_status.match(nxt):
                flush()
                letter = m.group(1)
                title_lines, j = [], i + 1
                toc_title = squash(self.toc_titles.get(f'ANNEX {letter}', ''))
                while j < len(lines) and len(title_lines) < 4:
                    t = lines[j][1].strip()
                    if t:
                        if ANNEX_CLAUSE.match(lines[j][1]) or HEADING.match(lines[j][1]):
                            break
                        # the table of contents knows the title: stop at the first line that is not part of it
                        if toc_title and title_lines and not toc_title.startswith(squash(' '.join(title_lines + [t]))):
                            break
                        title_lines.append(t)
                    elif title_lines and not title_lines[-1].startswith('('):
                        break
                    j += 1
                status = title_lines[0] if title_lines and title_lines[0].startswith('(') else None
                title = ' '.join(title_lines[1:] if status else title_lines)
                annex = letter
                annex_numbers = []
                current = self.add(f'ANX_{letter}', doc, 'annex', None, number=letter,
                                   title=f'{self.p.words["annex"]} {letter} {status or ""} {title}'.replace('  ', ' ').strip(),
                                   pno=pno)
                by_number[letter] = current
                in_defs = False
                i = j
                continue
            notes = self.page_footnotes(lines, i) if re.match(r'^\s*_{5,}\s*$', line) else None
            if notes is not None:
                # a rule above the footnotes of the page: the paragraph goes on on the next page, the footnotes
                # are printed at the end of the clause
                footnotes.extend(notes[0])
                i = notes[1]
                continue
            if self.p.skip.match(line):
                flush()
                current = None
                i += 1
                continue
            if self.p.biblio.match(line):
                flush()
                current = self.add('BIBLIO', doc, 'bibliography', None, title=line.strip(), pno=pno)
                annex = None
                i += 1
                continue
            if annex is not None:
                m = ANNEX_CLAUSE.match(line) or ANNEX_NUMBER_ONLY.match(line) or \
                    self.toc_heading(ANNEX_CLAUSE_LOOSE, line) or self.aligned_heading(ANNEX_CLAUSE_LOOSE, lines, i)
                if m and m.group(1).startswith(annex + '.'):
                    num = m.group(1)
                    rel = num[len(annex) + 1:]
                    if plausible_next(annex_numbers, rel) and self.title_like(m, lines, i):
                        flush()
                        title, i = self.heading_title(m, lines, i, num)
                        parent = by_number.get(num.rsplit('.', 1)[0], by_number[annex])
                        current = self.add(f'ANX_{annex}.CL_{num}', parent, 'clause', None, number=num, title=title,
                                           pno=pno)
                        by_number[num] = current
                        annex_numbers.append(rel)
                        continue
            else:
                m = HEADING.match(line) or self.toc_heading(HEADING_LOOSE, line) or \
                    self.aligned_heading(HEADING_LOOSE, lines, i) or \
                    (NUMBER_ONLY.match(line) if in_defs or numbers else None) or \
                    (HEADING_TERM.match(line) if in_defs else None)
                if m and m.re is HEADING_TERM and not m.group(1).startswith(self.defs_clause + '.'):
                    m = None
                # siblings are either all titled or all untitled: after "6.4.1.1 Drafting information ..." the line
                # "6.4.1.2 Information shall be provided to the user ... taking into" is not a title either
                prev_sibling = m and re.sub(r'(\d+)$', lambda x: str(int(x.group(1)) - 1), m.group(1))
                if m and plausible_next(numbers, m.group(1)) and self.title_like(m, lines, i) and \
                        prev_sibling not in untitled and self.toc_agrees(m, lines, i):
                    flush()
                    num = m.group(1)
                    is_def = in_defs and num.startswith(self.defs_clause + '.')
                    title, i = self.heading_title(m, lines, i, None if is_def else num)
                    parent = by_number.get(num.rsplit('.', 1)[0], doc) if '.' in num else doc
                    if is_def:
                        current = self.add(f'DEF_{num}', parent, 'definition', None, number=num, title=title, pno=pno)
                        self.by_id[current].term[self.language] = title
                    else:
                        current = self.add(f'CL_{num}', parent, 'clause', None, number=num, title=title, pno=pno)
                    by_number[num] = current
                    numbers.append(num)
                    if self.definitions_clause:
                        if num == self.definitions_clause:
                            in_defs, self.defs_clause = True, num
                        elif in_defs and not num.startswith(self.defs_clause + '.'):
                            in_defs = False
                    elif '.' not in num:
                        in_defs = bool(self.p.terms.match(title))
                        if in_defs:
                            self.defs_clause = num
                    continue
                if m and m.re is HEADING and not in_defs and '.' in m.group(1) and plausible_next(numbers, m.group(1)) \
                        and m.group(1).rsplit('.', 1)[0] in by_number:
                    # a numbered clause without a title, its text starting on the number line ("6.4.1.1 Drafting
                    # information for use is an integral part ..."): a clause like any other, the number line is
                    # its first text line
                    flush()
                    num = m.group(1)
                    current = self.add(f'CL_{num}', by_number[num.rsplit('.', 1)[0]], 'clause', None, number=num,
                                       title='', pno=pno)
                    by_number[num] = current
                    numbers.append(num)
                    untitled.add(num)
                    buf.append((pno, line.replace(num, '', 1).lstrip()))
                    i += 1
                    continue
            m = self.p.caption.match(line)
            if m and current is not None and not self.p.toc_line.match(line):
                kind = 'figure' if m.group(1) == self.p.words['figure'] else 'table'
                key = (kind, m.group(2))
                # a caption that continues on the next page ends with "(1 di 2)", "(2 di 2)": the same table
                cap_title = re.sub(r'\s*\((?:\d+ (?:di|of) \d+|continued|segue|continua)\)\s*$', '', m.group(3) or '')
                dup = None
                if key in captions and cap_title and squash(cap_title) != captions_title.get(key):
                    # the same number printed under two different figures (CEI EN IEC 62061 Figure H.4): a second node
                    dup = 2
                    self.report.setdefault('duplicateCaptions', []).append(f'{m.group(1)} {m.group(2)}')
                if key not in captions or dup:
                    captions.add(key)
                    captions_title.setdefault(key, squash(cap_title))
                    title = f'{m.group(1)} {m.group(2)}' + (f' — {cap_title}' if cap_title else '')
                    # a title continued on the next line ("... hazards generated" / "by moving parts")
                    nxt = lines[i + 1][1].strip() if i + 1 < len(lines) else ''
                    if m.group(3) and re.match(r'[a-zà-ÿ]', nxt):
                        title += ' ' + nxt
                    nid = self.add(('FIG_' if kind == 'figure' else 'TAB_') + m.group(2) + (f'~{dup}' if dup else ''),
                                   current, kind, None, number=m.group(2), title=title, pno=pno)
                    if dup:
                        self.by_id[nid].attrs['duplicate'] = dup
            buf.append((pno, line))
            i += 1
        flush()
        self.check_toc(toc)
        split_designations(self.nodes, self.language)
        return self.nodes

    def read_front_annexes(self, front, doc):
        """European annexes (ZA, ZB) printed in the front matter before the body: read up to the table of contents."""
        k = 0
        while k < len(front):
            m = self.p.annex.match(front[k][1])
            nxt = self.next_text(front, k)
            if m and m.group(1).startswith('Z') and nxt and self.p.annex_status.match(nxt):
                letter, pno = m.group(1), front[k][0]
                j = k + 1
                body = []
                while j < len(front) and not self.p.front_annex_end.match(front[j][1]):
                    body.append(front[j][1])
                    j += 1
                stripped = [l.strip() for l in body]
                first = next((x for x, l in enumerate(stripped) if l), 0)
                status = stripped[first] if stripped else ''
                title_lines, started = [], False
                for l in stripped[first + 1:]:
                    if not l:
                        if started:
                            break
                        continue
                    started = True
                    title_lines.append(l)
                title = ' '.join(title_lines)
                text = clean_text('\n'.join(body))
                nid = self.add(f'ANX_{letter}', doc, 'annex', None, number=letter,
                               title=f'{self.p.words["annex"]} {letter} {status} {title}'.strip(), pno=pno)
                self.by_id[nid].text[self.language] = text
                k = j
            else:
                k += 1

    def read_front_sections(self, front, doc):
        """Foreword(s) and Introduction printed before the body. The Introduction is substantive (it can hold
        figures, e.g. the block diagram of IEC 60204-1 Figure 1); forewords give edition and legal context."""
        k = 0
        while k < len(front):
            m = self.p.front_section.match(front[k][1])
            if not m:
                k += 1
                continue
            name, pno = m.group(1).strip(), front[k][0]
            j = k + 1
            body = []
            while j < len(front) and not self.p.front_end.match(front[j][1]):
                body.append(front[j])
                j += 1
            body = drop_title_tail(body, self.title)
            path, kind = self.p.front_key(name)
            nid = self.add(path, doc, kind, None, title=name.capitalize(), pno=pno)
            self.by_id[nid].text[self.language] = clean_text('\n'.join(l for _, l in body))
            for bp, line in body:
                c = self.p.caption.match(line)
                if c:
                    kind = 'figure' if c.group(1) == self.p.words['figure'] else 'table'
                    title = f'{c.group(1)} {c.group(2)}' + (f' — {c.group(3)}' if c.group(3) else '')
                    self.add(('FIG_' if kind == 'figure' else 'TAB_') + c.group(2), nid, kind, None,
                             number=c.group(2), title=title, pno=bp)
                    self.front_captions.add((kind, c.group(2)))
            k = j

    def find_body_start(self, lines):
        """Index of the '1 Scope' heading of the body (not the one in the table of contents)."""
        for k, (_, line) in enumerate(lines):
            m = HEADING.match(line)
            if m and m.group(1) == '1' and self.p.scope.match(m.group(2)) and not self.p.toc_line.match(line):
                return k
        raise ValueError(f'{self.normId}: body start "1 {self.p.words["scope"]}" not found')

    def title_like(self, m, lines, i):
        title = m.group(2) if m.lastindex and m.lastindex >= 2 else self.next_text(lines, i)
        if not title:
            return False
        title = title.strip()
        if len(title) > 160 or title.endswith(('.', ';', ',')) and len(title) > 60:
            return False
        return bool(re.match(r'[A-Za-zÀ-ÿ(]', title))

    @staticmethod
    def page_footnotes(lines, i):
        """([footnote, ...], index after them) when the rule at lines[i] separates the footnotes of a page: only
        footnote lines ("3   Under preparation. ...", a marker then the text; indented lines go on the one before)
        follow it on that page. None for a rule that ends the text of the document."""
        pno = lines[i][0]
        notes, j = [], i + 1
        while j < len(lines) and lines[j][0] == pno:
            text = lines[j][1]
            if text.strip():
                # marks: 3, a, *, and the national editor's notes "( 1)" "( * )" of CEI editions
                m = re.match(r'^\s{0,3}(\(\s*(?:\d{1,2}|\*)\s*\)|\d{1,2}|[a-z]|\*{1,3})\s+(\S.*)$', text)
                if m:
                    notes.append(f'{re.sub(r"\s+", "", m.group(1))} {m.group(2).strip()}')
                elif notes and text.startswith(' '):
                    notes[-1] += ' ' + text.strip()
                else:
                    return None
            j += 1
        return (notes, j) if notes and j < len(lines) else None

    def toc_heading(self, pattern, line):
        """An indented numbered line ("     B.1      Overview" on a page whose table starts further left) is a
        heading when the table of contents lists that number with that title."""
        m = pattern.match(line)
        if not m:
            return None
        toc = squash(getattr(self, 'toc_titles', {}).get(m.group(1), ''))
        title = squash(m.group(2))
        return m if toc and title and toc[:min(len(toc), len(title), 12)] == title[:min(len(toc), len(title), 12)] else None

    @staticmethod
    def aligned_heading(pattern, lines, i):
        """An indented numbered line aligned with the text that follows it (the page has a wider margin than its
        table, IEC 62443-3-3 Annex B: "     B.1      Overview" then "     This annex ...") is a heading; the
        number order and the title shape are checked by the caller."""
        m = pattern.match(lines[i][1])
        if not m:
            return None
        indent = len(lines[i][1]) - len(lines[i][1].lstrip(' '))
        nxt = next((l for _, l in lines[i + 1:i + 4] if l.strip()), None)
        if nxt is None or re.match(r'^\s*\d', nxt):
            return None
        return m if len(nxt) - len(nxt.lstrip(' ')) == indent else None

    def toc_agrees(self, m, lines, i):
        """A numbered line is the heading the table of contents lists under that number only if its title begins
        as that entry does: "5 Optimizing ... improvement in these areas." (a row of a table) is not clause 5
        "Practice 1 - Security management". Numbers the contents does not list are not judged here."""
        toc = squash(getattr(self, 'toc_titles', {}).get(m.group(1), ''))
        title = squash((m.group(2) if m.lastindex and m.lastindex >= 2 else self.next_text(lines, i)) or '')
        if not toc or not title:
            return True
        k = min(len(toc), len(title), 12)
        return toc[:k] == title[:k]

    def next_text(self, lines, i):
        for j in range(i + 1, min(i + 4, len(lines))):
            if lines[j][1].strip():
                return lines[j][1].strip()
        return None

    def heading_title(self, m, lines, i, num=None):
        """Title of a heading and the index of the first line after it. A title printed on two lines is completed
        with the lines that, together with it, still match the title of the table of contents."""
        if m.lastindex and m.lastindex >= 2:
            title, nxt = re.sub(r'\s+', ' ', m.group(2)).strip(), i + 1
        else:
            title, nxt = '', i + 1
            for j in range(i + 1, min(i + 4, len(lines))):
                if lines[j][1].strip():
                    title, nxt = re.sub(r'\s+', ' ', lines[j][1]).strip(), j + 1
                    break
        toc = squash(getattr(self, 'toc_titles', {}).get(num, '')) if num else ''
        while toc and len(squash(title)) < len(toc) and nxt < len(lines):
            line = lines[nxt][1].strip()
            if not line:
                break
            longer = f'{title} {line}'
            if not toc.startswith(squash(longer)):
                break
            title, nxt = longer, nxt + 1
        if num and not toc:
            # no title in the table of contents: a title ending without punctuation goes on with a following
            # lower-case line that is followed by a blank line ("... cleaning or" / "maintenance")
            while nxt + 1 < len(lines) and not re.search(r'[.;:]\s*$', title):
                line = lines[nxt][1].strip()
                if not line or not line[0].islower() or len(line) > 100 or re.search(r'[.;:]\s*$', line) or \
                        lines[nxt + 1][1].strip():
                    break
                title, nxt = f'{title} {line}', nxt + 1
        return title, nxt

    # ---------- nodes ----------
    def add(self, path, parent, kind, elem, number=None, title='', pno=None):
        if not hasattr(self, 'by_id'):
            self.by_id = {}
        nid = node_id(self.normId, path)
        k = 2
        base = nid
        while nid in self.by_id:
            nid = f'{base}~{k}'
            k += 1
        n = Node(nodeId=nid, normId=self.normId, parentId=parent, kind=kind, seq=len(self.nodes) + 1, number=number)
        n.title[self.language] = title
        n.text[self.language] = ''
        n.source = {'file': self.pdf.rsplit('/', 1)[-1], 'page': str(pno or '')}
        self.nodes.append(n)
        self.by_id[nid] = n
        return nid

    def check_toc(self, toc):
        found = {n.number for n in self.nodes if n.number}
        found |= {f'ANNEX {n.number}' for n in self.nodes if n.kind == 'annex'}
        missing = [num for num, _ in toc if num not in found]
        self.report['tocMissing'] = missing
        dup = [n.nodeId for n in self.nodes if '~' in n.nodeId]
        self.report['duplicates'] = dup


# a designator of a standard, with the partition cited inside it ("ISO 14118:2000, Clause 5", "IEC 61508-3:2010,
# Allegato F", "ISO 12100:2010, 3.1"), so that the partition is not taken for one of the citing norm
STD_DESIGNATOR = r'\b(?:EN\s+)?(?:ISO/IEC|ISO/TR|ISO/TS|IEC/TS|IEC/TR|ISO|IEC|EN)\s+\d{3,5}(?:-\d+)*(?::\d{4})?'


def std_patterns(lang):
    w = words_of(lang)
    part = r'(?:(?:' + w['clause'] + '|' + w['annex'] + '|' + w['table'] + '|' + w['figure'] + \
        r')\s+(?:\d{1,2}|[A-Z]{1,2})(?:\.\d{1,2})*|\d{1,2}(?:\.\d{1,2})*)\b'
    return {
        'ext': re.compile(STD_DESIGNATOR + r'(?:,\s*(' + part + r'))?'),
        # the prefix word and the number are separated by spaces, or by nothing after a parenthesis: "(5.2.5)"
        'internal': re.compile(r'(?:' + w['refBefore'] + r')\s*((?:\d{1,2}(?:\.\d{1,2}){1,5})|[A-Z]\.\d{1,2}(?:\.\d{1,2}){0,4})\b'),
        'clause': re.compile(r'\b' + w['clause'] + r'\s+(\d{1,2})\b'),
        'annex': re.compile(r'\b' + w['annex'] + r'\s+([A-Z]{1,2})\b'),
        # "Annex B of ISO 13849-2", "Allegato K della IEC 61508-2": a partition of another norm
        'ofOther': re.compile(r'\s+(?:' + w['of'] + r')\s*' + STD_DESIGNATOR),
    }


def std_references(nodes, known_patterns, lang='en'):
    """References inside a standard (subclauses, Clause N, Annex X) and to other standards."""
    # figures and tables share the numbering of annex clauses ("Figura H.1", "H.1 Generalità"): a bare number cites
    # a partition of the text
    by_number = {}
    for n in nodes:
        if n.number and '~' not in n.nodeId and n.kind in ('clause', 'definition', 'annex'):
            by_number.setdefault(n.number, n.nodeId)
    pat = std_patterns(lang)
    ext = pat['ext']
    for n in nodes:
        text = n.text.get(lang) or ''
        refs, seen = [], set()

        def add(raw, target, norm=None, external=None):
            key = (raw, target, external)
            if key in seen or target == n.nodeId:
                return
            seen.add(key)
            refs.append(Reference(raw=raw, targetNormId=norm or (n.normId if target else None), targetNodeId=target,
                                  external=external))

        spans = []
        for m in ext.finditer(text):
            raw = m.group(0)
            known = known_norm(raw, known_patterns)
            spans.append(m.span())
            if known == n.normId:
                continue
            add(raw, None, known, None if known else re.sub(r'\s+', ' ', raw))
        def inside(pos):
            return any(a <= pos < b for a, b in spans)
        def of_other(m):
            return bool(pat['ofOther'].match(text, m.end()))
        for m in pat['internal'].finditer(text):
            if inside(m.start(1)) or of_other(m):
                continue
            # "(H.3)" alone in parentheses numbers an equation of annex H
            if m.group(1)[0].isalpha() and text[m.start():m.start(1)].strip() == '(':
                continue
            num = m.group(1)
            if num in by_number:
                add(num, by_number[num])
        for m in pat['clause'].finditer(text):
            if not inside(m.start()) and not of_other(m) and m.group(1) in by_number:
                add(m.group(0), by_number[m.group(1)])
        for m in pat['annex'].finditer(text):
            if not inside(m.start()) and not of_other(m) and m.group(1) in by_number:
                add(m.group(0), by_number[m.group(1)])
        n.references = refs
    return nodes
