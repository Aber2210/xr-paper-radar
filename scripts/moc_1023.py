# -*- coding: utf-8 -*-
# moc_1023.py — 生成 MOC-2026-10-23.md + MOC-backfill-1023.md，并增量刷新 MOC-总索引.md
import json, re

ROOT = 'D:/Agent/WorkBuddy/Research'
reg = {}
for l in open(f'{ROOT}/papers/library/registry.jsonl', encoding='utf-8'):
    if l.strip():
        d = json.loads(l)
        reg[d['id'].split(':')[-1].split('v')[0]] = d
slug = {}
for g in (1, 2, 3, 4, 5):
    for x in json.load(open(f'{ROOT}/data/notes_content_1023_g{g}.json', encoding='utf-8')):
        slug[x['id']] = x['slug']

def items_of(batch):
    return [d for d in reg.values() if d.get('batch') == batch]

# ============================================================ MOC-2026-10-23
items = sorted(items_of('2026-10-23'), key=lambda d: -d['value'])
top10 = [d for d in items if d['in_top10']]
rest = [d for d in items if not d['in_top10']]

def row(d, rank=None):
    bid = d['id'].split(':')[-1]
    link = f"[→](../notes/{bid}__{slug[bid]}.md)"
    if rank:
        return f"| {rank} | {d['title_zh']} | {d['track']} | {d['value']:.2f} | {d['grade']} | {d['evidence']} | {link} |"
    return f"| {d['title_zh']} | {d['track']} | {d['value']:.2f} | {d['grade']} | {d['evidence']} | {link} |"

L = []
L.append('# MOC · 2026-10-23（主批次）')
L.append('')
L.append('> **公告窗口**：2026-10-22（周四）公告批次（提交日 10-15~10-21、周四 20:00 ET 释放）；**拉取日**：2026-10-23（周五 02:30）。')
L.append('> **诚实口径**：本批处理 10-22 公告批次的真新提交（2610.* 前缀甄别：20 new + 5 cross + 2 个 replace-v2 首次入馆），**非当日（10-23）新提交**（公告日≠拉取日）；RSS 混入的旧稿 replace/cross 中 4 篇 XR 相关单列 [MOC-backfill-1023](./MOC-backfill-1023.md)，listing 对账发现的 10-21 公告批次漏网 5 篇亦入该 backfill；2 篇库内 v2 再公告（NormLift / HumanVerse）已剔除。')
L.append('')
L.append('## 本批概览')
L.append('')
L.append('- 入馆 **15 篇**（S×0 / A×7 / B×6 / C×2），registry 573 → **588**；同日 backfill-1023 补录 9 篇 → **597**。Top10：**7 A + 3 B**，最高 **3.78**（SSIO）。')
L.append('- 全文 **15 篇候选全部 L0/FULL**（41,612–130,608 字符），串行 3s/篇，无限流/降级/伪造。')
L.append('- 覆盖度三关全过：门① 最大 Jaccard **0.071**（2610.30032 vs 库内 2609.25422，<0.62 通过）；门② Top10 覆盖 **8 赛道**（≥5 通过，全批同覆 8 赛道）；门③ 当日最高 **3.78 < 库内近 30 天 Top10 均分 4.416**（现算，窗口 2026-09-23~10-23、444 条入窗，差值 -0.636）→ **非重磅日，无 S 级，未拔高**。三关全过、**未触发重筛**。')
L.append('- OUTDATED/SUPERSEDED：**0 篇**；路线观察 3 条——① 惯性里程计「免真值自监督」成为跨载体训练新范式（SSIO 对库内 AirIO/RoNIN/TLIO 监督线构成补充而非取代）；② 稀疏视图 NeRF 从「加先验」转向「修目标」（DriftNeRF 诊断渲染损失无跨射线一致性项，与库内 FreeNeRF/DNGaussian 先验线互补）；③ 3DGS 压缩走到「语义-几何联合约束」（ClunoGS 对库内 RGB 驱动剪枝线构成语义保持改进）。')
L.append('- 上游对账（第 1 步）：listing 7 分类最新公告日 10-22；10-21 组 532 篇（上批已处理、复核）+ 10-22 组 402 篇全量对账；摘要级 XR 过滤（914 篇池、KW 全称+缩写双层）**10-22 组 22 篇全部在 RSS 集合内（0 漏网）**；10-21 组复核 19 篇命中，5 篇 XR 相关漏网 → backfill-1023。')
L.append('')
L.append('## Top10（按加权降序，同分按 IMP/NOV → 赛道多样性 → id 升序）')
L.append('')
L.append('| 排名 | 论文 | 赛道 | 分值 | 等级 | 证据 | 笔记 |')
L.append('|---:|---|---|---:|---|---|---|')
for i, d in enumerate(top10, 1):
    L.append(row(d, i))
