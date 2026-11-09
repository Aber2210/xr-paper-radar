# -*- coding: utf-8 -*-
# digest_1110.py — 从 L0 全文抽取结构化摘要（摘要/方法/实验/结论），供 7 维评分与笔记精读。
import json, os, re
ROOT = "D:/Agent/WorkBuddy/Research"
FT = f"{ROOT}/data/fulltext"
OUT = f"{ROOT}/data/digest_1110"
os.makedirs(OUT, exist_ok=True)

HDR = re.compile(r"^\s*(?:(?:\d+(?:\.\d+)*|I{1,3}V?X?|IV|IX)\.?\s+)?(Abstract|Introduction|Related Work|Method|Methods|Approach|Model|Architecture|Implementation|Experiment|Experiments|Results|Evaluation|Discussion|Conclusion|Limitations)\b", re.I | re.M)

MAIN = ["2611.09089", "2611.09129", "2611.09195", "2611.09238", "2611.09394", "2611.09708",
        "2611.09458", "2611.09036", "2611.09074", "2611.08731", "2611.09692", "2611.08578",
        "2611.09584", "2611.09524"]
BF = ["2511.18127", "2605.16981", "2605.31557", "2607.24409"]


def sections(text):
    ms = list(HDR.finditer(text))
    out = {}
    for i, m in enumerate(ms):
        name = m.group(1).capitalize()
        start = m.end()
        end = ms[i + 1].start() if i + 1 < len(ms) else len(text)
        out.setdefault(name, []).append(text[start:end].strip())
    return out


for bid in MAIN + BF:
    p = f"{FT}/{bid}.txt"
    if not os.path.exists(p):
        print("MISS", bid)
        continue
    text = open(p, encoding="utf-8").read()
    text = re.sub(r"^# LEVEL.*?^\[", "[", text, flags=re.S)
    sec = sections(text)
    parts = []
    ab = sec.get("Abstract")
    if ab:
        parts.append("【摘要】\n" + ab[0][:1800])
    intro = " ".join(sec.get("Introduction", []))
    if intro:
        parts.append("【引言】\n" + intro[:2200])
    meth = " ".join(sec.get("Method", []) + sec.get("Methods", []) + sec.get("Approach", []) + sec.get("Model", []) + sec.get("Architecture", []) + sec.get("Implementation", []))
    if meth:
        parts.append("【方法】\n" + meth[:4200])
    exp = " ".join(sec.get("Experiment", []) + sec.get("Experiments", []) + sec.get("Results", []) + sec.get("Evaluation", []))
    if exp:
        parts.append("【实验】\n" + exp[:4200])
    con = " ".join(sec.get("Conclusion", []) + sec.get("Discussion", []) + sec.get("Limitations", []))
    if con:
        parts.append("【结论/局限】\n" + con[:1800])
    digest = "\n\n".join(parts)
    digest = re.sub(r"\n{3,}", "\n\n", digest)
    with open(f"{OUT}/{bid}.txt", "w", encoding="utf-8") as fh:
        fh.write(digest)
    print(f"{bid}: digest {len(digest)} chars (sections: {list(sec.keys())})")
print("done ->", OUT)
