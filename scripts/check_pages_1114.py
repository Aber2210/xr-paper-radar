# -*- coding: utf-8 -*-
"""check_pages_1114.py — curl Range 分块下载 Pages 线上大文件，重组后与本地规范化 md5 比对 + DATA 计数核验。
（11-07 教训：代理会静默截断大文件直下；11-08 教训：urllib 直连可能被代理瞬时 ConnectionReset，改用 curl -r。）
本批基线：registry 935 / notes 587 / batches 61；11-14 主批 20 篇 max 4.15；backfill-1114 8 篇 max 4.50；
另核 11-14 修补的 3 条裸 ID 标题（2611.08731 eSharp / 2611.09692 PoseRieFlow / 2611.09524 RadarDINO）。
用法：python scripts/check_pages_1114.py"""
import subprocess, hashlib, re, json, sys, time

URL = 'https://aber2210.github.io/xr-paper-radar/xr-paper-hub.html'
LOCAL = 'web/xr-paper-hub.html'

# 1) HEAD 取大小（Pages CDN 偶尔首次回源慢，重试 3 次）
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

# 2) Range 分块下载（<=1MB/块）
chunks = []
pos = 0
while pos < total:
    end = min(pos + 1024 * 1024 - 1, total - 1)
    r = subprocess.run(['curl', '-s', '-r', f'{pos}-{end}', URL], capture_output=True)
    chunks.append(r.stdout)
    pos = end + 1
online = b''.join(chunks)
print('downloaded:', len(online), 'bytes in', len(chunks), 'chunks')

# 3) 本地规范化（CRLF->LF）后比对 md5
local = open(LOCAL, 'rb').read()
lm = hashlib.md5(local.replace(b'\r\n', b'\n')).hexdigest()
om = hashlib.md5(online.replace(b'\r\n', b'\n')).hexdigest()
print('local  md5 (normalized):', lm)
print('online md5 (normalized):', om)
print('md5 match:', lm == om)
print('local bytes:', len(local), '| CRLF lines (autocrlf normalization):', local.count(b'\r\n'))

# 4) DATA 计数核验
h = online.replace(b'\r\n', b'\n').decode('utf-8', 'replace')
d = json.loads(re.search(r'const DATA = (\{.*?\});\s*\n', h, re.S).group(1))
np_, nn, nb = len(d['papers']), len(d['notes']), len(d['batches'])
print('online DATA: papers=%d notes=%d batches=%d' % (np_, nn, nb))

b = next((x for x in d['batches'] if x['key'] == '2026-11-14'), None)
if b:
    g = {k: v for k, v in (b.get('grades') or {}).items() if v}
    print('11-14 card: count=%d max=%s grades=%s' % (b['count'], b['max'], g))
else:
    print('11-14 card: MISSING')
bf = next((x for x in d['batches'] if x['key'] == 'backfill-1114'), None)
print('backfill-1114 card:', ('count=%d max=%s' % (bf['count'], bf['max'])) if bf else 'MISSING')

# 标题修补核验（11-10 批次遗留 3 条裸 ID）
CHECKS = {'2611.08731': 'eSharp', '2611.09692': 'PoseRieFlow', '2611.09524': 'RadarDINO'}
title_ok = {}
for pid, kw in CHECKS.items():
    p = next((x for x in d['papers'] if x['id'].endswith(pid)), None)
    t = (p.get('title') or '') + ' | ' + (p.get('title_zh') or '') if p else ''
    hit = bool(p) and kw.lower() in t.lower() and pid not in (p.get('title') or '')
    title_ok[pid] = hit
    print('title %s -> %s (%s)' % (pid, hit, (p.get('title') or 'MISSING')[:70]))

# 主批 28 篇全部在场
IDS_MAIN = 20
present = sum(1 for x in d['papers'] if (x.get('batch') or '') == '2026-11-14')
present_bf = sum(1 for x in d['papers'] if (x.get('batch') or '') == 'backfill-1114')
print('papers tagged batch=2026-11-14: %d | backfill-1114: %d' % (present, present_bf))

ok = (lm == om and np_ == 935 and nn == 587 and nb == 61
      and b and b['count'] == 20 and abs(float(b['max']) - 4.15) < 1e-6
      and bf and bf['count'] == 8 and abs(float(bf['max']) - 4.50) < 1e-6
      and all(title_ok.values()) and present == IDS_MAIN and present_bf == 8)
print('RESULT:', 'PASS' if ok else 'FAIL')
sys.exit(0 if ok else 1)
