"""2026-11-09（周一凌晨状态日）：把 audit 输出转为 filter_missed_xr_abstract.py 需要的
day->{id:{cat,title}} 结构，对 11-06 组未入馆 363 篇跑 API 摘要级 XR 过滤（漏网复核）。"""
import json, subprocess, sys

missed = json.load(open("data/missed_listing_1109.json", encoding="utf-8"))      # 11-06 组未入馆 id->[cat,title]

pool = {"2026-11-06": {}}
for p, v in missed.items():
    pool["2026-11-06"][p] = {"cat": v[0], "title": v[1]}

print({d: len(v) for d, v in pool.items()}, flush=True)
json.dump(pool, open("data/missed_listing_1109_days.json", "w", encoding="utf-8"), ensure_ascii=False)

r = subprocess.run([sys.executable, "scripts/filter_missed_xr_abstract.py",
                    "data/missed_listing_1109_days.json", "2026-11-06",
                    "data/missed_xr_abstract_1109.json"],
                   cwd=".", capture_output=True, text=True, encoding="utf-8")
print(r.stdout[-12000:])
if r.stderr:
    print("STDERR:", r.stderr[-3000:])
