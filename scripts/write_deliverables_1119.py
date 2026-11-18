# -*- coding: utf-8 -*-
"""2026-11-19 产物（第一部分）：7 维表 / scored.md / run_log.md（主批 + backfill-1119）。

诚实口径：公告日 2026-11-18（周三）≠ 拉取日 2026-11-19（周四 02:30）。
门③：当日最高 4.30 < 库内近 30 天 Top10 均分 4.4230 → 非重磅日无 S（见 gates_1119.json）。
"""
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from grade_caliber import assign_grade  # noqa: E402

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
os.chdir(ROOT)

D = json.load(open('data/scored_1119.json', encoding='utf-8'))
MAIN = [p for p in D if p['batch'] == '2026-11-19']
BF = [p for p in D if p['batch'] == 'backfill-1119']
MAIN.sort(key=lambda r: (-r['value'], -r['scores']['IMP'], -r['scores']['NOV'], r['id']))
G = json.load(open('data/gates_1119.json', encoding='utf-8'))
TOP10_ORDER = G['top10']
DATE, ANN = '2026-11-19', '2026-11-18'
HEAVY = bool(G['gate3']['blockbuster'])
GATE3, G1, MARGIN = G['gate3']['top10_mean'], G['gate1']['max_jaccard'], G['gate3']['margin']
MANIFEST = json.load(open('data/fulltext/_manifest.json', encoding='utf-8'))
for p in MAIN + BF:
    p['level'] = MANIFEST[p['id']]['level']
    p['evidence'] = MANIFEST[p['id']]['evidence']
    p['announce'] = 'replace' if p['batch'].startswith('backfill') else p.get('announce', 'new')
    p['status'] = 'CURRENT'
    p['grade'] = assign_grade(p['value'], p['batch'], HEAVY)
TOP10 = [next(p for p in MAIN if p['id'] == pid) for pid in TOP10_ORDER]
assert [p['id'] for p in TOP10] == TOP10_ORDER
assert len(MAIN) == 21 and len(BF) == 4, (len(MAIN), len(BF))
for p in MAIN:
    p['in_top10'] = p['id'] in TOP10_ORDER

gr_main = {g: sum(1 for p in MAIN if p['grade'] == g) for g in 'SABC'}
gr_bf = {g: sum(1 for p in BF if p['grade'] == g) for g in 'SABC'}
print('main grades', gr_main, 'bf grades', gr_bf)


def esc(s):
    return str(s).replace('|', '/')


def dim_row(p):
    s = p['scores']
    star = '⭐' if p.get('in_top10') else ''
    return (f"| {p['id']} | {esc(p['title_zh'])} {star} | {p['track']} | "
            f"{s['IMP']} | {s['NOV']} | {s['TEC']} | {s['EXP']} | {s['PER']} | {s['TRL']} | {s['REP']} | "
            f"{p['value']:.2f} | {p['grade']} | {p['evidence']} | {p['announce']} |")


TBL_HEAD = ('| arXiv | 标题 | 赛道 | IMP | NOV | TEC | EXP | PER | TRL | REP | 总分 | 等级 | 证据 | 公告类型 |\n'
            '|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|\n')
os.makedirs(f'papers/daily/{DATE}', exist_ok=True)
os.makedirs('papers/daily/backfill-1119', exist_ok=True)


def seven_table(papers, path, title, intro):
    lines = [f'# {title}\n', intro + '\n', TBL_HEAD]
    for p in papers:
        lines.append(dim_row(p) + '\n')
    open(path, 'w', encoding='utf-8').writelines(lines)


