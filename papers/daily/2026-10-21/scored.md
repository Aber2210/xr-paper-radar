# 评分明细 · 2026-10-21

- 公告窗口：10-20（周二）公告批次（09-28~10-19 提交、周二 10-20 20:00 ET 释放；拉取日 10-21 周三）。
- 评分口径：先抓全文再定稿；31 篇候选 30 篇 L0/FULL（26,060–118,689 字符）+ 1 篇 PARTIAL（2610.26549 Holi-World，ar5iv 仅返摘要页，按摘要级评估并显式声明），串行 3s/篇，无限流/降级/伪造。
- 定稿 Top10：10 篇（S×0 / A×10 / B×0），全部 A 级，无 S 级。

## Top10 排行

| 排名 | ID | 标题 | 赛道 | 总分 | 等级 | 证据 |
|---|---|---|---|---|---|---|
| 1 | 2610.24462 | O-SCD++：递归证据融合的免回放在线场景变化检测 | 感知与认知 | 3.85 | A | FULL |
| 2 | 2610.24812 | SwitchSplat：从随手捕获场景学习离散物体状态 | 神经渲染 | 3.85 | A | FULL |
| 3 | 2610.24926 | Stable Signer V3：4D 可变形基元泼溅用于手语生成 | 化身与人体 | 3.85 | A | FULL |
| 4 | 2610.26583 | DenseHap：单目图像的稠密手部触觉估计 | 触觉与多模态 | 3.85 | A | FULL |
| 5 | 2610.26625 | EgoXperience：从人类经验学习世界锚定的第一视角表征 | 感知与认知 | 3.85 | A | FULL |
| 6 | 2610.26780 | V-JEPA Hand：从第一视角视频恢复 3D 手部与相机轨迹 | 感知与认知 | 3.85 | A | FULL |
| 7 | 2610.24400 | Spatons：空-色调局部化神经算子用于高效 XR 预畸变补偿 | 渲染与显示 | 3.78 | A | FULL |
| 8 | 2610.26067 | PhysSkin++：自监督神经蒙皮的实时可泛化物理动画 | 化身与人体 | 3.77 | A | FULL |
| 9 | 2610.24031 | SynerGest：双人对话的时空协同手势生成 | 化身与人体 | 3.72 | A | FULL |
| 10 | 2610.24285 | ACTS：从人类物理交互学习视觉-触觉世界模型 | 触觉与多模态 | 3.63 | A | FULL |

## 覆盖度三关

**门① 同质去重（max Jaccard < 0.62）**：最高 0.143（2610.24285 vs 库内 2609.22332）→ **通过**（无同质）。

**门② 赛道覆盖（≥5）**：Top10 覆盖 **5 赛道**（感知与认知×3、化身与人体×3、触觉与多模态×2、神经渲染×1、渲染与显示×1）→ **通过**；全批 31 篇覆盖 12 赛道。

**门③ 价值天花板（校准关，不触发重筛）**：库内近 30 天（date≥2026-09-21）Top10 均分 = **4.416**（现算：2610.03162 4.65, 2610.03283 4.58, 2610.19674 4.57, 2610.23772 4.57, 2609.34367 4.37, 2610.18872 4.3, 2610.22778 4.3, 2610.03192 4.28, 2609.34817 4.27, 2610.17474 4.27）；当日最高 = **3.85**（2610.24462）→ **非重磅日（差值 -0.566），不宣称重磅、无 S 级**。

## 全量评分明细（按加权降序，同分按 IMP/NOV → 赛道多样性 → id 升序）

