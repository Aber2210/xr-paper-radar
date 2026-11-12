# 运行日志 · 2026-11-13（周五 02:30 · 工作日公告跳空状态日：11-12 公告批次未释放）

## 1. 漏网对账（Step 1）

- listing 7 分类日期头（`scripts/audit_listing_1113.py`，show=500 单页×7 分类，PREV_DAY=2026-11-11 / NEW_DAY=2026-11-12）：
  **最新公告日全部为 2026-11-11（周三）**，**无 11-12（周四）公告日组**（`newest=2026-11-11`，NEW_DAY declared=None / got=0）。缓存穿透复验（cs.CV `recent?cb=` 随机参数 → 仍 149 条 11-11 组；`pastweek` 视图同为 11-11）与跨学科复核（math.AP 51 / physics.optics 25 / cs.CL 112 / q-bio.NC 15，最新日组均为 11-11）→ **arXiv 11-12 公告批次未释放，非本分类/本机故障**。
- 11-11 公告组完整性复采（验证上批处理完整性）：逐分类 **declared=got**（CV 149 / GR 6 / HC 34 / MM 14 / RO 69 / AI 248 / IV 12，槽位合计 **532**，全局去重 **436 篇唯一论文**），与 11-12 运行采集数字逐项一致；
- 未入馆 **421 篇**（436 − 15 篇 11-12 运行已入馆主批；该批无 listing 侧漏网），摘要级 XR 过滤（`scripts/filter_missed_1113.py`，**50 id/批 + 12s 间隔**，meta fetched **421/421**、覆盖率 **1.0000**、缺失 0）命中 **13 篇**：

  - 2611.12932 URL-Sim: Unified and Regulated LiDAR Simulation（LiDAR 仿真/自动驾驶数据合成）
  - 2611.12949 Maze Runner: Autonomous Maze Navigation（机器人迷宫导航与定位）
  - 2611.12976 Partition, Refine, and Detect（开放词汇目标检测）
  - 2611.13030 APS-VLA: Action-Guided Token Pruning（VLA 推理加速）
  - 2611.13057 Continuous-Time Set-Transformers for WiFi-IMU Indoor Localization（室内定位）
  - 2611.13062 Elicitation of the parameters of a multi-criteria sorting model（多准则决策建模）
  - 2611.13307 Does Haptic Connection to a Healthy Partner Improve Motor Learning in Chronic Stroke?（触觉康复训练，非 XR 呈现/交互核心）
  - 2611.13610 From Egocentric Human Video to Robot Manipulation（具身智能综述，泛化口径）
  - 2611.13685 Ego Guidance: Robot Policy Learning with Action-Free Egocentric Videos（机器人策略学习）
  - 2611.13784 Marrying Capacity and Precision for Efficient 2D Gaussian Image Representation（2D 高斯图像表示/压缩，非场景重建）
  - 2611.14033 Few-Step Streaming Video Generation via Condition Shifting（视频生成加速）
  - 2611.14093 BODYinTRANSIT-Lab: Multimodal Dataset for Sensory-Driven Transformation（身体感知数据集，XR 关联薄弱）
  - 2611.14373 Gaussian Process-Augmented MPC Contouring Control for 6-DoF Trajectory Tracking（加工轨迹跟踪控制）

  → 与 11-12 运行显式剔除的 13 篇非 XR **逐篇 id 一致（双向差集 0）**，维持上批裁决 → **0 漏网、无 backfill**。
- 落盘：`data/audit_1113_days.json` / `data/audit_1113_alldays.json` / `data/missed_listing_1113.json`（421 篇）/ `data/newday_1113.json`（空）/ `data/missed_new_1113.json`（空）/ `data/missed_xr_abstract_1113.json`（13 篇）。

## 2. 数据源探测（Step 2）

