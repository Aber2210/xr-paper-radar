# -*- coding: utf-8 -*-
"""build_status_report_1128.py —— 生成 2026-11-28 周六状态日运行报告（11-27 周五公告组未释放）。"""
import io, json, os, sys
sys.path.insert(0, "scripts")
from grade_caliber import assign_grade

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)

scored = json.load(open("data/scored_1127.json", encoding="utf-8"))
reg = {}
for l in io.open("papers/library/registry.jsonl", encoding="utf-8"):
    if l.strip():
        r = json.loads(l)
        reg[r["id"].split(":")[-1].split("v")[0]] = r
G = json.load(open("data/gates_1128.json", encoding="utf-8"))
g3 = G["gate3"]
audit = json.load(open("data/audit_1128_days.json", encoding="utf-8"))

rows = []
for r in scored:
    g = (reg.get(r["id"]) or {}).get("grade") or assign_grade(r["value"], r["batch"], False)
    rows.append(dict(r, grade=g))
rows.sort(key=lambda r: (-r["value"], -r["scores"]["IMP"], -r["scores"]["NOV"], r["id"]))
main = [r for r in rows if r["batch"] == "2026-11-27"]
bf = [r for r in rows if r["batch"] == "backfill-1127"]
top10_ids = json.load(open("data/gates_1127.json", encoding="utf-8"))["gate2"]["top10_ids"]
top10 = [r for r in rows if r["id"] in top10_ids]
top10.sort(key=lambda r: (-r["value"], -r["scores"]["IMP"], -r["scores"]["NOV"], r["id"]))
gcnt_main = {k: sum(1 for r in main if r["grade"] == k) for k in "SABC"}
gcnt_bf = {k: sum(1 for r in bf if r["grade"] == k) for k in "SABC"}
grades_all = {}
for r in reg.values():
    grades_all[r.get("grade")] = grades_all.get(r.get("grade"), 0) + 1

tbl = ["| # | arXiv | 标题 | 赛道 | 总分 | 等级 | 批次 |", "|---|---|---|---|---:|---|---|"]
for i, r in enumerate(rows, 1):
    batch = "主批 11-27" if r["batch"] == "2026-11-27" else "backfill-1127"
    title = (r.get("title_zh") or r["title"]).replace("|", "｜")
    tbl.append(f"| {i} | {r['id']} | {title} | {r['track']} | **{r['value']:.2f}** | {r['grade']} | {batch} |")

t10 = ["| 排名 | arXiv | 标题 | 赛道 | 总分 | 等级 |", "|---:|---|---|---|---:|---|"]
for i, r in enumerate(top10, 1):
    rk = f"**{i}**" if r["id"] in top10_ids else f"({i})"
    t10.append(f"| {i} | {r['id']} | {(r.get('title_zh') or r['title']).replace('|', '｜')} | {r['track']} | **{r['value']:.2f}** | {r['grade']} |")

lib_tbl = ["| # | arXiv | 分数 | 档 | 日期 | 批次 |", "|---|---|---:|---|---|---|"]
for i, r in enumerate(g3["top10_lib"], 1):
    lib_tbl.append(f"| {i} | {r['id']} | {r['value']:.2f} | {r['grade']} | {r['date']} | {r['batch']} |")

acats = "；".join(f"{c} {v['prev']['got']}/{v['prev']['declared']}" for c, v in audit.items())
slots = sum(v["prev"]["got"] for v in audit.values())

