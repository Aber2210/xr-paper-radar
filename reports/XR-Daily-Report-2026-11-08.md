# XR 每日论文雷达 · 运行报告 · 2026-11-08（周日 02:30）

> **诚实口径声明**：本运行日（2026-11-08，周日 02:30）**无新增可处理论文**。经三源交叉验证：listing 7 分类最新公告日均为 **2026-11-06（周五）**（11-07 周六、11-08 周日无公告日段，符合 arXiv skipDays 节律）；API `submittedDate` 前沿停滞 2026-11-05（11-06 公告组来源，已全部入馆或已裁决）；RSS 7 分类全部 0 条目（lastBuildDate Sat, 07 Nov 2026 05:00 UTC）。上一批（11-07 运行）处理的 11-06 公告批次经本日 show=500 单页全量复采复核：458 槽位 declared=got、386 篇唯一论文、未入馆 363 篇摘要级 XR 过滤 12 篇命中均为 11-07 运行已显式剔除的非 XR 稿（逐篇一致）→ **0 漏网、无 backfill**。**本报告不包含任何「当日新论文」解读、不虚构 Top10/评分/S 级**；文末附表为文献库最新前沿参考。

---

## 一、执行摘要

| 项 | 结论 |
|---|---|
| 运行性质 | **状态报告日**（周日，周六 skipDays 无公告；漏网对账 + 三源探针 + 采集完整性复核 + 知识库存量维护 + 前端重建与双渠道发布） |
| 公告状态 | listing 7 分类最新公告日均为 **2026-11-06**；11-07/11-08 周末无公告日段（skipDays 节律）；无漏跑公告日 |
| 漏网对账 | 11-06 公告组 show=500 单页全量复采：逐分类 declared=got（CV 138/GR 11/HC 22/MM 2/RO 81/AI 198/IV 6，槽位 458、唯一论文 386）；未入馆 363 篇摘要级 XR 命中 12 篇，均为 11-07 运行已剔非 XR → **0 漏网**；无需 backfill |
| 数据源 | API 双主机 200（submittedDate 前沿 11-05，已全部入馆或已裁决）；RSS 7 分类全部 0 条目（周末节律空源，WROTE=0） |
| 新入馆论文 | **0 篇**（registry 维持 **831 条**：S 17 / A 394 / B 325 / C 95） |
| 新原子笔记 | 0 篇（维持 **502 篇**） |
| 库内近 30 天 Top10 均分 | **4.399**（现算，窗口 2026-10-09~2026-11-08（431 条入窗）；门③ 为校准关，本日无候选不触发） |
| 交付 | 状态报告 1 + 前沿参考 7 维表 1（23 篇）+ run_log 1 + MOC 总索引维护 + 前端重建与双渠道发布 |

**下一批预期**：11-09（周一）02:30 运行预期仍为状态日（周末积压公告时刻 = 周一 00:00 UTC = 当日 08:00 北京时间，晚于运行时刻，同 11-02 模式）；**11-10（周二）02:30 处理 11-09 公告批次**（若 11-09 周日有公告释放）；门③ 务必现算（勿沿用 4.399）。

---

## 二、漏网对账（Step 1）

对账目的：确认自上一批次公告日（2026-11-06）至今是否有漏跑公告日或漏收 XR 论文。

### 2.1 公告日头核验（目标窗口 ≥ 2026-11-07）

| 分类 | 最新公告日 | 11-06 组 declared | 11-06 组实采 |
|---|---|---:|---:|
| cs.CV | Fri, 6 Nov 2026 | 138 | 138 |
| cs.GR | Fri, 6 Nov 2026 | 11 | 11 |
| cs.HC | Fri, 6 Nov 2026 | 22 | 22 |
| cs.MM | Fri, 6 Nov 2026 | 2 | 2 |
| cs.RO | Fri, 6 Nov 2026 | 81 | 81 |
| cs.AI | Fri, 6 Nov 2026 | 198 | 198 |
| eess.IV | Fri, 6 Nov 2026 | 6 | 6 |

- **无 11-07/11-08 公告日组**：七分类 recent 视图一致；周末无公告符合 arXiv RSS `<skipDays>` 节律（同 11-01 模式）。
- **三源互证**：① listing 七分类最新日组全部为 Fri, 6 Nov 2026；② API `submittedDate` 降序前沿 = 2026-11-05（即 11-06 公告组来源）；③ RSS 7 分类 0 条目（lastBuildDate 2026-11-07 05:00 UTC）。

### 2.2 11-06 公告组完整性复核（验证上批处理完整性）

本日复采方案（`scripts/audit_listing_1108.py`，show=500 单页×7 分类）：11-06 组各分类条目数均 <500，单页即完整包含目标组。结果：

- 逐分类 **declared = got**（上表），槽位合计 458，全局去重后 **386 篇唯一论文**，与 11-07 运行复采数字逐项一致；
- 未入馆 **363 篇**（386 − 23 篇 11-07 运行已入馆主批；11-07 运行无 backfill，listing 日组天然只含新提交）；
- 摘要级 XR 过滤（`filter_missed_xr_abstract.py`，363/363 fetched）：命中 **12 篇**，与 11-07 运行显式剔除的 12 篇非 XR **逐篇一致**：

