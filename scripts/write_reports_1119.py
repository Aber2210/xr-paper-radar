# -*- coding: utf-8 -*-
"""2026-11-19 报告：主批 + backfill-1119 解读报告。"""
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from grade_caliber import assign_grade  # noqa: E402

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
os.chdir(ROOT)

D = json.load(open('data/scored_1119.json', encoding='utf-8'))
MAIN = [p for p in D if p['batch'] == '2026-11-19']
BF = [p for p in D if p['batch'] == 'backfill-1119']
MAIN.sort(key=lambda r: (-r['value'], -r['scores']['IMP'], -r['scores']['NOV'], r['id']))
BF.sort(key=lambda r: (-r['value'], -r['scores']['IMP'], -r['scores']['NOV'], r['id']))
G = json.load(open('data/gates_1119.json', encoding='utf-8'))
TOP10_ORDER = G['top10']
DATE = '2026-11-19'
HEAVY = bool(G['gate3']['blockbuster'])
MAN = json.load(open('data/fulltext/_manifest.json', encoding='utf-8'))
for p in MAIN + BF:
    p['grade'] = assign_grade(p['value'], p['batch'], HEAVY)
    p['in_top10'] = p['id'] in TOP10_ORDER
    p['level'] = MAN[p['id']]['level']
    p['evidence'] = MAN[p['id']]['evidence']
TOP10 = [next(p for p in MAIN if p['id'] == i) for i in TOP10_ORDER]

