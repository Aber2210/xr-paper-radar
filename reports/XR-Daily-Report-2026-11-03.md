# XR 每日论文解读报告 · 2026-11-03（11-02 公告批次）

## 一、执行摘要
- **公告日 2026-11-02（周一）≠ 拉取日 2026-11-03（周二 02:30）**——诚实口径：本批处理的是 11-02 公告批次（周末 10-31/11-01 积压于周一 00:00 UTC=08:00 北京时间释放）；API published 口径核验提交日 **10-29×3 / 10-30×8**（均早于公告日，非当日硬提交）。
- **主批 XR 新稿 11 篇（7 A / 2 B / 2 C，无 S 级）**。Top10（**实数 9 篇**，第 10 名候选为 C 级不纳入）：VoxLution 4.15（TUM/UVA，体素进化 3D 室内场景生成，3D-FRONT FPD/FID 较 LT3SD 降 59.6%/51.1%、体素 1.5625 cm）· DrawSplat 4.15（东北大等，Atlanta World 引导隐式高斯 SLAM，Apartment ATE 较次优降 60%、F1 93.7、模型 18.29 MB）· MotorSense 4.14（UMD，100 小时视频-EMG 配对数据集，EK100 动词 +15.86、视频扩散 FVD 373→304）· PGGT-Loc 4.14（中科院，基元接地前馈相机定位，ScanNet 召回 69.0% vs 48.5%、代码开源）· OpenVIO 3.87（首尔国立，统一针孔/鱼眼/360° 的开源 VIO，TUM-VI 单目 ATE 0.377 m 九系统最优、MIT 许可）· PriorGS 3.87（Waterloo，单曝光 HDR 新视角合成，超全部基线约 4-8 dB、单 3090 可复现）· EgoHSI3R 3.85（清华，在线 4D 手-场景交互重建，ARCTIC W-MPJPE 108.80 mm 最优、10.07 FPS）· FoAViS 3.42（哥廷根/McGill，中央凹主动视觉学习注视策略，T=4 ImageNet +4.8 Acc、涌现 IoR）· VR 手部视觉反馈×特发性震颤 3.20（萨拉戈萨，MQ3 追踪衰减震颤频段 15.79-22.49 dB、患者物理震颤功率中位降 47%/57%）。
- **覆盖 6 赛道**：内容生成×1 / 重建与SLAM×3 / 评估与数据集×1 / 神经渲染×1 / 化身与人体×1 / 感知与认知×2（全批 8 赛道）。
- **覆盖度三关**：门① 0.116；门② 6 赛道（≥5，无需重筛）；门③ 4.15 < 4.429（现算，393 条入窗）→ **非重磅日、无 S 级**（全批无 ≥4.2 达线论文）。
- **全文证据**：13 篇候选中 12 篇 L0/FULL（24,878–228,891 字符）+ 1 篇 L1/PARTIAL（2610.41680，摘要级评估并显式声明）。
- **同批 backfill-1103**：RSS 混入旧稿 replace 再公告 2 篇首次入馆（1 A / 1 B，最高 DiTGaze 3.72），详见 [XR-Backfill-Report-backfill-1103.md](XR-Backfill-Report-backfill-1103.md)。

## 二、排行榜（按加权降序）

| 排名 | 论文 | 赛道 | 总分 | 等级 | 证据 | 落后标记 |
|---|---|---|---|---|---|---|
| 1 | VoxLution：体素进化的高保真 3D 室内场景生成（2610.41501） | 内容生成 | 4.15 | A | FULL | — |
| 2 | DrawSplat：Atlanta World 引导的隐式高斯 SLAM 室内重建（2610.41602） | 重建与SLAM | 4.15 | A | FULL | — |
| 3 | MotorSense：视频-EMG 电机感觉表征配对数据集（2610.41127） | 评估与数据集 | 4.14 | A | FULL | — |
| 4 | PGGT-Loc：基元接地的几何 Transformer 前馈相机定位（2610.41833） | 重建与SLAM | 4.14 | A | FULL | — |
| 5 | OpenVIO：支持针孔/鱼眼/360° 的统一开源视觉惯性里程计系统（2610.41671） | 重建与SLAM | 3.87 | A | FULL | — |
| 6 | PriorGS：先验引导的单曝光 HDR 新视角合成（2610.41011） | 神经渲染 | 3.87 | A | FULL | — |
| 7 | EgoHSI3R：第一视角视频的在线 4D 手-场景交互重建（2610.40832） | 化身与人体 | 3.85 | A | FULL | — |
| 8 | FoAViS：中央凹主动视觉系统的学习注视策略分析（2610.41987） | 感知与认知 | 3.42 | B | FULL | — |
| 9 | VR 中改变手部视觉反馈对特发性震颤的探索性研究（2610.41496） | 感知与认知 | 3.20 | B | FULL | — |

## 三、逐篇深度解读

### 第 1 章 · VoxLution：体素进化的高保真 3D 室内场景生成（2610.41501，4.15 A，FULL）

- **赛道 / 场合**：内容生成 / arXiv preprint（慕尼黑工业大学（TUM）与弗吉尼亚大学，cs.CV，2026-10）
- **公告类型**：new
- **一句话结论**：VoxLution 用训练-free 的 resolution-invariant octant coding（ROC）把多分辨率稀疏体素八叉树串行化为单一序列，将室内场景生成转化为 coarse-to-fine 的逐块超分辨率；体素分辨率 1.5625 cm（比现有基线细 41%），3D-FRONT 上 FPD/FID 较 LT3SD 分别降低 59.6%/51.1%，ScanNet++ 上降低 70.5%/73.8%，并可扩展至含噪真实扫描。
- **要解决的问题**：高保真室内场景生成需同时保证全局布局合理与家具级细节丰富，而高体素分辨率下 3D 空间维度灾难严重、表面占空比极低；现有方法要么依赖学习式潜空间压缩（几何过平滑、分辨率受限），要么只能处理完整整洁的合成数据，难以利用真实扫描的稀疏、含噪与不完整特性。核心难点是：如何不按分辨率重训 tokenizer、并原生利用场景稀疏性来扩展生成分辨率。
- **方法详解**：VoxLution 以多分辨率体素八叉树表示场景（体素 25 cm 逐级减半至 1.5625 cm，K=4 级联加粗场景生成器 Φ(0)）。核心 ROC：父体素 8 个子体素占用按 z-y-x 遍历编码为单 token T=Σo_i·2^i，256 项 codebook 跨所有层级共享且训练-free，空间序列长度较逐体素表示缩减 8×。稀疏多分辨率序列化：场景切分为轴对齐 chunk（raster-scan 顺序生成），每块序列由三级粗层条件 S_C(k-3..k-1)、已生成左/后/角邻块的边界条件（共享 GRU 压缩的全局摘要 B_global 加保留 3D 位置信息的 1-ring 局部前缀 B_local）与目标级 token 组成，丢弃空 token；位置编码为层级、空间、类型三类可学习嵌入之和。最后由稀疏 VAE Φ_m（基于 Flexible Dual Grid/SC-VAE 改造，decoder 可预测并增删子占用）预测 dual-contouring 属性以提取三角网格。另支持以语义 bounding box layout（CLIP 文本特征加 Fourier 坐标特征）进行条件生成。
- **实验与结果**：3D-FRONT（5 类房间、19,237 个）与 ScanNet++（过滤后 781 个），80/5/15 划分；基线为 WorldGrow、BlockFusion、LT3SD、微调的 OctGPT 与 Seen2Scene；指标为 FPD（Uni3D 特征）、FID/KID（DINOv2 ViT-B/14）。3D-FRONT：FPD 11.03×10²、FID 2.40×10⁻²、KID 1.49×10²，较 LT3SD 降 59.6%/51.1%/62.6%；ScanNet++：FPD 10.14×10²、FID 1.96×10⁻²、KID 2.08×10²，降 70.5%/73.8%/72.5%；layout 条件生成全面优于 Seen2Scene（FPD 降 31.6%）。单卡 H100 每房间约 22 分钟（级联占约 20 分钟），稀疏化较 dense 提速 20.7×（1,321 s vs 27,335 s，dense 在 level 4 仅完成 38/101 个测试房间）；22 人用户研究总体偏好 84.6%、房间类型识别 90.6%。
- **创新点与贡献**：['提出 ROC：训练-free、分辨率不变的八叉树 token 化，单一 256 项 codebook 跨全部级联层级共享，克服 VQ-VAE 需按分辨率分别训练量化器的限制', '设计稀疏多分辨率 token 序列：chunk 划分加三级粗层条件加邻块边界条件（GRU 全局摘要与 1-ring 局部前缀），实现无缝逐块 coarse-to-fine 超分辨率', '首次把高分辨率场景生成扩展到含噪、不完整的真实扫描（ScanNet++），natively 支持稀疏与部分观测', '构建基于 Flexible Dual Grid 的生成式稀疏 VAE，decoder 可增删体素以补小洞、去除杂散体素', '生成体素分辨率比现有基线细 41%，几何（FPD）与感知（FID/KID）指标同时取得 SOTA，消融验证 ROC、多分辨率序列、稀疏化与级联设计各自不可替代']
- **局限与风险**：仅支持单层室内场景，多层建筑需高度感知的位置编码；级联由 K+1 个独立训练的 transformer 组成，要更细分辨率须新增训练一级而非扩展现有级；在真实数据上继承扫描的孔洞与噪声，场景级几何补全留作未来工作；每房间生成约 22 分钟（未做 KV cache/批化解码等优化），离实用有距；输出为几何网格，不涉及纹理外观生成。
- **与文献库的关系**：位于「3D 几何自回归生成」与「稀疏层次表示」两条技术线的交汇：向上追溯至 PolyGen、MeshGPT 的网格 token 自回归，以及 OctFormer、OctGPT（本文直接基线，被从物体级微调改造到场景级对比）、ShapeFormer 等的八叉树/占用自回归，并受图像域 VAR 的 next-scale 多尺度预测启发；coarse-to-fine 扩散一线（BlockFusion、LT3SD、WorldGrow）与 layout 组合式方法（ATISS、SceneFormer、DiffuScene）为主要对照。与 Scaffold-GS、TRELLIS.2 结构化 latent 路线相比，VoxLution 放弃学习式潜压缩、直接在稀疏体素占用上做序列建模，代表场景级生成中「显式稀疏自回归」的一支。
- **可复现性**：论文提供项目主页 daoyig.github.io/VoxLution/；训练与评价细节披露充分（PyTorch、AdamW、峰值学习率 1×10⁻⁴，GPT-2 decoder 骨干 24 层/1024 维/16 头，每个 transformer 于 4 张 NVIDIA H100 训练约 4 天；mesh VAE 初始化自 TRELLIS.2 的 SC-VAE 预训练权重、在 2 张 RTX A6000 上训练 30K 迭代），但代码与模型权重是否开源原文未述。
- **行动建议**：VR/空间计算室内场景资产生成的即用基线：3D-FRONT FPD/FID 较 LT3SD 降 59.6%/51.1%、ScanNet++ 降 70.5%/73.8%，体素细至 1.5625 cm（较基线细 41%），22 人用户研究总体偏好 84.6%；每房间约 22 分钟（级联占 20 分钟）离实用有距、代码与权重开源情况原文未述需跟进；仅单层室内场景、不含纹理外观，组合纹理生成线（如 TRILLIS.2/Scaffold-GS）可补全。

