# -*- coding: utf-8 -*-
"""2026-11-17 产物生成（第三部分）：原子笔记 / MOC / registry / MOC-总索引。"""
import glob
import json
import os
import re
import shutil

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
os.chdir(ROOT)
D = json.load(open('data/scored_1117.json', encoding='utf-8'))
MAIN = [p for p in D if p['batch'] == '2026-11-17']
BF = [p for p in D if p['batch'] == 'backfill-1117']
MAIN.sort(key=lambda r: (-r['value'], -r['scores']['IMP'], -r['scores']['NOV'], r['id']))
G = json.load(open('data/gates_1117.json', encoding='utf-8'))
TOP10_ORDER = G['top10']
DATE, ANN = '2026-11-17', '2026-11-16'
GATE3, G1 = G['gate3']['top10_mean'], G['gate1']['max_jaccard']
MANIFEST = json.load(open('data/fulltext/_manifest.json', encoding='utf-8'))
for p in MAIN + BF:
    p['level'] = MANIFEST[p['id']]['level']
    p['evidence'] = MANIFEST[p['id']]['evidence']
    p['announce'] = 'replace' if p['batch'].startswith('backfill') else 'new'
    p['status'] = 'CURRENT'
    v = p['value']
    p['grade'] = 'S' if v >= 4.2 else ('A' if v >= 3.6 else ('B' if v >= 3.0 else 'C'))
    if p['batch'].startswith('backfill') and p['grade'] == 'S':
        p['grade'] = 'A'
    p['in_top10'] = p['id'] in TOP10_ORDER


def esc(s):
    return str(s).replace('|', '/')


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
        in_top10=('true' if p['in_top10'] else 'false'),
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
        L.append(f"| {i} | {esc(p['title_zh'])} | {p['track']} | {p['value']:.2f} | {p['grade']} | "
                 f"{p['evidence']} | {link} |")
    L += ['\n## 批次要点\n']
    for p in papers:
        L.append(f"- **{esc(p['title_zh'])}**（{p['id']}，{p['value']:.2f} {p['grade']}）：{p['conclusion']}")
    open(path, 'w', encoding='utf-8').writelines([x + '\n' for x in L])


moc(MAIN, f'papers/MOC/MOC-{DATE}.md', f'MOC · {DATE}（11-16 公告批次 · 周末积压周一释放）',
    '> 当日地图：**公告日 2026-11-16（周一）≠ 拉取日 2026-11-17（周二 02:30）**——诚实口径。'
    '周末 11-14/11-15 无公告日段（`skipDays` 节律），两日提交积压于周一 00:00 UTC（08:00 北京时间）统一释放；'
    'API published 核验主批提交日 **11-13×12 / 11-12×1**（RSS published 为公告时间戳）。\n'
    '> 主批 XR 新稿 **13 篇（5 A / 6 B / 2 C，无 S）**，Top10 实数 10 篇最高 **3.93**（EcoVGGT）；'
    '11-16 组 271 篇摘要级（覆盖率 271/271）+ 标题级补扫 22 篇 → 33 候选 → 剔 20 篇误命中 → 13 篇；'
    '11-13 组复采 581 篇未入馆与上批 581/581 逐篇一致 → 0 漏网。\n'
    '> 全文：**12 篇 L0/FULL + 1 篇 L1/PARTIAL**（2611.17903 ar5iv 仅摘要页，摘要级评估）。\n'
    '> 覆盖度三关：门① 0.231 / 门② 定稿 **8 赛道**（未重筛）/ 门③ **3.93 < 4.4030**（现算，398 条入窗）→ **非重磅日，无 S**。\n'
    '> Top10（实数 10 篇）：EcoVGGT 3.93 · FOMOS 3.85 · DeepBA 3.85 · A·LoMa 3.80 · VACO 3.78 · D2ToF 3.58 · '
    'MacroGS 3.57 · TouchTwin 3.55 · DIRT 3.51 · Zoom In Scale Out 3.12（PARTIAL）。')

moc(BF, 'papers/MOC/MOC-backfill-1117.md', 'MOC · backfill-1117（旧稿 v2 再公告首次入馆）',
    '> **非当日新提交**：本批 3 篇均为 11-16 公告 RSS 混入的旧稿 v2 再公告（原始投稿 2025-01-22 / 2026-08-19 / 2026-11-12，'
    '2026-11-13 更新），诚实口径单独编号，不参与当日重磅日判定。\n'
    '> 定稿 **3 A（无 S）**，最高 **2611.17238 HEIR 4.07**（人机双视角配对数据集 + 意图理解基准）——高于主批最高 3.93；'
    '其余：2608.19372 The Missing Touch 4.01（触觉显示回显接触几何）· 2501.12764 Grid-based Submap Joining 3.87（栅格子图拼接 NLLS）。')
print('MOC written')


# ---------- registry ----------
reg_path = 'papers/library/registry.jsonl'
bak_path = 'papers/library/registry.jsonl.bak-20261117'
if not os.path.exists(bak_path):
    shutil.copy(reg_path, bak_path)
    print('backup ->', bak_path)
rows = [json.loads(l) for l in open(reg_path, encoding='utf-8') if l.strip()]
have = {r['id'].split(':')[-1].split('v')[0] for r in rows}
added = 0
with open(reg_path, 'a', encoding='utf-8') as f:
    for p in MAIN + BF:
        if p['id'] in have:
            print('exists skip', p['id'])
            continue
        entry = dict(id=f"arXiv:{p['id']}", title=p['title'], title_zh=p['title_zh'],
                     track=p['track'], date=DATE, value=p['value'], grade=p['grade'],
                     scores=p['scores'], status=p['status'], evidence=p['evidence'],
                     fetch_level=p['level'], fulltext_chars=MANIFEST[p['id']]['chars'],
                     in_top10=p['in_top10'], batch=p['batch'],
                     announce_type=p['announce'], flags=[])
        f.write(json.dumps(entry, ensure_ascii=False) + '\n')
        added += 1
total = len(rows) + added
print(f'registry +{added}（{len(rows)} -> {total}）')
assert total == 951, total
