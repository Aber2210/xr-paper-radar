# XR Backfill 报告 · backfill-1114（旧稿 v2/v3 再公告首次入馆）

## 一、执行摘要
- **诚实口径**：本批 8 篇均为 **11-13 公告批次 RSS 混入的旧稿 v2/v3 再公告**（原始投稿 2025-08-22 / 2025-10-04 / 2025-12-10 / 2026-03-01 / 2026-03-10 / 2026-05-20 / 2026-07-06 / 2026-07-15；API `updated` = 2026-11-11×7 / 2026-11-12×1），首次入馆；**均非 11-13 当日新提交**，单独编号、不参与当日重磅日判定。
- **定稿 4 A / 4 B**，最高 **2603.01178 riMESA 4.50**（协同 SLAM 后端：28 个真实数据集平均最优性差距 **45.09%**，比 DLGBP 352.81% 低约 7.8×、比 DDF-SAM2 787.30% 低约 17.5×；2,430 个合成数据集 + 实时 + 开源；**达 S 线但按口径一律记 A**）。其余：Instant NuRec 4.28（~1.5 s 重建 10–20 s 多相机日志，Waymo PSNR 28.26 / 动态区 24.93 vs 21.76） · OMG4 3.80（2087 MB→3.59 MB、57→129 FPS） · AVI-HT 3.73（手套式 3D 手部追踪视觉-IMU 融合，证据链最完整） · ENIGMA-360 3.49（全量开放的 ego-exo 工业数据集） · GUSH3R 3.42（单目前馈人体-场景高斯） · COSMO-Bench 3.34（协同 SLAM 优化基准，但无后端基线） · ReflFlow 3.00（动态高光光线追踪，HyperNeRF 上仍落后 4DGS）。
- **全文**：8 篇全部 L0/FULL（47,054–149,662 字符）。
- **剔除**：同批 v2/v3 未入馆 17 篇中 9 篇经摘要核实非 XR（MedGS 医学 / BLaFA 抓取 / 空间句法户型 / 虚拟夹具 / 液体防溢 / 黎曼采样规划 / VLA 推理解码 / LLM 连续扩散 / SWAM 世界动作模型）。

## 二、排行榜（按加权降序）

| 排名 | 论文 | 赛道 | 总分 | 等级 | 证据 | 落后标记 |
|---|---|---|---|---|---|---|
| 1 | riMESA：面向真实世界协同 SLAM 的共识 ADMM（2603.01178） | 重建与SLAM | 4.50 | A | FULL | — |
| 2 | Instant NuRec：面向驾驶场景仿真的前馈三维高斯重建（2607.14203） | 世界模型与仿真 | 4.28 | A | FULL | — |
| 3 | OMG4：面向高效动态场景表示的优化最小 4D Gaussian Splatting（2510.03857） | 神经渲染 | 3.80 | A | FULL | — |
| 4 | AVI-HT：面向手套式 3D 手部追踪的自适应视觉–IMU 融合（2605.21714） | 交互与输入 | 3.73 | A | FULL | — |
| 5 | ENIGMA-360：面向工业场景人类行为理解的自我–外部视角数据集（2603.09741） | 评估与数据集 | 3.49 | B | FULL | — |
| 6 | GUSH3R：单目视频前馈式动态人体–场景高斯重建（2607.05243） | 重建与SLAM | 3.42 | B | FULL | — |
| 7 | COSMO-Bench：协同 SLAM 优化基准（2508.16731） | 评估与数据集 | 3.34 | B | FULL | — |
| 8 | ReflFlow：几何引导光线追踪的动态高光重建（2512.10095） | 渲染与显示 | 3.00 | B | FULL | — |

## 三、逐篇深度解读

### 第 1 章 · riMESA：面向真实世界协同 SLAM 的共识 ADMM（2603.01178，4.50 A，FULL）

- **赛道 / 场合**：重建与SLAM / arXiv preprint（cs.RO）
- **公告类型**：replace（公告日 2026-11-13，拉取日 2026-11-14）
- **等级说明**：backfill 不参与重磅日判定，≥4.2 按口径记 A
- **一句话结论**：riMESA 把流形上、可分的 edge-based C-ADMM（MESA+）增量化为随通信机会摊销的异步后端，并用 riSAM/GNC 做局部鲁棒优化、RWBP 与对偶衰减处理过时约束；在 28 个真实数据集上平均最优性差距 45.09%，比 DLGBP 的 352.81% 低 7.8×、比 DDF-SAM2 的 787.30% 低 17.5×，并在 2430 个合成数据集、7 类 C-SLAM 场景上保持实时与一致。
- **要解决的问题**：真实部署给 C-SLAM 后端提了三重约束：只能依赖 ad-hoc、稀疏、时变、常断连的网络（0.1–10 Hz 成对异步通信，还可能出现只有一方感知失败的 Two-Generals 故障）；前端因感知混叠必然产生外点，而 NLS 对外点极敏感；下游规划导航要求在线输出。现有方案各有硬伤：集中式需每步连通且单点故障、难扩展；去中心化要求更大带宽与冗余算力；分布式批式方法（MB-ADMM、DGS、GeoD、MM-PGO、DC2-PGO、ASAPP）需数百至数千次迭代，无法在单步内收敛，且要求当前时刻网络连通。真正面向增量分布式的只有 DDF-SAM2 与 DLGBP，但前者不约束共享变量的线性化点、无法收敛到一致解，后者基于 Loopy BP、连凸问题都不保证收敛，二者精度在真实数据上很差。鲁棒化组合（M-Estimator、PCM/GkCM、变量增广、GNC）又会继承各自的低效或初值敏感。
- **方法详解**：问题：Θ_MAP=argmin Σ_i Σ_{m∈M_i}||h_m(Θ_i)−m||²_Σm，增量鲁棒版每步只优化内点集 I_i 并给定上一步解；内点用 χ²(T) 阈值定义。C-ADMM 对每条边引入 i 持有的 z_(i,j) 与 j 持有的 z_(j,i)，把 x_i=z_(i,j)、x_j=z_(j,i) 拆开，按 x、z、λ、β 四步迭代。C-SLAM 可分：机器人只观测 Θ_i，共享集 S_(i,j)=Θ_i∩Θ_j，采用 SOVA 式约束 A_(i,j)x_i=B_(i,j)x_j，并把标量约束换成流形约束 q_s(θ_si,θ_sj)=0。为复用 NLS，把对偶项与惩罚项并为 biased prior，得 (β/2)||q_s(θ,z)+λ/β||²_Σs；因 SE(N) 平移（±D 米）与旋转（±π）量纲差数个量级，需加权 Σ_s（σ_r=0.1、σ_t=1）。约束函数比较 geodesic、apx-geo、split、chordal，geodesic 配 SPLIT(θ_si,θ_sj,0.5) 有闭式 z 更新且实验最好。riMESA 三处改造：①摊销，把约束收紧摊到每次通信机会，中间解仍可用，局部更新调 riSAM；②鲁棒，局部目标外包核 ρ，并把 biased prior 也包核（RWBP），使机器人可把过时约束当外点拒绝；③对偶衰减 λ^{k+1}=𝔡λ^k+β^k q_s(·)，𝔡=0.9；未初始化 RWBP 用 β_uninit=1e-4，初始化后 β 固定 1.0。
- **实验与结果**：
    - 规模：2430 个合成数据集（R=6 机器人、3D 无障碍环境、1000 位姿轨迹、回环外点率 10%–25%）+ 28 个真实数据集（COSMO-Bench 24 个 + Nebula 4 个）。
    - 泛化实验（7 类场景）：C-PGO、Range-Aided PGO、Range-Only、Bearing-Range-Only、Landmark、Landmark+Direct、Unconstrained 3D C-PGO，各 20 个随机数据集；riMESA 最接近使用 oracle 外点信息的集中式上界，仅在低秩机间测量 + 大噪声时退化。
    - 真实精度（Table II/III）：相对 Centralized GNC 的平均最优性差距为 riMESA 45.09%、kiMESA 157.70%、DDF-SAM2 787.30%、DLGBP 352.81%，即比 DLGBP 低约 7.8×、比 DDF-SAM2 低约 17.5×。
    - 一致性：riMESA 是唯一在全部真实数据集上都不出现灾难性失败的方法（DDF-SAM2 在 ntu_r4_00_proradio 崩溃、DLGBP 在多个数据集偏差大），且 ATE 随时间曲线贴合 Centralized Oracle。
    - 通信实验：标准 C-PGO 在高信噪比下对通信质量不敏感；Range-Aided 与 Range-Only 在低信噪比下随通信质量提升显著改善，支持「退化源于通信而非外点」的假设。
    - 消融：分别去掉 RWBP（−R）、对偶衰减（−D）及两者（−B），在 50 个平面 3D C-PGO 上均显著变差，二者共同构成性能来源；kiMESA 用 iSAM2+Geman-McClure 替代 riSAM，差距说明局部鲁棒增量求解器不可省。
    - 实时与带宽：i9-13900K / 128 GB 上除 DDF-SAM2 外分布式方法均满足实时更新与累计时间约束，集中式鲁棒方法（GNC/PCM）超实时；Wi-Fi 下峰值 625.3 KB/s、均值 54.9 KB/s，Pro-Radio 峰值 825.3 KB/s、均值 57.6 KB/s，均低于模型上限（2000/1000 KB/s），ntu_r3_02_wifi 峰值仅 3.8 KB/s。
