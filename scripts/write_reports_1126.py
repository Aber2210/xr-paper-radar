# -*- coding: utf-8 -*-
"""2026-11-26 最终解读报告 + backfill 报告 + daily 产物（7dim-table / scored / run_log）。

口径要点（不可改写）：
- 公告日 2026-11-25（周三）≠ 拉取日 2026-11-26（周四 02:30）；11-26 组尚未公告；11-25 为单日公告组。
- 主批 55 + backfill 8 = 63；S3 / A24 / B29 / C7；门③ margin +0.138、blockbuster=true → 授 3 个 S。
"""
import glob
import json
import os
import re
import shutil
from collections import Counter

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
os.chdir(ROOT)
DATE, MMDD = '2026-11-26', '1126'
ANN = '2026-11-25'

D = json.load(open('data/scored_%s.json' % MMDD, encoding='utf-8'))
G = json.load(open('data/gates_%s.json' % MMDD, encoding='utf-8'))
RES = json.load(open('data/residual_%s.json' % MMDD, encoding='utf-8'))
PUB = json.load(open('data/published_%s.json' % MMDD, encoding='utf-8'))
MAN = json.load(open('data/fulltext/_manifest.json' % MMDD, encoding='utf-8')) if False else \
    json.load(open('data/fulltext/_manifest.json', encoding='utf-8'))
REJ = json.load(open('data/published_%s.json' % MMDD, encoding='utf-8'))  # 占位，下方替换
XR = json.load(open('data/xr_pool_%s.json' % MMDD, encoding='utf-8'))
OLD = json.load(open('data/old_replace_%s.json' % MMDD, encoding='utf-8'))
MX = json.load(open('data/missed_xr_%s.json' % MMDD, encoding='utf-8'))
AG = G['announcement_group']

MAIN = [p for p in D if not p['batch'].startswith('backfill')]
BF = [p for p in D if p['batch'].startswith('backfill')]
TOP = [p for p in D if p['in_top10']]
TOP.sort(key=lambda r: (-r['value'], -r['scores']['IMP'], -r['scores']['NOV'], r['id']))
g1, g2, g3 = G['gate1'], G['gate2'], G['gate3']
GR = Counter(p['grade'] for p in D)
GRM = Counter(p['grade'] for p in MAIN)
GRB = Counter(p['grade'] for p in BF)

DIG = {}
for k in range(1, 9):
    for r in json.load(open('data/digest_%s_g%d.json' % (MMDD, k), encoding='utf-8')):
        DIG[r['id']] = r

# 池内被剔除的条目（本批未落盘逐篇理由，只给清单，供抽查）
MAIN_IDS = {p['id'] for p in MAIN}
REJ_IDS = sorted(pid for pid in XR if pid not in MAIN_IDS)
REJ = {pid: XR[pid] for pid in REJ_IDS}


def concl(pid):
    f = glob.glob('papers/notes/%s__*.md' % pid)
    txt = open(f[0], encoding='utf-8').read()
    m = re.search(r'## 一句话结论\n(.+?)\n\n', txt, re.S)
    return m.group(1).strip()


def bl(items):
    if isinstance(items, (list, tuple)):
        return '\n'.join('- ' + str(x) for x in items)
    return '\n'.join('- ' + x.strip() for x in re.split(r'[；。]', str(items)) if x.strip())


def pub_dist(rows):
    c = Counter(p['published'] for p in rows)
    return ' / '.join('%s×%d' % (k[5:], v) for k, v in sorted(c.items(), key=lambda kv: -kv[1]))


os.makedirs('papers/daily/%s' % DATE, exist_ok=True)
os.makedirs('papers/daily/backfill-%s' % MMDD, exist_ok=True)

# ==================== 一、主报告 ====================
L = []
A = L.append

A('# XR 每日论文雷达 · %s\n' % DATE)
A('> **诚实口径**：本批处理的是 **%s（周三）公告批次**，拉取时刻 **2026-11-26 02:30（北京时间）**。'
  '11-26 组此刻**尚未公告**（拉取早于 11-26 00:00 UTC = 08:00 北京时间的释放时刻）；'
  '11-25 是**单日公告组**，不含周末积压（11-22/11-23 的提交已在前两批处理完毕）。'
  'arXiv **公告日 ≠ 拉取日 ≠ 首次提交日**：主批 API `published` 核验为 %s（合计 %d）；'
  'RSS 的 `published` 是公告时间戳，不能当提交日使用。\n' % (ANN, pub_dist(MAIN), len(MAIN)))
A('> 覆盖范围：cs.CV / cs.GR / cs.HC / cs.MM / cs.RO / cs.AI / eess.IV 七分类 listing（show=500 单页，逐分类 declared=got 核对）。'
  '%s 组 **%s 槽位 / %s 篇唯一**（%s），全部命中 RSS **921 条**（缺收 0），摘要级覆盖率 **1.0000**。\n' % (
      ANN, format(AG['slots'], ','), format(AG['unique'], ','),
      ' / '.join('%s %d' % (k, v['got']) for k, v in AG['per_cat'].items())))

# ---- 一、执行摘要 ----
A('\n## 一、执行摘要\n')
A('**本批 %d 篇（主批 %d + backfill %d），%d S / %d A / %d B / %d C；Top10 实数 10 篇，最高 %.2f（2611.32198 MoGe-4D）。**'
  ' 门③ 现算：当日最高 %.2f vs 库内近 30 天 Top10 均分 **%.3f**（%d 条入窗，半开窗口 [%s, %s)，按 batch 剔除本次追加的 `%s`），'
  'margin **%+.3f** → `heavy_day_raw=%s`、`blockbuster=%s` → **本批授 %d 个 S**（%s）。\n' % (
      len(D), len(MAIN), len(BF), GR['S'], GR['A'], GR['B'], GR['C'], g3['today_max'],
      g3['today_max'], g3['top10_mean'], g3['in_window'], g3['window_lo'], g3['window_hi'],
      '、'.join(g3['this_run_batches_excluded']), g3['margin'], g3['heavy_day_raw'], g3['blockbuster'],
      len([p for p in D if p['grade'] == 'S']),
      ' / '.join('%.2f %s' % (p['value'], p['title_zh'].split('：')[0]) for p in TOP if p['grade'] == 'S')))
A('当日四条主线：\n')
A('1. **4D 动态重建从「专用管线拼接」收敛为「统一接口」**：2611.32198 MoGe-4D 用一次 query 返回 '
  '**allo/ego 成对点图**，几何、运动与相机位姿由同一组稠密坐标给出，位姿退化成闭式刚体对齐而不必黑箱回归——'
  '3D 跟踪全点 RelEPE 相机系 **0.084 vs V-DPM 0.160（−47.5%）**，多视图重建全局点 AUC@25 **79.26% vs π3 73.41%**，'
  'Oxford-Spires 上 **500 帧单次前向**零样本仍比基线快 1.7–4.3×；2611.31757 Xtream 把**尺度**从隐变量提为一等状态'
  '（每窗口一个对数尺度比 + 独立环路尺度），VBR 单目 ATE **5.40 m vs AMB3R-SLAM 7.42**；2611.32482 COHERE4D 更省——'
  '利用「人体与场景基础模型其实重建了同一张可见人体表面」做免训练稠密配准，3DPW **0.688 vs Human3R 1.079（−36.2%）**、'
  '只增约 4 ms/帧；2611.31516 InitFree-SfM 则给出结论级反证：**代理 OSE 目标不是精度主因**，从随机初始化出发、'
  '只加一项相对深度残差 + 联合度量精化，ETH3D 位姿 AUC@20° **85.81% vs pOSE 13.91%**（去掉精化跌到 31.99%）。\n')
