# -*- coding: utf-8 -*-
"""write_status_1113.py — 2026-11-13 状态日产物（周五 02:30 · 11-12 公告批次未释放）。

产物：
  papers/daily/2026-11-13/7dim-table.md   前沿参考表（19 篇：11-12 主批 15 + backfill-1112 4，非当日新拉取）
  papers/daily/2026-11-13/run_log.md      执行日志
  reports/XR-Daily-Report-2026-11-13.md   状态报告
  papers/MOC/MOC-总索引.md                状态注记 + 速查入口 + 批次索引行 + 页脚刷新
"""
import io, json, os, re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

reg = []
for l in io.open(os.path.join(ROOT, 'papers/library/registry.jsonl'), encoding='utf-8'):
    l = l.strip()
    if l:
        reg.append(json.loads(l))

ref = [r for r in reg if r.get('batch') in ('2026-11-12', 'backfill-1112')]
ref.sort(key=lambda x: (-x.get('value', 0), x['id']))

os.makedirs(os.path.join(ROOT, 'papers/daily/2026-11-13'), exist_ok=True)

GATE3 = 4.437
GATE3_WIN = '2026-10-14~2026-11-13（454 条入窗）'
GATE3_TOP = ('2610.19674 SMoRe 4.57 / 2610.23772 视频扩散化身 4.57 / 2611.06817 Open-HumanScale 4.57 / '
             '2611.11169 Map2SLAM 4.57 / 2610.39399 ACD-GS 4.37 / 2611.09458 左右一致立体匹配 4.37 / '
             '2611.07902 XM4D 4.36 / 2610.34263 RacerGS 4.35 / 2611.08578 HaNDF 4.34 / 2609.31418 CognitiveReality 4.30')
GRADES = {}
for r in reg:
    GRADES[r.get('grade', 'C')] = GRADES.get(r.get('grade', 'C'), 0) + 1
NOTES_N = len([f for f in os.listdir(os.path.join(ROOT, 'papers/notes')) if f.endswith('.md')])
DAILY_N = len([d for d in os.listdir(os.path.join(ROOT, 'papers/daily'))])

EXCL13 = [
    ('2611.12932', 'URL-Sim: Unified and Regulated LiDAR Simulation（LiDAR 仿真/自动驾驶数据合成）'),
    ('2611.12949', 'Maze Runner: Autonomous Maze Navigation（机器人迷宫导航与定位）'),
    ('2611.12976', 'Partition, Refine, and Detect（开放词汇目标检测）'),
    ('2611.13030', 'APS-VLA: Action-Guided Token Pruning（VLA 推理加速）'),
    ('2611.13057', 'Continuous-Time Set-Transformers for WiFi-IMU Indoor Localization（室内定位）'),
    ('2611.13062', 'Elicitation of the parameters of a multi-criteria sorting model（多准则决策建模）'),
    ('2611.13307', 'Does Haptic Connection to a Healthy Partner Improve Motor Learning in Chronic Stroke?（触觉康复训练，非 XR 呈现/交互核心）'),
    ('2611.13610', 'From Egocentric Human Video to Robot Manipulation（具身智能综述，泛化口径）'),
    ('2611.13685', 'Ego Guidance: Robot Policy Learning with Action-Free Egocentric Videos（机器人策略学习）'),
    ('2611.13784', 'Marrying Capacity and Precision for Efficient 2D Gaussian Image Representation（2D 高斯图像表示/压缩，非场景重建）'),
    ('2611.14033', 'Few-Step Streaming Video Generation via Condition Shifting（视频生成加速）'),
    ('2611.14093', 'BODYinTRANSIT-Lab: Multimodal Dataset for Sensory-Driven Transformation（身体感知数据集，XR 关联薄弱）'),
    ('2611.14373', 'Gaussian Process-Augmented MPC Contouring Control for 6-DoF Trajectory Tracking（加工轨迹跟踪控制）'),
]

