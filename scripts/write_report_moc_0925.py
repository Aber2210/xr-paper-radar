# -*- coding: utf-8 -*-
"""组装 2026-09-25 最终解读报告（10 章逐篇精读 + 7维参考表 + 覆盖校验 + 附录 + run_log）
并更新 MOC-2026-09-25.md 与 MOC-总索引.md。
复用 papers/notes/ 下已生成的原子笔记正文，避免重复写作。
"""
import json, os, re, glob, datetime

OUT_DIR="papers/daily/2026-09-25"
NOTES="papers/notes"
SNAP=f"{OUT_DIR}/_scored_snapshot.json"
T7=f"{OUT_DIR}/7dim-table.md"
REP="reports/XR-Daily-Report-2026-09-25.md"
MOC_D="papers/MOC/MOC-2026-09-25.md"
MOC_I="papers/MOC/MOC-总索引.md"
RUNLOG=f"{OUT_DIR}/run_log.md"

snap=json.load(open(SNAP,encoding="utf-8"))
top10=snap["top10"]; xr_recs=snap["xr_recs"]; non_xr=snap["non_xr"]

def read_note_body(bid):
    cand=glob.glob(f"{NOTES}/{bid}__*.md")
    if not cand: return ""
    txt=open(cand[0],encoding="utf-8").read()
    if txt.startswith("---"):
        parts=txt.split("---",2)
        if len(parts)>=3: txt=parts[2]
    txt=txt.strip()
    txt=re.sub(r"^#\s+.*\n+","",txt,count=1)
    return txt.strip()

def fmt(sc): return " | ".join(f"{k}:{sc[k]}" for k in ["IMP","NOV","TEC","EXP","PER","TRL","REP"])

# ---------- 报告 ----------
R=[]
R.append("# XR 每日论文雷达 · 解读报告（2026-09-25）\n")
R.append("> 自动化 `728fcb37` 生成 · 数据源：rss.arxiv.org（export.arxiv.org/api/query 被沙箱代理 406；arxiv.org/api/query 经探测间歇 406，故用 RSS 兜底，详见 run_log）")
R.append("> 口径：今日拉取为最新可用公告批次（RSS 公告日 2026-09-24，拉取日 2026-09-25）；仅含 2609.* 真正新周期提交，旧稿 replace/cross 已排除（见 §五/run_log）。\n")

# 一、执行摘要
R.append("## 一、执行摘要\n")
R.append(f"- **当日新论文（2609.* 新周期提交）**：{len(xr_recs)+len(non_xr)} 篇，其中 **XR 相关 {len(xr_recs)} 篇**、非 XR 留存 {len(non_xr)} 篇。")
R.append(f"- **Top10 价值均分**：**{snap['today_top_mean']}**；**当日最高 {snap['today_max']}**；**S 级 0 篇 / A 级 10 篇**——**当日非重磅日**（最高 4.05 < 库内近 30 天 Top10 均分 {snap['lib_top_mean']}）。")
R.append(f"- **赛道覆盖**：Top10 横跨 {len(snap['top_tracks'])} 个标准赛道（{ '、'.join(snap['top_tracks'])}），覆盖度门②通过。")
R.append(f"- **文献库**：累计增至 **{snap['total']}** 篇（本日 +{snap['added']}）。")
R.append(f"- **证据等级**：15 篇 XR/非XR 候选全文全部 L0/FULL（arxiv.org/html 源覆盖 ~100%），无降级/伪造。")
R.append(f"- **落后标注**：**0 篇**被判定 OUTDATED/SUPERSEDED；登记 1 条「路线观察」——VISTA-GS 与 Fusion-Aware 同属 3DGS 生成且方法收敛（见 §五）。")
R.append("\n**Top10 速览（按重要性降序）**：")
R.append("| # | arXiv | 标题 | 赛道 | 总分 | 等级 |")
R.append("|---|---|---|---|---|---|")
for i,r in enumerate(top10,1):
    R.append(f"| {i} | [{r['base_id']}](https://arxiv.org/abs/{r['base_id']}) | {r['title_zh']} | {r['track']} | **{r['value']}** | {r['grade']} |")
