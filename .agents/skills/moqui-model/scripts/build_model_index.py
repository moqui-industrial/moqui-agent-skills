#!/usr/bin/env python3
"""Build a compact, greppable index of the Moqui data model ("what can be expressed").

Usage:
  build_model_index.py OUT_DIR COMPONENT_DIR [COMPONENT_DIR ...]

A component dir is any directory containing entity/ and/or data/ subdirectories
(moqui-framework/framework, mantle-udm, mantle-usl, moqui-math, moqui-device, your own).

Output (all plain Markdown, one line per item, made for grep):
  entities/<pkg-group>.md   entities + view-entities grouped by package prefix
  enums.md                  Enumeration values grouped by enumTypeId
  status.md                 StatusItem values by statusTypeId + StatusFlowTransition edges
  roles.md                  RoleType values
  patterns.md               counts of recurring data patterns, with example entities
Seed data is read from <seed-data> blocks inside entity files and from data/*.xml files of
type seed, seed-initial and install. Demo data is ignored on purpose.
"""
import sys, os, glob, collections
import xml.etree.ElementTree as ET

SEED_TYPES = {"seed", "seed-initial", "install"}


def local(tag):
    return tag.split("}")[-1]


def short(name):
    return name.split(".")[-1]


def pkg_group(pkg):
    parts = pkg.split(".")
    return ".".join(parts[:2]) if len(parts) >= 2 else pkg


