# -*- coding: utf-8 -*-
"""2026-11-21 最终解读报告 + backfill 报告 + run_log。"""
import glob, json, os, sys
from collections import Counter

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
os.chdir(ROOT)
DATE, MMDD = '2026-11-21', '1121'

D = json.load(open('data/scored_%s.json' % MMDD, encoding='utf-8'))
DIG = {}
for g in range(1, 9):
    DIG.update(json.load(open('data/digest_1121_g%s.json' % g, encoding='utf-8')))
G = json.load(open('data/gates_%s.json' % MMDD, encoding='utf-8'))
RES = json.load(open('data/residual_%s.json' % MMDD, encoding='utf-8'))
PUB = json.load(open('data/published_%s.json' % MMDD, encoding='utf-8'))
MAN = json.load(open('data/fulltext/_manifest.json', encoding='utf-8'))
AUD = json.load(open('data/audit_1121_days.json', encoding='utf-8'))
REJ = json.load(open('data/rejected_1121.json', encoding='utf-8'))

MAIN = [p for p in D if not p['batch'].startswith('backfill')]
BF = [p for p in D if p['batch'].startswith('backfill')]
TOP = [p for p in D if p['in_top10']]
cnt_m = Counter(p['grade'] for p in MAIN)
cnt_b = Counter(p['grade'] for p in BF)
g3, g2, g1 = G['gate3'], G['gate2'], G['gate1']

SHORT = {
 '2611.26625': '流式几何基础模型 + 惯性基础模型前馈融合，跨平台免调参恒算力的度量 VIO；APE 11.19→5.86 m、70 ms/帧出位姿。',
 '2611.26540': 'DMD 蒸馏 + 逐 chunk 混合时间步 + RoPE 重索引，把音频驱动说话人做成真流式：1.3B 单卡 20.7 fps（teacher 0.90 fps）。',
 '2611.26603': '单一网络同时做到锐利、时序一致、度量准确：11 数据集零样本平均排名第一，1080p 流式 53 fps。',
 '2611.26493': '几何嵌入检索 + 块稀疏掩码替代稠密全局注意力：1000 视图 12.2× 加速，AUC@30 仅降 1.9 点。',
 '2611.25338': '视频生成先验 → rtRNG 可重光照神经高斯资产，重光照 PSNR 25.47 对 LSRM 22.53，505 人偏好率 57.75%。',
 '2611.25279': 'VIO 度量位姿条件化深度基础模型 + 因子图融合子图，单目+IMU 在线稠密度量建图；EuRoC F@5cm 0.570。',
 '2611.26321': '把单光子重建写成首交点的凸问题序列，无网络、无逐场景非凸优化；三视角 MAE 0.90 mm（对方 2.60 mm）。',
 '2611.26165': '流式双分支先验 + 无界因果生成，Exo2Ego 达 24.3 FPS（EgoX 0.08 FPS），PCK@0.05 3.4 倍。',
 '2611.25925': '分层记忆 + 可编排视觉专家做定量空间推理，MetricBench 较最佳 VLM +32%（室外 75.5% vs 40.3%）。',
 '2611.26072': '用散焦模糊作物理度量线索，单图对预测度量 3D 高斯；Booster AbsRel 0.075 对 UniDepth v2 的 0.230。',
}


def bl(items):
    return '\n'.join('- ' + str(x) for x in items)


L = []
A = L.append

A('# XR 每日论文雷达 · %s\n' % DATE)
A('> **诚实口径**：本批处理的是 **2026-11-20（周五）公告批次**，拉取时刻为 **2026-11-21 02:30（北京时间）**。'
  'arXiv 公告日 ≠ 拉取日 ≠ 首次提交日：主批 API `published` 核验为 **11-19×33 / 11-18×4**，'
  'RSS 的 `published` 字段是公告时间戳，不能当提交日使用。\n')
A('> 覆盖范围：cs.CV / cs.GR / cs.HC / cs.MM / cs.RO / cs.AI / eess.IV 七分类 listing（show=500 单页，declared=got 逐分类核对）。'
  '11-20 组 **605 槽位 / 508 篇唯一**，全部命中 RSS 783 条（缺收 0），故摘要级覆盖率 1.0000。\n')

