# -*- coding: utf-8 -*-
"""2026-11-12 定稿评分：合并 4 组 notes_content，写入主会话校准后的 7 维分与赛道 → scored_1112.json。

- batch 字段显式写入（2026-11-12 / backfill-1112），消费者脚本禁止默认值兜底。
- 门③ 现算（窗口 2026-10-13~2026-11-12，442 条入窗，Top10 均分 4.4370）→ today_max 4.08 < 4.4370
  → 非重磅日，无 S 级（全批无 ≥4.2 达线者）。
- 校准说明：子代理评分整体经复核，仅 2611.13628 维持 TEC 3（DTU 0.51 mm 未超 GSPrior 0.50 mm，
  且引理 2 为标量近似），其余沿用并核对 scores_why 与正文数字一致。
"""
import json
import glob

W = {"IMP": 0.20, "NOV": 0.20, "TEC": 0.15, "EXP": 0.15, "PER": 0.15, "TRL": 0.08, "REP": 0.07}

FINAL = {
    # id: (track, IMP, NOV, TEC, EXP, PER, TRL, REP)
    "2611.13626": ("内容生成", 4, 4, 4, 4, 5, 4, 3),
    "2611.13528": ("重建与SLAM", 4, 3, 5, 4, 4, 3, 4),
    "2611.13662": ("重建与SLAM", 4, 4, 4, 4, 4, 3, 2),
    "2611.14062": ("系统与平台", 4, 3, 4, 3, 5, 4, 2),
    "2611.13772": ("神经渲染", 4, 4, 3, 4, 4, 3, 2),
    "2611.13654": ("化身与人体", 4, 4, 3, 4, 3, 3, 4),
    "2611.13808": ("神经渲染", 4, 3, 4, 4, 4, 3, 2),
    "2611.13486": ("感知与认知", 3, 3, 4, 4, 4, 2, 4),
    "2611.12912": ("空间计算与UI", 3, 3, 4, 3, 3, 4, 4),
    "2611.13280": ("神经渲染", 3, 3, 4, 4, 4, 2, 2),
    "2611.13628": ("重建与SLAM", 3, 3, 3, 4, 4, 3, 2),
    "2611.14029": ("感知与认知", 3, 3, 3, 4, 3, 2, 3),
    "2611.14389": ("触觉与多模态", 3, 3, 3, 3, 3, 2, 3),
    "2611.13906": ("交互与输入", 3, 3, 4, 2, 2, 2, 3),
    "2611.13296": ("系统与平台", 2, 2, 2, 1, 1, 1, 1),
    # backfill-1112（旧稿 v2/v3 再公告，首次入馆）
    "2505.20858": ("重建与SLAM", 4, 4, 5, 5, 4, 3, 3),
    "2605.22715": ("化身与人体", 4, 4, 4, 4, 4, 3, 3),
    "2608.04971": ("空间计算与UI", 3, 3, 3, 4, 4, 3, 4),
    "2503.00868": ("内容生成", 3, 4, 4, 2, 4, 2, 2),
}

TITLE_ZH = {
    "2611.13626": "FlashMotion：超快长时序 3D 动作生成",
    "2611.13528": "GEMOR-GS：全局外参精化的 3DGS SLAM 建图与在线重定位",
    "2611.13662": "NIF-VIO：跨惯性／非惯性参考系的视觉-惯性里程计",
    "2611.14062": "建筑机器人的人在环控制范式：从 VR 遥操作到半自治双臂作业",
    "2611.13772": "RF3DGS：自先验的无反射 3D 高斯泼溅",
    "2611.13654": "EgoHMP：以第一视角线索在 3D 场景中精确预测人体运动",
    "2611.13808": "FastWild-GS：紧凑逐图外观自适应的分钟级野外高斯泼溅",
    "2611.13486": "第一视角视频中的手-物接触转场检测",
    "2611.12912": "大范围空间对齐锚点：借外部漂移校正追踪扩展 XR 锚点精度",
    "2611.13280": "RetinexGS：Retinex 启发的低照 RAW 高斯泼溅重建",
    "2611.13628": "DepthGS：深度引导与自适应正则的高质量表面重建高斯泼溅",
    "2611.14029": "在哪里即兴？真实与虚拟 XR 空间对音乐创造力、共在感、情绪与心流的影响",
    "2611.14389": "面向三维形状触觉传达的编码策略评估",
    "2611.13906": "刺激消失式 MR P300 界面的目标选择：可行性与可区分线索对比",
    "2611.13296": "XR 实时三维元胞自动机仿真的统一交互框架",
    "2505.20858": "TFD-SfM：无轨迹稠密运动恢复结构",
    "2605.22715": "AnyMo：野外人体运动的几何感知与设置无关建模",
    "2608.04971": "探索投影与头显之间的跨现实转场：面向沉浸式数字艺术",
    "2503.00868": "物理驱动的单目视频动态流体资产提取：生成式 3DGS",
}

