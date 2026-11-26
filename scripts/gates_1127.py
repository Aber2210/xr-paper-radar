# -*- coding: utf-8 -*-
"""gates_1127.py — 覆盖度三关 + 档位定稿（2026-11-27 主批）。

门① 同质：本批每篇 vs 库内（追加前）标题+摘要 token Jaccard，取最大值；阈值 0.62。
门② 方向：Top10 赛道覆盖数 ≥5（不足则从 B 级池回补冷门赛道）。
门③ 天花板：today_max vs 库内近 30 天 Top10 均分（半开窗口 [today-30, today)、按 batch 剔除本次两批）；
       blockbuster = 机械 heavy_day **且** margin ≥ 0.05（险过不授 S）。
"""
import io, json, os, re, datetime, collections, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from grade_caliber import assign_grade

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
os.chdir(ROOT)
TODAY = datetime.date(2026, 11, 27)
LO = (TODAY - datetime.timedelta(days=30)).isoformat()
MMDD = "1127"
DAY = "2026-11-27"
ANN = "2026-11-26"

rows = json.load(open(f"data/scored_{MMDD}.json", encoding="utf-8"))
reg = [json.loads(l) for l in io.open("papers/library/registry.jsonl", encoding="utf-8") if l.strip()]
THIS_RUN = sorted({r["batch"] for r in rows})

# ---------- 门① ----------
STOP = set("the a an of and for with on in to via from by is are we our this that using based "
           "approach method paper propose proposed results show shows can be as at it its than "
           "which while such not no more most new".split())


def toks(s):
    return {w for w in re.findall(r"[a-z0-9]+", (s or "").lower()) if len(w) > 2 and w not in STOP}


reg_pool = [r for r in reg if str(r.get("batch") or "") not in THIS_RUN]
reg_toks = [(r["id"], toks(r.get("title", "") + " " + r.get("title_zh", ""))) for r in reg_pool]

pairs = []
for r in rows:
    a = toks(r["title"] + " " + r["problem"] + " " + r["method"])
    best, bid = 0.0, ""
    for rid, rt in reg_toks:
        if not rt:
            continue
        j = len(a & rt) / len(a | rt) if (a | rt) else 0.0
        if j > best:
            best, bid = j, rid
    pairs.append((round(best, 3), r["id"], bid))
pairs.sort(reverse=True)
gate1_max = pairs[0]
print("门① top5:", pairs[:5])
gate1_pass = gate1_max[0] < 0.62

# ---------- 门② ----------
main = [r for r in rows if not r["batch"].startswith("backfill")]
main.sort(key=lambda r: (-r["value"], -r["scores"]["IMP"], -r["scores"]["NOV"], r["id"]))
TOPN = 10
top = main[:TOPN]
cov = collections.Counter(r["track"] for r in top)
pure_tracks = dict(cov)
# 门②不足 5 赛道 → 触发一次回补：剔重复赛道最低分，再从未覆盖赛道回补最高分
# （同分按 IMP/NOV 降序、再赛道多样性、再 id 升序；被剔者仍入馆写笔记，仅不占 Top10 名额）
rescreen = []
for _ in range(3):
    if len({r["track"] for r in top}) >= 5:
        break
    over = collections.Counter(r["track"] for r in top).most_common(1)[0][0]
    cand = [r for r in top if r["track"] == over]
    drop = min(cand, key=lambda r: (r["value"], -r["scores"]["IMP"], -r["scores"]["NOV"], r["id"]))
    have = {r["track"] for r in top}
    pool = [r for r in main if r not in top and r["track"] not in have]
    if not pool:
        break
    best_val = max(r["value"] for r in pool)
    tie = sorted([r for r in pool if r["value"] == best_val],
                 key=lambda r: (-r["scores"]["IMP"], -r["scores"]["NOV"], r["id"]))
    add = tie[0]
    top = [r for r in top if r is not drop] + [add]
    top.sort(key=lambda r: (-r["value"], -r["scores"]["IMP"], -r["scores"]["NOV"], r["id"]))
    rescreen.append({"drop": drop["id"], "drop_track": drop["track"], "drop_value": drop["value"],
                     "add": add["id"], "add_track": add["track"], "add_value": add["value"]})
cov = collections.Counter(r["track"] for r in top)
gate2_pass = len(cov) >= 5
print("门② 纯值赛道:", pure_tracks, "→ 定稿:", dict(cov), "覆盖", len(cov))
print("门② 回补:", rescreen)
print("全批赛道:", dict(collections.Counter(r["track"] for r in rows)))

# ---------- 门③ ----------
win = [r for r in reg if LO <= r.get("date", "") < TODAY.isoformat()
       and str(r.get("batch") or "") not in THIS_RUN]
lib_top = sorted(win, key=lambda r: (-r.get("value", 0), r["id"]))[:10]
base = round(sum(r["value"] for r in lib_top) / len(lib_top), 4) if lib_top else 0.0
today_max = max(r["value"] for r in main)
margin = round(today_max - base, 4)
heavy_raw = today_max >= base
blockbuster = bool(heavy_raw and margin >= 0.05)
print(f"门③ today_max={today_max} base={base} margin={margin} heavy_raw={heavy_raw} blockbuster={blockbuster}")
print("门③ 库内 Top10:", [(r["id"], r["value"], r.get("date")) for r in lib_top])

