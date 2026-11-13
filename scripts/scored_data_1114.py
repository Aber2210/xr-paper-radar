# -*- coding: utf-8 -*-
"""2026-11-14 定稿评分：合并 4 组 notes_content → scored_1114.json。

- batch 字段显式写入（2026-11-14 / backfill-1114），消费者脚本禁止默认值兜底。
- 门③ 现算（窗口 2026-10-15~2026-11-14，428 条入窗，Top10 均分 4.4100）→ today_max 4.15 < 4.4100
  → 非重磅日，无 S 级。
- 主会话校准：
  ① 2611.15153 MatrixSplat TRL 4→3（正文仅「will release」无仓库，按 rubric「开源代码」未满足）；
  ② 2611.17331 TTB TRL 4→3（仅项目页有结果可视化，无代码仓库）；
  ③ 2611.16793 EG360 赛道 系统与平台→重建与SLAM（深度估计属重建/几何，非系统平台）；
  ④ 其余沿用子代理评分，逐条核对 scores_why 与正文数字（MatrixSplat 599.9/702.6/510.9 FPS、
     riMESA 45.09% vs 352.81%/787.30%、Instant NuRec 28.26 dB/+2.01 dB 均已回文核对）。
- 门② 纯值 Top10 仅 4 赛道（重建与SLAM×6）→ 触发一次重筛：剔除重复赛道最低分 SteinPnP 3.50，
  回补未覆盖赛道最高分 MRxD 3.17（空间计算与UI，XR 核心赛道）→ 定稿 5 赛道。
"""
import json
import glob

W = {"IMP": 0.20, "NOV": 0.20, "TEC": 0.15, "EXP": 0.15, "PER": 0.15, "TRL": 0.08, "REP": 0.07}

FINAL = {
    # id: (track, IMP, NOV, TEC, EXP, PER, TRL, REP)
    "2611.15153": ("渲染与显示", 4, 4, 4, 5, 5, 3, 3),
    "2611.16012": ("重建与SLAM", 4, 4, 5, 4, 4, 3, 4),
    "2611.16840": ("重建与SLAM", 5, 3, 4, 5, 4, 3, 2),
    "2611.16259": ("神经渲染", 4, 4, 4, 4, 4, 3, 3),
    "2611.17331": ("神经渲染", 4, 4, 4, 4, 4, 3, 3),
    "2611.14895": ("重建与SLAM", 4, 4, 4, 4, 3, 3, 2),
    "2611.15435": ("重建与SLAM", 4, 3, 4, 4, 4, 3, 2),
    "2611.15429": ("重建与SLAM", 4, 3, 3, 4, 4, 3, 4),
    "2611.15561": ("交互与输入", 4, 4, 3, 3, 3, 4, 4),
    "2611.15437": ("重建与SLAM", 3, 4, 4, 4, 4, 2, 2),
    "2611.16793": ("重建与SLAM", 3, 3, 4, 4, 4, 3, 3),
    "2611.15802": ("交互与输入", 3, 3, 3, 3, 4, 3, 4),
    "2611.16171": ("空间计算与UI", 4, 4, 3, 3, 2, 2, 3),
    "2611.16472": ("评估与数据集", 4, 2, 4, 4, 2, 3, 3),
    "2611.15526": ("化身与人体", 3, 3, 3, 4, 3, 3, 2),
    "2611.17018": ("交互与输入", 3, 3, 3, 3, 2, 2, 3),
    "2611.16056": ("感知与认知", 3, 3, 2, 3, 3, 2, 3),
    "2611.15143": ("重建与SLAM", 2, 2, 2, 3, 1, 1, 4),
    "2611.16446": ("感知与认知", 3, 2, 1, 1, 1, 1, 1),
    "2611.16594": ("交互与输入", 2, 2, 1, 1, 1, 1, 1),
    # backfill-1114（旧稿 v2 再公告，首次入馆）
    "2603.01178": ("重建与SLAM", 5, 4, 5, 5, 4, 4, 4),
    "2607.14203": ("世界模型与仿真", 5, 4, 4, 4, 5, 4, 3),
    "2510.03857": ("神经渲染", 4, 3, 4, 4, 4, 4, 4),
    "2605.21714": ("交互与输入", 4, 3, 4, 5, 4, 3, 2),
    "2603.09741": ("评估与数据集", 4, 3, 3, 3, 4, 3, 5),
    "2607.05243": ("重建与SLAM", 4, 3, 4, 3, 3, 3, 4),
    "2508.16731": ("评估与数据集", 4, 3, 3, 2, 4, 3, 5),
    "2512.10095": ("渲染与显示", 3, 3, 4, 3, 3, 2, 2),
}

