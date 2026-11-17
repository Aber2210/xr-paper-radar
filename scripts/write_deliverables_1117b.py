# -*- coding: utf-8 -*-
"""2026-11-17 产物生成（第二部分）：run_log / 原子笔记 / MOC / 报告 / registry / 总索引。"""
import glob
import json
import os
import re
import shutil
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from grade_caliber import assign_grade  # noqa: E402  档位口径单一实现

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
os.chdir(ROOT)
D = json.load(open('data/scored_1117.json', encoding='utf-8'))
MAIN = [p for p in D if p['batch'] == '2026-11-17']
BF = [p for p in D if p['batch'] == 'backfill-1117']
MAIN.sort(key=lambda r: (-r['value'], -r['scores']['IMP'], -r['scores']['NOV'], r['id']))
G = json.load(open('data/gates_1117.json', encoding='utf-8'))
TOP10_ORDER = G['top10']
DATE, ANN = '2026-11-17', '2026-11-16'
GATE3, G1 = G['gate3']['top10_mean'], G['gate1']['max_jaccard']
HEAVY = bool(G['gate3']['heavy_day'])
MANIFEST = json.load(open('data/fulltext/_manifest.json', encoding='utf-8'))
for p in MAIN + BF:
    p['level'] = MANIFEST[p['id']]['level']
    p['evidence'] = MANIFEST[p['id']]['evidence']
    p['announce'] = 'replace' if p['batch'].startswith('backfill') else 'new'
    p['status'] = 'CURRENT'
    p['grade'] = assign_grade(p['value'], p['batch'], HEAVY)
    p['in_top10'] = p['id'] in TOP10_ORDER
TOP10 = [next(p for p in MAIN if p['id'] == pid) for pid in TOP10_ORDER]


def esc(s):
    return str(s).replace('|', '/')


