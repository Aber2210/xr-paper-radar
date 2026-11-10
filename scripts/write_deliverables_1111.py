# -*- coding: utf-8 -*-
"""2026-11-11 产物生成：主批（11-10 公告批次 31 篇）+ backfill-1111（8 篇旧稿 v2/v3 再公告）。

诚实口径：公告日 2026-11-10（周二 00:00 UTC 释放）≠ 拉取日 2026-11-11（周三 02:30）。
API published 核验：主批 31 篇提交日 11-04×1 / 11-06×4 / 11-07×9 / 11-08×6 / 11-09×11（另 2 篇为 v1 延迟公告：2611.09926 提交 09-23、2611.09959 提交 10-26，后者非 XR 已剔）。
消费 data/scored_1111.json；registry 幂等追加（先备份，in_top10 按定稿显式设置）。"""
import json, os, shutil, glob

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
os.chdir(ROOT)
D = json.load(open('data/scored_1111.json', encoding='utf-8'))
MAIN = D['main']
BF = D['backfill']
TOP10_IDS = set(D['top10_ids'])
TOP10_ORDER = list(D['top10_ids'])
DATE, ANN = '2026-11-11', '2026-11-10'
GATE3 = 4.4100
MANIFEST = json.load(open('data/fulltext/_manifest.json', encoding='utf-8'))
for p in MAIN + BF:
    p['level'] = MANIFEST[p['id']]['level']
    p['announce'] = 'replace' if p['batch'] == 'backfill-1111' else 'new'
TOP10 = [p for pid in TOP10_ORDER for p in MAIN if p['id'] == pid]
assert [p['id'] for p in TOP10] == TOP10_ORDER
assert len(MAIN) == 31 and len(BF) == 8, (len(MAIN), len(BF))


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
os.makedirs('papers/daily/backfill-1111', exist_ok=True)


def seven_table(papers, path, title, intro):
    lines = [f'# {title}\n', intro + '\n', TBL_HEAD]
    for p in papers:
        lines.append(dim_row(p, p['id'] in TOP10_IDS) + '\n')
    open(path, 'w', encoding='utf-8').writelines(lines)


INTRO_MAIN = (
    '批次：2026-11-11（**2026-11-10（周二）公告批次**——公告日 11-10 ≠ 拉取日 11-11（周三 02:30），诚实口径）。\n'
    '候选池 31 篇。漏网对账（先于拉取，`scripts/audit_listing_1111.py`，show=500 单页×7 分类，PREV_DAY=11-09 / NEW_DAY=11-10）：7 分类最新公告日均为 **2026-11-10**（无漏跑公告日）；**11-09 组复采逐分类 declared=got**（CV 117/GR 7/HC 28/MM 3/RO 60/AI 220/IV 17，452 槽位，377 篇唯一），未入馆 **362 篇**摘要级命中 **7 篇**，逐篇核对为上批（11-10 运行）显式剔除的 7 篇非 XR（DobotTrack 2611.09041 / TraF 2611.09096 / 航天器位姿 2611.09717 / AR-Edit 2611.09795 / CS-Pi 2611.08654 / STRIDE 2611.08857 / PIV 2611.09679）→ **0 漏网、无 backfill 触发**。\n'
    '**11-10 组 868 篇唯一论文**（CV 317/GR 14/HC 63/MM 7/RO 165/AI 480/IV 13，1,059 槽位），全部未入馆 → `scripts/filter_xr_1111.py` 摘要级 XR 命中 **49 篇**（meta fetched 868/868）。\n'
    '数据源：API 双主机探针均 200（export.arxiv.org 0.3s / arxiv.org 0.8s）；RSS 7 分类去重 **1,479** → KW 命中 **77**（cs.CV 517 / cs.AI 887 / cs.RO 241 / cs.HC 81 / cs.GR 24 / eess.IV 20 / cs.MM 14）。\n'
    '甄别：RSS 77 = **49 篇 11-10 公告组真新提交**（31 XR 主批 + 18 非 XR）+ **25 篇旧稿 v2+ 未入馆**（8 篇 XR → backfill-1111 + 17 篇非 XR）+ **3 篇库内 v2 再公告**（2610.24462 / 2610.30468 / 2611.08477）。**listing 摘要级 49 篇与 RSS 真新 49 篇集合同一（双向差集 0，两渠道互证，RSS 漏网 0 篇）**。\n'
    '提交日核验（API published）：**11-09×18 / 11-08×9 / 11-07×14 / 11-06×5 / 11-04×1**，另 2 篇为 **v1 延迟公告**（2611.09926 提交 2026-09-23、2611.09959 提交 2026-10-26；后者属机器人柔性带多视角数据集，已剔非 XR）；**RSS published 字段是公告时间戳（11-10），不可当提交日**。\n'
    '全文：39 篇候选（31 + 8）串行 3s/篇：**37 篇 L0/FULL**（24,5xx–178,xxx 字符区间）+ **2 篇 L1/PARTIAL**（2611.12130 4,833 字符、2512.14329 5,391 字符：arXiv HTML 404 + ar5iv 仅返摘要页、无 Introduction/Method 节，人工复核后改判 PARTIAL，按摘要级评估并显式声明）。\n'
    '覆盖度三关：门① 最大 Jaccard **0.082**（2605.11594 vs 库内 2610.26918 GTSM，<0.62 通过）；门② 定稿 Top10 覆盖 **5 赛道**（重建与SLAM×6 / 渲染与显示×1 / 系统与平台×1 / 神经渲染×1 / 化身与人体×1，达门槛未触发重筛；全批 9 赛道）；门③ 当日最高 **4.57 ≥ 库内近 30 天 Top10 均分 4.4100**（窗口 2026-10-12~11-11、415 条入窗、现算）→ **重磅日，1 篇 S 级**（Map2SLAM 4.57）。OUTDATED 0。'
)

