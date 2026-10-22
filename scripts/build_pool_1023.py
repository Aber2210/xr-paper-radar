# -*- coding: utf-8 -*-
# build_pool_1023.py — 构造 2026-10-23 主批 XR 池 + backfill-1023 池（含元数据）
import json, re
ROOT = "D:/Agent/WorkBuddy/Research"

rss = {}
for l in open(f"{ROOT}/data/raw/2026-10-23_rss.jsonl", encoding="utf-8"):
    if l.strip():
        d = json.loads(l); rss[d["base_id"]] = d
xr_abs = json.load(open(f"{ROOT}/data/missed_xr_abstract_1023.json", encoding="utf-8"))

def clean_ab(s):
    return s.split("Abstract:", 1)[-1].strip() if "Abstract:" in s else s.strip()

MAIN = ["2610.29014","2610.29517","2610.30032","2610.07217","2610.28821","2610.28962",
        "2610.29106","2610.29374","2610.29396","2610.29647","2610.29768","2610.29936",
        "2610.30013","2610.30089","2610.25988"]
BF = ["2610.26918","2610.27622","2610.28004","2610.28131","2610.28585",
      "2604.11685","2608.21009","2604.10809","2607.06464"]

def meta(bid):
    if bid in rss:
        d = rss[bid]
        return {"id": bid, "title": re.sub(r"\s+", " ", d["title"]).strip(),
                "abstract": clean_ab(d["abstract"]),
                "published": d.get("published", "")[:10],
                "primary_category": d.get("primary_category", "")}
    if bid in xr_abs:
        v = xr_abs[bid]
        return {"id": bid, "title": re.sub(r"\s+", " ", v["title"]).strip(),
                "abstract": v["abstract"], "published": v.get("published", ""),
                "primary_category": v.get("cat", "")}
    raise KeyError(bid)

main_pool = [meta(b) for b in MAIN]
bf_pool = [meta(b) for b in BF]
json.dump(main_pool, open(f"{ROOT}/data/xr_pool_2026-10-23.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
json.dump(bf_pool, open(f"{ROOT}/data/xr_pool_backfill_1023.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("main pool:", len(main_pool), "| backfill pool:", len(bf_pool))
for p in main_pool + bf_pool:
    print(" ", p["id"], p["published"], p["primary_category"], "|", p["title"][:80])