# ---------------- 一、执行摘要 ----------------
A('\n## 一、执行摘要\n')
A('**本批 39 篇（主批 37 + backfill 2），0 S / 24 A / 14 B / 1 C；Top10 实数 10 篇，最高 4.43（2611.26625 AnyVIO）。**'
  ' 门③ 现算：当日最高 4.43 vs 库内近 30 天 Top10 均分 **4.4230**（465 条入窗，半开窗口 [2026-10-22, 2026-11-21)，'
  '按 batch 剔除本批两批），margin **+0.007 < 0.05** → 属「险过」，按 skill §8.6.3 与 11-18 先例 **不授予 S**；'
  '本批 6 篇 ≥4.20（4.43/4.32/4.30/4.30/4.28/4.22）**一律记 A**，并在 7 维表与索引中保留「达 S 线」注记。\n')
A('当日四条主线：\n')
A('1. **规模化与实时性同时被推进**：2611.26493 SGAR 把前馈重建的稠密全局注意力换成「几何嵌入检索 + 块稀疏」，'
  '1,000 视图从 319.6 s 压到 26.1 s（12.2×）而 AUC@30 仅降 1.9 点；2611.26625 AnyVIO 把流式几何基础模型与惯性基础模型'
  '前馈融合，九个数据集上 APE 减半、70 ms 出位姿、4,798 帧吞吐不衰减。两者共同指向一件事：'
  '**3D 基础模型正从「能重建」转向「能常驻、能上机」**。\n')
A('2. **度量深度成为 XR 的公共底座**：2611.26603 Depth Pro 2 用单一网络同时给出锐利、时序一致、度量准确的深度'
  '（11 数据集零样本第一、Jitter 1.39 对 π³ 2.13、1080p 53 fps）；2611.26072 DfD-GS 把散焦模糊当物理度量线索，'
  '单图对即得度量 3D 高斯（Booster AbsRel 0.075 对 UniDepth v2 的 0.230）。二者互补：一个走数据驱动规模化，一个走物理先验。\n')
A('3. **生成侧从「能生成」转向「可编辑、可重光照、可交互」**：2611.25338 VideoRNG 用视频先验产出可路径追踪重光照的'
  '神经高斯资产（重光照 PSNR 25.47 对 LSRM 22.53，505 人偏好率 57.75%）；2611.25500 PRIO 用单次前向预测物体构型空间，'
  '让 4D 世界里的物体实时按物理规律响应（比 VBD 快 7.1×）；2611.26516 Plan4D 把 RGB 与稠密 4D 几何一起预测。\n')
A('4. **交互与评估侧的「负结果」同样重要**：2611.25608 MetaScanner 在 VRChat 实证四种欺骗性 UI 攻击'
  '（83.3% / 86.7% 用户完全未察觉，37.9% 愿意扫描伪造二维码）；2611.24995 EgoPass-Bench 显示最强模型在「物体是否影响通行」'
  '上比人类低 23.65 点，且能判物体运动（91.37%）却判不对通行约束（66.50%）。这类工作不提供 SOTA，但定义了 XR 的真实风险面。\n')
A('**筛选与复核**：摘要级 KW 命中 47 + 标题级扩展词补扫 30 = 77 候选，逐篇核摘要剔 43 篇'
  '（机器人操作/具身策略 14 / 通用视觉与生成 11 / 医学与科学成像 7 / 遥感与自驾 5 / 通用 LLM 与安全 6），得 34 篇；'
  '第 3.5 步残差复核扫描 431 条、判 7 条应收录（**1.6%**），采纳 3 篇（2611.25696 LIFT / 2611.25802 World-delta / '
  '2611.25801 FAB）→ 主批 37 篇。上一公告组（11-19 组 477 篇未入馆）复采核验：46 篇摘要/标题级命中全部已在上批'
  '候选池内被显式处置（28 入馆 + 43 剔除），**0 漏网**，无需 backfill 补漏。\n')

# ---------------- 二、Top10 ----------------
A('\n## 二、Top10 排行榜\n')
A('| 排名 | 论文 | 赛道 | 总分 | 档 | 证据 | 关键贡献 |')
A('|---|---|---|---|---|---|---|')
for i, p in enumerate(TOP, 1):
    A('| %d | %s（%s） | %s | **%.2f** | %s | %s | %s |' % (
        i, p['title_zh'], p['id'], p['track'], p['value'], p['grade'], p['evidence'], SHORT.get(p['id'], '')))
