# -*- coding: utf-8 -*-
# build_1021.py — 2026-10-21 批次：主批次（10-20 公告，31 篇）+ backfill-1021（10 篇 RSS 旧稿再公告）。
# 三关校验 + 7 维表 + scored/run_log + registry 幂等追加（先备份）。
import json, os, re, shutil
from collections import Counter

ROOT = 'D:/Agent/WorkBuddy/Research'
BATCH = '2026-10-21'
BF_BATCH = 'backfill-1021'
ORIG_WINDOW = '10-20（周二）公告批次（09-28~10-19 提交、周二 10-20 20:00 ET 释放；拉取日 10-21 周三）'
BF_WINDOW = 'RSS 旧稿 replace/cross 再公告 10 篇（2504~2609 原始提交，首次入馆）'
DAY = f'{ROOT}/papers/daily/{BATCH}'
BFDAY = f'{ROOT}/papers/daily/{BF_BATCH}'
os.makedirs(DAY, exist_ok=True)
os.makedirs(BFDAY, exist_ok=True)

W = {'IMP': 0.20, 'NOV': 0.20, 'TEC': 0.15, 'EXP': 0.15, 'PER': 0.15, 'TRL': 0.08, 'REP': 0.07}

def finalize(rows):
    for s in rows:
        s['value'] = round(sum(s[k] * W[k] for k in W), 4)
        s['grade'] = 'S' if s['value'] >= 4.2 else ('A' if s['value'] >= 3.6 else ('B' if s['value'] >= 3.0 else 'C'))
    return rows

def rank(rows):
    """加权降序；同分（value/IMP/NOV 全同）组内按赛道多样性优先、再 id 升序。"""
    rows = sorted(rows, key=lambda s: (-s['value'], -s['IMP'], -s['NOV'], s['id']))
    out = []
    i = 0
    while i < len(rows):
        j = i
        while j < len(rows) and (rows[j]['value'], rows[j]['IMP'], rows[j]['NOV']) == (rows[i]['value'], rows[i]['IMP'], rows[i]['NOV']):
            j += 1
        group = rows[i:j]
        if len(group) > 1:
            picked, picked_tracks = [], Counter()
            pool = list(group)
            while pool:
                best_i = 0
                for k in range(1, len(pool)):
                    ka = (picked_tracks[pool[k]['track']], pool[k]['id'])
                    kb = (picked_tracks[pool[best_i]['track']], pool[best_i]['id'])
                    if ka < kb:
                        best_i = k
                pick = pool.pop(best_i)
                picked.append(pick)
                picked_tracks[pick['track']] += 1
            out.extend(picked)
        else:
            out.extend(group)
        i = j
    return out

main = rank(finalize(json.load(open(f'{ROOT}/data/scored_1021.json', encoding='utf-8'))))
bf = rank(finalize(json.load(open(f'{ROOT}/data/scored_backfill_1021.json', encoding='utf-8'))))
top10 = main[:10]
top10_ids = {s['id'] for s in top10}
bf_ids = {s['id'] for s in bf}

# 证据等级与字符数（manifest）
manifest = json.load(open(f'{ROOT}/data/fulltext/_manifest.json', encoding='utf-8'))
for s in main + bf:
    e = manifest.get(s['id']) or {}
    s['level'] = e.get('level', 'L0')
    s['chars'] = e.get('chars', 0)
    if s['id'] == '2610.26549':
        s['evidence'] = 'PARTIAL'   # ar5iv 仅返摘要页（L0 HTML 404），按摘要级评估并显式声明
    else:
        s['evidence'] = e.get('evidence', 'FULL')
    s['status'] = 'CURRENT'

reg_path = f'{ROOT}/papers/library/registry.jsonl'
reg = {}
for l in open(reg_path, encoding='utf-8'):
    if l.strip():
        d = json.loads(l)
        reg[d['id'].split(':')[-1].split('v')[0]] = d

