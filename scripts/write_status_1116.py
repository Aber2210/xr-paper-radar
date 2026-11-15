# -*- coding: utf-8 -*-
"""write_status_1116.py — 2026-11-16 状态日产物（周一 02:30 · 早于周末积压公告时刻，0 新稿）。

产物：
  papers/daily/2026-11-16/7dim-table.md   前沿参考表（28 篇：11-14 主批 20 + backfill-1114 8，非当日新拉取）
  papers/daily/2026-11-16/run_log.md      执行日志
  reports/XR-Daily-Report-2026-11-16.md   状态报告
  papers/MOC/MOC-总索引.md                状态注记 + 速查入口 + 批次索引行 + 页脚刷新
"""
import io, json, os, re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

reg = []
for l in io.open(os.path.join(ROOT, 'papers/library/registry.jsonl'), encoding='utf-8'):
    l = l.strip()
    if l:
        reg.append(json.loads(l))

ref = [r for r in reg if r.get('batch') in ('2026-11-14', 'backfill-1114')]
ref.sort(key=lambda x: (-x.get('value', 0), x['id']))

os.makedirs(os.path.join(ROOT, 'papers/daily/2026-11-16'), exist_ok=True)

GATE3 = 4.403
GATE3_WIN = '2026-10-17~2026-11-16（406 条入窗）'
GATE3_TOP = ('2611.06817 Open-HumanScale 4.57 / 2611.11169 Map2SLAM 4.57 / 2603.01178 riMESA 4.50 / '
             '2610.39399 ACD-GS 4.37 / 2611.09458 跨注入左右一致立体匹配 4.37 / 2611.07902 XM4D 4.36 / '
             '2610.34263 RacerGS 4.35 / 2611.08578 HaNDF 4.34 / 2609.31418 CognitiveReality 4.30 / '
             '2610.37602 RESPLE2 4.30')

GRADES = {}
for r in reg:
    g = r.get('grade', 'C')
    GRADES[g] = GRADES.get(g, 0) + 1
NOTES_N = len([f for f in os.listdir(os.path.join(ROOT, 'papers/notes')) if f.endswith('.md')])
DAILY_N = len([d for d in os.listdir(os.path.join(ROOT, 'papers/daily'))])
MOC_N = len([f for f in os.listdir(os.path.join(ROOT, 'papers/MOC'))
             if f.startswith('MOC-') and f != 'MOC-总索引.md'])

# 11-16 摘要级复核命中 28 篇（581 篇未入馆全量摘要级过滤，覆盖率 1.0000）
# 与 11-15 运行 28 篇逐篇 id 一致（双向差集 0），亦与 11-14 运行显式剔除集合一致
EXCL28 = [
    ('2611.15040', 'Moving Beyond the DRW Model: Learning Quasar Variability（类星体光变生成建模/天体物理）'),
    ('2611.15082', 'Prediction or Persistence? What Future-Prediction Scores Miss（世界模型评分指标研究）'),
    ('2611.15117', 'PolyMorphWBC: Whole-Body Control from End-Effector Trajectories（四足移动操作全身控制）'),
    ('2611.15135', 'ARTS: Open-Source Three-Arm Platform for Autonomy Research（三臂自主研究平台）'),
    ('2611.15216', 'Where is My Mug? Training-Free Personalized Image Segmentation（个性化图像分割）'),
    ('2611.15277', 'DroneDiffusion: Uncertainty-Guided Diffusion Path Planner（无人机扩散路径规划）'),
    ('2611.15280', 'Autonomous Trail Racing with a Bicycle Robot（自行车机器人越野竞速）'),
    ('2611.15579', 'FoveaDet: Software-Hardware Co-Design of Foveated CNN-Transformer（注视点目标检测硬件协同，非近眼显示）'),
    ('2611.15650', 'Single-View RGB-D Force-Deformation Estimation（机器人操作力-形变估计）'),
    ('2611.15659', 'GraSLA: Lightweight Spatial-Language-Action Model（抓取假设几何的空间-语言-动作模型）'),
    ('2611.15764', 'AIFR: Adaptive Identity Feature Recovery（妆容/动漫人像扩散生成）'),
    ('2611.15766', 'Prior-as-Skill: On-Policy Self-Distillation（LLM 自蒸馏）'),
    ('2611.15789', 'VibePrevisBench: Agentic Coding for 4D Scene Generation in Blender（生成工具链基准）'),
    ('2611.15937', 'MOSAIC: Obstacle and Spatial-Aware Framework for Manipulation（杂乱场景操作）'),
    ('2611.16282', 'Robot Navigation and Obstacle Avoidance from External Cameras（外部相机机器人导航）'),
    ('2611.16417', 'VBot Exo2Ego Policy: Exocentric-to-Egocentric Video Generation（数据采集与操作策略）'),
    ('2611.16424', 'PhysCapBench: Cross-Domain Benchmark for Video Captioning（物理视频描述基准）'),
    ('2611.16439', 'HALO: Human-Aligned Data Collection for Mobile Manipulation（全身移动操作数据采集）'),
    ('2611.16452', 'Can an LVLM Perceive Event Boundaries Like a Human?（LVLM 认知评测）'),
    ('2611.16655', 'MuViRL: View-Invariant Visual Speech Representation（视觉语音表征）'),
    ('2611.16728', 'EgoX: Egocentric Cross-Embodiment Manipulation（第一视角跨本体操作策略）'),
    ('2611.16869', 'Raysemble: Metric 3D Bone Reconstruction from a Single X-ray（单 X 光医学骨重建）'),
    ('2611.17060', 'Ropedia Xperience 2: Physical AI Environments（物理 AI 环境数据规模化）'),
    ('2611.17110', 'SALA: Semantically Aligned Latent Actions（具身基础模型潜动作）'),
    ('2611.17163', 'UAV-Flow++: Language-Guided UAV Flight Benchmark（无人机语言引导飞行基准）'),
    ('2611.17235', 'Al-Ghasali: Simulating Islamic Jurisprudential Rulings（法律推理模拟）'),
    ('2611.17238', 'HEIR: Harness Egocentric Intent for Human-Robot Interactions（第一视角意图机器人交互）'),
    ('2611.17284', 'Augmented Hybrid TV Services: Habits and Expectations（电视服务用户调研；augmented 关键词误命中）'),
]

