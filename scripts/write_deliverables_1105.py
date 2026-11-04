# -*- coding: utf-8 -*-
"""2026-11-05 产物生成：主批（11-04 公告批次 9 篇）+ backfill-1105（旧稿 replace/cross 再公告 8 篇）。
公告日 2026-11-04（周三）≠ 拉取日 2026-11-05（周四 02:30），诚实口径。
API published 口径核验提交日：主批 9 篇均为 2026-11-03 提交。
listing 11-03 组 965 篇未入馆摘要级复核 0 漏网；11-04 组 450 篇摘要级 XR 命中 22 篇与 RSS 真新集合逐篇一致。
消费 data/scored_1105.json；registry 幂等追加（先备份，in_top10 按定稿显式设置）。"""
import json, os, shutil, glob

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
os.chdir(ROOT)
D = json.load(open('data/scored_1105.json', encoding='utf-8'))
MAIN, BF = D['main'], D['backfill']
TOP10_IDS = set(D['top10_ids'])
TOP10_ORDER = list(D['top10_ids'])   # 定稿展示顺序（同分多样性优先已体现在该列表；勿用 set 迭代，会丢顺序）
DATE, BFB = '2026-11-05', 'backfill-1105'
ANN = '2026-11-04'          # 公告日（周三）
GATE3 = 4.429               # 门③ 现算均分（窗口 2026-10-06~11-05，447 条入窗）
TODAY_MAX = MAIN[0]['value']  # 3.99
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
    '批次：2026-11-05（**2026-11-04（周三）公告批次**——公告日 11-04 ≠ 拉取日 11-05（周四 02:30），诚实口径）。\n'
    '候选池 9 篇：漏网对账（先于拉取，TARGET_DAY=2026-11-03）listing 7 分类最新公告日均为 **2026-11-04**（无漏跑公告日）；**11-03 组逐分类 declared=got**（CV 395/GR 19/HC 66/MM 7/RO 149/AI 521/IV 33，cs.AI 补采第 2 页 merged=273 后 521/521）→ 未入馆 **965 篇** = 11-04 运行采集的 1,000 篇中 35 篇已入馆（逐篇核验一致，复采新增 0），摘要级复核 **27 篇命中均为 11-04 运行已剔非 XR → 0 漏网**；**11-04 组 450 篇唯一论文**（CV 160/GR 2/HC 21/MM 5/RO 72/AI 252/IV 13）→ 摘要级 XR 命中 **22 篇**。\n'
    'RSS 7 分类去重 **737** → KW 命中 **38** = **22 篇 11-04 公告组真新提交（9 篇 XR + 13 篇非 XR 剔除）+ 13 篇旧稿 replace/cross 再公告（8 篇 XR → backfill-1105 + 5 篇非 XR 剔除）+ 3 篇库内 v2 再公告（剔除）**；listing 摘要级 22 篇**全部被 RSS 覆盖，RSS 漏网 0 篇**——两渠道互证。\n'
    'arXiv API published 口径核验提交日：主批 9 篇**全部为 2026-11-03 提交**（早于公告日 11-04；RSS published 字段为公告时间戳，非提交日）。\n'
    '全文：17 篇候选（主批 9 + backfill 8）串行 3s/篇：**16 篇 L0/FULL**（33,685–142,478 字符）+ **1 篇 L1/PARTIAL**（2611.05359：ar5iv 仅返摘要页 5,282 字符无正文节，manifest 人工复核改判 PARTIAL，按摘要级评估并显式声明，禁止脑补）。\n'
    '覆盖度三关：门① 最大 Jaccard **0.107**（2608.00232 vs 库内 2610.27877 Gaze2HOI，<0.62 通过）；门② 定稿 Top10（实数 7 篇）覆盖 **5 赛道**（评估与数据集×1 / 重建与SLAM×3 / 空间计算×1 / 神经渲染×1 / 世界模型与仿真×1；全批 6 赛道）；门③ 当日最高 **3.99 < 库内近 30 天 Top10 均分 4.429**（窗口 2026-10-06~11-05、447 条入窗、现算）→ **非重磅日、无 S 级**，未拔高。全批无 ≥4.2 达线论文。',
    len(TOP10))

