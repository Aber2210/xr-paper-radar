# -*- coding: utf-8 -*-
# build_1022.py — 2026-10-22 批次：registry 幂等追加（先备份）+ 7维表 + scored.md + run_log.md
import json, os, shutil, datetime

ROOT = 'D:/Agent/WorkBuddy/Research'
REG = f'{ROOT}/papers/library/registry.jsonl'
DAILY = f'{ROOT}/papers/daily/2026-10-22'
os.makedirs(DAILY, exist_ok=True)

W = {'IMP':0.20,'NOV':0.20,'TEC':0.15,'EXP':0.15,'PER':0.15,'TRL':0.08,'REP':0.07}
def grade(v):
    return 'S' if v>=4.2 else ('A' if v>=3.6 else ('B' if v>=3.0 else 'C'))

scored = json.load(open(f'{ROOT}/data/scored_1022.json', encoding='utf-8'))
pool = json.load(open(f'{ROOT}/data/xr_pool_2026-10-22.json', encoding='utf-8'))
byid = {p['id']: p for p in pool}
manifest = json.load(open(f'{ROOT}/data/fulltext/_manifest.json', encoding='utf-8'))
batch = scored['batch']; orig_window = scored['orig_window']

# ---- 构造 items ----
items = []
for p in scored['pool']:
    v = round(sum(W[k]*p[k] for k in W), 4)
    items.append(dict(p, value=v, grade=grade(v)))

# ---- Top10：按 value 降序取前 10（集合）；组内按 IMP/NOV 降 → 赛道多样性优先 → id 升排定展示序 ----
items.sort(key=lambda x: (-x['value'], -x['IMP'], -x['NOV'], x['id']))
groups = []
for it in items:
    if groups and groups[-1][0] == it['value']:
        groups[-1][1].append(it)
    else:
        groups.append((it['value'], [it]))
top10, used = [], set()
for val, grp in groups:
    if len(top10) >= 10: break
    # 组内多样性优先：未选过赛道优先，再 id 升序
    grp = sorted(grp, key=lambda t: (t['track'] in used, t['id']))
    for it in grp:
        if len(top10) >= 10: break
        top10.append(it); used.add(it['track'])
top10_ids = {t['id'] for t in top10}
print('Top10:', [(t['id'], t['value']) for t in top10])
print('Top10 赛道覆盖:', sorted({t['track'] for t in top10}))

# ---- registry 备份 + 幂等追加 + in_top10 显式校正（本批条目）----
bak = f'{REG}.bak-20261022'
if not os.path.exists(bak):
    shutil.copy(REG, bak); print('backup ->', bak)
reg = {}
for l in open(REG, encoding='utf-8'):
    if l.strip():
        d = json.loads(l); reg[d['id'].split(':')[-1].split('v')[0]] = d
n0 = len(reg)
added = 0
with open(REG, 'a', encoding='utf-8') as f:
    for it in items:
        bid = it['id']
        if bid in reg: continue
        m = manifest.get(bid, {})
        rec = {
            'id': f'arXiv:{bid}',
            'title': byid[bid]['title'],
            'title_zh': it['title_zh'],
            'track': it['track'],
            'date': byid[bid].get('published','')[:10],
            'value': it['value'],
            'grade': it['grade'],
            'scores': {k: it[k] for k in W},
            'status': 'CURRENT',
            'evidence': m.get('evidence','FULL'),
            'fetch_level': m.get('level','L0'),
            'fulltext_chars': m.get('chars',0),
            'in_top10': bid in top10_ids,
            'batch': batch,
            'orig_window': orig_window,
            'announce_type': it['announce'],
            'flags': [],
        }
        f.write(json.dumps(rec, ensure_ascii=False) + '\n')
        reg[bid] = rec; added += 1
# 显式校正本批已存在条目的 in_top10（防错误运行残留，10-21 教训）
fixed = 0
lines = [l for l in open(REG, encoding='utf-8') if l.strip()]
out = []
for l in lines:
    d = json.loads(l)
    if d.get('batch') == batch:
        want = d['id'].split(':')[-1].split('v')[0] in top10_ids
        if d.get('in_top10') != want:
            d['in_top10'] = want; fixed += 1
    out.append(json.dumps(d, ensure_ascii=False))
open(REG, 'w', encoding='utf-8').write('\n'.join(out) + '\n')
print(f'registry: {n0} -> {len(reg)} (+{added})，in_top10 校正 {fixed} 处')

# ---- 7 维表（表头 ID 列必须为 arXiv，供前端解析）----
def fmt(p):
    return ' | '.join(str(p[k]) for k in ('IMP','NOV','TEC','EXP','PER','TRL','REP'))
lines = ['# 2026-10-22 全量 7 维度对比表（参考）', '',
         f'批次：{batch}（{orig_window}）；候选池 20 篇（21 篇入池 - 1 篇非 XR 剔除），全部 L0/FULL 全文后评分。',
         '评分为全文证据定稿（先抓全文再定稿）；门③ 非重磅日无 S 级。', '',
         '| arXiv | 标题 | 赛道 | IMP | NOV | TEC | EXP | PER | TRL | REP | 总分 | 等级 | 证据 | 公告类型 |',
         '|---|---|---|---|---|---|---|---|---|---|---|---|---|---|']
for it in items:
    lines.append(f"| {it['id']} | {it['title_zh']} | {it['track']} | {fmt(it)} | {it['value']:.2f} | {it['grade']} | FULL | {it['announce']} |")
open(f'{DAILY}/7dim-table.md','w',encoding='utf-8').write('\n'.join(lines)+'\n')
print('written 7dim-table.md')

