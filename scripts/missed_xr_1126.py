# -*- coding: utf-8 -*-
"""上一公告组（2026-11-24 / 1,045 篇唯一）未入馆复采核验（第 1 步配套）。

口径：把 11-24 组未入馆的 977 篇用 11-25 与 11-26 两轮 RSS 全量核摘要 + 标题级扩展词复扫，
命中的每一篇都必须落在上批（1125）的处置集合内（scored_1125 / xr_pool_1125 / nonxr_1125 /
old_replace_1125），否则即为真漏网，需写入 missed_xr_1126.json 并上报。
"""
import json
import re
import sys

sys.path.insert(0, 'scripts')
from fetch_rss import kw_match
from triage_1126 import EXTRA

REG = set()
for line in open('papers/library/registry.jsonl', encoding='utf-8'):
    if line.strip():
        d = json.loads(line)
        REG.add(d['id'].split(':')[-1].split('v')[0])

MISS = json.load(open('data/missed_prev_1126.json', encoding='utf-8'))
print('11-24 组未入馆', len(MISS))

# 两轮 RSS 合并（11-25 全量含摘要 1,547 条；11-26 全量 921 条）
byid = {}
for fn in ('data/raw/2026-11-25_all_full.jsonl', 'data/raw/2026-11-26_all.jsonl'):
    for line in open(fn, encoding='utf-8'):
        if not line.strip():
            continue
        r = json.loads(line)
        byid.setdefault(r['base_id'], r)

cov = sum(1 for p in MISS if p in byid)
print('有摘要覆盖 %d/%d = %.4f' % (cov, len(MISS), cov / len(MISS)))

CLEAN = re.compile(r'^arXiv:\S+\s+Announce Type:\s*\w+\s+Abstract:\s*')


def abs_of(r):
    return CLEAN.sub('', r.get('abstract', '')).strip()


hits = {}
for pid, meta in MISS.items():
    r = byid.get(pid)
    title = (r or {}).get('title') or (meta[1] if len(meta) > 1 else '')
    body = abs_of(r) if r else ''
    txt = title + ' ' + body
    if r and kw_match(txt):
        hits[pid] = ['KW', title]
    else:
        low = title.lower()
        for k in EXTRA:
            if k in low:
                hits[pid] = ['TITLE_EXTRA:' + k, title]
                break
print('摘要/标题级命中', len(hits))

DISP = {}
for fn, tag in (('data/scored_1125.json', 'scored'),
                ('data/xr_pool_1125.json', 'pool'),
                ('data/nonxr_1125.json', 'nonxr'),
                ('data/old_replace_1125.json', 'old_replace')):
    try:
        d = json.load(open(fn, encoding='utf-8'))
    except FileNotFoundError:
        continue
    for pid in (d.keys() if isinstance(d, dict) else [x['id'] for x in d]):
        DISP.setdefault(pid, set()).add(tag)

leak = {}
for pid, (how, title) in hits.items():
    if pid in REG:
        DISP.setdefault(pid, set()).add('registry')
    if not (DISP.get(pid, set()) & {'scored', 'pool', 'nonxr', 'old_replace', 'registry'}):
        leak[pid] = [how, title]

out = {
    'prev_group': '2026-11-24',
    'unadmitted': len(MISS),
    'with_abstract': cov,
    'hits': {k: v for k, v in sorted(hits.items())},
    'disposition': {k: sorted(v) for k, v in sorted(DISP.items()) if k in hits},
    'leak': leak,
    'leak_n': len(leak),
}
json.dump(out, open('data/missed_xr_1126.json', 'w', encoding='utf-8'),
          ensure_ascii=False, indent=1)
print('真漏网', len(leak), list(leak)[:10])
print('命中处置分布', {k: sum(1 for v in DISP.values() if k in v) for k in ('scored', 'pool', 'nonxr', 'old_replace')})
