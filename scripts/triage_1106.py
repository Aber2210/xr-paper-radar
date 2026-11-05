"""2026-11-06 甄别：RSS 37 命中 → 11-04 组真新 / 旧稿 replace-cross / 库内 v2。
真新 = base_id 在 11-05 公告组 listing 集合内；旧稿 = 不在 11-05 组且不在 registry；
库内 v2 = 在 registry。"""
import json

reg = {}
for l in open("papers/library/registry.jsonl", encoding="utf-8"):
    if l.strip():
        d = json.loads(l)
        reg[d["id"].split(":")[-1].split("v")[0]] = d

newday = json.load(open("data/audit_1106_newday.json", encoding="utf-8"))
g1105 = set()
for day, items in newday.items():
    g1105.update(items)
print("11-05 公告组 listing 唯一论文:", len(g1105))

abs_hits = json.load(open("data/missed_xr_abstract_1106.json", encoding="utf-8"))
g1105_abs = {p for p, v in abs_hits.items() if v["day"] == "2026-11-05"}
print("11-05 组摘要级 XR 命中:", len(g1105_abs))

recs = [json.loads(l) for l in open("data/raw/2026-11-06.jsonl", encoding="utf-8") if l.strip()]
print("RSS KW 命中:", len(recs))

true_new, old_reann, v2 = [], [], []
for r in recs:
    b = r["base_id"]
    if b in g1105:
        true_new.append(r)
    elif b in reg:
        v2.append(r)
    else:
        old_reann.append(r)

print(f"\n真新（11-05 组）: {len(true_new)}")
for r in true_new:
    print(f"  {r['base_id']} [{r['primary_category']}] {r['title'][:90]}")
print(f"\n旧稿 replace/cross: {len(old_reann)}")
for r in old_reann:
    print(f"  {r['base_id']} [{r['primary_category']}] {r['title'][:90]}")
print(f"\n库内 v2: {len(v2)}")
for r in v2:
    print(f"  {r['base_id']} [{r['primary_category']}] {r['title'][:90]}")

# 两渠道互证：listing 摘要级 11-04 命中 vs RSS 真新
tn_ids = {r["base_id"] for r in true_new}
print(f"\n互证: listing摘要级命中中不在RSS真新的: {sorted(g1105_abs - tn_ids)}")
print(f"互证: RSS真新中不在listing摘要级命中的: {sorted(tn_ids - g1105_abs)}")

json.dump([r["base_id"] for r in true_new], open("data/truenew_1106.json", "w", encoding="utf-8"))
json.dump([r["base_id"] for r in old_reann], open("data/oldcand_1106.json", "w", encoding="utf-8"))
