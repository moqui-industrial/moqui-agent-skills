"""Tests of the vocabulary converter. Run from the scripts directory of moqui-norm-hooks: python3 -m unittest discover tests"""
import json
import re
import sys
import tempfile
import unittest
import xml.dom.minidom
from pathlib import Path

HERE = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(HERE))
import vocab  # noqa: E402

PROPOSAL = vocab.paths.VOCABULARY / 'VOCAB-BASE.json'
IR = vocab.paths.IR
ITEMS = vocab.paths.ITEMS


def proposal_with(concepts, norms=('EU-REG-2023-1230',)):
    d = {'proposalId': 'T', 'version': 1, 'norms': list(norms), 'normAliases': {'R': 'EU-REG-2023-1230'}, 'concepts': concepts}
    f = tempfile.NamedTemporaryFile('w', suffix='.json', delete=False)
    json.dump(d, f)
    f.close()
    return f.name


def concept(key, scheme='product', **kw):
    c = {'key': key, 'scheme': scheme, 'label': key, 'description': 'own words', 'clauses': [['R:ART_3.PT_1', 'd']]}
    c.update(kw)
    return c


class ValidationTest(unittest.TestCase):
    def errors(self, concepts, ir=IR):
        return vocab.Vocabulary(proposal_with(concepts), ir).validate()[0]

    def test_base_proposal_is_valid(self):
        errors, _ = vocab.Vocabulary(PROPOSAL, IR).validate()
        self.assertEqual(errors, [])

    def test_unknown_broader_and_cycle(self):
        e = self.errors([concept('a', broader=['b']), concept('b', broader=['a']), concept('c', broader=['zz'])])
        self.assertTrue(any('broader cycle' in x for x in e))
        self.assertTrue(any('broader zz not defined' in x for x in e))

    def test_scheme_rules(self):
        e = self.errors([concept('g', 'featureGroup', featureType='CmpPftEnergySource'),
                         concept('f', 'feature'), concept('p', broader=['g']),
                         concept('fn-a', 'function'), concept('fn-b', 'function'),
                         concept('fn-c', 'function', broader=['fn-a', 'fn-b'])])
        self.assertTrue(any(x.startswith('f: a feature needs') for x in e))
        self.assertTrue(any(x.startswith('p: broader g has scheme featureGroup') for x in e))
        self.assertTrue(any(x.startswith('fn-c: an Enumeration has one parent') for x in e))

    @unittest.skipUnless((ITEMS / 'EU-REG-2023-1230.jsonl').exists(), 'items of the Regulation not built')
    def test_item_must_exist(self):
        e = self.errors([concept('a', clauses=[['R@ART999', 'd']]), concept('b', clauses=[['R:ART_3', 'd']])])
        self.assertTrue(any('a: R@ART999: no such item' in x for x in e))
        # clause ids of the retired norm graphs are refused
        self.assertTrue(any(x.startswith('b: R:ART_3: an old clause id') for x in e))

    @unittest.skipUnless((ITEMS / 'EU-REG-2023-1230.jsonl').exists(), 'items of the Regulation not built')
    def test_copy_of_public_text_is_a_warning(self):
        v = vocab.Vocabulary(proposal_with([concept('a', clauses=[['R@ART3.pt20', 'd']],
                                                     description='any person placing a product from a third country on the union market')]), IR)
        errors, warnings = v.validate()
        self.assertEqual(errors, [])
        self.assertTrue(any('copies' in w for w in warnings))


class SeedTest(unittest.TestCase):
    def test_seed_is_well_formed_and_stable(self):
        with tempfile.TemporaryDirectory() as d:
            a, b = Path(d) / 'a.xml', Path(d) / 'b.xml'
            v = vocab.Vocabulary(PROPOSAL, IR)
            self.assertEqual(v.validate()[0], [])
            counts = v.write_seed(a)
            v2 = vocab.Vocabulary(PROPOSAL, IR)
            v2.validate()
            v2.write_seed(b)
            self.assertEqual(a.read_text(), b.read_text())
            xml.dom.minidom.parse(str(a))
            text = a.read_text()
            self.assertNotIn(' -- ', text.split('<entity-facade-xml')[0])
            self.assertEqual(counts['concepts'], len(v.concepts))
            # every id fits the Moqui id type
            for rid in re.findall(r'(?:productCategoryId|productFeatureId|productFeatureGroupId|enumId|graphVertexId|parameterId|graphEdgeId)="([^"]+)"', text):
                self.assertLessEqual(len(rid), vocab.ID_MAX, rid)

    def test_enumeration_parents_come_first(self):
        with tempfile.TemporaryDirectory() as d:
            p = Path(d) / 's.xml'
            v = vocab.Vocabulary(PROPOSAL, IR)
            v.validate()
            v.write_seed(p)
            seen = set()
            for enum_id, parent in re.findall(r'<moqui\.basic\.Enumeration enumId="([^"]+)" enumTypeId="DevicePurpose"(?: parentEnumId="([^"]+)")?', p.read_text()):
                if parent:
                    self.assertIn(parent, seen, enum_id)
                seen.add(enum_id)


if __name__ == '__main__':
    unittest.main()
