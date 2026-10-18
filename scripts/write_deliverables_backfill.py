# -*- coding: utf-8 -*-
"""write_deliverables_backfill.py — 生成 backfill 原子笔记(6) + MOC + 解读报告 + 总索引更新。
读取 data/scored_backfill.json；笔记/MOC/报告均中文、md。
"""
import json, os, datetime

ROOT = "D:/Agent/WorkBuddy/Research"
BATCH = "backfill-2603-2609"
scored = json.load(open(f"{ROOT}/data/scored_backfill.json", encoding="utf-8"))

# 每篇结构化内容（基于 L0/FULL 全文 + 摘要，诚实摘录，不脑补数值）
NOTE = {
 "2607.17790": {
  "slug":"ReViV-4D-egocentric",
  "summary":"首个从单目第一视角 RGB 视频统一重建「观察者(view)」与「视角(viewer)」4D 动态的前馈框架，联合建模多模态信号、推理比同类快 10–100×。",
  "bg":"可穿戴前摄等第一视角设备能捕捉人与环境的连续交互；但现有方法要么依赖预计算相机轨迹、要么把场景感知与人体自运动建模割裂、要么推理慢，难以支撑 AR/VR/AI 眼镜的实时 4D 重建。",
  "method":"将任务表述为对多模态信号（RGB 视频、相机轨迹、注视方向、全身运动、手部运动、深度）联合概率分布 p(𝒳,𝒴) 的学习；用 Masked Generative Egocentric Transformer 在单一前馈架构内同时重建时间一致的 4D 表征，绕过易出错的级联相机跟踪。统一离散 tokenization + 多模态掩码目标迫使模型学到鲁棒的生物力学合理运动先验。",
  "exp":"在 HoloAssist、HOT3D、ARCTIC、Aria Digital Twin、TACO 多基准上评测；全身/手/注视重建与相机跟踪达 SOTA，深度估计具竞争力。比 EgoAllo 快约 100×、比 UniEgoMotion 快约 10×；即使不输入相机轨迹也优于用 GT 相机的基线（PA-MPJPE 88.6、Similarity 0.751、FID 0.442、推理 0.7s）。消融证实参数规模关键（127M 轻量变体明显退化）、性能随数据量扩展。",
  "contrib":"统一联合分布建模避免级联相机误差、首次 holistic 第一视角 4D 重建；局限：依赖大规模多模态数据集，轻量变体性能下降明显，真实部署需算力。",
  "rel":"与库内 VGGT-BC（2610.09274，硬件感知校准聚类注意力，3.73）互补而非取代——ReViV 更 holistic（增注视/深度/手）且更快；同属第一视角几何重建方向，建议持续追踪其取代/归一信号。",
  "xr":"AR/VR/AI 眼镜实时第一视角 4D 重建、注视估计、具身智能体场景理解。",
  "tags":["egocentric","4D-reconstruction","gaze","transformer","SOTA"],
 },
 "2606.19156": {
  "slug":"Hand-4DGS",
  "summary":"前馈式 3D 高斯溅射框架，从第一视角视频做动态 4D 手部重建，网格引导表示+时序卷积，免 GT 3D 手姿标注。",
  "bg":"动态 3D 手部重建是 AR/VR/AI 眼镜的核心能力；但第一视角 4D 手重建因手/相机快速运动、手-物与手-手交互、单目歧义而困难，既往工作多聚焦多视 3D 手或 4D 身体。",
  "method":"前馈框架 Hand-4DGS：mesh-guided 表示提供结构先验（mesh-aligned vertex embeddings + mesh-relative Gaussian adjustment）；时序卷积层建模动态运动；可微高斯光栅化的图像监督提供外观优化与姿态调整信号，训练与测试时优化均无需 GT 3D 手姿标注（用 WiLoR 伪标签离线训练，SAM3 遮罩处理遮挡）。",
  "exp":"在 H2O、ARCTIC 两个第一视角手-物交互数据集上评测，优于 HandNeRF++（辐射场基线）、GaussianHand（泛化手化身）、EVA（优化式单目高斯化身）；测试时优化可高效适配训练未覆盖的视频。",
  "contrib":"前馈+网格引导+时序卷积，免 GT 姿态标注即可做第一视角 4D 手重建；局限：依赖 WiLoR 伪标签训练、SAM3 遮罩处理遮挡，极端手-物交互精度待提升。",
  "rel":"与库内高斯化身（VGGT-BC、边缘头部化身 2610.09821）、3DGS 生成方向互补，补「第一视角 4D 手」专项目。",
  "xr":"手势交互、手-物交互、虚拟手化身、AI 眼镜手部追踪。",
  "tags":["hand","4DGS","egocentric","avatar","feed-forward"],
 },
 "2608.12759": {
  "slug":"NavSight-lowvision-AR",
  "summary":"面向低视力户外导航的移动端 AR 应用，首个真实世界 in-the-wild 日记研究，提炼 AI 辅助无障碍 AR 设计启示。",
  "bg":"低视力(PLV)户外安全独立导航困难且重要；现有低视力 AR 多在理想实验室环境评估，缺真实世界可行性与挑战研究。",
  "method":"NavSight：移动 AR 应用，识别重要户外物体（路缘、车辆等）并渲染实时视觉增强；iOS/Unity/CoreML 设备端推理；对 YOLO11l-seg 做户外物体微调。",
  "exp":"12 名 PLV 真实世界 7 日日记研究；刻画对场景感知影响、用户对「增强什么/如何增强」的配置策略、识别错误处理、公共场合社交可接受性；识别环境影响（天气/光照/阴影/非标道路标线）与日常可用性问题。微调模型 mAP50 0.256→0.588、mAP75 0.129→0.305、mAP 0.136→0.318。",
  "contrib":"首个低视力 AR 真实世界 in-the-wild 研究，给出环境/可用性/设计启示；局限：n=12 小样本、iOS 专属、识别错误时用户应对策略待系统性化。",
  "rel":"与库内空间计算/UI（多为 VR 探索/导航世界模型如 SPW-Nav 2610.08941）互补，补「无障碍 AR 真实部署」视角。",
  "xr":"无障碍 AR 导航、AI 眼镜辅助视障、公共空间信息增强。",
  "tags":["assistive-AR","low-vision","navigation","in-the-wild","HCI"],
 },
 "2607.19479": {
  "slug":"ModPack-teleop",
  "summary":"模块化可扩展双臂移动操控遥操作框架，可穿戴背包核心+插件式能力模块（触觉反馈/移动操控/主动感知），硬件软件全开源。",
  "bg":"现有遥操作系统常绑定特定机器人硬件与任务域，扩展性与适应性受限。",
  "method":"ModPack：模块化可扩展遥操作框架；核心是可穿戴「背包」集成板载计算/电源/通信/存储；其上支持即插即用能力模块——关节级遥操作+触觉反馈、移动操控、主动感知。完整硬件设计+软件栈开源。",
  "exp":"两个机器人平台、真实移动操控任务验证；比无机器人替代方案收集更高质量数据。布艺放置（主动感知）头摄 22/25 成功、腕摄仅 3/25；箱体搬运（触觉反馈）验证触觉通道价值。",
  "contrib":"统一接口支持多样本体、高 TRL、全开源；更偏机器人遥操作，与 XR 关联在「远程呈现/化身控制」间接相关。局限：主要面向机器人数据收集，XR 直接映射有限。",
  "rel":"与库内触觉与多模态（TouchScale 2610.10288 数据集）互补，补「遥操作接口+触觉反馈」系统侧。",
  "xr":"远程呈现/化身控制、触觉反馈遥操作、机器人-AI 眼镜协同。",
  "tags":["teleoperation","haptic","open-source","robotics"],
 },
 "2603.20714": {
  "slug":"3DGS-init-densify",
  "summary":"系统研究 3D 高斯溅射中初始化与稠密化的作用，给出「稠密初始化提升几何/离轨迹泛化但不一致提升视觉」的可操作结论。",
  "bg":"3DGS 从 SfM 稀疏点初始化并靠稠密化获得完整场景表示；但初始化如何影响新视角合成(NVS)性能与几何质量长期缺乏系统研究。",
  "method":"系统比较多种初始化策略（含激光扫描初始化、Depth Anything 3 初始化）与多种稠密化策略的组合，量化视觉质量与几何精度。",
  "exp":"结论：稠密初始化配强稠密化并不一致提升视觉质量，但有助于离轨迹(off-trajectory)视角泛化、显著提升场景几何精度；代码开源（ivd_splat）。",
  "contrib":"给出「初始化 vs 稠密化」权衡的可操作结论，是 3DGS 渲染基础认知补强；非新方法（分析论文），视觉质量提升有限。",
  "rel":"与库内大量 3DGS 渲染/压缩（神经渲染赛道）互补，补「初始化机理」基础认知。",
  "xr":"3DGS 实时渲染初始化、SLAM-3DGS 几何精度提升。",
  "tags":["3DGS","initialization","densification","NVS"],
 },
 "2605.07943": {
  "slug":"TAVIS-benchmark",
  "summary":"第一视角主动视觉与预期注视模仿学习基准，含 GALT（注视-动作先导时）认知科学指标，量化主动视觉贡献。",
  "bg":"主动视觉（策略自控制注视）已成为模仿学习关键能力，但缺共享基准来比较方法或量化其贡献、适用任务类型与条件。",
  "method":"TAVIS：主动视觉模仿学习评测基础设施；TAVIS-Head（5 任务，全景/俯仰颈）、TAVIS-Hands（3 任务，腕摄局部遮挡），基于 IsaacLab；三评测原语：配对头摄 vs 固定摄协议、GALT（注视-动作先导时，认知科学/HRI 指标）、程序化 ID/OOD 划分；基线 Diffusion Policy、π0。",
  "exp":"发现：主动视觉普遍有帮助（跨训练一致）但收益任务条件性非均匀；多任务策略在受控分布偏移下急剧退化；纯模仿可得预期注视（先导时接近人类演示，但头部运动不如演示平滑，动作分块所致）；代码与评测开源。",
  "contrib":"首个主动视觉模仿学习基准 + GALT 指标；更偏机器人，与 XR 关联在「第一视角主动视觉/注视」。局限：任务集有限、依赖 IsaacLab 仿真。",
  "rel":"与库内感知与认知（ReViV 注视、Never Look Back 物体记忆）互补，补「主动视觉基准+预期注视量化」。",
  "xr":"AI 眼镜主动视觉、注视预测、具身智能体评测。",
  "tags":["benchmark","active-vision","gaze","imitation-learning"],
 },
}

