# -*- coding: utf-8 -*-
"""组装 2026-10-31 评分数据：digest（子代理全文精读）+ 主会话 7 维评分定稿。
输出 data/scored_1031.json（main 18 + backfill 6）。内联中文文本统一中文弯引号。
候选池：2026-10-30（周五）公告批次 = 10-29 周四公告跳空后延迟释放（覆盖 10-27~10-29 提交，
API published 核验：10-27×1 / 10-28×7 / 10-29×10）；listing 728 篇摘要级 XR 命中 31 篇与 RSS 34 篇真新互证。
backfill-1031：RSS 混入的 12 篇旧稿 replace 再公告中 6 篇 XR（2501/2604/2605×2/2608×2，首次入馆）。"""
import json

D = {}
for g in ('g1', 'g2', 'g3', 'g4'):
    for d in json.load(open(f'data/digest_1031_{g}.json', encoding='utf-8')):
        D[d['id']] = d

# 评分表：id -> (title_zh, track, IMP,NOV,TEC,EXP,PER,TRL,REP, grade, grade_note, relation, action)
S_MAIN = {
 '2610.39399': ('ACD-GS：非对称曲率感知致密化的 3D 高斯泼溅', '渲染与显示', 4,4,4,5,5,4,5, 'A',
   '总分 4.37 达 S 线（≥4.2），但当日最高分 4.37 < 库内近 30 天 Top10 均分 4.420（现算，394 条入窗）→ 非重磅日，按校准关记 A（同 10-24 EgoHand / 10-27 WFM / 10-28 RacerGS / 10-29 RESPLE2 先例）',
   '属库内 3DGS 训练期密度控制与压缩线（Pixel-GS/AbsGS/GDAGS/FastGS 及后置压缩 LightGaussian/HAC/Mini-Splatting）：首次以二阶深度曲率（对几何边界敏感、对平面纹理稳健）替代一阶屏幕空间梯度作致密化先验，并以边界抑克隆/促分裂的非对称解耦 + 多视图光度门控 + 容量配额退火实现训练时原生稀疏化，与库内 RacerGS/ParetoGS 连续预算线正交可组合。',
   '3DGS 生产管线的即插即用模块：三大数据集高斯数与存储平均降约 60%（DB 151.9 / Mip360 274.3 / T&T 150.4 MB）且 Deep Blending PSNR 25.12 dB 最佳、训练最快，代码已公开；极端压缩下纯显式表征容量上限使高频纹理受损（作者建议轻量 MLP 混合架构）、曲率来自渲染深度依赖当前高斯质量、与后置量化/熵编码组合未评测。'),
 '2610.39745': ('UniffordInteractor：人-多物体交互的统一可承受性推理', '内容生成', 4,4,5,5,5,3,3, 'A',
   '总分 4.30 达 S 线（≥4.2），非重磅日按校准关记 A（同 10-24 EgoHand / 10-27 WFM / 10-28 RacerGS / 10-29 RESPLE2 先例）',
   '位于库内 HOI 运动合成与 3D affordance grounding 交叉线（HIMO/SyncDiff/SeqAfford/3D-AffordanceLLM）：首次以统一 affordance（Unifford）联合约束人-物与物-物接触并用 3D-MLLM 做关系推理，是库内 avatar 交互内容生产（文本/几何驱动）的上游；与 FlowHOI（语义接地流匹配生成）构成「先推理后生成 vs 端到端流匹配」两条路线。',
   'VR/AR 可交互角色动画生成的参考框架：HIMO FID 1.199/C% 0.348/Coll% 0.181 均最佳、3 物体场景 FID 较专用模型降约 50%，ACM TOG 正式发表；推理 8.27 s/样本距实时尚远、固定 K=3 物体槽、OOD 泛化明显退化（FID 1.316→4.587）；代码声明正式发表后发布。'),
 '2610.38951': ('GradSplat：前向传播内梯度精化的前馈 3D 高斯泼溅', '神经渲染', 4,5,4,5,4,3,4, 'A',
   '总分 4.27 达 S 线（≥4.2），非重磅日按校准关记 A（同 10-24 EgoHand / 10-27 WFM / 10-28 RacerGS / 10-29 RESPLE2 先例）',
   '属库内前馈 3DGS 线（pixelSplat/MVSplat/DepthSplat/AnySplat/NoPoSplat/YoNoSplat）并直接回应摊销差距：论证差距由高斯形状（scale/rotation）承载，首个在前向传播内以学习式梯度步自 refined 高斯（外观→形状分工 + 保体积对数各向异性校正），承接 LISTA/RAFT/QuickSplat 学习式优化传统，单模型覆盖 6→42 输入视图。',
   '稀疏视图实时重建的前馈 3DGS 新参照：RE10K 两套六视图协议九法 SOTA（窄 33.683/0.9593、宽 26.755/0.8993）、DL3DV 零样本 24.787 dB 最优；推理需多次额外渲染前向（每场景时延未报）、训练 178K 步四阶段 50.5 h（16×GH200）成本高；代码承诺发布（github.com/Jingong-Chen/GradSplat），跟进复现。'),
 '2610.40495': ('LucidLyra：前馈生成式可查询 3D 场景重建与联合理解', '内容生成', 4,4,5,5,4,3,4, 'A',
   '总分 4.22 达 S 线（≥4.2），非重磅日按校准关记 A（同 10-24 EgoHand / 10-27 WFM / 10-28 RacerGS / 10-29 RESPLE2 先例）',
   '处库内「生成式 3D 重建 × 3DGS 场景理解」交叉线（延续 Lyra latent-to-Gaussian 与 LangSplat/Gaussian Grouping/IGGT 两线）：首个把开放词汇语义与类无关实例理解经多任务蒸馏进前馈生成解码器（SAM/SAM2 轨迹 + RADSeg 语义的 track 池化目标），使单图产出的 3D 世界「可渲染且可查询」，补上库内生成式内容结构化一环。',
   '单图→可查询 3D 世界的首选框架：LucidLyra-SDG mIoU 64.1 超 lifted teacher 上界 60.5（较最强基线 +31.7）、mTrackPR 21.5（+9.8）、单场景分割 2.1 min（LangSplatV2 697 min）；教师预处理 1580 A100 GPU-days 成本极高、动态场景有轻微 PSNR trade-off（21.88 vs Lyra 22.16）；项目页承诺发布数据与基准。'),
 '2610.40614': ('L3G-World：潜空间 3D 高斯记忆的实时无限世界生成', '世界模型与仿真', 4,4,5,4,5,3,3, 'A', '',
   '处库内交互式世界模型/视频生成与显式 3D 记忆线（GEN3C/Spatia/Lyra 2.0/NeoVerse 3D 记忆派 + WorldKV/Yume 1.5 时间上下文派）：以潜空间 3D 高斯记忆（每高斯存 VAE latent 特征、直接渲染进 DiT 条件空间，消除重编码）+ 渲染误差引导的选择生成 + 门控残差精修同时满足紧凑、实时与跨回环一致，是库内实时世界模型线（OuroWorld/ME-World/InteractiveWorld）的效率跃迁。',
   '可实时探索的一致 3D 世界生成底座：较最强 3D 记忆基线 primitive 少 26.7–38.9×、VAE 渲染快 349–359×、481 帧回环自一致 PSNR 最佳、单卡 H100 9.02 FPS 唯一实时（WorldKV OOM）；记忆主要面向静态场景、极大尺度探索仍需自适应剪枝、Fast 蒸馏变体质量下降（16.00→14.59）；算力门槛高（4×A100 优化）、代码未承诺。'),
 '2610.37818': ('GOFish：全视场鱼眼高斯泼溅与网格提取', '渲染与显示', 4,4,5,5,4,3,3, 'A', '',
   '属库内「3DGS + 表面重建/数字孪生」线（GOF/SOF/PGSR/CoMe）与鱼眼渲染线（Fisheye-GS/DirectFisheye-GS/3DGUT/3DGRT）的交叉：首个直接在鱼眼图像上训练、光栅化超过 180° 全视场并从同一高斯场景提取对齐碰撞网格的方法，补上库内广角/全景采集在渲染与几何两端的缺口。',
   '机器人/自动驾驶传感器仿真与 360° 场景数字孪生的即用基线：全视场渲染 + 网格一体化输出（FIORD 200° PSNR +2.28 dB、F-score 0.245 居首、A10G 79 FPS）；项目页仅可视化、未声明代码开源，标定与位姿误差敏感、静态场景假设；广角外观建模（边缘衰减 +3.17 dB）与标定 Mip 过滤（高斯数降 2.2–5.4×）可迁移至其他广角管线。'),
 '2610.38278': ('BudSplat：渲染预算约束下的紧凑前馈 3D 高斯泼溅', '神经渲染', 4,4,4,5,5,3,3, 'A', '',
   '属库内前馈 3DGS 线（pixelSplat/MVSplat/DepthSplat/AnySplat/NoPoSplat/WorldMirror）：首次把原语增长问题形式化为渲染预算约束下的表示学习（VGGT 残差 token 细节重要性 + 保重要性体素融合 + 质量感知剪枝 + patch 配额重分配），与库内重建后压缩线（RacerGS/ParetoGS/Budgeted-GS/LoBE-GS）互补但定位在预测阶段。',
   'XR 实时渲染与大规模流式加载的前馈 3DGS 新基线：RE10K 32 视图 5% 保留率 97K 高斯 23.08 PSNR（AnySplat 1363K 得 22.69）、ACID 72 视图 227K 对 4557K；骨干显存占全流程 79%（24 视图约 42 GB/卡）是下一瓶颈、自建低重叠协议绝对分数与公开基准不可直接比较；匿名可视化页公开、代码未释放。'),
 '2610.38349': ('单视图新视角合成基准的坐标对齐评测协议', '评估与数据集', 4,4,4,5,4,3,5, 'A', '',
   '属库内「NVS 评测方法论」空白的第一篇工作：把经典视觉定位流程（2D-2D 匹配→2D-3D→PnP→共视区优化）上升为单视图 NVS 基准协议层，重评了库内常客 Flash3D/Lyra/SHARP/ViewCrafter 等，结论直接影响 XR 单图→3D 内容生产的方法选型；其「视频生成 + 3DGS 初始化」免任务基线也与 XR 场景快速数字化相关。',
   '单视图 NVS 论文复现与选型前必读：修正后排名剧变（Flash3D RE10K 14.52→22.04 dB、SHARP 降至 17.74），任何新方法都应在共视区对齐协议下报告；免任务训练基线平均 18.39 PSNR 媲美专训 SOTA，本身即低成本强基线；评测代码已公开（ubc-vision/aligned-sv-nvs-bench）。'),
 '2610.39076': ('Tactus：面向自然灵巧数据采集的触觉与姿态感知手套', '触觉与多模态', 3,4,5,5,4,4,3, 'A', '',
   '属库内可穿戴触觉感知线（STAG/OSMO/PPS/JQ 手套 + UmeTrack/AVI-HT 视觉-惯性融合 + ARCTIC/HOT3D 手物交互基准）：首个把校准指尖力、抗遮挡姿态与保自然抓取形态共注册于同一 3D 针织服装的平台（Meta Reality Labs），并建立首个跨平台触觉手套定量基准，与库内 VR 遥操作/第一人称交互同域。',
   '遥操作/VR 交互与机器人数据采集的触觉手套选型参照：最小可检测力 0.59 N（较商用基线低 1.6–2.7×）、跨被试一致性 0.87、23 项灵巧任务时间比 1.06（外骨骼 1.89）；滑移检测仅为可行性结果、每会话仍需人工在线校正、用户研究规模小（N=3/N=5）；无硬件开源，按论文工程细节可自建复现。'),
 '2610.39936': ('MLLM-GS：多模态大模型先验引导的极端环境新视角合成', '神经渲染', 4,4,4,4,5,3,3, 'A', '',
   '属库内退化/极端环境 NVS 与高效 3DGS 线（上承 DehazeGS/WaterSplatting/Smoke-GS 物理或生成先验重建，下接 Faster-GS/Speedy-Splat 加速）：首次以通用 MLLM 视觉先验替代退化特定成像模型，配套 HVI 色彩空间轻量校正网络（约 4M 参数、仅 3 对干净视图）与三方面系统加速，是库内恶劣条件沉浸式场景重建的底座。',
   '烟雾/暗光等恶劣条件 3D 重建首选基线：RealX3D 烟雾 PSNR 22.27 dB（+4.69 over 最强基线）、5K 迭代即超所有方法 30K 迭代、训练降约 9×、Gaussian 数降 80–95%；强离焦/运动模糊与曝光变化仅定性结果、默认依赖闭源商用 MLLM（Nano Banana Pro）、仍需每场景 3 对配对干净视图；数据集已公开。'),
 '2610.40599': ('HairDeck：单图生成可动画程式化头发卡片', '内容生成', 3,4,4,5,4,3,3, 'A', '',
   '属库内程式化角色资产生成线（直接对标 CHARM，与 strand 系 DiffLocks/HairGPT、image-to-3D TRELLIS.2/Hunyuan3D 及 set diffusion 方法同域）：首次面向可动画资产结构，把发卡与弹簧骨作为两重无序集合生成（一 primitive 一 token + set DiT + flow matching + 脸部锚定 head frame），服务库内 VR/AR avatar 与游戏角色头发资产生成空白。',
   'avatar 头发资产生成即用方案：CHARM 测试集 CD 降 44%（0.0066 vs 0.0117）、朝向误差降逾半、快 33 倍（1.01 s），输出 VRM 就绪含弹簧骨链（recall 0.625 vs 检索 0.289）；只生成几何与 UV 不生成纹理、训练分布限程式化 VRoid 发型（极短发与写实 alpha-textured 不在分布内）；项目页已公开、代码未承诺。'),
 '2610.39201': ('COGS：属性感知的物体级 3D 高斯泼袭感知诊断基准', '评估与数据集', 4,3,4,5,3,3,5, 'A', '',
   '属库内 3DGS 直接感知线（MACGS/ShapeSplat/SceneSplat）与特征提升线（LangSplat/Gaussian Grouping）之间的诊断性工作：以生成式管线 + 三重人工质检构建 15,675 物体 40 类无伪影 3DGS 数据集，用八属性配置协议与跨数据集外验把「3DGS 感知属性利用」变成可测量问题，为库内 3DGS 感知架构设计提供原则。',
   '3DGS 感知研发的评测台：八属性配置 + HALO-B/L 参考模型（94.50%/94.70% OA）可直接用于模型选型；「属性并非越多越好」（PointNet/DGCNN POSQ 胜全量）与「聚合先于抽取」原则可迁移；TRELLIS 生成资产与真实采集分布有别（自述为补充而非替代），需与 MACGS/ScanNet 真实基准并用；数据集 HF 公开（非商业许可）。'),
 '2610.40525': ('CrossWeave：稀疏 2D-3D 对齐的跨模态场景与实例检索', '感知与认知', 3,3,4,5,4,3,5, 'A', '',
   '属库内跨模态（2D-3D）检索与视觉位置识别线（CrossOver 双模型 / SceneGraphLoc 场景图定位 / NetVLAD/SALAD 局部聚合）：以局部 patch-point 对应监督取代全局对齐作为唯一监督、用最优传输聚合替代平均池化，是库内 AR 设备对预扫描环境重定位与内容锚定的检索底座。',
   'AR 重定位/内容锚定的检索底座：ScanNet 场景 Top-1 61.54（较 CrossOver +21.16）、实例 Top-1 78.77、3RScan 场景 46.50（+22.93），单卡 A6000 约 21 GPU 小时训练、10% 数据仍超前 SOTA；推理假设查询图像来自同次观看会话（跨会话未处理）、依赖上游分割质量（R@75% 降 12.5–22.9 点）；代码已公开（crossweave3d/crossweave）。'),
 '2610.38117': ('ProACT：性能驱动的 VR 消防训练动态难度调节', '空间计算与UI', 4,3,4,4,4,3,2, 'B', '',
   '属库内「沉浸式应急训练 × 动态难度调整（DDA）」线（与 VR 消防/压力训练研究同域，承接 Hunicke 以来游戏 DDA 一脉）：把适应对象从指令反馈层换成仿真火行为本身（全局蔓延概率 PI 控制 + 局部 LLM 语义可燃性更新），以任务进度而非用户技能建模驱动调节，可迁移至灾害疏散、工业安全等难度由动态场景行为涌现的训练领域。',
   'VR 技能训练系统的难度调节设计参考：双尺度架构（0.5 s 全局 PI + 20 s 局部 LLM 有界更新）、2D/3D 仿真 on-target 率四档最高、8 人 VR 研究 8 项指标居首；用户研究规模很小（n=8）、自编量表、无代码，结论外推需更大样本与标准化测量；团队级标定与多 HMD 同步是明确开放问题。'),
 '2610.38358': ('Volley3D：单目转播的全序列 3D 排球重建', '内容生成', 3,4,4,4,4,2,3, 'B', '',
   '属库内「单目体育 3D 重建」线（MonoTrack/TT3D/VIRD/Soccer on Your Tabletop）：首个处理集体球类高幅起跳与球-人耦合的框架，以物理接地（起跳牛顿插值 + 空气动力学边值问题绑定 3D 手部顶点）绕开 2D 重投影深度漂移，与库内多视图 3DGS 重建（LiveSplats 一脉）形成单目-多视对照。',
   '赛事沉浸式回放/AR 新视角转播的模块化参考：起跳漂移 1.05→0.23 m、球轨迹 3D RMSE 0.272 m（MonoTrack 1.56 m 且重投影过拟合）；离线管线（实时性留待未来）、缺「转播视角 + 同步 3D 真值」端到端数据集、无球旋转（Magnus）建模；项目页公开、人工标注承诺公开、无代码仓库。'),
 '2610.38536': ('智能体数量与行为对 VR 疏散训练心理反应的影响', '感知与认知', 4,3,3,4,3,2,2, 'B', '',
   '属库内「VR 疏散/灾害训练 × 人群心理」线（承接 Helbing/Moussaïd 疏散人群行为研究与 Kasahara/Wei/Cao 等 VR 人群心理学工作）：首次把智能体数量、路线选择比例、情绪与行为多样性作为受控组内自变量，直接量化对恐惧/安全感/自信/犹豫及疏散成功率的影响，填补库内从众偏差设计的实证空白。',
   'XR 应急训练的智能体行为设计准则参考：无智能体同行显著提高恐惧（p=.009）、智能体集体正确路线显著提成功率（10%→80% 单调上升）；警惕反直觉发现（行为/情绪最多变时恐惧最低但成功率最差）与「智能体误导—失败归咎—自主性受损」风险；20 人小样本、自编 VAS 量表、无代码/数据，结论需更大样本复验。'),
 '2610.38629': ('ItemCompass：商品级硬件上的实时可穿戴寻物系统', '空间计算与UI', 4,3,4,4,3,4,2, 'B', '',
   '属库内可穿戴/普适计算的空间记忆线（MemPal 一脉）并构成库内 SLAM-based AR 的替代路线：以轻量 PDR + 视觉锚点重置在微控制器级眼镜节点上实现持久空间记忆 + 本地 LLM 语音检索，把库内「空间锚点/数字孪生」概念落到家庭辅助与老年无障碍场景而非渲染管线。',
   '低成本 AR 寻物/辅助系统的完整工程参照：眼镜节点 + 边缘服务端闭环（总延迟 36.7 ms、PDR 漂移 0.40 m、步频精度 97.5%）、硬件级隐私护盾（100% 检测）、N=31 信任 4.6/5.0；多房间重复转弯航向漂移累积、微物体召回 3 m 仅 6.7%、舒适度 3.5/5.0 待小型化；mAP 表内数据不一致（表 1 记 0.707 vs 正文 0.874）引用需谨慎；无开源。'),
 '2610.39147': ('KCA：4D 点云视频模型的运动-几何黑盒因果归因', '感知与认知', 3,4,4,4,3,2,4, 'B', '',
   '处库内 4D 点云视频理解（MeteorNet/PSTNet/P4Transformer/Mamba4D）与因果归因 XAI（LENS/CaCE/DANCE）的交叉带：首个把 4D 模型决策完备分解为运动项与几何项的黑盒方法（免点对应的集合式干预算子 + 序对称 Shapley 分解 + 四重验证协议），与库内 4D LangSplat/4DGC 动态场景表征共享数据模态但目标是解释识别决策而非生成。',
   '4D 感知模型部署前审计工具：黑盒访问 + 真实传感数据 + A100 上 0.5–2.3 s/片段成本，适合 assistive monitoring/AR 应用上线前的依赖检查（交叉审计分离运动 vs 几何训练线索）；骨干从头训练且运动任务模型仅 3/6 种子可靠、分解语义依赖代理角、k-means 区域追踪在快速/遮挡下漂移；附录称代码已释放。'),
}