- **创新点与贡献**：
    - 把 C-ADMM 作为 C-SLAM 后端的统一理论基座，给出「可分 + 流形 + edge-based 异步」的完整推导（MESA+），并用四种约束函数的闭式解比较确定 geodesic + SPLIT。
    - 提出增量摊销：把 ADMM 的约束收紧摊到稀疏通信机会上，使中间解仍可用，从而把批式 C-ADMM 变成随时可中断、可恢复的在线算法。
    - RWBP 把 biased prior 也包上鲁棒核，使机器人可把过时约束视为外点拒绝，配合对偶衰减（𝔡=0.9）解决「约束被拒后对偶残留」问题。
    - 给出未初始化 RWBP 的小惩罚（β_uninit=1e-4）+ 初始化后固定 β（β_init=1.0）的工程方案，避免新回环被大惩罚锁死，并用鲁棒共享变量初始化保留双方信息。
    - 在 2430 合成 + 28 真实数据集上同时验证精度、实时性、带宽与跨场景泛化，是同类工作中规模最大的一次系统评测。
- **局限与风险**：
    - （作者承认）riMESA 没有形式化收敛保证：增量摊销、RWBP、对偶衰减都偏离标准 C-ADMM 的固定问题假设，取极限（通信→∞、RWBP→加权 biased prior、𝔡→1）才回到鲁棒 MESA+。
    - （作者承认）真实数据集的参考解并非真值，且真实噪声下 C-SLAM 的全局最优未必对应参考解，因此连 Centralized Oracle 也可能出现指标劣于其他方法的情况。
    - （我在正文发现）真实实验的带宽上限未被真正约束（「we did not limit communications based on bandwidth」），带宽结论是事后统计而非硬约束下的结果。
    - （我在正文发现）平均最优性差距仍有 45.09%，相对集中式 GNC 差距不小；作者归因于通信受限，但未给出「通信量→差距」的定量曲线。
    - （我在正文发现）共享环境变量（landmark）的关联依赖描述子相似度假设，正文承认实现上「likely need to compare some form of descriptor」，跨机器人数据关联误差未单独评估。
    - （我在正文发现）评测以 ATE 与 F1 为主，未报告姿态/重力对齐误差、Map 一致性或长期漂移的专项指标。
- **与文献库的关系**：本文是作者线 iMESA（McGann & Kaess, RSS 2024）与 MESA 的直接延续：iMESA 已给出 C-ADMM 用于 C-SLAM 的批式版本，riMESA 补上外点处理、非阻塞通信、环境变量与共享变量初始化四项。理论侧承接 C-ADMM、edge-based 异步收敛与 Choudhary 等的 biased prior 技巧；鲁棒侧承接 GNC 与 riSAM 的增量 continuation 思路，并与 PCM/GkCM/iRRR 的松弛一致性对照。系统侧与 DDF-SAM2、DLGBP 正面对比；应用侧对照 Kimera-Multi、DOOR-SLAM、COVINS、LAMP 2.0、Swarm-SLAM。评测直接用配套 COSMO-Bench 与 Nebula。本篇为旧稿 v2 再公告（v1 未入馆），按首次入馆处理。
- **可复现性**：代码开源：https://github.com/rpl-cmu/rimesa （正文脚注 2）。真实数据用 COSMO-Bench（DOI 10.1184/R1/29652158）与 Nebula；合成数据生成器、噪声模型与通信模型参数在 §VII-A 给出（r_c=1 Hz 或 5 Hz、d_c=30 m、p_c=0.9、b_c<1 s 或 ≤200 ms、5% Two-Generals 故障注入）。基线实现：DLGBP 由原作者提供（窗口 w=30），DDF-SAM2 由本文作者实现（Geman-McClure c=3），kiMESA 用 iSAM2 + Geman-McClure c=6，集中式 GNC 用 GTSAM 默认参数、PCM 用 Kimera-RPGO（χ²(0.95)）。硬件 i9-13900K / 128 GB。
- **行动建议**：先读 §IV-B5 的 biased prior 加权与 §V-A/V-B 的摊销 + RWBP，这两处决定能否在线；再看 §VII-F 的真实精度与 Fig. 10 的运行时。核四个数字：45.09% 与 352.81%/787.30% 的比值（7.8×/17.5×）、28 个真实集是否为 24 个 COSMO-Bench + 4 个 Nebula、2430 个合成集的场景构成、54.9 KB/s 均值是否在未限带宽下测得。风险点：无收敛保证、参考解不完美、landmark 关联依赖描述子。

### 第 2 章 · Instant NuRec：面向驾驶场景仿真的前馈三维高斯重建（2607.14203，4.28 A，FULL）

- **赛道 / 场合**：世界模型与仿真 / arXiv preprint（cs.GR，cross-list cs.CV 与 cs.AI）；NVIDIA，v2 再公告
- **公告类型**：replace（公告日 2026-11-13，拉取日 2026-11-14）
- **等级说明**：backfill 不参与重磅日判定，≥4.2 按口径记 A
- **一句话结论**：Instant NuRec 单次前向把 10–20 s 多相机驾驶日志重建为分层 3DGS 世界，约 1.5 s 完成，而逐场景优化的 NuRec 约需 75 min（超过 3 个数量级加速）；Waymo 验证集全图 PSNR 28.26、SSIM 0.859，比最强基线 DGGT 的 26.25 高 2.01 dB，动态区 24.93 对 21.76；140 个场景闭环 rollout 中五种策略排序与 NuRec 完全一致。
- **要解决的问题**：闭环仿真是自动驾驶开发与验证的核心工具，要求同时成立三件事：照片级渲染、场景显式分解为静态背景与动态体、能自由重摆自车位姿并重定时序以评估反事实。3DGS 让渲染变便宜，OmniRe 一类逐场景优化已能忠实复现真实日志，但每段 clip 要数十分钟到数小时优化、需精调超参，还依赖 LiDAR、语义掩码、cuboid 轨迹等辅助输入，无法承载车队每天百万级 clip。驾驶世界模型（latent diffusion、video-GPT）能生成逼真视频，但只输出 2D 像素，planner 不能重摆位，也不给出可仿真状态。前馈重建（STORM、DrivingForward、DepthSplat、DGGT）解决速度，但输出是裸 RGB 高斯，不含静态/动态分层、语义与 ISP 校正，不能直接喂给仿真器。缺口即：能否一次前向产出与逐场景优化同格式、可被 NuRec/AlpaSim 消费的分层世界。
- **方法详解**：输入 V×T 张 RGB（2–4 Hz）加每张 6-DoF 位姿 T_{v,t}∈SE(3)、内参 κ_{v,t}。输出四件：静态层 G^s（高斯属性加世界法向 n 与 road/non-road 语义）；动态层 G^d（位置改为 3 节点分段线性轨迹，不透明度按 exp(−x^10) 淡入淡出）；天空 cubemap I^sky；每相机 ISP 仿射 {A_v}。编码器用 Depth-Anything-3 的交替注意力 ViT，输出 latent F。解码挂轻量头：DPT 头出深度、法向、语义；3DGS 头从深度抬升 query 点 Q，与 F 交叉注意力后回归高斯参数；运动头复用 Q，以 AdaLN 按 t_tgt 条件化回归两个 3D 位移。query 分 Dense 与 Selective（步长 s、p×p 聚 token）：s=2、p=8 时单视图约 88 K 高斯，比 Dense 的 351 K 少 4×。长 clip 用重叠 chunk：按 α<1e−2 剪枝并转世界系后做视锥归属剪枝——高斯 g 在 chunk i 到最近光心距离 D_gi，仅当 D_gi ≤ min_j D_gj + δ（式1）保留。损失 L=L_context+L_motion+L_render（式2）：context 监督深度、法向、语义；motion 为前后向 3D flow；render 在留出视角算 L1+LPIPS。三阶段课程：Stage 1 复现 DA3 预训练；Stage 2 开天空、深度、运动头微调编码器；Stage 3 冻结编码器只训 ISP 与 GS 头。
- **实验与结果**：
    - Waymo Open Dataset 验证集，沿用 STORM 协议：每样本 2 s 窗口、20 帧 @10 Hz，输入 4 帧 context（间隔 0.5 s），指标在 240×160 上计算；基线 DepthSplat、STORM、Depth-Anything-3、DGGT 均用发布 checkpoint 不再微调（DGGT 不取位姿，先做轨迹对齐）。
    - 表 1 全图：Ours 28.26/0.859，DGGT 26.25/0.805，DepthSplat 22.48/0.645，STORM 21.88/0.752，DA3 20.30/0.557；深度 AbsRel 0.076、δ₁ 0.937（STORM 0.123/0.870，DGGT 0.135/0.841）。
    - 表 1 动态区：Ours 24.93/0.793，DGGT 21.76/0.652，STORM 19.89/0.556，DepthSplat 18.59/0.391；动态区 AbsRel 0.085、δ₁ 0.922。
    - 内部数据（约 40K clips，最多 5 相机、300–600 帧 @30 Hz）：Selective 把高斯预算从约 351 K/视图降到约 120 K（18 帧场景 6.3 M 降到 2.2 M，约 3×），图像与深度仅轻微下降；Dense 与 Selective 均约 1.5 s 重建，对比 NuRec 约 75 min。
    - 闭环仿真：140 个场景、每场景 20 s、每 500 ms 重规划、6 次独立试验，5 种策略（VaVAM、Alpamayo R1、Alpamayo 1.5 的 1/2/4 相机版），指标取 Collision（前、侧、后）与 Offroad 的平均；Instant NuRec 下的策略排序与 NuRec 完全一致。
    - 消融（表 2，内部验证集）：完整模型 29.93/0.793/0.069/0.950；单阶段训练 27.65/0.751/0.077/0.955；天空改用 MLP 26.73/0.692；去 LPIPS 26.81/0.705；去深度损失 28.92/0.782 但 AbsRel 0.103、δ₁ 0.862；去视锥归属合并 26.10/0.648/0.098/0.891。
    - 训练：PyTorch 加 3DGUT 可微渲染，DDP 跨节点、每卡有效 batch 1–2 clip，V∈{1,3,5}、T∈{8,12,18}，余弦退火加线性 warmup 至 1e−4，三阶段共约 6 天、8 节点。