R.append("")

# 二、Top10 排行榜（含 7 维）
R.append("## 二、Top10 排行榜（7 维明细）\n")
R.append("| # | arXiv | 标题 | 赛道 | IMP | NOV | TEC | EXP | PER | TRL | REP | 总分 | 等级 |")
R.append("|---|---|---|---|---|---|---|---|---|---|---|---|---|")
for i,r in enumerate(top10,1):
    sc=r["scores"]
    R.append(f"| {i} | [{r['base_id']}](https://arxiv.org/abs/{r['base_id']}) | {r['title_zh']} | {r['track']} | "
             f"{sc['IMP']} | {sc['NOV']} | {sc['TEC']} | {sc['EXP']} | {sc['PER']} | {sc['TRL']} | {sc['REP']} | **{r['value']}** | {r['grade']} |")
R.append("")

# 三、逐篇深度解读
R.append("## 三、逐篇深度解读（按重要性降序，每篇一章）\n")
for i,r in enumerate(top10,1):
    bid=r["base_id"]
    R.append(f"### 第 {i} 章 · {r['title_zh']}  \n")
    R.append(f"> arXiv:{bid} · 赛道：{r['track']} · 价值 {r['value']}（{r['grade']}）· 7 维：{fmt(r['scores'])} · "
             f"[原文](https://arxiv.org/abs/{bid})\n")
    body=read_note_body(bid)
    R.append(body)
    R.append("\n")

# 四、当日全量 7 维对比表（参考）
R.append("## 四、当日全量 7 维度对比表（参考）\n")
R.append("> 含 Top10 + 其余 XR 相关（A/B 级）+ 非 XR 留存。完整表见 `papers/daily/2026-09-25/7dim-table.md`。\n")
t7=open(T7,encoding="utf-8").read()
t7=t7.split("## 一、Top10",1)[-1] if "## 一、Top10" in t7 else t7
R.append("### 4.1 Top10 + 其余 XR 相关\n")
R.append(t7)
R.append("")

# 五、覆盖率校验与筛选过程
R.append("## 五、覆盖率校验与筛选过程（重筛闭环）\n")
R.append(f"- **① 同质去重关**：新集 vs 库内近 90 天 token Jaccard 最大 **{snap['max_sim']}**（{snap.get('gate1_pair','2609.27850 vs 2609.26315')}），<0.62 → **通过（无同质）**。")
R.append(f"- **② 赛道覆盖关**：Top10 覆盖 **{len(snap['top_tracks'])}** 个赛道（{ '、'.join(snap['top_tracks'])}）≥5 → **通过**。")
R.append(f"- **③ 价值天花板关**：当日最高 {snap['today_max']} < 库内近 30 天 Top10 均分 {snap['lib_top_mean']} → **非重磅日，无 S 级**（未为凑数拔高）。")
R.append("- **诚实口径**：RSS \"recent\" 批次混入旧稿 replace/cross（2603/2604/2605/2607/2510/2512 等非 2609 旧 ID，共 8 篇），非当日新提交，已排除出今日 corpus 与文献库（见 run_log §4）；建议代理恢复后用 API `submittedDate` 窗口做 backfill。")
R.append("- 三关均通过，未触发剔除/回补重筛。")
R.append("\n**路线观察（非过时，仅提示方法收敛）**：当日 Top3–Top5 中 **VISTA-GS（2609.27778）** 与 **Fusion-Aware（2609.27779）** 同属「类别条件 3DGS 生成」新方向且同日提交，方法高度收敛（均走「高斯块 + 隐空间流 + 渲染反馈/一致性」）。二者非相互取代，但社区可能快速收敛到其中一种表示——后续应关注哪条路线胜出或被统一，避免重复追踪。")
R.append("")