# ---------- 7dim-table.md ----------
L = []
L.append('# 7 维度对比表 · 2026-11-13（文献库最新前沿参考，非当日新拉取）')
L.append('')
L.append('> ⚠️ 说明：本运行日（周五 2026-11-13 02:30）经漏网对账 + 三源探针核验，**无新增可处理论文**：')
L.append('> ① listing 7 分类（cs.CV / cs.GR / cs.HC / cs.MM / cs.RO / cs.AI / eess.IV）最新公告日均为 **2026-11-11（周三）**，**无 11-12（周四）公告日组**；缓存穿透复验（`?_cb=` 随机参数）与 `pastweek` 视图一致，跨学科复核（math.AP / physics.optics / cs.CL / q-bio.NC）最新公告日同为 11-11 → **arXiv 11-12 公告批次未释放（工作日公告跳空，10-29 之后第 2 次）**；')
L.append('> ② API `submittedDate` 降序前沿 = **2026-11-10**（`--since 2026-11-11` 回 **WROTE=0**；`submittedDate:[202611120000 TO 202611122359]` cs.CV 命中 **0** 篇）；')
L.append('> ③ RSS 7 分类 **全部 0 条目**（`lastBuildDate` = Thu, 12 Nov 2026 05:00 UTC；`fetch_rss.py` WROTE=0）；')
L.append('> ④ 11-11 公告组（上批）完整性复采：逐分类 declared=got（CV 149 / GR 6 / HC 34 / MM 14 / RO 69 / AI 248 / IV 12，槽位 **532**、唯一论文 **436**），未入馆 **421 篇**摘要级 XR 过滤（421/421 fetched，覆盖率 1.0000）命中 **13 篇**，与 11-12 运行显式剔除的 13 篇非 XR **逐篇 id 一致（双向差集 0）→ 0 漏网**。')
L.append('> 下表为**文献库最新前沿（11-12 运行处理的 11-11 公告批次：主批 15 篇 + backfill-1112 4 篇）的 7 维参考表**，供查阅，**非「当日新论文」对比表**。')
L.append('')
L.append('> 维度与权重固定：`Value = 0.20·IMP + 0.20·NOV + 0.15·TEC + 0.15·EXP + 0.15·PER + 0.08·TRL + 0.07·REP`；分档：S≥4.2 / A 3.6–4.2 / B 3.0–3.6 / C<3.0')
L.append('')
L.append('> 拉取窗口：无（状态日；最新公告日 2026-11-11，已由 11-12 运行完整处理，本日复核 0 漏网）')
L.append('')
L.append('| # | arXiv | 标题 | 赛道 | IMP | NOV | TEC | EXP | PER | TRL | REP | 总分 | 等级 | 批次 | 证据 | 状态 |')
L.append('|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|')
for i, r in enumerate(ref, 1):
    s = r.get('scores') or {}
    star = ' ⭐' if r.get('in_top10') else ''
    batch_tag = '主批 2026-11-12' if r.get('batch') == '2026-11-12' else 'backfill-1112'
    L.append('| %d | [%s](https://arxiv.org/abs/%s) | %s%s | %s | %s | %s | %s | %s | %s | %s | %s | **%.2f** | %s | %s | %s | %s |' % (
        i, r['id'].split(':')[-1], r['id'].split(':')[-1],
        r.get('title_zh') or r.get('title', ''), star,
        r.get('track', ''),
        s.get('IMP', ''), s.get('NOV', ''), s.get('TEC', ''), s.get('EXP', ''),
        s.get('PER', ''), s.get('TRL', ''), s.get('REP', ''),
        r.get('value', 0), r.get('grade', ''), batch_tag,
        r.get('evidence', ''), r.get('status', 'CURRENT')))
L.append('')
L.append('> 证据列：FULL = 完整正文（L0/L1）；本表 19 篇证据等级以 registry 登记为准（11-12 运行：18 篇 L0/FULL + 1 篇 L1/PARTIAL —— 2611.13296 的 arXiv HTML 404、ar5iv 仅摘要页 4,350 字符，已人工抽看无正文节改判 PARTIAL，按摘要级评估并显式声明）。')
L.append('> 门③ 参考：库内近 30 天 Top10 均分 **%.3f**（窗口 %s，现算）；本日 0 候选不触发校准关。' % (GATE3, GATE3_WIN))

with io.open(os.path.join(ROOT, 'papers/daily/2026-11-13/7dim-table.md'), 'w', encoding='utf-8') as f:
    f.write('\n'.join(L) + '\n')
