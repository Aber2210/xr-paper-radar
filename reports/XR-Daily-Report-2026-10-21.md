# XR 每日论文雷达 · 运行报告 2026-10-21

> **公告窗口**：2026-10-20（周二）公告批次（09-28~10-19 提交、周二 10-20 20:00 ET 释放）；**拉取日**：2026-10-21（周三）。
> **诚实口径**：本批处理 10-20 公告批次的**真新提交**（2610.* 前缀甄别）——**公告日≠拉取日**（周二公告、周三拉取），非当日（10-21）新提交。另单列 **backfill-1021**（RSS 旧稿 replace/cross 再公告 10 篇，2504~2609 原始提交首次入馆），未混入主批 Top10。

---

## 一、执行摘要

- **数据源与对账（第 1–3 步）**：listing 7 分类最新公告日 = **2026-10-20（周二）**（10-17/10-18 周末无公告）；10-20 日组 936 篇全部入账（无调度恢复后最大公告日），10-19 日组 373 篇中 361 篇不在库（摘要级命中 7 篇全部非 XR，与 10-20 运行互证，无新增漏网）。探针四源全 200（RSS cs.CV 505 条、cs.AI 789 条，双频道均非空——不同于 10-20 运行的 cs.AI 真空源）。
- **拉取与甄别**：RSS 7 分类去重 1426 条 → 关键词命中 91 条 → 去 registry(512) 后 **67 篇 2610.* 真新提交**（甄别 **31 篇 XR 核心/强相关**入评分池，36 篇非 XR 剔除）+ 20 篇旧稿 replace/cross（10 篇 XR 入 backfill-1021）+ 4 篇库内 v2 再公告剔除。listing×RSS 交叉验证：listing API 摘要级过滤命中 63 篇与 RSS 通道完全互证（RSS 为超集）。
- **全文抓取**：主批 31 篇 + backfill 10 篇共 41 篇候选，**40 篇 L0/FULL**（26,060–141,031 字符）+ **1 篇 PARTIAL**（2610.26549 Holi-World：L0 HTML 404、ar5iv 仅返摘要页 5177 字符，按摘要级评估并显式声明，禁止脑补正文）；串行 3s/篇，无限流/降级/伪造。
- **评分与 Top10**：主批入馆 **31 篇（S×0 / A×11 / B×15 / C×5）**；Top10 **10 篇全 A 级**（无 S 级），最高 **3.85**（O-SCD++ / SwitchSplat / Stable Signer V3 / DenseHap / EgoXperience / V-JEPA Hand 六篇并列）。
- **覆盖度三关**：门① 最大 Jaccard **0.143**（2610.24285 vs 库内 2609.22332，<0.62 通过）；门② Top10 覆盖 **5 赛道**（感知与认知×3、化身与人体×3、触觉与多模态×2、神经渲染×1、渲染与显示×1，≥5 通过）；门③ 当日最高 **3.85 < 库内近 30 天 Top10 均分 4.416**（现算，差值 -0.566）→ **非重磅日，无 S 级，未拔高**。
- **重要发现**：
  1. **第一视角手-物感知成簇**——EgoXperience（共享世界系联合输出相机+深度+双手+物体 6-DoF）、V-JEPA Hand（单次前馈恢复双手 MANO+相机轨迹）、DenseHap（单目稠密手部触觉）三篇同批入馆，第一视角手部感知从单任务估计走向「联合重建 + 触觉扩展」；与库内 EgoP²C/ReViV/ESTHER/Hand-4DGS 构成连续簇；
  2. **前馈 3DGS 效率线再添两条**——backfill 的 ZipSplat（62K 高斯 25.34 PSNR，token 解码）与主批 FineSplat（4×4 细粒度 patch 双分组）从「表示压缩」两侧挤压 per-pixel 基线，与库内 pixel-aligned 族（MVSplat/DepthSplat/DA3）构成效率竞合；SwitchSplat 则开辟「离散物体状态」这一新表示维度；
  3. **XR 显示预畸变补偿新范式**——Spatons 用空-色调局部化神经算子做预畸变（G-Res 混合几何畸变场景 PSNR 37.5 dB），与库内 CompenNet++ 等经典补偿网络构成不同范式对照，补库内渲染与显示硬件侧空白。

---

## 二、Top10 排行榜

| 排名 | 论文 | 赛道 | 总分 | 等级 | 证据 |
|---:|---|---|---:|---|---|---|
| 1 | O-SCD++：递归证据融合的免回放在线场景变化检测 | 感知与认知 | 3.85 | A | FULL |
| 2 | SwitchSplat：从随手捕获场景学习离散物体状态 | 神经渲染 | 3.85 | A | FULL |
| 3 | Stable Signer V3：4D 可变形基元泼溅用于手语生成 | 化身与人体 | 3.85 | A | FULL |
| 4 | DenseHap：单目图像的稠密手部触觉估计 | 触觉与多模态 | 3.85 | A | FULL |
| 5 | EgoXperience：从人类经验学习世界锚定的第一视角表征 | 感知与认知 | 3.85 | A | FULL |
| 6 | V-JEPA Hand：从第一视角视频恢复 3D 手部与相机轨迹 | 感知与认知 | 3.85 | A | FULL |
| 7 | Spatons：空-色调局部化神经算子用于高效 XR 预畸变补偿 | 渲染与显示 | 3.78 | A | FULL |
| 8 | PhysSkin++：自监督神经蒙皮的实时可泛化物理动画 | 化身与人体 | 3.77 | A | FULL |
| 9 | SynerGest：双人对话的时空协同手势生成 | 化身与人体 | 3.72 | A | FULL |
| 10 | ACTS：从人类物理交互学习视觉-触觉世界模型 | 触觉与多模态 | 3.63 | A | FULL |

Top10 均分 3.79；全部 CURRENT，无 OUTDATED/SUPERSEDED。同分排序规则：加权降序 →（value/IMP/NOV 全同组内）赛道多样性优先 → id 升序（六篇 3.85 并列、ACTS 与 EgoRayFormer 3.63 并列均按此裁决，见第五节）。

---

## 三、逐篇深度解读（按重要性降序）

### 第 1 章 · O-SCD++：递归证据融合的免回放在线场景变化检测（3.85 A）

**一句话结论**：免回放在线 SCD：PASLCD 上 mIoU 0.575 / F1 0.715、吞吐 25.6 FPS（为任一现有在线方法两倍以上），精度反超离线版 O-SCD（0.556/0.700）；CL-Splats 0.703/0.807、ChangeSim 0.474/0.605 均列第一。

