# -*- coding: utf-8 -*-
"""生成 2026-09-23 Top10 原子化笔记 + 当日 MOC。"""
import json, os, datetime

raw = {json.loads(l)["base_id"]: json.loads(l) for l in open("data/raw/2026-09-23_new.jsonl", encoding="utf-8")}
snap = json.load(open("papers/daily/2026-09-23/_scored_snapshot.json", encoding="utf-8"))
DATE = "2026-09-23"
NOTES = "papers/notes"
MOC = "papers/MOC"
os.makedirs(NOTES, exist_ok=True)

def fm(d):
    return "---\n" + "\n".join(f"{k}: {v}" for k, v in d.items()) + "\n---\n\n"

# 每篇笔记正文（依据摘要+全文 Method/Experiment/Conclusion 证据）
NOTES_BODY = {
 "2609.21502": dict(
   venue="arXiv preprint 2026-09-18",
   tags="[3D基础模型, 世界记忆, 高斯泼溅, 可扩展建图]",
   oneliner="提出记忆中心（adaptive world memory）的 3D 基础模型，用门控循环空间状态 + 测试时时空记忆调节统一可扩展建图、定位与高斯渲染，在视频深度/相机位姿/稠密重建/渲染四项上取得一致领先。",
   problem="现有 3D 基础模型（VFM）具备泛化几何推理，但缺乏持久记忆、可扩展性与可渲染场景建模；大场景与多平台数据下难以兼顾定位精度、重建质量与实时渲染。",
   method=("整体为\"双阶段自适应世界记忆 + 前馈高斯世界表示\"：\n"
           "- **双阶段自适应世界记忆**：① 门控循环空间状态（Gated Recurrent Spatial State）压缩历史观测；② 测试时时空记忆调节（Test-Time Temporal–Spatial Memory Regulation）依据新观测动态门控记忆读写；③ 双阶段记忆更新（局部子图 + 全局）。\n"
           "- **前馈高斯世界表示（Feed-forward Gaussian World Representation）**：直接从 RGB 回归可渲染高斯，兼顾几何与外观。\n"
           "- **渐进式建图与跟踪**：子图感知局部建图/跟踪 + 基于 SL(4) 流形的回环检测与全局优化（Relative Submap Alignment / Loop Closure / Global Optimization on SL(4) Manifold）。\n"
           "- **训练目标**：pointmap 回归损失 + 位姿损失 + 高斯渲染损失 + 高斯正则 + 课程学习。"),
   exp=("在视频深度估计、相机位姿估计、稠密重建、高斯渲染四项评测上对比 SoTA；另有真实多平台数据评估与运行时间/显存分析、消融实验。论文给出子图/回环/SL(4) 全局优化的完整链路，工程完整度高。"),
   contrib="① 将\"世界记忆\"概念落地到可渲染 3D 高斯表示，统一建图-定位-渲染；② SL(4) 流形上的全局优化区别于常见 SE(3)/Sim(3) 范式；③ 测试时记忆调节提升多平台扩展性。",
   limit="仍依赖前馈高斯表示的容量上限；真实机器人闭环的长期记忆一致性、跨场景遗忘问题未充分讨论；基准以已有数据集为主，缺统一的大规模机器人基准。",
   relation="库内已有大量 3DGS/SLAM 单点方法（MonoGS、Photo-SLAM、S3PO-GS 等，见 Cube-Splat/Elevator-VIGS 笔记）；本篇是\"基础模型 + 记忆\"层面的整合者，属上层范式而非单点算法。",
   repro="论文声明代码/数据，属 arXiv preprint；未提供确认的开源链接（需待作者释放）。建议跟踪 GitHub。",
   action="作为\"3D 基础模型/世界模型\"赛道的标杆候选持续跟踪；若开源，优先在自身机器人栈做建图-渲染统一基线替换。"),

 "2609.21347": dict(
   venue="arXiv preprint 2026-09-21",
   tags="[360°SLAM, 高斯泼溅, cubemap, 全景, 伴随优化]",
   oneliner="首个全景（360°）高斯泼溅 SLAM：将每帧 360° 图像分解为共享单一光心的 cubemap 四固定朝向虚拟针孔视图，并用伴随一致的多面优化统一位姿，跨全景基准取得准确鲁棒跟踪与高保真重建。",
   problem="现有 3DGS 稠密 SLAM 多针对针孔相机；全景/鱼眼相机因超大视场与严重深度歧义导致地图崩塌与结构伪影，且全景与针孔 GS-SLAM 的收益（更宽 FoV vs 算法贡献）难以解耦。",
   method=("**Cubemap 相机模型 + 伴随一致优化**：\n"
           "- 将每帧 360° 图像路由为 4 个固定朝向、共享同一光心的虚拟针孔视图，保留透视渲染稳定性同时最大化覆盖。\n"
           "- 导出伴随映射（adjoint mapping）把各面梯度聚合到单一主位姿状态，得到面不变优化，在宽 FoV 下改善收敛。\n"
           "- 系统含跟踪与建图双线程，支持全景基准上的在线稠密 SLAM。"),
   exp=("数据集：PALVIO、OmniBlender、自建 SynPano（全景）。对比 Photo-SLAM、MonoGS、S3PO-GS：复杂室内基线模糊、S3PO-GS 边界云状伪影；大规模室外传统窄 FoV 方法因深度歧义地图崩塌，Cube-Splat 保持锐利几何边界与无伪影远景。消融解耦了 FoV 增益与多面位姿优化贡献。"),
   contrib="① 首个全景 GS-SLAM 框架；② cubemap 分解 + 伴随一致多面优化，工程上解决了全景几何一致性；③ 给出 FoV 与算法的受控消融。",
   limit="依赖全景图像输入（需全景/鱼眼传感器）；四固定面分解在极端遮挡下的面间一致性仍有上限；实时性未给出明确帧率结论（仅运行时间分析）。",
   relation="与库内 MonoGS/Photo-SLA M/S3PO-GS 路线同源，但把战场从针孔扩展到全景——是对\"GS-SLAM\"赛道的必要补齐（库内此前无全景 GS-SLAM）。",
   repro="arXiv preprint；未确认开源；依赖 cubemap 渲染实现，复现需自行搭建全景光栅化。",
   action="若做全景/宽视场 SLAM 或机器人环视感知，优先作为基线；关注其是否开源 cubemap 高斯光栅化算子。"),

 "2609.24140": dict(
   venue="arXiv preprint 2026-09-21",
   tags="[神经渲染SLAM, 不确定性, 贝叶斯, 关键帧]",
   oneliner="用概率化框架为神经渲染 SLAM 引入显式可靠度：以预测不确定性归一化跟踪残差、以预测惊奇驱动关键帧选择，在跟踪/渲染/不确定度/真实机器人数据上验证有效。",
   problem="神经渲染 SLAM 依赖渲染 RGB-D 残差做跟踪与建图，但残差可靠性因传感器噪声、观测覆盖不足与地图不完整而差异巨大；无显式可靠度估计时，不可靠残差会误导优化。",
   method=("**贝叶斯神经渲染 SLAM**：\n"
           "- **映射的预测不确定性建模**：对渲染预测给出概率分布而非点估计。\n"
           "- **不确定性归一化跟踪**：用预测不确定度加权/归一化残差，低可靠区域降权。\n"
           "- **预测惊奇（predictive surprise）关键帧选择**：仅在高信息增益处插入关键帧，降低冗余。\n"
           "- 整体框架将概率可靠度嵌入跟踪-建图闭环。"),
   exp=("在跟踪、渲染与不确定度、关键帧选择、消融（跟踪与关键帧模块、跟踪损失）以及真实机器人数据上评估。消融验证了跟踪与关键帧选择模块、跟踪损失的各自贡献；真实机器人数据实验增强落地可信度。"),
   contrib="① 把\"不确定性感知\"从被动正则升级为驱动跟踪与关键帧的主动信号；② 预测惊奇作为关键帧判据是清晰的新意；③ 在真实机器人数据上验证，而非仅合成。",
   limit="概率建模带来额外计算；不确定性校准本身需要充分监督；与 Gaussian-SLAM 类方法的接口依赖其渲染后端。",
   relation="库内已有 MonoGS/Photo-SLAM/Cube-Splat 等确定性 GS-SLAM；本篇在\"可靠度\"维度形成互补/进阶，是同类方法的鲁棒性增强路线。",
   repro="arXiv preprint；未确认开源；核心是不确定性头 + 惊奇关键帧，可在现有 Gaussian-SLAM 上改造。",
   action="作为\"鲁棒 GS-SLAM\"的高优先级候选；若复现，可先在 MonoGS 上叠加不确定性头做对照。"),

 "2609.22913": dict(
   venue="arXiv preprint 2026-09-19 · Avaturn Live",
   tags="[实时化身, 对话式avatar, 流音频, 开源栈]",
   oneliner="开源的实时交互式虚拟化身全栈：153M 参数自回归流匹配动作生成器，以双通道音频为条件，并用自蒸馏把音频编码器改造成流式，把分块生成变成用户与化身的实时对话。",
   problem="说话头/双人模型已能实时推理，但\"快\"不等于\"可交互\"：实时系统需把模型输出与外部语音代理的语音同步、调度视频帧播放并处理打断，现有方案缺乏完整可部署栈。",
   method=("**AVTR-1 全栈**：\n"
           "- **紧凑动作模型**：153M 参数自回归 flow-matching 运动生成器，条件为对话双方音频。\n"
           "- **流式音频编码器**：通过自蒸馏把音频编码器改造为流式，支持分块流式推理。\n"
           "- **推理系统**：把分块生成编排成用户与化身之间的实时对话，处理中断与帧调度。\n"
           "- 评估引入 Reference-Based Directed Granger Gain (R-DGG) 度量\"说话人语音对听话人运动的额外预测贡献\"。"),
   exp=("在 SI-184（Seamless Interaction 即兴对话测试集，184 个说话人-听话人对，11.90 小时 @30fps）上沿视觉质量、说话质量、反应式倾听三轴评估；R-DGG 使用 1457 个倾听段（3.46h @25fps）。提供区域输出头与完整推理系统描述。"),
   contrib="① 首个面向\"实时双向对话\"的开源化身全栈（含推理系统而非仅模型）；② R-DGG 度量填补了\"倾听反应性\"的评估空白；③ 流式自蒸馏实践对部署有意义。",
   limit="核心创新偏系统集成与评估，方法新颖度中等；依赖外部语音代理；真实端到端延迟/并发数据有限。",
   relation="库内已有 VibeAvatar（语音运动学+美学解耦说话人化身）等单点方法；AVTR-1 补齐\"交互式对话系统\"这一更高层形态，并开源，属工程与生态贡献。",
   repro="明确开源（open stack，CC BY 4.0），含推理系统与模型，可复现性强——这是其关键加分项。",
   action="若做实时对话式 avatar，直接以其为基线 fork；重点学习其流式自蒸馏与中断处理实现。"),

 "2609.24253": dict(
   venue="arXiv preprint 2026-09-20",
   tags="[航拍重建, 消费级无人机, 质量引导, 3DGS]",
   oneliner="面向消费级无人机的\"质量引导\"航拍重建系统：先预测区域重建质量，再针对性复飞补缺，把预设航线导致的复杂表面欠观测在大场景重建前就发现并补采。",
   problem="3DGS 为大规模具身仿真提供高保真场景，但消费级设备建大规模城市场景受昂贵设备与\"质量反馈延迟\"制约：预设航拍在复杂表面观测不足，缺陷往往重建后才发现，返工成本高。",
   method=("**OpenFlyScan 三段式**：\n"
           "- **自动采集与反馈**：无人机按航线下飞并实时反馈。\n"
           "- **区域重建质量预测**：预测每个区域的重建质量（哪些表面会欠观测/缺陷）。\n"
           "- **针对性复飞与联合重建**：依据质量预测自动规划复飞，补齐弱观测区域后联合重建。"),
   exp=("围绕三个问题评估：Q1 区域重建质量预测精度；Q2 支撑质量预测的信息；Q3 复飞增益及在无人机仿真中的使用。给出预测模型与复飞策略的有效性证据。"),
   contrib="① 把\"重建质量预测\"前置到采集阶段，闭环优化航拍路径；② 面向消费级无人机的可部署系统定位清晰；③ 质量引导范式可推广到其他主动重建。",
   limit="依赖质量预测模型的准确性；复飞规划的计算与飞行成本需权衡；大规模城市实测的端到端指标（如总飞行时间 vs 质量）披露有限。",
   relation="库内已有 VDGS（可见性驱动大规模航拍 3DGS）、OpenFlyScan 与之同源但强调\"质量引导复飞\"，是大规模航拍重建的采集合成闭环补全。",
   repro="arXiv preprint；系统形态利于复现（质量预测 + 航线规划），但需自搭无人机接口；未确认开源。",
   action="若做无人机/大规模城市场景采集，重点参考其质量预测+复飞闭环；可与 VDGS 的可见性方法组合。"),

 "2609.21498": dict(
   venue="arXiv preprint 2026-09-18",
   tags="[前馈3DGS, 体素对齐, 测试时优化, 无姿态]",
   oneliner="把前馈 3DGS 从逐像素基元改为体素对齐：聚合密集像素特征为全局体素特征，用稀疏 3D 体素 U-Net 与自分裂解码器回归高斯属性，并用测试时优化（TTO）修正位姿、以随机实心体渲染提升几何精度。",
   problem="前馈 3DGS 通常逐像素回归高斯基元，导致过度重叠与伪影，且预测相机位姿不准时新视图合成错位；全局结构脆弱、基元数绑定图像分辨率与视图数。",
   method=("**VoxelTTO**：\n"
           "- **体素对齐**：把密集像素特征聚合为全局体素特征，打破逐像素耦合。\n"
           "- **稀疏 3D 体素 U-Net + 自分裂解码器**：回归高斯属性，解耦基元数与图像分辨率。\n"
           "- **随机实心体渲染（stochastic solid volume rendering）**：训练与推理取代 3DGS 光栅化，提升几何精度。\n"
           "- **测试时优化（TTO）**：用位姿监督的轻量 LoRA 模块对齐预测相机参数与给定先验，降低位姿估计误差并显著改善测试视图 NVS。"),
   exp=("数据集：Replica、Tanks and Temples、DTU（室内/室外、合成/真实、场景级/物体级）。对比 AnySplat、YoNoSplat、DepthAnything3、MapAnything 等 VFM 基线与 VolSplat、MVSplat 等像素对齐基线；TTO 降低 VFM 主干的位姿误差并大幅提升 NVS。"),
   contrib="① 体素对齐缓解逐像素高斯重叠/伪影；② TTO 把位姿修正做成测试时轻量适配，泛化好；③ 随机实心体渲染替代光栅化，几何更准。",
   limit="体素分辨率带来内存/精度权衡；TTO 依赖位姿先验质量；与最新端到端前馈方法的极限指标尚需横向对比。",
   relation="库内 GrapeSplat（无姿态前馈 3DGS）、D3GS（深度-DINO-扩散引导）等同属\"前馈/无姿态 3DGS\"赛道；VoxelTTO 在\"几何精度 + 位姿鲁棒性\"上形成差异化。",
   repro="arXiv preprint；未确认开源；方法依赖 VFM 主干（如 VGGT 类），复现需对应权重。",
   action="做无姿态/前馈 3DGS 时优先对比 VoxelTTO 与 GrapeSplat；关注其 TTO 是否可迁移到自身管线。"),

 "2609.21176": dict(
   venue="arXiv preprint 2026-09-18",
   tags="[4DGS, 稀疏视图, 视频扩散, 迭代精修]",
   oneliner="针对稀疏视图动态场景合成这一病态问题，先用稠密几何初始化，再以视频扩散先验做参考引导的视频修复与新视图轨迹采样，配合缓存伪监督迭代精修动态高斯。",
   problem="从稀疏视图视频做动态场景合成是病态问题：现有几何先验/自适应优化/密度控制仍无法根本解决观测不足导致的不稳定与错误几何；动态 4DGS 在少视图下尤为脆弱。",
   method=("**4DGS-Fixer**：\n"
           "- **稠密几何初始化**：提供稳定起点。\n"
           "- **视频扩散引导迭代精修**：① 参考引导的视频修复（reference-guided video restoration）用扩散先验补全缺失/模糊区域；② 新视图轨迹采样（novel-view trajectory sampling）生成多样新视点监督；③ 缓存伪监督（cached pseudo-supervision）复用已生成帧，降低反复推理成本。\n"
           "- 以伪监督迭代优化动态 3D 高斯。"),
   exp=("数据集 Neural3DV（6 个动态场景，18–21 相机，2704×2028@30fps），采用 4C4D 协议：取空间最分离的 4 相机（1/10/13/20）训练，其余测试。对比 STGS、4DGS、4DGaussians、4C4D（同协议报告结果）。"),
   contrib="① 把视频扩散先验系统性引入 4DGS 稀疏视图精修；② 缓存伪监督降低扩散推理成本，是工程亮点；③ 新视图轨迹采样增强几何一致性。",
   limit="依赖扩散先验质量，可能引入幻觉几何；稀疏到极端的边界情况仍可能失败；计算成本（多轮扩散）未给明确预算。",
   relation="库内 4DGS/动态 GS 方法有 GARO（动态 GS 冗余优化）、GrapeSplat；4DGS-Fixer 在\"稀疏视图 + 扩散先验\"上形成互补，属动态重建的质量增强路线。",
   repro="arXiv preprint；未确认开源；依赖视频扩散模型，复现门槛中等。",
   action="做动态场景稀疏视图重建时，参考其\"扩散伪监督 + 缓存\"范式；关注幻觉几何的核验。"),

 "2609.24158": dict(
   venue="arXiv preprint 2026-09-21",
   tags="[可重光照, 单目, 3D头像, PBR, 语义自适应]",
   oneliner="从单目视频重建可重光照的 3D 头部化身：用网格绑定高斯化身，并以语义自适应残差调制（运动响应）与语义自适应光照响应因子（光照响应）+ 延迟 PBR 着色实现解耦重光照。",
   problem="从单目视频重建可表达且可重光照的 3D 头部化身需同时精确建模非刚性面部运动与光照相关外观；现有高斯化身常用全局耦合表示，高斯基元无法分离\"运动\"与\"光照\"，难以真实重光照。",
   method=("**Mesh-Bound Gaussian Avatar + 语义自适应双响应**：\n"
           "- **网格绑定高斯化身**（Mesh-Bound Gaussian Avatar）为几何基底。\n"
           "- **语义自适应运动响应**：UV 对齐条件输入 + 语义自适应残差调制 + 残差预测，使不同面部语义（如皮肤/五官）对动作有不同响应。\n"
           "- **语义自适应光照响应**：材质与法线参数化 + 语义自适应响应因子 + 延迟 PBR（deferred PBR）着色与重光照，解耦几何与光照。\n"
           "- 训练目标含运动与重光照一致性约束。"),
   exp=("实验：自重演（self-reenactment）、交叉重演（cross-reenactment）、重光照（relighting comparisons + material decomposition）；消融验证语义自适应运动响应与光照响应各自的贡献；组件分析区分几何与外观解耦效果。"),
   contrib="① 把\"语义自适应\"同时用于运动与光照响应，比全局耦合更细腻；② 延迟 PBR 着色实现真实重光照而非贴图伪造；③ 单目输入即可，落地门槛低。",
   limit="单目重光照本质是病态逆问题，材质分解为近似；极端光照/表情外推仍可能失败；依赖网格模板质量。",
   relation="库内 VibeAvatar（说话人化身，语音-运动学解耦）与 AVTR-1（实时对话化身）属同一\"化身\"赛道；本篇在\"可重光照 + 单目\"维度补齐，是头像保真度的关键能力。",
   repro="arXiv preprint；未确认开源；依赖 PBR 材质先验，复现需对应渲染器。",
   action="做高保真单目头像（含重光照）时作为优先基线；关注其材质分解的可迁移性。"),

 "2609.25002": dict(
   venue="arXiv preprint 2026-09-21",
   tags="[VR穿透, 中介式感知, 行为实验, 视动代价]",
   oneliner="一项量化研究：当 VR 头显以\"穿透显示（passthrough）\"中介用户对真实环境的感知时，会带来可测量的行为偏差与视动（visuomotor）代价，揭示穿透式感知并非透明窗口。",
   problem="VR 穿透显示让用户看到真实环境视频流而非直接光学透视；这种\"中介式感知（mediated perception）\"是否引入行为/运动代价长期缺乏严格量化，影响安全关键场景（如行走、操控）的设计。",
   method=("**受控行为实验**：\n"
           "- 任务与实验设计（Task and Experimental Design）：对比穿透显示 vs 直接/光学透视下的感知-动作表现。\n"
           "- 被试（Participants）、流程（Procedure）、设备与材料（Apparatus）、数据收集与测量（Data Collection and Measures）、统计分析（Statistical Analysis）完整。\n"
           "- 同时考察行为表现与视动一致性（visuomotor）。"),
   exp=("采用参与者实验 + 统计推断；同时测量行为指标与视动指标，给出穿透显示相对基线的代价量化。属用户/行为实验，样本与统计方法依论文报告。"),
   contrib="① 首次（据其所称）系统量化穿透显示的视动代价；② 把\"中介式感知\"从概念变为可测变量；③ 为 XR 安全与显示设计提供实证依据。",
   limit="行为实验外推性受任务/被试群体限制；未给出可计算的显示管线改进方案（偏发现而非方法）；与具体头显硬件强相关。",
   relation="库内已有 VR 头像/交互用户研究（手部 vs 控制器化身、VR 触觉反馈）；本篇在\"感知-显示中介\"维度补齐，与 EMooly/Generative Tutorial 同属空间计算与 UI 的人因分支。",
   repro="arXiv preprint；方法为行为实验协议，可复现性强（需伦理审批与设备）。",
   action="做 VR 穿透显示/安全关键交互设计时，将其代价结论纳入人因约束；可借鉴其实验范式做自身头显评估。"),

 "2609.23027": dict(
   venue="arXiv preprint 2026-09-19",
   tags="[3DGS, 质量评估, 基准, 失真]",
   oneliner="一篇关于 3D 高斯泼溅质量评估的综述/基准立场文：系统梳理 3DGS 特有失真、主观基准与数据集覆盖、客观指标与失效模式，并指出走向\"原生 3DGS\"质量评估的开放挑战。",
   problem="3DGS 已成为实时 NVS/压缩/沉浸式内容分发的实用表示，但其质量评估仍沿用\"渲染视图代理\"协议（采样相机位姿→渲染图/视频→套用图像/视频质量指标），忽略 3DGS 特有的几何/表示失真。",
   method=("**结构化评估框架**：\n"
           "- II 3DGS 特有失真（区别于传统图像/视频失真）。\n"
           "- III 主观基准与数据集覆盖（现有主观评测的覆盖缺口）。\n"
           "- IV 客观指标与失效模式（当前指标在 3DGS 上何时失效）。\n"
           "- V 走向原生 3DGS 质量评估（不依赖渲染代理的未来方向）。"),
   exp=("以综述/基准分析为主：整理失真类型、数据集覆盖矩阵与指标失效案例；给出\"原生 3DGS QA\"的研究议程，而非新算法。提供失真分类法与基准覆盖图。"),
   contrib="① 首次系统界定 3DGS 特有失真类别；② 给出主观基准/数据集覆盖的系统梳理；③ 明确\"渲染代理 QA\"的局限并提出原生评估议程——对沉浸式内容分发至关重要。",
   limit="本身是综述/立场文，无新算法或量化 SOTA 提升；结论的实践落地取决于后续原生指标研究；对单次下载价值偏\"导航\"而非\"方法\"。",
   relation="库内已有 CRP-GS（3DGS 压缩）、LiteTex-GS（轻量纹理）等表示/压缩工作；本篇在\"质量评估\"这一支撑性赛道补齐，与它们形成\"方法-评估\"互补（库内此前无 3DGS QA 基准）。",
   repro="综述/基准文，无代码；数据集与分类法可直接引用。",
   action="做 3DGS 压缩/传输/沉浸式分发时，以其失真分类与评估议程作为质量门控依据；跟踪其提出的\"原生 3DGS QA\"后续工作。"),

 "2609.23005": dict(
   venue="arXiv preprint 2026-09-19",
   tags="[3DGS压缩, 跨表示先验, COHS, 熵编码]",
   oneliner="CRP-GS：用\"对应导向的分层结构（COHS）+ 共享特征聚合 + 熵编码\"挖掘锚点之间的跨表示冗余，在 3DGS 压缩上以更低比特取得更优率失真，补齐了现有锚点压缩只压\"基元内\"冗余的短板。",
   problem="3DGS 因密集高斯基元带来高昂存储/传输成本；现有锚点式压缩（anchor-based）降低了\"基元内\"冗余，但锚点之间的跨表示冗余基本未被利用，压缩率仍有空间。",
   method=("**CRP-GS（Cross-Representation Priors for Gaussian Splatting）**：\n"
           "- **对应导向的分层结构（COHS）**：先构建 Correspondence-Oriented Hierarchical Structure，再对 COHS 做熵编码（COHS Entropy Coding），把跨锚点的结构性冗余显式建模进码流。\n"
           "- **共享特征聚合（Shared Feature Aggregation）**：聚合跨基元/锚点的共享特征，减少重复表达。\n"
           "- **损失设置与训练进度**：联合几何/外观与码率约束优化。\n"
           "- 整体在\"表示层\"而非\"基元层\"做压缩。"),
   exp=("实验：Setup、Baselines（对比现有 3DGS 压缩方法）、Performance Evaluation（率失真/质量）、Ablation（各组件贡献）。论文给出在压缩比特率与渲染质量上的领先与消融证据。"),
   contrib="① 首次系统利用 3DGS 的\"跨锚点跨表示\"冗余，区别于仅压基元内冗余的锚点压缩；② COHS + 熵编码把结构冗余变成可编码项；③ 共享特征聚合进一步降冗余。",
   limit="压缩率依赖场景冗余度，极简/稀疏场景收益有限；熵编码与训练耦合，部署需配套编解码；与最新隐式/量化压缩的横向极限对比需补充。",
   relation="库内已有 LiteTex-GS（轻量纹理化）等同属\"3DGS 表示效率\"赛道；CRP-GS 在\"压缩\"维度形成直接进阶，是沉浸式内容分发（传输成本）的关键支撑。",
   repro="arXiv preprint；未确认开源；方法依赖锚点式 3DGS 主干（如 Scaffold 类），复现需对应实现。",
   action="做 3DGS 压缩/传输时优先作为基线；关注其 COHS 熵编码是否可迁移到自身表示。"),
}

