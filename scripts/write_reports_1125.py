# -*- coding: utf-8 -*-
"""2026-11-25 最终解读报告 + backfill 报告 + daily 产物（7dim-table / scored / run_log）。

口径要点（不可改写）：
- 公告日 2026-11-24（周二）≠ 拉取日 2026-11-25 02:30；11-25 组尚未公告。
- 11-21 / 11-22 为周末 skipDays 不公告，其提交并入 11-24 公告批次。
- 主批 68 + backfill 6 = 74；A46 / B26 / C2；0 S（门③ blockbuster=false）。
"""
import glob
import json
import os
import re
import shutil
from collections import Counter

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
os.chdir(ROOT)
DATE, MMDD = '2026-11-25', '1125'
ANN = '2026-11-24'

D = json.load(open('data/scored_%s.json' % MMDD, encoding='utf-8'))
G = json.load(open('data/gates_%s.json' % MMDD, encoding='utf-8'))
RES = json.load(open('data/residual_%s.json' % MMDD, encoding='utf-8'))
PUB = json.load(open('data/published_%s.json' % MMDD, encoding='utf-8'))
MAN = json.load(open('data/fulltext/_manifest.json', encoding='utf-8'))
REJ = json.load(open('data/rejected_%s.json' % MMDD, encoding='utf-8'))
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
for k in range(1, 7):
    for r in json.load(open('data/digest_%s_g%d.json' % (MMDD, k), encoding='utf-8')):
        DIG[r['id']] = r

# 评分要点标签直接取自 build_scored 的行内注释（唯一实现，避免二次人工转录）
LABEL = {}
for ln in open('scripts/build_scored_%s.py' % MMDD, encoding='utf-8'):
    m = re.search(r'"(\d{4}\.\d{4,5})":\s*\(([\d,\s]+)\),\s*#\s*(.+)', ln)
    if m:
        LABEL[m.group(1)] = m.group(3).strip()


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
A('> **诚实口径**：本批处理的是 **%s（周二）公告批次**，拉取时刻 **2026-11-25 02:30（北京时间）**。'
  '11-25 组此刻**尚未公告**（拉取早于 11-25 00:00 UTC = 08:00 北京时间的释放时刻）；'
  '11-21（周六）/ 11-22（周日）为 `skipDays` 无公告段，其提交并入 11-24 公告批次统一释放。'
  'arXiv **公告日 ≠ 拉取日 ≠ 首次提交日**：主批 API `published` 核验为 %s（合计 68）；'
  'RSS 的 `published` 是公告时间戳，不能当提交日使用。\n' % (ANN, pub_dist(MAIN)))
A('> 覆盖范围：cs.CV / cs.GR / cs.HC / cs.MM / cs.RO / cs.AI / eess.IV 七分类 listing（show=500 单页，逐分类 declared=got 核对）。'
  '%s 组 **%s 槽位 / %s 篇唯一**（%s），全部命中 RSS **1,547 条**（缺收 0），摘要级覆盖率 **1.0000**。\n' % (
      ANN, format(AG['slots'], ','), format(AG['unique'], ','),
      ' / '.join('%s %d' % (k, v['got']) for k, v in AG['per_cat'].items())))

# ---- 一、执行摘要 ----
A('\n## 一、执行摘要\n')
A('**本批 %d 篇（主批 %d + backfill %d），0 S / %d A / %d B / %d C；Top10 实数 10 篇、全 A，最高 %.2f（2611.31140 HoloSplat）。**'
  ' 门③ 现算：当日最高 %.2f vs 库内近 30 天 Top10 均分 **%.3f**（%d 条入窗，半开窗口 [%s, %s)，按 batch 剔除本次追加的 `%s`），'
  'margin **%+.3f** → `heavy_day_raw=false`、`blockbuster=false`，**本批无 S 级**；'
  'HoloSplat 已过 4.20 线，仍按口径记 A（不因「接近 S」上调）。\n' % (
      len(D), len(MAIN), len(BF), GR['A'], GR['B'], GR['C'], g3['today_max'],
      g3['today_max'], g3['top10_mean'], g3['in_window'], g3['window_lo'], g3['window_hi'],
      '、'.join(g3['this_run_batches_excluded']), g3['margin']))
A('当日四条主线：\n')
A('1. **前馈人体与手部重建跨过「实时可用」门槛，且提速点不在算力而在表示层**：2611.31140 HoloSplat 把码率控制点'
  '前移到 Gaussian head **之前**的 token 空间——token 低维、紧支撑，对量化扰动的敏感度远低于指数尺度的 Gaussian 属性，'
  '于是 4×RTX 5090 上做到 **32.2 FPS @ 50 Mbit/s**（仅 1 张/6 张卡时 8.0/51.3 FPS），RTX 3050 Ti 笔记本解码每帧 **22.1 ms**，'
  '208.2 kB/帧对未压缩 4,753.1 kB/帧少 **22.8×**；2611.30597 ViDiHand2 把 VDM 手部深度从「外观回归」改成'
  '「测试相机射线上的几何约束求解」，野外 MPJPE-abs-p **56.55→32.59 mm（−42%）**、域内 24.46→19.62 mm，'
  '检测失败/误检帧占比仅 0.07%/0.11%（比 ViDiHand 少 14.57×/8.82×）；2611.29163 把「结构性缺失」当一等设定，'
  '按解剖规则在 3D 上删 MANO 段再渲染，IncNYU `E_avg` **8.00 对 11.49（−30.4%）** 而 NYU 精度不降。\n')
A('2. **空间智能的几何从「外挂模块」搬进「可读写、可干预的内部状态」**：2611.28649 S-Mind 不再训一个空间 VLM，'
  '而是给模型一段**场景 token**（`z_0` 承载融合场景、`z_k` 在每次声明视角时重表达），并用冻结读出器把'
  '「感知」与「变换」解耦监督——Qwen3.5-9B 四基准均值 **74.03%**（比最强微调基线高 6.76 分），'
  '跨视图点恢复率 **65.11% vs 基线最高 16.02%**，均值已超 GPT-6-Astra（73.58%）；2611.29236 更极端，'
  '不重训、不改表示、不需要目标视角观测，只用同一冻结表示在不同视角下的**误差互补性**构造候选，'
  '准入按「期望绝对误差下降」而非「改进概率」（并从理论上证明代价加权 BCE 的零 logit 阈值正好与之对齐）——'
  'DTU AbsRel 0.0440→0.0180、RIG 动态骨干降 21.7–45.5%；2611.31156 用 router 在 decoder **之前**预测目标视角会用到哪些 '
  'source token，24 视图比 LagerNVS 快 **6.4×**（PSNR 仅低 0.68 dB），固定预算下 82–87 FPS 与源视图数近乎脱钩。\n')
