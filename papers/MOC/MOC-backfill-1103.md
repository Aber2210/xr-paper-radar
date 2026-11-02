# MOC · backfill-1103（旧稿再公告补录）

> 本批为 **backfill**：11-02 公告批次 RSS 混入的旧稿 replace 再公告 2 篇首次入馆（原始投稿 2511=2025-11 / 2602=2026-02），**均非当日新提交**。
> 1 A / 1 B；最高 DiTGaze 3.72（无 S 线）。门① 0.116 / 门② 2 赛道（2 篇低量批次实际上限）/ 门③ 不适用。

## 本批论文（按加权降序）

| # | 论文 | 赛道 | 总分 | 等级 | 证据 | 笔记 |
|---|---|---|---|---|---|---|
| 1 | DiTGaze：几何条件扩散增强的少样本视线估计 | 感知与认知 | 3.72 | A | FULL | [→](../notes/2511.11231__ditgaze-geometry-conditioned-diffusion-augmentat.md) |
| 2 | AdaGS：置信门控扩散自适应的无位姿稀疏视图 3DGS 重建 | 重建与SLAM | 3.58 | B | FULL | [→](../notes/2602.21535__adags-confidence-gated-diffusion-adaptation-for-.md) |

## 批次要点

- **DiTGaze：几何条件扩散增强的少样本视线估计**（2511.11231，3.72 A）：DiTGaze 在 GazeGaussian 双流 3DGS 骨干上加入中间 yaw-pitch 采样、变形正交约束与几何条件 latent DiT 渲染器，生成器级视线误差 6.622°→6.353°（相对降 4.1%），在 1–9 shot 全预算排名第一；N=9 重复配对比较把受试级估计误差从 5.63° 降到 4.90°（降 0.73°，15 个身份中 14 个改善，p<0.001）。
- **AdaGS：置信门控扩散自适应的无位姿稀疏视图 3DGS 重建**（2602.21535，3.58 B）：AdaGS 用两阶段训练的 artifact-aware adapter 抑制 floater 线索、以双向置信融合门控扩散伪视图、并以表征侧高斯稳定化打断 artifact amplification loop，在 DL3DV/Waymo/KITTI 三个户外数据集上取得 PSNR 24.27/23.76/17.95 与 ATE RMSE 0.077/1.352/2.471，全面优于 11 个基线。
