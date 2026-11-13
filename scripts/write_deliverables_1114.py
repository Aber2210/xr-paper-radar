# -*- coding: utf-8 -*-
"""2026-11-14 产物生成：主批（11-13 公告批次 20 篇）+ backfill-1114（8 篇旧稿 v2/v3 再公告）。

诚实口径：公告日 2026-11-13（周五 00:00 UTC 释放）≠ 拉取日 2026-11-14（周六 02:30）。
关键：**11-12（周四）公告批次跳空**，11-11（周三）与 11-12（周四）两日提交一并并入 11-13 组释放
（API published：主批 11-11×11 / 11-12×9）；RSS published 是公告时间戳（11-13），不可当提交日。
backfill 原始投稿 2025-08-22 ~ 2026-07-15，v2/v3 于 2026-11-11（7 篇）/ 11-12（1 篇）更新后再公告。
消费 data/scored_1114.json；registry 幂等追加（先备份，in_top10 按定稿显式设置）。
"""
import glob
import json
import os
import re
import shutil

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
os.chdir(ROOT)
D = json.load(open('data/scored_1114.json', encoding='utf-8'))
MAIN = D['main']
BF = D['backfill']
TOP10_IDS = set(D['top10_ids'])
TOP10_ORDER = list(D['top10_ids'])
DATE, ANN = '2026-11-14', '2026-11-13'
GATE3 = D['gate3_mean']
MANIFEST = json.load(open('data/fulltext/_manifest.json', encoding='utf-8'))
for p in MAIN + BF:
    p['level'] = MANIFEST[p['id']]['level']
    p['evidence'] = MANIFEST[p['id']]['evidence']
    p['announce'] = 'replace' if p['batch'].startswith('backfill') else 'new'
TOP10 = [p for pid in TOP10_ORDER for p in MAIN if p['id'] == pid]
assert [p['id'] for p in TOP10] == TOP10_ORDER
assert len(MAIN) == 20 and len(BF) == 8, (len(MAIN), len(BF))


def esc(s):
    return str(s).replace('|', '/')


def dim_row(p, star):
    s = p['scores']
    return (f"| {p['id']} | {esc(p['title_zh'])} {'⭐' if star else ''} | {p['track']} | "
            f"{s['IMP']} | {s['NOV']} | {s['TEC']} | {s['EXP']} | {s['PER']} | {s['TRL']} | {s['REP']} | "
            f"{p['value']:.2f} | {p['grade']} | {p['evidence']} | {p['announce']} |")


TBL_HEAD = ('| arXiv | 标题 | 赛道 | IMP | NOV | TEC | EXP | PER | TRL | REP | 总分 | 等级 | 证据 | 公告类型 |\n'
            '|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|\n')
os.makedirs(f'papers/daily/{DATE}', exist_ok=True)
os.makedirs('papers/daily/backfill-1114', exist_ok=True)


def seven_table(papers, path, title, intro):
    lines = [f'# {title}\n', intro + '\n', TBL_HEAD]
    for p in papers:
        lines.append(dim_row(p, p['id'] in TOP10_IDS) + '\n')
    open(path, 'w', encoding='utf-8').writelines(lines)


INTRO_MAIN = (
    '批次：2026-11-14（**2026-11-13（周五）公告批次**——公告日 11-13 ≠ 拉取日 11-14（周六 02:30），诚实口径）。'
    '**11-12（周四）公告批次跳空**（工作日跳空第 2 次，首次为 10-29），11-11（周三）与 11-12（周四）两日提交并入 11-13 组释放：'
    '主批 20 篇中 API published 为 11-11×11 / 11-12×9。\n'
    '漏网对账（先于拉取，`scripts/audit_listing_1114.py`，show=500 单页×7 分类 + 目标组 declared≠got 自动补页，PREV_DAY=11-11 / NEW_DAYS=11-12,11-13）：'
    '7 分类最新公告日均为 **2026-11-13**，**不存在 11-12 日组**（跳空在 listing 侧可见）；11-11 组复采逐分类 **declared=got**'
    '（CV 149 / GR 6 / HC 34 / MM 14 / RO 69 / AI 248 / IV 12 = 532 槽位；cs.AI 补采 skip=500 合并 69 条），'
    '未入馆 **421 篇与 11-13 运行集合逐篇一致（diff 0）**，摘要级 13 篇命中与上批已剔 13 篇 id 逐篇一致 → **0 漏网、无滞后补录**。\n'
    '**11-13 组 601 篇唯一论文**（695 槽位：CV 196 / GR 6 / HC 43 / MM 2 / RO 106 / AI 321 / IV 21，全部未入馆）'
    '→ 摘要级 XR 过滤（`scripts/filter_missed_1114.py`，50 id/批 + 12s，meta fetched **601/601**，覆盖率 1.0000）'
    'KW 命中 **43 篇**；另经标题级补充扫描补入 KW 未命中的 5 篇（EG360 / TTB / VR 语言学习 / V-JEPA 多视图重建 / SCR-Mamba），候选池 **20 篇**。\n'
    '数据源：API 双主机可用（id_list 摘要级过滤）；RSS 7 分类去重 **979** → KW 命中 **67** = **43 篇 11-13 公告组真新提交**（与 listing 摘要级 43 篇**双向差集 0**）+ '
    '**17 篇旧稿 v2/v3 再公告未入馆**（8 篇 XR → backfill-1114 + 9 篇非 XR）+ **7 篇库内 v2**。'
    '**注意：两渠道一致性仅在关键词层（43=43）；标题级补扫的 5 篇不属关键词层，故候选池大于关键词层 XR 子集（15 篇）。**\n'
    '全文：28 篇候选（20 + 8）串行 3s/篇：**28 篇全部 L0/FULL**（43,212–171,293 字符），无 PARTIAL / L5 / OCR。\n'
    '覆盖度三关：门① 最大 Jaccard **0.082**（2512.10095 vs 库内 2609.23509，<0.62；主批内最大 0.071，2611.16840 vs 2610.17513）；'
    '门② 纯值 Top10 仅 **4 赛道**（重建与SLAM×6）→ **触发一次重筛**：剔除重复赛道最低分 SteinPnP 3.50，回补未覆盖赛道最高分 MRxD 3.17（空间计算与UI）'
    '→ **定稿 Top10 覆盖 5 赛道**；门③ 当日最高 **4.15 < 库内近 30 天 Top10 均分 4.4100**（窗口 2026-10-15~11-14、428 条入窗、现算）'
    '→ **非重磅日，无 S 级**。OUTDATED 0。'
)
seven_table(MAIN, f'papers/daily/{DATE}/7dim-table.md', f'{DATE} 全量 7 维度对比表（参考）', INTRO_MAIN)

