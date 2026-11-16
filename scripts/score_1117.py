# -*- coding: utf-8 -*-
"""2026-11-17 汇总：合并 4 组 notes_content → 加权评分 → scored_1117.json（显式带 batch）。"""
import json, glob

W = {"IMP": 0.20, "NOV": 0.20, "TEC": 0.15, "EXP": 0.15, "PER": 0.15, "TRL": 0.08, "REP": 0.07}
MAIN_BATCH = "2026-11-17"
BF_BATCH = "backfill-1117"
BF_IDS = {"2501.12764", "2608.19372", "2611.17238"}
PUB = json.load(open("data/published_1117.json", encoding="utf-8"))     # 提交日核验
MAN = json.load(open("data/fulltext/_manifest.json", encoding="utf-8"))  # 证据等级

rows = []
for f in sorted(glob.glob("data/notes_content_1117_g*.json")):
    d = json.load(open(f, encoding="utf-8"))
    print(f, len(d))
    rows.extend(d)

print("total", len(rows))
ids = [r["id"] for r in rows]
assert len(ids) == len(set(ids)), "dup ids"

out = []
for r in rows:
    s = r["scores"]
    assert set(s) == set(W), (r["id"], s)
    val = round(sum(W[k] * s[k] for k in W), 2)
    batch = BF_BATCH if r["id"] in BF_IDS else MAIN_BATCH
    out.append({
        "id": r["id"],
        "batch": batch,
        "title": PUB.get(r["id"], {}).get("title", ""),
        "title_zh": r["title_zh"],
        "slug": r["slug"],
        "track": r["track"],
        "venue": r["venue"],
        "tags": r["tags"],
        "scores": s,
        "value": val,
        "evidence": MAN.get(r["id"], {}).get("evidence", "?"),
        "level": MAN.get(r["id"], {}).get("level", "?"),
        "chars": MAN.get(r["id"], {}).get("chars", 0),
        "published": PUB.get(r["id"], {}).get("published", ""),
        "updated": PUB.get(r["id"], {}).get("updated", ""),
        "conclusion": r["conclusion"],
        "problem": r["problem"],
        "method": r["method"],
        "experiments": r["experiments"],
        "innovation": r["innovation"],
        "limits": r["limits"],
        "relation": r["relation"],
        "repro": r["repro"],
        "action": r["action"],
        "scores_why": r["scores_why"],
    })

out.sort(key=lambda x: (-x["value"], -x["scores"]["IMP"], -x["scores"]["NOV"], x["id"]))
json.dump(out, open("data/scored_1117.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)

print("\n=== 排名（主批 + backfill）===")
for i, r in enumerate(out, 1):
    print(f"{i:2d}. {r['id']} {r['value']:.2f} {r['batch']:14s} {r['track']:8s} "
          f"{r['scores']} {r['evidence']:8s} {r['title_zh'][:44]}")
main = [r for r in out if r["batch"] == MAIN_BATCH]
bf = [r for r in out if r["batch"] == BF_BATCH]
print(f"\n主批 {len(main)} 篇；backfill {len(bf)} 篇；最高分 {out[0]['value']:.2f}（{out[0]['id']}）")
