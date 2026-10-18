# -*- coding: utf-8 -*-
"""write_deliverables_1010.py — 生成 2026-10-10 批次的全部交付物：
原子笔记(10) + 当日MOC + 总索引刷新 + 最终解读报告 + run_log 修正 + registry 证据等级修正。
内容来自 Top10 全文(L0/FULL)精读 + 摘要级其余候选。
"""
import json, os, re

ROOT = "D:/Agent/WorkBuddy/Research"
BATCH = "2026-10-10"
ANNOUNCE = "2026-10-09"
scored = json.load(open(f"{ROOT}/data/scored_1010.json", encoding="utf-8"))
# manifest
manifest = {}
mp = f"{ROOT}/data/fulltext/_manifest.json"
if os.path.exists(mp):
    manifest = json.load(open(mp, encoding="utf-8"))

TOP = scored[:10]
top_ids = [s["base_id"] for s in TOP]

# ---------- 1) 修正 registry 证据等级 ----------
reg_path = f"{ROOT}/papers/library/registry.jsonl"
regs = [json.loads(l) for l in open(reg_path, encoding="utf-8") if l.strip()]
for r in regs:
    if r.get("batch") == BATCH:
        bid = r["id"].split(":")[-1]
        fp = f"{ROOT}/data/fulltext/{bid}.txt"
        if os.path.exists(fp):
            r["evidence"] = "FULL"; r["fetch_level"] = "L0"
            r["fulltext_chars"] = manifest.get(bid, {}).get("chars", 0)
        else:
            r["evidence"] = "ABSTRACT_ONLY"; r["fetch_level"] = "L5"
with open(reg_path, "w", encoding="utf-8") as f:
    for r in regs:
        f.write(json.dumps(r, ensure_ascii=False) + "\n")
print("registry 证据等级已修正（Top10=L0/FULL，其余=ABSTRACT_ONLY/L5）")