- API 双主机探针 200（`export.arxiv.org` / `arxiv.org/api/query`）；`submittedDate` 降序前沿 = **2026-11-10**（cs.CV / cs.AI / cs.GR top-8 最新 published 均为 11-10）；`submittedDate:[202611120000 TO 202611122359]` cs.CV 命中 **0** 篇；`fetch_arxiv.py --since 2026-11-11 --max 200` → **WROTE=0**（越过下界即止，已全部入馆）。
- RSS（`rss.arxiv.org` 7 分类）：**全部 0 条目**，`lastBuildDate` = Thu, 12 Nov 2026 05:00 UTC（7 分类同批重建，非代理故障）；`fetch_rss.py` **WROTE=0**。
- 判定：**0 篇新候选**，不进入 Steps 3-7。

## 3. 甄别 / 全文 / 评分 / Top10（Steps 3-7）

- 候选池 0 篇 → 不触发全文抓取、7 维评分、覆盖度三关与 Top10 选拔。
- **未伪造 Top10 / 评分 / S 级**（诚实口径硬约束）。
- 门③ 现算参考：库内近 30 天 Top10 均分 **4.437**（窗口 2026-10-14~2026-11-13（454 条入窗）；Top10 = 2610.19674 SMoRe 4.57 / 2610.23772 视频扩散化身 4.57 / 2611.06817 Open-HumanScale 4.57 / 2611.11169 Map2SLAM 4.57 / 2610.39399 ACD-GS 4.37 / 2611.09458 左右一致立体匹配 4.37 / 2611.07902 XM4D 4.36 / 2610.34263 RacerGS 4.35 / 2611.08578 HaNDF 4.34 / 2609.31418 CognitiveReality 4.30）。

## 4. 产物与发布（Steps 8-9）

- registry **907 条**（S18/A428/B352/C109）：本日无新增入馆；**另执行 1 处数据修补** —— 2611.08578 的 `title` 字段曾被误写为裸 ID（`2611.08578`），经 arXiv API 核验真实标题为 `HaNDF: Object-Conditioned Geometric Neural Hand Distance Fields`，已按 `registry.jsonl.bak-20261113` 备份后修正 registry 与对应原子笔记 frontmatter（title_zh/评分不变）。
- 原子笔记 **564 篇**（无新增）；daily 目录 **59 个**（新增 2026-11-13）。
- 产物：本 run_log + `papers/daily/2026-11-13/7dim-table.md`（19 篇前沿参考）+ `reports/XR-Daily-Report-2026-11-13.md` + MOC 总索引维护。
- 前端：BATCH_LABELS 补 11-13 标签 → 重建 hub → DATA 计数核验 → node --check 双 script 块 → CDP 冒烟 → 双渠道发布（详见报告 §5.5）。

## 5. 异常与教训

- **工作日公告跳空第 2 次**（首次为 2026-10-29 周四）：11-12（周四）公告批次未释放，三源 + 跨学科四分类五重互证。按 10-29→10-30 先例，延迟批次预计在 **11-13 00:00 UTC（= 11-13 08:00 北京时间）** 释放，晚于本运行时刻 02:30 → **下一调度（11-14 周六 02:30）应能见到 11-12 或 11-13 公告组，须按标准流水线补处理并显式标注「公告日≠拉取日」**。
- 采集完整性复核再次以「逐分类 declared=got + 未入馆集合逐篇比对 + 摘要级 id 双向差集」三段式完成；本批 421 篇摘要级覆盖率 1.0000，未出现 11-12 记录过的 id_list 429 静默丢批（50 id/批 + 12s 间隔生效）。
- 门③ 现值 4.437 已较上批 4.4370 持平（Top10 集合未变）；下次运行仍须现算，勿沿用。
- 渠道①（workbuddy_sites_deploy）自 10-21 起连续不可用且 URL 已 403；若恢复可用须优先补部署（挂账批次 10-21~11-12 共 23 批 + 本批 11-13）。硬件类渲染缺口仍仅 CVQPG + HoOPOE 两篇破冰。
