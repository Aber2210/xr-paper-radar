# -*- coding: utf-8 -*-
"""check_pages_1116.py — curl Range 分块下载 Pages 线上大文件，重组后与本地规范化 md5 比对 + DATA 计数核验。
（11-07 教训：代理会静默截断大文件直下；11-08 教训：urllib 直连可能被代理瞬时 ConnectionReset，改用 curl -r。）
本批基线：registry 935 / notes 587 / batches 63；11-15 状态日卡片 count=0 + refPapers=28；
11-14 主批 20 篇 max 4.15；backfill-1114 8 篇 max 4.50。
用法：python scripts/check_pages_1116.py"""
import subprocess, hashlib, re, json, sys, time

URL = 'https://aber2210.github.io/xr-paper-radar/xr-paper-hub.html'
LOCAL = 'web/xr-paper-hub.html'

total = 0
for attempt in range(3):
    head = subprocess.run(['curl', '-sI', URL], capture_output=True, text=True).stdout
    m = re.search(r'[Cc]ontent-[Ll]ength:\s*(\d+)', head)
    if m:
        total = int(m.group(1))
        break
    time.sleep(3)
print('Pages Content-Length:', total)
if not total:
    print('RESULT: FAIL (no Content-Length)')
    sys.exit(1)

chunks = []
pos = 0
while pos < total:
    end = min(pos + 1024 * 1024 - 1, total - 1)
    r = subprocess.run(['curl', '-s', '-r', f'{pos}-{end}', URL], capture_output=True)
    chunks.append(r.stdout)
    pos = end + 1
online = b''.join(chunks)
print('downloaded:', len(online), 'bytes in', len(chunks), 'chunks')

local = open(LOCAL, 'rb').read()
lm = hashlib.md5(local.replace(b'\r\n', b'\n')).hexdigest()
om = hashlib.md5(online.replace(b'\r\n', b'\n')).hexdigest()
print('local  md5 (normalized):', lm)
print('online md5 (normalized):', om)
md5ok = (lm == om)
print('md5 match:', md5ok)
print('local bytes:', len(local), '| CRLF lines (autocrlf normalization):', local.count(b'\r\n'))

h = online.replace(b'\r\n', b'\n').decode('utf-8', 'replace')
d = json.loads(re.search(r'const DATA = (\{.*?\});\s*\n', h, re.S).group(1))
np_, nn, nb = len(d['papers']), len(d['notes']), len(d['batches'])
print('online DATA: papers=%d notes=%d batches=%d' % (np_, nn, nb))
ok = md5ok and np_ == 935 and nn == 587 and nb == 63

b15 = next((x for x in d['batches'] if x['key'] == '2026-11-16'), None)
if b15:
    ref = b15.get('refPapers') or []
    print('11-16 card: count=%d refPapers=%d' % (b15['count'], len(ref)))
    if b15['count'] != 0 or len(ref) != 28:
        print('FAIL: 11-16 card mismatch'); ok = False
else:
    print('11-16 card: MISSING'); ok = False

b = next((x for x in d['batches'] if x['key'] == '2026-11-14'), None)
if b:
    g = {k: v for k, v in (b.get('grades') or {}).items() if v}
    print('11-14 card: count=%d max=%s grades=%s' % (b['count'], b['max'], g))
    if b['count'] != 20 or abs(float(b['max']) - 4.15) > 1e-6:
        print('FAIL: 11-14 card mismatch'); ok = False
else:
    print('11-14 card: MISSING'); ok = False

bf = next((x for x in d['batches'] if x['key'] == 'backfill-1114'), None)
if bf:
    print('backfill-1114 card: count=%d max=%s' % (bf['count'], bf['max']))
    if bf['count'] != 8 or abs(float(bf['max']) - 4.50) > 1e-6:
        print('FAIL: backfill-1114 card mismatch'); ok = False
else:
    print('backfill-1114 card: MISSING'); ok = False

print('RESULT:', 'PASS' if ok else 'FAIL')
sys.exit(0 if ok else 1)
