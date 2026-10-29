# XR 每日论文雷达 · 运行报告 · 2026-10-30（周五 02:30）

> **诚实口径声明**：本运行日（2026-10-30，周五 02:30）**无新增可处理论文**。经三源交叉验证，**arXiv 10-29（周四）公告批次未释放**（listing 7 分类最新公告日仍为 2026-10-28、API 全分类 submittedDate 10-28/10-29 区间 0 篇、RSS 全局重建后空源）——属 arXiv 侧跳空/延迟，非本地数据源故障；该批次（10-28 公告组）已于 10-29 运行完整处理（主批 20 篇 + backfill-1029 4 篇），本日复采复核 **0 漏网**。**本报告不包含任何「当日新论文」解读、不虚构 Top10/评分/S 级**；文末附表为文献库最新前沿参考。

---

## 一、执行摘要

| 项 | 结论 |
|---|---|
| 运行性质 | **状态报告日**（无新稿；漏网对账 + 三源探针 + 知识库存量维护 + 前端重建与双渠道发布） |
| 公告状态 | listing 7 分类最新公告日均为 **2026-10-28**（与 10-29 运行逐项一致）；**10-29 公告批次未释放**（arXiv 侧跳空/延迟，首次遇到的工作日公告缺失） |
| 漏网对账 | 10-28 公告组 462 篇复采，未入馆 443 篇摘要级 XR 命中 14 篇，**全部为 10-29 运行已显式剔除的非 XR 稿** → **0 漏网**；无漏跑公告日（10-29 根本没有发生公告），无需 backfill |
| 数据源 | API 双主机 200（全分类 submittedDate 10-28/10-29 = 0，前沿停滞 10-27）；RSS 10-29 04:00 UTC 全局重建后 6/7 分类 0 条目（其他学科同样空源）；cs.AI feed 残留 10-28 批次陈旧内容（407 条），7 条 KW 命中全部已处置 |
| 新入馆论文 | **0 篇**（registry 维持 **693 条**：S 16 / A 329 / B 273 / C 75） |
| 新原子笔记 | 0 篇（维持 **384 篇**） |
| 库内近 30 天 Top10 均分 | **4.420**（现算，窗口 2026-09-30~10-30 共 422 条入窗；门③ 为校准关，本日无候选不触发） |
| 交付 | 状态报告 1 + 前沿参考 7 维表 1（24 篇）+ run_log 1 + MOC 总索引维护 + 前端重建与双渠道发布 |

**下一批预期**：10-31（周六）运行须复核 10-29 公告是否延迟释放；若已发布则按标准流水线补处理（诚实标注公告日 10-29 ≠ 拉取日 10-31）；若 10-29/10-30 连续无公告，继续状态日模式并挂账观察 arXiv 侧状态。门③ 均分务必现算（勿沿用 4.420）。

---

## 二、漏网对账（Step 1，本日核心工作）

对账目的：确认自上一批次公告日（2026-10-28）至今是否有漏跑公告日或漏收 XR 论文。

### 2.1 公告日头核验（目标窗口 ≥ 2026-10-28）

| 分类 | 最新公告日 | 10-28 日组声明/实采 |
|---|---|---:|
| cs.CV | Wed, 28 Oct 2026 | 156 / 156 |
| cs.GR | Wed, 28 Oct 2026 | 10 / 10 |
| cs.HC | Wed, 28 Oct 2026 | —（并入 cs.GR 组采齐） |
| cs.MM | Wed, 28 Oct 2026 | 8 / 8 |
| cs.RO | Wed, 28 Oct 2026 | 85 / 85 |
| cs.AI | Wed, 28 Oct 2026 | 254 / 254 |
| eess.IV | Wed, 28 Oct 2026 | 8 / 8 |

