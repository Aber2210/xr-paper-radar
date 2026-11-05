# -*- coding: utf-8 -*-
"""2026-11-06 产物生成：主批（11-05 公告批次 12 篇）+ backfill-1106（旧稿 replace/cross 再公告 6 篇）。
公告日 2026-11-05（周四）≠ 拉取日 2026-11-06（周五 02:30），诚实口径。
API published 口径核验提交日：主批 11 篇 2026-11-04 提交 + 1 篇 2026-11-03 提交。
listing 11-04 组复采 declared=got 且 13 篇摘要级命中均为上批已剔非 XR（0 漏网）；11-05 组 398 篇摘要级 XR 命中 22 篇与 RSS 真新集合同一。
消费 data/scored_1106.json；registry 幂等追加（先备份，in_top10 按定稿显式设置）。"""
import json, os, shutil, glob

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
os.chdir(ROOT)
D = json.load(open('data/scored_1106.json', encoding='utf-8'))
MAIN, BF = D['main'], D['backfill']
TOP10_IDS = set(D['top10_ids'])
TOP10_ORDER = list(D['top10_ids'])   # 定稿展示顺序（门②重筛后；勿用 set 迭代，会丢顺序）
DATE, BFB = '2026-11-06', 'backfill-1106'
ANN = '2026-11-05'          # 公告日（周四）
GATE3 = 4.363               # 门③ 现算均分（窗口 2026-10-07~11-06，428 条入窗）
TODAY_MAX = MAIN[0]['value']  # 4.57
TOP10 = [p for pid in TOP10_ORDER for p in MAIN if p['id'] == pid]
assert [p['id'] for p in TOP10] == TOP10_ORDER

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
    '批次：2026-11-06（**2026-11-05（周四）公告批次**——公告日 11-05 ≠ 拉取日 11-06（周五 02:30），诚实口径）。\n'
    '候选池 12 篇：漏网对账（先于拉取，TARGET_DAY=2026-11-04）listing 7 分类最新公告日均为 **2026-11-05**（无漏跑公告日）；**11-04 组逐分类 declared=got**（CV 160/GR 2/HC 21/MM 5/RO 72/AI 252/IV 13，525 槽位）→ 未入馆 **441 篇**，摘要级复核 **13 篇命中均为 11-05 运行已剔非 XR → 0 漏网**；**11-05 组 398 篇唯一论文**（CV 148/GR 7/HC 29/MM 6/RO 62/AI 217/IV 8，477 槽位）→ 摘要级 XR 命中 **22 篇**。\n'
    'RSS 7 分类去重 **647** → KW 命中 **37** = **22 篇 11-05 公告组真新提交（12 篇 XR + 10 篇非 XR 剔除）+ 8 篇旧稿 replace/cross 再公告（6 篇 XR → backfill-1106 + 2 篇非 XR 剔除）+ 7 篇库内 v2 再公告（剔除）**；listing 摘要级 22 篇**全部被 RSS 覆盖，RSS 漏网 0 篇**——两渠道互证。\n'
    'arXiv API published 口径核验提交日：主批 **11 篇为 2026-11-04 提交 + 1 篇为 2026-11-03 提交**（均早于公告日 11-05；RSS published 字段为公告时间戳，非提交日）。\n'
    '全文：18 篇候选（主批 12 + backfill 6）串行 3s/篇，全部 **L0/FULL**（21,776–178,380 字符；人工复核正文中段均含实质章节，排除 ar5iv 摘要页误判）。\n'
    '覆盖度三关：门① 最大 Jaccard **0.167**（2611.06593 BudgetSplat vs 库内 2610.20590 Feed-Forward Multi-View Feature Coding，<0.62 通过）；门② 纯价值 Top10 仅覆盖 **4 赛道**（神经渲染×4 冗余）→ **触发一次重筛**：剔除神经渲染最低分 BudgetSplat 3.51，回补未覆盖核心赛道（空间计算与UI）B 级池最高分 VR HIIT 3.18 → 定稿 Top10 覆盖 **5 赛道**（同 11-04 SHield/Virtual Box 先例，BudgetSplat 仍入馆写 B 级笔记仅不占名额）；门③ 当日最高 **4.57 ≥ 库内近 30 天 Top10 均分 4.363**（窗口 2026-10-07~11-06、428 条入窗、现算）→ **重磅日，可评 S 级（1 篇 S）**。OUTDATED 0。',
    len(TOP10))

seven_table(BF, f'papers/daily/{BFB}/7dim-table.md',
    f'{BFB} 全量 7 维度对比表（参考）',
    '批次：backfill-1106（**11-05 公告批次中 RSS 混入的旧稿 replace/cross 再公告**（首次入馆；原始投稿 2401=2024-01 / 2506=2025-06 / 2511=2025-11 / 2604=2026-04 / 2607=2026-07 / 2611=2026-10，v2-v4 于 2026-11-04 更新后再公告）；均非 11-05 当日新提交，诚实口径单独编号）。\n'
    '候选 6 篇：EgoM2P（第一人称 4D 多模态多任务预训练）/ AEGIS（3D 高斯化身隐私遮蔽）/ EgoGen（第一人称合成数据生成）/ EvSLAM（高速事件 SLAM 基准）/ PIDiffSign（物理约束手语产生）/ AuroraWorld（结构化 4D 世界建模 exo-to-ego 生成）。全部 L0/FULL 全文后定稿。\n'
    '门③ 对 backfill 不适用；本批不参与当日「重磅日」判定。门① 全池合并复核最大 Jaccard 0.167 < 0.62（通过，无同质重复）；门② 覆盖 6 赛道。\n'
    '注：本批 6 篇均未达 S 线（最高 EgoM2P 4.10），按实数定级。',
    len(BF))