| ID | 标题 | 11-07 运行裁决 |
|---|---|---|
| 2611.06993 | Batch-Conditioned Semantic Anchors for Robust Transductive Adaptation of Vision-Language Models（JPTA，视觉语言模型直推适配） | 非 XR（已显式剔除） |
| 2611.07063 | SD-LoRA: Training-Time Structural Distillation into LoRA for Few-Shot Vision-Language Adaptation（少样本视觉语言适配） | 非 XR（已显式剔除） |
| 2611.07081 | Wide View Synthesis from Overlapping Perspective Cameras in Autonomous Driving（WV-GS，自动驾驶宽视角合成） | 非 XR（已显式剔除） |
| 2611.07551 | Training-Free Predictive Spatio-Temporal Token Pruning for Few-Step Autoregressive Video（PreSTP，视频扩散 token 剪枝加速） | 非 XR（已显式剔除） |
| 2611.07630 | Real-Time Event-Based LED Tracking and Pose Estimation with PWM-Encoded Markers（事件相机 LED 跟踪，无人机引导） | 非 XR（已显式剔除） |
| 2611.07651 | GraspBench: Execution-Aware Cross-Robot Evaluation of 6-DoF Grasp Generation in MuJoCo（跨机器人抓取评测） | 非 XR（已显式剔除） |
| 2611.07712 | AffectiveVLA: Safe and Intent-Aware VLA Control for Human-Humanoid Social Interaction（人形机器人社交触摸） | 非 XR（已显式剔除） |
| 2611.08005 | Deformable Contact-Aware 3D Object Placement（DCAP，可变接触 3D 物体放置） | 非 XR（已显式剔除） |
| 2611.08097 | STEP: Spatiotemporal Training with Explicit Prediction for Perceptive Humanoid Locomotion（人形机器人运动） | 非 XR（已显式剔除） |
| 2611.08100 | An Integrated Open-Source Stack for Vision-Based Autonomous Navigation of Wheeled Rovers（巡视器自主导航栈） | 非 XR（已显式剔除） |
| 2611.08372 | MOMASPLAT: Dynamic Novel-View Demonstration Augmentation for Mobile Manipulation（移动操作示范增广） | 非 XR（已显式剔除） |
| 2611.08407 | Social Humanoid: Socially Responsive Human-Humanoid Interaction（人-人形交互） | 非 XR（已显式剔除） |

- API 前沿条目归属核验：submittedDate top-5 中 4 篇未入馆者（2611.08486 / 2611.08485 / 2611.08449 / 2611.08441）均在 363 篇集合内，标题明确非 XR（图表技法 / grounded 推理 / 视觉规划 / 骑行安全感知），与摘要级过滤结论一致。
- 结论：**0 漏网、无 backfill**。

---

## 三、数据源探测记录（Step 2）

- API 双主机探针 200；`submittedDate` 降序前沿 = **2026-11-05**（cs.CV top-5 published 全部 11-05；= 11-06 公告组来源）。
- RSS（7 分类探针）：**全部 0 条目**（lastBuildDate Sat, 07 Nov 2026 05:00 UTC，周末节律空源）。
- 判定：**0 篇新候选**，不进入 Steps 3-7。

---

## 四、文献库最新前沿参考（11-06 公告批次 · 23 篇 · 非当日新拉取）

以下为 11-07 运行处理的 11-06 公告批次 7 维参考表（主批 23 篇），完整版见 [papers/daily/2026-11-08/7dim-table.md](../papers/daily/2026-11-08/7dim-table.md)：