# ---------- 2) 笔记内容 ----------
# 每篇：标题中文、赛道、一句话、问题、方法、实验、贡献、局限、关系、复现、行动、标签
NOTE = {
"2610.12461": dict(slug="ouroworld-3d-cinemagraph",
  one="OuroWorld 将任意静态 3D 高斯场景自动转化为多视角无缝循环、含多样运动的 3D 电影图（cinemagraph），无需遮罩。",
  prob="现有 3D 世界模型生成的场景是'冻结在时间中'的静态可探索场景，缺乏让场景生动循环运动的能力；多数方法需遮罩或只能产生短暂/不连贯循环。",
  method="mask-free 框架：VLM 推断合理动力学并引导视频模型合成参考视频 → 提升到多视角视频 → 提出 Inconsistency-Robust Periodic 4DGS（傅里叶级数表示周期运动）学习；引入 scene-view consistent optimization（SVCO）与 VLM 过滤缓解不完美监督带来的不一致；提出 ground-truth-free 的 Vividness 指标（Motion/Illumination/Visual Variation）。",
  exp="39 个评估场景（Mip-NeRF 360 / HY-World 2.0 / Marble / Lyra 2.0）。Vividness 全面超越 Gaussians-to-Life / 3D Cinemagraphy / LoopGaussian / 3D-MOM——Illumination Variation 0.0518 vs 各基线 ≤0.0248、Motion Variation 0.0413 vs 0.0588（Gaussians-to-Life 仅循环 0.5s 故 MV 高但 MALF 低）。消融：去除 grounding 主要降低 Motion Variation（0.0413→0.0324）；去除 SVCO 一致性/清晰度最差。含用户研究。",
  contri="首个 mask-free 的 3D cinemagraph 框架；周期性 4DGS 表示；无真值生动度指标。",
  limit="受视频生成先验约束，不合理生成会传播到最终场景（VLM 过滤缓解）；单参考视频在宽视角范围产生更大遮挡与不一致；生成多参考视频是改进方向。",
  rel="补强库内'内容生成/世界模型'方向（与 VISTA-GS/Fusion-Aware 等 3DGS 生成互补，属'静态→动态'拓展）。",
  repro="arXiv v1；项目页未明示代码；评估用 39 场景数据集（部分来自生成式世界模型库）。",
  act="关注其与库内 3DGS 生成路线的范式关系；若开源则纳入动态场景生成基准。",
  tags=["3DGS","4DGS","cinemagraph","内容生成","世界模型"]),
"2610.10811": dict(slug="masking-judder-foveated",
  one="提出用相位偏移噪声掩盖注视点渲染中因低帧率产生的 judder（时域混叠），在不增加高频内容损失的前提下让用户容忍更高相机角速度。",
  prob="注视点渲染在 periphery 降低时空分辨率以省算力，但低帧率导致 judder（时域混叠）降低感知质量；时域滤波/模糊可抑制但增加算力且损失细节。",
  method="从频域建模 judder（时域混叠）：judder 表现为时域频率域的混叠；用相位偏移的噪声占据混叠频带，掩盖 alias 而非消除——在 judder 可察觉的速度处，混叠副本位于远低于注视点截止的空间频率，故去高频既不能隐藏 alias 也不能移除其低频能量，须用平滑移动的噪声能量占据该频带。",
  exp="用户研究（12 名学生，eccentricity 28/35/42°，Forest/City 两地图，5 条件：无 foveation / 两档 foveation / 同两档自适应噪声）。配对 t 检验 + Holm 校正。结果：自适应噪声在高 foveation 下将可容忍角速度提升 1.96×（相对全分辨率）、1.62–1.66× 相对模糊；低 foveation 下噪声吸引力评分与模糊无差异（p=0.83），高 foveation 下 +0.67（p=0.004）表明噪声开始可分辨并分散注意力。",
  contri="首次从频域给出 judder 的 masking 方案；用 StelaCSF 量化噪声可见性随刷新率变化。",
  limit="样本量 12 人偏小；高 foveation 下噪声可被察觉（distraction +0.67）。",
  rel="直接补强库内'渲染与显示'赛道（注视点渲染/省算力），与 10-08 Foveated Compression 互补（彼为 VLM 应用、此为渲染质量机制）。",
  repro="arXiv v1；未明示代码；实验用 60Hz 显示器（更常见的显示类型验证）。",
  act="XR 头显注视点渲染省算力的实用技术，值得纳入渲染管线评估与硬件实现。",
  tags=["注视点渲染","judder","foveated","渲染与显示","感知"]),
"2610.11070": dict(slug="facegan-talking-head",
  one="提出 FaceGAN，用单遍 GAN + 因果噪声整形实现实时音频驱动说话头，25Hz、40ms 音频前瞻，质量匹配/超越扩散模型且无需蒸馏。",
  prob="音频驱动面部动画需在线流式运行（每帧由截至当前的音频生成）；扩散模型需多次网络评估不适合流式；单遍 GAN 受限于'随机结构'——因果时不变生成器无法在不坍塌逐帧创新的情况下抑制某频段谱。",
  method="解耦身份与动画；证明障碍在噪声通路而非容量。FaceGAN 通过'因果噪声整形'（acausal noise shaping）化解：驱动噪声是合成的，其未来可现在采样，故音频-表情路径保持因果，模型支持完全因果运行。单前向 pass 每帧输出表情+头部姿态，有界注意力窗口，可无限生成不漂移。",
  exp="对比 MemoryTalker / DiffPoseTalk / 扩散模型（Table 7 等）；25Hz、40ms 前瞻；质量 match/outperform SOTA；实时基准显示单遍前向延迟低、支持无限长生成不漂移。",
  contri="论证该领域单遍 GAN 已足够，推翻扩散主导假设；acausal noise shaping 化解频谱限制而不牺牲因果性。",
  limit="来自 Meta Reality Labs，闭源可能性高；'低维流形'假设可能不适用于极端表情/身份。",
  rel="补强库内'化身与人体/实时说话头'方向（与 GaussianAvatars 等互补，属'流式低延迟'路线）。",
  repro="Meta Reality Labs；代码未公开（v1）；方法基于 StyleGAN-T 等现代 GAN 基线。",
  act="实时数字人/telepresence 的关键实用路线；持续跟踪其是否开源与移动端部署。",
  tags=["说话头","telepresence","GAN","实时","化身与人体","Meta"]),
"2610.11815": dict(slug="fast-pose-tracking",
  one="提出轻量跟踪模块，叠在多种对应估计方法之上，用紧凑位姿图优化（不确定性感知 PGO）保持 6D 位姿跟踪低漂移、快速度，适用于机器人操作与 AR。",
  prob="长时程 6D 位姿跟踪需昂贵 onboarding 或全程维护重建，对机器人操作/AR 不实用；需要即开即用、实时。",
  method="避免点基优化，改用紧凑位姿图；关键思想是不在点云里逐点优化，而是用不确定性感知 PGO——在几何歧义（无纹理/薄物体）情况下建模不确定性提升鲁棒性。",
  exp="HOI4D 刚体物体 5 类；AUC@10° 旋转精度领先 3/5 非 CAD 类、平均 46.5 vs BundleTrack 44.2 / BundleSDF 43.5 / UNOPose 40.8 / FoundationPose(CAD) 32.2；定性显示不确定建模改善纹理少/薄物体鲁棒性。",
  contri="与上游对应估计方法解耦的即插即用跟踪；不确定性感知 PGO 在歧义场景下防漂移。",
  limit="仅刚体；依赖上游对应估计质量；长时程/非刚体未覆盖。",
  rel="补强库内'重建与SLAM/姿态跟踪'赛道（与 VGGSfM/VGGT/FoundationPose 类互补）。",
  repro="arXiv v1；未明示代码；HOI4D 公开数据集。",
  act="AR 物体跟踪/机器人操作的实用组件；关注其对接主流对应估计器的泛化。",
  tags=["6D位姿","姿态跟踪","SLAM","AR","机器人"]),
"2610.11011": dict(slug="pcasplat",
  one="提出 PCAsplat，用局部 PCA 正则化约束 3D 高斯的方向/尺度，抑制被遮挡/少贡献高斯漂移产生的游离（floater）伪影。",
  prob="现有 3DGS 主要用光栅化损失监督，仅当 splat 贡献于采样射线时才被监督；被遮挡/少贡献高斯获得弱或零几何梯度，漂离表面产生 floaters。",
  method="几何感知的局部 PCA 正则化框架：约束每个高斯的形状（方向/尺度）贴合其局部表面结构，使不在采样射线上的高斯基也能获得几何约束而不漂离。",
  exp="NeRF Synthetic / ScanNet++ / DTU；对比多种 SOTA（用各自 GitHub 最新超参复现，保证可复现性一致口径）；VGGT-Ω 用深度反投影+相似变换对齐坐标系。结果 Tab.1/Tab.3 报告几何与渲染指标。",
  contri="针对性解决 3DGS floaters 的几何正则，不改表示、易插入现有 pipeline。",
  limit="正则化强度需调；对极度稀疏视角可能不足；消融细节依赖复现。",
  rel="补强库内'神经渲染/3DGS'赛道（与 TileSkipper/PePESeg3D/ManifoldSplat 等 3DGS 质量方向互补）。",
  repro="arXiv v1；未明示代码；多数据集公开。",
  act="3DGS 重建质量提升的实用组件；关注其与库内'逐高斯压缩/结构化表示'路线的关系。",
  tags=["3DGS","floaters","正则化","神经渲染","重建"]),
"2610.10945": dict(slug="gharp-head-animation",
  one="GHARP 在学习的规范高斯表示上实时动画 3D 头部化身，用 8× 更少高斯、数量级更低推理成本达到 SOTA 质量；BAN 提升时序稳定性。",
  prob="实时头部化身需兼顾保真度/质量/速度；多视角输入下动画成本随视角数增长，难以即开即用。",
  method="解耦为身份阶段（离线建规范高斯表示，固定规模高斯捕捉几何与外观）+ 动画阶段（运行时在规范表示上预测表情残差）。Body Alignment Network（BAN）在训练中解决身体外观不一致，提升动画时序稳定。",
  exp="Ava-256 / Internal10K；AKD/CSIM 最优；仅 65K 高斯（vs Avat3r 182K–730K、FastGHA 150K–602K）；推理 1.92ms、iPhone 17 Pro 上 1.45ms；BAN 使 body 时序 σ 低一个数量级；跨身份重定目标 AED 5.35（优于基线）。",
  contri="规范表示解耦使动画成本与视角数无关；BAN 身体稳定；8× 更少高斯 + 数量级更低推理成本。",
  limit="依赖标定相机位姿（估计不准会传播）；未做时序噪声鲁棒/材质分解；仅限头部。",
  rel="补强库内'化身与人体/实时高斯头部化身'方向（与 10-09 边缘头部化身、Fresco++ 互补）。",
  repro="arXiv v1；未明示代码；Ava-256/Internal10K 数据集。",
  act="移动端实时头像的强候选；关注其与 Fresco++ 的优化范式差异。",
  tags=["头部化身","高斯","实时","avatar","化身与人体"]),
"2610.11181": dict(slug="mate4d",
  one="MATE4D 从单张图像生成可编辑的动态 4D 内容，用'图像矩阵模块(IMM)'+'背景编辑(BEM)'+'动态信息输入(DII)'，在 Objaverse-XL / Diffusion4D 上 FVD 大幅领先。",
  prob="单图→4D 因单视角结构线索有限、运动证据弱，难以生成时序稳定且真实的可编辑 4D。",
  method="构建时空多视角图像矩阵（文本引导背景操纵）提供视角/外观/运动一致监督；IMM 保证多视角一致；BEM 文本引导背景/光照编辑；DII 注入动态信息。",
  exp="Objaverse-XL（千万级 3D 物体渲染多视角序列）、Diffusion4D；FVD-F/FVD-Diag/FVD4D 全面领先（MATE4D 273.9/457.3/397.3 vs 次优 Gaussian-Flow 370.5/555.6/618.8）。消融：全模型 CLIP-I 0.962/PSNR 38.76/FVD4D 175.8；去 IMM FVD4D 升至 421.6 证明 IMM 不可或缺；加 DII 后 FVD4D 降至 213.7。",
  contri="单图可编辑 4D 生成；用图像矩阵提供一致监督是核心。",
  limit="依赖多视角图像矩阵的合成质量；复杂/快速运动泛化待验；编辑一致性依赖文本引导。",
  rel="补强库内'内容生成/4D 生成'方向（与 4DGS-JEPA/ VISTA-GS 互补，属'单图→4D'路线）。",
  repro="arXiv v1；未明示代码；Objaverse-XL/Diffusion4D 公开。",
  act="单图 4D 内容创作的实用框架；关注其 4D 一致性指标与库内 4DGS 路线的对比。",
  tags=["4D生成","单图","可编辑","内容生成","视频扩散"]),
"2610.11412": dict(slug="fresco-head-avatar",
  one="Fresco++ 是精细且视角一致的头部化身统一优化框架，用'空间局部频率课程'+'规范组共识(CGC)'稳定优化、跨视图一致，可迁移到 GaussianAvatars/TensorGA。",
  prob="头部化身高度耦合优化易陷不稳定局部解：高频细节在可靠粗结构形成前被拟合，局部外观/结构跨视图漂移。",
  method="不重设计表示，从两方面规范优化：空间局部频率课程（粗→细，先稳定低频再细化高频）+ CGC（在规范域建立对应、多视图共识形成可靠跨视图监督）。主实现用混合 mesh–Gaussian（FLAME 面部 + 3DGS 头发/周边）。",
  exp="新视角合成 + reenactment 对比；受控消融（频率课程顺序、CGC vs UV-space 一致性）；表示可迁移性研究（GaussianAvatars/TensorGA，额外训练成本但推理效率不变）；四个互补视角评估。",
  contri="频率课程 + 规范组共识的通用优化范式；可迁移到不同高斯化身表示。",
  limit="仍需底层表示训练；额外训练成本（迁移时）；未覆盖极端姿态/光照。",
  rel="与 GHARP、库内头部化身方向互补（优化范式层面，与 10-09 边缘头像、GHARP 形成'表示/优化/实时'三角）。",
  repro="arXiv v1；未明示代码；对比 GaussianAvatars/TensorGA 等。",
  act="头部化身训练稳定性的通用改进；关注其迁移到库内现有化身表示的收益。",
  tags=["头部化身","优化","频率课程","规范共识","化身与人体"]),
"2610.12299": dict(slug="me-world-multiagent",
  one="ME-World 将多智能体第一视角世界模型建模为共享世界中多 agent 经细粒度动作交互的同步 ego-stream 生成，联合去噪多流、共享环境记忆，提升共享世界一致性/动作控制/视频质量。",
  prob="现有第一视角世界模型多为单 agent；多 agent 世界模型只用粗粒度动作（移动/相机/离散指令），细粒度具身交互未充分探索；需跨视图动作一致性、共享环境一致性、交互引发状态更新的传播。",
  method="在共享 token 序列联合去噪多 ego 流；每流条件于所有 agent 的目标视角位姿；共享环境记忆（SEM）grounding 生成。基于 Cosmos-Predict2.5 2B 微调 DiT（冻结 VAE/文本编码器，rectified-flow，A100×4 训练，35 步推理、CFG 7.0）。",
  exp="真实+合成多 agent 数据；提出共享世界一致性指标（环境/更新/身份一致性）；对比多视图视频生成（GEN3C/AnyView-DVS）、单 ego 世界模型（EgoSim/JointControlVideo）、通用世界模型（DreamX-World/LingBot-World）及多 agent 基线（MultiWorld/Solaris/γ-World/MetaWorld）。ME-World 全部指标最优；消融：SEM + Joint Gen + Shared Action 逐步提升（Senv 0.456）。",
  contri="细粒度具身交互的多 agent 第一视角世界模型；共享环境记忆；新一致性指标。",
  limit="基于扩散 Transformer，算力重；真实数据规模有限；交互种类受数据集约束。",
  rel="补强库内'世界模型与仿真'方向（与 World SLAM Model/Dexterous Tactile World Model 互补，属'多 agent 共享世界'拓展）。",
  repro="项目页 cvlab-kaist.github.io/ME-World；KAIST；Cosmos-Predict2.5 开源 backbone。",
  act="具身多智能体仿真/社交 XR 的关键方向；关注其共享世界一致性指标是否成为基准。",
  tags=["世界模型","多智能体","具身","第一视角","仿真"]),
"2610.12442": dict(slug="lego-exo2ego",
  one="LEGO 提出 lifting-free 的外中心→内中心视频生成：用学习的视图合成器（LVSM 式 transformer，无需深度/点云/重投影）直接渲染内中心视图作为视频扩散模型的条件，避免深度误差导致的内容错位。",
  prob="从单张外中心视频生成内中心视频是难的新视角合成（两相机重叠少、目标视图多未观测）；SOTA 显式重建（深度→点云→重投影渲染）的确定性映射把每个像素指派到单一重投影位置，保留纹理但把深度误差转成错位内容（手/近物最明显）。",
  method="论证条件应'先对齐再清晰'——生成器更易恢复细节而非纠正错位内容；用学习的视图合成器渲染内中心视图（LVSM 式，内部解决跨视图对应），其概率映射按学习到的对应分布对候选源位置取平均，保留结构、细纹理被平均掉；置信门控 + ARC（无需重训练的引导）。",
  exp="Ego-Exo4D（按 EgoX 协议）seen/unseen 两 split；优于 EgoX 所有图像指标与 FVD（seen：PSNR 15.52 vs 13.74、LPIPS 0.545 vs 0.573、FVD 332.41 vs 421.83；unseen 类似）。消融：条件输入（合成器渲染 > 点云渲染 > 空）、门控、引导逐项贡献；无 GT 的 in-the-wild 视频上差距更大。",
  contri="lifting-free conditioning 范式；置信门控 + 训练免费引导；冻结合成器可零重训练迁移到新场景/录制。",
  limit="细纹理被平均掉（概率映射的代价）；依赖 LVSM 合成器质量；未覆盖极端相机轨迹。",
  rel="补强库内'感知与认知/新视角合成/自我中心'方向（与 EgoLAP/库内 ego 视频生成互补）。",
  repro="代码+HF 已发布（github.com/suhwan-cho/lego）；GenGenAI；Ego-Exo4D 公开。",
  act="第一视角视频生成/AR 巡检的实用方法（已开源）；优先纳入 ego→exo 工具链评估。",
  tags=["新视角合成","自我中心","视频扩散","lifting-free","感知与认知"]),
}

