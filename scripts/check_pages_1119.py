# -*- coding: utf-8 -*-
"""2026-11-19 Pages 核验：curl -r 分块（≤1MB）重组 → 规范化 md5 vs 本地；解析 DATA 逐项比对。"""
import hashlib
import json
import os
import subprocess

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
os.chdir(ROOT)
URL = 'https://aber2210.github.io/xr-paper-radar/'
CHUNK = 1024 * 1024
tmp = os.path.join(ROOT, 'data', '_chk')
os.makedirs(tmp, exist_ok=True)
out = os.path.join(tmp, 'pages_1119.html')

head = subprocess.run(['curl', '-sI', URL], capture_output=True, text=True).stdout
code = head.split()[1] if head else '?'
clen = None
for line in head.splitlines():
    if line.lower().startswith('content-length'):
        clen = int(line.split(':')[1].strip())
print('HTTP', code, 'Content-Length', clen)

if clen:
    parts = []
    off = 0
    while off < clen:
        end = min(off + CHUNK - 1, clen - 1)
        r = subprocess.run(['curl', '-s', '-r', f'{off}-{end}', URL], capture_output=True)
        parts.append(r.stdout)
        off = end + 1
    body = b''.join(parts)
    print('downloaded', len(body), 'bytes in', len(parts), 'chunks')
    open(out, 'wb').write(body)
    norm = lambda b: b.replace(b'\r\n', b'\n')
    local = norm(open('web/xr-paper-hub.html', 'rb').read())
    print('md5 local(norm)', hashlib.md5(local).hexdigest())
    print('md5 remote(norm)', hashlib.md5(norm(body)).hexdigest())
    print('MD5 MATCH:', hashlib.md5(local).hexdigest() == hashlib.md5(norm(body)).hexdigest())
    html = body.decode('utf-8', 'replace')
    print('has const DATA:', 'const DATA' in html)
    i = html.find('const DATA')
    j = html.find('{', i)
    data, _ = json.JSONDecoder().raw_decode(html[j:])
    print('remote DATA papers', len(data['papers']), 'notes', len(data['notes']), 'batches', len(data['batches']))
    for key in ('2026-11-19', 'backfill-1119'):
        b = next((x for x in data['batches'] if x['key'] == key), None)
        print(' ', key, '->', None if not b else {'count': b['count'], 'avg': b['avg'], 'max': b['max']})
    print('has 11-19 paper rows:', sum(1 for p in data['papers'] if p.get('batch') == '2026-11-19'),
          '| backfill-1117:', sum(1 for p in data['papers'] if p.get('batch') == 'backfill-1119'))
