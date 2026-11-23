# -*- coding: utf-8 -*-
"""2026-11-24 最终解读报告 + backfill 报告 + run_log。"""
import glob, json, os, re, shutil

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
os.chdir(ROOT)
DATE, MMDD = '2026-11-24', '1124'
ANN = '2026-11-23'

D = json.load(open('data/scored_%s.json' % MMDD, encoding='utf-8'))
G = json.load(open('data/gates_%s.json' % MMDD, encoding='utf-8'))
RES = json.load(open('data/residual_%s.json' % MMDD, encoding='utf-8'))
PUB = json.load(open('data/published_%s.json' % MMDD, encoding='utf-8'))
MAN = json.load(open('data/fulltext/_manifest.json', encoding='utf-8'))
AUD = json.load(open('data/audit_1124_days.json', encoding='utf-8'))
XR = json.load(open('data/xr_pool_1124.json', encoding='utf-8'))
CAND = json.load(open('data/cand_1124.json', encoding='utf-8'))
BFJ = json.load(open('data/backfill_1124.json', encoding='utf-8'))
MX = json.load(open('data/missed_xr_1124.json', encoding='utf-8'))

MAIN = [p for p in D if not p['batch'].startswith('backfill')]
BF = [p for p in D if p['batch'].startswith('backfill')]
TOP = [p for p in D if p['in_top10']]
TOP.sort(key=lambda r: (-r['value'], -r['scores']['IMP'], -r['scores']['NOV'], r['id']))
g3, g2, g1 = G['gate3'], G['gate2'], G['gate1']


def concl(pid):
    f = glob.glob('papers/notes/%s__*.md' % pid)
    txt = open(f[0], encoding='utf-8').read()
    m = re.search(r'## 一句话结论\n(.+?)\n\n', txt, re.S)
    return m.group(1).strip()


def bl(items):
    if isinstance(items, (list, tuple)):
        return '\n'.join('- ' + str(x) for x in items)
    return '\n'.join('- ' + x.strip() for x in re.split(r'[；。]', str(items)) if x.strip())


def slots(day):
    n = 0
    for cat in AUD:
        v = AUD[cat]['new'].get(day) or AUD[cat]['prev']
        if v['day'] == day:
            n += v['got']
    return n


L = []
A = L.append

A('# XR 每日论文雷达 · %s\n' % DATE)
A('> **诚实口径**：本批处理的是 **2026-11-23（周一）公告批次**，拉取时刻为 **2026-11-24 02:30（北京时间）**。'
  '11-21 与 11-22 为周末 `skipDays`，listing 无对应公告段；本批**不含任何「周一日内新增」以外的稿件**。'
  'arXiv 公告日 ≠ 拉取日 ≠ 首次提交日：主批 API `published` 核验为 **11-20×34 / 11-19×7**，'
  'RSS 的 `published` 字段是公告时间戳，不能当提交日使用。\n')
A('> 覆盖范围：cs.CV / cs.GR / cs.HC / cs.MM / cs.RO / cs.AI / eess.IV 七分类 listing（show=500 单页，declared=got 逐分类核对）。'
  '11-23 组 **506 槽位 / 404 篇唯一**，全部命中 RSS 639 条（缺收 0），故摘要级覆盖率 1.0000。\n')

# ---------------- 一、执行摘要 ----------------
A('\n## 一、执行摘要\n')
A('**本批 50 篇（主批 41 + backfill 9），0 S / 31 A / 19 B；Top10 实数 10 篇，最高 4.27（2611.26744 forth / '
  '2611.27290 EgoLAM / 2611.27963 非穿透世界模型，三篇并列）。**'
  ' 门③ 现算：当日最高 4.27 vs 库内近 30 天 Top10 均分 **4.432**（464 条入窗，半开窗口 [2026-10-25, 2026-11-24)，'
  '按 batch 剔除本次追加两批），margin **−0.162** → `heavy_day_raw=false`、`blockbuster=false`，'
  '**本批无 S 级**；3 篇 4.27 虽过 4.20 线，仍按口径一律记 A（skill §8.6.3）。\n')
