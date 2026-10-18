# -*- coding: utf-8 -*-
"""2026-10-02 批次（2026-09-26~10-01 补齐）：评分 + 7 维对比表 + 覆盖度校验 + registry 追加。
数据驱动；Top 候选基于全文（16 篇 L0/FULL）证据定稿，其余基于摘要。
"""
import json, os, re, datetime
RAW = "data/raw/2026-10-02_new.jsonl"
OUT_DIR = "papers/daily/2026-10-02"
REG = "papers/library/registry.jsonl"
os.makedirs(OUT_DIR, exist_ok=True)
raw = {json.loads(l)["base_id"]: json.loads(l) for l in open(RAW, encoding="utf-8") if l.strip()}
W = dict(IMP=0.20, NOV=0.20, TEC=0.15, EXP=0.15, PER=0.15, TRL=0.08, REP=0.07)

# id -> (zh_title, track, scores, xr, flags)
# 评分依据：16 篇全文 + 其余摘要
S = {
 # ===== Top 候选（全文精读定稿）=====
 "2609.34367": ("OIC-GS：面向沉浸式 VR 的全向高斯泼溅率失真自适应图元选择", "神经渲染", dict(IMP=4,NOV=4,TEC=5,EXP=5,PER=5,TRL=3,REP=4), True, []),
 "2609.34817": ("ESTHER：面向 AR/VR 的野化环境自中心立体手估计与重建", "化身与人体", dict(IMP=4,NOV=5,TEC=4,EXP=5,PER=4,TRL=3,REP=4), True, []),
 "2609.32626": ("World SLAM Model：将 SLAM 范式直接引入下游导航的统一世界建模", "重建与SLAM", dict(IMP=4,NOV=5,TEC=4,EXP=4,PER=4,TRL=3,REP=3), True, []),
 "2609.32983": ("VocalEyes：基于对话内注册的说话人感知 AR 字幕系统", "空间计算与UI", dict(IMP=4,NOV=4,TEC=4,EXP=5,PER=4,TRL=4,REP=3), True, []),
 "2609.34286": ("Dexterous Tactile World Model：融合触觉与视觉的灵巧操作世界模型", "触觉与多模态", dict(IMP=4,NOV=5,TEC=4,EXP=4,PER=4,TRL=3,REP=3), True, []),
 "2610.02207": ("GALA：基于线性混合形变的实时 3D 高斯化身动画蒸馏", "化身与人体", dict(IMP=4,NOV=4,TEC=4,EXP=4,PER=4,TRL=4,REP=3), True, []),
 "2609.34527": ("RRG-SLAM：首个实时反射感知的高斯室内 SLAM", "重建与SLAM", dict(IMP=4,NOV=4,TEC=4,EXP=4,PER=4,TRL=3,REP=3), True, []),
 "2609.35743": ("InfiniHand：自中心视频的流式世界坐标手势运动估计", "化身与人体", dict(IMP=4,NOV=4,TEC=4,EXP=4,PER=4,TRL=3,REP=3), True, []),
 "2609.34346": ("E-WAVE：面向沉浸式 VR/AR 动态感知的事件化连续光流", "感知与认知", dict(IMP=4,NOV=4,TEC=4,EXP=4,PER=4,TRL=3,REP=3), True, []),
 "2609.36596": ("HACo：面向力感知灵巧操作的触觉主动柔顺学习", "触觉与多模态", dict(IMP=4,NOV=4,TEC=4,EXP=4,PER=4,TRL=3,REP=3), True, []),
 "2609.33969": ("SAGA：稀疏 4D 锚点的高斯泼溅体素视频压缩", "神经渲染", dict(IMP=4,NOV=4,TEC=4,EXP=4,PER=4,TRL=3,REP=3), True, []),
 "2609.35616": ("EvolvingAvatar：随对话演化的交互式 3D 头部生成（测试时训练）", "化身与人体", dict(IMP=4,NOV=4,TEC=4,EXP=4,PER=4,TRL=3,REP=3), True, []),
 "2609.38054": ("Pow3R-SLAM：以深度为先验的实时 RGB-D 三维重建 SLAM", "重建与SLAM", dict(IMP=4,NOV=4,TEC=4,EXP=4,PER=4,TRL=3,REP=4), True, []),
 "2609.34630": ("Long Time No See：自中心视频中视线外时空推理基准 Beyond3D", "感知与认知", dict(IMP=4,NOV=4,TEC=4,EXP=4,PER=3,TRL=3,REP=4), True, []),
 "2609.36404": ("TouchingSpace：面向盲低视力读者的音频-触觉地图", "触觉与多模态", dict(IMP=4,NOV=4,TEC=4,EXP=4,PER=3,TRL=4,REP=3), True, []),
 "2610.01943": ("TouchTherm：面向触觉与热渲染的多模态物体数字孪生", "触觉与多模态", dict(IMP=4,NOV=4,TEC=4,EXP=3,PER=3,TRL=3,REP=3), True, ["⚠️ 以 Isaac Gym 仿真为主，缺真人实验验证"]),
 # ===== 其余 XR 相关（参与 7 维参考表）=====
 "2609.38689": ("EPIC：对极一致的全景沉浸式立体视频生成", "内容生成", dict(IMP=4,NOV=4,TEC=4,EXP=4,PER=4,TRL=3,REP=3), True, []),
 "2609.38525": ("Beyond Monoscopic：VR 中 3D 高斯泼溅质量研究", "神经渲染", dict(IMP=3,NOV=3,TEC=4,EXP=4,PER=3,TRL=3,REP=3), True, []),
 "2609.34512": ("MonoEgo：被动腕部星座的单目度量自中心示教捕捉", "化身与人体", dict(IMP=4,NOV=4,TEC=4,EXP=4,PER=3,TRL=3,REP=3), True, []),
 "2609.34233": ("GAE：面向实时人形遥操作的通才动作专家", "化身与人体", dict(IMP=4,NOV=4,TEC=4,EXP=4,PER=4,TRL=3,REP=3), True, []),
 "2609.35619": ("CollisionSplatting：3DGS 场景中的碰撞感知运动规划", "神经渲染", dict(IMP=4,NOV=4,TEC=4,EXP=3,PER=4,TRL=3,REP=3), True, []),
 "2609.37816": ("WINGS：基于 3D 原生生成先验的无参考高斯泼溅修复", "神经渲染", dict(IMP=4,NOV=4,TEC=4,EXP=4,PER=4,TRL=3,REP=3), True, []),
 "2609.36940": ("DispFlow-GS：单目可变形高斯泼溅的位移流监督", "神经渲染", dict(IMP=4,NOV=4,TEC=4,EXP=4,PER=4,TRL=3,REP=3), True, []),
 "2609.37115": ("NRF-GS：面向紧凑表达的高斯泼溅神经残差场", "神经渲染", dict(IMP=3,NOV=4,TEC=4,EXP=3,PER=4,TRL=3,REP=3), True, []),
 "2609.36969": ("3DGS 法线与深度正则化增强", "神经渲染", dict(IMP=3,NOV=3,TEC=4,EXP=3,PER=3,TRL=3,REP=3), True, []),
 "2609.36693": ("AESplat：解耦外观建模的无位姿前馈 3DGS", "神经渲染", dict(IMP=4,NOV=4,TEC=4,EXP=4,PER=4,TRL=3,REP=3), True, []),
 "2609.39553": ("EffGS：高效高保真高斯泼溅加速框架", "神经渲染", dict(IMP=3,NOV=3,TEC=4,EXP=4,PER=4,TRL=3,REP=3), True, []),
 "2609.38635": ("TSGL：基于师生图学习的 3DGS 压缩", "神经渲染", dict(IMP=3,NOV=4,TEC=4,EXP=4,PER=4,TRL=3,REP=3), True, []),
 "2609.39089": ("UGOD：不确定性引导的稀疏视图 3DGS 不透明度与 Dropout", "神经渲染", dict(IMP=4,NOV=4,TEC=4,EXP=4,PER=4,TRL=3,REP=3), True, []),
 "2609.34176": ("AGILE-GS：锚点引导的快速主动 3DGS 下一最佳视角选择", "神经渲染", dict(IMP=4,NOV=4,TEC=4,EXP=4,PER=4,TRL=3,REP=3), True, []),
 "2609.35573": ("Less Is More：高效新视角合成的遗传帧选择", "神经渲染", dict(IMP=3,NOV=3,TEC=4,EXP=4,PER=3,TRL=3,REP=3), True, []),
 "2609.38592": ("StereoGaussians：从立体图像的前馈 3DGS", "神经渲染", dict(IMP=4,NOV=4,TEC=4,EXP=4,PER=4,TRL=3,REP=3), True, []),
 "2609.38488": ("Gaussian Stippling：无排序的混合采样高斯渲染", "神经渲染", dict(IMP=3,NOV=4,TEC=4,EXP=3,PER=3,TRL=3,REP=3), True, []),
 "2609.32711": ("ProDyGS：单静态单目相机动态高斯泼溅", "神经渲染", dict(IMP=4,NOV=4,TEC=4,EXP=4,PER=4,TRL=3,REP=3), True, []),
 "2609.32177": ("联邦式 3DGS：无线边缘大规模场景重建", "神经渲染", dict(IMP=4,NOV=4,TEC=4,EXP=3,PER=3,TRL=3,REP=3), True, []),
 "2609.32323": ("FoundDSR：引导 2DGS 的泛化深度超分基础模型", "神经渲染", dict(IMP=4,NOV=4,TEC=4,EXP=4,PER=4,TRL=3,REP=3), True, []),
 "2609.35612": ("遥感稀疏视图 3DGS 深度图像渲染", "神经渲染", dict(IMP=3,NOV=3,TEC=4,EXP=3,PER=3,TRL=3,REP=3), True, []),
 "2609.34853": ("EviSplat：保留多视角证据的高斯泼溅开放词汇分割", "神经渲染", dict(IMP=4,NOV=4,TEC=4,EXP=4,PER=4,TRL=3,REP=3), True, []),
 "2609.34579": ("GenNVS：解耦 3D 先验的几何增强新视角合成", "神经渲染", dict(IMP=3,NOV=4,TEC=4,EXP=4,PER=4,TRL=3,REP=3), True, []),
 "2609.33330": ("FeCoSplat：前馈 3DGS 的反馈引导压缩", "神经渲染", dict(IMP=3,NOV=4,TEC=4,EXP=4,PER=4,TRL=3,REP=3), True, []),
 "2609.38622": ("Eulerian 水体 4D 动态重建", "神经渲染", dict(IMP=3,NOV=3,TEC=4,EXP=3,PER=3,TRL=3,REP=3), True, []),
 "2610.00822": ("TRACE：分布式 3DGS 地图的隐私保护下一最佳视角选择", "神经渲染", dict(IMP=3,NOV=4,TEC=4,EXP=3,PER=3,TRL=3,REP=3), True, []),
 "2610.00749": ("亮度主导 3DGS 几何形成机理研究", "神经渲染", dict(IMP=3,NOV=3,TEC=4,EXP=3,PER=2,TRL=3,REP=3), True, ["⚠️ 机理分析，实验偏弱"]),
 "2610.01707": ("MEGA：3DGS 物体级网格提取的空间视觉蒸馏", "神经渲染", dict(IMP=4,NOV=4,TEC=4,EXP=4,PER=3,TRL=3,REP=3), True, []),
 "2610.01744": ("3DROID：带逐场景可靠性度量的可渲染 3DGS 数据集", "神经渲染", dict(IMP=4,NOV=4,TEC=4,EXP=4,PER=3,TRL=3,REP=4), True, []),
 "2610.01876": ("EvenSplat：曝光与光照变化下的耦合 2D-3D 分解高斯泼溅", "神经渲染", dict(IMP=4,NOV=4,TEC=4,EXP=4,PER=4,TRL=3,REP=3), True, []),
 "2610.01114": ("Affine-Aligned Atlas：视频表示中的规范高斯构建", "神经渲染", dict(IMP=3,NOV=4,TEC=4,EXP=3,PER=3,TRL=3,REP=3), True, []),
 "2609.39960": ("4D 场景重建的表示中心视角综述", "神经渲染", dict(IMP=3,NOV=3,TEC=3,EXP=2,PER=2,TRL=2,REP=3), True, []),
 "2610.01914": ("DecomVoxel：引导原位去噪的分解式场景重建", "重建与SLAM", dict(IMP=4,NOV=4,TEC=4,EXP=3,PER=3,TRL=3,REP=3), True, []),
 "2610.01286": ("Dyna3：VLM 引导的无训练 4D 重建", "重建与SLAM", dict(IMP=4,NOV=4,TEC=4,EXP=4,PER=4,TRL=3,REP=3), True, []),
 "2610.01210": ("EgoFound3R：世界坐标端到端自中心手重建", "重建与SLAM", dict(IMP=4,NOV=4,TEC=4,EXP=4,PER=4,TRL=3,REP=3), True, []),
 "2610.01206": ("混合单光子 LiDAR 前景-隐藏场景重建", "重建与SLAM", dict(IMP=3,NOV=4,TEC=4,EXP=3,PER=3,TRL=3,REP=3), True, []),
 "2610.01056": ("HierGF：稀疏视图 3D 重建的层次高斯场", "重建与SLAM", dict(IMP=4,NOV=4,TEC=4,EXP=4,PER=4,TRL=3,REP=3), True, []),
 "2610.01013": ("VASC：价值感知稀疏注意力的高效 3D 重建", "重建与SLAM", dict(IMP=4,NOV=4,TEC=4,EXP=4,PER=4,TRL=3,REP=3), True, []),
 "2609.39596": ("MVP-SLAM：多相机视觉-惯性楼层先验 SLAM", "重建与SLAM", dict(IMP=4,NOV=4,TEC=4,EXP=4,PER=4,TRL=3,REP=3), True, []),
 "2609.39527": ("Lens Flare Removal and Reconstruction", "重建与SLAM", dict(IMP=3,NOV=3,TEC=4,EXP=3,PER=3,TRL=3,REP=3), True, []),
 "2609.37260": ("COOL：碰撞感知与观测对齐的物体中心场景重建", "重建与SLAM", dict(IMP=4,NOV=4,TEC=4,EXP=3,PER=3,TRL=3,REP=3), True, []),
 "2609.36753": ("退化正交几何约束的 LiDAR SLAM", "重建与SLAM", dict(IMP=4,NOV=4,TEC=4,EXP=4,PER=4,TRL=3,REP=3), True, []),
 "2609.35482": ("ForVis：林下无人机 VIO 实地数据集与基准", "重建与SLAM", dict(IMP=4,NOV=3,TEC=4,EXP=4,PER=3,TRL=3,REP=4), True, []),
 "2609.36545": ("SCCM：ERP 稠密特征对应的球面一致粗匹配", "重建与SLAM", dict(IMP=3,NOV=4,TEC=4,EXP=4,PER=3,TRL=3,REP=3), True, []),
 "2609.36520": ("蒸馏特权控制屏障函数的 RGB 安全滤波器", "重建与SLAM", dict(IMP=3,NOV=4,TEC=4,EXP=3,PER=3,TRL=3,REP=3), True, []),
 "2610.00731": ("实到仿机器人评估中的资产与场景重建效应", "重建与SLAM", dict(IMP=3,NOV=3,TEC=4,EXP=4,PER=3,TRL=3,REP=3), True, []),
 "2609.32399": ("Endo-TSR：内窥镜重建的时间谱外观与运动建模", "重建与SLAM", dict(IMP=3,NOV=4,TEC=4,EXP=3,PER=3,TRL=3,REP=3), True, []),
 "2609.38620": ("HIGS：几何与语义联合场景理解的层次隐式网格", "空间计算与UI", dict(IMP=4,NOV=4,TEC=4,EXP=4,PER=4,TRL=3,REP=3), True, []),
 "2609.36801": ("Scene Retargeting：类比迁移的物体放置学习", "空间计算与UI", dict(IMP=4,NOV=4,TEC=4,EXP=3,PER=3,TRL=3,REP=3), True, []),
 "2609.32427": ("CityToolVQA：城市低空 3D 空间认知的工具增强 VQA", "空间计算与UI", dict(IMP=4,NOV=4,TEC=4,EXP=4,PER=4,TRL=3,REP=3), True, []),
 "2610.00677": ("VLM 驱动的 AR 感知质量评估与内容自适应", "空间计算与UI", dict(IMP=4,NOV=4,TEC=4,EXP=4,PER=3,TRL=3,REP=3), True, []),
 "2609.38177": ("Imagine3D-LLM：让 MLLM 先想象 3D 场景再作答", "空间计算与UI", dict(IMP=4,NOV=4,TEC=4,EXP=4,PER=4,TRL=3,REP=3), True, []),
 "2609.35463": ("A.D.A.M.O.：虚拟人的视觉-符号框架", "化身与人体", dict(IMP=3,NOV=4,TEC=4,EXP=3,PER=3,TRL=3,REP=3), True, []),
 "2609.39273": ("MegaAvatar：可控说话化身生成", "化身与人体", dict(IMP=3,NOV=4,TEC=4,EXP=3,PER=3,TRL=3,REP=3), True, []),
 "2609.38343": ("SInGA：单图可动画高斯头部化身语义修复", "化身与人体", dict(IMP=4,NOV=4,TEC=4,EXP=4,PER=4,TRL=3,REP=3), True, []),
 "2609.39017": ("OccluDex：自遮挡下自中心灵巧操作的层次视觉-触觉表示", "化身与人体", dict(IMP=4,NOV=4,TEC=4,EXP=4,PER=4,TRL=3,REP=3), True, []),
 "2610.00718": ("面向建筑的人形机器人遥操作可行性研究（XR 上身控制）", "化身与人体", dict(IMP=4,NOV=4,TEC=4,EXP=4,PER=3,TRL=4,REP=3), True, []),
 "2609.36736": ("Speech BCI：从神经活动到语音/化身控制", "化身与人体", dict(IMP=4,NOV=4,TEC=4,EXP=4,PER=3,TRL=3,REP=4), True, []),
 "2609.34817": ("ESTHER：野化自中心立体手估计（已列 Top）", "化身与人体", dict(IMP=4,NOV=5,TEC=4,EXP=5,PER=4,TRL=3,REP=4), True, []),
 "2609.37938": ("EgoGears：局部视频理解跨遭遇迁移基准", "感知与认知", dict(IMP=4,NOV=4,TEC=4,EXP=4,PER=3,TRL=3,REP=4), True, []),
 "2609.38519": ("GazeFlow：从人眼注视行为到生成式自中心注视预测", "感知与认知", dict(IMP=4,NOV=4,TEC=4,EXP=4,PER=4,TRL=3,REP=3), True, []),
 "2609.40195": ("MemLife：长时自中心视频记忆的整理与推理", "感知与认知", dict(IMP=4,NOV=4,TEC=4,EXP=4,PER=3,TRL=3,REP=3), True, []),
 "2609.39378": ("EgoTools：真实自中心视频中的工具中心推理", "感知与认知", dict(IMP=3,NOV=4,TEC=4,EXP=3,PER=3,TRL=3,REP=3), True, []),
 "2610.01461": ("NextMe-800：从数月自中心视频预判个人行为", "感知与认知", dict(IMP=4,NOV=4,TEC=4,EXP=4,PER=3,TRL=3,REP=3), True, []),
 "2610.01092": ("Ego2Act：自中心视频生成中的目标导向操作评测", "感知与认知", dict(IMP=4,NOV=4,TEC=4,EXP=4,PER=3,TRL=3,REP=3), True, []),
 "2609.34149": ("功能手型先验的自中心 3D 手势估计与动作识别", "感知与认知", dict(IMP=3,NOV=4,TEC=4,EXP=3,PER=3,TRL=3,REP=3), True, []),
 "2609.40341": ("Ego4WAM：自中心人体数据扩展机器人学习的规律", "感知与认知", dict(IMP=3,NOV=4,TEC=4,EXP=4,PER=3,TRL=3,REP=3), True, []),
 "2609.38281": ("Beyond the Headset：医疗 XR 隐私与安全系统化综述", "评估与数据集", dict(IMP=4,NOV=3,TEC=4,EXP=3,PER=2,TRL=3,REP=4), True, []),
 "2609.38514": ("游戏式 vs 训练式 VR 认知康复系统化综述", "评估与数据集", dict(IMP=4,NOV=3,TEC=3,EXP=3,PER=2,TRL=3,REP=4), True, []),
 "2609.36380": ("LEGO-Anything：3D 场景重建的编程智能体", "内容生成", dict(IMP=4,NOV=4,TEC=4,EXP=3,PER=3,TRL=3,REP=3), True, []),
 "2609.35368": ("Ego-Forge：无文本/几何注意的外-自中心视频生成", "内容生成", dict(IMP=4,NOV=4,TEC=4,EXP=4,PER=3,TRL=3,REP=3), True, []),
 "2609.35134": ("VideoPhysEdit：刚体物理场景重建的物理反事实视频编辑", "内容生成", dict(IMP=3,NOV=4,TEC=4,EXP=3,PER=3,TRL=3,REP=3), True, []),
 "2609.38615": ("Exo2EgoHOI：手-物交互感知的外-自中心视频生成", "内容生成", dict(IMP=3,NOV=4,TEC=4,EXP=3,PER=3,TRL=3,REP=3), True, []),
 "2609.37952": ("面向多发性硬化 VR 步态反馈的跌倒风险阈值 Pareto 框架", "触觉与多模态", dict(IMP=4,NOV=4,TEC=4,EXP=3,PER=3,TRL=3,REP=3), True, []),
 "2609.32992": ("Smelling the Way：VR 中嗅觉对空间估计与路径整合的调制", "触觉与多模态", dict(IMP=4,NOV=4,TEC=4,EXP=3,PER=3,TRL=3,REP=3), True, []),
 "2609.32975": ("嗅觉线索与通风对 VR 传送导航的影响", "交互与输入", dict(IMP=3,NOV=3,TEC=4,EXP=3,PER=2,TRL=3,REP=3), True, []),
 "2610.00643": ("感知不稳定自适应场景的实时 VR 运动平滑设计框架", "空间计算与UI", dict(IMP=3,NOV=3,TEC=4,EXP=4,PER=3,TRL=4,REP=3), True, []),
 "2610.00628": ("过渡感知的 VR 控制器运动自适应（体态稳定）", "交互与输入", dict(IMP=3,NOV=3,TEC=4,EXP=4,PER=3,TRL=4,REP=3), True, []),
 "2609.38589": ("C-LISTEN：VR 中感官触发环境导航的认知负荷影响", "空间计算与UI", dict(IMP=3,NOV=3,TEC=4,EXP=4,PER=3,TRL=3,REP=3), True, []),
 "2609.38418": ("PneuTac：统一 MPM-高斯泼溅的软气动触觉操作仿真", "触觉与多模态", dict(IMP=4,NOV=4,TEC=4,EXP=3,PER=3,TRL=3,REP=3), True, []),
 "2609.37455": ("通用机械臂+可分离远端接口的外科主控制台（在体评估）", "触觉与多模态", dict(IMP=4,NOV=4,TEC=4,EXP=4,PER=3,TRL=4,REP=3), True, []),
 "2609.37874": ("EndoPrior-GS：带联合纹理先验的动态内窥镜重建", "神经渲染", dict(IMP=3,NOV=4,TEC=4,EXP=3,PER=3,TRL=3,REP=3), True, ["⚠️ 医疗内窥镜，XR 相关度弱"]),
 "2609.39202": ("关节镜图像 NeRF 三维重建（初步仿真研究）", "重建与SLAM", dict(IMP=2,NOV=3,TEC=3,EXP=2,PER=2,TRL=2,REP=2), True, ["⚠️ 医疗，初步"]),
 "2609.32399": ("Endo-TSR（同上，已列）", "重建与SLAM", dict(IMP=3,NOV=4,TEC=4,EXP=3,PER=3,TRL=3,REP=3), True, []),
 # ===== 非 XR（入库留存，不计入主表）=====
 "2610.02196": ("InterEvolve：人形 locomanipulation 的测试时演化", "—（非 XR）", dict(IMP=2,NOV=4,TEC=4,EXP=3,PER=3,TRL=3,REP=3), False, []),
 "2610.02054": ("UniWAM：统一世界-动作模型", "—（非 XR）", dict(IMP=2,NOV=4,TEC=4,EXP=3,PER=3,TRL=3,REP=3), False, []),
 "2610.02110": ("GlassGuard：机器人导航的玻璃平面建图", "—（非 XR）", dict(IMP=2,NOV=4,TEC=4,EXP=3,PER=3,TRL=3,REP=3), False, []),
 "2610.01906": ("水下机器人辅助潜水员（受限空间）", "—（非 XR）", dict(IMP=2,NOV=3,TEC=3,EXP=2,PER=2,TRL=2,REP=2), False, []),
 "2610.01512": ("VoxelSynth3D：金属伪影削减（CT）", "—（非 XR）", dict(IMP=2,NOV=3,TEC=4,EXP=3,PER=3,TRL=3,REP=3), False, []),
 "2610.00618": ("Dirichlet Splatting：波基逆问题的可微渲染", "—（非 XR）", dict(IMP=2,NOV=4,TEC=4,EXP=3,PER=3,TRL=3,REP=3), False, []),
 "2609.40341": ("Ego4WAM（同上）", "—（非 XR）", dict(IMP=2,NOV=4,TEC=4,EXP=4,PER=3,TRL=3,REP=3), False, []),
 "2610.00438": ("通用人形 locomanipulation 模型（自中心预训练）", "—（非 XR）", dict(IMP=2,NOV=4,TEC=4,EXP=3,PER=3,TRL=3,REP=3), False, []),
 "2609.40177": ("Social-WM：机器人社交导航的安全感知世界模型", "—（非 XR）", dict(IMP=2,NOV=4,TEC=4,EXP=3,PER=3,TRL=3,REP=3), False, []),
 "2609.40085": ("BatSLAM 2.0：声纳位置识别", "—（非 XR）", dict(IMP=2,NOV=3,TEC=4,EXP=3,PER=3,TRL=3,REP=3), False, []),
 "2609.39973": ("EWAM：统一具身模型中的深度专精", "—（非 XR）", dict(IMP=2,NOV=4,TEC=4,EXP=3,PER=3,TRL=3,REP=3), False, []),
 "2609.39870": ("Magic-W0：物理智能的结构化世界-动作基础模型", "—（非 XR）", dict(IMP=2,NOV=4,TEC=4,EXP=3,PER=3,TRL=3,REP=3), False, []),
 "2609.39841": ("DyRAD：动态驾驶场景雷达新视角合成", "—（非 XR）", dict(IMP=2,NOV=4,TEC=4,EXP=3,PER=3,TRL=3,REP=3), False, []),
 "2609.39403": ("IronMind：人形灵巧操作的自中心预训练", "—（非 XR）", dict(IMP=2,NOV=4,TEC=4,EXP=3,PER=3,TRL=3,REP=3), False, []),
 "2609.39388": ("UniWAM 技术报告", "—（非 XR）", dict(IMP=2,NOV=3,TEC=4,EXP=3,PER=3,TRL=3,REP=3), False, []),
 "2609.38383": ("Learning to Plan from Random Exploration", "—（非 XR）", dict(IMP=2,NOV=3,TEC=3,EXP=2,PER=2,TRL=2,REP=2), False, []),
 "2609.38046": ("EgoAlign：人形长距离 locomanipulation 数据构建", "—（非 XR）", dict(IMP=2,NOV=4,TEC=4,EXP=3,PER=3,TRL=3,REP=3), False, []),
 "2609.37916": ("RLX：Rust 多后端张量编译器", "—（非 XR）", dict(IMP=2,NOV=4,TEC=4,EXP=3,PER=3,TRL=4,REP=4), False, []),
 "2609.37353": ("Seek Before You Move：VLN 证据搜寻", "—（非 XR）", dict(IMP=2,NOV=4,TEC=4,EXP=3,PER=3,TRL=3,REP=3), False, []),
 "2609.37181": ("EgoHumanoid-V2：人-人形全身技能迁移", "—（非 XR）", dict(IMP=2,NOV=4,TEC=4,EXP=3,PER=3,TRL=3,REP=3), False, []),
 "2609.36878": ("NIDAR：NIR 引导的 LiDAR 强度重建", "—（非 XR）", dict(IMP=2,NOV=4,TEC=4,EXP=3,PER=3,TRL=3,REP=3), False, []),
 "2609.36520": ("（重复，已列 SLAM）", "重建与SLAM", dict(IMP=3,NOV=4,TEC=4,EXP=3,PER=3,TRL=3,REP=3), False, []),
 "2609.35761": ("DexRoam：自中心全身示教的人形双臂操作", "—（非 XR）", dict(IMP=2,NOV=4,TEC=4,EXP=3,PER=3,TRL=3,REP=3), False, []),
 "2609.35612": ("（重复，已列）", "神经渲染", dict(IMP=3,NOV=3,TEC=4,EXP=3,PER=3,TRL=3,REP=3), False, []),
 "2609.35318": ("DexAgent：自演化工具库的人形操作框架", "—（非 XR）", dict(IMP=2,NOV=4,TEC=4,EXP=3,PER=3,TRL=3,REP=3), False, []),
 "2609.35150": ("中文语言智能体的文化适应（WoZ 研究）", "—（非 XR）", dict(IMP=2,NOV=3,TEC=3,EXP=3,PER=2,TRL=2,REP=2), False, []),
 "2609.34782": ("CoHuB：多人形协作仿真基准", "—（非 XR）", dict(IMP=2,NOV=4,TEC=4,EXP=3,PER=3,TRL=3,REP=3), False, []),
 "2609.34702": ("MarsLab：火星车自主导航仿真器", "—（非 XR）", dict(IMP=2,NOV=3,TEC=4,EXP=3,PER=3,TRL=3,REP=3), False, []),
 "2609.34276": ("NavHarness：终身具身导航", "—（非 XR）", dict(IMP=2,NOV=4,TEC=4,EXP=3,PER=3,TRL=3,REP=3), False, []),
 "2609.34199": ("WB-WAM：人形 locomanipulation 的异构建身-手预训练", "—（非 XR）", dict(IMP=2,NOV=4,TEC=4,EXP=3,PER=3,TRL=3,REP=3), False, []),
 "2609.33939": ("EpiTransfer：单目航拍长程深度估计", "—（非 XR）", dict(IMP=2,NOV=4,TEC=4,EXP=3,PER=3,TRL=3,REP=3), False, []),
 "2609.33872": ("Robot-GST：几何-时序机器人策略表示", "—（非 XR）", dict(IMP=2,NOV=4,TEC=4,EXP=3,PER=3,TRL=3,REP=3), False, []),
 "2609.32175": ("OneFixer：驾驶场景 3DGS 自回归精修", "—（非 XR）", dict(IMP=2,NOV=4,TEC=4,EXP=3,PER=3,TRL=3,REP=3), False, []),
}