DEEP = {
    "2611.22095": "值得关注的是「调度」而非「剪枝」：Gaussian 集合与形变网络都不动，只决定每帧对哪些 Gaussian 求形变，因此质量损失可压在 0.16 dB 内。工程上要留意两点——router 需按 scene×backbone×budget 逐组训练（A6000 上 1–2 分钟准备），且实现假定均匀时间步顺序渲染，时间跳转/变速播放尚不支持。",
    "2611.22164": "这篇的真正贡献是把「推理后处理」也纳入可学习闭环：编码 agent 改 harness、按信息源蒸馏回网络、网络更新后重验 harness。读的时候重点看它的十指标 no-regression 门——单指标门控会引入 trade-off，这是 3D 感知这类多维指标任务的通用陷阱。局限也在这：第 1–2 轮曾参考 test 分数做决定，隔离并不彻底。",
    "2611.22235": "全景多机的关键不在高斯表示，而在回环：equirectangular 的 yaw 是循环移位、tilt 按纬度扭曲，平面匹配直接失效；作者改用 S² 上的 SO(3) 相关（tilt 分解 + 经度 FFT），再用三 agent 闭环的全局 Sim(3) 一致拒绝对称房间的「互相一致的错误变换」。要注意系统是离线服务端式的：1 FPS 输入、A100 上对齐 3,113 s。",
    "2611.22240": "把「可移植」从「换一门着色语言」重构为「同一数学更新 + 每设备选一条可行 schedule」，这是系统论文的正确抽象。八种跨六厂商配置全部跑完 30k 步、跨设备 PSNR 差异 <0.07 dB，说明正确性而非性能才是卖点。代价是固定偏好序牺牲设备最优速度（RX9070XT 上慢 2.94×），且四条 driver 规则只在一个 Adreno740 上验证过。",
    "2611.22541": "MentalGrid 把「不看中间画面推演空间状态」拆成 SSP/FSP/DPT 三档，使感知误差与模拟误差可分离——这是评测设计的价值所在。结论也很克制：最佳模型 58.93% 仍低于人类 74.73%，开源模型多在随机水平附近；SpatialWalker-3B 的 +33.81 点主要来自课程训练，而非新架构。",
    "2611.22207": "核心洞见是「模板、LBS 与渲染已经给出了几何对应，不该让 attention 从数据里重新学」：FAC 用动画渲染后的投影坐标做 RoPE，ITR 把坐标变成层内可迭代的 rendering-in-the-loop。68M 参数在 6 视角 NeuMan 上超 609M 的 LHM++ 2.73 dB，但单视角（27.02 vs 27.71）仍弱——它没有训练 inpaint 不可见区域。",
    "2611.22829": "把重定位拆成 place-finding（颜色足够）与 pose-refinement（几何精化）后，学习模块只需 55.7K 参数：82 ms/帧、1.44 GB，精度与 24 s/帧的 GeDi 统计等价。最实用的细节是「多候选 + 全库联合搜索」，避免了检索错房间就直接丢帧（Retrieve-1+Fast 会掉 56 点）。强依赖颜色一致，灰度输入下失效。",
    "2611.22146": "用 Quest/PICO 控制器追踪 + 编码器测开合 + 可换「机器人同款指尖」，把采集端与部署端的接触几何对齐；562 条无机器人演示训练 ACT 折毛巾 12/20，而基线 0/20。工程完整度是亮点（四级标定、7 臂 IK 重定向、Apache-2.0 开源），但真机只一个任务、单 seed，跨本体证据仅为仿真。",
    "2611.22415": "在 VSI-Bench 上逐层移除几何注入后发现「低级感知靠 shallow、高级推理靠 deep」，于是用任务条件化门控做多层级凸组合，并用负熵正则防门控塌缩。提升幅度不大（69.6→71.5、71.3→72.3），但方向明确；短板在单视图绝对距离与方向估计（SPBench-SI 60.95 vs 63.50）。",
    "2611.22657": "用投射阴影做「物理读数」，把正向匹配（T1）、干预后预测（T2）、逆向归因（T3）分开测——这是把「会不会预测」与「会不会反推」解耦的漂亮设计。GRPO 把 8B 从 24.40% 拉到 38.73%，但合成场景被简化为单平面接收面，真实图上增益仅 +2.00 点，T1 的阴影长度判断仍是全模型弱项。",
}
RELATION = {
    "2611.22095": "库内 4DGS 加速多为剪枝/静动态分解（如 2610.x 的动态 GS 压缩线），本篇是「冻结主干 + 可学习调度」的第一篇，属新增而非取代。",
    "2611.22164": "库内手部追踪以单点模型为主（WiLoR/HaWoR 系），本篇是系统级的 harness+蒸馏闭环，属新增范式；与 11-18 的 WinDEX/MetricHand 构成「精度—工程」互补。",
    "2611.22235": "库内 SLAM 线已有 UniGS-SLAM、DPGS-SLAM 等单机稠密方案，本篇补上「多机 + 全景」维度，属新增场景而非取代。",
    "2611.22240": "库内 3DGS 系统工作多在 CUDA 侧优化吞吐，本篇补上跨厂商可移植性，属新增维度。",
    "2611.22541": "库内空间推理基准（SpatialCast、VSI-Bench 系）以静态场景为主，本篇补上动态状态推演，属新增评测维度。",
    "2611.22207": "库内化身重建以 feedforward 大模型为主（LHM 系），本篇给出「几何先验换 scaling」的对照证据，属新增技术路线。",
    "2611.22829": "库内重定位/配准以点云配准方法为主（GeDi/BUFFER-X 系），本篇把代价压到 82 ms，属显著改进。",
    "2611.22146": "库内数据采集线有 UMI/YUBI 系，本篇在接触几何一致性与开源完整度上改进，属增量式改进。",
    "2611.22415": "库内 MLLM 空间推理工作（SpatialStack 系）为固定层级融合，本篇改为任务条件化门控，属改进。",
    "2611.22657": "库内空间基准多测静态关系，本篇以阴影为物理证据补上因果推理维度，属新增。",
}
for p in MAIN + BF:
    p['deep'] = DEEP.get(p['id'], '')
    p['relation'] = RELATION.get(p['id'], '本批新增，与库内同赛道论文构成并列参考；未发现直接取代关系。')

REPORT = 'reports/XR-Daily-Report-' + DATE + '.md'
L = []
A = L.append