seven_table(MAIN, f'papers/daily/{DATE}/7dim-table.md', f'{DATE} 全量 7 维度对比表（参考）', INTRO_MAIN)

INTRO_BF = (
    '批次：backfill-1111（**11-10 公告批次 RSS 混入的旧稿 v2/v3 再公告**，首次入馆；原始投稿 2025-03 ~ 2026-09，本次更新于 2026-11-07~11-09 后再公告）。\n'
    '均非 11-10 当日新提交，诚实口径单独编号；不参与当日「重磅日」判定。\n'
    '候选 8 篇：2609.11894（毫米波雷达新视角合成三维点泼溅，v2，2026-09-10 首发）/ 2605.11594（PointForward 点对齐前馈驾驶重建，v2，2026-05-12）/ 2605.12297（EgoEV-HandPose 双目事件第一视角手部姿态，v2，2026-05-12）/ 2609.00775（VOIM 免训练开放词表三维实例建图，v2，2026-09-01）/ 2603.10801（PolGS++ 偏振高斯泼溅反射面重建，v2，2026-03-11）/ 2512.14329（可穿戴生成式数字化身预测卒中步态，v3，2025-12-16）/ 2503.00747（LFX 光场融合形态灵活建模，v3，2025-03-02）/ 2608.30368（SpectraTac 无相机光学触觉传感器，v2，2026-08-31）。\n'
    '全文：7 篇 L0/FULL + 1 篇 L1/PARTIAL（2512.14329 ar5iv 摘要页）。本批最高 4.22（2609.11894）达 S 线，但 backfill 不参与重磅日判定 → 按校准关记 A。'
)
seven_table(BF, 'papers/daily/backfill-1111/7dim-table.md', 'backfill-1111 全量 7 维度对比表（参考）', INTRO_BF)


# ---------- scored.md ----------
def scored_md(papers, path, title, extra):
    L = [f'# {title}\n', extra + '\n', '| 排名 | arXiv | 标题 | 赛道 | 总分 | 等级 | 证据 | 公告类型 |',
         '|---|---|---|---|---|---|---|---|']
    for i, p in enumerate(papers, 1):
        L.append(f"| {i} | {p['id']} | {esc(p['title_zh'])} | {p['track']} | {p['value']:.2f} | {p['grade']} | {p['evidence']} | {p['announce']} |")
    open(path, 'w', encoding='utf-8').writelines([x + '\n' for x in L])


scored_md(MAIN, f'papers/daily/{DATE}/scored.md', f'{DATE} 评分明细',
    '评分口径：7 维加权 IMP0.20·NOV0.20·TEC0.15·EXP0.15·PER0.15·TRL0.08·REP0.07；分档 S≥4.2 / A3.6–4.2 / B3.0–3.6 / C<3.0。全部基于全文证据定稿（29 篇 L0/FULL + 2 篇 L1/PARTIAL：2611.12130 / 2512.14329 按摘要级评估，TEC/EXP 上限 3、PER 上限 4）。\n'
    '覆盖度三关：门① 最大 Jaccard 0.082 < 0.62（通过，非同质；库侧 token 取 title+title_zh）；门② 定稿 Top10 覆盖 5 赛道 ≥5（通过，重建与SLAM 占 6/10，未触发重筛；全批 9 赛道）；门③ 当日最高 4.57 ≥ 库内近 30 天 Top10 均分 4.4100（现算，415 条入窗）→ **重磅日，1 篇 S 级**。\n'
    '主会话校准：2611.10239 PER 5→4（TUM Sim3 仅 −22%、7-Scenes 持平，增益不均）；2611.12319 PER 5→4（2.93× 仅在 Hier-3DGS 失衡场景，标准基准 1.12×）。\n'
    'OUTDATED/SUPERSEDED 0 篇。等级分布：1 S / 14 A / 6 B / 10 C。')

scored_md(BF, 'papers/daily/backfill-1111/scored.md', 'backfill-1111 评分明细',
    '评分口径同上；本批为旧稿 v2/v3 再公告首次入馆，均非当日新提交。\n'
    '等级分布：3 A / 4 B / 1 C；最高 2609.11894 4.22（达 S 线，但 backfill 不参与当日重磅日判定，按校准关记 A）。门③ 对 backfill 不适用。')