INTRO_BF = (
    '批次：backfill-1114（**11-13 公告批次 RSS 混入的旧稿 v2/v3 再公告**，首次入馆；'
    '原始投稿 2025-08-22 ~ 2026-07-15，v2/v3 于 2026-11-11（7 篇）/ 11-12（ENIGMA-360 v3）更新后再公告）。\n'
    '均非 11-13 当日新提交，诚实口径单独编号；不参与当日「重磅日」判定，≥4.2 亦按口径记 A。\n'
    '候选 8 篇：2603.01178 riMESA（v2，2026-03-01 首发）/ 2607.14203 Instant NuRec（v2，2026-07-15）/ '
    '2510.03857 OMG4（v2，2025-10-04）/ 2605.21714 AVI-HT（v2，2026-05-20）/ 2603.09741 ENIGMA-360（v3，2026-03-10）/ '
    '2607.05243 GUSH3R（v2，2026-07-06）/ 2508.16731 COSMO-Bench（v3，2025-08-22）/ 2512.10095 ReflFlow（v2，2025-12-10）。\n'
    '同批另 9 篇旧稿经摘要核实非 XR 剔除（MedGS 医学 / BLaFA 抓取 / 空间句法户型生成 / 虚拟夹具 / 液体防溢控制 / '
    '黎曼流形采样规划 / VLA 推理解码加速 / LLM 连续扩散 / SWAM 世界动作模型）。\n'
    '全文：8 篇全部 L0/FULL（47,054–149,662 字符）。本批最高 **4.50（riMESA）**——若计入主批将越过门③ 线，但按口径 backfill 不参与重磅日判定、一律不评 S。'
)
seven_table(BF, 'papers/daily/backfill-1114/7dim-table.md', 'backfill-1114 全量 7 维度对比表（参考）', INTRO_BF)


# ---------- scored.md ----------
def scored_md(papers, path, title, extra):
    L = [f'# {title}\n', extra + '\n', '| 排名 | arXiv | 标题 | 赛道 | 总分 | 等级 | 证据 | 公告类型 |',
         '|---|---|---|---|---|---|---|---|']
    for i, p in enumerate(papers, 1):
        L.append(f"| {i} | {p['id']} | {esc(p['title_zh'])} | {p['track']} | {p['value']:.2f} | {p['grade']} | {p['evidence']} | {p['announce']} |")
    open(path, 'w', encoding='utf-8').writelines([x + '\n' for x in L])


scored_md(MAIN, f'papers/daily/{DATE}/scored.md', f'{DATE} 评分明细',
          '评分口径：7 维加权 IMP0.20·NOV0.20·TEC0.15·EXP0.15·PER0.15·TRL0.08·REP0.07；分档 S≥4.2 / A3.6–4.2 / B3.0–3.6 / C<3.0。'
          '全部基于全文证据定稿（20 篇全 L0/FULL）。\n'
          '覆盖度三关：门① 最大 Jaccard 0.082 < 0.62（通过；主批内最大 0.071）；'
          '门② 纯值 Top10 仅 4 赛道 → **重筛一次**：剔除重复赛道最低分 SteinPnP 3.50，回补空间计算与UI 最高分 MRxD 3.17 → 定稿 5 赛道；'
          '门③ 当日最高 4.15 < 库内近 30 天 Top10 均分 4.4100（窗口 2026-10-15~11-14、428 条入窗、现算）→ **非重磅日，无 S 级**。\n'
          '主会话校准：① 2611.15153 MatrixSplat TRL 4→3（正文仅「will release」、无仓库，按 rubric 未满足「开源代码」）；'
          '② 2611.17331 TTB TRL 4→3（仅项目页有结果可视化，无代码）；③ 2611.16793 EG360 赛道 系统与平台→重建与SLAM（深度估计属几何重建）；'
          '④ 其余沿用子代理评分，逐条核对 scores_why 与正文数字（MatrixSplat 599.9/702.6/510.9 FPS、riMESA 45.09% vs 352.81%/787.30%、'
          'Instant NuRec 28.26 dB/+2.01 dB 已回文核对）。\n'
          'OUTDATED/SUPERSEDED 0 篇。等级分布：6 A / 9 B / 5 C（无 S）。')

scored_md(BF, 'papers/daily/backfill-1114/scored.md', 'backfill-1114 评分明细',
          '评分口径同上；本批为旧稿 v2/v3 再公告首次入馆，均非当日新提交。\n'
          '等级分布：4 A / 4 B；最高 **2603.01178 riMESA 4.50**（达 S 线但 backfill 不参与重磅日判定，按口径记 A）。门③ 对 backfill 不适用。')

