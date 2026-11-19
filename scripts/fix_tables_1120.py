# -*- coding: utf-8 -*-
"""修正 2026-11-20 的 7 维表结构，并补齐 backfill-1120 批次目录。

根因（2026-11-20 踩坑）：
  build_frontend.parse_daily_table -> _parse_rows 用 `ci = find("arXiv")` 定位 ID 列，
  表头若无“arXiv”列，ci 为 None，所有数据行直接 continue -> 批次卡片 表内=0。
  另一处：batches 以 papers/daily/* 目录枚举，缺 backfill-1120 目录则该卡不出现。

本脚本只重写表/明细/日志，不改 registry、不改评分。
"""
import json
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DIMS = ["IMP", "NOV", "TEC", "EXP", "PER", "TRL", "REP"]

MAIN_BATCH = "2026-11-20"
BF_BATCH = "backfill-1120"


def read_json(p):
    with open(p, encoding="utf-8") as f:
        return json.load(f)


def write(p, s):
    os.makedirs(os.path.dirname(p), exist_ok=True)
    with open(p, "w", encoding="utf-8", newline="\n") as f:
        f.write(s)
    print("WROTE", os.path.relpath(p, ROOT), len(s), "chars")


def cell(s):
    return str(s).replace("|", "/").strip()


def row(i, r, star):
    sc = r["scores"]
    t = cell(r.get("title_zh") or r.get("title", ""))
    if star:
        t = t + " ⭐"
    return "| %d | %s | %s | %s | %s | %s | %s | %s | %s | %s | %s | **%.2f** | %s | %s | %s |" % (
        i, r["id"], t, cell(r["track"]),
        sc["IMP"], sc["NOV"], sc["TEC"], sc["EXP"], sc["PER"], sc["TRL"], sc["REP"],
        r["value"], r["grade"], cell(r.get("announce", "new")), cell(r.get("evidence", "FULL")),
    )


# 表头必须带 arXiv 列（build_frontend._parse_rows 以它为 ID 锚点），
# 首列序号列也要在表头占位，否则数据行比表头多一格、列索引整体错位。
HEAD = ("| # | arXiv | 标题 | 赛道 | IMP | NOV | TEC | EXP | PER | TRL | REP | 总分 | 等级 | 公告类型 | 证据 |\n"
        "|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|")


def table(rows, start=1, star_n=0):
    out = [HEAD]
    for i, r in enumerate(rows):
        out.append(row(start + i, r, i < star_n))
    return "\n".join(out)


def sort_rows(rows):
    return sorted(rows, key=lambda r: (-r["value"], r["id"]))


def grade_stat(rows):
    return " / ".join("%d %s" % (sum(1 for r in rows if r["grade"] == g), g) for g in "SABC")


