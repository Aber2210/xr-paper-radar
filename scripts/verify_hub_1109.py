# -*- coding: utf-8 -*-
"""verify_hub_1109.py — 核验 web/xr-paper-hub.html 内 DATA 计数与磁盘一致 + 11-09 状态日卡片形态。"""
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

# 11-08 卡片
b = next((x for x in data['batches'] if x['key'] == '2026-11-09'), None)
if not b:
    print('FAIL: 2026-11-09 batch missing'); ok = False
else:
    print('11-09 card: count=%d refPapers=%d avg=%s max=%s note=%s' % (
        b['count'], len(b['refPapers']), b['avg'], b['max'], (b['note'] or '')[:60]))
    if b['count'] != 0:
        print('FAIL: 11-09 count should be 0'); ok = False
    if len(b['refPapers']) != 23:
        print('FAIL: 11-09 refPapers should be 23'); ok = False
    if not b['note'] or '当日无新稿' not in b['note']:
        print('FAIL: 11-09 note missing'); ok = False
    # refPapers 应与 registry 中 batch=2026-11-07 的 23 篇一致
    ids = {r['id'] for r in b['refPapers']}
    reg1107 = set()
    for l in open(os.path.join(ROOT, 'papers/library/registry.jsonl'), encoding='utf-8'):
        if l.strip():
            d = json.loads(l)
            if d.get('batch') == '2026-11-07':
                reg1107.add(d['id'].split(':')[-1].split('v')[0])
    if ids != reg1107:
        print('FAIL: refPapers != registry batch 2026-11-07 set; diff:', ids ^ reg1107); ok = False
    else:
        print('refPapers == registry batch 2026-11-07 (23 篇) ✓')
    if '2611.07902' not in ids:
        print('FAIL: refPapers missing XM4D 2611.07902'); ok = False

# statusNote 应含 11-08 状态注记
if data['batches'] and b:
    print('11-09 statusNote present:', bool(b.get('statusNote')))

print('RESULT:', 'PASS' if ok else 'FAIL')
sys.exit(0 if ok else 1)