A('3. **世界模型与触觉都开始「先验证、再使用」**：2611.30572 VeriTouch 把触觉作为独立专家接入预训练视频 MoT，'
  '并把「触觉真实性 + 接触力合理性 + 视触接触区间时间对齐」做成联合验证器，在动作提取前过滤——'
  '五个真实任务四种策略平均成功率 **19.4%→33.8%**（Bo3 30.8%→48.8%），而**去掉验证器只有 22.9%**（与仅真实数据持平）：'
  '这条负结果比 SOTA 数字更能界定「合成数据什么时候真的有用」。同向的还有第 3.5 步残差捞回的 2611.28136 Engram'
  '（可靠性加权潜融合 + 遮挡感知分层读出）与 2611.28666 RecallWorld（情节记忆的持久具身世界模型）——'
  '「记忆 / 可靠性」已成为世界模型的独立设计维度，而非训练副产品。\n')
A('4. **主动感知从「下一最佳视角」升级为「目标 + 路径」，重建从「迭代优化」压成「单次前向」**：2611.30802 '
  '把稀疏主动重建的决策对象从单个 NBV 换成「目标 + 变长路径前缀」，用持久目标把走廊通行折算为远端房间的剩余价值，'
  '并以表面 cell 上记录的「更新后缺陷 + 观测方向」做免渲染打分——HSSD 平均 Cov10 **74.1%→93.3%**、HM3D **47.2%→95.6%**'
  '（Chamfer 降 26.9×），500 视图预算下 33 房间住宅仍达 **74.1%**（所有基线 <20%）；2611.28520 VG3R 的关键洞察是'
  '视频 DiT 内部**已经**编码了深度与相机、只是「形式不对」，用片段级 shift 修正归一化逆深度、用多层特征直接回归相机，'
  '把迭代去噪式重建压成单次前向——ScanNet/TUM ATE 降 **55.1%/56.3%**，单帧 74–84 ms（GH200），比 Geo4D 快约 14×。\n')
A('> 另有一处结构性变化值得单列：**渲染与显示赛道本批 3 篇**，其中残差捞回的 2611.29678 Ref2Light 是连续多批'
  '「无器件级破冰」之后**首次命中光场裸眼 3D 显示**（单图→可交互裸眼 3D 角色）。但它仍属内容与算法侧'
  '（合成光场/多视点编码），**不是波导、可变焦、Maxwellian 一类器件突破**，口径上不计作硬件破冰。\n')
A('**筛选与复核**：摘要级 KW 命中 **%d** 篇 + 标题级扩展词补扫 **%d** 篇 = 候选池 **%d** 篇；逐篇核摘要剔 **%d** 篇'
  '（机器人操作/控制/自动驾驶 27、遥感测绘雷达与 BIM 13、医学与生物医学 10、通用 LLM/VLM 空间推理 16、'
  '生成式通用视觉 10、音频/OCR/安全/纯数学 8），得 **%d** 篇；第 3.5 步残差复核扫描 **%d 条**、判 **%d 条**应收录'
  '（**%.2f%%**）、**采纳 %d 篇** → 主批 **%d 篇**。'
  '上一公告组（11-23 组，404 篇唯一）未入馆 **363 篇** 复采核验：**363/363 均有摘要**，摘要/标题级命中 40 篇'
  '**全部落在上批处置集合**（`nonxr_1124 ∪ xr_pool_1124 ∪ backfill_1124 ∪ scored_1124`）→ **0 漏网**'
  '（`data/missed_xr_%s.json` 为空对象），无需补漏。\n' % (
      G['recall']['kw_hits'], G['recall']['title_extra'], G['recall']['pool'],
      G['recall']['rejected_from_pool'], len(MAIN), RES['n_scanned'], RES['n_flagged'],
      RES['rate'] * 100, G['recall']['residual_adopted'], len(MAIN), MMDD))

# ---- 二、Top10 ----
A('\n## 二、Top10 排行榜\n')
A('| 排名 | 论文 | 赛道 | 总分 | 档 | 证据 | 关键贡献 |')
A('|---|---|---|---|---|---|---|')
SHORT = {
 '2611.31140': '码率控制点前移到 Gaussian head 之前的 token 空间：4×5090 上 32.2 FPS @ 50 Mbit/s，208.2 kB/帧（少 22.8×），笔记本解码 22.1 ms。',
 '2611.28649': '给模型可被注意力读写的场景 token，并用冻结读出器解耦感知与变换：Qwen3.5-9B 四基准均值 74.03%（+6.76），跨视图点恢复 65.11% 对 16.02%。',
 '2611.30597': 'VDM 手部深度改为相机射线上的几何约束求解（多关节对距离定尺度）：野外 MPJPE 56.55→32.59 mm（−42%），失败帧占比少 8.82×。',
 '2611.30461': '解耦显示时钟与生成时钟（光流 warp + 交叉淡化）：720p 25 FPS、新帧 370–490 ms，LPIPS 0.137→0.077，长裤失败率 33%→4.2%。',
 '2611.30802': '决策对象从单个 NBV 换成「目标 + 变长路径前缀」，免渲染端点/路径/目标统一打分：HSSD Cov10 74.1%→93.3%、HM3D 47.2%→95.6%。',
 '2611.29236': '不重训不改表示，用冻结表示跨视角的误差互补性做选择性纠正，准入按期望绝对误差下降：DTU AbsRel 0.0440→0.0180，RIG 动态骨干降 21.7–45.5%。',
 '2611.30572': '触觉作独立专家接入视频 MoT，真实性/接触力/时空对齐联合验证后再提动作：五任务平均 SR 19.4%→33.8%，去掉验证器仅 22.9%。',
 '2611.31156': 'router 在 decoder 前预测目标视角会用哪些 source token（NMS 去重复编码）：24 视图快 6.4×（PSNR −0.68 dB），82–87 FPS 与视图数近脱钩。',
 '2611.28520': '把视频 DiT 内部已编码的深度与相机直接读出（片段级 shift + 多层特征）：ScanNet/TUM ATE 降 55.1%/56.3%，单帧 74–84 ms，比 Geo4D 快 14×。',
 '2611.29163': '结构性缺失当一等设定（3D 删 MANO 段再渲染）+ 拓扑蒸馏与沿链父子推理：IncNYU E_avg 8.00 对 11.49（−30.4%），NYU 精度不降。',
}
for i, p in enumerate(TOP, 1):
    A('| %d | %s（%s） | %s | **%.2f** | %s | %s | %s |' % (
        i, p['title_zh'], p['id'], p['track'], p['value'], p['grade'], p['evidence'], SHORT[p['id']]))
