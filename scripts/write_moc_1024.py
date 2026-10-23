# -*- coding: utf-8 -*-
"""2026-10-24：MOC-2026-10-24 + MOC-backfill-1024 + 总索引刷新 + 运行报告。"""
import json, glob, os, re

scored = {}
for f in ('data/scored_1024.json', 'data/scored_backfill_1024.json'):
    for r in json.load(open(f, encoding='utf-8')):
        scored[r['id']] = r
digest = {}
for g in (1, 2, 3):
    for x in json.load(open(f'data/digest_1024_g{g}.json', encoding='utf-8')):
        digest[x['id']] = x

def notefile(pid):
    hits = glob.glob(f'papers/notes/{pid}__*.md')
    return os.path.basename(hits[0]) if hits else None

main_rows = sorted([r for r in scored.values() if r.get('batch', '2026-10-24') == '2026-10-24'], key=lambda r: -r['value'])
bf_rows = sorted([r for r in scored.values() if r.get('batch') == 'backfill-1024'], key=lambda r: -r['value'])
top10 = main_rows[:10]

# ---------- MOC-2026-10-24 ----------
L = []
L.append('# MOC · 2026-10-24（主批次）')
L.append('')
L.append('> **公告窗口**：2026-10-23（周五）公告批次（提交日 10-16~10-22、周五 20:00 ET 释放）；**拉取日**：2026-10-24（周六 02:30）。')
L.append('> **诚实口径**：本批处理 10-23 公告批次的真新提交（RSS 命中 + listing 对账补齐），**非当日（10-24）新提交**（公告日≠拉取日）；RSS 混入的旧稿 replace 再公告中 4 篇 XR 相关单列 [MOC-backfill-1024](./MOC-backfill-1024.md)；2 篇库内 v2 再公告（2610.28490 / 2610.22363）已剔除。')
L.append('')
L.append('## 本批概览')
L.append('')
L.append('- 入馆 **17 篇**（S×0 / A×8 / B×9 / C×0），registry 597 → **614**；同日 backfill-1024 补录 4 篇 → **618**。Top10：**8 A + 2 B**，最高 **4.22**（EgoHand，已达 S 线但因非重磅日按校准关记 A）。')
L.append('- 全文 **21 篇候选（17 主批 + 4 backfill）全部 L0/FULL**（39,907–108,292 字符），串行 3s/篇，无限流/降级/伪造。')
L.append('- 覆盖度三关全过：门① 最大 Jaccard **0.109**（2605.22190 vs 库内 2609.32711，<0.62 通过）；门② Top10 覆盖 **7 赛道**（化身与人体×2 / 交互与输入 / 重建与SLAM×2 / 神经渲染 / 触觉与多模态 / 系统与平台 / 感知与认知，≥5 通过）；门③ 当日最高 **4.22 < 库内近 30 天 Top10 均分 4.416**（现算，窗口 2026-09-24~10-24、447 条入窗，差值 -0.196）→ **非重磅日，无 S 级，未拔高**。三关全过、**未触发重筛**。')
L.append('- OUTDATED/SUPERSEDED：**0 篇**；路线观察 3 条——① 「冻结骨干 + 后处理/证据复用」免训练范式同期收敛（RecallGS 历史回忆替代学习式 3D 分支、Stream4D KV Cache 运动线索、MVLoMa 复用几何基础模型 token）；② 第一视角手部重建双路线互补（EgoHand 相机感知单目 vs MEgoVista stereo 度量标尺）；③ 社交 VR 实证从「个体沉浸」转向「空间配置与群体动力学」（30353 共看空间配置 / 30731 VR 录播传播 / 30734 VR 告别仪式三篇用户研究同期）。')
L.append('- 上游对账（第 1 步）：listing 7 分类最新公告日 10-23；10-22 组 402 篇 + 10-23 组 411 篇全量对账。摘要级 XR 过滤：**10-22 组 9 篇命中全部为 10-23 运行已甄别剔除的非 XR（0 漏网）**；**10-23 组 23 篇命中 = RSS 15 篇 + RSS 漏网 8 篇**（5 篇 XR 相关经 listing 补齐入主批：PiHand / VR 告别 / VR 漫游 / VecTile / IMU 定向；3 篇非 XR：术中肿瘤定位 / 机械 immobilization / 上肢震颤辅助装置）。')
L.append('')
L.append('## Top10（按加权降序，同分按 IMP/NOV → 赛道多样性 → id 升序）')
L.append('')
L.append('| 排名 | 论文 | 赛道 | 分值 | 等级 | 证据 | 公告类型 | 笔记 |')
L.append('|---:|---|---|---:|---|---|---|---|')
for i, r in enumerate(top10, 1):
    L.append(f"| {i} | {r['title_zh']} | {r['track']} | {r['value']:.2f} | {r['grade']} | {r['evidence']} | {r['announce_type']} | [→](../notes/{notefile(r['id'])}) |")
