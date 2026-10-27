# -*- coding: utf-8 -*-
"""2026-10-28 产物生成：主批（10-27 公告批次 26 篇）+ backfill-1028（旧稿再公告 10 篇）。
消费 data/scored_1028.json；registry 幂等追加（先备份，in_top10 按定稿 Top10 显式设置）；
生成 7 维表/scored/run_log/笔记/MOC/报告并刷新总索引。"""
import json, os, shutil, glob

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
os.chdir(ROOT)
D = json.load(open('data/scored_1028.json', encoding='utf-8'))
MAIN, BF = D['main'], D['backfill']
DATE, BFB = '2026-10-28', 'backfill-1028'
GATE3 = 4.416          # 门③ 现算均分（窗口 2026-09-28~10-28，431 条入窗）
TODAY_MAX = MAIN[0]['value']  # 4.35
TOP10 = MAIN[:10]      # 定稿 Top10（同分 IMP/NOV→赛道多样性→id 升序；3.85 组 6 篇同分同 IMP/NOV，候选赛道均已被覆盖，按 id 升序取前二）
TOP10_IDS = {p['id'] for p in TOP10}

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
        lines.append(dim_row(p, i < topn) + '\n')
    open(path, 'w', encoding='utf-8').writelines(lines)

os.makedirs(f'papers/daily/{DATE}', exist_ok=True)
os.makedirs(f'papers/daily/{BFB}', exist_ok=True)

seven_table(MAIN, f'papers/daily/{DATE}/7dim-table.md',
    f'{DATE} 全量 7 维度对比表（参考）',
    '批次：2026-10-28（**2026-10-27（周二）公告批次**；公告日 10-27 ≠ 拉取日 10-28 02:30，诚实口径）。\n'
    '候选池 26 篇：listing 对账 10-27 公告组 794 篇 → 摘要级 XR 命中 41 篇；RSS 7 分类去重 1047 → KW 命中 67 = **44 篇 2610.* 真新提交 + 15 篇旧稿 replace/cross 再公告 + 8 篇库内 v2 再公告**；listing 摘要级 41 篇全部被 RSS 覆盖（**RSS 漏网 0 篇**，两渠道互证）。44 篇真新中甄别 XR 核心/强相关 **26 篇**入评分池，剔非 XR 18 篇（机器人抓取/VLA/航空 VLN/灵巧手采集/医学影像×3/医学配准/光子逆设计/人形机器人×2/建筑场景图/施工文档/视频蒸馏/社交机器人 HRI/抓取合成/机器人到达/空间 VPR 等）。\n'
    'RSS 同批另混入 15 篇旧稿 replace/cross 再公告（10 篇 XR → backfill-1028）+ 8 篇库内 v2 再公告剔除。\n'
    '全文：26 篇候选 **25 篇 L0/FULL + 1 篇 L1/FULL**（2610.34223 单相机试穿化身：ar5iv 转换版 5,083 字符，无实验章节，按摘要级评估并显式声明）；先抓全文再定稿。\n'
    '覆盖度三关：门① 最大 Jaccard **0.083**（2610.35224 GaussianSpline vs 库内 2610.26918，<0.62 通过）；门② Top10 覆盖 **8 赛道**（渲染与显示/系统与平台/化身与人体/神经渲染/评估与数据集/重建与SLAM/感知与认知/内容生成，≥5 通过）；门③ 当日最高 **4.35 < 库内近 30 天 Top10 均分 4.416**（431 条入窗，现算）→ **非重磅日、无 S 级**，未拔高。RacerGS 4.35 达 S 线按校准关记 A（同 10-24 EgoHand / 10-27 WFM 先例）。',
    len(TOP10))