A('# XR 每日论文雷达 · ' + DATE + '（11-18 公告批次）\n')
A('> **诚实口径**：本批处理的是 **2026-11-18（周三）公告批次**，拉取时刻为 **2026-11-19 02:30（周四）**——公告日 ≠ 拉取日。')
A('> 主批 21 篇的 API published 提交日为 **11-17×17 / 11-16×3 / 09-27×1**')
A('> （2611.21642 RelicTouch 提交 2026-09-27、延迟约 7 周公告）。RSS 的 published 字段是公告时间戳，不可当提交日。')
A('> 另设 **backfill-1119** 批次（4 篇旧稿 v2/v3 再公告，非当日新提交），单独报告。\n')

A('## 一、执行摘要\n')
A('- **规模**：11-18 公告组 **599 槽位 / 496 篇唯一论文**（cs.CV 207 / cs.GR 10 / cs.HC 26 / cs.MM 3 / cs.RO 89 / cs.AI 259 / eess.IV 5），全部未入馆；RSS 全量 766 条覆盖 listing 496/496（缺收 0）。')
A('- **入选**：摘要级 KW 命中 37 篇 + 标题级补扫 21 篇 → 58 候选 → 逐篇核摘要剔除 37 篇误命中 → **XR 21 篇**（0 S / 12 A / 7 B / 2 C）。')
A('- **全文**：25 候选（21 + 4）串行抓取，**25 篇全部 L0/FULL**（17,275–130,366 字符）；无 PARTIAL、无摘要级评估。')
A('- **三关**：门① 最大 Jaccard **' + f'{G["gate1"]["max_jaccard"]:.3f}' + '**（<0.62）；门② 定稿 Top10 覆盖 **6 赛道**（全批 8，纯值排序即达、未重筛）；门③ 当日最高 **' + f'{G["gate3"]["today_max"]:.2f}' + ' vs 库内近 30 天 Top10 均分 **' + f'{G["gate3"]["top10_mean"]:.4f}' + '**（窗口 2026-10-20~11-19、436 条入窗、按 batch 剔除本批两批）→ **非重磅日，无 S 级**（margin ' + f'{G["gate3"]["margin"]:+.4f}' + '）。')
A('- **本批主线**：')
A('  1. **端侧 3DGS 从「能跑」进入「跑得动、跑得稳」**——CueSplat 把 4DGS 形变评估变成可学习调度（Jetson Orin 上 1.75–6.74×、PSNR 仅降 ≤0.16 dB），Cross3DGS 把训练搬到采集设备（八种跨厂商 GPU 全部跑完 30k 步、跨设备 PSNR 差异 <0.07 dB）。')
A('  2. **手部/化身链条继续加厚**——HandRSI 用编码 agent 递归改进 harness 与权重（HOT3D MPJPE-p 12.97→8.37 mm、jitter −52%），ARG-Avatar 用几何先验替代 scaling（68M 参数超 609M 的 LHM++ 2.73 dB），HandUMI 用 Quest/PICO + 手戴夹爪采集双臂数据（ACT 折毛巾 12/20 对基线 0/20）。')
A('  3. **空间智能从静态走向动态**——MentalGrid 把「无中间视觉反馈的状态推演」形式化为 SSP/FSP/DPT 三档基准（最佳模型 58.93% vs 人类 74.73%），SpatialCast 用投射阴影做物理读数（GRPO 使 8B +14.33 点），SpatialMind 做任务条件化的多层级几何融合（VSI-Bench 同规模第一）。')
A('  4. **重建侧工程化收敛**——CoSphere-SLAM 把多机全景 ATE 从 1.353 压到 0.082 m，Kolibri 把建筑尺度重定位压到 82 ms/帧，Refin3R 用 SfM 引导把稠密 point map 的 AUC@1cm 提升 24–35%。')
A('  5. **硬件显示侧连续第 30 批无器件级破冰**（波导/可变焦/Maxwellian/光场均无新稿）；本批触觉侧仅一篇 100 美元级振动触觉像素阵列（3.00 B）。')
A('- **S 级说明**：本期 **0 篇 S**。最高 4.30（CueSplat / HandRSI 并列）未达库内近 30 天 Top10 均分 4.4230，门③ 明确判非重磅日，未触发险过条款。\n')

