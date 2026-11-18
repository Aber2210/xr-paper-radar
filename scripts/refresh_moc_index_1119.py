# -*- coding: utf-8 -*-
"""刷新 MOC-总索引.md：追加 2026-11-19 / backfill-1119 两批。"""
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from grade_caliber import assign_grade  # noqa: E402

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
os.chdir(ROOT)

P = 'papers/MOC/MOC-总索引.md'
t = open(P, encoding='utf-8').read()
orig_len = len(t)

G = json.load(open('data/gates_1119.json', encoding='utf-8'))
HEAVY = bool(G['gate3']['blockbuster'])
D = json.load(open('data/scored_1119.json', encoding='utf-8'))
MAIN = [p for p in D if p['batch'] == '2026-11-19']
BF = [p for p in D if p['batch'] == 'backfill-1119']
MAIN.sort(key=lambda r: (-r['value'], -r['scores']['IMP'], -r['scores']['NOV'], r['id']))
BF.sort(key=lambda r: -r['value'])
TOP = [next(p for p in MAIN if p['id'] == i) for i in G['top10']]
tmean = sum(p['value'] for p in TOP) / len(TOP)


def rep(old, new, tag):
    global t
    assert t.count(old) == 1, 'anchor %s count=%d' % (tag, t.count(old))
    t = t.replace(old, new, 1)


# ---------- 1. 头部统计与批次列表 ----------
rep('累计 **990 篇**；跨度 2026-09-15 ~ 2026-11-18',
    '累计 **1,015 篇**；跨度 2026-09-15 ~ 2026-11-19', 'head-count')

lines = t.split('\n')
assert lines[3].startswith('> 文献库：'), lines[3][:40]
lines[3] = lines[3] + (
    ' **11-19 周四处理 11-18 公告批次（21 篇 XR 新稿 12A/7B/2C，非重磅日无S；'
    'backfill-1119 补录 4 篇 3A/1B）**。')
t = '\n'.join(lines)

# ---------- 2. 速查入口 ----------
rep('| 最新一期 | [MOC · 2026-11-18](./MOC-2026-11-18.md) |',
    '| 最新一期 | [MOC · 2026-11-19](./MOC-2026-11-19.md) |', 'quick-latest')
rep('| 上一期 | [MOC · 2026-11-17](./MOC-2026-11-17.md) |',
    '| 上一期 | [MOC · 2026-11-18](./MOC-2026-11-18.md) |', 'quick-prev')
rep('（现有 632 篇）', '（现有 655 篇）', 'quick-notes')

old_status_start = '| 最新运行状态 | [运行报告 2026-11-18](../../reports/XR-Daily-Report-2026-11-18.md)'
i0 = t.find(old_status_start)
assert i0 > 0
i1 = t.find('\n', i0)
new_status = (
    '| 最新运行状态 | [运行报告 2026-11-19](../../reports/XR-Daily-Report-2026-11-19.md)'
    '（11-18 周三公告批次 XR 21 篇 12A/7B/2C **非重磅日无S**；公告日≠拉取日；listing 496 篇 100% 被 RSS 覆盖（缺收 0）；'
    'KW 命中 37 + 标题级补扫 21 → 剔 37 篇误命中 → XR 21 篇；11-17 组复采 811 篇未入馆、摘要级 69 篇命中与上批 rejected 逐篇一致 0 漏网；'
    '全文 25×L0/FULL（主批 21 + backfill 4）；Top10 覆盖 6 赛道（未重筛）；'
    '门③ 当日最高 4.30 vs 4.4230（436 条入窗、半开窗口、剔除本批）→ 非重磅日无 S）；'
    '上一期为 [11-18 运行报告](../../reports/XR-Daily-Report-2026-11-18.md) |'
)
t = t[:i0] + new_status + t[i1:]

