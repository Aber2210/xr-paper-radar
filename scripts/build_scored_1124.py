# -*- coding: utf-8 -*-
"""2026-11-24 定稿评分：合并 4 组 digest（主批 41 = 33 直接候选 + 8 残差采纳；backfill 9），
主会话按标准权重逐篇校准后落 scored。

权重 IMP .20 / NOV .20 / TEC .15 / EXP .15 / PER .15 / TRL .08 / REP .07。
评分锚点：库内 4.50+（riMESA 4.50 / Open-HumanScale 4.57 / Map2SLAM 4.57 / AnyVIO 4.43）为能力级工作；
本批 4.27 三篇（EgoLAM / FORTH / Non-penetrating）属「重要但非能力级」，不与 S 级锚点并置。
"""
import json, sys
sys.path.insert(0, "scripts")
from grade_caliber import assign_grade

W = {"IMP": .20, "NOV": .20, "TEC": .15, "EXP": .15, "PER": .15, "TRL": .08, "REP": .07}
MMDD, DAY = "1124", "2026-11-24"

S = {
    # ---- g1 ----
    "2611.27788": (3, 3, 4, 4, 3, 2, 2),   # FoVT 注视式 ViT
    "2611.27719": (3, 4, 4, 4, 4, 2, 2),   # VeilGS
    "2611.27621": (3, 4, 3, 4, 5, 2, 2),   # 3D 标注布局多视图 QA
    "2611.27512": (3, 4, 4, 4, 4, 2, 4),   # PGS-PCQA
    "2611.27459": (4, 5, 4, 4, 4, 2, 2),   # Ego2Ego
    "2611.27290": (4, 5, 4, 4, 5, 3, 4),   # EgoLAM
    "2611.27281": (3, 4, 4, 4, 3, 2, 2),   # GAAFormer
    "2611.27224": (4, 4, 4, 3, 4, 2, 2),   # EAST
    "2611.27101": (4, 4, 4, 4, 4, 3, 4),   # EgoSurgHands
    "2611.27030": (3, 4, 4, 4, 5, 2, 2),   # TSIR
    "2611.27003": (3, 4, 4, 4, 4, 2, 2),   # S2D-Splat
    # ---- g2 ----
    "2611.26937": (4, 4, 4, 4, 3, 2, 4),   # Looking Right（评测类，PER 记诊断力）
    "2611.26883": (4, 4, 5, 5, 4, 2, 3),   # TouchBench
    "2611.26783": (4, 4, 4, 4, 4, 3, 4),   # CADENCE
    "2611.26730": (4, 4, 4, 4, 5, 2, 3),   # SparseHPS
    "2611.26992": (4, 5, 4, 1, 2, 1, 3),   # Geo-Force（纯理论，无实验）
    "2611.26764": (4, 5, 4, 4, 5, 2, 3),   # TacHOI
    "2611.27525": (4, 4, 4, 5, 4, 3, 3),   # PennyGS
    "2611.27817": (3, 4, 3, 4, 4, 4, 2),   # BRINA
    "2611.27633": (4, 3, 2, 3, 4, 3, 3),   # Instant-LIVO（PARTIAL）
    "2611.27603": (3, 4, 4, 4, 5, 2, 3),   # HOI 测试时潜适配
    "2611.27513": (4, 4, 4, 4, 4, 2, 3),   # Ego4Gen
    # ---- g3 ----
    "2611.27418": (3, 4, 4, 4, 4, 2, 2),   # FS-Nav
    "2611.27047": (3, 4, 4, 4, 5, 2, 2),   # BeyondEgo
    "2611.26950": (4, 4, 3, 2, 3, 1, 2),   # 电容指尖机理
    "2611.26916": (4, 4, 4, 5, 4, 3, 4),   # RoboCap-10k
    "2611.26744": (4, 5, 4, 4, 5, 3, 4),   # FORTH
    "2611.27915": (4, 4, 4, 4, 5, 2, 2),   # StereoVLM
    "2611.27509": (4, 4, 4, 3, 4, 2, 2),   # 事件连续时间深度
    "2611.27289": (3, 4, 3, 4, 3, 2, 2),   # InterBand-EMG
    "2611.27136": (3, 4, 3, 4, 3, 2, 2),   # TrajRealm
    "2611.26779": (4, 4, 4, 4, 5, 3, 4),   # Tracktail
    "2611.27299": (3, 4, 4, 3, 4, 2, 2),   # Re-JEPA
    # ---- g4 主批 ----
    "2611.26773": (4, 4, 4, 3, 5, 4, 2),   # FACET
    "2611.26981": (4, 4, 4, 5, 5, 3, 2),   # ViewDreamer
    "2611.27164": (4, 4, 4, 3, 5, 2, 2),   # PhysForce
    "2611.27336": (4, 5, 3, 3, 4, 3, 2),   # Zing-1.0
    "2611.27397": (3, 4, 4, 4, 4, 3, 2),   # AnyBodyCodec
    "2611.27412": (3, 4, 3, 4, 4, 3, 2),   # 事件结构光时间图
    "2611.27845": (4, 4, 4, 4, 4, 4, 2),   # 人形 VR 遥操作安全滤波
    "2611.27963": (4, 5, 4, 4, 5, 3, 4),   # Non-penetrating World Models
    # ---- g4 backfill ----
    "2605.19889": (3, 4, 4, 4, 5, 3, 4),   # GLUT
    "2606.16202": (3, 4, 4, 4, 4, 3, 2),   # EgoPhys
    "2607.02921": (4, 4, 4, 4, 4, 3, 4),   # R3D
    "2609.08848": (4, 4, 4, 4, 5, 3, 2),   # FIRE3D
    "2609.31248": (4, 4, 4, 4, 4, 3, 2),   # TailorGS
    "2611.25417": (3, 4, 4, 4, 4, 4, 3),   # MIR-Depth
    "2601.13574": (3, 4, 4, 4, 4, 3, 2),   # 可变形本体感知膜
    "2605.19257": (4, 4, 4, 4, 4, 3, 2),   # PRISM-SLAM
    "2611.21057": (4, 4, 4, 5, 5, 4, 2),   # WiTac
}

