#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Update papers/MOC/MOC-总索引.md for the 2026-10-08 batch (14th run)."""
import io

P = "D:/Agent/WorkBuddy/Research/papers/MOC/MOC-总索引.md"
s = open(P, encoding="utf-8").read()
orig = s

def rep(old, new, n=1):
    global s
    c = s.count(old)
    if c != n:
        print("!! EXPECTED", n, "GOT", c, "for:\n   ", old[:70])
    s = s.replace(old, new, n)

# A. registry count line
rep(
    "> 文献库：`papers/library/registry.jsonl`（累计 **337 篇**；跨度 2026-09-15 ~ 2026-10-05；批次 09-21:27 · 09-23:47 · 09-24:21 · 09-25:15 · 09-26:22 · 10-02:128 · 10-03:6 · 10-06:10 · 09-20 基线 38；10-04/10-05 因周末+周一节律与 API 索引滞后 **0 新稿**）。",
    "> 文献库：`papers/library/registry.jsonl`（累计 **347 篇**；跨度 2026-09-15 ~ 2026-10-07；批次 09-21:27 · 09-23:47 · 09-24:21 · 09-25:15 · 09-26:22 · 10-02:128 · 10-03:6 · 10-06:10 · 10-07:23 · 10-08:10 · 09-20 基线 38；10-04/10-05 因周末+周一节律与 API 索引滞后 **0 新稿**）。",
)

# B. append 10-08 status note after 10-07 note
note7 = "> **状态注记（2026-10-07）**：周三，API `submittedDate` 前沿仍停滞 10-02，RSS 公告日 10-06（补齐 10-03~10-06 工作日积压），真实新增由 RSS 兜底。本调度入选 **XR 新稿 23 篇（全 A/B，0 S）**，全文全 L0/FULL，三关通过、回补 2 篇化身与人体达 5 赛道、无重筛、无 OUTDATED。详见 [运行报告](../../reports/XR-Daily-Report-2026-10-07.md)。"
note8 = "> **状态注记（2026-10-08）**：周四，arXiv API（`arxiv.org/api/query`）已恢复 200，但 `export.arxiv.org` 仍 406（历史老问题），真实新增由 RSS 兜底（公告日 10-07）。本调度入选 **XR 新稿 15 篇（Top10：7 A / 3 B）**，全文 14 L0/FULL + 1 L1/PARTIAL（EVFormer 因 ar5iv 降级正文不完整，按 PARTIAL 证据、摘要级评估并显式标注）；三关通过、无重筛、无 OUTDATED。详见 [运行报告](../../reports/XR-Daily-Report-2026-10-08.md)。"
rep(note7, note7 + "\n" + note8)

# C. latest issue link
rep("| 最新一期 | [MOC · 2026-10-07](./MOC-2026-10-07.md) |",
    "| 最新一期 | [MOC · 2026-10-08](./MOC-2026-10-08.md) |")

# D. notes count
rep("（现有 102 篇）", "（现有 112 篇）")

# E. footer last-updated line
rep(
    "*最后更新：2026-10-07 · 库内 337 篇 · 原子笔记 102 篇 · MOC 12 份 · 落后/认知纠正登记（历史 15 条，10-06 新增路线观察 1 条：SCION 组合基元范式；10-07 无新增）*",
    "*最后更新：2026-10-08 · 库内 347 篇 · 原子笔记 112 篇 · MOC 13 份 · 落后/认知纠正登记（历史 15 条，10-06 新增路线观察 1 条：SCION 组合基元范式；10-07 无新增；10-08 新增路线观察 1 条：3DGS 语义理解走向训练后/在线解耦）*",
)

# F. batch index row
row6 = "| 2026-10-06 | [MOC-2026-10-06](./MOC-2026-10-06.md) | XR 10 · Top10 均分 3.95 · **含 S 级（重磅日）** | RSS 兜底（API 索引滞后 10-02） |"
row8 = "| 2026-10-08 | [MOC-2026-10-08](./MOC-2026-10-08.md) | XR 15（入选 10）· Top10 均分 3.61 · 非重磅日（无S） | RSS 兜底（API 索引滞后 10-02） |"
rep(row6, row6 + "\n" + row8)

# G. insert 10-08 Top10 subsection before "结构性缺口（持续）" note
subsec = """### 2026-10-08 新增（Top10，7 A / 3 B，非重磅日）

> 公告日 2026-10-07，RSS 兜底（export.arxiv.org 仍 406，arxiv.org/api/query 恢复 200，但 submittedDate 索引前沿停滞 10-02）。经 2610.* 前缀去重 registry、剔除 12 篇非 XR/弱相关后入选 XR 新稿 15 篇；Top10（7 A / 3 B）全文精读。全文 14 L0/FULL + 1 L1/PARTIAL（EVFormer 经 ar5iv 降级正文不完整，按 PARTIAL 证据、摘要级评估并显式标注）；覆盖率三关全过（max Jaccard 0.073、7 赛道、当日最高 4.15<库均 ~4.20~4.30），**未触发重筛、无 OUTDATED、无 S 级**。路线观察 1 条：3DGS 语义理解从“训练期联合”走向“训练后/在线解耦”（2610.08756 + 2610.07569）。

| 排名 | 论文 | 赛道 | 分值 | 等级 | 笔记 |
|---:|---|---|---:|---|---|
| 1 | DensiTok 让前馈式 3DGS 看见更多视角 | 神经渲染 | 4.15 | A | [→](../notes/2610.07958__DensiTok-3D.md) |
| 2 | Foveated Compression 中央凹式 VLM Token 压缩 | 渲染与显示 | 4.00 | A | [→](../notes/2610.07729__Token-VLM.md) |
| 3 | View Matters 关键帧引导 3DGS 编辑 | 内容生成 | 3.77 | A | [→](../notes/2610.08179__Matters-3D.md) |
| 4 | GSCV 标准视频编解码压缩 3DGS 序列 | 神经渲染 | 3.73 | A | [→](../notes/2610.07795__GSCV.md) |
| 5 | MRPilot MR 监督 LLM 多机器人团队 | 空间计算与UI | 3.68 | A | [→](../notes/2610.07477__MRPilot-LLM.md) |
| 6 | OpenSplatGraph 稠密语义地图到场景图 | 感知与认知 | 3.65 | A | [→](../notes/2610.07569__OpenSplatGraph.md) |
| 7 | Post-Training Semantic Lifting 3DGS 训练后语义提升 | 感知与认知 | 3.65 | A | [→](../notes/2610.08756__3D.md) |
| 8 | EgoLAP 第一视角人类→机器人 VLA 预训练 | 感知与认知 | 3.50 | B | [→](../notes/2610.08726__EgoLAP.md) |
| 9 | EVFormer 视觉-EMG 双手手姿（PARTIAL） | 交互与输入 | 3.40 | B | [→](../notes/2610.06970__EVFormer.md) |
| 10 | Hugging Suit 气动远程触觉服 | 触觉与多模态 | 3.20 | B | [→](../notes/2610.08305__Hugging-Suit.md) |

"""
anchor = "**结构性缺口（持续）**"
assert anchor in s, "anchor missing"
rep(anchor, subsec + "\n" + anchor)

if s == orig:
    print("NO CHANGES MADE!")
else:
    open(P, "w", encoding="utf-8").write(s)
    print("MOC-总索引 updated. new length:", len(s))
