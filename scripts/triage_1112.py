#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""2026-11-12 对账第二层：listing 日组摘要级 XR 过滤。

池 A：newday_1112.json（11-11 新公告组全部条目，436 篇唯一）
池 B：missed_listing_1112.json（11-10 上批公告组未入馆 837 篇，复核 0 漏网）

输出：
  data/meta_1112.json            两池全部条目的 title/abstract/published/primary
  data/missed_new_1112_xr.json   11-11 组摘要级 XR 命中（含 abstract）
  data/missed_prev_1112_xr.json  11-10 组未入馆者摘要级 XR 命中（用于 0 漏网判定）
"""
import json
import sys
import time
import urllib.parse
import urllib.request
from xml.etree import ElementTree as ET

sys.path.insert(0, "scripts")
from fetch_rss import kw_match  # noqa: E402

UA = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
NS = {"atom": "http://www.w3.org/2005/Atom", "arxiv": "http://arxiv.org/schemas/atom"}
API = "https://export.arxiv.org/api/query"


def load_pool(path, key_mode="list"):
    raw = json.load(open(path, encoding="utf-8"))
    pool = {}
    for p, v in raw.items():
        if key_mode == "list":
            cat, title = v[0], v[1]
        else:
            cat, title = v.get("cat", ""), v.get("title", "")
        pool[p] = {"cat": cat, "title": title}
    return pool


def fetch_meta(ids):
    meta = {}
    for i in range(0, len(ids), 100):
        chunk = ids[i:i + 100]
        q = urllib.parse.quote(" OR ".join(f"id:{p}" for p in chunk), safe="")
        url = f"{API}?search_query={q}&max_results=100"
        ok = False
        for attempt in range(4):
            try:
                req = urllib.request.Request(url, headers={"User-Agent": UA})
                with urllib.request.urlopen(req, timeout=90) as r:
                    root = ET.fromstring(r.read())
                for e in root.findall("atom:entry", NS):
                    aid = (e.findtext("atom:id", "", NS) or "").split("/abs/")[-1]
                    base = aid.split("v")[0]
                    pc = e.find("arxiv:primary_category", NS)
                    meta[base] = {
                        "title": " ".join((e.findtext("atom:title", "", NS) or "").split()),
                        "abstract": " ".join((e.findtext("atom:summary", "", NS) or "").split()),
                        "published": (e.findtext("atom:published", "", NS) or "")[:10],
                        "primary": pc.get("category", "") if pc is not None else "",
                    }
                ok = True
                break
            except Exception as ex:
                wait = min(60, 5 * 2 ** attempt)
                print(f"  batch {i // 100} attempt{attempt + 1} FAIL {type(ex).__name__}: {ex} 退避 {wait}s", flush=True)
                time.sleep(wait)
        if not ok:
            print(f"  batch {i // 100} 最终失败", flush=True)
        print(f"  meta batch {i // 100}: 累计 {len(meta)}", flush=True)
        time.sleep(3)
    return meta


def main():
    reg = set()
    for line in open("papers/library/registry.jsonl", encoding="utf-8"):
        if line.strip():
            d = json.loads(line)
            reg.add(d["id"].split(":")[-1].split("v")[0])

    newpool = load_pool("data/newday_1112.json")
    prevpool = load_pool("data/missed_listing_1112.json")
    print(f"registry={len(reg)}  newpool={len(newpool)}  prevpool={len(prevpool)}", flush=True)

    allids = sorted(set(newpool) | set(prevpool))
    meta = fetch_meta(allids)
    print(f"meta fetched: {len(meta)}/{len(allids)}", flush=True)
    json.dump(meta, open("data/meta_1112.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)

    def build(pool, label):
        hits = {}
        for p, info in pool.items():
            m = meta.get(p, {})
            title = m.get("title") or info["title"]
            abs_ = m.get("abstract", "")
            if kw_match(title + " " + abs_):
                hits[p] = {
                    "cat": info["cat"],
                    "title": title,
                    "abstract": abs_,
                    "published": m.get("published", ""),
                    "primary": m.get("primary", ""),
                    "in_registry": p in reg,
                }
        print(f"\n## {label}: 摘要级 XR 命中 {len(hits)}/{len(pool)}", flush=True)
        for p, v in sorted(hits.items()):
            print(f"  {p} [{v['cat']}] reg={v['in_registry']} pub={v['published']} {v['title'][:80]}", flush=True)
        return hits

    newxr = build(newpool, "11-11 新公告组")
    prevxr = build(prevpool, "11-10 上批组未入馆")
    json.dump(newxr, open("data/missed_new_1112_xr.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    json.dump(prevxr, open("data/missed_prev_1112_xr.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print("\nsaved data/missed_new_1112_xr.json  data/missed_prev_1112_xr.json", flush=True)


if __name__ == "__main__":
    main()
