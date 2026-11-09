# 2026-11-10 执行日志

## 数据源与对账（第 1-3 步）
- **漏网对账（先于拉取）**：`scripts/audit_listing_1110.py`（PREV_DAY=2026-11-06 上批公告日 / NEW_DAY=2026-11-09；show=500 单页×7 分类，目标组 declared≠got 自动补采后续页 continued/last 兼容）→ 7 分类最新公告日均为 **2026-11-09**；**11-06 组逐分类 declared=got**（CV 138/GR 11/HC 22/MM 2/RO 81/AI 198/IV 6，458 槽位）→ 未入馆 **363 篇**与 11-08/11-09 运行集合**逐篇一致（diff 0）**，沿用上批摘要级结论（12 篇命中均为已剔非 XR）→ **0 漏网**。
- **摘要级 XR 过滤（新公告组）**：11-09 组 **377 篇唯一论文**（CV 117/GR 7/HC 28/MM 3/RO 60/AI 220/IV 17，452 槽位）→ 摘要级 XR 命中 **18 篇**（data/missed_xr_abstract_1110.json；`scripts/convert_newday_1110.py` 转格式 + `scripts/filter_missed_xr_abstract_1110.py`，meta fetched 377/377 全量）。
- **数据源**：`export.arxiv.org` 探针 **HTTP 502**（本批实测）→ 立即切 `https://arxiv.org/api/query`（200，submittedDate 前沿 11-06，与「11-09 公告组来源=11-05/11-06 提交」节律一致）；RSS 7 分类 HTTP 200（cs.CV 210 / cs.AI 397 / cs.RO 103 / cs.HC 40 / eess.IV 24 / cs.GR 8 / cs.MM 4，lastBuildDate 2026-11-09 05:00 UTC）→ 去重 **660** → KW 命中 **31**（WROTE=31）。
- **提交日核验**：API id_list 逐篇 published + 版本号（data/meta_1110.json）→ 17 篇 **v1**（2611.08654 11-05 + 16 篇 11-06）为真新提交；14 篇 **v2+** 为再公告（9 篇未入馆 + 5 篇已在库）。**RSS published 字段是公告时间戳（2026-11-09），不可当提交日**。

## 甄别（第 3 步）
- 主批 XR 核心/强相关 **14 篇**入评分池；剔非 XR **3 篇 v1**（2611.08654 CS-Pi 约束满足流策略采样 / 2611.08857 STRIDE 人形机器人步态 RL / 2611.09679 PIV 自主流场测量）+ **5 篇语义歧义或纯机器人**（2611.09041 DobotTrack 具身行人跟踪 / 2611.09096 TraF 自回归长视频生成「AR=autoregressive」/ 2611.09717 事件相机航天器位姿 / 2611.09795 AR-Edit 视频编辑「AR=autoregressive」/ 2611.08920·2611.08939·2611.09293·2611.08954·2611.09816·2611.08989 标题级候选中经摘要核实为机器人抓取/触觉仿真/世界动作模型/通用空间表征，非 XR）。
- 旧稿 v2+ 未入馆 **9 篇**：**4 篇 XR → backfill-1110**（2605.16981 / 2511.18127 / 2607.24409 / 2605.31557）+ 5 篇非 XR（2604.08410 机器人灵巧抓取 / 2606.01946 电磁跟踪医疗工具 / 2610.26165 TriTD 自回归视频 / 2610.40748 WorldBridge 机器人世界动作模型 / 2611.07551 视频扩散 token 剪枝）。
- 库内 v2 再公告 **5 篇**剔除（2610.13549 / 2611.00375 / 2611.00482 / 2611.06817 / 2606.16881）。

## 全文抓取（第 4 步）
- 18 篇候选跑 `scripts/fetch_fulltext.py`，严格串行 3s/篇（约 1 分钟）：**16 篇 L0/FULL**（25,010–148,056 字符）+ **2 篇 L1/PARTIAL**——2611.09708（可穿戴触觉 I/O）与 2611.09195（InstantHMR）：**arXiv HTML 404（该两稿无 HTML 版）、ar5iv 仅返摘要页（4,839 / 4,731 字符，无 Introduction/Method/Results 节）**，本机缺 pdfminer.six / pdftotext（pip 镜像亦不可达）无法解析 PDF → manifest 改判 PARTIAL 并加 note，按摘要级评估并在 7 维表/报告/笔记显式声明，**未脑补任何未核实的数值或架构**。
- **人工复核**：逐篇检查正文是否含 Introduction/Method/Experiments 节（2611.09584 46,548 字符虽无字面 "Introduction" 但含 Method/Experiment 节，为真实正文）；WROTE=18>0；manifest 合并写入校验通过。

## 评分与三关（第 5-6 步）
- 先抓全文再定稿。7 维加权定稿：主批 **7 A / 7 B**（最高 4.37 立体匹配左右一致性，4 篇 ≥4.20 达 S 线但非重磅日按校准关记 A）。
- 门① 最大 Jaccard **0.054**（2611.09129 TouchAnnotator vs 库内 2609.38615 Exo2EgoHOI；<0.62，非同质）。
- 门② 定稿 Top10 覆盖 **7 赛道**（重建与SLAM×2 / 化身与人体×2 / 触觉与多模态×2 / 内容生成×1 / 系统与平台×1 / 评估与数据集×1 / 感知与认知×1）≥5，通过，**未触发重筛**；全批亦 7 赛道。
- 门③ 当日最高 **4.37 < 库内近 30 天 Top10 均分 4.399**（窗口 2026-10-11~11-10、397 条入窗、现算；Top10 = SMoRe 4.57 / 视频扩散化身 4.57 / Open-HumanScale 4.57 / ACD-GS 4.37 / XM4D 4.36 / RacerGS 4.35 / EgoExplorer 4.30 / dGS-dBS 4.30 / CognitiveReality 4.30 / RESPLE2 4.30）→ **非重磅日，无 S 级**；4 篇达线者按校准关记 A（同 10-24 EgoHand / 10-27 WFM / 11-07 XM4D 先例）。
- OUTDATED/SUPERSEDED **0 篇**。

## 产物（第 7-8 步）
- 报告 2 份（主批 + backfill）+ 原子笔记 18 篇（grade≥B 全覆盖，无 C 级）+ MOC 2 份 + 总索引刷新 + 7 维表/scored/run_log 各 2 套。
- registry 831 → **849**（+14 +4；备份 `papers/library/registry.jsonl.bak-20261110`；按 base_id 幂等）。
- 门③ 现算值供下一批参考：**4.399**（本批 4.37/4.34/4.23/4.23 入窗后会微降）。
