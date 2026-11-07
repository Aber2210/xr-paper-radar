# -*- coding: utf-8 -*-
"""write_status_1108.py — 生成 2026-11-08 状态日产物（周日 02:30，周六 skipDays 无公告，同 11-01 模式）。

产物：
  papers/daily/2026-11-08/7dim-table.md   前沿参考表（23 篇，非当日新拉取）
  papers/daily/2026-11-08/run_log.md      执行日志
  reports/XR-Daily-Report-2026-11-08.md   状态报告
  papers/MOC/MOC-总索引.md                状态注记 + 批次索引行 + 页脚刷新
"""
import json, os, io, re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

reg = []
for l in io.open(os.path.join(ROOT, 'papers/library/registry.jsonl'), encoding='utf-8'):
    l = l.strip()
    if l:
        reg.append(json.loads(l))

# 前沿参考 = 11-07 运行批次（11-06 公告批次：主批 23 篇，无 backfill），按 value 降序
ref = [r for r in reg if r.get('batch') == '2026-11-07']
ref.sort(key=lambda x: (-x.get('value', 0), x['id']))

os.makedirs(os.path.join(ROOT, 'papers/daily/2026-11-08'), exist_ok=True)

GATE3 = 4.399
GATE3_WIN = '2026-10-09~2026-11-08（431 条入窗）'
GRADES = {}
for r in reg:
    GRADES[r.get('grade', 'C')] = GRADES.get(r.get('grade', 'C'), 0) + 1
NOTES_N = len([f for f in os.listdir(os.path.join(ROOT, 'papers/notes')) if f.endswith('.md')])

EXCL12 = [
    ('2611.06993', 'Batch-Conditioned Semantic Anchors for Robust Transductive Adaptation of Vision-Language Models（JPTA，视觉语言模型直推适配）'),
    ('2611.07063', 'SD-LoRA: Training-Time Structural Distillation into LoRA for Few-Shot Vision-Language Adaptation（少样本视觉语言适配）'),
    ('2611.07081', 'Wide View Synthesis from Overlapping Perspective Cameras in Autonomous Driving（WV-GS，自动驾驶宽视角合成）'),
    ('2611.07551', 'Training-Free Predictive Spatio-Temporal Token Pruning for Few-Step Autoregressive Video（PreSTP，视频扩散 token 剪枝加速）'),
    ('2611.07630', 'Real-Time Event-Based LED Tracking and Pose Estimation with PWM-Encoded Markers（事件相机 LED 跟踪，无人机引导）'),
    ('2611.07651', 'GraspBench: Execution-Aware Cross-Robot Evaluation of 6-DoF Grasp Generation in MuJoCo（跨机器人抓取评测）'),
    ('2611.07712', 'AffectiveVLA: Safe and Intent-Aware VLA Control for Human-Humanoid Social Interaction（人形机器人社交触摸）'),
    ('2611.08005', 'Deformable Contact-Aware 3D Object Placement（DCAP，可变接触 3D 物体放置）'),
    ('2611.08097', 'STEP: Spatiotemporal Training with Explicit Prediction for Perceptive Humanoid Locomotion（人形机器人运动）'),
    ('2611.08100', 'An Integrated Open-Source Stack for Vision-Based Autonomous Navigation of Wheeled Rovers（巡视器自主导航栈）'),
    ('2611.08372', 'MOMASPLAT: Dynamic Novel-View Demonstration Augmentation for Mobile Manipulation（移动操作示范增广）'),
    ('2611.08407', 'Social Humanoid: Socially Responsive Human-Humanoid Interaction（人-人形交互）'),
]