A('\n> **门② 未触发重筛**：纯值 Top10 已覆盖 **%d 赛道**（%s），全批 **%d 赛道**。\n' % (
    g2['n_tracks'], '、'.join('%s×%d' % (k, v) for k, v in g2['top10_tracks'].items()), g2['all_batch_tracks']))
A('> **OUTDATED / SUPERSEDED 均为 0**：本批未发现「同问题更优且更晚」的直接取代关系。'
  'backfill 6 篇为 `replace` 类旧稿再公告（首发 2025-11-25 ~ 2026-10-30），其中 2610.41373 Queryable Gaussian View Index'
  '（2026-10-30 首发）已在笔记中标注时效性风险，但未达论文级 OUTDATED 证据门槛。\n')

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
        p['batch'], p['announce'], p['track'], p['published'])
    if p.get('recall') == 'RESIDUAL_ADOPT':
        rel += ('\n- **由第 3.5 步残差复核捞回**：摘要级 KW 与标题级扩展词均未命中，说明现有词表在该表述上仍有语义缺口'
                '（该篇走完「全文抓取 → 7 维评分 → 产物」全流程后才入馆，清单本身未直接并库）。')
    if p.get('note'):
        rel += '\n- 备注：%s' % p['note']
    rel += '\n- 与库内同赛道论文构成并列参考；本批 OUTDATED/SUPERSEDED 判定为 0。'
    A('**与文献库的关系**\n\n%s\n' % rel)
    A('**可复现性**\n\n- 代码/项目页：%s\n- 全文证据：%s（%s，%s 字符，%s）\n' % (
        p.get('code') or '正文未提供', p['evidence'], MAN[p['id']]['level'],
        format(MAN[p['id']]['chars'], ','), MAN[p['id']]['url']))
    act = '- 纳入重点精读：方法与实验节可直接支撑选题与技术选型。' if p['grade'] == 'A' else '- 浏览级。'
    _cd = (p.get('code') or '').strip()
    _has = ('http' in _cd) and not _cd.startswith('未')
    if _has:
        act += '\n- 有公开代码/项目页，可先跑通再评估迁移成本。'
    else:
        act += '\n- 未见公开代码，复现需按正文细节自行实现。'
    if p['value'] >= 4.20:
        act += ('\n- 达 S 线（≥4.20）而本批门③ 判非重磅日（margin %+.3f）：值得优先读，'
                '但不宜按 S 级对外表述。' % g3['margin'])
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
A('- 7 分类最新公告日**全部为 %s（周二）**；11-25 组 `declared=None / got=0`（尚未释放）；'
  '11-21、11-22 为周末 `skipDays`，listing 无公告段。\n' % ANN)
A('- %s 组逐分类 declared=got：%s = **%s 槽位**，唯一论文 **%s 篇**（跨列表重复 %s）。'
  '上一公告组（11-23）复采 **506 槽位 / 404 篇唯一**、逐分类 declared=got。\n' % (
      ANN, ' / '.join('%s %d' % (k, v['got']) for k, v in AG['per_cat'].items()),
      format(AG['slots'], ','), format(AG['unique'], ','), format(AG['slots'] - AG['unique'], ',')))
A('- 上一公告组（11-23 组 404 篇唯一）未入馆 **363 篇 = 404 − 41（上批主批已入馆）**；'
  '用 11-23/11-24 两份 RSS 全量核摘要，**363/363 全覆盖、0 篇缺摘要**，摘要/标题级命中 **40 篇**'
  '**全部落入上批处置集合** → **0 漏网**（`data/missed_xr_%s.json` = `{}`）。\n' % MMDD)
A('### 5.2 数据源与召回\n')
A('- RSS 7 分类 `--no-filter` 去重 **1,547 条**（`WROTE=1547`、`OK_CATS=7/7`，完整采集：任一分类失败即 exit 2，本批未触发）。'
  'listing %s 篇 **100%% 被 RSS 覆盖（缺收 0）** → **免 API `id_list` 枚举**，规避 429 静默丢批；'
  'API 仅用于 74 篇的提交日核验（25 id/批、12 s 间隔，74/74 全齐）。\n' % format(AG['unique'], ','))
A('- 召回三层：摘要级 KW **%d** + 标题级扩展词补扫 **%d** = **%d 篇命中** → 逐篇核摘要剔 **%d 篇**'
  '（明细见 `data/rejected_%s.json`）→ **%d 篇**；残差采纳 **%d** 篇 → **主批 %d 篇**。'
  '入选主批的列表类别分布：%s。\n' % (
      G['recall']['kw_hits'], G['recall']['title_extra'], G['recall']['pool'],
      G['recall']['rejected_from_pool'],
      MMDD, G['recall']['pool'] - G['recall']['rejected_from_pool'],
      G['recall']['residual_adopted'], len(MAIN),
      ' / '.join('%s %d' % (k, v) for k, v in Counter(p['cat'] for p in MAIN).most_common())))

