# -*- coding: utf-8 -*-
"""组装 2026-10-29 评分数据：digest（子代理全文精读）+ 主会话 7 维评分定稿。
输出 data/scored_1029.json（main 20 + backfill 4）。内联中文文本统一中文弯引号。
候选池：10-28 公告批次 19 篇 + ParetoGS 补录（10-27 公告批次，上批候选→评分环节静默丢失，今日 listing 对账重新发现）。"""
import json

D = {}
for g in ('g1', 'g2', 'g3', 'g4'):
    for d in json.load(open(f'data/digest_1029_{g}.json', encoding='utf-8')):
        D[d['id']] = d

# 2610.34235 ParetoGS：复用上批（10-28 运行）已完成的 digest（同一篇全文，未重跑子代理避免重复计费）
for d in json.load(open('data/digest_1028_g1.json', encoding='utf-8')):
    if d['id'] == '2610.34235':
        D['2610.34235'] = d

# 2610.36014 Immersive Commons：L1 ar5iv 仅摘要页（4,706 字符），按摘要级 digest（主会话补录）
D['2610.36014'] = dict(id='2610.36014', slug='immersive-commons',
  venue='SIGraDi 2026（Iberoamerican Society of Digital Graphics；Wuwu Ran, Mohammed Faraj Al-Suwaidi）',
  tags=['共址MR','空间对话','设计框架','Research through Design','社会临场感'],
  conclusion='Immersive Commons 设计框架 + Atmos Messages 原型（手势即时空间消息+语音转写+预设文本+公共平面图总览）：15 名参与者两场次创建 236 条消息（48 条语音），问卷凸显游戏性与社会感知，交互聚集于公共显示屏附近。【摘要级：ar5iv 仅摘要页，定量细节未在正文核实】',
  problem='头显 MR 常优先个体沉浸，把注意力从同室他人处拉走；戴头显者与非戴头显者的共址交流缺乏支持。',
  method='Research through Design：提出 Immersive Commons 设计框架；实现 Atmos Messages 原型，结合基于手势的短暂（ephemeral）空间消息、语音转写、预设文本与对非头显观察者可见的公共楼层平面总览。',
  experiments='15 名参与者、两个场次、共 236 条消息（含 48 条语音撰写）；问卷 + 观察分析；交互聚集于公共显示屏（也是参与者戴头显的位置）。',
  innovation='①面向共址 MR 空间对话的设计框架；②短暂空间消息+公共总览原型；③以 RtD 方法获得游戏性与社会感知的定性证据。',
  limits='摘要级评估（L1 仅摘要页）：小样本定性研究；交互聚集于公共显示屏与戴头显位置混杂；缺乏定量比较与长期部署数据。',
  relation='属库内共址 MR/社会临场感一脉（化身可见性、共享空间 UI），差异在以短暂空间消息+公共总览支持戴头显者与非戴头显者交流。',
  repro='正文未述（摘要级无法核实代码/数据发布）。')