def main():
    scored = read_json(os.path.join(ROOT, "data/scored_1120.json"))
    main_rows = sort_rows([r for r in scored if r["batch"] == MAIN_BATCH])
    bf_rows = sort_rows([r for r in scored if r["batch"] == BF_BATCH])
    assert len(main_rows) == 25, len(main_rows)
    assert len(bf_rows) == 3, len(bf_rows)
    assert not [r for r in scored if r["batch"] not in (MAIN_BATCH, BF_BATCH)]

    top10 = main_rows[:10]
    rest = main_rows[10:]
    tracks = []
    for r in top10:
        if r["track"] not in tracks:
            tracks.append(r["track"])

    # ---------- 主批 7 维表 ----------
    L = []
    L.append("# 7 维对比表 · 2026-11-20（主批 25 篇）")
    L.append("")
    L.append("> 拉取窗口：2026-11-19 公告批次（公告日 11-19 ≠ 拉取日 11-20 02:30）")
    L.append("")
    L.append("权重 IMP0.20·NOV0.20·TEC0.15·EXP0.15·PER0.15·TRL0.08·REP0.07；"
             "档位 S≥4.20 且 blockbuster / A3.60–4.20 / B3.00–3.60 / C<3.00。")
    L.append("")
    L.append("本批 **25 篇**（listing 502 篇 → KW 52 + 标题级补扫 16 = 68 候选 → 剔 43 → 22 篇，"
             "残差复核采纳 3 篇 → 25 篇）。档位 **%s**，最高 **%.2f**（2611.23417 AVM）。" % (
                 grade_stat(main_rows), main_rows[0]["value"]))
    L.append("门③ 当日最高 %.2f < 库内近 30 天 Top10 均分 4.4230（margin -0.093）→ 非重磅日，无 S。" % main_rows[0]["value"])
    L.append("backfill 3 篇另见 `papers/daily/backfill-1120/`。")
    L.append("")
    L.append("## Top10（按加权总分降序，覆盖 %d 赛道）" % len(tracks))
    L.append("")
    L.append(table(top10, 1, 10))
    L.append("")
    L.append("## 其余 XR 新稿（11–25）")
    L.append("")
    L.append(table(rest, 11, 0))
    L.append("")
    write(os.path.join(ROOT, "papers/daily/2026-11-20/7dim-table.md"), "\n".join(L))

    # ---------- backfill 7 维表 ----------
    B = []
    B.append("# backfill-1120 全量 7 维度对比表（参考）")
    B.append("")
    B.append("> 拉取窗口：2026-11-19 公告批次的 RSS replace 类混入旧稿（v2 再公告），单独编号")
    B.append("")
    B.append("批次：backfill-1120（**11-19 公告批次 RSS 混入的旧稿 v2 再公告**，首次入馆）。")
    B.append("")
    B.append("均非 11-19 当日新提交（API published：2025-11-22 / 2026-06-05 / 2026-07-09；"
             "updated 2026-11-17~11-18），诚实口径单独编号；不参与当日「重磅日」判定，"
             "≥4.20 亦按口径记 A。")
    B.append("")
    B.append("候选来源：RSS replace 类 19 篇 XR 命中中逐篇核摘要取 **3 篇**。")
    B.append("")
    B.append("全文：3 篇全部 **FULL**（含 1 篇 ar5iv 兜底、1 篇 arXiv HTML v2 空壳后补）。"
             "本批最高 **%.2f（2606.07179 EvoGS）**。档位 **%s**。" % (bf_rows[0]["value"], grade_stat(bf_rows)))
    B.append("")
    B.append(table(bf_rows, 1, 0))
    B.append("")
    write(os.path.join(ROOT, "papers/daily/backfill-1120/7dim-table.md"), "\n".join(B))

    # ---------- backfill scored.md ----------
    S = []
    S.append("# 评分明细 · backfill-1120（3 篇）")
    S.append("")
    S.append("- 档位：**%s**（backfill 批最高记 A，不授予 S）" % grade_stat(bf_rows))
    S.append("- 全文：3 篇 FULL；2611 系列主批判定见 `papers/daily/2026-11-20/scored.md`。")
    S.append("")
    S.append("## 逐篇评分理由")
    S.append("")
    for r in bf_rows:
        S.append("### %s %s（%.2f / %s）" % (r["id"], r.get("title_zh", ""), r["value"], r["grade"]))
        S.append("")
        S.append(r.get("scores_why", ""))
        S.append("")
        if r.get("note"):
            S.append("> 注：%s" % r["note"])
            S.append("")
    write(os.path.join(ROOT, "papers/daily/backfill-1120/scored.md"), "\n".join(S))

    # ---------- backfill run_log ----------
    R = []
    R.append("# backfill-1120 执行日志")
    R.append("")
    R.append("- **来源**：11-19 公告批次 RSS 全量 753 条中 replace 类 19 篇 XR 命中（`data/old_replace_1120.json`），"
             "逐篇核摘要取 **3 篇**。")
    R.append("- **诚实口径**：全部为 **v2 再公告**（API updated 2026-11-17~11-18），"
             "原始投稿 2025-11-22 / 2026-06-05 / 2026-07-09；均非 11-19 当日新提交，"
             "单独编号、不参与当日重磅日判定。")
    R.append("- **全文**：3 篇全部 FULL。2606.07179 的 arXiv HTML v2 为 1,578 字符空壳，"
             "改用 ar5iv 抓取 56,366 字符（L1/FULL）。")
    R.append("- **定稿 %s（无 S）**：%s" % (grade_stat(bf_rows), " · ".join(
        "%s %s **%.2f**" % (r["id"], r.get("title_zh", "")[:18], r["value"]) for r in bf_rows)))
    R.append("- **标题不一致**：2606.07179 的 arXiv 元数据标题为 *Lifting 3D Gaussians: A Wavelet "
             "Multiresolution Representation for Scalable Gaussian Splatting Streaming*，"
             "正文（v2 / ar5iv）标题为 *EvoGS: Constructing Continuous-Layered Gaussian Splatting "
             "with Evolution Tree for Scalable 3D Streaming*，疑为 v2 改题；registry 采用元数据标题。")
    R.append("- **registry**：+3（batch=backfill-1120，按 base_id 幂等）。")
    R.append("")
    write(os.path.join(ROOT, "papers/daily/backfill-1120/run_log.md"), "\n".join(R))

    # ---------- backfill 报告 ----------
    P = []
    P.append("# XR Backfill 报告 · backfill-1120")
    P.append("")
    P.append("**批次**：backfill-1120　|　**来源公告批次**：2026-11-19（周四）　|　"
             "**拉取日**：2026-11-20 02:30（北京时间）")
    P.append("")
    P.append("> 本批 3 篇均非 11-19 当日新提交，系 RSS replace 类混入的 v2 再公告旧稿。"
             "按诚实口径单独编号，不参与当日「重磅日」判定，最高分亦按 A 记。")
    P.append("")
    P.append("## 一、为什么要单列")
    P.append("")
    P.append("arXiv 每日 RSS 的 replace 通道会把「旧论文发新版」混进当日列表，"
             "其 `published` 时间戳是公告时间、并非首次提交时间。"
             "若与当日新稿同批评分，会把几个月前的存量工作算成当日前沿，"
             "既污染「当日最高分 vs 库内近 30 天均值」的门③ 判定，也让批次统计失真。")
    P.append("")
    P.append("本批 3 篇的首次提交日（API 核验）分别为 **2025-11-22**、**2026-06-05**、**2026-07-09**，"
             "与公告日 2026-11-19 相差 4–12 个月。")
    P.append("")
    P.append("## 二、本批清单")
    P.append("")
    P.append(table(bf_rows, 1, 0))
    P.append("")
    P.append("## 三、价值判断")
    P.append("")
    for r in bf_rows:
        P.append("### %s %s（%.2f / %s）" % (r["id"], r.get("title_zh", ""), r["value"], r["grade"]))
        P.append("")
        P.append("**赛道**：%s　|　**证据**：%s　|　**代码**：%s" % (
            r["track"], r.get("evidence", "FULL"), r.get("code", "—")))
        P.append("")
        P.append(r.get("scores_why", ""))
        P.append("")
    P.append("## 四、口径与产物")
    P.append("")
    P.append("- 表：`papers/daily/backfill-1120/7dim-table.md`（3 篇全量）")
    P.append("- 明细：`papers/daily/backfill-1120/scored.md`")
    P.append("- 日志：`papers/daily/backfill-1120/run_log.md`")
    P.append("- MOC：`papers/MOC/MOC-backfill-1120.md`")
    P.append("- registry：`batch=backfill-1120`，按 base_id 幂等追加 3 条")
    P.append("")
    write(os.path.join(ROOT, "reports/XR-Backfill-Report-1120.md"), "\n".join(P))


if __name__ == "__main__":
    main()