**要解决的问题**：在线场景变化检测要求设备在持续建图中实时发现「场景本身变了」，但既有方法缺口明显：原始 ChangeSim 在 PASLCD 上 mIoU 仅 0.018；GeSCF 系与 SplatPose 系在线方法最高 0.237；离线 O-SCD 虽达 0.556 却无法在线运行，其在线版 O-SCD 回落到 0.489/0.643 且只有 11.8 FPS。需要同时免回放、免人工标注并保持高精度高速度的在线检测。

**方法详解**：O-SCD++ 采用递归证据融合：将当前帧线索（cue）与已累积的地图证据（map）加权融合（Eq. 17 两项，消融显示缺一不可：仅 cue 0.454 / 仅 map 0.526 mIoU，融合 0.575）。聚合权重使用有界质量函数（bounded weight, Eq. 13）替代无界质量 ρ_{g,t}=m_{g,t}（0.562→0.575）。决策规则用 exact scan 逐帧精确扫描阈值，替代固定 0.5 截断（0.522）与 Otsu（0.313）。方法同时具备 LF（免标注）、PA、MV（多视图融合）三项特性，为表中唯一三者齐备的在线方法，且无需回放历史帧。位姿前端基于 XFeat；附录 C 的改进——用参考地图渲染的深度提升参考关键点而非三角化——可把 ChangeSim 上 O-SCD++ 提到 0.558 mIoU。

**实验与结果**：PASLCD 主基准：O-SCD++ 0.575/0.715 @25.6 FPS，超过 ChangeSim（0.018/0.034 @11.5 FPS）、CS+CYWS2D（0.243/0.360）、CS+GeSCF（0.181/0.270）、FastGeSCF（0.122/0.198 @1.43 FPS）、SplatPose（0.173/0.281）、SplatPose+（0.237/0.358）与在线 O-SCD（0.489/0.643 @11.8 FPS），吞吐为任一现有方法两倍以上。CL-Splats：O-SCD++ 0.703/0.807 vs O-SCD 0.657/0.773；ChangeSim：0.474/0.605 vs 0.404/0.535（绝对精度受位姿前端限制，XFeat 在合成图上匹配失败、未注册图像得空 mask 拖低指标）。消融（PASLCD）：cue-only 0.454/0.595、map-only 0.526/0.676、map+cue 0.575/0.715；无界质量 0.562/0.701 vs 有界权重 0.575/0.715；固定阈值 0.522/0.671、Otsu 0.313/0.422、exact scan 0.575/0.715；oracle 上界 0.640/0.770。

**创新点**：① 递归证据融合：当前帧 cue 与累积 map 证据联合决策，在线免回放设置下达到甚至超过离线精度；② 有界聚合权重与 exact scan 阈值决策两个组件即插即用，各自带来可量化增益（+0.013 / +0.053 mIoU 相对被替代版本）；③ 在 PASLCD、CL-Splats、ChangeSim 三个基准上同时取得最高 mIoU/F1 与最高吞吐（25.6 FPS）。

**局限**：ChangeSim 上位姿前端（XFeat 对合成图像匹配不稳）成为瓶颈，需按附录 C 修改前端才能完全释放精度；对位姿估计失败敏感——未注册图像输出空 mask、IoU 记零；oracle 上界 0.640 表明融合策略仍有提升空间；digest 未给出失败案例的量化分析。

**与库内关系**：隶属「场景变化检测/在线建图」研究线：直接前身为离线 O-SCD（同表对比 0.556/0.700），与 SplatPose/SplatPose+（3DGS 系在线 SCD）、CS+GeSCF/FastGeSCF（GeSCF 系）构成同基准竞争；与库内动态 SLAM 线（2610.23496 FLoTS-SLAM）互补——后者解决动态几何的建图，本文化解决「场景静态结构本身发生变化」的检测与地图维护。

### 第 2 章 · SwitchSplat：从随手捕获场景学习离散物体状态（3.85 A）

**一句话结论**：从 Insta360 X4 随手拍摄的 12 个场景（10 个 casual + 2 个 golden）学习状态感知 3DGS：场景拆成共享静态基座 + 每物体一个 slot（on/off 双状态，softmax 至 1+2K 通道），推理时可自由组合捕获中从未共现的物体状态；slot 表由 VLM 初始化并经可微渲染端到端精化，全程无人工标注。

**要解决的问题**：既有动态场景表示（4DGS 等）以时间为条件，推理时无法自由组合物体状态；articulation 类方法又需额外结构假设。随手拍摄的 360° 视频中，交互物体的 on/off 状态与相机轨迹、时间纠缠在一起，缺少一种免标注、可自由状态组合的场景表示。

**方法详解**：① State-aware Gaussian Splat：每个高斯附加可学习 logit 向量 ℓ，softmax 到 1+2K 个通道——1 个 static base 通道 ℓ[0]，加每 slot 一对 off（ℓ[2k-1]）/on（ℓ[2k]）通道；每 slot 用双通道而非单通道，使 softmax 把每个高斯唯一指派到一个配置，不相交的高斯子集得以分别建模同一物体两种状态的几何与外观（关/开的门占据不同空间，单条共享基元无法表达）。渲染时用户指定各状态激活与否，按 Eq.(1) 计算每个高斯的出现概率 ω(p̃)。② Differentiable slot table：slot 由 VLM 初始化，训练时渲染联合精化。③ 训练目标含 sparsity loss 与 compactness loss，促使高斯指派稀疏、紧凑。预处理：FullCircle 抹除拍摄者、COLMAP 标定、双鱼眼去畸变为 pinhole；每第 8 帧留出测试，剔除状态切换瞬间的帧以降指标噪声（这些帧仍保留在训练集内）。

**实验与结果**：自采 Insta360 X4 双鱼眼 360° 数据集：standard set 10 个 casual 场景（8 室内 + 2 室外，每场景 3–9 次物体交互）；golden set 2 个场景带受控测试序列，评测 novel camera trajectories 与训练中未见过的 state combinations（泛化到训练配置之外）。基线：FullCircle（其 3DGUT 架构，静态）、4DGS、DeGauss（动态）。评估遵循标准 NeRF 流程（每 8 帧留出）。digest 未包含 Table 1 的具体数值。

**创新点**：① 把「场景状态」从「时间」解耦：slot + static base 分解使推理时可自由组合物体配置，包括捕获中从未共现的组合——这是时间条件动态方法（4DGS/DeGauss）根本做不到的；② 每 slot 采用 off/on 双 softmax 通道，保证两种状态由不相交高斯子集独立建模几何与外观；③ VLM 初始化 + 可微渲染端到端精化，全流程免人工标注。