seven_table(BF, f'papers/daily/{BFB}/7dim-table.md',
    f'{BFB} 全量 7 维度对比表（参考）',
    '批次：backfill-1028（**10-27 公告批次中 RSS 混入的旧稿 replace/cross 再公告**（首次入馆；原始投稿月 2601/2602/2603/2604/2605/2606/2609）；均非 10-27 当日新提交，诚实口径单独编号）。\n'
    '候选 10 篇：2609.31418 CognitiveReality（VR 遥操作语义高斯映射）/ 2609.02847 RoGe（端到端隐式重建+生成 NVS）/ 2602.13444 FlowHOI（手物交互流匹配生成）/ 2603.28064 4DSurf（动态表面重建）/ 2605.18553 StableHand（质量感知双手估计）/ 2605.31352 Haptic Sorter（触觉探索+可微操作）/ 2604.07279 Mem3R（混合记忆流式重建）/ 2605.30488 CoMo3R-SLAM（协同单目稠密 SLAM）/ 2606.01950 MRO-GWM（物体中心高斯世界模型）/ 2601.00913 CleanGS（免训练 3DGS 场景清理）。全部 L0/FULL 全文后定稿。\n'
    '门③ 对 backfill 不适用；本批不参与当日「重磅日」判定。门① 最大 Jaccard 0.076（4DSurf vs 库内 2609.23509，<0.62 通过）；门② 覆盖 8 赛道（空间计算与UI/神经渲染/内容生成/重建与SLAM/化身与人体/触觉与多模态/世界模型与仿真）。\n'
    '注：CognitiveReality 4.30 / RoGe 4.27 / FlowHOI 4.23 加权达 S 线（≥4.2），但当日最高分 4.35 < 库内近 30 天 Top10 均分 4.416 → 非重磅日，按校准关记 A 级（同 10-24 EgoHand / 10-27 WFM 先例；分数如实保留）。',
    len(BF))

# ---------- 2. scored.md + run_log.md ----------
def scored_md(papers, path, title, extra):
    L = [f'# {title}\n', extra + '\n', '| 排名 | arXiv | 标题 | 赛道 | 总分 | 等级 | 证据 | 公告类型 |',
         '|---|---|---|---|---|---|---|---|']
    for i, p in enumerate(papers, 1):
        L.append(f"| {i} | {p['id']} | {esc(p['title_zh'])} | {p['track']} | {p['value']:.2f} | {p['grade']} | {p['evidence']} | {p['announce']} |")
    open(path, 'w', encoding='utf-8').writelines([x + '\n' for x in L])

scored_md(MAIN, f'papers/daily/{DATE}/scored.md', f'{DATE} 评分明细',
    '评分口径：7 维加权 IMP0.20·NOV0.20·TEC0.15·EXP0.15·PER0.15·TRL0.08·REP0.07；分档 S≥4.2 / A3.6–4.2 / B3.0–3.6 / C<3.0。全部基于全文证据定稿（2610.34223 为 L1 ar5iv 摘要级，显式声明）。\n'
    f'覆盖度三关：门① 最大 Jaccard 0.083 < 0.62（通过，非同质）；门② Top10 覆盖 8 赛道 ≥ 5（通过）；门③ 当日最高 4.35 < 库内近 30 天 Top10 均分 4.416（现算，431 条入窗）→ 非重磅日、无 S 级（校准关，不触发重筛；RacerGS 4.35 达 S 线按校准关记 A）。\n'
    'OUTDATED/SUPERSEDED 0 篇。等级分布：18 A / 6 B / 2 C。')
scored_md(BF, f'papers/daily/{BFB}/scored.md', f'{BFB} 评分明细',
    '评分口径同上。本批为旧稿 replace/cross 再公告首次入馆（非当日新提交），门③ 不适用。\n'
    '门① 最大 Jaccard 0.076 < 0.62（通过）；门② 覆盖 8 赛道 ≥ 5（通过）；OUTDATED/SUPERSEDED 0 篇。等级分布：9 A / 1 B。')

