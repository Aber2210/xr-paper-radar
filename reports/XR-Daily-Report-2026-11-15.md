# XR 每日论文雷达 · 运行报告 · 2026-11-15（周日 02:30）

> **诚实口径声明**：本运行日（2026-11-15，周日 02:30）**无新增可处理论文**——**周末 arXiv 不公告**（`skipDays` 节律），listing 7 分类最新公告日均为 **2026-11-13（周五）**，无 11-14 / 11-15 公告日组。五重互证：① listing 日期头 7 分类一致（各分类 declared=got）；② 缓存穿透复验（`recent?cb=7731`）与 `pastweek` 视图同为 `Fri, 13 Nov 2026`；③ 跨学科复核 math.AP / cs.CL 最新日组同为 11-13 → 非本分类故障；④ API 双主机 200、`submittedDate` 前沿 **11-12**（11-13 公告组来源，已全部入馆）、`[20261114 TO 20261114]` 与 `[20261115 TO 20261115]` cs.CV 均 0 篇、`--since 2026-11-13` **WROTE=0**；⑤ RSS 7 分类全部 0 条目（`lastBuildDate` Sat, 14 Nov 2026 05:00 UTC）。上一批（11-14 运行）处理的 11-13 公告组经本日全量复采复核：**695 槽位 declared=got、601 篇唯一论文**，未入馆 581 篇摘要级 XR 命中 28 篇，与 11-14 运行已显式剔除的 28 篇**逐篇 id 一致** → **0 漏网、无 backfill**。**本报告不含任何「当日新论文」解读，不虚构 Top10/评分/S 级**；第四节为文献库最新前沿参考。

---

## 一、执行摘要

| 项 | 结论 |
|---|---|
| 运行性质 | **周末状态报告日**（0 新稿；漏网对账 + 五重源核验 + 采集完整性复核 + 知识库存量维护 + 前端重建与双渠道发布） |
| 公告状态 | listing 7 分类最新公告日均为 **2026-11-13（周五）**；**无 11-14（周六）/ 11-15（周日）公告日组**（skipDays 周末节律）；跨学科 math.AP / cs.CL 同为 11-13 |
| 漏网对账 | 11-13 公告组 show=500 单页全量复采：逐分类 declared=got（CV 196/GR 6/HC 43/MM 2/RO 106/AI 321/IV 21，槽位 695、唯一论文 601）；未入馆 581 篇摘要级 XR 命中 28 篇，与 11-14 运行已剔 28 篇逐篇 id 一致 → **0 漏网**；无需 backfill |
| 数据源 | API 双主机 200（前沿 11-12；11-14 / 11-15 区间 0 篇；WROTE=0）；RSS 7 分类全部 0 条目（lastBuildDate 11-14 05:00 UTC） |
| 新入馆论文 | **0 篇**（registry 维持 **935 条**：S 18 / A 438 / B 365 / C 114） |
| 新原子笔记 | 0 篇（维持 **587 篇**；daily 目录 62 个） |
| 数据修补 | 无（交付前 `title == id` / `len(title)<12` 抽查 0 命中） |
| 库内近 30 天 Top10 均分 | **4.430**（现算，窗口 2026-10-16~2026-11-15（443 条入窗）；门③ 为校准关，本日无候选不触发） |
| 交付 | 状态报告 1 + 前沿参考 7 维表 1（28 篇）+ run_log 1 + MOC 总索引维护 + 前端重建与双渠道发布 |

**下一批预期**：周一 2026-11-16 00:00 UTC（08:00 北京时间）释放周末（11-14 / 11-15）提交积压；**下一调度（11-16 周一 02:30）早于该时刻，仍应为状态日；11-17（周二）02:30 才是处理该批次的标准运行**，须现算门③、并显式标注「公告日≠拉取日」。

---

## 二、漏网对账（Step 1）

对账目的：确认自上一批次公告日（2026-11-13）至今是否有漏跑公告日或漏收 XR 论文。

### 2.1 公告日头核验（目标窗口 ≥ 2026-11-14）

