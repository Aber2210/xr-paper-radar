# -*- coding: utf-8 -*-
"""2026-10-27 产物生成：主批（10-26 公告批次 7 篇）+ backfill-1027（旧稿再公告 8 篇）。
消费 data/scored_1027.json；registry 幂等追加（先备份）；生成笔记/MOC/报告并刷新总索引。"""
import json, os, shutil, glob

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
os.chdir(ROOT)
D = json.load(open('data/scored_1027.json', encoding='utf-8'))
MAIN, BF = D['main'], D['backfill']
DATE, BFB = '2026-10-27', 'backfill-1027'
GATE3 = 4.416          # 门③ 现算均分（窗口 2026-09-27~10-27，421 条入窗）
TODAY_MAX = MAIN[0]['value']  # 3.85

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
    '批次：2026-10-27（**2026-10-26（周一）公告批次**，覆盖周末 10-24/10-25 提交积压；公告日 10-26 ≠ 拉取日 10-27 02:30，诚实口径）。\n'
    '候选池 7 篇：listing 对账 10-26 公告组 358 篇 → 摘要级 XR 命中 18 篇（与 RSS 命中集合完全一致，两渠道互证）→ 甄别 XR 核心/强相关 **7 篇**入评分池，11 篇非 XR 误命中剔除（机器人演示分割 2610.31801 / 机器人 VLA 策略 2610.31845 / 航空 GNSS-IMU 完整性 2610.32259 / 光子逆设计 2610.32485 / 脑 CT-MR 合成 2610.32491 / 机器人超声 2610.32525 / 自动驾驶分割 2610.32612 / MLLM 视觉 token 预算 2610.32664 / 无人机 VLN 2610.32697 / 机器人 OCT 2610.32961 / 灵巧手数据采集 2610.32969）。\n'
    'RSS 同批另混入 8 篇旧稿 replace/cross 再公告（单列 backfill-1027）+ 4 篇库内 v2 再公告剔除。\n'
    '全文：7 篇候选 **6 篇 L0/FULL + 1 篇 L1/PARTIAL**（2610.32232 Virtual Placebo，ar5iv 仅返回摘要页无正文章节，按摘要级评估并显式声明）；先抓全文再定稿。\n'
    '覆盖度三关：门① 最大 Jaccard **0.065**（AudioLift vs 库内 Kandinsky S2V 1.0，<0.62 通过）；门② 覆盖 **6 赛道**（化身与人体/神经渲染/感知与认知/交互与输入/评估与数据集/渲染与显示，≥5 通过）；门③ 当日最高 **3.85 < 库内近 30 天 Top10 均分 4.416**（421 条入窗，现算）→ **非重磅日、无 S 级**，未拔高、未凑数（候选仅 7 篇 grade≥B，Top10 按实数 7 篇列示）。',
    len(MAIN))

seven_table(BF, f'papers/daily/{BFB}/7dim-table.md',
    f'{BFB} 全量 7 维度对比表（参考）',
    '批次：backfill-1027（**10-26 公告批次中 RSS 混入的旧稿 replace/cross 再公告**（首次入馆；原始投稿月 2412/2503/2601/2606/2607/2608/2610）；均非 10-26/10-27 当日新提交，诚实口径单独编号）。\n'
    '候选 8 篇：2412.01090 STATIC（视频深度，v2 2025-11）/ 2503.21288 FH-HBTS（触觉遥操作，v2 2025-06）/ 2601.00705 TopoGS-SLAM / 2606.15417 TAG（第一视角动作图）/ 2607.01202 World from Motion（Stanford+NVIDIA）/ 2608.05663 Vorch-Streamer（流式化身）/ 2608.16499 OccamView（主动 3DGS）/ 2610.25068 LENS（FPGA 场景记忆）。全部 L0/FULL 全文后定稿。\n'
    '门③ 对 backfill 不适用；本批不参与当日「重磅日」判定。门① 最大 Jaccard 0.067（World from Motion vs ProDyGS，<0.62 通过）；门② 覆盖 6 赛道（神经渲染/重建与SLAM/化身与人体/感知与认知/系统与平台/触觉与多模态）。\n'
    '注：World from Motion 加权 4.27 已达 S 线（≥4.2），但当日最高分 4.27 < 库内近 30 天 Top10 均分 4.416 → 非重磅日，按校准关记 A 级（同 10-24 EgoHand 先例；分数如实保留）。',
    len(BF))

