# -*- coding: utf-8 -*-
"""2026-11-27 定稿评分：合并 8 组 digest（主批 44 + 残差采纳 12 + backfill 8 = 64），
主会话按标准权重校准后落 scored。

权重 IMP .20 / NOV .20 / TEC .15 / EXP .15 / PER .15 / TRL .08 / REP .07。
校准纪律：库内 4.50+（riMESA 4.50 / Open-HumanScale 4.57 / Map2SLAM 4.57 / MoGe-4D 4.57）为能力级锚点。
"""
import glob
import json

W = {"IMP": .20, "NOV": .20, "TEC": .15, "EXP": .15, "PER": .15, "TRL": .08, "REP": .07}
MMDD, DAY = "1127", "2026-11-27"

# 主会话校准（相对子代理初评）——每条都要有事实依据
OVERRIDE = {
    # 2611.33313 PARTIAL（ar5iv 摘要页）：摘要仅述原型与 106 人评测，无量化对比 → TEC/EXP 下调
    "2611.33313": {"TEC": 2, "EXP": 2},
}
TRL_TEXT_FIX = {}

dig = {}
for f in sorted(glob.glob("data/digest_1127_g*.json")):
    for r in json.load(open(f, encoding="utf-8")):
        if r["id"] in dig:
            raise SystemExit("DUP " + r["id"])
        dig[r["id"]] = r
print("digest", len(dig))

main = json.load(open("data/xr_final_1127.json", encoding="utf-8"))
old = json.load(open("data/backfill_pool_1127.json", encoding="utf-8"))
adopt = json.load(open("data/adopt_1127.json", encoding="utf-8"))
nonxr = json.load(open("data/nonxr_1127.json", encoding="utf-8"))
pub = json.load(open("data/published_1127.json", encoding="utf-8"))
man = json.load(open("data/fulltext/_manifest.json", encoding="utf-8"))

missing = [i for i in list(main) + list(old) + list(adopt) if i not in dig]
if missing:
    raise SystemExit("digest 缺: %s" % missing)

rows = []
for i in list(main) + list(adopt) + list(old):
    g = dig[i]
    s = dict(g["scores"])
    s.update(OVERRIDE.get(i, {}))
    # 主批/backfill 池值是记录 dict（内含 track），残差采纳池值是赛道字符串
    if i in main:
        rec = main[i]
        track = rec["track"]
    elif i in adopt:
        rec = nonxr.get(i, {})
        track = adopt[i]
    else:
        rec = old[i]
        track = rec["track"]
    if not isinstance(track, str) or not track:
        raise SystemExit("track 非法: %s -> %r" % (i, track))
    if i in main:
        batch = DAY
    elif i in adopt:
        batch = DAY
    else:
        batch = "backfill-%s" % MMDD
    recall = ("RESIDUAL_ADOPT" if i in adopt else (rec.get("recall") or "KW"))
    ev = man.get(i, {})
    rows.append({
        "id": i,
        "title": g["title"],
        "title_zh": g["title_zh"],
        "track": track,
        "batch": batch,
        "announce": rec.get("announce", ""),
        "recall": recall,
        "published": pub.get(i, {}).get("published", rec.get("published_rss", "")),
        "cat": rec.get("cat", pub.get(i, {}).get("cat", "")),
        "value": round(sum(W[k] * s[k] for k in W), 2),
        "scores": s,
        "evidence": ev.get("evidence", ""),
        "level": ev.get("level", ""),
        "chars": ev.get("chars", 0),
        "code": g.get("code", "未提及"),
        "venue": g.get("venue", "arXiv preprint"),
        "note": "",
        "problem": g["problem"],
        "method": g["method"],
        "key_numbers": g["key_numbers"],
        "ablation": g["ablation"],
        "baselines": g["baselines"],
        "datasets": g["datasets"],
        "novelty": g["novelty"],
        "limitations": g["limitations"],
        "trl_evidence": TRL_TEXT_FIX.get(i, g["trl_evidence"]),
        "scores_why": g["scores_why"],
        "grade": "",
        "in_top10": False,
    })

bad = [r["id"] for r in rows if not r["evidence"]]
assert not bad, bad
json.dump(rows, open("data/scored_%s.json" % MMDD, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("scored", len(rows), "main", sum(1 for r in rows if r["batch"] == DAY),
      "backfill", sum(1 for r in rows if r["batch"].startswith("backfill")))
for r in sorted(rows, key=lambda x: -x["value"])[:14]:
    print(f"  {r['value']:.2f} {r['id']} {r['track']} {r['title_zh'][:44]}")