L.append('')
L.append('## 其余入馆（7 篇）')
L.append('')
L.append('| 论文 | 赛道 | 分值 | 等级 | 证据 | 笔记 |')
L.append('|---|---|---:|---|---|---|')
for r in main_rows[10:]:
    L.append(f"| {r['title_zh']} | {r['track']} | {r['value']:.2f} | {r['grade']} | {r['evidence']} | [→](../notes/{notefile(r['id'])}) |")
L.append('')
L.append('## 本批剔除（公告窗口内不入馆）')
L.append('')
L.append('- 非 XR 6 篇：AgentVQA（智能体视觉理解基准）、TerraTransfer++（机器人端到端规划）、上肢震颤 3-DoF 辅助装置（辅助机器人）、IORA（不规则物体 immobilization 机械操作）、月球视觉 SLAM 前端评估（行星机器人）、术中肿瘤弱监督定位（医学）。')
L.append('- 旧稿 replace 再公告 XR 相关 4 篇（2605.22190 / 2609.16684 / 2601.14895 / 2508.15169）→ 单列 backfill-1024；另 4 篇旧稿非 XR（心脏 MRI 去噪 / 人形操作 / 无人机事件 SLAM 基准 / 6G 联邦学习）剔除。')
L.append('- 库内 v2 再公告 2 篇：2610.28490（2026-10-22 批）、2610.22363（2026-10-17 批）。逐篇清单见 [scored.md](../daily/2026-10-24/scored.md)。')
L.append('')
L.append('## 同日 backfill')
L.append('')
L.append('- [MOC-backfill-1024](./MOC-backfill-1024.md)：10-23 公告批次中 RSS 混入的旧稿 replace 再公告 4 篇（2 A / 2 B，最高 4.15 NoPo4D 与 MEgoVista 并列），诚实标注非当日新提交。')
L.append('')
L.append('## 数据与过程')
L.append('')
L.append('- [7 维对比表](../daily/2026-10-24/7dim-table.md) · [评分明细](../daily/2026-10-24/scored.md) · [执行日志](../daily/2026-10-24/run_log.md)')
L.append('- [运行报告](../../reports/XR-Daily-Report-2026-10-24.md)')
L.append('- 数据源：API 双源探针 200；RSS 200（公告日 10-23，7 分类去重 643 条、关键词命中 33）→ RSS 主源 + listing 摘要级对账双通道互证。')
L.append('')
open('papers/MOC/MOC-2026-10-24.md', 'w', encoding='utf-8').write('\n'.join(L))

# ---------- MOC-backfill-1024 ----------
B = []
B.append('# MOC · backfill-1024（旧稿 replace 再公告补录）')
B.append('')
B.append('> **诚实口径**：本批为 10-23 公告批次中 RSS 混入的**旧稿 replace 再公告**（首次入馆），原始投稿月 2508 / 2601 / 2605 / 2609，公告日 2026-10-23、拉取日 2026-10-24，**非 10-24 当日新提交**。')
B.append('')
B.append('## 本批概览')
B.append('')
B.append('- 入馆 **4 篇**（A×2 / B×2 / C×0），registry 597 → 618 的组成部分；backfill 内部排序：NoPo4D 4.15 / MEgoVista 4.15 / SpatialMem 3.55 / MeSS 3.23。')
B.append('- 全文 **4 篇全部 L0/FULL**；门① 最大 Jaccard 0.109（与主批合并计算）；门③ 对 backfill 不适用。')
B.append('- 同批旧稿另 4 篇经甄别非 XR 剔除：2609.31777（心脏 MRI Rician 去噪）、2604.07993（HEX 人形全身操作）、2604.24033（事件相机 SLAM 基准，无人机高速机动）、2607.06768（AirPASS 6G 联邦学习）。')
B.append('')
B.append('## 补录清单')
B.append('')
B.append('| 论文 | 赛道 | 分值 | 等级 | 证据 | 原始投稿 | 笔记 |')
B.append('|---|---|---:|---|---|---|---|')
orig = {'2605.22190': '2026-05（2605）', '2609.16684': '2026-09（2609）', '2601.14895': '2026-01（2601）', '2508.15169': '2025-08（2508）'}
for r in bf_rows:
    B.append(f"| {r['title_zh']} | {r['track']} | {r['value']:.2f} | {r['grade']} | {r['evidence']} | {orig[r['id']]} | [→](../notes/{notefile(r['id'])}) |")