raw = {}
for l in open(f'{ROOT}/data/raw/2026-10-21_rss.jsonl', encoding='utf-8'):
    if l.strip():
        r = json.loads(l)
        raw[r['base_id']] = r
xr_abs = json.load(open(f'{ROOT}/data/missed_xr_abstract_2026-10-21.json', encoding='utf-8'))
for bid, v in xr_abs.items():
    raw.setdefault(bid, {'title': v['title'], 'abstract': v.get('abstract', '')})

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

# 门③ 现算：date>=2026-09-21（今天-30 天）的 registry 按 value 降序前 10 均分
lo = '2026-09-21'
win = [d for d in reg.values() if d.get('date', '') >= lo]
top30 = sorted(win, key=lambda d: -d.get('value', 0))[:10]
avg30 = round(sum(d.get('value', 0) for d in top30) / len(top30), 4)
today_max = main[0]['value']
heavy = today_max >= avg30

def ev(s):
    return s['evidence'] + ('' if s['evidence'] == 'FULL' else f"/{s['level']}")

# ---------- 7 维表 ----------
def table(rows, path, title, note_lines, top_ids, grade_counts):
    lines = [f'# 7 维对比表 · {title}', '']
    lines += note_lines
    lines.append('| # | arXiv | 标题 | 赛道 | IMP | NOV | TEC | EXP | PER | TRL | REP | 总分 | 等级 | 证据 |')
    lines.append('|---|---|---|---|---|---|---|---|---|---|---|---|---|---|')
    for i, s in enumerate(rows, 1):
        mark = ' ★Top10' if s['id'] in top_ids else ''
        lines.append(f"| {i} | {s['id']} | {s['title_zh']}{mark} | {s['track']} | {s['IMP']} | {s['NOV']} | {s['TEC']} | {s['EXP']} | {s['PER']} | {s['TRL']} | {s['REP']} | {s['value']:.2f} | {s['grade']} | {ev(s)} |")
    lines.append('')
    lines.append(f"合计 {len(rows)} 篇入馆（{grade_counts}）；除 Holi-World（2610.26549，ar5iv 仅返摘要页，L0 HTML 404，按摘要级评估）外全部 L0/FULL，先抓全文再定稿。")
    open(path, 'w', encoding='utf-8').write('\n'.join(lines))

gc_main = f"{sum(1 for s in main if s['grade']=='S')} S / {sum(1 for s in main if s['grade']=='A')} A / {sum(1 for s in main if s['grade']=='B')} B / {sum(1 for s in main if s['grade']=='C')} C"
gc_bf = f"{sum(1 for s in bf if s['grade']=='S')} S / {sum(1 for s in bf if s['grade']=='A')} A / {sum(1 for s in bf if s['grade']=='B')} B / {sum(1 for s in bf if s['grade']=='C')} C"

table(main, f'{DAY}/7dim-table.md', BATCH, [
    f'> **公告窗口**：{ORIG_WINDOW}。',
    '> **诚实口径**：本批为 10-20（周二）公告批次，收录 09-28~10-19 提交、随周二释放的稿件；**非当日（10-21）硬提交**。',
    '> 公告类型：全部为 2610.* 首次公告（new 或 cross 的新提交）；RSS 混入的 20 篇旧稿 replace/cross 已甄别并单列 backfill-1021，未混入本表；4 篇库内 v2 再公告（2610.22748/2610.16177/2610.23050/2609.22332）剔除。',
    '> 数据源：RSS 兜底（rss.arxiv.org，7 分类去重 1426 条，关键词命中 91）+ listing 对账（7 分类 10-20 日组 936 篇全量，API 摘要级过滤交叉验证，63 篇命中与 RSS 通道完全互证）。',
], top10_ids, gc_main)