run_log_main = f'''# {DATE} 执行日志

## 数据源与对账（第 1-3 步）
- **漏网对账（先于拉取）**：`scripts/audit_gap_listing.py`（TARGET_LO=2026-10-26，上一批次公告日）7 分类采集。listing 最新公告日 = **2026-10-27**（10-24/10-25 周末无公告日段；10-26 组复采一致）。**10-27 组 794 篇全部未入馆**（新公告批次）；10-26 组 358 篇摘要级复核：11 篇命中均为 10-27 运行已显式剔除的非 XR 稿 → **0 漏网**。
- **摘要级 XR 过滤**：`scripts/filter_missed_xr_abstract.py`（MIN_DAY=2026-10-26）→ 1,145 篇取回 1,145 条 API 元数据，XR 命中 **52 篇**（10-26 组 11 + 10-27 组 41）。
- **RSS 主渠道交叉验证**：`scripts/fetch_rss.py` 7 分类全量去重 1047 条 → KW 命中 67 = **44 篇 2610.* 真新提交 + 15 篇旧稿 replace/cross 再公告 + 8 篇库内 v2 再公告**。listing 摘要级 41 篇（10-27 组）**全部被 RSS 覆盖，RSS 漏网 0 篇**——两渠道互证（探针 02:30 时 RSS 命中 50 条、fetch 时 67 条，feed 更新中现象仍存在，但 listing 层兜底证明无实质漏网）。
- **API 探针**：export.arxiv.org / arxiv.org/api/query 均可达（200）；`submittedDate` 前沿停滞 10-22，真实新增由 RSS+listing 双渠道获得。

## 甄别（第 3 步）
- 主批 XR 核心/强相关 **26 篇**入评分池；剔非 XR **18 篇**（2610.24016 抓取编排 / 2610.32697 航空 VLN / 2610.32969 灵巧手采集 / 2610.33071 脑灌注数字孪生 / 2610.33124 医学 INR / 2610.33317 人形可达性 / 2610.33554 前列腺分割 / 2610.33685 跨本体 VLA / 2610.34041 激光雷达施工场景图 / 2610.34092 视频蒸馏 / 2610.34186 人形 VLA / 2610.34534 社交机器人 HRI / 2610.34600 医学配准 / 2610.34632 驾驶场景反射去除 / 2610.34893 多模态抓取 / 2610.35626 腕部相机 VLA 到达 / 2610.35642 空间域 VPR）。
- 旧稿 replace/cross 再公告 15 篇中 **10 篇 XR → backfill-1028**（首次入馆，单独编号）；5 篇非 XR 剔除（2511.22459 火焰重建 VFX / 2604.05475 眼动阅读检测 / 2606.19609 施工适配记录 / 2606.29924 可控抓取生成 / 2609.15213 人形全身控制）。
- 库内 v2 再公告 8 篇剔除（2412.01090 / 2601.00705 / 2601.14895 / 2607.01202 / 2610.27712 / 2610.28402 / 2610.29014 / 2610.30089）。

## 全文抓取（第 4 步）
- 36 篇候选（主批 26 + backfill 10）跑 `scripts/fetch_fulltext.py`，严格串行 3s/篇（约 2 分 21 秒）：**35 篇 L0/FULL**（23,720–166,062 字符）+ **1 篇 L1/FULL**（2610.34223 单相机试穿化身：ar5iv 转换版仅 5,083 字符、无实验章节 → 按摘要级评估并在 7 维表/笔记/报告显式声明，禁止脑补）。无限流/降级/伪造。
- manifest 合并写入校验通过；WROTE=36>0。

## 评分与三关（第 5-6 步）
- 先抓全文再定稿。7 维加权定稿：主批 18 A / 6 B / 2 C（最高 4.35 RacerGS）；backfill 9 A / 1 B（最高 4.30 CognitiveReality）。
- 门① 最大 Jaccard **0.083**（GaussianSpline vs 库内 2610.26918；<0.62，非同质）。
- 门② 主批 Top10 覆盖 **8 赛道**；backfill 覆盖 **8 赛道**（均 ≥5）。
- 门③ 当日最高 **4.35 < 库内近 30 天 Top10 均分 4.416**（窗口 2026-09-28~10-28、431 条入窗、现算）→ **非重磅日、无 S 级**；RacerGS 4.35（主批）/CognitiveReality 4.30 / RoGe 4.27 / FlowHOI 4.23（backfill）达 S 线按校准关记 A（同 10-24 EgoHand / 10-27 WFM 先例）。三关全过，**未触发重筛**。
- OUTDATED/SUPERSEDED **0 篇**。路线级观察：① 3DGS 压缩/预算线三箭齐发（RacerGS 残差自回归熵编码 / ParetoGS 连续预算 / BoundedGS 训练显存）；② 动态 4D 表示两条正交路线（GaussianSpline 轨迹参数化 vs DimFlow 特征双向学习）；③ 免位姿前馈 3DGS 的几何-属性解耦（SG-Splat）与位姿精化（PosePlaner/Mem3R）形成组合拳；④ VR 遥操作+语义高斯+LLM 智能体闭环（CognitiveReality）与 real-to-sim 智能体管线（SceneAgent）同现，机器人与人形操作的基础设施日。

## 产物（第 7-8 步）
- 报告 2 份（主报告 + backfill 报告）+ 原子笔记 34 篇（grade≥B；2 篇 C 级仅入馆不解读）+ MOC 2 份 + 总索引刷新 + 7 维表/scored/run_log 各 2 套。
- registry 633 → **669**（+26 主批 +10 backfill；备份 `papers/library/registry.jsonl.bak-20261028`；按 base_id 幂等）。
'''
open(f'papers/daily/{DATE}/run_log.md', 'w', encoding='utf-8').write(run_log_main)