# ---------- 2. scored.md + run_log.md ----------
def scored_md(papers, path, title, extra):
    L = [f'# {title}\n', extra + '\n', '| 排名 | arXiv | 标题 | 赛道 | 总分 | 等级 | 证据 | 公告类型 |',
         '|---|---|---|---|---|---|---|---|']
    for i, p in enumerate(papers, 1):
        L.append(f"| {i} | {p['id']} | {esc(p['title_zh'])} | {p['track']} | {p['value']:.2f} | {p['grade']} | {p['evidence']} | {p['announce']} |")
    open(path, 'w', encoding='utf-8').writelines([x + '\n' for x in L])

scored_md(MAIN, f'papers/daily/{DATE}/scored.md', f'{DATE} 评分明细',
    '评分口径：7 维加权 IMP0.20·NOV0.20·TEC0.15·EXP0.15·PER0.15·TRL0.08·REP0.07；分档 S≥4.2 / A3.6–4.2 / B3.0–3.6 / C<3.0。全部基于全文证据定稿（2610.32232 为 PARTIAL 摘要级）。\n'
    f'覆盖度三关：门① 最大 Jaccard 0.065 < 0.62（通过，非同质）；门② 覆盖 6 赛道 ≥ 5（通过）；门③ 当日最高 3.85 < 库内近 30 天 Top10 均分 4.416（现算，421 条入窗）→ 非重磅日、无 S 级（校准关，不触发重筛）。\n'
    '低量日处理：XR 新稿仅 7 篇且全部 grade≥B，Top10 按实数 7 篇列示，**未凑数至 10**。OUTDATED/SUPERSEDED 0 篇。')
scored_md(BF, f'papers/daily/{BFB}/scored.md', f'{BFB} 评分明细',
    '评分口径同上。本批为旧稿 replace/cross 再公告首次入馆（非当日新提交），门③ 不适用。\n'
    '门① 最大 Jaccard 0.067 < 0.62（通过）；门② 覆盖 6 赛道 ≥ 5（通过）；OUTDATED/SUPERSEDED 0 篇。')

