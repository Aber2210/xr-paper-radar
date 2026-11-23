# -*- coding: utf-8 -*-
"""2026-11-24 定稿：7dim-table + scored.md（含 50 篇逐篇 7 维评分理由）。"""
import json, os, sys
from collections import Counter
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from grade_caliber import assign_grade  # noqa: E402

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
os.chdir(ROOT)
DAY, MMDD = '2026-11-24', '1124'
ANN = '2026-11-23'

D = json.load(open(f'data/scored_{MMDD}.json', encoding='utf-8'))
G = json.load(open(f'data/gates_{MMDD}.json', encoding='utf-8'))
HEAVY = bool(G['gate3']['blockbuster'])
TOP10 = G['top10']

WHY = json.load(open('data/why_1124.json', encoding='utf-8'))


def table(rows, title):
    hdr = ("| # | arXiv | 论文 | 赛道 | IMP | NOV | TEC | EXP | PER | TRL | REP | 总分 | 档 | 公告 | 证据 |\n"
           "|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|\n")
    L = [hdr]
    for i, r in enumerate(rows, 1):
        s = r['scores']
        L.append("| %d | %s | %s | %s | %d | %d | %d | %d | %d | %d | %d | **%.2f** | %s | %s | %s |\n" % (
            i, r['id'], r['title_zh'][:40].replace('|', '/'), r['track'], s['IMP'], s['NOV'], s['TEC'],
            s['EXP'], s['PER'], s['TRL'], s['REP'], r['value'], r['grade'],
            r['announce'] or '-', r['evidence']))
    return title + ''.join(L)


for r in D:
    r['in_top10'] = r['id'] in TOP10
    r['grade'] = assign_grade(r['value'], r['batch'], HEAVY)
    r['scores_why'] = WHY[r['id']]
json.dump(D, open(f'data/scored_{MMDD}.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)

MAIN = [r for r in D if not r['batch'].startswith('backfill')]
BF = [r for r in D if r['batch'].startswith('backfill')]
MAIN.sort(key=lambda r: (-r['value'], -r['scores']['IMP'], -r['scores']['NOV'], r['id']))
BF.sort(key=lambda r: (-r['value'], -r['scores']['IMP'], -r['scores']['NOV'], r['id']))

head = ("# 7 维对比表 · %s（主批 %d 篇 + backfill %d 篇）\n\n"
        "权重 IMP0.20·NOV0.20·TEC0.15·EXP0.15·PER0.15·TRL0.08·REP0.07；"
        "档位 S≥4.20 且 blockbuster / A3.60–4.20 / B3.00–3.60 / C<3.00。\n"
        "公告日 %s（周一）≠ 拉取日 %s（周二 02:30）；11-21/11-22 为周末 skipDays 无公告段。\n\n" % (
            DAY, len(MAIN), len(BF), ANN, DAY))
os.makedirs(f'papers/daily/{DAY}', exist_ok=True)
open(f'papers/daily/{DAY}/7dim-table.md', 'w', encoding='utf-8').write(
    head + table(MAIN, f'## 主批（公告日 {ANN}）\n\n'))
os.makedirs(f'papers/daily/backfill-{MMDD}', exist_ok=True)
open(f'papers/daily/backfill-{MMDD}/7dim-table.md', 'w', encoding='utf-8').write(
    head + table(BF, f'## backfill-{MMDD}（旧稿 v2 再公告，首次入馆；非当日新提交）\n\n'))

# ---- scored.md ----
g = G['gate3']; g1 = G['gate1']; g2 = G['gate2']
sm = ["# 评分明细与覆盖校验 · %s\n\n" % DAY,
      "## 一、门禁三关\n\n",
      "- 门① 最大 Jaccard **%.3f**（%s vs %s）< 0.62 → PASS（只对比追加前库内集合，不含本批两批）\n" % (
          g1['max_jaccard'], g1['pair'][0], g1['pair'][1]),
      "- 门② 定稿 Top10 覆盖 **%d 赛道**（%s；全批 %d 赛道）→ PASS，未触发重筛\n" % (
          g2['n_tracks'], '、'.join(f"{k}{v}" for k, v in g2['top10_tracks'].items()), g2['all_batch_tracks']),
      "- 门③ 当日最高 **%.2f** vs 库内近 30 天 Top10 均分 **%.4f**（半开窗口 [%s, %s)、%d 条入窗、"
      "按 batch 剔除本次追加两批 %s）→ heavy_day_raw=%s、margin **%+.4f** → **blockbuster=%s，S 授予 %s**\n\n" % (
          g['today_max'], g['top10_mean'], g['window_lo'], g['window_hi'], g['in_window'],
          '、'.join(g['this_run_batches_excluded']), g['heavy_day_raw'], g['margin'],
          g['blockbuster'], g['s_awarded']),
      "## 二、分档统计\n\n",
      "- 主批 %d 篇：%s\n" % (len(MAIN), ' / '.join(f"{k} {v}" for k, v in sorted(Counter(r['grade'] for r in MAIN).items()))),
      "- backfill %d 篇：%s\n\n" % (len(BF), ' / '.join(f"{k} {v}" for k, v in sorted(Counter(r['grade'] for r in BF).items()))),
      "## 三、逐篇评分理由\n\n"]
for r in MAIN + BF:
    sm.append("### %s %s（%.2f / %s / %s）\n\n%s\n\n" % (
        r['id'], r['title_zh'], r['value'], r['grade'], r['batch'], r['scores_why']))
open(f'papers/daily/{DAY}/scored.md', 'w', encoding='utf-8').write(''.join(sm))

print('grades main', dict(Counter(r['grade'] for r in MAIN)), 'bf', dict(Counter(r['grade'] for r in BF)))
print('top10:', [(r['id'], r['value'], r['grade']) for r in MAIN if r['in_top10']])
print('7dim rows main', len(MAIN), 'bf', len(BF))
