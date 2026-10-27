# -*- coding: utf-8 -*-
"""组装 2026-10-28 评分数据：digest（子代理全文精读）+ 主会话 7 维评分定稿。
输出 data/scored_1028.json（main 27 + backfill 10）。内联中文文本统一中文弯引号。"""
import json

D = {}
for g in ('g1', 'g2', 'g3', 'g4'):
    for d in json.load(open(f'data/digest_1028_{g}.json', encoding='utf-8')):
        D[d['id']] = d

# 评分表：id -> (title_zh, track, IMP,NOV,TEC,EXP,PER,TRL,REP, grade, grade_note, relation, action)
S_MAIN = {
 '2610.34263': ('RacerGS：残差自回归上下文的 3D 高斯泼溅压缩', '渲染与显示', 4,5,5,4,5,3,3, 'A',
   '总分 4.35 达 S 线（≥4.2），但当日最高分 4.35 < 库内近 30 天 Top10 均分 4.416 → 非重磅日，按校准关记 A（同 10-24 EgoHand / 10-27 WFM 先例）',
   '属库内 3DGS 压缩线（Scaffold-GS→HAC/HAC++→ContextGS 一脉）的率失真新顶点；与 Budgeted-GS（2610.03162，LOD 预算压缩）、RLSplat（2610.27712，资源线性预算）构成「压缩-预算」两条正交路线，门① max Jaccard 0.071 非同质。',
   'XR 流式传输管线首选压缩基线；关注算术编解码耗时占比与并行熵编码改进；与库内 RLSplat/Budgeted-GS 做同口径码率-质量复测。'),
 '2610.34233': ('BoundedGS：高分辨率 3DGS 训练的单卡显存有界执行', '系统与平台', 4,4,4,5,5,3,3, 'A', '',
   '属库内 3DGS 训练效率线（gsplat/Taming-3DGS/Faster-GS/InfiniGS），首次系统刻画完整训练步的显存峰值构成并把光栅化与投影反向解耦；与库内训练加速类工作互补而非取代。',
   '高分辨率 3DGS 资产生产可直接采用（单卡 4090 可训 12K）；关注 SSIM 叶片边界效应与 CPU 内存换 GPU 峰值的权衡。'),
 '2610.35152': ('CGR-GS：复杂度先验正则的可泛化人体高斯泼溅', '化身与人体', 4,4,4,4,5,4,4, 'A', '',
   '属库内可泛化人体高斯线（GPS-Gaussian/GHG/RoGSplat/GHGS-MVSC），以着装人体几何+纹理熵定义复杂度先验，把「高斯该放多密」变为可计算量；密度度量承自 CDC-GS。',
   '化身渲染管线的密度分配新范式；跨域零迁移 +0.93/+0.96 dB 有实用价值；关注 SMPL 蒙皮驱动扩展（作者自述未来工作）。'),
 '2610.34344': ('Birth-Death：以一阶变分分数做 3DGS 结构学习', '神经渲染', 4,4,4,4,4,4,4, 'A', '',
   '属库内 3DGS 密度控制线（后端 3DGS-MCMC，对照 AbsGS/EDGS/ConeGS/GHAP 系剪枝），理论源自 SRM（ICLR 2026）WFR first variation 的离散化；门① max Jaccard 0.071。',
   '紧预算 3DGS 训练（≤100k）优先对比基线；代码已开源可直接复用；关注自动曝光等跨视图不一致场景下的分数误导风险。'),
 '2610.33966': ('InteractiveWorld：可验证的人本闭环助手环境与 InteractiveBench', '评估与数据集', 4,4,4,5,3,3,5, 'A', '',
   '区别于库内 Ego4D/EgoPlan 静态第一人称基准与机器人中心模拟器，是首个动态多轮第一人称助手闭环基准；揭示「感知+记忆错误占首错 70.4%–85.7%」与库内具身助手评测互为补充。',
   '可穿戴助手研发的必用评测台；最佳模型仅 41.7% 通过率说明闭环能力远未解决；记忆字段增强（+5–15%）可直接借鉴。'),
 '2610.33158': ('GEMS：面向长时程时空推理的 3DGS 情景记忆', '重建与SLAM', 4,4,4,4,4,3,4, 'A', '',
   '与库内 Khronos/ReMEmbR/DAAAM/STaR/Mind Palace 等情景记忆/EQA 工作对比，差异在全视觉证据的 3DGS 时序 delta 保留（每高斯 lifespan）；数字孪生/机器人记忆方向。',
   '数字孪生长时程演化查询可复用其「时序切片+同位姿渲染对比」机制；存储随变化量增长（1.95 GiB/4 次重访）是关键卖点。'),
 '2610.33558': ('GeoLift：以显式 3D 地图为视频空间推理接地', '感知与认知', 4,4,4,4,5,2,3, 'A', '',
   '与库内 VG-LLM/Spatial-MLLM/VLM-3R/VideoAnchor/TRACE 等空间推理路线互补，差异在全冻结组件+显式 3D 计算（免训练）；首次量化 MLLM 多转弯路径规划崩塌。',
   '免训练即超 Qwen3-VL-8B 训练型方法，空间智能研究必备参照；门控回退机制设计可迁移到其他几何证据不可靠场景。'),
 '2610.35756': ('VidEdit3D：以视频扩散做灵活的 3D 高斯编辑', '内容生成', 4,4,4,4,4,3,4, 'A', '',
   '属库内 3DGS 编辑线（GaussianEditor/DGE/VCEdit/GaussCtrl/EditSplat/Omni3DEdit/ViP3DE），将参考引导 3D 编辑重构为 I2V 视频轨迹传播；与库内视频扩散化身线（Kandinsky S2V）共享 Wan 骨干。',
   '3D 内容编辑首选对比基线；TGR 关键帧选择+ECG 早期源条件放大是可复用技巧；交互成本高（14B 反复去噪）待轻量化。'),
 '2610.34845': ('PosePlaner：平面卷绕残差条件化的前馈位姿精化', '重建与SLAM', 4,4,4,4,4,3,3, 'A', '',
   '位于库内 DUSt3R/VGGT/CUT3R/TTT3R/WinT3R/Spann3R 前馈重建线与 NopeSAC 式软融合之间；与同批 Mem3R（2604.07279）可串联为「流式估计+周期性精化」。',
   '两视图训练、零重训练用作流式估计器尾部精化器，工程价值明确；平面结构少的场景增益下降，注意适用边界。'),
 '2610.33356': ('TLEIO：紧融合的Transformer 事件惯性里程计', '重建与SLAM', 4,4,4,4,4,3,3, 'A', '',
   '延续库内 TLIO 的 SC-EKF 过滤范式并以事件替代纯 IMU 学习约束；与库内 DEVO/DEIO/Ultimate-SLAM 事件里程计及 HexVIO（2610.03283，DSP 立体惯性）构成传感融合谱系。',
   '事件相机+XR 追踪的高效路线（运行时较优化类降 48.9%）；头级微调即可 sim2real 迁移；精度仍不及对应-优化类方法。'),
 '2610.34093': ('LegoOcc++：一致的开放词汇 3D 占用预测', '感知与认知', 4,4,4,4,4,3,3, 'A', '',
   'CVPR 2026 Oral LegoOcc 的期刊扩展，与库内 EmbodiedOcc/GaussianFormer2/PGOcc/GaussTR 构成占用预测谱系；Poisson 式 opacity-aware G2O 统一了几何聚合与语义渲染的不一致。',
   '开放词汇室内场景理解的强基线（IoU 61.73 超全部闭词全监督方法）；室外无标注扩展值得关注；6.22 FPS 距实时交互有距离。'),
 '2610.34952': ('DimFlow：网格-专家双向学习的动态高斯重建', '神经渲染', 4,4,4,4,4,3,3, 'A', '',
   '属库内动态 4D 高斯特征表示线（4D-GS/DG-Mesh/K-Planes/HexPlane/TiNeuVox-B/MSTH），以对抗对齐+掩码残差反馈实现两特征分支双向交换；与同批 GaussianSpline（轨迹参数化）构成动态表示两条正交路线。',
   '动态 4D 重建新对比基线（聚合 39.73 dB/85 FPS/18.9 MB）；FlowsME/TSV/EDE 诊断指标可复用于其他动态方法评测。'),
 '2610.35002': ('DUET4D：自校正耦合引导的稀疏视图 4D 重建', '神经渲染', 4,4,4,4,4,3,3, 'A', '',
   '属库内稀疏视图 4D 重建/生成先验线（SparseCam4D VDM 约 40 小时/场景、Diffuman4D、4C4D），以冻结 SDM+自校正规避重查询 VDM；与库内视频扩散先验线（World from Motion 2607.01202）共享「生成-蒸馏」思想但目标不同。',
   '稀疏相机 4D 重建新基线（Neu3d 20.28 dB/246 FPS/0.05M 高斯；受控对比超 SparseCam4D 且帧率 123/263/228 vs 11/8/12）；自校正闭环设计可迁移到其他生成先验+显式表示组合。'),
 '2610.35361': ('SG-Splat：位姿不确定性下稳定几何学习的免位姿前馈 3DGS', '重建与SLAM', 4,4,4,4,4,3,3, 'A', '',
   '属库内前馈重建线（NoPoSplat/AnySplat/WorldMirror/YoNoSplat/MVSplat/DepthSplat），几何/属性分支解耦+混合位姿训练解决训推不一致；几何先验来自 DUSt3R/MASt3R/VGGT/π³ 一系。',
   '免位姿 3DGS 重建新 SOTA（DL3DV 24v 23.19 dB）；位姿 AUC 超 VGGT/π³；假设内参已知限制野生图像适用性。'),
 '2610.33174': ('Bracketing：自适应包围曝光策略用于鲁棒视觉 SLAM', '重建与SLAM', 3,4,4,4,4,3,4, 'A', '',
   '与库内事件相机里程计、学习式曝光控制等高动态范围鲁棒位姿估计工作互补；首次把「采集策略×估计器」作为联合设计变量系统比较（B-Adapt×BVSLAM）。',
   '隧道/出入洞等快速光照跃变场景的 VSLAM 解决方案（误差降 78%）；BVSLAM 需离线处理，实时化是后续方向；代码已开源。'),
 '2610.34283': ('ChronoReplay：流式空间智能的因果回放监督组织', '感知与认知', 3,4,4,4,4,3,4, 'A', '',
   '与库内 StreamingBench/OVO-Bench 流式基准及 Video-R1/Cambrian-S 空间 SFT 互补，聚焦监督组织而非新架构；实证命名「接口锁定」现象。',
   '流式空间 VLM 训练必读：单族训练互相损害（-2.55 OST）的实证；族平衡配比 α=0.5 与因果回放构造可直接复用；代码+HF 模型已公开。'),
 '2610.35224': ('GaussianSpline：自适应 Bézier 样条的高动态 4D 高斯泼溅', '神经渲染', 4,4,4,3,4,3,3, 'A', '',
   '属库内动态 4D 高斯显式轨迹线（STG 多项式/Gaussian-Flow 多项式+Fourier/SplineGS 均匀 Hermite），是「均匀→自适应时间参数化」的一支； flames 27.42 dB 较次优 +3.46。',
   '高动态场景（火焰/碰撞）4D 重建优先尝试；无辅助网络的紧凑表示直接复用 3DGS 致密化管线；瞬态动力学仍需自适应插段。'),
 '2610.35554': ('Insta360 SfM 的惯性度量尺度估计', '重建与SLAM', 3,3,4,4,4,4,4, 'A', '',
   '与库内 COLMAP 管线 SfM、VIO 线性初始化（Martinelli/VINS）及单目度量深度尺度估计直接对应；证明 MoGe-2/3 单目度量深度偏差大（-3.2%/-18.8%）不宜作尺度参考。',
   '360 相机内容生产管线的自包含尺度方案（MAE 0.81%，免第二设备）；分段估计消偏是关键工程结论；OverMaps360-50 数据集已公开。'),
 '2610.33191': ('Whale You Go Green：具身对话化身的可持续行为劝导纵向实验', '化身与人体', 4,3,4,5,3,2,3, 'B', '',
   '延续库内 OceanChat/EcoEcho 对话海洋角色劝导研究，把对照与纵向设计推进为六条件 RCT；化身即刻效应（β=.401–.609）与两月后仅白鲸维持（β=.657）的分解有方法论价值。',
   '社交 XR 化身劝导效应研究的设计范本（预注册+ANCOVA+BH-FDR+IPW）；控制组也上升 0.568 提示测量反应性，XR 实验设计应设置中性对照。'),
 '2610.35414': ('Unveil the Mask：外观无关的化身操作者验证', '化身与人体', 3,4,4,4,3,3,4, 'B', '',
   '与 WBA2026 官方基线（ST-GCN 地标、Chapariniya 帧差视频）直接对比，属库内化身行为生物特征验证线；地标扩散掩码预训练（DiMP）适配人脸序列是新尝试。',
   '化身身份安全/操作者溯源的技术参照；Diff Gen 0.637 表明跨生成器泛化仍未解决；代码已开源。'),
 '2610.34564': ('FlockWorld：群体规模多智能体视频世界模型测试床', '世界模型与仿真', 3,4,4,3,3,2,4, 'B', '',
   '承接库内 Solaris/MIRA/Gamma-World 单/多人世界模型并扩展到人工生命群体规模；「一致性指标被渲染密度混淆」的方法论警示值得所有世界模型评测借鉴。',
   '多智能体世界模型研究的可控测试床；2D 设置与真实 3D 社会交互差距大，结论外推需谨慎；代码已开源。'),
 '2610.33868': ('RelateGS：可靠语义与关系证据的 3D 场景理解', '感知与认知', 3,3,3,3,3,3,3, 'B', '',
   '与库内 GaussianGraph/Occam\'s LGS/LangSplat/LEGaussians 同线，是 GaussianGraph 的场景侧证据精炼扩展（置信度语义提升+图引导补查询）；Sr3D+ Acc@0.25 +7.9pp。',
   '3D 视觉定位的关系证据质量问题可借鉴其「按图所缺条件化获取证据」范式（同 VLM 预算下比随机补询 +2.44/+3.66pp）；仅 8 个室内场景验证。'),
 '2610.34223': ('单相机仿真与试穿就绪的化身建模', '化身与人体', 4,3,3,2,2,4,3, 'B', '',
   '与库内 3DGS 人体/服装重建与虚拟试衣类工作同属化身建模赛道，差异在单相机输入与物理集成双层 GS-Mesh 解耦；IEEE TVCG 已接收。【PARTIAL：ar5iv 仅摘要页，按摘要级评估】',
   '虚拟试衣/单目化身重建可关注其双层解耦思想；定量结果需以 PDF 全文核实后复评。'),
 '2610.34597': ('几何一致房间去家具化的提示式编辑器微调', '内容生成', 3,3,3,3,3,2,3, 'C', '',
   '与库内 DeepDR/DimSplat 等结构感知减弱现实方法互补，定位为单图生成式 inpainting 模块；首次系统量化通用提示式编辑器在去家具化上的几何失真（Layout Error 2.03 px）。',
   'XR 减弱现实/虚拟布景管线的即插即用模块；无显式 3D 条件，多视图时序一致性无保证，5 s/张仅适合离线预处理。'),
 '2610.34745': ('SceneAgent：从 3D/4D 采集到仿真环境的智能体管线', '内容生成', 3,3,4,3,4,3,3, 'B', '',
   '与库内 real-to-sim 重建/策略评估工作同域，差异在以智能体编排协调「分割-物理参数-部件分解-铰接-可变形仿真」全链并经模拟器视觉检查修复中间错误；MessyKitchens/GraspClutter6D/4DCodeBench 三基准评估。',
   'real-to-sim 资产生产管线范本（GraspClutter6D F1@1cm 60.75% vs SimFoundry 6.9%；4DCodeBench 动态 IoU 0.86%→99.09%）；物理参数未对标实测、转换慢（反复 VLM 调用+GPU 工作站）是落地瓶颈。'),
 '2610.34865': ('ECHOES：LLM 讲解员核心的 AR 眼镜遗产解说系统', '交互与输入', 3,2,2,1,1,3,2, 'C', '',
   '与库内 AR 导览/智能眼镜助手类工作同属 LLM+AR 场景化问答路线，UbiComp Companion 演示型系统；站点锚定+可溯源 RAG+眼镜输出 schema 有工程参考价值。',
   '演示论文无定量评估，仅作系统设计参照；偏好记忆限单会话、未真实线路部署。'),
}