class Index:
    def __init__(self):
        self.entities = {}      # full name -> dict
        self.views = {}         # full name -> dict
        self.enums = collections.defaultdict(dict)   # enumTypeId -> {enumId: desc}
        self.enum_types = {}
        self.status = collections.defaultdict(dict)  # statusTypeId -> {statusId: desc}
        self.status_types = {}
        self.flows = collections.defaultdict(list)   # statusFlowId -> [(from,to,name)]
        self.roles = {}
        self.enum_parents = {}
        self.gl_names, self.item_gl = {}, []
        self.enum_groups = collections.defaultdict(set)
        self.sources = collections.Counter()

    # ---------- entities ----------
    def parse_entity_file(self, path, comp):
        try:
            root = ET.parse(path).getroot()
        except ET.ParseError as e:
            print(f"WARN parse error {path}: {e}", file=sys.stderr)
            return
        for el in root:
            tag = local(el.tag)
            if tag in ("entity", "extend-entity") and el.get("entity-name"):
                self._entity(el, comp, tag == "extend-entity")
            elif tag == "view-entity":
                self._view(el, comp)
            elif tag == "seed-data":
                for d in el:
                    self._data_el(d)

    def _entity(self, el, comp, extend):
        pkg = el.get("package") or el.get("package-name") or ""
        name = el.get("entity-name")
        full = f"{pkg}.{name}" if pkg else name
        e = self.entities.get(full)
        if e is None:
            if extend:
                # extend-entity of something not (yet) seen: record under its name
                e = {"pkg": pkg, "name": name, "comp": comp, "pk": [], "fields": [], "rels": [], "extends": []}
                e["ralias"], e["masters"] = {}, {}
            else:
                e = {"pkg": pkg, "name": name, "comp": comp, "pk": [], "fields": [], "rels": [], "extends": []}
                e["ralias"], e["masters"] = {}, {}
            self.entities[full] = e
        if extend:
            e["extends"].append(comp)
        if el.get("cache"):
            e["cache"] = el.get("cache")
        for f in el:
            t = local(f.tag)
            if t == "field":
                fn, ft = f.get("name"), f.get("type", "")
                e["fields"].append((fn, ft))
                if f.get("is-pk") == "true":
                    e["pk"].append(fn)
            elif t == "relationship":
                rel = f.get("related") or f.get("related-entity-name") or ""
                ti = f.get("title", "")
                e["rels"].append((f.get("type", "one"), rel, ti))
                for key in filter(None, [f.get("short-alias"), (ti + "#" + rel) if ti else rel,
                                         (ti + "#" + short(rel)) if ti else short(rel), ti + short(rel)]):
                    e["ralias"].setdefault(key, rel)
            elif t == "master":
                e["masters"][f.get("name", "default")] = f
            elif t == "seed-data":
                for d in f:
                    self._data_el(d)
        self.sources[comp] += 0 if extend else 1

    def _view(self, el, comp):
        pkg = el.get("package") or el.get("package-name") or ""
        name = el.get("entity-name")
        full = f"{pkg}.{name}" if pkg else name
        members = [(m.get("entity-alias"), m.get("entity-name"), m.get("join-optional") == "true")
                   for m in el if local(m.tag) == "member-entity"]
        members += [(m.get("entity-alias"), f"rel {m.get('join-from-alias')}:{m.get('relationship')}",
                     m.get("join-optional") == "true") for m in el if local(m.tag) == "member-relationship"]
        aliases = [a.get("name") for a in el if local(a.tag) == "alias" and a.get("name")]
        alias_all = [a.get("entity-alias") for a in el if local(a.tag) == "alias-all"]
        self.views[full] = {"pkg": pkg, "name": name, "comp": comp, "members": members,
                            "aliases": aliases, "alias_all": alias_all}

    # ---------- data ----------
    def parse_data_file(self, path):
        try:
            root = ET.parse(path).getroot()
        except ET.ParseError as e:
            print(f"WARN parse error {path}: {e}", file=sys.stderr)
            return
        if root.get("type") not in SEED_TYPES:
            return
        for d in root:
            self._data_el(d)

    def _data_el(self, d):
        t = short(local(d.tag))
        a = d.attrib
        if t == "Enumeration" and a.get("enumId"):
            desc = a.get("description", "")
            if a.get("parentEnumId"):
                desc += f" (parent: {a['parentEnumId']})"
                self.enum_parents[a["enumId"]] = a["parentEnumId"]
            self.enums[a.get("enumTypeId", "?")][a["enumId"]] = desc
        elif t == "EnumerationType" and a.get("enumTypeId"):
            self.enum_types[a["enumTypeId"]] = a.get("description", "")
        elif t == "StatusItem" and a.get("statusId"):
            self.status[a.get("statusTypeId", "?")][a["statusId"]] = a.get("description", "")
        elif t == "StatusType" and a.get("statusTypeId"):
            self.status_types[a["statusTypeId"]] = a.get("description", "")
        elif t == "StatusFlowTransition" and a.get("statusId"):
            self.flows[a.get("statusFlowId", "Default")].append(
                (a["statusId"], a.get("toStatusId", ""), a.get("transitionName", "")))
        elif t == "RoleType" and a.get("roleTypeId"):
            self.roles[a["roleTypeId"]] = a.get("description", "")
        elif t == "EnumGroupMember" and a.get("enumId") and a.get("enumGroupEnumId"):
            self.enum_groups[a["enumId"]].add(a["enumGroupEnumId"])
        elif t == "GlAccount" and a.get("glAccountId"):
            self.gl_names[a["glAccountId"]] = a.get("accountName", "")
        elif t == "ItemTypeGlAccount" and a.get("itemTypeEnumId"):
            self.item_gl.append((a.get("organizationPartyId", ""), a["itemTypeEnumId"], a.get("direction", ""),
                                 a.get("glAccountId", "")))
        # nested children (e.g. Enumeration inside EnumerationType)
        for c in d:
            if local(c.tag)[0].isupper() or "." in local(c.tag):
                self._data_el(c)

    # ---------- output ----------
    def write(self, out):
        os.makedirs(os.path.join(out, "entities"), exist_ok=True)
        groups = collections.defaultdict(list)
        for full, e in self.entities.items():
            groups[pkg_group(e["pkg"])].append(("E", full, e))
        for full, v in self.views.items():
            groups[pkg_group(v["pkg"])].append(("V", full, v))
        toc = []
        for g in sorted(groups):
            items = sorted(groups[g], key=lambda x: (x[0], x[1]))
            path = os.path.join(out, "entities", f"{g}.md")
            with open(path, "w") as f:
                f.write(f"# {g}\n\nOne line per entity. E = entity, V = view-entity. Generated; do not edit.\n\n")
                for kind, full, x in items:
                    if kind == "E":
                        fields = ", ".join(f"{n}:{t}" for n, t in x["fields"] if n not in x["pk"])
                        rels = ", ".join(f"{ty}>{short(r)}" + (f"[{ti}]" if ti else "") for ty, r, ti in x["rels"])
                        ext = f" | extended-by: {','.join(x['extends'])}" if x["extends"] else ""
                        f.write(f"- E {full} | src: {x['comp']} | pk: {','.join(x['pk'])} | fields: {fields}"
                                f" | rels: {rels}{ext}\n")
                    else:
                        mem = ", ".join(f"{al}={short(n)}" + ("?" if opt else "") for al, n, opt in x["members"])
                        al = ", ".join(x["aliases"])
                        aa = f" | alias-all: {','.join(x['alias_all'])}" if x["alias_all"] else ""
                        f.write(f"- V {full} | src: {x['comp']} | members: {mem}{aa} | aliases: {al}\n")
            ne = sum(1 for k, _, _ in items if k == "E")
            toc.append((g, ne, len(items) - ne))
        with open(os.path.join(out, "entities", "INDEX.md"), "w") as f:
            f.write("# Entity index by package group\n\n| Group | Entities | View entities |\n| --- | --- | --- |\n")
            for g, ne, nv in toc:
                f.write(f"| {g} | {ne} | {nv} |\n")

        with open(os.path.join(out, "enums.md"), "w") as f:
            f.write("# Enumerations (seed/install data)\n\nFormat: `## enumTypeId` then `- enumId: description`.\n\n")
            for t in sorted(self.enums):
                f.write(f"## {t}" + (f" — {self.enum_types[t]}" if self.enum_types.get(t) else "") + "\n")
                for k, v in sorted(self.enums[t].items()):
                    f.write(f"- {k}: {v}\n")
                f.write("\n")

        with open(os.path.join(out, "status.md"), "w") as f:
            f.write("# Status items and status flows (seed/install data)\n\n## Status items by type\n\n")
            for t in sorted(self.status):
                f.write(f"### {t}" + (f" — {self.status_types[t]}" if self.status_types.get(t) else "") + "\n")
                for k, v in sorted(self.status[t].items()):
                    f.write(f"- {k}: {v}\n")
                f.write("\n")
            f.write("## Status flow transitions\n\nFormat: `from -> to (transitionName)`. Only these moves are allowed by default.\n\n")
            for fl in sorted(self.flows):
                f.write(f"### flow {fl}\n")
                for a, b, n in sorted(self.flows[fl]):
                    f.write(f"- {a} -> {b}" + (f" ({n})" if n else "") + "\n")
                f.write("\n")

        with open(os.path.join(out, "roles.md"), "w") as f:
            f.write("# Role types (seed/install data)\n\n")
            for k, v in sorted(self.roles.items()):
                f.write(f"- {k}: {v}\n")

        self._patterns(out)
        self._structures(out)
        self._masters(out)
        self._item_types(out)

    def _patterns(self, out):
        pats = collections.OrderedDict()

        def add(key, full):
            pats.setdefault(key, []).append(full)

        for full, e in self.entities.items():
            fn = {n for n, _ in e["fields"]}
            if "fromDate" in e["pk"]:
                add("Effective dating: fromDate in PK (+ thruDate) — query with date-filter", full)
            if "statusId" in fn:
                add("Status-bearing: has statusId — changes go through services, check StatusFlow", full)
            if "pseudoId" in fn:
                add("Has pseudoId: user-facing code distinct from the technical PK", full)
            if any(n.endswith("TypeEnumId") for n in fn):
                add("Typed by Enumeration: *TypeEnumId field", full)
            if len(e["pk"]) >= 2 and any(p.endswith("SeqId") for p in e["pk"]):
                add("Detail/line pattern: parent PK + *SeqId", full)
            if {"partyId", "roleTypeId"} <= fn and e["name"] != "PartyRole":
                add("Party-in-role: partyId + roleTypeId on a business object", full)
            if e["name"].endswith("Type") and "parentTypeId" in fn:
                add("Type hierarchy entity: *Type with parentTypeId", full)
        with open(os.path.join(out, "patterns.md"), "w") as f:
            f.write("# Recurring data patterns (computed)\n\n")
            for k, lst in pats.items():
                ex = ", ".join(sorted(short(x) for x in lst)[:12])
                f.write(f"## {k}\n- count: {len(lst)}\n- examples: {ex}\n\n")


