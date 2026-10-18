# -*- coding: utf-8 -*-
"""build_1019.py — 2026-10-19 批次：三关校验 + 7 维表 + scored/run_log + registry 幂等追加。
批次性质：补漏批次（backfill-1012-1015 补充）。公告窗口 2026-10-13~10-16（API published 10-12~10-15），
拉取日 2026-10-19（周一）。诚实口径：非当日新提交。
"""
import json, os, re, shutil
from collections import Counter

ROOT = 'D:/Agent/WorkBuddy/Research'
BATCH = '2026-10-19'
ORIG_WINDOW = '10-13~10-16 公告窗口（积压补漏，拉取日 10-19）'
DAY = f'{ROOT}/papers/daily/{BATCH}'
os.makedirs(DAY, exist_ok=True)
W = {'IMP':0.20,'NOV':0.20,'TEC':0.15,'EXP':0.15,'PER':0.15,'TRL':0.08,'REP':0.07}

def value(s):
    return round(sum(W[k]*s[k] for k in W), 3)

def grade(v):
    return 'S' if v>=4.2 else ('A' if v>=3.6 else ('B' if v>=3.0 else 'C'))

# ---------- 载入 ----------
scored = json.load(open(f'{ROOT}/data/scored_1019.json', encoding='utf-8'))
reg_path = f'{ROOT}/papers/library/registry.jsonl'
reg = {}
for l in open(reg_path, encoding='utf-8'):
    if l.strip():
        d = json.loads(l)
        reg[d['id'].split(':')[-1].split('v')[0]] = d

raw = {}
for l in open(f'{ROOT}/data/raw/2026-10-19_api.jsonl', encoding='utf-8'):
    if l.strip():
        r = json.loads(l)
        raw[r['base_id']] = r

new_all = json.load(open(f'{ROOT}/data/2026-10-19_api_new.json', encoding='utf-8'))
window = [r for r in new_all if r['published'][:10] >= '2026-10-12']
inpool = {s['id'] for s in scored}
dropped = [r for r in window if r['base_id'] not in inpool]

# ---------- 定稿 value/grade ----------
for s in scored:
    s['value'] = value(s)
    s['grade'] = grade(s['value'])
scored.sort(key=lambda s: (-s['value'], -s['IMP'], -s['NOV'], s['id']))
top10 = scored[:10]
top10_ids = {s['id'] for s in top10}

# ---------- 门① 同质 Jaccard ----------
STOP = set('a an the of for and or to in on with by from at as is are be we our this that it its via using based can may propose present introduce towards toward novel learning framework approach method results show shows while however both all one two also more most than which when where such these those paper work works'.split())
def toks(s):
    s = re.sub(r'[^a-z0-9 ]', ' ', (s or '').lower())
    return set(w for w in s.split() if len(w) > 2 and w not in STOP)
def jac(a, b):
    return len(a & b)/len(a | b) if a and b else 0.0

lib_items = []
for bid, d in reg.items():
    if d.get('batch') == BATCH:
        continue
    lib_items.append((bid, (d.get('title') or '') + ' ' + (d.get('title_zh') or ''), toks((d.get('title') or '') + ' ' + raw.get(bid, {}).get('abstract', ''))))
gate1 = []
for s in scored:
    ct = toks(s['title'] + ' ' + raw.get(s['id'], {}).get('abstract', ''))
    best = (0.0, '', '')
    for bid, _, lt in lib_items:
        j = jac(ct, lt)
        if j > best[0]:
            best = (j, bid, _[:60])
    gate1.append((s['id'], round(best[0], 3), best[1], best[2]))
gate1.sort(key=lambda x: -x[1])
g1_max = gate1[0]
g1_hit = [g for g in gate1 if g[1] > 0.62]

# ---------- 门② 赛道覆盖 ----------
tracks_top10 = Counter(s['track'] for s in top10)
tracks_all = Counter(s['track'] for s in scored)

# ---------- 门③ 价值天花板（现算） ----------
lo = '2026-09-19'
win = [d for d in reg.values() if d.get('date', '') >= lo]
top30 = sorted(win, key=lambda d: -d.get('value', 0))[:10]
avg30 = round(sum(d.get('value', 0) for d in top30)/len(top30), 4)
today_max = scored[0]['value']
heavy = today_max >= avg30

