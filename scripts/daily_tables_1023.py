# -*- coding: utf-8 -*-
# daily_tables_1023.py — 写两个批次的 7dim-table.md / scored.md / run_log.md
import json, datetime
ROOT = 'D:/Agent/WorkBuddy/Research'
W = ('IMP','NOV','TEC','EXP','PER','TRL','REP')

def load(f): return json.load(open(f'{ROOT}/{f}', encoding='utf-8'))

manifest = load('data/fulltext/_manifest.json')

MAIN_SC = load('data/scored_1023.json'); MAIN_POOL = {p['id']: p for p in load('data/xr_pool_2026-10-23.json')}
BF_SC = load('data/scored_backfill_1023.json'); BF_POOL = {p['id']: p for p in load('data/xr_pool_backfill_1023.json')}
T_MAIN = load('data/top10_2026-10-23.json'); T_BF = load('data/top10_backfill-1023.json')

def rows(sc, pool):
    out = []
    for p in sc['pool']:
        v = round(sum({'IMP':0.20,'NOV':0.20,'TEC':0.15,'EXP':0.15,'PER':0.15,'TRL':0.08,'REP':0.07}[k]*p[k] for k in W), 4)
        g = 'S' if v>=4.2 else ('A' if v>=3.6 else ('B' if v>=3.0 else 'C'))
        m = manifest.get(p['id'], {})
        out.append(dict(id=p['id'], tzh=p['title_zh'], track=p['track'], announce=p['announce'],
                        dims={k: p[k] for k in W}, value=v, grade=g,
                        ev=m.get('evidence','FULL'), lvl=m.get('level','L0')))
    out.sort(key=lambda x: -x['value'])
    return out

M = rows(MAIN_SC, MAIN_POOL)
B = rows(BF_SC, BF_POOL)

# ================= 主批 7 维表 =================
DAILY = f'{ROOT}/papers/daily/2026-10-23'
lines = ['# 2026-10-23 全量 7 维度对比表（参考）', '',
 '批次：2026-10-23（10-22 周四公告批次，提交日 10-15~10-21、周四 20:00 ET 释放；拉取日 10-23 周五 02:30）。',
 '候选池 15 篇（RSS 命中 33 → 去 registry(573) 后 31 新 → 剔非 XR 10 篇 + 旧稿 replace 4 篇单列 backfill + 库内 v2 再公告 2 篇剔除），全部 L0/FULL 全文后评分。',
 '评分为全文证据定稿（先抓全文再定稿）；门③ 当日最高 3.78 < 库内近 30 天 Top10 均分 4.416（现算）→ **非重磅日，无 S 级**。', '',
 '| arXiv | 标题 | 赛道 | IMP | NOV | TEC | EXP | PER | TRL | REP | 总分 | 等级 | 证据 | 公告类型 |',
 '|---|---|---|---|---|---|---|---|---|---|---|---|---|---|']
for it in M:
    lines.append(f"| {it['id']} | {it['tzh']} | {it['track']} | {' | '.join(str(it['dims'][k]) for k in W)} | {it['value']:.2f} | {it['grade']} | {it['ev']} | {it['announce']} |")
open(f'{DAILY}/7dim-table.md','w',encoding='utf-8').write('\n'.join(lines)+'\n')
print('written 7dim-table.md (15 rows)')

# ================= 主批 scored.md =================
top_ids = T_MAIN['top10']
byid = {x['id']: x for x in M}
s = ['# 2026-10-23 评分明细与覆盖率校验', '',
 '窗口：10-22（周四）公告批次（提交日 10-15~10-21；拉取日 10-23 周五）——公告日≠拉取日，非当日硬提交。', '',
 '## 一、覆盖度三关', '',
 '- 门①（同质去重，仅对比非本批文献）：最大 Jaccard **0.071**（2610.30032 vs 库内 2609.25422），< 0.62 **通过**，无同质；0.45~0.62 区间 0 篇。',
 '- 门②（赛道覆盖）：Top10 覆盖 **8 赛道**（重建与SLAM/神经渲染/感知与认知/具身交互/交互与输入/评估与数据集/世界模型与仿真/系统与平台），≥5 **通过**；全批 15 篇同覆 8 赛道。',
 '- 门③（价值天花板，校准关）：当日最高 **3.78** < 库内近 30 天 Top10 均分 **4.416**（现算：窗口 2026-09-23~10-23，444 条入窗，按 value 降序前 10：4.65/4.58/4.57/4.57/4.37/4.30/4.30/4.28/4.27/4.27）→ **非重磅日，无 S 级**，未拔高、未触发重筛。',
 '',
 '## 二、Top10 排行榜（按加权降序；同分按 IMP/NOV 降序 → 赛道多样性优先 → id 升序）', '',
 '| 排名 | arXiv | 标题 | 赛道 | 总分 | 等级 | 证据 |',
 '|---|---|---|---|---|---|---|']
