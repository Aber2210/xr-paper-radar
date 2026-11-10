"""2026-11-11 候选池摘要速览（供人工甄别 XR 相关度）。"""
import json

recs = {r["base_id"]: r for r in (json.loads(l) for l in open("data/raw/2026-11-11.jsonl", encoding="utf-8") if l.strip())}
tn = json.load(open("data/truenew_1111.json", encoding="utf-8"))
old = json.load(open("data/oldcand_1111.json", encoding="utf-8"))

out = []
out.append(f"### 真新候选 {len(tn)} 篇（11-10 公告组）")
for i, b in enumerate(tn, 1):
    r = recs[b]
    out.append(f"\n[{i}] {b} | {r.get('primary_category','')} | {r.get('published','')[:10]}")
    out.append(f"T: {r['title']}")
    out.append(f"A: {r.get('abstract','')[:520]}")
out.append(f"\n\n### 旧稿 replace/cross {len(old)} 篇（backfill 候选）")
for i, b in enumerate(old, 1):
    r = recs[b]
    out.append(f"\n[{i}] {b} | {r.get('primary_category','')} | {r.get('published','')[:10]}")
    out.append(f"T: {r['title']}")
    out.append(f"A: {r.get('abstract','')[:420]}")
txt = "\n".join(out)
open("data/cands_1111_dump.txt", "w", encoding="utf-8").write(txt)
print(txt[:200])
print("saved data/cands_1111_dump.txt", len(txt))
