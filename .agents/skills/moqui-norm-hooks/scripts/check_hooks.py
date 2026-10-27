#!/usr/bin/env python3
"""Verification of a hook pass (PLAN-NORMS-AGREEMENT.md section 5): what the text of a part names and the hooks do not
link. Three reports per item of the part:

- TERM   the text contains the label, an alternative label or a defined term of a concept that is not linked to the
         item (possible missed hook);
- NUMBER the text contains a value with a unit (mm, m, V, dB, Pa, kg, years, ...) and no quantitative feature is linked
         to the item (possible missed threshold);
- WORD   the text names a component (device, equipment, sensor, switch, display, ...) and no product concept is
         linked to the item or to its ancestors (possible missing category).

A finding is either fixed in the hooks file or declared not a hook in its `reviewed` list ([item, kind, reason]), so
the check is repeatable: a part is verified when it reports nothing new.

    python3 check_hooks.py EU-REG-2023-1230 ANXIII.B.1.2 [ANXIII.B.1.3 ...]
"""
import argparse
import glob
import json
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent.parent / 'moqui-norm-loading' / 'scripts'))

from normkb import paths                    # noqa: E402
from normkb.items import read_items_jsonl   # noqa: E402
from normkb.std_items import BOX_PREFIX       # noqa: E402

UNITS = r'(?:mm/s|m/s|km/h|mm|cm|m|kg|t|N|kN|V|kV|A|W|kW|Hz|dB|dB\s*\(A\)|Pa|kPa|MPa|bar|°C|K|s|ms|min|h|years?|months?|days?|lux|%)'
NUMBER = re.compile(r'(?<![\w.,])(\d+(?:[.,]\d+)?)\s*' + UNITS + r'(?![\w/])')
COMPONENT_WORDS_EN = re.compile(r'\b(devices?|equipment|sensors?|switch(?:es)?|displays?|cabins?|seats?|guards?|valves?|'
                             r'brakes?|hoses?|pipes?|cables?|connectors?|screens?|indicators?|pendants?|selectors?|'
                             r'actuators?|motors?|drives?|batter(?:y|ies)|filters?|lamps?|lights|systems?|tools?|'
                             r'platforms?|ladders?|handholds?|ropes?|hooks?|carriers?|controls?)\b', re.I)
# the same words in Italian editions
COMPONENT_WORDS_IT = re.compile(r'\b(dispositiv[oi]|apparecchiatur[ae]|equipaggiament[oi]|sensor[ei]|interruttor[ei]|display|'
                                r'cabin[ae]|sedil[ei]|ripar[oi]|valvol[ae]|fren[oi]|tub[oi] flessibil[ei]|tubazion[ei]|'
                                r'cav[oi]|connettor[ei]|schermo|schermi|indicator[ei]|pulsantier[ae]|selettor[ei]|attuator[ei]|'
                                r'motor[ei]|azionament[oi]|batteri[ae]|filtr[oi]|lampad[ae]|sistem[ai]|utensil[ei]|'
                                r'piattaform[ae]|scal[ae]|funi|gancio|ganci|contattor[ei]|relè|controllor[ei]|componenti?)\b', re.I)
COMPONENT_WORDS = {'en': COMPONENT_WORDS_EN, 'it': COMPONENT_WORDS_IT}


review_langs = {}   # (item, kind) -> language the review was made for


def load(norm_id, alias):
    items = read_items_jsonl(paths.ITEMS / f'{norm_id}.jsonl')
    by_id = {i.seqId: i for i in items}
    files = [paths.VOCABULARY / 'VOCAB-BASE.json'] + sorted(Path(p) for p in glob.glob(str(paths.VOCABULARY / 'HOOKS-*.json')))
    concepts, links, reviewed = {}, {}, set()
    review_langs.clear()
    skip = set()
    procedural = set()  # parts that lay down procedures, not product properties: only TERM is checked
    references = set()  # lists of cited documents (normative references, bibliography): titles, not checked
    data = [(f, json.loads(f.read_text(encoding='utf-8'))) for f in files]
    for f, d in data:
        for c in d.get('concepts', []):
            concepts[c['key']] = c
    for f, d in data:
        for key, ref, role in d.get('addClauses', []):
            concepts[key].setdefault('clauses', []).append([ref, role])
        skip.update(k for k, _reason in d.get('lexiconSkip', []))
        if f.name != f'HOOKS-{norm_id}.json':
            continue
        # a concept whose name has another sense in this norm ("protective device" = electrical protective device in
        # IEC 60204-1): skipped for this norm only
        skip.update(k for k, _reason in d.get('normLexiconSkip', []))
        # reviewed findings and procedural parts are item ids of this norm: only its own hooks file
        for r in d.get('reviewed', []):
            # [item, kind, reason] or [item, kind, reason, language]: a review made for one language of the norm
            reviewed.add((r[0], r[1]))
            review_langs[(r[0], r[1])] = r[3] if len(r) > 3 else d.get('language', 'en')
        procedural.update(sid for sid, _reason in d.get('proceduralParts', []))
        references.update(sid for sid, _reason in d.get('referenceParts', []))
    for c in concepts.values():
        for ref, _role in c.get('clauses', []):
            if ref.startswith(alias + '@'):
                links.setdefault(ref.split('@', 1)[1], set()).add(c['key'])
    return items, by_id, concepts, links, reviewed, skip, procedural, references