run_log_bf = f'''# {BFB} 执行日志

- **批次性质**：backfill（非当日新提交）——10-27 公告批次中 RSS 混入的旧稿 replace/cross 再公告 10 篇首次入馆；原始投稿月 2026-01 ~ 2026-09（arXiv ID 前缀 2601/2602/2603/2604/2605/2606/2609）。
- **来源**：`scripts/fetch_rss.py` 7 分类全量去重 1047 → KW 命中 67；其中 15 篇旧稿再公告经 XR 甄别保留 10 篇（剔非 XR 5 篇：2511.22459 火焰 VFX / 2604.05475 眼动阅读 / 2606.19609 施工记录 / 2606.29924 抓取生成 / 2609.15213 人形控制）。
- **全文**：10 篇全部 L0/FULL（45,971–131,491 字符），串行 3s/篇，无限流/降级/伪造。
- **评分**：9 A / 1 B（最高 CognitiveReality 4.30 达 S 线，非重磅日按校准关记 A）。门① max Jaccard 0.076 < 0.62；门② 覆盖 8 赛道；门③ 不适用；OUTDATED 0。
- **诚实口径**：全部条目 `batch=backfill-1028` + `orig_window` 标注，绝不混入「当日新论文」。
'''
open(f'papers/daily/{BFB}/run_log.md', 'w', encoding='utf-8').write(run_log_bf)

# ---------- 3. registry（先备份，幂等追加，in_top10 显式） ----------
reg_path = 'papers/library/registry.jsonl'
shutil.copy(reg_path, reg_path.replace('.jsonl', '.bak-20261028'))
rows = [json.loads(l) for l in open(reg_path, encoding='utf-8') if l.strip()]
have = {r['id'].split(':')[-1].split('v')[0] for r in rows}
added = 0
with open(reg_path, 'a', encoding='utf-8') as f:
    for p in MAIN + BF:
        if p['id'] in have:
            continue
        entry = dict(id=f"arXiv:{p['id']}", title=p['title'], title_zh=p['title_zh'],
                     track=p['track'], date=(DATE if p in MAIN else '2026-10-27'),
                     value=p['value'], grade=p['grade'], scores=p['scores'],
                     status=p['status'], evidence=p['evidence'], fetch_level=p['level'],
                     fulltext_chars=0, in_top10=(p['id'] in TOP10_IDS), batch=p['batch'],
                     announce_type=p['announce'], flags=[])
        if p in BF:
            entry['orig_window'] = p['orig_window']
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
        date=(DATE if p in MAIN else '2026-10-27'), value=f"{p['value']:.2f}", grade=p['grade'],
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

