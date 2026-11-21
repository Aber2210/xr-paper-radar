# -*- coding: utf-8 -*-
"""build_status_report_1122.py —— 生成 2026-11-22 周末状态日运行报告。"""
import io, json, os, sys
sys.path.insert(0, "scripts")
from grade_caliber import assign_grade

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)

scored = json.load(open("data/scored_1121.json", encoding="utf-8"))
reg = {}
for l in io.open("papers/library/registry.jsonl", encoding="utf-8"):
    if l.strip():
        r = json.loads(l)
        reg[r["id"].split(":")[-1].split("v")[0]] = r
G = json.load(open("data/gates_1122.json", encoding="utf-8"))
g3 = G["gate3"]

rows = []
for r in scored:
    g = (reg.get(r["id"]) or {}).get("grade") or assign_grade(r["value"], r["batch"], False)
    rows.append(dict(r, grade=g))
rows.sort(key=lambda r: (-r["value"], -r["scores"]["IMP"], -r["scores"]["NOV"], r["id"]))
main = [r for r in rows if r["batch"] == "2026-11-21"]

tbl = ["| # | arXiv | 标题 | 赛道 | 总分 | 等级 | 批次 |", "|---|---|---|---|---:|---|---|"]
for i, r in enumerate(rows, 1):
    batch = "主批 11-21" if r["batch"] == "2026-11-21" else "backfill-1121"
    title = (r.get("title_zh") or r["title"]).replace("|", "｜")
    tbl.append(f"| {i} | {r['id']} | {title} | {r['track']} | **{r['value']:.2f}** | {r['grade']} | {batch} |")

lib_tbl = ["| # | arXiv | 分数 | 档 | 日期 | 批次 |", "|---|---|---:|---|---|---|"]
for i, r in enumerate(g3["top10_lib"], 1):
    lib_tbl.append(f"| {i} | {r['id']} | {r['value']:.2f} | {r['grade']} | {r['date']} | {r['batch']} |")