run_log_main = f'''# {DATE} 执行日志

## 数据源与对账（第 1-3 步）
- **漏网对账（先于拉取）**：`scripts/audit_gap_listing.py`（TARGET_LO=2026-10-23，上一批次公告日）7 分类采集。listing 最新公告日 = **2026-10-26**（周一，周末积压公告 00:00 UTC=08:00 北京时间已释放）；10-24/10-25 周末无公告日段。10-23 组 411 篇（上批 10-26 已全量复核 0 漏网，本次复采一致）；**10-26 组 358 篇全部未入馆**（新公告批次）。
- **摘要级 XR 过滤**：`scripts/filter_missed_xr_abstract.py`（MIN_DAY=2026-10-26）→ 358 篇取回 358 条 API 元数据，XR 命中 **18 篇**（全 2610.* 新提交）。
- **RSS 主渠道交叉验证**：`scripts/fetch_rss.py` 7 分类全量去重 581 条 → KW 命中 30 条 = **18 篇 2610.* 真新提交（与 listing 命中集合逐篇一致）+ 8 篇旧稿 replace/cross 再公告 + 4 篇库内 v2 再公告**。两渠道互证无矛盾。
- **API 探针**：export.arxiv.org / arxiv.org/api/query 均可达（200）；`submittedDate` 前沿停滞 10-22，真实新增由 RSS+listing 双渠道获得。

## 甄别（第 3 步）
- 主批 XR 核心/强相关 **7 篇**入评分池；剔非 XR **11 篇**（机器人演示分割/机器人 VLA 策略/航空 GNSS-IMU 完整性/光子逆设计/脑 CT-MR 合成/机器人超声/自动驾驶分割/MLLM 视觉 token/无人机 VLN/机器人 OCT/灵巧手数据采集）。
- 旧稿 replace/cross 再公告 8 篇 → **backfill-1027**（首次入馆，单独编号，绝不混入当日新论文）。
- 库内 v2 再公告 4 篇剔除（2601.14895/2610.27712/2610.28402/2610.29014）。

## 全文抓取（第 4 步）
- 15 篇候选（主批 7 + backfill 8）跑 `scripts/fetch_fulltext.py`，严格串行 3s/篇：**14 篇 L0/FULL**（45,727–126,513 字符）+ **1 篇 L1/PARTIAL**（2610.32232 Virtual Placebo：ar5iv 仅返回摘要页、无 Methods/Results 正文章节 → 改判 PARTIAL，按摘要级评估并显式声明，禁止脑补）。无限流/降级/伪造。
- manifest 合并写入校验通过；WROTE=15>0。

## 评分与三关（第 5-6 步）
- 先抓全文再定稿。7 维加权定稿：主批 4 A / 3 B（最高 3.85 PixGR/HEALPix 并列）；backfill 4 A / 4 B（最高 4.27 World from Motion）。
- 门① 最大 Jaccard **0.065**（AudioLift vs 2610.19290 Kandinsky S2V 1.0；<0.62，无非质同源）。
- 门② 主批覆盖 **6 赛道**；backfill 覆盖 **6 赛道**（均 ≥5）。
- 门③ 当日最高 **4.27（backfill WFM）/ 3.85（主批）< 库内近 30 天 Top10 均分 4.416**（窗口 2026-09-27~10-27、421 条入窗、现算）→ **非重磅日、无 S 级**；WFM 4.27 达 S 线按校准关记 A（同 10-24 EgoHand 先例）。三关全过，**未触发重筛**。
- OUTDATED/SUPERSEDED **0 篇**。路线级观察：① 生成式中间表示进入化身/4D 重建主线（AudioLift/WFM）；② 前馈 3DGS 重建的生成式解码变体（PixGR）与 budgeted 压缩线并行；③ 晕动症/眼动仪评估两个「研究基础设施」方向同日出现（32019/32915）。

## 产物（第 7-8 步）
- 报告 2 份（主报告 + backfill 报告）+ 原子笔记 15 篇 + MOC 2 份 + 总索引刷新 + 7 维表/scored/run_log 各 2 套。
- registry 618 → **633**（+7 主批 +8 backfill；备份 `papers/library/registry.jsonl.bak-20261027`；按 base_id 幂等）。
'''
open(f'papers/daily/{DATE}/run_log.md', 'w', encoding='utf-8').write(run_log_main)

run_log_bf = f'''# {BFB} 执行日志

- **来源**：10-26 公告批次 RSS 混入的旧稿 replace/cross 再公告 8 篇（首次入馆）：2412.01090（replace）/ 2503.21288（replace）/ 2601.00705（replace）/ 2606.15417（replace）/ 2607.01202（replace-cross）/ 2608.05663（replace）/ 2608.16499（replace-cross）/ 2610.25068（replace-cross）。原始投稿月 2024-12 ~ 2026-10，v1→v2 跨度 2025-06 ~ 2026-10。
- **甄别**：8 篇全部 XR 相关（视频深度/触觉遥操/高斯 SLAM/第一视角理解/4D 重建/流式化身/主动重建/边缘场景记忆），无非 XR 剔除。
- **全文**：8 篇全部 **L0/FULL**（50,425–81,134 字符），串行 3s，无限流/降级。
- **评分**：4 A / 4 B；门① 最大 Jaccard 0.067；门② 6 赛道；门③ 不适用（backfill）。
- **诚实口径**：本批全部标注 `batch={BFB}`、`orig_window`，绝不混入「当日新论文」表。
'''
open(f'papers/daily/{BFB}/run_log.md', 'w', encoding='utf-8').write(run_log_bf)

