# -*- coding: utf-8 -*-
"""2026-11-03 产物生成：主批（11-02 周一公告批次 11 篇）+ backfill-1103（旧稿 replace 再公告 2 篇）。
公告日 2026-11-02（周一，周末 10-31/11-01 积压于 00:00 UTC=08:00 北京时间释放）≠ 拉取日 2026-11-03（周二 02:30）。
API published 核验提交日 10-29×3 / 10-30×8。listing 347 篇摘要级 XR 命中 21 篇与 RSS 真新集合逐篇一致（RSS 漏网 0）。
消费 data/scored_1103.json（字段齐全、显式带 batch）；registry 幂等追加（先备份，in_top10 按定稿显式设置）；
生成 7 维表/scored/run_log/笔记/MOC/报告并刷新总索引。"""
import json, os, shutil, glob

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
os.chdir(ROOT)
D = json.load(open('data/scored_1103.json', encoding='utf-8'))
MAIN, BF = D['main'], D['backfill']
TOP10_IDS = set(D['top10_ids'])
DATE, BFB = '2026-11-03', 'backfill-1103'
ANN = '2026-11-02'          # 公告日（周一）
GATE3 = 4.429               # 门③ 现算均分（窗口 2026-10-04~11-03，393 条入窗）
TODAY_MAX = MAIN[0]['value']  # 4.15
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
    '批次：2026-11-03（**2026-11-02（周一）公告批次**——周末 10-31/11-01 积压于周一 00:00 UTC（=08:00 北京时间）释放；公告日 11-02 ≠ 拉取日 11-03（周二 02:30），诚实口径）。\n'
    '候选池 11 篇：漏网对账（先于拉取，TARGET_DAY=2026-10-30）listing 7 分类最新公告日均为 **2026-11-02**（10-31/11-01 周末无公告日段）；**11-02 组 347 篇唯一论文全部未入馆**（CV 102 / GR 4 / HC 20 / MM 2 / RO 72 / AI 186 / IV 20）→ 摘要级 XR 命中 **21 篇**；RSS 7 分类去重 540 → KW 命中 32 = **21 篇 11-02 公告组真新提交（11 篇 XR + 10 篇非 XR 剔除）+ 11 篇旧稿 replace/cross 再公告（2 篇 XR → backfill-1103 + 9 篇非 XR 剔除）+ 2 篇库内 v2 再公告（剔除）**；listing 摘要级 21 篇全部被 RSS 覆盖（**RSS 漏网 0 篇**，两渠道互证）。\n'
    'arXiv API published 口径核验提交日：**10-29×3 / 10-30×8**（均早于公告日 11-02；RSS published 字段为公告时间戳，非提交日）。\n'
    '全文：13 篇候选（主批 11 + backfill 2）串行 3s/篇：**12 篇 L0/FULL**（24,878–228,891 字符）+ **1 篇 L1/PARTIAL**（2610.41680：arXiv HTML 404、ar5iv 仅返摘要页 5,660 字符，按摘要级评估并显式声明，禁止脑补）。\n'
    '覆盖度三关：门① 最大 Jaccard **0.116**（2610.41833 PGGT-Loc vs 库内 2606.25430，<0.62 通过）；门② 定稿 Top10 覆盖 **6 赛道**（全批 8 赛道，≥5 通过，无需重筛）；门③ 当日最高 **4.15 < 库内近 30 天 Top10 均分 4.429**（窗口 2026-10-04~11-03、393 条入窗、现算）→ **非重磅日、无 S 级**，未拔高。全批无 ≥4.2 达线论文。',
    len(TOP10))

seven_table(BF, f'papers/daily/{BFB}/7dim-table.md',
    f'{BFB} 全量 7 维度对比表（参考）',
    '批次：backfill-1103（**11-02 公告批次中 RSS 混入的旧稿 replace 再公告**（首次入馆；原始投稿 2511=2025-11 / 2602=2026-02，v2 分别于 2026-10-29/10-30 更新后再公告）；均非 11-02 当日新提交，诚实口径单独编号）。\n'
    '候选 2 篇：DiTGaze（几何条件扩散增强的少样本视线估计）/ AdaGS（置信门控扩散自适应的无位姿稀疏视图 3DGS 重建）。全部 L0/FULL 全文后定稿。\n'
    '门③ 对 backfill 不适用；本批不参与当日「重磅日」判定。门① 全池合并复核最大 Jaccard 0.116 < 0.62（通过，无同质重复）；门② 覆盖 2 赛道（感知与认知 / 重建与SLAM；2 篇低量批次实际上限）。\n'
    '注：本批 2 篇均未达 S 线（最高 DiTGaze 3.72），按实数定级。',
    len(BF))

