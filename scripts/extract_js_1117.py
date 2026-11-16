# -*- coding: utf-8 -*-
"""抽出 web/xr-paper-hub.html 的 <script> 块，落盘供 node --check（项目内路径，避免 /tmp 跨工具坑）。"""
import os
import re

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
html = open(os.path.join(ROOT, 'web/xr-paper-hub.html'), encoding='utf-8').read()
out = os.path.join(ROOT, 'data', '_chk')
os.makedirs(out, exist_ok=True)
blocks = re.findall(r'<script[^>]*>(.*?)</script>', html, re.S)
n = 0
for i, b in enumerate(blocks):
    if len(b.strip()) < 50:
        continue
    p = os.path.join(out, f'block{i}.js')
    open(p, 'w', encoding='utf-8').write(b)
    print(f'{p}: {len(b)} chars')
    n += 1
print('blocks written:', n)
