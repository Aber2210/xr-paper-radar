#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Generate XR Daily Brief deliverables for 2026-10-06 from scored evidence.
Produces: 7dim-table, scored, run_log, 10 atomic notes, daily MOC, full report, registry update.
"""
import json, os, datetime

ROOT = "D:/Agent/WorkBuddy/Research"
DATE = "2026-10-06"
BATCH = "2026-10-06"

# ---------- load fulltext manifest for char counts ----------
manifest = {}
mp = os.path.join(ROOT, "data/fulltext/_manifest.json")
if os.path.exists(mp):
    try:
        manifest = json.load(open(mp, encoding="utf-8"))
    except Exception:
        manifest = {}

def fchars(bid):
    m = manifest.get(bid, {})
    return m.get("chars", 0)

# ---------- the 10 scored papers (evidence-based) ----------
# weights: IMP .20 NOV .20 TEC .15 EXP .15 PER .15 TRL .08 REP .07
W = dict(IMP=.20, NOV=.20, TEC=.15, EXP=.15, PER=.15, TRL=.08, REP=.07)
def value(s):
    return round(sum(W[k]*s[k] for k in W), 2)
def grade(v):
    if v>=4.2: return "S"
    if v>=3.6: return "A"
    if v>=3.0: return "B"
    return "C"

PAPERS = [
{
 "id":"arXiv:2610.03162","bid":"2610.03162","title":"Budgeted-GS: Real-Time Large-Scale Gaussian Splatting via Factoring LOD",
 "title_zh":"Budgeted-GS：基于因式分解 LOD 的实时大规模高斯泼溅",
 "track":"渲染与显示","authors":"Haipeng Wang",
 "scores":{"IMP":5,"NOV":4,"TEC":5,"EXP":5,"PER":5,"TRL":4,"REP":4},
 "one":"提出 Budgeted-GS，将任意训练好的 3DGS 模型转化为“因式树”多分辨率层级，并按目标设备显存自动选 LOD；首次给出可理论量化的“容量下限/预算-误差定律”，在消费级 GPU 上以原生 1080p 全 SH 实时渲染城市级场景。",
 "problem":"3D Gaussian Splatting 在城市场景下携带数百万高斯、数 GB 显存，消费级 GPU 无法实时高质渲染；且训练时盲目堆高斯再压缩浪费算力。",
 "method":"后处理法——构造“因式树”（moment-matched aggregates 的多分辨率层级），数秒构建后单一质量参数按视角选择 LOD 以适配显存；训练侧法——先测场景所需基元数再直接按预算训练。理论支撑：基于相空间最优传输的预算-误差定律 + covering theorem 认证冗余基元选择；实时 CUDA 光栅路径去除每帧选择开销。",
 "exp":"13 个公开场景在 preregistered 协议下验证容量下限；从物体场景到官方城市场景捕获，单消费级 GPU 以原生 1920x1080、全 SH 实时渲染（实测约 71 fps 全集合 1080p）。",
 "nov":"可理论量化的容量下限回答“场景到底需要多少高斯、可安全舍弃多少”；训练-推理统一的预算理论；LOD 因式树适配异构设备显存。",
 "limit":"依赖已训练 3DGS（后处理路线）；极端动态/无结构场景未验证；容量下限假设需满足覆盖定理条件，普适性待考。",
 "lib":"库内已有大量 3DGS 压缩/抽象（COSA-GS、MoQSplat、TopoGS、SplatLabel、PePESeg3D、Observation-Gram、GS-PQM 等）。Budgeted-GS 是首篇给出理论容量下限 + 训练侧预算控制的，区别于“逐高斯压缩”，属互补而非取代。",
 "repro":"preregistered 协议、官方城市场景、CUDA 光栅器；论文提及代码/项目页（以正文 URL 为准）。",
 "action":"城市场景/设备端 3DGS 部署优先采用；关注容量下限的普适性与跨数据集验证。",
},
{
 "id":"arXiv:2610.03283","bid":"2610.03283","title":"HexVIO: Towards All-Day Stereo-Inertial Tracking Through Commodity DSPs",
 "title_zh":"HexVIO：借助商用 DSP 实现全天候立体-惯性追踪",
 "track":"重建与SLAM","authors":"Patrick Wolf, Mateo de Mayo, Daniel Cremers",
 "scores":{"IMP":5,"NOV":4,"TEC":5,"EXP":5,"PER":5,"TRL":4,"REP":3},
 "one":"将立体-惯性 VIO 的视觉前端卸载到骁龙 Hexagon DSP、后端留主 CPU，在商用手机上实现 67% 功耗下降或 86% 吞吐提升，0.83W 维持 30fps 实时追踪约 18 小时——为 XR/可穿戴“全天追踪”提供系统级解法。",
 "problem":"XR/可穿戴设备需要全天、低温、长续航的 VIO；纯 CPU 实现高功耗、低吞吐。",
 "method":"利用 commodity Hexagon DSP（HVX 宽 SIMD + HMX 矩阵单元 + VTCM 紧耦合内存）；前端（金字塔/检测/追踪）DSP 化、后端 CPU；FastRPC 共享内存跨边界零拷贝；稀疏特征采样需驻留 VTCM。",
 "exp":"7 个 EuRoC 类序列（EV102/EMH03/TR2/TR6/MOO02/MOO08/XWALK）做 CPU vs DSP 对比，指标含 ATE/RTE/FPS/前后端时延；DSP 前端时延由 ~7–9ms 降到 ~2ms，端到端 p99 约 14.7ms；30fps、0.83W 长时追踪。",
 "nov":"把 VIO 前端搬上 commodity DSP 的系统工程创新；量化“全天追踪”续航（约 18 小时）；真实手机实现的参考价值极高。",
 "limit":"绑定特定 DSP 架构（骁龙 V73）；后端尚未 DSP 化；主要评 EuRoC 类室内序列，室外/大场景未覆盖。",
 "lib":"库内已有大量 SLAM/VIO（RRG-SLAM、KYS-SLAM、DAVIO、World SLAM Model、FMCW-LIO 等），HexVIO 的增量在“低功耗硬件落地”维度，与算法型 VIO 互补。",
 "repro":"真实手机实现 + 详细 DSP 架构描述；倾向有代码（以正文为准）。",
 "action":"XR 一体机/眼镜续航优化的重要参考；关注后端 DSP 化与跨芯片移植。",
},
{
 "id":"arXiv:2610.03192","bid":"2610.03192","title":"PocketSplat: Mobile Gaussian Reconstruction via World-Space Latent Allocation",
 "title_zh":"PocketSplat：基于世界空间潜分配的移动端高斯重建",
 "track":"神经渲染","authors":"Wenzhi Guo 等",
 "scores":{"IMP":5,"NOV":4,"TEC":4,"EXP":5,"PER":4,"TRL":4,"REP":3},
 "one":"前馈式“预算可控”移动端高斯重建框架：给定输出预算在世界空间分配整型容量，在 iPhone 上直接构建比可部署 MVSplat 更紧凑、更高质量的资产且显著更快，原生 MVSplat/DepthSplat 超出设备显存。",
 "problem":"移动端高斯重建需同时满足“模型在设备算力包络内运行”与“资产大小适配下游移动使用”；现有前馈重建解码稠密图像对齐候选，基数由输入分辨率/视角隐式决定。",
 "method":"图像条件世界空间 latent 场 + 预算条件高斯解码器；在预测世界空间组织几何感知 latent 候选，按局部 cell 分配精确整型容量，仅对保留候选解码完整高斯属性；cell-conditioned latent 融合聚合多视角证据；spatial responsibility decoding 局部稀疏化后适配高斯支撑。",
 "exp":"DL3DV 与 OOD 基准建立质量-预算权衡；Mip-NeRF 360 上在目标 iPhone 直接运行，构建比可部署 streamed MVSplat 变体更快的紧凑高质量资产；原生 MVSplat/DepthSplat 超出设备显存。",
 "nov":"显式预算控制（整型容量分配）而非隐式决定基数；世界空间 latent 聚合多视角证据；面向真机部署验证。",
 "limit":"预算固定后灵活性受限；依赖前馈假设；主要在 DL3DV/Mip-NeRF 360 评测，跨域泛化待考。",
 "lib":"库内 3DGS 重建多侧重离线质量；PocketSplat 补“移动端实时预算重建”缺口，与 Budgeted-GS（后处理压缩）形成“训练侧预算 vs 后处理预算”双路线。",
 "repro":"真机 iPhone 实验 + 对比基线；倾向有代码（以正文为准）。",
 "action":"移动 XR 内容生成/扫描首选关注；与 Budgeted-GS 组合（重建 + 部署压缩）。",
},
{
 "id":"arXiv:2610.03607","bid":"2610.03607","title":"World Action Learning via Interaction-Centric Spectral Latent Guidance (WING)",
 "title_zh":"WING：基于交互中心谱域潜引导的世界动作学习",
 "track":"感知与认知","authors":"Zhiming Liu 等",
 "scores":{"IMP":4,"NOV":4,"TEC":4,"EXP":5,"PER":5,"TRL":3,"REP":3},
 "one":"WING 从第一视角（egocentric）视频把“交互中心”的运动知识迁移到机器人策略，用谱域低频对齐跨具身共享语义，在 LIBERO 99.2%、RoboTwin 2.0 93.8%、RoboCasa-GR1 57.7% 及 4 项真实操作任务上显著优于基线。",
 "problem":"机器人策略需海量真实交互数据、成本高；egocentric 视频丰富但帧重建潜动作易被相机自身运动等干扰主导，且人-机器人时序动态不同。",
 "method":"先分离观察者诱导运动与手-物交互，把交互中心成分蒸馏为潜动作；利用跨具身任务语义集中于慢变时序结构的观察，在谱域识别 egocentric 潜动作与机器人行为的共享低频成分（DCT 低频分量），引导动作生成。",
 "exp":"LIBERO 99.20%、RoboTwin 2.0 93.80%、RoboCasa-GR1 57.7%；4 项真实操作任务多泛化设置；4 个研究问题 + 消融（observer debiasing、spectral guidance、DCT 分量数、ego 预训练策略）。",
 "nov":"交互中心谱域引导；跨具身低频对齐；不依赖大规模机器人演示即可迁移人类交互知识。",
 "limit":"依赖第一视角数据质量；真实任务 57.7% 仍有落差；与最新 VLA 大模型的正面对比需核实。",
 "lib":"库内有人形导航 TANGO、具身相关方向；WING 属“egocentric→robot policy”迁移，补感知-动作迁移缺口。",
 "repro":"项目页 + 多基准 + 真实实验；倾向代码（以正文为准）。",
 "action":"数据高效机器人学习方向重点追踪；关注与 VLA 结合的下一步。",
},
{
 "id":"arXiv:2610.03441","bid":"2610.03441","title":"ChromaGS: Text-Driven Semantic Editing of 4D Gaussian Avatars",
 "title_zh":"ChromaGS：面向 4D 高斯化身的文本驱动语义编辑",
 "track":"化身与人体","authors":"Antonio Canela, Jordi Sànchez-Riera",
 "scores":{"IMP":4,"NOV":4,"TEC":4,"EXP":4,"PER":4,"TRL":3,"REP":4},
 "one":"ChromaGS 对可动 3D 高斯头部化身做实时语言引导的颜色编辑，给每个高斯学语义区域软分配并把颜色分解为区域基色 + 高斯残差，首次实现确定性、局部精确、渲染时即时（约 50ms）改色且无需重训。",
 "problem":"现有文本驱动头像编辑要么纠缠特征/缺乏几何一致性，要么需慢速逐提示优化或牺牲身份/绑定；生成式编辑会引入非预期改动。",
 "method":"语义掩码（SAM3 + 文本）→ K=6 语义类（发/眉/眼/唇/肤/背景）；颜色分解为区域基色 + 高斯残差；两阶段语言管线（Flan-T5-Small 解析为结构化指令 + 确定性颜色解析器处理绝对/相对指令）；编辑在渲染时应用。",
 "exp":"基于 animatable GS 框架，RTX 5090 训练约 15min；FaceScape/INSTA，每场景 14 种编辑 × 多主体约 10k 编辑帧 @512²；指标 Identity Preservation(ArcFace)、CLIP Score、Context Preservation(1-LPIPS)；对比 GaussianAvatar-Editor（每编辑约 800s）与 InstructPix2Pix（约 400ms/帧，有颜色溢出/过饱和）。",
 "nov":"确定性局部颜色控制（vs 生成式）；残差保留细节；渲染时即时编辑。",
 "limit":"仅颜色（非几何）；依赖 SAM3 掩码质量；K=6 语义类有限。",
 "lib":"库内化身方向有 PHOSA（手语化身）、ARS-Avatar（可重光照）、化身畸变意图识别等；ChromaGS 补“高斯化身实时颜色编辑”，且与同作者 ManifoldSplat（形状编辑）互补。",
 "repro":"项目页 + 代码 + 明确指标。",
 "action":"虚拟人/VR 化身实时换装换色方向重点；关注与 ManifoldSplat 合并为统一编辑框架。",
},
{
 "id":"arXiv:2610.03599","bid":"2610.03599","title":"ManifoldSplat: Language-Guided Semantic Shape Editing of 3D Gaussian Head Avatars",
 "title_zh":"ManifoldSplat：面向 3D 高斯头部化身的语义形状编辑",
 "track":"化身与人体","authors":"Antonio Canela, Jordi Sànchez-Riera",
 "scores":{"IMP":4,"NOV":4,"TEC":4,"EXP":4,"PER":4,"TRL":3,"REP":4},
 "one":"ManifoldSplat 是首个端到端、语言引导的 3D 高斯头部化身“形状”语义编辑框架，在 FLAME 流形内编辑（而非直接优化非结构高斯云），严格保持身份与动画，约 90s 重建+编辑、约 800fps 渲染，在局部提示对齐/几何一致性/身份保持上达 SOTA。",
 "problem":"文本驱动头像编辑难提供细粒度局部控制（特征纠缠/缺几何一致性）；自然语言改几何需慢速逐提示优化或牺牲身份/绑定。",
 "method":"在结构化 FLAME 流形内编辑而非非结构高斯云；DeltaRegion——按区域解耦的 CVAE 前馈输出形状增量；加 refining 阶段恢复视角一致细节；单目视频重建。",
 "exp":"合成数据集可扩展生成；FaceScape 等基准；SOTA 于局部提示对齐/几何一致性/身份保持；约 90s + 约 800fps。",
 "nov":"流形约束保身份/绑定；前馈形状增量（vs 逐提示优化）；与 ChromaGS 形成“形状 + 颜色”双编辑。",
 "limit":"仍限头部化身；依赖 FLAME 参数化；单目重建假设。",
 "lib":"与 ChromaGS 同作者互补；库内化身编辑方向补强（PHOSA/ARS-Avatar 等）。",
 "repro":"项目页 + 代码。",
 "action":"高斯化身编辑方向核心参考；关注形状 + 颜色统一。",
},
{
 "id":"arXiv:2610.02322","bid":"2610.02322","title":"SCION: Scene Composition with Instanced Neural Primitives",
 "title_zh":"SCION：基于实例化神经基元的场景组合表示",
 "track":"神经渲染","authors":"Princeton (light.princeton.edu/SCION)",
 "scores":{"IMP":4,"NOV":4,"TEC":4,"EXP":4,"PER":4,"TRL":3,"REP":3},
 "one":"SCION 用“可复用基元词汇 + 轻量世界空间实例”的层次化组合场景表示替代独立高斯，联合离散/连续优化，1.2MB 维持高质并支持实例级编辑/动画，率失真优于现有高斯压缩。",
 "problem":"现有神经场景表示把每个元素当作独立高斯，存冗余参数、缺乏操作句柄；Splat&Replace 类需人工选重复元素。",
 "method":"层次化组合表示——紧凑可复用基元词汇 + 变换副本的世界空间实例；多视角联合优化离散（基元分配）+ 连续（变换）参数；两级 densification（高斯 + 实例）+ 对抗损失保共享基元细节。",
 "exp":"率失真优于现有高斯压缩；1.2MB；实例级编辑/动画无需重训；含消融。",
 "nov":"组合基元发现（vs 压缩）；实例级编辑/动画；对抗损失保共享细节。",
 "limit":"基元词汇容量需预设；复杂非重复结构收益下降；仅场景表示（未涉渲染管线优化）。",
 "lib":"库内高斯压缩/抽象密集（COSA-GS/MoQSplat/TopoGS/SplatLabel/PePESeg3D/Observation-Gram/GS-PQM）。SCION 是“组合基元”新范式，区别于逐高斯压缩——路线级观察：库正从纯压缩走向结构化组合表示。",
 "repro":"项目页（Princeton）；倾向代码（以正文为准）。",
 "action":"大规模场景资产生产关注；注意与 Budgeted-GS/PocketSplat 的互补（组合表示 + 预算部署）。",
},
{
 "id":"arXiv:2610.02697","bid":"2610.02697","title":"GeoScaffold: Learning Compact Geometric Latents via Reconstruction for Efficient Vision-Language Navigation",
 "title_zh":"GeoScaffold：通过重建学习紧凑几何潜变量以实现高效视觉-语言导航",
 "track":"空间计算与UI","authors":"Yixuan Jiang 等",
 "scores":{"IMP":4,"NOV":4,"TEC":4,"EXP":4,"PER":4,"TRL":3,"REP":3},
 "one":"GeoScaffold 在训练时一次性把几何监督“内化”进 VLA 策略（深度 tokenizer + 几何 query tokens 重建深度/连通性/可达性），推理时丢弃脚手架，在连续 VLN 基准上一致优于纯视觉导航器，适合轻量边缘部署。",
 "problem":"流式 Video-LLM 导航策略继承 2D 预训练的弱 3D 几何先验；现有几何增强在推理时持续付费（深度传感器/3D 编码器/每步感知调用）。",
 "method":"训练时学紧凑深度 tokenizer（冻结）；用少量可学习几何 query tokens 微调策略，让其隐状态重建导航关键几何；脚手架（tokenizer/生成器/重建头）训练后丢弃，主干与动作接口不变。",
 "exp":"VLN-CE 基准一致优于领先纯视觉导航器；推理效率对比几何增强方法；主干通用性；实现细节完整。",
 "nov":"训练时付费、推理时免费的几何内化；脚手架隐喻；边缘部署友好。",
 "limit":"仍属 VLN（具身导航）而非 XR 直接应用；几何仅重建深度/连通性/可达性；未在真实机器人长时验证。",
 "lib":"库内有 TANGO（人形导航）；GeoScaffold 补“几何先验内化”思路，属空间计算/具身交叉。",
 "repro":"基准实验 + 方法清晰；倾向代码（以正文为准）。",
 "action":"具身/空间智能方向关注；思考向 AR 导航迁移。",
},
{
 "id":"arXiv:2610.02715","bid":"2610.02715","title":"Ego2World: Compiling Egocentric Cooking Videos into Executable Worlds for Belief-State Planning",
 "title_zh":"Ego2World：将第一视角烹饪视频编译为可执行世界以支持信念态规划",
 "track":"感知与认知","authors":"Qinchuan Cheng 等",
 "scores":{"IMP":3,"NOV":3,"TEC":4,"EXP":4,"PER":4,"TRL":3,"REP":3},
 "one":"Ego2World 把标注过的烹饪第一视角视频编译为部分可观测下的可执行规划环境，分离世界状态与智能体信念，支持对规划/记忆选择的受控研究；6 规划器 105 任务显示接受操作常未达成目标，Qwen-Plus 配对研究信念持久化提升动作有效性 4.15pp、降视觉查询 90.27%。",
 "problem":"评测智能体需评估其自选动作后果；第一视角视频丰富但缺可执行环境。",
 "method":"编译器把源步骤/物体链接到符号动作规则、持久世界状态、显式任务条件；世界状态与信念分离；执行轨迹 + 条件检查区分中断/部分/完成。",
 "exp":"105 任务评 6 规划器；Qwen-Plus 配对研究（信念持久化 +4.15pp 动作有效性、-90.27% 视觉查询，令牌更多但无完成增益）。",
 "nov":"把人类活动编译为可执行世界；信念-世界分离的可控研究；可复用测试床。",
 "limit":"仅烹饪域；编译依赖标注质量；结论偏诊断性（无完成增益）。",
 "lib":"库内第一视角可执行世界基准少；补“可执行世界模型评测”缺口。",
 "repro":"基准/数据集/编译器；倾向公开（以正文为准）。",
 "action":"具身智能评测方向关注；跨域（非烹饪）扩展价值高。",
},
{
 "id":"arXiv:2610.03232","bid":"2610.03232","title":"Seeing through the Eyes of AI: Situated Explainability in Augmented Reality",
 "title_zh":"透过 AI 之眼：增强现实中的情境化可解释性",
 "track":"空间计算与UI","authors":"Ana Stanescu 等",
 "scores":{"IMP":4,"NOV":3,"TEC":3,"EXP":4,"PER":3,"TRL":3,"REP":3},
 "one":"提出用 AR 把可解释 AI（XAI）信息以“情境化/空间化”方式实时呈现在用户工作空间中，解决 2D 屏上解释需用户自行映射到物理对象的问题，并通过两项用户研究给出体验洞察。",
 "problem":"现有 XAI 多在 2D 屏用预录数据呈现，用户需把显示信息映射回物理对象与真实位置，解释难在情境中理解。",
 "method":"在 AR 中实时呈现空间可解释性信息；展示已知 XAI 方法如何应用于 AR；两项用户研究（探索性 + 对比性）收集体验。",
 "exp":"用户研究 1（探索性评估）+ 用户研究 2（对比）；主题涵盖情境化解释、信任/可靠、ML/AI 经验、LLM 集成等。",
 "nov":"把 XAI 从 2D 屏搬到物理情境（情境化解释）；方法论应用而非新算法。",
 "limit":"方法新颖性偏低（应用已知 XAI 于 AR）；偏定性用户研究、缺量化 SOTA；样本/规模未明。",
 "lib":"库内 AR/空间计算有情境化解释缺口；补“AR + XAI”交叉。",
 "repro":"用户研究设计清晰；无代码（HCI 论文）。",
 "action":"AR 智能助手/工业巡检解释界面参考；关注量化对比后续。",
},
]

for p in PAPERS:
    p["value"] = value(p["scores"])
    p["grade"] = grade(p["value"])

# sort by value desc
PAPERS.sort(key=lambda x: -x["value"])

# ---------- 1) 7dim table (reference) ----------
os.makedirs(os.path.join(ROOT,f"papers/daily/{DATE}"),exist_ok=True)
def dim_cell(s): return str(s)
lines = []
lines.append("# 当日新论文 7 维度对比表（参考）")
lines.append("")
lines.append(f"> 拉取日 {DATE} · 数据源 arXiv RSS（公告日 2026-10-05，补齐 10-03~10-05 周末/周一积压提交）· 新提交 XR 相关 {len(PAPERS)} 篇")
lines.append("")
header = "| 排名 | arXiv | 标题 | 赛道 | IMP | NOV | TEC | EXP | PER | TRL | REP | 总分 | 等级 | 落后 |"
sep = "|---|---|---|---|---|---|---|---|---|---|---|---|---|---|"
lines.append(header); lines.append(sep)
for i,p in enumerate(PAPERS,1):
    s=p["scores"]
    lines.append(f"| {i} | {p['bid']} | {p['title_zh']} | {p['track']} | {s['IMP']} | {s['NOV']} | {s['TEC']} | {s['EXP']} | {s['PER']} | {s['TRL']} | {s['REP']} | {p['value']} | {p['grade']} | — |")
lines.append("")
lines.append("维度定义：IMP 问题重要性 · NOV 方法创新性 · TEC 技术完整度 · EXP 实验强度 · PER 性能增益 · TRL 落地成熟度 · REP 可复现与影响力（均 1–5）。权重 0.20·IMP+0.20·NOV+0.15·TEC+0.15·EXP+0.15·PER+0.08·TRL+0.07·REP。分档 S≥4.2 / A 3.6–4.2 / B 3.0–3.6 / C<3.0。")
open(os.path.join(ROOT,f"papers/daily/{DATE}/7dim-table.md"),"w",encoding="utf-8").write("\n".join(lines))

# ---------- 2) scored.md ----------
sl=[]
sl.append("# 评分明细与覆盖率校验")
sl.append("")
sl.append("## 评分明细")
sl.append("")
sl.append("| arXiv | 标题 | 赛道 | IMP | NOV | TEC | EXP | PER | TRL | REP | 总分 | 等级 |")
sl.append("|---|---|---|---|---|---|---|---|---|---|---|---|")
for p in PAPERS:
    s=p["scores"]
    sl.append(f"| {p['bid']} | {p['title_zh']} | {p['track']} | {s['IMP']} | {s['NOV']} | {s['TEC']} | {s['EXP']} | {s['PER']} | {s['TRL']} | {s['REP']} | {p['value']} | {p['grade']} |")
sl.append("")
sl.append("## 覆盖率校验（三关）")
sl.append("")
sl.append("- ① 同质去重（Jaccard > 0.62 判定同质）：本批 10 篇与库内 304 篇逐一比对，max Jaccard = 0.066（2610.03283 vs arXiv:2609.21015），远低于 0.62 阈值 → **通过，无同质重复**。")
sl.append("- ② 赛道覆盖：本批覆盖 渲染与显示 / 重建与SLAM / 神经渲染 / 感知与认知 / 化身与人体 / 空间计算与UI 共 **6 个赛道**（≥5） → **通过**。")
sl.append("- ③ 价值天花板：当日最高分 4.65（Budgeted-GS） ≥ 库内近 30 天 Top10 均分 4.298 → **重磅日，含 3 篇 S 级**（4.65 / 4.58 / 4.28），未拔高。")
sl.append("")
sl.append("## 结论")
sl.append("三关全部通过，**未触发重筛**。入选 10 篇均基于全文（L0/FULL）证据打分；低量日约束不适用（本日有 10 篇 ≥ B 级新稿）。")
open(os.path.join(ROOT,f"papers/daily/{DATE}/scored.md"),"w",encoding="utf-8").write("\n".join(sl))

# ---------- 3) run_log.md ----------
rl=[]
rl.append("# 执行日志 run_log")
rl.append("")
rl.append(f"- 拉取日：{DATE}（周二）")
rl.append("- 数据源探针：arxiv.org/api/query 200；export.arxiv.org 200；rss.arxiv.org 200（cs.CV 191 条）。API 恢复正常，但 submittedDate 索引前沿仍停滞于 10-02，故转 RSS 兜底（与历史 10-03~10-05 同因）。")
rl.append("- 拉取：`fetch_arxiv.py --since 2026-10-02` 仅回 10 条（全为 10-02 已滞后索引，非新）；`fetch_rss.py` 7 分类 652 条去重 → 关键词命中 26 条。")
rl.append("- 过滤：按 2610.* 前缀 + 排除库内已有（2609.* v2 再公告）+ 排除旧稿 replace/cross（2605/2606/2607/2608/2510/2512）+ 排除非 XR 误命中（2610.02382 医学体渲染、2610.02772 LLM 知识编辑）→ **真正新提交 XR 相关 10 篇**。（2610.01943 已在库）")
rl.append("- 全文抓取：`fetch_fulltext.py` 10 篇 → **全部 L0 / FULL**（arxiv.org/html 源），串行 3s/篇，无限流/降级/伪造；manifest 全 L0/FULL。")
rl.append("- 评分：10 篇均基于正文证据打分（先抓全文再定稿，符合 skill §8.6.2）。")
rl.append("- 覆盖率三关：① max Jaccard 0.066 < 0.62 通过；② 6 赛道 ≥5 通过；③ 当日最高 4.65 ≥ 库近30天Top10均分 4.298 → 重磅日含 S 级，通过。")
rl.append("- 落后标注：OUTDATED/SUPERSEDED 0 篇（方法均为当期新贡献，无同质）；路线级观察 1 条（SCION 组合基元范式 vs 库内纯压缩范式，非取代）。")
rl.append("- 环境：C: 盘余 16.3 GB（健康）；无盘满风险。")
rl.append("- 交付：报告 1 + 原子笔记 10 + 当日 MOC + 总索引更新 + 7维表/scored/run_log 各 1 + 文献库 304→314（+10）。")
open(os.path.join(ROOT,f"papers/daily/{DATE}/run_log.md"),"w",encoding="utf-8").write("\n".join(rl))

# ---------- 4) atomic notes ----------
notes_dir = os.path.join(ROOT,"papers/notes")
os.makedirs(notes_dir,exist_ok=True)
def slug(t):
    import re
    return re.sub(r'[^0-9a-zA-Z]+','-',t)[:40].strip('-')
for p in PAPERS:
    fm = [
        "---",
        f"id: {p['id']}",
        f"title: \"{p['title']}\"",
        f"title_zh: \"{p['title_zh']}\"",
        f"track: {p['track']}",
        "venue: arXiv preprint",
        f"date: {DATE}",
        f"value: {p['value']}",
        f"grade: {p['grade']}",
        "evidence: FULL",
        "status: CURRENT",
        f"fetch_level: L0",
        f"fulltext_chars: {fchars(p['bid'])}",
        f"scores: {json.dumps(p['scores'],ensure_ascii=False)}",
        f"tags: [{p['track']}]",
        "---",
        "",
        f"# {p['title_zh']}",
        "",
        "## 一句话结论",
        p["one"],
        "",
        "## 要解决的问题",
        p["problem"],
        "",
        "## 方法详解",
        p["method"],
        "",
        "## 实验与结果",
        p["exp"],
        "",
        "## 创新点与贡献",
        p["nov"],
        "",
        "## 局限与风险",
        p["limit"],
        "",
        "## 与文献库的关系",
        p["lib"],
        "",
        "## 可复现性",
        p["repro"],
        "",
        "## 行动建议",
        p["action"],
        "",
    ]
    fn = f"{p['bid']}__{slug(p['title_zh'])}.md"
    open(os.path.join(notes_dir,fn),"w",encoding="utf-8").write("\n".join(fm))

# ---------- 5) daily MOC ----------
moc=[]
moc.append(f"# MOC · {DATE}（XR 每日论文雷达）")
moc.append("")
moc.append(f"> 拉取日 {DATE} · 公告日 2026-10-05（补齐 10-03~10-05 周末/周一积压）· 新提交 XR 相关 10 篇 · S 级 3 / A 级 5 / B 级 2")
moc.append("")
moc.append("## 排行榜（按重要性降序）")
moc.append("")
moc.append("| 排名 | arXiv | 标题 | 赛道 | 总分 | 等级 | 笔记 |")
moc.append("|---|---|---|---|---|---|---|")
for i,p in enumerate(PAPERS,1):
    fn = f"{p['bid']}__{slug(p['title_zh'])}.md"
    moc.append(f"| {i} | {p['bid']} | {p['title_zh']} | {p['track']} | {p['value']} | {p['grade']} | [笔记](../notes/{fn}) |")
moc.append("")
moc.append("## 赛道分布")
moc.append("")
tracks={}
for p in PAPERS: tracks.setdefault(p["track"],[]).append(p["bid"])
for t,ids in tracks.items():
    moc.append(f"- **{t}**：" + "、".join(ids))
moc.append("")
moc.append("## 落后/路线观察")
moc.append("- 全部 CURRENT，无 OUTDATED。")
moc.append("- 路线观察：SCION（组合基元范式）相对库内密集的“逐高斯压缩”范式（COSA-GS/MoQSplat/TopoGS 等）代表从压缩走向结构化组合表示的新方向，非取代。")
moc.append("")
moc.append("## 参考")
moc.append(f"- [7 维度对比表](../daily/{DATE}/7dim-table.md) · [评分与覆盖](../daily/{DATE}/scored.md) · [执行日志](../daily/{DATE}/run_log.md)")
open(os.path.join(ROOT,f"papers/MOC/MOC-{DATE}.md"),"w",encoding="utf-8").write("\n".join(moc))

# ---------- 6) full report ----------
rep=[]
rep.append(f"# XR 每日论文雷达 · 解读报告（{DATE}）")
rep.append("")
rep.append("## 一、执行摘要")
rep.append("")
rep.append(f"本日为周二（2026-10-06）。arXiv API 已恢复 200，但 `submittedDate` 索引前沿仍停滞于 2026-10-02，真实新增须由 RSS 兜底获取。RSS 公告日 2026-10-05，补齐了 10-03~10-05 周末/周一积压提交。经按 `2610.*` 前缀过滤、剔除库内已有 v2 再公告、剔除旧稿 replace/cross 与非 XR 误命中后，**入选 XR 相关新提交 10 篇**。")
rep.append("")
rep.append("全文抓取 10 篇**全部 L0/FULL**（arxiv.org/html 源，串行 3s/篇，无限流/降级/伪造）。评分基于正文证据。覆盖率三关全部通过：① 与库内 304 篇 max Jaccard=0.066（远低于 0.62）；② 覆盖 6 赛道（≥5）；③ 当日最高 4.65 ≥ 库近 30 天 Top10 均分 4.298 → **本日为重磅日，含 3 篇 S 级**。**未触发重筛，未拔高评分**。**无 OUTDATED 论文**；路线级观察 1 条（SCION 组合基元范式）。")
rep.append("")
rep.append(f"**S 级（3 篇）**：Budgeted-GS（4.65，城市级 3DGS 实时/容量下限理论）、HexVIO（4.58，VIO 卸载 DSP 全天候追踪）、PocketSplat（4.28，移动端预算可控高斯重建）。")
rep.append("")
rep.append("## 二、Top10 排行榜")
rep.append("")
rep.append("| 排名 | arXiv | 标题 | 赛道 | 总分 | 等级 | 落后 |")
rep.append("|---|---|---|---|---|---|---|")
for i,p in enumerate(PAPERS,1):
    rep.append(f"| {i} | {p['bid']} | {p['title_zh']} | {p['track']} | {p['value']} | {p['grade']} | — |")
rep.append("")
rep.append("## 三、逐篇深度解读（按重要性降序）")
rep.append("")
for i,p in enumerate(PAPERS,1):
    fn = f"{p['bid']}__{slug(p['title_zh'])}.md"
    rep.append(f"### 第 {i} 章 · {p['title_zh']}（{p['bid']} · {p['grade']} · {p['value']}）")
    rep.append("")
    rep.append(f"> 赛道：{p['track']} · 证据等级：FULL（L0 全文）· [原子笔记](../papers/notes/{fn})")
    rep.append("")
    rep.append("**一句话结论**："+p["one"])
    rep.append("")
    rep.append("**要解决的问题**："+p["problem"])
    rep.append("")
    rep.append("**方法详解**："+p["method"])
    rep.append("")
    rep.append("**实验与结果**："+p["exp"])
    rep.append("")
    rep.append("**创新点与贡献**："+p["nov"])
    rep.append("")
    rep.append("**局限与风险**："+p["limit"])
    rep.append("")
    rep.append("**与文献库的关系**："+p["lib"])
    rep.append("")
    rep.append("**可复现性**："+p["repro"])
    rep.append("")
    rep.append("**行动建议**："+p["action"])
    rep.append("")
rep.append("## 四、当日全量 7 维度对比表（参考）")
rep.append("")
rep.append(f"见 [papers/daily/{DATE}/7dim-table.md](../papers/daily/{DATE}/7dim-table.md)。（亦在本文末附简表）")
rep.append("")
rep.append("| 排名 | arXiv | 赛道 | 总分 | 等级 |")
rep.append("|---|---|---|---|---|")
for i,p in enumerate(PAPERS,1):
    rep.append(f"| {i} | {p['bid']} | {p['track']} | {p['value']} | {p['grade']} |")
rep.append("")
rep.append("## 五、覆盖率校验与筛选过程说明")
rep.append("")
rep.append("1. **同质去重（关①）**：10 篇新稿与库内 304 篇逐篇计算标题+摘要 token Jaccard，最大值 0.066（2610.03283 HexVIO vs arXiv:2609.21015），远低于 0.62 同质阈值 → 通过，无同质重复，无需剔除或降权。")
rep.append("2. **赛道覆盖（关②）**：覆盖 渲染与显示、重建与SLAM、神经渲染、感知与认知、化身与人体、空间计算与UI 共 6 赛道 ≥5 → 通过，无筛选偏食。")
rep.append("3. **价值天花板（关③）**：当日最高 4.65 ≥ 库内近 30 天 Top10 均分 4.298 → 确为重磅日，3 篇 S 级为真高价值，未为凑数拔高。")
rep.append("4. **重筛闭环**：三关均通过，**未触发重筛**。入选 10 篇全为基于全文证据打分、且均 ≥B 级，低量日约束不适用。")
rep.append("")
rep.append("## 六、附录")
rep.append("")
rep.append("- **抓取失败/降级清单**：无。10 篇全文全部 L0/FULL，manifest 校验通过。")
rep.append("- **证据等级分布**：L0/FULL ×10。")
rep.append("- **落后标注**：OUTDATED/SUPERSEDED 0 篇；路线级观察 1 条（SCION 组合基元范式 vs 库内纯压缩范式，非取代）。")
rep.append(f"- **文献库前沿**：本次 +10（304→314）；公告日 2026-10-05，拉取日 {DATE}。")
open(os.path.join(ROOT,f"reports/XR-Daily-Report-{DATE}.md"),"w",encoding="utf-8").write("\n".join(rep))

# ---------- 7) registry update (idempotent append) ----------
reg_path = os.path.join(ROOT,"papers/library/registry.jsonl")
existing=set()
if os.path.exists(reg_path):
    with open(reg_path,encoding="utf-8") as f:
        for line in f:
            line=line.strip()
            if line: existing.add(json.loads(line)["id"])
added=0
with open(reg_path,"a",encoding="utf-8") as f:
    for p in PAPERS:
        if p["id"] in existing: continue
        rec={
          "id":p["id"],"title":p["title"],"title_zh":p["title_zh"],"track":p["track"],
          "date":DATE,"value":p["value"],"grade":p["grade"],"scores":p["scores"],
          "status":"CURRENT","evidence":"FULL","fetch_level":"L0",
          "fulltext_chars":fchars(p["bid"]),"in_top10":True,"batch":BATCH,"flags":[]
        }
        f.write(json.dumps(rec,ensure_ascii=False)+"\n")
        added+=1
print("NOTES:",len(PAPERS),"REPORT+TABLES written. REGISTRY +",added)
print("TOP3:",[(p['bid'],p['value'],p['grade']) for p in PAPERS[:3]])
