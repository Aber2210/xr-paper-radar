"""2026-11-13 漏网复核：对 11-11 公告组未入馆条目跑 API 摘要级 XR 过滤。

改进（沿用 11-12 教训）：id_list 批量 50 条/批 + 12s 间隔 + 覆盖率校验 +
缺失 id 二次补采，避免 429 静默丢批导致摘要级过滤退化为标题级。
"""
import json, sys, time, urllib.parse, urllib.request
sys.path.insert(0, "scripts")
from fetch_rss import kw_match
from xml.etree import ElementTree as ET

UA = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
NS = {"atom": "http://www.w3.org/2005/Atom", "arxiv": "http://arxiv.org/schemas/atom"}

MISSED = "data/missed_listing_1113.json"
DAY = "2026-11-11"
OUT = "data/missed_xr_abstract_1113.json"

missed = json.load(open(MISSED, encoding="utf-8"))
reg = set()
for l in open("papers/library/registry.jsonl", encoding="utf-8"):
    if l.strip():
        d = json.loads(l)
        reg.add(d["id"].split(":")[-1].split("v")[0])

pool = {}
for p, v in missed.items():
    pool[p] = {"day": DAY, "cat": v[0], "title": v[1]}
ids = sorted(pool)
print(f"pool: {len(ids)} 篇（{DAY} 组未入馆），registry 已有 {sum(1 for p in pool if p in reg)} 篇", flush=True)


def fetch(chunk, tag):
    q = urllib.parse.quote(" OR ".join(f"id:{p}" for p in chunk), safe="")
    url = f"https://export.arxiv.org/api/query?search_query={q}&max_results={len(chunk)}"
    for attempt in range(4):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": UA})
            with urllib.request.urlopen(req, timeout=90) as r:
                root = ET.fromstring(r.read())
            got = {}
            for e in root.findall("atom:entry", NS):
                aid = (e.findtext("atom:id", "", NS) or "").split("/abs/")[-1]
                base = aid.split("v")[0]
                pc = e.find("arxiv:primary_category", NS)
                got[base] = {
                    "title": " ".join((e.findtext("atom:title", "", NS) or "").split()),
                    "abstract": " ".join((e.findtext("atom:summary", "", NS) or "").split()),
                    "published": (e.findtext("atom:published", "", NS) or "")[:10],
                    "primary": pc.get("category", "") if pc is not None else "",
                }
            return got
        except Exception as ex:
            wait = min(120, 5 * 2 ** attempt)
            print(f"  {tag} attempt{attempt+1} FAIL {type(ex).__name__}，退避 {wait}s", flush=True)
            time.sleep(wait)
    print(f"  {tag} 最终失败", flush=True)
    return {}


meta = {}
BATCH = 50
for i in range(0, len(ids), BATCH):
    chunk = ids[i:i + BATCH]
    got = fetch(chunk, f"batch{i//BATCH}")
    meta.update(got)
    print(f"  batch{i//BATCH}: want={len(chunk)} got={len(got)} cum={len(meta)}", flush=True)
    time.sleep(12)

missing = [p for p in ids if p not in meta]
print(f"meta fetched: {len(meta)}/{len(ids)} 覆盖率={len(meta)/len(ids):.4f} 缺失={len(missing)}", flush=True)
if missing:
    print("  二次补采缺失 id...", flush=True)
    for i in range(0, len(missing), BATCH):
        chunk = missing[i:i + BATCH]
        meta.update(fetch(chunk, f"retry{i//BATCH}"))
        time.sleep(12)
    missing = [p for p in ids if p not in meta]
    print(f"  补采后 meta={len(meta)}/{len(ids)} 覆盖率={len(meta)/len(ids):.4f} 仍缺={len(missing)}", flush=True)

xr = {}
for p, info in pool.items():
    m = meta.get(p)
    title = m["title"] if m else info["title"]
    abs_ = m["abstract"] if m else ""
    if kw_match(title + " " + abs_):
        xr[p] = {"day": info["day"], "cat": info["cat"], "title": title,
                 "abstract": abs_, "published": (m or {}).get("published", ""),
                 "in_registry": p in reg, "abstract_verified": p in meta}

print(f"\n## {DAY}：摘要级 XR 命中 {len(xr)} 篇", flush=True)
for p, v in sorted(xr.items()):
    print(f"  {p} [{v['cat']}] abs={v['abstract_verified']} reg={v['in_registry']} pub={v['published']} {v['title'][:86]}", flush=True)
json.dump(xr, open(OUT, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("saved", OUT, flush=True)
