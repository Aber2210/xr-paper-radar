# -*- coding: utf-8 -*-
"""2026-11-04 产物生成：主批（11-03 公告批次 35 篇）+ backfill-1104（旧稿 replace/cross 再公告 8 篇）。
公告日 2026-11-03（周二）≠ 拉取日 2026-11-04（周三 02:30），诚实口径。
API published 口径核验提交日 10-30×2 / 10-31×7 / 11-01×10 / 11-02×16。
listing 1000 篇摘要级 XR 命中 62 篇与 RSS 真新集合逐篇一致（RSS 漏网 0）。
消费 data/scored_1104.json；registry 幂等追加（先备份，in_top10 按定稿显式设置）。"""
import json, os, shutil, glob

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
os.chdir(ROOT)
D = json.load(open('data/scored_1104.json', encoding='utf-8'))
MAIN, BF = D['main'], D['backfill']
TOP10_IDS = set(D['top10_ids'])
DATE, BFB = '2026-11-04', 'backfill-1104'
ANN = '2026-11-03'          # 公告日（周二）
GATE3 = 4.429               # 门③ 现算均分（窗口 2026-10-05~11-04，406 条入窗）
TODAY_MAX = MAIN[0]['value']  # 3.93
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
    '批次：2026-11-04（**2026-11-03（周二）公告批次**——公告日 11-03 ≠ 拉取日 11-04（周三 02:30），诚实口径）。\n'
    '候选池 35 篇：漏网对账（先于拉取，TARGET_DAY=2026-11-02）listing 7 分类最新公告日均为 **2026-11-03**（无漏跑公告日；11-02 组复采 declared=got 全分类完整，未入馆 336 篇 = 347 篇中 11 篇已由 11-03 运行入馆，摘要级复核 10 篇命中均为已剔非 XR → 0 漏网）；**11-03 组 1,000 篇唯一论文**（CV 395/GR 19/HC 66/MM 7/RO 149/AI 521/IV 33 槽位，cs.AI 首页 500/521 + 补采第 2 页 21 条完成）→ 摘要级 XR 命中 **62 篇**。\n'
    'RSS 7 分类去重 1,492 → KW 命中 89 = **62 篇 11-03 公告组真新提交（35 篇 XR + 27 篇非 XR 剔除）+ 22 篇旧稿 replace/cross 再公告（8 篇 XR → backfill-1104 + 14 篇非 XR 剔除）+ 5 篇库内 v2 再公告（剔除）**；listing 摘要级 62 篇全部被 RSS 覆盖（**RSS 漏网 0 篇**，两渠道互证）。\n'
    'arXiv API published 口径核验提交日：**10-30×2 / 10-31×7 / 11-01×10 / 11-02×16**（均早于公告日 11-03；RSS published 字段为公告时间戳，非提交日）。\n'
    '全文：43 篇候选（主批 35 + backfill 8）串行 3s/篇：**41 篇 L0/FULL**（14,301–178,813 字符）+ **2 篇 L1/PARTIAL**（2611.01229 / 2611.01759：ar5iv 仅摘要页 4,899/5,252 字符，按摘要级评估并显式声明，禁止脑补）。\n'
    '覆盖度三关：门① 最大 Jaccard **0.151**（2611.02658 OctreeSplat vs 库内 2610.27604 HiQGS，<0.62 通过）；门② 纯值 Top10 仅 4 赛道 → 按多样性回补（Virtual Box 替换 SHield）后定稿 Top10 覆盖 **5 赛道**（全批 11 赛道）；门③ 当日最高 **3.93 < 库内近 30 天 Top10 均分 4.429**（窗口 2026-10-05~11-04、406 条入窗、现算）→ **非重磅日、无 S 级**，未拔高。全批无 ≥4.2 达线论文。',
    len(TOP10))

seven_table(BF, f'papers/daily/{BFB}/7dim-table.md',
    f'{BFB} 全量 7 维度对比表（参考）',
    '批次：backfill-1104（**11-03 公告批次中 RSS 混入的旧稿 replace/cross 再公告**（首次入馆；原始投稿 2508=2025-08 / 2509=2025-09 / 2511=2025-11 / 2512=2025-12 / 2603=2026-03 / 2605=2026-05 / 2606=2026-06 / 2607=2026-07，v2 于 2026-11-03 公告前更新后再公告）；均非 11-03 当日新提交，诚实口径单独编号）。\n'
    '候选 8 篇：EAvatar（表情感知头部化身重建）/ 4D-GRT（4D 高斯光线追踪相机效应数据生成）/ Material-GS（数字孪生材质感知高斯泼溅）/ FLEG（前馈语言嵌入高斯泼溅）/ AR 机器人超声脊柱穿刺 / Aes3D（3DGS 美学评估）/ Splaxel（分布式 3DGS 训练）/ VR 眼部验证。全部 L0/FULL 全文后定稿。\n'
    '门③ 对 backfill 不适用；本批不参与当日「重磅日」判定。门① 全池合并复核最大 Jaccard 0.151 < 0.62（通过，无同质重复）；门② 覆盖 6 赛道。\n'
    '注：本批 8 篇均未达 S 线（最高 FLEG 3.58 / AR 超声 3.58），按实数定级。',
    len(BF))

