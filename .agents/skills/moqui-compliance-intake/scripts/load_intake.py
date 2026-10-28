#!/usr/bin/env python3
"""Load a reviewed intake (the bill of materials with its hooks, function levels and, for an installation, the
instances) into Moqui, after checking it. Nothing is written when a check fails: the failures are the questions to ask.

    python3 -I load_intake.py intake.json --check      # checks only, prints the questions for the user
    python3 -I load_intake.py intake.json              # checks, then loads (Data Import + add_function_product)

intake.json (see references/intake-format.md):
  {"mode": "product" | "installation",
   "root": "<productId>",
   "products": [{"productId", "productName", "partNo"?, "parentProductId"?, "quantity"?, "passive"?,
                 "digital": true|false, "categories": [...], "features": [...]}],
   "functions": [{"parentProductId", "purposeEnumId", "productName", "members": [{"productId", "role"}]}],
   "assets":  [{"assetId", "productId", "serialNumber", "assetName"?, "facilityId"?}],
   "devices": [{"deviceId", "assetId", "deviceTypeEnumId", "purposeEnumId"?, "parentDeviceId"?,
                "physical": {"deviceName", "vendorName", "modelName", "serialNumber", "firmwareVersion", ...}}],
   "groups":  [{"deviceId", "groupName", "deviceTypeEnumId"?, "purposeEnumId", "members": [{"memberDeviceId", "purposeEnumId"?}]}]}

mode "product": a standard product (a boiler, a machine type): products, hooks and function levels only; its zones,
conduits and functions are function products of the type. mode "installation": the plant of one customer: the same
product records plus the Asset (serial number) and Device / PhysicalDevice of every installed unit, and DeviceGroup
records for the zones, conduits and functions found in the drawings (a DeviceGroup is a Device: its purposeEnumId is
the hook, the member purposeEnumId is the role).
"""
import argparse
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from moqui_client import Moqui, xml_attr  # noqa: E402

FROM = '2026-01-01 00:00:00'
FRS = {'IAC', 'UC', 'SI', 'DC', 'RDF', 'TRE', 'RA'}
ROLES = {'CmpDepRoleInput', 'CmpDepRoleLogic', 'CmpDepRoleOutput', 'CmpDepRoleActuator', 'CmpDepRoleMember'}


