# -*- coding: utf-8 -*-
"""2026-10-31 产物生成：主批（10-30 公告批次 18 篇）+ backfill-1031（旧稿 replace/cross 再公告 6 篇）。
公告日 2026-10-30 = 10-29（周四）公告批次未释放（arXiv 侧跳空/延迟）后延迟释放；拉取日 2026-10-31（周六 02:30）。
消费 data/scored_1031.json（字段齐全、显式带 batch）；registry 幂等追加（先备份，in_top10 按定稿 Top10 显式设置）；
生成 7 维表/scored/run_log/笔记/MOC/报告并刷新总索引。"""
import json, os, shutil, glob

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
os.chdir(ROOT)
D = json.load(open('data/scored_1031.json', encoding='utf-8'))
MAIN, BF = D['main'], D['backfill']
TOP10_IDS = set(D['top10_ids'])
DATE, BFB = '2026-10-31', 'backfill-1031'
ANN = '2026-10-30'          # 公告日（10-29 公告跳空后延迟释放）
GATE3 = 4.420               # 门③ 现算均分（窗口 2026-10-01~10-31，394 条入窗）
TODAY_MAX = MAIN[0]['value']  # 4.37
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
    '批次：2026-10-31（**2026-10-30（周五）公告批次**——10-29（周四）公告批次未释放（arXiv 侧跳空/延迟；10-30 运行已三源互证：listing 无 10-29 日组 + API `submittedDate` 10-28/10-29 区间 0 篇 + RSS 全局空源），延迟至 10-30 00:00 UTC 释放；公告日 10-30 ≠ 拉取日 10-31（周六 02:30），诚实口径）。\n'
    '候选池 18 篇：漏网对账（先于拉取，TARGET_LO=2026-10-29）listing 7 分类最新公告日均为 **2026-10-30**（无 10-29 日组）；**10-30 组 728 篇全部未入馆**（cs.CV 233 / cs.GR 7 / cs.HC 48 / cs.MM 7 / cs.RO 112 / cs.AI 315 / cs.IV 6）→ 摘要级 XR 命中 **31 篇**；RSS 7 分类去重 1,115 → KW 命中 52 = **31 篇 10-30 公告组真新提交（18 篇 XR + 13 篇非 XR 剔除）+ 15 篇旧稿 replace/cross 再公告（6 篇 XR → backfill-1031 + 9 篇非 XR 剔除）+ 6 篇库内 v2 再公告（剔除）**；listing 摘要级 31 篇全部被 RSS 覆盖（**RSS 漏网 0 篇**，两渠道互证）。\n'
    'arXiv API published 口径核验提交日：10-27×1 / 10-28×7 / 10-29×10（均早于公告日 10-30，符合「周四/周五提交、周五 00:00 UTC 释放」节律；RSS published 字段为公告时间戳，非提交日）。\n'
    '全文：18 篇候选全部 **L0/FULL**（26,072–126,850 字符），串行 3s/篇，先抓全文再定稿。\n'
    '覆盖度三关：门① 最大 Jaccard **0.075**（2610.39745 UniffordInteractor vs 库内 2610.27725，<0.62 通过）；门② 定稿 Top10 覆盖 **6 赛道**（全批 8 赛道，≥5 通过，无需重筛）；门③ 当日最高 **4.37 < 库内近 30 天 Top10 均分 4.420**（窗口 2026-10-01~10-31、394 条入窗、现算）→ **非重磅日、无 S 级**，未拔高。ACD-GS 4.37 / UniffordInteractor 4.30 / GradSplat 4.27 / LucidLyra 4.22 达 S 线按校准关记 A（同 10-24 EgoHand / 10-27 WFM / 10-28 RacerGS / 10-29 RESPLE2 先例）。',
    len(TOP10))

