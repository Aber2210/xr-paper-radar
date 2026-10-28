# XR 每日论文解读报告 · 2026-10-29（10-28 公告批次）

## 一、执行摘要
- **公告日 2026-10-28（周三）≠ 拉取日 2026-10-29（周四 02:30）**——诚实口径：本批处理的是 10-28 公告批次，非当日硬提交。
- **主批 XR 新稿 20 篇（14 A / 4 B / 2 C，无 S 级）** = 10-28 公告组甄别 19 篇 + **ParetoGS 补录 1 篇**（10-27 公告批次，上批候选→评分环节静默丢失，今日 listing 对账补回，诚实标注）。Top10：RESPLE2 4.30（多传感器里程计，非均匀 B 样条+IMU 精确预测）· GraftRay 4.20（路径追踪物理一致高斯场景网格插入）· LingGS 4.15（几何求解器取代学习相机头的高斯 SLAM）· StereoSplat 4.07（立体原生前馈 3DGS，AbsRel 0.04）· HoloRecon 4.07（前馈几何验证的长程全景重建）· DomeGS 4.00（VR 无界 3DGS 背景补全，36 人用户研究）· GeoGSplat 4.00（几何接地非像素对齐 3DGS）· PrinGS 3.92（3DGS 后训练隐私匿名化）· ParetoGS 3.85（连续预算 3DGS，补录）· SOMA 3.79（第一视角人体运动理解基准，门②回补）。
- **覆盖 5 赛道**：重建与SLAM / 渲染与显示 / 神经渲染 / 内容生成 / 评估与数据集。
- **覆盖度三关**：门① 0.308；门② 纯值 Top10 仅 4 赛道 → 回补后 5 赛道；门③ 4.30 < 4.417（现算）→ **非重磅日、无 S 级**；RESPLE2 4.30 / GraftRay 4.20 达 S 线按校准关记 A。
- **全文证据**：19 篇 L0/FULL + 1 篇 L1 摘要级（2610.36014，ar5iv 仅摘要页）。
- **同批 backfill-1029**：RSS 混入旧稿 replace/cross 再公告 4 篇首次入馆（3 A / 1 B，最高 LoBE-GS 3.73），详见 [XR-Backfill-Report-backfill-1029.md](XR-Backfill-Report-backfill-1029.md)。

## 二、排行榜（按加权降序）

| 排名 | 论文 | 赛道 | 总分 | 等级 | 证据 | 落后标记 |
|---|---|---|---|---|---|---|
| 1 | RESPLE2：惯性知情的非均匀 B 样条递归多传感器里程计（2610.37602） | 重建与SLAM | 4.30 | A | FULL | — |
| 2 | GraftRay：路径追踪的物理一致网格插入高斯场景（2610.37036） | 内容生成 | 4.20 | A | FULL | — |
| 3 | LingGS：几何预测与相机跟踪解耦的高保真高斯 SLAM（2610.36853） | 重建与SLAM | 4.15 | A | FULL | — |
| 4 | StereoSplat：立体接地的度量尺度前馈 3DGS（2610.35902） | 神经渲染 | 4.07 | A | FULL | — |
| 5 | HoloRecon：前馈几何验证的长程全景一致重建（2610.36876） | 重建与SLAM | 4.07 | A | FULL | — |
| 6 | GeoGSplat：几何接地的非像素对齐高斯泼溅（2610.36760） | 神经渲染 | 4.00 | A | FULL | — |
| 7 | DomeGS：无界 3DGS 的感知一致背景补全（VR）（2610.37172） | 渲染与显示 | 4.00 | A | FULL | — |
| 8 | PrinGS：高斯泼溅的后训练隐私保护（2610.36168） | 渲染与显示 | 3.92 | A | FULL | — |
| 9 | ParetoGS：稀疏适配锚点的连续预算高质量 3DGS（2610.34235） | 渲染与显示 | 3.85 | A | FULL | — |
| 10 | SOMA：第一视角细粒度人体运动理解基准（2610.36384） | 评估与数据集 | 3.79 | A | FULL | — |

## 三、逐篇深度解读

### 第 1 章 · RESPLE2：惯性知情的非均匀 B 样条递归多传感器里程计（2610.37602，4.30 A，FULL）

- **赛道 / 场合**：重建与SLAM / arXiv preprint（林雪平大学 / ETH Zürich / 多伦多大学等；arXiv:2610.37602v1 [cs.RO] 2026-10-27）
- **公告类型**：new
- **等级说明**：总分 4.30 达 S 线（≥4.2），但当日最高分 4.30 < 库内近 30 天 Top10 均分 4.417（现算，435 条入窗）→ 非重磅日，按校准关记 A（同 10-24 EgoHand / 10-27 WFM / 10-28 RacerGS 先例）
- **一句话结论**：在 GrandTour、JEPLO、PPS TV、HOPPER、HANDI 等手持/履带/腿式/腿式四旋翼平台上，RESPLE2 以非均匀 B 样条 + IEKF 实现与 SOTA 相当或更优的实时估计：JEPLO 全部 8 条序列 APE 最低（LKIO 0.005–0.010 m），HOPPER 在 ±4 g 内置 IMU 频繁饱和、约 25 g 峰值加速度与 18 rad/s 角速率下仍为除 flip4（内置 IMU）外全部序列最低 APE，消融显示惯性知情控制点预测使 APE 相对降低约 39%–76%，且每帧仅占时间预算 10.6%–18.3%。
- **要解决的问题**：激进动力学、非结构化环境与有限机载算力持续挑战 6-DoF 自运动估计；现有多传感器里程计多为传感器特定且离散时间表示，异步测量需插值近似，LiDAR 与卷帘相机在机动中还产生运动畸变；连续时间估计几乎全是滑动窗优化，实时部署与新增模态集成困难；RESPLE 的均匀节点间隔难以同时兼顾激进运动精度与每步充分约束（几何退化风险）；理论上 B 样条控制点一般不在轨迹上，故无法像离散时间/GP 方法那样用 IMU 积分直接预测新控制点，且当时无非均匀 B 样条里程计原生支持回环全局精化。
- **方法详解**：6-DoF 轨迹以非均匀三次 B 样条表示：位置 s(t)=[s_{n−3},s_{n−2},s_{n−1},s_n]Ωu（u=(t−t_{n−1})/τ_{n−1}），姿态 r(t)=r_{n−4}∙∏_{i=n−3}^{n}Exp(λ_iδ_i)（δ_i=Log(r_{i−1}⁻¹∙r_i)，λ=Φu），由运动学插值得速度/加速度/角速度。核心是 knot-clamping 边界性质：新边界节点以三重度加入（t_n=t_{n+1}=t_{n+2}），使 t_n 处 s(t_n)=s_n、ṡ(t_n)=3(s_n−s_{n−1})/τ_{n−1}、s̈(t_n)=6(μs_{n−2}−(1+μ)s_{n−1}+s_n)/τ_{n−1}²、r(t_n)=r_n、ω(t_n)=6δ_n/τ_{n−1}——最新控制点恰在轨迹上，从而可用 IMU strapdown 精确预测（子步状态含 3 个旧 RCP、新 CP、双 IMU 偏置与速度：f_s=s+vΔt+½a^WΔt²、f_v=v+a^WΔt、f_δ=Log(Exp(δ)∙Exp(Δtω/2))，a^W=R(z_acc−b_acc)−g）。节点扩展准则：LiDAR 批几何充分性（点数>N1、IMU 数>N2，加权法矩阵 G=Σn_in_iᵀ/σ_i² 满足 λ_min(G)≥γ 且 λ_min/tr(G)≥η，0<η≤1/3）、间隔>τ_max、位移>d_max、姿态增量>θ_max、速度变化>v_max。新节引入后反钳制改变局部基，用 RCP reset 恢复 t_{n−1} 处位置/速度/加速度与姿态/角速度：位置 reset 闭式（s⁺=J_ss⁻），姿态 reset 以牛顿迭代解最小二乘（通常 5 次内收敛），协方差 P⁺=JP⁻Jᵀ（J=diag(J_s,J_r,I₆)）。更新为 IEKF：δx_i=K_i(z_k−h(x̂_i))−(I−K_iH_i)(x̂_i−x̂_{k|k−1})，K_i=PH_iᵀ(HPH_iᵀ+Σ_k)⁻¹。多传感器测量模型按各自原生时间戳接入：LiDAR point-to-plane（VoxelMap 局部地图，残差方差融合平面与点协方差并设方差下限）、IMU（对加速度残差施加 block-Huber 权重 β_i=δ_acc/s_i 抑制饱和/离群）、视觉投影（KLT 跟踪 + LiDAR 同配准深度）、腿式运动学（前向运动学足速 + point-to-plane，假设接触无滑移）。全局精化：iBTC 检测回环后直接优化非均匀控制点，最小化 m 个回环残差 + N−1 个相邻控制点间相对平移/旋转里程计残差（LM 求解，每个里程计残差雅可比支撑仅 2 个控制点，保持稀疏），修正累积漂移同时保住局部高阶运动学。
- **实验与结果**：数据集与平台（Table I）：GrandTour（ANYmal D + Boxi，室内/室外/野外，6 测试 + 4 训练序列）、JEPLO（Unitree Go2 楼梯/箱子机动，Mid360 倒装有限视场，EIL_Mask1/2 贴胶带诱导感知退化）、PPS TV（履带车昼夜高速机动，night_street 峰值角速率 4.5 rad/s，Mid360 内置 IMU ±4 g 频繁饱和）、HOPPER（腿式四旋翼 12 条室内序列，瞬时加速度约 25 g、角速率至 18 rad/s；外置 BMI088 ±24 g@1000/500 Hz vs 内置 ICM40609 200 Hz；Vicon 10 相机真值）、HANDI（手持 13 条序列，Avia/Mid360/ZedX1/D455 多种 LVI 配置）。基线：Coco-LIC、FAST-LIVO2、CTE-MLO、Point-LIO、Leg-KILO、RESPLE（其 ikd-Tree 换成 VoxelMap 以隔离估计差异）。评测主机 Ubuntu 24.04 + Ryzen 9 9950X + 32 GB RAM，evo 按 0.5 m 路径增量算 RPE。

JEPLO（Table III，APE RMSE m）：RESPLE2-LKIO 8/8 序列最低——EIL_Box 0.005（LeKILO 0.032、CoLIC 0.054、FLIVO2 3.200）、EIL_Mask1 0.008、EIL_Mask2 0.010、EIL_Mix 0.010、EIL_Stairs 0.007、Long_Stairs 0.007、Outdoor1 0.007、Outdoor2 0.006；FLIVO2 在 5 条序列失败（✗）。

HOPPER（Table V，APE m）：RESPLE2 在两种 IMU 配置下除 flip4（内置）外全部最低；high2 外置 IMU：RESPLE2 0.005、CoLIC 0.017、FLIVO2 0.021、RESPLE 0.011；内置 IMU 下 CoLIC 与 FLIVO2 全部序列失败，Point-LIO 靠饱和轴拒绝完成但误差更高（high2 0.594），RESPLE2-LO 无 IMU 亦完成全部序列且优于 Point-LIO 内置 IMU 表现。速度估计（Table VI）：内置 IMU 下 RESPLE2 所有序列精度最高（如 base1 0.617 vs RESPLE 0.732、PLIO 1.674）。