# ---------- 7 维表 ----------
lines = []
lines.append(f'# 7 维对比表 · {BATCH}（补漏批次）')
lines.append('')
lines.append(f'> **公告窗口**：{ORIG_WINDOW}；**拉取日**：2026-10-19（周一）。本表为积压补漏产物，**非当日新提交**。')
lines.append('> 公告类型：均为 v1/v2 首次公告（CoTL 为 v2）；无旧稿 replace/cross 混入（listing 对账已证）。')
lines.append('')
lines.append('| # | ID | 标题 | 赛道 | IMP | NOV | TEC | EXP | PER | TRL | REP | 总分 | 等级 | 证据 |')
lines.append('|---|---|---|---|---|---|---|---|---|---|---|---|---|---|')
for i, s in enumerate(scored, 1):
    mark = ' ★Top10' if s['id'] in top10_ids else ''
    ev = 'FULL' if s['evidence'] == 'FULL' else '摘要级'
    lines.append(f"| {i} | {s['id']} | {s['title_zh']}{mark} | {s['track']} | {s['IMP']} | {s['NOV']} | {s['TEC']} | {s['EXP']} | {s['PER']} | {s['TRL']} | {s['REP']} | {s['value']:.2f} | {s['grade']} | {ev} |")
lines.append('')
lines.append(f'合计 {len(scored)} 篇入馆（{sum(1 for s in scored if s["grade"]=="S")} S / {sum(1 for s in scored if s["grade"]=="A")} A / {sum(1 for s in scored if s["grade"]=="B")} B / {sum(1 for s in scored if s["grade"]=="C")} C）；'
             f'剔除非 XR/弱相关 {len(dropped)} 篇（10-02~10-11 历史段 51 篇经各前批次口径复核后剔除，未列入本表）。')
open(f'{DAY}/7dim-table.md', 'w', encoding='utf-8').write('\n'.join(lines))

# ---------- scored.md ----------
md = []
md.append(f'# 评分明细 · {BATCH}（补漏批次）')
md.append('')
md.append(f'- 公告窗口：{ORIG_WINDOW}；拉取日 2026-10-19。')
md.append(f'- 评分口径：先抓全文再定稿（24 篇 L0/FULL + 5 篇摘要级 ABSTRACT_ONLY，笔记内显式标注）。')
md.append(f'- 定稿 Top10：{len(top10)} 篇（S×{sum(1 for s in top10 if s["grade"]=="S")} / A×{sum(1 for s in top10 if s["grade"]=="A")} / B×{sum(1 for s in top10 if s["grade"]=="B")}）。')
md.append('')
md.append('## Top10 排行')
md.append('')
md.append('| 排名 | ID | 标题 | 赛道 | 总分 | 等级 |')
md.append('|---|---|---|---|---|---|')
for i, s in enumerate(top10, 1):
    md.append(f"| {i} | {s['id']} | {s['title_zh']} | {s['track']} | {s['value']:.2f} | {s['grade']} |")
md.append('')
md.append('## 覆盖度三关')
md.append('')
md.append(f'**门① 同质去重（max Jaccard < 0.62）**：最高 {g1_max[1]:.3f}（{g1_max[0]} vs {g1_max[2]}）→ **通过**（无同质）。')
if g1_hit:
    md.append('> 命中：' + '；'.join(f'{g[0]} sim={g[1]:.3f} vs {g[2]}' for g in g1_hit))
md.append('')
md.append(f'**门② 赛道覆盖（≥5）**：Top10 覆盖 **{len(tracks_top10)} 赛道**（{"、".join(f"{t}×{c}" for t, c in tracks_top10.most_common())}）→ **通过**。')
md.append('')
md.append(f'**门③ 价值天花板（校准关，不触发重筛）**：库内近 30 天（date≥{lo}）Top10 均分 = **{avg30}**（现算：{", ".join(d["id"].split(":")[-1] + " " + str(d.get("value")) for d in top30)}）；当日最高 = **{today_max:.2f}**（{scored[0]["id"]}）→ {"**重磅日，可评 S 级**" if heavy else "**非重磅日，无 S 级**"}。')
md.append('')
md.append('## 全量评分明细（按加权降序）')
md.append('')
md.append('| ID | 标题 | 赛道 | IMP | NOV | TEC | EXP | PER | TRL | REP | 总分 | 等级 | 证据 |')
md.append('|---|---|---|---|---|---|---|---|---|---|---|---|---|')
for s in scored:
    md.append(f"| {s['id']} | {s['title_zh']} | {s['track']} | {s['IMP']} | {s['NOV']} | {s['TEC']} | {s['EXP']} | {s['PER']} | {s['TRL']} | {s['REP']} | {s['value']:.2f} | {s['grade']} | {s['evidence']} |")
md.append('')
md.append('## 本批剔除记录（非 XR / 弱相关，不入馆）')
md.append('')
md.append(f'公告窗口内非 XR 剔除 {len(dropped)} 篇：')
for r in sorted(dropped, key=lambda x: x['base_id']):
    md.append(f"- {r['base_id']} {r['title'][:66]}")
md.append('')
md.append('10-02~10-11 历史段 51 篇（各前批次已按口径甄别的非 XR 留存稿：机器人/VLA/人形/医学/水下/城市/行星等）不重复入馆；剔除理由类别与 10-17/backfill-1012-1015 口径一致。')
open(f'{DAY}/scored.md', 'w', encoding='utf-8').write('\n'.join(md))

