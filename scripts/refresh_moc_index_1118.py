# -*- coding: utf-8 -*-
"""刷新 MOC-总索引.md：追加 2026-11-18 / backfill-1118 两批。"""
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

G = json.load(open('data/gates_1118.json', encoding='utf-8'))
HEAVY = bool(G['gate3']['blockbuster'])
D = json.load(open('data/scored_1118.json', encoding='utf-8'))
MAIN = [p for p in D if p['batch'] == '2026-11-18']
BF = [p for p in D if p['batch'] == 'backfill-1118']
MAIN.sort(key=lambda r: (-r['value'], -r['scores']['IMP'], -r['scores']['NOV'], r['id']))
BF.sort(key=lambda r: -r['value'])
TOP = [next(p for p in MAIN if p['id'] == i) for i in G['top10']]
tmean = sum(p['value'] for p in TOP) / len(TOP)


def rep(old, new, tag):
    global t
    assert t.count(old) == 1, 'anchor %s count=%d' % (tag, t.count(old))
    t = t.replace(old, new, 1)


# ---------- 1. 头部统计与批次列表 ----------
rep('累计 **951 篇**；跨度 2026-09-15 ~ 2026-11-17',
    '累计 **990 篇**；跨度 2026-09-15 ~ 2026-11-18', 'head-count')

rep('· **backfill-1117:3（11-16 公告 RSS 混入旧稿 v2 再公告，首次入馆）**；',
    '· **backfill-1117:3（11-16 公告 RSS 混入旧稿 v2 再公告，首次入馆）** · '
    '**2026-11-18:33（11-17 周二公告批次真新提交，非重磅日无S——门③ 机械 heavy_day 但差值仅 0.027 属险过，按 skill §8.6.3 拒绝 S）** · '
    '**backfill-1118:6（11-17 公告 RSS 混入旧稿 v2/v3 再公告，首次入馆）**；',
    'head-batches')

# ---------- 2. 速查入口 ----------
rep('| 最新一期 | [MOC · 2026-11-17](./MOC-2026-11-17.md) |',
    '| 最新一期 | [MOC · 2026-11-18](./MOC-2026-11-18.md) |', 'quick-latest')
rep('| 上一期 | [MOC · 2026-11-14](./MOC-2026-11-14.md) |',
    '| 上一期 | [MOC · 2026-11-17](./MOC-2026-11-17.md) |', 'quick-prev')
rep('（现有 601 篇）', '（现有 632 篇）', 'quick-notes')

old_status_start = '| 最新运行状态 | [运行报告 2026-11-17](../../reports/XR-Daily-Report-2026-11-17.md)'
i0 = t.find(old_status_start)
assert i0 > 0
i1 = t.find('\n', i0)
old_status_full = t[i0:i1]
new_status = (
    '| 最新运行状态 | [运行报告 2026-11-18](../../reports/XR-Daily-Report-2026-11-18.md)'
    '（11-17 周二公告批次 XR 33 篇 19A/7B/7C **非重磅日无S**；公告日≠拉取日；listing 844 篇 100% 被 RSS 覆盖（缺收 0）；'
    'KW 56 条命中 66 + 标题级补扫 36 → 剔 69 篇误命中 → XR 33 篇；11-16 组复采 0 漏网；'
    '全文 35×L0/FULL + 4×L1/PARTIAL；Top10 覆盖 6 赛道（未重筛）；'
    '门③ 当日最高 4.43 vs 4.4030，差值 0.027 < 0.05 **险过不记 S**，4 篇 ≥4.20 记 A）；'
    '上一期为 [11-17 运行报告](../../reports/XR-Daily-Report-2026-11-17.md) |'
)
t = t[:i0] + new_status + t[i1:]

