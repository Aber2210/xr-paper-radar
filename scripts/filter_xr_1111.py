"""2026-11-11 摘要级 XR 过滤：11-10 新公告组（全量候选）+ 11-09 上批组（漏网复核）。

输入：
  data/newday_1111.json         {id: [cat, title]}   11-10 组 868 篇（全部未入馆）
  data/missed_listing_1111.json {id: [cat, title]}   11-09 组未入馆 362 篇
输出：
  data/missed_new_1111_xr.json   11-10 组摘要级 XR 命中（含摘要）
  data/missed_prev_1111_xr.json  11-09 组未入馆者摘要级 XR 命中（漏网复核）
"""
import json, sys, time, urllib.request, urllib.parse
from xml.etree import ElementTree as ET
sys.path.insert(0, "scripts")
from fetch_rss import kw_match

UA = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
NS = {"atom": "http://www.w3.org/2005/Atom", "arxiv": "http://arxiv.org/schemas/atom"}


def fetch_meta(ids):
    meta = {}
    for i in range(0, len(ids), 90):
        chunk = ids[i:i + 90]
        q = urllib.parse.quote(" OR ".join(f"id:{p}" for p in chunk), safe="")
        url = f"https://export.arxiv.org/api/query?search_query={q}&max_results=90"
        ok = False
        for attempt in range(4):
            try:
                req = urllib.request.Request(url, headers={"User-Agent": UA})
                with urllib.request.urlopen(req, timeout=90) as r:
                    root = ET.fromstring(r.read())
                for e in root.findall("atom:entry", NS):
                    aid = (e.findtext("atom:id", "", NS) or "").split("/abs/")[-1]
                    base = aid.split("v")[0]
                    meta[base] = {
                        "title": " ".join((e.findtext("atom:title", "", NS) or "").split()),
                        "abstract": " ".join((e.findtext("atom:summary", "", NS) or "").split()),
                        "published": (e.findtext("atom:published", "", NS) or "")[:10],
                        "primary": (e.find("arxiv:primary_category", NS).get("category", "")
                                    if e.find("arxiv:primary_category", NS) is not None else ""),
                    }
                ok = True
                break
            except Exception as ex:
                wait = min(60, 5 * 2 ** attempt)
                print(f"  batch {i//90} attempt{attempt+1} FAIL {type(ex).__name__} 退避 {wait}s", flush=True)
                time.sleep(wait)
        if not ok:
            print(f"  batch {i//90} 最终失败", flush=True)
        print(f"  batch {i//90} ok meta={len(meta)}", flush=True)
        time.sleep(3)
    return meta


def main():
    newday = json.load(open("data/newday_1111.json", encoding="utf-8"))
    prev = json.load(open("data/missed_listing_1111.json", encoding="utf-8"))
    reg = set()
    for l in open("papers/library/registry.jsonl", encoding="utf-8"):
        if l.strip():
            reg.add(json.loads(l)["id"].split(":")[-1].split("v")[0])

    for label, pool, out in (("11-10 新公告组", newday, "data/missed_new_1111_xr.json"),
                             ("11-09 上批组（未入馆）", prev, "data/missed_prev_1111_xr.json")):
        ids = sorted(pool)
        print(f"\n=== {label}: {len(ids)} 篇 ===", flush=True)
        meta = fetch_meta(ids)
        print(f"meta fetched: {len(meta)}", flush=True)
        xr = {}
        for p in ids:
            v = pool[p]
            cat, title = v[0], v[1]
            m = meta.get(p)
            t = m["title"] if m else title
            ab = m["abstract"] if m else ""
            if kw_match(t + " " + ab):
                xr[p] = {"cat": cat, "title": t, "abstract": ab,
                         "published": (m or {}).get("published", ""),
                         "in_registry": p in reg}
        for p, v in sorted(xr.items(), key=lambda kv: kv[1]["cat"]):
            print(f"  {p} [{v['cat']}] reg={v['in_registry']} pub={v['published']} {v['title'][:92]}", flush=True)
        print(f"{label} 摘要级 XR 命中 {len(xr)} 篇", flush=True)
        json.dump(xr, open(out, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
        print("saved", out, flush=True)


if __name__ == "__main__":
    main()
