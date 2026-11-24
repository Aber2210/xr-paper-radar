# 运行日志 · 2026-11-25

- 02:30 起跑；跑前查 C: 盘剩余空间（未触发磁盘保护）。收尾实测 C: 11.71 GB / D: 222.75 GB。
- 第 1 步 对账：`scripts/audit_listing_1125.py`（PREV_DAY=11-23 / NEW_DAYS=11-24,11-25 / 窗口下界 2026-11-23），7/7 分类成功、exit 0；2026-11-24 组 **1,285 槽位 / 1,045 唯一**；11-25 组 declared=None（未释放）；11-23 组复采 declared=got（171/5/13/4/89/214/10）。
- 第 2 步 数据源：API 双主机探针 200（仅用于提交日核验）；RSS 7/7、**1,547 条**，WROTE=1547 OK_CATS=7/7。listing 1,045/1,045 覆盖 → 免 id_list。
- 第 3 步 甄别：`triage_1125.py`（数据源 `_all_full.jsonl` 1547 条 no-filter 全量，只取 day=11-24 的 newday）→ 覆盖率 1.0000（1045/1045）、KW 100 + TITLE_EXTRA 46 = 池 146 → `triage_decide_1125.py` 逐篇判读剔 84 → 62。
- 第 3 步补充 backfill：502 条 `replace` 条目中未入馆且摘要级 XR 命中 35 篇，逐篇核摘要取 6 篇。
- 第 3.5 步 残差：`residual_scan.py dump/ingest` → 5 批（4×190 + 139）并行盲评，扫描 **899**、判 **22**（**2.45%**）、采纳 **6** → 主批 68。踩坑：ingest 的 rate 分母是 `verdicts.jsonl` **行数**而非 nonxr 总数，先把 899 条逐条写入（命中写 `verdict=1`、其余写 `verdict=0`）才得到 2.45%；若只写命中行，分母会退化成 22 而得 100%。
- 第 4 步 全文：74 篇串行 3 s/篇 → **72 L0/FULL + 2 L1/PARTIAL**（2611.29647 5,105 字符、2611.30012 4,581 字符，ar5iv 仅返回摘要落地页，手动改判 PARTIAL 并同步 `.txt` 头）；字符 4,581–312,858。
- 第 4 步补充 提交日核验：`check_published_1125.py`（25 id/批 + 12 s 间隔）→ 74/74 全齐；主批 11-23×29 / 11-21×17 / 11-22×14 / 11-20×1 / 11-16×1 / 09-18×1 / 11-19×1 / 11-17×1 / 11-18×1 / 11-04×1 / 10-05×1。踩坑：`_ids_1125_clean.txt` 是换行分隔（上批为逗号分隔），派生脚本的读取方式需改为 `.read().split()`。
- 第 5 步 评分：6 组子代理 digest（13/13/13/13/13/9 = 74）+ 主会话按标准权重重算 74 篇；评分要点取自 `build_scored_1125.py` 行内注释，Top10 逐维理由落 `papers/daily/2026-11-25/scored.md`。
- 第 6 步 三关：门① 0.263（2611.28802 vs arXiv:2609.23436）；门② 6 赛道（未重筛）；门③ 4.21 vs 4.432，margin -0.222 → heavy_day_raw=false、blockbuster=false、s_awarded=false。
- 第 7 步 Top10：实数 10 篇（4.21–3.92），全部 A；全批 A 46 / B 26 / C 2，0 S。
- 第 8 步 产物：报告 2 + 笔记 72（C 级 2 篇不写）+ MOC 2 + 总索引刷新 + 7dim-table（主批/backfill 各 1）+ scored.md + run_log；registry 1,132 → **1,206**（备份 `papers/library/registry.jsonl.bak-20261125`）。易错点：`7dim-table.md` 表头必须保留 `arXiv` 列，否则前端批次卡表内计数为 0。
- 第 9 步 发布：见下方发布记录（构建 → `node --check` → CDP 冒烟 → `check_release` → 提交 → 推送 → Pages 核验）。
