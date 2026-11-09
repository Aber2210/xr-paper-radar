# -*- coding: utf-8 -*-
"""2026-11-10 产物生成：主批（11-09 公告批次 14 篇）+ backfill-1110（4 篇旧稿 v2+ 再公告）。

诚实口径：公告日 2026-11-09（周一 00:00 UTC = 08:00 北京时间释放周末 11-07/11-08 积压）≠ 拉取日 2026-11-10（周二 02:30）。
API published 核验提交日：17 篇 v1 中 1 篇 11-05 + 16 篇 11-06（均早于公告日；RSS published 为公告时间戳）。
消费 data/scored_1110.json；registry 幂等追加（先备份，in_top10 按定稿显式设置）。"""
import json, os, shutil, glob

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
os.chdir(ROOT)
D = json.load(open('data/scored_1110.json', encoding='utf-8'))
MAIN = D['main']
BF = D['backfill']
TOP10_IDS = set(D['top10_ids'])
TOP10_ORDER = list(D['top10_ids'])
DATE, ANN = '2026-11-10', '2026-11-09'
GATE3 = 4.399
TODAY_MAX = MAIN[0]['value']
MANIFEST = json.load(open('data/fulltext/_manifest.json', encoding='utf-8'))
for p in MAIN + BF:
    p['level'] = MANIFEST[p['id']]['level']
    p['announce'] = 'replace' if p['batch'] == 'backfill-1110' else 'new'
TOP10 = [p for pid in TOP10_ORDER for p in MAIN if p['id'] == pid]
assert [p['id'] for p in TOP10] == TOP10_ORDER
assert len(MAIN) == 14 and len(BF) == 4


def esc(s):
    return str(s).replace('|', '/')


def dim_row(p, star):
    s = p['scores']
    return (f"| {p['id']} | {esc(p['title_zh'])} {'⭐' if star else ''} | {p['track']} | "
            f"{s['IMP']} | {s['NOV']} | {s['TEC']} | {s['EXP']} | {s['PER']} | {s['TRL']} | {s['REP']} | "
            f"{p['value']:.2f} | {p['grade']} | {p['evidence']} | {p['announce']} |")


TBL_HEAD = ('| arXiv | 标题 | 赛道 | IMP | NOV | TEC | EXP | PER | TRL | REP | 总分 | 等级 | 证据 | 公告类型 |\n'
            '|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|\n')
os.makedirs(f'papers/daily/{DATE}', exist_ok=True)
os.makedirs('papers/daily/backfill-1110', exist_ok=True)


def seven_table(papers, path, title, intro):
    lines = [f'# {title}\n', intro + '\n', TBL_HEAD]
    for p in papers:
        lines.append(dim_row(p, p['id'] in TOP10_IDS) + '\n')
    open(path, 'w', encoding='utf-8').writelines(lines)


INTRO_MAIN = (
    '批次：2026-11-10（**2026-11-09（周一）公告批次**——公告日 11-09 ≠ 拉取日 11-10（周二 02:30），诚实口径）。\n'
    '候选池 14 篇：漏网对账（先于拉取，`scripts/audit_listing_1110.py`，show=500 单页×7 分类，PREV_DAY=11-06 / NEW_DAY=11-09）→ 7 分类最新公告日均为 **2026-11-09**（周末 11-07/11-08 无公告日段，积压于周一 00:00 UTC = 08:00 北京时间释放，与 11-09 运行预判一致）→ 无漏跑公告日；**11-06 组复采逐分类 declared=got**（CV 138/GR 11/HC 22/MM 2/RO 81/AI 198/IV 6，458 槽位）→ 未入馆 **363 篇**与 11-08/11-09 两次运行的集合逐篇一致（scripts diff 差异 0），沿用上批摘要级复核结论（12 篇命中均为已剔非 XR）→ **0 漏网**。\n'
    '**11-09 组 377 篇唯一论文**（CV 117/GR 7/HC 28/MM 3/RO 60/AI 220/IV 17，452 槽位；376 篇未入馆 + 1 篇跨列表已在库）→ `scripts/filter_missed_xr_abstract_1110.py` 摘要级 XR 命中 **18 篇**（data/missed_xr_abstract_1110.json，meta fetched 377/377）。\n'
    '数据源：export.arxiv.org **502**（本批实测）→ 切 `https://arxiv.org/api/query`（200，submittedDate 前沿 11-06）；RSS 7 分类去重 **660** → KW 命中 **31**（cs.CV 210 / cs.AI 397 / cs.RO 103 / cs.HC 40 / eess.IV 24 / cs.GR 8 / cs.MM 4，lastBuildDate 2026-11-09 05:00 UTC）。\n'
    '甄别：RSS 31 = **17 篇 v1 真新提交**（1 篇 11-05 + 16 篇 11-06 提交，API 版本号核验）+ **9 篇旧稿 v2+ 再公告未入馆**（4 篇 XR → backfill-1110 + 5 篇非 XR）+ **5 篇库内 v2 再公告**（2610.13549 / 2611.00375 / 2611.00482 / 2611.06817 / 2606.16881 剔除）。**listing 摘要级 18 篇命中 = 17 篇 v1 + 1 篇已在库跨列表（2611.06817），RSS 漏网 0 篇，两渠道互证**。\n'
    '全文：18 篇候选（14 + 4）串行 3s/篇：**16 篇 L0/FULL**（25,010–148,056 字符）+ **2 篇 L1/PARTIAL**（2611.09708、2611.09195：arXiv HTML 404 + ar5iv 仅摘要页 4,739/4,731 字符无正文节，本机无 pdfminer/pdftotext 无法解析 PDF → 按摘要级评估并显式声明；人工抽看正文确认非全文）。\n'
    '覆盖度三关：门① 最大 Jaccard **0.054**（2611.09129 vs 库内 2609.38615，<0.62 通过）；门② 定稿 Top10 覆盖 **7 赛道**（全批亦 7 赛道），无需重筛；门③ 当日最高 **4.37 < 库内近 30 天 Top10 均分 4.399**（窗口 2026-10-11~11-10、397 条入窗、现算）→ **非重磅日，无 S 级**；4 篇 ≥4.20（4.37/4.34/4.23/4.23）按校准关记 A。OUTDATED 0。'
)

