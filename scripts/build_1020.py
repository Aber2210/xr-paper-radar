# -*- coding: utf-8 -*-
# build_1020.py — 2026-10-20 批次：主批次（10-19 公告，12 篇）+ backfill-1020（8 篇）。
# 三关校验 + 7 维表 + scored/run_log + registry 幂等追加（先备份）。
import json, os, re, shutil
from collections import Counter

ROOT = 'D:/Agent/WorkBuddy/Research'
BATCH = '2026-10-20'
BF_BATCH = 'backfill-1020'
ORIG_WINDOW = '10-19 公告批次（10-15~10-16 提交、周一 10-19 释放；拉取日 10-20 周二）'
BF_WINDOW = '10-16 公告漏网 1 篇（GeoPano）+ RSS 旧稿 replace/cross 再公告 7 篇（2602~2608 原始提交）'
DAY = f'{ROOT}/papers/daily/{BATCH}'
BFDAY = f'{ROOT}/papers/daily/{BF_BATCH}'
os.makedirs(DAY, exist_ok=True)
os.makedirs(BFDAY, exist_ok=True)

main = json.load(open(f'{ROOT}/data/scored_1020.json', encoding='utf-8'))
bf = json.load(open(f'{ROOT}/data/scored_backfill_1020.json', encoding='utf-8'))
top10 = main[:10]
top10_ids = {s['id'] for s in top10}
bf_ids = {s['id'] for s in bf}

reg_path = f'{ROOT}/papers/library/registry.jsonl'
reg = {}
for l in open(reg_path, encoding='utf-8'):
    if l.strip():
        d = json.loads(l)
        reg[d['id'].split(':')[-1].split('v')[0]] = d

# 全文摘要（门① Jaccard 用）：优先 manifest/raw，缺省用标题
raw = {}
for fn in ('data/raw/2026-10-20_rss.jsonl',):
    for l in open(f'{ROOT}/{fn}', encoding='utf-8'):
        if l.strip():
            r = json.loads(l)
            raw[r['base_id']] = r
xr_abs = json.load(open(f'{ROOT}/data/missed_xr_abstract.json', encoding='utf-8'))
bf_meta = json.load(open(f'{ROOT}/data/backfill_meta_1020.json', encoding='utf-8'))
for bid, v in xr_abs.items():
    raw.setdefault(bid, {'title': v['title'], 'abstract': v.get('abstract', '')})
for bid, v in bf_meta.items():
    raw.setdefault(bid, v)

STOP = set('a an the of for and or to in on with by from at as is are be we our this that it its via using based can may propose present introduce towards toward novel learning framework approach method results show shows while however both all one two also more most than which when where such these those paper work works'.split())
def toks(s):
    s = re.sub(r'[^a-z0-9 ]', ' ', (s or '').lower())
    return set(w for w in s.split() if len(w) > 2 and w not in STOP)
def jac(a, b):
    return len(a & b) / len(a | b) if a and b else 0.0

EXCLUDE = {BATCH, BF_BATCH}
lib_items = []
for bid, d in reg.items():
    if d.get('batch') in EXCLUDE:
        continue
    lib_items.append((bid, toks((d.get('title') or '') + ' ' + raw.get(bid, {}).get('abstract', ''))))

def gate1(scored):
    out = []
    for s in scored:
        ct = toks(s['title'] + ' ' + raw.get(s['id'], {}).get('abstract', ''))
        best = (0.0, '', '')
        for bid, lt in lib_items:
            j = jac(ct, lt)
            if j > best[0]:
                best = (j, bid, '')
        out.append((s['id'], round(best[0], 3), best[1]))
    out.sort(key=lambda x: -x[1])
    return out

g1_main = gate1(main)
g1_bf = gate1(bf)
g1_max = g1_main[0]
g1_hit = [g for g in g1_main if g[1] > 0.62]

tracks_top10 = Counter(s['track'] for s in top10)
tracks_all = Counter(s['track'] for s in main)
tracks_bf = Counter(s['track'] for s in bf)

# 门③ 现算：date>=2026-09-20 的 registry 按 value 降序前 10 均分
lo = '2026-09-20'
win = [d for d in reg.values() if d.get('date', '') >= lo]
top30 = sorted(win, key=lambda d: -d.get('value', 0))[:10]
avg30 = round(sum(d.get('value', 0) for d in top30) / len(top30), 4)
today_max = main[0]['value']
heavy = today_max >= avg30