# ---------- 2. scored.md + run_log.md ----------
def scored_md(papers, path, title, extra):
    L = [f'# {title}\n', extra + '\n', '| 排名 | arXiv | 标题 | 赛道 | 总分 | 等级 | 证据 | 公告类型 |',
         '|---|---|---|---|---|---|---|---|']
    for i, p in enumerate(papers, 1):
        L.append(f"| {i} | {p['id']} | {esc(p['title_zh'])} | {p['track']} | {p['value']:.2f} | {p['grade']} | {p['evidence']} | {p['announce']} |")
    open(path, 'w', encoding='utf-8').writelines([x + '\n' for x in L])

scored_md(MAIN, f'papers/daily/{DATE}/scored.md', f'{DATE} 评分明细',
    '评分口径：7 维加权 IMP0.20·NOV0.20·TEC0.15·EXP0.15·PER0.15·TRL0.08·REP0.07；分档 S≥4.2 / A3.6–4.2 / B3.0–3.6 / C<3.0。全部基于全文证据定稿（12 篇 L0/FULL + 1 篇 L1/PARTIAL 摘要级）。\n'
    f'覆盖度三关：门① 最大 Jaccard 0.116 < 0.62（通过，非同质）；门② 定稿 Top10 覆盖 6 赛道 ≥ 5（通过，全批 8 赛道，无需重筛）；门③ 当日最高 4.15 < 库内近 30 天 Top10 均分 4.429（现算，393 条入窗）→ 非重磅日、无 S 级（校准关，不触发重筛）。\n'
    'OUTDATED/SUPERSEDED 0 篇。等级分布：7 A / 2 B / 2 C。Top10 实数 9 篇：第 10 名候选 2610.41680（2.50 C，PARTIAL）按「C 级仅入馆不解读」不纳入 Top10，不凑数。')
scored_md(BF, f'papers/daily/{BFB}/scored.md', f'{BFB} 评分明细',
    '评分口径同上。本批为旧稿 replace 再公告首次入馆（非当日新提交），门③ 不适用。\n'
    '门① 全池合并复核最大 Jaccard 0.116 < 0.62（通过）；门② 覆盖 2 赛道（2 篇低量批次实际上限）；OUTDATED/SUPERSEDED 0 篇。等级分布：1 A / 1 B。')

