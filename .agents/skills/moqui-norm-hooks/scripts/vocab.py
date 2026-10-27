"""Shared vocabulary of the norms: proposal JSON to Moqui seed data.

A vocabulary proposal (data/norms/vocabulary/VOCAB-*.json of mantle-compliance) lists concepts. Each concept is one notion shared by all norms of the
knowledge base, cited by every clause that defines, specifies, lists or excludes it. The converter writes:

- a moqui.math Graph NG_CMP_VOCABULARY: one GraphVertex per concept, GraphEdges for broader and related, Parameters
  for key, scheme, label, description, the norm items that cite the concept (CmpConceptItem: agreementId and
  agreementItemSeqId, parameterEnumId = role) and the mantle record that realises the concept (symbolicValue = entity,
  textValue = pk; its id is also on the vertex);
- the mantle and moqui-device records realising product-facing concepts: ProductCategory and ProductCategoryRollup
  (scheme product), ProductFeatureGroup (featureGroup), ProductFeature and ProductFeatureGroupAppl (feature),
  ProductCategoryFeatGrpAppl (featureGroups of a product), DevicePurpose Enumerations (function, memberRole).

Concepts of scheme term, actor, process and document live only in the graph: the procedural layer refers to them.
Every id is derived from the concept key, so regenerating gives the same records.
"""
import hashlib
import json
import re
import sys
from pathlib import Path
from xml.sax.saxutils import escape, quoteattr

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent / 'moqui-norm-loading' / 'scripts'))
from normkb import paths  # noqa: E402
from normkb.ir import vertex_id  # noqa: E402
from normkb.items import read_items_jsonl     # noqa: E402

GRAPH_ID = 'NG_CMP_VOCABULARY'
VOCAB_NS = 'CMP-VOCAB'
FROM_DATE = '2026-01-01 00:00:00.000'
ID_MAX = 40
LABEL_MAX = 63
DESCRIPTION_MAX = 400
COPY_WORDS = 8
PUBLIC_PREFIXES = ('EU-',)

SCHEMES = {
    'product': 'CmpCsProduct', 'featureGroup': 'CmpCsFeatureGroup', 'feature': 'CmpCsFeature',
    'function': 'CmpCsFunction', 'memberRole': 'CmpCsMemberRole', 'term': 'CmpCsTerm', 'actor': 'CmpCsActor',
    'process': 'CmpCsProcess', 'document': 'CmpCsDocument',
}
ROLES = {'d': 'CmpCcrDefines', 's': 'CmpCcrSpecifies', 'l': 'CmpCcrLists', 'x': 'CmpCcrExcludes'}
FEATURE_TYPES = {'CmpPftHazardOrigin', 'CmpPftWorkedMaterial', 'CmpPftLoadingMode', 'CmpPftUseCharacteristic',
                 'CmpPftAdaptiveBehaviour', 'CmpPftEnergySource', 'CmpPftConnectivity', 'CmpPftMotion',
                 'CmpPftFallHeight', 'CmpPftNoiseEmission', 'CmpPftHygiene', 'CmpPftHazardConsequence', 'CmpPftElectricalRating', 'CmpPftEnvironment', 'CmpPftFunctionalSafety', 'CmpPftSecurityLevel', 'CmpPftProcessMaturity', 'CmpPftCyberSecurity',
                 'CmpPftVibrationEmission', 'CmpPftLiftingRating'}
COMPARISONS = {'>', '>=', '<', '<=', '='}
GRAPH_ONLY = {'term', 'actor', 'process', 'document'}
# scheme of a concept -> schemes allowed for its broader concepts
BROADER_OK = {
    'product': {'product'}, 'featureGroup': set(), 'feature': {'featureGroup'}, 'function': {'function'},
    'memberRole': {'memberRole'}, 'term': GRAPH_ONLY, 'actor': GRAPH_ONLY, 'process': GRAPH_ONLY,
    'document': GRAPH_ONLY,
}
ENTITY = {
    'product': 'mantle.product.category.ProductCategory', 'featureGroup': 'mantle.product.feature.ProductFeatureGroup',
    'feature': 'mantle.product.feature.ProductFeature', 'function': 'moqui.basic.Enumeration',
    'memberRole': 'moqui.basic.Enumeration',
}