# ---------- 3. registry（先备份，幂等追加） ----------
reg_path = 'papers/library/registry.jsonl'
shutil.copy(reg_path, reg_path.replace('.jsonl', '.bak-20261027'))
rows = [json.loads(l) for l in open(reg_path, encoding='utf-8') if l.strip()]
have = {r['id'].split(':')[-1].split('v')[0] for r in rows}
added = 0
with open(reg_path, 'a', encoding='utf-8') as f:
    for p in MAIN + BF:
        if p['id'] in have:
            continue
        entry = dict(id=f"arXiv:{p['id']}", title=p['title'], title_zh=p['title_zh'],
                     track=p['track'], date=(DATE if p in MAIN else '2026-10-26'),
                     value=p['value'], grade=p['grade'], scores=p['scores'],
                     status=p['status'], evidence=p['evidence'], fetch_level=p['level'],
                     fulltext_chars=0, in_top10=True, batch=p['batch'],
                     announce_type=p['announce'], flags=[])
        if p in BF:
            entry['orig_window'] = f"{BFB}：10-26 公告批次 RSS 混入旧稿 replace/cross 再公告（首次入馆）；均非当日新提交"
            entry['in_top10'] = False
        f.write(json.dumps(entry, ensure_ascii=False) + '\n')
        added += 1
print(f'registry +{added}（现有 {len(rows)+added}）')

# ---------- 4. 原子笔记 ----------
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
for p in MAIN + BF:
    fn = f"papers/notes/{p['id']}__{slugify(p['title'])}.md"
    if os.path.exists(fn):
        continue
    body = NOTE_TMPL.format(
        id=p['id'], title=p['title'], title_zh=p['title_zh'], track=p['track'], venue=p['venue'],
        date=(DATE if p in MAIN else '2026-10-26'), value=f"{p['value']:.2f}", grade=p['grade'],
        evidence=p['evidence'], status=p['status'],
        IMP=p['scores']['IMP'], NOV=p['scores']['NOV'], TEC=p['scores']['TEC'], EXP=p['scores']['EXP'],
        PER=p['scores']['PER'], TRL=p['scores']['TRL'], REP=p['scores']['REP'],
        level=p['level'], batch=p['batch'], announce=p['announce'],
        in_top10=('true' if p in MAIN else 'false'),
        tags=', '.join(p['tags']), conclusion=p['conclusion'], problem=p['problem'],
        method=p['method'], experiments=p['experiments'], innovation=p['innovation'],
        limits=p['limits'], relation=p['relation'], repro=p['repro'], action=p['action'])
    open(fn, 'w', encoding='utf-8').write(body)
print('notes written:', len(MAIN) + len(BF))

# ---------- 5. 当日 MOC ----------
def moc(papers, path, title, intro, batch):
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

moc(MAIN, f'papers/MOC/MOC-{DATE}.md', f'MOC · {DATE}（10-26 公告批次）',
    '> 当日地图：**公告日 2026-10-26（周一，覆盖周末 10-24/10-25 提交积压）≠ 拉取日 2026-10-27（周二 02:30）**——诚实口径，非当日硬提交。\n'
    '> 主批 XR 新稿 7 篇（4 A / 3 B，无 S——非重磅日）；listing 与 RSS 两渠道互证 18 篇真新提交中 7 篇 XR 核心/强相关；全文 6 L0/FULL + 1 L1/PARTIAL。\n'
    '> 覆盖度三关：门① 0.065 / 门② 6 赛道 / 门③ 3.85 < 4.416（现算）→ 非重磅日无 S，未凑数（Top10 实数 7 篇）。',
    DATE)
moc(BF, f'papers/MOC/MOC-{BFB}.md', f'MOC · {BFB}（旧稿再公告补录）',
    '> 本批为 **backfill**：10-26 公告批次 RSS 混入的旧稿 replace/cross 再公告 8 篇首次入馆（原始投稿月 2412~2610），**均非当日新提交**。\n'
    '> 4 A / 4 B；World from Motion 4.27 达 S 线但因非重磅日按校准关记 A。门① 0.067 / 门② 6 赛道 / 门③ 不适用。',
    BFB)