# ---------- 7dim-table.md ----------
L = []
L.append('# 7 维度对比表 · 2026-11-16（文献库最新前沿参考，非当日新拉取）')
L.append('')
L.append('> ⚠️ 说明：本运行日（周一 2026-11-16 02:30）经漏网对账 + 三源探针核验，**无新增可处理论文**——')
L.append('> **周末积压公告时刻为周一 00:00 UTC = 08:00 北京时间，晚于本运行时刻 02:30**，故 11-14（周六）/ 11-15（周日）提交批次尚未公告：')
L.append('> ① listing 7 分类（cs.CV / cs.GR / cs.HC / cs.MM / cs.RO / cs.AI / eess.IV）最新公告日均为 **2026-11-13（周五）**，**无 11-14 / 11-15 / 11-16 公告日组**；缓存穿透复验（`recent?cb=7741`）与 `pastweek` 视图一致，跨学科复核（math.AP / cs.CL）最新日组同为 **Fri, 13 Nov 2026**；')
L.append('> ② API 双主机 200，`submittedDate` 降序前沿 = **2026-11-12**（11-13 公告组来源，已全部入馆）；`submittedDate:[20261114…]` / `[20261115…]` / `[20261116…]` cs.CV 均命中 **0** 篇；`fetch_arxiv.py --since 2026-11-13` → **WROTE=0**；')
L.append('> ③ RSS 7 分类 **全部 0 条目**（`lastBuildDate` = Sun, 15 Nov 2026 05:00 UTC，周末节律空源，HTTP 200 非代理故障）；')
L.append('> ④ 11-13 公告组（上批）完整性复采：逐分类 declared=got（CV 196 / GR 6 / HC 43 / MM 2 / RO 106 / AI 321 / IV 21，槽位 **695**、唯一论文 **601**），未入馆 **581 篇**摘要级 XR 过滤（581/581 fetched，覆盖率 **1.0000**）命中 **28 篇**，与 11-15 / 11-14 运行显式剔除的 28 篇非 XR **逐篇 id 一致（双向差集 0）→ 0 漏网**。')
L.append('> 下表为**文献库最新前沿（11-14 运行处理的 11-13 公告批次：主批 20 篇 + backfill-1114 8 篇）的 7 维参考表**，供查阅，**非「当日新论文」对比表**。')
L.append('')
L.append('> 维度与权重固定：`Value = 0.20·IMP + 0.20·NOV + 0.15·TEC + 0.15·EXP + 0.15·PER + 0.08·TRL + 0.07·REP`；分档：S≥4.2 / A 3.6–4.2 / B 3.0–3.6 / C<3.0')
L.append('')
L.append('> 拉取窗口：无（状态日；最新公告日 2026-11-13，已由 11-14 运行完整处理，本日复核 0 漏网）')
L.append('')
L.append('| # | arXiv | 标题 | 赛道 | IMP | NOV | TEC | EXP | PER | TRL | REP | 总分 | 等级 | 批次 | 证据 | 状态 |')
L.append('|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|')
for i, r in enumerate(ref, 1):
    s = r.get('scores') or {}
    star = ' ⭐' if r.get('in_top10') else ''
    batch_tag = '主批 2026-11-14' if r.get('batch') == '2026-11-14' else 'backfill-1114'
    L.append('| %d | [%s](https://arxiv.org/abs/%s) | %s%s | %s | %s | %s | %s | %s | %s | %s | %s | **%.2f** | %s | %s | %s | %s |' % (
        i, r['id'].split(':')[-1], r['id'].split(':')[-1],
        r.get('title_zh') or r.get('title', ''), star,
        r.get('track', ''),
        s.get('IMP', ''), s.get('NOV', ''), s.get('TEC', ''), s.get('EXP', ''),
        s.get('PER', ''), s.get('TRL', ''), s.get('REP', ''),
        r.get('value', 0), r.get('grade', ''), batch_tag,
        r.get('evidence', ''), r.get('status', 'CURRENT')))
