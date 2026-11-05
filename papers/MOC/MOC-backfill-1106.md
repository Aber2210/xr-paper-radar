# MOC · backfill-1106（旧稿再公告补录）

> 本批为 **backfill**：11-05 公告批次 RSS 混入的旧稿 replace/cross 再公告 6 篇首次入馆（原始投稿 2401=2024-01 / 2506=2025-06 / 2511=2025-11 / 2604=2026-04 / 2607=2026-07 / 2611=2026-10），**均非当日新提交**。
> 5 A / 1 B；最高 EgoM2P 4.10（无 S 线）。门① 0.167 / 门② 6 赛道 / 门③ 不适用。

## 本批论文（按加权降序）

| # | 论文 | 赛道 | 总分 | 等级 | 证据 | 笔记 |
|---|---|---|---|---|---|---|
| 1 | EgoM2P：第一人称多模态多任务预训练 | 感知与认知 | 4.10 | A | FULL | [→](../notes/2506.07886__egom2p-egocentric-multimodal-multitask-pretraini.md) |
| 2 | AEGIS：以对抗扰动保护 3D 面部化身隐私 | 化身与人体 | 4.08 | A | FULL | [→](../notes/2511.17747__aegis-preserving-privacy-of-3d-facial-avatars-wi.md) |
| 3 | EgoGen：第一人称合成数据生成器 | 感知与认知 | 3.92 | A | FULL | [→](../notes/2401.08739__egogen-an-egocentric-synthetic-data-generator.md) |
| 4 | EvSLAM：面向高速机动的事件相机 SLAM 基准 | 评估与数据集 | 3.69 | A | FULL | [→](../notes/2604.24033__event-based-slam-benchmark-for-high-speed-maneuv.md) |
| 5 | PIDiffSign：基于扩散的运动学动力学模型的三维手语产生 | 化身与人体 | 3.67 | A | FULL | [→](../notes/2607.14836__a-diffusion-based-kinematics-and-dynamics-model-.md) |
| 6 | AuroraWorld：面向机器人操作中外部到第一人称视频生成的结构化 4D 世界建模 | 世界模型与仿真 | 3.56 | B | FULL | [→](../notes/2611.00177__auroraworld-structured-4d-world-modeling-for-exo.md) |

## 批次要点

- **EgoM2P：第一人称多模态多任务预训练**（2506.07886，4.10 A）：EgoM2P 是首个面向 4D 第一人称数据的多模态多任务大模型：以统一 temporal tokenizer 将 RGB/depth/gaze/camera 四模态离散化，基于 T5-Base 做 multimodal masked pretraining（4B token 库上采样 400B 训练 token，约 400M 参数），在 camera tracking、gaze estimation、单目视频深度与条件视频合成上匹配或超越 specialist SOTA，且推理快一个数量级（60 帧相机轨迹 0.18 s、300+ FPS；深度 0.8 s vs 基线 37–90 s）。
- **AEGIS：以对抗扰动保护 3D 面部化身隐私**（2511.17747，4.08 A）：AEGIS 是首个面向 3D Gaussian avatar 的身份遮蔽框架：用约束 PGD 仅扰动 DC 球谐颜色系数，在 60 个 NeRSemble avatar 上把黑盒人脸验证与检索率压到近零（uniform ε=0.2 时验证率与 Rank-1 均为 0%），推荐配置 AEGIS RA（ε=0.2）验证率 1.25%、Rank-1 0.83%，同时保持 SSIM 0.9347、PSNR 32.66 dB，且无渲染开销（约 120 FPS 交互播放）。
- **EgoGen：第一人称合成数据生成器**（2401.08739，3.92 A）：EgoGen 用 egocentric sensing 深度代理驱动 PPO 训练的 collision-avoiding motion primitives（CAMPs）合成虚拟人运动并渲染带精确 GT 的第一人称多模态数据，无需预定义全局路径、免 multi-agent RL 即在动态与多人场景取得 97–100% 成功率；其合成数据使 LaMAR 建图定位 recall 从 66.9% 升至 76.7%，并在 EgoBody 上把 depth-based human mesh recovery 的 G-MPJPE/MPJPE/V2V 分别降低 22.9%/20.7%/19.5%。
- **EvSLAM：面向高速机动的事件相机 SLAM 基准**（2604.24033，3.69 A）：EvSLAM 在无人机、直线滑轨、机械臂、Mecanum 轮车 4 个平台上用 VGA 立体事件相机（640×480、10 cm baseline）加 D435 与 IMU 采集 19 条室内高速机动序列（MoCap 亚毫米 GT），分两批评测 12 个 SOTA 方法得出：IMU 连续约束显著改善高速段速度估计 AUC、事件相机在高光流场景优于帧相机但 HDR 加高速下事件质量退化、事件与帧可互补；同时指出现有数据集立体观测时空不一致（左右事件数差约 10%–86%）与 megapixel 竞赛的数据率问题，主张 VGA 是当前最适用分辨率。
- **PIDiffSign：基于扩散的运动学动力学模型的三维手语产生**（2607.14836，3.67 A）：PIDiffSign 用 forward-kinematics 输出头把 gloss-to-pose 生成从关节坐标回归改为骨方向加骨长参数化，受控协议下 back-translation WER 降低约 5 个点（PHOENIX14T 93.47→87.83–88.70，CSL-Daily 87.31→82.68），而几何惩罚无可测收益；Newton–Euler 动力学先验在 PHOENIX14T 上再降约 1 点（87.77±0.33，最佳配置 FK+ℓ1+ℒ_NE 为 86.49±0.70），在 CSL-Daily 上无效。
- **AuroraWorld：面向机器人操作中外部到第一人称视频生成的结构化 4D 世界建模**（2611.00177，3.56 B）：AuroraWorld 从稀疏 exocentric 观测推断结构化 4D 世界表征（运动轨迹+时间锚点+空间几何）并指导 ego 视频生成，DROID 上 PSNR 17.87/FVD 60.17 全面优于 6 个基线（BWM 15.77/70.07、WristWorld 13.68/141.98），RLBench 策略成功率 RVT-2 64.00%、π0.5 40.15% 居合成视角之首，真机 ARX X5 平均 70.7%（Real Ego 78.0%）。
