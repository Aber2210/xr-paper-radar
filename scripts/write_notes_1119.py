# -*- coding: utf-8 -*-
"""2026-11-19 产物（第二部分）：原子笔记 / 当日 MOC / registry 幂等追加。"""
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

D = json.load(open('data/scored_1119.json', encoding='utf-8'))
MAIN = [p for p in D if p['batch'] == '2026-11-19']
BF = [p for p in D if p['batch'] == 'backfill-1119']
MAIN.sort(key=lambda r: (-r['value'], -r['scores']['IMP'], -r['scores']['NOV'], r['id']))
G = json.load(open('data/gates_1119.json', encoding='utf-8'))
TOP10_ORDER = G['top10']
DATE = '2026-11-19'
HEAVY = bool(G['gate3']['blockbuster'])
MANIFEST = json.load(open('data/fulltext/_manifest.json', encoding='utf-8'))
for p in MAIN + BF:
    p['level'] = MANIFEST[p['id']]['level']
    p['evidence'] = MANIFEST[p['id']]['evidence']
    p['status'] = 'CURRENT'
    p['grade'] = assign_grade(p['value'], p['batch'], HEAVY)
    p['in_top10'] = p['id'] in TOP10_ORDER


def esc(s):
    return str(s).replace('|', '/')


def slugify(t):
    s = re.sub(r'[^a-z0-9]+', '-', t.lower()).strip('-')
    return s[:52]


def bullets(text):
    parts = [x.strip() for x in re.split(r'[；。]', text) if x.strip()]
    return '\n'.join(f'- {x}' for x in parts)


def repro_text(p):
    if p['code'] and p['code'] != 'none':
        return f"- 代码/项目页：{p['code']}\n- 全文证据：{p['evidence']}（{p['level']}，{p['chars']:,} 字符）"
    return f"- 代码/项目页：正文未提供\n- 全文证据：{p['evidence']}（{p['level']}，{p['chars']:,} 字符）"


def relation_text(p):
    rank = TOP10_ORDER.index(p['id']) + 1 if p['id'] in TOP10_ORDER else None
    base = f"- 本批新增（batch `{p['batch']}`，公告类型 `{p['announce']}`），赛道「{p['track']}」。"
    if rank:
        base += f"\n- 本批 Top10 第 {rank} 名。"
    base += "\n- 与库内同赛道论文构成并列参考；本批 OUTDATED/SUPERSEDED 判定为 0，未发现直接取代关系。"
    return base


def action_text(p):
    if p['grade'] == 'A':
        a = "- 纳入重点精读：方法与实验节可直接支撑选题/技术选型。"
    else:
        a = "- 浏览级：关注其问题设定与结论，方法细节按需回看。"
    if p['code'] and p['code'] != 'none':
        a += "\n- 有公开代码/项目页，可先跑通再评估迁移成本。"
    else:
        a += "\n- 未提供代码，复现需按正文细节自行实现。"
    return a


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
        method=p['method'], experiments=bullets('；'.join(p['experiments'])),
        innovation=bullets(p['novelty']), limits=bullets(p['limitations']),
        relation=relation_text(p), repro=repro_text(p), action=action_text(p))
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


moc(MAIN, f'papers/MOC/MOC-{DATE}.md', f'MOC · {DATE}（11-18 公告批次 · 端侧 3DGS 与空间推理）',
    '> 当日地图：**公告日 2026-11-18（周三）≠ 拉取日 2026-11-19（周四 02:30）**——诚实口径。'
    '主批 API published 核验提交日 **11-17×17 / 11-16×3 / 09-27×1**'
    '（2611.21642 RelicTouch 提交 09-27、延迟约 7 周公告；RSS published 为公告时间戳）。\n'
    '> 主批 XR 新稿 **21 篇（0 S / 12 A / 7 B / 2 C）**，Top10 实数 10 篇最高 **4.30**（CueSplat 与 HandRSI 并列）；'
    '11-18 组 599 槽位 / 496 篇唯一，摘要级覆盖率 496/496 + 标题级补扫 21 篇 → 58 候选 → 剔 37 篇误命中 → 21 篇；'
    '11-17 组复采 811 篇未入馆（= 844 − 33）→ 摘要级命中 69 篇与上批 rejected 逐篇一致 → 0 漏网。\n'
    '> 全文：**25 篇全部 L0/FULL**（主批 21 + backfill 4）。\n'
    '> 覆盖度三关：门① **0.261** / 门② 定稿 **6 赛道**（未重筛）/ 门③ **4.30 vs 4.4230**（现算，436 条入窗，'
    '半开窗口 [2026-10-20, 2026-11-19) 且按 batch 剔除本批两批）→ **非重磅日，无 S**（margin −0.123）。\n'
    '> Top10（实数 10 篇）：CueSplat 4.30 · HandRSI 4.30 · CoSphere-SLAM 4.15 · Cross3DGS 4.15 · MentalGrid 3.92 · '
    'ARG-Avatar 3.85 · Kolibri 3.85 · HandUMI 3.72 · SpatialMind 3.65 · SpatialCast 3.65。')

moc(BF, 'papers/MOC/MOC-backfill-1119.md', 'MOC · backfill-1119（旧稿 v2/v3 再公告首次入馆）',
    '> **非当日新提交**：本批 4 篇均为 11-18 公告 RSS 混入的旧稿 v2/v3 再公告（原始投稿 2026-05-21 ~ 2026-10-19，'
    '2026-11-16~11-17 更新），诚实口径单独编号，不参与当日重磅日判定。\n'
    '> 定稿 **3 A / 1 B（无 S）**，最高 **2606.04493 SFMambaNet 3.85**（频域感知 Mamba 对应剪枝，'
    'YFCC100M mAP@5° 73.83%）；其余：2610.27275 Max-Clique vs Max-Consensus 3.84（配准准则的理论分离）· '
    '2607.05598 SSA-3DGS 3.65（屏幕空间伪影无监督去除）· 2605.22631 HolisticMotion 3.28（掩码全身观测建模）。')
print('MOC written')

# ---------- registry ----------
reg_path = 'papers/library/registry.jsonl'
bak_path = 'papers/library/registry.jsonl.bak-20261119'
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
                     fetch_level=p['level'], fulltext_chars=p['chars'],
                     in_top10=p['in_top10'], batch=p['batch'],
                     announce_type=p['announce'], flags=[])
        f.write(json.dumps(entry, ensure_ascii=False) + '\n')
        added += 1
total = len(rows) + added
print(f'registry +{added}（{len(rows)} -> {total}）')
assert total == 1015, total
print('notes total', len(glob.glob('papers/notes/*.md')), 'daily', len(glob.glob('papers/daily/*')), 'moc', len(glob.glob('papers/MOC/*.md')))
