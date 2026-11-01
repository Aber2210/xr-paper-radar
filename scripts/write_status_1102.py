# -*- coding: utf-8 -*-
"""write_status_1102.py — 生成 2026-11-02 状态日产物（周一 02:30，周末积压公告未到时刻，同 10-26 模式）。

产物：
  papers/daily/2026-11-02/7dim-table.md   前沿参考表（24 篇，非当日新拉取）
  papers/daily/2026-11-02/run_log.md      执行日志
  reports/XR-Daily-Report-2026-11-02.md   状态报告
  papers/MOC/MOC-总索引.md                状态注记 + 批次索引行 + 页脚刷新
"""
import json, os, io

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

reg = []
for l in io.open(os.path.join(ROOT, 'papers/library/registry.jsonl'), encoding='utf-8'):
    l = l.strip()
    if l:
        reg.append(json.loads(l))

# 前沿参考 = 10-31 运行批次（10-30 公告批次：主批 18 + backfill-1031 6 篇），按 value 降序
ref = [r for r in reg if r.get('batch') in ('2026-10-31', 'backfill-1031')]
ref.sort(key=lambda x: (-x.get('value', 0), x['id']))

os.makedirs(os.path.join(ROOT, 'papers/daily/2026-11-02'), exist_ok=True)

GATE3 = 4.429
GATE3_WIN = '2026-10-03~2026-11-02（393 条入窗）'
GRADES = {}
for r in reg:
    GRADES[r.get('grade', 'C')] = GRADES.get(r.get('grade', 'C'), 0) + 1
NOTES_N = len([f for f in os.listdir(os.path.join(ROOT, 'papers/notes')) if f.endswith('.md')])

# ---------- 7dim-table.md ----------
L = []
L.append('# 7 维度对比表 · 2026-11-02（文献库最新前沿参考，非当日新拉取）')
L.append('')
L.append('> ⚠️ 说明：本运行日（周一 2026-11-02 02:30）经漏网对账 + 三源探针核验，**无新增可处理论文**：')
L.append('> ① listing 7 分类最新公告日均为 **2026-10-30（周五）**（10-31 周六、11-01 周日无公告日段，符合 arXiv skipDays 节律；周末积压公告时刻 = 周一 00:00 UTC = 当日 08:00 北京时间，**晚于本运行时刻 02:30**，同 10-26 模式）；')
L.append('> ② 10-30 公告组经 show=500 单页全量复采 **842 个分类槽位 / 728 篇唯一论文**（逐分类 declared=got：CV 233/GR 14/HC 51/MM 8/RO 129/AI 392/IV 15），未入馆 **710 篇**与 11-01 运行复采集合一致；摘要级 XR 过滤命中 **13 篇**，与 10-31 运行显式剔除的 13 篇非 XR 逐篇一致 → **0 漏网**；')
L.append('> ③ API `submittedDate` 降序前沿 = **2026-10-29**（= 10-30 公告组来源，已全部入馆；双主机 200）；')
L.append('> ④ RSS 7 分类 **全部 0 条目**（lastBuildDate 11-01 04:00 UTC，周末节律空源；`fetch_rss.py` WROTE=0）。')
L.append('> 下表为**文献库最新前沿（10-31 运行处理的 10-30 公告批次：主批 18 篇 + backfill-1031 6 篇）的 7 维参考表**，供查阅，**非「当日新论文」对比表**。')
L.append('')
L.append('> 维度与权重固定：`Value = 0.20·IMP + 0.20·NOV + 0.15·TEC + 0.15·EXP + 0.15·PER + 0.08·TRL + 0.07·REP`；分档：S≥4.2 / A 3.6–4.2 / B 3.0–3.6 / C<3.0')
L.append('')
L.append('> 拉取窗口：无（状态日；最新公告日 2026-10-30，已由 10-31 运行完整处理，11-01 运行复核 0 漏网）')
L.append('')
L.append('| # | arXiv | 标题 | 赛道 | IMP | NOV | TEC | EXP | PER | TRL | REP | 总分 | 等级 | 批次 | 证据 | 状态 |')
L.append('|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|')
for i, r in enumerate(ref, 1):
    s = r.get('scores') or {}
    star = ' ⭐' if r.get('in_top10') else ''
    batch = '主批 2026-10-31' if r.get('batch') == '2026-10-31' else 'backfill-1031'
    L.append('| %d | [%s](https://arxiv.org/abs/%s) | %s%s | %s | %s | %s | %s | %s | %s | %s | %s | **%.2f** | %s | %s | %s | %s |' % (
        i, r['id'].split(':')[-1], r['id'].split(':')[-1],
        r.get('title_zh') or r.get('title', ''), star,
        r.get('track', ''),
        s.get('IMP', ''), s.get('NOV', ''), s.get('TEC', ''), s.get('EXP', ''),
        s.get('PER', ''), s.get('TRL', ''), s.get('REP', ''),
        r.get('value', 0), r.get('grade', ''), batch,
        r.get('evidence', ''), r.get('status', 'CURRENT')))