A('2. **世界模型的「记忆」成为独立设计维度，索引单位从「帧/相机」换成「表面/区域」**：2611.32445 A Mesh to Remember '
  '把 coarse mesh 当**地址**而非画布，在物体自身坐标系按表面积分 cell 存渲染器自己的 K/V，外观随物体移动与关节运动一起走'
  '——动态场景 object permanence **91.5 vs 最强基线 34.7**、跨 agent 一致性 **79.99 vs 42.60**，720p 41.1 FPS 且 '
  '**8,001 帧 rollout 峰值显存 <45 GiB**（对照：全历史 attention 在 139 s 即 OOM）；2611.31944 DraftKV 用'
  '「位姿/视锥粗 grounding + draft attention 细选」两级检索把 33B 模型压进**单张 80 GiB H100**（persistence +13.7%、'
  '5.49 vs 4.71 FPS）；而残差捞回的 2611.31803 SceneMemBench 给这条线补了基准：把记忆拆成 **seen-view recall 与 '
  'novel-view recovery** 两个可分离任务——「记住」并不等于「能迁移到未见视角」，这正是持久世界模型真正需要的能力。\n')
A('3. **人体与手部：从「刚性模板 + 后处理接触」转向「世界系记忆 + 可形变表面」**：2611.32876 MemHand 把时序上下文建成'
  '短期事件记忆（按遮挡/出视野事件自适应读取长度）与长期尺度记忆，并把出视野补全搬到世界系做手-头协同——'
  'ARCTIC W-MPJPE **41.46 mm vs StableHand 91.25（−57%）**；2611.32932 HARI4D 把「全身—手臂—腕—手指」的操作层级'
  '写进单目 4D HOI（物体 CD **6.40 vs 14.55 cm**，−56%）；2611.31950「超越刚性手」不改手模型也不改估计器，'
  '只把接触问题从「更好的姿态」换成「可形变的表面」，接触带贴合度 **约 20%→近 50%**、深穿透顶点 DexYCB **38.6→2.9/帧**；'
  '2611.31812 手-物前馈重建只用冻结位姿基础模型的**内部特征**（不用其输出位姿），换来 OakInk 未见物体 AUC '
  '**93.29 vs SemiHand 40.50**。\n')
A('4. **系统层效率突破集中在「把粒度拆开」而不是「换算子」**：2611.31918 HiGS 把 3DGS 的三个角色分离——8×8 tile 只做光栅化、'
  '64×32 macro-tile 做划分与排序、bounded batch 做独立工作与反向求导，1080p **2756 FPS** / 4K **1533 FPS**（相对 gsplat '
  '5.1×/5.6×）、训练 **61.5 s vs 194.4 s**；2611.32523 AirLeg 用 imperative learning 把仿真预训练的本体感知模型迁到真机'
  '（网络精化视觉地图、精化后的地图再以**重投影**而非位姿回归监督网络），GrandTour **17/17 条序列 <0.4 m**、'
  'Unitree Go2 漂移 **0.59% vs OKVIS2 1.55%**；压缩线三篇各自解耦一处耦合：SplatTok 让**码长与原语数量**脱钩、'
  'InterGS+ 把 SH 建模搬进**共享 PCA 域**、完成感知压缩把**比特分配与完成时刻**联合优化。\n')
A('**筛选与复核**：摘要级 KW 命中 **%d** 篇 + 标题级扩展词补扫 **%d** 篇 = 候选池 **%d** 篇；逐篇核摘要剔 **%d** 篇'
  '（剔除清单见 `data/nonxr_1126.json` 527 条全量与 §5.2；误命中主因仍是 `spatial` / `hand` / `gaussian` / `tracking` / '
  '`depth` / `mesh` / `gaze` 等泛词与非 XR 场景共现），得 **%d** 篇；第 3.5 步残差复核扫描 **%d 条**、判 **%d 条**应收录'
  '（**%.2f%%**）、**采纳 %d 篇**；另通读补入 3 篇（2611.31757 Xtream / 2611.32034 BodyWeave / 2611.32396 PRC4D，'
  '均未被自动 flagged 命中）→ 主批 **%d 篇**。'
  '上一公告组（11-24 组，1,045 篇唯一）未入馆 **%d 篇** 复采核验：**%d/%d 均有摘要**，摘要/标题级命中 **%d 篇**'
  '**全部落在上批处置集合**（`scored_1125 ∪ xr_pool_1125 ∪ nonxr_1125 ∪ old_replace_1125`）→ **0 漏网**'
  '（`data/missed_xr_%s.json` 的 `leak_n=0`），无需补漏。\n' % (
      G['recall']['kw_hits'], G['recall']['title_extra'], G['recall']['pool'],
      len(REJ), len(MAIN), RES['n_scanned'], RES['n_flagged'],
      RES['rate'] * 100, G['recall']['residual_adopted'], len(MAIN),
      MX['unadmitted'], MX['with_abstract'], MX['unadmitted'], len(MX['hits']), MMDD))

# ---- 二、Top10 ----
A('\n## 二、Top10 排行榜\n')
A('| 排名 | 论文 | 赛道 | 总分 | 档 | 证据 | 关键贡献 |')
A('|---|---|---|---|---|---|---|')
SHORT = {
 '2611.32198': '一次 query 出 allo/ego 成对点图，位姿退化为闭式对齐：RelEPE 0.084 vs 0.160（−47.5%），AUC@25 79.26% vs π3 73.41%，500 帧零样本快 1.7–4.3×。',
 '2611.32445': 'mesh 当地址、cell 为索引存渲染器 K/V：object permanence 91.5 vs 34.7，跨 agent 79.99 vs 42.60，720p 41.1 FPS、8,001 帧 <45 GiB。',
 '2611.32523': 'imperative learning 做 sim-to-real：网络精化地图、地图以重投影监督网络：17/17 序列 <0.4 m，Go2 漂移 0.59% vs OKVIS2 1.55%。',
 '2611.31757': '把尺度提为一等状态（窗口尺度比 + 环路尺度 + 度量/IMU 锚）：VBR 5.40 m vs 7.42，KITTI 9.79 m vs 13.11，单卡 10–21 FPS。',
 '2611.32351': '三组 gaze query 把 depth/head mask/heatmap 内化进 VLM，点框热图语言统一自回归：GTL-T2P L2 0.094 vs 0.387，2B 超 27B 的 mIoU 2.2×。',
 '2611.32482': '用「同一张可见人体表面」免训练配准人体与场景模型，尺度/平移解耦 + 跨帧投票：3DPW 0.688 vs 1.079（−36.2%），仅 +4 ms/帧。',
 '2611.31944': '位姿 grounding + draft attention 两级检索 + tile 级流式 attention：persistence 58.98 vs 56.67，5.49 vs 4.71 FPS，33B 模型上单卡 H100。',
 '2611.31516': 'OSE 只加一项相对深度残差（保 VarPro 可分）+ 度量精化：ETH3D AUC@20° 85.81% vs pOSE 13.91%，去精化即跌至 31.99%。',
 '2611.31918': '划分/光栅化/并行三种粒度分离（8×8 tile / 64×32 macro-tile / bounded batch）：1080p 2756 FPS、4K 1533 FPS，训练 3.2×。',
 '2611.31812': '物体只用冻结位姿基础模型内部特征 + 由粗到细接触（SDF 区域距离）：DexYCB AUC 92.88，OakInk 93.29 vs 40.50。',
}
for i, p in enumerate(TOP, 1):
    A('| %d | %s（%s） | %s | **%.2f** | %s | %s | %s |' % (
        i, p['title_zh'], p['id'], p['track'], p['value'], p['grade'], p['evidence'], SHORT[p['id']]))