def snake(key):
    return re.sub(r'[^A-Z0-9]+', '_', key.upper()).strip('_')


def camel(key):
    return ''.join(p[:1].upper() + p[1:] for p in re.split(r'[^A-Za-z0-9]+', key) if p)


# field of the vocabulary GraphVertex holding the record that realises the concept (entity/ComplianceEntities.xml)
HOOK_FIELD = {'product': 'productCategoryId', 'featureGroup': 'productFeatureGroupId', 'feature': 'productFeatureId',
              'function': 'enumId', 'memberRole': 'enumId'}


def record_id(c):
    """Primary key of the mantle record realising concept c, or None for graph-only schemes."""
    s, k = c['scheme'], c['key']
    if s == 'product':
        return 'CMP_PC_' + snake(k)
    if s == 'featureGroup':
        return 'CMP_PFG_' + snake(k)
    if s == 'feature':
        return 'CMP_PF_' + snake(k)
    if s == 'function':
        return 'CmpDep' + camel(k[3:] if k.startswith('fn-') else k)
    if s == 'memberRole':
        return 'CmpDep' + camel(k)
    return None


def concept_vertex(key):
    return vertex_id(f'{VOCAB_NS}:{key}')


def short_id(prefix, *parts):
    return prefix + hashlib.sha1('|'.join(parts).encode('utf-8')).hexdigest()[:30]


