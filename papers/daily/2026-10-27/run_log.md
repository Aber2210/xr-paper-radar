# 2026-10-27 执行日志

## 数据源与对账（第 1-3 步）
- **漏网对账（先于拉取）**：`scripts/audit_gap_listing.py`（TARGET_LO=2026-10-23，上一批次公告日）7 分类采集。listing 最新公告日 = **2026-10-26**（周一，周末积压公告 00:00 UTC=08:00 北京时间已释放）；10-24/10-25 周末无公告日段。10-23 组 411 篇（上批 10-26 已全量复核 0 漏网，本次复采一致）；**10-26 组 358 篇全部未入馆**（新公告批次）。
- **摘要级 XR 过滤**：`scripts/filter_missed_xr_abstract.py`（MIN_DAY=2026-10-26）→ 358 篇取回 358 条 API 元数据，XR 命中 **18 篇**（全 2610.* 新提交）。
- **RSS 主渠道交叉验证**：`scripts/fetch_rss.py` 7 分类全量去重 581 条 → KW 命中 30 条 = **18 篇 2610.* 真新提交（与 listing 命中集合逐篇一致）+ 8 篇旧稿 replace/cross 再公告 + 4 篇库内 v2 再公告**。两渠道互证无矛盾。
- **API 探针**：export.arxiv.org / arxiv.org/api/query 均可达（200）；`submittedDate` 前沿停滞 10-22，真实新增由 RSS+listing 双渠道获得。

## 甄别（第 3 步）
- 主批 XR 核心/强相关 **7 篇**入评分池；剔非 XR **11 篇**（机器人演示分割/机器人 VLA 策略/航空 GNSS-IMU 完整性/光子逆设计/脑 CT-MR 合成/机器人超声/自动驾驶分割/MLLM 视觉 token/无人机 VLN/机器人 OCT/灵巧手数据采集）。
- 旧稿 replace/cross 再公告 8 篇 → **backfill-1027**（首次入馆，单独编号，绝不混入当日新论文）。
- 库内 v2 再公告 4 篇剔除（2601.14895/2610.27712/2610.28402/2610.29014）。

## 全文抓取（第 4 步）
- 15 篇候选（主批 7 + backfill 8）跑 `scripts/fetch_fulltext.py`，严格串行 3s/篇：**14 篇 L0/FULL**（45,727–126,513 字符）+ **1 篇 L1/PARTIAL**（2610.32232 Virtual Placebo：ar5iv 仅返回摘要页、无 Methods/Results 正文章节 → 改判 PARTIAL，按摘要级评估并显式声明，禁止脑补）。无限流/降级/伪造。
- manifest 合并写入校验通过；WROTE=15>0。

## 评分与三关（第 5-6 步）
- 先抓全文再定稿。7 维加权定稿：主批 4 A / 3 B（最高 3.85 PixGR/HEALPix 并列）；backfill 4 A / 4 B（最高 4.27 World from Motion）。
- 门① 最大 Jaccard **0.065**（AudioLift vs 2610.19290 Kandinsky S2V 1.0；<0.62，无非质同源）。
- 门② 主批覆盖 **6 赛道**；backfill 覆盖 **6 赛道**（均 ≥5）。
- 门③ 当日最高 **4.27（backfill WFM）/ 3.85（主批）< 库内近 30 天 Top10 均分 4.416**（窗口 2026-09-27~10-27、421 条入窗、现算）→ **非重磅日、无 S 级**；WFM 4.27 达 S 线按校准关记 A（同 10-24 EgoHand 先例）。三关全过，**未触发重筛**。
- OUTDATED/SUPERSEDED **0 篇**。路线级观察：① 生成式中间表示进入化身/4D 重建主线（AudioLift/WFM）；② 前馈 3DGS 重建的生成式解码变体（PixGR）与 budgeted 压缩线并行；③ 晕动症/眼动仪评估两个「研究基础设施」方向同日出现（32019/32915）。

## 产物（第 7-8 步）
- 报告 2 份（主报告 + backfill 报告）+ 原子笔记 15 篇 + MOC 2 份 + 总索引刷新 + 7 维表/scored/run_log 各 2 套。
- registry 618 → **633**（+7 主批 +8 backfill；备份 `papers/library/registry.jsonl.bak-20261027`；按 base_id 幂等）。