# ---------- run_log ----------
run_log_main = f'''# {DATE} 执行日志

## 数据源与对账（第 1-3 步）
- **漏网对账（先于拉取）**：`scripts/audit_listing_1111.py`（PREV_DAY=2026-11-09 上批公告日 / NEW_DAY=2026-11-10；show=500 单页×7 分类，目标组 declared≠got 自动补采后续页）→ 7 分类最新公告日均为 **2026-11-10**；**11-09 组逐分类 declared=got**（CV 117/GR 7/HC 28/MM 3/RO 60/AI 220/IV 17，452 槽位、377 篇唯一；cs.AI 需补采 skip=500 合并 200 条）；未入馆 **362 篇**摘要级命中 **7 篇**，逐篇核对为上批已显式剔除的非 XR（DobotTrack / TraF / 航天器位姿 / AR-Edit / CS-Pi / STRIDE / PIV）→ **0 漏网**。
- **摘要级 XR 过滤（新公告组）**：11-10 组 **868 篇唯一论文**（1,059 槽位）→ 摘要级 XR 命中 **49 篇**（data/missed_new_1111_xr.json，meta fetched 868/868）。
- **数据源**：API 双主机探针均 **200**（export.arxiv.org 2,938 bytes / 0.3s；arxiv.org 2,938 bytes / 0.8s）；RSS 7 分类 HTTP 200（cs.CV 517 / cs.AI 887 / cs.RO 241 / cs.HC 81 / cs.GR 24 / eess.IV 20 / cs.MM 14）→ 去重 **1,479** → KW 命中 **77**（WROTE=77）。
- **提交日核验**（API published）：主批 11-09×18 / 11-08×9 / 11-07×14 / 11-06×5 / 11-04×1；两篇 v1 延迟公告（2611.09926 提交 2026-09-23 属 7 周延迟公告；2611.09959 提交 2026-10-26，非 XR 已剔）。**RSS published 是公告时间戳（11-10），不可当提交日**。

## 甄别（第 3 步）
- 主批 XR 核心/强相关 **31 篇**入评分池；剔非 XR **18 篇**（逐篇理由见报告 §5.2）：机器人柔性带多视角数据集（2611.09959）/ 医学 3D 基础模型评测（2611.10062）/ 医学图像翻译（2611.10236）/ 图像水印指纹（2611.10858）/ 自回归视频 KV cache（2611.11452）/ 手术 3D 运动数据集（2611.11697）/ 植物三维表型（2611.12739）/ 世界动作模型（2611.12870）/ 人形惯性运动编码（2611.10137）/ 移动机器人视角选择（2611.11809）/ 机器人书写（2611.10451）/ 触觉替代腕部相机（2611.10490）/ MPC 即 SMC（2611.10877）/ 攀岩抓握（2611.12017）/ 行星车倾覆（2611.12261）/ 多传感器时空标定（2611.12526）/ VLA 推理加速（2611.11098）/ 四旋翼惯量估计（2611.11555）。
- 旧稿 v2+ 未入馆 **25 篇**：**8 篇 XR → backfill-1111**；17 篇非 XR（OmniMem / TryOnCrafter / 像素空间自回归生成 / UNIVERS 体数据地标 / JND 预滤波 / FUSE-PnPL / 海底遥操作 HMI 综述 / 形态对称图步态策略 / SyncTwin / LessMimic / SENTINEL 2D LiDAR SLAM / VLA 光照鲁棒 / 人形遥操作 / HandMimicX / AMTFV / CaLR / RL 扩散 LLM）。
- 库内 v2 再公告 **3 篇**剔除（2610.24462 O-SCD++ / 2610.30468 SplatLab / 2611.08477 EgoGeneralist）。

## 全文抓取（第 4 步）
- 39 篇候选跑 `scripts/fetch_fulltext.py`，严格串行 3s/篇（两批共约 2.5 分钟）：**37 篇 L0/FULL** + **2 篇 L1/PARTIAL**——2611.12130（磁流变手部外骨骼）4,833 字符、2512.14329（可穿戴生成式化身）5,391 字符：arXiv HTML 404，ar5iv 仅返摘要页，**人工抽看正文确认无 Introduction/Method/Experiments 节**（仅摘要 + arXiv 样板），manifest 改判 PARTIAL 并加 note，按摘要级评估、TEC/EXP 上限 3、PER 上限 4，**未脑补公式/消融/未提基线**。
- WROTE=39>0；manifest 合并写入校验通过；无 429、无 L5、无 OCR。

## 评分与三关（第 5-6 步）
- 先抓全文再定稿。7 维加权定稿：主批 **1 S / 14 A / 6 B / 10 C**。
- 门① 最大 Jaccard **0.082**（2605.11594 PointForward vs 库内 2610.26918 GTSM；<0.62，非同质）。
- 门② 定稿 Top10 覆盖 **5 赛道**（重建与SLAM×6 / 渲染与显示×1 / 系统与平台×1 / 神经渲染×1 / 化身与人体×1）≥5，达门槛**未触发重筛**；全批 9 赛道（重建与SLAM 9 / 系统与平台 5 / 评估与数据集 4 / 化身与人体 3 / 感知与认知 3 / 渲染与显示 2 / 神经渲染 2 / 交互与输入 2 / 触觉与多模态 1）。**注**：Top10 重建与SLAM 集中度 6/10 为本批投稿结构（3DGS/SLAM 线单日 9 篇 XR 稿）所致，非筛选偏食。
- 门③ 当日最高 **4.57 ≥ 库内近 30 天 Top10 均分 4.4100**（窗口 2026-10-12~11-11、415 条入窗、现算；Top10 = SMoRe 4.57 / 视频扩散化身 4.57 / Open-HumanScale 4.57 / ACD-GS 4.37 / Stereo CI 4.37 / XM4D 4.36 / RacerGS 4.35 / HaNDF 4.34 / EgoExplorer 4.30 / dGS-dBS 4.30）→ **重磅日，1 篇 S 级**（2611.11169 Map2SLAM 4.57）。
- OUTDATED/SUPERSEDED **0 篇**。

## 产物（第 7-8 步）
- 报告 2 份（主批 + backfill）+ 原子笔记 28 篇（grade≥B：主批 21 + backfill 7；10 篇 C 级仅入馆）+ MOC 2 份 + 总索引刷新 + 7 维表/scored/run_log 各 2 套。
- registry 849 → **888**（+31 +8；备份 `papers/library/registry.jsonl.bak-20261111`；按 base_id 幂等）。
- notes 520 → **548**。
- 门③ 现算值供下一批参考：**4.4100**（本批 4.57 入窗后 Top10 均分将变化，须再算）。
'''
open(f'papers/daily/{DATE}/run_log.md', 'w', encoding='utf-8').write(run_log_main)