seven_table(MAIN, f'papers/daily/{DATE}/7dim-table.md', f'{DATE} 全量 7 维度对比表（参考）', INTRO_MAIN)

INTRO_BF = (
    '批次：backfill-1110（**11-09 公告批次 RSS 混入的旧稿 v2/v3/v4 再公告**，首次入馆；原始投稿 2511=2025-11 / 2605=2026-05 / 2607=2026-07，本次更新于 2026-11-06 后再公告）。\n'
    '均非 11-09 当日新提交，诚实口径单独编号；不参与当日「重磅日」判定。\n'
    '候选 4 篇：2605.16981（长序列循环 3D 重建状态更新门的诊断与免训练修正，v4）/ 2511.18127（SFHand 流式第一视角 3D 手部预测，v3）/ 2607.24409（高端街景影像视觉定位精度潜力 + FHNW Muttenz 数据集，v2）/ 2605.31557（EGOSTREAM 第一视角流式情景记忆诊断基准，v3）。全部 L0/FULL 全文后定稿。\n'
    '门② 覆盖 3 赛道（重建与SLAM×2 / 交互与输入×1 / 评估与数据集×1）；本批最高 4.00（2605.16981）未达 S 线。'
)
seven_table(BF, 'papers/daily/backfill-1110/7dim-table.md', 'backfill-1110 全量 7 维度对比表（参考）', INTRO_BF)


# ---------- scored.md ----------
def scored_md(papers, path, title, extra):
    L = [f'# {title}\n', extra + '\n', '| 排名 | arXiv | 标题 | 赛道 | 总分 | 等级 | 证据 | 公告类型 |',
         '|---|---|---|---|---|---|---|---|']
    for i, p in enumerate(papers, 1):
        L.append(f"| {i} | {p['id']} | {esc(p['title_zh'])} | {p['track']} | {p['value']:.2f} | {p['grade']} | {p['evidence']} | {p['announce']} |")
    open(path, 'w', encoding='utf-8').writelines([x + '\n' for x in L])


scored_md(MAIN, f'papers/daily/{DATE}/scored.md', f'{DATE} 评分明细',
    '评分口径：7 维加权 IMP0.20·NOV0.20·TEC0.15·EXP0.15·PER0.15·TRL0.08·REP0.07；分档 S≥4.2 / A3.6–4.2 / B3.0–3.6 / C<3.0。全部基于全文证据定稿（16 篇 L0/FULL + 2 篇 L1/PARTIAL：2611.09708 / 2611.09195 按摘要级评估，TEC/EXP 上限 3、PER 上限 4）。\n'
    '覆盖度三关：门① 最大 Jaccard 0.054 < 0.62（通过，非同质；库侧 token 取 title+title_zh，registry 无摘要字段）；门② 定稿 Top10 覆盖 7 赛道 ≥5（通过，全批亦 7 赛道，未触发重筛）；门③ 当日最高 4.37 < 库内近 30 天 Top10 均分 4.399（现算，397 条入窗）→ **非重磅日，无 S 级**（4 篇 ≥4.20 按校准关记 A）。\n'
    'OUTDATED/SUPERSEDED 0 篇。等级分布：7 A / 7 B。')

scored_md(BF, 'papers/daily/backfill-1110/scored.md', 'backfill-1110 评分明细',
    '评分口径同上；本批为旧稿 v2+ 再公告首次入馆，均非当日新提交。\n'
    '等级分布：2 A / 2 B；最高 2605.16981 4.00（未达 S 线）。门③ 对 backfill 不适用，本批不参与当日重磅日判定。')

