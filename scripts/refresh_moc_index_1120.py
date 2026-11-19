# -*- coding: utf-8 -*-
"""刷新 MOC-总索引.md：追加 2026-11-20 / backfill-1120 两批（锚点式替换，逐处断言唯一）。"""
import glob, json, os, sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
os.chdir(ROOT)
P = 'papers/MOC/MOC-总索引.md'
t = open(P, encoding='utf-8').read()

G = json.load(open('data/gates_1120.json', encoding='utf-8'))
D = json.load(open('data/scored_1120.json', encoding='utf-8'))
MAIN = [p for p in D if not p['batch'].startswith('backfill')]
BF = [p for p in D if p['batch'].startswith('backfill')]
TOP = [p for p in D if p['in_top10']]
g3 = G['gate3']


def rep(old, new, tag, cnt=1):
    global t
    assert t.count(old) == cnt, '%s count=%d' % (tag, t.count(old))
    t = t.replace(old, new, cnt)


# 1. 头部计数
rep('累计 **1,015 篇**；跨度 2026-09-15 ~ 2026-11-19',
    '累计 **1,043 篇**；跨度 2026-09-15 ~ 2026-11-20', 'head')

# 2. 批次清单追加
old_tail = ' **11-19 周四处理 11-18 公告批次（21 篇 XR 新稿 12A/7B/2C，非重磅日无S；backfill-1119 补录 4 篇 3A/1B）**。'
rep(old_tail, old_tail + ' **11-20 周五处理 11-19 公告批次（25 篇 XR 新稿 18A/4B/3C，非重磅日无S；'
    'backfill-1120 补录 3 篇 2A/1B）**。', 'batch-list')

# 3. 状态注记（插在 11-19 注记之后）
anchor = '[Backfill 报告](../../reports/XR-Backfill-Report-backfill-1119.md)。'
NOTE = ('\n> **状态注记（2026-11-20）**：周五 02:30，处理 **2026-11-19（周四）公告批次**（公告日≠拉取日，诚实口径）。'
 '**listing 对账**（`scripts/audit_listing_1120.py`，PREV_DAY=11-18 / NEW_DAYS=11-19,11-20）：7 分类最新公告日均为 **2026-11-19**，'
 '11-20 组尚未释放；11-18 组复采逐分类 **declared=got**（CV 207/GR 10/HC 26/MM 3/RO 89/AI 259/IV 5 = **599 槽位 / 496 唯一**），'
 '未入馆 **475 篇 = 496 − 21（上批主批已入馆）**，用 11-19 的 RSS 全量核摘要 **475/475 覆盖**，摘要/标题级命中 **37 篇全部落在上批 `xr_pool_1119.json`**'
 '（21 入馆 + 37 剔除）→ **0 漏网**。**11-19 组 599 槽位 / 502 篇唯一**（CV 223/GR 3/HC 23/MM 6/RO 104/AI 230/IV 10）。'
 '**数据源**：API 双主机探针 200；RSS 7 分类 `--no-filter` 去重 **753 条**（OK_CATS 7/7），**listing 502 篇 100% 被 RSS 覆盖（缺收 0）** → 免 API `id_list`。'
 '**召回三层**：摘要级 KW 命中 **52 篇** + 标题级扩展词补扫 **16 篇** = 68 候选 → 逐篇核摘要剔 **43 篇误命中**'
 '（医学影像 9 / 机器人操作 11 / 自驾遥感 8 / 通用 LLM-NLP 9 / 科学成像 6）→ **22 篇**；'
 '**第 3.5 步残差复核**（`data/residual_1120.json`）扫描 434 条、判 12 条应收录（**2.8%**），**采纳 3 篇**'
 '（2611.23417 神经渲染 / 2611.23534 系统与平台 / 2611.24193 世界模型与仿真）→ **主批 25 篇**。'
 '**提交日核验**（API published）：**11-17×8 / 11-18×17**（RSS published 为公告时间戳 11-19，不可当提交日）。'
 '**全文**：28 篇串行 3 s/篇 → **27 篇 L0/FULL + 1 篇 L1/FULL（ar5iv 补）**；**2611.24193 为 PARTIAL**'
 '（arXiv HTML 仅前言/引言/图注，无 Method/Experiments，ar5iv 与 v1 复核同样缺正文，按摘要级评估并显式声明）。'
 '**三关**：门① max Jaccard **0.072**；门② 定稿 Top10 **7 赛道**（世界模型与仿真/化身与人体/感知与认知/神经渲染/系统与平台/触觉与多模态/重建与SLAM，全批 10 赛道，**未重筛**）；'
 '门③ 当日最高 **4.33** vs 库内近 30 天 Top10 均分 **4.4230**（半开窗口 [2026-10-21, 2026-11-20)、**457 条入窗**、'
 '按 batch 剔除本次追加的 `2026-11-20` 与 `backfill-1120`、现算）→ **非重磅日无 S**（margin −0.093）。OUTDATED / SUPERSEDED **0**。'
 '主批 **0 S / 18 A / 4 B / 3 C**；backfill-1120 **2 A / 1 B**（最高 EvoGS 4.05，按口径不评 S）。'
 'registry 1,015 → **1,043**（+25 +3，备份 `registry.jsonl.bak-20261120`）；笔记 655 → **680**；daily 69 → **70**。'
 '详见 [运行报告](../../reports/XR-Daily-Report-2026-11-20.md) / [MOC-2026-11-20](./MOC-2026-11-20.md) / '
 '[MOC-backfill-1120](./MOC-backfill-1120.md)。')
