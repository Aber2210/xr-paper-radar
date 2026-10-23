# -*- coding: utf-8 -*-
"""2026-10-24 运行报告：10 章全文精读 + 7 维参考表 + 覆盖校验 + 附录。"""
import json, glob, os, ast, re

scored = {}
for f in ('data/scored_1024.json', 'data/scored_backfill_1024.json'):
    for r in json.load(open(f, encoding='utf-8')):
        scored[r['id']] = r
digest = {}
for g in (1, 2, 3):
    for x in json.load(open(f'data/digest_1024_g{g}.json', encoding='utf-8')):
        digest[x['id']] = x

# 从 write_notes_1024.py 中解析 EXTRA 字典（不执行写笔记逻辑）
src = open('scripts/write_notes_1024.py', encoding='utf-8').read()
m = re.search(r'EXTRA = (\{.*?\n\})\n', src, re.S)
EXTRA = ast.literal_eval(m.group(1))

def notefile(pid):
    hits = glob.glob(f'papers/notes/{pid}__*.md')
    return os.path.basename(hits[0]) if hits else None

main_rows = sorted([r for r in scored.values() if r.get('batch', '2026-10-24') == '2026-10-24'], key=lambda r: -r['value'])
bf_rows = sorted([r for r in scored.values() if r.get('batch') == 'backfill-1024'], key=lambda r: -r['value'])
top10 = main_rows[:10]
DIMS = ['IMP', 'NOV', 'TEC', 'EXP', 'PER', 'TRL', 'REP']

R = []
R.append('# XR 每日论文雷达 · 运行报告 2026-10-24')
R.append('')
R.append('> **公告窗口**：2026-10-23（周五）公告批次（提交日 10-16~10-22、周五 20:00 ET 释放）。')
R.append('> **拉取日**：2026-10-24（周六 02:30）。**诚实口径：本批处理 10-23 公告批次的真新提交，非 10-24 当日新提交**（公告日≠拉取日；周六无新公告）。')
R.append('> 本报告由 `xr-paper-daily-brief` skill 驱动，全流程 9 步执行；所有评分为全文证据定稿（先抓全文再定稿）。')
R.append('')
R.append('## 一、执行摘要')
R.append('')
R.append('- **入选**：主批 XR 相关新稿 **17 篇**（8 A / 9 B / 0 S / 0 C）+ 同日 backfill-1024 补录旧稿 **4 篇**（2 A / 2 B）；registry 597 → **618**。')
R.append('- **Top10**：8 A + 2 B，最高 **4.22**（EgoHand，NVIDIA）——加权分已达 S 级线（≥4.2），但当日为非重磅日（4.22 < 库内近 30 天 Top10 均分 4.416，现算），按覆盖度门③校准关**不评 S 级**，分数如实保留 4.22。')
R.append('- **全文证据**：21 篇候选（17 主批 + 4 backfill）**全部 L0/FULL**（39,907–108,292 字符），无限流、无降级、无伪造。')
R.append('- **覆盖度三关**：门① 最大 Jaccard 0.109（<0.62 通过）；门② Top10 覆盖 7 赛道（≥5 通过）；门③ 4.22 < 4.416（现算）→ 非重磅日无 S（校准关，不触发重筛）。**三关全过、未触发重筛。**')
R.append('- **落后登记**：OUTDATED/SUPERSEDED **0 篇**；技术路线观察 3 条（免训练「冻结骨干+后处理/证据复用」范式收敛；第一视角手部重建双路线互补；社交 VR 实证转向空间配置与群体动力学）。')
R.append('- **上游对账（第 1 步）**：listing 7 分类最新公告日 10-23；10-22 组 402 篇 + 10-23 组 411 篇全量对账。摘要级 XR 过滤 10-22 组 9 篇命中全部为 10-23 运行已剔除的非 XR（**0 漏网**）；10-23 组 23 篇命中中 **8 篇为 RSS 漏网**，其中 5 篇 XR 相关经对账补齐入主批（PiHand / VR 告别 / VR 漫游视频 / VecTile / IMU 定向）——两渠道交叉互证覆盖完整。')
R.append('- **重要发现**：① 本批出现库内触觉硬件类第二篇力感知阵列（VecTile，继 Hugging Suit 之后的柔性 3-DoF 剪切方案）；② 社交 VR 用户研究三篇同期（共看空间配置 / VR 录播传播 / VR 告别仪式），标志 VR 实证从「个体沉浸」转向「空间与社会设计」；③ 4D 高斯生态快速扩展（Stream4D 流式免训练、R4DGS 指代分割、NoPo4D 免位姿前馈）。')
R.append('')
R.append('## 二、Top10 排行榜')
R.append('')
R.append('| 排名 | 论文 | 赛道 | 总分 | 等级 | 证据 | 公告类型 | 落后标记 |')
R.append('|---:|---|---|---:|---|---|---|---|')
for i, r in enumerate(top10, 1):
    R.append(f"| {i} | {r['title_zh']}（{r['id']}） | {r['track']} | {r['value']:.2f} | {r['grade']} | {r['evidence']} | {r['announce_type']} | — |")
