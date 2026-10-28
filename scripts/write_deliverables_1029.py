# -*- coding: utf-8 -*-
"""2026-10-29 产物生成：主批（10-28 公告批次 19 篇 + ParetoGS 补录 1 篇）+ backfill-1029（旧稿 replace 再公告 4 篇）。
消费 data/scored_1029.json；registry 幂等追加（先备份，in_top10 按定稿 Top10 显式设置）；
生成 7 维表/scored/run_log/笔记/MOC/报告并刷新总索引。"""
import json, os, shutil, glob

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
os.chdir(ROOT)
D = json.load(open('data/scored_1029.json', encoding='utf-8'))
MAIN, BF = D['main'], D['backfill']
TOP10_IDS = set(D['top10_ids'])
DATE, BFB = '2026-10-29', 'backfill-1029'
GATE3 = 4.417          # 门③ 现算均分（窗口 2026-09-29~10-29，435 条入窗）
TODAY_MAX = MAIN[0]['value']  # 4.30
TOP10 = [p for p in MAIN if p['id'] in TOP10_IDS]

def esc(s):
    return str(s).replace('|', '/')

def dim_row(p, star):
    s = p['scores']
    return (f"| {p['id']} | {esc(p['title_zh'])} {'⭐' if star else ''} | {p['track']} | "
            f"{s['IMP']} | {s['NOV']} | {s['TEC']} | {s['EXP']} | {s['PER']} | {s['TRL']} | {s['REP']} | "
            f"{p['value']:.2f} | {p['grade']} | {p['evidence']} | {p['announce']} |")

TBL_HEAD = ('| arXiv | 标题 | 赛道 | IMP | NOV | TEC | EXP | PER | TRL | REP | 总分 | 等级 | 证据 | 公告类型 |\n'
            '|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|\n')

# ---------- 1. 7 维表 ----------
def seven_table(papers, path, title, intro, topn):
    lines = [f'# {title}\n', intro + '\n', TBL_HEAD]
    for i, p in enumerate(papers):
        lines.append(dim_row(p, p['id'] in TOP10_IDS) + '\n')
    open(path, 'w', encoding='utf-8').writelines(lines)

os.makedirs(f'papers/daily/{DATE}', exist_ok=True)
os.makedirs(f'papers/daily/{BFB}', exist_ok=True)

seven_table(MAIN, f'papers/daily/{DATE}/7dim-table.md',
    f'{DATE} 全量 7 维度对比表（参考）',
    '批次：2026-10-29（**2026-10-28（周三）公告批次**；公告日 10-28 ≠ 拉取日 10-29 02:30，诚实口径）。\n'
    '候选池 20 篇：listing 对账 10-28 公告组 462 篇 → 摘要级 XR 命中 33 篇；RSS 7 分类去重 714 → KW 命中 48 = **33 篇 2610.* 真新提交（10-28 公告组）+ 14 篇旧稿 replace/cross 再公告 + 1 篇库内 v2 再公告**；listing 摘要级 33 篇全部被 RSS 覆盖（**RSS 漏网 0 篇**，两渠道互证）。33 篇真新中甄别 XR 核心/强相关 **19 篇**入评分池，剔非 XR 14 篇（RL 可塑性/水下声呐/四足姿态/人形迁移/ViT 骨干/视觉 AR 生成/机器人主动感知/无人机主动 SLAM/医学 CT 烘焙/跨本体 VLA/卫星 NVS/机械拇指/网球时空/视觉生成范式）。\n'
    '另：**ParetoGS（2610.34235）为 10-27 公告批次补录**——10-28 运行曾入候选池并 digest，但候选→评分环节静默丢失未入馆；10-29 listing 对账重新发现（上批 15 篇摘要级未入馆命中之一），补入本批并诚实标注。\n'
    'RSS 同批另混入 14 篇旧稿 replace/cross 再公告（4 篇 XR → backfill-1029）+ 1 篇库内 v2 再公告剔除。\n'
    '全文：20 篇候选 **19 篇 L0/FULL + 1 篇 L1/PARTIAL**（2610.36014 Immersive Commons：ar5iv 仅摘要页 4,706 字符，按摘要级评估并显式声明）；先抓全文再定稿。\n'
    '覆盖度三关：门① 最大 Jaccard **0.308**（2610.36760 GeoGSplat vs 库内 2610.31293，<0.62 通过）；门② 纯值 Top10 仅覆盖 4 赛道，按重筛闭环剔除重复赛道最低分 SG²SLAM（4.00，重建与SLAM 第 4 篇）、回补未覆盖赛道最高分 SOMA（3.79，评估与数据集）→ **定稿 Top10 覆盖 5 赛道**（重建与SLAM×3/渲染与显示×3/神经渲染×2/内容生成×1/评估与数据集×1，≥5 通过）；门③ 当日最高 **4.30 < 库内近 30 天 Top10 均分 4.417**（435 条入窗，现算）→ **非重磅日、无 S 级**，未拔高。RESPLE2 4.30 / GraftRay 4.20 达 S 线按校准关记 A（同 10-24 EgoHand / 10-27 WFM / 10-28 RacerGS 先例）。',
    len(TOP10))