doc = f"""# XR 每日论文雷达 · 运行报告 · 2026-11-28（周六 02:30）

> **运行性质：状态日（0 新稿）· 11-27（周五）公告组未释放**。
> listing 7 分类实测最新公告日**仍为 2026-11-26（周四）**，11-27 / 11-28 无公告日段；上一批（11-27 运行）已完整处理 11-26 公告组（主批 55 篇 + backfill 8 篇）。
> **本报告不含任何「当日新论文」、新评分或新 Top10**；第四节为文献库最新前沿参考表（63 篇，逐行与 registry 一致）。
> 公告日 ≠ 拉取日：本日**没有公告日可对**，故不产生新批次编号。

## 一、执行摘要

| 项 | 结果 |
|---|---|
| 新稿 | **0**（无 11-27 / 11-28 公告组；11-27 周五组未释放） |
| 漏网 | **0**（11-26 组未入馆 513 篇，摘要级命中 47 篇全部已在 11-27 运行显式处置） |
| backfill | **无** |
| registry | **1,332 条**（S21 / A671 / B496 / C144），无变更 |
| 笔记 / daily | **954 / 83**（新增本日状态目录 1 个 → **84**） |
| 门③ 现算参考 | **4.465**（窗口 [2026-10-29, 2026-11-28)，**659 条入窗**） |
| S 级 | **0**（状态日不评新稿，不授 S） |
| 残差复核 | 不适用（无新增 `nonxr_1128` 集合） |

**一句话结论**：11-27（周五）公告组在本次 02:30 运行时刻**尚未释放**（工作日公告跳空，与 2026-10-29、2026-11-12 同型），全库无新增；11-26 公告组 569 篇唯一稿已由 11-27 运行消化 56 篇、其余 513 篇逐篇复核为 0 漏网。**下一个调度（11-29 02:30）须优先复核 11-27 组是否延迟释放**。

## 二、漏网对账（Step 1）

### 2.1 公告日头核验（目标窗口 ≥ 2026-11-27）

- 脚本 `scripts/audit_listing_1128.py`（7 分类 × show=500 单页，`declared≠got` 自动补页），**7/7 分类成功，exit 0**；守卫 `check_audit_guard.py` PASS。
- 逐分类最新公告日 **均为 2026-11-26（周四）**，槽位合计 **{slots}**：{acats}。
- `NEW_DAYS = [2026-11-27, 2026-11-28]` 两日 **declared=None、got=0** → 无公告日段（`data/newday_1128.json` 为空）。
- 交叉复核：`recent?cb=1128a` 与 `pastweek` 均 `Thu, 26 Nov 2026`；跨学科 `math.AP` / `cs.CL` `pastweek` 同为 11-26 → 排除分类级 / 本机故障。

### 2.2 11-26 公告组完整性复核（验证上批处理完整性）

- 复采逐分类 **declared=got**（**{slots} 槽位 / 569 篇唯一**，与 11-27 运行逐项一致，`data/group_1126_1128.json`）。
- 已入馆 **56 篇** = 11-27 主批 **55 篇**（逐篇核对全部在组内）+ 1 篇库内既有 cross 再公告；未入馆 **513 篇**。
- 摘要级 XR 过滤（`scripts/filter_missed_1128.py`，RSS 摘要来自 11-27（上一批，覆盖 569/569）与 11-28 两份，**513/513 覆盖，覆盖率 1.0000**）命中 **47 篇**。
- 47 篇 **全部**落在 11-27 运行处置集合（`nonxr_1127` ∪ `xr_pool_1127` ∪ `xr_final_1127` ∪ `backfill_pool_1127` ∪ `scored_1127` ∪ `old_replace_1127` ∪ registry）→ **0 漏网**，`data/missed_xr_1128.json` 为空，**无需 backfill**。

## 三、数据源探测与五源互证（Step 2）

| 源 | 结果 |
|---|---|
| `export.arxiv.org/api/query` | **200**，`cat:cs.CV` 降序前沿 `published` = **2026-11-25T18:59:59Z** |
| `arxiv.org/api/query` | **200**，`cat:cs.CV AND submittedDate:[20261126 TO 20261128]` → **0 篇** |
| listing（7 分类 + 缓存穿透 + pastweek） | 最新日组 **2026-11-26**，11-27 / 11-28 **无日组** |
| 跨学科（math.AP / cs.CL `pastweek`） | 同为 **2026-11-26** |
| RSS（`fetch_rss.py --no-filter`） | `OK_CATS=7/7`、`WROTE=398`：6 分类 **0 条目**；cs.AI **398 条为陈旧 feed 重戳**（逐条 ⊂ 11-27 批 RSS 849 条，`cur_only=0`） |

**RSS 判读（本日关键）**：cs.AI 返回 398 条、`lastBuildDate = Fri, 27 Nov 2026 05:00 UTC`、条目 `published` 全为 `2026-11-27T00:00:00Z`——**看似新公告，实为陈旧内容**。判定方法：与上一批 RSS（`data/raw/2026-11-27.jsonl`，849 条）做 `base_id` 集合比较，**398 条全部在旧集合内、`cur_only=0`**，故不构成新稿。单分类非空 ≠ 有新公告（同 2026-10-30 先例）。

五源互证结论一致：**无新稿可处理**。

## 四、文献库最新前沿参考（11-26 公告批次 · 63 篇 · 非当日新拉取）

下两表为 11-27 运行处理的批次（主批 {len(main)} 篇 {gcnt_main['S']}S/{gcnt_main['A']}A/{gcnt_main['B']}B/{gcnt_main['C']}C + backfill-1127 {len(bf)} 篇 {gcnt_bf['S']}S/{gcnt_bf['A']}A/{gcnt_bf['B']}B/{gcnt_bf['C']}C），完整 7 维表见 [papers/daily/2026-11-28/7dim-table.md](../papers/daily/2026-11-28/7dim-table.md)。

### 4.1 该批 Top10（定稿含门②回补）

{chr(10).join(t10)}

> 门② 重筛记录：纯值 Top10 仅覆盖 **4 赛道**（重建与SLAM 5 席）→ 剔除 2611.34932（4.01，赛道冗余，仍入馆记 A）回补 2611.33467（4.00，世界模型与仿真）→ 定稿 **5 赛道**。档位：非重磅日（margin −0.109），4.35 / 4.20 达 S 线者记 **A** 并注明达线。

### 4.2 全量（63 篇，按加权分降序）

{chr(10).join(tbl)}

## 五、覆盖度校验（Step 6）

| 关 | 本日状态 | 说明 |
|---|---|---|
| 门① 最大 Jaccard < 0.62 | **不适用** | 0 候选，无本批集合可比 |
| 门② Top10 覆盖 ≥5 赛道 | **不适用** | 无新 Top10；上一批（11-27）纯值 4 赛道 → 回补一次 → 5 赛道 |
| 门③ 价值天花板 | **仅现算基线** | 窗口 [2026-10-29, 2026-11-28)，**659 条入窗**，Top10 均分 **{g3['top10_mean']}**；今日无候选 → `today_max=null`、`blockbuster=false`、`s_awarded=false` |

### 5.1 门③ 库内 Top10（现算，供下一批对照）

{chr(10).join(lib_tbl)}

> 均分 **{g3['top10_mean']}**（上一批 4.459）**上升 0.006**：窗口前移使 2026-10-28 批出窗、11-27 批入库（2611.31822 backfill 4.43 / 2611.34480 4.35 等），Top10 集合本次含 backfill-1127 的 4.43。**窗口每日滑动，下一批务必现算，勿沿用本值。**

## 六、残差复核（Step 3.5）

- 状态日无新增 `data/nonxr_1128.json`，`residual_scan.py` **未执行**，不生成 `data/residual_1128.json`（不为消 WARN 补造）。
- 历史 rate：11-26 批 **1.52%**、11-27 批 **5.71%（30/525，近 20 批最高）**；距 12% 上报阈值仍远，不触发连续超标计数（连续 3 日 >12% 才上报）。
- 11-27 批登记的缺口方向（几何记忆 / 世界模型状态 / 社会具身）在本日空跑中无法验证，**留待下一次真实批次观察是否成批漏检**。

## 七、附录

### 7.1 证据等级分布

本日无新抓取。前沿参考 63 篇的证据等级沿用 11-27 批：**62 篇 L0/FULL + 1 篇 L1/PARTIAL**（2611.33313，`fetch_fulltext.py` 的 landing-page 守卫首次真实拦截：ar5iv 仅返摘要落地页）。

### 7.2 失败/降级清单

无失败项。RSS 6 分类空源为周五/周六节律（非故障）；cs.AI 陈旧 feed 已按集合比对排除；API 双主机 200；对账 7/7 分类 exit 0；上一公告组 513/513 摘要覆盖。

### 7.3 产物清单

| 产物 | 路径 |
|---|---|
| 状态报告 | `reports/XR-Daily-Report-2026-11-28.md` |
| 前沿参考 7 维表（63 篇） | `papers/daily/2026-11-28/7dim-table.md` |
| 运行日志 | `papers/daily/2026-11-28/run_log.md` |
| 对账数据 | `data/audit_1128_days.json`、`audit_1128_alldays.json`、`newday_1128.json`、`missed_prev_1128.json`、`missed_new_1128.json`、`missed_xr_1128.json`、`group_1126_1128.json` |
| 门③ 留痕 | `data/gates_1128.json` |
| 总索引 | `papers/MOC/MOC-总索引.md`（11-28 状态注记 + 批次索引行 + 页脚） |

### 7.4 发布记录

见文末「发布」节与 `STATUS.md` §5 自检清单。
"""
io.open("reports/XR-Daily-Report-2026-11-28.md", "w", encoding="utf-8").write(doc)
print("written", len(doc), "chars; rows", len(rows), "main", len(main), "bf", len(bf), "top10", len(top10))