L.append('')
L.append('> 证据列：FULL = 完整正文（L0/L1）；本表 24 篇证据等级均以 registry 登记为准（10-31 运行：24 篇全 L0/FULL）。')
L.append('> 门③ 参考：库内近 30 天 Top10 均分 **%.3f**（窗口 %s，现算）；本日 0 候选不触发校准关。' % (GATE3, GATE3_WIN))

with io.open(os.path.join(ROOT, 'papers/daily/2026-11-02/7dim-table.md'), 'w', encoding='utf-8') as f:
    f.write('\n'.join(L) + '\n')
print('written 7dim-table.md:', len(ref), 'ref rows')

# ---------- run_log.md ----------
R = []
R.append('# 运行日志 · 2026-11-02（周一 02:30 · 状态日：周末积压公告未到时刻）')
R.append('')
R.append('## 1. 漏网对账（Step 1）')
R.append('')
R.append('- listing 7 分类日期头（`scripts/audit_listing_1102_fast.py`，show=500 单页）：')
R.append('  **最新公告日全部为 2026-10-30（周五）**（cs.CV / cs.GR / cs.HC / cs.MM / cs.RO / cs.AI / eess.IV 七分类一致）。10-31（周六）/11-01（周日）无公告日段（skipDays 节律）；**周末积压公告时刻 = 周一 00:00 UTC = 当日 08:00 北京时间，晚于本运行时刻 02:30** → 本运行尚不可见周末提交批次（将由 11-03 调度处理），同 10-26 模式。**无漏跑公告日**。')
R.append('- 10-30 公告组完整性复采（验证上两批处理完整性）：逐分类 declared=got 全对齐（CV 233 / GR 14 / HC 51 / MM 8 / RO 129 / AI 392 / IV 15，槽位合计 842，全局去重 728 篇唯一论文）；未入馆 **710 篇**，与 11-01 运行 show=500 重采集合一致。')
R.append('- 摘要级 XR 过滤（`scripts/filter_missed_xr_abstract.py`，meta fetched 710/710）：命中 **13 篇**，与 10-31 运行显式剔除的 13 篇非 XR **逐篇一致**（野火数据集 2610.38086 / SKiD-SLAM 2610.38141 / SpaceAct 2610.38405 / 机器人抓取 2610.38443 / 动态接抛 2610.39044 / 连续体机器人 2610.39055 / EgoContact 2610.39167 / 自回归图像生成 2610.39293 / UMI-Live 2610.39385 / 手机室内定位 2610.39691 / 穿刺规划 2610.39879 / 月面遥操作 2610.39998 / 空间状态探测 2610.40636）→ **0 漏网、无 backfill**。')
R.append('- 落盘：`data/audit_1102_days.json` / `data/audit_1102_alldays.json` / `data/missed_listing_1102.json`（710 篇）/ `data/missed_listing_1102_fmt.json` / `data/missed_xr_abstract_1102.json`（13 篇）/ `data/audit_1102_newday.json`（>10-30 日组：无）/ `data/raw/2026-11-02.jsonl`（RSS 0 条）。')
R.append('')
R.append('## 2. 数据源探测（Step 2）')
R.append('')
R.append('- API 双主机（export.arxiv.org / arxiv.org）探针 200；`submittedDate` 降序前沿 = **2026-10-29**（cs.CV 抽查 5 条一致；10-29 提交 = 10-30 公告组来源，已全部入馆）。')
R.append('- RSS（`scripts/fetch_rss.py`，7 分类）：**全部 0 条目**（lastBuildDate 11-01 04:00 UTC；周末节律空源）→ KW 命中 0 条，WROTE=0。')
R.append('- 判定：**0 篇新候选**，不进入 Steps 3-7。')
R.append('')
R.append('## 3. 甄别 / 全文 / 评分 / Top10（Steps 3-7）')
R.append('')
R.append('- 候选池 0 篇 → 不触发全文抓取、7 维评分、覆盖度三关与 Top10 选拔。')
R.append('- **未伪造 Top10 / 评分 / S 级**（诚实口径硬约束）。')
R.append('- 门③ 现算参考：库内近 30 天 Top10 均分 **%.3f**（窗口 %s）。' % (GATE3, GATE3_WIN))
R.append('')
R.append('## 4. 产物与发布（Steps 8-9）')
R.append('')
R.append('- registry **无变更**（%d 条：S%d/A%d/B%d/C%d；本次未修改故无备份需要）；原子笔记 %d 篇无新增。' % (len(reg), GRADES.get('S',0), GRADES.get('A',0), GRADES.get('B',0), GRADES.get('C',0), NOTES_N))
R.append('- 产物：本 run_log + `papers/daily/2026-11-02/7dim-table.md`（24 篇前沿参考）+ `reports/XR-Daily-Report-2026-11-02.md` + MOC 总索引维护。')
R.append('- 前端：BATCH_LABELS 补 11-02 标签 → 重建 hub → DATA 计数核验 → CDP 冒烟 → 双渠道发布（详见报告 §5.5）。')
R.append('')
R.append('## 5. 异常与教训')
R.append('')
R.append('- **audit 脚本效率改进**：11-01 发现 show=250 分页跨组丢失缺陷后，本日对账改用 `audit_listing_1102_fast.py`（show=500 单页×7 分类）——10-30 组各分类条目数均 <500，单页即完整包含目标组且必含最新日期头，同时完成「最新公告日判定 + 目标组全量复采」，全程约 1 分钟（原全量翻页方案需 20 分钟以上，已中止）。')
R.append('- 周一凌晨状态日模式第 2 次验证（同 10-26）：周末积压公告时刻（周一 00:00 UTC = 08:00 北京时间）晚于 02:30 运行时刻，listing 最新公告日仍为上周五。')
R.append('- 下次运行（11-03 周二 02:30）：处理 **11-02 周一公告批次**（覆盖周末 10-31/11-01 提交积压），按标准流水线跑；门③ 务必现算（勿沿用 %.3f）。' % GATE3)
R.append('- 渠道①（workbuddy_sites_deploy）自 10-21 起连续不可用，若本会话恢复可用须优先补部署（挂账批次 10-21~11-02 共 13 批）；硬件类渲染缺口仍仅 CVQPG + HoOPOE 两篇破冰，继续补波导/可变焦/Maxwellian/光场。')

