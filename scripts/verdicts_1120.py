# -*- coding: utf-8 -*-
"""2026-11-20 残差复核判定：对 nonxr 434 条逐条读（标题+摘要前两句）后写入 verdicts.jsonl。

判 1 口径 = 属于 12 收录赛道之一（decision_probe.py q2.1 定义），且服务 XR/AR/VR/MR 或提供
XR 管线可直接使用的技术。0 = 通用视觉/语言/机器人/医学/遥感/科学成像，不属任何赛道。
"""
import json

FLAG = {
    # batch_00
    "2611.23417": ("神经渲染", "沿指定相机路径生成视角流的自回归视角模型，属新视角合成"),
    "2611.23534": ("系统与平台", "智能眼镜 2020-2026 系统综述，XR 设备层直接参考"),
    "2611.23674": ("系统与平台", "智能眼镜图像超分/复原课程学习，VLM 视觉辅助前置"),
    "2611.23727": ("世界模型与仿真", "分层 holon 场景生成，面向可扩展世界建模"),
    "2611.23845": ("内容生成", "MLLM 闭环扩散的 3D 室内场景生成"),
    "2611.23891": ("评估与数据集", "隐藏视角重建与 3D 装配推理基准"),
    # batch_01
    "2611.24010": ("系统与平台", "可穿戴自我中心影像 DSLR 级增强，智能眼镜成像管线"),
    "2611.24193": ("世界模型与仿真", "MLLM 交互式世界模型，单图持久可编辑世界生成"),
    "2611.24253": ("内容生成", "按用户相机轨迹重拍视频，6-DoF 视角合成式内容编辑"),
    "2611.24408": ("评估与数据集", "交互式视频世界模型的场景刚性与动作一致性基准"),
    # batch_02
    "2611.24862": ("化身与人体", "语音与手势统一生成的说话化身驱动"),
    "2611.24869": ("世界模型与仿真", "可配置规则下的交互式世界建模"),
}

index = {e["n"]: e["id"] for e in json.load(open("data/residual_1120/index.json", encoding="utf-8"))}
byid = {v: k for k, v in index.items()}
lines, missing = [], []
for n in sorted(index):
    pid = index[n]
    if pid in FLAG:
        tr, why = FLAG[pid]
        lines.append(json.dumps({"n": n, "verdict": 1, "track": tr, "why": why}, ensure_ascii=False))
    else:
        lines.append(json.dumps({"n": n, "verdict": 0}, ensure_ascii=False))
for pid in FLAG:
    if pid not in byid:
        missing.append(pid)
open("data/residual_1120/verdicts.jsonl", "w", encoding="utf-8").write("\n".join(lines) + "\n")
print("verdicts", len(lines), "flagged", len(FLAG), "missing", missing)