R.append('')
R.append('> 同分排序规则：加权降序 → IMP/NOV 降序 → 赛道多样性优先 → id 升序。本批无同分并列进入 Top10 的情形。')
R.append('')
R.append('## 三、逐篇深度解读（按重要性降序）')
R.append('')
for i, r in enumerate(top10, 1):
    pid = r['id']
    d = digest[pid]
    oneline, action, tags = EXTRA[pid]
    s = r['scores']
    R.append(f"### 第 {i} 章 · {d['title_zh']}（{pid}）— {r['value']:.2f} {r['grade']} · {r['track']}")
    R.append('')
    R.append(f"**一句话结论**：{oneline}")
    R.append('')
    R.append(f"**7 维评分**：IMP {s['IMP']} · NOV {s['NOV']} · TEC {s['TEC']} · EXP {s['EXP']} · PER {s['PER']} · TRL {s['TRL']} · REP {s['REP']}（加权 {r['value']:.2f}；venue：{d['venue']}；证据：{r['evidence']}，{r['fetch_level']}，{r['fulltext_chars']:,} 字符）")
    R.append('')
    R.append(f"**要解决的问题**：{d['problem']}")
    R.append('')
    R.append(f"**方法详解**：{d['method']}")
    R.append('')
    R.append(f"**实验与结果**：{d['experiments']}")
    R.append('')
    R.append('**创新点与贡献**：')
    for x in d['innovation']:
        R.append(f"- {x}")
    R.append('')
    R.append('**局限与风险**：')
    for x in d['limits']:
        R.append(f"- {x}")
    R.append('')
    R.append(f"**与文献库的关系**：{d['relation']}")
    R.append('')
    R.append(f"**可复现性**：{d['repro']}")
    R.append('')
    R.append(f"**行动建议**：{action}")
    R.append('')
    R.append(f"原子笔记：[`papers/notes/{notefile(pid)}`](../notes/{notefile(pid)})")
    R.append('')

R.append('## 四、当日全量 7 维度对比表（参考）')
R.append('')
R.append('主批 17 篇（公告日 2026-10-23，全部 L0/FULL；⭐ = Top10）：')
R.append('')
R.append('| arXiv | 标题 | 赛道 | IMP | NOV | TEC | EXP | PER | TRL | REP | 总分 | 等级 | 公告类型 |')
R.append('|---|---|---|---|---|---|---|---|---|---|---|---|---|')
for r in main_rows:
    s = r['scores']
    star = ' ⭐' if r['in_top10'] else ''
    R.append(f"| {r['id']} | {r['title_zh']}{star} | {r['track']} | {s['IMP']} | {s['NOV']} | {s['TEC']} | {s['EXP']} | {s['PER']} | {s['TRL']} | {s['REP']} | {r['value']:.2f} | {r['grade']} | {r['announce_type']} |")
R.append('')
R.append('backfill-1024 补录 4 篇（旧稿 replace 再公告首次入馆，非当日新提交）：')
R.append('')
R.append('| arXiv | 标题 | 赛道 | IMP | NOV | TEC | EXP | PER | TRL | REP | 总分 | 等级 | 公告类型 |')
R.append('|---|---|---|---|---|---|---|---|---|---|---|---|---|')
for r in bf_rows:
    s = r['scores']
    R.append(f"| {r['id']} | {r['title_zh']} | {r['track']} | {s['IMP']} | {s['NOV']} | {s['TEC']} | {s['EXP']} | {s['PER']} | {s['TRL']} | {s['REP']} | {r['value']:.2f} | {r['grade']} | {r['announce_type']} |")