L.append('')
L.append('> 证据列：FULL = 完整正文（L0/L1）；本表 28 篇证据等级以 registry 登记为准（11-14 运行：**28 篇全部 L0/FULL**，43,212–171,293 字符，无 PARTIAL / ABSTRACT_ONLY）。')
L.append('> 门③ 参考：库内近 30 天 Top10 均分 **%.3f**（窗口 %s，现算）；本日 0 候选不触发校准关。' % (GATE3, GATE3_WIN))

with io.open(os.path.join(ROOT, 'papers/daily/2026-11-16/7dim-table.md'), 'w', encoding='utf-8') as f:
    f.write('\n'.join(L) + '\n')
print('written 7dim-table.md:', len(ref), 'ref rows')

# ---------- run_log.md ----------
R = []
R.append('# 运行日志 · 2026-11-16（周一 02:30 · 周末积压未公告状态日：0 新稿）')
R.append('')
R.append('## 1. 漏网对账（Step 1）')
R.append('')
R.append('- listing 7 分类日期头（`scripts/audit_listing_1116.py`，show=500 单页×7 分类，PREV_DAY=2026-11-13 / NEW_DAYS=2026-11-14,2026-11-15,2026-11-16）：')
R.append('  **最新公告日全部为 2026-11-13（周五）**，**无 11-14 / 11-15 / 11-16 公告日组**（`newest=2026-11-13`，NEW_DAYS declared=None / got=0）。')
R.append('- 时序口径：arXiv 周末提交积压于**周一 00:00 UTC = 08:00 北京时间**统一公告；本运行时刻 02:30 **早于该时刻** → 11-14/11-15 提交批次尚不可见，属预期（同 10-26 / 11-02 / 11-09 周一凌晨模式）。')
R.append('- 缓存与故障排除：① cs.CV `recent?cb=7741` 随机参数缓存穿透 → 最新日组仍 `Fri, 13 Nov 2026`（55,112 bytes）；② cs.CV `pastweek` 视图一致；③ 跨学科复核 math.AP（41,537 bytes）/ cs.CL（60,482 bytes）`pastweek` 最新日组同为 `Fri, 13 Nov 2026` → 非本分类/本机故障。')
R.append('- 11-13 公告组完整性复采（验证上批处理完整性）：逐分类 **declared=got**（CV 196 / GR 6 / HC 43 / MM 2 / RO 106 / AI 321 / IV 21，槽位合计 **695**，全局去重 **601 篇唯一论文**），与 11-14 / 11-15 运行采集数字逐项一致；')
R.append('- 未入馆 **581 篇**（601 − 20 篇 11-14 运行已入馆主批），与 `data/missed_prev_1115.json` **逐篇 id 一致（581/581，双向差集 0）**；摘要级 XR 过滤（`scripts/filter_missed_1116.py`，**50 id/批 + 12s 间隔**，meta fetched **581/581**、覆盖率 **1.0000**、缺失 0）命中 **28 篇**，与 11-15 运行命中集合**双向差集 0**，亦与 11-14 运行显式剔除的 28 篇非 XR 一致：')
R.append('')
for pid, desc in EXCL28:
    R.append('  - %s %s' % (pid, desc))
