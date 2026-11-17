# -*- coding: utf-8 -*-
"""2026-11-17 报告生成：主批 Top10 深度解读 + backfill-1117 报告。"""
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from grade_caliber import assign_grade  # noqa: E402  档位口径单一实现

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
os.chdir(ROOT)
D = json.load(open('data/scored_1117.json', encoding='utf-8'))
MAIN = [p for p in D if p['batch'] == '2026-11-17']
BF = [p for p in D if p['batch'] == 'backfill-1117']
MAIN.sort(key=lambda r: (-r['value'], -r['scores']['IMP'], -r['scores']['NOV'], r['id']))
G = json.load(open('data/gates_1117.json', encoding='utf-8'))
TOP10_ORDER = G['top10']
DATE, ANN = '2026-11-17', '2026-11-16'
GATE3, G1 = G['gate3']['top10_mean'], G['gate1']['max_jaccard']
HEAVY = bool(G['gate3']['heavy_day'])
MANIFEST = json.load(open('data/fulltext/_manifest.json', encoding='utf-8'))
for p in MAIN + BF:
    p['level'] = MANIFEST[p['id']]['level']
    p['evidence'] = MANIFEST[p['id']]['evidence']
    p['announce'] = 'replace' if p['batch'].startswith('backfill') else 'new'
    p['status'] = 'CURRENT'
    v = p['value']
    # 档位口径（README 与门③ 一致）：S 需「分数 ≥4.20 且当日为重磅日」。实现在
    # grade_caliber.assign_grade，与 7 维表/笔记/registry 共用，避免同批不同档。
    p['grade'] = assign_grade(v, p['batch'], HEAVY)
TOP10 = [next(p for p in MAIN if p['id'] == pid) for pid in TOP10_ORDER]


def esc(s):
    return str(s).replace('|', '/')


def report(papers, path, title, header, gate_lines, appendix):
    L = [f'# {title}\n', header + '\n', '## 二、排行榜（按加权降序）\n',
         '| 排名 | 论文 | 赛道 | 总分 | 等级 | 证据 | 落后标记 |', '|---|---|---|---|---|---|---|']
    for i, p in enumerate(papers, 1):
        mark = '⛔ OUTDATED' if p['status'] != 'CURRENT' else '—'
        L.append(f"| {i} | {esc(p['title_zh'])}（{p['id']}） | {p['track']} | {p['value']:.2f} | "
                 f"{p['grade']} | {p['evidence']} | {mark} |")
    L.append('\n## 三、逐篇深度解读\n')
    for i, p in enumerate(papers, 1):
        L.append(f"### 第 {i} 章 · {esc(p['title_zh'])}（{p['id']}，{p['value']:.2f} {p['grade']}，{p['evidence']}）\n")
        L.append(f"- **赛道 / 场合**：{p['track']} / {p['venue']}")
        L.append(f"- **公告类型**：{p['announce']}（公告日 2026-11-16，拉取日 2026-11-17；提交日 {p['published']}）")
        if p['evidence'] == 'PARTIAL':
            L.append('- **证据等级说明**：本篇 `PARTIAL`——arXiv HTML 404、ar5iv 仅返回摘要页，'
                     '正文不可得，以下内容仅基于摘要与元数据，具体数值已标注「（摘要仅述，未在正文核实）」。')
        L.append(f"- **一句话结论**：{p['conclusion']}")
        L.append(f"- **要解决的问题**：{p['problem']}")
        L.append(f"- **方法详解**：{p['method']}")
        L.append('- **实验与结果**：')
        for x in p['experiments']:
            L.append(f"    - {x}")
        L.append('- **创新点与贡献**：')
        for x in p['innovation']:
            L.append(f"    - {x}")
        L.append('- **局限与风险**：')
        for x in p['limits']:
            L.append(f"    - {x}")
        L.append(f"- **与文献库的关系**：{p['relation']}")
        L.append(f"- **可复现性**：{p['repro']}")
        L.append(f"- **行动建议**：{p['action']}\n")
    L.append('## 四、当日全量 7 维度对比表（参考）\n')
    L.append(f'见 [`papers/daily/{DATE}/7dim-table.md`](../papers/daily/{DATE}/7dim-table.md)。\n')
    L.append('## 五、覆盖率校验与筛选过程说明\n')
    L += gate_lines
    L.append('\n## 六、附录\n')
    L += appendix
    open(path, 'w', encoding='utf-8').writelines([x + '\n' for x in L])