# ---------- run_log ----------
run_log_main = f'''# {DATE} 执行日志

## 数据源与对账（第 1-3 步）
- **漏网对账（先于拉取）**：`scripts/audit_listing_1110.py`（PREV_DAY=2026-11-06 上批公告日 / NEW_DAY=2026-11-09；show=500 单页×7 分类，目标组 declared≠got 自动补采后续页 continued/last 兼容）→ 7 分类最新公告日均为 **2026-11-09**；**11-06 组逐分类 declared=got**（CV 138/GR 11/HC 22/MM 2/RO 81/AI 198/IV 6，458 槽位）→ 未入馆 **363 篇**与 11-08/11-09 运行集合**逐篇一致（diff 0）**，沿用上批摘要级结论（12 篇命中均为已剔非 XR）→ **0 漏网**。
- **摘要级 XR 过滤（新公告组）**：11-09 组 **377 篇唯一论文**（CV 117/GR 7/HC 28/MM 3/RO 60/AI 220/IV 17，452 槽位）→ 摘要级 XR 命中 **18 篇**（data/missed_xr_abstract_1110.json；`scripts/convert_newday_1110.py` 转格式 + `scripts/filter_missed_xr_abstract_1110.py`，meta fetched 377/377 全量）。
- **数据源**：`export.arxiv.org` 探针 **HTTP 502**（本批实测）→ 立即切 `https://arxiv.org/api/query`（200，submittedDate 前沿 11-06，与「11-09 公告组来源=11-05/11-06 提交」节律一致）；RSS 7 分类 HTTP 200（cs.CV 210 / cs.AI 397 / cs.RO 103 / cs.HC 40 / eess.IV 24 / cs.GR 8 / cs.MM 4，lastBuildDate 2026-11-09 05:00 UTC）→ 去重 **660** → KW 命中 **31**（WROTE=31）。
- **提交日核验**：API id_list 逐篇 published + 版本号（data/meta_1110.json）→ 17 篇 **v1**（2611.08654 11-05 + 16 篇 11-06）为真新提交；14 篇 **v2+** 为再公告（9 篇未入馆 + 5 篇已在库）。**RSS published 字段是公告时间戳（2026-11-09），不可当提交日**。

## 甄别（第 3 步）
- 主批 XR 核心/强相关 **14 篇**入评分池；剔非 XR **3 篇 v1**（2611.08654 CS-Pi 约束满足流策略采样 / 2611.08857 STRIDE 人形机器人步态 RL / 2611.09679 PIV 自主流场测量）+ **5 篇语义歧义或纯机器人**（2611.09041 DobotTrack 具身行人跟踪 / 2611.09096 TraF 自回归长视频生成「AR=autoregressive」/ 2611.09717 事件相机航天器位姿 / 2611.09795 AR-Edit 视频编辑「AR=autoregressive」/ 2611.08920·2611.08939·2611.09293·2611.08954·2611.09816·2611.08989 标题级候选中经摘要核实为机器人抓取/触觉仿真/世界动作模型/通用空间表征，非 XR）。
- 旧稿 v2+ 未入馆 **9 篇**：**4 篇 XR → backfill-1110**（2605.16981 / 2511.18127 / 2607.24409 / 2605.31557）+ 5 篇非 XR（2604.08410 机器人灵巧抓取 / 2606.01946 电磁跟踪医疗工具 / 2610.26165 TriTD 自回归视频 / 2610.40748 WorldBridge 机器人世界动作模型 / 2611.07551 视频扩散 token 剪枝）。
- 库内 v2 再公告 **5 篇**剔除（2610.13549 / 2611.00375 / 2611.00482 / 2611.06817 / 2606.16881）。

## 全文抓取（第 4 步）
- 18 篇候选跑 `scripts/fetch_fulltext.py`，严格串行 3s/篇（约 1 分钟）：**16 篇 L0/FULL**（25,010–148,056 字符）+ **2 篇 L1/PARTIAL**——2611.09708（可穿戴触觉 I/O）与 2611.09195（InstantHMR）：**arXiv HTML 404（该两稿无 HTML 版）、ar5iv 仅返摘要页（4,839 / 4,731 字符，无 Introduction/Method/Results 节）**，本机缺 pdfminer.six / pdftotext（pip 镜像亦不可达）无法解析 PDF → manifest 改判 PARTIAL 并加 note，按摘要级评估并在 7 维表/报告/笔记显式声明，**未脑补任何未核实的数值或架构**。
- **人工复核**：逐篇检查正文是否含 Introduction/Method/Experiments 节（2611.09584 46,548 字符虽无字面 "Introduction" 但含 Method/Experiment 节，为真实正文）；WROTE=18>0；manifest 合并写入校验通过。

## 评分与三关（第 5-6 步）
- 先抓全文再定稿。7 维加权定稿：主批 **7 A / 7 B**（最高 4.37 立体匹配左右一致性，4 篇 ≥4.20 达 S 线但非重磅日按校准关记 A）。
- 门① 最大 Jaccard **0.054**（2611.09129 TouchAnnotator vs 库内 2609.38615 Exo2EgoHOI；<0.62，非同质）。
- 门② 定稿 Top10 覆盖 **7 赛道**（重建与SLAM×2 / 化身与人体×2 / 触觉与多模态×2 / 内容生成×1 / 系统与平台×1 / 评估与数据集×1 / 感知与认知×1）≥5，通过，**未触发重筛**；全批亦 7 赛道。
- 门③ 当日最高 **4.37 < 库内近 30 天 Top10 均分 4.399**（窗口 2026-10-11~11-10、397 条入窗、现算；Top10 = SMoRe 4.57 / 视频扩散化身 4.57 / Open-HumanScale 4.57 / ACD-GS 4.37 / XM4D 4.36 / RacerGS 4.35 / EgoExplorer 4.30 / dGS-dBS 4.30 / CognitiveReality 4.30 / RESPLE2 4.30）→ **非重磅日，无 S 级**；4 篇达线者按校准关记 A（同 10-24 EgoHand / 10-27 WFM / 11-07 XM4D 先例）。
- OUTDATED/SUPERSEDED **0 篇**。

## 产物（第 7-8 步）
- 报告 2 份（主批 + backfill）+ 原子笔记 18 篇（grade≥B 全覆盖，无 C 级）+ MOC 2 份 + 总索引刷新 + 7 维表/scored/run_log 各 2 套。
- registry 831 → **849**（+14 +4；备份 `papers/library/registry.jsonl.bak-20261110`；按 base_id 幂等）。
- 门③ 现算值供下一批参考：**4.399**（本批 4.37/4.34/4.23/4.23 入窗后会微降）。
'''
open(f'papers/daily/{DATE}/run_log.md', 'w', encoding='utf-8').write(run_log_main)