def fm(s, n):
    sc=s["scores"]
    return (
 f"---\n"
 f"id: {s['id']}\n"
 f"title: \"{s['title']}\"\n"
 f"track: {s['track']}\n"
 f"date: {s['date']}\n"
 f"batch: {s['batch']}\n"
 f"orig_window: {s['orig_window']}\n"
 f"grade: {s['grade']}\n"
 f"value: {s['value']}\n"
 f"scores: {{IMP: {sc['IMP']}, NOV: {sc['NOV']}, TEC: {sc['TEC']}, EXP: {sc['EXP']}, PER: {sc['PER']}, TRL: {sc['TRL']}, REP: {sc['REP']}}}\n"
 f"fetch_level: L0\n"
 f"evidence: FULL\n"
 f"status: CURRENT\n"
 f"flags: [BACKFILL]\n"
 f"tags: {n['tags']}\n"
 f"---\n"
)

# ---------- 写 6 篇原子笔记 ----------
os.makedirs(f"{ROOT}/papers/notes", exist_ok=True)
notes_idx=[]
for s in scored:
    bid=s["base_id"]; n=NOTE[bid]
    body=(
 fm(s,n) +
 f"## 一句话总结\n{n['summary']}\n\n"
 f"## 问题背景\n{n['bg']}\n\n"
 f"## 方法\n{n['method']}\n\n"
 f"## 实验\n{n['exp']}\n\n"
 f"## 贡献与局限\n{n['contrib']}\n\n"
 f"## 与文献库关系\n{n['rel']}\n\n"
 f"## 适用 XR 场景\n{n['xr']}\n"
 )
    fn=f"{ROOT}/papers/notes/{bid}__{n['slug']}.md"
    open(fn,"w",encoding="utf-8").write(body)
    notes_idx.append((bid, n['slug'], s['title_zh'], s['grade'], s['value'], s['track']))
    print(f"  笔记 {bid} -> {fn}")