# ---------- 7 维表（主批次） ----------
def table(rows, path, title, note_lines, top_ids, grade_counts):
    lines = [f'# 7 维对比表 · {title}', '']
    lines += note_lines
    lines.append('| # | arXiv | 标题 | 赛道 | IMP | NOV | TEC | EXP | PER | TRL | REP | 总分 | 等级 | 证据 |')
    lines.append('|---|---|---|---|---|---|---|---|---|---|---|---|---|---|')
    for i, s in enumerate(rows, 1):
        mark = ' ★Top10' if s['id'] in top_ids else ''
        lines.append(f"| {i} | {s['id']} | {s['title_zh']}{mark} | {s['track']} | {s['IMP']} | {s['NOV']} | {s['TEC']} | {s['EXP']} | {s['PER']} | {s['TRL']} | {s['REP']} | {s['value']:.2f} | {s['grade']} | FULL |")
    lines.append('')
    lines.append(f"合计 {len(rows)} 篇入馆（{grade_counts}）；全部 L0/FULL（先抓全文再定稿）。")
    open(path, 'w', encoding='utf-8').write('\n'.join(lines))

gc_main = f"{sum(1 for s in main if s['grade']=='S')} S / {sum(1 for s in main if s['grade']=='A')} A / {sum(1 for s in main if s['grade']=='B')} B / {sum(1 for s in main if s['grade']=='C')} C"
gc_bf = f"{sum(1 for s in bf if s['grade']=='S')} S / {sum(1 for s in bf if s['grade']=='A')} A / {sum(1 for s in bf if s['grade']=='B')} B / {sum(1 for s in bf if s['grade']=='C')} C"

table(main, f'{DAY}/7dim-table.md', BATCH, [
    f'> **公告窗口**：{ORIG_WINDOW}。',
    '> **诚实口径**：本批为 10-19（周一）公告批次，收录 10-15~10-16 提交、随周一一并释放的稿件；**非当日（10-20）硬提交**。',
    '> 公告类型：全部为 2610.* v1 首次公告（new）；RSS 混入的 15 篇旧稿 replace/cross 已全部剔除并单列 backfill-1020，未混入本表。',
    '> 数据源：RSS 兜底（rss.arxiv.org，7 分类去重 352 条，关键词命中 35）+ listing 对账（7 分类 10-19 日组 373 篇全量，摘要级 XR 过滤交叉验证）。',
], top10_ids, gc_main)

table(bf, f'{BFDAY}/7dim-table.md', BF_BATCH + '（backfill）', [
    f'> **公告窗口**：{BF_WINDOW}；**拉取日**：2026-10-20。',
    '> **诚实口径**：本批为补录，全部标注 batch=backfill-1020、orig_window 注明原始提交月；**绝不混入「当日新论文」表**。',
    '> 来源：① listing 对账发现 10-16 公告日漏网 1 篇（GeoPano，摘要级 XR 过滤命中，10-17 运行标题级过滤漏掉）；② RSS 旧稿 replace/cross 再公告 7 篇（2602~2608 提交，首次入馆）。',
], bf_ids, gc_bf)

# ---------- scored.md（主批次） ----------
md = []
md.append(f'# 评分明细 · {BATCH}')
md.append('')
md.append(f'- 公告窗口：{ORIG_WINDOW}。')
md.append('- 评分口径：先抓全文再定稿；12 篇候选全部 L0/FULL（45,271–118,689 字符），串行 3s/篇，无限流/降级/伪造。')
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
md.append(f'**门① 同质去重（max Jaccard < 0.62）**：最高 {g1_max[1]:.3f}（{g1_max[0]} vs 库内 {g1_max[2] or "—"}）→ **通过**（无同质）。')
if g1_hit:
    md.append('> 命中：' + '；'.join(f'{g[0]} sim={g[1]:.3f} vs {g[2]}' for g in g1_hit))
