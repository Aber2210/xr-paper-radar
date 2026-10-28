# XR Backfill 补录报告 · backfill-1029（旧稿再公告）

## 一、执行摘要
- **批次性质**：backfill（非当日新提交）——10-28 公告批次中 RSS 混入的旧稿 replace/cross 再公告 4 篇，首次入馆；原始投稿 2508=2025-08 / 2510=2025-10 / 2604=2026-04 / 2605=2026-05。
- **补录 4 篇（3 A / 1 B）**：LoBE-GS 3.73（NTHU+NVIDIA，负载均衡大规模 3DGS 训练，端到端约 2.9×）· AmaraSpatial-10K 3.67（10,071 个度量锚定 3D 资产，CLIP R@5 3.4×）· VolFill 3.65（UMass Amherst，体素流匹配 amodal 重建，SCRREAM CD 3.03）· PIS3R 3.58（VGGT 深度重建的超大视差拼接，Sampson 误差约 3.1×）。
- **覆盖 4 赛道**；门① 0.143；门③ 对 backfill 不适用；OUTDATED 0。
- **诚实口径**：全部条目 `batch=backfill-1029` + `orig_window` 标注，绝不混入「当日新论文」。

## 二、排行榜（按加权降序）

| 排名 | 论文 | 赛道 | 总分 | 等级 | 证据 | 落后标记 |
|---|---|---|---|---|---|---|
| 1 | LoBE-GS：负载均衡的高效大规模 3DGS 训练（2510.01767） | 系统与平台 | 3.73 | A | FULL | — |
| 2 | AmaraSpatial-10K：空间计算与具身 AI 的 3D 资产数据集（2604.23018） | 评估与数据集 | 3.67 | A | FULL | — |
| 3 | VolFill：体素流匹配的单图 amodal 场景重建（2605.31466） | 重建与SLAM | 3.65 | A | FULL | — |
| 4 | PIS3R：深度 3D 重建的超大视差图像拼接（2508.04236） | 重建与SLAM | 3.58 | B | FULL | — |

## 三、逐篇深度解读

### 第 1 章 · LoBE-GS：负载均衡的高效大规模 3DGS 训练（2510.01767，3.73 A，FULL）

