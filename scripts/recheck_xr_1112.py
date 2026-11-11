# -*- coding: utf-8 -*-
"""补全 meta 后重算两池摘要级 XR 命中，确认候选集合稳定。"""
import json
import sys
sys.path.insert(0, "scripts")
from fetch_rss import kw_match  # noqa: E402

reg = set()
for line in open("papers/library/registry.jsonl", encoding="utf-8"):
    if line.strip():
        reg.add(json.loads(line)["id"].split(":")[-1].split("v")[0])

meta = json.load(open("data/meta_1112.json", encoding="utf-8"))
newpool = json.load(open("data/newday_1112.json", encoding="utf-8"))
prevpool = json.load(open("data/missed_listing_1112.json", encoding="utf-8"))


def build(pool, out):
    hits = {}
    for p, v in pool.items():
        m = meta.get(p, {})
        title = m.get("title") or (v[1] if isinstance(v, list) else v.get("title", ""))
        abs_ = m.get("abstract", "")
        if kw_match(title + " " + abs_):
            hits[p] = {"cat": v[0] if isinstance(v, list) else v.get("cat", ""), "title": title,
                       "abstract": abs_, "published": m.get("published", ""),
                       "primary": m.get("primary", ""), "in_registry": p in reg}
    json.dump(hits, open(out, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    return hits


n = build(newpool, "data/missed_new_1112_xr.json")
p = build(prevpool, "data/missed_prev_1112_xr.json")
print("11-11 新组 XR:", len(n), " 11-10 组未入馆 XR:", len(p))
print("缺摘要:", sum(1 for k in list(newpool) + list(prevpool) if k not in meta))
print("new ids:", sorted(n))
print("prev ids:", sorted(p))
