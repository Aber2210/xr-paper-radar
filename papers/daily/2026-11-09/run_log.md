# 运行日志 · 2026-11-09（周一 02:30 · 周一凌晨状态日：周末积压公告未到时刻）

## 1. 漏网对账（Step 1）

- listing 7 分类日期头（`scripts/audit_listing_1109.py`，show=500 单页×7 分类）：
  **最新公告日全部为 2026-11-06（周五）**（cs.CV / cs.GR / cs.HC / cs.MM / cs.RO / cs.AI / eess.IV 七分类一致）。11-07（周六）/11-08（周日）无公告日段（skipDays 节律）；**周末积压公告时刻 = 周一 00:00 UTC = 当日 08:00 北京时间，晚于本运行时刻 02:30**，故 11-09 公告组尚未释放（同 11-02/10-26 模式）；**无漏跑公告日**。
- 11-06 公告组完整性复采（验证上批处理完整性）：逐分类 declared=got 全对齐（CV 138 / GR 11 / HC 22 / MM 2 / RO 81 / AI 198 / IV 6，槽位合计 458，全局去重 386 篇唯一论文）；未入馆 **363 篇**，与 11-08 运行复采集合**逐篇一致（差异 0）**。
- 摘要级 XR 过滤（`scripts/run_filter_1109.py` → `scripts/filter_missed_xr_abstract.py`，meta fetched 363/363）：命中 **12 篇**，与 11-07 运行显式剔除的 12 篇非 XR **逐篇一致**（与 11-08 运行命中集合差异 0）：

  - 2611.06993 Batch-Conditioned Semantic Anchors for Robust Transductive Adaptation of Vision-Language Models（JPTA，视觉语言模型直推适配）
  - 2611.07063 SD-LoRA: Training-Time Structural Distillation into LoRA for Few-Shot Vision-Language Adaptation（少样本视觉语言适配）
  - 2611.07081 Wide View Synthesis from Overlapping Perspective Cameras in Autonomous Driving（WV-GS，自动驾驶宽视角合成）
  - 2611.07551 Training-Free Predictive Spatio-Temporal Token Pruning for Few-Step Autoregressive Video（PreSTP，视频扩散 token 剪枝加速）
  - 2611.07630 Real-Time Event-Based LED Tracking and Pose Estimation with PWM-Encoded Markers（事件相机 LED 跟踪，无人机引导）
  - 2611.07651 GraspBench: Execution-Aware Cross-Robot Evaluation of 6-DoF Grasp Generation in MuJoCo（跨机器人抓取评测）
  - 2611.07712 AffectiveVLA: Safe and Intent-Aware VLA Control for Human-Humanoid Social Interaction（人形机器人社交触摸）
  - 2611.08005 Deformable Contact-Aware 3D Object Placement（DCAP，可变接触 3D 物体放置）
  - 2611.08097 STEP: Spatiotemporal Training with Explicit Prediction for Perceptive Humanoid Locomotion（人形机器人运动）
  - 2611.08100 An Integrated Open-Source Stack for Vision-Based Autonomous Navigation of Wheeled Rovers（巡视器自主导航栈）
  - 2611.08372 MOMASPLAT: Dynamic Novel-View Demonstration Augmentation for Mobile Manipulation（移动操作示范增广）
  - 2611.08407 Social Humanoid: Socially Responsive Human-Humanoid Interaction（人-人形交互）

  → **0 漏网、无 backfill**。
- API 前沿条目归属核验：`fetch_arxiv.py --since 2026-11-05 --max 200` 回 16 条（published 均 2026-11-05，属 11-06 公告组），其中 14 篇已入馆；2 篇未入馆者（2611.08372 MOMASPLAT / 2611.08100 巡视器导航栈）均为 11-07 运行已显式剔除的非 XR 稿，与摘要级过滤结论一致。
- 落盘：`data/audit_1109_days.json` / `data/audit_1109_alldays.json` / `data/missed_listing_1109.json`（363 篇）/ `data/missed_listing_1109_days.json` / `data/missed_xr_abstract_1109.json`（12 篇）/ `data/audit_1109_newday.json`（>11-06 日组：无）/ `data/raw/2026-11-09_api.jsonl`（16 条）。

## 2. 数据源探测（Step 2）

- API 双主机探针（export.arxiv.org 200；arxiv.org 备用）：`submittedDate` 降序前沿 = **2026-11-05**（16 条全部 11-05 published；= 11-06 公告组来源，已全部入馆或已裁决）。
- RSS（`rss.arxiv.org` 7 分类探针）：**全部 0 条目**（周末节律空源，非代理故障；`fetch_rss.py` WROTE=0）。
- 判定：**0 篇新候选**，不进入 Steps 3-7。

## 3. 甄别 / 全文 / 评分 / Top10（Steps 3-7）

- 候选池 0 篇 → 不触发全文抓取、7 维评分、覆盖度三关与 Top10 选拔。
- **未伪造 Top10 / 评分 / S 级**（诚实口径硬约束）。
- 门③ 现算参考：库内近 30 天 Top10 均分 **4.399**（窗口 2026-10-10~2026-11-09（400 条入窗）；Top10 = 2610.19674 SMoRe 4.57 / 2610.23772 视频扩散化身 4.57 / 2611.06817 Open-HumanScale 4.57 / 2610.39399 ACD-GS 4.37 / 2611.07902 XM4D 4.36 / 2610.34263 RacerGS 4.35 / 2610.18872 EgoExplorer 4.30 / 2610.22778 dGS-dBS 4.30 / 2609.31418 CognitiveReality 4.30 / 2610.37602 RESPLE2 4.30）。

## 4. 产物与发布（Steps 8-9）

- registry **无变更**（831 条：S17/A394/B325/C95；本次未修改故无备份需要）；原子笔记 502 篇无新增。
- 产物：本 run_log + `papers/daily/2026-11-09/7dim-table.md`（23 篇前沿参考）+ `reports/XR-Daily-Report-2026-11-09.md` + MOC 总索引维护。
- 前端：BATCH_LABELS 补 11-09 标签 → 重建 hub → DATA 计数核验 → node --check 双 script 块 → CDP 冒烟 → 双渠道发布（详见报告 §5.5）。

## 5. 异常与教训

- 周一凌晨状态日模式第 3 次验证（同 10-26 / 11-02）：周末积压公告时刻 = 周一 00:00 UTC = 08:00 北京时间，晚于 02:30 运行时刻，故周一凌晨必然只见上周五公告组。
- 下次运行（11-10 周二 02:30）：处理 **11-09（周一）公告批次**（覆盖周末 11-07/11-08 积压，08:00 已释放），按标准流水线跑；门③ 务必现算（勿沿用 4.399）。
- 渠道①（workbuddy_sites_deploy）自 10-21 起连续不可用（本会话复检），若恢复可用须优先补部署（挂账批次 10-21~11-09 共 20 批）；硬件类渲染缺口仍仅 CVQPG + HoOPOE 两篇破冰，继续补波导/可变焦/Maxwellian/光场。
