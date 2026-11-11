# -*- coding: utf-8 -*-
"""2026-11-12 产物生成：主批（11-11 公告批次 15 篇）+ backfill-1112（4 篇旧稿 v2/v3 再公告）。

诚实口径：公告日 2026-11-11（周三 00:00 UTC 释放）≠ 拉取日 2026-11-12（周四 02:30）。
API published 核验：主批 11-10×12 / 11-09×2 / 10-22×1（2611.12912 属三周延迟公告）；
backfill 原始提交 2025-03-02 / 2025-05-27 / 2026-05-21 / 2026-08-05，v2/v3 于 2026-11-09~11-10 更新。
消费 data/scored_1112.json；registry 幂等追加（先备份，in_top10 按定稿显式设置）。
"""
import glob
import json
import os
import re
import shutil

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
os.chdir(ROOT)
D = json.load(open('data/scored_1112.json', encoding='utf-8'))
MAIN = D['main']
BF = D['backfill']
TOP10_IDS = set(D['top10_ids'])
TOP10_ORDER = list(D['top10_ids'])
DATE, ANN = '2026-11-12', '2026-11-11'
GATE3 = D['gate3_mean']
MANIFEST = json.load(open('data/fulltext/_manifest.json', encoding='utf-8'))
for p in MAIN + BF:
    p['level'] = MANIFEST[p['id']]['level']
    p['evidence'] = MANIFEST[p['id']]['evidence']
    p['announce'] = 'replace' if p['batch'].startswith('backfill') else 'new'
TOP10 = [p for pid in TOP10_ORDER for p in MAIN if p['id'] == pid]
assert [p['id'] for p in TOP10] == TOP10_ORDER
assert len(MAIN) == 15 and len(BF) == 4, (len(MAIN), len(BF))


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
os.makedirs('papers/daily/backfill-1112', exist_ok=True)


def seven_table(papers, path, title, intro):
    lines = [f'# {title}\n', intro + '\n', TBL_HEAD]
    for p in papers:
        lines.append(dim_row(p, p['id'] in TOP10_IDS) + '\n')
    open(path, 'w', encoding='utf-8').writelines(lines)


INTRO_MAIN = (
    '批次：2026-11-12（**2026-11-11（周三）公告批次**——公告日 11-11 ≠ 拉取日 11-12（周四 02:30），诚实口径）。\n'
    '候选池 15 篇（listing 摘要级 28 篇命中，剔非 XR 13 篇）。漏网对账（先于拉取，`scripts/audit_listing_1112.py`，show=500 单页×7 分类 + 目标组补页，PREV_DAY=11-10 / NEW_DAY=11-11）：7 分类最新公告日均为 **2026-11-11**（无漏跑公告日）；**11-10 组复采逐分类 declared=got**（CV 317/GR 14/HC 63/MM 7/RO 165/AI 480/IV 13 = 1,059 槽位，cs.AI 补采 skip=500 合并 228 条），未入馆 **837 篇**（= 上批 868 篇唯一 − 已入馆 31 篇）摘要级命中 **18 篇**，**逐篇 id 与上批（11-11 运行）显式剔除的 18 篇非 XR 完全一致** → **0 漏网、无 backfill 触发**。\n'
    '**11-11 组 436 篇唯一论文**（CV 149/GR 6/HC 34/MM 14/RO 69/AI 248/IV 12 = 532 槽位，全部未入馆）→ `scripts/triage_1112.py` 摘要级 XR 命中 **28 篇**（meta fetched 1,273/1,273，首次 429 丢 200 篇已由 `fill_meta_1112.py` 补齐）。\n'
    '数据源：API 双主机探针均 200（各 2,938 bytes / 0.3–0.6s）；RSS 7 分类去重 **669** → KW 命中 **37**（cs.CV 239 / cs.AI 381 / cs.RO 111 / cs.HC 46 / eess.IV 17 / cs.MM 16 / cs.GR 9）。\n'
    '甄别：RSS 37 = **28 篇 11-11 公告组真新提交**（15 XR 主批 + 13 非 XR）+ **7 篇旧稿 v2/v3 再公告未入馆**（4 篇 XR → backfill-1112 + 3 篇非 XR）+ **2 篇库内 v2**（2609.30468 SplatLab / 2611.06817 Open-HumanWAM）。**listing 摘要级 28 篇与 RSS 真新 28 篇集合同一（双向差集 0，两渠道互证，RSS 漏网 0 篇）**。\n'
    '提交日核验（API published）：主批 **11-10×12 / 11-09×2 / 10-22×1**（2611.12912 属三周延迟公告）；**RSS published 字段是公告时间戳（11-11），不可当提交日**。\n'
    '全文：19 篇候选（15 + 4）串行 3s/篇：**18 篇 L0/FULL**（26,116–114,240 字符）+ **1 篇 L1/PARTIAL**（2611.13296 4,350 字符：arXiv HTML 404 + ar5iv 仅返 arXiv 摘要页、无 Introduction/Method 节，人工复核后改判 PARTIAL，按摘要级评估并显式声明）。\n'
    '覆盖度三关：门① 最大 Jaccard **0.082**（2611.13280 vs 库内 2609.22849 LINGO，<0.62 通过）；门② 定稿 Top10 覆盖 **7 赛道**（神经渲染×3 / 重建与SLAM×2 / 内容生成·系统与平台·化身与人体·感知与认知·空间计算与UI 各×1；全批 9 赛道）；门③ 当日最高 **4.08 < 库内近 30 天 Top10 均分 4.4370**（窗口 2026-10-13~11-12、442 条入窗、现算）→ **非重磅日，无 S 级**。OUTDATED 0。'
)
seven_table(MAIN, f'papers/daily/{DATE}/7dim-table.md', f'{DATE} 全量 7 维度对比表（参考）', INTRO_MAIN)

