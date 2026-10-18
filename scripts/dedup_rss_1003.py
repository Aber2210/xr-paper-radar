# -*- coding: utf-8 -*-
"""RSS 929 全量 vs registry：找出真正新提交（不在库内）的 2610.* ID，并看 pubDate 分布。"""
import json
from collections import Counter
RSS = "data/raw/2026-10-03_rss.jsonl"
REG = "papers/library/registry.jsonl"

rss = [json.loads(l) for l in open(RSS, encoding="utf-8") if l.strip()]
reg_ids = set()
for l in open(REG, encoding="utf-8"):
    l=l.strip()
    if not l: continue
    try: reg_ids.add(json.loads(l)["id"].split(":")[-1].split("v")[0])
    except: pass

# 字段探查
print("RSS sample keys:", list(rss[0].keys()))
# pubDate / published 字段
def pdate(r):
    return (r.get("published") or r.get("pubDate") or "")[:10]

pubs = Counter(pdate(r) for r in rss)
print("RSS pubDate 分布:", dict(sorted(pubs.items(), reverse=True)))

# 不在库内的
new = [r for r in rss if r["base_id"] not in reg_ids]
print("\n不在 registry 的 RSS 条目数:", len(new))
newpubs = Counter(pdate(r) for r in new)
print("其中 pubDate 分布:", dict(sorted(newpubs.items(), reverse=True)))
print("\n新 ID 列表（前 60）:")
for r in sorted(new, key=lambda x: pdate(x), reverse=True)[:60]:
    print(f"  {r['base_id']:14} {pdate(r):12} {r.get('title','')[:60]}")
# 是否都是 2610.* 还是混了旧稿
import re
prefix = Counter(re.match(r"(\d{4})\.", r["base_id"]).group(1) for r in new if re.match(r"\d{4}\.", r["base_id"]))
print("\n新 ID 年份前缀分布:", dict(prefix))