print('written 7dim-table.md:', len(ref), 'ref rows')

# ---------- run_log.md ----------
R = []
R.append('# 运行日志 · 2026-11-13（周五 02:30 · 工作日公告跳空状态日：11-12 公告批次未释放）')
R.append('')
R.append('## 1. 漏网对账（Step 1）')
R.append('')
R.append('- listing 7 分类日期头（`scripts/audit_listing_1113.py`，show=500 单页×7 分类，PREV_DAY=2026-11-11 / NEW_DAY=2026-11-12）：')
R.append('  **最新公告日全部为 2026-11-11（周三）**，**无 11-12（周四）公告日组**（`newest=2026-11-11`，NEW_DAY declared=None / got=0）。缓存穿透复验（cs.CV `recent?cb=` 随机参数 → 仍 149 条 11-11 组；`pastweek` 视图同为 11-11）与跨学科复核（math.AP 51 / physics.optics 25 / cs.CL 112 / q-bio.NC 15，最新日组均为 11-11）→ **arXiv 11-12 公告批次未释放，非本分类/本机故障**。')
R.append('- 11-11 公告组完整性复采（验证上批处理完整性）：逐分类 **declared=got**（CV 149 / GR 6 / HC 34 / MM 14 / RO 69 / AI 248 / IV 12，槽位合计 **532**，全局去重 **436 篇唯一论文**），与 11-12 运行采集数字逐项一致；')
R.append('- 未入馆 **421 篇**（436 − 15 篇 11-12 运行已入馆主批；该批无 listing 侧漏网），摘要级 XR 过滤（`scripts/filter_missed_1113.py`，**50 id/批 + 12s 间隔**，meta fetched **421/421**、覆盖率 **1.0000**、缺失 0）命中 **13 篇**：')
R.append('')
for pid, desc in EXCL13:
    R.append('  - %s %s' % (pid, desc))
R.append('')
R.append('  → 与 11-12 运行显式剔除的 13 篇非 XR **逐篇 id 一致（双向差集 0）**，维持上批裁决 → **0 漏网、无 backfill**。')
R.append('- 落盘：`data/audit_1113_days.json` / `data/audit_1113_alldays.json` / `data/missed_listing_1113.json`（421 篇）/ `data/newday_1113.json`（空）/ `data/missed_new_1113.json`（空）/ `data/missed_xr_abstract_1113.json`（13 篇）。')
R.append('')
R.append('## 2. 数据源探测（Step 2）')
R.append('')
R.append('- API 双主机探针 200（`export.arxiv.org` / `arxiv.org/api/query`）；`submittedDate` 降序前沿 = **2026-11-10**（cs.CV / cs.AI / cs.GR top-8 最新 published 均为 11-10）；`submittedDate:[202611120000 TO 202611122359]` cs.CV 命中 **0** 篇；`fetch_arxiv.py --since 2026-11-11 --max 200` → **WROTE=0**（越过下界即止，已全部入馆）。')
R.append('- RSS（`rss.arxiv.org` 7 分类）：**全部 0 条目**，`lastBuildDate` = Thu, 12 Nov 2026 05:00 UTC（7 分类同批重建，非代理故障）；`fetch_rss.py` **WROTE=0**。')
R.append('- 判定：**0 篇新候选**，不进入 Steps 3-7。')
R.append('')
R.append('## 3. 甄别 / 全文 / 评分 / Top10（Steps 3-7）')
R.append('')
R.append('- 候选池 0 篇 → 不触发全文抓取、7 维评分、覆盖度三关与 Top10 选拔。')
R.append('- **未伪造 Top10 / 评分 / S 级**（诚实口径硬约束）。')
R.append('- 门③ 现算参考：库内近 30 天 Top10 均分 **%.3f**（窗口 %s；Top10 = %s）。' % (GATE3, GATE3_WIN, GATE3_TOP))
R.append('')
R.append('## 4. 产物与发布（Steps 8-9）')
R.append('')
R.append('- registry **907 条**（S%d/A%d/B%d/C%d）：本日无新增入馆；**另执行 1 处数据修补** —— 2611.08578 的 `title` 字段曾被误写为裸 ID（`2611.08578`），经 arXiv API 核验真实标题为 `HaNDF: Object-Conditioned Geometric Neural Hand Distance Fields`，已按 `registry.jsonl.bak-20261113` 备份后修正 registry 与对应原子笔记 frontmatter（title_zh/评分不变）。' % (
    GRADES.get('S', 0), GRADES.get('A', 0), GRADES.get('B', 0), GRADES.get('C', 0)))
