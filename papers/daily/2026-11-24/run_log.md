# 运行日志 · 2026-11-24

- 02:30 起跑；跑前查 C: 盘剩余空间（未触发磁盘保护）。收尾实测 C: 12.85 GB / D: 242.22 GB。
- 第 1 步 对账：`scripts/audit_listing_1124.py`（PREV_DAY=11-20 / NEW_DAYS=11-21..11-24），7/7 分类成功，exit 0；11-23 组 506 槽位 / 404 唯一；11-21、11-22 declared=None（周末 skipDays）；11-20 组复采 605 槽位 / 508 唯一、declared=got。
- 第 2 步 数据源：API 双主机探针 200（仅用于提交日核验）；RSS 7/7、639 条，WROTE=639。listing 404/404 覆盖 → 免 id_list。
- 第 3 步 甄别：`triage_1124.py` → KW + TITLE_EXTRA 共 75 → `build_cand_1124.py` 逐篇判读剔 42 → 33（主批）+ 9（backfill）。
- 第 3.5 步 残差：`residual_scan.py dump/ingest` → 扫描 371、判 8（2.2%）、采纳 8 → 主批 41。踩坑：首版 `verdicts.jsonl` 只写 14 行（8 采纳 + 6 拒绝），ingest 分母取判定行数得 57.1%；补齐 371 行后得 2.2%。
- 第 4 步 全文：50 篇（41+9）串行 3 s/篇，49 L0/FULL + 1 L1/PARTIAL（2611.27633：arXiv HTML v1 404、ar5iv 仅摘要落地页，手动改判 PARTIAL）；字符 4,993–140,986（FULL 篇最小 25,942）。
- 第 4 步补充 提交日核验：`check_published_1124.py`（id_list 50/批 + 12 s 间隔）→ 50/50 全齐；主批 11-20×34 / 11-19×7。踩坑：`_ids_1124.txt` 首行混入计数数字 42，改用正则过滤后的 `_ids_1124_clean.txt`。
- 第 5 步 评分：4 组子代理 digest（11/11/11/17 篇）+ 主会话按标准权重重算 50 篇；评分理由落 `data/why_1124.json`，并由脚本正则校验 50 条 `X=n` 与评分表逐维一致（0 处不一致）。
- 第 6 步 三关：门① 0.40（2609.31248 vs 库内 2611.02044）；门② 7 赛道（未重筛）；门③ 4.27 vs 4.432，margin −0.162 → heavy_day_raw=false，blockbuster=false，无 S。
- 第 7 步 Top10：实数 10 篇（4.27–3.92），全部 A；本批无 C 级（入池门槛已把 C 级挡在候选外）。
- 第 8 步 产物：报告 2 + 笔记 50 + MOC 2 + 总索引 + 7dim-table（主批/backfill 各 1）+ scored.md + run_log；registry 1,082 → 1,132（备份 `registry.jsonl.bak-20261124`）。易错点：`7dim-table.md` 表头必须保留 `arXiv` 列，否则前端批次卡表内计数为 0。
- 第 9 步 发布：`build_frontend.py` → `verified {papers: 1132, notes: 768, batches: 77}`（5,808.8 KB）；`smoke_hub.mjs` CDP 冒烟 **SMOKE: PASS**（papersEqDisk / notesEqDisk / batchesEqDisk / uiSorts / uiHide / uiPop 全 true，PAGE_ERRORS none，77 张卡）；`check_release.py` **VERDICT: PASS**（G1 1132/768/77、G2 险过四字段齐、G3 无 S 泄漏、R 残差 2.2%）；渠道① `workbuddy_sites_deploy` 不在工具集 → 不可用（累计第 35 批挂账，含状态日）；渠道② 本地 commit `f0774fa` → **增量推送**（101 变更 / 2119 未变 / 60.37 MB）→ main `67868a4b` → Deploy Pages run `45244161325` **success** → 线上 HTTP 200、含 `const DATA`、md5 `0705fad6…` 与本地 LF 归一化版逐字节相等。