### 第 2 章 · DrawSplat：Atlanta World 引导的隐式高斯 SLAM 室内重建（2610.41602，4.15 A，FULL）

- **赛道 / 场合**：重建与SLAM / arXiv preprint（日本东北大学、RIKEN AIP、东京大学、中国科学技术大学、萨拉戈萨大学等，cs.CV，2026-10）
- **公告类型**：new
- **一句话结论**：DrawSplat 让显式点线几何先「起稿」结构、隐式神经高斯再「填充」细节，用 Atlanta World 共享重力先验把线诱导结构面转为高斯中心与法向的可微正则；Replica Apartment 上位姿误差较次优基线降 60%（1.09 cm vs MG-SLAM 2.77 cm），ScanNet 渲染 PSNR 提升 2.54 dB（27.07 vs 24.53），并以 18.29 MB 模型、4.5 GB 显存取得高斯 SLAM 中最高 F1（93.7）。
- **要解决的问题**：现有 Gaussian SLAM 在弱纹理、大平面、遮挡、深度噪声与长轨迹的室内场景中，仅靠光度、深度或局部 frame-to-model 约束易产生位姿漂移、表面厚度伪影、法向噪声与结构边界模糊；已有结构先验方法（如 MG-SLAM）未把结构充分接入可微高斯优化，NeRF 先验方法（DenseSplat）则引入额外模型开销。需要一种把显式几何跟踪与隐式高斯建图耦合、同时保持紧凑高效的在线框架。
- **方法详解**：DrawSplat 采用混合 Gaussian SLAM 范式。前端：基于 ORB 点特征加 EDLines 线段（LBD 描述子关联）联合估计位姿，2D 重投影残差加 3D 几何残差（Huber 核）构成 L_T；局部 BA 与 BoW 回环触发的全局 BA 抑制长时漂移；由结构线最小化 L_g(n)=Σω_i·min(|d_i·n|,1-|d_i·n|)（ω_i 为几何可靠度乘语义结构置信度）估计重力方向。后端：anchor-based 隐式高斯——体素化 anchor（分辨率 0.01、32 维特征、每 anchor K=10 个 offset）经轻量 MLP 解码颜色/透明度/旋转/尺度/语义，统一可微渲染颜色-深度-法向-语义四种模态。Atlanta World 结构正则：由跟踪线拟合结构面（方向一致性 e_dir、位置一致性 e_pos、AW 一致性 e_aw），经语义软权重 w_kj 转为高斯位置正则 L_gp=Σw_kj(n_j·P_k+δ_j)²、法向正则 L_gn=Σw_kj(1-|n_k·n_j|) 与平面 AW 项 L_aw；自适应结构采样以线响应 ρ_ℓ、深度梯度 ρ_d、光度残差 ρ_c 构造结构权重，调制 densification 分数 s(x)=||g(x)||·(1+w(x))。地图目标 L_M=L_rgb+λ_d L_d+λ_n L_n+λ_s L_struct+λ_sem L_sem+λ_o L_dist（λ_gp=0.2、λ_gn=0.2、λ_aw=0.1、λ_d=0.4、λ_n=0.1、λ_s=1、λ_sem=1、λ_o=100）。
- **实验与结果**：在 Replica、ScanNet、ScanNet++、Replica Apartment 四数据集对比 SplaTAM、MonoGS、Photo-SLAM、RTG-SLAM、Splat-SLAM、LoopSplat、HI-SLAM2、MG-SLAM、SEGS-SLAM，几何重建另加 NICE-SLAM、Co-SLAM、ESLAM（单卡 A100 40 GB 加 EPYC 7542，5 次平均）。跟踪 ATE RMSE：Replica 0.27 cm、ScanNet 6.52 cm（最优，MG-SLAM 6.77）、Apartment 1.09 cm（最优，MG-SLAM 2.77）。渲染 PSNR：Replica 39.43 dB（最优）、ScanNet 27.07 dB（最优，LoopSplat 24.53）、Apartment 38.79 dB/LPIPS 0.029。几何：Replica Depth L1 0.52 cm、F1 93.7（高斯类最高）；ScanNet Depth L1 4.41（SplaTAM 6.46、LoopSplat 28.88）。效率：跟踪 24.55 FPS、渲染 209 FPS、SLAM 2.02 FPS，显存 4.5 GB 与模型 18.29 MB 为全场最小。
- **创新点与贡献**：['提出 Atlanta World 引导的 Gaussian SLAM：把跟踪线、重力与结构面统一转为高斯原语的可微正则（L_gp/L_gn/L_aw），将 AW 先验首次接入在线增量高斯地图优化', '显式点线跟踪加隐式 anchor-based 神经高斯的混合设计，点线联合在位姿估计上互补，且前端不依赖演化中的外观图', '语义辅助的平面-高斯软关联（w_kj）与自适应结构采样，把高斯容量重分配到墙角、门框、深度不连续等结构信息区', '质量-效率-模型大小的实用平衡：18.29 MB 模型、4.5 GB 显存下达高斯 SLAM 最优 F1 与 PSNR', '消融完整：点/线/全局 BA 组合、平面来源（点诱导 vs 线诱导）、重力来源、各结构损失分量、语义来源（GT vs Mask2Former 预测）均有量化分析']
- **局限与风险**：面向具主导建筑结构的 RGB-D 室内场景，高动态环境、室外或弱 AW 假设空间性能不稳；严重深度误差或不可靠线段会连带损害位姿、重力与平面估计；无法像生成式方法那样补全未观测孔洞；隐式表示带来解码开销，渲染速度（209 FPS）低于高度优化的显式高斯系统（MonoGS 465 FPS）；语义图依赖 Mask2Former 预计算（9.2 FPS，单独计时）；论文未承诺代码开源。
- **与文献库的关系**：处于 Gaussian SLAM 与结构先验 SLAM 的汇合点：承接 SplaTAM/MonoGS 的显式高斯在线建图、LoopSplat 的回环一致性与 SEGS-SLAM 的隐式/结构增强路线，直接对标 Manhattan World 假设的 MG-SLAM（论文指出其结构先验未接入可微优化）、NeRF 先验稠密化 DenseSplat 与预计算位姿的 AtlasGS。相较 ORB-SLAM 点线传统与 NeRF 系（NICE-SLAM、Co-SLAM、ESLAM），它以 3DGS 可微光栅化换实时性，以 Atlanta World（多水平主导方向加共享重力）替代单一 Manhattan 框架以适配多房间布局，是「结构先验 × 隐式高斯」方向在 RGB-D 室内 SLAM 的代表性推进。
- **可复现性**：原文未承诺代码或数据开源；但硬件与实现细节披露完整（单卡 NVIDIA A100 40 GB、AMD EPYC 7542、C++ 前端加 Python/CUDA 后端、Adam、每序列 30K 迭代映射预算、体素 0.01、K=10、特征 32 维、语义用预训练 Mask2Former 预计算、全部损失权重已列），具备复现条件，需自行实现。
- **行动建议**：RGB-D 室内 SLAM 的实用新基线：Replica ATE 0.27 cm、Apartment 1.09 cm 较次优 MG-SLAM 降 60%、ScanNet PSNR +2.54 dB、F1 93.7 高斯类最高、模型 18.29 MB/显存 4.5 GB 全场最小；无代码但硬件与实现细节披露完整可自建复现；室外/高动态/弱 AW 假设空间性能不稳、语义图依赖 Mask2Former 预计算（9.2 FPS）是部署瓶颈，渲染 209 FPS 低于高度优化的显式高斯系统（MonoGS 465 FPS）。

