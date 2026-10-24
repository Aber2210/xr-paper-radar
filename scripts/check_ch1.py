# -*- coding: utf-8 -*-
"""解析渠道①线上 Hub 的 DATA 计数（2026-10-25 核验）"""
import json, re, sys

p = "D:/Agent/WorkBuddy/Research/data/tmp_check/ch1_hub.html"
h = open(p, encoding="utf-8", errors="ignore").read()
start = h.find("const DATA = ")
if start < 0:
    print("FATAL: const DATA not found in channel1 page"); sys.exit(1)
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
print("channel1 serving: papers=%d notes=%d batches=%d" % (
    len(d.get("papers", [])), len(d.get("notes", [])), len(d.get("batches", []))))
batches = sorted(set(p2.get("batch", "") for p2 in d["papers"] if p2.get("batch")))
print("latest 4 batches served:", batches[-4:])
b25 = [b for b in d["batches"] if b.get("key") == "2026-10-25"]
print("has 2026-10-25 batch:", bool(b25))