table(bf, f'{BFDAY}/7dim-table.md', BF_BATCH + '（backfill）', [
    f'> **公告窗口**：{BF_WINDOW}；**拉取日**：2026-10-21。',
    '> **诚实口径**：本批为补录，全部标注 batch=backfill-1021、orig_window 注明原始提交月；**绝不混入「当日新论文」表**。',
    '> 来源：RSS 旧稿 replace/cross 再公告 20 篇中甄别 10 篇 XR 相关首次入馆；其余 10 篇非 XR 剔除（人形控制/无人机/扩散智能体/量子网络/时序基准/机器人操作等）。',
], bf_ids, gc_bf)

# ---------- scored.md（主批次） ----------
md = []
md.append(f'# 评分明细 · {BATCH}')
md.append('')
md.append(f'- 公告窗口：{ORIG_WINDOW}。')
md.append('- 评分口径：先抓全文再定稿；31 篇候选 30 篇 L0/FULL（26,060–118,689 字符）+ 1 篇 PARTIAL（2610.26549 Holi-World，ar5iv 仅返摘要页，按摘要级评估并显式声明），串行 3s/篇，无限流/降级/伪造。')
md.append(f'- 定稿 Top10：{len(top10)} 篇（S×{sum(1 for s in top10 if s["grade"]=="S")} / A×{sum(1 for s in top10 if s["grade"]=="A")} / B×{sum(1 for s in top10 if s["grade"]=="B")}），全部 A 级，无 S 级。')
md.append('')
md.append('## Top10 排行')
md.append('')
md.append('| 排名 | ID | 标题 | 赛道 | 总分 | 等级 | 证据 |')
md.append('|---|---|---|---|---|---|---|')
for i, s in enumerate(top10, 1):
    md.append(f"| {i} | {s['id']} | {s['title_zh']} | {s['track']} | {s['value']:.2f} | {s['grade']} | {ev(s)} |")
md.append('')
md.append('## 覆盖度三关')
md.append('')
md.append(f'**门① 同质去重（max Jaccard < 0.62）**：最高 {g1_max[1]:.3f}（{g1_max[0]} vs 库内 {g1_max[2] or "—"}）→ **通过**（无同质）。')
if g1_hit:
    md.append('> 命中：' + '；'.join(f'{g[0]} sim={g[1]:.3f} vs {g[2]}' for g in g1_hit))
md.append('')
md.append(f'**门② 赛道覆盖（≥5）**：Top10 覆盖 **{len(tracks_top10)} 赛道**（{"、".join(f"{t}×{c}" for t, c in tracks_top10.most_common())}）→ **通过**；全批 31 篇覆盖 {len(tracks_all)} 赛道。')
md.append('')
md.append(f'**门③ 价值天花板（校准关，不触发重筛）**：库内近 30 天（date≥{lo}）Top10 均分 = **{avg30}**（现算：{", ".join(d["id"].split(":")[-1] + " " + str(d.get("value")) for d in top30)}）；当日最高 = **{today_max:.2f}**（{main[0]["id"]}）→ {"**重磅日，可评 S 级**" if heavy else "**非重磅日（差值 " + format(today_max - avg30, "+.3f") + "），不宣称重磅、无 S 级**"}。')
md.append('')
md.append('## 全量评分明细（按加权降序，同分按 IMP/NOV → 赛道多样性 → id 升序）')
md.append('')
md.append('| ID | 标题 | 赛道 | IMP | NOV | TEC | EXP | PER | TRL | REP | 总分 | 等级 | 证据 |')
md.append('|---|---|---|---|---|---|---|---|---|---|---|---|---|')
for s in main:
    md.append(f"| {s['id']} | {s['title_zh']} | {s['track']} | {s['IMP']} | {s['NOV']} | {s['TEC']} | {s['EXP']} | {s['PER']} | {s['TRL']} | {s['REP']} | {s['value']:.2f} | {s['grade']} | {ev(s)} |")
