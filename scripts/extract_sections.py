# -*- coding: utf-8 -*-
"""从已抓取的全文中抽取 Method / Experiment / Results 段落，供打分与写笔记精读。"""
import re, sys
SEC = re.compile(r"(?im)^\s*(?:[IVXLC]+\.|\d+(?:\.\d+)*|[A-Z][A-Za-z ]{2,40})\.?\s+"
                 r"(Abstract|Introduction|Related Work|Method|Methods|Approach|Model|"
                 r"Architecture|Implementation|Experiment|Experiments|Results|Evaluation|"
                 r"Discussion|Conclusion|References|Background)\b")
def chunks(path):
    txt = open(path, encoding="utf-8", errors="ignore").read()
    parts = SEC.split(txt)
    # parts: [pre, name1, body1, name2, body2, ...]
    out = {}
    for i in range(1, len(parts)-1, 2):
        out[parts[i].strip().lower()] = parts[i+1]
    return out
ids = sys.argv[1:]
for bid in ids:
    p = f"data/fulltext/{bid}.txt"
    try:
        ch = chunks(p)
    except Exception as e:
        print(f"[{bid}] ERR {e}"); continue
    print(f"\n========== {bid} ==========")
    for key in ["method","methods","approach","model","architecture","experiment","experiments","results","evaluation"]:
        if key in ch:
            body = re.sub(r"\s+"," ", ch[key]).strip()
            print(f"\n--- {key.upper()} (前1800字) ---\n{body[:1800]}")