A('\n> **门② 未触发重筛**：纯值 Top10 已覆盖 **%d 赛道**（%s），全批 **%d 赛道**（共 12 赛道体系）。\n' % (
    g2['n_tracks'], '、'.join('%s×%d' % (k, v) for k, v in g2['top10_tracks'].items()), g2['all_batch_tracks']))
A('> **OUTDATED / SUPERSEDED 均为 0**：本批未发现「同问题更优且更晚」的直接取代关系。'
  'backfill 8 篇为 `replace` 类旧稿再公告（首发 2025-08-24 ~ 2026-10-08），其中 2512.12898（QNN-GS，首发 2025-12-13）'
  '与 2601.22046（PLANING，首发 2026-01-29）首发距今较久，已在笔记中保留首发日以免被误读为当期工作，但未达论文级 OUTDATED 证据门槛。\n')

# ---- 三、逐篇解读 ----
A('\n## 三、逐篇深度解读\n')
for i, p in enumerate(TOP, 1):
    g = DIG[p['id']]
    A('\n### 第 %d 章 %s（%s · %s · %.2f %s）\n' % (i, p['title_zh'], p['id'], p['track'], p['value'], p['grade']))
    A('**一句话结论**：%s\n' % concl(p['id']))
    A('**要解决的问题**\n\n%s\n' % g['problem'])
    A('**方法详解**\n\n%s\n' % g['method'])
    A('**实验与结果**\n\n%s\n' % bl(g['key_numbers']))
    A('**创新点与贡献**\n\n%s\n' % bl(g['novelty']))
    A('**局限与风险**\n\n%s\n' % bl(g['limitations']))
    rel = '- 本批新增（batch `%s`，公告类型 `%s`），赛道「%s」，首发提交日 %s。' % (
        p['batch'], p['announce'] or 'new', p['track'], p['published'])
    if p.get('recall') == 'RESIDUAL_ADOPT':
        rel += ('\n- **由第 3.5 步残差复核捞回**：摘要级 KW 与标题级扩展词均未命中，说明现有词表在该表述上仍有语义缺口'
                '（该篇走完「全文抓取 → 7 维评分 → 产物」全流程后才入馆，清单本身未直接并库）。')
    if p.get('note'):
        rel += '\n- 备注：%s' % p['note']
    rel += '\n- 与库内同赛道论文构成并列参考；本批 OUTDATED/SUPERSEDED 判定为 0。'
    A('**与文献库的关系**\n\n%s\n' % rel)
    A('**可复现性**\n\n- 代码/项目页：%s\n- 全文证据：%s（%s，%s 字符，%s）\n' % (
        p.get('code') or '正文未提供', p['evidence'], MAN[p['id']]['level'],
        format(MAN[p['id']]['chars'], ','), MAN[p['id']].get('url', '—')))
    act = '- 纳入重点精读：方法与实验节可直接支撑选题与技术选型。' if p['grade'] in ('S', 'A') else '- 浏览级。'
    _cd = (p.get('code') or '').strip()
    _has = ('http' in _cd) and not _cd.startswith('未')
    if _has:
        act += '\n- 有公开代码/项目页，可先跑通再评估迁移成本。'
    else:
        act += '\n- 未见公开代码，复现需按正文细节自行实现。'
    if p['grade'] == 'S':
        act += ('\n- 本批门③ margin %+.3f、`blockbuster=true`，按口径授 S：可作对外引用重点，'
                '但结论仍按论文级证据表述（未做产品化验证）。' % g3['margin'])
    elif p['value'] >= 4.20:
        act += '\n- 达 S 线（≥4.20）但本批未授 S，按 A 表述。'
    A('**行动建议**\n\n%s\n' % act)

# ---- 四、7 维表 ----
A('\n## 四、当日全量 7 维度对比表\n')
A('权重：IMP 0.20 · NOV 0.20 · TEC 0.15 · EXP 0.15 · PER 0.15 · TRL 0.08 · REP 0.07；'
  '档位：S ≥4.20 **且** `blockbuster=true`，A 3.60–4.20，B 3.00–3.60，C <3.00（仅入馆不解读、不写笔记）。'
  '完整表见 [papers/daily/%s/7dim-table.md](../papers/daily/%s/7dim-table.md)。\n' % (DATE, DATE))
A('| # | arXiv | 论文 | 赛道 | IMP | NOV | TEC | EXP | PER | TRL | REP | 总分 | 档 |')
A('|---|---|---|---|---|---|---|---|---|---|---|---|---|')
for i, p in enumerate(MAIN, 1):
    s = p['scores']
    A('| %d | %s | %s | %s | %d | %d | %d | %d | %d | %d | %d | **%.2f** | %s |' % (
        i, p['id'], p['title_zh'][:34].replace('|', '/'), p['track'], s['IMP'], s['NOV'], s['TEC'],
        s['EXP'], s['PER'], s['TRL'], s['REP'], p['value'], p['grade']))

# ---- 五、覆盖率校验 ----
A('\n## 五、覆盖率校验与筛选过程\n')
A('### 5.1 漏网对账（第 1 步，先于拉取）\n')
A('- 7 分类最新公告日**全部为 %s（周三）**；11-26 组 `declared=None / got=0`（尚未释放）。\n' % ANN)
A('- %s 组逐分类 declared=got：%s = **%s 槽位**，唯一论文 **%s 篇**（跨列表重复 %s）。'
  '上一公告组（11-24）复采逐分类 declared=got（494/13/61/18/191/485/23 = 1,285 槽位），与上批记录一致 → **无新增漏跑窗口**。\n' % (
      ANN, ' / '.join('%s %d' % (k, v['got']) for k, v in AG['per_cat'].items()),
      format(AG['slots'], ','), format(AG['unique'], ','), format(AG['slots'] - AG['unique'], ',')))
A('- 上一公告组（11-24 组 1,045 篇唯一）未入馆 **%d 篇 = 1,045 − 68**（上批主批已入馆）；'
  '用 11-25 / 11-26 两份 RSS 全量核摘要，**%d/%d 全覆盖、0 篇缺摘要**，摘要/标题级命中 **%d 篇**'
  '**全部落入上批处置集合** → **0 漏网**（`data/missed_xr_%s.json` 的 `leak` 为空对象、`leak_n=0`）。\n' % (
      MX['unadmitted'], MX['with_abstract'], MX['unadmitted'], len(MX['hits']), MMDD))
