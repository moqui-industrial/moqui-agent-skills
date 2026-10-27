"""Clause-level intermediate representation (IR) of a norm.

One IR node is one citable partition of a norm: a chapter, article, paragraph, point, definition, recital, annex,
annex section or clause of a standard. Every node keeps only its own text; the text of its children stays in the
children. Node ids are stable: they are built from the partition path, never from the position in a file.
"""
import hashlib
import json
import re
from dataclasses import asdict, dataclass, field
from typing import Dict, List, Optional

KINDS = {
    'document', 'preamble', 'recital', 'chapter', 'section', 'article', 'paragraph', 'point', 'definition',
    'annex', 'annexSection', 'clause', 'note', 'table', 'figure', 'bibliography',
    'flowStep', 'flowDecision', 'flowTerminal',   # parts of a figure modelled as a flow (config/figures)
}
TERM_STATUS = {'preferred', 'admitted', 'abbreviation'}


@dataclass
class Reference:
    raw: str                      # text as written, e.g. "Article 6(1)" or "ISO 12100:2010, 3.30"
    targetNormId: Optional[str]   # normId of the target, or None when not a known norm
    targetNodeId: Optional[str]   # resolved node id inside the target, or None
    external: Optional[str] = None  # normalized designator of a norm outside the knowledge base


@dataclass
class Node:
    nodeId: str
    normId: str
    parentId: Optional[str]
    kind: str
    seq: int
    number: Optional[str] = None
    title: Dict[str, str] = field(default_factory=dict)   # language -> title
    text: Dict[str, str] = field(default_factory=dict)    # language -> own text
    term: Dict[str, str] = field(default_factory=dict)    # language -> defined term (definitions only)
    # language -> other designations of the defined concept: [{'term': 'SPE', 'status': 'abbreviation'}]
    altTerms: Dict[str, List[Dict[str, str]]] = field(default_factory=dict)
    # figure flows only: [{'to': nodeId, 'condition': 'YES' | 'NO' | None, 'label': text | None}]
    flows: List[Dict[str, Optional[str]]] = field(default_factory=list)
    attrs: Dict[str, str] = field(default_factory=dict)  # extra metadata: figure image, flow groups
    references: List[Reference] = field(default_factory=list)
    source: Dict[str, str] = field(default_factory=dict)  # file, element id, page

    def to_json(self):
        d = asdict(self)
        return json.dumps(d, ensure_ascii=False, sort_keys=True)


def node_id(norm_id, path):
    return f'{norm_id}:{path}'


def vertex_id(nid):
    """Graph vertex id: stable, at most 40 characters (Moqui type id)."""
    return 'NV' + hashlib.sha1(nid.encode('utf-8')).hexdigest()[:30]


def graph_id(norm_id):
    return ('NG_' + norm_id.replace('-', ''))[:40]


def clean_text(s):
    s = s.replace(' ', ' ').replace('­', '')
    s = re.sub(r'[ \t]+', ' ', s)
    s = re.sub(r' *\n *', '\n', s)
    s = re.sub(r'\n{3,}', '\n\n', s)
    return s.strip()


def validate(nodes):
    """Structural checks that must hold for every norm. Returns a list of error strings."""
    errors = []
    ids = {}
    for n in nodes:
        if n.nodeId in ids:
            errors.append(f'duplicate id {n.nodeId}')
        ids[n.nodeId] = n
        if n.kind not in KINDS:
            errors.append(f'{n.nodeId}: unknown kind {n.kind}')
    roots = [n for n in nodes if n.parentId is None]
    if len(roots) != 1:
        errors.append(f'expected one root, found {len(roots)}')
    for n in nodes:
        if n.parentId is not None and n.parentId not in ids:
            errors.append(f'{n.nodeId}: parent {n.parentId} missing')
        for r in n.references:
            if r.targetNodeId is not None and r.targetNormId == n.normId and r.targetNodeId not in ids:
                errors.append(f'{n.nodeId}: reference {r.raw} to missing {r.targetNodeId}')
        for f in n.flows:
            if f['to'] not in ids:
                errors.append(f'{n.nodeId}: flow to missing {f["to"]}')
        for lg, alts in n.altTerms.items():
            for a in alts:
                if a.get('status') not in TERM_STATUS:
                    errors.append(f'{n.nodeId}: term status {a.get("status")}')
    return errors


def write_jsonl(nodes, path):
    with open(path, 'w', encoding='utf-8') as f:
        for n in nodes:
            f.write(n.to_json() + '\n')


def read_jsonl(path):
    nodes = []
    with open(path, encoding='utf-8') as f:
        for line in f:
            d = json.loads(line)
            d['references'] = [Reference(**r) for r in d.get('references', [])]
            nodes.append(Node(**d))
    return nodes