GROUP = {
 'G1': ('机器人操作 / 控制 / 自动驾驶 / 人形与无人机',
        '2611.27423 2611.28129 2611.28274 2611.28438 2611.28521 2611.28675 2611.28697 2611.28707 2611.28752 '
        '2611.28839 2611.29195 2611.29279 2611.29377 2611.29662 2611.29748 2611.29868 2611.29912 2611.29980 '
        '2611.30026 2611.30283 2611.30310 2611.30490 2611.30495 2611.30646 2611.30658 2611.30813 2611.30963'),
 'G2': ('遥感 / 测绘 / 雷达与光谱 / 林业与 BIM',
        '2611.28191 2611.28197 2611.28403 2611.28545 2611.28820 2611.29148 2611.29282 2611.29341 2611.29388 '
        '2611.30198 2611.30215 2611.30471 2611.30602'),
 'G3': ('医学与生物医学成像（含手术、牙科、rPPG、生物力学）',
        '2611.27996 2611.28185 2611.28283 2611.28901 2611.28905 2611.29105 2611.29330 2611.29421 '
        '2611.30131 2611.31128'),
 'G4': ('通用 LLM / VLM 空间推理、基准与训练机制',
        '2606.28090 2611.28706 2611.29146 2611.29194 2611.29206 2611.29265 2611.29954 2611.30040 '
        '2611.30055 2611.30424 2611.30514 2611.30564 2611.30720 2611.31021 2611.31022 2611.31025'),
 'G5': ('生成式通用视觉与三维内容生成（非 XR 管线）',
        '2611.28402 2611.28646 2611.29002 2611.29071 2611.29213 2611.29494 2611.29850 2611.30725 '
        '2611.30728 2611.31164'),
 'G6': ('音频 / 语音 / OCR / 安全 / 纯数学与仪器物理',
        '2611.29116 2611.29226 2611.29283 2611.29315 2611.29381 2611.29874 2611.30436 2611.31129'),
}
_assigned = set()
for _k, (_nm, _ids) in GROUP.items():
    _assigned |= set(_ids.split())
assert _assigned == set(REJ), ('分组与剔除集合不一致', sorted(set(REJ) - _assigned), sorted(_assigned - set(REJ)))
A('- 剔除 %d 篇的六组构成：\n' % len(REJ))
for _k in sorted(GROUP):
    _nm, _ids = GROUP[_k]
    A('  - **%s %d 篇**：%s' % (_nm, len(_ids.split()), '、'.join(sorted(_ids.split())[:4]) + ' 等'))
A('')
A('  误命中主因是 `spatial` / `hand` / `gaussian` / `tracking` / `depth` / `mesh` / `gaze` 等泛词与上述场景共现：'
  '`spatial` 多指空间推理基准与地理偏见，`hand` 多为手写体 OCR 与手部 X 光，`gaussian` 大量落在高斯分布 / EDA，'
  '`tracking` 多为状态跟踪与航空建图。\n')
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
A('\n> 采纳口径：6 篇全部为 12 赛道内的核心表述（%s），且与已入馆条目无同质（门① 复算 max Jaccard %.3f）。'
  '清单本身只作报警，**未直接并入 registry**——6 篇均另行走「全文抓取 → 7 维评分 → 产物」全流程后才入馆。'
  '残差率 **%.2f%%**，连续四批（2.2%% / 1.6%% / 2.8%%）远低于 12%% 阈值，词表不重估。\n' % (
      '、'.join('%s %d' % (k, v) for k, v in RES['by_track'].items()), g1['max_jaccard'], RES['rate'] * 100))
A('### 5.4 三关\n')
A('| 关卡 | 口径 | 本批数值 | 结论 |')
A('|---|---|---|---|')
A('| 门① 同质度 | 与库内非本批条目最大 Jaccard < 0.62 | **%.3f**（%s vs 库内 %s） | PASS |' % (
    g1['max_jaccard'], g1['pair'][0], g1['pair'][1]))
A('| 门② 赛道覆盖 | Top10 覆盖 ≥5 赛道 | **%d 赛道**（%s） | PASS（未重筛） |' % (
    g2['n_tracks'], '、'.join('%s×%d' % (k, v) for k, v in g2['top10_tracks'].items())))
A('| 门③ 价值天花板 | today_max ≥ 近 30 天 Top10 均分，且 margin ≥ 0.05 才授 S | **%.2f vs %.3f**，margin **%+.3f** | 非重磅日，**blockbuster=false，无 S** |' % (
    g3['today_max'], g3['top10_mean'], g3['margin']))
A('\n> 门③ 留痕（`data/gates_%s.json`）：`window_lo=%s`、`window_hi=%s`、`window_excludes_today=%s`、'
  '`window_excludes_this_run_batches=%s`、`this_run_batches_excluded=%s`、`heavy_day_raw=%s`、`margin=%.4f`、'
  '`blockbuster=%s`、`s_awarded=%s`；入窗 **%d 条**。\n' % (
      MMDD, g3['window_lo'], g3['window_hi'], g3['window_excludes_today'],
      g3['window_excludes_this_run_batches'], '、'.join(g3['this_run_batches_excluded']),
      g3['heavy_day_raw'], g3['margin'], g3['blockbuster'], g3['s_awarded'], g3['in_window']))
A('> 窗口为**半开区间** [今天−30 天, 今天)，且按 batch 剔除本次运行追加的两批（`2026-11-25`、`backfill-1125`）；'
  '该口径自 2026-11-18 起实施，历史数值不回算。本批 `today_max %.2f` 与 `gate3.top10_mean %.3f` 之差为 %.3f，'
  '低于 0.05 的授 S 门槛，故即使 today_max 已过 4.20 线也不授 S。\n' % (
      g3['today_max'], g3['top10_mean'], g3['margin']))
A('### 5.5 评分披露（影响档位与可信度的三处判定）\n')
A('- **2611.29647 与 2611.30012 记 PARTIAL**：`fetch_fulltext.py` 初判 L1/FULL，但 5,105 / 4,581 字符实为 ar5iv 的'
  '**摘要落地页**（含 `Skip to main content`、`View PDF`、`Submission history`，无 Introduction / Method / Results 节）。'
  '已手动改判 `evidence=PARTIAL`、`.txt` 头同步为 `# EVIDENCE: PARTIAL`，并要求子代理只按摘要级证据作答；'
  '两篇 TEC/EXP（含 2611.30012 的 PER）已相应下调，笔记与本章均标注该限制。**这是本批唯一的非 FULL 证据**，'
  '不参与任何「方法细节」断言。\n')
A('- **2 篇 C 级仅入馆、不写笔记**：2611.28027（无代码可穿戴验证工具链，2.85）与 2611.30552（商用语音 AI + 化身的'
  '实验装置，1.85）——前者是工程工具、后者是装置描述，均缺可迁移方法。按口径 C 级留 registry 供查重与去重，'
  '不生成原子笔记、不进 Top10、不计入批次卡表内计数。\n')
