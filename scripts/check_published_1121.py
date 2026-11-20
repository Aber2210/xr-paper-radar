"""2026-11-21 提交日核验：逐篇查 arXiv API 的 published（首次提交）/updated。"""
import urllib.request, json, time, re, sys

ids = open("data/_ids_1121.txt").read().split(",")
UA = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120.0 Safari/537.36"}
out = {}
B = 20  # 50 id/批曾触发 429 静默丢批，改为 20
for i in range(0, len(ids), B):
    chunk = ids[i:i + B]
    url = "https://export.arxiv.org/api/query?id_list=" + ",".join(chunk) + "&max_results=100"
    data = None
    for n in range(4):
        try:
            req = urllib.request.Request(url, headers=UA)
            with urllib.request.urlopen(req, timeout=60) as r:
                data = r.read().decode("utf-8", "replace")
            break
        except Exception as e:
            wait = min(60, 5 * 2 ** n)
            print(f"  retry {n+1} after {wait}s ({e})", flush=True)
            time.sleep(wait)
    if not data:
        print("FATAL batch", i, flush=True)
        sys.exit(2)
    for ent in re.findall(r"<entry>(.*?)</entry>", data, re.S):
        m = re.search(r"<id>https?://arxiv.org/abs/([^<]+)</id>", ent)
        if not m:
            continue
        aid = m.group(1)
        base = aid.split("v")[0]
        pub = re.search(r"<published>([^<]+)</published>", ent)
        upd = re.search(r"<updated>([^<]+)</updated>", ent)
        out[base] = {"arxiv_id": aid, "published": pub.group(1)[:10] if pub else "",
                     "updated": upd.group(1)[:10] if upd else ""}
    time.sleep(6)
miss = [i for i in ids if i not in out]
print("queried", len(out), "missing", miss)
json.dump(out, open("data/published_1121.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
from collections import Counter
print(Counter(v["published"] for v in out.values()))
