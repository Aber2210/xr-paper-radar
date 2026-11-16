# -*- coding: utf-8 -*-
"""gates_1117.py — 2026-11-17 覆盖度三关（门① Jaccard / 门② 赛道覆盖 / 门③ 价值天花板）。

口径（用户任务书第 6 步）：
  门① 最大 Jaccard < 0.62（仅对比非本批文献）
  门② Top10 覆盖 ≥5 赛道
  门③ 当日最高分 vs 库内近 30 天 Top10 均分（date>=today-30 按 value 降序取前 10 均值，现算）
        today_max >= 均分 → 重磅日可评 S；否则非重磅日无 S（校准关，不触发重筛）
  backfill 不参与门③（口径固定）。
"""
import io, json, os, re, datetime, collections

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TODAY = datetime.date(2026, 11, 17)
LO = (TODAY - datetime.timedelta(days=30)).isoformat()
STOP = set("""a an the of for and to in on with via from by is are we our this that using based
towards toward new towards: method approach results using can be as at it its not no than then""".split())


def toks(s):
    return {w for w in re.findall(r"[a-z0-9]{3,}", (s or "").lower()) if w not in STOP}


reg = []
for l in io.open(os.path.join(ROOT, "papers/library/registry.jsonl"), encoding="utf-8"):
    if l.strip():
        reg.append(json.loads(l))
regids = {r["id"].split(":")[-1].split("v")[0] for r in reg}
print("registry", len(reg), "unique ids", len(regids))

scored = json.load(open(os.path.join(ROOT, "data/scored_1117.json"), encoding="utf-8"))
main = [r for r in scored if r["batch"] == "2026-11-17"]
bf = [r for r in scored if r["batch"] == "backfill-1117"]
main.sort(key=lambda r: (-r["value"], -r["scores"]["IMP"], -r["scores"]["NOV"], r["id"]))

BAN = "C 级（<3.0）仅入馆不解读"
top10 = [r for r in main if r["value"] >= 3.0][:10]
print("\n门②/定稿候选 Top", len(top10), "：", [r["id"] for r in top10])

# ---- 门① 同质度（对比非本批：库内 90 天内 + 本批之外条目）----
lib = [r for r in reg if r.get("date", "") >= (TODAY - datetime.timedelta(days=90)).isoformat()]
lib_tok = [(r["id"].split(":")[-1].split("v")[0], toks(r.get("title", "") + " " + r.get("abstract", "")),
            r.get("date")) for r in lib]
worst = []
for r in top10:
    t = toks(r["title"] + " " + (r["problem"] or ""))
    best = (0.0, None, None)
    for lid, lt, ld in lib_tok:
        if lid == r["id"] or lid in {x["id"] for x in scored}:
            continue
        inter = len(t & lt)
        if not inter:
            continue
        j = inter / max(1, len(t | lt))
        if j > best[0]:
            best = (j, lid, ld)
    worst.append((r["id"], round(best[0], 3), best[1], best[2]))
worst.sort(key=lambda x: -x[1])
print("\n门① 各定稿篇最大 Jaccard（对比库内 90 天非本批）：")
for w in worst:
    print(f"   {w[0]} max_j={w[1]:.3f} vs {w[2]} ({w[3]})")
g1_max = worst[0][1] if worst else 0.0

# ---- 门② 赛道覆盖 ----
tracks = collections.Counter(r["track"] for r in top10)
all_tracks = collections.Counter(r["track"] for r in main)

# ---- 门③ 价值天花板 ----
win = [r for r in reg if r.get("date", "") >= LO]
top = sorted(win, key=lambda r: (-r.get("value", 0), r["id"]))[:10]
mean = round(sum(r["value"] for r in top) / len(top), 4) if top else 0.0
today_max = max(r["value"] for r in main)

out = {
    "run_date": TODAY.isoformat(),
    "gate1": {"max_jaccard": g1_max, "threshold": 0.62, "pass": g1_max < 0.62,
              "detail": [{"id": w[0], "j": w[1], "vs": w[2], "date": w[3]} for w in worst]},
    "gate2": {"top10_tracks": dict(tracks), "n_tracks": len(tracks),
              "all_batch_tracks": dict(all_tracks), "n_all": len(all_tracks),
              "pass": len(tracks) >= 5},
    "gate3": {"window_lo": LO, "window_hi": TODAY.isoformat(), "in_window": len(win),
              "top10_mean": mean, "today_max": today_max,
              "heavy_day": today_max >= mean,
              "top10_lib": [{"id": r["id"], "date": r.get("date"), "value": r.get("value"),
                             "grade": r.get("grade")} for r in top]},
    "top10": [r["id"] for r in top10],
    "main_n": len(main), "bf_n": len(bf),
    "excluded_lt3": [r["id"] for r in main if r["value"] < 3.0],
    "note_lt3": BAN,
}
json.dump(out, io.open(os.path.join(ROOT, "data/gates_1117.json"), "w", encoding="utf-8"),
          ensure_ascii=False, indent=1)

print("\n=== 三关 ===")
print(f"门① max Jaccard {g1_max:.3f} < 0.62 → {'PASS' if g1_max < 0.62 else 'FAIL'}")
print(f"门② Top{len(top10)} 覆盖 {len(tracks)} 赛道 {dict(tracks)}（全批 {len(all_tracks)}）→ {'PASS' if len(tracks)>=5 else 'FAIL'}")
print(f"门③ 当日最高 {today_max:.2f} vs 库内近30天Top10均分 {mean:.4f}（窗口 {LO}~{TODAY}，{len(win)} 条入窗）"
      f" → {'重磅日' if today_max >= mean else '非重磅日无 S'}")
for r in top:
    print("   lib top:", r.get("date"), r["id"], r.get("value"), r.get("grade"))
print("C 级（<3.0）不解读：", out["excluded_lt3"])