moc(MAIN, f'papers/MOC/MOC-{DATE}.md', f'MOC · {DATE}（10-27 公告批次）',
    '> 当日地图：**公告日 2026-10-27（周二）≠ 拉取日 2026-10-28（周三 02:30）**——诚实口径，非当日硬提交。\n'
    '> 主批 XR 新稿 26 篇（18 A / 6 B / 2 C，无 S——非重磅日）；listing 与 RSS 两渠道互证 44 篇真新提交中 26 篇 XR 核心/强相关；全文 25 L0/FULL + 1 L1 摘要级。\n'
    '> 覆盖度三关：门① 0.083 / 门② 8 赛道 / 门③ 4.35 < 4.416（现算）→ 非重磅日无 S；RacerGS 4.35 达 S 线按校准关记 A。Top10 实数 10 篇。')
moc(BF, f'papers/MOC/MOC-{BFB}.md', f'MOC · {BFB}（旧稿再公告补录）',
    '> 本批为 **backfill**：10-27 公告批次 RSS 混入的旧稿 replace/cross 再公告 10 篇首次入馆（原始投稿月 2601~2609），**均非当日新提交**。\n'
    '> 9 A / 1 B；CognitiveReality 4.30 / RoGe 4.27 / FlowHOI 4.23 达 S 线但因非重磅日按校准关记 A。门① 0.076 / 门② 8 赛道 / 门③ 不适用。')

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
    L.append('- 门①（同质去重）：最大 Jaccard 0.083 < 0.62，通过，无同质重复。')
    L.append('- 门②（赛道覆盖）：本批覆盖 8 个标准赛道（≥5），通过，无冷门高价值候选可回补。')
    L.append('- 门③（价值天花板）：当日最高分 4.35 < 库内近 30 天 Top10 均分 4.416（现算）→ 非重磅日、无 S 级，未拔高、未凑数；达 S 线的 RacerGS 4.35 按校准关记 A。')
    L.append('- 三关均未触发重筛；OUTDATED/SUPERSEDED 0 篇。\n')
    L.append('## 六、附录：证据等级分布与抓取记录\n')
    nf = sum(1 for p in papers if p['evidence'] == 'FULL')
    L.append(f'- FULL {nf} 篇；PARTIAL 0 篇；ABSTRACT_ONLY 0 篇（2610.34223 为 L1 ar5iv 摘要级：转换版 5,083 字符无实验章节，已在 7 维表与笔记显式声明并按摘要级评估）。')
    L.append('- 抓取降级：无 L5；无 OCR；无伪造。串行 3s/篇，无限流。')
    open(path, 'w', encoding='utf-8').writelines([x + '\n' for x in L])