# ---------- 3) 写原子笔记 ----------
notes_dir = f"{ROOT}/papers/notes"
os.makedirs(notes_dir, exist_ok=True)
for s in TOP:
    bid = s["base_id"]
    n = NOTE[bid]
    sc = s["scores"]
    fm = f"""---
id: arXiv:{bid}
title: "{s['title']}"
title_zh: "{s['title_zh']}"
track: {s['track']}
venue: arXiv preprint 2026-10-09
date: {ANNOUNCE}
value: {s['value']}
grade: {s['grade']}
evidence: FULL
status: CURRENT
superseded_by: []
scores: {{IMP:{sc['IMP']}, NOV:{sc['NOV']}, TEC:{sc['TEC']}, EXP:{sc['EXP']}, PER:{sc['PER']}, TRL:{sc['TRL']}, REP:{sc['REP']}}}
fetch_level: L0
tags: [{', '.join(n['tags'])}]
---

# {s['title_zh']}

## 一句话结论
{n['one']}

## 要解决的问题
{n['prob']}

## 方法详解
{n['method']}

## 实验与结果
{n['exp']}

## 创新点与贡献
{n['contri']}

## 局限与风险
{n['limit']}

## 与文献库的关系（新增 / 改进 / 取代 X）
{n['rel']}

## 可复现性（代码/数据/硬件）
{n['repro']}

## 行动建议
{n['act']}
"""
    fn = f"{notes_dir}/{bid}__{n['slug']}.md"
    open(fn, "w", encoding="utf-8").write(fm)
