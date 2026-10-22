# XR 论文 Backfill 报告 · backfill-1023

> **批次性质**：补录批次，**非 2026-10-23 当日新提交**。两部分来源：
> ① **10-21 公告批次 listing 漏网 5 篇**（公告日 10-21、提交日 10-15~10-20；10-22 运行已处理该公告批次的主流水，本批补录其摘要级过滤漏网的 XR 相关稿）；
> ② **旧稿 replace/cross 再公告首次入馆 4 篇**（原始投稿周期 2604 / 2607 / 2608，10-23 RSS 拉取混入，经甄别为 XR 相关旧稿）。
> **诚实口径**：全部条目在 registry 中标 `batch=backfill-1023` 与 `orig_window`，7 维表列「来源」区分；绝不混入「当日新论文」叙事。

## 一、执行摘要

- **补录入馆 9 篇**（S×0 / A×1 / B×7 / C×1），registry 588 → **597**；最高 **3.65**（Unfolding 3DGS）。
- 覆盖度：门① 最大 Jaccard **0.075**（2610.28131 vs 库内 2610.08756，<0.62 通过）；全批覆盖 **7 赛道**；门③ 对 backfill 不适用。
- 全文证据：8 篇 L0/FULL（29,750–139,019 字符）+ 1 篇 L1/PARTIAL（2610.28131 OV-Foam，ar5iv 正文缺失，摘要级评估并显式声明）。
- 覆盖补强：3DGS 紧凑渐进渲染 LOD 第三条路线（Unfolding 3DGS，6.5MB→50.7MB vs 601.1MB）、XR 年龄保障新模态（手背图像，无面部生物特征）、光学-感知联合可微设计（编码孔径+3DGS 虚拟环境）、单图仿真就绪场景（SceneRig）、无电子 UMI 采集（$122 头戴相机）、热动力学 4DGS（GTSM）、幂图特征提升（OV-Foam）、360° VIO 基准（Hilti-Trimble-Oxford）。
- OUTDATED/SUPERSEDED **0 篇**（门①通过且无同质取代）。

## 二、排名（按加权降序）

| 排名 | 论文 | 赛道 | 总分 | 等级 | 证据 | 来源 |
|---:|---|---|---:|---|---|---|
| 1 | Unfolding 3DGS：迭代高斯概要实现紧凑渐进渲染 | 神经渲染 | 3.65 | A | FULL | replace 再公告 |
| 2 | 手背图像用于 XR 沉浸式年龄保障与儿童安全 | 感知与认知 | 3.40 | B | FULL | replace 再公告 |
| 3 | 可微任务驱动编码孔径相机设计（3DGS 场景表示） | 渲染与显示 | 3.35 | B | FULL | 10-21 漏网 |
| 4 | SceneRig：单图生成仿真就绪 3D 场景的智能体系统 | 世界模型与仿真 | 3.35 | B | FULL | 10-21 漏网 |
| 5 | WARPED：手腕对齐渲染（第一视角示范→机器人策略） | 内容生成 | 3.30 | B | FULL | replace 再公告 |
| 6 | 单头戴相机标注的无电子 UMI 手套数据采集 | 系统与平台 | 3.23 | B | FULL | 10-21 漏网 |
| 7 | GTSM：热状态空间动力学高斯泼溅（4D 热场重建与预测） | 神经渲染 | 3.17 | B | FULL | 10-21 漏网 |
| 8 | OV-Foam：幂图划分表示下的开放词汇特征提升 | 神经渲染 | 3.12 | B | FULL | 10-21 漏网 |
| 9 | Hilti-Trimble-Oxford：360° 视觉惯性基准（户型图先验） | 评估与数据集 | 2.95 | C | FULL | replace 再公告 |

## 三、逐篇解读（按重要性降序）

### 第 1 章 · Unfolding 3DGS：迭代高斯概要实现紧凑渐进渲染（3.65 A · 神经渲染 · FULL）

# Unfolding 3DGS：迭代高斯概要实现紧凑渐进渲染

## 一句话结论
Unfolding 3DGS 以 top-down unfolding 把 3DGS anchor 结构组织成层次 synopsis：从 6.5MB 概要逐级展开至 50.7MB 最高保真（标准 3DGS 为 601.1MB），在四数据集上各级保持渲染质量，服务带宽/内存受限的实时流式场景。

## 要解决的问题
实时 3DGS 渲染在带宽与内存受限场景（移动 XR、云流式传输）中需要 LOD 与渐进传输，但标准 3DGS 为每个高斯单独存储全部属性，模型体积大（本文实验中基线总大小 601.1MB）；已有压缩/LOD 方法多独立训练各级或缺乏清晰的层次渐进组织，LOD 切换时易出现空间不连续与视觉 popping。如何从单一紧凑表示逐级展开出多个质量档位、各级均保持渲染质量，并让过渡尽量连续，是核心问题。

## 方法详解（含关键公式/架构，保留原文术语）
基础表示沿用 3DGS：每个 3D 高斯由中心 μ 与协方差 Σ=RSS^T R^T 定义，G(x)=exp(-1/2(x-μ)^T Σ^{-1}(x-μ))，附带 opacity α 与 SH 视角相关颜色；渲染时投影为 2D 椭圆并按深度 alpha compositing：C(x′)=Σ_{i∈N(x′)} c_i σ_i(x′) Π_{j=1}^{i-1}(1-σ_j(x′))，其中 σ_i(x′)=α_i G_i′(x′)。在此之上采用 Scaffold-GS 式 anchor：每个 anchor 含特征 f_a∈R^32、位置 x_a∈R^3、基础缩放 l_a∈R^3 与 k 个可学习偏移 O_a∈R^{k×3}，由相机距离 σ_c=||x-x_c||_2 与方向 d_c 经神经预测 F(f_a, σ_c, d_c) 生成 k 个神经高斯的 {α^i, c^i, s^i, r^i}。核心为 Iterative Gaussian Synopsis：对全分辨率 anchor 结构做 top-down unfolding，逐级凝结出层次化 LOD，训练从最紧凑 synopsis（6.5MB）开始迭代展开至最高保真级（50.7MB），并配 level-specific adaptation；推理时按带宽/内存选择档位，实现从紧凑概要到高保真的渐进渲染。

## 实验与结果（表格化关键数字）
在 Mip-NeRF360、Tanks & Temples、DeepBlending、BungeeNeRF 四个公开数据集上评测，覆盖复杂室内外场景。核心对比见 Fig.1 的 LOD 阶梯：本方法从 6.5MB 的紧凑 synopsis 渐进展开到 50.7MB 最高保真级，标准 3DGS 基线总大小 601.1MB；中间级表示比基线更清晰，在相当视觉质量下存储成本大幅降低。作者结论为全部 LOD 保持高渲染质量，验证了在带宽/内存受限场景做实时 3DGS 渲染的实用性与可扩展性。实验章节含 Architectural Analysis 与 Ablation Studies，但 digest 未收录逐数据集 PSNR/SSIM 数值表，压缩-质量的具体 trade-off 曲线待核。

