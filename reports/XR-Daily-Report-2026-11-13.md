# XR 每日论文雷达 · 运行报告 · 2026-11-13（周五 02:30）

> **诚实口径声明**：本运行日（2026-11-13，周五 02:30）**无新增可处理论文**——**arXiv 2026-11-12（周四）公告批次未释放**（工作日公告跳空，继 2026-10-29 之后第 2 次）。五重互证：① listing 7 分类最新公告日均为 **2026-11-11（周三）**，无 11-12 日组；② 缓存穿透复验（`recent?cb=`）与 `pastweek` 视图一致；③ 跨学科复核 math.AP / physics.optics / cs.CL / q-bio.NC 最新日组同为 11-11 → 非本分类故障；④ API `submittedDate` 前沿 **11-10**、`[20261112 TO 20261112]` cs.CV 命中 0、`--since 2026-11-11` WROTE=0；⑤ RSS 7 分类全部 0 条目（`lastBuildDate` 11-12 05:00 UTC）。上一批（11-12 运行）处理的 11-11 公告组经本日全量复采复核：**532 槽位 declared=got、436 篇唯一论文**，未入馆 421 篇摘要级 XR 命中 13 篇，与 11-12 运行已显式剔除的 13 篇**逐篇 id 一致** → **0 漏网、无 backfill**。**本报告不含任何「当日新论文」解读，不虚构 Top10/评分/S 级**；第四节为文献库最新前沿参考。

---

## 一、执行摘要

| 项 | 结论 |
|---|---|
| 运行性质 | **状态报告日**（工作日公告跳空：11-12 公告批次未释放；漏网对账 + 五重源核验 + 采集完整性复核 + 知识库存量维护 + 前端重建与双渠道发布） |
| 公告状态 | listing 7 分类最新公告日均为 **2026-11-11（周三）**；**无 11-12（周四）公告日组**；跨学科四分类最新日组同为 11-11 → arXiv 公告流水线跳空，非本机故障 |
| 漏网对账 | 11-11 公告组 show=500 单页全量复采：逐分类 declared=got（CV 149/GR 6/HC 34/MM 14/RO 69/AI 248/IV 12，槽位 532、唯一论文 436）；未入馆 421 篇摘要级 XR 命中 13 篇，与 11-12 运行已剔 13 篇逐篇 id 一致 → **0 漏网**；无需 backfill |
| 数据源 | API 双主机 200（前沿 11-10；11-12 区间 0 篇；WROTE=0）；RSS 7 分类全部 0 条目（lastBuildDate 11-12 05:00 UTC） |
| 新入馆论文 | **0 篇**（registry 维持 **907 条**：S 18 / A 428 / B 352 / C 109） |
| 新原子笔记 | 0 篇（维持 **564 篇**；daily 目录 59 个） |
| 数据修补 | 1 处：2611.08578 的 `title` 曾误写为裸 ID，经 API 核验后修正为 `HaNDF: Object-Conditioned Geometric Neural Hand Distance Fields`（备份 `registry.jsonl.bak-20261113`） |
| 库内近 30 天 Top10 均分 | **4.437**（现算，窗口 2026-10-14~2026-11-13（454 条入窗）；门③ 为校准关，本日无候选不触发） |
| 交付 | 状态报告 1 + 前沿参考 7 维表 1（19 篇）+ run_log 1 + MOC 总索引维护 + 前端重建与双渠道发布 |

**下一批预期**：11-12 公告批次预计延迟至 **11-13 00:00 UTC（08:00 北京时间）** 释放（同 10-29→10-30 先例），晚于本运行时刻 02:30；**下一调度（11-14 周六 02:30）须按标准流水线补处理并显式标注「公告日≠拉取日」**，门③ 务必现算。

---

## 二、漏网对账（Step 1）

对账目的：确认自上一批次公告日（2026-11-11）至今是否有漏跑公告日或漏收 XR 论文。

### 2.1 公告日头核验（目标窗口 ≥ 2026-11-12）

