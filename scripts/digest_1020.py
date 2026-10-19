# -*- coding: utf-8 -*-
"""digest_1020.py — 同 1019，ID 换 2026-10-20 批次（12 当日新稿 + 8 backfill）"""
import json, os, re
ROOT="D:/Agent/WorkBuddy/Research"
IDS=['2610.22681', '2610.22720', '2610.22748', '2610.22778', '2610.22822', '2610.22878', '2610.23039', '2610.23050', '2610.23336', '2610.23496', '2610.23772', '2610.23833', '2610.21297', '2602.07891', '2602.11693', '2604.00852', '2604.02107', '2605.25563', '2606.28637', '2608.15060']
FT=f"{ROOT}/data/fulltext"
OUT=f"{ROOT}/data/digest_1020"
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
