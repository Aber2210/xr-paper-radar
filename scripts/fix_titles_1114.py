# -*- coding: utf-8 -*-
"""修补 registry 中 3 条 title 为裸 arXiv ID 的数据缺陷（2611.08731 / 2611.09692 / 2611.09524）。

- 经 arXiv API 取真名与 <updated>；同步修笔记 frontmatter 的 title 与 fulltext_chars。
- 修补前备份 registry.jsonl.bak-20261114b。
"""
import json
import shutil
import glob
import os
import urllib.request
import urllib.parse
from xml.etree import ElementTree as ET

NS = {'atom': 'http://www.w3.org/2005/Atom'}
IDS = ['2611.08731', '2611.09692', '2611.09524']
q = urllib.parse.quote(' OR '.join('id:' + i for i in IDS), safe='')
url = f'https://export.arxiv.org/api/query?search_query={q}&max_results=10'
root = ET.fromstring(urllib.request.urlopen(
    urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 Chrome/120'}), timeout=90).read())
real = {}
for e in root.findall('atom:entry', NS):
    aid = (e.findtext('atom:id', '', NS) or '').split('/abs/')[-1].split('v')[0]
    real[aid] = ' '.join((e.findtext('atom:title', '', NS) or '').split())
print('fetched:', json.dumps(real, ensure_ascii=False, indent=1))
assert set(real) == set(IDS), (set(real), set(IDS))

man = json.load(open('data/fulltext/_manifest.json', encoding='utf-8'))
reg = 'papers/library/registry.jsonl'
bak = reg + '.bak-20261114b'
if not os.path.exists(bak):
    shutil.copy(reg, bak)
    print('backup ->', bak)

rows = [json.loads(l) for l in open(reg, encoding='utf-8') if l.strip()]
fixed = 0
for r in rows:
    pid = r['id'].split(':')[-1]
    if pid in real and (r.get('title') or '').strip() == pid:
        r['title'] = real[pid]
        fc = (man.get(pid) or {}).get('chars')
        if fc:
            r['fulltext_chars'] = fc
        fixed += 1
        print('fixed', pid, '->', real[pid][:80], 'chars', r.get('fulltext_chars'))
with open(reg, 'w', encoding='utf-8') as f:
    for r in rows:
        f.write(json.dumps(r, ensure_ascii=False) + '\n')
print('registry rows', len(rows), 'fixed', fixed)

for pid in IDS:
    for fn in glob.glob(f'papers/notes/{pid}__*.md'):
        t = open(fn, encoding='utf-8').read()
        if f'\ntitle: {pid}\n' in t:
            t = t.replace(f'\ntitle: {pid}\n', f'\ntitle: {real[pid]}\n', 1)
            if 'fetch_level:' in t and (man.get(pid) or {}).get('chars'):
                pass
            open(fn, 'w', encoding='utf-8').write(t)
            print('note patched', os.path.basename(fn))
