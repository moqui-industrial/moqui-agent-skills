#!/usr/bin/env python3
"""The verification loop of the norms knowledge base: run it after every change (a reader rule, a configuration, a
transcription, a hook part) and before every commit or load. One command checks every norm, not only the one that
changed, because a reader change can move the items of the others.

    python3 verify_norms.py                      # every configured norm
    python3 verify_norms.py IEC-62061-2021       # one norm, plus the shared checks
    python3 verify_norms.py --db                 # also the read-only SQL checks of the running instance
    python3 verify_norms.py --write              # build into data/ instead of a scratch directory

Per norm: build (errors stop it), the new seeds against the seeds in data/ (items with every field, references;
every change must be explained), content check (Formex blocks or PDF words by page), check_data on the seeds.
Shared: unit tests, vocab.py --check and the vocabulary against data/60_, check_hooks of every norm in each language it is loaded in, hook suite; with --db the agreement and cross-reference
SQL checks. The exit code is 1 when any check fails. Uses the moqui-data and moqui-seed-reload skills next to this
one; data/ is the one of mantle-compliance (normkb/paths.py).
"""
import argparse
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from normkb import paths  # noqa: E402

COMPONENT = paths.COMPONENT
os.environ['MANTLE_COMPLIANCE'] = str(COMPONENT)   # the scripts run below find the same component
FRAMEWORK = paths.FRAMEWORK
NORMKB = paths.LOADING
EXTRACTION = paths.HOOKS
SKILL_DIRS = [str(paths.SKILLS)]


def skill_file(rel):
    for d in SKILL_DIRS:
        if d and (Path(d) / rel).exists():
            return Path(d) / rel
    return None


def run(cmd, cwd, timeout=1800):
    p = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True, timeout=timeout)
    return p.returncode, p.stdout + p.stderr


def seeds(data_dir, norm_id):
    """The seed data of a norm as the database will hold it: items keyed (agreement, item) with every field and the
    text, references (AgreementAssoc of the 40_ and 42_ files) as (agreement, item, target agreement, target item,
    text as written, type), and the other rows (Agreement, AgreementContent) with their fields. The seeds in data/
    are the source of truth: a new build is compared with them, not with an intermediate file."""
    import xml.etree.ElementTree as ET
    items, refs, other = {}, set(), set()
    for f in sorted(Path(data_dir).glob(f'40_Norm_{norm_id}_*.xml')) + \
            sorted(Path(data_dir).glob(f'42_NormCrossRefs_{norm_id}.xml')):
        for e in ET.parse(f).getroot():
            fields = dict(e.attrib, **{c.tag: c.text or '' for c in e})
            if e.tag.endswith('.AgreementItem'):
                items[(fields['agreementId'], fields['agreementItemSeqId'])] = fields
            elif e.tag.endswith('.AgreementAssoc'):
                refs.add(tuple(fields.get(k) for k in ('agreementId', 'agreementItemSeqId', 'toAgreementId',
                                                       'toAgreementItemSeqId', 'assocText', 'agreementAssocTypeEnumId')))
            else:
                other.add((e.tag, tuple(sorted(fields.items()))))
    return items, refs, other


def aliases_and_languages(cfg):
    """normId -> (alias, [languages]) from the vocabulary files and the norm configuration."""
    aliases = {}
    for f in [paths.VOCABULARY / 'VOCAB-BASE.json'] + sorted(paths.VOCABULARY.glob('HOOKS-*.json')):
        for a, n in json.loads(f.read_text(encoding='utf-8')).get('normAliases', {}).items():
            aliases[n] = a
    out = {}
    for n in cfg['norms']:
        langs = list(n['dirs']) if n['reader'] == 'formex' else [n['language']]
        if n['normId'] in aliases:
            out[n['normId']] = (aliases[n['normId']], langs)
    return out


