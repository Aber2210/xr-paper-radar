# -*- coding: utf-8 -*-
# report_1021.py — 生成 reports/XR-Daily-Report-2026-10-21.md（Top10 逐篇深度解读 + 7 维参考表 + 覆盖校验 + backfill 专章 + 附录）。
import json

ROOT = 'D:/Agent/WorkBuddy/Research'

reg = {}
for l in open(f'{ROOT}/papers/library/registry.jsonl', encoding='utf-8'):
    if l.strip():
        d = json.loads(l)
        reg[d['id'].split(':')[-1].split('v')[0]] = d

C = {}
for g in (1, 2, 3, 4):
    for x in json.load(open(f'{ROOT}/data/notes_content_1021_g{g}.json', encoding='utf-8')):
        C[x['id']] = x

TOP10 = ['2610.24462', '2610.24812', '2610.24926', '2610.26583', '2610.26625',
         '2610.26780', '2610.24400', '2610.26067', '2610.24031', '2610.24285']
BF = ['2512.19283', '2606.05102', '2609.03892', '2504.20829', '2605.17661',
      '2606.25430', '2511.09397', '2605.10760', '2603.24591', '2606.16881']

R = []
R.append('# XR 每日论文雷达 · 运行报告 2026-10-21')
R.append('')
R.append('> **公告窗口**：2026-10-20（周二）公告批次（09-28~10-19 提交、周二 10-20 20:00 ET 释放）；**拉取日**：2026-10-21（周三）。')
R.append('> **诚实口径**：本批处理 10-20 公告批次的**真新提交**（2610.* 前缀甄别）——**公告日≠拉取日**（周二公告、周三拉取），非当日（10-21）新提交。另单列 **backfill-1021**（RSS 旧稿 replace/cross 再公告 10 篇，2504~2609 原始提交首次入馆），未混入主批 Top10。')
R.append('')
R.append('---')
R.append('')
R.append('## 一、执行摘要')
R.append('')
R.append('- **数据源与对账（第 1–3 步）**：listing 7 分类最新公告日 = **2026-10-20（周二）**（10-17/10-18 周末无公告）；10-20 日组 936 篇全部入账（无调度恢复后最大公告日），10-19 日组 373 篇中 361 篇不在库（摘要级命中 7 篇全部非 XR，与 10-20 运行互证，无新增漏网）。探针四源全 200（RSS cs.CV 505 条、cs.AI 789 条，双频道均非空——不同于 10-20 运行的 cs.AI 真空源）。')
R.append('- **拉取与甄别**：RSS 7 分类去重 1426 条 → 关键词命中 91 条 → 去 registry(512) 后 **67 篇 2610.* 真新提交**（甄别 **31 篇 XR 核心/强相关**入评分池，36 篇非 XR 剔除）+ 20 篇旧稿 replace/cross（10 篇 XR 入 backfill-1021）+ 4 篇库内 v2 再公告剔除。listing×RSS 交叉验证：listing API 摘要级过滤命中 63 篇与 RSS 通道完全互证（RSS 为超集）。')
R.append('- **全文抓取**：主批 31 篇 + backfill 10 篇共 41 篇候选，**40 篇 L0/FULL**（26,060–141,031 字符）+ **1 篇 PARTIAL**（2610.26549 Holi-World：L0 HTML 404、ar5iv 仅返摘要页 5177 字符，按摘要级评估并显式声明，禁止脑补正文）；串行 3s/篇，无限流/降级/伪造。')
R.append('- **评分与 Top10**：主批入馆 **31 篇（S×0 / A×11 / B×15 / C×5）**；Top10 **10 篇全 A 级**（无 S 级），最高 **3.85**（O-SCD++ / SwitchSplat / Stable Signer V3 / DenseHap / EgoXperience / V-JEPA Hand 六篇并列）。')
R.append('- **覆盖度三关**：门① 最大 Jaccard **0.143**（2610.24285 vs 库内 2609.22332，<0.62 通过）；门② Top10 覆盖 **5 赛道**（感知与认知×3、化身与人体×3、触觉与多模态×2、神经渲染×1、渲染与显示×1，≥5 通过）；门③ 当日最高 **3.85 < 库内近 30 天 Top10 均分 4.416**（现算，差值 -0.566）→ **非重磅日，无 S 级，未拔高**。')
R.append('- **重要发现**：')
R.append('  1. **第一视角手-物感知成簇**——EgoXperience（共享世界系联合输出相机+深度+双手+物体 6-DoF）、V-JEPA Hand（单次前馈恢复双手 MANO+相机轨迹）、DenseHap（单目稠密手部触觉）三篇同批入馆，第一视角手部感知从单任务估计走向「联合重建 + 触觉扩展」；与库内 EgoP²C/ReViV/ESTHER/Hand-4DGS 构成连续簇；')
R.append('  2. **前馈 3DGS 效率线再添两条**——backfill 的 ZipSplat（62K 高斯 25.34 PSNR，token 解码）与主批 FineSplat（4×4 细粒度 patch 双分组）从「表示压缩」两侧挤压 per-pixel 基线，与库内 pixel-aligned 族（MVSplat/DepthSplat/DA3）构成效率竞合；SwitchSplat 则开辟「离散物体状态」这一新表示维度；')
R.append('  3. **XR 显示预畸变补偿新范式**——Spatons 用空-色调局部化神经算子做预畸变（G-Res 混合几何畸变场景 PSNR 37.5 dB），与库内 CompenNet++ 等经典补偿网络构成不同范式对照，补库内渲染与显示硬件侧空白。')
R.append('')
R.append('---')
R.append('')
R.append('## 二、Top10 排行榜')
R.append('')
R.append('| 排名 | 论文 | 赛道 | 总分 | 等级 | 证据 |')
R.append('|---:|---|---|---:|---|---|---|')
for i, pid in enumerate(TOP10, 1):
    d = reg[pid]
    ev = d['evidence'] + ('' if d['evidence'] == 'FULL' else '/' + d['fetch_level'])
    R.append(f"| {i} | {d['title_zh']} | {d['track']} | {d['value']:.2f} | {d['grade']} | {ev} |")
