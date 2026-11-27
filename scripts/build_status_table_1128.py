# -*- coding: utf-8 -*-
"""build_status_table_1128.py —— 生成 2026-11-28 状态日的 7 维前沿参考表。

状态日无新稿：整表为「文献库最新前沿参考（11-27 运行处理的 11-26 公告批次：主批 55 + backfill 8）」，
表头必须含 `#` 与 `arXiv` 两列（build_frontend._parse_rows 以 arXiv 列取 ID 锚点，缺列会让批次卡表内=0）。
"""
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

HEAVY = False  # 11-27 批非重磅日（当日最高 4.35 vs 库内 4.459，margin −0.109），未授予 S
rows = []
for r in scored:
    rid = r["id"]
    g = (reg.get(rid) or {}).get("grade") or assign_grade(r["value"], r["batch"], HEAVY)
    calc = assign_grade(r["value"], r["batch"], HEAVY)
    assert g == calc, f"{rid} registry={g} calc={calc}"
    rows.append(dict(r, grade=g))
rows.sort(key=lambda r: (-r["value"], -r["scores"]["IMP"], -r["scores"]["NOV"], r["id"]))

main = [r for r in rows if r["batch"] == "2026-11-27"]
bf = [r for r in rows if r["batch"] == "backfill-1127"]
gcnt_main = {k: sum(1 for r in main if r["grade"] == k) for k in "SABC"}
gcnt_bf = {k: sum(1 for r in bf if r["grade"] == k) for k in "SABC"}

head = f"""# 7 维度对比表 · 2026-11-28（文献库最新前沿参考，非当日新拉取）

> ⚠️ 说明：本运行日（周六 2026-11-28 02:30）经漏网对账 + 五源互证核验，**无新增可处理论文**——
> ① listing 7 分类（cs.CV / cs.GR / cs.HC / cs.MM / cs.RO / cs.AI / eess.IV）最新公告日**均为 2026-11-26（周四）**，**无 11-27（周五）/ 11-28（周六）公告日组**（周五公告组未释放——工作日公告跳空，与 10-29、11-12 同型；周六为 `skipDays` 节律）；缓存穿透 `recent?cb=1128a` 与 `pastweek` 复验一致，跨学科复核（math.AP / cs.CL `pastweek`）最新日组同为 `Thu, 26 Nov 2026`；
> ② API `export.arxiv.org` **200**，`submittedDate` 降序前沿 = **2026-11-25**（11-26 公告组来源，已全部入馆）；`cat:cs.CV AND submittedDate:[20261126 TO 20261128]` 命中 **0 篇**；
> ③ RSS `OK_CATS=7/7`：cs.CV / cs.GR / cs.HC / cs.MM / cs.RO / eess.IV **均为 0 条目**；cs.AI 有 **398 条**但为**陈旧 feed 重戳日期**（`lastBuildDate` Fri 27 Nov 05:00 UTC，逐条 `base_id` 全部 ⊂ 上一批 `data/raw/2026-11-27.jsonl`（849 条）的 11-26 组内容，`cur_only=0`）——**单分类非空 ≠ 有新公告**；
> ④ 11-26 公告组（上批）完整性复采：逐分类 **declared=got**（CV 288/GR 10/HC 20/MM 7/RO 109/AI 248/IV 13 = **695 槽位 / 569 篇唯一**），未入馆 **513 篇**（= 569 − 56 已入馆，其中 55 篇为 11-27 主批、1 篇为库内既有 cross 再公告）摘要级 XR 过滤（513/513 有 RSS 摘要，覆盖率 **1.0000**）命中 **47 篇**，全部落在 11-27 运行显式处置集合（nonxr_1127 ∪ xr_pool_1127 ∪ xr_final_1127 ∪ backfill_pool_1127 ∪ scored_1127 ∪ old_replace_1127 ∪ registry）→ **0 漏网、无 backfill**。
> 下表为**文献库最新前沿（11-27 运行处理的 11-26 公告批次：主批 {len(main)} 篇 + backfill-1127 {len(bf)} 篇）的 7 维参考表**，供查阅，**非「当日新论文」对比表**。

> 维度与权重固定：`Value = 0.20·IMP + 0.20·NOV + 0.15·TEC + 0.15·EXP + 0.15·PER + 0.08·TRL + 0.07·REP`；分档：S≥4.20 且 blockbuster / A 3.60–4.20 / B 3.00–3.60 / C<3.00

> 拉取窗口：无（状态日；最新公告日 2026-11-26，已由 11-27 运行完整处理，本日复核 0 漏网）

## 前沿参考（公告日 2026-11-26 · 11-27 运行处理：主批 {len(main)} 篇 {gcnt_main['S']}S/{gcnt_main['A']}A/{gcnt_main['B']}B/{gcnt_main['C']}C + backfill-1127 {len(bf)} 篇 {gcnt_bf['S']}S/{gcnt_bf['A']}A/{gcnt_bf['B']}B/{gcnt_bf['C']}C）

| # | arXiv | 论文 | 赛道 | IMP | NOV | TEC | EXP | PER | TRL | REP | 总分 | 档 | 批次 | 证据 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
"""
lines = [head]
for i, r in enumerate(rows, 1):
    s = r["scores"]
    title = r.get("title_zh") or r["title"]
    batch = "主批 2026-11-27" if r["batch"] == "2026-11-27" else "backfill-1127"
    lines.append(
        f"| {i} | [{r['id']}](https://arxiv.org/abs/{r['id']}) | {title} | {r['track']} | "
        f"{s['IMP']} | {s['NOV']} | {s['TEC']} | {s['EXP']} | {s['PER']} | {s['TRL']} | {s['REP']} | "
        f"**{r['value']:.2f}** | {r['grade']} | {batch} | {r.get('evidence', 'FULL')} |\n")
lines.append("\n> 档位口径：11-27 批为**非重磅日**（当日最高 4.35 vs 库内近 30 天 Top10 均分 4.459，margin **−0.109**、blockbuster=false），"
             "按 §7 档位口径不授予 S——4.35（ProManO / AnyCam）、4.20（Who Is Ego）达 S 线者**记 A 并注明达线**；"
             "backfill-1127 不参与重磅日判定，最高 4.43（2611.31822）亦记 A。本日无新评分，档位与 registry 逐行一致。\n")
os.makedirs("papers/daily/2026-11-28", exist_ok=True)
io.open("papers/daily/2026-11-28/7dim-table.md", "w", encoding="utf-8").write("".join(lines))
print("rows", len(rows), "main", len(main), "bf", len(bf))
print("grades main", gcnt_main, "bf", gcnt_bf)
print("max", rows[0]["value"], rows[0]["id"], rows[0].get("title_zh"))
