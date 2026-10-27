"""Figures modelled by hand: flowcharts and block diagrams added to the IR as nodes inside their figure node.

A PDF reader only sees the words of a drawing, so the structure of a figure (boxes, decisions, YES/NO branches)
is written once in config/figures/<normId>.json, from the rendered page, in our own words. This module turns it
into IR nodes (kinds flowStep, flowDecision, flowTerminal) with their flows and references to the cited clauses.
"""
import json
import os
import re

from .ir import Node, Reference

CONDITIONS = {'YES', 'NO', 'SÌ', 'Sì', 'No'}


def add_figures(nodes, spec_path, lang='en'):
    """Append the nodes of every figure of the spec. The figure node (FIG_n) must exist: its caption was found by
    the reader. Returns the nodes; raises ValueError on an unknown figure, node, flow or clause reference."""
    if not os.path.exists(spec_path):
        return nodes
    spec = json.load(open(spec_path, encoding='utf-8'))
    by_id = {n.nodeId: n for n in nodes}
    by_number = {}
    for n in nodes:
        if n.number and '~' not in n.nodeId and n.kind in ('clause', 'definition', 'annex'):
            by_number.setdefault(n.number, n.nodeId)
    norm = spec['normId']
    for fig in spec['figures']:
        fid = f'{norm}:{fig["figure"]}'
        if fid not in by_id:
            raise ValueError(f'figure {fid} not found by the reader (missing caption?)')
        fnode = by_id[fid]
        if fig.get('image'):
            fnode.attrs['image'] = fig['image']
        for k, v in fig.get('attrs', {}).items():
            fnode.attrs[k] = v
        for k, v in fig.get('groups', {}).items():
            fnode.attrs['group:' + k] = v
        ids = {}
        for item in fig['nodes']:
            ids[item['id']] = f'{fid}.N_{item["id"]}'
        for seq, item in enumerate(fig['nodes'], 1):
            parent = ids[item['parent']] if item.get('parent') else fid
            n = Node(nodeId=ids[item['id']], normId=norm, parentId=parent, kind=item['kind'],
                     seq=len(nodes) + 1, number=None)
            n.title[lang] = item['label']
            n.text[lang] = ''
            n.source = dict(fnode.source)
            n.attrs['flowKey'] = item['id']
            if item.get('groups'):
                n.attrs['groups'] = ','.join(item['groups'])
            for k, v in item.get('attrs', {}).items():
                n.attrs[k] = v
            for ref in item.get('refs', []):
                num = re.sub(r'^(Clause|Annex)\s+', '', ref)
                target = by_number.get(num)
                if not target:
                    raise ValueError(f'{n.nodeId}: cited {ref} not found')
                n.references.append(Reference(raw=ref, targetNormId=norm, targetNodeId=target))
            nodes.append(n)
            by_id[n.nodeId] = n
        for flow in fig['flows']:
            # [from, to] or [from, to, label or condition]
            frm, to, cond = (list(flow) + [None])[:3]
            if frm not in ids or to not in ids:
                raise ValueError(f'{fid}: flow {frm} -> {to} uses an unknown node')
            by_id[ids[frm]].flows.append({'to': ids[to], 'condition': cond if cond in CONDITIONS else None,
                                          'label': None if cond in CONDITIONS else cond})
    return nodes