# ---------- 2. scored.md + run_log.md ----------
def scored_md(papers, path, title, extra):
    L = [f'# {title}\n', extra + '\n', '| 排名 | arXiv | 标题 | 赛道 | 总分 | 等级 | 证据 | 公告类型 |',
         '|---|---|---|---|---|---|---|---|']
    for i, p in enumerate(papers, 1):
        L.append(f"| {i} | {p['id']} | {esc(p['title_zh'])} | {p['track']} | {p['value']:.2f} | {p['grade']} | {p['evidence']} | {p['announce']} |")
    open(path, 'w', encoding='utf-8').writelines([x + '\n' for x in L])

scored_md(MAIN, f'papers/daily/{DATE}/scored.md', f'{DATE} 评分明细',
    '评分口径：7 维加权 IMP0.20·NOV0.20·TEC0.15·EXP0.15·PER0.15·TRL0.08·REP0.07；分档 S≥4.2 / A3.6–4.2 / B3.0–3.6 / C<3.0。全部基于全文证据定稿（18 篇全 L0/FULL）。\n'
    f'覆盖度三关：门① 最大 Jaccard 0.167 < 0.62（通过，非同质）；门② 纯价值 Top10 覆盖 4 赛道 → 触发一次重筛（剔除 BudgetSplat、回补 VR HIIT），定稿 Top10 覆盖 5 赛道 ≥5（通过；全批 6 赛道）；门③ 当日最高 4.57 ≥ 库内近 30 天 Top10 均分 4.363（现算，428 条入窗）→ **重磅日，1 篇 S 级**（校准关达标，未拔高——S 级论文 Open-HumanScale 4.57 系全文证据定稿）。\n'
    'OUTDATED/SUPERSEDED 0 篇。等级分布：1 S / 5 A / 6 B。')
scored_md(BF, f'papers/daily/{BFB}/scored.md', f'{BFB} 评分明细',
    '评分口径同上。本批为旧稿 replace/cross 再公告首次入馆（非当日新提交），门③ 不适用。\n'
    '门① 全池合并复核最大 Jaccard 0.167 < 0.62（通过）；门② 覆盖 6 赛道；OUTDATED/SUPERSEDED 0 篇。等级分布：5 A / 1 B。')