run_log_main = f'''# {DATE} 执行日志

## 数据源与对账（第 1-3 步）
- **漏网对账（先于拉取）**：`scripts/audit_listing_1103.py`（TARGET_DAY=2026-10-30，上批公告日；show=500 单页×7 分类）→ 7 分类最新公告日均为 **2026-11-02**（周末 10-31/11-01 无公告日段，积压于周一 00:00 UTC=08:00 北京时间释放，与上批 11-02 运行预判一致）；**11-02 组 347 篇唯一论文全部未入馆**（CV 102/GR 4/HC 20/MM 2/RO 72/AI 186/IV 20，declared=got 全分类完整）。cs.AI 首页被 11-02 组挤出 10-30 组尾部 78 条，`scripts/audit_csai_p2_1103.py` 补采第 2 页（continued 声明正则兼容）→ **10-30 组未入馆 710 篇与 11-02 运行集合逐篇一致（差异 0）**，摘要级复核沿用上批结论（13 篇命中均为已剔非 XR）→ **0 漏网、无 backfill**。
- **摘要级 XR 过滤**：`scripts/filter_missed_xr_abstract.py` 对 11-02 组 347 篇跑 API 摘要级过滤（meta fetched 347/347）→ XR 命中 **21 篇**（`data/missed_xr_abstract_1103.json`）。
- **RSS 主渠道交叉验证**：`scripts/fetch_rss.py` 7 分类全量去重 540 条 → KW 命中 **32** = **21 篇 11-02 公告组真新提交（11 篇 XR + 10 篇非 XR）+ 11 篇旧稿 replace/cross 再公告（2 篇 XR → backfill-1103 + 9 篇非 XR 剔除）+ 2 篇库内 v2 再公告（剔除）**。listing 摘要级 21 篇**全部被 RSS 覆盖，RSS 漏网 0 篇**——两渠道互证。
- **API 探针**：双主机 200；`id_list` 批量核验 13 篇候选 published（原始提交日）：主批 11 篇 = 10-29×3 / 10-30×8（均早于公告日 11-02）；backfill 2 篇 = 2511.11231（2025-11-14 提交，v2 于 10-29 更新）/ 2602.21535（2026-02-25 提交，v2 于 10-30 更新）。RSS published 字段为公告时间戳（11-02），非提交日，两口径已区分。

## 甄别（第 3 步）
- 主批 XR 核心/强相关 **11 篇**入评分池；剔非 XR **10 篇**（2610.40748 WorldBridge 机器人世界动作模型 / 2610.41063 胰腺 MRI 分割 / 2610.41254 Hawkeye 场景文字识别 / 2610.41336 HandMimicX 机器人灵巧操作 / 2610.41380 Pinching Antennas 6G ISAC 波导天线 / 2610.41402 DUGO 第一视角在线动作定位 / 2610.41429 机器人穿刺标定 / 2610.41702 柔性臂机器人控制 / 2610.41768 差速轮机器人 SLAM / 2610.42021 Nexus-VLA 跨本体 VLA）。
- 旧稿 replace/cross 再公告 11 篇中 **2 篇 XR → backfill-1103**（首次入馆，单独编号）；9 篇非 XR 剔除（2603.21142 VLM 自适应 CBF 导航 / 2606.18426 VEGA 导航 VLA / 2607.24747 数据手套按键生物识别 / 2608.06192 HOPE 单目手物压力估计 / 2608.19740 Franka ROS 2 栈 / 2609.27439 水下声呐导航）。
- 库内 v2 再公告 2 篇剔除（2606.25430 PRISM，10-21 已入馆 / 2609.33969 高斯泼溅 volumetric video 压缩，10-02 已入馆）。

## 全文抓取（第 4 步）
- 13 篇候选（主批 11 + backfill 2）跑 `scripts/fetch_fulltext.py`，严格串行 3s/篇（约 50 秒）：**12 篇 L0/FULL**（24,878–228,891 字符）+ **1 篇 L1/PARTIAL**（2610.41680：arXiv HTML 404、ar5iv 仅返摘要页 5,660 字符无正文节，manifest 已改判 PARTIAL，按摘要级评估并显式声明）。无限流/降级/伪造。
- manifest 合并写入校验通过；WROTE=13>0。

## 评分与三关（第 5-6 步）
- 先抓全文再定稿。7 维加权定稿：主批 **7 A / 2 B / 2 C**（最高 4.15 VoxLution/DrawSplat 并列；全批无 ≥4.2 达线论文）；backfill **1 A / 1 B**（最高 DiTGaze 3.72）。
- 门① 最大 Jaccard **0.116**（2610.41833 PGGT-Loc vs 库内 2606.25430；<0.62，非同质）。
- 门② 定稿 Top10（实数 9 篇）覆盖 **6 赛道**（内容生成×1 / 重建与SLAM×3 / 评估与数据集×1 / 神经渲染×1 / 化身与人体×1 / 感知与认知×2；全批 8 赛道，≥5 通过，**无需重筛**）。
- 门③ 当日最高 **4.15 < 库内近 30 天 Top10 均分 4.429**（窗口 2026-10-04~11-03、393 条入窗、现算）→ **非重磅日、无 S 级**（校准关，不触发重筛）。三关全过，**未触发重筛**。
- OUTDATED/SUPERSEDED **0 篇**。路线级观察：① 结构先验回归 SLAM/定位主线——DrawSplat（Atlanta World 结构面转高斯可微正则）与 PGGT-Loc（平面基元 grounding 前馈定位）同批出现，与库内 MG-SLAM/PlanaReLoc/SplitGS-Loc 一脉相承，「显式结构约束替代纯学习」成本周清晰信号；② 具身数据层继续扩充——MotorSense（EMG 特权信号预训练）与 EgoHSI3R（手-场景-接触联合在线重建）分别从数据与在线推理两端加强第一人称交互理解，与库内 Ego-OSCAR/Tactus 形成「采集-预训练-在线推理」链条；③ 场景生成走向显式稀疏自回归——VoxLution 的 ROC token 化与多分辨率序列，与库内 BlockFusion/LT3SD 扩散级联及 TRELLIS.2 latent 路线形成三支对照；④ 硬件类缺口依旧——本批触觉（需求研究 C 级 PARTIAL）与中央凹视觉（FoAViS 类脑系统）仍非近眼显示硬件，近眼显示/光场/全息方向仍仅 CVQPG 与 HoOPOE 两篇，波导/可变焦/Maxwellian 继续空缺。

## 产物（第 7-8 步）
- 报告 2 份（主报告 + backfill 报告）+ 原子笔记 12 篇（grade≥B；2 篇 C 仅入馆）+ MOC 2 份 + 总索引刷新 + 7 维表/scored/run_log 各 2 套。
- registry 717 → **730**（+11 主批 +2 backfill；备份 `papers/library/registry.jsonl.bak-20261103`；按 base_id 幂等）。
'''
open(f'papers/daily/{DATE}/run_log.md', 'w', encoding='utf-8').write(run_log_main)

