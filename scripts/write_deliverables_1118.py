# -*- coding: utf-8 -*-
"""2026-11-18 产物（第一部分）：7 维表 / scored.md / run_log.md（主批 + backfill-1118）。

诚实口径：公告日 2026-11-17（周二）≠ 拉取日 2026-11-18（周三 02:30）。
门③ 险过：机械 heavy_day=true，但差值 0.027 < 0.05，按 skill §8.6.3 不授予 S（详见 gates_1118.json）。
"""
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from grade_caliber import assign_grade  # noqa: E402

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
os.chdir(ROOT)

D = json.load(open('data/scored_1118.json', encoding='utf-8'))
MAIN = [p for p in D if p['batch'] == '2026-11-18']
BF = [p for p in D if p['batch'] == 'backfill-1118']
MAIN.sort(key=lambda r: (-r['value'], -r['scores']['IMP'], -r['scores']['NOV'], r['id']))
G = json.load(open('data/gates_1118.json', encoding='utf-8'))
TOP10_ORDER = G['top10']
DATE, ANN = '2026-11-18', '2026-11-17'
HEAVY = bool(G['gate3']['blockbuster'])          # 险过不授予 S
HEAVY_RAW = bool(G['gate3']['heavy_day_raw'])
GATE3, G1, MARGIN = G['gate3']['top10_mean'], G['gate1']['max_jaccard'], G['gate3']['margin']
MANIFEST = json.load(open('data/fulltext/_manifest.json', encoding='utf-8'))
for p in MAIN + BF:
    p['level'] = MANIFEST[p['id']]['level']
    p['evidence'] = MANIFEST[p['id']]['evidence']
    p['announce'] = 'replace' if p['batch'].startswith('backfill') else 'new'
    p['status'] = 'CURRENT'
    p['grade'] = assign_grade(p['value'], p['batch'], HEAVY)
TOP10 = [next(p for p in MAIN if p['id'] == pid) for pid in TOP10_ORDER]
assert [p['id'] for p in TOP10] == TOP10_ORDER
assert len(MAIN) == 33 and len(BF) == 6, (len(MAIN), len(BF))
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
os.makedirs('papers/daily/backfill-1118', exist_ok=True)


def seven_table(papers, path, title, intro):
    lines = [f'# {title}\n', intro + '\n', TBL_HEAD]
    for p in papers:
        lines.append(dim_row(p) + '\n')
    open(path, 'w', encoding='utf-8').writelines(lines)


