# XR Backfill 补录报告 · backfill-1104（旧稿再公告）

## 一、执行摘要
- **批次性质**：backfill（非当日新提交）——11-03 公告批次中 RSS 混入的旧稿 replace/cross 再公告 8 篇，首次入馆；原始投稿 2508=2025-08 / 2509=2025-09 / 2511=2025-11 / 2512=2025-12 / 2603=2026-03 / 2605=2026-05 / 2606=2026-06 / 2607=2026-07（v2 于 2026-11-03 公告前更新）。
- **补录 8 篇（5 B / 3 C）**：FLEG 3.58（SJTU/ECNU，任意视角前馈语言嵌入高斯泼溅，2 视角 ScanNet++ mIoU 46.61 超 Uni3R 39.54、密集 32 视角 60.97 远超 LangSplat 41.24，语义 embedding 仅 3.7%）· AR 引导机器人超声 3.58（TUM，OST-AR 脊柱穿刺系统，16 人 phantom 研究总体时间降 49%、误差降 25%、可用性 +50%）· 4D-GRT 3.43（NeurIPS 2025 Workshop，4D 高斯光线追踪渲染物理相机效应，pinhole 32.80 dB @36.56 FPS 较 MSTH 29.43 @9.38 FPS 量质双升）· Splaxel 3.31（UT Arlington 等，像素级通信分布式 3DGS 训练，Big City Street 7.6× 加速、通信占比 73-80%→10-20%）· EAvatar 3.08（Monmouth/重庆大学，生成式几何先验的表情感知头部化身，NeRSemble 16 视角 PSNR 25.07 超 GHA 24.56）· VR 眼部验证 2.93 · 材质感知高斯泼溅数字孪生 2.78 · Aes3D 3DGS 美学评估 2.72。
- **覆盖 6 赛道**；门① 0.151（全池合并复核）；门③ 对 backfill 不适用；OUTDATED 0。
- **诚实口径**：全部条目 `batch=backfill-1104` + `orig_window` 标注，绝不混入「当日新论文」。

## 二、排行榜（按加权降序）

| 排名 | 论文 | 赛道 | 总分 | 等级 | 证据 | 落后标记 |
|---|---|---|---|---|---|---|
| 1 | AR 引导机器人超声联合锥束 CT 用于脊柱操作的可行性（2603.22174） | 空间计算与UI | 3.58 | B | FULL | — |
| 2 | FLEG：经紧凑语义表示的任意视角前馈语言嵌入高斯泼溅（2512.17541） | 神经渲染 | 3.58 | B | FULL | — |
| 3 | 4D 高斯光线追踪：基于物理的相机效应数据生成（2509.10759） | 神经渲染 | 3.43 | B | FULL | — |
| 4 | Splaxel：经像素级通信的高效分布式 3D 高斯泼溅训练（2606.18588） | 系统与平台 | 3.31 | B | FULL | — |
| 5 | EAvatar：以生成式几何先验进行表情感知的头部化身重建（2508.13537） | 化身与人体 | 3.08 | B | FULL | — |
| 6 | VR 的眼部验证（2607.20790） | 感知与认知 | 2.93 | C | FULL | — |
| 7 | 数字孪生 3D 世界重建中的材质感知高斯泼溅（2511.20348） | 重建与SLAM | 2.78 | C | FULL | — |
| 8 | Aes3D：3D 高斯泼溅的美学评估（2605.05155） | 评估与数据集 | 2.72 | C | FULL | — |

## 三、逐篇深度解读

### 第 1 章 · AR 引导机器人超声联合锥束 CT 用于脊柱操作的可行性（2603.22174，3.58 B，FULL）