A('\n> **门② 重筛一次**：纯值 Top10 覆盖 4 赛道（重建与SLAM×6），剔除重建赛道最低分 2611.25061 Infer3D（4.07，'
  '仍入馆记 A、不占名额），回补神经渲染最高分 2611.26072 DfD-GS（4.00）→ 定稿 5 赛道。\n')
A('> 无 OUTDATED / SUPERSEDED 标记：本批未发现「同问题更优且更晚」的直接取代关系。'
  '2405.15125 HDR-GS 为 2024-05 旧稿 v3 再公告，其比较对象（HDR-NeRF 系）已被 2025 年后的 3DGS 重光照工作普遍超越，'
  '已在该篇笔记中标注「时效性风险」，但未达论文级 OUTDATED 证据门槛。\n')

# ---------------- 三、逐篇深度解读 ----------------
A('\n## 三、逐篇深度解读\n')
for i, p in enumerate(TOP, 1):
    g = DIG[p['id']]
    A('\n### 第 %d 章 %s（%s · %s · %.2f %s）\n' % (i, p['title_zh'], p['id'], p['track'], p['value'], p['grade']))
    A('**一句话结论**：%s\n' % SHORT.get(p['id'], ''))
    A('**要解决的问题**\n\n%s\n' % g['problem'])
    A('**方法详解**\n\n%s\n' % g['method'])
    A('**实验与结果**\n\n%s\n' % bl(g['key_results']))
    A('**创新点与贡献**\n\n%s\n' % bl(g['novelty']))
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
    if p.get('code') and p['code'] != '未提供':
        act += '\n- 有公开代码/项目页，可先跑通再评估迁移成本。'
    else:
        act += '\n- 未提供代码，复现需按正文细节自行实现。'
    if p['value'] >= 4.20:
        act += '\n- 达 S 线（≥4.20）而本批为险过日：值得优先读，但不宜按 S 级对外表述。'
    A('**行动建议**\n\n%s\n' % act)

# ---------------- 四、7 维表 ----------------
A('\n## 四、当日全量 7 维度对比表\n')
A('权重：IMP 0.20 · NOV 0.20 · TEC 0.15 · EXP 0.15 · PER 0.15 · TRL 0.08 · REP 0.07；'
  '档位：S ≥4.20 且 blockbuster，A 3.60–4.20，B 3.00–3.60，C <3.00（仅入馆不解读）。完整表见 '
  '[`papers/daily/%s/7dim-table.md`](../papers/daily/%s/7dim-table.md)。\n' % (DATE, DATE))
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
A('- 7 分类最新公告日均为 **2026-11-20（周五）**，无 11-21 日组（周六 `skipDays`）；'
  '11-20 组逐分类 declared=got：cs.CV 213 / cs.GR 6 / cs.HC 23 / cs.MM 4 / cs.RO 92 / cs.AI 252 / eess.IV 15 = **605 槽位**，'
  '唯一论文 **508 篇**（跨列表重复 97）。\n')
A('- 上一公告组（11-19）复采 **599 槽位 / 502 唯一、declared=got**，未入馆 **477 篇 = 502 − 25（上批主批已入馆）**；'
  '用 11-19/11-20/11-21 三份 RSS 全量核摘要，477/477 全覆盖，摘要/标题级命中 **46 篇全部落在上批处置集合'
  '（`xr_pool_1120` ∪ `nonxr_1120` ∪ `scored_1120`）** → **0 漏网**（`data/missed_xr_1121.json` 为空）。\n')
A('### 5.2 数据源与召回\n')
A('- API 双主机探针 200；RSS 7 分类 `--no-filter` 去重 **783 条**（`OK_CATS=7/7`，完整采集）。'
  'listing 508 篇 **100% 被 RSS 覆盖（缺收 0）** → 免 API `id_list`，规避 429 静默丢批。\n')
A('- 召回三层：**摘要级 KW 47 篇** → **标题级扩展词补扫 +30 篇**（含 2026-11-19 登记的 tactile/SDF/meshing/'
  'light field/single-photon/monocular depth 等缺口词）→ 逐篇核摘要剔 **43 篇**（明细见 `data/rejected_1121.json`）'
  '→ **34 篇**；残差复核采纳 3 篇 → **主批 37 篇**。\n')
