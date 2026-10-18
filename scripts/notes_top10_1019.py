# -*- coding: utf-8 -*-
"""notes_top10_1019.py — 生成 Top10 原子笔记（详写，基于 L0 全文精读）。"""
import json, os

ROOT = 'D:/Agent/WorkBuddy/Research'
OUT = f'{ROOT}/papers/notes'
os.makedirs(OUT, exist_ok=True)

NOTES = []

NOTES.append(dict(
    id='2610.19674',
    slug='smore-scaffold-memory-3d-geometry',
    title='Remember, Revisit, Revise: Scaffold Memory for Long-Horizon 3D Geometry',
    title_zh='记住、重访、修订：长时程 3D 几何的脚手架记忆（SMoRe）',
    track='重建与SLAM',
    venue='arXiv preprint',
    date='2026-10-14',
    value=4.57, grade='S',
    evidence='FULL', status='CURRENT',
    scores={'IMP':5,'NOV':4,'TEC':5,'EXP':5,'PER':5,'TRL':3,'REP':4},
    tags=['几何基础模型','长时程重建','SLAM','在线修订','点云'],
    conclusion='给前馈/流式几何基础模型（DUSt3R/VGGT/π³ 等）加一层可在线修订的「脚手架记忆」，把 Replica 重建误差从 12.85cm 压到 3.85cm（约 3.3 倍），且对流式模型同样有效。',
    problem='几何基础模型以固定长度窗口处理长序列：前馈模型逐窗口独立预测再对齐，误差随窗口链式累积；流式模型保留历史服务未来预测，却无法在后续观测揭示错误时修订早前估计。长时程 3D 几何（位姿+结构）一致性因此成为基础模型落地的核心瓶颈。',
    method='SMoRe（Scaffold MemOry for Revision）在流式模型之上维护一份全局「脚手架状态」：① 将窗口变换后的相机位姿/方向编码为紧凑记忆地址，学习「观测→地址」与「地址→脚手架状态」的联想通路；② 当当前观测与某历史地址关联（重访）时，从该地址恢复早前脚手架状态，做几何校验（双源窗口联合预测），必要时修订全局摆放；③ 修订后的窗口变换用于更新全局地图；④ 持续吸引子场（continuous attractor fields）维持与移动所表征的位姿，保证状态可恢复。高斯解码器把存储的几何渲染成图像用于评估（每源像素 11 通道输入，约 7M 参数四级 U-Net）。',
    experiments='五项下游任务全面验证：相机位姿估计、多视图深度、3D 点云重建、SLAM、新视图合成。Replica：DUSt3R 12.85→3.85cm、Fast3R 14.15→4.21cm、MASt3R 5.88→3.15cm、VGGT 9.50→2.55cm、VGGT-Ω 7.80→2.05cm、π³ 4.55→2.25cm；StreamVGGT 6.90→1.92cm、STream3R 3.55→1.72cm。ScanNet++：DUSt3R 32.40→8.51cm、VGGT 25.80→6.25cm、VGGT-Ω 21.50→5.15cm。SLAM 在 7-Scenes 七场景对比 NICER-SLAM/DROID-SLAM/MASt3R-SLAM/GLUEMAP/VGGT-SLAM++/CUT3R 等 12 个已发表基线；每实验三次运行取均值。',
    innovation='① 首次把「修订」引入几何基础模型的长时程流程——不是丢弃历史而是可回改的脚手架状态；② 框架无关：对 8 个主流 GFM（含流式）一致有效，说明是通用外层而非特调；③ 误差降幅达 3-4 倍，属数量级改进。',
    limits='① 脚手架状态的联想通路为在线学习，冷启动与鲁棒性依赖训练分布；② 修订触发依赖重访检测，首次到访的错误无法当期纠正；③ 计算开销（诊断/检索）论文报告有限；④ 尚未在超大场景（>建筑级）验证。',
    relation='与库内 VGGT-BC（2610.10538 一类前馈路线）、STream3R/CUT3R（流式路线）构成「基础模型长时程化」的第三条路线（可修订记忆层）；与 cuVSLAM/LIN-SLAM/HexVIO 等传统 SLAM 是不同范式（无手工前端/后端）。',
    repro='论文含完整附录（A-I 九节，含训练配置与诊断协议）；作者未在 digest 可见处给出代码链接，复现需按附录实现；评估协议公开（数据集/指标/对齐方式写明）。',
    action='追踪其开源状态；对做长序列 3DGS/数字孪生的管线，SMoRe 可作为 GFM 输出的即插即用后处理层评估。',
))

