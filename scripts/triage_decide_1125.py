# -*- coding: utf-8 -*-
"""2026-11-25 人工甄别：对 146 篇摘要级/标题级候选逐篇核摘要，剔除跨域误命中，落实赛道。

判定原则（沿用历史口径）：
  收录 = XR/AR/VR/MR 本体研究，或直接服务 XR 管线的核心 3D 视觉/图形技术
         （重建/SLAM/神经渲染/3DGS/化身/触觉/空间计算/世界模型/评估数据集）
  剔除 = 域外应用或通用方法（医学影像、遥感测绘、林业、自动驾驶感知、机器人操作策略、
         CAD/BIM、LLM 内部机制、通用图像生成/视频生成）

输出：
  data/cand_1125.json      主批候选（含 track）
  data/rejected_1125.json  从候选池剔除的误命中（供下批互证）
  data/backfill_1125.json  replace 旧稿中确认相关的 backfill 批次
"""
import json

INCLUDE = {
    # --- cs.AI ---
    "2611.30042": "世界模型与仿真",   # SWAM: 多智能体 3D 环境状态感知世界动作模型
    "2611.30226": "评估与数据集",     # VeriWorld: 3D 环境空间推理可验证基准
    "2611.31215": "评估与数据集",     # Seeking in Space: VLM 主动空间探索基准
    # --- cs.CV ---
    "2611.28085": "渲染与显示",       # UbiEnlight: 智能眼镜低照度视频增强
    "2611.28090": "感知与认知",       # Ego-HAR: 第一视角多模态活动识别
    "2611.28111": "神经渲染",         # GC-GS: 梯度冲突作几何信号优化 3DGS
    "2611.28193": "重建与SLAM",       # FastD4RT: 动态 4D 重建免训练加速
    "2611.28520": "重建与SLAM",       # VG3R: 视频生成模型做前馈 3D 重建
    "2611.28636": "神经渲染",         # SemGuard: 3DGS 资产语义解耦水印
    "2611.28649": "空间计算与UI",     # S-Mind: 多视图几何内化空间智能
    "2611.28665": "感知与认知",       # CoT 破坏空间 VQA 的机理分析
    "2611.28670": "神经渲染",         # 跨模态高斯渲染的连续场景深度
    "2611.28673": "空间计算与UI",     # ViewAgent3D: 免训练多视图 3D 场景理解
    "2611.28682": "化身与人体",       # CHORD: 人-物交互闭环整流流分解
    "2611.28792": "世界模型与仿真",   # ArgsWorld: 3DGS 重建+生成+外推统一
    "2611.28802": "神经渲染",         # 稀疏视角 3DGS 分解梯度平坦性
    "2611.28878": "世界模型与仿真",   # Eidetic Code World Model (Paintress)
    "2611.28913": "重建与SLAM",       # Morton 序稀疏映射高效 3D 网格生成
    "2611.28979": "化身与人体",       # AlignHand: 多视图手部重建
    "2611.29026": "化身与人体",       # RAGA: 单图可刷新可动画高斯化身
    "2611.29059": "重建与SLAM",       # Recurrent Point Transformer: 流式点云编码
    "2611.29112": "空间计算与UI",     # 去中心化多视图空间推理（AR/VR 多用户）
    "2611.29163": "化身与人体",       # Inclusive Hand Pose: 拓扑感知蒸馏
    "2611.29168": "空间计算与UI",     # SpatialDuet: 度量/几何双专家路由（可穿戴）
    "2611.29218": "化身与人体",       # Ego-HMB: 第一视角人体运动桥接
    "2611.29236": "神经渲染",         # 高斯泼溅的互补几何
    "2611.29293": "重建与SLAM",       # GALILEO: 动态场景几何 RoPE
    "2611.29376": "感知与认知",       # Chameleon: VR 场景匹配纹理与风险解读
    "2611.29614": "重建与SLAM",       # GravHMR: SLAM 与人体网格共享重力系
    "2611.29693": "内容生成",         # HandiVid: 手驱第一视角交互视频数据集
    "2611.29838": "重建与SLAM",       # 事件引导连续时间 4D 重建
    "2611.29920": "重建与SLAM",       # 事件+结构先验动态高斯重建
    "2611.30012": "交互与输入",       # FlexGaze: 弱监督大规模视线估计
    "2611.30102": "神经渲染",         # LMnOP: 3DGS 剪枝
    "2611.30351": "神经渲染",         # NNS-GS: 非局部神经散射可重光照 GS
    "2611.30388": "化身与人体",       # BASE: 全双工对话化身流式具身层
    "2611.30392": "交互与输入",       # LiquidGazeNet: 事件相机近眼视线估计
    "2611.30461": "内容生成",         # LiveMirror: 消费级 GPU 实时扩散虚拟试衣（AR 镜）
    "2611.30597": "化身与人体",       # ViDiHand2: 视频扩散先验 3D 手部运动重建
    "2611.30607": "化身与人体",       # Tri-DNO: 三体扩散噪声优化 3D HOI
    "2611.30734": "评估与数据集",     # EgoDepth-Bench: 第一视角度量深度基准
    "2611.30777": "化身与人体",       # AvatarAnyone: YouTube 视频分层网格化身
    "2611.30787": "重建与SLAM",       # BridgeMVS: MVS 与单目深度双向融合
    "2611.30802": "重建与SLAM",       # Go Far Look Less: 主动多房间重建
    "2611.30898": "世界模型与仿真",   # World Models as Native Latent Action Models
    "2611.31023": "神经渲染",         # WildAnySplat: 野外前馈 3DGS
    "2611.31140": "化身与人体",       # HoloSplat: 实时 token 流式人体重建（远程呈现/XR）
    "2611.31156": "神经渲染",         # 保局部性 token 锚点可扩展新视角合成
    # --- cs.GR ---
    "2611.28793": "重建与SLAM",       # STAC++: 流式 3D 重建缓存压缩
    "2611.31018": "重建与SLAM",       # DiffSimp: 可微网格简化
    # --- cs.HC ---
    "2611.28020": "渲染与显示",       # SoundFleXR: XR 音频渲染轴向约束
    "2611.28027": "交互与输入",       # 免代码可穿戴运动传感验证工具链
    "2611.29647": "感知与认知",       # 沉浸式视频效果的持续性（presence）
    "2611.30552": "系统与平台",       # 具身对话 AI 实验装置（商用 VR + 化身）
    # --- cs.RO ---
    "2611.28939": "触觉与多模态",     # T-Tac: 柔性主动热触觉传感器
    "2611.29240": "触觉与多模态",     # Tacinf: 统一触觉基础设施
    "2611.30166": "重建与SLAM",       # 消费级 LiDAR 房间尺度扫描（深度-惯性）
    "2611.30173": "重建与SLAM",       # Confidently Lost: 稠密视觉 SLAM 静默失效
    "2611.30184": "重建与SLAM",       # OmniSLAM: 持久物体地图证据授权修订
    "2611.30572": "触觉与多模态",     # VeriTouch: 可视触觉世界模型
    # --- cs.MM ---
    "2611.30629": "神经渲染",         # Fast-GSVC: 2D 高斯视频编码
    # --- eess.AS ---
    "2611.28056": "评估与数据集",     # NAVIQUAL-XR: AR 现场音乐空间音频 QoE
}