# ---------- 7dim-table.md ----------
L = []
L.append('# 7 维度对比表 · 2026-11-08（文献库最新前沿参考，非当日新拉取）')
L.append('')
L.append('> ⚠️ 说明：本运行日（周日 2026-11-08 02:30）经漏网对账 + 三源探针核验，**无新增可处理论文**：')
L.append('> ① listing 7 分类最新公告日均为 **2026-11-06（周五）**（11-07 周六、11-08 周日无公告日段，符合 arXiv skipDays 节律）；')
L.append('> ② 11-06 公告组经 show=500 单页全量复采 **458 个分类槽位 / 386 篇唯一论文**（逐分类 declared=got：CV 138/GR 11/HC 22/MM 2/RO 81/AI 198/IV 6），未入馆 **363 篇**；摘要级 XR 过滤命中 **12 篇**，与 11-07 运行显式剔除的 12 篇非 XR **逐篇一致** → **0 漏网**；')
L.append('> ③ API `submittedDate` 降序前沿 = **2026-11-05**（= 11-06 公告组来源，已全部入馆或已裁决；双主机 200）；')
L.append('> ④ RSS 7 分类 **全部 0 条目**（lastBuildDate Sat, 07 Nov 2026 05:00 UTC，周末节律空源；`fetch_rss.py` WROTE=0）。')
L.append('> 下表为**文献库最新前沿（11-07 运行处理的 11-06 公告批次：主批 23 篇，无 backfill）的 7 维参考表**，供查阅，**非「当日新论文」对比表**。')
L.append('')
L.append('> 维度与权重固定：`Value = 0.20·IMP + 0.20·NOV + 0.15·TEC + 0.15·EXP + 0.15·PER + 0.08·TRL + 0.07·REP`；分档：S≥4.2 / A 3.6–4.2 / B 3.0–3.6 / C<3.0')
L.append('')
L.append('> 拉取窗口：无（状态日；最新公告日 2026-11-06，已由 11-07 运行完整处理，本日复核 0 漏网）')
L.append('')
L.append('| # | arXiv | 标题 | 赛道 | IMP | NOV | TEC | EXP | PER | TRL | REP | 总分 | 等级 | 批次 | 证据 | 状态 |')
L.append('|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|')
for i, r in enumerate(ref, 1):
    s = r.get('scores') or {}
    star = ' ⭐' if r.get('in_top10') else ''
    L.append('| %d | [%s](https://arxiv.org/abs/%s) | %s%s | %s | %s | %s | %s | %s | %s | %s | %s | **%.2f** | %s | %s | %s | %s |' % (
        i, r['id'].split(':')[-1], r['id'].split(':')[-1],
        r.get('title_zh') or r.get('title', ''), star,
        r.get('track', ''),
        s.get('IMP', ''), s.get('NOV', ''), s.get('TEC', ''), s.get('EXP', ''),
        s.get('PER', ''), s.get('TRL', ''), s.get('REP', ''),
        r.get('value', 0), r.get('grade', ''), '主批 2026-11-07',
        r.get('evidence', ''), r.get('status', 'CURRENT')))
L.append('')
L.append('> 证据列：FULL = 完整正文（L0/L1）；本表 23 篇证据等级均以 registry 登记为准（11-07 运行：22 篇 L0/FULL + 1 篇 L0/PARTIAL 2611.08301 REACT）。')
L.append('> 门③ 参考：库内近 30 天 Top10 均分 **%.3f**（窗口 %s，现算）；本日 0 候选不触发校准关。' % (GATE3, GATE3_WIN))

with io.open(os.path.join(ROOT, 'papers/daily/2026-11-08/7dim-table.md'), 'w', encoding='utf-8') as f:
    f.write('\n'.join(L) + '\n')
print('written 7dim-table.md:', len(ref), 'ref rows')

# ---------- run_log.md ----------
R = []
R.append('# 运行日志 · 2026-11-08（周日 02:30 · 状态日：周六 skipDays 无公告）')
R.append('')
R.append('## 1. 漏网对账（Step 1）')
R.append('')
R.append('- listing 7 分类日期头（`scripts/audit_listing_1108.py`，show=500 单页×7 分类）：')
R.append('  **最新公告日全部为 2026-11-06（周五）**（cs.CV / cs.GR / cs.HC / cs.MM / cs.RO / cs.AI / eess.IV 七分类一致）。11-07（周六）无公告日段（skipDays 节律）；**无漏跑公告日**。')
R.append('- 11-06 公告组完整性复采（验证上批处理完整性）：逐分类 declared=got 全对齐（CV 138 / GR 11 / HC 22 / MM 2 / RO 81 / AI 198 / IV 6，槽位合计 458，全局去重 386 篇唯一论文）；未入馆 **363 篇**（386 − 23 篇 11-07 运行已入馆主批）。')
R.append('- 摘要级 XR 过滤（`scripts/run_filter_1108.py` → `scripts/filter_missed_xr_abstract.py`，meta fetched 363/363）：命中 **12 篇**，与 11-07 运行显式剔除的 12 篇非 XR **逐篇一致**：')
R.append('')
for pid, desc in EXCL12:
    R.append('  - %s %s' % (pid, desc))