### 第 3 章 · MotorSense：视频-EMG 电机感觉表征配对数据集（2610.41127，4.14 A，FULL）

- **赛道 / 场合**：评估与数据集 / arXiv preprint（University of Maryland, College Park 等，cs.CV，2026-10；含 NeurIPS 论文清单，应为 NeurIPS 投稿）
- **公告类型**：new
- **一句话结论**：MotorSense 发布 100 小时配对 egocentric 视频与双臂 EMG 数据集，CLIP 式传感器运动对齐预训练使冻结视觉 backbone 在动作识别（EPIC-Kitchens-100 动词较最佳基线 +15.86）、3D 手重建（H2O MPJPE 降 4.63 mm）与接触重建（IoU +4.61）上全面超越纯 RGB 自监督，EMG 运动码条件化还将视频扩散 FVD 从 373 降至 304（仅 50M 可训练参数）。
- **要解决的问题**：视觉模型只能从动作的视觉后果学习，看不到产生动作的肌肉活动等具身运动信号，动作结构隐式分布在高维像素流中；而 EMG 提供无遮挡、无标注偏差的稠密替代监督。同时语言、关键点等现有可控生成条件无法描述精细的力与手指构型：语言过于高层、关键点靠近接触时噪声大且不含力信息。作者需要大规模配对数据验证「传感器运动对齐」能否成为比纯视频自监督更强的视觉预训练范式，以及 EMG 能否作为细粒度生成控制信号。
- **方法详解**：采集：每腕佩戴 MindRove Armband（8 通道干电极环状分布、500 Hz、24-bit）+6 轴 IMU（50 Hz），与 Project Aria Gen1/Gen2 眼镜及头戴手机（896×504@30fps）视频同步，共 100 小时厨房/家务无脚本操作；85 条录制标注动作（5,209 段、57 动词、180 名词），57 条手机录制标注手部接触（4,700 区间）。传感器运动对齐：Hiera-B 视频塔（K400-MAE 初始化）与 EMG/IMU 塔（1D 卷积+残差深度可分离块+双向 LSTM）经对称 InfoNCE 对齐至 1024 维共享空间，不做时间池化，批内样本取自同一录制；训练 180 epoch、全局批 328、4×H200。运动码：EMG+IMU 经 VQ-VAE（1.5 s 窗、嵌入 256、码本 64、码率 64 codes/s、λ=0.25）离散化，再以 Video2LoRA 式 HyperNetwork 预测 LoRA 权重条件化冻结的 CogVideoX-Fun I2V 骨干，仅 50M 参数可训。
- **实验与结果**：动作识别（Hiera-B，冻结/端到端）：冻结下全面胜出——EK100 动词 59.85/noun 29.79/action 21.29、SSv2 33.57、Ego-Exo4D 36.11、MotorSense 35.02，较最佳基线分别 +15.86/+5.06/+7.50/+4.40/+8.29/+14.71；同录制的 SimCLR/MoCo/BYOL 基线多数不及 K400-MAE 初始化。3D 手重建（ArcticNet-SF hand-only+ResNet-50）：ARCTIC MPJPE 21.71（-2.58）、H2O 19.65（-4.63）、HOT3D 28.39（-2.46）。接触重建 IoU 55.20±0.62、AUROC 97.19±0.15（较最佳基线 +4.61/+3.83）。视频扩散 FVD 304、LPIPS 0.27、PSNR 22.5，优于 video history 条件（373）与全量监督微调（772，5.57B 参数）。
- **创新点与贡献**：['发布大规模配对 egocentric 视频与双臂 EMG 数据集：100 小时无脚本操作，含动作与接触标注子集，经 IRB、去标识化与选择偏差披露（作者在评审后收窄了「首个」表述，承认 ActionSense 在先）', '提出传感器运动对齐范式：EMG 作为预训练期特权信号、推理期丢弃，冻结表征即在四类动作理解基准全面超越纯 RGB 自监督', '提出无人工标签的 motor codes 离散表征（VQ-VAE，64 codes/s）', '首次以运动码经 HyperNetwork-LoRA 条件化视频扩散，实现细粒度、力感知的操控生成控制', '配套完整预训练消融、局限与伦理/隐私披露']
- **局限与风险**：论文自述：8 通道消费级 EMG 信息有限（商用 16 通道、研究系统可达 128 通道）；参与者少（Aria 仅 8 人）且存在前臂周径选择偏差（与性别、体型相关，细腕易滑脱产生伪影），不代表总体人群；解剖差异影响 EMG 幅度与电极-肌肉对应；跨主体评测仅覆盖运动码预测；活动域迁移（装配、清洁、洗衣）下降幅大于主体迁移；IMU 对快速腕动有稳定作用；egocentric 视频与生理 EMG 存在隐私/生物特征风险。
- **与文献库的关系**：位于具身感知与第一视角理解交叉线：数据侧上承 ActionSense、Ego4D/EPIC-Kitchens 及 FEEL/OpenTouch/TouchScale 等力-触觉数据集，以 EMG 提供更稠密且不遮挡手部的信号；表征侧对标 IMU2CLIP 及音频/触觉/语言对比预训练，把 CLIP 式对齐从视觉-文本/音频扩展到视觉-肌肉信号；生成侧与语言/关键点/音频条件扩散（CogVideoX、MimicMotion 一系）并列，首次引入 EMG 运动码条件并复用 Video2LoRA 轻量控制；下游直接用 ARCTIC/H2O/HOT3D 等手-物基准评测。
- **可复现性**：数据集、训练模型（EMG tokenizer、对齐 backbone、扩散适配器）与训练/评测代码全部公开：项目页 https://www.cs.umd.edu/~edessale/motorsense/ ，匿名仓库 https://anonymous.4open.science/r/MotorSense-7173/ ；附录含采集协议、硬件、预处理、超参与算力（4×H200、RTX A5000）；IRB 批准、每场次 25 美元报酬、EgoBlur 去标识化后按研究用途条款发布。
- **行动建议**：第一视角具身预训练的数据底座（100 小时配对视频-EMG、数据/模型/代码全公开，IRB 与去标识化完备）：EK100 动词较最佳基线 +15.86、H2O MPJPE -4.63 mm、接触 IoU +4.61 全面超越纯 RGB 自监督，EMG 运动码条件扩散 FVD 373→304（仅 50M 可训参数）；8 通道消费级 EMG 信息上限、参与者偏少（Aria 仅 8 人）与前臂周径选择偏差是主要数据局限，egocentric 视频与生理 EMG 的隐私/生物特征风险需按研究用途条款评估。