# ---------- 2. scored.md + run_log.md ----------
def scored_md(papers, path, title, extra):
    L = [f'# {title}\n', extra + '\n', '| 排名 | arXiv | 标题 | 赛道 | 总分 | 等级 | 证据 | 公告类型 |',
         '|---|---|---|---|---|---|---|---|']
    for i, p in enumerate(papers, 1):
        L.append(f"| {i} | {p['id']} | {esc(p['title_zh'])} | {p['track']} | {p['value']:.2f} | {p['grade']} | {p['evidence']} | {p['announce']} |")
    open(path, 'w', encoding='utf-8').writelines([x + '\n' for x in L])

scored_md(MAIN, f'papers/daily/{DATE}/scored.md', f'{DATE} 评分明细',
    '评分口径：7 维加权 IMP0.20·NOV0.20·TEC0.15·EXP0.15·PER0.15·TRL0.08·REP0.07；分档 S≥4.2 / A3.6–4.2 / B3.0–3.6 / C<3.0。全部基于全文证据定稿（33 篇 L0/FULL + 2 篇 L1/PARTIAL 摘要级）。\n'
    f'覆盖度三关：门① 最大 Jaccard 0.151 < 0.62（通过，非同质）；门② 纯值 Top10 仅 4 赛道 → 以 Virtual Box（3.65，空间计算与UI）替换同赛道冗余的 SHield（3.80）回补后定稿 Top10 覆盖 5 赛道 ≥5（通过；全批 11 赛道）；门③ 当日最高 3.93 < 库内近 30 天 Top10 均分 4.429（现算，406 条入窗）→ 非重磅日、无 S 级（校准关，不触发重筛）。\n'
    'OUTDATED/SUPERSEDED 0 篇。等级分布：13 A / 12 B / 10 C。')
scored_md(BF, f'papers/daily/{BFB}/scored.md', f'{BFB} 评分明细',
    '评分口径同上。本批为旧稿 replace/cross 再公告首次入馆（非当日新提交），门③ 不适用。\n'
    '门① 全池合并复核最大 Jaccard 0.151 < 0.62（通过）；门② 覆盖 6 赛道；OUTDATED/SUPERSEDED 0 篇。等级分布：5 B / 3 C。')