A('当日四条主线：\n')
A('1. **触觉从「信号」被推到「可判定的物理量」**：2611.26744 forth 把触觉 VLA 的适配与滑移门控全部压在纯前向路径'
  '（Forward-Forward + 零阶）上，冻结 4-bit 骨干仍达 LIBERO 97.6%，而峰值显存只有反传的 1/7.12、'
  '滑移门控夹持力 0.77 N 对 reflex ramp 的 22.43 N；2611.26764 TacHOI 更激进——把「已标定手 + 空间分离的实测接触」'
  '当物理卡尺，无模板、无深度、无训练即把 ARCTIC ADD-S* 从最近基线的 15.6 cm 压到 3.6 cm；'
  '而 2611.26883 TouchBench 给出反面证据：四个 VLM 在不可见物理属性上 Tier B 相对准确率仅 **49.8%（近随机）**。'
  '三篇合起来说明：**触觉在 XR/机器人里的瓶颈已不是传感器，而是「表征与判据」**。\n')
A('2. **世界模型开始显式建模物理约束，而非寄望于隐式涌现**：2611.27963 证明生成器隐状态里**已经**含碰撞信息，'
  '只需极小读出即可把六模型平均违规率从 74% 降到 16%（LingBot 89%→4%），Pred 模式每条仅多 0.7 s；'
  '2611.26981 ViewDreamer 用块间共享 slot 把「逐视角生成」与「跨视角交互」解耦，真机 Franka 闭环 67.5% 对 30.0%；'
  '2611.27513 Ego4Gen 把接口从视频潜变量换成「几何 + 运动」token，RoboTwin Hard 51%/37% 而两个基线皆为 0%。\n')
A('3. **数据与评估基础设施继续补齐，且开始「自证精度」**：2611.26916 RoboCap-10k 是首个单设备逐 session 在线标定、'
  '同时带度量头部位姿与 3D 手部标注的万小时级语料（10,000 h / 137.8 万 episodes，ATE 中位 3.0 mm、'
  '手部 PA-MPJPE 4.5 mm）；2611.26937 则把「看着对不等于几何对」量化：同一视频的密集重建几何分 75.9，'
  '而 GPT-6 Astra 仅 51.4，中位绝对尺度误差 4.6–10.4%。**评估侧的负结果，比又一个 SOTA 更能界定 XR 的真实能力面**。\n')
A('4. **效率与工程落地同日推进**：2611.27525 PennyGS 在 RTX 3060 上把全分辨率 Mip-NeRF 360 单场景训练从 LiteGS 的'
  '34m08s 压到 **6m25s**（峰值显存 1.04 GB），靠的不是单点 kernel 而是逐阶段消除「冗余像素 / 冗余字节 / 冗余 pass」；'
  '2611.26779 Tracktail 完全不用深度输入做多视角 3D 点跟踪，Panoptic AJ 86.5 已超带 GT 深度的 MVTracker（84.2）；'
  '2611.26730 SparseHPS 用一套权重同时服务深度相机与 LiDAR，单帧即超已发表的 32 帧序列方法。\n')
A('**筛选与复核**：摘要级 KW 命中 75 篇（含标题级扩展词补扫），逐篇核摘要剔 **42 篇**（遥感/测绘/林业与工业巡检 6、'
  '医学与生物成像 5、通用 LLM 与空间推理 11、机器人控制与自动驾驶 11、眼动与通用视觉 9），得 **33 篇**；'
  '第 3.5 步残差复核扫描 **371 条**、判 **8 条**应收录（**2.2%**），8 篇全部采纳 → **主批 41 篇**。'
  '上一公告组（11-20 组 508 篇唯一、未入馆 471 篇）复采核验：摘要/标题级命中 43 篇**全部已在上批处置集合内**，'
  '**0 漏网**，无需 backfill 补漏（`data/missed_xr_1124.json` 为空）。\n')

