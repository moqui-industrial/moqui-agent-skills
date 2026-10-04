#!/usr/bin/env python3
"""Catalog of every DataDocument and DataFeed defined in the data files of the given components.

Usage: build_document_catalog.py OUT_FILE COMPONENT_DIR [COMPONENT_DIR ...]
Use it to reuse or clone an existing document before writing a new one.
"""
import sys, os, glob, collections
import xml.etree.ElementTree as ET

DD = {"moqui.entity.document.DataDocument", "dataDocuments", "DataDocument"}
DF = {"moqui.entity.feed.DataFeed", "dataFeeds", "DataFeed"}


def local(t):
    return t.split("}")[-1]


def main():
    out, comps = sys.argv[1], sys.argv[2:]
    docs, feeds = [], []
    for c in comps:
        cname = os.path.basename(os.path.normpath(c))
        for p in sorted(glob.glob(os.path.join(c, "data", "*.xml"))):
            try:
                root = ET.parse(p).getroot()
            except ET.ParseError:
                continue
            for el in root:
                if not isinstance(el.tag, str):
                    continue
                t = local(el.tag)
                if t in DD:
                    kids = [local(k.tag) for k in el if isinstance(k.tag, str)]
                    nf = sum(1 for k in kids if k in ("fields", "moqui.entity.document.DataDocumentField"))
                    nc = sum(1 for k in kids if k in ("conditions", "moqui.entity.document.DataDocumentCondition"))
                    paths = [k.get("fieldPath", "") for k in el if isinstance(k.tag, str)
                             and local(k.tag) in ("fields", "moqui.entity.document.DataDocumentField")]
                    rels = sorted({p.split(":")[0] for p in paths if ":" in p and "(" not in p})
                    docs.append((el.get("indexName", ""), el.get("dataDocumentId"), el.get("primaryEntityName", ""),
                                 nf, nc, ", ".join(rels), cname, os.path.basename(p)))
                elif t in DF:
                    dl = [k.get("dataDocumentId") for k in el if isinstance(k.tag, str)]
                    feeds.append((el.get("dataFeedId"), el.get("dataFeedTypeEnumId", ""), el.get("feedName", ""),
                                  ", ".join(x for x in dl if x), cname, os.path.basename(p)))
    fed = collections.defaultdict(list)
    for fid, _, _, dl, _, _ in feeds:
        for d in dl.split(", "):
            if d:
                fed[d].append(fid)
    with open(out, "w") as f:
        f.write("# DataDocuments and DataFeeds in the components (generated)\n\n")
        f.write(f"{len(docs)} documents, {len(feeds)} feeds. A document without a feed is never indexed "
                "automatically; Mantle keeps such documents as templates to clone.\n\n")
        f.write("## Documents by index\n\n| Index | Document | Primary entity | Fields | Conditions | Relationships used | Feeds | Source |\n"
                "| --- | --- | --- | --- | --- | --- | --- | --- |\n")
        for idx, did, prim, nf, nc, rels, cname, fn in sorted(docs, key=lambda x: (x[0], x[1] or "")):
            f.write(f"| {idx} | {did} | {prim.split('.')[-1]} | {nf} | {nc} | {rels} | {', '.join(fed.get(did, [])) or '—'} | {cname}/{fn} |\n")
        f.write("\n## Feeds\n\n| Feed | Type | Name | Documents | Source |\n| --- | --- | --- | --- | --- |\n")
        for fid, ft, fn_, dl, cname, fn in sorted(feeds):
            f.write(f"| {fid} | {ft} | {fn_} | {dl} | {cname}/{fn} |\n")
    print(f"documents={len(docs)} feeds={len(feeds)}")


if __name__ == "__main__":
    main()
