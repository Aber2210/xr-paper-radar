# -*- coding: utf-8 -*-
"""2026-11-20 最终解读报告：reports/XR-Daily-Report-2026-11-20.md + run_log.md"""
import glob, json, os, sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
os.chdir(ROOT)
DATE, MMDD = '2026-11-20', '1120'

D = json.load(open('data/scored_%s.json' % MMDD, encoding='utf-8'))
DIG = {}
for g in range(1, 6):
    DIG.update(json.load(open('data/digest_1120_g%s.json' % g, encoding='utf-8')))
G = json.load(open('data/gates_%s.json' % DATE, encoding='utf-8'))
RES = json.load(open('data/residual_1120.json', encoding='utf-8'))
PUB = json.load(open('data/published_1120.json', encoding='utf-8'))
MAN = json.load(open('data/fulltext/_manifest.json', encoding='utf-8'))

MAIN = [p for p in D if not p['batch'].startswith('backfill')]
BF = [p for p in D if p['batch'].startswith('backfill')]
TOP = [p for p in D if p['in_top10']]
from collections import Counter
cnt = Counter(p['grade'] for p in D)
cnt_m = Counter(p['grade'] for p in MAIN)
g3 = G['gate3']

def bl(items):
    return '\n'.join('- ' + x for x in items)

L = []
A = L.append

A('# XR 每日论文雷达 · %s\n' % DATE)
A('> **诚实口径**：本批处理的是 **2026-11-19（周四）公告批次**，拉取时刻为 **2026-11-20 02:30（北京时间）**。'
  'arXiv 公告日 ≠ 拉取日 ≠ 首次提交日：主批 API `published` 核验为 **11-17×8 / 11-18×17**，'
  'RSS 的 `published` 字段是公告时间戳，不能当提交日使用。\n')
A('> 覆盖范围：cs.CV / cs.GR / cs.HC / cs.MM / cs.RO / cs.AI / eess.IV 七分类 listing（show=500 单页，declared=got 逐分类核对）。'
  '11-19 组 **599 槽位 / 502 篇唯一**，全部命中 RSS 753 条（缺收 0），故摘要级覆盖率 1.0000。\n')

# ---------------- 一、执行摘要 ----------------
A('\n## 一、执行摘要\n')
A('**本批 28 篇（主批 25 + backfill 3），0 S / 20 A / 5 B / 3 C，Top10 实数 10 篇，最高 4.33（2611.23417 Autoregressive View Model）。**'
  ' 门③ 现算：当日最高 4.33 < 库内近 30 天 Top10 均分 4.4230（457 条入窗，半开窗口 [2026-10-21, 2026-11-20)，按 batch 剔除本批两批），'
  '**判定为非重磅日，不授予 S 级**（margin −0.093，不属于「险过」区间）。\n')
A('当日三条主线：\n')
A('1. **端侧 AR 成像从「能跑」走向「可工程化」**：2611.24805 把 RAW 压缩与复原拆成端侧轻编码 + 后台重解码的非对称架构，'
  '在 Rokid Glass 上给出实测延迟与功耗（BD-rate 相对 VVC+NAFNet 降低 70.5%），是本期最接近产品的系统工作；'
  '2611.23670 用 OCT + 解剖点云 + 近眼图像训练 3D 眼睛生成器，把纯合成数据训练的眼动误差压到 3.53°。\n')
A('2. **场景表示在「显式 3D」之外继续试探**：2611.23417 直接放弃显式 3D，把场景生成为沿相机路径的「视角流」，'
  '721 帧闭环回访 PSNR 28.04（最佳世界模型基线 12.29），相机可控性 70.67 对 3.91——这篇是**残差复核捞回来的**'
  '（摘要级 KW 与标题扩展词均未命中），也说明词表层仍有系统性缺口。同方向还有 2611.23736（把持续学习放进每个高斯基元）'
  '与 backfill 的 2606.07179（演化树连续分层流式，存储降 33.6–53.3%）。\n')