# ---------------- 二、Top10 ----------------
A('\n## 二、Top10 排行榜\n')
A('| 排名 | 论文 | 赛道 | 总分 | 档 | 证据 | 关键贡献 |')
A('|---|---|---|---|---|---|---|')
SHORT = {
 '2611.26744': '纯前向触觉 VLA：LIBERO 97.6% 追平反传，显存 1/7.12、延迟 1/2、滑移门控夹持力 1/29。',
 '2611.27290': '以实测手腕位姿监督潜动作瓶颈，LIBERO 79.38%（专家 BC +28.73 点），并给出 AD/IC 诊断指标。',
 '2611.27963': '非穿透写成无几何世界模型的约束问题：六模型平均违规率 74%→16%，每条仅多 0.7 s。',
 '2611.26764': '标定手 + 实测接触当物理卡尺，免训练破解单目尺度歧义：ARCTIC ADD-S* 3.6 cm（基线 15.6 cm）。',
 '2611.26981': '块间共享 slot 解耦逐视角生成与跨视角交互：3 视角 FVD 25.41 对 32.93，真机 67.5% 对 30.0%。',
 '2611.26779': '首个免深度输入的多视角 3D 点跟踪：Panoptic AJ 86.5，超带 GT 深度的 MVTracker（84.2）。',
 '2611.26883': '把「视觉可答性」做成受控变量：VLM 在不可见物理属性上 49.8%（近随机），统计量文本接口零样本 62.9%。',
 '2611.26916': '万小时级度量精确自我中心语料：10,000 h / 137.8 万 episodes，ATE 3.0 mm、手部 4.5 mm。',
 '2611.27525': '逐阶段消除三类冗余：RTX 3060 全分辨率 3DGS 训练 6m25s（LiteGS 34m08s），显存 1.04 GB。',
 '2611.26730': '一套权重同时服务深度相机与 LiDAR：SLOPER4D 关节误差 28.6 mm（BMLiCap 36.5 mm）。',
}
for i, p in enumerate(TOP, 1):
    A('| %d | %s（%s） | %s | **%.2f** | %s | %s | %s |' % (
        i, p['title_zh'], p['id'], p['track'], p['value'], p['grade'], p['evidence'], SHORT[p['id']]))
A('\n> **门② 未触发重筛**：纯值 Top10 已覆盖 **7 赛道**（触觉与多模态 3、世界模型与仿真 2、具身交互 1、重建与SLAM 1、'
  '评估与数据集 1、神经渲染 1、化身与人体 1），全批 11 赛道。\n')
A('> **无 OUTDATED / SUPERSEDED 标记**：本批未发现「同问题更优且更晚」的直接取代关系。'
  '9 篇 backfill 均为 2026-01 至 2026-11 的旧稿 v2 再公告（详见独立 backfill 报告），'
  '其中 2609.31248 TailorGS（2026-09-25 首发）与 2605.19257 PRISM-SLAM（2026-05-19 首发）已在其笔记中标注「时效性风险」，'
  '但未达论文级 OUTDATED 证据门槛。\n')

# ---------------- 三、逐篇深度解读 ----------------
A('\n## 三、逐篇深度解读\n')
DIG = {}
for k in range(1, 5):
    for r in json.load(open('data/digest_%s_g%d.json' % (MMDD, k), encoding='utf-8')):
        DIG[r['id']] = r
