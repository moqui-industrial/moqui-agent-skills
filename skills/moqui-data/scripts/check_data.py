#!/usr/bin/env python3
"""Validate a Moqui entity-facade-xml data file against the real model.

Usage:
  check_data.py DATA.xml --src DIR [--src DIR ...]

--src: component roots (moqui-framework/framework, mantle-udm, mantle-usl, moqui-math, moqui-device, yours).
Checks:
  ROOT   <entity-facade-xml> root with a type attribute (seed, seed-initial, install, demo, or a custom type)
  REF    every top-level element is an entity (full or unique short name) or a service (path.verbNoun or path.verb#Noun)
  NEST   every nested element resolves to a relationship of its parent (short-alias, title+related, related)
         or to an entity that has a relationship back to the parent
  FIELD  every attribute is a field of the entity (or an in-parameter of the service)
  VALUE  *EnumId, statusId, roleTypeId values exist in seed/install data of the sources or in this file
  DOC    DataDocument: primaryEntityName exists, every fieldPath resolves through relationship names to a field,
         expression paths have a fieldNameAlias, conditions refer to fields or aliases of the document
Exit code 1 on any ERROR.
"""
import sys, re, glob, argparse, collections
import xml.etree.ElementTree as ET


def local(t):
    return t.split("}")[-1]


def short(n):
    return n.split(".")[-1]