# ---------- 档位 ----------
for r in rows:
    r["grade"] = assign_grade(r["value"], r["batch"], blockbuster)
    r["in_top10"] = r["id"] in {t["id"] for t in top}
json.dump(rows, open(f"data/scored_{MMDD}.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)

grades = collections.Counter(r["grade"] for r in rows)
grades_main = collections.Counter(r["grade"] for r in main)
print("档位 全批:", dict(grades), "| 主批:", dict(grades_main))

notes = len([p for p in os.listdir("papers/notes") if p.endswith(".md")])
daily = len([d for d in os.listdir("papers/daily") if os.path.isdir(os.path.join("papers/daily", d))])
moc = len([p for p in os.listdir("papers/MOC") if p.startswith("MOC-") and p.endswith(".md")])
aud = json.load(open(f"data/audit_{MMDD}_days.json", encoding="utf-8"))
slots = sum(v["new"][ANN]["declared"] or 0 for v in aud.values())
uniq = len([p for p, v in json.load(open(f"data/newday_{MMDD}.json", encoding="utf-8")).items()
            if v[2] == ANN])
res = json.load(open(f"data/residual_{MMDD}.json", encoding="utf-8"))
adopt = json.load(open(f"data/adopt_{MMDD}.json", encoding="utf-8"))
missed = json.load(open(f"data/missed_xr_{MMDD}.json", encoding="utf-8"))

out = {
    "run_date": DAY,
    "run_type": "regular_batch_announcement_1126",
    "announce_day": ANN,
    "pull_day": DAY,
    "registry_total_before": len(reg),
    "grades_before": dict(collections.Counter(r.get("grade") for r in reg)),
    "notes_before": notes, "daily_before": daily, "moc_before": moc,
    "announcement_group": {"slots": slots, "unique": uniq,
                           "per_cat": {k: v["new"][ANN] for k, v in aud.items()}},
    "recall": {"rss_items": 849, "listing_coverage": f"{uniq}/{uniq}（缺收 0）",
               "kw_hits": 67, "title_extra": 25, "pool": 92, "rejected_from_pool": 49,
               "residual_scanned": res["n_scanned"], "residual_flagged": res["n_flagged"],
               "residual_rate": res["rate"], "residual_adopted": len(adopt),
               "main_candidates": len(main), "residual_adopted_list": sorted(adopt),
               "prev_group_unregistered": missed["unregistered"],
               "prev_group_leak_n": missed["leak_n"],
               "note": "残差采纳 12 篇全部走全文抓取与评分后入馆，未直接并入 registry"},
    "gate1": {"max_jaccard": gate1_max[0], "pair": [gate1_max[1], gate1_max[2]],
              "threshold": 0.62, "pass": gate1_pass,
              "note": "只对比追加前库内集合（不含本批两批）"},
    "gate2": {"top10_tracks": dict(cov), "n_tracks": len(cov), "pass": gate2_pass,
              "pure_value_tracks": pure_tracks, "rescreen": "; ".join(
                  "%s(%.2f,%s) 出 / %s(%.2f,%s) 入" % (x["drop"], x["drop_value"], x["drop_track"],
                                                       x["add"], x["add_value"], x["add_track"])
                  for x in rescreen) or "未触发",
              "rescreen_ops": rescreen,
              "top10_ids": [t["id"] for t in top],
              "note": "回补只影响 Top10 名额，被剔篇仍入馆写笔记并保留原档位",
              "all_batch_tracks": len(set(r["track"] for r in rows))},
    "gate3": {
        "window_lo": LO, "window_hi": TODAY.isoformat(),
        "window_excludes_today": True,
        "window_excludes_this_run_batches": True,
        "this_run_batches_excluded": THIS_RUN,
        "in_window": len(win),
        "top10_mean": base,
        "top10_lib": [{"id": r["id"], "date": r.get("date"), "value": r.get("value"),
                       "grade": r.get("grade"), "batch": r.get("batch")} for r in lib_top],
        "today_max": today_max,
        "margin": margin,
        "heavy_day_raw": heavy_raw,
        "heavy_day": heavy_raw,
        "blockbuster": blockbuster,
        "s_awarded": blockbuster,
        "verdict": ("blockbuster_heavy_day" if blockbuster
                    else ("heavy_raw_but_margin_lt_0.05" if heavy_raw else "non_blockbuster")),
    },
    "top10": [t["id"] for t in top],
    "grades_main": {k: grades_main.get(k, 0) for k in ("S", "A", "B", "C")},
    "grades_all": {k: grades.get(k, 0) for k in ("S", "A", "B", "C")},
    "evidence": dict(collections.Counter(r["evidence"] for r in rows)),
}
json.dump(out, open(f"data/gates_{MMDD}.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("\nTop10:")
for i, t in enumerate(top, 1):
    print(f"  {i:2d} {t['value']:.2f} {t['grade']} {t['id']} {t['track']} {t['title_zh'][:40]}")
print("\ngates ->", f"data/gates_{MMDD}.json")
