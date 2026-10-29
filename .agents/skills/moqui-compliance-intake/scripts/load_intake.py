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

The checks and the writing are the Moqui service mantle.compliance.IntakeServices.load#Intake (MCP tool load_intake):
this script only sends the file, so an agent in a chat (LibreChat) and one in a terminal run the same checks.
"""
import argparse
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from moqui_client import Moqui  # noqa: E402

def main():
    ap = argparse.ArgumentParser(description=__doc__.split('\n')[0])
    ap.add_argument('intake')
    ap.add_argument('--check', action='store_true')
    a = ap.parse_args()
    d = json.load(open(a.intake, encoding='utf-8'))
    r = Moqui().mcp('load_intake', intake=d, checkOnly=a.check)
    q = r.get('questions') or []
    if q:
        print(f'# {len(q)} open questions: ask the user, update the intake, run again. Nothing was loaded.')
        for i, s in enumerate(q, 1):
            print(f'{i:3}. {s}')
        sys.exit(2)
    if a.check:
        print('# checks passed: nothing open, ready to load')
        return
    print(f"# written {r.get('written')}; function products {r.get('functionProductIds')}")


if __name__ == '__main__':
    main()
