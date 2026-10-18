#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""2026-10-07 准备：从 fresh 候选中筛 XR 相关，分配赛道，输出 corpus.jsonl。
XR 判定依据标题+摘要；非 XR（导盲机器人/自动驾驶/显微镜/音频编解码/纯社交HCI/纯机器人导航）剔除。
"""
import json, os

FRESH = "data/raw/2026-10-07_fresh.jsonl"
OUT = "data/2026-10-07_corpus.jsonl"

# base_id -> (track, 是否XR相关, 备注)
TRIAGE = {
    "2610.04007": ("神经渲染", True,  "VolS-GS 可重光照高斯泼溅+次表面散射"),
    "2610.04013": ("重建与SLAM", True, "MAV 返航可行探索+3DGS 重建"),
    "2610.04076": ("神经渲染", True,  "VCURF 辐射场像素级不确定性"),
    "2610.04139": ("空间计算与UI", True, "SpatialMind 预测式空间推理 VLM"),
    "2610.04203": ("神经渲染", True,  "Sparse-GS2Mesh 稀疏视角表面重建"),
    "2610.04336": ("世界模型与仿真", True, "3DGS-SPH 拉格朗日耦合可微物理"),
    "2610.04351": ("神经渲染", True,  "LoCoSplat 实时前馈 3DGS"),
    "2610.04506": ("评估与数据集", True, "EgoExo-Next 自我中心视觉推理基准"),
    "2610.04606": ("神经渲染", True,  "Sparse-View 4DGS 时空先验"),
    "2610.04689": ("化身与人体", True,  "Neuroll 实时神经发丝仿真"),
    "2610.04883": ("重建与SLAM", True,  "反射鲁棒 6DoF 跟踪+光场"),
    "2610.05013": ("评估与数据集", True, "EMBER-Bench 跨事件因果记忆基准"),
    "2610.05081": ("触觉与多模态", True,  "数字孪生遥操作+力/视觉反馈"),
    "2610.05207": ("重建与SLAM", True,  "F^2 SLAM 前馈几何→持久因子"),
    "2610.05233": ("化身与人体", True,  "PixReenact 头部化身重演"),
    "2610.05289": ("神经渲染", True,  "Mobile-4DGS 移动端实时动态高斯"),
    "2610.05526": ("空间计算与UI", True,  "自我中心助手空间对话记忆"),
    "2610.05576": ("神经渲染", True,  "SteadySplats 低方差高斯重采样随机渲染"),
    "2610.05610": ("触觉与多模态", True,  "SEA-LM 可穿戴空间音频理解"),
    "2610.05757": ("重建与SLAM", True,  "HDS 人在环神经符号 SLAM 漂移预测"),
    "2610.05772": ("空间计算与UI", True,  "VR 视觉假体智能导航"),
    "2610.06472": ("神经渲染", True,  "MaRO-GS 掩码鲁棒物体中心高斯"),
    "2610.06688": ("神经渲染", True,  "GS-Pool 3DGS 物体级变化检测"),
}

recs = [json.loads(l) for l in open(FRESH, encoding="utf-8")]
by_id = {r["base_id"]: r for r in recs}

corpus = []
for bid, (track, xr, note) in TRIAGE.items():
    r = by_id.get(bid)
    if not r:
        print("MISSING", bid); continue
    corpus.append({
        "base_id": bid,
        "arxiv_id": r["arxiv_id"],
        "title": r["title"],
        "abstract": r["abstract"],
        "primary_category": r["primary_category"],
        "published": (r.get("published") or "")[:10],
        "track": track,
        "xr": xr,
        "note": note,
    })

os.makedirs(os.path.dirname(OUT), exist_ok=True)
with open(OUT, "w", encoding="utf-8") as f:
    for c in corpus:
        f.write(json.dumps(c, ensure_ascii=False) + "\n")
print(f"corpus XR 候选 = {len(corpus)} → {OUT}")
# 赛道分布
from collections import Counter
print("赛道分布:", dict(Counter(c["track"] for c in corpus)))