run_log_bf = f'''# backfill-1110 执行日志

- **来源**：11-09 公告批次 RSS（7 分类去重 660 → KW 命中 31）中 9 篇 v2+ 再公告未入馆者，经摘要+标题核实 XR 相关 4 篇 → 本批；另 5 篇非 XR（2604.08410 机器人灵巧抓取 / 2606.01946 电磁跟踪医疗工具 / 2610.26165 TriTD 自回归视频 / 2610.40748 WorldBridge 世界动作模型 / 2611.07551 视频扩散 token 剪枝）剔除。
- **诚实口径**：本批全部为 **v2/v3/v4 再公告**（2511.18127 v3 / 2605.16981 v4 / 2605.31557 v3 / 2607.24409 v2），原始投稿分别为 2025-11-22 / 2026-05-16 / 2026-05-29 / 2026-07-27，本次更新 2026-11-06 后再公告；均非 11-09 当日新提交，单独编号、不参与当日重磅日判定。
- **全文**：4 篇全部 **L0/FULL**（57,703–148,056 字符），串行 3s/篇，无限流/降级。
- **定稿**：2 A / 2 B。最高 **2605.16981 4.00**（长序列循环 3D 重建的状态更新门诊断 + 免训练帧级门，6 基准长序列 ATE 降 51%）· 2511.18127 3.85（SFHand 流式第一视角 3D 手部预测）· 2607.24409 3.17（街景视觉定位精度潜力 + FHNW Muttenz 数据集）· 2605.31557 3.04（EGOSTREAM 第一视角流式记忆基准）。
- **registry**：+4（batch=backfill-1110，幂等）。
'''
open('papers/daily/backfill-1110/run_log.md', 'w', encoding='utf-8').write(run_log_bf)

# ---------- registry ----------
reg_path = 'papers/library/registry.jsonl'
bak_path = reg_path + '.bak-20261110'
if not os.path.exists(bak_path):
    shutil.copy(reg_path, bak_path)
rows = [json.loads(l) for l in open(reg_path, encoding='utf-8') if l.strip()]
have = {r['id'].split(':')[-1].split('v')[0] for r in rows}
added = 0
with open(reg_path, 'a', encoding='utf-8') as f:
    for p in MAIN + BF:
        if p['id'] in have:
            continue
        entry = dict(id=f"arXiv:{p['id']}", title=p['title'], title_zh=p['title_zh'],
                     track=p['track'], date=DATE, value=p['value'], grade=p['grade'],
                     scores=p['scores'], status=p['status'], evidence=p['evidence'],
                     fetch_level=p['level'], fulltext_chars=0,
                     in_top10=(p['id'] in TOP10_IDS), batch=p['batch'],
                     announce_type=p['announce'], flags=[])
        f.write(json.dumps(entry, ensure_ascii=False) + '\n')
        added += 1
print(f'registry +{added}（现有 {len(rows)+added}）')

# ---------- notes ----------
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
    fn = f"papers/notes/{p['id']}__{slugify(p['slug'])}.md"
    if os.path.exists(fn):
        print('skip existing', fn)
        continue
    body = NOTE_TMPL.format(
        id=p['id'], title=p['title'], title_zh=p['title_zh'], track=p['track'], venue=p['venue'],
        date=DATE, value=f"{p['value']:.2f}", grade=p['grade'], evidence=p['evidence'],
        status=p['status'], IMP=p['scores']['IMP'], NOV=p['scores']['NOV'], TEC=p['scores']['TEC'],
        EXP=p['scores']['EXP'], PER=p['scores']['PER'], TRL=p['scores']['TRL'], REP=p['scores']['REP'],
        level=p['level'], batch=p['batch'], announce=p['announce'],
        in_top10=('true' if p['id'] in TOP10_IDS else 'false'),
        tags=', '.join(p['tags']), conclusion=p['conclusion'], problem=p['problem'],
        method=p['method'], experiments=p['experiments'], innovation=p['innovation'],
        limits=p['limits'], relation=p['relation'], repro=p['repro'], action=p['action'])
    open(fn, 'w', encoding='utf-8').write(body)
    n_notes += 1
print('notes written:', n_notes)


# ---------- MOC ----------
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


moc(MAIN, f'papers/MOC/MOC-{DATE}.md', f'MOC · {DATE}（11-09 公告批次）',
    '> 当日地图：**公告日 2026-11-09（周一）≠ 拉取日 2026-11-10（周二 02:30）**——诚实口径。11-09 00:00 UTC（08:00 北京时间）释放周末 11-07/11-08 积压提交；API published 口径核验提交日 **11-05×1 / 11-06×16**（均早于公告日；RSS published 为公告时间戳）。\n'
    '> 主批 XR 新稿 **14 篇（7 A / 7 B，非重磅日无 S）**，Top10 实数 10 篇最高 **4.37**（立体匹配左右一致性），4 篇 ≥4.20 达 S 线按校准关记 A；listing 11-09 组 377 篇摘要级命中 18 篇中 17 篇 v1 真新（1 篇跨列表已在库），RSS 漏网 0 篇；11-06 组复采 0 漏网。\n'
    '> 全文：16×L0/FULL + 2×L1/PARTIAL（2611.09708、2611.09195：arXiv HTML 404 + ar5iv 摘要页，按摘要级评估并显式声明）。\n'
    '> 覆盖度三关：门① 0.054 / 门② 定稿 Top10 覆盖 7 赛道（无需重筛）/ 门③ 4.37 < 4.399（现算，397 条入窗）→ 非重磅日，无 S。\n'
    '> Top10（实数 10 篇）：Stereo CI 4.37 · HaNDF 4.34 · Emo-LiveSync 4.23 · EventHOI 4.23 · eSharp 3.92 · PoseRieFlow 3.77 · TouchAnnotator 3.70 · ToolDex 3.57 · 可穿戴触觉 I/O 3.53 · VR 视听错位 3.50。')

moc(BF, 'papers/MOC/MOC-backfill-1110.md', 'MOC · backfill-1110（旧稿 v2+ 再公告首次入馆）',
    '> **非当日新提交**：本批 4 篇均为 11-09 公告 RSS 混入的旧稿 v2/v3/v4 再公告（原始投稿 2025-11 ~ 2026-07，2026-11-06 更新），诚实口径单独编号，不参与当日重磅日判定。\n'
    '> 定稿 2 A / 2 B，最高 **2605.16981 4.00**（长序列循环 3D 重建状态更新门，6 基准长序列 ATE 降 51%）。其余：SFHand 3.85 / 街景视觉定位精度潜力 3.17 / EGOSTREAM 3.04。')