report(MAIN, f'reports/XR-Daily-Report-{DATE}.md',
    f'XR 每日论文解读报告 · {DATE}（10-27 公告批次）',
    '## 一、执行摘要\n'
    f'- **公告日 2026-10-27（周二）≠ 拉取日 2026-10-28（周三 02:30）**——诚实口径：本批处理的是 10-27 公告批次，非当日硬提交。\n'
    '- **主批 XR 新稿 26 篇（18 A / 6 B / 2 C，无 S 级）**：RacerGS 4.35（3DGS 残差自回归熵编码，150× 压缩）· BoundedGS 4.15（高分辨率 3DGS 训练显存 -82.3%）· CGR-GS 4.15（复杂度先验可泛化人体高斯）· Birth-Death 4.00（变分分数结构学习）· InteractiveWorld 3.99（可验证人本闭环助手基准，最佳模型仅 41.7%）· GEMS 3.92（3DGS 情景记忆）· GeoLift 3.92（显式 3D 地图空间推理接地）· VidEdit3D 3.92（视频扩散 3D 高斯编辑）· TLEIO 3.85（事件惯性里程计）· LegoOcc++ 3.85（开放词汇占用预测）。\n'
    '- **覆盖 8 赛道**：渲染与显示 / 系统与平台 / 化身与人体 / 神经渲染 / 评估与数据集 / 重建与SLAM / 感知与认知 / 内容生成。\n'
    '- **覆盖度三关**：门① 0.083；门② 8 赛道；门③ 4.35 < 4.416（现算）→ **非重磅日、无 S 级**；RacerGS 4.35 达 S 线按校准关记 A。\n'
    '- **全文证据**：25 篇 L0/FULL + 1 篇 L1 摘要级（2610.34223，ar5iv 无实验章节）。\n'
    '- **同批 backfill-1028**：RSS 混入旧稿 replace/cross 再公告 10 篇首次入馆（9 A / 1 B，最高 CognitiveReality 4.30 达 S 线按校准关记 A），详见 [XR-Backfill-Report-backfill-1028.md](XR-Backfill-Report-backfill-1028.md)。',
    DATE, 10)

report(BF, f'reports/XR-Backfill-Report-{BFB}.md',
    f'XR Backfill 补录报告 · {BFB}（旧稿再公告）',
    '## 一、执行摘要\n'
    '- **批次性质**：backfill（非当日新提交）——10-27 公告批次中 RSS 混入的旧稿 replace/cross 再公告 10 篇，首次入馆；原始投稿月 2026-01 ~ 2026-09。\n'
    '- **补录 10 篇（9 A / 1 B）**：CognitiveReality 4.30（Skoltech，VR 遥操作语义高斯映射，工具匹配 81.24% vs 规则 48.33%）· RoGe 4.27（小米/东北大学，端到端隐式重建+生成 NVS，FVD 58 vs 206）· FlowHOI 4.23（MBZUAI 等，HOI 流匹配生成，仿真 SR 55.96% vs 28.44%）· 4DSurf 4.00（ANU/NVIDIA，SDF 流正则动态表面，Hi4D CD -49%）· StableHand 4.00（质量感知双手运动估计，W-MPJPE -20%）· Haptic Sorter 3.93（触觉探索+可微操作势，300 Hz 闭环）· Mem3R 3.92（Google/HKUST，混合记忆流式重建，参数 -19%）· CoMo3R-SLAM 3.72（ETH 等，协同单目稠密 SLAM）· MRO-GWM 3.65（物体中心高斯世界模型，MPC 0.79 vs 启发式 0.14）· CleanGS 3.52（免训练 3DGS 场景清理，ICVGIP 2026）。\n'
    '- **覆盖 8 赛道**；门① 0.076；门③ 对 backfill 不适用；OUTDATED 0。\n'
    '- **诚实口径**：全部条目 `batch=backfill-1028` + `orig_window` 标注，绝不混入「当日新论文」。',
    BFB, 10)

# ---------- 7. MOC-总索引刷新 ----------
moc_path = 'papers/MOC/MOC-总索引.md'
h = open(moc_path, encoding='utf-8').read()

# 7.1 头部计数与批次列表
h = h.replace('文献库：`papers/library/registry.jsonl`（累计 **633 篇**；跨度 2026-09-15 ~ 2026-10-26',
              '文献库：`papers/library/registry.jsonl`（累计 **669 篇**；跨度 2026-09-15 ~ 2026-10-27')