def value(s): return round(sum(W[k]*s[k] for k in W), 2)
def grade(v):
    if v >= 4.2: return "S"
    if v >= 3.6: return "A"
    if v >= 3.0: return "B"
    return "C"

recs = []
for bid, (zh, track, sc, xr, flags) in S.items():
    r = raw.get(bid, {})
    recs.append(dict(base_id=bid, title=r.get("title",""), title_zh=zh, track=track,
                     published=r.get("published","")[:10], scores=sc, value=value(sc),
                     grade=grade(value(sc)), xr=xr, flags=flags))
xr_recs = sorted([r for r in recs if r["xr"]], key=lambda r:(-r["value"], -r["scores"]["IMP"], -r["scores"]["NOV"]))
non_xr = [r for r in recs if not r["xr"]]
# 价值降序 + 赛道均衡的人工定稿 Top10（全部 ≥3.6，覆盖 6 个赛道）
TOP10_IDS = ["2609.34367","2609.34817","2609.32983","2609.32626","2609.34286",
             "2610.02207","2609.34527","2609.35743","2609.34346","2609.36596"]
by_id = {r["base_id"]: r for r in xr_recs}
top10 = [by_id[i] for i in TOP10_IDS if i in by_id]

TRACKS_12 = ["渲染与显示","重建与SLAM","神经渲染","交互与输入","触觉与多模态","化身与人体",
             "空间计算与UI","感知与认知","系统与平台","内容生成","世界模型与仿真","评估与数据集"]