# 评分表：id -> (title_zh, track, IMP,NOV,TEC,EXP,PER,TRL,REP, grade, grade_note, relation, action)
S_MAIN = {
 '2610.37602': ('RESPLE2：惯性知情的非均匀 B 样条递归多传感器里程计', '重建与SLAM', 4,4,5,5,4,4,4, 'A',
   '总分 4.30 达 S 线（≥4.2），但当日最高分 4.30 < 库内近 30 天 Top10 均分 4.417（现算，435 条入窗）→ 非重磅日，按校准关记 A（同 10-24 EgoHand / 10-27 WFM / 10-28 RacerGS 先例）',
   '延续库内连续时间估计线（B 样条/IEKF 里程计）与多传感融合谱系（TLEIO 事件惯性 / HexVIO 立体惯性）；首个非均匀 B 样条递归框架，借 knot-clamping 边界性质实现控制点的精确 IMU 积分预测是核心差异，反钳制 RCP reset 保持节点扩展时的轨迹局部一致性。',
   '多平台（手持/履带/腿式/腿式四旋翼）实时里程计的强基线：JEPLO 8/8 序列 APE 最低、HOPPER 在 ±4 g IMU 饱和与约 25 g 峰值加速度下仍几乎全部最低；惯性知情预测降 APE 39%–76% 且每帧仅占预算 10.6%–18.3%。关注无 LiDAR 深度时的视觉特征约束（作者未来工作）与传感器退化鲁棒性。'),
 '2610.37036': ('GraftRay：路径追踪的物理一致网格插入高斯场景', '内容生成', 4,5,4,4,5,3,3, 'A',
   '总分 4.20 达 S 线（≥4.2），非重磅日按校准关记 A（同 10-24 EgoHand / 10-27 WFM / 10-28 RacerGS 先例）',
   '与库内高斯场景物体插入（IRGS/EAG-PT 一脉）及 inverse rendering 环境光估计同域；差异在扩展 OptiX 路径追踪器联合追踪随机透明高斯与插入 mesh（3σ AABB+峰响应求交），并把饱和像素视为删失观测、以路径追踪单位辐射度基图+非负最小二乘估计发射器强度，免传统联合优化。',
   'AR 虚拟物体插入/阴影合成的首选基线（FIPT ΔPSNR 35.17 vs IRGS 28.40、阴影 IoU 0.76 vs 0.50、每帧 1.6 min 较 EAG-PT 约 12×）；光源需手动 SAM 标记、依赖 2D 材质/法线先验是落地门槛；实时化（当前离线内容生产）是后续方向。'),
 '2610.36853': ('LingGS：几何预测与相机跟踪解耦的高保真高斯 SLAM', '重建与SLAM', 4,4,4,5,5,3,3, 'A', '',
   '位于库内单目高斯 SLAM 线（MonoGS/S3PO-GS/Photo-SLAM/OTF）与冻结流式 3D 基础模型（DUSt3R/VGGT/CUT3R/TTT3R 一脉）之间；把冻结流式模型当虚拟 RGB-D 传感器、以直接深度残差+恒定相对不确定度（ε=0.05）的显式几何求解器取代学习相机头，附录从理论上证明虚拟立体对深度误差的 z⁻⁴ 敏感性并给出更自然的 z⁻² 权重。',
   '单目高斯 SLAM 新参照：4 数据集渲染 PSNR 全部最高（最高 +3.1 dB）、ATE 较相机头最高降 87.6%（跨 4 骨干降 31.0–96.7%）、单卡 4090 约 7 FPS；无回环、不处理动态场景、依赖 ORB 特征（弱/重复纹理受限）是部署缺口。'),
 '2610.35902': ('StereoSplat：立体接地的度量尺度前馈 3DGS', '神经渲染', 4,4,4,4,5,3,4, 'A', '',
   '属库内前馈 3DGS 线（pixelSplat/MVSplat/AnySplat/DepthSplat/NoPoSplat），首个原生面向立体视频设计的前馈框架；FoundationStereo 立体先验当几何锚，XRStereo 数据集（137k 帧、多种 rig 配置）填补合成立体视频空白。',
   '立体/XR 双摄采集的度量尺度 NVS 首选：KITTI AbsRel 0.04 / δ₁ 96.0%（DepthSplat 0.13/79.8%），819k→132k primitive（6.2×）且 236.9 FPS 最快；依赖已标定立体对与静态场景假设，未标定/单目采集与动态场景是开放方向。'),
 '2610.36876': ('HoloRecon：前馈几何验证的长程全景一致重建', '重建与SLAM', 4,4,4,5,4,3,4, 'A', '',
   '与库内全景 SLAM/SfM（PanoVGGT/Scal3R/360DVO/COLMAP-ERP/Spherical-SfM）及前馈几何（Pi3/VGGT 一脉）同域；差异在以前馈局部几何对跨视角 ORB 匹配做 3D 验证（含分组交叉验证抗重复纹理）建立长程 Sim(3) 约束，并提出稀疏建图与前馈几何相互依赖的耦合范式；发布 PanoRecon 基准（RTK LiDAR 参考位姿）。',
   '长序列 360 内容生产管线的全局一致性方案：三数据集最低平均 ATE（0.270/3.527/1.697 m）与最高 20 cm F-score，GPU 全景 BA 较 CPU 4.31×；运动模糊/低纹理与动态物体未处理，Sequence C 总计 181 min 未达实时。'),
 '2610.37172': ('DomeGS：无界 3DGS 的感知一致背景补全（VR）', '渲染与显示', 4,4,4,5,4,3,3, 'A', '',
   '针对库内无界 3DGS 重建的地平线不完整问题（破坏 VR 沉浸），把传统 VR skybox/skydome 思想落到高斯表示内部：远景为统一 3DGS 资产中有限半径球壳上的背景高斯，头部平移时提供深度一致运动视差；360° 感知生成外扩+wrap-seam 调和+角色相关 alpha 监督实现无缝补全。',
   'VR 无界场景内容生产即用方案：N=36 用户研究 SKY +1.24（p<0.001, d=0.85）、IMM +0.44（p<0.001）、IPQ 空间临场感 1.73 vs 1.41、75.0% 偏好且无眩晕/负荷代价；Tower 场景不显著（skybox 已高分）、Close 场景偏好未达显著（p=0.0522），补全质量依赖生成模型。'),
 '2610.36760': ('GeoGSplat：几何接地的非像素对齐高斯泼溅', '神经渲染', 4,4,4,4,5,3,3, 'A', '',
   '属库内前馈 3DGS 线非像素对齐一支（AnySplat/TokenGS/MVSplat/NoPoSplat）；以固定 65,536 高斯预算+Anchor（粗结构约束）与 Triplane（细粒度可查询特征）双分支互补表征，Anchor-to-Point→Point-to-Gaussian 两级分层解码，对称 Chamfer 几何监督贯穿始终。',
   '前馈 3DGS 新对比基线：DTU PSNR 20.48 dB（较 TokenGS +2.77）、CD 0.018（较 0.082 降 78%）、NRGBD 24.78 dB，且离输入视角越远优势越大；训练成本高（128×L20、320K 迭代）、依赖 GT 深度监督、室外/大规模未充分验证、未报推理速度。'),
 '2610.36168': ('PrinGS：高斯泼溅的后训练隐私保护', '渲染与显示', 4,4,4,4,4,3,4, 'A', '',
   '库内首个 3DGS 隐私工作：给定训练后 splat 与用户参考视图，定位敏感区域并直接在 3D 表征上匿名化，无需原始训练图像与重训练；配套 privacy-by-design 训练策略（多视图分割+loss 掩码+周期性干预）防止敏感特征在训练期被编码，并构建首个 3DGS 人脸隐私基准 PrinGS-Humans。',
   '3DGS 资产分享/部署前的隐私审计与匿名化工具：FSM 83.87%→9.79%（-74.08%）且保留 FDR 39.47%、OCR-CER 1.00、匿名化 <1 s；FDR 表明匿名化后人脸仍可被检测为脸（身份嵌入不可再匹配）；后训练设置缺 GT 图像、深度纠缠场景的回顾性修改可能留有痕迹。'),
 '2610.34235': ('ParetoGS：稀疏适配锚点的连续预算高质量 3DGS', '渲染与显示', 4,4,4,4,4,3,3, 'A',
   '【补录】2610.34235 属 2026-10-27 公告批次：10-28 运行曾入候选池并完成 digest，但候选→评分环节静默丢失未入馆；10-29 listing 对账重新发现，补入本批评分池，诚实标注非 10-28 公告批次新提交。',
   '属库内 3DGS 压缩/预算线（Scaffold-GS→HAC→ContextGS/Budgeted-GS/RLSplat/RacerGS 一脉）：把连续预算表示为嵌套成员轨迹与预算特化参数状态的联合轨迹，GNS 收缩构建 11 个严格嵌套锚点（0.1%→100%），分层残差图集（成员层×参数域正交分解、高阶 SH 低秩、INT8 块量化）+分段插值/门控解码任意整数预算。',
   '可缩放 3DGS 资产服务（一资产多预算）首选：10% 保留率 27.17 dB 超 CLOD-3DGS 25.59/303K、MGS 25.74/492K（162K 高斯），附加状态 390.0→85.7 MB（-78.0%）质量几乎不变，离线构建 10.3 min（CLOD-3DGS 约 35、MGS 约 74）；锚点过稀疏时连接质量下降（Garden SSIM 0.6569→0.6180）、解码需 GPU 驻留相邻锚点、区间校准仅用 ≤10 训练视图。'),
 '2610.36384': ('SOMA：第一视角细粒度人体运动理解基准', '评估与数据集', 4,3,4,5,3,3,5, 'A', '',
   '区别于库内 Ego4D/EgoPlan/InteractiveWorld 等第一视角基准（对象/场景/粗动作），首个面向身体本身的细粒度感知基准（12 任务/3 能力轴）；数据构造含盲语言过滤（剔除 45.9% 语言可猜题）与视频+同步 3D 身体姿态渲染辅助人工审核；配套 SOMA-Train（28,596 QA、110.2 小时三模态对齐）。',
   '可穿戴助手/XR 感知研发的必用评测台：人类 68.5% vs 最强 Qwen3.6-27B 50.0%，Repetition Counting 差 45.3 分；首次量化右手偏置（78.8% vs 44.3%）与系统性少数偏差（24/37 模型）——模型选择的重要警示；精确计数依赖人工标注规模受限，SOMA-Train 生成未经人工验证。'),
 '2610.36312': ('SG²SLAM：空间几何信息的单目户外 3DGS SLAM', '重建与SLAM', 4,4,4,5,4,3,3, 'A', '',
   '属库内单目 3DGS SLAM 线（MonoGS/S3PO-GS/Photo-SLAM/OTF 及同批 LingGS）：以 chunk 级流式空间几何先验（poses+point maps+confidence 单源监督）取代逐帧 2D 像素-3D 点跨维关联，射线条件 3DGS 核（均值/协方差跨越空间块与视方向子空间、闭式 Schur 补条件化）消除掠射角混合与浮动 primitive，chunk 间 Sim(3) 全局联合图优化一次性结算尺度漂移。',
   '户外单目 3DGS SLAM 强基线：KITTI 11 序列平均 ATE RMSE 6.24 m、Waymo 9 序列 0.63 m、KITTI 渲染 22.70 dB/0.86/0.41，多序列追踪大幅超 MonoGS/S3PO-GS/DiskChunGS/GigaSLAM；chunk 大小敏感（300/500 帧明显差于 200）、深度失效区（天空/远场）显式排除、部分序列（03/04）ATE 略逊。'),
 '2610.37271': ('HILMARTS：移动 AR 胸腔手术虚拟模型-患者配准', '空间计算与UI', 4,3,4,4,4,4,3, 'A', '',
   '属库内 AR 手术导航/医疗 AR 一脉：device-coupled 手动粗对齐交互（虚拟模型镜像平板 6-DoF 运动，免除外设跟踪）+商用 iPad LiDAR+BlazePose 语义隔离躯干的免标记点云精配准（量程/统计/双边滤波+语义 mask+DBSCAN），占据栅格 Surface Coverage Score 实时反馈采集几何完整性（70% 阈值触发注册）。',
   'AR 手术导航低成本落地参照：16 人 phantom 研究 mTRE 3.31±1.26 mm（手动粗对齐 12.82±15.40 mm，p=0.0052）、约 4 min 完成、SUS 84.06；CT 仰卧采集 vs 侧卧体位的软组织形变未建模、顺序效应存疑、被试以 STEM 学生为主（仅 1 名临床医生）是临床推广前需解决的问题。'),
 '2610.36462': ('ClusterSplat：3DGS 视觉定位的语义簇选择', '感知与认知', 3,4,4,4,4,3,3, 'A', '',
   '属库内 3DGS 开放词汇定位线（LangSplat/OpenGaussian/ReferSplat/Dr.Splat 及 GaussianGraph 关系推理）：把 3D 目标选择从 primitive 级分数过滤重构为场景自适应候选簇上的离散选择，MDL（描述长度）+BIC 式惩罚指导聚类（簇数 53–143），query-conditioned cluster scoring（自注意力场景上下文+CLIP query 交叉注意力+余弦 token attention），彻底免除逐查询/逐场景阈值。',
   '3DGS 场景指代定位新 SOTA：ScanRefer 2D mIoU 39.72% / 3D mIoU 23.33%（ReferSplat 31.30/4.05）、每查询 19.55 ms；候选池过合并邻近相似物体或拆分物体会限制保守 Top-1 完整性（类名 mAcc 46.60% 强而 3D mIoU 29.21% 更严格）；仅处理单物体表达，复数/可变数量实例留待未来。'),
 '2610.37149': ('GCSR-OCC：几何校准与语义路由的开放词汇占用预测', '感知与认知', 3,4,4,4,4,3,3, 'A', '',
   '属库内占用预测谱系（LegoOcc/EmbodiedOcc/GaussianFormer2/PGOcc/GaussTR 及前批 LegoOcc++）：EC-G2O（核质量归一化+p 范数聚合+可学习增益）在不破坏与渲染共享 α_i 的前提下抑制高斯尺度膨胀与局部证据过累积；MM-QGSR 多模式 query-first 高斯语义路由在体素聚合前分配语言证据，缓解跨/高斯内语义混合。',
   '开放词汇室内占用强基线：Occ-ScanNet 几何 IoU 63.31%（超全部闭词汇几何方法）、mIoU 27.44%（超 LegoOcc +6.39），聚合 Gaussian-voxel 对 -51.3%、几何聚合延迟 -34.8%；p 范数适度压制也削弱细粒度语义响应（mIoU 22.82→22.64），mIoU 仍略低于全监督 ISO（28.71）。'),
 '2610.36592': ('LabWorld：交互式 4D 实验室世界学习', '世界模型与仿真', 4,4,4,3,3,3,3, 'B', '',
   '与库内 Real2Sim/交互式环境重建（SceneAgent/SimFoundry 一线）及 4D 重建工作同域；事件条件重建把流程事件的时空要求作为运动重建约束，约束视觉合理但物理不一致的解；统一输出可复用资产、度量场景、时变物体状态与流程事件。',
   '实验自动化/科学智能体的 Real2Sim 参照：移液 Mask IoU 0.501（最强基线 0.468）、涡旋 PCK-AUC 0.638（0.603）、物理约束满足率 5/35→35/35；2D 指标与物理有效性可背离的诊断（去掉事件约束 IoU 反升而约束满足崩坏）值得借鉴；自采 20 段视频规模小，细功能几何/透明度/材质/精确物理尺寸仍缺，单目度量对薄/反光工具不确定。'),
 '2610.36658': ('SAGE：语义增强几何专家的点云配准', '重建与SLAM', 3,4,4,4,3,3,3, 'B', '',
   '属库内低重叠点云配准线（GeoTransformer/RoITr 一脉）：SG-MoE 把路由信号与专家输入解耦——路由只用冻结 Sonata 语义特征、专家处理语义-几何特征，避免注册损失把融合特征塌缩为纯几何模式；跨场景专家专业化（沙发/床/台面路由到同一专家）无显式监督自发涌现。',
   '低重叠配准新基线：3DLoMatch 单遍 RR 76.3%（超 GeoTransformer 2.3 点）、相同 6 次迭代预算下两基准最高 IR/RR、KITTI 平移误差最低 6.1 cm；依赖冻结 Sonata 质量与泛化（50% 随机替换时 RR 76.3%→73.5%），工业/医疗器械等分布外类别可能误导路由，语义同质场景收益有限（MIT Lab 81.2% 低于 GeoTransformer 83.9%）。'),
 '2610.36014': ('Immersive Commons：共址 MR 的短暂空间对话设计', '空间计算与UI', 4,3,3,4,2,2,3, 'B',
   '证据等级 PARTIAL：L1 ar5iv 仅摘要页（4,706 字符），按摘要级评估并显式声明，定量细节未在正文核实',
   '属库内共址 MR/社会临场感一脉（化身可见性、共享空间 UI），差异在以短暂空间消息+公共楼层平面总览支持戴头显者与非戴头显者的交流；Atmos Messages 组合手势消息、语音转写与预设文本。',
   '社交 MR 设计范本（SIGraDi 2026）：游戏性与社会感知的定性证据；小样本（15 人）定性研究、交互聚集于公共显示屏与戴头显位置混杂、缺定量比较与长期部署数据——结论外推需谨慎。'),
 '2610.36610': ('4D Reconstruction with Events & RGB（事件-RGB 融合的 4D 重建）', '神经渲染', 3,3,3,4,2,3,3, 'B', '',
   '在库内前馈 4D 重建（MonST3R 一脉）上做最小事件融合扩展（8→3 通道卷积 adapter+事件体素输入）；证明 RGB（空间信息）与事件（运动线索）互补：融合优于 RGB-only、事件转 RGB 翻译（HyperE2VID）与事件-only 三种变体；与库内事件相机里程计（DEVO/TLEIO）共享事件-运动互补思想。',
   '事件+RGB 4D 重建的概念验证（NeVi 2026 @ ECCV）：三基准平均 Abs Rel -3.4%、高物体运动下 Log RMSE 额外 -0.327，最大增益区间定位在高物体运动；事件由 V2E 模拟（无真实事件相机验证）、融合仅为拼接（未建模 RGB 同步/事件异步差异）、基于 MonST3R 非最强骨干、仅 4 数据集——作者自述 preliminary study，定位为初步证据。'),
 '2610.37427': ('TSAE：协同 VR 沟通同步的时动态语义-活动纠缠', '感知与认知', 3,3,3,3,2,2,3, 'C', '',
   '延续库内社交 VR/团队行为分析脉络，把 Gloor et al.（2022）的 entanglement 适配 VR 无向自由对话：相对发言活动+上下文语义对齐（余弦+欧氏衰减）组成二元时变纠缠，late-chunking 长上下文嵌入表示短话语，Gini 系数把团队级同步刻画为分布问题。',
   '协同 VR 团队沟通的描述性度量工具：15 个德语会话（每队 5–8 人、约 25 min）session 级 Gini 0.139–0.355，前 20%/40%/60% 参与者占约 31%/54%/74%，与 core–periphery 模式形成定性对比；德语数据集与人口统计缺失限制泛化，TSAE 不建立主观团队 flow 或协作质量，时间窗口选择显著影响结论。'),
 '2610.36674': ('超越一维 RV 连续谱：七种 XR 范式的二维框架', '空间计算与UI', 3,3,2,1,1,2,3, 'C', '',
   '对 Milgram RV 连续谱的概念扩展（India HCI 2026）：以信息增减为第二维度，把 VR/AR/MR/AV/PR/AnR/DR 七范式统一置入二维平面，并给出纵轴压平回到一维连续谱的映射操作。',
   'XR 分类学的概念参照：为 AR 与 DR 等在一维谱上位置相近但信息操作相反的范式提供可区分表述；无任何定量验证（作者自述需问卷与用户研究），分析基于作者个人经验的定性判断，地震场景概念展示的外推需谨慎。'),
}