- **赛道 / 场合**：空间计算与UI / arXiv preprint（Technical University of Munich，Chair for Computer-Aided Medical Procedures and Augmented Reality + Munich Center for Machine Learning；cs.HC；正文标注为 Healthcare Technology Letters 期刊 Original Article，与 AE-CAI/CARE/OR 2.0/PRiSM Joint MICCAI Workshop 2026 特刊相关；v1 于 2026-03 首次投稿（据 arXiv 编号 2603 推断），v2 于 2026-10-30 更新）
- **公告类型**：replace（旧稿 replace 再公告（首次入馆）：2603=2026-03 投稿（Healthcare Technology Letters），v2 于 2026-11-03 公告）
- **一句话结论**：16 名受试者（6 女 10 男，22–43 岁，平均 28.75±4.49）的 phantom within-subject 研究显示：AR 相较常规屏幕总体执行时间降 49%（W=5.0，p=0.0003）、放置误差降 25%（t=3.29，p=0.0050）。分任务：LP 时间降 42%（78.25±56.46→45.31±24.90 s，p=0.002）、LP 误差降 32%（13.12±5.43→8.89±2.71 mm，p=0.015，显著）；FJ 时间降 54%（95.25±54.51→43.50±19.17 s，p=0.003）、FJ 误差降 18%（11.76±6.37→9.69±2.93 mm，p=0.228，不显著）。主观：可用性 +50%（p=0.00060）、NASA-TLX 负荷 -37%（p=0.0025）、信任 +41%（p=0.00070）、空间理解 +89%（p=0.0004）。系统精度：US-CBCT 目标配准误差 1.72±0.62 mm、探头标定 0.65±0.2 mm、点云配准 RMSE 9.1 mm。
- **要解决的问题**：脊柱介入（腰椎穿刺 LP、小关节注射 FJ）依赖 CT/透视辐射且缺乏实时 3D 反馈；超声受声影遮挡缺少全局解剖上下文；屏幕显示要求临床医生在 bedside 做 2D-3D 心理配准；现有 AR 导航多基于静态 CT 叠加或人工配准，未与机器人及实时超声集成，缺少 AR vs 屏幕的同受试者配对证据。
- **方法详解**：系统整合 KUKA LBR iiwa 14 R820 机械臂（手持手柄控制）+ Siemens ACUSON Juniper 5C1 凸头超声（3D 打印夹具含可拆卸针导）+ 机器人 CBCT 三维脊柱模型（3D Slicer 从 DICOM 提取网格）。预标定：光学跟踪相机与探头 marker、机器人末端-基座变换构手-眼问题 AX=XB 解 T^R_O，链式求 US-CBCT 变换 T^C_U。虚拟-真实配准：用户框选机械臂 3D bounding box 滤噪，多视角累积深度点云，与同步关节角采样的虚拟机器人表面点云做 maximal cliques 全局配准 + point-to-point ICP 精配准（任意时刻可做、无需预设姿态）。AR 界面（Unity + Microsoft HoloLens 2，TCP/IP 通信）原位显示配准好的脊柱模型；针导轴线参数化为射线 r(t)=o_R+t·d_R，与三角网格做 Möller–Trumbore ray–triangle 相交，最小正交点渲染为红色小球，无交点则不显示。
- **实验与结果**：within-subject 2 条件（屏幕 vs AR，顺序 counterbalanced）×2 任务（FJ 如左 L2–L3、LP 如 L3–L4 中线，目标随机分配、每目标仅出现一次），无练习试次；腰椎 phantom 置于 35×25×24 cm 容器、水面声耦合、泡沫粒遮挡直视；单场约 40 分钟。主观量表：SUS、NASA-TLX、SEQ（7 点）、Jian 信任量表、IPQ 空间理解问卷；统计用 Shapiro–Wilk 正态性 + paired t-test/Wilcoxon（α=0.05）。针尖位置由不知情的实验者在最终冻结超声帧上鼠标标定，再经标定变换转入 CBCT 坐标系，放置误差定义为与预定义目标点的三维欧氏距离。
- **创新点与贡献**：['OST-AR 原位可视化 CBCT 全局 3D 上下文 + 实时超声局部验证的统一坐标系框架', '抗干扰的流线式虚拟-真实配准流程（maximal clique 全局 + ICP 精配准，无需预设机器人姿态）', '针轨 raycasting 命中点预测叠加，支持快速轨迹规划与解剖有效性反馈', '同受试者 AR vs 常规屏幕的配对比较，覆盖效率-精度-负荷-信任-空间理解多维终点']
- **局限与风险**：['论文自述：rigid phantom 未模拟组织变形、呼吸、针弯曲与 CBCT 采集后体位变化，可能引入 registration drift', '未测量端到端 AR guidance/display TRE；放置误差混合了受试者执行与技术误差及人工针尖定位误差', '受试者均非执业临床医生，结论不能直接外推到介入放射/麻醉/脊柱外科', 'VAC 等 OST 深度感知效应未正式评估；CBCT-AR 条件数据与 Song et al. 2026 共享、非独立新观测；任务完成以受试者口头声明为准']
- **与文献库的关系**：谱系：robotic ultrasound 脊柱应用自 Rasoulian 2014、Tirindelli（US+力反馈融合）到 Esteban 的 OR 集成工作流（扫描规划-体积合成-针导对齐模板）；AR 脊柱导航对标 Agten（AR 小关节注射）、Jiang（可穿戴 AR 腰椎穿刺）与 pedicle screw AR 研究；Li et al. 的 CBCT+RUS 共配准是本系统直接前作。本文位置：首次把 CBCT-AR 界面与常规屏幕做同受试者配对比较，补齐可视化模态维度的效率/负荷证据。
- **可复现性**：原文未提及代码或数据开源；硬件 KUKA LBR iiwa 14 R820、Siemens ACUSON Juniper + 5C1 探头、Meta HoloLens 2、机器人 CBCT（Ouster OS1-128 用于真实采集验证）；AR 用 Unity 开发、TCP/IP 通信。
- **行动建议**：落地时优先补端到端 guidance/display TRE 的独立测量（刚体跟踪靶标分布工作体积）；临床转化需动态解剖跟踪或周期性 US-CBCT 再配准以应对形变；用临床专家与尸体/临床试验验证；可与纯超声 shape completion 方案做辐射-精度权衡对比。

### 第 2 章 · FLEG：经紧凑语义表示的任意视角前馈语言嵌入高斯泼溅（2512.17541，3.58 B，FULL）

- **赛道 / 场合**：神经渲染 / arXiv preprint（Shanghai Jiao Tong University + East China Normal University + Shanghai Artificial Intelligence Laboratory；cs.CV；v1 于 2025-12 首次投稿（据 arXiv 编号 2512 推断），v2 于 2026-04-05 更新）
- **公告类型**：replace（旧稿 replace 再公告（首次入馆）：2512=2025-12 投稿，v3 于 2026-11-03 公告）
- **一句话结论**：FLEG 在 2 视角 ScanNet++ 上 mIoU 46.61/mAcc 71.18/PSNR 28.14，超过 Uni3R（39.54/58.59/24.95）与 LSM（39.36/58.35/19.87）；ScanNet 2 视角 mIoU 48.01/mAcc 73.59。32 密集视角下 ScanNet mIoU 60.97 显著高于 per-scene 优化的 LangSplat（41.24）。DGLE 稀疏语义高斯仅用 73.89K 个 embedding（密集像素对齐 2.012M 的约 3.7%，论文表述为不足 5%）、存储 18.04 MB vs 491.3 MB，语义保真度相当。消融：去掉 instance-guided contrastive learning mIoU 从 46.87 跌至 40.22；去掉几何蒸馏跌至 18.56、训练不稳定。
- **要解决的问题**：前馈 language-embedded 高斯重建此前面局限于固定 2 视图输入或需要相机参数；给每个高斯挂语言 embedding 造成语义冗余，embedding 数量随输入视图线性增长、存储开销大；3D 几何+语义标注稀缺限制训练规模与数据多样性，难以支撑可扩展的前馈语义重建。
- **方法详解**：网络沿用 VGGT 式大 transformer（DINOv2 patchify + 可学习 camera token + 4 个 register token，24 层 global/frame-wise attention，深度与相机头），DPT-based Gaussian head 预测 μ/s/r/σ/SH 颜色与 D 维语义 emb，体素化聚合成标准高斯 G={μ,s,r,σ,c}。双分支蒸馏免 3D 标注：几何分支用 frozen VGGT 做 novel-view-based distillation（按 context views 点云投影覆盖率阈值 τ 选 target views， photometric+LPIPS 与深度/相机伪标签监督，防止对输入视角过拟合）；语义分支用 SAM2 实例掩膜 + CLIP 实例特征对齐，并以 instance-guided contrastive learning（anchor-pixel 相似度，复杂度 O(Np·K) 替代逐像素 O(Np²)）增强实例判别。DGLE 用更大 voxel 把语言 embedding 软加权融合成稀疏语义高斯 G_sem={μ,s,r,σ,emb}（各向同性协方差由 moment matching 近似、旋转固定单位四元数），与标准高斯解耦。
- **实验与结果**：ScanNet + ScanNet++ 训练（与 LSM/Uni3R 相同数据以公平对比），输入视角 2–16（另测密集 32），约 1B 参数，8×NVIDIA H200 训练约 2 天；指标 mIoU/mAcc（LangSplat 开放词汇分割协议）/PSNR/SSIM/LPIPS。基线：AnySplat、LSM、Uni3R（前馈）、LangSplat、LangScene-X（per-scene 优化）、LSeg/SAM2+CLIP（2D）。超参：λ1=2.0、λ2=1.0、λ3=0.5、λ4=0.05、η1=0.5、η2=0.2，蒸馏深度 MSE 权重 0.1、相机 Huber 10.0，输入长边最大 518 像素。消融（ScanNet++，2/4/8/16 视角平均）：w/o sparse(voxel) 1.625M emb/396.7MB、w/o sparse(pixel) 2.012M/491.3MB、w/o novel distill PSNR 24.77、w/o geo distill 18.56。
- **创新点与贡献**：['任意数量、无标定无姿态多视图输入的前馈语言嵌入高斯重建（2 到 30+ 视角同一模型）', 'novel-view-based distillation：无需相机真值即获新视角监督，缓解输入视角过拟合、保训练稳定', 'instance-guided contrastive learning 以 O(Np·K) 复杂度获得实例级语义判别', 'DGLE 解耦稀疏语义高斯：不足 5% 的 embedding 数量保持语义保真，大幅降低资产存储']
- **局限与风险**：['论文自述：几何精度受 VGGT 蒸馏上限约束（VGGT 数据与算力远大于本文）', '跨数据集泛化主要在室内场景验证（训练限于 ScanNet/ScanNet++），室外数据待扩展', '语言 embedding 仍占额外 GPU 显存，难以处理数百至数千张输入图像（需压缩或流式重建）', '语义稀疏性结论基于当前任务，语义极密/极稀场景的表现未充分测试']
- **与文献库的关系**：谱系：per-scene optimization 一线为 LangSplat、FastLGS、DF-3DGS；前馈重建上游为 PixelSplat、MVSplat、SelfSplat、AnySplat 与 3D 基础模型 VGGT；直接对标前馈语义重建 LSM（两视角）、Uni3R（多视图但需相机参数）与实例级点图 IGGT。本文位置：首个支持任意无位姿多视图 + 稀疏语言 embedding 的前馈语言高斯框架，面向机器人导航/操作的开放词汇 3D 交互。
- **可复现性**：project page https://fangzhou2000.github.io/projects/fleg ；原文未给出代码仓库链接（未明确开源）；训练用 8×NVIDIA H200 约 2 天；训练数据 ScanNet/ScanNet++ 公开。
- **行动建议**：机器人开放词汇 3D 场景理解可直接采用该前馈范式，免去逐场景优化的分钟/小时级开销；用稀疏语义高斯控制重建资产存储；扩展到室内外混合数据以提升泛化；百级以上输入需配合模型压缩或流式重建。

