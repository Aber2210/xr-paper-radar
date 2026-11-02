# -*- coding: utf-8 -*-
"""组装 2026-11-03 评分数据：digest（子代理全文精读）+ 主会话 7 维评分定稿。
输出 data/scored_1103.json（main 11 + backfill 2）。内联中文文本统一中文弯引号。
候选池：2026-11-02（周一）公告批次（周末 10-31/11-01 积压于周一 00:00 UTC=08:00 北京时间释放；
API published 核验提交日 10-29×3 / 10-30×8）；listing 347 篇摘要级 XR 命中 21 篇与 RSS 真新集合逐篇一致。
backfill-1103：RSS 混入的旧稿 replace 再公告中 2 篇 XR（2511=2025-11 投稿 / 2602=2026-02 投稿，首次入馆）。"""
import json

D = {}
for g in ('g1', 'g2', 'g3', 'g4'):
    for d in json.load(open(f'data/digest_1103_{g}.json', encoding='utf-8')):
        D[d['id']] = d

# 评分表：id -> (title_zh, track, IMP,NOV,TEC,EXP,PER,TRL,REP, grade, grade_note, relation, action)
S_MAIN = {
 '2610.41501': ('VoxLution：体素进化的高保真 3D 室内场景生成', '内容生成', 4,4,4,5,5,3,3, 'A', '',
   '位于「3D 几何自回归生成」与「稀疏层次表示」两条技术线的交汇：向上追溯至 PolyGen、MeshGPT 的网格 token 自回归，以及 OctFormer、OctGPT（本文直接基线，被从物体级微调改造到场景级对比）、ShapeFormer 等的八叉树/占用自回归，并受图像域 VAR 的 next-scale 多尺度预测启发；coarse-to-fine 扩散一线（BlockFusion、LT3SD、WorldGrow）与 layout 组合式方法（ATISS、SceneFormer、DiffuScene）为主要对照。与 Scaffold-GS、TRELLIS.2 结构化 latent 路线相比，VoxLution 放弃学习式潜压缩、直接在稀疏体素占用上做序列建模，代表场景级生成中「显式稀疏自回归」的一支。',
   'VR/空间计算室内场景资产生成的即用基线：3D-FRONT FPD/FID 较 LT3SD 降 59.6%/51.1%、ScanNet++ 降 70.5%/73.8%，体素细至 1.5625 cm（较基线细 41%），22 人用户研究总体偏好 84.6%；每房间约 22 分钟（级联占 20 分钟）离实用有距、代码与权重开源情况原文未述需跟进；仅单层室内场景、不含纹理外观，组合纹理生成线（如 TRILLIS.2/Scaffold-GS）可补全。'),
 '2610.41602': ('DrawSplat：Atlanta World 引导的隐式高斯 SLAM 室内重建', '重建与SLAM', 4,4,5,5,4,3,3, 'A', '',
   '处于 Gaussian SLAM 与结构先验 SLAM 的汇合点：承接 SplaTAM/MonoGS 的显式高斯在线建图、LoopSplat 的回环一致性与 SEGS-SLAM 的隐式/结构增强路线，直接对标 Manhattan World 假设的 MG-SLAM（论文指出其结构先验未接入可微优化）、NeRF 先验稠密化 DenseSplat 与预计算位姿的 AtlasGS。相较 ORB-SLAM 点线传统与 NeRF 系（NICE-SLAM、Co-SLAM、ESLAM），它以 3DGS 可微光栅化换实时性，以 Atlanta World（多水平主导方向加共享重力）替代单一 Manhattan 框架以适配多房间布局，是「结构先验 × 隐式高斯」方向在 RGB-D 室内 SLAM 的代表性推进。',
   'RGB-D 室内 SLAM 的实用新基线：Replica ATE 0.27 cm、Apartment 1.09 cm 较次优 MG-SLAM 降 60%、ScanNet PSNR +2.54 dB、F1 93.7 高斯类最高、模型 18.29 MB/显存 4.5 GB 全场最小；无代码但硬件与实现细节披露完整可自建复现；室外/高动态/弱 AW 假设空间性能不稳、语义图依赖 Mask2Former 预计算（9.2 FPS）是部署瓶颈，渲染 209 FPS 低于高度优化的显式高斯系统（MonoGS 465 FPS）。'),
 '2610.41127': ('MotorSense：视频-EMG 电机感觉表征配对数据集', '评估与数据集', 4,4,4,5,4,3,5, 'A', '',
   '位于具身感知与第一视角理解交叉线：数据侧上承 ActionSense、Ego4D/EPIC-Kitchens 及 FEEL/OpenTouch/TouchScale 等力-触觉数据集，以 EMG 提供更稠密且不遮挡手部的信号；表征侧对标 IMU2CLIP 及音频/触觉/语言对比预训练，把 CLIP 式对齐从视觉-文本/音频扩展到视觉-肌肉信号；生成侧与语言/关键点/音频条件扩散（CogVideoX、MimicMotion 一系）并列，首次引入 EMG 运动码条件并复用 Video2LoRA 轻量控制；下游直接用 ARCTIC/H2O/HOT3D 等手-物基准评测。',
   '第一视角具身预训练的数据底座（100 小时配对视频-EMG、数据/模型/代码全公开，IRB 与去标识化完备）：EK100 动词较最佳基线 +15.86、H2O MPJPE -4.63 mm、接触 IoU +4.61 全面超越纯 RGB 自监督，EMG 运动码条件扩散 FVD 373→304（仅 50M 可训参数）；8 通道消费级 EMG 信息上限、参与者偏少（Aria 仅 8 人）与前臂周径选择偏差是主要数据局限，egocentric 视频与生理 EMG 的隐私/生物特征风险需按研究用途条款评估。'),
 '2610.41833': ('PGGT-Loc：基元接地的几何 Transformer 前馈相机定位', '重建与SLAM', 4,4,4,5,4,3,5, 'A', '',
   '处于 DUSt3R 式前馈几何 Transformer 与高层地图相机定位两条线的交汇：架构上承接 DUSt3R/MASt3R/VGGT 一系可扩展多视图 Transformer 范式；任务上直接对标并大幅改进同组前作 PlanaReLoc（CVPR 2026，平面基元 region matching，数据管线亦沿用其工作流）与 SPVLoc（ECCV 2024，layout render-and-compare），并与 MeshLoc、F3Loc、LASER 等 render-and-compare 及 GeoTransformer/FreeReg 等 I2P 基线比较。对 XR/AR 谱系而言，它把无纹理、紧凑、可人工编辑的结构地图纳入实时 6-DoF 定位的可选项。',
   'AR 设备端重定位的前馈新范式：ScanNet（0.2m,10°）召回 69.0%（PlanaReLoc+Refine 48.5%）、中位 2.7°/0.14 m，免显式对应求解/PnP/穷举渲染且不依赖相机内参先验，代码与模型已开源；仅限平面基元构成的地图、多房间合并地图召回随规模显著下降、surface/layout 两类任务需分别训练是落地缺口；与库内 SplitGS-Loc（高斯特征场定位）构成「结构基元 vs 高斯特征场」两条设备端定位路线。'),
 '2610.41671': ('OpenVIO：支持针孔/鱼眼/360° 的统一开源视觉惯性里程计系统', '重建与SLAM', 4,3,4,4,4,4,5, 'A', '',
   '属于滤波器式 VIO 谱系的系统化延伸：核心估计器是 Mourikis & Roumeliotis 的 MSCKF 结合 Li & Mourikis 的持久 landmark 与逆深度参数化，动态初始化沿用 Geneva & Huang 的视觉惯性 SfM 线性求解加 Ceres 精化框架；对标表中所列九大开源系统（MSCKF-VIO、ROVIO、OKVIS、VINS-Mono/Fusion、SVO Pro、OpenVINS、Basalt、Kimera-VIO），以 360° ERP 支持形成差异化。相对 ORB-SLAM 式点线方案，它以单位光线抽象加 EKF 换取跨相机模型的统一实现与轻量部署，是开源 VIO 基础设施方向的实用贡献。',
   '开源 VIO 基础设施的实用贡献（MIT 许可、pinhole/fisheye/360° ERP 统一接口）：TUM-VI 单目平均 ATE 0.377 m 为九系统最优、EuRoC/TUM-VI 全序列完成、PanoAir 17 架次平均 ATE 1.14 m 并在线估计 ERP 拼接误差与双镜头曝光延迟；XR 设备与全景相机追踪的直接可选底座；无回环与地图复用（仅导出接口）、滤波器长时一致性弱于优化式后端、未报帧率是明确缺口，二次开发接回环即可面向产品。'),
 '2610.41011': ('PriorGS：先验引导的单曝光 HDR 新视角合成', '神经渲染', 3,4,4,4,5,3,4, 'A', '',
   '位于 HDR-NVS 主线：从多曝光的 HDR-NeRF/HDR-GS/GaussHDR 到单曝光的 SeHDR、Mono-HDR-GS 演进线，直接对标这两个同期单曝光工作。其伪 HDR 先验承接 2D 单曝光 HDR 重建（Eilertsen、IntrinsicHDR 一系），base-gain 表征对应 2D 域 LDR-gain 格式（ISO 21496-1、Ultra HDR、Gain-MLP），CRF 先验源于 DoRF 数据库与 Eilertsen 双参数近似，是把 2D 逆色调映射知识系统迁移进 3DGS 框架的代表工作。',
   '沉浸式 HDR 内容生产（虚拟制片/HDR 显示）的单曝光 3DGS 重建基线：真实场景重曝光 PSNR 24.31/23.00 dB、合成 HDR-NVS 31.22 dB，较全部基线提升约 4-8 dB，并支持 3D HDR 外观编辑（gain field 缩放）；单张 RTX 3090 可复现全部实验、实现基于公开 HDR-GS 代码、承诺发表后开源；数据集小（每数据集 4-8 场景）、性能对所选 2D HDR 方法敏感（GMNet 变体在 HDR-Plenoxels 不及 GaussHDR）、μ-law 协议依赖逐场景亮度校正是复现选型注意点。'),
 '2610.40832': ('EgoHSI3R：第一视角视频的在线 4D 手-场景交互重建', '化身与人体', 4,4,4,4,4,3,3, 'A', '',
   '位于前馈几何基础模型线（DUSt3R/VGGT→Spann3R/SLAM3R/CUT3R 的序列化路线）与第一视角手部重建线（HaMeR/WiLoR 相机系，HaWoR/Dyn-HaMR/StableHand 世界空间系）的交叉点，并首次把稠密接触估计（HACO、ContactPose 一系）纳入统一前馈框架；与 MINT（相机+手轨迹）、UniSH/Human3R（第三人称 SMPL）互补，对标并超越 HaWoR、StableHand、HandFlow 等世界空间方法。',
   '具身/XR 手-场景交互理解的在线重建底座：ARCTIC W-MPJPE 108.80 mm 最优（较 StableHand 降 15.79 mm）、端到端 10.07 FPS、峰值显存 6.65 GiB，可作 VR 遥操作/第一视角助手的实时手-物状态估计上游；接触 recall 偏低（45-50%）、参数 1470M 偏大、无未来帧平滑（AccEr 16.91 偏高）、接触标签为几何距离生成而非力标注、代码尚未发布是主要缺口。'),
 '2610.41987': ('FoAViS：中央凹主动视觉系统的学习注视策略分析', '感知与认知', 3,4,4,4,3,2,3, 'B', '',
   '位于 RAM（Mnih et al. 2014）/DRAM 开创的深度主动视觉线与计算神经科学 gaze 模型线的交汇处。论文以系统比较 20 余个模型，直接对标 CanViT（Berreby et al. 2026，高分辨率 canvas 记忆但仅随机位置加熵启发式）、GVSM、AdaptiveNN、AdaGlimpse、TORE、Saccader 等；foveation 沿用 Lukanov et al. 2021 的 log-polar 方案；理论上连接 normative gaze 传统（Najemnik & Geisler 理想观察者）与数据驱动 scanpath 模型（Kümmerer/Bethge、DeepGaze III）。对 XR 注视点渲染谱系，它提供可学习注视策略的类脑对照系统。',
   '中央凹渲染/眼动研究的类脑参照系：并发策略-任务共适应全面超随机位置训练（T=4 ImageNet +4.8 Acc、C-MNIST +8.8%）、涌现无监督 inhibition of return、scanpath 统计与人类（MIT1003）对照；绝对性能仍明显落后 passive 全图基线（分割低 4.8-6.4 mIoU）、13.5M 小模型无代码、log-polar 仅定性近似视网膜，作为注视策略先验用于 foveated rendering 调度需先解决 passive 差距与 stop-grad 训练不稳定问题。'),
 '2610.41496': ('VR 中改变手部视觉反馈对特发性震颤的探索性研究', '感知与认知', 4,3,3,4,3,2,2, 'B', '',
   '处于「感知反馈操纵」与「神经运动障碍康复」的交叉线：上游承接 redirected walking 与 hand redirection（Zenner & Krüger、Steinicke 组等）关于视觉-运动差异可被不被察觉地操纵的结论，以及 Cohn et al. 2018 以移动平均滤除虚拟手震颤的单被试探索；与多发性硬化、帕金森病的屏幕式视觉反馈研究（Feys et al.、Liu et al.）同属视觉调制震颤的谱系，但首次把 VR 手部视觉反馈操纵用于 ET 患者物理震颤的实验检验，为 TREMOvR 等个性化在线震颤调节路线提供实证起点。',
   'VR 震颤研究与手部追踪设计的双重参考：消费级 MQ3 手部追踪自发衰减震颤频段运动 15.79-22.49 dB 且不妨碍任务完成（该特性可作为震颤研究工具）、8 例 ET 患者伸手类任务物理震颤功率中位降 47%/57%（7/8 例）；患者样本仅 8 例单次会话、多重校正后单项比较未达显著、无触觉反馈与追踪误差可能污染测量，结论外推需更大队列；按用户/任务自适应调节视觉反馈是明确的干预设计方向。'),
 '2610.41680': ('可穿戴触觉步态提示的用户需求设计研究（跨住宅护理与社区场景）', '触觉与多模态', 3,2,3,3,2,2,2, 'C', '',
   '属康复工程 × HCI 的辅助技术设计需求研究线，而非触觉节律刺激的临床疗效线。方法上承接 HCI 的 technology probes 传统与以患者为中心的设计研究（目标期刊即 Disability and Rehabilitation: Assistive Technology）；与 gait cueing/可穿戴触觉反馈文献互补——后者多测步态参数疗效，本文测真实使用需求与照护支持结构。对 XR 中触觉/多模态提示的可用性设计亦有旁证价值。',
   '可穿戴触觉提示系统的设计需求清单参考（七大需求域及其相互冲突：可感知性-位置 vs 可穿戴性-固定、固定节律 vs 地形/疲劳适应、照护者协同配置）；**证据等级 PARTIAL**（ar5iv 仅摘要页、arXiv HTML 404），所有细节未经正文核实；仅服务设计指导、不建立临床疗效，落地前需补正文核验与疗效试验。'),
 '2610.40760': ('Personalised 3D Mnemonics：情境中词汇学习的个性化 3D 助记符', '空间计算与UI', 3,2,1,1,2,2,2, 'C', '',
   '处于 AR 教育与助记符研究交叉线：上游为 Atkinson 关键词记忆法及 VocabulARy（TVCG 2022）的 AR 情境化标注，旁支为 TransPhoner、SmartPhone、LLM overgenerate-and-rank 等自动助记生成与 MnemoMaker、WordCraft 等人机共创，下游对标本团队的 VocabulARy 2.0 demo（ISMAR-Adjunct 2026）。技术上首次把 TRELLIS.2/Meshy 类 2D 引导 3D 生成管线引入助记资产构造，但学术定位是设计概念而非方法突破。',
   '仅入馆不解读（C 级）：概念+故事板短文，无系统实现、无学习效果评估，两条 2D→3D 生成管线示例（Gemini 3 Pro Image+TRELLIS.2 本地、Meshy AI 云端）证明资产生成可行性；作为 AR 教育设计点（object-transforming mnemonics：把熟悉真实物体改造为助记关联本身）有参考价值，待姊妹系统 demo（VocabulARy 2.0）发表后再评估。'),
}

