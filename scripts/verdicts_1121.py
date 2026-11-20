"""2026-11-21 残差复核判读落盘：431 条 nonxr 逐条判定，1 = 属于 12 赛道之一（应收录）。"""
import json

idx = json.load(open("data/residual_1121/index.json", encoding="utf-8"))
nmap = {r["id"]: r["n"] for r in idx}

HITS = {
    "2611.25166": ("化身与人体", "人-物协同运动合成，接触约束下的人类动作生成（化身/动画管线）"),
    "2611.25389": ("内容生成", "少视图条件下生成等距柱状全景，可作沉浸式场景背景"),
    "2611.25696": ("神经渲染", "把语言控制图像融合提升到自由视点 3D 场景，属新视角合成"),
    "2611.25801": ("化身与人体", "快速人体估计，直接预测骨架关节与稠密表面点（虚拟化身驱动）"),
    "2611.25802": ("世界模型与仿真", "增量式 3D 场景生成，可随新观测持续扩展/修订三维世界"),
    "2611.25838": ("世界模型与仿真", "交互式游戏世界的动态上下文视频渲染（生成式渲染器）"),
    "2611.26433": ("重建与SLAM", "稀疏多视图下连续时间 3D 动力学重建与任意时刻位置预测"),
}

lines = []
for r in idx:
    n, pid = r["n"], r["id"]
    if pid in HITS:
        tr, why = HITS[pid]
        lines.append(json.dumps({"n": n, "verdict": 1, "track": tr, "why": why}, ensure_ascii=False))
    else:
        lines.append(json.dumps({"n": n, "verdict": 0}, ensure_ascii=False))

open("data/residual_1121/verdicts.jsonl", "w", encoding="utf-8").write("\n".join(lines) + "\n")
print("verdicts", len(lines), "hits", len(HITS), [nmap[p] for p in HITS])