for i, p in enumerate(TOP, 1):
    g = DIG[p['id']]
    A('\n### 第 %d 章 %s（%s · %s · %.2f %s）\n' % (i, p['title_zh'], p['id'], p['track'], p['value'], p['grade']))
    A('**一句话结论**：%s\n' % concl(p['id']))
    A('**要解决的问题**\n\n%s\n' % g['problem'])
    A('**方法详解**\n\n%s\n' % g['method'])
    A('**实验与结果**\n\n%s\n' % bl(g['key_numbers']))
    A('**创新点与贡献**\n\n%s\n' % bl(g['novelty']))
    A('**局限与风险**\n\n%s\n' % bl(g['limitations']))
    rel = '- 本批新增（batch `%s`，公告类型 `%s`），赛道「%s」。' % (p['batch'], p['announce'], p['track'])
    if p.get('recall') == 'RESIDUAL':
        rel += '\n- **由第 3.5 步残差复核捞回**：摘要级 KW 与标题级扩展词均未命中，说明现有词表对该表述存在语义缺口。'
    if p.get('note'):
        rel += '\n- 备注：%s' % p['note']
    rel += '\n- 与库内同赛道论文构成并列参考；本批 OUTDATED/SUPERSEDED 判定为 0。'
    A('**与文献库的关系**\n\n%s\n' % rel)
    A('**可复现性**\n\n- 代码/项目页：%s\n- 全文证据：%s（%s，%s 字符，%s）\n' % (
        p.get('code') or '正文未提供', p['evidence'], MAN[p['id']]['level'],
        format(MAN[p['id']]['chars'], ','), MAN[p['id']]['url']))
    act = '- 纳入重点精读：方法与实验节可直接支撑选题与技术选型。' if p['grade'] == 'A' else '- 浏览级。'
    if p.get('code') and p['code'] not in ('未提供', '无'):
        act += '\n- 有公开代码/项目页，可先跑通再评估迁移成本。'
    else:
        act += '\n- 未提供代码，复现需按正文细节自行实现。'
    if p['value'] >= 4.20:
        act += '\n- 达 S 线（≥4.20）而本批门③ 判定非重磅日（margin −0.162）：值得优先读，但不宜按 S 级对外表述。'
    A('**行动建议**\n\n%s\n' % act)

# ---------------- 四、7 维表 ----------------
A('\n## 四、当日全量 7 维度对比表\n')
A('权重：IMP 0.20 · NOV 0.20 · TEC 0.15 · EXP 0.15 · PER 0.15 · TRL 0.08 · REP 0.07；'
  '档位：S ≥4.20 且 blockbuster，A 3.60–4.20，B 3.00–3.60，C <3.00（仅入馆不解读）。完整表见 '
  '[papers/daily/%s/7dim-table.md](../papers/daily/%s/7dim-table.md)。\n' % (DATE, DATE))
A('| # | arXiv | 论文 | 赛道 | IMP | NOV | TEC | EXP | PER | TRL | REP | 总分 | 档 |')
A('|---|---|---|---|---|---|---|---|---|---|---|---|---|')
for i, p in enumerate(MAIN, 1):
    s = p['scores']
    A('| %d | %s | %s | %s | %d | %d | %d | %d | %d | %d | %d | **%.2f** | %s |' % (
        i, p['id'], p['title_zh'][:34].replace('|', '/'), p['track'], s['IMP'], s['NOV'], s['TEC'],
        s['EXP'], s['PER'], s['TRL'], s['REP'], p['value'], p['grade']))

# ---------------- 五、覆盖率校验 ----------------
A('\n## 五、覆盖率校验与筛选过程\n')
A('### 5.1 漏网对账（第 1 步，先于拉取）\n')
A('- 7 分类最新公告日均为 **2026-11-23（周一）**；11-21、11-22 为周末，`declared=None` 且 got=0；'
  '11-24 组尚未公告（本批拉取于 11-24 02:30，早于当日 00:00 UTC 释放）。\n')
A('- 11-23 组逐分类 declared=got：cs.CV 171 / cs.GR 5 / cs.HC 13 / cs.MM 4 / cs.RO 89 / cs.AI 214 / eess.IV 10 '
  '= **506 槽位**，唯一论文 **404 篇**（跨列表重复 102）。上一公告组（11-20）复采 **605 槽位 / 508 唯一**、'
  '逐分类 declared=got。\n')
A('- 上一公告组（11-20）未入馆 **471 篇 = 508 − 37（上批主批已入馆）**；用 11-19/11-20/11-21/11-24 四份 RSS 全量核摘要，'
  '471/471 全覆盖，摘要/标题级命中 **43 篇全部落在上批处置集合（`nonxr_1121` ∪ `xr_pool_1121` ∪ `rejected` ∪ '
  '`backfill_pool_1121` ∪ `scored_1121`）** → **0 漏网**（`data/missed_xr_1124.json` 为空对象）。\n')
