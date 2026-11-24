# -*- coding: utf-8 -*-
"""2026-11-25 定稿评分：合并 6 组 digest（主批 68 = 62 直接候选 + 6 残差采纳；backfill 6），
主会话按标准权重逐篇校准后落 scored。

权重 IMP .20 / NOV .20 / TEC .15 / EXP .15 / PER .15 / TRL .08 / REP .07。
评分锚点：库内 4.50+（riMESA 4.50 / Open-HumanScale 4.57 / Map2SLAM 4.57 / AnyVIO 4.43）为能力级工作；
本批 4.21（HoloSplat）属「重要且工程完整但非能力级」，不与 S 级锚点并置，且门③未过则按口径记 A。
"""
import json, sys
sys.path.insert(0, "scripts")
from grade_caliber import assign_grade

W = {"IMP": .20, "NOV": .20, "TEC": .15, "EXP": .15, "PER": .15, "TRL": .08, "REP": .07}
MMDD, DAY = "1125", "2026-11-25"

S = {
    # ---- 主批 ----
    "2611.28020": (4, 4, 4, 4, 3, 3, 3),   # SoundFleXR XR 音频维度约束
    "2611.28027": (3, 3, 3, 2, 2, 4, 4),   # 无代码可穿戴验证工具链
    "2611.28056": (3, 3, 4, 4, 3, 3, 3),   # NAVIQUAL-XR
    "2611.28085": (4, 4, 4, 4, 4, 4, 2),   # UbiEnlight 智能眼镜低光
    "2611.28090": (3, 4, 4, 3, 4, 2, 2),   # Ego-HAR 双表征重建
    "2611.28111": (3, 4, 4, 4, 3, 2, 2),   # GC-GS 梯度冲突
    "2611.28136": (4, 4, 4, 4, 4, 2, 2),   # Engram 世界模型记忆
    "2611.28193": (4, 3, 4, 4, 5, 3, 4),   # FastD4RT
    "2611.28520": (4, 4, 4, 4, 4, 3, 4),   # VG3R
    "2611.28636": (3, 3, 4, 4, 5, 3, 4),   # SemGuard GS 水印
    "2611.28649": (4, 4, 4, 4, 5, 3, 4),   # S-Mind
    "2611.28665": (4, 4, 4, 4, 3, 2, 4),   # CoT 破坏空间 VQA
    "2611.28666": (4, 4, 4, 4, 4, 2, 2),   # RecallWorld
    "2611.28670": (3, 4, 4, 4, 4, 2, 2),   # 跨模态高斯深度
    "2611.28673": (3, 4, 3, 4, 4, 2, 2),   # ViewAgent3D
    "2611.28682": (4, 4, 4, 4, 4, 2, 2),   # CHORD
    "2611.28792": (4, 4, 4, 3, 3, 2, 2),   # ArgsWorld
    "2611.28793": (4, 4, 4, 4, 4, 2, 2),   # STAC++
    "2611.28802": (3, 4, 4, 4, 3, 2, 2),   # 稀疏视图 3DGS 平坦性
    "2611.28878": (4, 4, 4, 3, 5, 2, 2),   # Paintress
    "2611.28913": (3, 4, 4, 4, 4, 2, 2),   # Morton 稀疏映射
    "2611.28939": (3, 4, 4, 3, 4, 3, 2),   # T-Tac
    "2611.28979": (3, 3, 4, 4, 4, 2, 3),   # AlignHand
    "2611.29026": (4, 4, 4, 4, 3, 4, 2),   # RAGA
    "2611.29059": (3, 4, 4, 4, 4, 2, 2),   # PoinTTT
    "2611.29112": (4, 4, 3, 4, 3, 2, 3),   # 去中心化多视图空间推理
    "2611.29163": (4, 4, 4, 4, 4, 3, 4),   # 包容性手部姿态
    "2611.29168": (4, 4, 3, 4, 4, 3, 2),   # SpatialDuet
    "2611.29218": (3, 4, 4, 4, 4, 2, 4),   # Ego-HMB
    "2611.29236": (4, 4, 4, 4, 5, 3, 2),   # 高斯泼溅互补几何
    "2611.29240": (3, 3, 4, 4, 4, 4, 4),   # Tacinf
    "2611.29293": (3, 4, 4, 4, 4, 2, 2),   # GALILEO
    "2611.29376": (4, 4, 4, 4, 3, 3, 2),   # Chameleon VR
    "2611.29389": (4, 4, 4, 4, 4, 3, 2),   # PINE
    "2611.29614": (4, 4, 4, 4, 4, 3, 3),   # GravHMR
    "2611.29647": (4, 3, 3, 4, 3, 2, 2),   # 沉浸式视频纵向效应（PARTIAL）
    "2611.29678": (4, 4, 4, 4, 4, 3, 3),   # Ref2Light 裸眼 3D
    "2611.29693": (3, 3, 4, 4, 4, 3, 4),   # HandiVid
    "2611.29838": (4, 4, 4, 4, 4, 2, 2),   # 连续时间 4D 重建
    "2611.29897": (3, 4, 4, 4, 4, 4, 3),   # Motion Mamba 2.0
    "2611.29920": (3, 4, 4, 4, 4, 3, 4),   # 事件+结构先验动态高斯
    "2611.30012": (3, 4, 3, 3, 3, 2, 4),   # FlexGaze（PARTIAL）
    "2611.30042": (4, 4, 4, 4, 5, 2, 2),   # SWAM
    "2611.30102": (4, 4, 4, 4, 4, 3, 2),   # LMnOP
    "2611.30166": (4, 4, 4, 4, 3, 4, 2),   # 消费级 LiDAR 房间扫描
    "2611.30173": (4, 4, 4, 4, 3, 4, 2),   # Confidently Lost
    "2611.30184": (3, 4, 4, 3, 3, 3, 4),   # OmniSLAM
    "2611.30226": (3, 4, 4, 4, 4, 3, 4),   # VeriWorld
    "2611.30351": (3, 4, 4, 4, 4, 2, 2),   # NNS-GS
    "2611.30388": (3, 4, 4, 3, 3, 4, 2),   # BASE 对话化身
    "2611.30392": (4, 4, 4, 3, 4, 2, 2),   # LiquidGazeNet
    "2611.30461": (4, 4, 4, 4, 5, 4, 2),   # LiveMirror
    "2611.30552": (2, 2, 2, 1, 1, 3, 3),   # 具身对话实验装置（无评估）
    "2611.30572": (4, 4, 4, 4, 5, 3, 2),   # VeriTouch
    "2611.30597": (4, 4, 4, 4, 5, 3, 4),   # ViDiHand2
    "2611.30607": (4, 4, 4, 4, 4, 2, 2),   # Tri-DNO
    "2611.30629": (4, 4, 4, 4, 5, 2, 2),   # Fast-GSVC
    "2611.30734": (4, 4, 4, 4, 3, 3, 4),   # EgoDepth-Bench
    "2611.30777": (4, 4, 4, 4, 4, 3, 3),   # AvatarAnyone
    "2611.30787": (3, 4, 4, 4, 3, 3, 4),   # BridgeMVS
    "2611.30802": (4, 4, 4, 4, 5, 3, 3),   # Go Far, Look Less
    "2611.30898": (4, 4, 4, 4, 4, 3, 3),   # World Models as LAM
    "2611.31018": (3, 4, 4, 4, 5, 3, 2),   # DiffSimp
    "2611.31023": (4, 4, 4, 4, 4, 3, 2),   # WildAnySplat
    "2611.31140": (5, 4, 4, 4, 5, 4, 2),   # HoloSplat
    "2611.31143": (3, 4, 4, 4, 4, 2, 2),   # Head Anything
    "2611.31156": (4, 4, 4, 4, 5, 3, 2),   # 保局部性 token 锚点
    "2611.31215": (4, 4, 4, 4, 3, 3, 4),   # Seeking in Space
    # ---- backfill-1125（replace 旧稿）----
    "2511.20578": (4, 4, 4, 3, 3, 3, 2),   # 电触觉器件
    "2605.00389": (3, 3, 3, 4, 4, 3, 2),   # VR 游戏化训练
    "2607.11627": (3, 3, 4, 3, 3, 4, 4),   # IBPA 增量网格
    "2608.04701": (4, 4, 4, 4, 3, 3, 4),   # UniView 大基线 NVS
    "2608.28386": (4, 4, 4, 4, 4, 2, 2),   # GraspHOI
    "2610.41373": (4, 4, 3, 3, 4, 2, 2),   # Queryable Gaussian View Index
}