R.append('')
R.append('Top10 均分 3.79；全部 CURRENT，无 OUTDATED/SUPERSEDED。同分排序规则：加权降序 →（value/IMP/NOV 全同组内）赛道多样性优先 → id 升序（六篇 3.85 并列、ACTS 与 EgoRayFormer 3.63 并列均按此裁决，见第五节）。')
R.append('')
R.append('---')
R.append('')
R.append('## 三、逐篇深度解读（按重要性降序）')
R.append('')
for i, pid in enumerate(TOP10, 1):
    d = reg[pid]
    c = C[pid]
    R.append(f"### 第 {i} 章 · {d['title_zh']}（{d['value']:.2f} {d['grade']}）")
    R.append('')
    R.append(f"**一句话结论**：{c['conclusion']}")
    R.append('')
    R.append(f"**要解决的问题**：{c['problem']}")
    R.append('')
    R.append(f"**方法详解**：{c['method']}")
    R.append('')
    R.append(f"**实验与结果**：{c['experiments']}")
    R.append('')
    R.append(f"**创新点**：{c['innovation']}")
    R.append('')
    R.append(f"**局限**：{c['limits']}")
    R.append('')
    R.append(f"**与库内关系**：{c['relation']}")
    R.append('')
R.append('---')
R.append('')
R.append('## 四、当日全量 7 维度对比表（31 篇入馆）')
R.append('')
R.append('见 [papers/daily/2026-10-21/7dim-table.md](../papers/daily/2026-10-21/7dim-table.md)（含 IMP/NOV/TEC/EXP/PER/TRL/REP 分明细、总分、等级与证据列）。分布：S×0 / A×11 / B×15 / C×5；除 Holi-World（2610.26549，PARTIAL/L1 摘要级）外全部 L0/FULL。')
R.append('')
R.append('---')
R.append('')
R.append('## 五、覆盖率校验与筛选过程说明')
R.append('')
R.append('**候选来源**：RSS 7 分类去重 1426 条 → KW 双层过滤（全称子串 + 缩写词边界）命中 91 → 去 registry(512) 后 67 新 = 67 篇真新提交 + 20 篇旧稿 replace/cross + 4 篇库内 v2 再公告；67 篇真新中 31 篇 XR 入池。公告窗口内剔除 36 篇非 XR/弱相关：医学×3（MRI 超分/动脉瘤分割/胶质瘤合成）、自动驾驶×2、机器人×20+（灵巧操作/导航/规划/动捕/人形）、无人机×2、通用视频生成×3、通用具身/NLP/气象/几何/推荐系统等。listing 对账（10-20 日组 936 篇 API 摘要级过滤命中 63 篇）与 RSS 通道完全互证；10-19 日组摘要级命中 7 篇全部非 XR（与 10-20 运行结论一致）。')
R.append('')
R.append('**三关结果**：')
R.append('- 门① 同质去重：最高 Jaccard **0.143**（2610.24285 ACTS vs 库内 2609.22332）→ **通过，无重筛**。')
R.append('- 门② 赛道覆盖：Top10 覆盖 **5 赛道**（感知与认知×3、化身与人体×3、触觉与多模态×2、神经渲染×1、渲染与显示×1）→ **通过**；全批 31 篇覆盖 12 赛道。')
R.append('- 门③ 价值天花板：库内近 30 天（date≥2026-09-21）Top10 均分 = **4.416**（现算：2610.03162 4.65 / 2610.03283 4.58 / 2610.19674 4.57 / 2610.23772 4.57 / 2609.34367 4.37 / 2610.18872 4.3 / 2610.22778 4.3 / 2610.03192 4.28 / 2609.34817 4.27 / 2610.17474 4.27）；当日最高 **3.85** → 差值 -0.566，**非重磅日，无 S 级，未拔高**。')
R.append('')
R.append('**筛选过程修正记录**：本批评分基于全文证据定稿（先抓全文再定稿）。① 六篇 3.85 并列（IMP/NOV 全同）按赛道多样性优先裁决入场顺序，感知与认知以 3 篇封顶 Top10（O-SCD++/EgoXperience/V-JEPA Hand），EgoRayFormer（3.63，同分第四席感知与认知）让位 ACTS（触觉与多模态）；② Holi-World 因全文获取失败（L0 HTML 404、ar5iv 仅返摘要页）按摘要级评估定 3.20 B，并在 7 维表/scored/笔记三处显式标注 PARTIAL，未脑补正文；③ 36 篇剔除中机器人域占比最高（20+ 篇），反映 10-20 公告日机器人论文泛滥，与既往口径一致（纯机器人域不纳入 XR 文献库）。')
R.append('')
R.append('---')
R.append('')
R.append('## 六、backfill-1021 专章（10 篇：4 A / 5 B / 1 C，非当日新提交）')
R.append('')
R.append('**来源与诚实口径**：RSS 旧稿 replace/cross 再公告 20 篇（2504~2609 原始提交）中甄别 10 篇 XR 相关首次入馆；其余 10 篇非 XR 剔除（人形控制/自动驾驶/视频可操作神经函数/多机器人空间推理/人形世界模型/机器人意图跟随/零样本智能体/NLP/高光谱超分）。**全部非当日新提交，单列 backfill-1021，未混入主批 Top10**。')
R.append('')
R.append('**排行**（按加权降序）：OmniEgoCap 3.85 A（设备无关序列级第一视角动作重建，扩散框架+8×A5000 16h）· ZipSplat 3.85 A（62K 高斯 25.34 PSNR，比 per-pixel 基线高约 2dB）· GraFT 3.85 A（免训练 3D 场景图 MLLM 空间推理，GPT-o3 VSI-Bench +5.9）· GaussTrap 3.72 A（KDD 2026，3DGS 隐蔽后门攻击）· Mono-Hydra++ 3.45 B（ISPRS JPRS，单目实时场景图 ATE 6.91cm）· PRISM 3.43 B（扩散蒸馏为前馈单图重建）· OUGS 3.43 B（FIM+EMA 不确定性驱动主动视角选择）· MAGS-SLAM 3.08 B（单目多智能体 GS SLAM）· Vibe Coding XR 3.00 B（XR Blocks+Gemini 原型工具链）· SGM-SLAM 2.93 C（场景图匹配分布式 SLAM，感知消息压缩 65×）。')
R.append('')
R.append('**覆盖三关**：门① max Jaccard **0.133**（通过）；门② 覆盖 **4 赛道**（感知与认知×2、神经渲染×4、重建与SLAM×3、空间计算与UI；backfill 为机会性补录，不适用 Top10 选拔）；门③ 不适用。无重筛、无 OUTDATED。全文 10 篇全部 L0/FULL。')
R.append('')
R.append('**关键互证**：① ZipSplat × FineSplat × 库内 pixel-aligned 族——前馈 3DGS「token 粒度/基元数量」效率竞合三线；② Mono-Hydra++ × SGM-SLAM——「场景图建图-通信」互补对，与库内 OpenSplatGraph 同属 3D 高斯语义场景图线；③ GraFT × 库内 SpatialMind——「免训练 vs 微调」MLLM 空间推理对照；④ GaussTrap 开库内 3DGS 安全视角；⑤ OmniEgoCap × 库内 EgoWholeView/OmniPoser/ESTHER——第一视角动作重建族新变体。')
R.append('')
R.append('详见 [MOC-backfill-1021](../papers/MOC/MOC-backfill-1021.md)。')
R.append('')
R.append('---')
R.append('')
R.append('## 七、附录')
R.append('')
R.append('**证据等级分布**：主批 31 篇 = **30 篇 FULL**（L0，26,060–141,031 字符）+ **1 篇 PARTIAL/L1**（2610.26549 Holi-World，L0 HTML 404、ar5iv 仅返摘要页 5177 字符，按摘要级评估）；backfill 10 篇全部 FULL（L0）。')
R.append('')
R.append('**抓取失败/降级清单**：仅 Holi-World 一篇降级（上述），手动重试 L0 HTML 确认 404 后按摘要级评估并三处显式标注；无限流封禁、无伪造；manifest 合并写入校验通过。XRT（2610.24257）digest 提取不完整（LaTeXML 样板），其笔记改用 arXiv 官方摘要补全并在 limits 中如实说明。')
R.append('')
R.append('**诚实口径声明**：本批公告窗口 2026-10-20（周二释放，09-28~10-19 提交），拉取日 2026-10-21——**公告日≠拉取日**；backfill-1021 为旧稿 replace/cross 再公告补录（原始提交 2025-04 ~ 2026-09），非当日新提交。所有 registry 条目带 `batch=2026-10-21` / `batch=backfill-1021` 与 `orig_window` 字段，backfill 条目 flags 含 `BACKFILL`。')
R.append('')
R.append('**产物清单**：本报告 + [当日 MOC](../papers/MOC/MOC-2026-10-21.md) + [backfill MOC](../papers/MOC/MOC-backfill-1021.md) + 原子笔记 41 篇（主批 31 + backfill 10）+ [主批 7 维表](../papers/daily/2026-10-21/7dim-table.md) + [主批评分明细](../papers/daily/2026-10-21/scored.md) + [执行日志](../papers/daily/2026-10-21/run_log.md) + [backfill 7 维表](../papers/daily/backfill-1021/7dim-table.md) + [backfill 评分明细](../papers/daily/backfill-1021/scored.md) + registry 追加 41 条（512→553，备份 `registry.jsonl.bak-20261021`；另 `registry.jsonl.bak-20261021b` 为 in_top10 修正前备份）+ [MOC 总索引刷新](../papers/MOC/MOC-总索引.md)。')
R.append('')

open(f'{ROOT}/reports/XR-Daily-Report-2026-10-21.md', 'w', encoding='utf-8').write('\n'.join(R))
print('report written, lines:', len(R))