seven_table(BF, f'papers/daily/{BFB}/7dim-table.md',
    f'{BFB} 全量 7 维度对比表（参考）',
    '批次：backfill-1031（**10-30 公告批次中 RSS 混入的旧稿 replace/cross 再公告**（首次入馆；原始投稿 2501=2025-01 / 2604=2026-04 / 2605=2026-05 / 2608=2026-08）；均非 10-30 当日新提交，诚实口径单独编号）。\n'
    '候选 6 篇：InHabit（图像基础模型规模化生成 3D 人-场景交互数据）/ SplitGS-Loc（高斯劈分解多对一对应的视觉定位）/ Ego-OSCAR（开源头戴双目-惯性第一视角采集系统）/ VidParse（免训练第一视角流程在线解析）/ BitC-3DGS（位压缩 token 化 3DGS 水印）/ GSVC（2D 高斯泼溅视频表示与压缩）。全部 L0/FULL 全文后定稿。\n'
    '门③ 对 backfill 不适用；本批不参与当日「重磅日」判定。门① 全池合并复核最大 Jaccard 0.075 < 0.62（通过，无同质重复）；门② 覆盖 5 赛道（评估与数据集 / 重建与SLAM / 系统与平台×2 / 感知与认知 / 渲染与显示；6 篇低量批次实际上限）。\n'
    '注：本批 6 篇均未达 S 线（最高 InHabit 4.07），按实数定级。',
    len(BF))

# ---------- 2. scored.md + run_log.md ----------
def scored_md(papers, path, title, extra):
    L = [f'# {title}\n', extra + '\n', '| 排名 | arXiv | 标题 | 赛道 | 总分 | 等级 | 证据 | 公告类型 |',
         '|---|---|---|---|---|---|---|---|']
    for i, p in enumerate(papers, 1):
        L.append(f"| {i} | {p['id']} | {esc(p['title_zh'])} | {p['track']} | {p['value']:.2f} | {p['grade']} | {p['evidence']} | {p['announce']} |")
    open(path, 'w', encoding='utf-8').writelines([x + '\n' for x in L])

scored_md(MAIN, f'papers/daily/{DATE}/scored.md', f'{DATE} 评分明细',
    '评分口径：7 维加权 IMP0.20·NOV0.20·TEC0.15·EXP0.15·PER0.15·TRL0.08·REP0.07；分档 S≥4.2 / A3.6–4.2 / B3.0–3.6 / C<3.0。全部基于全文证据定稿（18 篇全部 L0/FULL）。\n'
    f'覆盖度三关：门① 最大 Jaccard 0.075 < 0.62（通过，非同质）；门② 定稿 Top10 覆盖 6 赛道 ≥ 5（通过，全批 8 赛道，无需重筛）；门③ 当日最高 4.37 < 库内近 30 天 Top10 均分 4.420（现算，394 条入窗）→ 非重磅日、无 S 级（校准关，不触发重筛；ACD-GS 4.37 / UniffordInteractor 4.30 / GradSplat 4.27 / LucidLyra 4.22 达 S 线按校准关记 A）。\n'
    'OUTDATED/SUPERSEDED 0 篇。等级分布：13 A / 5 B。')
scored_md(BF, f'papers/daily/{BFB}/scored.md', f'{BFB} 评分明细',
    '评分口径同上。本批为旧稿 replace/cross 再公告首次入馆（非当日新提交），门③ 不适用。\n'
    '门① 全池合并复核最大 Jaccard 0.075 < 0.62（通过）；门② 覆盖 5 赛道（6 篇低量批次实际上限）；OUTDATED/SUPERSEDED 0 篇。等级分布：5 A / 1 B。')