NOTES.append(dict(
    id='2610.18872',
    slug='egoexplorer-vision-motion-touch-observatory',
    title='EgoExplorer: A Vision-Motion-Touch Observatory for Human Loco-Manipulation In Situ',
    title_zh='EgoExplorer：原位人类运动-操作视觉-动作-触觉观测站（100 小时）',
    track='触觉与多模态',
    venue='arXiv preprint（上海AI实验室等）',
    date='2026-10-13',
    value=4.30, grade='S',
    evidence='FULL', status='CURRENT',
    scores={'IMP':4,'NOV':4,'TEC':5,'EXP':4,'PER':5,'TRL':4,'REP':4},
    tags=['第一视角','可穿戴','触觉数据集','全身重建','接触标注'],
    conclusion='用 5 个 inside-out 追踪器 + 头戴相机 + 手套构成无外部相机阵列的可穿戴系统，产出 100 小时「视觉-运动-触觉」对齐的人原位运动-操作数据；全身重建 18.0mm、手部 Tip RMS 9.5mm/成功率 100%、接触 IoU 0.915，大幅超越多视角 RGB 与惯性服方案。',
    problem='学习人形运动-操作需要同时观测移动、姿态、物体交互如何随任务协同演化；现有数据集只有部分视角（HOT3D 需光学标记+红外相机体积、Nymeria/ParaHome 需惯性服+相机阵列），部署受限，且几乎没有「区域接触」的稠密标注。',
    method='硬件层：五 inside-out 追踪器（身体-传感器标定，无需外部阵列/基站）+ 头戴 ego 相机 + 触觉手套。算法层三层约束重建：① 骨骼运动约束（协议引导标定 + 先验运动补全）；② 表面间隙约束；③ 身体-地面一致性约束 + 关节精化。手-触融合与专家程序上下文注入，MLLM 生成文本标注并经人工核验（事实错误率等五类指标专家审查）。评测子集覆盖全身运动、手指 articulation、区域接触。',
    experiments='全身重建：18.0mm body-point / 20.3mm non-tracked（17 未观测关节），优于公开预训练 checkpoint + 标定转换、裸追踪器位姿、五锚点微调三种基线（基线 86-128mm 量级）。手部：Tip/Hold RMS 9.5/0.4mm、Missing 0.0%、Gap p95 0.00s、Success 100%（HaWoR 27.1/4.5mm、47%；HandFlow 30.7/11.3mm、67%）。接触：IoU 0.915/F1 0.956 vs RGB HACO 0.621/0.766、纯手部姿态 0.324/0.490。另含 Cosmos3-Edge 初步训练研究（视频+SMPL-X 动作+触觉联合生成）与专业-技能消融。',
    innovation='① 无外部阵列的全身-手-接触统一可穿戴采集；② 三层约束把稀疏锚点扩展到全身 articulation（肘/膝误差也降）；③ 接触质量的量化基准（帧-区域标签）此前缺失；④ 视觉-运动-触觉-文本四对齐闭环。',
    limits='① 手套/追踪器仍是侵入式可穿戴（对比纯视觉方案）；② 自然录制子集无精度参考，只评传感器一致性与几何一致性；③ 初步训练研究为概念验证（Cosmos3-Edge 适配），规模有限；④ 许可 CC BY-NC-SA 4.0 限非商用。',
    relation='补强库内「第一视角多模态」薄处（与 ReViV/第一视角 4D 手类互补）；触觉区域接触标注与库内触觉感知类（如粘弹性渲染感知）形成「采集-标注-感知」链条。',
    repro='数据集格式、统计、重建协议全部在附录公开；评测子集与参考标注可复现；许可非商用。',
    action='人形/灵巧操作团队可直接申请使用；做 sim2real 的可用其接触标签做接触一致性校验。',
))

