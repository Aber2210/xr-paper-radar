"""把 audit_1104_newday.json 的 {day:{id:[cat,title]}} 转成 filter_missed_xr_abstract.py
需要的 {day:{id:{title,cat}}} 格式（11-03 新公告组 + 11-02 组未入馆复采二次核验）。"""
import json

newday = json.load(open("data/audit_1104_newday.json", encoding="utf-8"))
out = {}
for day, papers in newday.items():
    out[day] = {p: {"title": v[1], "cat": v[0]} for p, v in papers.items()}
json.dump(out, open("data/missed_listing_1104_newday.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("11-03 group papers:", len(out.get('2026-11-03', {})), "days:", list(out))

# 11-02 组未入馆（missed_listing_1104.json 是 {id:[cat,title]} 平铺）转日组格式
m = json.load(open("data/missed_listing_1104.json", encoding="utf-8"))
g = {"2026-11-02": {p: {"title": v[1], "cat": v[0]} for p, v in m.items()}}
json.dump(g, open("data/missed_listing_1104_g1102.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("11-02 group unregistered papers:", len(m))