R.append('')
R.append('  → 维持上批裁决（均为非 XR 或泛机器人/生成工具链方向）→ **0 漏网、无 backfill**。')
R.append('- 落盘：`data/audit_1116_days.json` / `data/audit_1116_alldays.json` / `data/missed_prev_1116.json`（581 篇）/ `data/newday_1116.json`（空）/ `data/missed_new_1116.json`（空）/ `data/missed_xr_abstract_1116.json`（28 篇）/ `data/gates_1116.json`。')
R.append('')
R.append('## 2. 数据源探测（Step 2）')
R.append('')
R.append('- API 双主机探针 200（`export.arxiv.org` / `arxiv.org/api/query`）；`submittedDate` 降序前沿 = **2026-11-12**（cs.CV top-8 最新 published 均为 11-12，即 11-13 公告组来源，已全部入馆）；`submittedDate:[20261114…]` / `[20261115…]` / `[20261116…]` cs.CV 均命中 **0** 篇；`fetch_arxiv.py --since 2026-11-13 --max 200` → **WROTE=0**（降序首页即越过下界）。')
R.append('- RSS（`rss.arxiv.org` 7 分类）：**全部 0 条目**，`lastBuildDate` = Sun, 15 Nov 2026 05:00:00–05:00:06 UTC（7 分类同批重建，HTTP 200，非代理故障，属周末节律空源）；`fetch_rss.py` → **WROTE=0**（全量去重 0 → 关键词命中 0）。')
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
R.append('- registry **%d 条**（S%d/A%d/B%d/C%d）：本日无新增入馆、无数据修补（交付前 `title == id` / `len(title)<12` 抽查 0 命中）。' % (
    len(reg), GRADES.get('S', 0), GRADES.get('A', 0), GRADES.get('B', 0), GRADES.get('C', 0)))
R.append('- 原子笔记 **%d 篇**（无新增）；daily 目录 **%d 个**（新增 2026-11-16）。' % (NOTES_N, DAILY_N))
R.append('- 产物：本 run_log + `papers/daily/2026-11-16/7dim-table.md`（28 篇前沿参考）+ `reports/XR-Daily-Report-2026-11-16.md` + MOC 总索引维护。')
R.append('- 前端：BATCH_LABELS 补 2026-11-16 标签 → 重建 hub → DATA 计数核验 → node --check 双 script 块 → CDP 冒烟 → 双渠道发布（详见报告 §5.5）。')
R.append('')
R.append('## 5. 异常与教训')
R.append('')
R.append('- 周一凌晨状态日模式第 **4** 次验证（10-26 / 11-02 / 11-09 + 本日）；周末状态日另有 7 次（10-04 / 10-05 / 10-18 / 10-25 / 11-01 / 11-08 / 11-15）。判据固定为「listing 日期头为唯一决定依据 + 缓存穿透/pastweek + 跨学科分类 + API 区间 + RSS 条数」五重互证。')
R.append('- **RSS 空 ≠ 无公告** 的反向教训仍成立（11-07 反例：RSS 空但 listing 有 11-06 组，真实运行 23 篇）；本日结论由 listing 日期头（7 分类均 11-13、无 11-14/11-15/11-16 日组）决定，RSS 空源仅作辅证。')
R.append('- 摘要级过滤覆盖率 581/581 = 1.0000，未出现 11-12 记录过的 id_list 429 静默丢批（50 id/批 + 12s 间隔生效）。')
R.append('- 门③ 现值 **%.3f**（窗口较上批前移一日：10-16 出窗、10-17 入窗，2610.23772 视频扩散化身 4.57 出窗 → 均分由 4.430 降至 4.403）；下次运行仍须现算，勿沿用。' % GATE3)
R.append('- 渠道①（workbuddy_sites_deploy）自 10-21 起连续不可用且 URL 已 403；若恢复可用须优先补部署（挂账批次 10-21~11-16 共 27 批）。硬件类渲染缺口仍仅 CVQPG + HoOPOE 两篇破冰。')

with io.open(os.path.join(ROOT, 'papers/daily/2026-11-16/run_log.md'), 'w', encoding='utf-8') as f:
    f.write('\n'.join(R) + '\n')
print('written run_log.md')