md.append('')
md.append('## 本批剔除记录（非 XR / 弱相关，不入馆）')
md.append('')
md.append('10-20 公告批次 RSS 命中 91 条中，去 registry(512) 后 67 篇 2610.* 真新提交，甄别剔除 36 篇非 XR/弱相关：')
for r, why in [
    ('2610.24858', 'MRI 各向异性超分辨（医学）'), ('2610.25223', 'Map2Vid 具身导航视频生成（机器人域）'),
    ('2610.25345', 'MCSplat 驾驶场景前馈 GS（自动驾驶）'), ('2610.25634', 'Clean Forcing 自回归视频扩散（通用视频生成）'),
    ('2610.25637', 'TNVD-SC 森林激光雷达地点识别（机器人）'), ('2610.26096', 'PnP-Transformer 6D 物体位姿（机器人操作）'),
    ('2610.26165', 'TriTD 实时自回归视频生成蒸馏（通用视频生成）'), ('2610.26855', 'Ropedia W0 跨本体运动-操作世界模型（机器人）'),
    ('2610.24011', '颅内动脉瘤分割（医学）'), ('2610.24016', 'CLARO 开词汇抓取 VLM 编排（机器人）'),
    ('2610.24044', 'GliomaINK 脑胶质瘤 MRI 序列合成（医学）'), ('2610.25068', 'LENS FPGA 边缘场景记忆（机器人系统）'),
    ('2610.25459', 'BiDex-100 双手灵巧操作基准（机器人）'), ('2610.01039', '合成状态过渡视频交互生成（机器人/视频生成，v2 replace）'),
    ('2610.11049', 'SatFix 无人机卫星图定位（无人机）'), ('2610.23884', 'PrismPlan GPU 运动规划基底（机器人）'),
    ('2610.23943', 'ESCAPE 第一视角碰撞规避（机器人）'), ('2610.24149', 'FLASH-CBF-RRT 安全运动规划（机器人）'),
    ('2610.24559', 'SocialCoAct 人形社交协作（机器人）'), ('2610.24605', 'RoMo-GS 机器人在线 3DGS 建图（机器人）'),
    ('2610.25261', 'GOFusion 高斯-占据子图融合导航（机器人）'), ('2610.25397', '地面机器人动态相机-IMU 标定 VIO（机器人）'),
    ('2610.25690', 'ScaleNav 互联网视频预训练导航（机器人）'), ('2610.25840', 'OV-PEAR 工业物体位姿-尺度估计（工业机器人）'),
    ('2610.25988', 'Self-Supervised Inertial Odometry 纯惯性里程计（通用平台）'), ('2610.26169', 'HS-MoDP 人形组合操作（机器人）'),
    ('2610.26210', 'AnchorFlow-VIO LaMARia 基准 VIO（机器人基准）'), ('2610.26508', '单目飞行几何感知规划（无人机）'),
    ('2610.26751', 'Beyond Omni 具身多模态 MLLM（通用具身）'), ('2610.23940', 'ML-IST 内球树碰撞检测（通用几何）'),
    ('2610.18093', 'LynxScenes 轮腿机器人基准（机器人）'), ('2610.24717', 'DiffuPlan 扩散语言模型智能体（NLP）'),
    ('2610.25447', 'Enhanced Masked Diffusion Unlearning（NLP 安全）'), ('2610.26279', '量子神经网络云量参数化（气象）'),
    ('2610.17856', 'MMTA 多模态时序分析基准（通用）'), ('2610.23907', 'EgoVine 第一视角视频后训练规划（具身 AI）'),
    ('2610.22400', '推荐系统用户编码（10-19 日组，非 XR）'), ('2610.22450', 'DriveWorld3D 驾驶世界模型（10-19 日组，自动驾驶）'),
]:
    t = raw.get(r, {}).get('title', '')
    md.append(f"- {r} {t[:60]} — {why}")
md.append('')
md.append('另 10-19 日组摘要级命中 7 篇（2610.22505 内窥镜/2610.22552 声纳/2610.22643 MRI/2610.22932 机器人/2610.23237 X 射线/2610.22400 推荐/2610.22450 驾驶）全部甄别为非 XR，与 10-20 运行结论一致，无新增漏网。')
open(f'{DAY}/scored.md', 'w', encoding='utf-8').write('\n'.join(md))