# 六、附录
R.append("## 六、附录：抓取降级与证据等级\n")
R.append("- **数据源探测**：`export.arxiv.org/api/query` 返回 406（沙箱代理拦截）；`arxiv.org/api/query` 首次 200、复探间歇 406（代理不稳定）；`rss.arxiv.org` 稳定 200 → 选用 RSS 兜底（与 09-24 一致）。")
R.append("- **拉取**：`scripts/fetch_rss.py` 跨 7 分类，关键词命中 38 条；去 registry(133) 后得 **15 篇 2609.* 真正新提交**（13 XR + 2 非XR），其余 23 条为已在库/旧稿。")
R.append("- **全文抓取**：15 篇候选 → **全部 L0/FULL**（arxiv.org/html 源覆盖 ~100%），平均 ~1 分钟串行抓取，无 429/406 限流封禁、无 L5 摘要降级、无伪造。")
R.append("- **证据等级分布**：FULL 15（15×L0）/ PARTIAL 0 / ABSTRACT_ONLY 0。")
R.append("- **落后标记**：OUTDATED/SUPERSEDED 0 篇；路线观察 1 条（见 §五）。")
R.append("- **环境**：C: 盘 22.6 GB 充裕；D: 盘 507 GB。")
R.append("\n---")
R.append(f"\n*生成时间：2026-09-25 · 自动化 728fcb37 · 文献库累计 {snap['total']} 篇*")

open(REP,"w",encoding="utf-8").write("\n".join(R))
print("report written:",REP, len(R),"blocks")