A('### 5.2 数据源与召回\n')
A('- RSS 7 分类 `--no-filter` 去重 **639 条**（`WROTE=639`、`OK_CATS=7/7`，完整采集）。'
  'listing 404 篇 **100% 被 RSS 覆盖（缺收 0）** → 免 API `id_list`，规避 429 静默丢批；'
  'API 仅用于 50 篇的提交日核验（50/批，3 chunk，12 s 间隔）。\n')
A('- 召回三层：摘要级 KW + **标题级扩展词补扫** = **75 篇命中** → 逐篇核摘要剔 **42 篇**'
  '（明细见 `data/nonxr_1124.json`）→ **33 篇**；残差复核采纳 8 篇 → **主批 41 篇**。'
  '命中类别分布：cs.CV 31 / cs.RO 17 / cs.GR 2。\n')
A('- 剔除 42 篇的五组构成：**遥感/测绘/林业/风电与工业巡检 6**（如 2611.26715 林业单株分割、2611.27407 风机叶片重建、'
  '2611.27383 全空域 UAV 跟踪）；**医学与生物成像 5**（3D MRI 表征、OCTA、肿瘤跟踪、犬类姿态模型）；'
  '**通用 LLM 与空间推理 11**（空间查询可验证奖励、Qwen3-VL 手写公式、长视频记忆 agent、网络搜索趋势）；'
  '**机器人控制与自动驾驶 11**（VLA 不完整动作、人形单目姿态、GGDriver 自驾、世界模型策略梯度）；'
  '**眼动与通用视觉 9**（GAZEAIDE 编码场景、CoGITAtion 眼动、风格化、并行多重网格）。'
  '误命中主因是 `depth` / `tracking` / `spatial` / `gaze` / `hand` / `mesh` / `sdf` / `affine` 等泛词与上述场景共现。\n')
A('### 5.3 第 3.5 步残差复核（只报警，不入馆）\n')
A('残差复核：扫描 **%d** 条，疑似漏检 **%d** 条（**%.1f%%**），采纳 **8** 条。\n' % (
    RES['n_scanned'], RES['n_flagged'], RES['rate'] * 100))
A('| # | arXiv | 标题 | 赛道 | 处置 |')
A('|---|---|---|---|---|')
ADOPT = {f['id'] for f in RES['flagged']}
for it in RES['flagged']:
    A('| %d | %s | %s | %s | %s |' % (it['n'], it['id'], it['title'][:62].replace('|', '/'), it['track'],
                                     '**采纳入本批**' if it['id'] in ADOPT else '留待人工挑选池'))
A('\n> 采纳口径：8 篇**全部**为 12 赛道内的核心表述（世界模型与仿真 4、化身与人体 2、重建与SLAM 1、系统与平台 1），'
  '且与已入馆条目无同质（门① 复算 max Jaccard %.3f）。清单本身只作报警，**未直接并入 registry**——'
  '8 篇均另行走「全文抓取 → 7 维评分 → 产物」全流程后才入馆。残差率 2.2%%，连续两批（上批 1.6%%）远低于 12%% 阈值，'
  '词表不重估。\n' % g1['max_jaccard'])
A('### 5.4 三关\n')
A('| 关卡 | 口径 | 本批数值 | 结论 |')
A('|---|---|---|---|')
A('| 门① 同质度 | 与库内非本批条目最大 Jaccard < 0.62 | **%.3f**（%s vs 库内 %s） | PASS |' % (
    g1['max_jaccard'], g1['pair'][0], g1['pair'][1]))
A('| 门② 赛道覆盖 | Top10 覆盖 ≥5 赛道 | **%d 赛道**（%s） | PASS（未重筛） |' % (
    g2['n_tracks'], '、'.join('%s×%d' % (k, v) for k, v in g2['top10_tracks'].items())))