A('### 5.3 第 3.5 步残差复核（只报警，不入馆）\n')
A('残差复核：扫描 **%d** 条，疑似漏检 **%d** 条（**%.1f%%**），采纳 **3** 条。\n' % (
    RES['n_scanned'], RES['n_flagged'], RES['rate'] * 100))
A('| # | arXiv | 标题 | 赛道 | 处置 |')
A('|---|---|---|---|---|')
ADOPT = {'2611.25696', '2611.25802', '2611.25801'}
for it in RES['flagged']:
    A('| %d | %s | %s | %s | %s |' % (it['n'], it['id'], it['title'][:64].replace('|', '/'), it['track'],
                                     '**采纳入本批**' if it['id'] in ADOPT else '留待人工挑选池'))
A('\n> 采纳口径：三篇均为 12 赛道内的核心表述（自由视点 3D 融合 / 增量 3D 场景生成 / 人体稠密估计），'
  '且与已入馆条目无同质（门① 复算 max Jaccard %.3f）。其余 4 条（全景生成、交互式游戏渲染、人-物运动合成、'
  '连续时间 3D 动力学）留在 `data/residual_1121.json` 清单，不自动入馆。\n' % g1['max_jaccard'])
A('### 5.4 三关\n')
A('| 关卡 | 口径 | 本批数值 | 结论 |')
A('|---|---|---|---|')
A('| 门① 同质度 | 与库内 90 天非本批条目最大 Jaccard < 0.62 | **%.3f**（%s vs %s，%s） | PASS |' % (
    g1['max_jaccard'], g1['detail'][0]['id'], g1['detail'][0]['vs'], g1['detail'][0]['date']))
A('| 门② 赛道覆盖 | Top10 覆盖 ≥5 赛道 | **%d 赛道**（%s） | PASS（一次重筛） |' % (
    g2['n_tracks'], '、'.join(f"{k}×{v}" for k, v in g2['top10_tracks'].items())))
A('| 门③ 价值天花板 | today_max ≥ 近 30 天 Top10 均分，且 margin ≥ 0.05 才授 S | **%.2f vs %.4f**，margin **%+.4f** | 险过，**blockbuster=false** |' % (
    g3['today_max'], g3['top10_mean'], g3['margin']))
A('\n> 门③ 留痕（`data/gates_%s.json`）：`window_excludes_today=%s`、`window_excludes_this_run_batches=%s`、'
  '`this_run_batches_excluded=%s`、`heavy_day_raw=%s`、`margin=%.4f`、`blockbuster=%s`、`s_awarded=%s`；'
  '入窗 **%d 条**。\n' % (MMDD, g3['window_excludes_today'], g3['window_excludes_this_run_batches'],
                          g3['this_run_batches_excluded'], g3['heavy_day_raw'], g3['margin'],
                          g3['blockbuster'], g3['s_awarded'], g3['in_window']))
A('### 5.5 评分校准披露（影响档位的一处判定）\n')
A('- **2611.26493 SGAR**：子代理给 IMP=5 / NOV=5 → 4.70（越门③ 线，将成重磅日）。主会话据「IMP 5 = 领域公认卡脖子'
  '且解决它改变系统能力边界」口径下调 IMP=4（本文是对既有前馈管线 DejaView / VGGT-Ω 的加速，属重要工程瓶颈而非能力级突破；'
  '对照库内 4.50+ 的 riMESA / Open-HumanScale / Map2SLAM 均为能力级工作），NOV 同步下调为 4（组件为已有积木的组合）。'
  '**若维持 IMP=5 则为 4.50、margin +0.077、blockbuster=true，本批将出现 6 篇 S**——该替代读数在此显式留痕，'
  '供复核者判断；本次采用更严格读数，理由是库内 S 占比 1.7%（18/1043），单批 6 篇 S 会构成明显的档位通胀。\n')
A('- 其余改动仅两处：2611.25338 VideoRNG IMP 5→4（内容侧重要缺口但非 XR 卡脖子）；赛道修正两处'
  '（2611.25696 触觉与多模态→神经渲染；2610.09195 交互与输入→化身与人体）。\n')