## 创新点与贡献
- 首次以 top-down unfolding 组织 3DGS anchor 结构，把单一模型变成 6.5MB→50.7MB 的层次 synopsis 阶梯
- Iterative Gaussian Synopsis 训练框架：从最紧凑级迭代展开，各级共享 anchor 表示
- 相对标准 3DGS 601.1MB 的存储压缩约一个数量级，且中间 LOD 表示更清晰
- 共享 anchor 天然抑制 LOD 过渡的空间不连续，优于独立参数基线

## 局限与风险
- 引入额外训练复杂度（作者自述）
- 仅限静态场景，动态内容需要扩展 unfolding 机制
- 离散层次结构在新 anchor 激活时仍可能产生 mild popping 伪影
- digest 未含逐数据集定量数值，压缩率-质量曲线待核

## 与文献库的关系（新增 / 改进 / 取代 X）
直接对标库内 3DGS 压缩/LOD 家族：MoQSplat 3.75（自适应渐进流式）、Budgeted-GS 4.65（LOUD）、COSA-GS、TopoGS、Towards Practical Compression of 3DGS 3.85；其 anchor 神经预测路线继承 Scaffold-GS 系（如库内 2610.29041）。差异在 top-down unfolding 与迭代 synopsis 的层次渐进组织及 MB 级 LOD 阶梯，可作库内渐进传输方案的对照锚点。

## 可复现性（代码/数据/硬件）
Project page：https://cs-luyq.github.io/UnfoldingGS/ ；digest 未提及代码/数据开源；License CC BY-NC-SA 4.0。

## 行动建议
① 做 XR 云渲染/流式传输时，把 6.5→50.7MB 的 LOD 阶梯作为带宽自适应档位设计参考；② 复现重点在 anchor 共享与迭代展开的损失调度，并在四数据集上量化 popping 伪影；③ 与库内 MoQSplat 的自适应渐进流式做同场景对照，评估存储-带宽-质量 trade-off。

### 第 2 章 · 手背图像用于 XR 沉浸式年龄保障与儿童安全（3.40 B · 感知与认知 · FULL）

# 手背图像用于 XR 沉浸式年龄保障与儿童安全

## 一句话结论
首个跨 minor-adult 边界（10 岁+）并以 ITA 覆盖全 Fitzpatrick 谱系的年龄分层手背研究：participant-level 5 折下 SwinV2-B MAE 5.78yr、pAUC@0.1 0.0587，论证手背 RGB 支持隐私友好的 XR 年龄保障与儿童安全。

## 要解决的问题
XR 平台的年龄保障与儿童安全需要低成本年龄推断，但主流依赖面部生物特征，隐私与重识别风险高；手背是 XR 交互中自然暴露的部位且无面部争议，却缺乏系统研究——没有跨法定 18 岁边界、含未成年参与者的数据集与基准，也没有全 Fitzpatrick 谱系的肤色公平性证据。本文要在标准架构上刻画手背 RGB 在 minor-adult 边界的可达到精度，评估其作为 safety-critical age gate 的可行性与偏差。

## 方法详解（含关键公式/架构，保留原文术语）
两任务评测：连续年龄回归与二元 adult/minor 分类（age gate），统一 participant-level 分层 5 折交叉验证。概率化回归：每模型输出均值 μ 与 log-variance，最小化 Gaussian NLL（Eq.1），gate 由概率输出导出。四个骨干各代表一个设计点：ResNet-50 224×224、EfficientNetV2-S 384×384（主 CNN 候选，保留 wrinkle density、melanin distribution 细纹理）、Swin Transformer V2-B 384×384（shifted-window 注意力适配手部局部纹理）、MobileNetV3-Large 224×224（端上 XR 推理效率前沿）。数据划分防身份泄漏：先按年龄×肤色联合分层抽 15% held-out test（2 年 bin 至 50 岁、其后 5 年 bin），其余 85% 同方案 5 折（每折约 68%/17%）。因 XR 中手姿态不受限，增强含 [-360°,360°] 全旋转、水平/垂直翻转与 ±10% 亮度对比度抖动，ImageNet 归一化；AdamW（lr 3e-4、weight decay 1e-2）≤40 epoch、early stopping（patience 20、min delta 1e-3）、batch 32、seed 42，8×A100 训练；统计用 5 折配对检验、repeated-measures ANOVA + Friedman 与 Holm–Bonferroni 校正。

## 实验与结果（表格化关键数字）
年龄回归：SwinV2-B 最低 MAE 5.78±0.64 yr、RMSE 7.47±0.72 yr；EfficientNetV2-S MAE 6.01±0.11 yr 次之；MobileNetV3-L 全面最差；另报 intra-user STD（每人 16 次采集）衡量 gate 决策稳定性。Omnibus 检验确认三指标跨模型差异显著；Holm 校正后 pairwise MAE 差异不显著，但 MobileNetV3-L 与 SwinV2-B 的 RMSE 差距达显著（p=0.016）。Age gate：Table 2(A) 报跨模型 AUC 与 pAUC@0.1，SwinV2-B pAUC@0.1=0.0587；Fig.6(a) 给四架构 5 折 ROC（mean±std，FPR=0.1 参考线），(b) 将 SwinV2-B ROC 按肤色组分解（Light=ITA I–III、Medium=IV、Dark=V–VII）；Table 2(B) 报三阈值下 minors FPR 与 adults FNR；另做 multi-capture aggregation 实验。

## 创新点与贡献
- 首个跨 minor-adult 边界、含未成年参与者（10 岁+）的手背年龄推断研究与基准
- 首次将 ITA 全 Fitzpatrick 谱系肤色刻画引入年龄保障公平性评估
- 概率化 Gaussian NLL 回归直接映射既有 age-assurance 框架，输出不确定度供 gate 决策
- 针对 XR 手姿不受限设计 [-360°,360°] 全旋转增强，并评估端上候选 MobileNetV3-L
- 利用手背无面部生物特征、低重识别风险的隐私属性，契合数据最小化监管要求

## 局限与风险
- 手背推断精度有限（MAE 5.78yr），18 岁边界附近的误分类风险需部署前评估
- digest 未报告数据集总样本量与逐肤色组样本数，泛化估计的统计功效待核
- 仅静态 RGB 手背图像，未覆盖 XR 实际使用中的遮挡、传感器噪声与运动模糊
- 跨设备、跨场景泛化未验证（作者列为未来工作）

