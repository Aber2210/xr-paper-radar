# -*- coding: utf-8 -*-
"""verify_hub_1114.py — 核验 web/xr-paper-hub.html 内 DATA 与磁盘一致 + 11-14 / backfill-1114 卡片形态。"""
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

# 11-14 卡片
b = next((x for x in data['batches'] if x['key'] == '2026-11-14'), None)
if not b:
    print('FAIL: 2026-11-14 batch missing'); ok = False
else:
    print('11-14 card: count=%d avg=%s max=%s grades=%s' % (b['count'], b['avg'], b['max'], b.get('grades')))
    if b['count'] != 20:
        print('FAIL: 11-14 count should be 20'); ok = False
    if abs(float(b['max']) - 4.15) > 1e-6:
        print('FAIL: 11-14 max should be 4.15'); ok = False
    g = {k: v for k, v in (b.get('grades') or {}).items() if v}
    if g != {'A': 6, 'B': 9, 'C': 5}:
        print('FAIL: 11-14 grades mismatch', g); ok = False
    print('11-14 label:', (b.get('label') or '')[:110])

# backfill-1114 卡片
bf = next((x for x in data['batches'] if x['key'] == 'backfill-1114'), None)
if not bf:
    print('FAIL: backfill-1114 batch missing'); ok = False
else:
    print('bf-1114 card: count=%d avg=%s max=%s grades=%s' % (bf['count'], bf['avg'], bf['max'], bf.get('grades')))
    if bf['count'] != 8 or abs(float(bf['max']) - 4.50) > 1e-6:
        print('FAIL: backfill-1114 count/max mismatch'); ok = False

# 新论文全部在场 + top10 标记
reg = {}
for l in open(os.path.join(ROOT, 'papers/library/registry.jsonl'), encoding='utf-8'):
    if l.strip():
        d = json.loads(l)
        reg[d['id'].split(':')[-1].split('v')[0]] = d
new_ids = [k for k, v in reg.items() if v.get('batch') in ('2026-11-14', 'backfill-1114')]
have = {p['id'].split(':')[-1].split('v')[0] for p in data['papers']}
miss = [i for i in new_ids if i not in have]
print('new papers in DATA: %d/%d missing=%s' % (len(new_ids) - len(miss), len(new_ids), miss))
if miss:
    ok = False
top = [p['id'].split(':')[-1] for p in data['papers'] if p.get('top10') and reg.get(p['id'].split(':')[-1], {}).get('batch') == '2026-11-14']
print('11-14 top10 flagged:', len(top), sorted(top))
if len(top) != 10:
    print('FAIL: 11-14 top10 flag count should be 10'); ok = False

# 标题修补核验（2611.08731 / 2611.09692 / 2611.09524）
for pid, kw in (('2611.08731', 'eSharp'), ('2611.09692', 'PoseRieFlow'), ('2611.09524', 'RadarDINO')):
    p = next((x for x in data['papers'] if x['id'].endswith(pid)), None)
    if not p or kw not in (p.get('title') or ''):
        print('FAIL: title not repaired for', pid); ok = False
    else:
        print('title ok', pid, '->', p['title'][:70])

print('RESULT:', 'PASS' if ok else 'FAIL')
sys.exit(0 if ok else 1)