S_BF = {
 '2511.11231': ('DiTGaze：几何条件扩散增强的少样本视线估计', '感知与认知', 3,4,4,5,4,2,3, 'A', '',
   '处于 3D 视线重定向线：STED（2D latent 变换）→ GazeNeRF（CVPR 2023，双流 NeRF）→ GazeGaussian（ICCV 2025，双流 3DGS 加 Eye Rotation Field，本文直接继承的骨干）→ DiTGaze（几何条件 latent DiT 渲染）。上游连接 Gaussian Head Avatar（CVPR 2024，动态高斯头部）与 DMTet/DeepSDF 几何初始化；渲染侧承接 latent diffusion（Rombach et al. 2022）与 DiT（Peebles & Xie 2023），首次将其用于 gaze-controlled 头部重定向。下游沿用 GazeNeRF/GazeGaussian 的 few-shot 协议，与 FAZE（无合成元学习）、Render-to-Adapt（无监督自适应）构成校准策略对照。',
   '眼动追踪校准数据增强的离线工具：1-9 shot 全预算排名第一、N=9 受试级估计误差 5.63°→4.90°（15 个身份中 14 个改善，p<0.001）、平均较 GazeGaussian 降 10.3%、较 real-only 降 31.8%，可直接用于 HMD 眼动仪 per-user 校准的数据扩充；离线生成（191 张需 31.5-36.3 s）不适合实时、无代码、跨域残差大（域内 4.8°→跨域 9.5°）、合成数超 191 后收益饱和是主要限制。'),
 '2602.21535': ('AdaGS：置信门控扩散自适应的无位姿稀疏视图 3DGS 重建', '重建与SLAM', 3,4,4,4,4,3,2, 'B', '',
   'backfill 论文，位于 unposed sparse-view 3DGS 与 diffusion prior 两条技术线的交汇点。位姿侧承接 CF-3DGS（COLMAP-free）、InstantSplat（DUSt3R 初始化）、LongSplat（MASt3R/VGGT）及同组前作 RegGS（ICCV 2025）、OpenGS-SLAM/S3PO-GS 的免 COLMAP 联合优化路线；生成先验侧承接 Difix3D+、3DGS-Enhancer、ViewCrafter、SGD、GaussianScenes 的扩散伪监督思路，但区别于这些工作直接采信生成内容，本文核心贡献在门控而非生成本身。与 AnySplat、ProSplat、Depth Anything 3、DGGT 等 feed-forward 路线互为对照，代表 per-scene 优化系在稀疏无位姿户外场景下的演进。',
   '户外稀疏无位姿 3DGS 重建的幻觉抑制基线：DL3DV/Waymo/KITTI PSNR 24.27/23.76/17.95 与 ATE RMSE 0.077/1.352/2.471，11 基线全面最优；其「artifact amplification loop」形式化与双向置信融合门控可迁移至任何扩散先验重建管线；仅户外驾驶类场景验证（未覆盖室内/动态）、逐场景优化开销大、无代码无数据（自建 1 万余样本 artifact 数据集未公开）是复现门槛。'),
}