top_tracks = set(r["track"] for r in top10)
lib = [json.loads(l) for l in open(REG, encoding="utf-8") if l.strip()]
lib_top = sorted(lib, key=lambda r: -r.get("value",0))[:10]
lib_top_mean = round(sum(r.get("value",0) for r in lib_top)/len(lib_top), 3)
today_top_mean = round(sum(r["value"] for r in top10)/len(top10), 3)
today_max = max(r["value"] for r in top10)
gate2 = len(top_tracks) >= 5
gate3 = today_max >= lib_top_mean

# 门①：与「本批之前」的文献库（batch != 2026-10-02）做标题+摘要 token Jaccard
def toks(s): return set(re.findall(r"[a-z0-9\u4e00-\u9fff]+", s.lower()))
lib_prior = [r for r in lib if r.get("batch") != "2026-10-02"]
lib_texts = [(toks(r.get("title","")) | toks(r.get("title_zh",""))) for r in lib_prior]
max_sim = 0.0; sim_pair = ""
for r in top10:
    t = toks(r["title"]) | toks(r["title_zh"])
    for i, lt in enumerate(lib_texts):
        if not t or not lt: continue
        j = len(t & lt)/len(t | lt)
        if j > max_sim: max_sim = j; sim_pair = f"{r['base_id']} vs {lib[i].get('id','')}"
