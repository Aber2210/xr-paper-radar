# -*- coding: utf-8 -*-
"""生成 data/digest_1119_g4.json（2026-11-19 第 4 组，5 篇全文精读）。

数据来源：data/fulltext/<id>.txt（HTML 全文，EVIDENCE=FULL）
评分权重沿用 scripts/build_1007.py：
IMP .20 / NOV .20 / TEC .15 / EXP .15 / PER .15 / TRL .08 / REP .07
"""
import json
import os

W = dict(IMP=0.20, NOV=0.20, TEC=0.15, EXP=0.15, PER=0.15, TRL=0.08, REP=0.07)

D = {}

D["2611.22805"] = {
    "id": "2611.22805",
    "title_en": "DOOM-GS: Dynamic Out-of-core Optimization for Massive Gaussian Splatting",
    "title_zh": "DOOM-GS：面向海量高斯泼溅的动态外存优化",
    "track": "神经渲染",
    "problem": "3DGS 训练默认所有 primitives 常驻 GPU，城市级场景的 primitive 数量远超显存容量。现有 out-of-core 训练（CLM-GS、TideGS、A LoD of Gaussians）只处理静态场景，其两条隐含前提在动态场景失效：一是“空间邻近的 Gaussian 始终一起访问”，但动态 Gaussian 会移动且只在有限时间区间活跃，静态空间分组随时间丧失局部性；二是“单视图可见 primitive 能放进显存以便排序与 alpha 混合”，而大场景单视图可见量本身就可能超显存。因此需要一套面向时空 primitives 的外存训练与渲染机制，并缺少相应的大规模动态评测数据。",
    "method": "沿用 GraphiXS 的显式时空高斯：每个组件含均值/协方差/opacity/SH，外加时间中心 g_i、时长 u_i 与 v/a/j/s 四阶运动系数，opacity 随时间按高斯衰减。SSD 上以 B=4096 定长 block 存储（59 个静态 + 14 个动态参数），CPU 作 cache，只把当前 batch 可见 block 载入 GPU。时空块剔除由 κ=sqrt(-2lnε) 得每个 Gaussian 的活跃半宽 δ_i、由最大位移 ρ_i 扩张包围球半径 R_k、并由 g_i 与 Δ_k 得块时间支撑 S_k，块仅当时间活跃且视锥可见时进入 working set K(C)。训练中在线维护块布局：cloning 按 3D 位置梯度与 opacity 的组合分数采样并沿用 3DGS-MCMC 分裂；relocation 把不活跃槽位（opacity<0.005，或 <0.01 且 2000 iter 无位置梯度）复用给新目标，带 Morton cell 与“一个中位块直径”局部性约束，每步最多迁移 5%；每 2000 iter 做一次 4D Morton repacking，长寿命 Gaussian 用空间 Morton、其余按时长分四类。相机调度用视锥占用体素的 Jaccard 相似度做全局贪心：每 pass 每相机只选一次，再取最少使用且时间最近的帧，以提升 block 复用并保持视角/时间多样性。渲染改用 sort-free 的 Gaussian Point Splatting 并给出可学习梯度估计：把期望颜色按 Gaussian i 之前/自身/之后三段拆分，推出 ∂L/∂sh=o_iT_ig 与 ∂L/∂o=T_ig(sh_i-c̄^b_i)，其中“i 之后的期望颜色” c̄^b_i 用 framebuffer 中第二近点的颜色 c_2(q) 做无偏估计。流式训练把 working set 切 chunk：前向逐 chunk 渲入每相机独立 framebuffer，反向重放同批采样点并与所有相机 framebuffer 对齐累加梯度，使峰值显存与单视图可见 Gaussian 数解耦。实验在 20M Gaussian、4 图 batch、1800 block（约 7.4M Gaussian）预算下训练，Corner/Block 40K iter、District 200K iter。",
    "key_results": [
        "DynamicMatrixCity 原生动态对比（同一 GraphiXS 表征、同一初始化）：PSNR Corner 24.93 vs Dynamic TideGS 15.60（+9.3 dB）、Block 23.19 vs 9.28（+13.9 dB）、District 19.35 vs 10.19（+9.2 dB）。",
        "SSIM Block 由 0.344 升至 0.721、District 由 0.286 升至 0.658；LPIPS Corner 由 0.570 降至 0.293；GPU hit rate Block 78%→89%。",
        "训练时间相对 Dynamic TideGS 降低 46%（Corner）、31%（Block）、28%（District）；District 峰值显存 20.5→12.6 GB，Block 18.9→16.8 GB。",
        "与逐帧静态基线（Corner/Block，120 帧各训 2.5M 模型，合计 300M）相比，单一 2.5M 动态模型在 Block 上 PSNR 高 1.3 dB（对最强逐帧基线）、高 3.5 dB（对 TideGS），Gaussian 数少 120 倍；Corner 上 CLM-GS 的 PSNR 反而高 0.37 dB，但本文 SSIM/LPIPS 更优。",
        "时间一致性：flicker 相对最稳定基线降低 7.1 倍（Corner，2.79 vs 19.84）与 6.3 倍（Block，2.89 vs 18.24）。",
        "消融（20M）：去 space-time repacking 的 PSNR 变化 ≤0.28 dB，但 hit rate 降 31-38 点、训练时间增 1.7-6.7 倍；去局部性约束 relocation 的 hit rate 降 24-28 点；换随机 batch 调度 PSNR 降 0.95 dB（Corner）/0.37 dB（Block），时间增 2.1-7.7 倍。",
    ],
    "novelty": "首个面向大规模动态场景的 out-of-core GS 训练框架，把外存范式的组织单位从“空间块”改为“时空块”，并配套 4D Morton 重排与保局部性的槽位复用。把原本只能前向的 Gaussian Point Splatting 扩成可学习模型，用第二近点 framebuffer 估计被遮挡背景色从而绕开深度排序，使单视图 primitive 数不再受显存约束。同时贡献 DynamicMatrixCity 城市级动态多视数据集，填补“大规模 + 动态 + 稠密多视”三者兼具的评测空缺。",
    "limitations": "方法绑定显式运动表征（四阶多项式 + 有限时间支撑），无法直接支持 implicit deformation 类动态表示。完整模型必须常驻 SSD，作者明确指出极端规模下存储开销会显著上升。评测只在自行合成的 DynamicMatrixCity（MatrixCity 加程序化行人车辆）上进行，无真实采集；对比基线是把 GraphiXS 表征塞进 TideGS 的自行改造版本，并非原生动态外存方法，增益幅度存在被放大的风险。",
    "code": "none",
    "venue": "arXiv preprint（arXiv:2611.22805v1 [cs.GR]，2026-11-17，CC BY 4.0）",
    "evidence": "FULL",
    "scores_hint": {"IMP": 3, "NOV": 4, "TEC": 4, "EXP": 3, "PER": 4, "TRL": 3, "REP": 2},
    "scores_why": "IMP=3：解决城市级动态 GS 的显存与训练瓶颈，是大规模 XR 场景内容生产的重要使能项，但不直接触及头显实时渲染与跟踪。NOV=4：首个动态 out-of-core GS 框架，时空块组织、4D Morton 重排与可学习 point splatting 梯度估计共同构成新架构。TEC=4：分块剔除、调度、流式反传均有完整推导并配三场景消融，但只有单一合成数据集与自改造基线。EXP=3：仅 DynamicMatrixCity 三个合成场景，无真实采集、无用户实验。PER=4：PSNR 提升 9.2-13.9 dB、flicker 降 6-7 倍，但基线为自行改造的 Dynamic TideGS，绝对增益需打折看待。TRL=3：单张 24GB 卡可训 city-scale，属实验室原型，且未提供运行时流式渲染方案。REP=2：无代码/数据链接，数据集与超参仅见正文。",
}

