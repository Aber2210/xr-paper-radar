# -*- coding: utf-8 -*-
"""2026-11-17 前端核验：HTML 内 DATA 计数 vs 磁盘，新批次在场性，卡片 count/refPapers。"""
import json
import os
import re

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
os.chdir(ROOT)
html = open('web/xr-paper-hub.html', encoding='utf-8').read()
i = html.find('const DATA')
assert i > 0, 'DATA not found'
j = html.find('{', i)
data, end = json.JSONDecoder().raw_decode(html[j:])
print('DATA parsed, keys:', sorted(data.keys())[:12])

reg = [json.loads(l) for l in open('papers/library/registry.jsonl', encoding='utf-8') if l.strip()]
notes = [f for f in os.listdir('papers/notes') if f.endswith('.md')]
daily = os.listdir('papers/daily')
print('disk: registry', len(reg), 'notes', len(notes), 'daily', len(daily))

for k, v in (('papers', len(reg)), ('notes', len(notes))):
    if k in data:
        got = data[k] if isinstance(data[k], int) else len(data[k])
        print(f'  DATA.{k}={got} vs disk {v} ->', 'OK' if got == v else 'MISMATCH')

# daily 卡片
daily_cards = data.get('daily') or data.get('batches') or []
if isinstance(daily_cards, list):
    print('daily cards:', len(daily_cards))
    for c in daily_cards:
        if c.get('date') in ('2026-11-17',) or c.get('key') in ('2026-11-17', 'backfill-1117'):
            print('  ', {kk: c.get(kk) for kk in ('key', 'date', 'count', 'avg', 'max', 'refCount', 'label')})
    keys = [c.get('key') or c.get('date') for c in daily_cards]
    print('has 2026-11-17:', '2026-11-17' in keys, '| has backfill-1117:', 'backfill-1117' in keys)
    print('disk daily dirs missing in frontend:', sorted(set(daily) - set(k for k in keys if k)))

# 论文库计数
for k in ('papers',):
    pass
# 新论文在场性
ids = set()
for p in reg:
    if p.get('batch') in ('2026-11-17', 'backfill-1117'):
        pid = p['id'].split(':')[-1].split('v')[0]
        ids.add(pid)
missing = [x for x in ids if x not in html]
print('新批次论文在 HTML 中缺失:', missing)
