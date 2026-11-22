# -*- coding: utf-8 -*-
"""verify_hub_1123.py —— 11-23 状态日前端核验：DATA 三计数 vs 磁盘、卡片在场性、refPapers。"""
import json, os

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
os.chdir(ROOT)
html = open('web/xr-paper-hub.html', encoding='utf-8').read()
i = html.find('const DATA')
assert i > 0, 'DATA not found'
j = html.find('{', i)
data, _ = json.JSONDecoder().raw_decode(html[j:])

reg = [json.loads(l) for l in open('papers/library/registry.jsonl', encoding='utf-8') if l.strip()]
notes = [f for f in os.listdir('papers/notes') if f.endswith('.md')]
daily = [d for d in os.listdir('papers/daily') if os.path.isdir(os.path.join('papers/daily', d))]
print('disk: registry', len(reg), 'notes', len(notes), 'daily', len(daily))

ok = True
for k, v in (('papers', len(reg)), ('notes', len(notes)), ('batches', len(daily))):
    got = data[k] if isinstance(data.get(k), int) else len(data.get(k) or [])
    flag = 'OK' if got == v else 'MISMATCH'
    ok &= got == v
    print(f'  DATA.{k}={got} vs disk {v} -> {flag}')

cards = data.get('daily') or data.get('batches') or []
keys = [c.get('key') or c.get('date') for c in cards]
print('cards', len(cards), '| has 2026-11-23:', '2026-11-23' in keys)
for c in cards:
    if (c.get('key') or c.get('date')) in ('2026-11-23', '2026-11-22', '2026-11-21', 'backfill-1121'):
        print('  ', {kk: c.get(kk) for kk in ('key', 'date', 'count', 'avg', 'max', 'refCount', 'refPapers')}
                if 'refPapers' in c else {kk: c.get(kk) for kk in ('key', 'date', 'count', 'avg', 'max', 'refCount')},
              '| refPapers len =', len(c.get('refPapers') or []))
print('disk daily dirs missing in frontend:', sorted(set(daily) - set(k for k in keys if k)))

# 11-21 批论文在场性
ids21 = {p['id'].split(':')[-1].split('v')[0] for p in reg if p.get('batch') in ('2026-11-21', 'backfill-1121')}
print('11-21 批缺失于 HTML:', [x for x in sorted(ids21) if x not in html])
print('VERDICT', 'PASS' if ok else 'FAIL')