INTRO_BF = (
    '批次：backfill-1112（**11-11 公告批次 RSS 混入的旧稿 v2/v3 再公告**，首次入馆；原始投稿 2025-03-02 ~ 2026-08-05，v2/v3 于 2026-11-09~11-10 更新后再公告）。\n'
    '均非 11-11 当日新提交，诚实口径单独编号；不参与当日「重磅日」判定。\n'
    '候选 4 篇：2608.04971（投影–HMD 跨现实转场，v2，2026-08-05 首发）/ 2605.22715（AnyMo 可穿戴动捕设置无关建模，v3，2026-05-21）/ 2505.20858（TFD-SfM 无轨迹稠密 SfM，v3，2025-05-27）/ 2503.00868（生成式 3DGS 流体资产提取，v3，2025-03-02）。\n'
    '同批另 3 篇旧稿经摘要核实非 XR 剔除（2605.30770 SSR 人形越野 / 2611.08100 轮式巡视器 ROS2 导航栈 / 2611.01491 mmWave 无线电 SLAM）。\n'
    '全文：4 篇全部 L0/FULL（71,312–114,240 字符）。本批最高 4.15（TFD-SfM）未达 S 线，且 backfill 不参与重磅日判定。'
)
seven_table(BF, 'papers/daily/backfill-1112/7dim-table.md', 'backfill-1112 全量 7 维度对比表（参考）', INTRO_BF)


# ---------- scored.md ----------
def scored_md(papers, path, title, extra):
    L = [f'# {title}\n', extra + '\n', '| 排名 | arXiv | 标题 | 赛道 | 总分 | 等级 | 证据 | 公告类型 |',
         '|---|---|---|---|---|---|---|---|']
    for i, p in enumerate(papers, 1):
        L.append(f"| {i} | {p['id']} | {esc(p['title_zh'])} | {p['track']} | {p['value']:.2f} | {p['grade']} | {p['evidence']} | {p['announce']} |")
    open(path, 'w', encoding='utf-8').writelines([x + '\n' for x in L])


scored_md(MAIN, f'papers/daily/{DATE}/scored.md', f'{DATE} 评分明细',
          '评分口径：7 维加权 IMP0.20·NOV0.20·TEC0.15·EXP0.15·PER0.15·TRL0.08·REP0.07；分档 S≥4.2 / A3.6–4.2 / B3.0–3.6 / C<3.0。全部基于全文证据定稿（14 篇 L0/FULL + 1 篇 L1/PARTIAL：2611.13296 按摘要级评估）。\n'
          '覆盖度三关：门① 最大 Jaccard 0.082 < 0.62（通过，非同质；库侧 token 取 title+title_zh）；门② 定稿 Top10 覆盖 7 赛道 ≥5（通过，无需重筛；全批 9 赛道）；门③ 当日最高 4.08 < 库内近 30 天 Top10 均分 4.4370（现算，442 条入窗）→ **非重磅日，无 S 级**（全批无 ≥4.2 达线论文，校准关未触发降级改写）。\n'
          '主会话校准：子代理 19 篇评分逐条对照 scores_why 与正文数字复核，仅确认 2611.13628 维持 TEC 3（DTU 0.51 mm 未超 GSPrior 0.50 mm，引理 2 为标量近似），未发现需改判项。\n'
          'OUTDATED/SUPERSEDED 0 篇。等级分布：6 A / 6 B / 3 C（无 S）。')

scored_md(BF, 'papers/daily/backfill-1112/scored.md', 'backfill-1112 评分明细',
          '评分口径同上；本批为旧稿 v2/v3 再公告首次入馆，均非当日新提交。\n'
          '等级分布：2 A / 2 B；最高 2505.20858 TFD-SfM 4.15（未达 4.2 S 线）。门③ 对 backfill 不适用。')