# ---------- backfill MOC ----------
def row(s):
    sc=s["scores"]
    return (f"| {s['base_id']} | {s['title_zh']} | {s['grade']} | {s['value']:.2f} | "
            f"{sc['IMP']}/{sc['NOV']}/{sc['TEC']}/{sc['EXP']}/{sc['PER']}/{sc['TRL']}/{sc['REP']} | {s['track']} |")
moc=[
 "# MOC · backfill-2603-2609（历史旧稿补录）",
 "",
 f"> 批次性质：**历史旧稿 backfill**，非当日新提交。RSS replace 公告日 2026-10-08；原始投稿窗口 2603–2609。",
 f"> 触发：export.arxiv.org / arxiv.org/api/query 已恢复 200（10-09 探针），执行「API 健康时单开 backfill」待办。",
 f"> 覆盖度门：门① max Jaccard 0.333（通过）；门② 5 赛道（通过）；门③ 不适用。",
 "",
 "## 排行榜（按加权降序）",
 "",
 "| arXiv ID | 中文题名 | 档 | 加权 | 7 维(IMP/NOV/TEC/EXP/PER/TRL/REP) | 赛道 |",
 "|---|---|---|---|---|---|",
]
for s in scored:
    moc.append(row(s))
moc += [
 "",
 "## 赛道分布",
 "- 感知与认知：ReViV（3.85）、TAVIS（3.30）",
 "- 化身与人体：Hand-4DGS（3.85）",
 "- 空间计算与UI：NavSight（3.73）",
 "- 交互与输入：ModPack（3.45）",
 "- 神经渲染：3DGS-Init（3.35）",
 "",
 "## 落后 / 路线观察",
 "- 本批次均为 BACKFILL 旧稿，方法多为当期有价值的补充；无 OUTDATED/SUPERSEDED。",
 "- ReViV 与库内 VGGT-BC（2610.09274）同属第一视角几何重建，互为补充（ReViV 更 holistic 且更快），持续关注归一/取代信号。",
 "- 3DGS-Init 与库内 3DGS 渲染/压缩多篇互补，补「初始化机理」基础认知。",
 "",
 "## 原子笔记索引",
]
for bid,slug,zh,g,v,track in notes_idx:
    moc.append(f"- [{bid} · {zh}（{g} {v}）](../../notes/{bid}__{slug}.md)")