rep(anchor, anchor + NOTE, 'note')

# 4. 速查入口
rep('| 最新一期 | [MOC · 2026-11-19](./MOC-2026-11-19.md) |',
    '| 最新一期 | [MOC · 2026-11-20](./MOC-2026-11-20.md) |', 'latest')
rep('| 上一期 | [MOC · 2026-11-18](./MOC-2026-11-18.md) |',
    '| 上一期 | [MOC · 2026-11-19](./MOC-2026-11-19.md) |', 'prev')
rep('（现有 655 篇）', '（现有 680 篇）', 'notes')

i0 = t.find('| 最新运行状态 |')
assert i0 > 0
i1 = t.find('\n', i0)
new_status = ('| 最新运行状态 | [运行报告 2026-11-20](../../reports/XR-Daily-Report-2026-11-20.md)'
 '（11-19 周四公告批次 XR 25 篇 18A/4B/3C **非重磅日无S**；公告日≠拉取日；listing 502 篇 100% 被 RSS 覆盖（缺收 0）；'
 'KW 52 + 标题级补扫 16 → 剔 43 → 22 篇；残差复核 434 条判 12（2.8%）采纳 3 → 25 篇；'
 '11-18 组复采 475 篇未入馆、37 篇命中全在上批候选池 → 0 漏网；全文 28 篇（27 L0/FULL + 1 L1/FULL + 1 PARTIAL）；'
 'Top10 覆盖 7 赛道（未重筛）；门③ 当日最高 4.33 vs 4.4230（457 条入窗、半开窗口、剔除本批）→ 非重磅日无 S）；'
 '上一期为 [11-19 运行报告](../../reports/XR-Daily-Report-2026-11-19.md) |')
t = t[:i0] + new_status + t[i1:]

# 5. 批次索引表追加
row_anchor = '| 2026-11-19 |'
assert t.count(row_anchor) == 1, t.count(row_anchor)
i2 = t.find('\n', t.find(row_anchor))
rows = ('\n| 2026-11-20 | [MOC-2026-11-20](./MOC-2026-11-20.md) | XR 25 + backfill 3 · Top10 最高 4.33 · 非重磅日（无S） | '
        '11-19 公告批次；listing 502 唯一、RSS 缺收 0；残差采纳 3 |')
t = t[:i2] + rows + t[i2:]

# 6. 页脚
old_foot_pref = '*最后更新：'
i3 = t.find(old_foot_pref)
assert i3 > 0
i4 = t.find('\n', i3)
t = t[:i3] + ('*最后更新：2026-11-20（**11-19 周四公告批次**：25 篇 XR 新稿 18A/4B/3C **非重磅日无S**；'
 'listing 502 唯一 / 599 槽位；RSS 753 条覆盖 502/502（缺收 0）；KW 52 + 标题补扫 16 → 剔 43 → 22，残差采纳 3 → 25；'
 '11-18 组复采 475 篇未入馆 diff 0 → 0 漏网；全文 28 篇（1 篇 PARTIAL）；门② 7 赛道未重筛；门③ 4.33 < 4.4230 无 S；'
 'backfill-1120 补录 3 篇 2A/1B，最高 EvoGS 4.05）。* · 库内 **1,043 篇** · 原子笔记 **680 篇** · MOC **59 份**') + t[i4:]

open(P, 'w', encoding='utf-8').write(t)
print('MOC index refreshed, chars', len(t))