A('## 二、排行榜（按加权降序，Top10）\n')
A('| # | 论文 | 赛道 | 总分 | 等级 | 证据 | 关键数字 |')
A('|---:|---|---|---:|---|---|---|')
for i, p in enumerate(TOP10, 1):
    key = p['experiments'][0]
    A(f"| {i} | {p['title_zh']}（{p['id']}） | {p['track']} | {p['value']:.2f} | {p['grade']} | {p['evidence']} | {key[:120]} |")
A('')

A('## 三、逐篇深度解读\n')
A('> 以下 10 章按价值降序，对应 Top10。每章含问题、方法、结果、创新、深读要点、局限、库内关系、可复现性与行动建议。\n')
for i, p in enumerate(TOP10, 1):
    s = p['scores']
    A(f"### {i}. {p['title_zh']}（{p['id']}）\n")
    A(f"**赛道**：{p['track']}　**总分**：{p['value']:.2f}（{p['grade']}）　**证据**：{p['evidence']}/{p['level']}　"
      f"**7 维**：IMP {s['IMP']} · NOV {s['NOV']} · TEC {s['TEC']} · EXP {s['EXP']} · PER {s['PER']} · TRL {s['TRL']} · REP {s['REP']}\n")
    A(f"**一句话结论**：{p['conclusion']}\n")
    A(f"**要解决的问题**：{p['problem']}\n")
    A(f"**方法详解**：{p['method']}\n")
    A('**实验与结果**：')
    for x in p['experiments']:
        A(f'- {x}')
    A('')
    A(f"**创新点**：{p['novelty']}\n")
    if p['deep']:
        A(f"**深读要点**：{p['deep']}\n")
    A(f"**局限与风险**：{p['limitations']}\n")
    A(f"**与文献库的关系**：{p['relation']}\n")
    A('**可复现性**：' + ('代码/项目页 ' + p['code'] if p['code'] and p['code'] != 'none' else '正文未提供代码') + f"；全文 {p['chars']:,} 字符（{p['level']}/{p['evidence']}）。\n")
    A('**行动建议**：' + ('纳入重点精读，先跑通公开代码再评估迁移成本。' if p['code'] and p['code'] != 'none' else '纳入重点精读；无公开代码，需按正文细节复现。') + '\n')

A('## 四、当日全量 7 维度对比表\n')
A('完整表见 `papers/daily/' + DATE + '/7dim-table.md`（21 篇全量，含 C 级）。摘要如下：\n')
A('| arXiv | 标题 | 赛道 | 总分 | 等级 | 证据 |')
A('|---|---|---|---:|---|---|')
for p in MAIN:
    A(f"| {p['id']} | {p['title_zh']} | {p['track']} | {p['value']:.2f} | {p['grade']} | {p['evidence']} |")
A('')