L.append('')
L.append('## 其余入馆（5 篇）')
L.append('')
L.append('| 论文 | 赛道 | 分值 | 等级 | 证据 | 笔记 |')
L.append('|---|---|---:|---|---|---|')
for d in rest:
    L.append(row(d))
L.append('')
L.append('## 本批剔除（公告窗口内不入馆）')
L.append('')
L.append('- 非 XR 10 篇：UNIVERS（医学体积定位）、FogTTA（雾天检测）、AirPlayground（无人机导航基准）、DiffResearch（扩散 LLM）、Block Diffusion EHR（医学记录）、A2I-Calib++（多 IMU 标定）、距离场 RL 碰撞回避、移动机械臂 NBV、假体可供性分割。')
L.append('- 旧稿 replace 非 XR 2 篇：2610.24858（MRI 高斯超分）、2602.01860（无人机竞速）。')
L.append('- 旧稿 replace/cross XR 相关 4 篇（2604.11685 / 2608.21009 / 2604.10809 / 2607.06464）→ 单列 backfill-1023。')
L.append('- 库内 v2 再公告 2 篇：NormLift（2609.18898）、HumanVerse（2610.18950）。逐篇清单见 [scored.md](../daily/2026-10-23/scored.md)。')
L.append('')
L.append('## 同日 backfill')
L.append('')
L.append('- [MOC-backfill-1023](./MOC-backfill-1023.md)：10-21 公告批次 listing 漏网 5 篇 + 旧稿 replace/cross 再公告 4 篇（1 A / 7 B / 1 C），诚实标注非当日新提交。')
L.append('')
L.append('## 数据与过程')
L.append('')
L.append('- [7 维对比表](../daily/2026-10-23/7dim-table.md) · [评分明细](../daily/2026-10-23/scored.md) · [执行日志](../daily/2026-10-23/run_log.md)')
L.append('- [运行报告](../../reports/XR-Daily-Report-2026-10-23.md) · [Backfill 报告](../../reports/XR-Backfill-Report-1023.md)')
L.append('- 数据源：API 双源探针 200（submittedDate 停滞 10-21）；RSS cs.CV 212 条（公告日 10-22）→ RSS 兜底，7 分类去重 649 条、关键词命中 33。')
L.append('')
open(f'{ROOT}/papers/MOC/MOC-2026-10-23.md', 'w', encoding='utf-8').write('\n'.join(L))
print('written MOC-2026-10-23.md')

# ============================================================ MOC-backfill-1023
bitems = sorted(items_of('backfill-1023'), key=lambda d: -d['value'])
L = []
L.append('# MOC · backfill-1023（补录批次）')
L.append('')
L.append('> **批次性质**：补录批次，**非 2026-10-23 当日新提交**。')
L.append('> ① **10-21 公告批次 listing 漏网 5 篇**（公告日 10-21、提交日 10-15~10-20；10-22 运行已处理该公告日主流水，本批补录其摘要级过滤漏网的 XR 相关稿）；')
L.append('> ② **旧稿 replace/cross 再公告首次入馆 4 篇**（原始投稿周期 2604 / 2607 / 2608，10-23 RSS 拉取混入）。')
L.append('')
L.append('## 本批概览')
L.append('')
L.append('- 补录入馆 **9 篇**（S×0 / A×1 / B×7 / C×1），registry 588 → **597**；最高 **3.65**（Unfolding 3DGS）。')
L.append('- 全文证据：**8 篇 L0/FULL**（29,750–139,019 字符）+ **1 篇 L1/PARTIAL**（2610.28131 OV-Foam，ar5iv 仅返 abs 页壳、正文缺失，按摘要级评估并显式声明）。')
L.append('- 覆盖度：门① 最大 Jaccard **0.075**（2610.28131 vs 库内 2610.08756，<0.62 通过）；全批覆盖 **7 赛道**；门③ 对 backfill 不适用。无重筛、无 OUTDATED。')
L.append('- 覆盖补强：3DGS LOD 第三条路线（Unfolding 3DGS）、XR 年龄保障新模态（手背图像、无面部生物特征）、光学-感知联合可微设计（编码孔径+3DGS）、单图仿真就绪场景（SceneRig）、无电子 UMI 采集、热动力学 4DGS（GTSM，边界纳入）、幂图特征提升（OV-Foam）、360° VIO 基准（Hilti）。')
L.append('- 口径说明：GTSM 应用域为工业热场监测（10-22 运行曾据此剔除出主批），本批以其 3DGS 方法贡献边界纳入、B 级入馆。')
L.append('')
L.append('## 排名（按加权降序）')
L.append('')
L.append('| 排名 | 论文 | 赛道 | 分值 | 等级 | 证据 | 来源 | 笔记 |')
L.append('|---:|---|---|---:|---|---|---|---|')
for i, d in enumerate(bitems, 1):
    bid = d['id'].split(':')[-1]
    src = '10-21 漏网' if d.get('announce_type')=='leak-1021' else f"{d.get('announce_type','replace')} 再公告"
    L.append(f"| {i} | {d['title_zh']} | {d['track']} | {d['value']:.2f} | {d['grade']} | {d['evidence']} | {src} | [→](../notes/{bid}__{slug[bid]}.md) |")