for i, t in enumerate([byid[x] for x in top_ids], 1):
    s.append(f"| {i} | {t['id']} | {t['tzh']} | {t['track']} | {t['value']:.2f} | {t['grade']} | {t['ev']} |")
s += ['', '## 三、全池评分明细（15 篇）', '',
 '| arXiv | 标题 | 赛道 | IMP | NOV | TEC | EXP | PER | TRL | REP | 总分 | 等级 | Top10 | 证据 |',
 '|---|---|---|---|---|---|---|---|---|---|---|---|---|---|']
for it in M:
    s.append(f"| {it['id']} | {it['tzh']} | {it['track']} | {' | '.join(str(it['dims'][k]) for k in W)} | {it['value']:.2f} | {it['grade']} | {'✓' if it['id'] in top_ids else ''} | {it['ev']} |")
s += ['', '## 四、漏斗与甄别记录', '',
 '- 第 1 步 listing 对账：7 分类最新公告日 10-22；10-21 组 532 篇（上批已处理，复核）+ 10-22 组 402 篇全量对账；摘要级 XR 过滤（KW 全称+缩写双层）10-22 组 22 篇**全部在 RSS 集合内（0 漏网）**；10-21 组复核出 19 篇摘要级命中，其中 5 篇 XR 相关未入馆 → 单列 backfill-1023（见当日 backfill 产物）。',
 '- 数据源探针：export.arxiv.org / arxiv.org/api/query 均 200（submittedDate 前沿停滞 10-21）；RSS cs.CV 212 条（lastBuildDate 2026-10-22 04:00 UTC）→ RSS 兜底拉取。',
 '- RSS 拉取：fetch_rss.py 7 分类去重 649 → 关键词命中 33 → 去 registry(573) 后 31 新（20 new + 5 cross + 6 replace）。',
 '- 甄别：31 新中 **15 篇入 XR 池**（10 new + 3 cross + 2 replace-v2 首次入馆：2610.07217 RoboCap / 2610.25988 SSIO）；剔除非 XR 10 篇（医学体积定位 UNIVERS、雾天检测 FogTTA、无人机 AirPlayground、LLM DiffResearch/EHR 扩散、IMU 标定 A2I-Calib++、碰撞回避 RL、机械臂 NBV、假肢可供性分割）；replace 旧稿 4 篇（2604.11685/2608.21009/2604.10809/2607.06464）XR 相关 → 单列 backfill-1023；库内 v2 再公告 2 篇（2609.18898 NormLift / 2610.18950 HumanVerse）剔除。',
 '- 全文：15 篇候选全部 **L0/FULL**（41,612–130,608 字符），串行 3s/篇，无限流/降级/伪造；manifest 合并写入校验通过。',
 '- 评分：先抓全文再定稿；15 篇入馆（7 A / 6 B / 2 C），全部 CURRENT 无 OUTDATED。',
 '- backfill-1023（同日补录，单独编号）：9 篇 = 10-21 公告批次 listing 漏网 5 篇（2610.26918/27622/28004/28131/28585）+ 旧稿 replace/cross 再公告首次入馆 4 篇（2604.11685/2608.21009/2604.10809/2607.06464）；1 A / 7 B / 1 C，全部诚实标注非 10-23 当日新提交。',
 '']
open(f'{DAILY}/scored.md','w',encoding='utf-8').write('\n'.join(s)+'\n')
print('written scored.md')