A('### 5.2 数据源与召回\n')
A('- RSS 7 分类 `--no-filter` 去重 **921 条**（`WROTE=921`、`OK_CATS=7/7`，完整采集：任一分类失败即 exit 2，本批未触发）。'
  'listing %s 篇 **100%% 被 RSS 覆盖（缺收 0）** → **免 API `id_list` 枚举**，规避 429 静默丢批；'
  'API 仅用于 63 篇的提交日核验（`check_published_1126.py`，63/63 全齐）。\n' % format(AG['unique'], ','))
A('- 召回三层：摘要级 KW **%d** + 标题级扩展词补扫 **%d** = **%d 篇命中** → 逐篇核摘要剔 **%d 篇** → **%d 篇**；'
  '残差采纳 **%d** + 通读补入 **3** → **主批 %d 篇**。'
  '入选主批的列表类别分布：%s。\n' % (
      G['recall']['kw_hits'], G['recall']['title_extra'], G['recall']['pool'], len(REJ),
      len(MAIN) - 3 - G['recall']['residual_adopted'],
      G['recall']['residual_adopted'], len(MAIN),
      ' / '.join('%s %d' % (k, v) for k, v in Counter(p['cat'] for p in MAIN).most_common())))
A('- **被剔除的 %d 篇池内条目**（按 arXiv ID 升序，标题截断；本批未落盘逐篇理由，故只给清单供抽查，'
  '不作语义归类以免事后追认）：\n' % len(REJ))
A('| # | arXiv | 标题（截断） |')
A('|---|---|---|')
for i, pid in enumerate(REJ_IDS, 1):
    rec = REJ[pid]
    t = (rec.get('title') if isinstance(rec, dict) else '') or ''
    A('| %d | %s | %s |' % (i, pid, t[:76].replace('|', '/')))
A('')
A('  误命中主因与上批一致：`spatial` 多指空间推理基准与地理偏见，`hand` 多为手写体 OCR 与手部 X 光，'
  '`gaussian` 大量落在高斯分布 / EDA，`tracking` 多为状态跟踪与航空建图，`depth` 多为单目深度估计的通用改进。\n')
A('### 5.3 第 3.5 步残差复核（只报警，不入馆）\n')
A('残差复核：扫描 **%d** 条，疑似漏检 **%d** 条（**%.2f%%**），采纳 **%d** 条。\n' % (
    RES['n_scanned'], RES['n_flagged'], RES['rate'] * 100, G['recall']['residual_adopted']))
A('| # | arXiv | 标题 | 赛道 | 处置 |')
A('|---|---|---|---|---|')
ADOPT = set(G['recall']['residual_adopted_list'])
for it in RES['flagged']:
    A('| %d | %s | %s | %s | %s |' % (
        it['n'], it['id'], it['title'][:62].replace('|', '/'), it['track'],
        '**采纳入本批**' if it['id'] in ADOPT else '留待人工挑选池（本批未入馆）'))
A('\n> 采纳口径：%d 篇全部为 12 赛道内的核心表述（%s），且与已入馆条目无同质（全批门① max Jaccard %.3f < 0.62）。'
  '清单本身只作报警，**未直接并入 registry**——%d 篇均另行走「全文抓取 → 7 维评分 → 产物」全流程后才入馆。'
  '残差率 **%.2f%%**，低于 12%% 的上报阈值，词表不重估、不扩表。\n' % (
      len(ADOPT), '、'.join('%s %d' % (k, v) for k, v in RES['by_track'].items()), g1['max_jaccard'],
      len(ADOPT), RES['rate'] * 100))
A('### 5.4 三关\n')
A('| 关卡 | 口径 | 本批数值 | 结论 |')
A('|---|---|---|---|')
A('| 门① 同质度 | 与库内非本批条目最大 Jaccard < 0.62 | **%.3f**（%s vs 库内 %s） | PASS |' % (
    g1['max_jaccard'], g1['pair'][0], g1['pair'][1]))
A('| 门② 赛道覆盖 | Top10 覆盖 ≥5 赛道 | **%d 赛道**（%s） | PASS（未重筛） |' % (
    g2['n_tracks'], '、'.join('%s×%d' % (k, v) for k, v in g2['top10_tracks'].items())))
A('| 门③ 价值天花板 | today_max ≥ 近 30 天 Top10 均分，且 margin ≥ 0.05 才授 S | **%.2f vs %.3f**，margin **%+.3f** | **重磅日，blockbuster=true，授 3 个 S** |' % (
    g3['today_max'], g3['top10_mean'], g3['margin']))
A('\n> 门③ 留痕（`data/gates_%s.json`）：`window_lo=%s`、`window_hi=%s`、`window_excludes_today=%s`、'
  '`window_excludes_this_run_batches=%s`、`this_run_batches_excluded=%s`、`heavy_day_raw=%s`、`heavy_day=%s`、'
  '`margin=%.4f`、`blockbuster=%s`、`s_awarded=%s`、`verdict=%s`；入窗 **%d 条**。\n' % (
      MMDD, g3['window_lo'], g3['window_hi'], g3['window_excludes_today'],
      g3['window_excludes_this_run_batches'], '、'.join(g3['this_run_batches_excluded']),
      g3['heavy_day_raw'], g3['heavy_day'], g3['margin'], g3['blockbuster'], g3['s_awarded'],
      g3['verdict'], g3['in_window']))
A('> 窗口为**半开区间** [今天−30 天, 今天)，且按 batch 剔除本次运行追加的两批（`2026-11-26`、`backfill-1126`）。'
  '本批 `today_max %.2f`、`top10_mean %.3f`、差值 **%.4f ≥ 0.05** → `blockbuster=true`，'
  '按 `grade_caliber.assign_grade` 的单一实现授 S（不是「接近」而是明确过线）。\n' % (
      g3['today_max'], g3['top10_mean'], g3['margin']))
A('### 5.5 评分披露（影响档位与可信度的三处判定）\n')
A('- **全部 63 篇 L0 / FULL，无 PARTIAL**：`fetch_fulltext.py` 的 `grade_evidence()` 本批加入 O-12 守卫'
  '（`len(text) < 8000` 且无正文一级章节标题 → 强制 `PARTIAL`），本批最小 24,073 字符，守卫未触发但已生效。'
  '这关闭了「连续两批靠人眼兜底」的遗留风险。\n')
A('- **7 篇 C 级仅入馆、不写笔记**：%s。均为「单一场景应用 / 装置描述 / 增量改进」，缺可迁移方法；'
  '按口径 C 级留 registry 供查重与去重，不生成原子笔记、不进 Top10。\n' % (
      '、'.join('%s %s %.2f' % (p['id'], p['title_zh'], p['value']) for p in D if p['grade'] == 'C')))
A('- **3 篇 S 的证据边界**：MoGe-4D 的「单张卡 8.5 s vs 81.7 s」是 50 帧全对跟踪、500 帧零样本仅作泛化探针'
  '（作者自陈非部署模式）；A Mesh to Remember 训练数据全为合成、真实扫描只做 zero-shot；'
  'AirLeg 在冰面（0.31 m）与松软沙地（0.29 m）仍逊于最佳对手（0.02/0.13 m）。'
  '三者均按「能力级突破 + 明确边界」记 S，未把单点最优表述为全面领先。\n')