TITLE_ZH = {
    "2611.15153": "MatrixSplat：面向 GPU 的矩阵并行、特征可扩展 3D Gaussian Splatting（3D 高斯泼溅）渲染",
    "2611.16012": "面向第一人称视频的拓扑感知 4D Gaussian Splatting（Topo-4DGS）与 TopoEgo 基准",
    "2611.16840": "Kosmo-GFM：面向生产的几何基础模型",
    "2611.16259": "能重建多少就重建多少：无干扰物的 4D Gaussian Splatting（4D 高斯泼溅）",
    "2611.17331": "TTB：面向 decoder-only 视角合成模型的测试时烘焙加速渲染",
    "2611.14895": "HeadIO：面向头戴设备的体坐标系航向分解神经惯性里程计",
    "2611.15435": "ThermalSplat：面向稀疏视角热红外三维重建的可泛化无位姿 Gaussian Splatting",
    "2611.15429": "IncR-3DSGG：基于有位姿 RGB 图像的增量三维场景图生成与特权深度监督",
    "2611.15561": "基于通用粒子系统的沉浸式视觉遮蔽碰撞预防",
    "2611.15437": "SteinPnP：PnP 问题中的非参数位姿不确定性量化",
    "2611.16793": "EG360：基于自适应全景-透视蒸馏与球面跨层特征融合的高效可泛化 360° 深度估计",
    "2611.15802": "RUMI：面向机器人学习的 Robotiq 匹配型通用操作接口，结合增强现实（AR）与触觉反馈",
    "2611.16171": "MRxD：混合现实跨设备交互的使用模式框架",
    "2611.16472": "边缘端 RGB-D SLAM：在 Raspberry Pi 5 上基准测试与剖析 RTAB-Map 与 ORB-SLAM3",
    "2611.15526": "SCR-Mamba：骨架条件 Mamba 与跨尺度增量细化用于高效三维人体姿态估计",
    "2611.17018": "探索面向包容性小组对话的社会可接受 3D 反馈设计",
    "2611.16056": "BiScopeNet：文本引导的手别对齐用于第一视角子动作识别",
    "2611.15143": "基于 V-JEPA 特征的多视图三维重建",
    "2611.16446": "面向洪水危机管理中公民参与训练的严肃游戏（概念与研究议程）",
    "2611.16594": "通过沉浸式多用户游戏化进行语言学习（概念与实验设计）",
    "2603.01178": "riMESA：面向真实世界协同 SLAM 的共识 ADMM",
    "2607.14203": "Instant NuRec：面向驾驶场景仿真的前馈三维高斯重建",
    "2510.03857": "OMG4：面向高效动态场景表示的优化最小 4D Gaussian Splatting",
    "2605.21714": "AVI-HT：面向手套式 3D 手部追踪的自适应视觉–IMU 融合",
    "2603.09741": "ENIGMA-360：面向工业场景人类行为理解的自我–外部视角数据集",
    "2607.05243": "GUSH3R：单目视频前馈式动态人体–场景高斯重建",
    "2508.16731": "COSMO-Bench：协同 SLAM 优化基准",
    "2512.10095": "ReflFlow：几何引导光线追踪的动态高光重建",
}