R.append('')
R.append('  → **0 漏网、无 backfill**。')
R.append('- API 前沿条目归属核验：submittedDate 降序 top-5（2611.08486v1 / 2611.08485v1 / 2611.08477v1 / 2611.08449v1 / 2611.08441v1，published 均 2026-11-05）中 4 篇未入馆者均在上述 363 篇集合内，标题明确非 XR（图表技法 / grounded 推理 / 视觉规划 / 骑行安全感知），与摘要级过滤结论一致。')
R.append('- 落盘：`data/audit_1108_days.json` / `data/audit_1108_alldays.json` / `data/missed_listing_1108.json`（363 篇）/ `data/missed_listing_1108_days.json` / `data/missed_xr_abstract_1108.json`（12 篇）/ `data/audit_1108_newday.json`（>11-06 日组：无）。')
R.append('')
R.append('## 2. 数据源探测（Step 2）')
R.append('')
R.append('- API 双主机探针（export.arxiv.org 200；arxiv.org 备用）：`submittedDate` 降序前沿 = **2026-11-05**（cs.CV 抽查 5 条一致；11-05 提交 = 11-06 公告组来源，已全部入馆或已裁决）。')
R.append('- RSS（`rss.arxiv.org` 7 分类探针）：**全部 0 条目**（lastBuildDate Sat, 07 Nov 2026 05:00 UTC；周日 skipDays 节律空源，非代理故障）。')
R.append('- 判定：**0 篇新候选**，不进入 Steps 3-7。')
R.append('')
R.append('## 3. 甄别 / 全文 / 评分 / Top10（Steps 3-7）')
R.append('')
R.append('- 候选池 0 篇 → 不触发全文抓取、7 维评分、覆盖度三关与 Top10 选拔。')
R.append('- **未伪造 Top10 / 评分 / S 级**（诚实口径硬约束）。')
R.append('- 门③ 现算参考：库内近 30 天 Top10 均分 **%.3f**（窗口 %s；Top10 = SMoRe 4.57 / 视频扩散化身 4.57 / Open-HumanScale 4.57 / ACD-GS 4.37 / XM4D 4.36 / RacerGS 4.35 / EgoExplorer 4.30 / dGS-dBS 4.30 / CognitiveReality 4.30 / RESPLE2 4.30）。' % (GATE3, GATE3_WIN))
R.append('')
R.append('## 4. 产物与发布（Steps 8-9）')
R.append('')
R.append('- registry **无变更**（%d 条：S%d/A%d/B%d/C%d；本次未修改故无备份需要）；原子笔记 %d 篇无新增。' % (len(reg), GRADES.get('S',0), GRADES.get('A',0), GRADES.get('B',0), GRADES.get('C',0), NOTES_N))
R.append('- 产物：本 run_log + `papers/daily/2026-11-08/7dim-table.md`（23 篇前沿参考）+ `reports/XR-Daily-Report-2026-11-08.md` + MOC 总索引维护。')
R.append('- 前端：BATCH_LABELS 补 11-08 标签 → 重建 hub → DATA 计数核验 → node --check 双 script 块 → CDP 冒烟 → 双渠道发布（详见报告 §5.5）。')
R.append('')
R.append('## 5. 异常与教训')
R.append('')
R.append('- 周末状态日模式第 7 次验证（同 11-01；11-07 周六为真实运行日，因 11-06 公告组于周五 00:00 UTC 释放）：周日运行 listing 最新公告日仍为 11-06 且该组已全量入馆，三源互证 0 新稿。')
R.append('- 下次运行（11-09 周一 02:30）：预期仍为状态日（周末积压公告时刻 = 周一 00:00 UTC = 当日 08:00 北京时间，晚于运行时刻 02:30，同 11-02 模式）；**11-10（周二）02:30 处理 11-09 周日公告批次**（若 11-09 有公告）；门③ 务必现算（勿沿用 %.3f）。' % GATE3)
R.append('- 渠道①（workbuddy_sites_deploy）自 10-21 起连续不可用（本会话复检），若恢复可用须优先补部署（挂账批次 10-21~11-08 共 19 批）；硬件类渲染缺口仍仅 CVQPG + HoOPOE 两篇破冰，继续补波导/可变焦/Maxwellian/光场。')