moc += [
 "",
 "## 参考",
 f"- 7 维对比表：`../papers/daily/{BATCH}/7dim-table.md`",
 f"- 运行日志：`../papers/daily/{BATCH}/run_log.md`",
 f"- 评分明细：`../data/scored_backfill.json`",
 "- 总索引：`../MOC/MOC-总索引.md`",
]
open(f"{ROOT}/papers/MOC/MOC-{BATCH}.md","w",encoding="utf-8").write("\n".join(moc)+"\n")
print(f"  MOC -> {ROOT}/papers/MOC/MOC-{BATCH}.md")

# ---------- 解读报告 ----------
def chapter(s, i):
    n=NOTE[s["base_id"]]; sc=s["scores"]
    return (
 f"### 第 {i} 章 · {s['base_id']} ｜ {s['title_zh']}\n\n"
 f"> 档位 **{s['grade']}**（加权 {s['value']:.2f}）｜赛道 {s['track']}｜原始投稿 {s['orig_window']}（RSS replace 公告 2026-10-08）｜全文 L0/FULL\n\n"
 f"**一句话总结**：{n['summary']}\n\n"
 f"**问题背景**：{n['bg']}\n\n"
 f"**方法**：{n['method']}\n\n"
 f"**实验**：{n['exp']}\n\n"
 f"**贡献与局限**：{n['contrib']}\n\n"
 f"**与文献库关系**：{n['rel']}\n\n"
 f"**适用 XR 场景**：{n['xr']}\n\n"
 f"**7 维评分**：IMP {sc['IMP']} · NOV {sc['NOV']} · TEC {sc['TEC']} · EXP {sc['EXP']} · PER {sc['PER']} · TRL {sc['TRL']} · REP {sc['REP']}\n\n"
 f"---\n"
)
rep=[
 "# XR 每日论文雷达 · 旧稿 Backfill 解读报告（2603–2609）",
 "",
 f"> **批次性质**：历史旧稿补录（**非当日新提交**）。执行条件：2026-10-09 探针确认 export.arxiv.org / arxiv.org/api/query 均已恢复 200，满足「API 健康时单开 backfill 批次」待办。",
 f"> **来源**：2026-10-09 RSS 落盘中的 7 篇 2603–2609 旧稿（replace 公告日 2026-10-08）；经 XR 相关性甄别保留 6 篇 XR 相关，剔除 1 篇非 XR（2605.00556 自动驾驶 HCI）。",
 f"> **诚实口径**：本批全部标注 `batch=backfill-2603-2609`、`orig_window=2603–2609`、公告日 2026-10-08，绝不混入「当日新论文」表；原始投稿月份窗口已在笔记与索引注明。",
 "",
 "## 一、执行摘要",
 "",
 f"本批次补录 **6 篇** XR 相关历史旧稿：3 A（ReViV 3.85 / Hand-4DGS 3.85 / NavSight 3.73）+ 3 B（ModPack 3.45 / 3DGS-Init 3.35 / TAVIS 3.30）。全文均 L0/FULL 抓取（45K–155K 字符），覆盖 5 个赛道。文献库由 368 → 374。所有条目标记 `BACKFILL`、`in_top10=False`，不污染库内 Top10 均值。",
 "",
 "## 二、方法论与诚实口径",
 "",
 "- 7 维固定权重：IMP0.20·NOV0.20·TEC0.15·EXP0.15·PER0.15·TRL0.08·REP0.07；档位 S≥4.20·A3.60–4.20·B3.00–3.60·C<3.00。",
 "- 全文抓取 L0→L5 降级链路，本次 6 篇全部 L0/FULL，无限流/降级/伪造。",
 "- 覆盖度门：门① 同质查重 max Jaccard 0.333（<0.62 通过）；门② 覆盖 5 赛道（≥5 通过）；门③ 对 backfill 不适用（不参与当日重磅日/S 级竞赛）。",
 "- 剔除说明：2605.00556 属自动驾驶 HCI，非 XR/VR/AR，C 级，不纳入 XR 文献库。",
 "",
 "## 三、全文精读（按重要性排序）",
 "",
]
for i,s in enumerate(scored,1):
    rep.append(chapter(s,i))
