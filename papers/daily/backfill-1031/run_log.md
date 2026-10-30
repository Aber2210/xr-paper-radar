# backfill-1031 执行日志

- **批次性质**：backfill（非当日新提交）——10-30 公告批次中 RSS 混入的旧稿 replace/cross 再公告 6 篇首次入馆；原始投稿 2501=2025-01 / 2604=2026-04 / 2605=2026-05 / 2608=2026-08（arXiv ID 前缀 2501/2604/2605/2608）。
- **来源**：`scripts/fetch_rss.py` 7 分类全量去重 1,115 → KW 命中 52；其中 15 篇旧稿再公告经 XR 甄别保留 6 篇（剔非 XR 9 篇：事件相机综述/ProcObject-10K/RadLoc/EgoHTR/WNM-3D/语义通信/A4-MR/HumiMimic/Ego-CEVR）。
- **全文**：6 篇全部 L0/FULL，串行 3s/篇，无限流/降级/伪造。
- **评分**：5 A / 1 B（最高 InHabit 4.07，无 S 线）。门① 全池合并复核最大 Jaccard 0.075 < 0.62；门② 覆盖 5 赛道（6 篇低量批次实际上限）；门③ 不适用；OUTDATED 0。
- **诚实口径**：全部条目 `batch=backfill-1031` + `orig_window` 标注，绝不混入「当日新论文」。