# ---------- run_log ----------
run_log_main = f'''# {DATE} 执行日志

## 数据源与对账（第 1-3 步）
- **漏网对账（先于拉取）**：`scripts/audit_listing_1112.py`（PREV_DAY=2026-11-10 上批公告日 / NEW_DAY=2026-11-11；show=500 单页×7 分类，目标组 declared≠got 自动补采后续页）→ 7 分类最新公告日均为 **2026-11-11**（无漏跑公告日、无跳空）。
- **上批组复核**：11-10 组逐分类 **declared=got**（CV 317/GR 14/HC 63/MM 7/RO 165/AI 480/IV 13 = 1,059 槽位；cs.AI 补采 skip=500 合并 228 条 → 480/480）。未入馆 **837 篇** 摘要级 XR 命中 **18 篇**，逐篇 id 与上批（11-11 运行）显式剔除的 18 篇非 XR **完全一致**（2611.09959/10062/10137/10236/10451/10490/10858/10877/11098/11452/11555/11697/11809/12017/12261/12526/12739/12870）→ **0 漏网、无 backfill-1112 之外的补录**。
- **新公告组**：11-11 组 **436 篇唯一论文**（532 槽位）全部未入馆 → 摘要级 XR 命中 **28 篇**（data/missed_new_1112_xr.json）。
- **数据源**：API 双主机探针均 **200**（各 2,938 bytes / 0.3–0.6s）；RSS 7 分类 HTTP 200（cs.CV 239 / cs.AI 381 / cs.RO 111 / cs.HC 46 / eess.IV 17 / cs.MM 16 / cs.GR 9）→ 去重 **669** → KW 命中 **37**（WROTE=37）。
- **提交日核验**（API published）：主批 11-10×12 / 11-09×2 / **10-22×1**（2611.12912 大范围空间锚点，提交 2026-10-22、延迟约三周公告）。**RSS published 是公告时间戳（11-11），不可当提交日**。
- **429 处理**：`scripts/triage_1112.py` 首轮 id_list 批量查询触发 429，13 批中 2 批（200 篇）失败 → `scripts/fill_meta_1112.py` 以 50 id/批 + 12s 间隔补齐，最终 meta 1,273/1,273，候选集合重算后仍为 28 篇（与首次一致，无漏判）。

## 甄别（第 3 步）
- 主批 XR 核心/强相关 **15 篇**入评分池；剔非 XR **13 篇**（逐篇理由见报告 §5.2）：自动驾驶 LiDAR 仿真（2611.12932）/ 2D LiDAR 迷宫导航 ROS2 栈（2611.12949）/ 开放词表检测（2611.12976）/ VLA token 剪枝（2611.13030）/ WiFi-IMU 室内定位（2611.13057）/ MCDA 参数诱导（2611.13062）/ 康复机器人触觉 dyad（2611.13307）/ Ego2Robot 综述（2611.13610）/ 机器人策略自视角预训练（2611.13685）/ 2D 高斯图像编码（2611.13784）/ 少步流式视频生成（2611.14033）/ AUV 六自由度轨迹跟踪（2611.14373）/ 身体感知多模态数据集（2611.14093）。
- 旧稿 v2/v3 未入馆 **7 篇**：**4 篇 XR → backfill-1112**（2608.04971 / 2605.22715 / 2505.20858 / 2503.00868）；3 篇非 XR（2605.30770 SSB 人形越野 / 2611.08100 巡视器导航栈 / 2611.01491 mmWave 无线电 SLAM）。
- 库内 v2 再公告 **2 篇**剔除（2609.30468 SplatLab / 2611.06817 Open-HumanWAM）。

## 全文抓取（第 4 步）
- 19 篇候选跑 `scripts/fetch_fulltext.py`，严格串行 3s/篇（约 74 秒）：**18 篇 L0/FULL**（26,116–114,240 字符）+ **1 篇 L1/PARTIAL**——2611.13296（XR 实时三维元胞自动机）：arXiv HTML 404、ar5iv 仅返 **arXiv 摘要页 4,350 字符**（正文含 Skip to main content / arXivLabs 样板、无任何章节标题），**人工抽看正文后改判 PARTIAL** 并在 manifest 加 note，按摘要级评估、TEC/EXP 上限 3、PER 上限 4，未脑补公式/消融/未提基线。
- WROTE=19>0；manifest 合并写入校验通过；无 L5、无 OCR。
- **脚本判定不可依赖字符数**：2611.13296 的 4,350 字符被脚本初判 FULL，实际无正文节——再次印证「PARTIAL 必须人工抽看正文」。

## 评分与三关（第 5-6 步）
- 先抓全文再定稿。7 维加权定稿：主批 **6 A / 6 B / 3 C（无 S）**；backfill **2 A / 2 B**。
- 门① 最大 Jaccard **0.082**（2611.13280 RetinexGS vs 库内 2609.22849 LINGO；<0.62，非同质）。
- 门② 定稿 Top10 覆盖 **7 赛道**（神经渲染×3 / 重建与SLAM×2 / 内容生成×1 / 系统与平台×1 / 化身与人体×1 / 感知与认知×1 / 空间计算与UI×1）≥5，**未触发重筛**；全批 9 赛道（重建与SLAM 3 / 神经渲染 3 / 系统与平台 2 / 感知与认知 2 / 内容生成 1 / 化身与人体 1 / 空间计算与UI 1 / 触觉与多模态 1 / 交互与输入 1）。
- 门③ 当日最高 **4.08 < 库内近 30 天 Top10 均分 4.4370**（窗口 2026-10-13~11-12、442 条入窗、现算；Top10 = SMoRe 4.57 / 视频扩散化身 4.57 / Open-HumanScale 4.57 / Map2SLAM 4.57 / ACD-GS 4.37 / Stereo CI 4.37 / XM4D 4.36 / RacerGS 4.35 / HaNDF 4.34 / EgoExplorer 4.30）→ **非重磅日，无 S 级**（本批亦无 ≥4.2 达线论文，无需校准关降级）。
- OUTDATED/SUPERSEDED **0 篇**。

## 产物（第 7-8 步）
- 报告 2 份（主批 + backfill）+ 原子笔记 16 篇（grade≥B：主批 12 + backfill 4；3 篇 C 级仅入馆）+ MOC 2 份 + 总索引刷新 + 7 维表/scored/run_log 各 2 套。
- registry 888 → **907**（+15 +4；备份 `papers/library/registry.jsonl.bak-20261112`；按 base_id 幂等）。
- notes 548 → **564**。
- 门③ 现算值供下一批参考：**4.4370**（窗口将逐日滚动，须再算）。
'''
open(f'papers/daily/{DATE}/run_log.md', 'w', encoding='utf-8').write(run_log_main)