def val(s):
    return round(0.20*s[0]+0.20*s[1]+0.15*s[2]+0.15*s[3]+0.15*s[4]+0.08*s[5]+0.07*s[6], 4)

MAIN, BF = [], []
ANNOUNCE_MAIN = {'2610.41496': 'cross', '2610.41671': 'cross'}
EVID = {'2610.41680': ('L1', 'PARTIAL')}
for pid, (tzh, track, imp, nov, tec, exp, per, trl, rep, grade, note, rel, act) in S_MAIN.items():
    d = D[pid]
    lv, ev = EVID.get(pid, ('L0', 'FULL'))
    MAIN.append(dict(id=pid, title='', title_zh=tzh, track=track,
        scores=dict(IMP=imp,NOV=nov,TEC=tec,EXP=exp,PER=per,TRL=trl,REP=rep), grade=grade,
        grade_note=note, evidence=ev, level=lv,
        status='CURRENT', venue=d['venue'],
        announce=ANNOUNCE_MAIN.get(pid, 'new'), tags=d['tags'],
        conclusion=d['conclusion'], problem=d['problem'], method=d['method'], experiments=d['experiments'],
        innovation=d['innovation'], limits=d['limits'], relation=rel, repro=d['repro'], action=act,
        value=val((imp,nov,tec,exp,per,trl,rep)), batch='2026-11-03'))