### 第 3 章 · 4D 高斯光线追踪：基于物理的相机效应数据生成（2509.10759，3.43 B，FULL）

- **赛道 / 场合**：神经渲染 / NeurIPS 2025 Workshop on Space in Vision, Language, and Embodied AI（arXiv:2509.10759v2 [cs.CV]；v1 于 2025-09 首次投稿（据 arXiv 编号 2509 推断），v2 于 2025-10-21 更新）
- **公告类型**：replace（旧稿 replace 再公告（首次入馆）：2509=2025-09 投稿（NeurIPS 2025 Workshop），v2 于 2026-11-03 公告）
- **一句话结论**：在自建 8 个室内动态场景×4 种相机效应基准上，4D-GRT 渲染速度全面最快且质量与 MSTH 相当或更优：pinhole PSNR 32.801 @36.56 FPS（MSTH 29.431 @9.38 FPS）、DoF 31.2475 @3.44 FPS（MSTH 0.57 FPS）、fisheye masked PSNR 28.8927 @41.53 FPS（MSTH masked 26.7930 @9.38 FPS）、rolling shutter chunk=4 时 31.6146 @4.99 FPS（chunk=16 时 13.54 FPS，指标几乎无损）。效率：训练 3 小时/存储 364.875 MB（HexPlane 12h/238MB，MSTH 8min/889MB）。fisheye 评测需用直径 409.6 的圆形 mask 屏蔽训练视角外区域。
- **要解决的问题**：真实相机效应（鱼眼畸变、卷帘快门、景深）训练数据稀缺：Blender 合成人力成本高且有 sim-to-real gap；视频生成/world model 不理解相机效应参数、产出违背物理（chicken-and-egg 问题）；动态 NeRF 能建模光传输但渲染慢、质量不如 GS；3DGS 快但仅支持 pinhole 相机模型，模拟鱼眼/卷帘/景深需特殊设计与复杂 Jacobian。
- **方法详解**：两阶段。阶段一：以 4D-GS（4D voxel planes 提特征 + MLP φ 融合 + φ_x/φ_r/φ_s 预测 Δx/Δr/Δs 残差）表示动态场景，在 3DGRT 可微光线追踪框架（k-buffer hit-based marching + NVIDIA OptiX）下直接对高斯图元 traced rays 端到端重建，损失 L1(C_v,t, Ĉ_v,t)+L_TV。阶段二把物理相机模型接入 ray tracer：fisheye 采用 4 次多项式径向畸变 θ=k0+k1r+k2r²+k3r³+k4r⁴，把像素转为传感器物理坐标后求球面光线方向；DoF 按 focus distance f_z 与 aperture radius r_a 在透镜面单位圆盘采样扰动光线原点并多次平均；rolling shutter 按行感知时间 t_r 取该时刻变形高斯 traced 单光线，用 chunk（Nc=1/4/16）近似 chunk 内平均感知时间以并行化。
- **实验与结果**：Blender 4.5 + BlenderKit 构建 8 个动态场景（篮球场、仓库、客厅、浴室 4 类环境），每场景 50 相机视角×4 效应（pinhole/fisheye/rolling shutter/DoF）×50 帧 512×512；PlenoBlenderNeRF 插件自动布相机与点云。基线 HexPlane/MSTH 装配与本文相同的相机效应渲染模块以保证公平；RTX 4090 训练评测，训练至收敛。pinhole：HexPlane 23.1124/0.7956/0.2942 @0.20 FPS；DoF：HexPlane 18.3722 @0.01 FPS；fisheye：HexPlane 15.6489（masked 21.6869）；rolling shutter：MSTH 28.7003/0.8927/0.1190 @9.35 FPS。另在 Neural 3D Video 真实数据集定性验证。
- **创新点与贡献**：['首个在动态场景高斯表示上执行光线追踪的工作（4D-GS + 3DGRT 组合）', '把鱼眼/景深/卷帘快门以物理相机模型统一接入 ray tracing，参数可控、物理准确且多视图一致', '发布 8 动态场景×4 相机效应的配对多视角视频基准', 'chunk 近似策略缓解卷帘快门逐行感知时间导致的 ray tracing 无法并行问题']
- **局限与风险**：['论文自述：依赖充分多视图视频才能重建高质量动态场景，稀疏视角或单目输入不适用', 'rolling shutter 当前假设静态相机（运动相机需插值轨迹后投射光线）', 'chunk 尺寸过大可能因近似引入 blocking artifacts', '数据为合成室内场景，真实域差距未定量评估；真实数据仅定性']
- **与文献库的关系**：上游为 3D-GS/4D-GS、3DGRT（静态高斯 ray tracing）与 3DGUT（sigma point + unscented transform 近似）；动态渲染基线为 HexPlane/MSTH（dynamic NeRF）与 Deformable 3D Gaussians；生成式路线对标 Curved Diffusion、AKiRa 与 Genie 3 等 world model。本文位置：以 4D 重建+物理 ray tracing 绕开 world model 对相机参数的不理解，直接大规模产出带精确参数标注的相机效应视频。
- **可复现性**：project page https://shigon255.github.io/4DGRT-project-page ；论文称构建并发布 8 场景配对数据集，但原文未明确代码开源方式；硬件 GeForce RTX 4090，渲染管线基于 Blender 4.5 相机模型。
- **行动建议**：需要带物理参数标注的相机效应训练数据时优先用 4D-GRT 而非 prompt 式视频生成；卷帘快门建议 chunk=4 起步（4.99 FPS、指标与 chunk=1 持平）；fisheye 评测务必 mask 训练视角盲区；后续可结合生成式/基础模型从单目视频重建动态场景以摆脱多视图依赖。