# ---------- 报告 ----------
P = []
P.append('# XR 每日论文雷达 · 运行报告 · 2026-11-16（周一 02:30）')
P.append('')
P.append('> **诚实口径声明**：本运行日（2026-11-16，周一 02:30）**无新增可处理论文**——**周末提交积压的公告时刻为周一 00:00 UTC（08:00 北京时间），晚于本运行时刻**，故 11-14（周六）/ 11-15（周日）提交批次尚未公告。五重互证：① listing 7 分类最新公告日均为 **2026-11-13（周五）**，无 11-14 / 11-15 / 11-16 日组（各分类 declared=got）；② 缓存穿透复验（`recent?cb=7741`）与 `pastweek` 视图同为 `Fri, 13 Nov 2026`；③ 跨学科复核 math.AP / cs.CL 最新日组同为 11-13 → 非本分类故障；④ API 双主机 200、`submittedDate` 前沿 **11-12**（11-13 公告组来源，已全部入馆）、`[20261114…]` / `[20261115…]` / `[20261116…]` cs.CV 均 0 篇、`--since 2026-11-13` **WROTE=0**；⑤ RSS 7 分类全部 0 条目（`lastBuildDate` Sun, 15 Nov 2026 05:00 UTC）。上一批（11-14 运行）处理的 11-13 公告组经本日全量复采复核：**695 槽位 declared=got、601 篇唯一论文**，未入馆 581 篇摘要级 XR 命中 28 篇，与 11-15 / 11-14 运行已显式剔除的 28 篇**逐篇 id 一致（双向差集 0）** → **0 漏网、无 backfill**。**本报告不含任何「当日新论文」解读，不虚构 Top10/评分/S 级**；第四节为文献库最新前沿参考。')
P.append('')
P.append('---')
P.append('')
P.append('## 一、执行摘要')
P.append('')
P.append('| 项 | 结论 |')
P.append('|---|---|')
P.append('| 运行性质 | **状态报告日**（0 新稿；漏网对账 + 五重源核验 + 采集完整性复核 + 知识库存量维护 + 前端重建与双渠道发布） |')
P.append('| 公告状态 | listing 7 分类最新公告日均为 **2026-11-13（周五）**；**无 11-14 / 11-15 / 11-16 公告日组**；周末积压公告时刻（周一 00:00 UTC = 08:00 北京时间）晚于运行时刻 02:30；跨学科 math.AP / cs.CL 同为 11-13 |')
P.append('| 漏网对账 | 11-13 公告组 show=500 单页全量复采：逐分类 declared=got（CV 196/GR 6/HC 43/MM 2/RO 106/AI 321/IV 21，槽位 695、唯一论文 601）；未入馆 581 篇摘要级 XR 命中 28 篇，与 11-15 / 11-14 运行已剔 28 篇逐篇 id 一致 → **0 漏网**；无需 backfill |')
P.append('| 数据源 | API 双主机 200（前沿 11-12；11-14 / 11-15 / 11-16 区间各 0 篇；WROTE=0）；RSS 7 分类全部 0 条目（lastBuildDate 11-15 05:00 UTC；WROTE=0） |')
P.append('| 新入馆论文 | **0 篇**（registry 维持 **%d 条**：S %d / A %d / B %d / C %d） |' % (
    len(reg), GRADES.get('S', 0), GRADES.get('A', 0), GRADES.get('B', 0), GRADES.get('C', 0)))
P.append('| 新原子笔记 | 0 篇（维持 **%d 篇**；daily 目录 %d 个） |' % (NOTES_N, DAILY_N))
P.append('| 数据修补 | 无（交付前 `title == id` / `len(title)<12` 抽查 0 命中） |')
P.append('| 库内近 30 天 Top10 均分 | **%.3f**（现算，窗口 %s；门③ 为校准关，本日无候选不触发） |' % (GATE3, GATE3_WIN))
P.append('| 交付 | 状态报告 1 + 前沿参考 7 维表 1（28 篇）+ run_log 1 + MOC 总索引维护 + 前端重建与双渠道发布 |')
P.append('')
P.append('**下一批预期**：周一 2026-11-16 00:00 UTC（08:00 北京时间）释放周末（11-14 / 11-15）提交积压；**下一调度（11-17 周二 02:30）应可捕获该批次**，须现算门③、逐篇核验提交日（`published`）并显式标注「公告日≠拉取日」。若届时 listing 仍无 11-16 日组，则按工作日公告跳空流程五重互证后转为状态日并挂账复核。')
P.append('')
P.append('---')
P.append('')
P.append('## 二、漏网对账（Step 1）')
P.append('')
P.append('对账目的：确认自上一批次公告日（2026-11-13）至今是否有漏跑公告日或漏收 XR 论文。')
P.append('')
P.append('### 2.1 公告日头核验（目标窗口 ≥ 2026-11-14）')
P.append('')
P.append('| 分类 | 最新公告日 | 11-13 组 declared | 11-13 组实采 | 11-14 组 | 11-15 组 | 11-16 组 |')
P.append('|---|---|---|---:|---|---|---|')
for c, n in [('cs.CV', 196), ('cs.GR', 6), ('cs.HC', 43), ('cs.MM', 2),
             ('cs.RO', 106), ('cs.AI', 321), ('eess.IV', 21)]:
    P.append('| %s | Fri, 13 Nov 2026 | %d | %d | **无** | **无** | **无** |' % (c, n, n))
