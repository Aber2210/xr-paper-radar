# 2026-11-07 执行日志

## 数据源与对账（第 1-3 步）
- **漏网对账（先于拉取）**：`scripts/audit_listing_1107.py`（TARGET_DAY=2026-11-05，上批公告日；show=500 单页×7 分类）→ 7 分类最新公告日均为 **2026-11-06**（无漏跑公告日）；**11-05 组复采逐分类 declared=got**（CV 148/GR 7/HC 29/MM 6/RO 62/AI 217/IV 8，477 槽位）→ 未入馆 **386 篇**，`scripts/filter_missed_xr_abstract.py` 摘要级复核 **10 篇命中均为 11-06 运行已剔非 XR（与上批 10 篇剔除清单逐篇一致，双向差集 0）→ 0 漏网、无 backfill**（data/missed_xr_abstract_1107_g1105.json）。
- **摘要级 XR 过滤（新公告组）**：11-06 组 **386 篇唯一论文**（CV 138/GR 11/HC 22/MM 2/RO 81/AI 198/IV 6，458 槽位，全部未入馆）→ 摘要级 XR 命中 **35 篇**（data/missed_xr_abstract_1107.json，meta fetched 386/386）。
- **RSS 通道**：`scripts/fetch_rss.py` 7 分类 **WROTE=0**——周六 skipDays 节律空源（lastBuildDate 2026-11-07 05:00 UTC，非代理故障）；**本批以 listing 为唯一采集渠道**。三源互证：listing 日期头（11-06 为最新公告日）+ API published（提交日 11-04×5/11-05×30，与 11-06 公告组节律一致）+ RSS 空源（周六无公告）。
- **API 探针**：export.arxiv.org 与 arxiv.org 双主机 200。

## 甄别（第 3 步）
- 主批 XR 核心/强相关 **23 篇**入评分池；剔非 XR **12 篇**（2611.06993 JPTA 视觉语言模型直推适配 / 2611.07063 SD-LoRA 少样本视觉语言适配 / 2611.07081 WV-GS 自动驾驶宽视角合成 / 2611.07551 PreSTP 视频扩散 token 剪枝加速 / 2611.07630 事件相机 LED 跟踪（无人机引导）/ 2611.07651 GraspBench 跨机器人抓取评测 / 2611.07712 AffectiveVLA 人形机器人社交触摸 / 2611.08005 DCAP 可变接触3D物体放置 / 2611.08097 STEP 人形机器人运动 / 2611.08100 巡视器自主导航栈 / 2611.08372 MOMASPLAT 移动操作示范增广 / 2611.08407 Social Humanoid 人-人形交互）。
- 旧稿 replace/cross 再公告：**0 篇**（RSS 空源；listing 公告日组天然只含新提交，与 10-18 确认的「旧稿再公告只进 RSS 不进 listing 日组」机制一致）→ **无 backfill**。

## 全文抓取（第 4 步）
- 23 篇候选跑 `scripts/fetch_fulltext.py`，严格串行 3s/篇（约 3 分钟）：**22 篇 L0/FULL**（13,629–179,859 字符）+ **1 篇 L0/PARTIAL**（2611.08301 REACT：arXiv HTML 仅提供 Supplementary Material——主文（问题陈述/训练细节/数据集名称）缺失；ar5iv 无转换版（仅摘要页）；按摘要级评估并在 7 维表/报告/笔记显式声明，manifest 已改判 PARTIAL 并加 note）。无限流/降级/伪造。
- **人工复核正文中段章节**（防 11-05 ar5iv 摘要页误判教训）：22 篇 FULL 均含 Method/Experiments/Results/Conclusion 等实质章节；最小两篇（2611.07798 13,629 字符系统论文 / 2611.08398 25,978 字符设备论文）经中段抽查为真实正文（实现细节/控制回路），确认非摘要页。
- manifest 合并写入校验通过；WROTE=23>0。

## 评分与三关（第 5-6 步）
- 先抓全文再定稿。7 维加权定稿：主批 **8 A / 12 B / 3 C**（最高 XM4D 4.36 达 S 线但非重磅日按校准关记 A）。
- 门① 最大 Jaccard **0.074**（2611.08330 InstantHand vs 库内 2609.21498 VoxelTTO；<0.62，非同质）。
- 门② 纯价值 Top10 覆盖 **4 赛道**（神经渲染×3/感知与认知×3/重建与SLAM×2/化身与人体×2）<5 → **触发一次重筛**：剔除神经渲染赛道最低分 T²-Splat 3.575（与 ReferClaw 同分；按赛道冗余度与库内增量定位取舍——库内已有 MeshSplatting 直接前作），回补未覆盖核心赛道（触觉与多模态）B 级池最高分 多模态触觉显示 3.365 → 定稿 Top10 覆盖 **5 赛道** ≥5，通过（T²-Splat 仍入馆写 B 级笔记，仅不占 Top10 名额）。
- 门③ 当日最高 **4.36 < 库内近 30 天 Top10 均分 4.393**（窗口 2026-10-08~11-07、436 条入窗、现算）→ **非重磅日，无 S 级**；XM4D 4.36 达 S 线按校准关记 A（同 10-24 EgoHand/10-27 WFM/10-28 RacerGS 先例）。
- OUTDATED/SUPERSEDED **0 篇**。路线级观察：① 在线/前馈重建三篇同批（HIBS 在线 beta 泼溅、SM4RT 级联前馈 4D、InstantHand 前馈手部化身），「免优化前馈 + 在线增量」双路线并进；② 网格-高斯混合渲染两篇（T²-Splat 拓扑自适应、Gaussolve 减法范式、P-MGS 感知分配），与库内 GaMeS/Mani-GS/MeshSplatting 竞争白热化；③ 第一视角生态连续第三批强化（EgoGeneralist 统一模型 + ReferClaw 交互层 + 2611.07673 物体可供性），助手侧从感知走向交互闭环；④ 硬件类缺口仍仅 CVQPG + HoOPOE 两篇涉及近眼显示光学（本批触觉显示为台面式硬件增量，非近眼光学；波导/可变焦/Maxwellian/光场仍待补）。

## 产物（第 7-8 步）
- 报告 1 份 + 原子笔记 20 篇（grade≥B：8 A + 12 B；3 篇 C 仅入馆）+ MOC 1 份 + 总索引刷新 + 7 维表/scored/run_log 各 1 套。
- registry 808 → **831**（+23；备份 `papers/library/registry.jsonl.bak-20261107`；按 base_id 幂等）。