INTRO_MAIN = (
    '批次：2026-11-18（**2026-11-17（周二）公告批次**——公告日 11-17 ≠ 拉取日 11-18（周三 02:30），诚实口径）。'
    'API published 核验主批提交日 **11-16×16 / 11-15×8 / 11-14×3 / 11-13×3 / 11-10×1 / 11-06×1 / 10-31×1**'
    '（2611.18679 提交 10-31、延迟约 17 天公告；RSS published 为公告时间戳，不可当提交日）。\n'
    '漏网对账（先于拉取，`scripts/audit_listing_1118.py`，show=500 单页×7 分类 + 目标组 declared≠got 自动补页，'
    'PREV_DAY=11-16 / NEW_DAYS=11-17,11-18）：7 分类最新公告日均为 **2026-11-17**，无 11-18 日组；'
    '11-16 组复采逐分类 **declared=got**（CV 91 / GR 5 / HC 13 / MM 0 / RO 38 / AI 164 / IV 9 = **320 槽位 / 271 唯一**，'
    'cs.AI 补采 skip=500 合并 92），未入馆 **258 篇 = 271 − 13（上批主批已入馆）**，与 11-17 运行候选集合一致 → **0 漏网、无滞后补录**。\n'
    '**11-17 组 1,016 槽位 / 844 篇唯一论文**（CV 342 / GR 15 / HC 58 / MM 11 / RO 134 / AI 428 / IV 28，全部未入馆）'
    '→ 摘要级 XR 过滤（`scripts/triage_1118.py`；listing 844 篇 100% 被 RSS 全量 1,323 条覆盖，摘要覆盖率 **844/844 = 1.0000**，'
    '故直接用 RSS 全摘要、不走 API id_list）KW 命中 **66 篇**；标题级扩展词补扫再补 **36 篇** → 候选 **102 篇**；'
    '逐篇核摘要剔除 **69 篇误命中** → **XR 池 33 篇**（该层不计入「RSS 漏网」统计）。\n'
    '数据源：API 双主机 200（id_list 仅用于提交日核验，39 id 分 3 批 13 篇、间隔 12s，返回 39/39）；'
    'RSS 7 分类 `--no-filter` 去重 **1,323 条**，`OK_CATS=7/7`（完整采集）。\n'
    '全文：39 候选（33 + 6）串行 3s/篇 → **35 篇 L0/FULL**（24,146–414,440 字符）+ **4 篇 L1/PARTIAL**'
    '（2611.18822 / 2611.20196 / 2611.20570 / 2611.21485：arXiv HTML 404、ar5iv 仅返摘要页且无正文节，'
    '沙箱无 PDF 解析库 → 摘要级评估，已在笔记与报告中显式声明）。\n'
    f'覆盖度三关：门① 最大 Jaccard **{G1:.3f}**（2611.21060 vs 库内 2605.18553，<0.62）；'
    f'门② 定稿 Top10 覆盖 **6 赛道**（全批 10 赛道，纯值排序即达，**未触发重筛**）；'
    f'门③ 当日最高 **{G["gate3"]["today_max"]:.2f} vs 库内近 30 天 Top10 均分 {GATE3:.4f}**（窗口 2026-10-19~11-18、'
    f'410 条入窗、现算）→ 机械 heavy_day=true，但**差值仅 {MARGIN:.3f} < 0.05**，按 skill §8.6.3「险过不得宣称重磅工作」，'
    f'**本期不记 S**：4 篇 ≥4.20（2611.21143 / 2611.21479 / 2611.19773 / 2611.20797）记 A 并注明达线。OUTDATED 0。'
)
seven_table(MAIN, f'papers/daily/{DATE}/7dim-table.md', f'{DATE} 全量 7 维度对比表（参考）', INTRO_MAIN)

INTRO_BF = (
    '批次：backfill-1118（**11-17 公告批次 RSS 混入的旧稿 v2/v3 再公告**，首次入馆）。\n'
    '均非 11-17 当日新提交（API published：2025-11-20 / 2026-05-07 / 2026-05-10 / 2026-07-04 / 2026-09-25 / 2026-11-13），'
    '诚实口径单独编号；不参与当日「重磅日」判定，≥4.20 亦按口径记 A。\n'
    '候选来源：RSS 全量 1,323 条中 **replace 类 479 篇**未入馆者，经摘要级 XR 过滤命中 **32 篇**，'
    '逐篇核摘要后取 **6 篇**（剔除机器人抓取/自动驾驶定位/医学骨重建/农业 NVS 等 26 篇非 XR）。\n'
    '全文：6 篇全部 **L0/FULL**（51,940–86,581 字符）。本批最高 **3.93（MACRO）**，高于主批最高 4.43 之外的多数主批论文，'
    '说明「特写渲染的参考图对齐」是被主批新稿掩盖的一条实用线。'
)
seven_table(BF, 'papers/daily/backfill-1118/7dim-table.md',
            'backfill-1118 全量 7 维度对比表（参考）', INTRO_BF)


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
          '分档 S≥4.2 / A3.6–4.2 / B3.0–3.6 / C<3.0。33 篇全部先抓全文再定稿（29 L0/FULL + 4 L1/PARTIAL）。\n'
          f'覆盖度三关：门① 最大 Jaccard **{G1:.3f}** < 0.62；门② 定稿 Top10 覆盖 **6 赛道**（全批 10，未重筛）；'
          f'门③ 当日最高 **{G["gate3"]["today_max"]:.2f} vs {GATE3:.4f}**（窗口 2026-10-19~11-18、410 条入窗）'
          f'→ 机械 heavy_day=true 但差值 {MARGIN:.3f} < 0.05，按 §8.6.3 **不记 S**。\n'
          f'等级分布：{gr_main["A"]} A / {gr_main["B"]} B / {gr_main["C"]} C（无 S）；'
          '7 篇 C 级（2611.18822 / 2611.18979 / 2611.19765 / 2611.20245 / 2611.20568 / 2611.20570 / 2611.21233）仅入馆不解读。')
