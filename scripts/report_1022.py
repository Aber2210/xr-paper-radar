# -*- coding: utf-8 -*-
# report_1022.py — 聚合 20 篇笔记生成 reports/XR-Daily-Report-2026-10-22.md
import json, re, os

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

def note_body(bid):
    p = f"{ROOT}/papers/notes/{bid}__{slug[bid]}.md"
    t = open(p, encoding='utf-8').read()
    t = re.sub(r'^---.*?---\n', '', t, flags=re.S)  # 去 frontmatter
    return t.strip()

L = []
L.append('# XR 每日论文解读报告 · 2026-10-22')
L.append('')
L.append('> **公告窗口**：2026-10-21（周三）公告批次（提交日 10-16~10-20、周三 20:00 ET 释放）；**拉取日**：2026-10-22（周四 02:30）。')
L.append('> **诚实口径**：本批处理 10-21 公告批次的真新提交（2610.* 前缀甄别：27 new + 12 cross），**非当日（10-22）新提交**；公告日≠拉取日已显式标注。RSS 混入的 5 篇 replace 旧稿均经甄别为非 XR，**无 backfill**；4 篇库内 v2 再公告（SwitchSplat / Stable Signer V3 / HumanSkill-4D / Thinker-WM）已剔除。')
L.append('')
L.append('## 一、执行摘要')
L.append('')
L.append('- **入馆 20 篇**（S×0 / A×12 / B×6 / C×2），registry 553 → **573**；Top10 全 A 级、最高 **4.00**（三篇并列）。')
L.append('- **非重磅日**：当日最高 4.00 < 库内近 30 天 Top10 均分 **4.416**（现算，窗口 2026-09-22~10-22、424 条入窗）→ 无 S 级，未拔高。')
L.append('- 全文证据：21 篇候选（含后剔除 1 篇非 XR）**全部 L0/FULL**（26,524–130,608 字符），串行 3s/篇，无限流/降级/伪造。')
L.append('- 覆盖度三关全过：门① 最大 Jaccard **0.096**（<0.62）；门② Top10 覆盖 **5 赛道**；门③ 见上。**未触发重筛**，OUTDATED/SUPERSEDED **0 篇**。')
L.append('- 本批结构性看点：① 3DGS 压缩首次走到**编解码器兼容**（CCT-GS，SH-AC 属性图入标准视频编码管线 + LoRA 场景适配，BD-rate -51.3%）；② 单图高斯头部 enrollment 质量跃升（EGGHead，LPIPS 0.017 vs 基线 0.110）；③ 注视点意图消歧进入 HOI 预测（Gaze2HOI，HO-Pen 1.70 vs 10.20）；④ 多智能体世界模型一致性（OverSeer，固定辅助视图代理世界状态）；⑤ 「视频生成 × 显式 4DGS」统一世界模型同日双路线（AEON / EgoACT）。')
L.append('- 上游对账：listing 7 分类最新公告日 10-21；10-20 日组 936 篇 + 10-21 日组 532 篇全量对账；摘要级 XR 过滤两渠道完全互证（10-20 组 32 篇与上批互证为非 XR、**0 漏网**；10-21 组 39 篇与 RSS 一致）。')
L.append('')
L.append('## 二、Top10 排行榜')
L.append('')
L.append('| 排名 | 论文 | 赛道 | 总分 | 等级 | 证据 |')
L.append('|---:|---|---|---:|---|---|')
for i, d in enumerate(top10, 1):
    L.append(f"| {i} | {d['title_zh']} | {d['track']} | {d['value']:.2f} | {d['grade']} | {d['evidence']} |")
L.append('')
L.append('> 同分排序规则：加权降序 → IMP/NOV 降序 → 赛道多样性优先 → id 升序。三篇 4.00 并列（EGGHead / CCT-GS / Gaze2HOI）。')
L.append('')
L.append('## 三、逐篇深度解读（按重要性降序）')
L.append('')
for i, d in enumerate(top10, 1):
    bid = d['id'].split(':')[-1]
    L.append(f'### 第 {i} 章 · {d["title_zh"]}（{d["value"]:.2f} {d["grade"]} · {d["track"]} · {d["evidence"]}）')
    L.append('')
    L.append(note_body(bid))
    L.append('')
L.append('## 四、当日全量 7 维度对比表（参考）')
L.append('')
L.append('> 20 篇入馆全量（含非 Top10）；权重 IMP0.20·NOV0.20·TEC0.15·EXP0.15·PER0.15·TRL0.08·REP0.07；分档 S≥4.2 / A3.6–4.2 / B3.0–3.6 / C<3.0。')
L.append('')
L.append('| arXiv | 标题 | 赛道 | IMP | NOV | TEC | EXP | PER | TRL | REP | 总分 | 等级 | 证据 | 公告类型 |')
L.append('|---|---|---|---|---|---|---|---|---|---|---|---|---|---|')
for d in sorted(items, key=lambda x: -x['value']):
    s = d['scores']
    L.append(f"| {d['id'].split(':')[-1]} | {d['title_zh']} | {d['track']} | {s['IMP']} | {s['NOV']} | {s['TEC']} | {s['EXP']} | {s['PER']} | {s['TRL']} | {s['REP']} | {d['value']:.2f} | {d['grade']} | {d['evidence']} | {d.get('announce_type','new')} |")
