# -*- coding: utf-8 -*-
"""2026-11-07 产物生成：主批（11-06 公告批次 23 篇，无 backfill——RSS 周六 skipDays 空源）。
公告日 2026-11-06（周五）≠ 拉取日 2026-11-07（周六 13:38），诚实口径。
API published 口径核验提交日：11-04×5 / 11-05×30（均早于公告日）。
漏网对账（先于拉取）：listing 7 分类最新公告日均为 2026-11-06；11-05 组复采 declared=got，
386 篇未入馆摘要级复核 10 篇命中均为 11-06 运行已剔非 XR（与上批清单逐篇一致）→ 0 漏网；
11-06 组 386 篇唯一论文摘要级 XR 命中 35 篇 = 23 XR + 12 非 XR（RSS 周六空源，listing 为唯一采集渠道）。
消费 data/scored_1107.json；registry 幂等追加（先备份，in_top10 按定稿显式设置）。"""
import json, os, shutil, glob

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
os.chdir(ROOT)
D = json.load(open('data/scored_1107.json', encoding='utf-8'))
MAIN = D['main']
TOP10_IDS = set(D['top10_ids'])
TOP10_ORDER = list(D['top10_ids'])   # 定稿展示顺序（门②重筛后；勿用 set 迭代，会丢顺序）
DATE, ANN = '2026-11-07', '2026-11-06'
GATE3 = 4.393               # 门③ 现算均分（窗口 2026-10-08~11-07，436 条入窗）
TODAY_MAX = MAIN[0]['value']  # 4.36
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

def seven_table(papers, path, title, intro):
    lines = [f'# {title}\n', intro + '\n', TBL_HEAD]
    for p in papers:
        lines.append(dim_row(p, p['id'] in TOP10_IDS) + '\n')
    open(path, 'w', encoding='utf-8').writelines(lines)

os.makedirs(f'papers/daily/{DATE}', exist_ok=True)

seven_table(MAIN, f'papers/daily/{DATE}/7dim-table.md',
    f'{DATE} 全量 7 维度对比表（参考）',
    '批次：2026-11-07（**2026-11-06（周五）公告批次**——公告日 11-06 ≠ 拉取日 11-07（周六 13:38），诚实口径）。\n'
    '候选池 23 篇：漏网对账（先于拉取，`scripts/audit_listing_1107.py`，TARGET_DAY=2026-11-05，show=500 单页×7 分类）→ 7 分类最新公告日均为 **2026-11-06**（无漏跑公告日）；**11-05 组复采逐分类 declared=got**（CV 148/GR 7/HC 29/MM 6/RO 62/AI 217/IV 8，477 槽位）→ 未入馆 **386 篇**，摘要级复核 **10 篇命中均为 11-06 运行已剔非 XR（与上批 10 篇剔除清单逐篇一致）→ 0 漏网**；**11-06 组 386 篇唯一论文**（CV 138/GR 11/HC 22/MM 2/RO 81/AI 198/IV 6，458 槽位，全部未入馆）→ 摘要级 XR 命中 **35 篇**（23 XR + 12 非 XR）。\n'
    '数据源：API 双主机 200；**RSS 7 分类周六 skipDays 空源**（lastBuildDate 2026-11-07 05:00 UTC，`fetch_rss.py` WROTE=0）→ **本批以 listing 为唯一采集渠道**（周末节律，三源核验：listing 日期头 + API submittedDate/published + RSS 空源）。arXiv API published 口径核验提交日：**11-04×5 / 11-05×30**（均早于公告日 11-06；RSS published 字段为公告时间戳，非提交日）。\n'
    '全文：23 篇候选串行 3s/篇：**22 篇 L0/FULL**（13,629–179,859 字符）+ **1 篇 L0/PARTIAL**（2611.08301 REACT：arXiv HTML 仅提供 Supplementary Material、ar5iv 无转换版，主文缺失，按摘要级评估并显式声明；人工复核正文中段排除 ar5iv 摘要页误判）。\n'
    '覆盖度三关：门① 最大 Jaccard **0.074**（2611.08330 InstantHand vs 库内 2609.21498 VoxelTTO，<0.62 通过）；门② 纯价值 Top10 覆盖 **4 赛道**（神经渲染×3/感知与认知×3/重建与SLAM×2/化身与人体×2）→ **触发一次重筛**：剔除神经渲染赛道最低分 T²-Splat 3.575（与 ReferClaw 同分，按赛道冗余度与库内增量定位取舍），回补未覆盖核心赛道（触觉与多模态）B 级池最高分 多模态触觉显示 3.365 → 定稿 Top10 覆盖 **5 赛道**（T²-Splat 仍入馆写 B 级笔记仅不占名额，同 11-04 SHield/11-06 BudgetSplat 先例）；门③ 当日最高 **4.36 < 库内近 30 天 Top10 均分 4.393**（窗口 2026-10-08~11-07、436 条入窗、现算）→ **非重磅日，无 S 级**；XM4D 4.36 达 S 线（≥4.2）按校准关记 A（同 10-24 EgoHand/10-27 WFM/10-28 RacerGS 先例）。OUTDATED 0。')

