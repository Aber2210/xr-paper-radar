"""2026-11-18 候选提交日核验（arXiv API id_list，分批 13 篇 + 12s 间隔，规避 429 静默丢批）。"""
import json, time, urllib.parse, urllib.request
from xml.etree import ElementTree as ET

UA = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
NS = {"atom": "http://www.w3.org/2005/Atom", "arxiv": "http://arxiv.org/schemas/atom"}
IDS = ['2611.18679', '2611.18708', '2611.18734', '2611.18822', '2611.18894', '2611.18979', '2611.19095', '2611.19096', '2611.19429', '2611.19765', '2611.19771', '2611.19773', '2611.19803', '2611.20083', '2611.20196', '2611.20245', '2611.20283', '2611.20533', '2611.20546', '2611.20568', '2611.20570', '2611.20797', '2611.20879', '2611.20950', '2611.21044', '2611.21060', '2611.21143', '2611.21233', '2611.21253', '2611.21334', '2611.21383', '2611.21479', '2611.21485', '2511.16349', '2605.05712', '2605.09586', '2607.03875', '2609.31117', '2611.18267']
CHUNK = 13

out = {}
for s in range(0, len(IDS), CHUNK):
    part = IDS[s:s + CHUNK]
    q = urllib.parse.quote(" OR ".join(f"id:{i}" for i in part), safe="")
    url = f"https://export.arxiv.org/api/query?search_query={q}&max_results={len(part)}"
    for attempt in range(3):
        try:
            raw = urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent": UA}), timeout=120).read()
            root = ET.fromstring(raw)
            break
        except Exception as e:
            print("  retry", attempt, e, flush=True)
            time.sleep(min(60, 6 * 2 ** attempt))
    else:
        continue
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
    print(f"batch {s//CHUNK+1}: 累计 {len(out)}/{len(IDS)}", flush=True)
    time.sleep(12)

print(f"API 返回 {len(out)}/{len(IDS)}")
for i in IDS:
    v = out.get(i)
    print(f"  {i} " + (f"pub={v['published']} upd={v['updated']} {v['primary']:10s} {v['title'][:60]}" if v else "MISSING"))
json.dump(out, open("data/published_1118.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("MISSING_IDS", [i for i in IDS if i not in out])