### 第 4 章 · PGGT-Loc：基元接地的几何 Transformer 前馈相机定位（2610.41833，4.14 A，FULL）

- **赛道 / 场合**：重建与SLAM / arXiv preprint（中国科学院大学人工智能学院/中科院自动化所/北京航空航天大学，cs.CV，2026-10）
- **公告类型**：new
- **一句话结论**：Pggt-Loc 以 DUSt3R 式双分支跨模态 Transformer 把查询图像 patch 直接 grounding 到平面地图基元，单次前馈输出 6-DoF 位姿：ScanNet 上（0.2m,10°）召回 69.0%、中位误差 2.7°/0.14m，较 PlanaReLoc+Refine 三项召回平均相对提升 28.6%，并在最小 layout 模型上以无需穷举渲染与 FoV 先验的方式全面超过 SPVLoc。
- **要解决的问题**：现有相机定位多依赖需昂贵构建、存储与维护的专用地图（structure-based 2D-3D 匹配、mesh/NeRF/3DGS 渲染）；而紧凑且人类可读的高层基元地图（平面表面图、layout 模型）与视觉观测间存在显著 modality gap，潜力未被利用。PlanaReLoc 依赖外置 plane recovery 模块且其三阶段流水线无法用于 minimal layout models；SPVLoc 的 render-and-compare 需穷举采样视点渲染并丢失结构信息。目标：无需显式对应求解或穷举渲染、可泛化到未见环境的 feed-forward 6-DoF 定位。
- **方法详解**：Pggt 继承 DUSt3R 双分支互联 decoder 架构：查询图像经冻结的 DINOv2 ViT-Large patch 化为 l_q 个 patch token；平面基元集合经可训练 primitive embedder（PointNet 3D 编码器 + MLP 平面参数位置编码，每基元采 1024 点）化为 l_m 个 token；每层 cross-attention 实现跨模态交互，query 分支接 Dual-DPT 层（聚合第 2/5/8/11 层 token）产出像素对齐稠密特征。四个预测头：patch-primitive 软分配矩阵（描述子相似度 × 置信度，confidence 超阈值 τ 后取 argmax 赋值）、逐像素平面参数图 P∈R^{3×H×W}（预测 n/d，锚定于 query 坐标系）、逐像素 camera ray 图 R∈R^{6×H×W}（[d;o] 过参数化隐式编码位姿与内参）、prepended camera/map token 直接解码位姿。位姿推断三条通路：Param.-based（用分配矩阵做点对平面 registration）、Ray-based（ray origin 平均得 t、ray direction homography 分解得 q）、Token-based。多任务损失 L=L_assign+L_param+L_ray+L_pose。训练用约 400K query-map pairs（ScanNet/ScanNet++/Matterport3D/MP3D-Habitat，4000+ 场景），N=12 层、l_q=1200、AdamW 峰值 lr 2e-4、125K 迭代、batch 128、8×H20 约 2 天。Layout 任务另加 Semantics Injection（wall/floor/door/window/ceiling 五类语义嵌入 + 辅助分割监督）与 Isolation Injection（房间级 attention mask），在 3250 个 Structured3D layout 上从头训练（每基元 256 点，FoV 45°–135°）。
- **实验与结果**：稠密表面图：ScanNet 测试集 7735 图/303 场景，Ours(Ray) 中位 Δq=2.7°、Δt=0.14m，三档召回 69.0/92.7/95.4%，大幅优于 PlanaReLoc+Refine（3.8°/0.20m，48.5/73.1/81.8%）、PlanaReLoc（37.1/69.8/79.8%）、MeshLoc、MASt3R、MatchAnything、NOPE-SAC、Plana3R、PlaneRecTR++、GeoTransformer、FreeReg；12Scenes 跨域 1023 查询中位 3.6°/0.15m，召回 68.6/90.1/93.8%，基元匹配 F1 76.0%、AP 92.4%。Layout：S3D-official（6405 图/250 场景）中位 2D 误差 11.2cm/0.42°，1m&30° 召回 93.5%，优于 SPVLoc（12.9cm/1.26°，84.2%）；S3D-resampled 90°FoV（3426 图）10cm 召回 56.0% vs SPVLoc 50.1%，120°FoV 91.7% vs 88.0%。消融：去掉 L_assign 或 L_param 明显掉点（62.0→54.7/54.9），语义单独加入反而掉点、与 isolation 联合协同；显式平面参数主要提升细粒度精度；Integrated Rooms 多房间合并随规模扩大召回显著下降。平面恢复副产品 RI 0.94、depth RMSE 0.16，超 PlaneRecTR/ZeroPlane/MoGe-2+RANSAC。
- **创新点与贡献**：['提出 primitive-grounded localization 新概念：把相机定位重新表述为 query 观测对 map 基元的 grounding', 'Pggt 网络直接以图像 patch 与平面基元为输入，单次前馈预测多个定位目标，免除显式对应求解、PnP 与穷举渲染，且不依赖相机内参先验', '同一基座架构统一稠密表面图与最小 layout 模型两类定位任务', '平面恢复与基元匹配作为免费副产品，质量超过单目平面恢复方法', '代码与模型开源（github.com/3dv-casia/PGGT-Loc）']
- **局限与风险**：论文明示：surface map 与 layout 两类任务需分别训练、尚未统一；仅限由平面基元构成的地图，不适合非结构化或非平面场景；主要在房间尺度室内训练，多房间合并地图上召回随规模显著下降，未验证真实大型建筑或室外；失败案例源于运动模糊/低光照、结构细节有限或高度重复模式、无信息查询观测。客观不足：部分案例中 Ray 通路不如 Param.-based；深度估计准确不等于定位成功（重复模式歧义）；全图推理方式限制大规模地图扩展。
- **与文献库的关系**：处于 DUSt3R 式前馈几何 Transformer 与高层地图相机定位两条线的交汇：架构上承接 DUSt3R/MASt3R/VGGT 一系可扩展多视图 Transformer 范式；任务上直接对标并大幅改进同组前作 PlanaReLoc（CVPR 2026，平面基元 region matching，数据管线亦沿用其工作流）与 SPVLoc（ECCV 2024，layout render-and-compare），并与 MeshLoc、F3Loc、LASER 等 render-and-compare 及 GeoTransformer/FreeReg 等 I2P 基线比较。对 XR/AR 谱系而言，它把无纹理、紧凑、可人工编辑的结构地图纳入实时 6-DoF 定位的可选项。
- **可复现性**：代码与模型已开源：https://github.com/3dv-casia/PGGT-Loc ；训练数据由公开数据集（ScanNet、ScanNet++、Matterport3D、Structured3D）按 PlanaReLoc 工作流处理，论文附录 A.1/A.2 给出数据统计与完整实现细节；训练约需 8×H20 GPU 2 天。
- **行动建议**：AR 设备端重定位的前馈新范式：ScanNet（0.2m,10°）召回 69.0%（PlanaReLoc+Refine 48.5%）、中位 2.7°/0.14 m，免显式对应求解/PnP/穷举渲染且不依赖相机内参先验，代码与模型已开源；仅限平面基元构成的地图、多房间合并地图召回随规模显著下降、surface/layout 两类任务需分别训练是落地缺口；与库内 SplitGS-Loc（高斯特征场定位）构成「结构基元 vs 高斯特征场」两条设备端定位路线。

### 第 5 章 · OpenVIO：支持针孔/鱼眼/360° 的统一开源视觉惯性里程计系统（2610.41671，3.87 A，FULL）

