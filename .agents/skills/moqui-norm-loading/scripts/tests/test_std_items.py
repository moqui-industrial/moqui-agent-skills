"""Items of standards read from PDF (std_items, pdf_tables, untitled clauses of pdfstd).
Run from the scripts directory of moqui-norm-loading: python3 -m unittest discover tests

The rules are tested on made-up text; the checks on the licensed PDF run only where the PDF is present."""
import json
import os
import sys
import unittest

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, HERE)

from normkb import paths                         # noqa: E402

from normkb.ir import Node                                                  # noqa: E402
from normkb.pdf_tables import row_text                                      # noqa: E402
from normkb.std_items import CAPTION, blocks, check_partition, index_refs, nodes_to_items, split_clause  # noqa: E402


def node(path, kind, number, text='', title=''):
    n = Node(nodeId=f'X:{path}', normId='X', parentId=None, kind=kind, seq=1, number=number)
    n.text['en'] = text
    n.title['en'] = title
    return n


class SplitClauseTest(unittest.TestCase):
    def test_single_paragraph_keeps_text(self):
        own, children = split_clause(node('CL_1', 'clause', '1', 'The machine shall stop.'), 'en', '1')
        self.assertEqual(own, 'The machine shall stop.')
        self.assertEqual(children, [])

    def test_list_belongs_to_introducing_paragraph(self):
        text = ('The designer shall consider:\n\na) the limits of the machine;\n\nb) the hazards.\n\n'
                'A second paragraph.')
        own, children = split_clause(node('CL_2', 'clause', '2', text), 'en', '2')
        got = [(c.seqId, c.parentSeqId, c.type) for c in children]
        self.assertEqual(own, '')
        self.assertEqual(got, [('2.p1', '2', 'AitParagraph'), ('2.p1.pta', '2.p1', 'AitPoint'),
                               ('2.p1.ptb', '2.p1', 'AitPoint'), ('2.p2', '2', 'AitParagraph')])

    def test_heading_point_owns_following_paragraphs(self):
        text = ('Risk elements:\n\na) Severity of harm\n\nThe severity depends on the harm.\n\n'
                'b) Probability of harm\n\nThe probability depends on exposure.')
        own, children = split_clause(node('CL_3', 'clause', '3', text), 'en', '3')
        paras = [c for c in children if c.type == 'AitParagraph' and c.parentSeqId != '3']
        self.assertEqual(sorted(p.parentSeqId for p in paras), ['3.p1.pta', '3.p1.ptb'])

    def test_note_inside_open_list_goes_to_point(self):
        text = 'Measures:\n\na) guards;\n\nNOTE Guards can be fixed.\n\nb) devices.'
        own, children = split_clause(node('CL_4', 'clause', '4', text), 'en', '4')
        note = next(c for c in children if c.type == 'AitNote')
        self.assertEqual(note.parentSeqId, '4.pta')


class LayoutRulesTest(unittest.TestCase):
    def test_note_inside_dash_list_goes_to_item(self):
        text = 'It applies to machines that:\n\n– are sewing machines;\n\nNOTE 7 For sewing machines, see X.\n\n– are hoisting machines.'
        own, children = split_clause(node('CL_1', 'clause', '1', text), 'en', '1')
        note = next(c for c in children if c.type == 'AitNote')
        self.assertEqual(note.parentSeqId, '1.li1')

    def test_note_introduces_list(self):
        text = 'Definition text\n\nNOTE 2 The hazard envisaged in this definition:\n\n– either is present;\n\n– or appears.'
        own, children = split_clause(node('CL_3', 'clause', '3.28', text), 'en', '3.28')
        self.assertEqual([c.parentSeqId for c in children if c.type == 'AitPoint'], ['3.28.n1', '3.28.n1'])

    def test_numbered_sections_of_a_form(self):
        text = ('Name of user\n\n1. Special conditions\n\na) Open air? Yes No\n\nb) Explosive? Yes No\n\n'
                '2. Electrical supplies\n\na) Voltage fluctuations')
        own, children = split_clause(node('ANX_B', 'annex', 'B', text), 'en', 'ANXB')
        ids = [c.seqId for c in children]
        self.assertIn('ANXB.pt1.pta', ids)
        self.assertIn('ANXB.pt2.pta', ids)
        self.assertEqual(len(ids), len(set(ids)))

    def test_next_letter_line_is_next_point(self):
        bl = blocks('d) Can the machine present special hazards when Yes/No\nproducing materials?\ne) Is it for mines? Yes No')
        self.assertEqual(len(bl), 2)
        self.assertTrue(bl[1].startswith('e)'))

    def test_clause_colon_entries(self):
        bl = blocks('The following differences exist:\n5.1: Exception is not allowed (USA).\n'
                    '6.3.3 b), 13.4.5 b): TT systems are not allowed\n(USA).\n7.2.3: Disconnection is mandatory.')
        self.assertEqual(len(bl), 4)