run_log_main = f'''# {DATE} 执行日志

## 数据源与对账（第 1-3 步）
- **漏网对账（先于拉取）**：`scripts/audit_listing_1104.py`（TARGET_DAY=2026-11-02，上批公告日；show=500 单页×7 分类 + 目标日组 declared≠got 自动补采后续页）→ 7 分类最新公告日均为 **2026-11-03**（无漏跑公告日）；**11-02 组逐分类 declared=got**（CV 102/GR 4/HC 20/MM 2/RO 72/IV 20；cs.AI 首页被 11-03 组占满未露面，`scripts/audit_csai_p2_1104.py` 补采第 2 页 declared=186 got=186）→ 未入馆 **336 篇** = 11-03 运行采集的 347 篇中 11 篇已入馆（逐篇核验一致，复采新增 0），摘要级复核 10 篇命中均为 11-03 运行已剔非 XR → **0 漏网、无 backfill**。
- **摘要级 XR 过滤**：`scripts/filter_missed_xr_abstract.py` 对 11-03 组 1,000 篇跑 API 摘要级过滤（meta fetched 1,000/1,000）→ XR 命中 **62 篇**（`data/missed_xr_abstract_1104.json`）。
- **RSS 主渠道交叉验证**：`scripts/fetch_rss.py` 7 分类全量去重 **1,492** 条 → KW 命中 **89** = **62 篇 11-03 公告组真新提交（35 篇 XR + 27 篇非 XR）+ 22 篇旧稿 replace/cross 再公告（8 篇 XR → backfill-1104 + 14 篇非 XR 剔除）+ 5 篇库内 v2 再公告（剔除）**。listing 摘要级 62 篇**全部被 RSS 覆盖，RSS 漏网 0 篇**——两渠道互证（本批为 10-28 以来命中量最大批次之一）。
- **API 探针**：双主机 200；`id_list` 口径核验提交日：主批 35 篇 = **10-30×2 / 10-31×7 / 11-01×10 / 11-02×16**（均早于公告日 11-03）。RSS published 字段为公告时间戳（11-03），非提交日，两口径已区分。

## 甄别（第 3 步）
- 主批 XR 核心/强相关 **35 篇**入评分池；剔非 XR **27 篇**（2611.00158 可验证机器人 / 2611.00177 AuroraWorld 机器人 exo-to-ego 视频生成 / 2611.00392 蚂蚁学习行走机器人 / 2611.00527 工业探伤神经渲染 / 2611.00657 Spatial DJ 扬声器空间音频 / 2611.00734 长程操作记忆 / 2611.01220 可微迭代学习控制 / 2611.01438 VLM 视频理解效率 / 2611.01491 mmWave 信道估计与 radio SLAM / 2611.01529 放射报告生成 / 2611.01631 放射科决策模型评测 / 2611.01659 人形抓取 / 2611.01677 小米汽车世界模型 / 2611.01684 可穿戴步态评估 / 2611.01778 角色扮演智能体 / 2611.01814 潜空间运动规划 / 2611.01888 4D MRI 重建 / 2611.02026 LVLM 空间智能诊断 / 2611.02393 服装虚拟 IMU 生成 / 2611.02587 Hadith 幻觉基准 / 2611.02794 软体抓取 / 2611.02822 自回归视频扩散 / 2611.02871 人形反应式交互 / 2611.02999 手眼标定 / 2611.03092 个人智能体 / 2611.03268 机器人目标位姿生成 / 2611.03548 人-群交互）。
- 旧稿 replace/cross 再公告 22 篇中 **8 篇 XR → backfill-1104**（首次入馆，单独编号）；14 篇非 XR 剔除（多机器人信念空间规划 / SemICP 医学配准 / 自回归图像生成 / 高自由度机器人感知规划 / 低光感知域自适应 / 场景图运动规划 / ArthroCut 膝关节手术 / LiFT 医学体积合成 / Any-ttach 末端快换 / RoboSnap 真实到仿真 / UAV-DualCog 基准 / 3D-USE 水下增强 / CamTrol++ 相机控制 NVS）。
- 库内 v2 再公告 5 篇剔除（2610.09791 Counterfactual Route Optimization / 2610.10288 TouchScale / 2610.11412 Fresco++ / 2610.27604 HiQGS / 2610.39076 Tactus）。

## 全文抓取（第 4 步）
- 43 篇候选（主批 35 + backfill 8）跑 `scripts/fetch_fulltext.py`，严格串行 3s/篇（约 2 分 48 秒）：**41 篇 L0/FULL**（14,301–178,813 字符）+ **2 篇 L1/PARTIAL**（2611.01229 / 2611.01759：ar5iv 仅返摘要页 4,899/5,252 字符无正文节，manifest 标注 L1，按摘要级评估并显式声明）。无限流/降级/伪造。
- manifest 合并写入校验通过；WROTE=43>0。

## 评分与三关（第 5-6 步）
- 先抓全文再定稿。7 维加权定稿：主批 **13 A / 12 B / 10 C**（最高 3.93 AbacusGS；全批无 ≥4.2 达线论文）；backfill **5 B / 3 C**（最高 FLEG 3.58 / AR 超声 3.58 并列）。
- 门① 最大 Jaccard **0.151**（2611.02658 OctreeSplat vs 库内 2610.27604 HiQGS；<0.62，非同质）。
- 门② **触发一次重筛**：纯值 Top10（3.93 AbacusGS + 七篇 3.85 + 3.80 SHield + 3.78 AnchorComplete）仅覆盖 **4 赛道**（神经渲染×5 / 重建与SLAM×3 / 世界模型与仿真×1 / 化身与人体×1）→ 按赛道多样性回补，以 **Virtual Box 3.65（空间计算与UI）替换同赛道冗余的 SHield 3.80**，定稿 Top10 覆盖 **5 赛道**（神经渲染×4 / 重建与SLAM×3 / 世界模型与仿真×1 / 化身与人体×1 / 空间计算与UI×1；全批 11 赛道）→ 通过。
- 门③ 当日最高 **3.93 < 库内近 30 天 Top10 均分 4.429**（窗口 2026-10-05~11-04、406 条入窗、现算）→ **非重磅日、无 S 级**（校准关，不触发重筛）。
- OUTDATED/SUPERSEDED **0 篇**。路线级观察：① 3DGS 工程化主线密集——AbacusGS（免逐 splat 排序，web/mobile  viewer 瓶颈）、损失感知密度控制、OctreeSplat（前馈八叉树）、VLSplat（物体中心语义）同批出现，与库内 ACD-GS/GradSplat 构成「致密化-排序-前馈-语义」四面推进；② 世界模型生成-重建闭环——GSExplorer 以持久化 3DGS 世界状态闭环视频生成，与库内 EgoExplorer/SMoRe 的世界记忆线呼应；③ 触觉硬件稀缺文献两块——MetamorphX（UIST ’22 CMG 非接地力矩显示）与 Selfrionette（UIST ’24 指尖力输入）补触觉与多模态赛道，硬件类缺口仍仅 CVQPG + HoOPOE 两篇涉及近眼显示光学；④ 基准审计类认知纠正——「直线不是相机位姿」（ATE 协议缺陷）与 GaussFlaw（3DGS 伪影诊断）分别从协议与伪影两端修正领域评测实践。

## 产物（第 7-8 步）
- 报告 2 份（主报告 + backfill 报告）+ 原子笔记 30 篇（grade≥B：主批 25 + backfill 5；13 篇 C 仅入馆）+ MOC 2 份 + 总索引刷新 + 7 维表/scored/run_log 各 2 套。
- registry 730 → **773**（+35 主批 +8 backfill；备份 `papers/library/registry.jsonl.bak-20261104`；按 base_id 幂等）。
'''
open(f'papers/daily/{DATE}/run_log.md', 'w', encoding='utf-8').write(run_log_main)

