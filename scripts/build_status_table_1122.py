# -*- coding: utf-8 -*-
"""build_status_table_1122.py —— 生成 2026-11-22 状态日的 7 维前沿参考表。

状态日无新稿：整表为「文献库最新前沿参考（11-21 运行处理的 11-20 公告批次：主批 37 + backfill 2）」，
表头必须含 `#` 与 `arXiv` 两列（build_frontend._parse_rows 以 arXiv 列取 ID 锚点，缺列会让批次卡表内=0）。
"""
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

HEAVY = False  # 11-21 批为险过日（margin +0.007 < 0.05），未授予 S
rows = []
for r in scored:
    rid = r["id"]
    g = (reg.get(rid) or {}).get("grade") or assign_grade(r["value"], r["batch"], HEAVY)
    calc = assign_grade(r["value"], r["batch"], HEAVY)
    assert g == calc, f"{rid} registry={g} calc={calc}"
    rows.append(dict(r, grade=g))
rows.sort(key=lambda r: (-r["value"], -r["scores"]["IMP"], -r["scores"]["NOV"], r["id"]))

main = [r for r in rows if r["batch"] == "2026-11-21"]
bf = [r for r in rows if r["batch"] == "backfill-1121"]
gcnt_main = {k: sum(1 for r in main if r["grade"] == k) for k in "SABC"}
gcnt_bf = {k: sum(1 for r in bf if r["grade"] == k) for k in "SABC"}

head = f"""# 7 维度对比表 · 2026-11-22（文献库最新前沿参考，非当日新拉取）

> ⚠️ 说明：本运行日（周日 2026-11-22 02:30）经漏网对账 + 五源互证核验，**无新增可处理论文**——
> ① listing 7 分类（cs.CV / cs.GR / cs.HC / cs.MM / cs.RO / cs.AI / eess.IV）最新公告日均为 **2026-11-20（周五）**，**无 11-21（周六）/ 11-22（周日）公告日组**（`skipDays` 节律）；缓存穿透 `recent?cb=8801` 与 `pastweek` 复验一致，跨学科复核（math.AP / cs.CL `pastweek`）最新日组同为 `Fri, 20 Nov 2026`；
> ② API 双主机（export.arxiv.org / arxiv.org/api/query）均 **200**，`submittedDate` 降序前沿 = **2026-11-19**（11-20 公告组来源，已全部入馆）；
> ③ RSS 7 分类 **全部 0 条目**（`fetch_rss.py` `WROTE=0`、`OK_CATS=7/7`，周末节律空源，非代理故障）；
> ④ 11-20 公告组（上批）完整性复采：逐分类 **declared=got**（CV 213/GR 6/HC 23/MM 4/RO 92/AI 252/IV 15 = **605 槽位 / 508 篇唯一**），未入馆 **471 篇**（= 508 − 37 已入馆）摘要级 XR 过滤（471/471 有 RSS 摘要，覆盖率 **1.0000**）命中 **43 篇**，全部落在 11-21 运行显式处置集合（nonxr_1121 ∪ xr_pool_1121 ∪ rejected_1121 ∪ backfill_pool_1121 ∪ scored_1121）→ **0 漏网、无 backfill**。
> 下表为**文献库最新前沿（11-21 运行处理的 11-20 公告批次：主批 {len(main)} 篇 + backfill-1121 {len(bf)} 篇）的 7 维参考表**，供查阅，**非「当日新论文」对比表**。

> 维度与权重固定：`Value = 0.20·IMP + 0.20·NOV + 0.15·TEC + 0.15·EXP + 0.15·PER + 0.08·TRL + 0.07·REP`；分档：S≥4.20 且 blockbuster / A 3.60–4.20 / B 3.00–3.60 / C<3.00

> 拉取窗口：无（状态日；最新公告日 2026-11-20，已由 11-21 运行完整处理，本日复核 0 漏网）

## 前沿参考（公告日 2026-11-20 · 11-21 运行处理：主批 {len(main)} 篇 {gcnt_main['S']}S/{gcnt_main['A']}A/{gcnt_main['B']}B/{gcnt_main['C']}C + backfill-1121 {len(bf)} 篇 {gcnt_bf['S']}S/{gcnt_bf['A']}A/{gcnt_bf['B']}B/{gcnt_bf['C']}C）

| # | arXiv | 论文 | 赛道 | IMP | NOV | TEC | EXP | PER | TRL | REP | 总分 | 档 | 批次 | 证据 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
"""
lines = [head]
for i, r in enumerate(rows, 1):
    s = r["scores"]
    title = r.get("title_zh") or r["title"]
    batch = "主批 2026-11-21" if r["batch"] == "2026-11-21" else "backfill-1121"
    lines.append(
        f"| {i} | [{r['id']}](https://arxiv.org/abs/{r['id']}) | {title} | {r['track']} | "
        f"{s['IMP']} | {s['NOV']} | {s['TEC']} | {s['EXP']} | {s['PER']} | {s['TRL']} | {s['REP']} | "
        f"**{r['value']:.2f}** | {r['grade']} | {batch} | {r.get('evidence', 'FULL')} |\n")
lines.append("\n> 档位口径：11-21 批为**险过日**（当日最高 4.43 vs 库内近 30 天 Top10 均分 4.4230，margin +0.007 < 0.05），"
             "按 skill §8.6.3 不授予 S——6 篇 ≥4.20（4.43/4.32/4.30/4.30/4.28/4.22）**记 A 并注明达 S 线**；"
             "backfill-1121 不参与重磅日判定，≥4.20 亦记 A。本日无新评分，档位与 registry 逐行一致。\n")
os.makedirs("papers/daily/2026-11-22", exist_ok=True)
io.open("papers/daily/2026-11-22/7dim-table.md", "w", encoding="utf-8").write("".join(lines))
print("rows", len(rows), "main", len(main), "bf", len(bf))
print("grades main", gcnt_main, "bf", gcnt_bf)
print("max", rows[0]["value"], rows[0]["id"], rows[0]["title_zh"])