run_log_main = f'''# {DATE} 执行日志

## 数据源与对账（第 1-3 步）
- **漏网对账（先于拉取）**：`scripts/audit_gap_listing.py`（TARGET_LO=2026-10-29，上一批次公告日）7 分类采集，完整性校验全过。listing 7 分类最新公告日均为 **2026-10-30**（10-29 周四公告批次未释放——arXiv 侧跳空/延迟，10-30 运行已三源互证并记录；本批确认其延迟至 10-30 00:00 UTC 释放）。**10-30 组 728 篇全部未入馆**（cs.CV 233 / cs.GR 7 / cs.HC 48 / cs.MM 7 / cs.RO 112 / cs.AI 315 / cs.IV 6），摘要级 XR 命中 **31 篇**（`data/missed_xr_abstract_1031.json`，API 元数据取回 728/728）。
- **摘要级 XR 过滤**：`scripts/filter_missed_xr_abstract.py` 对 10-30 组 728 篇跑 API 摘要级过滤 → XR 命中 31 篇。
- **RSS 主渠道交叉验证**：`scripts/fetch_rss.py` 7 分类全量去重 1,115 条 → KW 命中 **52** = **31 篇 10-30 公告组真新提交（18 篇 XR + 13 篇非 XR）+ 15 篇旧稿 replace/cross 再公告（6 篇 XR → backfill-1031 + 9 篇非 XR 剔除）+ 6 篇库内 v2 再公告（剔除）**。listing 摘要级 31 篇**全部被 RSS 覆盖，RSS 漏网 0 篇**——两渠道互证（漏网候选清单 `data/missed_xr.json` 本批无新增）。
- **API 探针**：arXiv API `id_list` 批量核验 18 篇主批 published（原始提交日）：10-27×1 / 10-28×7 / 10-29×10，均早于公告日 10-30，符合「周四/周五提交、周五 00:00 UTC 释放」节律；RSS published 字段为公告时间戳（10-30），非提交日，两口径已区分。

## 甄别（第 3 步）
- 主批 XR 核心/强相关 **18 篇**入评分池；剔非 XR **13 篇**（2610.38086 多大陆野火数据集 / 2610.38141 SKiD-SLAM 多机器人 LiDAR SLAM / 2610.38405 SpaceAct 3D 时空推理基准 / 2610.38443 机器人抓取骨架自动标注 / 2610.39044 动态接抛 / 2610.39055 封闭空间连续体机器人 / 2610.39167 EgoContact / 2610.39293 自回归图像 any-order 生成 / 2610.39385 UMI-Live 双臂数据采集 / 2610.39691 手机室内定位 / 2610.39879 机器人穿刺规划 / 2610.39998 月面机械臂遥操作 / 2610.40636 视觉基础模型空间状态探测）。
- 旧稿 replace/cross 再公告 15 篇中 **6 篇 XR → backfill-1031**（首次入馆，单独编号）；9 篇非 XR 剔除（2505.05488 事件相机综述 / 2512.03479 ProcObject-10K / 2607.08115 RadLoc 雷达定位 / 2607.13472 EgoHTR / 2608.07267 WNM-3D 世界导航模型 / 2609.06242 面向任务语义通信 / 2610.13056 A4-MR 医学 MRI / 2610.36615 HumiMimic / 2610.37509 Ego-CEVR）。
- 库内 v2 再公告 6 篇剔除（2608.12759 NavSight，backfill-2603-2609 已入馆 / 2609.25633 动态 3DGS 压缩，09-24 已入馆 / 2609.37115 NRF-GS，10-02 已入馆 / 2610.13309 NovaSplat，backfill-1012-1015 已入馆 / 2610.32915 VR 眼动仪精度，10-27 已入馆 / 2610.36168 PrinGS，10-29 已入馆）。

## 全文抓取（第 4 步）
- 24 篇候选（主批 18 + backfill 6）跑 `scripts/fetch_fulltext.py`，严格串行 3s/篇（约 1 分 30 秒）：**全部 L0/FULL**（26,072–126,850 字符）。无限流/降级/伪造。
- manifest 合并写入校验通过；WROTE=24>0。

## 评分与三关（第 5-6 步）
- 先抓全文再定稿。7 维加权定稿：主批 **13 A / 5 B**（最高 4.37 ACD-GS；ACD-GS 4.37 / UniffordInteractor 4.30 / GradSplat 4.27 / LucidLyra 4.22 达 S 线）；backfill **5 A / 1 B**（最高 InHabit 4.07）。
- 门① 最大 Jaccard **0.075**（2610.39745 UniffordInteractor vs 库内 2610.27725；<0.62，非同质）。
- 门② 定稿 Top10 覆盖 **6 赛道**（渲染与显示×2 / 内容生成×2 / 神经渲染×3 / 世界模型与仿真×1 / 评估与数据集×1 / 触觉与多模态×1；全批 8 赛道，≥5 通过，**无需重筛**）。
- 门③ 当日最高 **4.37 < 库内近 30 天 Top10 均分 4.420**（窗口 2026-10-01~10-31、394 条入窗、现算）→ **非重磅日、无 S 级**；4 篇达 S 线者按校准关记 A（同 10-24 EgoHand / 10-27 WFM / 10-28 RacerGS / 10-29 RESPLE2 先例）。三关全过，**未触发重筛**。
- OUTDATED/SUPERSEDED **0 篇**。路线级观察：① 前馈 3DGS 进入「梯度进前向、预算即约束」阶段（GradSplat 前向内学习式梯度步 + BudSplat 渲染预算表示学习 + LucidLyra 生成式可查询场景），与 ACD-GS 的训练期致密化共同压缩「质量-成本」帕累托前沿；② 3DGS 评测方法论自律（2610.38349 坐标对齐协议：Flash3D RE10K 由 14.52 dB 修正为 22.04 dB，排名失真根因是坐标系未对齐）；③ 交互内容生成从单物体走向人-多物体联合推理（UniffordInteractor TOG）；④ 硬件类缺口依旧——本期触觉（Tactus）与鱼眼全视场（GOFish）属传感/光学系统工程，近眼显示/光场/全息方向仍仅 CVQPG 与 HoOPOE 两篇。

## 产物（第 7-8 步）
- 报告 2 份（主报告 + backfill 报告）+ 原子笔记 24 篇（grade≥B）+ MOC 2 份 + 总索引刷新 + 7 维表/scored/run_log 各 2 套。
- registry 693 → **717**（+18 主批 +6 backfill；备份 `papers/library/registry.jsonl.bak-20261031`；按 base_id 幂等）。
'''
open(f'papers/daily/{DATE}/run_log.md', 'w', encoding='utf-8').write(run_log_main)

