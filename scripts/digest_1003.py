# -*- coding: utf-8 -*-
"""Build a compact digest (abstract+intro+method+exp) per paper for scoring."""
import re, os
FT = "data/fulltext"
IDS = ["2610.00040","2610.00069","2610.00195","2610.01863","2609.11434","2609.09158"]
HEAD = re.compile(r"^\s*(?:\d+[.\s]+|[IVXLC]+[.\s]+)?"
                  r"(Abstract|Introduction|Related Work|Method|Methods|Approach|"
                  r"Proposed|Model|Architecture|Experiment|Experiments|Evaluation|"
                  r"Results|Result|Implementation|Conclusion|Discussion)\b", re.I)
def sections(text):
    lines = text.splitlines()
    idx = []
    for i,l in enumerate(lines):
        if HEAD.match(l):
            idx.append((i, l.strip()[:60]))
    return idx
def grab(text, name, nchars=2600):
    lines = text.splitlines()
    hdr = re.compile(r"^\s*(?:\d+[.\s]+|[IVXLC]+[.\s]+)?"+name+r"\b", re.I)
    for i,l in enumerate(lines):
        if hdr.match(l):
            buf=[]
            for j in range(i+1, min(i+120, len(lines))):
                if HEAD.match(lines[j]): break
                buf.append(lines[j])
            s="\n".join(buf).strip()
            return s[:nchars]
    return ""
out=[]
for bid in IDS:
    p=os.path.join(FT, bid+".txt")
    if not os.path.exists(p):
        out.append(f"\n##### {bid}: FILE MISSING #####\n"); continue
    t=open(p,encoding="utf-8",errors="replace").read()
    # strip header lines
    body=t.split("\n",5)[-1] if t.count("\n")>5 else t
    out.append(f"\n{'='*70}\n##### {bid} #####\n{'='*70}")
    out.append("\n--- ABSTRACT ---\n"+(grab(t,"Abstract",2200) or "(no abstract header; first 1500)\n"+body[:1500]))
    out.append("\n--- INTRODUCTION ---\n"+(grab(t,"Introduction",1800) or body[:1800]))
    m = grab(t,"Method",2600) or grab(t,"Approach",2600) or grab(t,"Proposed",2600) or grab(t,"Model",2600) or grab(t,"Architecture",2600)
    out.append("\n--- METHOD/APPROACH ---\n"+(m or "(no method header found)"))
    e = grab(t,"Experiment",2600) or grab(t,"Evaluation",2600) or grab(t,"Result",2600)
    out.append("\n--- EXPERIMENTS/RESULTS ---\n"+(e or "(no exp header found)"))
open("data/fulltext/_digest_1003.md","w",encoding="utf-8").write("\n".join(out))
print("digest written:", sum(len(x) for x in out), "chars")
