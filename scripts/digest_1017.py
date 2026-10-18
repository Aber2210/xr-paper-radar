#!/usr/bin/env python3
"""digest_1017.py — 抽取 10-16 批次候选论文的关键内容用于 7 维评分。"""
import re, sys, json

IDS = "2610.21121,2610.21067,2610.21386,2610.21484,2610.16186,2610.21634,2610.21668,2610.22363,2610.20904,2610.20958,2610.21282,2610.21619,2610.21199,2610.21353,2610.21965,2610.21409,2610.19541,2610.21588".split(",")

SEC_RE = re.compile(r'^(?:[IVXLC]+|\d+(?:\.\d+)*|[A-Z])\.?\s+[A-Z]', re.M)

def sections(text):
    lines = text.split('\n')
    secs, cur, buf = [], None, []
    for ln in lines:
        s = ln.strip()
        if not s:
            if cur: buf.append('')
            continue
        if SEC_RE.match(s) and len(s) < 90:
            if cur: secs.append((cur, '\n'.join(buf)))
            cur, buf = s, []
        else:
            if cur: buf.append(s)
    if cur: secs.append((cur, '\n'.join(buf)))
    return secs

def grab(secs, keys, maxc=1400):
    for k, v in secs:
        kl = k.lower()
        if any(x in kl for x in keys):
            return v[:maxc]
    return ''

for pid in IDS:
    try:
        text = open(f'data/fulltext/{pid}.txt', encoding='utf-8').read()
    except FileNotFoundError:
        print(f'==== {pid} MISSING'); continue
    # 去掉文件头
    body = text.split('# FETCHED', 1)[-1]
    body = re.sub(r'^.*?License: arXiv.*?\n', '', body, flags=re.S)
    secs = sections(body)
    print(f'\n########## {pid} ##########')
    m = re.search(r'Abstract\s*\n(.*?)\n\s*(?:1\s|I\s|Introduction)', body, re.S)
    if m:
        print('[ABSTRACT]', re.sub(r'\s+', ' ', m.group(1))[:700])
    for keys, tag in [(['method', 'approach', 'model', 'framework'], 'METHOD'),
                      (['experiment', 'evaluation', 'result', 'setup'], 'EXP'),
                      (['ablation'], 'ABLATION'),
                      (['conclusion', 'limitation', 'discussion'], 'CONCL')]:
        c = grab(secs, keys)
        if c:
            print(f'[{tag}]', re.sub(r'\s+', ' ', c)[:1100])
            print()