run_log_bf = f'''# {BFB} 执行日志

- **批次性质**：backfill（非当日新提交）——10-30 公告批次中 RSS 混入的旧稿 replace/cross 再公告 6 篇首次入馆；原始投稿 2501=2025-01 / 2604=2026-04 / 2605=2026-05 / 2608=2026-08（arXiv ID 前缀 2501/2604/2605/2608）。
- **来源**：`scripts/fetch_rss.py` 7 分类全量去重 1,115 → KW 命中 52；其中 15 篇旧稿再公告经 XR 甄别保留 6 篇（剔非 XR 9 篇：事件相机综述/ProcObject-10K/RadLoc/EgoHTR/WNM-3D/语义通信/A4-MR/HumiMimic/Ego-CEVR）。
- **全文**：6 篇全部 L0/FULL，串行 3s/篇，无限流/降级/伪造。
- **评分**：5 A / 1 B（最高 InHabit 4.07，无 S 线）。门① 全池合并复核最大 Jaccard 0.075 < 0.62；门② 覆盖 5 赛道（6 篇低量批次实际上限）；门③ 不适用；OUTDATED 0。
- **诚实口径**：全部条目 `batch=backfill-1031` + `orig_window` 标注，绝不混入「当日新论文」。
'''
open(f'papers/daily/{BFB}/run_log.md', 'w', encoding='utf-8').write(run_log_bf)

# ---------- 3. registry（先备份，幂等追加，in_top10 显式） ----------
reg_path = 'papers/library/registry.jsonl'
shutil.copy(reg_path, reg_path.replace('.jsonl', '.bak-20261031'))
rows = [json.loads(l) for l in open(reg_path, encoding='utf-8') if l.strip()]
have = {r['id'].split(':')[-1].split('v')[0] for r in rows}
PREFIX_MONTH = {'2501': '2025-01', '2604': '2026-04', '2605': '2026-05', '2608': '2026-08'}
added = 0
with open(reg_path, 'a', encoding='utf-8') as f:
    for p in MAIN + BF:
        if p['id'] in have:
            continue
        entry = dict(id=f"arXiv:{p['id']}", title=p['title'], title_zh=p['title_zh'],
                     track=p['track'], date=(DATE if p in MAIN else ANN),
                     value=p['value'], grade=p['grade'], scores=p['scores'],
                     status=p['status'], evidence=p['evidence'], fetch_level=p['level'],
                     fulltext_chars=0, in_top10=(p['id'] in TOP10_IDS), batch=p['batch'],
                     announce_type=p['announce'], flags=[])
        if p in BF:
            entry['in_top10'] = False
            entry['orig_window'] = f"旧稿 replace/cross 再公告（首次入馆）：{PREFIX_MONTH[p['id'][:4]]} 投稿，{ANN} 公告批次 RSS 混入"
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
        date=(DATE if p in MAIN else ANN), value=f"{p['value']:.2f}", grade=p['grade'],
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

