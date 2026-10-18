#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Fix ASCII inner double-quotes in the PAPERS/REF data block of write_deliverables_1008.py.
Inner quotes (Chinese emphasis) must be Chinese curly quotes so they don't terminate Python strings.
Structural quotes (keys, value delimiters, scores dict) are preserved.
Outputs a valid JSON file data/scored_1008.json containing {"PAPERS":[...],"REF":[...]}.
"""
import re, json, os

SRC = "D:/Agent/WorkBuddy/Research/scripts/write_deliverables_1008.py"
OUT = "D:/Agent/WorkBuddy/Research/data/scored_1008.json"

src = open(SRC, encoding="utf-8").read()

KEY_RE = re.compile(r'"([A-Za-z_]+)":')          # a key like "id":
CLOSE_RE = re.compile(r'\s*([,}\])]|"([A-Za-z_]+)":)')  # value delimiter follows

def fix_line(line):
    out = []
    i = 0
    n = len(line)
    in_value = False
    inner_open = True  # next inner quote is opening
    while i < n:
        c = line[i]
        if c == '"':
            m = KEY_RE.match(line, i)
            if m:
                # key open+close+colon emitted as-is
                out.append('"' + m.group(1) + '":')
                i = m.end()
                # skip spaces after colon
                while i < n and line[i] in ' \t':
                    out.append(line[i]); i += 1
                if i < n and line[i] == '"':
                    out.append('"'); i += 1; in_value = True; inner_open = True
                elif i < n and line[i] == '{':
                    # scores dict: copy verbatim until balanced
                    depth = 0
                    while i < n:
                        ch = line[i]
                        out.append(ch); i += 1
                        if ch == '{': depth += 1
                        elif ch == '}':
                            depth -= 1
                            if depth == 0:
                                break
                    in_value = False
                continue
            else:
                # not a key: inside value (open/inner/close) or stray
                if in_value:
                    rest = line[i+1:]
                    if CLOSE_RE.match(rest) or rest == '':
                        # value close
                        out.append('"'); i += 1; in_value = False
                    else:
                        # inner quote -> Chinese curly (alternate)
                        out.append('“' if inner_open else '”')
                        i += 1; inner_open = not inner_open
                else:
                    # value open not preceded by detected key (rare) -> keep ASCII
                    out.append('"'); i += 1; in_value = True; inner_open = True
        elif c in '{}[]()':
            out.append(c); i += 1
        else:
            out.append(c); i += 1
    return ''.join(out)

# Locate PAPERS and REF blocks
def extract_list(name):
    pat = re.compile(r'%s\s*=\s*\[' % re.escape(name))
    m = pat.search(src)
    if not m:
        raise RuntimeError("cannot find " + name)
    start = m.end()  # position right after '['
    depth = 1
    i = start
    n = len(src)
    while i < n:
        if src[i] == '[':
            depth += 1
        elif src[i] == ']':
            depth -= 1
            if depth == 0:
                break
        i += 1
    inner = src[start:i]  # text between [ and ]
    return inner

def parse_list(inner):
    # split into lines, fix each, then eval as a Python list literal
    fixed_lines = []
    changed = 0
    for ln in inner.split('\n'):
        fl = fix_line(ln)
        if fl != ln:
            changed += 1
        fixed_lines.append(fl)
    fixed = '\n'.join(fixed_lines)
    # build a module and eval the list
    expr = '[' + fixed + ']'
    # safety: only allow literals
    import ast
    try:
        val = ast.literal_eval(expr)
    except Exception as e:
        # fall back: write fixed to a temp file for inspection
        open("D:/Agent/WorkBuddy/Research/data/_fixed_1008.txt","w",encoding="utf-8").write(expr)
        raise
    return val, changed

papers, c1 = parse_list(extract_list("PAPERS"))
ref, c2 = parse_list(extract_list("REF"))

out = {"PAPERS": papers, "REF": ref}
json.dump(out, open(OUT, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("PAPERS:", len(papers), "REF:", len(ref))
print("lines changed PAPERS:", c1, "REF:", c2)
print("wrote", OUT)