seven_table(BF, f'papers/daily/{BFB}/7dim-table.md',
    f'{BFB} 全量 7 维度对比表（参考）',
    '批次：backfill-1029（**10-28 公告批次中 RSS 混入的旧稿 replace/cross 再公告**（首次入馆；原始投稿 2508=2025-08 / 2510=2025-10 / 2604=2026-04 / 2605=2026-05）；均非 10-28 当日新提交，诚实口径单独编号）。\n'
    '候选 4 篇：2510.01767 LoBE-GS（负载均衡大规模 3DGS 训练）/ 2604.23018 AmaraSpatial-10K（空间计算 3D 资产数据集）/ 2605.31466 VolFill（体素流匹配 amodal 重建）/ 2508.04236 PIS3R（深度 3D 重建超大视差拼接）。全部 L0/FULL 全文后定稿。\n'
    '门③ 对 backfill 不适用；本批不参与当日「重磅日」判定。门① 最大 Jaccard 0.143（PIS3R vs 库内，<0.62 通过）；门② 覆盖 4 赛道（系统与平台/评估与数据集/重建与SLAM×2；4 篇低量批次实际上限）。\n'
    '注：本批 4 篇均未达 S 线（最高 LoBE-GS 3.73），按实数定级。',
    len(BF))

# ---------- 2. scored.md + run_log.md ----------
def scored_md(papers, path, title, extra):
    L = [f'# {title}\n', extra + '\n', '| 排名 | arXiv | 标题 | 赛道 | 总分 | 等级 | 证据 | 公告类型 |',
         '|---|---|---|---|---|---|---|---|']
    for i, p in enumerate(papers, 1):
        L.append(f"| {i} | {p['id']} | {esc(p['title_zh'])} | {p['track']} | {p['value']:.2f} | {p['grade']} | {p['evidence']} | {p['announce']} |")
    open(path, 'w', encoding='utf-8').writelines([x + '\n' for x in L])

scored_md(MAIN, f'papers/daily/{DATE}/scored.md', f'{DATE} 评分明细',
    '评分口径：7 维加权 IMP0.20·NOV0.20·TEC0.15·EXP0.15·PER0.15·TRL0.08·REP0.07；分档 S≥4.2 / A3.6–4.2 / B3.0–3.6 / C<3.0。全部基于全文证据定稿（2610.36014 为 L1 ar5iv 摘要级，显式声明）。\n'
    f'覆盖度三关：门① 最大 Jaccard 0.308 < 0.62（通过，非同质）；门② 定稿 Top10 覆盖 5 赛道 ≥ 5（通过；纯值 Top10 仅 4 赛道，按重筛闭环以 SOMA 3.79 回补替换 SG²SLAM 4.00）；门③ 当日最高 4.30 < 库内近 30 天 Top10 均分 4.417（现算，435 条入窗）→ 非重磅日、无 S 级（校准关，不触发重筛；RESPLE2 4.30 / GraftRay 4.20 达 S 线按校准关记 A）。\n'
    'OUTDATED/SUPERSEDED 0 篇。等级分布：14 A / 4 B / 2 C。')
scored_md(BF, f'papers/daily/{BFB}/scored.md', f'{BFB} 评分明细',
    '评分口径同上。本批为旧稿 replace/cross 再公告首次入馆（非当日新提交），门③ 不适用。\n'
    '门① 最大 Jaccard 0.143 < 0.62（通过）；门② 覆盖 4 赛道（4 篇低量批次实际上限）；OUTDATED/SUPERSEDED 0 篇。等级分布：3 A / 1 B。')