| 分类 | 最新公告日 | 11-13 组 declared | 11-13 组实采 | 11-14 组 | 11-15 组 |
|---|---|---|---:|---|---|
| cs.CV | Fri, 13 Nov 2026 | 196 | 196 | **无** | **无** |
| cs.GR | Fri, 13 Nov 2026 | 6 | 6 | **无** | **无** |
| cs.HC | Fri, 13 Nov 2026 | 43 | 43 | **无** | **无** |
| cs.MM | Fri, 13 Nov 2026 | 2 | 2 | **无** | **无** |
| cs.RO | Fri, 13 Nov 2026 | 106 | 106 | **无** | **无** |
| cs.AI | Fri, 13 Nov 2026 | 321 | 321 | **无** | **无** |
| eess.IV | Fri, 13 Nov 2026 | 21 | 21 | **无** | **无** |

- 槽位合计 **695**，全局去重 **601 篇唯一论文**（跨列表重复 94 条），与 11-14 运行采集数字逐项一致。
- **无 11-14 / 11-15 公告日组**：`audit_listing_1115.py` 对 NEW_DAYS 采到 declared=None / got=0。
- **缓存与故障排除**：① cs.CV `recent?cb=7731`（随机参数）→ 最新日组仍 `Fri, 13 Nov 2026`（103,411 bytes），排除页面缓存；② cs.CV `pastweek` 最新日组一致；③ 跨学科 math.AP（41,529 bytes）/ cs.CL（60,475 bytes）`pastweek` 最新日组同为 `Fri, 13 Nov 2026` → **周末不公告属 arXiv 全局节律，非本分类/本机故障**。

### 2.2 11-13 公告组完整性复核（验证上批处理完整性）

- 逐分类 **declared = got**（上表），未入馆 **581 篇** = 601 − 20（11-14 运行主批已入馆；该批 listing 侧无漏网），与 11-14 运行复采集合**逐篇一致**；
- 摘要级 XR 过滤（`scripts/filter_missed_1115.py`，50 id/批 + 12s 间隔；**meta fetched 581/581，覆盖率 1.0000**，缺失 0）：命中 **28 篇**；
- 与 11-14 运行已显式剔除的非 XR 集合比对：11-14 摘要级命中 43 篇，其中 **15 篇** 进入主批（另 5 篇由标题级扩展词补扫进入），剩余 28 篇即上批显式剔除者；本日 28 篇与之一一对应，**双向差集 0**。