R.append('- 原子笔记 **%d 篇**（无新增）；daily 目录 **%d 个**（新增 2026-11-13）。' % (NOTES_N, DAILY_N))
R.append('- 产物：本 run_log + `papers/daily/2026-11-13/7dim-table.md`（19 篇前沿参考）+ `reports/XR-Daily-Report-2026-11-13.md` + MOC 总索引维护。')
R.append('- 前端：BATCH_LABELS 补 11-13 标签 → 重建 hub → DATA 计数核验 → node --check 双 script 块 → CDP 冒烟 → 双渠道发布（详见报告 §5.5）。')
R.append('')
R.append('## 5. 异常与教训')
R.append('')
R.append('- **工作日公告跳空第 2 次**（首次为 2026-10-29 周四）：11-12（周四）公告批次未释放，三源 + 跨学科四分类五重互证。按 10-29→10-30 先例，延迟批次预计在 **11-13 00:00 UTC（= 11-13 08:00 北京时间）** 释放，晚于本运行时刻 02:30 → **下一调度（11-14 周六 02:30）应能见到 11-12 或 11-13 公告组，须按标准流水线补处理并显式标注「公告日≠拉取日」**。')
R.append('- 采集完整性复核再次以「逐分类 declared=got + 未入馆集合逐篇比对 + 摘要级 id 双向差集」三段式完成；本批 421 篇摘要级覆盖率 1.0000，未出现 11-12 记录过的 id_list 429 静默丢批（50 id/批 + 12s 间隔生效）。')
R.append('- 门③ 现值 %.3f 已较上批 4.4370 持平（Top10 集合未变）；下次运行仍须现算，勿沿用。' % GATE3)
R.append('- 渠道①（workbuddy_sites_deploy）自 10-21 起连续不可用且 URL 已 403；若恢复可用须优先补部署（挂账批次 10-21~11-12 共 23 批 + 本批 11-13）。硬件类渲染缺口仍仅 CVQPG + HoOPOE 两篇破冰。')

with io.open(os.path.join(ROOT, 'papers/daily/2026-11-13/run_log.md'), 'w', encoding='utf-8') as f:
    f.write('\n'.join(R) + '\n')
print('written run_log.md')

# ---------- 报告 ----------
P = []
P.append('# XR 每日论文雷达 · 运行报告 · 2026-11-13（周五 02:30）')
P.append('')
P.append('> **诚实口径声明**：本运行日（2026-11-13，周五 02:30）**无新增可处理论文**——**arXiv 2026-11-12（周四）公告批次未释放**（工作日公告跳空，继 2026-10-29 之后第 2 次）。五重互证：① listing 7 分类最新公告日均为 **2026-11-11（周三）**，无 11-12 日组；② 缓存穿透复验（`recent?cb=`）与 `pastweek` 视图一致；③ 跨学科复核 math.AP / physics.optics / cs.CL / q-bio.NC 最新日组同为 11-11 → 非本分类故障；④ API `submittedDate` 前沿 **11-10**、`[20261112 TO 20261112]` cs.CV 命中 0、`--since 2026-11-11` WROTE=0；⑤ RSS 7 分类全部 0 条目（`lastBuildDate` 11-12 05:00 UTC）。上一批（11-12 运行）处理的 11-11 公告组经本日全量复采复核：**532 槽位 declared=got、436 篇唯一论文**，未入馆 421 篇摘要级 XR 命中 13 篇，与 11-12 运行已显式剔除的 13 篇**逐篇 id 一致** → **0 漏网、无 backfill**。**本报告不含任何「当日新论文」解读，不虚构 Top10/评分/S 级**；第四节为文献库最新前沿参考。')
P.append('')
P.append('---')
P.append('')
P.append('## 一、执行摘要')
P.append('')
P.append('| 项 | 结论 |')
P.append('|---|---|')
P.append('| 运行性质 | **状态报告日**（工作日公告跳空：11-12 公告批次未释放；漏网对账 + 五重源核验 + 采集完整性复核 + 知识库存量维护 + 前端重建与双渠道发布） |')
P.append('| 公告状态 | listing 7 分类最新公告日均为 **2026-11-11（周三）**；**无 11-12（周四）公告日组**；跨学科四分类最新日组同为 11-11 → arXiv 公告流水线跳空，非本机故障 |')
P.append('| 漏网对账 | 11-11 公告组 show=500 单页全量复采：逐分类 declared=got（CV 149/GR 6/HC 34/MM 14/RO 69/AI 248/IV 12，槽位 532、唯一论文 436）；未入馆 421 篇摘要级 XR 命中 13 篇，与 11-12 运行已剔 13 篇逐篇 id 一致 → **0 漏网**；无需 backfill |')
P.append('| 数据源 | API 双主机 200（前沿 11-10；11-12 区间 0 篇；WROTE=0）；RSS 7 分类全部 0 条目（lastBuildDate 11-12 05:00 UTC） |')
P.append('| 新入馆论文 | **0 篇**（registry 维持 **%d 条**：S %d / A %d / B %d / C %d） |' % (
    len(reg), GRADES.get('S', 0), GRADES.get('A', 0), GRADES.get('B', 0), GRADES.get('C', 0)))