- **创新点与贡献**：
    - 单次前向直接产出仿真可用的分层世界（静态、动态、天空、ISP），而不只是裸 RGB 高斯，格式与 NuRec、AlpaSim 对齐。
    - 把高斯与像素解耦，用深度抬升的 query 点加 Selective 聚类把高斯预算降约 4×，质量基本保持。
    - 运动头直接回归分段线性轨迹，重建时无需逐 actor 的 cuboid 轨迹输入。
    - 视锥归属的 chunk 合并策略按「谁看得最近」决定高斯归属，显著抑制长序列的 floater。
    - 几何监督与渲染监督解耦的三阶段课程，使 40K clip 规模训练稳定可行，并用闭环策略排序验证仿真可用性。
- **局限与风险**：
    - （作者承认）高斯数量与质量存在固有张力：追平逐场景优化需要很多基元，预算小则细结构欠采样；测试时训练微调是可能的补法。
    - （作者承认）泛化受训练语料限制，低安装位或纯鱼眼等与训练差异大的 rig 需微调。
    - （作者承认）三段关键帧的分段线性轨迹无法表达亚秒级非刚性运动（如行人关节运动），需更密关键帧。
    - （我在正文发现）训练依赖 NVIDIA 内部约 40K clips 与内部 cuboid 自动标注器，外部无法复现训练；Waymo 评测仅 240×160、4 帧 context，分辨率与视角数偏低。
    - （我在正文发现）「策略排序完全一致」只说明相对排序，正文未给碰撞率与越界率的绝对数值及置信区间，无法判断差距是否在噪声内。
    - （我在正文发现）1.5 s 重建的硬件型号与批设置未在实验节标明（只说训练用 8 节点），跨平台速度不可直接比较。
- **与文献库的关系**：论文站在三条线交汇处。逐场景神经重建：NeRF 与 3DGS 的城市级扩展、Neural Scene Graphs 的「静态背景加刚性前景」分解、显式高斯化的 Street Gaussians 系列，以及 OmniRe（分解扩展到非刚性行人与骑行者）；渲染器侧是 3DGRT 与 3DGUT（原生支持畸变相机与 secondary rays），本文用 3DGUT。前馈重建：单物体 LRM 系列到场景级可泛化高斯，以及面向动态驾驶的 STORM 与 DrivingForward；还有把高斯与像素解耦的 TokenGS。生成式世界模型：latent diffusion 街景生成、长时程自回归与 video-GPT、跨具身世界基础模型，以及「重建器加生成器」联合方案。本文定位在重建侧，作为生成式修复与联合模型的快速 3D 主干；工业侧继承 NuRec 与 AlpaSim 的输出格式与仿真栈。
- **可复现性**：代码公开：https://github.com/nvidia/instant-nurec，文档 https://docs.nvidia.com/nurec/index.html；输出可导出 USDZ 并被 NuRec 与 AlpaSim 消费。训练语料为 NVIDIA 内部约 40K clips，不公开；依赖内部 cuboid 自动标注器与语义分割模型。Waymo Open Dataset 公开，可用其验证集复现表 1；3DGUT 渲染器公开。
- **行动建议**：先读 §5.1 表 1 与 §5.2 的闭环实验，这两块决定方法能否接进你的仿真链；再读 §3.4 的式(1) 视锥归属剪枝，它是长序列质量的关键。核对：2.01 dB 的对比口径（240×160、4 帧 context、DGGT 做了轨迹对齐）、表 2 消融的 29.93 出自内部数据不可与 Waymo 的 28.26 直接比、1.5 s 的硬件未标明。风险：训练数据不可得、依赖 NVIDIA NuRec 与 AlpaSim 生态、动态轨迹只有 3 个关键帧。

### 第 3 章 · OMG4：面向高效动态场景表示的优化最小 4D Gaussian Splatting（2510.03857，3.80 A，FULL）

- **赛道 / 场合**：神经渲染 / arXiv preprint（cs.CV）
- **公告类型**：replace（公告日 2026-11-13，拉取日 2026-11-14）
- **一句话结论**：OMG4 用 SD-Score 采样、双阈值剪枝与可学习权重合并三级缩减高斯，再叠加时间条件隐式外观与分阶段 3D→4D SVQ，在 N3DV 上把 Real-Time4DGS 从 2087 MB 压到 3.59 MB（约 99%），PSNR 31.85 对 31.96、FPS 由 57 升到 129（2.26×）；同等质量下比 GIFStream 的 10.0 MB 少 65%，并可迁移到 FreeTimeGS（61.04→3.07 MB）与 STG（172→11.17 MB）。
- **要解决的问题**：4D Gaussian Splatting 以百万级带时间属性的显式高斯基元换取高保真动态重建，Real-Time4DGS 在 N3DV 单场景即占 2 GB 级存储，直接阻碍移动端、流式与 VR/AR 部署。已有压缩工作各有缺口：4DGS-1K 用 lifespan 重要性剪枝后仍在 50 MB 量级；GIFStream 以特征流做运动感知剪枝，但只在自身表示上验证；Light4GS、ADC-GS 面向形变式动态高斯（context/anchor），4DGS-CC 是面向 4DGS 的熵编码框架，而 OMG 的 SVQ 只针对静态 3DGS。更关键的是，4D 高斯的冗余在静态区与动态区异质，时间属性又与空间几何、外观强耦合，一次性量化全部属性会破坏优化稳定性——正文指出的「先缩减、后量化」顺序问题此前未被系统处理，也缺少跨 RT-4DGS/STG/FreeTimeGS 的通用性验证。
- **方法详解**：输入为预训练 4D 高斯集合 P={(x_i,f_i,a_i)}，x 为参考位置、f 为外观、a 含不透明度/尺度/旋转/时间参数，方法对三种时间参数化通用。①Sampling：SD^(i)=N_minmax(S_grad)·N_rank(T_grad)，S_grad=Σ_j||∇_{u_ij}L_j||_2 为全部图像上对投影坐标的梯度累积（静态区稀疏持久，微小扰动即影响多帧损失），T_grad=Σ_j∇_{μ_ti}L_j 为带符号时间梯度累积，符号频繁翻转者在归一化前相互抵消，充当一致性滤波；按 τ_GS 采样后优化 1000 次。②Pruning：P_GP={G_i | N(S)≥τ_S ∨ N(T)≥τ_T}，阈值取 p 分位数（中等模型 0.8），只剔双低象限。③Merging：4D 时空体划网格，仅同 cell 内聚类，S(G_i,G_j)=-(||x_i-x_j||²+λ||f_i-f_j||²)，按 τ_sim 成簇并去重为极大簇；代理 x̄_q=Σw_i^x x_i、f̄_q=Σw_i^f f_i，其余属性取自位置权重最大者（尺度/旋转/时间非线性，平均不稳定），重复 M 次并放大网格。属性压缩沿用 OMG 的 MLP 并对不透明度与颜色加时间条件；SVQ 保留 4D 均值全精度、只量化其余属性，先 3D 后 4D 分阶段（4000 步训 MLP、9000 步开 3D、10000 步开 4D，共 11000 步），末端 Huffman+LZMA。
- **实验与结果**：
    - 数据集与硬件：N3DV（1352×1014）、SelfCap（6 场景、每段 60 帧，遵循 FreeTimeGS 协议）、ENeRF-Outdoor（1200 帧长序列），另有 N3DV 1024×768 补充设置；RTX 4090，11000 次迭代 45.17 min（Table 14）。
    - N3DV 主结果（Table 1）：Ours–M 为 PSNR 31.85 / SSIM 0.941 / LPIPS 0.060 / FPS 129 / 170,044 高斯 / 3.59 MB；基线 Real-Time4DGS 为 31.96 / 0.946 / 0.051 / 57 / 3,397,510 / 2087 MB。
    - 对比 GIFStream-L：存储 10.0 MB→3.59 MB（-65%）、PSNR 31.75→31.85；低码率档 Ours–T 31.54 dB / 2.18 MB 优于 4DGS-CC(4DGS)-S 的 30.97 dB / 2.30 MB；BD-rate 相对 GIFStream −71.65%、相对 4DGS-CC(Saro-GS) −83.79%。
    - 跨表示：FreeTimeGS 61.04 MB→3.07 MB（Ours–M，PSNR 32.80→32.62）；SelfCap 122 MB→4.06 MB（Ours–T，PSNR 26.74 对 GIFStream-S 25.56 / 5.52 MB）；STG 172 MB→11.17 MB，比 CSTG 少 27% 内存。
    - ENeRF-Outdoor：RT-4DGS 8,059 MB / 24.40 dB → Ours(RT4DGS) 11 MB / 24.30 dB；FTGS 488 MB / 25.04 dB → Ours(FTGS) 53.44 MB / 24.70 dB，且可单次跑完 1200 帧（GIFStream 需 20 个分块模型、共 17 h）。
    - 消融：未缩减直接做属性压缩即 OOM；同时 3D/4D 量化 31.54 dB vs 分阶段 31.85 dB（+0.31）；采样与剪枝合并为一步掉 0.15 dB；动态分数改绝对梯度 31.65 dB（-0.20）；改用光流 27.19 dB（-4.56）；合并时额外学习协方差/时间权重分别降到 31.72 / 31.75 dB。
- **创新点与贡献**：
    - 把 4DGS 压缩拆成「静态–动态显著性采样 → 双阈值剪枝 → 局部时空合并」的可微三级缩减，并以消融证明阶段不可合并（合并后 -0.15 dB）。
    - 提出 SD-Score：屏幕空间梯度（静态）与带符号时间梯度（动态）经极值/秩归一化后相乘，带符号累积同时充当时间一致性滤波（优于绝对梯度 0.20 dB、优于光流 4.56 dB）。
    - 把 SVQ 扩展到 4D 属性并提出 3D→4D 分阶段量化，论证量化可行性依赖前级高斯缩减（全量直接压缩 OOM），分阶段比同时量化高 0.31 dB。
    - 同一流程可插到 Real-Time4DGS、STG、FreeTimeGS 三种时间参数化，均取得 27%–99% 存储下降。