class Model:
    def __init__(self, srcs):
        self.ent = {}          # full -> {"fields": set, "pk": [], "rels": [(related, title, alias)]}
        self.ent_alias = {}    # entity short-alias (usable as top-level element) -> full
        self.svc_impl = {}     # service name -> implemented interface names
        self.svc = {}          # name variants -> set(in params)
        self.enum_ids, self.status_ids, self.role_ids = set(), set(), set()
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
                    if t in ("entity", "extend-entity") and el.get("entity-name"):
                        pkg = el.get("package") or el.get("package-name") or ""
                        full = f"{pkg}.{el.get('entity-name')}" if pkg else el.get("entity-name")
                        e = self.ent.setdefault(full, {"fields": {"lastUpdatedStamp"}, "pk": [], "rels": []})
                        if el.get("short-alias"):
                            self.ent_alias[el.get("short-alias")] = full
                        for f in el:
                            ft = local(f.tag)
                            if ft == "field":
                                e["fields"].add(f.get("name"))
                                if f.get("is-pk") == "true":
                                    e["pk"].append(f.get("name"))
                            elif ft == "relationship":
                                e["rels"].append((f.get("related") or f.get("related-entity-name") or "",
                                                  f.get("title", ""), f.get("short-alias", "")))
                            elif ft == "seed-data":
                                for d in f.iter():
                                    self._seed(d)
                    elif t == "seed-data":
                        for d in el.iter():
                            self._seed(d)
            for p in glob.glob(f"{s}/data/*.xml"):
                try:
                    root = ET.parse(p).getroot()
                except ET.ParseError:
                    continue
                if root.get("type") == "demo":
                    continue
                for d in root.iter():
                    self._seed(d)
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
                    verb, noun = el.get("verb", ""), el.get("noun", "")
                    ins = {x.get("name") for x in el.iter() if local(x.tag) == "parameter" and x.get("name")}
                    for x in el.iter():
                        if local(x.tag) == "auto-parameters":
                            # Moqui falls back to the service noun when entity-name is missing
                            ins.add("*auto*:" + (x.get("entity-name") or noun))
                    impl = [i.get("service") for i in el if local(i.tag) == "implements" and i.get("service")]
                    for n in (f"{rel}.{verb}#{noun}", f"{rel}.{verb}{noun}", f"{rel}.{verb}"):
                        self.svc[n] = ins
                    self.svc_impl[f"{rel}.{verb}#{noun}"] = impl
        self.by_short = collections.defaultdict(list)
        for full in self.ent:
            self.by_short[short(full)].append(full)
        # inherit in-parameters through <implements>, recursively
        def inherited(n, seen=()):
            out = set()
            for i in self.svc_impl.get(n, []):
                if i in seen:
                    continue
                out |= self.svc.get(i, set()) | inherited(i, seen + (n,))
            return out
        for n in list(self.svc_impl):
            extra = inherited(n)
            if extra:
                self.svc[n] |= extra
        for n, ins in self.svc.items():
            for mk in [x for x in ins if x.startswith("*auto*:")]:
                ins.discard(mk)
                full = self.entity(mk.split(":", 1)[1])
                if full:
                    ins |= self.ent[full]["fields"]
                else:
                    ins.add("*")

    def _seed(self, d):
        t, a = short(local(d.tag)), d.attrib
        if t == "Enumeration" and a.get("enumId"):
            self.enum_ids.add(a["enumId"])
        elif t == "StatusItem" and a.get("statusId"):
            self.status_ids.add(a["statusId"])
        elif t == "RoleType" and a.get("roleTypeId"):
            self.role_ids.add(a["roleTypeId"])

    def rel_target(self, ent, name):
        """Relationship by name only (short-alias, title+related, related), no fallback."""
        for related, title, alias in self.ent[ent]["rels"]:
            if name in {alias, title + short(related), title + "#" + related, related, short(related)} - {""}:
                return self.entity(related)
        return None

    def entity(self, name):
        if name in self.ent:
            return name
        if name in self.ent_alias:
            return self.ent_alias[name]
        c = self.by_short.get(name, [])
        return c[0] if len(c) == 1 else None

    def child_entity(self, parent, tag):
        """Resolve a nested element: relationship short-alias / name, or an entity related back to the parent."""
        pe = self.ent[parent]
        for related, title, alias in pe["rels"]:
            names = {alias, title + short(related), title + "#" + related, related, short(related)} - {""}
            if tag in names:
                return self.entity(related) or related
        full = self.entity(tag)
        if full and any(self.entity(r) == parent for r, _, _ in self.ent[full]["rels"]):
            return full
        return None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("file")
    ap.add_argument("--src", action="append", required=True)
    a = ap.parse_args()
    m = Model(a.src)
    root = ET.parse(a.file).getroot()
    errors, warns = [], []
    if local(root.tag) != "entity-facade-xml":
        errors.append("ROOT root element must be <entity-facade-xml>")
    if not root.get("type"):
        warns.append("ROOT no type attribute: the file loads with every load type")
    # values defined in this file count as existing
    for d in root.iter():
        m._seed(d)

    def check_values(ent_name, el):
        for k, v in el.attrib.items():
            if not v or "$" in v:
                continue
            if k.endswith("EnumId") and v not in m.enum_ids:
                errors.append(f"VALUE {short(ent_name)}.{k}='{v}' is not a known Enumeration")
            elif k == "statusId" and v not in m.status_ids:
                errors.append(f"VALUE {short(ent_name)}.statusId='{v}' is not a known StatusItem")
            elif k == "roleTypeId" and v not in m.role_ids:
                errors.append(f"VALUE {short(ent_name)}.roleTypeId='{v}' is not a known RoleType")

    def walk(el, ent_name, path):
        for c in el:
            tag = local(c.tag)
            if not isinstance(c.tag, str):
                continue
            if tag in m.ent[ent_name]["fields"]:
                continue  # field value given as a child element (long text, CDATA)
            ce = m.child_entity(ent_name, tag)
            if not ce and m.entity(tag):
                # any entity may be nested: the loader passes the parent's values down to fields with the same name
                ce = m.entity(tag)
                warns.append(f"NEST {path}/{tag}: no direct relationship to {short(ent_name)}; "
                             f"only fields with matching names are filled from the parent")
            if not ce or ce not in m.ent:
                errors.append(f"NEST {path}/{tag}: not a relationship of {short(ent_name)}, a field, or an entity")
                continue
            for k in c.attrib:
                if k not in m.ent[ce]["fields"]:
                    errors.append(f"FIELD {short(ce)} has no field '{k}' (at {path}/{tag})")
            check_values(ce, c)
            walk(c, ce, f"{path}/{tag}")

    for el in root:
        if not isinstance(el.tag, str):
            continue
        tag = local(el.tag)
        ent = m.entity(tag)
        if ent:
            for k in el.attrib:
                if k not in m.ent[ent]["fields"]:
                    errors.append(f"FIELD {short(ent)} has no field '{k}'")
            check_values(ent, el)
            walk(el, ent, short(ent))
        elif tag in m.svc:
            ins = m.svc[tag]
            if "*" not in ins:
                for k in el.attrib:
                    if k not in ins:
                        errors.append(f"FIELD service {tag} has no in-parameter '{k}'")
        else:
            errors.append(f"REF {tag}: neither an entity nor a service")
    # DataDocument checks: every fieldPath must resolve on the primary entity through relationship names
    DD, DDF, DDC = "moqui.entity.document.DataDocument", "moqui.entity.document.DataDocumentField", \
        "moqui.entity.document.DataDocumentCondition"
    for el in root:
        if not isinstance(el.tag, str) or m.entity(local(el.tag)) != DD:
            continue
        ddid, prim = el.get("dataDocumentId", "?"), m.entity(el.get("primaryEntityName", ""))
        if not prim:
            errors.append(f"DOC {ddid}: primaryEntityName '{el.get('primaryEntityName')}' is not an entity")
            continue
        aliases = set()
        for c in el:
            if not isinstance(c.tag, str) or m.child_entity(DD, local(c.tag)) != DDF:
                continue
            fp, alias = c.get("fieldPath", ""), c.get("fieldNameAlias")
            if re.search(r"[()?*+/ <>=!]", fp):
                if not alias:
                    errors.append(f"DOC {ddid}: expression fieldPath '{fp}' needs a fieldNameAlias")
                warns.append(f"DOC {ddid}: fieldPath '{fp}' is a Groovy expression")
                aliases.add(alias or fp)
                continue
            cur, parts = prim, fp.split(":")
            for rn in parts[:-1]:
                nxt = m.rel_target(cur, rn)
                if not nxt:
                    errors.append(f"DOC {ddid}: '{rn}' in fieldPath '{fp}' is not a relationship of {short(cur)}")
                    cur = None
                    break
                cur = nxt
            if cur and parts[-1] not in m.ent[cur]["fields"]:
                errors.append(f"DOC {ddid}: {short(cur)} has no field '{parts[-1]}' (fieldPath '{fp}')")
            aliases.add(alias or parts[-1])
        for c in el:
            if isinstance(c.tag, str) and m.child_entity(DD, local(c.tag)) == DDC:
                fa = c.get("fieldNameAlias")
                if fa and fa not in aliases:
                    errors.append(f"DOC {ddid}: condition on '{fa}', which is not a field or alias of the document")
    for w in dict.fromkeys(warns):
        print("WARN ", w)
    for e in dict.fromkeys(errors):
        print("ERROR", e)
    print(f"checked: {a.file} | entities={len(m.ent)} services={len(m.svc)//3} enums={len(m.enum_ids)} | "
          f"errors={len(set(errors))} warnings={len(set(warns))}")
    sys.exit(1 if errors else 0)


if __name__ == "__main__":
    main()