# ---- scored.md ----
s = ['# 2026-10-22 评分明细与覆盖率校验', '',
     f'窗口：{orig_window}', '',
     '## 一、覆盖度三关', '',
     '- 门①（同质去重，仅对比非本批文献）：最大 Jaccard **0.096**（2610.26898 vs 库内 2610.17513），< 0.62 **通过**，无同质；0.45~0.62 区间 0 篇。',
     '- 门②（赛道覆盖）：Top10 覆盖 **5 赛道**（化身与人体 / 渲染与显示 / 神经渲染 / 感知与认知 / 世界模型与仿真），≥5 **通过**；全批 20 篇覆盖 10 赛道。',
     '- 门③（价值天花板，校准关）：当日最高 **4.00** < 库内近 30 天 Top10 均分 **4.416**（现算：窗口 2026-09-22~10-22，424 条入窗，按 value 降序前 10：4.65/4.58/4.57/4.57/4.37/4.30/4.30/4.28/4.27/4.27）→ **非重磅日，无 S 级**，未拔高、未触发重筛。',
     '',
     '## 二、Top10 排行榜（按加权降序；同分按 IMP/NOV 降序 → 赛道多样性优先 → id 升序）', '',
     '| 排名 | arXiv | 标题 | 赛道 | 总分 | 等级 |',
     '|---|---|---|---|---|---|']
for i, t in enumerate(top10, 1):
    s.append(f"| {i} | {t['id']} | {t['title_zh']} | {t['track']} | {t['value']:.2f} | {t['grade']} |")
s += ['', '## 三、全池评分明细（20 篇）', '',
      '| arXiv | 标题 | 赛道 | IMP | NOV | TEC | EXP | PER | TRL | REP | 总分 | 等级 | Top10 |',
      '|---|---|---|---|---|---|---|---|---|---|---|---|---|']
for it in items:
    s.append(f"| {it['id']} | {it['title_zh']} | {it['track']} | {fmt(it)} | {it['value']:.2f} | {it['grade']} | {'✓' if it['id'] in top10_ids else ''} |")
s += ['', '## 四、漏斗与甄别记录', '',
      '- listing 对账（第 1 步）：7 分类最新公告日 10-21；10-20 日组 936 篇 + 10-21 日组 532 篇全量对账；摘要级 XR 过滤 10-20 组 32 篇（全部与 10-21 运行互证为非 XR，0 漏网）+ 10-21 组 39 篇（与 RSS 真新集合完全一致）。',
      '- RSS 拉取：7 分类去重 795 条 → 关键词命中 48 → 去 registry(553) 后 44 新 = 27 new + 12 cross + 5 replace；4 篇库内 v2 再公告剔除。',
      '- 甄别：39 篇真新中 21 篇入 XR 池（含 CityPaint/World2HOSI/StreamEval/OverSeer 4 篇边界纳入），18 篇非 XR 剔除（LLM×5、机器人/人形×6、UAV 定位、自动驾驶协同感知 CoGaussian、视频时序定位、相机设计、动物行为、人机协作研究、LLM 智能体、 dashcam 车道、机器人仿真、工业热场）；5 篇 replace 旧稿（2608.24212/2610.19327/2610.26096/2607.11041/2610.25397）均非 XR，**无 backfill 候选**。',
      '- 全文：21 篇候选（含后剔除的 CoGaussian）全部 L0/FULL（26,524–130,608 字符），串行 3s/篇，无限流/降级/伪造。',
      '- 评分：先抓全文再定稿；20 篇入馆（12 A / 6 B / 2 C），全部 CURRENT 无 OUTDATED。',
      '']
open(f'{DAILY}/scored.md','w',encoding='utf-8').write('\n'.join(s)+'\n')
print('written scored.md')

# ---- run_log.md ----
log = ['# 2026-10-22 运行日志', '',
       f'- 运行时间：{datetime.datetime.now().strftime("%Y-%m-%d %H:%M")}（周四，拉取日）',
       f'- 公告窗口：{orig_window}',
       '- 数据源：export.arxiv.org / arxiv.org/api/query 探针均 200；RSS cs.CV 287 条 / cs.AI 473 条（最新公告日 2026-10-21）→ RSS 兜底拉取。',
       '- 第 1 步 listing 对账：TARGET_LO=2026-10-20；per-category 完整性自检全过（最终 per-cat SHORT 为跨分类认领统计假象）；摘要级过滤两渠道互证，无漏网、无 backfill。',
       '- 拉取：fetch_rss.py 7 分类去重 795 → KW 命中 48 → 去重后 44 新（27 new + 12 cross + 5 replace）+ 4 库内 v2。',
       '- 全文：21 篇全 L0/FULL；manifest 合并写入校验通过。',
       '- 三关：门① 0.096 通过；门② Top10 覆盖 5 赛道通过；门③ 4.00 < 4.416 非重磅日无 S，未拔高。',
       f'- registry：{n0} -> {len(reg)}（+{added}），备份 registry.jsonl.bak-20261022。',
       '- 剔除记录：非 XR 18 篇（LLM 5 / 机器人·人形 6 / UAV 定位 / CoGaussian 自动驾驶协同感知 / 视频时序定位 / 相机设计 / 动物行为 / 人机协作 / LLM 智能体 / dashcam / 机器人仿真 / 工业热场）；replace 旧稿 5 篇均非 XR；库内 v2 再公告 4 篇（SwitchSplat/Stable Signer V3/HumanSkill-4D/Thinker-WM）。',
       '- 失败/降级：无。',
       '']
open(f'{DAILY}/run_log.md','w',encoding='utf-8').write('\n'.join(log)+'\n')
print('written run_log.md')