HOOK_SCHEMES = {'product', 'feature', 'featureGroup', 'function', 'memberRole'}
# concepts of the scope, true of every item of the act: never reported
SCOPE = {'machinery', 'related-product', 'reg-product', 'partly-completed-machinery'}


def clean(name):
    return re.sub(r'\s+', ' ', re.sub(r'\([^)]*\)', '', name)).strip().lower()


IT_PREPOSITIONS = {'di', 'del', 'della', 'dei', 'delle', 'degli', 'a', 'al', 'alla', 'ai', 'per', 'con', 'da', 'in', 'su', 'e', 'o'}


def plural_it_word(w):
    """Plural forms of one Italian word: -ma -> -mi (sistema), -ca/-ga -> -che/-ghe, -co/-go -> both -ci/-chi
    (elettrici, blocchi), -o/-e -> -i, -a -> -e; short and accented words do not change."""
    if len(w) <= 3 or not re.search(r'[oae]$', w):
        return [w]
    if w.endswith('ma'):
        return [w[:-1] + 'i']
    if re.search(r'[cg]a$', w):
        return [w[:-1] + 'he']
    if re.search(r'[cg]o$', w):
        return [w[:-1] + 'i', w[:-1] + 'hi']
    return [w[:-1] + ('e' if w.endswith('a') else 'i')]


def plural_it(name):
    """Plural forms of an Italian name: the words before the first preposition change their ending (dispositivo di
    abilitazione -> dispositivi di abilitazione, riparo mobile -> ripari mobili); in a second form the adjectives after
    the complement agree too (sistema di controllo relativo alla sicurezza -> sistemi di controllo relativi alla
    sicurezza): every word that is not a preposition and does not follow one."""
    words = name.split()
    k = next((i for i, w in enumerate(words) if w in IT_PREPOSITIONS), len(words))
    out = []
    for change in ([i < k for i in range(len(words))],
                   [w not in IT_PREPOSITIONS and (i == 0 or words[i - 1] not in IT_PREPOSITIONS)
                    for i, w in enumerate(words)]):
        forms = [[]]
        for w, c in zip(words, change):
            forms = [f + [p] for f in forms for p in (plural_it_word(w) if c else [w])]
        out += [' '.join(f) for f in forms if ' '.join(f) not in out]
    return out


def names(c, by_id, labels=frozenset(), local=None, lang='en'):
    """Words that name a concept: its label (without parenthesised parts) and the defined terms of its defining
    items that share a word with the label (a concept linked to the definition of another notion does not take
    that notion's term). In another language (local = [label, other terms ...] of LABELS-<lang>.json) the label and
    the other terms of that language, and the defined terms of that language."""
    out = set()
    lab = clean(local[0] if local else c['label'])
    words = {w for w in re.findall(r'[a-zà-ÿ]{4,}', lab)}
    for n in [lab] + [clean(x) for x in (local or [])[1:]]:
        if len(n) > 2 and len(n.split()) <= 6:
            out.add(n)
            if lang == 'it' and local:
                out.update(plural_it(n))
    for ref, role in c.get('clauses', []):
        if role == 'd' and '@' in ref:
            it = by_id.get(ref.split('@', 1)[1])
            if it:
                terms = [it.term.get(lang)] if local else list(it.term.values())
                # the term of a notion that has a concept of its own (labels) is that concept's name
                out.update(t.lower() for t in terms if t and words & set(re.findall(r'[a-zà-ÿ]{4,}', t.lower()))
                           and (t.lower() == lab or t.lower() not in labels))
    return out


