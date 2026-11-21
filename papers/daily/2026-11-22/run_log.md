# 运行日志 · 2026-11-22（周日 02:30 · 周末状态日：0 新稿）

## 0. 结论速览

| 项 | 结果 |
|---|---|
| 运行性质 | **周末状态日**（`skipDays` 无 11-21 / 11-22 公告组），0 新稿、0 漏网、无 backfill |
| 最新公告日 | **2026-11-20（周五）**（已由 11-21 运行完整处理） |
| registry | **1,082 条**（S18 / A526 / B408 / C130），无变更、无备份需要 |
| 笔记 / daily / MOC | **718 / 73 / 62** |
| 门③ 现算参考 | **4.432**（窗口 2026-10-23 ~ 2026-11-22，**485 条入窗**） |
| 残差复核 | **不适用**（状态日无 `data/nonxr_1122.json`；沿用 11-21 批 1.6%，距 12% 阈值远） |

## 1. 漏网对账（Step 1，先于拉取）

- 脚本：`scripts/audit_listing_1122.py`（PREV_DAY=2026-11-20 / NEW_DAYS=2026-11-21,2026-11-22，show=500 单页×7 分类，含 `declared≠got` 自动补页 + `ok_cats<7 → exit 2` 守卫）。`check_audit_guard.py` 预检 PASS（25 份：守卫 7 / 豁免 18 / 违规 0）。
- 结果：**7/7 分类成功**（exit 0），最新公告日 **全部为 2026-11-20**，`NEW_DAYS` 两日 `declared=None / got=0` → **无 11-21 / 11-22 公告日组**。
- 11-20 组复采逐分类 **declared=got**：CS.CV 213 / GR 6 / HC 23 / MM 4 / RO 92 / AI 252 / eess.IV 15 = **605 槽位**（与 11-21 运行采集数字逐项一致），唯一论文 **508 篇**。
- 未入馆 **471 篇**（= 508 − 37 篇主批已入馆），摘要级 XR 过滤（`scripts/filter_missed_1122.py`，RSS 摘要取自 11-19 / 11-20 / 11-21 三份全量文件，**471/471 有摘要，覆盖率 1.0000**）命中 **43 篇**，**全部**落在 11-21 运行显式处置集合（`nonxr_1121 ∪ xr_pool_1121 ∪ rejected_1121 ∪ backfill_pool_1121 ∪ scored_1121`）→ **0 漏网**（`data/missed_xr_1122.json` 为空），**无 backfill**。
- 当日全量日组计数（跨分类槽位）：11-20 **605** / 11-19 599 / 11-18 215 / 11-17 246 / 11-16 65。

## 2. 数据源探测（Step 2）

| 源 | 状态 |
|---|---|
| `export.arxiv.org/api/query` | **200**（2,938 bytes 探针响应） |
| `arxiv.org/api/query` | **200** |
| cs.CV `submittedDate` 降序前沿 | **2026-11-19**（= 11-20 公告组来源，已全部入馆；无越过 11-20 组的新前沿） |
| `rss.arxiv.org` 7 分类 | HTTP 200，**全部 0 条目**，`fetch_rss.py` → `WROTE=0 OK_CATS=7/7`（exit 0：源可用、当日无条目，周末节律空源，非代理故障） |

## 3. 五源互证（状态日判定依据）

1. **listing 日期头**（7/7 分类）：newest = `Fri, 20 Nov 2026`，无 11-21 / 11-22 日组；
2. **缓存穿透**：`cs.CV/recent?cb=8801`（59,638 bytes）最新日组同为 `Fri, 20 Nov 2026`；
3. **pastweek 视图**：`cs.CV/pastweek`（59,662 bytes）同为 11-20；
4. **跨学科复核**：`math.AP/pastweek`（42,193 bytes）与 `cs.CL/pastweek`（58,925 bytes）最新日组同为 `Fri, 20 Nov 2026` → 排除本分类 / 本机故障；
5. **API + RSS**：API 双主机 200、前沿 11-19（不越过 11-20 组）；RSS 7/7 空源。

