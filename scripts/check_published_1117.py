"""2026-11-17 候选提交日核验（arXiv API id_list，单批 16 篇，远低于 50 上限）。"""
import json, urllib.parse, urllib.request
from xml.etree import ElementTree as ET

UA = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
NS = {"atom": "http://www.w3.org/2005/Atom", "arxiv": "http://arxiv.org/schemas/atom"}
IDS = ["2611.18438", "2611.18256", "2611.18170", "2611.18099", "2611.17957", "2611.17752",
       "2611.18340", "2611.17755", "2611.17458", "2611.17619", "2611.18243", "2611.17828",
       "2611.17903", "2501.12764", "2608.19372", "2611.17238"]

q = urllib.parse.quote(" OR ".join(f"id:{i}" for i in IDS), safe="")
url = f"https://export.arxiv.org/api/query?search_query={q}&max_results={len(IDS)}"
root = ET.fromstring(urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent": UA}), timeout=120).read())
out = {}
for e in root.findall("atom:entry", NS):
    aid = (e.findtext("atom:id", "", NS) or "").split("/abs/")[-1]
    base = aid.split("v")[0]
    pc = e.find("arxiv:primary_category", NS)
    out[base] = {
        "title": " ".join((e.findtext("atom:title", "", NS) or "").split()),
        "published": (e.findtext("atom:published", "", NS) or "")[:10],
        "updated": (e.findtext("atom:updated", "", NS) or "")[:10],
        "primary": pc.get("category", "") if pc is not None else "",
        "comment": " ".join((e.findtext("arxiv:comment", "", NS) or "").split()),
    }
print(f"API 返回 {len(out)}/{len(IDS)}")
for i in IDS:
    v = out.get(i)
    if v:
        print(f"  {i} pub={v['published']} upd={v['updated']} {v['primary']:10s} {v['title'][:66]}")
    else:
        print(f"  {i} MISSING")
json.dump(out, open("data/published_1117.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