with io.open(os.path.join(ROOT, 'papers/daily/2026-11-08/run_log.md'), 'w', encoding='utf-8') as f:
    f.write('\n'.join(R) + '\n')
print('written run_log.md')

# ---------- 报告 ----------
P = []
P.append('# XR 每日论文雷达 · 运行报告 · 2026-11-08（周日 02:30）')
P.append('')
P.append('> **诚实口径声明**：本运行日（2026-11-08，周日 02:30）**无新增可处理论文**。经三源交叉验证：listing 7 分类最新公告日均为 **2026-11-06（周五）**（11-07 周六、11-08 周日无公告日段，符合 arXiv skipDays 节律）；API `submittedDate` 前沿停滞 2026-11-05（11-06 公告组来源，已全部入馆或已裁决）；RSS 7 分类全部 0 条目（lastBuildDate Sat, 07 Nov 2026 05:00 UTC）。上一批（11-07 运行）处理的 11-06 公告批次经本日 show=500 单页全量复采复核：458 槽位 declared=got、386 篇唯一论文、未入馆 363 篇摘要级 XR 过滤 12 篇命中均为 11-07 运行已显式剔除的非 XR 稿（逐篇一致）→ **0 漏网、无 backfill**。**本报告不包含任何「当日新论文」解读、不虚构 Top10/评分/S 级**；文末附表为文献库最新前沿参考。')
P.append('')
P.append('---')
P.append('')
P.append('## 一、执行摘要')
P.append('')
P.append('| 项 | 结论 |')
P.append('|---|---|')
P.append('| 运行性质 | **状态报告日**（周日，周六 skipDays 无公告；漏网对账 + 三源探针 + 采集完整性复核 + 知识库存量维护 + 前端重建与双渠道发布） |')
P.append('| 公告状态 | listing 7 分类最新公告日均为 **2026-11-06**；11-07/11-08 周末无公告日段（skipDays 节律）；无漏跑公告日 |')
P.append('| 漏网对账 | 11-06 公告组 show=500 单页全量复采：逐分类 declared=got（CV 138/GR 11/HC 22/MM 2/RO 81/AI 198/IV 6，槽位 458、唯一论文 386）；未入馆 363 篇摘要级 XR 命中 12 篇，均为 11-07 运行已剔非 XR → **0 漏网**；无需 backfill |')
P.append('| 数据源 | API 双主机 200（submittedDate 前沿 11-05，已全部入馆或已裁决）；RSS 7 分类全部 0 条目（周末节律空源，WROTE=0） |')
P.append('| 新入馆论文 | **0 篇**（registry 维持 **%d 条**：S %d / A %d / B %d / C %d） |' % (len(reg), GRADES.get('S',0), GRADES.get('A',0), GRADES.get('B',0), GRADES.get('C',0)))
P.append('| 新原子笔记 | 0 篇（维持 **%d 篇**） |' % NOTES_N)
P.append('| 库内近 30 天 Top10 均分 | **%.3f**（现算，窗口 %s；门③ 为校准关，本日无候选不触发） |' % (GATE3, GATE3_WIN))
P.append('| 交付 | 状态报告 1 + 前沿参考 7 维表 1（23 篇）+ run_log 1 + MOC 总索引维护 + 前端重建与双渠道发布 |')
P.append('')
P.append('**下一批预期**：11-09（周一）02:30 运行预期仍为状态日（周末积压公告时刻 = 周一 00:00 UTC = 当日 08:00 北京时间，晚于运行时刻，同 11-02 模式）；**11-10（周二）02:30 处理 11-09 公告批次**（若 11-09 周日有公告释放）；门③ 务必现算（勿沿用 %.3f）。' % GATE3)
P.append('')
P.append('---')
P.append('')
P.append('## 二、漏网对账（Step 1）')
P.append('')
P.append('对账目的：确认自上一批次公告日（2026-11-06）至今是否有漏跑公告日或漏收 XR 论文。')
P.append('')
P.append('### 2.1 公告日头核验（目标窗口 ≥ 2026-11-07）')
P.append('')
P.append('| 分类 | 最新公告日 | 11-06 组 declared | 11-06 组实采 |')
P.append('|---|---|---:|---:|')
P.append('| cs.CV | Fri, 6 Nov 2026 | 138 | 138 |')
P.append('| cs.GR | Fri, 6 Nov 2026 | 11 | 11 |')
P.append('| cs.HC | Fri, 6 Nov 2026 | 22 | 22 |')
P.append('| cs.MM | Fri, 6 Nov 2026 | 2 | 2 |')
P.append('| cs.RO | Fri, 6 Nov 2026 | 81 | 81 |')
P.append('| cs.AI | Fri, 6 Nov 2026 | 198 | 198 |')
P.append('| eess.IV | Fri, 6 Nov 2026 | 6 | 6 |')
P.append('')
P.append('- **无 11-07/11-08 公告日组**：七分类 recent 视图一致；周末无公告符合 arXiv RSS `<skipDays>` 节律（同 11-01 模式）。')
P.append('- **三源互证**：① listing 七分类最新日组全部为 Fri, 6 Nov 2026；② API `submittedDate` 降序前沿 = 2026-11-05（即 11-06 公告组来源）；③ RSS 7 分类 0 条目（lastBuildDate 2026-11-07 05:00 UTC）。')
P.append('')
P.append('### 2.2 11-06 公告组完整性复核（验证上批处理完整性）')
P.append('')
P.append('本日复采方案（`scripts/audit_listing_1108.py`，show=500 单页×7 分类）：11-06 组各分类条目数均 <500，单页即完整包含目标组。结果：')
P.append('')
P.append('- 逐分类 **declared = got**（上表），槽位合计 458，全局去重后 **386 篇唯一论文**，与 11-07 运行复采数字逐项一致；')
P.append('- 未入馆 **363 篇**（386 − 23 篇 11-07 运行已入馆主批；11-07 运行无 backfill，listing 日组天然只含新提交）；')
P.append('- 摘要级 XR 过滤（`filter_missed_xr_abstract.py`，363/363 fetched）：命中 **12 篇**，与 11-07 运行显式剔除的 12 篇非 XR **逐篇一致**：')
P.append('')
P.append('| ID | 标题 | 11-07 运行裁决 |')
P.append('|---|---|---|')
for pid, desc in EXCL12:
    P.append('| %s | %s | 非 XR（已显式剔除） |' % (pid, desc))