B.append('')
B.append('## 数据与过程')
B.append('')
B.append('- [7 维对比表](../daily/backfill-1024/7dim-table.md) · [执行日志](../daily/backfill-1024/run_log.md)')
B.append('- 甄别入口：RSS 10-23 公告批次 33 命中中 8 篇旧稿（2508/2601/2604/2605/2607/2609 前缀），XR 相关性甄别留 4 篇。')
B.append('')
open('papers/MOC/MOC-backfill-1024.md', 'w', encoding='utf-8').write('\n'.join(B))
print('MOCs written')

# ---------- 总索引刷新 ----------
p = 'papers/MOC/MOC-总索引.md'
t = open(p, encoding='utf-8').read()

# 1) 头部文献库计数与批次清单
t = t.replace('（累计 **597 篇**', '（累计 **618 篇**', 1)
t = t.replace('跨度 2026-09-15 ~ 2026-10-21', '跨度 2026-09-15 ~ 2026-10-22', 1)
t = t.replace('**backfill-1023:9（10-21 公告 listing 漏网 5 篇 + 旧稿 replace/cross 再公告 4 篇）**',
              '**backfill-1023:9（10-21 公告 listing 漏网 5 篇 + 旧稿 replace/cross 再公告 4 篇）** · **2026-10-24:17（10-23 公告批次真新提交，非重磅日无S；listing 摘要级对账补齐 RSS 漏网 5 篇）** · **backfill-1024:4（10-23 公告 RSS 混入旧稿 replace 再公告，首次入馆）**', 1)

# 2) 状态注记（插在 backfill-1023 注记之后、分隔线之前）
note = ('> **状态注记（2026-10-24）**：周六，处理 **2026-10-23（周五）公告批次**（提交日 10-16~10-22、周五 20:00 ET 释放；公告日≠拉取日，诚实口径）。listing 对账：10-22 组摘要级 9 篇命中全为 10-23 运行已剔除的非 XR（**0 漏网**）；10-23 组摘要级 23 篇命中 = RSS 15 + **RSS 漏网 8 篇**（5 篇 XR 相关经对账补齐：PiHand / VR 告别 / VR 漫播 / VecTile / IMU 定向）。RSS 7 分类去重 643 条 → KW 命中 33 → 去 registry(597) 后 31 新 = **17 篇真新 XR 相关**（甄别入池）+ 6 非 XR + 2 库内 v2 再公告 + 4 旧稿 replace（XR 相关 → backfill-1024）+ 2 旧稿 replace 非 XR。主批 17 篇 + backfill 4 篇全文全部 **L0/FULL**。Top10：**8 A + 2 B**，最高 **4.22**（EgoHand，加权已达 S 线，因当日为非重磅日按校准关记 A、分数如实保留）。三关通过（门① 0.109；门② 7 赛道；门③ 4.22 < 库近 30 天 Top10 均分 **4.416** 现算，447 条入窗，**非重磅日无 S 级**）、无重筛、无 OUTDATED。详见 [运行报告](../../reports/XR-Daily-Report-2026-10-24.md) 与 [MOC-2026-10-24](./MOC-2026-10-24.md)。\n'
        '> **状态注记（backfill-1024）**：周六，10-23 公告批次 RSS 混入的旧稿 replace 再公告 4 篇首次入馆（2 A / 2 B，最高 4.15 NoPo4D 与 MEgoVista 并列；原始投稿月 2508/2601/2605/2609），全文全 L0/FULL；门① 0.109（合并计算）、门③ 不适用；无重筛、无 OUTDATED。诚实口径：**非当日新提交**。详见 [MOC-backfill-1024](./MOC-backfill-1024.md)。\n')
anchor = '\n---\n\n## 一、速查入口'
t = t.replace(anchor, '\n' + note + anchor, 1)

# 3) 速查入口
t = t.replace('| 最新一期 | [MOC · 2026-10-23](./MOC-2026-10-23.md) |', '| 最新一期 | [MOC · 2026-10-24](./MOC-2026-10-24.md) |')
t = t.replace('| 上一期 | [MOC · 2026-10-22](./MOC-2026-10-22.md) |', '| 上一期 | [MOC · 2026-10-23](./MOC-2026-10-23.md) |')
t = t.replace('（现有 292 篇）', '（现有 313 篇）')
t = t.replace('| 最新运行状态 | [运行报告 2026-10-23](../../reports/XR-Daily-Report-2026-10-23.md)（10-22 公告批次 15 篇 + backfill-1023 9 篇；0 S / 8 A / 13 B / 3 C；非重磅日） |',
              '| 最新运行状态 | [运行报告 2026-10-24](../../reports/XR-Daily-Report-2026-10-24.md)（10-23 公告批次 17 篇 + backfill-1024 4 篇；0 S / 10 A / 11 B；非重磅日） |')

