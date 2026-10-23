# -*- coding: utf-8 -*-
"""抽出 web/xr-paper-hub.html 内联 <script> 块，node --check 语法校验。"""
import re, subprocess, os, tempfile
h = open('web/xr-paper-hub.html', encoding='utf-8').read()
blocks = re.findall(r'<script(?:\s[^>]*)?>(.*?)</script>', h, re.S)
node = r'C:\Users\Admin\.workbuddy\binaries\node\versions\22.22.2-6\node.exe'
ok = True
for i, b in enumerate(blocks):
    if not b.strip():
        continue
    if 'src=' in (re.search(r'<script([^>]*)>', h[h.index(b)-200:h.index(b)+10]).group(1) if h.index(b) > 200 else ''):
        pass
    fd, path = tempfile.mkstemp(suffix='.js', dir=os.environ.get('TEMP', '.'))
    os.write(fd, b.encode('utf-8'))
    os.close(fd)
    r = subprocess.run([node, '--check', path], capture_output=True, text=True)
    status = 'OK' if r.returncode == 0 else 'SYNTAX ERROR'
    if r.returncode != 0:
        ok = False
        print(f'block {i}: {status}\n{r.stderr[:600]}')
    else:
        print(f'block {i}: {status} ({len(b)} chars)')
    os.remove(path)
print('ALL BLOCKS OK' if ok else 'BLOCK CHECK FAILED')