HANDI（Table VII，APE m；括号为 +LC 全局精化后）：az-corri 6.166→1.339(0.044)、az-inout 1.334→0.031(0.030)、mz-inout 1.491→0.668(0.026)、ar-inout 10.177→0.394(0.076)、az-out2 5.355→2.767(0.009)、az-out1 4.780→0.009(0.009)；RESPLE2 完成全部序列，LVIO 在退化长廊与室内外过渡优于所有对照，长距离端到端误差最低；首次回环处轨迹位置误差最多修正近 2 m 且保持速度连续。

GrandTour（Table II）：用较低端 Mid360 内置 IMU 仍总体竞争或更优，RESPLE2-LKVIO 为变体最优；Coco-LIC RPE 低但 APE 未转化为全局精度优势。

消融（Table VIII，HOPPER  enclosed 序列 APE m）：惯性知情预测 vs 常数转移矩阵——base1 0.015→0.005、high1 0.017→0.004、high2 0.012→0.005、side1 0.010→0.004、side2 0.011→0.004、flip1 0.015→0.008、flip2 0.016→0.008、flip3 0.018→0.011、flip4 0.017→0.009（相对降约 39%–76%，high1 最大）。节点放置：flip1 全程 RESPLE2 用 2087 个控制点 vs Coco-LIC 2362（−11.6%）且精度更高；RESPLE2 在着陆冲击处加密节点、弹道段稀疏，Coco-LIC 近均匀。

运行时（Table IX，ms/帧）：flip1(LIO) 7.7/50（15.4%）、day_open(LVIO) 18.3/100（18.3%）、Outdoor1(LKIO) 5.3/50（10.6%）；IEKF 更新为最大项（LIO 约 1/3、LKIO 约 1/2），RCP 预测+reset ≤0.51 ms 且 <7%；ar-inout 上 16 次全局优化每次约 15 次迭代、最新一次约 2 s。
- **创新点与贡献**：['首个非均匀 B 样条递归连续时间多传感器里程计：借 knot-clamping 边界性质实现控制点的精确 IMU 积分预测，节点放置随运动与测量可得性自适应', '反钳制后的 RCP reset（位置闭式 J_s + 姿态牛顿迭代 + 协方差变换）在节点扩展时保持轨迹局部一致性，支撑后续数据关联', '统一框架支持 LO/LIO/LVIO/LKIO/LKVIO 与 LiDAR-only，各模态在原生时间戳经连续时间观测模型接入，IMU 样本交替划分为预测/更新子集', '轻量全局精化：iBTC 回环 + 直接优化非均匀控制点（相邻控制点里程计残差保持稀疏），原生支持回环并保持局部高阶运动学一致']
- **局限与风险**：正文未设独立 Limitations 节。从实验边界与未来工作推断：① 结论节称未来将研究自适应传感器加权与不依赖 LiDAR 深度的视觉特征约束，以改善传感器退化下的鲁棒性，暗示当前视觉特征深度来自 LiDAR 同配准、严重退化场景仍受制于此；② RESPLE2-LO（无 IMU）退化为常速过程模型（位置按线性速度预测、姿态增量按节点间隔比缩放），与 IMU 配置存在精度差距；③ GrandTour 测试序列结果经 COMFORT Localization Benchmark 提交获得，而其他系统使用其高端 HG4930 MEMS IMU（RESPLE2 不可用），横向对比存在硬件不对等；④ 内置 ±4 g IMU 下 flip4 并非最优（RESPLE 更优）；⑤ 验证集中于作者与公开数据集上的三类平台，更广泛平台与场景泛化待测；⑥ 全局精化依赖 iBTC 在 LVIO 配置下的回环检测，LO/LIO/LKIO 配置下未启用。
- **与文献库的关系**：延续库内连续时间估计线（B 样条/IEKF 里程计）与多传感融合谱系（TLEIO 事件惯性 / HexVIO 立体惯性）；首个非均匀 B 样条递归框架，借 knot-clamping 边界性质实现控制点的精确 IMU 积分预测是核心差异，反钳制 RCP reset 保持节点扩展时的轨迹局部一致性。
- **可复现性**：代码与实验数据集公开：https://github.com/ASIG-X/RESPLE2。实现为 ROS2 包，依赖 Eigen、OpenMP（每节点约 5 线程）、Pinocchio（腿式正向运动学）、Eigen 的 CHOLMOD 接口（稀疏线性求解、跨迭代复用符号分解）。评测环境：Ubuntu 24.04 + AMD Ryzen 9 9950X + 32 GB RAM。数据集：GrandTour（grand-tour.leggedrobotics.com）、JEPLO、PPS TV（datasets.leggedrobotics.com）及自采 HOPPER/HANDI（随代码发布）；真值：Vicon（HOPPER，10×Vantage）、Qualisys（HANDI）；评估用 evo 包（RPE 按 0.5 m 路径增量）。
- **行动建议**：多平台（手持/履带/腿式/腿式四旋翼）实时里程计的强基线：JEPLO 8/8 序列 APE 最低、HOPPER 在 ±4 g IMU 饱和与约 25 g 峰值加速度下仍几乎全部最低；惯性知情预测降 APE 39%–76% 且每帧仅占预算 10.6%–18.3%。关注无 LiDAR 深度时的视觉特征约束（作者未来工作）与传感器退化鲁棒性。

### 第 2 章 · GraftRay：路径追踪的物理一致网格插入高斯场景（2610.37036，4.20 A，FULL）

- **赛道 / 场合**：内容生成 / arXiv preprint（慕尼黑工业大学 TUM；arXiv:2610.37036v1 [cs.CV] 2026-10-27）
- **公告类型**：cross
- **等级说明**：总分 4.20 达 S 线（≥4.2），非重磅日按校准关记 A（同 10-24 EgoHand / 10-27 WFM / 10-28 RacerGS 先例）
- **一句话结论**：在 FIPT 合成场景上，GraftRay 以 ΔPSNR 35.17、阴影 IoU 0.76（DiffusionRenderer 版；RGB↔X 版为 34.29/0.77）刷新 mesh 插入高斯场景的 SOTA，大幅超过 IRGS（28.40/0.50）与 EAG-PT（24.26/0.40）等基线，且单卡 RTX 3090 上每帧插入仅需 1.6 min（同采样量下 EAG-PT 约 12×）。
- **要解决的问题**：将虚拟 mesh 物体插入 2D/3D 高斯泼溅（2DGS/3DGS）场景时，物体既要被场景光照正确照亮，又要向场景投射物理一致的阴影并贡献间接光。现有图像空间 harmonization 方法牺牲多视图一致性；环境图（environment map）方法无法显式表示窗户、灯具等近场面光源及其与几何的遮挡；联合 inverse rendering 引入超出插入所需的未知量，且 LDR 观测难以区分自发光体与高反表面。
- **方法详解**：流程分四步。① 材质与法线估计：从高斯场景渲染 V 个虚拟视角，用内在图像扩散模型 RGB↔X（或 DiffusionRenderer）加 S 个随机种子预测 albedo/roughness/metallic/normal；按透射率定义可见表面深度 z（累积透射率首次低于 1/2 处），仅当 |r−z|/z<τ_z 时把预测反投影到该高斯；先对接受视图按种子平均，再跨种子取逐通道中值，得到场景级材质并在光照估计中固定不变。② 发射器初始化：用户用 SAM 在少数视图标记窗、灯等光源，反投影得 3D 点集，拟合单侧解析矩形 E_j（RANSAC 加权亮高斯定平面 + PCA 细化），贴墙发射器轴向对齐水平/垂直方向。③ 高斯场景路径追踪：每个高斯用 3σ 轴对齐包围盒表示，峰响应求交 t_i*=−p·q/‖q‖²、m_i²=‖p‖²−(p·q)²/‖q‖²，当 m_i²<9 时命中，有效不透明度 α_i=o_i·exp(−m_i²/2)；any-hit 以概率 α_i 随机接受（随机透明），首个被接受概率 w_i=α_i∏_{j∈F_i}(1−α_j)；阴影射线用独立 ray type 确定性累积透射率、低于 5×10⁻³ 终止；光传输遵循 Mitsuba 式路径积分，Cook–Torrance/GGX BRDF + 解析矩形上的 NEE + BSDF 采样经 MIS（power heuristic）组合，Russian roulette 终止。④ 发射器辐射度估计：几何与材质固定时 I(L)=Σ_j L_j B_j（B_j 为仅 E_j 单位辐射度的基图，渲染时剔除 E_j 附近薄板内亮高斯）；饱和通道（阈值 τ=0.98）只提供下界，目标函数对未裁剪观测直接拟合、对裁剪观测用单边惩罚 [τ−g(B^TL_c)]_+²，每通道解非负最小二乘（J 个未知数通常 <20，GPU 上 Levenberg–Marquardt 解 J×J 法方程）；最后差分合成 I_out=M·k·I_with+(1−M)·I_3dgs⊙clip(I_with/I_without,0,c)（c=3，k 为背景像素 I_3dgs/I_without 比值的中值以补偿曝光）。
- **实验与结果**：数据集：4 个 FIPT 房间 + 2 个 NFINITE（合成，路径追踪 GT）、2 个 FIPT-Real + 5 个 ScanNet++（真实）、5 个 SpAItial 平台生成的 3DGS 场景；所有方法用相同物体、放置与灯光，每场景 3 个视角。有 GT 报 ΔPSNR/mask PSNR/阴影 IoU/阴影 RMSE，无 GT 报无参考 VQAScore ratio（LightHarmony3D）。

FIPT 合成场景主结果（Table 1）：
| 方法 | ΔPSNR↑ | Mask PSNR↑ | 阴影 IoU↑ | 阴影 RMSE↓ |
| Ours (DiffusionRenderer) | 35.17 | 29.14 | 0.76 | 0.08 |
| Ours (RGB↔X) | 34.29 | 28.49 | 0.77 | 0.07 |
| IRGS（最强基线） | 28.40 | 22.56 | 0.50 | 0.15 |
| EAG-PT | 24.26 | 21.19 | 0.40 | 0.29 |
| ComGS | 13.09 | 8.27 | 0.26 | 0.33 |

材料恢复（Fig. 5，FIPT 四房间平均）：Ours 对齐后 albedo 19.9 dB，EAG-PT 20.2 dB 但仅恢复 diffuse albedo；GS-IR/GI-GS 把阴影与窗光烘进 albedo，低 6–8 dB；GS-IR 全零 metallic 得分尚可，因仅约 1–6% 像素为金属。

效率（单卡 RTX 3090）：bedroom 重建 22 min；DiffusionRenderer 先验 1.5 h/seed；反投影 6 min；辐射度拟合 13.5 min；插入一帧 1024×576@256 spp 1.6 min（含两次路径追踪）；EAG-PT 在其 1024 spp 下 14.4 min/帧，等采样量约 12×。