| 分类 | 最新公告日 | 11-11 组 declared | 11-11 组实采 | 11-12 组 |
|---|---|---|---:|---|
| cs.CV | Wed, 11 Nov 2026 | 149 | 149 | **无** |
| cs.GR | Wed, 11 Nov 2026 | 6 | 6 | **无** |
| cs.HC | Wed, 11 Nov 2026 | 34 | 34 | **无** |
| cs.MM | Wed, 11 Nov 2026 | 14 | 14 | **无** |
| cs.RO | Wed, 11 Nov 2026 | 69 | 69 | **无** |
| cs.AI | Wed, 11 Nov 2026 | 248 | 248 | **无** |
| eess.IV | Wed, 11 Nov 2026 | 12 | 12 | **无** |

- **无 11-12 公告日组**：`audit_listing_1113.py` 对 NEW_DAY=2026-11-12 采到 declared=None / got=0。
- **缓存与故障排除**：① 加随机 `cb` 参数复验 cs.CV → 仍为 11-11 组（149 条），排除页面缓存；② `pastweek` 视图最新日组同为 11-11；③ 跨学科复核 math.AP（51）/ physics.optics（25）/ cs.CL（112）/ q-bio.NC（15）最新日组**全部为 11-11** → 属 arXiv 全局公告跳空，与 10-29（周四批次未释放）同类。
- **延迟释放先例**：10-29 跳空后该批次于 10-30（周五）00:00 UTC 释放并被 10-31 运行捕获。据此预判 11-12 批次将于 **11-13 00:00 UTC（08:00 北京时间）** 释放，晚于本运行 02:30。

### 2.2 11-11 公告组完整性复核（验证上批处理完整性）

- 逐分类 **declared = got**（上表），槽位合计 **532**，全局去重 **436 篇唯一论文**（与 11-12 运行采集数字逐项一致）；
- 未入馆 **421 篇** = 436 − 15（11-12 运行主批已入馆；该批 listing 侧无漏网），与 11-12 运行复采集合**逐篇一致**；
- 摘要级 XR 过滤（`scripts/filter_missed_1113.py`，50 id/批 + 12s 间隔；**meta fetched 421/421，覆盖率 1.0000**）：命中 **13 篇**，与 11-12 运行显式剔除的 13 篇非 XR **逐篇 id 一致（双向差集 0）**：

| ID | 标题 | 11-12 运行裁决（本批复核维持） |
|---|---|---|
| 2611.12932 | URL-Sim: Unified and Regulated LiDAR Simulation（LiDAR 仿真/自动驾驶数据合成） | 非 XR（已显式剔除） |
| 2611.12949 | Maze Runner: Autonomous Maze Navigation（机器人迷宫导航与定位） | 非 XR（已显式剔除） |
| 2611.12976 | Partition, Refine, and Detect（开放词汇目标检测） | 非 XR（已显式剔除） |
| 2611.13030 | APS-VLA: Action-Guided Token Pruning（VLA 推理加速） | 非 XR（已显式剔除） |
| 2611.13057 | Continuous-Time Set-Transformers for WiFi-IMU Indoor Localization（室内定位） | 非 XR（已显式剔除） |
| 2611.13062 | Elicitation of the parameters of a multi-criteria sorting model（多准则决策建模） | 非 XR（已显式剔除） |
| 2611.13307 | Does Haptic Connection to a Healthy Partner Improve Motor Learning in Chronic Stroke?（触觉康复训练，非 XR 呈现/交互核心） | 非 XR（已显式剔除） |
| 2611.13610 | From Egocentric Human Video to Robot Manipulation（具身智能综述，泛化口径） | 非 XR（已显式剔除） |
| 2611.13685 | Ego Guidance: Robot Policy Learning with Action-Free Egocentric Videos（机器人策略学习） | 非 XR（已显式剔除） |
| 2611.13784 | Marrying Capacity and Precision for Efficient 2D Gaussian Image Representation（2D 高斯图像表示/压缩，非场景重建） | 非 XR（已显式剔除） |
| 2611.14033 | Few-Step Streaming Video Generation via Condition Shifting（视频生成加速） | 非 XR（已显式剔除） |
| 2611.14093 | BODYinTRANSIT-Lab: Multimodal Dataset for Sensory-Driven Transformation（身体感知数据集，XR 关联薄弱） | 非 XR（已显式剔除） |
| 2611.14373 | Gaussian Process-Augmented MPC Contouring Control for 6-DoF Trajectory Tracking（加工轨迹跟踪控制） | 非 XR（已显式剔除） |