S_BF = {
 '2604.19673': ('InHabit：基于图像基础模型的 3D 人-场景交互数据规模化生成', '评估与数据集', 4,4,4,5,4,3,4, 'A', '',
   '处库内「2D 生成先验提升到 3D」与「人-场景交互数据合成」交叉线（GenZI/POSA/HumanWild/DAViD 及 TRUMANS/PROX/BEDLAM 捕获集）：以全自动 render–generate–lift 管线把 VLM 动作推理与图像编辑合成经 PhySIC 式优化提升为建筑级 3D 场景中的 SMPL-X 交互，是库内场景内容生成管线的数据层，与本批 UniffordInteractor（交互生成）构成上下游。',
   '具身/XR 仿真的人物填充与 HSI 训练数据供给：78k 样本/约 800 场景、用户研究 78.1% 首选、DECO 接触 F1 +7.4%、GRAFT PA-MPJPE 72.52→54.83；仅生成静态姿态、依赖闭源 Gemini 2.5（版本敏感）、接触指标为 LLM 伪真值存在评估偏差；数据集与代码承诺公开（virtualhumans.mpi-inf.mpg.de/inhabit）。'),
 '2605.07351': ('SplitGS-Loc：高斯劈分消解多对一对应的视觉定位', '重建与SLAM', 3,4,4,5,4,3,5, 'A', '',
   '属库内「高斯特征场视觉定位（GSFFs）」线（GSplatLoc/GSFFs-PR/STDLoc）：首次指出光度优化 GSFF 与 PnP 的结构性错位（体积延展致多对一对应 + 视图相关冗余高斯），以组成权重特征提升（PlugGS-Loc，一分钟免训练转换）+ 沿主轴混合高斯劈分从几何上消歧，是库内 3DGS 重定位/AR 设备端定位方向的效率改进者。',
   'AR 设备端视觉定位的轻量方案：Cambridge Landmarks 平均 8.7cm/0.15°（STDLoc 11.1/0.19°）、建图 7 分钟、地图 97MB（STDLoc 精化版 415MB）、代码已公开（misoleekr/SplitGS-Loc）；依赖原始 3DGS 质量（剧烈光照变化/稀疏轨迹受限）、仅中小规模场景验证；特征渲染精化可再降至 8.4cm 但需存完整 GSFF（地图 415MB）。'),
 '2608.08285': ('Ego-OSCAR：开源头戴双目-惯性第一人称采集系统', '系统与平台', 4,3,4,4,3,4,5, 'A', '',
   '属库内「具身 AI 数据采集硬件与数据集」线（Ego4D/EPIC-KITCHENS/Nymeria 语料 + Project Aria 硬件谱系 + UMI/Mobile ALOHA 开源硬件）：以约 200 美元整机物料把可访问性-保真度前沿推到智能手机方案与封闭研究设备之间，是库内第一人称数据底座（EgoACT/EgoJEPA 等消费的上游）的采集基建。',
   '自建公尺度双目第一人称数据底座的完整蓝本：硬件同步全局快门立体 + 同步 IMU + 看门狗，CAD/BOM/固件/采集栈全开源（CC BY 4.0），6 个月 1,462 会话约 550 小时/相机、96% 可用会话率、随设备发布 209,315 条开放词表动作片段；消费级 IMU 是位姿误差主因（可更换未基准测试）、未证明语料学习价值、语料集中于印度 25 名贡献者偏家庭活动。'),
 '2608.27562': ('VidParse：免训练的第一视角流程在线解析', '感知与认知', 3,4,4,4,4,3,4, 'A', '',
   '属库内「在线时序动作分割/第一人称流程解析」线（OnlineTAS/ProTAS/Mamba-OTR + VideoGraph/活动语法/GEBD）：首个把免训练通用事件边界检测与图约束动作解析无缝整合（操作锚定特征 + 高斯锥形棋盘核 + 任务图硬约束束搜索），服务库内 AR 实时助手（步骤引导）的设备端部署。',
   'AR 步骤引导/第一视角助手的免训练解析方案：EgoPER F1@0.5 77.6（在线 ProTAS 51.3）、5/7 步转移 AUC 达基线 5–10 倍、8.6 FPS 零梯度更新、解码 CPU 32.8 s/视频（ProTAS GPU 706 s）；任务图从训练序列归纳（未见流程变体泛化差）、手-物检测在严重遮挡/运动模糊下误检或迟检、段级处理不适合超低时延应用；代码公开（learn2phoenix/VidParse）。'),
 '2605.29583': ('BitC-3DGS：位压缩 token 化的高容量 3DGS 水印', '渲染与显示', 3,4,4,4,4,3,3, 'A', '',
   '属库内「3DGS 资产安全与版权保护」线（GaussianMarker/3D-GSW 低层扰动 + GuardSplat CLIP 语义水印 + PrinGS 后训练隐私匿名化）：以位压缩 token 化把 CLIP 77 token 容量上限改写为 75n bit，配 chunk/bit 双分支解码与难样本消息采样，补上库内 3DGS 资产溯源/授权/防篡改的高容量元数据承载能力。',
   '3DGS 内容分发（溯源/授权/防篡改）的水印工具：128 bit 恢复精度 90.59%（[In] 91.42%）且 PSNR 34.32/LPIPS 0.0068 保真、seen/unseen 差距远小于基线、模型空间删克隆/噪声下 96 bit 仍 86%+；容量越大解码越难（128 bit 约 91%）、仅 Blender/LLFF 两类数据、未验证其他高斯表示；无代码仓库但实现细节完备。'),
 '2501.12060': ('GSVC：以 2D 高斯泼溅为基元的视频表示与压缩', '系统与平台', 3,4,4,4,4,2,3, 'B', '',
   '属库内「高斯泼溅用于视觉媒体压缩/表示」线（GaussianImage 图像级、VGR/VeGaS 3DGS 视频）：首次以压缩为主目标，把 I/P 帧预测、GSP 可学习剪枝、GSA 新内容增强、DKS 场景切换检测等经典编解码概念移植到 2D 高斯基元，与库内 volumetric video 压缩线共享「显式表示 + 学习压缩」思想。',
   '沉浸式视频实时播放的参考编解码器：率失真与 AV1/HEVC 相当（MS-SSIM/VMAF 优于或持平多数标准编解码器）、解码 1583.72 fps（DCVC-DC 2.4）、免预训练、显式规模-质量-时长控制；编码约 200 s/帧离实时甚远、仅 3 条 UVG 视频验证、L2 损失某些场景 PSNR 逊于标准编码器；定位为方向性参考而非生产方案。'),
}