run_log_bf = f'''# {BFB} 执行日志

- **批次性质**：backfill（非当日新提交）——11-03 公告批次中 RSS 混入的旧稿 replace/cross 再公告 8 篇首次入馆；原始投稿 2508=2025-08 / 2509=2025-09 / 2511=2025-11 / 2512=2025-12 / 2603=2026-03 / 2605=2026-05 / 2606=2026-06 / 2607=2026-07（arXiv ID 前缀；v2 于 2026-11-03 公告前更新）。
- **来源**：`scripts/fetch_rss.py` 7 分类全量去重 1,492 → KW 命中 89；其中 22 篇旧稿再公告经 XR 甄别保留 8 篇（剔非 XR 14 篇：多机器人信念空间规划/SemICP 医学配准/自回归图像生成/高自由度机器人感知规划/低光感知域自适应/场景图运动规划/ArthroCut 膝关节手术/LiFT 医学体积合成/Any-ttach 末端快换/RoboSnap 真实到仿真/UAV-DualCog 基准/3D-USE 水下增强/CamTrol++ 相机控制 NVS）。
- **全文**：8 篇全部 L0/FULL，串行 3s/篇，无限流/降级/伪造。
- **评分**：5 B / 3 C（最高 FLEG 3.58 / AR 超声 3.58 并列，无 S 线）。门① 全池合并复核最大 Jaccard 0.151 < 0.62；门② 覆盖 6 赛道；门③ 不适用；OUTDATED 0。
- **诚实口径**：全部条目 `batch=backfill-1104` + `orig_window` 标注，绝不混入「当日新论文」。
'''
open(f'papers/daily/{BFB}/run_log.md', 'w', encoding='utf-8').write(run_log_bf)

# ---------- 3. registry（先备份，幂等追加，in_top10 显式） ----------
reg_path = 'papers/library/registry.jsonl'
shutil.copy(reg_path, reg_path.replace('.jsonl', '.bak-20261104'))
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

moc(MAIN, f'papers/MOC/MOC-{DATE}.md', f'MOC · {DATE}（11-03 公告批次）',
    '> 当日地图：**公告日 2026-11-03（周二）≠ 拉取日 2026-11-04（周三 02:30）**——诚实口径。API published 口径核验提交日 **10-30×2 / 10-31×7 / 11-01×10 / 11-02×16**。\n'
    '> 主批 XR 新稿 35 篇（13 A / 12 B / 10 C，无 S——非重磅日）；listing 与 RSS 两渠道互证 62 篇真新提交中 35 篇 XR（RSS 漏网 0 篇）；全文 33 篇 L0/FULL + 2 篇 L1/PARTIAL。\n'
    '> 覆盖度三关：门① 0.151 / 门② 纯值 Top10 仅 4 赛道 → Virtual Box 回补替换 SHield 后 5 赛道（全批 11 赛道）/ 门③ 3.93 < 4.429（现算，406 条入窗）→ 非重磅日无 S。\n'
    '> Top10（实数 10 篇）：AbacusGS 3.93 · GSExplorer 3.85 · EgoMo3R 3.85 · MoRE-GS 3.85 · Spade-SLAM 3.85 · 损失感知密度控制 3.85 · UniGS-SLAM 3.85 · OctreeSplat 3.85 · AnchorComplete 3.78 · Virtual Box 3.65。')