run_log_bf = f'''# backfill-1112 执行日志

- **来源**：11-11 公告批次 RSS（7 分类去重 669 → KW 命中 37）中 7 篇 v2/v3 再公告未入馆者，经摘要核实 XR 相关 4 篇 → 本批；另 3 篇非 XR 剔除（SSR 人形越野 / 巡视器导航栈 / mmWave 无线电 SLAM）。
- **诚实口径**：本批全部为 **v2/v3 再公告**（2608.04971 v2 / 2605.22715 v3 / 2505.20858 v3 / 2503.00868 v3），原始投稿 **2026-08-05 / 2026-05-21 / 2025-05-27 / 2025-03-02**，API `updated` 显示 2026-11-09~11-10 更新后再公告；均非 11-11 当日新提交，单独编号、不参与当日重磅日判定。
- **全文**：4 篇全部 **L0/FULL**（71,312 / 78,301 / 114,240 / 82,526 字符）。
- **定稿**：2 A / 2 B。最高 **2505.20858 TFD-SfM 4.15**（严格冷启动联合优化外参、焦距与几何，ETH3D RRA@5°=97.9 / RTA@5°=91.4 高于 COLMAP 的 91.2）· 2605.22715 AnyMo 3.85（14 个未见可穿戴数据集 Acc 35.7 vs UniMTS 31.9）· 2608.04971 跨现实转场 3.37（N=24 一致性劣化使 presence 4.82→3.85）· 2503.00868 流体 3DGS 3.20（反解仿真器参数，速度场量级 ×10^-1→×10^-3）。
- **registry**：+4（batch=backfill-1112，幂等）。
'''
open('papers/daily/backfill-1112/run_log.md', 'w', encoding='utf-8').write(run_log_bf)

# ---------- registry ----------
reg_path = 'papers/library/registry.jsonl'
bak_path = reg_path + '.bak-20261112'
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
print(f'registry +{added}（现有 {len(rows) + added}）')

# ---------- notes ----------
def slugify(t):
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
        method=p['method'], experiments='\n'.join(f'- {x}' for x in p['experiments']),
        innovation='\n'.join(f'- {x}' for x in p['innovation']),
        limits='\n'.join(f'- {x}' for x in p['limits']),
        relation=p['relation'], repro=p['repro'], action=p['action'])
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


moc(MAIN, f'papers/MOC/MOC-{DATE}.md', f'MOC · {DATE}（11-11 公告批次）',
    '> 当日地图：**公告日 2026-11-11（周三）≠ 拉取日 2026-11-12（周四 02:30）**——诚实口径。11-11 00:00 UTC 释放当日公告批次；API published 口径核验提交日 **11-10×12 / 11-09×2 / 10-22×1**（2611.12912 为三周延迟公告；RSS published 为公告时间戳）。\n'
    '> 主批 XR 新稿 **15 篇（6 A / 6 B / 3 C，无 S）**，Top10 实数 10 篇最高 **4.08**（FlashMotion）；listing 11-11 组 436 篇摘要级命中 28 篇 = RSS 真新 28 篇（两渠道逐篇一致，RSS 漏网 0 篇）；11-10 组复采 837 篇未入馆、摘要级 18 篇命中与上批已剔 18 篇完全一致 → 0 漏网。\n'
    '> 全文：18×L0/FULL + 1×L1/PARTIAL（2611.13296：arXiv HTML 404 + ar5iv 摘要页，按摘要级评估并显式声明）。\n'
    '> 覆盖度三关：门① 0.082 / 门② 定稿 Top10 覆盖 7 赛道（未重筛；全批 9 赛道）/ 门③ **4.08 < 4.4370**（现算，442 条入窗）→ **非重磅日，无 S**。\n'
    '> Top10（实数 10 篇）：FlashMotion 4.08 · GEMOR-GS 3.87 · NIF-VIO 3.78 · VR 遥操作建筑机器人 3.66 · RF3DGS 3.63 · EgoHMP 3.62 · FastWild-GS 3.58 · 第一视角手-物接触转场 3.44 · 大范围空间锚点 3.30 · RetinexGS 3.30。')

moc(BF, 'papers/MOC/MOC-backfill-1112.md', 'MOC · backfill-1112（旧稿 v2/v3 再公告首次入馆）',
    '> **非当日新提交**：本批 4 篇均为 11-11 公告 RSS 混入的旧稿 v2/v3 再公告（原始投稿 2025-03 ~ 2026-08，2026-11-09~11-10 更新），诚实口径单独编号，不参与当日重磅日判定。\n'
    '> 定稿 2 A / 2 B，最高 **2505.20858 4.15**（TFD-SfM 严格冷启动联合优化外参/焦距/几何）。其余：AnyMo 3.85（可穿戴设置无关动捕）· 跨现实转场 3.37（投影–HMD 一致性劣化的代价）· 流体 3DGS 3.20（反解仿真器参数）。')


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
        L.append(f"- **公告类型**：{p['announce']}（公告日 2026-11-11，拉取日 2026-11-12）")
        if p.get('grade_note'):
            L.append(f"- **等级说明**：{p['grade_note']}")
        L.append(f"- **一句话结论**：{p['conclusion']}")
        L.append(f"- **要解决的问题**：{p['problem']}")
        L.append(f"- **方法详解**：{p['method']}")
        L.append('- **实验与结果**：')
        for x in p['experiments']:
            L.append(f"    - {x}")
        L.append('- **创新点与贡献**：')
        for x in p['innovation']:
            L.append(f"    - {x}")
        L.append('- **局限与风险**：')
        for x in p['limits']:
            L.append(f"    - {x}")
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
    L.append('- 抓取降级：19 篇候选串行 3s/篇；18 篇 L0 一次命中；2611.13296 **arXiv HTML 404**、ar5iv 仅返 arXiv 摘要页（4,350 字符，人工确认无 Introduction/Method 节、正文为 arXiv 站点样板）→ manifest 改判 **PARTIAL** 并加 note，按摘要级评估；TEC/EXP 上限 3、PER 上限 4，**未脑补公式、消融或未提基线**。无限流、无 L5、无 OCR、无伪造。')
    open(path, 'w', encoding='utf-8').writelines([x + '\n' for x in L])


