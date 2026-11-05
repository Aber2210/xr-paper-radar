# 2026-11-06 执行日志

## 数据源与对账（第 1-3 步）
- **漏网对账（先于拉取）**：`scripts/audit_listing_1106.py`（TARGET_DAY=2026-11-04，上批公告日；show=500 单页×7 分类）→ 7 分类最新公告日均为 **2026-11-05**（无漏跑公告日）；**11-04 组逐分类 declared=got**（CV 160/GR 2/HC 21/MM 5/RO 72/AI 252/IV 13，525 槽位）→ 未入馆 **441 篇**，`scripts/run_filter_1106.py` 摘要级复核 **13 篇命中均为 11-05 运行已剔非 XR（与上批 13 篇剔除清单逐篇一致）→ 0 漏网、无 backfill**。
- **摘要级 XR 过滤（新公告组）**：11-05 组 **398 篇唯一论文**（CV 148/GR 7/HC 29/MM 6/RO 62/AI 217/IV 8，477 槽位）→ 摘要级 XR 命中 **22 篇**（`data/missed_xr_abstract_1106.json`，meta fetched 839/839 两组合计）。
- **RSS 主渠道交叉验证**：`scripts/fetch_rss.py` 7 分类全量去重 **647** 条 → KW 命中 **37** = **22 篇 11-05 公告组真新提交（12 篇 XR + 10 篇非 XR）+ 8 篇旧稿 replace/cross 再公告（6 篇 XR → backfill-1106 + 2 篇非 XR 剔除）+ 7 篇库内 v2 再公告（剔除）**。listing 摘要级 22 篇**全部被 RSS 覆盖，RSS 漏网 0 篇**——两渠道互证（`scripts/triage_1106.py` 双向差集 0）。
- **API 探针**：双主机 200；`id_list` 口径核验提交日：主批 **11 篇 2026-11-04 提交 + 1 篇（2611.05593）2026-11-03 提交**（均早于公告日 11-05）。RSS published 字段为公告时间戳（11-05），非提交日，两口径已区分。

## 甄别（第 3 步）
- 主批 XR 核心/强相关 **12 篇**入评分池；剔非 XR **10 篇**（2611.05542 全页广告排序 / 2611.05569 LiDAR 点云分割不确定性 / 2611.05667 PHIL 机器人策略主动干预 / 2611.05741 OUCH 医疗触觉刺激装置 / 2611.05874 Feature Puzzles 多视图三维分割 / 2611.05897 FWIK 机器人逆运动学 / 2611.05936 LumiTac 机器人触觉传感器 / 2611.06068 Fluidic Body 群体机器人有形界面 / 2611.06442 TwinBridge 数字孪生机器人 RL / 2611.06838 上下文感知自回归图像生成）。
- 旧稿 replace/cross 再公告 8 篇中 **6 篇 XR → backfill-1106**（首次入馆，单独编号）；2 篇非 XR 剔除（2608.15968 低成本 4-DoF 机械臂 / 2611.05163 RoboTryOn 机器人演示合成）。
- 库内 v2 再公告 7 篇剔除（2611.05176 MM-AR / 2606.29494 VCS-SLAM / 2610.20590 Feed-Forward MV Feature Coding / 2610.28631 AEON / 2611.03114 3DGS 自学习神经视图相关颜色 / 2611.05359 GSCV++ / 2610.39076 Tactus）。

## 全文抓取（第 4 步）
- 18 篇候选（主批 12 + backfill 6）跑 `scripts/fetch_fulltext.py`，严格串行 3s/篇（约 1 分钟）：**18 篇全部 L0/FULL**（21,776–178,380 字符）。无限流/降级/伪造。
- **人工复核正文中段章节**（防 11-05 ar5iv 摘要页误判教训）：18 篇均含 Method/Experiments/Results/Conclusion 等实质章节，manifest FULL 判定全部确认。
- manifest 合并写入校验通过；WROTE=18>0。

## 评分与三关（第 5-6 步）
- 先抓全文再定稿。7 维加权定稿：主批 **1 S / 5 A / 6 B**（最高 4.57 Open-HumanScale）；backfill **5 A / 1 B**（最高 EgoM2P 4.10）。
- 门① 最大 Jaccard **0.167**（2611.06593 BudgetSplat vs 库内 2610.20590；<0.62，非同质）。
- 门② 纯价值 Top10 覆盖 **4 赛道**（感知与认知×2 / 重建与SLAM×3 / 交互与输入×1 / 神经渲染×4）<5 → **触发一次重筛**：剔除神经渲染赛道最低分 BudgetSplat 3.51，回补未覆盖核心赛道（空间计算与UI）B 级池最高分 VR HIIT 3.18 → 定稿 Top10 覆盖 **5 赛道** ≥5，通过（BudgetSplat 仍入馆写 B 级笔记，仅不占 Top10 名额，同 11-04 SHield 先例）。
- 门③ 当日最高 **4.57 ≥ 库内近 30 天 Top10 均分 4.363**（窗口 2026-10-07~11-06、428 条入窗、现算）→ **重磅日，可评 S 级；全批 1 篇 S（Open-HumanScale 4.57），按实数定级未拔高**。
- OUTDATED/SUPERSEDED **0 篇**。路线级观察：① 前馈 3DGS 效率线三篇同批——CrossPressor（fusion 侧 26×）、BudgetSplat（表示侧预算控制）、GaussianRenderFormer（渲染侧无光栅化探索），与库内 ZPressor/pixelSplat/MVSplat 主线构成「表示-融合-渲染」全链路优化图景；② 第一人称数据链闭环——backfill EgoGen（合成）→ EgoM2P（统一预训练）→ Open-HumanScale（50k 小时开放缩放配方）三篇同批互证，AR 眼镜数据基础设施日趋完整；③ 度量尺度与 AR 落地——METRIC-GS（从重建自身读尺度+弃权路由）与 PVLC 投影 AR（8ms 低延迟三维定位）从内容放置与空间配准两端补 AR 工程实证；④ 硬件类缺口仍仅 CVQPG + HoOPOE 两篇涉及近眼显示光学（本批无波导/可变焦/Maxwellian/光场新文献）。

## 产物（第 7-8 步）
- 报告 2 份（主报告 + backfill 报告）+ 原子笔记 18 篇（grade≥B：主批 12 + backfill 6，无 C 级）+ MOC 2 份 + 总索引刷新 + 7 维表/scored/run_log 各 2 套。
- registry 790 → **808**（+12 主批 +6 backfill；备份 `papers/library/registry.jsonl.bak-20261106`；按 base_id 幂等）。
