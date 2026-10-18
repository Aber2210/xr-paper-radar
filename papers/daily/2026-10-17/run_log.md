# 2026-10-17 运行日志

## 数据源与拉取
- 探针：export.arxiv.org API 间歇不可用（历史老问题）；rss.arxiv.org 200 → RSS 兜底（同 09-24 起惯例）。
- RSS 7 分类去重 37 条关键词命中，全部公告日 2026-10-16（周五）。
- 去 registry(399) 后 36 新：27 篇 2610.* + 9 篇旧稿 replace/cross。
- 旧稿 9 篇（不并入当日 corpus，单列 backfill 候选）：
  - 2608.13586 The Tool-to-Entity Threshold: Parasocial Dynamics of Personalised AI Agents in S
  - 2505.15737 RUSplatting: Robust 3D Gaussian Splatting for Sparse-View Underwater Scene Recon
  - 2603.20428 Benchmarking Efficient & Effective Camera Pose Estimation Strategies for Novel V
  - 2604.11142 Naka-GS: Naka-Guided Chroma Correction and Point-Prior Compaction for Low-Light 
  - 2607.25234 WHTMix: Efficient Stereo Depth Estimation via Walsh-Hadamard Token Mixing
  - 2606.26046 RoboAtlas: Contextual Active SLAM
  - 2602.16511 Unified Perceptive Fall Safety for Humanoids
  - 2512.00667 Active Learning of Fractional-Order Viscoelastic Model Parameters for Realistic 
  - 2607.06768 AirPASS: Over-the-Air Federated Learning via Pinching Antenna Systems

## 全文抓取
- 18 篇候选全部 **L0/FULL**（arxiv.org/html），串行 3s/篇，无限流/降级/伪造。
- manifest 合并写入校验通过。

## 覆盖度三关
- 门① max Jaccard 0.357（2610.22363 vs arXiv:2610.02054）< 0.62 → 通过
- 门② Top10 覆盖 7 赛道 → 通过
- 门③ 当日最高 4.00 < 库内近30天Top10均分 4.434 → 非重磅日，无 S 级，未拔高
- 未触发重筛。

## 落后登记
- OUTDATED / SUPERSEDED：0 篇（当日方法均为当期新贡献，门①无同质）。
- 路线观察：
  1. 前馈 3DGS 表示范式持续演化：Anchor3DGS（锚基、免位姿、0.26M 高斯）与库内 PocketSplat（世界空间潜分配，10-05）、Budgeted-GS（因式分解 LOD，10-05）构成「紧凑前馈表示」家族第三条路线，关注是否收敛。
  2. 触觉渲染建模：本期 21965 以 76 人次感知实验证明分数阶粘弹性模型（FO-SLS）感知 realism 显著优于整数阶（77% vs 35% 判为接近实物），与 backfill 候选 2512.00667（分数阶参数主动学习，同课题组方向）形成「建模-感知验证」互补。
  3. 第一视角灵巧操作数据范式：EgoJEPA（潜动作、免重定向）与 P3-WAM（统一世界-动作模型）同周出现，均以「免重定向/统一建模范式」挑战传统 retargeting 流水线，社区可能归一。

## 交付物
- 本目录：7dim-table.md / scored.md / run_log.md
- 报告：reports/XR-Daily-Report-2026-10-17.md
- 原子笔记 10 篇（papers/notes/2610.*）+ MOC-2026-10-17.md + MOC-总索引.md 刷新
- registry：399 → 417（+18，幂等追加，batch=2026-10-17）