#!/usr/bin/env python3
"""Catalog of the data files shipped with components: load type, load order and what each file defines.

Usage: build_data_catalog.py OUT_FILE COMPONENT_DIR [COMPONENT_DIR ...]
Components must be given in load (dependency) order; inside a component files load in file-name order.
"""
import sys, os, glob, collections
import xml.etree.ElementTree as ET


def short(t):
    return t.split("}")[-1].split(".")[-1]


def main():
    out, comps = sys.argv[1], sys.argv[2:]
    with open(out, "w") as f:
        f.write("# Data files catalog (generated)\n\n")
        f.write("Load order: components in dependency order, then files in name order. Use these files as "
                "patterns for your own setup data; demo files are examples of style, never sources of ids.\n\n")
        for c in comps:
            files = sorted(glob.glob(os.path.join(c, "data", "*.xml")))
            if not files:
                continue
            f.write(f"## {os.path.basename(os.path.normpath(c))}\n\n| File | Type | Records | Main content (top-level element counts) |\n| --- | --- | --- | --- |\n")
            for p in files:
                try:
                    root = ET.parse(p).getroot()
                except ET.ParseError:
                    continue
                cnt = collections.Counter(short(e.tag) for e in root if isinstance(e.tag, str))
                total = sum(1 for e in root.iter() if isinstance(e.tag, str)) - 1
                main = ", ".join(f"{k} {v}" for k, v in cnt.most_common(6))
                f.write(f"| {os.path.basename(p)} | {root.get('type', '')} | {total} | {main} |\n")
            f.write("\n")
    print("ok")


if __name__ == "__main__":
    main()
