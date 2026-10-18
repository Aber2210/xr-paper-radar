# 运行日志 · backfill-2603-2609（旧稿补录）

- 性质：**历史旧稿 backfill**，非当日新提交。触发条件：export.arxiv.org / arxiv.org/api/query 已恢复 200（10-09 探针确认），满足「API 健康时单开 backfill 批次」待办。
- 来源：2026-10-09 RSS 落盘 `data/raw/2026-10-09_rss.jsonl` 中 7 篇 2603–2609 旧稿(replace 公告日 2026-10-08)；经 XR 相关性甄别，保留 **6 篇 XR 相关**，剔除 1 篇非 XR。
- 剔除：2605.00556（Linking Behaviour and Perception to Evaluate Meaningful Human Control over Partially Automated Driving）——属自动驾驶 HCI，非 XR/VR/AR，C 级，不纳入 XR 文献库。
- 全文：fetch_fulltext.py 7 篇（含剔除稿）**全部 L0/FULL**（arxiv.org/html，45K–155K 字符，串行 3s，无限流/降级/伪造）；6 篇 XR 入馆。
- 评分：7 维加权；3 A（ReViV/Hand-4DGS/NavSight）+ 3 B（ModPack/3DGS-Init/TAVIS）。
- 覆盖度门：门① 最大 Jaccard 0.333（通过）；门② 覆盖 5 赛道（通过）；门③ backfill 不适用。重筛触发：False。
- 同质关注 0 条（见上）。
- 文献库：368 → 374（+6，均为 BACKFILL 标记，in_top10=False）。
- 诚实口径：本批次为补录，明确标注 batch=backfill-2603-2609、orig_window=2603–2609、公告日 2026-10-08，绝不混入「当日新论文」表；原始投稿月份窗口已在笔记与索引注明。