## 与文献库的关系（新增 / 改进 / 取代 X）
属库内感知与认知方向：与 Gaze2HOI 4.00 同属 XR 感知输入，但首次把手背生物特征用于 age assurance；库内 VR 安全/隐私方向薄弱，本文以「非面部、低重识别风险」模态填补年龄门控空白，可与 gaze 交互安全、家长控制类研究组合成 XR 儿童安全证据链。其概率回归与分组公平性协议也可复用到库内其他生物特征模态。

## 可复现性（代码/数据/硬件）
digest 未提及代码/数据开源；License CC BY 4.0；训练于 University of Greenwich HPC（8×NVIDIA A100-SXM4 80GB）。

## 行动建议
① 做 XR 年龄保障/儿童安全功能时，将手背作为面部之外的补充模态评估，重点核对 18 岁边界 FPR/FNR 及肤色分组差异；② 复现须严格遵守 participant-level 划分与 ITA 分组协议，避免身份泄漏与公平性高估；③ 参考其 multi-capture aggregation 提升 gate 稳定性。

### 第 3 章 · 可微任务驱动编码孔径相机设计（3DGS 场景表示）（3.35 B · 渲染与显示 · FULL）

# 可微任务驱动编码孔径相机设计（3DGS 场景表示）

## 一句话结论
提出可微任务驱动相机设计框架：以真实采集重建的 3DGS 作可微虚拟成像环境，相机参数、编码孔径 mask 与任务网络端到端联合优化，在单目/立体 depth-from-defocus 与 AiF 重建上一致优于固定相机与无导数优化基线，并揭示解耦设计会错过的可解释权衡。

## 要解决的问题
编码孔径等计算摄影相机的设计（mask 图案、焦距、f-number、传感器、立体基线）长期依赖手工解耦设计与无导数优化，难以联合考虑下游感知任务（深度估计、AiF 重建）的真实目标，可扩展性受限；同时缺乏可微的「虚拟环境」仿真成像过程——真实场景采集成本高、覆盖有限。要把相机设计与下游任务放进同一可微管线，并用重建的 3D 场景表示充当可微图像形成环境，是关键挑战。

## 方法详解（含关键公式/架构，保留原文术语）
框架核心是用 gsplat 重建的 3D Gaussian 表示作为可微虚拟环境：仿真编码孔径相机的图像形成（defocus blur 由 focus、焦距、f-num、传感器与像素尺寸等参数驱动），梯度可经任务损失反传到相机参数、coded aperture mask 与任务网络，实现三者（含立体场景的 inter-camera geometry）的端到端联合优化，避免无导数优化的可扩展性上限。环境度量尺度用 Depth Anything 3 的度量深度对齐重建恢复。优化用 Adam 20,000 步、batch size 3，相机参数 lr=1e-2、mask 与任务网络 lr=1e-3；噪声模型在 Basler Dart DaA1280-54uc（5ms 曝光、10dB gain、f/8）上标定，作为泛化参考点。任务选取两个 close-range 场景：单目面向机器人抓取工作空间的单捕获 RGB-D，立体面向微距摄影（浅 DoF 强 defocus，立体对补充 photometric 与 geometric 深度线索）。

## 实验与结果（表格化关键数字）
场景取自 MipNeRF360 与 LLFF 的 close-range 子集：单目 6 场景（leaves、flower、fortress、orchids、bonsai、room），立体 7 场景（4 个 LLFF 场景 + counter、kitchen、bonsai）。每场景建 3DGS 虚拟环境并对齐 Depth Anything 3 度量尺度，相机设计与任务网络跨场景联合优化，留部分视图评估。指标含 AiF 的 PSNR/SSIM/LPIPS 与深度的 RMSE/MAE/log10/δ<1.25，并设 Noise×100 场景。Table 1 中 Fixed Cam.+Phase+Ikoma et al. 配置：AiF PSNR 22.587dB、SSIM 0.669、LPIPS 0.308，深度 RMSE 0.131m、MAE 0.080m、log10 0.102、δ<1.25 0.910。Table 2 立体对比中，monocular row 为同窄 FoV 下自身最强单目配置以隔离第二视角收益，并与 CADS（最近 coded-aperture 基线，dual-pixel 限于亚毫米孔径尺度）比较；作者报告立体设计在 AiF 重建上优势尤其明显。另做消融与 real-world validation；digest 未含完整分方法数值表。

## 创新点与贡献
- 用 3DGS 重建充当可微虚拟成像环境，把相机设计从无导数搜索/真实采集依赖中解放
- 相机参数、coded aperture mask、任务网络（含立体几何）端到端联合可微优化
- 设计准则直接优化 depth-from-defocus 与 AiF 等下游任务目标，而非间接成像指标
- 真实相机噪声标定 + real-world validation，揭示解耦流程会错过的可解释设计权衡

## 局限与风险
- 聚焦 close-range（defocus 线索在远处信息量不足），中远距场景未覆盖
- 依赖 3DGS 重建质量与 Depth Anything 3 的尺度对齐，上游误差会传入设计
- digest 未含完整定量表，相对基线的提升幅度与最优设计参数待核
- 3DGS 虚拟环境与真实传感器（噪声、畸变、运动）间的 sim-to-real 差距需逐硬件标定

## 与文献库的关系（新增 / 改进 / 取代 X）
属库内渲染与显示（硬件类）：与 HoOPOE 4.27（全息 CGH 感知损失）同属用感知/任务损失设计光学元件，与 CVQPG 2609.11434（全息/近眼显示 3DGS）、Foveated Compression 4.00、Masking Judder 3.78 构成计算成像-近眼显示谱系。独特之处是把 3DGS 从「被渲染对象」转为「可微相机设计的虚拟光场」，与库内 3DGS 压缩家族（Scaffold-GS 系、同批 Unfolding 3DGS）形成表示质量→成像设计的上下游。

## 可复现性（代码/数据/硬件）
digest 未提及代码开源；License：arXiv.org perpetual non-exclusive license；实验基于 gsplat、Depth Anything 3 与 Basler Dart DaA1280-54uc 噪声标定。

## 行动建议
① 设计 XR 环境感知/近眼相机时，用「3DGS 虚拟环境+任务损失」联合优化孔径、焦距与立体基线，替代手工解耦；② 复现先建 gsplat 场景并完成 Depth Anything 3 尺度对齐，再按 20k 步 Adam（相机 lr 1e-2）联合训练；③ 重视其噪声标定协议以缩小 sim-to-real 差距。

### 第 4 章 · SceneRig：单图生成仿真就绪 3D 场景的智能体系统（3.35 B · 世界模型与仿真 · FULL）

# SceneRig：单图生成仿真就绪 3D 场景的智能体系统

