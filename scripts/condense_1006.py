#!/usr/bin/env python3
"""Condense full-text .txt into a scoring brief: abstract + method + experiments/results."""
import re, json, os, glob

IDS = ["2610.02322","2610.02697","2610.02715","2610.03162","2610.03192",
       "2610.03232","2610.03283","2610.03441","2610.03599","2610.03607"]
FT = "data/fulltext"

def sections(text):
    """Return list of (header, body) for numbered/roman sections."""
    lines = text.splitlines()
    out = []
    cur_h, cur_b = None, []
    # section header: line like '1 Introduction' or 'IV Method' or '3.2 Foo'
    hdr = re.compile(r'^\s*([0-9]+(?:\.[0-9]+)*|[IVXLC]+)\.?\s+[A-Z][A-Za-z].*')
    for ln in lines:
        if hdr.match(ln) and len(ln) < 80:
            if cur_h is not None:
                out.append((cur_h, "\n".join(cur_b)))
            cur_h = ln.strip()
            cur_b = []
        else:
            if cur_h is not None:
                cur_b.append(ln)
    if cur_h is not None:
        out.append((cur_h, "\n".join(cur_b)))
    return out

def grab(text, keywords, maxchars=3200):
    secs = sections(text)
    picked = []
    for h, b in secs:
        hl = h.lower()
        if any(k in hl for k in keywords):
            b2 = re.sub(r'\s+', ' ', b).strip()
            picked.append((h, b2[:maxchars]))
    return picked

def abstract(text):
    m = re.search(r'Abstract\s*(.*?)(?=\n\d+\.?\s+[A-Z])', text, re.S)
    if m:
        return re.sub(r'\s+',' ', m.group(1)).strip()[:1800]
    return ""

os.makedirs("data/briefs", exist_ok=True)
summary = {}
for bid in IDS:
    p = os.path.join(FT, f"{bid}.txt")
    if not os.path.exists(p):
        summary[bid] = "MISSING"
        continue
    txt = open(p, encoding="utf-8", errors="ignore").read()
    abs = abstract(txt)
    method = grab(txt, ["method","approach","model","framework","architecture","formulation"], 2600)
    exp = grab(txt, ["experiment","evaluation","result","benchmark","dataset","ablation","user study"], 3200)
    brief = f"# {bid}\n\n## Abstract\n{abs}\n\n## Method/Approach\n"
    for h,b in method[:3]:
        brief += f"\n### {h}\n{b}\n"
    brief += "\n## Experiments/Results\n"
    for h,b in exp[:3]:
        brief += f"\n### {h}\n{b}\n"
    open(f"data/briefs/{bid}.brief.md","w",encoding="utf-8").write(brief)
    summary[bid] = f"abs={len(abs)} method_secs={len(method)} exp_secs={len(exp)} chars={len(txt)}"
    print(bid, summary[bid])

json.dump(summary, open("data/briefs/_summary.json","w"), indent=2)
print("DONE")