P.append('')
P.append('- API 前沿条目归属核验：submittedDate top-5 中 4 篇未入馆者（2611.08486 / 2611.08485 / 2611.08449 / 2611.08441）均在 363 篇集合内，标题明确非 XR（图表技法 / grounded 推理 / 视觉规划 / 骑行安全感知），与摘要级过滤结论一致。')
P.append('- 结论：**0 漏网、无 backfill**。')
P.append('')
P.append('---')
P.append('')
P.append('## 三、数据源探测记录（Step 2）')
P.append('')
P.append('- API 双主机探针 200；`submittedDate` 降序前沿 = **2026-11-05**（cs.CV top-5 published 全部 11-05；= 11-06 公告组来源）。')
P.append('- RSS（7 分类探针）：**全部 0 条目**（lastBuildDate Sat, 07 Nov 2026 05:00 UTC，周末节律空源）。')
P.append('- 判定：**0 篇新候选**，不进入 Steps 3-7。')
P.append('')
P.append('---')
P.append('')
P.append('## 四、文献库最新前沿参考（11-06 公告批次 · 23 篇 · 非当日新拉取）')
P.append('')
P.append('以下为 11-07 运行处理的 11-06 公告批次 7 维参考表（主批 23 篇），完整版见 [papers/daily/2026-11-08/7dim-table.md](../papers/daily/2026-11-08/7dim-table.md)：')
P.append('')
P.append('| # | arXiv | 标题 | 赛道 | 总分 | 等级 |')
P.append('|---|---|---|---|---|---|')
for i, r in enumerate(ref, 1):
    star = ' ⭐' if r.get('in_top10') else ''
    P.append('| %d | %s | %s%s | %s | **%.2f** | %s |' % (
        i, r['id'].split(':')[-1], (r.get('title_zh') or r.get('title', ''))[:38], star,
        r.get('track', ''), r.get('value', 0), r.get('grade', '')))