**局限**：每物体仅支持二值状态（on/off）；slot 发现质量依赖 VLM 初始化；测试协议显式剔除状态切换帧，切换瞬间的渲染质量未被量化；golden set 仅 2 个场景，泛化结论统计力有限；digest 未报告与基线的定量对比数值。

**与库内关系**：隶属 NeRF/3DGS 场景表示线：静态基线 FullCircle/3DGUT、动态基线 4DGS/DeGauss；与库内 3DGS 效率/压缩线（2610.22778 dGS、2605.25563 CodecSplat）同属「3DGS 表示改进」但目标不同（状态可控性 vs 参数效率）；其 360° casual 捕获预处理（FullCircle、双鱼眼→pinhole）与全景内容线（2610.21297 GeoPano、2604.00852 PanoAir）共享采集处理流程。

### 第 3 章 · Stable Signer V3：4D 可变形基元泼溅用于手语生成（3.85 A）

**一句话结论**：4D 可变形基元泼溅的手语生产框架：SignSparK 补全词典检索稀疏姿态 + GUAVA 初始化表面绑定高斯化身；共享面部基元 + 测试时身份专属身体基元 + tunneling 超分三件套，使头部重建误差降 71.4%（1.267→0.362 mm）、10 个身份身体边界误差降 35.1%、高分辨率 RGB 重建误差降 24.2%，并保持交互式推理。

**要解决的问题**：手语生成（SLP）既要精细面部表情，又要身份专属的身体/外观适配与高分辨率渲染；既有管线（SignSparK 姿态补全 + GUAVA 高斯化身）缺乏共享表情几何与 per-identity 细节适配能力，而逐身份重训成本高昂。

**方法详解**：流水线：SignSparK 将词典检索的稀疏姿态补全为身体/手/脸控制 {q_t}；GUAVA 从参考图初始化表面绑定高斯化身；图像形成 Î_t = D_{ψ_s}(R_{π_t}[G_s(q_t; φ, θ_s)])，其中 φ 为共享面部控制器、θ_s 为身份专属身体适配。三模块：① 共享面部基元泼溅（FLAME 监督，用同一 articulation 的受限 FLAME 载体预测全表情目标，隔离待恢复的表情几何）；② 测试时身体基元泼溅；③ 测试时 Tunneling 超分解码器输出高分辨率 RGB。核心表示是 4D（姿态+时间条件）可变形基元：基元 k 有中心 c_k、正交框架 R_k、轴长 a_k 与归一化距离 d_k(x)=‖diag(a_k)^{-1}R_k^T(x-c_k)‖_4（水平集 d_k=1 为固定形状指数的超椭球）；稀疏场按 w_k(x)=exp[-2d_k(x)²]/Σ_j exp[-2d_j(x)²] 混合控制器预测的仿射残差：Δx_t=Σ_k w_k(x)[A_{k,t}(x_t-c_k)+b_{k,t}]；控制器零初始化保持几何，基元支撑在控制器学习期间固定，固定参考表面绑定保证绑定稳定。身份适配每身份仅一次，之后从存储参数驱动任意签名序列。

**实验与结果**：受控面部与身体研究用时间序 80/20 训练-评估划分、固定优化预算，checkpoint 仅用训练段选择；跨方法渲染用同姿态、同相机、同背景、同 crop，按身份聚合后 macro 平均。面部：GUAVA 跟踪 FLAME 序列上，平均头部误差 1.267→0.362 mm（-71.4%），面部误差 1.492→0.518 mm。身体适配：精修 RGB L1、边界 L1、SSIM，跨 10 个身份边界误差 -35.1%。渲染对比：前景 PSNR/SSIM/LPIPS。语义保持：对渲染视频重新提取姿态，固定回译评估 BLEU-4 与 ROUGE-L F1。运行时区分各阶段独立吞吐与驻留管线 wall time。digest 未包含逐项数值表。

**创新点**：① 把共享面部控制器与身份专属身体适配统一进同一可复用的 4D 可变形基元表示，表情控制与个性化渲染解耦；② 基于超二次曲面支撑的稀疏仿射残差混合，控制器零初始化 + 固定参考表面绑定，训练稳定、绑定不漂移；③ 身份适配与高分辨率细节恢复均在测试时完成（tunneling 解码器），免逐身份重训且保留交互式推理。

**局限**：面部载体为受限 FLAME（同一 articulation），表情几何恢复范围受限；论文 future work 明确要扩大 signer 与动作覆盖，并引入专业手语使用者评估——当前未经聋人/听障社群验证；digest 未报告与外部 SOTA 方法的定量对比表。

**与库内关系**：隶属「化身与人体」线：上游为 SignSparK（词典检索稀疏姿态补全）与 GUAVA（表面绑定高斯化身）；与库内 3DGS 化身族（LAM/GAGAvatar/FlexAvatar、2602.11693 OMEGA-Avatar、2610.23772 VDA）共享「参考资产初始化 + 姿态驱动」范式，区别在于本文化以「一次性身份适配 + 共享表情层」替代逐身份训练；与 SynerGest（2610.24031）互补——后者做对话伴随手势（语用级节律），本文化做手语（语言级精确动作）。

### 第 4 章 · DenseHap：单目图像的稠密手部触觉估计（3.85 A）

**一句话结论**：单张 RGB 单次前向同时输出逐顶点接触、距离与 3D 手部网格：在 18 个清洗数据集（1,162,799 样本）上训练，分布内平均 F1 超 HACO 3–5%，OOD 平均提升约 10%；吞吐约为「重建-接触级联」方案的 1.7 倍。

**要解决的问题**：稠密手部触觉（接触/距离/力）估计此前缺少统一的高质量训练数据与高效单阶段模型：公开手-物接触数据集质量参差（digest 审计 30 个数据集约 400 万样本，仅 18 个达标），级联管线慢，且对陌生分布泛化差。

**方法详解**：① 数据审计：设定质量控制标准，从 30 个数据集中剔除 10 个（GigaHands 标注不可靠、EgoTouch 手套手、InterHand2.6M 仅手-手、GRAB 无真实图像、HOT3D crop/侧向匹配错误、Open3DHOI 拟合后无接触、EgoPressure 接触-图像错位、HIC 手-手且测试仅 39 样本、PROX SMPL-X 映射不可靠、OpenTouch crop 错误），保留 18 个共 1,162,799 样本；ContactPose 与 EPIC-Contact 完全留出仅作测试。② 架构：三个参数独立的 vertex-query cross-attention trunk（接触/距离/网格）挂到静态 WiLoR 骨干，用多损失设计应对类别不平衡，单次前向输出 per-vertex contact、distance 与 MANO 网格。