run_log_main = f'''# {DATE} 执行日志

## 数据源与对账（第 1-3 步）
- **漏网对账（先于拉取）**：`scripts/audit_gap_listing.py`（TARGET_LO=2026-10-27，上一批次公告日）7 分类采集，完整性校验全过。listing 最新公告日 = **2026-10-28**（10-26 组复采一致；10-27 组 794 篇与上批一致）。**10-28 组 462 篇全部未入馆**（新公告批次）；10-27 组 768 篇未入馆者摘要级复核：15 篇命中均为 10-28 运行已显式剔除的非 XR 稿 → **0 漏网**（其中 2610.34235 ParetoGS 例外：上批候选→评分环节静默丢失，本批作补录处理，见下）。
- **摘要级 XR 过滤**：`scripts/filter_missed_xr_abstract.py`（MIN_DAY=2026-10-27）→ 1,230 篇取回 1,230 条 API 元数据，XR 命中 **48 篇**（10-27 组 15 + 10-28 组 33）。
- **RSS 主渠道交叉验证**：`scripts/fetch_rss.py` 7 分类全量去重 714 条 → KW 命中 48 = **33 篇 2610.* 真新提交（10-28 公告组）+ 14 篇旧稿 replace/cross 再公告 + 1 篇库内 v2 再公告**。listing 摘要级 33 篇（10-28 组）**全部被 RSS 覆盖，RSS 漏网 0 篇**——两渠道互证。
- **API 探针**：export.arxiv.org / arxiv.org/api/query 均可达（200）；`submittedDate` 前沿推进到 10-27（`fetch_arxiv.py --since 2026-10-27` 回 20 条，全部归属 listing 10-28 公告组，证实「10-27 提交→10-28 公告」的 arXiv 节律）；真实新增由 RSS+listing 双渠道获得。

## 甄别（第 3 步）
- 主批 XR 核心/强相关 **20 篇**入评分池 = 10-28 公告组甄别 **19 篇** + **ParetoGS 补录 1 篇**；剔非 XR **14 篇**（2610.36309 RL 可塑性 / 2610.36454 水下声呐 / 2610.36599 四足姿态 / 2610.36615 人形交互迁移 / 2610.36719 ViT 骨干 / 2610.36793 视觉 AR 生成 / 2610.36859 机器人主动感知 / 2610.37111 无人机主动 SLAM / 2610.37406 医学 CT 烘焙 / 2610.37509 跨本体 VLA / 2610.37545 卫星 NVS / 2610.37582 机械拇指 / 2610.37619 网球时空 / 2610.37626 视觉生成范式）。
- **补录说明（诚实口径）**：2610.34235 ParetoGS 属 10-27 公告批次，10-28 运行曾入候选池（candidates_1028.json main 27 篇）并完成 digest，但候选→评分环节静默丢失（scored main 仅 26 篇、未入馆、上批 run_log 剔除清单亦未列）；10-29 listing 对账的摘要级复核重新发现。本批将其补入评分池，7 维表「公告类型」列标「补录」，绝不伪装为 10-28 公告批次新提交。
- 旧稿 replace/cross 再公告 14 篇中 **4 篇 XR → backfill-1029**（首次入馆，单独编号）；10 篇非 XR 剔除（2506.19846 智能体记忆基准 / 2601.01535 图像 tokenizer / 2605.29927 规划实证 / 2605.31217 航天器位姿 / 2609.14087 可达性理论 / 2610.32259 ARAIM GNSS/IMU / 2510.04883 红外主动重建 / 2610.09857 机器人操作定位 / 2610.25459 双手操作基准 等）。
- 库内 v2 再公告 1 篇剔除（2610.35554 Insta360 SfM，10-27 批已入馆）。

## 全文抓取（第 4 步）
- 24 篇候选（主批 20 + backfill 4）跑 `scripts/fetch_fulltext.py`，严格串行 3s/篇（约 1 分 36 秒）：**23 篇 L0/FULL**（25,273–146,381 字符）+ **1 篇 L1/PARTIAL**（2610.36014 Immersive Commons：ar5iv 仅摘要页 4,706 字符 → 按摘要级评估并在 7 维表/笔记/报告显式声明，禁止脑补）。无限流/降级/伪造。
- manifest 合并写入校验通过；WROTE=24>0。

## 评分与三关（第 5-6 步）
- 先抓全文再定稿。7 维加权定稿：主批 14 A / 4 B / 2 C（最高 4.30 RESPLE2，RESPLE2 4.30 与 GraftRay 4.20 达 S 线）；backfill 3 A / 1 B（最高 LoBE-GS 3.73）。
- 门① 最大 Jaccard **0.308**（2610.36760 GeoGSplat vs 库内 2610.31293；<0.62，非同质）。
- 门② 纯值 Top10 仅覆盖 **4 赛道**（重建与SLAM×4/渲染与显示×3/神经渲染×2/内容生成×1）→ 触发一次回补：剔除重复赛道中最低分者 SG²SLAM（4.00，重建与SLAM 第 4 篇），回补未覆盖赛道最高分 SOMA（3.79，评估与数据集）→ **定稿 Top10 覆盖 5 赛道**（重建与SLAM×3/渲染与显示×3/神经渲染×2/内容生成×1/评估与数据集×1），通过。SG²SLAM 仍入馆并写笔记（A 级），仅不占 Top10 名额。
- 门③ 当日最高 **4.30 < 库内近 30 天 Top10 均分 4.417**（窗口 2026-09-29~10-29、435 条入窗、现算）→ **非重磅日、无 S 级**；RESPLE2 4.30 / GraftRay 4.20 达 S 线按校准关记 A（同 10-24 EgoHand / 10-27 WFM / 10-28 RacerGS 先例）。三关全过，**未触发重筛**（门② 的回补即重筛闭环动作）。
- OUTDATED/SUPERSEDED **0 篇**。路线级观察：① 3DGS 前沿重建三箭齐发（LingGS 显式几何跟踪 / SG²SLAM chunk 度量先验 / StereoSplat 立体原生），「学习相机头 vs 显式求解器」路线竞争白热化；② 3DGS 压缩/预算线再添正交分支（ParetoGS 连续预算 + LoBE-GS 负载均衡训练）；③ VR 感知科学化（DomeGS 36 人用户研究 + TSAE 团队沟通度量），XR 评测从任务指标走向感知/社会维度。

## 产物（第 7-8 步）
- 报告 2 份（主报告 + backfill 报告）+ 原子笔记 22 篇（grade≥B；2 篇 C 级仅入馆不解读）+ MOC 2 份 + 总索引刷新 + 7 维表/scored/run_log 各 2 套。
- registry 669 → **693**（+19 主批新稿 +1 补录 +4 backfill；备份 `papers/library/registry.jsonl.bak-20261029`；按 base_id 幂等）。
'''
open(f'papers/daily/{DATE}/run_log.md', 'w', encoding='utf-8').write(run_log_main)