print(f"原子笔记 {len(TOP)} 篇已写 -> {notes_dir}")

# ---------- 4) 当日 MOC ----------
moc = f"""# MOC · {BATCH}（XR 每日论文雷达）

> 拉取日 {BATCH}（周六）· submittedDate 批次 {ANNOUNCE}（周五）· 新提交 XR 核心相关 **25 篇**（含 Top10 全部 A 级，最高 3.90）；另剔除 2 篇非 XR + 4 篇旧稿再公告单列 backfill。无 S 级（非重磅日，当日最高 3.90 < 库近 30 天 Top10 均分 3.903）。
> 数据源：arxiv.org/api/query 探针 200 但 submittedDate 前沿停滞 10-08；rss.arxiv.org 200 → **RSS 兜底**（7 分类全量去重 828 条）。Top10 全文 10 篇全部 **L0/FULL**。

## 排行榜（按重要性降序）

| 排名 | arXiv | 标题 | 赛道 | 总分 | 等级 | 笔记 |
|---|---|---|---|---|---|---|
"""
rank = 1
for s in TOP:
    n = NOTE[s["base_id"]]
    moc += f"| {rank} | {s['base_id']} | {s['title_zh']} | {s['track']} | {s['value']:.2f} | {s['grade']} | [笔记](../notes/{s['base_id']}__{n['slug']}.md) |\n"
    rank += 1
