# -*- coding: utf-8 -*-
"""核验 web/xr-paper-hub.html 内 DATA 计数与磁盘一致（2026-10-25 批次）"""
import re, json, glob, os, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
html = open(os.path.join(ROOT, "web", "xr-paper-hub.html"), encoding="utf-8").read()

start = html.find("const DATA = ")
if start < 0:
    print("FATAL: const DATA not found"); sys.exit(1)
start += len("const DATA = ")
depth = 0; i = start; instr = False; esc = False
while i < len(html):
    ch = html[i]
    if instr:
        if esc: esc = False
        elif ch == "\\": esc = True
        elif ch == '"': instr = False
    else:
        if ch == '"': instr = True
        elif ch == "{": depth += 1
        elif ch == "}":
            depth -= 1
            if depth == 0: break
    i += 1
data = json.loads(html[start:i + 1])

reg = sum(1 for l in open(os.path.join(ROOT, "papers/library/registry.jsonl"), encoding="utf-8") if l.strip())
notes = len(glob.glob(os.path.join(ROOT, "papers/notes/*.md")))
daily = len(glob.glob(os.path.join(ROOT, "papers/daily/*")))

print("HTML DATA: papers=%d notes=%d batches=%d" % (len(data["papers"]), len(data["notes"]), len(data["batches"])))
print("DISK     : registry=%d notes=%d daily_dirs=%d" % (reg, notes, daily))

ok = True
if len(data["papers"]) != reg:
    print("MISMATCH papers"); ok = False
if len(data["notes"]) != notes:
    print("MISMATCH notes"); ok = False
if len(data["batches"]) != daily:
    print("MISMATCH batches vs daily dirs"); ok = False

b25 = [b for b in data["batches"] if b.get("key") == "2026-10-25"]
for b in b25:
    print("10-25 batch: count=%d refPapers=%d label=%s" % (
        b.get("count", -1), len(b.get("refPapers") or []), b.get("batchLabel", "")))
    if b.get("count") != 0:
        print("FAIL: 10-25 count should be 0"); ok = False
    if len(b.get("refPapers") or []) != 21:
        print("FAIL: 10-25 refPapers should be 21"); ok = False

print("VERIFY:", "PASS" if ok else "FAIL")
sys.exit(0 if ok else 1)