with io.open(os.path.join(ROOT, 'papers/daily/2026-11-02/run_log.md'), 'w', encoding='utf-8') as f:
    f.write('\n'.join(R) + '\n')
print('written run_log.md')

# ---------- 报告 ----------
P = []
P.append('# XR 每日论文雷达 · 运行报告 · 2026-11-02（周一 02:30）')
P.append('')
P.append('> **诚实口径声明**：本运行日（2026-11-02，周一 02:30）**无新增可处理论文**。经三源交叉验证：listing 7 分类最新公告日均为 **2026-10-30（周五）**（10-31/11-01 周末无公告日段，符合 arXiv skipDays 节律；周末积压公告时刻为周一 00:00 UTC = 当日 08:00 北京时间，**晚于本运行时刻**，同 10-26 模式）；API `submittedDate` 前沿停滞 2026-10-29（10-30 公告组来源，已全部入馆）；RSS 7 分类全部 0 条目（lastBuildDate 11-01 04:00 UTC）。上一批（10-31 运行）处理的 10-30 公告批次经本日 show=500 单页全量复采复核：842 槽位 declared=got、728 篇唯一论文、未入馆 710 篇与 11-01 运行集合一致，摘要级 XR 过滤 13 篇命中均为 10-31 运行已显式剔除的非 XR 稿 → **0 漏网、无 backfill**。**本报告不包含任何「当日新论文」解读、不虚构 Top10/评分/S 级**；文末附表为文献库最新前沿参考。')
P.append('')
P.append('---')
P.append('')
P.append('## 一、执行摘要')
P.append('')
P.append('| 项 | 结论 |')
P.append('|---|---|')
P.append('| 运行性质 | **状态报告日**（周一凌晨，周末积压公告未到时刻；漏网对账 + 三源探针 + 采集完整性复核 + 知识库存量维护 + 前端重建与双渠道发布） |')
P.append('| 公告状态 | listing 7 分类最新公告日均为 **2026-10-30**；10-31/11-01 周末无公告日段（skipDays 节律）；周末积压公告时刻 08:00（北京时间）晚于 02:30 运行时刻 |')
P.append('| 漏网对账 | 10-30 公告组 show=500 单页全量复采：逐分类 declared=got（CV 233/GR 14/HC 51/MM 8/RO 129/AI 392/IV 15，槽位 842、唯一论文 728）；未入馆 710 篇摘要级 XR 命中 13 篇，均为 10-31 运行已剔非 XR → **0 漏网**；无漏跑公告日，无需 backfill |')
P.append('| 数据源 | API 双主机 200（submittedDate 前沿 10-29，已全部入馆）；RSS 7 分类全部 0 条目（周末节律空源，WROTE=0） |')
P.append('| 新入馆论文 | **0 篇**（registry 维持 **%d 条**：S %d / A %d / B %d / C %d） |' % (len(reg), GRADES.get('S',0), GRADES.get('A',0), GRADES.get('B',0), GRADES.get('C',0)))
P.append('| 新原子笔记 | 0 篇（维持 **%d 篇**） |' % NOTES_N)
P.append('| 库内近 30 天 Top10 均分 | **%.3f**（现算，窗口 %s；门③ 为校准关，本日无候选不触发） |' % (GATE3, GATE3_WIN))
P.append('| 交付 | 状态报告 1 + 前沿参考 7 维表 1（24 篇）+ run_log 1 + MOC 总索引维护 + 前端重建与双渠道发布 |')
P.append('')
P.append('**下一批预期**：11-03（周二）02:30 运行处理 **11-02 周一公告批次**（覆盖周末 10-31/11-01 提交积压，周一 00:00 UTC = 08:00 北京时间已释放），按标准流水线跑；门③ 务必现算（勿沿用 %.3f）。' % GATE3)
P.append('')
P.append('---')
P.append('')
P.append('## 二、漏网对账（Step 1）')
P.append('')
P.append('对账目的：确认自上一批次公告日（2026-10-30）至今是否有漏跑公告日或漏收 XR 论文。')
P.append('')
P.append('### 2.1 公告日头核验（目标窗口 ≥ 2026-10-31）')
P.append('')
P.append('| 分类 | 最新公告日 | 10-30 组 declared | 10-30 组实采 |')
P.append('|---|---|---:|---:|')
P.append('| cs.CV | Fri, 30 Oct 2026 | 233 | 233 |')
P.append('| cs.GR | Fri, 30 Oct 2026 | 14 | 14 |')
P.append('| cs.HC | Fri, 30 Oct 2026 | 51 | 51 |')
P.append('| cs.MM | Fri, 30 Oct 2026 | 8 | 8 |')
P.append('| cs.RO | Fri, 30 Oct 2026 | 129 | 129 |')
P.append('| cs.AI | Fri, 30 Oct 2026 | 392 | 392 |')
P.append('| eess.IV | Fri, 30 Oct 2026 | 15 | 15 |')
P.append('')
P.append('- **无 10-31/11-01/11-02 公告日组**：七分类 recent 视图一致；周末无公告符合 arXiv RSS `<skipDays>` 节律；周一积压公告时刻（08:00 北京时间）尚未到达。')
P.append('- **三源互证**：① listing 七分类最新日组全部为 Fri, 30 Oct 2026；② API `submittedDate` 降序前沿 = 2026-10-29（即 10-30 公告组来源）；③ RSS 7 分类 0 条目（lastBuildDate 11-01 04:00 UTC）。')
P.append('')
P.append('### 2.2 10-30 公告组完整性复核（验证上两批处理完整性）')
P.append('')
P.append('本日采用高效复采方案（`scripts/audit_listing_1102_fast.py`，show=500 单页×7 分类）：10-30 组各分类条目数均 <500，单页即完整包含目标组，且必含最新公告日期头。结果：')
P.append('')
P.append('- 逐分类 **declared = got**（上表），槽位合计 842，全局去重后 **728 篇唯一论文**，与 11-01 运行 show=500 全量重采数字逐项一致；')
P.append('- 未入馆 **710 篇**（728 − 18 篇已入馆主批；backfill-1031 6 篇为旧稿再公告、不在 listing 日组），与 11-01 运行复采集合（710/710）一致；')
P.append('- 摘要级 XR 过滤（`filter_missed_xr_abstract.py`，710/710 fetched）：命中 **13 篇**，与 10-31 运行显式剔除的 13 篇非 XR **逐篇一致**：')
P.append('')
P.append('| ID | 标题 | 10-31 运行裁决 |')
P.append('|---|---|---|')
P.append('| 2610.38086 | From Next Day Wildfire to Next Days Wildfire（多大洲野火数据集） | 非 XR（野火数据集） |')
P.append('| 2610.38141 | SKiD-SLAM（行星任务资源感知分布式多机器人 LiDAR SLAM） | 非 XR（机器人 SLAM） |')
P.append('| 2610.38405 | SpaceAct（闭环动作空间推理基准） | 非 XR（机器人空间推理） |')
P.append('| 2610.38443 | Skeleton-Guided Geometry-Aware Auto-Labeling for Robotic Grasping | 非 XR（机器人抓取） |')
P.append('| 2610.39044 | Catch It All!（灵巧手动态接抛） | 非 XR（机器人操作） |')
P.append('| 2610.39055 | Controlling Continuum Robot Shape in Enclosed Space | 非 XR（连续体机器人） |')
P.append('| 2610.39167 | EgoContact（第一视角物理智能评估） | 非 XR（机器人评估） |')
P.append('| 2610.39293 | Unlocking Any-Order Generation in Pretrained Autoregressive Image Models | 非 XR（自回归图像生成） |')
P.append('| 2610.39385 | UMI-Live（野外双臂机器人数据采集） | 非 XR（机器人数据采集） |')
P.append('| 2610.39691 | Smartphone Indoor Localization（手机室内定位） | 非 XR（手机传感定位） |')
P.append('| 2610.39879 | Compressed Orientation Reachability Maps（机器人穿刺规划） | 非 XR（机器人规划） |')
P.append('| 2610.39998 | Gaze-Assisted Supervisory Control for Lunar Robotic Arm Teleoperation | 非 XR（月面遥操作） |')
P.append('| 2610.40636 | Probing Spatial State Representations in Visual Foundation Models | 非 XR（视觉基础模型空间状态探测） |')
P.append('')
P.append('- 结论：**0 漏网、无 backfill**。')
P.append('')
P.append('---')
P.append('')
P.append('## 三、数据源探测记录（Step 2）')
P.append('')
P.append('- API 双主机（export.arxiv.org / arxiv.org）探针 200；`submittedDate` 降序前沿 = **2026-10-29**（cs.CV top-5 published 全部 10-29；= 10-30 公告组来源，已全部入馆）。')
P.append('- RSS（`scripts/fetch_rss.py`，7 分类）：**全部 0 条目**（lastBuildDate 11-01 04:00 UTC，周末节律空源）→ KW 命中 **0 条**，WROTE=0，落盘 `data/raw/2026-11-02.jsonl`。')
P.append('- 判定：**0 篇新候选**，不进入 Steps 3-7。')
P.append('')
P.append('---')
P.append('')
P.append('## 四、文献库最新前沿参考（10-30 公告批次 · 24 篇 · 非当日新拉取）')
P.append('')
P.append('以下为 10-31 运行处理的 10-30 公告批次 7 维参考表（主批 18 篇 + backfill-1031 6 篇），完整版见 [papers/daily/2026-11-02/7dim-table.md](../daily/2026-11-02/7dim-table.md)：')
P.append('')
P.append('| # | arXiv | 标题 | 赛道 | 总分 | 等级 | 批次 |')
P.append('|---|---|---|---|---|---|---|')
for i, r in enumerate(ref, 1):
    star = ' ⭐' if r.get('in_top10') else ''
    batch = '主批 10-31' if r.get('batch') == '2026-10-31' else 'backfill-1031'
    P.append('| %d | %s | %s%s | %s | **%.2f** | %s | %s |' % (
        i, r['id'].split(':')[-1], (r.get('title_zh') or r.get('title', ''))[:38], star,
        r.get('track', ''), r.get('value', 0), r.get('grade', ''), batch))