- **赛道 / 场合**：重建与SLAM / arXiv preprint（韩国首尔国立大学，cs.RO，2026-10）
- **公告类型**：cross
- **一句话结论**：OpenVIO 是 MIT 许可的滤波器式 VIO，以统一的单位光线相机接口同时支持 pinhole、fisheye 与拼接 360° ERP 图像（单目/双目），完成 EuRoC 与 TUM-VI 全部 31 条序列，TUM-VI 单目平均 ATE 0.377 m 为九个对比系统中最优，并在 PanoAir 全部 17 架次（总长 15.5 km）取得平均 ATE 1.14 m，同时在线估计 ERP 拼接误差与双镜头曝光延迟。
- **要解决的问题**：VIO 已被广泛用于机器人、无人机、AR 与自动驾驶，但既有开源系统（MSCKF-VIO、ROVIO、OKVIS、VINS 系列、SVO Pro、OpenVINS、Basalt、Kimera-VIO）大多只支持 pinhole/fisheye、许可各异（GPL/BSD），无一支持 360° 全景 ERP 输入；而全景相机存在拼接标定误差与前后镜头曝光不同步两类额外误差源。缺少一个许可宽松、用同一估计器覆盖全部相机模型、并对全景误差在线自校的滤波器式 VIO。
- **方法详解**：OpenVIO 采用 MSCKF 加持久 landmark（逆深度参数化）的 EKF：状态含 IMU（姿态/位置/速度/bias）、相机-IMU 时间偏移 t_d、后镜头曝光延迟 δt_b、标定状态 x_cal（相机-IMU 外参加 ERP 拼接误差 k）、历史位姿 clone（默认 20 个）与 landmark（150 个）；IMU 以四阶 Runge–Kutta 传播、协方差用闭式 ACI² 方法与 first-estimate Jacobians；出窗 track 三角化后经 nullspace 投影去点贡献、χ² 门控并 QR 压缩为单次更新。前端为金字塔 Lucas–Kanade 光流加前后向校验加基于单位光线的 RANSAC 旋转拟合外点剔除，按网格配额保留长 track，丢失 landmark 用 NCC patch 在射线切平面采样上重识别（ERP 跨左右接缝连续采样）。初始化按静止/运动自动选择：静止法以陀螺均值定 bias、加速度均值定重力方向与沿重力 bias；动态法先解线性初始化 min‖Az-b‖²（约束 ‖g0‖=g），再以 Ceres 联合精化（Cauchy loss）。360° 扩展在线估计拼接误差 θ'=θ+k·g(θ)（g(θ)=θ(1-(2θ/π)²）与后镜头延迟 δt_b，并以匀速模型预测后曝光位姿。
- **实验与结果**：与 9 个开源 VIO 系统对比（均关回环）：EuRoC（11 条无人机序列，双目 pinhole）单目平均 ATE 0.135 m（最优，OpenVINS/VINS-Fusion 0.160）、双目 0.077 m（次于 Basalt 0.061）；TUM-VI（20 条室内序列，手持双目鱼眼 512×512）单目 0.377 m、双目 0.718 m，均优于 OpenVINS（0.851/1.022）与 Basalt（双目 0.819）；单目与双目配置下 EuRoC 11/11、TUM-VI 20/20 序列全部完成。PanoAir（17 架次，阴天/晴天/夜间，双镜头 ERP 1280×640@30 Hz，RTK-GNSS 真值）全部成功，平均 ATE 1.14 m；15 架次 k 估计落在 0.0055–0.0068，δt_b 除第 10 架次 35 ms（约一帧）外均小于 0.5 ms。
- **创新点与贡献**：['首个以像素到单位光线的统一接口同时支持 pinhole、fisheye 与 360° ERP 的开源 VIO，同一滤波器处理全部相机模型（含相机后方的光线）', '对双镜头 360° 相机在线估计拼接误差 k 与后镜头曝光延迟 δt_b，滤波内以匀速模型预测后曝光位姿', '面向丢失 landmark 的切平面 patch 重识别：容忍透镜畸变与 ERP 拉伸，支持跨 ERP 左右接缝匹配', '静止/动态自动选择的初始化与启动期时间偏移标定（含双镜头偏移差估计），降低人工场景设定依赖', 'MIT 宽松许可加覆盖 EuRoC/TUM-VI/PanoAir 的全序列完成率基准，并导出 keyframe 与特征观测接口供回环扩展']
- **局限与风险**：不含回环检测与地图复用（作者明示，仅提供导出接口）；360° ERP 输入仅支持单目模式；滤波器式估计在长时一致性上通常弱于优化式后端；论文未报告计算耗时/帧率，实时性与资源占用未知；PanoAir 上 k 与 δt_b 无参考真值，在线估计仅作自洽性展示；依赖预先标定的相机-IMU 外参。
- **与文献库的关系**：属于滤波器式 VIO 谱系的系统化延伸：核心估计器是 Mourikis & Roumeliotis 的 MSCKF 结合 Li & Mourikis 的持久 landmark 与逆深度参数化，动态初始化沿用 Geneva & Huang 的视觉惯性 SfM 线性求解加 Ceres 精化框架；对标表中所列九大开源系统（MSCKF-VIO、ROVIO、OKVIS、VINS-Mono/Fusion、SVO Pro、OpenVINS、Basalt、Kimera-VIO），以 360° ERP 支持形成差异化。相对 ORB-SLAM 式点线方案，它以单位光线抽象加 EKF 换取跨相机模型的统一实现与轻量部署，是开源 VIO 基础设施方向的实用贡献。
- **可复现性**：代码以 MIT 许可开源于 github.com/93won/openvio（论文首页即给出地址）；基准使用公开数据集（EuRoC、TUM-VI、PanoAir）与发布配置，重复运行通过缩放 IMU 噪声密度（0.9/1.1）与微调光流终止容差实现（系统本身确定性），复现门槛低。
- **行动建议**：开源 VIO 基础设施的实用贡献（MIT 许可、pinhole/fisheye/360° ERP 统一接口）：TUM-VI 单目平均 ATE 0.377 m 为九系统最优、EuRoC/TUM-VI 全序列完成、PanoAir 17 架次平均 ATE 1.14 m 并在线估计 ERP 拼接误差与双镜头曝光延迟；XR 设备与全景相机追踪的直接可选底座；无回环与地图复用（仅导出接口）、滤波器长时一致性弱于优化式后端、未报帧率是明确缺口，二次开发接回环即可面向产品。

### 第 6 章 · PriorGS：先验引导的单曝光 HDR 新视角合成（2610.41011，3.87 A，FULL）

