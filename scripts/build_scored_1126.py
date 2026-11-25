# -*- coding: utf-8 -*-
"""2026-11-26 定稿评分：合并 7 组 digest（主批 55 = 47 直接候选 + 8 残差采纳；backfill 8），
主会话按标准权重逐篇校准后落 scored。

权重 IMP .20 / NOV .20 / TEC .15 / EXP .15 / PER .15 / TRL .08 / REP .07。
主会话校准（相对子代理初评）：
  - 2611.32198 MoGe-4D：TRL 4→3（离线片段推理，项目页未给出可核实实时系统）
  - 2611.32523 AirLeg：TRL 5→4（真机实时但「宣称开源」，未到产品化；trl_evidence 删除无法核实的 38 ms 表述）
  - 2611.31757 Xtream：PER 5→4（ATE 降幅 25–28%，未达 §3 的 >30% 档）
评分锚点：库内 4.50+（riMESA 4.50 / Open-HumanScale 4.57 / Map2SLAM 4.57）为能力级。
"""
import json
import glob
import os

W = {"IMP": .20, "NOV": .20, "TEC": .15, "EXP": .15, "PER": .15, "TRL": .08, "REP": .07}
MMDD, DAY = "1126", "2026-11-26"

OVERRIDE = {
    "2611.32198": {"TRL": 3},
    "2611.32523": {"TRL": 4},
    "2611.31757": {"PER": 4},
}
TRL_TEXT_FIX = {
    "2611.32523": ("在工业级 ANYmal D 公开数据集与自建低成本 Unitree Go2 平台上完成真机验证，"
                   "在 Jetson AGX Orin 上实时运行（正文给出模块级触发频率与耗时表，含在线自适应）；"
                   "作者声明开源代码与数据集并提供项目页，属可部署系统形态但未到产品化。"),
}

dig = {}
for f in sorted(glob.glob("data/digest_1126_g*.json")):
    for r in json.load(open(f, encoding="utf-8")):
        if r["id"] in dig:
            raise SystemExit("DUP " + r["id"])
        dig[r["id"]] = r

dec = json.load(open("data/decisions_1126.json", encoding="utf-8"))
pool = json.load(open("data/xr_pool_1126.json", encoding="utf-8"))
old = json.load(open("data/old_replace_1126.json", encoding="utf-8"))
pub = json.load(open("data/published_1126.json", encoding="utf-8"))
man = json.load(open("data/fulltext/_manifest.json", encoding="utf-8"))

rows = []
for i, track in list(dec["main"].items()) + list(dec["backfill"].items()):
    g = dig[i]
    s = dict(g["scores"])
    s.update(OVERRIDE.get(i, {}))
    rec = pool.get(i) or old.get(i) or {}
    batch = "2026-11-26" if i in dec["main"] else "backfill-1126"
    ev = man.get(i, {})
    rows.append({
        "id": i,
        "title": g["title"],
        "title_zh": g["title_zh"],
        "track": track,
        "batch": batch,
        "announce": rec.get("announce", ""),
        "recall": rec.get("recall", "RESIDUAL_ADOPT" if i in dec["main"] and i not in pool else ""),
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

missing = [r["id"] for r in rows if not r["evidence"]]
assert not missing, missing
json.dump(rows, open("data/scored_%s.json" % MMDD, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("scored", len(rows), "main", sum(1 for r in rows if r["batch"] == DAY),
      "backfill", sum(1 for r in rows if r["batch"].startswith("backfill")))
for r in sorted(rows, key=lambda x: -x["value"])[:12]:
    print(f"  {r['value']:.2f} {r['id']} {r['track']} {r['title_zh'][:44]}")