run_log_bf = f'''# {BFB} 执行日志

- **批次性质**：backfill（非当日新提交）——11-02 公告批次中 RSS 混入的旧稿 replace 再公告 2 篇首次入馆；原始投稿 2511=2025-11（v2 于 2026-10-29 更新）/ 2602=2026-02（v2 于 2026-10-30 更新）（arXiv ID 前缀 2511/2602）。
- **来源**：`scripts/fetch_rss.py` 7 分类全量去重 540 → KW 命中 32；其中 11 篇旧稿再公告经 XR 甄别保留 2 篇（剔非 XR 9 篇：VLM 自适应 CBF 导航/导航 VLA/数据手套生物识别/单目手物压力估计/Franka ROS 2 栈/水下声呐导航）。
- **全文**：2 篇全部 L0/FULL，串行 3s/篇，无限流/降级/伪造。
- **评分**：1 A / 1 B（最高 DiTGaze 3.72，无 S 线）。门① 全池合并复核最大 Jaccard 0.116 < 0.62；门② 覆盖 2 赛道（2 篇低量批次实际上限）；门③ 不适用；OUTDATED 0。
- **诚实口径**：全部条目 `batch=backfill-1103` + `orig_window` 标注，绝不混入「当日新论文」。
'''
open(f'papers/daily/{BFB}/run_log.md', 'w', encoding='utf-8').write(run_log_bf)

# ---------- 3. registry（先备份，幂等追加，in_top10 显式） ----------
reg_path = 'papers/library/registry.jsonl'
shutil.copy(reg_path, reg_path.replace('.jsonl', '.bak-20261103'))
rows = [json.loads(l) for l in open(reg_path, encoding='utf-8') if l.strip()]
have = {r['id'].split(':')[-1].split('v')[0] for r in rows}
PREFIX_MONTH = {'2511': '2025-11', '2602': '2026-02'}
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
            entry['orig_window'] = f"旧稿 replace 再公告（首次入馆）：{PREFIX_MONTH[p['id'][:4]]} 投稿，{ANN} 公告批次 RSS 混入"
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

moc(MAIN, f'papers/MOC/MOC-{DATE}.md', f'MOC · {DATE}（11-02 公告批次）',
    '> 当日地图：**公告日 2026-11-02（周一）≠ 拉取日 2026-11-03（周二 02:30）**——诚实口径。周末 10-31/11-01 积压于周一 00:00 UTC（08:00 北京时间）释放；API 核验提交日 10-29×3 / 10-30×8。\n'
    '> 主批 XR 新稿 11 篇（7 A / 2 B / 2 C，无 S——非重磅日）；listing 与 RSS 两渠道互证 21 篇真新提交中 11 篇 XR（RSS 漏网 0 篇）；全文 12 篇 L0/FULL + 1 篇 L1/PARTIAL。\n'
    '> 覆盖度三关：门① 0.116 / 门② 定稿 Top10 6 赛道（全批 8 赛道，无需重筛）/ 门③ 4.15 < 4.429（现算，393 条入窗）→ 非重磅日无 S。**Top10 实数 9 篇**（第 10 名候选 2610.41680 为 C 级 2.50，按「C 仅入馆不解读」不纳入）。')