消融（bedroom，Table 2；格式 ΔPSNR/Mask/IoU/RMSE）：完整 35.4/31.6/0.80/0.08；点光源 26.5/20.5/0.51/0.12；环境图 27.6/27.4/0.56/0.55（PT/3DGS）；反弹 1/2/3/4 次 ΔPSNR 25.7/30.8/32.9/34.0（4 次与完整追踪器差 1.4 dB 内）；GT 窗口几何 35.4/31.7/0.80/0.08；窗口尺寸 ×0.8/1.25/1.5 → 34.2/35.4/35.4；位移 5/10/20 cm → 35.4/35.1/34.3（IoU 均 0.80）；shadow only / one-way IoU 降至 0.58/0.00；emissive 3DGS IoU 0；灰 albedo mask PSNR 腰斩至 15.6；去掉差分合成 ΔPSNR 跌至 24.8。
- **创新点与贡献**：['仅凭 LDR 图像：把多视角 2D 材质/法线预测反投影到单个 2D/3D 高斯，无需传统 inverse rendering 的联合优化即可提供场景级物理属性，且支持无原始训练图的合成高斯场景', '扩展 OptiX 路径追踪器联合追踪随机透明高斯与插入 mesh，用 3σ AABB + 峰响应求交实现高斯场景上的显式光传输（光照、阴影、间接光）', '把饱和像素视为删失观测，用路径追踪单位辐射度基图 + 非负最小二乘高效估计发射器强度，并以未饱和区域区分真光源与亮反射面', '差分合成把插入物体的光照变化迁移到原 3DGS 渲染，在获得阴影/间接光的同时保留原重建的视角相关外观']
- **局限与风险**：正文 4.3 节明示两条主要局限：① 光源必须手动标记——用户需用 SAM 在一个或少数视图中框选窗户与灯具（只需近似 mask）；② 依赖先验信息——albedo、roughness、metallic 与法线来自 2D 估计器（RGB↔X 或 DiffusionRenderer），先验误差会传导到拟合灯光与插入效果。另实验中观察到 metallic 通道会溢到漫反射表面（Fig. 5），且真实/生成场景的无 GT 指标 VQAScore 几乎无法区分方法。
- **与文献库的关系**：与库内高斯场景物体插入（IRGS/EAG-PT 一脉）及 inverse rendering 环境光估计同域；差异在扩展 OptiX 路径追踪器联合追踪随机透明高斯与插入 mesh（3σ AABB+峰响应求交），并把饱和像素视为删失观测、以路径追踪单位辐射度基图+非负最小二乘估计发射器强度，免传统联合优化。
- **可复现性**：正文未提及代码/数据公开链接。硬件：全部步骤在单张 NVIDIA RTX 3090 完成。软件栈：OptiX 加速路径追踪器、Mitsuba 式路径积分器、SAM、RGB↔X 与 DiffusionRenderer 先验模型；评测数据为 FIPT/NFINITE/FIPT-Real/ScanNet++ 与 SpAItial 生成场景（SpAItial 为商业平台，Plant-Wall 场景用初步物体放置）。
- **行动建议**：AR 虚拟物体插入/阴影合成的首选基线（FIPT ΔPSNR 35.17 vs IRGS 28.40、阴影 IoU 0.76 vs 0.50、每帧 1.6 min 较 EAG-PT 约 12×）；光源需手动 SAM 标记、依赖 2D 材质/法线先验是落地门槛；实时化（当前离线内容生产）是后续方向。

### 第 3 章 · LingGS：几何预测与相机跟踪解耦的高保真高斯 SLAM（2610.36853，4.15 A，FULL）

- **赛道 / 场合**：重建与SLAM / arXiv preprint（KAUST / 香港科技大学（广州））
- **公告类型**：cross
- **一句话结论**：LingGS 把冻结流式 3D 基础模型（LingBot-Map）当虚拟 RGB-D 传感器、用直接深度残差的显式几何求解器替代模型自带相机头，在 4 个数据集上渲染 PSNR 全部最高（较基线最高 +3.1 dB，Oxford Spires 26.35 dB）、深度 L1 全部最低，ATE 较相机头最高降 87.6%（跨 4 个骨干降 31.0–96.7%），单卡 RTX 4090 上约 7 FPS。
- **要解决的问题**：单目高斯 SLAM 需在有限在线算力内联合恢复相机位姿、几何与外观：依赖稀疏特征或增量优化难以高保真；密集深度联合优化增加在线开销，且逐帧深度存在跨帧尺度不一致。流式 3D 基础模型能输出一致密集深度与位姿，但作者观察到直接使用其回归位姿会产生跨帧错位，即使深度可用也限制重建质量。目标是在线获得一致的密集深度与相机位姿。
- **方法详解**：系统由三部分组成。①虚拟 RGB-D 传感器：冻结的流式模型 LingBot-Map 从初始帧固定相机内参 K，逐帧输出深度 D_t。②几何求解器（Sec.3.1）：基于 ORB-SLAM3（保留其特征提取、投影引导匹配与局部 BA），每帧提取 N_f=1200 个 8 层金字塔 ORB 特征；对 2D-3D 对应联合最小化图像重投影残差与直接深度残差 r_j(T)=[u_j-π_u(T x_j^w), v_j-π_v(T x_j^w), z_j-[T x_j^w]_z]（Eq.1），协方差 Σ_j=diag(σ_j², σ_j², (ε z_j)²) 且 ε=0.05，即恒定相对深度不确定度（区别于 ORB-SLAM3 把深度编码为虚拟右像坐标导致残差对深度误差呈 z⁻⁴ 敏感；直接深度残差权重为 z_j⁻²，附录 A.1 给出推导）；SE(3) 左扰动更新 T←exp((δξ)^∧)T，4 个外循环交替优化与外点重分类，Huber 鲁棒核。③高斯映射器（Sec.3.2）：Laplacian 引导插入——权重 w_t(p)=[ℓ(I_t)-ℓ(Î_t)]⁺（归一化离散拉普拉斯差），优先在渲染高频响应不足处新增高斯；几何初始化以深度反投影定中心，尺度 s=κz/f_x（κ=2，名义 2 像素足迹）、初始不透明度 0.07、颜色取像素值；随后按 OTF 方案以关键帧回放做 n=30 步精化，损失 L_j=0.8 L_rgb+0.2(1-SSIM)+λ_d L_depth（λ_d=0.01，逆深度空间 L1），每步以概率 p_last=0.2 选最新关键帧、否则均匀采样全部关键帧，用 gsplat 可微光栅器渲染。
- **实验与结果**：数据集 7-Scenes（室内）、Oxford Spires（室外 6 段 1000–2001 帧）、RE10K（60 段 71–279 帧）、TUM-D（11 段手持 fr1-fr3），全部 518×392 处理；基线 MonoGS、S3PO-GS、Photo-SLAM、OTF；硬件单卡 RTX 4090 + Threadripper PRO 3995WX。

主结果（Table 1）：7-Scenes PSNR 24.48（最佳）ATE 8.58 cm（次优）；Oxford Spires PSNR 26.35（最佳）ATE 73.81 cm（最佳）；RE10K PSNR 25.73（最佳）ATE 2.84 cm；TUM-D PSNR 20.89（最佳）ATE 41.33 cm（最佳）。摘要称渲染 PSNR 最高提升 3.1 dB。

深度精度（Table 2，渲染深度 L1，m）：7-Scenes 0.15 vs S3PO-GS 0.17（-11.8%）、TUM-D 0.33 vs 0.57（-42.1%）、Oxford Spires 3.18 vs 4.47（-28.9%），三数据集均最低。

跟踪消融（Table 3，Oxford Spires，ATE cm/RPE-t cm/RPE-R °）：虚拟立体 79.5/1.123/0.104；仅 2D 重投影 162.1/4.723/0.140（PSNR 掉 3.45 dB）；CPU ICP 307.2/15.14/0.482；模型相机头 598.5/15.39/0.259；本文 73.8/0.943/0.095。求解器仅增 6.6 ms，ATE 降 87.6%、RPE-t 降 93.9%，端到端 7.04→6.40 FPS。

骨干泛化（Table 4，Keble College-02）：XStreamVGGT ATE 23.277→0.773 m、STream3R 25.560→2.332 m、TTT3R 10.57→7.29 m、LingBot-Map 8.224→1.224 m；ATE 降 31.0–96.7%、RPE-t 降 64.3–97.1%、RPE-R 降 55.9–78.8%，每帧 16.1 ms。

映射迭代（Fig.2）：20→30 步 +0.93 dB，30→75 +0.88 dB，>100 步仅 27.11–27.15 dB 平台，默认取 n=30。
- **创新点与贡献**：['提出直接深度残差+恒定相对不确定度（ε=0.05）的位姿求解，替代 ORB-SLAM3 虚拟立体残差，附录从理论上证明虚拟立体对深度误差的 z⁻⁴ 敏感性并给出更自然的 z⁻² 权重。', '把冻结流式 3D 基础模型当作虚拟 RGB-D 传感器，与显式几何跟踪、增量高斯映射三者解耦组合，无需任何训练即达 SOTA 渲染质量。', '证明几何求解器可跨骨干迁移（XStreamVGGT/STream3R/TTT3R/LingBot-Map），为流式模型设计提供位姿-几何耦合的实证依据。']
- **局限与风险**：正文未设独立 Limitations 节（Conclusion 中陈述）：①系统不含回环检测，长程一致性无保障；②不处理动态场景；③依赖 ORB 特征提取与匹配，在重复纹理或弱纹理环境中对应可能歧义或缺失，跟踪受损；④深度质量受流式模型预测上限约束。此外 7-Scenes 的 ATE 次于 S3PO-GS/Photo-SLAM（对方位姿估计算力预算更大），深度 L1 对比基于四舍五入值计算。
- **与文献库的关系**：位于库内单目高斯 SLAM 线（MonoGS/S3PO-GS/Photo-SLAM/OTF）与冻结流式 3D 基础模型（DUSt3R/VGGT/CUT3R/TTT3R 一脉）之间；把冻结流式模型当虚拟 RGB-D 传感器、以直接深度残差+恒定相对不确定度（ε=0.05）的显式几何求解器取代学习相机头，附录从理论上证明虚拟立体对深度误差的 z⁻⁴ 敏感性并给出更自然的 z⁻² 权重。
- **可复现性**：Reproducibility statement 称源码与配置文件将在论文录用后公开（未给出 URL）；硬件单卡 NVIDIA RTX 4090+AMD Threadripper PRO 3995WX；依赖公开组件 LingBot-Map、ORB-SLAM3、gsplat；处理分辨率 518×392。
- **行动建议**：单目高斯 SLAM 新参照：4 数据集渲染 PSNR 全部最高（最高 +3.1 dB）、ATE 较相机头最高降 87.6%（跨 4 骨干降 31.0–96.7%）、单卡 4090 约 7 FPS；无回环、不处理动态场景、依赖 ORB 特征（弱/重复纹理受限）是部署缺口。

### 第 4 章 · StereoSplat：立体接地的度量尺度前馈 3DGS（2610.35902，4.07 A，FULL）