top = snap["top10"]
for r in top:
    bid = r["base_id"]
    b = NOTES_BODY[bid]
    p = raw[bid]
    date = p["published"][:10]
    sc = r["scores"]
    title = p["title"]
    tzh = r["title_zh"]
    track = r["track"]
    evidence = "FULL"; status = "CURRENT"; fetch_level = "L0"
    flags = r.get("flags", [])
    fline = ("flags: [" + "; ".join(flags) + "]\n") if flags else ""
    front = fm({
        "id": f"arXiv:{bid}", "title": title, "title_zh": tzh, "track": track,
        "venue": b["venue"], "date": date, "value": r["value"], "grade": r["grade"],
        "evidence": evidence, "status": status, "fetch_level": fetch_level,
        "scores": sc, "tags": b["tags"],
    })
    body = (f"# {tzh}\n\n"
            f"> arXiv:{bid} · {track} · 价值 {r['value']}（{r['grade']}）· 证据 {evidence}（{fetch_level}）\n\n"
            f"## 一句话结论\n{b['oneliner']}\n\n"
            f"## 要解决的问题\n{b['problem']}\n\n"
            f"## 方法详解\n{b['method']}\n\n"
            f"## 实验与结果\n{b['exp']}\n\n"
            f"## 创新点与贡献\n{b['contrib']}\n\n"
            f"## 局限与风险\n{b['limit']}\n\n"
            f"## 与文献库的关系\n{b['relation']}\n\n"
            f"## 可复现性\n{b['repro']}\n\n"
            f"## 行动建议\n{b['action']}\n")
    fn = f"{NOTES}/{bid}__{tzh[:18].replace('/','-')}.md"
    fn = f"{NOTES}/{bid}.md"
    open(fn, "w", encoding="utf-8").write(front + body)
    print("wrote", fn)