# ---------- report ----------
def report(papers, path, title, header, topn, gate_lines):
    L = [f'# {title}\n', header + '\n', '## 二、排行榜（按加权降序）\n',
         '| 排名 | 论文 | 赛道 | 总分 | 等级 | 证据 | 落后标记 |', '|---|---|---|---|---|---|---|']
    for i, p in enumerate(papers[:topn], 1):
        mark = '⛔ OUTDATED' if p['status'] != 'CURRENT' else '—'
        L.append(f"| {i} | {esc(p['title_zh'])}（{p['id']}） | {p['track']} | {p['value']:.2f} | {p['grade']} | {p['evidence']} | {mark} |")
    L.append('\n## 三、逐篇深度解读\n')
    for i, p in enumerate(papers[:topn], 1):
        L.append(f"### 第 {i} 章 · {esc(p['title_zh'])}（{p['id']}，{p['value']:.2f} {p['grade']}，{p['evidence']}）\n")
        L.append(f"- **赛道 / 场合**：{p['track']} / {p['venue']}")
        L.append(f"- **公告类型**：{p['announce']}（公告日 2026-11-09，拉取日 2026-11-10）")
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
    L.append(f'见 [`papers/daily/{DATE}/7dim-table.md`](../papers/daily/{DATE}/7dim-table.md)。\n')
    L.append('## 五、覆盖率校验与筛选过程说明\n')
    L += gate_lines
    L.append('\n## 六、附录：证据等级分布与抓取记录\n')
    nf = sum(1 for p in papers if p['evidence'] == 'FULL')
    np_ = sum(1 for p in papers if p['evidence'] == 'PARTIAL')
    L.append(f'- 本表 {len(papers)} 篇：FULL {nf} 篇；PARTIAL {np_} 篇；ABSTRACT_ONLY 0 篇。')
    L.append('- 抓取降级：18 篇候选串行 3s/篇；16 篇 L0 一次命中；2611.09708 与 2611.09195 该两稿 **arXiv HTML 404**、ar5iv 仅返摘要页（4,839 / 4,731 字符，无正文节），本机无 pdfminer.six/pdftotext（pip 镜像不可达）→ manifest 改判 **PARTIAL** 并加 note，按摘要级评估；TEC/EXP 上限 3、PER 上限 4，**未脑补公式、消融或未提基线**。无限流、无 L5、无 OCR、无伪造。')
    open(path, 'w', encoding='utf-8').writelines([x + '\n' for x in L])


HEADER = (
    '## 一、执行摘要\n'
    '- **公告日 2026-11-09（周一）≠ 拉取日 2026-11-10（周二 02:30）**——诚实口径。11-09 00:00 UTC（08:00 北京时间）释放周末 11-07/11-08 积压提交（上批 11-09 运行处于该时刻之前，故为状态日）；API published 核验提交日 **11-05×1 / 11-06×16**（均早于公告日；RSS published 为公告时间戳非提交日）。\n'
    '- **数据源**：`export.arxiv.org` 探针 **HTTP 502** → 立即切 `https://arxiv.org/api/query`（200，submittedDate 前沿 11-06）；RSS 7 分类 HTTP 200（lastBuildDate 2026-11-09 05:00 UTC）去重 **660** → KW 命中 **31**。两渠道互证：**listing 摘要级 18 篇 = 17 篇 v1 真新 + 1 篇已在库跨列表，RSS 漏网 0 篇**。\n'
    '- **主批 XR 新稿 14 篇（7 A / 7 B；非重磅日，无 S；Top10 实数 10 篇）**。Top10：**跨注入左右一致迭代立体匹配 4.37（Meta/ETH 体系，把「左右不一致」从评测指标变成细化器每步的显式输入线索 + 双向梯度路由一致性损失，5 基准×3 骨干验证，Booster 上 LR 不一致减半以上、单视图视差 15 格中 14 格改善，额外开销仅 +23.9%，代码开源于 facebookresearch/stereo_crossinjection；达 S 线按校准关记 A）** · HaNDF 4.34（物体条件化黎曼神经手部距离场，HOI4D 补全 Δq 16.60°→12.57°、FID 0.156→0.060、生成 FID 0.547 vs LatentHOI 2.784，200 步推理 12 ms，可作 EasyHOI/AlignSDF 插件） · Emo-LiveSync 4.23（LivePortrait 隐关键点空间做音频蒸馏 + 免训练情绪控制门，HDTF LMD 2.74、24 FPS、较 OmniSync 快 6 倍且支持风格化角色） · EventHOI 4.23（密歇根大学+Samsung，事件相机+IMU 自运动抵消驱动选择性 RGB 采集与 HOI 感知编码，常开后端功耗降 5×+、BLE 可传、精度损失 ≤1%，50 小时 Nymeria + 19.8 小时自采真机验证） · eSharp 3.92（WACV 2027，扩散先验迁移到事件流做稠密米制深度，DSEC AbsRel 0.149/-22%、RMSE -39%） · PoseRieFlow 3.77（SO(3)^52 乘积流形上的黎曼流匹配，21.6M 参数做全身文本到姿态） · TouchAnnotator 3.70（特权视图蒸馏的自我中心双手触觉标注，时刻精度 63.29→68.67） · ToolDex 3.57（10,853 条/60 小时 ego-exo 工具使用演示数据集） · 可穿戴触觉 I/O 3.53（36 通道电触觉阵列 + 电容触摸同坐标注册，24 人揭示个体化感知图；PARTIAL 摘要级） · VR 视听错位 3.50（真实感 VR 场景下真实/感知错位对空间感知的影响，理想条件 DT25=-4.61°/DT75=3.82°）。\n'
    '- **覆盖 7 赛道**：重建与SLAM×2 / 化身与人体×2 / 触觉与多模态×2 / 内容生成×1 / 系统与平台×1 / 评估与数据集×1 / 感知与认知×1（全批亦 7 赛道）。\n'
    '- **覆盖度三关**：门① 最大 Jaccard **0.054**（TouchAnnotator vs 库内 Exo2EgoHOI，<0.62）；门② 定稿 Top10 覆盖 **7 赛道** ≥5（未触发重筛）；门③ 当日最高 **4.37 < 库内近 30 天 Top10 均分 4.399**（现算，397 条入窗）→ **非重磅日，无 S 级**（4 篇 ≥4.20 按校准关记 A，未拔高）。\n'
    '- **全文证据**：16 篇 **L0/FULL**（25,010–148,056 字符）+ 2 篇 **L1/PARTIAL**（2611.09708 / 2611.09195：arXiv HTML 404 + ar5iv 摘要页，摘要级评估并显式声明）。\n'
    '- **backfill-1110（4 篇，非当日新提交）**：11-09 公告 RSS 混入的旧稿 v2/v3/v4 再公告首次入馆——2605.16981 4.00（长序列循环 3D 重建状态更新门，ATE 降 51%）· SFHand 3.85 · 街景视觉定位精度潜力 3.17 · EGOSTREAM 3.04。\n'
    '- **路线观察**：① 逐眼立体一致性首次被当作可注入的中间量处理（Stereo CI），直指 AR/VR passthrough 的撕裂/重影痛点，并与库内立体原生前馈 3DGS（10-29 StereoSplat）形成「几何一致性」新主线；② 手-物交互先验同时向「可查询流形」（HaNDF）与「大规模真机数据」（ToolDex 10,853 条 ego-exo）两端推进；③ 智能眼镜系统侧出现完整闭环（EventHOI：事件触发 + 编码 + BLE 链路 + 功耗实测），硬件类渲染缺口（波导/可变焦/Maxwellian/光场）仍待补；④ 感知科学侧两篇（VR 视听错位 N=13 阈值研究、VR 头显生理信号隐性影响 LLM 说服 N=24）共同提示「沉浸式内容的跨模态一致性」是可量化的设计约束。'
)

