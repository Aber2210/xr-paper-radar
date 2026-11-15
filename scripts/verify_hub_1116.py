# -*- coding: utf-8 -*-
"""verify_hub_1116.py — 核验 web/xr-paper-hub.html 内 DATA 与磁盘一致 + 11-16 状态日卡片形态。"""
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

# 2026-11-16 状态日卡片：count=0 + 参考论文 28 篇（上一内容批次 11-14 主批 20 + backfill-1114 8）
b = next((x for x in data['batches'] if x['key'] == '2026-11-16'), None)
if not b:
    print('FAIL: 2026-11-15 batch missing'); ok = False
else:
    print('11-16 card: count=%d refPapers=%s avg=%s max=%s' % (
        b['count'], len(b.get('refPapers') or []), b.get('avg'), b.get('max')))
    if b['count'] != 0:
        print('FAIL: 11-16 count should be 0'); ok = False
    ref = b.get('refPapers') or []
    if len(ref) != 28:
        print('FAIL: 11-16 refPapers should be 28'); ok = False

# 上一内容批次卡片仍在场
b14 = next((x for x in data['batches'] if x['key'] == '2026-11-14'), None)
if not b14 or b14['count'] != 20:
    print('FAIL: 2026-11-14 card count mismatch'); ok = False
else:
    print('11-14 card: count=%d max=%s grades=%s' % (b14['count'], b14['max'], b14.get('grades')))

bf14 = next((x for x in data['batches'] if x['key'] == 'backfill-1114'), None)
if not bf14 or bf14['count'] != 8:
    print('FAIL: backfill-1114 card count mismatch'); ok = False
else:
    print('bf-1114 card: count=%d max=%s' % (bf14['count'], bf14['max']))

# 全部 registry 论文在场
reg = {}
for l in open(os.path.join(ROOT, 'papers/library/registry.jsonl'), encoding='utf-8'):
    if l.strip():
        d = json.loads(l)
        reg[d['id'].split(':')[-1].split('v')[0]] = d
have = {p['id'].split(':')[-1].split('v')[0] for p in data['papers']}
miss = [i for i in reg if i not in have]
print('registry papers in DATA: %d/%d missing=%s' % (len(reg) - len(miss), len(reg), miss[:6]))
if miss:
    ok = False

# 参考表论文（11-14 主批 + backfill-1114）全部在场
ref_ids = [k for k, v in reg.items() if v.get('batch') in ('2026-11-14', 'backfill-1114')]
miss_ref = [i for i in ref_ids if i not in have]
print('ref papers in DATA: %d/%d missing=%s' % (len(ref_ids) - len(miss_ref), len(ref_ids), miss_ref))
if miss_ref or len(ref_ids) != 28:
    ok = False

print('RESULT:', 'PASS' if ok else 'FAIL')
sys.exit(0 if ok else 1)