moc += "\n## 赛道分布\n\n"
track_map = {}
for s in TOP:
    track_map.setdefault(s["track"], []).append(s["base_id"])
for t, ids in sorted(track_map.items()):
    moc += f"- **{t}**：" + "、".join(ids) + "\n"
moc += "\n## 落后/路线观察\n\n"
moc += "- 本期 **OUTDATED/SUPERSEDED 0 篇**（门① 最大 Jaccard 0.357 < 0.62，无同质取代）。\n"
moc += "- 路线观察：头部化身方向本期集中 3 篇（GHARP 实时规范表示 / Fresco++ 优化范式 / 延续 10-09 边缘头像），与库内'逐高斯压缩/结构化表示'并行，构成'表示-优化-实时'三角，关注后续收敛信号。\n"
moc += "- 内容生成方向本期 OuroWorld（静态→动态 cinemagraph）与 MATE4D（单图→4D）互补，均建立在 3DGS/视频扩散之上。\n"
moc += "\n## 其余 XR 候选（B/A 级，未入 Top10，详见 [7 维表](../../papers/daily/2026-10-10/7dim-table.md)）\n\n"
rest = [s for s in scored if s["base_id"] not in top_ids]
for s in rest:
    moc += f"- {s['base_id']}（{s['grade']} {s['value']:.2f} [{s['track']}]）{s['title_zh']}\n"
