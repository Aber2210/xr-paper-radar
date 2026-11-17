# -*- coding: utf-8 -*-
"""2026-11-17 MOC-总索引刷新。"""
import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from grade_caliber import assign_grade  # noqa: E402  档位口径单一实现

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
os.chdir(ROOT)
D = json.load(open('data/scored_1117.json', encoding='utf-8'))
MAIN = [p for p in D if p['batch'] == '2026-11-17']
BF = [p for p in D if p['batch'] == 'backfill-1117']
MAIN.sort(key=lambda r: (-r['value'], -r['scores']['IMP'], -r['scores']['NOV'], r['id']))
G = json.load(open('data/gates_1117.json', encoding='utf-8'))
TOP10_ORDER = G['top10']
GATE3 = G['gate3']['top10_mean']
HEAVY = bool(G['gate3']['heavy_day'])
for _p in MAIN + BF:
    # 档位走单一实现（2026-11-17 复评 N-06 的第 5 处，b03 首轮漏改）：
    # MOC 表里的等级此前只按分数判，非重磅日会与笔记/registry/报告不一致。
    _p['grade'] = assign_grade(_p['value'], _p['batch'], HEAVY)


def esc(s):
    return str(s).replace('|', '/')


moc_path = 'papers/MOC/MOC-总索引.md'
h = open(moc_path, encoding='utf-8').read()
n0 = len(h)


def rep(old, new, tag):
    global h
    assert old in h, f'ANCHOR NOT FOUND: {tag}'
    h = h.replace(old, new, 1)


rep('累计 **935 篇**；跨度 2026-09-15 ~ 2026-11-14',
    '累计 **951 篇**；跨度 2026-09-15 ~ 2026-11-17', 'head-count')
rep('**backfill-1114:8（11-13 公告 RSS 混入旧稿 v2/v3 再公告，首次入馆）**；',
    '**backfill-1114:8（11-13 公告 RSS 混入旧稿 v2/v3 再公告，首次入馆）** · '
    '**2026-11-17:13（11-16 周一公告批次真新提交——周末 11-14/11-15 提交积压于周一 08:00 北京时间释放，非重磅日无S）** · '
    '**backfill-1117:3（11-16 公告 RSS 混入旧稿 v2 再公告，首次入馆）**；', 'batch-list')