A('- **HoloSplat 4.21 达 S 线未授 S**：门③ 机械判定 `today_max 4.21 < 4.432`（margin %+.3f），'
  '`heavy_day_raw=false` → `blockbuster=false`；按 `grade_caliber.assign_grade` 的单一实现，S 需「≥4.20 **且** blockbuster」，'
  '故记 A。**未做任何人工上调**：与 11-21（margin +0.007 险过）不同，本批差值为 %.3f，属明确非重磅日。\n' % (
      g3['margin'], g3['margin']))

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
A('- %d 篇 FULL：逐篇抽看含 Introduction / Method / Experiments 正文节（最小约 2.5 万字符，远超 ar5iv 摘要页 ~5k 量级）。'
  '唯一 2 篇 PARTIAL 见 §5.5。\n' % ev['FULL'])
A('### 6.2 本批数据文件\n')
A('- `data/audit_1125_days.json` / `audit_1125_alldays.json`：对账原始记录（7 分类日期头、declared/got）\n'
  '- `data/newday_1125.json`（1,045 篇唯一）、`data/missed_prev_1125.json`（363）、`data/missed_xr_1125.json`（空）\n'
  '- `data/xr_pool_1125.json`（146）、`data/rejected_1125.json`（84）、`data/cand_1125.json`（62）、'
  '`data/backfill_1125.json`（6）、`data/nonxr_1125.json`（899）\n'
  '- `data/residual_1125.json` + `data/residual_1125/{index,verdicts}.jsonl`（899 条逐条判定）\n'
  '- `data/published_1125.json`、`data/scored_1125.json`、`data/gates_1125.json`\n'
  '- `data/digest_1125_g1..g6.json`（74 篇精读 digest）、`data/fulltext/<id>.txt` + `_manifest.json`\n')
A('### 6.3 待办与风险\n')
A('- **硬件显示侧仍未破冰，但出现首个内容侧信号**：本批「渲染与显示」3 篇，其中 Ref2Light（光场裸眼 3D）是'
  '连续多批 0 篇之后首次命中该方向；但它解决的是「单图 → 可交互裸眼 3D 角色」的生成与编码，不涉及光学器件。'
  '波导 / 可变焦 / Maxwellian / 眼动光学仍只能靠会议或厂商渠道补充。\n')
A('- **PARTIAL 守卫仍未落到脚本里**：上一批 §6.3 已提出「`chars < 8000` 且命中 landing 特征 → 强制 PARTIAL」，'
  '但本批仍是人工抽看后发现（两篇 4–5k 字符被判 L1/FULL）。**这是连续第二批靠人眼兜底**，'
  '下批必须把守卫写进 `fetch_fulltext.py`，否则证据等级会系统性虚高。\n')
A('- **残差率 %.2f%%**（上批 2.2%%、再上批 1.6%%、再上批 2.8%%），连续四批低于 12%% 阈值；本批 6 条采纳中'
  '「世界模型与仿真 2 / 化身与人体 2 / 重建与SLAM 1 / 渲染与显示 1」，缺口仍集中在 `world model`、'
  '`avatar`、`light field` 三个表述的语义边界。\n' % (RES['rate'] * 100))
A('- **backfill 占比回升**：本批 backfill 6 篇（占 8.1%%），全部为 `replace` 再公告；其中 2511.20578 首发于 **2025-11-25**'
  '（v2 于 2026-11-23 更新），跨度超过一年，需在笔记层保留首发日以免被误读为当期工作。\n')

open('reports/XR-Daily-Report-%s.md' % DATE, 'w', encoding='utf-8').write('\n'.join(L) + '\n')
print('main report', len('\n'.join(L)))

# ==================== 二、7dim-table（主批 + backfill） ====================
T = []
t = T.append
t('# 7 维对比表 · %s（主批 %d 篇 + backfill %d 篇）\n' % (DATE, len(MAIN), len(BF)))
t('权重 IMP0.20·NOV0.20·TEC0.15·EXP0.15·PER0.15·TRL0.08·REP0.07；'
  '档位 S≥4.20 且 blockbuster / A3.60–4.20 / B3.00–3.60 / C<3.00。')
t('公告日 %s（周二）≠ 拉取日 %s（周三 02:30）；11-21/11-22 为周末 skipDays 不公告，其提交并入本公告批次。' % (ANN, DATE))
t('\n## 主批（公告日 %s，%d 篇）\n' % (ANN, len(MAIN)))
t('| # | arXiv | 论文 | 赛道 | IMP | NOV | TEC | EXP | PER | TRL | REP | 总分 | 档 | 公告 | 证据 |')
t('|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|')
for i, p in enumerate(MAIN, 1):
    s = p['scores']
    t('| %d | %s | %s | %s | %d | %d | %d | %d | %d | %d | %d | **%.2f** | %s | %s | %s |' % (
        i, p['id'], p['title_zh'].replace('|', '/'), p['track'], s['IMP'], s['NOV'], s['TEC'],
        s['EXP'], s['PER'], s['TRL'], s['REP'], p['value'], p['grade'], p['announce'], p['evidence']))
t('\n> 主批档位分布：A %d / B %d / C %d（C 级仅入馆、不写笔记）。本批 `blockbuster=false`，故 4.21 的 HoloSplat 记 A。\n' % (
    GRM['A'], GRM['B'], GRM['C']))
open('papers/daily/%s/7dim-table.md' % DATE, 'w', encoding='utf-8').write('\n'.join(T) + '\n')
print('7dim main', len(T))

TB = []
tb = TB.append
tb('# 7 维对比表 · backfill-%s（%d 篇）\n' % (MMDD, len(BF)))
tb('权重同上；**backfill 永不记 S**（即使 ≥4.20），且不参与当日重磅日判定。')
tb('本批为 %s 公告 RSS 中 `replace` 类再公告的旧稿，首发 2025-11-25 ~ 2026-10-30。\n' % ANN)
tb('| # | arXiv | 论文 | 赛道 | IMP | NOV | TEC | EXP | PER | TRL | REP | 总分 | 档 | 首发日 | 证据 |')
tb('|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|')
for i, p in enumerate(BF, 1):
    s = p['scores']
    tb('| %d | %s | %s | %s | %d | %d | %d | %d | %d | %d | %d | **%.2f** | %s | %s | %s |' % (
        i, p['id'], p['title_zh'].replace('|', '/'), p['track'], s['IMP'], s['NOV'], s['TEC'],
        s['EXP'], s['PER'], s['TRL'], s['REP'], p['value'], p['grade'], p['published'], p['evidence']))
tb('\n> backfill 档位分布：A %d / B %d；最高 %.2f（2608.04701 UniView）。\n' % (GRB['A'], GRB['B'], max(p['value'] for p in BF)))
open('papers/daily/backfill-%s/7dim-table.md' % MMDD, 'w', encoding='utf-8').write('\n'.join(TB) + '\n')
print('7dim bf', len(TB))