HEADER = (
    '## 一、执行摘要\n'
    '- **公告日 2026-11-16（周一）≠ 拉取日 2026-11-17（周二 02:30）**——诚实口径。'
    '周末 11-14（周六）/ 11-15（周日）无公告日段（`skipDays` 节律），两日提交积压于**周一 00:00 UTC = 08:00 北京时间**统一释放，'
    '构成 listing 的 11-16 日组；API published 核验主批提交日 **11-13×12 / 11-12×1**（RSS published 是公告时间戳，不可当提交日）。'
    '11-16（周一）02:30 的运行早于该时刻，故为状态日；本批是新一周首个真实批次。\n'
    '- **漏网对账（先于拉取）**：`scripts/audit_listing_1117.py` 显示 7 分类最新公告日均为 11-16、无 11-14/11-15/11-17 日组；'
    '11-13 组复采逐分类 **declared=got**（695 槽位 / 601 唯一），未入馆 **581 篇与 11-16 运行集合 581/581 逐篇一致** → **0 漏网**。\n'
    '- **数据源**：API 双主机 200（仅用于提交日核验，单批 16 id 返回 16/16）；RSS 7 分类 `--no-filter` 去重 **435 条** = '
    '**189 new + 82 cross + 164 replace**；**listing 271 篇 100% 被 RSS 覆盖（RSS 缺收 0 篇）**，故摘要级过滤直接用 RSS 全摘要'
    '（清单见 `scripts/triage_1117.py`），规避 11-12 的 429 静默丢批风险。\n'
    '- **主批 XR 新稿 13 篇（5 A / 6 B / 2 C，无 S；Top10 实数 10 篇）**。Top10：'
    '**EcoVGGT 3.93 A**（31 帧固定键集 + pin/attach 精确分解替代全帧注意力：VGGT 500 帧成功率 70%→82%、ATE 0.111→0.090、8.5× 加速；'
    'π³ 版 1,000 帧保持 94% 且 13.8×，单卡可重建 4,000 帧） · '
    'FOMOS 3.85（从 SDF 直接估局部特征尺寸做 ε-sampling 网格化：512³ Chamfer 7.5×10⁻⁴、复杂度由立方降为平方，10240³ TSDF 可内存出网格） · '
    'DeepBA 3.85（2.04M 参数 GNN 把 BA 摊销为冷启动迭代细化：CO3Dv2 AUC@30° 78.6 vs GASfM 71.2、RRA@15° 97.4 vs 79.9，参数少 71×） · '
    'A·LoMa 3.80（把仿射对应从 32×32 局部块扩到图像/图像对层级：HPatches 误差 1.50 vs AffNet 26.9，ScanNet1500 AUC@20° 70.2 vs 44.7） · '
    'VACO 3.78（每个 MANO 顶点作独立 query 在投影处采样：Hi4D F1 0.860 vs HACO 0.653，AGILE 右手 CD 23.11→12.46 mm） · '
    'D2ToF 3.58（一步扩散从 8×8×100 SPAD 直方图恢复 128×128 深度：Middlebury RMSE 11.7 mm vs Marigold-DC 32.9 mm，83 ms/帧） · '
    'MacroGS 3.57（宏像素共享 Gaussian 基元解耦「基元数×视角数」：8 编码器 ×4 平均 PSNR +0.34–0.70 dB、解码快 10–18×、仅 0.37 M 参数） · '
    'TouchTwin 3.55（880-taxel 手套实测触觉驱动 real-to-sim：策略握力 0.31×/1.55× → 0.99×，接触漏检 32.2%→13.1%） · '
    'DIRT 3.51（无训练确定性深度补全 IBR：LiveNVS 22.18 dB / 0.1959 LPIPS / 69 ms，较 On-the-fly NVS PSNR +17.6%、时延 −9×） · '
    'Zoom In, Scale Out 3.12（免标注数字变焦一致性检验：Depth Anything V2 的深度按 s^−0.95 漂移，理想为 s⁰；PARTIAL 证据）。\n'
    '- **覆盖 9 赛道（全批）/ Top10 覆盖 8 赛道**：重建与SLAM 4（Top10 占 3）/ 内容生成 1 / 化身与人体 1 / 系统与平台 1 / 神经渲染 2（占 1）/ '
    '触觉与多模态 1 / 渲染与显示 1 / 评估与数据集 1 / 交互与输入 1（13 篇全批；Top10 未含交互与输入与「渲染与显示」之外的偏门赛道）。\n'
    f'- **覆盖度三关**：门① 最大 Jaccard **{G1:.3f}**（2611.17619 vs 库内 2610.18950，<0.62）；'
    '门② 定稿 Top10 **8 赛道**（全批 9，纯值排序即达，**未触发重筛**）；'
    f'门③ 当日最高 **3.93 < 库内近 30 天 Top10 均分 {GATE3:.4f}**（现算，窗口 2026-10-18~11-17、398 条入窗）→ **非重磅日，无 S 级**。\n'
    '- **全文证据**：13 篇候选 → **12 篇 L0/FULL**（24,146–128,049 字符）+ **1 篇 L1/PARTIAL**'
    '（2611.17903：arXiv HTML 404、ar5iv 仅摘要页 5,216 字符无正文节；沙箱无 PDF 解析库，按摘要级评估并逐处标注）。OUTDATED 0。\n'
    '- **backfill-1117（3 篇，非当日新提交）**：11-16 公告 RSS 混入的旧稿 v2 再公告首次入馆——'
    'HEIR 4.07（17 人 / 300 session / 38.56 h / 1836 episode 人机双视角配对数据集，+人视角与注视使 Plan EM 63.51→78.11） · '
    'The Missing Touch 4.01（32 像素电渗泵触觉显示 30 Hz 回显接触几何：按键任务 −46%、DTW 偏离 −77%，π0.5 成功率 63.2%→92.3%） · '
    'Grid-based Submap Joining 3.87（栅格子图拼接 NLLS + pose-only GN 独立性证明，误差比 Cartographer/SLAM Toolbox 小 3–12 倍）。\n'
    '- **路线观察**：① **前馈重建进入「推理工程」阶段**——EcoVGGT 证明长序列 3D 基础模型的瓶颈已从精度转向 KV 组织方式，'
    '且「按内容选键反而更差（ATE +9.3%）」是对主流检索式流式的方向性反驳；② **经典几何求解器持续被摊销**——DeepBA 替代逐场景非线性最小二乘、'
    'A·LoMa 把上下文搬进仿射对应，几何前端正被学习化重写；③ **触觉成为本批最清晰的 XR 主线**——TouchTwin（测）与 backfill 的 The Missing Touch（显）'
    '构成接触几何的闭环两端，且后者把「自然度」用 DTW 距离量化；④ **3DGS 子方向出现饱和信号**——稀疏视角 dropout 线（SLD+LBD）相对最强基线仅 +0.02 dB，'
    '而结构性改写（MacroGS 解耦基元×视角）仍有 0.34–0.70 dB 与 10–18× 提速余量；⑤ **深度感知双向进展与警示**——D2ToF 把 8×8 SPAD 超分到 128×128，'
    '而 Zoom In, Scale Out 指出度量深度模型把数字变焦误判为靠近（α=0.95），对 AR 尺度估计是直接风险；⑥ **硬件显示方向仍无破冰**（波导/可变焦/Maxwellian/全息光场连续多批无新增）。'
)