A('| 门③ 价值天花板 | today_max ≥ 近 30 天 Top10 均分，且 margin ≥ 0.05 才授 S | **%.2f vs %.4f**，margin **%+.4f** | 非重磅日，**blockbuster=false** |' % (
    g3['today_max'], g3['top10_mean'], g3['margin']))
A('\n> 门③ 留痕（`data/gates_%s.json`）：`window_lo=%s`、`window_hi=%s`、`window_excludes_today=%s`、'
  '`window_excludes_this_run_batches=%s`、`this_run_batches_excluded=%s`、`heavy_day_raw=%s`、`heavy_day=%s`、'
  '`margin=%.4f`、`blockbuster=%s`、`s_awarded=%s`；入窗 **%d 条**。\n' % (
      MMDD, g3['window_lo'], g3['window_hi'], g3['window_excludes_today'],
      g3['window_excludes_this_run_batches'], '、'.join(g3['this_run_batches_excluded']),
      g3['heavy_day_raw'], g3['heavy_day'], g3['margin'], g3['blockbuster'],
      g3['s_awarded'], g3['in_window']))
A('> 门③ 窗口为**半开区间** [今天−30 天, 今天)，且按 batch 剔除本次运行追加的两批（`2026-11-24`、`backfill-1124`）；'
  '该项自 2026-11-18 起实施，历史数值不回算。\n')
A('### 5.5 评分披露（影响档位与可信度的三处判定）\n')
A('- **2611.27633 Instant-LIVO 记 PARTIAL**：`fetch_fulltext.py` 初判 L1/FULL，但 4,993 字符实为 ar5iv 摘要落地页'
  '（`https://arxiv.org/html/2611.27633v1` 返回 **404**，正文无 Introduction / Method / Results 节）。'
  '已手动改判 `evidence=PARTIAL`，TEC=2、EXP=3，并要求子代理只按摘要级证据作答——其笔记与本章均标注该限制。'
  '**这是本批唯一非 FULL 证据**，不参与任何「方法细节」断言。\n')
A('- **2611.26937 与 2611.26992 的 PER 记「诊断力」而非性能增益**：前者是评测论文（无新方法），后者是纯理论工作'
  '（正文零实验，EXP=1、PER=2、TRL=1）。两者档位仍为其分数所对应的 B 级，不因选题重要而上调。\n')
A('- **3 篇 4.27 未授 S**：门③ 机械判定 `today_max 4.27 < 4.432`，`heavy_day_raw=false` 即 `blockbuster=false`；'
  '按 `grade_caliber.assign_grade` 的单一实现，S 需「≥4.20 且 blockbuster」，故三篇并列第一均记 A。'
  '**未做任何人工上调**——本批与 11-21（margin +0.007 险过）不同，差值为 −0.162，属明确非重磅日。\n')

# ---------------- 六、附录 ----------------
A('\n## 六、附录\n')
A('### 6.1 全文抓取与证据等级\n')
from collections import Counter  # noqa: E402
lv = Counter(MAN[p['id']]['level'] for p in D)
ev = Counter(MAN[p['id']]['evidence'] for p in D)
A('- 50 篇（41 + 9）串行 3 s/篇（`scripts/fetch_fulltext.py`）：**%s**；证据 **%s**；字符数 %s–%s。\n' % (
    ' / '.join('%s %d' % (k, v) for k, v in sorted(lv.items())),
    ' / '.join('%s %d' % (k, v) for k, v in sorted(ev.items())),
    format(min(MAN[p['id']]['chars'] for p in D), ','),
    format(max(MAN[p['id']]['chars'] for p in D), ',')))
A('- 49 篇 FULL：逐篇抽看含 Introduction / Method / Experiments 正文节（最少约 2.5 万字符，远超 ar5iv 摘要页 ~5k 量级）。'
  '唯一 PARTIAL 为 2611.27633，原因见 §5.5。\n')