| ID | 标题 | 11-14 运行裁决（本批复核维持） |
|---|---|---|
| 2611.15040 | Moving Beyond the DRW Model: Learning Quasar Variability（类星体光变生成建模/天体物理） | 非 XR（已显式剔除） |
| 2611.15082 | Prediction or Persistence? What Future-Prediction Scores Miss（世界模型评分指标研究） | 非 XR（已显式剔除） |
| 2611.15117 | PolyMorphWBC: Whole-Body Control from End-Effector Trajectories（四足移动操作全身控制） | 非 XR（已显式剔除） |
| 2611.15135 | ARTS: Open-Source Three-Arm Platform for Autonomy Research（三臂自主研究平台） | 非 XR（已显式剔除） |
| 2611.15216 | Where is My Mug? Training-Free Personalized Image Segmentation（个性化图像分割） | 非 XR（已显式剔除） |
| 2611.15277 | DroneDiffusion: Uncertainty-Guided Diffusion Path Planner（无人机扩散路径规划） | 非 XR（已显式剔除） |
| 2611.15280 | Autonomous Trail Racing with a Bicycle Robot（自行车机器人越野竞速） | 非 XR（已显式剔除） |
| 2611.15579 | FoveaDet: Software-Hardware Co-Design of Foveated CNN-Transformer（注视点目标检测硬件协同，非近眼显示） | 非 XR（已显式剔除） |
| 2611.15650 | Single-View RGB-D Force-Deformation Estimation（机器人操作力-形变估计） | 非 XR（已显式剔除） |
| 2611.15659 | GraSLA: Lightweight Spatial-Language-Action Model（抓取假设几何的空间-语言-动作模型） | 非 XR（已显式剔除） |
| 2611.15764 | AIFR: Adaptive Identity Feature Recovery（妆容/动漫人像扩散生成） | 非 XR（已显式剔除） |
| 2611.15766 | Prior-as-Skill: On-Policy Self-Distillation（LLM 自蒸馏） | 非 XR（已显式剔除） |
| 2611.15789 | VibePrevisBench: Agentic Coding for 4D Scene Generation in Blender（生成工具链基准） | 非 XR（已显式剔除） |
| 2611.15937 | MOSAIC: Obstacle and Spatial-Aware Framework for Manipulation（杂乱场景操作） | 非 XR（已显式剔除） |
| 2611.16282 | Robot Navigation and Obstacle Avoidance from External Cameras（外部相机机器人导航） | 非 XR（已显式剔除） |
| 2611.16417 | VBot Exo2Ego Policy: Exocentric-to-Egocentric Video Generation（数据采集与操作策略） | 非 XR（已显式剔除） |
| 2611.16424 | PhysCapBench: Cross-Domain Benchmark for Video Captioning（物理视频描述基准） | 非 XR（已显式剔除） |
| 2611.16439 | HALO: Human-Aligned Data Collection for Mobile Manipulation（全身移动操作数据采集） | 非 XR（已显式剔除） |
| 2611.16452 | Can an LVLM Perceive Event Boundaries Like a Human?（LVLM 认知评测） | 非 XR（已显式剔除） |
| 2611.16655 | MuViRL: View-Invariant Visual Speech Representation（视觉语音表征） | 非 XR（已显式剔除） |
| 2611.16728 | EgoX: Egocentric Cross-Embodiment Manipulation（第一视角跨本体操作策略） | 非 XR（已显式剔除） |
| 2611.16869 | Raysemble: Metric 3D Bone Reconstruction from a Single X-ray（单 X 光医学骨重建） | 非 XR（已显式剔除） |
| 2611.17060 | Ropedia Xperience 2: Physical AI Environments（物理 AI 环境数据规模化） | 非 XR（已显式剔除） |
| 2611.17110 | SALA: Semantically Aligned Latent Actions（具身基础模型潜动作） | 非 XR（已显式剔除） |
| 2611.17163 | UAV-Flow++: Language-Guided UAV Flight Benchmark（无人机语言引导飞行基准） | 非 XR（已显式剔除） |
| 2611.17235 | Al-Ghasali: Simulating Islamic Jurisprudential Rulings（法律推理模拟） | 非 XR（已显式剔除） |
| 2611.17238 | HEIR: Harness Egocentric Intent for Human-Robot Interactions（第一视角意图机器人交互） | 非 XR（已显式剔除） |
| 2611.17284 | Augmented Hybrid TV Services: Habits and Expectations（电视服务用户调研；augmented 关键词误命中） | 非 XR（已显式剔除） |

- 结论：**0 漏网、无 backfill**；上批 20 篇 XR 主批入馆完整（581 篇未入馆者中无 XR 命中）。

---

## 三、数据源探测记录（Step 2）

| 源 | 状态 | 关键证据 |
|---|---|---|
| API `export.arxiv.org` / `arxiv.org/api/query` | 200（双主机） | `submittedDate` 前沿 = **2026-11-12**（cs.CV / cs.GR / cs.RO top-5 一致）；`[20261114 TO 20261114]` 与 `[20261115 TO 20261115]` cs.CV **0 篇**；`--since 2026-11-13` → **WROTE=0** |
| RSS `rss.arxiv.org`（7 分类） | 200 但全空 | 7 分类各 **0 条 item**（各 892–900 bytes），`lastBuildDate` = Sat, 14 Nov 2026 05:00 UTC（同批重建，周末节律空源） |
| listing `arxiv.org/list/*/recent` | 200 | 7 分类最新日组 11-13；`recent?cb=` 与 `pastweek` 一致；跨学科 math.AP / cs.CL 最新日组 11-13 |

- 判定：**0 篇新候选**，不进入 Steps 3-7（全文抓取 / 评分 / 三关 / Top10）。

---

## 四、文献库最新前沿参考（11-13 公告批次 · 28 篇 · 非当日新拉取）

