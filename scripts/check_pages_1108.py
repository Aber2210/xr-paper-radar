# -*- coding: utf-8 -*-
"""check_pages_1108.py — Range 分块下载 Pages 线上大文件，重组后与本地规范化 md5 比对 + DATA 计数核验。
（11-07 教训：代理会静默截断大文件直下，HTTP 200 但只收部分内容。）"""
import urllib.request, hashlib, json, re, sys

URL = 'https://aber2210.github.io/xr-paper-radar/xr-paper-hub.html'
LOCAL = 'web/xr-paper-hub.html'
UA = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120.0 Safari/537.36'}

def fetch_range(url, start, end):
    req = urllib.request.Request(url, headers={**UA, 'Range': f'bytes={start}-{end}'})
    with urllib.request.urlopen(req, timeout=120) as r:
        return r.read(), r.status

# 1) 获取总大小
req = urllib.request.Request(URL, headers=UA)
with urllib.request.urlopen(req, timeout=120) as r:
    total = int(r.headers.get('Content-Length', 0))
    status = r.status
print('Pages status:', status, 'Content-Length:', total)

# 2) Range 分块下载（≤1MB/块）
chunks = []
pos = 0
while pos < total:
    end = min(pos + 1024 * 1024 - 1, total - 1)
    data, st = fetch_range(URL, pos, end)
    chunks.append(data)
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
crlf = local.count(b'\r\n')
print('CRLF lines in local (autocrlf normalization):', crlf)

# 4) DATA 计数核验
h = online.decode('utf-8', 'replace')
m = re.search(r'const DATA = (\{.*?\});\s*\n', h, re.S)
d = json.loads(m.group(1))
print('online DATA: papers=%d notes=%d batches=%d' % (len(d['papers']), len(d['notes']), len(d['batches'])))
b = next((x for x in d['batches'] if x['key'] == '2026-11-08'), None)
print('11-08 card:', ('count=%d refPapers=%d' % (b['count'], len(b['refPapers']))) if b else 'MISSING')
ok = lm == om and len(d['papers']) == 831 and len(d['notes']) == 502 and len(d['batches']) == 51 and b and b['count'] == 0 and len(b['refPapers']) == 23
print('RESULT:', 'PASS' if ok else 'FAIL')
sys.exit(0 if ok else 1)