A('## 五、覆盖率校验与筛选过程说明\n')
A('### 5.1 漏网对账（先于拉取）\n')
A('- `scripts/audit_listing_1119.py` 以 show=500 单页复采 7 分类，目标日组 declared≠got 时自动补采后续页（continued/last 兼容）。')
A('- 7 分类最新公告日均为 **2026-11-18**，无 11-19 日组；11-17 组复采逐分类 declared=got（1,016 槽位 / 844 唯一），未入馆 **811 篇 = 844 − 33（上批主批已入馆）**。')
A('- 用 11-18 的 RSS 全量逐篇核摘要：811 篇中 XR 命中 **69 篇**，与上批 `data/rejected_1118.json` 的 69 篇**逐篇一致** → **0 漏网、无滞后补录、无 backfill 触发**（本批 backfill 来自今日 RSS 的 replace 流，与补漏无关）。')
A('- **采集完整性**：七分类 declared=got 全部成立，脚本 exit 0（非采集不全的 exit 2）。\n')
A('### 5.2 门① 同质度\n')
A(f"- 定稿 Top10 对库内 90 天非本批文献的最大 Jaccard 为 **{G['gate1']['max_jaccard']:.3f}**（2611.22415 SpatialMind vs 2609.03892，2026-09-03），远低于 0.62 阈值；其余 9 篇 0.091–0.188。")
A('- 结论：无同质重复，无需降权或剔除。\n')
A('### 5.3 门② 赛道覆盖\n')
t = G['gate2']['top10_tracks']
A('- 定稿 Top10 覆盖 **6 赛道**：' + '、'.join(f'{k}×{v}' for k, v in t.items()) + f"（全批 {G['gate2']['n_all']} 赛道）。")
A('- 结论：纯值排序即达标（≥5），**未触发重筛**；赛道分布以感知与认知（3 篇）最集中，但均属不同子问题（动态模拟 / 多层级融合 / 阴影因果），不构成冗余。\n')
A('### 5.4 门③ 价值天花板（校准关）\n')
A(f"- 当日最高 **{G['gate3']['today_max']:.2f}** vs 库内近 30 天 Top10 均分 **{G['gate3']['top10_mean']:.4f}**（窗口 2026-10-20~11-19、436 条入窗、按 batch 剔除 2026-11-19 与 backfill-1119）。")
A('- 结论：**非重磅日，无 S 级**（margin ' + f'{G["gate3"]["margin"]:+.4f}' + '，未进入 0.05 险过区）。按 skill §8.6.3，不因「接近」而拔高评分。')
A('- 库内 Top10 构成（供对照）：' + '、'.join(f"{x['id']} {x['value']}" for x in G['gate3']['top10_lib'][:6]) + '。\n')
A('### 5.5 召回分层与剔除\n')
A('- 摘要级 KW 命中 37 篇（保留 15）→ 标题级扩展词补扫 21 篇（保留 6）→ 候选 58 篇 → 剔 37 篇误命中 → **XR 21 篇**。')
A('- 误命中主因：`SLAM`/`point cloud`/`monocular depth` 把自动驾驶与机器人操作带入（12 篇），`AR`/`MR` 缩写误命中自回归（2 篇），`spatial`/`tracking`/`depth` 泛词带入通用 2D 视觉（8 篇）。')
A('- **C 级 2 篇仅入馆不解读**：2611.22151 EgoHandWAM 2.92（受控探针、以负结果为主）、2611.21642 RelicTouch 2.85（n=20 主观评分、无客观解读指标）。')
A('- OUTDATED/SUPERSEDED：**0 篇**（无足够证据判定任何一篇被库内或本批取代）。\n')

A('## 六、附录\n')
A('### 6.1 证据等级与抓取\n')
A('- 25 篇全部 **L0/FULL**（arXiv HTML 正文），无 L1/L2/L5 降级；字符数 17,275–130,366。')
A('- **剔除说明**：2611.23209（gaze-guided VLM）虽 L0 抓取成功，但正文仅含摘要页 + 参考文献（无 Introduction/Method/Results），按诚实口径不纳入评分，记入证据不足清单。')
A('- 抓取严格串行 3s/篇，无限流、无 429；manifest 合并写入校验通过。\n')
A('### 6.2 数据与脚本\n')
A('- 对账：`scripts/audit_listing_1119.py`；甄别：`scripts/triage_1119.py`；漏网复核：`scripts/filter_missed_1119.py`；三关：`scripts/gates_1119.py`；评分：`data/scored_1119.json`；产物：`scripts/write_deliverables_1119.py`、`scripts/write_notes_1119.py`、`scripts/write_reports_1119.py`。')
A('- 对账数据：`data/audit_1119_days.json`、`data/newday_1119.json`、`data/missed_prev_1119.json`、`data/missed_new_1119.json`、`data/missed_xr_1119.json`（0 条）。\n')
A('### 6.3 库况\n')
A('- registry **990 → 1,015**（+21 主批 +4 backfill，按 base_id 幂等，备份 `registry.jsonl.bak-20261119`）；')
A('- 原子笔记 632 → **655**（本批 23 篇，grade≥B）；daily 目录 67 → **69**；MOC 55 → **57**。\n')
A('### 6.4 backfill-1119\n')
A('4 篇旧稿 v2/v3 再公告，单独报告见 `reports/XR-Backfill-Report-backfill-1119.md`：SFMambaNet 3.85 A · Max-Clique vs Max-Consensus 3.84 A · SSA-3DGS 3.65 A · HolisticMotion 3.28 B。\n')

open(REPORT, 'w', encoding='utf-8').writelines([x + '\n' for x in L])
print('main report', REPORT, len(''.join(L)))

