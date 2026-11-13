# -*- coding: utf-8 -*-
import json, glob, os, collections

rows = [json.loads(l) for l in open('papers/library/registry.jsonl', encoding='utf-8') if l.strip()]
print('registry', len(rows))
print('grades', collections.Counter(r['grade'] for r in rows))
print('batch1114', collections.Counter(r['batch'] for r in rows if r['date'] == '2026-11-14'))
bad = [r for r in rows if (r.get('title') or '').strip() == r['id'].split(':')[-1] or len(r.get('title') or '') < 12]
print('suspicious titles:', [(r['id'], r.get('title')) for r in bad])
print('notes', len(glob.glob('papers/notes/*.md')), 'daily', len(os.listdir('papers/daily')))
print('dup ids', [k for k, v in collections.Counter(r['id'] for r in rows).items() if v > 1][:5])
# 抽查本批笔记与报告
for f in ['papers/notes/2611.15153__matrixsplat-matrix-parallel-3dgs.md']:
    t = open(f, encoding='utf-8').read()
    print('---', f, len(t), 'chars')
    print(t[:600])
r = open('reports/XR-Daily-Report-2026-11-14.md', encoding='utf-8').read()
print('report chars', len(r), 'chapters', r.count('### 第 '))
print('7dim rows', open('papers/daily/2026-11-14/7dim-table.md', encoding='utf-8').read().count('\n| 2611'))
print('bf 7dim rows', open('papers/daily/backfill-1114/7dim-table.md', encoding='utf-8').read().count('\n| 26') + open('papers/daily/backfill-1114/7dim-table.md', encoding='utf-8').read().count('\n| 25'))