P.append('')
P.append('- 槽位合计 **695**，全局去重 **601 篇唯一论文**（跨列表重复 94 条），与 11-14 / 11-15 运行采集数字逐项一致。')
P.append('- **无 11-14 / 11-15 / 11-16 公告日组**：`audit_listing_1116.py` 对 NEW_DAYS 采到 declared=None / got=0。')
P.append('- **时序解释**：arXiv 在周末不公告（`skipDays`），周五 18:30 UTC 之后至周日的全部提交统一于**周一 00:00 UTC（08:00 北京时间）**公告；本运行 02:30 早于该时刻，故最新日组仍为 11-13。')
P.append('- **缓存与故障排除**：① cs.CV `recent?cb=7741`（随机参数）→ 最新日组仍 `Fri, 13 Nov 2026`（55,112 bytes），排除页面缓存；② cs.CV `pastweek`（55,136 bytes）最新日组一致；③ 跨学科 math.AP（41,537 bytes）/ cs.CL（60,482 bytes）`pastweek` 最新日组同为 `Fri, 13 Nov 2026` → **周末不公告属 arXiv 全局节律，非本分类/本机故障**。')
P.append('')
P.append('### 2.2 11-13 公告组完整性复核（验证上批处理完整性）')
P.append('')
P.append('- 逐分类 **declared = got**（上表），未入馆 **581 篇** = 601 − 20（11-14 运行主批已入馆；该批 listing 侧无漏网）；与 `data/missed_prev_1115.json` 集合**逐篇 id 一致（581/581，双向差集 0）**；')
P.append('- 摘要级 XR 过滤（`scripts/filter_missed_1116.py`，50 id/批 + 12s 间隔；**meta fetched 581/581，覆盖率 1.0000**，缺失 0）：命中 **28 篇**；')
P.append('- 与 11-15 运行命中集合（28 篇）**双向差集 0**，亦即 11-14 运行摘要级 43 篇中未进主批的 28 篇显式剔除者。')
P.append('')
P.append('| ID | 标题 | 裁决（本批复核维持） |')
P.append('|---|---|---|')
for pid, desc in EXCL28:
    P.append('| %s | %s | 非 XR（已显式剔除） |' % (pid, desc))
P.append('')
P.append('- 结论：**0 漏网、无 backfill**；上批 20 篇 XR 主批入馆完整（581 篇未入馆者中无 XR 命中）。')
P.append('')
P.append('---')
P.append('')
P.append('## 三、数据源探测记录（Step 2）')
P.append('')
P.append('| 源 | 状态 | 关键证据 |')
P.append('|---|---|---|')
P.append('| API `export.arxiv.org` / `arxiv.org/api/query` | 200（双主机） | `submittedDate` 前沿 = **2026-11-12**（cs.CV top-8 一致）；`[20261114…]` / `[20261115…]` / `[20261116…]` cs.CV **各 0 篇**；`--since 2026-11-13` → **WROTE=0** |')
P.append('| RSS `rss.arxiv.org`（7 分类） | 200 但全空 | 7 分类各 **0 条 item**，`lastBuildDate` = Sun, 15 Nov 2026 05:00 UTC（同批重建，周末节律空源）；`fetch_rss.py` **WROTE=0** |')
P.append('| listing `arxiv.org/list/*/recent` | 200 | 7 分类最新日组 11-13；`recent?cb=7741` 与 `pastweek` 一致；跨学科 math.AP / cs.CL 最新日组 11-13 |')
P.append('')
P.append('- 判定：**0 篇新候选**，不进入 Steps 3-7（全文抓取 / 评分 / 三关 / Top10）。')
P.append('')
P.append('---')
P.append('')
P.append('## 四、文献库最新前沿参考（11-13 公告批次 · 28 篇 · 非当日新拉取）')
P.append('')
P.append('以下为 11-14 运行处理的 11-13 公告批次（主批 20 篇 + backfill-1114 8 篇），完整 7 维表见 [papers/daily/2026-11-16/7dim-table.md](../papers/daily/2026-11-16/7dim-table.md)：')
P.append('')
P.append('| # | arXiv | 标题 | 赛道 | 总分 | 等级 | 批次 |')
P.append('|---|---|---|---|---|---|---|')
for i, r in enumerate(ref, 1):
    star = ' ⭐' if r.get('in_top10') else ''
    batch_tag = '主批' if r.get('batch') == '2026-11-14' else 'backfill'
    P.append('| %d | %s | %s%s | %s | **%.2f** | %s | %s |' % (
        i, r['id'].split(':')[-1], (r.get('title_zh') or r.get('title', ''))[:42], star,
        r.get('track', ''), r.get('value', 0), r.get('grade', ''), batch_tag))
