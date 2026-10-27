#!/usr/bin/env python3
"""Edit a hooks extension file (data/norms/vocabulary/HOOKS-<normId>.json of mantle-compliance) keeping its layout: one top-level key per line, one
list element per line, so that every hook pass shows as a small diff.

    python3 hooks_file.py add vocabulary/HOOKS-ISO-12100-2010.json part.json   # merge one part
    python3 hooks_file.py unreview vocabulary/HOOKS-ISO-12100-2010.json 3.40:TERM:fn-stop 6.2.7.li1:WORD
    python3 hooks_file.py format vocabulary/HOOKS-ISO-12100-2010.json
    python3 hooks_file.py dedupe vocabulary/HOOKS-ISO-12100-2010.json   # same link or review given twice
    python3 hooks_file.py labels vocabulary/LABELS-it.json new-labels.json  # names of new concepts
    python3 hooks_file.py migrate T old/40_Norm_X_IT.xml new/40_Norm_X_IT.xml --labels vocabulary/LABELS-it.json \
        [--write] vocabulary/VOCAB-BASE.json vocabulary/HOOKS-*.json         # links of items the reader moved

A part file has the keys of a hooks file: part (its name in `parts`), about, concepts, addClauses, addFeatureGroups,
reviewed, lexiconSkip, normLexiconSkip, proceduralParts, referenceParts. `unreview` removes the reviews that check_hooks.py prints as stale.
"""
import json
import re
import sys

LISTS = ('concepts', 'addClauses', 'addFeatureGroups', 'reviewed', 'lexiconSkip', 'proceduralParts', 'referenceParts', 'normLexiconSkip')


def dumps(d):
    out = ['{']
    keys = list(d)
    for i, k in enumerate(keys):
        v, comma = d[k], ',' if i < len(keys) - 1 else ''
        key = json.dumps(k)
        if isinstance(v, dict) and v:
            out.append(f'  {key}: {{')
            out.append(',\n'.join(f'    {json.dumps(a, ensure_ascii=False)}: {json.dumps(b, ensure_ascii=False)}'
                                  for a, b in v.items()))
            out.append('  }' + comma)
        elif isinstance(v, list) and v:
            out.append(f'  {key}: [')
            out.append(',\n'.join('    ' + json.dumps(x, ensure_ascii=False) for x in v))
            out.append('  ]' + comma)
        else:
            out.append(f'  {key}: {json.dumps(v, ensure_ascii=False)}{comma}')
    out.append('}')
    return '\n'.join(out) + '\n'


def load(path):
    with open(path, encoding='utf-8') as fh:
        return json.load(fh)


def save(path, d):
    with open(path, 'w', encoding='utf-8') as fh:
        fh.write(dumps(d))


def add(path, part_path):
    d, p = load(path), load(part_path)
    d.setdefault('parts', {})[p['part']] = p['about']
    for k in LISTS:
        d.setdefault(k, []).extend(p.get(k, []))
    save(path, d)
    return {k: len(d[k]) for k in LISTS}


def unreview(path, drops):
    d = load(path)
    drop = {tuple(x.split(':', 1)) for x in drops}
    before = len(d['reviewed'])
    d['reviewed'] = [r for r in d['reviewed'] if (r[0], r[1]) not in drop]
    save(path, d)
    return before - len(d['reviewed'])


def dedupe(path):
    d = load(path)
    removed = 0
    # links a concept of this file already has in its own clauses
    own = {(c['key'], ref) for c in d.get('concepts', []) for ref, _role in c.get('clauses', [])}
    for key, ident in (('addClauses', lambda a: (a[0], a[1])), ('reviewed', lambda r: (r[0], r[1]))):
        seen, out = set(own) if key == 'addClauses' else set(), []
        for a in d.get(key, []):
            if ident(a) not in seen:
                seen.add(ident(a))
                out.append(a)
        removed += len(d.get(key, [])) - len(out)
        d[key] = out
    save(path, d)
    return removed


def dump_labels(d):
    """A LABELS-<lang>.json file: one key per line at the top, one concept per line in "labels", sorted."""
    out = ['{']
    keys = list(d)
    for i, k in enumerate(keys):
        comma = ',' if i < len(keys) - 1 else ''
        if k == 'labels':
            out.append('  "labels": {')
            out.append(',\n'.join(f'    {json.dumps(a, ensure_ascii=False)}: {json.dumps(b, ensure_ascii=False)}'
                                  for a, b in sorted(d[k].items())))
            out.append('  }' + comma)
        elif isinstance(d[k], list) and d[k]:
            out.append(f'  {json.dumps(k)}: [')
            out.append(',\n'.join('    ' + json.dumps(x, ensure_ascii=False) for x in d[k]))
            out.append('  ]' + comma)
        else:
            out.append(f'  {json.dumps(k)}: {json.dumps(d[k], ensure_ascii=False)}{comma}')
    out.append('}')
    return '\n'.join(out) + '\n'


def add_labels(path, new_path):
    """Merge {concept: [label, other terms]} into a LABELS file; a concept already named is an error."""
    d, new = load(path), load(new_path)
    clash = sorted(k for k in new if k in d['labels'] and d['labels'][k] != new[k])
    if clash:
        sys.exit(f'already named differently: {clash}')
    d['labels'].update(new)
    with open(path, 'w', encoding='utf-8') as fh:
        fh.write(dump_labels(d))
    return len(new)


