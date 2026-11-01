# -*- coding: utf-8 -*-
"""核验 GitHub Pages 线上版本与本地一致（2026-11-02）：DATA 计数 + 11-02 卡片"""
import json, sys

p = sys.argv[1] if len(sys.argv) > 1 else "data/_pages_check.html"
h = open(p, encoding="utf-8", errors="replace").read()
start = h.find("const DATA = ")
if start < 0:
    print("FATAL: no const DATA"); sys.exit(1)
start += len("const DATA = ")
depth = 0; i = start; instr = False; esc = False
while i < len(h):
    ch = h[i]
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
d = json.loads(h[start:i + 1])
print("PAGES online: papers=%d notes=%d batches=%d" % (len(d["papers"]), len(d["notes"]), len(d["batches"])))
b = [x for x in d["batches"] if x.get("key") == "2026-11-02"]
if b:
    print("11-02 card: count=%s refPapers=%d" % (b[0].get("count"), len(b[0].get("refPapers", []) or [])))
    print("11-02 label:", b[0].get("label"))
else:
    print("FATAL: 2026-11-02 batch missing on Pages")
ok = len(d["papers"]) == 717 and len(d["notes"]) == 408 and len(d["batches"]) == 41 and bool(b) and b[0].get("count") == 0 and len(b[0].get("refPapers", []) or []) == 24
print("RESULT:", "PASS" if ok else "FAIL")
sys.exit(0 if ok else 1)
