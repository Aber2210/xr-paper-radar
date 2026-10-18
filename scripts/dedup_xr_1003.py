# -*- coding: utf-8 -*-
"""XR-filtered RSS (45) vs registry：列出全部，并标出真正新（2610.* 且不在库）。"""
import json, re
from collections import Counter
XR = "data/raw/2026-10-03_xr.jsonl"
REG = "papers/library/registry.jsonl"
xr = [json.loads(l) for l in open(XR, encoding="utf-8") if l.strip()]
reg_ids = set()
for l in open(REG, encoding="utf-8"):
    l=l.strip()
    if not l: continue
    try: reg_ids.add(json.loads(l)["id"].split(":")[-1].split("v")[0])
    except: pass
print("XR 命中:", len(xr))
pref = Counter(re.match(r"(\d{4})", r["base_id"]).group(1) for r in xr)
print("年份前缀:", dict(pref))
print()
print(f"{'base_id':14} {'in_reg':6} {'track?':6} title")
new = []
for r in sorted(xr, key=lambda x:x['base_id']):
    bid=r["base_id"]; inreg = bid in reg_ids
    is_new = (bid not in reg_ids) and bid.startswith("2610")
    if is_new: new.append(r)
    tag = "NEW" if is_new else ("old" if inreg else "old-non2610")
    print(f"{bid:14} {str(inreg):6} {tag:6} {r.get('title','')[:64]}")
print("\n真正新（2610.* 且不在库）:", len(new))
for r in new: print("  ", r["base_id"], r.get('title','')[:70])