# ---------- scored.md + run_log.md ----------
def scored_md(papers, path, title, extra):
    L = [f'# {title}\n', extra + '\n', '| 排名 | arXiv | 标题 | 赛道 | 总分 | 等级 | 证据 | 公告类型 |',
         '|---|---|---|---|---|---|---|---|']
    for i, p in enumerate(papers, 1):
        L.append(f"| {i} | {p['id']} | {esc(p['title_zh'])} | {p['track']} | {p['value']:.2f} | {p['grade']} | {p['evidence']} | {p['announce']} |")
    open(path, 'w', encoding='utf-8').writelines([x + '\n' for x in L])

scored_md(MAIN, f'papers/daily/{DATE}/scored.md', f'{DATE} 评分明细',
    '评分口径：7 维加权 IMP0.20·NOV0.20·TEC0.15·EXP0.15·PER0.15·TRL0.08·REP0.07；分档 S≥4.2 / A3.6–4.2 / B3.0–3.6 / C<3.0。全部基于全文证据定稿（22 篇 L0/FULL + 1 篇 L0/PARTIAL：REACT 仅补充材料）。\n'
    '覆盖度三关：门① 最大 Jaccard 0.074 < 0.62（通过，非同质）；门② 纯价值 Top10 覆盖 4 赛道 → 触发一次重筛（剔除 T²-Splat、回补 多模态触觉显示），定稿 Top10 覆盖 5 赛道 ≥5（通过；全批 7 赛道）；门③ 当日最高 4.36 < 库内近 30 天 Top10 均分 4.393（现算，436 条入窗）→ **非重磅日，无 S 级**（XM4D 4.36 达 S 线按校准关记 A）。\n'
    'OUTDATED/SUPERSEDED 0 篇。等级分布：8 A / 12 B / 3 C。')

