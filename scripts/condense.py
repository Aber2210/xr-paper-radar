#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""压缩 digest：摘要 + 方法首段 + 含量化结果的句子 + 结论/局限。"""
import os, re, sys

D = "data/digest"
NUM = re.compile(r"(\d+\.?\d*\s*(%|×|x|dB|fps|ms|s\b|MB|GB|K\b|M\b|B\b)|"
                 r"(PSNR|SSIM|LPIPS|ATE|F-Score|mALDE|IoU|R@|recall|success|accuracy|"
                 r"speedup|faster|outperform|reduce[sd]?|improve[sd]?|gain))", re.I)
SENT = re.compile(r"(?<=[.!?])\s+")


def main(ids, budget=6500):
    for bid in ids:
        p = os.path.join(D, f"{bid}.md")
        t = open(p, encoding="utf-8").read()
        parts = re.split(r"\n########## \[(.+?)\] ##########\n", t)
        secs = [(parts[i], parts[i + 1]) for i in range(1, len(parts) - 1, 2)]

        print("\n" + "=" * 90)
        print(f"### {bid}")
        used = 0
        for name, body in secs:
            low = name.lower()
            keep = None
            if "abstract" in low:
                keep = body[:1800]
            elif any(k in low for k in ("introduction",)):
                keep = body[:1200]
            elif any(k in low for k in ("method", "approach", "overview", "preliminary")):
                keep = body[:2600]
            elif any(k in low for k in ("experiment", "result", "evaluation", "ablation")):
                sents = [s for s in SENT.split(body) if NUM.search(s) and 25 < len(s) < 420]
                keep = "  ".join(sents[:26])[:3400]
                if not keep:
                    keep = body[:2200]
            elif any(k in low for k in ("conclusion", "limitation", "discussion", "future")):
                keep = body[:1800]
            else:
                continue
            if not keep or not keep.strip():
                continue
            print(f"\n--- [{name}] ---\n{keep.strip()}")
            used += len(keep)
            if used > budget:
                print("\n...[后续章节已省略]...")
                break


if __name__ == "__main__":
    ids = sys.argv[1:]
    main(ids)