NOTES.append(dict(
    id='2610.17474',
    slug='hoopoe-holography-perceptual-loss',
    title='HoOPOE: A Holography-Optimized Perceptual ObjectivE function',
    title_zh='HoOPOE：全息优化的感知目标函数（CGH 散斑隐藏）',
    track='渲染与显示',
    venue='SIGGRAPH Asia 2026 Conference Papers',
    date='2026-10-12',
    value=4.27, grade='S',
    evidence='FULL', status='CURRENT',
    scores={'IMP':5,'NOV':4,'TEC':4,'EXP':5,'PER':4,'TRL':3,'REP':4},
    tags=['全息显示','计算机生成全息','散斑','感知度量','近眼显示'],
    conclusion='为计算机生成全息（CGH）提出感知损失 HoOPOE：以人眼时空频率+颜色敏感度加权，把散斑藏进视觉不敏感区；12 人 4362 组成对比较（JOD 度量）显示显著优于 MSE/MSE-LAB/SCCGH 等基准（p<0.05，部分 p<0.001），且给出 240fps 为性价比拐点的帧率-功耗-质量实证。',
    problem='全息设备要用有限 SLM 像素借助标量波衍射重建整个光场，相干照明导致 CGH 优化普遍带散斑（speckle）。通用图像损失（MSE 等）不理解人眼对时空频率与颜色的敏感度，优化目标与「看起来好不好」脱节。',
    method='HoOPOE 把 HVS 的 spatio-temporal 频率敏感度与颜色敏感度参数化进 CGH 优化目标：空间加权（Spatial HoOPOE）处理色度/亮度权重，时间加权（利用帧间视觉积分）进一步隐藏闪动散斑。两个变体（Spatial / 完整 HoOPOE）在相同 CGH 优化器下对比基准损失。',
    experiments='用户研究：12 名参与者、4,362 组成对比较，pwcmp 库转 JOD（1 JOD = 75% 偏好概率），1,000 bootstrap，剔除 1 名离群者。HoOPOE 在各基准帧率下显著占优（p<0.05，部分 p<0.001）；Spatial HoOPOE > MSE-LAB（证空/色加权有效），HoOPOE > Spatial HoOPOE（证时间加权价值）。帧率实验：120→240fps 提升最大（74% 偏好），240→480fps 仅 50.7% 偏好；单帧验证（N=18）排除时间复用依赖。',
    innovation='① 首个 CGH 专用感知损失（区别于通用图像质量损失）；② 空-时-色三维 HVS 建模系统落地到全息优化；③ JOD 度量 + 帧率-功耗联合实证，给全息显示的工程折中提供数据。',
    limits='① 感知模型参数（频率/颜色敏感度）的人群泛化待验（N=12/18 偏小）；② 在 SLM 分辨率/视场扩大下的行为未测；③ 与学习式 CGH 前沿的对比未纳入；④ 散斑隐藏不等于散斑消除（物理层仍受衍射极限约束）。',
    relation='库内第二篇硬件类渲染论文（继 2609.11434 CVQPG 全息 3DGS 显示之后），直接补「近眼显示/全息」长期缺口；与算法侧 3DGS 渲染形成「软件生成-硬件呈现」对照。',
    repro='SIGGRAPH Asia 正会论文（DOI 10.1145/3829340.3842313），补充材料 S7/S8/S9/S16 含逐刺激 JOD 与假设检验；作者来自 Rochester/Meta/UNC。',
    action='做全息/光场显示评估时优先采用 JOD 口径；帧率实验数据可作为近眼硬件功耗预算参考。',
))

