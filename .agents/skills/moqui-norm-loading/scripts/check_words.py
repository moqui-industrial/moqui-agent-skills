#!/usr/bin/env python3
"""Content check of a PDF standard after build_agreement.py: the words of the pages kept (boilerplate lines left
out) against the words of the items (titles, terms and texts). The partition check only covers the text inside the
clauses the reader found; this check finds text the reader never put in a clause.

    python3 check_words.py IEC-62061-2021 [--pages 12] [--lines]

Prints the words lost and added, and the pages that lose words found on at most three pages (where the loss is):
explain every such page (cover, contents, an index in another language are expected; a section of the norm is a
reader error). Generated words (Columns, Drawing labels, Block ...) show as added.

Counting words hides a loss when the same words occur elsewhere (a paragraph cut at a page break, a header line kept as
text). --lines also lists, page by page, the lines of the PDF of which no sequence of three words is in an item (numbers and
list markers at the start left out, lines of fewer than four words and contents pages left out).
"""
import argparse
import json
import os
import re
import sys
from collections import Counter

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

from normkb import paths                         # noqa: E402
from normkb.items import read_items_jsonl   # noqa: E402
from normkb.pdfstd import PdfStandardReader, publisher_page  # noqa: E402

WORD = re.compile(r'[A-Za-zÀ-ÿ]{3,}')


def words(text):
    return [w.lower() for w in WORD.findall(text or '')]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('normId')
    ap.add_argument('--pages', type=int, default=15, help='how many pages to list')
    ap.add_argument('--lines', action='store_true', help='also the lines of the PDF in no item, page by page')
    a = ap.parse_args()
    cfg = json.load(open(paths.CONFIG, encoding='utf-8'))
    norm = next(n for n in cfg['norms'] if n['normId'] == a.normId)
    lang = norm['language']
    reader = PdfStandardReader(norm['normId'], os.path.join(cfg['sourceRoot'], norm['file']), language=lang,
                               boilerplate=norm.get('boilerplate', []), title=norm['title'],
                               bilingual=norm.get('bilingual', True), paragraph_gaps=norm.get('paragraphGaps', False),
                                   line_fixes=norm.get('lineFixes', []))
    pages = reader.pages()
    langs = reader.page_languages(pages)
    items = read_items_jsonl(paths.ITEMS / f'{a.normId}.jsonl')
    have = Counter(w for it in items for t in (it.text.get(lang), it.title.get(lang), it.term.get(lang)) for w in words(t))
    src, where = Counter(), {}
    for pno, (page, pl) in enumerate(zip(pages, langs), 1):
        if pl not in (lang, None, 'mix') or publisher_page(page):
            continue
        for line in page.split('\n'):
            if any(b.match(line.rstrip()) for b in reader.boiler):
                continue
            for w in words(line):
                src[w] += 1
                where.setdefault(w, set()).add(pno)
    lost, added = src - have, have - src
    print(f'source words {sum(src.values())}, item words {sum(have.values())}, '
          f'lost {sum(lost.values())}, added {sum(added.values())}')
    by_page = Counter()
    for w, c in lost.items():
        if len(where[w]) <= 3:
            for p in where[w]:
                by_page[p] += c
    print('pages losing words:', by_page.most_common(a.pages))
    print('most lost words:', lost.most_common(20))
    print('most added words:', added.most_common(10))
    if a.lines:
        # a line is found when one sequence of three of its words is in an item: a table line crossing several
        # cells is found by the words of one cell, a lost line of text by none
        toks = lambda t: re.findall(r'[0-9a-zà-ÿ]+', t.lower())
        shingles = set()
        for it in items:
            for t in (it.text.get(lang), it.title.get(lang)):
                w = toks(t or '')
                shingles.update(' '.join(w[i:i + 3]) for i in range(len(w) - 2))
        marker = re.compile(r'^\s*(?:[A-Z]?\.?\d+(?:\.\d+)*|[a-z]\)|\d{1,2}\)|\(\d{1,2}\)|[–—•⎯-])\s+')
        missing = Counter()
        examples = {}
        for pno, (page, pl) in enumerate(zip(pages, langs), 1):
            if pl not in (lang, None, 'mix') or page.count('....') > 5 or publisher_page(page):
                continue
            for line in page.split('\n'):
                if any(b.match(line.rstrip()) for b in reader.boiler):
                    continue
                w = toks(marker.sub('', line))
                if len(w) >= 4 and not any(' '.join(w[i:i + 3]) in shingles for i in range(len(w) - 2)):
                    missing[pno] += 1
                    examples.setdefault(pno, []).append(line.strip()[:100])
        print(f'missing lines {sum(missing.values())}')
        for pno, n in sorted(missing.items()):
            print(f'  page {pno}: {n}', examples[pno][:3])
    return 0


if __name__ == '__main__':
    sys.exit(main())
