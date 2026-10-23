# -*- coding: utf-8 -*-
import json, glob
h = open('web/xr-paper-hub.html', encoding='utf-8').read()
i = h.index('const DATA = ')
start = h.index('{', i)
depth = 0; instr = False; esc = False
end = None
for j in range(start, len(h)):
    c = h[j]
    if instr:
        if esc:
            esc = False
        elif c == '\\':
            esc = True
        elif c == '"':
            instr = False
        continue
    if c == '"':
        instr = True
    elif c == '{':
        depth += 1
    elif c == '}':
        depth -= 1
        if depth == 0:
            end = j + 1
            break
d = json.loads(h[start:end])
papers = d['papers']; notes = d.get('notes', []); batches = d.get('batches', [])
print('HTML papers:', len(papers), 'notes:', len(notes), 'batches:', len(batches))
reg = sum(1 for l in open('papers/library/registry.jsonl', encoding='utf-8') if l.strip())
nd = len(glob.glob('papers/notes/*.md'))
print('disk registry:', reg, 'notes:', nd)
ids = [p['id'] for p in papers]
print('dup ids:', len(ids) - len(set(ids)))
for x in batches:
    if '1024' in x['key']:
        print('batch:', x['key'], 'count:', x['count'], 'label:', x['label'])
b1024 = [p for p in papers if p['batch'] == '2026-10-24']
print('1024 papers in DATA:', len(b1024), 'top10:', sum(1 for p in b1024 if p['top10']))
bf = [p for p in papers if p['batch'] == 'backfill-1024']
print('backfill-1024 papers:', len(bf), 'top10 flags:', sum(1 for p in bf if p['top10']))
# 一致性断言
assert len(papers) == reg, 'papers != registry'
assert len(notes) == nd, 'notes != disk'
assert len(b1024) == 17 and len(bf) == 4
print('ALL COUNTS CONSISTENT')
