# MOC · backfill-1027（旧稿再公告补录）

> 本批为 **backfill**：10-26 公告批次 RSS 混入的旧稿 replace/cross 再公告 8 篇首次入馆（原始投稿月 2412~2610），**均非当日新提交**。
> 4 A / 4 B；World from Motion 4.27 达 S 线但因非重磅日按校准关记 A。门① 0.067 / 门② 6 赛道 / 门③ 不适用。

## 本批论文（按加权降序）

| # | 论文 | 赛道 | 总分 | 等级 | 证据 | 笔记 |
|---|---|---|---|---|---|---|
| 1 | World from Motion：单目视频生成式动态高斯重建 | 神经渲染 | 4.27 | A | FULL | [→](../notes/2607.01202__world-from-motion-generative-dynamic-gaussian-re.md) |
| 2 | RGS-SLAM：重思高斯 SLAM 致密化——静止采样视角 | 重建与SLAM | 3.92 | A | FULL | [→](../notes/2601.00705__rethinking-densification-in-gaussian-slam-a-stat.md) |
| 3 | Vorch-Streamer：实时长时文本到音视频流式化身生成 | 化身与人体 | 3.85 | A | FULL | [→](../notes/2608.05663__vorch-streamer-extending-human-audio-visual-gene.md) |
| 4 | LENS：边缘 FPGA 场景记忆——机器人定位与神经泼溅加速 | 系统与平台 | 3.65 | A | FULL | [→](../notes/2610.25068__localization-and-neural-splatting-on-the-edge-an.md) |
| 5 | 从帧流到时序图：VLM 上下文学习的第一视角动作识别 | 感知与认知 | 3.50 | B | FULL | [→](../notes/2606.15417__from-frames-to-temporal-graphs-in-context-egocen.md) |
| 6 | STATIC：表面法线引导的双分支对齐与时序集成（视频单目深度一致性） | 感知与认知 | 3.15 | B | FULL | [→](../notes/2412.01090__static-surface-normal-guided-two-branch-alignmen.md) |
| 7 | 自由手牙科操作的双边触觉遥操作系统 | 触觉与多模态 | 3.15 | B | FULL | [→](../notes/2503.21288__haptic-bilateral-teleoperation-system-for-free-h.md) |
| 8 | OccamView：对象条件化的帧预算主动 3DGS 重建视角选择 | 重建与SLAM | 3.00 | B | FULL | [→](../notes/2608.16499__occamview-object-conditioned-view-selection-for-.md) |

## 批次要点

- **World from Motion：单目视频生成式动态高斯重建**（2607.01202，4.27 A）：用视频模型以「稠密像素对齐的动态 3DGS 渲染（外观/几何/沿输入与目标轨迹的运动）」为条件生成新视角，修正渲染伪影并补全缺失区域，再把生成蒸馏回单一一致动态 3DGS；DyCheck mPSNR（pose-opt covisible）20.38 超 WorldTree 19.75 / Shape-of-Motion 17.32，宣称 4D 重建新 SOTA。
- **RGS-SLAM：重思高斯 SLAM 致密化——静止采样视角**（2601.00705，3.92 A）：用免训练 correspondence-to-Gaussian 一次性三角化初始化（DINOv3 描述子 + 置信度感知内点分类）替代残差驱动致密化，把「精化」与「容量增长」解耦：收敛加速约 20%，Replica ATE 0.61cm，建图 925 FPS。
- **Vorch-Streamer：实时长时文本到音视频流式化身生成**（2608.05663，3.85 A）：后训练框架把双向音视频模型改造为因果实时流式生成：混合 Teacher Forcing + Diffusion Forcing 训练因果生成器 + 长程 Self Forcing（DMD 蒸馏）+ LLM 25Hz 言语规划 token；27.12 FPS 实时、WER 7.92%（基线外推法 94–98%）。
- **LENS：边缘 FPGA 场景记忆——机器人定位与神经泼溅加速**（2610.25068，3.65 A）：AMD KR260 上的边缘场景记忆系统：INT16 场景坐标回归（SCR）加速器保持 DSAC* 定位精度（板载 25.42ms）+ 位精确定点有序 3DGS 渲染器（alpha 透射率 log-sum-exp 重写）；Cambridge 34.11dB（vs ACEsplat 33.20）、RE10K 27.84dB（vs 26.11）；每瓦性能超 Jetson Orin NX 1.9–5.7×。
- **从帧流到时序图：VLM 上下文学习的第一视角动作识别**（2606.15417，3.50 B）：把第一视角视频转为「时序动作图」（TAG）再交 VLM 符号推理：每类 2 个图示例即把 EGTEA 平均 MCA 从 30.35% 提到 37.25%；零样本下图推理仍具竞争力；跨 11 个开源 VLM 的结论——当前 VLM 更适合做符号推理者而非直接视觉观察者。
- **STATIC：表面法线引导的双分支对齐与时序集成（视频单目深度一致性）**（2412.01090，3.15 B）：两帧输入 + 表面法线相似度模块（SNS）+ 掩码静态模块（MS）实现视频单目深度时序一致性：相对时序一致性（rTC）较此前最佳 +1.76%，RMSE 较 MAMo 改善约 0.60% 且仅用两帧（MAMo 用更多帧）。
- **自由手牙科操作的双边触觉遥操作系统**（2503.21288，3.15 B）：面向自由手牙科操作的触觉双边遥操作系统：眼手协调控制器（咬合相位+人手震颤过滤）+ 导纳模型交互控制 + 自由手力限制策略 + 触觉反馈控制器；场景 A 交互力降低约 50%。
- **OccamView：对象条件化的帧预算主动 3DGS 重建视角选择**（2608.16499，3.00 B）：用开放词汇检测维护在线对象记忆、以保守隐藏区域代理表示对象周边未解析占用，遮挡感知代理覆盖打分选视角；Geo-Floor 机制把对象重排序限制于几何竞争力候选；Replica/Matterport3D 五档帧预算下 Completion 与 Completion Ratio 一致改善（f40 时 Completion 28.52→16.x cm）。