run_log_main = f'''# {DATE} 执行日志

## 数据源与对账（第 1-3 步）
- **漏网对账（先于拉取）**：`scripts/audit_listing_1107.py`（TARGET_DAY=2026-11-05，上批公告日；show=500 单页×7 分类）→ 7 分类最新公告日均为 **2026-11-06**（无漏跑公告日）；**11-05 组复采逐分类 declared=got**（CV 148/GR 7/HC 29/MM 6/RO 62/AI 217/IV 8，477 槽位）→ 未入馆 **386 篇**，`scripts/filter_missed_xr_abstract.py` 摘要级复核 **10 篇命中均为 11-06 运行已剔非 XR（与上批 10 篇剔除清单逐篇一致，双向差集 0）→ 0 漏网、无 backfill**（data/missed_xr_abstract_1107_g1105.json）。
- **摘要级 XR 过滤（新公告组）**：11-06 组 **386 篇唯一论文**（CV 138/GR 11/HC 22/MM 2/RO 81/AI 198/IV 6，458 槽位，全部未入馆）→ 摘要级 XR 命中 **35 篇**（data/missed_xr_abstract_1107.json，meta fetched 386/386）。
- **RSS 通道**：`scripts/fetch_rss.py` 7 分类 **WROTE=0**——周六 skipDays 节律空源（lastBuildDate 2026-11-07 05:00 UTC，非代理故障）；**本批以 listing 为唯一采集渠道**。三源互证：listing 日期头（11-06 为最新公告日）+ API published（提交日 11-04×5/11-05×30，与 11-06 公告组节律一致）+ RSS 空源（周六无公告）。
- **API 探针**：export.arxiv.org 与 arxiv.org 双主机 200。

## 甄别（第 3 步）
- 主批 XR 核心/强相关 **23 篇**入评分池；剔非 XR **12 篇**（2611.06993 JPTA 视觉语言模型直推适配 / 2611.07063 SD-LoRA 少样本视觉语言适配 / 2611.07081 WV-GS 自动驾驶宽视角合成 / 2611.07551 PreSTP 视频扩散 token 剪枝加速 / 2611.07630 事件相机 LED 跟踪（无人机引导）/ 2611.07651 GraspBench 跨机器人抓取评测 / 2611.07712 AffectiveVLA 人形机器人社交触摸 / 2611.08005 DCAP 可变接触3D物体放置 / 2611.08097 STEP 人形机器人运动 / 2611.08100 巡视器自主导航栈 / 2611.08372 MOMASPLAT 移动操作示范增广 / 2611.08407 Social Humanoid 人-人形交互）。
- 旧稿 replace/cross 再公告：**0 篇**（RSS 空源；listing 公告日组天然只含新提交，与 10-18 确认的「旧稿再公告只进 RSS 不进 listing 日组」机制一致）→ **无 backfill**。

## 全文抓取（第 4 步）
- 23 篇候选跑 `scripts/fetch_fulltext.py`，严格串行 3s/篇（约 3 分钟）：**22 篇 L0/FULL**（13,629–179,859 字符）+ **1 篇 L0/PARTIAL**（2611.08301 REACT：arXiv HTML 仅提供 Supplementary Material——主文（问题陈述/训练细节/数据集名称）缺失；ar5iv 无转换版（仅摘要页）；按摘要级评估并在 7 维表/报告/笔记显式声明，manifest 已改判 PARTIAL 并加 note）。无限流/降级/伪造。
- **人工复核正文中段章节**（防 11-05 ar5iv 摘要页误判教训）：22 篇 FULL 均含 Method/Experiments/Results/Conclusion 等实质章节；最小两篇（2611.07798 13,629 字符系统论文 / 2611.08398 25,978 字符设备论文）经中段抽查为真实正文（实现细节/控制回路），确认非摘要页。
- manifest 合并写入校验通过；WROTE=23>0。

## 评分与三关（第 5-6 步）
- 先抓全文再定稿。7 维加权定稿：主批 **8 A / 12 B / 3 C**（最高 XM4D 4.36 达 S 线但非重磅日按校准关记 A）。
- 门① 最大 Jaccard **0.074**（2611.08330 InstantHand vs 库内 2609.21498 VoxelTTO；<0.62，非同质）。
- 门② 纯价值 Top10 覆盖 **4 赛道**（神经渲染×3/感知与认知×3/重建与SLAM×2/化身与人体×2）<5 → **触发一次重筛**：剔除神经渲染赛道最低分 T²-Splat 3.575（与 ReferClaw 同分；按赛道冗余度与库内增量定位取舍——库内已有 MeshSplatting 直接前作），回补未覆盖核心赛道（触觉与多模态）B 级池最高分 多模态触觉显示 3.365 → 定稿 Top10 覆盖 **5 赛道** ≥5，通过（T²-Splat 仍入馆写 B 级笔记，仅不占 Top10 名额）。
- 门③ 当日最高 **4.36 < 库内近 30 天 Top10 均分 4.393**（窗口 2026-10-08~11-07、436 条入窗、现算）→ **非重磅日，无 S 级**；XM4D 4.36 达 S 线按校准关记 A（同 10-24 EgoHand/10-27 WFM/10-28 RacerGS 先例）。
- OUTDATED/SUPERSEDED **0 篇**。路线级观察：① 在线/前馈重建三篇同批（HIBS 在线 beta 泼溅、SM4RT 级联前馈 4D、InstantHand 前馈手部化身），「免优化前馈 + 在线增量」双路线并进；② 网格-高斯混合渲染两篇（T²-Splat 拓扑自适应、Gaussolve 减法范式、P-MGS 感知分配），与库内 GaMeS/Mani-GS/MeshSplatting 竞争白热化；③ 第一视角生态连续第三批强化（EgoGeneralist 统一模型 + ReferClaw 交互层 + 2611.07673 物体可供性），助手侧从感知走向交互闭环；④ 硬件类缺口仍仅 CVQPG + HoOPOE 两篇涉及近眼显示光学（本批触觉显示为台面式硬件增量，非近眼光学；波导/可变焦/Maxwellian/光场仍待补）。

## 产物（第 7-8 步）
- 报告 1 份 + 原子笔记 20 篇（grade≥B：8 A + 12 B；3 篇 C 仅入馆）+ MOC 1 份 + 总索引刷新 + 7 维表/scored/run_log 各 1 套。
- registry 808 → **831**（+23；备份 `papers/library/registry.jsonl.bak-20261107`；按 base_id 幂等）。
'''
open(f'papers/daily/{DATE}/run_log.md', 'w', encoding='utf-8').write(run_log_main)