run_log_bf = f'''# {BFB} 执行日志

- **批次性质**：backfill（非当日新提交）——10-28 公告批次中 RSS 混入的旧稿 replace/cross 再公告 4 篇首次入馆；原始投稿 2508=2025-08 / 2510=2025-10 / 2604=2026-04 / 2605=2026-05（arXiv ID 前缀 2508/2510/2604/2605）。
- **来源**：`scripts/fetch_rss.py` 7 分类全量去重 714 → KW 命中 48；其中 14 篇旧稿再公告经 XR 甄别保留 4 篇（剔非 XR 10 篇：智能体记忆基准/图像 tokenizer/规划实证/航天器位姿/可达性理论/ARAIM/红外主动重建/机器人操作定位/双手操作基准 等）。
- **全文**：4 篇全部 L0/FULL（52,679–105,670 字符），串行 3s/篇，无限流/降级/伪造。
- **评分**：3 A / 1 B（最高 LoBE-GS 3.73，无 S 线）。门① max Jaccard 0.143 < 0.62；门② 覆盖 4 赛道（4 篇低量批次实际上限）；门③ 不适用；OUTDATED 0。
- **诚实口径**：全部条目 `batch=backfill-1029` + `orig_window` 标注，绝不混入「当日新论文」。
'''
open(f'papers/daily/{BFB}/run_log.md', 'w', encoding='utf-8').write(run_log_bf)

# ---------- 3. registry（先备份，幂等追加，in_top10 显式） ----------
reg_path = 'papers/library/registry.jsonl'
shutil.copy(reg_path, reg_path.replace('.jsonl', '.bak-20261029'))
rows = [json.loads(l) for l in open(reg_path, encoding='utf-8') if l.strip()]
have = {r['id'].split(':')[-1].split('v')[0] for r in rows}
added = 0
with open(reg_path, 'a', encoding='utf-8') as f:
    for p in MAIN + BF:
        if p['id'] in have:
            continue
        entry = dict(id=f"arXiv:{p['id']}", title=p['title'], title_zh=p['title_zh'],
                     track=p['track'], date=(DATE if p in MAIN else '2026-10-28'),
                     value=p['value'], grade=p['grade'], scores=p['scores'],
                     status=p['status'], evidence=p['evidence'], fetch_level=p['level'],
                     fulltext_chars=0, in_top10=(p['id'] in TOP10_IDS), batch=p['batch'],
                     announce_type=p['announce'], flags=[])
        if p.get('orig_window'):
            entry['orig_window'] = p['orig_window']
        if p in BF:
            entry['in_top10'] = False
        f.write(json.dumps(entry, ensure_ascii=False) + '\n')
        added += 1
print(f'registry +{added}（现有 {len(rows)+added}）')

# ---------- 4. 原子笔记（grade≥B；C 级仅入馆） ----------
def slugify(t):
    import re
    s = re.sub(r'[^a-z0-9]+', '-', t.lower()).strip('-')
    return s[:48]

NOTE_TMPL = '''---
id: arXiv:{id}
title: {title}
title_zh: {title_zh}
track: {track}
venue: {venue}
date: {date}
value: {value}
grade: {grade}
evidence: {evidence}
status: {status}
superseded_by: []
scores: {{IMP:{IMP}, NOV:{NOV}, TEC:{TEC}, EXP:{EXP}, PER:{PER}, TRL:{TRL}, REP:{REP}}}
fetch_level: {level}
batch: {batch}
announce_type: {announce}
in_top10: {in_top10}
tags: [{tags}]
---

# {title_zh}

## 一句话结论
{conclusion}

## 要解决的问题
{problem}

## 方法详解
{method}

## 实验与结果
{experiments}

## 创新点与贡献
{innovation}

## 局限与风险
{limits}

## 与文献库的关系
{relation}

## 可复现性（代码/数据/硬件）
{repro}

## 行动建议
{action}
'''
os.makedirs('papers/notes', exist_ok=True)
n_notes = 0
for p in MAIN + BF:
    if p['grade'] == 'C':
        continue
    fn = f"papers/notes/{p['id']}__{slugify(p['title'])}.md"
    if os.path.exists(fn):
        continue
    body = NOTE_TMPL.format(
        id=p['id'], title=p['title'], title_zh=p['title_zh'], track=p['track'], venue=p['venue'],
        date=(DATE if p in MAIN else '2026-10-28'), value=f"{p['value']:.2f}", grade=p['grade'],
        evidence=p['evidence'], status=p['status'],
        IMP=p['scores']['IMP'], NOV=p['scores']['NOV'], TEC=p['scores']['TEC'], EXP=p['scores']['EXP'],
        PER=p['scores']['PER'], TRL=p['scores']['TRL'], REP=p['scores']['REP'],
        level=p['level'], batch=p['batch'], announce=p['announce'],
        in_top10=('true' if p['id'] in TOP10_IDS else 'false'),
        tags=', '.join(p['tags']), conclusion=p['conclusion'], problem=p['problem'],
        method=p['method'], experiments=p['experiments'], innovation=p['innovation'],
        limits=p['limits'], relation=p['relation'], repro=p['repro'], action=p['action'])
    open(fn, 'w', encoding='utf-8').write(body)
    n_notes += 1