- 结论：**0 漏网、无 backfill**；上批 15 篇 XR 主批入馆完整（421 篇未入馆者中无 XR 命中）。

---

## 三、数据源探测记录（Step 2）

| 源 | 状态 | 关键证据 |
|---|---|---|
| API `export.arxiv.org` / `arxiv.org/api/query` | 200（双主机） | `submittedDate` 前沿 = **2026-11-10**；`[20261112 TO 20261112]` cs.CV **0 篇**；`--since 2026-11-11` → **WROTE=0** |
| RSS `rss.arxiv.org`（7 分类） | 200 但全空 | 7 分类各 **0 条 item**，`lastBuildDate` = Thu, 12 Nov 2026 05:00 UTC（同批重建） |
| listing `arxiv.org/list/*/recent` | 200 | 7 分类最新日组 11-11；`pastweek` 一致；跨学科四分类最新日组 11-11 |

- 判定：**0 篇新候选**，不进入 Steps 3-7（全文抓取 / 评分 / 三关 / Top10）。

---

## 四、文献库最新前沿参考（11-11 公告批次 · 19 篇 · 非当日新拉取）

以下为 11-12 运行处理的 11-11 公告批次（主批 15 篇 + backfill-1112 4 篇），完整 7 维表见 [papers/daily/2026-11-13/7dim-table.md](../papers/daily/2026-11-13/7dim-table.md)：

| # | arXiv | 标题 | 赛道 | 总分 | 等级 | 批次 |
|---|---|---|---|---|---|---|
| 1 | 2505.20858 | TFD-SfM：无轨迹稠密运动恢复结构 | 重建与SLAM | **4.15** | A | backfill |
| 2 | 2611.13626 | FlashMotion：超快长时序 3D 动作生成 ⭐ | 内容生成 | **4.08** | A | 主批 |
| 3 | 2611.13528 | GEMOR-GS：全局外参精化的 3DGS SLAM 建图与在线重定位 ⭐ | 重建与SLAM | **3.87** | A | 主批 |
| 4 | 2605.22715 | AnyMo：野外人体运动的几何感知与设置无关建模 | 化身与人体 | **3.85** | A | backfill |
| 5 | 2611.13662 | NIF-VIO：跨惯性／非惯性参考系的视觉-惯性里程计 ⭐ | 重建与SLAM | **3.78** | A | 主批 |
| 6 | 2611.14062 | 建筑机器人的人在环控制范式：从 VR 遥操作到半自治双臂作业 ⭐ | 系统与平台 | **3.66** | A | 主批 |
| 7 | 2611.13772 | RF3DGS：自先验的无反射 3D 高斯泼溅 ⭐ | 神经渲染 | **3.63** | A | 主批 |
| 8 | 2611.13654 | EgoHMP：以第一视角线索在 3D 场景中精确预测人体运动 ⭐ | 化身与人体 | **3.62** | A | 主批 |
| 9 | 2611.13808 | FastWild-GS：紧凑逐图外观自适应的分钟级野外高斯泼溅 ⭐ | 神经渲染 | **3.58** | B | 主批 |
| 10 | 2611.13486 | 第一视角视频中的手-物接触转场检测 ⭐ | 感知与认知 | **3.44** | B | 主批 |
| 11 | 2608.04971 | 探索投影与头显之间的跨现实转场：面向沉浸式数字艺术 | 空间计算与UI | **3.37** | B | backfill |
| 12 | 2611.12912 | 大范围空间对齐锚点：借外部漂移校正追踪扩展 XR 锚点精度 ⭐ | 空间计算与UI | **3.30** | B | 主批 |
| 13 | 2611.13280 | RetinexGS：Retinex 启发的低照 RAW 高斯泼溅重建 ⭐ | 神经渲染 | **3.30** | B | 主批 |
| 14 | 2611.13628 | DepthGS：深度引导与自适应正则的高质量表面重建高斯泼溅 | 重建与SLAM | **3.23** | B | 主批 |
| 15 | 2503.00868 | 物理驱动的单目视频动态流体资产提取：生成式 3DGS | 内容生成 | **3.20** | B | backfill |
| 16 | 2611.14029 | 在哪里即兴？真实与虚拟 XR 空间对音乐创造力、共在感、情绪与心流的影响 | 感知与认知 | **3.07** | B | 主批 |
| 17 | 2611.14389 | 面向三维形状触觉传达的编码策略评估 | 触觉与多模态 | **2.92** | C | 主批 |
| 18 | 2611.13906 | 刺激消失式 MR P300 界面的目标选择：可行性与可区分线索对比 | 交互与输入 | **2.77** | C | 主批 |
| 19 | 2611.13296 | XR 实时三维元胞自动机仿真的统一交互框架 | 系统与平台 | **1.55** | C | 主批 |

