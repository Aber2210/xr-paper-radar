# 运行日志 · 2026-11-23（周一 02:30）· 周一凌晨状态日 · 0 新稿

## 0. 结论

- **新稿 0 篇、漏网 0 篇、backfill 无**。本日为周一时序状态日：周末提交积压于 **周一 00:00 UTC = 08:00 北京时间**公告，晚于本次运行时刻 02:30，因此 11-23 公告组此刻尚不可见（同 10-26 / 11-02 / 11-09 三次先例，本模式第 4 次验证）。
- registry 维持 **1,082**（S18 / A526 / B408 / C130）；笔记 **718**；daily **75**（本次新增目录）；MOC **62**。
- 未伪造 Top10 / 评分 / S 级；未生成 `residual_1123.json`（状态日无新增 nonxr）。

## 1. 漏网对账（Step 1，先于拉取）

| 项 | 结果 |
|---|---|
| 脚本 | `scripts/audit_listing_1123.py`（由 1122 版派生；PREV_DAY=2026-11-20，NEW_DAYS=11-21/11-22/11-23；show=500 单页 × 7 分类，`declared≠got` 自动补页） |
| 分类成功 | **7/7，exit 0**；`check_audit_guard.py` PASS（守卫在任何 `json.dump(...missed...)` 之前） |
| 最新公告日 | 全部 **2026-11-20（周五）**：cs.CV 213 / cs.GR 6 / cs.HC 23 / cs.MM 4 / cs.RO 92 / cs.AI 252 / eess.IV 15 = **605 槽位** |
| NEW_DAYS | 11-21 / 11-22 / 11-23 三日 **declared=None、got=0** → 无公告日段 |
| 11-20 组复采 | 逐分类 **declared=got**，**508 篇唯一**（与 11-21 / 11-22 两次运行逐项一致） |
| 未入馆 | **471 篇**（= 508 − 37 主批已入馆） |
| 摘要覆盖 | RSS 摘要取自 `2026-11-19_all` / `2026-11-20_all` / `2026-11-21_all` 三份全量，**471/471 有摘要，覆盖率 1.0000**（今日 RSS 为空源，未误用） |
| 摘要级 XR 命中 | **43 篇**，全部落在 11-21 运行处置集合（`nonxr_1121 ∪ xr_pool_1121 ∪ rejected_1121 ∪ backfill_pool_1121 ∪ scored_1121`） |
| 结论 | **0 漏网**，`data/missed_xr_1123.json` = `{}`，无 backfill |

## 2. 数据源探测（Step 2）与五源互证

| 源 | 结果 |
|---|---|
| `export.arxiv.org/api/query` | 200 |
| `arxiv.org/api/query` | 200 |
| cs.CV `submittedDate` 降序前 5 | 全部 2026-11-19（11-20 公告组来源，已全部入馆） |
| `cs.CV AND submittedDate:[20261121…]` / `[20261122…]` / `[20261123…]` | 各 **0 条** |
| RSS 7 分类（`scripts/fetch_rss.py --out data/raw/2026-11-23_all.jsonl`） | `WROTE=0 OK_CATS=7/7`（源可用、当日无条目，周末节律） |
| 缓存穿透 / pastweek | `recent?cb=9101` 与 `pastweek` 均 `Fri, 20 Nov 2026` |
| 跨学科 | `math.AP` / `cs.CL` `pastweek` 最新日组同为 `Fri, 20 Nov 2026` |

五源结论一致：**无新稿可处理**。

## 3. 拉取与甄别（Step 3）

不执行：无新公告组，`fetch_rss.py` 已核为空源（`WROTE=0`，非 exit 2），listing 三日区间各 0 篇。

## 4. 残差复核（Step 3.5）

不适用：状态日无 `data/nonxr_1123.json`，未生成 `data/residual_1123.json`（不为消 `check_release` 的 R 项 WARN 而补造）。
历史 rate：11-20 批 2.8%、11-21 批 1.6%，距 12% 上报阈值远。

## 5. 全文抓取 / 评分 / 三关 / Top10（Step 4–7）

均不适用（0 候选）：

- 门① 无本批集合可比；门② 无新 Top10（上一批 11-21 定稿 5 赛道）；门③ 仅现算基线。
- 门③ 现算：窗口 **[2026-10-24, 2026-11-23)**，**464 条入窗**，库内 Top10 均分 **4.432**；`today_max=null`、`margin=null`、`heavy_day_raw=false`、`blockbuster=false`、`s_awarded=false`（`data/gates_1123.json` 四项留痕 + `window_excludes_*` 齐备）。
- 数值与 11-22 相同属**巧合**：窗口已滑动（10-23 批出窗、本日无新增入窗，Top10 集合未变）。**下一批必须现算。**

## 6. 知识库产物（Step 8）

| 产物 | 路径 |
|---|---|
| 状态报告 | `reports/XR-Daily-Report-2026-11-23.md`（8,365 字符） |
| 前沿参考 7 维表（39 篇，非当日新拉取） | `papers/daily/2026-11-23/7dim-table.md` |
| 运行日志 | `papers/daily/2026-11-23/run_log.md`（本文件） |
| 对账数据 | `data/audit_1123_days.json`、`audit_1123_alldays.json`、`newday_1123.json`、`missed_prev_1123.json`、`missed_new_1123.json`、`missed_xr_1123.json` |
| 门③ 留痕 | `data/gates_1123.json` |
| 总索引 | `papers/MOC/MOC-总索引.md`（11-23 状态注记 + 速查入口 + 批次索引行 + 页脚） |

## 7. 前端与发布（Step 9）

见报告 §7.4 与 `STATUS.md` §5 自检清单（构建计数、`node --check`、CDP 冒烟、`check_release`、渠道② 推送与线上 md5 核验、渠道① 挂账计数）。

## 8. 已知限制与继承事项

1. 渠道① `xr-paper-hub.app.workbuddy.host` 自 2026-10-21 起 403，`workbuddy_sites_deploy` 不在工具集，累计挂账批次数见 STATUS.md O-1。
2. 硬件显示侧（波导 / 可变焦 / Maxwellian / 光场）连续多批无器件级破冰。
3. 上一公告组复核**必须用上一批的 RSS 文件**（今日空源会致 471/471 无摘要）。