moc(MAIN, f'papers/MOC/MOC-{DATE}.md', f'MOC · {DATE}（10-30 公告批次）',
    '> 当日地图：**公告日 2026-10-30（周五）≠ 拉取日 2026-10-31（周六 02:30）**——诚实口径，非当日硬提交。10-29（周四）公告批次未释放（arXiv 侧跳空/延迟），延迟至 10-30 00:00 UTC 释放。\n'
    '> 主批 XR 新稿 18 篇（13 A / 5 B，无 S——非重磅日）；listing 与 RSS 两渠道互证 31 篇真新提交中 18 篇 XR（RSS 漏网 0 篇）；全文 18 篇全部 L0/FULL。\n'
    '> 覆盖度三关：门① 0.075 / 门② 定稿 Top10 6 赛道（全批 8 赛道，无需重筛）/ 门③ 4.37 < 4.420（现算，394 条入窗）→ 非重磅日无 S；ACD-GS 4.37 / UniffordInteractor 4.30 / GradSplat 4.27 / LucidLyra 4.22 达 S 线按校准关记 A。Top10 实数 10 篇。')
moc(BF, f'papers/MOC/MOC-{BFB}.md', f'MOC · {BFB}（旧稿再公告补录）',
    '> 本批为 **backfill**：10-30 公告批次 RSS 混入的旧稿 replace/cross 再公告 6 篇首次入馆（原始投稿 2501/2604/2605/2608），**均非当日新提交**。\n'
    '> 5 A / 1 B；最高 InHabit 4.07（无 S 线）。门① 0.075 / 门② 5 赛道（6 篇低量批次实际上限）/ 门③ 不适用。')

# ---------- 6. 报告 ----------
def report(papers, path, title, header, batch_label, topn, gate_lines):
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
    L += gate_lines
    L.append('\n## 六、附录：证据等级分布与抓取记录\n')
    nf = sum(1 for p in papers if p['evidence'] == 'FULL')
    L.append(f'- FULL {nf} 篇；PARTIAL 0 篇；ABSTRACT_ONLY 0 篇（本批 24 篇候选全部 L0/FULL，无摘要级降级评估）。')
    L.append('- 抓取降级：无 L5；无 OCR；无伪造。串行 3s/篇，无限流。')
    open(path, 'w', encoding='utf-8').writelines([x + '\n' for x in L])

report(TOP10,
       f'reports/XR-Daily-Report-{DATE}.md',
       f'XR 每日论文解读报告 · {DATE}（10-30 公告批次）',
       '## 一、执行摘要\n'
       f'- **公告日 2026-10-30（周五）≠ 拉取日 2026-10-31（周六 02:30）**——诚实口径：本批处理的是 10-30 公告批次；**10-29（周四）公告批次未释放**（arXiv 侧跳空/延迟，10-30 运行三源互证：listing 无 10-29 日组 + API submittedDate 区间 0 篇 + RSS 全局空源），延迟至 10-30 00:00 UTC 释放，非当日硬提交。\n'
       '- **主批 XR 新稿 18 篇（13 A / 5 B，无 S 级）**。Top10：ACD-GS 4.37（非对称曲率感知致密化，高斯数与存储平均降约 60%）· UniffordInteractor 4.30（TOG，人-多物体交互统一 affordance 推理）· GradSplat 4.27（前向传播内梯度精化的前馈 3DGS，RE10K 33.68 dB）· LucidLyra 4.22（前馈生成式可查询 3D 场景重建，mIoU 64.1）· L3G-World 4.15（潜空间 3D 高斯记忆的实时无限世界生成）· GOFish 4.15（全视场鱼眼 3DGS 与网格提取，200° PSNR +2.28 dB）· BudSplat 4.15（渲染预算约束的紧凑前馈 3DGS，5% 保留率 97K 高斯 23.08 PSNR）· 单视图 NVS 坐标对齐评测协议 4.14（Flash3D RE10K 由 14.52 修正为 22.04 dB）· Tactus 4.03（Meta RL 触觉+姿态感知手套，0.59 N 最小可检测力）· MLLM-GS 4.00（MLLM 先验引导极端环境 NVS，训练降约 9×）。\n'
       '- **覆盖 6 赛道**：渲染与显示×2 / 内容生成×2 / 神经渲染×3 / 世界模型与仿真×1 / 评估与数据集×1 / 触觉与多模态×1（全批 8 赛道）。\n'
       '- **覆盖度三关**：门① 0.075；门② 6 赛道（≥5，无需重筛）；门③ 4.37 < 4.420（现算，394 条入窗）→ **非重磅日、无 S 级**；ACD-GS 4.37 / UniffordInteractor 4.30 / GradSplat 4.27 / LucidLyra 4.22 达 S 线按校准关记 A。\n'
       '- **全文证据**：18 篇全部 L0/FULL（26,072–126,850 字符），无摘要级降级。\n'
       '- **同批 backfill-1031**：RSS 混入旧稿 replace/cross 再公告 6 篇首次入馆（5 A / 1 B，最高 InHabit 4.07），详见 [XR-Backfill-Report-backfill-1031.md](XR-Backfill-Report-backfill-1031.md)。',
       DATE, 10,
       ['- 门①（同质去重）：最大 Jaccard 0.075 < 0.62，通过，无同质重复。',
        '- 门②（赛道覆盖）：定稿 Top10 覆盖 6 赛道（≥5），通过；全批 8 赛道，纯值排序即满足，未触发重筛。',
        '- 门③（价值天花板）：当日最高分 4.37 < 库内近 30 天 Top10 均分 4.420（现算，394 条入窗）→ 非重磅日、无 S 级，未拔高、未凑数；达 S 线的 ACD-GS 4.37 / UniffordInteractor 4.30 / GradSplat 4.27 / LucidLyra 4.22 按校准关记 A（同 10-24 EgoHand / 10-27 WFM / 10-28 RacerGS / 10-29 RESPLE2 先例）。',
        '- 三关均未触发重筛；OUTDATED/SUPERSEDED 0 篇。\n'])