R.append('')
R.append('## 五、覆盖率校验与筛选过程说明')
R.append('')
R.append('### 5.1 数据源与对账')
R.append('')
R.append('- API 双源探针 200（export.arxiv.org / arxiv.org/api/query）；submittedDate 前沿不停滞（本批以公告日口径为准）。')
R.append('- RSS（rss.arxiv.org）200：7 分类全量去重 643 条 → 关键词命中 33（公告日全部为 2026-10-23）。')
R.append('- listing 对账（第 1 步，先于拉取）：TARGET_LO=2026-10-22；10-22 组 402 篇、10-23 组 411 篇全量采集（show=500，逐日完整性校验通过；per-cat SHORT 为跨分类认领的统计假象，以 per-category 自检为准）。摘要级过滤：10-22 组 9 篇命中全部为 10-23 运行已甄别剔除的非 XR（0 漏网）；10-23 组 23 篇命中 = RSS 15 + RSS 漏网 8。')
R.append('')
R.append('### 5.2 甄别链')
R.append('')
R.append('RSS 命中 33 → 去 registry(597) 后 31 新 → 剔除：库内 v2 再公告 2 篇（2610.28490 / 2610.22363）+ 非 XR 误命中 6 篇 + 旧稿 replace 再公告 6 篇（4 篇 XR 相关 → backfill-1024；2 篇非 XR：心脏 MRI 去噪、6G 联邦学习）→ 主批 XR 相关 17 篇。listing 对账补齐的 5 篇 RSS 漏网 XR 稿并入主批（PiHand / 30734 / 30731 / 31472 / 31156），另有 3 篇 listing 漏网经甄别非 XR（31253 医学 / 30969 机械操作 / 30955 辅助机器人）。')
R.append('')
R.append('### 5.3 覆盖度三关')
R.append('')
R.append('| 关卡 | 判据 | 实测 | 结论 |')
R.append('|---|---|---|---|')
R.append('| 门① 同质去重 | 21 候选 vs 库内 597 条标题+摘要 Jaccard < 0.62 | max 0.109（2605.22190 vs 2609.32711） | **通过** |')
R.append('| 门② 赛道覆盖 | Top10 ≥ 5 赛道 | 7 赛道（化身与人体×2 / 交互与输入 / 重建与SLAM×2 / 神经渲染 / 触觉与多模态 / 系统与平台 / 感知与认知） | **通过** |')
R.append('| 门③ 价值天花板 | 当日最高 vs 库内近 30 天 Top10 均分（现算） | 4.22 < 4.416（window≥2026-09-24，447 条入窗） | **非重磅日，无 S 级**（校准关，不触发重筛） |')
R.append('')
R.append('三关全过，未触发重筛；低量不凑数（本批 17 篇真新稿，无需回补）。')
R.append('')
R.append('### 5.4 落后登记')
R.append('')
R.append('- 论文级 OUTDATED/SUPERSEDED：**0 篇**（门①通过且无同质；新稿方法均为当期贡献）。')
R.append('- 路线观察 3 条：① 免训练「冻结骨干 + 后处理/证据复用」范式在语义 3DGS/4D 重建/特征匹配三处同期收敛（RecallGS / Stream4D / MVLoMa）；② 第一视角手部重建双路线互补（EgoHand 相机感知单目 vs MEgoVista calibrated stereo 度量标尺），非取代；③ 社交 VR 实证转向空间配置与群体动力学（30353 / 30731 / 30734）。')
R.append('')
R.append('## 六、附录')
R.append('')
R.append('### 6.1 抓取与证据等级分布')
R.append('')
R.append('- 21 篇候选：L0 × 21、L1 × 0、PARTIAL × 0、ABSTRACT_ONLY × 0。字符范围 39,907（2610.31284）– 108,292（2610.30353）。')
R.append('- 抓取配置：严格串行 3s/篇；无限流（429/503）、无 406 持续拒绝、无降级链路触发。')
R.append('')
R.append('### 6.2 剔除清单（公告窗口内不入馆）')
R.append('')
R.append('- 非 XR 6 篇：2610.31494 AgentVQA / 2610.30319 TerraTransfer++ / 2610.30955 上肢震颤辅助装置 / 2610.30969 IORA / 2610.30774 月球视觉 SLAM 评估 / 2610.31253 术中肿瘤定位。')
R.append('- 旧稿 replace 非 XR 2 篇：2609.31777 心脏 MRI 去噪 / 2607.06768 AirPASS（6G）。（另 2 篇旧稿非 XR：2604.07993 HEX 人形操作 / 2604.24033 事件相机 SLAM 基准，见 run_log。）')
R.append('- 库内 v2 再公告 2 篇：2610.28490 / 2610.22363。')
R.append('- 旧稿 replace XR 相关 4 篇 → backfill-1024（2605.22190 / 2609.16684 / 2601.14895 / 2508.15169）。')
R.append('')
R.append('### 6.3 产物清单')
R.append('')
R.append('- 本报告 + [MOC-2026-10-24](../MOC/MOC-2026-10-24.md) + [MOC-backfill-1024](../MOC/MOC-backfill-1024.md) + [MOC-总索引](../MOC/MOC-总索引.md)（刷新）')
R.append('- 原子笔记 21 篇（`papers/notes/`，主批 17 + backfill 4）')
R.append('- [7 维对比表](../daily/2026-10-24/7dim-table.md) · [评分明细](../daily/2026-10-24/scored.md) · [执行日志](../daily/2026-10-24/run_log.md) · [backfill-1024 7 维表](../daily/backfill-1024/7dim-table.md)')
R.append('- registry 597 → 618（备份 `papers/library/registry.jsonl.bak-20261024`）')
R.append('- 前端 `web/xr-paper-hub.html` 重建；双渠道发布（WorkBuddy 托管 + GitHub Pages）')
R.append('')
open('reports/XR-Daily-Report-2026-10-24.md', 'w', encoding='utf-8').write('\n'.join(R))
print('report written:', len('\n'.join(R)), 'chars')
