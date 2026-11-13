# MOC · backfill-1114（旧稿 v2/v3 再公告首次入馆）

> **非当日新提交**：本批 8 篇均为 11-13 公告 RSS 混入的旧稿 v2/v3 再公告（原始投稿 2025-08 ~ 2026-07，2026-11-11/11-12 更新），诚实口径单独编号，不参与当日重磅日判定。
> 定稿 4 A / 4 B，最高 **2603.01178 riMESA 4.50**（协同 SLAM 共识 ADMM：真实集平均最优性差距 45.09% vs DLGBP 352.81% / DDF-SAM2 787.30%；按口径记 A）。其余：Instant NuRec 4.28（驾驶场景前馈 3DGS，~1.5 s/10–20 s 日志）· OMG4 3.80（4DGS 极致压缩 2087 MB→3.59 MB）· AVI-HT 3.73（视觉-IMU 手套追踪）· ENIGMA-360 3.49 · GUSH3R 3.42 · COSMO-Bench 3.34 · ReflFlow 3.00。

## 本批论文（按加权降序）

| # | 论文 | 赛道 | 总分 | 等级 | 证据 | 笔记 |
|---|---|---|---|---|---|---|
| 1 | riMESA：面向真实世界协同 SLAM 的共识 ADMM | 重建与SLAM | 4.50 | A | FULL | [→](../notes/2603.01178__rimesa-consensus-admm-cslam.md) |
| 2 | Instant NuRec：面向驾驶场景仿真的前馈三维高斯重建 | 世界模型与仿真 | 4.28 | A | FULL | [→](../notes/2607.14203__instant-nurec-driving-3dgs.md) |
| 3 | OMG4：面向高效动态场景表示的优化最小 4D Gaussian Splatting | 神经渲染 | 3.80 | A | FULL | [→](../notes/2510.03857__omg4-minimal-4d-gaussian.md) |
| 4 | AVI-HT：面向手套式 3D 手部追踪的自适应视觉–IMU 融合 | 交互与输入 | 3.73 | A | FULL | [→](../notes/2605.21714__avi-ht-vision-imu-gloved-hand.md) |
| 5 | ENIGMA-360：面向工业场景人类行为理解的自我–外部视角数据集 | 评估与数据集 | 3.49 | B | FULL | [→](../notes/2603.09741__enigma-360-ego-exo-industrial.md) |
| 6 | GUSH3R：单目视频前馈式动态人体–场景高斯重建 | 重建与SLAM | 3.42 | B | FULL | [→](../notes/2607.05243__gush3r-feedforward-human-scene.md) |
| 7 | COSMO-Bench：协同 SLAM 优化基准 | 评估与数据集 | 3.34 | B | FULL | [→](../notes/2508.16731__cosmo-bench-cslam-optimization.md) |
| 8 | ReflFlow：几何引导光线追踪的动态高光重建 | 渲染与显示 | 3.00 | B | FULL | [→](../notes/2512.10095__reflflow-dynamic-specular-raytracing.md) |

## 批次要点

