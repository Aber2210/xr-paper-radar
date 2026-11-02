"""数据源探针：API 双主机 + RSS 7 分类连通性/新鲜度探测。"""
import urllib.request, time
UA = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120.0 Safari/537.36"}

def probe(url, name):
    try:
        req = urllib.request.Request(url, headers=UA)
        with urllib.request.urlopen(req, timeout=30) as r:
            data = r.read()
            return f"{name}: HTTP {r.status}, {len(data)} bytes"
    except Exception as e:
        return f"{name}: FAIL {type(e).__name__} {e}"

print(probe("https://arxiv.org/api/query?search_query=all:electron&max_results=1", "API arxiv.org"), flush=True)
print(probe("https://export.arxiv.org/api/query?search_query=all:electron&max_results=1", "API export"), flush=True)
for c in ["cs.CV","cs.GR","cs.HC","cs.MM","cs.RO","cs.AI","eess.IV"]:
    print(probe(f"https://rss.arxiv.org/rss/{c}", f"RSS {c}"), flush=True)
    time.sleep(1)