---

## 五、附录

### 5.1 覆盖度三关（本日不触发）

- 门① 同质去重 / 门② 赛道覆盖 / 门③ 价值天花板：候选池 0 篇，三关均不触发。
- 门③ 参考值现算：库内近 30 天 Top10 均分 **4.437**（窗口 2026-10-14~2026-11-13（454 条入窗）；Top10 = 2610.19674 SMoRe 4.57 / 2610.23772 视频扩散化身 4.57 / 2611.06817 Open-HumanScale 4.57 / 2611.11169 Map2SLAM 4.57 / 2610.39399 ACD-GS 4.37 / 2611.09458 左右一致立体匹配 4.37 / 2611.07902 XM4D 4.36 / 2610.34263 RacerGS 4.35 / 2611.08578 HaNDF 4.34 / 2609.31418 CognitiveReality 4.30）。

### 5.2 证据等级分布

- 本日无新抓取。参考表 19 篇：18 篇 **L0/FULL** + 1 篇 **L1/PARTIAL**（2611.13296：arXiv HTML 404、ar5iv 仅摘要页 4,350 字符，11-12 运行人工抽看无正文节后改判，按摘要级评估并显式声明）；无 ABSTRACT_ONLY。

### 5.3 失败/降级清单

- 无抓取失败（本日不抓取）。数据源：RSS 7 分类空源（与 listing 全无 11-12 日组一致，非故障）；API 双主机 200，仅 `submittedDate` 前沿停在 11-10。
- 采集保护：摘要级过滤采用 50 id/批 + 12s 间隔，meta 覆盖率 421/421 = 1.0000，未出现 11-12 记录过的 429 静默丢批。

### 5.4 产物清单

| 产物 | 路径 |
|---|---|
| 状态报告 | `reports/XR-Daily-Report-2026-11-13.md` |
| 前沿参考 7 维表 | `papers/daily/2026-11-13/7dim-table.md`（19 篇） |
| 运行日志 | `papers/daily/2026-11-13/run_log.md` |
| 对账数据 | `data/audit_1113_days.json` / `data/audit_1113_alldays.json` / `data/missed_listing_1113.json` / `data/newday_1113.json` / `data/missed_new_1113.json` / `data/missed_xr_abstract_1113.json` |
| registry 备份 | `papers/library/registry.jsonl.bak-20261113`（标题修补前） |
| MOC 总索引 | `papers/MOC/MOC-总索引.md`（11-13 状态注记 + 速查入口 + 批次索引行 + 页脚刷新） |
| 前端 | `web/xr-paper-hub.html`（重建） |

### 5.5 发布记录

- 渠道① WorkBuddy 托管（workbuddy_sites_deploy）：见收尾汇报（自 10-21 起连续不可用，URL 已 403）。
- 渠道② GitHub Pages：见收尾汇报（commit + `push_to_github.py --incremental` + deploy run + Pages 200 核验）。

---

*报告生成：2026-11-13 02:30 自动化运行（xr-paper-daily-brief skill · 9 步流水线）。*
