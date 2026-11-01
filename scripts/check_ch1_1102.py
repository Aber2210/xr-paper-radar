# -*- coding: utf-8 -*-
"""核验渠道①线上服务版本（2026-11-02）：解析 const DATA 计数"""
import json, sys

p = sys.argv[1] if len(sys.argv) > 1 else "data/_ch1_check.html"
h = open(p, encoding="utf-8").read()
print("bytes:", len(h))
start = h.find("const DATA = ")
if start < 0:
    print("no DATA (可能是跳转桩/错误页)")
    print("head:", h[:200])
    sys.exit(2)
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
print("CH1 online: papers=%d notes=%d batches=%d" % (len(d["papers"]), len(d["notes"]), len(d["batches"])))
print("has 11-02 batch:", any(b.get("key") == "2026-11-02" for b in d["batches"]))
print("newest batch keys:", [b.get("key") for b in d["batches"][-3:]])
