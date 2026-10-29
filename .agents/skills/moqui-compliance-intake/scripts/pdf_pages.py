#!/usr/bin/env python3
"""Read a large PDF (drawings, datasheets, certificates) piece by piece, so that only what matters enters the conversation.

    python3 -I pdf_pages.py info  FILE                         # pages, title, producer
    python3 -I pdf_pages.py grep  FILE 'profinet|ethernet|STO'  # matching lines with their page and sheet label
    python3 -I pdf_pages.py text  FILE 6 7                      # the text of pages 6 to 7 (layout kept)
    python3 -I pdf_pages.py image FILE 126 [--dpi 80]           # page 126 as PNG in the workspace, to look at

FILE is a path, or a name relative to INBOX_DIR / CONTENT_DIR (the analysis sandbox mounts the compliance inbox and the
content store there, read only). Images are written to WORKSPACE_DIR (default the current directory). Needs poppler
(pdfinfo, pdftotext, pdftoppm). Electrical drawings: cross references like /122.7 are sheet numbers; grep prints the
sheet label of a page ("Page 122") next to the PDF page number when the title block makes it readable.
"""
import os
import re
import subprocess
import sys


def resolve(name):
    if os.path.isfile(name):
        return name
    clean = os.path.basename(name)
    matches = []
    for env in ('INBOX_DIR', 'UPLOADS_DIR', 'CONTENT_DIR'):
        base = os.environ.get(env)
        if not base or not os.path.isdir(base):
            continue
        direct = os.path.join(base, name.lstrip('/'))
        if os.path.isfile(direct):
            return direct
        for root, dirs, files in os.walk(base):
            dirs[:] = [d for d in dirs if d != 'temp']
            for fn in files:
                if fn == clean or fn.endswith('__' + clean):
                    p = os.path.join(root, fn)
                    matches.append((os.path.getmtime(p), p))
    if matches:
        return max(matches)[1]
    sys.exit(f'{name}: not found (give a path, or a name inside INBOX_DIR, UPLOADS_DIR or CONTENT_DIR)')


def run(*cmd):
    return subprocess.run(cmd, capture_output=True, text=True, check=False).stdout


def pages_text(path, first=None, last=None):
    args = ['pdftotext', '-layout'] + (['-f', str(first)] if first else []) + (['-l', str(last)] if last else []) + [path, '-']
    return run(*args).split('\f')


def main():
    if len(sys.argv) < 3 or sys.argv[1] not in ('info', 'grep', 'text', 'image'):
        sys.exit(__doc__)
    cmd, path = sys.argv[1], resolve(sys.argv[2])
    if cmd == 'info':
        print(run('pdfinfo', path))
    elif cmd == 'grep':
        pat = re.compile(sys.argv[3], re.I)
        for i, page in enumerate(pages_text(path), 1):
            sheet = re.search(r'(?:Page|Pagina|Blatt|Sheet)\s+(\S+)\s*$', page.strip().splitlines()[-1] if page.strip() else '')
            for line in page.splitlines():
                if pat.search(line):
                    print(f'p{i}{" sheet " + sheet.group(1) if sheet else ""}: {" ".join(line.split())[:200]}')
    elif cmd == 'text':
        first, last = int(sys.argv[3]), int(sys.argv[4] if len(sys.argv) > 4 else sys.argv[3])
        for i, page in enumerate(pages_text(path, first, last), first):
            if page.strip():
                print(f'===== page {i} =====\n{page.rstrip()}')
    else:
        page = int(sys.argv[3])
        dpi = sys.argv[sys.argv.index('--dpi') + 1] if '--dpi' in sys.argv else '80'
        stem = re.sub(r'^[0-9a-fA-F-]{36}__', '', os.path.splitext(os.path.basename(path))[0])
        out = os.path.join(os.environ.get('WORKSPACE_DIR', '.'), f'{stem}-p{page}')
        run('pdftoppm', '-r', dpi, '-png', '-f', str(page), '-l', str(page), '-singlefile', path, out)
        print(out + '.png')


if __name__ == '__main__':
    main()