- **赛道 / 场合**：系统与平台 / arXiv preprint（cs.CV，v2 公告于 2026-04-10；作者署名 National Tsing Hua University 与 NVIDIA AI Technology Center (NVAITC)；旧稿 replace 再公告首次入馆；未声明会议录用）
- **公告类型**：replace/cross（旧稿 replace/cross 再公告（首次入馆）：2508=2025-08 投稿、2510=2025-10 投稿、2604=2026-04 投稿、2605=2026-05 投稿，2026-10-28 公告批次 RSS 混入）
- **一句话结论**：提出以负载均衡 KD 树划分、深度反投影快速相机选择、可见性裁剪与选择性致密化为核心的 3DGS 大规模训练框架 LoBE-GS：端到端训练时间较使用 coarse model 的基线快至 2 倍（MatrixCity-Aerial 1:13 vs CityGS 3:31，约 2.9×；Building 0:55 vs 2:26），划分时间从小时级降至分钟级，同时 PSNR/SSIM 持平或更优。
- **要解决的问题**：将 3DGS 扩展到城市级无界场景时，divide-and-conquer 方法存在两个瓶颈：均匀或启发式划分不反映真实计算需求，块间负载严重失衡，最慢块（straggler）主导总训练时间形成长尾；coarse-to-fine 流水线对 coarse 阶段利用不足，且相机分配需对 M 个块 × N 个相机逐一投影渲染，可占端到端运行时近一半、耗时达数小时。
- **方法详解**：三大组件：①负载均衡 KD 树场景划分，叶子即 M 个训练块，节点工作量估计为相机数 L(ℬ^(b))=|𝒞^(b)|；按 AABB 最长边选切分轴、以粗 Gaussian 中心投影中位数初始化切位，best-first 策略每次分裂 workload 最大的叶子；cutline refinement 以 minimax 目标 J(q)=max(L(ℬ_L(q)), L(ℬ_R(q))) 在 q∈[0.1, 0.9] 内做 3 步二分搜索，直接压低最重子块。②快速相机选择（FCS）：每相机仅做一次 α-blending 深度合成 D=Σ d_i α_i Π_{j<i}(1-α_j) 并反投影为 3D 点，按块内可见比例 V_{c,b}=(1/N_p)Σ 1[p_{c,k}∈ℬ^(b)] ≥ τ=0.1 分配相机，划分时只重分配父块已有相机。③可见性裁剪（VC）每块仅保留至少一个分配相机可见的 Gaussian；选择性致密化（SD）仅允许块内 Gaussian 参与 densification，块外 Gaussian 仍参与渲染监督但不繁衍新 Gaussian。并行细训一 GPU 一块、块间无通信，无需 NVLink 类紧耦合基础设施。
- **实验与结果**：数据集：MatrixCity-Aerial（宽 1600 px，36 块）、Mill19 Building（20 块）与 Rubble（9 块）、UrbanScene3D Residence（20 块）与 Sci-Art（9 块），真实数据集统一 4 倍降采样。基线：CityGS、VastGS†（无外观建模）、Grendel-GS（4×L40、200k 迭代）、3DGS†（60k 迭代）。标准指标（Table 1）：MatrixCity-Aerial 27.69/0.875/0.185 vs CityGS 27.46/0.865/0.204，Building 22.13/0.790/0.231 vs 21.55/0.778/0.246，其余场景与 CityGS 相当且 LPIPS 多数更优、#GS 相当。颜色校正指标（Table 2）对 VastGS† 全面占优：Aerial 28.88/0.880/0.183 vs 28.33/0.835/0.220，Residence 22.95/0.816/0.208 vs 21.01/0.699/0.261，Building 22.97/0.786/0.235 vs 21.80/0.728/0.225。运行时（Table 3，hh:mm）：T_E2E 分别 Aerial 01:13（CityGS 03:31）、Residence 00:55（02:36）、Rubble 00:49（02:29）、Building 00:55（02:26）、Sci-Art 00:38（01:35）；T_partition 由 CityGS 的 01:39/00:31/00:09/00:21/00:08 降至 00:08/00:03/00:01/00:02/00:02。消融（Table 4）：去 VC/SD/CR 均升高 Max T_fine；以 SSIM 相机选择替换 FCS 使 Aerial T_partition 升至 15:30；proxy 分析（Table 5）camera count 对最重块 recall@Top-5%/10% 达 0.529/0.471，优于 block area（0.353/0.412）与 visible points（0.117/0.265）。
- **创新点与贡献**：['负载均衡 KD 树划分 + minimax cutline refinement，以相机数为工作量代理，从划分阶段主动均衡块负载、抑制 fine 阶段 straggler；', '深度反投影式快速相机选择，将预处理从 M×N 次投影降为每相机一次深度合成，T_partition 从小时级降到分钟级；', '可见性裁剪与选择性致密化两项轻量技术，降低每块优化涉及的 Gaussian 数与峰值显存（Aerial 上 M_peak 由 22.1 GB 降至 16.7 GB）；', '建立 T_E2E=T_coarse+T_partition+max T_fine 的标准化端到端计时协议，并验证 fine 阶段零通信的多 GPU 训练不依赖 NVLink。']
- **局限与风险**：正文未设独立 Limitations 节，局限见于 Conclusion 与 future work：GPU 数量远少于块数时细训须分多轮，即使单块最长时间低，总墙钟时间仍可能很长；当前仅评估 5 个场景，作者计划在更大更复杂、需更多块的场景及含稀疏相机区域的数据集上进一步验证，并探索 LoD/2DGS 表示与 KD 树之外的划分策略。
- **与文献库的关系**：属库内大规模 3DGS 训练线（CityGS/VastGS/Grendel-GS/InfiniGS 一脉）：负载均衡 KD 树划分（相机数为工作量代理+minimax cutline refinement）从划分阶段主动均衡块负载，深度反投影式快速相机选择把预处理从 M×N 次投影降为每相机一次深度合成，可见性裁剪+选择性致密化降低每块优化高斯数与峰值显存；建立 T_E2E=T_coarse+T_partition+max T_fine 标准化计时协议。
- **可复现性**：附录 0.A.1 声明源码与预构建 Docker 镜像将在论文录用后发布，全部运行时在 Docker 环境中测量；VastGS 非官方实现引自 github.com/kangpeilun/VastGaussian，依赖 gsplat v1.5.3 与 fused-ssim；硬件为 10 节点 × 8×NVIDIA L40 + Intel Xeon Platinum 8362 集群（共 80 GPU）。
- **行动建议**：城市级 3DGS 生产管线的训练加速方案：MatrixCity-Aerial 端到端 1:13 vs CityGS 3:31（约 2.9×）、划分时间小时级→分钟级、峰值显存 22.1→16.7 GB，PSNR/SSIM 持平或更优且 fine 阶段零通信不依赖 NVLink；GPU 数远少于块数时须多轮细训，仅 5 场景验证，LoD/2DGS 表示与其他划分策略留待未来。