report(BF, f'reports/XR-Backfill-Report-{BFB}.md',
       f'XR Backfill 补录报告 · {BFB}（旧稿再公告）',
       '## 一、执行摘要\n'
       '- **批次性质**：backfill（非当日新提交）——10-30 公告批次中 RSS 混入的旧稿 replace/cross 再公告 6 篇，首次入馆；原始投稿 2501=2025-01 / 2604=2026-04 / 2605=2026-05 / 2608=2026-08。\n'
       '- **补录 6 篇（5 A / 1 B）**：InHabit 4.07（图宾根大学/马普/Bosch，图像基础模型规模化 3D 人-场景交互数据）· SplitGS-Loc 3.94（成均馆大学+NAVER LABS，高斯劈分解多对一对应的视觉定位）· Ego-OSCAR 3.72（开源头戴双目-惯性第一视角采集系统）· VidParse 3.72（免训练第一视角流程在线解析）· BitC-3DGS 3.65（位压缩 token 化高容量 3DGS 水印）· GSVC 3.57（NUS，2D 高斯泼溅视频表示与压缩）。\n'
       '- **覆盖 5 赛道**；门① 0.075（全池合并复核）；门③ 对 backfill 不适用；OUTDATED 0。\n'
       '- **诚实口径**：全部条目 `batch=backfill-1031` + `orig_window` 标注，绝不混入「当日新论文」。',
       BFB, 10,
       ['- 门①（同质去重）：全池合并复核最大 Jaccard 0.075 < 0.62，通过，无同质重复。',
        '- 门②（赛道覆盖）：覆盖 5 赛道（评估与数据集 / 重建与SLAM / 系统与平台×2 / 感知与认知 / 渲染与显示），6 篇低量批次实际上限。',
        '- 门③（价值天花板）：对 backfill 不适用；本批 6 篇均未达 S 线（最高 InHabit 4.07），按实数定级，未拔高。',
        '- OUTDATED/SUPERSEDED 0 篇。\n'])

# ---------- 7. MOC-总索引刷新 ----------
moc_path = 'papers/MOC/MOC-总索引.md'
h = open(moc_path, encoding='utf-8').read()
n0 = len(h)

def rep(old, new, tag):
    global h
    assert old in h, f'ANCHOR NOT FOUND: {tag}'
    h = h.replace(old, new, 1)

# 7.1 头部计数与批次列表
rep('累计 **693 篇**；跨度 2026-09-15 ~ 2026-10-28',
    '累计 **717 篇**；跨度 2026-09-15 ~ 2026-10-30', 'head-count')
rep('**backfill-1029:4（10-28 公告 RSS 混入旧稿 replace/cross 再公告，首次入馆）**；',
    '**backfill-1029:4（10-28 公告 RSS 混入旧稿 replace/cross 再公告，首次入馆）** · '
    '**2026-10-31:18（10-30 公告批次真新提交——10-29 公告跳空后延迟释放，非重磅日无S；listing+RSS 两渠道互证 31 篇中 18 篇 XR）** · '
    '**backfill-1031:6（10-30 公告 RSS 混入旧稿 replace/cross 再公告，首次入馆）**；', 'batch-list')