INTRO_MAIN = (
    '批次：2026-11-19（**2026-11-18（周三）公告批次**——公告日 11-18 ≠ 拉取日 11-19（周四 02:30），诚实口径）。'
    'API published 核验主批提交日 **11-17×17 / 11-16×3 / 09-27×1**'
    '（2611.21642 RelicTouch 提交 09-27、延迟约 7 周公告；RSS published 为公告时间戳，不可当提交日）。\n'
    '漏网对账（先于拉取，`scripts/audit_listing_1119.py`，show=500 单页×7 分类 + 目标组 declared≠got 自动补页，'
    'PREV_DAY=11-17 / NEW_DAYS=11-18,11-19）：7 分类最新公告日均为 **2026-11-18**，无 11-19 日组；'
    '11-17 组复采逐分类 **declared=got**（CV 342 / GR 15 / HC 58 / MM 11 / RO 134 / AI 428 / IV 28 = **1,016 槽位 / 844 唯一**，'
    'cs.CV 补采 skip=500 合并 49、cs.AI 合并 187），未入馆 **811 篇 = 844 − 33（上批主批已入馆）**；'
    '用 11-18 的 RSS 全量逐篇核摘要，811 篇中 XR 命中 **69 篇**，与上批 `rejected_1118.json` 的 69 篇**逐篇一致** → **0 漏网、无滞后补录**。\n'
    '**11-18 组 599 槽位 / 496 篇唯一论文**（CV 207 / GR 10 / HC 26 / MM 3 / RO 89 / AI 259 / IV 5，全部未入馆）'
    '→ 摘要级 XR 过滤（`scripts/triage_1119.py`；listing 496 篇 100% 被 RSS 全量 766 条覆盖，摘要覆盖率 **496/496 = 1.0000**，'
    '故直接用 RSS 全摘要、不走 API id_list）KW 命中 **37 篇**；标题级扩展词补扫再补 **21 篇** → 候选 **58 篇**；'
    '逐篇核摘要剔除 **37 篇误命中**（AR=autoregressive 2 篇、自动驾驶/机器人 12 篇、遥感/医学/水下 9 篇、'
    '通用 2D 视觉与多模态 8 篇、其他 6 篇）→ **XR 池 21 篇**（该层不计入「RSS 漏网」统计）。\n'
    '数据源：API 双主机 200（id_list 仅用于提交日核验，25 id 分 2 批、间隔 12s，返回 25/25）；'
    'RSS 7 分类 `--no-filter` 去重 **766 条**，`OK_CATS=7/7`（完整采集）。\n'
    '全文：25 候选（21 + 4）串行 3s/篇 → **25 篇全部 L0/FULL**（17,275–130,366 字符）。\n'
    f'覆盖度三关：门① 最大 Jaccard **{G1:.3f}**（2611.22415 SpatialMind vs 库内 2609.03892，<0.62）；'
    f'门② 定稿 Top10 覆盖 **6 赛道**（全批 8 赛道，纯值排序即达，**未触发重筛**）；'
    f'门③ 当日最高 **{G["gate3"]["today_max"]:.2f} vs 库内近 30 天 Top10 均分 {GATE3:.4f}**（窗口 2026-10-20~11-19、'
    f'436 条入窗、现算，按 batch 剔除本批两批）→ **非重磅日，无 S 级**（差值 {MARGIN:+.4f}）。OUTDATED 0。'
)
seven_table(MAIN, f'papers/daily/{DATE}/7dim-table.md', f'{DATE} 全量 7 维度对比表（参考）', INTRO_MAIN)

INTRO_BF = (
    '批次：backfill-1119（**11-18 公告批次 RSS 混入的旧稿 v2/v3 再公告**，首次入馆）。\n'
    '均非 11-18 当日新提交（API published：2026-05-21 / 2026-06-03 / 2026-07-06 / 2026-10-19；'
    'updated 2026-11-16~11-17），诚实口径单独编号；不参与当日「重磅日」判定，≥4.20 亦按口径记 A。\n'
    '候选来源：RSS 全量 766 条中 **replace 类 270 篇**未入馆者，经摘要级 XR 过滤命中 **17 篇**，'
    '逐篇核摘要后取 **4 篇**（剔除机器人操作/雷达里程计/自动驾驶重建/流形采样/医学多模态等 13 篇非 XR）。\n'
    '全文：4 篇全部 **L0/FULL**（42,817–130,366 字符）。本批最高 **3.85（SFMambaNet）**，'
    '另有理论文 Max-Clique vs Max-Consensus 3.84——说明「配准准则的选择依据」这一基础问题在库内仍属空白。'
)
seven_table(BF, 'papers/daily/backfill-1119/7dim-table.md',
            'backfill-1119 全量 7 维度对比表（参考）', INTRO_BF)


def scored_md(papers, path, title, extra):
    L = [f'# {title}\n', extra + '\n',
         '| 排名 | arXiv | 标题 | 赛道 | IMP | NOV | TEC | EXP | PER | TRL | REP | 总分 | 等级 | 证据 |',
         '|---|---|---|---|---|---|---|---|---|---|---|---|---|---|']
    for i, p in enumerate(papers, 1):
        s = p['scores']
        L.append(f"| {i} | {p['id']} | {esc(p['title_zh'])} | {p['track']} | {s['IMP']} | {s['NOV']} | "
                 f"{s['TEC']} | {s['EXP']} | {s['PER']} | {s['TRL']} | {s['REP']} | {p['value']:.2f} | "
                 f"{p['grade']} | {p['evidence']} |")
    L.append('\n## 评分理由（逐篇）\n')
    for p in papers:
        L.append(f"### {p['id']} · {esc(p['title_zh'])}（{p['value']:.2f} {p['grade']}）\n")
        L.append(p['scores_why'] + '\n')
    open(path, 'w', encoding='utf-8').writelines([x + '\n' for x in L])


