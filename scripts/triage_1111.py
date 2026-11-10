"""2026-11-11 甄别：RSS 77 命中 → 11-10 组真新 / 旧稿 replace-cross / 库内 v2。
真新 = base_id 在 11-10 公告组 listing 集合内；旧稿 = 不在 11-10 组且不在 registry；
库内 v2 = 在 registry。"""
import json

reg = {}
for l in open("papers/library/registry.jsonl", encoding="utf-8"):
    if l.strip():
        d = json.loads(l)
        reg[d["id"].split(":")[-1].split("v")[0]] = d

g1110 = set(json.load(open("data/newday_1111.json", encoding="utf-8")).keys())
print("11-10 公告组 listing 唯一论文:", len(g1110), flush=True)

abs_hits = json.load(open("data/missed_new_1111_xr.json", encoding="utf-8"))
print("11-10 组摘要级 XR 命中:", len(abs_hits), flush=True)

recs = [json.loads(l) for l in open("data/raw/2026-11-11.jsonl", encoding="utf-8") if l.strip()]
print("RSS KW 命中:", len(recs), flush=True)

true_new, old_reann, v2 = [], [], []
for r in recs:
    b = r["base_id"]
    if b in g1110:
        true_new.append(r)
    elif b in reg:
        v2.append(r)
    else:
        old_reann.append(r)

print(f"\n真新（11-10 组）: {len(true_new)}")
for r in true_new:
    print(f"  {r['base_id']} [{r.get('primary_category','')}] {r['title'][:92]}")
print(f"\n旧稿 replace/cross（不在库）: {len(old_reann)}")
for r in old_reann:
    print(f"  {r['base_id']} [{r.get('primary_category','')}] {r['title'][:92]}")
print(f"\n库内 v2 再公告: {len(v2)}")
for r in v2:
    print(f"  {r['base_id']} [{r.get('primary_category','')}] {r['title'][:92]}")

tn_ids = {r["base_id"] for r in true_new}
ab_ids = set(abs_hits)
print(f"\n互证: listing摘要级命中的未在RSS真新: {sorted(ab_ids - tn_ids)}")
print(f"互证: RSS真新中未在listing摘要级命中: {sorted(tn_ids - ab_ids)}")

json.dump([r["base_id"] for r in true_new], open("data/truenew_1111.json", "w", encoding="utf-8"))
json.dump([r["base_id"] for r in old_reann], open("data/oldcand_1111.json", "w", encoding="utf-8"))
json.dump([r["base_id"] for r in v2], open("data/v2_1111.json", "w", encoding="utf-8"))
