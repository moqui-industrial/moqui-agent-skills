"""Hook test suite (PLAN-NORMS-AGREEMENT.md WPE.3), first cases on the proposals: from a hook, the norm items it
reaches must include the expected ones (recall) and must not include the excluded ones (precision). The same cases
will run against the database once the vocabulary is loaded. Run from the scripts directory of moqui-norm-hooks:
python3 -m unittest discover tests"""
import glob
import json
import sys
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(HERE))
import vocab  # noqa: E402

PROPOSALS = vocab.paths.VOCABULARY
IR = vocab.paths.IR

# hook key -> (items that must be reached, items that must not be reached); R@ = Regulation, I@ = ISO 12100, E@ = IEC 60204-1
CASES = {
    # search test T5: a PLC loaded in the PLM
    'safety-logic-unit': ({'R@ANXI.B.pt17', 'R@ANXII.pt4', 'I@6.2.11.7'}, {'R@ANXI.B.pt16'}),
    # search test T1: control devices and their position
    'control-device': ({'R@ANXIII.B.1.2.2.p1', 'R@ANXIII.B.1.2.3.p1', 'R@ANXIII.B.1.2.4.1.p2'}, {'R@ANXIII.B.1.3.4'}),
    # cyber security hooks of 1.1.9
    'data-transmission-hardware': ({'R@ANXIII.B.1.1.9.p2'}, {'R@ANXIII.B.1.1.9.p4'}),
    'cn-intervention-logging': ({'R@ANXIII.B.1.1.9.p2', 'R@ANXIII.B.1.1.9.p5'}, {'R@ANXIII.B.1.1.9.p1'}),
    'cn-safety-version-log-5y': ({'R@ANXIII.B.1.2.1.p2.ptf'}, {'R@ANXIII.B.1.2.1.p3.ptb'}),
    # features with a threshold
    'travel-over-6mm': ({'R@ANXI.B.pt9'}, {'R@ANXI.B.pt10'}),
    'uc-explosive-atmosphere': ({'R@ANXIII.B.1.5.7.p2', 'R@ANXIII.B.1.7.3.p3'}, {'R@ANXIII.B.1.5.7.p1'}),
    # chapter 3: autonomous mobile machinery, remote control (cyber security: the machine answers only its units)
    'autonomous-mobile-machinery': ({'R@ANXIII.B.3.1.1.ptc', 'R@ANXIII.B.3.3.3.p6', 'R@ANXIII.B.3.5.1.p3'}, {'R@ANXIII.B.4.2.2'}),
    'uc-remote-controlled': ({'R@ANXIII.B.3.3.p2', 'R@ANXIII.B.3.3.p4'}, {'R@ANXIII.B.3.3.p1'}),
    'fn-signal-loss-stop': ({'R@ANXIII.B.3.3.3.p4.ptd'}, {'R@ANXIII.B.3.3.3.p3'}),
    # chapters 4 and 6: lifting
    'fn-overload-protection': ({'R@ANXIII.B.4.2.2', 'R@ANXIII.B.6.1.2'}, {'R@ANXIII.B.4.2.1'}),
    'load-carrier': ({'R@ANXIII.B.4.1.1.ptg', 'R@ANXIII.B.6.4.2'}, {'R@ANXIII.B.4.3.2.p1'}),
    # ISO 12100: guards, by kind, down to the point and the index row (French and German terms, clause list)
    'interlocking-guard': ({'I@3.27.4', 'I@6.3.2.2.ptb', 'I@6.3.2.3.pta', 'I@ANXC.r124'}, {'I@6.3.2.2.pta'}),
    'fixed-guard': ({'I@3.27.1', 'I@6.3.3.2.2', 'I@6.3.2.2.pta', 'I@ANXC.r83'}, {'I@6.3.2.2.ptb'}),
    'presence-sensing-device': ({'I@3.28.5', 'I@6.3.2.5', 'I@6.3.2.2.ptd'}, {'I@6.3.2.2.pta'}),
    # the machine as functional chain (Annex A): device roles of a safety function
    'role-input': ({'I@FIGA.1.sensors', 'I@6.2.11.7.2'}, {'I@FIGA.1.power-control'}),
    'role-output': ({'I@FIGA.1.power-control'}, {'I@FIGA.1.sensors'}),
    'control-system': ({'R@ANXIII.B.1.2.1.p1', 'R@ANXIII.B.1.2.1.p2', 'R@ANXIII.B.1.2.1.p2.ptb', 'R@ANXIII.B.1.2.1.p3',
                        'I@6.2.11', 'I@FIGA.1.processing', 'I@ANXC.r31'},
                       {'R@ANXIII.B.1.2.1.p3.pta', 'R@ANXIII.B.1.5.12', 'I@6.3.4.2'}),
    # zones of an assembly (DeviceGroup), isolation and stored energy
    'machine-zone': ({'I@6.2.11.1.p7'}, {'I@6.2.11.1.p6'}),
    'fn-isolation': ({'I@6.2.11.1.p7', 'I@6.3.5.4.p1.pta'}, {'I@6.3.5.4.p1.ptc'}),
    # cyber security: restricted access to safety software and to modes
    'cn-access-restriction': ({'I@6.2.11.7.3.p3', 'I@6.2.11.10.p2', 'I@ANXC.r1'}, {'I@6.2.11.7.3.p1'}),
    # hazards by origin (Table B.1 row of their type) and by consequence
    'hzo-high-pressure': ({'I@TABB.1.r1', 'I@6.2.10'}, {'I@TABB.1.r2'}),
    'hzc-crushing': ({'I@TABB.1.r1', 'I@6.2.2.1.p2.ptb', 'I@ANXC.r32', 'R@ANXIII.B.3.3.4.p1.pta'}, {'I@TABB.1.r2'}),
    'hzc-electric-shock': ({'I@TABB.1.r2', 'I@ANXC.r54'}, {'I@TABB.1.r1'}),
    # risk graph parameters (severity, exposure, avoidance)
    'severity-of-harm': ({'I@5.5.2.2', 'I@FIG3.severity'}, {'I@5.5.2.3'}),
    'harm-avoidance': ({'I@5.5.2.3.3'}, {'I@5.5.2.2'}),
    # IEC 60204-1, the disconnect switch case: the supply disconnecting device in the three norms
    'supply-disconnecting-device': ({'E@5.3', 'E@TABF.1.r4', 'I@6.3.5.4', 'R@ANXIII.B.1.6.3'}, {'E@10.7', 'E@FIG1.power-supply'}),
    'disconnecting-device': ({'E@5.5.p3', 'E@5.6.p2'}, {'E@5.3'}),
    'emergency-stop-device': ({'R@ANXII.pt10', 'R@ANXIII.B.1.2.4.3.p1', 'R@ANXIII.B.1.2.2.p1.ptg', 'E@10.7',
                               'E@9.2.5.4.2.p1', 'I@6.3.5.2'}, {'R@ANXII.pt16', 'E@10.8.4'}),
    'fn-stop-cat-0': ({'E@9.2.2', 'E@9.2.5.4.2.p2'}, {'E@9.2.2.li3'}),
    # in IEC 60204-1 "protective device" is an electrical protective device, not a safeguard
    'electrical-protective-device': ({'E@7.9.p1', 'E@D.2.p2'}, {'E@3.49'}),
    'protective-device': ({'E@3.49', 'E@9.4.1.p3.li1'}, {'E@7.9.p1', 'E@D.2.p2'}),
    'residual-current-device': ({'E@15.1.n2', 'E@7.7.p1'}, {'E@7.2.8'}),
    # the block diagram of a typical machine: a box is linked by its own label
    'programmable-controller': ({'R@ANXIII.B.1.2.1.p2.ptc', 'I@6.2.11.7.1', 'E@FIG1.plc'}, {'R@ANXIII.B.1.3.4', 'E@FIG1.equipment'}),
    # IEC 62061 (T@, Italian edition): the SCS and its subsystems at the clauses whose subject they are
    'scs': ({'T@3.2.3', 'T@6', 'T@INTRO.p1', 'R@ANXIII.B.3.3.3.p4.ptc'}, {'T@FOREWORD'}),
    'scs-subsystem': ({'T@3.2.4', 'T@7'}, {'T@6.8'}),
    # SIL and PFH limits at their own row of Table 3 and of the comparison Table 4
    'sil-3': ({'T@TAB3.r3', 'T@TAB4.r4', 'T@TAB6.r2'}, {'T@TAB3.r1', 'T@TAB4.r2'}),
    'pfh-below-1e-7': ({'T@TAB3.r3'}, {'T@TAB3.r1'}),
    # architectures and diagnostic coverage levels: the definition and the table rows that state them
    'arch-d': ({'T@7.5.2.4', 'T@FIG11', 'T@TABH.1.r1'}, {'T@7.5.2.3'}),
    'dc-from-99pct': ({'T@7.4.3.3', 'T@TABD.1.r3', 'T@B.4.2.3.p1'}, {'T@TABD.1.r2'}),
    'sff-from-60pct': ({'T@TAB6', 'T@7.5.3.p3'}, {'T@7.5.3.p2'}),
    # security of the SCS (clause 6.8 and the definitions of 3.2.69)
    'cn-security-measures': ({'T@3.2.69', 'T@6.8'}, {'T@6.7'}),
    'enabling-device': ({'T@FIGF.1', 'T@TABF.3.r7', 'E@10.9'}, {'T@TABF.3.r3'}),
    # IEC 62443 (P33@ 3-3, P42@ 4-2, P41@ 4-1): security levels from the SL lists and the Annex B rows, not the level below
    'iac-sl-2': ({'P33@5.1.li2', 'P33@5.3.4.li2', 'P42@5.3.4.li2', 'P33@TABB.1.r3'}, {'P33@5.3.4.li1', 'P42@5.3.4.li1'}),
    'iacs-component': ({'P42@3.1.10', 'P42@5', 'P41@3.1.13'}, {'P33@5'}),
    'embedded-device': ({'P42@3.1.18', 'P42@13', 'P42@A.2'}, {'P42@14'}),
    'security-zone': ({'P33@3.1.47', 'P33@9.4.1'}, {'P33@3.1.12'}),
    'threat-modelling': ({'P41@3.1.37', 'P41@6.3'}, {'P41@6.2'}),
    'sdl-maturity-3': ({'P41@TAB1.r3'}, {'P41@TAB1.r1'}),
    # Cyber Resilience Act (C@): classes, essential requirements, support period, SBOM
    'cra-routers-modems-switches': ({'C@ANXIII.clI.pt12'}, {'C@ANXIII.clII.pt2'}),
    'critical-product': ({'C@ANXIV', 'C@ART8'}, {'C@ANXIII'}),
    'cn-access-protection': ({'C@ANXI.I.pt2.spd'}, {'C@ANXI.I.pt2.spe'}),
    'support-period-from-5y': ({'C@ART13.8.s3'}, {'C@ART3.pt20'}),
    'support-period': ({'C@ART3.pt20'}, set()),
    'sbom': ({'C@ART3.pt39', 'C@ANXI.II.pt1'}, {'C@ANXI.II.pt2'}),
}
# hook key -> feature groups its category must carry (ProductCategoryFeatGrpAppl)
GROUPS = {'metal-press': {'fg-motion'}, 'person-lifting-device': {'fg-fall-height'}, 'machinery': {'fg-noise-emission'},
          'lifting-machinery': {'fg-lifting-rating'}, 'mobile-machinery': {'fg-vibration-emission'},
          'food-pharma-machinery': {'fg-hygiene'}}