**实验与结果**：稠密接触（Skip 协议、逐顶点 F1、各自最优阈值）：MOW .571（距离头）/ContactPose .675/EPIC .524/ARCTIC .713/RICH .799/Hi4D .424；对比 HACO（.522/.599/.459/.684/.781/.474），分布内平均 +3–5%，OOD 平均约 +10%（Hi4D 例外，.424 低于 HACO .474）。距离：ARCTIC 上 778 个 MANO 顶点、截断 100 mm 的 H→O 距离 MAE：<10 mm 3.70（InterField-SF 7.92）、10–20 mm 4.12（7.62）、≥20 mm 16.21（10.51）；近场优化契合多数数据集 10 mm 接触阈值。定性：BSTRO/DECO 接触估计粗糙，HACO 常不分掌背且受离群样本干扰；DenseHap 在过暗/歧义图像上仍吃力。

**创新点**：① 迄今最系统的手-物接触数据集审计（30→18、116 万样本统一语料，排除理由全部公开）；② 三个参数独立 vertex-query cross-attention trunk + 静态 WiLoR 的单阶段多任务架构，接触/距离/网格一次前出；③ 近场距离专门优化 + 类别不平衡多损失设计，带来分布内 3–5%、OOD 约 10% 的 F1 提升与 1.7× 吞吐。

**局限**：严重遮挡下性能显著下降；过暗/歧义图像估计不稳；≥20 mm 远场距离不如 InterField（16.21 vs 10.51 MAE）；Hi4D 上仍未超过 HACO；力（pressure）预测的完整评估在 digest 结论段被截断。

**与库内关系**：隶属「触觉与多模态」研究线：与 2608.15060 EgoTac、2610.22748 ElectroCalm、同批 2610.24257 XRT 构成触觉感知族；骨干 WiLoR 同时是 V-JEPA Hand（2610.26780）的基线与 EgoXperience（2610.26625）的对比方法，三文共同勾勒第一视角手-物感知栈；其 10 mm 接触阈值与 ACTS（2610.24285）的力感知动作编码形成「图像域触觉推断」与「传感级触觉」的互补。

### 第 5 章 · EgoXperience：从人类经验学习世界锚定的第一视角表征（3.85 A）

**一句话结论**：统一端到端在共享度量世界系重建相机、稠密深度、双手与刚体 6-DoF 位姿：HOT3D 手部 PA-MPJPE 3.70 mm（次优 HaWoR 6.06）、物体 ADD 28.00 mm（次优 Any6D 67.06）；配套 EgoX-Engine 为 50 小时 EgoX-Data-6M 提供对齐多模态标注，并策划留出 1 小时 EgoX-Bench。

**要解决的问题**：第一视角手-物 4D 重建长期被拆成相机 SLAM、深度、手重建、物体位姿多个级联模块，误差沿链路累积且世界系尺度不一致；同时缺少大规模、几何对齐的多模态第一视角训练数据，也缺少单一模型联合输出全部量的能力。

**方法详解**：三段式：任务驱动采集（task-driven capture）+ 几何对齐标注（EgoX-Engine）+ 联合重建。EgoX 在 EgoX-Data-6M（50 小时）标注与 harmonized 公开数据集上训练，单模型输出相机、稠密深度、MANO 手、刚体物体 6-DoF 位姿，共享度量世界系。输入仅 RGB + 首帧物体 mask（物体基线常另需估计深度、内参、逐帧 mask 或度量 CAD）。评测用 HOT3D/EgoX-Bench/H2O/HOI4D 统一 150 观测 clip，评估序列排除于训练之外；世界系手指标用各方法自身估计相机，物体位姿在相机系评估；主对比不喂 GT 相机位姿或尺度。

**实验与结果**：手重建（mm）：HOT3D PA-MPJPE 3.70 / WA 15.54 / W 38.89，全面优于 HaWoR（6.06/29.80/56.30）、MINT（9.94/37.76/85.85）、ReViV（14.01/49.90/109.02）、WiLoR+SLAM（5.90/25.52/58.55）、HandFlow（5.54/59.01/119.48）；EgoX-Bench PA 4.64（次优 8.51）、HOI4D PA 3.32、H2O PA 4.97/WA 11.41/W 23.95。物体位姿（ADD/ADD-S mm、AUC-S50 %）：HOT3D 28.00/14.03/73.71 vs Any6D 67.06/44.05/42.99、FoundationPose 92.49/59.87/23.32、GigaPose+MegaPose 71.92/32.42/57.59；EgoX-Bench ADD 27.11、HOI4D 44.55、H2O 22.10。Table 4 相机/深度对比含 VGGT、VGGT-Ω、CUT3R、Any4D、DA3 Nested 等（HOT3D nATE：VGGT-Ω 0.0018、DA3 Nested 0.0036），但 EgoX 行未包含在 digest 内；论文自述深度估计亦强。

**创新点**：① 本对比中唯一在同一世界系端到端联合输出相机+深度+双手+物体 6-DoF 的方法（digest 原文如此表述）；② EgoX-Engine：任务驱动采集 + 几何对齐多模态标注流水线，产出 50 小时 EgoX-Data-6M 与留出 1 小时 EgoX-Bench；③ 统一 150-clip 匹配协议（不喂 GT 相机/尺度），使相机/深度/手/物体四类结果可同台比较。

**局限**：假设刚体物体且不预测物体 mesh（列为 future work）；仅单目 RGB 输入（多视图输入亦为 future work）；EgoX-Bench 为作者自建，独立第三方基准仍缺；Table 4 的相机/深度定量结果未在 digest 中呈现。

**与库内关系**：隶属「第一视角」研究线：与 2610.22681 EgoP²C 同属第一视角表征学习；其基线中的 WiLoR 同为 DenseHap 骨干与 V-JEPA Hand 基线，相机/深度对比中的 VGGT/VGGT-Ω/CUT3R/Any4D/DA3 直通库内几何基础模型线（2602.07891 SAGE、2610.23039 VGGT+TokenGS、DA3）——本文化可视为把 VGGT 式几何基础模型扩展到「人手-物联合世界系」的一步，与 V-JEPA Hand（2610.26780，专注手+相机）同批互补。

### 第 6 章 · V-JEPA Hand：从第一视角视频恢复 3D 手部与相机轨迹（3.85 A）

**一句话结论**：单次前传从第一视角视频同时恢复双手 MANO、相机运动与焦距：HOT3D 上 PA-MPJPE 5.72 mm vs WiLoR 7.57 / HaWoR 7.64，EP 5.71 vs 22.11 / 8.16，Jit 5.74 vs 17.19 / 13.41；ARCTIC 上 PA 6.59 mm；全程无需手部检测与 SLAM。