- **无 10-29 公告日组**：recent / pastweek 视图（含 cache-buster 复验）均无 10-29 日组。
- **10-29 公告批次未释放的三源互证**：
  1. listing：7 分类（recent + pastweek + 缓存穿透复验）最新日组全部为 Wed, 28 Oct 2026；
  2. API：全分类 `submittedDate:[202610280000 TO 202610292359]` = **0 篇**，cs.CV/cs.AI 单查亦 0；`submittedDate` 降序前沿 = 10-27（2610.37668 等，即 10-28 公告组来源，已全部入馆）；
  3. RSS：10-29 04:00 UTC 全局重建后，7 分类中 6 个 0 条目；其他学科（math.AP / physics.optics / cs.LG / cs.CL / eess.AS / q-bio.NC）同样 0 条目——排除沙箱代理侧问题，指向 arXiv 公告侧跳空/延迟。
- arXiv 主页无维护/中断通知。

### 2.2 10-28 公告组复采复核（验证上一批处理完整性）

- 复采 10-28 公告组 **462 篇**（与 10-29 运行采集逐项一致），未入馆 **443 篇**（registry 现含该组 19 篇 XR = 10-29 运行主批）。
- 摘要级过滤（`scripts/filter_missed_xr_abstract.py`）命中 **14 篇**，逐篇核对均为 10-29 运行已显式剔除的非 XR 稿：

| ID | 标题（摘要级命中） | 10-29 运行剔除理由 |
|---|---|---|
| 2610.36309 | Bridging Exploration and Loss of Plasticity in On-Policy RL | RL 可塑性（非 XR） |
| 2610.36454 | SVIn+: Underwater State Estimation with 3D Sonar | 水下声呐（非 XR） |
| 2610.36599 | Camera-to-Quadruped Robot Pose Estimation | 四足姿态（非 XR） |
| 2610.36615 | Mimetic Embodiment Transfer of Human-Humanoid Interaction | 人形交互迁移（非 XR） |
| 2610.36719 | SAGE: Saliency-Annealed Gated Encoder | ViT 骨干（非 XR） |
| 2610.36793 | Visual Autoregressive Generation with Next Token Imagination | 视觉 AR 生成（非 XR） |
| 2610.36859 | ActiveAlign: Aligning Egocentric Manipulation via Active Perception | 机器人主动感知（非 XR） |
| 2610.37111 | RAVEN: Active SLAM for Aerial Exploration | 无人机主动 SLAM（非 XR） |
| 2610.37406 | CTBakeGS: Baking CT Volume Renderings into 3DGS | 医学 CT 烘焙（非 XR） |
| 2610.37509 | Ego-CEVR: Cross-Embodiment Visual Representations | 跨本体 VLA（非 XR） |
| 2610.37545 | GroundControl: Satellite-Conditioned Multi-View Diffusion | 卫星 NVS（非 XR） |
| 2610.37582 | EgoThumb: Supernumerary Robotic Thumb | 机械拇指（非 XR） |
| 2610.37619 | Perceiving and Predicting Dynamic Sports | 网球时空（非 XR） |
| 2610.37626 | Know, then Draw: A New Learning Paradigm for Visual Generation | 视觉生成范式（非 XR） |

**结论：10-28 公告批次无 XR 漏网；无漏跑公告日（10-29 无公告发生）；无需 backfill。**

---

## 三、数据源探测记录（Step 2）

- `fetch_rss.py` 7 分类：cs.AI 407 条（**陈旧 feed**：内容为 10-28 公告批次，pubDate 10-29，id 上限 2610.37668 = 10-27 提交），其余 6 类 0 条；KW 命中 7 条。
- 7 条 KW 命中去向核验（防误纳陈旧 feed 内容）：