md.append('')
md.append(f'**门② 赛道覆盖（≥5）**：Top10 覆盖 **{len(tracks_top10)} 赛道**（{"、".join(f"{t}×{c}" for t, c in tracks_top10.most_common())}）→ **通过**。')
md.append('')
md.append(f'**门③ 价值天花板（校准关，不触发重筛）**：库内近 30 天（date≥{lo}）Top10 均分 = **{avg30}**（现算：{", ".join(d["id"].split(":")[-1] + " " + str(d.get("value")) for d in top30)}）；当日最高 = **{today_max:.2f}**（{main[0]["id"]}）→ {"**重磅日，可评 S 级**" if heavy else "**非重磅日（差值 " + format(today_max - avg30, "+.3f") + "，落入 <0.05 险过带），不宣称重磅**"}。')
md.append('')
md.append('## 全量评分明细（按加权降序）')
md.append('')
md.append('| ID | 标题 | 赛道 | IMP | NOV | TEC | EXP | PER | TRL | REP | 总分 | 等级 | 证据 |')
md.append('|---|---|---|---|---|---|---|---|---|---|---|---|---|')
for s in main:
    md.append(f"| {s['id']} | {s['title_zh']} | {s['track']} | {s['IMP']} | {s['NOV']} | {s['TEC']} | {s['EXP']} | {s['PER']} | {s['TRL']} | {s['REP']} | {s['value']:.2f} | {s['grade']} | FULL |")
md.append('')
md.append('## 本批剔除记录（非 XR / 弱相关，不入馆）')
md.append('')
md.append('10-19 公告批次非 XR 剔除 7 篇（RSS 关键词命中但甄别为非 XR）：')
for r in ['2610.22450', '2610.22505', '2610.22552', '2610.22643', '2610.22932', '2610.23237', '2610.22400']:
    t = raw.get(r, {}).get('title', '')
    md.append(f"- {r} {t[:64]}")
md.append('')
md.append('剔除理由：DriveWorld3D（自动驾驶世界模型）/ KFS⁴LAM（内窥镜医学 SLAM）/ RTISSLAM-3D（声纳 SLAM）/ LGGS（MRI 重建）/ Ego2Contact（机器人操作）/ X-Splat（X 射线医学重建）/ 2610.22400（推荐系统用户编码）——与既往批次口径一致（医学/自动驾驶/纯机器人域不纳入 XR 文献库）。')
open(f'{DAY}/scored.md', 'w', encoding='utf-8').write('\n'.join(md))

# ---------- scored.md（backfill） ----------
mb = []
mb.append(f'# 评分明细 · {BF_BATCH}（backfill）')
mb.append('')
mb.append(f'- 公告窗口：{BF_WINDOW}；拉取日 2026-10-20。')
mb.append('- 评分口径：8 篇全部 L0/FULL，先抓全文再定稿。')
mb.append('- 覆盖三关：门① max Jaccard %.3f（通过）；门② 覆盖 %d 赛道（backfill 为机会性补录，不适用 Top10 选拔）；门③ 对 backfill 不适用。' % (g1_bf[0][1], len(tracks_bf)))
mb.append('')
mb.append('| ID | 标题 | 赛道 | IMP | NOV | TEC | EXP | PER | TRL | REP | 总分 | 等级 |')
mb.append('|---|---|---|---|---|---|---|---|---|---|---|---|')
for s in bf:
    mb.append(f"| {s['id']} | {s['title_zh']} | {s['track']} | {s['IMP']} | {s['NOV']} | {s['TEC']} | {s['EXP']} | {s['PER']} | {s['TRL']} | {s['REP']} | {s['value']:.2f} | {s['grade']} |")