A('### 6.2 本批数据文件\n')
A('- `data/audit_1124_days.json` / `audit_1124_alldays.json`：对账原始记录（7 分类日期头、declared/got）\n'
  '- `data/newday_1124.json`（404 篇唯一）、`data/missed_prev_1124.json`（471）、`data/missed_xr_1124.json`（空）\n'
  '- `data/xr_pool_1124.json`（75）、`data/cand_1124.json`（33）、`data/backfill_1124.json`（9）、`data/nonxr_1124.json`（371）\n'
  '- `data/residual_1124.json` + `data/residual_1124/{index,verdicts}.jsonl`（371 条逐条判定）\n'
  '- `data/published_1124.json`、`data/scored_1124.json`、`data/gates_1124.json`、`data/why_1124.json`\n'
  '- `data/digest_1124_g1..g4.json`（50 篇精读 digest）、`data/fulltext/<id>.txt` + `_manifest.json`\n')
A('### 6.3 待办与风险\n')
A('- **硬件显示侧连续第 35 批无器件级破冰**：本批「渲染与显示」赛道 0 篇，`空间计算与UI` 仅 1 篇（3D 标注布局质检）。'
  '触觉硬件只有 2611.26950（机理分析，TRL=1、无样机）与 backfill 的 2601.13574（本体感知膜，TRL=3）。'
  '波导 / 可变焦 / Maxwellian / 光场显示方向仍需外部追踪或会议渠道补充。\n')
A('- **残差率 2.2%**（上批 1.6%、再上批 2.8%），连续三批低于 12% 阈值；本批 8 条采纳全部来自「世界模型/化身」表述，'
  '说明缺口集中在 `world model` 与 `avatar` 的语义边界，而非词表整体失效。\n')
A('- **PARTIAL 处理需固化**：ar5iv 对部分新稿只返回摘要落地页，`chars` 在 4–6k 区间时应直接判 PARTIAL 而非 FULL。'
  '下批拟在 `fetch_fulltext.py` 增加「chars < 8000 且命中 landing 特征 → 强制 PARTIAL」的守卫。\n')

open('reports/XR-Daily-Report-%s.md' % DATE, 'w', encoding='utf-8').write('\n'.join(L) + '\n')
print('main report', len('\n'.join(L)))

# ---------------- backfill 报告 ----------------
B = []
b = B.append
b('# XR Backfill 报告 · backfill-%s\n' % MMDD)
b('> **非当日新提交**：本批 9 篇均为 2026-11-23 公告 RSS 混入的 `replace` 类旧稿再公告，首次入馆。'
  '按诚实口径单独编号，**不参与当日重磅日判定**，≥4.20 亦记 A。\n')
b('> 原始首次提交日（API `published`）：2611.21057 = **2026-11-16**（v2 于 11-20 更新）；2611.25417 = **2026-11-19**；'
  '2609.31248 = **2026-09-25**；2609.08848 = **2026-09-08**；2607.02921 = **2026-07-03**；2606.16202 = **2026-06-15**；'
  '2605.19889 与 2605.19257 = **2026-05-19**；2601.13574 = **2026-01-20**。\n')
b('\n## 一、摘要\n')
b('11-23 公告 RSS 共 235 篇未入馆 `replace` 旧稿，摘要级 XR 命中 18 篇，逐篇核摘要后取 **9 篇**'
  '（其余 9 篇为机器人操作、医学影像、点云检测、通用视觉等非 XR 方向）。定稿 **7 A / 2 B，无 S**。\n')
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
    b('**可复现性**\n\n- 代码/项目页：%s\n- 全文证据：%s（%s，%s 字符）\n- 首发提交日 %s（本批为 v2 再公告）\n' % (
        p.get('code') or '正文未提供', p['evidence'], MAN[p['id']]['level'],
        format(MAN[p['id']]['chars'], ','), p['published']))
b('\n## 三、完整 7 维表\n')
b('见 [papers/daily/backfill-%s/7dim-table.md](../papers/daily/backfill-%s/7dim-table.md)。\n' % (MMDD, MMDD))
open('reports/XR-Backfill-Report-backfill-%s.md' % MMDD, 'w', encoding='utf-8').write('\n'.join(B) + '\n')
print('backfill report', len('\n'.join(B)))

