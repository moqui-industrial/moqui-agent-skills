#!/usr/bin/env python3
"""Deterministic checks of a compliance project before a gate (closing requirements, publishing a report): what a
script can decide is never left to judgement. Exit code 1 when any check fails.

    python3 -I check_project.py --project 100198
    python3 -I check_project.py --project 100198 --advisories advisories.json --root FMQ_DRYING36

Checks:
  project      the SQL checks of moqui-norm-requirements (assets/project-checks.sql): rows "check: ..." must be 0
  evidence     every satisfied requirement has a closed task with evidence; evidence that is only a web page is listed
               for the verifier (a page can change; a stored copy is better)
  firmware     (--advisories) installed firmware of the devices (PhysicalDevice.firmwareVersion) against the minimum
               fixed versions of the advisories; devices without a recorded version are listed
  cve          (--advisories) every CVE of the advisories belongs to the vendor and product it is cited for, read from
               the CVE record (cveawg.mitre.org); a CVE of another vendor is an error (needs network)

advisories.json: [{"advisory": "SSA-688146", "url": "...", "vendor": "Siemens", "productMatch": "1514SP",
                   "minVersion": "V4.1.6", "noFix": false, "cves": ["CVE-2026-25786"], "cveVendor": "Siemens"}]
"""
import argparse
import json
import os
import re
import sys
import urllib.request

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'moqui-compliance-intake', 'scripts'))
from moqui_client import Moqui  # noqa: E402

CHECKS_SQL = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'moqui-norm-requirements', 'assets', 'project-checks.sql')


def version_key(v):
    return [int(x) for x in re.findall(r'\d+', v or '')]


def check_project(m, project):
    sql = open(CHECKS_SQL, encoding='utf-8').read().replace(':project', project)
    sql = '\n'.join(l for l in sql.splitlines() if not l.startswith('--'))
    rows = m.sql(sql)[1:]
    bad = [r for r in rows if r[0].startswith('check:') and r[1] not in ('0', '')]
    for r in rows:
        print(f'  {r[0]}: {r[1]}')
    return bad


def check_evidence(m, project):
    rows = m.sql(f"""SELECT r.REQUIREMENT_ID, c.CONTENT_LOCATION FROM REQUIREMENT r JOIN WORK_REQUIREMENT_FULFILLMENT f ON f.REQUIREMENT_ID = r.REQUIREMENT_ID
        JOIN WORK_EFFORT w ON w.WORK_EFFORT_ID = f.WORK_EFFORT_ID JOIN WORK_EFFORT_CONTENT c ON c.WORK_EFFORT_ID = w.WORK_EFFORT_ID
        WHERE w.ROOT_WORK_EFFORT_ID = '{project}' AND r.STATUS_ID = 'RqmtStSatisfied'""")[1:]
    web = [r for r in rows if r[1].startswith('http')]
    print(f'  satisfied requirements with evidence: {len({r[0] for r in rows})}; evidence only as a web page: {len(web)}')
    for r in web:
        print(f'    {r[0]}: {r[1]} (store a copy with attach_content; the verifier reads it)')
    return []


def check_firmware(m, root, advisories):
    rows = m.sql("""SELECT d.DEVICE_ID, p.VENDOR_NAME, p.MODEL_NAME, p.FIRMWARE_VERSION, a.PRODUCT_ID FROM DEVICE d
        JOIN PHYSICAL_DEVICE p ON p.DEVICE_ID = d.DEVICE_ID LEFT JOIN ASSET a ON a.ASSET_ID = d.ASSET_ID""")[1:]
    bad = []
    for dev, vendor, model, fw, product in rows:
        if root and product and not product.startswith(root.split('_')[0]):
            continue
        for adv in advisories:
            if adv.get('vendor', '').lower() not in (vendor or '').lower() or adv['productMatch'].lower() not in (model or '').lower():
                continue
            if not fw:
                bad.append(f'{dev} {model}: no firmware version recorded, cannot check {adv["advisory"]}')
            elif adv.get('noFix'):
                bad.append(f'{dev} {model} {fw}: {adv["advisory"]} has no fix, the mitigations must be applied')
            elif version_key(fw) < version_key(adv['minVersion']):
                bad.append(f'{dev} {model} {fw} < {adv["minVersion"]} ({adv["advisory"]})')
    for b in bad:
        print('  ' + b)
    print(f'  devices checked: {len(rows)}, findings: {len(bad)}')
    return bad


def check_cves(advisories):
    bad = []
    for adv in advisories:
        for cve in adv.get('cves', []):
            try:
                with urllib.request.urlopen(f'https://cveawg.mitre.org/api/cve/{cve}', timeout=30) as r:
                    rec = json.loads(r.read().decode())
            except Exception as e:  # noqa: BLE001
                bad.append(f'{cve}: CVE record not readable ({e})')
                continue
            aff = rec.get('containers', {}).get('cna', {}).get('affected', [])
            vendors = {(a.get('vendor') or '') for a in aff}
            want = adv.get('cveVendor') or adv.get('vendor', '')
            if not any(want.lower() in v.lower() for v in vendors):
                bad.append(f'{cve} cited in {adv["advisory"]} for {want}: the CVE record names {sorted(vendors)}')
    for b in bad:
        print('  ' + b)
    print(f'  CVEs checked: {sum(len(a.get("cves", [])) for a in advisories)}, mismatches: {len(bad)}')
    return bad


def main():
    ap = argparse.ArgumentParser(description=__doc__.split('\n')[0])
    ap.add_argument('--project', required=True)
    ap.add_argument('--advisories')
    ap.add_argument('--root', help='product id prefix of the project, to limit the firmware check')
    a = ap.parse_args()
    m = Moqui()
    failed = []
    print('== project'); failed += check_project(m, a.project)
    print('== evidence'); failed += check_evidence(m, a.project)
    if a.advisories:
        adv = json.load(open(a.advisories, encoding='utf-8'))
        print('== firmware'); failed += check_firmware(m, a.root, adv)
        print('== cve'); failed += check_cves(adv)
    print(f'RESULT: {"FAIL" if failed else "PASS"} ({len(failed)} findings)')
    sys.exit(1 if failed else 0)


if __name__ == '__main__':
    main()
