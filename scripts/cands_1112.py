# -*- coding: utf-8 -*-
"""2026-11-12 候选集构建：主批 15 篇（11-11 公告批次 XR 核心/强相关）+ backfill-1112 4 篇旧稿。

甄别口径：listing 摘要级 28 篇命中 → 剔非 XR 13 篇（自动驾驶 LiDAR 仿真/迷宫导航/开放词表检测/VLA 剪枝/WiFi-IMU 定位/
MCDA/康复触觉 dyad/Ego2Robot 综述/机器人策略/2DGS 图像编码/少步视频生成/AUV 轨迹跟踪/身体感知数据集）；
RSS 37 命中中 7 篇旧稿再公告 → 4 篇 XR 相关入 backfill（跨现实转场/可穿戴动捕/SfM/流体 3DGS），3 篇非 XR 剔除。
"""
import json

MAIN = ["2611.12912", "2611.13280", "2611.13296", "2611.13486", "2611.13528",
        "2611.13626", "2611.13628", "2611.13654", "2611.13662", "2611.13772",
        "2611.13808", "2611.13906", "2611.14029", "2611.14062", "2611.14389"]
BF = ["2608.04971", "2605.22715", "2505.20858", "2503.00868"]
REJECT = ["2611.12932", "2611.12949", "2611.12976", "2611.13030", "2611.13057",
          "2611.13062", "2611.13307", "2611.13610", "2611.13685", "2611.13784",
          "2611.14033", "2611.14373", "2611.14093"]

meta = json.load(open("data/meta_1112.json", encoding="utf-8"))
rss = {json.loads(l)["arxiv_id"].split("v")[0]: json.loads(l)
       for l in open("data/raw/2026-11-12.jsonl", encoding="utf-8")}

rows = []
for pid in MAIN + BF:
    if pid in meta:
        m = meta[pid]
        rows.append({"arxiv_id": pid, "base_id": pid, "title": m["title"],
                     "abstract": m["abstract"], "published": m["published"]})
    else:
        r = rss[pid]
        rows.append({"arxiv_id": r["arxiv_id"], "base_id": pid, "title": r["title"],
                     "abstract": r["abstract"], "published": r.get("published", "")[:10]})

with open("data/raw/2026-11-12_cands.jsonl", "w", encoding="utf-8") as f:
    for r in rows:
        f.write(json.dumps(r, ensure_ascii=False) + "\n")

cand = {"main": MAIN, "backfill": BF, "reject": REJECT,
        "reject_reason": {
            "2611.12932": "自动驾驶 LiDAR 仿真（AV 安全验证域，非 XR）",
            "2611.12949": "2D LiDAR 迷宫导航（ROS2 机器人栈）",
            "2611.12976": "开放词表目标检测（基础视觉任务）",
            "2611.13030": "VLA 视觉 token 剪枝（机器人推理加速）",
            "2611.13057": "WiFi-IMU 室内定位（无线指纹，非视觉/XR 追踪）",
            "2611.13062": "多准则决策参数诱导（MCDA，误命中）",
            "2611.13307": "康复机器人触觉 dyad（无 XR 显示/交互）",
            "2611.13610": "Ego2Robot 综述（机器人操作学习）",
            "2611.13685": "人类自视角视频辅助机器人策略（机器人学习）",
            "2611.13784": "2D 高斯图像编码（图像压缩码率优化）",
            "2611.14033": "少步流式视频生成（扩散蒸馏加速）",
            "2611.14373": "AUV 六自由度轨迹跟踪（水下控制）",
            "2611.14093": "身体感知多模态数据集（听觉反馈，无 XR 设备）",
        }}
json.dump(cand, open("data/cands_1112.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("rows", len(rows), "main", len(MAIN), "bf", len(BF), "reject", len(REJECT))
print(rows[0]["title"][:60])
