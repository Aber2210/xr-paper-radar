# -*- coding: utf-8 -*-
"""2026-11-17 产物生成：主批（11-16 公告批次 13 篇）+ backfill-1117（3 篇旧稿 v2 再公告）。

诚实口径：
  公告日 2026-11-16（周一 00:00 UTC = 08:00 北京时间释放，覆盖周末 11-14/11-15 提交积压）
  ≠ 拉取日 2026-11-17（周二 02:30）。周末 11-14/11-15 无公告日段（skipDays 节律）。
  RSS published 是公告时间戳，提交日以 arXiv API published 为准（主批 11-13×12 / 11-12×1）。
消费 data/scored_1117.json；registry 幂等追加（先备份，in_top10 按定稿显式设置）。
"""
import glob
import json
import os
import re
import shutil

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
os.chdir(ROOT)
D = json.load(open('data/scored_1117.json', encoding='utf-8'))
MAIN = [p for p in D if p['batch'] == '2026-11-17']
BF = [p for p in D if p['batch'] == 'backfill-1117']
MAIN.sort(key=lambda r: (-r['value'], -r['scores']['IMP'], -r['scores']['NOV'], r['id']))
G = json.load(open('data/gates_1117.json', encoding='utf-8'))
TOP10_ORDER = G['top10']
DATE, ANN = '2026-11-17', '2026-11-16'
GATE3 = G['gate3']['top10_mean']
G1 = G['gate1']['max_jaccard']
MANIFEST = json.load(open('data/fulltext/_manifest.json', encoding='utf-8'))
for p in MAIN + BF:
    p['level'] = MANIFEST[p['id']]['level']
    p['evidence'] = MANIFEST[p['id']]['evidence']
    p['announce'] = 'replace' if p['batch'].startswith('backfill') else 'new'
    p['status'] = 'CURRENT'
    v = p['value']
    p['grade'] = 'S' if v >= 4.2 else ('A' if v >= 3.6 else ('B' if v >= 3.0 else 'C'))
    if p['batch'].startswith('backfill') and p['grade'] == 'S':
        p['grade'] = 'A'   # 口径：backfill 不参与重磅日判定，≥4.2 一律记 A
TOP10 = [next(p for p in MAIN if p['id'] == pid) for pid in TOP10_ORDER]
assert [p['id'] for p in TOP10] == TOP10_ORDER
assert len(MAIN) == 13 and len(BF) == 3, (len(MAIN), len(BF))
for p in TOP10:
    p['in_top10'] = True
for p in MAIN:
    p.setdefault('in_top10', False)

gr_main = {g: sum(1 for p in MAIN if p['grade'] == g) for g in 'SABC'}
gr_bf = {g: sum(1 for p in BF if p['grade'] == g) for g in 'SABC'}
print('main grades', gr_main, 'bf grades', gr_bf)


def esc(s):
    return str(s).replace('|', '/')


def dim_row(p):
    s = p['scores']
    star = '⭐' if p.get('in_top10') else ''
    return (f"| {p['id']} | {esc(p['title_zh'])} {star} | {p['track']} | "
            f"{s['IMP']} | {s['NOV']} | {s['TEC']} | {s['EXP']} | {s['PER']} | {s['TRL']} | {s['REP']} | "
            f"{p['value']:.2f} | {p['grade']} | {p['evidence']} | {p['announce']} |")


TBL_HEAD = ('| arXiv | 标题 | 赛道 | IMP | NOV | TEC | EXP | PER | TRL | REP | 总分 | 等级 | 证据 | 公告类型 |\n'
            '|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|\n')
os.makedirs(f'papers/daily/{DATE}', exist_ok=True)
os.makedirs('papers/daily/backfill-1117', exist_ok=True)


def seven_table(papers, path, title, intro):
    lines = [f'# {title}\n', intro + '\n', TBL_HEAD]
    for p in papers:
        lines.append(dim_row(p) + '\n')
    open(path, 'w', encoding='utf-8').writelines(lines)