print('notes written:', n_notes)

# ---------- 5. 当日 MOC ----------
def moc(papers, path, title, intro):
    L = [f'# {title}\n', intro + '\n', '## 本批论文（按加权降序）\n',
         '| # | 论文 | 赛道 | 总分 | 等级 | 证据 | 笔记 |', '|---|---|---|---|---|---|---|']
    for i, p in enumerate(papers, 1):
        note = glob.glob(f"papers/notes/{p['id']}__*")
        link = f"[→](../notes/{os.path.basename(note[0])})" if note else '→'
        L.append(f"| {i} | {esc(p['title_zh'])} | {p['track']} | {p['value']:.2f} | {p['grade']} | {p['evidence']} | {link} |")
    L += ['\n## 批次要点\n']
    for p in papers:
        L.append(f"- **{esc(p['title_zh'])}**（{p['id']}，{p['value']:.2f} {p['grade']}）：{p['conclusion']}")
    open(path, 'w', encoding='utf-8').writelines([x + '\n' for x in L])

moc(MAIN, f'papers/MOC/MOC-{DATE}.md', f'MOC · {DATE}（10-28 公告批次）',
    '> 当日地图：**公告日 2026-10-28（周三）≠ 拉取日 2026-10-29（周四 02:30）**——诚实口径，非当日硬提交。\n'
    '> 主批 XR 新稿 20 篇（14 A / 4 B / 2 C，无 S——非重磅日）= 10-28 公告组甄别 19 篇 + ParetoGS 补录 1 篇（10-27 公告批次，上批候选→评分环节静默丢失，今日 listing 对账补回）；listing 与 RSS 两渠道互证 33 篇真新提交中 19 篇 XR；全文 19 L0/FULL + 1 L1 摘要级。\n'
    '> 覆盖度三关：门① 0.308 / 门② 定稿 Top10 5 赛道（纯值 Top10 仅 4 赛道，按重筛闭环以 SOMA 3.79 回补替换 SG²SLAM 4.00）/ 门③ 4.30 < 4.417（现算）→ 非重磅日无 S；RESPLE2 4.30 / GraftRay 4.20 达 S 线按校准关记 A。Top10 实数 10 篇。')
moc(BF, f'papers/MOC/MOC-{BFB}.md', f'MOC · {BFB}（旧稿再公告补录）',
    '> 本批为 **backfill**：10-28 公告批次 RSS 混入的旧稿 replace/cross 再公告 4 篇首次入馆（原始投稿 2508/2510/2604/2605），**均非当日新提交**。\n'
    '> 3 A / 1 B；最高 LoBE-GS 3.73（无 S 线）。门① 0.143 / 门② 4 赛道（4 篇低量批次实际上限）/ 门③ 不适用。')