TITLE_EN = {
    "2611.15153": "MatrixSplat: Matrix-Parallel and Feature-Scalable 3D Gaussian Splatting Rendering on GPUs",
    "2611.16012": "Topology-Aware 4D Gaussian Splatting for Egocentric Videos",
    "2611.16840": "Kosmo-GFM: A Production-Ready Geometry Foundation Model",
    "2611.16259": "Reconstruct What You Can: Distractor-free 4D Gaussian Splatting",
    "2611.17331": "TTB: Test-time Baking for Efficient Rendering of Decoder-only View Synthesis Models",
    "2611.14895": "HeadIO: Body-Frame Heading Decomposition for Neural Inertial Odometry on Head-Mounted Devices",
    "2611.15435": "ThermalSplat: Generalizable Pose-Free Gaussian Splatting for Sparse-View Thermal 3D Reconstruction",
    "2611.15429": "IncR-3DSGG: Incremental Posed RGB Image Based 3D Scene Graph Generation via Privileged Depth Supervision",
    "2611.15561": "Immersive Sight-Restriction-Based Collision Prevention Using Generic Particle Systems in Virtual Reality",
    "2611.15437": "SteinPnP: Non-Parametric Uncertainty Quantification in the Perspective-N-Point Problem",
    "2611.16793": "EG360: Efficient and Generalizable 360-degree Depth Estimation via Adaptive Panorama-Perspective Distillation and Spherical Cross-Level Feature Fusion",
    "2611.15802": "RUMI: A Robotiq-Matched Universal Manipulation Interface for Robot Learning with Augmented Reality and Haptic Feedback",
    "2611.16171": "MRxD: A Usage-Pattern Framework for Mixed-Reality Cross-Device Interaction",
    "2611.16472": "RGB-D SLAM on the Edge: Benchmarking and Profiling RTAB-Map and ORB-SLAM3 on the Raspberry Pi 5",
    "2611.15526": "SCR-Mamba: Skeleton-conditioned Mamba with Cross-Scale Incremental Refinement for Efficient 3D Human Pose Estimation",
    "2611.17018": "Exploring Socially Acceptable 3D Feedback Design for Inclusive Small-Group Conversation",
    "2611.16056": "Sub-actions in Action: Text-Guided Hand-Role Alignment for Sub-Action Recognition",
    "2611.15143": "Multi-View 3D Reconstruction Using V-JEPA Features",
    "2611.16446": "A Serious Game for Training Civil Participation in Flood Crisis Management",
    "2611.16594": "Language Learning through Immersive Multi-User Gamification",
    "2603.01178": "riMESA: Consensus ADMM for Real-World Collaborative SLAM",
    "2607.14203": "Instant NuRec: Feed-Forward 3D Gaussian Reconstruction for Driving Scene Simulation",
    "2510.03857": "Optimized Minimal 4D Gaussian Splatting for Efficient Dynamic Scene Representation",
    "2605.21714": "AVI-HT: Adaptive Vision-IMU Fusion for 3D Gloved Hand Tracking",
    "2603.09741": "ENIGMA-360: An Ego-Exo Dataset for Human Behavior Understanding in Industrial Scenarios",
    "2607.05243": "GUSH3R: Everyone Everywhere All at Once as Gaussians",
    "2508.16731": "COSMO-Bench: A Benchmark for Collaborative SLAM Optimization",
    "2512.10095": "ReflFlow: Learning Geometry-Guided Ray Tracing for Dynamic Specular Reconstruction",
}

# 门② 重筛后的定稿 Top10（列表迭代，禁用 set —— 11-05 踩坑）
TOP10_ORDER = ["2611.15153", "2611.16012", "2611.16840", "2611.16259", "2611.17331",
               "2611.14895", "2611.15435", "2611.15429", "2611.15561", "2611.16171"]

cands = json.load(open("data/candidates_1114.json", encoding="utf-8"))
G3 = json.load(open("data/gates_1114.json", encoding="utf-8"))
man = json.load(open("data/fulltext/_manifest.json", encoding="utf-8"))