### 第 4 章 · Splaxel：经像素级通信的高效分布式 3D 高斯泼溅训练（2606.18588，3.31 B，FULL）

- **赛道 / 场合**：系统与平台 / arXiv preprint（UT Arlington 牵头，联合 Texas A&M、Rice、University of Georgia、University of Houston、University of Washington、Argonne National Labs 等；cs.DC；v1 于 2026-06 首次投稿（据 arXiv 编号 2606 推断），v2 于 2026-10-30 更新）
- **公告类型**：replace（旧稿 replace-cross 再公告（首次入馆）：2606=2026-06 投稿，v2 于 2026-11-03 公告）
- **一句话结论**：8 GPU 下相较 SOTA 分布式 3DGS 框架 Grendel：Big City Street（120M 高斯）训练 48.8h→6.4h（7.6×，PSNR 均 23.2）、Big City Aerial 3.6h→1.2h（2.9×，PSNR 30.4→31.2）、Small City Street 7.5h→1.3h（5.9×，PSNR 21.4→21.7）、Small City Aerial 25.5m→8.0m（PSNR 26.6→27.3）。吞吐最高 90 img/s（Big City Street，Grendel 14）与 142 img/s（Big City Aerial，Grendel 52）。通信占迭代时间从 Grendel 的 73.0%–80.4% 降至 10%–20%；redundancy reduction 使 zero-pixel 比例降 39%（Small Street）/55%（Small Aerial）、saturated-pixel 降 40%/34%；GPU 利用率提升 20%–35%。
- **要解决的问题**：大规模 3DGS 训练需把数亿高斯分布到多 GPU：现有框架或把场景切成孤立区域分别优化（牺牲全局一致性、产生可见接缝），或做全局 Gaussian-level all-to-all（Grendel），通信量随高斯数与 GPU 数非线性暴涨并主导迭代时间（10M→50M 高斯时每迭代通信 200MB→800MB；20M 高斯 2→8 GPU 时通信占比 16.7%→74.3%）；且单视角只涉及部分分区，naive 一视角一迭代调度下 GPU 大量空闲（利用率约 50%）。
- **方法详解**：Splaxel 把分布式训练重构为 pixel-level local rendering + global composition：每个 GPU 只渲染本地凸分区（AABB 凸划分保证光线与每分区至多相交一次，从而全局 alpha-blending 顺序一致），只交换逐像素 color/transmittance/depth（分辨率固定则通信量恒定、与高斯数无关），反向传播用重 formulation 的梯度公式经各 GPU 保留的 partial pixel 本地回传、无需额外通信。冗余消除：初始化时把视锥与凸分区的重叠三维区域顶点投影到像平面得可见像素区， selective all-to-all 只传有效像素（spatial redundancy，naive 下最高 64% 传输像素为零）；训练中按累计 transmittance<ε（固定 1e-4）动态判定饱和像素并跳过后续分区（saturation redundancy，去除空间冗余后仍最高 53%）。调度：conflict-free view consolidation 把 GPU 集合无交集的视图贪心分桶并行执行，配异步流水线重叠通信与计算。
- **实验与结果**：MatrixCity 四数据集：Big City Street 206,412 训练/22,744 测试/25.3 km²、Big City Aerial 51,632/9,066/25.3 km²、Small City Street 27,505/3,256/2.7 km²、Small City Aerial 5,621/741/2.7 km²（合计约 28 km²、60K 航拍+350K 街景图像，1080p），迭代数分别 1.2M/300k/150k/30k。平台 1：8×RTX 6000 Ada（48GB）；平台 2：8×RTX PRO 6000 Blackwell（96GB）；双 AMD EPYC 9254；CUDA 12.8 + PyTorch 2.9.0；batch=GPU 数。消融：Small City Street 单组件约 100ms/迭代，+redundancy 2.2×，+view consolidation 3.3×；Big City Street 约 80ms，3.1× 与 4.3×。batch 4/8/16 速度 5.8/5.9/5.9× 稳定。透射阈值 ≤1e-2 时 PSNR 稳定，固定 1e-4 无需逐场景调。
- **创新点与贡献**：['像素级通信方案在保持数学一致性的前提下使通信量与高斯数解耦', '凸分区保证全局混合顺序的几何洞察及配套的梯度重 formulation', '几何不可见 + 透射饱和双通道像素冗余预测/检测，免额外通信', 'conflict-free view consolidation 调度消除 GPU bubble，配合异步流水线']
- **局限与风险**：['原文未单列 limitations 节；可推断：小场景/少 GPU 下优势有限，收益随场景与 GPU 规模增长', '通信降至 10–20% 后反传成为迭代时间主要成分，瓶颈转移', '透射阈值固定 1e-4，对极端透明/不透明材质的泛化未测', '原文未提及代码开源，第三方复现门槛高']
- **与文献库的关系**：直接对标 Grendel（Zhao et al. 2025，唯一保持全局一致的 Gaussian-level 通信分布式 3DGS 框架，本文的动机分析与唯一基线均基于它）；算法分区类前作（Lin et al.、Liu et al. 等 divide-and-conquer）被指牺牲全局一致性；通用 DNN 分布式框架（DeepSpeed、PyTorch DDP、Alpha）因假设静态均衡张量计算而不适配 3DGS 的动态视图访问。上游为 3DGS（Kerbl et al. 2023）与 MatrixCity 大规模数据集。本文位置：系统侧首个像素级通信的分布式 3DGS 训练框架。
- **可复现性**：原文未提及代码开源；数据 MatrixCity 公开；硬件双 AMD EPYC 9254 + 8×RTX 6000 Ada（48GB）或 8×RTX PRO 6000 Blackwell（96GB）；软件 CUDA 12.8、PyTorch 2.9.0。
- **行动建议**：大规模城市/航拍 3DGS 训练采用像素级通信 + 冗余消除 + 视图合并三件套；批大小与 GPU 数可放心扩展（5.8–5.9× 稳定）；通信占比压到 20% 以下后应转向优化反传与本地渲染；复现需自建框架，建议关注作者后续开源动态。

