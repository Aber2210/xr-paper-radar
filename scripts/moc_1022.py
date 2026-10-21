# -*- coding: utf-8 -*-
# moc_1022.py — 生成 MOC-2026-10-22.md（从 registry + content slug 渲染）
import json

ROOT = 'D:/Agent/WorkBuddy/Research'
reg = {}
for l in open(f'{ROOT}/papers/library/registry.jsonl', encoding='utf-8'):
    if l.strip():
        d = json.loads(l)
        reg[d['id'].split(':')[-1].split('v')[0]] = d
slug = {}
for g in (1, 2, 3, 4):
    for x in json.load(open(f'{ROOT}/data/notes_content_1022_g{g}.json', encoding='utf-8')):
        slug[x['id']] = x['slug']
items = [d for d in reg.values() if d.get('batch') == '2026-10-22']
top10 = sorted([d for d in items if d['in_top10']], key=lambda d: -d['value'])
rest = sorted([d for d in items if not d['in_top10']], key=lambda d: -d['value'])
tracks_top = sorted({d['track'] for d in top10})
tracks_all = sorted({d['track'] for d in items})

L = ['# MOC · 2026-10-22（主批次）', '',
     '> **公告窗口**：2026-10-21（周三）公告批次（提交日 10-16~10-20、周三 20:00 ET 释放）；**拉取日**：2026-10-22（周四）。',
     '> **诚实口径**：本批处理 10-21 公告批次的真新提交（2610.* 前缀甄别，27 new + 12 cross），**非当日（10-22）新提交**（公告日≠拉取日）；RSS 混入的 5 篇 replace 旧稿均非 XR，**无 backfill 候选**；4 篇库内 v2 再公告已剔除。', '',
     '## 本批概览', '',
     '- 入馆 **20 篇**（S×0 / A×12 / B×6 / C×2——Top10 全 A 级，无 S 级），registry 553 → **573**；本批无 backfill。',
     '- 全文 **21 篇候选全部 L0/FULL**（26,524–130,608 字符；含后甄别剔除的 1 篇非 XR），串行 3s/篇，无限流/降级/伪造。',
     f'- Top10：**10 篇全 A 级**，最高 4.00（EGGHead / CCT-GS / Gaze2HOI 三篇并列），覆盖 **{len(tracks_top)} 赛道**（{" / ".join(tracks_top)}）。',
     '- 覆盖度三关：门① 最大 Jaccard **0.096**（2610.26898 vs 库内 2610.17513，<0.62 通过，无同质）；门② Top10 覆盖 **5 赛道**（≥5 通过，全批 20 篇覆盖 10 赛道）；门③ 当日最高 **4.00 < 库内近 30 天 Top10 均分 4.416**（现算，窗口 2026-09-22~10-22 共 424 条入窗，差值 -0.416）→ **非重磅日，无 S 级，未拔高**。三关全过、**未触发重筛**。',
     '- OUTDATED/SUPERSEDED：**0 篇**；路线观察 3 条（3DGS 压缩走向编解码器兼容的标准视频编码管线；世界模型「视频生成 × 显式 4DGS」双路线同日竞合——AEON 与 EgoACT；在线场景变化检测「证据模型可学习化」——O-SCD++ 的直接后续竞品）。',
     '- 上游对账：listing 7 分类最新公告日 10-21；10-20 日组 936 篇 + 10-21 日组 532 篇全量对账，摘要级 XR 过滤两渠道完全互证（10-20 组 32 篇全部与 10-21 运行互证为非 XR，0 漏网；10-21 组 39 篇与 RSS 真新集合一致）。',
     '', '## Top10（按加权降序，同分按 IMP/NOV → 赛道多样性 → id 升序）', '',
     '| 排名 | 论文 | 赛道 | 分值 | 等级 | 证据 | 笔记 |',
     '|---:|---|---|---:|---|---|---|']
for i, d in enumerate(top10, 1):
    L.append(f"| {i} | {d['title_zh']} | {d['track']} | {d['value']:.2f} | {d['grade']} | {d['evidence']} | [→](../notes/{d['id'].split(':')[-1]}__{slug[d['id'].split(':')[-1]]}.md) |")
L += ['', f'## 其余入馆（{len(rest)} 篇）', '',
      '| 论文 | 赛道 | 分值 | 等级 | 证据 | 笔记 |',
      '|---|---|---:|---|---|---|']
for d in rest:
    L.append(f"| {d['title_zh']} | {d['track']} | {d['value']:.2f} | {d['grade']} | {d['evidence']} | [→](../notes/{d['id'].split(':')[-1]}__{slug[d['id'].split(':')[-1]]}.md) |")
L += ['', '## 本批剔除（公告窗口内不入馆）', '',
      '- 非 XR 18 篇：LLM×5（BitMTP/Large Flow/扩散语言模型事实访问/ProMemAgent/掩码扩散遗忘）、机器人与人形×6（UMI 手套数据采集/LocoPilot 遥操作/MAPLE 室内探索/CLOSER 物体目标导航/SceneRig 机器人仿真/VLM 接触重定向）、MatchCityLoc（UAV 定位）、CoGaussian（自动驾驶协同感知 OPV2V）、SuperClip（视频时序定位）、可微编码孔径相机设计、动物短期运动表征、人机协作主导权研究、dashcam 车道质量评估、GTSM（工业热场重建）。',
      '- replace 旧稿再公告 5 篇均非 XR（NeoWorld-Pro 具昧场景编程/SonoWorld 超声世界模型/PnP-Transformer 6D 位姿/PAKE 全身运动操作/地面机器人 VIO）→ 无 backfill。',
      '- 库内 v2 再公告 4 篇（SwitchSplat/Stable Signer V3/HumanSkill-4D/Thinker-WM）。逐篇清单见 [scored.md](../daily/2026-10-22/scored.md)。',
      '', '## 数据与过程', '',
      '- [7 维对比表](../daily/2026-10-22/7dim-table.md) · [评分明细](../daily/2026-10-22/scored.md) · [执行日志](../daily/2026-10-22/run_log.md)',
      '- [运行报告](../../reports/XR-Daily-Report-2026-10-22.md)',
      '- 数据源：API 双源探针 200；RSS cs.CV 287 / cs.AI 473 条（公告日 10-21）→ RSS 兜底，7 分类去重 795 条、关键词命中 48。',
      '']
open(f'{ROOT}/papers/MOC/MOC-2026-10-22.md', 'w', encoding='utf-8').write('\n'.join(L))
print('written MOC-2026-10-22.md, top10:', len(top10), 'rest:', len(rest))