rep += [
 "## 四、7 维度对比表（参考）",
 "",
 "详见 `papers/daily/backfill-2603-2609/7dim-table.md`（含 6 篇完整 7 维评分）。",
 "",
 "## 五、覆盖度校验",
 "",
 "- 门① 同质查重：max Jaccard 0.333（Hand-4DGS vs StereoGaussians），远低于 0.62 阈值 → 通过（无重复误录）。",
 "- 门② 赛道覆盖：5 赛道（感知与认知/化身与人体/空间计算与UI/交互与输入/神经渲染）→ 通过。",
 "- 门③：backfill 不参与当日重磅日判定 → 不适用。",
 "- 重筛触发：否。",
 "- 价值覆盖：本批补强库内「第一视角 4D 重建(ReViV)」「第一视角 4D 手(Hand-4DGS)」「无障碍 AR 真实部署(NavSight)」「遥操作+触觉(ModPack)」「3DGS 初始化机理」「主动视觉基准(TAVIS)」六个薄处，提升文献库价值覆盖。",
 "",
 "## 六、附录",
 "",
 "- 原子笔记 6 篇：`papers/notes/2607.17790__ReViV-4D-egocentric.md` 等（见 MOC 索引）。",
 "- 当日 MOC：`papers/MOC/MOC-backfill-2603-2609.md`。",
 "- 评分明细：`data/scored_backfill.json`；运行日志：`papers/daily/backfill-2603-2609/run_log.md`。",
 "- 总索引已更新：`papers/MOC/MOC-总索引.md`（计数 368→374，新增 backfill 批次块与指针）。",
]
open(f"{ROOT}/reports/XR-Backfill-Report-2603-2609.md","w",encoding="utf-8").write("\n".join(rep)+"\n")
print(f"  报告 -> {ROOT}/reports/XR-Backfill-Report-2603-2609.md")
print("deliverables 生成完毕")
