"""2026-11-18 甄别：对 11-17 公告组 844 篇（listing 全集）与 replace 旧稿做摘要级 XR 过滤。

数据来源：data/raw/2026-11-18_all.jsonl（RSS 7 分类 --no-filter 全量 1323 条，含完整摘要）
覆盖率校验：listing 11-17 组 844 篇 ⊂ RSS 集合（前一步已验证差异 0），故摘要级覆盖率 = 1.0000，
无需再走 API id_list（避免 429 静默丢批风险）；API 仅用于后续候选提交日核验。

输出：
  data/xr_pool_1118.json      11-17 公告组 XR 命中（含 announce type / 摘要 / published）
  data/old_replace_1118.json  replace 类旧稿 XR 命中（backfill 候选）
  data/nonxr_1118.json        当日组非 XR 剔除清单（供下批复核互证）
"""
import json, re, sys
sys.path.insert(0, "scripts")
from fetch_rss import kw_match

# 标题级扩展词补扫（第三层召回，2026-11-14 起固化；不计入 RSS 漏网统计）
EXTRA = [
    "virtual reality", "augmented reality", "mixed reality", "spatial", "immersive",
    "head mounted", "goggles", "stereo", "3d reconstruction", "novel view",
    "view synthesis", "point cloud", "mesh", "6-dof", "pose estimation",
    "hand", "gaze", "user study", "presence", "teleoperation", "sim-to-real",
    "gaussian", "radiance field", "depth", "visual odometry", "tracking",
]

reg = {}
for l in open("papers/library/registry.jsonl", encoding="utf-8"):
    if l.strip():
        d = json.loads(l)
        reg[d["id"].split(":")[-1].split("v")[0]] = d

rss = [json.loads(l) for l in open("data/raw/2026-11-18_all.jsonl", encoding="utf-8") if l.strip()]
byid = {r["base_id"]: r for r in rss}
newday = json.load(open("data/newday_1118.json", encoding="utf-8"))


def announce_type(r):
    m = re.search(r"Announce Type:\s*(\w+)", r.get("abstract", ""))
    return m.group(1) if m else "NA"


def clean_abs(a):
    return re.sub(r"^arXiv:\S+\s+Announce Type:\s*\w+\s+Abstract:\s*", "", a).strip()


pool = {p: byid[p] for p in newday if p in byid}
print(f"11-17 公告组 {len(pool)}/{len(newday)} 有 RSS 摘要，覆盖率 {len(pool)/len(newday):.4f}", flush=True)

# --- 第一/二层：RSS 关键词层（KW 全称 + 缩写边界）---
xr, nonxr = {}, {}
for p, r in pool.items():
    txt = r["title"] + " " + clean_abs(r["abstract"])
    rec = {
        "day": "2026-11-17",
        "cat": r["primary_category"],
        "title": r["title"],
        "abstract": clean_abs(r["abstract"]),
        "announce": announce_type(r),
        "published_rss": r["published"][:10],
        "in_registry": p in reg,
    }
    if kw_match(txt):
        rec["recall"] = "KW"
        xr[p] = rec
    else:
        nonxr[p] = rec

# --- 第三层：标题级扩展词补扫（仅标题，计入 title_extra 标记）---
extra_hits = []
for p, rec in list(nonxr.items()):
    t = rec["title"].lower()
    hits = [w for w in EXTRA if w in t]
    if hits:
        rec["recall"] = "TITLE_EXTRA:" + ",".join(hits[:4])
        xr[p] = rec
        extra_hits.append((p, rec["title"][:70], hits[:3]))
        del nonxr[p]

print(f"\n## 摘要级 KW 命中 {sum(1 for v in xr.values() if v['recall']=='KW')} 篇")
print(f"## 标题级扩展词补扫新增 {len(extra_hits)} 篇（不计入 RSS 漏网统计）")
for p, t, h in extra_hits:
    print(f"   + {p} {t} [{h}]")

print(f"\n## 11-17 公告组 XR 池合计 {len(xr)} 篇 / 非 XR {len(nonxr)} 篇")
for p, v in sorted(xr.items(), key=lambda kv: kv[1]["cat"]):
    print(f"  {p} [{v['cat']}] {v['announce']:7s} pub={v['published_rss']} {v['title'][:82]}")

# --- replace 旧稿（backfill 候选）---
old = {}
for r in rss:
    if announce_type(r) != "replace":
        continue
    p = r["base_id"]
    if p in reg:
        continue
    txt = r["title"] + " " + clean_abs(r["abstract"])
    if kw_match(txt):
        old[p] = {
            "cat": r["primary_category"], "title": r["title"],
            "abstract": clean_abs(r["abstract"]), "announce": "replace",
            "published_rss": r["published"][:10], "in_registry": False,
        }
print(f"\n## replace 旧稿未入馆 {sum(1 for r in rss if announce_type(r)=='replace')} 篇 → XR 命中 {len(old)} 篇（backfill 候选）")
for p, v in sorted(old.items()):
    print(f"  {p} [{v['cat']}] {v['title'][:82]}")

json.dump(xr, open("data/xr_pool_1118.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
json.dump(old, open("data/old_replace_1118.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
json.dump(nonxr, open("data/nonxr_1118.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("\nsaved data/xr_pool_1118.json", len(xr), "| old_replace", len(old), "| nonxr", len(nonxr))
