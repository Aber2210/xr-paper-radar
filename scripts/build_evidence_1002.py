# -*- coding: utf-8 -*-
"""抽取 Top10 全文的 abstract + method + experiments，输出紧凑证据包，供写原子笔记。"""
import re, json, os

TOP = ["2609.34367","2609.34817","2609.32983","2609.32626","2609.34286",
       "2610.02207","2609.34527","2609.35743","2609.34346","2609.36596"]

# 标题（来自 scored 快照）
TITLE_ZH = {
 "2609.34367":"OIC-GS：面向沉浸式 VR 的全向高斯泼溅率失真自适应图元选择",
 "2609.34817":"ESTHER：野化自中心立体手估计",
 "2609.32983":"VocalEyes：基于对话内注册的说话人感知 AR 字幕系统",
 "2609.32626":"World SLAM Model：将 SLAM 范式直接引入下游导航的统一世界建模",
 "2609.34286":"Dexterous Tactile World Model：融合触觉与视觉的灵巧操作世界模型",
 "2610.02207":"GALA：基于线性混合形变的实时 3D 高斯化身动画蒸馏",
 "2609.34527":"RRG-SLAM：首个实时反射感知的高斯室内 SLAM",
 "2609.35743":"InfiniHand：自中心视频的流式世界坐标手势运动估计",
 "2609.34346":"E-WAVE：面向沉浸式 VR/AR 动态感知的事件化连续光流",
 "2609.36596":"HACo：面向力感知灵巧操作的触觉主动柔顺学习",
}
TRACK = {
 "2609.34367":"神经渲染","2609.34817":"化身与人体","2609.32983":"空间计算与UI",
 "2609.32626":"重建与SLAM","2609.34286":"触觉与多模态","2610.02207":"化身与人体",
 "2609.34527":"重建与SLAM","2609.35743":"化身与人体","2609.34346":"感知与认知",
 "2609.36596":"触觉与多模态",
}
PUB = {
 "2609.34367":"2026-09-28","2609.34817":"2026-09-28","2609.32983":"2026-09-26",
 "2609.32626":"2026-09-26","2609.34286":"2026-09-28","2610.02207":"2026-10-01",
 "2609.34527":"2026-09-28","2609.35743":"2026-09-28","2609.34346":"2026-09-28",
 "2609.36596":"2026-09-29",
}

# 章节头正则：罗马/阿拉伯章节号 + 名称
SEC = re.compile(r"(?im)^\s*(?:[IVXLC]+\.|\d+(?:\.\d+)*|[A-Z][A-Za-z ]{2,40})\.?\s+"
                 r"(Abstract|Introduction|Related Work|Method|Methods|Approach|Model|"
                 r"Architecture|Implementation|Experiment|Experiments|Results|Evaluation|"
                 r"Discussion|Conclusion|References|Background)\b")
def chunks(path):
    txt = open(path, encoding="utf-8", errors="ignore").read()
    parts = SEC.split(txt)
    out = {}
    for i in range(1, len(parts)-1, 2):
        out[parts[i].strip().lower()] = parts[i+1]
    return out

def clean(s, n=1600):
    s = re.sub(r"\s+"," ", s).strip()
    return s[:n]

def grab(ch, keys, n=1600):
    for k in keys:
        if k in ch and len(ch[k].strip())>40:
            return clean(ch[k], n)
    return ""

out_lines=[]
for bid in TOP:
    p=f"data/fulltext/{bid}.txt"
    if not os.path.exists(p):
        out_lines.append(f"\n## {bid} :: {TITLE_ZH[bid]}\n(fulltext missing)\n"); continue
    ch=chunks(p)
    abstract = grab(ch,["abstract"], 2600)
    method = grab(ch,["method","methods","approach","model","architecture"], 1700)
    exp = grab(ch,["experiments","experiment","evaluation","results"], 1700)
    out_lines.append(f"\n{'='*70}\n## {bid} :: {TITLE_ZH[bid]}\n赛道={TRACK[bid]} | 发布={PUB[bid]} | https://arxiv.org/abs/{bid}")
    out_lines.append(f"\n### ABSTRACT\n{abstract}")
    out_lines.append(f"\n### METHOD\n{method}")
    out_lines.append(f"\n### EXPERIMENTS\n{exp}")

open("data/raw/evidence_1002.md","w",encoding="utf-8").write("\n".join(out_lines))
print("evidence written:", len("\n".join(out_lines)), "chars")