### 第 2 章 · AmaraSpatial-10K：空间计算与具身 AI 的 3D 资产数据集（2604.23018，3.67 A，FULL）

- **赛道 / 场合**：评估与数据集 / arXiv preprint（cs.CV，v2 公告于 2026-05-13；作者署名 Zero One Creative，CC BY 4.0；旧稿 replace 再公告首次入馆；未声明会议录用）
- **公告类型**：replace/cross（旧稿 replace/cross 再公告（首次入馆）：2508=2025-08 投稿、2510=2025-10 投稿、2604=2026-04 投稿、2605=2026-05 投稿，2026-10-28 公告批次 RSS 混入）
- **一句话结论**：发布 10,071 个度量缩放、语义锚定、PBR 就绪的合成 3D 资产数据集 AmaraSpatial-10K：CLIP Recall@5 较 Objaverse 提升 3.4×（0.612 vs 0.181，中位排名 267→3），Habitat-Sim 跌落测试物理稳定性 99.1%（V-HACD）且墙钟时间较 Objaverse 快约 20×，作为 Holodeck 资产包实现零重叠场景。
- **要解决的问题**：Web 级 3D 资产集合量大但极少达到可部署状态：任意度量缩放（Objaverse seating 类高度跨 0.02–115,276 m）、pivot/朝向错误、几何脆弱、纹理不全，这些缺陷破坏具身 AI、机器人与 AR/VR 的放置、碰撞、物理与检索；且度量尺度、规范朝向、语义锚点无法从几何事后推断，过滤无法恢复从未被 authoring 的属性，单图生成 3D 的基础模型还会把资产缺陷学进先验。
- **方法详解**：数据集侧：双 LLM（Qwen2-32B-Instruct + Gemini 3）为 476 个子类别生成多句描述、参考图提示与米制尺寸估计，Gemini 3 Flash Image 出参考图，in-house 引擎生成 mesh 后做三轴标准化——polycount（多数约 50K 三角形、约 2K 个约 10K 低模、约 1K 个约 100K hero 资产）、PBR（高频几何细节烘焙为分离的 Normal+Roughness 贴图嵌入 .glb）、凸碰撞包壳（每资产 <1,000 三角形）；空间对齐为 V_aligned=s·(R·V_raw)+t：s 使主尺度匹配 LLM 估计尺寸，R 以 90° 增量旋转至 VLM 判定正面朝前，t 按语义放置原点（落地物取底心、悬挂物取形心、吊装物取顶心）；三道自动筛选门（几何健康、尺度合理性 [ℓ/3, 3u]、前向轴审计）总通过率 91.4%。评测侧：提出 SPS(x,ℓ,u)=exp(-(d/h)²) 连续尺度合理性分数（区间内满分、区间外高斯衰减，d 为到边界距离、h=(u-ℓ)/2，d=h 时约 0.37）、intra-category 变异系数 CV=σ/x̄、anchor 误差 ε_anchor、跨模态 CLIP 一致性（4 个正交视图渲染取平均）、LLM Concept Density（Color/Material/Style/Shape/Component 五轴各 1 分，0–5）。
- **实验与结果**：评测对象为 AmaraSpatial-10K 与 Objaverse、HSSD、ABO、GSO 的关键词匹配子集。尺度审计（9 类 5,222 资产）：mean SPS 0.815 vs Objaverse 匹配集 0.412（1.98×），%Perfect 51.8 vs 7.7；mean CV 3.40 vs 9.92（2.9×）；Seating 类中位 0.72 m、56.7% 落在 [0.6, 1.1] m，Objaverse 181 个仅 17.7% 且 5% 截尾均值仍约 3× 上限。锚定：中位 ε_anchor 1 mm、79.7% 在 1 cm 内，Objaverse 中位 2.57 m。碰撞包壳平均 876 三角形、体积覆盖 V_hull/V_bbox=0.431（优于 HSSD 的 0.200）、顶点包含 99.99%。CLIP 一致性：Text↔Ref 0.303±0.037、Text↔3D 0.238±0.041（Objaverse 0.203±0.054）、Ref↔3D 0.726±0.064。检索（Table 6，N=10,071 vs 9,264）：R@5 0.612 vs 0.181、R@1 0.349 vs 0.089，中位排名 3 vs 267；仅用 brief description 消融降至 0.416（仍 2.3×）。Holodeck 场景合成（N=6 场景/包）：object overlap 0.00±0.00 vs Objaverse Matched 3.83±3.06，floor contact 100.00±0.00 vs 68.88±18.18。Habitat-Sim 跌落测试（2,569 vs 1,780 资产）：稳定率 99.1%（V-HACD）/97.4%（凸包）vs 95.5%，穿地 -0.003±0.003 m vs -0.013±0.037 m，墙钟 0.022±0.024 s vs 0.442±1.105 s。
- **创新点与贡献**：['发布 10,000+ 同时满足度量缩放、语义锚定、PBR、碰撞包壳、配对参考图与多句描述的 3D 资产库，填补 ShapeNet/Objaverse/GSO/ABO/HSSD 均未联合覆盖的属性组合；', '提出可复用的 3D 资产库评测套件（SPS、intra-category CV、anchor error、跨模态 CLIP coherence、LLM Concept Density）并在 5 个数据集上建立基线；', '三项下游验证：CLIP 检索 3.4× 增益（消融归因于描述丰富度）、Holodeck 零重叠满接触场景、Habitat-Sim 99.1% 物理稳定 + 约 20× 墙钟加速；', '以 Objaverse Matched 受控对比证明 authored alignment 优于 post-hoc filtering。']
- **局限与风险**：正文 §8.1 设独立 Limitations：资产为程序生成而非扫描，相对 GSO 等摄影测量资源存在几何与材质精度的系统偏差；476 个子类别中 23 个仅含 1 个资产，不足以支撑子类级生成训练；PBR 仅 Normal+Roughness，缺次表面散射、各向异性等完整 BRDF 现象；度量尺寸为 LLM 估计而非实测；文本元数据仅英文；SPS 绝对值受类级区间宽度限制（Vehicle 0.762、Tableware 0.479 偏低，子类级分辨率下升至 0.914/0.832）；场景合成研究仅 N=6 且依赖单一 VLM 评分；数据集不适用于照片级产品渲染或需验证摄影测量保真的场景（如 LiDAR/深度传感器仿真基准）。
- **与文献库的关系**：填补 ShapeNet/Objaverse/GSO/ABO/HSSD 均未联合覆盖的属性组合（度量缩放+语义锚定+PBR+碰撞包壳+配对参考图+多句描述）；提出可复用的 3D 资产库评测套件（SPS、intra-category CV、anchor error、跨模态 CLIP coherence、LLM Concept Density）并在 5 个数据集上建立基线，以 Objaverse Matched 受控对比证明 authored alignment 优于 post-hoc filtering。
- **可复现性**：数据集在 Hugging Face 公开：huggingface.co/datasets/ZeroOneCreative/amara-spatial-10k（CC BY 4.0，承诺五年维护）；评测套件参考实现随数据集发布，LLM-as-Judge 提示词与冻结区间在附录 M 公开；无 canonical train/val/test split，建议按子类别分层留出；in-house 生成引擎见 amara.01c.ai；训练硬件与生成算力正文未述。
- **行动建议**：空间计算/具身 AI 的即用资产库：10,071 个资产，CLIP Recall@5 较 Objaverse 3.4×（0.612 vs 0.181、中位排名 267→3）、Habitat-Sim 跌落测试物理稳定 99.1% 且墙钟快约 20×，作为 Holodeck 资产包实现零重叠满接触场景；程序生成资产较摄影测量资源有几何/材质精度系统偏差，476 子类中 23 个仅 1 资产，PBR 仅 Normal+Roughness，度量尺寸为 LLM 估计。

