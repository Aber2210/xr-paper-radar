# -*- coding: utf-8 -*-
"""复核 11-26 公告组未入馆 513 篇：摘要级 XR 命中是否全部已被上批（11-27）显式处置。

判定：命中集合 ⊆ (nonxr_1127 ∪ xr_pool_1127 ∪ xr_final_1127 ∪ backfill_pool_1127 ∪ scored_1127 ∪ registry)
     → 该公告组 0 漏网；否则列入漏网候选。

摘要来源：11-27（上一批 RSS，覆盖 11-26 组 569/569）与 11-28（今日 cs.AI 陈旧 feed 子集）两份全量；
今日 cs.CV/cs.GR/HC/MM/RO/eess.IV 均为 0 条目（周五公告组未释放）。
"""

import json, re, sys
sys.path.insert(0, "scripts")
from fetch_rss import kw_match

EXTRA = ["virtual reality", "augmented reality", "mixed reality", "spatial", "immersive",
         "head mounted", "goggles", "stereo", "3d reconstruction", "novel view",
         "view synthesis", "point cloud", "mesh", "6-dof", "pose estimation",
         "hand", "gaze", "user study", "presence", "teleoperation", "sim-to-real",
         "gaussian", "radiance field", "depth", "visual odometry", "tracking"]

rss = {}
for f in ("data/raw/2026-11-27.jsonl", "data/raw/2026-11-28_all.jsonl"):
    for l in open(f, encoding="utf-8"):
        if l.strip():
            r = json.loads(l)
            rss.setdefault(r["base_id"], r)

missed = json.load(open("data/missed_prev_1128.json", encoding="utf-8"))


def ids_of(obj):
    if isinstance(obj, dict):
        return set(obj.keys())
    return {r["id"] if isinstance(r, dict) else r for r in obj}


handled = set()
for f in ("data/nonxr_1127.json", "data/xr_pool_1127.json", "data/xr_final_1127.json",
          "data/backfill_pool_1127.json", "data/scored_1127.json", "data/old_replace_1127.json"):
    try:
        handled |= ids_of(json.load(open(f, encoding="utf-8")))
    except FileNotFoundError:
        print("  (missing)", f)

unknown = [p for p in missed if p not in rss]
print(f"prev 组未入馆 {len(missed)} 篇，其中 {len(unknown)} 篇无 RSS 摘要（无法判定）")
if unknown:
    print("  无摘要样例:", unknown[:5])
hits, new_hits = {}, {}
for p in missed:
    r = rss.get(p)
    if not r:
        continue
    txt = r["title"] + " " + re.sub(r"^arXiv:\S+\s+Announce Type:\s*\w+\s+Abstract:\s*", "", r.get("abstract", ""))
    t = r["title"].lower()
    hit_kw = kw_match(txt)
    hit_ex = [w for w in EXTRA if w in t]
    if hit_kw or hit_ex:
        hits[p] = {"title": r["title"], "cat": r.get("primary_category"),
                   "kw": bool(hit_kw), "extra": hit_ex[:3], "handled": p in handled}
        if p not in handled:
            new_hits[p] = hits[p]

print(f"摘要/标题级 XR 命中 {len(hits)} 篇；其中上批未处置（潜在漏网）{len(new_hits)} 篇")
for p, v in sorted(new_hits.items()):
    print("  MISS?", p, v["cat"], v["title"][:90], v["extra"])
json.dump(new_hits, open("data/missed_xr_1128.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("saved data/missed_xr_1128.json", len(new_hits))