# ---------- run_log ----------
run_log_main = f'''# {DATE} 执行日志

## 数据源与对账（第 1-3 步）
- **漏网对账（先于拉取）**：`scripts/audit_listing_1117.py`（PREV_DAY=2026-11-13 / NEW_DAYS=2026-11-14,11-15,11-16,11-17；show=500 单页×7 分类，目标组 declared≠got 自动补采后续页）。7 分类最新公告日均为 **2026-11-16（周一）**，**无 11-14/11-15 日组**（周末 `skipDays` 节律）、无 11-17 日组（当日尚未释放）。
- **上批组复核**：11-13 组逐分类 **declared=got**（CV 196 / GR 6 / HC 43 / MM 2 / RO 106 / AI 321 / IV 21 = **695 槽位 / 601 唯一**），未入馆 **581 篇与 11-16 运行集合 581/581 逐篇一致** → **0 漏网**（摘要级 28 篇命中亦与 11-15/11-16 两次运行完全一致，均为 11-14 运行已显式剔除的非 XR 稿）。
- **新公告组**：11-16 组 **271 篇唯一论文**（320 槽位：CV 91 / GR 5 / HC 13 / MM 0 / RO 38 / AI 164 / IV 9），全部未入馆。
- **摘要级过滤**：`scripts/triage_1117.py`。listing 271 篇 **100% 被 RSS 全量覆盖（缺收 0 篇）**，摘要覆盖率 **271/271 = 1.0000**，故直接使用 RSS 全摘要而不走 API `id_list`（规避 11-12 的 429 静默丢批风险）。KW 命中 **11 篇**。
- **标题级扩展词补扫（第三层召回，诚实披露）**：对 271 篇标题扫扩展词补入 **22 篇** KW 未命中者；33 篇候选逐篇核摘要剔除 **20 篇误命中** → **XR 池 13 篇**。该层**不计入「RSS 漏网」统计**。
- **数据源**：API 双主机 200（仅用于提交日核验）；RSS 7 分类 `--no-filter` 去重 **435 条** = **189 new + 82 cross + 164 replace**。两渠道互证：listing 271 篇全部在 RSS 内（**RSS 缺收 0 篇**）——本批为「RSS 有源、listing 定全集」的典型日。
- **提交日核验**（API published，单批 16 id 一次查询，返回 16/16）：主批 **11-13×12 / 11-12×1**；backfill **2025-01-22 / 2026-08-19 / 2026-11-12**。**RSS published 字段为公告时间戳（11-16），不可当提交日**。

## 甄别（第 3 步）
- 主批 XR 入评分池 **13 篇**：KW 层 5 篇（2611.18438 / 2611.18256 / 2611.18170 / 2611.17957 / 2611.17752）+ 标题级补扫 8 篇（2611.18099 / 2611.17458 / 2611.18340 / 2611.17755 / 2611.18243 / 2611.17619 / 2611.17828 / 2611.17903）。
- **误命中剔除 20 篇**（逐篇核摘要）：医学 MRI 类 4 篇（2611.17983 脑肿瘤交互分割 / 2611.18097 AG-JEPA / 2611.17758 ADPKD 基因型 / 2611.17862 FlexCast——后三者由 `\\bMR\\b` / `\\bAR\\b` 缩写层误命中）· 手写文本识别 3 篇（2611.18143 / 2611.17952 / 2611.17966）· 空间转录组学与高光谱 2 篇（2611.17899 / 2611.17974）· V2X 与自动驾驶跟踪 2 篇（2611.18023 / 2611.17505）· 机器人操作与导航 4 篇（2611.18491 / 2611.18422 / 2611.18123 / 2611.17730）· 其他 5 篇（2611.18372 VLA 综述 / 2611.18033 梯田点云分割 / 2611.17495 LLM 串行深度 / 2611.18542 高斯采样理论 / 2611.17854 El Niño 预测）。
- 旧稿 replace 未入馆 **164 篇** → XR 命中 **4 篇**，剔除 1 篇（2610.30969 IORA，低自由度耦合手抓取）→ **backfill-1117 3 篇**。

## 全文抓取（第 4 步）
- 16 篇候选（13 + 3）跑 `scripts/fetch_fulltext.py`，严格串行 3s/篇（约 60 秒）：**15 篇 L0/FULL**（24,146–184,205 字符）+ **1 篇 L1/PARTIAL**。
- **人工复核改判**：2611.17903 脚本初判 L1/FULL（5,216 字符），抽看正文中段确认 ar5iv 仅返回**摘要页**（含 metadata + 摘要 + 样板，无任何正文章节），已改判 `evidence=PARTIAL` 并在 manifest 加 note；沙箱无 pdfminer/pypdf，L2 PDF 路径不可用，按摘要级评估并显式声明。
- WROTE=16>0；manifest 合并写入校验通过；无 L5、无 OCR。

## 评分与三关（第 5-6 步）
- 先抓全文再定稿。7 维加权：主批 **5 A / 6 B / 2 C（无 S，最高 3.93 EcoVGGT）**；backfill **3 A**（最高 4.07 HEIR）。
- 门① 最大 Jaccard **{G1:.3f}**（2611.17619 vs 库内 2610.18950，2026-10-15），通过；其余 9 篇均 <0.20。
- 门② 定稿 Top10 覆盖 **8 赛道**（重建与SLAM 3 / 内容生成 1 / 化身与人体 1 / 系统与平台 1 / 神经渲染 1 / 触觉与多模态 1 / 渲染与显示 1 / 评估与数据集 1；全批 9 赛道）→ **纯值排序即达标，未触发重筛**。
- 门③ 当日最高 **3.93 < 库内近 30 天 Top10 均分 4.4030**（窗口 2026-10-18~11-17、**398 条入窗**、现算）→ **非重磅日，无 S 级**（本批亦无 ≥4.2 达线论文，校准关未触发降级改写）。
- OUTDATED/SUPERSEDED **0 篇**。

## 产物（第 7-8 步）
- 报告 2 份（主批 + backfill）+ 原子笔记 **14 篇**（grade≥B：主批 11 + backfill 3；2 篇 C 级仅入馆）+ MOC 2 份 + 总索引刷新 + 7 维表/scored/run_log 各 2 套。
- registry 935 → **951**（+13 +3；备份 `papers/library/registry.jsonl.bak-20261117`；按 base_id 幂等）。
- notes 587 → **601**；daily 63 → **65**；MOC 51 → **53**。
- 门③ 现算值供下一批参考：**4.4030**（窗口逐日滚动，须再算）。

## 召回缺口记录（供下一批改进）
- 本批 KW 层仅命中 5/13，**8 篇靠标题级补扫**才入池，暴露关键词表缺口：`tactile`/`taxel`（TouchTwin）、`SDF`/`meshing`（FOMOS）、`affine correspondence`（ALoMa）、`bundle adjustment`（DeepBA）、`light field super-resolution`（MacroGS）、`image-based rendering`（DIRT）、`single-photon`/`SPAD`（D2ToF）、`monocular depth`（Signal Scaffolding / Zoom In）。
- 其中 3 篇进入 Top10（EcoVGGT / FOMOS / DIRT 等），说明**关键词层召回不足会直接影响榜单**。建议下一批在 `scripts/fetch_rss.py` 的 KW 表补入上述词（注意 `mesh`/`depth` 这类泛词需配限定词，避免噪声）。

## 观察（供后续批次）
- **前馈重建进入「推理工程」阶段**：EcoVGGT 用 31 帧固定键集 + pin/attach 精确分解把 VGGT 的 500 帧推理提速 8.5×（ATE 0.111→0.090）、π³ 版 1,000 帧 13.8×，且证明「按内容选键反而更差」——长序列 3D 基础模型的瓶颈已从精度转向 KV 组织方式。
- **经典几何求解器持续被摊销**：DeepBA 用 2.04M 参数 GNN 替代逐场景非线性最小二乘（CO3Dv2 AUC@30° 78.6 vs GASfM 71.2，参数少 71×）；ALoMa 把仿射对应从 32×32 局部块扩到图像与图像对层级（HPatches 误差低约一个数量级）。两者共同指向「几何前端正在被学习化重写」。
- **触觉成为本批最清晰的 XR 主线**：TouchTwin（880-taxel 手套实测触觉驱动 real-to-sim，握力比 0.31×/1.55× → 0.99×）与 backfill 的 The Missing Touch（32 像素电渗泵触觉显示以 30 Hz 回显接触几何，按键任务时间 −46%、π0.5 成功率 63.2%→92.3%）恰好构成「测」与「显」两端。
- **3DGS 子方向出现饱和信号**：稀疏视角 dropout 线（SLD+LBD）在 LLFF 3-view 仅比最强基线 DropAnSH-GS 高 0.02 dB，实为持平；相对地，MacroGS 从「基元数×视角数」的结构耦合入手（8 编码器 ×4 平均 PSNR +0.34–0.70 dB、解码快 10–18×），说明**结构性改写仍有余量，正则化调参已接近极限**。
- **深度感知的双向进展与警示**：D2ToF 把 8×8×100 SPAD 直方图一步扩散超分到 128×128（Middlebury RMSE 11.7 mm vs Marigold-DC 32.9 mm，单次前向 83 ms）；2611.17903 则指出度量深度模型把数字变焦误判为相机靠近（Depth Anything V2 的 α=0.95，理想 0）——对 AR 尺度估计是直接风险。
- **硬件类显示方向仍无破冰**：波导 / 可变焦 / Maxwellian / 全息光场连续多批无新增，本批 rendering 侧仅 DIRT（无训练、69 ms capture-to-image）触及端侧实时。
'''
open(f'papers/daily/{DATE}/run_log.md', 'w', encoding='utf-8').write(run_log_main)