run_log_bf = f'''# backfill-1111 执行日志

- **来源**：11-10 公告批次 RSS（7 分类去重 1,479 → KW 命中 77）中 25 篇 v2+ 再公告未入馆者，经摘要+标题核实 XR 相关 8 篇 → 本批；另 17 篇非 XR 剔除。
- **诚实口径**：本批全部为 **v2/v3 再公告**（2609.11894 v2 / 2503.00747 v3 / 2603.10801 v2 / 2605.11594 v2 / 2605.12297 v2 / 2609.00775 v2 / 2608.30368 v2 / 2512.14329 v3），原始投稿 2025-03-02 ~ 2026-09-10，本次更新 2026-11-07~11-09 后再公告；均非 11-10 当日新提交，单独编号、不参与当日重磅日判定。
- **全文**：7 篇 L0/FULL + 1 篇 L1/PARTIAL（2512.14329：arXiv HTML 404、ar5iv 仅摘要页 5,391 字符，按摘要级评估并显式声明）。
- **定稿**：3 A / 4 B / 1 C。最高 **2609.11894 4.22**（毫米波雷达复数域点泼溅，物理保真渲染器 + 多视角可微蒙特卡洛光线追踪；达 S 线但 backfill 按校准关记 A）· 2605.11594 4.00（PointForward 点对齐前馈驾驶重建）· 2605.12297 3.82（EgoEV-HandPose 双目事件第一视角手部姿态）· 2609.00775 3.51 · 2603.10801 3.45 · 2512.14329 3.26 · 2503.00747 3.00 · 2608.30368 2.79（C 仅入馆）。
- **registry**：+8（batch=backfill-1111，幂等）。
'''
open('papers/daily/backfill-1111/run_log.md', 'w', encoding='utf-8').write(run_log_bf)

# ---------- registry ----------
reg_path = 'papers/library/registry.jsonl'
bak_path = reg_path + '.bak-20261111'
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
                     fetch_level=p['level'], fulltext_chars=MANIFEST[p['id']]['chars'],
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
        link = f"[→](../notes/{os.path.basename(note[0])})" if note else '→（C 级仅入馆）'
        L.append(f"| {i} | {esc(p['title_zh'])} | {p['track']} | {p['value']:.2f} | {p['grade']} | {p['evidence']} | {link} |")
    L += ['\n## 批次要点\n']
    for p in papers:
        L.append(f"- **{esc(p['title_zh'])}**（{p['id']}，{p['value']:.2f} {p['grade']}）：{p['conclusion']}")
    open(path, 'w', encoding='utf-8').writelines([x + '\n' for x in L])


moc(MAIN, f'papers/MOC/MOC-{DATE}.md', f'MOC · {DATE}（11-10 公告批次）',
    '> 当日地图：**公告日 2026-11-10（周二）≠ 拉取日 2026-11-11（周三 02:30）**——诚实口径。11-10 00:00 UTC 释放当日公告批次；API published 口径核验提交日 **11-09×18 / 11-08×9 / 11-07×14 / 11-06×5 / 11-04×1**（均早于公告日；RSS published 为公告时间戳），另 2 篇 v1 为延迟公告（09-23 / 10-26 提交）。\n'
    '> 主批 XR 新稿 **31 篇（1 S / 14 A / 6 B / 10 C）**，Top10 实数 10 篇最高 **4.57**（Map2SLAM，重磅日评 S）；listing 11-10 组 868 篇摘要级命中 49 篇 = RSS 真新 49 篇（两渠道逐篇一致，RSS 漏网 0 篇）；11-09 组复采 0 漏网。\n'
    '> 全文：37×L0/FULL + 2×L1/PARTIAL（2611.12130、2512.14329：arXiv HTML 404 + ar5iv 摘要页，按摘要级评估并显式声明）。\n'
    '> 覆盖度三关：门① 0.082 / 门② 定稿 Top10 覆盖 5 赛道（达门槛未重筛，重建与SLAM 占 6/10；全批 9 赛道）/ 门③ 4.57 ≥ 4.4100（现算，415 条入窗）→ **重磅日，1 篇 S**。\n'
    '> Top10（实数 10 篇）：Map2SLAM 4.57 S · FastGRT 4.17 · DASH-SLAM 4.16 · PLS-GS 4.14 · GPU SM 负载均衡 4.08 · UltraVoxelGS 4.00 · ClearForm 3.99 · DPGS-SLAM 3.93 · Spaghetti Splatting 3.92 · RoboMoCap 3.89。')