- **赛道 / 场合**：神经渲染 / arXiv preprint（University of Amsterdam & Meta，cs.GR，2026-09-29）
- **公告类型**：new
- **一句话结论**：StereoSplat 是首个面向立体视频的前馈 3DGS 框架，凭 FoundationStereo 立体先验在 KITTI 上达 AbsRel 0.04、δ₁ 96.0%（最强基线 DepthSplat 为 0.13/79.8%），并将 819k 个 primitive 压缩至 132k（6.2×）且渲染 236.9 FPS 为对比方法最快。
- **要解决的问题**：现有前馈 3DGS 方法缺乏可靠几何 grounding：pixelSplat、MVSplat 等靠 cost volume 或 cross-attention 隐式推断深度，几何带噪且只恢复到任意尺度；引入深度基础模型或 3D 基础模型（DepthSplat、AnySplat、NoPoSplat）的方法仍锚定在尺度模糊的 affine-invariant 表示，远处细节退化。这些方法把输入当通用无序图像，丢弃了相机标定与极线约束。立体设备/机器人平台本可经标定基线直接三角化出绝对度量深度，FoundationStereo 等立体基础模型也具备零样本视差估计与多尺度特征，但尚无工作把立体基础模型与显式 3DGS 场景表示桥接。
- **方法详解**：输入为 N 组校正立体图像对及外参、共享内参，学习 f_θ 直接预测世界坐标系高斯集合。Grounding module：冻结 FoundationStereo 作骨干，利用对极几何对称性，水平翻转计算右视差 d_i^R = flip(ℱ(flip(I_i^R), flip(I_i^L)))，再由焦距 f 与基线 b 换算度量深度 D_i^v = f·b/d_i^v，同一次前向还给出多尺度上下文特征金字塔。Gaussian decoder：每个尺度用轻量 cross-view transformer（pre-norm，注意力矩阵 2N×2N，每像素计算复杂度与 H_s×W_s 无关，注意力输出投影与末层 FFN 零初始化以恒等映射起步）融合左右特征；将全分辨率图像特征、log D 深度特征与跨视图增强金字塔上采样残差融合为全分辨率张量，用可学习标量门 α=σ(α₀) 混合立体深度与精化深度 D′=(1−α)D+αD̂（α₀ 初始化强偏立体深度），线性头回归高斯属性后按 K、T 反投影得初始集合 𝒢̃（|𝒢̃|=2NHW）。Gaussian aggregation：中心映射到逆深度坐标 [x/z, y/z, 1/z] 并以 δ 量化哈希（远处 unit 横向 δz、深度向 δz²，近处保细节远处强合并），哈希键附加量化 DC 颜色、尺度与不透明度防止跨不连续混合；簇内用温度缩放 softmax w_k=exp(z_k/τ)/Σ_{j∈𝒞}exp(z_j/τ)（τ=exp(log τ₀) 可学习，初始 τ=1 且权重头零初始化，初始等价 scatter_mean）做学习重要性加权聚合，离散分配下加权聚合仍可微。训练用 gsplat 可微光栅，L=0.8·L1_rgb+0.2·SSIM_rgb+0.05·LPIPS_rgb+0.5·L1_depth（深度项仅监督 [0,80] m 内有效 GT）。配套构建 XRStereo 合成数据集：137k 帧、20k 时序序列、13 个室内外环境、200 个资产、1K 分辨率校正立体对、FOV 50–130°、基线 40–120 mm。
- **实验与结果**：训练仅用合成数据（XRStereo+TartanAir+Infinigen 训练集）；评测 Infinigen 未见测试集、TartanAir v2、真实 KITTI（人工剔除动态片段）；基线为 VicaSplat、AnySplat、DA3-Giant、MVSplat†、pixelSplat†、DepthSplat†（†用 GT 位姿）。
Table 1（3 个立体帧窗口，StereoSplat 320×640，部分基线原生 256×256）：
数据集 | 方法 | AbsRel↓ | δ₁↑ | L1↓ | PSNR↑ | SSIM↑ | LPIPS↓
Infinigen | DepthSplat† | 0.21 | 63.0 | 7.1 | 26.8 | 0.91 | 0.13
Infinigen | Ours | 0.03 | 98.6 | 1.1 | 29.4 | 0.95 | 0.12
TartanV2 | DepthSplat† | 0.15 | 78.7 | 1.8 | 25.8 | 0.93 | 0.10
TartanV2 | Ours | 0.06 | 94.9 | 0.7 | 26.3 | 0.94 | 0.10
KITTI | DepthSplat† | 0.13 | 79.8 | 2.4 | 22.1 | 0.88 | 0.18
KITTI | Ours | 0.04 | 96.0 | 0.9 | 25.2 | 0.94 | 0.10
（VicaSplat/AnySplat 在 Infinigen δ₁ 低至 4.5/0.5；Ours 在三个数据集 PSNR 均最高）
消融：跨视图融合 None PSNR 22.8/L1 1.4 → Ours 25.2/0.9；聚合策略 No-Agg 23.3、Voxel 23.2、Learnable Vox. 23.3、Ours 25.2 且压缩率 1.6×；门控深度（KITTI）α=0 时 23.9/0.20、α=1 时 24.8/0.14、学习门 25.2/0.10。
效率（A100-80GB，4 视图，CUDA event 计时）：Ours 参数 65.0M、峰值显存 2.03 GB、Splats 819k→132k、总 1.7 FPS、渲染 236.9 FPS；DepthSplat 38.4M/6.14 GB/1,376k/5.2 FPS/59.5；AnySplat 1.19B/5.73 GB/776k→505k/1.9/157.2。运行时分拆：FoundationStereo 冻结骨干 558.5 ms（91.4%），decoder 43.9 ms，聚合 4.4 ms（34 参数），渲染 4.2 ms；GRU 迭代 12→8 加速 1.14×（AbsRel +0.6%），6 次 1.23×（+2.0%）。换 IGEV++ 骨干仍优于全部基线但 PSNR 落后 0.9–3.2 dB（KITTI 差距最大）。长视频可分块推理后拼接并少量优化，成功把 600+ 输入帧整合为全局一致表征。
- **创新点与贡献**：['首个原生面向立体视频设计的前馈 3DGS 框架，实现可泛化的度量尺度新视角合成，克服既有方法尺度歧义', '立体感知 Gaussian decoder：cross-view feature fusion + gated depth refinement，把度量立体深度当几何锚', '逆深度空间的距离自适应（depth-adaptive）聚类聚合机制，融合几何、外观与学习置信度压缩逐像素 primitive', '大规模合成立体视频预训练数据集 XRStereo（137k 帧、多种 rig 配置）显著提升真实数据零样本迁移']
- **局限与风险**：正文设有 Limitations and Future Work 节：① 依赖已标定立体对，不能用于未标定或单目采集；② 场景聚合假设静态环境，高动态视频下重建质量下降；③ 端到端重建速度受限于立体骨干（聚合后显存与渲染速度仍为对比方法最优）。未来方向为放松标定要求与扩展到动态场景。
- **与文献库的关系**：属库内前馈 3DGS 线（pixelSplat/MVSplat/AnySplat/DepthSplat/NoPoSplat），首个原生面向立体视频设计的前馈框架；FoundationStereo 立体先验当几何锚，XRStereo 数据集（137k 帧、多种 rig 配置）填补合成立体视频空白。
- **可复现性**：项目页 https://vladimiryugay.github.io/stereosplat ；训练 320×640、每样本 3 输入视图、AdamW、有效 batch 40、10 epoch（lr 1e-3 余弦衰减至 1e-5）、约 240 GPU 小时 NVIDIA H100；框架为 PyTorch + FoundationStereo 原始实现 + gsplat 光栅器；效率评测在单张 A100-80GB；代码/数据开源状态正文未明确声明（仅给出项目页）。
- **行动建议**：立体/XR 双摄采集的度量尺度 NVS 首选：KITTI AbsRel 0.04 / δ₁ 96.0%（DepthSplat 0.13/79.8%），819k→132k primitive（6.2×）且 236.9 FPS 最快；依赖已标定立体对与静态场景假设，未标定/单目采集与动态场景是开放方向。

### 第 5 章 · HoloRecon：前馈几何验证的长程全景一致重建（2610.36876，4.07 A，FULL）

- **赛道 / 场合**：重建与SLAM / arXiv preprint（香港科技大学（广州）/ 利物浦大学 / 香港理工大学 / 西交利物浦大学）
- **公告类型**：new
- **一句话结论**：HoloRecon 把前馈 Pi3 的局部几何用作 3D 证据验证远距离特征匹配并构建相机约束，在 360LOC/YUTO MMS/PanoRecon 三数据集取得最低平均 ATE（0.270 m / 3.527 m / 1.697 m）与最高 20 cm F-score（62.04 / 48.71 / 63.16），GPU 全景 BA 较 CPU 加速 4.31 倍且精度不降。
- **要解决的问题**：长序列全景（ERP）重建需要跨远距离重访的全局一致位姿与稠密几何：特征式全景 SLAM/增量 SfM 依赖特征对应，重复建筑纹理与小部分重叠使可靠长程连接难以建立（松阈值引入假回环、紧阈值拒掉真回环），累积漂移无法消除；前馈模型局部几何好但推理窗口受显存/算力限制，窗口间仍需全局约束。两者各有短板，需要耦合。
- **方法详解**：框架为「ORB 稀疏建图前端+微调前馈模型」的增量管线。Sec.3.1 锚定几何：前端（ORB 式 ERP 前端）增量估计相机-世界位姿 T_i 与稀疏路标 L_j；连续关键帧分组为含 4 帧重叠的 16 帧子图窗口，渲染为带标定透视视图交给在 Holo360D 上微调的 Pi3 预测局部几何；深度尺度经路标观测拟合共享窗口对数尺度 a_w 与逐帧修正 b_wi（Huber + λ_p=32 平滑 + λ_s=64 邻帧正则，修正裁剪至 ±log(1.05)，Eq.2），世界点 X_wiv=T_i(s_wi Q_v ẑ_wiv K_v⁻¹ p̄)，s_wi=exp(a_w+b_wi)（Eq.1）；另以轻量 sky head 替代逐视图天空分割网络，子图推理从 40 s 降至 13 s。Sec.3.2 长程连接：按体素重叠（0.25 m、η≥0.15）与视线可见性（≥0.6）挑候选子图，对全部关键帧对做互 ORB 匹配，用标定深度反投影为 3D 对应，RANSAC+最小二乘拟合 Sim(3) 相似变换 S_A←B；再做跨视角验证（双向距离 ≤0.3 map 单位、方位角 ≤1°、每侧 ≥3 关键帧各 ≥10 内点、每侧独有特征 ≥40、总内点 ≥60/大校正 ≥100、内点率 ≥0.35/0.50，大校正按均衡匹配数分组交叉验证并约束组间尺度/旋转/位移一致，Eq.9-10）；验证通过的变换转为相机约束 Ĝ_b←a=T_b⁻¹ S_A←B⁻¹ T_a（Eq.3），权重 w_e=clip(n_AB/3,10,100)/m_AB（Eq.11）。Sec.3.3 全局传播：相似位姿图优化（剔除不一致新边再重解）+ 路标融合使重访区域共享观测，随后 GPU 加速全景 BA（ERP 重投影残差带 wrap_W 处理接缝、Huber δ_b=5.99146、金字塔逆方差加权，Eq.4；BAE/PyPose 稀疏自动微分+matrix-free Schur+GPU PCG，双精度、≤250 次迭代、容差 1e-5）；最后用更新位姿重拟合尺度并重放缓存稠密点，不重跑推理。
- **实验与结果**：数据集 360LOC（4 场景）、YUTO MMS（4 序列、20.1 km、Sequence C 9.137 km/10,778 图）、自建 PanoRecon（7 场景，平均时长 11.49 min、0.1 s 采样、平均轨迹 0.87 km（0.26–1.69）、参考位姿重投影 RMSE 0.1917 px、Insta360 X4 5K 30fps、3 m 延长杆、RTK LiDAR）；基线 PanoVGGT、Scal3R、360DVO、Open-vSLAM、Stella-vSLAM、COLMAP（ERP 与 Pinhole）、Spherical-SfM；硬件单卡 RTX PRO 6000 Blackwell。