P.append('| 新原子笔记 | 0 篇（维持 **%d 篇**；daily 目录 %d 个） |' % (NOTES_N, DAILY_N))
P.append('| 数据修补 | 1 处：2611.08578 的 `title` 曾误写为裸 ID，经 API 核验后修正为 `HaNDF: Object-Conditioned Geometric Neural Hand Distance Fields`（备份 `registry.jsonl.bak-20261113`） |')
P.append('| 库内近 30 天 Top10 均分 | **%.3f**（现算，窗口 %s；门③ 为校准关，本日无候选不触发） |' % (GATE3, GATE3_WIN))
P.append('| 交付 | 状态报告 1 + 前沿参考 7 维表 1（19 篇）+ run_log 1 + MOC 总索引维护 + 前端重建与双渠道发布 |')
P.append('')
P.append('**下一批预期**：11-12 公告批次预计延迟至 **11-13 00:00 UTC（08:00 北京时间）** 释放（同 10-29→10-30 先例），晚于本运行时刻 02:30；**下一调度（11-14 周六 02:30）须按标准流水线补处理并显式标注「公告日≠拉取日」**，门③ 务必现算。')
P.append('')
P.append('---')
P.append('')
P.append('## 二、漏网对账（Step 1）')
P.append('')
P.append('对账目的：确认自上一批次公告日（2026-11-11）至今是否有漏跑公告日或漏收 XR 论文。')
P.append('')
P.append('### 2.1 公告日头核验（目标窗口 ≥ 2026-11-12）')
P.append('')
P.append('| 分类 | 最新公告日 | 11-11 组 declared | 11-11 组实采 | 11-12 组 |')
P.append('|---|---|---|---:|---|')
for c, d, n in [('cs.CV', 'Wed, 11 Nov 2026', 149), ('cs.GR', 'Wed, 11 Nov 2026', 6),
                ('cs.HC', 'Wed, 11 Nov 2026', 34), ('cs.MM', 'Wed, 11 Nov 2026', 14),
                ('cs.RO', 'Wed, 11 Nov 2026', 69), ('cs.AI', 'Wed, 11 Nov 2026', 248),
                ('eess.IV', 'Wed, 11 Nov 2026', 12)]:
    P.append('| %s | %s | %d | %d | **无** |' % (c, d, n, n))