## 一句话结论
SceneRig 用智能体系统从单图重建仿真就绪 3D 场景：VLM 提出 relational scene graph，MoGe-2 度量初始化，物理沉降与 physics-grounded pose refinement 精修，在 80 图基准上超四基线，支持 real-to-sim 策略评估。

## 要解决的问题
机器人仿真需要与真实场景外观和物体摆放一致的 3D 场景，但单图重建不知道物体间支撑/结构关系、缺乏度量尺度与重力对齐坐标系，生成摆放常不满足物理稳定（穿模、悬空），资产也不可直接仿真（无碰撞体/材质）。已有方法或忽略关系与物理，或不能端到端产出 simulator-ready 场景；需要把感知（关系解析、度量估计）、生成（几何/材质/光照）与物理仿真（沉降、位姿修正）组织为一个智能体系统。

## 方法详解（含关键公式/架构，保留原文术语）
实体表示：可动物体 O 与根表面 R（桌/地/墙）构成 V=O∪R，每个实体有持久身份与状态 x_v=(M_v, τ_v, θ_v^phys, X_v)——几何、外观、碰撞与物理属性、度量变换；场景图 G=(V,E)，E=E_sup∪E_surf 分别记录物体-支撑边与根间结构边；另维护光照 L。流水线三阶段：① relational & metric initialization——VLM 提出物体/根表面及支撑结构关系与逐实例描述，MolmoPoint 定位并取 SAM3 候选实例 mask，后检查补漏、修复分裂/合并 mask、修订根表面，遮挡物体可选 LanPaint 去遮挡再分割；MoGe-2 估相机内参与密集度量 3D 点图（有 RGB-D 则替换），主支撑面拟合平面定义重力对齐坐标系（支撑面 z=0），拟合平面与接触几何作为关系验证证据；② agentic scene construction——几何、材质、光照 agent 构建周围场景并经 support-ordered settling 物理沉降初始化；③ physics-grounded object pose refinement——pose-refinement agent 检查成对 reference/render crops，调用几何与物理 grounded 工具修正物体摆放，最终导出仿真器。

## 实验与结果（表格化关键数字）
基准含 80 张桌面图像，其中 44 张为 RoboDojo 仿真渲染图。基线与对照：VIGA、REST3D、SceneConductor、SimFoundry 四个方法（VIGA 加 object-grouping contract 以支持物体中心评测）；SAM3D* 共享分割、相机、物体与场景上下文但保留 SAM3D 预测位姿，去掉度量 grounding、物理沉降与位姿修正，用于隔离各组件贡献；另有 GPT-6 Astra 时代的 Codex（通用 harness 直接在 Blender 重建）。默认 VLM 为 Claude Opus 5。评测重建保真、物体恢复、3D layout 与物理稳定性，并消融 physics-grounded placement、VLM backbone 与重建 harness；机器人应用含 real-to-sim policy evaluation 与 open-loop trajectory replay，比 SimFoundry 更忠实复现真实世界结果。digest 未含具体数值表（原文有）。

## 创新点与贡献
- 把单图场景重建组织为关系解析→度量初始化→agentic 构建→物理 grounded 修正的智能体流水线
- relational scene graph + 支撑面拟合的重力对齐度量坐标系（z=0），直接产出 simulator-ready 摆放
- physics-grounded pose refinement：agent 对比参考/渲染 crop 并调用几何+物理工具迭代修正
- 在 80 图基准上系统对比 4 基线 + SAM3D* + Codex，并以 real-to-sim 策略评估闭环验证

## 局限与风险
- 复杂房间场景仍困难：遮挡、深度歧义与频繁接触
- SAM3D 缺 PBR 材质，真实感受限
- 每个物体视为单一刚体，不恢复关节结构或变形
- 依赖 VLM 与多个基础模型（MoGe-2/SAM3/MolmoPoint/LanPaint），计算成本高且误差传播未量化

## 与文献库的关系（新增 / 改进 / 取代 X）
属库内世界模型与仿真方向：与 SnapPhysics 4.12（单视图物理场景图）共享「单图→物理场景」目标，但 SceneRig 走 agentic 多工具路线并直接导出仿真；与 GaussianBench 3.57（高斯物理保真度基准）互补——后者评测、前者产出；与 Astronex-World 4.32、EgoExplorer 4.30 同属场景/世界构建线。其 MoGe-2 度量初始化与库内 3DGS 重建线（本批 Unfolding 3DGS、2610.29041）共享度量点图上游。

## 可复现性（代码/数据/硬件）
项目页 https://red-fairy.github.io/SceneRig/ ；License CC BY 4.0；digest 未明确代码开源；默认 VLM 为 Claude Opus 5，仿真器导出细节见附录。

## 行动建议
① 做 real-to-sim/机器人仿真时，用「场景图+物理沉降+位姿修正 agent」从单图快速搭场景，替代手工摆放；② 复现先接 MoGe-2 度量深度与 SAM3 分割，再实现 pose-refinement agent 的成对 crop 检查回路；③ 以 80 图基准与 SimFoundry 对比协议作为验收标准。

### 第 5 章 · WARPED：手腕对齐渲染（第一视角示范→机器人策略）（3.30 B · 内容生成 · FULL）

# WARPED：手腕对齐渲染（第一视角示范→机器人策略）

## 一句话结论
WARPED 用单目 RGB 第一视角示范合成手腕相机观测与重定向动作：SfM+3DGS 场景、hand-object optimization 跟踪、手腕视图渲染并增强 10 倍，diffusion policy 在 6 个真实 xArm7 任务上优于 Meta Quest 2 VR 遥操作基线。

## 要解决的问题
训练 robust 手腕相机视觉运动策略需要大量机器人示范，采集成本高、难扩展；人类第一视角示范易获取，但观测视角（第一视角 vs 手腕视图）与动作空间（人手 vs 夹爪）双重不匹配，无法直接使用。已有方法常依赖多视角相机、深度传感器或定制硬件，且只能从第三/第一视角执行策略。需要仅用单目 RGB 把人类示范转为手腕视图的机器人观测-动作对，并支持低成本数据增强。

## 方法详解（含关键公式/架构，保留原文术语）
五阶段流水线：data collection、interactive scene initialization、hand-object optimization、wrist-view retargeting & rendering、policy training & deployment；仅需单目 RGB 相机。假设：刚性物体桌面操作（另评一个单轴 articulated 物体）、夹爪末端、物体保持部分可见、有限手内运动且无重复重抓。采集：先扫工作空间（<1 分钟），LightGlue 特征匹配的 SfM 估位姿并建稀疏 3D，用于初始化 3DGS 并定位后续示范；用户戴头盔 GoPro Hero9（线性镜头、针孔模型）录示范。初始化：Hierarchical Localization 逐帧定位，SpatialTrackerV2 提取时序一致单目深度并与 SfM/3DGS 尺度对齐，HAMER 初始化手部形状位姿并经序列级优化（时序平滑+深度一致）精修。hand-object optimization：接触起止估计 + 关节手-物联合精修 + 辅助损失。重定向与渲染：hand-to-end-effector mapping、pre-contact trajectory optimization、contact point selection、contact grasp refinement，轨迹重定向到夹爪并合成手腕视图渲染。示范增强 10 倍后训练 diffusion policy。