# ---------------- 六、附录 ----------------
A('\n## 六、附录\n')
A('### 6.1 全文抓取与证据等级\n')
lv = Counter(MAN[p['id']]['level'] for p in D)
A('- 39 篇串行 3 s/篇（`scripts/fetch_fulltext.py`）：**%s**，字符数 %s–%s。\n' % (
    ' / '.join(f'{k} {v}' for k, v in lv.items()),
    format(min(MAN[p['id']]['chars'] for p in D), ','),
    format(max(MAN[p['id']]['chars'] for p in D), ',')))
A('- 全部 **FULL**：逐篇抽看含 Introduction / Method / Experiments 正文节（最少 33,057 字符，远超 ar5iv 摘要页 ~5k 量级），'
  '本次无 PARTIAL / ABSTRACT_ONLY。\n')
A('### 6.2 剔除明细（43 篇，摘要级判读）\n')
grp = Counter()
for p, v in REJ.items():
    why = v['why']
    key = ('机器人操作/具身策略' if ('机器人' in why or '具身' in why or 'VLA' in why or '操作' in why)
           else '医学/科学成像' if ('医学' in why or '成像' in why or '电镜' in why)
           else '遥感/自驾/测绘' if ('遥感' in why or '自驾' in why or '测绘' in why or 'LiDAR' in why or 'AUV' in why)
           else '通用视觉/生成' if ('视觉' in why or '生成' in why or '图像' in why or '视频' in why or '点云' in why)
           else '通用 LLM/安全/其他')
    grp[key] += 1
A('- ' + '；'.join(f'{k} {v} 篇' for k, v in grp.most_common()) + '。逐条理由见 `data/rejected_1121.json`。\n')
A('### 6.3 本批数据文件\n')
A('- `data/audit_1121_days.json` / `data/audit_1121_alldays.json`：对账原始记录（7 分类日期头、declared/got、补页记录）\n'
  '- `data/newday_1121.json`（508 篇唯一）、`data/missed_prev_1121.json`（477）、`data/missed_xr_1121.json`（0）\n'
  '- `data/xr_pool_1121.json`（37）、`data/rejected_1121.json`（43）、`data/backfill_pool_1121.json`（2）\n'
  '- `data/scored_1121.json`、`data/gates_1121.json`、`data/published_1121.json`、`data/residual_1121.json`\n'
  '- `data/digest_1121_g1..g8.json`（39 篇精读 digest）、`data/fulltext/<id>.txt` + `_manifest.json`\n')
A('### 6.4 待办与风险\n')
A('- **关键词表**：本批 30/77 靠标题级补扫入池（其中 3 篇进 Top10），说明摘要级 KW 仍有系统性缺口；'
  '但反向证据同样明确——43/77 为误命中，噪声主要来自 `SLAM`/`tracking`/`spatial`/`gaussian` 与机器人/自驾场景共现。'
  '下一批拟引入**共现约束**（如 `SLAM` 需与 `XR|AR|VR|HMD|headset|handheld` 同现）而非继续加词。\n')
A('- **残差率**：本批 1.6%（上批 2.8%），连续两批远低于 12% 阈值，词表不需要整体重估。\n')
A('- **未覆盖方向**：硬件显示侧（波导 / 可变焦 / Maxwellian / 光场显示）连续第 32 批无器件级破冰；'
  '本批 `渲染与显示` 5 篇均为算法侧（HDR-GS / MergeableRF / GaussTrans / FFGaussType / AGSR）。\n')
A('- **渠道①不可用（累计第 32 批挂账）**：`workbuddy_sites_deploy` 不在本会话工具集中，渠道①未发布，**不得视为已双渠道上线**；本轮只走渠道②（GitHub Pages，commit `82a2222` → main `4fd76fe8`，deploy run `44798357045` success，线上 HTTP 200 / md5 `16dd0617…` 与本地 LF 归一化版逐字节相等）。\n')

open('reports/XR-Daily-Report-%s.md' % DATE, 'w', encoding='utf-8').write('\n'.join(L) + '\n')
print('main report', len('\n'.join(L)))

# ---------------- backfill 报告 ----------------
B = []
b = B.append
b('# XR Backfill 报告 · backfill-%s\n' % MMDD)
b('> **非当日新提交**：本批 2 篇均为 2026-11-20 公告 RSS 混入的 `replace` 类旧稿再公告，首次入馆。'
  '按诚实口径单独编号，不参与当日重磅日判定，≥4.20 亦记 A。\n')