run_log_main = f'''# {DATE} 执行日志

## 数据源与对账（第 1-3 步）
- **漏网对账（先于拉取）**：`scripts/audit_listing_1106.py`（TARGET_DAY=2026-11-04，上批公告日；show=500 单页×7 分类）→ 7 分类最新公告日均为 **2026-11-05**（无漏跑公告日）；**11-04 组逐分类 declared=got**（CV 160/GR 2/HC 21/MM 5/RO 72/AI 252/IV 13，525 槽位）→ 未入馆 **441 篇**，`scripts/run_filter_1106.py` 摘要级复核 **13 篇命中均为 11-05 运行已剔非 XR（与上批 13 篇剔除清单逐篇一致）→ 0 漏网、无 backfill**。
- **摘要级 XR 过滤（新公告组）**：11-05 组 **398 篇唯一论文**（CV 148/GR 7/HC 29/MM 6/RO 62/AI 217/IV 8，477 槽位）→ 摘要级 XR 命中 **22 篇**（`data/missed_xr_abstract_1106.json`，meta fetched 839/839 两组合计）。
- **RSS 主渠道交叉验证**：`scripts/fetch_rss.py` 7 分类全量去重 **647** 条 → KW 命中 **37** = **22 篇 11-05 公告组真新提交（12 篇 XR + 10 篇非 XR）+ 8 篇旧稿 replace/cross 再公告（6 篇 XR → backfill-1106 + 2 篇非 XR 剔除）+ 7 篇库内 v2 再公告（剔除）**。listing 摘要级 22 篇**全部被 RSS 覆盖，RSS 漏网 0 篇**——两渠道互证（`scripts/triage_1106.py` 双向差集 0）。
- **API 探针**：双主机 200；`id_list` 口径核验提交日：主批 **11 篇 2026-11-04 提交 + 1 篇（2611.05593）2026-11-03 提交**（均早于公告日 11-05）。RSS published 字段为公告时间戳（11-05），非提交日，两口径已区分。

## 甄别（第 3 步）
- 主批 XR 核心/强相关 **12 篇**入评分池；剔非 XR **10 篇**（2611.05542 全页广告排序 / 2611.05569 LiDAR 点云分割不确定性 / 2611.05667 PHIL 机器人策略主动干预 / 2611.05741 OUCH 医疗触觉刺激装置 / 2611.05874 Feature Puzzles 多视图三维分割 / 2611.05897 FWIK 机器人逆运动学 / 2611.05936 LumiTac 机器人触觉传感器 / 2611.06068 Fluidic Body 群体机器人有形界面 / 2611.06442 TwinBridge 数字孪生机器人 RL / 2611.06838 上下文感知自回归图像生成）。
- 旧稿 replace/cross 再公告 8 篇中 **6 篇 XR → backfill-1106**（首次入馆，单独编号）；2 篇非 XR 剔除（2608.15968 低成本 4-DoF 机械臂 / 2611.05163 RoboTryOn 机器人演示合成）。
- 库内 v2 再公告 7 篇剔除（2611.05176 MM-AR / 2606.29494 VCS-SLAM / 2610.20590 Feed-Forward MV Feature Coding / 2610.28631 AEON / 2611.03114 3DGS 自学习神经视图相关颜色 / 2611.05359 GSCV++ / 2610.39076 Tactus）。

## 全文抓取（第 4 步）
- 18 篇候选（主批 12 + backfill 6）跑 `scripts/fetch_fulltext.py`，严格串行 3s/篇（约 1 分钟）：**18 篇全部 L0/FULL**（21,776–178,380 字符）。无限流/降级/伪造。
- **人工复核正文中段章节**（防 11-05 ar5iv 摘要页误判教训）：18 篇均含 Method/Experiments/Results/Conclusion 等实质章节，manifest FULL 判定全部确认。
- manifest 合并写入校验通过；WROTE=18>0。

## 评分与三关（第 5-6 步）
- 先抓全文再定稿。7 维加权定稿：主批 **1 S / 5 A / 6 B**（最高 4.57 Open-HumanScale）；backfill **5 A / 1 B**（最高 EgoM2P 4.10）。
- 门① 最大 Jaccard **0.167**（2611.06593 BudgetSplat vs 库内 2610.20590；<0.62，非同质）。
- 门② 纯价值 Top10 覆盖 **4 赛道**（感知与认知×2 / 重建与SLAM×3 / 交互与输入×1 / 神经渲染×4）<5 → **触发一次重筛**：剔除神经渲染赛道最低分 BudgetSplat 3.51，回补未覆盖核心赛道（空间计算与UI）B 级池最高分 VR HIIT 3.18 → 定稿 Top10 覆盖 **5 赛道** ≥5，通过（BudgetSplat 仍入馆写 B 级笔记，仅不占 Top10 名额，同 11-04 SHield 先例）。
- 门③ 当日最高 **4.57 ≥ 库内近 30 天 Top10 均分 4.363**（窗口 2026-10-07~11-06、428 条入窗、现算）→ **重磅日，可评 S 级；全批 1 篇 S（Open-HumanScale 4.57），按实数定级未拔高**。
- OUTDATED/SUPERSEDED **0 篇**。路线级观察：① 前馈 3DGS 效率线三篇同批——CrossPressor（fusion 侧 26×）、BudgetSplat（表示侧预算控制）、GaussianRenderFormer（渲染侧无光栅化探索），与库内 ZPressor/pixelSplat/MVSplat 主线构成「表示-融合-渲染」全链路优化图景；② 第一人称数据链闭环——backfill EgoGen（合成）→ EgoM2P（统一预训练）→ Open-HumanScale（50k 小时开放缩放配方）三篇同批互证，AR 眼镜数据基础设施日趋完整；③ 度量尺度与 AR 落地——METRIC-GS（从重建自身读尺度+弃权路由）与 PVLC 投影 AR（8ms 低延迟三维定位）从内容放置与空间配准两端补 AR 工程实证；④ 硬件类缺口仍仅 CVQPG + HoOPOE 两篇涉及近眼显示光学（本批无波导/可变焦/Maxwellian/光场新文献）。

## 产物（第 7-8 步）
- 报告 2 份（主报告 + backfill 报告）+ 原子笔记 18 篇（grade≥B：主批 12 + backfill 6，无 C 级）+ MOC 2 份 + 总索引刷新 + 7 维表/scored/run_log 各 2 套。
- registry 790 → **808**（+12 主批 +6 backfill；备份 `papers/library/registry.jsonl.bak-20261106`；按 base_id 幂等）。
'''
open(f'papers/daily/{DATE}/run_log.md', 'w', encoding='utf-8').write(run_log_main)

run_log_bf = f'''# {BFB} 执行日志

- **批次性质**：backfill（非当日新提交）——11-05 公告批次中 RSS 混入的旧稿 replace/cross 再公告 6 篇首次入馆；原始投稿 2401=2024-01-16 / 2506=2025-06-09 / 2511=2025-11-21 / 2604=2026-04-27 / 2607=2026-07-16 / 2611=2026-10-30（arXiv ID 前缀；v2-v4 于 2026-11-04 更新）。
- **来源**：`scripts/fetch_rss.py` 7 分类全量去重 647 → KW 命中 37；其中 8 篇旧稿再公告经 XR 甄别保留 6 篇（剔非 XR 2 篇：低成本 4-DoF 机械臂 / RoboTryOn 机器人演示合成）。
- **全文**：6 篇全部 L0/FULL，串行 3s/篇，无限流/降级/伪造。
- **评分**：5 A / 1 B（最高 EgoM2P 4.10，无 S 线）。门① 全池合并复核最大 Jaccard 0.167 < 0.62；门② 覆盖 6 赛道；门③ 不适用；OUTDATED 0。
- **诚实口径**：全部条目 `batch=backfill-1106` + `orig_window` 标注，绝不混入「当日新论文」。
'''
open(f'papers/daily/{BFB}/run_log.md', 'w', encoding='utf-8').write(run_log_bf)