report(MAIN, f'reports/XR-Daily-Report-{DATE}.md', f'XR 每日论文解读报告 · {DATE}（11-09 公告批次）', HEADER, 10,
       ['- 门①（同质去重）：最大 Jaccard **0.054** < 0.62（2611.09129 TouchAnnotator vs 库内 2609.38615 Exo2EgoHOI），通过，无同质重复。库侧 token 取 title+title_zh（registry 无摘要字段），口径偏保守。',
        '- 门②（赛道覆盖）：定稿 Top10 覆盖 **7 赛道**（重建与SLAM×2 / 化身与人体×2 / 触觉与多模态×2 / 内容生成×1 / 系统与平台×1 / 评估与数据集×1 / 感知与认知×1）≥5，**未触发重筛**；全批亦 7 赛道。同分位（3.50）按「IMP/NOV 降序 → 赛道多样性优先 → id 升序」定序：InstantHMR（化身与人体，已双占）让位 VR 视听错位（感知与认知），仍入馆写 B 级笔记。',
        '- 门③（价值天花板）：当日最高 **4.37** < 库内近 30 天 Top10 均分 **4.399**（现算，窗口 2026-10-11~11-10、397 条入窗；Top10 = SMoRe/视频扩散化身/Open-HumanScale 4.57 · ACD-GS 4.37 · XM4D 4.36 · RacerGS 4.35 · EgoExplorer/dGS-dBS/CognitiveReality/RESPLE2 4.30）→ **非重磅日，无 S 级**；4 篇达 S 线（4.37/4.34/4.23/4.23）按校准关记 A（同 10-24 EgoHand/10-27 WFM/11-07 XM4D 先例）。',
        '- 低量日不凑数原则复核：主批 14 篇全部 grade≥B（7 A + 7 B），Top10 取实数 10 篇（7 A + 3 B），余 4 篇 B 级入馆写笔记；无 C 级、无降格凑数。',
        '- OUTDATED/SUPERSEDED **0 篇**。\n'])

report(BF, 'reports/XR-Backfill-Report-backfill-1110.md', 'XR Backfill 报告 · backfill-1110（旧稿 v2+ 再公告首次入馆）',
       '## 一、执行摘要\n'
       '- **诚实口径**：本批 4 篇均为 **11-09 公告批次 RSS 混入的旧稿 v2/v3/v4 再公告**（原始投稿 2025-11-22 / 2026-05-16 / 2026-05-29 / 2026-07-27，本次更新 2026-11-06 后再公告），首次入馆；**均非 11-09 当日新提交**，单独编号、不参与当日重磅日判定。\n'
       '- **定稿 2 A / 2 B**，最高 **2605.16981 4.00**（诊断 TTT3R 类 per-token 门控记忆视界仅约 3 帧，提出免训练免参数的帧级门 α_t，6 基准长序列 ATE 降 51% 并超过专用长序列方法）。其余：SFHand 3.85（流式语言引导 3D 手部预测 + 新数据集，ADE 相对最强基线降约 30%）· 街景视觉定位精度潜力 3.17（FHNW Muttenz 10 km 路网、真值 6–9 mm，系统化给出视觉定位对测绘级要求的差距）· EGOSTREAM 3.04（2,250 题 × 七维记忆 + Answer Validity Window，8,528 次评测）。\n'
       '- **全文**：4 篇全部 L0/FULL（57,703–148,056 字符），串行 3s/篇，无限流/降级。\n'
       '- **剔除**：同批 v2+ 未入馆 9 篇中 5 篇经摘要核实非 XR（机器人灵巧抓取 / 电磁跟踪医疗工具 / 自回归视频 TriTD / 机器人世界动作模型 WorldBridge / 视频扩散 token 剪枝）。',
       4,
       ['- 门①/门③ 对 backfill 不适用（非当日新提交，不参与重磅日判定）；门② 覆盖 3 赛道（重建与SLAM×2 / 交互与输入×1 / 评估与数据集×1）。',
        '- 本批最高 4.00 未达 S 线，按实数定级。\n'])