P.append('')
P.append('- **无 11-12 公告日组**：`audit_listing_1113.py` 对 NEW_DAY=2026-11-12 采到 declared=None / got=0。')
P.append('- **缓存与故障排除**：① 加随机 `cb` 参数复验 cs.CV → 仍为 11-11 组（149 条），排除页面缓存；② `pastweek` 视图最新日组同为 11-11；③ 跨学科复核 math.AP（51）/ physics.optics（25）/ cs.CL（112）/ q-bio.NC（15）最新日组**全部为 11-11** → 属 arXiv 全局公告跳空，与 10-29（周四批次未释放）同类。')
P.append('- **延迟释放先例**：10-29 跳空后该批次于 10-30（周五）00:00 UTC 释放并被 10-31 运行捕获。据此预判 11-12 批次将于 **11-13 00:00 UTC（08:00 北京时间）** 释放，晚于本运行 02:30。')
P.append('')
P.append('### 2.2 11-11 公告组完整性复核（验证上批处理完整性）')
P.append('')
P.append('- 逐分类 **declared = got**（上表），槽位合计 **532**，全局去重 **436 篇唯一论文**（与 11-12 运行采集数字逐项一致）；')
P.append('- 未入馆 **421 篇** = 436 − 15（11-12 运行主批已入馆；该批 listing 侧无漏网），与 11-12 运行复采集合**逐篇一致**；')
P.append('- 摘要级 XR 过滤（`scripts/filter_missed_1113.py`，50 id/批 + 12s 间隔；**meta fetched 421/421，覆盖率 1.0000**）：命中 **13 篇**，与 11-12 运行显式剔除的 13 篇非 XR **逐篇 id 一致（双向差集 0）**：')
P.append('')
P.append('| ID | 标题 | 11-12 运行裁决（本批复核维持） |')
P.append('|---|---|---|')
for pid, desc in EXCL13:
    P.append('| %s | %s | 非 XR（已显式剔除） |' % (pid, desc))
P.append('')
P.append('- 结论：**0 漏网、无 backfill**；上批 15 篇 XR 主批入馆完整（421 篇未入馆者中无 XR 命中）。')
P.append('')
P.append('---')
P.append('')
P.append('## 三、数据源探测记录（Step 2）')
P.append('')
P.append('| 源 | 状态 | 关键证据 |')
P.append('|---|---|---|')
P.append('| API `export.arxiv.org` / `arxiv.org/api/query` | 200（双主机） | `submittedDate` 前沿 = **2026-11-10**；`[20261112 TO 20261112]` cs.CV **0 篇**；`--since 2026-11-11` → **WROTE=0** |')
P.append('| RSS `rss.arxiv.org`（7 分类） | 200 但全空 | 7 分类各 **0 条 item**，`lastBuildDate` = Thu, 12 Nov 2026 05:00 UTC（同批重建） |')
P.append('| listing `arxiv.org/list/*/recent` | 200 | 7 分类最新日组 11-11；`pastweek` 一致；跨学科四分类最新日组 11-11 |')
P.append('')
P.append('- 判定：**0 篇新候选**，不进入 Steps 3-7（全文抓取 / 评分 / 三关 / Top10）。')
P.append('')
P.append('---')
P.append('')
P.append('## 四、文献库最新前沿参考（11-11 公告批次 · 19 篇 · 非当日新拉取）')
P.append('')
P.append('以下为 11-12 运行处理的 11-11 公告批次（主批 15 篇 + backfill-1112 4 篇），完整 7 维表见 [papers/daily/2026-11-13/7dim-table.md](../papers/daily/2026-11-13/7dim-table.md)：')
P.append('')
P.append('| # | arXiv | 标题 | 赛道 | 总分 | 等级 | 批次 |')
P.append('|---|---|---|---|---|---|---|')
for i, r in enumerate(ref, 1):
    star = ' ⭐' if r.get('in_top10') else ''
    batch_tag = '主批' if r.get('batch') == '2026-11-12' else 'backfill'
    P.append('| %d | %s | %s%s | %s | **%.2f** | %s | %s |' % (
        i, r['id'].split(':')[-1], (r.get('title_zh') or r.get('title', ''))[:40], star,
        r.get('track', ''), r.get('value', 0), r.get('grade', ''), batch_tag))
