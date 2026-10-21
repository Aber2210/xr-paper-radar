# -*- coding: utf-8 -*-
# notes_1022.py — 渲染 2026-10-22 批次 20 篇原子笔记（内容来自 4 个 content JSON，元数据来自 registry）。
import json, os

ROOT = 'D:/Agent/WorkBuddy/Research'
OUT = f'{ROOT}/papers/notes'
os.makedirs(OUT, exist_ok=True)

reg = {}
for l in open(f'{ROOT}/papers/library/registry.jsonl', encoding='utf-8'):
    if l.strip():
        d = json.loads(l)
        reg[d['id'].split(':')[-1].split('v')[0]] = d

CONTENT = {}
for g in (1, 2, 3, 4):
    for x in json.load(open(f'{ROOT}/data/notes_content_1022_g{g}.json', encoding='utf-8')):
        CONTENT[x['id']] = x

batch_ids = [i for i, d in reg.items() if d.get('batch') == '2026-10-22']
missing = [i for i in batch_ids if i not in CONTENT]
print('content missing for:', missing)

def render(n):
    s = n
    def lst(x):
        if isinstance(x, list):
            return '\n'.join(f'- {i}' for i in x)
        return x or ''
    fm = ['---',
          f"id: arXiv:{s['id']}", f"title: {s['title']}", f"title_zh: {s['title_zh']}",
          f"track: {s['track']}", f"venue: {s['venue']}", f"date: {s['date']}",
          f"value: {s['value']}", f"grade: {s['grade']}",
          f"evidence: {s['evidence']}", f"status: {s['status']}",
          f"scores: {{IMP:{s['IMP']}, NOV:{s['NOV']}, TEC:{s['TEC']}, EXP:{s['EXP']}, PER:{s['PER']}, TRL:{s['TRL']}, REP:{s['REP']}}}",
          f"fetch_level: {s['level']}", f"tags: [{', '.join(s['tags'])}]", '---', '']
    body = [f"# {s['title_zh']}", '', '## 一句话结论', s['conclusion'], '',
            '## 要解决的问题', s['problem'], '',
            '## 方法详解（含关键公式/架构，保留原文术语）', s['method'], '',
            '## 实验与结果（表格化关键数字）', s['experiments'], '',
            '## 创新点与贡献', lst(s['innovation']), '',
            '## 局限与风险', lst(s['limits']), '',
            '## 与文献库的关系（新增 / 改进 / 取代 X）', s['relation'], '',
            '## 可复现性（代码/数据/硬件）', s['repro'], '',
            '## 行动建议', s['action'], '']
    return '\n'.join(fm + body)

n = 0
for bid, c in CONTENT.items():
    d = reg.get(bid)
    if not d:
        print('!! not in registry:', bid); continue
    s = dict(c)
    s.update({'title': d['title'], 'title_zh': d['title_zh'], 'track': d['track'], 'date': d['date'],
              'value': d['value'], 'grade': d['grade'], 'evidence': d['evidence'], 'status': d['status'],
              'IMP': d['scores']['IMP'], 'NOV': d['scores']['NOV'], 'TEC': d['scores']['TEC'],
              'EXP': d['scores']['EXP'], 'PER': d['scores']['PER'], 'TRL': d['scores']['TRL'],
              'REP': d['scores']['REP'], 'level': d['fetch_level']})
    fn = f"{OUT}/{bid}__{c['slug']}.md"
    open(fn, 'w', encoding='utf-8').write(render(s))
    n += 1
print('total notes:', n)