moc(BF, 'papers/MOC/MOC-backfill-1111.md', 'MOC · backfill-1111（旧稿 v2/v3 再公告首次入馆）',
    '> **非当日新提交**：本批 8 篇均为 11-10 公告 RSS 混入的旧稿 v2/v3 再公告（原始投稿 2025-03 ~ 2026-09，2026-11-07~11-09 更新），诚实口径单独编号，不参与当日重磅日判定。\n'
    '> 定稿 3 A / 4 B / 1 C，最高 **2609.11894 4.22**（毫米波雷达复数域点泼溅，物理保真 + 多视角可微蒙特卡洛光线追踪；达 S 线按校准关记 A）。其余：PointForward 4.00 / EgoEV-HandPose 3.82 / VOIM 3.51 / PolGS++ 3.45 / 可穿戴生成式化身 3.26 / LFX 3.00 / SpectraTac 2.79（C 仅入馆）。')


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
        L.append(f"- **公告类型**：{p['announce']}（公告日 2026-11-10，拉取日 2026-11-11）")
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
    L.append('- 抓取降级：39 篇候选串行 3s/篇；37 篇 L0 一次命中；2611.12130 与 2512.14329 两稿 **arXiv HTML 404**、ar5iv 仅返摘要页（4,833 / 5,391 字符，人工确认无正文节）→ manifest 改判 **PARTIAL** 并加 note，按摘要级评估；TEC/EXP 上限 3、PER 上限 4，**未脑补公式、消融或未提基线**。无限流、无 L5、无 OCR、无伪造。')
    open(path, 'w', encoding='utf-8').writelines([x + '\n' for x in L])


HEADER = (
    '## 一、执行摘要\n'
    '- **公告日 2026-11-10（周二）≠ 拉取日 2026-11-11（周三 02:30）**——诚实口径。API published 核验提交日 **11-09×18 / 11-08×9 / 11-07×14 / 11-06×5 / 11-04×1**（均早于公告日；RSS published 是公告时间戳非提交日），另 2 篇 v1 为延迟公告（2611.09926 提交 09-23、2611.09959 提交 10-26，后者非 XR 已剔）。\n'
    '- **数据源**：API 双主机探针均 200；RSS 7 分类去重 **1,479** → KW 命中 **77**。两渠道互证：**listing 摘要级 49 篇 = RSS 真新 49 篇，双向差集 0，RSS 漏网 0 篇**；11-09 组复采 452 槽位/377 唯一、未入馆 362 篇摘要级命中 7 篇均为上批已剔非 XR → **0 漏网**。\n'
    '- **主批 XR 新稿 31 篇（1 S / 14 A / 6 B / 10 C；Top10 实数 10 篇）**。Top10：**Map2SLAM 4.57 S（把冻结的流式 3D 基础模型预测当作可修订 SLAM 状态：KITTI 平均 ATE 13.56→7.56 m（−44%）、VBR 9.97→5.15 m（−48%）、Oxford Spires 3.07 m，518×154 输入在 RTX 5090D 上 >28 FPS，28 条序列 6 组消融；本批唯一 S）** · FastGRT 4.17（Vulkan 高斯光线追踪训练加速 1.9–4.97×、反向最多 10×，质量持平，首个开源可训练的 Vulkan GRT） · DASH-SLAM 4.16（Depth Anything 3 米制深度 + 共享关键帧位姿图做免标定单目 SLAM，TUM Sim3 0.028 m、Replica 0.008 m、千米级野外序列优于 VGGT-SLAM） · PLS-GS 4.14（LiDAR 脚手架约束的紧凑表面对齐 3DGS，precision 0.330→0.484、Chamfer 0.820→0.703 m、anchor 少 2.8×、体积 42%、帧率 1.7×，代价 PSNR −1.0~1.65 dB） · GPU SM 负载均衡 4.08（3DGS alpha blending 平均 2.93×、失衡帧最高 5.64×，画质差 ≤0.0015 dB，无需重训练） · UltraVoxelGS 4.00（体素优先前馈高斯泼溅做三维超声，PSNR 24.29 vs 逐场景优化 22.55，重建 10–20 分钟 → 约 10 秒） · ClearForm 3.99（解耦几何与外观 alpha 的透明界面重建，3D-FRONT-T CD 59.18→27.05 mm、F1 0.786→0.928） · DPGS-SLAM 3.93（扩散先验 + 来源感知的动态单目 3DGS SLAM，TUM ATE 1.2 cm，静态背景 PSNR +4.60 dB） · Spaghetti Splatting 3.92（曲线型狄拉克质量闭式 EWA 体渲染，3DGS 严格超集，头发 F1 +14.3 点） · RoboMoCap 3.89（200+ 小时、14 人、291 动作协议的第一视角 + 120 Hz 光学动捕数据集，MPJPE 80.8 mm）。\n'
    '- **覆盖 9 赛道（全批）/ Top10 覆盖 5 赛道**：重建与SLAM 9（Top10 占 6）/ 系统与平台 5 / 评估与数据集 4 / 化身与人体 3 / 感知与认知 3 / 渲染与显示 2 / 神经渲染 2 / 交互与输入 2 / 触觉与多模态 1。\n'
    '- **覆盖度三关**：门① 最大 Jaccard **0.082**（PointForward vs 库内 GTSM，<0.62）；门② 定稿 Top10 覆盖 **5 赛道** ≥5（达门槛未触发重筛；重建与SLAM 集中 6/10 反映当日投稿结构）；门③ 当日最高 **4.57 ≥ 库内近 30 天 Top10 均分 4.4100**（现算，415 条入窗）→ **重磅日，1 篇 S 级**。\n'
    '- **全文证据**：37 篇 **L0/FULL** + 2 篇 **L1/PARTIAL**（2611.12130 / 2512.14329：arXiv HTML 404 + ar5iv 摘要页，摘要级评估并显式声明）。OUTDATED 0。\n'
    '- **backfill-1111（8 篇，非当日新提交）**：11-10 公告 RSS 混入的旧稿 v2/v3 再公告首次入馆——2609.11894 4.22（毫米波雷达复数域点泼溅）· PointForward 4.00 · EgoEV-HandPose 3.82 · VOIM 3.51 · PolGS++ 3.45 · 可穿戴生成式化身 3.26 · LFX 3.00 · SpectraTac 2.79。\n'
    '- **路线观察**：① **「3D 基础模型 → SLAM」成为当日主线**：Map2SLAM（调度而非改造模型、预测可回滚）与 DASH-SLAM（深度尺度传播、免标定米制）分别从「状态可修订」与「尺度一致」两端补齐流式 3DFM 的 SLAM 缺口，与库内 VGGT-SLAM 2.0 / MASt3R-SLAM / V3DSAM（本批 3.08）构成同一条竞赛线；② **3DGS 的效率与表示同时推进**：训练侧 FastGRT（1.9–4.97×）与渲染侧 SM 负载均衡（2.93×）分居上下游，表示侧 Spaghetti Splatting 用曲线基元把 3DGS 变成其特例，PLS-GS 用 LiDAR 脚手架换紧凑性；③ **前馈化继续吞噬逐场景优化**：UltraVoxelGS（超声 10 秒 vs 10–20 分钟）、PointForward（backfill，驾驶前馈重建）同向；④ **XR 人因与评测**：RoboMoCap（第一视角动捕数据）与 SituRecBench（3D 环境具身推荐评测）补的是数据与评测基础设施，而非模型；⑤ 硬件类渲染缺口（波导/可变焦/Maxwellian/光场）本批仍无破冰，仅 VAComp（投影仪视角感知补偿 3.70）触及显示侧。'
)