TITLE_EN = {
    "2611.13626": "FlashMotion: Ultra-Fast Long-Term 3D Motion Generation",
    "2611.13528": "GEMOR-GS: Global Extrinsic-calibration-refined Mapping and Online Relocalization for 3D Gaussian-Splatting SLAM",
    "2611.13662": "NIF-VIO: Visual--Inertial Odometry Across Inertial and Non-Inertial Reference Frames",
    "2611.14062": "A human-in-the-loop Control Paradigm for Construction Robotics: From VR-Guided Teleoperation to Semi-Autonomous Dual-Arm Operation",
    "2611.13772": "RF3DGS: Reflection-Free 3D Gaussian Splatting with Self-Priors",
    "2611.13654": "EgoHMP: Achieving Precise Human Motion Prediction in 3D Scenes via Egocentric Cues",
    "2611.13808": "FastWild-GS: Minutes-Scale In-the-Wild Gaussian Splatting via Compact Per-Image Appearance Adaptation",
    "2611.13486": "Hand-Object Contact Transition Detection in Egocentric Video",
    "2611.12912": "Large-area Spatially Aligned Anchors",
    "2611.13280": "RetinexGS: Retinex-Inspired Gaussian Splatting for Low-Light RAW Reconstruction",
    "2611.13628": "DepthGS: Depth-Guided Gaussian Splatting with Adaptive Regularization for High-Quality Surface Reconstruction",
    "2611.14029": "Where do we Jam? - The Impact of Real and Virtual XR Spaces on Musical Creativity, Co-Presence, Affect, and Flow",
    "2611.14389": "Evaluating Tactile Encoding Strategies for Communicating 3-D Shape",
    "2611.13906": "Target Selection with a Disappearing-Stimulus Mixed-Reality P300 Interface: Feasibility and Object-Distinguishable Versus Uniform Cues",
    "2611.13296": "A Unified Interactive Framework for Real-Time Three-Dimensional Cellular Automata Simulation in XR",
    "2505.20858": "Track-Free Dense Structure from Motion",
    "2605.22715": "AnyMo: Geometry-Aware Setup-Agnostic Modeling of Human Motion in the Wild",
    "2608.04971": "Exploring Cross-Reality Transitions between Projections and Head-Mounted Displays for Immersive Digital Art",
    "2503.00868": "Physics-Driven Extraction of Dynamic Fluid Asset from Monocular Video with Generative 3DGS",
}

cands = json.load(open("data/cands_1112.json", encoding="utf-8"))
meta = json.load(open("data/meta_1112.json", encoding="utf-8"))
G3 = json.load(open("data/gates_1112.json", encoding="utf-8"))
man = json.load(open("data/fulltext/_manifest.json", encoding="utf-8"))

content = {}
for f in sorted(glob.glob("data/notes_content_1112_g*.json")):
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
    today_max = 4.08
    if value >= 4.2 and today_max < g3:
        grade = "A"
        note = f"达 S 线但当日最高 {today_max:.2f} < 库内近30天 Top10 均分 {g3:.4f}，按校准关记 A（非重磅日）"
    if batch.startswith("backfill") and value >= 4.2:
        grade = "A"
        note = "backfill 不参与重磅日判定，≥4.2 记 A"
    c = content[pid]
    return {
        "id": pid,
        "title": TITLE_EN[pid],
        "title_zh": TITLE_ZH[pid],
        "track": tr,
        "venue": f"arXiv preprint（{meta.get(pid, {}).get('primary', 'cs.CV')}）" if pid in meta else "arXiv preprint",
        "batch": batch,
        "date": "2026-11-12",
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


main = [build(p, "2026-11-12") for p in cands["main"]]
bf = [build(p, "backfill-1112") for p in cands["backfill"]]
main.sort(key=lambda x: (-x["value"], -(x["scores"]["IMP"] + x["scores"]["NOV"]), x["id"]))
bf.sort(key=lambda x: (-x["value"], x["id"]))

# Top10：主批按加权降序，门② 赛道覆盖 ≥5（本批纯值前 10 已覆盖 7 赛道，无需回补）
top = main[:10]
tracks = [p["track"] for p in top]
assert len(set(tracks)) >= 5, set(tracks)

out = {
    "date": "2026-11-12",
    "gate3_mean": G3["gate3_mean"],
    "heavy_day": max(p["value"] for p in main) >= G3["gate3_mean"],
    "main": main,
    "backfill": bf,
    "top10_ids": [p["id"] for p in top],
    "top10_backfill_ids": [p["id"] for p in bf],
}
json.dump(out, open("data/scored_1112.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print(f"main={len(main)} bf={len(bf)} heavy={out['heavy_day']} max={max(p['value'] for p in main):.2f} gate3={G3['gate3_mean']:.4f}")
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