# ---------- 6. 报告 ----------
def report(papers, path, title, header, batch_label, topn):
    L = [f'# {title}\n', header + '\n', '## 二、排行榜（按加权降序）\n',
         '| 排名 | 论文 | 赛道 | 总分 | 等级 | 证据 | 落后标记 |', '|---|---|---|---|---|---|---|']
    for i, p in enumerate(papers[:topn], 1):
        mark = '⛔ OUTDATED' if p['status'] != 'CURRENT' else '—'
        L.append(f"| {i} | {esc(p['title_zh'])}（{p['id']}） | {p['track']} | {p['value']:.2f} | {p['grade']} | {p['evidence']} | {mark} |")
    L.append('\n## 三、逐篇深度解读\n')
    for i, p in enumerate(papers[:topn], 1):
        L.append(f"### 第 {i} 章 · {esc(p['title_zh'])}（{p['id']}，{p['value']:.2f} {p['grade']}，{p['evidence']}）\n")
        L.append(f"- **赛道 / 场合**：{p['track']} / {p['venue']}")
        L.append(f"- **公告类型**：{p['announce']}" + (f"（{p['orig_window']}）" if p.get('orig_window') else ''))
        if p.get('grade_note'):
            L.append(f"- **等级说明**：{p['grade_note']}")
        L.append(f"- **一句话结论**：{p['conclusion']}")
        L.append(f"- **要解决的问题**：{p['problem']}")
        L.append(f"- **方法详解**：{p['method']}")
        L.append(f"- **实验与结果**：{p['experiments']}")
        L.append(f"- **创新点与贡献**：{p['innovation']}")
        L.append(f"- **局限与风险**：{p['limits']}")
        L.append(f"- **与文献库的关系**：{p['relation']}")
        L.append(f"- **可复现性**：{p['repro']}")
        L.append(f"- **行动建议**：{p['action']}\n")
    L.append('## 四、当日全量 7 维度对比表（参考）\n')
    L.append(f'见 [`papers/daily/{batch_label}/7dim-table.md`](../papers/daily/{batch_label}/7dim-table.md)。\n')
    L.append('## 五、覆盖率校验与筛选过程说明\n')
    L.append('- 门①（同质去重）：最大 Jaccard 0.308 < 0.62，通过，无同质重复。')
    L.append('- 门②（赛道覆盖）：纯值 Top10 仅覆盖 4 赛道 → 按重筛闭环剔除重复赛道最低分 SG²SLAM（4.00，重建与SLAM 第 4 篇），回补未覆盖赛道最高分 SOMA（3.79，评估与数据集）→ 定稿 Top10 覆盖 5 赛道（≥5），通过；SG²SLAM 仍入馆并写笔记（A 级），仅不占 Top10 名额。')
    L.append('- 门③（价值天花板）：当日最高分 4.30 < 库内近 30 天 Top10 均分 4.417（现算，435 条入窗）→ 非重磅日、无 S 级，未拔高、未凑数；达 S 线的 RESPLE2 4.30 / GraftRay 4.20 按校准关记 A。')
    L.append('- 三关均未触发重筛（门② 的回补即重筛闭环动作）；OUTDATED/SUPERSEDED 0 篇。\n')
    L.append('## 六、附录：证据等级分布与抓取记录\n')
    nf = sum(1 for p in papers if p['evidence'] == 'FULL')
    L.append(f'- FULL {nf} 篇；PARTIAL 1 篇；ABSTRACT_ONLY 0 篇（2610.36014 Immersive Commons 为 L1 ar5iv 仅摘要页 4,706 字符，已在 7 维表与笔记显式声明并按摘要级评估）。')
    L.append('- 抓取降级：无 L5；无 OCR；无伪造。串行 3s/篇，无限流。')
    open(path, 'w', encoding='utf-8').writelines([x + '\n' for x in L])

report(TOP10 + [p for p in MAIN if p['id'] not in TOP10_IDS][:0] or TOP10,
       f'reports/XR-Daily-Report-{DATE}.md',
       f'XR 每日论文解读报告 · {DATE}（10-28 公告批次）',
       '## 一、执行摘要\n'
       f'- **公告日 2026-10-28（周三）≠ 拉取日 2026-10-29（周四 02:30）**——诚实口径：本批处理的是 10-28 公告批次，非当日硬提交。\n'
       '- **主批 XR 新稿 20 篇（14 A / 4 B / 2 C，无 S 级）** = 10-28 公告组甄别 19 篇 + **ParetoGS 补录 1 篇**（10-27 公告批次，上批候选→评分环节静默丢失，今日 listing 对账补回，诚实标注）。Top10：RESPLE2 4.30（多传感器里程计，非均匀 B 样条+IMU 精确预测）· GraftRay 4.20（路径追踪物理一致高斯场景网格插入）· LingGS 4.15（几何求解器取代学习相机头的高斯 SLAM）· StereoSplat 4.07（立体原生前馈 3DGS，AbsRel 0.04）· HoloRecon 4.07（前馈几何验证的长程全景重建）· DomeGS 4.00（VR 无界 3DGS 背景补全，36 人用户研究）· GeoGSplat 4.00（几何接地非像素对齐 3DGS）· PrinGS 3.92（3DGS 后训练隐私匿名化）· ParetoGS 3.85（连续预算 3DGS，补录）· SOMA 3.79（第一视角人体运动理解基准，门②回补）。\n'
       '- **覆盖 5 赛道**：重建与SLAM / 渲染与显示 / 神经渲染 / 内容生成 / 评估与数据集。\n'
       '- **覆盖度三关**：门① 0.308；门② 纯值 Top10 仅 4 赛道 → 回补后 5 赛道；门③ 4.30 < 4.417（现算）→ **非重磅日、无 S 级**；RESPLE2 4.30 / GraftRay 4.20 达 S 线按校准关记 A。\n'
       '- **全文证据**：19 篇 L0/FULL + 1 篇 L1 摘要级（2610.36014，ar5iv 仅摘要页）。\n'
       '- **同批 backfill-1029**：RSS 混入旧稿 replace/cross 再公告 4 篇首次入馆（3 A / 1 B，最高 LoBE-GS 3.73），详见 [XR-Backfill-Report-backfill-1029.md](XR-Backfill-Report-backfill-1029.md)。',
       DATE, 10)