doc = f"""# XR 每日论文雷达 · 运行报告 · 2026-11-22（周日 02:30）

> **运行性质：周末状态日（0 新稿）**。arXiv `skipDays` 含周六/周日，11-21 / 11-22 无公告批次；
> 最新公告日 **2026-11-20（周五）** 已由 11-21 运行完整处理（主批 37 篇 + backfill 2 篇）。
> **本报告不含任何「当日新论文」、新评分或新 Top10**；第四节为文献库最新前沿参考表（39 篇，逐行与 registry 一致）。

## 一、执行摘要

| 项 | 结果 |
|---|---|
| 新稿 | **0**（无 11-21 / 11-22 公告组） |
| 漏网 | **0**（11-20 组未入馆 471 篇，摘要级命中 43 篇全部已在 11-21 运行显式处置） |
| backfill | **无** |
| registry | **1,082 条**（S18 / A526 / B408 / C130），无变更 |
| 笔记 / daily / MOC | **718 / 73 / 62** |
| 门③ 现算参考 | **4.432**（窗口 2026-10-23 ~ 2026-11-22，485 条入窗） |
| S 级 | **0**（状态日不评新稿，不授 S） |
| 残差复核 | 不适用（无新增 nonxr 集合） |

**一句话结论**：本日是节律性空窗——周末不公告，11-20 公告组已在上一批（11-21）全量消化，逐篇复核未发现漏网；库况与前一批结束后完全一致，唯一变化是文档侧维护与前端/远端同步。

## 二、漏网对账（Step 1）

### 2.1 公告日头核验（目标窗口 ≥ 2026-11-21）

- 脚本 `scripts/audit_listing_1122.py`（7 分类 × show=500 单页，`declared≠got` 自动补页），**7/7 分类成功，exit 0**；守卫预检 `check_audit_guard.py` PASS。
- 逐分类最新公告日 **均为 2026-11-20**：cs.CV 213 槽 / cs.GR 6 / cs.HC 23 / cs.MM 4 / cs.RO 92 / cs.AI 252 / eess.IV 15。
- `NEW_DAYS = [2026-11-21, 2026-11-22]` 两日 **declared=None、got=0** → 无公告日段。
- 交叉复核：`recent?cb=8801` 与 `pastweek` 均 `Fri, 20 Nov 2026`；跨学科 `math.AP` / `cs.CL` `pastweek` 同为 11-20 → 排除分类级/本机故障。

### 2.2 11-20 公告组完整性复核（验证上批处理完整性）

- 复采逐分类 **declared=got**（**605 槽位**，与 11-21 运行逐项一致），唯一论文 **508 篇**。
- 未入馆 **471 篇**（= 508 − 37 主批已入馆），摘要级 XR 过滤（`scripts/filter_missed_1122.py`，RSS 摘要来自 11-19/11-20/11-21 三份全量，**471/471 覆盖，覆盖率 1.0000**）命中 **43 篇**。
- 43 篇 **全部**落在 11-21 运行处置集合（`nonxr_1121` 428 条 ∪ `xr_pool_1121` 37 条 ∪ `rejected_1121` ∪ `backfill_pool_1121` ∪ `scored_1121` 39 条）→ **0 漏网**，`data/missed_xr_1122.json` 为空，**无需 backfill**。

## 三、数据源探测与五源互证（Step 2）

| 源 | 结果 |
|---|---|
| `export.arxiv.org/api/query` | 200 |
| `arxiv.org/api/query` | 200 |
| cs.CV `submittedDate` 前沿 | **2026-11-19**（11-20 公告组来源，已全部入馆） |
| RSS 7 分类 | 200，**0 条目**，`WROTE=0 OK_CATS=7/7`（周末节律空源，非代理故障） |

五源互证（listing 日期头 / 缓存穿透 / pastweek / 跨学科 / API+RSS）结论一致：**无新稿可处理**。

**时序口径**：周末提交积压于**周一 00:00 UTC = 2026-11-23 08:00 北京时间**释放，晚于 11-23 02:30 运行时刻 → 11-23 预计仍为状态日；**11-24（周二）02:30** 才处理该批次，须标注「公告日 ≠ 拉取日」并逐篇核 API `published`。

## 四、文献库最新前沿参考（11-20 公告批次 · 39 篇 · 非当日新拉取）

以下为 11-21 运行处理的批次（主批 37 篇 0S/23A/13B/1C + backfill-1121 2 篇 1A/1B），完整 7 维表见 [papers/daily/2026-11-22/7dim-table.md](../papers/daily/2026-11-22/7dim-table.md)：

{chr(10).join(tbl)}

> 档位口径：11-21 批为**险过日**（当日最高 4.43 vs 库内近 30 天 Top10 均分 4.4230，margin +0.007 < 0.05），按 skill §8.6.3 不授予 S——6 篇 ≥4.20（4.43 / 4.32 / 4.30 / 4.30 / 4.28 / 4.22）**记 A 并注明达 S 线**；backfill-1121 不参与重磅日判定，最高 StableGrasp 4.08 记 A。

## 五、覆盖度校验（Step 6）

| 关 | 本日状态 | 说明 |
|---|---|---|
| 门① 最大 Jaccard < 0.62 | **不适用** | 0 候选，无本批集合可比 |
| 门② Top10 覆盖 ≥5 赛道 | **不适用** | 无新 Top10；上一批（11-21）定稿 5 赛道（重筛一次） |
| 门③ 价值天花板 | **仅现算基线** | 窗口 [2026-10-23, 2026-11-22)，**485 条入窗**，Top10 均分 **{g3['top10_mean']}**；今日无候选 → `today_max=null`、`blockbuster=false`、`s_awarded=false` |

### 5.1 门③ 库内 Top10（现算，供下一批对照）

{chr(10).join(lib_tbl)}

> 均分 4.432，较上一批的 4.4230 升 0.009：11-21 批 AnyVIO 4.43 与 11-18 批 4.43 / 4.37 均已入窗，同时 2610.23772（4.57）仍在窗内。**窗口每日滑动，下一批务必现算，勿沿用本值。**

## 六、残差复核（Step 3.5）

- 状态日无新增 `data/nonxr_1122.json`，`residual_scan.py` **未执行**，不生成 `data/residual_1122.json`。
- 历史 rate：11-20 批 **2.8%**、11-21 批 **1.6%**，距 12% 上报阈值远；本日空跑不计入连续超标计数。
- `check_release.py` 的 R 项对本日报 **WARN（未执行）**，属状态日预期。

## 七、附录

### 7.1 证据等级分布

本日无新抓取。前沿参考 39 篇的证据等级沿用 11-21 批：**39 篇全部 L0/FULL**（33,057–196,730 字符，bad=0；该批无 PARTIAL）。

### 7.2 失败/降级清单

无失败项。RSS 空源为 `skipDays` 节律（非故障）；API 双主机 200；对账 7/7 分类 exit 0。

### 7.3 产物清单

| 产物 | 路径 |
|---|---|
| 状态报告 | `reports/XR-Daily-Report-2026-11-22.md` |
| 前沿参考 7 维表（39 篇） | `papers/daily/2026-11-22/7dim-table.md` |
| 运行日志 | `papers/daily/2026-11-22/run_log.md` |
| 对账数据 | `data/audit_1122_days.json`、`audit_1122_alldays.json`、`newday_1122.json`、`missed_prev_1122.json`、`missed_new_1122.json`、`missed_xr_1122.json` |
| 门③ 留痕 | `data/gates_1122.json` |
| 总索引 | `papers/MOC/MOC-总索引.md`（11-22 状态注记 + 速查入口 + 批次索引行 + 页脚） |

### 7.4 发布记录

见文末「发布」节与 `STATUS.md` §5 自检清单。
"""
io.open("reports/XR-Daily-Report-2026-11-22.md", "w", encoding="utf-8").write(doc)
print("written", len(doc), "chars; rows", len(rows), "main", len(main))