class Vocabulary:
    def __init__(self, proposal_path, ir_dir, extensions=()):
        self.path = Path(proposal_path)
        self.data = json.loads(self.path.read_text(encoding='utf-8'))
        self.aliases = self.data.get('normAliases', {})
        self.concepts = self.data['concepts']
        self.extension_errors = []
        # concepts of all extensions first, then their links: an extension may link a concept of another one
        exts = [(Path(e), json.loads(Path(e).read_text(encoding='utf-8'))) for e in extensions]
        for path, ext in exts:
            self.extend(path, ext, links=False)
        for path, ext in exts:
            self.extend(path, ext, concepts=False)
        # names in other languages: LABELS-<lang>.json next to the proposal, per concept [preferred label, other terms ...]
        self.labels = {}
        for lp in sorted(self.path.parent.glob('LABELS-*.json')):
            ld = json.loads(lp.read_text(encoding='utf-8'))
            self.labels[ld['language']] = ld['labels']
        self.by_key = {}
        self.ir_dir = Path(ir_dir)
        # norms loaded as Agreement items (PLAN-NORMS-AGREEMENT.md): references "R@<agreementItemSeqId>"
        self.items, self.agreement = {}, {}
        cfg = json.loads(paths.CONFIG.read_text(encoding='utf-8'))
        for norm in cfg['norms']:
            f = self.ir_dir.parent / 'items' / f'{norm["normId"]}.jsonl'
            if f.exists() and norm['normId'] in self.data['norms']:
                self.items[norm['normId']] = {i.seqId: i for i in read_items_jsonl(f)}
                lang = list(norm['dirs'])[0] if norm['reader'] == 'formex' else norm['language']
                self.agreement[norm['normId']] = f'{norm["normId"]}-{lang.upper()}'

    def extend(self, path, ext, concepts=True, links=True):
        """Merge a vocabulary extension (kind vocabulary-extension, written by a hook pass): new concepts, and
        clauses added to concepts that already exist (addClauses: [key, ref, role])."""
        if concepts:
            if ext.get('kind') != 'vocabulary-extension':
                self.extension_errors.append(f'{path.name}: kind must be vocabulary-extension')
                return
            self.aliases.update(ext.get('normAliases', {}))
            for n in ext.get('norms', []):
                if n not in self.data['norms']:
                    self.data['norms'].append(n)
            self.concepts.extend(ext.get('concepts', []))
        if not links or ext.get('kind') != 'vocabulary-extension':
            return
        keys = {c['key']: c for c in self.concepts}
        for key, ref, role in ext.get('addClauses', []):
            if key not in keys:
                self.extension_errors.append(f'{path.name}: addClauses to unknown concept {key}')
            elif [ref, role] in keys[key]['clauses']:
                self.extension_errors.append(f'{path.name}: {key} already cites {ref} as {role}')
            else:
                keys[key]['clauses'].append([ref, role])
        for key, group in ext.get('addFeatureGroups', []):
            if key not in keys:
                self.extension_errors.append(f'{path.name}: addFeatureGroups to unknown concept {key}')
            elif group in keys[key].setdefault('featureGroups', []):
                self.extension_errors.append(f'{path.name}: {key} already has feature group {group}')
            else:
                keys[key]['featureGroups'].append(group)

    def item_ref(self, ref):
        """'R@ANXIII.B.1.2.1' -> (normId, item) or None when ref is an old clause id."""
        if '@' not in ref.split(':', 1)[0]:
            return None
        alias, seq = ref.split('@', 1)
        norm = self.aliases.get(alias, alias)
        return norm, self.items.get(norm, {}).get(seq), seq

    def cited_texts(self, ref):
        """(id, texts, terms, public) of a cited clause or item, None when unknown."""
        ir = self.item_ref(ref)
        if ir:
            norm, it, seq = ir
            return (f'{norm}:{seq}', list(it.text.values()), list(it.term.values()), norm.startswith(PUBLIC_PREFIXES)) \
                if it else None
        return None

    # ---------------------------------------------------------------- validation
    def validate(self):
        errors, warnings = list(self.extension_errors), []
        for c in self.concepts:
            k = c.get('key')
            if not k or not re.fullmatch(r'[a-z0-9]+(-[a-z0-9]+)*', k):
                errors.append(f'bad key {k!r}')
                continue
            if k in self.by_key:
                errors.append(f'{k}: duplicate key')
            self.by_key[k] = c
        # every concept named in every language of the LABELS files, and no label for an unknown concept
        for lang, labels in self.labels.items():
            for k in sorted(set(self.by_key) - set(labels)):
                errors.append(f'{k}: no label in LABELS-{lang}.json')
            # a label of a concept of an extension not loaded in this run (tests load the base only): not an error
            unknown = sorted(set(labels) - set(self.by_key))
            if unknown:
                warnings.append(f'LABELS-{lang}.json: {len(unknown)} labels of concepts not loaded, e.g. {unknown[:3]}')
            for k, names in labels.items():
                if not names or not all(isinstance(n, str) and n.strip() for n in names):
                    errors.append(f'LABELS-{lang}.json: {k} needs a preferred label')
        for c in self.concepts:
            k, s = c['key'], c.get('scheme')
            if s not in SCHEMES:
                errors.append(f'{k}: unknown scheme {s!r}')
                continue
            for f in ('label', 'description'):
                if not c.get(f):
                    errors.append(f'{k}: missing {f}')
            if len(c.get('description', '')) > DESCRIPTION_MAX:
                errors.append(f'{k}: description longer than {DESCRIPTION_MAX} characters')
            rid = record_id(c)
            if rid and len(rid) > ID_MAX:
                errors.append(f'{k}: record id {rid} longer than {ID_MAX}')
            for b in c.get('broader', []):
                if b not in self.by_key:
                    errors.append(f'{k}: broader {b} not defined')
                elif self.by_key[b]['scheme'] not in BROADER_OK[s]:
                    errors.append(f'{k}: broader {b} has scheme {self.by_key[b]["scheme"]}, not allowed for {s}')
            if s in ('function', 'memberRole') and len(c.get('broader', [])) > 1:
                errors.append(f'{k}: an Enumeration has one parent, broader has {len(c["broader"])}')
            if s == 'feature' and not c.get('broader'):
                errors.append(f'{k}: a feature needs at least one featureGroup in broader')
            if any(f in c for f in ('number', 'uom', 'comparison')):
                if s != 'feature':
                    errors.append(f'{k}: number / uom / comparison only on features')
                elif not isinstance(c.get('number'), (int, float)) or c.get('comparison', '=') not in COMPARISONS:
                    errors.append(f'{k}: a quantitative feature needs a numeric number and a comparison in {COMPARISONS}')
            for r in c.get('related', []):
                if r not in self.by_key:
                    errors.append(f'{k}: related {r} not defined')
            if s == 'featureGroup' and c.get('featureType') not in FEATURE_TYPES:
                errors.append(f'{k}: featureType {c.get("featureType")!r} not in {sorted(FEATURE_TYPES)}')
            for g in c.get('featureGroups', []):
                if s != 'product':
                    errors.append(f'{k}: featureGroups only on products')
                elif g not in self.by_key or self.by_key[g]['scheme'] != 'featureGroup':
                    errors.append(f'{k}: featureGroups {g} is not a featureGroup')
            if not c.get('clauses'):
                errors.append(f'{k}: no clause cited')
            for ref, role in c.get('clauses', []):
                if role not in ROLES:
                    errors.append(f'{k}: clause role {role!r}')
                ir = self.item_ref(ref)
                if ir:
                    if ir[0] not in self.items:
                        errors.append(f'{k}: {ref}: items of {ir[0]} not built')
                    elif ir[1] is None:
                        errors.append(f'{k}: {ref}: no such item')
                    continue
                # the norm graphs (50_NormGraph_*) are retired: a clause id "R:..." is migrated to "R@<itemSeqId>"
                errors.append(f'{k}: {ref}: an old clause id of the retired norm graphs, migrate it to an item '
                              f'reference <alias>@<agreementItemSeqId>')
            for msg, public in self.copy_hits(c):
                (warnings if public else errors).append(msg)
        errors += self.cycle_errors()
        return errors, warnings

    def copy_hits(self, c):
        """Descriptions are in our own words: flag any run of COPY_WORDS words found verbatim in a cited clause.

        A hit on a licensed standard is an error; on public EU law it is only a warning."""
        words = re.findall(r"[a-z0-9]+", c.get('description', '').lower())
        grams = {' '.join(words[i:i + COPY_WORDS]) for i in range(len(words) - COPY_WORDS + 1)}
        if not grams:
            return []
        out = []
        for ref, _ in c.get('clauses', []):
            t = self.cited_texts(ref)
            if not t:
                continue
            text = ' '.join(re.findall(r"[a-z0-9]+", ' '.join(t[1]).lower()))
            hit = next((g for g in grams if g in text), None)
            if hit:
                out.append((f'{c["key"]}: description copies "{hit}" from {t[0]}', t[3]))
        return out

    def cycle_errors(self):
        state, out = {}, []

        def visit(k, path):
            if state.get(k) == 2:
                return
            if state.get(k) == 1:
                out.append('broader cycle: ' + ' > '.join(path + [k]))
                return
            state[k] = 1
            for b in self.by_key.get(k, {}).get('broader', []):
                visit(b, path + [k])
            state[k] = 2

        for k in self.by_key:
            visit(k, [])
        return out

    def alt_labels(self, c):
        """Other designations of the concept, taken from its defining clauses: the terms (preferred, admitted,
        abbreviation) of every definition the concept cites with role d, except the concept label itself. So the
        concept hazard-zone gets "danger zone" (ISO 12100 3.11 admitted term, Regulation Annex III A(b)) and
        presence-sensing-device gets "sensitive protective equipment" and "SPE"."""
        out = []
        seen = {c['label'].lower()}
        for ref, role in c.get('clauses', []):
            cited = self.cited_texts(ref)
            if role != 'd' or not cited:
                continue
            for t in cited[2]:
                if t and t.lower() not in seen:
                    seen.add(t.lower())
                    out.append(t)
        return out

    # ---------------------------------------------------------------- seed data
    def write_seed(self, path):
        out = []
        counts = dict.fromkeys(('concepts', 'categories', 'rollups', 'featureGroups', 'features', 'groupAppls',
                                'categoryGroupAppls', 'purposes', 'edgesBroader', 'edgesRelated',
                                'parameters'), 0)
        written = set()

        def param(def_id, owner_field, owner_id, sym=None, enum=None, text=None, key='', extra=None):
            pid = short_id('NP', GRAPH_ID, owner_id, def_id, key)
            if pid in written:
                raise ValueError(f'duplicate parameter {def_id} {owner_id} {key}')
            written.add(pid)
            a = [f'parameterId={quoteattr(pid)}', f'parameterDefId={quoteattr(def_id)}', f'graphId={quoteattr(GRAPH_ID)}']
            if owner_field:
                a.append(f'{owner_field}={quoteattr(owner_id)}')
            if sym is not None:
                a.append(f'symbolicValue={quoteattr(sym[:255])}')
            if enum is not None:
                a.append(f'parameterEnumId={quoteattr(enum)}')
            for f, val in (extra or {}).items():
                a.append(f'{f}={quoteattr(val)}')
            counts['parameters'] += 1
            if text is None:
                out.append(f'    <moqui.math.Parameter {" ".join(a)}/>')
            else:
                out.append(f'    <moqui.math.Parameter {" ".join(a)}><textValue>{escape(text)}</textValue></moqui.math.Parameter>')

        def label(s):
            return s if len(s) <= LABEL_MAX else s[:LABEL_MAX - 3] + '...'

        norms = ', '.join(self.data['norms'])
        out.append(f'    <moqui.math.Graph graphId="{GRAPH_ID}" graphTypeEnumId="GtDirectedMulti" name="Compliance vocabulary" '
                   f'description={quoteattr(("Shared vocabulary of " + norms)[:255])} loopsAllowed="N"/>')
        param('CmpVocabularyProposal', None, 'GRAPH', sym=f'{self.data["proposalId"]} v{self.data["version"]}')

        # mantle and moqui-device records first, so the graph parameters can point to existing records
        out.append('')
        out.append('    <!-- ProductCategory tree (scheme product) -->')
        for c in self.concepts:
            if c['scheme'] == 'product':
                out.append(f'    <mantle.product.category.ProductCategory productCategoryId="{record_id(c)}" '
                           f'productCategoryTypeEnumId="CmpPctNormClass" categoryName={quoteattr(c["label"])} '
                           f'description={quoteattr(c["description"])}/>')
                counts['categories'] += 1
        for c in self.concepts:
            if c['scheme'] == 'product':
                for i, b in enumerate(c.get('broader', []), 1):
                    out.append(f'    <mantle.product.category.ProductCategoryRollup productCategoryId="{record_id(c)}" '
                               f'parentProductCategoryId="{record_id(self.by_key[b])}" fromDate="{FROM_DATE}" sequenceNum="{i}"/>')
                    counts['rollups'] += 1
        out.append('')
        out.append('    <!-- ProductFeatureGroup and ProductFeature (schemes featureGroup, feature) -->')
        for c in self.concepts:
            if c['scheme'] == 'featureGroup':
                out.append(f'    <mantle.product.feature.ProductFeatureGroup productFeatureGroupId="{record_id(c)}" '
                           f'description={quoteattr(c["label"])}/>')
                counts['featureGroups'] += 1
        seq = {}
        for c in self.concepts:
            if c['scheme'] == 'feature':
                ftype = self.by_key[c['broader'][0]]['featureType']
                qty = (f' numberSpecified="{c["number"]}"' + (f' numberUomId="{c["uom"]}"' if c.get('uom') else '')) \
                    if 'number' in c else ''
                out.append(f'    <mantle.product.feature.ProductFeature productFeatureId="{record_id(c)}" '
                           f'productFeatureTypeEnumId="{ftype}" description={quoteattr(c["label"][:255])} '
                           f'idCode={quoteattr(c["key"])}{qty}/>')
                counts['features'] += 1
        for c in self.concepts:
            if c['scheme'] == 'feature':
                for g in c['broader']:
                    seq[g] = seq.get(g, 0) + 1
                    out.append(f'    <mantle.product.feature.ProductFeatureGroupAppl productFeatureGroupId="{record_id(self.by_key[g])}" '
                               f'productFeatureId="{record_id(c)}" fromDate="{FROM_DATE}" sequenceNum="{seq[g]}"/>')
                    counts['groupAppls'] += 1
        for c in self.concepts:
            for g in c.get('featureGroups', []):
                out.append(f'    <mantle.product.feature.ProductCategoryFeatGrpAppl productCategoryId="{record_id(c)}" '
                           f'productFeatureGroupId="{record_id(self.by_key[g])}" fromDate="{FROM_DATE}" applTypeEnumId="PfatSelectable"/>')
                counts['categoryGroupAppls'] += 1
        out.append('')
        out.append('    <!-- DevicePurpose values (schemes function, memberRole), parents before children -->')
        done = set()

        def purpose(c):
            if c['key'] in done:
                return
            for b in c.get('broader', []):
                purpose(self.by_key[b])
            done.add(c['key'])
            parent = (c.get('broader') or [None])[0]
            pattr = f' parentEnumId="{record_id(self.by_key[parent])}"' if parent else ''
            out.append(f'    <moqui.basic.Enumeration enumId="{record_id(c)}" enumTypeId="DevicePurpose"{pattr} '
                       f'enumCode={quoteattr(c["key"])} sequenceNum="{len(done)}" description={quoteattr(c["label"])}/>')
            counts['purposes'] += 1

        for c in self.concepts:
            if c['scheme'] in ('function', 'memberRole'):
                purpose(c)

        out.append('')
        out.append('    <!-- Concepts: one GraphVertex each, then edges and parameters -->')
        for c in self.concepts:
            # the hook record realising the concept, so that a DataDocument can start from the hook
            rid = record_id(c)
            hook = f' {HOOK_FIELD[c["scheme"]]}={quoteattr(rid)}' if rid else ''
            out.append(f'    <moqui.math.GraphVertex graphVertexId="{concept_vertex(c["key"])}" graphId="{GRAPH_ID}"{hook} '
                       f'label={quoteattr(label(c["label"]))}/>')
            counts['concepts'] += 1
        edges = set()
        for c in self.concepts:
            v = concept_vertex(c['key'])
            for b in c.get('broader', []):
                edges.add((v, concept_vertex(b), 'CmpGetBroader'))
            for r in c.get('related', []):
                a, z = sorted((v, concept_vertex(r)))
                edges.add((a, z, 'CmpGetRelated'))
        for frm, to, kind in sorted(edges):
            eid = short_id('NE', GRAPH_ID, frm, to, kind)
            lbl = 'broader' if kind == 'CmpGetBroader' else 'related'
            directed = 'Y' if kind == 'CmpGetBroader' else 'N'
            out.append(f'    <moqui.math.GraphEdge graphEdgeId="{eid}" graphId="{GRAPH_ID}" edgeTypeEnumId="{kind}" '
                       f'fromVertexId="{frm}" toVertexId="{to}" isDirected="{directed}" isLoop="N" label="{lbl}"/>')
            counts['edgesBroader' if kind == 'CmpGetBroader' else 'edgesRelated'] += 1
        for c in self.concepts:
            v = concept_vertex(c['key'])
            param('CmpConceptKey', 'graphVertexId', v, sym=c['key'])
            param('CmpConceptScheme', 'graphVertexId', v, enum=SCHEMES[c['scheme']])
            param('CmpConceptLabel', 'graphVertexId', v, text=c['label'])
            param('CmpConceptDescription', 'graphVertexId', v, text=c['description'])
            for alt in self.alt_labels(c):
                param('CmpConceptAltLabel', 'graphVertexId', v, sym=alt, key=alt.lower())
                counts['altLabels'] = counts.get('altLabels', 0) + 1
            for lang, labels in sorted(self.labels.items()):
                names = labels.get(c['key']) or []
                if names:
                    param('CmpConceptLocalLabel', 'graphVertexId', v, sym=lang, text=names[0], key=lang)
                for alt in dict.fromkeys(n for n in names[1:] if n.lower() != names[0].lower()):
                    param('CmpConceptLocalAltLabel', 'graphVertexId', v, sym=alt[:255], text=lang, key=f'{lang}:{alt.lower()}')
            if c.get('note'):
                param('CmpConceptNote', 'graphVertexId', v, text=c['note'])
            for ref, role in c['clauses']:
                ir = self.item_ref(ref)
                if ir:
                    agr = self.agreement[ir[0]]
                    # the item as fields of the Parameter (relationship conceptItem), one copy
                    param('CmpConceptItem', 'graphVertexId', v, enum=ROLES[role], key=f'{agr}:{ir[2]}{role}',
                          extra={'agreementId': agr, 'agreementItemSeqId': ir[2]})
                    counts['itemLinks'] = counts.get('itemLinks', 0) + 1
            rid = record_id(c)
            if rid:
                param('CmpConceptRecord', 'graphVertexId', v, sym=ENTITY[c['scheme']], text=rid)
            if c.get('comparison'):
                param('CmpFeatureComparison', 'graphVertexId', v, sym=c['comparison'])
        # names of the records in other languages (LocalizedEntityField, read by the framework for the user locale)
        loc_field = {'product': ('mantle.product.category.ProductCategory', 'categoryName'),
                     'featureGroup': ('mantle.product.feature.ProductFeatureGroup', 'description'),
                     'feature': ('mantle.product.feature.ProductFeature', 'description'),
                     'function': ('moqui.basic.Enumeration', 'description'),
                     'memberRole': ('moqui.basic.Enumeration', 'description')}
        out.append('')
        out.append('    <!-- Names of the records in other languages (LABELS-<lang>.json) -->')
        for lang, labels in sorted(self.labels.items()):
            for c in self.concepts:
                rid, lf = record_id(c), loc_field.get(c['scheme'])
                if rid and lf and labels.get(c['key']):
                    out.append(f'    <moqui.basic.LocalizedEntityField entityName="{lf[0]}" fieldName="{lf[1]}" '
                               f'pkValue="{rid}" locale="{lang}" localized={quoteattr(labels[c["key"]][0][:255])}/>')
                    counts['localizedNames'] = counts.get('localizedNames', 0) + 1
        header = ('<?xml version="1.0" encoding="UTF-8"?>\n'
                  f'<!-- Generated by vocab.py (skill moqui-norm-hooks) from {self.path.name}. Do not edit by hand: '
                  'regenerate.\n     Descriptions are written for this knowledge base; they do not reproduce the text of the norms. -->\n'
                  '<entity-facade-xml type="seed">\n')
        Path(path).write_text(header + '\n'.join(out) + '\n</entity-facade-xml>\n', encoding='utf-8')
        return counts


