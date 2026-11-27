# 运行日志 · 2026-11-28（周六 · 状态日 · 11-27 周五公告组未释放）

- 02:30 起跑；跑前查磁盘：C: **11.84 GB** / D: **225.17 GB**（未触发磁盘保护）。文本产物全部写 D 盘，临时文件 `D:\Agent\.tmp`。
- 第 1 步 对账：`scripts/audit_listing_1128.py`（PREV_DAY=2026-11-26 / NEW_DAYS=2026-11-27,2026-11-28，7 分类 × show=500 单页 + `declared≠got` 自动补页）→ **7/7 分类成功、exit 0**；最新公告日**均为 2026-11-26（周四）**，槽位 **695**（CV 288 / GR 10 / HC 20 / MM 7 / RO 109 / AI 248 / IV 13，逐分类 declared=got）；`NEW_DAYS` 两日 **declared=None、got=0** → **11-27（周五）公告组未释放**。
- 第 1 步 交叉复核：`recent?cb=1128a`、`pastweek`（cs.CV）均 `Thu, 26 Nov 2026`；跨学科 `math.AP` / `cs.CL` `pastweek` 同为 11-26 → 排除分类级 / 本机故障，判定为**工作日公告跳空**（同 2026-10-29、2026-11-12 先例）。
- 第 1 步 上一组复采：重新拉取 11-26 组全量并去重 → **569 篇唯一**（`data/group_1126_1128.json`），与 11-27 运行记录的 569 逐项一致；已入馆 **56**（11-27 主批 55 全在组内 + 1 篇库内既有 cross 再公告），未入馆 **513**。
- 第 1 步 漏网复核：`scripts/filter_missed_1128.py`（摘要取自 `data/raw/2026-11-27.jsonl` 849 条 + `2026-11-28_all.jsonl` 398 条）→ 摘要覆盖 **513/513 = 1.0000**；摘要/标题级 XR 命中 **47 篇**，全部落在 11-27 处置集合（nonxr_1127 ∪ xr_pool_1127 ∪ xr_final_1127 ∪ backfill_pool_1127 ∪ scored_1127 ∪ old_replace_1127 ∪ registry）→ **0 漏网**，`data/missed_xr_1128.json` 为空，**无 backfill**。
- 第 2 步 数据源：`export.arxiv.org` 200（前沿 published `2026-11-25T18:59:59Z`）；`arxiv.org/api/query` 200（`cat:cs.CV AND submittedDate:[20261126 TO 20261128]` → **0 篇**）；RSS `fetch_rss.py --no-filter` → `WROTE=398`、`OK_CATS=7/7`，其中 6 分类 **0 条目**、cs.AI **398 条**。
- 第 2 步 RSS 判读（关键）：cs.AI 398 条 `lastBuildDate` = Fri, 27 Nov 2026 05:00 UTC、条目 `published` 全为 `2026-11-27T00:00:00Z`，**看似新公告**；与上一批 RSS（`data/raw/2026-11-27.jsonl`，849 条）做 `base_id` 集合比对 → **398 条全部在旧集合内、`cur_only=0`** → 判定为**陈旧 feed 重戳日期**，不构成新稿（同 2026-10-30 先例）。
- 第 3 步 甄别：无新稿 → 候选池为空，无 triage。
- 第 3.5 步 残差复核：无 `data/nonxr_1128.json`（状态日无新候选）→ **不适用、未执行**，不生成 `data/residual_1128.json`。
- 第 4-7 步：无候选 → 无全文抓取、无新评分、无 Top10。前沿参考沿用 11-27 批（63 篇：主批 55 + backfill 8），`scripts/build_status_table_1128.py` 复算档位并与 registry 逐行 assert 一致。
- 第 6 步 门③ 现算：`scripts/gates_1128.py` → 窗口 **[2026-10-29, 2026-11-28)**、**659 条入窗**、Top10 均分 **4.465**（上一批 4.459，+0.006）；`today_max/margin=null`、`heavy_day_raw/heavy_day/blockbuster/s_awarded` 全 false；`window_excludes_today=true`、`window_excludes_this_run_batches=true`、`this_run_batches_excluded=[]`（状态日无追加批）。
- 第 8 步 产物：状态报告 1 + 前沿参考 7 维表（63 篇）+ run_log + 对账 JSON 7 份 + `gates_1128.json` + MOC 总索引维护；registry **无变更**（1332：S21/A671/B496/C144），无需备份。
- 第 9 步 发布：`check_release.py` → 见收尾；前端重建 + 冒烟 + 渠道②推送见报告/STATUS。
