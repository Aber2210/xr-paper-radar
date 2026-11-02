"""把 audit_1103_newday.json 的 {day:{id:[cat,title]}} 转成 filter_missed_xr_abstract.py
需要的 {day:{id:{title,cat}}} 格式（仅 11-02 组），并合并 10-30 组复采结果用于二次核验。"""
import json

newday = json.load(open("data/audit_1103_newday.json", encoding="utf-8"))
out = {}
for day, papers in newday.items():
    if day != "2026-11-02":
        continue
    out[day] = {}
    for p, v in papers.items():
        out[day][p] = {"title": v[1], "cat": v[0]}
json.dump(out, open("data/missed_listing_1103_newday.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("11-02 group papers:", sum(len(v) for v in out.values()))

# 10-30 组（missed_listing_1103.json 是 {id:[cat,title]} 平铺格式）转日组格式
m = json.load(open("data/missed_listing_1103.json", encoding="utf-8"))
g30 = {"2026-10-30": {p: {"title": v[1], "cat": v[0]} for p, v in m.items()}}
json.dump(g30, open("data/missed_listing_1103_g30.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("10-30 group unregistered papers:", len(m))