S_BF = {
 '2609.31418': ('CognitiveReality：机器人无关语义高斯映射与沉浸式协同 VR 遥操作', '空间计算与UI', 4,4,5,5,4,4,4, 'A',
   '总分 4.30 达 S 线（≥4.2），但当日最高分 4.35 < 库内近 30 天 Top10 均分 4.416 → 非重磅日，按校准关记 A（同 10-24 EgoHand / 10-27 WFM 先例）',
   '与库内 VRSplat/RFFR/HIL-GS（高斯 VR 遥操作）、ConceptGraphs/LangSplat/OpenGS-SLAM（开放词汇映射）及 GSMem/3DGSNav（高斯地图+VLM 探索）同域，差异在 live robot-built map+指向落地+质量感知闭环；多平台 PSNR +2–8 dB。',
   'VR 遥操作+语义地图+LLM 智能体的完整闭环参考实现；四平台（四足/UR10/人形/无人机）实机验证；确认门不重校验的局限需在部署时注意。'),
 '2609.02847': ('RoGe：端到端隐式重建与生成的新视角合成', '神经渲染', 4,5,4,4,5,3,4, 'A',
   '总分 4.27 达 S 线（≥4.2），但当日最高分 4.35 < 库内近 30 天 Top10 均分 4.416 → 非重磅日，按校准关记 A（同 10-24 EgoHand / 10-27 WFM 先例）',
   '承接库内 LagerNVS（VGGT token 直接渲染）与 SEVA/FrameCrafter（生成式 NVS），与 GEN3C/NeoVerse/Difix3D+ 等解耦两阶段混合方法直接对比；ray-scene 交叉注意力+端到端联训是差异化内核。',
   '稀疏位姿 NVS 新 SOTA（FVD 58 vs LagerNVS 206/GEN3C 281）；「无显式 3D 中间表示的射线查询条件化」思路可迁移；16×H20 训练成本高。'),
 '2602.13444': ('FlowHOI：语义接地的手物交互流匹配生成', '内容生成', 4,4,4,5,5,4,3, 'A',
   '总分 4.23 达 S 线（≥4.2），但当日最高分 4.35 < 库内近 30 天 Top10 均分 4.416 → 非重磅日，按校准关记 A（同 10-24 EgoHand / 10-27 WFM 先例）',
   '承接库内 DiffH2O/LatentHOI 的 HOI 生成路线并以流匹配替代扩散；EgoDex 第一视角视频重建 HOI 数据管线与库内第一视角数据工作呼应；混合 3D 场景 token（3DGS 质心+Concerto/SceneSplat）是跨方向结合点。',
   '灵巧操作 HOI 生成首选基线（仿真 SR 55.96% vs 28.44%，推理快 40×）；纯运动学轨迹需物理精化，在线扰动应对是开放问题。'),
 '2605.30488': ('CoMo3R-SLAM：学习式 3D 重建先验的协同单目稠密 SLAM', '重建与SLAM', 3,4,4,4,4,3,4, 'A', '',
   '与库内 MASt3R-SLAM/VGGT-SLAM（单智能体先验 SLAM）及 MAGiC-SLAM/MNE-SLAM/CP-SLAM（RGB-D 协作稠密 SLAM）同表对比，属单目室外多智能体稠密 SLAM 的稀疏工作；点图锚定跨智能体尺度是核心思想。',
   '多机器人协作建图可复用其「稠密对应双向验证+统一 Sim(3) 图」；无深度传感器是部署亮点；集中式计算未测终端延迟。'),
 '2605.31352': ('Haptic Sorter：触觉探索与可微操作势统一的在线形状估计与分拣', '触觉与多模态', 4,4,4,4,4,4,3, 'A', '',
   '与库内 Tactile-SLAM/GelSlam/cost-aware 主动触觉探索/Superquadric Recovery 等单点累积式触觉建图对照，主打同时多接触+探索-建模-控制同参数化；补齐库内触觉「建模-感知-控制」链条。',
   '接触富集操作（未知形状）的可微框架范本；约 300 Hz 闭环纠偏；仅限凸形 2D 交互与准静态假设，闭环对形状精度高度敏感（点云参数反劣于开环）是重要警示。'),
 '2604.07279': ('Mem3R：混合记忆的流式 3D 重建', '重建与SLAM', 4,4,4,4,4,3,4, 'A', '',
   '直接建立在库内 CUT3R/TTT3R/TTSA3R 之上，与 Spann3R/Point3R/StreamVGGT 流式重建及 LaCT 快权重记忆文献对应；参数 -19% 而长序列更优，证明增益来自记忆表示而非容量。',
   '长序列流式重建（≥400–500 帧）的首选记忆架构；通道门控兼容 TTT3R 即插即用；重训练成本高（32×H100）。'),
 '2603.28064': ('4DSurf：SDF 流正则的动态场景表面重建', '重建与SLAM', 4,4,4,4,5,3,3, 'A', '',
   '与库内 Neural SDF-Flow/ST-2DGS/Dynamic-2DGS/GauSTAR 等动态表面方法同线；高斯速度场+SDF 流正则+重叠分段增量+IMT（LoRA）形成组合差异；Hi4D CD 较次优低逾 49%。',
   '大变形长序列动态表面重建优先基线；时序稳定性 STD 0.18 为最佳；遮挡/稀疏视图下 SDF 近似粗糙，未在真实非受控数据验证。'),
 '2605.18553': ('StableHand：质量感知的世界空间双手运动估计', '化身与人体', 4,4,4,5,4,3,3, 'A', '',
   '与库内 HaMeR/WiLoR+DROID-SLAM/HaWoR/Dyn-HaMR/UniHand 第一人称手部恢复工作同任务对比，是质量条件化生成式双手运动估计的新一支；H2O 零训练迁移 56.77 mm/30.62 s（Dyn-HaMR 60.88/323.89）。',
   '第一人称双手估计（XR 具身输入）强基线；四通道质量信号统一驱动四机制的设计可迁移到其他缺失观测生成任务；换估计器需重训练才有效。'),
 '2606.01950': ('MRO-GWM：物体中心高斯世界模型的刚体动力学预测', '世界模型与仿真', 3,4,4,4,4,3,3, 'A', '',
   '与库内 PIN-WM/ContactGaussian-WM（可微物理+高斯，单物体）、3DGSim（高斯形变 Transformer）、NGFF（物体中心力场）及 NeRF 世界模型构成谱系；差异在多物体动作条件刚体预测与部分观测。',
   '桌面操作世界模型的统一表示（动力学预测+渲染跟踪+MPC 规划）；MPC 0.79 vs 启发式 0.14 证明可规划性；旋转误差较大（滚动/倾覆），sim2real 域随机化未做。'),
 '2601.00913': ('CleanGS：帕累托视图选择的免训练 3DGS 场景清理', '神经渲染', 3,3,4,4,4,3,4, 'B', '',
   '与库内 FlashSplat/GaussianCut/Lifting by Gaussians 等掩码提升与 3DGS 压缩工作同线，差异在先选证据再过滤（Pareto 视图选择+光栅化感知多视图投票）与保留资产直接评估；6× 扩视协议值得复用。',
   '3DGS 资产生成管线的免训练清理步骤（快 9–13×、省内存 18–22×）；跨视图一致相邻表面仍可幸存，固定扩视不暴露永久遮挡 clutter。'),
}