REFERENCE_TARGETS = {"Enumeration", "StatusItem", "Uom", "UserAccount", "Geo", "TimePeriod"}


def _structures(self, out):
    ents = self.entities
    by_short = collections.defaultdict(list)
    for full, e in ents.items():
        by_short[e["name"]].append(full)

    def target(rel):
        c = by_short.get(short(rel), [])
        return c[0] if len(c) == 1 else (rel if rel in ents else None)

    # 1. aggregates: identifying composition (child PK strictly contains parent PK)
    #    or detail by name (child name starts with parent name and has a one> link to it)
    children = collections.defaultdict(list)
    has_parent = set()
    for full, e in ents.items():
        for ty, rel, ti in e["rels"]:
            if not ty.startswith("one") or ti:
                continue
            pf = target(rel)
            if not pf or pf == full or short(pf) in REFERENCE_TARGETS:
                continue
            p = ents[pf]
            ident = p["pk"] and set(p["pk"]) < set(e["pk"])
            named = e["name"].startswith(p["name"]) and e["name"] != p["name"]
            if ident or named:
                children[pf].append((full, "pk" if ident else "detail"))
                has_parent.add(full)
    roots = sorted(r for r in children if r not in has_parent)

    def tree(n, depth, seen, lines):
        for c, kind in sorted(children.get(n, [])):
            if c in seen:
                continue
            seen.add(c)
            lines.append("  " * depth + f"- {short(c)}" + ("" if kind == "pk" else " (own id, linked)"))
            tree(c, depth + 1, seen, lines)

    multi = []
    for r in roots:
        lines = []
        tree(r, 1, {r}, lines)
        depth = max((len(l) - len(l.lstrip(" "))) // 2 for l in lines) if lines else 0
        multi.append((r, depth, lines))
    # 2. self hierarchies: parent* field pointing to the same entity
    selfh = []
    for full, e in ents.items():
        for fn, _ in e["fields"]:
            if fn.startswith("parent") and fn.endswith("Id"):
                selfh.append((full, fn))
    # 3. hubs / star schema: many one> links to business entities
    hubs = []
    for full, e in ents.items():
        tg = {short(r) for ty, r, ti in e["rels"] if ty.startswith("one") and short(r) not in REFERENCE_TARGETS}
        if len(tg) >= 8:
            hubs.append((len(tg), full, sorted(tg)))
    hubs.sort(reverse=True)
    # 4. group / member and assoc (graph edges between instances of the same entity)
    groups, assocs = [], []
    for full, e in ents.items():
        tg = [short(r) for ty, r, ti in e["rels"] if ty.startswith("one")]
        if e["name"].endswith("Member"):
            groups.append((full, list(dict.fromkeys(tg))))
        cnt = collections.Counter(t for t in tg if t not in REFERENCE_TARGETS)
        same = [t for t, n in cnt.items() if n >= 2]
        if e["name"].endswith("Assoc") and same:
            assocs.append((full, same))

    with open(os.path.join(out, "structures.md"), "w") as f:
        f.write("# Structural patterns (computed from entity relationships)\n\n")
        f.write("Use this file to understand how concepts are composed before writing a query or a write.\n\n")
        f.write("## 1. Aggregates (header, parts, lines, details)\n\n")
        f.write("Children are created after their parent and usually through the parent's services. "
                "Plain child: its PK contains the parent PK plus a *SeqId. "
                "'own id, linked': it has its own id but belongs to the parent. "
                "Multi-level aggregates are listed first.\n\n")
        for r, depth, lines in sorted(multi, key=lambda x: (-x[1], x[0])):
            f.write(f"### {short(r)} ({r}) — depth {depth}\n" + "\n".join(lines) + "\n\n")
        f.write("Note: a line can also point to a sibling level without being its child by PK "
                "(OrderItem has orderPartSeqId: it belongs to an OrderPart of the same OrderHeader).\n\n")
        f.write("## 2. Self hierarchies (parent*Id on the same entity)\n\n")
        f.write("Trees of the same concept: a WorkEffort under a WorkEffort, an OrderItem under an OrderItem, "
                "an Enumeration under an Enumeration (parentEnumId, see enums.md).\n\n")
        for full, fn in sorted(selfh):
            f.write(f"- {short(full)}.{fn}\n")
        f.write("\n## 3. Hubs (star-schema-like entities)\n\n")
        f.write("Entities that tie many business objects together, like a fact table. "
                "Good starting points for analytical queries and for tracing what happened to an item.\n\n")
        for n, full, tg in hubs:
            f.write(f"- {short(full)} ({n} links): {', '.join(tg)}\n")
        f.write("\n## 4. Group / member\n\n")
        f.write("Membership, usually with validity dates (fromDate in PK): add a member by creating the row, "
                "remove it by setting thruDate.\n\n")
        for full, tg in sorted(groups):
            f.write(f"- {short(full)}: {' + '.join(tg)}\n")
        f.write("\n## 5. Assoc (typed links between instances of the same entity)\n\n")
        for full, same in sorted(assocs):
            f.write(f"- {short(full)}: links {', '.join(same)} to {', '.join(same)}\n")
        if self.enum_parents:
            f.write(f"\n## 6. Enumeration hierarchies\n\n{len(self.enum_parents)} enum values have a parentEnumId "
                    "(shown as '(parent: X)' in enums.md). A child value is a refinement of its parent: "
                    "code that checks the parent must also accept its children.\n")


Index._structures = _structures


def _masters(self, out):
    ents = self.entities
    by_short = collections.defaultdict(list)
    for full in ents:
        by_short[short(full)].append(full)

    def resolve(name):
        if name in ents:
            return name
        c = by_short.get(short(name), [])
        return c[0] if len(c) == 1 else None

    def walk(ent_full, node, depth, lines):
        e = ents.get(ent_full)
        for d in node:
            if local(d.tag) != "detail":
                continue
            rn = d.get("relationship", "")
            rel = e["ralias"].get(rn) if e else None
            tgt = resolve(rel) if rel else None
            label = short(tgt) if tgt else "?"
            um = d.get("use-master")
            lines.append("  " * depth + f"- {rn} -> {label}" + (f" (use-master {um})" if um else ""))
            if tgt:
                walk(tgt, d, depth + 1, lines)

    with open(os.path.join(out, "masters.md"), "w") as f:
        f.write("# Entity masters (declared aggregates, generated)\n\n")
        f.write("A <master> in an entity definition is Moqui's own declaration of a business document: the root entity "
                "plus the relationships that belong to it, nested. The same definition drives the master REST API "
                "(/rest/m1/...) and data export with dependents. Prefer it over the computed trees in structures.md.\n\n")
        n = 0
        for full in sorted(ents):
            for mname, node in ents[full]["masters"].items():
                lines = []
                walk(full, node, 1, lines)
                f.write(f"## {short(full)} — master '{mname}' ({full})\n" + "\n".join(lines) + "\n\n")
                n += 1
    print(f"masters={n}")


Index._masters = _masters


def _item_types(self, out):
    item = self.enums.get("ItemType", {})
    mapped = collections.defaultdict(list)
    for org, it, d, gl in self.item_gl:
        mapped[it].append(f"{d or '?'}:{gl} {self.gl_names.get(gl, '')}".strip() + (f" [{org}]" if org != "DefaultSettings" else ""))
    users = [full for full, e in self.entities.items() if any(n == "itemTypeEnumId" for n, _ in e["fields"])]
    with open(os.path.join(out, "item-types.md"), "w") as f:
        f.write("# Item types and their GL accounts (generated)\n\n")
        f.write("`itemTypeEnumId` (Enumeration type `ItemType`) is a field of: " +
                ", ".join(sorted(short(u) for u in users)) + ".\n\n")
        f.write("The GL mapping comes from `ItemTypeGlAccount` rows in install data (mostly ZaaGlAccountsInstallData.xml, "
                "for the template organization DefaultSettings, copied to a real organization by "
                "mantle.ledger.LedgerServices.init#PartyAccountingConfiguration). Direction: O = outgoing/sales, "
                "I = incoming/purchase, E = either.\n\n")
        f.write("When an invoice item is posted, the account is looked up by product first (product category, product, "
                "asset type) for product item types, then by the exact itemTypeEnumId in ItemTypeGlAccount: the parent "
                "enum is NOT used as a fallback, so every item type that is invoiced needs its own mapping.\n\n")
        f.write("Groups (EnumGroupMember) say where a type may be used: EngItemsSales = outgoing/receivable/sales lines, "
                "EngItemsPurchase = incoming/payable/purchase lines, EngItemsAdjust = invoice adjustments, "
                "EngItemsProduct = product lines.\n\n")
        f.write("| Item type | Description | Parent | Groups | GL mapping |\n| --- | --- | --- | --- | --- |\n")
        for it in sorted(item):
            desc = item[it].split(" (parent:")[0]
            par = self.enum_parents.get(it, "")
            grp = ", ".join(sorted(g.replace("EngItems", "") for g in self.enum_groups.get(it, ())))
            f.write(f"| {it} | {desc} | {par} | {grp} | {'; '.join(mapped.get(it, [])) or '—'} |\n")
        unmapped = [it for it in item if it not in mapped]
        f.write(f"\n{len(item)} item types, {len(item) - len(unmapped)} with a GL mapping, {len(unmapped)} without.\n")
    print(f"itemTypes={len(item)} mapped={len(item) - len(unmapped)}")


Index._item_types = _item_types


def main():
    if len(sys.argv) < 3:
        print(__doc__)
        sys.exit(1)
    out, comps = sys.argv[1], sys.argv[2:]
    idx = Index()
    for c in comps:
        cname = os.path.basename(os.path.normpath(c))
        if cname == "framework":
            cname = "moqui-framework"
        for p in sorted(glob.glob(os.path.join(c, "entity", "*.xml"))):
            if p.endswith((".eecas.xml", ".secas.xml")):
                continue
            idx.parse_entity_file(p, cname)
        for p in sorted(glob.glob(os.path.join(c, "data", "*.xml"))):
            idx.parse_data_file(p)
    idx.write(out)
    print(f"entities={len(idx.entities)} views={len(idx.views)} enumTypes={len(idx.enums)} "
          f"statusTypes={len(idx.status)} flows={len(idx.flows)} roles={len(idx.roles)}")


if __name__ == "__main__":
    main()