- **局限与风险**：
    - （我在正文发现）方法为 post-hoc 压缩，必须先有百万级高斯的预训练 4DGS 模型，正文未报告与压缩联合训练或从零优化的结果。
    - （我在正文发现）ENeRF-Outdoor 上即便 Ours(FTGS) 仍有 1,999,800 高斯 / 53.44 MB（N=1,F=1200），压缩率远低于 N3DV 的 99%，长序列场景收益有限。
    - （我在正文发现）SelfCap 上 PSNR 26.74 略低于 FTGS 的 26.96，LPIPS 0.254 明显差于 0.194（Ours–T），强非刚性运动下以保真度换存储。
    - （我在正文发现）τ_GS、分位数 p、合并轮数 M、网格缩放均按数据集与模型档位分别设定，正文未给出跨数据集统一配置的敏感性分析。
    - （我在正文发现）无主观/感知评测，也没有真实流式传输或端侧解码实验，「可实用」主要由存储与 FPS 推断。
    - （我在正文发现）多数基线数字引自原论文（∗ 为复现），仅部分方法复现，跨论文比较口径不完全一致。
- **与文献库的关系**：静态侧继承 OMG（Lee et al., 2025）的 SVQ 与隐式属性 MLP，并与 LightGaussian、LP-3DGS、HAC、Scaffold-GS 等剪枝/锚点/上下文方法对照；动态侧以 Real-Time4DGS（Yang et al., 2024）为主干，与 STG（Li et al., 2024）、FreeTimeGS（Wang et al., 2025）共享显式高斯基元抽象，故可跨表示复用。相对 4DGS-1K 的 lifespan 剪枝、GIFStream 的特征流剪枝、MEGA 的内存高效表示、Light4GS/ADC-GS 的 context-anchor、4DGS-CC 的熵编码，本文差异是把基元级缩减与属性级量化串成一条流水线，并强调缩减是量化前提。本篇为旧稿 v2 再公告（v1 未入馆），按首次入馆处理。
- **可复现性**：代码与项目页公开：https://minshirley.github.io/OMG4/（摘要给出）。N3DV、SelfCap、ENeRF-Outdoor 均为公开基准；超参见 §5.1 与附录 C（τ_GS、分位数 p、M、码本 2^9/2^13/2^10 等）。FreeTimeGS 官方代码与权重未公开，作者自述使用自行复现的 FTGS 模型（脚注 1），该部分不能与官方模型直接对比。硬件 RTX 4090，解码约 8 s。
- **行动建议**：先读 §4.1 的 SD-Score 与 §4.4 的分阶段 SVQ 调度，再看 Table 5 确认三级缩减各自增益。核三个数字：2087 MB→3.59 MB 是否包含 MLP 权重/码本/熵编码元数据（§5.1 声称包含）、GIFStream 的 10.0 MB 是否同分辨率同场景、ENeRF-Outdoor 的 11 MB 是否只统计 RT-4DGS 分支。风险点：post-hoc 依赖预训练模型、超参按数据集分别调、SelfCap 上 LPIPS 反而劣于 FTGS。

### 第 4 章 · AVI-HT：面向手套式 3D 手部追踪的自适应视觉–IMU 融合（2605.21714，3.73 A，FULL）

- **赛道 / 场合**：交互与输入 / arXiv preprint（cs.CV；交叉 cs.RO）
- **公告类型**：replace（公告日 2026-11-13，拉取日 2026-11-14）
- **一句话结论**：AVI-HT 把 12 个手套 6-DoF IMU（200 Hz，14 帧窗口 14×23×3）与头显单目图像（60 Hz，512×640）经带运动学先验掩码的层级跨传感器注意力融合，在自建 DexGloveHOI（100K+ 帧、2.4M IMU 样本、4 名被试、17 类任务、3.5 h）上把 UMETrack 的 MKPE 从 12.342 mm 降到 10.359 mm（−16.1%）、指尖 F.MKPE 从 17.478 降到 13.253 mm（−24.2%），MANO 下 PA-MPJPE 13.754→10.519 mm（−23.5%），接触丢失率降 8.5%。
- **要解决的问题**：第一人称手部追踪的核心矛盾是：抓握越紧，手越被物体遮住，而 AR/VR 与遥操作恰恰发生在接触最密集的时刻。纯视觉方法（HaMeR、METRO、MeshGraphormer）泛化好，但遮挡下可解释的 kinematic 构型集合过大，误差骤增；纯 IMU 方案多用密集 9-DoF 阵列，磁力计受室内电磁干扰，6-DoF 虽避开磁干扰却缺绝对朝向并累积陀螺漂移，无法给出全局腕部位姿。视觉–IMU 融合在全身动捕（DIP-IMU、TransPose）已证明有效，但细粒度手部几乎空白，原因被作者归为两点：缺少适合自然操作的无创 IMU 手套硬件，以及缺少同步 ego 视频 + 密集 IMU + 3D 真值的数据集。已有手部数据集（HOI4D、HOT3D）或为纯视觉、或受控棚拍，均不含惯性信号，因此无法判断融合带来真实增益还是仅增加复杂度。
- **方法详解**：硬件与信号：Meta Quest 单目灰度相机 60 Hz、512×640；全手覆盖手套 12 个 6-DoF IMU，四指近/远节各一、拇指与手背各一，200 Hz。每个视频帧对齐最近 IMU 时间戳，取此前 14 个样本，每样本由 6-DoF 算重力向量并与 3 轴陀螺拼接，得 14×23×3 窗口。真值由光学标记动捕给出，先解为 UMETrack 位姿，再用 Levenberg–Marquardt 转 MANO。模型：IMU 编码器把 3 维线性映射到 69 维、加 14 步正弦位置编码、2 层 transformer，取末步经两层 MLP 得 F_imu∈R^{23×d}；视觉编码器分两版——UME 用 ResNet + FTL（把 2D 特征经 SE(3) 提升为相机解耦 3D 表示）+ 卷积 RNN，MANO 用 ViT-Huge 编码 256×192 crop 得 N×1280 patch token。融合：Z=[F_vis*,s_1,…,s_12]∈R^{13×d}，运动学先验掩码 M_ij=−α·d_geo(i,j)，一级注意力 softmax(QK^T/√d_k+M)V；因单视觉 token 面对 12 个 IMU token 易被淹没，二级把 12 个传感器 token 池化为 s̄，与视觉 token 组成 2×d 序列做自注意力再校准。输出：UME 头解码 22 维关节角、腕部 (R,t)∈SE(3) ，用 landmark NLL + 关节角损失经可微前向运动学得 3D 点；MANO 头解码 θ、β、相机 π，用 3D/2D + 对抗损失。
- **实验与结果**：
    - DexGloveHOI：4 名被试、每 session 17 类精细操作任务、45–55 min 可用采集、共 3.5 h，产出 100K+ ego 帧、2.4M IMU 样本、720 GB 同步记录；训练用另一份约 8M 图像的私有手套数据，被试/场次/任务与评测完全不相交。
    - UMETrack 表示（Table 4）：UMETrack 12.342 / 17.478 / 9.359 / 17.798 / 76.059 / 81.433；UMETrack+EKF 15.406 / 18.658 / 7.891 / 14.232 / 70.903 / 84.210；IMU-Tracker 仅 7.151 / 12.923 / – / 85.769；AVI-HT 10.359 / 13.253 / 7.021 / 12.785 / 79.315 / 85.859（MKPE/F.MKPE/MKPE.T/F.MKPE.T/P.A/P.A.T）。
    - MANO 表示（Table 5/6）：HaMeR 13.754 / 12.736 / 0.516 / 0.882 → AVI-HT 10.519 / 9.265 / 0.628 / 0.936（PA-MPJPE / PA-MPVPE / F@5 / F@15），降幅 23.5% 与 27.3%。
    - 融合消融（Table 1）：early concat 11.928、late fusion 12.139、pooled IMU token 11.956、fusion-1 only 11.113、w/o k-prior 10.901、full 10.359（MKPE）；去运动学先验 +0.54 mm、去二级注意力 +0.75 mm。
    - 遮挡分层（Table 3）：按每帧被遮挡关键点数分箱，UMETrack 的 F.MKPE 从 16.525 涨到 21.741（+5.2 mm），AVI-HT 从 13.034 到 15.539（+2.5 mm）；优势由 3.5–3.9 mm 扩大到 6.2–7.5 mm。
    - 跨被试（Table 2）：四名留出被试 MKPE 8.852–11.266 mm、P.A 77.486–82.333，每人六项指标均优于聚合的 UMETrack。
    - 接触保持（Table 7，15 个木块 session）：Disp. 9.91→8.96 mm、Ret@5 56.60→59.41、Ret@10 84.12→86.73、Capt. 58.09→61.20、Longest 50.13→53.84、Loss/s 0.911→0.834。
- **创新点与贡献**：
    - 用「逐指 IMU 手套 + 头显单目」这一互补组合解决抓握遮挡，并给出同步采集 + 动捕真值的完整数据链路，填补手部视觉–惯性融合的数据空白。
    - 提出带运动学先验掩码的层级跨传感器注意力：M_ij 用骨架跳数编码物理邻近性，使遮挡时注意力自动转向对应 IMU；二级 2-token 自注意力纠正 1 视 vs 12 IMU 的 softmax 失衡。
    - 把注意力首行 a_vis 直接解释为「每个 IMU 的信任度」，并用逐指/逐活动热图验证对角线效应，给出可解释的融合证据。
    - 同时覆盖实时 AR/VR（UMETrack，22 关节角 + SE(3) 腕）与离线重建（MANO，θ/β/π）两种表示，证明融合设计与骨干无关。
