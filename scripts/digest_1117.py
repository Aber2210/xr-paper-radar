# -*- coding: utf-8 -*-
# digest_1117.py — 从 L0/L1 全文抽取结构化摘要（摘要/引言/方法/实验/结论），供 7 维评分与笔记精读。
import os, re

ROOT = "D:/Agent/WorkBuddy/Research"
FT = f"{ROOT}/data/fulltext"
OUT = f"{ROOT}/data/digest_1117"
os.makedirs(OUT, exist_ok=True)

HDR = re.compile(
    r"^\s*(?:(?:\d+(?:\.\d+)*|[IVXLC]{1,4})\.?\s+)?"
    r"(Abstract|Introduction|Related Work|Background|Preliminaries|Problem Formulation|Formulation|"
    r"Method|Methods|Methodology|Approach|Model|Architecture|System|System Design|"
    r"Implementation|Training|Experiment|Experiments|Experimental Setup|Results|Evaluation|"
    r"Ablation|Analysis|Discussion|Conclusion|Conclusions|Limitations)\b",
    re.I | re.M)

MAIN = ["2611.18438", "2611.18256", "2611.18170", "2611.18099", "2611.17957", "2611.17752",
        "2611.18340", "2611.17755", "2611.17458", "2611.17619", "2611.18243", "2611.17828",
        "2611.17903"]
BF = ["2501.12764", "2608.19372", "2611.17238"]


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
        parts.append("【摘要】\n" + ab[0][:2000])
    intro = " ".join(sec.get("Introduction", []))
    if intro:
        parts.append("【引言】\n" + intro[:2600])
    meth = " ".join(sec.get("Method", []) + sec.get("Methods", []) + sec.get("Methodology", [])
                    + sec.get("Approach", []) + sec.get("Model", []) + sec.get("Architecture", [])
                    + sec.get("System", []) + sec.get("System Design", [])
                    + sec.get("Implementation", []) + sec.get("Training", []))
    if meth:
        parts.append("【方法】\n" + meth[:6000])
    exp = " ".join(sec.get("Experiment", []) + sec.get("Experiments", [])
                   + sec.get("Experimental Setup", []) + sec.get("Results", [])
                   + sec.get("Evaluation", []) + sec.get("Ablation", []) + sec.get("Analysis", []))
    if exp:
        parts.append("【实验】\n" + exp[:6000])
    con = " ".join(sec.get("Conclusion", []) + sec.get("Conclusions", [])
                   + sec.get("Discussion", []) + sec.get("Limitations", []))
    if con:
        parts.append("【结论/局限】\n" + con[:2000])
    digest = "\n\n".join(parts)
    digest = re.sub(r"\n{3,}", "\n\n", digest)
    with open(f"{OUT}/{bid}.txt", "w", encoding="utf-8") as fh:
        fh.write(digest)
    print(f"{bid}: digest {len(digest)} chars (sections: {list(sec.keys())[:10]})")
print("done ->", OUT)