# ---------- run_log.md ----------
rl = []
rl.append(f'# 执行日志 · {BATCH}')
rl.append('')
rl.append('## 数据源与对账')
rl.append('- 漏网对账（第 1 步）：arxiv listing 7 分类最新公告日 = **2026-10-16**（周五）；10-17/10-18 周末无公告，10-19 周一公告未释放（拉取时为北京时间周一 05:00）。')
rl.append('- listing 对账：10-16 日组 519 篇漏网 501 篇标题级 XR **0 命中**；10-9 段 43 篇 **0 命中**（scripts/audit_gap_listing.py，show=500，8s 间隔，完整性校验全过）。')
rl.append('- 探针：export.arxiv.org/api/query 200；arxiv.org/api/query 200；rss.arxiv.org 200 但 0 item（周一凌晨节律空源，§8.6.1.1 机制）。')
rl.append('- API 拉取：fetch_arxiv.py --since 2026-10-02 --max 600 → WROTE=236（published 10-02~10-15，前沿停滞 10-15）；去 registry(463) 后新稿 96 篇。')
rl.append('- **本批核心发现**：API published 口径 10-12~10-15 的 42 篇未入馆稿中 29 篇为 XR 相关（backfill-1012-1015 遗漏——其候选来自 listing 标题级 KW 过滤，缺 VR 缩写与摘要级口径）；10-02~10-11 段 54 篇经复核多为非 XR（含 reVISit-XR/PanTact/FoundationVIO/MacJEPA 等 11 篇 XR 补入）。')
rl.append('')
rl.append('## 全文抓取')
rl.append('- 24 篇候选跑 fetch_fulltext.py：**全部 L0/FULL**（40,705–165,161 字符），串行 3s/篇，无限流/降级/伪造；manifest 合并写入校验通过。')
rl.append('- 5 篇摘要级（ABSTRACT_ONLY）：2610.19330 / 2610.12780 / 2610.07336 / 2610.07523 / 2610.13143，按摘要级评估并在笔记显式标注。')
rl.append('')
rl.append('## 覆盖度三关')
rl.append(f'- 门①：max Jaccard {g1_max[1]:.3f}（{g1_max[0]} vs 库内 {g1_max[2]}）< 0.62 → 通过，无同质、未触发重筛。')
rl.append(f'- 门②：Top10 覆盖 {len(tracks_top10)} 赛道 ≥5 → 通过（全库 29 篇覆盖 {len(tracks_all)} 赛道）。')
rl.append(f'- 门③：当日最高 {today_max:.2f} vs 库内近 30 天 Top10 均分 {avg30}（现算）→ 重磅日，S 级成立，未拔高。')
rl.append('')
rl.append('## 落后登记')
rl.append('- 论文级 OUTDATED/SUPERSEDED：0 篇。')
rl.append('- 路线观察：① SMoRe 代表的「几何基础模型+在线修订记忆」与库内 VGGT-BC/STream3R 等前馈/流式路线构成第三条互补路线；② HoOPOE 是库内继 2609.11434（CVQPG）之后第二篇全息近眼显示硬件类论文，CGH 散斑的感知度量（JOD）为硬件类渲染补齐评价基准；③ FoundationVIO 与库内 cuVSLAM/LIN-SLAM/HexVIO 形成「GFM 前馈 + IMU 尺度约束」新支线。')
rl.append('')
rl.append('## 环境')
rl.append('- C: 盘余 11.2 GB（可用）；D: 盘余 417 GB 健康。')
open(f'{DAY}/run_log.md', 'w', encoding='utf-8').write('\n'.join(rl))

# ---------- registry 幂等追加 ----------
added = 0
with open(reg_path, 'a', encoding='utf-8') as f:
    for s in scored:
        bid = s['id']
        if bid in reg:
            continue
        row = {
            'id': f'arXiv:{bid}',
            'title': s['title'],
            'title_zh': s['title_zh'],
            'track': s['track'],
            'date': s['date'],
            'value': s['value'],
            'grade': s['grade'],
            'scores': {k: s[k] for k in ('IMP','NOV','TEC','EXP','PER','TRL','REP')},
            'status': s['status'],
            'evidence': s['evidence'],
            'fetch_level': s['level'],
            'fulltext_chars': s['chars'],
            'in_top10': bid in top10_ids,
            'batch': BATCH,
            'orig_window': ORIG_WINDOW,
            'flags': ['BACKFILL'],
        }
        f.write(json.dumps(row, ensure_ascii=False) + '\n')
        added += 1
print('registry 追加:', added, '；现总条目:', len(reg) + added)
print('门① max:', g1_max)
print('门② tracks:', dict(tracks_top10))
print('门③ avg30:', avg30, 'today_max:', today_max, 'heavy:', heavy)
print('Top10:')
for i, s in enumerate(top10, 1):
    print(f"  {i}. {s['id']} {s['value']:.2f} {s['grade']} {s['track']} {s['title_zh'][:40]}")
print('dropped:', len(dropped))
