# -*- coding: utf-8 -*-
"""修补 venue 字段：arXiv API 的 id_list 查询未返回 primary_category，导致「arXiv preprint（）」。

主批用 listing 摘要级命中文件的 cat 字段；backfill 用 RSS 的 primary_category。
同步修补 scored_1112.json / 报告章节行 / 原子笔记 frontmatter。
"""
import glob
import json
import re

sc_path = "data/scored_1112.json"
D = json.load(open(sc_path, encoding="utf-8"))
xr = json.load(open("data/missed_new_1112_xr.json", encoding="utf-8"))
rss = {json.loads(l)["base_id"]: json.loads(l) for l in open("data/raw/2026-11-12.jsonl", encoding="utf-8")}

fixed = 0
for p in D["main"] + D["backfill"]:
    cat = ""
    if p["id"] in xr:
        cat = xr[p["id"]]["cat"]
    elif p["id"] in rss:
        cat = rss[p["id"]].get("primary_category") or ""
    if not cat:
        print("NO CAT", p["id"])
        continue
    p["venue"] = f"arXiv preprint（{cat}）"
    fixed += 1
json.dump(D, open(sc_path, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("scored venue fixed", fixed)

# 报告：章节行
rp = "reports/XR-Daily-Report-2026-11-12.md"
s = open(rp, encoding="utf-8").read()
for p in D["main"] + D["backfill"]:
    old = f"### 第 "
    # 逐篇替换该章的 venue 片段
    pat = re.compile(r"(- \*\*赛道 / 场合\*\*：" + re.escape(p["track"]) + r" / )arXiv preprint（[^）]*）")
    s2 = pat.sub(lambda m: m.group(1) + p["venue"], s, count=0)
    s = s2
open(rp, "w", encoding="utf-8").write(s)
print("report remaining empty venue:", s.count("arXiv preprint（）"))

# 笔记 frontmatter
n = 0
for f in glob.glob("papers/notes/*.md"):
    t = open(f, encoding="utf-8").read()
    if "venue: arXiv preprint（）" in t or "venue: arXiv preprint\n" in t:
        body = t
        for p in D["main"] + D["backfill"]:
            if f"id: arXiv:{p['id']}" in body:
                body = re.sub(r"^venue: .*$", f"venue: {p['venue']}", body, count=1, flags=re.M)
                break
        if body != t:
            open(f, "w", encoding="utf-8").write(body)
            n += 1
print("notes venue fixed", n)
left = [f for f in glob.glob("papers/notes/*.md") if "arXiv preprint（）" in open(f, encoding="utf-8").read()]
print("notes still empty:", len(left))
