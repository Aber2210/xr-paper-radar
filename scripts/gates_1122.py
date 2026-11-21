# -*- coding: utf-8 -*-
"""gates_1122.py — 2026-11-22 状态日：门③ 价值天花板基线现算（门①/② 不适用：0 候选）。

口径（任务书第 6 步 + b03 整改）：
  门③ 半开窗口 [today-30, today)，按 batch 剔除本次运行追加的批（本日为状态日，无追加批）。
  今日无新稿 → today_max = null、heavy_day_raw/blockbuster/s_awarded 一律 false（不授 S）。
  留痕四项 + window_excludes_* 齐备，供下一批参考。
"""
import io, json, os, datetime, collections

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TODAY = datetime.date(2026, 11, 22)
LO = (TODAY - datetime.timedelta(days=30)).isoformat()

reg = []
for l in io.open(os.path.join(ROOT, "papers/library/registry.jsonl"), encoding="utf-8"):
    if l.strip():
        reg.append(json.loads(l))
print("registry", len(reg))

THIS_RUN_BATCHES = set()  # 状态日无追加批
win = [r for r in reg
       if LO <= r.get("date", "") < TODAY.isoformat()
       and str(r.get("batch") or "") not in THIS_RUN_BATCHES]
top = sorted(win, key=lambda r: (-r.get("value", 0), r["id"]))[:10]
mean = round(sum(r["value"] for r in top) / len(top), 4) if top else 0.0
print("window", LO, "~", TODAY.isoformat(), "in_window", len(win), "top10_mean", mean)

grades = collections.Counter(r.get("grade") for r in reg)
notes = len([p for p in os.listdir(os.path.join(ROOT, "papers/notes")) if p.endswith(".md")])
daily = len([d for d in os.listdir(os.path.join(ROOT, "papers/daily"))
             if os.path.isdir(os.path.join(ROOT, "papers/daily", d))])
moc = len([p for p in os.listdir(os.path.join(ROOT, "papers/MOC")) if p.startswith("MOC-") and p.endswith(".md")])

out = {
    "run_date": TODAY.isoformat(),
    "run_type": "status_day_weekend_no_announcement",
    "registry_total": len(reg),
    "grades": {k: grades.get(k, 0) for k in ("S", "A", "B", "C")},
    "notes": notes,
    "daily_dirs": daily,
    "moc_files": moc,
    "gate1": "N/A（0 候选：周末 skipDays 无 11-21/11-22 公告组）",
    "gate2": "N/A（0 候选）",
    "gate3": {
        "window_lo": LO,
        "window_hi": TODAY.isoformat(),
        "window_excludes_today": True,
        "window_excludes_this_run_batches": True,
        "this_run_batches_excluded": sorted(THIS_RUN_BATCHES),
        "in_window": len(win),
        "top10_mean": mean,
        "top10_lib": [{"id": r["id"], "date": r.get("date"), "value": r.get("value"),
                       "grade": r.get("grade"), "batch": r.get("batch")} for r in top],
        "today_max": None,
        "margin": None,
        "heavy_day_raw": False,
        "heavy_day": False,
        "blockbuster": False,
        "s_awarded": False,
        "verdict": "no_candidate_status_day",
    },
}
json.dump(out, io.open(os.path.join(ROOT, "data/gates_1122.json"), "w", encoding="utf-8"),
          ensure_ascii=False, indent=1)
print("\n=== 门③ 基线 ===")
print(f"窗口 {LO} ~ {TODAY}，{len(win)} 条入窗，Top10 均分 {mean}")
for r in top:
    print("  ", r.get("date"), r["id"], r.get("value"), r.get("grade"), r.get("batch"))
print("grades", out["grades"], "notes", notes, "daily", daily, "moc", moc)
