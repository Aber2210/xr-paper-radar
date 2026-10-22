# -*- coding: utf-8 -*-
# digest_1023.py — 从 L0 全文抽取结构化摘要（摘要/方法/实验/结论），供 7 维评分与笔记精读。
import json, os, re
ROOT = "D:/Agent/WorkBuddy/Research"
FT = f"{ROOT}/data/fulltext"
OUT = f"{ROOT}/data/digest_1023"
os.makedirs(OUT, exist_ok=True)

HDR = re.compile(r"^\s*(?:(?:\d+(?:\.\d+)*|I{1,3}V?X?|IV|IX)\.?\s+)?(Abstract|Introduction|Related Work|Method|Methods|Approach|Model|Architecture|Implementation|Experiment|Experiments|Results|Evaluation|Discussion|Conclusion|Limitations)\b", re.I | re.M)

def sections(text):
    ms = list(HDR.finditer(text))
    out = {}
    for i, m in enumerate(ms):
        name = m.group(1).capitalize()
        start = m.end(); end = ms[i+1].start() if i+1 < len(ms) else len(text)
        body = text[start:end].strip()
        out.setdefault(name, []).append(body)
    return out

pools = {}
for f in ("xr_pool_2026-10-23.json", "xr_pool_backfill_1023.json"):
    for item in json.load(open(f"{ROOT}/data/{f}", encoding="utf-8")):
        pools[item["id"]] = item

for bid, item in pools.items():
    p = f"{FT}/{bid}.txt"
    if not os.path.exists(p):
        print("MISS", bid); continue
    text = open(p, encoding="utf-8").read()
    text = re.sub(r"^# LEVEL.*?^[@\n]+\n", "", text, flags=re.S)
    text = re.sub(r"^# (EVIDENCE|CHARS|URL).*\n", "", text, flags=re.M)
    sec = sections(text)
    parts = []
    ab = sec.get("Abstract")
    if ab: parts.append("【摘要】\n" + ab[0][:1600])
    meth = " ".join(sec.get("Method", []) + sec.get("Methods", []) + sec.get("Approach", []) + sec.get("Model", []) + sec.get("Architecture", []) + sec.get("Implementation", []))
    if meth: parts.append("【方法】\n" + meth[:3400])
    exp = " ".join(sec.get("Experiment", []) + sec.get("Experiments", []) + sec.get("Results", []) + sec.get("Evaluation", []))
    if exp: parts.append("【实验】\n" + exp[:3200])
    con = " ".join(sec.get("Conclusion", []) + sec.get("Discussion", []) + sec.get("Limitations", []))
    if con: parts.append("【结论/局限】\n" + con[:1400])
    digest = "\n\n".join(parts)
    digest = re.sub(r"\n{3,}", "\n\n", digest)
    open(f"{OUT}/{bid}.txt", "w", encoding="utf-8").write(digest)
    print(f"{bid}: digest {len(digest)} chars (sections: {list(sec.keys())})")
print("done ->", OUT)