moc += f"\n## 参考\n- 运行报告：[XR-Daily-Report-{BATCH}.md](../../reports/XR-Daily-Report-{BATCH}.md)\n- 7 维参考表：[daily/{BATCH}/7dim-table.md](../../papers/daily/{BATCH}/7dim-table.md)\n"
open(f"{ROOT}/papers/MOC/MOC-{BATCH}.md", "w", encoding="utf-8").write(moc)
print(f"当日 MOC -> papers/MOC/MOC-{BATCH}.md")

# ---------- 5) 总索引刷新 ----------
total_moc = f"{ROOT}/papers/MOC/MOC-总索引.md"
tm = open(total_moc, encoding="utf-8").read()
# 更新计数 374 -> 399
tm = tm.replace("累计 **374 篇**", "累计 **399 篇**")
tm = tm.replace("原子笔记目录](../notes/)（现有 122 篇）", "原子笔记目录](../notes/)（现有 132 篇）")
# 最新一期指针
tm = tm.replace("[MOC · 2026-10-09](./MOC-2026-10-09.md)", f"[MOC · {BATCH}](./MOC-{BATCH}.md)")
# 顶部追加状态注记（在最后一个状态注记后、--- 前插入）
note_new = (f"> **状态注记（{BATCH}）**：周六，arXiv API（arxiv.org/api/query）探针 200 但 `submittedDate` 前沿停滞 10-08，"
            f"真实新增由 **RSS 兜底**（公告日/批次 {ANNOUNCE}，周五提交）。本调度入选 **XR 新稿 25 篇**（Top10：10 A，最高 3.90；"
            f"另 15 篇 B/A 级 XR 候选入馆、2 篇非 XR + 4 篇旧稿再公告剔除）；Top10 全文 10 篇全部 **L0/FULL**；"
            f"三关通过（门① 最大 Jaccard 0.357；门② 覆盖 7 赛道；门③ 最高 3.90 < 库近 30 天 Top10 均分 3.903，**非重磅日无 S 级**）、无重筛、无 OUTDATED。"
            f"详见 [运行报告](../../reports/XR-Daily-Report-{BATCH}.md)。\n")