# ---------- 3. registry（先备份，幂等追加，in_top10 显式） ----------
reg_path = 'papers/library/registry.jsonl'
bak_path = reg_path.replace('.jsonl', '.jsonl.bak-20261106')
if not os.path.exists(bak_path):   # 重跑时保留首跑的追加前快照，勿覆盖
    shutil.copy(reg_path, bak_path)
rows = [json.loads(l) for l in open(reg_path, encoding='utf-8') if l.strip()]
have = {r['id'].split(':')[-1].split('v')[0] for r in rows}
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
            entry['orig_window'] = p['orig_window']
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

moc(MAIN, f'papers/MOC/MOC-{DATE}.md', f'MOC · {DATE}（11-05 公告批次）',
    '> 当日地图：**公告日 2026-11-05（周四）≠ 拉取日 2026-11-06（周五 02:30）**——诚实口径。API published 口径核验提交日 **主批 11 篇为 2026-11-04 提交 + 1 篇为 2026-11-03 提交**。\n'
    '> 主批 XR 新稿 12 篇（1 S / 5 A / 6 B，**重磅日含 1 篇 S**）；listing 与 RSS 两渠道互证 22 篇真新提交中 12 篇 XR（RSS 漏网 0 篇）；全文 18 篇候选全 L0/FULL。\n'
    '> 覆盖度三关：门① 0.167 / 门② 纯价值 Top10 仅 4 赛道触发一次重筛（BudgetSplat 让位 VR HIIT）后定稿 Top10 覆盖 5 赛道 / 门③ 4.57 ≥ 4.363（现算，428 条入窗）→ 重磅日，1 篇 S。\n'
    '> Top10（实数 10 篇）：Open-HumanScale 4.57 S · METRIC-GS 4.00 · 尺度锚定 VGGT-SLAM 3.96 · TouchéWorld 3.88 · CrossPressor 3.83 · OccSplat 3.64 · GaussianRenderFormer 3.55 · 反射鲁棒 Stereo VIO 3.47 · PVLC 三维位姿 3.44 · 智能手机 VR HIIT 3.18。')
moc(BF, f'papers/MOC/MOC-{BFB}.md', f'MOC · {BFB}（旧稿再公告补录）',
    '> 本批为 **backfill**：11-05 公告批次 RSS 混入的旧稿 replace/cross 再公告 6 篇首次入馆（原始投稿 2401=2024-01 / 2506=2025-06 / 2511=2025-11 / 2604=2026-04 / 2607=2026-07 / 2611=2026-10），**均非当日新提交**。\n'
    '> 5 A / 1 B；最高 EgoM2P 4.10（无 S 线）。门① 0.167 / 门② 6 赛道 / 门③ 不适用。')

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
    np_ = sum(1 for p in papers if p['evidence'] == 'PARTIAL')
    L.append(f'- 本表 {len(papers)} 篇：FULL {nf} 篇；PARTIAL {np_} 篇；ABSTRACT_ONLY 0 篇。')
    L.append('- 抓取降级：无。18 篇候选（主批 12 + backfill 6）全部 L0/FULL（21,776–178,380 字符），人工复核正文中段均含实质章节（排除 ar5iv 摘要页误判），串行 3s/篇，无限流、无 L5、无 OCR、无伪造。')
    open(path, 'w', encoding='utf-8').writelines([x + '\n' for x in L])