# ---------- MOC-总索引 ----------
moc_path = 'papers/MOC/MOC-总索引.md'
h = open(moc_path, encoding='utf-8').read()
n0 = len(h)


def rep(old, new, tag):
    global h
    assert old in h, f'ANCHOR NOT FOUND: {tag}'
    h = h.replace(old, new, 1)


rep('累计 **831 篇**；跨度 2026-09-15 ~ 2026-11-06',
    '累计 **849 篇**；跨度 2026-09-15 ~ 2026-11-09', 'head-count')
rep('**2026-11-07:23（11-06 公告批次真新提交，非重磅日无S；RSS 周六 skipDays 空源、listing 为唯一采集渠道，摘要级命中 35 篇中 23 篇 XR）**；',
    '**2026-11-07:23（11-06 公告批次真新提交，非重磅日无S；RSS 周六 skipDays 空源、listing 为唯一采集渠道，摘要级命中 35 篇中 23 篇 XR）** · '
    '**2026-11-10:14（11-09 公告批次·周末积压，真新提交，非重磅日无S；listing+RSS 两渠道互证 17 篇 v1 中 14 篇 XR）** · '
    '**backfill-1110:4（11-09 公告 RSS 混入旧稿 replace 再公告，首次入馆）**；', 'batch-list')

note10 = ('> **状态注记（2026-11-10）**：周二 02:30，处理 **2026-11-09（周一）公告批次**（公告日≠拉取日，诚实口径；11-09 00:00 UTC = 08:00 北京时间释放周末 11-07/11-08 积压提交，上批 11-09 运行处于该时刻之前故为状态日）。'
 'API published 口径核验提交日 **11-05×1 / 11-06×16**（均早于公告日；RSS published 为公告时间戳）。'
 '漏网对账（先于拉取，`scripts/audit_listing_1110.py`，PREV_DAY=11-06 / NEW_DAY=11-09）：listing 7 分类最新公告日均为 **11-09**（无漏跑公告日）；11-06 组复采逐分类 **declared=got**（CV 138/GR 11/HC 22/MM 2/RO 81/AI 198/IV 6，458 槽位），未入馆 **363 篇与 11-08/11-09 运行集合逐篇一致（diff 0）**、摘要级 12 篇命中均为已剔非 XR → **0 漏网**；**11-09 组 377 篇唯一论文**（CV 117/GR 7/HC 28/MM 3/RO 60/AI 220/IV 17，452 槽位）摘要级 XR 命中 **18 篇**。'
 '**数据源**：export.arxiv.org **502** → 切 `https://arxiv.org/api/query`（200）；RSS 去重 **660** → KW 命中 **31** = 17 篇 v1 真新 + 9 篇旧稿 v2+ 未入馆（4 XR → backfill-1110）+ 5 篇库内 v2；**listing 18 篇 = 17 v1 + 1 已在库跨列表，RSS 漏网 0 篇（两渠道互证）**。'
 '主批甄别 **XR 核心/强相关 14 篇**（剔 v1 非 XR 3 篇 + 语义歧义/纯机器人 5 篇 + 标题级候选经摘要核实非 XR 6 篇）；全文 **16 篇 L0/FULL + 2 篇 L1/PARTIAL**（2611.09708、2611.09195：arXiv HTML 404 + ar5iv 仅摘要页，本机无 PDF 解析器 → 摘要级评估并显式声明）。'
 'Top10（**实数 10 篇**）：最高 **4.37（跨注入左右一致迭代立体匹配），非重磅日无 S**；**4 篇达 S 线（4.37/4.34/4.23/4.23）按校准关记 A**；覆盖 **7 赛道**（重建×2/化身×2/触觉×2/内容生成/系统与平台/评估/感知）。'
 '三关：门① max Jaccard **0.054**（2611.09129 vs 库内 2609.38615 Exo2EgoHOI）；门② 定稿 Top10 覆盖 7 赛道 ≥5（未触发重筛）；门③ 当日最高 4.37 < 库内近 30 天 Top10 均分 **4.399**（397 条入窗，现算）→ **非重磅日，无 S 级**；OUTDATED 0。'
 'registry 831 → **849**（+14 +4）。详见 [运行报告](../../reports/XR-Daily-Report-2026-11-10.md) / [MOC-2026-11-10](./MOC-2026-11-10.md) / [MOC-backfill-1110](./MOC-backfill-1110.md) / [Backfill 报告](../../reports/XR-Backfill-Report-backfill-1110.md)。\n')
anchor_end = '详见 [状态报告](../../reports/XR-Daily-Report-2026-11-09.md)。'
i = h.find(anchor_end)
assert i >= 0, 'ANCHOR NOT FOUND: note1109-end'
j = h.find('\n', i) + 1
h = h[:j] + note10 + h[j:]

rep('| 最新一期 | [MOC · 2026-11-07](./MOC-2026-11-07.md) |',
    '| 最新一期 | [MOC · 2026-11-10](./MOC-2026-11-10.md) |', 'quick-latest')
rep('| 上一期 | [MOC · 2026-11-06](./MOC-2026-11-06.md) |',
    '| 上一期 | [MOC · 2026-11-07](./MOC-2026-11-07.md) |', 'quick-prev')