def val(s):
    return round(0.20*s[0]+0.20*s[1]+0.15*s[2]+0.15*s[3]+0.15*s[4]+0.08*s[5]+0.07*s[6], 4)

# SceneAgent（2610.34745）未分配子代理 digest，按主会话全文阅读补录
D['2610.34745'] = dict(id='2610.34745', slug='sceneagent', venue='arXiv preprint（Harvard University Computational Robotics Group, SEAS）',
  tags=['real-to-sim','智能体管线','3DGS','4D 视频','仿真环境生成','策略学习'],
  conclusion='以智能体编排经模拟器视觉检查与修复把 3DGS/摄影测量/LiDAR/AI 生成 3DGS/4D 视频转为可交互仿真环境：GraspClutter6D 杂乱箱 F1@1cm 最佳 60.75%（SimFoundry 6.9%），4DCodeBench 动态 IoU 0.86%→99.09%。',
  problem='视觉采集转为交互仿真环境需要物体重建、物理建模与中间错误纠正，现有 real-to-sim 管线（如 SimFoundry）在杂乱遮挡场景重建质量低，且生成策略评估环境缺乏物理/铰接/可变形建模与演示数据。',
  method='智能体编排：输入准备与场景表示（3DGS/摄影测量/LiDAR/AI 生成 3DGS/4D 视频）→ 物体分割与背景补全 → 物理属性（质量/摩擦/刚性）估计、部件分解、铰接与断裂仿真 → 3D 到 4D（动态场景）→ 场景导出与编辑 → 数字孪生与「digital sisters」变体 + 脚本演示生成（策略自动研究循环、初始状态随机化、专家与回合过滤、策略微调）。全链经模拟器视觉检查发现几何不一致并修复。',
  experiments='MessyKitchens 厨房场景 + GraspClutter6D scene hard/000091（20 个 YCB 物体堆叠遮挡、13 视图 1920×1080）：多种 coding agent harness 带/不带 SceneAgent skills 配对转换，按 Chamfer 距离报告 CD 与 F1@τ；所有 agent 配置超 SimFoundry（最佳 60.75% vs 6.9%）。4DCodeBench 三个动态场景：Gemini 4 Argon 平均动态 IoU 0.86%→99.09%。附定性场景/物体转换与初步真机策略迁移。',
  innovation='①把 real-to-sim 转换组织为「智能体编排+模拟器视觉检查修复」闭环；②统一处理 3D 与 4D（动态）采集输入；③生成多样化物体变体（digital sisters）与脚本演示直接服务策略学习。',
  limits='转换需反复 VLM 调用与外部 GPU 工作站，慢且易错；视觉检查无法建立隐藏几何/物理参数精度；质量/摩擦/刚性/铰接参数未对标实测机器人交互；高斯保留原光照，重光照与合成可出现阴影不一致；评估仅一个厨房+一个杂乱箱+三个动态场景，每配置仅转换一次。',
  repro='项目页 https://computationalrobotics.seas.harvard.edu/SceneAgent/ ；代码与数据发布情况摘要级未明示。',
  relation_hint='real-to-sim 重建/策略评估线，与 SimFoundry 同基准对比。', track_hint='内容生成')