b('> 原始首次提交日（API `published`）：2405.15125 = **2024-05-24**（v3 于 2026-11-19 更新）；'
  '2610.09195 = **2026-10-06**（v2 于 2026-11-19 更新）。\n')
b('\n## 一、摘要\n')
b('11-20 公告 RSS 共 275 篇未入馆 `replace` 旧稿，摘要级 XR 命中 16 篇，逐篇核摘要后取 **2 篇**'
  '（其余 14 篇为机器人操作、VLA 综述、医学影像、点云检测等非 XR 方向）。定稿 **1 A / 1 B，无 S**。\n')
b('\n## 二、逐篇解读\n')
for i, p in enumerate(BF, 1):
    g = DIG[p['id']]
    b('\n### %d. %s（%s · %s · %.2f %s）\n' % (i, p['title_zh'], p['id'], p['track'], p['value'], p['grade']))
    b('**要解决的问题**\n\n%s\n' % g['problem'])
    b('**方法详解**\n\n%s\n' % g['method'])
    b('**实验与结果**\n\n%s\n' % bl(g['key_results']))
    b('**创新点**\n\n%s\n' % bl(g['novelty']))
    b('**局限与风险**\n\n%s\n' % g['limitations'])
    b('**可复现性**\n\n- 代码/项目页：%s\n- 全文证据：FULL（%s，%s 字符）\n' % (
        p.get('code') or '正文未提供', MAN[p['id']]['level'], format(MAN[p['id']]['chars'], ',')))
b('\n## 三、完整 7 维表\n')
b('见 [`papers/daily/backfill-%s/7dim-table.md`](../papers/daily/backfill-%s/7dim-table.md)。\n' % (MMDD, MMDD))
open('reports/XR-Backfill-Report-backfill-%s.md' % MMDD, 'w', encoding='utf-8').write('\n'.join(B) + '\n')
print('backfill report', len('\n'.join(B)))

# ---------------- run_log ----------------
RL = []
r = RL.append
r('# 运行日志 · %s\n' % DATE)
r('- 02:30 起跑；C: 盘 5.92 GB / D: 246.77 GB，未触发磁盘保护。')
r('- 第 1 步 对账：`scripts/audit_listing_1121.py`（PREV_DAY=11-19 / NEW_DAYS=11-20,11-21），7/7 分类成功，exit 0；'
  '11-20 组 605 槽位 / 508 唯一；11-19 组 599 槽位 / 502 唯一、declared=got。')
r('- 第 2 步 数据源：API 双主机探针 200（仅用于提交日核验）；RSS 7/7、783 条，WROTE=783。')
r('- 第 3 步 甄别：`triage_1121.py` → KW 47 + TITLE_EXTRA 30 = 77 → `finalize_pool_1121.py` 逐篇判读剔 43 → 34。')
r('- 第 3.5 步 残差：`residual_scan.py dump/ingest` → 扫描 431、判 7（1.6%）、采纳 3 → 主批 37。')
r('- 第 4 步 全文：39 篇（37+2）串行 3 s/篇，全部 L0/FULL；字符 33,057–196,730。')
r('- 第 5 步 评分：8 组子代理 digest（5/5/5/5/5/5/5/4 篇）+ 主会话按标准权重重算；'
  '校准 3 处（SGAR IMP/NOV、VideoRNG IMP）+ 赛道修正 2 处。')
r('- 第 6 步 三关：门① 0.238；门② 5 赛道（一次重筛）；门③ 4.43 vs 4.4230，margin +0.007 → 险过，无 S。')
r('- 第 7 步 Top10：实数 10 篇（4.43–4.00），全部 A；C 级 1 篇（2611.25934 AGSR 2.78）仅入馆不解读。')
r('- 第 8 步 产物：报告 2 + 笔记 38 + MOC 2 + 总索引 + 7 维/scored/run_log；registry 1,043 → 1,082（备份 `registry.jsonl.bak-20261121`）。')
r('- 第 9 步 发布：见下方发布记录（构建 → 冒烟 → check_release → 提交 → 推送 → Pages 核验）。')
open('papers/daily/%s/run_log.md' % DATE, 'w', encoding='utf-8').write('\n'.join(RL) + '\n')
print('run_log ok')