def checks(m, d):
    q = []  # questions for the user (blocking)
    prods = {p['productId']: p for p in d.get('products', [])}
    if d.get('mode') not in ('product', 'installation'):
        q.append('mode: is this a standard product (type) or the installation of one customer?')
    for p in prods.values():
        for fr, lvl in (p.get('slTarget') or {}).items():
            if fr not in FRS or lvl not in (1, 2, 3, 4):
                q.append(f"{p['productId']}: SL-T {fr}={lvl}: foundational requirement {sorted(FRS)}, level 1-4")
        if p.get('slTarget') and p.get('purposeEnumId') not in ('CmpDepSecurityZone', 'CmpDepSecConduit'):
            q.append(f"{p['productId']}: an SL-T belongs to a zone or conduit product (purposeEnumId CmpDepSecurityZone / CmpDepSecConduit)")
    if d.get('root') not in prods:
        q.append(f"root {d.get('root')}: the root product (machine, system under consideration) is not among the products")
    for p in prods.values():
        if p.get('parentProductId') and p['parentProductId'] not in prods:
            q.append(f"{p['productId']}: parent {p['parentProductId']} is not in the bill")
        if p.get('digital') and not p.get('categories'):
            q.append(f"{p['productId']} ({p.get('productName')}): has digital elements but no category: what is it?")
        if not p.get('passive') and 'digital' not in p:
            q.append(f"{p['productId']} ({p.get('productName')}): does it have digital elements (software, firmware, "
                     f"network or data interface)? Check the datasheet")
    cats = {c for p in prods.values() for c in p.get('categories', [])}
    feats = {f for p in prods.values() for f in p.get('features', [])}
    purposes = {f['purposeEnumId'] for f in d.get('functions', [])} | {g.get('purposeEnumId') for g in d.get('groups', []) if g.get('purposeEnumId')} \
        | {x.get('purposeEnumId') for x in d.get('devices', []) if x.get('purposeEnumId')}
    for missing, kind in ((cats - m.existing('PRODUCT_CATEGORY', 'PRODUCT_CATEGORY_ID', cats), 'category'),
                          (feats - m.existing('PRODUCT_FEATURE', 'PRODUCT_FEATURE_ID', feats), 'feature'),
                          (purposes - m.existing('ENUMERATION', 'ENUM_ID', purposes), 'purpose')):
        for x in sorted(missing):
            q.append(f'{kind} {x} does not exist in the vocabulary: choose another hook or propose a vocabulary change')
    for f in d.get('functions', []):
        if f['parentProductId'] not in prods:
            q.append(f"function {f['productName']}: parent {f['parentProductId']} is not in the bill")
        if not f.get('members'):
            q.append(f"function {f['productName']}: which products realise it?")
        for mb in f.get('members', []):
            if mb['productId'] not in prods:
                q.append(f"function {f['productName']}: member {mb['productId']} is not in the bill")
            if mb.get('role') not in ROLES:
                q.append(f"function {f['productName']}: role of {mb['productId']} (input, logic, output, actuator, member)?")
    if d.get('mode') == 'installation':
        assets = {a['assetId']: a for a in d.get('assets', [])}
        for a in assets.values():
            if a.get('productId') not in prods:
                q.append(f"asset {a['assetId']}: product {a.get('productId')} is not in the bill")
            if not a.get('serialNumber') and prods.get(a.get('productId'), {}).get('productTypeEnumId') != 'CmpPtFunction':
                q.append(f"asset {a['assetId']} ({a.get('assetName')}): serial number (nameplate)?")
        devs = {x['deviceId'] for x in d.get('devices', [])} | {g['deviceId'] for g in d.get('groups', [])}
        if d.get('rootDeviceId') not in devs:
            q.append('rootDeviceId: which device group is the installation (the plant section the assessment covers)?')
        for g in d.get('groups', []):
            if g.get('assetId') and g['assetId'] not in assets:
                q.append(f"group {g['deviceId']}: asset {g['assetId']} missing")
        for x in d.get('devices', []):
            if x.get('assetId') not in assets:
                q.append(f"device {x['deviceId']}: asset {x.get('assetId')} missing")
            ph = x.get('physical') or {}
            if not ph.get('firmwareVersion') and prods.get(assets.get(x.get('assetId'), {}).get('productId'), {}).get('digital'):
                q.append(f"device {x['deviceId']}: firmware version installed (needed for the vulnerability check)?")
        for g in d.get('groups', []):
            if not g.get('purposeEnumId') and g['deviceId'] != d.get('rootDeviceId'):
                q.append(f"group {g['deviceId']} ({g.get('groupName')}): zone, conduit or which function?")
            for mb in g.get('members', []):
                if mb['memberDeviceId'] not in devs:
                    q.append(f"group {g['deviceId']}: member {mb['memberDeviceId']} is not a device of the installation")
    return q