- **赛道 / 场合**：神经渲染 / arXiv preprint（University of Waterloo，cs.CV，2026-10）
- **公告类型**：new
- **一句话结论**：PriorGS 以伪 HDR 监督、base-gain 高斯表征与 DoRF 先验约束的可学习 CRF 解决无 HDR GT 的单曝光 HDR-NVS，真实场景重曝光 LDR PSNR 24.31/23.00 dB、合成场景 HDR-NVS PSNR 31.22 dB，较全部基线提升约 4-8 dB。
- **要解决的问题**：单曝光 LDR 视图作为唯一直接监督源时，高光裁剪与阴影噪声造成的信息丢失使 HDR 重建在数学上欠约束，缺先验的方法能复现训练曝光却恢复错误辐射度。同时单曝光只能监督 CRF 在有限 unsaturated 区间内的行为，现有 MLP-CRF 泛化差且不保证单调性，启发式固定 CRF 又有响应失配风险。此外逐视图生成的伪 HDR 目标存在跨视图不一致，直接编码为高斯颜色会引发严重颜色与几何伪影。
- **方法详解**：PriorGS 基于 3DGS，每个高斯携带两组 RGB SH 系数：β^c 编码 LDR base 颜色、β^g 编码 log-gain，HDR 辐射度 h=(l+δ)⊙2^g−δ（δ=1/64，l 为反 gamma 线性值），同一几何分别渲染 LDR base 与 HDR 视图。训练前用 2D 单曝光 HDR 方法（主选 IntrinsicHDR）为每个训练视图生成伪 HDR 目标施加先验。CRF 为 f(E)=t(η(E))：t(x)=(1+σ)x^n/(x^n+σ) 取 DoRF 201 条曲线平均响应的双参数单调近似，η(E)=sigmoid(a·ln(E+ε)+b) 为可学习软归一化，逐场景学习四参数、RGB 三通道共享、构造上严格单调；拟合 DoRF 平均 MSE 2.081e-5（较双参数响应降 63.6%）。闭环重建要求 HDR 渲染经 CRF 重曝光后匹配输入 LDR；总损失 L=L_base+0.5L_HDR+0.5L_ReExp（HDR 项 μ-law 压缩，μ=5000）。base-gain 表征另支持以系数 ρ 缩放 gain field 做视图一致的 3D HDR 外观编辑。
- **实验与结果**：在 HDR-NeRF（4 真实+8 Blender 合成）与 HDR-Plenoxels（4 真实）按单曝光协议评测：每场景 5 个曝光、只训 1 个、其余 4 个做重曝光并取平均；18 训练/17 测试视图（HDR-NeRF）、27/13（HDR-Plenoxels）。真实场景重曝光 PSNR 24.31/23.00 dB、SSIM 0.9248/0.9021、LPIPS 0.064/0.092，超 GaussHDR（16.28/17.73）与 SeHDR（13.75/14.21）约 7-8 dB；合成 HDR-NVS PSNR 31.22 dB（基线最高 26.96）、重曝光 22.96 dB（基线最高 15.76）。消融：去先验跌至 18.39；直接编码在 HDR-Plenoxels 跌至 15.05；固定 gamma CRF 跌至 14.87。训练曝光处 LDR-NVS 亦最优（真实 36.10 dB），且对 4 种 2D HDR 方法均鲁棒。
- **创新点与贡献**：['首次把学习式 LDR-to-HDR 重建先验以伪 HDR 监督引入单曝光 HDR-NVS，并实验证明其对欠约束问题的必要性', '提出 3D base-gain HDR 表征（LDR base+3D gain field），把 2D LDR-gain 格式扩展到 3D，缓解跨视图伪 HDR 不一致', '提出 DoRF 先验约束的可学习 CRF：构造上严格单调、监督区外响应合理且保留逐场景适应性，附容量分析与单调性证明', '构建 LDR base→HDR→重曝光 LDR 闭环，在两端锚定输入 LDR 观测', '展示 3D HDR 外观编辑新应用：缩放 gain field（ρ=0-1.5）实现视图一致的动态范围扩展']
- **局限与风险**：论文自述：受 2D HDR 重建方法质量限制，伪 HDR 目标中丢失纹理恢复不佳会拖累重建；跨视图不一致仍可能被编码为虚假视角相关外观。客观看：数据集小（每数据集 4-8 个场景）且仅静态场景；真实场景性能对所选 2D HDR 方法敏感（GMNet 变体在 HDR-Plenoxels 的 PSNR 不及 GaussHDR）；HDR 指标依赖逐场景亮度校正与 μ-law 协议；伪 HDR 按全场景最大辐射度归一化引入额外假设。
- **与文献库的关系**：位于 HDR-NVS 主线：从多曝光的 HDR-NeRF/HDR-GS/GaussHDR 到单曝光的 SeHDR、Mono-HDR-GS 演进线，直接对标这两个同期单曝光工作。其伪 HDR 先验承接 2D 单曝光 HDR 重建（Eilertsen、IntrinsicHDR 一系），base-gain 表征对应 2D 域 LDR-gain 格式（ISO 21496-1、Ultra HDR、Gain-MLP），CRF 先验源于 DoRF 数据库与 Eilertsen 双参数近似，是把 2D 逆色调映射知识系统迁移进 3DGS 框架的代表工作。
- **可复现性**：实现基于公开的 HDR-GS 代码，使用公开 HDR-NeRF/HDR-Plenoxels 数据集与公开 IntrinsicHDR；作者声明发表后将在 GitHub 公开实现；单张 RTX 3090（24GB）可复现全部实验；CRF 初始化（DoRF 平均响应）与超参见附录 A.3。
- **行动建议**：沉浸式 HDR 内容生产（虚拟制片/HDR 显示）的单曝光 3DGS 重建基线：真实场景重曝光 PSNR 24.31/23.00 dB、合成 HDR-NVS 31.22 dB，较全部基线提升约 4-8 dB，并支持 3D HDR 外观编辑（gain field 缩放）；单张 RTX 3090 可复现全部实验、实现基于公开 HDR-GS 代码、承诺发表后开源；数据集小（每数据集 4-8 场景）、性能对所选 2D HDR 方法敏感（GMNet 变体在 HDR-Plenoxels 不及 GaussHDR）、μ-law 协议依赖逐场景亮度校正是复现选型注意点。

### 第 7 章 · EgoHSI3R：第一视角视频的在线 4D 手-场景交互重建（2610.40832，3.85 A，FULL）

- **赛道 / 场合**：化身与人体 / arXiv preprint（清华大学，cs.CV，2026-10）
- **公告类型**：new
- **一句话结论**：EgoHSI3R 以 CUT3R 循环场景表征为底座，融合 WiLoR 手部先验与交互感知接触建模，用单一在线前馈网络联合恢复相机运动、稠密场景几何、世界空间双侧 MANO 手与逐顶点接触，在 ARCTIC 取得最优 W-MPJPE 108.80 mm（较最强基线 StableHand 降 15.79 mm），端到端 10.07 FPS。
- **要解决的问题**：第一视角视频蕴含丰富手-物交互信息，但相机系方法只恢复相机坐标系手姿而无世界坐标位置，世界空间方法靠外部 SLAM 估相机轨迹却不重建场景几何、不建模接触，两者都不完整。把专用预测拼成完整 4D 重建通常需要逐序列离线优化，难以满足机器人示教、人机协作等在线更新场景；且独立估计的手与场景常出现浮空手或穿模，需在预测阶段本身建模手-场景空间关系。
- **方法详解**：EgoHSI3R 以 CUT3R 循环场景状态为底座（持久累积几何与相机证据，提供共享世界空间与尺度），把 WiLoR 裁剪式手部先验（M=18 token：16 姿态+形状/全局平移）注入解码器。Hand Prompt Builder 用在线检测框经 RoIAlign 提取局部场景特征并池化为上下文，以特征门控 g=σ(φ_g([q;s])) 融合：P=φ_mix(q+g⊙s)，缺失手用学习 mask token 保持固定双手布局。Interaction-Aware Contact Builder 以固定 MANO skinning 矩阵 W∈R^{778×16} 把 16 个关节 token 传播到 778 个顶点，顶点查询对同框场景上下文做多头交叉注意力输出接触概率，并经门控 α 残差反馈精化手部 token，形成接触→手闭环。训练损失 L=L_rec+L_MANO+0.3(L_focal+0.1 L_part)，MANO 项含参数、相机系、腕相对与 2D 重投影监督。
- **实验与结果**：训练用 HOT3D、ARCTIC、TACO、H2O、HOI4D、DexYCB 六个第一视角手-物数据集（接触标签按 1 cm 几何阈值生成）。世界空间手重建（ARCTIC，150 帧片段）：W-MPJPE 108.80 mm、WA-MPJPE 25.82 mm 均最优，较 StableHand 降 15.79/6.84 mm；相机系（p-free 协议）PA-p 7.025（ARCTIC）/6.312 mm（HOT3D）最优；接触估计（ARCTIC/DexYCB）precision 52.15/51.62 超 HACO，但 recall 45.02/50.38 偏低；H2O 场景重建 Abs Rel 0.027、δ<1.25 0.993 最优。消融：WiLoR 微调使 ARCTIC MPJPE 22.916→19.952 mm，接触反馈再降 W-MPJPE 4.495 mm。效率：端到端 10.070 FPS、峰值显存 6.650 GiB、参数 1470.25M。
- **创新点与贡献**：['首个在线、前馈、无测试时优化的统一 4D 手-场景交互重建框架，一次前向同时输出相机、稠密场景、世界空间双手与逐顶点接触', '统一循环场景表征为手与场景提供共享世界空间和尺度，从预测本身缓解浮空手/穿模不一致', 'Hand Prompt Builder 以 RoIAlign+特征门控把参数化手先验注入循环重建，兼顾先验结构与局部场景上下文', '基于 MANO skinning 矩阵的顶点级接触查询与交互感知残差反馈，把接触建模闭合进手-场景推理环', '在六个第一视角手-物数据集上联合训练，并在手重建、场景重建、接触、效率四类评测上系统验证']
- **局限与风险**：论文自述：因果推理无法做未来帧平滑，AccEr（16.91）与 MRRPE（120.77 mm）偏高；时间抖动高于专做运动平滑的方法；接触 recall 低、预测偏保守；手重建与接触联合训练存在优化不稳定。客观看：WiLoR 先验原本只针对右手；接触标签为几何距离生成而非力或人工标注；参数 1470.25M 偏大；代码尚未发布。
- **与文献库的关系**：位于前馈几何基础模型线（DUSt3R/VGGT→Spann3R/SLAM3R/CUT3R 的序列化路线）与第一视角手部重建线（HaMeR/WiLoR 相机系，HaWoR/Dyn-HaMR/StableHand 世界空间系）的交叉点，并首次把稠密接触估计（HACO、ContactPose 一系）纳入统一前馈框架；与 MINT（相机+手轨迹）、UniSH/Human3R（第三人称 SMPL）互补，对标并超越 HaWoR、StableHand、HandFlow 等世界空间方法。
- **可复现性**：原文称「正在准备代码公开」（preparing the code for public release），截至撰写时未发布，未承诺数据集开源；实验设置、数据划分、训练细节与硬件（单卡 NVIDIA H200）在正文与附录给出，项目页 https://pmz-enterprise.github.io/egohsi3r-page/ 。
- **行动建议**：具身/XR 手-场景交互理解的在线重建底座：ARCTIC W-MPJPE 108.80 mm 最优（较 StableHand 降 15.79 mm）、端到端 10.07 FPS、峰值显存 6.65 GiB，可作 VR 遥操作/第一视角助手的实时手-物状态估计上游；接触 recall 偏低（45-50%）、参数 1470M 偏大、无未来帧平滑（AccEr 16.91 偏高）、接触标签为几何距离生成而非力标注、代码尚未发布是主要缺口。