- **局限与风险**：
    - （作者承认）数据手套改变手部外观，对期望裸手图像的下游管线存在 domain gap，需手部 avatar 渲染弥补。
    - （作者承认）只验证了一种手套，对其他传感器布局、形态与 IMU 规格的泛化未知。
    - （我在正文发现）摘要把 24.2% 归为「wrist-aligned 变体」，但 Table 4 中 24.2% 对应的是指尖 F.MKPE（17.478→13.253），腕对齐 MKPE.T 实为 9.359→7.021（−25.0%），指标口径表述不一致。
    - （我在正文发现）未声明 DexGloveHOI 与代码是否公开，训练还依赖约 8M 图像的私有手套数据，外部无法复现。
    - （我在正文发现）仅 4 名被试、单一 Quest 头显与单一手套硬件，缺少跨设备/跨光照/跨手型实验。
    - （我在正文发现）未报告推理延迟、功耗或端侧算力占用，而「实时 AR/VR」是其核心卖点之一。
- **与文献库的关系**：视觉侧以 UMETrack（Han et al., 2022）与 HaMeR（Pavlakos et al., 2024）为骨干基线，分别代表 AR/VR 实时关节角回归与 Transformer 大规模手网格回归；上游可追到 METRO、MeshGraphormer 的自注意力网格建模。惯性侧与 IMU-Tracker（Sarker et al., 2026）的 6-DoF 纯惯性方案对照。融合承接全身动捕的 DIP-IMU（Huang et al., 2018）与 TransPose（Yi et al., 2021），手部与 UMETrack+EKF（Lei et al., 2023）这类后验滤波直接比较。数据侧对标 HOI4D、HOT3D 等纯视觉手–物数据集，差异是加入 12 路同步 IMU 与动捕真值。本篇为旧稿 v2 再公告（v1 未入馆），按首次入馆处理。
- **可复现性**：代码与 DexGloveHOI 数据集均未见公开声明，正文只描述采集协议与附录 A/B 的实现细节（含动捕布置）；训练使用约 8M 图像的内部手套数据集，评测集与训练集在 subject/session/task 上不相交但不可获取。硬件为 Meta Quest 单目灰度相机 + 自研 12 路 6-DoF 手套 + 光学标记动捕，复现门槛高。基线（UMETrack、HaMeR、IMU-Tracker、UMETrack+EKF）均在同一训练集上微调。
- **行动建议**：先读 §3.3 的 token 构造与式 (1) 的 M_ij 定义，再看 §5.1 的融合消融与 Table 3 的遮挡分层，这两处是论文的核心证据。核三个数字：−16.1% 对应 MKPE、−24.2% 对应 F.MKPE（勿按摘要理解为 wrist-aligned）、接触丢失 8.5% 是否等价于 Loss/s 0.911→0.834。风险点：数据与代码不公开、单一手套硬件、无延迟/功耗数据、指标口径在摘要与表格间不一致。

### 第 5 章 · ENIGMA-360：面向工业场景人类行为理解的自我–外部视角数据集（2603.09741，3.49 B，FULL）

- **赛道 / 场合**：评估与数据集 / arXiv preprint（cs.CV）
- **公告类型**：replace（公告日 2026-11-13，拉取日 2026-11-14）
- **一句话结论**：ENIGMA-360 在真实工业实验室采集 180 段自我中心与 180 段外部视角同步视频（34 名被试、平均 18.59 min、合计 111.54 h、68 类 keystep、14,556 段时序标注、12,597 帧 HOI 标注、25 类物体），给出 TAS/Keystep/HOI 三套基线：同视角最优 FACT 在 EGO→EGO 上 F1@10 78.7、Acc 70.8；跨视角最好仅 C2F-TCN 的 EGO→EXO F1@10 7.2，ASFormer 的 EXO→EGO F1@10 20.9，量化出现有模型的 ego-exo 崩塌。
- **要解决的问题**：工业行为理解既需自我中心视角的手–物细节，又需外部视角的环境与流程上下文，但公开数据长期缺这一组合。现有工业类数据集多用替代场景：MECCANO 是 20 段带 gaze/深度的第一人称视频、IndustReal 用玩具车装配、Assembly101 是无线索纹理玩具车的拆装，均缺真实工具与流程；Ego-Exo4D、H2O、LEMMA、IKEA ASM 虽多视角，却不针对工业维修。缺口有三：①没有在真实工业实验室同步采集 ego+exo 的数据；②缺同时具备 keystep 级时序与手–物空间标注（框、手侧、接触态、关联）的体系；③没有跨视角评测协议，无法判断模型学到行为还是过拟合某一视角的外观。
- **方法详解**：在自建 ENIGMA 实验室（25 类固定/可移动工业对象）设计高/低压两块板的两套维修流程，每套 4 个版本，共 68 个 keystep。用 Unity 开发的 HoloLens 2 应用以 gTTS 音频 + 混合现实图片逐步下指令，替代纸质手册。ego 流为 HoloLens 2 RGB 2272×1278@30 fps，exo 流为 ZED 672×376@15 fps，用工作台灯泡亮起做时间对齐；34 名被试，平均 18.59 min，共 111.54 h，划分 103/29/48。标注：以应用日志时间戳为初值，用定制 VIA Subtitle Annotator 修正起止，得 14,556 个 keystep；14,036 个交互关键帧，物体为 (class,x,y,w,h,state) 五元组共 275,135 个，手框用 100DOH 类模型出伪标签再人工修正手侧与关联共 56,473 个；HOI 子集 12,597 帧、17,363 只手（10,043 接触）、9,342 个 active object。附加 SAM-HQ 的 197,814 手掩码与 1,435,006 物体掩码、DINOv2-large 1024 维特征、Matterport + ARTEC EVA 的 3D 模型。基线：TAS 用 C2F-TCN、MSTCN++、LTContext、ASFormer、DiffAct、FACT ；Keystep 用 TimeSformer 8 帧窗口；HOI 用 VISOR HOS 与 Leonardi 2025/2024，报 COCO Mask AP。
- **实验与结果**：
    - 规模：180 ego + 180 exo 同步视频、34 名被试、平均 18.59 min、合计 111.54 h；ego 2272×1278@30 fps（HoloLens 2），exo 672×376@15 fps（ZED），划分 103/29/48。
    - 标注量：68 类 keystep、14,556 段时序标注（均长 7.92 s）、14,036 个交互关键帧、275,135 个物体框、56,473 个手框、12,597 个 HOI 帧（17,363 只手，10,043 接触，9,342 active object）、197,814 手掩码 / 1,435,006 物体掩码。
    - TAS 同视角（Table 3a）：EGO→EGO 最优 FACT 为 F1@10/25/50 = 78.7/73.2/59.5、Edit 84.6、Acc 70.8、AccB 72.7；EXO→EXO 最优 FACT 72.8/66.5/50.4、Edit 76.6、Acc 63.3、AccB 68.2。
    - TAS 跨视角（Table 3b）：EGO→EXO 最优 C2F-TCN 仅 7.2/5.5/3.5、Edit 13.1、Acc 5.6、AccB 29.7；EXO→EGO 最优 ASFormer 20.9/19.0/13.6、Edit 22.8、Acc 22.7、AccB 49.0。
    - Keystep（Table 4）：TimeSformer-EGO 为 P 0.75 / R 0.74 / F1 0.74 / Acc 0.83 / IoU 0.62；TimeSformer-EXO 为 0.50 / 0.47 / 0.46 / 0.47 / 0.32。
    - HOI（Table 5）：VISOR HOS 掩码 Overall 63.84（Hand 85.01、H+S 81.05、H+C 52.32、Object 51.35）；加标签传播后 64.55（85.75 / 82.51 / 52.59 / 53.24）；框基线 Overall 仅 46.24（Hand 90.81、H+S 90.35）。
    - 跨视角协议：每个基线分别在 ego 与 exo 训练子集训练后，在两种测试集上各评一次，用于量化视角域 gap，而非只报单视角成绩。
- **创新点与贡献**：
    - 首个在真实工业实验室采集的同步 ego-exo 数据集（180+180），用真实示波器、焊台、电路板替代玩具/无线索纹理替代场景。
    - 建立 keystep 级时序 + 手–物级空间的联合标注体系（68 类、14,556 段、12,597 HOI 帧、手侧/接触/关联五元组），并附 SAM-HQ 掩码、DINOv2 特征与全场景 3D 模型。
    - 首次系统给出跨视角（EGO↔EXO）的 TAS/Keystep/HOI 基线，用同一协议量化「同视角 78.7 → 跨视角 7.2」的域 gap。
    - 用 HoloLens 2 混合现实应用替代纸质手册下发步骤指令，并借应用日志半自动生成时序标注初值，降低长流程采集与标注成本。
- **局限与风险**：
    - （作者承认）数据来自单一实验室，布局固定、光照受控、工具与流程仅两套，被试数量有限，向其他工厂/流程/工种的泛化受限。
    - （我在正文发现）跨视角 TAS 近乎失效（F1@10 最低 0.3、Acc 0.9），但正文未分析失败机理，也未给出任何跨视角对齐/域适应基线。
    - （我在正文发现）划分按视频（103/29/48）而非按被试，正文未说明是否 subject-disjoint，存在同一被试跨集导致高估的风险。
    - （我在正文发现）空间标注只在 ego 子集做（「we identified the interaction key frames within the egocentric subset」），exo 侧没有对应手–物框，限制真正的双视角 HOI 监督。
    - （我在正文发现）全部为单次运行结果，无多 seed 方差或显著性检验，方法间 1–2 个点的差异不可判读。
    - （我在正文发现）本次全文为 v2（2026-03-11）只含 3 项任务，而 arXiv v3 摘要另列 Video-Grounded Cross-View VQA，正文缺少该任务章节，版本内容不一致。
