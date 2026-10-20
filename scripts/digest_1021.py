# -*- coding: utf-8 -*-
"""digest_1021.py — 2026-10-21 批次（31 主批次 + 10 backfill）证据浓缩，复用 1020 模式"""
import json, os, re, sys
ROOT="D:/Agent/WorkBuddy/Research"
IDS=['2610.24812','2610.24926','2610.26067','2610.24237','2610.24364','2610.24640','2610.26278','2610.26338','2610.26360','2610.26598','2610.24257','2610.24400','2610.24452','2610.24462','2610.25887','2610.26641','2610.25006','2610.26583','2610.26549','2610.26625','2610.26780','2610.25309','2610.24031','2610.23895','2610.25011','2610.25681','2610.24811','2610.23899','2610.26633','2610.24285','2610.23903',
     '2603.24591','2504.20829','2512.19283','2606.05102','2606.25430','2609.03892','2605.17661','2605.10760','2606.16881','2511.09397']
FT=f"{ROOT}/data/fulltext"
OUT=f"{ROOT}/data/digest_1021"
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
    if meth: parts.append("【方法】\n"+meth[:3200])
    exp=" ".join(sec.get("Experiment",[])+sec.get("Experiments",[])+sec.get("Results",[])+sec.get("Evaluation",[]))
    if exp: parts.append("【实验】\n"+exp[:2800])
    con=" ".join(sec.get("Conclusion",[])+sec.get("Discussion",[])+sec.get("Limitations",[]))
    if con: parts.append("【结论/局限】\n"+con[:1200])
    digest="\n\n".join(parts)
    digest=re.sub(r"\n{3,}","\n\n",digest)
    open(f"{OUT}/{bid}.txt","w",encoding="utf-8").write(digest)
    print(f"{bid}: digest {len(digest)} chars")
print("done ->",OUT)
