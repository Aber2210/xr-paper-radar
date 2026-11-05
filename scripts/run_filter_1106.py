"""2026-11-06：把 audit 输出转为 filter_missed_xr_abstract.py 需要的 day->{id:{cat,title}} 结构，
对 11-04 组（漏网复核）与 11-05 组（新公告日）一起跑 API 摘要级 XR 过滤。"""
import json, subprocess, sys

missed = json.load(open("data/missed_listing_1106.json", encoding="utf-8"))      # 11-03 组未入馆 id->[cat,title]
newday = json.load(open("data/audit_1106_newday.json", encoding="utf-8"))        # {"2026-11-04": {id:[cat,title]}}

pool = {"2026-11-04": {}, "2026-11-05": {}}
for p, v in missed.items():
    pool["2026-11-04"][p] = {"cat": v[0], "title": v[1]}
for day, items in newday.items():
    for p, v in items.items():
        pool.setdefault(day, {})[p] = {"cat": v[0], "title": v[1]}

print({d: len(v) for d, v in pool.items()}, flush=True)
json.dump(pool, open("data/missed_listing_1106_days.json", "w", encoding="utf-8"), ensure_ascii=False)

# 直接内联复用 filter_missed_xr_abstract.py 的 main 逻辑（通过命令行调用）
r = subprocess.run([sys.executable, "scripts/filter_missed_xr_abstract.py",
                    "data/missed_listing_1106_days.json", "2026-11-04",
                    "data/missed_xr_abstract_1106.json"],
                   cwd=".", capture_output=True, text=True, encoding="utf-8")
print(r.stdout[-12000:])
if r.stderr:
    print("STDERR:", r.stderr[-3000:])
