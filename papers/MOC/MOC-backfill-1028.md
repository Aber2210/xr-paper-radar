# MOC · backfill-1028（旧稿再公告补录）

> 本批为 **backfill**：10-27 公告批次 RSS 混入的旧稿 replace/cross 再公告 10 篇首次入馆（原始投稿月 2601~2609），**均非当日新提交**。
> 9 A / 1 B；CognitiveReality 4.30 / RoGe 4.27 / FlowHOI 4.23 达 S 线但因非重磅日按校准关记 A。门① 0.076 / 门② 8 赛道 / 门③ 不适用。

## 本批论文（按加权降序）

| # | 论文 | 赛道 | 总分 | 等级 | 证据 | 笔记 |
|---|---|---|---|---|---|---|
| 1 | CognitiveReality：机器人无关语义高斯映射与沉浸式协同 VR 遥操作 | 空间计算与UI | 4.30 | A | FULL | [→](../notes/2609.31418__cognitivereality-robot-agnostic-semantic-gaussia.md) |
| 2 | RoGe：端到端隐式重建与生成的新视角合成 | 神经渲染 | 4.27 | A | FULL | [→](../notes/2609.02847__roge-novel-view-synthesis-via-end-to-end-implici.md) |
| 3 | FlowHOI：语义接地的手物交互流匹配生成 | 内容生成 | 4.23 | A | FULL | [→](../notes/2602.13444__flowhoi-flow-based-semantics-grounded-generation.md) |
| 4 | 4DSurf：SDF 流正则的动态场景表面重建 | 重建与SLAM | 4.00 | A | FULL | [→](../notes/2603.28064__textit-4dsurf-high-fidelity-dynamic-scene-surfac.md) |
| 5 | StableHand：质量感知的世界空间双手运动估计 | 化身与人体 | 4.00 | A | FULL | [→](../notes/2605.18553__stablehand-quality-aware-flow-matching-for-world.md) |
| 6 | Haptic Sorter：触觉探索与可微操作势统一的在线形状估计与分拣 | 触觉与多模态 | 3.93 | A | FULL | [→](../notes/2605.31352__haptic-sorter-a-unified-planning-framework-for-o.md) |
| 7 | Mem3R：混合记忆的流式 3D 重建 | 重建与SLAM | 3.92 | A | FULL | [→](../notes/2604.07279__mem3r-streaming-3d-reconstruction-with-hybrid-me.md) |
| 8 | CoMo3R-SLAM：学习式 3D 重建先验的协同单目稠密 SLAM | 重建与SLAM | 3.72 | A | FULL | [→](../notes/2605.30488__como3r-slam-collaborative-monocular-dense-slam-w.md) |
| 9 | MRO-GWM：物体中心高斯世界模型的刚体动力学预测 | 世界模型与仿真 | 3.65 | A | FULL | [→](../notes/2606.01950__learning-action-conditional-and-object-centric-g.md) |
| 10 | CleanGS：帕累托视图选择的免训练 3DGS 场景清理 | 神经渲染 | 3.52 | B | FULL | [→](../notes/2601.00913__cleangs-pareto-guided-post-hoc-cleanup-of-3d-gau.md) |

## 批次要点

- **CognitiveReality：机器人无关语义高斯映射与沉浸式协同 VR 遥操作**（2609.31418，4.30 A）：CognitiveReality 合 Gaussian-TSDF 语义建图、LLM 路由与 VR 交互：工具匹配 81.24%(规则基线 48.33%)，实机导航 26/30、重观测 20/20。
- **RoGe：端到端隐式重建与生成的新视角合成**（2609.02847，4.27 A）：RoGe 以相机条件 VGGT 的射线查询隐式特征条件化视频扩散并端到端联训，DL3DV PSNR 20.92、LPIPS 0.124、TSED 0.9977、FVD 58，超重建/生成/混合基线。
- **FlowHOI：语义接地的手物交互流匹配生成**（2602.13444，4.23 A）：FlowHOI 两阶段流匹配生成语义接地 HOI：GRAB 仿真成功率 55.96%（LatentHOI 28.44%，约 1.7 倍）、推理 0.16 s 快约 40 倍，真机四任务成功率 57.5% 对 DiffH2O 10.0%。
- **4DSurf：SDF 流正则的动态场景表面重建**（2603.28064，4.00 A）：4DSurf 以 SDF 流正则+重叠分段增量训练动态 2DGS：Hi4D 总体 Chamfer 距离较次优低逾 49%（0.47–0.48 cm），CMU Panoptic 低 19%（12.7–12.8 mm），时序稳定性 STD 0.18 为最佳。
- **StableHand：质量感知的世界空间双手运动估计**（2605.18553，4.00 A）：StableHand 以四通道质量信号驱动流匹配，HOT3D/ARCTIC 全指标 SOTA，W-MPJPE 较最强基线降约 20%（57.83 mm）与 25%（124.59 mm）。
- **Haptic Sorter：触觉探索与可微操作势统一的在线形状估计与分拣**（2605.31352，3.93 A）：Haptic Sorter 融合 BO 触觉探索与可微操作势，Haptic ODE 以力残差估计位姿：分拣圆/矩形 10/10、椭圆 8/10，RMSE 较点云低 15.74mm，观测约 300Hz。
- **Mem3R：混合记忆的流式 3D 重建**（2604.07279，3.92 A）：Mem3R 以 1.56M 快权重 TTT 记忆替换 CUT3R 的 152.31M 位姿记忆并加通道门控，参数 793M→644M（−19%）：TUM Dynamics 500–1000 帧序列 ATE 较 CUT3R+TTT3R 最高低 39%。
- **CoMo3R-SLAM：学习式 3D 重建先验的协同单目稠密 SLAM**（2605.30488，3.72 A）：CoMo3R-SLAM 以 MASt3R 先验做跨智能体验证与统一优化，Tanks&Temples 四场景三个 ATE 最低(均值0.0875m)，无深度传感器，3080 Ti 上 6-8 FPS。
- **MRO-GWM：物体中心高斯世界模型的刚体动力学预测**（2606.01950，3.65 A）：MRO-GWM 以物体中心高斯加时序-空间 Transformer 预测刚体动力学：位置误差0.717cm、旋转12.484°，MPC成功率0.79/0.74(启发式0.14)，并支持跟踪与真机演示。
- **CleanGS：帕累托视图选择的免训练 3DGS 场景清理**（2601.00913，3.52 B）：CleanGS 以 Pareto 选 3 个互补视图并二取一投票过滤高斯：18 场景标准/6×扩视 PSNR 19.03/17.83 dB，超 FlashSplat（16.44/16.29）与 GaussianCut（15.28/15.10），过滤导出中位 20 s、峰值内存 1.9 GB。