S_BF = {
 '2510.01767': ('LoBE-GS：负载均衡的高效大规模 3DGS 训练', '系统与平台', 4,3,4,4,4,4,3, 'A', '',
   '属库内大规模 3DGS 训练线（CityGS/VastGS/Grendel-GS/InfiniGS 一脉）：负载均衡 KD 树划分（相机数为工作量代理+minimax cutline refinement）从划分阶段主动均衡块负载，深度反投影式快速相机选择把预处理从 M×N 次投影降为每相机一次深度合成，可见性裁剪+选择性致密化降低每块优化高斯数与峰值显存；建立 T_E2E=T_coarse+T_partition+max T_fine 标准化计时协议。',
   '城市级 3DGS 生产管线的训练加速方案：MatrixCity-Aerial 端到端 1:13 vs CityGS 3:31（约 2.9×）、划分时间小时级→分钟级、峰值显存 22.1→16.7 GB，PSNR/SSIM 持平或更优且 fine 阶段零通信不依赖 NVLink；GPU 数远少于块数时须多轮细训，仅 5 场景验证，LoD/2DGS 表示与其他划分策略留待未来。'),
 '2604.23018': ('AmaraSpatial-10K：空间计算与具身 AI 的 3D 资产数据集', '评估与数据集', 3,3,4,4,4,4,5, 'A', '',
   '填补 ShapeNet/Objaverse/GSO/ABO/HSSD 均未联合覆盖的属性组合（度量缩放+语义锚定+PBR+碰撞包壳+配对参考图+多句描述）；提出可复用的 3D 资产库评测套件（SPS、intra-category CV、anchor error、跨模态 CLIP coherence、LLM Concept Density）并在 5 个数据集上建立基线，以 Objaverse Matched 受控对比证明 authored alignment 优于 post-hoc filtering。',
   '空间计算/具身 AI 的即用资产库：10,071 个资产，CLIP Recall@5 较 Objaverse 3.4×（0.612 vs 0.181、中位排名 267→3）、Habitat-Sim 跌落测试物理稳定 99.1% 且墙钟快约 20×，作为 Holodeck 资产包实现零重叠满接触场景；程序生成资产较摄影测量资源有几何/材质精度系统偏差，476 子类中 23 个仅 1 资产，PBR 仅 Normal+Roughness，度量尺寸为 LLM 估计。'),
 '2605.31466': ('VolFill：体素流匹配的单图 amodal 场景重建', '重建与SLAM', 3,4,4,4,4,3,3, 'A', '',
   '属库内 amodal/完整场景重建线（LaRI/NOVA3R/MoGe2 一脉）：首次将体素流匹配生成框架用于场景级 amodal 重建，TUDF 结构化表征支持阈值直接提点云与经 MeshUDF 抽网格；混合稀疏-稠密 3D VAE 实现 16× 空间压缩（occupancy 引导 dense-to-sparse 解码，1.7 GB vs dense-only 9.2 GB），几何基础模型双条件（全局 MoGe2 token+可见几何 latent inpainting，加性零初始化融合优于拼接），无符号 TUDF 规避室内非水密几何歧义。',
   '单图完整场景重建新 SOTA：SCRREAM 完整场景 CD 3.03、FS_0.02 54.83（LaRI 5.19/30.85、NOVA3R 3.43/45.12）、遮挡区 CD 3.46 亦最优，RTX 4090 推理 1.4 s/图、峰值显存 3.0 GB；重遮挡区域偶尔残留小孔、可见面因联合生成略钝（可用 training-free visible reinstatement 缓解）、仅限室内（KITTI 街景与 Sintel 失败）、256³ 固定网格需重训 VAE 与 DiT。'),
 '2508.04236': ('PIS3R：深度 3D 重建的超大视差图像拼接', '重建与SLAM', 3,4,4,4,4,3,2, 'B', '',
   '区别于库内 warping/seam-cutting 拼接线（UDIS++/APAP/ELA/OBJ-GSP），首个把前馈深度 3D 重建（VGGT）引入超大视差（VLP）拼接：视觉几何 grounded transformer 深度估计+点云重投影+点条件 RDDM 扩散精炼，拼接结果显式保持逐像素 3D 投影一致性，可直接馈入 SfM/SLAM 下游；提出 RSR 指标与先 padding、再配准、后算指标的三步评测协议，自建 Blender 合成与手机实拍两套 VLP 测试集。',
   '大基线宽 FOV 采集的拼接方案：合成集 PSNR 22.026/RSR 95.7%、Sampson 对极误差 4.12 pixel（UDIS++ 12.94，约 3.1×）、真实集 RSR 100%；大视差与大旋转共存时不重叠区域重投影缺失畸变、大面积遮挡时残差扩散退化为噪声；5.8 s/图显著慢于 UDIS++ 2.7 s，作者建议以 parallax classification 分流。'),
}