seven_table(BF, f'papers/daily/{BFB}/7dim-table.md',
    f'{BFB} 全量 7 维度对比表（参考）',
    '批次：backfill-1105（**11-04 公告批次中 RSS 混入的旧稿 replace/cross 再公告**（首次入馆；原始投稿 2603=2026-03 ×2 / 2606=2026-06 ×4 / 2607=2026-07 ×1 / 2608=2026-07 ×1，v2-v4 于 2026-11-02/11-03 公告前更新后再公告）；均非 11-04 当日新提交，诚实口径单独编号）。\n'
    '候选 8 篇：VCS-SLAM（可见性一致语义融合 3D 高斯 SLAM）/ SimuScene（物理在环单图组合场景重建）/ EmbedTalk（高斯嵌入说话头合成）/ AniGS（三维场景动画）/ 手语条件崩塌诊断 / 手术 AR 遮挡检测 / FlatLands（单视角 BEV 地板图补全基准）/ 狗耳主动-被动触觉具身研究。全部 L0/FULL 全文后定稿。\n'
    '门③ 对 backfill 不适用；本批不参与当日「重磅日」判定。门① 全池合并复核最大 Jaccard 0.107 < 0.62（通过，无同质重复）；门② 覆盖 6 赛道。\n'
    '注：本批 8 篇均未达 S 线（最高 VCS-SLAM 3.87），按实数定级。',
    len(BF))

# ---------- 2. scored.md + run_log.md ----------
def scored_md(papers, path, title, extra):
    L = [f'# {title}\n', extra + '\n', '| 排名 | arXiv | 标题 | 赛道 | 总分 | 等级 | 证据 | 公告类型 |',
         '|---|---|---|---|---|---|---|---|']
    for i, p in enumerate(papers, 1):
        L.append(f"| {i} | {p['id']} | {esc(p['title_zh'])} | {p['track']} | {p['value']:.2f} | {p['grade']} | {p['evidence']} | {p['announce']} |")
    open(path, 'w', encoding='utf-8').writelines([x + '\n' for x in L])

scored_md(MAIN, f'papers/daily/{DATE}/scored.md', f'{DATE} 评分明细',
    '评分口径：7 维加权 IMP0.20·NOV0.20·TEC0.15·EXP0.15·PER0.15·TRL0.08·REP0.07；分档 S≥4.2 / A3.6–4.2 / B3.0–3.6 / C<3.0。全部基于全文证据定稿（8 篇 L0/FULL + 1 篇 L1/PARTIAL 摘要级）。\n'
    f'覆盖度三关：门① 最大 Jaccard 0.107 < 0.62（通过，非同质）；门② 定稿 Top10（实数 7 篇，C 级仅入馆不解读、低量日不凑数）覆盖 5 赛道 ≥5（通过；全批 6 赛道）；门③ 当日最高 3.99 < 库内近 30 天 Top10 均分 4.429（现算，447 条入窗）→ 非重磅日、无 S 级（校准关，不触发重筛）。\n'
    'OUTDATED/SUPERSEDED 0 篇。等级分布：5 A / 2 B / 2 C。')
scored_md(BF, f'papers/daily/{BFB}/scored.md', f'{BFB} 评分明细',
    '评分口径同上。本批为旧稿 replace/cross 再公告首次入馆（非当日新提交），门③ 不适用。\n'
    '门① 全池合并复核最大 Jaccard 0.107 < 0.62（通过）；门② 覆盖 6 赛道；OUTDATED/SUPERSEDED 0 篇。等级分布：3 A / 5 B。')