NOTES.append(dict(
    id='2610.14685',
    slug='demiurge-navigable-4d-worlds',
    title='Demiurge: Forging Navigable 4D Worlds via Autoregressive Video Rerendering',
    title_zh='Demiurge：自回归视频重渲染锻造可导航 4D 世界',
    track='世界模型与仿真',
    venue='arXiv preprint',
    date='2026-10-10',
    value=3.85, grade='A',
    evidence='FULL', status='CURRENT',
    scores={'IMP':4,'NOV':4,'TEC':4,'EXP':4,'PER':4,'TRL':3,'REP':3},
    tags=['4D 世界模型','视频扩散','点云记忆','新视图合成','导航'],
    conclusion='把单视频 + 相机轨迹重渲染成 N 条目标轨迹一致的 4D 世界：动态 4D 点云记忆做持久世界状态，逐轨迹「生成-恢复-更新」自回归迭代（外观视频扩散 + 视频深度补全 + 几何精化 + 双流 warping），跨轨迹一致性显著优于独立处理轨迹的方法；作者承诺开源代码/权重/评测脚本。',
    problem='视频扩散已能单视频新视图合成，但现有方法独立处理各相机轨迹，缺乏构建连贯可导航 4D 世界所需的跨轨迹一致性（同一场景沿不同路径走，外观/几何会漂移）。',
    method='① 记忆引导外观视频扩散：渲染 4D 记忆得视觉条件（RGB/深度/掩码）引导扩散；② 记忆一致视频深度补全（cache-supported 区域 + 全局仿射对齐 + Poisson 精化）；③ 记忆感知双流 warping（流特定源掩码、并行点云 warping、深度冲突检测、逐像素流选择）；④ 几何感知视频精化 + 反投影融合回记忆，进入下一轨迹。generate-recover-update 循环逐步扩展可导航世界。',
    experiments='以 FVD、Q-Align、Projection MSE、相机轨迹估计（旋转/平移误差）为指标，对比最佳感知质量、跨轨迹一致性、相机可控性三项均称 SOTA；报告训练数据构成、骨干、分辨率、序列长度与算力；含项目页与补充视频。',
    innovation='① 「generate-recover-update」自回归循环把世界状态显式维护在 4D 点云记忆中；② 双流 warping 处理深度冲突（静态/动态分流）；③ 跨轨迹一致性作为一等指标（此前极少被量化）。',
    limits='① 依赖单目深度估计的初始记忆，尺度/遮挡误差会传导；② 长轨迹累积漂移未量化；③ 动态物体的大幅形变/非刚性行为受限；④  digest 未见与最新 4D 专用方法的逐项对比。',
    relation='与库内世界模型类（ME-World/OuroWorld/Thinker-WM/DAO+JING）同属「可交互世界生成」但路径不同（显式点云状态 + 视频扩散重渲染 vs 端到端隐状态）；与 4DGS 类编辑/生成（Edit4D 等）互补。',
    repro='匿名项目页 + 拟 release 代码/checkpoint/评测脚本；digest 未给出链接。',
    action='机器人/具身仿真团队可作「真视频→可导航 4D 环境」的低成本管线评估；关注其开源后的跨轨迹一致性基准。',
))

NOTES.append(dict(
    id='2610.18447',
    slug='thinker-wm-unified-world-model',
    title='Thinker-WM: A Unified World Model with Shared Multimodal Representations for Embodied Intelligence',
    title_zh='Thinker-WM：共享多模态表征的统一世界模型',
    track='世界模型与仿真',
    venue='arXiv preprint',
    date='2026-10-13',
    value=3.85, grade='A',
    evidence='FULL', status='CURRENT',
    scores={'IMP':4,'NOV':4,'TEC':4,'EXP':4,'PER':4,'TRL':3,'REP':3},
    tags=['世界模型','多模态生成','RGB-D-动作','闭环控制','RoboTwin'],
    conclusion='一个共享「统一动力学 Transformer」同时建模并生成 RGB、度量深度与机器人动作三模态；RoboTwin turn_switch 闭环任务成功率从 RGB-only 60.0% → 单向深度 63.3% → 双向交互 75.0%（+15.0 个百分点），证明外观与几何在共享骨干内共同演化有实收益；深度 AbsRel 0.136 优于 RynnWorld-4D 的 0.1625。',
    problem='世界模型系统通常把视觉动态、几何结构、可执行动作拆给独立接口/下游模块，模态间只是松耦合，无法在同一动力学模型里联合表征与演化。',
    method='统一动力学 Transformer（Unified Dynamics Transformer）作为共享中间表征，联合建模 RGB、metric depth 与 robot action；生成端共享扩散采样框架。闭环消融：RGB-only（去深度流）/ RGB+Depth one-way（限制交互单向）/ 完整双向。',
    experiments='RoboTwin turn_switch：三配置同训练配方（8K 步、24 帧、48 步动作视界），6K/7K/8K checkpoint 各 20 次闭环试验，总体成功率 60.0/63.3/75.0%；深度质量 AbsRel/RMSE 对比 RynnWorld-4D。',
    innovation='① 三模态（RGB+深度+动作）在单一共享动力学 Transformer 内联合生成，而非接口拼接；② 双向 RGB-深度交互的闭环收益被量化（+15pp 不可替代）。',
    limits='① 单任务闭环验证（turn_switch），泛化待验；② 动作空间限于该平台；③ 训练成本（8K 步）对复现有一定门槛；④ 与视频生成型世界模型（如 Demiurge/DAO+JING）未同台对比。',
    relation='与库内世界模型三路线并立：端到端生成式（DAO+JING）、显式状态+扩散（Demiurge）、统一多模态动力学（本篇）；深度-动作联合与库内 VLA/几何基础模型线互补。',
    repro='digest 未明确代码/数据链接；训练配方（8K 步/24 帧/48 步）已写明，可依此复现实验设置。',
    action='做具身世界模型的建议把「双向 RGB-深度交互」列为必测消融；关注多任务扩展。',
))