report(TOP10,
       f'reports/XR-Daily-Report-{DATE}.md',
       f'XR 每日论文解读报告 · {DATE}（11-05 公告批次）',
       '## 一、执行摘要\n'
       f'- **公告日 2026-11-05（周四）≠ 拉取日 2026-11-06（周五 02:30）**——诚实口径：本批处理的是 11-05 公告批次；API published 口径核验提交日 **主批 11 篇为 2026-11-04 提交 + 1 篇为 2026-11-03 提交**（均早于公告日，非当日硬提交；RSS published 为公告时间戳非提交日）。\n'
       '- **主批 XR 新稿 12 篇（1 S / 5 A / 6 B；重磅日，Top10 实数 10 篇）**。Top10：**Open-HumanScale 4.57（S，北京大学 DAGroup，开放 50,000 小时第一人称语料与全栈训练配方，下游 OOD 成功率遵循 log-linear 缩放定律 R²=0.877–0.971，RoboTwin 2.0 上 HumanWAM-Goal 平均 88.65% 创 SOTA，真机零样本 20 项任务平均 20.0%→30.5%，全栈开源）** · METRIC-GS 4.00（从 3DGS 重建自身语义内容读取度量尺度并以弃权为一等输出，47 个 ScanNet++ 场景尺度误差 21.1%→16.6%，选择性路由以 60% 更少调用匹配全量 MASt3R，直接服务 AR 内容放置） · 尺度锚定 VGGT-SLAM 3.96（SALAD 引导 fixed-root 尺度锚定 + 短序列验证 direct Sim(3) 回环，TUM 平均 ATE -55.6%、LaMAR -92.5%，代码开源） · TouchéWorld 3.88（首个统一相机-手部在线交互的视频世界模型，双向教师较纯相机基线 PSNR +2.82 dB，TouchéBench 四维评测，权重与数据将发布） · CrossPressor 3.83（training-free coverage-cycled evidence routing，256 视图 cross-view fusion 26.12× 加速、p5 ΔPSNR 仅 -0.0063 dB） · OccSplat 3.64（遮挡感知高斯致密化把驾驶重建遮挡处理从图像空间搬到 3D 表示空间，nuScenes PSNR +1.74 dB，遮挡区 LPIPS 0.194→0.182） · GaussianRenderFormer 3.55（首个渲染路径无光栅化器的前馈高斯渲染器——诚实的负面结果：38.08 dB vs 光栅化 44.02 dB、慢数百倍，但诊断完整且 MIT 开源） · 反射鲁棒 Stereo VIO 3.47（Kalman 滤波地面高度估计选择性剔除地面以下虚拟特征，6/8 序列改善、DynaVINS 4 条发散序列恢复收敛） · PVLC 三维位姿 3.44（首次把 PnP 引入像素级可见光通信，8 ms 延迟、RMSE 19.2 mm，高速下误差增长远小于相机 AR 标记） · 智能手机 VR HIIT 3.18（门②回补项，三脚架手机 + MediaPipe + GPT-4o + Quest 3 的低成本 VR 健身平台，N=20 被试内实验 enjoyment 显著提升）。\n'
       '- **覆盖 5 赛道**：感知与认知×2 / 重建与SLAM×3 / 交互与输入×1 / 神经渲染×3 / 空间计算与UI×1（全批 6 赛道）。\n'
       '- **覆盖度三关**：门① 0.167；门② 纯价值 Top10 仅 4 赛道 → **触发一次重筛**（剔除神经渲染冗余的 BudgetSplat 3.51、回补空间计算与UI 赛道 VR HIIT 3.18），定稿 Top10 覆盖 5 赛道 ≥5（通过）；门③ 当日最高 4.57 ≥ 库内近 30 天 Top10 均分 4.363（现算，428 条入窗）→ **重磅日，1 篇 S 级**（校准关达标，按实数定级未拔高）。\n'
       '- **全文证据**：18 篇候选（主批 12 + backfill 6）**全部 L0/FULL**（21,776–178,380 字符；人工复核正文中段均含实质章节，无 ar5iv 摘要页误判）。\n'
       '- **同批 backfill-1106**：RSS 混入旧稿 replace/cross 再公告 6 篇首次入馆（5 A / 1 B，最高 EgoM2P 4.10），与主批 Open-HumanScale 构成「第一人称数据生成→统一预训练→开放缩放配方」完整链路，详见 [XR-Backfill-Report-backfill-1106.md](XR-Backfill-Report-backfill-1106.md)。',
       DATE, 10,
       ['- 门①（同质去重）：最大 Jaccard 0.167 < 0.62，通过，无同质重复。',
        '- 门②（赛道覆盖）：纯价值 Top10 覆盖 4 赛道（神经渲染×4 冗余）<5 → 触发一次重筛——剔除神经渲染赛道最低分 BudgetSplat 3.51（仍入馆写 B 级笔记仅不占名额，同 11-04 SHield 先例），回补未覆盖核心赛道（空间计算与UI）B 级池最高分 VR HIIT 3.18 → 定稿 Top10 覆盖 5 赛道（感知与认知×2 / 重建与SLAM×3 / 交互与输入×1 / 神经渲染×3 / 空间计算与UI×1）≥5，通过；全批 6 赛道。',
        '- 门③（价值天花板）：当日最高分 4.57 ≥ 库内近 30 天 Top10 均分 4.363（现算，428 条入窗）→ **重磅日，可评 S 级**；全批 1 篇 S（Open-HumanScale 4.57），按实数定级、未拔高；A 级 5 篇、B 级 6 篇（含 2 篇门②相关：BudgetSplat 让位、VR HIIT 回补）。',
        '- 低量日不凑数原则复核：本批 grade≥B 共 12 篇（主批），Top10 取实数 10 篇（1 S + 5 A + 3 B + 1 门②回补 B），余 2 篇 B 级入馆写笔记，无 C 级、未降格凑数。',
        '- OUTDATED/SUPERSEDED 0 篇。\n'])