P.append('')
P.append('---')
P.append('')
P.append('## 五、附录')
P.append('')
P.append('### 5.1 覆盖度三关（本日不触发）')
P.append('')
P.append('- 门① 同质去重 / 门② 赛道覆盖 / 门③ 价值天花板：候选池 0 篇，三关均不触发。')
P.append('- 门③ 参考值现算：库内近 30 天 Top10 均分 **%.3f**（窗口 %s；Top10 为 2610.03162 4.65 / 2610.03283 4.58 / 2610.19674 4.57 / 2610.23772 4.57 / 2610.39399 4.37 / 2610.34263 4.35 / 2610.18872 4.30 / 2610.22778 4.30 / 2609.31418 4.30 / 2610.37602 4.30）。' % (GATE3, GATE3_WIN))
P.append('')
P.append('### 5.2 证据等级分布')
P.append('')
P.append('- 本日无新抓取。参考表 24 篇证据等级：24 篇全 L0/FULL（10-31 运行实测）；无 PARTIAL / ABSTRACT_ONLY。')
P.append('')
P.append('### 5.3 失败/降级清单')
P.append('')
P.append('- 无抓取失败。数据源状态：RSS 周末节律空源（7 分类 0 条目，非故障）；API 双主机 200。')
P.append('- 工具效率改进 1 项：对账脚本由全量翻页改为 show=500 单页方案（10-30 组各分类均 <500 条，单页即完整），全程约 1 分钟。')
P.append('')
P.append('### 5.4 产物清单')
P.append('')
P.append('| 产物 | 路径 |')
P.append('|---|---|')
P.append('| 状态报告 | `reports/XR-Daily-Report-2026-11-02.md` |')
P.append('| 前沿参考 7 维表 | `papers/daily/2026-11-02/7dim-table.md`（24 篇） |')
P.append('| 运行日志 | `papers/daily/2026-11-02/run_log.md` |')
P.append('| 对账数据 | `data/audit_1102_days.json` / `data/audit_1102_alldays.json` / `data/missed_listing_1102.json` / `data/missed_listing_1102_fmt.json` / `data/missed_xr_abstract_1102.json` / `data/audit_1102_newday.json` / `data/raw/2026-11-02.jsonl` |')
P.append('| MOC 总索引 | `papers/MOC/MOC-总索引.md`（11-02 状态注记 + 批次索引行 + 页脚刷新） |')
P.append('| 前端 | `web/xr-paper-hub.html`（重建） |')
P.append('')
P.append('### 5.5 发布记录')
P.append('')
P.append('- 渠道① WorkBuddy 托管（workbuddy_sites_deploy）：见收尾汇报（若工具不可用则挂账，自 10-21 起连续不可用）。')
P.append('- 渠道② GitHub Pages：见收尾汇报（commit + push_to_github.py --incremental + deploy run + Pages 200 核验）。')
P.append('')
P.append('---')
P.append('')
P.append('*报告生成：2026-11-02 02:30 自动化运行（xr-paper-daily-brief skill · 9 步流水线）。*')