### 第 5 章 · EAvatar：以生成式几何先验进行表情感知的头部化身重建（2508.13537，3.08 B，FULL）

- **赛道 / 场合**：化身与人体 / arXiv preprint（Monash University + Chongqing University；cs.CV；v1 于 2025-08 首次投稿（据 arXiv 编号 2508 推断），v2 于 2026-11-02 更新）
- **公告类型**：replace（旧稿 replace 再公告（首次入馆）：2508=2025-08 投稿，v2 于 2026-11-03 公告）
- **一句话结论**：在 NeRSemble 多视图数据上，EAvatar 自驱重演 5 个 identity 全 16 视角平均 PSNR 25.07、SSIM 0.857、LPIPS 0.168，超过 GHA（24.56/0.853/0.175）与 TensorialGA（24.07/0.848/0.204）；新视角合成 PSNR 23.22 vs GHA 22.89、TensorialGA 21.51。RTX 3090 上渲染约 32 FPS、单主体训练约 2.5 天；相较 GaussianAvatars（183 FPS 但 PSNR 22.50、预处理 32.7 小时）以 12.0 小时预处理换取更高保真。生成式先验使 Stage I 训练时间减少 11%。消融：Case 1 PSNR 由 baseline 23.28 经 +control 23.36、+split 23.47 升至全模块 23.66；控制阈值 τ=0.3 优于 0.15 与 0.4。
- **要解决的问题**：3DGS 头部 avatar 在嘴部、眉宇等高形变区域难以建模细粒度表情与局部纹理连续性；早期训练几何不稳定；依赖 mesh 先验的方法又限制分布外局部几何的表达；全局线性混合（如 HeadGaS）缺乏局部控制。
- **方法详解**：两阶段框架。Stage I 结构感知几何建模：逐帧拟合 3DMM（BFM）得表情系数 θ∈R^d_exp 与 pose β∈R^6；MLP 拟合 SDF，DMTet 可微提取网格，再与大规模生成模型（Xiang et al. 2024）产出的 identity-specific 先验网格做 ICP 对齐，施加只约束全局 center 与 scale 的 alignment loss（避免点级监督噪声）。Stage II 动态高斯优化：以 expression/pose 残差 MLP 分别预测位置、颜色、旋转、缩放、透明度残差；controllable Gaussian mechanism 按预测位移阈值 τ=0.3 选出 Control Gaussians，以高斯核距离加权（半径 r 内）把形变向量传播到邻域；deformation-aware splitting 在 τ_split=0.2 处把大位移高斯二分以增加局部密度。Stage I 损失为 RGB/silhouette/offset/landmark/Laplacian/mesh 加权和（λ_rgb=1.0、λ_sil=0.1、λ_offset=0.01、λ_lmk=0.1、λ_lap=100、λ_mesh=1.0），Stage II 用 RGB+LPIPS（λ=1.0/0.1）。
- **实验与结果**：NeRSemble 16 相机视角，每 identity 用 FREE 序列测试、其余训练（比 GaussianAvatars/TensorialGA 原协议更难，二者延长训练至 800k 迭代仍未充分收敛）。指标 PSNR/SSIM/LPIPS；跨身份重演无 ground truth 仅定性；新视角合成用 8 视角训练/8 视角测试。消融：Stage I 损失全模型 24.82 最佳（w/o offset+lap 24.67、w/o landmark 24.71、w/o lap 24.78）；阈值扫描 τ=0.3 PSNR 24.24/24.82 最高；效率表：NeRFace 4 天/~0.06 FPS、HAvatar 7 天/~7 FPS、GHA 3 天/~32 FPS、GaussianAvatars 1 天/~183 FPS、本文 2.5 天/~32 FPS。Stage I 训练 10,000 迭代（lr 1e-3、batch 4），Stage II 500,000 迭代。
- **创新点与贡献**：['按预测位移大小自适应选择 Control Gaussians 并向邻域传播的局部形变控制机制', '基于属性位移量（而非 opacity）触发 Gaussian splitting 的形变感知细分策略', '生成模型先验网格 + 全局 center/scale 对齐损失，稳定早期几何训练并改善轮廓与遮挡区', '跨身份表情重演下保持身份一致与牙齿/眼睛等高频细节']
- **局限与风险**：['论文自述：口腔内部等高铰合/部分遮挡区域因拓扑复杂、可见性变化频繁、有效监督弱而难稳健建模', '非面部邻近区域与大姿态、光照变化未显式建模，稳定性下降', '训练成本较高（单主体 2.5 天、500k 迭代），渲染 32 FPS 低于 GaussianAvatars/TensorialGA 等实时方法', '框架为多视图设计，稀疏/单目输入不适用']
- **与文献库的关系**：谱系：3DMM/FLAME → NeRF/NeuS/FaceNeRF/NeRFace/IMAvatar/Neural Head Avatars → 3DGS 头部 avatar（HeadGaS、PointAvatar、GaussianAvatars、SplattingAvatar、GHA、TensorialGA、ScaffoldAvatar）。上游工具为 3DGS（Kerbl et al. 2023）、DMTet 与生成式 3D 先验（Xiang et al. 2024）。本文以 expression-aware + deformation-aware 双机制切入，对标 GHA/TensorialGA 等高保真 3DGS avatar，差异在局部形变控制与生成先验几何初始化。
- **可复现性**：project page https://saralkun.github.io/EAvatar ；原文未提及代码或数据开源；训练/渲染硬件为单张 NVIDIA RTX 3090。
- **行动建议**：关注论文点名的嘴部内部结构先验、非面部区域时序稳定、显式眼姿建模与光照感知表示等方向；fidelity 优先的离线 avatar 生产管线适合两阶段方案；需要实时渲染时与 FLAME-rigged 高斯方案按 operating point 取舍并比较预处理成本。

### 第 6 章 · VR 的眼部验证（2607.20790，2.93 C，FULL）

