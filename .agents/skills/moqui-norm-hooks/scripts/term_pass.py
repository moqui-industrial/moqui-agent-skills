#!/usr/bin/env python3
"""Rule-based term pass: from the TERM findings of check_hooks.py, a part file that links each named concept at the
item that names it, the role by the kind of item (definitions, notes, examples, list points, table rows and figure
boxes list it: l; requirement text specifies it: s). Allowed only with a random sample read against the text
(moqui-norm-hooks): the sample is printed, read it before adding the part.

    python3 term_pass.py IEC-62443-4-2-2019 P42 --part 4 --out part.json [--lang en] [--exclude a,b] [--sample 25]
"""
import argparse
import json
import random
import re
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent.parent / 'moqui-norm-loading' / 'scripts'))
from normkb import paths  # noqa: E402

ITEMS = paths.ITEMS


def role(sid, item):
    # forewords, endorsement notices and introductions name a notion, they do not set a requirement on it
    if re.match(r'^(FOREWORD|EUFOREWORD|ENDORSEMENT|INTRO|PRE|REC)', sid):
        return 'l'
    if item['type'] in ('AitNote', 'AitExample', 'AitPoint', 'AitSubPoint', 'AitTable', 'AitFigure') or \
            re.search(r'\.(r\d+|li\d+|n\d+|x\d+)$', sid) or re.match(r'^3\.\d+\.\d+', sid) or sid.startswith('FIG'):
        return 'l'
    return 's'


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('normId')
    ap.add_argument('alias')
    ap.add_argument('--part', required=True)
    ap.add_argument('--out', required=True)
    ap.add_argument('--lang', default='en')
    ap.add_argument('--exclude', default='')
    ap.add_argument('--sample', type=int, default=25)
    ap.add_argument('--seed', type=int, default=1)
    a = ap.parse_args()
    roots = subprocess.run([sys.executable, 'dump_part.py', a.normId, a.alias, '--roots'], cwd=HERE,
                           capture_output=True, text=True, check=True).stdout.split()
    out = subprocess.run([sys.executable, 'check_hooks.py', a.normId, *roots, '--alias', a.alias, '--lang', a.lang],
                         cwd=HERE, capture_output=True, text=True, check=True).stdout
    items = {}
    for line in (ITEMS / f'{a.normId}.jsonl').read_text(encoding='utf-8').splitlines():
        d = json.loads(line)
        items[d['seqId']] = d
    exclude = set(filter(None, a.exclude.split(',')))
    links, found = [], []
    for line in out.splitlines():
        f = line.split('\t')
        if len(f) < 3 or not f[1].startswith('TERM:'):
            continue
        key = f[1].split(':', 1)[1]
        if key in exclude:
            continue
        r = role(f[0], items[f[0]])
        links.append([key, f'{a.alias}@{f[0]}', r])
        found.append((f[0], key, f[2], r))
    part = {'part': a.part, 'about': f'Rule-based term pass on {a.normId} ({a.lang}): every concept named at the item that '
            f'names it, role by item kind; sample of {min(a.sample, len(found))} read against the text', 'addClauses': links}
    Path(a.out).write_text(json.dumps(part, ensure_ascii=False, indent=1), encoding='utf-8')
    by_role = {}
    for _, _, _, r in found:
        by_role[r] = by_role.get(r, 0) + 1
    print(f'{len(links)} links {by_role}; excluded {sorted(exclude)}')
    random.seed(a.seed)
    for sid, key, name, r in random.sample(found, min(a.sample, len(found))):
        text = re.sub(r'\s+', ' ', items[sid]['text'].get(a.lang) or items[sid]['title'].get(a.lang) or '')
        i = text.lower().find(name.lower())
        print(f'{sid} {key} [{r}] ...{text[max(0, i - 70):i + 70]}...')


if __name__ == '__main__':
    main()