A('3. **触觉从器件到物理量闭环**：2611.23575 用彩色硅胶壁把剪切编码进色度，$138 成本做到每点三轴力（插孔成功率 40%→87%）；'
  '2611.23871 把双手与多物体放进同一动力学联合反解，单视角 RGB-D 即可反推接触力（MAE 1.020 N，较 HOPE 降 24.5%）。'
  '两篇合起来回答了「触觉数据从哪来、怎么便宜地采」这一长期缺口。\n')
A('**筛选与复核**：摘要级 KW 命中 52 + 标题级扩展词补扫 16 = 68 候选，逐篇核摘要后剔 43 篇（医学影像 9 / 机器人操作 11 / '
  '自驾与遥感 8 / 通用 LLM 与 NLP 9 / 科学成像 6），得 22 篇；第 3.5 步残差复核 434 条中判 12 条应收录（2.8%），'
  '采纳 3 篇进入本批（2611.23417 / 2611.23534 / 2611.24193），其余 9 条留待后续批次人工挑选。'
  '上一公告组（11-18 组 475 篇未入馆）复采核验：37 篇摘要/标题级命中全部已在上批候选池内被显式处置（21 入馆 + 37 剔除），**0 漏网**。\n')

# ---------------- 二、Top10 ----------------
A('\n## 二、Top10 排行榜\n')
A('| 排名 | 论文 | 赛道 | 总分 | 档 | 证据 | 关键贡献 |')
A('|---|---|---|---|---|---|---|')
SHORT = {
 '2611.23417': '无显式 3D 的「视角流」生成，回访一致性大幅超越世界模型基线',
 '2611.24805': '端侧轻编码 + 后台重解码的 RAW 联合压缩复原，Rokid Glass 实测',
 '2611.23670': '解剖先验 3D 眼睛生成，合成数据训练眼动 E50 3.53°',
 '2611.23575': '彩色光学 taxel 阵列，$138 实现每点三轴力，全栈开源',
 '2611.23736': '持续学习闭环下沉到高斯基元，14 场景 +3.41 dB 不遗忘',
 '2611.23871': '单视角 RGB-D 手物交互力重建，MAE 1.020 N（−24.5%）',
 '2611.23935': '首个实时三角泼溅 SLAM，113 FPS，网格 chamfer −44%',
 '2611.24938': '几何+时空双教师蒸馏的场景结构表征，跨具身迁移领先',
 '2611.23554': '逐层选择注意力估计器，2.0× 加速仅损 1.38 AUC@5',
 '2611.23513': '沿射线平移校正焦距深度偏置，最坏误差 284.3→56.0 mm',
}
for i, p in enumerate(TOP, 1):
    A('| %d | %s（%s） | %s | **%.2f** | %s | %s | %s |' % (
        i, p['title_zh'], p['id'], p['track'], p['value'], p['grade'], p['evidence'],
        SHORT.get(p['id'], '')))
A('\n> 无 OUTDATED / SUPERSEDED 标记：本批未发现「同问题更优且更晚」的直接取代关系。'
  '2611.24193（WM^MLLM）因 arXiv HTML 缺正文按 PARTIAL 评估，未进 Top10。\n')

# ---------------- 三、逐篇深度解读 ----------------
A('\n## 三、逐篇深度解读\n')
for i, p in enumerate(TOP, 1):
    g = DIG[p['id']]
    A('\n### 第 %d 章 %s（%s · %s · %.2f %s）\n' % (i, p['title_zh'], p['id'], p['track'], p['value'], p['grade']))
    A('**一句话结论**：%s\n' % SHORT.get(p['id'], ''))
    A('**要解决的问题**\n\n%s\n' % g['problem'])
    A('**方法详解**\n\n%s\n' % g['method'])
    A('**实验与结果**\n\n%s\n' % bl(g['key_results']))
    A('**创新点与贡献**\n\n%s\n' % g['novelty'])
    A('**局限与风险**\n\n%s\n' % g['limitations'])
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
    act += '\n- 有公开代码/项目页，可先跑通再评估迁移成本。' if (p.get('code') and p['code'] != 'none') else '\n- 未提供代码，复现需按正文细节自行实现。'
    A('**行动建议**\n\n%s\n' % act)