class ItalianEditionRulesTest(unittest.TestCase):
    def test_caption_variants(self):
        for c in ('Tabella 8 –Diversi livelli', 'Figura A.2 –- Esempio proforma', 'Figura H.4-Correlazione tra',
                  'Figura I.2 (2 di 2)', 'Tabella D.1 - Stime (1 di 2)'):
            self.assertTrue(CAPTION.match(c), c)

    def test_lettered_list_inside_note_stays(self):
        bl = blocks('NOTA 4 Tenendo conto di fattori tra cui:\na) la responsabilità;\nh) la tecnologia;\ni) la sicurezza;\nj) il quadro normativo.')
        self.assertEqual(len(bl), 1)

    def test_note_after_paragraph_dashes_keeps_order(self):
        text = ('Si tiene conto di:\n\na) Prevedibilità del comportamento.\n\n– prima osservazione;\n\n– seconda osservazione.\n\n'
                'NOTA 1 Nota sulla prevedibilità.\n\nb) Comportamento umano')
        own, children = split_clause(node('CL_A', 'clause', 'A.2', text, ''), 'en', 'A.2')
        note = next(c for c in children if c.type == 'AitNote')
        dash = next(c for c in children if c.seqId.endswith('.li2'))
        self.assertEqual(note.parentSeqId, dash.parentSeqId)


class EditionTest(unittest.TestCase):
    def test_dated_citations(self):
        from normkb.refs import known_norm
        self.assertEqual(known_norm('IEC 60204-1:2005'), 'IEC-60204-1-2006')
        self.assertEqual(known_norm('ISO 13849-1'), 'ISO-13849-1-2015')
        self.assertIsNone(known_norm('ISO 13849-1:2006'))
        self.assertIsNone(known_norm('ISO 12100-1:2003'))
        self.assertIsNone(known_norm('ISO 12100-2'))
        self.assertEqual(known_norm('EN ISO 12100'), 'ISO-12100-2010')


class CaptionTest(unittest.TestCase):
    def test_captions(self):
        self.assertTrue(CAPTION.match('Table B.1'))
        self.assertTrue(CAPTION.match('Table B.3 (continued)'))
        self.assertTrue(CAPTION.match('Figure 3 — Elements of risk'))
        self.assertFalse(CAPTION.match('Table B.2 is a subset of Table B.1'))


class FormulaAndListRulesTest(unittest.TestCase):
    """Rules found loading IEC 62443-4-1, 4-2, 3-3 (2026-10-24), on texts written for the test."""

    def structure(self, text, sid='9'):
        own, children = split_clause(node('CL_' + sid, 'clause', sid, text), 'en', sid)
        return [(c.seqId, c.parentSeqId) for c in children], {c.seqId: c.text['en'] for c in children}

    def test_fraction_on_three_lines(self):
        from normkb.pdfstd import linearize_formulas
        page = '            A\n   X = 1 − (    ) × 100\n            B\nwhere'
        self.assertEqual(linearize_formulas(page).split('\n')[0].split(), ['X', '=', '1', '−', '(', 'A/B', ')', '×', '100'])
        # two fractions, the sign of the middle line between their numerators
        page = '            2 U\n     Z ≤     ×\n            3 I\n'
        self.assertEqual(linearize_formulas(page).split('\n')[0].split(), ['Z', '≤', '2/3', '×', 'U/I'])
        # a table column with an empty cell is not a fraction
        page = '   alpha      beta\n   gamma\n   delta      eps'
        self.assertEqual(linearize_formulas(page), page)

    def test_symbol_font_characters(self):
        from normkb.pdfstd import SYMBOL
        self.assertEqual('\uf06cD \uf0b4 \uf04d\uf054\uf054F \uf0b3 99 \uf044'.translate(SYMBOL), 'λD × MTTF ≥ 99 Δ')

    def test_page_footnotes(self):
        from normkb.pdfstd import PdfStandardReader
        lines = [(1, 'a paragraph that goes on on the'), (1, '___________'), (1, '3   A footnote of the page.'),
                 (1, '    its second line.'), (2, 'next page.')]
        self.assertEqual(PdfStandardReader.page_footnotes(lines, 1), (['3 A footnote of the page. its second line.'], 4))
        # the rule that ends the document is not followed by footnotes
        self.assertIsNone(PdfStandardReader.page_footnotes([(1, '___________'), (1, 'Price group XY')], 0))

    def test_legend_joins_its_formula_while_contiguous(self):
        text = ('The value is:\n\nX = A × B\nwhere\n\nA is the first factor;\n\nB is the second factor:\n\n'
                '– condition one;\n\nC is a third factor.')
        got, texts = self.structure(text)
        self.assertTrue(texts['9.p2'].endswith('B is the second factor:'))
        self.assertIn(('9.p2.li1', '9.p2'), got)
        self.assertEqual(texts['9.p3'], 'C is a third factor.')      # after the list: a paragraph again

    def test_numbered_points_and_new_list(self):
        got, _ = self.structure('Rules:\n\n1) first rule;\n\n2) second rule.')
        self.assertEqual(got, [('9.pt1', '9'), ('9.pt2', '9')])     # 2) follows 1), not a sub-point of it
        got, _ = self.structure('Access by:\n\nKind one:\n\na) first\n\nb) second\n\nKind two:\n\na) third')
        self.assertIn(('9.p3.pta', '9.p3'), got)

    def test_point_ending_with_comma_is_not_a_heading(self):
        got, _ = self.structure('Where the circuit is either:\n\n1) connected one way, or;\n\n'
                                '2) connected the other way,\n\nMulti-pole switches are then used.')
        self.assertIn(('9.p2', '9'), got)


