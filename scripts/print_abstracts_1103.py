"""打印 30 篇未入馆候选的摘要到文件，供 XR 甄别（主批 21 + 旧稿 9）。"""
import json

raw = []
for l in open("data/raw/2026-11-03.jsonl", encoding="utf-8"):
    if l.strip():
        raw.append(json.loads(l))
reg = set()
for l in open("papers/library/registry.jsonl", encoding="utf-8"):
    if l.strip():
        d = json.loads(l); reg.add(d["id"].split(":")[-1].split("v")[0])
new = [r for r in raw if r["base_id"] not in reg]
with open("data/abstracts_1103.txt", "w", encoding="utf-8") as f:
    for r in sorted(new, key=lambda x: x["base_id"]):
        f.write("="*100 + "\n")
        f.write(f"{r['base_id']} [{r['primary_category']}] {r['title']}\n")
        f.write(f"published={r.get('published','')} cats={r.get('categories','')}\n")
        f.write(r.get("abstract","")[:1500] + "\n")
print("written data/abstracts_1103.txt", len(new), "papers")