# 4) A 级新增段（插在 2026-10-21 新增段之后）
a_sec = ['\n### 2026-10-24 新增（A 级 8 篇 + B 级 2 篇，非重磅日）\n',
         '> 本期公告日 2026-10-23（拉取日 10-24 周六）；当日最高 4.22（EgoHand）< 库近 30 天 Top10 均分 4.416（现算），**非重磅日无 S 级**；EgoHand 加权 4.22 达 S 线，按校准关记 A（分数保留）。全文全 L0/FULL，三关通过，无 OUTDATED。\n',
         '\n| 论文 | 赛道 | 分值 | 日期 | 状态 | 笔记 |\n|---|---|---:|---|---|---|']
for r in top10:
    a_sec.append(f"| {r['title_zh']} | {r['track']} | {r['value']:.2f} | 10-23 | ✅ | [→](../notes/{notefile(r['id'])}) |")
a_sec.append('\n### backfill-1024 补录（2 A / 2 B，非当日新提交）\n')
a_sec.append('\n| 论文 | 赛道 | 分值 | 公告日 | 状态 | 笔记 |\n|---|---|---:|---|---|---|')
for r in bf_rows:
    a_sec.append(f"| {r['title_zh']} | {r['track']} | {r['value']:.2f} | 10-23 | ✅ | [→](../notes/{notefile(r['id'])}) |")
a_sec.append('')
a_sec_txt = '\n'.join(a_sec)
anchor2 = '\n### 2026-09-23 新增（A 级，10 篇，非重磅日）'
t = t.replace(anchor2, a_sec_txt + anchor2, 1)

# 5) 批次索引表补 2 行（backfill-1023 行之后）
row24 = '| 2026-10-24 | [MOC-2026-10-24](./MOC-2026-10-24.md) | XR 17（入选 10）· Top10 8A/2B · 非重磅日（无S） | 10-23 公告批次；listing 摘要级对账补齐 RSS 漏网 5 篇 |\n'
rowbf = '| backfill-1024 | [MOC-backfill-1024](./MOC-backfill-1024.md) | 补录 4（2A/2B）· 非当日新提交 | 10-23 公告 RSS 混入旧稿 replace 再公告 4 篇（2508/2601/2605/2609） |'
import re as _re
m = _re.search(r'(\| backfill-1023 \|[^\n]*\n)', t)
assert m, 'backfill-1023 row not found'
t = t.replace(m.group(1), m.group(1) + row24 + rowbf + '\n', 1)

# 6) 批次索引 Top10 段（插在 backfill-1023 段之后）
seg = ['\n### 2026-10-24 新增（Top10：8 A + 2 B，非重磅日无 S）\n',
       '\n| # | 论文 | 赛道 | 分值 | 等级 | 证据 |\n|---:|---|---|---:|---|---|']
for i, r in enumerate(top10, 1):
    seg.append(f"| {i} | {r['title_zh']} | {r['track']} | {r['value']:.2f} | {r['grade']} | {r['evidence']} |")
seg.append('\n### backfill-1024 补录（Top：2 A + 2 B，非当日新提交）\n')
seg.append('\n| # | 论文 | 赛道 | 分值 | 等级 | 证据 |\n|---:|---|---|---:|---|---|')
for i, r in enumerate(bf_rows, 1):
    seg.append(f"| {i} | {r['title_zh']} | {r['track']} | {r['value']:.2f} | {r['grade']} | {r['evidence']} |")
seg.append('')
seg_txt = '\n'.join(seg)
t = t.rstrip('\n') + '\n' + seg_txt

# 7) 页脚
t = t.replace('*最后更新：2026-10-23（10-22 公告批次 + backfill-1023） · 库内 **597 篇** · 原子笔记 **292 篇** · MOC 24 份',
              '*最后更新：2026-10-24（10-23 公告批次 + backfill-1024） · 库内 **618 篇** · 原子笔记 **313 篇** · MOC 26 份')
t = t.replace('registry 573→597（备份 registry.jsonl.bak-20261023，in_top10 校正 0 处）；路线观察新增 3 条（惯性里程计免真值自监督范式、稀疏视图 NeRF「修目标」线、3DGS 语义-几何联合压缩）*',
              'registry 573→597（备份 registry.jsonl.bak-20261023，in_top10 校正 0 处）；路线观察新增 3 条（惯性里程计免真值自监督范式、稀疏视图 NeRF「修目标」线、3DGS 语义-几何联合压缩）；10-24：registry 597→618（备份 registry.jsonl.bak-20261024，幂等追加 21 条），路线观察新增 3 条（免训练「冻结骨干+后处理/证据复用」范式收敛、第一视角手部重建双路线互补、社交 VR 实证转向空间配置与群体动力学）*')
open(p, 'w', encoding='utf-8').write(t)
print('MOC-总索引 refreshed')
print('notes total:', len(glob.glob('papers/notes/*.md')))
print('registry total:', sum(1 for l in open('papers/library/registry.jsonl', encoding='utf-8') if l.strip()))