HEADER = (
    '## 一、执行摘要\n'
    '- **公告日 2026-11-11（周三）≠ 拉取日 2026-11-12（周四 02:30）**——诚实口径。API published 核验提交日 **11-10×12 / 11-09×2 / 10-22×1**（2611.12912 大范围空间锚点提交于 10-22，延迟约三周公告；RSS published 是公告时间戳非提交日）。\n'
    '- **数据源**：API 双主机探针均 200；RSS 7 分类去重 **669** → KW 命中 **37**。两渠道互证：**listing 摘要级 28 篇 = RSS 真新 28 篇，双向差集 0，RSS 漏网 0 篇**；11-10 组复采 1,059 槽位 / 868 唯一，未入馆 837 篇摘要级命中 18 篇与上批已剔 18 篇逐篇一致 → **0 漏网**。\n'
    '- **主批 XR 新稿 15 篇（6 A / 6 B / 3 C，无 S；Top10 实数 10 篇）**。Top10：**FlashMotion 4.08 A（MeanFlow 改写为干净运动预测 + 非自回归 BiMamba：BABEL 4 步 R@1 29.13（GT 28.50）、FID 0.907，10^4 帧 46,303 FPS ≈ 最快 T2M 基线 13.6×，模型仅 60M）** · GEMOR-GS 3.87（LiDAR-相机外参离线精化 + 全局精化建图 + 在线重定位 3DGS SLAM：离线重建 100% 胜在线地图、逐帧 PSNR +14.3–19.9 dB、留出视角重定位 86–100% vs CBD 35%/Bright 0%） · NIF-VIO 3.78（一致性证据驱动的融合状态机 + 载体运动模型：车/地铁/电梯正确定位率 24.00%/35.79%/76.61% → 98.49%/98.56%/98.19%） · VR 遥操作建筑机器人 3.66（半自治把钻孔成功率 53%→82%、位姿误差 36.4→23.3 mm、NASA-TLX 61.7→32.9，但标定良好时规则式全自主仍最优 96%） · RF3DGS 3.63（多视图最小像素强度先验生成伪标签 + Adaptive Twin Rendering：自建基准 PSNR 31.45 vs vanilla 3DGS 29.58 / NeRFReN 26.36） · EgoHMP 3.62（第一视角 + 头动替代 gaze 推断交互意图：GIMO MPJPE-Path 141.2→114.9 mm） · FastWild-GS 3.58（128 维逐图外观令牌 + 小 MLP 取代 SH 颜色：PhotoTourism 8.8 分钟/场景 25.52 dB，比 AsymGS 快 23×） · 第一视角手-物接触转场 3.44（4,021 段自建数据 + object-aware 联合建模：无 NMS 49.30 / 有 NMS 51.19 mAP） · 大范围空间锚点 3.30（距离加权逐帧点云配准把 ~3 m 锚点有效半径扩到二十余米，误差 2.24–3.16 cm / 0.76–1.17°） · RetinexGS 3.30（RAW 域 Retinex 分解 + 传感器噪声感知：sRGB PSNR 25.01 dB 比 LE3D +2.18 dB，91–145 FPS）。\n'
    '- **覆盖 9 赛道（全批）/ Top10 覆盖 7 赛道**：重建与SLAM 3（Top10 占 2）/ 神经渲染 3（Top10 占 3）/ 系统与平台 2 / 感知与认知 2 / 内容生成 1 / 化身与人体 1 / 空间计算与UI 1 / 触觉与多模态 1 / 交互与输入 1。\n'
    '- **覆盖度三关**：门① 最大 Jaccard **0.082**（2611.13280 vs 库内 2609.22849 LINGO，<0.62）；门② 定稿 Top10 覆盖 **7 赛道** ≥5（未触发重筛）；门③ 当日最高 **4.08 < 库内近 30 天 Top10 均分 4.4370**（现算，442 条入窗）→ **非重磅日，无 S 级**（本批无 ≥4.2 达线论文）。\n'
    '- **全文证据**：18 篇 **L0/FULL** + 1 篇 **L1/PARTIAL**（2611.13296：arXiv HTML 404 + ar5iv 摘要页，摘要级评估并显式声明）。OUTDATED 0。\n'
    '- **backfill-1112（4 篇，非当日新提交）**：11-11 公告 RSS 混入的旧稿 v2/v3 再公告首次入馆——TFD-SfM 4.15（严格冷启动 SfM，ETH3D RRA@5° 97.9 / RTA@5° 91.4 高于 COLMAP 91.2）· AnyMo 3.85（可穿戴设置无关动捕，14 个未见数据集 Acc 35.7 vs UniMTS 31.9）· 跨现实转场 3.37（一致性劣化使 presence 4.82→3.85、TLX 23.47→36.32）· 流体 3DGS 3.20（反解仿真器参数，速度场量级 ×10⁻¹→×10⁻³）。\n'
    '- **路线观察**：① **XR 显示侧「一致性」成为可量化变量**：2608.04971 把投影–HMD 的空间/外观/时延一致性逐项劣化后测出 presence/TLX/耗时三路代价，与库内 2609.2xxxx 系列「多显示一致性」条目互补；② **3DGS 的重心从「更快重建」转向「更准几何与更省传输」**：GEMOR-GS（外参精化 + 可重入地图）、DepthGS（深度误差上界驱动的正则）、RF3DGS（反射解耦）、RetinexGS（RAW 噪声建模）四条线同日均指向「退化条件下的可信几何」，而 FastWild-GS 转向分钟级野外可用性；③ **VIO/SLAM 的鲁棒性研究从「算法层」下沉到「参考系层」**：NIF-VIO 明确指出「相机与 IMU 同处惯性系」这一被默认的假设在车载/电梯场景失效，与库内 DPGS-SLAM、DASH-SLAM 的「先验失效」议题同源；④ **XR 人因研究开始给出效应量而非仅显著性**：2611.14029（VR vs AR 合奏，N=28）只在 Involvement 上显著（r=.70），创造力支持与情绪无差异，偏好 14:13 几乎五五开——对「VR 天然更适合创作」的叙事是一次有分量的反证；⑤ 硬件类渲染缺口（波导/可变焦/Maxwellian/光场）本批 **仍无破冰**，触觉侧亦只有 2611.14389（2D 触觉编码 3D 形状，C 级）。'
)