P.append('')
P.append('---')
P.append('')
P.append('## 五、附录')
P.append('')
P.append('### 5.1 覆盖度三关（本日不触发）')
P.append('')
P.append('- 门① 同质去重 / 门② 赛道覆盖 / 门③ 价值天花板：候选池 0 篇，三关均不触发。')
P.append('- 门③ 参考值现算：库内近 30 天 Top10 均分 **%.3f**（窗口 %s；Top10 = 2610.19674 SMoRe 4.57 / 2610.23772 视频扩散化身 4.57 / 2611.06817 Open-HumanScale 4.57 / 2610.39399 ACD-GS 4.37 / 2611.07902 XM4D 4.36 / 2610.34263 RacerGS 4.35 / 2610.18872 EgoExplorer 4.30 / 2610.22778 dGS/dBS 4.30 / 2609.31418 CognitiveReality 4.30 / 2610.37602 RESPLE2 4.30）。' % (GATE3, GATE3_WIN))
P.append('')
P.append('### 5.2 证据等级分布')
P.append('')
P.append('- 本日无新抓取。参考表 23 篇证据等级：22 篇 L0/FULL + 1 篇 L0/PARTIAL（2611.08301 REACT，arXiv HTML 仅补充材料，11-07 运行人工改判并显式声明）；无 ABSTRACT_ONLY。')
P.append('')
P.append('### 5.3 失败/降级清单')
P.append('')
P.append('- 无抓取失败。数据源状态：RSS 周末节律空源（7 分类 0 条目，非故障）；API 双主机 200。')
P.append('')
P.append('### 5.4 产物清单')
P.append('')
P.append('| 产物 | 路径 |')
P.append('|---|---|')
P.append('| 状态报告 | `reports/XR-Daily-Report-2026-11-08.md` |')
P.append('| 前沿参考 7 维表 | `papers/daily/2026-11-08/7dim-table.md`（23 篇） |')
P.append('| 运行日志 | `papers/daily/2026-11-08/run_log.md` |')
P.append('| 对账数据 | `data/audit_1108_days.json` / `data/audit_1108_alldays.json` / `data/missed_listing_1108.json` / `data/missed_listing_1108_days.json` / `data/missed_xr_abstract_1108.json` / `data/audit_1108_newday.json` |')
P.append('| MOC 总索引 | `papers/MOC/MOC-总索引.md`（11-08 状态注记 + 批次索引行 + 页脚刷新） |')
P.append('| 前端 | `web/xr-paper-hub.html`（重建） |')
P.append('')
P.append('### 5.5 发布记录')
P.append('')
P.append('- 渠道① WorkBuddy 托管（workbuddy_sites_deploy）：见收尾汇报（若工具不可用则挂账，自 10-21 起连续不可用）。')
P.append('- 渠道② GitHub Pages：见收尾汇报（commit + push_to_github.py --incremental + deploy run + Pages 200 核验）。')
P.append('')
P.append('---')
P.append('')
P.append('*报告生成：2026-11-08 02:30 自动化运行（xr-paper-daily-brief skill · 9 步流水线）。*')

