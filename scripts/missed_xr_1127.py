# -*- coding: utf-8 -*-
"""2026-11-27 上一公告组（11-25）复采核验：569 篇未入馆者是否为真漏网。

口径（历史踩坑固化）：
- 摘要必须取上一批的 RSS 文件 data/raw/2026-11-26_all.jsonl（今日文件只含今日组）。
- 处置集合必须并入 registry、上一批 xr_pool / nonxr / old_replace / scored。
"""
import json, re, sys
sys.path.insert(0, "scripts")
from fetch_rss import kw_match
from kw_extra import EXTRA

PREV_DAY = "2026-11-25"


def main():
    missed_prev = json.load(open("data/missed_prev_1127.json", encoding="utf-8"))
    print("上一组未入馆（对账口径）:", len(missed_prev))

    reg = {}
    for l in open("papers/library/registry.jsonl", encoding="utf-8"):
        if l.strip():
            d = json.loads(l)
            reg[d["id"].split(":")[-1].split("v")[0]] = d

    disp = set(reg)
    for fn in ("data/xr_pool_1126.json", "data/nonxr_1126.json", "data/old_replace_1126.json"):
        try:
            disp |= set(json.load(open(fn, encoding="utf-8")))
        except FileNotFoundError:
            print("WARN 缺", fn)
    for r in json.load(open("data/scored_1126.json", encoding="utf-8")):
        disp.add(r["id"])

    ab = {}
    for fn in ("data/raw/2026-11-26_all.jsonl", "data/raw/2026-11-27.jsonl"):
        try:
            for l in open(fn, encoding="utf-8"):
                if not l.strip():
                    continue
                r = json.loads(l)
                ab.setdefault(r["base_id"], r)
        except FileNotFoundError:
            print("WARN 缺", fn)

    def clean(a):
        return re.sub(r"^arXiv:\S+\s+Announce Type:\s*\w+\s+Abstract:\s*", "", a or "").strip()

    no_abs, hits, leak = [], [], []
    for p, (cat, title) in sorted(missed_prev.items()):
        r = ab.get(p)
        if not r or len(clean(r.get("abstract", ""))) < 120:
            no_abs.append(p)
            continue
        txt = r["title"] + " " + clean(r["abstract"])
        t = r["title"].lower()
        if kw_match(txt) or any(w in t for w in EXTRA):
            hits.append((p, title[:70], cat))
            if p not in disp:
                leak.append((p, title[:80], cat))

    print("摘要覆盖 %d/%d = %.4f" % (len(missed_prev) - len(no_abs), len(missed_prev),
                                   (len(missed_prev) - len(no_abs)) / max(1, len(missed_prev))))
    print("召回层命中 %d 篇，其中不在上批处置集合（真漏网）%d 篇" % (len(hits), len(leak)))
    for x in leak:
        print("   LEAK", x)
    out = {"prev_day": PREV_DAY, "unregistered": len(missed_prev), "no_abstract": no_abs,
           "hits": [{"id": p, "title": t, "cat": c} for p, t, c in hits],
           "leak": [{"id": p, "title": t, "cat": c} for p, t, c in leak],
           "leak_n": len(leak)}
    json.dump(out, open("data/missed_xr_1127.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print("saved data/missed_xr_1127.json")


if __name__ == "__main__":
    main()