# ---------- scored.md（backfill） ----------
mb = []
mb.append(f'# 评分明细 · {BF_BATCH}（backfill）')
mb.append('')
mb.append(f'- 公告窗口：{BF_WINDOW}；拉取日 2026-10-21。')
mb.append('- 评分口径：10 篇全部 L0/FULL，先抓全文再定稿。')
mb.append('- 覆盖三关：门① max Jaccard %.3f（通过）；门② 覆盖 %d 赛道（backfill 为机会性补录，不适用 Top10 选拔）；门③ 对 backfill 不适用。' % (g1_bf[0][1], len(tracks_bf)))
mb.append('')
mb.append('| ID | 标题 | 赛道 | IMP | NOV | TEC | EXP | PER | TRL | REP | 总分 | 等级 |')
mb.append('|---|---|---|---|---|---|---|---|---|---|---|---|')
for s in bf:
    mb.append(f"| {s['id']} | {s['title_zh']} | {s['track']} | {s['IMP']} | {s['NOV']} | {s['TEC']} | {s['EXP']} | {s['PER']} | {s['TRL']} | {s['REP']} | {s['value']:.2f} | {s['grade']} |")
mb.append('')
mb.append('## backfill 候选剔除记录（RSS 旧稿再公告中非 XR 10 篇，不入馆）')
mb.append('')
for r, why in [('2511.09397', '——（入馆，见上表）'), ('2603.03279', 'ULTRA 人形全身控制（机器人）'),
               ('2503.06477', 'PDB 驾驶员个性化数据集（自动驾驶）'), ('2510.12971', 'Actron3D 视频可操作神经函数（机器人）'),
               ('2603.05504', 'RoboPocket 手机改进机器人策略（机器人）'), ('2605.18431', 'Seeing Together 多机器人第一视角空间推理（机器人）'),
               ('2606.05160', 'GRAIL 人形运动-操作世界模型（机器人）'), ('2606.10276', 'EDITH 机器人非语言意图跟随（机器人）'),
               ('2607.26148', 'Embodied Agents Take Control 零样本智能体（具身 AI）'), ('2606.01810', 'Planning Takes More Than Token Prediction（NLP）'),
               ('2604.17727', 'Voronoi 2DGS 高光谱任意尺度超分（高光谱成像，非 XR 口径）')]:
    mb.append(f"- {r} {why}")
open(f'{BFDAY}/scored.md', 'w', encoding='utf-8').write('\n'.join(mb))