moc(BF, f'papers/MOC/MOC-{BFB}.md', f'MOC · {BFB}（旧稿再公告补录）',
    '> 本批为 **backfill**：11-02 公告批次 RSS 混入的旧稿 replace 再公告 2 篇首次入馆（原始投稿 2511=2025-11 / 2602=2026-02），**均非当日新提交**。\n'
    '> 1 A / 1 B；最高 DiTGaze 3.72（无 S 线）。门① 0.116 / 门② 2 赛道（2 篇低量批次实际上限）/ 门③ 不适用。')

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
    L.append(f'- FULL {nf} 篇；PARTIAL {np_} 篇；ABSTRACT_ONLY 0 篇。')
    L.append('- 抓取降级：2610.41680 L1/PARTIAL（arXiv HTML 404 + ar5iv 仅摘要页 5,660 字符，按摘要级评估并显式声明，未脑补正文细节）；其余 12 篇 L0/FULL。无 L5、无 OCR、无伪造；串行 3s/篇，无限流。')
    open(path, 'w', encoding='utf-8').writelines([x + '\n' for x in L])

report(TOP10,
       f'reports/XR-Daily-Report-{DATE}.md',
       f'XR 每日论文解读报告 · {DATE}（11-02 公告批次）',
       '## 一、执行摘要\n'
       f'- **公告日 2026-11-02（周一）≠ 拉取日 2026-11-03（周二 02:30）**——诚实口径：本批处理的是 11-02 公告批次（周末 10-31/11-01 积压于周一 00:00 UTC=08:00 北京时间释放）；API published 口径核验提交日 **10-29×3 / 10-30×8**（均早于公告日，非当日硬提交）。\n'
       '- **主批 XR 新稿 11 篇（7 A / 2 B / 2 C，无 S 级）**。Top10（**实数 9 篇**，第 10 名候选为 C 级不纳入）：VoxLution 4.15（TUM/UVA，体素进化 3D 室内场景生成，3D-FRONT FPD/FID 较 LT3SD 降 59.6%/51.1%、体素 1.5625 cm）· DrawSplat 4.15（东北大等，Atlanta World 引导隐式高斯 SLAM，Apartment ATE 较次优降 60%、F1 93.7、模型 18.29 MB）· MotorSense 4.14（UMD，100 小时视频-EMG 配对数据集，EK100 动词 +15.86、视频扩散 FVD 373→304）· PGGT-Loc 4.14（中科院，基元接地前馈相机定位，ScanNet 召回 69.0% vs 48.5%、代码开源）· OpenVIO 3.87（首尔国立，统一针孔/鱼眼/360° 的开源 VIO，TUM-VI 单目 ATE 0.377 m 九系统最优、MIT 许可）· PriorGS 3.87（Waterloo，单曝光 HDR 新视角合成，超全部基线约 4-8 dB、单 3090 可复现）· EgoHSI3R 3.85（清华，在线 4D 手-场景交互重建，ARCTIC W-MPJPE 108.80 mm 最优、10.07 FPS）· FoAViS 3.42（哥廷根/McGill，中央凹主动视觉学习注视策略，T=4 ImageNet +4.8 Acc、涌现 IoR）· VR 手部视觉反馈×特发性震颤 3.20（萨拉戈萨，MQ3 追踪衰减震颤频段 15.79-22.49 dB、患者物理震颤功率中位降 47%/57%）。\n'
       '- **覆盖 6 赛道**：内容生成×1 / 重建与SLAM×3 / 评估与数据集×1 / 神经渲染×1 / 化身与人体×1 / 感知与认知×2（全批 8 赛道）。\n'
       '- **覆盖度三关**：门① 0.116；门② 6 赛道（≥5，无需重筛）；门③ 4.15 < 4.429（现算，393 条入窗）→ **非重磅日、无 S 级**（全批无 ≥4.2 达线论文）。\n'
       '- **全文证据**：13 篇候选中 12 篇 L0/FULL（24,878–228,891 字符）+ 1 篇 L1/PARTIAL（2610.41680，摘要级评估并显式声明）。\n'
       '- **同批 backfill-1103**：RSS 混入旧稿 replace 再公告 2 篇首次入馆（1 A / 1 B，最高 DiTGaze 3.72），详见 [XR-Backfill-Report-backfill-1103.md](XR-Backfill-Report-backfill-1103.md)。',
       DATE, 9,
       ['- 门①（同质去重）：最大 Jaccard 0.116 < 0.62，通过，无同质重复。',
        '- 门②（赛道覆盖）：定稿 Top10 覆盖 6 赛道（≥5），通过；全批 8 赛道，纯值排序即满足，未触发重筛。',
        '- 门③（价值天花板）：当日最高分 4.15 < 库内近 30 天 Top10 均分 4.429（现算，393 条入窗）→ 非重磅日、无 S 级，未拔高、未凑数；本批无论文达 S 线（≥4.2），按实数定级。',
        '- Top10 实数说明：按加权降序第 10 名候选为 2610.41680（2.50 C 级，PARTIAL 证据），依「C 级仅入馆不解读」原则不纳入 Top10——**低量日不凑数**。',
        '- 三关均未触发重筛；OUTDATED/SUPERSEDED 0 篇。\n'])