L.append('')
L.append('## 数据与过程')
L.append('')
L.append('- [7 维对比表](../daily/backfill-1023/7dim-table.md) · [评分明细](../daily/backfill-1023/scored.md) · [执行日志](../daily/backfill-1023/run_log.md)')
L.append('- [Backfill 报告](../../reports/XR-Backfill-Report-1023.md)')
L.append('')
open(f'{ROOT}/papers/MOC/MOC-backfill-1023.md', 'w', encoding='utf-8').write('\n'.join(L))
print('written MOC-backfill-1023.md')

# ============================================================ 刷新 MOC-总索引
idx = open(f'{ROOT}/papers/MOC/MOC-总索引.md', encoding='utf-8').read()

# 1) 头部批次列表：在 10-22 段后追加 10-23 与 backfill-1023
old = '· **2026-10-22:20（10-21 公告批次真新提交，非重磅日无S）**'
new = old + ' · **2026-10-23:15（10-22 公告批次真新提交，非重磅日无S）** · **backfill-1023:9（10-21 公告 listing 漏网 5 篇 + 旧稿 replace/cross 再公告 4 篇）**'
assert old in idx; idx = idx.replace(old, new)

# 2) registry 计数
old = '（累计 **573 篇**'
new = '（累计 **597 篇**'
assert old in idx; idx = idx.replace(old, new)

# 3) 状态注记：在 10-22 注记后追加 10-23 + backfill-1023 两条
anchor = '详见 [运行报告](../../reports/XR-Daily-Report-2026-10-22.md)。\n'
note = ('> **状态注记（2026-10-23）**：周五，API 双源探针 200、submittedDate 前沿停滞 10-21；RSS cs.CV 212 条（公告日 10-22，周四）→ RSS 兜底。本批处理 **10-22 公告批次**真新提交 15 篇（S×0 / A×7 / B×6 / C×2，Top10：7 A / 3 B，最高 3.78 SSIO），全文 15 篇全 **L0/FULL**；三关通过（门① max Jaccard 0.071；门② Top10 覆盖 8 赛道；门③ 3.78 < 库近 30 天 Top10 均分 4.416 现算，**非重磅日无 S 级**）、无重筛、无 OUTDATED。listing 对账：10-21 组 532 篇（复核）+ 10-22 组 402 篇；摘要级过滤 10-22 组 22 篇全在 RSS 集合（**0 漏网**），10-21 组复核 19 篇中 5 篇 XR 漏网 → backfill-1023。详见 [运行报告](../../reports/XR-Daily-Report-2026-10-23.md) 与 [MOC-2026-10-23](./MOC-2026-10-23.md)。\n'
        '> **状态注记（backfill-1023）**：周五，listing 漏网补录 + 旧稿 replace/cross 再公告首次入馆 9 篇（A×1 / B×7 / C×1，最高 3.65 Unfolding 3DGS），8 篇 L0/FULL + 1 篇 L1/PARTIAL（2610.28131 OV-Foam，ar5iv 正文缺失、摘要级评估并显式声明）；门① max Jaccard 0.075、门② 7 赛道、门③ 不适用；无重筛、无 OUTDATED。诚实口径：**非当日新提交**。详见 [Backfill 报告](../../reports/XR-Backfill-Report-1023.md) 与 [MOC-backfill-1023](./MOC-backfill-1023.md)。\n')
assert anchor in idx
idx = idx.replace(anchor, anchor + note, 1)

# 4) 速查入口
old = '| 最新一期 | [MOC · 2026-10-21](./MOC-2026-10-21.md) |'
new = '| 最新一期 | [MOC · 2026-10-23](./MOC-2026-10-23.md) |'
assert old in idx; idx = idx.replace(old, new)
old = '| 上一期 | [MOC · 2026-10-20](./MOC-2026-10-20.md) |'
new = '| 上一期 | [MOC · 2026-10-22](./MOC-2026-10-22.md) |'
assert old in idx; idx = idx.replace(old, new)
old = '（现有 268 篇）'
new = '（现有 292 篇）'
assert old in idx; idx = idx.replace(old, new)
old = '| 最新运行状态 | [运行报告 2026-10-21](../../reports/XR-Daily-Report-2026-10-21.md)（10-20 公告批次 31 篇 + backfill-1021 10 篇；0 S / 15 A / 20 B / 6 C；非重磅日） |'
new = '| 最新运行状态 | [运行报告 2026-10-23](../../reports/XR-Daily-Report-2026-10-23.md)（10-22 公告批次 15 篇 + backfill-1023 9 篇；0 S / 8 A / 13 B / 3 C；非重磅日） |'
assert old in idx; idx = idx.replace(old, new)