def val(s):
    return round(0.20*s[0]+0.20*s[1]+0.15*s[2]+0.15*s[3]+0.15*s[4]+0.08*s[5]+0.07*s[6], 4)

MAIN, BF = [], []
ANNOUNCE_MAIN = {'2610.36853': 'cross', '2610.37036': 'cross', '2610.34235': '补录'}
for pid, (tzh, track, imp, nov, tec, exp, per, trl, rep, grade, note, rel, act) in S_MAIN.items():
    d = D[pid]
    MAIN.append(dict(id=pid, title='', title_zh=tzh, track=track,
        scores=dict(IMP=imp,NOV=nov,TEC=tec,EXP=exp,PER=per,TRL=trl,REP=rep), grade=grade,
        grade_note=note, evidence=('PARTIAL' if pid=='2610.36014' else 'FULL'),
        level=('L1' if pid=='2610.36014' else 'L0'),
        status='CURRENT', venue=d['venue'],
        announce=ANNOUNCE_MAIN.get(pid, 'new'), tags=d['tags'],
        conclusion=d['conclusion'], problem=d['problem'], method=d['method'], experiments=d['experiments'],
        innovation=d['innovation'], limits=d['limits'], relation=rel, repro=d['repro'], action=act,
        value=val((imp,nov,tec,exp,per,trl,rep)), batch='2026-10-29'))
