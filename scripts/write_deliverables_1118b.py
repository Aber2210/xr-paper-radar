# -*- coding: utf-8 -*-
"""2026-11-18 产物（第二部分）：原子笔记 / 当日 MOC / registry 幂等追加。
门③ 险过 → blockbuster=false → 档位按 A 封顶（不记 S）。
"""
import glob
import json
import os
import re
import shutil
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from grade_caliber import assign_grade  # noqa: E402

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
os.chdir(ROOT)

D = json.load(open('data/scored_1118.json', encoding='utf-8'))
MAIN = [p for p in D if p['batch'] == '2026-11-18']
BF = [p for p in D if p['batch'] == 'backfill-1118']
MAIN.sort(key=lambda r: (-r['value'], -r['scores']['IMP'], -r['scores']['NOV'], r['id']))
G = json.load(open('data/gates_1118.json', encoding='utf-8'))
TOP10_ORDER = G['top10']
DATE = '2026-11-18'
HEAVY = bool(G['gate3']['blockbuster'])
MANIFEST = json.load(open('data/fulltext/_manifest.json', encoding='utf-8'))
for p in MAIN + BF:
    p['level'] = MANIFEST[p['id']]['level']
    p['evidence'] = MANIFEST[p['id']]['evidence']
    p['announce'] = 'replace' if p['batch'].startswith('backfill') else 'new'
    p['status'] = 'CURRENT'
    p['grade'] = assign_grade(p['value'], p['batch'], HEAVY)
    p['in_top10'] = p['id'] in TOP10_ORDER


def esc(s):
    return str(s).replace('|', '/')


def slugify(t):
    s = re.sub(r'[^a-z0-9]+', '-', t.lower()).strip('-')
    return s[:52]


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
published: {published}
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
        in_top10=('true' if p['in_top10'] else 'false'), published=p['published'],
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


moc(MAIN, f'papers/MOC/MOC-{DATE}.md', f'MOC · {DATE}（11-17 公告批次 · 手部与交互主线）',
    '> 当日地图：**公告日 2026-11-17（周二）≠ 拉取日 2026-11-18（周三 02:30）**——诚实口径。'
    '主批 API published 核验提交日 **11-16×16 / 11-15×8 / 11-14×3 / 11-13×3 / 11-10×1 / 11-06×1 / 10-31×1**'
    '（2611.18679 延迟约 17 天公告；RSS published 为公告时间戳）。\n'
    '> 主批 XR 新稿 **33 篇（0 S / 19 A / 7 B / 7 C）**，Top10 实数 10 篇最高 **4.43**（WinDEX）；'
    '11-17 组 1,016 槽位 / 844 篇唯一，摘要级覆盖率 844/844 + 标题级补扫 36 篇 → 102 候选 → 剔 69 篇误命中 → 33 篇；'
    '11-16 组复采 258 篇未入馆（= 271 − 13）→ 0 漏网。\n'
    '> 全文：**29 篇 L0/FULL + 4 篇 L1/PARTIAL**（2611.18822 / 2611.20196 / 2611.20570 / 2611.21485 ar5iv 仅摘要页，摘要级评估）。\n'
    '> 覆盖度三关：门① 0.318 / 门② 定稿 **6 赛道**（未重筛）/ 门③ **4.43 vs 4.4030**（现算，410 条入窗）'
    '→ 机械 heavy_day=true，但**差值 0.027 < 0.05 属险过**，按 skill §8.6.3 **不记 S**（4 篇 ≥4.20 记 A）。\n'
    '> Top10（实数 10 篇）：WinDEX 4.43 · LynnReal-Hand 4.37 · SemLite-GS 4.30 · MomentPnP 4.27 · JEPA4R 4.15 · '
    'RemeshingAgent 4.15 · CiGS 4.08 · Is It Still There 4.07 · Mask Is Not the Object 4.07 · MetricHand 4.00。')

moc(BF, 'papers/MOC/MOC-backfill-1118.md', 'MOC · backfill-1118（旧稿 v2/v3 再公告首次入馆）',
    '> **非当日新提交**：本批 6 篇均为 11-17 公告 RSS 混入的旧稿 v2/v3 再公告（原始投稿 2025-11-20 ~ 2026-11-13，'
    '2026-11-14~11-16 更新），诚实口径单独编号，不参与当日重磅日判定。\n'
    '> 定稿 **2 A / 3 B / 1 C（无 S）**，最高 **2607.03875 MACRO 3.93**（特写渲染的深度平面参考图对齐，免训练）；'
    '其余：2511.16349 LoC-IN 3.81（神经渲染 LiDAR 地图定位）· 2611.18267 TetraCoder 3.58（自适应四面体编码）· '
    '2605.09586 DeformMaster 3.55（形变世界模型）· 2605.05712 EgoEMG 3.49（sEMG + 第一视角数据集）· '
    '2609.31117 XR 笔式控制 2.20（C 级仅入馆）。')
print('MOC written')

# ---------- registry ----------
reg_path = 'papers/library/registry.jsonl'
bak_path = 'papers/library/registry.jsonl.bak-20261118'
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
assert total == 990, total