### 第 8 章 · FoAViS：中央凹主动视觉系统的学习注视策略分析（2610.41987，3.42 B，FULL）

- **赛道 / 场合**：感知与认知 / arXiv preprint（德国哥廷根大学/马普动力学与自组织研究所、加拿大 McGill 大学与 Mila 等，cs.CV，2026-10）
- **公告类型**：new
- **一句话结论**：FoAViS 以 log-polar foveation + 64×64 二维空间 LSTM 记忆 + 与任务并发训练的注视策略，在 4 个基准上全面超过随机位置训练（T=4 时 C-MNIST +8.8%、ImageNet +4.8% Acc，ADE20K +2.5、COCO-Stuff +1.7 mIoU），且即便给随机训练模型喂学习到的 scanpath 也无法追平——同时涌现出任务特异的注视分布与无显式监督的 inhibition of return。
- **要解决的问题**：生物视觉是中央凹化且主动的，但已有 active vision 模型在设计轴上各有缺失：foveation 多用矩形 crop 或 patch pyramid 而非偏心依赖的分辨率衰减；记忆常抹平空间结构或受低分辨率/低容量限制；注视策略多为启发式或冻结的任务模型。缺乏一个统一框架同时具备类脑 foveation、显式 spatiotopic 记忆、全局与稠密任务支持、以及与任务并发训练的可学习注视策略，因而难以在受控条件下系统研究注视行为（如 IoR 的涌现）。
- **方法详解**：FoAViS 自回归展开 T 步，每步五组件：log-polar foveation 以当前注视点为中心，将图像采样到固定 R×A=64×64 网格（ρ_t=log√(x_c,t²+y_c,t²)、α_t=atan2(y_c,t,x_c,t) mod 2π，角度与 log 半径均均匀，最大半径=图像边长 S，双线性插值共 4096 点）；Res-UNet backbone（4 阶段编码器通道 64 起、解码器全程 128 通道）提取特征后逆 log-polar 变换回图像坐标系，写入 64×64×128 的 per-position LSTM 记忆 H_t=LSTM_θ(H_{t-1},F_t)，未覆盖网格置零；policy head（3 个 128 通道卷积 + 1×1 卷积）输出 64×64 概率图 π_θ(·|H_t)=softmax(ψ_θ(H_t))，采样下一注视点；task head 全局卷积+pooling+MLP（分类）或 1×1 卷积上采样（分割）。训练目标 L=L_task+L_policy：任务为每步交叉熵；奖励定义为任务损失下降 r_t=CE(ŷ_t)−CE(ŷ_{t+1})，按批内逐步标准化；策略损失 -Σ sg[r̃_t]·log π_θ(f_{t+1}|sg[H_t])，对奖励与记忆施加 stop-gradient，使策略梯度只更新 policy head。首次注视固定图像中心，T=4，测试用 argmax 确定性评估。
- **实验与结果**：数据集：ImageNet、C-MNIST（自制 10 类）、ADE20K（150 类）、COCO-Stuff（171 类），T=4 glimpses、3 个随机种子。原生评估：learned-policy 模型 C-MNIST 99.4%、ImageNet 68.5%、ADE20K 24.3 mIoU、COCO-Stuff 24.9 mIoU，全面优于 random-location 模型（90.6/63.7/21.8/23.2）；单 glimpse 两者相当；T=6 继续上升（ImageNet 69.4）。passive 全图基线（128×128 单次前馈）仍更强（ImageNet 70.5、ADE20K 30.7、COCO-Stuff 29.7），分割差距更大。策略迁移：random-location 模型 + ImageNet 学习策略 66.3%，仍低于并发训练模型 68.5%；learned-policy 模型改用他策略普遍掉点（ImageNet 65.3–66.7%），显示 backbone 特化于自身策略诱导的输入分布。扫描路径分析：任务/数据集特异的累积注视分布、水平/垂直 saccade 偏向、180° 反转偏向、涌现 IoR（注视后 logits 骤降再部分恢复）；但缺少人类式的 saccade 幅度负自相关。stop-grad 消融显示去掉后任务性能显著下降、熵正则仅能部分恢复。
- **创新点与贡献**：['首个（作者所称）同时具备类脑 foveation、显式高分辨率 2D 空间记忆、可学习注视策略、并发策略-任务训练且支持全局+稠密任务的主动视觉系统', '64×64 spatiotopic 记忆（per-position LSTM）使分类与分割无需任何架构改动即可切换', '以任务损失下降定义奖励并做批内逐步标准化的策略梯度训练配方', '实证发现表征-策略并发共适应优于「随机位置训练 + 测试期策略迁移」', '系统记录学习策略的 scanpath 统计并与人类（MIT1003）对照，报告无监督涌现的 inhibition of return', '揭示 joint task-policy 优化的 stop-grad 不稳定性问题及其缓解']
- **局限与风险**：论文明示：Res-UNet 仅约 13.5M 参数、从头训练、低算力预算，绝对性能落后于大模型/蒸馏特征方法（AdaptiveNN、CanViT）；log-polar 采样仅定性近似视网膜且牺牲局部等距性；模型无时间概念（每个 glimpse 计算量相同、无 fixation duration）；glimpse 严格自底向上编码、无 top-down 反馈；2D 记忆面向静态场景；未反映皮层分区；与人类行为仍有差异（无 saccade 幅度负自相关、saccade 幅度系统性偏大）。与 passive 基线差距明显（分割任务低 4.8–6.4 mIoU）；joint optimization 去 stop-grad 后训练不稳定。
- **与文献库的关系**：位于 RAM（Mnih et al. 2014）/DRAM 开创的深度主动视觉线与计算神经科学 gaze 模型线的交汇处。论文以系统比较 20 余个模型，直接对标 CanViT（Berreby et al. 2026，高分辨率 canvas 记忆但仅随机位置加熵启发式）、GVSM、AdaptiveNN、AdaGlimpse、TORE、Saccader 等；foveation 沿用 Lukanov et al. 2021 的 log-polar 方案；理论上连接 normative gaze 传统（Najemnik & Geisler 理想观察者）与数据驱动 scanpath 模型（Kümmerer/Bethge、DeepGaze III）。对 XR 注视点渲染谱系，它提供可学习注视策略的类脑对照系统。
- **可复现性**：原文未承诺代码/模型开源（全文未给出仓库链接）；实验基于公开数据集（ImageNet、MNIST/EMNIST、ADE20K、COCO-Stuff）与自制 C-MNIST（生成流程见附录 B）；训练在单张 A100/H100 GPU 上分别约 3 天（ImageNet）、2 天（分割）、20 小时（C-MNIST），附录 A.1/A.3 给出架构与超参细节。
- **行动建议**：中央凹渲染/眼动研究的类脑参照系：并发策略-任务共适应全面超随机位置训练（T=4 ImageNet +4.8 Acc、C-MNIST +8.8%）、涌现无监督 inhibition of return、scanpath 统计与人类（MIT1003）对照；绝对性能仍明显落后 passive 全图基线（分割低 4.8-6.4 mIoU）、13.5M 小模型无代码、log-polar 仅定性近似视网膜，作为注视策略先验用于 foveated rendering 调度需先解决 passive 差距与 stop-grad 训练不稳定问题。