report(BF, f'reports/XR-Backfill-Report-{BFB}.md',
       f'XR Backfill 补录报告 · {BFB}（旧稿再公告）',
       '## 一、执行摘要\n'
       '- **批次性质**：backfill（非当日新提交）——11-05 公告批次中 RSS 混入的旧稿 replace/cross 再公告 6 篇，首次入馆；原始投稿 2401=2024-01-16 / 2506=2025-06-09 / 2511=2025-11-21 / 2604=2026-04-27 / 2607=2026-07-16 / 2611=2026-10-30（v2-v4 于 2026-11-04 更新）。\n'
       '- **补录 6 篇（5 A / 1 B）**：EgoM2P 4.10（上海科技大学等，首个第一人称 4D 多模态多任务模型，统一 temporal tokenizer 离散化 RGB/depth/gaze/camera 四模态，匹配或超越 specialist SOTA 且推理快一个数量级——60 帧相机轨迹 0.18 s）· AEGIS 4.09（滑铁卢大学等，首个面向 3D Gaussian avatar 的身份遮蔽框架，仅扰动 DC 球谐系数即把黑盒验证率压到近零（ε=0.2 时 0%）、保持 SSIM 0.9347/PSNR 32.66 dB 且无渲染开销，代码开源）· EgoGen 3.93（上海科技大学，PPO 训练的 collision-avoiding motion primitives 驱动第一人称合成数据生成，LaMAR 建图定位 recall 66.9%→76.7%、EgoBody 人体 mesh recovery G-MPJPE -22.9%）· EvSLAM 3.69（湖南大学，四平台 19 条室内高速机动序列 + 12 个 SOTA 方法两批评测，指出现有立体事件数据集时空不一致（左右事件数差 10%–86%）并主张 VGA 为当前最适用分辨率，数据集公开）· PIDiffSign 3.68（萨里大学等，首个把刚体动力学引入手语产生——FK 输出头 + Newton-Euler 先验，back-translation WER 降约 5 个点）· AuroraWorld 3.57（中科院自动化所等，从稀疏外部观测推断结构化 4D 世界表征指导 ego 视频生成，DROID PSNR 17.87/FVD 60.17 全面优于 6 基线，真机策略 70.7% 对真实 ego 78.0%）。\n'
       '- **覆盖 6 赛道**；门① 0.167（全池合并复核）；门③ 对 backfill 不适用；OUTDATED 0。\n'
       '- **诚实口径**：全部条目 `batch=backfill-1106` + `orig_window` 标注，绝不混入「当日新论文」。',
       BFB, 6,
       ['- 门①（同质去重）：全池合并复核最大 Jaccard 0.167 < 0.62，通过，无同质重复。',
        '- 门②（赛道覆盖）：覆盖 6 赛道（感知与认知×2 / 化身与人体×2 / 评估与数据集×1 / 世界模型与仿真×1），6 篇低量批次实际上限。',
        '- 门③（价值天花板）：对 backfill 不适用；本批 6 篇均未达 S 线（最高 4.10），按实数定级，未拔高。',
        '- OUTDATED/SUPERSEDED 0 篇。\n'])

# ---------- 7. MOC-总索引刷新 ----------
moc_path = 'papers/MOC/MOC-总索引.md'
h = open(moc_path, encoding='utf-8').read()
n0 = len(h)

def rep(old, new, tag):
    global h
    assert old in h, f'ANCHOR NOT FOUND: {tag}'
    h = h.replace(old, new, 1)

# 7.1 头部计数与批次枚举
rep('累计 **790 篇**；跨度 2026-09-15 ~ 2026-11-04',
    '累计 **808 篇**；跨度 2026-09-15 ~ 2026-11-05', 'head-count')
rep('**backfill-1105:8（11-04 公告 RSS 混入旧稿 replace/cross 再公告，首次入馆）**；',
    '**backfill-1105:8（11-04 公告 RSS 混入旧稿 replace/cross 再公告，首次入馆）** · '
    '**2026-11-06:12（11-05 公告批次真新提交，重磅日含1S；listing+RSS 两渠道互证 22 篇中 12 篇 XR）** · '
    '**backfill-1106:6（11-05 公告 RSS 混入旧稿 replace/cross 再公告，首次入馆）**；', 'batch-list')
rep('**11-05 周四处理 11-04 公告批次（9 篇 XR 新稿 5A/2B/2C + backfill-1105 补录 8 篇 3A/5B，非重磅日无S）**。',
    '**11-05 周四处理 11-04 公告批次（9 篇 XR 新稿 5A/2B/2C + backfill-1105 补录 8 篇 3A/5B，非重磅日无S）**；'
    '**11-06 周五处理 11-05 公告批次（12 篇 XR 新稿 1S/5A/6B 重磅日 + backfill-1106 补录 6 篇 5A/1B）**。',
    'narrative')