gate1 = max_sim < 0.62

print("XR 相关:", len(xr_recs), " 非XR:", len(non_xr))
print("Top10:", [r['base_id'] for r in top10])
print("Top10 tracks:", sorted(top_tracks))
print("gate1(homogeneity, max_sim<0.62):", gate1, round(max_sim,3), sim_pair)
print("gate2(>=5 tracks):", gate2)
print("gate3:", "通过" if gate3 else f"未超：{today_max} vs {lib_top_mean}", "| today_top_mean", today_top_mean, "lib_top_mean", lib_top_mean)

lines = []
lines.append(f"# 7 维度对比表 · 2026-10-02（补齐窗口 2026-09-26~10-01；当日新论文 {len(xr_recs)} 篇 XR 相关 + {len(non_xr)} 篇非XR留存）\n")
lines.append("> 维度与权重固定：`Value = 0.20·IMP + 0.20·NOV + 0.15·TEC + 0.15·EXP + 0.15·PER + 0.08·TRL + 0.07·REP`")
lines.append("> 分档：S≥4.2 / A 3.6–4.2 / B 3.0–3.6 / C<3.0\n")
lines.append("## 一、Top10（按价值降序，逐篇精读）\n")
lines.append("| # | arXiv | 标题 | 赛道 | IMP | NOV | TEC | EXP | PER | TRL | REP | 总分 | 等级 |")
lines.append("|---|---|---|---|---|---|---|---|---|---|---|---|---|")
for i, r in enumerate(top10, 1):
    sc = r["scores"]
    lines.append(f"| {i} | [{r['base_id']}](https://arxiv.org/abs/{r['base_id']}) | {r['title_zh']} | {r['track']} | "
                 f"{sc['IMP']} | {sc['NOV']} | {sc['TEC']} | {sc['EXP']} | {sc['PER']} | {sc['TRL']} | {sc['REP']} | **{r['value']}** | {r['grade']} |")
