# 运行日志 · 2026-11-27

- 02:30 起跑；跑前查 C: 盘剩余空间（未触发磁盘保护）。收尾实测 C: 11.20 GB / D: 211.98 GB。
- 第 1 步 对账：`scripts/audit_listing_1127.py`（PREV_DAY=11-25 / NEW_DAYS=11-26,11-27），7/7 分类成功、exit 0；2026-11-26 组 **695 槽位 / 569 唯一**；11-27 组 declared=None（未释放）；11-25 组复采 declared=got（cs.CV 302/302 含 skip=500 补 90、cs.AI 300/300 含补 48）。
- 第 1 步补充 上一组复采：`scripts/missed_xr_1127.py` → 未入馆 **569** 篇、摘要覆盖 **569/569 = 1.0000**、命中 **53** 篇全部落在上批处置集合 → **0 漏网**。
- 第 2 步 数据源：API 双主机探针 200（仅用于提交日核验）；RSS 7/7、**849 条**，WROTE=849 OK_CATS=7/7；listing 569/569 覆盖 → 免 id_list。
- 第 3 步 甄别：`triage_1127.py`（数据源 `2026-11-27.jsonl` 849 条 no-filter，只取 day=11-26 的 newday）→ 覆盖率 1.0000（569/569）、KW 67 + TITLE_EXTRA 25 = 池 92 → 逐篇核摘要剔 49 → 43；另 26 条 `replace` XR 命中逐篇核摘要取 8 篇。
- 第 3 步修正：`2611.30173`（Confidently Lost）在池中且 `in_registry=true`（11-25 批 3.71），初版定稿误将其纳入主批；按「库内 cross/v2 再公告不重复入馆」移入 REJECT，主批 44→43、全量 64→63，并重跑 build_scored / gates（否则门① 会与**自身**比对、虚高且无效）。
- 第 3.5 步 残差：`residual_scan.py dump/ingest` → 扫描 **525**、判 **30**（**5.71%**）、采纳 **12**；采纳篇全部另跑全文抓取（11 FULL + 1 PARTIAL）→ 主批 55。
- 第 4 步 全文：63 篇串行 3 s/篇 → **FULL 62 / PARTIAL 1**；字符 4,551–209,939。2611.33313 的 ar5iv 返回摘要落地页（4,551 字符）被 LANDING_RE 守卫判 PARTIAL，按摘要级证据降档。
- 第 4 步补充 提交日核验：`check_published_1127.py`（25 个 id/批 × 12 s 间隔）→ 64/64 全齐；主批 11-25×47 / 11-24×8。
- 第 5 步 评分：8 组子代理 digest（各 8 篇 = 64）+ 主会话按标准权重重算；主会话校准一处：2611.33313 TEC 2 / EXP 2（PARTIAL 摘要页，无量化对比）。Top10 逐维理由落 `papers/daily/2026-11-27/scored.md`（取自 digest `scores_why`）。
- 第 6 步 三关：门① 0.127（2611.34810 vs arXiv:2609.22941）；门② 纯值 4 赛道 → 回补 1 次 → 5 赛道；门③ 4.35 vs 4.459，margin -0.109 → heavy_day_raw=false、blockbuster=false、s_awarded=false。
- 第 7 步 Top10：实数 10 篇（4.35–4.00），全 A；全批 S 0 / A 44 / B 14 / C 5。
- 第 8 步 产物：报告 2 + 笔记 58（C 级 5 篇不写）+ MOC 2 + 总索引刷新 + 7dim-table（主批/backfill 各 1）+ scored.md + run_log；registry 1,269 → **1,332**（+63，备份 `registry.jsonl.bak-20261127`）。易错点：`7dim-table.md` 表头必须保留 `arXiv` 列，否则前端批次卡表内计数为 0。
- 第 9 步 发布：`check_release.py` PASS（--record 共 9 批）→ 前端重建（1332/954/83）→ 内联脚本 `node --check` 通过 → CDP 冒烟 PASS → `git add -A && git commit`（本地 `4d5fa2e`）→ `push_to_github.py --incremental`（127 变更 / 2,456 未变 / 删除 0）→ 远端 main `3d8cec6c` → deploy run `45882725875` success → 线上 HTTP 200、4,840,812 字符、含 `const DATA` 与 `2026-11-27`，与本地逐字节相等。**渠道① `workbuddy_sites_deploy` 本会话不可用 → 累计第 38 批挂账（未声称已发布）。**