# 7.2 追加 11-06 状态注记（在 11-05 注记后）
note06 = ('> **状态注记（2026-11-06）**：周五 02:30，处理 **2026-11-05（周四）公告批次**（公告日≠拉取日，诚实口径；API published 口径核验提交日 **主批 11 篇为 2026-11-04 提交 + 1 篇为 2026-11-03 提交**，RSS published 为公告时间戳非提交日）。'
 '漏网对账（先于拉取，TARGET_DAY=2026-11-04）：listing 7 分类最新公告日均为 **11-05**（无漏跑公告日）；11-04 组复采逐分类 **declared=got**（CV 160/GR 2/HC 21/MM 5/RO 72/AI 252/IV 13，525 槽位），未入馆 **441 篇**摘要级复核 **13 篇命中均为 11-05 运行已剔非 XR（逐篇一致）→ 0 漏网、无 backfill**；**11-05 组 398 篇唯一论文**（CV 148/GR 7/HC 29/MM 6/RO 62/AI 217/IV 8，477 槽位）摘要级 XR 命中 **22 篇**。'
 'RSS 7 分类去重 **647** → KW 命中 37 = **22 篇 11-05 公告组真新提交（12 XR + 10 非 XR）+ 8 篇旧稿 replace/cross 再公告（6 XR → backfill-1106 + 2 非 XR）+ 7 篇库内 v2**；listing 摘要级 22 篇全部被 RSS 覆盖（**RSS 漏网 0 篇**，两渠道互证，双向差集 0）。'
 '主批甄别 **XR 核心/强相关 12 篇**（剔非 XR 10 篇：全页广告排序/LiDAR 点云分割不确定性/PHIL 机器人策略干预/OUCH 医疗触觉刺激/Feature Puzzles 多视图分割/FWIK 机器人 IK/LumiTac 机器人触觉传感器/Fluidic Body 群体机器人有形界面/TwinBridge 数字孪生机器人 RL/自回归图像生成）；全文 **18 篇候选（主批 12 + backfill 6）全部 L0/FULL**（21,776–178,380 字符，人工复核正文中段章节排除 ar5iv 摘要页误判）。'
 'Top10（**实数 10 篇**）：最高 **4.57（Open-HumanScale），重磅日含 1 篇 S**；覆盖 5 赛道（感知与认知×2/重建与SLAM×3/交互与输入×1/神经渲染×3/空间计算与UI×1；全批 6 赛道）。'
 '三关：门① max Jaccard **0.167**（2611.06593 vs 库内 2610.20590）；门② 纯价值 Top10 仅 4 赛道（神经渲染×4 冗余）→ **触发一次重筛**（剔除 BudgetSplat 3.51、回补空间计算与UI 赛道 VR HIIT 3.18）后定稿 Top10 覆盖 5 赛道 ≥5（通过）；门③ 当日最高 4.57 ≥ 库内近 30 天 Top10 均分 **4.363**（428 条入窗，现算）→ **重磅日，1 篇 S 级，未拔高**；OUTDATED 0。'
 '**backfill-1106**：旧稿 replace/cross 再公告 6 篇首次入馆（5 A / 1 B，最高 EgoM2P 4.10，无 S 线；原始投稿 2401/2506/2511/2604/2607/2611）。'
 'registry 790 → **808**（+12 +6）。详见 [运行报告](../../reports/XR-Daily-Report-2026-11-06.md) 与 [MOC-2026-11-06](./MOC-2026-11-06.md) / [MOC-backfill-1106](./MOC-backfill-1106.md) / [Backfill 报告](../../reports/XR-Backfill-Report-backfill-1106.md)。\n')
anchor_end = '[Backfill 报告](../../reports/XR-Backfill-Report-backfill-1105.md)。'
i = h.find(anchor_end)
assert i >= 0, 'ANCHOR NOT FOUND: note1105-end'
j = h.find('\n', i) + 1
h = h[:j] + note06 + h[j:]

# 7.3 速查入口
rep('| 最新一期 | [MOC · 2026-11-05](./MOC-2026-11-05.md) |',
    '| 最新一期 | [MOC · 2026-11-06](./MOC-2026-11-06.md) |', 'quick-latest')
rep('| 上一期 | [MOC · 2026-11-04](./MOC-2026-11-04.md) |',
    '| 上一期 | [MOC · 2026-11-05](./MOC-2026-11-05.md) |', 'quick-prev')
rep('（现有 464 篇）', '（现有 482 篇）', 'quick-notes')
rep('| 最新运行状态 | [运行报告 2026-11-05](../../reports/XR-Daily-Report-2026-11-05.md)（11-04 公告批次 9 篇 5A/2B/2C 非重磅日无S + backfill-1105 补录 8 篇 3A/5B；listing 450 篇+RSS 两渠道互证 22 篇中 9 篇 XR，RSS 漏网 0 篇；全文 16×L0/FULL + 1×L1/PARTIAL；Top10 实数 7 篇覆盖 5 赛道） |',
    '| 最新运行状态 | [运行报告 2026-11-06](../../reports/XR-Daily-Report-2026-11-06.md)（11-05 公告批次 12 篇 1S/5A/6B 重磅日 + backfill-1106 补录 6 篇 5A/1B；listing 398 篇+RSS 两渠道互证 22 篇中 12 篇 XR，RSS 漏网 0 篇；全文 18×L0/FULL；门② 触发一次重筛回补 VR HIIT，Top10 实数 10 篇覆盖 5 赛道） |', 'quick-status')

# 7.4 批次索引表追加两行
row_main = ('| 2026-11-06 | [MOC-2026-11-06](./MOC-2026-11-06.md) | XR 12（Top10 实数 10）· 1S/5A/6B · 重磅日（1S） | '
            '11-05 公告批次真新提交 12 篇（11 篇 11-04 提交 + 1 篇 11-03 提交）；listing 398 篇+RSS 两渠道互证 22 篇中 12 篇 XR；全文 18×L0/FULL |')