定位（Table 1，ATE/RPE-t/RPE-r）：360LOC Ours 0.270/0.030/0.044（次优 COLMAP-ERP 0.355）；YUTO MMS Ours 3.527/0.052/0.022（次优 Spherical-SfM 21.186，Scal3R 187.407，COLMAP-ERP 124.490）；PanoRecon Ours 1.697/0.111/0.086（COLMAP-Pinhole 1.736）。PanoVGGT 在单卡全部 OOM。

稠密重建（Table 2，20 cm P/R/F%）：360LOC 79.22/52.87/62.04；YUTO MMS 60.56/40.77/48.71；PanoRecon 64.22/62.36/63.16；三数据集 F 均最高（对照 COLMAP-Pinhole 57.25/17.28/59.75，Stella 58.68/17.24/31.97）。

BA 后端（Table 3）：GPU 求解 2.244 s/总 7.581 s/4.31× 加速，重投影 RMSE 0.8420 与 CPU 0.8466 相当。

全局约束消融（Table 4，Residence2）：无连接 ATE 1.358 m→PG 0.977→PG+BA 0.922→PG+fusion 0.877→PG+fusion+BA 0.708 m，融合使长程观测 160,186→293,827。

子图对齐迁移（Table 10，PanoVGGT+本文子图对齐于 Residence2）：ATE 26.831→4.203 m，F-score 4.40%→18.67%。

运行时（Table 9，Sequence C）：本文总计 181.38 min（Pi3 推理 38.96 min/257 窗口、连接匹配+验证 56.60 min、GPU BA 0.87 min/91 次），COLMAP-Pinhole 总计 1530.86 min。
- **创新点与贡献**：['提出长程全局连接机制：用前馈局部几何对跨视角 ORB 匹配做 3D 验证，在重访区域无共享稀疏路标时仍能建立 Sim(3) 相机约束（含分组交叉验证抗重复纹理）。', '提出「相互依赖」耦合范式：稀疏建图为前馈几何提供尺度与坐标锚定，前馈几何反过来为稀疏图提供约束证据；稠密几何以缓存+位姿重放方式更新，免重复推理。', '发布 PanoRecon 基准（7 场景、重复建筑、大小回环、RTK LiDAR 参考位姿与几何，重投影 RMSE 0.1917 px），填补全景全局一致性评测空白。']
- **局限与风险**：第 6 节 Limitations 明示：①严重运动模糊或长时间低纹理会削弱跟踪与深度标定所需的可靠特征观测；②不显式处理动态物体（行驶车辆、行人）；③尚未达到实时重建（Sequence C 总计 181.38 min）。另从实验看：依赖单卡 RTX PRO 6000 Blackwell，PanoVGGT 在其设置下 OOM；PanoRecon 平均轨迹 0.87 km 且重访部分重叠有限，更长距离/更高动态场景未验证。
- **与文献库的关系**：与库内全景 SLAM/SfM（PanoVGGT/Scal3R/360DVO/COLMAP-ERP/Spherical-SfM）及前馈几何（Pi3/VGGT 一脉）同域；差异在以前馈局部几何对跨视角 ORB 匹配做 3D 验证（含分组交叉验证抗重复纹理）建立长程 Sim(3) 约束，并提出稀疏建图与前馈几何相互依赖的耦合范式；发布 PanoRecon 基准（RTK LiDAR 参考位姿）。
- **可复现性**：项目页 HoloRecon（正文为超链接文本，未给出可提取 URL），未声明代码/数据开源细节；实验硬件单卡 NVIDIA RTX PRO 6000 Blackwell Workstation Edition；PanoRecon 数据由 Insta360 X4（5K 30fps）+RTK LiDAR 自采；依赖 ORB 前端、微调 Pi3、BAE/PyPose 与 g2o（CPU 后端）。
- **行动建议**：长序列 360 内容生产管线的全局一致性方案：三数据集最低平均 ATE（0.270/3.527/1.697 m）与最高 20 cm F-score，GPU 全景 BA 较 CPU 4.31×；运动模糊/低纹理与动态物体未处理，Sequence C 总计 181 min 未达实时。

### 第 6 章 · GeoGSplat：几何接地的非像素对齐高斯泼溅（2610.36760，4.00 A，FULL）

- **赛道 / 场合**：神经渲染 / arXiv preprint（西安交通大学 / EPFL / 地平线机器人 / 中国科学院大学）
- **公告类型**：new
- **一句话结论**：GeoGSplat 以固定 65,536 个高斯的非像素对齐预测结合 Anchor+Triplane 几何先验，在 DTU 与 NRGBD 上同时超越像素对齐与非像素对齐方法：DTU PSNR 20.48 dB（较 TokenGS +2.77 dB）、CD 0.018（较 TokenGS 0.082 降 78%），NRGBD PSNR 24.78 dB、CD 0.017，且目标视角离输入越远优势越大。
- **要解决的问题**：前馈高斯泼溅中，像素对齐方法（pixelSplat、MVSplat、DepthSplat、AnySplat）虽继承逐像素深度的几何约束，但高斯基元数量随图像分辨率与输入视图数增长、跨视图重叠区域产生冗余；非像素对齐方法（TokenGS、VolSplat）预测固定数量高斯，却丢弃了射线/深度约束，导致高斯基中心错位、过拟合观测视角，在大视角变化下出现严重渲染伪影。如何在保持固定高斯预算的同时恢复显式几何先验，是本文要解决的问题。
- **方法详解**：GeoGSplat 由双分支结构编码器+几何引导分层解码器组成。编码器：RGB patch 嵌入与 Plücker 射线嵌入相加后过标准 ViT（8 个 ViT block）得多视图特征 F_img；两组可学习 query Q^A（M=4096）与 Q^T（n_T=3S0²，S0=64）经共享注意力模块（12 个注意力 block）分别聚合出 Anchor 与 Triplane 特征。Anchor 为带可学习中心与自适应半径的稀疏 3D 球：中心由参考点加线性偏移经 tanh 约束在归一化场景体积内（Eq.4），半径以到 4 个最近 Anchor 的中位距离 d_i 乘以 sigmoid 有界因子生成（Eq.5）。Triplane 由三个正交 2D 特征面构成，经两级「双线性上采样×2+Triplane refinement block（残差卷积+跨面融合+图像条件交叉注意力）」从 64 逐级精化到 256 分辨率（Eq.6），任意 3D 坐标 x 经三面投影双线性采样拼接得到 ϕ(x)（Eq.7）。解码器分两级：Anchor-to-Point 在每个 Anchor 局部区域内初始化 K=16 个参考点，用 K 个可学习 token 对 Triplane 几何特征做交叉注意力预测偏移，并以半径 r_i 缩放得 K 个稠密 3D 点（Eq.8）；Point-to-Gaussian 在稠密点处重新查询 Triplane，经共享 MLP 与 Gaussian head 预测 (Δμ,α,s,q,c)，最终 μ_j=x_j+Δμ_j（Eq.9）。高斯总数 N=M×K=4096×16=65,536，与输入视图数/分辨率解耦。训练损失 L=L_geo+L_render：L_geo 为 Anchor 中心与稠密点对 GT 点云（输入视角有效深度反投影融合后 FPS 采样）的对称 Chamfer 距离（Eq.10）；L_render 为 L_rgb+λ_s L_SSIM+λ_p L_LPIPS；先用几何监督单独训练 15K 迭代再加入渲染损失。
- **实验与结果**：训练集 ScanNet++、ARKitScenes、BlendedMVS、CO3D、WildRGB-D（5 个）；评测 DTU（物体级）与 NRGBD（场景级），4 输入视图、4 新视角，256×256；指标 PSNR/SSIM/LPIPS 与 Chamfer 距离 CD。

NVS 4 视图（Table 1）：DTU PSNR 20.48/SSIM 0.771/LPIPS 0.137@65K，对比 TokenGS 17.71/0.643/0.354@65K、AnySplat* 17.54/0.700/0.148@166K、MVSplat 14.44@158K；NRGBD 24.78/0.847/0.120@65K，对比 TokenGS 23.82@65K、AnySplat* 20.52@624K（其高斯基数约为本文 10 倍）。

3D 重建（Table 2，CD↓）：DTU Ours 0.018 vs TokenGS 0.082、AnySplat* 0.025、MVSplat 0.166；NRGBD Ours 0.017 vs TokenGS 0.277、AnySplat* 0.042；TokenGS 在 NRGBD 上 Pred→GT 高达 0.515 而 GT→Pred 仅 0.039，显示其大量基中心偏离真值几何。

大视角变化（Fig.5）：目标-上下文距离增大时 GeoGSplat 对 TokenGS 的 PSNR 优势持续扩大。

消融（Table 3，缩小模型）：去 Anchor PSNR -1 dB 以上（DTU 18.67/NRGBD 22.46），去 Triplane 18.63/22.47，去 Anchor-to-Point 18.32/21.81，去 Point-to-Gaussian 18.71/22.35，去几何损失灾难性下降至 13.60/18.53（CD 0.218/0.135），Full 为 19.79/23.70（CD 0.019）。

视图数泛化（Table 5，不重训）：2 视图 DTU 17.53 dB/NRGBD 21.68 dB 附近领先；12 视图 DTU 22.53 dB/CD 0.014、NRGBD 25.21 dB/CD 0.015，高斯数恒为 65K。

重训对照（Table 4）：TokenGS-R 13.75 dB、加几何损失 14.41 dB，仍远低于 GeoGSplat 20.48 dB，证明增益源于架构而非数据或监督。
- **创新点与贡献**：['提出「几何接地的非像素对齐」前馈高斯范式：固定高斯预算 N=M×K 与显式几何先验兼得，兼弃像素对齐的冗余与非像素对齐的几何缺失。', '设计 Anchor（粗结构约束）+Triplane（细粒度可查询特征）的双分支互补场景表征。', '提出 Anchor-to-Point→Point-to-Gaussian 两级分层解码：先用 Anchor 几何约束重建稠密点，再在点上重查 Triplane 预测高斯，并以对称 Chamfer 几何监督贯穿始终。']
- **局限与风险**：正文未设独立 Limitations 节（据实验设置推断）：①仅在 DTU（物体级）与 NRGBD（场景级）两个室内数据集评测，室外/大规模场景与 Mip-NeRF 360 仅见附录；②训练成本高，需 128 张 NVIDIA L20、320K 迭代；③几何监督依赖输入视角的 GT 深度（反投影融合），无 GT 深度的场景需替代方案；④固定 65K 高斯预算对超复杂场景的容量上限未验证；⑤正文未报告推理速度与显存占用，实用性数据缺失。
- **与文献库的关系**：属库内前馈 3DGS 线非像素对齐一支（AnySplat/TokenGS/MVSplat/NoPoSplat）；以固定 65,536 高斯预算+Anchor（粗结构约束）与 Triplane（细粒度可查询特征）双分支互补表征，Anchor-to-Point→Point-to-Gaussian 两级分层解码，对称 Chamfer 几何监督贯穿始终。
- **可复现性**：项目页 https://comedy0913.github.io/projects/geogsplat （正文未明确声明代码开源）；训练配置：320K 迭代、AdamW、峰值 lr 4×10⁻⁴、BF16、128× NVIDIA L20、全局 batch 128、256×256 分辨率；推理硬件需求正文未述。
- **行动建议**：前馈 3DGS 新对比基线：DTU PSNR 20.48 dB（较 TokenGS +2.77）、CD 0.018（较 0.082 降 78%）、NRGBD 24.78 dB，且离输入视角越远优势越大；训练成本高（128×L20、320K 迭代）、依赖 GT 深度监督、室外/大规模未充分验证、未报推理速度。