note = ('> **状态注记（2026-11-17）**：周二 02:30，处理 **2026-11-16（周一）公告批次**（公告日≠拉取日，诚实口径）。'
        '**周末积压兑现**：11-14（周六）/11-15（周日）无公告日段（`skipDays` 节律），两日提交积压于**周一 00:00 UTC = 08:00 北京时间**释放，'
        '11-16（周一）02:30 的运行早于该时刻（状态日），本批为新一周首个真实批次。'
        '**listing 对账**（`scripts/audit_listing_1117.py`）：7 分类最新公告日均为 **2026-11-16**，无 11-14/11-15/11-17 日组；'
        '11-13 组复采逐分类 **declared=got**（CV 196/GR 6/HC 43/MM 2/RO 106/AI 321/IV 21 = 695 槽位 / **601 唯一**），'
        '未入馆 **581 篇与 11-16 运行集合 581/581 逐篇一致** → **0 漏网、无滞后补录**。'
        '**11-16 组 271 篇唯一论文**（320 槽位：CV 91/GR 5/HC 13/MM 0/RO 38/AI 164/IV 9，全部未入馆）。'
        '**数据源**：API 双主机 200（仅提交日核验，16 id 单批返回 16/16）；RSS 7 分类 `--no-filter` 去重 **435 条** = **189 new + 82 cross + 164 replace**；'
        '**listing 271 篇 100% 被 RSS 覆盖（缺收 0 篇）**，故摘要级过滤直接用 RSS 全摘要（覆盖率 **271/271 = 1.0000**），规避 429 静默丢批风险。'
        '**召回三层**：摘要级 KW 命中 **11 篇** + 标题级扩展词补扫 **22 篇** → 33 候选 → 逐篇核摘要剔除 **20 篇误命中**'
        '（医学 MRI 4（`\\bMR\\b`/`\\bAR\\b` 缩写误命中）/ 手写文本 3 / 转录组与高光谱 2 / V2X 与自动驾驶 2 / 机器人操作与导航 4 / 其他 5）→ **XR 池 13 篇**；'
        '该补扫层**不计入「RSS 漏网」统计**。**提交日核验**（API published）：主批 **11-13×12 / 11-12×1**（RSS published 为公告时间戳 11-16）。'
        '**全文**：13 篇 → **12 篇 L0/FULL**（24,146–128,049 字符）+ **1 篇 L1/PARTIAL**（2611.17903：arXiv HTML 404、ar5iv 仅摘要页 5,216 字符无正文节）。'
        '**三关**：门① max Jaccard **0.231**（2611.17619 vs 库内 2610.18950）；门② 定稿 Top10 **8 赛道**（全批 9，纯值即达，**未重筛**）；'
        f'门③ 当日最高 **3.93 < {GATE3:.4f}**（窗口 2026-10-18~11-17、**398 条入窗**、现算）→ **非重磅日，无 S**；OUTDATED 0。'
        '主批 **5 A / 6 B / 2 C**（2 篇 C 仅入馆不解读）；backfill-1117 **3 A**（最高 HEIR 4.07，高于主批最高，按口径不评 S）。'
        'registry 935 → **951**（+13 +3）；笔记 587 → **601**；daily 63 → **65**；MOC 51 → **53**。'
        '详见 [运行报告](../../reports/XR-Daily-Report-2026-11-17.md) / [MOC-2026-11-17](./MOC-2026-11-17.md) / '
        '[MOC-backfill-1117](./MOC-backfill-1117.md) / [Backfill 报告](../../reports/XR-Backfill-Report-1117.md)。\n')
anchor_end = '详见 [状态报告](../../reports/XR-Daily-Report-2026-11-16.md)。'
i = h.find(anchor_end)
assert i >= 0, 'ANCHOR NOT FOUND: note-end'
j = h.find('\n', i) + 1
h = h[:j] + note + h[j:]

rep('| 最新一期 | [MOC · 2026-11-14](./MOC-2026-11-14.md) |',
    '| 最新一期 | [MOC · 2026-11-17](./MOC-2026-11-17.md) |', 'quick-latest')
rep('| 上一期 | [MOC · 2026-11-12](./MOC-2026-11-12.md) |',
    '| 上一期 | [MOC · 2026-11-14](./MOC-2026-11-14.md) |', 'quick-prev')
rep('（现有 587 篇）', '（现有 601 篇）', 'quick-notes')

k = h.find('| 最新运行状态 |')
assert k >= 0, 'ANCHOR NOT FOUND: quick-status'
k_end = h.find('\n', k)
new_status = ('| 最新运行状态 | [运行报告 2026-11-17](../../reports/XR-Daily-Report-2026-11-17.md)'
              '（11-16 周一公告批次 13 篇 5A/6B/2C **非重磅日无S**；周末 11-14/11-15 提交积压于周一 08:00 北京时间释放；'
              'listing 271 篇摘要级 KW 11 + 标题级补扫 22 → 剔 20 篇误命中 → XR 13 篇；11-13 组复采 581 篇未入馆 diff 0 → 0 漏网；'
              '全文 12×L0/FULL + 1×L1/PARTIAL；Top10 实数 10 篇覆盖 8 赛道（未重筛）；门③ 现算 4.4030，当日最高 3.93 未达线 → 无 S）；'
              '上一期为 [11-16 状态报告](../../reports/XR-Daily-Report-2026-11-16.md) |')
h = h[:k] + new_status + h[k_end:]