- **赛道 / 场合**：感知与认知 / arXiv preprint（University of Wyoming + San Diego State University；cs.CV；v1 于 2026-07 首次投稿（据 arXiv 编号 2607 推断），v2 于 2026-10-30 更新；license CC BY-NC-ND 4.0；NSF REU Site 2349771 资助）
- **公告类型**：replace（旧稿 replace 再公告（首次入馆）：2607=2026-07 投稿，v2 于 2026-11-03 公告）
- **一句话结论**：在 VRBiom（Meta Quest Pro 内向 NIR，400×400，900 段 bonafide 视频、25 名受试者、平均约 23K 帧/人）上：单模态虹膜 EER 0.44/AUC 0.59/d' 0.34，眼周（MobileFaceNet）EER 0.34/AUC 0.76/d' 1.08；最佳 peri-heavy 融合（w_i=0.25/w_p=0.75）EER 0.33、AUC 0.75、d' 0.99（约 3 倍于虹膜），论文自述相对单模态虹膜 AUC 提升约 16%、EER 降低约 11%。UnReflect 去高光使所有眼周模型 EER 下降（MobileFaceNet 34.70→31.97），但 UNIR-Net 照明修复反而使虹膜 AUC 从 0.62 跌至 0.59；OAC 几何校正表现最差（插值与 padding 损伤高频纹理）。ISO margin adequacy 在 MITRE 框架仅 4.38±16.37（远低于推荐阈值 80），concentricity 同样在 VR 原生影像上失效。
- **要解决的问题**：VR 头显采集天然是 off-axis gaze、非均匀 NIR 照明、睫毛遮挡与强镜面反射的非受控条件，传统虹膜识别协议失效；ISO/IEC 29794-6 质量指标从未在 VR 数据上系统评估（且不同实现分歧大）；图像级生成式增强对认证效用的影响未知；iris+periocular 的最优融合权重缺乏定量分析。
- **方法详解**：三模块。(1) 眼部图像调整：DINOv3 + H8Net 回归 8-DoF 投影 homography 做 off-axis 校正（perspective warp 恢复圆形虹膜）；UnReflectAnything（frozen DINOv3 ViT + inpainting）去镜面反射；UNIR-Net 做非均匀照明恢复（NIR 单通道复制为 3 通道 RGB 输入）。(2) ISO/IEC 29794-6 质量评估：用 MITRE BIQTIris 与 UND 两套独立实现统计 12 项指标（Usable Iris Area、Iris-Sclera/Pupil Contrast、Circularity、Grayscale Utilization、Radius、Pupil-Iris Ratio、Concentricity、Margin Adequacy、Sharpness、Motion Blur、Overall Quality）的 μ±σ。(3) 认证与融合：虹膜用 ArcIris（UND 提交 NIST IREX X 的开源实现 openiris-cvrl），眼周用 MobileFaceNet/ResNet-18/ResNet-50，再做加权分数级融合 S_fused=w_i·S_iris+w_p·S_peri 并扫描权重。
- **实验与结果**：仅用 VRBiom bonafide 数据；3 种凝视状态（steady/moving/partially closed）×戴/不戴眼镜；眼周实验每视频随机采 3 帧（约 110 帧/人）；指标 EER、FNMR@FMR=1e-2、AUC、d'；3 个模型 fold 平均；PyEER 画误差曲线；推理用 NVIDIA L40S 或 H100。ISO 两框架分歧巨大：Usable Iris Area MITRE 97.59±7.63 vs UND 54.29±22.75，UNIR-Net 后 UND 跌至 43.26；Sharpness MITRE 原始 7.98±9.58、UNIR-Net 后 38.34±18.25。眼周各模型（Original/UnReflect/UNIR-Net 的 EER%）：MobileFaceNet 34.70/31.97/35.14、ResNet-50 36.37/32.32/36.54、ResNet-18 35.83/31.65/36.47。融合权重：50/50 EER 0.34、75/25（iris-heavy）0.38、40/60 0.33、25/75 0.33。
- **创新点与贡献**：['首次在 VR 眼部数据上系统评估 ISO/IEC 29794-6 全部指标并用 MITRE/UND 两套独立框架交叉验证', '把 off-axis 几何校正、镜面去除、照明恢复三类生成/几何增强用于 VR 眼部认证预处理并量化其双刃剑效应', '定量揭示 margin adequacy 与 concentricity 在 VR 原生影像上失效（off-axis 所致而非质量差）', '多权重 score-level 融合系统比较，给出 peri-heavy 最优配置（25/75）']
- **局限与风险**：['论文自述：UnReflect/UNIR-Net 在 RGB 而非 NIR 上训练，可能改变细微虹膜纹理，需微调/域适应', 'margin adequacy 与 concentricity 指标在 VR 影像上失效，ISO 阈值/指标需针对 VR 修订', '仅用 bonafide 数据，未测 presentation attack；样本 25 人、单一头显型号（Quest Pro）', 'OAC 因 warping padding 干扰使眼周识别最差；ISO 指标结果对分割实现高度敏感']
- **与文献库的关系**：上游：Daugman/Wildes 经典虹膜与 periocular 生物特征（LBP/BSIF/SIFT 等手工特征）；VR 生物特征一线为 Boutros et al.（HMD iris+periocular 融合）、ImmerIris（500K VR 数据集）、GazeShift（解缠凝视与外观）、SAM2 虹膜分割（Sharma et al.）与 VRBiom 数据集（Kotwal et al.）；识别模型为 ArcIris（Khan et al.，openiris-cvrl）与 Kolf et al. 轻量化眼周。本文位置：以质量评估-图像调整-认证融合三模块系统剖析 VR 眼部认证，首次给出 VR 场景 ISO 指标统计基线与双框架分歧证据。
- **可复现性**：代码开源：github.com/rtran7530/vrsyntheye-reu.git ；数据 VRBiom 公开（Meta Quest Pro NIR 400×400）；推理 NVIDIA L40S 或 H100；依赖 MITRE BIQTIris、UnReflectAnything、UNIR-Net、openiris-cvrl/ArcIris 与 PyEER 等开源组件。
- **行动建议**：VR 认证落地优先眼周或 peri-heavy（25/75）融合而非纯虹膜；ISO 质量指标用于 VR 前需重订阈值（margin adequacy 等直接失效，且实现分歧巨大建议双框架交叉）；把生成式修复模型在 NIR 域微调/域适应以避免纹理幻觉；按论文未来方向实现 quality-driven adaptive fusion，用逐帧 ISO 分数动态调整模态权重。

### 第 7 章 · 数字孪生 3D 世界重建中的材质感知高斯泼溅（2511.20348，2.78 C，FULL）