GATE_LINES = [
    f'- 门①（同质去重）：最大 Jaccard **{G1:.3f}** < 0.62（2611.17619 TouchTwin vs 库内 2610.18950，2026-10-15），通过；'
    '其余 9 篇均 <0.20（2611.17903 0.188 / 2611.18256 0.176 / 2611.18340 0.172）。库侧 token 取 title+abstract（registry 字段），口径偏保守。',
    '- 门②（赛道覆盖）：定稿 Top10 覆盖 **8 赛道**（重建与SLAM 3 / 内容生成 1 / 化身与人体 1 / 系统与平台 1 / 神经渲染 1 / '
    '触觉与多模态 1 / 渲染与显示 1 / 评估与数据集 1）≥5，**纯值排序即达标，未触发重筛**；全批 13 篇覆盖 9 赛道（另含交互与输入 1）。',
    f'- 门③（价值天花板）：当日最高 **3.93（EcoVGGT）** < 库内近 30 天 Top10 均分 **{GATE3:.4f}**（现算，窗口 2026-10-18~11-17、**398 条入窗**；'
    '库内 Top10 = 2611.06817 4.57 S · 2611.11169 4.57 S · 2603.01178 4.50 A · 2610.39399 4.37 A · 2611.09458 4.37 A · 2611.07902 4.36 A · '
    '2610.34263 4.35 A · 2611.08578 4.34 A · 2609.31418 4.30 A · 2610.37602 4.30 A）→ **非重磅日，无 S 级**。'
    '本批亦无 ≥4.2 达线论文，校准关未触发降级改写。',
    '- **低量日不凑数原则**：主批 13 篇中 2 篇 C 级（2611.17752 2.93 / 2611.18438 2.08）仅入馆不写笔记、不占 Top10 名额；'
    'Top10 取实数 10 篇（含 4 篇 B 级），未把 B 级拔高为 A，也未为凑满而放宽下限。',
    '- **召回补层与误命中剔除（诚实披露）**：摘要级 KW 层命中 11 篇，仅 5 篇最终入选；标题级扩展词补扫补入 22 篇（其中 8 篇入选）。'
    '33 篇候选逐篇核摘要剔除 20 篇误命中——医学 MRI 4 篇（由 `\\bMR\\b`/`\\bAR\\b` 缩写层误命中）、手写文本识别 3 篇、空间转录组学与高光谱 2 篇、'
    'V2X 与自动驾驶跟踪 2 篇、机器人操作与导航 4 篇、其他 5 篇（VLA 综述 / 梯田点云分割 / LLM 串行深度 / 高斯采样理论 / El Niño 预测）。'
    '**该标题级补扫层不计入「RSS 漏网」统计**（本批 RSS 对 listing 缺收为 0，两渠道无矛盾）。',
    '- **outdated 判定**：本批无被库内更晚工作取代者（0 篇 OUTDATED / SUPERSEDED）；2611.17752 相对 DropAnSH-GS 已无优势，'
    '但属同期并存方法而非被取代，按 `CURRENT` 处理并在笔记中记录「该子方向接近饱和」。\n',
]

