# MOC · backfill-1119（旧稿 v2/v3 再公告首次入馆）

> **非当日新提交**：本批 4 篇均为 11-18 公告 RSS 混入的旧稿 v2/v3 再公告（原始投稿 2026-05-21 ~ 2026-10-19，2026-11-16~11-17 更新），诚实口径单独编号，不参与当日重磅日判定。
> 定稿 **3 A / 1 B（无 S）**，最高 **2606.04493 SFMambaNet 3.85**（频域感知 Mamba 对应剪枝，YFCC100M mAP@5° 73.83%）；其余：2610.27275 Max-Clique vs Max-Consensus 3.84（配准准则的理论分离）· 2607.05598 SSA-3DGS 3.65（屏幕空间伪影无监督去除）· 2605.22631 HolisticMotion 3.28（掩码全身观测建模）。

## 本批论文（按加权降序）

| # | 论文 | 赛道 | 总分 | 等级 | 证据 | 笔记 |
|---|---|---|---|---|---|---|
| 1 | 平滑内点、跳变外点：面向双视图对应学习的频率感知 Mamba | 重建与SLAM | 3.85 | A | FULL | [→](../notes/2606.04493__smooth-inliers-erratic-outliers-frequency-aware-mamb.md) |
| 2 | 点云配准中最大团与最大一致集表述的关系研究 | 重建与SLAM | 3.84 | A | FULL | [→](../notes/2610.27275__on-maximum-clique-and-maximum-consensus-formulations.md) |
| 3 | SSA-3DGS：无监督去除 3D 高斯泼溅中的屏幕空间伪影 | 神经渲染 | 3.65 | A | FULL | [→](../notes/2607.05598__ssa-3dgs-unsupervised-removal-of-screen-space.md) |
| 4 | HolisticMotion：稀疏跟踪下全身运动的整体建模 | 化身与人体 | 3.28 | B | FULL | [→](../notes/2605.22631__holisticmotion-holistic-modeling-for-motion-reconstr.md) |

## 批次要点

- **平滑内点、跳变外点：面向双视图对应学习的频率感知 Mamba**（2606.04493，3.85 A）：用 cluster 诱导顺序 + 可学习复值低通门让 Mamba 扫描获得频率含义，YFCC100M mAP@5° 73.83%，超 MatchMamba 3.6 点。
- **点云配准中最大团与最大一致集表述的关系研究**（2610.27275，3.84 A）：证明最大团与最大一致集在点云配准中可任意分离，给出 d+1/d+2 最小充分 group 阶数与 0.18 ms 的 anchor certificate。
- **SSA-3DGS：无监督去除 3D 高斯泼溅中的屏幕空间伪影**（2607.05598，3.65 A）：区分屏幕空间伪影与世界空间瞬态，无监督联合分解 scene/overlay，合成 Mip-NeRF 360 平均 +2.9 dB、Dashboard 类最高 +7.5 dB。
- **HolisticMotion：稀疏跟踪下全身运动的整体建模**（2605.22631，3.28 B）：把稀疏三点头手跟踪改写为掩码全身观测建模，AMASS-P1 MPJPE 2.95 cm 优于 HMD-Poser 3.15 cm，消融增益落在噪声内。