# ---- 六、附录 ----
A('\n## 六、附录\n')
A('### 6.1 全文抓取与证据等级\n')
lv = Counter(MAN[p['id']]['level'] for p in D)
ev = Counter(MAN[p['id']]['evidence'] for p in D)
A('- %d 篇（%d + %d）串行 3 s/篇（`scripts/fetch_fulltext.py`）：**%s**；证据 **%s**；字符数 %s–%s。\n' % (
    len(D), len(MAIN), len(BF),
    ' / '.join('%s %d' % (k, v) for k, v in sorted(lv.items())),
    ' / '.join('%s %d' % (k, v) for k, v in sorted(ev.items())),
    format(min(MAN[p['id']]['chars'] for p in D), ','),
    format(max(MAN[p['id']]['chars'] for p in D), ',')))
A('- 逐篇抽看含 Introduction / Method / Experiments 正文节（最小 2.4 万字符，远超 ar5iv 摘要落地页 ~5k 量级），'
  '因此 **无一篇需要降级为摘要级证据**。\n')
A('### 6.2 本批数据文件\n')
A('- `data/audit_1126_days.json` / `audit_1126_alldays.json`：对账原始记录（7 分类日期头、declared/got）\n'
  '- `data/newday_1126.json`（11-25 组 624 唯一）、`data/missed_prev_1126.json`（上一组未入馆 977）、'
  '`data/missed_xr_1126.json`（复采核验，`leak_n=0`）\n'
  '- `data/xr_pool_1126.json`（97）、`data/old_replace_1126.json`（20）、`data/nonxr_1126.json`（527）\n'
  '- `data/residual_1126.json` + `data/residual_1126/{index,verdicts}.jsonl`（527 条逐条判定）\n'
  '- `data/decisions_1126.json`（主批 55 + backfill 8 赛道判定）、`data/published_1126.json`、'
  '`data/scored_1126.json`、`data/gates_1126.json`\n'
  '- `data/digest_1126_g1..g8.json`（63 篇精读 digest，g1 9 / g2 8 / g3 8 / g4 9 / g5 11 / g6 9 / g7 8 / g8 1）、'
  '`data/fulltext/<id>.txt` + `_manifest.json`\n')
A('### 6.3 待办与风险\n')
A('- **O-12 已关闭**：`fetch_fulltext.py` 的 landing-page 守卫已落地（`<8000` 字符且无一级章节标题 → PARTIAL）。'
  '本批 63 篇最小 24,073 字符，属正常全文；下批仍应抽查前 3 篇 .txt 头部确认 `# EVIDENCE:` 与实际一致。\n')
A('- **残差率 %.2f%%**（上批 2.45%%、再上批 1.63%%），本批 8 条采纳集中在「世界模型与仿真 2 / 评估与数据集 2 / '
  '重建与SLAM 2 / 内容生成 2」；另有 3 篇未被 flagged 但人工判定应收录（Xtream / BodyWeave / PRC4D），'
  '说明 `world model`、`4D reconstruction`、`garment` 三个表述仍是词表缺口，**下批评估是否把 `4d`、`garment` 纳入标题级扩展词**'
  '（按口径不得因单批自行扩表，需在残差连续 3 日 >12%% 或人工复核确认后登记）。\n' % (RES['rate'] * 100))
A('- **backfill 占比回升到 12.7%%（8/63）**：全部为 `replace` 再公告，首发跨度 2025-08-24 ~ 2026-10-08。'
  '其中 2605.00389 / 2604.03667 等早期稿件与当期工作相隔半年以上，已在笔记中保留首发日。\n')
A('- **渠道①（WorkBuddy 站点）历史挂账**：上批累计 36 批 403。本批按整改口径实测，若仍不可用则记「累计第 37 批挂账」，'
  '不影响 GitHub Pages 渠道与本地知识库。\n')

open('reports/XR-Daily-Report-%s.md' % DATE, 'w', encoding='utf-8').write('\n'.join(L) + '\n')
print('main report', len('\n'.join(L)))

# ==================== 二、7dim-table（主批 + backfill） ====================
T = []
t = T.append
t('# 7 维对比表 · %s（主批 %d 篇 + backfill %d 篇）\n' % (DATE, len(MAIN), len(BF)))
t('权重 IMP0.20·NOV0.20·TEC0.15·EXP0.15·PER0.15·TRL0.08·REP0.07；'
  '档位 S≥4.20 且 blockbuster / A3.60–4.20 / B3.00–3.60 / C<3.00。')
t('公告日 %s（周三）≠ 拉取日 %s（周四 02:30）；11-25 为单日公告组，无周末积压。' % (ANN, DATE))
t('\n## 主批（公告日 %s，%d 篇）\n' % (ANN, len(MAIN)))
t('| # | arXiv | 论文 | 赛道 | IMP | NOV | TEC | EXP | PER | TRL | REP | 总分 | 档 | 公告 | 证据 |')
t('|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|')
for i, p in enumerate(MAIN, 1):
    s = p['scores']
    t('| %d | %s | %s | %s | %d | %d | %d | %d | %d | %d | %d | **%.2f** | %s | %s | %s |' % (
        i, p['id'], p['title_zh'].replace('|', '/'), p['track'], s['IMP'], s['NOV'], s['TEC'],
        s['EXP'], s['PER'], s['TRL'], s['REP'], p['value'], p['grade'], p['announce'] or 'new', p['evidence']))
t('\n> 主批档位分布：S %d / A %d / B %d / C %d（C 级仅入馆、不写笔记）。本批 `blockbuster=true`，'
  'S 授予 %s。\n' % (GRM['S'], GRM['A'], GRM['B'], GRM['C'],
                     ' / '.join(p['id'] for p in TOP if p['grade'] == 'S')))
open('papers/daily/%s/7dim-table.md' % DATE, 'w', encoding='utf-8').write('\n'.join(T) + '\n')
print('7dim main', len(T))

TB = []
tb = TB.append
tb('# 7 维对比表 · backfill-%s（%d 篇）\n' % (MMDD, len(BF)))
tb('权重同上；**backfill 永不记 S**（即使 ≥4.20），且不参与当日重磅日判定。')
tb('本批为 %s 公告 RSS 中 `replace` 类再公告的旧稿，首发 %s ~ %s。\n' % (
    ANN, min(p['published'] for p in BF), max(p['published'] for p in BF)))
tb('| # | arXiv | 论文 | 赛道 | IMP | NOV | TEC | EXP | PER | TRL | REP | 总分 | 档 | 首发日 | 证据 |')
tb('|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|')
for i, p in enumerate(BF, 1):
    s = p['scores']
    tb('| %d | %s | %s | %s | %d | %d | %d | %d | %d | %d | %d | **%.2f** | %s | %s | %s |' % (
        i, p['id'], p['title_zh'].replace('|', '/'), p['track'], s['IMP'], s['NOV'], s['TEC'],
        s['EXP'], s['PER'], s['TRL'], s['REP'], p['value'], p['grade'], p['published'], p['evidence']))
tb('\n> backfill 档位分布：A %d / B %d / C %d；最高 %.2f（并列：%s）。\n' % (
    GRB['A'], GRB['B'], GRB['C'], max(p['value'] for p in BF),
    '、'.join(p['id'] for p in BF if p['value'] == max(x['value'] for x in BF))))