P.append('')
P.append('---')
P.append('')
P.append('## 五、附录')
P.append('')
P.append('### 5.1 覆盖度三关（本日不触发）')
P.append('')
P.append('- 门① 同质去重 / 门② 赛道覆盖 / 门③ 价值天花板：候选池 0 篇，三关均不触发。')
P.append('- 门③ 参考值现算：库内近 30 天 Top10 均分 **%.3f**（窗口 %s；Top10 = %s）。' % (GATE3, GATE3_WIN, GATE3_TOP))
P.append('')
P.append('### 5.2 证据等级分布')
P.append('')
P.append('- 本日无新抓取。参考表 19 篇：18 篇 **L0/FULL** + 1 篇 **L1/PARTIAL**（2611.13296：arXiv HTML 404、ar5iv 仅摘要页 4,350 字符，11-12 运行人工抽看无正文节后改判，按摘要级评估并显式声明）；无 ABSTRACT_ONLY。')
P.append('')
P.append('### 5.3 失败/降级清单')
P.append('')
P.append('- 无抓取失败（本日不抓取）。数据源：RSS 7 分类空源（与 listing 全无 11-12 日组一致，非故障）；API 双主机 200，仅 `submittedDate` 前沿停在 11-10。')
P.append('- 采集保护：摘要级过滤采用 50 id/批 + 12s 间隔，meta 覆盖率 421/421 = 1.0000，未出现 11-12 记录过的 429 静默丢批。')
P.append('')
P.append('### 5.4 产物清单')
P.append('')
P.append('| 产物 | 路径 |')
P.append('|---|---|')
P.append('| 状态报告 | `reports/XR-Daily-Report-2026-11-13.md` |')
P.append('| 前沿参考 7 维表 | `papers/daily/2026-11-13/7dim-table.md`（19 篇） |')
P.append('| 运行日志 | `papers/daily/2026-11-13/run_log.md` |')
P.append('| 对账数据 | `data/audit_1113_days.json` / `data/audit_1113_alldays.json` / `data/missed_listing_1113.json` / `data/newday_1113.json` / `data/missed_new_1113.json` / `data/missed_xr_abstract_1113.json` |')
P.append('| registry 备份 | `papers/library/registry.jsonl.bak-20261113`（标题修补前） |')
P.append('| MOC 总索引 | `papers/MOC/MOC-总索引.md`（11-13 状态注记 + 速查入口 + 批次索引行 + 页脚刷新） |')
P.append('| 前端 | `web/xr-paper-hub.html`（重建） |')
P.append('')
P.append('### 5.5 发布记录')
P.append('')
P.append('- 渠道① WorkBuddy 托管（workbuddy_sites_deploy）：见收尾汇报（自 10-21 起连续不可用，URL 已 403）。')
P.append('- 渠道② GitHub Pages：见收尾汇报（commit + `push_to_github.py --incremental` + deploy run + Pages 200 核验）。')
P.append('')
P.append('---')
P.append('')
P.append('*报告生成：2026-11-13 02:30 自动化运行（xr-paper-daily-brief skill · 9 步流水线）。*')

with io.open(os.path.join(ROOT, 'reports/XR-Daily-Report-2026-11-13.md'), 'w', encoding='utf-8') as f:
    f.write('\n'.join(P) + '\n')
print('written report, chars:', len('\n'.join(P)))

# ---------- MOC-总索引.md 维护 ----------
moc_path = os.path.join(ROOT, 'papers/MOC/MOC-总索引.md')
moc = io.open(moc_path, encoding='utf-8').read()

note = ('> **状态注记（2026-11-13）**：周五 02:30，**无新增可处理论文**——**arXiv 11-12（周四）公告批次未释放**（工作日公告跳空，继 10-29 之后第 2 次）。'
        'listing 7 分类最新公告日均为 **2026-11-11（周三）**、无 11-12 日组（缓存穿透 `recent?cb=` 与 `pastweek` 复验一致）；跨学科复核 math.AP 51 / physics.optics 25 / cs.CL 112 / q-bio.NC 15 最新日组同为 11-11 → 非本分类故障；'
        'API `submittedDate` 前沿 = **11-10**（`[20261112 TO 20261112]` cs.CV 0 篇、`--since 2026-11-11` WROTE=0）；RSS 7 分类全部 0 条目（lastBuildDate 11-12 05:00 UTC）。'
        '11-11 公告组 show=500 单页全量复采：逐分类 declared=got（CV 149/GR 6/HC 34/MM 14/RO 69/AI 248/IV 12，槽位 532、唯一论文 436），未入馆 **421 篇**摘要级 XR 过滤（421/421 fetched，覆盖率 1.0000）命中 **13 篇**，与 11-12 运行已剔 13 篇**逐篇 id 一致** → **0 漏网、无 backfill**。'
        '未伪造 Top10/评分/S 级；registry 维持 **%d 条**（S%d/A%d/B%d/C%d，另修补 2611.08578 标题字段为 HaNDF 真名，备份 `.bak-20261113`）；门③ 现算参考 **%.3f**（窗口 %s）。'
        '**下一调度（11-14 周六 02:30）预计捕获延迟释放的 11-12 公告批次**（先例：10-29 跳空 → 10-30 00:00 UTC 释放），须按标准流水线补处理并显式标注「公告日≠拉取日」。'
        '详见 [状态报告](../../reports/XR-Daily-Report-2026-11-13.md)。') % (
    len(reg), GRADES.get('S', 0), GRADES.get('A', 0), GRADES.get('B', 0), GRADES.get('C', 0), GATE3, GATE3_WIN)

