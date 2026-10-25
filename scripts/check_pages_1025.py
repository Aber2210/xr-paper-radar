# -*- coding: utf-8 -*-
"""比对本地与 GitHub Pages 线上 Hub 的 DATA 计数（2026-10-25）"""
import json, sys

def parse(p):
    h = open(p, encoding="utf-8", errors="ignore").read()
    s = h.find("const DATA = ")
    if s < 0:
        return None
    s += len("const DATA = ")
    depth = 0; i = s; instr = False; esc = False
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
    return json.loads(h[s:i + 1])

loc = parse("D:/Agent/WorkBuddy/Research/web/xr-paper-hub.html")
pg = parse("D:/Agent/WorkBuddy/Research/data/tmp_pages.html")
for name, d in [("local", loc), ("pages", pg)]:
    if d is None:
        print(name, "NO DATA"); sys.exit(1)
    b25 = [b for b in d["batches"] if b.get("key") == "2026-10-25"]
    print("%s: papers=%d notes=%d batches=%d | 10-25 batch=%s refPapers=%d" % (
        name, len(d["papers"]), len(d["notes"]), len(d["batches"]),
        bool(b25), len(b25[0].get("refPapers", [])) if b25 else 0))
ok = (len(loc["papers"]) == len(pg["papers"]) and len(loc["notes"]) == len(pg["notes"])
      and len(loc["batches"]) == len(pg["batches"])
      and any(b.get("key") == "2026-10-25" and b.get("count") == 0 for b in pg["batches"]))
print("PAGES MATCH:", "PASS" if ok else "FAIL")
sys.exit(0 if ok else 1)