# ---------------- 四、7 维表 ----------------
A('\n## 四、当日全量 7 维度对比表\n')
A('权重：IMP 0.20 · NOV 0.20 · TEC 0.15 · EXP 0.15 · PER 0.15 · TRL 0.08 · REP 0.07；'
  '分档：S ≥ 4.20 且 blockbuster=true / A 3.60–4.20 / B 3.00–3.60 / C < 3.00。\n')
A('| # | 论文 | 赛道 | IMP | NOV | TEC | EXP | PER | TRL | REP | 总分 | 档 | 批次 |')
A('|---|---|---|---|---|---|---|---|---|---|---|---|---|')
for i, p in enumerate(D, 1):
    s = p['scores']
    A('| %d | %s（%s） | %s | %d | %d | %d | %d | %d | %d | %d | **%.2f** | %s | %s |' % (
        i, p['title_zh'], p['id'], p['track'], s['IMP'], s['NOV'], s['TEC'], s['EXP'],
        s['PER'], s['TRL'], s['REP'], p['value'], p['grade'], p['batch']))

# ---------------- 五、覆盖校验 ----------------
A('\n## 五、覆盖率校验与筛选过程\n')
A('### 5.1 三关结果\n')
A('- **门① 同质去重**：最大 Jaccard **%.3f**（%s vs %s），远低于 0.62 阈值 → PASS，无需降权。' % (
    G['gate1']['max_jaccard'], G['gate1']['pair'][0], G['gate1']['pair'][1]))
A('- **门② 赛道覆盖**：Top10 覆盖 **%d 个赛道**（%s）→ PASS（阈值 ≥5），未触发重筛；全批覆盖 %d 个赛道。' % (
    G['gate2']['n_tracks'], '、'.join(G['gate2']['tracks_top10']), len({p['track'] for p in D})))
A('- **门③ 价值天花板**：当日最高 **%.2f** vs 库内近 30 天 Top10 均分 **%.4f**（%d 条入窗，半开窗口 %s~%s，已按 batch 剔除本次两批）'
  ' → heavy_day_raw=%s，margin=%.3f，**blockbuster=%s**，S 授予=%s。门③ 是校准关，不触发重筛。' % (
    g3['today_max'], g3['lib_top10_mean'], g3['n_window'], g3['window'][0], g3['window'][1],
    g3['heavy_day_raw'], g3['margin'], g3['blockbuster'], g3['s_awarded']))
A('\n### 5.2 筛选漏斗\n')
A('| 阶段 | 数量 | 说明 |')
A('|---|---|---|')
A('| listing 11-19 组 | 502 篇唯一（599 槽位） | declared=got 逐分类核对，7/7 分类 OK |')
A('| RSS 摘要覆盖 | 502/502 | 缺收 0 → 免 API `id_list`，规避 429 静默丢批 |')
A('| 摘要级 KW 命中 | 52 | KW 56 词 + 缩写词边界 |')
A('| 标题级扩展词补扫 | +16 | 第三层召回，不计入「RSS 漏网」统计 |')
A('| 逐篇核摘要剔除 | −43 | 医学影像 9 / 机器人操作 11 / 自驾遥感 8 / LLM-NLP 9 / 科学成像 6 |')
A('| 残差复核采纳 | +3 | 2611.23417 / 2611.23534 / 2611.24193 |')
A('| 定稿主批 | **25** | 0 S / 17 A / 5 B / 3 C |')
A('| backfill 旧稿 | **3** | replace v2 再公告，最高记 A |')
A('\n### 5.3 残差复核（第 3.5 步）\n')
A('残差复核：扫描 **%d** 条，疑似漏检 **%d** 条（**%.1f%%**），采纳 **3** 条。' % (
    RES['n_scanned'], RES['n_flagged'], 100 * RES['rate']))