content = {}
for f in sorted(glob.glob("data/notes_content_1114_g*.json")):
    for p in json.load(open(f, encoding="utf-8")):
        content[p["id"]] = p

assert set(content) == set(FINAL), (set(content) ^ set(FINAL))


def build(pid, batch):
    tr, *sc = FINAL[pid]
    scores = dict(zip(["IMP", "NOV", "TEC", "EXP", "PER", "TRL", "REP"], sc))
    value = round(sum(W[k] * scores[k] for k in W), 4)
    if value >= 4.2:
        grade, note = "S", ""
    elif value >= 3.6:
        grade, note = "A", ""
    elif value >= 3.0:
        grade, note = "B", ""
    else:
        grade, note = "C", ""
    g3 = G3["gate3_mean"]
    today_max = 4.15
    if value >= 4.2 and today_max < g3:
        grade = "A"
        note = f"达 S 线但当日最高 {today_max:.2f} < 库内近30天 Top10 均分 {g3:.4f}，按校准关记 A（非重磅日）"
    if batch.startswith("backfill") and value >= 4.2:
        grade = "A"
        note = "backfill 不参与重磅日判定，≥4.2 按口径记 A"
    c = content[pid]
    return {
        "id": pid,
        "title": TITLE_EN[pid],
        "title_zh": TITLE_ZH[pid],
        "track": tr,
        "venue": c["venue"],
        "batch": batch,
        "date": "2026-11-14",
        "value": value,
        "grade": grade,
        "grade_note": note,
        "scores": scores,
        "scores_why": c["scores_why"],
        "evidence": man[pid]["evidence"],
        "fetch_level": man[pid]["level"],
        "conclusion": c["conclusion"],
        "slug": c["slug"],
        "tags": c["tags"],
        "problem": c["problem"],
        "method": c["method"],
        "experiments": c["experiments"],
        "innovation": c["innovation"],
        "limits": c["limits"],
        "relation": c["relation"],
        "repro": c["repro"],
        "action": c["action"],
        "status": "CURRENT",
    }


main = [build(p, "2026-11-14") for p in cands["main"]]
bf = [build(p, "backfill-1114") for p in cands["backfill"]]
main.sort(key=lambda x: (-x["value"], -(x["scores"]["IMP"] + x["scores"]["NOV"]), x["id"]))
bf.sort(key=lambda x: (-x["value"], x["id"]))

TOP10 = [p for pid in TOP10_ORDER for p in main if p["id"] == pid]
assert [p["id"] for p in TOP10] == TOP10_ORDER, [p["id"] for p in TOP10]
tracks = [p["track"] for p in TOP10]
assert len(set(tracks)) >= 5, set(tracks)
assert max(p["value"] for p in main) == TOP10[0]["value"]

out = {
    "date": "2026-11-14",
    "gate3_mean": G3["gate3_mean"],
    "heavy_day": max(p["value"] for p in main) >= G3["gate3_mean"],
    "main": main,
    "backfill": bf,
    "top10_ids": TOP10_ORDER,
    "top10_backfill_ids": [p["id"] for p in bf],
}
json.dump(out, open("data/scored_1114.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print(f"main={len(main)} bf={len(bf)} heavy={out['heavy_day']} max={max(p['value'] for p in main):.2f} "
      f"gate3={G3['gate3_mean']:.4f}")
for p in main:
    print(f"  {p['value']:.2f} {p['grade']} {p['track']:8s} {p['id']} {p['title_zh'][:40]}")
print("-- backfill --")
for p in bf:
    print(f"  {p['value']:.2f} {p['grade']} {p['track']:8s} {p['id']} {p['title_zh'][:40]}")
print("top10 tracks:", {t: tracks.count(t) for t in sorted(set(tracks))})
allt = {}
for p in main:
    allt[p["track"]] = allt.get(p["track"], 0) + 1
print("all main tracks:", allt)
print("grades:", {g: sum(1 for p in main if p['grade'] == g) for g in 'SABC'})