for pid, (tzh, track, imp, nov, tec, exp, per, trl, rep, grade, note, rel, act) in S_BF.items():
    d = D[pid]
    BF.append(dict(id=pid, title='', title_zh=tzh, track=track,
        scores=dict(IMP=imp,NOV=nov,TEC=tec,EXP=exp,PER=per,TRL=trl,REP=rep), grade=grade,
        grade_note=note, evidence='FULL', level='L0',
        status='CURRENT', venue=d['venue'], announce='replace/cross', tags=d['tags'],
        conclusion=d['conclusion'], problem=d['problem'], method=d['method'], experiments=d['experiments'],
        innovation=d['innovation'], limits=d['limits'], relation=rel, repro=d['repro'], action=act,
        value=val((imp,nov,tec,exp,per,trl,rep)), batch='backfill-1029',
        orig_window='旧稿 replace/cross 再公告（首次入馆）：2508=2025-08 投稿、2510=2025-10 投稿、2604=2026-04 投稿、2605=2026-05 投稿，2026-10-28 公告批次 RSS 混入'))

# 原始英文标题（RSS + 上批 candidates 兜底 ParetoGS）
rss = {json.loads(l)['base_id']: json.loads(l) for l in open('data/raw/2026-10-29_rss.jsonl',encoding='utf-8') if l.strip()}
for p in MAIN + BF:
    p['title'] = rss[p['id']]['title'] if p['id'] in rss else 'ParetoGS: High-Quality Continuous-Budget 3D Gaussian Splatting with Sparse Adapted Anchors'

