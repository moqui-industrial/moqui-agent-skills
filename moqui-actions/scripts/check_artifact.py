#!/usr/bin/env python3
"""Static checks for a generated Moqui services file, against real sources.

Usage:
  check_artifact.py GENERATED.xml --src DIR [--src DIR ...] [--allow-script]

--src points at component roots (moqui-framework/framework, mantle-udm, mantle-usl, moqui-math, ...).
Checks:
  REF   every service-call targets an existing service (incl. entity-auto create#/update#/store#/delete#)
  REF   every entity-name used exists as entity or view-entity
  REF   field names in field-map / econdition / order-by / select-field exist on that entity (entities only)
  PARAM in-map keys passed with the literal [key:value] syntax are declared in-parameters of the target
        (entity-auto targets accept the entity fields)
  PROF  no <script> (unless --allow-script)
  PROF  no direct entity-create/update/delete/store on a status-bearing entity (has statusId)
  PROF  no service-call to a service with authenticate="false" or "anonymous-all"
Exit code 1 if any ERROR. Warnings do not fail.
"""
import sys, re, glob, argparse
import xml.etree.ElementTree as ET


def local(t):
    return t.split("}")[-1]


def load_sources(srcs):
    entities, views, services, rels = {}, {}, {}, {}
    for s in srcs:
        for p in glob.glob(f"{s}/entity/*.xml"):
            if p.endswith((".eecas.xml", ".secas.xml")):
                continue
            try:
                root = ET.parse(p).getroot()
            except ET.ParseError:
                continue
            for el in root:
                t = local(el.tag)
                if t not in ("entity", "extend-entity", "view-entity") or not el.get("entity-name"):
                    continue
                pkg = el.get("package") or el.get("package-name") or ""
                full = f"{pkg}.{el.get('entity-name')}" if pkg else el.get("entity-name")
                if t == "view-entity":
                    views[full] = el
                else:
                    flds = entities.setdefault(full, set())
                    flds.update(f.get("name") for f in el if local(f.tag) == "field")
                    rl = rels.setdefault(full, [])
                    rl.extend((f.get("related") or f.get("related-entity-name") or "", f.get("title", ""),
                               f.get("short-alias", "")) for f in el if local(f.tag) == "relationship")
        for p in glob.glob(f"{s}/service/**/*.xml", recursive=True):
            if p.endswith((".secas.xml", ".eecas.xml", ".rest.xml")):
                continue
            rel = p.split("/service/", 1)[1][:-4].replace("/", ".")
            try:
                root = ET.parse(p).getroot()
            except ET.ParseError:
                continue
            for el in root:
                if local(el.tag) != "service":
                    continue
                name = f"{rel}.{el.get('verb')}#{el.get('noun')}" if el.get("noun") else f"{rel}.{el.get('verb')}"
                ins = set()
                for ip in el.iter():
                    if local(ip.tag) == "in-parameters":
                        for prm in ip:
                            if local(prm.tag) == "parameter" and prm.get("name"):
                                ins.add(prm.get("name"))
                            if local(prm.tag) == "auto-parameters":
                                ae = prm.get("entity-name") or el.get("noun")  # Moqui falls back to the noun
                                ins.add(f"*auto*:{ae}" if ae else "*auto*")
                impl = [i.get("service") for i in el if local(i.tag) == "implements" and i.get("service")]
                services[name] = {"in": ins, "auth": el.get("authenticate", "true"), "impl": impl}
    by_short = {}
    for full in list(entities) + list(views):
        by_short.setdefault(full.split(".")[-1], []).append(full)
    # inherit in-parameters through <implements> (recursive)
    def all_in(n, seen=()):
        sv = services.get(n)
        if not sv or n in seen:
            return set()
        r = set(sv["in"])
        for i in sv["impl"]:
            r |= all_in(i, seen + (n,))
        return r
    for n in services:
        services[n]["in"] = all_in(n)
        # replace auto-parameters markers with the real entity fields when the entity is known
        for mk in [x for x in services[n]["in"] if x.startswith("*auto*:")]:
            ae = mk.split(":", 1)[1]
            full = ae if ae in entities else (by_short.get(ae.split(".")[-1]) or [None])[0]
            services[n]["in"].discard(mk)
            if full in entities:
                services[n]["in"] |= entities[full]
            else:
                services[n]["in"].add("*auto*")
    # expand view-entity fields: explicit aliases + alias-all (prefix, exclude), members may be views
    resolved = {}
    def view_fields(full, depth=0):
        if full in resolved:
            return resolved[full]
        el = views[full]
        members = {m.get("entity-alias"): m.get("entity-name") for m in el if local(m.tag) == "member-entity"}
        # member-relationship: the member is the related entity of a relationship of another member
        for m in el:
            if local(m.tag) != "member-relationship":
                continue
            src = members.get(m.get("join-from-alias"), "")
            sfull = src if src in rels else (by_short.get(src.split(".")[-1]) or [None])[0]
            rn = m.get("relationship", "")
            for related, title, alias in rels.get(sfull, []):
                short_rel = related.split(".")[-1]
                if rn in {alias, title + short_rel, title + "#" + related, related, short_rel} - {""}:
                    members[m.get("entity-alias")] = related
                    break
        flds = {a.get("name") for a in el if local(a.tag) == "alias" and a.get("name")}
        for aa in el:
            if local(aa.tag) != "alias-all":
                continue
            mem = members.get(aa.get("entity-alias"), "")
            mfull = mem if (mem in entities or mem in views) else (by_short.get(mem.split(".")[-1]) or [None])[0]
            if mfull in entities:
                base = set(entities[mfull])
            elif mfull in views and depth < 5:
                base = view_fields(mfull, depth + 1)
            else:
                base = set()
            excl = {x.get("field") for x in aa if local(x.tag) == "exclude"}
            pre = aa.get("prefix")
            for f in base - excl:
                flds.add(pre + f[0].upper() + f[1:] if pre else f)
        resolved[full] = flds
        return flds
    for v in list(views):
        view_fields(v)
    views.clear()
    views.update(resolved)
    return entities, views, services, by_short


