# MOC · backfill-1020（漏网 + 旧稿再公告补录）

> 补录两部分：① **10-16 公告日漏网 1 篇**（2610.21297 GeoPano，10-15 提交、10-16 公告，10-17 运行标题级过滤未命中——摘要才提 AR/VR，本次摘要级过滤补获）；② **RSS 旧稿 replace/cross 再公告 7 篇**（2602~2608 原始提交，10-19 公告批次随 RSS 再流通，首次入馆）。非当日新提交，绝不伪装。
> 漏斗：RSS 10-19 公告批次 352 条去重 → 关键词命中 35 → 去 registry 33 新 = 18 篇真新 + 14 篇旧稿再公告（7 篇 XR 入本批、8 篇非 XR 剔除）。

## 排行榜（按加权降序，8 篇：6 A / 2 B）

| arXiv ID | 中文题名 | 档 | 加权 | 7 维(IMP/NOV/TEC/EXP/PER/TRL/REP) | 赛道 | 来源 |
|---|---|---|---|---|---|---|
| 2602.07891 | SAGE：互联网视频弱监督扩展 3D 几何基础模型 | A | 4.00 | 4/4/4/4/5/3/3 | 重建与SLAM | 旧稿再公告 |
| 2602.11693 | OMEGA-Avatar：360° 高斯化身的单图建模（TOG） | A | 4.00 | 4/4/4/4/4/4/4 | 化身与人体 | 旧稿再公告 |
| 2605.25563 | CodecSplat：前馈 3D 高斯泼溅的超紧凑潜编码 | A | 3.85 | 4/4/4/4/4/3/3 | 神经渲染 | 旧稿再公告 |
| 2610.21297 | GeoPano：单幅全景图的几何精确 3D 重建 | A | 3.85 | 4/4/4/4/4/3/3 | 重建与SLAM | 10-16 公告漏网 |
| 2604.00852 | PanoAir：全景视觉惯性 SLAM 与跨时段真实无人机数据集 | A | 3.80 | 3/4/4/4/4/4/4 | 重建与SLAM | 旧稿再公告 |
| 2604.02107 | HyVGGT-VO：经典 VO 与前馈模型混合的稠密视觉里程计（IEEE LRA） | A | 3.65 | 4/3/4/4/3/4/4 | 重建与SLAM | 旧稿再公告 |
| 2608.15060 | EgoTac：从第一视角视频预测真实场景触觉信号 | B | 3.52 | 3/3/4/4/4/3/4 | 触觉与多模态 | 旧稿再公告 |
| 2606.28637 | PinNet：LiDAR SLAM 回环的关键点感知学习描述子 | B | 3.45 | 3/3/4/4/4/3/3 | 重建与SLAM | 旧稿再公告 |

## 赛道分布

- **重建与SLAM**（5）：2602.07891、2610.21297、2604.00852、2604.02107、2606.28637
- **化身与人体**（1）：2602.11693
- **神经渲染**（1）：2605.25563
- **触觉与多模态**（1）：2608.15060

## Top10 精读（8 篇全量，按加权降序）

1. [2602.07891 SAGE：互联网视频弱监督扩展 3D 几何基础模型](../../papers/notes/2602.07891__sage-gfm-internet-video-scaling.md)（4.00 A）
2. [2602.11693 OMEGA-Avatar：360° 高斯化身的单图建模](../../papers/notes/2602.11693__omega-avatar-360-fullhead.md)（4.00 A）
3. [2605.25563 CodecSplat：前馈 3D 高斯泼溅的超紧凑潜编码](../../papers/notes/2605.25563__codecsplat-ff3dgs-latent-coding.md)（3.85 A）
4. [2610.21297 GeoPano：单幅全景图的几何精确 3D 重建](../../papers/notes/2610.21297__geopano-single-panorama-reconstruction.md)（3.85 A）
5. [2604.00852 PanoAir：全景视觉惯性 SLAM 与跨时段真实无人机数据集](../../papers/notes/2604.00852__panoair-panoramic-vi-slam-uav.md)（3.80 A）
6. [2604.02107 HyVGGT-VO：经典 VO 与前馈模型混合的稠密视觉里程计](../../papers/notes/2604.02107__hyvggt-vo-hybrid-dense-vo.md)（3.65 A）
7. [2608.15060 EgoTac：从第一视角视频预测真实场景触觉信号](../../papers/notes/2608.15060__egotac-tactile-from-egocentric-vision.md)（3.52 B）
8. [2606.28637 PinNet：LiDAR SLAM 回环的关键点感知学习描述子](../../papers/notes/2606.28637__pinnet-lidar-loop-closure-descriptors.md)（3.45 B）

## 落后 / 路线观察

- OUTDATED / SUPERSEDED：0 篇（门① max Jaccard 0.074 通过）。
- 路线观察：① SAGE 与库内 GFM 线（VGGT-BC/SMoRe/STream3R/FoundationVIO）构成「数据扩展」支线，其对数线性标定律为数据预算规划提供依据；② OMEGA-Avatar 与主批 VDA（2610.23772）构成同赛道「显式 3DGS vs 视频扩散」范式直接对照；③ CodecSplat 与 TriFold 同属「3DGS 结构化潜空间」思路但目标不同（传输 vs 生成）；④ GeoPano 与 PanoAir 构成「全景重建-跟踪」互补对。

## 链接

- [7 维表](../daily/backfill-1020/7dim-table.md) ｜ [scored](../daily/backfill-1020/scored.md) ｜ [主批次 MOC](./MOC-2026-10-20.md)