# ---------- 3. 等级总表：追加状态注记 ----------
NOTE = (
    '> **状态注记（2026-11-18）**：周三 02:30，处理 **2026-11-17（周二）公告批次**（公告日≠拉取日，诚实口径）。'
    '**listing 对账**（`scripts/audit_listing_1118.py`）：7 分类最新公告日均为 **2026-11-17**，无 11-18 日组；'
    '11-16 组复采逐分类 **declared=got**（CV 91/GR 5/HC 13/MM 0/RO 38/AI 164/IV 9 = 320 槽位 / **271 唯一**，cs.AI 补采 skip=500 合并 92），'
    '未入馆 **258 篇 = 271 − 13（上批已入馆）**，与 11-17 运行候选集逐篇一致 → **0 漏网、无滞后补录**。'
    '**11-17 组 1,016 槽位 / 844 篇唯一论文**（CV 342/GR 15/HC 58/MM 11/RO 134/AI 428/IV 28，全部未入馆）。'
    '**数据源**：API 仅用于提交日核验（39 id 分 3 批 ×13、间隔 12 s，返回 39/39）；'
    'RSS 7 分类 `--no-filter` 去重 **1,323 条**（AI 717/CV 511/RO 217/HC 79/IV 36/GR 19/MM 18）＝ **OK_CATS 7/7**，'
    '**listing 844 篇 100% 被 RSS 覆盖（缺收 0，coverage 1.0）**。'
    '**召回三层**：摘要级 KW **56 条**（本批据 11-17 run_log 缺口新增 26 词：`tactile`/`taxel`/`SDF`/`meshing`/`bundle adjustment`/`SPAD`/'
    '`monocular depth`/`6-DoF`/`hand-object`/`egocentric video`/`user study` 等）命中 **66 篇** + 标题级扩展词补扫 **36 篇** → 102 候选 → '
    '逐篇核摘要剔除 **69 篇误命中**（医学影像 6 / 机器人操作 8 / 自驾雷达 9 / 无人机农业 5 / 通用 LLM-HCI 6 / 通用位姿与分割 9 / 其他 26）→ '
    '**XR 池 33 篇**；标题级补扫**不计入「RSS 漏网」统计**。**提交日核验**（API published）：主批 '
    '**11-16×16 / 11-15×8 / 11-14×3 / 11-13×3 / 11-10×1 / 11-06×1 / 10-31×1**（2611.18679 提交 10-31、延迟约 17 天公告；'
    'RSS published 为公告时间戳 11-17，不可当提交日）。**全文**：39 篇串行 3 s/篇 → **35 篇 L0/FULL**（24,146–414,440 字符）+ '
    '**4 篇 L1/PARTIAL**（2611.18822 / 2611.20196 / 2611.20570 / 2611.21485：arXiv HTML v1 复核 404、ar5iv 仅返摘要页 4,567–5,535 字符'
    '且无任何正文节，沙箱无 pdfminer 故 L2 PDF 不可用，均显式标注「摘要级评估」）；L5 降级 0、OCR 未使用。'
    '**三关**：门① max Jaccard **0.318**（2611.21060 vs 2605.18553，其余 0.118–0.214）；'
    '门② 定稿 Top10 **6 赛道**（化身与人体 2 / 世界模型与仿真 2 / 重建与SLAM 2 / 神经渲染 2 / 内容生成 1 / 感知与认知 1；全批 10 赛道，纯值即达，**未重筛**）；'
    '门③ 当日最高 **4.43** vs 库内近 30 天 Top10 均分 **4.4030**（半开窗口 [2026-10-19, 2026-11-18)、**410 条入窗**、'
    '按 batch 剔除本次追加的 `2026-11-18` 与 `backfill-1118`、现算）→ 机械 `heavy_day=true`，但**差值仅 0.027 < 0.05**，'
    '按 skill §8.6.3「险过不得宣称重磅工作」**本期不记 S**；4 篇 ≥4.20（WinDEX 4.43 / LynnReal-Hand 4.37 / SemLite-GS 4.30 / MomentPnP 4.27）'
    '**记 A 并注明达线**。`data/gates_1118.json` 保留 `heavy_day_raw=true` / `margin=0.027` / `blockbuster=false` / `s_awarded=false` 供事后自证。'
    'OUTDATED / SUPERSEDED **0**。主批 **0 S / 19 A / 7 B / 7 C**（7 篇 C 仅入馆不解读）；'
    'backfill-1118 **2 A / 3 B / 1 C**（最高 MACRO 3.93，按口径不评 S、不得并入当日重磅判定）。'
    'registry 951 → **990**（+33 +6，备份 `registry.jsonl.bak-20261118`）；笔记 601 → **632**；daily 65 → **67**；MOC 53 → **55**。'
    '详见 [运行报告](../../reports/XR-Daily-Report-2026-11-18.md) / [MOC-2026-11-18](./MOC-2026-11-18.md) / '
    '[MOC-backfill-1118](./MOC-backfill-1118.md) / [Backfill 报告](../../reports/XR-Backfill-Report-backfill-1118.md)。\n'
)
anchor = '\n\n\n\n---\n\n## 一、速查入口'
assert t.count(anchor) == 1, 'anchor sec1 count=%d' % t.count(anchor)
t = t.replace(anchor, '\n' + NOTE + '\n\n---\n\n## 一、速查入口', 1)