D["2611.22829"] = {
    "id": "2611.22829",
    "title_en": "Kolibri: Color Finds the Place, Refinement Sets the Pose for RGB-D Localization in Colored Point Clouds",
    "title_zh": "Kolibri：颜色找位置、精化定姿态——彩色点云中的 RGB-D 定位",
    "track": "重建与SLAM",
    "problem": "机器人在已扫描建筑内需要把相机定位到训练时从未见过的房间，参考数据是预先已知的彩色度量点云。点云配准方法（GeDi、BUFFER-X 等）能把每帧 RGB-D 对齐到点云，但代价极高：单房间内 BUFFER-X 中位 1.4 s/帧、GeDi 24 s/帧，整栋搜索要按房间或立方体重跑一遍。用图像检索先选房间虽能缩小搜索，但选错房间在姿态估计开始前就丢帧——100 个 ScanNet 房间中检索仅 28.6% 把真房间排第一。因此需要一种既保持配准精度、又能支撑无房间标签全库搜索的低成本定位方案。",
    "method": "核心思路是把 RGB-D 重定位拆成“找位置（学习）”与“定姿态（几何）”两段，并先用实验证明拆分的可行性：在真实 ScanNet 帧上测得 refinement basin 边界为初始位置误差 7.7 cm（成功率降到一半），basin 内 99% 的帧成败与初值无关，因此学习模块只需把候选送进 basin。具体做法是把 frame 深度反投影点与参考点云都池化为 10 cm 立方 cell，每 cell 存点均值位置与颜色，以 k=16 近邻建图，法向取邻居偏移协方差最小特征值方向。逐 cell 输入 8 维特征（中灰居中颜色、log 边长均值与方差、linearity/planarity/scattering），边特征为 log 长度与“偏移-法向”“法向-法向”的绝对余弦，用绝对值消除法向朝向敏感。一层 message passing（EdgeConv 式逐特征 max 聚合，width 128，GELU + LayerNorm）输出 32 维单位描述符，全网络仅 55,712 参数；点云描述符离线算一次并可复用。匹配阶段每个 frame cell 取 top-5 相似点云 cell，τ=0.1 的 softmax 作权重；用 SC²-PCR 的距离一致性（ρ=25 cm）为 256 个 match 各种子 consensus set，加权刚体拟合得候选；为对抗重复家具造成的错误一致群，保留 4 个互相间隔 ≥0.5 m 或 10° 的候选、剔除被已选位姿解释（残差 <0.5 m）的 match 后再做 2 轮补充，最多 6 个候选。每个候选跑 point-to-plane ICP（1000 个均匀采样点、10 iter、对应半径 20→5 cm），以 3 cm 内点数作 fit score 选最终位姿。可选 Precise 用 Tukey 加权二级精化（+35 ms/+4.0 点），color pass 对通道做共享仿射把亮度均值与方差对齐点云后重跑全流程，按 fit score 择优。训练用 170 个房间（165 ScanNet + 5 校园空间）的渲染视角，加随距离平方增长的深度噪声、尺度/亮度/对比/白平衡扰动与缺失扇区，正样本为 0.5 m 内最近点云 cell，softmax 交叉熵，AdamW lr=1e-3、18,600 步 ×8 视图，RTX 4090 上 ≤53 分钟。",
    "key_results": [
        "ScanNet-96（96 房间 / 7,986 帧，房间已知，5 cm & 5°）：Fast 81.4%±1.8 vs GeDi 80.3%±1.9（统计等价），BUFFER-X 69.4%、RGB GeoTransformer 77.8%、ColorPCR 80.3%、PREDATOR 49.6%、FPFH+TEASER++ 33.2%。",
        "效率（RTX 2080 Ti，200 帧中位数）：82 ms/帧、1.44 GB，BUFFER-X 1,416 ms（约 18 倍）、GeDi 24,149 ms、RGB GeoTransformer 2,501 ms。",
        "无房间标签搜索：100 房间合成点云（15.0 M 点）达 79.9%，仅比给定真值房间低 1.3 点；单候选时降到 46.2%；Retrieve-1+Fast 仅 23.9%（相对全库搜索 -56.0 点）。",
        "医院急诊科真实手持激光扫描（49 m × 42 m，440 帧渲染）：86.5%±0.7 @ 5 cm & 5°，384 ms/帧；GeDi 整云 26.7%、1,090 个 3 m cube 76.7% 但需 91 分钟/帧（Fast 与 GeDi-cube 差异统计上不确定，+7.8 点 [-7.8,+23.4]）。",
        "消融（ScanNet-10 消融房间 + 7-Scenes，Precise）：去 message passing 降 13.4/13.4 点，去颜色降 26.2/26.2 点，只留颜色降 3.4/3.4 点；参数量从 4,736 到 915,584 变化时 recall 波动 ≤1.0 点；22 房间训练与 170 房间等价。",
        "失效边界：灰度帧上 RGB GeoTransformer 领先 47.2 点（0.25 m & 2°）；Bonn 跨相机（ASUS Xtion 帧 vs 地面激光扫描着色）Fast 仅 26.3%，加 color pass 47.2%，而 GeDi-cube 91.5%（11 分钟/帧）。",
    ],
    "novelty": "把 RGB-D 重定位显式分解为 place-finding 与 pose-refinement，并用 basin 宽度实测把“学习部分可以极小”从直觉变成可检验命题：55.7K 参数即可在匹配精化下追平 3.11M 参数的 GeDi。配套的“多候选 + 几何 fit score + 全库联合搜索”避免了两阶段检索的错误传播，使百房间/整栋无标签搜索在百毫秒级可行。相对既有工作，这是问题形式化与系统设计的双重创新，而非单纯换描述符。",
    "limitations": "强依赖 frame 与点云颜色一致（仅容忍亮度/对比度的仿射变化），灰度输入或跨相机色响应差异下明显失效，此时点云配准方法仍领先。refinement basin 仅 7.7 cm，最优候选落在 basin 外时需靠其他候选挽救（51% 的帧），再差就整帧失败。只在房间尺度室内场景验证，作者指出扩展到整栋需要“不丢弃正确位置”的层级化搜索结构。正文未报告训练/推理代码或数据发布。",
    "code": "none",
    "venue": "arXiv preprint（arXiv:2611.22829v1 [cs.CV]，2026-11-17，CC BY 4.0）",
    "evidence": "FULL",
    "scores_hint": {"IMP": 4, "NOV": 4, "TEC": 4, "EXP": 4, "PER": 4, "TRL": 3, "REP": 3},
    "scores_why": "IMP=4：建筑尺度已知点云重定位是 AR/VR 室内导航与持久化地图的高频刚需，82 ms 级延迟可直接进入 XR 运行时预算。NOV=4：把重定位拆成 place-finding 与 pose-refinement，并用实测 basin 宽度支撑“学习模块可极小”的命题，属问题形式化层面的创新。TEC=4：含 walk bootstrap 统计协议、等价/领先判据、组件与规模消融及详尽附录，唯缺代码。EXP=4：ScanNet-96/96-S2、7-Scenes、12-Scenes、一次性 held-out 与真实医院扫描多套评测，但医院帧为扫描渲染而非真实 RGB-D 采集。PER=4：精度与 GeDi 持平（81.4 vs 80.3），成本低 18-300 倍，综合效能显著领先。TRL=3：RTX 2080 Ti 上 82 ms 可跑，仍是学术原型且未开源。REP=3：训练/评测细节与附录极完整，但无代码与数据发布。",
}