A('')
A('采纳条目与赛道：2611.23417（神经渲染，自回归视角模型）、2611.23534（系统与平台，智能眼镜综述）、'
  '2611.24193（世界模型与仿真，WM^MLLM）。未采纳的 9 条留待后续批次人工挑选，**均未写入 registry**——'
  '清单只是报警，入馆仍走全文抓取 → 评分 → 产物。\n')
A('分布：%s。本批 rate 2.8%%，低于 12%% 阈值，未触发关键词层整体重估。\n' % '、'.join(
    '%s %d' % (k, v) for k, v in sorted(RES['by_track'].items(), key=lambda x: -x[1])))
A('### 5.4 上一公告组对账（0 漏网）\n')
A('11-18 组复采 declared=got（599 槽位 / 496 唯一），未入馆 475 篇（= 496 − 21 主批）全部有 RSS 摘要（475/475）；'
  '摘要/标题级命中 37 篇，全部落在上批候选池 `xr_pool_1119.json` 内（21 入馆 + 37 剔除），**未处置 0 篇 → 0 漏网**。\n')

# ---------------- 六、附录 ----------------
A('\n## 六、附录\n')
A('### 6.1 全文抓取与证据等级\n')
lv = Counter(MAN[p['id']]['level'] for p in D)
ev = Counter(MAN[p['id']]['evidence'] for p in D)
A('- 抓取 **28 篇**（主批 25 + backfill 3），串行 3 s/篇：级别 %s；证据 %s。' % (
    dict(lv), dict(ev)))
A('- **2611.24193（WM^MLLM）为 PARTIAL**：arXiv HTML 只渲染出前言、引言与图注，无 Method / Experiments 节，'
  'ar5iv 与 `/html/…v1` 复核同样缺正文 → 按摘要级评估并显式声明；其 TEC / EXP 已按证据等级下调，报告未引用未核实数字作为结论。')
A('- **2606.07179（backfill）为 L1/FULL**：arXiv HTML v2 是空壳页（仅导航 1,578 字符），改由 ar5iv 取全正文 56,366 字符，'
  'manifest 记 note。另：arXiv 元数据标题为 *Lifting 3D Gaussians: A Wavelet Multiresolution Representation for Scalable '
  'Gaussian Splatting Streaming*，正文（v2/ar5iv）标题为 *EvoGS: Constructing Continuous-Layered Gaussian Splatting '
  'with Evolution Tree for Scalable 3D Streaming*，疑为 v2 改题，registry 采用 arXiv 元数据标题。')
A('- 失败/降级：0 篇 NO_FULLTEXT，0 篇 ABSTRACT_ONLY。\n')
A('### 6.2 backfill 批次（非当日新提交）\n')
A('| 论文 | 赛道 | 总分 | 档 | 首发 | 说明 |')
A('|---|---|---|---|---|---|')
for p in BF:
    A('| %s（%s） | %s | %.2f | %s | %s | replace v2 再公告 |' % (
        p['title_zh'], p['id'], p['track'], p['value'], p['grade'], p['published']))
A('\nbackfill 不参与当日重磅日判定，按口径最高记 A。2606.07179（4.05）若计入主批将改变头部排序，但批次身份不同，'
  '报告中不与主批混排。\n')
A('### 6.3 数据源与采集状态\n')
A('- API 双主机探针：export.arxiv.org 200 / arxiv.org 200（各 1 次最简查询）。')
A('- RSS：`OK_CATS=7/7`，全量去重 753 条（KW 命中 78 条落 `data/raw/2026-11-20.jsonl`，全量落 `_all.jsonl`）。')
A('- listing：7 分类 show=500 单页，`declared=got` 逐分类一致（CV 223 / GR 3 / HC 23 / MM 6 / RO 104 / AI 230 / IV 10），无补页。')
A('- 提交日核验：28 篇逐篇过 API，`missing=[]`。\n')
A('### 6.4 发布状态（详见 run_log）\n')
A('- 渠道② GitHub Pages：见文末 run_log 与 STATUS.md。')
A('- 渠道① WorkBuddy 托管：工具不在工具集，**本批仍不可用**，按「渠道①不可用（累计第 N 批挂账）」如实记录，不声称已发布。\n')