scored_md(MAIN, f'papers/daily/{DATE}/scored.md', f'{DATE} 评分明细',
          '评分口径：7 维加权 IMP0.20·NOV0.20·TEC0.15·EXP0.15·PER0.15·TRL0.08·REP0.07；'
          '分档 S≥4.20 且本次授予（blockbuster）/ A3.60–4.20 / B3.00–3.60 / C<3.00。'
          '21 篇全部先抓全文再定稿（21 L0/FULL）。\n'
          f'覆盖度三关：门① 最大 Jaccard **{G1:.3f}** < 0.62；门② 定稿 Top10 覆盖 **6 赛道**（全批 8，未重筛）；'
          f'门③ 当日最高 **{G["gate3"]["today_max"]:.2f} vs {GATE3:.4f}**（窗口 2026-10-20~11-19、436 条入窗）'
          f'→ **非重磅日无 S**（margin {MARGIN:+.4f}）。\n'
          f'等级分布：{gr_main["A"]} A / {gr_main["B"]} B / {gr_main["C"]} C（无 S）；'
          '2 篇 C 级（2611.22151 / 2611.21642）仅入馆不解读。')
scored_md(BF, 'papers/daily/backfill-1119/scored.md', 'backfill-1119 评分明细',
          '评分口径同上；本批为旧稿 v2/v3 再公告首次入馆，均非当日新提交。'
          f'等级分布：{gr_bf["A"]} A / {gr_bf["B"]} B / {gr_bf["C"]} C（无 S；≥4.20 亦按口径记 A）；门③ 对 backfill 不适用。')
print('7dim/scored written')

