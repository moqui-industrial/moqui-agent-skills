"""Tables of a standard read from the PDF with their rows and columns (PyMuPDF find_tables).

pdftotext -layout reads a multi-column table line by line and mixes its columns ("approach of a moving element
crushing; 6.2.3 a)"); the table is read again from the page geometry, so that every row keeps its cells.

Which table a ruled table on a page belongs to: the caption line nearest above it on the same page ("Table B.4"), or,
when there is none above it, the table that continues from the previous page ("Table B.3 (continued)", or its header
row repeated at the top of the next page). Only pages
where the caption is a line of its own count, so an index that mentions "Table B.1" is not a page of Table B.1.
"""
import re


def words(text):
    return set(re.findall(r'[A-Za-zÀ-ÿ]{3,}', (text or '').lower()))


def caption_lines(page, caption_word):
    """[(y, number)] of the caption lines of a page: 'Table B.1', 'Table B.1 (continued)', 'Table 3 — Title'."""
    out = []
    pat = re.compile(r'^\s*' + caption_word + r'\s+((?:[A-Z]{1,2}\.)?\d{1,2})\s*(\((continued|segue|\d+ (?:di|of) \d+)\)|[—–-]{1,2}\s*\S.*)?\s*$')
    for b in page.get_text('dict')['blocks']:
        for line in b.get('lines', []):
            text = ''.join(s['text'] for s in line['spans'])
            m = pat.match(text)
            if m:
                out.append((line['bbox'][1], m.group(1)))
    return sorted(out)


def read_tables(pdf, numbers, caption_word='Table', pages_kept=None):
    """{number: {'header': [..], 'rows': [[..], ..], 'pages': [..], 'words': set}} for the table numbers given, read
    on the pages of the edition's language only (pages_kept, from the text reader)."""
    import pymupdf
    from .pdfstd import SYMBOL, dingbats, page_private_fonts, single_line_brackets   # the alphabet of the clauses
    doc = pymupdf.open(pdf)
    wanted = set(numbers)
    parts = {}           # number -> list of extracted row lists, in page order
    pages = {}
    current = None       # table continuing from the previous page
    last = None          # (number, header row) of the last table read on the previous page
    for p in range(len(doc)):
        if pages_kept is not None and p + 1 not in pages_kept:
            continue      # a page of the other language of a bilingual edition
        page = doc[p]
        caps = caption_lines(page, caption_word)
        if not caps and current is None and last is None:
            continue
        tabs = page.find_tables().tables if (caps or current or last) else []
        read_here = None
        wing = dingbats(page_private_fonts(page)) if tabs else {}
        for tb in sorted(tabs, key=lambda t: t.bbox[1]):
            above = [num for y, num in caps if y <= tb.bbox[1] + 2]
            raw = tb.extract()
            # the header without the superscript note letters of its labels ("Origin" with a): the first row, and
            # the second when it is a second header row (empty first cell)
            for i, row in enumerate(tb.rows[:2]):
                if i == 1 and (raw[1][0] or '').strip():
                    break
                for j, bbox in enumerate(row.cells):
                    if bbox and raw[i][j]:
                        raw[i][j] = drop_note_letters(page, bbox, raw[i][j])
            data = [[single_line_brackets(re.sub(r'\s*\n\s*', ' ', c or '').translate(wing)).translate(SYMBOL).strip()
                     for c in r] for r in raw]
            num = above[-1] if above else current
            if num is None and last and data and any(last[1]) and data[0] == last[1]:
                # no "(continued)" caption, but the header row repeated at the top of the page (IEC 62443-4-1
                # Table B.1)
                num = last[0]
            if num not in wanted:
                continue
            parts.setdefault(num, []).append(data)
            pages.setdefault(num, []).append(p + 1)
            read_here = (num, parts[num][0][0])
        last = read_here
        if caps:
            current = caps[-1][1] if caps[-1][1] in wanted else None
        # a table goes on only on the next page when that page says so
        nxt = doc[p + 1].get_text() if p + 1 < len(doc) else ''
        if current and not re.search(caption_word + r'\s+' + re.escape(current) + r'\s*\((continued|segue|\d+ (?:di|of) \d+)\)', nxt):
            current = None
    out = {}
    for num, chunks in parts.items():
        header, rows = None, []
        for data in chunks:
            body_start = next((i for i, r in enumerate(data) if r and re.match(r'^\d+$', r[0] or '')), None)
            if body_start is None:
                # no numbered first column: the first row is the header (repeated on continuation pages)
                body_start = 1
                # a second header row: empty first cell, short labels under a cell that spans them ("HFT" / 0 1 2)
                while (body_start < len(data) - 1 and not (data[body_start][0] or '').strip()
                       and any(data[body_start][1:]) and all(len(c or '') <= 12 for c in data[body_start])):
                    body_start += 1
            data = align_columns(data, body_start)
            top = [list(r) for r in data[:body_start]]
            for r, below in zip(top, top[1:]):
                # a header cell spanning the columns below it is carried over them
                for k in range(1, len(r)):
                    if not r[k] and below[k] and r[k - 1]:
                        r[k] = r[k - 1]
            head = [' '.join(x for x in col if x) for col in zip(*top)]
            if header is None:
                header = head
            rows.extend(r for r in data[body_start:] if any(r))
        out[num] = {'header': header, 'rows': rows, 'pages': sorted(set(pages[num])),
                    'words': words(' '.join(header + [c for r in rows for c in r]))}
    return out


