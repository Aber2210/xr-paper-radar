"""API id_list 核验候选论文的 submittedDate（RSS published 是公告时间戳，不可当提交日）。"""
import urllib.request, urllib.parse, time
from xml.etree import ElementTree as ET

UA = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120.0 Safari/537.36"}
NS = {"atom": "http://www.w3.org/2005/Atom", "arxiv": "http://arxiv.org/schemas/atom"}

IDS = [
    # 主批 XR 候选 11
    "2610.40760","2610.40832","2610.41011","2610.41127","2610.41496","2610.41501",
    "2610.41602","2610.41671","2610.41680","2610.41833","2610.41987",
    # backfill 候选 2
    "2511.11231","2602.21535",
]
q = urllib.parse.quote(" OR ".join(f"id:{p}" for p in IDS), safe="")
url = f"https://export.arxiv.org/api/query?search_query={q}&max_results=50"
for attempt in range(4):
    try:
        req = urllib.request.Request(url, headers=UA)
        with urllib.request.urlopen(req, timeout=60) as r:
            root = ET.fromstring(r.read())
        break
    except Exception as ex:
        wait = min(60, 5*2**attempt)
        print(f"attempt {attempt+1} FAIL {ex}, backoff {wait}s", flush=True)
        time.sleep(wait)
else:
    raise SystemExit("API failed")

for e in root.findall("atom:entry", NS):
    aid = (e.findtext("atom:id", "", NS) or "").split("/abs/")[-1]
    base = aid.split("v")[0]
    pub = (e.findtext("atom:published", "", NS) or "")[:10]
    upd = (e.findtext("atom:updated", "", NS) or "")[:10]
    prim = e.find("arxiv:primary_category", NS)
    prim = prim.get("term","") if prim is not None else ""
    title = " ".join((e.findtext("atom:title", "", NS) or "").split())
    print(f"{base} v={aid.split('v')[-1]} submitted={pub} updated={upd} [{prim}] {title[:70]}")