def ancestors(sid, by_id):
    out = []
    while sid in by_id and by_id[sid].parentSeqId:
        sid = by_id[sid].parentSeqId
        out.append(sid)
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('normId')
    ap.add_argument('parts', nargs='+')
    ap.add_argument('--alias', default='R')
    ap.add_argument('--lang', default='en')
    a = ap.parse_args()
    items, by_id, concepts, links, reviewed, skip, procedural, references = load(a.normId, a.alias)
    local = {}
    lp = paths.VOCABULARY / f'LABELS-{a.lang}.json'
    if a.lang != 'en' and lp.exists():
        ld = json.loads(lp.read_text(encoding='utf-8'))
        local = ld['labels']
        # names too generic in that language to be found mechanically ("protezione")
        skip = skip | {k for k, _reason in ld.get('lexiconSkip', [])}
    labels = frozenset(clean(local[k][0] if k in local else c['label']) for k, c in concepts.items())
    lexicon = [(n, k) for k, c in concepts.items() if c['scheme'] in HOOK_SCHEMES and k not in SCOPE | skip
               for n in names(c, by_id, labels, local.get(k), a.lang)]
    findings = []
    used = set()     # reviewed findings that still occur
    checked = set()
    for it in items:
        # an item belongs to a part when it is the part or one of its descendants (recitals REC1.. are below PRE)
        if it.seqId not in a.parts and not set(ancestors(it.seqId, by_id)) & set(a.parts):
            continue
        if it.seqId in references or set(ancestors(it.seqId, by_id)) & references:
            continue
        if it.type == 'AitFigure' and any(c.parentSeqId == it.seqId for c in items):
            # a modelled figure: its text joins the text of its boxes, which are checked one by one
            continue
        checked.add(it.seqId)
        text = (it.text.get(a.lang) or '')
        if BOX_PREFIX.match(text):
            # a box of a modelled figure: its own label, not the boxes its flows lead to
            text = text.split(' -> ', 1)[0]
        # names broken over two lines and plurals match too ("fixed\nguard", "guard-rails")
        low = re.sub(r'\s+', ' ', text.lower())
        linked = links.get(it.seqId, set())
        up = set().union(*(links.get(x, set()) for x in ancestors(it.seqId, by_id)))
        reported = set()
        # an occurrence inside the name of a linked concept is not a finding ("guard" in a linked "adjustable guard")
        spans = [m.span() for n, k in lexicon if k in linked or k in up
                 for m in re.finditer(r'\b' + re.escape(n) + r'(?:s|es)?\b', low)]

        def free(n):
            return any(not any(a <= m.start() and m.end() <= b and (b - a) > len(n) for a, b in spans)
                       for m in re.finditer(r'\b' + re.escape(n) + r'(?:s|es)?\b', low))
        for n, k in lexicon:
            if k not in linked and k not in up and k not in reported and free(n):
                if (it.seqId, f'TERM:{k}') in reviewed:
                    used.add((it.seqId, f'TERM:{k}'))
                else:
                    findings.append((it.seqId, f'TERM:{k}', n))
                    reported.add(k)
        if it.seqId in procedural or set(ancestors(it.seqId, by_id)) & procedural:
            continue
        quantitative = any('number' in concepts[k] for k in linked)
        # the number of a note or example ("NOTE 1 A hazard ...") is not a value
        for m in NUMBER.finditer(re.sub(r'\b(NOTE|NOTA|EXAMPLE|ESEMPIO)\s+\d+', '', text)):
            if not quantitative and (it.seqId, 'NUMBER') in reviewed:
                used.add((it.seqId, 'NUMBER'))
            elif not quantitative:
                findings.append((it.seqId, 'NUMBER', m.group(0)))
                break
        products = [k for k in linked | up if concepts[k]['scheme'] == 'product' and k not in SCOPE]
        if not products:
            m = COMPONENT_WORDS.get(a.lang, COMPONENT_WORDS_EN).search(text)
            if m and (it.seqId, 'WORD') in reviewed:
                used.add((it.seqId, 'WORD'))
            elif m:
                findings.append((it.seqId, 'WORD', text[max(0, m.start() - 40):m.end() + 30].replace('\n', ' ')))
    for f in findings:
        print('\t'.join(f))
    # a review whose finding no longer occurs (fixed by a link or by the check itself) is to be removed
    # reviews were made in the language of the hooks file (key language, default en): stale only there
    for sid, kind in sorted(r for r in reviewed if r[0] in checked and r not in used and review_langs.get(r) == a.lang):
        print(f'# stale review {sid} {kind}', file=sys.stderr)
    print(f'# {len(findings)} findings in {", ".join(a.parts)}', file=sys.stderr)
    return 0


if __name__ == '__main__':
    sys.exit(main())