with io.open(os.path.join(ROOT, 'reports/XR-Daily-Report-2026-11-02.md'), 'w', encoding='utf-8') as f:
    f.write('\n'.join(P) + '\n')
print('written report, chars:', len('\n'.join(P)))

# ---------- MOC-总索引.md 维护 ----------
moc_path = os.path.join(ROOT, 'papers/MOC/MOC-总索引.md')
moc = io.open(moc_path, encoding='utf-8').read()

# 1) 状态注记：插在 11-01 状态注记之后（若尚无 11-02 注记）
if '状态注记（2026-11-02）' not in moc:
    note = ('> **状态注记（2026-11-02）**：周一 02:30，**无新增可处理论文**（周一凌晨状态日，周末积压公告未到时刻，同 10-26 模式）。'
            'listing 7 分类最新公告日均为 **2026-10-30**（10-31/11-01 周末无公告日段；周末积压公告时刻 = 周一 00:00 UTC = 当日 08:00 北京时间，晚于运行时刻）；'
            'API `submittedDate` 前沿 = **10-29**（已全部入馆）；RSS 7 分类全部 0 条目（lastBuildDate 11-01 04:00 UTC，周末节律空源）。'
            '10-30 公告组 show=500 单页全量复采：逐分类 declared=got（CV 233/GR 14/HC 51/MM 8/RO 129/AI 392/IV 15，槽位 842、唯一论文 728），未入馆 710 篇摘要级 XR 命中 13 篇均为 10-31 运行已剔非 XR → **0 漏网、无 backfill**。'
            '未伪造 Top10/评分/S 级；registry 维持 **%d 条**（S%d/A%d/B%d/C%d）；门③ 现算参考 **%.3f**（窗口 %s）。'
            '详见 [状态报告](../../reports/XR-Daily-Report-2026-11-02.md)。') % (len(reg), GRADES.get('S',0), GRADES.get('A',0), GRADES.get('B',0), GRADES.get('C',0), GATE3, GATE3_WIN)
    # 找到 11-01 状态注记行的末尾
    anchor = '详见 [运行报告](../../reports/XR-Daily-Report-2026-11-01.md)。'
    idx = moc.find(anchor)
    if idx >= 0:
        insert_at = idx + len(anchor)
        moc = moc[:insert_at] + '\n' + note + moc[insert_at:]
        print('MOC: 11-02 状态注记已插入')
    else:
        print('MOC WARN: 11-01 状态注记锚点未找到')