### 第 3 章 · VolFill：体素流匹配的单图 amodal 场景重建（2605.31466，3.65 A，FULL）

- **赛道 / 场合**：重建与SLAM / arXiv preprint（cs.CV，v2 公告于 2026-10-27；作者署名 UMass Amherst 与 Technical University of Crete，CC BY 4.0；文末附 NeurIPS Paper Checklist 投稿模板但正文未声明录用；旧稿 replace 再公告首次入馆）
- **公告类型**：replace/cross（旧稿 replace/cross 再公告（首次入馆）：2508=2025-08 投稿、2510=2025-10 投稿、2604=2026-04 投稿、2605=2026-05 投稿，2026-10-28 公告批次 RSS 混入）
- **一句话结论**：提出以混合 3D VAE + 潜空间流匹配 DiT 生成完整 TUDF 体素网格的单图 amodal 场景重建框架 VolFill：SCRREAM 上完整场景 CD 3.03、FS_0.02 54.83（×10²），显著优于 LaRI（5.19/30.85）与 NOVA3R（3.43/45.12），NRGB-D 上 FS_0.02 63.92 亦领先；RTX 4090 推理仅 1.4 s/图、峰值显存 3.0 GB。
- **要解决的问题**：从单张 RGB 图恢复包含被遮挡结构的完整 3D 几何本质欠定；前馈方法受 pixel alignment 硬约束只能重建可见表面，优化式方法需稠密采集与逐场景优化（数小时），大重建/生成模型多面向物体级场景；场景级 amodal 方法中 LaRI 的固定层数对密集遮挡欠表征且产生 layered artifacts（multiple wall 效应），NOVA3R 的点云输出噪声大、结构碎裂，且非结构化表征无法直接等值面抽取。
- **方法详解**：输入单图 I∈R^{H×W×3}，输出视锥对齐的 256³ TUDF 网格 V(p)=min(dist(p,𝒮),τ)（τ=3 voxels，无符号以适应非水密室内场景）。混合 3D VAE：稀疏卷积编码 16× 下采样至 16³×C=16 稠密潜空间并经 KL 正则；解码先稠密上采样至 64³、由 occupancy head 预测掩码（监督自 GT occupancy，IoU 99.8%）再稀疏卷积至 256³，损失 ℒ_VAE=L1+λ_bce BCE+λ_dice Dice+λ_kl KL。潜 DiT（12 blocks、768 dim、12 heads、AdaLN 时间步条件、QK-RMSNorm）以 rectified flow 训练：z_t=(1-t)ε+t z_1，ℒ_gen=E‖u_Φ(z̃_t,t,F_GFM)-(z_1-ε)‖²。双条件策略：冻结 MoGe2 的全局特征 F_GFM 经 cross-attention 注入各 DiT block；可见几何转 TUDF 后经冻结 VAE 编码为 z_vis，以零初始化 MLP 加性融合 z̃_t=z_t+MLP_zero(z_vis)。训练用 3D-FRONT 18k 场景构 96k 图像-TUDF 对 + ScanNet++ 46k 样本，2 阶段共约 5.5 天（2×A6000/L40S）；推理 50 步 Euler ODE、CFG scale 3.0、条件 drop 概率 0.1。
- **实验与结果**：基准：SCRREAM 460 样本与 NRGB-D 137 样本（9 场景，按 amodal-enrichment ratio ≥0.2 过滤）；指标 CD/APD_γ/FS_γ/FPD（×10²，评测前以 7-DoF Sim(3) 对齐，协议与 NOVA3R 一致）。SCRREAM 完整场景：VolFill CD 3.03、FS_0.1 95.03、FS_0.02 54.83，对比 LaRI 5.19/85.43/30.85、NOVA3R 3.43/95.26/45.12、MoGe2 5.74/83.96/45.84；遮挡区 CD 3.46 优于 LaRI 5.23 与 NOVA3R 3.56。NRGB-D：完整 CD 6.44、FS_0.05 63.92 vs LaRI 9.79/43.47、NOVA3R 8.19/49.92。度量几何（Table 3）：CD 3.88、FS_0.02 44.90、FPD 4.86 vs NOVA3R 6.56/22.23/16.50。消融：dual conditioning（MoGe2+Add）CD 3.03/FS 54.83 > 仅 MoGe2 3.81/46.80 > 仅 DINOv2 5.46/35.98；VAE hybrid decoder L1 0.43、0.07 s、1.7 GB，优于 dense-only 0.49/0.63 s/9.2 GB；5 个随机种子下 complete CD 3.11±0.08、FS_0.02 54.2±0.5。
- **创新点与贡献**：['首次将体素流匹配生成式框架用于场景级 amodal 重建：TUDF 结构化表征支持阈值直接提点云与经 MeshUDF 直接抽网格，摆脱点云/光线表征的无序性；', '混合稀疏-稠密 3D VAE 实现 16× 空间压缩，occupancy 引导的 dense-to-sparse 解码兼顾保真与显存（1.7 GB vs dense-only 9.2 GB）；', '几何基础模型双条件策略（全局 MoGe2 token + 可见几何 latent inpainting），加性零初始化融合优于拼接融合；', '采用无符号 TUDF 规避室内非水密几何的 inside/outside 歧义，并配套 training-free visible reinstatement 后处理（可见 CD 降至 2.01）。']
- **局限与风险**：正文 §5 设独立 Limitations：重遮挡区域偶尔残留小孔；可见面因联合生成而略钝于 MoGe2（可用 training-free visible reinstatement 或显式 3D 监督缓解）；训练与评测仅限室内场景，域外 KITTI 街景与 Sintel 合成帧失败（图 12）；网格固定 256³，512³/1024³ 需重训 VAE 与 DiT；迭代采样 1.4 s/图慢于单次前馈回归；附录 A.5 另指出大场景体素尺寸增大但评测范围内精度未降。
- **与文献库的关系**：属库内 amodal/完整场景重建线（LaRI/NOVA3R/MoGe2 一脉）：首次将体素流匹配生成框架用于场景级 amodal 重建，TUDF 结构化表征支持阈值直接提点云与经 MeshUDF 抽网格；混合稀疏-稠密 3D VAE 实现 16× 空间压缩（occupancy 引导 dense-to-sparse 解码，1.7 GB vs dense-only 9.2 GB），几何基础模型双条件（全局 MoGe2 token+可见几何 latent inpainting，加性零初始化融合优于拼接），无符号 TUDF 规避室内非水密几何歧义。
- **可复现性**：项目页 ngoductuanlhp.github.io/VolFill；推理代码与预训练权重已公开，训练/评测/数据处理代码及处理后的 TUDF 数据与 split 文件声明将发布（NeurIPS checklist 第 5 题答 No）；硬件：训练 2×RTX A6000 或 2×L40S（48 GB），本地工作站 RTX 4090 + Core i9 + 64 GB RAM；总计算约 1,680 GPU 小时；依赖开源 MoGe2 与公开 3D-FRONT、ScanNet++。
- **行动建议**：单图完整场景重建新 SOTA：SCRREAM 完整场景 CD 3.03、FS_0.02 54.83（LaRI 5.19/30.85、NOVA3R 3.43/45.12）、遮挡区 CD 3.46 亦最优，RTX 4090 推理 1.4 s/图、峰值显存 3.0 GB；重遮挡区域偶尔残留小孔、可见面因联合生成略钝（可用 training-free visible reinstatement 缓解）、仅限室内（KITTI 街景与 Sintel 失败）、256³ 固定网格需重训 VAE 与 DiT。