# ---------- run_log ----------
run_log_main = f'''# {DATE} 执行日志

## 数据源与对账（第 1-3 步）
- **漏网对账（先于拉取）**：`scripts/audit_listing_1114.py`（PREV_DAY=2026-11-11 / NEW_DAYS=2026-11-12,2026-11-13；show=500 单页×7 分类，目标组 declared≠got 自动补采后续页，continued/last 声明兼容）。
- **跳空确认**：7 分类最新公告日均为 **2026-11-13**，**不存在 2026-11-12 日组**——与 11-13 运行五重互证（listing + 缓存穿透 + pastweek + 跨学科四分类 + API 区间 0 篇）的「11-12 公告批次未释放」结论一致，本日兑现延迟释放。
- **上批组复核**：11-11 组逐分类 **declared=got**（CV 149 / GR 6 / HC 34 / MM 14 / RO 69 / AI 248 / IV 12 = 532 槽位；cs.AI 补采 skip=500 合并 69 条 → 248/248）。未入馆 **421 篇与 11-13 运行集合逐篇一致（diff 0）**，摘要级 13 篇命中与上批已剔 13 篇 id 逐篇一致（双向差集 0）→ **0 漏网**。
- **新公告组**：11-13 组 **601 篇唯一论文**（695 槽位）全部未入馆 → 摘要级 XR 过滤（`scripts/filter_missed_1114.py`，50 id/批 + 12s 间隔 + 覆盖率校验，二次补采 0 篇）命中 **43 篇**，meta **601/601**（覆盖率 1.0000）。
- **补充标题扫描（召回补层）**：对 601 篇标题做扩展词扫描（headset/gaze/display/immersive/panorama/view synthesis/3D reconstruction/pose estimation/splat 等），20 个标题命中 → 8 篇取 API 摘要复核 → **5 篇入池**（2611.16793 EG360 / 2611.17331 TTB / 2611.16594 VR 语言学习 / 2611.15143 V-JEPA 3R / 2611.15526 SCR-Mamba），3 篇剔除（ReFineR 相机-LiDAR 配准 / 逆体渲染散射算子 / 遥操作意图解码）。
- **数据源**：API id_list 可用（50 id/批，无 429）；RSS 7 分类去重 **979** → KW 命中 **67**（WROTE=67）。两渠道互证（关键词层）：**listing 43 = RSS 真新 43，双向差集 0**。
- **提交日核验**（API published）：主批 **11-11×11 / 11-12×9**——印证 11-13 组同时承载周三与周四两日提交（11-12 公告批次跳空的后果）。**RSS published 字段为公告时间戳（11-13），不可当提交日**。

## 甄别（第 3 步）
- 主批 XR 核心/强相关 **20 篇**入评分池（关键词层 15 篇 + 标题级补扫 5 篇）；关键词层 43 篇中 **28 篇非 XR 剔除**：类星体变率 / 世界模型预测评分 / 四足全身控制 / 手术三臂平台 / 个性化分割 / 无人机扩散规划 / 自行车越野竞速 / 边缘检测硬件协同 / 弹性体力-形变 / 抓取空间-语言-动作 / 妆容与动漫人像 FR / VLM 自演化技能 / Blender 4D 场景生成基准 / VLA 遮挡感知 / 外部相机机器人导航 / Exo2Ego 视频生成 / 物理接地视频描述基准 / 全身移动操作采集 / 事件边界感知 / 视觉语音表征 / 跨具身操作 / 单 X 光骨重建 / 物理 AI 环境平台 / 具身潜动作 / UAV 语言飞行基准 / 伊斯兰法理 FSA / 第一视角意图 HRI / 混合电视服务调研。
- 旧稿 v2/v3 未入馆 **17 篇**：**8 篇 XR → backfill-1114**；9 篇非 XR 剔除（见 backfill 日志）。
- 库内 v2 再公告 **7 篇**剔除（GraftRay / GS 特征场 2D-3D 对应 / InstantHMR / FlashMotion / RF3DGS / Reading the Room / DPGS-SLAM）。

## 全文抓取（第 4 步）
- 28 篇候选跑 `scripts/fetch_fulltext.py`，严格串行 3s/篇（约 72 秒）：**28 篇全部 L0/FULL**（43,212–171,293 字符）。
- 抽查正文中段确认非 ar5iv 摘要页误判（11-05 踩坑）；WROTE=28>0；manifest 合并写入校验通过；无 L5、无 OCR、无 PARTIAL。

## 评分与三关（第 5-6 步）
- 先抓全文再定稿。7 维加权定稿：主批 **6 A / 9 B / 5 C（无 S，最高 4.15 MatrixSplat）**；backfill **4 A / 4 B**（最高 4.50 riMESA，按口径记 A）。
- 门① 最大 Jaccard **0.082**（2512.10095 ReflFlow vs 库内 2609.23509 GARO；主批内最大 0.071，2611.16840 vs 2610.17513）。
- 门② **纯值 Top10 仅 4 赛道**（渲染与显示 1 / 重建与SLAM 6 / 神经渲染 2 / 交互与输入 1）→ **触发一次重筛**：剔除重复赛道最低分 **SteinPnP 3.50**，回补未覆盖赛道最高分 **MRxD 3.17（空间计算与UI）** → 定稿 Top10 覆盖 **5 赛道**（重建与SLAM 5 / 神经渲染 2 / 渲染与显示 1 / 交互与输入 1 / 空间计算与UI 1）。SteinPnP 仍入馆写 B 级笔记，仅不占 Top10 名额（同 10-29 SOMA / 11-04 Virtual Box 先例）。
- 门③ 当日最高 **4.15 < 库内近 30 天 Top10 均分 4.4100**（窗口 2026-10-15~11-14、**428 条入窗**、现算）→ **非重磅日，无 S 级**（本批亦无 ≥4.2 达线论文，校准关未触发降级改写）。
- OUTDATED/SUPERSEDED **0 篇**。

## 产物（第 7-8 步）
- 报告 2 份（主批 + backfill）+ 原子笔记 23 篇（grade≥B：主批 15 + backfill 8；5 篇 C 级仅入馆）+ MOC 2 份 + 总索引刷新 + 7 维表/scored/run_log 各 2 套。
- registry 907 → **935**（+20 +8；备份 `papers/library/registry.jsonl.bak-20261114`；按 base_id 幂等）。
- notes 564 → **587**。
- 门③ 现算值供下一批参考：**4.4100**（窗口将逐日滚动，须再算）。

## 观察（供后续批次）
- **系统层加速成为 3DGS 新竞争面**：MatrixSplat（矩阵核复用 / warp 级 MMA）与 TTB（把 cross-view attention 烘焙进轻量 MLP）同日出现，分别攻「特征累积吞吐」与「视角合成解码成本」两端。
- **退化模态与拓扑变化是 4D 重建主线**：ThermalSplat（热红外 + 无位姿稀疏视角）、ReCan-GS（干扰物分离）、TopoEgo/Topo-4DGS（切割/装配/开合的事件门控）三家共同把「非理想输入」当一等公民。
- **3D 基础模型的生产化叙事 vs 可复现缺口**：Kosmo-GFM 以 20 数据集预训练 + PoseEngine 给出 AbsRel 0.063 / 训练 14.07 h，但代码权重全未公开；对照 IncR-3DSGG 已发布 checkpoint 却仅 1 fps——「能用」与「可验」仍分离。
- **XR 追踪的参考系议题**：HeadIO 指出「重力对齐世界系」在头戴设备上非 yaw 等变，与 backfill 的 AVI-HT（视觉-IMU 手套追踪）同向，说明输入侧鲁棒性正从算法替换转向坐标系/融合策略设计。
- **XR-HCI 本批偏弱**：VR 防碰撞（MUM'26，可见率 37.0% vs 12.6%）与 MR 跨设备框架（238 篇系统综述）提供设计知识，但两篇 VR 严肃游戏仅为概念/研究议程（1.60 / 1.40 C）；硬件显示方向（波导/可变焦/Maxwellian/光场）**仍无破冰**。
'''
open(f'papers/daily/{DATE}/run_log.md', 'w', encoding='utf-8').write(run_log_main)

