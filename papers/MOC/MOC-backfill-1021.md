# MOC · backfill-1021（backfill）

> **公告窗口**：RSS 旧稿 replace/cross 再公告 10 篇（2504~2609 原始提交，首次入馆）；**拉取日**：2026-10-21（周三）。
> **诚实口径**：本批为补录，全部标注 batch=backfill-1021、orig_window 注明原始提交月；**绝不混入「当日新论文」表**（这些论文的原始提交日期为 2025-04 ~ 2026-09，非本批公告日）。

## 本批概览

- 入馆 **10 篇**（S×0 / A×4 / B×5 / C×1），registry 543 → **553**。
- 全文 **10 篇全部 L0/FULL**（54,915–82,520 字符），先抓全文再定稿，串行 3s/篇。
- 覆盖三关：门① max Jaccard **0.133**（通过）；门② 覆盖 **4 赛道**（感知与认知×2、神经渲染×4、重建与SLAM×3、空间计算与UI；backfill 为机会性补录，不适用 Top10 选拔）；门③ 对 backfill 不适用。
- OUTDATED/SUPERSEDED：**0 篇**。
- 来源：RSS 旧稿 replace/cross 再公告 20 篇中甄别 10 篇 XR 相关首次入馆；其余 10 篇非 XR 剔除（人形控制/自动驾驶/视频可操作神经函数/多机器人空间推理/人形世界模型/机器人意图跟随/零样本智能体/NLP/高光谱超分）。

## 排行（按加权降序）

| 论文 | 赛道 | 原始提交 | 分值 | 等级 | 笔记 |
|---|---|---|---:|---|---|
| OmniEgoCap：设备无关的序列级第一视角动作重建 | 感知与认知 | 2025-12 | 3.85 | A | [→](../notes/2512.19283__omniegocap-egocentric-motion-reconstruction.md) |
| ZipSplat：更少的高斯、更好的泼溅 | 神经渲染 | 2026-06 | 3.85 | A | [→](../notes/2606.05102__zipsplat-fewer-gaussians.md) |
| GraFT：基于 3D 场景图的免训练 MLLM 空间推理框架 | 感知与认知 | 2026-09 | 3.85 | A | [→](../notes/2609.03892__graft-scene-graph-spatial-reasoning.md) |
| GaussTrap：针对 3DGS 的隐蔽后门攻击（KDD 2026） | 神经渲染 | 2025-04 | 3.72 | A | [→](../notes/2504.20829__gausstrap-3dgs-backdoor-attack.md) |
| Mono-Hydra++：多任务学习的实时单目场景图构建（ISPRS JPRS） | 重建与SLAM | 2026-05 | 3.45 | B | [→](../notes/2605.17661__mono-hydra-plus-plus-scene-graph.md) |
| PRISM：几何翘曲-残差分解的前馈单图 3D 重建 | 神经渲染 | 2026-06 | 3.43 | B | [→](../notes/2606.25430__prism-feedforward-single-image-3d.md) |
| OUGS：3DGS 物体感知不确定性的主动视角选择 | 神经渲染 | 2025-11 | 3.43 | B | [→](../notes/2511.09397__ougs-active-view-selection.md) |
| MAGS-SLAM：单目多智能体高斯泼溅 SLAM | 重建与SLAM | 2026-05 | 3.08 | B | [→](../notes/2605.10760__mags-slam-multi-agent-gs-slam.md) |
| Vibe Coding XR：用 XR Blocks 与 Gemini 加速 AI+XR 原型开发 | 空间计算与UI | 2026-03 | 3.00 | B | [→](../notes/2603.24591__vibe-coding-xr-prototyping.md) |
| SGM-SLAM：场景图匹配的高效分布式 SLAM | 重建与SLAM | 2026-06 | 2.93 | C | [→](../notes/2606.16881__sgm-slam-scene-graph-matching.md) |

## 关键互证与库内关系

- **ZipSplat × 前馈 3DGS 效率线**：与库内 pixel-aligned 族（MVSplat/DepthSplat/DA3）及同批 FineSplat（4×4 细粒度 patch）构成「token 粒度/基元数量」效率竞合；与 dGS（2610.22778，解码加速）构成「表示压缩 vs 解码提速」互补两面。
- **Mono-Hydra++ × 场景图 SLAM 线**：Hydra 系单目化 + 多任务学习，与 SGM-SLAM（场景图匹配分布式）构成「建图-通信」互补；与库内 OpenSplatGraph（10-08）同属 3D 高斯语义场景图线。
- **GraFT × MLLM 空间推理线**：免训练 3D 场景图提示工程，与库内 SpatialMind（10-07）/VLM 空间推理线互补，为「免训练 vs 微调」对照。
- **GaussTrap × 3DGS 安全线**：库内新增「3DGS 后门攻击」安全视角，与渲染/表征族构成风险对冲证据。
- **OmniEgoCap × 第一视角动捕线**：与库内 EgoWholeView/OmniPoser/ESTHER 构成第一视角动作重建族；设备无关序列级扩散为新增变体。

## 数据与过程

- [backfill 7 维表](../daily/backfill-1021/7dim-table.md) · [backfill 评分明细](../daily/backfill-1021/scored.md)
- [当日 MOC](./MOC-2026-10-21.md) · [运行报告](../../reports/XR-Daily-Report-2026-10-21.md)