# ---------- 4. 批次索引表：追加两行 ----------
old_row = ('| backfill-1117 | [MOC-backfill-1117](./MOC-backfill-1117.md) | 补录 3（3A）· 非当日新提交 | '
           '11-16 公告 RSS 混入旧稿 v2 再公告 3 篇（2501.12764 / 2608.19372 / 2611.17238，2026-11-13 更新）；'
           '最高 2611.17238 HEIR 4.07（按口径记 A） |')
new_rows = old_row + '\n' + (
    '| 2026-11-18 | [MOC-2026-11-18](./MOC-2026-11-18.md) | XR 33（Top10 实数 10）· 0S/19A/7B/7C · '
    '**非重磅日（无S，门③ 险过 +0.027）** | 11-17 周二公告批次真新提交 33 篇（11-16×16/11-15×8/11-14×3/11-13×3/11-10×1/11-06×1/10-31×1）；'
    'listing 844 篇 100% 被 RSS 覆盖（缺收 0）；KW 56 条命中 66 + 标题级补扫 36 → 剔 69 篇误命中；11-16 组复采 0 漏网；'
    '全文 35×L0/FULL + 4×L1/PARTIAL（摘要级评估）；门③ 现算 4.4030 vs 当日最高 4.43，差值 0.027 < 0.05 不记 S |\n'
    '| backfill-1118 | [MOC-backfill-1118](./MOC-backfill-1118.md) | 补录 6（2A/3B/1C）· 非当日新提交 | '
    '11-17 公告 RSS 混入旧稿 v2/v3 再公告 6 篇（2511.16349 / 2605.05712 / 2605.09586 / 2607.03875 / 2609.31117 / 2611.18267，'
    '2026-11-14~16 更新；原始投稿 2025-11-20~2026-11-13）；最高 2607.03875 MACRO 3.93（按口径记 A，不参与当日重磅判定） |'
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
    '\n### 2026-11-18 新增（Top10 实数 10 篇：全 A，非重磅日无 S——4 篇达 S 线按校准关记 A）\n\n'
    '> 11-17（周二）公告批次，拉取 11-18 02:30，**公告日≠拉取日**。Top10 均分 **%.3f**。'
    '门③ 当日最高 4.43 vs 库内 4.4030（410 条入窗、半开窗口、剔除本批），差值 0.027 < 0.05 → '
    '按 skill §8.6.3 **不宣称重磅日、不授予 S**。\n\n%s\n%s\n'
    % (tmean, hdr, top_rows(TOP))
)
sec_bf = (
    '\n### backfill-1118 补录（6 篇：2 A / 3 B / 1 C，非当日新提交）\n\n'
    '> 11-17 公告 RSS 混入的 replace 类旧稿（未入馆 479 篇 → 摘要级 XR 命中 32 篇 → 逐篇核摘要取 6 篇）。'
    '原始投稿 2025-11-20 / 2026-05-07 / 2026-05-10 / 2026-07-04 / 2026-09-25 / 2026-11-13。'
    '单独编号，不参与当日重磅日判定；≥4.20 亦按口径记 A。\n\n%s\n%s\n'
    % (hdr, top_rows(BF))
)
assert t.endswith('| FULL |\n'), 'tail=%r' % t[-24:]
t = t.rstrip('\n') + '\n' + sec_main + sec_bf + '\n'

open(P, 'w', encoding='utf-8').write(t)
print('MOC index refreshed: %d -> %d chars' % (orig_len, len(t)))