| # | arXiv | 标题 | 赛道 | 总分 | 等级 |
|---|---|---|---|---|---|
| 1 | 2611.07902 | XM4D：可证全局最优几何优化的 4D 重建 ⭐ | 重建与SLAM | **4.36** | A |
| 2 | 2611.07709 | AffineGS：空间变化仿射矫正解锁 3DGS 几何精度 ⭐ | 神经渲染 | **4.15** | A |
| 3 | 2611.08330 | InstantHand：单图前馈可动画 3D 高斯手部化身重建 ⭐ | 化身与人体 | **4.08** | A |
| 4 | 2611.08288 | HIBS：面向在线重建的分层增量 Beta 泼溅 ⭐ | 重建与SLAM | **4.01** | A |
| 5 | 2611.07909 | EDGAR：合成失败数据驱动的扩散式高斯化身高效精化 ⭐ | 化身与人体 | **3.98** | A |
| 6 | 2611.08477 | EgoGeneralist：视频原生建模统一第一视角动作-视频任务 ⭐ | 感知与认知 | **3.96** | A |
| 7 | 2611.07049 | Gaussolve：选择性溶解网格不一致内容的混合场景渲染（神经溶解场） ⭐ | 神经渲染 | **3.83** | A |
| 8 | 2611.07873 | PVDepth：几何感知时空自适应的全景视频深度估计（含 PanoCARLA ⭐ | 感知与认知 | **3.69** | A |
| 9 | 2611.06974 | T²-Splat：拓扑自适应与残差纹理解耦的三角形网格泼溅 | 神经渲染 | **3.58** | B |
| 10 | 2611.07683 | ReferClaw：以澄清提问消解用户意图的第一视角流式助手 ⭐ | 感知与认知 | **3.58** | B |
| 11 | 2611.07386 | Breaking the Modality Barrier：缺失模态鲁棒的晕 | 感知与认知 | **3.54** | B |
| 12 | 2611.08436 | SM4RT：先几何后运动的级联前馈 4D 重建 | 重建与SLAM | **3.47** | B |
| 13 | 2611.07463 | FREE-LIVO：免刚性 rig 与时间同步的紧耦合激光雷达-惯性-视觉里 | 重建与SLAM | **3.43** | B |
| 14 | 2611.07979 | P-MGS：感知优于几何——基于网格泼溅的高斯分配重思 | 神经渲染 | **3.37** | B |
| 15 | 2611.08398 | 柔软度与温度同步调制的多模态触觉显示（无泵颗粒堵塞+热皮肤） ⭐ | 触觉与多模态 | **3.37** | B |
| 16 | 2611.07345 | Slide to Report：VR 晕动症症状特异的沉浸中连续报告（N=5 | 感知与认知 | **3.29** | B |
| 17 | 2611.08301 | REACT：骨骼运动信号的实时补全（S4 多候选融合） | 交互与输入 | **3.18** | B |
| 18 | 2611.07673 | 物体与视觉语言可供性引导的第一视角动作识别 | 感知与认知 | **3.08** | B |
| 19 | 2611.07687 | Not Losing Your Way：按需创造视觉特征缓解 VIO 漂移的 | 重建与SLAM | **3.04** | B |
| 20 | 2611.07272 | VREgo：用消费级 VR 头显采集第一视角演示学习机械臂操作 | 交互与输入 | **3.00** | B |
| 21 | 2611.08321 | ControlAnything：编码智能体按需生成连接器与生成式 UI 的  | 空间计算与UI | **2.90** | C |
| 22 | 2611.07798 | VocabulARy 2.0：生成式 AR 个性化 3D 记忆术词汇学习系统 | 空间计算与UI | **2.42** | C |
| 23 | 2611.08167 | Reflective Nature Experiences in VR：促进 | 感知与认知 | **2.24** | C |

---

## 五、附录

### 5.1 覆盖度三关（本日不触发）

- 门① 同质去重 / 门② 赛道覆盖 / 门③ 价值天花板：候选池 0 篇，三关均不触发。
- 门③ 参考值现算：库内近 30 天 Top10 均分 **4.399**（窗口 2026-10-09~2026-11-08（431 条入窗）；Top10 = 2610.19674 SMoRe 4.57 / 2610.23772 视频扩散化身 4.57 / 2611.06817 Open-HumanScale 4.57 / 2610.39399 ACD-GS 4.37 / 2611.07902 XM4D 4.36 / 2610.34263 RacerGS 4.35 / 2610.18872 EgoExplorer 4.30 / 2610.22778 dGS/dBS 4.30 / 2609.31418 CognitiveReality 4.30 / 2610.37602 RESPLE2 4.30）。

### 5.2 证据等级分布

- 本日无新抓取。参考表 23 篇证据等级：22 篇 L0/FULL + 1 篇 L0/PARTIAL（2611.08301 REACT，arXiv HTML 仅补充材料，11-07 运行人工改判并显式声明）；无 ABSTRACT_ONLY。

### 5.3 失败/降级清单

- 无抓取失败。数据源状态：RSS 周末节律空源（7 分类 0 条目，非故障）；API 双主机 200。

### 5.4 产物清单

| 产物 | 路径 |
|---|---|
| 状态报告 | `reports/XR-Daily-Report-2026-11-08.md` |
| 前沿参考 7 维表 | `papers/daily/2026-11-08/7dim-table.md`（23 篇） |
| 运行日志 | `papers/daily/2026-11-08/run_log.md` |
| 对账数据 | `data/audit_1108_days.json` / `data/audit_1108_alldays.json` / `data/missed_listing_1108.json` / `data/missed_listing_1108_days.json` / `data/missed_xr_abstract_1108.json` / `data/audit_1108_newday.json` |
| MOC 总索引 | `papers/MOC/MOC-总索引.md`（11-08 状态注记 + 批次索引行 + 页脚刷新） |
| 前端 | `web/xr-paper-hub.html`（重建） |

### 5.5 发布记录

- 渠道① WorkBuddy 托管（workbuddy_sites_deploy）：见收尾汇报（若工具不可用则挂账，自 10-21 起连续不可用）。
- 渠道② GitHub Pages：见收尾汇报（commit + push_to_github.py --incremental + deploy run + Pages 200 核验）。

---

*报告生成：2026-11-08 02:30 自动化运行（xr-paper-daily-brief skill · 9 步流水线）。*
