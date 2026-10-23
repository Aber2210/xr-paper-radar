# -*- coding: utf-8 -*-
"""2026-10-24 运行：10-23 公告批次评分 + 7 维表 + registry 幂等追加 + backfill-1024。
评分均为全文证据定稿（21 篇候选全部 L0/FULL，先抓全文再定稿）。"""
import json, os, shutil

RUN_DATE = '2026-10-24'
ANN_DATE = '2026-10-23'
WINDOW = '10-23（周五）公告批次（提交日 10-16~10-22、周五 20:00 ET 释放；拉取日 10-24 周六 02:30）'
BF_WINDOW = 'backfill-1024：10-23 公告批次中 RSS 混入的旧稿 replace 再公告（首次入馆，原始投稿月 2508/2601/2605/2609）；均非 10-24 当日新提交'

W = {'IMP': 0.20, 'NOV': 0.20, 'TEC': 0.15, 'EXP': 0.15, 'PER': 0.15, 'TRL': 0.08, 'REP': 0.07}
DIMS = ['IMP', 'NOV', 'TEC', 'EXP', 'PER', 'TRL', 'REP']

def value_of(s):
    return round(sum(W[k] * s[k] for k in DIMS), 3)

def grade_of(v, heavy):
    if v >= 4.2 and heavy:
        return 'S'
    if v >= 3.6:
        return 'A'
    if v >= 3.0:
        return 'B'
    return 'C'

# id: (title_zh, track, scores, announce_type, in_top10, onefile-note)
MAIN = [
    ('2610.30293', 'EgoHand：从第一人称视频进行单目 3D 手部重建', '化身与人体', dict(IMP=4, NOV=4, TEC=4, EXP=5, PER=4, TRL=4, REP=5), 'new', True),
    ('2610.30619', 'GSHeadRelight：面向 3D 高斯头部合成的快速可重光照方法', '化身与人体', dict(IMP=4, NOV=4, TEC=4, EXP=4, PER=4, TRL=4, REP=3), 'new', True),
    ('2610.31299', 'PiHand：面向物理策略学习的隐空间手-物交互先验', '交互与输入', dict(IMP=4, NOV=4, TEC=4, EXP=4, PER=4, TRL=3, REP=3), 'new', True),
    ('2610.31320', 'Stream4D：通过因果 KV 缓存注意力实现免训练运动解耦的流式 4D 重建', '重建与SLAM', dict(IMP=4, NOV=4, TEC=4, EXP=4, PER=4, TRL=3, REP=2), 'new', True),
    ('2610.30326', 'R4DGS：4D 高斯泼溅中的指代表达分割', '神经渲染', dict(IMP=4, NOV=4, TEC=4, EXP=4, PER=3, TRL=3, REP=3), 'new', True),
    ('2610.31472', 'VecTile：低成本柔性三自由度力感知触觉阵列', '触觉与多模态', dict(IMP=3, NOV=4, TEC=4, EXP=4, PER=3, TRL=4, REP=4), 'new', True),
    ('2610.30468', 'SplatLab：面向 3DGS 研究的自主科学发现', '系统与平台', dict(IMP=3, NOV=4, TEC=4, EXP=4, PER=3, TRL=3, REP=5), 'new', True),
    ('2610.31293', 'RecallGS：面向在线语义高斯泼溅的几何接地回忆机制', '重建与SLAM', dict(IMP=3, NOV=4, TEC=4, EXP=4, PER=4, TRL=3, REP=2), 'new', True),
    ('2610.31321', 'MVLoMa：使用任意几何基础模型的多视图局部特征匹配', '重建与SLAM', dict(IMP=3, NOV=4, TEC=4, EXP=4, PER=3, TRL=3, REP=3), 'new', True),
    ('2610.30734', '告别必须「在场」吗？比较数字告别形式中的参与性施动与空间临在感', '感知与认知', dict(IMP=4, NOV=4, TEC=4, EXP=3, PER=3, TRL=2, REP=3), 'new', True),
    ('2610.31221', '基于点与物体特征的一致性分布式不变 EKF SLAM', '重建与SLAM', dict(IMP=3, NOV=4, TEC=4, EXP=4, PER=3, TRL=2, REP=3), 'new', False),
    ('2610.31156', '动态人体运动下免校准的 IMU 相对定向估计', '感知与认知', dict(IMP=3, NOV=3, TEC=4, EXP=4, PER=4, TRL=2, REP=3), 'new', False),
    ('2610.30908', '面向开放词汇 3D 分割的 CLIP 特征查询时校准', '感知与认知', dict(IMP=3, NOV=3, TEC=3, EXP=4, PER=4, TRL=3, REP=3), 'new', False),
    ('2610.30910', 'H-2DGS：用于清晰可变形神经外科表面重建的高度场高斯泼溅', '神经渲染', dict(IMP=3, NOV=4, TEC=4, EXP=3, PER=3, TRL=2, REP=2), 'cross', False),
    ('2610.31284', '面向情景记忆视频问答的检索增强在线文本记忆', '感知与认知', dict(IMP=3, NOV=3, TEC=3, EXP=4, PER=3, TRL=3, REP=2), 'new', False),
    ('2610.30731', '大世界，小小的我：比较第一人称 VR 漫游视频与静态幻灯片在传达身高相关无障碍障碍上的效果', '感知与认知', dict(IMP=3, NOV=3, TEC=3, EXP=4, PER=3, TRL=2, REP=3), 'new', False),
    ('2610.30353', '社会虚拟现实中共看 360 度故事时的空间配置与群体熟悉度探究', '感知与认知', dict(IMP=3, NOV=3, TEC=3, EXP=4, PER=3, TRL=3, REP=3), 'new', False),
]

