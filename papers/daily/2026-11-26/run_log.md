# 运行日志 · 2026-11-26

- 02:30 起跑；跑前查 C: 盘剩余空间（未触发磁盘保护）。收尾实测 C: 11.42 GB / D: 212.71 GB。
- 第 1 步 对账：`scripts/audit_listing_1126.py`（PREV_DAY=11-24 / NEW_DAYS=11-25,11-26），7/7 分类成功、exit 0；2026-11-25 组 **761 槽位 / 624 唯一**；11-26 组 declared=None（未释放）；11-24 组复采 declared=got（494/13/61/18/191/485/23）。
- 第 1 步补充 上一组复采：`scripts/missed_xr_1126.py` → 未入馆 **977** 篇、摘要覆盖 **977/977 = 1.0000**、命中 **84** 篇全部落在上批处置集合 → **0 漏网**。
- 第 2 步 数据源：API 双主机探针 200（仅用于提交日核验）；RSS 7/7、**921 条**，WROTE=921 OK_CATS=7/7；listing 624/624 覆盖 → 免 id_list。
- 第 3 步 甄别：`triage_1126.py`（数据源 `2026-11-26_all.jsonl` 921 条 no-filter，只取 day=11-25 的 newday）→ 覆盖率 1.0000（624/624）、KW 61 + TITLE_EXTRA 36 = 池 97 → 逐篇核摘要剔 53 → 44。
- 第 3 步补充 backfill：20 条 `replace` XR 命中，逐篇核摘要取 8 篇（首发 2025-08-24 ~ 2026-10-08）。
- 第 3.5 步 残差：`residual_scan.py dump/ingest` → 扫描 **527**、判 **8**（**1.52%**）、采纳 **8**；另通读补入 3 篇（2611.31757 / 2611.32034 / 2611.32396，未被自动 flagged）→ 主批 55。
- 第 4 步 全文：63 篇串行 3 s/篇 → **63 L0/FULL**（O-12 守卫已入库，本批最小 24,073 字符未触发降级）；字符 24,073–242,491。
- 第 4 步补充 提交日核验：`check_published_1126.py` → 63/63 全齐；主批 11-24×50 / 11-23×5。
- 第 5 步 评分：8 组子代理 digest（9/8/8/9/11/9/8/1 = 63）+ 主会话按标准权重重算；主会话校准三处：MoGe-4D TRL 4→3、AirLeg TRL 5→4 并删除正文查不到的「38 ms 端到端」表述、Xtream PER 5→4；Top10 逐维理由落 `papers/daily/2026-11-26/scored.md`。
- 第 6 步 三关：门① 0.192（2610.11810 vs arXiv:2611.29112）；门② 5 赛道（未重筛）；门③ 4.57 vs 4.432，margin +0.138 → heavy_day_raw=true、blockbuster=true、s_awarded=true。
- 第 7 步 Top10：实数 10 篇（4.57–3.85），3 S / 7 A；全批 S 3 / A 24 / B 29 / C 7。
- 第 8 步 产物：报告 2 + 笔记 56（C 级 7 篇不写）+ MOC 2 + 总索引刷新 + 7dim-table（主批/backfill 各 1）+ scored.md + run_log；registry 1,206 → **1,269**（+63，备份 `registry.jsonl.bak-20261126`）。易错点：`7dim-table.md` 表头必须保留 `arXiv` 列，否则前端批次卡表内计数为 0。
- 第 9 步 发布：见下方发布记录（构建 → `node --check` → CDP 冒烟 → `check_release` → 提交 → 推送 → Pages 核验）。

## 发布记录（第 9 步）

  - 构建：`python scripts/build_frontend.py` → **`verified: {'papers': 1269, 'notes': 896, 'batches': 81}`**，与磁盘一致；`BATCH_LABELS` 补 `2026-11-26` 与 `backfill-1126` 两条中文标签。
  - 语法：抽出 2 个 `<script>` 块（4,445,820 / 33,328 字符）逐个 `node --check` → 均 OK。
  - 冒烟：`node scripts/smoke_hub.mjs` → **SMOKE: PASS**（papers/notes/batches 与磁盘一致、lastThree = 11-26/11-25/11-24、五标签渲染 4/2/2/3/1、排序 8 项单调性、隐藏与弹窗交互、`PAGE_ERRORS: none`、81 张批次卡）。
  - 发布门：`python scripts/check_release.py` → G1 PASS（1269/896/81 == DATA）、G2 PASS（`gates_1126` 门③ 四字段齐 + `window_excludes_*`）、G3 PASS（本批授予 S=True 且 blockbuster 自洽、backfill 记 S=0、泄漏 0）、R OK（527 判 8 = 1.5%）→ **VERDICT: PASS**。
  - 渠道① **不可用**：本会话 ToolSearch 无 `workbuddy_sites_deploy`；`https://xr-paper-hub.app.workbuddy.host/` 与 `/index.html` 实测均 **403 / 3,174 bytes** → 按口径写「**渠道① 不可用（累计第 37 批挂账）**」，**未声称已发布**。
  - 渠道② 成功：commit `3779e92` → `python scripts/push_to_github.py --incremental`（变更/新增 **112**、删除 0、未变 2,349）→ main **`7c5829c0`**；`gh run list` 首次 run **45682436410 failure**（`No artifacts named "github-pages"`：Upload artifact 步骤 success 但 deploy 读不到产物，属 Actions 侧瞬时问题），`gh run rerun` 后 **success**。
  - 线上核验：`https://aber2210.github.io/xr-paper-radar/` → **HTTP 200 / 7,018,738 bytes**、含 `const DATA`；LF 归一化 md5 **`b88af674cce7deaa335707dc52c85ea6`** 与本地 `web/xr-paper-hub.html` **完全一致（MATCH）**。
  - **收尾文档提交 `184d2b10` 的部署未成功（平台侧）**：run `45682922667`（push）首跑与 `gh run rerun` **均 failure**，手动 `workflow_dispatch` 的 run `45683161976` 仍 failure，报错同一条 `Found 0 artifact(s)`。日志可证产物其实已生成：`Upload artifact` → 「Artifact github-pages.zip successfully finalized. Artifact ID 15054012962 / 4,558,066 bytes」，但 `deploy-pages` 调 artifacts 列表返回 0 条 → 属 **GitHub Actions/Pages 侧 incident**，非仓库或产物问题。该提交只含 `STATUS.md` / 报告 / run_log（`web/` 无变更），页面内容与已部署版本完全一致，对外交付不受影响。
  - 复查 O-13：`No artifacts` **不再局限于 `schedule` 触发**——本批 push 首跑（1/2 次）与 `workflow_dispatch` 均复现；已把 `STATUS.md` O-13 扩注为「push/手动亦会复现，届时先 rerun，连续两次同错则等平台恢复」。
  - **平台恢复后最终提交已部署成功**：把上述 incident 与 O-13 扩注写入文档后提交 `97867606` 并推送，`deploy-pages.yml` run `45683331850` → **success**；线上复验 **HTTP 200 / 7,018,738 bytes**、md5 仍为 `b88af674cce7deaa335707dc52c85ea6`（与本地逐字节相等），页面已含 `2026-11-26` 批次卡。