D["2611.23051"] = {
    "id": "2611.23051",
    "title_en": "Refin3R: Geometry-Guided Refinement for Feed-Forward 3D Reconstruction",
    "title_zh": "Refin3R：面向前馈三维重建的几何引导精化",
    "track": "重建与SLAM",
    "problem": "前馈重建模型（DA3、Pi3X、VGGT 等）一次前向即为所有视图输出稠密 point map，速度快、可扩展，但完全由学习先验回归、没有三角化等显式几何约束，导致跨视图不一致且局部精度不足。SfM 有显式多视约束、点准但稀疏，在宽基线/低重叠下脆弱。已有结合方式各有缺陷：几何条件化模型只把位姿/深度当辅助输入，depth completion 逐视图独立处理，GGPT 虽在 3D 空间联合精化，但只精化 SfM 覆盖到的局部立方块，纹理缺失面与单视图可见区域几乎得不到改善。",
    "method": "输入两路互补重建：冻结的多视前馈 backbone（DA3 或 Pi3X）给出相机与稠密深度 D^ff；GGPT 的 SfM 管线（RoMa v2 匹配 + sparse bundle adjustment + 多视 DLT 三角化）给出部分深度 D^sfm 与有效掩码 M。两者统一表示为沿像素射线的深度并取对数 ζ=log D 以压缩动态范围；每像素几何通道为 [r_i, ζ^ff, ζ^sfm, ζ^sfm-ζ^ff, M]，其中显式给出两路重建的差值。从 backbone 四个中间层取 image token，经端到端训练的 DPT head 融合并上采样成图像分辨率几何感知特征 F。2D 分支是 ConvNeXt block 构成的 6 尺度 U-Net，输入逐像素几何通道拼接 F，预测 log-depth 残差与 confidence logit，输出 ζ^2D=ζ^ff+Δζ^2D，把 SfM 深度沿图像传播到无三角化像素。3D 分支按 MoGe-3 在每个视图的“图像坐标 + log 深度”上建体素网格，把所有视图的 SfM 点体素化进去（仅保留位于相机前方且投影落在图像内的点），用 5 级 residual sparse 3D convolution 的 U-Net 聚合 3D 邻域，逐占用体素预测残差与 confidence，并只在 own voxel（本视图三角化点）读出，因而能引入被本视图遮挡、仅由其他视图三角化的点。两分支在 stride 8 与 16 两个尺度、特征宽度相同时做双向交互：Inject 把像素处图像特征广播给该 pixel column 的所有体素（MLP 融合），Gather 把该列的 own voxel 特征沿深度平均池化、LayerNorm 后以残差加回图像特征（只用 own voxel，排除仅由他视图构成的体素）。Spatial fusion 用动态 SPN 在 linear depth 上迭代 6 轮：SfM 观测像素上以 confidence β 把 D^sfm 与 D^3D 混成 anchor a_i，2D 分支的第二个 decoder 预测 K=5 邻居的 affinity、offset 与 anchoring weight η，最终 D^pred=D^(6) 用 SfM 相机反投影为 point map。损失为 confidence-weighted L1（c=1+exp(ĉ)≥1，α=0.2）监督最终深度与 2D 分支，3D 分支只在 own SfM 像素用纯 L1。训练 200K iter、4×A6000、AdamW lr=1e-4，数据为 ScanNet++/TartanAir v2/UnrealStereo4K/BlendedMVS，按 covisibility 约束随机游走采 3-16 视图。",
    "key_results": [
        "ScanNet++（域内，AUC@1 cm %）：4/8/16 视图 33.7/39.6/45.2（Pi3X 版）vs GGPT 25.6/29.5/34.8；DA3 版 31.5/37.5/43.4 vs GGPT-DA3 21.6/27.4/31.8。",
        "ETH3D（跨域）：16 视图 AUC@1 cm 53.3（Pi3X）/53.6（DA3）vs GGPT 39.4/32.6；AUC@5 cm 76.4 vs 69.1。",
        "Tanks&Temples 4 视图 AUC@1 cm 17.1（Pi3X）/15.6（DA3）vs GGPT 16.1/14.9；域外 4D-DRESS @1 cm 80.2 vs GGPT-Pi3X 64.6、VGGT-Ω 42.0；MV-dVRK @1 mm 72.3（DA3）vs GGPT-DA3 67.0。",
        "效率（ETH3D，RTX A6000，16 视图）：0.86 s/5.1 GB vs GGPT 12.92 s（约 15 倍）/6.2 GB、Pi3X 1.88 s、Any2Full 3.17 s；含 DA3 encoder 时 1.58 s。",
        "消融（ScanNet++ / ETH3D 平均，AUC@1/@5）：DA3 1.0/6.9、GGPT 27.0/55.5 → 仅几何 2D 分支 34.3/64.7（ETH3D 42.8/67.4）→ 加图像特征 35.4/66.3 → 加 3D 分支与交互 36.7/67.2 → 加 spatial fusion 37.5/67.8（ETH3D 47.6/71.1）。",
    ],
    "novelty": "把几何引导精化从“3D 点 patch”搬到“图像网格上的 per-view depth”，从而能借用前馈 backbone 的稠密语义/几何特征，把 SfM 几何外推到其覆盖之外（弱纹理面、单视图区域）。用稀疏体素聚合所有视图的 SfM 点，并通过 pixel-column 的 Inject/Gather 双向交互与 2D 分支在同一坐标系对齐，最后用 SPN 把 3D 证据 anchor 后空间传播，形成“稠密先验 + 多视证据 + 自适应融合”的新架构，而非在 GGPT 上调参。",
    "limitations": "依赖 SfM 前端（RoMa v2 匹配 + BA + 三角化），其失败与外点会直接传入，宽基线/低重叠场景的上限仍受前端约束。相机参数固定不优化，精度上限被冻结 backbone 与 SfM 相机限制。效率表只计方法本身，不含 SfM 前端时间（正文明确说明各方法共享同一 SfM 输出），因此端到端延迟远高于 0.86 s，仍是离线多视图管线。正文未给出失败案例统计与逐场景最差表现。",
    "code": "https://cvlab-kaist.github.io/Refin3R（正文声明的项目页；代码未声明发布）",
    "venue": "arXiv preprint（arXiv:2611.23051v1 [cs.CV]，2026-11-17，CC BY 4.0）",
    "evidence": "FULL",
    "scores_hint": {"IMP": 3, "NOV": 4, "TEC": 4, "EXP": 4, "PER": 4, "TRL": 3, "REP": 3},
    "scores_why": "IMP=3：稠密 point map 精度对 MR 场景网格化与空间理解有直接价值，但管线依赖 SfM、非实时，属间接支撑而非 XR 卡脖子环节。NOV=4：将精化域从 3D 点 patch 改为图像网格 per-view depth，并用 pixel-column 双向交互接稀疏体素多视证据，是明确的新架构。TEC=4：双分支、双向交互、SPN 融合与三项损失齐备，五个数据集 + 逐组件消融 + 效率对比。EXP=4：ScanNet++/ETH3D/T&T 三个标准集各三种视图数，另加 4D-DRESS 与 MV-dVRK 域外评测，但无真机/在线验证。PER=4：AUC@1 cm 相对 GGPT 提升 24-35%（ScanNet++ 25.6→33.7、ETH3D 39.4→53.3）。TRL=3：0.86 s/16 视图且不含 SfM 时间，属实验室管线。REP=3：有项目页与完整训练配置，代码未声明发布。",
}