- **赛道 / 场合**：重建与SLAM / arXiv preprint（Siemens Digital Industries Software + Delft University of Technology；cs.CV；v1 于 2025-11 首次投稿（据 arXiv 编号 2511 推断），v2 于 2025-11-28 更新；ROBUSTIFAI/SYNERGIES 等 Horizon Europe 与 VLAIO 项目）
- **公告类型**：replace（旧稿 replace 再公告（首次入馆）：2511=2025-11 投稿，v2 于 2026-11-03 公告）
- **一句话结论**：仅用相机的管线在 5 个城市场景上达到与 LiDAR-camera 融合（NKSR 网格）相当的 LiDAR 反射率仿真精度：MAE 10.05 vs 10.14、中位误差 6.48 vs 6.78。视觉质量上本文 adapted H3DGS 的 LPIPS 0.44 为全场最佳（3DGS 0.46、CityGaussianV2 0.50、3DGUT 0.53，5 场景中 4 个最优），但 PSNR 18.27、SSIM 0.41 低于三个基线（20.07–21.22 / 0.56–0.58）。材质分割消融（MCubes 500 图）：RMSNet 准确率 0.63/mIoU 0.28，+FastSAM 0.65/0.29，+SAM2 0.67/0.31。
- **要解决的问题**：Digital Twin 的 3D 重建中，LiDAR 几何准确但缺纹理与语义材质，且对玻璃/金属等透明反射材质失效；LiDAR-camera 融合需复杂标定与同步，稀疏视图下纹理仍差；把 2D 材质分割自动投影到 3D 表面并赋物理材质用于传感器仿真，一直是 camera-only GS 管线的开放问题。
- **方法详解**：解耦的五阶段 camera-only 管线：(1) 单目材质提取：RMSNet（asphalt/concrete/glass/metal 等）+ FastSAM 实例边界 + 区域多数投票得 shape-aware 材质掩膜；(2) 大规模 GS：COLMAP 稀疏点云 + GPS 位姿/内外参先验（ego 车辆掩除），训练 H3DGS（可视化，关闭 LoD 与抗锯齿并自定义合并 chunk）与 MiLO（网格，同一 COLMAP 输出，共享坐标系）；(3) per-pixel 材质投影：可微光栅化渲染高斯保 3D-2D 对应，深度排序取最近高斯标签，SegAnyGS 保证跨视角一致，KNN 把标签传给最近 mesh 三角形；(4) 物理材质赋值：按 Principled BSDF（Disney 标准）从 Matsynth（4,000+ 材质、14 类）选 PBR 贴图（base color/normal/roughness/metallic）赋到三角形；(5) 仿真验证：导入 Simcenter Prescan，按 Ouster OS1-128 规格复现传感器与 MATLAB API 导入 ego 轨迹，生成带材质反射率的合成 LiDAR 点云并与真实测量对比。
- **实验与结果**：instrumented test vehicle：Ouster OS1-128 LiDAR + 6 路环视相机 + RTK-GPS，20Hz 硬件同步；5 个静态城市场景（各约 8 秒，移动 ego 车辆采集）；每场景 50 个均匀采样新视角评 PSNR/SSIM/LPIPS。传感器仿真基线为 NKSR（LiDAR 点云网格）+ 与本文相同的相机材质标签，控制变量后对比反射率 MAE/中位误差。硬件 Dell Precision 7680（64GB RAM + NVIDIA RTX A4000 ADA laptop GPU），Simcenter Prescan 2411 + MATLAB R2023b。定性显示：高反射/透明表面仍错位、侧视相机因车辆运动模糊降质、密集遮挡场景质量下降、植被反射率系统性高估。
- **创新点与贡献**：['模块化 camera-only 数字孪生管线：GS 保真渲染 + 显式网格的混合表示，免 LiDAR 硬件与标定', '基于高斯可微光栅化的自动 2D→3D 逐像素材质投影（SegAnyGS 一致性 + KNN 传标签）', '把语义材质映射为 Principled BSDF 物理参数，直接服务 LiDAR 等物理传感器仿真', '以真实 LiDAR 反射率为 ground truth 定量验证 camera-only 重建的传感器仿真精度']
- **局限与风险**：['论文自述：高反射与透明表面重建仍错位；侧视相机运动模糊降质；密集物体分布与遮挡场景质量降低', '相机重建几何噪声高于 LiDAR，植被反射率因简化 PBR 材质参数而高估', '仅覆盖静态场景；内部数据集未公开，泛化能力待外部验证', '为兼容仿真引擎关闭 H3DGS 的 LoD 与抗锯齿，牺牲了像素级 PSNR/SSIM']
- **与文献库的关系**：上游：NeRF/3DGS、大规模场景 GS（CityGaussianV2、H3DGS）、高斯网格提取（Poisson、SDF-based、MiLO）、NKSR（LiDAR 神经核表面重建）、材质分割（RMSNet/MCubes）、SegAnyGS、Matsynth PBR 材质库与 Simcenter Prescan 仿真平台。本文位置：把 GS 重建、语义材质投影与物理传感器仿真串成免 LiDAR 的 digital twin 替代流程，并以 LiDAR-camera 融合为基线做反射率对表。
- **可复现性**：原文未提及代码或数据开源（instrumented test vehicle 内部数据集；license CC BY-NC-SA 4.0）；硬件 Dell Precision 7680 + RTX A4000 ADA laptop GPU；软件 Simcenter Prescan 2411 + MATLAB R2023b。
- **行动建议**：无 LiDAR 或标定受限的 ADAS 数字孪生场景可用该管线替代 LiDAR-camera 融合；玻璃/金属与强反射表面需专门处理；评估传感器仿真应优先看反射率 MAE/中位误差而非 PSNR；下一步动态场景与学习式材质表示（减少对预定义 PBR 库依赖）是论文明确的未来方向。

### 第 8 章 · Aes3D：3D 高斯泼溅的美学评估（2605.05155，2.72 C，FULL）