# ==================== 三、backfill 报告 ====================
B = []
b = B.append
b('# XR Backfill 报告 · backfill-%s\n' % MMDD)
b('> **非当日新提交**：本批 %d 篇均为 %s 公告 RSS 混入的 `replace` 类旧稿再公告，首次入馆。'
  '按诚实口径单独编号，**不参与当日重磅日判定**，≥4.20 亦记 A（本批实际最高 %.2f，未触及该线）。\n' % (
      len(BF), ANN, max(p['value'] for p in BF)))
b('> 首发提交日（API `published`，非公告日）：%s。其中 2511.20578 首发于 **2025-11-25**、v2 于 2026-11-23 更新，'
  '跨度超一年；2610.41373 首发 2026-10-30、2611.20578 之后已属「同方向后续工作可能已发表」的时效风险区。\n' % (
      '；'.join('%s = %s' % (p['id'], p['published']) for p in sorted(BF, key=lambda x: x['published']))))
b('\n## 一、摘要\n')
b('%s 公告 RSS 共 **502 条** `replace` 类条目（含已入馆者的重复公告）；扣除已入馆后，摘要级 XR 命中 **%d 篇**，'
  '逐篇核摘要取 **%d 篇**——其余多为机器人操作、医学影像、点云检测、通用视觉等非 XR 方向。'
  '定稿 **%d A / %d B，无 S**。\n' % (ANN, len(OLD), len(BF), GRB['A'], GRB['B']))