scored_md(BF, 'papers/daily/backfill-1118/scored.md', 'backfill-1118 评分明细',
          '评分口径同上；本批为旧稿 v2/v3 再公告首次入馆，均非当日新提交。'
          f'等级分布：{gr_bf["A"]} A / {gr_bf["B"]} B / {gr_bf["C"]} C（无 S；≥4.20 亦按口径记 A）；门③ 对 backfill 不适用。')
print('7dim/scored written')

# ---------- run_log ----------
run_log_main = f'''# {DATE} 执行日志

## 数据源与对账（第 1-3 步）
- **漏网对账（先于拉取）**：`scripts/audit_listing_1118.py`（PREV_DAY=2026-11-16 / NEW_DAYS=11-17,11-18；show=500 单页×7 分类，目标组 declared≠got 自动补采后续页）。7 分类最新公告日均为 **2026-11-17（周二）**，无 11-18 日组（当日尚未释放）。
- **上批组复核**：11-16 组逐分类 **declared=got**（CV 91 / GR 5 / HC 13 / MM 0 / RO 38 / AI 164 / IV 9 = **320 槽位 / 271 唯一**；cs.AI 补采 skip=500 合并 92），未入馆 **258 篇 = 271 − 13（上批主批已入馆）**，与 11-17 运行的 271 篇候选集合一致 → **0 漏网、无滞后补录**。
- **新公告组**：11-17 组 **1,016 槽位 / 844 篇唯一论文**（CV 342 / GR 15 / HC 58 / MM 11 / RO 134 / AI 428 / IV 28），全部未入馆。
- **摘要级过滤**：`scripts/triage_1118.py`。listing 844 篇 **100% 被 RSS 全量 1,323 条覆盖（缺收 0 篇）**，摘要覆盖率 **844/844 = 1.0000**，故直接使用 RSS 全摘要而不走 API `id_list`（规避 11-12 的 429 静默丢批风险）。KW 命中 **66 篇**。
- **标题级扩展词补扫（第三层召回，诚实披露）**：对 844 篇标题扫扩展词补入 **36 篇** KW 未命中者；候选 **102 篇** 逐篇核摘要剔除 **69 篇误命中** → **XR 池 33 篇**。该层**不计入「RSS 漏网」统计**。
- **数据源**：API 双主机 200（id_list 仅用于提交日核验：39 id 分 3 批 ×13、间隔 12s，返回 **39/39**）；RSS 7 分类 `--no-filter` 去重 **1,323 条**，`OK_CATS=7/7`（完整采集，非 exit 2 场景）。
- **提交日核验**（API published）：主批 **11-16×16 / 11-15×8 / 11-14×3 / 11-13×3 / 11-10×1 / 11-06×1 / 10-31×1**；其中 **2611.18679 提交 10-31、延迟约 17 天公告**。backfill 为 2025-11-20 / 2026-05-07 / 2026-05-10 / 2026-07-04 / 2026-09-25 / 2026-11-13（updated 11-14~11-16）。**RSS published 是公告时间戳（11-17），不可当提交日**。

## 甄别（第 3 步）
- 主批 XR 入评分池 **33 篇**：KW 层 66 命中中的真 XR 24 篇 + 标题级补扫补入 9 篇（逐篇核摘要确认）。
- **误命中剔除 69 篇**（逐篇核摘要，代表性归类）：医学/生物影像 6 篇（2611.18766 胎儿 MRI 神经高斯 / 2611.18756 空间转录组 / 2611.19066 胼胝体参数化 / 2611.18744 鼠脑脂质 3D 重建 / 2611.16869 X 光骨重建 等）· 机器人操作与抓取 8 篇（2611.18976 TMA / 2611.20692 ARMFUL / 2611.18919 点云抓取 / 2611.21104 GRAZE / 2611.21057 WiTac 等）· 自动驾驶/雷达/V2X 9 篇（2611.19830 / 2611.19857 / 2611.20203 / 2611.21162 / 2611.20737 / 2611.20241 等）· 无人机/农业/环境 5 篇（2611.20502 玉米 3D / 2611.19703 空气污染 / 2611.21311 A2A-UAV 等）· 通用 LLM/智能体/HCI 6 篇（2611.18642 / 2611.20935 / 2611.21125 / 2611.21405 等）· 通用位姿/深度/点云分割 9 篇（2611.20361 / 2611.20518 / 2611.20797 之外的分割与检测稿）· 其余（音频-视觉、手写识别、电路、气象、遥感等）26 篇。完整剔除清单见 `data/rejected_1118.json`。
- 旧稿 replace 未入馆 **479 篇** → XR 命中 **32 篇**，逐篇核摘要后取 **6 篇**（其余 26 篇为机器人抓取/水下定位/自动驾驶/医学骨重建/农业 NVS 等非 XR）→ **backfill-1118**。

## 全文抓取（第 4 步）
- 39 篇候选（33 + 6）跑 `scripts/fetch_fulltext.py`，严格串行 3s/篇（约 2 分 33 秒）：**35 篇 L0/FULL**（24,146–414,440 字符）+ **4 篇 L1/PARTIAL**。
- **人工复核改判**：2611.18822 / 2611.20196 / 2611.20570 / 2611.21485 脚本初判 L1/FULL（4,567–5,535 字符），抽看正文中段确认 ar5iv 仅返回**摘要页**（含 metadata + 摘要 + 样板，无任何正文章节），arXiv HTML 均 404（v1 复核），已改判 `evidence=PARTIAL` 并在 manifest 加 note；沙箱无 pdfminer/pypdf，L2 PDF 路径不可用，按摘要级评估并显式声明。
- WROTE=39>0；manifest 合并写入校验通过；无 L5、无 OCR。

## 评分与三关（第 5-6 步）
- 先抓全文再定稿。7 维加权：主批 **{gr_main['A']} A / {gr_main['B']} B / {gr_main['C']} C（无 S，最高 4.43 WinDEX）**；backfill **{gr_bf['A']} A / {gr_bf['B']} B / {gr_bf['C']} C**（最高 3.93 MACRO）。
- 门① 最大 Jaccard **{G1:.3f}**（2611.21060 MetricHand vs 库内 2605.18553，2026-10-27），通过；其余 9 篇 0.118–0.214。
- 门② 定稿 Top10 覆盖 **6 赛道**（化身与人体 2 / 世界模型与仿真 2 / 重建与SLAM 2 / 神经渲染 2 / 内容生成 1 / 感知与认知 1；全批 10 赛道）→ **纯值排序即达标，未触发重筛**。
- 门③ 当日最高 **{G['gate3']['today_max']:.2f} vs 库内近 30 天 Top10 均分 {GATE3:.4f}**（窗口 2026-10-19~11-18、**410 条入窗**、现算）→ **机械 heavy_day=true，但差值仅 {MARGIN:.3f} < 0.05**；按 skill §8.6.3「险过不得宣称重磅工作」，本次以 `blockbuster=false` 参与档位判定，**4 篇 ≥4.20 记 A 并注明达线，S 不授予**。机械值保留于 `gates_1118.json.gate3.heavy_day_raw` 供复核。
- OUTDATED/SUPERSEDED **0 篇**。

## 产物（第 7-8 步）
- 报告 2 份（主批 + backfill）+ 原子笔记 **31 篇**（grade≥B：主批 26 + backfill 5；7 篇 C 级仅入馆）+ MOC 2 份 + 总索引刷新 + 7 维表/scored/run_log 各 2 套。
- registry 951 → **990**（+33 +6；备份 `papers/library/registry.jsonl.bak-20261118`；按 base_id 幂等）。
- notes 601 → **632**；daily 65 → **67**；MOC 53 → **55**。
- 门③ 现算值供下一批参考：**{GATE3:.4f}**（窗口逐日滚动，须再算）。

## 召回缺口记录（供下一批改进）
- 本批 KW 表已补入 11-17 记录的缺口词（`tactile`/`taxel`、`signed distance`、`meshing`、`affine correspondence`、`bundle adjustment`、`image-based rendering`、`light field super-resolution`、`single-photon`/`SPAD`、`monocular depth`、`point cloud` 等 26 个），KW 命中从 11-17 的 11 篇升到 **66 篇**，但**噪声同步上升**（缩略词 `SLAM`/`IMU`/`6-DoF` 把机器人操作与自动驾驶大量带入），标题级补扫仍贡献 9 篇真 XR。
- 结论：**KW 层负责召回、人工核摘要负责精度**的分工不变；下一批可考虑给 `SLAM`/`point cloud` 增加「非自动驾驶」负向过滤词（V2X、LiDAR odometry、driving）。

## 观察（供后续批次）
- **手部成为本批最强主线**：WinDEX（1000 h 野外标注、43.61 FPS 离线 / 171 FPS 流式、策略成功率 61% vs WiLoR 8%）与 MetricHand（HOT3D 世界系 MPJPE 20.58 mm，−28.7%）同日出现，加上 backfill 的 EgoEMG、DoF-Query，说明「手部度量重建 + 遥操作数据飞轮」正在从单点方法转为工程闭环。
- **世界模型开始被「手」控制**：LynnReal-Hand 用三阶段训练把 MANO 手部监督塞进视频世界模型（FVD −38.3%、540p 单卡 18 FPS、权重开源），JEPA4R 则把 JEPA 搬到 4D 点云潜空间（MetaWorld 98.4%）。两条路线共同指向「交互可控」而非「画面好看」。
- **3DGS 的「物理化」与「可信化」**：CiGS 把 GS 变成热传导 BIE 的求解载体（内部温度误差 0.17% 量程），QuantileGS 给逐像素共形误差界（LLFF 覆盖率 69.6%→89.6%），Mask Is Not the Object 纠正「掩码=物体」的监督偏差（mRDE −30%）。GS 正从渲染原语变成可计算、可度量的场景表示。
- **硬件显示侧终于有量化锚**：WL-Headset Law 的 HRMD 库（241 款）把 PPD 估计误差从 14.8% 压到 3.2%，并给出「30 g 级设备 2035 年 60 PPD」的外推——这是库内继 CVQPG、HoOPOE 之后第三篇硬件/显示侧论文，但仍是「度量与预测」而非「器件与光学设计」。
'''
open(f'papers/daily/{DATE}/run_log.md', 'w', encoding='utf-8').write(run_log_main)