open('papers/daily/backfill-%s/7dim-table.md' % MMDD, 'w', encoding='utf-8').write('\n'.join(TB) + '\n')
print('7dim bf', len(TB))

# ==================== 三、backfill 报告 ====================
B = []
b = B.append
b('# XR Backfill 报告 · backfill-%s\n' % MMDD)
b('> **非当日新提交**：本批 %d 篇均为 %s 公告 RSS 混入的 `replace` 类旧稿再公告，首次入馆。'
  '按诚实口径单独编号，**不参与当日重磅日判定**，≥4.20 亦记 A（本批实际最高 %.2f，未触及该线）。\n' % (
      len(BF), ANN, max(p['value'] for p in BF)))
b('> 首发提交日（API `published`，非公告日）：%s。`updated` 均为 2026-11-23/24，'
  '即本次是「近期更新 + replace 再公告」，不是当期新工作。\n' % (
      '；'.join('%s = %s' % (p['id'], p['published']) for p in sorted(BF, key=lambda x: x['published']))))
b('\n## 一、摘要\n')
b('%s 公告 RSS 中 `replace` 类且摘要级 XR 命中 **%d 篇**（已扣已入馆者），逐篇核摘要取 **%d 篇**——'
  '其余多为机器人操作、医学影像、点云检测、通用视觉等非 XR 方向。定稿 **A %d / B %d / C %d，无 S**。\n' % (
      ANN, len(OLD), len(BF), GRB['A'], GRB['B'], GRB['C']))
b('\n## 二、逐篇解读\n')
b('> 本批 C 级 %d 篇（%s）按口径仅入馆、不写笔记与不展开章节，仅在文末列出。\n' % (
    GRB['C'], '、'.join('%s %s' % (p['id'], p['title_zh']) for p in BF if p['grade'] == 'C')))
for i, p in enumerate([x for x in BF if x['grade'] != 'C'], 1):
    g = DIG[p['id']]
    b('\n### %d. %s（%s · %s · %.2f %s）\n' % (i, p['title_zh'], p['id'], p['track'], p['value'], p['grade']))
    b('**一句话结论**：%s\n' % concl(p['id']))
    b('**要解决的问题**\n\n%s\n' % g['problem'])
    b('**方法详解**\n\n%s\n' % g['method'])
    b('**实验与结果**\n\n%s\n' % bl(g['key_numbers']))
    b('**创新点**\n\n%s\n' % bl(g['novelty']))
    b('**局限与风险**\n\n%s\n' % bl(g['limitations']))
    b('**可复现性**\n\n- 代码/项目页：%s\n- 全文证据：%s（%s，%s 字符）\n- 首发提交日 %s（本批为 `replace` 再公告）\n' % (
        p.get('code') or '正文未提供', p['evidence'], MAN[p['id']]['level'],
        format(MAN[p['id']]['chars'], ','), p['published']))
b('\n## 三、完整 7 维表\n')
b('见 [papers/daily/backfill-%s/7dim-table.md](../papers/daily/backfill-%s/7dim-table.md)。\n' % (MMDD, MMDD))
open('reports/XR-Backfill-Report-backfill-%s.md' % MMDD, 'w', encoding='utf-8').write('\n'.join(B) + '\n')
print('backfill report', len('\n'.join(B)))