## 实验与结果（表格化关键数字）
硬件：UFactory xArm7 + xArm G1 Gripper；示范用头盔 GoPro Hero9，rollout 手腕侧 GoPro Hero9 + Max Lens Mod 1.0。任务：5 个刚性桌面任务（Rotate Box、Pour Mug、Bottle from Dish Rack、Wipe Plate with Brush、Can on Plate）+ 1 个 articulated 任务（Open Microwave）。每任务 30 个示范（固定工作空间、单一物体实例）+ 单张物体图供 SAM3D 网格重建，增强 10 倍，4×NVIDIA Tesla V100 训练 diffusion policy，成功率按 20 次试验评估。基线：Meta Quest 2 VR 头显+手柄遥操作示范训练的策略（同样 30 示范、不用合成增强），以及 RwoR 的 Alter 基线（测试时无公开代码/模型）；所有方法统一手腕相机观测模态。附录含 hand-object optimization 消融、数据增强消融、背景干扰物鲁棒性、与遥操作共训练、OOD 场景、与 UMI 对比及数据处理时间。

## 创新点与贡献
- 仅用单目 RGB 第一视角视频合成手腕视图观测-动作对，免多视角/深度传感器/定制硬件
- 视觉基础模型栈初始化交互场景：SfM+3DGS+SpatialTrackerV2+HAMER，再以 hand-object optimization 联合精修
- 重定向含接触点选择与抓取精修，渲染观测直接匹配部署时手腕相机模态
- 合成增强 10 倍 + diffusion policy，真实机器人上超过 Quest 2 VR 遥操作数据基线

## 局限与风险
- 假设较强：刚性/单轴 articulated、物体部分可见、无重复重抓与接触点突变
- 依赖 SAM3D 等基础模型的网格与位姿质量，误差传播未量化
- 每任务单一物体实例与固定工作空间采集，泛化仅部分验证（附录 OOD 实验）
- RwoR 无公开代码/模型，与最强竞品的直接对比缺失

## 与文献库的关系（新增 / 改进 / 取代 X）
属库内内容生成/具身方向：与 UMI-Bridge 3.80（人-机动作空间映射）同属人类示范→机器人策略，但 WARPED 增加 3DGS 手腕视图渲染层，直接弥合观测模态差；与 EgoJEPA 3.85（第一视角灵巧操作）互补——后者学第一视角表征、前者产手腕视图训练数据；库内暂缺其竞品 RwoR，本条可作该方向基准锚点。其 SfM+3DGS 场景构建与本批 Unfolding 3DGS、SceneRig 的度量重建线呼应。

## 可复现性（代码/数据/硬件）
项目页 https://kantor-lab.github.io/WARPED/ ；License CC BY 4.0；digest 未明确代码开源；训练用 4×NVIDIA Tesla V100。

## 行动建议
① 需低成本机器人操作数据时，用「单目 RGB+3DGS 手腕视图渲染」转化人类示范，先核对任务是否满足刚体/部分可见假设；② 复现重点是 hand-object optimization 的接触起止估计与 contact grasp refinement；③ 与库内 UMI-Bridge 的动作空间映射对照，量化手腕视图渲染的 sim-to-real 增益。

### 第 6 章 · 单头戴相机标注的无电子 UMI 手套数据采集（3.23 B · 系统与平台 · FULL）

# 单头戴相机标注的无电子 UMI 手套数据采集

## 一句话结论
USD 122 头戴单目相机 + USD 22 无电子 fiducial 手套 + 纸 tile 取代手腕相机、位姿跟踪器（SLAM/IMU/VR 控制器），同帧解算夹爪位姿与钳口开度标注：中位误差 6.5 mm，替代编码器训练 val 损失仅差 3%，手套段共训练显著放大低预算遥操作收益。

## 要解决的问题
手持演示设备把数据采集与机器人解耦，但常规设计让手背负手腕相机、线缆与位姿跟踪器（SLAM、IMU、VR 控制器，或会被采集者身体遮挡的固定外相机），管线还要对多路数据流做时间戳、同步与交叉标定，硬件与工程负担随流数增长。本文要回答：能否用「一个随头部运动的单目相机」同时完成观测与标注，去掉全部电子器件与额外数据流——既压低采集成本，又让标注来自策略将要看到的同一画面，从机制上消除采集—部署的视角差。

## 方法详解（含关键公式/架构，保留原文术语）
硬件与标注链全部去电子化：采集者头戴一副 USD 122 单目 egocentric 相机；手套为 USD 22 无电子手套，表面打印 fiducial 标识；工作区四周贴纸 tile 作空间参照。相机读取手套 fiducial 相对纸 tile 的构型，解算 6-DoF gripper pose 与 jaw width，且标注帧即策略将要看到的观测帧。部署时同一相机改置于机器人旁一副 USD 120 低成本机械臂（positioner）上，由机器人关节状态实时复现采集者头部运动，使采集与部署视角闭环。数据侧把遥操作 episode（编码器标签）与手套演示 segment 混合共训练（co-training）；策略为 ACT，验证损失取 6 个留验遥操作 episode（编码器目标）上的 ACT loss。tile 布局按中位单 tile 位姿细化而非全 bundle adjustment。rollout 协议：25 次放置、每次一试、60 s 预算，失败分未抓取（n）、掉落（d/b）与超时（t）。八臂设计把共训练、标签来源（编码器 vs 头相机）、观察视角（头相机/手腕 fisheye/固定相机）三个因子解耦。

## 实验与结果（表格化关键数字）
八臂消融（Table 1）：arm 1 纯遥操作 172 episode：val 0.318、18/25；arm 2 加 194 手套段共训练：val 0.263、20/25；低预算 arm 3（48）10/25，arm 4（48+194）17/25，持平 172 条纯遥操作的 18/25。arm 6 用头相机标签训练：val 0.328 对 0.318（差 3%），机器人 15/25 对 18/25，McNemar p=0.58。视角臂：arm 5 手腕相机 UMI 方案（消融加 fisheye）15/25，失败以 dropped 为主（n6 d3 b1）；arm 7 固定相机 12/25；arm 8 头标注+手腕视角 14/25。标签精度：以 YAM 球为参照、编码器为真值，5,065 帧内 tool point 中位误差 6.5 mm（p90 14.1 mm）、1.55°（p90 2.70°），帧覆盖 93–100%；钳口开度在 112 个 episode（24.6k 帧）中位误差 3.5% 行程（p90 7.9%），闭合状态 2.3%，无延迟，9/10 episode 每帧有标签，误差跨工作空间/距离/俯仰/视角分箱平坦（2.8–4.8% 中位）。头相机可见前臂与手指，glove-only 策略不迁移（val 0.52 对 0.26）。