b('\n## 二、逐篇解读\n')
for i, p in enumerate(BF, 1):
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
 '2611.31140': ('前馈流式人体重建决定「人体能否进实时管线」，属能力级使能；但它优化的是传输与解码链，不改重建范式。',
                '把码率控制点从 Gaussian 属性前移到 token 空间，并用逆 PCA 折进首层、残差 hypernetwork 折进输出层实现零显式展开，是把「表示选择」当压缩设计的少见做法。',
                'NSC 只用 warm-up 一秒的输入视角、配合 rank 截断，工程细节完整；缺端到端时延分解与丢包鲁棒性。',
                '4 卡 32.2 FPS / 单卡 8.0 FPS / 6 卡 51.3 FPS 三档实测 + 笔记本 22.1 ms 解码 + 208.2 kB/帧对 4,753.1 kB/帧，跨设备口径齐。',
                '4.21 为本批最高，且 22.8× 压缩与 22.1 ms 解码同时成立，是本批唯一同时改「带宽」与「延迟」两条硬指标的工作。',
                'TRL=4：有真实多卡部署与消费级 GPU 解码，仍属实验室原型，无产品级集成。',
                'REP=4：码率与 FPS 口径明确、可复算；未见公开代码。'),
 '2611.28649': ('空间智能是 XR 交互的前置能力，但本文是「把几何内化进 VLM」的路径验证，短期不直接产出产品指标。',
                '不是再训一个空间 VLM，而是给模型一段可被注意力读写的场景 token，并用冻结读出器把感知与变换解耦监督——把「几何」从外挂模块变成可干预的内部状态。',
                'token 状态替换/扣留的因果干预写得清楚，但没有给出 token 维度与表达力的关系曲线。',
                '四基准均值 74.03%（+6.76）、4B 72.83%、跨视图点恢复 65.11% vs 16.02%，并直接对比 GPT-6-Astra 73.58%。',
                '首次在同规模开源骨干上把跨视图点恢复率从 16% 量级抬到 65%，且均值超过同期闭源最强空间模型。',
                'TRL=3：研究级管线，依赖多视图输入与已知相机声明。',
                'REP=4：基准、骨干、消融齐备；代码未见公开。'),
 '2611.30597': ('野外 3D 手部运动重建是手部交互的入口问题，−42% 的误差下降属量级改善。',
                '把手部深度从外观回归改成「测试相机射线上的几何约束求解」，用多关节对距离而非单一骨长定尺度，绕开对焦距与训练相机的依赖。',
                '整段射线拟合提供跨帧约束，8× 热图细化与置信门控融合分别处理定位精度与遮挡；实现链条较长但每步有据。',
                '野外 MPJPE-abs-p 56.55→32.59 mm、域内 24.46→19.62 mm，失败/误检帧占比 0.07%/0.11%（少 14.57×/8.82×）。',
                '用「射线约束 + 多关节对距离」替代单骨长先验，是本批方法层最干净的一处替换。',
                'TRL=3：依赖 VDM 先验与检测前端，长时序列与极端遮挡仍未覆盖。',
                'REP=4：与多个公开基线同协议对比，指标口径清楚。'),
 '2611.30461': ('实时虚拟试衣是消费级 XR/直播的直接用例，25 FPS 720p 已达可用线。',
                '把「显示时钟」与「生成时钟」解耦（光流 warp + 交叉淡化），让 400 ms/帧的扩散模型支撑相机帧率的镜子；数据侧用 parser 抠图自监督构造配对，绕开民族服饰缺 flat-lay 配对的瓶颈。',
                '给出逐阶段时延预算与「哪些加速会破坏印花」的实测，属少见的负向工程结论。',
                '720p 25 FPS、新帧 370–490 ms（RTX 4080 16 GB），LPIPS 0.137→0.077，长裤失败率 33%/32%→4.2%/2.5%。',
                '「双时钟」框架与 hem-aware 两遍掩码把两类不同失败（长衣盖裤、下摆以下重绘）分开解决。',
                'TRL=4：消费级单卡可跑，但仅覆盖上半身+下装，未处理多人、手部交互与遮挡进出。',
                'REP=3：给出数据集与指标，代码未见公开。'),
 '2611.30802': ('主动重建是家庭扫描/数字孪生的核心环节，本批把「房间级」推进到「多房间住宅级」。',
                '决策对象从单个 NBV 换成「目标 + 变长路径前缀」，用持久目标把走廊通行折算为远端房间的剩余价值；表面 cell 上记录「更新后缺陷 + 观测方向」做免渲染统一打分。',
                '把「不可约残差」作为目标释放条件，直接针对贪心 NBV 的结构性缺陷，而非调参。',
                'HSSD Cov10 74.1%→93.3%（PSNR +3.1 dB），HM3D 47.2%→95.6%（PSNR +11.7 dB、Chamfer 降 26.9×）；500 视图下 33 房间住宅 74.1%（基线 <20%）。',
                '在「预算受限 + 多房间长距离 transit」这一最不利设定上，把覆盖率从 <20% 抬到 74.1%，是结构性提升。',
                'TRL=3：仿真环境（HSSD/HM3D）验证，无真机扫描。',
                'REP=3：基准与预算设定清楚，代码未见公开。'),
 '2611.29236': ('稀疏视图几何质量决定 3DGS 能否直接用于展示与测量，本文提供的是「不改模型也涨点」的通路。',
                '把新视角几何改进重新表述为**选择性纠正**而非重建：不修改高斯表示、不重训骨干、不需要目标视角观测，只用同一冻结表示在不同视角下的误差互补性构造候选；准入用「期望绝对误差下降」而非「改进概率」，并从理论上证明代价加权 BCE 的零 logit 阈值与该准则对齐。',
                '给出 RIG 这一带留出相机实测深度的真实基准，可同时评静态与动态重建，补上了社区缺「真值深度」的短板。',
                'DTU AbsRel 0.0440→0.0180（DA3）/0.0418（Self），RIG 静态骨干平均降 10.2%/53.4%，动态骨干降 21.7–45.5%（4DGS −47.5%、Swift4D −63.9%）。',
                '零训练、零改动、零目标视角观测即可在四个骨干、静态与动态两类任务上一致涨点，性价比在本批最高。',
                'TRL=3：可作为后处理插件接入现有管线，但依赖同一表示的多次渲染成本。',
                'REP=4：给出理论证明 + 公开基准 RIG，复现路径明确。'),
 '2611.30572': ('视触觉世界模型是「合成数据能否替代真机采样」的关键一问，本文给出了带负结果的答案。',
                '触觉作为独立专家接入预训练视频 MoT，共享时间轴联合注意力实现视触同步生成；验证器把触觉真实性、接触力合理性与视触接触区间时间对齐联合起来，在动作提取前过滤。',
                '验证器放在「动作提取之前」而非策略训练之后，避免了迭代重训或仿真回放，工程上更可持续。',
                '五任务四策略平均 SR 19.4%→33.8%（Bo3 30.8%→48.8%）；**去掉验证器只有 22.9%**（与仅真实数据持平）；N0-VTLA 31.3%→51.7%、π0.5 19.7%→30.0%。',
                '首次用「去掉验证器即退回基线」的对照，把合成数据的增益来源钉在验证环节，而非数据量。',
                'TRL=3：真机任务验证，但任务数与物体类别仍少。',
                'REP=4：任务、策略、消融三组对照齐全。'),
 '2611.31156': ('新视图合成的成本随源视图数增长是规模化部署的硬约束，本文把成本与视图数解耦。',
                '把光栅化的「只处理可见图元」迁移到无显式几何的 transformer 渲染：router 在 decoder 之前预测目标视角会用到哪些 source token，一次排序服务所有预算、可在渲染时甚至帧间切换；用 cross-attention profile 上的 NMS 解决「同一表面被多视图重复编码」的预算浪费。',
                'NMS 去重复编码是针对注意力渲染的结构性浪费，而非单纯阈值剪枝。',
                '24 源视图、两视图量 token 下比 LagerNVS 快 6.4×（PSNR 仅低 0.68 dB）；固定预算 82–87 FPS（任意视图数）；4→24 视图本方法 PSNR +5.1 dB 而帧率仅降 6%（LagerNVS 慢 5.5×）。',
                '首次做到「帧率与源视图数近乎脱钩」，且 82–87 FPS 已进实时区。',
                'TRL=3：256×256 分辨率下的实时，高分辨率与动态场景未验。',
                'REP=3：与 LagerNVS 同协议对比，代码未见公开。'),
 '2611.28520': ('前馈重建的实用化取决于「一次前向能否同时给出深度与相机」，本文正面回答。',
                '关键洞察是视频 DiT 内部已编码深度与相机运动、只是「形式不对」：用片段级 shift 修正归一化逆深度、用多层特征直接回归相机，把迭代去噪式重建压成单次前向。',
                '相比只做深度的 DVD/GenCeption 联合输出相机；相比 Aether/Geo4D 不做迭代采样，定位清晰。',
                'ScanNet/TUM ATE 相对最好基线降 55.1%/56.3%，7-Scenes 重建误差 0.047→0.018（−61.7%），单帧 74–84 ms（GH200，含深度与相机）。',
                '在本批所有重建工作里速度优势最明显（比 Geo4D 快约 14×）且精度同时领先。',
                'TRL=3：需 GH200 级算力，消费级部署尚远。',
                'REP=3：多数据集同协议对比，代码未见公开。'),
 '2611.29163': ('手部姿态的「结构性缺失」长期被 2D 遮挡增广糊过去，本文把它做成一等设定与可复现基准。',
                '按解剖规则在 3D 上删 MANO 段再按原相机渲染，并保留被删关节参考位置用于受控评测；方法上把拓扑先验拆成特征层成对蒸馏（等价于约束关节间相对组织）与预测层沿链父子条件推理。',
                '「先删 3D 段再渲染」与 2D mask 增广有本质差别，基准本身即是贡献。',
                'IncNYU 重训 E_avg 8.00 vs 11.49（E_com −32.1%、E_inc −29.9%），NYU MPJPE 7.07（不牺牲完整手），NYU→IncNYU 不重训 E_avg 17.44（−5.58%）但 E_inc 33.40 仍高于 HandR2N2 的 26.36。',
                '在「缺失手」子集上把误差降三成而不损完整手精度，且不重训的跨域设定也有效。',
                'TRL=2：基准与方法均为研究级，未涉及实时部署。',
                'REP=4：给出可复现基准与完整消融。'),
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
s_('- 主批 %d 篇：A %d / B %d / C %d（C 级仅入馆、不写笔记）' % (len(MAIN), GRM['A'], GRM['B'], GRM['C']))
s_('- backfill %d 篇：A %d / B %d' % (len(BF), GRB['A'], GRB['B']))
s_('- 全批：A %d / B %d / C %d，**0 S**' % (GR['A'], GR['B'], GR['C']))
s_('\n## 三、Top10 逐维评分理由（10 篇）\n')
for p in TOP:
    s_('### %s %s（%.2f / %s / %s）\n' % (p['id'], p['title_zh'], p['value'], p['grade'], p['track']))
    sc = p['scores']
    for k in ('IMP', 'NOV', 'TEC', 'EXP', 'PER', 'TRL', 'REP'):
        s_('- **%s=%d**：%s' % (k, sc[k], WHY[p['id']][('IMP', 'NOV', 'TEC', 'EXP', 'PER', 'TRL', 'REP').index(k)]))
    s_('')
