#!/usr/bin/env python3
"""Build the xml-actions reference ("how things are programmed") from the XSD and real code.

Usage:
  build_actions_reference.py XML_ACTIONS_XSD OUT_FILE CODE_DIR [CODE_DIR ...]

For every element declared in xml-actions-3.xsd it writes: substitution group, documentation,
attributes (required, default, allowed values, short doc), allowed children, how often it is
used inside <actions> blocks of the given code dirs, and the shortest real example found.
Elements are ordered by real usage, so the top of the file is what matters most.
"""
import sys, re, glob, collections
import xml.etree.ElementTree as ET

XS = "{http://www.w3.org/2001/XMLSchema}"


def clean(s, n=None):
    s = re.sub(r"\s+", " ", (s or "")).strip()
    return (s[:n] + "…") if n and len(s) > n else s


def doc_of(el):
    d = el.find(f"{XS}annotation/{XS}documentation")
    return clean(d.text if d is not None else "")


def parse_xsd(path):
    root = ET.parse(path).getroot()
    elements = {}
    for el in root.findall(f"{XS}element"):
        name = el.get("name")
        if not name or el.get("abstract") == "true":
            continue
        info = {"group": el.get("substitutionGroup", ""), "doc": doc_of(el), "attrs": [], "children": []}
        ct = el.find(f"{XS}complexType")
        if ct is not None:
            for a in ct.iter(f"{XS}attribute"):
                vals = [e.get("value") for e in a.iter(f"{XS}enumeration")]
                info["attrs"].append({
                    "name": a.get("name") or a.get("ref"),
                    "req": a.get("use") == "required",
                    "default": a.get("default"),
                    "values": vals,
                    "doc": doc_of(a),
                })
            for r in ct.iter(f"{XS}element"):
                if r.get("ref"):
                    info["children"].append(r.get("ref"))
            for g in ct.iter(f"{XS}group"):
                if g.get("ref") == "AllOperations":
                    info["children"].append("(any action)")
        elements[name] = info
    return elements


def scan_usage(dirs, names):
    count = collections.Counter()
    in_screens = collections.Counter()
    example = {}
    files = []
    for d in dirs:
        files += glob.glob(f"{d}/**/*.xml", recursive=True)
    tag_re = re.compile(r"<([a-z][a-z-]*)(\s[^<>]*?)?/>|<([a-z][a-z-]*)(\s[^<>]*?)?>", re.S)
    for f in files:
        try:
            text = open(f, encoding="utf-8").read()
        except Exception:
            continue
        is_screen = "/screen/" in f or "/template/" in f
        for _, block in re.findall(r"<(actions|always-actions|pre-actions|row-actions)>(.*?)</\1>", text, re.S):
            for m in tag_re.finditer(block):
                name = m.group(1) or m.group(3)
                if name not in names:
                    continue
                count[name] += 1
                if is_screen:
                    in_screens[name] += 1
                snippet = clean(m.group(0))
                if 20 <= len(snippet) <= 220 and (name not in example or len(snippet) > len(example[name][0]) and len(example[name][0]) < 60):
                    example[name] = (snippet, f.split("/")[-1])
    return count, example, in_screens


def main():
    if len(sys.argv) < 4:
        print(__doc__)
        sys.exit(1)
    xsd, out, dirs = sys.argv[1], sys.argv[2], sys.argv[3:]
    elements = parse_xsd(xsd)
    count, example, in_screens = scan_usage(dirs, set(elements))
    total = sum(count.values()) or 1
    order = sorted(elements, key=lambda n: (-count[n], n))
    with open(out, "w") as f:
        f.write("# xml-actions element reference (generated)\n\n")
        f.write(f"Source: xml-actions-3.xsd plus usage counted inside <actions> blocks of {', '.join(dirs)}.\n")
        f.write(f"Total element occurrences counted: {total}. Elements ordered by real usage.\n\n")
        f.write("## Usage summary\n\nUses counts every <actions>, <always-actions>, <pre-actions> and <row-actions> block; "
                "'in screens' is the part found in screen files (screen, transition and form actions).\n\n"
                "| Element | Uses | In screens | Cumulative |\n| --- | --- | --- | --- |\n")
        cum = 0
        for n in order:
            if count[n] == 0:
                continue
            cum += count[n]
            f.write(f"| {n} | {count[n]} | {in_screens[n]} | {cum * 100 // total}% |\n")
        unused = [n for n in order if count[n] == 0]
        f.write(f"\nDeclared but never used in the scanned code: {', '.join(unused)}\n\n## Elements\n\n")
        for n in order:
            e = elements[n]
            f.write(f"### {n}\n")
            f.write(f"- uses: {count[n]} (in screens: {in_screens[n]})" + (f" | group: {e['group']}" if e["group"] else "") + "\n")
            if e["doc"]:
                f.write(f"- doc: {clean(e['doc'], 400)}\n")
            if e["children"]:
                f.write(f"- children: {', '.join(dict.fromkeys(e['children']))}\n")
            for a in e["attrs"]:
                bits = []
                if a["req"]:
                    bits.append("required")
                if a["default"] is not None:
                    bits.append(f"default={a['default']}")
                if a["values"]:
                    bits.append("values=" + "|".join(a["values"]))
                line = f"  - `{a['name']}`" + (f" ({', '.join(bits)})" if bits else "")
                if a["doc"]:
                    line += f": {clean(a['doc'], 220)}"
                f.write(line + "\n")
            if n in example:
                f.write(f"- example ({example[n][1]}): `{example[n][0]}`\n")
            f.write("\n")
    print(f"elements={len(elements)} used={sum(1 for n in elements if count[n])} occurrences={total}")


if __name__ == "__main__":
    main()