class RequirementRefsTest(unittest.TestCase):
    def test_identifiers_and_enhancements(self):
        from normkb.items import Item
        from normkb.req_refs import requirement_refs

        def item(sid, parent, typ, title='', text='', number=None):
            it = Item(seqId=sid, parentSeqId=parent, type=typ, number=number)
            it.title['en'], it.text['en'] = title, text
            return it
        items = [item('5.3', None, 'AitArticle', 'CR 1.1 – Human user identification'),
                 item('5.3.3', '5.3', 'AitArticle', 'Requirement enhancements'),
                 item('5.3.3.pt1', '5.3.3', 'AitPoint', text='(1) Unique identification', number='1'),
                 item('5.3.4', '5.3', 'AitArticle', 'Security levels'),
                 item('5.3.4.li2', '5.3.4', 'AitPoint', text='• SL-C(IAC,component) 2: CR 1.1 (1)'),
                 item('5.4.1', None, 'AitArticle', 'Requirement', 'See SR 9.9 and CR 1.1.')]
        requirement_refs(items, 'X', [], '/nonexistent', {})
        self.assertEqual([(r.raw, r.toSeqId) for r in items[4].refs], [('CR 1.1 (1)', '5.3.3.pt1')])
        self.assertEqual([(r.raw, r.toSeqId) for r in items[5].refs], [('CR 1.1', '5.3')])   # SR 9.9: not defined


class RowTextTest(unittest.TestCase):
    def test_labels_as_read_and_empty_cells(self):
        # note letters are left out when the header is read (by size and position): a label ending in a or b is a word
        self.assertEqual(row_text(['No.', 'Esempi di criteri di prova', 'Potential consequences'], ['1', 'crushing', '']),
                         'No.: 1; Esempi di criteri di prova: crushing')

    def test_footnote_row(self):
        self.assertEqual(row_text(['No.', 'Origin'], ['a A footnote of the table.', '']), 'a A footnote of the table.')


class IndexRefsTest(unittest.TestCase):
    IDS = {'3.29', '5.5.2.3.1', '5.5.2.3.1.p1', '5.5.2.3.1.p1.pta', '7', '7.p1', '7.p1.ptc', 'ANXB', 'TABB.1',
           'FIG1', 'INTRO', '3.30', '3.34', '3.21', '3.22'}

    def test_kinds(self):
        refs, bad = index_refs('3.29; 5.5.2.3.1 a); Clause 7 c); Annex B; Table B.1.1; Figure 1; Introduction',
                               self.IDS)
        self.assertEqual(bad, [])
        self.assertEqual([s for _, s in refs], ['3.29', '5.5.2.3.1.p1.pta', '7.p1.ptc', 'ANXB', 'TABB.1', 'FIG1',
                                                'INTRO'])

    def test_ranges_occurrences_and_stray_stop(self):
        refs, bad = index_refs('3.30 to 3.34; 3.21;.3.22; numerous occurrences in Clause 6', self.IDS)
        self.assertEqual(bad, [])
        self.assertEqual([s for _, s in refs], ['3.30', '3.34', '3.21', '3.22'])

    def test_unknown_is_reported(self):
        self.assertEqual(index_refs('6.4.1.3', self.IDS)[1], ['6.4.1.3'])


