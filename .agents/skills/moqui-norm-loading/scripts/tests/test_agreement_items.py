"""Checks of the Agreement items (PLAN-NORMS-AGREEMENT.md WPA.2, WPB.1). Run from the scripts directory of moqui-norm-loading:
python3 -m unittest discover tests"""
import os
import sys
import unittest

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, HERE)

from normkb import paths                         # noqa: E402

from normkb.items import Item, check_items, read_items_jsonl, stub_id   # noqa: E402

ITEMS = str(paths.ITEMS / 'EU-REG-2023-1230.jsonl')


def item(sid, parent, typ='AitParagraph', seq=1, text='x'):
    return Item(seqId=sid, parentSeqId=parent, type=typ, sequence=seq, text={'en': text})


class CheckItemsTest(unittest.TestCase):
    def test_valid_tree(self):
        items = [item('ART1', None, 'AitArticle', text=''), item('ART1.p1', 'ART1'), item('ART1.p2', 'ART1', seq=2)]
        self.assertEqual(check_items(items, ['en']), [])

    def test_errors(self):
        items = [item('ART1', None, 'AitArticle'), item('ART1.p1', 'ART9'), item('ART1.p1', 'ART1'),
                 item('X' * 41, None), item('ART2', None, 'AitWhatever'), item('ART3', None, text='')]
        errors = ' '.join(check_items(items, ['en']))
        for expected in ('parent ART9 missing', 'duplicate id ART1.p1', 'longer than 40', 'unknown type',
                         'empty leaf'):
            self.assertIn(expected, errors)

    def test_stub_ids(self):
        self.assertEqual(stub_id('Directive 2006/42/EC'), 'STUB-EU-DIR-2006-42-EC')
        self.assertEqual(stub_id('Regulation (EU) No 1025/2012'), 'STUB-EU-REG-1025-2012')
        self.assertEqual(stub_id('ISO 14118:2000, Clause 5'), 'STUB-ISO-14118')


@unittest.skipUnless(os.path.exists(ITEMS), 'items not built (python3 build_agreement.py EU-REG-2023-1230)')
class RegulationTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.items = read_items_jsonl(ITEMS)
        cls.by_id = {i.seqId: i for i in cls.items}

    def children(self, sid):
        return [i.seqId for i in self.items if i.parentSeqId == sid]

    def test_annex_iii_1_2_1_has_three_lists(self):
        self.assertEqual(self.children('ANXIII.B.1.2.1'), [f'ANXIII.B.1.2.1.p{k}' for k in range(1, 6)])
        self.assertEqual(len(self.children('ANXIII.B.1.2.1.p2')), 6)       # a-f
        self.assertEqual(len(self.children('ANXIII.B.1.2.1.p3')), 3)       # a-c
        self.assertEqual(len(self.children('ANXIII.B.1.2.1.p4')), 8)       # a-h
        self.assertTrue(self.by_id['ANXIII.B.1.2.1.p4.pta'].text['en'].startswith('the machinery or related product '
                                                                                  'shall not start unexpectedly'))

    def test_list_in_a_paragraph_belongs_to_the_paragraph_before(self):
        # general principle 1: "... the manufacturer shall:" then (a)-(e), no empty paragraph in between
        p2 = self.by_id['ANXIII.B.pt1.p2']
        self.assertTrue(p2.text['en'].rstrip().endswith(':'))
        self.assertEqual(len(self.children('ANXIII.B.pt1.p2')), 5)

    def test_definitions_in_both_languages(self):
        self.assertEqual(self.by_id['ART3.pt3'].term, {'en': 'safety component', 'it': 'componente di sicurezza'})
        self.assertEqual(self.by_id['ANXIII.A.ptb'].term, {'en': 'danger zone', 'it': 'zona pericolosa'})
        self.assertEqual(self.by_id['ANXIII.A.pte'].term.get('it'), 'rischio')

    def test_references(self):
        refs = {(i.seqId, r.raw): r for i in self.items for r in i.refs}
        self.assertEqual(refs[('ART47.6', 'Article 6(11)')].toSeqId, 'ART6.11')
        self.assertEqual(refs[('PRE', 'Article 114 of the Treaty on the Functioning of the European Union')].external,
                         'the Treaty on the Functioning of the European Union')
        self.assertFalse([k for k, r in refs.items() if r.toNormId == 'EU-REG-2023-1230' and not r.toSeqId])
        # an annex "of" or "to" another act is that act's annex; the act cited by its own name is itself
        self.assertEqual(refs[('REC54', 'Annex IV of Directive 2006/42/EC')].external, 'Directive 2006/42/EC')
        self.assertEqual(refs[('ANXV.B.pt5', 'Annex III')].toSeqId, 'ANXIII')


CRA_ITEMS = str(paths.ITEMS / 'EU-REG-2024-2847.jsonl')


@unittest.skipUnless(os.path.exists(CRA_ITEMS), 'items not built (python3 build_agreement.py EU-REG-2024-2847)')
class CyberResilienceActTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.items = read_items_jsonl(CRA_ITEMS)
        cls.by_id = {i.seqId: i for i in cls.items}
        cls.refs = {(i.seqId, r.raw): r for i in cls.items for r in i.refs}

    def test_parts_and_classes_named_as_printed(self):
        self.assertEqual(self.by_id['ANXI.I'].type, 'AitAnnexPart')
        self.assertEqual(self.by_id['ANXI.II.pt8'].number, '8')
        self.assertEqual(self.by_id['ANXIII.clII'].title['it'], 'Classe II')

    def test_references_to_parts_and_points_of_annexes(self):
        self.assertEqual(self.refs[('ART13.3', 'Part I, point (2), of Annex I')].toSeqId, 'ANXI.I.pt2')
        self.assertEqual(self.refs[('ANXII.pt8.spe', 'Part I, point (2)(c), of Annex I')].toSeqId, 'ANXI.I.pt2.spc')
        self.assertEqual(self.refs[('ART3.pt20', 'Part II of Annex I')].toSeqId, 'ANXI.II')
        self.assertNotIn(('ART3.pt20', 'Annex I'), self.refs)

    def test_references_to_other_acts(self):
        self.assertEqual(self.refs[('REC123', 'Article 218 TFEU')].external, 'TFEU')
        r = self.refs[('REC53', 'point 1.1.9 of Annex III of Regulation (EU) 2023/1230')]
        self.assertEqual((r.toNormId, r.toSeqId), ('EU-REG-2023-1230', 'ANXIII.B.1.1.9'))
        self.assertFalse([k for k, r in self.refs.items() if r.toNormId == 'EU-REG-2024-2847' and not r.toSeqId])


if __name__ == '__main__':
    unittest.main()