rep('（现有 502 篇）', '（现有 520 篇）', 'quick-notes')
rep('| 最新运行状态 | [运行报告 2026-11-07](../../reports/XR-Daily-Report-2026-11-07.md)（11-06 公告批次 23 篇 8A/12B/3C 非重磅日无S；RSS 周六 skipDays 空源、listing 唯一采集渠道，386 篇摘要级命中 35 篇中 23 篇 XR；11-05 组复采 0 漏网；全文 22×L0/FULL + 1×L0/PARTIAL；门② 触发一次重筛回补多模态触觉显示，Top10 实数 10 篇覆盖 5 赛道；门③ 现算 4.393） |',
    '| 最新运行状态 | [运行报告 2026-11-10](../../reports/XR-Daily-Report-2026-11-10.md)（11-09 公告批次·周末积压 14 篇 7A/7B 非重磅日无S；listing 377 篇摘要级命中 18 篇 = 17 篇 v1 + 1 已在库，RSS 漏网 0 篇；11-06 组复采 363 篇 diff 0；全文 16×L0/FULL + 2×L1/PARTIAL；Top10 实数 10 篇覆盖 7 赛道（未触发重筛）；门③ 现算 4.399，当日最高 4.37 未达线，4 篇达 S 线按校准关记 A） |', 'quick-status')

row_main = ('| 2026-11-10 | [MOC-2026-11-10](./MOC-2026-11-10.md) | XR 14（Top10 实数 10）· 7A/7B · 非重磅日（无S） | '
            '11-09 公告批次（周末 11-07/11-08 积压周一释放）真新提交 14 篇（11-05×1/11-06×16 提交）；listing 377 篇+RSS 两渠道互证 17 篇 v1 中 14 篇 XR，RSS 漏网 0 篇；11-06 组复采 0 漏网；全文 16×L0/FULL + 2×L1/PARTIAL |\n'
            '| backfill-1110 | [MOC-backfill-1110](./MOC-backfill-1110.md) | 补录 4（2A/2B）· 非当日新提交 | 11-09 公告 RSS 混入旧稿 v2/v3/v4 再公告 4 篇（2511/2605/2605/2607，2026-11-06 更新）；最高 2605.16981 4.00 |')
rep('| 2026-11-09 | — | **0 新稿**（周一凌晨：listing 七分类最新公告日 11-06 + API 前沿 11-05 + RSS 7 分类空源三源互证；周末积压公告时刻 08:00 晚于运行时刻，11-09 公告组尚未释放） | 状态报告日；11-06 公告组 show=500 单页复采 declared=got（458 槽位/386 唯一），未入馆 363 篇与 11-08 运行集合逐篇一致、摘要级 12 篇命中均为 11-07 运行已剔非 XR，0 漏网；门③ 现算 4.399 |',
    '| 2026-11-09 | — | **0 新稿**（周一凌晨：listing 七分类最新公告日 11-06 + API 前沿 11-05 + RSS 7 分类空源三源互证；周末积压公告时刻 08:00 晚于运行时刻，11-09 公告组尚未释放） | 状态报告日；11-06 公告组 show=500 单页复采 declared=got（458 槽位/386 唯一），未入馆 363 篇与 11-08 运行集合逐篇一致、摘要级 12 篇命中均为 11-07 运行已剔非 XR，0 漏网；门③ 现算 4.399 |\n'
    + row_main, 'batch-table')

seg = '\n### 2026-11-10 新增（Top10 实数 10 篇：7 A + 3 B，非重磅日无 S；4 篇达 S 线按校准关记 A）\n\n| # | 论文 | 赛道 | 分值 | 等级 | 证据 |\n|---:|---|---|---:|---|---|\n'
for i2, pid in enumerate(TOP10_ORDER, 1):
    p = next(x for x in MAIN if x['id'] == pid)
    seg += f"| {i2} | {esc(p['title_zh'])} | {p['track']} | {p['value']:.2f} | {p['grade']} | {p['evidence']} |\n"
seg += '\n### backfill-1110 补录（4 篇：2 A + 2 B，非当日新提交）\n\n| # | 论文 | 赛道 | 分值 | 等级 | 证据 |\n|---:|---|---|---:|---|---|\n'
for i2, p in enumerate(BF, 1):
    seg += f"| {i2} | {esc(p['title_zh'])} | {p['track']} | {p['value']:.2f} | {p['grade']} | {p['evidence']} |\n"
h = h.rstrip() + '\n' + seg

rep('*最后更新：2026-11-09（周一凌晨状态日：listing 七分类最新公告日 11-06 + API 前沿 11-05 + RSS 7 分类空源三源互证；周末积压公告时刻 08:00 晚于运行时刻；11-06 公告组 show=500 单页复采 declared=got，未入馆 363 篇与 11-08 运行集合逐篇一致、摘要级 12 篇命中均为 11-07 运行已剔非 XR，0 漏网无 backfill；registry 831 / 笔记 502）。* · MOC 43 份',
    '*最后更新：2026-11-10（11-09 公告批次·周末积压：14 篇 XR 新稿 7A/7B 非重磅日无S；listing 377 篇摘要级命中 18 篇 = 17 篇 v1 + 1 已在库，RSS 漏网 0 篇；11-06 组复采 363 篇 diff 0；export.arxiv.org 502 已切 arxiv.org/api/query；全文 16×L0/FULL + 2×L1/PARTIAL（2611.09708/2611.09195 摘要级）；Top10 覆盖 7 赛道未触发重筛；门③ 现算 4.399，当日最高 4.37 未达线，4 篇达 S 线按校准关记 A；backfill-1110 补录 4 篇 2A/2B）。* · 库内 **849 篇** · 原子笔记 **520 篇** · MOC 45 份',
    'footer')

open(moc_path, 'w', encoding='utf-8').write(h)
print('MOC-总索引 refreshed（%d -> %d chars）' % (n0, len(h)))
print('DONE')
