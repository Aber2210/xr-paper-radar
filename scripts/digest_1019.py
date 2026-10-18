# -*- coding: utf-8 -*-
"""digest_1019.py — 从 L0 全文抽取结构化摘要（方法/实验/结论），供笔记精读，控制上下文体积。"""
import json, os, re
ROOT="D:/Agent/WorkBuddy/Research"
IDS=["2610.17474","2610.18183","2610.19152","2610.19413","2610.08700","2610.15074","2610.18746","2610.18872","2610.19857","2610.16252","2610.13549","2610.19726","2610.14685","2610.19681","2610.19502","2610.19674","2610.14951","2610.13541","2610.18446","2610.16176","2610.08684","2610.08192","2610.18447","2610.17521"]
FT=f"{ROOT}/data/fulltext"
OUT=f"{ROOT}/data/digest_1019"
os.makedirs(OUT,exist_ok=True)

HDR=re.compile(r"^\s*(?:(?:\d+(?:\.\d+)*|I{1,3}V?X?|IV|IX)\.?\s+)?(Abstract|Introduction|Related Work|Method|Methods|Approach|Model|Architecture|Implementation|Experiment|Experiments|Results|Evaluation|Discussion|Conclusion|Limitations)\b",re.I|re.M)
def sections(text):
    ms=list(HDR.finditer(text))
    out={}
    for i,m in enumerate(ms):
        name=m.group(1).capitalize()
        start=m.end(); end=ms[i+1].start() if i+1<len(ms) else len(text)
        body=text[start:end].strip()
        out.setdefault(name,[]).append(body)
    return out

for bid in IDS:
    p=f"{FT}/{bid}.txt"
    if not os.path.exists(p):
        print("MISS",bid); continue
    text=open(p,encoding="utf-8").read()
    text=re.sub(r"^# LEVEL.*?^[@\n]+\n","",text,flags=re.S)
    sec=sections(text)
    parts=[]
    ab=sec.get("Abstract")
    if ab: parts.append("【摘要】\n"+ab[0][:1500])
    meth=" ".join(sec.get("Method",[])+sec.get("Methods",[])+sec.get("Approach",[])+sec.get("Model",[])+sec.get("Architecture",[])+sec.get("Implementation",[]))
    if meth: parts.append("【方法】\n"+meth[:3000])
    exp=" ".join(sec.get("Experiment",[])+sec.get("Experiments",[])+sec.get("Results",[])+sec.get("Evaluation",[]))
    if exp: parts.append("【实验】\n"+exp[:2600])
    con=" ".join(sec.get("Conclusion",[])+sec.get("Discussion",[])+sec.get("Limitations",[]))
    if con: parts.append("【结论/局限】\n"+con[:1200])
    digest="\n\n".join(parts)
    digest=re.sub(r"\n{3,}","\n\n",digest)
    open(f"{OUT}/{bid}.txt","w",encoding="utf-8").write(digest)
    print(f"{bid}: digest {len(digest)} chars")
print("done ->",OUT)
