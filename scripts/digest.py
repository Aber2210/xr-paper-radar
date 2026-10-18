#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""从全文 txt 中抽取：摘要/引言 / 方法 / 实验关键数字 / 结论与局限。"""
import os, re, sys

SRC = "data/fulltext"
OUT = "data/digest"
os.makedirs(OUT, exist_ok=True)

HEAD = re.compile(
    r"^\s*(?:(?:[IVXLC]+|\d+(?:\.\d+)*|[A-Z])\.?\s+)?(Abstract|Introduction|Related Work|Method|Methods|"
    r"Approach|Proposed Method|Technical Approach|Overview|Preliminary|"
    r"Experiments?|Experimental (Setup|Results|Evaluation)|Results|Evaluation|"
    r"Ablation|Ablation Study|Discussion|Conclusion|Conclusions|Limitations?|"
    r"Future Work|Acknowledg)"
    r"(\s+(and|,)?\s*[A-Z][A-Za-z ]{0,40})?\s*$", re.I | re.M)


def clean(t):
    t = re.sub(r"[ \t]+", " ", t)
    t = re.sub(r"\n\s*\n\s*\n+", "\n\n", t)
    return t.strip()


def main(ids):
    for bid in ids:
        p = os.path.join(SRC, f"{bid}.txt")
        if not os.path.exists(p):
            print(f"!! missing {bid}")
            continue
        raw = open(p, encoding="utf-8").read()
        body = raw.split("\n\n", 3)[-1]
        text = clean(re.sub(r"\n{2,}", "\n", body))

        marks = [(m.start(), m.group(0).strip()) for m in HEAD.finditer(text)]
        # 去重：只保留位置递增且间隔 >400 的标题
        kept, last = [], -10**9
        for pos, name in marks:
            if pos - last > 400:
                kept.append((pos, name))
                last = pos
        if not kept:
            kept = [(0, "FULL")]

        chunks = []
        for i, (pos, name) in enumerate(kept):
            end = kept[i + 1][0] if i + 1 < len(kept) else len(text)
            seg = text[pos:end]
            if len(seg) > 6000:
                seg = seg[:3000] + "\n\n...[中略]...\n\n" + seg[-3000:]
            chunks.append(f"\n\n########## [{name}] ##########\n{seg}")

        out = f"# {bid}\n" + "".join(chunks)
        with open(os.path.join(OUT, f"{bid}.md"), "w", encoding="utf-8") as f:
            f.write(out)
        print(f"{bid}: {len(kept)} 段, {len(out)} 字符")


if __name__ == "__main__":
    main(sys.argv[1:])
