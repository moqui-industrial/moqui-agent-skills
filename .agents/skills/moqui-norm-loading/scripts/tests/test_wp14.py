"""Checks added with WP1.4 (Italian editions, references). Run from the scripts directory of moqui-norm-loading: python3 -m unittest discover tests"""
import os
import sys
import unittest

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, HERE)

from normkb import paths                         # noqa: E402

from normkb.ir import Node, read_jsonl                                    # noqa: E402
from normkb.pdfstd import Patterns, drop_title_tail, split_designations, std_references   # noqa: E402
from normkb.refs import KNOWN                                             # noqa: E402

IR = str(paths.IR)


def node(path, kind, number, text='', lang='en'):
    n = Node(nodeId=f'X:{path}', normId='X', parentId=None, kind=kind, seq=1, number=number)
    n.text[lang] = text
    return n


def targets(n):
    return {(r.raw, r.targetNodeId.split(':')[1] if r.targetNodeId else None, r.external) for r in n.references}


class ItalianPatternsTest(unittest.TestCase):
    def test_structure_words(self):
        p = Patterns('it')
        self.assertTrue(p.annex.match('                                              Allegato ZA'))
        self.assertTrue(p.annex_status.match('   (informativo)'))
        self.assertTrue(p.biblio.match('                                         Bibliografia'))
        self.assertTrue(p.front_section.match('                                           INTRODUZIONE'))
        self.assertEqual(p.front_key('AVVISO DI ADOZIONE'), ('ENDORSEMENT', 'preamble'))
        for caption in ('Figura 1 – Campo di applicazione del presente documento',
                        'Figura A.2 –- Esempio proforma per il processo di assegnazione del SIL',
                        'Figura H.4 –Sottosistema C con funzione esterna per la gestione dei guasti',
                        'Tabella 4 - SIL richiesto e PFH del sottosistema preesistente'):
            self.assertTrue(p.caption.match(caption), caption)

    def test_unknown_language_is_an_error(self):
        with self.assertRaises(ValueError):
            Patterns('de')

    def test_definition_followed_by_a_list_has_no_designation(self):
        n = node('DEF_3.2.7', 'definition', '3.2.7',
                 'componente/sottosistema in cui\n\n– i modi di guasto sono ben definiti; e', 'it')
        split_designations([n], 'it')
        self.assertEqual(n.altTerms, {})
        m = node('DEF_3.2.1', 'definition', '3.2.1', 'macchina\nassieme, dotato o destinato a essere dotato', 'it')
        split_designations([m], 'it')
        self.assertEqual(m.altTerms['it'], [{'term': 'macchina', 'status': 'admitted'}])

    def test_title_of_the_standard_is_dropped_from_the_front_section(self):
        body = [(10, 'Le metodologie sono fornite nell\'Allegato A.'), (10, ''), (11, 'SICUREZZA DEL MACCHINARIO –'),
                (11, 'SICUREZZA FUNZIONALE DEI SISTEMI DI COMANDO E CONTROLLO'), (11, 'RELATIVI ALLA SICUREZZA')]
        title = 'EN IEC 62061:2021 Sicurezza del macchinario - Sicurezza funzionale dei sistemi di comando e ' \
                'controllo relativi alla sicurezza'
        self.assertEqual(drop_title_tail(body, title), body[:1])


class ReferenceTest(unittest.TestCase):
    def test_partition_of_another_norm_is_external(self):
        n = node('CL_6.2.10', 'clause', '6.2.10', 'means are provided (see also ISO 14118:2000, Clause 5), and\n'
                 'device (see Annex A of\nIEC 60947-2).')
        nodes = [n, node('CL_5', 'clause', '5'), node('ANX_A', 'annex', 'A')]
        std_references(nodes, KNOWN, 'en')
        self.assertEqual(targets(n), {('ISO 14118:2000, Clause 5', None, 'ISO 14118:2000, Clause 5'),
                                      ('IEC 60947-2', None, 'IEC 60947-2')})

    def test_italian_references(self):
        n = node('CL_4.2', 'clause', '4.2', 'Determinare l\'integrità richiesta (5.2.5) e vedi anche 10.3 '
                 '(vedi l’Articolo 7). Vedi la IEC 61508-3:2010, Allegato F, e l\'Allegato C della IEC 61508-2:2010; '
                 'resa simile alla 3.2.39.', 'it')
        nodes = [n] + [node(f'CL_{x}', 'clause', x, lang='it') for x in ('5.2.5', '10.3', '7')] + \
            [node('DEF_3.2.39', 'definition', '3.2.39', lang='it'), node('ANX_C', 'annex', 'C', lang='it'),
             node('ANX_F', 'annex', 'F', lang='it')]
        std_references(nodes, KNOWN, 'it')
        internal = {(raw, t) for raw, t, _ in targets(n) if t}
        self.assertEqual(internal, {('5.2.5', 'CL_5.2.5'), ('10.3', 'CL_10.3'), ('Articolo 7', 'CL_7'),
                                    ('3.2.39', 'DEF_3.2.39')})

    def test_equation_numbers_and_figures_are_not_references(self):
        n = node('ANX_H.CL_H.2.2', 'clause', 'H.2.2', 'PFH = λDe1 + λDen (H.1)\ndove (vedi la Figura 7) e l’Articolo 7',
                 'it')
        nodes = [n, node('FIG_7', 'figure', '7', lang='it'), node('CL_7', 'clause', '7', lang='it'),
                 node('ANX_H.CL_H.1', 'clause', 'H.1', lang='it')]
        std_references(nodes, KNOWN, 'it')
        self.assertEqual({(raw, t) for raw, t, _ in targets(n)}, {('Articolo 7', 'CL_7')})


class Iec62061Test(unittest.TestCase):
    @unittest.skipUnless(os.path.exists(os.path.join(IR, 'IEC-62061-2021.jsonl')), 'IR not built')
    def test_structure(self):
        nodes = read_jsonl(os.path.join(IR, 'IEC-62061-2021.jsonl'))
        kinds = {}
        for n in nodes:
            kinds[n.kind] = kinds.get(n.kind, 0) + 1
        self.assertEqual(kinds['definition'], 69)                   # 3.2.1 to 3.2.69
        self.assertEqual(kinds['annex'], 12)                        # A to J, ZA, ZZ
        self.assertEqual(kinds['figure'], 33)
        self.assertEqual(kinds['table'], 37)                        # 1 to 9, A.1 to J.2, ZZ.1
        by_id = {n.nodeId.split(':')[1]: n for n in nodes}
        self.assertTrue(by_id['ANX_ZZ'].title['it'].endswith('che si intende soddisfare'))
        self.assertTrue(by_id['ANX_ZZ'].text['it'].startswith('La presente Norma europea'))
        for n in nodes:
            for r in n.references:
                self.assertFalse(r.targetNodeId and r.targetNodeId.split(':')[1].startswith(('FIG_', 'TAB_')),
                                 f'{n.nodeId} cites {r.raw} as a figure or table')


if __name__ == '__main__':
    unittest.main()
