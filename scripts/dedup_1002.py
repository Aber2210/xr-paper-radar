# -*- coding: utf-8 -*-
"""2026-10-02 批次：去重 + XR 相关度初筛 + 摘要快照导出。
输入：data/raw/2026-10-02.jsonl（gap 09-26~10-02 全量）
输出：data/raw/2026-10-02_new.jsonl（库内没有的新条目，全量含非XR）
      并打印 XR 相关度统计与逐篇摘要，供人工 7 维打分。
"""
import json, os, re

RAW = "data/raw/2026-10-02.jsonl"
REG = "papers/library/registry.jsonl"
OUT = "data/raw/2026-10-02_new.jsonl"

# 文献库已有 base_id
have = set()
for l in open(REG, encoding="utf-8"):
    l = l.strip()
    if not l: continue
    bid = json.loads(l)["id"].split(":")[-1].split("v")[0]
    have.add(bid)

raw = [json.loads(l) for l in open(RAW, encoding="utf-8") if l.strip()]
print("原始拉取:", len(raw))

# 去重：剔除库内已有（含 v2 再公告）
new = [r for r in raw if r["base_id"] not in have]
print("去重后新条目:", len(new))

# 旧稿 replace/cross 过滤（非 2610/2609 等近期前缀 → 若 < 2609 视为旧稿混入，单独列出 backfill）
KW = ["virtual reality","augmented reality","mixed reality","extended reality","head-mounted",
      "wearable display","3d gaussian","gaussian splatting","nerf","slam","spatial computing",
      "haptic","telepresence","avatar","egocentric","scene reconstruction","near-eye","light field",
      "waveguide","holographic display","varifocal","maxwellian","retinal projection","pancake optics",
      "foveated","accommodation-vergence","headset","oculus","hololens","quest","hmd","3dgs",
      "neural rendering","point cloud","volumetric","teleoperation","embodied","world model",
      "mixed reality","depth estimation","pose estimation","hand tracking","eye tracking"]

def is_xr(r):
    blob = (r["title"] + " " + r["abstract"]).lower()
    return any(k in blob for k in KW)

xr = [r for r in new if is_xr(r)]
non_xr = [r for r in new if not is_xr(r)]

# 按 published 日期统计命中区间
from collections import Counter
date_counts = Counter(r["published"][:10] for r in new)
print("命中日期分布:", dict(sorted(date_counts.items())))

# 写 new 全量（含非XR留存）
with open(OUT, "w", encoding="utf-8") as f:
    for r in new:
        f.write(json.dumps(r, ensure_ascii=False) + "\n")
print("写:", OUT, "共", len(new))

print(f"\n=== XR 相关 {len(xr)} 篇 / 非XR {len(non_xr)} 篇 ===")
# 按日期+价值线索打印供打分
xr_sorted = sorted(xr, key=lambda r: r["published"][:10], reverse=True)
for r in xr_sorted:
    a = re.sub(r"\s+", " ", r["abstract"])[:240]
    print(f"\n[{r['base_id']}] {r['published'][:10]} | {r['title']}")
    print(f"   {a}")