### 第 7 章 · DomeGS：无界 3DGS 的感知一致背景补全（VR）（2610.37172，4.00 A，FULL）

- **赛道 / 场合**：渲染与显示 / arXiv preprint（雅盖隆大学；arXiv:2610.37172v1 [cs.GR] 2026-10-27；页眉为 IEEE vgtc 模板，疑投 TVCG/CG&A）
- **公告类型**：new
- **一句话结论**：N=36 完全被试内用户研究显示，相比传统无限 skybox，DomeGS 显著提升运动中的背景一致性（SKY Δ=+1.24，p<0.001，d=0.85）与沉浸感（IMM Δ=+0.44，p<0.001，d=0.35），IPQ 空间临场感（1.73 vs 1.41，p=0.042）与真实感（0.36 vs −0.07，p=0.042）显著更高，75.0% 参与者因更愿意久留而偏好 DomeGS，且眩晕程度与任务负荷无差异。
- **要解决的问题**：用 3DGS 重建无界室外场景时，远场（天空、远景立面、地平线）因多视图视差与几何标志缺失而无法重建，出现锯齿边界、漂浮伪影与空洞，破坏 VR 沉浸；传统做法是把全景图贴到无限远 skybox（cubemap）或手工搭建 skydome，前者与重建几何存在颜色/光照不一致与可见接缝、无平移视差，后者需定制 mesh 与 shader；已有生成式方法或生成全新环境、或把背景当独立 HDRI 处理，无法在场景一致性约束下补全现有 3DGS 重建的未观测周边，且其评估多在静态视点进行。
- **方法详解**：三阶段流水线。① 全景提取与外扩（Stage I）：虚拟全景相机置于轨迹质心 e=(1/K)Σt_k，剔除距 e 为 r+s_i^max 排斥球内的高斯得 G_pano，渲染等距柱状投影 I_0 并构造二值补全 mask M（M=1 为未观测天空/空洞）；用 360° 感知潜扩散模型（FLUX.2-klein-base-9B + 360 ERP LoRA）以 I_0、M 为条件全局外扩得 I⁽¹⁾，再循环平移 180° 使接缝重定位，对新边界处竖直条带 M_seam 二次 inpainting 得无缝全景 I⁽²⁾。② 场景自适应数据集（Stage II）：由 e 处 6 面 cubemap 可见高斯的深度分布估计球壳半径 R=m·Quantile_q({‖μ_i−e‖})（q=98%、m=1）；以 ψ*=argmax_ψ(|G(ψ)∩G_fg|/|G_fg|−λ_ψ|G(ψ)∖G_fg|/|G(ψ)|)（λ_ψ=0.3）求最优基准俯仰；用 180° yaw 翻转、俯仰偏离的 look-back 探针相机识别背面 floater 并剪除；在分层相机环（向下 p_down、水平过渡 p_scene、向上 p_bg）上按角色相关目标合成多视图监督 I_sup：向下视角直接用清理后场景渲染，过渡/天空视角用 I_G′(T)+I_bg(T)⊙(1−α(T))（α 为累积 2D 不透明度），I_bg 由相机射线与半径 R 包围球求交后采样 I⁽²⁾ 得到。③ 统一天空高斯优化（Stage III）：固定 r_f=max_k‖t_k−e‖ 内的高斯不动，在上半球壳 μ_j=e+r_jd_j（d_j∼Unif(S₊²)、r_j∼Unif([γR,R])、γ=0.99）播种种子高斯，尺度适配局部采样密度；联合目标 L=L_photo+λ_shellL_shell+λ_planL_plan，其中 L_photo=(1−λ_ds)‖Î_G−I_sup‖₁+λ_ds(1−SSIM)，径向壳损失 L_shell 惩罚 d_j=‖μ_j−e‖ 越出 [γR,R]，平面率损失 L_plan=(s_j^max/(s_j^min+ε))·(1−|a_j^min·r̂_j|) 抑制尖刺高斯；种子高斯免于剪枝/密度重置，背景高斯禁用尺度剔除，最终得统一场景 G=G′∪G_bg。
- **实验与结果**：用户研究：4 个室外无界 3DGS 场景（Panoramic：Buddha、Tower；Close：Garden、Bear），2×2 被试内设计（技术 × 场景类型），N=36（31 男 5 女，20–37 岁，M=26.2、SD=3.8；VR/AR 经验 M=0.8 年）；两条件共享同一前景高斯、同一补全全景 I* 与同一传送点布局；Meta Quest Pro + Unity 90 Hz（i7-14700K + 32 GB + RTX 4070 SUPER）。

微观探针 LMM（N=288，−3…+3 量表；Table 2）：
| 项目 | Δ(DomeGS−Skybox) | 95% CI | F(1,245) | Holm p | d |
| SKY 运动背景一致性 | +1.24 | [0.95, 1.53] | 70.70 | <0.001 | 0.85 |
| IMM 沉浸感 | +0.44 | [0.21, 0.68] | 14.01 | <0.001 | 0.35 |

场景级 SKY 对比：Buddha +2.08（p<0.001）、Bear +1.14（p=0.002）、Garden +1.08（p=0.004）、Tower +0.67 不显著（Holm p=0.225，该场景 Skybox 基线本身已高分）；technology×scene 交互显著（F(3,245)=4.10，p=0.007）。

IPQ（Wilcoxon + Holm 校正）：SP 1.73 vs 1.41（Δ=+0.32，p=0.042）、REAL 0.36 vs −0.07（Δ=+0.44，p=0.042）显著；G1/INV/Total 不显著（p=0.117/0.374/0.055）；内部一致性 α=0.86（DomeGS）/0.80（Skybox）。

偏好（非平手二项检验）：久留 75.0% vs 8.3%（p<0.001）、全景观看 69.4%（p=0.004）、总体沉浸 66.7%（p=0.004）、Close 场景 52.8% vs 22.2% 未达显著（p=0.0522，25.0% 平局为四项最高）。

任务负荷等效（TOST，Table 3；边界 ±60 s/±6 m/±2600°）：搜索时长 Δ=−6.7 s [−38.8, 25.4]（p_TOST=0.004）、头部路径 −0.40 m [−3.74, 2.95]（0.004）、转头量 −220° [−1694, 1254]（0.005）；SSQ 总分 16.5 vs 17.9（n.s.，轻度范围），前后累计不显著（14.4→18.0，p=0.931）。

Qwen3-VL-32B 自动视觉评测（Table 4，1–5 分；成对 −2…+2，位置交换）：均值 B/C/P：Skybox 2.71/2.98/2.91 vs DomeGS 3.63/3.71/3.63；成对偏好均值 +0.672（Tower +0.747、Buddha +1.083、Garden +0.475、Bear +0.383）。

生成器消融（Fig. 3/§4）：FLUX.2-klein-base-9B + 360 ERP LoRA 色彩一致性与接缝最优并用于 VR 条件；FLUX.2-dev 色彩不匹配、FLUX.1-Fill-dev 结构重复、512-inpainting-ema 地平线处不连续、Nano Banana 天空可见接缝。
- **创新点与贡献**：['把 skydome 思想落到高斯表示内部：远景不再是扁平背景壳，而是统一 3DGS 资产中有限半径球壳上的背景高斯，在头部平移时提供深度一致的运动视差', '360° 感知生成外扩 + wrap-seam 调和 + 角色相关 alpha 监督，实现与前景光照/色调一致的无接缝补全，且不破坏主重建（固定 r_f 内前景高斯、种子高斯免剪枝）', '系统化用户研究（36 人、2×2 完全被试内、微观探针 + IPQ + TOST 等效 + SSQ + 视觉语言模型自动评审）证明显著增益且无舒适度代价']
- **局限与风险**：正文未设独立 Limitations 节。从实验设置与讨论推断：① 仅 4 个室外场景、36 名被试，Tower 场景 SKY 优势不显著（Skybox 在该场景已高分，作者归因于其主要缺失为天空、恰适于无限远假设），Close 场景偏好未达显著（p=0.0522、25% 平局，近景密集几何已提供足够深度线索，远景增益被稀释）；② 补全质量依赖生成模型，不同生成器存在色彩不匹配/结构重复/接缝（Fig. 3），对遮挡严重或几何特殊的场景未验证；③ 壳厚 γ=0.99、q=98%、m=1、λ_ψ=0.3 等为全场统一设定，未做场景自适应；④ 单次会话（≈30–40 min，含 15–25 min HMD 暴露）未考察长期适应与学习效应；⑤ 论文以 skybox 为唯一基线，未与 EnvMap-GS 等 3DGS 补全方法定量比较。
- **与文献库的关系**：针对库内无界 3DGS 重建的地平线不完整问题（破坏 VR 沉浸），把传统 VR skybox/skydome 思想落到高斯表示内部：远景为统一 3DGS 资产中有限半径球壳上的背景高斯，头部平移时提供深度一致运动视差；360° 感知生成外扩+wrap-seam 调和+角色相关 alpha 监督实现无缝补全。
- **可复现性**：代码公开：https://github.com/Anastasiya999/DomeGS。硬件：Meta Quest Pro HMD（Quest Air Link，5/6 GHz Wi-Fi）、Unity 90 Hz、Intel Core i7-14700K + 32 GB RAM + NVIDIA RTX 4070 SUPER（Windows 11 Home）。生成模型：FLUX.2-klein-base-9B + 360 ERP LoRA（https://huggingface.co/nomadoor/flux-2-klein-9B-360-erp-outpaint-lora）；关键超参：R 分位 q=98%、m=1、λ_ψ=0.3、壳厚 γ=0.99；语料为 4 个既有室外 3DGS 重建（Garden、Bear、Buddha、Tower）。
- **行动建议**：VR 无界场景内容生产即用方案：N=36 用户研究 SKY +1.24（p<0.001, d=0.85）、IMM +0.44（p<0.001）、IPQ 空间临场感 1.73 vs 1.41、75.0% 偏好且无眩晕/负荷代价；Tower 场景不显著（skybox 已高分）、Close 场景偏好未达显著（p=0.0522），补全质量依赖生成模型。

### 第 8 章 · PrinGS：高斯泼溅的后训练隐私保护（2610.36168，3.92 A，FULL）

