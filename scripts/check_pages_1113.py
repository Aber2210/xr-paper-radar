# -*- coding: utf-8 -*-
"""check_pages_1113.py — curl Range 分块下载 Pages 线上大文件，重组后与本地规范化 md5 比对 + DATA 计数核验。
（11-07 教训：代理会静默截断大文件直下；11-08 教训：urllib 直连可能被代理瞬时 ConnectionReset，改用 curl -r。）
用法：python scripts/check_pages_1113.py"""
import subprocess, hashlib, re, json, sys

URL = 'https://aber2210.github.io/xr-paper-radar/xr-paper-hub.html'
LOCAL = 'web/xr-paper-hub.html'

# 1) HEAD 取大小
head = subprocess.run(['curl', '-sI', URL], capture_output=True, text=True).stdout
m = re.search(r'[Cc]ontent-[Ll]ength:\s*(\d+)', head)
total = int(m.group(1))
print('Pages Content-Length:', total)

# 2) Range 分块下载（≤1MB/块）
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
local_norm = local.replace(b'\r\n', b'\n')
online_norm = online.replace(b'\r\n', b'\n')
lm = hashlib.md5(local_norm).hexdigest()
om = hashlib.md5(online_norm).hexdigest()
print('local  md5 (normalized):', lm)
print('online md5 (normalized):', om)
print('md5 match:', lm == om)
print('CRLF lines in local (autocrlf normalization):', local.count(b'\r\n'))

# 4) DATA 计数核验
h = online_norm.decode('utf-8', 'replace')
d = json.loads(re.search(r'const DATA = (\{.*?\});\s*\n', h, re.S).group(1))
print('online DATA: papers=%d notes=%d batches=%d' % (len(d['papers']), len(d['notes']), len(d['batches'])))
b = next((x for x in d['batches'] if x['key'] == '2026-11-13'), None)
print('11-13 card:', ('count=%d refPapers=%d' % (b['count'], len(b['refPapers']))) if b else 'MISSING')
b12 = next((x for x in d['batches'] if x['key'] == '2026-11-12'), None)
print('11-12 card:', ('count=%d max=%s' % (b12['count'], b12['max'])) if b12 else 'MISSING')
p = next((x for x in d['papers'] if x['id'].endswith('2611.08578')), None)
print('2611.08578 title_zh:', p.get('title_zh') if p else 'MISSING')
ok = (lm == om and len(d['papers']) == 907 and len(d['notes']) == 564
      and len(d['batches']) == 59 and b and b['count'] == 0 and len(b['refPapers']) == 19
      and b12 and b12['count'] == 15 and p and 'HaNDF' in (p.get('title_zh') or ''))
print('RESULT:', 'PASS' if ok else 'FAIL')
sys.exit(0 if ok else 1)