report(BF, f'reports/XR-Backfill-Report-{BFB}.md',
       f'XR Backfill 补录报告 · {BFB}（旧稿再公告）',
       '## 一、执行摘要\n'
       '- **批次性质**：backfill（非当日新提交）——10-28 公告批次中 RSS 混入的旧稿 replace/cross 再公告 4 篇，首次入馆；原始投稿 2508=2025-08 / 2510=2025-10 / 2604=2026-04 / 2605=2026-05。\n'
       '- **补录 4 篇（3 A / 1 B）**：LoBE-GS 3.73（NTHU+NVIDIA，负载均衡大规模 3DGS 训练，端到端约 2.9×）· AmaraSpatial-10K 3.67（10,071 个度量锚定 3D 资产，CLIP R@5 3.4×）· VolFill 3.65（UMass Amherst，体素流匹配 amodal 重建，SCRREAM CD 3.03）· PIS3R 3.58（VGGT 深度重建的超大视差拼接，Sampson 误差约 3.1×）。\n'
       '- **覆盖 4 赛道**；门① 0.143；门③ 对 backfill 不适用；OUTDATED 0。\n'
       '- **诚实口径**：全部条目 `batch=backfill-1029` + `orig_window` 标注，绝不混入「当日新论文」。',
       BFB, 10)

# ---------- 7. MOC-总索引刷新 ----------
moc_path = 'papers/MOC/MOC-总索引.md'
h = open(moc_path, encoding='utf-8').read()

# 7.1 头部计数与批次列表
h = h.replace('文献库：`papers/library/registry.jsonl`（累计 **669 篇**；跨度 2026-09-15 ~ 2026-10-27',
              '文献库：`papers/library/registry.jsonl`（累计 **693 篇**；跨度 2026-09-15 ~ 2026-10-28')
h = h.replace('**backfill-1028:10（10-27 公告 RSS 混入旧稿 replace/cross 再公告，首次入馆）**；',
              '**backfill-1028:10（10-27 公告 RSS 混入旧稿 replace/cross 再公告，首次入馆）** · **2026-10-29:20（10-28 公告批次真新提交 19 + ParetoGS 补录 1，非重磅日无S；listing+RSS 两渠道互证 33 篇中 19 篇 XR）** · **backfill-1029:4（10-28 公告 RSS 混入旧稿 replace/cross 再公告，首次入馆）**；')
h = h.replace('**10-28 周三处理 10-27 公告批次（26 篇 XR 新稿 18A/6B/2C + backfill-1028 补录 10 篇 9A/1B，非重磅日无S）**。',
              '**10-28 周三处理 10-27 公告批次（26 篇 XR 新稿 18A/6B/2C + backfill-1028 补录 10 篇 9A/1B，非重磅日无S）**；**10-29 周四处理 10-28 公告批次（19 篇 XR 新稿 + ParetoGS 补录 1 = 20 篇 14A/4B/2C + backfill-1029 补录 4 篇 3A/1B，非重磅日无S）**。')

# 7.2 追加 10-29 状态注记（在 10-28 注记后）
note29 = ('> **状态注记（2026-10-29）**：周四 02:30，处理 **2026-10-28（周三）公告批次**（公告日≠拉取日，诚实口径）。'
 '漏网对账（TARGET_LO=10-27）：listing 7 分类最新公告日 **10-28**（10-27 组 794 篇复采一致）；**10-28 组 462 篇全部未入馆**，摘要级 XR 命中 33 篇；10-27 组未入馆 768 篇摘要级复核 15 篇命中均为上批已剔非 XR（0 漏网），**唯一例外 2610.34235 ParetoGS 为上批候选→评分环节静默丢失**（candidates 27→scored 26），本批作补录处理并诚实标注。'
 'RSS 7 分类去重 714 → KW 命中 48 = **33 篇 2610.* 真新提交 + 14 篇旧稿 replace/cross 再公告 + 1 篇库内 v2 再公告**；listing 摘要级 33 篇全部被 RSS 覆盖（**RSS 漏网 0 篇**，两渠道互证）。API 双源 200、submittedDate 前沿推进到 10-27（20 条全部归属 10-28 公告组，证实 10-27 提交→10-28 公告节律）。'
 '主批甄别 **XR 核心/强相关 20 篇**（10-28 组 19 + 补录 1；剔非 XR 14 篇：RL 可塑性/水下声呐/四足姿态/人形迁移/ViT 骨干/视觉 AR 生成/机器人主动感知/无人机主动 SLAM/医学 CT/跨本体 VLA/卫星 NVS/机械拇指/网球时空/视觉生成）；全文 **19 L0/FULL + 1 L1 摘要级**（2610.36014 Immersive Commons，ar5iv 仅摘要页）。'
 'Top10（实数 10 篇）：**14 A / 4 B / 2 C 全批，最高 4.30（RESPLE2），无 S 级**；覆盖 5 赛道（纯值 Top10 仅 4 赛道，按重筛闭环以 SOMA 3.79 回补替换 SG²SLAM 4.00）。'
 '三关：门① max Jaccard **0.308**；门② 定稿 5 赛道；门③ 当日最高 4.30 < 库内近 30 天 Top10 均分 **4.417**（435 条入窗，现算）→ **非重磅日、无 S 级，未拔高**；RESPLE2 4.30 / GraftRay 4.20 达 S 线按校准关记 A；OUTDATED 0。'
 '**backfill-1029**：旧稿 replace/cross 再公告 4 篇首次入馆（3 A / 1 B，最高 LoBE-GS 3.73，无 S 线）。'
 'registry 669 → **693**（+19 +1 +4）。详见 [运行报告](../../reports/XR-Daily-Report-2026-10-29.md) 与 [MOC-2026-10-29](./MOC-2026-10-29.md) / [MOC-backfill-1029](./MOC-backfill-1029.md) / [Backfill 报告](../../reports/XR-Backfill-Report-backfill-1029.md)。\n')
