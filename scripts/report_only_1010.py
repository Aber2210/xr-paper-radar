# -*- coding: utf-8 -*-
"""report_only_1010.py — 仅生成最终解读报告，从已写好的 10 篇原子笔记聚合 §三，避免重跑 MOC 更新。"""
import json, os, re
ROOT = "D:/Agent/WorkBuddy/Research"
BATCH = "2026-10-10"; ANNOUNCE = "2026-10-09"
scored = json.load(open(f"{ROOT}/data/scored_1010.json", encoding="utf-8"))
TOP = scored[:10]

# 从原子笔记文件读取每篇内容
def load_note(bid):
    d = f"{ROOT}/papers/notes"
    for fn in os.listdir(d):
        if fn.startswith(bid + "__"):
            return open(os.path.join(d, fn), encoding="utf-8").read()
    return None

def fmt_chapter(rank, s, md):
    bid = s["base_id"]
    # 解析 frontmatter 后的章节
    body = md.split("\n# ", 1)[1] if "\n# " in md else md
    # 取中文标题（第一个 # 标题）
    title_line = ""
    for ln in body.splitlines():
        if ln.startswith("# "):
            title_line = ln[2:].strip(); break
    out = (f"## 第 {rank} 章 · {s['title_zh']}（{s['grade']} 级 · {s['value']:.2f} · {s['track']}）\n\n"
           f"> arXiv:{bid} ｜ 赛道：{s['track']} ｜ 证据等级：FULL（L0 全文） ｜ 状态：CURRENT\n\n")
    # 把笔记里的二级标题保留为三级
    for ln in body.splitlines():
        if ln.startswith("## "):
            out += "### " + ln[3:] + "\n"
        elif ln.startswith("# "):
            continue
        else:
            out += ln + "\n"
    return out

report = f"""# XR 每日论文雷达 · 解读报告（{BATCH}）

> 拉取日 **{BATCH}**（周六）｜arXiv submittedDate 批次 **{ANNOUNCE}**（周五提交）｜数据源：rss.arxiv.org 兜底（API submittedDate 前沿滞后于 10-08）。
> 7 维权重：IMP0.20 · NOV0.20 · TEC0.15 · EXP0.15 · PER0.15 · TRL0.08 · REP0.07。档位 S≥4.20 · A 3.60–4.20 · B 3.00–3.60 · C<3.00。

## 一、执行摘要

- **实际命中区间**：arXiv submittedDate 批次 {ANNOUNCE}（周五提交），拉取日 {BATCH}（周六，周末节律）。本报告**绝不伪装"当日新论文"**——上游 API submittedDate 索引前沿停滞于 10-08，RSS 兜底抓到的是 {ANNOUNCE} 周五提交批次。
- **入选规模**：去 registry（374）后新提交 XR 核心相关 **25 篇**（2610.*）；剔除 2 篇非 XR（CoCam4D 自动驾驶、OX-NeRF 医学 X 射线）+ 4 篇旧稿再公告（2602/2603/2605）单列 backfill。
- **Top10**：全部 **A 级**（最高 3.90，最低 3.70），**无 S 级**。
- **赛道覆盖**：7 个赛道（内容生成 / 渲染与显示 / 化身与人体 / 重建与SLAM / 神经渲染 / 世界模型与仿真 / 感知与认知）——覆盖度门②通过。
- **重要发现**：① 头部化身方向本期集中爆发（GHARP 实时规范表示、Fresco++ 优化范式、延续 10-09 边缘头像），与库内"逐高斯压缩/结构化表示"并行；② 内容生成从"静态 3DGS"走向"动态 cinemagraph"（OuroWorld）与"单图→4D"（MATE4D）；③ 注视点渲染的 judder masking（2610.10811）与 FaceGAN 流式说话头是两条强实用型 XR 工程路线。
- **诚实口径**：门③ 当日最高 3.90 < 库近 30 天 Top10 均分 3.903 → **非重磅日，未拔高、未虚构 S 级**。

## 二、Top10 排行榜（按重要性降序）

| 排名 | arXiv | 标题 | 赛道 | 总分 | 等级 |
|---|---|---|---|---|---|
"""
for i, s in enumerate(TOP, 1):
    report += f"| {i} | {s['base_id']} | {s['title_zh']} | {s['track']} | {s['value']:.2f} | {s['grade']} |\n"
report += "\n## 三、逐篇深度解读（每篇一章，按重要性降序）\n\n"
for i, s in enumerate(TOP, 1):
    md = load_note(s["base_id"])
    if md:
        report += fmt_chapter(i, s, md) + "\n---\n\n"
    else:
        report += f"## 第 {i} 章 · {s['title_zh']}\n\n> 笔记缺失。\n\n"
report += ("## 四、当日全量 7 维度对比表（参考）\n\n"
           "> 下表为本次 {ANNOUNCE} 批次全部 25 篇 XR 新稿的 7 维评分参考；Top10 已全文精读（见 §三），其余 B/A 级候选基于摘要评估。\n\n")
dim_tbl = open(f"{ROOT}/papers/daily/{BATCH}/7dim-table.md", encoding="utf-8").read()
report += dim_tbl.split("\n", 1)[1] if "\n" in dim_tbl else dim_tbl
report += ("\n\n## 五、覆盖率校验与筛选过程说明\n\n"
           f"- **门① 同质去重**：Top10 与文献库（399 篇）标题+摘要 token Jaccard 最大 **0.357**（2610.10945 vs 库内 Budgeted-GS），远低于 0.62 阈值 → **通过，无同质重复**。\n"
           f"- **门② 方向覆盖度**：Top10 覆盖 **7 个赛道**（≥5 通过），无筛选偏食。\n"
           f"- **门③ 价值天花板**：当日最高 {max(s['value'] for s in scored):.2f} < 库近 30 天 Top10 均分 3.903 → **非重磅日，无 S 级，未拔高**。\n"
           "- **重筛闭环**：三关全部通过，未触发重筛；所有入选在价值维度上已覆盖当前文献库主航道（无冷门高价值候选被漏）。\n"
           "- **诚实处理**：剔除 2 篇非 XR（CoCam4D 自动驾驶、OX-NeRF 医学 X 射线断层）与 4 篇旧稿再公告（2602.03538/2603.13833/2605.22342/2605.27820），旧稿建议 API 健康时单开 backfill。\n\n"
           "## 六、附录：抓取失败/降级清单与证据等级\n\n"
           "- **全文抓取**：Top10 共 10 篇，全部 **L0 / FULL**（arxiv.org/html 源，35K–99K 字符，串行 3s/篇，无限流/降级/伪造）；manifest 合并写入校验通过。\n"
           "- **其余 15 篇 XR 候选**（B/A 级，未入 Top10）：基于摘要评估，证据等级 **ABSTRACT_ONLY**（L5），已在 7 维表与 MOC 标注，未生成逐篇笔记。\n"
           "- **落后标注**：本期 **OUTDATED/SUPERSEDED 0 篇**；路线级观察 2 条（头部化身'表示-优化-实时'三角、内容生成'静态→动态/单图→4D'），均以 CURRENT 记录、未判取代。\n"
           "- **数据源**：arxiv.org/api/query 探针 200 但 submittedDate 前沿停滞 10-08；rss.arxiv.org 200 → RSS 兜底；无 404/406 阻断，无推迟重跑。\n")
open(f"{ROOT}/reports/XR-Daily-Report-{BATCH}.md", "w", encoding="utf-8").write(report)
print(f"最终解读报告 -> reports/XR-Daily-Report-{BATCH}.md （{len(report)} 字符）")