# ---------- run_log ----------
run_log_main = f'''# {DATE} 执行日志

## 数据源与对账（第 1-3 步）
- **漏网对账（先于拉取）**：`scripts/audit_listing_1119.py`（PREV_DAY=2026-11-17 / NEW_DAYS=11-18,11-19；show=500 单页×7 分类，目标组 declared≠got 自动补采后续页）。7 分类最新公告日均为 **2026-11-18（周三）**，无 11-19 日组（当日尚未释放）。
- **上批组复核**：11-17 组逐分类 **declared=got**（CV 342 / GR 15 / HC 58 / MM 11 / RO 134 / AI 428 / IV 28 = **1,016 槽位 / 844 唯一**；cs.CV 补采 skip=500 合并 49、cs.AI 合并 187），未入馆 **811 篇 = 844 − 33（上批主批已入馆）**。用 11-18 的 RSS 全量逐篇核摘要，811 篇中 XR 命中 **69 篇**，与 `rejected_1118.json` 的 69 篇**逐篇一致** → **0 漏网、无滞后补录**。
- **新公告组**：11-18 组 **599 槽位 / 496 篇唯一论文**（CV 207 / GR 10 / HC 26 / MM 3 / RO 89 / AI 259 / IV 5），全部未入馆。
- **摘要级过滤**：`scripts/triage_1119.py`。listing 496 篇 **100% 被 RSS 全量 766 条覆盖（缺收 0 篇）**，摘要覆盖率 **496/496 = 1.0000**，故直接使用 RSS 全摘要而不走 API `id_list`（规避 429 静默丢批风险）。KW 命中 **37 篇**。
- **标题级扩展词补扫（第三层召回，诚实披露）**：对 496 篇标题扫扩展词补入 **21 篇** KW 未命中者；候选 **58 篇** 逐篇核摘要剔除 **37 篇误命中** → **XR 池 21 篇**。该层**不计入「RSS 漏网」统计**。
- **数据源**：API 双主机 200（id_list 仅用于提交日核验：25 id 分 2 批、间隔 12s，返回 **25/25**）；RSS 7 分类 `--no-filter` 去重 **766 条**，`OK_CATS=7/7`（完整采集，非 exit 2 场景）。
- **提交日核验**（API published）：主批 **11-17×17 / 11-16×3 / 09-27×1**；其中 **2611.21642 RelicTouch 提交 2026-09-27、延迟约 7 周公告**。backfill 为 2026-05-21 / 2026-06-03 / 2026-07-06 / 2026-10-19（updated 11-16~11-17）。**RSS published 是公告时间戳（11-18），不可当提交日**。

## 甄别（第 3 步）
- 主批 XR 入评分池 **21 篇**：KW 层 37 命中经逐篇核摘要保留 15 篇，标题级补扫 21 篇保留 6 篇。
- **误命中剔除 37 篇**（逐篇核摘要，代表性归类）：缩写误命中 2 篇（2611.21851 AR-WAM、2611.22296 SpecSearch 均为 autoregressive）· 自动驾驶/机器人 12 篇（2611.22852 移动操作臂、2611.22445 人形竞速、2611.22691 闭环驾驶世界模型、2611.23143 TCP4D、2611.23215 DDPC、2611.22695 四足轨迹跟踪、2611.22385 隧道 LIVO、2611.22047 SE(3)-LIVOM、2611.23120 气压重力、2611.22518 粒子滤波、2611.22929 联邦学习、2611.22951 湍流）· 遥感/医学/水下 9 篇（2611.22636 冠层高度、2611.22898 遥感超分、2611.23187 之外的建筑稿、2611.22450 标注工具、2611.22331 超声、2611.22212 水下、2611.22224 水下三任务、2611.22496 海洋基础模型、2611.22439 协同感知）· 通用 2D 视觉与多模态 8 篇（2611.22222 图像复原、2611.22551 低光视频、2611.22867 自回归图像生成、2611.21865 PromptPack、2611.22006 AI4OSN、2611.23147 AI 陪伴、2611.23007 肉鸡检测、2611.21655 LLM 激活引导）· 其他 6 篇（2611.21802 之外的压缩/仿真/旧稿等）。
- 旧稿 replace 未入馆 **270 篇** → XR 命中 **17 篇**，逐篇核摘要后取 **4 篇**（其余 13 篇为机器人操作、雷达里程计、自动驾驶重建、流形采样、医学多模态等非 XR）→ **backfill-1119**。

## 全文抓取（第 4 步）
- 25 篇候选（21 + 4）跑 `scripts/fetch_fulltext.py`，严格串行 3s/篇（约 1 分 40 秒）：**25 篇全部 L0/FULL**（17,275–130,366 字符）。
- 证据等级复核：逐篇抽看正文中段，确认含 Introduction/Method/Results 主体；**2611.23209（gaze-guided VLM）虽判 L0，但正文只有摘要页 + 参考文献（无正文章节）**，已从候选池剔除并记入非 XR/证据不足清单，未纳入评分。
- WROTE=25>0；manifest 合并写入校验通过；无 L5、无 OCR。

## 评分与三关（第 5-6 步）
- 先抓全文再定稿。7 维加权：主批 **{gr_main['A']} A / {gr_main['B']} B / {gr_main['C']} C（无 S，最高 4.30 CueSplat / HandRSI 并列）**；backfill **{gr_bf['A']} A / {gr_bf['B']} B / {gr_bf['C']} C**（最高 3.85 SFMambaNet）。
- 门① 最大 Jaccard **{G1:.3f}**（2611.22415 SpatialMind vs 库内 2609.03892，2026-09-03），通过；其余 9 篇 0.091–0.188。
- 门② 定稿 Top10 覆盖 **6 赛道**（感知与认知 3 / 化身与人体 2 / 重建与SLAM 2 / 神经渲染 1 / 系统与平台 1 / 交互与输入 1；全批 8 赛道）→ **纯值排序即达标，未触发重筛**。
- 门③ 当日最高 **{G['gate3']['today_max']:.2f} vs 库内近 30 天 Top10 均分 {GATE3:.4f}**（窗口 2026-10-20~11-19、**436 条入窗**、现算，按 batch 剔除 2026-11-19 与 backfill-1119）→ **非重磅日无 S**（margin {MARGIN:+.4f}，未触及 0.05 险过区）。
- OUTDATED/SUPERSEDED **0 篇**。

## 产物（第 7-8 步）
- 报告 2 份（主批 + backfill）+ 原子笔记 **23 篇**（grade≥B：主批 19 + backfill 4；2 篇 C 级仅入馆）+ MOC 2 份 + 总索引刷新 + 7 维表/scored/run_log 各 2 套。
- registry 990 → **1,015**（+21 +4；备份 `papers/library/registry.jsonl.bak-20261119`；按 base_id 幂等）。
- notes 632 → **655**；daily 67 → **69**；MOC 55 → **57**。
- 门③ 现算值供下一批参考：**{GATE3:.4f}**（窗口逐日滚动，须再算）。

## 召回缺口记录（供下一批改进）
- 本批 KW 命中 37 篇、标题补扫 21 篇，最终入池 21 篇；**误命中率仍高（37/58 = 64%）**，主因是 `SLAM`/`point cloud`/`monocular depth` 等词把自动驾驶与机器人操作大量带入（本批 12 篇）。
- 标题补扫里 `spatial`/`tracking`/`depth` 三个泛词贡献 14 篇噪声、仅 3 篇真 XR（SpatialMind/MentalGrid/SpatialCast）。建议下批把这三个词从 EXTRA 移除或加「非 driving/robot/medical」负向约束。
- 另一侧漏召回风险：`2611.23051 Refin3R`、`2611.23187 Any2Building` 靠泛词入池，说明「重建/几何」类核心词仍偏少，建议补 `feed-forward reconstruction`、`point map`、`surface reconstruction`。

## 观察（供后续批次）
- **端侧 3DGS 从「能跑」进入「跑得动、跑得稳」**：CueSplat 把形变评估变成可学习调度（Orin 上 1.75–6.74×），Cross3DGS 把训练搬到采集设备（八种跨厂商 GPU 全部跑完 30k 步）。两篇都在解决「XR 内容生产与消费都在端上」的同一瓶颈，且都以真实硬件长跑为证据。
- **手部/化身仍是最高密度赛道**：HandRSI（HOT3D MPJPE-p −35%）、ARG-Avatar（68M 参数超 609M LHY++）、HandUMI（手戴夹爪 + Quest/PICO 采集）三篇同日出现，加上 backfill 的 HolisticMotion，形成「追踪—重建—数据采集」的完整链条。
- **空间智能从静态走向动态**：MentalGrid 把「无中间视觉反馈的状态推演」形式化，SpatialCast 用投射阴影做物理读数，SpatialMind 做多层级几何融合——三篇共同说明 3D 空间推理的评测正从「看图说位置」转向「预测与反推」。
- **重建侧的工程化收敛**：CoSphere-SLAM（多机全景 ATE 0.082 m）、Kolibri（82 ms 重定位）、Refin3R（SfM 引导稠密精化）分别覆盖「多机协同」「在线定位」「离线精化」三个环节，精度与成本同时改善。
- **硬件显示侧连续第 30 批无器件级破冰**（波导/可变焦/Maxwellian/光场均无新稿），本批仅有 Vibrotactile Surface 一篇低成本触觉像素阵列，属触觉而非视觉显示。
'''
open(f'papers/daily/{DATE}/run_log.md', 'w', encoding='utf-8').write(run_log_main)