- **与文献库的关系**：本文是作者团队前作 Ragusa et al.（2024）ENIGMA 的扩展：新增 129 段 ego 与全部 180 段 exo，补齐时序与空间标注。横向与 MECCANO（Ragusa et al., 2023）、IndustReal（Schoonbeek et al., 2024，玩具车装配）、Assembly101（Sener et al., 2022）划界——后者均非真实工业对象；与 Ego-Exo4D、H2O、LEMMA、IKEA ASM 相比，差异在工业维修流程与 keystep 级标注。基线覆盖 C2F-TCN、ASFormer、LTContext、MSTCN++、DiffAct、FACT、TimeSformer 与 VISOR HOS/Leonardi 系列。本篇为旧稿 v2/v3 再公告（v1 未入馆），按首次入馆处理。
- **可复现性**：数据集、标注与附加资源公开：https://fpv-iplab.github.io/ENIGMA-360/ ，含 360 段视频、keystep/HOI/物体/手框标注、SAM-HQ 掩码、DINOv2 1024 维特征 LMDB、Matterport/ARTEC EVA 重建的实验室与物体 3D 模型。基线代码未声明单独发布；TAS 与 HOI 基线均引用公开实现（C2F-TCN、ASFormer、LTContext、MSTCN++、DiffAct、FACT、VISOR HOS）。采集硬件 HoloLens 2 + ZED，标注工具为定制 VIA Subtitle Annotator。
- **行动建议**：先读 §3.2 采集与同步（灯泡对齐）和 §3.3 标注统计，再核对 §4.1/4.3 的跨视角协议。核四个数字：14,556 段与 12,597 帧是否互斥口径、17,363 只手与 56,473 个手框的统计层级、111.54 h 是否含 exo、103/29/48 是否 subject-disjoint。重点看 Table 3b 的崩塌幅度是否为标注/对齐问题而非模型问题。风险点：单实验室、ego-only 空间标注、无方差统计。

### 第 6 章 · GUSH3R：单目视频前馈式动态人体–场景高斯重建（2607.05243，3.42 B，FULL）