run_log_bf = f'''# backfill-1117 执行日志

- **来源**：11-16 公告批次 RSS 全量 435 条中 **replace 类 164 篇**未入馆者，经摘要级 XR 过滤命中 **4 篇**，剔除 1 篇（2610.30969 IORA：低自由度耦合手抓取与支撑面几何，非 XR）→ 本批 **3 篇**。
- **诚实口径**：全部为 **v2 再公告**（API `updated` = 2026-11-13×3），原始投稿 2025-01-22 / 2026-08-19 / 2026-11-12；均非 11-16 当日新提交，单独编号、不参与当日重磅日判定。
- **全文**：3 篇全部 **L0/FULL**（46,770 / 112,020 / 184,205 字符）。
- **定稿 3 A（无 S）**：2608.19372 The Missing Touch **4.01**（32 像素电渗泵触觉显示 30 Hz 回显接触几何：按键任务时间 −46%、DTW 偏离 −77%，π0.5 微调成功率 63.2%→92.3%）· 2611.17238 HEIR **4.07**（17 人 / 300 session / 38.56 h / 1836 episode 人机双视角配对数据集，+人视角与注视使 Plan EM 63.51→78.11，但真机端到端成功率仅 18.52%）· 2501.12764 Grid-based Submap Joining **3.87**（栅格子图拼接 NLLS + pose-only GN 证明，误差比 Cartographer/SLAM Toolbox 小 3–12 倍，拼接 0.6–5.2 s）。
- **registry**：+3（batch=backfill-1117，幂等）。
'''
open('papers/daily/backfill-1117/run_log.md', 'w', encoding='utf-8').write(run_log_bf)
print('run_log written')