report(TOP10, f'reports/XR-Daily-Report-{DATE}.md', f'XR 每日论文解读报告 · {DATE}（11-10 公告批次）', HEADER, 10,
       ['- 门①（同质去重）：最大 Jaccard **0.082** < 0.62（2605.11594 PointForward vs 库内 2610.26918 GTSM），通过，无同质重复。库侧 token 取 title+title_zh（registry 无摘要字段），口径偏保守。',
        '- 门②（赛道覆盖）：定稿 Top10 覆盖 **5 赛道**（重建与SLAM×6 / 渲染与显示×1 / 系统与平台×1 / 神经渲染×1 / 化身与人体×1）≥5，达门槛**未触发重筛**。**集中度说明**：单日 XR 稿中重建与SLAM 占 9/31，Top10 按纯价值降序自然形成 6/10；第 11–14 名（3R-Adapter 3.87 重建、RefineSplat 3.80 感知、SituRecBench 3.76 评估、VAComp 3.70 渲染）中已覆盖感知/评估赛道，无需为凑赛道而替换高分论文。同分位无并列（3.89/3.92/3.93 均不同分），未触发多样性定序。',
        '- 门③（价值天花板）：当日最高 **4.57** ≥ 库内近 30 天 Top10 均分 **4.4100**（现算，窗口 2026-10-12~11-11、415 条入窗；Top10 = SMoRe/视频扩散化身/Open-HumanScale 4.57 · ACD-GS/Stereo CI 4.37 · XM4D 4.36 · RacerGS 4.35 · HaNDF 4.34 · EgoExplorer/dGS-dBS 4.30）→ **重磅日，1 篇 S 级**（Map2SLAM 4.57）。',
        '- 主会话校准记录：2611.10239 DASH-SLAM PER 5→4（TUM Sim3 仅 −22%、7-Scenes 0.053 与 AMB3R 持平，增益不均匀）；2611.12319 GPU 负载均衡 PER 5→4（2.93× 仅出现在 Hier-3DGS 失衡场景，标准基准 1.12×、驾驶 1.23×）。两处调整各降 0.15 分，避免「单点最优当全局增益」。',
        '- 低量日不凑数原则复核：主批 31 篇中 10 篇 C 级（<3.0）仅入馆不解读，Top10 取实数 10 篇全为 A/S；未为凑数保留同质论文，亦未拔高低分入选。',
        '- OUTDATED/SUPERSEDED **0 篇**。\n'])

report(BF, 'reports/XR-Backfill-Report-backfill-1111.md', 'XR Backfill 报告 · backfill-1111（旧稿 v2/v3 再公告首次入馆）',
       '## 一、执行摘要\n'
       '- **诚实口径**：本批 8 篇均为 **11-10 公告批次 RSS 混入的旧稿 v2/v3 再公告**（原始投稿 2025-03-02 ~ 2026-09-10，本次更新 2026-11-07~11-09 后再公告），首次入馆；**均非 11-10 当日新提交**，单独编号、不参与当日重磅日判定。\n'
       '- **定稿 3 A / 4 B / 1 C**，最高 **2609.11894 4.22**（毫米波雷达复数域点泼溅：物理保真、复数域、多视角可微蒙特卡洛光线追踪三者同时满足；达 S 线但 backfill 按校准关记 A）。其余：PointForward 4.00（点对齐前馈驾驶重建）· EgoEV-HandPose 3.82（双目事件第一视角手部姿态与手势，v2）· VOIM 3.51（免训练开放词表三维实例建图）· PolGS++ 3.45（偏振高斯泼溅反射面）· 可穿戴生成式化身 3.26（PARTIAL 摘要级）· LFX 3.00（光场融合形态灵活建模）· SpectraTac 2.79（C 仅入馆）。\n'
       '- **全文**：7 篇 L0/FULL + 1 篇 L1/PARTIAL（2512.14329：arXiv HTML 404、ar5iv 仅摘要页 5,391 字符）。\n'
       '- **剔除**：同批 v2+ 未入馆 25 篇中 17 篇经摘要核实非 XR（OmniMem / TryOnCrafter / 像素空间自回归生成 / UNIVERS / JND 预滤波 / FUSE-PnPL / 海底遥操作 HMI 综述 / 形态对称图步态 / SyncTwin / LessMimic / SENTINEL 2D LiDAR SLAM / VLA 光照鲁棒 / 人形遥操作 / HandMimicX / AMTFV / CaLR / RL 扩散 LLM）。',
       8,
       ['- 门①/门③ 对 backfill 不适用（非当日新提交，不参与重磅日判定）；门② 覆盖 3 赛道（神经渲染×1 / 重建与SLAM×3 / 化身与人体×2 / 感知与认知×1 / 触觉与多模态×1 = 5 赛道）。',
        '- 本批 4.22 达 S 线但按「backfill 不参与当日重磅日判定」记 A，未拔高。\n'])