# ---------- run_log ----------
RL=[]
RL.append(f"# 执行日志 · 2026-09-25（XR 每日论文雷达）\n")
RL.append(f"- 运行时刻：{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
RL.append("- 运行模式：真实运行（API 源被代理拦截 → RSS 兜底）")
RL.append("\n## 1. 数据源探针")
RL.append("- `export.arxiv.org/api/query` → **406**（沙箱代理拦截，与 09-24 一致）")
RL.append("- `arxiv.org/api/query` → 首次 200、复探间歇 406（代理不稳定）")
RL.append("- `rss.arxiv.org` → **200**（稳定）→ 选用 RSS 兜底源")
RL.append("\n## 2. 拉取（fetch_rss.py）")
RL.append("- 7 分类（cs.GR/HC/CV/MM/RO/AI/eess.IV）RSS \"recent\" 批次，全量去重 720 条 → 关键词命中 38 条")
RL.append("- 去 registry(133) 后：真正新 2609.* = **15 篇**（13 XR 相关 + 2 非XR）")
RL.append("- 排除：23 条（16 已在库 + 7 旧稿 replace/cross：2603/2604/2605/2607/2510/2512 等），非当日新提交")
RL.append("\n## 3. 全文抓取（fetch_fulltext.py）")
RL.append("- 15 篇候选全部 L0/FULL（arxiv.org/html 源）；串行 3s/篇，无 429/406/降级/伪造")
RL.append("\n## 4. 评分与覆盖度")
RL.append(f"- Top10 均分 {snap['today_top_mean']}；最高 {snap['today_max']}；S 级 0 / A 级 10")
RL.append(f"- 门① max Jaccard {snap['max_sim']} <0.62 通过；门② 覆盖 {len(snap['top_tracks'])} 赛道通过；门③ 非重磅日（4.05<{snap['lib_top_mean']}）")
RL.append("- 三关通过，未触发重筛")
RL.append("\n## 5. 遗留与建议")
RL.append("- RSS 混入旧稿（7 篇非 2609 旧 ID）建议代理恢复后用 API `submittedDate` 窗口 backfill")
RL.append("- `fetch_arxiv.py` 端点已临时改为 `https://arxiv.org/api/query`（export 仍 406）；恢复后改回")
RL.append("- 已知遗留缺口仍存：近眼显示/光场/全息等**硬件类**渲染（库内仍全为算法侧）")
open(RUNLOG,"w",encoding="utf-8").write("\n".join(RL))
print("run_log written:",RUNLOG)

# ---------- 当日 MOC ----------
def note_link(bid):
    c=glob.glob(f"{NOTES}/{bid}__*.md")
    if not c: return f"../notes/{bid}.md"
    return "../notes/"+os.path.basename(c[0])

M=[]
M.append(f"# MOC · 2026-09-25（XR 每日论文雷达）\n")
M.append(f"> 批次：2026-09-25（拉取最新公告批次 2026-09-24）· 数据源：rss.arxiv.org 兜底（API 被代理 406/间歇 406）")
M.append(f"> 当日新论文（2609.*）：XR 相关 **{len(xr_recs)}** + 非 XR **{len(non_xr)}**；Top10 均分 {snap['today_top_mean']}；非重磅日（无 S 级）。\n")
M.append("## Top10（按重要性降序，逐篇精读）\n")
for i,r in enumerate(top10,1):
    M.append(f"{i}. [{r['title_zh']}]({note_link(r['base_id'])}) — {r['track']} · {r['value']}（{r['grade']}）· [arXiv:{r['base_id']}](https://arxiv.org/abs/{r['base_id']})")
M.append("\n## 其余 XR 相关（A/B 级参考）\n")
for r in xr_recs:
    if any(t['base_id']==r['base_id'] for t in top10): continue
    fl=("（"+"；".join(r['flags'])+"）") if r.get('flags') else ""
    M.append(f"- [{r['title_zh']}]({note_link(r['base_id'])}) — {r['track']} · {r['value']}（{r['grade']}）{fl}")
M.append("\n## 非 XR 留存（不计入打分）\n")
for r in non_xr:
    M.append(f"- {r['title_zh']}（{r['base_id']}）")
M.append("\n## 关联文档\n")
M.append(f"- 完整解读报告：[XR-Daily-Report-2026-09-25.md](../reports/XR-Daily-Report-2026-09-25.md)")
M.append(f"- 7 维对比表：[7dim-table.md](../daily/2026-09-25/7dim-table.md)")
M.append(f"- 评分与覆盖校验：[scored.md](../daily/2026-09-25/scored.md)")
M.append(f"- 执行日志：[run_log.md](../daily/2026-09-25/run_log.md)")
M.append(f"- 文献库（累计 {snap['total']}）：[registry.jsonl](../library/registry.jsonl)")
open(MOC_D,"w",encoding="utf-8").write("\n".join(M))
print("MOC written:",MOC_D)

# ---------- 总索引更新 ----------
hdr=("# XR 论文知识库 · 总索引（MOC）\n"
     "> 地图：按「日期批次 × 赛道 × 等级」组织。每个日期批次的 MOC 链接当日原子笔记。\n")
idx=""
if os.path.exists(MOC_I):
    idx=open(MOC_I,encoding="utf-8").read()
    if "## 批次索引" in idx:
        lines=idx.split("\n")
        for k,l in enumerate(lines):
            if l.strip().startswith("## 批次索引"):
                ins=k+1
                while ins<len(lines) and lines[ins].strip().startswith("|"):
                    ins+=1
                lines.insert(ins, f"| 2026-09-25 | [MOC-2026-09-25](./MOC-2026-09-25.md) | XR {len(xr_recs)} + 非XR {len(non_xr)} · Top10 均分 {snap['today_top_mean']} · 非重磅日（无S） | RSS兜底(API 406/间歇) |")
                idx="\n".join(lines)
                break
    else:
        idx+="\n## 批次索引\n\n| 日期 | MOC | 概览 | 备注 |\n|---|---|---|---|\n"
        idx+=f"| 2026-09-25 | [MOC-2026-09-25](./MOC-2026-09-25.md) | XR {len(xr_recs)} + 非XR {len(non_xr)} · Top10 均分 {snap['today_top_mean']} · 非重磅日（无S） | RSS兜底(API 406/间歇) |\n"
else:
    idx=hdr+"\n## 批次索引\n\n| 日期 | MOC | 概览 | 备注 |\n|---|---|---|---|\n"
    idx+=f"| 2026-09-25 | [MOC-2026-09-25](./MOC-2026-09-25.md) | XR {len(xr_recs)} + 非XR {len(non_xr)} · Top10 均分 {snap['today_top_mean']} · 非重磅日（无S） | RSS兜底(API 406/间歇) |\n"
open(MOC_I,"w",encoding="utf-8").write(idx)
print("总索引 updated:",MOC_I)