def val(s):
    return round(0.20*s[0]+0.20*s[1]+0.15*s[2]+0.15*s[3]+0.15*s[4]+0.08*s[5]+0.07*s[6], 4)

MAIN, BF = [], []
ANNOUNCE_MAIN = {'2610.37818': 'cross', '2610.40599': 'cross'}
for pid, (tzh, track, imp, nov, tec, exp, per, trl, rep, grade, note, rel, act) in S_MAIN.items():
    d = D[pid]
    MAIN.append(dict(id=pid, title='', title_zh=tzh, track=track,
        scores=dict(IMP=imp,NOV=nov,TEC=tec,EXP=exp,PER=per,TRL=trl,REP=rep), grade=grade,
        grade_note=note, evidence='FULL', level='L0',
        status='CURRENT', venue=d['venue'],
        announce=ANNOUNCE_MAIN.get(pid, 'new'), tags=d['tags'],
        conclusion=d['conclusion'], problem=d['problem'], method=d['method'], experiments=d['experiments'],
        innovation=d['innovation'], limits=d['limits'], relation=rel, repro=d['repro'], action=act,
        value=val((imp,nov,tec,exp,per,trl,rep)), batch='2026-10-31'))
for pid, (tzh, track, imp, nov, tec, exp, per, trl, rep, grade, note, rel, act) in S_BF.items():
    d = D[pid]
    BF.append(dict(id=pid, title='', title_zh=tzh, track=track,
        scores=dict(IMP=imp,NOV=nov,TEC=tec,EXP=exp,PER=per,TRL=trl,REP=rep), grade=grade,
        grade_note=note, evidence='FULL', level='L0',
        status='CURRENT', venue=d['venue'], announce='replace', tags=d['tags'],
        conclusion=d['conclusion'], problem=d['problem'], method=d['method'], experiments=d['experiments'],
        innovation=d['innovation'], limits=d['limits'], relation=rel, repro=d['repro'], action=act,
        value=val((imp,nov,tec,exp,per,trl,rep)), batch='backfill-1031',
        orig_window='旧稿 replace 再公告（首次入馆）：2501=2025-01 投稿、2604=2026-04 投稿、2605=2026-05 投稿、2608=2026-08 投稿，2026-10-30 公告批次 RSS 混入'))