以下为 11-14 运行处理的 11-13 公告批次（主批 20 篇 + backfill-1114 8 篇），完整 7 维表见 [papers/daily/2026-11-15/7dim-table.md](../papers/daily/2026-11-15/7dim-table.md)：

| # | arXiv | 标题 | 赛道 | 总分 | 等级 | 批次 |
|---|---|---|---|---|---|---|
| 1 | 2603.01178 | riMESA：面向真实世界协同 SLAM 的共识 ADMM | 重建与SLAM | **4.50** | A | backfill |
| 2 | 2607.14203 | Instant NuRec：面向驾驶场景仿真的前馈三维高斯重建 | 世界模型与仿真 | **4.28** | A | backfill |
| 3 | 2611.15153 | MatrixSplat：面向 GPU 的矩阵并行、特征可扩展 3D Gaussian ⭐ | 渲染与显示 | **4.15** | A | 主批 |
| 4 | 2611.16012 | 面向第一人称视频的拓扑感知 4D Gaussian Splatting（Topo-4 ⭐ | 重建与SLAM | **4.07** | A | 主批 |
| 5 | 2611.16840 | Kosmo-GFM：面向生产的几何基础模型 ⭐ | 重建与SLAM | **3.93** | A | 主批 |
| 6 | 2611.16259 | 能重建多少就重建多少：无干扰物的 4D Gaussian Splatting（4D  ⭐ | 神经渲染 | **3.85** | A | 主批 |
| 7 | 2611.17331 | TTB：面向 decoder-only 视角合成模型的测试时烘焙加速渲染 ⭐ | 神经渲染 | **3.85** | A | 主批 |
| 8 | 2510.03857 | OMG4：面向高效动态场景表示的优化最小 4D Gaussian Splatting | 神经渲染 | **3.80** | A | backfill |
| 9 | 2605.21714 | AVI-HT：面向手套式 3D 手部追踪的自适应视觉–IMU 融合 | 交互与输入 | **3.73** | A | backfill |
| 10 | 2611.14895 | HeadIO：面向头戴设备的体坐标系航向分解神经惯性里程计 ⭐ | 重建与SLAM | **3.63** | A | 主批 |
| 11 | 2611.15435 | ThermalSplat：面向稀疏视角热红外三维重建的可泛化无位姿 Gaussian ⭐ | 重建与SLAM | **3.58** | B | 主批 |
| 12 | 2611.15429 | IncR-3DSGG：基于有位姿 RGB 图像的增量三维场景图生成与特权深度监督 ⭐ | 重建与SLAM | **3.57** | B | 主批 |
| 13 | 2611.15561 | 基于通用粒子系统的沉浸式视觉遮蔽碰撞预防 ⭐ | 交互与输入 | **3.55** | B | 主批 |
| 14 | 2611.15437 | SteinPnP：PnP 问题中的非参数位姿不确定性量化 | 重建与SLAM | **3.50** | B | 主批 |
| 15 | 2603.09741 | ENIGMA-360：面向工业场景人类行为理解的自我–外部视角数据集 | 评估与数据集 | **3.49** | B | backfill |
| 16 | 2611.16793 | EG360：基于自适应全景-透视蒸馏与球面跨层特征融合的高效可泛化 360° 深度估 | 重建与SLAM | **3.45** | B | 主批 |
| 17 | 2607.05243 | GUSH3R：单目视频前馈式动态人体–场景高斯重建 | 重建与SLAM | **3.42** | B | backfill |
| 18 | 2508.16731 | COSMO-Bench：协同 SLAM 优化基准 | 评估与数据集 | **3.34** | B | backfill |
| 19 | 2611.15802 | RUMI：面向机器人学习的 Robotiq 匹配型通用操作接口，结合增强现实（AR） | 交互与输入 | **3.22** | B | 主批 |
| 20 | 2611.16171 | MRxD：混合现实跨设备交互的使用模式框架 ⭐ | 空间计算与UI | **3.17** | B | 主批 |
| 21 | 2611.16472 | 边缘端 RGB-D SLAM：在 Raspberry Pi 5 上基准测试与剖析 R | 评估与数据集 | **3.15** | B | 主批 |
| 22 | 2611.15526 | SCR-Mamba：骨架条件 Mamba 与跨尺度增量细化用于高效三维人体姿态估计 | 化身与人体 | **3.08** | B | 主批 |
| 23 | 2512.10095 | ReflFlow：几何引导光线追踪的动态高光重建 | 渲染与显示 | **3.00** | B | backfill |
| 24 | 2611.16056 | BiScopeNet：文本引导的手别对齐用于第一视角子动作识别 | 感知与认知 | **2.77** | C | 主批 |
| 25 | 2611.17018 | 探索面向包容性小组对话的社会可接受 3D 反馈设计 | 交互与输入 | **2.77** | C | 主批 |
| 26 | 2611.15143 | 基于 V-JEPA 特征的多视图三维重建 | 重建与SLAM | **2.06** | C | 主批 |
| 27 | 2611.16446 | 面向洪水危机管理中公民参与训练的严肃游戏（概念与研究议程） | 感知与认知 | **1.60** | C | 主批 |
| 28 | 2611.16594 | 通过沉浸式多用户游戏化进行语言学习（概念与实验设计） | 交互与输入 | **1.40** | C | 主批 |