时序口径：arXiv `skipDays` 含周六、周日 → 11-21 / 11-22 不公告；周末提交积压将于**周一 00:00 UTC = 2026-11-23 08:00 北京时间**释放，晚于 11-23 02:30 的运行时刻，故 11-23 仍应为状态日，11-24（周二）02:30 才处理该批次（同 10-26 / 11-02 / 11-09 / 11-16 模式）。

## 4. 门③ 价值天花板基线（Step 6 参考值，非本批判定）

- 脚本：`scripts/gates_1122.py` → `data/gates_1122.json`（`run_type=status_day_weekend_no_announcement`）。
- 半开窗口 **[2026-10-23, 2026-11-22)**，**485 条入窗**，库内近 30 天 Top10 均分 **4.432**。
- 今日无候选 → `today_max=null`、`heavy_day_raw=false`、`blockbuster=false`、`s_awarded=false`（不授予 S）；`window_excludes_today` / `window_excludes_this_run_batches` / `this_run_batches_excluded` 三项留痕齐备。
- 均分较上批 4.4230 **升 0.009**：11-21 批 AnyVIO 4.43 与 11-18 批 4.43 / 4.37 均已入窗，同期 2610.23772（4.57）仍在窗内（10-23 起算）。**门③ 随窗口滑动变化，下一批务必现算。**
- 库内 Top10（现算）：2611.06817 4.57 S · 2611.11169 4.57 S · 2603.01178 4.50 A · 2611.21143 4.43 A · 2611.26625 4.43 A · 2610.39399 4.37 A · 2611.09458 4.37 A · 2611.21479 4.37 A · 2611.07902 4.36 A · 2610.34263 4.35 A。

## 5. 残差复核（Step 3.5）

- 状态日**无新增 nonxr 集合**（未拉取、未甄别），故 `data/residual_1122.json` 不生成，`residual_scan.py` 未执行。
- 如实登记：连续两批 rate = 2.8%（11-20）→ 1.6%（11-21），**距 12% 上报阈值远**；本日空跑，不计入连续超标计数。
- `check_release.py` 的 R 项因缺 `residual_1122.json` 报 **WARN（未执行）**，属状态日预期，不影响发布（FAIL 级判据不涉及）。

## 6. 产物

| 产物 | 路径 |
|---|---|
| 状态报告 | `reports/XR-Daily-Report-2026-11-22.md` |
| 前沿参考 7 维表（39 篇：主批 37 + backfill-1121 2，**非当日新拉取**） | `papers/daily/2026-11-22/7dim-table.md` |
| 运行日志 | `papers/daily/2026-11-22/run_log.md` |
| 对账数据 | `data/audit_1122_days.json` / `audit_1122_alldays.json` / `newday_1122.json` / `missed_prev_1122.json` / `missed_new_1122.json` / `missed_xr_1122.json` |
| 门③ 留痕 | `data/gates_1122.json` |
| 总索引 | `papers/MOC/MOC-总索引.md`（11-22 状态注记 + 速查入口 + 批次索引行 + 页脚计数） |

## 7. 发布（Step 9）

- 前端重建：`scripts/build_frontend.py`（BATCH_LABELS 补 `2026-11-22` 中文标签）→ 期望 DATA **1082 / 718 / 74**（daily 目录 73 → 74，新增本日目录）。
- `check_release.py`：G1 三计数一致 / G2 gates 留痕齐 / G3 无泄漏 S（状态日）→ 见收尾记录。
- 冒烟：`node --check` 抽块 + `scripts/smoke_hub.mjs`（磁盘不变量 + 五标签 + 排序/隐藏/弹层三组交互）。
- 渠道①（workbuddy_sites_deploy）：本会话工具集中不可用，按既定口径如实写「渠道①不可用（累计第 33 批挂账）」。
- 渠道②（GitHub Pages）：`git commit` → `scripts/push_to_github.py --incremental` → 核验 ref / Pages 200 / DATA 三计数。

## 8. 诚实口径

- 本日**未产生任何新论文、新评分或新 Top10**；前沿参考表全部为 11-21 运行已发布的 39 篇（主批 37 + backfill 2），档位与 registry 逐行一致（`assign_grade(value, batch, heavy_day=False)` 断言通过）。
- 公告日 **2026-11-20** ≠ 拉取日 **2026-11-22**；周末两日无公告属 `skipDays` 正常节律，非数据源故障。