# ================= 主批 run_log =================
log = ['# 2026-10-23 运行日志', '',
 f'- 运行时间：{datetime.datetime.now().strftime("%Y-%m-%d %H:%M")}（周五，拉取日）',
 '- 公告窗口：10-22（周四）公告批次；拉取日 10-23。',
 '- 数据源：export.arxiv.org / arxiv.org/api/query 探针均 200，submittedDate 前沿停滞 10-21；RSS cs.CV 212 条（公告日 10-22）→ RSS 兜底。',
 '- 第 1 步 listing 对账（audit_gap_listing.py，TARGET_LO=2026-10-21）：10-21 组 532 篇 + 10-22 组 402 篇；per-category 完整性自检 attempt1 全过（最终 per-cat SHORT 为跨分类认领统计假象）；摘要级过滤（filter_missed_xr_abstract_1021.py，914 篇池）10-22 组 22 篇全在 RSS 集合（0 漏网）；10-21 组 19 篇中 5 篇 XR 相关漏网 → backfill-1023。',
 '- 拉取：fetch_rss.py 7 分类去重 649 → KW 命中 33 → 去重后 31 新（20 new + 5 cross + 6 replace）+ 2 库内 v2。',
 '- 全文：15 主批候选全 L0/FULL；backfill 9 篇中 8 篇 L0/FULL + 1 篇 L1 PARTIAL（2610.28131 OV-Foam：ar5iv 仅返回 abs 页壳、正文不完整，按摘要级评估并显式声明）。',
 '- 三关：门① 0.071 通过；门② Top10 覆盖 8 赛道通过；门③ 3.78 < 4.416（现算）非重磅日无 S，未拔高。',
 '- registry：573 → 588（主批 +15）→ 597（backfill +9），备份 registry.jsonl.bak-20261023。',
 '- 剔除记录：非 XR 10 篇（UNIVERS 医学体积/FogTTA 雾天/AirPlayground 无人机/DiffResearch LLM/EHR 扩散/A2I-Calib++ IMU 标定/碰撞回避 RL/机械臂 NBV/假肢可供性）；replace 旧稿非 XR 2 篇（2610.24858 MRI 超分/2602.01860 无人机竞速）；库内 v2 再公告 2 篇。',
 '- 失败/降级：OV-Foam（2610.28131）L1 ar5iv 正文缺失 → PARTIAL 摘要级；其余无降级。',
 '']
open(f'{DAILY}/run_log.md','w',encoding='utf-8').write('\n'.join(log)+'\n')
print('written run_log.md')

# ================= backfill 7 维表 =================
DBF = f'{ROOT}/papers/daily/backfill-1023'
lines = ['# backfill-1023 全量 7 维度对比表（参考）', '',
 '批次：backfill-1023（**非 10-23 当日新提交**）= 10-21 公告批次 listing 漏网 5 篇 + 旧稿 replace/cross 再公告首次入馆 4 篇；拉取日 10-23。',
 '候选池 9 篇，8 篇 L0/FULL + 1 篇 L1/PARTIAL（2610.28131，ar5iv 正文缺失按摘要级评估）。',
 '门① 最大 Jaccard 0.075（<0.62 通过）；门③ 对 backfill 不适用；**无 S 级**（最高 3.65 A）。', '',
 '| arXiv | 标题 | 赛道 | IMP | NOV | TEC | EXP | PER | TRL | REP | 总分 | 等级 | 证据 | 来源 |',
 '|---|---|---|---|---|---|---|---|---|---|---|---|---|---|']
for it in B:
    src = '10-21漏网' if it['announce']=='leak-1021' else f"{it['announce']}再公告"
    lines.append(f"| {it['id']} | {it['tzh']} | {it['track']} | {' | '.join(str(it['dims'][k]) for k in W)} | {it['value']:.2f} | {it['grade']} | {it['ev']} | {src} |")
open(f'{DBF}/7dim-table.md','w',encoding='utf-8').write('\n'.join(lines)+'\n')
print('written backfill 7dim-table.md')

# ================= backfill scored.md =================
btop = T_BF['top10']; bby = {x['id']: x for x in B}
s = ['# backfill-1023 评分明细与覆盖率校验', '',
 '窗口：10-21 公告批次 listing 漏网 5 篇（公告日 10-21、提交日 10-15~10-20）+ 旧稿 replace/cross 再公告 4 篇（原始投稿 2604/2607/2608 周期，首次入馆）；拉取日 10-23。**全部非当日新提交**。', '',
 '## 一、覆盖度三关', '',
 '- 门①（同质去重，仅对比非本批文献）：最大 Jaccard **0.075**（2610.28131 vs 库内 2610.08756），< 0.62 **通过**，无同质。',
 '- 门②（赛道覆盖）：全批 9 篇覆盖 **7 赛道**（神经渲染/感知与认知/渲染与显示/世界模型与仿真/内容生成/系统与平台/评估与数据集），≥5 **通过**。',
 '- 门③（价值天花板）：对 backfill 批次不适用（校准关，参照 10-17/10-19 口径）。',
 '',
 '## 二、排名（按加权降序）', '',
 '| 排名 | arXiv | 标题 | 赛道 | 总分 | 等级 | 证据 |',
 '|---|---|---|---|---|---|---|']