### 第 4 章 · PIS3R：深度 3D 重建的超大视差图像拼接（2508.04236，3.58 B，FULL）

- **赛道 / 场合**：重建与SLAM / arXiv preprint（cs.CV，v2 公告于 2025-11-27；旧稿 replace 再公告首次入馆；全文未署机构、未声明会议录用）
- **公告类型**：replace/cross（旧稿 replace/cross 再公告（首次入馆）：2508=2025-08 投稿、2510=2025-10 投稿、2604=2026-04 投稿、2605=2026-05 投稿，2026-10-28 公告批次 RSS 混入）
- **一句话结论**：提出基于 VGGT 深度 3D 重建 + 点云重投影 + RDDM 扩散精炼的超大视差（VLP）拼接框架 PIS3R：自建合成集 PSNR 22.026、RSR 95.7%，Sampson 对极误差 4.12 pixel（较 UDIS++ 的 12.94 降低约 3.1 倍），且拼接结果保持逐像素 3D 投影一致性、可直接输入 SfM 流程。
- **要解决的问题**：场景存在深度变化且相机基线显著时，homography 平面假设失效产生视差；现有自适应 warping、seam cutting 与深度拼接方法在超大视差下均失效，且以视觉无缝为首要目标，普遍忽视拼接结果的 3D 投影几何一致性，导致结果无法直接服务 SfM、SLAM、位姿估计、深度估计等下游 3D 视觉任务。
- **方法详解**：三步流水线：①深度 3D 重建，用前馈模型 VGGT 对 N 张无标定图像联合恢复相机内外参与稠密点云，形式化为 F((I_i))=(g_i, D_i, P_i, E_i)，g_i∈R^9；②点云重投影，世界系点云经 P_c^i=R^i P_w+t^i 变换到相机系、再按 P_uv^i=K_i P_c^i/Z_c^i 投影到像素，同一像素多个 3D 点取相机系最小深度 k=argmin Z_c^i(j)，像素网格分辨率由投影点坐标范围动态决定；空洞先取已填充点集凸 hull ℋ_i 内 K 个最近邻、按高斯权重 α=exp(-||Δ||²/2σ²) 加权填充，凸 hull 外置背景色，得到初始拼接图 Ŝ_i；③扩散精炼，采用残差去噪扩散 RDDM（前向 x_t=x_0+ᾱ_t x_res+β̄_t ε，x_res=x_in-x_0），由残差 U-Net 与去噪 U-Net 分别预测 x_res 与 ε。实现：接受 VGGT 全部预测点（不加置信度阈值）；RDDM 以自建 3DIS-D（RainDrop GT 加工）512×512、10 采样步、12 万迭代一阶段训练，再以 GoPro、5 采样步、2 万迭代二阶段微调，全局学习率 8e-5、batch size 1，全部在单张 RTX 4090 上完成。
- **实验与结果**：数据集：UDIS-D（无 GT，以纯旋转与轻微视差为主）；自建合成集（Blender 渲染 20 场景、600 图像对、含 GT）；自建真实集（手机拍摄 10 场景、682 图像对）。基线：APAP、ELA、UDIS++、OBJ-GSP。GT 集指标 PSNR/SSIM/LPIPS/RSR，UDIS-D 用 NIQE/PIQE，几何一致性用 Sampson 对极误差 d_Sam²。合成集（全部图像对）：PIS3R 22.026/0.782/0.110、RSR 95.7%，四项均第一；剔除配准失败样本后 22.351/0.796/0.102 仍领先 UDIS++ 的 21.038/0.748/0.097。真实集：19.674/0.644/0.180、RSR 100%。UDIS-D：NIQE 4.059、PIQE 44.13，与 UDIS++（4.098/43.79）相当。对极误差（pixel）：PIS3R 4.12 vs OBJ-GSP 16.43、UDIS++ 12.94、APAP 22.78、ELA 38.97。消融：3D 重建 backbone VGGT（合成 22.754/0.794/0.121）优于 Dust3R（21.872）与 Mast3R（21.814）；扩散模块 RDDM 最优（LPIPS 0.110 vs DiffIR 0.120、DDRM 0.132），精炼主要改善感知指标而对 PSNR/SSIM 影响甚微。耗时 5.8 s/图（重建 1.1 s + 重投影 3.5 s + 扩散 1.2 s），慢于 UDIS++ 的 2.7 s。
- **创新点与贡献**：['首个将前馈深度 3D 重建（VGGT）引入超大视差图像拼接的流水线，区别于既有 warping/seam cutting/深度拼接技术路线；', '拼接结果显式保持 3D 摄影测量一致性（对极误差 4.12 pixel，较 SOTA 降低约 3 倍），可直接馈入 SfM/SLAM 等下游任务；', '提出点条件 RDDM 扩散精炼模块，兼顾补洞去噪与几何结构保持；', '提出 RSR 指标与「先 padding、再配准、后算指标」的三步式评测协议，并构建 Blender 合成与手机实拍两套 VLP 测试集。']
- **局限与风险**：正文未设独立 Limitations 节，局限见于 Discussion 的 Limitation 条目：①输入同时含大视差与大旋转时，前景或背景的不重叠区域在重投影后产生明显缺失与畸变；②大面积物体遮挡时缺失区缺乏几何结构，残差扩散在该区域失效、退化为纯噪声，导致畸变、不一致与孔洞；③处理速度 5.8 s/图显著慢于 UDIS++ 的 2.7 s，作者建议以附录 parallax classifier 预估视差等级后再选用本方法。
- **与文献库的关系**：区别于库内 warping/seam-cutting 拼接线（UDIS++/APAP/ELA/OBJ-GSP），首个把前馈深度 3D 重建（VGGT）引入超大视差（VLP）拼接：视觉几何 grounded transformer 深度估计+点云重投影+点条件 RDDM 扩散精炼，拼接结果显式保持逐像素 3D 投影一致性，可直接馈入 SfM/SLAM 下游；提出 RSR 指标与先 padding、再配准、后算指标的三步评测协议，自建 Blender 合成与手机实拍两套 VLP 测试集。
- **可复现性**：正文给出 VGGT 仓库 github.com/facebookresearch/vggt、RDDM github.com/nachifur/RDDM、DiffIR github.com/Zj-BinXia/DiffIR、DDRM github.com/bahjat-kawar/ddrm；训练数据为基于 RainDrop 与 GoPro 数据集加工而成的自建 3DIS-D（未声明公开）；硬件要求单张 NVIDIA RTX 4090；PIS3R 自身代码与数据集未声明发布。
- **行动建议**：大基线宽 FOV 采集的拼接方案：合成集 PSNR 22.026/RSR 95.7%、Sampson 对极误差 4.12 pixel（UDIS++ 12.94，约 3.1×）、真实集 RSR 100%；大视差与大旋转共存时不重叠区域重投影缺失畸变、大面积遮挡时残差扩散退化为噪声；5.8 s/图显著慢于 UDIS++ 2.7 s，作者建议以 parallax classification 分流。