BACKFILL = {
    "2511.20578": "触觉与多模态",   # 非束缚电触觉器件（沉浸式人机交互）
    "2605.00389": "系统与平台",     # VR 超声引导导管插管训练模拟器
    "2607.11627": "重建与SLAM",     # IBPA: 实时自由曲面网格重建
    "2608.04701": "神经渲染",       # UniWorld-View: 大基线视频扩散视角合成
    "2608.28386": "化身与人体",     # GraspHOI: 单图全身 3D 人-物重建
    "2610.41373": "神经渲染",       # Queryable Gaussian View Index
}

pool = json.load(open("data/xr_pool_1125.json", encoding="utf-8"))
old = json.load(open("data/old_replace_1125.json", encoding="utf-8"))

cand, rejected = {}, {}
for p, v in pool.items():
    if p in INCLUDE:
        v["track"] = INCLUDE[p]
        cand[p] = v
    else:
        rejected[p] = v
missing = [p for p in INCLUDE if p not in pool]
assert not missing, f"INCLUDE 中有 id 不在候选池: {missing}"

bf = {}
for p in BACKFILL:
    assert p in old, f"backfill id 不在 replace 候选: {p}"
    v = dict(old[p])
    v["track"] = BACKFILL[p]
    bf[p] = v

json.dump(cand, open("data/cand_1125.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
json.dump(rejected, open("data/rejected_1125.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
json.dump(bf, open("data/backfill_1125.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)

print(f"候选池 {len(pool)} → 收录 {len(cand)} / 剔除 {len(rejected)}")
from collections import Counter
print("赛道分布:", dict(Counter(v["track"] for v in cand.values()).most_common()))
print("backfill:", len(bf), dict(Counter(v["track"] for v in bf.values())))