def seed_items(path):
    """itemSeqId -> (parent, text) of an Agreement seed file (40_Norm_*.xml)."""
    import xml.etree.ElementTree as ET
    out = {}
    for e in ET.parse(path).getroot():
        if e.tag.endswith('.AgreementItem'):
            t = e.find('itemText')
            text = ' '.join(((t.text if t is not None else '') or '').split())
            out[e.get('agreementItemSeqId')] = (e.get('parentItemSeqId'), text or (e.get('itemTitle') or ''))
    return out


def migration(old, new, names):
    """New id(s) for an item id of the old seeds that the new seeds do not have, by content (letters and digits
    only, so that a symbol now read as a Greek letter or a cell separator does not hide it): the same text; the item
    that took the text in (a legend joined to its formula); the new items the old text was split into that name the
    concept (a block of index lines read as table rows), none when no part names it; else the old parent."""
    key = lambda t: re.sub(r'[^0-9a-zà-ÿ]', '', t.lower())
    new_keys = {k: key(t) for k, (_p, t) in new.items()}

    def go(sid, text, parent):
        k_old = key(text)
        same = [k for k, t in new_keys.items() if t == k_old]
        if same:
            return same[:1], 'same text'
        took = [k for k, t in new_keys.items() if k_old and k_old in t]
        if took:
            return sorted(took, key=lambda k: (new[k][0] != parent, len(new_keys[k])))[:1], 'text taken in'
        parts = [k for k, t in new_keys.items() if (k not in old or key(old[k][1]) != t) and len(t) > 8 and
                 key(new[k][1].split(': ', 1)[-1]) in k_old]
        if parts:
            named = [k for k in parts if any(n in new[k][1].lower() for n in names)]
            return named, 'split, parts naming the concept' if named else 'split, no part names the concept: dropped'
        return ([parent] if parent in new else []), 'parent'
    return go


def migrate(paths, alias, old_seed, new_seed, labels=None, write=False):
    """Move the links and reviews of the hooks files from items the reader no longer produces to the items that now
    hold their text. Prints every move; --write saves the files (then run dedupe)."""
    old, new = seed_items(old_seed), seed_items(new_seed)
    key = lambda t: re.sub(r'[^0-9a-zà-ÿ]', '', t.lower())
    # items that vanished, and ids that now hold another text (after a legend joined its formula, D.2.p7 is
    # another paragraph): a link must follow its text, not its id. Run once per pair of seeds.
    gone = {k for k in old if k not in new or key(old[k][1]) != key(new[k][1])}
    norm_id = re.match(r'40_Norm_(.+)_[A-Z]{2}\.xml$', old_seed.split('/')[-1]).group(1)
    local = load(labels)['labels'] if labels else {}
    concepts = {}
    for path in paths:
        for c in load(path).get('concepts', []):
            concepts[c['key']] = c

    def names(key):
        c = concepts.get(key, {})
        out = [re.sub(r'\s*\([^)]*\)', '', c.get('label', '')).strip().lower()]
        out += [re.sub(r'\s*\([^)]*\)', '', x).strip().lower() for x in local.get(key, [])]
        return [n for n in out if len(n) > 2]
    unresolved = 0
    for path in paths:
        d = load(path)
        changed = False

        def move(key, ref):
            nonlocal changed, unresolved
            if not ref.startswith(alias + '@') or ref.split('@', 1)[1] not in gone:
                return [ref]
            sid = ref.split('@', 1)[1]
            ids, how = migration(old, new, names(key))(sid, old[sid][1], old[sid][0])
            print(f'{path.split("/")[-1]}: {key} {ref} -> {[alias + "@" + i for i in ids]} ({how})')
            changed = True
            if not ids and 'dropped' not in how:
                unresolved += 1
                return [ref]
            return [alias + '@' + i for i in ids]
        for c in d.get('concepts', []):
            c['clauses'] = [[r2, role] for r, role in c.get('clauses', []) for r2 in move(c['key'], r)]
        d['addClauses'] = [[k, r2, *rest] for k, r, *rest in d.get('addClauses', []) for r2 in move(k, r)]
        # reviews name items of the norm of their file (HOOKS-<normId>.json)
        if d.get('reviewed') and path.split('/')[-1] == f'HOOKS-{norm_id}.json':
            d['reviewed'] = [[r2.split('@', 1)[1], *rest] for sid, *rest in d['reviewed']
                             for r2 in move(rest[0], alias + '@' + sid)]
        if changed and write:
            save(path, d)
    return unresolved


def main(argv):
    if len(argv) < 2 or argv[0] not in ('add', 'unreview', 'format', 'dedupe', 'migrate', 'labels'):
        sys.exit(__doc__)
    cmd, path = argv[0], argv[1]
    if cmd == 'migrate':
        # migrate <alias> <old 40_ seed> <new 40_ seed> [--labels LABELS-xx.json] [--write] <hooks files...>
        args = argv[1:]
        write = '--write' in args
        args = [a for a in args if a != '--write']
        labels = None
        if '--labels' in args:
            k = args.index('--labels')
            labels = args[k + 1]
            del args[k:k + 2]
        alias, old_seed, new_seed, files = args[0], args[1], args[2], args[3:]
        n = migrate(files, alias, old_seed, new_seed, labels, write)
        print(f'{n} links without a new item')
        return 1 if n else 0
    if cmd == 'labels':
        # labels vocabulary/LABELS-it.json new-labels.json
        print(add_labels(path, argv[2]), 'concepts named')
        return 0
    if cmd == 'add':
        print(add(path, argv[2]))
    elif cmd == 'unreview':
        print(unreview(path, argv[2:]), 'reviews removed')
    elif cmd == 'dedupe':
        print(dedupe(path), 'duplicates removed')
    else:
        save(path, load(path))
    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