for pid, (tzh, track, imp, nov, tec, exp, per, trl, rep, grade, note, rel, act) in S_BF.items():
    d = D[pid]
    BF.append(dict(id=pid, title='', title_zh=tzh, track=track,
        scores=dict(IMP=imp,NOV=nov,TEC=tec,EXP=exp,PER=per,TRL=trl,REP=rep), grade=grade,
        grade_note=note, evidence='FULL', level='L0',
        status='CURRENT', venue=d['venue'], announce='replace', tags=d['tags'],
        conclusion=d['conclusion'], problem=d['problem'], method=d['method'], experiments=d['experiments'],
        innovation=d['innovation'], limits=d['limits'], relation=rel, repro=d['repro'], action=act,
        value=val((imp,nov,tec,exp,per,trl,rep)), batch='backfill-1103',
        orig_window='旧稿 replace 再公告（首次入馆）：2511=2025-11 投稿（v2 于 2026-10-29 更新）、2602=2026-02 投稿（v2 于 2026-10-30 更新），2026-11-02 公告批次 RSS 混入'))

# 原始英文标题（RSS）
rss = {json.loads(l)['base_id']: json.loads(l) for l in open('data/raw/2026-11-03.jsonl',encoding='utf-8') if l.strip()}
for p in MAIN + BF:
    p['title'] = rss[p['id']]['title']

