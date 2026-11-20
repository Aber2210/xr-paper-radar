# 运行日志 · 2026-11-21

- 02:30 起跑；C: 盘 5.92 GB / D: 246.77 GB，未触发磁盘保护。
- 第 1 步 对账：`scripts/audit_listing_1121.py`（PREV_DAY=11-19 / NEW_DAYS=11-20,11-21），7/7 分类成功，exit 0；11-20 组 605 槽位 / 508 唯一；11-19 组 599 槽位 / 502 唯一、declared=got。
- 第 2 步 数据源：API 双主机探针 200（仅用于提交日核验）；RSS 7/7、783 条，WROTE=783。
- 第 3 步 甄别：`triage_1121.py` → KW 47 + TITLE_EXTRA 30 = 77 → `finalize_pool_1121.py` 逐篇判读剔 43 → 34。
- 第 3.5 步 残差：`residual_scan.py dump/ingest` → 扫描 431、判 7（1.6%）、采纳 3 → 主批 37。
- 第 4 步 全文：39 篇（37+2）串行 3 s/篇，全部 L0/FULL；字符 33,057–196,730。
- 第 5 步 评分：8 组子代理 digest（5/5/5/5/5/5/5/4 篇）+ 主会话按标准权重重算；校准 3 处（SGAR IMP/NOV、VideoRNG IMP）+ 赛道修正 2 处。
- 第 6 步 三关：门① 0.238；门② 5 赛道（一次重筛）；门③ 4.43 vs 4.4230，margin +0.007 → 险过，无 S。
- 第 7 步 Top10：实数 10 篇（4.43–4.00），全部 A；C 级 1 篇（2611.25934 AGSR 2.78）仅入馆不解读。
- 第 8 步 产物：报告 2 + 笔记 38 + MOC 2 + 总索引 + 7 维/scored/run_log；registry 1,043 → 1,082（备份 `registry.jsonl.bak-20261121`）。
- 第 9 步 发布：见下方发布记录（构建 → 冒烟 → check_release → 提交 → 推送 → Pages 核验）。

## 发布记录（第 9 步）

- **前端重建**：`build_frontend.py` → `verified: {'papers': 1082, 'notes': 718, 'batches': 73}`；批次卡 `2026-11-21` 表内=37（23A/13B/1C，max 4.43）、`backfill-1121` 表内=2（1A/1B，max 4.08）；两个 `<script>` 块 `node --check` 通过。
- **冒烟**：`node scripts/smoke_hub.mjs` → **PASS**（磁盘不变量 papers/notes/batches 全等；lastThree 首卡 2026-11-21；排序 8 项断言、隐藏开关、弹层全绿；PAGE_ERRORS none）。
- **发布前自检**：`check_release.py` → **PASS**（G1 1082/718/73 ｜ G2 `gates_1121.json` 无缺、险过四字段齐 ｜ G3 本批授予S=False、泄漏 0 ｜ R 残差 1.6%）；`--record` 已写入 `data/verdicts.jsonl`；`check_audit_guard.py` PASS（24 份：守卫 6 / 豁免 18 / 违规 0）。
- **渠道①**：`xr-paper-hub.app.workbuddy.host` 仍 403，**渠道①不可用（累计第 32 批挂账）**，本批未发布。
- **渠道②（GitHub Pages）**：commit `82a2222` → `push_to_github.py --incremental` 增量 **96 文件**（56.72 MB 全量树中未变 1992）→ main **`4fd76fe8`**；deploy run **44798357045** success；`https://aber2210.github.io/xr-paper-radar/` **HTTP 200 / 5,613,320 bytes**，含 `const DATA`，**md5 `16dd0617c6a87a29074a285adc33f26f` 与本地 LF 归一化版逐字节相等**；线上含 `2026-11-21` ×425 / `backfill-1121` ×14 / `AnyVIO` ×8。
- **两次仅文档的后续推送**：`6022ae7`（run_log/STATUS/报告渠道①口径）→ main `c3baf0a1`，deploy `44798650783` success；`d4be314e`（`data/missed_xr.json` 补记三批零漏网）→ deploy `44798863138` success。两次均未改 HTML，线上 md5 保持 `16dd0617c6a87a29074a285adc33f26f` 不变（复验 HTTP 200 / 5,613,320 bytes）。
> **SHA 对照说明**：`push_to_github.py` 走 Git Data API 重建提交，**本地 commit SHA 与远端不同**（tree 相同）。本批映射：本地 `82a2222`/`6022ae7`/`f8b7df9`/`6eadcb9` → 远端 `4fd76fe8`/`c3baf0a1`/`d4be314e`/`9d2486ba`。核对内容一致性看远端 tree 或线上 md5，不要用本地 SHA 去远端找。
