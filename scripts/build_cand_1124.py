#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""2026-11-24 候选定稿：人工逐篇核摘要，从 75 篇 KW/标题命中里剔误命中，落 33 篇 XR 候选池。

判定依据：XR 范围 = AR/VR/MR/XR 及强相关（3D 重建、SLAM/VIO、神经渲染/3DGS、具身交互、
空间计算、近眼显示、光场、触觉/力反馈、虚拟化身、世界模型、3D 内容评估）。
误命中主因：泛词 depth/tracking/spatial/gaze/hand/mesh/sdf/affine 把 LLM 推理、医疗影像、
工业检测、林业、自驾、机器人控制带入。

输出：
  data/cand_1124.json     主批 33 篇候选（id -> rec + track + why）
  data/backfill_1124.json backfill 9 篇（replace 旧稿）
  data/nonxr_1124.json    非 XR 剔除清单（原 329 + 本次剔 42 = 371，供残差复核）
"""
import json, re

TRACK = {
    "2611.26730": ("化身与人体", "深度相机/LiDAR 点云统一人体姿态与形状模型"),
    "2611.26744": ("触觉与多模态", "触觉 VLA 的力控接地，proxy loss 不蕴含物理力"),
    "2611.26764": ("触觉与多模态", "第一视角视频接触感知的物体重建与跟踪"),
    "2611.26779": ("重建与SLAM", "多视图 3D 点跟踪免深度输入"),
    "2611.26783": ("化身与人体", "视频时序一致的全身 SMPL-X 网格恢复"),
    "2611.26883": ("触觉与多模态", "VLM 触觉/不可见物理属性基准"),
    "2611.26916": ("评估与数据集", "度量精确的第一视角机器人学习数据集"),
    "2611.26937": ("评估与数据集", "Agent 构建 3D 场景的几何精度评估"),
    "2611.26950": ("触觉与多模态", "电容指端接近-触觉统一观测的机理分析"),
    "2611.26992": ("触觉与多模态", "由物体几何推力的虚拟力传感理论"),
    "2611.27003": ("重建与SLAM", "动态驾驶场景静态优先高斯重建"),
    "2611.27030": ("神经渲染", "三角面片泼溅的逆渲染与重光照，面向 AR"),
    "2611.27047": ("具身交互", "人形机器人 ego-exo 预见式操作（第一视角感知）"),
    "2611.27101": ("化身与人体", "开放手术第一视角 3D 手部姿态数据集"),
    "2611.27136": ("评估与数据集", "千万帧级点跟踪数据集"),
    "2611.27224": ("神经渲染", "事件相机锚定的高斯表面重建"),
    "2611.27281": ("重建与SLAM", "点云去噪与上采样统一 Transformer"),
    "2611.27289": ("交互与输入", "sEMG 跨带基础模型手部姿态估计"),
    "2611.27290": ("具身交互", "从手/头运动学习隐动作（第一视角视频）"),
    "2611.27299": ("交互与输入", "sEMG 手部连续跟踪的 JEPA 表征"),
    "2611.27418": ("世界模型与仿真", "VLN 未来状态世界模型"),
    "2611.27459": ("感知与认知", "跨协作者生成式视角转换"),
    "2611.27509": ("重建与SLAM", "事件相机连续时间深度与自运动估计"),
    "2611.27512": ("评估与数据集", "无参考点云质量评估的感知门控监督"),
    "2611.27513": ("世界模型与仿真", "第一视角 4D 未来生成的世界-动作接口"),
    "2611.27525": ("神经渲染", "消费级 GPU 上全分辨率 3DGS 训练"),
    "2611.27603": ("化身与人体", "人-物交互运动合成的测试时潜适配"),
    "2611.27621": ("空间计算与UI", "3D 标注布局的多视图质量评估"),
    "2611.27633": ("重建与SLAM", "紧耦合 LiDAR-惯性-视觉里程计"),
    "2611.27719": ("神经渲染", "Retinex 3DGS 的暗光重建"),
    "2611.27788": ("感知与认知", "注视式 ViT 的细粒度识别效率"),
    "2611.27817": ("重建与SLAM", "前视声呐 SLAM 的水下导航"),
    "2611.27915": ("感知与认知", "双目 VLM 的度量 3D 空间推理"),
}

BACKFILL = {
    "2601.13574": ("触觉与多模态", "可变形本体感知膜实时 3D 形貌重建"),
    "2605.19257": ("重建与SLAM", "视觉基础模型先验的尺度感知单目 SLAM"),
    "2605.19889": ("神经渲染", "3D 高斯查找表的连续色彩变换"),
    "2606.16202": ("世界模型与仿真", "第一视角可形变物体的物理数字孪生"),
    "2607.02921": ("评估与数据集", "第一视角可穿戴设备的定量 3D 空间推理基准"),
    "2609.08848": ("重建与SLAM", "单图/随手视频一分钟内交互式 3D 场景重建"),
    "2609.31248": ("神经渲染", "3DGS 密度控制的自适应选取"),
    "2611.21057": ("触觉与多模态", "腕部信息融合的触觉表征用于富接触操作"),
    "2611.25417": ("重建与SLAM", "透明物体单视 RGB-D 深度补全"),
}

pool = json.load(open("data/xr_pool_1124.json", encoding="utf-8"))
nonxr = json.load(open("data/nonxr_1124.json", encoding="utf-8"))
old = json.load(open("data/old_replace_1124.json", encoding="utf-8"))

cand, rejected = {}, {}
for p, v in pool.items():
    if p in TRACK:
        t, why = TRACK[p]
        rec = dict(v)
        rec["track"] = t
        rec["why"] = why
        cand[p] = rec
    else:
        rejected[p] = v
        nonxr[p] = v

bf, bf_rejected = {}, {}
for p, v in old.items():
    if p in BACKFILL:
        t, why = BACKFILL[p]
        rec = dict(v)
        rec["track"] = t
        rec["why"] = why
        rec["day"] = "backfill-1124"
        bf[p] = rec
    else:
        bf_rejected[p] = v

missing_main = [p for p in TRACK if p not in cand]
missing_bf = [p for p in BACKFILL if p not in bf]
assert not missing_main, f"主批缺 {missing_main}"
assert not missing_bf, f"backfill 缺 {missing_bf}"

json.dump(cand, open("data/cand_1124.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
json.dump(bf, open("data/backfill_1124.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
json.dump(nonxr, open("data/nonxr_1124.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)

print(f"主批候选 {len(cand)} | backfill 候选 {len(bf)} | 本批剔除 {len(rejected)} | nonxr 合计 {len(nonxr)}")
print(f"backfill 另剔 {len(bf_rejected)} 篇非 XR 旧稿")
from collections import Counter
print("主批赛道:", Counter(v["track"] for v in cand.values()).most_common())
print("backfill 赛道:", Counter(v["track"] for v in bf.values()).most_common())
