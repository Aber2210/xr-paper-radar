# -*- coding: utf-8 -*-
"""2026-10-03 探针：API/RSS 可达性 + 上游最新提交日 + 磁盘空间。"""
import urllib.request, json, re, shutil, datetime, sys

UA = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                    "(KHTML, like Gecko) Chrome/120.0 Safari/537.36"}

def get(url, timeout=25, retries=2):
    last = None
    for i in range(retries):
        try:
            req = urllib.request.Request(url, headers=UA)
            with urllib.request.urlopen(req, timeout=timeout) as r:
                return r.status, r.read().decode("utf-8", "replace")
        except Exception as e:
            last = e
            import time; time.sleep(2*(i+1))
    return None, str(last)

print("=== DISK ===")
for d in ("C:/", "D:/"):
    try:
        du = shutil.disk_usage(d)
        print(f"{d} free={round(du.free/1e9,2)}GB total={round(du.total/1e9,2)}GB")
    except Exception as e:
        print(d, "ERR", e)

print("\n=== API probe: export.arxiv.org ===")
api_url = ("https://export.arxiv.org/api/query?search_query=all:electron"
           "&start=0&max_results=5&sortBy=submittedDate&sortOrder=descending")
st, body = get(api_url)
print("status:", st, "(len", len(body), ")")
if st == 200:
    dates = re.findall(r"<published>([^<]+)</published>", body)
    print("top-5 published:", dates[:5])
else:
    print("API error:", body[:300])

print("\n=== API probe: arxiv.org/api/query (alt) ===")
api2 = ("https://arxiv.org/api/query?search_query=all:electron"
        "&start=0&max_results=5&sortBy=submittedDate&sortOrder=descending")
st2, body2 = get(api2)
print("status:", st2, "(len", len(body2), ")")
if st2 == 200:
    dates2 = re.findall(r"<published>([^<]+)</published>", body2)
    print("top-5 published:", dates2[:5])

print("\n=== RSS probe: rss.arxiv.org/rss/cs.CV ===")
st3, body3 = get("https://rss.arxiv.org/rss/cs.CV")
print("status:", st3, "(len", len(body3), ")")
if st3 == 200:
    items = re.findall(r"<item>(.*?)</item>", body3, re.S)
    print("items:", len(items))
    if items:
        d0 = re.search(r"<pubDate>(.*?)</pubDate>", items[0], re.S)
        print("first pubDate:", d0.group(1) if d0 else None)