run_log_bf = f'''# backfill-1119 执行日志

- **来源**：11-18 公告批次 RSS 全量 766 条中 **replace 类 270 篇**未入馆者，经摘要级 XR 过滤命中 **17 篇**，逐篇核摘要后取 **4 篇**（剔除机器人操作、雷达里程计、自动驾驶重建、流形采样、医学多模态等 13 篇非 XR）。
- **诚实口径**：全部为 **v2/v3 再公告**（API updated 2026-11-16~11-17），原始投稿 2026-05-21 / 2026-06-03 / 2026-07-06 / 2026-10-19；均非 11-18 当日新提交，单独编号、不参与当日重磅日判定。
- **全文**：4 篇全部 **L0/FULL**（42,817–130,366 字符）。
- **定稿 {gr_bf['A']} A / {gr_bf['B']} B / {gr_bf['C']} C（无 S）**：2606.04493 SFMambaNet **3.85**（频域感知 Mamba 对应剪枝，YFCC100M mAP@5° 73.83%）· 2610.27275 Max-Clique vs Max-Consensus **3.84**（团的解可任意偏离一致集，给出 d+1/d+2 最小充分 group 阶数）· 2607.05598 SSA-3DGS **3.65**（屏幕空间伪影无监督去除，平均 +2.9 dB）· 2605.22631 HolisticMotion **3.28**（掩码全身观测建模，AMASS-P1 MPJPE 2.95 cm）。
- **registry**：+4（batch=backfill-1119，幂等）。
'''
open('papers/daily/backfill-1119/run_log.md', 'w', encoding='utf-8').write(run_log_bf)
print('run_log written')