# 2) 批次索引表：补 11-02 行（插在 11-01 行之后）
row = '| 2026-11-02 | — | **0 新稿**（周一凌晨：listing 七分类最新公告日 10-30 + API 前沿 10-29 + RSS 7 分类空源三源互证；周末积压公告时刻 08:00 晚于运行时刻） | 状态报告日；10-30 公告组 show=500 单页复采 declared=got（842 槽位/728 唯一），未入馆 710 篇摘要级 13 篇命中均为已剔非 XR，0 漏网；门③ 现算 4.429 |'
if '| 2026-11-02 |' not in moc:
    lines = moc.split('\n')
    for i, l in enumerate(lines):
        if l.startswith('| 2026-11-01 |'):
            lines.insert(i + 1, row)
            moc = '\n'.join(lines)
            print('MOC: 批次索引 11-02 行已插入')
            break

# 3) 页脚刷新
import re as _re
footer_new = ('*最后更新：2026-11-02（周一凌晨状态日：listing 七分类最新公告日 10-30 + API 前沿 10-29 + RSS 7 分类空源三源互证；'
              '周末积压公告时刻 08:00 晚于运行时刻；10-30 公告组 show=500 单页复采 declared=got，未入馆 710 篇摘要级 13 篇命中均为已剔非 XR，0 漏网无 backfill；registry %d / 笔记 %d）。*' % (len(reg), NOTES_N))