### 第 9 章 · VR 中改变手部视觉反馈对特发性震颤的探索性研究（2610.41496，3.20 B，FULL）

- **赛道 / 场合**：感知与认知 / arXiv preprint（西班牙萨拉戈萨大学 I3A/BSICoS 组、马德里 12 de Octubre 大学医院神经科、CIBERNED 等，cs.HC，2026-10）
- **公告类型**：cross
- **一句话结论**：Meta Quest 3 原生手部追踪可使视觉呈现的震颤频段（3–9 Hz）运动衰减 15.79–22.49 dB 而不妨碍全部 6 项日常任务完成；在 8 例特发性震颤（ET）患者中，伸手类任务（指鼻、用勺进食）的物理震颤频段功率在 VR 中分别中位降低 47% 与 57%（7/8 例患者），效应强烈依赖任务类型与个体。
- **要解决的问题**：病理性震颤（ET 频率 4–12 Hz，影响约 0.9% 人口、65 岁以上约 5.79%）机制未明且治疗常不充分；视觉反馈是调节震颤表达的重要传入通路（提高视觉增益可放大 ET 震颤幅度），但真实世界中手的视觉运动与物理运动天然耦合、无法单独操纵。VR 可将二者解耦，本研究要回答：在 VR 中视觉抑制手的非自主高频成分，能否反过来影响其物理表达，并验证消费级头显能否可靠复现日常手部任务范式。
- **方法详解**：基于 Meta Quest 3（Unity 6000.1.9f1，单眼 2064×2208、110°×96° FOV、120 Hz）搭建客厅场景，受试在匹配的 VR 与真实世界（RW）条件下完成 6 项借鉴 TETRAS/FTMTRS 量表的日常任务（姿势保持 30 s、捏持移杯、指鼻、全手握杯移动、用勺进食、持手机 30 s），条件顺序 counterbalanced。震颤带功率用独立于头显的 x-IMU3（100 Hz）测量，视觉衰减量化为 10·log10(P_MQ3/P_IMU)；患者实验加测 ECR/FCR 双 32 通道 HDsEMG（2000 Hz）。健康人实验以 FES（50 Hz 载波、400 μs 脉宽，FCR 9.2±2.2 mA、ECR 14.2±3.7 mA）诱导 4–8 Hz 模拟震颤。统计用 Wilcoxon signed-rank、Friedman 检验、Holm 校正与 Kendall's W。
- **实验与结果**：实验一（15 名健康受试：8 女 6 男 1 非二元，22–40 岁，均值 28.4±5.38）：FES 使 IMU 震颤功率升高 1.98–7.76 dB（各任务 Holm 校正后 p≤.025），而 MQ3 视觉表征衰减 15.79–22.49 dB（用勺最小、捏持最大，均 p<.001），VR 与 VR-FES 的头显端功率无显著差异；全部任务成功完成，SSQ 无显著升高，NASA-TLX 仅 VR-FES 负荷偏高（总体 4.33 vs RW 1.67）；捏持与握杯任务 VR 完成时间显著变长（44.64→73.30 s、44.18→82.54 s）。实验二（8 例 ET：58–85 岁，68.8±10.6）：指鼻与用勺的 VR/RW 陀螺仪震颤功率中位比 0.528、0.427（均 7/8 例降低，Holm 校正后未达显著，指鼻 p_Holm=.094）；四任务分组比较显著（χ²(3)=11.10，p=.011，W=.463），reaching 组 0.475（8/8 降低）优于 fine interaction 组 1.115（4/8）；EMG 趋势一致且 ECR 功率与陀螺仪强相关（Spearman ρ=.964，p=.0028）。
- **创新点与贡献**：['首个在真实 ET 患者中检验「视觉抑制震颤能否改变其物理表达」的发表研究，填补 hand redirection 文献在病理震颤方向的空白', '设计并验证可在 VR/RW 间匹配比较的 6 任务日常手部范式，任务集源自 TETRAS 与 FTMTRS 临床量表', '量化消费级 MQ3 手部追踪对高频非自主运动的自发衰减（约 16–22 dB 且任务依赖），提示该特性可作为震颤研究工具', '联合 IMU 运动学与 HDsEMG，发现 VR 中震颤运动学的改变伴随 tremorgenic 神经驱动变化，而非仅视觉表征变化', '揭示强任务依赖（reaching 类降低、fine interaction 类反升）与个体异质性，提出按用户自适应调节视觉反馈的干预方向']
- **局限与风险**：患者样本仅 8 例、单次会话，统计效力与可推广性受限，无法评估纵向适应效应；VR 无触觉反馈、追踪误差与执行速度差异可能污染测量；MQ3 原生追踪滤波为专有系统、参数不可控；单项比较经多重校正后均未达显著；论文明示未确立任何临床或治疗收益，需更大队列与更精确的视觉操纵控制。
- **与文献库的关系**：处于「感知反馈操纵」与「神经运动障碍康复」的交叉线：上游承接 redirected walking 与 hand redirection（Zenner & Krüger、Steinicke 组等）关于视觉-运动差异可被不被察觉地操纵的结论，以及 Cohn et al. 2018 以移动平均滤除虚拟手震颤的单被试探索；与多发性硬化、帕金森病的屏幕式视觉反馈研究（Feys et al.、Liu et al.）同属视觉调制震颤的谱系，但首次把 VR 手部视觉反馈操纵用于 ET 患者物理震颤的实验检验，为 TREMOvR 等个性化在线震颤调节路线提供实证起点。
- **可复现性**：原文未承诺代码或数据开源；装置为商用 Meta Quest 3、x-IMU3 与 Muovi HDsEMG，任务演示视频见补充材料，复现需自行搭建 Unity 场景、FES 刺激与信号处理管线（论文对带通滤波、PSD 估计与统计检验有完整参数描述）。
- **行动建议**：VR 震颤研究与手部追踪设计的双重参考：消费级 MQ3 手部追踪自发衰减震颤频段运动 15.79-22.49 dB 且不妨碍任务完成（该特性可作为震颤研究工具）、8 例 ET 患者伸手类任务物理震颤功率中位降 47%/57%（7/8 例）；患者样本仅 8 例单次会话、多重校正后单项比较未达显著、无触觉反馈与追踪误差可能污染测量，结论外推需更大队列；按用户/任务自适应调节视觉反馈是明确的干预设计方向。

## 四、当日全量 7 维度对比表（参考）

见 [`papers/daily/2026-11-03/7dim-table.md`](../papers/daily/2026-11-03/7dim-table.md)。

## 五、覆盖率校验与筛选过程说明

- 门①（同质去重）：最大 Jaccard 0.116 < 0.62，通过，无同质重复。
- 门②（赛道覆盖）：定稿 Top10 覆盖 6 赛道（≥5），通过；全批 8 赛道，纯值排序即满足，未触发重筛。
- 门③（价值天花板）：当日最高分 4.15 < 库内近 30 天 Top10 均分 4.429（现算，393 条入窗）→ 非重磅日、无 S 级，未拔高、未凑数；本批无论文达 S 线（≥4.2），按实数定级。
- Top10 实数说明：按加权降序第 10 名候选为 2610.41680（2.50 C 级，PARTIAL 证据），依「C 级仅入馆不解读」原则不纳入 Top10——**低量日不凑数**。
- 三关均未触发重筛；OUTDATED/SUPERSEDED 0 篇。


## 六、附录：证据等级分布与抓取记录

- FULL 9 篇；PARTIAL 0 篇；ABSTRACT_ONLY 0 篇。
- 抓取降级：2610.41680 L1/PARTIAL（arXiv HTML 404 + ar5iv 仅摘要页 5,660 字符，按摘要级评估并显式声明，未脑补正文细节）；其余 12 篇 L0/FULL。无 L5、无 OCR、无伪造；串行 3s/篇，无限流。
