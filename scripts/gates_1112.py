# -*- coding: utf-8 -*-
"""2026-11-12 覆盖度三关（门① 现算 / 门③ 现算；门② 在 scored 定稿后复核）。

门①：19 篇候选（15 主批 + 4 backfill）标题+摘要 token Jaccard vs 库内 888 条（追加前）。
门③：库内近 30 天（2026-10-13~2026-11-12）按 value 降序 Top10 均分。
"""
import json
import re
from datetime import date, timedelta

STOP = set("""a an the of for and or to in on with by from at as is are be we our this that
it its via using based can may propose present introduce towards toward novel
learning framework approach method results show shows while however both all one
two also more most than which when where such these those paper work works""".split())


def toks(s):
    s = re.sub(r"[^a-z0-9 ]", " ", (s or "").lower())
    return set(w for w in s.split() if len(w) > 2 and w not in STOP)


def jaccard(a, b):
    if not a or not b:
        return 0.0
    return len(a & b) / len(a | b)


cand = json.load(open("data/cands_1112.json", encoding="utf-8"))
CAND = cand["main"] + cand["backfill"]
raw = {}
for line in open("data/raw/2026-11-12_cands.jsonl", encoding="utf-8"):
    r = json.loads(line)
    raw[r["base_id"]] = r

lib = [json.loads(l) for l in open("papers/library/registry.jsonl", encoding="utf-8") if l.strip()]
print("candidates", len(CAND), "registry (pre-append)", len(lib))

lib_items = [(r["id"].split(":")[-1].split("v")[0], (r.get("title") or ""),
              toks((r.get("title") or "") + " " + (r.get("title_zh") or ""))) for r in lib]

rows = []
for pid in CAND:
    ct = toks(raw[pid]["title"] + " " + raw[pid]["abstract"])
    best = (0.0, "", "")
    for bid, t, lt in lib_items:
        j = jaccard(ct, lt)
        if j > best[0]:
            best = (j, bid, t[:60])
    rows.append((pid, best[0], best[1], best[2]))
rows.sort(key=lambda x: -x[1])
for pid, j, bid, t in rows[:8]:
    print(f"{pid} max_jaccard={j:.3f} vs {bid} {t}")
print(f"\n门① max Jaccard = {rows[0][1]:.3f} ({rows[0][0]} vs {rows[0][2]}) -> "
      f"{'PASS' if rows[0][1] < 0.62 else 'FAIL'}")

today = date(2026, 11, 12)
lo = (today - timedelta(days=30)).isoformat()
win = [r for r in lib if (r.get("date") or "") >= lo]
win.sort(key=lambda r: -float(r.get("value", 0)))
t10 = win[:10]
mean = sum(float(r["value"]) for r in t10) / len(t10)
print(f"\n门③ window {lo}~{today} | in-window {len(win)} | 30d Top10 mean = {mean:.4f}")
for r in t10:
    print(f"   {float(r['value']):.2f} {r.get('grade')} {r['id'].split(':')[-1]} {r.get('date')} {(r.get('title_zh') or '')[:36]}")
json.dump({"gate1_max_jaccard": rows[0][1], "gate1_pair": [rows[0][0], rows[0][2]],
           "gate3_mean": mean, "gate3_window": [lo, today.isoformat()], "gate3_in_window": len(win),
           "gate3_top10": [[float(r["value"]), r["id"].split(":")[-1], r.get("date")] for r in t10]},
          open("data/gates_1112.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("saved data/gates_1112.json")
