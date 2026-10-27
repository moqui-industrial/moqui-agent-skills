#!/usr/bin/env python3
"""Build the intermediate representation of one norm (build/norm-kb/ir/<normId>.jsonl of mantle-compliance): read the source, extract references,
validate. The per-norm graph seeds (50_NormGraph_*) are retired: the norms are Agreement seeds (build_agreement.py)
and their associations one graph (moqui-norm-associations assoc.py, 70_CmpAssociations.xml).

    python3 build_norm.py ISO-12100-2010            # writes build/norm-kb/ir/<normId>.jsonl
"""
import argparse
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

from normkb import paths                         # noqa: E402
from normkb.figures import add_figures          # noqa: E402
from normkb.formex import FormexReader          # noqa: E402
from normkb.ir import validate, write_jsonl     # noqa: E402
from normkb.pdfstd import PdfStandardReader, std_references   # noqa: E402
from normkb.refs import KNOWN, eu_references, unresolved      # noqa: E402


def source_text_length(norm, root):
    """Characters of the source text (whitespace collapsed), the reference for the coverage check."""
    import glob
    import re
    import subprocess
    import xml.etree.ElementTree as ET
    if norm['reader'] == 'formex':
        total = 0
        for lg, d in norm['dirs'].items():
            for f in glob.glob(os.path.join(root, d, '*.xml')):
                if '.doc.' not in f and '.toc.' not in f:
                    total += len(re.sub(r'\s+', ' ', ' '.join(ET.parse(f).getroot().itertext())))
            return total
    out = subprocess.run(['pdftotext', os.path.join(root, norm['file']), '-'], capture_output=True, text=True).stdout
    return len(re.sub(r'\s+', ' ', out))


def coverage_errors(nodes, lang, source_len):
    """The own texts of the nodes must cover the source without duplicating it, and no own text may contain the
    heading of another node (a sign that a heading was missed and two partitions were merged)."""
    import re
    total = sum(len(re.sub(r'\s+', ' ', n.text.get(lang) or '')) for n in nodes)
    errors = []
    ratio = total / source_len if source_len else 0
    print(f'coverage: node texts {total} chars, source {source_len} chars, ratio {ratio:.2f}', file=sys.stderr)
    if ratio > 1.05:
        errors.append(f'node texts are {ratio:.2f} times the source: text is duplicated')
    if ratio < 0.5:
        errors.append(f'node texts are only {ratio:.2f} of the source: text is lost')
    return errors


def content_errors(nodes):
    """Checks on what was extracted, not only on how much (WP1.3): a citation of a norm of the knowledge base must
    not be left as an external reference."""
    errors = []
    for n in nodes:
        for r in n.references:
            if r.external and any(p.search(r.external) for p, _ in KNOWN):
                errors.append(f'{n.nodeId}: "{r.raw}" cites a norm of the knowledge base but is external')
    return errors


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('normId')
    ap.add_argument('--config', default=str(paths.CONFIG))
    args = ap.parse_args()
    cfg = json.load(open(args.config, encoding='utf-8'))
    norm = next(n for n in cfg['norms'] if n['normId'] == args.normId)
    root = cfg['sourceRoot']
    if norm['reader'] == 'formex':
        reader = FormexReader(norm['normId'], {lg: os.path.join(root, d) for lg, d in norm['dirs'].items()})
        problems = reader.check_parallel()
        if problems:
            sys.exit(f'language versions differ: {problems}')
        nodes = eu_references(reader.read())
        report = {'unresolved': unresolved(nodes)}
        languages = tuple(norm['dirs'].keys())
        source = ', '.join(norm['dirs'].values()) + ' (Formex 4)'
    else:
        reader = PdfStandardReader(norm['normId'], os.path.join(root, norm['file']), language=norm['language'],
                                   boilerplate=norm.get('boilerplate', []), title=norm['title'],
                                   bilingual=norm.get('bilingual', True), definitions_clause=norm.get('definitionsClause'),
                                   paragraph_gaps=norm.get('paragraphGaps', False), line_fixes=norm.get('lineFixes', []))
        nodes = std_references(reader.read(), KNOWN, norm['language'])
        nodes = add_figures(nodes, paths.FIGURES / f'{norm["normId"]}.json', norm['language'])
        report = reader.report
        languages = (norm['language'],)
        source = norm['file'] + ' (pdftotext -layout)'
    src_len = report.get('sourceChars') if isinstance(report, dict) and report.get('sourceChars') else \
        source_text_length(norm, root)
    errors = validate(nodes) + coverage_errors(nodes, languages[0], src_len) + content_errors(nodes)
    if errors:
        sys.exit('IR errors:\n' + '\n'.join(errors[:50]))
    os.makedirs(paths.IR, exist_ok=True)
    write_jsonl(nodes, paths.IR / f'{norm["normId"]}.jsonl')
    kinds = {}
    for n in nodes:
        kinds[n.kind] = kinds.get(n.kind, 0) + 1
    report = dict(report) if isinstance(report, dict) else {'report': report}
    report['otherDesignations'] = {n.number: n.altTerms for n in nodes if n.altTerms}
    print(json.dumps({'normId': norm['normId'], 'nodes': len(nodes), 'kinds': kinds, 'report': report},
                     indent=1, default=str))


if __name__ == '__main__':
    main()