report(TOP10, f'reports/XR-Daily-Report-{DATE}.md', f'XR 每日论文解读报告 · {DATE}（11-11 公告批次）', HEADER, 10,
       ['- 门①（同质去重）：最大 Jaccard **0.082** < 0.62（2611.13280 RetinexGS vs 库内 2609.22849 LINGO），通过，无同质重复。库侧 token 取 title+title_zh（registry 无摘要字段），口径偏保守。',
        '- 门②（赛道覆盖）：定稿 Top10 覆盖 **7 赛道**（神经渲染×3 / 重建与SLAM×2 / 内容生成×1 / 系统与平台×1 / 化身与人体×1 / 感知与认知×1 / 空间计算与UI×1）≥5，**未触发重筛**，为本批首次无需回补即达门槛。第 11–13 名（DepthGS 3.23 重建、XR 合奏 3.07 感知、3D 触觉编码 2.92 触觉）分属三条未进 Top10 的赛道，说明覆盖不是靠低分补位达成。',
        '- 门③（价值天花板）：当日最高 **4.08** < 库内近 30 天 Top10 均分 **4.4370**（现算，窗口 2026-10-13~11-12、442 条入窗；Top10 = SMoRe/视频扩散化身/Open-HumanScale/Map2SLAM 4.57 · ACD-GS/Stereo CI 4.37 · XM4D 4.36 · RacerGS 4.35 · HaNDF 4.34 · EgoExplorer 4.30）→ **非重磅日，无 S 级**。本批亦无 ≥4.2 达线论文，校准关未触发任何降级改写。',
        '- 主会话校准记录：19 篇子代理评分逐条核对 scores_why 与正文数字，确认 2611.13628 DepthGS 维持 TEC 3（DTU Chamfer 0.51 mm 未超 GSPrior 0.50 mm，引理 2 为标量近似），未改判任何维度；2611.13296 因 PARTIAL 按摘要级从严（TEC/EXP≤3、PER≤4）计 1.55 C。',
        '- 低量日不凑数原则复核：主批 15 篇中 3 篇 C 级（<3.0）仅入馆不解读；Top10 取实数 10 篇（含 4 篇 B 级），未为凑满 10 篇而放宽 B 级下限，亦未把 B 级拔高为 A。',
        '- OUTDATED/SUPERSEDED **0 篇**（本批无被库内更晚工作取代者；硬件类显示方向仍无新增）。\n'])

report(BF, 'reports/XR-Backfill-Report-backfill-1112.md', 'XR Backfill 报告 · backfill-1112（旧稿 v2/v3 再公告首次入馆）',
       '## 一、执行摘要\n'
       '- **诚实口径**：本批 4 篇均为 **11-11 公告批次 RSS 混入的旧稿 v2/v3 再公告**（原始投稿 2025-03-02 / 2025-05-27 / 2026-05-21 / 2026-08-05，API `updated` 显示 2026-11-09~11-10 更新后再公告），首次入馆；**均非 11-11 当日新提交**，单独编号、不参与当日重磅日判定。\n'
       '- **定稿 2 A / 2 B**，最高 **2505.20858 TFD-SfM 4.15**（从严格冷启动联合优化相机外参、焦距与几何：ETH3D RRA@5° 97.9 / RTA@5° 91.4 / ACC@5cm 69.9，RTA 高于 COLMAP 的 91.2 与 DKM 硬塞 COLMAP 的 65.5；DTU 99.4/90.0、Mip-NeRF 360 100.0/99.2）。其余：AnyMo 3.85（14 个未见可穿戴数据集 Acc 35.7 / macro-F1 29.5 / R@2 57.5，相对 UniMTS +3.8/+3.1/+10.6 点）· 跨现实转场 3.37（N=24，一致性劣化后 presence 4.82→3.85、TLX 23.47→36.32、精密交互 +82.92 s）· 流体 3DGS 3.20（把「恢复流体」改写为「反解仿真器参数」，速度场量级 ×10⁻¹→×10⁻³，15 名从业者主观优于逐帧生成）。\n'
       '- **全文**：4 篇全部 L0/FULL（71,312 / 78,301 / 114,240 / 82,526 字符）。\n'
       '- **剔除**：同批 v2/v3 未入馆 7 篇中 3 篇经摘要核实非 XR（2605.30770 SSR 人形越野 / 2611.08100 轮式巡视器 ROS2 导航栈 / 2611.01491 mmWave 无线电 SLAM）。',
       4,
       ['- 门①/门③ 对 backfill 不适用（非当日新提交，不参与重磅日判定）；门② 覆盖 4 赛道（重建与SLAM×1 / 化身与人体×1 / 空间计算与UI×1 / 内容生成×1）。',
        '- 本批最高 4.15 未达 4.2 S 线，且 backfill 一律不评 S（即便达线亦按校准关记 A），未拔高。\n'])