# 5) 批次索引表：末尾两行
old = '| 2026-10-22 | [MOC-2026-10-22](./MOC-2026-10-22.md) | XR 20（入选 10）· Top10 10A · 非重磅日（无S） | 10-21 公告批次；listing 摘要级两渠道互证 0 漏网，无 backfill |\n'
new = (old +
 '| 2026-10-23 | [MOC-2026-10-23](./MOC-2026-10-23.md) | XR 15（入选 10）· Top10 7A/3B · 非重磅日（无S） | 10-22 公告批次；listing 摘要级 0 漏网；10-21 组复核 5 篇漏网入 backfill |\n'
 '| backfill-1023 | [MOC-backfill-1023](./MOC-backfill-1023.md) | 补录 9（1A/7B/1C）· 非当日新提交 | 10-21 公告 listing 漏网 5 篇 + 旧稿 replace/cross 再公告 4 篇；1 篇 PARTIAL |\n')
assert old in idx; idx = idx.replace(old, new)

# 6) 新增两个批次 Top10 段（追加在文件末尾前）
sections = []
sections.append('### 2026-10-23 新增（Top10：7 A / 3 B，非重磅日无 S）\n')
sections.append('> 10-22（周四）公告批次（拉取日 10-23 周五，公告日≠拉取日）；当日最高 3.78 < 库近 30 天 Top10 均分 4.416（现算）→ 非重磅日。三关通过（门① 0.071；门② 8 赛道）、无重筛、无 OUTDATED。\n')
sections.append('| 排名 | 论文 | 赛道 | 分值 | 等级 | 笔记 |')
sections.append('|---:|---|---|---:|---|---|')
for i, d in enumerate(top10, 1):
    bid = d['id'].split(':')[-1]
    sections.append(f"| {i} | {d['title_zh']} | {d['track']} | {d['value']:.2f} | {d['grade']} | [→](../notes/{bid}__{slug[bid]}.md) |")
sections.append('')
sections.append('### backfill-1023 补录（9 篇：1 A / 7 B / 1 C，非当日新提交）\n')
sections.append('> 10-21 公告批次 listing 漏网 5 篇 + 旧稿 replace/cross 再公告 4 篇；8 篇 L0/FULL + 1 篇 L1/PARTIAL（2610.28131 OV-Foam）。门① max Jaccard 0.075、门② 7 赛道；无重筛、无 OUTDATED。\n')
sections.append('| 论文 | 赛道 | 分值 | 等级 | 来源 | 笔记 |')
sections.append('|---|---|---:|---|---|---|')
for d in bitems:
    bid = d['id'].split(':')[-1]
    src = '10-21 漏网' if d.get('announce_type')=='leak-1021' else f"{d.get('announce_type','replace')} 再公告"
    sections.append(f"| {d['title_zh']} | {d['track']} | {d['value']:.2f} | {d['grade']} | {src} | [→](../notes/{bid}__{slug[bid]}.md) |")
sections.append('')
idx = idx.rstrip('\n') + '\n\n' + '\n'.join(sections)

# 7) 页脚
old = '*最后更新：2026-10-21（10-20 公告批次 + backfill-1021） · 库内 **553 篇** · 原子笔记 **248 篇** · MOC 22 份'
new = '*最后更新：2026-10-23（10-22 公告批次 + backfill-1023） · 库内 **597 篇** · 原子笔记 **292 篇** · MOC 24 份'
assert old in idx; idx = idx.replace(old, new)
old = '10-21 完成：批次索引表补 2 行、补 10-21 状态注记/A 级段/Top10 段与 backfill-1021 段、页脚计数刷新；registry in_top10 修正 14 处（备份 registry.jsonl.bak-20261021b）*'
new = old + '；10-23 完成：批次索引表补 2 行、补 10-23 与 backfill-1023 状态注记/Top10 段、速查入口与页脚刷新；registry 573→597（备份 registry.jsonl.bak-20261023，in_top10 校正 0 处）；路线观察新增 3 条（惯性里程计免真值自监督范式、稀疏视图 NeRF「修目标」线、3DGS 语义-几何联合压缩）*'
assert old in idx; idx = idx.replace(old, new)

open(f'{ROOT}/papers/MOC/MOC-总索引.md', 'w', encoding='utf-8').write(idx)
print('updated MOC-总索引.md')
