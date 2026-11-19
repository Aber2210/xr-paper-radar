# -*- coding: utf-8 -*-
"""2026-11-20 定稿评分：合并 5 组 digest，主会话按标准权重逐篇校准后落 scored/gates/7dim/scored.md。

校准原则（相对子代理 scores_hint 的改动，全部有正文依据）：
  - 2611.24938 Phoenix：IMP 5→4（机器人操作 world-action，不是 XR 核心瓶颈）；
    PER 4→3（LIBERO-Plus +2.0 点、RoboTwin C2R +0.5 点，均 <10%）。
  - 2611.23670 EyeDiT：PER 4→3（正文可核：gaze E50 3.53° vs oracle 2.59°；子代理所称 +14% PSNR / 基线 8.41° 未在正文检出，不予采信）。
  - 2611.23871 HOForce：TRL 4→3（算法级贡献，无系统原型）。
  - 2611.24805 Edge RAW：TRL 5→4（Rokid Glass 真机 Table 6 有实测，但方法未进产品）。
  - 2606.07179 EvoGS：PER 4→3（PSNR 仅 +0.31 dB；存储/显存下降不计入渲染精度）。
  - 2611.24193 WM^MLLM：evidence FULL→PARTIAL（arXiv HTML 仅前言+引言+图注，无 Method/Experiments 节），
    TEC 3→2、EXP 4→2；PER 5→4（数字为摘要自述，未能在正文核实）。
"""
import json, re, datetime, sys
sys.path.insert(0, "scripts")
from grade_caliber import assign_grade

W = {"IMP": .20, "NOV": .20, "TEC": .15, "EXP": .15, "PER": .15, "TRL": .08, "REP": .07}
MMDD, DAY = "1120", "2026-11-20"

D = {}
for g in range(1, 6):
    D.update(json.load(open(f"data/digest_1120_g{g}.json", encoding="utf-8")))

main = json.load(open(f"data/cand_main_{MMDD}.json", encoding="utf-8"))
bf = json.load(open(f"data/cand_bf_{MMDD}.json", encoding="utf-8"))
cands = {**main, **bf}

OVERRIDE = {
    "2611.24938": {"IMP": 4, "PER": 3},
    "2611.23670": {"PER": 3},
    "2611.23871": {"TRL": 3},
    "2611.24805": {"TRL": 4},
    "2606.07179": {"PER": 3},
    "2611.24193": {"TEC": 2, "EXP": 2, "PER": 4},
}
NOTE = {
    "2611.24193": "证据等级 PARTIAL：arXiv HTML 仅前言/引言/图注，数字为摘要自述",
    "2606.07179": "arXiv 元数据标题为 Lifting 3D Gaussians…，正文（v2/ar5iv）标题为 EvoGS…，疑 v2 改题",
    "2611.24938": "PER 按主力基准 +2.0/+0.5 点计，不按缩放增益 27.0 点计",
}

rows = []
for pid, g in D.items():
    c = cands[pid]
    s = dict(g["scores_hint"])
    for k, v in OVERRIDE.get(pid, {}).items():
        s[k] = v
    val = round(sum(W[k] * s[k] for k in W), 2)
    rows.append({
        "id": pid, "title": g["title_en"], "title_zh": g["title_zh"],
        "track": c["track"], "batch": c["batch"], "announce": c.get("announce", ""),
        "published": c.get("published_rss", ""), "cat": c.get("cat", ""),
        "value": val, "scores": s, "scores_why": g["scores_why"],
        "evidence": "PARTIAL" if pid == "2611.24193" else "FULL",
        "code": g.get("code", ""), "venue": g.get("venue", ""),
        "recall": c.get("recall", ""), "note": NOTE.get(pid, ""),
    })

rows.sort(key=lambda r: (-r["value"], -r["scores"]["IMP"], -r["scores"]["NOV"], r["id"]))
main_rows = [r for r in rows if not r["batch"].startswith("backfill")]

# ---------------- 门①：最大 Jaccard（仅对比非本批文献）----------------
def toks(t):
    return {w for w in re.findall(r"[a-z0-9]{3,}", (t or "").lower())}

this_run = {r["batch"] for r in rows}
lib = []
for l in open("papers/library/registry.jsonl", encoding="utf-8"):
    if l.strip():
        d = json.loads(l)
        if d.get("batch") not in this_run:
            lib.append(d)
lib_tok = [(d["id"], toks(d.get("title", "") + " " + d.get("abstract", ""))) for d in lib]
worst = (0.0, "", "")
for r in main_rows[:10]:
    a = toks(r["title"] + " " + cands[r["id"]].get("abstract", ""))
    for lid, b in lib_tok:
        inter = len(a & b)
        if not inter:
            continue
        j = inter / len(a | b)
        if j > worst[0]:
            worst = (j, r["id"], lid)
gate1 = round(worst[0], 3)
tracks_top = sorted({r["track"] for r in main_rows[:10]})
gate2 = len(tracks_top)

# ---------------- 门③：现算库内近 30 天 Top10 均分（半开窗口，剔除本次批）----------------
today = datetime.date.fromisoformat(DAY)
lo = today - datetime.timedelta(days=30)
win = []
for l in open("papers/library/registry.jsonl", encoding="utf-8"):
    if l.strip():
        d = json.loads(l)
        if d.get("batch") in this_run:
            continue
        try:
            dt = datetime.date.fromisoformat(d["date"][:10])
        except Exception:
            continue
        if lo <= dt < today:
            win.append(d)