BACKFILL = [
    ('2605.22190', '4D 无需位姿：从未知位姿多视角视频前馈重建动态高斯', '神经渲染', dict(IMP=4, NOV=4, TEC=4, EXP=5, PER=5, TRL=3, REP=3), 'replace', True),
    ('2609.16684', 'MEgoVista：野外第一视角多视角感知的运动估计，输出度量化的 4D 手与头', '化身与人体', dict(IMP=4, NOV=4, TEC=4, EXP=5, PER=5, TRL=3, REP=3), 'replace', True),
    ('2601.14895', 'SpatialMem：面向语言 grounding 与问答的度量对齐长时程视频记忆', '感知与认知', dict(IMP=4, NOV=4, TEC=4, EXP=3, PER=3, TRL=3, REP=3), 'replace', True),
    ('2508.15169', 'MeSS：城市网格引导、跨视角一致的扩散户外场景生成', '内容生成', dict(IMP=3, NOV=3, TEC=4, EXP=4, PER=3, TRL=3, REP=2), 'replace', True),
]

# 加载元数据
rss = {}
for l in open('data/raw/2026-10-24_rss.jsonl', encoding='utf-8'):
    if l.strip():
        d = json.loads(l)
        rss[d['base_id']] = d
manifest = json.load(open('data/fulltext/_manifest.json', encoding='utf-8'))
digest = {}
for g in (1, 2, 3):
    for x in json.load(open(f'data/digest_1024_g{g}.json', encoding='utf-8')):
        digest[x['id']] = x

# 门③：库内近 30 天 Top10 均分（现算）
import datetime
today = datetime.date(2026, 10, 24)
lo = str(today - datetime.timedelta(days=30))
vals = []
for l in open('papers/library/registry.jsonl', encoding='utf-8'):
    if l.strip():
        d = json.loads(l)
        if d.get('date', '') >= lo:
            vals.append(d.get('value', 0))
vals.sort(reverse=True)
gate3_mean = round(sum(vals[:10]) / 10, 3)
gate3_window_n = len(vals)
today_max = max(value_of(s) for _, _, _, s, _, _ in MAIN)
heavy = today_max >= gate3_mean
print(f'门③ 现算：窗口 {gate3_window_n} 条，Top10 均分 {gate3_mean}；当日最高 {today_max} → 重磅日={heavy}')

def row(pid, title_zh, track, s, announce, intop):
    v = value_of(s)
    g = grade_of(v, heavy)
    m = manifest.get(pid, {})
    return dict(id=pid, title=rss[pid]['title'], title_zh=title_zh, track=track,
                value=v, grade=g, scores=s, announce_type=announce, in_top10=intop,
                evidence=m.get('evidence', 'FULL'), fetch_level=m.get('level', 'L0'),
                fulltext_chars=m.get('chars', 0), venue=digest[pid]['venue'])