for i, t in enumerate([bby[x] for x in btop], 1):
    s.append(f"| {i} | {t['id']} | {t['tzh']} | {t['track']} | {t['value']:.2f} | {t['grade']} | {t['ev']} |")
s += ['', '## 三、全池评分明细（9 篇）', '',
 '| arXiv | 标题 | 赛道 | IMP | NOV | TEC | EXP | PER | TRL | REP | 总分 | 等级 | 来源 |',
 '|---|---|---|---|---|---|---|---|---|---|---|---|---|']
for it in B:
    src = '10-21漏网' if it['announce']=='leak-1021' else f"{it['announce']}再公告"
    s.append(f"| {it['id']} | {it['tzh']} | {it['track']} | {' | '.join(str(it['dims'][k]) for k in W)} | {it['value']:.2f} | {it['grade']} | {src} |")
s += ['', '## 四、甄别记录', '',
 '- 来源一（listing 漏网，10-21 公告批次）：10-22 运行的摘要级过滤复核出 19 篇命中，甄别 5 篇 XR 相关（GTSM 热场 3DGS / UMI 手套 / 编码孔径相机 / OV-Foam / SceneRig）；其余 14 篇非 XR（视频时序定位、无人机定位、动物行为、人机协作、LLM 智能体记忆、知识编辑、ObjectNav、低比特 LLM、dashcam 车道、人形接触重定向、CoGaussian 自动驾驶协同感知（尊重 10-22 运行剔除判断）、流式语言模型、室内探索、SIFT 类匹配）。',
 '- 来源二（RSS 旧稿 replace/cross 再公告，首次入馆）：2604.11685 Unfolding 3DGS（3DGS LOD）/ 2608.21009 手背 XR 年龄保障 / 2604.10809 WARPED 手腕渲染 / 2607.06464 Hilti 360 VIO 基准；同批非 XR 旧稿剔除（2610.24858 MRI 超分 / 2602.01860 无人机竞速 / 2602.11321 人形遥操作）。',
 '- 全文：9 篇中 8 篇 L0/FULL（29,750–139,019 字符）；2610.28131 OV-Foam L1 ar5iv 仅返 abs 页壳（4,552 字符导航文本）→ **PARTIAL，按摘要级评估并显式声明**，禁止脑补正文。',
 '- 评分：先抓全文再定稿；9 篇入馆（1 A / 7 B / 1 C），全部 CURRENT 无 OUTDATED。',
 '- 覆盖补强：3DGS 紧凑渐进渲染第三条 LOD 路线（Unfolding 3DGS）、XR 年龄保障新模态（手背）、光学-感知联合可微设计（编码孔径+3DGS）、单图仿真就绪场景（SceneRig）、无电子 UMI 采集、热动力学 4DGS、幂图特征提升、360 VIO 基准。',
 '']
open(f'{DBF}/scored.md','w',encoding='utf-8').write('\n'.join(s)+'\n')
print('written backfill scored.md')

# ================= backfill run_log =================
log = ['# backfill-1023 运行日志', '',
 f'- 运行时间：{datetime.datetime.now().strftime("%Y-%m-%d %H:%M")}（周五，与 10-23 主批同日补录）',
 '- 性质：backfill（listing 漏网 5 篇 + 旧稿 replace 再公告 4 篇），**非 10-23 当日新提交**；批次单独编号 backfill-1023。',
 '- 来源：① 10-22 运行 listing 对账的 10-21 组摘要级过滤漏网（5 篇 XR 相关）；② 10-23 RSS 拉取混入的旧稿 replace/cross（4 篇 XR 相关，首次入馆）。',
 '- 全文：8 篇 L0/FULL + 1 篇 L1/PARTIAL（2610.28131 OV-Foam ar5iv 正文缺失）。',
 '- 三关：门① 0.075 通过；门② 7 赛道通过；门③ 不适用。',
 '- registry：588 → 597（+9），in_top10 校正 0 处。',
 '- 失败/降级：OV-Foam PARTIAL（摘要级评估，已显式声明）。',
 '']
open(f'{DBF}/run_log.md','w',encoding='utf-8').write('\n'.join(log)+'\n')
print('written backfill run_log.md')
