# XR Backfill 补录报告 · backfill-1103（旧稿再公告）

## 一、执行摘要
- **批次性质**：backfill（非当日新提交）——11-02 公告批次中 RSS 混入的旧稿 replace 再公告 2 篇，首次入馆；原始投稿 2511=2025-11（v2 于 2026-10-29 更新）/ 2602=2026-02（v2 于 2026-10-30 更新）。
- **补录 2 篇（1 A / 1 B）**：DiTGaze 3.72（南安普顿大学，几何条件 latent DiT 渲染的少样本视线估计数据增强，N=9 受试级误差 5.63°→4.90°、14/15 身份改善 p<0.001）· AdaGS 3.58（香港科技大学（广州），置信门控扩散适应的无位姿稀疏视图 3DGS 重建，DL3DV/Waymo/KITTI 11 基线全面最优）。
- **覆盖 2 赛道**；门① 0.116（全池合并复核）；门③ 对 backfill 不适用；OUTDATED 0。
- **诚实口径**：全部条目 `batch=backfill-1103` + `orig_window` 标注，绝不混入「当日新论文」。

## 二、排行榜（按加权降序）

| 排名 | 论文 | 赛道 | 总分 | 等级 | 证据 | 落后标记 |
|---|---|---|---|---|---|---|
| 1 | DiTGaze：几何条件扩散增强的少样本视线估计（2511.11231） | 感知与认知 | 3.72 | A | FULL | — |
| 2 | AdaGS：置信门控扩散自适应的无位姿稀疏视图 3DGS 重建（2602.21535） | 重建与SLAM | 3.58 | B | FULL | — |

## 三、逐篇深度解读

### 第 1 章 · DiTGaze：几何条件扩散增强的少样本视线估计（2511.11231，3.72 A，FULL）