run_log_bf = f'''# backfill-1114 执行日志

- **来源**：11-13 公告批次 RSS（7 分类去重 979 → KW 命中 67）中 17 篇 v2/v3 再公告未入馆者，经摘要核实 XR 相关 **8 篇** → 本批；另 9 篇非 XR 剔除。
- **诚实口径**：全部为 **v2/v3 再公告**（API `updated` = 2026-11-11×7 / 2026-11-12×1），原始投稿 **2025-08-22 / 2025-10-04 / 2025-12-10 / 2026-03-01 / 2026-03-10 / 2026-05-20 / 2026-07-06 / 2026-07-15**；均非 11-13 当日新提交，单独编号、不参与当日重磅日判定。
- **全文**：8 篇全部 **L0/FULL**（47,054 / 49,xxx / 63,xxx / 68,023 / 69,115 / 73,149 / 73,573 / 82,283 / 149,662 字符区间内）。
- **定稿**：4 A / 4 B。最高 **2603.01178 riMESA 4.50**（协同 SLAM 后端：28 个真实数据集平均最优性差距 45.09%，比 DLGBP 352.81% 低 7.8×、比 DDF-SAM2 787.30% 低 17.5×；2,430 个合成集 + 实时 + 开源）· 2607.14203 Instant NuRec 4.28（10–20 s 多相机日志 ~1.5 s 出分层 3DGS，Waymo PSNR 28.26 / +2.01 dB，动态区 24.93 vs 21.76）· 2510.03857 OMG4 3.80（2087 MB→3.59 MB、57→129 FPS）· 2605.21714 AVI-HT 3.73（手套式 3D 手部追踪视觉-IMU 融合）· 2603.09741 ENIGMA-360 3.49 · 2607.05243 GUSH3R 3.42 · 2508.16731 COSMO-Bench 3.34 · 2512.10095 ReflFlow 3.00。
- **剔除**：9 篇非 XR（MedGS 医学多模态 / BLaFA 抓取功能可供性 / 空间句法户型生成 / 概率虚拟夹具 / 液体防溢应急停止 / 黎曼流形直接信息采样 / VLA 检索式推测解码 / LLM 连续扩散 / SWAM 世界动作模型）。
- **registry**：+8（batch=backfill-1114，幂等）。
'''
open('papers/daily/backfill-1114/run_log.md', 'w', encoding='utf-8').write(run_log_bf)

# ---------- registry ----------
reg_path = 'papers/library/registry.jsonl'
bak_path = reg_path + '.bak-20261114'
if not os.path.exists(bak_path):
    shutil.copy(reg_path, bak_path)
rows = [json.loads(l) for l in open(reg_path, encoding='utf-8') if l.strip()]
have = {r['id'].split(':')[-1].split('v')[0] for r in rows}
added = 0
with open(reg_path, 'a', encoding='utf-8') as f:
    for p in MAIN + BF:
        if p['id'] in have:
            continue
        entry = dict(id=f"arXiv:{p['id']}", title=p['title'], title_zh=p['title_zh'],
                     track=p['track'], date=DATE, value=p['value'], grade=p['grade'],
                     scores=p['scores'], status=p['status'], evidence=p['evidence'],
                     fetch_level=p['level'], fulltext_chars=MANIFEST[p['id']]['chars'],
                     in_top10=(p['id'] in TOP10_IDS), batch=p['batch'],
                     announce_type=p['announce'], flags=[])
        f.write(json.dumps(entry, ensure_ascii=False) + '\n')
        added += 1
print(f'registry +{added}（现有 {len(rows) + added}）')

# ---------- notes ----------
def slugify(t):
    s = re.sub(r'[^a-z0-9]+', '-', t.lower()).strip('-')
    return s[:48]


NOTE_TMPL = '''---
id: arXiv:{id}
title: {title}
title_zh: {title_zh}
track: {track}
venue: {venue}
date: {date}
value: {value}
grade: {grade}
evidence: {evidence}
status: {status}
superseded_by: []
scores: {{IMP:{IMP}, NOV:{NOV}, TEC:{TEC}, EXP:{EXP}, PER:{PER}, TRL:{TRL}, REP:{REP}}}
fetch_level: {level}
batch: {batch}
announce_type: {announce}
in_top10: {in_top10}
tags: [{tags}]
---

# {title_zh}

## 一句话结论
{conclusion}

## 要解决的问题
{problem}

## 方法详解
{method}

## 实验与结果
{experiments}

## 创新点与贡献
{innovation}

## 局限与风险
{limits}

## 与文献库的关系
{relation}

## 可复现性（代码/数据/硬件）
{repro}

## 行动建议
{action}
'''
os.makedirs('papers/notes', exist_ok=True)
n_notes = 0
for p in MAIN + BF:
    if p['grade'] == 'C':
        continue
    fn = f"papers/notes/{p['id']}__{slugify(p['slug'])}.md"
    if os.path.exists(fn):
        print('skip existing', fn)
        continue
    body = NOTE_TMPL.format(
        id=p['id'], title=p['title'], title_zh=p['title_zh'], track=p['track'], venue=p['venue'],
        date=DATE, value=f"{p['value']:.2f}", grade=p['grade'], evidence=p['evidence'],
        status=p['status'], IMP=p['scores']['IMP'], NOV=p['scores']['NOV'], TEC=p['scores']['TEC'],
        EXP=p['scores']['EXP'], PER=p['scores']['PER'], TRL=p['scores']['TRL'], REP=p['scores']['REP'],
        level=p['level'], batch=p['batch'], announce=p['announce'],
        in_top10=('true' if p['id'] in TOP10_IDS else 'false'),
        tags=', '.join(p['tags']), conclusion=p['conclusion'], problem=p['problem'],
        method=p['method'], experiments='\n'.join(f'- {x}' for x in p['experiments']),
        innovation='\n'.join(f'- {x}' for x in p['innovation']),
        limits='\n'.join(f'- {x}' for x in p['limits']),
        relation=p['relation'], repro=p['repro'], action=p['action'])
    open(fn, 'w', encoding='utf-8').write(body)
    n_notes += 1
print('notes written:', n_notes)


# ---------- MOC ----------
def moc(papers, path, title, intro):
    L = [f'# {title}\n', intro + '\n', '## 本批论文（按加权降序）\n',
         '| # | 论文 | 赛道 | 总分 | 等级 | 证据 | 笔记 |', '|---|---|---|---|---|---|---|']
    for i, p in enumerate(papers, 1):
        note = glob.glob(f"papers/notes/{p['id']}__*")
        link = f"[→](../notes/{os.path.basename(note[0])})" if note else '→（C 级仅入馆）'
        L.append(f"| {i} | {esc(p['title_zh'])} | {p['track']} | {p['value']:.2f} | {p['grade']} | {p['evidence']} | {link} |")
    L += ['\n## 批次要点\n']
    for p in papers:
        L.append(f"- **{esc(p['title_zh'])}**（{p['id']}，{p['value']:.2f} {p['grade']}）：{p['conclusion']}")
    open(path, 'w', encoding='utf-8').writelines([x + '\n' for x in L])