run_log_main = f'''# {DATE} 执行日志

## 数据源与对账（第 1-3 步）
- **漏网对账（先于拉取）**：`scripts/audit_listing_1105.py`（TARGET_DAY=2026-11-03，上批公告日；show=500 单页×7 分类 + 目标日组 declared≠got 自动补采后续页）→ 7 分类最新公告日均为 **2026-11-04**（无漏跑公告日）；**11-03 组逐分类 declared=got**（CV 395/GR 19/HC 66/MM 7/RO 149/AI 521/IV 33；cs.CV 与 cs.AI 目标组超 500 触发补页，cs.CV skip=500 merged=55、cs.AI skip=500 merged=273）→ 未入馆 **965 篇** = 11-04 运行采集的 1,000 篇中 35 篇已入馆（逐篇核验一致，复采新增 0），`scripts/run_filter_1105.py` 摘要级复核 **27 篇命中均为 11-04 运行已剔非 XR → 0 漏网、无 backfill**。
- **摘要级 XR 过滤（新公告组）**：11-04 组 **450 篇唯一论文**（CV 160/GR 2/HC 21/MM 5/RO 72/AI 252/IV 13）→ 摘要级 XR 命中 **22 篇**（`data/missed_xr_abstract_1105.json`，meta fetched 1,415/1,415 两组合计）。
- **RSS 主渠道交叉验证**：`scripts/fetch_rss.py` 7 分类全量去重 **737** 条 → KW 命中 **38** = **22 篇 11-04 公告组真新提交（9 篇 XR + 13 篇非 XR）+ 13 篇旧稿 replace/cross 再公告（8 篇 XR → backfill-1105 + 5 篇非 XR 剔除）+ 3 篇库内 v2 再公告（剔除）**。listing 摘要级 22 篇**全部被 RSS 覆盖，RSS 漏网 0 篇**——两渠道互证（本批为低量批次，候选量 10-28 以来最低之一）。
- **API 探针**：双主机 200；`id_list` 口径核验提交日：主批 9 篇**全部为 2026-11-03 提交**（早于公告日 11-04）。RSS published 字段为公告时间戳（11-04），非提交日，两口径已区分。

## 甄别（第 3 步）
- 主批 XR 核心/强相关 **9 篇**入评分池；剔非 XR **13 篇**（2611.05027 多机器人力反馈共享控制 / 2611.04397 无目标相机-LiDAR 外参审计 / 2611.04548 森林冠层空隙预测 / 2611.05172 免训练户型图定位 / 2611.05291 低密度点云分类 / 2611.03932 机器人实时特征匹配 / 2611.04255 手术室人形自主编排 / 2611.04485 视觉基础模型蒸馏 visuomotor 策略 / 2611.04493 MPM 引导 3D 高斯仿真物理扩散策略 / 2611.05163 RoboTryOn 机器人演示合成 / 2611.03651 CARD 证明携带接口 / 2611.03995 音乐元宇宙语义通信 / 2611.04068 遮挡 NLOS 检测）。
- 旧稿 replace/cross 再公告 13 篇中 **8 篇 XR → backfill-1105**（首次入馆，单独编号）；5 篇非 XR 剔除（2606.08029 IntentNav 机器人导航 / 2609.02542 WM-LOCO 人形运动 / 2609.14936 轨迹评估协议 / 2610.34534 社交机器人 HRI（10-28 运行已剔，维持剔除）/ 2607.08227 StatLUT 风格迁移）。
- 库内 v2 再公告 3 篇剔除（2610.13549 ELMA / 2610.27877 Gaze2HOI / 2611.02044 损失感知密度控制）。

## 全文抓取（第 4 步）
- 17 篇候选（主批 9 + backfill 8）跑 `scripts/fetch_fulltext.py`，严格串行 3s/篇（约 1 分 05 秒）：**16 篇 L0/FULL**（33,685–142,478 字符）+ **1 篇 L1/PARTIAL**（2611.05359：ar5iv 仅返摘要页 5,282 字符无正文节——脚本初判 FULL，人工复核 manifest 改判 PARTIAL，按摘要级评估并显式声明）。无限流/降级/伪造。
- manifest 合并写入校验通过；WROTE=17>0。

## 评分与三关（第 5-6 步）
- 先抓全文再定稿。7 维加权定稿：主批 **5 A / 2 B / 2 C**（最高 3.99 3DGS-VBench+；全批无 ≥4.2 达线论文）；backfill **3 A / 5 B**（最高 VCS-SLAM 3.87）。
- 门① 最大 Jaccard **0.107**（2608.00232 vs 库内 2610.27877 Gaze2HOI；<0.62，非同质）。
- 门② 定稿 Top10（实数 7 篇，C 级仅入馆不解读）覆盖 **5 赛道**（评估与数据集×1 / 重建与SLAM×3 / 空间计算×1 / 神经渲染×1 / 世界模型与仿真×1；全批 6 赛道）≥5，通过（低量日不凑数至 10 篇）。
- 门③ 当日最高 **3.99 < 库内近 30 天 Top10 均分 4.429**（窗口 2026-10-06~11-05、447 条入窗、现算）→ **非重磅日、无 S 级**（校准关，不触发重筛）。
- OUTDATED/SUPERSEDED **0 篇**。路线级观察：① 3DGS 建图动态化主线——SettleSplat（视野内持续变化）、Phase-DGS（非同步多视图 4DGS）、VCS-SLAM（语义可靠性融合）同批出现，与库内 MonoGS/SplaTAM/DROID-W/WildGS-SLAM 构成「静态→干扰物→持续变化→语义可靠」推进；② AR 眼镜系统级文献回暖——AR 空间记忆（全栈采集-召回闭环，RayNeo X3 Pro）与手术 AR 遮挡检测（边缘侧内容安全）从系统与安全两端补 AR 工程实证；③ 评测方法论两篇——3DGS-VBench+（渲染质量主观基准）与手语条件崩塌（生成忠实度诊断）分别从画质与语义忠实两端修正评测实践，延续库内「直线不是相机位姿」ATE 审计线；④ 硬件类缺口仍仅 CVQPG + HoOPOE 两篇涉及近眼显示光学（本批无波导/可变焦/Maxwellian/光场新文献）。

## 产物（第 7-8 步）
- 报告 2 份（主报告 + backfill 报告）+ 原子笔记 15 篇（grade≥B：主批 7 + backfill 8；2 篇 C 仅入馆）+ MOC 2 份 + 总索引刷新 + 7 维表/scored/run_log 各 2 套。
- registry 773 → **790**（+9 主批 +8 backfill；备份 `papers/library/registry.jsonl.bak-20261105`；按 base_id 幂等）。
'''
open(f'papers/daily/{DATE}/run_log.md', 'w', encoding='utf-8').write(run_log_main)