## 创新点与贡献
- 单头戴相机一举取代手腕相机、位姿跟踪器（SLAM/IMU/VR 控制器）及多路数据流，采集硬件降到 USD 122 相机 + USD 22 无电子手套 + 纸 tile
- 标注与策略观测同源同帧，从机制上消除采集—部署视角差；部署侧以 USD 120 机械臂由关节状态复现头部运动完成闭环
- 系统量化标签精度（6.5 mm/1.55° 中位、钳口 3.5% 行程），并证明约 194 条手套段可把 48 条遥操作拉到 172 条水平的成功率
- 八臂协议把共训练增益、标签来源、观察视角三因子解耦，为 UMI 类方案提供受控比较模板

## 局限与风险
- 标注需同时看到手套与纸 tile，覆盖依赖 tile 布局，论文只试了一种布局
- tile 布局仅按中位单 tile 位姿细化，未做全 bundle adjustment，作者自述还有收紧空间
- positioner 延迟 0.4 s、宽幅扫动触关节限位，视角模型为单会话线性拟合且未按 rollout 调优
- 手腕相机支架常遮挡钳口（仅为手腕视角消融保留，头相机系统不需要），移除它被作者列为最便宜的下一步改进

## 与文献库的关系（新增 / 改进 / 取代 X）
属库内系统与平台/数据采集线：UMI-Bridge 3.80 解决人—机动作空间对齐（手套到机器人的映射），本文解决标注与观测的硬件来源，两者正交互补；相对 DELUGE 4.65 等重型采集平台，本文是『USD 122 相机 + USD 22 手套』级的极简末端方案，直接补库内第一视角采集硬件的薄弱环节；八臂协议也为『数据构成 vs 观察视角』的受控比较提供模板。

## 可复现性（代码/数据/硬件）
digest 未提及代码链接；论文 License CC BY 4.0。硬件：USD 122 头戴相机 + USD 22 无电子打印 fiducial 手套 + 纸 tile + USD 120 复现臂；平台为 YAM；数据自采（172/48 条遥操作 episode 与 194/253/255 条手套段）；策略为 ACT，rollout 25 次放置×60 s。

## 行动建议
搭低成本遥操作采集时，可用『头戴单目 + 打印 fiducial 手套 + 纸 tile』整体替代 SLAM/IMU/VR 控制器链路，优先复刻其共训练配方（低预算遥操作混手套段收益最大）；抓取精度敏感的场景先按钳口中位 3.5% 行程误差口径在自有硬件上核验标签精度，并去掉手腕相机支架以消除钳口遮挡。

### 第 7 章 · GTSM：热状态空间动力学高斯泼溅（4D 热场重建与预测）（3.17 B · 神经渲染 · FULL）

# GTSM：热状态空间动力学高斯泼溅（4D 热场重建与预测）

## 一句话结论
GTSM 以场景级共享潜过程+每高斯局部热状态建模热演化，经可微 RK2 积分传播，免预定义 3D 模型/热力学方程即可恢复 4D 热场：RHD 上平均 PSNR 41.15 超 ETGS 40.23，外推 40.98 超 MLP 38.11 与 ETGS 29.49，兼容 3DGS/4DGS。

## 要解决的问题
工业与动态环境中的状态监测、过程分析依赖温度场重建与预测。既有路线或需预定义 3D 模型、规定热力学方程、给定升降温轨迹，难以直接从二维多时相观测恢复四维时空热状态；只能在观测区间内插值外观的方法没有连续热演化模型，无法外推未来时刻。GTSM 要同时解决：从多视角、多时相观测推断连续热动力学、越过观测区间预测未来温度，并兼容静态与随时间形变的几何。

## 方法详解（含关键公式/架构，保留原文术语）
GTSM（Gaussian Thermal State-Space Model）把热状态挂在 GS 图元上：热演化由共享的场景级潜过程（shared scene-level latent process）与每高斯特定的局部热状态（Gaussian-specific local thermal states）共同刻画；连续动力学经可微 RK2 积分传播，使热演化既能从多视角/多时相观测推断，又能连续外推到观测区间之外。该模块被设计为 backbone 无关的热动力学插件：在几何近似静态的设置（RHD 对应场景）中，热状态场由静态 3DGS 图元承载，相机运动提供多视角约束、毫秒级时间戳提供多时相约束；在几何与温度同步演化的设置中，则与动态 4DGS 结合，论文称验证了 GTSM 对形变目标的适用性。重建表示支持新视角热渲染与未来时刻热状态预测。作为对照，论文另设 MLP 基线——直接从空间位置与归一化查询时间预测每高斯温度，不含显式热状态、弛豫动力学与时序 rollout，用以度量结构化热动力学的增益。

## 实验与结果（表格化关键数字）
两个互补数据集：真实 RHD（Rapid Heat Dynamics，沿用自 ETGS）——多目标真实 RGB–IR 序列，覆盖 warming/cooling/heating/heat transfer，毫秒级时间戳、辐射定标，静态几何（3DGS 设置）；合成集——基于 D-NeRF 保留相机轨迹与目标运动，前景分割成语义组件并赋模拟组件级温度图（4DGS 设置）。within-interval 新视角/时序插值（Checkboard/Bottles/Dumbbells/Bench/Ebike/Transfer/Peaches/Workpiece/Cups/Workpieces 10 场景）：PSNR 平均 3DGS 32.16、Thermal3D-GS 34.68、4D-GS 32.34、NTR-Gaussian 34.96、ETGS 40.23、GTSM 41.15（首场景 Cooling 44.86 对 ETGS 43.14）；SSIM 平均 0.990 对 0.989；LPIPS 平均 0.055 对 0.058。时序外推只与 ETGS（明确建模连续热演化）及新增 MLP 基线比：PSNR 平均 GTSM 40.98 对 MLP 38.11、ETGS 29.49；SSIM 0.991 对 0.988、0.948；LPIPS 0.055 对 0.081、0.087。

## 创新点与贡献
- 把热场演化建成高斯热状态空间模型：场景级共享潜过程 + 图元级局部热状态
- 可微 RK2 积分传播连续动力学，实现越过观测区间的未来温度外推
- 免预定义 3D 模型/热力学方程/升降温轨迹，直接从 2D 多时相观测恢复 4D 热状态场
- backbone 无关热动力学模块，同一框架覆盖静态 3DGS 与动态 4DGS（形变目标）

