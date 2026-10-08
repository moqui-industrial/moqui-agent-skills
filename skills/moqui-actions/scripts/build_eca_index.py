#!/usr/bin/env python3
"""Index SECA and EECA rules: what runs automatically when a service is called or an entity is written.

Usage:
  build_eca_index.py OUT_FILE COMPONENT_DIR [COMPONENT_DIR ...]

Reads service/**/*.secas.xml and entity/*.eecas.xml. SECAs can be attached to any service name,
including entity-auto names like update#mantle.product.asset.Asset: that is how a status change made
through the service triggers business logic that a direct entity write would skip.
"""
import sys, os, glob, re, collections
import xml.etree.ElementTree as ET


def local(t):
    return t.split("}")[-1]


def clean(s, n=160):
    s = re.sub(r"\s+", " ", s or "").strip()
    return s[:n] + "…" if len(s) > n else s


def calls(el):
    out = []
    for c in el.iter():
        if local(c.tag) == "service-call" and c.get("name"):
            out.append(c.get("name") + (" (async)" if c.get("async") in ("true", "distribute") else ""))
    return out


def cond(el):
    for c in el:
        if local(c.tag) == "condition":
            exprs = [x.get("condition") or x.get("field") or "" for x in c.iter() if local(x.tag) in ("expression", "compare")]
            texts = [clean(x.text) for x in c.iter() if local(x.tag) == "expression" and x.text]
            return clean(" ".join(e for e in exprs + texts if e), 140)
    return ""


def main():
    if len(sys.argv) < 3:
        print(__doc__)
        sys.exit(1)
    out, comps = sys.argv[1], sys.argv[2:]
    secas = collections.defaultdict(list)
    eecas = collections.defaultdict(list)
    for c in comps:
        for p in sorted(glob.glob(f"{c}/service/**/*.secas.xml", recursive=True)):
            for el in ET.parse(p).getroot():
                if local(el.tag) != "seca":
                    continue
                svc = el.get("service", "")
                secas[svc].append((el.get("when", ""), el.get("id", ""), cond(el), calls(el), os.path.basename(p),
                                   el.get("run-on-error") == "true"))
        for p in sorted(glob.glob(f"{c}/entity/*.eecas.xml")):
            for el in ET.parse(p).getroot():
                if local(el.tag) != "eeca":
                    continue
                ops = [o for o in ("create", "update", "delete", "find") if el.get(f"on-{o}") == "true"]
                eecas[el.get("entity", "")].append((",".join(ops), el.get("id", ""), cond(el), calls(el),
                                                    os.path.basename(p), el.get("run-before") == "true",
                                                    el.get("get-original-value") == "true"))
    with open(out, "w") as f:
        f.write("# SECA and EECA rules (generated)\n\n")
        f.write("Before calling a service or writing an entity, look it up here: these rules run automatically.\n"
                "Calls marked (async) are skipped in simulation and run later in a separate transaction.\n\n")
        f.write(f"## SECAs by service ({sum(len(v) for v in secas.values())} rules on {len(secas)} services)\n\n")
        for s in sorted(secas):
            f.write(f"### {s}\n")
            for when, rid, cnd, cl, src, roe in secas[s]:
                f.write(f"- when={when} id={rid}" + (" run-on-error" if roe else "") +
                        (f" | if: {cnd}" if cnd else "") + (f" | calls: {', '.join(cl)}" if cl else "") + f" | {src}\n")
        f.write(f"\n## EECAs by entity ({sum(len(v) for v in eecas.values())} rules on {len(eecas)} entities)\n\n")
        for e in sorted(eecas):
            f.write(f"### {e}\n")
            for ops, rid, cnd, cl, src, before, orig in eecas[e]:
                f.write(f"- on={ops} id={rid}" + (" run-before" if before else "") + (" get-original-value" if orig else "") +
                        (f" | if: {cnd}" if cnd else "") + (f" | calls: {', '.join(cl)}" if cl else "") + f" | {src}\n")
    print(f"secas={sum(len(v) for v in secas.values())} services={len(secas)} "
          f"eecas={sum(len(v) for v in eecas.values())} entities={len(eecas)}")


if __name__ == "__main__":
    main()
