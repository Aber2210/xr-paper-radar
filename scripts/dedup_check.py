#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""覆盖度校验第①关：当日候选 vs 文献库 的同质去重 (token Jaccard)。"""
import json
import re
import sys

STOP = set("""a an the of for and or to in on with by from at as is are be we our this that
it its via using based can may we propose present introduce towards toward novel
learning framework approach method results show shows while however both all one
two also more most than which when where such these those paper work works""".split())


def toks(s):
    s = re.sub(r"[^a-z0-9 ]", " ", (s or "").lower())
    return set(w for w in s.split() if len(w) > 2 and w not in STOP)


def jaccard(a, b):
    if not a or not b:
        return 0.0
    return len(a & b) / len(a | b)


def main():
    raw = {}
    for line in open("data/raw/2026-09-21.jsonl", encoding="utf-8"):
        r = json.loads(line)
        raw[r["base_id"]] = r

    lib = [json.loads(l) for l in open("papers/library/registry.jsonl", encoding="utf-8")]
    lib_items = []
    for r in lib:
        bid = r["id"].split(":")[-1].split("v")[0]
        t = (r.get("title") or "") + " " + (r.get("title_zh") or "")
        a = raw.get(bid, {}).get("abstract", "")
        lib_items.append((bid, r.get("title", "")[:70], toks(t + " " + a)))

    cands = [json.loads(l) for l in open("data/raw/2026-09-21_new.jsonl", encoding="utf-8")]
    cands.sort(key=lambda r: (r["published"][:10], r["base_id"]))

    print(f"{'ID':<13}{'MAXSIM':<8}{'最相似库内论文':<50}标题")
    print("-" * 150)
    rows = []
    for r in cands:
        ct = toks(r["title"] + " " + r["abstract"])
        best = (0.0, "", "")
        for bid, title, lt in lib_items:
            j = jaccard(ct, lt)
            if j > best[0]:
                best = (j, bid, title)
        rows.append((r["base_id"], best[0], best[1], best[2], r["title"][:60]))
        print(f"{r['base_id']:<13}{best[0]:<8.3f}{best[2]:<50}{r['title'][:60]}")

    print()
    print("=== sim > 0.62 疑似同质 ===")
    hit = [x for x in rows if x[1] > 0.62]
    if not hit:
        print("无")
    for x in hit:
        print(f"  {x[0]}  sim={x[1]:.3f}  vs {x[2]} ({x[3]})")

    print()
    print("=== sim 0.45 ~ 0.62 需人工复核 ===")
    mid = [x for x in rows if 0.45 <= x[1] <= 0.62]
    for x in sorted(mid, key=lambda z: -z[1]):
        print(f"  {x[0]}  sim={x[1]:.3f}  vs {x[2]} ({x[3]})")

    json.dump([{"id": x[0], "sim": round(x[1], 4), "vs": x[2], "vs_title": x[3]} for x in rows],
              open("data/dedup_sim.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)


if __name__ == "__main__":
    main()