# ---------- 6. 报告 ----------
def report(papers, path, title, header, batch_label):
    L = [f'# {title}\n', header + '\n', '## 二、排行榜（按加权降序）\n',
         '| 排名 | 论文 | 赛道 | 总分 | 等级 | 证据 | 落后标记 |', '|---|---|---|---|---|---|---|']
    for i, p in enumerate(papers, 1):
        mark = '⛔ OUTDATED' if p['status'] != 'CURRENT' else '—'
        L.append(f"| {i} | {esc(p['title_zh'])}（{p['id']}） | {p['track']} | {p['value']:.2f} | {p['grade']} | {p['evidence']} | {mark} |")
    L.append('\n## 三、逐篇深度解读\n')
    for i, p in enumerate(papers, 1):
        L.append(f"### 第 {i} 章 · {esc(p['title_zh'])}（{p['id']}，{p['value']:.2f} {p['grade']}，{p['evidence']}）\n")
        L.append(f"- **赛道 / 场合**：{p['track']} / {p['venue']}")
        L.append(f"- **公告类型**：{p['announce']}" + (f"（{p['orig_window']}）" if p.get('orig_window') else ''))
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
    L.append('- 门①（同质去重）：最大 Jaccard 0.065 < 0.62，通过，无同质重复。')
    L.append('- 门②（赛道覆盖）：本批覆盖 6 个标准赛道（≥5），通过，无冷门高价值候选可回补。')
    L.append('- 门③（价值天花板）：当日最高分 3.85（主批）/ 4.27（backfill WFM）< 库内近 30 天 Top10 均分 4.416（现算）→ 非重磅日、无 S 级，未拔高、未凑数。')
    L.append('- 三关均未触发重筛；OUTDATED/SUPERSEDED 0 篇。\n')
    L.append('## 六、附录：证据等级分布与抓取记录\n')
    nf = sum(1 for p in papers if p['evidence'] == 'FULL')
    L.append(f'- FULL {nf} 篇；PARTIAL {len(papers)-nf} 篇（2610.32232 ar5iv 仅摘要页，摘要级评估并显式声明）；ABSTRACT_ONLY 0 篇。')
    L.append('- 抓取降级：无 L5；无 OCR；无伪造。串行 3s/篇，无限流。')
    open(path, 'w', encoding='utf-8').writelines([x + '\n' for x in L])

report(MAIN, f'reports/XR-Daily-Report-{DATE}.md',
    f'XR 每日论文解读报告 · {DATE}（10-26 公告批次）',
    '## 一、执行摘要\n'
    f'- **公告日 2026-10-26（周一，周末 10-24/10-25 提交积压释放）≠ 拉取日 2026-10-27（周二 02:30）**——诚实口径：本批处理的是 10-26 公告批次，非当日硬提交。\n'
    '- **主批 XR 新稿 7 篇（4 A / 3 B，无 S 级）**：PixGR 3.85（前馈 3DGS 像素空间生成解码）· 三头显眼动仪诊断 3.77 · AudioLift 3.70（音频驱动全头高斯化身）· HEALPix 球面 INR 全景压缩 3.70 · Present Drawing 3.34（UIST 26 化身绘画事件）· Gaze Under Strain 3.27（VRST 26 晕动症眼动）· Virtual Placebo 3.20（PARTIAL，VR 安慰剂对照综述）。\n'
    '- **覆盖 6 赛道**：神经渲染 / 评估与数据集 / 化身与人体 / 渲染与显示 / 交互与输入 / 感知与认知。\n'
    '- **覆盖度三关**：门① 0.065；门② 6 赛道；门③ 3.85 < 4.416（现算）→ **非重磅日、无 S 级**。候选仅 7 篇，**未凑数至 10**。\n'
    '- **全文证据**：6 篇 L0/FULL + 1 篇 L1/PARTIAL（2610.32232，ar5iv 仅摘要页）。\n'
    '- **同批 backfill-1027**：RSS 混入旧稿 replace/cross 再公告 8 篇首次入馆（4 A / 4 B，最高 World from Motion 4.27 达 S 线按校准关记 A），详见 [XR-Backfill-Report-1027.md](XR-Backfill-Report-1027.md)。',
    DATE)