**要解决的问题**：第一视角双手重建在严重遮挡（ARCTIC）与运动模糊（HOT3D）下退化，既有管线依赖手部检测 + 跟踪/SLAM 多级串联，世界系误差随相机估计漂移；缺少一个简单、快、且联合输出手部与相机轨迹的单阶段模型。

**方法详解**：V-JEPA 2.1 自监督视频编码器把 clip 编码为时空 token grid；query-based trajectory predictor（ViT）联合处理这些特征、每帧一个可学习 hand-pose query 与一个 intrinsics token，每帧输出双侧 MANO 姿态、手存在概率、相机运动与焦距，整个 clip 一次前传完成重建。训练为单阶段 + 多源监督：大规模伪标注视频与高质量数据共享同一训练目标；损失项含手部参数、前向运动学、重投影、时序平滑、手存在、相机运动与内参（附录 D 给细节）。

**实验与结果**：三基准：ARCTIC（严重遮挡下的双手操作）、HOT3D（快速头手运动模糊，HaWoR 验证划分约 49 分钟）、EgoStandard（商业标注多样场景约 60 分钟，完全排除于训练外测泛化）。ARCTIC：Ours PA-MPJPE 6.59 vs WiLoR 6.70、HaMeR 9.44、HaWoR 9.07、WildHands 9.55；EP 8.85 vs 28.84/18.67/16.24/16.05。HOT3D：PA 5.72 vs WiLoR 7.57、HaMeR 10.26、HaWoR 7.64、WildHands 12.40；EP 5.71 vs 22.11/36.35/8.16/38.82；GO 6.52 vs 16.49/36.35/10.50/38.82；Jit 5.74 vs 17.19/21.09/13.41/25.30；Acc 0.971 / Rec 0.979 / F1 0.980。注意 Jit 上 ViDiHand 更低（HOT3D 3.74 vs 5.74；ARCTIC 3.18 vs 6.09）。定性：低光、户外修剪、绘画、水槽等场景中三个基线全部漏检时仍能重建双手。消融：伪标注数据、损失项、预训练与时序上下文、编码器选择；模型规模与推理成本见 Sec 4.4（digest 未含数值），EgoStandard 的 Ours 行亦未包含在 digest 内。

**创新点**：① 把 V-JEPA 2.1 视频表征用于「手+相机」联合轨迹恢复，一次前传出双手 MANO、相机运动与内参；② query-based predictor（每帧一个 hand-pose query + intrinsics token）免去检测/SLAM 级联；③ 大规模伪标注 + 高质量数据的多源单阶段监督，在遮挡/模糊/未见数据上相对 WiLoR、HaMeR、HaWoR、WildHands 全面领先（coverage-aware 评估协议）。

**局限**：世界系指标依赖自身估计的相机轨迹，尺度误差会传导；依赖 V-JEPA 2.1 预训练与大规模伪标注数据的质量与规模；digest 未给出模型规模/推理速度数值与失败模式量化；Jit（抖动）指标上不及 ViDiHand。

**与库内关系**：隶属「感知与认知」第一视角人体感知线：与 EgoXperience（2610.26625）同批互补——后者联合相机+深度+手+物体，本文化专注手+相机轨迹；基线 WiLoR 同为 DenseHap 骨干与 EgoX 基线，三文构成「第一视角手-物-相机」同题竞争；V-JEPA 2.1 编码器属 JEPA 式自监督视频表征路线，与库内几何基础模型线（VGGT 系、2602.07891 SAGE）并列「自监督大模型 + 查询式解码」范式。

### 第 7 章 · Spatons：空-色调局部化神经算子用于高效 XR 预畸变补偿（3.78 A）

**一句话结论**：空-色调局部化神经算子：G-Res 在混合几何畸变场景 PSNR 37.5 dB / SSIM .987（Sc.3）、34.9 dB / .975（Sc.4），领先全部 UNet++ 变体约 8 dB，以约 250× 更少参数把与 CompenNet++ 的差距压到约 1.5 dB；公式无关模式下 8.5K 参数 NN2 在真实投影仪-相机数据上把约 10.3 dB 基线拉到 22.23 dB / 0.816 SSIM。

**要解决的问题**：XR 近眼显示/投影需要实时预畸变补偿（预先扭曲待显示图像以抵消光学畸变），但真实畸变是几何与色调在空间上非均匀耦合的，且常缺少可微畸变公式导致无法反传训练；既有学习式补偿网络（CompenNet++、Patch2Pixel、UNet++）参数量大，难以部署在端侧。

**方法详解**：Spatons 用空-色调局部化神经算子直接学习补偿映射，几何变体 G-Res/G-Hybrid 处理 keystone/fisheye/barrel 等几何畸变，C-Res 处理色调畸变。核心是两阶段公式无关方案：先从图像对拟合一个 forward-mimic 网络 NN1，再把可部署的 NN2 通过冻结的 NN1 训练，从而摆脱对手工可微畸变管线的依赖。训练用 AdamW + cosine annealing + warm restarts + AMP（Images.cv 256×256：batch 32、lr 1e-3→min-lr 1e-6、weight decay 1e-4、warmup 5 epochs、100 epochs）。论文另含视频预畸变、量化分析与解析式资源/时延模型。

**实验与结果**：Images.cv（26k 图、3×256×256、70/15/15 划分）为主基准，CelebA-HQ（28k 人脸）做零样本跨数据集测试。Sc.1/2（色调混合：色平衡、亮度对比、 elevated black、暗角、模糊、色边等）：C-Res 22.3/21.4 PSNR，Patch2Pixel-v2 (p=3) 27.4/23.0，UNet++-Large 29.4/23.5，CompenNet++ 29.4/23.3。Sc.3/4（几何混合 keystone+fisheye / keystone+barrel+fisheye）：G-Res 37.5/34.9 PSNR（SSIM .987/.975）、G-Hybrid 37.4/34.8、UNet++-Large 29.2/28.7、CompenNet++ 39.1/36.3；G-Res 领先全部 UNet++ 约 8 dB PSNR，以约 250× 更少参数进入 CompenNet++ 约 1.5 dB 内。公式无关验证：Sc.5 全空-色调下 8.5K 参数 NN2（经冻结 CompenNet++ mimic 训练）达 26.59 dB / 0.926 SSIM，距已知公式上界 0.9 dB 内；真实投影仪-相机数据（Huang and Ling 2019，lavender_np，700 对）从约 10.3 dB 提到 22.23 dB / 0.816 SSIM；空间非均匀四区域算子（keystone/fisheye × blur/contrast）下同样有效。