- **riMESA：面向真实世界协同 SLAM 的共识 ADMM**（2603.01178，4.50 A）：riMESA 把流形上、可分的 edge-based C-ADMM（MESA+）增量化为随通信机会摊销的异步后端，并用 riSAM/GNC 做局部鲁棒优化、RWBP 与对偶衰减处理过时约束；在 28 个真实数据集上平均最优性差距 45.09%，比 DLGBP 的 352.81% 低 7.8×、比 DDF-SAM2 的 787.30% 低 17.5×，并在 2430 个合成数据集、7 类 C-SLAM 场景上保持实时与一致。
- **Instant NuRec：面向驾驶场景仿真的前馈三维高斯重建**（2607.14203，4.28 A）：Instant NuRec 单次前向把 10–20 s 多相机驾驶日志重建为分层 3DGS 世界，约 1.5 s 完成，而逐场景优化的 NuRec 约需 75 min（超过 3 个数量级加速）；Waymo 验证集全图 PSNR 28.26、SSIM 0.859，比最强基线 DGGT 的 26.25 高 2.01 dB，动态区 24.93 对 21.76；140 个场景闭环 rollout 中五种策略排序与 NuRec 完全一致。
- **OMG4：面向高效动态场景表示的优化最小 4D Gaussian Splatting**（2510.03857，3.80 A）：OMG4 用 SD-Score 采样、双阈值剪枝与可学习权重合并三级缩减高斯，再叠加时间条件隐式外观与分阶段 3D→4D SVQ，在 N3DV 上把 Real-Time4DGS 从 2087 MB 压到 3.59 MB（约 99%），PSNR 31.85 对 31.96、FPS 由 57 升到 129（2.26×）；同等质量下比 GIFStream 的 10.0 MB 少 65%，并可迁移到 FreeTimeGS（61.04→3.07 MB）与 STG（172→11.17 MB）。
- **AVI-HT：面向手套式 3D 手部追踪的自适应视觉–IMU 融合**（2605.21714，3.73 A）：AVI-HT 把 12 个手套 6-DoF IMU（200 Hz，14 帧窗口 14×23×3）与头显单目图像（60 Hz，512×640）经带运动学先验掩码的层级跨传感器注意力融合，在自建 DexGloveHOI（100K+ 帧、2.4M IMU 样本、4 名被试、17 类任务、3.5 h）上把 UMETrack 的 MKPE 从 12.342 mm 降到 10.359 mm（−16.1%）、指尖 F.MKPE 从 17.478 降到 13.253 mm（−24.2%），MANO 下 PA-MPJPE 13.754→10.519 mm（−23.5%），接触丢失率降 8.5%。
- **ENIGMA-360：面向工业场景人类行为理解的自我–外部视角数据集**（2603.09741，3.49 B）：ENIGMA-360 在真实工业实验室采集 180 段自我中心与 180 段外部视角同步视频（34 名被试、平均 18.59 min、合计 111.54 h、68 类 keystep、14,556 段时序标注、12,597 帧 HOI 标注、25 类物体），给出 TAS/Keystep/HOI 三套基线：同视角最优 FACT 在 EGO→EGO 上 F1@10 78.7、Acc 70.8；跨视角最好仅 C2F-TCN 的 EGO→EXO F1@10 7.2，ASFormer 的 EXO→EGO F1@10 20.9，量化出现有模型的 ego-exo 崩塌。
- **GUSH3R：单目视频前馈式动态人体–场景高斯重建**（2607.05243，3.42 B）：GUSH3R 以 Human3R 的点云、SMPL-X 与 token 为先验，加场景与人体两个高斯解码器，在单目视频上以 0.54 s/帧流式前向输出统一 3DGS 表示；MultiEgo 新视角视频 PSNR 14.2（DA3 13.9、StreamSplat 13.2）、warping error 0.0015 最低、8 帧 5.50 s；NeuMan 18.2 dB 低于优化式 HSR 的 20.6，但 EMDB 18.0 高于 16.2，BEDLAM 多人全图 17.0 优于 AnySplat 15.9。
- **COSMO-Bench：协同 SLAM 优化基准**（2508.16731，3.34 B）：COSMO-Bench 用真实 LiDAR 轨迹（MCD 10 条 + CU-Multi 2 条）经统一 C-SLAM 前端（LOAM + 2 m 关键帧 + ScanContext + KISS-Matcher）与两种通信模型（Wi-Fi 2000 KB/s、Pro-Radio 1000 KB/s）派生 12 条序列 × 2 = 24 个后端基准数据集，含 358–2,019 个内回环（外点率 2.7%–19.5%）、参考解、经验噪声模型与 95% χ² 外点标注，全部以 JRL 格式与 DOI 公开。
- **ReflFlow：几何引导光线追踪的动态高光重建**（2512.10095，3.00 B）：在 NeRF-DS 七个动态高光场景上，ReflFlow 用 2DGS 的免近似法线、残差材质增广、动态环境高斯与光栅/光追混合管线，把平均 PSNR 从 SpectroMotion 的 24.17 提到 24.91（+0.74 dB）、SSIM 0.8522→0.8880、LPIPS 0.1778→0.1471；代价是 HyperNeRF 上 22.47 dB 低于 4DGS 的 24.89，且训练 2.8 h、推理 32 FPS。