# 插入到首个 `---` 之前（即状态注记区块之后）
idx = tm.find("\n---\n")
if idx > 0:
    tm = tm[:idx] + "\n" + note_new + tm[idx:]
# 在 A 级表中追加本期 Top10（A 级）行
a_sec = tm.find("### A 级（")
if a_sec > 0:
    # 找到该段末尾（下一个 ### 或 ## 三）
    nxt = tm.find("\n### ", a_sec + 10)
    if nxt < 0: nxt = tm.find("\n## ", a_sec + 10)
    ins = "\n### 2026-10-10 新增（A 级，10 篇，非重磅日）\n\n| 论文 | 赛道 | 分值 | 日期 | 状态 | 笔记 |\n|---|---|---|---|---|---|\n"
    for s in TOP:
        n = NOTE[s["base_id"]]
        ins += f"| {s['title_zh']} | {s['track']} | {s['value']:.2f} | {ANNOUNCE} | ✅ | [→](../notes/{s['base_id']}__{n['slug']}.md) |\n"
    tm = tm[:nxt] + ins + "\n" + tm[nxt:]
open(total_moc, "w", encoding="utf-8").write(tm)
print("总索引已刷新（计数 374→399、最新一期指针、A 级表、状态注记）")

# ---------- 6) run_log 修正 ----------
rl_path = f"{ROOT}/papers/daily/{BATCH}/run_log.md"
rl = open(rl_path, encoding="utf-8").read()
rl = rl.replace("fetch_fulltext.py 对 Top10 + 候选共 N 篇抓取（L0/FULL 优先），串行 3s/篇；manifest 校验。",
                "fetch_fulltext.py 对 Top10 共 10 篇抓取，**全部 L0/FULL**（arxiv.org/html，串行 3s/篇，无限流/降级/伪造）；manifest 合并写入校验通过；其余 15 篇 XR 候选（B/A 级）基于摘要评估（ABSTRACT_ONLY）。")
open(rl_path, "w", encoding="utf-8").write(rl)
print("run_log 已修正（全文 10 篇 L0/FULL）")

# ---------- 7) 最终解读报告 ----------
def chapter(s):
    bid = s["base_id"]; n = NOTE[bid]; sc = s["scores"]
    return (f"## 第 {CHAPTER_NO[bid]} 章 · {s['title_zh']}（{s['grade']} 级 · {s['value']:.2f} · {s['track']}）\n\n"
            f"> arXiv:{bid} ｜ 赛道：{s['track']} ｜ 证据等级：FULL（L0 全文） ｜ 状态：CURRENT\n\n"
            f"**一句话结论**：{n['one']}\n\n"
            f"### 要解决的问题\n{n['prob']}\n\n"
            f"### 方法详解\n{n['method']}\n\n"
            f"### 实验与结果\n{n['exp']}\n\n"
            f"### 创新点与贡献\n{n['contri']}\n\n"
            f"### 局限与风险\n{n['limit']}\n\n"
            f"### 与文献库的关系\n{n['rel']}\n\n"
            f"### 可复现性\n{n['repro']}\n\n"
            f"### 行动建议\n{n['act']}\n")

CHAPTER_NO = {bid: i+1 for i, s in enumerate(TOP)}

# 读 7 维表
dim_tbl = open(f"{ROOT}/papers/daily/{BATCH}/7dim-table.md", encoding="utf-8").read()