| ID | 标题 | 处置 |
|---|---|---|
| 2610.36384 | SOMA（第一视角人体运动基准） | 已在 registry（10-29 运行入馆，门② 回补 Top10） |
| 2610.37149 | GCSR-OCC（开放词汇占用预测） | 已在 registry（10-29 运行入馆） |
| 2604.23018 | AmaraSpatial-10K（3D 资产数据集） | 已在 registry（backfill-1029 入馆） |
| 2610.36859 | ActiveAlign（机器人主动感知） | 10-29 运行已剔非 XR |
| 2610.37545 | GroundControl（卫星 NVS） | 10-29 运行已剔非 XR |
| 2506.19846 | HiMA-Ecom（多智能体记忆基准） | 旧稿 replace 再公告（非 10-29 公告内容） |
| 2605.29927 | Does The Way You Plan Matter? | 旧稿 replace 再公告（非 10-29 公告内容） |

- 判定：**0 篇新候选**，不进入 Steps 3-7。

---

## 四、文献库最新前沿参考（10-28 公告批次 · 24 篇 · 非当日新拉取）

以下为 10-29 运行处理的 10-28 公告批次 7 维参考表（主批 20 篇 + backfill-1029 4 篇），完整版见 [papers/daily/2026-10-30/7dim-table.md](../daily/2026-10-30/7dim-table.md)：

| # | arXiv | 标题 | 赛道 | 总分 | 等级 | 批次 |
|---|---|---|---|---|---|---|
| 1 | 2610.37602 | RESPLE2：惯性知情的非均匀 B 样条递归多传感器里程计 ⭐ | 重建与SLAM | **4.30** | A | 主批 10-29 |
| 2 | 2610.37036 | GraftRay：路径追踪的物理一致网格插入高斯场景 ⭐ | 内容生成 | **4.20** | A | 主批 10-29 |
| 3 | 2610.36853 | LingGS：几何预测与相机跟踪解耦的高保真高斯 SLAM ⭐ | 重建与SLAM | **4.15** | A | 主批 10-29 |
| 4 | 2610.35902 | StereoSplat：立体接地的度量尺度前馈 3DGS ⭐ | 神经渲染 | **4.07** | A | 主批 10-29 |
| 5 | 2610.36876 | HoloRecon：前馈几何验证的长程全景一致重建 ⭐ | 重建与SLAM | **4.07** | A | 主批 10-29 |
| 6 | 2610.36312 | SG²SLAM：空间几何信息的单目户外 3DGS SLAM | 重建与SLAM | **4.00** | A | 主批 10-29 |
| 7 | 2610.36760 | GeoGSplat：几何接地的非像素对齐高斯泼溅 ⭐ | 神经渲染 | **4.00** | A | 主批 10-29 |
| 8 | 2610.37172 | DomeGS：无界 3DGS 的感知一致背景补全（VR） ⭐ | 渲染与显示 | **4.00** | A | 主批 10-29 |
| 9 | 2610.36168 | PrinGS：高斯泼溅的后训练隐私保护 ⭐ | 渲染与显示 | **3.92** | A | 主批 10-29 |
| 10 | 2610.34235 | ParetoGS：稀疏适配锚点的连续预算高质量 3DGS ⭐ | 渲染与显示 | **3.85** | A | 主批 10-29 |
| 11 | 2610.36384 | SOMA：第一视角细粒度人体运动理解基准 ⭐ | 评估与数据集 | **3.79** | A | 主批 10-29 |
| 12 | 2510.01767 | LoBE-GS：负载均衡的高效大规模 3DGS 训练 | 系统与平台 | **3.73** | A | backfill-1029 |
| 13 | 2610.37271 | HILMARTS：移动 AR 胸腔手术虚拟模型-患者配准 | 空间计算与UI | **3.73** | A | 主批 10-29 |
| 14 | 2604.23018 | AmaraSpatial-10K：空间计算与具身 AI 的 3D 资产数据集 | 评估与数据集 | **3.67** | A | backfill-1029 |
| 15 | 2605.31466 | VolFill：体素流匹配的单图 amodal 场景重建 | 重建与SLAM | **3.65** | A | backfill-1029 |
| 16 | 2610.36462 | ClusterSplat：3DGS 视觉定位的语义簇选择 | 感知与认知 | **3.65** | A | 主批 10-29 |
| 17 | 2610.37149 | GCSR-OCC：几何校准与语义路由的开放词汇占用预测 | 感知与认知 | **3.65** | A | 主批 10-29 |
| 18 | 2508.04236 | PIS3R：深度 3D 重建的超大视差图像拼接 | 重建与SLAM | **3.58** | B | backfill-1029 |
| 19 | 2610.36592 | LabWorld：交互式 4D 实验室世界学习 | 世界模型与仿真 | **3.55** | B | 主批 10-29 |
| 20 | 2610.36658 | SAGE：语义增强几何专家的点云配准 | 重建与SLAM | **3.50** | B | 主批 10-29 |
| 21 | 2610.36014 | Immersive Commons：共址 MR 的短暂空间对话设计 | 空间计算与UI | **3.12** | B | 主批 10-29 |
| 22 | 2610.36610 | 4D Reconstruction with Events & RGB（事件 | 神经渲染 | **3.00** | B | 主批 10-29 |
| 23 | 2610.37427 | TSAE：协同 VR 沟通同步的时动态语义-活动纠缠 | 感知与认知 | **2.77** | C | 主批 10-29 |
| 24 | 2610.36674 | 超越一维 RV 连续谱：七种 XR 范式的二维框架 | 空间计算与UI | **2.17** | C | 主批 10-29 |

