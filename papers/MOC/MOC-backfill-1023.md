# MOC · backfill-1023（补录批次）

> **批次性质**：补录批次，**非 2026-10-23 当日新提交**。
> ① **10-21 公告批次 listing 漏网 5 篇**（公告日 10-21、提交日 10-15~10-20；10-22 运行已处理该公告日主流水，本批补录其摘要级过滤漏网的 XR 相关稿）；
> ② **旧稿 replace/cross 再公告首次入馆 4 篇**（原始投稿周期 2604 / 2607 / 2608，10-23 RSS 拉取混入）。

## 本批概览

- 补录入馆 **9 篇**（S×0 / A×1 / B×7 / C×1），registry 588 → **597**；最高 **3.65**（Unfolding 3DGS）。
- 全文证据：**8 篇 L0/FULL**（29,750–139,019 字符）+ **1 篇 L1/PARTIAL**（2610.28131 OV-Foam，ar5iv 仅返 abs 页壳、正文缺失，按摘要级评估并显式声明）。
- 覆盖度：门① 最大 Jaccard **0.075**（2610.28131 vs 库内 2610.08756，<0.62 通过）；全批覆盖 **7 赛道**；门③ 对 backfill 不适用。无重筛、无 OUTDATED。
- 覆盖补强：3DGS LOD 第三条路线（Unfolding 3DGS）、XR 年龄保障新模态（手背图像、无面部生物特征）、光学-感知联合可微设计（编码孔径+3DGS）、单图仿真就绪场景（SceneRig）、无电子 UMI 采集、热动力学 4DGS（GTSM，边界纳入）、幂图特征提升（OV-Foam）、360° VIO 基准（Hilti）。
- 口径说明：GTSM 应用域为工业热场监测（10-22 运行曾据此剔除出主批），本批以其 3DGS 方法贡献边界纳入、B 级入馆。

## 排名（按加权降序）

| 排名 | 论文 | 赛道 | 分值 | 等级 | 证据 | 来源 | 笔记 |
|---:|---|---|---:|---|---|---|---|
| 1 | Unfolding 3DGS：迭代高斯概要实现紧凑渐进渲染 | 神经渲染 | 3.65 | A | FULL | replace 再公告 | [→](../notes/2604.11685__unfoldinggs-iterative-synopsis.md) |
| 2 | 手背图像用于 XR 沉浸式年龄保障与儿童安全 | 感知与认知 | 3.40 | B | FULL | replace 再公告 | [→](../notes/2608.21009__dorsal-hand-age-assurance-xr.md) |
| 3 | 可微任务驱动编码孔径相机设计（3DGS 场景表示） | 渲染与显示 | 3.35 | B | FULL | 10-21 漏网 | [→](../notes/2610.28004__diff-task-driven-coded-aperture.md) |
| 4 | SceneRig：单图生成仿真就绪 3D 场景的智能体系统 | 世界模型与仿真 | 3.35 | B | FULL | 10-21 漏网 | [→](../notes/2610.28585__scenerig-agentic-sim-ready.md) |
| 5 | WARPED：手腕对齐渲染（第一视角示范→机器人策略） | 内容生成 | 3.30 | B | FULL | replace 再公告 | [→](../notes/2604.10809__warped-wrist-aligned-rendering.md) |
| 6 | 单头戴相机标注的无电子 UMI 手套数据采集 | 系统与平台 | 3.23 | B | FULL | 10-21 漏网 | [→](../notes/2610.27622__head-camera-umi-glove.md) |
| 7 | GTSM：热状态空间动力学高斯泼溅（4D 热场重建与预测） | 神经渲染 | 3.17 | B | FULL | 10-21 漏网 | [→](../notes/2610.26918__gtsm-thermal-state-space.md) |
| 8 | OV-Foam：幂图划分表示下的开放词汇特征提升 | 神经渲染 | 3.12 | B | FULL | 10-21 漏网 | [→](../notes/2610.28131__ov-foam-powerfoam-lifting.md) |
| 9 | Hilti-Trimble-Oxford：360° 视觉惯性基准（户型图先验） | 评估与数据集 | 2.95 | C | FULL | replace 再公告 | [→](../notes/2607.06464__hilti-trimble-oxford-360-vi-bench.md) |

## 数据与过程

- [7 维对比表](../daily/backfill-1023/7dim-table.md) · [评分明细](../daily/backfill-1023/scored.md) · [执行日志](../daily/backfill-1023/run_log.md)
- [Backfill 报告](../../reports/XR-Backfill-Report-1023.md)