moc = _re.sub(r'\*最后更新：[^\n]*\*', footer_new, moc, count=1)

# 4) 顶部摘要行的批次清单追加 11-02 状态日说明
if '11-02 周一凌晨状态日 0 新稿' not in moc:
    old_tail = '**11-01 周日状态日 0 新稿（周末无公告：listing 七分类最新公告日 10-30 + API 前沿 10-29 + RSS 6/7 分类空源三源互证；10-30 公告组 show=500 全量重采 728 篇与上批集合逐篇一致 710/710 差异 0，0 漏网无 backfill；修复 audit show=250 分页缺陷）**。'
    new_tail = old_tail + '；**11-02 周一凌晨状态日 0 新稿**（周末积压公告时刻 08:00 晚于运行时刻，同 10-26 模式；10-30 公告组 show=500 单页复采 declared=got 842 槽位/728 唯一，未入馆 710 篇摘要级 13 篇命中均为 10-31 运行已剔非 XR，0 漏网无 backfill）**。'
    if old_tail in moc:
        moc = moc.replace(old_tail, new_tail)
        print('MOC: 顶部摘要行已追加 11-02')
    else:
        print('MOC WARN: 顶部摘要锚点未找到')

with io.open(moc_path, 'w', encoding='utf-8') as f:
    f.write(moc)
print('MOC-总索引.md updated')