open('reports/XR-Daily-Report-%s.md' % DATE, 'w', encoding='utf-8').write('\n'.join(L))
print('report chars', len('\n'.join(L)))

# ---------------- run_log ----------------
RL = []
RL.append('# run_log · %s（11-19 公告批次）\n' % DATE)
RL.append('## 1. 对账（先于拉取）')
RL.append('- `scripts/audit_listing_1120.py`（PREV_DAY=2026-11-18，NEW_DAYS=[2026-11-19, 2026-11-20]）')
RL.append('- 7/7 分类 newest=2026-11-19，prev 组 declared=got 全 OK，11-20 组未释放（运行时刻 02:30 早于 UTC 00:00 公告时刻后的索引刷新）')
RL.append('- 11-18 组复采 599 槽位 / 496 唯一；未入馆 475 篇摘要覆盖率 475/475；命中 37 篇全在 `xr_pool_1119.json` → 0 漏网')
RL.append('- `check_audit_guard.py`：PASS（23 份脚本，守卫 5 / 基线豁免 18 / 违规 0）\n')
RL.append('## 2. 数据源')
RL.append('- API 探针 export/www 均 200')
RL.append('- RSS 7/7 分类，753 条全量；KW 命中 78')
RL.append('- listing show=500 单页足够，无补页\n')
RL.append('## 3. 甄别与残差')
RL.append('- 502/502 摘要覆盖（缺收 0）→ 免 id_list')
RL.append('- KW 52 + 标题补扫 16 = 68 → 剔 43 → 22；残差采纳 3 → 25')
RL.append('- 残差扫描 434，判 12（2.8%），采纳 3；9 条留池')
RL.append('- replace 旧稿 19 篇 XR 命中中选 3 篇 backfill\n')
RL.append('## 4. 全文')
RL.append('- 25 篇首批 + 3 篇残差采纳 = 28 篇，串行 3 s')
RL.append('- 26 篇 L0/FULL；2611.24193 L0/PARTIAL（HTML 缺正文）；2606.07179 L1/FULL（ar5iv 补）')
RL.append('- 0 失败，0 ABSTRACT_ONLY\n')
RL.append('## 5. 评分与三关')
RL.append('- 7 维按标准权重重算（子代理 scores_hint 仅作参考）')
RL.append('- 校准改动：24938 IMP5→4/PER4→3；23670 PER4→3；23871 TRL4→3；24805 TRL5→4；2606.07179 PER4→3；24193 TEC3→2/EXP4→2/PER5→4')
RL.append('- 门① 0.072 / 门② 7 赛道 / 门③ 4.33 vs 4.4230（457 入窗）→ 非重磅日无 S')
RL.append('- 档位统计：%s\n' % dict(cnt))
RL.append('## 6. 产物')
RL.append('- 报告 1 + 笔记 25 + daily 目录（7dim-table/scored/run_log）+ MOC 2 + 总索引刷新')
RL.append('- registry 1015 → 1043（备份 registry.jsonl.bak-20261120）\n')
RL.append('## 7. 失败与降级')
RL.append('- 无抓取失败；2611.24193 证据降级 PARTIAL 并显式声明')
RL.append('- smoke/CDP 与发布结果见第 8 节（发布阶段追加）\n')
open('papers/daily/%s/run_log.md' % DATE, 'w', encoding='utf-8').write('\n'.join(RL))
print('run_log written')
print('grades', dict(cnt), 'main', dict(cnt_m))