run_log_bf = f'''# {BFB} 执行日志

- **批次性质**：backfill（非当日新提交）——11-04 公告批次中 RSS 混入的旧稿 replace/cross 再公告 8 篇首次入馆；原始投稿 2603=2026-03 ×2 / 2606=2026-06 ×4 / 2607=2026-07 ×1 / 2608=2026-07 ×1（arXiv ID 前缀；v2-v4 于 2026-11-02/11-03 公告前更新）。
- **来源**：`scripts/fetch_rss.py` 7 分类全量去重 737 → KW 命中 38；其中 13 篇旧稿再公告经 XR 甄别保留 8 篇（剔非 XR 5 篇：IntentNav 机器人导航 / WM-LOCO 人形运动 / 轨迹评估协议 / 社交机器人 HRI（10-28 已剔）/ StatLUT 风格迁移）。
- **全文**：8 篇全部 L0/FULL，串行 3s/篇，无限流/降级/伪造。
- **评分**：3 A / 5 B（最高 VCS-SLAM 3.87，无 S 线）。门① 全池合并复核最大 Jaccard 0.107 < 0.62；门② 覆盖 6 赛道；门③ 不适用；OUTDATED 0。
- **诚实口径**：全部条目 `batch=backfill-1105` + `orig_window` 标注，绝不混入「当日新论文」。
'''
open(f'papers/daily/{BFB}/run_log.md', 'w', encoding='utf-8').write(run_log_bf)

# ---------- 3. registry（先备份，幂等追加，in_top10 显式） ----------
reg_path = 'papers/library/registry.jsonl'
bak_path = reg_path.replace('.jsonl', '.jsonl.bak-20261105')
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

moc(MAIN, f'papers/MOC/MOC-{DATE}.md', f'MOC · {DATE}（11-04 公告批次）',
    '> 当日地图：**公告日 2026-11-04（周三）≠ 拉取日 2026-11-05（周四 02:30）**——诚实口径。API published 口径核验提交日 **主批 9 篇全部为 2026-11-03 提交**。\n'
    '> 主批 XR 新稿 9 篇（5 A / 2 B / 2 C，无 S——非重磅日）；listing 与 RSS 两渠道互证 22 篇真新提交中 9 篇 XR（RSS 漏网 0 篇）；全文 8 篇 L0/FULL + 1 篇 L1/PARTIAL。\n'
    '> 覆盖度三关：门① 0.107 / 门② 定稿 Top10（实数 7 篇）覆盖 5 赛道（全批 6 赛道）/ 门③ 3.99 < 4.429（现算，447 条入窗）→ 非重磅日无 S。\n'
    '> Top10（实数 7 篇）：3DGS-VBench+ 3.99 · SettleSplat 3.85 · AR 空间记忆 3.70 · Phase-DGS 3.65 · IGSW 3.65 · EndoS3 3.57 · ReconDreamer# 3.38。')
moc(BF, f'papers/MOC/MOC-{BFB}.md', f'MOC · {BFB}（旧稿再公告补录）',
    '> 本批为 **backfill**：11-04 公告批次 RSS 混入的旧稿 replace/cross 再公告 8 篇首次入馆（原始投稿 2603=2026-03 ×2 / 2606=2026-06 ×4 / 2607=2026-07 ×1 / 2608=2026-07 ×1），**均非当日新提交**。\n'
    '> 3 A / 5 B；最高 VCS-SLAM 3.87（无 S 线）。门① 0.107 / 门② 6 赛道 / 门③ 不适用。')

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
    L.append('- 抓取降级：2611.05359 为 L1/PARTIAL（ar5iv 仅返摘要页 5,282 字符无正文节，脚本初判 FULL 经人工复核改判，按摘要级评估并显式声明，未脑补正文细节，C 级仅入馆）；主批其余 8 篇 + backfill 8 篇 L0/FULL。无 L5、无 OCR、无伪造；串行 3s/篇，无限流。')
    open(path, 'w', encoding='utf-8').writelines([x + '\n' for x in L])