anchor = '> **状态注记（2026-10-28）**'
i = h.find(anchor)
j = h.find('\n\n', h.find('[Backfill 报告](../../reports/XR-Backfill-Report-backfill-1028.md)。', i))
h = h[:j] + '\n' + note29 + h[j:]

# 7.3 速查入口
h = h.replace('| 最新一期 | [MOC · 2026-10-28](./MOC-2026-10-28.md) |', '| 最新一期 | [MOC · 2026-10-29](./MOC-2026-10-29.md) |')
h = h.replace('| 上一期 | [MOC · 2026-10-27](./MOC-2026-10-27.md) |', '| 上一期 | [MOC · 2026-10-28](./MOC-2026-10-28.md) |')
h = h.replace('（现有 362 篇）', '（现有 384 篇）')
h = h.replace('| 最新运行状态 | [运行报告 2026-10-28](../../reports/XR-Daily-Report-2026-10-28.md)（10-27 公告批次 26 篇 18A/6B/2C 非重磅日无S + backfill-1028 补录 10 篇；listing+RSS 两渠道互证，RSS 漏网 0 篇） |',
              '| 最新运行状态 | [运行报告 2026-10-29](../../reports/XR-Daily-Report-2026-10-29.md)（10-28 公告批次 19 篇 + ParetoGS 补录 1 = 20 篇 14A/4B/2C 非重磅日无S + backfill-1029 补录 4 篇；listing+RSS 两渠道互证，RSS 漏网 0 篇；补录 ParetoGS 为上批静默丢失稿） |')

# 7.4 批次索引表追加两行
row_main = ('| 2026-10-29 | [MOC-2026-10-29](./MOC-2026-10-29.md) | XR 20（Top10 实数）· 14A/4B/2C · 非重磅日（无S） | '
            '10-28 公告批次 19 篇 + ParetoGS 补录 1（10-27 组上批静默丢失）；listing+RSS 两渠道互证 33 篇中 19 篇 XR；1 篇 L1 摘要级 |')
row_bf = ('| backfill-1029 | [MOC-backfill-1029](./MOC-backfill-1029.md) | 补录 4（3A/1B）· 非当日新提交 | '
          '10-28 公告 RSS 混入旧稿 replace/cross 再公告 4 篇（2508/2510/2604/2605） |')
h = h.replace('| backfill-1028 | [MOC-backfill-1028](./MOC-backfill-1028.md) | 补录 10（9A/1B）· 非当日新提交 | 10-27 公告 RSS 混入旧稿 replace/cross 再公告 10 篇（2601~2609） |',
              '| backfill-1028 | [MOC-backfill-1028](./MOC-backfill-1028.md) | 补录 10（9A/1B）· 非当日新提交 | 10-27 公告 RSS 混入旧稿 replace/cross 再公告 10 篇（2601~2609） |\n'
              + row_main + '\n' + row_bf)

# 7.5 追加 Top10 段（文件尾）
seg = '\n### 2026-10-29 新增（Top10 实数：14 A / 4 B / 2 C 全批，非重磅日无 S）\n\n| # | 论文 | 赛道 | 分值 | 等级 | 证据 |\n|---:|---|---|---:|---|---|\n'
for i2, p in enumerate(MAIN, 1):
    seg += f"| {i2} | {esc(p['title_zh'])} | {p['track']} | {p['value']:.2f} | {p['grade']} | {p['evidence']} |\n"
seg += '\n### backfill-1029 补录（4 篇：3 A + 1 B，非当日新提交）\n\n| # | 论文 | 赛道 | 分值 | 等级 | 证据 |\n|---:|---|---|---:|---|---|\n'
for i2, p in enumerate(BF, 1):
    seg += f"| {i2} | {esc(p['title_zh'])} | {p['track']} | {p['value']:.2f} | {p['grade']} | {p['evidence']} |\n"
h = h.rstrip() + '\n' + seg

# 7.6 页脚计数
h = h.replace('库内 **669 篇**', '库内 **693 篇**').replace('原子笔记 **362 篇**', '原子笔记 **384 篇**')
h = h.replace('MOC 30 份', 'MOC 32 份')
h = h.replace('*最后更新：2026-10-28（10-27 公告批次：26 篇 XR 新稿 18A/6B/2C 非重磅日无S + backfill-1028 补录 10 篇 9A/1B）',
              '*最后更新：2026-10-29（10-28 公告批次：19 篇 XR 新稿 + ParetoGS 补录 1 = 20 篇 14A/4B/2C 非重磅日无S + backfill-1029 补录 4 篇 3A/1B）')
open(moc_path, 'w', encoding='utf-8').write(h)
print('MOC-总索引 refreshed')
print('DONE')
