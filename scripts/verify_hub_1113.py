# -*- coding: utf-8 -*-
"""verify_hub_1113.py — 核验 web/xr-paper-hub.html 内 DATA 计数与磁盘一致 + 11-13 状态日卡片形态。"""
import json, re, os, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
html = open(os.path.join(ROOT, 'web/xr-paper-hub.html'), encoding='utf-8').read()

m = re.search(r'const DATA = (\{.*?\});\s*\n', html, re.S)
if not m:
    print('FAIL: const DATA not found'); sys.exit(1)
data = json.loads(m.group(1))

reg_n = sum(1 for l in open(os.path.join(ROOT, 'papers/library/registry.jsonl'), encoding='utf-8') if l.strip())
notes_n = len([f for f in os.listdir(os.path.join(ROOT, 'papers/notes')) if f.endswith('.md')])
daily_n = len([d for d in os.listdir(os.path.join(ROOT, 'papers/daily')) if os.path.isdir(os.path.join(ROOT, 'papers/daily', d))])

print('HTML DATA: papers=%d notes=%d batches=%d' % (len(data['papers']), len(data['notes']), len(data['batches'])))
print('disk     : registry=%d notes=%d daily_dirs=%d' % (reg_n, notes_n, daily_n))
ok = True
if len(data['papers']) != reg_n:
    print('FAIL: papers mismatch'); ok = False
if len(data['notes']) != notes_n:
    print('FAIL: notes mismatch'); ok = False
if len(data['batches']) != daily_n:
    print('FAIL: batches mismatch'); ok = False

# 11-13 卡片
b = next((x for x in data['batches'] if x['key'] == '2026-11-13'), None)
if not b:
    print('FAIL: 2026-11-13 batch missing'); ok = False
else:
    print('11-13 card: count=%d refPapers=%d avg=%s max=%s note=%s' % (
        b['count'], len(b['refPapers']), b['avg'], b['max'], (b['note'] or '')[:70]))
    if b['count'] != 0:
        print('FAIL: 11-13 count should be 0'); ok = False
    if len(b['refPapers']) != 19:
        print('FAIL: 11-13 refPapers should be 19'); ok = False
    if not b['note'] or '当日无新稿' not in b['note']:
        print('FAIL: 11-13 note missing'); ok = False
    ids = {r['id'] for r in b['refPapers']}
    refset = set()
    for l in open(os.path.join(ROOT, 'papers/library/registry.jsonl'), encoding='utf-8'):
        if l.strip():
            d = json.loads(l)
            if d.get('batch') in ('2026-11-12', 'backfill-1112'):
                refset.add(d['id'].split(':')[-1].split('v')[0])
    if ids != refset:
        print('FAIL: refPapers != registry batch(2026-11-12 + backfill-1112) set; diff:', ids ^ refset); ok = False
    else:
        print('refPapers == registry batch 2026-11-12 + backfill-1112 (19 篇) ✓')
    if '2611.13626' not in ids:
        print('FAIL: refPapers missing FlashMotion 2611.13626'); ok = False

# 上一批次完整性：11-12 卡片应为 15 篇
b12 = next((x for x in data['batches'] if x['key'] == '2026-11-12'), None)
print('11-12 card: count=%d max=%s' % (b12['count'] if b12 else -1, b12['max'] if b12 else None))
if not b12 or b12['count'] != 15:
    print('FAIL: 11-12 count should be 15'); ok = False

# 标题修补核验：2611.08578
p = next((x for x in data['papers'] if x['id'].endswith('2611.08578')), None)
if p:
    print('2611.08578 title_zh=%s' % p.get('title_zh'))
    if 'HaNDF' not in (p.get('title_zh') or ''):
        print('FAIL: 2611.08578 title_zh wrong'); ok = False
else:
    print('FAIL: 2611.08578 missing in DATA'); ok = False

# 批次标签在场
print('11-13 batchLabel:', (b or {}).get('label', '')[:80])

print('RESULT:', 'PASS' if ok else 'FAIL')
sys.exit(0 if ok else 1)
