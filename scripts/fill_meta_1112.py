#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""补采 triage_1112 因 429 丢失的摘要批次（小批量 + 长间隔）。"""
import json
import time
import urllib.parse
import urllib.request
from xml.etree import ElementTree as ET

UA = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
NS = {"atom": "http://www.w3.org/2005/Atom", "arxiv": "http://arxiv.org/schemas/atom"}
API = "https://export.arxiv.org/api/query"

meta = json.load(open("data/meta_1112.json", encoding="utf-8"))
newpool = json.load(open("data/newday_1112.json", encoding="utf-8"))
prevpool = json.load(open("data/missed_listing_1112.json", encoding="utf-8"))
missing = sorted((set(newpool) | set(prevpool)) - set(meta))
print("missing", len(missing), flush=True)

for i in range(0, len(missing), 50):
    chunk = missing[i:i + 50]
    q = urllib.parse.quote(" OR ".join(f"id:{p}" for p in chunk), safe="")
    url = f"{API}?search_query={q}&max_results=50"
    ok = False
    for attempt in range(6):
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
            wait = min(120, 10 * 2 ** attempt)
            print(f"  chunk {i // 50} attempt{attempt + 1} {type(ex).__name__} 退避 {wait}s", flush=True)
            time.sleep(wait)
    print(f"  chunk {i // 50} ok={ok} 累计 {len(meta)}", flush=True)
    json.dump(meta, open("data/meta_1112.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    time.sleep(12)

still = sorted((set(newpool) | set(prevpool)) - set(meta))
print("still missing", len(still), still[:20], flush=True)
