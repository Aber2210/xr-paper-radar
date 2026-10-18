#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""把 2026-09-21 批次的 27 篇追加进 papers/library/registry.jsonl（幂等：按 id 去重）。"""
import json
import os

RAW = "data/raw/2026-09-21_new.jsonl"
REG = "papers/library/registry.jsonl"
MANI = "data/fulltext/_manifest.json"

# id -> (title_zh, track, scores, value, grade, status, flags_note)
META = {
    "2609.18473": ("CADSplat：CAD 先验正则的稀疏视角 3DGS 数字孪生", "神经渲染",
                   {"IMP": 5, "NOV": 4, "TEC": 5, "EXP": 4, "PER": 4, "TRL": 4, "REP": 3}, 4.28, "S"),
    "2609.18898": ("NormLift：特征提升的闭式解与语义可靠性", "神经渲染",
                   {"IMP": 4, "NOV": 5, "TEC": 5, "EXP": 3, "PER": 4, "TRL": 3, "REP": 4}, 4.12, "A"),
    "2609.17814": ("GazeDiT：空间条件化的注视精确扩散生成", "渲染与显示",
                   {"IMP": 5, "NOV": 4, "TEC": 4, "EXP": 5, "PER": 3, "TRL": 3, "REP": 3}, 4.05, "A"),
    "2609.18634": ("GenStream：语义流式与生成式重建", "系统与平台",
                   {"IMP": 5, "NOV": 5, "TEC": 3, "EXP": 2, "PER": 5, "TRL": 2, "REP": 4}, 3.94, "A"),
    "2609.18632": ("VibeAvatar：语音运动学与美学策略解耦的说话人化身", "化身与人体",
                   {"IMP": 4, "NOV": 4, "TEC": 4, "EXP": 4, "PER": 4, "TRL": 4, "REP": 3}, 3.93, "A"),
    "2609.17909": ("Zing-0.5：5B 可玩世界模型（动作+文本联合控制）", "世界模型与仿真",
                   {"IMP": 4, "NOV": 4, "TEC": 4, "EXP": 3, "PER": 4, "TRL": 4, "REP": 4}, 3.85, "A"),
    "2609.18232": ("UMI-Bridge：动作锚定的跨本体潜空间对齐", "交互与输入",
                   {"IMP": 3, "NOV": 4, "TEC": 4, "EXP": 4, "PER": 5, "TRL": 3, "REP": 3}, 3.80, "A"),
    "2609.18430": ("StrucPhysVideo：结构化 caption 驱动的物理视频世界模型", "世界模型与仿真",
                   {"IMP": 4, "NOV": 4, "TEC": 5, "EXP": 3, "PER": 3, "TRL": 3, "REP": 4}, 3.77, "A"),
    "2609.18548": ("HAP：手部驱动的第一人称 6-DoF 头动预测", "感知与认知",
                   {"IMP": 5, "NOV": 4, "TEC": 4, "EXP": 3, "PER": 3, "TRL": 3, "REP": 3}, 3.75, "A"),
    "2609.18624": ("MoQSplat：基于 MoQ 的 3DGS 渐进流式传输", "系统与平台",
                   {"IMP": 5, "NOV": 4, "TEC": 4, "EXP": 2, "PER": 3, "TRL": 4, "REP": 4}, 3.75, "A"),
    "2609.17810": ("Wind on Trees：4DGS 动态重建的物理基础检验", "神经渲染",
                   {"IMP": 4, "NOV": 4, "TEC": 5, "EXP": 4, "PER": 2, "TRL": 2, "REP": 4}, 3.69, "A"),
    "2609.17688": ("CapMem：第一人称视频字幕情景记忆基准", "评估与数据集",
                   {"IMP": 4, "NOV": 3, "TEC": 4, "EXP": 4, "PER": 3, "TRL": 3, "REP": 5}, 3.64, "A"),
    "2609.18650": ("Project Kitchen：VR 游戏化机器人数据采集", "交互与输入",
                   {"IMP": 3, "NOV": 3, "TEC": 4, "EXP": 4, "PER": 4, "TRL": 3, "REP": 3}, 3.45, "B"),
    "2609.18732": ("PASSAGE：场景对齐的人形穿越运动学习", "化身与人体",
                   {"IMP": 2, "NOV": 3, "TEC": 4, "EXP": 5, "PER": 4, "TRL": 3, "REP": 3}, 3.40, "B"),
    "2609.18893": ("SOL-SLAM：逆合成高斯-牛顿声呐稠密 SLAM", "重建与SLAM",
                   {"IMP": 2, "NOV": 3, "TEC": 4, "EXP": 4, "PER": 4, "TRL": 4, "REP": 3}, 3.33, "B"),
    "2609.18514": ("ActiveScale：模型-数据-硬件协同的主动感知", "感知与认知",
                   {"IMP": 3, "NOV": 3, "TEC": 4, "EXP": 3, "PER": 3, "TRL": 3, "REP": 3}, 3.15, "B"),
    "2609.18483": ("EasyFashion：人-AI 共创服装设计与纸样生成", "化身与人体",
                   {"IMP": 2, "NOV": 3, "TEC": 4, "EXP": 4, "PER": 3, "TRL": 3, "REP": 3}, 3.10, "B"),
    "2609.18323": ("MiniMax-H3 物理世界推理能力评测", "评估与数据集",
                   {"IMP": 4, "NOV": 3, "TEC": 3, "EXP": 3, "PER": 2, "TRL": 2, "REP": 4}, 3.04, "B"),
    "2609.17728": ("RAF-VLA：未来表征对齐的端到端自动驾驶", "—（非 XR）",
                   {"IMP": 1, "NOV": 3, "TEC": 4, "EXP": 4, "PER": 3, "TRL": 3, "REP": 3}, 2.90, "C"),
    "2609.18193": ("WAVE-Go：世界模型驱动的可中断执行导航", "—（非 XR）",
                   {"IMP": 1, "NOV": 3, "TEC": 4, "EXP": 4, "PER": 3, "TRL": 3, "REP": 3}, 2.90, "C"),
    "2609.18413": ("GaitWorld：词汇引导的步态识别", "—（非 XR）",
                   {"IMP": 1, "NOV": 3, "TEC": 4, "EXP": 4, "PER": 3, "TRL": 2, "REP": 4}, 2.89, "C"),
    "2609.18737": ("Geometry beneath the Waves：水下稀疏 3DGS 稠密先验", "神经渲染",
                   {"IMP": 3, "NOV": 3, "TEC": 3, "EXP": 2, "PER": 3, "TRL": 2, "REP": 3}, 2.77, "C"),
    "2609.18853": ("基于自由能最小化的人机交互调节", "交互与输入",
                   {"IMP": 3, "NOV": 3, "TEC": 4, "EXP": 2, "PER": 2, "TRL": 2, "REP": 3}, 2.77, "C"),
    "2609.18442": ("RiskWorld：流引导占据演化的风险感知世界模型", "—（非 XR）",
                   {"IMP": 1, "NOV": 3, "TEC": 4, "EXP": 3, "PER": 3, "TRL": 3, "REP": 3}, 2.75, "C"),
    "2609.18434": ("MR-Robotics LAB：无硬件混合现实机器人实验室", "空间计算与UI",
                   {"IMP": 3, "NOV": 2, "TEC": 3, "EXP": 2, "PER": 2, "TRL": 4, "REP": 3}, 2.58, "C"),
    "2609.18326": ("UAV 具身智能综述", "—（非 XR）",
                   {"IMP": 2, "NOV": 2, "TEC": 3, "EXP": 1, "PER": 1, "TRL": 2, "REP": 3}, 1.92, "C"),
    "2609.19216": ("4D 毫米波雷达感知算法综述", "—（非 XR）",
                   {"IMP": 1, "NOV": 1, "TEC": 3, "EXP": 1, "PER": 1, "TRL": 2, "REP": 3}, 1.52, "C"),
}