APPENDIX = [
    '- 本表 10 篇：FULL 9 篇；PARTIAL 1 篇（2611.17903）；ABSTRACT_ONLY 0 篇。',
    '- 抓取记录：16 篇候选（主批 13 + backfill 3）串行 3s/篇，约 60 秒完成；15 篇 L0 一次命中（24,146–184,205 字符），'
    '1 篇走 L1（ar5iv）并因仅返回摘要页由人工改判 PARTIAL；无 406/429 重试、无 L5、无 OCR、无伪造。',
    '- 当日组构成：11-16 公告组 **271 篇唯一论文**（320 槽位：CV 91 / GR 5 / HC 13 / MM 0 / RO 38 / AI 164 / IV 9），全部未入馆；'
    '摘要级 XR 命中 11 篇（KW）+ 标题级补扫 22 篇 → 33 候选 → 13 篇入池。',
    '- 剔除清单（非 XR，26 篇）：2611.17983 / 2611.18097 / 2611.17758 / 2611.17862（医学与缩写误命中）· 2611.18143 / 2611.17952 / 2611.17966（手写文本）· '
    '2611.17899 / 2611.17974（转录组 / 高光谱）· 2611.18023 / 2611.17505（V2X / 自动驾驶）· 2611.18491 / 2611.18422 / 2611.18123 / 2611.17730（机器人操作与导航）· '
    '2611.18372 / 2611.18033 / 2611.17495 / 2611.18542 / 2611.17854（其他）；replace 旧稿剔除 1 篇（2610.30969 IORA）。',
    '- 库内计数：registry 935 → **951**（+13 主批 +3 backfill）；笔记 587 → **601**；daily 63 → **65**；MOC 51 → **53**。',
    '- 门③ 现算值供下一批参考：**4.4030**（窗口逐日滚动，务必再算，勿沿用）。'
]