- **赛道 / 场合**：渲染与显示 / ICVGIP 2026（17th Indian Conference on Computer Vision, Graphics and Image Processing，2026-12-21 至 25，印度 Kolkata）
- **公告类型**：new
- **一句话结论**：PrinGS 是首个 3DGS 后训练隐私保护框架，直接在表征上匿名化敏感高斯：FSM 由标准 3DGS 的 83.87% 降至 9.79%（降幅 74.08%）且保留 FDR 39.47%，文本 OCR-CER 达 1.00（基线 3DGS 平均 0.208），后训练匿名化全程不到 1 秒。
- **要解决的问题**：3DGS 表示会编码人脸、车牌、文档、屏幕等敏感信息，分享/部署 splat 时从任意新视角都可恢复，带来 GDPR 与印度 DPDP Act 合规风险；个人要求删除时从零重训练计算上不可行，原始训练图像也常不可得、不可及或重采集代价高。图像空间后处理匿名化是视角相关的，底层 3D 表征不变，换视角即泄露；而在训练前模糊/遮挡图像会损害 COLMAP 等 SfM 管线的特征匹配与位姿估计，且逐视图修改造成跨视角不一致、破坏 3DGS 优化稳定性。此外现有 3DGS 基准普遍缺少人脸等敏感内容，缺乏系统评测手段。
- **方法详解**：表征级框架，输入为已训练 splat + 用户参考视图 + 对应 2D 二值隐私掩码。3D 敏感高斯分割（Algorithm 1）：在可微光栅化 alpha compositing 阶段追踪每个重叠高斯的累积透射率 T_i，仅当 T_i>τ_T 时按像素是否落在掩码内原子更新 c_true/c_false 计数器，单视图判据 c_true>c_false；因投影歧义会使背景几何落入掩码，再对标记高斯的 3D 空间坐标 μ_i 跑 Isolation Forest 剔除空间离群 floater；多视图聚合维护全局可见性计数器 C_i，最终敏感子集 S={g_i∈𝒢 | C_i≥τ_v}。高斯匿名化：对每个敏感高斯取 k 近邻 𝒩_k(i)，迭代加权平均更新 θ_i^(t+1)=Σ_{j}w_j θ_j^(t)/Σ_j w_j。人脸匿名化只改外观参数（SH 系数 θ_i=c_i）并用尺度依赖权重 w_j=f(s_j)，让小尺度高频细节（眼、鼻、唇）被大尺度结构 splat 引导混色，从而剥离身份特征但保留头部几何；文本匿名化同时改外观与几何（θ_i={c_i, μ_i}）并用均匀权重 w_j=1，溶解字符颜色与物理形状。Post-training 设置用单视图分割+直接改写静态表征；privacy-by-design 设置在标准 3DGS 训练迭代（如 30K）收敛后做多视图分割再匿名化（保住已学几何），文本则用反转掩码 masked loss L=(1−λ)L1(I⊙M̄_v, Î⊙M̄_v)+λ L_D-SSIM(I⊙M̄_v, Î⊙M̄_v) 排除文本区域光度监督，并周期性中断训练循环施加多视图分割+均匀结构匿名化，压制浮动几何形成的可读结构。
- **实验与结果**：单张 NVIDIA RTX 3090 Ti 24GB；每第 8 帧留评测；人脸基准 PrinGS-Humans（Blender 合成 2 个室内场景、9 个主体、跨肤色/年龄/性别/发型/胡须）；文本隐私数据集为 Tanks&Temples 的 Truck/Barn/M60 + DL3DV-10K 的 Car/Piano；掩码用 SAM3 生成；指标为 InsightFace（SCRFD-10GF 检测 + ArcFace ResNet-50 512 维嵌入余弦相似度 FSM）、FDR、Google Cloud Vision OCR 的 recall-based CER。
Table 1（PrinGS-Humans，FSM↓/FDR↑，%）：
场景 | 3DGS FDR | 3DGS FSM | Ours FDR | Ours FSM
House | 91.67 | 78.68 | 36.11 | 6.55
Hospital | 97.50 | 88.55 | 42.50 | 12.70
Overall | 94.74 | 83.87 | 39.47 | 9.79
Table 2（OCR-CER↑）：3DGS 平均 0.208（Truck 0.500、Barn 0.028、M60 0.207、Piano 0.149、Car 0.158），Ours 全部场景 1.00（完全不可读）。
Table 3 后训练匿名化运行时：House(P1) 592K 高斯/1531 敏感、k=25、t=30、0.70 s；House(P2) 592K/1213、k=40、t=30、0.57 s；Hospital(P4) 538K/1334、0.62 s；Hospital(P2) 538K/1127、0.52 s；Truck 2052K/2551、k=100、t=1、0.24 s，均 <1 s。House 上增大 k 与 t 持续降低 FSM 但会饱和，之后转为视觉美学控制。
- **创新点与贡献**：['首个面向 3DGS 的后训练隐私保护框架：无需原始训练图像、无需重训练，1 秒内完成表征级匿名化，敏感信息从所有新视角永久移除', 'privacy-by-design 训练策略：把表征级匿名化（多视图分割+loss 掩码+周期性干预）集成进 3DGS 优化，防止敏感特征在训练期被编码', '构建首个 3DGS 人脸隐私基准 PrinGS-Humans（9 个合成主体、跨人口学属性）', '提出 FSM/FDR/OCR-CER 任务专用隐私度量，弥补 PSNR/SSIM/LPIPS 只测保真度不测隐私的空白']
- **局限与风险**：正文未设独立 Limitations 节（结论仅作展望）。从实验设置推断：① 人脸匿名化保留头部几何轮廓，FDR 39.47% 表明匿名化后人脸仍可被检测为脸，只是身份嵌入不可再匹配（作者称 FDR 同时反映保留的几何与丢失的面部特征）；② 后训练设置缺 ground-truth 图像，正文只给定性结果与受控定量（在补充材料）；③ 作者自述若敏感高斯与场景结构深度纠缠，回顾性修改可能留有痕迹，这正是引入 privacy-by-design 的动机；④ k/t 超过收敛点后收益主要转向视觉美观；⑤ 掩码依赖 SAM3 质量。
- **与文献库的关系**：库内首个 3DGS 隐私工作：给定训练后 splat 与用户参考视图，定位敏感区域并直接在 3D 表征上匿名化，无需原始训练图像与重训练；配套 privacy-by-design 训练策略（多视图分割+loss 掩码+周期性干预）防止敏感特征在训练期被编码，并构建首个 3DGS 人脸隐私基准 PrinGS-Humans。
- **可复现性**：项目页 PrivacyPreserving3DGS.github.io（列于作者联系处）；实验硬件为单张 NVIDIA RTX 3090 Ti 24GB；依赖 SIBR 查看器渲染参考视图、SAM3 分割、InsightFace（SCRFD-10GF+ArcFace）与 Google Cloud Vision OCR；指标与协议细节称在补充材料；代码/数据开源状态正文未明确声明（仅给出项目页）。
- **行动建议**：3DGS 资产分享/部署前的隐私审计与匿名化工具：FSM 83.87%→9.79%（-74.08%）且保留 FDR 39.47%、OCR-CER 1.00、匿名化 <1 s；FDR 表明匿名化后人脸仍可被检测为脸（身份嵌入不可再匹配）；后训练设置缺 GT 图像、深度纠缠场景的回顾性修改可能留有痕迹。

### 第 9 章 · ParetoGS：稀疏适配锚点的连续预算高质量 3DGS（2610.34235，3.85 A，FULL）

- **赛道 / 场合**：渲染与显示 / arXiv preprint（浙江大学）
- **公告类型**：补录
- **等级说明**：【补录】2610.34235 属 2026-10-27 公告批次：10-28 运行曾入候选池并完成 digest，但候选→评分环节静默丢失未入馆；10-29 listing 对账重新发现，补入本批评分池，诚实标注非 10-28 公告批次新提交。
- **一句话结论**：嵌套锚点+残差图集解码任意预算：10%保留率约162K高斯达27.17 dB（超CLOD-3DGS 25.59/303K、MGS 25.74 dB）；附加状态390.0→85.7 MB，质量几乎不变。
- **要解决的问题**：可缩放3DGS欲用一个资产服务多预算，但减员同时改变留存成员承担的重建任务，继承参数难拟合低预算表示；CLOD-3DGS微调随机前缀、MGS联合训练、FlexGS条件变换、NanoGS无监督合并的质量-预算曲线仍落后逐预算单独优化，且需重复训练或多资产。
- **方法详解**：ParetoGS把连续预算表示为嵌套成员轨迹与预算特化参数状态的联合轨迹。锚点构建：从Full起每阶段用GNS收缩到下一目标预算（15K–18K）再固定成员适应至25K，得到严格嵌套、持久身份对齐的11个锚点（约2倍递增，0.1%→100%），删除记录反转为进入序π。分层残差图集：以Full为公共参考，按成员层×参数域堆叠各锚点残差，沿锚点状态维正交分解、高阶SH沿通道维低秩（45通道取rank-36），INT8块量化+FP16量化尺度。分段解码：请求数K∈(L,U)时，前L个共享成员按θ(K)=(1-t^p)θ(L)+t^pθ(U)插值（t=(K-L)/(U-L)），进入成员取上锚几何外观、透明度按t^q门控；p、q每区间在≤10个训练视图上枚举校准（网格P 9×Q 8，惩罚回退与斜率偏差），仅存两个标量。
- **实验与结果**：13场景（Mip-NeRF360 9+T&T 2+Deep Blending 2），RTX 4090，Full 30K+11锚点。等保留率：10%时27.17 dB/0.821/0.269、约162K高斯，CLOD-3DGS 25.59 dB/303K、MGS 25.74 dB/492K；0.1%时21.15 vs 8.15/14.79 dB；四个低保留率对MGS平均+3.50 dB。共享Full：5%时26.48 vs FlexGS-imp 24.03 dB。离线构建10.3 min（CLOD-3DGS约35、MGS约74、FlexGS-imp约81）。消融：同ID成员配Full参数PSNR由25.47跌至17.07 dB；编码FP32 390.0→Atlas 85.7 MB（-78.0%）质量几乎不变；预算切换构造P95 2.77 ms；资产较FlexGS-imp约+17%。
- **创新点与贡献**：①将连续预算3DGS形式化为嵌套成员轨迹与预算特化参数状态的联合轨迹；②持久身份+对齐残差编码+分段插值/门控解码，任意整数预算无需逐点优化；③13场景多预算对比、非锚点曲线与锚点消融验证“适应态”价值，并以紧凑图集存储整个锚点族。
- **局限与风险**：正文未设独立Limitations节。风险：锚点过稀疏时连接质量下降（Garden 5/3/2锚点SSIM 0.6569→0.6180）；依赖GNS/ImprovedGS按场景优化；资产较FlexGS-imp约多17%存储；解码需GPU驻留相邻锚点；区间校准仅用≤10个训练视图。
- **与文献库的关系**：属库内 3DGS 压缩/预算线（Scaffold-GS→HAC→ContextGS/Budgeted-GS/RLSplat/RacerGS 一脉）：把连续预算表示为嵌套成员轨迹与预算特化参数状态的联合轨迹，GNS 收缩构建 11 个严格嵌套锚点（0.1%→100%），分层残差图集（成员层×参数域正交分解、高阶 SH 低秩、INT8 块量化）+分段插值/门控解码任意整数预算。
- **可复现性**：Project page: https://xiaobin2001.github.io/ParetoGS-Web/；附录A给出成员排序、残差编码、区间校准与解码完整流程，附录B逐场景结果，附录C预算切换计时协议；实验用RTX 4090（data_device=GPU）；代码开源声明摘要级未明示。
- **行动建议**：可缩放 3DGS 资产服务（一资产多预算）首选：10% 保留率 27.17 dB 超 CLOD-3DGS 25.59/303K、MGS 25.74/492K（162K 高斯），附加状态 390.0→85.7 MB（-78.0%）质量几乎不变，离线构建 10.3 min（CLOD-3DGS 约 35、MGS 约 74）；锚点过稀疏时连接质量下降（Garden SSIM 0.6569→0.6180）、解码需 GPU 驻留相邻锚点、区间校准仅用 ≤10 训练视图。

