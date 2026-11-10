"""校验 hub 页内联 script 语法 + DATA 关键断言（node --check 前置抽块）。"""
import re, json, subprocess, os

html = open('web/xr-paper-hub.html', encoding='utf-8').read()
blocks = re.findall(r'<script(?![^>]*src=)[^>]*>(.*?)</script>', html, re.S)
print('script blocks:', len(blocks), [len(b) for b in blocks])
os.makedirs('data/_check', exist_ok=True)
ok = True
for i, b in enumerate(blocks):
    p = f'data/_check/hub_block_{i}.js'
    open(p, 'w', encoding='utf-8').write(b)
    r = subprocess.run(['node', '--check', p], capture_output=True, text=True)
    print(f'block {i}: rc={r.returncode}', (r.stderr or '').strip()[:300])
    ok = ok and r.returncode == 0

i = html.find('const DATA = ')
d = json.JSONDecoder().raw_decode(html[i + len('const DATA = '):])[0]
print('DATA papers/notes/batches:', len(d['papers']), len(d['notes']), len(d['batches']))
b11 = [b for b in (d['batches'] if isinstance(d['batches'], list) else d['batches'].values()) if b.get('key') == '2026-11-11']
print('batch 2026-11-11:', b11[0] if b11 else 'MISSING')
newp = [p for p in d['papers'] if p.get('batch') == '2026-11-11']
print('papers in 2026-11-11:', len(newp), 'top10:', sum(1 for p in newp if p.get('top10')))
bf = [p for p in d['papers'] if p.get('batch') == 'backfill-1111']
print('papers in backfill-1111:', len(bf))
print('OVERALL', 'PASS' if ok and len(d['papers']) == 888 and len(d['notes']) == 548 and len(d['batches']) == 56 and b11 and len(newp) == 31 and len(bf) == 8 else 'FAIL')
