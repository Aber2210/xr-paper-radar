#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""extract_sections_backfill.py — 从 7 篇 backfill 全文抽取结构化 digest 以控制上下文体积。
抽取 Abstract / Method / Experiments / Result / Conclusion / Limitation 各段前 N 字符。
"""
import re, os, json

SRC = "data/fulltext/backfill_2603_2609"
OUT = "data/digest_backfill"
IDS = ["2605.00556","2608.12759","2603.20714","2606.19156","2607.17790","2605.07943","2607.19479"]

HDR = re.compile(
    r"^\s*(?:(?:\d+(?:\.\d+)*|I{1,3}V?X?|IV|IX)\.?\s+)?"
    r"(Abstract|Introduction|Related Work|Method|Methods|Approach|Model|"
    r"Architecture|Implementation|Experiment|Experiments|Results|Evaluation|"
    r"Discussion|Conclusion|Limitations|Background)\b",
    re.I | re.M)

TRACK_MAP = {
    "2605.00556": "交互与输入",
    "2608.12759": "空间计算与UI",
    "2603.20714": "神经渲染",
    "2606.19156": "化身与人体",
    "2607.17790": "感知与认知",
    "2605.07943": "感知与认知",
    "2607.19479": "交互与输入",
}

def split_sections(text):
    matches = list(HDR.finditer(text))
    secs = {}
    for i, m in enumerate(matches):
        name = m.group(1).capitalize()
        start = m.end()
        end = matches[i+1].start() if i+1 < len(matches) else len(text)
        body = text[start:end].strip()
        body = re.sub(r"\n{2,}", "\n", body)
        secs.setdefault(name, body)
    return secs

def main():
    os.makedirs(OUT, exist_ok=True)
    for bid in IDS:
        p = os.path.join(SRC, f"{bid}.txt")
        if not os.path.exists(p):
            print(f"  !! 缺 {p}"); continue
        raw = open(p, encoding="utf-8").read()
        # 去掉文件头 (# LEVEL ... )
        body = re.sub(r"^# .*(\n|$)", "", raw)
        body = body.strip()
        secs = split_sections(body)
        lines = [f"# {bid}  [{TRACK_MAP.get(bid,'?')}]", ""]
        for key in ["Abstract","Introduction","Method","Methods","Approach","Model",
                    "Experiment","Experiments","Results","Evaluation","Conclusion","Limitations"]:
            if key in secs:
                b = secs[key]
                # 截断每节前 1400 字符
                if len(b) > 1400:
                    b = b[:1400] + " …[截断]"
                lines.append(f"## {key}\n{b}\n")
        digest = "\n".join(lines)
        op = os.path.join(OUT, f"{bid}.txt")
        open(op, "w", encoding="utf-8").write(digest)
        print(f"  {bid}: {len(digest)} 字符 digest → {op}")

if __name__ == "__main__":
    main()