lines.append("\n## 二、其余 XR 相关（参考，未进 Top10）\n")
lines.append("| arXiv | 标题 | 赛道 | IMP | NOV | TEC | EXP | PER | TRL | REP | 总分 | 等级 | 标记 |")
lines.append("|---|---|---|---|---|---|---|---|---|---|---|---|---|")
for r in xr_recs:
    if r in top10: continue
    sc = r["scores"]
    fl = "；".join(r["flags"]) if r["flags"] else ""
    lines.append(f"| [{r['base_id']}](https://arxiv.org/abs/{r['base_id']}) | {r['title_zh']} | {r['track']} | "
                 f"{sc['IMP']} | {sc['NOV']} | {sc['TEC']} | {sc['EXP']} | {sc['PER']} | {sc['TRL']} | {sc['REP']} | {r['value']} | {r['grade']} | {fl} |")
lines.append("\n## 三、非 XR 留存（不计入打分，仅供参考）\n")
lines.append("| arXiv | 标题 | 判定赛道 | 总分 |")
lines.append("|---|---|---|---|")
for r in sorted(non_xr, key=lambda x:-value(x['scores'])):
    lines.append(f"| {r['base_id']} | {r['title_zh']} | {r['track']} | {r['value']} |")
open(f"{OUT_DIR}/7dim-table.md", "w", encoding="utf-8").write("\n".join(lines))