report(BF, f'reports/XR-Backfill-Report-{BFB}.md',
    f'XR Backfill 补录报告 · {BFB}（旧稿再公告）',
    '## 一、执行摘要\n'
    '- **批次性质**：backfill（非当日新提交）——10-26 公告批次中 RSS 混入的旧稿 replace/cross 再公告 8 篇，首次入馆；原始投稿月 2024-12 ~ 2026-10。\n'
    '- **补录 8 篇（4 A / 4 B）**：World from Motion 4.27（Stanford+NVIDIA，单目 4D 生成式重建，达 S 线因非重磅日记 A）· TopoGS-SLAM 3.92（高斯 SLAM 致密化重构）· Vorch-Streamer 3.85（实时流式化身）· LENS 3.65（FPGA 边缘场景记忆）· TAG 3.50（第一视角时序动作图）· FH-HBTS 3.15（牙科触觉遥操）· STATIC 3.15（视频深度一致性）· OccamView 3.00（主动 3DGS 视角选择）。\n'
    '- **覆盖 6 赛道**；门① 0.067；门③ 对 backfill 不适用；OUTDATED 0。\n'
    '- **诚实口径**：全部条目 `batch=backfill-1027` + `orig_window` 标注，绝不混入「当日新论文」。',
    BFB)

# ---------- 7. MOC-总索引刷新 ----------
moc_path = 'papers/MOC/MOC-总索引.md'
h = open(moc_path, encoding='utf-8').read()

# 7.1 头部计数与批次列表
h = h.replace('文献库：`papers/library/registry.jsonl`（累计 **618 篇**；跨度 2026-09-15 ~ 2026-10-22',
              '文献库：`papers/library/registry.jsonl`（累计 **633 篇**；跨度 2026-09-15 ~ 2026-10-26')
h = h.replace('**2026-10-24:17（10-23 公告批次真新提交，非重磅日无S；listing 摘要级对账补齐 RSS 漏网 5 篇）** · **backfill-1024:4（10-23 公告 RSS 混入旧稿 replace 再公告，首次入馆）**；',
              '**2026-10-24:17（10-23 公告批次真新提交，非重磅日无S；listing 摘要级对账补齐 RSS 漏网 5 篇）** · **backfill-1024:4（10-23 公告 RSS 混入旧稿 replace 再公告，首次入馆）** · **2026-10-27:7（10-26 周一公告批次·周末积压，真新提交，非重磅日无S；listing+RSS 两渠道互证 18 篇中 7 篇 XR）** · **backfill-1027:8（10-26 公告 RSS 混入旧稿 replace/cross 再公告，首次入馆）**；')
h = h.replace('**10-25 周日状态日 0 新稿**（listing 无 10-24/10-25 公告日段，10-23 公告组复核 0 漏网））。',
              '**10-25 周日状态日 0 新稿**（listing 无 10-24/10-25 公告日段，10-23 公告组复核 0 漏网）；10-26 周一凌晨状态日 0 新稿（周末积压公告时刻 08:00 晚于运行时刻）；**10-27 周二处理 10-26 公告批次（周末积压，7 篇 XR 新稿 + backfill-1027 补录 8 篇）**。')

# 7.2 追加 10-27 状态注记（在 10-26 注记后）
note27 = ('> **状态注记（2026-10-27）**：周二 02:30，处理 **2026-10-26（周一）公告批次**（周末 10-24/10-25 提交积压、周一 00:00 UTC 释放；公告日≠拉取日，诚实口径）。'
 '漏网对账（TARGET_LO=10-23）：listing 7 分类最新公告日 **10-26**（10-24/10-25 周末无公告日段）；10-26 公告组 358 篇全部未入馆，摘要级 XR 命中 18 篇；RSS 7 分类去重 581 → KW 命中 30 = **18 篇 2610.* 真新提交（与 listing 命中集合逐篇一致，两渠道互证）+ 8 篇旧稿 replace/cross 再公告 + 4 篇库内 v2 再公告**。'
 '主批甄别 **XR 核心/强相关 7 篇**（剔非 XR 11 篇：机器人 VLA/航空 GNSS/光子逆设计/医学影像/自动驾驶/无人机 VLN 等）；全文 **6 L0/FULL + 1 L1/PARTIAL**（2610.32232 Virtual Placebo，ar5iv 仅摘要页）。'
 'Top7（低量日实数，未凑数）：**4 A / 3 B，最高 3.85（PixGR / HEALPix 并列），无 S 级**；覆盖 6 赛道。'
 '三关：门① max Jaccard **0.065**；门② 6 赛道；门③ 当日最高 3.85 < 库内近 30 天 Top10 均分 **4.416**（421 条入窗，现算）→ **非重磅日、无 S 级，未拔高**；OUTDATED 0。'
 '**backfill-1027**：旧稿 replace/cross 再公告 8 篇首次入馆（4 A / 4 B，最高 World from Motion 4.27 达 S 线按校准关记 A，同 10-24 EgoHand 先例）。'
 'registry 618 → **633**（+7 +8）。详见 [运行报告](../../reports/XR-Daily-Report-2026-10-27.md) 与 [MOC-2026-10-27](./MOC-2026-10-27.md) / [MOC-backfill-1027](./MOC-backfill-1027.md) / [Backfill 报告](../../reports/XR-Backfill-Report-backfill-1027.md)。\n')
