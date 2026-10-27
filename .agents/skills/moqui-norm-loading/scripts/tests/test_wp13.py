"""Checks added with WP1.3. Run from the scripts directory of moqui-norm-loading: python3 -m unittest discover tests"""
import os
import sys
import unittest

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, HERE)

from normkb import paths                         # noqa: E402

from normkb.ir import Node, read_jsonl                 # noqa: E402
from normkb.pdfstd import CAPTION, split_designations  # noqa: E402
from normkb.refs import KNOWN                          # noqa: E402

IR = str(paths.IR)


def definition(text):
    n = Node(nodeId='X:DEF_1', normId='X', parentId=None, kind='definition', seq=1, number='1')
    n.text['en'] = text
    return n


class DesignationTest(unittest.TestCase):
    def test_admitted_and_abbreviation(self):
        a = definition('danger zone\nany space within and/or around machinery')
        b = definition('SPE\nequipment for detecting persons')
        split_designations([a, b], 'en')
        self.assertEqual(a.altTerms['en'], [{'term': 'danger zone', 'status': 'admitted'}])
        self.assertEqual(a.text['en'], 'any space within and/or around machinery')
        self.assertEqual(b.altTerms['en'][0]['status'], 'abbreviation')

    def test_short_definition_is_not_a_designation(self):
        for text in ('potential source of harm\nNOTE 1 The term can be qualified',
                     'guard or protective device',
                     'contact of persons with live parts\n[IEV 826-12-03]'):
            n = definition(text)
            split_designations([n], 'en')
            self.assertEqual(n.altTerms, {}, text)
            self.assertEqual(n.text['en'], text)

    @unittest.skipUnless(os.path.exists(os.path.join(IR, 'ISO-12100-2010.jsonl')), 'IR not built')
    def test_base_norms_have_exactly_the_known_designations(self):
        found = set()
        for norm in ('ISO-12100-2010', 'IEC-60204-1-2006'):
            p = os.path.join(IR, f'{norm}.jsonl')
            if os.path.exists(p):
                for n in read_jsonl(p):
                    for a in n.altTerms.get('en', []):
                        found.add((norm, n.number, a['term']))
        expected = {('ISO-12100-2010', '3.1', 'machine'), ('ISO-12100-2010', '3.11', 'danger zone'),
                    ('ISO-12100-2010', '3.27.6', 'control guard'), ('ISO-12100-2010', '3.28.1', 'interlock'),
                    ('ISO-12100-2010', '3.28.5', 'SPE'), ('ISO-12100-2010', '3.28.6', 'AOPD'),
                    ('ISO-12100-2010', '3.31', 'unintended start-up'),
                    ('ISO-12100-2010', '3.40', 'emergency stop function')}
        if os.path.exists(os.path.join(IR, 'IEC-60204-1-2006.jsonl')):
            expected |= {('IEC-60204-1-2006', '3.35', 'machine'), ('IEC-60204-1-2006', '3.37', 'N')}
        self.assertEqual(found, expected)


class CaptionAndReferenceTest(unittest.TestCase):
    def test_captions(self):
        self.assertTrue(CAPTION.match('    Figure 1 — Schematic representation of risk reduction process'))
        self.assertTrue(CAPTION.match('  Table D.2 – Derating factors'))
        self.assertTrue(CAPTION.match('Table B.1'))
        self.assertFalse(CAPTION.match('Table B.1.3'))           # index entry of ISO 12100 Annex C
        self.assertFalse(CAPTION.match('Table B.2 is a subset of Table B.1'))

    def test_bare_designator_resolves_to_the_loaded_part(self):
        def known(t):
            return next((n for p, n in KNOWN if p.search(t)), None)
        self.assertEqual(known('IEC 60204'), 'IEC-60204-1-2006')
        self.assertEqual(known('EN 60204-1'), 'IEC-60204-1-2006')
        self.assertIsNone(known('IEC 60204-32'))
        self.assertIsNone(known('ISO 13849-2'))


if __name__ == '__main__':
    unittest.main()