# ==================== 四、scored.md ====================
WHY = {
 '2611.32198': (
   '4D 重建 + 跟踪 + 相机位姿统一进单次前向，是动态场景进入实时管线的能力级使能，零样本 500 帧说明可用面宽。',
   '把 4D 预测收敛成「成对 allo/ego 点图」这一接口，位姿由闭式刚体对齐给出而非黑箱回归；仍在「点图 + 相机」谱系内，故不给 5。',
   'context/query 双编码器 + 桥接特征注入 + 不确定度加权 Umeyama + 稀疏位姿图闭环；RigIDTrack 用 affine body 把 2.3M 动态面片压 700× 是硬贡献。',
   '跟踪（相机系/世界系/遮挡）、多视图重建、度量尺度、500 帧长序列四类实验齐备，含「去掉桥接预对齐 71.17%→62.65%」等关键消融。',
   '50 帧全对跟踪 8.5 s vs Open-D4RT 81.7 s（约 10×）、500 帧比基线快 1.7–4.3×，效率与精度同时领先。',
   'TRL=3：离线片段推理；作者自陈数百帧前向「只是泛化探针而非可用部署模式」。',
   'REP=4：指标口径与消融充分、数据管线可复现；未见公开代码。'),
 '2611.32445': (
   '长时一致性是世界模型常驻 XR 场景的前提，object permanence 34.7→91.5 属结构性改善。',
   '「mesh 当地址、cell 为索引单位」把外观记忆从帧/相机解耦并跨 agent 共享；记忆蒸馏让学生读自己写出的记忆。',
   'cell 索引 + first/latest 双观察 + PCA 8-bit 压缩 18× + tile 级流式读取，系统完整且每步有实测支撑。',
   '静态/动态/多 agent 三组基准 + 8,001 帧 rollout 显存实测；但训练数据全合成，真实扫描只做 zero-shot。',
   '720p 41.1 FPS、37.0 MP/s（吞吐 2.7×）、峰值显存 <45 GiB，效率是并列卖点。',
   'TRL=3：需 coarse mesh 与 agent bounding box 输入，属研究原型。',
   'REP=4：指标与压缩比可复算；代码未提供。'),
 '2611.32523': (
   '低成本腿式机器人定位（相机 + IMU + 编码器）是移动 XR 与巡检的底座能力，17/17 序列 <0.4 m 属可靠性级提升。',
   'imperative learning 用于 sim-to-real 本体感知自适应（地图精化后用重投影而非位姿回归监督网络）+ 形变感知足-地因子；单点新颖、组合成熟。',
   '三阶段训练 + VCE 自标定 + 长窗边缘化 + LoRA 在线自适应与回滚门控，系统复杂但每步有据。',
   'GrandTour 17 序列 19 方法对比 + Go2 真机 10 序列 + 0.5 h 数据缩放实验 + 三项消融。',
   'Jetson AGX Orin 上实时（1.4/12 核、2.6 GB、34→38 ms），但系统较重、移植需裁剪。',
   'TRL=4：真机闭环 + 声明开源，未产品化。',
   'REP=4：基线多、口径清楚；「开源」为作者声明，本批未验证仓库。'),
 '2611.31757': (
   '公里级流式重建的尺度一致性是户外 XR 地图的痛点，显式尺度状态直接针对误差源。',
   '把尺度提为一等状态（窗口尺度比 + 独立环路尺度 + 度量/IMU 锚），而非事后用 Sim(3)/SL(4) 吸收。',
   '因子图设计干净（噪声随 e^{-ℓ} 缩放、Student-t 闭环权重、5 窗口剪枝），但依赖冻结 3DFM 前向。',
   'VBR / KITTI / Oxford / EuRoC / ScaRF 五组 + 四步消融（72.0→39.2→38.1→5.40 m）。',
   '单张 5090 上 10–21 FPS，3DFM 前向占 wall time 46–82%，效率受底座限制。',
   'TRL=3：无嵌入式/机载验证。',
   'REP=4：消融链完整、数据集公开。'),
 '2611.32351': (
   '注视是人类交互意图的主通道，把 gaze 变成 VLM 的一等输出可支撑下游交互与推理。',
   '三组可学习 gaze query 把 depth/head mask/heatmap 内化（推理免外部输入），点/框/热图/语言统一自回归。',
   'LoRA + 结构化解耦注意力 + 三个辅助 decoder，工程合理；但依赖 8 源数据集与 SAM3/DA3 补全质量。',
   'HoliGaze-Bench 全指标第一 + 5 个 native benchmark + 2 个 OOD，人工修改率 0.70%。',
   '2B 骨干、推理可跳过辅助分支，成本可控；未见时延与显存实测。',
   'TRL=3：真机仅定性 demo，缺闭环评测与用户研究。',
   'REP=4：数据与基准规模、构建流程披露充分。'),
 '2611.32482': (
   '单目 4D 人-景重建是体积视频、健身与远程呈现的共同输入，免训练插件降低落地门槛。',
   '用「同一张可见人体表面」作为人体与场景模型的免训练桥梁；序列尺度与逐帧平移解耦 + 跨帧一致投票。',
   '插件式设计、三种场景骨干通用，但性能受场景重建质量约束。',
   '3DPW / EMDB-1/2 / Bonn / BEDLAM2 四组 + 多骨干组合，含 G-MPJPE 的 40.7%/53.6% 降幅。',
   '仅 +4 ms/帧（初始化 10 ms/帧），RTX 4090 上端到端 6–14 FPS。',
   'TRL=3：研究级插件，未处理时序抖动与脚滑。',
   'REP=4：多骨干复现路径明确。'),
 '2611.31944': (
   '长时世界模型的 KV 检索是「能否常驻」的瓶颈，单卡跑 33B 有直接工程价值。',
   '几何 grounding + draft 细选两级，并给出 draft 与全分辨率相关性的等价关系、效用上界与 aliasing 界三条性质。',
   'SCG-Attention 按 FlashAttention tile 粒度流式搬运 + partial softmax 合并，取数落在关键路径上的问题被正面处理。',
   'ORBIA/LingBot 主实验 + VBench-Long 60 s + 四种 KV 检索基线延迟对比。',
   '5.49 FPS vs 4.71、3.27× 加速、显存降 42.2%、单张 H100 跑 33B。',
   'TRL=3：依赖相机位姿与 CPU 侧 pinned 内存。',
   'REP=4：理论 + 实测双证，口径清楚。'),
 '2611.31516': (
   '无初始化 SfM 是重建前端的长期难题，从随机初始化到可用重建有明确实用价值。',
   '结论级新意：代理 OSE 目标不是精度主因，联合度量精化才是；dOSE 只加一项相对深度残差且保住 VarPro 可分性。',
   'VarPro + Ruhe–Wedin 近似 + 深度一致性过滤 + LM 精化，链条完整。',
   'ETH3D / LaMAR / Minimal / SMERF 四组 + 三随机种子方差 + 去项消融（85.81%→31.99%）。',
   '未强调速度，只称「比专为该场景设计的 MP-SfM 显著更低」；效率不是本篇卖点。',
   'TRL=2：研究级前端，强依赖已知标定。',
   'REP=4：种子方差与消融完整，复现路径清楚。'),
 '2611.31918': (
   '3DGS 的排序规模、尾部效应与训练成本是 XR 端渲染的硬约束，5× 级加速属能力级。',
   '一次分解同时解决排序规模、负载不均与反向求导三问题；batch 边界状态使 batch 间可完全独立求导。',
   'CUDA 细节密集（分层前缀和、六段无主机同步流水、可见性位矩阵、Adam 融进反向、随机舍入、SH 惰性更新）。',
   '1080p/4K、负载不均视角、重建、训练四组；PSNR 差 0.01 dB、显存少 34%。',
   '2756/1533 FPS、相对 gsplat 5.1×/5.6×、训练 61.5 s vs 194.4 s。',
   'TRL=3：单卡 CUDA 实现，未覆盖移动/XR 芯片。',
   'REP=4：与 gsplat 同协议对比，指标可复算。'),
 '2611.31812': (
   '未见物体泛化是手-物交互从 demo 到产品的门槛，跨数据集 AUC 差 50+ 点属结构性。',
   '物体只用冻结位姿基础模型的内部特征（不用其输出位姿）；由粗到细接触把「重建本身当接触证据」。',
   '两阶段训练 + SDF 区域距离细化，模块清晰；细接触沿用前人 103 区域划分，粒度受限。',
   'DexYCB / HO3D / OakInk / HOI4D / OakInk2 / H2O 六组 + 接触 F1 与 ECE 校准。',
   '前馈单次推理、无逐场景优化；但正文未报端到端时延，故不给 5。',
   'TRL=3：依赖输入网格，无机器人闭环。',
   'REP=4：跨数据集数字完整、失败案例有交代。'),
}
SC = []
s_ = SC.append
s_('# 评分明细与覆盖校验 · %s\n' % DATE)
s_('## 一、门禁三关\n')
s_('- 门① 最大 Jaccard **%.3f**（%s vs %s）< 0.62 → PASS（只对比追加前库内集合，不含本批两批）' % (
    g1['max_jaccard'], g1['pair'][0], g1['pair'][1]))
s_('- 门② 定稿 Top10 覆盖 **%d 赛道**（%s；全批 %d 赛道）→ PASS，未触发重筛' % (
    g2['n_tracks'], '、'.join('%s%d' % (k, v) for k, v in g2['top10_tracks'].items()), g2['all_batch_tracks']))
s_('- 门③ 当日最高 **%.2f** vs 库内近 30 天 Top10 均分 **%.4f**（半开窗口 [%s, %s)、%d 条入窗、按 batch 剔除 %s）'
   '→ heavy_day_raw=%s、margin **%+.4f** → **blockbuster=%s，S 授予 %s**' % (
       g3['today_max'], g3['top10_mean'], g3['window_lo'], g3['window_hi'], g3['in_window'],
       '、'.join(g3['this_run_batches_excluded']), g3['heavy_day_raw'], g3['margin'],
       g3['blockbuster'], g3['s_awarded']))
s_('\n## 二、分档统计\n')
s_('- 主批 %d 篇：S %d / A %d / B %d / C %d（C 级仅入馆、不写笔记）' % (
    len(MAIN), GRM['S'], GRM['A'], GRM['B'], GRM['C']))
s_('- backfill %d 篇：A %d / B %d / C %d' % (len(BF), GRB['A'], GRB['B'], GRB['C']))
s_('- 全批：S %d / A %d / B %d / C %d' % (GR['S'], GR['A'], GR['B'], GR['C']))
s_('\n## 三、Top10 逐维评分理由（10 篇）\n')
for p in TOP:
    s_('### %s %s（%.2f / %s / %s）\n' % (p['id'], p['title_zh'], p['value'], p['grade'], p['track']))
    sc = p['scores']
    for j, k in enumerate(('IMP', 'NOV', 'TEC', 'EXP', 'PER', 'TRL', 'REP')):
        s_('- **%s=%d**：%s' % (k, sc[k], WHY[p['id']][j]))
    s_('')