class PartitionTest(unittest.TestCase):
    def test_lost_text_is_an_error(self):
        doc = node('DOC', 'document', None)
        cl = node('CL_1', 'clause', '1', 'First paragraph.\n\nSecond paragraph.', 'Scope')
        cl.parentId = doc.nodeId
        items = nodes_to_items([doc, cl], 'en')
        self.assertEqual(check_partition([doc, cl], items, 'en'), [])
        items = [i for i in items if i.seqId != '1.p2']
        self.assertTrue(check_partition([doc, cl], items, 'en'))


CFG = json.load(open(paths.CONFIG, encoding='utf-8'))
ISO = next(n for n in CFG['norms'] if n['normId'] == 'ISO-12100-2010')
ISO_PDF = os.path.join(CFG['sourceRoot'], ISO['file'])


IEC = next(n for n in CFG['norms'] if n['normId'] == 'IEC-60204-1-2006')
IEC_PDF = os.path.join(CFG['sourceRoot'], IEC['file'])


@unittest.skipUnless(os.path.exists(ISO_PDF) and os.path.exists(IEC_PDF), 'licensed PDF not present')
class TableHeaderTest(unittest.TestCase):
    def test_note_letters_superscript_only(self):
        from normkb.pdf_tables import read_tables
        iso = read_tables(ISO_PDF, ['B.1'])['B.1']
        self.assertIn('Examples of hazards Origin', iso['header'])          # "Origin" with its note a raised
        iec = read_tables(IEC_PDF, ['10'], pages_kept=None)['10']
        self.assertIn('I a N', ' '.join(c for r in iec['rows'] for c in r))  # the subscript a of Ia stays


@unittest.skipUnless(os.path.exists(IEC_PDF), 'licensed PDF not present')
class Iec60204PdfTest(unittest.TestCase):
    def test_page_alternation(self):
        from normkb.pdfstd import PdfStandardReader
        r = PdfStandardReader(IEC['normId'], IEC_PDF, language='en', boilerplate=IEC['boilerplate'], title=IEC['title'])
        langs = r.page_languages(r.pages())
        # Italian pages listing English titles (bibliography, references table) are Italian pages
        self.assertEqual([langs[p - 1] for p in (218, 219, 222, 223, 224, 225)], ['en', 'other'] * 3)
        self.assertEqual(r.report['languageCorrected'], [219, 223, 225])
        # the cover summary and the back cover stay as detected
        self.assertNotEqual(langs[1], 'en')


@unittest.skipUnless(os.path.exists(ISO_PDF), 'licensed PDF not present')
class Iso12100PdfTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        from normkb.pdf_tables import read_index
        ix = ISO['indexes'][0]
        cls.entries, cls.notes, cls.dropped = read_index(ISO_PDF, ix['pages'], ix['columns'])

    def test_index_entries(self):
        self.assertEqual(len(self.entries), 261)
        self.assertEqual(len(self.notes), 2)
        self.assertTrue(all(len(e) == 4 and e[0] and e[3] for e in self.entries))

    def test_index_cells_in_reading_order(self):
        # "3.28.8" sits on a different baseline than "5.3.3" in the PDF
        space = next(e for e in self.entries if e[0] == 'space limit')
        self.assertEqual(space[3], '3.28.8; 5.3.3')

    def test_untitled_clauses(self):
        from normkb.pdfstd import PdfStandardReader
        r = PdfStandardReader(ISO['normId'], ISO_PDF, language='en', boilerplate=ISO['boilerplate'],
                              title=ISO['title'])
        by = {n.number: n for n in r.read() if n.kind == 'clause'}
        for num in ('6.4.1.1', '6.4.1.2', '6.4.1.3'):
            self.assertEqual(by[num].title['en'], '', num)
            self.assertEqual(by[num].parentId, by['6.4.1'].nodeId)
        self.assertTrue(by['6.4.1.2'].text['en'].startswith('Information shall be provided'))
        self.assertEqual(by['6.4.5.1'].title['en'], 'Contents')


if __name__ == '__main__':
    unittest.main()