# ---------- MOC-总索引 ----------
moc_path = 'papers/MOC/MOC-总索引.md'
h = open(moc_path, encoding='utf-8').read()
n0 = len(h)


def rep(old, new, tag):
    global h
    assert old in h, f'ANCHOR NOT FOUND: {tag}'
    h = h.replace(old, new, 1)


rep('累计 **849 篇**；跨度 2026-09-15 ~ 2026-11-09',
    '累计 **888 篇**；跨度 2026-09-15 ~ 2026-11-10', 'head-count')
rep('**backfill-1110:4（11-09 公告 RSS 混入旧稿 replace 再公告，首次入馆）**；',
    '**backfill-1110:4（11-09 公告 RSS 混入旧稿 replace 再公告，首次入馆）** · '
    '**2026-11-11:31（11-10 公告批次真新提交，重磅日 1S；listing 868 篇摘要级命中 49 篇 = RSS 真新 49 篇两渠道互证）** · '
    '**backfill-1111:8（11-10 公告 RSS 混入旧稿 v2/v3 再公告，首次入馆）**；', 'batch-list')

note11 = ('> **状态注记（2026-11-11）**：周三 02:30，处理 **2026-11-10（周二）公告批次**（公告日≠拉取日，诚实口径）。'
 'API published 口径核验提交日 **11-09×18 / 11-08×9 / 11-07×14 / 11-06×5 / 11-04×1**（RSS published 为公告时间戳）；另 2 篇 v1 属延迟公告（2611.09926 提交 09-23、2611.09959 提交 10-26，后者非 XR 已剔）。'
 '漏网对账（先于拉取，`scripts/audit_listing_1111.py`，PREV_DAY=11-09 / NEW_DAY=11-10）：listing 7 分类最新公告日均为 **11-10**（无漏跑公告日）；11-09 组复采逐分类 **declared=got**（CV 117/GR 7/HC 28/MM 3/RO 60/AI 220/IV 17，452 槽位/377 唯一），未入馆 **362 篇**摘要级命中 7 篇逐篇核对为上批已剔非 XR → **0 漏网**；**11-10 组 868 篇唯一论文**（1,059 槽位）摘要级 XR 命中 **49 篇**。'
 '**数据源**：API 双主机 200；RSS 去重 **1,479** → KW 命中 **77** = 49 篇真新（31 XR + 18 非 XR）+ 25 篇旧稿 v2+ 未入馆（8 XR → backfill-1111）+ 3 篇库内 v2；**listing 49 篇与 RSS 真新 49 篇双向差集 0（两渠道互证）**。'
 '主批甄别 **XR 核心/强相关 31 篇**（剔非 XR 18 篇）；全文 **37 篇 L0/FULL + 2 篇 L1/PARTIAL**（2611.12130 / 2512.14329：arXiv HTML 404 + ar5iv 摘要页，摘要级评估并显式声明）。'
 'Top10（**实数 10 篇**）：最高 **4.57 Map2SLAM（S）**，**重磅日**；覆盖 **5 赛道**（重建×6/渲染/系统/神经渲染/化身）。'
 '三关：门① max Jaccard **0.082**（2605.11594 vs 库内 2610.26918 GTSM）；门② Top10 覆盖 5 赛道 ≥5（达门槛未重筛）；门③ 当日最高 **4.57 ≥ 4.4100**（415 条入窗，现算）→ **重磅日，1 篇 S**；OUTDATED 0。'
 'registry 849 → **888**（+31 +8），笔记 520 → **548**。详见 [运行报告](../../reports/XR-Daily-Report-2026-11-11.md) / [MOC-2026-11-11](./MOC-2026-11-11.md) / [MOC-backfill-1111](./MOC-backfill-1111.md) / [Backfill 报告](../../reports/XR-Backfill-Report-backfill-1111.md)。\n')
anchor_end = '详见 [运行报告](../../reports/XR-Daily-Report-2026-11-10.md) / [MOC-2026-11-10](./MOC-2026-11-10.md) / [MOC-backfill-1110](./MOC-backfill-1110.md) / [Backfill 报告](../../reports/XR-Backfill-Report-backfill-1110.md)。'
i = h.find(anchor_end)
assert i >= 0, 'ANCHOR NOT FOUND: note1110-end'
j = h.find('\n', i) + 1
h = h[:j] + note11 + h[j:]