h = h.replace('**backfill-1027:8（10-26 公告 RSS 混入旧稿 replace/cross 再公告，首次入馆）**；',
              '**backfill-1027:8（10-26 公告 RSS 混入旧稿 replace/cross 再公告，首次入馆）** · **2026-10-28:26（10-27 公告批次真新提交，非重磅日无S；listing+RSS 两渠道互证 44 篇中 26 篇 XR）** · **backfill-1028:10（10-27 公告 RSS 混入旧稿 replace/cross 再公告，首次入馆）**；')
h = h.replace('**10-27 周二处理 10-26 公告批次（周末积压，7 篇 XR 新稿 + backfill-1027 补录 8 篇）**。',
              '**10-27 周二处理 10-26 公告批次（周末积压，7 篇 XR 新稿 + backfill-1027 补录 8 篇）**；**10-28 周三处理 10-27 公告批次（26 篇 XR 新稿 18A/6B/2C + backfill-1028 补录 10 篇 9A/1B，非重磅日无S）**。')

# 7.2 追加 10-28 状态注记（在 10-27 注记后）
note28 = ('> **状态注记（2026-10-28）**：周三 02:30，处理 **2026-10-27（周二）公告批次**（公告日≠拉取日，诚实口径）。'
 '漏网对账（TARGET_LO=10-26）：listing 7 分类最新公告日 **10-27**（10-24/10-25 周末无公告日段）；10-26 组 358 篇摘要级复核 11 篇命中均为已剔非 XR（0 漏网）；**10-27 组 794 篇全部未入馆**，摘要级 XR 命中 41 篇。'
 'RSS 7 分类去重 1047 → KW 命中 67 = **44 篇 2610.* 真新提交 + 15 篇旧稿 replace/cross 再公告 + 8 篇库内 v2 再公告**；listing 摘要级 41 篇全部被 RSS 覆盖（**RSS 漏网 0 篇**，两渠道互证）。'
 '主批甄别 **XR 核心/强相关 26 篇**（剔非 XR 18 篇：机器人抓取/VLA/航空 VLN/灵巧手采集/医学影像/医学配准/人形×2/施工场景图/视频蒸馏/社交机器人 HRI/驾驶场景/空间 VPR 等）；全文 **25 L0/FULL + 1 L1 摘要级**（2610.34223 单相机试穿化身，ar5iv 无实验章节）。'
 'Top10（实数 10 篇）：**18 A / 6 B / 2 C，最高 4.35（RacerGS），无 S 级**；覆盖 8 赛道。'
 '三关：门① max Jaccard **0.083**；门② 8 赛道；门③ 当日最高 4.35 < 库内近 30 天 Top10 均分 **4.416**（431 条入窗，现算）→ **非重磅日、无 S 级，未拔高**；RacerGS 4.35 达 S 线按校准关记 A；OUTDATED 0。'
 '**backfill-1028**：旧稿 replace/cross 再公告 10 篇首次入馆（9 A / 1 B，最高 CognitiveReality 4.30 达 S 线按校准关记 A，同 10-24 EgoHand / 10-27 WFM 先例）。'
 'registry 633 → **669**（+26 +10）。详见 [运行报告](../../reports/XR-Daily-Report-2026-10-28.md) 与 [MOC-2026-10-28](./MOC-2026-10-28.md) / [MOC-backfill-1028](./MOC-backfill-1028.md) / [Backfill 报告](../../reports/XR-Backfill-Report-backfill-1028.md)。\n')
anchor = '> **状态注记（2026-10-27）**'
i = h.find(anchor)
j = h.find('\n\n', h.find('[Backfill 报告](../../reports/XR-Backfill-Report-backfill-1027.md)。', i))
h = h[:j] + '\n' + note28 + h[j:]