NOTES.append(dict(
    id='2610.15074',
    slug='motionanimator-xr-animation-authoring',
    title='MotionAnimator: Semantic-to-Motion Reasoning for Animating Part-Structured 3D Assets in XR',
    title_zh='MotionAnimator：XR 中部分结构化 3D 资产的语义到运动推理动画创作',
    track='空间计算与UI',
    venue='arXiv preprint（Penn State）',
    date='2026-10-10',
    value=3.78, grade='A',
    evidence='FULL', status='CURRENT',
    scores={'IMP':4,'NOV':4,'TEC':4,'EXP':4,'PER':3,'TRL':4,'REP':3},
    tags=['XR 内容创作','语义运动接地','代码生成','Unity','Quest 3'],
    conclusion='把「XR 里让 3D 资产动起来」重构为语义运动接地问题：语义理解代理（SUA）+ 运动规划代理（MPA）把用户意图解析为部件级参数化运动计划，再生成 Unity C# 代码在运行时编译执行；Quest 3 实测 SUA 物体身份 97.78%/部件标注 96.90%/方向框架 99.26%，端到端人评 IMA 5.83±1.16（ICC(2,5)=.794），去掉 MPA 得分从 5.57 崩到 2.54。',
    problem='3D 数字资产（教育/仿真/设计/沉浸式内容）大多只有几何与部件结构、缺语义标注与可执行行为；动画仍需手工 rigging、模板或编程，门槛高。MotionAnimator 让未标注资产在 XR 里边想边动。',
    method='意图 + 结构化 XR 场景上下文 + 目标聚焦捕获 → ① SUA 识别物体与功能部件、推断部件级运动 affordance（含语义方向框架 grounding）；② MPA 构造对象级/部件级协同的参数化运动计划；③ 生成 Unity C# 代码，运行时编译成可执行 XR 动画。实现：Unity 2022.3.58f1 + Meta XR All-in-One SDK/OpenXR，部署 Meta Quest 3，语音经 OpenAI 转录。',
    experiments='技术评估：SUA 三指标 97.78/96.90/99.26%；MPA MPF1 99.16% 但 MAA 87.77%（「哪些部件该动」易、「怎么动」难，Aerial Mobility 运动轴错误率最高 75%）。人评动画：5 名独立评估者（2 VR 开发+2 教师+1 学生）×30 case-level means，OLM/PLM/MD/OPC 四维 7 点量表，Full 5.77±1.15（Avg 5.57±1.35）；消融：w/o MPA 2.54、w/o SUA 4.14、SUA w/o SF 4.83、MPA w/o GE 5.07；Wilcoxon 配对 + Holm 校正；编译成功率 100%。',
    innovation='① 把 XR 动画创作定义为「语义运动接地」新任务；② 意图→计划→运行时代码的闭环（而非预制模板）；③ 人评+编译成功率+消融三重证据。',
    limits='① 运动轴/关节接地的精确度是主要失败源（MAA 87.77%，复杂几何行为更难）；② 依赖 LLM 语义先验，领域外资产可能误判 affordance；③ 单场景/单用户评估规模有限（n=30 case means）；④ 无长期创作工作流研究。',
    relation='库内 XR 创作工具类稀缺，本篇与 reVISit-XR（研究基础设施）互补；语义运动接地与库内语义 3DGS/场景图类共享「语义-几何对齐」主题。',
    repro='技术栈与指标写明；digest 未见公开代码链接；评测脚本与 prompt 模板有望随论文补充。',
    action='XR 教育/数字孪生团队可评估其「零 rigging 动画」管线；关注运动轴接地的后续改进。',
))

