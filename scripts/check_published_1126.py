# -*- coding: utf-8 -*-
"""核验 63 篇（主批 55 + backfill 8）的 arXiv published/updated 与 primary_category。

按 50 id/批 + 12s 间隔查 id_list，避免 429 静默丢批（2026-11-12 踩坑）。
输出 data/published_1126.json: id -> {published, updated, cat, title}
"""
import json, time, urllib.request, xml.etree.ElementTree as ET

NS = {"a": "http://www.w3.org/2005/Atom", "arxiv": "http://arxiv.org/schemas/atom"}
UA = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120.0 Safari/537.36"}

ids = open("data/_ids_1126_clean.txt", encoding="utf-8").read().split()
ids = [i.strip() for i in ids if i.strip()]
print("total ids", len(ids), flush=True)

out = {}
try:
    out = json.load(open("data/published_1126.json", encoding="utf-8"))
except Exception:
    pass

for k in range(0, len(ids), 25):
    chunk = ids[k:k + 25]
    url = "https://export.arxiv.org/api/query?id_list=%s&max_results=50" % ",".join(chunk)
    for attempt in range(4):
        try:
            req = urllib.request.Request(url, headers=UA)
            with urllib.request.urlopen(req, timeout=60) as r:
                root = ET.fromstring(r.read())
            break
        except Exception as e:
            wait = 12 * (attempt + 1)
            print("  retry", attempt + 1, e, "wait", wait, flush=True)
            time.sleep(wait)
    else:
        print("FAILED chunk", k, flush=True)
        continue
    got = 0
    for e in root.findall("a:entry", NS):
        aid = e.find("a:id", NS).text.split("/abs/")[-1]
        base = aid.split("v")[0]
        pc = e.find("arxiv:primary_category", NS)
        out[base] = {
            "published": e.find("a:published", NS).text[:10],
            "updated": e.find("a:updated", NS).text[:10],
            "cat": pc.get("term") if pc is not None else "",
            "title": " ".join(e.find("a:title", NS).text.split()),
        }
        got += 1
    print("chunk", k, "got", got, "/", len(chunk), flush=True)
    time.sleep(12)

missing = [i for i in ids if i not in out]
json.dump(out, open("data/published_1126.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("saved", len(out), "missing", missing, flush=True)