D["2611.23054"] = {
    "id": "2611.23054",
    "title_en": "ReTouchGS: Ultralight Render-free Aesthetic Color Enhancement and Transfer for 3D Gaussian Splatting",
    "title_zh": "ReTouchGS：面向 3D 高斯泼溅的超轻量免渲染美学调色与迁移",
    "track": "神经渲染",
    "problem": "现有 3DGS 颜色迁移与交互编辑都由参考图或用户显式指定的色彩调整驱动，但很多创作场景只想要“自动变得更好看”且跨视角色彩一致。把 2D 图像自适应增强逐视图套用会产生视角间不一致；把非线性颜色变换直接作用到每个 Gaussian 又与 alpha 混合不可交换，导致像素颜色与目标不符；基于渲染的逐场景优化（BilaRF、SAAD）即使只调颜色也要反复渲染，代价高昂。这一“无参考的美学增强”任务此前无人处理，也缺少带场景一致目标的三维评测基准。",
    "method": "整体把“决定场景颜色”与“在 Gaussian 参数上实现该决定”解耦：输入已训练 3DGS 资产与相机参数，先得到一个场景级颜色算子 T（默认 17³ grid LUT，Θ 存相对 identity 的位移，三线性插值 + 截断），再把它烘焙进 SH 颜色，输出仍是标准 3DGS 资产，几何与 opacity 完全不动。参考无关增强网络 E_φ 把 Gaussian 中心投影到粗图像网格，编码视图相关 SH 颜色、opacity、相对尺度并按 opacity 与深度加权池化，CNN encoder 汇总空间特征，RGB 与 luma 分位数描述色彩/色调分布，逐视角融合后 mean pool 成单一场景描述符；由于专家 LUT 高度相关，对训练 LUT 做 PCA，网络只回归标准化系数再按 μ+B(σ⊙z) 重建 LUT。参考引导迁移则渲染一次参考视角原图，用带 identity-centered ridge 惩罚的拟合求 grid LUT（14,739 个值），使单一编辑视角可定义场景级映射。为实现免渲染更新，先用 blended color context m_i（在粗投影网格上按 opacity/soft depth 池化 SH 颜色再聚合到该 Gaussian 投影处）对 T 做一阶展开，权重 a_i=exp(-||c_i-m_i||²/δ²) 在“context 处展开”与“自身颜色处展开”间过渡，同时用局部 Jacobian 变换高阶 SH 系数使视图相关变化跟随同一调整。残余的算子曲率与混合偏差由 44.7K 参数的 blend-aware 网络修正：在 3D 最近邻图上做两层 residual propagation，输入三类算子残差（direct、context、Jacobian）与 blending discrepancy b_T(a,b)=T((a+b)/2)-(T(a)+T(b))/2（节点用 b_T(u_i,m_i)，边用 b_T(u_i,u_j)），预测三通道共享的标量传播系数，输出 DC 修正 d_θ,i；identity 算子下所有残差为 0，构造上保持原色。训练分三段：美学网络 20K 步；refinement 先用渲染式 color solver 蒸馏 DC 目标 16K 步，再用渲染微调 12K 步并以 λ_corr 把学习修正拉回解析初值。基准 ReTouch3D 用 NamedCurves(MIT5K-DPE) 在重建视角生成增强图后联合拟合单一场景级 LUT 作为一致目标，28 个 DL3DV + 9 个 Mip-NeRF 360 场景，主指标为每场景 16 个 off-trajectory 视角的 ΔE76。",
    "key_results": [
        "美学增强（37 场景平均）：ΔE76 5.50 vs BilaRF 6.30、SAAD 6.18、ReparamGS 11.65；PSNR 28.08 vs 27.05；LPIPS 0.0561；耗时 22.97 s vs BilaRF 122.54 s、SAAD 3,461.78 s；网络参数 180.2K vs 0.99M 以上。",
        "参考引导迁移：ΔE76 4.03 vs BilaRF 5.73、SAAD 15.46、ReparamGS 11.44；PSNR 29.49 vs 27.87；19.32 s，网络仅 44.72K 参数。",
        "换用 VeraRetouch 目标（refinement 权重冻结、只重训美学网络或重拟合 LUT）：增强 ΔE76 5.13 vs BilaRF 6.03，迁移 3.08 vs 4.52，PSNR/SSIM 亦最优。",
        "视角泛化：参考视角 3.81 ΔE76、held-out 视角 3.85（37 场景平均），off-trajectory 差距很小。",
        "消融（增强/迁移 ΔE76）：去 blended context 与 refinement 6.417/5.299 → 去 refinement 5.911/4.649 → 去 residual propagation 5.594/4.189 → 去 blending discrepancy 5.563/4.147 → 完整 5.502/4.035。",
        "交付时间（含资产加载、编辑、导出）：DL3DV 5.6 s、Mip-NeRF 360 32.8 s（中位，RTX 5090）。",
    ],
    "novelty": "首个面向已训练 3DGS 资产的 reference-free 美学色彩增强框架，并同时支持参考引导迁移，两者共享同一 LUT 表征与同一免渲染更新阶段。关键洞见是把非线性算子与 alpha 混合的不可交换性显式建模为 blending discrepancy 特征，再配合解析一阶更新 + 极轻量残差传播，使网络只需 44.7K 参数即可完成原本需要逐场景渲染优化的任务。同时贡献 ReTouch3D：用联合拟合的场景级 LUT 生成视角一致目标，并首次在 off-trajectory 视角上评颜色保真与跨视角泛化。",
    "limitations": "只支持场景级全局颜色映射，无法做局部/逐物体或空间变化的编辑（正文把算子定义为跨视角共享的单一 LUT）。几何与 opacity 固定，不处理光照、材质或几何改动，属于纯后处理式调色。输入视角几乎未覆盖的 Gaussian 误差明显偏高：Table 13 中未观测区域 ΔE76 为 6.30（DL3DV 增强）与 4.62（Mip-NeRF 迁移），高于整体 5.50/4.03。参考迁移只用单个 edited view 拟合，颜色覆盖不足处依赖 ridge 锚回 identity，可能压制合理的大幅调整。",
    "code": "none",
    "venue": "arXiv preprint（arXiv:2611.23054v1 [cs.CV]，2026-11-17，CC BY-SA 4.0）",
    "evidence": "FULL",
    "scores_hint": {"IMP": 3, "NOV": 4, "TEC": 4, "EXP": 4, "PER": 3, "TRL": 3, "REP": 2},
    "scores_why": "IMP=3：3DGS 资产的美学调色是 XR 内容生产链上的实用工具，但不影响跟踪、渲染性能等核心环节。NOV=4：首个 reference-free 的 3DGS 美学增强，并用 blending discrepancy 显式处理非线性算子与 alpha 混合的不可交换性，配套 ReTouch3D 基准。TEC=4：算子预测/拟合、解析更新、44.7K 精化网络与三段训练完整，含组件消融与跨 LUT 源迁移实验。EXP=4：37 场景、8 个基线、两套目标（NamedCurves 与 VeraRetouch）与 off-trajectory 评测，但无用户主观实验。PER=3：迁移 ΔE76 相对最优基线降约 30%，美学增强仅 5.50 vs 6.18（约 11%），质量增益偏小，主要优势在 5 倍以上速度与 20 倍参数缩减。TRL=3：输出标准 3DGS、秒级交付，接近可用工具，但未开源。REP=2：无代码与基准下载链接，复现依赖附录细节。",
}