### 第 10 章 · SOMA：第一视角细粒度人体运动理解基准（2610.36384，3.79 A，FULL）

- **赛道 / 场合**：评估与数据集 / arXiv preprint（École Polytechnique Fédérale de Lausanne, EPFL，cs.CV，2026-10-26）
- **公告类型**：new
- **一句话结论**：SOMA 以 1,632 道人工验证选择题横评 37 个 MLLM：人类平均 68.5%，最强模型 Qwen3.6-27B 仅 50.0%（零样本），最大差距在 Repetition Counting（人类 88.9% vs 最佳模型 43.6%，差 45.3 分），并首次量化 MLLM 的右手偏置（平均右手 78.8% vs 左手 44.3%）与系统性少数偏差（24/37 模型少数）。
- **要解决的问题**：现有 MLLM 视频评测聚焦物体、场景与粗粒度动作，几乎不评估对身体本身（某一时刻的身体配置、动作如何随时间展开）的推理能力；第一人称视角下身体仅部分可见，细粒度运动动态（重复计数、运动方向）难以察觉，运动模糊与视角快速变化要求跨帧整合 ego-motion 线索。现有 egocentric 基准（EgoTaskQA、EgoSchema、EgoThink、EgoGazeVQA、EgoTempo、LEMONADE 等）瞄准长视频理解或目标任务推理，无一直接测量「运动中的身体」，因此无法判断 egocentric 视频上的进步源于人体运动理解还是物体/场景识别。
- **方法详解**：SOMA（希腊语「身体」）为多模态基准：12 个任务归入三大能力轴——Body Configuration（Hand Use、Bimanual Coordination、Body Posture、Concurrent Body-Part State）、Motion Dynamics（Repetition Counting、Movement Direction、Opposite Motion Discrimination）、Temporal Reasoning（Adjacent Action Identification、Chronological Ordering、Missing Event Inference、Next Action Prediction、Repeated Event Reasoning）。数据源为 Nymeria 与 Ego-Exo4D，利用其原子动作标注 𝒜 与 Nymeria 的姿态/手/腿运动叙述 ℳ。构造管线：LLM selector 先定位任务相关子序列，LLM generator（均实现为 Gemini 2.5 Flash）再生成 1 正确 + 3 任务特定干扰项的多项选择题，共产 3,928 候选；Repetition Counting 因叙述无法可靠计数改为人工标注；盲语言过滤用 Gemini 2.5 Flash、GPT-4o、Qwen2.5-72B、InternVL3-78B 在无视频条件下作答，剔除至少 2 个答对的题目（删除 45.9%），余 2,127 题进入人工审核（接受 945、修改 586、删除 596，连同 101 道人工计数题共 1,632 题，来自 397 段视频的 1,611 个片段，平均时长 35.6 秒，答案位置已平衡）。另发布 SOMA-Train：28,596 个 QA 对、110.2 小时对齐视频与身体运动（按 Patel et al. 2025 从多视角录像以 20 fps 重拟合 3D 人体运动，转 263 维表征，与评测集在受试者与场景级不相交）。身体感知基线：Qwen3-VL-8B 与 InternVL3.5-8B 加 VQ-VAE（卷积编码器，在 156,659 段 64 帧/20 fps 运动片段上预训练，取预量化连续特征、每 4 帧一个、全程冻结）+可训练 MLP 投影为 motion tokens；两阶段训练（Stage 1 运动-语言对齐 1 epoch、lr 1e-3、global batch 16；Stage 2 LoRA rank 128/α=256/dropout 0.05、2 epochs、lr 5e-5、bf16+gradient checkpointing、8×H100、per-device batch 6/global 48）。
- **实验与结果**：37 个模型（闭源 Claude Sonnet 5/Opus 4.8、GPT-5.6 Luna/5.1、Gemini 3.5 Flash/2.5 Pro/Flash；开源 Qwen3.8/3.6/3.5/3-VL、InternVL3.5、Gemma-4、GLM-4.6V、Kimi-VL、MiniCPM-o、Molmo2、LLaVA-OneVision-1.5、VideoLLaMA3；egocentric 专用 EgoGPT-7B、EgoVLM-3B、EgoThinker-7B），lmms-eval 评测、零样本、temperature 0、16 帧均匀采样。
Table 2 关键结果（准确率 %，Avg.）：人类 68.5（RC 88.9、HU 90.5、NAP 34.5、CBS 50.3）；Qwen3.6-27B 50.0（最佳）；Gemini 3.5 Flash 47.0（最佳闭源）；Qwen3.8-27B 47.0；Claude Opus 4.8 44.8；Qwen3.5-27B 49.5；随机 25.0；多数 egocentric 专用模型 30.8–35.8。人-模型差最大任务：RC 45.3、RER 25.4、BC 25.3；在 CBS（−1.1）与 NAP（−10.0）上人类无优势甚至落后。
推理时策略：帧数 1→16 平均 +5.4 分（模型间 1.2–10.3），16→64 至多再 +0.5；test-time thinking 仅 Qwen3.5–3.8 家族 5 个模型提升 1.0–10.2 分，其余 7 个持平或下降。
错误分析：右手偏置（37 模型平均，右手类 78.8% vs 左手类 44.3%；5 名人类 92.7/89.8 无偏）；RC 上 24/37 模型倾向少数（人类 88.9% vs 最佳模型 43.6%）；对 Qwen3.8-27B 与 Gemma-4-31B 各 200 道错题分四类：Motion and Body-State Perception 为 Body/Motion 轴主因，另有 Temporal Localization、Visual Grounding、Prior-Driven Inference。
微调（Table 3，%）：Qwen3-VL-8B 零样本 35.39 → Motion-only 28.21 → Video 41.49 → Video+Mot. 42.44；InternVL3.5-8B 35.20 → 29.54 → 41.42 → 41.93；motion 对 Body/Temp. 轴小升、Motion Dynamics 轴因 backbone 而异（Qwen 升、InternVL 微降）。
- **创新点与贡献**：['首个面向 egocentric 视频细粒度人体运动理解的多模态基准：12 任务/3 能力轴、1,632 道人工验证题、397 段源视频，填补身体感知评测空白', '数据构造管线含盲语言过滤（剔除 45.9% 语言可猜题）与视频+同步 3D 身体姿态渲染辅助的人工审核，保证题目必须靠视觉作答', '配套 SOMA-Train 训练集：28,596 QA、110.2 小时视频+身体运动+语言三模态对齐（20 fps、263 维表征），现有 egocentric 基准均无此组合', '横评 37 模型 + 5 人基线（>450 小时），系统量化右手偏置、少数偏差与四类推理错误，并验证 motion token 的互补但有限收益']
- **局限与风险**：正文未设独立 Limitations 节（结论仅作展望，另有 Ethics 声明）。从设置推断：① Repetition Counting 精确计数依赖人工标注（叙述不可靠），规模受限；② 盲语言过滤以 4 个 LLM 多数共识为准则，可能残留可被更强语言先验猜测的题目；③ SOMA-Train 生成未经人工验证，质量靠去偏验证流程保证；④ 自研基线为 vanilla LLaVA/MotionLLM 式融合，video+motion 增益有限且任务相关，不能否定其他融合架构；⑤ 运动覆盖依赖 Ego-Exo4D 重拟合（自建 20 fps 覆盖 96.6% vs EE4D-Motion 37.9%），Nymeria/Ego-Exo4D 域多样性限定泛化结论；⑥ 伦理声明提示该能力可能被用于监视或行为画像。
- **与文献库的关系**：区别于库内 Ego4D/EgoPlan/InteractiveWorld 等第一视角基准（对象/场景/粗动作），首个面向身体本身的细粒度感知基准（12 任务/3 能力轴）；数据构造含盲语言过滤（剔除 45.9% 语言可猜题）与视频+同步 3D 身体姿态渲染辅助人工审核；配套 SOMA-Train（28,596 QA、110.2 小时三模态对齐）。
- **可复现性**：承诺 Full benchmark, training data, and code will be released at: cnai.epfl.ch/soma（论文接受后公开，正文未给代码仓库地址）；评测框架 lmms-eval、零样本、temperature 0、每段 16 帧；微调硬件 8×H100（LoRA，global batch 48）；运动表征 263 维、20 fps；人类评测 5 名付费标注员、共 >450 小时；提示模板与实现细节见附录 C/E。
- **行动建议**：可穿戴助手/XR 感知研发的必用评测台：人类 68.5% vs 最强 Qwen3.6-27B 50.0%，Repetition Counting 差 45.3 分；首次量化右手偏置（78.8% vs 44.3%）与系统性少数偏差（24/37 模型）——模型选择的重要警示；精确计数依赖人工标注规模受限，SOMA-Train 生成未经人工验证。

## 四、当日全量 7 维度对比表（参考）

见 [`papers/daily/2026-10-29/7dim-table.md`](../papers/daily/2026-10-29/7dim-table.md)。

## 五、覆盖率校验与筛选过程说明

- 门①（同质去重）：最大 Jaccard 0.308 < 0.62，通过，无同质重复。
- 门②（赛道覆盖）：纯值 Top10 仅覆盖 4 赛道 → 按重筛闭环剔除重复赛道最低分 SG²SLAM（4.00，重建与SLAM 第 4 篇），回补未覆盖赛道最高分 SOMA（3.79，评估与数据集）→ 定稿 Top10 覆盖 5 赛道（≥5），通过；SG²SLAM 仍入馆并写笔记（A 级），仅不占 Top10 名额。
- 门③（价值天花板）：当日最高分 4.30 < 库内近 30 天 Top10 均分 4.417（现算，435 条入窗）→ 非重磅日、无 S 级，未拔高、未凑数；达 S 线的 RESPLE2 4.30 / GraftRay 4.20 按校准关记 A。
- 三关均未触发重筛（门② 的回补即重筛闭环动作）；OUTDATED/SUPERSEDED 0 篇。

## 六、附录：证据等级分布与抓取记录

- FULL 10 篇；PARTIAL 1 篇；ABSTRACT_ONLY 0 篇（2610.36014 Immersive Commons 为 L1 ar5iv 仅摘要页 4,706 字符，已在 7 维表与笔记显式声明并按摘要级评估）。
- 抓取降级：无 L5；无 OCR；无伪造。串行 3s/篇，无限流。