def drop_note_letters(page, bbox, text):
    """A header label without the note letters set as superscripts after its words ("Origina" is "Origin" with
    note a): a single lower-case letter, maybe in brackets, smaller than the label and raised above its baseline.
    Exponents and units ("10-5", "mm2") are digits and stay, subscripts ("I a") are lower and stay."""
    spans = [sp for b in page.get_text('dict', clip=bbox)['blocks'] for ln in b.get('lines', []) for sp in ln['spans']
             if sp['text'].strip()]
    if not spans:
        return text
    size = max(sp['size'] for sp in spans)
    for prev, sp in zip(spans, spans[1:]):
        mark = sp['text'].strip()
        # raised above the baseline of its word: a superscript, not a subscript ("I a" is the current Ia)
        if sp['size'] < 0.85 * size and re.fullmatch(r'\(?[a-z]\)?', mark) and \
                sp['origin'][1] < prev['origin'][1] - 1:
            word = (prev['text'].split() or [''])[-1]
            if word:
                text = re.sub(re.escape(word) + r'\s*' + re.escape(mark) + r'(?![a-z])', word, text, count=1)
    return text


def align_columns(data, body_start):
    """A grid finer than the table: a header label over a column without values goes to the next column that has
    values and no label (IEC 62443-3-3 Table B.1: "SL 1" one column right of its check marks), and columns empty in
    the header and in every row are dropped. Only for a header of one row."""
    if not data or body_start != 1:
        return data          # a header on two rows assembles its labels from both: left as it is
    rows = [list(r) for r in data]
    width = max(len(r) for r in rows)
    for r in rows:
        r.extend([''] * (width - len(r)))
    head, body = rows[:body_start], rows[body_start:]
    has_val = [any(r[j] for r in body) for j in range(width)]
    for h in head:
        for j in range(width):
            if h[j] and not has_val[j]:
                for k in (j - 1, j + 1):
                    if 0 <= k < width and has_val[k] and not any(x[k] for x in head):
                        h[k], h[j] = h[j], ''
                        break
    keep = [j for j in range(width) if has_val[j] or any(h[j] for h in head)]
    return [[r[j] for j in keep] for r in rows]


def row_text(header, row):
    """One row as 'Header: value; ...' with the empty cells left out (superscript note letters of the header are left
    out when the header is read, by their size). A row with only its first cell (a table footnote) is returned as
    it is."""
    filled = [v for v in row if v]
    if len(filled) == 1 and row[0] and not re.match(r'^\d+$', row[0]):
        return row[0]
    parts = []
    for h, v in zip(header, row):
        h = (h or '').strip()
        if v:
            parts.append(f'{h}: {v}' if h else v)
    return '; '.join(parts)



def read_index(pdf, pages, columns, gap=13):
    """Entries of an index printed in columns without rules (ISO 12100 Annex C: English, French, German, clauses),
    read from the word positions: a column starts at the most frequent left edge between its heading and the
    heading before it; lines closer than `gap` points belong to the same entry. Returns (entries, notes, dropped):
    entries are lists of cells, notes are the sentences printed under the index, dropped the words left out (column
    headings, letter headings, page headers and footers) for the content check."""
    import pymupdf
    from collections import Counter
    doc = pymupdf.open(pdf)
    entries, notes, dropped = [], [], []
    for p in range(pages[0] - 1, pages[1]):
        ws = doc[p].get_text('words')
        heads = []
        for c in columns:
            first = c.split()[0]
            h = next((w for w in ws if w[4] == first), None)
            if h is None:
                break
            heads.append(h)
        if len(heads) < len(columns):
            continue
        starts = []
        for k, h in enumerate(heads):
            lo = heads[k - 1][2] if k else 0
            xs = Counter(round(w[0]) for w in ws if lo < w[0] <= h[0] + 1 and w[1] > h[3])
            starts.append(xs.most_common(1)[0][0] - 2)
        top = max(w[3] for w in ws if abs(w[1] - heads[0][1]) < 15 and w[0] >= heads[-1][0] - 2 or w in heads)
        lines = {}
        for w in sorted(ws, key=lambda w: (w[1], w[0])):
            if w[1] <= top + 1:
                dropped.append(w[4])
                continue
            y = next((y for y in lines if abs(y - w[1]) < 3), w[1])
            lines.setdefault(y, []).append(w)
        rows = []
        for y in sorted(lines):
            # words of a line in reading order (underlined or bold words sit on a slightly different baseline)
            lines[y].sort(key=lambda w: w[0])
            text = ' '.join(w[4] for w in lines[y])
            if '©' in text or re.match(r'^\d+$', text):
                dropped.extend(w[4] for w in lines[y])
                continue
            rows.append((y, lines[y]))
        group, last = [], None
        for y, line in rows + [(None, None)]:
            if line is not None and (last is None or y - last < gap):
                group.append(line)
                last = y
                continue
            if group:
                text = ' '.join(w[4] for ln in group for w in ln)
                if re.match(r'^[A-Z]$', text):
                    dropped.append(text)
                elif re.match(r'^[A-Z][a-z].*\.$', text):
                    notes.extend(' '.join(w[4] for w in ln) for ln in group)
                else:
                    cells = [[] for _ in columns]
                    for ln in group:
                        for w in ln:
                            k = max(i for i, s in enumerate(starts) if w[0] >= s or i == 0)
                            cells[k].append(w[4])
                    entries.append([' '.join(c) for c in cells])
            group, last = ([line], y) if line is not None else ([], None)
    return entries, notes, dropped
