import json, sys
sys.path.insert(0, "scripts")
from fetch_rss import KW

def norm_title(v):
    t = v.get("title", "")
    if isinstance(t, list):   # 审计脚本历史 bug：title 存成 [cat, title]
        t = t[1] if len(t) > 1 else ""
    return t

missed = json.load(open("data/missed_listing_1019.json", encoding="utf-8"))
print("=== 漏网论文 · XR 关键词标题过滤 ===")
tot_all = 0; tot_xr = 0
xr_all = {}
for day in sorted(missed):
    items = missed[day]
    xr = {p: {"cat": v["cat"], "title": norm_title(v)} for p, v in items.items()
          if any(k.lower() in norm_title(v).lower() for k in KW)}
    tot_all += len(items); tot_xr += len(xr)
    xr_all[day] = xr
    print(f"\n## {day}：全量漏网 {len(items)} 篇，其中标题命中 XR 关键词 {len(xr)} 篇")
    for p, v in sorted(xr.items(), key=lambda x: x[1]["cat"]):
        print(f"  [{v['cat']}] {p}  {v['title'][:76]}")
print(f"\n=== 合计：漏网 {tot_all} 篇；标题级 XR 相关 {tot_xr} 篇（标题口径为下限，摘要级通常更多）===")
json.dump(xr_all, open("data/missed_xr.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("saved data/missed_xr.json")