anchor = '> **状态注记（2026-10-26）**'
i = h.find(anchor)
j = h.find('\n\n', h.find('周末提交批次将由 10-27 调度按标准流水线处理。'))
h = h[:j] + '\n' + note27 + h[j:]

# 7.3 速查入口
h = h.replace('| 最新一期 | [MOC · 2026-10-24](./MOC-2026-10-24.md) |', '| 最新一期 | [MOC · 2026-10-27](./MOC-2026-10-27.md) |')
h = h.replace('| 上一期 | [MOC · 2026-10-23](./MOC-2026-10-23.md) |', '| 上一期 | [MOC · 2026-10-24](./MOC-2026-10-24.md) |')
h = h.replace('（现有 313 篇）', '（现有 328 篇）')
h = h.replace('[运行报告 2026-10-26](../../reports/XR-Daily-Report-2026-10-26.md)', '[运行报告 2026-10-27](../../reports/XR-Daily-Report-2026-10-27.md)')

# 7.4 批次索引表追加两行
row_main = ('| 2026-10-27 | [MOC-2026-10-27](./MOC-2026-10-27.md) | XR 7（Top7 实数）· 4A/3B · 非重磅日（无S） | '
            '10-26 公告批次（周末积压）；listing+RSS 两渠道互证；1 篇 PARTIAL |')
row_bf = ('| backfill-1027 | [MOC-backfill-1027](./MOC-backfill-1027.md) | 补录 8（4A/4B）· 非当日新提交 | '
          '10-26 公告 RSS 混入旧稿 replace/cross 再公告 8 篇（2412~2610） |')
h = h.replace('| 2026-10-26 | — | **0 新稿**（周一 02:30 周末积压公告未到时刻 + API 前沿 10-22） | 状态报告日；10-23 公告组 411 篇全量标题级复核 0 漏网；周末批次待 10-27 调度处理 |',
              '| 2026-10-26 | — | **0 新稿**（周一 02:30 周末积压公告未到时刻 + API 前沿 10-22） | 状态报告日；10-23 公告组 411 篇全量标题级复核 0 漏网；周末批次待 10-27 调度处理 |\n'
              + row_main + '\n' + row_bf)

# 7.5 追加 Top10 段（文件尾）
seg = '\n### 2026-10-27 新增（Top7 实数：4 A + 3 B，非重磅日无 S）\n\n| # | 论文 | 赛道 | 分值 | 等级 | 证据 |\n|---:|---|---|---:|---|---|\n'
for i2, p in enumerate(MAIN, 1):
    seg += f"| {i2} | {esc(p['title_zh'])} | {p['track']} | {p['value']:.2f} | {p['grade']} | {p['evidence']} |\n"
seg += '\n### backfill-1027 补录（8 篇：4 A + 4 B，非当日新提交）\n\n| # | 论文 | 赛道 | 分值 | 等级 | 证据 |\n|---:|---|---|---:|---|---|\n'
for i2, p in enumerate(BF, 1):
    seg += f"| {i2} | {esc(p['title_zh'])} | {p['track']} | {p['value']:.2f} | {p['grade']} | {p['evidence']} |\n"
h = h.rstrip() + '\n' + seg

# 7.6 页脚计数
h = h.replace('文献库 618 篇', '文献库 633 篇').replace('笔记 313 篇', '笔记 328 篇')
open(moc_path, 'w', encoding='utf-8').write(h)
print('MOC-总索引 refreshed')
print('DONE')