## 局限与风险
- 真实评测限于 ETGS 的 RHD（10 场景），场景数量与多样性受限
- 动态几何仅在 D-NeRF 合成温度图上验证，真实『动态几何+热演化』数据仍缺失
- 外推设置仅对比 ETGS 与简单 MLP 基线，缺其他时序动力学参照；digest 未报告运行时/存储开销

## 与文献库的关系（新增 / 改进 / 取代 X）
库内神经渲染线的时间维度补充：库内 4DGS 家族（如 SplatLabel 的 4DGS 伪标注）多以形变场/外观时序建模，GTSM 把时序对象从 RGB 外观换成物理量（温度），并以状态空间+可微 RK2 的结构化动力学替代通用 MLP；与库内语义/条件监测方向互补，为物理场重建在 GS 表示中开出新分支。

## 可复现性（代码/数据/硬件）
digest 未提及代码链接；RHD 数据集引自 ETGS [32]，合成数据基于 D-NeRF [33] 自建（语义组件级温度图）；指标为 PSNR/SSIM/LPIPS。

## 行动建议
需从红外序列做温度场重建与未来预测（设备状态监测、工艺分析）时，可把 GTSM 热动力学模块挂到现有 3DGS/4DGS 管线；复现先在 RHD 静态设置复现 within-interval 与外推指标，再迁 D-NeRF 合成设置验形变目标；注意其增益主在外推设置（40.98 对 29.49）。

### 第 8 章 · OV-Foam：幂图划分表示下的开放词汇特征提升（3.12 B · 神经渲染 · FULL）

# OV-Foam：幂图划分表示下的开放词汇特征提升

## 一句话结论
OV-Foam 指出开放词汇分割的特征提升依赖反投影分配，而 3DGS 图元重度重叠使每光线多图元、提升次优——反投影仅在无两图元共享光线时最小二乘可解；为此改用 PowerFoam 幂图划分表示实现零重叠并削减每光线图元数，使分配近优，开放词汇分割优于高斯基线。

## 要解决的问题
开放词汇分割的特征提升把图像端的语言/语义特征反投影分配到三维图元上。3DGS 重建的图元重叠严重，一条光线由许多图元共同支配，反投影分配长期处于次优；而理论上反投影只有在任意两图元不共享光线时才化为最小二乘可解。本文的立意（标题即点题：3D 表示塑造语义特征提升）是打通表示与提升的耦合——不在重叠表示上修补提升算法，而换一种零重叠表示，从根上恢复提升问题的最优可解性。

## 方法详解（含关键公式/架构，保留原文术语）
方法主体是表示替换而非新提升算法。论文标题『How 3D Representations Shape Semantic Feature Lifting』即点明论点：3D 表示的选择决定语义特征提升的质量。OV-Foam 采用 PowerFoam 作为底层场景表示：以幂图（power-diagram）对场景做空间划分，使图元之间零重叠，并显著减少每条光线穿过的图元数量。零重叠恢复了反投影分配成为最小二乘可解问题所需的几何条件，每光线图元数的削减进一步简化分配，使图像特征可以更接近最优地赋给图元。换言之，其贡献定位在表示层：给定零重叠的幂图划分后，提升端仍沿用既有反投影式分配，无需重新设计提升算法。摘要明确报告的两条结论是：空间划分图元达到近优分配（near-optimal assignment）；开放词汇分割实验优于高斯基线（Gaussian baselines）。而幂图如何由观测构建、划分粒度如何控制、与 PowerFoam 原表示实现的差异、训练流程与 2D 特征来源等，digest 均未覆盖，需正文补齐。

## 实验与结果（表格化关键数字）
【证据等级 PARTIAL】ar5iv 未返回正文，以下仅基于摘要，未在正文中核实。摘要级实验声明仅两点：① OV-Foam 的空间划分图元达到近优分配（near-optimal assignment）；② 开放词汇分割实验优于高斯基线（Gaussian baselines）。摘要未给出数据集、评测指标、基线名单（未点 LangSplat 等具体方法，是否含 LangSplat 系列不明）、增益幅度、消融与运行时开销；论文规模为 22 页、10 图、7 表，实验体量存在但内容不可见。待正文（PDF）获取后需补齐：在哪些开放词汇分割基准与指标上、相对哪些高斯基线、提升幅度多少，以及幂图划分的存储/渲染开销与零重叠表示的构建成本。

## 创新点与贡献
- 指出 3DGS 图元重叠使反投影提升丧失最小二乘可解性，把提升质量瓶颈定位到表示层
- 引入 PowerFoam 幂图划分表示，实现图元零重叠
- 零重叠 + 每光线图元数大幅削减，使特征分配接近最优可解
- 以『表示—提升』耦合视角重述开放词汇分割问题，为 3DGS 语义线提供非重叠表示路线

## 局限与风险
- 全文抓取失败（ar5iv 仅返回摘要页），实验与消融细节完全未核实，本笔记证据等级 PARTIAL
- 摘要仅称优于 Gaussian baselines，未报告与 LangSplat/LangSplatV2 等专门开放词汇方法的定量对比
- 幂图划分相对原生 3DGS 的存储与渲染开销摘要未述
- 『近优分配』为作者自证口径，独立复现前无法确认

## 与文献库的关系（新增 / 改进 / 取代 X）
与库内 NormLift 4.12（3DGS 语义特征提升的理论研究）构成『表示—提升』互补：NormLift 在给定表示上分析提升的性质，OV-Foam 改表示本身（PowerFoam 幂图划分、零重叠）使提升条件成立；库内竞品 LangSplat/LangSplatV2 属重叠表示上的提升方案，OV-Foam 提供绕开重叠的替代路线，是库内 3DGS 语义线的表示层新分支。

## 可复现性（代码/数据/硬件）
全文不可得（ar5iv 仅摘要页）；22 页、10 图、7 表，cs.CV/cs.GR；作者 Yousef Rajeh 等 5 人；digest 未提及代码链接。

## 行动建议
先取 PDF 正文核验：开放词汇基准、相对 LangSplat/LangSplatV2 的增益与幂图开销；库内与 NormLift 并列为『特征提升』条目的表示侧参照；自有 3DGS 语义场景若提升质量受图元重叠制约，可试用 PowerFoam 表示替换并评估每光线图元数的变化。

### 第 9 章 · Hilti-Trimble-Oxford：360° 视觉惯性基准（户型图先验）（2.95 C · 评估与数据集 · FULL）

# Hilti-Trimble-Oxford：360° 视觉惯性基准（户型图先验）