## 四、当日全量 7 维度对比表（参考）

见 [`papers/daily/backfill-1029/7dim-table.md`](../papers/daily/backfill-1029/7dim-table.md)。

## 五、覆盖率校验与筛选过程说明

- 门①（同质去重）：最大 Jaccard 0.308 < 0.62，通过，无同质重复。
- 门②（赛道覆盖）：纯值 Top10 仅覆盖 4 赛道 → 按重筛闭环剔除重复赛道最低分 SG²SLAM（4.00，重建与SLAM 第 4 篇），回补未覆盖赛道最高分 SOMA（3.79，评估与数据集）→ 定稿 Top10 覆盖 5 赛道（≥5），通过；SG²SLAM 仍入馆并写笔记（A 级），仅不占 Top10 名额。
- 门③（价值天花板）：当日最高分 4.30 < 库内近 30 天 Top10 均分 4.417（现算，435 条入窗）→ 非重磅日、无 S 级，未拔高、未凑数；达 S 线的 RESPLE2 4.30 / GraftRay 4.20 按校准关记 A。
- 三关均未触发重筛（门② 的回补即重筛闭环动作）；OUTDATED/SUPERSEDED 0 篇。

## 六、附录：证据等级分布与抓取记录

- FULL 4 篇；PARTIAL 1 篇；ABSTRACT_ONLY 0 篇（2610.36014 Immersive Commons 为 L1 ar5iv 仅摘要页 4,706 字符，已在 7 维表与笔记显式声明并按摘要级评估）。
- 抓取降级：无 L5；无 OCR；无伪造。串行 3s/篇，无限流。