moc(MAIN, f'papers/MOC/MOC-{DATE}.md', f'MOC · {DATE}（11-13 公告批次 · 11-12 跳空后延迟释放）',
    '> 当日地图：**公告日 2026-11-13（周五）≠ 拉取日 2026-11-14（周六 02:30）**——诚实口径。**11-12（周四）公告批次跳空**（工作日跳空第 2 次），'
    '11-11 与 11-12 两日提交并入 11-13 组释放；API published 核验提交日 **11-11×11 / 11-12×9**（RSS published 为公告时间戳）。\n'
    '> 主批 XR 新稿 **20 篇（6 A / 9 B / 5 C，无 S）**，Top10 实数 10 篇最高 **4.15**（MatrixSplat）；'
    'listing 11-13 组 601 篇摘要级命中 43 篇 = RSS 真新 43 篇（关键词层双向差集 0）+ 标题级补扫 5 篇；11-11 组复采 421 篇未入馆与上批逐篇一致 → 0 漏网。\n'
    '> 全文：**28 篇全部 L0/FULL**（43,212–171,293 字符）。\n'
    '> 覆盖度三关：门① 0.082 / 门② 纯值仅 4 赛道 → 剔 SteinPnP 3.50 回补 MRxD 3.17 → 定稿 **5 赛道** / 门③ **4.15 < 4.4100**（现算，428 条入窗）→ **非重磅日，无 S**。\n'
    '> Top10（实数 10 篇）：MatrixSplat 4.15 · Topo-4DGS 4.07 · Kosmo-GFM 3.93 · ReCan-GS 3.85 · TTB 3.85 · HeadIO 3.63 · ThermalSplat 3.58 · IncR-3DSGG 3.57 · VR 粒子防碰撞 3.55 · MRxD 3.17（门②回补）。')

moc(BF, 'papers/MOC/MOC-backfill-1114.md', 'MOC · backfill-1114（旧稿 v2/v3 再公告首次入馆）',
    '> **非当日新提交**：本批 8 篇均为 11-13 公告 RSS 混入的旧稿 v2/v3 再公告（原始投稿 2025-08 ~ 2026-07，2026-11-11/11-12 更新），诚实口径单独编号，不参与当日重磅日判定。\n'
    '> 定稿 4 A / 4 B，最高 **2603.01178 riMESA 4.50**（协同 SLAM 共识 ADMM：真实集平均最优性差距 45.09% vs DLGBP 352.81% / DDF-SAM2 787.30%；按口径记 A）。'
    '其余：Instant NuRec 4.28（驾驶场景前馈 3DGS，~1.5 s/10–20 s 日志）· OMG4 3.80（4DGS 极致压缩 2087 MB→3.59 MB）· AVI-HT 3.73（视觉-IMU 手套追踪）· ENIGMA-360 3.49 · GUSH3R 3.42 · COSMO-Bench 3.34 · ReflFlow 3.00。')


# ---------- report ----------
def report(papers, path, title, header, topn, gate_lines):
    L = [f'# {title}\n', header + '\n', '## 二、排行榜（按加权降序）\n',
         '| 排名 | 论文 | 赛道 | 总分 | 等级 | 证据 | 落后标记 |', '|---|---|---|---|---|---|---|']
    for i, p in enumerate(papers[:topn], 1):
        mark = '⛔ OUTDATED' if p['status'] != 'CURRENT' else '—'
        L.append(f"| {i} | {esc(p['title_zh'])}（{p['id']}） | {p['track']} | {p['value']:.2f} | {p['grade']} | {p['evidence']} | {mark} |")
    L.append('\n## 三、逐篇深度解读\n')
    for i, p in enumerate(papers[:topn], 1):
        L.append(f"### 第 {i} 章 · {esc(p['title_zh'])}（{p['id']}，{p['value']:.2f} {p['grade']}，{p['evidence']}）\n")
        L.append(f"- **赛道 / 场合**：{p['track']} / {p['venue']}")
        L.append(f"- **公告类型**：{p['announce']}（公告日 2026-11-13，拉取日 2026-11-14）")
        if p.get('grade_note'):
            L.append(f"- **等级说明**：{p['grade_note']}")
        L.append(f"- **一句话结论**：{p['conclusion']}")
        L.append(f"- **要解决的问题**：{p['problem']}")
        L.append(f"- **方法详解**：{p['method']}")
        L.append('- **实验与结果**：')
        for x in p['experiments']:
            L.append(f"    - {x}")
        L.append('- **创新点与贡献**：')
        for x in p['innovation']:
            L.append(f"    - {x}")
        L.append('- **局限与风险**：')
        for x in p['limits']:
            L.append(f"    - {x}")
        L.append(f"- **与文献库的关系**：{p['relation']}")
        L.append(f"- **可复现性**：{p['repro']}")
        L.append(f"- **行动建议**：{p['action']}\n")
    L.append('## 四、当日全量 7 维度对比表（参考）\n')
    L.append(f'见 [`papers/daily/{DATE}/7dim-table.md`](../papers/daily/{DATE}/7dim-table.md)。\n')
    L.append('## 五、覆盖率校验与筛选过程说明\n')
    L += gate_lines
    L.append('\n## 六、附录：证据等级分布与抓取记录\n')
    nf = sum(1 for p in papers if p['evidence'] == 'FULL')
    np_ = sum(1 for p in papers if p['evidence'] == 'PARTIAL')
    L.append(f'- 本表 {len(papers)} 篇：FULL {nf} 篇；PARTIAL {np_} 篇；ABSTRACT_ONLY 0 篇。')
    L.append('- 抓取降级：28 篇候选串行 3s/篇，全部 L0 一次命中（43,212–171,293 字符）；无 406/429 重试、无 L1–L5 降级、无 OCR。无限流、无伪造。')
    open(path, 'w', encoding='utf-8').writelines([x + '\n' for x in L])