- **赛道 / 场合**：重建与SLAM / arXiv preprint（cs.CV）
- **公告类型**：replace（公告日 2026-11-13，拉取日 2026-11-14）
- **一句话结论**：GUSH3R 以 Human3R 的点云、SMPL-X 与 token 为先验，加场景与人体两个高斯解码器，在单目视频上以 0.54 s/帧流式前向输出统一 3DGS 表示；MultiEgo 新视角视频 PSNR 14.2（DA3 13.9、StreamSplat 13.2）、warping error 0.0015 最低、8 帧 5.50 s；NeuMan 18.2 dB 低于优化式 HSR 的 20.6，但 EMDB 18.0 高于 16.2，BEDLAM 多人全图 17.0 优于 AnySplat 15.9。
- **要解决的问题**：单目人体–场景重建要同时解场景几何、相机运动与非刚性人体，还要能照片级渲染。优化式方法（NeRF/3DGS 系，HSR、Vid2Avatar）质量高但需 per-scene 优化，无法快速或交互式重建；多视角动态方法要求同步多机位。前馈方法（VGGT、MASt3R-SfM、CUT3R、AnySplat、Depth Anything 3）能一次前向出几何，但输出多为点云/网格，不可直接渲染，或对非刚性人体失效；Human3R、UniSH 虽能一次前向给出场景点云 + SMPL-X 人体，输出却是异质表示，需额外外观建模或表示转换才能渲染。作者据此把「统一、可渲染、流式、免 pose 输入」作为缺口：现有前馈工作没有同时满足 streaming、dynamic humans、photo-reality 三项（Table 1）。
- **方法详解**：把场景分为跨时间累积的静态高斯 G_t^s 与逐帧的 K 个人体高斯 {G_{t,k}^h}，二者在 Human3R 的同一度量坐标系内直接预测。Human3R 逐帧输出相机位姿 T_t、点图 X_t、SMPL-X 顶点 V_{t,k}与循环状态 [F'_t,z'_t,H'_t]=Decoder([F_t,z_t,H_t],S_{t-1})。场景解码器以点图作高斯中心 μ_{t,i}，用 DPT 式解码器把 F'_t 解为逐像素特征 C^D，与 7×7 卷积的图像特征 C^I 相加，经卷积头 F_G 预测 (α,q,s,c)；新帧先按点置信度与膨胀人体掩码过滤，再按固定体素 Voxelize(G_{t-1}^s,G̃_t^s)，每体素按置信度取舍与加权。人体解码器以 SMPL-X 顶点为锚，定义人体 h、A-pose 规范顶点 V̂、图像 F'、记忆 m 四类 token；HGT 对 h/m/V̂ 自注意力、对 F' 交叉注意力，[m',V̂']=HGT(Q=[h,m,V̂],K=V=F')；顶点特征经 MLP F_H 预测 (α,q,s,c)，在规范空间定义后用 LBS 变换到当前姿态。记忆 m_{t+1}=(1−λ)m_t+λm'_t。冻结 Human3R、分别训练两解码器：L_scene 含 mse、lpips、depth 与尺度比正则（比值>3 受罚）；L_human 含 mse、全图与半身/面部 crop 的 LPIPS、silhouette 与同样的 reg。数据：场景 BEDLAM+DL3DV、人体 BEDLAM+MVHumanNet，每样本 4 帧等间隔。
- **实验与结果**：
    - 单人体（Table 2）：NeuMan 上 Ours 18.2 / 0.57 / 0.29、HSR 20.6 / 0.58 / 0.58（>1 h）、AnySplat 15.2 / 0.33 / 0.42（0.47 s）、AnySplat+LHM+Human3R 13.9 / 0.32 / 0.46（5.5 s）；EMDB 上 Ours 18.0 / 0.57 / 0.40、HSR 16.2 / 0.68 / 0.51；重建时间 0.54 s/帧。
    - 多人场景（BEDLAM，Table 3）：全图 Ours 17.0 / 0.53 / 0.34 优于 AnySplat 15.9 / 0.43 / 0.42；背景区 17.5 / 0.59 / 0.30；人体区 14.2 / 0.88 / 0.11，低于 AnySplat+LHM+Human3R 的 14.7 / 0.88 / 0.11。
    - 新视角视频（MultiEgo，Table 4）：Ours 14.2 / 0.70 / 0.38、warp error 0.0015、8 帧 5.50 s；DA3 13.9 / 0.68 / 0.45、2.26 s；StreamSplat 13.2 / 0.49 / 0.52、0.0099、5.91 s；MoVieS 12.9（需 pose，2.02 s）；Shape of Motion 12.2（274.3 s）。
    - 组件消融（NeuMan，Table 5）：场景去深度损失 19.7→19.3（4-view），去 DL3DV 仅 19.7→19.5；人体去交叉注意力 12.6→11.0（4-view）、13.7→12.4（8-view），去记忆 token 12.6→12.5，去 MVHumanNet 12.6→12.4。
    - 长序列（附录 B.3，500 帧）：体素 0.01 m 时累计 16.20M 高斯、234 帧即 OOM；0.03 m 与 0.05 m 可跑完 500 帧，峰值 15.26M / 12.23M，额外显存 3.31 GB / 1.30 GB。
    - 运行时（附录 B.4，NeuMan 8 帧均值）：总 540.27 ms/帧，其中 Human3R 推理 264.82 ms（49.0%）、场景解码 73.05 ms（13.5%）、人体解码 39.47 ms（7.3%）、更新与 I/O 162.93 ms（30.2%）。
- **创新点与贡献**：
    - 首个从单目视频前馈、流式输出「照片级可渲染」动态人体–场景统一 3DGS 表示的方法，把 streaming / dynamic humans / photo-reality 三项同时满足。
    - 不做「先分别重建再对齐」，而是共用 Human3R 的度量坐标系与 token，从结构上消除分解式管线的拼缝伪影。
    - 人体侧以 SMPL-X 顶点为锚、在 A-pose 规范空间预测高斯再用 LBS 驱动，并用记忆 token 维持跨帧外观一致（λ=0.5 指数滑动）。
    - 场景侧用体素化 + 置信度加权聚合实现常数级背景增长，使 500 帧长序列仍可在单卡运行（0.05 m 体素仅增 1.30 GB）。
- **局限与风险**：
    - （作者承认）依赖 Human3R 的相机、点图、人体检测与 SMPL-X 拟合，上游误差会传播到最终重建。
    - （作者承认）严重人–人遮挡与复杂交互仍困难，单目下身份关联与完整人体几何线索不足。
    - （作者承认）面部、手部、衣物在运动模糊/大幅度姿态变化/观测不足时仍有可见伪影；每顶点一个高斯限制头发与宽松衣物的细节。
    - （我在正文发现）NeuMan 上 PSNR 18.2 低于优化式 HSR 的 20.6，背景区在 NeuMan 也不及 AnySplat（Table 7），绝对渲染质量仍偏弱。
    - （我在正文发现）评测时目标帧 SMPL-X 由对整段序列（含目标帧 RGB）的额外 Human3R pass 估计，虽声明不用于外观，仍引入「用未来帧估姿态」的乐观假设。
    - （我在正文发现）人体高斯随帧累积不合并，500 帧即达 12–16M 高斯、1.3–3.3 GB 额外显存，长视频可扩展性受限于此。
- **与文献库的关系**：本文直接构建在 Human3R（Chen et al., 2026，ICLR）之上：沿用其循环状态、点图、SMPL-X 与 image/human token，只新增两个高斯解码器，与 Human3R、UniSH 构成「几何先验 → 可渲染表示」的接力。静态前馈侧对标 VGGT、MASt3R-SfM、CUT3R、AnySplat、StreamSplat、Depth Anything 3；动态侧与优化式 Shape of Motion、前馈 MoVieS、4DGT、StreamSplat 比较；人体侧用 LHM 做分解式基线、HSR 做优化式基线，并以 SMPL-X、BEDLAM、MVHumanNet 为表示与数据基础。相较 AnySplat+LHM 的「分别重建后组合」，本文主张共享坐标系联合预测可同时改善质量与速度。本篇为旧稿 v2 再公告（v1 未入馆），按首次入馆处理。
- **可复现性**：代码公开：https://github.com/abkeito/GUSH3R 。数据集 NeuMan、EMDB、BEDLAM、MultiEgo 均为公开基准；Human3R 冻结、两个解码器分别训练（BEDLAM+DL3DV、BEDLAM+MVHumanNet），训练细节在附录 A.1。计时在单张 NVIDIA A100 上测得（8 帧输入）。3DGS 光栅化器与 DPT、ViT 等组件均为公开实现。
- **行动建议**：先读 §3.3 的体素化聚合与 §3.4 的四类 token/HGT，再看 Table 2 与 Table 4 两组主结果。核三个数字：0.54 s/帧是否含 Human3R（附录 B.4 说含，占 49%）、NeuMan 18.2 与 HSR 20.6 的差距是否被「快 1000×」掩盖、MultiEgo 的 14.2 是否与 DA3 的 13.9 在统计上可区分。风险点：绝对 PSNR 偏低、目标帧姿态用未来信息、人体高斯线性增长。

### 第 7 章 · COSMO-Bench：协同 SLAM 优化基准（2508.16731，3.34 B，FULL）

- **赛道 / 场合**：评估与数据集 / arXiv preprint（cs.RO）
- **公告类型**：replace（公告日 2026-11-13，拉取日 2026-11-14）
- **一句话结论**：COSMO-Bench 用真实 LiDAR 轨迹（MCD 10 条 + CU-Multi 2 条）经统一 C-SLAM 前端（LOAM + 2 m 关键帧 + ScanContext + KISS-Matcher）与两种通信模型（Wi-Fi 2000 KB/s、Pro-Radio 1000 KB/s）派生 12 条序列 × 2 = 24 个后端基准数据集，含 358–2,019 个内回环（外点率 2.7%–19.5%）、参考解、经验噪声模型与 95% χ² 外点标注，全部以 JRL 格式与 DOI 公开。
- **要解决的问题**：分布式 C-SLAM 后端长期缺标准 benchmark，三种替代做法都不够用：①纯仿真可扩展但抓不住真实噪声的非参数、非平稳与外点；②把单机 benchmark（M3500、Intel、MIT-Killian、Garage、CSAIL）切分给多机器人，不符合真实多机的拓扑、视角差异与测量分布，也无外点，且 g2o/toro 格式不含时间；③闭源真实多机数据（部分 DDF-SAM2、DLGBP 评测）无法复现。开源多机数据又要求各自实现前端，前端差异会淹没后端差异。最接近的是 UTIAS 多机 benchmark（人工构造、受控实验室）与 Nebula（4 条地下隧道、LAMP 2.0 集中式回环），后者不符合分布式假设、样本也不足以测泛化。作者据此提出六条要求：代表性测量、充足回环、长轨迹（>1 km）、精确参考解、时间信息、易用性。
- **方法详解**：以 LiDAR 对光照/季节不变为前提，把同一环境多次单机采集在时间上拼成「伪多机」序列：选一条作锚 t*，其余按 Δ_i~N(0 s,40 s) 采样相对起始时间 t_i=t*+Δ_i。原始数据用 MCD 与 CU-Multi，标定由 evalio 统一处理。前端：LOAM 出里程计，行程超 d_kf=2 m 取关键帧；帧内与机间回环均用 ScanContext + RingKey 两阶段检索，并为每个队友维护独立描述子库；回环测量用 KISS-Matcher 计算（仍会产生真实外点）。通信模型：T_ab=(B/I_ab(t,Θ*))·C_ab(t,Θ*)·δ，B 为共享带宽、I_ab 为 d_intf 内同时通信数、C_ab~Bern(φ(d_ab))，φ(d)=min(P_max,α(β^{d/r_max}−β)) 由 Lajoie 等三机器人行星类比实验的 Wi-Fi 实测手工拟合；d_init 保证有时隙完成传输，超时 T=2 s。Wi-Fi 参数 B=2000 KB/s、d_init=30、d_intf=40、P_max=0.7、α=1.1、β=0.1、r_max=70；Pro-Radio 为 1000/150/150/0.8/1.8/0.3/200。传输关键帧的 [x,y,z] 32 位浮点，xz 压缩比 f~N(0.653,0.04)。参考解按关键帧取自 MCD 测绘级地图对齐与 CU-Multi LIO+RTK-GPS+DEM 结果；先验 σ_r=1e-4 rad、σ_t=1e-3 m；协方差在 se(3) 切空间估计；外点按加权残差超 95% χ² 判定。
- **实验与结果**：
    - 规模：12 条序列（MCD 10 条：ntu_r3/r4/r5、kth_r3/r4、tuhh_r3 系列；CU-Multi 2 条：kittredge_loop、main_campus），每条配 Wi-Fi 与 Pro-Radio 两个通信模型，共 24 个数据集。
    - 序列元数据（Fig. 1）：时长 5:47–46:12、里程 2.13–9.23 km；内回环 356–2,019 个（外点率 2.7%–19.5%），机间回环 Wi-Fi 26–2,821 个（0.0%–15.7%）、Pro-Radio 194–3,217 个（2.4%–19.4%）。
    - 前端组成：LOAM 里程计 + 2 m 距离关键帧 + ScanContext 两阶段检索 + KISS-Matcher 位姿计算；所有前端超参随数据集一并发布。
    - 通信仿真：δ=0.1 s 步长，单次通信超时 2 s；Wi-Fi 峰值带宽 2000 KB/s、Pro-Radio 1000 KB/s；连通概率由 φ(d)=min(P_max, α(β^{d/r_max}−β)) 伯努利采样。
    - 参考解与标注：MCD 对齐测绘级地图、CU-Multi 用 LIO+RTK-GPS+DEM；噪声模型按平台各取一趟（NTU=Night 4、KTH=Day 6、TUHH=Day 2、CU=Kittredge Loop Robot 3）；外点按 95% χ² 判定。
    - 附赠 Nebula 4 条（tunnel 71:06/2.59 km、urban 44:33/1.55 km、ku 57:54/6.01 km、finals 41:12/1.21 km），统一转 JRL 并重估噪声模型；正文提示 urban 的参考解存在扫描错位、精度不足。
- **创新点与贡献**：
    - 提出用「同一环境多次单机采集 + 时间平移」构造真实多机序列的路线，并用 LiDAR 的光照不变性论证其可行性，绕开真实多机数据稀缺。
    - 把通信模型作为数据集的一部分显式建模：从真实三机器人 Wi-Fi 实测拟合距离–连通概率曲线，给出 Wi-Fi 与 Pro-Radio 两套可复现参数。
    - 交付 24 个带参考解、经验噪声模型、χ² 外点标注与时间戳的后端数据集，并统一为人类可读、平台无关的 JRL 格式（而非 g2o/toro）。
    - 同时把 Nebula 4 条转成同一格式并修正其过于乐观的噪声模型，使新旧 benchmark 可在同一口径下比较。
- **局限与风险**：
    - （作者承认）通信模型的「同一时刻仅一对通信」「带宽均分」「忽略丢包时延」三条假设偏理想，且距离型连通函数不显式建模建筑/植被/墙体遮挡。
    - （作者承认）Nebula 的 urban 数据集参考解不准，扫描存在错位。
    - （我在正文发现）全文没有任何后端算法在这 24 个数据集上的基线结果或难度分层，无法从论文本身判断 benchmark 是否真的能区分方法。
    - （我在正文发现）时间对齐假设环境在多次采集间基本静态（仅以「动态物体」类比），对家具移动、施工、人流变化敏感的场景未评估。
    - （我在正文发现）通信模型的两个实例均由手工拟合/按比例缩放得到，正文未给出拟合误差或与留出实测的验证。
    - （我在正文发现）机间回环的扫描选择是「随机挑一帧未发送过的关键帧」，与真实系统中基于信息增益的调度差距较大。
- **与文献库的关系**：本文与同期 riMESA（2603.01178）构成「benchmark + 算法」的配套关系：riMESA 正是用 COSMO-Bench 的 24 个数据集与 Nebula 的 4 条做真实世界评测。方法上把单机 benchmark 的传统（M3500、Intel、MIT-Killian、Garage、CSAIL 提供前端测量供后端比较）迁移到多机，并与三种既有做法划界：仿真多机数据、切分单机数据、闭源真实数据。最直接的前作是 Nebula（LAMP 2.0，4 条地下隧道、集中式回环）与 UTIAS 多机 benchmark；前端组件全部复用公开实现——LOAM、ScanContext、KISS-Matcher、evalio，数据来自 MCD 与 CU-Multi，通信曲线来自 Lajoie 等的三机器人实测。本篇为旧稿 v2 再公告（v1 未入馆），按首次入馆处理。
- **可复现性**：完全公开：数据 DOI 10.1184/R1/29652158，入口 https://cosmobench.com ，JRL 格式解析器 https://github.com/DanMcGann/jrl 。24 个数据集 + Nebula 4 条 + 前端全部超参随发布提供；前端依赖 evalio（https://github.com/contagon/evalio）、ScanContext（https://github.com/DanMcGann/scan_context）、KISS-Matcher（https://github.com/MIT-SPARK/KISS-Matcher），均为开源。
- **行动建议**：先读 §IV-B 前端与 §IV-C 通信模型，再对照 Fig. 1 的 12 条序列元数据表。核四个点：外点率（2.7%–19.5%）是否覆盖足够难度梯度、Pro-Radio 的 1000 KB/s 与 150 m 初始化阈值是否有实测依据、参考解精度（尤其 CU-Multi 与 Nebula urban）、时间平移 40 s 的标准差对回环分布的影响。风险点：论文本身不含后端基线，选型时需自行跑一遍验证区分度。

### 第 8 章 · ReflFlow：几何引导光线追踪的动态高光重建（2512.10095，3.00 B，FULL）

- **赛道 / 场合**：渲染与显示 / arXiv preprint（cs.CV）
- **公告类型**：replace（公告日 2026-11-13，拉取日 2026-11-14）
- **一句话结论**：在 NeRF-DS 七个动态高光场景上，ReflFlow 用 2DGS 的免近似法线、残差材质增广、动态环境高斯与光栅/光追混合管线，把平均 PSNR 从 SpectroMotion 的 24.17 提到 24.91（+0.74 dB）、SSIM 0.8522→0.8880、LPIPS 0.1778→0.1471；代价是 HyperNeRF 上 22.47 dB 低于 4DGS 的 24.89，且训练 2.8 h、推理 32 FPS。
- **要解决的问题**：动态高光的两个物理前提——精确反射方向与可信反射模型——在单目 3DGS 体系里都不成立。3DGS 不显式表达表面，法线依赖近似（GaussianShader、SpectroMotion 等），误差会经 d_out=d_in−2(d_in·n)n 放大到高光颜色；环境贴图只能近似远场照明，受分辨率限制且无法表达近场反射（正文以 Press 场景镜中苹果未被重建为例）。NeRF-DS 用逐帧表面朝向条件化辐射场，7DGS 把方向纳入 7D 高斯，SpectroMotion 引入动态环境贴图并分解漫反射/高光，EnvGS 用环境高斯做静态视角相关外观——但没有方法同时解决「动态几何的法线精度」与「动态环境的近场高光」。此外仅监督最终颜色会使漫反射/高光分解病态，动态场景下缺少稳定化方案，训练早期易收敛到退化解。
- **方法详解**：以 2DGS 为几何载体：基元有中心 p_k、切向 t_u,t_v、缩放 S=(s_u,s_v)，P(u,v)=p_k+s_u t_u u+s_v t_v v，G(u)=exp(−(u²+v²)/2)，法线由 t_w=t_u×t_v 直接给出，故不必估法线即可算 d_out=d_in−2(d_in·n)n。每个 2D 高斯另加可学习 specular tint s_tint∈[0,1]，并用时间条件残差网络 ΔG^t=F_θG(p,t) 预测 (Δp,Δs,Δr,Δo,Δs_tint) 加到基准属性。几何监督两项：L_norm=(1/N_p)Σ(1−n_i^T N_d(u_i))，N_d 由深度梯度叉积归一化；另用 NormalCrafter 扩散先验法线 N_e 构造 L_tc-norm=(1/N_p)Σ(1−n_i^T N_e) 抑制闪烁。反射用 Dynamic Environment Gaussian G_env，同样以 F_θenv(p,t) 预测时间偏移；颜色分解 C=(1−α_spec)C_diffuse+α_spec C_specular，α_spec=Σ_i s_tint,i α_i Π_{j<i}(1−α_j) 由一次额外光栅化得到。混合渲染：C_diffuse 走 2DGS 光栅化，C_specular 由光追对每条反射射线取最多 k 个交点，C_specular=Σ_{i=1}^k T_i·G_i(H_i^{-1}x_i)·c_i。训练 60k 步三阶段：0–9k 仅漫反射、9k–15k 冻结漫反射只训高光、15k–60k 联合微调。
- **实验与结果**：
    - 数据与设置：NeRF-DS 七个单目动态高光场景（As/Basin/Bell/Cup/Plate/Press/Sieve）加 HyperNeRF，均用数据集自带 points.npy 初始化；指标 PSNR / SSIM / LPIPS(VGG)。
    - NeRF-DS 平均（Table 1）：Ours 24.91 / 0.8880 / 0.1471，SpectroMotion 24.17 / 0.8522 / 0.1778，NeRF-DS 23.24 / 0.8384 / 0.2402，4DGS 22.79 / 0.8235 / 0.2115，Deformable 3DGS 23.43 / 0.8284 / 0.2201。
    - 单场景：Sieve 27.95 对 SpectroMotion 25.22；Press 27.39 对 26.49；Plate 21.10 对 20.84；As 26.73 略低于 26.80。
    - HyperNeRF（Table 2）：Ours 22.47 / 0.6328 / 0.3106，4DGS 24.89 / 0.6781 / 0.3422，NeRF-DS 23.65 / 0.6405 / 0.3972；LPIPS 最优但 PSNR/SSIM 非最优。
    - 模块消融（4 场景均值，Table 3）：base 16.29→加 F_θG 18.97→加 F_θenv 20.25→加 L_norm 22.12→加 L_tc-norm 25.23；LPIPS 0.4126→0.2389→0.2313→0.2149→0.1536。
    - Coarse-to-fine 消融：去掉后 15.28 / 0.5782 / 0.4471，完整 21.10 / 0.8415 / 0.1821（4 场景）。
    - 效率（RTX 6000 Ada）：60k 步 2.8 h、32 FPS；SpectroMotion 40k 步 1.1 h、33 FPS。
- **创新点与贡献**：
    - 用 2DGS 的切向叉积直接给出法线，从表示层面消除「法线近似→反射方向偏差」的误差链，而不是在网络里补偿估计误差。
    - 把 specular tint 做成逐高斯的可学习材质参数，并用一次透射率加权光栅化得到 α_spec，使漫反射/高光混合权重既视角相关又几何相关。
    - 以 Dynamic Environment Gaussian 替代环境贴图，支持时间变化照明与近场反射，配合光追查询实现物理可信的高光合成。
    - 给出针对动态高光的三阶段 coarse-to-fine 调度，把「仅监督最终颜色」的病态分解稳定下来（去掉后 21.10→15.28 dB）。
- **局限与风险**：
    - （作者承认）单目动态重建本身病态，细粒度运动与非刚性形变下几何模糊会直接削弱法线与反射方向可靠性。
    - （作者承认）只处理单次反射；多次互反射在单目下不可辨识。
    - （作者承认）空间变化 BRDF 的光泽材质仍困难，材质与光照分解欠约束。
    - （我在正文发现）HyperNeRF 上 PSNR 22.47 明显低于 4DGS 的 24.89、SSIM 0.6328 低于 0.6781，泛化到非高光动态场景时不如纯动态重建方法。
    - （我在正文发现）训练 2.8 h 是 SpectroMotion 1.1 h 的约 2.5 倍，且依赖 NormalCrafter 外部法线先验，其误差会经 L_tc-norm 传入几何。
    - （我在正文发现）代码仅承诺「接收后 release」，当前无仓库，复现需自备 2DGS、EnvGS 光追器与 NormalCrafter 三套组件。
- **与文献库的关系**：本文站在三条脉络交汇处：几何侧继承 2DGS（Huang et al., 2024）的射线–splat 求交与法线一致性损失，替代 3DGS（Kerbl et al., 2023）的近似法线；反射侧对标 GaussianShader（Jiang et al., 2024）、GS-IR（Liang et al., 2024）、EnvGS（Xie et al., 2025）的「漫反射/高光分解 + 环境表示」路线，并把 EnvGS 的静态环境高斯扩为带残差网络的时间变化版本；动态侧与 NeRF-DS（Yan et al., 2023）、Deformable 3DGS、4DGS、SpectroMotion（Fan et al., 2024）对比，差异在用 2D 面元保证法线精度、用光追而非环境贴图取高光。本篇为旧稿 v2 再公告（v1 未入馆），按首次入馆处理。
- **可复现性**：代码与模型未公开，正文写明「will release our code and trained models upon acceptance」，当前无仓库链接。数据集 NeRF-DS 与 HyperNeRF 公开，均使用官方 points.npy 初始化。训练 60k 步、单卡 2.8 h（RTX 6000 Ada），三阶段切分点在附录 A 给出；法线先验依赖 NormalCrafter（arXiv 2504.11427）。
- **行动建议**：先读 §4.1 的 2DGS 法线论证与 §4.2 的 α_spec/光追公式，再对照 Table 1 的逐场景数值与 Table 3 的增量消融。核三处：+0.74 dB 只相对 SpectroMotion（对 4DGS 的 22.79 则为 +2.12）、HyperNeRF 掉点是否被正文淡化、LPIPS(VGG) 口径与基线是否一致。风险点：无代码、训练成本高、法线依赖外部扩散先验、单次反射假设限制互反射场景。

## 四、当日全量 7 维度对比表（参考）

见 [`papers/daily/2026-11-14/7dim-table.md`](../papers/daily/2026-11-14/7dim-table.md)。

## 五、覆盖率校验与筛选过程说明

- 门①/门③ 对 backfill 不适用（非当日新提交，不参与重磅日判定）；门② 覆盖 6 赛道（重建与SLAM×2 / 世界模型与仿真×1 / 神经渲染×1 / 交互与输入×1 / 评估与数据集×2 / 渲染与显示×1）。
- **口径说明（重要）**：本批最高 4.50 若计入主批将越过门③ 的 4.4100 线，但按既定口径 backfill 不参与重磅日判定、≥4.2 一律记 A，故本报告不宣称 S 级。


## 六、附录：证据等级分布与抓取记录

- 本表 8 篇：FULL 8 篇；PARTIAL 0 篇；ABSTRACT_ONLY 0 篇。
- 抓取降级：28 篇候选串行 3s/篇，全部 L0 一次命中（43,212–171,293 字符）；无 406/429 重试、无 L1–L5 降级、无 OCR。无限流、无伪造。
