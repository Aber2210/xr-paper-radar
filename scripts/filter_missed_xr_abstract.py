import json, re, time, sys, urllib.request, urllib.parse
sys.path.insert(0, "scripts")
from fetch_rss import kw_match
from xml.etree import ElementTree as ET

UA = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
NS = {"atom": "http://www.w3.org/2005/Atom", "arxiv": "http://arxiv.org/schemas/atom"}

missed = json.load(open(sys.argv[1] if len(sys.argv)>1 else "data/missed_listing.json", encoding="utf-8"))
MIN_DAY = sys.argv[2] if len(sys.argv)>2 else "2026-10-16"
OUT = sys.argv[3] if len(sys.argv)>3 else "data/missed_xr_abstract.json"
reg = set()
for l in open("papers/library/registry.jsonl", encoding="utf-8"):
    if l.strip():
        d = json.loads(l); reg.add(d["id"].split(":")[-1].split("v")[0])

# 汇总窗口内全部漏网 id（含标题，按日）
pool = {}   # id -> {"day":..., "cat":..., "title":...}
for day, items in missed.items():
    if day < MIN_DAY:
        continue
    for p, v in items.items():
        t = v["title"]
        if isinstance(t, list):
            t = t[1] if len(t) > 1 else ""
        pool[p] = {"day": day, "cat": v["cat"], "title": t}
ids = sorted(pool)
print(f"pool: {len(ids)} 篇（day>={MIN_DAY}），registry 已有 {sum(1 for p in pool if p in reg)} 篇", flush=True)

# 分批经 API 取摘要（id_list，100/批）
meta = {}
for i in range(0, len(ids), 100):
    chunk = ids[i:i+100]
    q = urllib.parse.quote(" OR ".join(f"id:{p}" for p in chunk), safe="")
    url = f"https://export.arxiv.org/api/query?search_query={q}&max_results=100"
    ok = False
    for attempt in range(4):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": UA})
            with urllib.request.urlopen(req, timeout=60) as r:
                root = ET.fromstring(r.read())
            for e in root.findall("atom:entry", NS):
                aid = (e.findtext("atom:id", "", NS) or "").split("/abs/")[-1]
                base = aid.split("v")[0]
                meta[base] = {
                    "title": " ".join((e.findtext("atom:title", "", NS) or "").split()),
                    "abstract": " ".join((e.findtext("atom:summary", "", NS) or "").split()),
                    "published": (e.findtext("atom:published", "", NS) or "")[:10],
                    "primary": e.find("arxiv:primary_category", NS).get("category", "") if e.find("arxiv:primary_category", NS) is not None else "",
                }
            ok = True
            break
        except Exception as ex:
            wait = min(60, 5 * 2 ** attempt)
            print(f"  batch {i//100} attempt{attempt+1} FAIL {type(ex).__name__}，退避 {wait}s", flush=True)
            time.sleep(wait)
    if not ok:
        print(f"  batch {i//100} 最终失败", flush=True)
    time.sleep(3)

print(f"meta fetched: {len(meta)}", flush=True)

# 摘要级 XR 过滤（KW 全称 + 缩写词边界）
xr = {}
for p, info in pool.items():
    m = meta.get(p)
    title = m["title"] if m else info["title"]
    abs_ = m["abstract"] if m else ""
    if kw_match(title + " " + abs_):
        xr[p] = {"day": info["day"], "cat": info["cat"], "title": title,
                 "abstract": abs_, "published": (m or {}).get("published", ""),
                 "in_registry": p in reg}
for day in sorted({v["day"] for v in xr.values()}):
    sub = {p: v for p, v in xr.items() if v["day"] == day}
    print(f"\n## {day}：摘要级 XR 命中 {len(sub)} 篇", flush=True)
    for p, v in sorted(sub.items()):
        print(f"  {p} [{v['cat']}] reg={v['in_registry']} {v['title'][:88]}", flush=True)
print(f"\n合计摘要级 XR 命中 {len(xr)} 篇", flush=True)
json.dump(xr, open(OUT, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("saved", OUT, flush=True)