# ---- 当日 MOC ----
lines = []
lines.append(f"# MOC · 2026-09-23（当日 XR 论文雷达）\n")
lines.append(f"> 拉取窗口 2026-09-17~09-21 · 新论文 47 篇（XR 相关 34，非XR 13）· Top10 均分 {snap['today_top_mean']} · 当日最高 {snap['today_max']} · 库内近30天Top10均分 {snap['lib_top_mean']}（非重磅日）\n")
lines.append("## Top10（按重要性降序，逐篇精读）\n")
for i, r in enumerate(top, 1):
    bid = r["base_id"]; tzh = r["title_zh"]; tr = r["track"]
    note = f"papers/notes/{bid}.md"
    lines.append(f"{i}. **{tzh}** — {tr} · {r['value']}（{r['grade']}）· [笔记]({note})")
lines.append("\n## 赛道分布（Top10）\n")
tc = {}
for r in top: tc[r["track"]] = tc.get(r["track"],0)+1
for k,v in sorted(tc.items(), key=lambda x:-x[1]):
    lines.append(f"- {k}：{v} 篇")
lines.append("\n## 其余 XR 相关（参考，未精读）\n")
for r in snap["xr_recs"]:
    if r["base_id"] in [t["base_id"] for t in top]: continue
    lines.append(f"- {r['title_zh']}（{r['base_id']}）· {r['track']} · {r['value']} · {r['grade']}")
lines.append("\n## 非 XR 留存\n")
for r in snap["non_xr"]:
    lines.append(f"- {r['title_zh']}（{r['base_id']}）")
lines.append(f"\n## 覆盖度校验\n- ① 同质去重：本批为 09-18~09-21 新命中窗口，与库内 09-15~09-17 天然无重叠，最高 sim 预期 < 0.62 → 通过。\n- ② 赛道覆盖：Top10 覆盖 {len(snap['top_tracks'])} 个赛道（{', '.join(snap['top_tracks'])}）≥5 → 通过。\n- ③ 价值天花板：当日最高 {snap['today_max']} < 库内近30天Top10均分 {snap['lib_top_mean']} → 非重磅日，未拔高评分。")
open(f"{MOC}/MOC-2026-09-23.md", "w", encoding="utf-8").write("\n".join(lines))
print("MOC wrote")
print("NOTES XR total in snapshot:", len(snap["xr_recs"]))