row_bf = ('| backfill-1106 | [MOC-backfill-1106](./MOC-backfill-1106.md) | 补录 6（5A/1B）· 非当日新提交 | '
          '11-05 公告 RSS 混入旧稿 replace/cross 再公告 6 篇（2401/2506/2511/2604/2607/2611） |')
rep('| backfill-1105 | [MOC-backfill-1105](./MOC-backfill-1105.md) | 补录 8（3A/5B）· 非当日新提交 | 11-04 公告 RSS 混入旧稿 replace/cross 再公告 8 篇（2603×2/2606×4/2607×1/2608×1） |',
    '| backfill-1105 | [MOC-backfill-1105](./MOC-backfill-1105.md) | 补录 8（3A/5B）· 非当日新提交 | 11-04 公告 RSS 混入旧稿 replace/cross 再公告 8 篇（2603×2/2606×4/2607×1/2608×1） |\n'
    + row_main + '\n' + row_bf, 'batch-table')

# 7.5 S 级总表：标题计数 16→17；追加 11-06 S 级段（在 10-20 S 级段后）
rep('## 二、等级总表（S 级 16 篇全量 · A 级 32 篇基线总表 + 各批次新增段）',
    '## 二、等级总表（S 级 17 篇全量 · A 级 32 篇基线总表 + 各批次新增段）', 'level-head')
seg_s = ('\n### 2026-11-06 新增（S 级，1 篇，重磅日）\n\n'
 '> 公告日 2026-11-05（周四；公告日≠拉取日 11-06，诚实口径；提交日 11 篇 11-04 + 1 篇 11-03）。当日最高 4.57 ≥ 库近 30 天 Top10 均分 4.363（现算，428 条入窗），**重磅日含 S 级**；18 篇候选全文全 L0/FULL；三关通过（门① 0.167；门② 触发一次重筛后定稿 Top10 覆盖 5 赛道），无 OUTDATED。\n\n'
 '| 论文 | 赛道 | 分值 | 公告日 | 状态 | 笔记 |\n|---|---|---:|---|---|---|\n'
 '| **Open-HumanScale 人机经验规模化开放配方** | 感知与认知 | 4.57 | 11-05 | ✅ | [→](../notes/2611.06817__open-humanscale-an-open-recipe-for-scaling-human-and-robot-experience-for-embodied-foundation-models.md) |\n')
anchor_s = '| **dGS 直接条件参数化 N 维泼溅** | 神经渲染 | 4.30 | 10-19 | ✅ | [→](../notes/2610.22778__direct-conditional-parameterization-nd-splatting.md) |\n'
i = h.find(anchor_s)
assert i >= 0, 'ANCHOR NOT FOUND: s-table-1020-end'
j = h.find('\n', i) + 1
h = h[:j] + seg_s + h[j:]

# 7.6 追加 Top10 段（文件尾）
seg = '\n### 2026-11-06 新增（Top10 实数 10 篇：1 S + 5 A + 3 B + 1 门②回补 B，重磅日）\n\n| # | 论文 | 赛道 | 分值 | 等级 | 证据 |\n|---:|---|---|---:|---|---|\n'
for i2, pid in enumerate(TOP10_ORDER, 1):
    p = next(x for x in MAIN if x['id'] == pid)
    seg += f"| {i2} | {esc(p['title_zh'])} | {p['track']} | {p['value']:.2f} | {p['grade']} | {p['evidence']} |\n"
seg += '\n### backfill-1106 补录（6 篇：5 A + 1 B，非当日新提交）\n\n| # | 论文 | 赛道 | 分值 | 等级 | 证据 |\n|---:|---|---|---:|---|---|\n'
for i2, p in enumerate(BF, 1):
    seg += f"| {i2} | {esc(p['title_zh'])} | {p['track']} | {p['value']:.2f} | {p['grade']} | {p['evidence']} |\n"
h = h.rstrip() + '\n' + seg

# 7.7 页脚计数
rep('*最后更新：2026-11-05（11-04 公告批次：9 篇 XR 新稿 5A/2B/2C 非重磅日无S + backfill-1105 补录 8 篇 3A/5B；listing 450 篇+RSS 两渠道互证 22 篇中 9 篇 XR，RSS 漏网 0 篇；全文 16×L0/FULL + 1×L1/PARTIAL；Top10 实数 7 篇覆盖 5 赛道；门③ 现算 4.429） · 库内 **790 篇** · 原子笔记 **464 篇** · MOC 40 份',
    '*最后更新：2026-11-06（11-05 公告批次：12 篇 XR 新稿 1S/5A/6B 重磅日 + backfill-1106 补录 6 篇 5A/1B；listing 398 篇+RSS 两渠道互证 22 篇中 12 篇 XR，RSS 漏网 0 篇；全文 18×L0/FULL；门② 触发一次重筛（BudgetSplat→VR HIIT）；门③ 现算 4.363，当日最高 4.57 达重磅日线，1 篇 S） · 库内 **808 篇** · 原子笔记 **482 篇** · MOC 42 份',
    'footer')

open(moc_path, 'w', encoding='utf-8').write(h)
print('MOC-总索引 refreshed（%d -> %d chars）' % (n0, len(h)))
print('DONE')