def main():
    ap = argparse.ArgumentParser(description=__doc__.split('\n')[0])
    ap.add_argument('norms', nargs='*')
    ap.add_argument('--db', action='store_true', help='run the read-only SQL checks of the running instance')
    ap.add_argument('--write', action='store_true', help='build into data/ instead of a scratch directory')
    a = ap.parse_args()
    cfg = json.loads(paths.CONFIG.read_text(encoding='utf-8'))
    norms = [n for n in cfg['norms'] if not a.norms or n['normId'] in a.norms]
    if a.norms and len(norms) != len(a.norms):
        sys.exit(f'unknown norm in {a.norms}')
    rows, failed = [], False
    check_data = skill_file('moqui-data/scripts/check_data.py')
    scratch = Path(tempfile.mkdtemp(prefix='verify-norms-'))
    data_dir = COMPONENT / 'data' if a.write else scratch
    if not a.write and (COMPONENT / 'data' / '41_NormStubs.xml').exists():
        shutil.copy(COMPONENT / 'data' / '41_NormStubs.xml', scratch)   # stubs are merged across norms
    for n in norms:
        nid = n['normId']
        row = {'norm': nid}
        before, refs_before, other_before = seeds(COMPONENT / 'data', nid)   # read before a --write build
        code, out = run([sys.executable, 'build_agreement.py', nid, '--data-dir', str(data_dir)], NORMKB)
        if code:
            row['build'] = 'FAIL'
            print(f'== {nid}: build failed\n' + '\n'.join(out.splitlines()[-25:]))
            rows.append(row)
            failed = True
            continue
        report = json.loads(out[out.index('{'):])
        row['build'] = f"{report['items']} items"
        after, refs_after, other_after = seeds(data_dir, nid)
        removed, added = set(before) - set(after), set(after) - set(before)
        changed = {k: sorted(f for f in set(before[k]) | set(after[k]) if before[k].get(f) != after[k].get(f))
                   for k in set(before) & set(after) if before[k] != after[k]}
        row['diff'] = 'same' if before and not (removed or added or changed or other_before != other_after) else (
            'first build' if not before else f'-{len(removed)} +{len(added)} ~{len(changed)}')
        if before and (removed or added or changed or other_before != other_after):
            print(f'== {nid}: seed items differ from data/ (explain every change)')
            for label, ids in (('removed', sorted(removed)), ('added', sorted(added))):
                if ids:
                    print(f'   {label}: {[i[1] for i in ids[:15]]}{" ..." if len(ids) > 15 else ""}')
            for k in sorted(changed)[:15]:
                print(f'   changed {k[0]} {k[1]}: {changed[k]}')
            for t, _ in sorted(other_before ^ other_after)[:5]:
                print(f'   changed {t}')
        if before and refs_before != refs_after:
            # a reference rule changed: every citation that moved must be explained like a changed text
            print(f'== {nid}: references differ from data/ (explain every change)')
            for sign, refs in (('-', refs_before - refs_after), ('+', refs_after - refs_before)):
                for r in sorted(refs, key=str)[:20]:
                    print(f'   {sign} {r}')
        row['refs'] = 'same' if before and refs_before == refs_after else (
            'first build' if not before else f'-{len(refs_before - refs_after)} +{len(refs_after - refs_before)}')
        if n['reader'] == 'formex':
            code, out = run([sys.executable, 'check_formex_items.py', nid], NORMKB)
            row['content'] = 'ok' if code == 0 else 'FAIL'
            failed |= code != 0
            if code:
                print(f'== {nid}: content check\n{out[-2000:]}')
        else:
            code, out = run([sys.executable, 'check_words.py', nid, '--pages', '8', '--lines'], NORMKB)
            m = re.search(r'lost (\d+)', out)
            pages = re.search(r'pages losing words: (.*)', out)
            lines = re.search(r'missing lines (\d+)', out)
            row['content'] = f"lost {m.group(1) if m else '?'} words, {lines.group(1) if lines else '?'} lines"
            print(f'== {nid}: pages losing words {pages.group(1) if pages else "?"} (explain each)')
            print('\n'.join(ln for ln in out.splitlines() if ln.startswith('  page '))[:1500])
        if check_data:
            errs = 0
            for f in sorted(data_dir.glob(f'4[02]_*{nid}*.xml')):
                code, out = run([sys.executable, str(check_data), '--src', 'framework', '--src',
                                 'runtime/component/mantle-udm', '--src', 'runtime/component/moqui-math', '--src',
                                 'runtime/component/mantle-compliance', str(f)], FRAMEWORK)
                m = re.search(r'errors=(\d+)', out)
                errs += int(m.group(1)) if m else 1
                if not m or int(m.group(1)):
                    print(f'== {nid}: check_data {f.name}\n' + '\n'.join(out.splitlines()[-8:]))
            row['check_data'] = f'{errs} errors'
            failed |= errs > 0
        else:
            row['check_data'] = 'skipped (moqui-data skill not found)'
        rows.append(row)
    shared = []
    for name, cmd, cwd in (('norm-kb tests', [sys.executable, '-m', 'unittest', 'discover', 'tests'], NORMKB),
                           ('extraction tests', [sys.executable, '-m', 'unittest', 'discover', 'tests'], EXTRACTION),
                           ('vocab.py --check', [sys.executable, 'vocab.py', '--check'], EXTRACTION)):
        code, out = run(cmd, cwd)
        ok = code == 0 and 'ERROR' not in out
        shared.append((name, 'ok' if ok else 'FAIL'))
        failed |= not ok
        if not ok:
            print(f'== {name}\n' + '\n'.join(out.splitlines()[-20:]))
    # the vocabulary seed is generated from the hooks files: data/60_ must be what they give now
    vocab_seed = COMPONENT / 'data' / '60_CmpVocabulary.xml'
    if vocab_seed.exists():
        code, out = run([sys.executable, 'vocab.py', '--out', str(scratch / '60_CmpVocabulary.xml')], EXTRACTION)
        seed_rows = lambda f: {l.strip() for l in f.read_text(encoding='utf-8').splitlines() if l.strip().startswith('<moqui.')}
        gen = scratch / '60_CmpVocabulary.xml'
        removed, added = (seed_rows(vocab_seed) - seed_rows(gen), seed_rows(gen) - seed_rows(vocab_seed)) if gen.exists() else (set(), {'?'})
        same = code == 0 and not removed and not added
        shared.append(('vocabulary (60_)', 'same' if same else f'-{len(removed)} +{len(added)} rows (regenerate: vocab.py)'))
        failed |= not same
        if not same:
            print('== vocabulary differs from data/60_ (explain every change, then run vocab.py)\n' +
                  '\n'.join(f'   {s} {l[:200]}' for s, ls in (('-', removed), ('+', added)) for l in sorted(ls)[:10]))
    for nid, (alias, langs) in aliases_and_languages(cfg).items():
        code, roots = run([sys.executable, 'dump_part.py', nid, alias, '--roots'], EXTRACTION)
        for lang in langs:
            code, out = run([sys.executable, 'check_hooks.py', nid, *roots.split(), '--alias', alias, '--lang', lang],
                            EXTRACTION)
            m = re.search(r'# (\d+) findings', out)
            n_find = int(m.group(1)) if m else -1
            stale = out.count('# stale review')
            shared.append((f'hooks {nid} {lang}', f'{n_find} findings' + (f', {stale} stale reviews' if stale else '')))
            failed |= n_find != 0
    # the shared seeds (types, stubs, vocabulary, associations) against the entity model, lengths included
    if check_data:
        for name in ('10_ComplianceTypeData', '41_NormStubs', '60_CmpVocabulary', '70_CmpAssociations', '80_CmpNormSearch'):
            f = COMPONENT / 'data' / f'{name}.xml'
            if not f.exists():
                continue
            code, out = run([sys.executable, str(check_data), '--src', 'framework', '--src', 'runtime/component/mantle-udm',
                             '--src', 'runtime/component/moqui-math', '--src', 'runtime/component/mantle-compliance',
                             str(f)], FRAMEWORK)
            m = re.search(r'errors=(\d+)', out)
            ok = bool(m) and m.group(1) == '0'
            shared.append((f'check_data {name}', 'ok' if ok else f'FAIL ({m.group(1) if m else "?"} errors)'))
            failed |= not ok
            if not ok:
                print(f'== check_data {name}\n' + '\n'.join(out.splitlines()[-8:]))
    # the associative graph of the norms, from the seeds: compared with data/70_CmpAssociations.xml
    code, out = run([sys.executable, str(paths.ASSOC / 'assoc.py'), '--sample', '0', '--compare'], COMPONENT)
    m = re.search(r'^ASSOC (.*)$', out, re.M)
    shared.append(('associations (70_)', m.group(1) if m and code == 0 else 'FAIL'))
    failed |= code != 0 or not m
    if m and m.group(1) != 'same':
        print('== associations differ from data/70_ (explain every change)\n' +
              '\n'.join(l for l in out.splitlines() if l.startswith(('   -', '   +', '==', 'total'))))
    if a.db:
        sqlq = skill_file('moqui-seed-reload/scripts/sqlq.sh')
        for q in ('agreement-checks.sql', 'cross-references.sql'):
            f = skill_file(f'moqui-seed-reload/assets/{q}')
            code, out = run(['bash', str(sqlq), q, str(f)], COMPONENT)
            bad = [ln for ln in out.splitlines()[2:] if ln.split(' | ')[-1].strip() not in ('0', '')]
            shared.append((f'db {q}', 'ok' if code == 0 and not bad and 'error=None' in out else 'FAIL'))
            print(out)
            failed |= bool(bad) or 'error=None' not in out
        # the database holds exactly the seeds: items and associations per Agreement (a load never deletes, so rows
        # of an older build stay unless deleted; a delete of the rows of one edition can drop a link of another)
        want = {}
        for f in sorted((COMPONENT / 'data').glob('4[02]_*.xml')):
            text = f.read_text(encoding='utf-8')
            for kind in ('AgreementItem', 'AgreementAssoc'):
                for m in re.finditer(rf'<mantle\.party\.agreement\.{kind}\b[^>]*?\bagreementId="([^"]+)"', text):
                    want.setdefault(m.group(1), [0, 0])[kind == 'AgreementAssoc'] += 1
        if want:
            ids = ','.join(f"'{i}'" for i in sorted(want))
            f = scratch / 'seed-counts.sql'
            f.write_text(f'SELECT AGREEMENT_ID, SUM(I) ITEMS, SUM(S) ASSOCS FROM (SELECT AGREEMENT_ID, 1 I, 0 S FROM '
                         f'AGREEMENT_ITEM WHERE AGREEMENT_ID IN ({ids}) UNION ALL SELECT AGREEMENT_ID, 0, 1 FROM '
                         f'AGREEMENT_ASSOC WHERE AGREEMENT_ID IN ({ids})) GROUP BY AGREEMENT_ID ORDER BY 1', encoding='utf-8')
            code, out = run(['bash', str(sqlq), 'seed-counts', str(f)], COMPONENT)
            got = {r[0]: [int(x.replace(',', '')) for x in r[1:3]] for r in
                   (ln.split(' | ') for ln in out.splitlines()[2:]) if len(r) == 3}
            bad = [f'{i}: seeds {w[0]} items {w[1]} assocs, db {got.get(i, [0, 0])[0]} / {got.get(i, [0, 0])[1]}'
                   for i, w in sorted(want.items()) if got.get(i) != w]
            shared.append(('db = seeds (items, assocs per Agreement)', 'ok' if code == 0 and not bad and 'error=None' in out
                           else f'FAIL ({len(bad)} agreements)'))
            if bad:
                print('== database differs from the seeds (delete and reload, moqui-seed-reload)\n' + '\n'.join(bad))
            failed |= bool(bad) or 'error=None' not in out
        # the associative graph: counts per kind for the log, the rows "check: ..." must be 0
        f = skill_file('moqui-norm-associations/assets/assoc-checks.sql')
        if f:
            code, out = run(['bash', str(sqlq), 'assoc-checks', str(f)], COMPONENT)
            bad = [ln for ln in out.splitlines() if ln.startswith('check:') and ln.split(' | ')[-1].strip() != '0']
            shared.append(('db assoc-checks.sql', 'ok' if code == 0 and not bad and 'error=None' in out else 'FAIL'))
            print(out)
            failed |= bool(bad) or 'error=None' not in out
    print('\n| norm | build | diff | refs | content | check_data |\n|---|---|---|---|---|---|')
    for r in rows:
        print(f"| {r['norm']} | {r.get('build', '')} | {r.get('diff', '')} | {r.get('refs', '')} | {r.get('content', '')} "
              f"| {r.get('check_data', '')} |")
    print('\n| check | result |\n|---|---|')
    for name, res in shared:
        print(f'| {name} | {res} |')
    print('\nRESULT:', 'FAIL' if failed else 'PASS')
    shutil.rmtree(scratch, ignore_errors=True)
    return 1 if failed else 0


if __name__ == '__main__':
    sys.exit(main())