# ---------- MOC-总索引 ----------
moc_path = 'papers/MOC/MOC-总索引.md'
h = open(moc_path, encoding='utf-8').read()
n0 = len(h)


def rep(old, new, tag):
    global h
    assert old in h, f'ANCHOR NOT FOUND: {tag}'
    h = h.replace(old, new, 1)


rep('累计 **888 篇**；跨度 2026-09-15 ~ 2026-11-10',
    '累计 **907 篇**；跨度 2026-09-15 ~ 2026-11-11', 'head-count')
rep('**backfill-1111:8（11-10 公告 RSS 混入旧稿 v2/v3 再公告，首次入馆）**；',
    '**backfill-1111:8（11-10 公告 RSS 混入旧稿 v2/v3 再公告，首次入馆）** · '
    '**2026-11-12:15（11-11 公告批次真新提交，非重磅日无S；listing 436 篇摘要级命中 28 篇 = RSS 真新 28 篇两渠道互证）** · '
    '**backfill-1112:4（11-11 公告 RSS 混入旧稿 v2/v3 再公告，首次入馆）**；', 'batch-list')

note12 = ('> **状态注记（2026-11-12）**：周四 02:30，处理 **2026-11-11（周三）公告批次**（公告日≠拉取日，诚实口径）。'
 'API published 口径核验提交日 **11-10×12 / 11-09×2 / 10-22×1**（2611.12912 大范围空间锚点提交 10-22，延迟约三周公告；RSS published 为公告时间戳）。'
 '漏网对账（先于拉取，`scripts/audit_listing_1112.py`，PREV_DAY=11-10 / NEW_DAY=11-11）：listing 7 分类最新公告日均为 **11-11**（无漏跑公告日、无跳空）；11-10 组复采逐分类 **declared=got**（CV 317/GR 14/HC 63/MM 7/RO 165/AI 480/IV 13，1,059 槽位；cs.AI 补采 skip=500 合并 228 条），未入馆 **837 篇**摘要级命中 **18 篇**，逐篇 id 与上批已剔 18 篇非 XR **完全一致** → **0 漏网**；**11-11 组 436 篇唯一论文**（532 槽位）摘要级 XR 命中 **28 篇**。'
 '**数据源**：API 双主机 200；RSS 去重 **669** → KW 命中 **37** = 28 篇真新（15 XR + 13 非 XR）+ 7 篇旧稿 v2/v3 未入馆（4 XR → backfill-1112）+ 2 篇库内 v2；**listing 28 篇与 RSS 真新 28 篇双向差集 0（两渠道互证）**。'
 '主批甄别 **XR 核心/强相关 15 篇**（剔非 XR 13 篇）；全文 **18 篇 L0/FULL + 1 篇 L1/PARTIAL**（2611.13296：arXiv HTML 404 + ar5iv 仅返 arXiv 摘要页 4,350 字符，人工复核改判，摘要级评估并显式声明）。'
 'Top10（**实数 10 篇**）：最高 **4.08 FlashMotion（A）**，**非重磅日无 S**；覆盖 **7 赛道**（神经渲染×3/重建×2/内容生成·系统·化身·感知·空间计算各×1）。'
 '三关：门① max Jaccard **0.082**（2611.13280 vs 库内 2609.22849 LINGO）；门② Top10 覆盖 7 赛道 ≥5（未重筛）；门③ 当日最高 **4.08 < 4.4370**（442 条入窗，现算）→ **非重磅日，无 S**；OUTDATED 0。'
 'registry 888 → **907**（+15 +4），笔记 548 → **564**。详见 [运行报告](../../reports/XR-Daily-Report-2026-11-12.md) / [MOC-2026-11-12](./MOC-2026-11-12.md) / [MOC-backfill-1112](./MOC-backfill-1112.md) / [Backfill 报告](../../reports/XR-Backfill-Report-backfill-1112.md)。\n')
anchor_end = '详见 [运行报告](../../reports/XR-Daily-Report-2026-11-11.md) / [MOC-2026-11-11](./MOC-2026-11-11.md) / [MOC-backfill-1111](./MOC-backfill-1111.md) / [Backfill 报告](../../reports/XR-Backfill-Report-backfill-1111.md)。'
i = h.find(anchor_end)
assert i >= 0, 'ANCHOR NOT FOUND: note1111-end'
j = h.find('\n', i) + 1
h = h[:j] + note12 + h[j:]