NOTES.append(dict(
    id='2610.19857',
    slug='omniposer-masked-flow-matching',
    title='OmniPoser: Flexible Human Motion Recovery in the Wild with Masked Flow Matching',
    title_zh='OmniPoser：掩码流匹配实现的通用户外人体运动恢复（含头显 6-DoF 输入）',
    track='化身与人体',
    venue='arXiv preprint（SJTU + 上海AI实验室）',
    date='2026-10-14',
    value=3.78, grade='A',
    evidence='FULL', status='CURRENT',
    scores={'IMP':4,'NOV':4,'TEC':4,'EXP':4,'PER':3,'TRL':4,'REP':3},
    tags=['化身驱动','稀疏传感','头显 6-DoF','流匹配','实时推理'],
    conclusion='一个模型吃任意组合的异构稀疏观测（3D 关键点、关节旋转、头显 6-DoF 位姿、稀疏 IMU 及其子集），用跨模态掩码 + Masked Conditioning Encoder + 解耦双流 + 条件流匹配，单步 ODE 推理恢复 SMPL 全身运动；三设置七基准与 SOTA 持平，速度 700+ FPS。',
    problem='稀疏可穿戴传感器（XR 头显/IMU/关键点子集）恢复全身运动本质欠定；现有方法绑定固定传感器配置，且基于扩散的推理慢到无法实时部署。',
    method='统一运动表示（root 轨迹、3D 关节、6D 旋转、形状、足接触）；跨模态掩码把任意观测视为同一规范身体表征的部分视图，未观测关节换为可学习 per-joint 嵌入（MCE 区分缺失模式）；解耦双流（temporal conv UNet 全局轨迹 + cross-attention DiT 局部姿态）以条件流匹配生成，单次 ODE 求值实时推理。',
    experiments='Setting 1 稀疏观测（AMASS/Nymeria，上半身关节位置/随机掩码，对 RoHM/HuMoR）；Setting 2 头显 6D 位姿（AMASS/RICH/Nymeria，对 EgoEgo/EgoAllo）；Setting 3 6 IMU+关键点（AIST++/TotalCapture/Nymeria）。七基准一致「与 SOTA 持平」且 >700 FPS；含 MCE 嵌入、多样性、输入约束与推理步数消融。',
    innovation='① 传感器配置无关的统一生成式 conditioning（一个模型覆盖所有组合）；② MCE 的 per-joint 可学习缺失嵌入；③ 流匹配单步推理把扩散级质量带到实时（700+FPS）。',
    limits='① 单人建模，无 body-object/多人交互；② 与 SOTA 持平而非全面超越（增益在速度与通用性）；③ 病态观测（极端稀疏）的失败模式未系统分析。',
    relation='直接服务库内「化身驱动」线（头显 6-DoF→全身）；与库内 AvatarPoser/EgoPoser/HMD-Poser 类构成同一问题的不同世代（统一掩码 conditioning 是通用性跃迁）。',
    repro='七基准协议写明；digest 未见代码链接；SMPL 许可需注意。',
    action='XR 头显厂商/虚拟化身团队可评估其作为通用驱动层的可行性；重点验证自身传感器组合下的精度-速度权衡。',
))

NOTES.append(dict(
    id='2610.16252',
    slug='mflowhoi-one-step-hoi-generation',
    title='MFlowHOI: Whole-Body Human-Object Interaction Generation via Part-Aware MeanFlow',
    title_zh='MFlowHOI：部件感知 MeanFlow 的全身人-物交互一步生成',
    track='内容生成',
    venue='arXiv preprint（中科院软件所 + UCAS + Google）',
    date='2026-10-12',
    value=3.70, grade='A',
    evidence='FULL', status='CURRENT',
    scores={'IMP':4,'NOV':4,'TEC':4,'EXP':3,'PER':4,'TRL':3,'REP':3},
    tags=['人-物交互生成','MeanFlow','RVQ-VAE','3DGS 渲染','化身内容'],
    conclusion='把全身 HOI 生成（身体+手指+物体轨迹+时变接触）压到单次网络评估：接触感知多部件 RVQ-VAE 编成时间-部件潜空间，ST-DiT 在该空间学条件 MeanFlow 速度场，单次 transport 评估生成完整交互；预测的物体局部接触进一步支持几何修正与向不同体型 3DGS 化身的交互保持迁移。',
    problem='全身 HOI 生成要协调身体、手指、物体轨迹与时变接触，现有方法靠迭代扩散或测试时优化，推理成本高；直接套用一步 MeanFlow 到现有 HOI 表示会导致运动质量下降与接触不稳定。',
    method='① 接触感知多部件 RVQ-VAE：按功能部件（身体/手/物体/接触）分解，流特定时间编码器捕捉细粒度动态，共享解码器保全局协调，形成结构化时间-部件潜空间；② 条件 MeanFlow：ST-DiT（时空+跨部件注意力）单次评估生成完整潜序列；③ 接触对应关系 → 几何精化 + 交互保持迁移到照片级 3DGS 化身。',
    experiments='GRAB（10 受试者×51 刚性物体）上较现有生成器提升分布质量与文本-动作对齐，推理延迟大幅下降；消融证实多部件潜空间及其时间/跨部件建模的必要性。',
    innovation='① 一步式 HOI 生成（单次 transport 评估）在质量-速度上同时占优；② 时间-部件结构化潜空间解决 HOI 组件异构（结构/尺度差异大）问题；③ 接触对应关系打通「生成→几何修正→化身渲染」链路。',
    limits='① 仅单一刚性物体（铰接/可变形物体留待未来）；② 单数据集（GRAB）评估；③ 接触预测精度对迁移保真度的影响未量化。',
    relation='库内 HOI/抓取生成线的「一步化」进展（与扩散类生成互补）；3DGS 化身渲染与库内化身编辑/生成类（ChromaGS/ManifoldSplat 等）共享渲染底座。',
    repro='GRAB 协议沿用前作；digest 未见代码链接。',
    action='虚拟人/游戏内容管线可评估一步生成带来的实时性；铰接物体扩展是下一个观察点。',
))