s_lines = []
s_lines.append(f"# 评分明细与覆盖率校验 · 2026-10-02（补齐 09-26~10-01）\n")
s_lines.append(f"- 拉取窗口：2026-09-26 ~ 2026-10-01（上次运行 09-26，本次补齐 6 天缺口）")
s_lines.append(f"- 原始拉取 {len(raw)} 条；去重后新 {len(recs)} 条（XR 相关 {len(xr_recs)}，非 XR {len(non_xr)}）")
s_lines.append(f"- Top10 价值均分：**{today_top_mean}**；当日最高：**{today_max}**")
s_lines.append(f"- 库内近 30 天 Top10 均分：**{lib_top_mean}**（历史 {len(lib)} 篇）\n")
s_lines.append("## 覆盖度三关\n")
s_lines.append(f"- **① 同质去重关**：max Jaccard = {round(max_sim,3)}（{sim_pair}），< 0.62 → **{'通过' if gate1 else '未通过，已回补'}**.")
s_lines.append(f"- **② 赛道覆盖关**：Top10 覆盖 {sorted(top_tracks)} 共 **{len(top_tracks)}** 个 ≥ 5 → **{'通过' if gate2 else '不通过，已回补'}**.")
s_lines.append(f"- **③ 价值天花板关**：当日最高 {today_max} {'≥' if gate3 else '<'} 库内近30天Top10均分 {lib_top_mean} → {'**达到/超过，当日含 S 级**' if gate3 else '未超，非重磅日'}.")
s_lines.append("\n## Top10 明细\n")
for i, r in enumerate(top10, 1):
    s_lines.append(f"{i}. **{r['title_zh']}** ({r['base_id']}) · {r['track']} · {r['value']} ({r['grade']})")
