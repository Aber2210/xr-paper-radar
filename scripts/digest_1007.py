#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""v3：稳健定位正文起点（首个“章节标题+紧随段落”，否则首个段落），整段折叠输出 [BODY]。
abstract 用 RSS 原始摘要。输出 data/2026-10-07_digest.txt。
"""
import json, re, os, glob

FT_DIR = "data/fulltext/2026-10-07"
CORPUS = "data/2026-10-07_corpus.jsonl"
RAW = "data/raw/2026-10-07.jsonl"
OUT = "data/2026-10-07_digest.txt"

CHROME = {
    "report github issue","×","title:","content selection saved. describe the issue below:",
    "description:","submit without github","submit in github","arxiv is now an independent nonprofit!",
    "learn more","back to arxiv","why html?","report issue","back to abstract","download pdf",
    "we're on github!","give feedback","skip to main content","license","contact","terms of use",
    "privacy policy","accessibility","sitemap","help","back to top",
}
ANY_HEADER_RE = re.compile(r'^\s*(?:\d{1,2}(?:\.\d+)*|[IVXLC]{1,6}(?:-[A-Z0-9]+)?(?:\.\d+)*|[A-Z]\.?\d?)\.?\s+[A-Z][A-Za-z0-9\s\-:&,(/]+$')

def clean_lines(text):
    out = []
    for ln in text.splitlines():
        s = ln.strip()
        if not s or s.lower() in CHROME or (len(s) <= 2 and not s.isalnum()):
            continue
        out.append(s)
    return out

def is_header(line):
    return bool(ANY_HEADER_RE.match(line))

def find_body_start(lines):
    n = len(lines)
    # 优先：首个“标题 + 紧随段落”的位置（正文区，非 TOC）
    for i in range(n):
        if is_header(lines[i]):
            j = i + 1
            while j < n and not lines[j].strip():
                j += 1
            if j < n and not is_header(lines[j]) and len(lines[j].strip()) >= 40:
                return i
    # 退回：首个长段落
    for i in range(n):
        if not is_header(lines[i]) and len(lines[i].strip()) >= 80:
            return i
    return 0

def collapse(lines, n):
    txt = " ".join(lines)
    txt = re.sub(r'\s+', ' ', txt).strip()
    txt = txt[:n]
    # 折行，避免单行过长被 Read 截断
    out = []
    for i in range(0, len(txt), 150):
        out.append(txt[i:i+150])
    return "\n".join(out)

corpus = [json.loads(l) for l in open(CORPUS, encoding="utf-8")]
by_id = {c["base_id"]: c for c in corpus}
raw = {json.loads(l)["base_id"]: json.loads(l) for l in open(RAW, encoding="utf-8")}

parts = []
for fp in sorted(glob.glob(os.path.join(FT_DIR, "*.txt"))):
    bid = os.path.basename(fp).replace(".txt","")
    if bid == "_manifest" or bid not in by_id:
        continue
    c = by_id[bid]
    lines = clean_lines(open(fp, encoding="utf-8", errors="ignore").read())
    bs = find_body_start(lines)
    body = collapse(lines[bs:], 4200)
    abs_t = raw.get(bid, {}).get("abstract","")
    abs_t = re.sub(r'^arXiv:[\d.]+v\d+\s*Announce Type:[^\n]*', '', abs_t)
    abs_t = re.sub(r'^Abstract:\s*', '', abs_t).strip()
    parts.append(f"\n{'#'*90}\n# {bid} | {c['track']} | {c['title']}\n{'#'*90}")
    parts.append(f"\n[ABSTRACT]\n{collapse([abs_t], 1500)}")
    parts.append(f"\n[BODY]\n{body}")

open(OUT, "w", encoding="utf-8").write("\n".join(parts))
print(f"digest written: {OUT} ({len(parts)} blocks, {sum(len(p) for p in parts)} chars)")