HEADER = (
    '## 一、执行摘要\n'
    '- **公告日 2026-11-13（周五）≠ 拉取日 2026-11-14（周六 02:30）**——诚实口径。'
    '**11-12（周四）公告批次跳空**（工作日跳空第 2 次，继 10-29），11-11（周三）与 11-12（周四）两日提交并入 11-13 组释放；'
    'API published 核验主批提交日 **11-11×11 / 11-12×9**（RSS published 是公告时间戳非提交日）。\n'
    '- **数据源**：API id_list 可用（50 id/批 × 12s，meta 601/601 覆盖，无 429）；RSS 7 分类去重 **979** → KW 命中 **67**。'
    '两渠道互证（关键词层）：**listing 摘要级 43 篇 = RSS 真新 43 篇，双向差集 0**；另经标题级补扫补入 KW 未命中 5 篇（EG360 / TTB / VR 语言学习 / V-JEPA 3R / SCR-Mamba）；'
    '11-11 组复采 532 槽位 / 436 唯一，未入馆 421 篇与上批集合 **diff 0**、摘要级 13 篇命中与上批已剔逐篇一致 → **0 漏网**。\n'
    '- **主批 XR 新稿 20 篇（6 A / 9 B / 5 C，无 S；Top10 实数 10 篇）**。Top10：'
    '**MatrixSplat 4.15 A（把 3DGS 的深度排序 alpha 合成改写为 warp 级打包 MMA + FP16/FP32 混合：Mip-NeRF 360 599.9 FPS（3DGS 156.0 / TC-GS 295.1）、LERF 702.6 FPS、3D-OVS 510.9 FPS，端到端最高 3.8×、D=256 核时间 36.7×，可替换四种渲染器混合核）** · '
    'Topo-4DGS 4.07（首个拓扑变化第一人称 4DGS 基准 TopoEgo：24 段 / 4,618 帧 / 34 事件，事件后 PSNR 24.30 vs 基线 19.83、+4.47 dB） · '
    'Kosmo-GFM 3.93（几何基础模型 + PoseEngine：SpatialBench Sparse AbsRel 0.063 vs VGGT-Ω 0.077、AUC@5 0.741 vs 0.695，34 场景重建 14.07 h vs COLMAP 47.08 h） · '
    'ReCan-GS 3.85（雅可比形变敏感度分离核心/瞬态高斯，干扰物场景 +1.26 dB） · '
    'TTB 3.85（把 cross-view attention 烘焙进轻量 MLP：960p/64 视角 30.20 dB、23 FPS vs DVSM 31.11 dB/1 FPS，local-duplicate 后 31.33 dB 追平） · '
    'HeadIO 3.63（体坐标系航向分解神经惯性里程计：RTE-5s 0.239 vs EqNIO 0.260，参数 0.97M；但 AEA 上 ATE 反落后） · '
    'ThermalSplat 3.58（无位姿稀疏视角热红外 3DGS，聚合 5 个热红外数据集） · '
    'IncR-3DSGG 3.57（无深度输入的增量 3D 场景图，物体 R@1 39.5 vs MonoSSG 28.6） · '
    'VR 粒子防碰撞 3.55（MUM 26：粒子雾替代网格边界，253 个 approach episode 可见率 37.0% vs 12.6%，p=.001） · '
    'MRxD 3.17（238 篇 MR 跨设备文献 → 三维修订框架 + 六种使用模式；门②回补）。\n'
    '- **覆盖 8 赛道（全批）/ Top10 覆盖 5 赛道**：重建与SLAM 8（Top10 占 5）/ 交互与输入 4（占 1）/ 神经渲染 2（占 2）/ 感知与认知 2 / 渲染与显示 1（占 1）/ 空间计算与UI 1（占 1）/ 评估与数据集 1 / 化身与人体 1。\n'
    '- **覆盖度三关**：门① 最大 Jaccard **0.082**（2512.10095 vs 库内 2609.23509；主批内 0.071）；'
    '门② 纯值 Top10 **仅 4 赛道 → 重筛一次**（剔 SteinPnP 3.50，回补 MRxD 3.17）→ **5 赛道**；'
    '门③ 当日最高 **4.15 < 库内近 30 天 Top10 均分 4.4100**（现算，428 条入窗）→ **非重磅日，无 S 级**。\n'
    '- **全文证据**：28 篇候选 **全部 L0/FULL**（43,212–171,293 字符），无 PARTIAL / L5 / OCR。OUTDATED 0。\n'
    '- **backfill-1114（8 篇，非当日新提交）**：11-13 公告 RSS 混入的旧稿 v2/v3 再公告首次入馆——'
    'riMESA 4.50（协同 SLAM 共识 ADMM：真实集最优性差距 45.09% vs DLGBP 352.81% / DDF-SAM2 787.30%，2,430 合成集 + 28 真实集 + 开源；**按口径记 A**） · '
    'Instant NuRec 4.28（10–20 s 多相机日志 ~1.5 s 出分层 3DGS，Waymo PSNR 28.26 / +2.01 dB） · '
    'OMG4 3.80（2087 MB→3.59 MB、57→129 FPS） · AVI-HT 3.73（视觉-IMU 手套追踪） · ENIGMA-360 3.49 · GUSH3R 3.42 · COSMO-Bench 3.34 · ReflFlow 3.00。\n'
    '- **路线观察**：① **3DGS 的系统层加速成为新竞争面**——MatrixSplat 攻「特征累积吞吐」（矩阵核 / warp MMA），TTB 攻「视角合成解码成本」（烘焙式轻量 MLP），'
    '两者共同把 3DGS 的性能边界从「训练/重建」推向「每帧执行效率」；② **退化模态与拓扑变化被当作一等公民**——ThermalSplat（热红外 / 无位姿 / 稀疏视角）、'
    'ReCan-GS（干扰物分离）、TopoEgo（切割/装配/开合事件）三家同周出现，说明 4D 重建的评测范式正从「干净场景」转向「真实失败模式」；'
    '③ **3D 基础模型的「生产化叙事」与「可验性」仍在分离**——Kosmo-GFM 给出 20 数据集预训练与 14.07 h 训练成本，却完全未公开代码权重；'
    'IncR-3DSGG 已放 checkpoint 但 1 fps，两端都还不足以支撑 XR 端侧；④ **XR 追踪议题下沉到参考系与融合策略**——HeadIO 指出「重力对齐世界系」在头戴设备上非 yaw 等变、'
    'backfill 的 AVI-HT 把视觉与 IMU 在手套场景重新配比，二者都指向「输入表征」而非「网络结构」；⑤ **XR-HCI 本批偏弱**：两篇 VR 严肃游戏仅为概念/议程（1.60 / 1.40 C），'
    '硬件类显示方向（波导 / 可变焦 / Maxwellian / 光场）**仍无破冰**。'
)

report(TOP10, f'reports/XR-Daily-Report-{DATE}.md', f'XR 每日论文解读报告 · {DATE}（11-13 公告批次 · 11-12 跳空后延迟释放）', HEADER, 10,
       ['- 门①（同质去重）：最大 Jaccard **0.082** < 0.62（2512.10095 ReflFlow vs 库内 2609.23509 GARO），通过；主批内最大 0.071（2611.16840 vs 2610.17513）。库侧 token 取 title+title_zh（registry 无摘要字段），口径偏保守。',
        '- 门②（赛道覆盖）：纯值 Top10 **仅 4 赛道**（重建与SLAM×6 / 神经渲染×2 / 渲染与显示×1 / 交互与输入×1）→ **触发一次重筛**：剔除重复赛道最低分 **SteinPnP 3.50**（重建与SLAM 第 6 篇），回补未覆盖赛道最高分 **MRxD 3.17**（空间计算与UI，XR 核心赛道）→ 定稿 **5 赛道**。SteinPnP 仍入馆并写 B 级笔记，仅不占 Top10 名额（同 10-29 SOMA / 11-04 Virtual Box 先例）。',
        '- 门③（价值天花板）：当日最高 **4.15** < 库内近 30 天 Top10 均分 **4.4100**（现算，窗口 2026-10-15~11-14、428 条入窗；Top10 = 视频扩散化身 4.57 · Open-HumanScale 4.57 · Map2SLAM 4.57 · ACD-GS 4.37 · 立体匹配 CI 4.37 · XM4D 4.36 · RacerGS 4.35 · HaNDF 4.34 · dGS/dBS 4.30 · CognitiveReality 4.30）→ **非重磅日，无 S 级**。本批亦无 ≥4.2 达线论文，校准关未触发降级改写。',
        '- 主会话校准记录：① MatrixSplat TRL 4→3（正文仅「will release」、无仓库）；② TTB TRL 4→3（仅项目页有结果可视化）；③ EG360 赛道 系统与平台→重建与SLAM；④ 其余沿用子代理评分并逐条核对正文数字（MatrixSplat 三数据集 FPS、riMESA 45.09%/352.81%/787.30%、Instant NuRec 28.26/+2.01 dB、TopoEgo +4.47 dB）。',
        '- 召回补层记录（诚实披露）：关键词层两渠道完全一致（43 = 43），但 KW 过滤存在召回缺口——对 601 篇标题做扩展词扫描后补入 5 篇未命中关键词者（EG360 / TTB / VR 语言学习 / V-JEPA 3R / SCR-Mamba），其中 3 篇进入 Top10 候选序列（TTB 3.85、EG360 3.45、SCR-Mamba 3.08）。该层不计入「RSS 漏网」统计。',
        '- 低量日不凑数原则复核：主批 20 篇中 5 篇 C 级（<3.0）仅入馆不解读；Top10 取实数 10 篇（含 4 篇 B 级），未为凑满 10 篇放宽 B 级下限，亦未把 B 级拔高为 A。',
        '- OUTDATED/SUPERSEDED **0 篇**（本批无被库内更晚工作取代者；硬件类显示方向仍无新增）。\n'])