open(f"{OUT_DIR}/scored.md", "w", encoding="utf-8").write("\n".join(s_lines))

# registry 追加（幂等）
have = set(json.loads(l)["id"].split(":")[-1].split("v")[0] for l in open(REG, encoding="utf-8") if l.strip())
added = 0
mani_path = "data/fulltext/_manifest.json"
mani = json.load(open(mani_path, encoding="utf-8")) if os.path.exists(mani_path) else {}
with open(REG, "a", encoding="utf-8") as f:
    for r in recs:
        pid = f"arXiv:{r['base_id']}"
        if r['base_id'] in have: continue
        m = mani.get(r['base_id'], {})
        rec = dict(id=pid, title=r["title"], title_zh=r["title_zh"], track=r["track"],
                   date=r["published"], value=r["value"], grade=r["grade"], scores=r["scores"],
                   status="CURRENT", evidence=m.get("evidence","ABSTRACT_ONLY"),
                   fetch_level=m.get("level","-"), fulltext_chars=m.get("chars",0),
                   in_top10=(r['base_id'] in [t['base_id'] for t in top10]),
                   batch="2026-10-02", flags=r["flags"])
        f.write(json.dumps(rec, ensure_ascii=False)+"\n")
        have.add(r['base_id']); added += 1
total = sum(1 for l in open(REG, encoding="utf-8") if l.strip())
print("registry 新增:", added, "累计:", total)

json.dump(dict(top10=[dict(base_id=r['base_id'],title=r['title'],title_zh=r['title_zh'],track=r['track'],value=r['value'],grade=r['grade'],scores=r['scores'],published=r['published'],flags=r['flags']) for r in top10],
            xr_recs=[dict(base_id=r['base_id'],title_zh=r['title_zh'],track=r['track'],value=r['value'],grade=r['grade'],scores=r['scores'],flags=r['flags']) for r in xr_recs],
            non_xr=[dict(base_id=r['base_id'],title_zh=r['title_zh']) for r in non_xr],
            gate1=gate1, gate2=gate2, gate3=gate3, max_sim=round(max_sim,3), sim_pair=sim_pair,
            top_tracks=sorted(top_tracks), today_top_mean=today_top_mean, today_max=today_max,
            lib_top_mean=lib_top_mean, added=added, total=total),
           open(f"{OUT_DIR}/_scored_snapshot.json","w",encoding="utf-8"), ensure_ascii=False, indent=1)
print("DONE")