NOTE = {
    "2611.29647": "证据等级 PARTIAL（ar5iv 仅摘要落地页，无正文节）；TEC/EXP 按摘要级证据下调，量化结论仅摘要所述",
    "2611.30012": "证据等级 PARTIAL（ar5iv 仅摘要落地页，无正文节）；TEC/EXP/PER 按摘要级证据下调",
    "2611.30552": "研究仪器论文：全文无用户研究与性能指标，EXP/PER 记 1（诚实口径）",
    "2611.31140": "达 S 线（4.21 ≥ 4.20）但门③未过 → 按口径记 A，见报告档位说明",
    "2611.28027": "工具链论文，单穿戴者单服装、无公开数据集，EXP=2",
    "2511.20578": "旧稿（2025-11-25 首次提交）v10 再公告；backfill 批次不参与重磅日判定",
    "2605.00389": "旧稿（2026-05-01 首次提交）v3 再公告；backfill 批次不参与重磅日判定",
    "2607.11627": "旧稿（2026-07-16 首次提交）v2 再公告；backfill 批次不参与重磅日判定",
    "2608.04701": "旧稿（2026-08-05 首次提交）v3 再公告；正文标题为 UniView",
    "2608.28386": "旧稿（2026-08-28 首次提交）v3 再公告；backfill 批次不参与重磅日判定",
    "2610.41373": "旧稿（2026-10-30 首次提交）v2 再公告；backfill 批次不参与重磅日判定",
}

D = {}
for g in range(1, 7):
    for x in json.load(open(f"data/digest_1125_g{g}.json", encoding="utf-8")):
        D[x["id"]] = x

cand = json.load(open("data/cand_1125.json", encoding="utf-8"))
bf = json.load(open("data/backfill_1125.json", encoding="utf-8"))
pub = json.load(open("data/published_1125.json", encoding="utf-8"))
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
    else:
        track, batch, announce = cand[pid]["track"], DAY, cand[pid].get("announce", "")
        recall = cand[pid].get("recall", "")
        title = cand[pid]["title"]
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
    print(f"  {r['value']:.2f} {r['id']} {r['track']:<8s} {r['title_zh'][:44]}")

json.dump(rows, open(f"data/scored_{MMDD}.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("\nscored ->", len(rows), "| 主批", sum(1 for r in rows if not r["batch"].startswith("backfill")),
      "| backfill", sum(1 for r in rows if r["batch"].startswith("backfill")))