rep('**10-30 周五状态日 0 新稿（10-29 公告批次未释放——arXiv 侧跳空/延迟，listing/API/RSS 三源互证；10-28 公告组复核 0 漏网）**。',
    '**10-30 周五状态日 0 新稿（10-29 公告批次未释放——arXiv 侧跳空/延迟，listing/API/RSS 三源互证；10-28 公告组复核 0 漏网）**；'
    '**10-31 周六处理 10-30 公告批次（10-29 公告跳空后延迟释放；18 篇 XR 新稿 13A/5B + backfill-1031 补录 6 篇 5A/1B，非重磅日无S）**。', 'narrative')

# 7.2 追加 10-31 状态注记（在 10-30 注记后）
note31 = ('> **状态注记（2026-10-31）**：周六 02:30，处理 **2026-10-30（周五）公告批次**（**10-29 周四公告批次未释放——arXiv 侧跳空/延迟，延迟至 10-30 00:00 UTC 释放**；公告日≠拉取日，诚实口径）。'
 '漏网对账（先于拉取，TARGET_LO=2026-10-29）：listing 7 分类最新公告日均为 **10-30**（无 10-29 日组）；**10-30 组 728 篇全部未入馆**（CV 233/GR 7/HC 48/MM 7/RO 112/AI 315/IV 6），摘要级 XR 命中 **31 篇**。'
 'RSS 7 分类去重 1,115 → KW 命中 52 = **31 篇 10-30 公告组真新提交（18 XR + 13 非 XR）+ 15 篇旧稿 replace/cross 再公告（6 XR → backfill-1031 + 9 非 XR）+ 6 篇库内 v2 再公告**；listing 摘要级 31 篇全部被 RSS 覆盖（**RSS 漏网 0 篇**，两渠道互证）。API published 口径核验提交日 10-27×1 / 10-28×7 / 10-29×10（均早于公告日，符合释放节律；RSS published 为公告时间戳，非提交日）。'
 '主批甄别 **XR 核心/强相关 18 篇**（剔非 XR 13 篇：野火数据集/SKiD-SLAM/SpaceAct/机器人抓取自动标注/动态接抛/连续体机器人/EgoContact/自回归图像 any-order 生成/UMI-Live/手机室内定位/机器人穿刺规划/月面遥操作/空间状态探测）；全文 **18 篇全部 L0/FULL**（26,072–126,850 字符）。'
 'Top10（实数 10 篇）：**13 A / 5 B 全批，最高 4.37（ACD-GS），无 S 级**；覆盖 6 赛道（渲染与显示×2/内容生成×2/神经渲染×3/世界模型与仿真×1/评估与数据集×1/触觉与多模态×1；全批 8 赛道）。'
 '三关：门① max Jaccard **0.075**；门② 6 赛道；门③ 当日最高 4.37 < 库内近 30 天 Top10 均分 **4.420**（394 条入窗，现算）→ **非重磅日、无 S 级，未拔高**；ACD-GS 4.37 / UniffordInteractor 4.30 / GradSplat 4.27 / LucidLyra 4.22 达 S 线按校准关记 A；OUTDATED 0。'
 '**backfill-1031**：旧稿 replace/cross 再公告 6 篇首次入馆（5 A / 1 B，最高 InHabit 4.07，无 S 线；原始投稿 2501/2604/2605/2608）。'
 'registry 693 → **717**（+18 +6）。详见 [运行报告](../../reports/XR-Daily-Report-2026-10-31.md) 与 [MOC-2026-10-31](./MOC-2026-10-31.md) / [MOC-backfill-1031](./MOC-backfill-1031.md) / [Backfill 报告](../../reports/XR-Backfill-Report-backfill-1031.md)。\n')
anchor = '> **状态注记（2026-10-30）**'
i = h.find(anchor)
assert i >= 0, 'ANCHOR NOT FOUND: note30'
j = h.find('[状态报告](../../reports/XR-Daily-Report-2026-10-30.md)。', i)
assert j >= 0, 'ANCHOR NOT FOUND: note30-end'
j = h.find('\n', j) + 1
h = h[:j] + note31 + h[j:]

# 7.3 速查入口
rep('| 最新一期 | [MOC · 2026-10-29](./MOC-2026-10-29.md) |',
    '| 最新一期 | [MOC · 2026-10-31](./MOC-2026-10-31.md) |', 'quick-latest')
