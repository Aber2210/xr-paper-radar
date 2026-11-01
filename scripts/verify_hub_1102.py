# -*- coding: utf-8 -*-
"""核验 web/xr-paper-hub.html 内 DATA 计数与磁盘一致（2026-11-02 批次）"""
import json, glob, os, sys

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
    print("MISMATCH batches"); ok = False

b = [x for x in data["batches"] if x.get("key") == "2026-11-02"]
if b:
    print("11-02 batch label:", b[0].get("label"))
    print("11-02 count:", b[0].get("count"), "| refPapers:", len(b[0].get("refPapers", []) or []))
else:
    print("FATAL: 2026-11-02 batch missing"); ok = False

print("RESULT:", "PASS" if ok else "FAIL")
sys.exit(0 if ok else 1)