moc(BF, f'papers/MOC/MOC-{BFB}.md', f'MOC · {BFB}（旧稿再公告补录）',
    '> 本批为 **backfill**：11-03 公告批次 RSS 混入的旧稿 replace/cross 再公告 8 篇首次入馆（原始投稿 2508=2025-08 / 2509=2025-09 / 2511=2025-11 / 2512=2025-12 / 2603=2026-03 / 2605=2026-05 / 2606=2026-06 / 2607=2026-07），**均非当日新提交**。\n'
    '> 5 B / 3 C；最高 FLEG 3.58 / AR 超声 3.58 并列（无 S 线）。门① 0.151 / 门② 6 赛道 / 门③ 不适用。')

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
    L.append('- 抓取降级：2611.01229 / 2611.01759 为 L1/PARTIAL（ar5iv 仅摘要页 4,899/5,252 字符，按摘要级评估并显式声明，未脑补正文细节，两篇均为 C 级仅入馆不解读）；主批其余 33 篇 L0/FULL。无 L5、无 OCR、无伪造；串行 3s/篇，无限流。')
    open(path, 'w', encoding='utf-8').writelines([x + '\n' for x in L])

report(TOP10,
       f'reports/XR-Daily-Report-{DATE}.md',
       f'XR 每日论文解读报告 · {DATE}（11-03 公告批次）',
       '## 一、执行摘要\n'
       f'- **公告日 2026-11-03（周二）≠ 拉取日 2026-11-04（周三 02:30）**——诚实口径：本批处理的是 11-03 公告批次；API published 口径核验提交日 **10-30×2 / 10-31×7 / 11-01×10 / 11-02×16**（均早于公告日，非当日硬提交；RSS published 为公告时间戳非提交日）。\n'
       '- **主批 XR 新稿 35 篇（13 A / 12 B / 10 C，无 S 级）**。Top10（实数 10 篇）：AbacusGS 3.93（Memphis/NUS，把 3DGS 混合顺序存进场景布局，CPU 排序 4.5×、文件 19.3 vs 248 字节、平均仅损 0.13 dB）· GSExplorer 3.85（港科广州/HKU，持久化 3DGS 世界状态的生成-重建闭环，WorldScore 单步 82.85 超最强基线 6.24 分、Camera Control 99.07）· EgoMo3R 3.85（Stanford/Panasonic，一阶联合优化同时恢复第一视角相机轨迹、metric 场景几何与 SMPL-X 运动，EgoExo4D 全指标最佳）· MoRE-GS 3.85（Texas A&M，运动机制专家路由的未来 4DGS 预测，D-NeRF 27.47 dB 较 GaussianPrediction +2.13 dB、后规范化 9.2× 加速）· Spade-SLAM 3.85（TUM，稀疏对应锚定+亮度对齐的自监督稠密 SLAM，TartanAir hard 0.50 m 较 D3FlowSLAM 提升 37% 且追平监督版）· 损失感知密度控制 3.85（Sungkyunkwan，把致密化重构为逐操作局部损失削减决策，三数据集 PSNR 全面第一且高斯数更少）· UniGS-SLAM 3.85（SJTU/HKUST，几何-语义解耦单目高斯 SLAM，ScanNet PSNR +4.00 dB、开集 mIoU +11~12 pp）· OctreeSplat 3.85（华东理工/上海开源大学，冻结 DA3-GIANT + 76M 参数的前馈八叉树高斯，Replica 10 视图 32.10 dB）· AnchorComplete 3.78（TUM，部分点云条件下的完整场景网格生成，Replica CD 0.067 较 Seen2Scene 0.132 近半）· Virtual Box 3.65（UBC，手术 AR 交互式 3D 剖面界面，定位误差降 61.6%/深度误差降 78.2%、14/15 被试偏好；**门②赛道回补入选**）。\n'
       '- **覆盖 5 赛道**：神经渲染×4 / 重建与SLAM×3 / 世界模型与仿真×1 / 化身与人体×1 / 空间计算与UI×1（全批 11 赛道）。\n'
       '- **覆盖度三关**：门① 0.151；门② 纯值 Top10 仅 4 赛道 → Virtual Box 替换 SHield 回补后 5 赛道（触发一次重筛并记录）；门③ 3.93 < 4.429（现算，406 条入窗）→ **非重磅日、无 S 级**（全批无 ≥4.2 达线论文）。\n'
       '- **全文证据**：43 篇候选中 41 篇 L0/FULL（14,301–178,813 字符）+ 2 篇 L1/PARTIAL（2611.01229 / 2611.01759，ar5iv 仅摘要页，摘要级评估并显式声明，均为 C 级仅入馆）。\n'
       '- **同批 backfill-1104**：RSS 混入旧稿 replace/cross 再公告 8 篇首次入馆（5 B / 3 C，最高 FLEG 3.58 / AR 超声 3.58 并列），详见 [XR-Backfill-Report-backfill-1104.md](XR-Backfill-Report-backfill-1104.md)。',
       DATE, 10,
       ['- 门①（同质去重）：最大 Jaccard 0.151 < 0.62，通过，无同质重复。',
        '- 门②（赛道覆盖）：纯值 Top10 仅覆盖 4 赛道（神经渲染×5 / 重建与SLAM×3 / 世界模型与仿真×1 / 化身与人体×1）→ **触发重筛**：以 Virtual Box 3.65（空间计算与UI）替换同赛道冗余的 SHield 3.80（神经渲染），回补后定稿 Top10 覆盖 **5 赛道**（≥5 通过；全批 11 赛道）。SHield 仍入馆并保留 A 级评价。',
        '- 门③（价值天花板）：当日最高分 3.93 < 库内近 30 天 Top10 均分 4.429（现算，406 条入窗）→ 非重磅日、无 S 级，未拔高、未凑数；本批无论文达 S 线（≥4.2），按实数定级。',
        '- 低量日不凑数原则复核：本批 grade≥B 共 25 篇（主批），Top10 取满 10 篇且全部 A 级，无降格凑数。',
        '- OUTDATED/SUPERSEDED 0 篇。\n'])