L.append('')
L.append('## 五、覆盖率校验与筛选过程说明')
L.append('')
L.append('### 5.1 覆盖度三关')
L.append('')
L.append('- **门①（同质去重）**：当日 20 篇 vs 全库（非本批）标题+摘要 token Jaccard，最大 **0.096**（2610.26898 vs 库内 2610.17513），0.45~0.62 区间 0 篇 → **通过**，无同质重复。')
L.append('- **门②（赛道覆盖）**：Top10 覆盖 **5 赛道**（化身与人体 / 渲染与显示 / 神经渲染 / 感知与认知 / 世界模型与仿真）≥5 → **通过**；全批 20 篇覆盖 **10 赛道**（另含触觉与多模态、内容生成、重建与SLAM、空间计算与UI、评估与数据集）。')
L.append('- **门③（价值天花板，校准关）**：当日最高 4.00 < 库内近 30 天 Top10 均分 **4.416**（现算：窗口 2026-09-22~10-22，registry 424 条入窗，按 value 降序前 10 为 4.65 / 4.58 / 4.57 / 4.57 / 4.37 / 4.30 / 4.30 / 4.28 / 4.27 / 4.27）→ **非重磅日、无 S 级**；门③为校准关，不触发重筛。')
L.append('')
L.append('### 5.2 漏斗与甄别')
L.append('')
L.append('```')
L.append('listing 对账（TARGET_LO=10-20）：10-20 组 936 篇 + 10-21 组 532 篇')
L.append('  → 摘要级 XR 过滤：10-20 组 32 篇（与上批互证，0 漏网）+ 10-21 组 39 篇')
L.append('RSS 拉取：7 分类去重 795 条 → 关键词命中 48')
L.append('  → 去 registry(553)：44 新 = 27 new + 12 cross + 5 replace；另 4 篇库内 v2 再公告')
L.append('  → 真新 39 篇甄别：21 篇 XR 入池（4 篇边界纳入：CityPaint/World2HOSI/StreamEval/OverSeer）+ 18 篇非 XR 剔除')
L.append('  → replace 旧稿 5 篇均非 XR → 无 backfill')
L.append('全文：21 候选全 L0/FULL（26,524–130,608 字符）')
L.append('评分：20 篇入馆（A12/B6/C2），Top10 = 前 10 名（全 A）')
L.append('```')
L.append('')
L.append('### 5.3 剔除原因分布（24 篇未入馆）')
L.append('')
L.append('- 非 XR 18 篇：LLM×5、机器人与人形×6、UAV 定位、自动驾驶协同感知（CoGaussian，OPV2V）、视频时序定位、可微相机设计、动物行为、人机协作研究、dashcam 车道评估、工业热场重建（GTSM）。')
L.append('- replace 旧稿 5 篇均非 XR；库内 v2 再公告 4 篇。')
L.append('')
L.append('## 六、附录')
L.append('')
L.append('### 6.1 抓取失败/降级清单')
L.append('')
L.append('- **无**。21 篇候选全部 L0（arXiv HTML）一次链路命中、FULL 证据；无限流（429/503）、无 L1–L5 降级、无伪造。')
L.append('')
L.append('### 6.2 证据等级分布')
L.append('')
L.append('| 证据等级 | 篇数 | 说明 |')
L.append('|---|---:|---|')
L.append('| FULL（L0） | 20 | 入馆 20 篇全部；另 1 篇（CoGaussian）抓取后甄别剔除 |')
L.append('| PARTIAL | 0 | — |')
L.append('| ABSTRACT_ONLY | 0 | — |')
L.append('')
L.append('### 6.3 产物清单')
L.append('')
L.append('- 7 维表 / 评分明细 / 运行日志：`papers/daily/2026-10-22/`')
L.append('- 原子笔记 20 篇：`papers/notes/2610.*__*.md`')
L.append('- 当日 MOC：`papers/MOC/MOC-2026-10-22.md`；总索引已刷新（573 篇 / 268 笔记 / 25 批次）')
L.append('- 文献库：`papers/library/registry.jsonl`（553→573，备份 `registry.jsonl.bak-20261022`）')
L.append('- 前端：`web/xr-paper-hub.html` 已重建（DATA 573/268/25 与磁盘一致）')
L.append('')
open(f'{ROOT}/reports/XR-Daily-Report-2026-10-22.md', 'w', encoding='utf-8').write('\n'.join(L))
print('written report, chapters:', len(top10))
