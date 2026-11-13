# -*- coding: utf-8 -*-
"""抽取 web/xr-paper-hub.html 内联 <script> 块到 data/_chk/ 供 node --check 语法校验。"""
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
html = open(os.path.join(ROOT, 'web/xr-paper-hub.html'), encoding='utf-8').read()
blocks = re.findall(r'<script[^>]*>(.*?)</script>', html, re.S)
outdir = os.path.join(ROOT, 'data', '_chk')
os.makedirs(outdir, exist_ok=True)
paths = []
for i, b in enumerate(blocks):
    p = os.path.join(outdir, f'hub_script_{i}.js')
    with open(p, 'w', encoding='utf-8') as f:
        f.write(b)
    paths.append(p)
    print(p, len(b), 'chars')
print('blocks', len(blocks))