report(BF, 'reports/XR-Backfill-Report-backfill-1114.md', 'XR Backfill 报告 · backfill-1114（旧稿 v2/v3 再公告首次入馆）',
       '## 一、执行摘要\n'
       '- **诚实口径**：本批 8 篇均为 **11-13 公告批次 RSS 混入的旧稿 v2/v3 再公告**（原始投稿 2025-08-22 / 2025-10-04 / 2025-12-10 / 2026-03-01 / 2026-03-10 / 2026-05-20 / 2026-07-06 / 2026-07-15；'
       'API `updated` = 2026-11-11×7 / 2026-11-12×1），首次入馆；**均非 11-13 当日新提交**，单独编号、不参与当日重磅日判定。\n'
       '- **定稿 4 A / 4 B**，最高 **2603.01178 riMESA 4.50**（协同 SLAM 后端：28 个真实数据集平均最优性差距 **45.09%**，比 DLGBP 352.81% 低约 7.8×、比 DDF-SAM2 787.30% 低约 17.5×；'
       '2,430 个合成数据集 + 实时 + 开源；**达 S 线但按口径一律记 A**）。其余：Instant NuRec 4.28（~1.5 s 重建 10–20 s 多相机日志，Waymo PSNR 28.26 / 动态区 24.93 vs 21.76） · '
       'OMG4 3.80（2087 MB→3.59 MB、57→129 FPS） · AVI-HT 3.73（手套式 3D 手部追踪视觉-IMU 融合，证据链最完整） · ENIGMA-360 3.49（全量开放的 ego-exo 工业数据集） · '
       'GUSH3R 3.42（单目前馈人体-场景高斯） · COSMO-Bench 3.34（协同 SLAM 优化基准，但无后端基线） · ReflFlow 3.00（动态高光光线追踪，HyperNeRF 上仍落后 4DGS）。\n'
       '- **全文**：8 篇全部 L0/FULL（47,054–149,662 字符）。\n'
       '- **剔除**：同批 v2/v3 未入馆 17 篇中 9 篇经摘要核实非 XR（MedGS 医学 / BLaFA 抓取 / 空间句法户型 / 虚拟夹具 / 液体防溢 / 黎曼采样规划 / VLA 推理解码 / LLM 连续扩散 / SWAM 世界动作模型）。',
       8,
       ['- 门①/门③ 对 backfill 不适用（非当日新提交，不参与重磅日判定）；门② 覆盖 6 赛道（重建与SLAM×2 / 世界模型与仿真×1 / 神经渲染×1 / 交互与输入×1 / 评估与数据集×2 / 渲染与显示×1）。',
        '- **口径说明（重要）**：本批最高 4.50 若计入主批将越过门③ 的 4.4100 线，但按既定口径 backfill 不参与重磅日判定、≥4.2 一律记 A，故本报告不宣称 S 级。\n'])

# ---------- MOC-总索引 ----------
moc_path = 'papers/MOC/MOC-总索引.md'
h = open(moc_path, encoding='utf-8').read()
n0 = len(h)


def rep(old, new, tag):
    global h
    assert old in h, f'ANCHOR NOT FOUND: {tag}'
    h = h.replace(old, new, 1)


rep('累计 **907 篇**；跨度 2026-09-15 ~ 2026-11-11',
    '累计 **935 篇**；跨度 2026-09-15 ~ 2026-11-14', 'head-count')
rep('**backfill-1112:4（11-11 公告 RSS 混入旧稿 v2/v3 再公告，首次入馆）**；',
    '**backfill-1112:4（11-11 公告 RSS 混入旧稿 v2/v3 再公告，首次入馆）** · '
    '**2026-11-14:20（11-13 公告批次真新提交——11-12 公告跳空后延迟释放，合并 11-11/11-12 两日提交，非重磅日无S）** · '
    '**backfill-1114:8（11-13 公告 RSS 混入旧稿 v2/v3 再公告，首次入馆）**；', 'batch-list')

note14 = ('> **状态注记（2026-11-14）**：周六 02:30，处理 **2026-11-13（周五）公告批次**（公告日≠拉取日，诚实口径）。'
 '**11-12（周四）公告批次跳空确认**（工作日跳空第 2 次，继 10-29）：listing 7 分类最新公告日 11-13、**无 11-12 日组**，'
 '11-11 与 11-12 两日提交并入 11-13 组释放；API published 核验主批 **11-11×11 / 11-12×9**（RSS published 为公告时间戳）。'
 '漏网对账（`scripts/audit_listing_1114.py`，PREV_DAY=11-11 / NEW_DAYS=11-12,11-13）：11-11 组复采逐分类 **declared=got**（532 槽位 / 436 唯一；cs.AI 补采合并 69 条），'
 '未入馆 **421 篇与 11-13 运行集合逐篇一致（diff 0）**、摘要级 13 篇命中与上批已剔逐篇一致 → **0 漏网**；'
 '**11-13 组 601 篇唯一论文**（695 槽位）摘要级过滤 meta 601/601（覆盖率 1.0000）命中 **43 篇**。'
 '**数据源**：API id_list 可用（50 id/批，无 429）；RSS 去重 **979** → KW 命中 **67** = 43 真新 + 17 旧稿未入馆（8 XR → backfill-1114）+ 7 库内 v2；'
 '**关键词层双向差集 0**，另标题级补扫补入 KW 未命中 5 篇（EG360 / TTB / VR 语言学习 / V-JEPA 3R / SCR-Mamba）。'
 '主批甄别 **XR 20 篇**（关键词层 28 篇非 XR 剔除）；全文 **28 篇全部 L0/FULL**（43,212–171,293 字符，无 PARTIAL/L5）。'
 'Top10（**实数 10 篇**）：最高 **4.15 MatrixSplat（A）**，**非重磅日无 S**；覆盖 **5 赛道**（重建与SLAM×5 / 神经渲染×2 / 渲染与显示·交互与输入·空间计算与UI 各×1）。'
 '三关：门① max Jaccard **0.082**（2512.10095 vs 库内 2609.23509）；门② 纯值仅 4 赛道 → 剔 SteinPnP 3.50 回补 MRxD 3.17 → 5 赛道；'
 '门③ 当日最高 **4.15 < 4.4100**（428 条入窗，现算）→ **非重磅日，无 S**；OUTDATED 0。'
 'registry 907 → **935**（+20 +8），笔记 564 → **587**。'
 '详见 [运行报告](../../reports/XR-Daily-Report-2026-11-14.md) / [MOC-2026-11-14](./MOC-2026-11-14.md) / [MOC-backfill-1114](./MOC-backfill-1114.md) / [Backfill 报告](../../reports/XR-Backfill-Report-backfill-1114.md)。\n')