- **赛道 / 场合**：感知与认知 / arXiv preprint（英国南安普顿大学 School of Electronics and Computer Science，cs.CV，2025-11 提交，v2 于 2026-10 更新）
- **公告类型**：replace（旧稿 replace 再公告（首次入馆）：2511=2025-11 投稿（v2 于 2026-10-29 更新）、2602=2026-02 投稿（v2 于 2026-10-30 更新），2026-11-02 公告批次 RSS 混入）
- **一句话结论**：DiTGaze 在 GazeGaussian 双流 3DGS 骨干上加入中间 yaw-pitch 采样、变形正交约束与几何条件 latent DiT 渲染器，生成器级视线误差 6.622°→6.353°（相对降 4.1%），在 1–9 shot 全预算排名第一；N=9 重复配对比较把受试级估计误差从 5.63° 降到 4.90°（降 0.73°，15 个身份中 14 个改善，p<0.001）。
- **要解决的问题**：个人化 gaze estimator 需要密集覆盖各视线方向的标注数据，但逐用户采集成本高、侵入性强；用少量校准图像做 gaze redirection 生成合成监督是可行路线，但图像空间 warping 与 2D 生成不显式建模眼部几何，且视觉逼真不等于标签可靠——虹膜微小误差直接改变 gaze 标签，身份、表情、头姿变化引入错误监督。核心问题：在何种条件下，几何条件的重定向能把小校准集变成有用的 few-shot 个人化监督？
- **方法详解**：沿用 GazeGaussian 双流 3D Gaussian Splatting 骨干（中性网格经 DMTet 初始化，Face Deform Field 预测表情/头姿条件的高斯偏移 Δx，Eye Rotation Field 预测 gaze+表情驱动的眼球旋转 Δq；面部各向异性、眼球各向同性高斯，光栅化为 32 通道特征图）。三项改进：(1) Intermediate Gaze Sampler 在与 Eye Rotation Field 同一的 yaw-pitch 坐标系中，于 N_grid×N_grid 网格（范围 ±R_gaze）上直接采样中间目标，混合随机采样与「早期中心偏置→后期均匀覆盖」课程，替换 gaze-redirection 损失中的目标图像 gaze，实现无像素对齐图像的连续角度监督；(2) 正交约束 L_ortho=w1|cos(v_gaze,v_expr)|+w2|cos(v_pose,v_expr)| 作用于 gaze/pose/expr 三个变形 MLP 首层嵌入，减少表情对 gaze 与 pose 的干扰；(3) 几何条件 latent DiT 渲染器：32 通道高斯特征图经可学习 1×1 投影为 3 通道 VAE 兼容表示，冻结 VAE 压缩至 4 通道 latent，patchify + 2D 正弦位置编码，6 个 DiT block（每块 8 个注意力头）迭代去噪，diffusion timestep 与身份/表情编码经 AdaLN 注入 scale/shift，最终经冻结 VAE 解码器成图。总损失 L=λ_I L_I+λ_G L_G+λ_ortho L_ortho（eye/face/head 分区 L1+SSIM+VGG 感知损失）。测试时先 30 秒身份自适应，再离线生成；下游微调 ResNet-50 估计器。
- **实验与结果**：域内（ETH-XGaze 测试集，15 个未见身份各 200 张，训练 80 身份 14400 张）：gaze 6.353° vs GazeGaussian 6.622°（-4.1%）、GazeNeRF 6.944°、STED 16.217°；PSNR 20.512（+1.778dB）、LPIPS 0.187（-13.4%）、ID 相似度 71.724（+3.975）、FID 38.319；pose 误差 2.349° 微升 0.221°（去正交约束升至 2.572°）。跨域（ColumbiaGaze/MPIIFaceGaze/GazeCapture）gaze/LPIPS/ID 全面最优（如 ColumbiaGaze gaze 7.265° vs 7.415°、ID 64.963 vs 59.788）。下游 1–9 shot（B=200，15 受试）：N=9 时 4.8° vs GazeGaussian 5.3°、GazeNeRF 5.9°、STED 7.9°、real-only 6.7°；平均较 GazeGaussian 降 10.3%、较 real-only 降 31.8%。N=9 重复比较（5 次校准抽样 × 3 估计器种子）：5.63±1.39°→4.90±1.29°，配对 Δ=0.73°（95% CI [0.49,0.97]），Wilcoxon p=1.83×10⁻⁴、r_rb=0.967。消融：去掉 gaze sampling +0.680°、DiT 渲染器 +0.346°、正交约束 +0.120°。合成数扫描：S=50→191 降 0.797°，191→300 仅 0.020°（饱和，目标多样性比数量更关键）。ETH→MPII 迁移 9.5° 仍最优。
- **创新点与贡献**：['将 latent DiT 作为 3DGS 渲染阶段的几何条件渲染器（可学习特征图投影 + 冻结 VAE + AdaLN 的 timestep/身份/表情条件），在保持显式 3D gaze 控制的同时提升保真度', 'Intermediate Gaze Sampler 在显式 yaw-pitch 空间提供连续 gaze-space 监督，直接扩展 Eye Rotation Field 的角度覆盖', '针对表情-gaze/pose 纠缠的变形嵌入正交约束', '校准高效的离线增强系统与固定 B=200 的 real+synthetic 微调协议（30 秒生成器身份自适应）', '需求驱动的系统评估：配对统计、校准/合成预算扫描、生成器级与下游级双消融、in/cross-domain、成本与失败模式分离']
- **局限与风险**：论明明示：离线生成而非实时（191 张需 31.5–36.3 s，单图 165–190 ms、约 40 GFLOPs）；pose 刚性小幅让步（+0.221°）；细框眼镜等 thin accessories、极端 gaze、异常光照下失败；合成样本超过 191 后收益饱和；未建立对预留方向的单调角度响应（需独立 angular-coverage 审计）；共享 gaze 标注器可能存在偏差；跨域残差仍大（域内 4.8°→跨域 9.5°）。客观不足：仅评测 ResNet-50 估计器；两阶段训练约 110 GPU-hours（A100-SXM4）。
- **与文献库的关系**：处于 3D 视线重定向线：STED（2D latent 变换）→ GazeNeRF（CVPR 2023，双流 NeRF）→ GazeGaussian（ICCV 2025，双流 3DGS 加 Eye Rotation Field，本文直接继承的骨干）→ DiTGaze（几何条件 latent DiT 渲染）。上游连接 Gaussian Head Avatar（CVPR 2024，动态高斯头部）与 DMTet/DeepSDF 几何初始化；渲染侧承接 latent diffusion（Rombach et al. 2022）与 DiT（Peebles & Xie 2023），首次将其用于 gaze-controlled 头部重定向。下游沿用 GazeNeRF/GazeGaussian 的 few-shot 协议，与 FAZE（无合成元学习）、Render-to-Adapt（无监督自适应）构成校准策略对照。
- **可复现性**：原文未承诺代码开源（未给出仓库链接）；数据全部使用公开数据集（ETH-XGaze、ColumbiaGaze、MPIIFaceGaze、GazeCapture），未收集新个人数据；实验在单张 NVIDIA A100-SXM4 上完成，两阶段训练约 110 GPU-hours、峰值显存 14.2 GB、推理 4.8 GB，论文给出 Adam（lr 1e-4 + step decay）等优化细节与身份自适应流程。
- **行动建议**：眼动追踪校准数据增强的离线工具：1-9 shot 全预算排名第一、N=9 受试级估计误差 5.63°→4.90°（15 个身份中 14 个改善，p<0.001）、平均较 GazeGaussian 降 10.3%、较 real-only 降 31.8%，可直接用于 HMD 眼动仪 per-user 校准的数据扩充；离线生成（191 张需 31.5-36.3 s）不适合实时、无代码、跨域残差大（域内 4.8°→跨域 9.5°）、合成数超 191 后收益饱和是主要限制。