- **赛道 / 场合**：评估与数据集 / arXiv preprint（The University of Sydney + The University of Hong Kong；cs.CV；v1 于 2026-05 首次投稿（据 arXiv 编号 2605 推断），v2 于 2026-05-23 更新；license CC BY-SA 4.0）
- **公告类型**：replace（旧稿 replace 再公告（首次入馆）：2605=2026-05 投稿，v5 于 2026-11-03 公告）
- **一句话结论**：Aesthetic3D 为首个 3D 场景美学数据集：278 个重建场景、92,649 个输入视图（平均 333 视角/场景，源自 DL3DV-10K 采样子集 + Bilarf），场景级分数跨度 0.184–0.825（均值 0.395、中位 0.369、std 0.129）；场景内视角分差均值 0.33（p90 0.47、max 0.85），83.2% 场景分差>0.20，证明 3D 美学强视角依赖。Aes3DGSNet 仅 3.2M 参数、29.4 GFLOPs：8-attr 标签下 PLCC 0.567/SRCC 0.554/KRCC 0.389，total 标签下 MAE 0.076/RMSE 0.101，均优于 Stochastic NR-PCQA（PLCC 0.509）、GSOQA（0.503）、MM-PCQA（0.441）、MUGSQA-DBCNN（0.311）与 ArtiMuse（0.224）等基线。
- **要解决的问题**：3DGS 场景评估长期侧重重建保真与感知真实（PSNR/SSIM/LPIPS、NR-IQA），忽视构图、和谐、视觉吸引力等高层美学属性；且缺少通用 3DGS 美学标注数据集；3DGS 作为低级图元表示，其美学质量还取决于高斯密度、颜色与几何等表示属性，难以直接捕捉高级美学特征。
- **方法详解**：标注管线：用 MLLM 美学评估器 ArtiMuse（ArtiMuse-10K 训练，Token As Score 把 101 个 token 映射为 0–100 分）对每个输入视图打总分，并按 8 个属性维度（Composition & Design、Visual Elements & Structure、Technical Execution、Originality & Creativity、Theme & Communication、Emotion & Viewer Response、Overall Gestalt、Comprehensive Evaluation）用统一 prompt 独立查询得属性分，跨视角平均后归一化到 [0,1] 为场景级标签。Aes3DGSNet：FPS 采 2,048 个高斯（中心 p_i + RGB c_i + 单位方向 p̄_i）经 4-block point Transformer（PTv3 风格、从零训练）+ attention pooling 得场景 token s；projection-based view tokenization 用相机内外参把 3D token 投到 14×14 patch 网格（mean/max pooling + empty-cell token + view-conditioned context a_v，不渲染图像）得视角描述子；FFS 启发的 top-8 视图选择器（listwise Transformer + 稀疏 top-K 权重）做视角选择；加权融合后经 3 层回归器输出分数；损失为 Huber + pairwise ranking（λ_rank=0.1）。
- **实验与结果**：80/20 划分，seeds {7,13,42}；每场景 32 个候选视角（球面均匀采样），几何按 95 分位半径归一化；指标 PLCC/SRCC/KRCC/MAE/RMSE。基线三组：(A) 2D IAA 零样本 ArtiMuse（~8B 参数、257.7K GFLOPs）、AADB（70.9M）、NIMA（14.7M）、TANet（13.9M）；(B) 3DGS QA：MUGSQA-DBCNN（15.3M/712.2 GFLOPs）、GSOQA（27.5M/3.5 GFLOPs）；(C) 点云 QA：MM-PCQA（52.9M）、LRL-GQA（17.4K）、Stochastic NR-PCQA（25.6M/6123.7 GFLOPs）。消融：全局场景 token 替代视角选择 PLCC 0.534；无选择器均匀平均 0.513；K=16 为 0.545、K=32 为 0.540；λ_rank=0 时 0.552、0.5 时 0.548。训练 16 epochs、AdamW（lr 5e-5、wd 1e-4、batch 4），实验用 RTX 5090，标注用 2×H100。
- **创新点与贡献**：['首个 3D 场景美学数据集 Aesthetic3D 与配套 benchmark（首个系统性的 3D 神经渲染美学评估框架）', 'IAA-based 标注策略：用 MLLM 的 8 维度属性 prompt 把 2D 美学评估器转化为结构化属性打分器', 'rendering-independent 评估：直接在 Gaussian primitives 上以几何投影获得视角证据，免渲染、降硬件门槛', '视角选择性证据聚合（top-K selector）匹配美学的视角依赖本质']
- **局限与风险**：['标签为 ArtiMuse 代理标签而非大规模人工评分（论文做了 human study 验证但规模有限）', '数据以室内场景（DL3DV/Bilarf）为主，室外泛化未验证', '场景内视角分差大（均值 0.33），单视角评分不可靠，必须多视角输入', '8 个属性分数高度相关（Spearman 0.933–0.994），应理解为共享美学信号的可解释分解而非独立监督目标']
- **与文献库的关系**：上游：2D IAA（AVA、AADB、NIMA、MUSIQ、TANet、ArtiMuse）、NeRF/3DGS 感知质量评估（GSOQA、MUGSQA 等）与点云 QA（PCQA 系列）。本文位置：把评估目标从 realism/distortion 提升到 aesthetics，首个面向 3DGS 的通用美学 benchmark；实证显示 2D 美学先验（含 ArtiMuse）向 3DGS 渲染视图迁移很差（PLCC 仅 0.224），必须几何感知 + 多视角推理才能可靠评估。
- **可复现性**：代码与数据集承诺发布于 github.com/LouckXu/Aes3D（原文未确认已发布）；硬件 NVIDIA RTX 5090（实验）与 2×H100（标注）；训练 16 epochs、AdamW lr 5e-5、batch 4；3DGS 重建由 DepthSplat 从多视图图像生成（附录 E）。
- **行动建议**：3D 内容创作/资产生成管线可用其做美学筛选与排序；把美学作为优化目标驱动 3D 渲染/编辑/压缩是论文指明方向；注意代理标签与人类感知的差距，关键场景建议人工抽检；输入务必多视角以覆盖场景内美学波动。

## 四、当日全量 7 维度对比表（参考）

见 [`papers/daily/backfill-1104/7dim-table.md`](../papers/daily/backfill-1104/7dim-table.md)。

## 五、覆盖率校验与筛选过程说明

- 门①（同质去重）：全池合并复核最大 Jaccard 0.151 < 0.62，通过，无同质重复。
- 门②（赛道覆盖）：覆盖 6 赛道（神经渲染×2 / 空间计算与UI×1 / 系统与平台×1 / 化身与人体×1 / 重建与SLAM×1 / 感知与认知×1 / 评估与数据集×1 中计 6），8 篇低量批次实际上限。
- 门③（价值天花板）：对 backfill 不适用；本批 8 篇均未达 S 线（最高 3.58），按实数定级，未拔高。
- OUTDATED/SUPERSEDED 0 篇。


## 六、附录：证据等级分布与抓取记录

- 本表 8 篇：FULL 8 篇；PARTIAL 0 篇；ABSTRACT_ONLY 0 篇。
- 抓取降级：2611.01229 / 2611.01759 为 L1/PARTIAL（ar5iv 仅摘要页 4,899/5,252 字符，按摘要级评估并显式声明，未脑补正文细节，两篇均为 C 级仅入馆不解读）；主批其余 33 篇 L0/FULL。无 L5、无 OCR、无伪造；串行 3s/篇，无限流。
