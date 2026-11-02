"""分析 RSS KW 命中集合：前缀分布、registry 去重、旧稿 replace/cross 识别。"""
import json
from collections import Counter

raw = []
for l in open("data/raw/2026-11-03.jsonl", encoding="utf-8"):
    if l.strip():
        raw.append(json.loads(l))
reg = set()
for l in open("papers/library/registry.jsonl", encoding="utf-8"):
    if l.strip():
        d = json.loads(l); reg.add(d["id"].split(":")[-1].split("v")[0])

print("KW hits:", len(raw), " registry:", len(reg))
pref = Counter(r["base_id"].split(".")[0] for r in raw)
print("prefix dist:", dict(sorted(pref.items())))
new = [r for r in raw if r["base_id"] not in reg]
print("not in registry:", len(new))
for r in sorted(new, key=lambda x: x["base_id"]):
    print(f"  {r['base_id']} [{r.get('primary_category','?')}] {r.get('title','')[:95]}")
print()
old = [r for r in raw if r["base_id"] in reg]
print("in registry (v2 re-announce or cross-listed):", len(old))
for r in sorted(old, key=lambda x: x["base_id"]):
    print(f"  {r['base_id']} {r.get('title','')[:80]}")