INTRO_MAIN = (
    '批次：2026-11-17（**2026-11-16（周一）公告批次**——公告日 11-16 ≠ 拉取日 11-17（周二 02:30），诚实口径）。'
    '周末 11-14（周六）/ 11-15（周日）无公告日段（`skipDays` 节律），两日提交积压于**周一 00:00 UTC = 08:00 北京时间**统一释放，'
    '构成 listing 的 11-16 日组；主批 API published 核验提交日 **11-13×12 / 11-12×1**（RSS published 是公告时间戳，不可当提交日）。\n'
    '漏网对账（先于拉取，`scripts/audit_listing_1117.py`，show=500 单页×7 分类 + 目标组 declared≠got 自动补页，'
    'PREV_DAY=11-13 / NEW_DAYS=11-14,11-15,11-16,11-17）：7 分类最新公告日均为 **2026-11-16**，**无 11-14/11-15/11-17 日组**；'
    '11-13 组复采逐分类 **declared=got**（CV 196 / GR 6 / HC 43 / MM 2 / RO 106 / AI 321 / IV 21 = 695 槽位 / **601 唯一**），'
    '未入馆 **581 篇与 11-16 运行集合 581/581 逐篇一致** → **0 漏网、无滞后补录**。\n'
    '**11-16 组 271 篇唯一论文**（320 槽位：CV 91 / GR 5 / HC 13 / MM 0 / RO 38 / AI 164 / IV 9，全部未入馆）'
    '→ 摘要级 XR 过滤（`scripts/triage_1117.py`；listing 271 ⊂ RSS 全量 435，覆盖率 **271/271 = 1.0000**，'
    '故直接使用 RSS 全摘要而不走 API id_list，规避 11-12 的 429 静默丢批风险）KW 命中 **11 篇**；'
    '另经标题级扩展词补扫补入 KW 未命中 **22 篇**，候选 33 篇 → 人工逐篇核摘要剔除 **20 篇误命中** → **XR 池 13 篇**。\n'
    '数据源：API 双主机 200（id_list 仅用于提交日核验）；RSS 7 分类 `--no-filter` 去重 **435 条** = '
    '**189 new + 82 cross + 164 replace**；listing 271 篇 100% 被 RSS 覆盖（**RSS 缺收 0 篇**）。\n'
    '全文：13 篇候选串行 3s/篇 → **12 篇 L0/FULL**（24,146–128,049 字符）+ **1 篇 L1/PARTIAL**'
    '（2611.17903：arXiv HTML 404、ar5iv 仅返摘要页 5,216 字符且无正文节，沙箱无 PDF 解析库 → 摘要级评估，已在笔记与报告中显式声明）。\n'
    '覆盖度三关：门① 最大 Jaccard **0.231**（2611.17619 vs 库内 2610.18950，<0.62）；'
    '门② 定稿 Top10 覆盖 **8 赛道**（全批 9 赛道，纯值排序即达，**未触发重筛**）；'
    '门③ 当日最高 **3.93 < 库内近 30 天 Top10 均分 4.4030**（窗口 2026-10-18~11-17、398 条入窗、现算）'
    '→ **非重磅日，无 S 级**。OUTDATED 0。'
)
seven_table(MAIN, f'papers/daily/{DATE}/7dim-table.md', f'{DATE} 全量 7 维度对比表（参考）', INTRO_MAIN)

INTRO_BF = (
    '批次：backfill-1117（**11-16 公告批次 RSS 混入的旧稿 v2 再公告**，首次入馆）。\n'
    '均非 11-16 当日新提交，诚实口径单独编号；不参与当日「重磅日」判定，≥4.2 亦按口径记 A。\n'
    '候选来源：RSS 全量 435 条中 **replace 类 164 篇**未入馆者，经摘要级 XR 过滤命中 **4 篇**，'
    '剔除 1 篇（2610.30969 IORA：低自由度耦合手抓取与支撑面几何，非 XR）→ **本批 3 篇**：\n'
    '2608.19372 The Missing Touch（v2，2026-08-19 首发，11-13 更新）/ '
    '2501.12764 Grid-based Submap Joining（v2，2025-01-22 首发）/ '
    '2611.17238 HEIR（v2，2026-11-12 首发，11-13 更新）。\n'
    '全文：3 篇全部 **L0/FULL**（46,770 / 112,020 / 184,205 字符）。'
    '本批最高 **4.07（HEIR）**，与主批最高 3.93 相比反超——backfill 与本批同期出现「触觉/遥操作 + 人机意图」两条强线。'
)
seven_table(BF, 'papers/daily/backfill-1117/7dim-table.md',
            'backfill-1117 全量 7 维度对比表（参考）', INTRO_BF)


# ---------- scored.md ----------
def scored_md(papers, path, title, extra):
    L = [f'# {title}\n', extra + '\n',
         '| 排名 | arXiv | 标题 | 赛道 | IMP | NOV | TEC | EXP | PER | TRL | REP | 总分 | 等级 | 证据 |',
         '|---|---|---|---|---|---|---|---|---|---|---|---|---|---|']
    for i, p in enumerate(papers, 1):
        s = p['scores']
        L.append(f"| {i} | {p['id']} | {esc(p['title_zh'])} | {p['track']} | {s['IMP']} | {s['NOV']} | "
                 f"{s['TEC']} | {s['EXP']} | {s['PER']} | {s['TRL']} | {s['REP']} | {p['value']:.2f} | "
                 f"{p['grade']} | {p['evidence']} |")
    L.append('\n## 评分理由（逐篇）\n')
    for p in papers:
        L.append(f"### {p['id']} · {esc(p['title_zh'])}（{p['value']:.2f} {p['grade']}）\n")
        L.append(p['scores_why'] + '\n')
    open(path, 'w', encoding='utf-8').writelines([x + '\n' for x in L])


scored_md(MAIN, f'papers/daily/{DATE}/scored.md', f'{DATE} 评分明细',
          '评分口径：7 维加权 IMP0.20·NOV0.20·TEC0.15·EXP0.15·PER0.15·TRL0.08·REP0.07；'
          '分档 S≥4.2 / A3.6–4.2 / B3.0–3.6 / C<3.0。13 篇全部先抓全文再定稿（12 L0/FULL + 1 L1/PARTIAL）。\n'
          f'覆盖度三关：门① 最大 Jaccard **{G1:.3f}** < 0.62；门② 定稿 Top10 覆盖 **8 赛道**（全批 9，未重筛）；'
          f'门③ 当日最高 **3.93 < 4.4030**（窗口 2026-10-18~11-17、398 条入窗、现算）→ **非重磅日，无 S 级**。\n'
          '等级分布：5 A / 6 B / 2 C（无 S）；2 篇 C 级（2611.17752 2.93 / 2611.18438 2.08）仅入馆不解读。')
scored_md(BF, 'papers/daily/backfill-1117/scored.md', 'backfill-1117 评分明细',
          '评分口径同上；本批为旧稿 v2 再公告首次入馆，均非当日新提交。'
          '等级分布：3 A（无 S；≥4.2 亦按口径记 A）；门③ 对 backfill 不适用。')
print('7dim/scored written')