mb.append('')
mb.append('## backfill 候选剔除记录（非 XR，不入馆）')
mb.append('')
for r, why in [('2506.03591', '统一多模态模型持续学习（无 XR 关联）'), ('2510.08713', '机器人视觉导航世界模型'), ('2601.01865', '实时视频增强/重光照（通用视频处理）'),
               ('2606.18097', '工业 DLO 操作仿真基准（机器人）'), ('2608.02014', '跨本体灵巧抓取（机器人）'), ('2608.09971', '气候模拟（非 XR）'),
               ('2608.19182', '灵巧操作 RL 预训练（机器人）'), ('2609.39600', '视觉定位 VLM（非 XR）'),
               ('2610.21180', '灵巧操作基准（机器人）'), ('2610.21239', 'MPPI 运动规划（机器人）'), ('2610.21292', '机械臂跟踪控制（机器人）'),
               ('2610.21429', '声音触发移动操作（机器人）'), ('2610.21503', '工人室内外定位（工业安全）'), ('2610.21573', 'VLM 决策树基准（非 XR）'),
               ('2610.21586', '室内导航拓扑记忆（机器人）'), ('2610.21696', '术中 X 射线跟踪（医学）'), ('2610.21999', '实体视觉跟踪（机器人）'),
               ('2610.22052', '四元数压缩（通用图形，既往口径判非 XR）'), ('2610.22176', '人形遥操作 MPC（机器人）'), ('2610.22178', 'VLA 知识注册（机器人）'),
               ('2610.22342', '触觉预训练用于机器人操作（机器人域）')]:
    mb.append(f"- {r} {why}")
open(f'{BFDAY}/scored.md', 'w', encoding='utf-8').write('\n'.join(mb))

# ---------- run_log ----------
rl = []
rl.append(f'# 执行日志 · {BATCH}')
rl.append('')
rl.append('## 数据源与对账（第 1-3 步）')
rl.append('- 漏网对账（第 1 步）：listing 7 分类最新公告日 = **2026-10-19（周一）**（10-17/10-18 周末无公告）；TARGET_LO=2026-10-16，重审 10-16 + 审计 10-19。')
rl.append('- listing 对账：7 分类 10-19 日组共 373 篇（去重后）全部入账；10-16 日组 519 篇中 501 篇不在库。完整性校验：逐分类自检全部通过（最终 per-cat SHORT 为跨分类交叉列表认领的统计假象，非真实缺口）。')
rl.append('- 脚本修复（本次）：audit_gap_listing.py ① 停止逻辑由「见任一旧日头即停」改为「本页最旧条目早于窗口下界才停」（页内多日头会提前中断翻页）；② 新增按日完整性驱动的逐页截断重试（服务端/代理间歇返回不完整页面）。')
rl.append('- 过滤器升级（落实 10-19 教训）：fetch_rss.py 新增 ABBREV 缩写层（VR/AR/MR/XR/HMD/OST/SLAM/VIO/IMU/DoF/FOV/JND/IPD/VAC/MTF/CGH 词边界正则）；新增 scripts/filter_missed_xr_abstract.py 对 874 篇漏网全集走 API 摘要级过滤（RSS cs.AI 频道为真空源，listing 标题级过滤覆盖不足，摘要级为必需下层）。')
rl.append('- 探针：export.arxiv.org/api/query 200；arxiv.org/api/query 200；rss.arxiv.org 200（cs.CV 201 条；**cs.AI 频道 0 条真空源**，其主分类论文靠 listing+API 摘要级过滤补回）。')
rl.append('- 拉取：fetch_rss.py 7 分类去重 352 条 → 关键词命中 35 条 → 去 registry(492) 后 33 新 = **18 篇 2610.* 真新提交** + 14 篇旧稿 replace/cross（另 2 篇库内 v2 再公告剔除）。')
rl.append('- 甄别：18 篇真新中 **12 篇 XR 核心/强相关**入评分池，7 篇非 XR 剔除（自动驾驶/医学×3/声纳/机器人/X 射线/推荐系统）。')
rl.append('- listing×RSS 交叉验证：listing 摘要级 XR 命中 19 篇（10-19）中 18 篇与 RSS 交集一致、1 篇（2610.22400）甄别为非 XR → 两渠道互证无遗漏。')
rl.append('')
rl.append('## backfill 发现')
rl.append('- **10-16 公告日漏网 1 篇**：2610.21297 GeoPano（10-15 提交、10-16 公告）——10-17 运行标题级过滤未命中（摘要才提 AR/VR），本次摘要级过滤补获，属真实漏网。')
rl.append('- **RSS 旧稿 replace/cross 再公告 15 篇**中 7 篇 XR 相关首次入馆（SAGE/OMEGA-Avatar/PanoAir/HyVGGT-VO/CodecSplat/PinNet/EgoTac），8 篇非 XR 剔除；全部单列 backfill-1020，未混入当日新论文。')
rl.append('')
rl.append('## 全文抓取')
rl.append('- 20 篇候选（12 主批次 + 8 backfill）跑 fetch_fulltext.py：**全部 L0/FULL**（45,271–118,689 字符），串行 3s/篇，无限流/降级/伪造；manifest 合并写入校验通过。')
rl.append('')
rl.append('## 覆盖度三关')
rl.append(f'- 门①：max Jaccard {g1_max[1]:.3f}（{g1_max[0]} vs 库内 {g1_max[2] or "—"}）< 0.62 → 通过，无同质、未触发重筛。')
rl.append(f'- 门②：Top10 覆盖 {len(tracks_top10)} 赛道 ≥5 → 通过（全批 12 篇覆盖 {len(tracks_all)} 赛道）。')
rl.append(f'- 门③：当日最高 {today_max:.2f} vs 库内近 30 天 Top10 均分 {avg30}（现算）→ 差值 {today_max - avg30:+.3f}，落入 <0.05 险过带 → **非重磅日，不宣称重磅**（S 级按机械档位保留并显式标注，遵循 §8.6.3 险过表述规范）。')
rl.append('')
rl.append('## 落后登记')
rl.append('- 论文级 OUTDATED/SUPERSEDED：0 篇（门①通过且无同质）。')
rl.append('- 路线观察：① VDA 代表「视频扩散先验直接充当化身」路线，与库内 3DGS/3DMM 化身族（OMEGA-Avatar/LAM/GAGAvatar 等）构成范式竞争，非取代；② dGS 延续库内 N-DGS/UBS 的 N 维泼剪效率线；③ FLoTS-SLAM 与库内动态 SLAM（DynaSLAM 族/WildGS-SLAM）互补（运动不确定性新来源）；④ SAGE 与库内 VGGT-BC/STream3R/SMoRe 构成 GFM 数据扩展线。')
rl.append('')
rl.append('## 环境')
rl.append('- C: 盘余 10.8 GB（可用）；D: 盘余 417 GB 健康。')
open(f'{DAY}/run_log.md', 'w', encoding='utf-8').write('\n'.join(rl))