---

## 五、附录

### 5.1 覆盖度三关（本日不触发）

- 门① 同质去重 / 门② 赛道覆盖 / 门③ 价值天花板：候选池 0 篇，三关均不触发。
- 门③ 参考值现算：库内近 30 天 Top10 均分 **4.420**（窗口 2026-09-30~10-30，422 条入窗；Top10 为 2610.03162 4.65 / 2610.03283 4.58 / 2610.19674 4.57 / 2610.23772 4.57 / 2610.34263 4.35 / 2610.18872 4.30 / 2610.22778 4.30 / 2609.31418 4.30 / 2610.37602 4.30 / 2610.03192 4.28）。

### 5.2 证据等级分布

- 本日无新抓取。参考表 24 篇证据等级：22 篇 FULL（L0）+ 1 篇 L1/PARTIAL（2610.36014 Immersive Commons，ar5iv 仅摘要页，10-29 运行已按摘要级评估并显式声明）+ 1 篇 backfill L0/FULL；无 ABSTRACT_ONLY。

### 5.3 失败/降级清单

- 无抓取失败。数据源异常 1 项：RSS cs.AI 残留 10-28 批次陈旧 feed（已核验处置，见 §三）；10-29 公告批次未释放（arXiv 侧，已三源互证并挂账观察）。

### 5.4 产物清单

| 产物 | 路径 |
|---|---|
| 状态报告 | `reports/XR-Daily-Report-2026-10-30.md` |
| 前沿参考 7 维表 | `papers/daily/2026-10-30/7dim-table.md`（24 篇） |
| 运行日志 | `papers/daily/2026-10-30/run_log.md` |
| 对账数据 | `data/missed_listing_1030.json` / `data/missed_xr_abstract_1030.json` / `data/raw/2026-10-30_rss.jsonl` |
| MOC 总索引 | `papers/MOC/MOC-总索引.md`（10-30 状态注记 + 批次索引行 + 页脚刷新） |
| 前端 | `web/xr-paper-hub.html`（重建） |

### 5.5 发布记录

- 渠道① WorkBuddy 托管（workbuddy_sites_deploy）：见收尾汇报（若工具不可用则挂账， historically 自 10-21 起连续不可用）。
- 渠道② GitHub Pages：见收尾汇报（commit + push_to_github.py --incremental + deploy run + Pages 200 核验）。

---

*报告生成：2026-10-30 02:30 自动化运行（xr-paper-daily-brief skill · 9 步流水线）。*