| ID | 标题 | 赛道 | IMP | NOV | TEC | EXP | PER | TRL | REP | 总分 | 等级 | 证据 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 2610.24462 | O-SCD++：递归证据融合的免回放在线场景变化检测 | 感知与认知 | 4 | 4 | 4 | 4 | 4 | 3 | 3 | 3.85 | A | FULL |
| 2610.24812 | SwitchSplat：从随手捕获场景学习离散物体状态 | 神经渲染 | 4 | 4 | 4 | 4 | 4 | 3 | 3 | 3.85 | A | FULL |
| 2610.24926 | Stable Signer V3：4D 可变形基元泼溅用于手语生成 | 化身与人体 | 4 | 4 | 4 | 4 | 4 | 3 | 3 | 3.85 | A | FULL |
| 2610.26583 | DenseHap：单目图像的稠密手部触觉估计 | 触觉与多模态 | 4 | 4 | 4 | 4 | 4 | 3 | 3 | 3.85 | A | FULL |
| 2610.26625 | EgoXperience：从人类经验学习世界锚定的第一视角表征 | 感知与认知 | 4 | 4 | 4 | 4 | 4 | 3 | 3 | 3.85 | A | FULL |
| 2610.26780 | V-JEPA Hand：从第一视角视频恢复 3D 手部与相机轨迹 | 感知与认知 | 4 | 4 | 4 | 4 | 4 | 3 | 3 | 3.85 | A | FULL |
| 2610.24400 | Spatons：空-色调局部化神经算子用于高效 XR 预畸变补偿 | 渲染与显示 | 4 | 4 | 4 | 4 | 4 | 3 | 2 | 3.78 | A | FULL |
| 2610.26067 | PhysSkin++：自监督神经蒙皮的实时可泛化物理动画 | 化身与人体 | 4 | 4 | 4 | 4 | 3 | 3 | 4 | 3.77 | A | FULL |
| 2610.24031 | SynerGest：双人对话的时空协同手势生成 | 化身与人体 | 3 | 4 | 4 | 4 | 4 | 3 | 4 | 3.72 | A | FULL |
| 2610.24285 | ACTS：从人类物理交互学习视觉-触觉世界模型 | 触觉与多模态 | 4 | 4 | 4 | 4 | 3 | 3 | 2 | 3.63 | A | FULL |
| 2610.26641 | EgoRayFormer：射线空间立体精化的第一视角 3D 人体姿态估计 | 感知与认知 | 4 | 4 | 4 | 4 | 3 | 3 | 2 | 3.63 | A | FULL |
| 2610.25887 | 重思稀疏视角 3DGS：过拟合防止的少样本学习视角 | 神经渲染 | 4 | 3 | 4 | 4 | 4 | 3 | 2 | 3.58 | B | FULL |
| 2610.23895 | GeoForward：几何引导跨视图对齐的前馈 3DGS | 神经渲染 | 3 | 4 | 4 | 4 | 4 | 3 | 2 | 3.58 | B | FULL |
| 2610.26338 | SplatXR：基于端侧 3DGS 的多层 XR 工具包 | 系统与平台 | 4 | 3 | 4 | 3 | 3 | 4 | 4 | 3.50 | B | FULL |
| 2610.24452 | HumanSkill-4D：可动画高斯化身的免训练时空语言查询 | 化身与人体 | 3 | 4 | 4 | 4 | 3 | 3 | 3 | 3.50 | B | FULL |
| 2610.24364 | GazeAgent：AI 眼镜的 VLM 引导隐式眼动校准 | 交互与输入 | 4 | 4 | 3 | 3 | 4 | 3 | 2 | 3.48 | B | FULL |
| 2610.24811 | DaFISH：方向因子化照明与球谐旋转 | 神经渲染 | 3 | 4 | 4 | 3 | 4 | 3 | 2 | 3.43 | B | FULL |
| 2610.26598 | TapID：可穿戴传感支持的 VR 快速触摸输入 | 交互与输入 | 4 | 3 | 3 | 4 | 3 | 3 | 2 | 3.28 | B | FULL |
| 2610.25011 | FineSplat：细粒度 patch、局部分组、细节泼溅 | 神经渲染 | 3 | 4 | 4 | 3 | 3 | 3 | 2 | 3.28 | B | FULL |
| 2610.25681 | RxGS：基于 BRDF 分解的可重光照高斯风格化 | 神经渲染 | 3 | 4 | 4 | 3 | 3 | 3 | 2 | 3.28 | B | FULL |
| 2610.24640 | 说还是抓？MR 界面自适应调整的对话式控制 | 空间计算与UI | 4 | 3 | 3 | 4 | 2 | 3 | 3 | 3.20 | B | FULL |
| 2610.26549 | Holi-World：从人类第一视角经验构建整体世界智能 | 世界模型与仿真 | 4 | 3 | 3 | 3 | 3 | 3 | 3 | 3.20 | B | PARTIAL/L1 |
| 2610.24257 | XRT：双操作员协作人形遥操作中的轻量接触反馈评估 | 触觉与多模态 | 4 | 3 | 3 | 4 | 2 | 3 | 2 | 3.13 | B | FULL |
| 2610.23899 | MicroSplat：走向自动化 3D 微尺度重建 | 重建与SLAM | 3 | 3 | 3 | 3 | 4 | 3 | 2 | 3.08 | B | FULL |
| 2610.26633 | CAOS-SLAM：类别无关物体感知的实时动态 vSLAM | 重建与SLAM | 3 | 3 | 3 | 4 | 3 | 3 | 2 | 3.08 | B | FULL |
| 2610.26360 | 异步多尺度 MR-VR 协作中桌面化化身注视控制的远程专家评估 | 空间计算与UI | 3 | 3 | 3 | 4 | 2 | 3 | 4 | 3.07 | B | FULL |
| 2610.25309 | SENRI：理解真实生活视频中的空间-事件关联 | 评估与数据集 | 3 | 3 | 3 | 4 | 2 | 2 | 3 | 2.92 | C | FULL |
| 2610.24237 | TMT-VR：VR 版连线测验在青年与老年群体中的可用性与接受度 | 评估与数据集 | 3 | 2 | 3 | 4 | 2 | 3 | 3 | 2.80 | C | FULL |
| 2610.26278 | 将物理驱动角色控制器策略引入 VR（Unity3D/WebXR） | 化身与人体 | 3 | 2 | 3 | 4 | 2 | 3 | 3 | 2.80 | C | FULL |
| 2610.25006 | 基于 MR 的可扩展半自主机器人遥操作（细粒度双手任务） | 系统与平台 | 3 | 3 | 3 | 3 | 2 | 3 | 2 | 2.78 | C | FULL |
| 2610.23903 | AI-Experiment：与人工智能共创的 AR 艺术项目 | 内容生成 | 2 | 2 | 2 | 2 | 1 | 2 | 2 | 1.85 | C | FULL |