anchor_end = '详见 [状态报告](../../reports/XR-Daily-Report-2026-11-13.md)。'
i = h.find(anchor_end)
assert i >= 0, 'ANCHOR NOT FOUND: note1113-end'
j = h.find('\n', i) + 1
h = h[:j] + note14 + h[j:]

rep('| 最新一期 | [MOC · 2026-11-12](./MOC-2026-11-12.md) |',
    '| 最新一期 | [MOC · 2026-11-14](./MOC-2026-11-14.md) |', 'quick-latest')
rep('| 上一期 | [MOC · 2026-11-11](./MOC-2026-11-11.md) |',
    '| 上一期 | [MOC · 2026-11-12](./MOC-2026-11-12.md) |', 'quick-prev')
rep('（现有 564 篇）', '（现有 587 篇）', 'quick-notes')

old_status_start = '| 最新运行状态 | [运行报告 2026-11-13]'
k = h.find(old_status_start)
assert k >= 0, 'ANCHOR NOT FOUND: quick-status'
k_end = h.find('\n', k)
new_status = ('| 最新运行状态 | [运行报告 2026-11-14](../../reports/XR-Daily-Report-2026-11-14.md)'
              '（11-13 公告批次 20 篇 6A/9B/5C **非重磅日无S**；11-12 公告跳空后延迟释放、合并 11-11/11-12 两日提交；'
              'listing 601 篇摘要级命中 43 篇 = RSS 真新 43 篇关键词层双向差集 0 + 标题级补扫 5 篇；11-11 组复采 0 漏网；'
              '全文 28×L0/FULL；Top10 实数 10 篇覆盖 5 赛道（门② 重筛一次：剔 SteinPnP 回补 MRxD）；'
              '门③ 现算 4.4100，当日最高 4.15 未达线 → 无 S）；上一期为 [11-13 状态报告](../../reports/XR-Daily-Report-2026-11-13.md) |')
h = h[:k] + new_status + h[k_end:]

row_main = ('| 2026-11-14 | [MOC-2026-11-14](./MOC-2026-11-14.md) | XR 20（Top10 实数 10）· 6A/9B/5C · **非重磅日（无S）** | '
            '11-13 公告批次真新提交 20 篇（11-11×11/11-12×9，11-12 公告跳空后延迟释放）；listing 601 篇摘要级命中 43 篇 = RSS 真新 43 篇（关键词层双向差集 0）+ 标题级补扫 5 篇；'
            '11-11 组复采 0 漏网；全文 28×L0/FULL |\n'
            '| backfill-1114 | [MOC-backfill-1114](./MOC-backfill-1114.md) | 补录 8（4A/4B）· 非当日新提交 | '
            '11-13 公告 RSS 混入旧稿 v2/v3 再公告 8 篇（2508/2510/2512/2603×2/2605/2607×2，2026-11-11~12 更新）；最高 2603.01178 riMESA 4.50（按口径记 A） |')
anchor_row = '| backfill-1112 | [MOC-backfill-1112](./MOC-backfill-1112.md) | 补录 4（2A/2B）· 非当日新提交 | 11-11 公告 RSS 混入旧稿 v2/v3 再公告 4 篇（2503/2505/2605/2608，2026-11-09~10 更新）；最高 2505.20858 4.15 |'
rep(anchor_row, anchor_row + '\n' + row_main, 'batch-table')

seg = '\n### 2026-11-14 新增（Top10 实数 10 篇：6 A + 4 B，非重磅日无 S）\n\n| # | 论文 | 赛道 | 分值 | 等级 | 证据 |\n|---:|---|---|---:|---|---|\n'
for i2, pid in enumerate(TOP10_ORDER, 1):
    p = next(x for x in MAIN if x['id'] == pid)
    seg += f"| {i2} | {esc(p['title_zh'])} | {p['track']} | {p['value']:.2f} | {p['grade']} | {p['evidence']} |\n"
seg += '\n### backfill-1114 补录（8 篇：4 A + 4 B，非当日新提交）\n\n| # | 论文 | 赛道 | 分值 | 等级 | 证据 |\n|---:|---|---|---:|---|---|\n'
for i2, p in enumerate(BF, 1):
    seg += f"| {i2} | {esc(p['title_zh'])} | {p['track']} | {p['value']:.2f} | {p['grade']} | {p['evidence']} |\n"
h = h.rstrip() + '\n' + seg

foot_pat = re.compile(r'^\*最后更新：[^\n]*\* · MOC \d+ 份$', re.M)
assert foot_pat.search(h), 'ANCHOR NOT FOUND: footer'
h = foot_pat.sub('*最后更新：2026-11-14（11-13 公告批次——**11-12 公告跳空后延迟释放**，合并 11-11/11-12 两日提交：20 篇 XR 新稿 6A/9B/5C **非重磅日无S**；'
                 'listing 601 篇摘要级命中 43 篇 = RSS 真新 43 篇（关键词层双向差集 0）+ 标题级补扫 5 篇；11-11 组复采 421 篇未入馆 diff 0、摘要级 13 篇与上批已剔逐篇一致 → 0 漏网；'
                 '全文 28×L0/FULL；门② 纯值仅 4 赛道 → 剔 SteinPnP 回补 MRxD → 5 赛道；门③ 现算 4.4100，当日最高 4.15 未达线 → 无 S；backfill-1114 补录 8 篇 4A/4B）。* '
                 '· 库内 **935 篇** · 原子笔记 **587 篇** · MOC 51 份', h)

open(moc_path, 'w', encoding='utf-8').write(h)
print('MOC-总索引 refreshed（%d -> %d chars）' % (n0, len(h)))
print('DONE')
