# -*- coding: utf-8 -*-
"""2026-11-21 定稿评分：合并 8 组 digest，主会话按标准权重逐篇校准后落 scored。

校准原则（相对子代理 scores_hint 的改动，全部有正文依据）：
  - 2611.26493 SGAR：NOV 5→4、IMP 5→4。几何检索替代注意力近似是漂亮的重构，但组件（学习嵌入 + 球面 k-means +
    块稀疏掩码）均为已有积木，未提出新架构/新范式，按「创新性 5=新范式」口径应为 4；
    IMP 按「5=领域公认卡脖子/高频痛点，且解决它改变系统能力边界」下调为 4——本文是对既有前馈管线
    （DejaView / VGGT-Ω）的加速，属重要工程瓶颈而非能力级突破（对照库内 4.50+ 的 riMESA / Open-HumanScale /
    Map2SLAM 均为能力级工作）。若按 IMP=5 则为 4.50、越门③ 线（4.4230+0.05）成重磅日，故此维判定直接影响档位，
    已在报告 §5 显式披露该判断及替代读数。
  - 2611.25338 VideoRNG：IMP 5→4。可重光照生成资产对内容是重要缺口，但尚未构成 XR 领域「公认卡脖子」，
    IMP=4 更贴合；NOV 保留 5（新任务 + 新表示 rtRNG）。
  - 赛道修正：2611.25696 LIFT 触觉与多模态→神经渲染（自由视点 3D 场景融合，与触觉无关）；
    2610.09195 StableGrasp 交互与输入→化身与人体（人手抓取重建属人体/化身建模）。
"""
import json, sys, datetime
sys.path.insert(0, "scripts")
from grade_caliber import assign_grade

W = {"IMP": .20, "NOV": .20, "TEC": .15, "EXP": .15, "PER": .15, "TRL": .08, "REP": .07}
MMDD, DAY = "1121", "2026-11-21"

D = {}
for g in range(1, 9):
    D.update(json.load(open(f"data/digest_1121_g{g}.json", encoding="utf-8")))

pool = json.load(open("data/xr_pool_1121.json", encoding="utf-8"))
bf = json.load(open("data/backfill_pool_1121.json", encoding="utf-8"))
cands = {**pool, **bf}
pub = json.load(open("data/published_1121.json", encoding="utf-8"))

OVERRIDE = {"2611.26493": {"NOV": 4, "IMP": 4}, "2611.25338": {"IMP": 4}}
TRACK_FIX = {"2611.25696": "神经渲染", "2610.09195": "化身与人体"}
NOTE = {
    "2611.26493": "NOV 5→4、IMP 5→4：几何检索是重构而非新范式；属既有管线加速而非能力级突破，已在报告 §5 披露替代读数",
    "2611.25338": "IMP 5→4：内容侧重要缺口但非 XR 卡脖子",
    "2405.15125": "旧稿（2024-05 首次提交）v3 再公告，NOV/REP 按公开时间下调",
    "2610.09195": "旧稿（2026-10-06 首次提交）v2 再公告",
    "2611.25696": "残差复核采纳（原被 KW/标题层漏检）",
    "2611.25802": "残差复核采纳（原被 KW/标题层漏检）",
    "2611.25801": "残差复核采纳（原被 KW/标题层漏检）",
}

rows = []
for pid, g in D.items():
    c = cands[pid]
    s = dict(g["scores_hint"])
    for k, v in OVERRIDE.get(pid, {}).items():
        s[k] = v
    track = TRACK_FIX.get(pid, g["track"])
    val = round(sum(W[k] * s[k] for k in W), 2)
    batch = "backfill-1121" if pid in bf else DAY
    rows.append({
        "id": pid, "title": g["title_en"], "title_zh": g["title_zh"],
        "track": track, "batch": batch,
        "announce": "replace" if pid in bf else c.get("announce", ""),
        "published": pub.get(pid, {}).get("published", ""),
        "last_update": pub.get(pid, {}).get("updated", ""),
        "cat": c.get("cat", ""), "value": val, "scores": s,
        "scores_why": g["scores_why"], "evidence": "FULL",
        "code": g.get("code", ""), "venue": g.get("venue", ""),
        "recall": "RESIDUAL" if c.get("recall") == "RESIDUAL" else c.get("recall", ""),
        "note": NOTE.get(pid, ""),
        # 供报告章节使用
        "problem": g["problem"], "method": g["method"], "key_results": g["key_results"],
        "novelty": g["novelty"], "limitations": g["limitations"],
    })

rows.sort(key=lambda r: (-r["value"], -r["scores"]["IMP"], -r["scores"]["NOV"], r["id"]))
json.dump(rows, open(f"data/scored_{MMDD}.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)

from collections import Counter
print("scored", len(rows), "main", sum(1 for r in rows if r["batch"] == DAY), "bf", sum(1 for r in rows if r["batch"] != DAY))
for r in rows:
    print("  %.2f %s [%s] %s %s" % (r["value"], r["id"], r["track"], r["batch"], r["title_zh"][:40]))
print("tracks all:", dict(Counter(r["track"] for r in rows)))