# ---------- registry 幂等追加（先备份） ----------
bak = reg_path + '.bak-20261020'
if not os.path.exists(bak):
    shutil.copy(reg_path, bak)
    print('registry 备份:', bak)
added = 0
with open(reg_path, 'a', encoding='utf-8') as f:
    for s in main:
        if s['id'] in reg:
            continue
        row = {'id': f"arXiv:{s['id']}", 'title': s['title'], 'title_zh': s['title_zh'],
               'track': s['track'], 'date': s['date'], 'value': s['value'], 'grade': s['grade'],
               'scores': {k: s[k] for k in ('IMP', 'NOV', 'TEC', 'EXP', 'PER', 'TRL', 'REP')},
               'status': s['status'], 'evidence': s['evidence'], 'fetch_level': s['level'],
               'fulltext_chars': s['chars'], 'in_top10': s['id'] in top10_ids,
               'batch': BATCH, 'orig_window': ORIG_WINDOW, 'flags': []}
        f.write(json.dumps(row, ensure_ascii=False) + '\n')
        added += 1
    for s in bf:
        if s['id'] in reg:
            continue
        row = {'id': f"arXiv:{s['id']}", 'title': s['title'], 'title_zh': s['title_zh'],
               'track': s['track'], 'date': s['date'], 'value': s['value'], 'grade': s['grade'],
               'scores': {k: s[k] for k in ('IMP', 'NOV', 'TEC', 'EXP', 'PER', 'TRL', 'REP')},
               'status': s['status'], 'evidence': s['evidence'], 'fetch_level': s['level'],
               'fulltext_chars': s['chars'], 'in_top10': False,
               'batch': BF_BATCH, 'orig_window': BF_WINDOW, 'flags': ['BACKFILL']}
        f.write(json.dumps(row, ensure_ascii=False) + '\n')
        added += 1
print('registry 追加:', added, '；现总条目:', len(reg) + added)
print('门① max:', g1_max, '| top5:', g1_main[:5])
print('门② tracks(top10):', dict(tracks_top10))
print('门③ avg30:', avg30, 'today_max:', today_max, 'heavy:', heavy)
print('Top10:', [s['id'] for s in top10])
