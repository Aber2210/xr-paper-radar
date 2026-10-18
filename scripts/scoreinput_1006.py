#!/usr/bin/env python3
"""Build a single consolidated score-input: RSS abstract + experiment/results excerpts."""
import re, json, os

IDS = ["2610.02322","2610.02697","2610.02715","2610.03162","2610.03192",
       "2610.03232","2610.03283","2610.03441","2610.03599","2610.03607"]
FT = "data/fulltext"

# abstracts from RSS
abs_map = {}
with open("data/raw/2026-10-06_rss.jsonl") as f:
    for line in f:
        line=line.strip()
        if not line: continue
        o=json.loads(line)
        if str(o.get('base_id')) in IDS:
            a=o.get('abstract','')
            a=re.sub(r'^arXiv:\S+\s+Announce Type: \w+\s+Abstract:\s*','',a)
            abs_map[str(o.get('base_id'))]=a

def sections(text):
    lines = text.splitlines()
    out=[]; cur_h=None; cur_b=[]
    hdr=re.compile(r'^\s*([0-9]+(?:\.[0-9]+)*|[IVXLC]+)\.?\s+[A-Z][A-Za-z].*')
    for ln in lines:
        if hdr.match(ln) and len(ln)<80:
            if cur_h is not None: out.append((cur_h,"\n".join(cur_b)))
            cur_h=ln.strip(); cur_b=[]
        else:
            if cur_h is not None: cur_b.append(ln)
    if cur_h is not None: out.append((cur_h,"\n".join(cur_b)))
    return out

def grab(text, keywords, maxchars=2600):
    out=[]
    for h,b in sections(text):
        hl=h.lower()
        if any(k in hl for k in keywords):
            b2=re.sub(r'\s+',' ',b).strip()
            out.append((h,b2[:maxchars]))
    return out

blob=[]
for bid in IDS:
    p=os.path.join(FT,f"{bid}.txt")
    txt=open(p,encoding="utf-8",errors="ignore").read() if os.path.exists(p) else ""
    blob.append(f"\n{'='*30}\n# {bid}\n{'='*30}")
    blob.append("\n## Abstract\n"+(abs_map.get(bid,"(none)")[:1700]))
    exp=grab(txt,["experiment","evaluation","result","benchmark","dataset","ablation","user study","comparison","quantitative"], 2600)
    blob.append("\n## Experiments/Results")
    for h,b in exp[:3]:
        blob.append(f"\n### {h}\n{b}")
    meth=grab(txt,["method","approach","system","pipeline","our ","design","technique","network","model","framework"], 2000)
    blob.append("\n## Method notes")
    for h,b in meth[:2]:
        blob.append(f"\n### {h}\n{b}")

open("data/briefs/_scoreinput.md","w",encoding="utf-8").write("\n".join(blob))
print("scoreinput written, chars:", len("\n".join(blob)))