def main(argv=None):
    import argparse
    ap = argparse.ArgumentParser(description='Validate a vocabulary proposal and write its seed data.')
    ap.add_argument('proposal', nargs='?', default=str(paths.VOCABULARY / 'VOCAB-BASE.json'))
    ap.add_argument('--extension', action='append', default=None,
                    help='vocabulary extension files (default: data/norms/vocabulary/HOOKS-*.json, in name order)')
    ap.add_argument('--ir', default=str(paths.IR))
    ap.add_argument('--out', default=str(paths.DATA / '60_CmpVocabulary.xml'))
    ap.add_argument('--check', action='store_true', help='validate only')
    a = ap.parse_args(argv)
    exts = a.extension if a.extension is not None else sorted(str(p) for p in paths.VOCABULARY.glob('HOOKS-*.json'))
    v = Vocabulary(a.proposal, a.ir, exts)
    if exts:
        print('extensions:', ', '.join(Path(e).name for e in exts))
    errors, warnings = v.validate()
    for w in warnings:
        print('WARNING', w)
    for e in errors:
        print('ERROR', e)
    if errors:
        print(f'{len(errors)} errors')
        return 1
    schemes = {}
    for c in v.concepts:
        schemes[c['scheme']] = schemes.get(c['scheme'], 0) + 1
    print('concepts by scheme:', schemes)
    if not a.check:
        print('written', a.out, v.write_seed(a.out))
    return 0


if __name__ == '__main__':
    sys.exit(main())