# ---------- 3. 等级总表：追加状态注记 ----------
NOTE = (
    '> **状态注记（2026-11-19）**：周四 02:30，处理 **2026-11-18（周三）公告批次**（公告日≠拉取日，诚实口径）。'
    '**listing 对账**（`scripts/audit_listing_1119.py`，PREV_DAY=11-17 / NEW_DAYS=11-18,11-19）：7 分类最新公告日均为 **2026-11-18**，无 11-19 日组；'
    '11-17 组复采逐分类 **declared=got**（CV 342/GR 15/HC 58/MM 11/RO 134/AI 428/IV 28 = **1,016 槽位 / 844 唯一**；cs.CV 补采 skip=500 合并 49、cs.AI 合并 187），'
    '未入馆 **811 篇 = 844 − 33（上批主批已入馆）**；用 11-18 的 RSS 全量逐篇核摘要，811 篇中 XR 命中 **69 篇**，与上批 `rejected_1118.json` 的 69 篇**逐篇一致** → **0 漏网、无滞后补录**。'
    '**11-18 组 599 槽位 / 496 篇唯一论文**（CV 207/GR 10/HC 26/MM 3/RO 89/AI 259/IV 5，全部未入馆）。'
    '**数据源**：API 仅用于提交日核验（25 id 分 2 批、间隔 12 s，返回 25/25）；'
    'RSS 7 分类 `--no-filter` 去重 **766 条**（CV 322/RO 133/AI 401/HC 33/GR 16/IV 10/MM 9 槽位，去重 766）＝ **OK_CATS 7/7**，'
    '**listing 496 篇 100% 被 RSS 覆盖（缺收 0，coverage 1.0）**。'
    '**召回三层**：摘要级 KW 命中 **37 篇** + 标题级扩展词补扫 **21 篇** → 58 候选 → 逐篇核摘要剔除 **37 篇误命中**'
    '（缩写 AR/MR 自回归 2 / 自动驾驶与机器人 12 / 遥感医学水下 9 / 通用 2D 视觉与多模态 8 / 其他 6）→ **XR 池 21 篇**；'
    '标题级补扫**不计入「RSS 漏网」统计**。**提交日核验**（API published）：主批 **11-17×17 / 11-16×3 / 09-27×1**'
    '（2611.21642 RelicTouch 提交 2026-09-27、延迟约 7 周公告；RSS published 为公告时间戳 11-18，不可当提交日）。'
    '**全文**：25 篇串行 3 s/篇 → **25 篇全部 L0/FULL**（17,275–130,366 字符）；无 PARTIAL、无 L5、无 OCR。'
    '另：2611.23209（gaze-guided VLM）虽 L0 抓取成功但正文仅摘要页 + 参考文献，按诚实口径不纳入评分。'
    '**三关**：门① max Jaccard **0.261**（2611.22415 vs 2609.03892，其余 0.091–0.188）；'
    '门② 定稿 Top10 **6 赛道**（感知与认知 3 / 化身与人体 2 / 重建与SLAM 2 / 神经渲染 1 / 系统与平台 1 / 交互与输入 1；全批 8 赛道，纯值即达，**未重筛**）；'
    '门③ 当日最高 **4.30** vs 库内近 30 天 Top10 均分 **4.4230**（半开窗口 [2026-10-20, 2026-11-19)、**436 条入窗**、'
    '按 batch 剔除本次追加的 `2026-11-19` 与 `backfill-1119`、现算）→ **非重磅日无 S**（margin −0.1230）。'
    'OUTDATED / SUPERSEDED **0**。主批 **0 S / 12 A / 7 B / 2 C**（2 篇 C 仅入馆不解读）；'
    'backfill-1119 **3 A / 1 B / 0 C**（最高 SFMambaNet 3.85，按口径不评 S、不得并入当日重磅判定）。'
    'registry 990 → **1,015**（+21 +4，备份 `registry.jsonl.bak-20261119`）；笔记 632 → **655**；daily 67 → **69**；MOC 55 → **57**。'
    '详见 [运行报告](../../reports/XR-Daily-Report-2026-11-19.md) / [MOC-2026-11-19](./MOC-2026-11-19.md) / '
    '[MOC-backfill-1119](./MOC-backfill-1119.md) / [Backfill 报告](../../reports/XR-Backfill-Report-backfill-1119.md)。\n'
)
anchor = '\n\n---\n\n## 一、速查入口'
assert t.count(anchor) == 1, 'anchor sec1 count=%d' % t.count(anchor)
t = t.replace(anchor, '\n\n' + NOTE + '\n---\n\n## 一、速查入口', 1)