MAIN.sort(key=lambda p: (-p['value'], -p['scores']['IMP'], -p['scores']['NOV'], p['id']))
BF.sort(key=lambda p: (-p['value'], -p['scores']['IMP'], -p['scores']['NOV'], p['id']))

# 定稿 Top10：按加权降序取前十（同分 IMP/NOV 降序、赛道多样性优先、id 升序）。
# 4.15 两篇并列（VoxLution 内容生成 / DrawSplat 重建与SLAM，IMP/NOV 均同）→ 赛道多样性优先保留两者（Top10 内均需覆盖），按 id 升序 VoxLution 在前；
# 4.14 两篇并列（MotorSense 评估与数据集 / PGGT-Loc 重建与SLAM）→ 同样按 id 升序 MotorSense 在前。
TOP10_IDS = [p['id'] for p in MAIN if p['grade'] != 'C'][:10]
TOP10 = [p for pid in TOP10_IDS for p in MAIN if p['id'] == pid]

json.dump({'main': MAIN, 'backfill': BF, 'top10_ids': TOP10_IDS},
          open('data/scored_1103.json','w',encoding='utf-8'), ensure_ascii=False, indent=1)
print('main:', len(MAIN), 'bf:', len(BF))
for p in MAIN: print('M', p['id'], f"{p['value']:.2f}", p['grade'], p['track'], p['announce'], p['evidence'], p['title_zh'][:36])
for p in BF: print('B', p['id'], f"{p['value']:.2f}", p['grade'], p['track'], p['title_zh'][:36])
print('TOP10:', TOP10_IDS)
from collections import Counter
print('grades main:', dict(Counter(p['grade'] for p in MAIN)), 'bf:', dict(Counter(p['grade'] for p in BF)))
print('tracks top10:', dict(Counter(p['track'] for p in TOP10)))
print('tracks all:', dict(Counter(p['track'] for p in MAIN)))
print('today_max:', MAIN[0]['value'])
print('saved data/scored_1103.json')