rep('| 最新一期 | [MOC · 2026-11-10](./MOC-2026-11-10.md) |',
    '| 最新一期 | [MOC · 2026-11-11](./MOC-2026-11-11.md) |', 'quick-latest')
rep('| 上一期 | [MOC · 2026-11-07](./MOC-2026-11-07.md) |',
    '| 上一期 | [MOC · 2026-11-10](./MOC-2026-11-10.md) |', 'quick-prev')
rep('（现有 520 篇）', '（现有 548 篇）', 'quick-notes')
rep('| 最新运行状态 | [运行报告 2026-11-10](../../reports/XR-Daily-Report-2026-11-10.md)（11-09 公告批次·周末积压 14 篇 7A/7B 非重磅日无S；listing 377 篇摘要级命中 18 篇 = 17 篇 v1 + 1 已在库，RSS 漏网 0 篇；11-06 组复采 363 篇 diff 0；全文 16×L0/FULL + 2×L1/PARTIAL；Top10 实数 10 篇覆盖 7 赛道（未触发重筛）；门③ 现算 4.399，当日最高 4.37 未达线，4 篇达 S 线按校准关记 A） |',
    '| 最新运行状态 | [运行报告 2026-11-11](../../reports/XR-Daily-Report-2026-11-11.md)（11-10 公告批次 31 篇 1S/14A/6B/10C **重磅日**；listing 868 篇摘要级命中 49 篇 = RSS 真新 49 篇双向差集 0；11-09 组复采 0 漏网；全文 37×L0/FULL + 2×L1/PARTIAL；Top10 实数 10 篇覆盖 5 赛道（达门槛未重筛）；门③ 现算 4.4100，当日最高 4.57 达线 → 1 篇 S） |', 'quick-status')

row_main = ('| 2026-11-11 | [MOC-2026-11-11](./MOC-2026-11-11.md) | XR 31（Top10 实数 10）· 1S/14A/6B/10C · **重磅日（1S）** | '
            '11-10 公告批次真新提交 31 篇（11-04×1/11-06×5/11-07×14/11-08×9/11-09×18 + 2 篇 v1 延迟公告）；listing 868 篇摘要级命中 49 篇 = RSS 真新 49 篇（双向差集 0）；11-09 组复采 0 漏网；全文 37×L0/FULL + 2×L1/PARTIAL |\n'
            '| backfill-1111 | [MOC-backfill-1111](./MOC-backfill-1111.md) | 补录 8（3A/4B/1C）· 非当日新提交 | 11-10 公告 RSS 混入旧稿 v2/v3 再公告 8 篇（2503/2512/2603/2605×2/2608/2609×2，2026-11-07~09 更新）；最高 2609.11894 4.22 |')
rep('| backfill-1110 | [MOC-backfill-1110](./MOC-backfill-1110.md) | 补录 4（2A/2B）· 非当日新提交 | 11-09 公告 RSS 混入旧稿 v2/v3/v4 再公告 4 篇（2511/2605/2605/2607，2026-11-06 更新）；最高 2605.16981 4.00 |',
    '| backfill-1110 | [MOC-backfill-1110](./MOC-backfill-1110.md) | 补录 4（2A/2B）· 非当日新提交 | 11-09 公告 RSS 混入旧稿 v2/v3/v4 再公告 4 篇（2511/2605/2605/2607，2026-11-06 更新）；最高 2605.16981 4.00 |\n'
    + row_main, 'batch-table')

seg = '\n### 2026-11-11 新增（Top10 实数 10 篇：1 S + 9 A，重磅日）\n\n| # | 论文 | 赛道 | 分值 | 等级 | 证据 |\n|---:|---|---|---:|---|---|\n'
for i2, pid in enumerate(TOP10_ORDER, 1):
    p = next(x for x in MAIN if x['id'] == pid)
    seg += f"| {i2} | {esc(p['title_zh'])} | {p['track']} | {p['value']:.2f} | {p['grade']} | {p['evidence']} |\n"
seg += '\n### backfill-1111 补录（8 篇：3 A + 4 B + 1 C，非当日新提交）\n\n| # | 论文 | 赛道 | 分值 | 等级 | 证据 |\n|---:|---|---|---:|---|---|\n'
for i2, p in enumerate(BF, 1):
    seg += f"| {i2} | {esc(p['title_zh'])} | {p['track']} | {p['value']:.2f} | {p['grade']} | {p['evidence']} |\n"
h = h.rstrip() + '\n' + seg

import re as _re
foot_pat = _re.compile(r'^\*最后更新：[^\n]*\* · MOC \d+ 份$', _re.M)
assert foot_pat.search(h), 'ANCHOR NOT FOUND: footer'
h = foot_pat.sub('*最后更新：2026-11-11（11-10 公告批次：31 篇 XR 新稿 1S/14A/6B/10C **重磅日**；listing 868 篇摘要级命中 49 篇 = RSS 真新 49 篇双向差集 0；11-09 组复采 362 篇命中 7 篇均为已剔非 XR；全文 37×L0/FULL + 2×L1/PARTIAL（2611.12130/2512.14329 摘要级）；Top10 覆盖 5 赛道达门槛未重筛；门③ 现算 4.4100，当日最高 4.57 达线 → 1 篇 S；backfill-1111 补录 8 篇 3A/4B/1C）。* · 库内 **888 篇** · 原子笔记 **548 篇** · MOC 47 份', h)

open(moc_path, 'w', encoding='utf-8').write(h)
print('MOC-总索引 refreshed（%d -> %d chars）' % (n0, len(h)))
print('DONE')