D["2611.23187"] = {
    "id": "2611.23187",
    "title_en": "Any2Building: Unifying Point Clouds and Images for Building Reconstruction via Shared Spatial Queries",
    "title_zh": "Any2Building：以共享空间查询统一点云与图像的建筑物重建",
    "track": "重建与SLAM",
    "problem": "LoD2 建筑重建的观测天然异质：部分点云给出不完整的 3D 表面测量，正射影像给出 footprint、屋面布局与屋顶构筑物的视觉线索但高度与遮挡面不确定。然而点云补全与图像生成长期被当作两个任务，现有方法都绑定单一观测设定：BuildAnyPoint 的体素对齐条件不便接入图像，SatSkylines 的噪声空间注入难以扩展到点云且会模糊细节，通用生成器（Axolotl3D、Hunyuan3D-Omni）直接拼接视觉与几何 token，把跨模态结构对齐和缺失几何推断都丢给生成器。缺的是一个把异质观测与完整建筑结构在 3D 上对齐的共享表示，从而支持任一模态或组合，并产生跨任务正迁移。",
    "method": "在 16³ 低分辨率 3D 网格上放 N=16³ 个 shared spatial queries，所有输入、查询与输出 64³ 体素共用一个归一化建筑坐标系，该坐标系与地理参考正射影像绑定，因此纯影像模式下结果也能反算回真实位置。tokenizer 分模态：点云用 4 级 EdgeConv（16 近邻）加 FPS 采样 2048→1024 中心，位置与局部特征经两个 MLP 相加得 1024×1024 token；影像用冻结 DINOv3 的 patch token；LoD0（三维 bbox）或 LoD1（footprint 按高度拉伸）先验体素化成 64³ 表面占用网格（内部留空），对每个对应 16³ cell 的 4³ block 计算表面占用存在 s_j、边界存在 b_j、占用率 ρ_j，经 MLP 编码。query 由位置编码与全局描述符（各模态均值池化特征 + availability flag，缺失模态补零）初始化；有先验时再以 s_j 与 φ_R(r_j) 做残差更新，且保留全部 query 位置以便生成超出先验占用的结构，训练时用 prior dropout 降低依赖。查询通过 cross-attention 分别读点/图 token，缺失模态读出为零，再拼接 availability flag 经 MLP 与 self-attention 得 Q。关键监督是占用辅助头：把完整建筑的 64³ 参考网格 max-pool 到 16³ 作为 target，用 BCE 监督 Q 的表面占用，迫使 query 在生成前就编码含未观测区的整体结构（该损失只监督 Q，不监督最终体素）。Q 以两条路径进入生成器：QE token（H_QE=H+Attn_back(LN(H),Q,Q)，点图双模时先用图 token 与 512 个可学习补全 query 更新点 token）与 spatial prompt（在选定 DiT block 上按同一 grid index 加零初始化线性投影的残差 h_ℓ←h_ℓ+βP_ℓ(LN(Q))）。主干是 flow-matching DiT，生成 16³ structure latent，速度目标 u_t=(1-σ_min)ε-x_0，损失为 flow MSE 加 λ_occ L_occ 与 λ_geo L_geo（把 x_t 按式 9 系数估回 x̂_0、解码成体素后做 BCE+Dice）。训练等概率采样 (P)、(I)、(P,I)、(I,R) 四种模式，共享 conditioner、generator 与同一完整建筑 target，QE token 与 spatial prompt 联合 dropout 以支持 CFG。LoD2 构建阶段：structure decoder 出 64³ 体素，在占用坐标 Ω 上运行去掉图像条件的 surface latent 生成器（作者发现仅凭预测体素已足够，额外点云条件反而降精度），再用 RoLoPM 做 low-poly remeshing；纹理用 ControlNet 依未贴图渲染与从影像/城市名推断的外观描述合成 facade 参考，再由预训练 texture generator 贴图。",
    "key_results": [
        "Building-PCC：点云 F-score 96.12%、CD 0.20、EMD 0.07（BuildAnyPoint 91.38%/0.35/0.10）；low-poly F-score 94.27% vs 80.14%，CD 0.30 vs 0.66，顶点/面数比偏差 e_V=0.08、e_F=0.07（BuildAnyPoint 0.23/0.27）。",
        "BuildingWorld-Image 单模态点云补全：low-poly CD_L1 8.65、F 97.19% vs AdaPoinTr 11.05/92.00%、BuildAnyPoint 12.88/92.00%、UniCo 11.28/91.00%。",
        "多模态补全（更稀疏点云 + 影像）：low-poly CD_L1 26.00、F 77.41% vs MAENet 46.11/52.00%、Hunyuan3D-Omni 44.52/50.00%、EGIInet 44.98/51.00%。",
        "单张正射影像生成：CD_L1 38.90、F 62.82%、PSNR 12.63 dB/SSIM 0.34 vs TRELLIS 54.89/49.20%/10.91/0.26、TRELLIS.2 65.09/31.05%、SAM 3D 55.82/44.34%。",
        "影像 + 粗几何先验：CD_L1 17.23、F 78.64%、PSNR 14.05/SSIM 0.41 vs SatSkylines 33.12/59.62%/11.21/0.28、SpaceControl 34.77/61.93%、Hunyuan3D-Omni 32.46/60.82%。",
        "消融：去占用监督后 I 由 62.82% 降至 54.83%、I+R 由 78.64% 降至 64.03%；去 spatial prompts 时 I+R 降至 57.02%；联合训练比四个单任务 specialist 分别高 1.89/5.44/4.50/1.81 点（P/I/P+I/I+R）；影像增益随点稀疏放大——2048 点 +3.02 点，41 点随机降采样 +25.65 点，裁剪后 41 点 +27.08 点。",
    ],
    "novelty": "用“共享 3D 空间查询 + 完整建筑表面占用监督”把点云补全与图像生成统一成同一条件接口，而不是拼接异构 token 让生成器自己解跨模态关系；占用监督使中间表示在生成前就补全未观测结构，这是区别于 SDFusion/CLAY/Hunyuan3D-Omni 的关键。一个联合训练生成器覆盖四种输入模式并给出正迁移证据；同时贡献约百万级对齐三元组、跨 18 城市的 BuildingWorld-Image；并证明仅凭预测体素即可驱动 surface 生成，省去点/图条件。",
    "limitations": "输出走 64³ 体素 → surface 生成 → RoLoPM 三段式，细节受体素分辨率与 low-poly 简化限制，作者也发现额外点云条件反而降低精度、增加耗时。纯影像模式外观质量仍弱（PSNR 12.63 dB、SSIM 0.34），纹理依赖 ControlNet 合成的 facade 参考而非真实观测。评测以 Building-PCC 与影像-低模配对的 BuildingWorld-Image 为主，遮挡、多屋面层级、建筑群与错误源轮廓在数据构建中被列为需人工复核的难例，真实城市大场景的泛化未验证。",
    "code": "https://henryhoou.github.io/Any2Building/",
    "venue": "arXiv preprint（arXiv:2611.23187v1 [cs.CV]，2026-11-17，CC BY 4.0）",
    "evidence": "FULL",
    "scores_hint": {"IMP": 3, "NOV": 4, "TEC": 4, "EXP": 4, "PER": 4, "TRL": 3, "REP": 3},
    "scores_why": "IMP=3：城市级 LoD2 建模对户外 AR 数字孪生与场景理解有价值，但属内容侧基础设施，不在 XR 跟踪/显示的关键路径上。NOV=4：以共享 3D 空间查询加完整建筑占用监督统一点云补全与图像生成，而非拼接异构 token，并用单一生成器覆盖四种输入模式。TEC=4：tokenizer、query 聚合、双路条件注入、flow-matching 与 LoD2 后处理链路完整，消融覆盖条件设计、联合训练、点退化与 surface 阶段。EXP=4：Building-PCC 与自建 BuildingWorld-Image（2,000 测试建筑）加 Skylines-50K 补充，多任务多基线，但均无实地/真机验证。PER=4：low-poly F-score 80.14→94.27、CD 0.66→0.30，影像生成 CD_L1 54.89→38.90，带先验 32.46→17.23（约 -47%）。TRL=3：8×A800 训练、12 步采样，有项目页但未见代码/数据开放。REP=3：项目页与数据构建、指标、基线适配附录较完整。",
}

out = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data", "digest_1119_g4.json")
with open(out, "w", encoding="utf-8") as f:
    json.dump(D, f, ensure_ascii=False, indent=1)

print("written:", out)
for k, v in D.items():
    s = v["scores_hint"]
    tot = round(sum(W[x] * s[x] for x in W), 2)
    print(k, v["track"], v["evidence"], tot)
