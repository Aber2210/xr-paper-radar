# -*- coding: utf-8 -*-
"""extract_sections_1009.py — 从 L0 全文抽取结构化摘要（方法/实验/结论），供笔记精读，控制上下文体积。"""
import json, os, re
ROOT="D:/Agent/WorkBuddy/Research"
TOP10=["2610.09304","2610.08941","2610.08978","2610.09455","2610.09853","2610.10538","2610.10539","2610.09274","2610.09821","2610.09444"]
FT=f"{ROOT}/data/fulltext/2026-10-09"
OUT=f"{ROOT}/data/digest_1009"
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

for bid in TOP10:
    p=f"{FT}/{bid}.txt"
    if not os.path.exists(p):
        print("MISS",bid); continue
    text=open(p,encoding="utf-8").read()
    # 去 LEVEL 头
    text=re.sub(r"^# LEVEL.*?^[@\n]+\n","",text,flags=re.S)
    sec=sections(text)
    parts=[]
    # Abstract
    ab=sec.get("Abstract")
    if ab: parts.append("【摘要】\n"+ab[0][:1600])
    # Method/Approach/Model/Architecture
    meth=" ".join(sec.get("Method",[])+sec.get("Methods",[])+sec.get("Approach",[])+sec.get("Model",[])+sec.get("Architecture",[])+sec.get("Implementation",[]))
    if meth: parts.append("【方法】\n"+meth[:3200])
    # Experiments/Results/Evaluation
    exp=" ".join(sec.get("Experiment",[])+sec.get("Experiments",[])+sec.get("Results",[])+sec.get("Evaluation",[]))
    if exp: parts.append("【实验】\n"+exp[:3000])
    # Conclusion/Discussion/Limitations
    con=" ".join(sec.get("Conclusion",[])+sec.get("Discussion",[])+sec.get("Limitations",[]))
    if con: parts.append("【结论/局限】\n"+con[:1400])
    digest="\n\n".join(parts)
    # 去多余空白
    digest=re.sub(r"\n{3,}","\n\n",digest)
    open(f"{OUT}/{bid}.txt","w",encoding="utf-8").write(digest)
    print(f"{bid}: digest {len(digest)} chars (sections: {list(sec.keys())})")
print("done ->",OUT)