## 一句话结论
Hilti-Trimble-Oxford 发布活跃施工现场的 360 视觉惯性基准：30 条序列、10 楼层、8 个月，真值由固连 360 相机的 LiDAR-惯性 SLAM 提供；挑战赛评全球最佳视觉 SLAM 与户型图定位，SLAM 62 队远超户型图定位 22 队，后者是明显空白。

## 要解决的问题
施工进度监测的自动化依赖高精度视觉 SLAM 与户型图定位支撑变更检测。LiDAR 建图精度高但成本高昂，消费级 360 宽 FoV 相机加嵌入式 IMU 是低成本替代，却长期缺少在真实活跃工地上采集的高质量基准：那里有变光照、移动工人、快速运动与重复结构，与受控室内或 MAV 序列差异巨大。本文填补该空白，并以公开挑战赛量化全球最好系统的水平与两类任务的关注度差异。

## 方法详解（含关键公式/架构，保留原文术语）
本文以数据集与基准为核心贡献。采集端在活跃施工现场使用消费级 360 相机（宽 FoV）加嵌入式 IMU，记录 30 条视觉惯性序列，跨 10 个楼层、历时 8 个月，刻意保留变光照、移动工人、快速运动与重复结构等真实退化因素。真值端由高质量 LiDAR-惯性 SLAM 系统刚性固连于 360 相机提供轨迹，保证真值与相机运动严格同步。围绕数据组织公开研究挑战赛，设两个任务——视觉 SLAM 与户型图（floor plan）定位，前者比视觉惯性里程计/SLAM，后者比利用户型图先验的定位。digest 参考文献显示参评系统覆盖 OKVIS2-X、OpenVINS、ORB-SLAM3、sqrt-VINS 等 VI 方法与 Z-FLoc 式零样本户型图定位，轨迹评测走 evo；另有 Mask2Former、ViT 分割类引用（TABLE IV），或对应语义/进度监测扩展，digest 未含该部分内容。

## 实验与结果（表格化关键数字）
摘要级事实：30 条序列、10 楼层、8 个月采集期，真值来自固连 LiDAR-惯性 SLAM；公开挑战赛对全球最佳视觉 SLAM 与户型图定位系统排名，SLAM 任务 62 队参与、户型图定位仅 22 队，作者据此论证视觉 SLAM 已相当受关注、户型图定位需要更多研究投入。digest 抓取的全文仅余参考文献列表（抓取不完整），未含任何结果表、指标数值或系统排名，无法给出定量结论。从引用可确认论文实验横向覆盖 OKVIS2-X/OpenVINS/ORB-SLAM3/sqrt-VINS 与 Z-FLoc 类方法，评测工具为 evo，并可能含语义分割实验。待正文补齐：各方法 ATE/RPE 量级、户型图定位精度与失败模式、变光照/移动工人/重复结构的分场景表现。

## 创新点与贡献
- 活跃施工现场 360 VI 基准：30 序列×10 楼层×8 个月，保留变光照/移动工人/快速运动/重复结构
- LiDAR-惯性 SLAM 刚性固连 360 相机的真值方案，兼顾高精度与严格同步
- 公开挑战赛同时评视觉 SLAM 与户型图定位，以参与度差异（62 对 22 队）量化社区空白
- 面向施工进度监测/变更检测的真实需求组织数据，替代成本高昂的 LiDAR 建图

## 局限与风险
- digest 仅含参考文献，正文结果（指标、排名、失败案例）完全未核实
- 真值依赖 LiDAR-惯性系统，无 LiDAR 的纯视觉成本场景未被基准直接覆盖
- 8 个月/10 楼层集中在单一工地，跨工地泛化性未知
- 户型图定位参与度低（22 队），该任务基线水平可能不足以支撑强结论

## 与文献库的关系（新增 / 改进 / 取代 X）
属库内评估与数据集线：与 SLAMSqueezeBench 3.57、VISTA 3.70、TAVIS（主动视觉基准，backfill-2603-2609 入馆）互补——后三者覆盖仿真/主动视觉/受控设定，本基准把域扩展到活跃施工现场；Hilti 类 VIO 基准与库内 EuRoC/TUM-VI 用法互证，可作为 VI 管线从受控序列走向工地级难度后的下一级评测。

## 可复现性（代码/数据/硬件）
数据与挑战赛官网：https://hilti-trimble-challenge.com/dataset-2026（摘要给出）；digest 未提及论文代码；评测工具链引用 evo；参评系统 OKVIS2-X/OpenVINS/ORB-SLAM3/sqrt-VINS/Z-FLoc。

## 行动建议
做施工进度监测或户型图定位研究时，申请该基准（30 序列/10 楼层/8 个月）替代 EuRoC/TUM-VI 类受控序列做最终评测；户型图定位仅 22 队参与，是库内空白机会，可结合 Z-FLoc 类零样本方法切入；复现注意真值为固连 LiDAR-惯性系统，指标口径走 evo。

## 四、甄别记录

- 来源一（10-21 公告批次 listing 漏网）：摘要级过滤 19 篇命中中甄别 5 篇 XR 相关纳入；剔除 14 篇非 XR（视频时序定位 SuperClip、无人机定位 MatchCityLoc、动物行为、人机协作、LLM 前瞻记忆 ProMemAgent、扩散模型知识编辑、ObjectNav 主动验证、低比特 LLM BitMTP、dashcam 车道质量、人形接触重定向 REACT、CoGaussian 自动驾驶协同感知（尊重 10-22 运行剔除判断）、流式语言模型 Lafa、免学习室内探索 MAPLE）。
- 来源二（RSS 旧稿 replace/cross 再公告）：纳入 4 篇 XR 相关（Unfolding 3DGS / 手背 XR 年龄保障 / WARPED / Hilti 基准）；剔除 3 篇非 XR（2610.24858 MRI 超分 / 2602.01860 无人机竞速 / 2602.11321 人形遥操作）。
- GTSM（2610.26918）应用域为工业热场监测（10-22 运行曾据此将其剔除出主批），本批以其 3DGS 方法贡献（热状态空间动力学 4D 重建）**边界纳入**、B 级入馆，特此说明口径差异。
- 全文：9 篇中 8 篇 L0/FULL；2610.28131 OV-Foam L1 ar5iv 仅返 abs 页壳 → PARTIAL 摘要级评估。

## 五、产物清单

- 7 维表 / 评分明细 / 运行日志：`papers/daily/backfill-1023/`
- 原子笔记 9 篇：`papers/notes/`（2604.11685 / 2608.21009 / 2610.28004 / 2610.28585 / 2604.10809 / 2610.27622 / 2610.26918 / 2610.28131 / 2607.06464）
- 当日 MOC：`papers/MOC/MOC-backfill-1023.md`；总索引已刷新
- 文献库：`papers/library/registry.jsonl`（588→597）