def resolve_entity(name, entities, views, by_short):
    if name in entities or name in views:
        return name
    cands = by_short.get(name, [])
    return cands[0] if len(cands) == 1 else None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("file")
    ap.add_argument("--src", action="append", required=True)
    ap.add_argument("--allow-script", action="store_true")
    a = ap.parse_args()
    entities, views, services, by_short = load_sources(a.src)
    errors, warns = [], []
    root = ET.parse(a.file).getroot()

    def fields_of(ent):
        return entities.get(ent) or views.get(ent) or set()

    for el in root.iter():
        t = local(el.tag)
        if t == "script" and not a.allow_script:
            errors.append("PROF <script> is not allowed")
        if t == "service-call":
            n = el.get("name", "")
            if "$" in n:
                continue
            m = re.match(r"(create|update|store|delete)#(.+)$", n)
            if m:
                ent = resolve_entity(m.group(2), entities, views, by_short)
                if not ent or ent not in entities:
                    errors.append(f"REF entity-auto target entity not found: {n}")
                    continue
                target_in = entities[ent] | {"*auto*"}
            elif n in services:
                target_in = services[n]["in"]
                if services[n]["auth"] in ("false", "anonymous-all"):
                    errors.append(f"PROF calls {n} which runs with authenticate={services[n]['auth']}")
            else:
                errors.append(f"REF service not found: {n}")
                continue
            im = el.get("in-map", "")
            if im.strip().startswith("[") and "*auto*" not in target_in:
                keys = re.findall(r"[\[,]\s*([A-Za-z_][A-Za-z0-9_]*)\s*:", im)
                for k in keys:
                    if k not in target_in:
                        errors.append(f"PARAM {n} has no in-parameter '{k}'")
        if t in ("entity-find", "entity-find-one", "entity-find-count", "entity-make-value",
                 "entity-create", "entity-update", "entity-delete", "entity-set"):
            en = el.get("entity-name")
            if en and "$" not in en:
                ent = resolve_entity(en, entities, views, by_short)
                if not ent:
                    errors.append(f"REF entity not found: {en}")
                    continue
                flds = fields_of(ent)
                for c in el.iter():
                    ct = local(c.tag)
                    fn = c.get("field-name") if ct in ("field-map", "econdition", "order-by", "select-field") else None
                    if not fn or "$" in fn:
                        continue
                    for one in fn.split(","):
                        one = one.strip().lstrip("-+^").split(" ")[0]
                        if one and one not in flds:
                            errors.append(f"REF {ent} has no field '{one}' ({ct})")
        if t in ("entity-create", "entity-update", "entity-delete", "entity-store"):
            warns.append(f"PROF direct {t} on value-field {el.get('value-field')}: prefer a service")
    # direct writes on status-bearing entities: resolve value-field back to the find/make that created it
    vf_entity = {}
    for el in root.iter():
        if local(el.tag) in ("entity-find-one", "entity-make-value") and el.get("value-field"):
            ent = resolve_entity(el.get("entity-name", ""), entities, views, by_short)
            if ent:
                vf_entity[el.get("value-field")] = ent
    for el in root.iter():
        if local(el.tag) in ("entity-create", "entity-update", "entity-delete", "entity-store"):
            ent = vf_entity.get(el.get("value-field"))
            if ent and "statusId" in entities.get(ent, set()):
                errors.append(f"PROF direct {local(el.tag)} on status-bearing entity {ent}")

    for w in dict.fromkeys(warns):
        print("WARN ", w)
    for e in dict.fromkeys(errors):
        print("ERROR", e)
    print(f"checked: {a.file} | services known={len(services)} entities={len(entities)} views={len(views)} | "
          f"errors={len(set(errors))} warnings={len(set(warns))}")
    sys.exit(1 if errors else 0)


if __name__ == "__main__":
    main()