MAIN.sort(key=lambda p: (-p['value'], -p['scores']['IMP'], -p['scores']['NOV'], p['id']))
BF.sort(key=lambda p: (-p['value'], -p['scores']['IMP'], -p['scores']['NOV'], p['id']))

# 定稿 Top10：按加权降序取前十，门②（≥5 赛道）触发一次回补——
# 纯值 Top10 = {37602,37036,36853,35902,36876,36312,36760,37172,36168,34235} 仅覆盖 4 赛道
# （重建与SLAM×4/渲染与显示×3/神经渲染×2/内容生成×1）；
# 按重筛闭环剔除重复赛道中最低分者 SG²SLAM（2610.36312，4.00，重建与SLAM 第 4 篇），
# 回补未覆盖赛道最高分 SOMA（2610.36384，3.79，评估与数据集）→ 覆盖 5 赛道。
TOP10_IDS = ['2610.37602','2610.37036','2610.36853','2610.35902','2610.36876','2610.37172',
             '2610.36760','2610.36168','2610.34235','2610.36384']
TOP10 = [p for pid in TOP10_IDS for p in MAIN if p['id'] == pid]

json.dump({'main': MAIN, 'backfill': BF, 'top10_ids': TOP10_IDS},
          open('data/scored_1029.json','w',encoding='utf-8'), ensure_ascii=False, indent=1)
print('main:', len(MAIN), 'bf:', len(BF))
for p in MAIN: print('M', p['id'], p['value'], p['grade'], p['track'], p['announce'], p['title_zh'][:34])
for p in BF: print('B', p['id'], p['value'], p['grade'], p['track'], p['title_zh'][:34])
print('TOP10:', TOP10_IDS)
print('saved data/scored_1029.json')