MAIN, BF = [], []
for pid, (tzh, track, imp, nov, tec, exp, per, trl, rep, grade, note, rel, act) in S_MAIN.items():
    d = D[pid]
    MAIN.append(dict(id=pid, title=d['title'] if 'title' in d else '', title_zh=tzh, track=track,
        scores=dict(IMP=imp,NOV=nov,TEC=tec,EXP=exp,PER=per,TRL=trl,REP=rep), grade=grade,
        grade_note=note, evidence=d.get('evidence','FULL'), level=('L1' if pid=='2610.34223' else 'L0'),
        status='CURRENT', venue=d['venue'], announce='new', tags=d['tags'],
        conclusion=d['conclusion'], problem=d['problem'], method=d['method'], experiments=d['experiments'],
        innovation=d['innovation'], limits=d['limits'], relation=rel, repro=d['repro'], action=act,
        value=val((imp,nov,tec,exp,per,trl,rep)), batch='2026-10-28'))
for pid, (tzh, track, imp, nov, tec, exp, per, trl, rep, grade, note, rel, act) in S_BF.items():
    d = D[pid]
    BF.append(dict(id=pid, title='', title_zh=tzh, track=track,
        scores=dict(IMP=imp,NOV=nov,TEC=tec,EXP=exp,PER=per,TRL=trl,REP=rep), grade=grade,
        grade_note=note, evidence=d.get('evidence','FULL'), level='L0',
        status='CURRENT', venue=d['venue'], announce='replace/cross', tags=d['tags'],
        conclusion=d['conclusion'], problem=d['problem'], method=d['method'], experiments=d['experiments'],
        innovation=d['innovation'], limits=d['limits'], relation=rel, repro=d['repro'], action=act,
        value=val((imp,nov,tec,exp,per,trl,rep)), batch='backfill-1028',
        orig_window='2026-01/02/03/04/05/06/09 投稿，2026-10-27 公告批次 RSS 混入旧稿 replace/cross 再公告（首次入馆）'))

# 从 candidates_1028.json 补 title（原始英文标题）
cands = json.load(open('data/candidates_1028.json', encoding='utf-8'))
tmap = {c['id']: c['title'] for g in ('main','backfill') for c in cands[g]}
for p in MAIN + BF:
    p['title'] = tmap.get(p['id'], p['title'])

MAIN.sort(key=lambda p: (-p['value'], -p['scores']['IMP'], -p['scores']['NOV'], p['id']))
BF.sort(key=lambda p: (-p['value'], -p['scores']['IMP'], -p['scores']['NOV'], p['id']))
json.dump({'main': MAIN, 'backfill': BF}, open('data/scored_1028.json','w',encoding='utf-8'), ensure_ascii=False, indent=1)
print('main:', len(MAIN), 'bf:', len(BF))
for p in MAIN: print('M', p['id'], p['value'], p['grade'], p['track'], p['title_zh'][:30])
for p in BF: print('B', p['id'], p['value'], p['grade'], p['track'], p['title_zh'][:30])
print('saved data/scored_1028.json')