## 本批剔除记录（非 XR / 弱相关，不入馆）

10-20 公告批次 RSS 命中 91 条中，去 registry(512) 后 67 篇 2610.* 真新提交，甄别剔除 36 篇非 XR/弱相关：
- 2610.24858 Arbitrary-Scale Anisotropic 3D MRI Super-Resolution with Gau — MRI 各向异性超分辨（医学）
- 2610.25223 Map2Vid: Embodied Navigation Video Generation with Human-Fri — Map2Vid 具身导航视频生成（机器人域）
- 2610.25345 MCSplat: Multi-View Photometric and Geometric Consistent Fee — MCSplat 驾驶场景前馈 GS（自动驾驶）
- 2610.25634 Clean Forcing: Drift-Resistant Autoregressive Video Diffusio — Clean Forcing 自回归视频扩散（通用视频生成）
- 2610.25637 TNVD-SC: Diagnosing Scan Context Failures in Forests with Te — TNVD-SC 森林激光雷达地点识别（机器人）
- 2610.26096 PnP-Transformer: A Neural Pose Solver for 6D Object Pose Est — PnP-Transformer 6D 物体位姿（机器人操作）
- 2610.26165 TriTD: Tri-Partite Trajectory-Distribution Distillation for  — TriTD 实时自回归视频生成蒸馏（通用视频生成）
- 2610.26855 Ropedia W0: Scaling Loco-Manipulation World Models across Em — Ropedia W0 跨本体运动-操作世界模型（机器人）
- 2610.24011 An Anatomy-Aware Staged Pipeline for Vessel-Specific Intracr — 颅内动脉瘤分割（医学）
- 2610.24016 CLARO: Clutter Aware Robot Orchestrator for Open-Vocabulary  — CLARO 开词汇抓取 VLM 编排（机器人）
- 2610.24044 GliomaINK: A Tumor and Anatomy Conditioned Flow Matching Fra — GliomaINK 脑胶质瘤 MRI 序列合成（医学）
- 2610.25068 Localization and Neural Splatting on the Edge: An FPGA Scene — LENS FPGA 边缘场景记忆（机器人系统）
- 2610.25459 BiDex-100: A Comprehensive Benchmark for Bimanual Dexterous  — BiDex-100 双手灵巧操作基准（机器人）
- 2610.01039 Bootstrapping Video Interaction Generation with Synthetic St — 合成状态过渡视频交互生成（机器人/视频生成，v2 replace）
- 2610.11049 SatFix: Absolute Visual Localization of UAVs in Satellite Ma — SatFix 无人机卫星图定位（无人机）
- 2610.23884 PrismPlan: A Shared GPU Substrate for Motion Planning Across — PrismPlan GPU 运动规划基底（机器人）
- 2610.23943 ESCAPE: Egocentric Sensing for Collision Avoidance and Polic — ESCAPE 第一视角碰撞规避（机器人）
- 2610.24149 FLASH-CBF-RRT: Fast Lipschitz-Adaptive Safe Horizon CBF Stee — FLASH-CBF-RRT 安全运动规划（机器人）
- 2610.24559 SocialCoAct: Enabling and Benchmarking Egocentric Social Co- — SocialCoAct 人形社交协作（机器人）
- 2610.24605 RoMo-GS: Efficient Online 3D Gaussian Splatting for Robot Ma — RoMo-GS 机器人在线 3DGS 建图（机器人）
- 2610.25261 GOFusion: Real-Time Gaussian-Occupancy Submap Fusion for Fis — GOFusion 高斯-占据子图融合导航（机器人）
- 2610.25397 Visual-Inertial Odometry for Ground Robots with Dynamic Came — 地面机器人动态相机-IMU 标定 VIO（机器人）
- 2610.25690 ScaleNav: Scalable Internet Video Pretraining for Language-C — ScaleNav 互联网视频预训练导航（机器人）
- 2610.25840 OV-PEAR: Observation-Verified Pose-Scale Estimation and Reco — OV-PEAR 工业物体位姿-尺度估计（工业机器人）
- 2610.25988 Self-Supervised Inertial Odometry — Self-Supervised Inertial Odometry 纯惯性里程计（通用平台）
- 2610.26169 Compositional Humanoid Manipulation through Isomorphic Teleo — HS-MoDP 人形组合操作（机器人）
- 2610.26210 AnchorFlow-VIO: Fixed-Template Monocular Visual-Inertial Odo — AnchorFlow-VIO LaMARia 基准 VIO（机器人基准）
- 2610.26508 Learning Geometry-Aware Planning Representations for Monocul — 单目飞行几何感知规划（无人机）
- 2610.26751 Beyond Omni: A Unified MLLM for Embodied Sensory Understandi — Beyond Omni 具身多模态 MLLM（通用具身）
- 2610.23940 Fast Construction of Inner Sphere Trees Using Machine Learni — ML-IST 内球树碰撞检测（通用几何）
- 2610.18093 LynxScenes: A Large-Scale Real-World Benchmark for Outdoor W — LynxScenes 轮腿机器人基准（机器人）
- 2610.24717 DiffuPlan: Editable Planning State for Diffusion Language Mo — DiffuPlan 扩散语言模型智能体（NLP）
- 2610.25447 Enhanced Masked Diffusion Unlearning — Enhanced Masked Diffusion Unlearning（NLP 安全）
- 2610.26279 Physics-anchored residual quantum neural networks for cloud- — 量子神经网络云量参数化（气象）
- 2610.17856 MMTA: Benchmarking Multimodal Temporal Analysis with Time Se — MMTA 多模态时序分析基准（通用）
- 2610.23907 EgoVine: Post-Training with Branching Experience Compiled fr — EgoVine 第一视角视频后训练规划（具身 AI）
- 2610.22400 Rethinking User Encoders: Routing Diffusion States for Scena — 推荐系统用户编码（10-19 日组，非 XR）
- 2610.22450 DriveWorld3D Evidence Constrained 3D World Modeling and Gene — DriveWorld3D 驾驶世界模型（10-19 日组，自动驾驶）

另 10-19 日组摘要级命中 7 篇（2610.22505 内窥镜/2610.22552 声纳/2610.22643 MRI/2610.22932 机器人/2610.23237 X 射线/2610.22400 推荐/2610.22450 驾驶）全部甄别为非 XR，与 10-20 运行结论一致，无新增漏网。