**创新点**：① 空-色调局部化神经算子统一处理几何+色调耦合畸变（G-Res/C-Res 家族），在混合场景大幅超越通用 UNet++ 架构；② 两阶段「先拟合 mimic、再蒸馏可部署小网」方案摆脱对可微畸变公式的依赖，任意黑盒光学系统均可被补偿；③ 8.5K 参数即可在真实数据上取得约 +11.9 dB 的修正，比 mimic 小 2–3 个数量级，面向端侧实时。

**局限**：主基准为 256×256 合成数据，更高分辨率/更多数据集的适用性见附录但 digest 未给数值；真实数据验证仅一个投影仪-相机数据集（700 对）；公式无关模式需先训练 NN1 mimic，两步流程增加部署前成本；digest 未报告在头显实际光学链路上的端到端验证。

**与库内关系**：隶属「渲染与显示」XR 显示补偿线：与基线 CompenNet++/Patch2Pixel-v2/UNet++ 同属学习式预畸变家族；其「大模型冻结为 mimic、小网蒸馏」思路与库内 3DGS 效率/压缩线（2610.22778 dGS、2605.25563 CodecSplat 的紧凑/前馈参数化）共享「大模型→可部署小模型」范式；与全景内容线（2610.21297 GeoPano、2604.00852 PanoAir）目标不同——本文化解决显示端光学畸变补偿而非内容生成。

### 第 8 章 · PhysSkin++：自监督神经蒙皮的实时可泛化物理动画（3.77 A）

**一句话结论**：从静态几何自监督学习连续神经蒙皮场（LBS 式 m 个仿射位移加权和）并在降阶子空间做隐式时间积分：一个框架跨多样 3D 形状与离散化实现实时物理动画，支持 mesh 顶点/点云/3D Gaussian 三种绑定与 rig 互补控制；为会议版 PhysSkin 的四方面扩展。

**要解决的问题**：经典全空间物理动画中，显式时间积分受稳定性条件限制，隐式积分需在高维全空间解大规模非线性优化，难以实时；会议版 PhysSkin 在可控性、碰撞与离散化绑定上受限。缺少一种免观测数据、可泛化到新形状的实时物理动画方案。

**方法详解**：① Neural Skinning Fields Autoencoder：transformer 形状编码器处理表面点得到 shape latents，可学习 query 经 cross-attention 提取 handle latents，空间 query 再经 cross-attention 得到 point-wise 特征，解码为连续蒙皮场；变形映射为 LBS 式 φ(X,z)=X+Σ_{i=1}^{m} W_i(X) Z_i [X;1]（m 个仿射位移变换的加权和）。② PISSL（Physics-Informed Self-Supervised Learning）：on-the-fly 蒙皮场归一化 + conflict-aware 梯度校正，稳定联合优化多个自监督损失，仅需静态几何、无观测数据。③ 运行时仅推进降阶子空间坐标的隐式时间积分，降低成本实现实时；动力学公式可控且碰撞感知，支持 Dirichlet 边界条件、交互控制、环境交互与多物体接触。④ Rig-complementary：以 rig Jacobian 定义 rig 空间互补项，在交互 rig 控制与用户 authored 动画下产生互补弹性响应，运行时无需强制执行该约束。⑤ 连续变形映射可绑定到 mesh 顶点、采样点与 3D 高斯表示。

**实验与结果**：论文称在多个数据集上评估所学蒙皮场，并演示跨多样形状、控制、交互与空间离散化的实时物理动画；digest 未包含定量表格与具体数值。

**创新点**：① 用 transformer + cross-attention 自动编码器从静态几何预测连续蒙皮场，实现跨形状泛化；② PISSL 的 on-the-fly 归一化与 conflict-aware 梯度校正解决多自监督损失联合优化的稳定性；③ 可控且碰撞感知的降阶动力学 + 离散化无关绑定（mesh/点云/3D Gaussian）；④ rig 空间互补项使物理动画与既有 rig 管线共存，无需运行时强制约束。

**局限**：digest 未提供定量结果与独立局限章节；从表示形式看，形变被约束在 m 个仿射变换张成的降阶子空间内，剧烈非线性形变可能超出子空间表达能力；交互控制与接触依赖降阶动力学的数值设置，其量化表现未经 digest 验证。

**与库内关系**：隶属「化身与人体」物理动画线：前身为会议版 PhysSkin（digest 明确本文为其四方面扩展：可控降阶动力学等）；与 3DGS 化身族（LAM/GAGAvatar/FlexAvatar、2602.11693 OMEGA-Avatar、2610.23772 VDA）互补——后者重外观渲染，本文化重物理一致的形变与接触；其「可绑定 3D Gaussian」的接口是把物理动画接入实时神经渲染管线的直接切入点，与 Stable Signer V3（2610.24926）的测试时适配同属「免重训角色部署」思路。

### 第 9 章 · SynerGest：双人对话的时空协同手势生成（3.72 A）

**一句话结论**：双人对话的协同手势生成（ACM MM '26 接收）：以 Contrastive Flow Matching 联合条件于听者与说话者的 48kHz 双声道语音，在 Audio2Photoreal 与 Seamless Interaction 两个双人对话数据集上，以 FGD/BC/Div/推理耗时 T_inf 四项指标对比 4 个基线（EMAGE、GestureLSM、TalkSHOW 与唯一双人基线 A2P）。

**要解决的问题**：共语手势生成既有工作几乎全是单人说（monadic）设定，忽略对话中听者与说话者的交互节律；双人设定缺少联合建模双方音频、并显式控制「动什么 / 何时动」的生成框架。

**方法详解**：① 条件生成：listener 与 partner 两路原始波形经冻结 AudioRhythm Encoder 独立处理并拼接为基础声学特征 F_a（wav2vec 2.0 骨干 + mel 特征，双通道独立）；为适应不同动力学特性，flow estimator 分离身体与表情双通路（PoseOnly / FaceOnly）。② Guide Transformer 从音频自回归预测离散 RVQ token，解码为引导关键帧（guide key-frame generation）。③ Dyadic-conditioned flow estimator：学习步长条件速度场 v_θ(x_t,t,d,c)，把高斯先验传输到经验分布；固定初始噪声与音频时从 t=0 积分到 1 得确定性 ODE 轨迹，更换初始样本则得到同一音频的另一个合势力势（context injection 与 condition vector 投影注入对话条件）。④ ITSA（Impulse-Trend Synergistic Attention）：Trend Feature Gating 决定「动什么」、Impulse Temporal Gating 决定「何时动」，再加可学习软混合 MHA。⑤ 训练目标为 Contrastive Flow Matching。