# ---------- registry（先备份，幂等追加，in_top10 显式） ----------
reg_path = 'papers/library/registry.jsonl'
bak_path = reg_path.replace('.jsonl', '.jsonl.bak-20261107')
if not os.path.exists(bak_path):   # 重跑时保留首跑的追加前快照，勿覆盖
    shutil.copy(reg_path, bak_path)
rows = [json.loads(l) for l in open(reg_path, encoding='utf-8') if l.strip()]
have = {r['id'].split(':')[-1].split('v')[0] for r in rows}
added = 0
with open(reg_path, 'a', encoding='utf-8') as f:
    for p in MAIN:
        if p['id'] in have:
            continue
        entry = dict(id=f"arXiv:{p['id']}", title=p['title'], title_zh=p['title_zh'],
                     track=p['track'], date=DATE,
                     value=p['value'], grade=p['grade'], scores=p['scores'],
                     status=p['status'], evidence=p['evidence'], fetch_level=p['level'],
                     fulltext_chars=0, in_top10=(p['id'] in TOP10_IDS), batch=p['batch'],
                     announce_type=p['announce'], flags=[])
        f.write(json.dumps(entry, ensure_ascii=False) + '\n')
        added += 1
print(f'registry +{added}（现有 {len(rows)+added}）')

# ---------- 原子笔记（grade≥B；C 级仅入馆） ----------
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
for p in MAIN:
    if p['grade'] == 'C':
        continue
    fn = f"papers/notes/{p['id']}__{slugify(p['title'])}.md"
    if os.path.exists(fn):
        continue
    body = NOTE_TMPL.format(
        id=p['id'], title=p['title'], title_zh=p['title_zh'], track=p['track'], venue=p['venue'],
        date=DATE, value=f"{p['value']:.2f}", grade=p['grade'],
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

# ---------- 当日 MOC ----------
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

moc(MAIN, f'papers/MOC/MOC-{DATE}.md', f'MOC · {DATE}（11-06 公告批次）',
    '> 当日地图：**公告日 2026-11-06（周五）≠ 拉取日 2026-11-07（周六 13:38）**——诚实口径。API published 口径核验提交日 **11-04×5 / 11-05×30**（均早于公告日，非当日硬提交）。\n'
    '> 主批 XR 新稿 23 篇（8 A / 12 B / 3 C，**非重磅日无 S**，最高 XM4D 4.36 达 S 线按校准关记 A）；listing 386 篇摘要级 XR 命中 35 篇中 23 篇 XR（RSS 周六 skipDays 空源，listing 为唯一采集渠道；11-05 组复采 0 漏网）；全文 22×L0/FULL + 1×L0/PARTIAL（REACT 仅补充材料）。\n'
    '> 覆盖度三关：门① 0.074 / 门② 纯价值 Top10 仅 4 赛道触发一次重筛（T²-Splat 让位 多模态触觉显示）后定稿 Top10 覆盖 5 赛道 / 门③ 4.36 < 4.393（现算，436 条入窗）→ 非重磅日，无 S。\n'
    '> Top10（实数 10 篇）：XM4D 4.36 · AffineGS 4.15 · InstantHand 4.09 · HIBS 4.01 · EDGAR 3.98 · EgoGeneralist 3.97 · Gaussolve 3.83 · PVDepth 3.69 · ReferClaw 3.58 · 多模态触觉显示 3.37（门②回补）。')

# ---------- 报告 ----------
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
        L.append(f"- **公告类型**：{p['announce']}")
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
    L.append('- 抓取降级：23 篇候选串行 3s/篇全部 L0 命中（22 篇 FULL + 1 篇 PARTIAL：2611.08301 REACT 的 arXiv HTML 仅提供 Supplementary Material、ar5iv 无转换版，主文缺失，按摘要级评估并显式声明）；人工复核正文中段均含实质章节（排除 ar5iv 摘要页误判），无限流、无 L5、无 OCR、无伪造。')
    open(path, 'w', encoding='utf-8').writelines([x + '\n' for x in L])

report(TOP10,
       f'reports/XR-Daily-Report-{DATE}.md',
       f'XR 每日论文解读报告 · {DATE}（11-06 公告批次）',
       '## 一、执行摘要\n'
       '- **公告日 2026-11-06（周五）≠ 拉取日 2026-11-07（周六 13:38）**——诚实口径：本批处理的是 11-06 公告批次；API published 口径核验提交日 **11-04×5 / 11-05×30**（均早于公告日，非当日硬提交；RSS published 为公告时间戳非提交日）。\n'
       '- **数据源说明（本周特例）**：RSS 7 分类周六 skipDays 空源（lastBuildDate 2026-11-07 05:00 UTC，WROTE=0）→ **本批以 arXiv listing 为唯一采集渠道**；三源互证（listing 日期头 + API submittedDate/published + RSS 空源）确认 11-06 为最新公告日且 11-06 组 386 篇采集完整（逐分类 declared=got）。\n'
       '- **主批 XR 新稿 23 篇（8 A / 12 B / 3 C；非重磅日，Top10 实数 10 篇）**。Top10：**XM4D 4.36（哈佛/Berkeley，相机运动与 EDG 非刚性变形均化为旋转 QCQP 经 SDP 松弛+BM 黎曼阶梯获可证全局最优，Replica/TUM 相机精度第一，DyCheck/NVIDIA/Syn4D 新视图渲染全面第一，可扩展至 2000 帧并输出零件级 SE(3) 运动面向仿真就绪数字孪生；达 S 线但非重磅日按校准关记 A）** · AffineGS 4.15（实证单目深度先验存在区域相关分段线性视差畸变——K=1 全局对齐仅 58.9% inlier、K=5 达 92.7%——空间变化仿射矫正+法线感知梯度正则，MuSHRoom AbsRel 0.0551 vs DN-Splatter 0.3542、网格 F-score 0.71 vs 0.28） · InstantHand 4.09（UNIST，首个单图免测试时优化可动画高斯手部化身前馈框架，2.84s 构建/161 FPS，InterHand2.6M PSNR 26.21 dB 匹配逐主体优化基线，HanCo 零样本差距≤0.14 dB，代码开源） · HIBS 4.01（维尔茨堡大学，有界 beta kernel 形状参数作几何置信度 Dial+误差驱动重定位+闭式 LOD 合并，MipNeRF360 在线协议 +0.81 dB、优化时间最多省 40%） · EDGAR 3.98（KAIST，合成失败三元组训练条件扩散精化高斯化身并蒸馏回 3D，用户研究整体偏好率 96.67%，一次性精化 5–16.6 分钟且渲染帧率保持基线 2% 以内） · EgoGeneralist 3.97（莫纳什+蚂蚁+中科院自动化所，Wan2.2-A14B 适配的统一第一视角动作-视频模型，五任务六模式，EgoDex PSNR 30.35/手部 Abs-MPJPE 27.73mm/HOT3D Reach@5cm 77.8%） · Gaussolve 3.83（东京大学，首个「减法」混合渲染范式：Neural Dissolve Field 选择性溶解不一致网格+连续透射率融合回填残差高斯，ML-Hypersim-AI 36.89 dB、高斯数较 MeshGS 少 59.5%、241 FPS） · PVDepth 3.69（北大+鹏城，PanoCARLA 全景 RGB-D 视频数据集 126.7K 帧+PSNI/CRTM 双 ERP 适配，AbsRel 0.199 优于 DepthCrafter FT 0.232，代码数据全开源） · ReferClaw 3.58（NUS/USTC，第一视角流式助手以成本感知澄清提问消解意图，BuddyVQA 74.3% 超 Clarify-or-Answer 15.8 点、提问率仅 18.6%） · 多模态触觉显示 3.37（Imperial/MIT/Duke-NUS，无泵颗粒堵塞与热皮肤整合的台式双模态显示，刚度 0.63→2.38 N/mm 可控、10–50°C、闭环 ±0.2°C；**门②回补项**）。\n'
       '- **覆盖 5 赛道**：感知与认知×3 / 重建与SLAM×2 / 神经渲染×2 / 化身与人体×2 / 触觉与多模态×1（全批 7 赛道）。\n'
       '- **覆盖度三关**：门① 0.074（InstantHand vs 库内 VoxelTTO，<0.62 通过）；门② 纯价值 Top10 仅 4 赛道（神经渲染×3 冗余）→ **触发一次重筛**（剔除 T²-Splat 3.575、回补触觉与多模态赛道 多模态触觉显示 3.365），定稿 Top10 覆盖 5 赛道 ≥5（通过）；门③ 当日最高 4.36 < 库内近 30 天 Top10 均分 4.393（现算，436 条入窗）→ **非重磅日，无 S 级**（XM4D 4.36 达 S 线按校准关记 A，未拔高）。\n'
       '- **全文证据**：23 篇候选 **22 篇 L0/FULL**（13,629–179,859 字符）+ **1 篇 L0/PARTIAL**（2611.08301 REACT：arXiv HTML 仅 Supplementary Material、ar5iv 无转换版，摘要级评估并显式声明；人工复核正文中段排除 ar5iv 摘要页误判）。\n'
       '- **无 backfill**：RSS 周六 skipDays 空源，无旧稿 replace/cross 再公告可收（listing 公告日组天然只含新提交，与 10-18 确认机制一致）。',
       10,
       ['- 门①（同质去重）：最大 Jaccard 0.074 < 0.62，通过，无同质重复。',
        '- 门②（赛道覆盖）：纯价值 Top10 覆盖 4 赛道（神经渲染×3/感知与认知×3/重建与SLAM×2/化身与人体×2）<5 → 触发一次重筛——剔除神经渲染赛道最低分 T²-Splat 3.575（与 ReferClaw 同分，按赛道冗余度与库内增量定位取舍：库内已有其直接前作 MeshSplatting；仍入馆写 B 级笔记仅不占名额，同 11-04 SHield/11-06 BudgetSplat 先例），回补未覆盖核心赛道（触觉与多模态）B 级池最高分 多模态触觉显示 3.365 → 定稿 Top10 覆盖 5 赛道（感知与认知×3/重建与SLAM×2/神经渲染×2/化身与人体×2/触觉与多模态×1）≥5，通过；全批 7 赛道。',
        '- 门③（价值天花板）：当日最高分 4.36 < 库内近 30 天 Top10 均分 4.393（现算，436 条入窗）→ **非重磅日，无 S 级**；XM4D 4.36 达 S 线（≥4.2）按校准关记 A（同 10-24 EgoHand/10-27 WFM/10-28 RacerGS 先例）；A 级 8 篇、B 级 12 篇（含 1 篇门②回补）、C 级 3 篇（仅入馆不解读）。',
        '- 低量日不凑数原则复核：本批 grade≥B 共 20 篇，Top10 取实数 10 篇（8 A + 1 B + 1 门②回补 B），余 10 篇 B 级入馆写笔记，3 篇 C 级仅入馆，未降格凑数。',
        '- OUTDATED/SUPERSEDED 0 篇。\n'])

# ---------- MOC-总索引刷新 ----------
moc_path = 'papers/MOC/MOC-总索引.md'
h = open(moc_path, encoding='utf-8').read()
n0 = len(h)

def rep(old, new, tag):
    global h
    assert old in h, f'ANCHOR NOT FOUND: {tag}'
    h = h.replace(old, new, 1)

# 7.1 头部计数与批次枚举
rep('累计 **808 篇**；跨度 2026-09-15 ~ 2026-11-05',
    '累计 **831 篇**；跨度 2026-09-15 ~ 2026-11-06', 'head-count')
rep('**backfill-1106:6（11-05 公告 RSS 混入旧稿 replace/cross 再公告，首次入馆）**；',
    '**backfill-1106:6（11-05 公告 RSS 混入旧稿 replace/cross 再公告，首次入馆）** · '
    '**2026-11-07:23（11-06 公告批次真新提交，非重磅日无S；RSS 周六 skipDays 空源、listing 为唯一采集渠道，摘要级命中 35 篇中 23 篇 XR）**；', 'batch-list')
rep('**11-06 周五处理 11-05 公告批次（12 篇 XR 新稿 1S/5A/6B 重磅日 + backfill-1106 补录 6 篇 5A/1B）**。',
    '**11-06 周五处理 11-05 公告批次（12 篇 XR 新稿 1S/5A/6B 重磅日 + backfill-1106 补录 6 篇 5A/1B）**；'
    '**11-07 周六处理 11-06 公告批次（23 篇 XR 新稿 8A/12B/3C，非重磅日无S；RSS 周六空源、listing 唯一采集渠道）**。',
    'narrative')

# 7.2 追加 11-07 状态注记（在 11-06 注记后）
note07 = ('> **状态注记（2026-11-07）**：周六 13:38，处理 **2026-11-06（周五）公告批次**（公告日≠拉取日，诚实口径；API published 口径核验提交日 **11-04×5 / 11-05×30**，RSS published 为公告时间戳非提交日）。'
 '漏网对账（先于拉取，TARGET_DAY=2026-11-05）：listing 7 分类最新公告日均为 **11-06**（无漏跑公告日）；11-05 组复采逐分类 **declared=got**（CV 148/GR 7/HC 29/MM 6/RO 62/AI 217/IV 8，477 槽位），未入馆 **386 篇**摘要级复核 **10 篇命中均为 11-06 运行已剔非 XR（与上批清单逐篇一致）→ 0 漏网、无 backfill**；**11-06 组 386 篇唯一论文**（CV 138/GR 11/HC 22/MM 2/RO 81/AI 198/IV 6，458 槽位，全部未入馆）摘要级 XR 命中 **35 篇**。'
 '**数据源特例**：RSS 7 分类 **周六 skipDays 空源**（lastBuildDate 2026-11-07 05:00 UTC，`fetch_rss.py` WROTE=0，非代理故障）→ **listing 为唯一采集渠道**；三源互证（listing 日期头 + API submittedDate/published + RSS 空源）。'
 '主批甄别 **XR 核心/强相关 23 篇**（剔非 XR 12 篇：VLM 直推适配×2/自动驾驶宽视角合成/视频扩散 token 剪枝/事件相机 LED 跟踪（无人机）/跨机器人抓取评测/人形机器人社交触摸/可变接触3D物体放置/人形机器人运动/巡视器导航栈/移动操作示范增广/人-人形交互）；全文 **22 篇 L0/FULL + 1 篇 L0/PARTIAL**（2611.08301 REACT：arXiv HTML 仅 Supplementary Material、ar5iv 无转换版，主文缺失，摘要级评估并显式声明）。'
 'Top10（**实数 10 篇**）：最高 **4.36（XM4D，哈佛/Berkeley，可证全局最优 4D 重建），非重磅日无 S**（4.36 达 S 线按校准关记 A）；覆盖 5 赛道（感知与认知×3/重建与SLAM×2/神经渲染×2/化身与人体×2/触觉与多模态×1；全批 7 赛道）。'
 '三关：门① max Jaccard **0.074**（2611.08330 vs 库内 2609.21498 VoxelTTO）；门② 纯价值 Top10 仅 4 赛道（神经渲染×3 冗余）→ **触发一次重筛**（剔除 T²-Splat 3.575、回补触觉与多模态赛道 多模态触觉显示 3.365）后定稿 Top10 覆盖 5 赛道 ≥5（通过）；门③ 当日最高 4.36 < 库内近 30 天 Top10 均分 **4.393**（436 条入窗，现算）→ **非重磅日，无 S 级**；OUTDATED 0。'
 'registry 808 → **831**（+23，无 backfill）。详见 [运行报告](../../reports/XR-Daily-Report-2026-11-07.md) 与 [MOC-2026-11-07](./MOC-2026-11-07.md)。\n')
anchor_end = '[Backfill 报告](../../reports/XR-Backfill-Report-backfill-1106.md)。'
i = h.find(anchor_end)
assert i >= 0, 'ANCHOR NOT FOUND: note1106-end'
j = h.find('\n', i) + 1
h = h[:j] + note07 + h[j:]

# 7.3 速查入口
rep('| 最新一期 | [MOC · 2026-11-06](./MOC-2026-11-06.md) |',
    '| 最新一期 | [MOC · 2026-11-07](./MOC-2026-11-07.md) |', 'quick-latest')
rep('| 上一期 | [MOC · 2026-11-05](./MOC-2026-11-05.md) |',
    '| 上一期 | [MOC · 2026-11-06](./MOC-2026-11-06.md) |', 'quick-prev')
rep('（现有 482 篇）', '（现有 502 篇）', 'quick-notes')
rep('| 最新运行状态 | [运行报告 2026-11-06](../../reports/XR-Daily-Report-2026-11-06.md)（11-05 公告批次 12 篇 1S/5A/6B 重磅日 + backfill-1106 补录 6 篇 5A/1B；listing 398 篇+RSS 两渠道互证 22 篇中 12 篇 XR，RSS 漏网 0 篇；全文 18×L0/FULL；门② 触发一次重筛回补 VR HIIT，Top10 实数 10 篇覆盖 5 赛道） |',
    '| 最新运行状态 | [运行报告 2026-11-07](../../reports/XR-Daily-Report-2026-11-07.md)（11-06 公告批次 23 篇 8A/12B/3C 非重磅日无S；RSS 周六 skipDays 空源、listing 唯一采集渠道，386 篇摘要级命中 35 篇中 23 篇 XR；11-05 组复采 0 漏网；全文 22×L0/FULL + 1×L0/PARTIAL；门② 触发一次重筛回补多模态触觉显示，Top10 实数 10 篇覆盖 5 赛道；门③ 现算 4.393） |', 'quick-status')

# 7.4 批次索引表追加行
row_main = ('| 2026-11-07 | [MOC-2026-11-07](./MOC-2026-11-07.md) | XR 23（Top10 实数 10）· 8A/12B/3C · 非重磅日（无S） | '
            '11-06 公告批次真新提交 23 篇（11-04×5/11-05×30 提交）；RSS 周六空源、listing 唯一采集渠道，386 篇摘要级命中 35 篇中 23 篇 XR；全文 22×L0/FULL + 1×L0/PARTIAL |')
rep('| backfill-1106 | [MOC-backfill-1106](./MOC-backfill-1106.md) | 补录 6（5A/1B）· 非当日新提交 | 11-05 公告 RSS 混入旧稿 replace/cross 再公告 6 篇（2401/2506/2511/2604/2607/2611） |',
    '| backfill-1106 | [MOC-backfill-1106](./MOC-backfill-1106.md) | 补录 6（5A/1B）· 非当日新提交 | 11-05 公告 RSS 混入旧稿 replace/cross 再公告 6 篇（2401/2506/2511/2604/2607/2611） |\n'
    + row_main, 'batch-table')

# 7.5 追加 Top10 段（文件尾）
seg = '\n### 2026-11-07 新增（Top10 实数 10 篇：8 A + 1 B + 1 门②回补 B，非重磅日无 S）\n\n| # | 论文 | 赛道 | 分值 | 等级 | 证据 |\n|---:|---|---|---:|---|---|\n'
for i2, pid in enumerate(TOP10_ORDER, 1):
    p = next(x for x in MAIN if x['id'] == pid)
    seg += f"| {i2} | {esc(p['title_zh'])} | {p['track']} | {p['value']:.2f} | {p['grade']} | {p['evidence']} |\n"
h = h.rstrip() + '\n' + seg

# 7.6 页脚计数
rep('*最后更新：2026-11-06（11-05 公告批次：12 篇 XR 新稿 1S/5A/6B 重磅日 + backfill-1106 补录 6 篇 5A/1B；listing 398 篇+RSS 两渠道互证 22 篇中 12 篇 XR，RSS 漏网 0 篇；全文 18×L0/FULL；门② 触发一次重筛（BudgetSplat→VR HIIT）；门③ 现算 4.363，当日最高 4.57 达重磅日线，1 篇 S） · 库内 **808 篇** · 原子笔记 **482 篇** · MOC 42 份',
    '*最后更新：2026-11-07（11-06 公告批次：23 篇 XR 新稿 8A/12B/3C 非重磅日无S；RSS 周六 skipDays 空源、listing 唯一采集渠道，386 篇摘要级命中 35 篇中 23 篇 XR；11-05 组复采 0 漏网；全文 22×L0/FULL + 1×L0/PARTIAL（REACT 仅补充材料）；门② 触发一次重筛（T²-Splat→多模态触觉显示）；门③ 现算 4.393，当日最高 4.36 未达重磅日线，XM4D 达 S 线按校准关记 A） · 库内 **831 篇** · 原子笔记 **502 篇** · MOC 43 份',
    'footer')

open(moc_path, 'w', encoding='utf-8').write(h)
print('MOC-总索引 refreshed（%d -> %d chars）' % (n0, len(h)))
print('DONE')