row = ('| 2026-11-17 | [MOC-2026-11-17](./MOC-2026-11-17.md) | XR 13（Top10 实数 10）· 5A/6B/2C · **非重磅日（无S）** | '
       '11-16 周一公告批次真新提交 13 篇（11-13×12/11-12×1，周末积压周一释放）；listing 271 篇摘要级 KW 11 + 标题级补扫 22 → 剔 20 篇误命中；'
       '11-13 组复采 0 漏网；全文 12×L0/FULL + 1×L1/PARTIAL；门③ 现算 4.4030 |\n'
       '| backfill-1117 | [MOC-backfill-1117](./MOC-backfill-1117.md) | 补录 3（3A）· 非当日新提交 | '
       '11-16 公告 RSS 混入旧稿 v2 再公告 3 篇（2501.12764 / 2608.19372 / 2611.17238，2026-11-13 更新）；'
       '最高 2611.17238 HEIR 4.07（按口径记 A） |')
anchor_row = ('| backfill-1114 | [MOC-backfill-1114](./MOC-backfill-1114.md) | 补录 8（4A/4B）· 非当日新提交 | '
              '11-13 公告 RSS 混入旧稿 v2/v3 再公告 8 篇（2508/2510/2512/2603×2/2605/2607×2，2026-11-11~12 更新）；'
              '最高 2603.01178 riMESA 4.50（按口径记 A） |')
rep(anchor_row, anchor_row + '\n' + row, 'batch-table')

seg = ('\n### 2026-11-17 新增（Top10 实数 10 篇：5 A + 4 B + 1 B/PARTIAL，非重磅日无 S）\n\n'
       '| # | 论文 | 赛道 | 分值 | 等级 | 证据 |\n|---:|---|---|---:|---|---|\n')
for i2, pid in enumerate(TOP10_ORDER, 1):
    p = next(x for x in MAIN if x['id'] == pid)
    seg += f"| {i2} | {esc(p['title_zh'])} | {p['track']} | {p['value']:.2f} | {p['grade']} | {p['evidence']} |\n"
seg += ('\n### backfill-1117 补录（3 篇：3 A，非当日新提交）\n\n'
        '| # | 论文 | 赛道 | 分值 | 等级 | 证据 |\n|---:|---|---|---:|---|---|\n')
for i2, p in enumerate(BF, 1):
    seg += f"| {i2} | {esc(p['title_zh'])} | {p['track']} | {p['value']:.2f} | {p['grade']} | {p['evidence']} |\n"
h = h.rstrip() + '\n' + seg

foot_pat = re.compile(r'^\*最后更新：[^\n]*\* · 库内 \*\*935 篇\*\* · 原子笔记 \*\*587 篇\*\* · MOC 51 份$', re.M)
assert foot_pat.search(h), 'ANCHOR NOT FOUND: footer'
new_foot = ('*最后更新：2026-11-17（**11-16 周一公告批次——周末 11-14/11-15 提交积压于周一 08:00 北京时间释放**：'
            '13 篇 XR 新稿 5A/6B/2C **非重磅日无S**；listing 271 篇摘要级 KW 11 + 标题级补扫 22 → 剔 20 篇误命中 → XR 13；'
            'listing 271 篇 100% 被 RSS 覆盖；11-13 组复采 581 篇未入馆 diff 0 → 0 漏网；'
            '全文 12×L0/FULL + 1×L1/PARTIAL（2611.17903 ar5iv 摘要页）；门② 定稿 8 赛道未重筛；'
            '门③ 现算 4.4030，当日最高 3.93 未达线 → 无 S；backfill-1117 补录 3 篇 3A（最高 HEIR 4.07））。* '
            '· 库内 **951 篇** · 原子笔记 **601 篇** · MOC 53 份')
h = foot_pat.sub(new_foot, h)

open(moc_path, 'w', encoding='utf-8').write(h)
print('MOC-总索引 refreshed（%d -> %d chars）' % (n0, len(h)))