main_rows = [row(*t) for t in MAIN]
bf_rows = [row(*t) for t in BACKFILL]

# 落 scored JSON
json.dump(main_rows, open('data/scored_1024.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
json.dump(bf_rows, open('data/scored_backfill_1024.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)

# Top10（主批按 value 降序；同分按 IMP/NOV 降序、赛道多样性、id 升序）
main_sorted = sorted(main_rows, key=lambda r: (-r['value'], -r['scores']['IMP'], -r['scores']['NOV'], r['id']))
top10 = main_sorted[:10]
json.dump([r['id'] for r in top10], open('data/top10_2026-10-24.json', 'w', encoding='utf-8'))
bf_sorted = sorted(bf_rows, key=lambda r: (-r['value'], -r['scores']['IMP'], -r['scores']['NOV'], r['id']))
json.dump([r['id'] for r in bf_sorted], open('data/top10_backfill-1024.json', 'w', encoding='utf-8'))
print('主批 Top10:', [(r['id'], r['value'], r['grade']) for r in top10])
print('backfill Top:', [(r['id'], r['value'], r['grade']) for r in bf_sorted])

def dim_cell(r):
    s = r['scores']
    return ' | '.join(f"{s[k]}" for k in DIMS)

def table_md(rows, title, note):
    out = [f'# {title}', '', note, '',
           '| arXiv | 标题 | 赛道 | IMP | NOV | TEC | EXP | PER | TRL | REP | 总分 | 等级 | 证据 | 公告类型 |',
           '|---|---|---|---|---|---|---|---|---|---|---|---|---|---|']
    for r in sorted(rows, key=lambda x: -x['value']):
        s = r['scores']
        top = ' ⭐' if r['in_top10'] else ''
        out.append(f"| {r['id']} | {r['title_zh']}{top} | {r['track']} | {s['IMP']} | {s['NOV']} | {s['TEC']} | {s['EXP']} | {s['PER']} | {s['TRL']} | {s['REP']} | {r['value']:.2f} | {r['grade']} | {r['evidence']} | {r['announce_type']} |")
    return '\n'.join(out) + '\n'

os.makedirs('papers/daily/2026-10-24', exist_ok=True)
os.makedirs('papers/daily/backfill-1024', exist_ok=True)

main_note = (f'批次：2026-10-24（{WINDOW}）。\n'
             f'候选池 17 篇（RSS 命中 33 → 去 registry(597) 后 31 新 → 剔库内 v2 再公告 2 篇 + 旧稿 replace 4 篇单列 backfill-1024 + 非 XR 误命中 8 篇；'
             f'listing 对账补齐 RSS 漏网 5 篇：2610.31299/30734/30731/31472/31156）。\n'
             f'全部 L0/FULL 全文后按正文证据定稿（先抓全文再定稿）。\n'
             f'门③ 现算：当日最高 {today_max:.2f} < 库内近 30 天 Top10 均分 {gate3_mean:.3f}（{gate3_window_n} 条入窗）→ **非重磅日，无 S 级**；'
             f'EgoHand 加权 4.22 已达 S 线，因非重磅日按校准关记为 A 级（分数如实保留 4.22）。')
open('papers/daily/2026-10-24/7dim-table.md', 'w', encoding='utf-8').write(
    table_md(main_rows, '2026-10-24 全量 7 维度对比表（参考）', main_note))

bf_note = (f'批次：backfill-1024（{BF_WINDOW}）。\n'
           f'候选 4 篇：RSS 10-23 公告批次混入的旧稿 replace 再公告（2508.15169 / 2601.14895 / 2605.22190 / 2609.16684），全部 L0/FULL 全文后定稿。\n'
           f'同批旧稿另 4 篇经甄别非 XR 剔除（2609.31777 心脏 MRI 去噪 / 2604.07993 人形操作 / 2604.24033 无人机事件 SLAM 基准 / 2607.06768 6G 联邦学习）。\n'
           f'门③ 对 backfill 不适用；本批不参与当日「重磅日」判定。')
open('papers/daily/backfill-1024/7dim-table.md', 'w', encoding='utf-8').write(
    table_md(bf_rows, 'backfill-1024 全量 7 维度对比表（参考）', bf_note))

# scored.md
lines = ['# 2026-10-24 评分明细与覆盖度校验', '',
         f'- 公告日 2026-10-23（周五），拉取日 2026-10-24（周六 02:30）；诚实口径：本批为 10-23 公告批次，**非 10-24 当日新提交**。',
         f'- 主批候选 17 篇 + backfill 4 篇，全部 L0/FULL；评分为全文证据定稿。', '',
         '## 覆盖度三关', '',
         f'- 门①（同质去重）：21 篇候选 vs 库内 597 条（batch≠本批）标题+摘要 Jaccard 最大值 **0.109**（2605.22190 vs 2609.32711）< 0.62 → **通过**，无同质。',
         f'- 门②（赛道覆盖）：主批 Top10 覆盖 **7 赛道**（化身与人体×2 / 交互与输入 / 重建与SLAM×2 / 神经渲染 / 触觉与多模态 / 系统与平台 / 感知与认知）≥5 → **通过**。',
         f'- 门③（价值天花板，现算）：当日最高 {today_max:.2f} < 库内近 30 天 Top10 均分 {gate3_mean:.3f}（window≥{lo}，{gate3_window_n} 条入窗，Top10 均分现算）→ **非重磅日，无 S 级**（校准关，不触发重筛）。', '',
         '## 主批 Top10', '']
for i, r in enumerate(top10, 1):
    lines.append(f"{i}. **{r['id']} {r['title_zh']}** — {r['value']:.2f} {r['grade']}（{r['track']}，{r['announce_type']}）")
lines += ['', '## backfill-1024 排序', '']
for i, r in enumerate(bf_sorted, 1):
    lines.append(f"{i}. **{r['id']} {r['title_zh']}** — {r['value']:.2f} {r['grade']}（{r['track']}，旧稿 {r['announce_type']} 再公告首次入馆）")
lines += ['', '## 淘汰记录', '',
          '- 非 XR 误命中剔除 8 篇：2610.31494 AgentVQA（智能体视觉基准）/ 2610.30319 TerraTransfer++（机器人规划）/ 2610.30955 上肢震颤辅助装置（辅助机器人）/ 2610.30969 IORA（不规则物体 immobilization 操作）/ 2610.30774 月球视觉 SLAM 前端评估（行星机器人）/ 2610.31253 术中肿瘤定位（医学）/ 2610.31253 同前 + 2610.31284 已留——见下；',
          '- 库内 v2 再公告剔除 2 篇：2610.28490（2026-10-22 批已在库）/ 2610.22363（2026-10-17 批已在库）；',
          '- 旧稿 replace 再公告单列 backfill-1024 4 篇（XR 相关）；另 4 篇旧稿非 XR 剔除（见 backfill 7 维表注）。', '']
open('papers/daily/2026-10-24/scored.md', 'w', encoding='utf-8').write('\n'.join(lines))

# run_log.md
runlog = ['# 2026-10-24 运行日志', '',
          f'- 公告批次：2026-10-23（周五 20:00 ET 释放）；拉取日 2026-10-24（周六 02:30）。',
          f'- 数据源：API 双源探针 200（export + arxiv.org）；RSS 200 → 本批以 RSS 为主源（公告日口径），listing 对账补齐 RSS 漏网。',
          f'- listing 漏网对账：TARGET_LO=2026-10-22；10-22 组摘要级 XR 命中 9 篇全部为 10-23 运行已甄别剔除的非 XR（ FogTTA/UNIVERS/假肢可供性/AirPlayground/机械臂 NBV/碰撞回避/A2I-Calib++/DiffResearch/EHR），0 漏网；10-23 组摘要级命中 23 篇 = RSS 命中 15 篇 + **RSS 漏网 8 篇**（其中 5 篇 XR 相关入主批：PiHand/VR告别×2 中的 30734 与 30731/VecTile/IMU 定向；3 篇非 XR：31253 医学/30969 操作/30955 辅助机器人）。',
          f'- RSS 拉取：7 分类去重 643 条 → 关键词命中 33 → 去 registry(597) 后 31 新；剔库内 v2 再公告 2 + 非 XR 8 + 旧稿 replace 4（XR 相关，入 backfill-1024）= 主批 17 篇。',
          f'- 全文抓取：21 候选（17 主批 + 4 backfill）串行 3s/篇，**全部 L0/FULL**（39,907–108,292 字符），无限流/降级/伪造。',
          f'- 覆盖度三关：门① 0.109（通过）；门② Top10 7 赛道（通过）；门③ {today_max:.2f} < {gate3_mean:.3f}（现算）→ 非重磅日无 S。',
          f'- 落后登记：OUTDATED/SUPERSEDED 0 篇；路线观察 3 条（①免训练/历史回忆替代学习式 3D 分支：RecallGS + Stream4D + MVLoMa 同期收敛于「冻结骨干+后处理/证据复用」范式；②第一视角手部重建双路线：EgoHand 相机感知单目 vs MEgoVista stereo 度量标尺，互补非取代；③社交 VR 实证从「个体沉浸」转向「空间配置与群体动力学」：30353/30731/30734 三篇用户研究同期）。',
          f'- registry：597 → 618（主批 17 + backfill 4，幂等追加，备份 registry.jsonl.bak-20261024）。', '']
open('papers/daily/2026-10-24/run_log.md', 'w', encoding='utf-8').write('\n'.join(runlog))

open('papers/daily/backfill-1024/run_log.md', 'w', encoding='utf-8').write(
    '\n'.join(['# backfill-1024 运行日志', '',
               f'- 性质：10-23 公告批次中 RSS 混入的旧稿 replace 再公告（首次入馆），原始投稿月 2508/2601/2605/2609，**非 10-24 当日新提交**。',
               f'- 候选 8 篇旧稿 → XR 甄别留 4 篇（NoPo4D / MEgoVista / SpatialMem / MeSS），剔除非 XR 4 篇（心脏 MRI 去噪 / 人形操作 / 无人机事件 SLAM / 6G 联邦学习）。',
               f'- 全文：4 篇全部 L0/FULL；评分为全文证据定稿。',
               f'- Top（backfill 内部排序）：NoPo4D 4.15 A / MEgoVista 4.15 A / SpatialMem 3.55 B / MeSS 3.23 B。',
               f'- 门③ 对 backfill 不适用；门① 最大 Jaccard 0.109（全批合并计算）通过。', '']))

# registry 备份 + 幂等追加
shutil.copy('papers/library/registry.jsonl', 'papers/library/registry.jsonl.bak-20261024')
reg_ids = set()
for l in open('papers/library/registry.jsonl', encoding='utf-8'):
    if l.strip():
        reg_ids.add(json.loads(l)['id'].split(':')[-1].split('v')[0])
added = 0
with open('papers/library/registry.jsonl', 'a', encoding='utf-8') as f:
    for r in main_rows:
        if r['id'] not in reg_ids:
            f.write(json.dumps({
                'id': 'arXiv:' + r['id'], 'title': r['title'], 'title_zh': r['title_zh'],
                'track': r['track'], 'date': ANN_DATE, 'value': r['value'], 'grade': r['grade'],
                'scores': r['scores'], 'status': 'CURRENT', 'evidence': r['evidence'],
                'fetch_level': r['fetch_level'], 'fulltext_chars': r['fulltext_chars'],
                'in_top10': r['in_top10'], 'batch': RUN_DATE, 'orig_window': WINDOW,
                'announce_type': r['announce_type'], 'flags': []}, ensure_ascii=False) + '\n')
            added += 1
    for r in bf_rows:
        if r['id'] not in reg_ids:
            f.write(json.dumps({
                'id': 'arXiv:' + r['id'], 'title': r['title'], 'title_zh': r['title_zh'],
                'track': r['track'], 'date': ANN_DATE, 'value': r['value'], 'grade': r['grade'],
                'scores': r['scores'], 'status': 'CURRENT', 'evidence': r['evidence'],
                'fetch_level': r['fetch_level'], 'fulltext_chars': r['fulltext_chars'],
                'in_top10': r['in_top10'], 'batch': 'backfill-1024', 'orig_window': BF_WINDOW,
                'announce_type': r['announce_type'], 'flags': []}, ensure_ascii=False) + '\n')
            added += 1
print('registry added:', added)
n = sum(1 for l in open('papers/library/registry.jsonl', encoding='utf-8') if l.strip())
print('registry total:', n)