P.append('')
P.append('> 说明：backfill-1114 中 riMESA（2603.01178）实测 4.50 达 S 线，但按既有口径（backfill 不参与重磅日判定）记 **A**，与 11-14 运行报告一致。')
P.append('')
P.append('---')
P.append('')
P.append('## 五、附录')
P.append('')
P.append('### 5.1 覆盖度三关（本日不触发）')
P.append('')
P.append('- 门① 同质去重 / 门② 赛道覆盖 / 门③ 价值天花板：候选池 0 篇，三关均不触发。')
P.append('- 门③ 参考值现算：库内近 30 天 Top10 均分 **%.3f**（窗口 %s；Top10 = %s）。' % (GATE3, GATE3_WIN, GATE3_TOP))
P.append('- 口径变化说明：窗口前移一日（10-16 出窗、10-17 入窗），2610.23772「视频扩散化身」4.57 出窗 → 均分由上批 4.430 降至 **4.403**；下次运行须再算。')
P.append('')
P.append('### 5.2 证据等级分布')
P.append('')
P.append('- 本日无新抓取。参考表 28 篇：**全部 L0/FULL**（11-14 运行 43,212–171,293 字符，无 PARTIAL / ABSTRACT_ONLY / L5）。')
P.append('')
P.append('### 5.3 失败/降级清单')
P.append('')
P.append('- 无抓取失败（本日不抓取）。数据源：RSS 7 分类空源（周末节律，与 listing 全无 11-14 / 11-15 / 11-16 日组一致，非故障）；API 双主机 200，仅 `submittedDate` 前沿停在 11-12（11-13 公告组来源，已全部入馆）。')
P.append('- 采集保护：摘要级过滤 50 id/批 + 12s 间隔，meta 覆盖率 581/581 = 1.0000，未出现 11-12 记录过的 429 静默丢批。')
P.append('')
P.append('### 5.4 产物清单')
P.append('')
P.append('| 产物 | 路径 |')
P.append('|---|---|')
P.append('| 状态报告 | `reports/XR-Daily-Report-2026-11-16.md` |')
P.append('| 前沿参考 7 维表 | `papers/daily/2026-11-16/7dim-table.md`（28 篇） |')
P.append('| 运行日志 | `papers/daily/2026-11-16/run_log.md` |')
P.append('| 对账数据 | `data/audit_1116_days.json` / `data/audit_1116_alldays.json` / `data/missed_prev_1116.json` / `data/newday_1116.json` / `data/missed_new_1116.json` / `data/missed_xr_abstract_1116.json` / `data/gates_1116.json` |')
P.append('| MOC 总索引 | `papers/MOC/MOC-总索引.md`（11-16 状态注记 + 速查入口 + 批次索引行 + 页脚刷新） |')
P.append('| 前端 | `web/xr-paper-hub.html`（重建） |')
P.append('')
P.append('### 5.5 发布记录')
P.append('')
P.append('- 渠道① WorkBuddy 托管（workbuddy_sites_deploy）：见收尾汇报（自 10-21 起连续不可用，URL 已 403）。')
P.append('- 渠道② GitHub Pages：见收尾汇报（commit + `push_to_github.py --incremental` + deploy run + Pages 200 核验）。')
P.append('')
P.append('---')
P.append('')
P.append('*报告生成：2026-11-16 02:30 自动化运行（xr-paper-daily-brief skill · 9 步流水线）。*')

with io.open(os.path.join(ROOT, 'reports/XR-Daily-Report-2026-11-16.md'), 'w', encoding='utf-8') as f:
    f.write('\n'.join(P) + '\n')
print('written report, chars:', len('\n'.join(P)))

# ---------- MOC-总索引.md 维护 ----------
moc_path = os.path.join(ROOT, 'papers/MOC/MOC-总索引.md')
moc = io.open(moc_path, encoding='utf-8').read()

note = ('> **状态注记（2026-11-16）**：周一 02:30，**无新增可处理论文**（周末积压未公告状态日）。'
        '**时序口径**：arXiv 周末提交积压于**周一 00:00 UTC = 08:00 北京时间**统一公告，晚于本运行时刻 02:30，故 11-14（周六）/ 11-15（周日）提交批次尚不可见（同 10-26 / 11-02 / 11-09 周一凌晨模式）。'
        'listing 7 分类最新公告日均为 **2026-11-13（周五）**、**无 11-14 / 11-15 / 11-16 公告日组**；缓存穿透 `recent?cb=7741` 与 `pastweek` 复验一致，跨学科复核 math.AP / cs.CL 最新日组同为 `Fri, 13 Nov 2026` → 非本分类故障；'
        'API 双主机 200、`submittedDate` 前沿 = **11-12**（11-13 公告组来源，已全部入馆），`[20261114…]` / `[20261115…]` / `[20261116…]` cs.CV 均 **0** 篇、`--since 2026-11-13` **WROTE=0**；RSS 7 分类全部 **0 条目**（lastBuildDate Sun, 15 Nov 2026 05:00 UTC，周末节律空源，`fetch_rss.py` WROTE=0）。'
        '11-13 公告组 show=500 单页全量复采：逐分类 declared=got（CV 196/GR 6/HC 43/MM 2/RO 106/AI 321/IV 21，槽位 **695**、唯一论文 **601**），未入馆 **581 篇**（与上批集合 581/581 逐篇一致）摘要级 XR 过滤（581/581 fetched，覆盖率 1.0000）命中 **28 篇**，与 11-15 / 11-14 运行已剔 28 篇**逐篇 id 一致（双向差集 0）** → **0 漏网、无 backfill**。'
        '未伪造 Top10/评分/S 级；registry 维持 **%d 条**（S%d/A%d/B%d/C%d），无数据修补（title 抽查 0 命中）；门③ 现算参考 **%.3f**（窗口 %s；窗口前移致 2610.23772 4.57 出窗，较上批 4.430 降）。'
        '**下一调度（11-17 周二 02:30）应捕获周末 11-14/11-15 提交批次**，须标注「公告日≠拉取日」并现算门③。'
        '详见 [状态报告](../../reports/XR-Daily-Report-2026-11-16.md)。') % (
    len(reg), GRADES.get('S', 0), GRADES.get('A', 0), GRADES.get('B', 0), GRADES.get('C', 0), GATE3, GATE3_WIN)