rep('| 最新一期 | [MOC · 2026-11-11](./MOC-2026-11-11.md) |',
    '| 最新一期 | [MOC · 2026-11-12](./MOC-2026-11-12.md) |', 'quick-latest')
rep('| 上一期 | [MOC · 2026-11-10](./MOC-2026-11-10.md) |',
    '| 上一期 | [MOC · 2026-11-11](./MOC-2026-11-11.md) |', 'quick-prev')
rep('（现有 548 篇）', '（现有 564 篇）', 'quick-notes')
rep('| 最新运行状态 | [运行报告 2026-11-11](../../reports/XR-Daily-Report-2026-11-11.md)（11-10 公告批次 31 篇 1S/14A/6B/10C **重磅日**；listing 868 篇摘要级命中 49 篇 = RSS 真新 49 篇双向差集 0；11-09 组复采 0 漏网；全文 37×L0/FULL + 2×L1/PARTIAL；Top10 实数 10 篇覆盖 5 赛道（达门槛未重筛）；门③ 现算 4.4100，当日最高 4.57 达线 → 1 篇 S） |',
    '| 最新运行状态 | [运行报告 2026-11-12](../../reports/XR-Daily-Report-2026-11-12.md)（11-11 公告批次 15 篇 6A/6B/3C **非重磅日无S**；listing 436 篇摘要级命中 28 篇 = RSS 真新 28 篇双向差集 0；11-10 组复采 837 篇未入馆、18 篇命中与上批已剔完全一致 → 0 漏网；全文 18×L0/FULL + 1×L1/PARTIAL（2611.13296 摘要级）；Top10 实数 10 篇覆盖 7 赛道（未重筛）；门③ 现算 4.4370，当日最高 4.08 未达线 → 无 S） |', 'quick-status')

row_main = ('| 2026-11-12 | [MOC-2026-11-12](./MOC-2026-11-12.md) | XR 15（Top10 实数 10）· 6A/6B/3C · **非重磅日（无S）** | '
            '11-11 公告批次真新提交 15 篇（11-10×12/11-09×2/10-22×1 延迟公告）；listing 436 篇摘要级命中 28 篇 = RSS 真新 28 篇（双向差集 0）；11-10 组复采 0 漏网；全文 18×L0/FULL + 1×L1/PARTIAL |\n'
            '| backfill-1112 | [MOC-backfill-1112](./MOC-backfill-1112.md) | 补录 4（2A/2B）· 非当日新提交 | 11-11 公告 RSS 混入旧稿 v2/v3 再公告 4 篇（2503/2505/2605/2608，2026-11-09~10 更新）；最高 2505.20858 4.15 |')
rep('| backfill-1111 | [MOC-backfill-1111](./MOC-backfill-1111.md) | 补录 8（3A/4B/1C）· 非当日新提交 | 11-10 公告 RSS 混入旧稿 v2/v3 再公告 8 篇（2503/2512/2603/2605×2/2608/2609×2，2026-11-07~09 更新）；最高 2609.11894 4.22 |',
    '| backfill-1111 | [MOC-backfill-1111](./MOC-backfill-1111.md) | 补录 8（3A/4B/1C）· 非当日新提交 | 11-10 公告 RSS 混入旧稿 v2/v3 再公告 8 篇（2503/2512/2603/2605×2/2608/2609×2，2026-11-07~09 更新）；最高 2609.11894 4.22 |\n'
    + row_main, 'batch-table')

seg = '\n### 2026-11-12 新增（Top10 实数 10 篇：6 A + 4 B，非重磅日无 S）\n\n| # | 论文 | 赛道 | 分值 | 等级 | 证据 |\n|---:|---|---|---:|---|---|\n'
for i2, pid in enumerate(TOP10_ORDER, 1):
    p = next(x for x in MAIN if x['id'] == pid)
    seg += f"| {i2} | {esc(p['title_zh'])} | {p['track']} | {p['value']:.2f} | {p['grade']} | {p['evidence']} |\n"
seg += '\n### backfill-1112 补录（4 篇：2 A + 2 B，非当日新提交）\n\n| # | 论文 | 赛道 | 分值 | 等级 | 证据 |\n|---:|---|---|---:|---|---|\n'
for i2, p in enumerate(BF, 1):
    seg += f"| {i2} | {esc(p['title_zh'])} | {p['track']} | {p['value']:.2f} | {p['grade']} | {p['evidence']} |\n"
h = h.rstrip() + '\n' + seg

foot_pat = re.compile(r'^\*最后更新：[^\n]*\* · MOC \d+ 份$', re.M)
assert foot_pat.search(h), 'ANCHOR NOT FOUND: footer'
h = foot_pat.sub('*最后更新：2026-11-12（11-11 公告批次：15 篇 XR 新稿 6A/6B/3C **非重磅日无S**；listing 436 篇摘要级命中 28 篇 = RSS 真新 28 篇双向差集 0；11-10 组复采 837 篇未入馆、18 篇命中与上批已剔完全一致；全文 18×L0/FULL + 1×L1/PARTIAL（2611.13296 摘要级）；Top10 覆盖 7 赛道未重筛；门③ 现算 4.4370，当日最高 4.08 未达线 → 无 S；backfill-1112 补录 4 篇 2A/2B）。* · 库内 **907 篇** · 原子笔记 **564 篇** · MOC 49 份', h)

open(moc_path, 'w', encoding='utf-8').write(h)
print('MOC-总索引 refreshed（%d -> %d chars）' % (n0, len(h)))
print('DONE')