report(TOP10,
       f'reports/XR-Daily-Report-{DATE}.md',
       f'XR 每日论文解读报告 · {DATE}（11-04 公告批次）',
       '## 一、执行摘要\n'
       f'- **公告日 2026-11-04（周三）≠ 拉取日 2026-11-05（周四 02:30）**——诚实口径：本批处理的是 11-04 公告批次；API published 口径核验提交日 **主批 9 篇全部为 2026-11-03 提交**（均早于公告日，非当日硬提交；RSS published 为公告时间戳非提交日）。\n'
       '- **主批 XR 新稿 9 篇（5 A / 2 B / 2 C，无 S 级；低量日，Top10 实数 7 篇不凑数）**。Top10：3DGS-VBench+ 3.99（上海交大/京东，3,036 个 3DGS 视频 × 9,108 MOS 的多维主观 VQA 基准 + 参考灵活 LMM 评估器，RR/NR 双模式九项指标全部 SOTA）· SettleSplat 3.85（George Mason/Futurewei，首个视野内持续变化的单目高斯建图，逐高斯动态性场 + 解析渲染深度不确定性门控，Bonn/Co-Fusion 11 序列全图与变化区域双超基线）· AR 空间记忆 3.70（独立研究者，RayNeo X3 Pro 全栈空间记忆系统，131.35 s 回放中 648 次观测仅选 6 次 RGB 采集 + 源链接分级召回，代码开源）· Phase-DGS 3.65（ETRI/首尔国立大，语义相位替代时间戳训练 4DGS，非同步条件最高 +8.5 dB PSNR，即插即用 RealTime-4DGS/FreeTimeGS 两类骨干）· IGSW 3.65（重庆大学，内在解耦 4D 高斯天气编辑，nuScenes/Waymo 四种设置 CLIP-S 与 Sem-CS 全部最高、E_warp 全部最低）· EndoS3 3.57（UCL，实例级语义指导的内镜 3DGS 语义 SLAM + CRCD++ 数据集，CRCD++ 平均 ATE-RMSE 3.03 mm 较次优降 17%）· ReconDreamer# 3.38（中科院自动化所等，驾驶场景重建-生成自进化闭环，Waymo 6 m 横移 NTA-IoU +8.8%、FID −15.1%）。\n'
       '- **覆盖 5 赛道**：评估与数据集×1 / 重建与SLAM×3 / 空间计算×1 / 神经渲染×1 / 世界模型与仿真×1（全批 6 赛道）。\n'
       '- **覆盖度三关**：门① 0.107；门② 定稿 Top10（实数 7 篇）覆盖 5 赛道 ≥5（通过，C 级仅入馆不解读、低量日不凑数至 10 篇）；门③ 3.99 < 4.429（现算，447 条入窗）→ **非重磅日、无 S 级**（全批无 ≥4.2 达线论文）。\n'
       '- **全文证据**：17 篇候选（主批 9 + backfill 8）中 16 篇 L0/FULL（33,685–142,478 字符）+ 1 篇 L1/PARTIAL（2611.05359，ar5iv 仅摘要页，脚本初判 FULL 经人工复核改判，摘要级评估并显式声明，C 级仅入馆）。\n'
       '- **同批 backfill-1105**：RSS 混入旧稿 replace/cross 再公告 8 篇首次入馆（3 A / 5 B，最高 VCS-SLAM 3.87），详见 [XR-Backfill-Report-backfill-1105.md](XR-Backfill-Report-backfill-1105.md)。',
       DATE, 7,
       ['- 门①（同质去重）：最大 Jaccard 0.107 < 0.62，通过，无同质重复。',
        '- 门②（赛道覆盖）：定稿 Top10（实数 7 篇，C 级仅入馆不解读）覆盖 5 赛道（评估与数据集×1 / 重建与SLAM×3 / 空间计算×1 / 神经渲染×1 / 世界模型与仿真×1）≥5，通过；全批 6 赛道。',
        '- 门③（价值天花板）：当日最高分 3.99 < 库内近 30 天 Top10 均分 4.429（现算，447 条入窗）→ 非重磅日、无 S 级，未拔高、未凑数；本批无论文达 S 线（≥4.2），按实数定级。',
        '- 低量日不凑数原则复核：本批 grade≥B 共 7 篇（主批），Top10 按实数取 7 篇（5 A + 2 B），C 级 2 篇仅入馆不解读，未降格凑数至 10 篇。',
        '- OUTDATED/SUPERSEDED 0 篇。\n'])