rep('| 上一期 | [MOC · 2026-10-28](./MOC-2026-10-28.md) |',
    '| 上一期 | [MOC · 2026-10-29](./MOC-2026-10-29.md) |', 'quick-prev')
rep('（现有 384 篇）', '（现有 408 篇）', 'quick-notes')
rep('| 最新运行状态 | [运行报告 2026-10-29](../../reports/XR-Daily-Report-2026-10-29.md)（10-28 公告批次 19 篇 + ParetoGS 补录 1 = 20 篇 14A/4B/2C 非重磅日无S + backfill-1029 补录 4 篇；listing+RSS 两渠道互证，RSS 漏网 0 篇；补录 ParetoGS 为上批静默丢失稿） |',
    '| 最新运行状态 | [运行报告 2026-10-31](../../reports/XR-Daily-Report-2026-10-31.md)（10-30 公告批次 18 篇 13A/5B 非重磅日无S + backfill-1031 补录 6 篇 5A/1B；10-29 公告跳空后延迟释放；listing+RSS 两渠道互证，RSS 漏网 0 篇；全文全 L0/FULL） |', 'quick-status')

# 7.4 批次索引表追加两行
row_main = ('| 2026-10-31 | [MOC-2026-10-31](./MOC-2026-10-31.md) | XR 18（Top10 实数）· 13A/5B · 非重磅日（无S） | '
            '10-30 公告批次（10-29 公告跳空后延迟释放）真新提交 18 篇；listing+RSS 两渠道互证 31 篇中 18 篇 XR；全文全 L0/FULL |')
row_bf = ('| backfill-1031 | [MOC-backfill-1031](./MOC-backfill-1031.md) | 补录 6（5A/1B）· 非当日新提交 | '
          '10-30 公告 RSS 混入旧稿 replace/cross 再公告 6 篇（2501/2604/2605/2608） |')
rep('| backfill-1029 | [MOC-backfill-1029](./MOC-backfill-1029.md) | 补录 4（3A/1B）· 非当日新提交 | 10-28 公告 RSS 混入旧稿 replace/cross 再公告 4 篇（2508/2510/2604/2605） |',
    '| backfill-1029 | [MOC-backfill-1029](./MOC-backfill-1029.md) | 补录 4（3A/1B）· 非当日新提交 | 10-28 公告 RSS 混入旧稿 replace/cross 再公告 4 篇（2508/2510/2604/2605） |\n'
    + row_main + '\n' + row_bf, 'batch-table')

# 7.5 追加 Top10 段（文件尾）
seg = '\n### 2026-10-31 新增（Top10 实数：13 A / 5 B 全批，非重磅日无 S）\n\n| # | 论文 | 赛道 | 分值 | 等级 | 证据 |\n|---:|---|---|---:|---|---|\n'
for i2, p in enumerate(MAIN, 1):
    seg += f"| {i2} | {esc(p['title_zh'])} | {p['track']} | {p['value']:.2f} | {p['grade']} | {p['evidence']} |\n"
seg += '\n### backfill-1031 补录（6 篇：5 A + 1 B，非当日新提交）\n\n| # | 论文 | 赛道 | 分值 | 等级 | 证据 |\n|---:|---|---|---:|---|---|\n'
for i2, p in enumerate(BF, 1):
    seg += f"| {i2} | {esc(p['title_zh'])} | {p['track']} | {p['value']:.2f} | {p['grade']} | {p['evidence']} |\n"
h = h.rstrip() + '\n' + seg

# 7.6 页脚计数
rep('*最后更新：2026-10-30（状态日：10-29 公告批次未释放，三源互证 listing 无 10-29 日组 + API submittedDate 0 篇 + RSS 全局空源；10-28 公告组 443 篇摘要级复核 0 漏网） · 库内 **693 篇** · 原子笔记 **384 篇** · MOC 32 份',
    '*最后更新：2026-10-31（10-30 公告批次：10-29 公告跳空后延迟释放；18 篇 XR 新稿 13A/5B 非重磅日无S + backfill-1031 补录 6 篇 5A/1B；listing+RSS 两渠道互证，RSS 漏网 0 篇；门③ 现算 4.420） · 库内 **717 篇** · 原子笔记 **408 篇** · MOC 34 份', 'footer')

open(moc_path, 'w', encoding='utf-8').write(h)
print('MOC-总索引 refreshed（%d -> %d chars）' % (n0, len(h)))
print('DONE')