with io.open(os.path.join(ROOT, 'reports/XR-Daily-Report-2026-11-08.md'), 'w', encoding='utf-8') as f:
    f.write('\n'.join(P) + '\n')
print('written report, chars:', len('\n'.join(P)))

# ---------- MOC-总索引.md 维护 ----------
moc_path = os.path.join(ROOT, 'papers/MOC/MOC-总索引.md')
moc = io.open(moc_path, encoding='utf-8').read()

# 1) 状态注记：插在 11-07 状态注记之后（若尚无 11-08 注记）
if '状态注记（2026-11-08）' not in moc:
    note = ('> **状态注记（2026-11-08）**：周日 02:30，**无新增可处理论文**（周六 skipDays 无公告，周末状态日模式第 7 次验证，同 11-01）。'
            'listing 7 分类最新公告日均为 **2026-11-06（周五）**（11-07/11-08 周末无公告日段）；'
            'API `submittedDate` 前沿 = **11-05**（已全部入馆或已裁决）；RSS 7 分类全部 0 条目（lastBuildDate 2026-11-07 05:00 UTC，周末节律空源）。'
            '11-06 公告组 show=500 单页全量复采：逐分类 declared=got（CV 138/GR 11/HC 22/MM 2/RO 81/AI 198/IV 6，槽位 458、唯一论文 386），未入馆 363 篇摘要级 XR 命中 12 篇均为 11-07 运行已剔非 XR（逐篇一致）→ **0 漏网、无 backfill**。'
            '未伪造 Top10/评分/S 级；registry 维持 **%d 条**（S%d/A%d/B%d/C%d）；门③ 现算参考 **%.3f**（窗口 %s）。'
            '详见 [状态报告](../../reports/XR-Daily-Report-2026-11-08.md)。') % (len(reg), GRADES.get('S',0), GRADES.get('A',0), GRADES.get('B',0), GRADES.get('C',0), GATE3, GATE3_WIN)
    # 找到 11-07 状态注记行的末尾
    anchor = '详见 [运行报告](../../reports/XR-Daily-Report-2026-11-07.md)。'
    idx = moc.find(anchor)
    if idx >= 0:
        insert_at = idx + len(anchor)
        moc = moc[:insert_at] + '\n' + note + moc[insert_at:]
        print('MOC: 11-08 状态注记已插入')
    else:
        print('MOC WARN: 11-07 状态注记锚点未找到')

# 2) 批次索引表：补 11-08 行（插在 11-07 行之后）
row = '| 2026-11-08 | — | **0 新稿**（周日：listing 七分类最新公告日 11-06 + API 前沿 11-05 + RSS 7 分类空源三源互证；周六 skipDays 无公告） | 状态报告日；11-06 公告组 show=500 单页复采 declared=got（458 槽位/386 唯一），未入馆 363 篇摘要级 12 篇命中均为 11-07 运行已剔非 XR（逐篇一致），0 漏网；门③ 现算 4.399 |'
if '| 2026-11-08 |' not in moc:
    lines = moc.split('\n')
    for i, l in enumerate(lines):
        if l.startswith('| 2026-11-07 |'):
            lines.insert(i + 1, row)
            moc = '\n'.join(lines)
            print('MOC: 批次索引 11-08 行已插入')
            break

# 3) 页脚刷新
footer_new = ('*最后更新：2026-11-08（周日状态日：listing 七分类最新公告日 11-06 + API 前沿 11-05 + RSS 7 分类空源三源互证；'
              '周六 skipDays 无公告；11-06 公告组 show=500 单页复采 declared=got，未入馆 363 篇摘要级 12 篇命中均为 11-07 运行已剔非 XR，0 漏网无 backfill；registry %d / 笔记 %d）。*' % (len(reg), NOTES_N))
moc = re.sub(r'\*最后更新：[^\n]*\*', footer_new, moc, count=1)

with io.open(moc_path, 'w', encoding='utf-8') as f:
    f.write(moc)
print('MOC-总索引.md updated')
