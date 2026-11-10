# -*- coding: utf-8 -*-
"""2026-11-11 渠道② 核验：curl -r 分块拉取 Pages 页面 → 解析 DATA → 与本地逐项比对。
（urllib 直连 Pages 曾被代理 ConnectionReset，沿用 11-09 的 curl -r 范式；大文件直下会被静默截断。）
"""
import json, subprocess, os, hashlib, re, sys

URL = 'https://aber2210.github.io/xr-paper-radar/'
TMP = 'data/tmp_check'
os.makedirs(TMP, exist_ok=True)
CH = 1_000_000
MAX = 6

parts = []
total = None
for i in range(MAX):
    fn = f'{TMP}/pages_{i}.bin'
    subprocess.run(['curl', '-s', '-r', f'{i*CH}-{i*CH+CH-1}', '-o', fn, '--max-time', '180', URL], check=False)
    if not os.path.exists(fn):
        print('chunk', i, 'missing'); break
    sz = os.path.getsize(fn)
    parts.append(fn)
    print(f'chunk {i}: {sz} bytes')
    if sz < CH:
        break
data = b''.join(open(p, 'rb').read() for p in parts)
print('total bytes', len(data))
open(f'{TMP}/pages_hub.html', 'wb').write(data)

h = data.decode('utf-8', 'replace')
i = h.find('const DATA')
if i < 0:
    print('FATAL: const DATA not found'); sys.exit(1)
st = h.find('{', i)
obj, _ = json.JSONDecoder().raw_decode(h[st:])
print('remote DATA: papers=%d notes=%d batches=%d' % (len(obj['papers']), len(obj['notes']), len(obj['batches'])))
keys = [b['key'] for b in obj['batches']]
print('has 11-11:', '2026-11-11' in keys, '| has backfill-1111:', 'backfill-1111' in keys)
b = next((x for x in obj['batches'] if x['key'] == '2026-11-11'), None)
if b:
    print('11-11 card: count=%s avg=%s max=%s grades=%s' % (b['count'], b['avg'], b['max'], b['grades']))
bf = next((x for x in obj['batches'] if x['key'] == 'backfill-1111'), None)
if bf:
    print('bf1111 card: count=%s avg=%s max=%s' % (bf['count'], bf['avg'], bf['max']))

loc = open('web/xr-paper-hub.html', 'rb').read()
md5_remote = hashlib.md5(data.replace(b'\r\n', b'\n')).hexdigest()
md5_local = hashlib.md5(loc.replace(b'\r\n', b'\n')).hexdigest()
print('md5 remote(norm) =', md5_remote)
print('md5 local (norm) =', md5_local)
print('IDENTICAL' if md5_remote == md5_local else 'DIFF (检查是否截断/行尾差异)')

import glob
n_papers = sum(1 for l in open('papers/library/registry.jsonl', encoding='utf-8') if l.strip())
n_notes = len(glob.glob('papers/notes/*.md'))
n_batches = len([d for d in glob.glob('papers/daily/*') if os.path.isdir(d)])
print('local build: papers=%d notes=%d batches=%d' % (n_papers, n_notes, n_batches))
ok = (len(obj['papers']) == n_papers and len(obj['notes']) == n_notes
      and len(obj['batches']) == n_batches
      and '2026-11-11' in keys and 'backfill-1111' in keys)
print('CHECK:', 'PASS' if ok else 'FAIL')