if '状态注记（2026-11-16）' not in moc:
    anchor = '详见 [状态报告](../../reports/XR-Daily-Report-2026-11-15.md)。'
    idx = moc.find(anchor)
    if idx >= 0:
        eol = moc.find('\n', idx)
        moc = moc[:eol] + '\n' + note + moc[eol:]
        print('MOC: 11-16 状态注记已插入')
    else:
        print('MOC WARN: 11-15 状态报告锚点未找到')

old_quick = re.search(r'\| 最新运行状态 \|[^\n]*\n', moc)
if old_quick and 'XR-Daily-Report-2026-11-16' not in old_quick.group(0):
    new_quick = ('| 最新运行状态 | [运行报告 2026-11-16](../../reports/XR-Daily-Report-2026-11-16.md)'
                 '（**周末积压未公告状态日 0 新稿**：周一 02:30 早于积压公告时刻（周一 00:00 UTC = 08:00 北京时间）；listing 七分类最新日组 11-13，无 11-14/11-15/11-16 日组；缓存穿透 `recent?cb=` 与 pastweek 复验一致；跨学科 math.AP/cs.CL 同为 11-13；API 前沿 11-12 且三日区间各 0 篇、WROTE=0；RSS 7 分类空源 → 五重互证；'
                 '11-13 组复采 695 槽位/601 唯一 declared=got，未入馆 581 篇（与上批逐篇一致）摘要级 28 篇命中与上批已剔逐篇一致 → 0 漏网）；'
                 '上一内容批次见 [11-14 报告](../../reports/XR-Daily-Report-2026-11-14.md) |\n')
    moc = moc[:old_quick.start()] + new_quick + moc[old_quick.end():]
    print('MOC: 速查入口最新运行状态已更新')

row = ('| 2026-11-16 | — | **0 新稿**（周末积压未公告状态日：周一 02:30 早于积压公告时刻 08:00 北京时间；listing 七分类最新日组 11-13，无 11-14/11-15/11-16 组；缓存穿透 `recent?cb=` + pastweek 复验 + 跨学科 math.AP/cs.CL 同 11-13 + API 前沿 11-12/三日区间 0 篇/WROTE=0 + RSS 7 分类空源五重互证） | '
       '状态报告日；11-13 公告组 show=500 单页复采 declared=got（695 槽位/601 唯一），未入馆 581 篇（与上批逐篇一致）摘要级 28 篇命中与 11-15/11-14 运行完全一致，0 漏网；无数据修补；门③ 现算 4.403 |')
if '| 2026-11-16 |' not in moc:
    lines = moc.split('\n')
    for i, l in enumerate(lines):
        if l.startswith('| 2026-11-15 |'):
            lines.insert(i + 1, row)
            moc = '\n'.join(lines)
            print('MOC: 批次索引 11-16 行已插入')
            break

footer_new = ('*最后更新：2026-11-16（**周末积压未公告状态日 0 新稿**：周一 02:30 早于积压公告时刻（周一 00:00 UTC = 08:00 北京时间）；'
              'listing 七分类最新日组 11-13、无 11-14/11-15/11-16 组，缓存穿透 `recent?cb=` 与 pastweek 复验一致，跨学科 math.AP/cs.CL 同为 11-13；'
              'API 双主机 200、前沿 11-12 且三日区间各 0 篇、WROTE=0；RSS 7 分类空源 → 五重互证；'
              '11-13 组复采 695 槽位 declared=got / 601 唯一，未入馆 581 篇摘要级 28 篇命中与上批逐篇一致 → 0 漏网无 backfill；门③ 现算 4.403）。* · 库内 **%d 篇** · 原子笔记 **%d 篇** · MOC %d 份' % (
                  len(reg), NOTES_N, MOC_N))
moc = re.sub(r'\*最后更新：[^\n]*\n', footer_new + '\n', moc, count=1)

with io.open(moc_path, 'w', encoding='utf-8') as f:
    f.write(moc)
print('MOC-总索引.md updated')