report(BF, f'reports/XR-Backfill-Report-{BFB}.md',
       f'XR Backfill 补录报告 · {BFB}（旧稿再公告）',
       '## 一、执行摘要\n'
       '- **批次性质**：backfill（非当日新提交）——11-03 公告批次中 RSS 混入的旧稿 replace/cross 再公告 8 篇，首次入馆；原始投稿 2508=2025-08 / 2509=2025-09 / 2511=2025-11 / 2512=2025-12 / 2603=2026-03 / 2605=2026-05 / 2606=2026-06 / 2607=2026-07（v2 于 2026-11-03 公告前更新）。\n'
       '- **补录 8 篇（5 B / 3 C）**：FLEG 3.58（SJTU/ECNU，任意视角前馈语言嵌入高斯泼溅，2 视角 ScanNet++ mIoU 46.61 超 Uni3R 39.54、密集 32 视角 60.97 远超 LangSplat 41.24，语义 embedding 仅 3.7%）· AR 引导机器人超声 3.58（TUM，OST-AR 脊柱穿刺系统，16 人 phantom 研究总体时间降 49%、误差降 25%、可用性 +50%）· 4D-GRT 3.43（NeurIPS 2025 Workshop，4D 高斯光线追踪渲染物理相机效应，pinhole 32.80 dB @36.56 FPS 较 MSTH 29.43 @9.38 FPS 量质双升）· Splaxel 3.31（UT Arlington 等，像素级通信分布式 3DGS 训练，Big City Street 7.6× 加速、通信占比 73-80%→10-20%）· EAvatar 3.08（Monmouth/重庆大学，生成式几何先验的表情感知头部化身，NeRSemble 16 视角 PSNR 25.07 超 GHA 24.56）· VR 眼部验证 2.93 · 材质感知高斯泼溅数字孪生 2.78 · Aes3D 3DGS 美学评估 2.72。\n'
       '- **覆盖 6 赛道**；门① 0.151（全池合并复核）；门③ 对 backfill 不适用；OUTDATED 0。\n'
       '- **诚实口径**：全部条目 `batch=backfill-1104` + `orig_window` 标注，绝不混入「当日新论文」。',
       BFB, 10,
       ['- 门①（同质去重）：全池合并复核最大 Jaccard 0.151 < 0.62，通过，无同质重复。',
        '- 门②（赛道覆盖）：覆盖 6 赛道（神经渲染×2 / 空间计算与UI×1 / 系统与平台×1 / 化身与人体×1 / 重建与SLAM×1 / 感知与认知×1 / 评估与数据集×1 中计 6），8 篇低量批次实际上限。',
        '- 门③（价值天花板）：对 backfill 不适用；本批 8 篇均未达 S 线（最高 3.58），按实数定级，未拔高。',
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
rep('累计 **730 篇**；跨度 2026-09-15 ~ 2026-11-02',
    '累计 **773 篇**；跨度 2026-09-15 ~ 2026-11-03', 'head-count')
rep('**backfill-1103:2（11-02 公告 RSS 混入旧稿 replace 再公告，首次入馆）**；',
    '**backfill-1103:2（11-02 公告 RSS 混入旧稿 replace 再公告，首次入馆）** · '
    '**2026-11-04:35（11-03 公告批次真新提交，非重磅日无S；listing+RSS 两渠道互证 62 篇中 35 篇 XR）** · '
    '**backfill-1104:8（11-03 公告 RSS 混入旧稿 replace/cross 再公告，首次入馆）**；', 'batch-list')
rep('registry 717 → **730**（+11 +2）。详见 [运行报告](../../reports/XR-Daily-Report-2026-11-03.md)',
    'registry 717 → **730**（+11 +2）。**11-04 周三处理 11-03 公告批次（35 篇 XR 新稿 13A/12B/10C + backfill-1104 补录 8 篇 5B/3C，非重磅日无S）**。详见 [运行报告](../../reports/XR-Daily-Report-2026-11-04.md)',
    'narrative')

# 7.2 追加 11-04 状态注记（在 11-03 注记后）
note04 = ('> **状态注记（2026-11-04）**：周三 02:30，处理 **2026-11-03（周二）公告批次**（公告日≠拉取日，诚实口径；API published 口径核验提交日 10-30×2 / 10-31×7 / 11-01×10 / 11-02×16，RSS published 为公告时间戳非提交日）。'
 '漏网对账（先于拉取，TARGET_DAY=2026-11-02）：listing 7 分类最新公告日均为 **11-03**（无漏跑公告日）；11-02 组复采逐分类 **declared=got**（cs.AI 首页被 11-03 组占满，补采第 2 页 declared=186 got=186），未入馆 **336 篇** = 11-03 运行采集 347 篇中 11 篇已入馆（逐篇核验一致、复采新增 0），摘要级复核 10 篇命中均为已剔非 XR → **0 漏网、无 backfill**；**11-03 组 1,000 篇唯一论文**（CV 395/GR 19/HC 66/MM 7/RO 149/AI 521/IV 33 槽位）摘要级 XR 命中 **62 篇**。'
 'RSS 7 分类去重 **1,492** → KW 命中 89 = **62 篇 11-03 公告组真新提交（35 XR + 27 非 XR）+ 22 篇旧稿 replace/cross 再公告（8 XR → backfill-1104 + 14 非 XR）+ 5 篇库内 v2**；listing 摘要级 62 篇全部被 RSS 覆盖（**RSS 漏网 0 篇**，两渠道互证）。'
 '主批甄别 **XR 核心/强相关 35 篇**（剔非 XR 27 篇：可验证机器人/机器人 exo-to-ego 视频生成/工业探伤神经渲染/扬声器空间音频/VLM 视频理解/mmWave 信道估计/放射报告生成/人形抓取/汽车世界模型/可穿戴步态评估/LVLM 空间智能诊断/视频扩散/手眼标定等）；全文 **33 篇 L0/FULL + 2 篇 L1/PARTIAL**（2611.01229 / 2611.01759 ar5iv 仅摘要页，摘要级评估并显式声明，两篇均 C 级仅入馆）。'
 'Top10（**实数 10 篇，全 A**）：最高 **3.93（AbacusGS），无 S 级**；覆盖 5 赛道（神经渲染×4/重建与SLAM×3/世界模型与仿真×1/化身与人体×1/空间计算与UI×1；全批 11 赛道）。'
 '三关：门① max Jaccard **0.151**；门② 纯值 Top10 仅 4 赛道 → **触发一次重筛**，以 Virtual Box 3.65（空间计算与UI）替换同赛道冗余的 SHield 3.80 后 5 赛道通过；门③ 当日最高 3.93 < 库内近 30 天 Top10 均分 **4.429**（406 条入窗，现算）→ **非重磅日、无 S 级，未拔高**；OUTDATED 0。'
 '**backfill-1104**：旧稿 replace/cross 再公告 8 篇首次入馆（5 B / 3 C，最高 FLEG 3.58 / AR 超声 3.58 并列，无 S 线；原始投稿 2508/2509/2511/2512/2603/2605/2606/2607）。'
 'registry 730 → **773**（+35 +8）。详见 [运行报告](../../reports/XR-Daily-Report-2026-11-04.md) 与 [MOC-2026-11-04](./MOC-2026-11-04.md) / [MOC-backfill-1104](./MOC-backfill-1104.md) / [Backfill 报告](../../reports/XR-Backfill-Report-backfill-1104.md)。\n')
anchor = '> **状态注记（2026-11-03）**'
i = h.find(anchor)
assert i >= 0, 'ANCHOR NOT FOUND: note1103'
j = h.find('[Backfill 报告](../../reports/XR-Backfill-Report-backfill-1103.md)。', i)
if j < 0:
    j = h.find('\n\n', i)
else:
    j = h.find('\n', j) + 1
h = h[:j] + note04 + h[j:]

# 7.3 速查入口
rep('| 最新一期 | [MOC · 2026-11-03](./MOC-2026-11-03.md) |',
    '| 最新一期 | [MOC · 2026-11-04](./MOC-2026-11-04.md) |', 'quick-latest')
rep('| 上一期 | [MOC · 2026-10-31](./MOC-2026-10-31.md) |',
    '| 上一期 | [MOC · 2026-11-03](./MOC-2026-11-03.md) |', 'quick-prev')
rep('（现有 419 篇）', '（现有 449 篇）', 'quick-notes')
rep('| 最新运行状态 | [运行报告 2026-11-03](../../reports/XR-Daily-Report-2026-11-03.md)（11-02 周一公告批次·周末积压 11 篇 7A/2B/2C 非重磅日无S + backfill-1103 补录 2 篇 1A/1B；listing+RSS 两渠道互证，RSS 漏网 0 篇；全文 12×L0/FULL + 1×L1/PARTIAL；Top10 实数 9 篇） |',
    '| 最新运行状态 | [运行报告 2026-11-04](../../reports/XR-Daily-Report-2026-11-04.md)（11-03 公告批次 35 篇 13A/12B/10C 非重磅日无S + backfill-1104 补录 8 篇 5B/3C；listing+RSS 两渠道互证 62 篇中 35 篇 XR，RSS 漏网 0 篇；全文 33×L0/FULL + 2×L1/PARTIAL；门② 触发一次重筛，Top10 实数 10 篇全 A） |', 'quick-status')

# 7.4 批次索引表追加两行
row_main = ('| 2026-11-04 | [MOC-2026-11-04](./MOC-2026-11-04.md) | XR 35（Top10 实数 10）· 13A/12B/10C · 非重磅日（无S） | '
            '11-03 公告批次真新提交 35 篇；listing 1000 篇+RSS 两渠道互证 62 篇中 35 篇 XR；全文 33×L0/FULL + 2×L1/PARTIAL；门② 重筛一次（Virtual Box 回补） |')
row_bf = ('| backfill-1104 | [MOC-backfill-1104](./MOC-backfill-1104.md) | 补录 8（5B/3C）· 非当日新提交 | '
          '11-03 公告 RSS 混入旧稿 replace/cross 再公告 8 篇（2508/2509/2511/2512/2603/2605/2606/2607） |')
rep('| backfill-1103 | [MOC-backfill-1103](./MOC-backfill-1103.md) | 补录 2（1A/1B）· 非当日新提交 | 11-02 公告 RSS 混入旧稿 replace 再公告 2 篇（2511/2602） |',
    '| backfill-1103 | [MOC-backfill-1103](./MOC-backfill-1103.md) | 补录 2（1A/1B）· 非当日新提交 | 11-02 公告 RSS 混入旧稿 replace 再公告 2 篇（2511/2602） |\n'
    + row_main + '\n' + row_bf, 'batch-table')

# 7.5 追加 Top10 段（文件尾）
seg = '\n### 2026-11-04 新增（Top10 实数 10 篇：全 A，非重磅日无 S）\n\n| # | 论文 | 赛道 | 分值 | 等级 | 证据 |\n|---:|---|---|---:|---|---|\n'
for i2, p in enumerate(MAIN, 1):
    seg += f"| {i2} | {esc(p['title_zh'])} | {p['track']} | {p['value']:.2f} | {p['grade']} | {p['evidence']} |\n"
seg += '\n### backfill-1104 补录（8 篇：5 B + 3 C，非当日新提交）\n\n| # | 论文 | 赛道 | 分值 | 等级 | 证据 |\n|---:|---|---|---:|---|---|\n'
for i2, p in enumerate(BF, 1):
    seg += f"| {i2} | {esc(p['title_zh'])} | {p['track']} | {p['value']:.2f} | {p['grade']} | {p['evidence']} |\n"
h = h.rstrip() + '\n' + seg

# 7.6 页脚计数
rep('*最后更新：2026-11-03（11-02 周一公告批次·周末积压：11 篇 XR 新稿 7A/2B/2C 非重磅日无S + backfill-1103 补录 2 篇 1A/1B；listing+RSS 两渠道互证，RSS 漏网 0 篇；全文 12×L0/FULL + 1×L1/PARTIAL；门③ 现算 4.429；Top10 实数 9 篇） · 库内 **730 篇** · 原子笔记 **419 篇** · MOC 36 份',
    '*最后更新：2026-11-04（11-03 公告批次：35 篇 XR 新稿 13A/12B/10C 非重磅日无S + backfill-1104 补录 8 篇 5B/3C；listing 1000 篇+RSS 两渠道互证 62 篇中 35 篇 XR，RSS 漏网 0 篇；全文 33×L0/FULL + 2×L1/PARTIAL；门② 触发一次重筛（Virtual Box 回补后 5 赛道）；门③ 现算 4.429；Top10 实数 10 篇全 A） · 库内 **773 篇** · 原子笔记 **449 篇** · MOC 38 份',
    'footer')

open(moc_path, 'w', encoding='utf-8').write(h)
print('MOC-总索引 refreshed（%d -> %d chars）' % (n0, len(h)))
print('DONE')