**实验与结果**：数据集：Audio2Photoreal（工作室录制双人对话 + 写实 Codec Avatar 资产，48kHz 双声道分别含说话者/听者波形）与 Seamless Interaction Naturalistic 子集（无脚本自发录制，单声道按参与者配对、重采样 48kHz、对齐时长后堆叠为双声道）。指标：FGD（动力学真实感）、BC（Beat Consistency，音频-动作同步）、Div（动作方差）、T_inf（每样本平均推理耗时）。基线：EMAGE、GestureLSM、TalkSHOW（三个单人说框架适配到双人协议）+ Audio2Photoreal（A2P，唯一双人基线），同数据处理公平对比。digest 未包含 Table 1 的具体数值。

**创新点**：① 面向双人对话的 CFM 手势生成框架，联合条件于听者/说话者双方音频；② 身体/表情解耦双通路 + Guide Transformer 的 RVQ 关键帧引导；③ ITSA 显式分解「动什么」（trend gating）与「何时动」（impulse temporal gating）；④ 步长条件速度场支持确定性 ODE 推理与同音频多样化采样。

**局限**：目标化身建模为 listener 角色（joint-modeling 场景下），speaker 侧生成未覆盖；依赖对话双方音频的配对与时间对齐；digest 未报告定量结果与运行时数值，也未给出失败模式分析。

**与库内关系**：隶属「化身与人体」手势/表情动画线：基线 EMAGE/GestureLSM/TalkSHOW/A2P 均为共语手势生成代表，A2P 的 Codec Avatar 资产与库内 3DGS 化身族（LAM/GAGAvatar/FlexAvatar、2602.11693 OMEGA-Avatar）同属「参考资产驱动」路线；与 Stable Signer V3（2610.24926）互补——后者做手语（语言级精确动作），本文化做对话伴随手势（语用级节律），可与 SynerGest 的输出共同驱动 XR 社交化身。

### 第 10 章 · ACTS：从人类物理交互学习视觉-触觉世界模型（3.63 A）

**一句话结论**：完全从人类物理交互训练的视觉-触觉世界模型：联合预测场景视频、双手腕视角与 GelSight 触觉共 5 路未来观测（8 帧条件→8 帧预测，0.53 s @15fps），论文结论称场景视图预测优于 ContactWorld 与 VT-WM 两个视觉-触觉基线，并不经微调零样本迁移到机器人 episodes。

**要解决的问题**：既有视觉-触觉世界模型多在机器人数据上训练，成本高、域窄；人类物理交互数据丰富，但缺少把「触觉传感器处的动作（运动 + 力变化）」与世界模型未来预测统一起来的框架，且从人类到机器人的跨本体迁移未被验证。

**方法详解**：观测流 M={V, W^L, W^R, T^L, T^R}（俯视场景 RGB、左右腕相机 RGB、左右 GelSight 触觉），建模 p_θ({X_F^m} | {X_H^m}, A)。编码：场景与两路腕相机共享预训练 Wan2.2 causal VAE 编码器（冻结），两路 GelSight 共享适配自建视觉-触觉数据集的变体（冻结）。动作表示含 force-aware sensor actions（运动 + 力变化）与 view-aligned actions（编码接触相关运动与场景视角传感器几何）；统一序列构建含时空对齐与全窗口动作条件。

**实验与结果**：在 React 数据上从零训练两个基线：ContactWorld（官方代码适配的 JEPA 式无解码器模型）与 VT-WM-style（复现其自回归 latent predictor + 动作条件接口）；Dream-Tac 因联合生成动作且要求机器人相机布局/本体感而无法适配。协议：8 观测帧（ContactWorld 为其原生 1 帧上下文）+ 记录动作 → 预测后 8 帧（0.53 s @15fps），按流（场景/腕×2/GelSight×2）分别报告 PSNR/SSIM/LPIPS，参考帧由冻结 VAE 从 GT latent 解码，相同测试窗与种子。评测：留出人类录制 + 机器人 episodes 零样本迁移（不微调）；机器人动作由 OptiTrack 传感器位姿 + GelSight 估计力构建——前向运动学每步平移与 OptiTrack 中位差 0.33 mm（约每步运动中位的一半），机器人数据需按人类数据归一化触觉颜色/光照与腕相机色调。digest 结论段被截断（「predicts the scene view better than two visuo-tactile base…」），具体数值未包含。

**创新点**：① 完全从人类物理交互数据训练视觉-触觉世界模型，动作定义在触觉传感器处（运动 + 力变化）；② 五路观测（场景 + 双手腕 + GelSight×2）在共享/适配 VAE 的统一 latent 预测框架下联合预测，全窗口动作条件；③ 人→机器人零样本迁移验证，并以 0.33 mm 中位差保证动作域一致。

**局限**：digest 结论段被截断，定量结果不完整；机器人迁移前需颜色/光照归一化，域差处理是隐式前提；动作定义依赖 OptiTrack + GelSight 硬件，裸相机器人数据不适用；ContactWorld 仅用 1 帧上下文（其原生设定），比较强度受协议差异影响。

**与库内关系**：隶属「触觉与多模态」世界模型线：与 2608.15060 EgoTac、2610.22748 ElectroCalm、同批 2610.24257 XRT 构成触觉感知/建模族；基线 ContactWorld（JEPA 式）与 VT-WM 为视觉-触觉世界模型代表；其 GelSight 触觉流与 DenseHap（2610.26583，图像域触觉估计）分别代表「传感级触觉」与「视觉推断触觉」两条互补路线；Wan2.2 causal VAE 编码器与视频生成/世界模型管线衔接。

---

## 四、当日全量 7 维度对比表（31 篇入馆）

见 [papers/daily/2026-10-21/7dim-table.md](../papers/daily/2026-10-21/7dim-table.md)（含 IMP/NOV/TEC/EXP/PER/TRL/REP 分明细、总分、等级与证据列）。分布：S×0 / A×11 / B×15 / C×5；除 Holi-World（2610.26549，PARTIAL/L1 摘要级）外全部 L0/FULL。

---

## 五、覆盖率校验与筛选过程说明

**候选来源**：RSS 7 分类去重 1426 条 → KW 双层过滤（全称子串 + 缩写词边界）命中 91 → 去 registry(512) 后 67 新 = 67 篇真新提交 + 20 篇旧稿 replace/cross + 4 篇库内 v2 再公告；67 篇真新中 31 篇 XR 入池。公告窗口内剔除 36 篇非 XR/弱相关：医学×3（MRI 超分/动脉瘤分割/胶质瘤合成）、自动驾驶×2、机器人×20+（灵巧操作/导航/规划/动捕/人形）、无人机×2、通用视频生成×3、通用具身/NLP/气象/几何/推荐系统等。listing 对账（10-20 日组 936 篇 API 摘要级过滤命中 63 篇）与 RSS 通道完全互证；10-19 日组摘要级命中 7 篇全部非 XR（与 10-20 运行结论一致）。