NOTES.append(dict(
    id='2610.14951',
    slug='foundationvio-metric-scale',
    title='FoundationVIO: Enforcing Metric Scale in Feed-forward Visual-Inertial Odometry',
    title_zh='FoundationVIO：前馈视觉惯性里程计中的度量尺度强制',
    track='重建与SLAM',
    venue='arXiv preprint（牛津 ORI + Georgia Tech）',
    date='2026-10-10',
    value=3.58, grade='B',
    evidence='FULL', status='CURRENT',
    scores={'IMP':4,'NOV':3,'TEC':4,'EXP':4,'PER':3,'TRL':4,'REP':3},
    tags=['VIO','SLAM','几何基础模型','因子图','度量尺度','Meta Aria'],
    conclusion='把 GFM（DA3/VGGT-Ω 等）的 up-to-scale 位姿预测与 IMU 测量、batch 间相对尺度估计放进一个因子图，得到原生度量尺度的轨迹与重建；视觉-惯性初始化用 GFM 位姿替换 SfM，低纹理/小视差下更稳；笔记本（i7-13850HX + RTX 3500 Ada 12GB）实时。',
    problem='GFM 预测局部一致但无物理尺度；即便在有尺度数据上训练也不直接测量尺度，链式 GFM 的轨迹/重建因此尺度漂移。',
    method='因子图变量：per-batch 尺度 l_k=log s_k、per-frame 位姿/速度/偏置；测量：IMU 预积分、GFM 位姿因子、batch 间尺度一致性因子。初始化沿用 VINS-Mono 的视觉-惯性初始化，但把 SfM 换成 GFM 位姿预测。兼容无人机/手机/AR 眼镜常见传感器。',
    experiments='三数据集：自采 Meta Aria Gen 1 头戴序列（150° HFoV 灰度相机 + 110° RGB + 双 IMU，多楼层多回环）、Oxford Spires、ScaRF-SLAM；里程计模式 + SLAM 模式（带回环）分别评估；稠密重建对比 GFM-enabled SLAM SOTA；笔记本实时性验证。',
    innovation='① 「GFM 前馈 + IMU 尺度约束」的系统化组合（非松耦合）；② GFM 位姿替换 SfM 的初始化在退化条件更稳；③ 明确以 AR 眼镜传感器配置为目标场景之一。',
    limits='① 依赖 GFM 预测质量（病态场景仍受限）；② 因子图规模随序列增长的效率未充分讨论；③ 头戴序列的激进运动（快速转头）下的退化行为待测。',
    relation='与库内 cuVSLAM（线特征低纹理）/LIN-SLAM（LiDAR-惯性神经）/HexVIO（轻量 VIO）构成「传统-神经-混合」VIO 谱系；GFM+尺度约束是与 SMoRe 并行的基础模型落地化路线。',
    repro='数据集（自采 Aria）与协议公开程度有限；实现依赖 DA3/VGGT-Ω 权重。',
    action='AR 眼镜/无人机 SLAM 团队评估「现成 GFM + IMU」低成本方案；关注自采 Aria 数据是否放出。',
))

