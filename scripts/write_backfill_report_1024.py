# -*- coding: utf-8 -*-
"""XR-Backfill-Report-1024：旧稿 replace 再公告补录报告（4 篇）。"""
import json, glob, os, ast, re

scored = json.load(open('data/scored_backfill_1024.json', encoding='utf-8'))
digest = {}
for g in (1, 2, 3):
    for x in json.load(open(f'data/digest_1024_g{g}.json', encoding='utf-8')):
        digest[x['id']] = x
src = open('scripts/write_notes_1024.py', encoding='utf-8').read()
EXTRA = ast.literal_eval(re.search(r'EXTRA = (\{.*?\n\})\n', src, re.S).group(1))

def notefile(pid):
    hits = glob.glob(f'papers/notes/{pid}__*.md')
    return os.path.basename(hits[0]) if hits else None

orig = {'2605.22190': '2026-05', '2609.16684': '2026-09', '2601.14895': '2026-01', '2508.15169': '2025-08'}
R = []
R.append('# XR Backfill 报告 · backfill-1024（旧稿 replace 再公告补录）')
R.append('')
R.append('> **诚实口径**：本批为 2026-10-23 公告批次中 RSS 混入的**旧稿 replace 再公告**（首次入馆），原始投稿月 2508 / 2601 / 2605 / 2609；公告日 2026-10-23、拉取日 2026-10-24。**非 10-24 当日新提交**。')
R.append('> 数据源：RSS 10-23 公告批次 33 命中中 8 篇旧稿（非 2610.* 前缀），经 XR 相关性甄别留 4 篇；4 篇全部 L0/FULL 全文后按正文证据定稿。')
R.append('')
R.append('## 补录总览')
R.append('')
R.append('- 入馆 **4 篇**（A×2 / B×2 / C×0），registry 597 → 618 的组成部分；门① 最大 Jaccard 0.109（与主批合并计算，<0.62 通过）；门③ 对 backfill 不适用。')
R.append('- 同批剔除的非 XR 旧稿 4 篇：2609.31777（心脏 MRI Rician 去噪）、2604.07993（HEX 人形全身操作）、2604.24033（事件相机 SLAM 基准·无人机高速机动）、2607.06768（AirPASS 6G 联邦学习）。')
R.append('- OUTDATED/SUPERSEDED：0 篇。')
R.append('')
R.append('## 补录清单（按加权降序）')
R.append('')
R.append('| # | 论文 | 赛道 | 分值 | 等级 | 证据 | 原始投稿 | 公告类型 | 笔记 |')
R.append('|---:|---|---|---:|---|---|---|---|---|')
for i, r in enumerate(scored, 1):
    R.append(f"| {i} | {r['title_zh']} | {r['track']} | {r['value']:.2f} | {r['grade']} | {r['evidence']} | {orig[r['id']]} | {r['announce_type']} | [→](../papers/notes/{notefile(r['id'])}) |")
R.append('')
R.append('## 逐篇要点')
R.append('')
for i, r in enumerate(scored, 1):
    pid = r['id']
    d = digest[pid]
    oneline, action, tags = EXTRA[pid]
    s = r['scores']
    R.append(f"### {i}. {d['title_zh']}（{pid}）— {r['value']:.2f} {r['grade']} · {r['track']}")
    R.append('')
    R.append(f"- **一句话结论**：{oneline}")
    R.append(f"- **7 维**：IMP {s['IMP']} · NOV {s['NOV']} · TEC {s['TEC']} · EXP {s['EXP']} · PER {s['PER']} · TRL {s['TRL']} · REP {s['REP']}（venue：{d['venue']}；证据：{r['evidence']} / {r['fetch_level']} / {r['fulltext_chars']:,} 字符）")
    R.append(f"- **关键实验**：{d['experiments'][:300]}")
    R.append(f"- **局限**：{'；'.join(d['limits'][:2])}")
    R.append(f"- **行动建议**：{action}")
    R.append('')
R.append('## 与文献库的关系')
R.append('')
R.append('- NoPo4D 补「前馈 + 免位姿 + 多视角 + 动态 + 一般场景」空白象限（与库内 NoPoSplat/FLARE/AnySplat 静态免位姿线、4DGT 需位姿线互补）；MEgoVista 与 10-23 批 EgoHand 构成第一视角手部重建「相机感知单目 vs stereo 度量标尺」双路线对照；SpatialMem 与库内 AR Office Recall（10-19）同属 memory-centric 空间记忆接口；MeSS 补城市场景生成的 mesh 先验路线。')
R.append('')
R.append('## 数据与过程')
R.append('')
R.append('- [backfill-1024 7 维对比表](../papers/daily/backfill-1024/7dim-table.md) · [执行日志](../papers/daily/backfill-1024/run_log.md) · [MOC-backfill-1024](../papers/MOC/MOC-backfill-1024.md)')
R.append('- 当日主批报告：[XR-Daily-Report-2026-10-24](./XR-Daily-Report-2026-10-24.md)')
R.append('')
open('reports/XR-Backfill-Report-1024.md', 'w', encoding='utf-8').write('\n'.join(R))
print('backfill report written:', len('\n'.join(R)), 'chars')