s_('\n## 四、backfill 逐篇理由（6 篇）\n')
for p in BF:
    sc = p['scores']
    s_('### %s %s（%.2f / %s / 首发 %s）\n' % (p['id'], p['title_zh'], p['value'], p['grade'], p['published']))
    s_('- 向量：IMP %d / NOV %d / TEC %d / EXP %d / PER %d / TRL %d / REP %d' % (
        sc['IMP'], sc['NOV'], sc['TEC'], sc['EXP'], sc['PER'], sc['TRL'], sc['REP']))
    s_('- 要点：%s' % LABEL.get(p['id'], '—'))
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
    s_('| %s | %s | %s | %d | %d | %d | %d | %d | %d | %d | %.2f | %s | %s |' % (
        p['id'], p['title_zh'][:28].replace('|', '/'), p['track'], sc['IMP'], sc['NOV'], sc['TEC'],
        sc['EXP'], sc['PER'], sc['TRL'], sc['REP'], p['value'], p['grade'], LABEL.get(p['id'], '—')))
s_('\n> 要点列取自 `scripts/build_scored_%s.py` 的行内注释（唯一实现，未二次转录）。' % MMDD)
s_('> 逐维展开只对 Top10 给出；其余篇目的档位由同一权重与 `grade_caliber.assign_grade` 机械计算，不参与 Top10 排序说明。\n')
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
r('- 第 1 步 对账：`scripts/audit_listing_1125.py`（PREV_DAY=11-23 / NEW_DAYS=11-24,11-25 / 窗口下界 2026-11-23），'
  '7/7 分类成功、exit 0；%s 组 **%s 槽位 / %s 唯一**；11-25 组 declared=None（未释放）；'
  '11-23 组复采 declared=got（171/5/13/4/89/214/10）。' % (
      ANN, format(AG['slots'], ','), format(AG['unique'], ',')))
r('- 第 2 步 数据源：API 双主机探针 200（仅用于提交日核验）；RSS 7/7、**1,547 条**，WROTE=1547 OK_CATS=7/7。'
  'listing %s/%s 覆盖 → 免 id_list。' % (format(AG['unique'], ','), format(AG['unique'], ',')))
r('- 第 3 步 甄别：`triage_1125.py`（数据源 `_all_full.jsonl` 1547 条 no-filter 全量，只取 day=11-24 的 newday）'
  '→ 覆盖率 1.0000（1045/1045）、KW %d + TITLE_EXTRA %d = 池 %d → `triage_decide_1125.py` 逐篇判读剔 %d → %d。' % (
      G['recall']['kw_hits'], G['recall']['title_extra'], G['recall']['pool'],
      G['recall']['rejected_from_pool'], G['recall']['pool'] - G['recall']['rejected_from_pool']))
r('- 第 3 步补充 backfill：502 条 `replace` 条目中未入馆且摘要级 XR 命中 %d 篇，逐篇核摘要取 %d 篇。' % (len(OLD), len(BF)))
r('- 第 3.5 步 残差：`residual_scan.py dump/ingest` → 5 批（4×190 + 139）并行盲评，扫描 **%d**、判 **%d**（**%.2f%%**）、'
  '采纳 **%d** → 主批 %d。踩坑：ingest 的 rate 分母是 `verdicts.jsonl` **行数**而非 nonxr 总数，'
  '先把 899 条逐条写入（命中写 `verdict=1`、其余写 `verdict=0`）才得到 2.45%%；'
  '若只写命中行，分母会退化成 22 而得 100%%。' % (
      RES['n_scanned'], RES['n_flagged'], RES['rate'] * 100, G['recall']['residual_adopted'], len(MAIN)))
r('- 第 4 步 全文：74 篇串行 3 s/篇 → **72 L0/FULL + 2 L1/PARTIAL**（2611.29647 5,105 字符、2611.30012 4,581 字符，'
  'ar5iv 仅返回摘要落地页，手动改判 PARTIAL 并同步 `.txt` 头）；字符 %s–%s。' % (
      format(min(MAN[p['id']]['chars'] for p in D), ','), format(max(MAN[p['id']]['chars'] for p in D), ',')))
r('- 第 4 步补充 提交日核验：`check_published_1125.py`（25 id/批 + 12 s 间隔）→ 74/74 全齐；'
  '主批 %s。踩坑：`_ids_1125_clean.txt` 是换行分隔（上批为逗号分隔），派生脚本的读取方式需改为 `.read().split()`。' % pub_dist(MAIN))
r('- 第 5 步 评分：6 组子代理 digest（13/13/13/13/13/9 = 74）+ 主会话按标准权重重算 74 篇；'
  '评分要点取自 `build_scored_1125.py` 行内注释，Top10 逐维理由落 `papers/daily/%s/scored.md`。' % DATE)
r('- 第 6 步 三关：门① %.3f（%s vs %s）；门② %d 赛道（未重筛）；门③ %.2f vs %.3f，margin %+.3f '
  '→ heavy_day_raw=false、blockbuster=false、s_awarded=false。' % (
      g1['max_jaccard'], g1['pair'][0], g1['pair'][1], g2['n_tracks'],
      g3['today_max'], g3['top10_mean'], g3['margin']))
r('- 第 7 步 Top10：实数 10 篇（4.21–3.92），全部 A；全批 A %d / B %d / C %d，0 S。' % (GR['A'], GR['B'], GR['C']))
r('- 第 8 步 产物：报告 2 + 笔记 72（C 级 2 篇不写）+ MOC 2 + 总索引刷新 + 7dim-table（主批/backfill 各 1）+ scored.md + run_log；'
  'registry 1,132 → **1,206**（备份 `papers/library/registry.jsonl.bak-20261125`）。'
  '易错点：`7dim-table.md` 表头必须保留 `arXiv` 列，否则前端批次卡表内计数为 0。')
r('- 第 9 步 发布：见下方发布记录（构建 → `node --check` → CDP 冒烟 → `check_release` → 提交 → 推送 → Pages 核验）。')
open('papers/daily/%s/run_log.md' % DATE, 'w', encoding='utf-8').write('\n'.join(RL) + '\n')
print('run_log ok')