# ---------------- run_log ----------------
u_c = shutil.disk_usage('C:/'); u_d = shutil.disk_usage('D:/')
RL = []
r = RL.append
r('# 运行日志 · %s\n' % DATE)
r('- 02:30 起跑；跑前查 C: 盘剩余空间（未触发磁盘保护）。收尾实测 C: %.2f GB / D: %.2f GB。' % (
    u_c.free / 2**30, u_d.free / 2**30))
r('- 第 1 步 对账：`scripts/audit_listing_1124.py`（PREV_DAY=11-20 / NEW_DAYS=11-21..11-24），7/7 分类成功，exit 0；'
  '11-23 组 506 槽位 / 404 唯一；11-21、11-22 declared=None（周末 skipDays）；11-20 组复采 605 槽位 / 508 唯一、declared=got。')
r('- 第 2 步 数据源：API 双主机探针 200（仅用于提交日核验）；RSS 7/7、639 条，WROTE=639。listing 404/404 覆盖 → 免 id_list。')
r('- 第 3 步 甄别：`triage_1124.py` → KW + TITLE_EXTRA 共 75 → `build_cand_1124.py` 逐篇判读剔 42 → 33（主批）+ 9（backfill）。')
r('- 第 3.5 步 残差：`residual_scan.py dump/ingest` → 扫描 371、判 8（2.2%）、采纳 8 → 主批 41。'
  '踩坑：首版 `verdicts.jsonl` 只写 14 行（8 采纳 + 6 拒绝），ingest 分母取判定行数得 57.1%；补齐 371 行后得 2.2%。')
r('- 第 4 步 全文：50 篇（41+9）串行 3 s/篇，49 L0/FULL + 1 L1/PARTIAL（2611.27633：arXiv HTML v1 404、ar5iv 仅摘要落地页，'
  '手动改判 PARTIAL）；字符 %s–%s（FULL 篇最小 %s）。' % (
      format(min(MAN[i]['chars'] for i in {q['id'] for q in D}), ','),
      format(max(MAN[p['id']]['chars'] for p in D), ','),
      format(min(MAN[p['id']]['chars'] for p in D if MAN[p['id']]['evidence'] == 'FULL'), ',')))
r('- 第 4 步补充 提交日核验：`check_published_1124.py`（id_list 50/批 + 12 s 间隔）→ 50/50 全齐；'
  '主批 11-20×34 / 11-19×7。踩坑：`_ids_1124.txt` 首行混入计数数字 42，改用正则过滤后的 `_ids_1124_clean.txt`。')
r('- 第 5 步 评分：4 组子代理 digest（11/11/11/17 篇）+ 主会话按标准权重重算 50 篇；'
  '评分理由落 `data/why_1124.json`，并由脚本正则校验 50 条 `X=n` 与评分表逐维一致（0 处不一致）。')
r('- 第 6 步 三关：门① 0.40（2609.31248 vs 库内 2611.02044）；门② 7 赛道（未重筛）；'
  '门③ 4.27 vs 4.432，margin −0.162 → heavy_day_raw=false，blockbuster=false，无 S。')
r('- 第 7 步 Top10：实数 10 篇（4.27–3.92），全部 A；本批无 C 级（入池门槛已把 C 级挡在候选外）。')
r('- 第 8 步 产物：报告 2 + 笔记 50 + MOC 2 + 总索引 + 7dim-table（主批/backfill 各 1）+ scored.md + run_log；'
  'registry 1,082 → 1,132（备份 `registry.jsonl.bak-20261124`）。易错点：`7dim-table.md` 表头必须保留 `arXiv` 列，'
  '否则前端批次卡表内计数为 0。')
r('- 第 9 步 发布：见下方发布记录（构建 → `node --check` → CDP 冒烟 → `check_release` → 提交 → 推送 → Pages 核验）。')
open('papers/daily/%s/run_log.md' % DATE, 'w', encoding='utf-8').write('\n'.join(RL) + '\n')
print('run_log ok')