# ---------------- backfill report ----------------
R2 = 'reports/XR-Backfill-Report-backfill-1119.md'
L = []
A = L.append
A('# XR 论文雷达 · backfill-1119（旧稿再公告批次）\n')
A('> **诚实口径**：本批 4 篇均为 **2026-11-18 公告批次 RSS 混入的旧稿 replace 再公告**（API published 2026-05-21 / 2026-06-03 / 2026-07-06 / 2026-10-19，updated 2026-11-16~11-17），')
A('> 均非 11-18 当日新提交。单独编号、不参与当日「重磅日」判定，≥4.20 亦按口径记 A。\n')
A('## 一、批次概览\n')
A('- 来源：RSS 全量 766 条中 **replace 类 270 篇**未入馆者 → 摘要级 XR 命中 **17 篇** → 逐篇核摘要取 **4 篇**（剔除机器人操作、雷达里程计、自动驾驶重建、流形采样、医学多模态等 13 篇非 XR）。')
A('- 全文：4 篇全部 **L0/FULL**（42,817–130,366 字符）。')
A('- 定稿：**3 A / 1 B / 0 C（无 S）**，最高 **3.85（SFMambaNet）**。\n')
A('## 二、排行榜\n')
A('| # | 论文 | 赛道 | 总分 | 等级 | 证据 | 关键数字 |')
A('|---:|---|---|---:|---|---|---|')
for i, p in enumerate(BF, 1):
    A(f"| {i} | {p['title_zh']}（{p['id']}） | {p['track']} | {p['value']:.2f} | {p['grade']} | {p['evidence']} | {p['experiments'][0][:120]} |")
A('')
A('## 三、逐篇解读\n')
for i, p in enumerate(BF, 1):
    s = p['scores']
    A(f"### {i}. {p['title_zh']}（{p['id']}）\n")
    A(f"**赛道**：{p['track']}　**总分**：{p['value']:.2f}（{p['grade']}）　**证据**：{p['evidence']}/{p['level']}　"
      f"**7 维**：IMP {s['IMP']} · NOV {s['NOV']} · TEC {s['TEC']} · EXP {s['EXP']} · PER {s['PER']} · TRL {s['TRL']} · REP {s['REP']}\n")
    A(f"**一句话结论**：{p['conclusion']}\n")
    A(f"**要解决的问题**：{p['problem']}\n")
    A(f"**方法详解**：{p['method']}\n")
    A('**实验与结果**：')
    for x in p['experiments']:
        A(f'- {x}')
    A('')
    A(f"**创新点**：{p['novelty']}\n")
    A(f"**局限与风险**：{p['limitations']}\n")
    A(f"**与文献库的关系**：{p['relation']}\n")
    A('**可复现性**：' + ('代码/项目页 ' + p['code'] if p['code'] and p['code'] != 'none' else '正文未提供代码') + f"；全文 {p['chars']:,} 字符。\n")
    A('**行动建议**：' + ('有公开代码/项目页，可直接复现。' if p['code'] and p['code'] != 'none' else '无公开代码，按正文细节复现；优先读其问题形式化与实验协议。') + '\n')
A('## 四、与主批的关系\n')
A('- **SFMambaNet** 与主批 Refin3R 同属「SfM/对应前端」链路：前者提升对应剪枝质量，后者提升稠密 point map 精度，可串联评估。')
A('- **Max-Clique vs Max-Consensus** 给主批 Kolibri 这类「配准式重定位」提供了准则选择的理论依据：最大团解可能无法被单一变换对齐，工程上应优先最大一致集或加证书过滤。')
A('- **SSA-3DGS** 与主批 ReTouchGS/DOOM-GS 同属 3DGS 资产质量与效率线，前者处理输入伪影、后者处理调色与外存训练。')
A('- **HolisticMotion** 与主批 ARG-Avatar/HandRSI 构成「稀疏跟踪 → 全身/手部重建」的上下游。\n')

open(R2, 'w', encoding='utf-8').writelines([x + '\n' for x in L])
print('bf report', R2, len(''.join(L)))