TOP10 = ["2609.18473", "2609.18898", "2609.17814", "2609.18634", "2609.18632",
         "2609.17909", "2609.18232", "2609.18430", "2609.18548", "2609.18624"]

# 技术路线级落后/存疑登记（论文级 status 仍为 CURRENT）
FLAGS = {
    "2609.18634": "⚠️ 路线落后（部分）：2D sprite 合成，作者自承应转体积化",
    "2609.17909": "⚠️ 与库内 Astronex-World（2609.20034）同期同规模竞争，WBench 口径需复测",
    "2609.18898": "⚠️ 依赖 CLIP 单位球假设",
    "2609.18632": "⚠️ 基于 LIA(2022) 潜 warp 空间",
    "2609.18624": "⚠️ 仅原型验证，无端到端带宽/QoE 数字",
    "2609.18737": "※ 摘要被 arXiv 截断，评分可信度低",
}


def main():
    mani = json.load(open(MANI, encoding="utf-8")) if os.path.exists(MANI) else {}
    have = set()
    if os.path.exists(REG):
        for line in open(REG, encoding="utf-8"):
            line = line.strip()
            if line:
                have.add(json.loads(line)["id"])

    rows = [json.loads(l) for l in open(RAW, encoding="utf-8")]
    added = 0
    with open(REG, "a", encoding="utf-8") as f:
        for r in rows:
            bid = r["base_id"]
            pid = f"arXiv:{bid}"
            if pid in have:
                continue
            zh, track, scores, value, grade = META[bid]
            m = mani.get(bid, {})
            rec = {
                "id": pid,
                "title": r["title"],
                "title_zh": zh,
                "track": track,
                "date": r["published"][:10],
                "value": value,
                "grade": grade,
                "scores": scores,
                "status": "CURRENT",
                "evidence": m.get("evidence", "ABSTRACT_ONLY"),
                "fetch_level": m.get("level", "-"),
                "fulltext_chars": m.get("chars", 0),
                "in_top10": bid in TOP10,
                "batch": "2026-09-21",
                "flags": [FLAGS[bid]] if bid in FLAGS else [],
            }
            f.write(json.dumps(rec, ensure_ascii=False) + "\n")
            have.add(pid)
            added += 1

    total = sum(1 for l in open(REG, encoding="utf-8") if l.strip())
    print(f"新增 {added} 条，registry 累计 {total} 条")


if __name__ == "__main__":
    main()