# 7.3 速查入口
h = h.replace('| 最新一期 | [MOC · 2026-10-27](./MOC-2026-10-27.md) |', '| 最新一期 | [MOC · 2026-10-28](./MOC-2026-10-28.md) |')
h = h.replace('| 上一期 | [MOC · 2026-10-24](./MOC-2026-10-24.md) |', '| 上一期 | [MOC · 2026-10-27](./MOC-2026-10-27.md) |')
h = h.replace('（现有 328 篇）', '（现有 362 篇）')
h = h.replace('| 最新运行状态 | [运行报告 2026-10-27](../../reports/XR-Daily-Report-2026-10-27.md)（周一 02:30 状态日 0 新稿：周末积压公告未到时刻，10-23 公告组 411 篇全量复核 0 漏网；上批数据日见 [2026-10-24](../../re2026-10-24](../../reports/XR-Daily-Report-2026-10-24.md)：10-23 公告批次 17 篇 + backfill-1024 4 篇） |',
              '| 最新运行状态 | [运行报告 2026-10-28](../../reports/XR-Daily-Report-2026-10-28.md)（10-27 公告批次 26 篇 18A/6B/2C 非重磅日无S + backfill-1028 补录 10 篇；listing+RSS 两渠道互证，RSS 漏网 0 篇） |')

# 7.4 批次索引表追加两行
row_main = ('| 2026-10-28 | [MOC-2026-10-28](./MOC-2026-10-28.md) | XR 26（Top10 实数）· 18A/6B/2C · 非重磅日（无S） | '
            '10-27 公告批次；listing+RSS 两渠道互证 44 篇中 26 篇 XR；1 篇 L1 摘要级 |')
row_bf = ('| backfill-1028 | [MOC-backfill-1028](./MOC-backfill-1028.md) | 补录 10（9A/1B）· 非当日新提交 | '
          '10-27 公告 RSS 混入旧稿 replace/cross 再公告 10 篇（2601~2609） |')
h = h.replace('| backfill-1027 | [MOC-backfill-1027](./MOC-backfill-1027.md) | 补录 8（4A/4B）· 非当日新提交 | 10-26 公告 RSS 混入旧稿 replace/cross 再公告 8 篇（2412~2610） |',
              '| backfill-1027 | [MOC-backfill-1027](./MOC-backfill-1027.md) | 补录 8（4A/4B）· 非当日新提交 | 10-26 公告 RSS 混入旧稿 replace/cross 再公告 8 篇（2412~2610） |\n'
              + row_main + '\n' + row_bf)

# 7.5 追加 Top10 段（文件尾）
seg = '\n### 2026-10-28 新增（Top10 实数：18 A / 6 B / 2 C 全批，非重磅日无 S）\n\n| # | 论文 | 赛道 | 分值 | 等级 | 证据 |\n|---:|---|---|---:|---|---|\n'
for i2, p in enumerate(MAIN, 1):
    seg += f"| {i2} | {esc(p['title_zh'])} | {p['track']} | {p['value']:.2f} | {p['grade']} | {p['evidence']} |\n"
seg += '\n### backfill-1028 补录（10 篇：9 A + 1 B，非当日新提交）\n\n| # | 论文 | 赛道 | 分值 | 等级 | 证据 |\n|---:|---|---|---:|---|---|\n'
for i2, p in enumerate(BF, 1):
    seg += f"| {i2} | {esc(p['title_zh'])} | {p['track']} | {p['value']:.2f} | {p['grade']} | {p['evidence']} |\n"
h = h.rstrip() + '\n' + seg

# 7.6 页脚计数
h = h.replace('库内 **633 篇**', '库内 **669 篇**').replace('原子笔记 **328 篇**', '原子笔记 **362 篇**')
h = h.replace('MOC 28 份', 'MOC 30 份')
h = h.replace('*最后更新：2026-10-27（10-26 公告批次：7 篇 XR 新稿 4A/3B 非重磅日无S + backfill-1027 补录 8 篇 4A/4B）',
              '*最后更新：2026-10-28（10-27 公告批次：26 篇 XR 新稿 18A/6B/2C 非重磅日无S + backfill-1028 补录 10 篇 9A/1B）')
open(moc_path, 'w', encoding='utf-8').write(h)
print('MOC-总索引 refreshed')
print('DONE')