> 说明：backfill-1114 中 riMESA（2603.01178）实测 4.50 达 S 线，但按既有口径（backfill 不参与重磅日判定）记 **A**，与 11-14 运行报告一致。

---

## 五、附录

### 5.1 覆盖度三关（本日不触发）

- 门① 同质去重 / 门② 赛道覆盖 / 门③ 价值天花板：候选池 0 篇，三关均不触发。
- 门③ 参考值现算：库内近 30 天 Top10 均分 **4.430**（窗口 2026-10-16~2026-11-15（443 条入窗）；Top10 = 2610.23772 视频扩散化身 4.57 / 2611.06817 Open-HumanScale 4.57 / 2611.11169 Map2SLAM 4.57 / 2603.01178 riMESA 4.50 / 2610.39399 ACD-GS 4.37 / 2611.09458 跨注入左右一致立体匹配 4.37 / 2611.07902 XM4D 4.36 / 2610.34263 RacerGS 4.35 / 2611.08578 HaNDF 4.34 / 2610.22778 dGS-dBS 4.30）。

### 5.2 证据等级分布

- 本日无新抓取。参考表 28 篇：**全部 L0/FULL**（11-14 运行 43,212–171,293 字符，无 PARTIAL / ABSTRACT_ONLY / L5）。

### 5.3 失败/降级清单

- 无抓取失败（本日不抓取）。数据源：RSS 7 分类空源（周末节律，与 listing 全无 11-14 / 11-15 日组一致，非故障）；API 双主机 200，仅 `submittedDate` 前沿停在 11-12（11-13 公告组来源，已全部入馆）。
- 采集保护：摘要级过滤 50 id/批 + 12s 间隔，meta 覆盖率 581/581 = 1.0000，未出现 11-12 记录过的 429 静默丢批。

### 5.4 产物清单

| 产物 | 路径 |
|---|---|
| 状态报告 | `reports/XR-Daily-Report-2026-11-15.md` |
| 前沿参考 7 维表 | `papers/daily/2026-11-15/7dim-table.md`（28 篇） |
| 运行日志 | `papers/daily/2026-11-15/run_log.md` |
| 对账数据 | `data/audit_1115_days.json` / `data/audit_1115_alldays.json` / `data/missed_prev_1115.json` / `data/newday_1115.json` / `data/missed_new_1115.json` / `data/missed_xr_abstract_1115.json` / `data/gates_1115.json` |
| MOC 总索引 | `papers/MOC/MOC-总索引.md`（11-15 状态注记 + 速查入口 + 批次索引行 + 页脚刷新） |
| 前端 | `web/xr-paper-hub.html`（重建） |

### 5.5 发布记录

- 渠道① WorkBuddy 托管（workbuddy_sites_deploy）：见收尾汇报（自 10-21 起连续不可用，URL 已 403）。
- 渠道② GitHub Pages：见收尾汇报（commit + `push_to_github.py --incremental` + deploy run + Pages 200 核验）。

---

*报告生成：2026-11-15 02:30 自动化运行（xr-paper-daily-brief skill · 9 步流水线）。*