**三关结果**：
- 门① 同质去重：最高 Jaccard **0.143**（2610.24285 ACTS vs 库内 2609.22332）→ **通过，无重筛**。
- 门② 赛道覆盖：Top10 覆盖 **5 赛道**（感知与认知×3、化身与人体×3、触觉与多模态×2、神经渲染×1、渲染与显示×1）→ **通过**；全批 31 篇覆盖 12 赛道。
- 门③ 价值天花板：库内近 30 天（date≥2026-09-21）Top10 均分 = **4.416**（现算：2610.03162 4.65 / 2610.03283 4.58 / 2610.19674 4.57 / 2610.23772 4.57 / 2609.34367 4.37 / 2610.18872 4.3 / 2610.22778 4.3 / 2610.03192 4.28 / 2609.34817 4.27 / 2610.17474 4.27）；当日最高 **3.85** → 差值 -0.566，**非重磅日，无 S 级，未拔高**。

**筛选过程修正记录**：本批评分基于全文证据定稿（先抓全文再定稿）。① 六篇 3.85 并列（IMP/NOV 全同）按赛道多样性优先裁决入场顺序，感知与认知以 3 篇封顶 Top10（O-SCD++/EgoXperience/V-JEPA Hand），EgoRayFormer（3.63，同分第四席感知与认知）让位 ACTS（触觉与多模态）；② Holi-World 因全文获取失败（L0 HTML 404、ar5iv 仅返摘要页）按摘要级评估定 3.20 B，并在 7 维表/scored/笔记三处显式标注 PARTIAL，未脑补正文；③ 36 篇剔除中机器人域占比最高（20+ 篇），反映 10-20 公告日机器人论文泛滥，与既往口径一致（纯机器人域不纳入 XR 文献库）。

---

## 六、backfill-1021 专章（10 篇：4 A / 5 B / 1 C，非当日新提交）

**来源与诚实口径**：RSS 旧稿 replace/cross 再公告 20 篇（2504~2609 原始提交）中甄别 10 篇 XR 相关首次入馆；其余 10 篇非 XR 剔除（人形控制/自动驾驶/视频可操作神经函数/多机器人空间推理/人形世界模型/机器人意图跟随/零样本智能体/NLP/高光谱超分）。**全部非当日新提交，单列 backfill-1021，未混入主批 Top10**。

**排行**（按加权降序）：OmniEgoCap 3.85 A（设备无关序列级第一视角动作重建，扩散框架+8×A5000 16h）· ZipSplat 3.85 A（62K 高斯 25.34 PSNR，比 per-pixel 基线高约 2dB）· GraFT 3.85 A（免训练 3D 场景图 MLLM 空间推理，GPT-o3 VSI-Bench +5.9）· GaussTrap 3.72 A（KDD 2026，3DGS 隐蔽后门攻击）· Mono-Hydra++ 3.45 B（ISPRS JPRS，单目实时场景图 ATE 6.91cm）· PRISM 3.43 B（扩散蒸馏为前馈单图重建）· OUGS 3.43 B（FIM+EMA 不确定性驱动主动视角选择）· MAGS-SLAM 3.08 B（单目多智能体 GS SLAM）· Vibe Coding XR 3.00 B（XR Blocks+Gemini 原型工具链）· SGM-SLAM 2.93 C（场景图匹配分布式 SLAM，感知消息压缩 65×）。

**覆盖三关**：门① max Jaccard **0.133**（通过）；门② 覆盖 **4 赛道**（感知与认知×2、神经渲染×4、重建与SLAM×3、空间计算与UI；backfill 为机会性补录，不适用 Top10 选拔）；门③ 不适用。无重筛、无 OUTDATED。全文 10 篇全部 L0/FULL。

**关键互证**：① ZipSplat × FineSplat × 库内 pixel-aligned 族——前馈 3DGS「token 粒度/基元数量」效率竞合三线；② Mono-Hydra++ × SGM-SLAM——「场景图建图-通信」互补对，与库内 OpenSplatGraph 同属 3D 高斯语义场景图线；③ GraFT × 库内 SpatialMind——「免训练 vs 微调」MLLM 空间推理对照；④ GaussTrap 开库内 3DGS 安全视角；⑤ OmniEgoCap × 库内 EgoWholeView/OmniPoser/ESTHER——第一视角动作重建族新变体。

详见 [MOC-backfill-1021](../papers/MOC/MOC-backfill-1021.md)。

---

## 七、附录

**证据等级分布**：主批 31 篇 = **30 篇 FULL**（L0，26,060–141,031 字符）+ **1 篇 PARTIAL/L1**（2610.26549 Holi-World，L0 HTML 404、ar5iv 仅返摘要页 5177 字符，按摘要级评估）；backfill 10 篇全部 FULL（L0）。

**抓取失败/降级清单**：仅 Holi-World 一篇降级（上述），手动重试 L0 HTML 确认 404 后按摘要级评估并三处显式标注；无限流封禁、无伪造；manifest 合并写入校验通过。XRT（2610.24257）digest 提取不完整（LaTeXML 样板），其笔记改用 arXiv 官方摘要补全并在 limits 中如实说明。

**诚实口径声明**：本批公告窗口 2026-10-20（周二释放，09-28~10-19 提交），拉取日 2026-10-21——**公告日≠拉取日**；backfill-1021 为旧稿 replace/cross 再公告补录（原始提交 2025-04 ~ 2026-09），非当日新提交。所有 registry 条目带 `batch=2026-10-21` / `batch=backfill-1021` 与 `orig_window` 字段，backfill 条目 flags 含 `BACKFILL`。

**产物清单**：本报告 + [当日 MOC](../papers/MOC/MOC-2026-10-21.md) + [backfill MOC](../papers/MOC/MOC-backfill-1021.md) + 原子笔记 41 篇（主批 31 + backfill 10）+ [主批 7 维表](../papers/daily/2026-10-21/7dim-table.md) + [主批评分明细](../papers/daily/2026-10-21/scored.md) + [执行日志](../papers/daily/2026-10-21/run_log.md) + [backfill 7 维表](../papers/daily/backfill-1021/7dim-table.md) + [backfill 评分明细](../papers/daily/backfill-1021/scored.md) + registry 追加 41 条（512→553，备份 `registry.jsonl.bak-20261021`；另 `registry.jsonl.bak-20261021b` 为 in_top10 修正前备份）+ [MOC 总索引刷新](../papers/MOC/MOC-总索引.md)。