report(BF, f'reports/XR-Backfill-Report-{BFB}.md',
       f'XR Backfill 补录报告 · {BFB}（旧稿再公告）',
       '## 一、执行摘要\n'
       '- **批次性质**：backfill（非当日新提交）——11-04 公告批次中 RSS 混入的旧稿 replace/cross 再公告 8 篇，首次入馆；原始投稿 2603=2026-03 ×2 / 2606=2026-06 ×4 / 2607=2026-07 ×1 / 2608=2026-07 ×1（v2-v4 于 2026-11-02/11-03 公告前更新）。\n'
       '- **补录 8 篇（3 A / 5 B）**：VCS-SLAM 3.87（NYU/NYU Abu Dhabi，可见性一致语义融合 3D 高斯 SLAM，Replica ATE 0.30 cm、Depth L1 0.321 cm、PSNR 36.03、7.27 FPS、mIoU 95.87%，污染退化率约为基线一半，代码开源）· SimuScene 3.79（首尔国立大，物理在环单图组合场景重建，ABO 0.507 vs SAM3D 0.218、穿透率降至 2.5%，代码开源）· EmbedTalk 3.73（利兹大学，逐高斯嵌入替代 tri-plane 的说话头合成，自驱动 PSNR 35.186、Sync-C 6.520 为 3DGS 类最高、模型 10.20 MB 笔记本 61 FPS）· AniGS 3.58（UIUC/Meta，大型杂乱可导航场景的场景级 3DGS 动画，FVD-LTX 415.89 vs Gaussians2Life 902.03 / PhysDreamer 839.46）· 手语条件崩塌诊断 3.57（George Mason，免训练三层诊断 + per-dataset GT-vs-GT 校准，How2Sign 14 检查点全部 ρ_faith 0.95–1.00 未达参考 0.849，FID 与忠实度脱节）· 手术 AR 遮挡检测 3.51（杜克大学，首个伪 AR 手术遮挡基准 350 张/7 类 + 级联小到大 VLM，87.43% 准确率、479 ms、时延降 62.90%）· FlatLands 3.37（ANU，270,575 观测单视角 BEV 地板图补全基准 + UMR/MES 新指标，oracle 下生成式样本集超最佳单输出）· 狗耳触觉具身 3.20（Drexel/Virginia Tech，n=28 2×2 被试内：被动触觉最强 5.048 vs 无触觉 3.631，双模态叠加反减益 F(1,27)=9.809）。\n'
       '- **覆盖 6 赛道**；门① 0.107（全池合并复核）；门③ 对 backfill 不适用；OUTDATED 0。\n'
       '- **诚实口径**：全部条目 `batch=backfill-1105` + `orig_window` 标注，绝不混入「当日新论文」。',
       BFB, 8,
       ['- 门①（同质去重）：全池合并复核最大 Jaccard 0.107 < 0.62，通过，无同质重复。',
        '- 门②（赛道覆盖）：覆盖 6 赛道（重建与SLAM×2 / 化身与人体×1 / 神经渲染×1 / 评估与数据集×2 / 空间计算与UI×1 / 触觉与多模态×1），8 篇低量批次实际上限。',
        '- 门③（价值天花板）：对 backfill 不适用；本批 8 篇均未达 S 线（最高 3.87），按实数定级，未拔高。',
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
rep('累计 **773 篇**；跨度 2026-09-15 ~ 2026-11-03',
    '累计 **790 篇**；跨度 2026-09-15 ~ 2026-11-04', 'head-count')
rep('**backfill-1104:8（11-03 公告 RSS 混入旧稿 replace/cross 再公告，首次入馆）**；',
    '**backfill-1104:8（11-03 公告 RSS 混入旧稿 replace/cross 再公告，首次入馆）** · '
    '**2026-11-05:9（11-04 公告批次真新提交，非重磅日无S；listing+RSS 两渠道互证 22 篇中 9 篇 XR）** · '
    '**backfill-1105:8（11-04 公告 RSS 混入旧稿 replace/cross 再公告，首次入馆）**；', 'batch-list')
rep('**11-03 周二处理 11-02 公告批次（周末积压周一释放；11 篇 XR 新稿 7A/2B/2C + backfill-1103 补录 2 篇 1A/1B，非重磅日无S）**。',
    '**11-03 周二处理 11-02 公告批次（周末积压周一释放；11 篇 XR 新稿 7A/2B/2C + backfill-1103 补录 2 篇 1A/1B，非重磅日无S）**；'
    '**11-04 周三处理 11-03 公告批次（35 篇 XR 新稿 13A/12B/10C + backfill-1104 补录 8 篇 5B/3C，非重磅日无S）**；'
    '**11-05 周四处理 11-04 公告批次（9 篇 XR 新稿 5A/2B/2C + backfill-1105 补录 8 篇 3A/5B，非重磅日无S）**。',
    'narrative')

# 7.2 追加 11-05 状态注记（在 11-04 注记后）
note05 = ('> **状态注记（2026-11-05）**：周四 02:30，处理 **2026-11-04（周三）公告批次**（公告日≠拉取日，诚实口径；API published 口径核验提交日 **主批 9 篇全部为 2026-11-03 提交**，RSS published 为公告时间戳非提交日）。'
 '漏网对账（先于拉取，TARGET_DAY=2026-11-03）：listing 7 分类最新公告日均为 **11-04**（无漏跑公告日）；11-03 组复采逐分类 **declared=got**（CV 395/GR 19/HC 66/MM 7/RO 149/AI 521/IV 33；cs.CV 与 cs.AI 目标组超 500 触发补页 merged=55/273），未入馆 **965 篇** = 11-04 运行采集 1,000 篇中 35 篇已入馆（逐篇核验一致、复采新增 0），摘要级复核 27 篇命中均为 11-04 运行已剔非 XR → **0 漏网、无 backfill**；**11-04 组 450 篇唯一论文**（CV 160/GR 2/HC 21/MM 5/RO 72/AI 252/IV 13）摘要级 XR 命中 **22 篇**。'
 'RSS 7 分类去重 **737** → KW 命中 38 = **22 篇 11-04 公告组真新提交（9 XR + 13 非 XR）+ 13 篇旧稿 replace/cross 再公告（8 XR → backfill-1105 + 5 非 XR）+ 3 篇库内 v2**；listing 摘要级 22 篇全部被 RSS 覆盖（**RSS 漏网 0 篇**，两渠道互证）。'
 '主批甄别 **XR 核心/强相关 9 篇**（剔非 XR 13 篇：多机器人力反馈共享控制/无目标相机-LiDAR 外参审计/森林冠层空隙预测/户型图定位/低密度点云分类/机器人特征匹配/手术室人形自主/VFM 蒸馏 visuomotor/MPM 物理扩散策略/RoboTryOn/CARD 证明接口/音乐元宇宙语义通信/NLOS 检测）；全文 **8 篇 L0/FULL + 1 篇 L1/PARTIAL**（2611.05359 ar5iv 仅摘要页，脚本初判 FULL 经人工复核改判，摘要级评估并显式声明，C 级仅入馆）。'
 'Top10（**实数 7 篇**，低量日不凑数）：最高 **3.99（3DGS-VBench+），无 S 级**；覆盖 5 赛道（评估与数据集×1/重建与SLAM×3/空间计算×1/神经渲染×1/世界模型与仿真×1；全批 6 赛道）。'
 '三关：门① max Jaccard **0.107**；门② 定稿 Top10 实数 7 篇覆盖 5 赛道 ≥5（通过）；门③ 当日最高 3.99 < 库内近 30 天 Top10 均分 **4.429**（447 条入窗，现算）→ **非重磅日、无 S 级，未拔高**；OUTDATED 0。'
 '**backfill-1105**：旧稿 replace/cross 再公告 8 篇首次入馆（3 A / 5 B，最高 VCS-SLAM 3.87，无 S 线；原始投稿 2603×2/2606×4/2607×1/2608×1）。'
 'registry 773 → **790**（+9 +8）。详见 [运行报告](../../reports/XR-Daily-Report-2026-11-05.md) 与 [MOC-2026-11-05](./MOC-2026-11-05.md) / [MOC-backfill-1105](./MOC-backfill-1105.md) / [Backfill 报告](../../reports/XR-Backfill-Report-backfill-1105.md)。\n')
anchor_end = '[Backfill 报告](../../reports/XR-Backfill-Report-backfill-1104.md)。'
i = h.find(anchor_end)
assert i >= 0, 'ANCHOR NOT FOUND: note1104-end'
j = h.find('\n', i) + 1
h = h[:j] + note05 + h[j:]

# 7.3 速查入口
rep('| 最新一期 | [MOC · 2026-11-04](./MOC-2026-11-04.md) |',
    '| 最新一期 | [MOC · 2026-11-05](./MOC-2026-11-05.md) |', 'quick-latest')
rep('| 上一期 | [MOC · 2026-11-03](./MOC-2026-11-03.md) |',
    '| 上一期 | [MOC · 2026-11-04](./MOC-2026-11-04.md) |', 'quick-prev')
rep('（现有 449 篇）', '（现有 464 篇）', 'quick-notes')
rep('| 最新运行状态 | [运行报告 2026-11-04](../../reports/XR-Daily-Report-2026-11-04.md)（11-03 公告批次 35 篇 13A/12B/10C 非重磅日无S + backfill-1104 补录 8 篇 5B/3C；listing+RSS 两渠道互证 62 篇中 35 篇 XR，RSS 漏网 0 篇；全文 33×L0/FULL + 2×L1/PARTIAL；门② 触发一次重筛，Top10 实数 10 篇全 A） |',
    '| 最新运行状态 | [运行报告 2026-11-05](../../reports/XR-Daily-Report-2026-11-05.md)（11-04 公告批次 9 篇 5A/2B/2C 非重磅日无S + backfill-1105 补录 8 篇 3A/5B；listing 450 篇+RSS 两渠道互证 22 篇中 9 篇 XR，RSS 漏网 0 篇；全文 16×L0/FULL + 1×L1/PARTIAL；Top10 实数 7 篇覆盖 5 赛道） |', 'quick-status')

# 7.4 批次索引表追加两行
row_main = ('| 2026-11-05 | [MOC-2026-11-05](./MOC-2026-11-05.md) | XR 9（Top10 实数 7）· 5A/2B/2C · 非重磅日（无S） | '
            '11-04 公告批次真新提交 9 篇（全部 11-03 提交）；listing 450 篇+RSS 两渠道互证 22 篇中 9 篇 XR；全文 8×L0/FULL + 1×L1/PARTIAL |')
row_bf = ('| backfill-1105 | [MOC-backfill-1105](./MOC-backfill-1105.md) | 补录 8（3A/5B）· 非当日新提交 | '
          '11-04 公告 RSS 混入旧稿 replace/cross 再公告 8 篇（2603×2/2606×4/2607×1/2608×1） |')
rep('| backfill-1104 | [MOC-backfill-1104](./MOC-backfill-1104.md) | 补录 8（5B/3C）· 非当日新提交 | 11-03 公告 RSS 混入旧稿 replace/cross 再公告 8 篇（2508/2509/2511/2512/2603/2605/2606/2607） |',
    '| backfill-1104 | [MOC-backfill-1104](./MOC-backfill-1104.md) | 补录 8（5B/3C）· 非当日新提交 | 11-03 公告 RSS 混入旧稿 replace/cross 再公告 8 篇（2508/2509/2511/2512/2603/2605/2606/2607） |\n'
    + row_main + '\n' + row_bf, 'batch-table')

# 7.5 追加 Top10 段（文件尾）
seg = '\n### 2026-11-05 新增（Top10 实数 7 篇：5 A + 2 B，非重磅日无 S）\n\n| # | 论文 | 赛道 | 分值 | 等级 | 证据 |\n|---:|---|---|---:|---|---|\n'
for i2, p in enumerate(MAIN, 1):
    seg += f"| {i2} | {esc(p['title_zh'])} | {p['track']} | {p['value']:.2f} | {p['grade']} | {p['evidence']} |\n"
seg += '\n### backfill-1105 补录（8 篇：3 A + 5 B，非当日新提交）\n\n| # | 论文 | 赛道 | 分值 | 等级 | 证据 |\n|---:|---|---|---:|---|---|\n'
for i2, p in enumerate(BF, 1):
    seg += f"| {i2} | {esc(p['title_zh'])} | {p['track']} | {p['value']:.2f} | {p['grade']} | {p['evidence']} |\n"
h = h.rstrip() + '\n' + seg

# 7.6 页脚计数
rep('*最后更新：2026-11-04（11-03 公告批次：35 篇 XR 新稿 13A/12B/10C 非重磅日无S + backfill-1104 补录 8 篇 5B/3C；listing 1000 篇+RSS 两渠道互证 62 篇中 35 篇 XR，RSS 漏网 0 篇；全文 33×L0/FULL + 2×L1/PARTIAL；门② 触发一次重筛（Virtual Box 回补后 5 赛道）；门③ 现算 4.429；Top10 实数 10 篇全 A） · 库内 **773 篇** · 原子笔记 **449 篇** · MOC 38 份',
    '*最后更新：2026-11-05（11-04 公告批次：9 篇 XR 新稿 5A/2B/2C 非重磅日无S + backfill-1105 补录 8 篇 3A/5B；listing 450 篇+RSS 两渠道互证 22 篇中 9 篇 XR，RSS 漏网 0 篇；全文 16×L0/FULL + 1×L1/PARTIAL；Top10 实数 7 篇覆盖 5 赛道；门③ 现算 4.429） · 库内 **790 篇** · 原子笔记 **464 篇** · MOC 40 份',
    'footer')

open(moc_path, 'w', encoding='utf-8').write(h)
print('MOC-总索引 refreshed（%d -> %d chars）' % (n0, len(h)))
print('DONE')