NOTES.append(dict(
    id='2610.18183',
    slug='ar-office-object-recall',
    title='Exploring Object Recall in an Object-Rich AR Office Scene',
    title_zh='物体丰富的 AR 办公场景中的物体回忆研究（ISMAR 2026）',
    track='感知与认知',
    venue='IEEE ISMAR 2026 / TVCG（preprint）',
    date='2026-10-13',
    value=3.57, grade='B',
    evidence='FULL', status='CURRENT',
    scores={'IMP':4,'NOV':3,'TEC':4,'EXP':4,'PER':3,'TRL':3,'REP':4},
    tags=['AR 认知','注意力、物体回忆','混合现实、用户研究'],
    conclusion='ISMAR 2026 用户研究：在虚实物体密集的 AR 办公室里做选择任务后测物体回忆，系统操纵物体级（虚拟性/尺寸）、上下文级（语义一致性/显著性）与用户级（线索提示/双任务音频）因素；发现 cueing 显著改善回忆，为「AR 是否降低对物理世界注意」提供了密集场景下的细粒度证据。',
    problem='既往认为 AR 会降低对物理环境的注意，但在虚实物体同样密集的环境中是否成立、哪些因素主导物体回忆，缺乏实证。',
    method='AR 头显 + 杂乱办公室场景；8 试次×45 秒，每试次 16 物体虚拟列表（指向-点击选择）；32 物体场景（16 物理/16 虚拟），回忆测试 8 物理+8 虚拟；用户级因素：无线索前 4 试次→语言线索后 4 试次；半数试次叠加音频双任务增加认知负荷；物体级/上下文级因素同步记录；含从参与者视点计算物体显著性的数据处理管线。',
    experiments='被试规模与完整统计见正文（ISMAR 正会版）；因变量为回忆准确率，分析 object/user/context 三层因素主效应与交互。',
    innovation='① 首个在「虚实双密集」办公场景操纵四层因素的回忆研究；② 把 saliency/congruency 等上下文计算指标与行为数据对齐；③ 对 AR 注意力占用的争议给出场景化答案。',
    limits='① 实验室场景（办公室）外向效度待验；② 45s 试次较短，长期记忆效应未覆盖；③ 头显型号/渲染质量对结论的影响未分离。',
    relation='与库内 VR 眼动/晕动/认知负荷类用户研究互补；为 AR 信息密度设计（多少虚拟标注算「过载」）提供实证锚点。',
    repro='ISMAR/TVCG 正会；数据分析管线（显著性计算）论文描述可复现。',
    action='AR UI/信息呈现设计者可引用其因素框架做密度-回忆权衡；后续可做长时间尺度复现。',
))

for n in NOTES:
    fm = []
    fm.append('---')
    fm.append(f'id: arXiv:{n["id"]}')
    fm.append(f'title: "{n["title"]}"')
    fm.append(f'title_zh: "{n["title_zh"]}"')
    fm.append(f'track: {n["track"]}')
    fm.append(f'venue: {n["venue"]}')
    fm.append(f'date: {n["date"]}')
    fm.append(f'value: {n["value"]}')
    fm.append(f'grade: {n["grade"]}')
    fm.append(f'evidence: {n["evidence"]}')
    fm.append('status: CURRENT')
    fm.append(f'scores: {{IMP:{n["scores"]["IMP"]}, NOV:{n["scores"]["NOV"]}, TEC:{n["scores"]["TEC"]}, EXP:{n["scores"]["EXP"]}, PER:{n["scores"]["PER"]}, TRL:{n["scores"]["TRL"]}, REP:{n["scores"]["REP"]}}}')
    fm.append('fetch_level: L0')
    fm.append(f'tags: [{", ".join(n["tags"])}]')
    fm.append('---')
    fm.append('')
    fm.append(f'# {n["title_zh"]}')
    fm.append('')
    fm.append('> 批次：2026-10-19 补漏批次（公告日 ' + n["date"] + '，拉取日 2026-10-19，积压补漏非当日新提交）。')
    fm.append('')
    fm.append('## 一句话结论')
    fm.append(n['conclusion'])
    fm.append('')
    fm.append('## 要解决的问题')
    fm.append(n['problem'])
    fm.append('')
    fm.append('## 方法详解')
    fm.append(n['method'])
    fm.append('')
    fm.append('## 实验与结果')
    fm.append(n['experiments'])
    fm.append('')
    fm.append('## 创新点与贡献')
    fm.append(n['innovation'])
    fm.append('')
    fm.append('## 局限与风险')
    fm.append(n['limits'])
    fm.append('')
    fm.append('## 与文献库的关系')
    fm.append(n['relation'])
    fm.append('')
    fm.append('## 可复现性')
    fm.append(n['repro'])
    fm.append('')
    fm.append('## 行动建议')
    fm.append(n['action'])
    fn = f'{OUT}/{n["id"]}__{n["slug"]}.md'
    open(fn, 'w', encoding='utf-8').write('\n'.join(fm))
    print('wrote', fn)