report(BF, f'reports/XR-Backfill-Report-{BFB}.md',
       f'XR Backfill 补录报告 · {BFB}（旧稿再公告）',
       '## 一、执行摘要\n'
       '- **批次性质**：backfill（非当日新提交）——11-02 公告批次中 RSS 混入的旧稿 replace 再公告 2 篇，首次入馆；原始投稿 2511=2025-11（v2 于 2026-10-29 更新）/ 2602=2026-02（v2 于 2026-10-30 更新）。\n'
       '- **补录 2 篇（1 A / 1 B）**：DiTGaze 3.72（南安普顿大学，几何条件 latent DiT 渲染的少样本视线估计数据增强，N=9 受试级误差 5.63°→4.90°、14/15 身份改善 p<0.001）· AdaGS 3.58（香港科技大学（广州），置信门控扩散适应的无位姿稀疏视图 3DGS 重建，DL3DV/Waymo/KITTI 11 基线全面最优）。\n'
       '- **覆盖 2 赛道**；门① 0.116（全池合并复核）；门③ 对 backfill 不适用；OUTDATED 0。\n'
       '- **诚实口径**：全部条目 `batch=backfill-1103` + `orig_window` 标注，绝不混入「当日新论文」。',
       BFB, 10,
       ['- 门①（同质去重）：全池合并复核最大 Jaccard 0.116 < 0.62，通过，无同质重复。',
        '- 门②（赛道覆盖）：覆盖 2 赛道（感知与认知 / 重建与SLAM），2 篇低量批次实际上限。',
        '- 门③（价值天花板）：对 backfill 不适用；本批 2 篇均未达 S 线（最高 DiTGaze 3.72），按实数定级，未拔高。',
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
rep('累计 **717 篇**；跨度 2026-09-15 ~ 2026-10-30',
    '累计 **730 篇**；跨度 2026-09-15 ~ 2026-11-02', 'head-count')
rep('**backfill-1031:6（10-30 公告 RSS 混入旧稿 replace/cross 再公告，首次入馆）**；',
    '**backfill-1031:6（10-30 公告 RSS 混入旧稿 replace/cross 再公告，首次入馆）** · '
    '**2026-11-03:11（11-02 周一公告批次·周末积压，真新提交，非重磅日无S；listing+RSS 两渠道互证 21 篇中 11 篇 XR）** · '
    '**backfill-1103:2（11-02 公告 RSS 混入旧稿 replace 再公告，首次入馆）**；', 'batch-list')
rep('**11-02 周一凌晨状态日 0 新稿**（周末积压公告时刻 08:00 晚于运行时刻，同 10-26 模式；10-30 公告组 show=500 单页复采 declared=got 842 槽位/728 唯一，未入馆 710 篇摘要级 13 篇命中均为 10-31 运行已剔非 XR，0 漏网无 backfill）**。',
    '**11-02 周一凌晨状态日 0 新稿**（周末积压公告时刻 08:00 晚于运行时刻，同 10-26 模式；10-30 公告组 show=500 单页复采 declared=got 842 槽位/728 唯一，未入馆 710 篇摘要级 13 篇命中均为 10-31 运行已剔非 XR，0 漏网无 backfill）**；'
    '**11-03 周二处理 11-02 公告批次（周末积压周一释放；11 篇 XR 新稿 7A/2B/2C + backfill-1103 补录 2 篇 1A/1B，非重磅日无S）**。', 'narrative')

# 7.2 追加 11-03 状态注记（在 11-02 注记后）
note03 = ('> **状态注记（2026-11-03）**：周二 02:30，处理 **2026-11-02（周一）公告批次**（**周末 10-31/11-01 积压于周一 00:00 UTC=08:00 北京时间释放**；公告日≠拉取日，诚实口径；API published 口径核验提交日 10-29×3 / 10-30×8，RSS published 为公告时间戳非提交日）。'
 '漏网对账（先于拉取，TARGET_DAY=2026-10-30）：listing 7 分类最新公告日均为 **11-02**（10-31/11-01 周末无公告日段）；**11-02 组 347 篇唯一论文全部未入馆**（CV 102/GR 4/HC 20/MM 2/RO 72/AI 186/IV 20），摘要级 XR 命中 **21 篇**；cs.AI 首页被 11-02 组挤出 10-30 组尾部 78 条，补采第 2 页完成复采 → 10-30 组未入馆 **710 篇与 11-02 运行集合逐篇一致（差异 0）**，0 漏网无 backfill。'
 'RSS 7 分类去重 540 → KW 命中 32 = **21 篇 11-02 公告组真新提交（11 XR + 10 非 XR）+ 11 篇旧稿 replace/cross 再公告（2 XR → backfill-1103 + 9 非 XR）+ 2 篇库内 v2**；listing 摘要级 21 篇全部被 RSS 覆盖（**RSS 漏网 0 篇**，两渠道互证）。'
 '主批甄别 **XR 核心/强相关 11 篇**（剔非 XR 10 篇：WorldBridge 机器人世界动作模型/胰腺 MRI 分割/Hawkeye 场景文字识别/HandMimicX 机器人灵巧操作/Pinching Antennas 6G ISAC 波导天线/DUGO 第一视角在线动作定位/机器人穿刺标定/柔性臂机器人控制/差速轮机器人 SLAM/Nexus-VLA 跨本体 VLA）；全文 **12 篇 L0/FULL + 1 篇 L1/PARTIAL**（2610.41680 arXiv HTML 404、ar5iv 仅摘要页，摘要级评估并显式声明）。'
 'Top10（**实数 9 篇**，第 10 名候选 2610.41680 为 C 级不纳入）：**7 A / 2 B 主批非 C 部分，最高 4.15（VoxLution/DrawSplat 并列），无 S 级**；覆盖 6 赛道（内容生成×1/重建与SLAM×3/评估与数据集×1/神经渲染×1/化身与人体×1/感知与认知×2；全批 8 赛道）。'
 '三关：门① max Jaccard **0.116**；门② 6 赛道；门③ 当日最高 4.15 < 库内近 30 天 Top10 均分 **4.429**（393 条入窗，现算）→ **非重磅日、无 S 级，未拔高**；OUTDATED 0。'
 '**backfill-1103**：旧稿 replace 再公告 2 篇首次入馆（1 A / 1 B，最高 DiTGaze 3.72，无 S 线；原始投稿 2511=2025-11 / 2602=2026-02）。'
 'registry 717 → **730**（+11 +2）。详见 [运行报告](../../reports/XR-Daily-Report-2026-11-03.md) 与 [MOC-2026-11-03](./MOC-2026-11-03.md) / [MOC-backfill-1103](./MOC-backfill-1103.md) / [Backfill 报告](../../reports/XR-Backfill-Report-backfill-1103.md)。\n')
anchor = '> **状态注记（2026-11-02）**'
i = h.find(anchor)
assert i >= 0, 'ANCHOR NOT FOUND: note1102'
j = h.find('[状态报告](../../reports/XR-Daily-Report-2026-11-02.md)。', i)
if j < 0:
    j = h.find('\n\n', i)
else:
    j = h.find('\n', j) + 1
h = h[:j] + note03 + h[j:]

# 7.3 速查入口
rep('| 最新一期 | [MOC · 2026-10-31](./MOC-2026-10-31.md) |',
    '| 最新一期 | [MOC · 2026-11-03](./MOC-2026-11-03.md) |', 'quick-latest')
rep('| 上一期 | [MOC · 2026-10-29](./MOC-2026-10-29.md) |',
    '| 上一期 | [MOC · 2026-10-31](./MOC-2026-10-31.md) |', 'quick-prev')
rep('（现有 408 篇）', '（现有 420 篇）', 'quick-notes')
rep('| 最新运行状态 | [运行报告 2026-10-31](../../reports/XR-Daily-Report-2026-10-31.md)（10-30 公告批次 18 篇 13A/5B 非重磅日无S + backfill-1031 补录 6 篇 5A/1B；10-29 公告跳空后延迟释放；listing+RSS 两渠道互证，RSS 漏网 0 篇；全文全 L0/FULL） |',
    '| 最新运行状态 | [运行报告 2026-11-03](../../reports/XR-Daily-Report-2026-11-03.md)（11-02 周一公告批次·周末积压 11 篇 7A/2B/2C 非重磅日无S + backfill-1103 补录 2 篇 1A/1B；listing+RSS 两渠道互证，RSS 漏网 0 篇；全文 12×L0/FULL + 1×L1/PARTIAL；Top10 实数 9 篇） |', 'quick-status')

# 7.4 批次索引表追加两行
row_main = ('| 2026-11-03 | [MOC-2026-11-03](./MOC-2026-11-03.md) | XR 11（Top10 实数 9）· 7A/2B/2C · 非重磅日（无S） | '
            '11-02 公告批次（周末积压周一释放）真新提交 11 篇；listing+RSS 两渠道互证 21 篇中 11 篇 XR；全文 12×L0/FULL + 1×L1/PARTIAL |')
row_bf = ('| backfill-1103 | [MOC-backfill-1103](./MOC-backfill-1103.md) | 补录 2（1A/1B）· 非当日新提交 | '
          '11-02 公告 RSS 混入旧稿 replace 再公告 2 篇（2511/2602） |')
rep('| 2026-11-02 | — | **0 新稿**（周一凌晨：listing 七分类最新公告日 10-30 + API 前沿 10-29 + RSS 7 分类空源三源互证；周末积压公告时刻 08:00 晚于运行时刻） | 状态报告日；10-30 公告组 show=500 单页复采 declared=got（842 槽位/728 唯一），未入馆 710 篇摘要级 13 篇命中均为已剔非 XR，0 漏网；门③ 现算 4.429 |',
    '| 2026-11-02 | — | **0 新稿**（周一凌晨：listing 七分类最新公告日 10-30 + API 前沿 10-29 + RSS 7 分类空源三源互证；周末积压公告时刻 08:00 晚于运行时刻） | 状态报告日；10-30 公告组 show=500 单页复采 declared=got（842 槽位/728 唯一），未入馆 710 篇摘要级 13 篇命中均为已剔非 XR，0 漏网；门③ 现算 4.429 |\n'
    + row_main + '\n' + row_bf, 'batch-table')

# 7.5 追加 Top10 段（文件尾）
seg = '\n### 2026-11-03 新增（Top10 实数 9 篇：7 A / 2 B 非 C 部分，非重磅日无 S）\n\n| # | 论文 | 赛道 | 分值 | 等级 | 证据 |\n|---:|---|---|---:|---|---|\n'
for i2, p in enumerate(MAIN, 1):
    seg += f"| {i2} | {esc(p['title_zh'])} | {p['track']} | {p['value']:.2f} | {p['grade']} | {p['evidence']} |\n"
seg += '\n### backfill-1103 补录（2 篇：1 A + 1 B，非当日新提交）\n\n| # | 论文 | 赛道 | 分值 | 等级 | 证据 |\n|---:|---|---|---:|---|---|\n'
for i2, p in enumerate(BF, 1):
    seg += f"| {i2} | {esc(p['title_zh'])} | {p['track']} | {p['value']:.2f} | {p['grade']} | {p['evidence']} |\n"
h = h.rstrip() + '\n' + seg

# 7.6 页脚计数
rep('*最后更新：2026-11-02（周一凌晨状态日：listing 七分类最新公告日 10-30 + API 前沿 10-29 + RSS 7 分类空源三源互证；周末积压公告时刻 08:00 晚于运行时刻；10-30 公告组 show=500 单页复采 declared=got，未入馆 710 篇摘要级 13 篇命中均为已剔非 XR，0 漏网无 backfill；registry 717 / 笔记 408）。*',
    '*最后更新：2026-11-03（11-02 周一公告批次·周末积压：11 篇 XR 新稿 7A/2B/2C 非重磅日无S + backfill-1103 补录 2 篇 1A/1B；listing+RSS 两渠道互证，RSS 漏网 0 篇；全文 12×L0/FULL + 1×L1/PARTIAL；门③ 现算 4.429；Top10 实数 9 篇） · 库内 **730 篇** · 原子笔记 **420 篇** · MOC 36 份', 'footer')

open(moc_path, 'w', encoding='utf-8').write(h)
print('MOC-总索引 refreshed（%d -> %d chars）' % (n0, len(h)))
print('DONE')