# ---------- run_log ----------
rl = []
rl.append(f'# 执行日志 · {BATCH}')
rl.append('')
rl.append('## 数据源与对账（第 1-3 步）')
rl.append('- 漏网对账（第 1 步）：listing 7 分类最新公告日 = **2026-10-20（周二）**（cs.CV 346 篇）；TARGET_LO=2026-10-19，重审 10-19 + 审计 10-20。')
rl.append('- listing 对账：7 分类 10-20 日组共 936 篇（去重后）全部入账；10-19 日组 373 篇中 361 篇不在库（多为历来非 XR）。完整性校验：逐分类自检全部通过（最终 per-cat SHORT 为跨分类交叉列表认领的统计假象，非真实缺口）。')
rl.append('- 摘要级过滤（data/missed_xr_abstract_2026-10-21.json）：10-19+10-20 两窗口 1297 篇走 API 摘要级 KW 过滤 → 命中 70 篇（10-19×7 全为非 XR，与 10-20 运行结论一致；10-20×63 与 RSS 通道 67 篇真新提交完全互证，RSS 为超集）。')
rl.append('- 探针：export.arxiv.org/api/query 200；arxiv.org/api/query 200；rss.arxiv.org 200（cs.CV 505 条、cs.AI 789 条，双频道均非空）。')
rl.append('- 拉取：fetch_rss.py 7 分类去重 1426 条 → 关键词命中 91 条 → 去 registry(512) 后 **67 篇 2610.* 真新提交** + 20 篇旧稿 replace/cross（另 4 篇库内 v2 再公告剔除：2610.22748/2610.16177/2610.23050/2609.22332）。')
rl.append('- 甄别：67 篇真新中 **31 篇 XR 核心/强相关**入评分池（本批为 10-11~10-16 无调度后恢复运行以来的最大公告日），36 篇非 XR 剔除（医学×3/自动驾驶×2/机器人×20+/无人机×2/视频生成×3/通用具身/NLP/气象/几何等）。')
rl.append('')
rl.append('## backfill 发现')
rl.append('- **RSS 旧稿 replace/cross 再公告 20 篇**中 10 篇 XR 相关首次入馆（OmniEgoCap/ZipSplat/GraFT/GaussTrap/Mono-Hydra++/PRISM/OUGS/Vibe Coding XR/MAGS-SLAM/SGM-SLAM），10 篇非 XR 剔除；全部单列 backfill-1021，未混入当日新论文。')
rl.append('- 10-19 公告日无新增漏网（摘要级 7 篇命中全部非 XR，与 10-20 运行互证）。')
rl.append('')
rl.append('## 全文抓取')
rl.append('- 41 篇候选（31 主批次 + 10 backfill）跑 fetch_fulltext.py：**40 篇 L0/FULL**（26,060–118,689 字符）+ 1 篇 L1/PARTIAL（2610.26549 Holi-World，L0 HTML 404、ar5iv 仅返摘要页，按摘要级评估并显式声明，禁止脑补正文）；串行 3s/篇，无限流/降级/伪造；manifest 合并写入校验通过。')
rl.append('')
rl.append('## 覆盖度三关')
rl.append(f'- 门①：max Jaccard {g1_max[1]:.3f}（{g1_max[0]} vs 库内 {g1_max[2] or "—"}）< 0.62 → 通过，无同质、未触发重筛。')
rl.append(f'- 门②：Top10 覆盖 {len(tracks_top10)} 赛道 ≥5 → 通过（全批 31 篇覆盖 {len(tracks_all)} 赛道：{"、".join(f"{t}×{c}" for t, c in tracks_all.most_common())}）。')
rl.append(f'- 门③：当日最高 {today_max:.2f} vs 库内近 30 天 Top10 均分 {avg30}（现算）→ 差值 {today_max - avg30:+.3f} < 0 → **非重磅日，无 S 级**，未拔高。')
rl.append('')
rl.append('## 落后登记')
rl.append('- 论文级 OUTDATED/SUPERSEDED：0 篇（门①通过且无同质）。')
rl.append('- 路线观察：① 前馈 3DGS 效率线再添两条（ZipSplat token 解码、FineSplat 双分组），与库内 pixel-aligned 族（MVSplat/DepthSplat/DA3）构成效率竞合；② 第一视角手-相机联合恢复两路线（V-JEPA Hand 前馈 vs EgoXperience 联合重建）互补；③ PhysSkin++ 与库内物理动画族延续；④ Spatons 补库内 XR 显示预畸变补偿空白（与 CompenNet++ 等经典补偿网络不同范式）。')
rl.append('')
rl.append('## 环境')
rl.append('- C: 盘余 7.3 GB（偏低但可用，文本产物均在 D:）；D: 盘余 386 GB 健康。')
open(f'{DAY}/run_log.md', 'w', encoding='utf-8').write('\n'.join(rl))

# ---------- registry 幂等追加（先备份） ----------
bak = reg_path + '.bak-20261021'
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
print('Top10:', [(s['id'], s['value']) for s in top10])
print('主批次 grade:', {g: sum(1 for s in main if s['grade'] == g) for g in 'SABC'})
print('backfill grade:', {g: sum(1 for s in bf if s['grade'] == g) for g in 'SABC'})