report = f"""# XR 每日论文雷达 · 解读报告（{BATCH}）

> 拉取日 **{BATCH}**（周六）｜arXiv submittedDate 批次 **{ANNOUNCE}**（周五提交）｜数据源：rss.arxiv.org 兜底（API submittedDate 前沿滞后于 10-08）。
> 7 维权重：IMP0.20 · NOV0.20 · TEC0.15 · EXP0.15 · PER0.15 · TRL0.08 · REP0.07。档位 S≥4.20 · A 3.60–4.20 · B 3.00–3.60 · C<3.00。

## 一、执行摘要

- **实际命中区间**：arXiv submittedDate 批次 {ANNOUNCE}（周五提交），拉取日 {BATCH}（周六，周末节律）。本报告**绝不伪装"当日新论文"**——上游 API submittedDate 索引前沿停滞于 10-08，RSS 兜底抓到的是 {ANNOUNCE} 周五提交批次。
- **入选规模**：去 registry（374）后新提交 XR 核心相关 **25 篇**（2610.*）；剔除 2 篇非 XR（CoCam4D 自动驾驶、OX-NeRF 医学 X 射线）+ 4 篇旧稿再公告（2602/2603/2605）单列 backfill。
- **Top10**：全部 **A 级**（最高 3.90，最低 3.70），**无 S 级**。
- **赛道覆盖**：7 个赛道（内容生成 / 渲染与显示 / 化身与人体 / 重建与SLAM / 神经渲染 / 世界模型与仿真 / 感知与认知）——覆盖度门②通过。
- **重要发现**：① 头部化身方向本期集中爆发（GHARP 实时规范表示、Fresco++ 优化范式、延续 10-09 边缘头像），与库内"逐高斯压缩/结构化表示"并行；② 内容生成从"静态 3DGS"走向"动态 cinemagraph"（OuroWorld）与"单图→4D"（MATE4D）；③ 注视点渲染的 judder masking（2610.10811）与 FaceGAN 流式说话头是两条强实用型 XR 工程路线。
- **诚实口径**：门③ 当日最高 3.90 < 库近 30 天 Top10 均分 3.903 → **非重磅日，未拔高、未虚构 S 级**。

## 二、Top10 排行榜（按重要性降序）

| 排名 | arXiv | 标题 | 赛道 | 总分 | 等级 |
|---|---|---|---|---|---|
"""
for i, s in enumerate(TOP, 1):
    report += f"| {i} | {s['base_id']} | {s['title_zh']} | {s['track']} | {s['value']:.2f} | {s['grade']} |\n"
report += "\n## 三、逐篇深度解读（每篇一章，按重要性降序）\n\n"
for s in TOP:
    report += chapter(s) + "\n---\n\n"
report += ("## 四、当日全量 7 维度对比表（参考）\n\n"
           "> 下表为本次 {ANNOUNCE} 批次全部 25 篇 XR 新稿的 7 维评分参考；Top10 已全文精读（见 §三），其余 B/A 级候选基于摘要评估。\n\n")
report += dim_tbl.split("\n", 1)[1] if "\n" in dim_tbl else dim_tbl
report += ("\n\n## 五、覆盖率校验与筛选过程说明\n\n"
           f"- **门① 同质去重**：Top10 与文献库（399 篇）标题+摘要 token Jaccard 最大 **0.357**（2610.10945 vs 库内 Budgeted-GS），远低于 0.62 阈值 → **通过，无同质重复**。\n"
           f"- **门② 方向覆盖度**：Top10 覆盖 **7 个赛道**（≥5 通过），无筛选偏食。\n"
           f"- **门③ 价值天花板**：当日最高 {max(s['value'] for s in scored):.2f} < 库近 30 天 Top10 均分 3.903 → **非重磅日，无 S 级，未拔高**。\n"
           "- **重筛闭环**：三关全部通过，未触发重筛；所有入选在价值维度上已覆盖当前文献库主航道（无冷门高价值候选被漏）。\n"
           "- **诚实处理**：剔除 2 篇非 XR（CoCam4D 自动驾驶、OX-NeRF 医学 X 射线断层）与 4 篇旧稿再公告（2602.03538/2603.13833/2605.22342/2605.27820），旧稿建议 API 健康时单开 backfill。\n\n"
           "## 六、附录：抓取失败/降级清单与证据等级\n\n"
           "- **全文抓取**：Top10 共 10 篇，全部 **L0 / FULL**（arxiv.org/html 源，35K–99K 字符，串行 3s/篇，无限流/降级/伪造）；manifest 合并写入校验通过。\n"
           "- **其余 15 篇 XR 候选**（B/A 级，未入 Top10）：基于摘要评估，证据等级 **ABSTRACT_ONLY**（L5），已在 7 维表与 MOC 标注，未生成逐篇笔记。\n"
           "- **落后标注**：本期 **OUTDATED/SUPERSEDED 0 篇**；路线级观察 2 条（头部化身'表示-优化-实时'三角、内容生成'静态→动态/单图→4D'），均以 CURRENT 记录、未判取代。\n"
           "- **数据源**：arxiv.org/api/query 探针 200 但 submittedDate 前沿停滞 10-08；rss.arxiv.org 200 → RSS 兜底；无 404/406 阻断，无推迟重跑。\n")
open(f"{ROOT}/reports/XR-Daily-Report-{BATCH}.md", "w", encoding="utf-8").write(report)
print(f"最终解读报告 -> reports/XR-Daily-Report-{BATCH}.md")
print("\n全部交付物生成完毕。")