# feature group -> its feature type (ProductFeatureType)
FEATURE_TYPES = {'fg-hazard-consequence': 'CmpPftHazardConsequence', 'hz-mechanical': 'CmpPftHazardOrigin',
                 'fg-electrical-rating': 'CmpPftElectricalRating', 'fg-environment': 'CmpPftEnvironment',
                 'fg-functional-safety': 'CmpPftFunctionalSafety', 'fg-fr1-iac': 'CmpPftSecurityLevel',
                 'fg-sdl-maturity': 'CmpPftProcessMaturity', 'fg-cra-essential-requirements': 'CmpPftCyberSecurity'}
# feature key -> (number, uom, comparison)
THRESHOLDS = {'travel-over-6mm': (6, 'LEN_mm', '>'), 'speed-over-30mms': (30, 'VEL_mm_s', '>'),
              'fall-height-over-3m': (3, 'LEN_m', '>'), 'cn-safety-version-log-5y': (5, 'TF_yr', '>='),
              'noise-workstation-over-70dba': (70, 'SND_dBA', '>'),
              'max-working-load-from-1000kg': (1000, 'WT_kg', '>='), 'overturning-moment-from-40000nm': (40000, 'TRQ_Nm', '>='),
              'vibration-whole-body-over-0-5': (0.5, 'ACC_m_s2', '>'),
              'motor-over-0-5kw': (0.5, 'PW_kw', '>'), 'control-voltage-max-277v': (277, 'ELEC_V', '<='),
              'plug-socket-from-30a': (30, 'OTH_A', '>='), 'supply-ac-up-to-1000v': (1000, 'ELEC_V', '<='),
              'storage-min-minus25c': (-25, 'TEMP_C', '>='),
              'pfh-below-1e-7': (1e-07, 'RATE_per_h', '<'), 'dc-from-99pct': (99, 'OTH_pct', '>='),
              'sff-from-60pct': (60, 'OTH_pct', '>='), 'iac-sl-3': (3, None, '>='),
              'support-period-from-5y': (5, 'TF_yr', '>='), 'security-update-kept-10y': (10, 'TF_yr', '>=')}


class HookSuiteTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        exts = sorted(glob.glob(str(PROPOSALS / 'HOOKS-*.json')))
        cls.v = vocab.Vocabulary(PROPOSALS / 'VOCAB-BASE.json', IR, exts)
        errors, _ = cls.v.validate()
        assert not errors, errors
        cls.by_key = {c['key']: c for c in cls.v.concepts}

    def reached(self, key):
        return {ref for ref, _ in self.by_key[key]['clauses']}

    def test_recall_and_precision(self):
        for key, (must, must_not) in CASES.items():
            with self.subTest(hook=key):
                got = self.reached(key)
                self.assertEqual(must - got, set(), f'{key}: expected items not reached')
                self.assertEqual(must_not & got, set(), f'{key}: items reached that do not concern it')

    def test_feature_groups_of_categories(self):
        for key, groups in GROUPS.items():
            with self.subTest(hook=key):
                self.assertTrue(groups <= set(self.by_key[key].get('featureGroups', [])))

    def test_feature_types(self):
        for key, ftype in FEATURE_TYPES.items():
            with self.subTest(group=key):
                self.assertEqual(self.by_key[key]['featureType'], ftype)

    def test_thresholds(self):
        for key, (num, uom, cmp) in THRESHOLDS.items():
            with self.subTest(feature=key):
                c = self.by_key[key]
                self.assertEqual((c['number'], c.get('uom'), c['comparison']), (num, uom, cmp))   # a level has no unit


if __name__ == '__main__':
    unittest.main()