def records(d):
    x = ['<entity-facade-xml type="seed">']
    prods = d.get('products', [])
    for p in prods:
        x.append(f'<mantle.product.Product productId="{xml_attr(p["productId"])}" productTypeEnumId="{xml_attr(p.get("productTypeEnumId", "PtAsset"))}" '
                 + (f'purposeEnumId="{xml_attr(p["purposeEnumId"])}" ' if p.get('purposeEnumId') else '')
                 + f'productName="{xml_attr(p.get("productName", ""))}"/>')
    for p in prods:
        if p.get('parentProductId'):
            x.append(f'<mantle.product.ProductAssoc productId="{xml_attr(p["parentProductId"])}" toProductId="{xml_attr(p["productId"])}" '
                     f'productAssocTypeEnumId="PatEngBom" fromDate="{FROM}" quantity="{p.get("quantity", 1)}"/>')
        for c in p.get('categories', []):
            x.append(f'<mantle.product.category.ProductCategoryMember productId="{xml_attr(p["productId"])}" '
                     f'productCategoryId="{xml_attr(c)}" fromDate="{FROM}"/>')
        for fr, lvl in (p.get('slTarget') or {}).items():
            x.append(f'<mantle.product.feature.ProductFeatureAppl productId="{xml_attr(p["productId"])}" '
                     f'productFeatureId="CMP_PF_{fr}_SL_{lvl}" applTypeEnumId="CmpPfatTarget" fromDate="{FROM}"/>')
        for f in p.get('features', []):
            x.append(f'<mantle.product.feature.ProductFeatureAppl productId="{xml_attr(p["productId"])}" '
                     f'productFeatureId="{xml_attr(f)}" applTypeEnumId="PfatStandard" fromDate="{FROM}"/>')
    for a in d.get('assets', []):
        x.append(f'<mantle.product.asset.Asset assetId="{xml_attr(a["assetId"])}" productId="{xml_attr(a["productId"])}" '
                 f'serialNumber="{xml_attr(a.get("serialNumber", ""))}" assetName="{xml_attr(a.get("assetName", ""))}"'
                 + (f' facilityId="{xml_attr(a["facilityId"])}"' if a.get('facilityId') else '') + '/>')
    for dv in d.get('devices', []) + [dict(g, deviceTypeEnumId=g.get('deviceTypeEnumId', 'DtDeviceGroup')) for g in d.get('groups', [])]:
        attrs = ' '.join(f'{k}="{xml_attr(dv[k])}"' for k in ('deviceId', 'assetId', 'deviceTypeEnumId', 'purposeEnumId', 'parentDeviceId') if dv.get(k))
        x.append(f'<moqui.device.Device {attrs} fromDate="{FROM}"/>')
        ph = dv.get('physical')
        if ph:
            pattrs = ' '.join(f'{k}="{xml_attr(v)}"' for k, v in ph.items() if v)
            x.append(f'<moqui.device.PhysicalDevice deviceId="{xml_attr(dv["deviceId"])}" {pattrs}/>')
    for g in d.get('groups', []):
        x.append(f'<moqui.device.DeviceGroup deviceId="{xml_attr(g["deviceId"])}" groupName="{xml_attr(g.get("groupName", ""))}"/>')
        for i, mb in enumerate(g.get('members', []), 1):
            x.append(f'<moqui.device.DeviceGroupMember deviceId="{xml_attr(g["deviceId"])}" memberDeviceId="{xml_attr(mb["memberDeviceId"])}"'
                     + (f' purposeEnumId="{xml_attr(mb["purposeEnumId"])}"' if mb.get('purposeEnumId') else '') + f' sequenceNum="{i}"/>')
    x.append('</entity-facade-xml>')
    return '\n'.join(x)


def main():
    ap = argparse.ArgumentParser(description=__doc__.split('\n')[0])
    ap.add_argument('intake')
    ap.add_argument('--check', action='store_true')
    ap.add_argument('--xml', help='also write the generated records to this file')
    a = ap.parse_args()
    d = json.load(open(a.intake, encoding='utf-8'))
    m = Moqui()
    q = checks(m, d)
    if q:
        print(f'# {len(q)} open questions: ask the user, update the intake, run again. Nothing was loaded.')
        for i, s in enumerate(q, 1):
            print(f'{i:3}. {s}')
        sys.exit(2)
    xml = records(d)
    if a.xml:
        open(a.xml, 'w', encoding='utf-8').write(xml)
    if a.check:
        print(f'# checks passed: {xml.count(chr(10)) - 1} records ready')
        return
    print(f'# loaded {m.load_xml(xml)} records')
    for f in d.get('functions', []):
        r = m.mcp('add_function_product', parentProductId=f['parentProductId'], purposeEnumId=f['purposeEnumId'],
                  productName=f['productName'], memberList=[{'productId': mb['productId'], 'purposeEnumId': mb['role']}
                                                            for mb in f['members']])
        print(f"# function {f['productName']}: product {r.get('productId')}, {r.get('addedMemberCount')} members")


if __name__ == '__main__':
    main()