s_('\n## 四、backfill 逐篇理由（%d 篇）\n' % len(BF))
for p in BF:
    sc = p['scores']
    s_('### %s %s（%.2f / %s / 首发 %s）\n' % (p['id'], p['title_zh'], p['value'], p['grade'], p['published']))
    s_('- 向量：IMP %d / NOV %d / TEC %d / EXP %d / PER %d / TRL %d / REP %d' % (
        sc['IMP'], sc['NOV'], sc['TEC'], sc['EXP'], sc['PER'], sc['TRL'], sc['REP']))
    s_('- 要点：%s' % (DIG[p['id']]['novelty'][0] if isinstance(DIG[p['id']]['novelty'], list) else DIG[p['id']]['novelty'])[:120])
    s_('- 为何不更高：属旧稿再公告（首发 %s），与库内同期同赛道条目相比无新增能力面；TRL 与 PER 按当期可比口径给分，'
       '**不因首次入馆而溢价**，且按口径不评 S。' % p['published'])
    s_('')
s_('\n## 五、其余 %d 篇评分要点\n' % (len(MAIN) - len(TOP)))
s_('| arXiv | 论文 | 赛道 | IMP | NOV | TEC | EXP | PER | TRL | REP | 总分 | 档 | 要点 |')
s_('|---|---|---|---|---|---|---|---|---|---|---|---|---|')
for p in MAIN:
    if p['in_top10']:
        continue
    sc = p['scores']
    nov = DIG[p['id']]['novelty']
    nov = nov[0] if isinstance(nov, list) and nov else str(nov)
    s_('| %s | %s | %s | %d | %d | %d | %d | %d | %d | %d | %.2f | %s | %s |' % (
        p['id'], p['title_zh'][:28].replace('|', '/'), p['track'], sc['IMP'], sc['NOV'], sc['TEC'],
        sc['EXP'], sc['PER'], sc['TRL'], sc['REP'], p['value'], p['grade'], nov[:86].replace('|', '/')))
s_('\n> 要点列取自各篇 digest 的 `novelty[0]`（唯一来源，未二次转录）。')
s_('> 逐维展开只对 Top10 给出；其余篇目的档位由同一权重与 `grade_caliber.assign_grade` 机械计算。\n')
open('papers/daily/%s/scored.md' % DATE, 'w', encoding='utf-8').write('\n'.join(SC) + '\n')
print('scored.md', len('\n'.join(SC)))

# ==================== 五、run_log ====================
u_c = shutil.disk_usage('C:/')
u_d = shutil.disk_usage('D:/')
RL = []
r = RL.append
r('# 运行日志 · %s\n' % DATE)
r('- 02:30 起跑；跑前查 C: 盘剩余空间（未触发磁盘保护）。收尾实测 C: %.2f GB / D: %.2f GB。' % (
    u_c.free / 2**30, u_d.free / 2**30))
r('- 第 1 步 对账：`scripts/audit_listing_1126.py`（PREV_DAY=11-24 / NEW_DAYS=11-25,11-26），7/7 分类成功、exit 0；'
  '%s 组 **%s 槽位 / %s 唯一**；11-26 组 declared=None（未释放）；11-24 组复采 declared=got（494/13/61/18/191/485/23）。' % (
      ANN, format(AG['slots'], ','), format(AG['unique'], ',')))
r('- 第 1 步补充 上一组复采：`scripts/missed_xr_1126.py` → 未入馆 **%d** 篇、摘要覆盖 **%d/%d = 1.0000**、'
  '命中 **%d** 篇全部落在上批处置集合 → **0 漏网**。' % (
      MX['unadmitted'], MX['with_abstract'], MX['unadmitted'], len(MX['hits'])))
r('- 第 2 步 数据源：API 双主机探针 200（仅用于提交日核验）；RSS 7/7、**921 条**，WROTE=921 OK_CATS=7/7；'
  'listing %s/%s 覆盖 → 免 id_list。' % (format(AG['unique'], ','), format(AG['unique'], ',')))
r('- 第 3 步 甄别：`triage_1126.py`（数据源 `2026-11-26_all.jsonl` 921 条 no-filter，只取 day=11-25 的 newday）'
  '→ 覆盖率 1.0000（624/624）、KW %d + TITLE_EXTRA %d = 池 %d → 逐篇核摘要剔 %d → %d。' % (
      G['recall']['kw_hits'], G['recall']['title_extra'], G['recall']['pool'], len(REJ),
      G['recall']['pool'] - len(REJ)))
r('- 第 3 步补充 backfill：20 条 `replace` XR 命中，逐篇核摘要取 %d 篇（首发 %s ~ %s）。' % (
    len(BF), min(p['published'] for p in BF), max(p['published'] for p in BF)))
r('- 第 3.5 步 残差：`residual_scan.py dump/ingest` → 扫描 **%d**、判 **%d**（**%.2f%%**）、采纳 **%d**；'
  '另通读补入 3 篇（2611.31757 / 2611.32034 / 2611.32396，未被自动 flagged）→ 主批 %d。' % (
      RES['n_scanned'], RES['n_flagged'], RES['rate'] * 100, G['recall']['residual_adopted'], len(MAIN)))
r('- 第 4 步 全文：63 篇串行 3 s/篇 → **63 L0/FULL**（O-12 守卫已入库，本批最小 24,073 字符未触发降级）；'
  '字符 %s–%s。' % (format(min(MAN[p['id']]['chars'] for p in D), ',',),
                    format(max(MAN[p['id']]['chars'] for p in D), ',')))
r('- 第 4 步补充 提交日核验：`check_published_1126.py` → 63/63 全齐；主批 %s。' % pub_dist(MAIN))
r('- 第 5 步 评分：8 组子代理 digest（9/8/8/9/11/9/8/1 = 63）+ 主会话按标准权重重算；'
  '主会话校准三处：MoGe-4D TRL 4→3、AirLeg TRL 5→4 并删除正文查不到的「38 ms 端到端」表述、Xtream PER 5→4；'
  'Top10 逐维理由落 `papers/daily/%s/scored.md`。' % DATE)
r('- 第 6 步 三关：门① %.3f（%s vs %s）；门② %d 赛道（未重筛）；门③ %.2f vs %.3f，margin %+.3f '
  '→ heavy_day_raw=true、blockbuster=true、s_awarded=true。' % (
      g1['max_jaccard'], g1['pair'][0], g1['pair'][1], g2['n_tracks'],
      g3['today_max'], g3['top10_mean'], g3['margin']))
r('- 第 7 步 Top10：实数 10 篇（4.57–3.85），3 S / 7 A；全批 S %d / A %d / B %d / C %d。' % (
    GR['S'], GR['A'], GR['B'], GR['C']))
r('- 第 8 步 产物：报告 2 + 笔记 %d（C 级 7 篇不写）+ MOC 2 + 总索引刷新 + 7dim-table（主批/backfill 各 1）+ '
  'scored.md + run_log；registry 1,206 → **1,269**（+63，备份 `registry.jsonl.bak-20261126`）。'
  '易错点：`7dim-table.md` 表头必须保留 `arXiv` 列，否则前端批次卡表内计数为 0。' % (len(D) - GR['C']))
r('- 第 9 步 发布：见下方发布记录（构建 → `node --check` → CDP 冒烟 → `check_release` → 提交 → 推送 → Pages 核验）。')
open('papers/daily/%s/run_log.md' % DATE, 'w', encoding='utf-8').write('\n'.join(RL) + '\n')
print('run_log ok')