run_log_bf = f'''# backfill-1118 执行日志

- **来源**：11-17 公告批次 RSS 全量 1,323 条中 **replace 类 479 篇**未入馆者，经摘要级 XR 过滤命中 **32 篇**，逐篇核摘要后取 **6 篇**（剔除机器人抓取、水下/卫星定位、自动驾驶、医学骨重建、农业 NVS 等 26 篇非 XR）。
- **诚实口径**：全部为 **v2/v3 再公告**（API updated 2026-11-14~11-16），原始投稿 2025-11-20 / 2026-05-07 / 2026-05-10 / 2026-07-04 / 2026-09-25 / 2026-11-13；均非 11-17 当日新提交，单独编号、不参与当日重磅日判定。
- **全文**：6 篇全部 **L0/FULL**（51,940–86,581 字符）。
- **定稿 {gr_bf['A']} A / {gr_bf['B']} B / {gr_bf['C']} C（无 S）**：2607.03875 MACRO **3.93**（深度平面裁剪参考图，DINOv2 距离 −26%、免训练）· 2511.16349 LoC-IN **3.81**（神经渲染 LiDAR 地图定位，0.59 cm、100% 定位率）· 2611.18267 TetraCoder **3.58**（自适应四面体编码，提网格快 6.4×）· 2605.09586 DeformMaster **3.55**（物理-神经形变世界模型，IoU 0.748）· 2605.05712 EgoEMG **3.49**（25.9 h 双侧 sEMG + 第一视角数据集）· 2609.31117 XR 笔式控制接口 **2.20**（10 人四接口对比，C 级仅入馆）。
- **registry**：+6（batch=backfill-1118，幂等）。
'''
open('papers/daily/backfill-1118/run_log.md', 'w', encoding='utf-8').write(run_log_bf)
print('run_log written')