# ---------- 4. 批次索引表：追加两行 ----------
old_row = ('| backfill-1118 | [MOC-backfill-1118](./MOC-backfill-1118.md) | 补录 6（2A/3B/1C）· 非当日新提交 | '
           '11-17 公告 RSS 混入旧稿 v2/v3 再公告 6 篇（2511.16349 / 2605.05712 / 2605.09586 / 2607.03875 / 2609.31117 / 2611.18267，'
           '2026-11-14~16 更新；原始投稿 2025-11-20~2026-11-13）；最高 2607.03875 MACRO 3.93（按口径记 A，不参与当日重磅判定） |')
new_rows = old_row + '\n' + (
    '| 2026-11-19 | [MOC-2026-11-19](./MOC-2026-11-19.md) | XR 21（Top10 实数 10）· 0S/12A/7B/2C · '
    '**非重磅日（无S，门③ 4.30 < 4.4230）** | 11-18 周三公告批次真新提交 21 篇（11-17×17/11-16×3/09-27×1）；'
    'listing 496 篇 100% 被 RSS 覆盖（缺收 0）；KW 命中 37 + 标题级补扫 21 → 剔 37 篇误命中；11-17 组复采 0 漏网；'
    '全文 25×L0/FULL；门③ 现算 4.4230 vs 当日最高 4.30 |\n'
    '| backfill-1119 | [MOC-backfill-1119](./MOC-backfill-1119.md) | 补录 4（3A/1B）· 非当日新提交 | '
    '11-18 公告 RSS 混入旧稿 v2/v3 再公告 4 篇（2605.22631 / 2606.04493 / 2607.05598 / 2610.27275，'
    '2026-11-16~17 更新；原始投稿 2026-05-21~2026-10-19）；最高 2606.04493 SFMambaNet 3.85（按口径记 A，不参与当日重磅判定） |'
)
rep(old_row, new_rows, 'index-rows')

# ---------- 5. 文末 Top10 段：追加两节 ----------
def top_rows(items):
    out = []
    for i, p in enumerate(items, 1):
        g = assign_grade(p['value'], p['batch'], HEAVY)
        out.append('| %d | %s | %s | %.2f | %s | %s |'
                   % (i, p['title_zh'], p['track'], p['value'], g, p['evidence']))
    return '\n'.join(out)


hdr = '| # | 论文 | 赛道 | 分值 | 等级 | 证据 |\n|---:|---|---|---:|---|---|'
sec_main = (
    '\n### 2026-11-19 新增（Top10 实数 10 篇：全 A，非重磅日无 S）\n\n'
    '> 11-18（周三）公告批次，拉取 11-19 02:30，**公告日≠拉取日**。Top10 均分 **%.3f**。'
    '门③ 当日最高 4.30 vs 库内 4.4230（436 条入窗、半开窗口、剔除本批）→ **非重磅日，不授予 S**。\n\n%s\n%s\n'
    % (tmean, hdr, top_rows(TOP))
)
sec_bf = (
    '\n### backfill-1119 补录（4 篇：3 A / 1 B，非当日新提交）\n\n'
    '> 11-18 公告 RSS 混入的 replace 类旧稿（未入馆 270 篇 → 摘要级 XR 命中 17 篇 → 逐篇核摘要取 4 篇）。'
    '原始投稿 2026-05-21 / 2026-06-03 / 2026-07-06 / 2026-10-19。'
    '单独编号，不参与当日重磅日判定；≥4.20 亦按口径记 A。\n\n%s\n%s\n'
    % (hdr, top_rows(BF))
)
t = t.rstrip('\n') + '\n' + sec_main + sec_bf + '\n'

open(P, 'w', encoding='utf-8').write(t)
print('MOC index refreshed: %d -> %d chars' % (orig_len, len(t)))