top10 = sorted(win, key=lambda d: -float(d.get("value", 0)))[:10]
mean = round(sum(float(d["value"]) for d in top10) / len(top10), 4)
today_max = max(r["value"] for r in main_rows)
heavy_raw = today_max >= mean
margin = round(today_max - mean, 3)
blockbuster = bool(heavy_raw and margin >= 0.05)
gates = {
    "date": DAY,
    "gate1": {"max_jaccard": gate1, "pair": [worst[1], worst[2]], "pass": gate1 < 0.62},
    "gate2": {"tracks_top10": tracks_top, "n_tracks": gate2, "pass": gate2 >= 5},
    # 门③ 口径字段必须落在 gate3 内：check_release.py 的 G2 只查 gate3 下的
    # window_excludes_* / this_run_batches_excluded，且 latest_gates() 靠 gate3.window_hi
    # 反推批次日期。2026-11-20 曾把这三个键写在顶层、且文件名用 gates_YYYY-MM-DD.json，
    # 结果 G2 FAIL，且该文件名在字符串排序上永远排最后，会遮蔽后续所有 gates_MMDD.json。
    "gate3": {"window_lo": str(lo), "window_hi": str(today), "in_window": len(win),
              "window_excludes_today": True, "window_excludes_this_run_batches": True,
              "this_run_batches_excluded": sorted(this_run),
              "top10_mean": mean, "today_max": today_max, "margin": margin,
              "heavy_day_raw": heavy_raw, "heavy_day": heavy_raw,
              "blockbuster": blockbuster, "s_awarded": blockbuster,
              "top10_lib": [{"id": d["id"], "date": str(d.get("date", ""))[:10],
                             "value": float(d["value"]), "grade": d.get("grade", "")}
                            for d in top10]},
}

for r in rows:
    r["grade"] = assign_grade(r["value"], r["batch"], gates["gate3"]["blockbuster"])
    r["in_top10"] = (not r["batch"].startswith("backfill")) and r in main_rows[:10]

json.dump(rows, open(f"data/scored_{MMDD}.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
json.dump(gates, open(f"data/gates_{MMDD}.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)

# ---------------- 7 维表 + scored.md ----------------
import os
os.makedirs(f"papers/daily/{DAY}", exist_ok=True)
hdr = "| # | arXiv | 论文 | 赛道 | IMP | NOV | TEC | EXP | PER | TRL | REP | 总分 | 档 | 公告 | 证据 |\n"
hdr += "|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|\n"
lines = [hdr]
for i, r in enumerate(rows, 1):
    s = r["scores"]
    mark = " ⛔" if r["grade"] == "C" else ""
    lines.append("| %d | %s | %s | %s | %d | %d | %d | %d | %d | %d | %d | **%.2f** | %s | %s | %s |\n" % (
        i, r["id"], r["title_zh"][:38], r["track"], s["IMP"], s["NOV"], s["TEC"], s["EXP"],
        s["PER"], s["TRL"], s["REP"], r["value"], r["grade"], r["announce"] or "-", r["evidence"]))
open(f"papers/daily/{DAY}/7dim-table.md", "w", encoding="utf-8").write(
    "# 7 维对比表 · %s（主批 %d 篇 + backfill %d 篇）\n\n" %
    (DAY, len(main_rows), len(rows) - len(main_rows)) +
    "权重 IMP0.20·NOV0.20·TEC0.15·EXP0.15·PER0.15·TRL0.08·REP0.07；档位 S≥4.20 且 blockbuster / A3.60–4.20 / B3.00–3.60 / C<3.00。\n\n"
    + "".join(lines))

sm = ["# 评分明细与覆盖校验 · %s\n\n## 一、门禁三关\n\n" % DAY,
      "- 门① 最大 Jaccard **%.3f**（%s vs %s）→ %s\n" % (gate1, gates["gate1"]["pair"][0], gates["gate1"]["pair"][1], "PASS" if gates["gate1"]["pass"] else "FAIL"),
      "- 门② Top10 覆盖 **%d 赛道**（%s）→ %s\n" % (gate2, "、".join(tracks_top), "PASS" if gates["gate2"]["pass"] else "FAIL"),
      "- 门③ 当日最高 **%.2f** vs 库内近 30 天 Top10 均分 **%.4f**（窗口 %s~%s，%d 条入窗，已剔除本次批次）→ heavy_day_raw=%s，margin=%.3f → **blockbuster=%s，S 授予 %s**\n\n"
      % (today_max, mean, lo, today, len(win), heavy_raw, margin, blockbuster, gates["gate3"]["s_awarded"]),
      "## 二、分档统计\n\n"]
from collections import Counter
cnt_main = Counter(r["grade"] for r in main_rows)
cnt_bf = Counter(r["grade"] for r in rows if r["batch"].startswith("backfill"))
sm.append("- 主批 %d 篇：%s\n" % (len(main_rows), " / ".join(f"{k} {v}" for k, v in sorted(cnt_main.items()))))
sm.append("- backfill %d 篇：%s\n\n" % (len(rows) - len(main_rows), " / ".join(f"{k} {v}" for k, v in sorted(cnt_bf.items()))))
sm.append("## 三、逐篇评分理由\n\n")
for r in rows:
    sm.append("### %s %s（%.2f / %s）\n\n%s\n\n" % (r["id"], r["title_zh"], r["value"], r["grade"], r["scores_why"]))
open(f"papers/daily/{DAY}/scored.md", "w", encoding="utf-8").write("".join(sm))

print("scored", len(rows), "main", len(main_rows), "bf", len(rows) - len(main_rows))
print("gate1", gate1, worst[1], worst[2], "| gate2", gate2, tracks_top)
print("gate3 max", today_max, "mean", mean, "margin", margin, "blockbuster", blockbuster, "n_win", len(win))
print("grades", Counter(r["grade"] for r in rows))
print("top10:")
for r in main_rows[:10]:
    print("  %.2f %s [%s] %s" % (r["value"], r["id"], r["track"], r["title_zh"][:46]))