### 第 2 章 · AdaGS：置信门控扩散自适应的无位姿稀疏视图 3DGS 重建（2602.21535，3.58 B，FULL）

- **赛道 / 场合**：重建与SLAM / 作者团队来自香港科技大学（广州）（Beizhen Zhao、Sicheng Yu、Guanzhi Ding、Yu Hu，通信作者 Hao Wang），cs.CV 预印本（arXiv:2602.21535），2026 年 2 月首帖、v2 于 2026 年 10 月 30 日再公告；属 backfill 批次旧稿，原文未述正式会议投稿信息
- **公告类型**：replace（旧稿 replace 再公告（首次入馆）：2511=2025-11 投稿（v2 于 2026-10-29 更新）、2602=2026-02 投稿（v2 于 2026-10-30 更新），2026-11-02 公告批次 RSS 混入）
- **一句话结论**：AdaGS 用两阶段训练的 artifact-aware adapter 抑制 floater 线索、以双向置信融合门控扩散伪视图、并以表征侧高斯稳定化打断 artifact amplification loop，在 DL3DV/Waymo/KITTI 三个户外数据集上取得 PSNR 24.27/23.76/17.95 与 ATE RMSE 0.077/1.352/2.471，全面优于 11 个基线。
- **要解决的问题**：无位姿稀疏视图下的户外 3D 高斯泼溅重建中，早期高斯优化欠约束，渲染图常含 floating Gaussian artifacts（深度不稳、视图相关瑕疵）。现有工作直接用预训练扩散模型做恢复或生成伪视图监督，但扩散模型倾向把渲染瑕疵解释为合理的物体级结构，补全为并不存在的车辆、树木或建筑部件，形成 floater→幻觉→回吸收进高斯的 artifact amplification loop，污染后续位姿与高斯联合优化。
- **方法详解**：整体为 adapter + 冻结扩散骨干 + 置信门控联合优化框架：先用 MASt3R 初始化位姿与深度先验，场景表示为高斯集合 𝒢={(μ,Σ,c,o)}。核心一，轻量 artifact-aware adapter A_θ（带 skip connections 的 encoder-decoder），输入当前渲染图与相邻两参考图 Î_t=A_θ(I_k^ref, I_t^gs, I_{k+1}^ref)；两阶段训练：Stage I 在自建 Gaussian artifact 数据集（1 万余样本，覆盖 floating Gaussians、ghosting、模糊边界、深度畸变）上用像素重建+结构相似度损失预训练；Stage II 级联冻结的 Difix3D 扩散模型 𝒟_φ 仅更新 θ，使中间图与冻结扩散先验兼容。核心二，双向恢复与残差置信融合：按重叠度 C_ab(p)=O_ab(p)·s_d(p)·s_t 选参考帧，融合 Î_t^fix=I_t^gs+W_k⊙R_t^k+W_{k+1}⊙R_t^{k+1}，权重 W_i=C_{t,i}/(C_{t,k}+C_{t,k+1}+ε)，幻觉门控 C_m(p)=½(𝕀_Mk(p)+𝕀_Mk+1(p)) 仅放行有跨视图几何支撑的区域。核心三，表征侧高斯稳定化：深度项 A_i^z=1-Norm(σ_z(i)/v̄_i) 与密度项 A_i^ρ=1-Norm(Σexp(-‖μi-μj‖²/2σρ²)) 合成 artifactness A_i=αA_i^z+(1-α)A_i^ρ，对稀疏弥散高斯软衰减并随机剪枝。位姿经 se(3) Lie 代数更新 T_t←exp(Δξ_t)T_t，配逐视图仿射曝光校正，总损失 ℒ=ℒ_real+λ_pvℒ_pv+λ_dℒ_d+λ_scaleℒ_scale。
- **实验与结果**：三个户外数据集：DL3DV（易，300 帧序列每 30 帧取 1 得 10 个输入视图）、Waymo（中）与 KITTI（难）（各取前 200 帧每 10 帧取 1 得 20 视图，其余帧做测试），平均视图重叠由 0.98 降至约 0.75；指标 PSNR/SSIM/LPIPS 与 ATE RMSE；对比 11 个基线（CF-3DGS、VideoLifter、InstantSplat、LongSplat、RegGS、OpenGS-SLAM、AnySplat、ProSplat、Depth Anything 3、DGGT、S3PO-GS）。全面最优：DL3DV PSNR 21.26→24.27；KITTI PSNR 15.58→17.95、SSIM 0.510→0.605；Waymo PSNR 23.76、SSIM 0.777；ATE RMSE 0.077/1.352/2.471 三数据集最低。消融（Waymo PSNR）：仅扩散 18.16、去 adapter 22.65、去 fusion 22.98、去 RSGS 23.01、完整模型 23.76。实现：PyTorch，单卡 A6000 重建；adapter 用 4×A6000、AdamW、1000 epochs 约 10 小时收敛。
- **创新点与贡献**：['首次识别并形式化 diffusion-guided 稀疏重建中的 artifact amplification loop：3D floater 被渲染为 2D 瑕疵、被扩散补全为幻觉、再作为监督回吸收进高斯场', '提出两阶段训练的 artifact-aware adapter：Stage I 在自建 Gaussian artifact 数据集预训练，Stage II 与冻结扩散骨干联合调优，保留预训练扩散恢复能力的同时只适配任务特定的 conditioning interface', '提出双向残差置信融合与幻觉门控：伪视图像素只有获得双向跨视图对应支撑才允许参与监督，从像素级阻止无依据生成内容进入优化', '提出表征侧高斯稳定化（RSGS）：以深度一致性与局部密度弥散度构造 artifactness 分数，对持久 floater 源做软衰减与随机剪枝，与图像空间门控互补', '构建含 1 万余样本的 Gaussian artifact 数据集，涵盖稀疏重建典型瑕疵类型']
- **局限与风险**：论文明示局限：视图重叠极低或大面积无纹理时，跨视图证据不足以验证所有恢复区域，置信融合失效；adapter 虽在多样瑕疵上训练，对未见重建误差的泛化仍有限；当前公式化仅假设静态场景。客观不足：评测限于户外驾驶类场景，未覆盖室内或动态场景；仍属逐场景优化范式，每轮需渲染加扩散恢复，训练与显存开销大；依赖 MASt3R 初始化，初始化失败场景未讨论；未承诺代码与数据集开源，复现依赖自建 artifact 数据集。
- **与文献库的关系**：backfill 论文，位于 unposed sparse-view 3DGS 与 diffusion prior 两条技术线的交汇点。位姿侧承接 CF-3DGS（COLMAP-free）、InstantSplat（DUSt3R 初始化）、LongSplat（MASt3R/VGGT）及同组前作 RegGS（ICCV 2025）、OpenGS-SLAM/S3PO-GS 的免 COLMAP 联合优化路线；生成先验侧承接 Difix3D+、3DGS-Enhancer、ViewCrafter、SGD、GaussianScenes 的扩散伪监督思路，但区别于这些工作直接采信生成内容，本文核心贡献在门控而非生成本身。与 AnySplat、ProSplat、Depth Anything 3、DGGT 等 feed-forward 路线互为对照，代表 per-scene 优化系在稀疏无位姿户外场景下的演进。
- **可复现性**：原文未承诺代码或数据集开源，未给出仓库链接。实现细节披露较完整：PyTorch，重建用单卡 NVIDIA A6000；adapter 训练用 4×A6000（AdamW、cosine 学习率、1000 epochs、约 10 小时）；扩散骨干为公开预训练的 Difix3D，位姿初始化用 MASt3R；自建 Gaussian artifact 数据集（1 万余样本）未承诺公开，硬件配置已披露。
- **行动建议**：户外稀疏无位姿 3DGS 重建的幻觉抑制基线：DL3DV/Waymo/KITTI PSNR 24.27/23.76/17.95 与 ATE RMSE 0.077/1.352/2.471，11 基线全面最优；其「artifact amplification loop」形式化与双向置信融合门控可迁移至任何扩散先验重建管线；仅户外驾驶类场景验证（未覆盖室内/动态）、逐场景优化开销大、无代码无数据（自建 1 万余样本 artifact 数据集未公开）是复现门槛。

## 四、当日全量 7 维度对比表（参考）

见 [`papers/daily/backfill-1103/7dim-table.md`](../papers/daily/backfill-1103/7dim-table.md)。

## 五、覆盖率校验与筛选过程说明

- 门①（同质去重）：全池合并复核最大 Jaccard 0.116 < 0.62，通过，无同质重复。
- 门②（赛道覆盖）：覆盖 2 赛道（感知与认知 / 重建与SLAM），2 篇低量批次实际上限。
- 门③（价值天花板）：对 backfill 不适用；本批 2 篇均未达 S 线（最高 DiTGaze 3.72），按实数定级，未拔高。
- OUTDATED/SUPERSEDED 0 篇。


## 六、附录：证据等级分布与抓取记录

- FULL 2 篇；PARTIAL 0 篇；ABSTRACT_ONLY 0 篇。
- 抓取降级：2610.41680 L1/PARTIAL（arXiv HTML 404 + ar5iv 仅摘要页 5,660 字符，按摘要级评估并显式声明，未脑补正文细节）；其余 12 篇 L0/FULL。无 L5、无 OCR、无伪造；串行 3s/篇，无限流。
