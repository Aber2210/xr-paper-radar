# -*- coding: utf-8 -*-
"""Inspect 2026-10-03 raw pull vs registry: date distribution + new vs already-in-library."""
import json, re
RAW = "data/raw/2026-10-03.jsonl"
REG = "papers/library/registry.jsonl"

raw = [json.loads(l) for l in open(RAW, encoding="utf-8") if l.strip()]
reg_ids = set()
for l in open(REG, encoding="utf-8"):
    l = l.strip()
    if not l: continue
    try: reg_ids.add(json.loads(l)["id"].split(":")[-1].split("v")[0])
    except: pass

print("RAW count:", len(raw))
from collections import Counter
dates = Counter(r.get("published","")[:10] for r in raw)
print("Published date distribution:", dict(sorted(dates.items())))
print()
print(f"{'base_id':14} {'published':12} {'in_reg':6} title")
new = []
for r in sorted(raw, key=lambda x:x.get("published",""), reverse=True):
    bid = r["base_id"]
    inreg = bid in reg_ids
    if not inreg: new.append(bid)
    print(f"{bid:14} {r.get('published','')[:10]:12} {str(inreg):6} {r.get('title','')[:70]}")
print()
print("NEW (not in registry):", len(new))
for b in new: print("  ", b)
