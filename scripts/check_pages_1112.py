# -*- coding: utf-8 -*-
"""核验 GitHub Pages 线上版本：Range 分块下载重组 → 解析 DATA → 与本地逐项比对。"""
import json
import re
import subprocess
import sys

URL = "https://aber2210.github.io/xr-paper-radar/"
TMP = "D:/Agent/.tmp/pages_1112.html"
CHUNK = 1024 * 1024


def head_len():
    out = subprocess.run(["curl", "-sI", URL], capture_output=True, text=True, timeout=60).stdout
    code = out.split("\n")[0].strip()
    ln = None
    for line in out.split("\n"):
        if line.lower().startswith("content-length:"):
            ln = int(line.split(":")[1].strip())
    return code, ln


code, total = head_len()
print("HEAD:", code, "content-length", total)
if not total:
    sys.exit("no content-length")

parts = []
pos = 0
while pos < total:
    end = min(pos + CHUNK - 1, total - 1)
    r = subprocess.run(["curl", "-s", "-r", f"{pos}-{end}", URL], capture_output=True, timeout=120)
    b = r.stdout
    if not b:
        sys.exit(f"empty chunk at {pos}")
    parts.append(b)
    pos += len(b)
raw = b"".join(parts)
print("downloaded", len(raw), "bytes (expected", total, ")")
open(TMP, "wb").write(raw)

h = raw.decode("utf-8", "replace")
print("has const DATA:", "const DATA" in h)
m = re.search(r"const DATA\s*=\s*", h)
if not m:
    sys.exit("DATA not found")
i = h.index("{", m.end())
d, _ = json.JSONDecoder().raw_decode(h[i:])
print("remote papers", len(d["papers"]), "notes", len(d["notes"]), "batches", len(d["batches"]))

loc = open("D:/Agent/WorkBuddy/Research/web/xr-paper-hub.html", encoding="utf-8").read()
m2 = re.search(r"const DATA\s*=\s*", loc)
i2 = loc.index("{", m2.end())
d2, _ = json.JSONDecoder().raw_decode(loc[i2:])
print("local  papers", len(d2["papers"]), "notes", len(d2["notes"]), "batches", len(d2["batches"]))

b12 = [b for b in d["batches"] if b["key"] == "2026-11-12"]
bf12 = [b for b in d["batches"] if b["key"] == "backfill-1112"]
for b in b12 + bf12:
    print("remote batch", b["key"], "count", b["count"], "grades", {g: sum(1 for p in b["papers"] if p["grade"] == g) for g in "SABC"})
print("remote 11-12 max", max(p["value"] for p in b12[0]["papers"]) if b12 else None)
print("remote has 11-12 papers:", sum(1 for p in d["papers"] if p.get("batch") == "2026-11-12"))
print("remote has bf-1112 papers:", sum(1 for p in d["papers"] if p.get("batch") == "backfill-1112"))
ok = (len(d["papers"]) == len(d2["papers"]) == 907 and len(d["notes"]) == len(d2["notes"]) == 564
      and len(b12) == 1 and b12[0]["count"] == 15 and len(bf12) == 1 and bf12[0]["count"] == 4)
print("PAGES CHECK:", "PASS" if ok else "FAIL")
