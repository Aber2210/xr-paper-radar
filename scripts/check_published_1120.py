# -*- coding: utf-8 -*-
"""2026-11-20 提交日核验：逐篇查 arXiv API published/updated（ID 前缀 ≠ 提交月份，必须实查）。"""
import json, re, time, urllib.request, urllib.parse
from xml.etree import ElementTree as ET

IDS = ("2611.23416,2611.23417,2611.23450,2611.23513,2611.23534,2611.23554,2611.23575,2611.23670,"
       "2611.23736,2611.23825,2611.23871,2611.23935,2611.23939,2611.23970,2611.23994,2611.24193,"
       "2611.24207,2611.24334,2611.24404,2611.24565,2611.24616,2611.24731,2611.24805,2611.24938,"
       "2611.24941,2511.18173,2606.07179,2607.08514").split(",")
NS = {"atom": "http://www.w3.org/2005/Atom", "arxiv": "http://arxiv.org/schemas/atom"}
UA = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120.0 Safari/537.36"}
out = {}
for i in range(0, len(IDS), 13):
    batch = IDS[i:i + 13]
    url = "https://export.arxiv.org/api/query?id_list=%s&max_results=50" % ",".join(batch)
    for attempt in range(4):
        try:
            req = urllib.request.Request(url, headers=UA)
            with urllib.request.urlopen(req, timeout=90) as r:
                root = ET.fromstring(r.read())
            break
        except Exception as e:
            wait = min(120, 5 * 2 ** attempt)
            print(f"retry {attempt+1} after {wait}s ({e})", flush=True)
            time.sleep(wait)
    else:
        raise SystemExit("API FAILED batch %d" % i)
    n = 0
    for e in root.findall("atom:entry", NS):
        aid = e.findtext("atom:id", "", NS).split("/abs/")[-1]
        base = aid.split("v")[0]
        pc = e.find("arxiv:primary_category", NS)
        out[base] = {
            "published": (e.findtext("atom:published", "", NS) or "")[:10],
            "updated": (e.findtext("atom:updated", "", NS) or "")[:10],
            "cat": pc.get("term") if pc is not None else "",
            "version": aid.split("v")[-1] if "v" in aid else "",
        }
        n += 1
    print(f"batch {i//13+1}: got {n}", flush=True)
    time.sleep(12)
missing = [x for x in IDS if x not in out]
print("missing:", missing)
json.dump(out, open("data/published_1120.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
for k in IDS:
    v = out.get(k, {})
    print(k, v.get("published"), v.get("updated"), v.get("cat"), v.get("version"))