NOTE = {
    "2611.27633": "证据等级 PARTIAL（ar5iv 仅摘要页、arXiv HTML v1 404），TEC/EXP 按摘要级证据下调",
    "2611.26992": "纯理论工作：给出等变/归零/Lipschitz 界与 6 类失效情形，但无任何实验（EXP=1）",
    "2611.26937": "评测类论文，PER 记诊断力（揭示渲染相似度与几何精度的偏离），非性能增益",
    "2611.26950": "设计阶段证据（解析 + FEM），无样机实测，TRL=1",
    "2611.27136": "数据集「计划发布」，REP 按当前未公开计 2",
    "2611.27336": "可运行系统但无逐模块端到端消融，TEC=3",
    "2611.27788": "注视式 ViT 属效率研究，XR 关联弱，IMP=3",
    "2601.13574": "旧稿（2026-01-20 首次提交）v2 再公告；无外部方法对比，PER 按自建指标上限计 4",
    "2606.16202": "旧稿（2026-06-15 首次提交）v2 再公告",
    "2607.02921": "旧稿（2026-07-03 首次提交）v3 再公告",
    "2609.08848": "旧稿（2026-09-08 首次提交）v2 再公告",
    "2609.31248": "旧稿（2026-09-25 首次提交）v2 再公告",
    "2605.19889": "旧稿（2026-05-19 首次提交）v2 再公告",
    "2605.19257": "旧稿（2026-05-19 首次提交）v2 再公告",
    "2611.25417": "旧稿（2026-11-19 首次提交）v2 再公告",
    "2611.21057": "旧稿（2026-11-16 首次提交）v2 再公告",
}

D = {}
for g in range(1, 5):
    for x in json.load(open(f"data/digest_1124_g{g}.json", encoding="utf-8")):
        D[x["id"]] = x

cand = json.load(open("data/cand_1124.json", encoding="utf-8"))
bf = json.load(open("data/backfill_1124.json", encoding="utf-8"))
res = {f["id"]: f for f in json.load(open("data/residual_1124.json", encoding="utf-8"))["flagged"]}
pub = json.load(open("data/published_1124.json", encoding="utf-8"))
man = json.load(open("data/fulltext/_manifest.json", encoding="utf-8"))

missing = [p for p in S if p not in D]
assert not missing, f"digest 缺 {missing}"
assert set(S) == set(D), f"评分表与 digest 不一致：多 {set(S)-set(D)} 缺 {set(D)-set(S)}"

rows = []
for pid, tup in S.items():
    s = dict(zip(["IMP", "NOV", "TEC", "EXP", "PER", "TRL", "REP"], tup))
    val = round(sum(W[k] * s[k] for k in W), 2)
    if pid in bf:
        track, batch, announce, recall = bf[pid]["track"], f"backfill-{MMDD}", "replace", "REPLACE"
        title = bf[pid]["title"]
    elif pid in cand:
        track, batch, announce = cand[pid]["track"], DAY, cand[pid].get("announce", "")
        recall = cand[pid].get("recall", "")
        title = cand[pid]["title"]
    else:
        track, batch, announce, recall = res[pid]["track"], DAY, "new", "RESIDUAL"
        title = res[pid]["title"]
    rows.append({
        "id": pid, "title": title, "title_zh": D[pid]["title_zh"], "track": track, "batch": batch,
        "announce": announce, "recall": recall,
        "published": pub.get(pid, {}).get("published", ""),
        "cat": pub.get(pid, {}).get("cat", "") or cand.get(pid, {}).get("cat", ""),
        "value": val, "scores": s,
        "evidence": man.get(pid, {}).get("evidence", "FULL"),
        "level": man.get(pid, {}).get("level", "L0"),
        "chars": man.get(pid, {}).get("chars", 0),
        "code": D[pid].get("code", ""), "venue": D[pid].get("venue", "arXiv preprint"),
        "note": NOTE.get(pid, ""),
        "problem": D[pid]["problem"], "method": D[pid]["method"],
        "key_numbers": D[pid]["key_numbers"], "ablation": D[pid]["ablation"],
        "baselines": D[pid]["baselines"], "datasets": D[pid]["datasets"],
        "novelty": D[pid]["novelty"], "limitations": D[pid]["limitations"],
        "trl_evidence": D[pid]["trl_evidence"],
    })

rows.sort(key=lambda r: (-r["value"], -r["scores"]["IMP"], -r["scores"]["NOV"], r["id"]))
print("按值排序（主批）:")
for r in [x for x in rows if not x["batch"].startswith("backfill")]:
    print(f"  {r['value']:.2f} {r['id']} {r['track']:<8s} {r['title_zh'][:42]}")

json.dump(rows, open(f"data/scored_{MMDD}.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("\nscored ->", len(rows), "| 主批", sum(1 for r in rows if not r["batch"].startswith("backfill")),
      "| backfill", sum(1 for r in rows if r["batch"].startswith("backfill")))