def appendix_bf():
    return [
        '- 本表 3 篇：FULL 3 篇；PARTIAL 0 篇；ABSTRACT_ONLY 0 篇。',
        '- 来源：11-16 公告批次 RSS 全量 435 条中 replace 类 **164 篇**未入馆者，摘要级 XR 命中 4 篇，剔除 1 篇（2610.30969 IORA）→ 3 篇。',
        '- 抓取：3 篇全部 L0 一次命中（46,770 / 112,020 / 184,205 字符），串行 3s/篇，无限流与降级。',
        '- 口径：backfill 不参与当日「重磅日」判定，≥4.2 亦一律记 A（本批无 ≥4.2，最高 4.07）。'
    ]


report(TOP10, f'reports/XR-Daily-Report-{DATE}.md',
       f'XR 每日论文解读报告 · {DATE}（11-16 公告批次 · 周末积压周一释放）', HEADER, GATE_LINES, APPENDIX)

BF_HEADER = (
    '## 一、执行摘要\n'
    '- **诚实口径**：本批 3 篇均为 **11-16 公告批次 RSS 混入的旧稿 v2 再公告**（原始投稿 2025-01-22 / 2026-08-19 / 2026-11-12；'
    'API `updated` = 2026-11-13×3），首次入馆；**均非 11-16 当日新提交**，单独编号、不参与当日重磅日判定。\n'
    '- **定稿 3 A（无 S）**，最高 **2611.17238 HEIR 4.07**（人机双视角配对数据集：17 人 / 300 session / 38.56 h / 1836 episode / 6416 子任务，'
    '加入人视角与实测注视后意图理解 Plan EM 由 63.51 升至 78.11，但四组件串联的真机端到端 episode 成功率仅 18.52%）——**高于主批最高 3.93**。\n'
    '- 其余：**2608.19372 The Missing Touch 4.01**（32 像素电渗泵触觉显示以 30 Hz 回显机器人指尖局部接触几何：按键任务完成时间 −46%、'
    'DTW 自然度偏离 −77%，peg-rolling −33%/−28%，其演示微调的 π0.5 成功率 63.2%→92.3%） · '
    '**2501.12764 Grid-based Submap Joining 3.87**（把栅格子图拼接写成同时优化全局占据图与子图坐标的 NLLS，并证明 GN 位姿增量与地图占据值解耦 → '
    '可用 pose-only GN；误差比 Cartographer / SLAM Toolbox 小 3–12 倍，拼接 0.6–5.2 s）。\n'
    '- **全批共同信号**：这 3 篇恰好落在 XR 的两条长期缺口上——「触觉闭环」（感知 + 显示）与「以人为中心的数据/意图」，'
    '且均给出了可量化的自然度或效率证据，而非仅提出概念框架。'
)

report(BF, 'reports/XR-Backfill-Report-1117.md', 'XR Backfill 报告 · backfill-1117（旧稿 v2 再公告首次入馆）',
       BF_HEADER,
       ['- 门①/门③ 对 backfill 不适用（非当日新提交，不参与重磅日判定）；'
        '门② 3 篇覆盖 3 赛道（感知与认知 / 触觉与多模态 / 重建与SLAM）。',
        '- **口径说明**：本批最高 4.07 若计入主批将超过当日最高 3.93，但仍低于门③ 的 4.4030 线，故即便计入也不改变「非重磅日」结论；'
        '按既定口径 backfill 不参与判定，本报告不宣称 S 级。\n'],
       appendix_bf())
print('reports written')