if '状态注记（2026-11-13）' not in moc:
    anchor = '详见 [运行报告](../../reports/XR-Daily-Report-2026-11-12.md)'
    idx = moc.find(anchor)
    if idx >= 0:
        # 找到该注记行行尾
        eol = moc.find('\n', idx)
        moc = moc[:eol] + '\n' + note + moc[eol:]
        print('MOC: 11-13 状态注记已插入')
    else:
        print('MOC WARN: 11-12 状态注记锚点未找到')

# 速查入口：最新运行状态 → 今日状态报告
old_quick = re.search(r'\| 最新运行状态 \|[^\n]*\n', moc)
if old_quick and 'XR-Daily-Report-2026-11-13' not in old_quick.group(0):
    new_quick = ('| 最新运行状态 | [运行报告 2026-11-13](../../reports/XR-Daily-Report-2026-11-13.md)'
                 '（**状态日 0 新稿**：arXiv 11-12 公告批次未释放，listing/API/RSS + 跨学科四分类五重互证；11-11 组复采 532 槽位/436 唯一、未入馆 421 篇摘要级 13 篇命中与上批已剔完全一致 → 0 漏网）；'
                 '上一内容批次见 [11-12 报告](../../reports/XR-Daily-Report-2026-11-12.md) |\n')
    moc = moc[:old_quick.start()] + new_quick + moc[old_quick.end():]
    print('MOC: 速查入口最新运行状态已更新')

row = ('| 2026-11-13 | — | **0 新稿**（工作日公告跳空：arXiv 11-12 公告批次未释放；listing 七分类最新日组 11-11 + 缓存穿透/pastweek 复验 + 跨学科四分类 11-11 + API 前沿 11-10/区间 0 篇 + RSS 7 分类空源五重互证） | '
       '状态报告日；11-11 公告组 show=500 单页复采 declared=got（532 槽位/436 唯一），未入馆 421 篇摘要级 13 篇命中与 11-12 运行已剔完全一致，0 漏网；另修补 2611.08578 标题字段；门③ 现算 4.437 |')
if '| 2026-11-13 |' not in moc:
    lines = moc.split('\n')
    for i, l in enumerate(lines):
        if l.startswith('| 2026-11-12 |'):
            lines.insert(i + 1, row)
            moc = '\n'.join(lines)
            print('MOC: 批次索引 11-13 行已插入')
            break

footer_new = ('*最后更新：2026-11-13（**状态日 0 新稿**：arXiv 11-12 公告批次未释放（工作日跳空第 2 次，继 10-29）；'
              'listing 七分类最新日组 11-11 + 缓存穿透/pastweek 复验 + 跨学科四分类同 11-11 + API 前沿 11-10/11-12 区间 0 篇 + RSS 7 分类空源五重互证；'
              '11-11 组复采 532 槽位 declared=got / 436 唯一，未入馆 421 篇摘要级 13 篇命中与上批已剔逐篇一致 → 0 漏网无 backfill；'
              '修补 2611.08578 标题字段；registry %d / 笔记 %d / daily %d）。*' % (len(reg), NOTES_N, DAILY_N))
moc = re.sub(r'\*最后更新：[^\n]*\*', footer_new, moc, count=1)

with io.open(moc_path, 'w', encoding='utf-8') as f:
    f.write(moc)
print('MOC-总索引.md updated')