# 原始英文标题（RSS）
rss = {json.loads(l)['base_id']: json.loads(l) for l in open('data/raw/2026-10-31.jsonl',encoding='utf-8') if l.strip()}
for p in MAIN + BF:
    p['title'] = rss[p['id']]['title']

MAIN.sort(key=lambda p: (-p['value'], -p['scores']['IMP'], -p['scores']['NOV'], p['id']))
BF.sort(key=lambda p: (-p['value'], -p['scores']['IMP'], -p['scores']['NOV'], p['id']))

# 定稿 Top10：按加权降序取前十（同分按 IMP/NOV 降序、再按赛道多样性优先、再 id 升序）。
# 4.15 三篇并列（L3G-World/GOFish/BudSplat，IMP/NOV 均同）→ 赛道多样性优先 L3G-World
# （世界模型与仿真为未覆盖赛道），GOFish 与 BudSplat 按 id 升序。
TOP10_IDS = ['2610.39399','2610.39745','2610.38951','2610.40495','2610.40614','2610.37818',
             '2610.38278','2610.38349','2610.39076','2610.39936']
TOP10 = [p for pid in TOP10_IDS for p in MAIN if p['id'] == pid]

json.dump({'main': MAIN, 'backfill': BF, 'top10_ids': TOP10_IDS},
          open('data/scored_1031.json','w',encoding='utf-8'), ensure_ascii=False, indent=1)
print('main:', len(MAIN), 'bf:', len(BF))
for p in MAIN: print('M', p['id'], f"{p['value']:.2f}", p['grade'], p['track'], p['announce'], p['title_zh'][:34])
for p in BF: print('B', p['id'], f"{p['value']:.2f}", p['grade'], p['track'], p['title_zh'][:34])
print('TOP10:', TOP10_IDS)
from collections import Counter
print('grades main:', dict(Counter(p['grade'] for p in MAIN)), 'bf:', dict(Counter(p['grade'] for p in BF)))
print('tracks top10:', dict(Counter(p['track'] for p in TOP10)))
print('tracks all:', dict(Counter(p['track'] for p in MAIN)))
print('today_max:', MAIN[0]['value'])
print('saved data/scored_1031.json')
