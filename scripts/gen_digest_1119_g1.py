# -*- coding: utf-8 -*-
"""生成 data/digest_1119_g1.json —— XR 论文雷达 2026-11-19 g1 组（6 篇）全文精读 digest。

全部内容仅取自 data/fulltext/2611.21642|21690|21802|21938|22095|22146.txt（arXiv HTML 正文）。
"""

import json
import os

W = {"IMP": 0.20, "NOV": 0.20, "TEC": 0.15, "EXP": 0.15, "PER": 0.15, "TRL": 0.08, "REP": 0.07}

DIGEST = {}

# ---------------------------------------------------------------- 1. RelicTouch
DIGEST["2611.21642"] = {
    "id": "2611.21642",
    "title_en": "RelicTouch: Exploring Fingertip Vibrotactile Feedback for Image Interpretation",
    "title_zh": "RelicTouch：探索用于图像解读的指尖振动触觉反馈",
    "track": "触觉与多模态",
    "problem": "现有触屏触觉增强研究大多把振动反馈当作材质模拟（roughness、compliance），隐含假设触觉应逼近真实材料，因而难以承载复杂图像内容的空间结构。同时，用户在没有视觉通道辅助时如何在连续触屏探索中解读被编码的振动信号、信号参数与手指配置如何共同决定可读性，仍缺少证据。以往参数研究多针对孤立刺激或离散辨别任务，与“边移动边比较”的图像探索情形不同。",
    "method": "RelicTouch 由 10.1 英寸 Android 平板端的触摸采集、主机侧处理模块与三枚 10×10×4 mm LRA 组成，执行器贴于手指背侧以保留指腹直接接触屏幕；触摸事件被转成“执行器 ID + PWM 强度”的文本指令，经串口送入 Arduino Uno 再分发到对应 LRA，多点触控时每个触点绑定独立触觉通道。系统在滑动过程中按图像导出的特征实时调制振动强度：更显著或边缘更丰富的区域给更强反馈，平坦区域给更弱反馈，使线索保持 movement-contingent 并与图像空间位置绑定。作者先用 MPU6050 加速度计在自由振动与指-面接触两种条件下标定六个 PWM 档位的 RMS 加速度（约 0.04→1.75 g 与 0.04→1.63 g），确认单调性后再做阈值预实验（12 人），确定 35 PWM 为最低可辨强度、25 pseudo-height 为最小可辨点距、15 单位为区分间距差的近似下界。Study 1 为控制变量主体内实验：20 名被试 × 6 强度 × 3 间距 × 3 手指配置（单指 / 双指 / 三指，LRA 贴于食指、中指、无名指），每人 54 trials，任务是口头报告触觉-视觉一致性最高的图像编号，并使用贝叶斯 bootstrap（Dirichlet 加权重采样）估计选择概率热图，问卷为 8 项 7 点 Likert（含反向计分题）。Study 2 用 8 名领域专家做探索性质性研究：每个触控像素按 BT.709 计算亮度并归一化，用 inverse luminance 定义 pseudo-depth D=1−L_norm^1.5，再叠加 3×3 Sobel 梯度项，参数固定为 P_d=1.5、S_e=0.35、G_thresh=80、I_flat=35、I_min=15、I_max=255 且不随图像调参。三个活动（盲触描述、引导式图像探索、体验与设计批评）共约 60 分钟，录音转写后用 affinity diagramming 由两名作者独立编码并归纳主题。",
    "key_results": [
        "Study 1（n=20）：三种手指配置的总体主观评分差异显著，Friedman χ²(2)=19.18, p<.001, Kendall's W=.48；单指 M=5.48 (SD=.70) > 双指 5.08 (.58) > 三指 4.49 (.88)，Holm 校正 Wilcoxon 两两比较 p=.003（r=.72）、p=.001（r=.78）、p=.003（r=.74）。",
        "Study 1 选择概率热图：双指与三指在 79 PWM × 65 pseudo-height 处出现 ≈0.60 的峰值，单指在同区间仅 ≈0.30–0.35；123 与 167 PWM 下三指峰更窄（80 与 110 pseudo-height 处 ≈0.50），单指分布更宽、空间选择性更弱。",
        "阈值预实验（n=12）：最低可感知振动 35 PWM、最小可辨点距 25 pseudo-height、可区分间距差异的近似下界 15 pseudo-height。",
        "执行器标定：六个 PWM 档位的 RMS 加速度由约 0.04 g 单调升至 1.75 g（自由振动）与 1.63 g（指-面接触），接触只改变绝对幅值、不改变档位相对顺序。",
        "振动检测阈值与总体主观评分的相关不显著（r=.32, p=.224），说明基线触觉敏感度不足以解释被试间的评分差异。",
        "Study 2（n=8 专家）为质性研究，主题归纳为主，正文未给出量化对比。",
    ],
    "novelty": "把指尖振动触觉从“复现材料质感”重新定位为“随交互展开的空间结构解释性编码”，评估指标也从保真度换成可读性（signal separability、movement-contingent comparison），这是对既有材质模拟范式的前提性改写。方法上用贝叶斯 bootstrap 在选择概率空间里刻画“可解释子区域”而非拟合强度-间距映射，从而把触觉设计问题表述为在结构化刺激耦合中寻找感知最优点。两阶段设计（受控参数空间 → 专家情境化探索）也区别于以往只做单项阈值或离散辨别的工作。",
    "limitations": "正文明确承认未直接测量认知负荷（原文 'Although cognitive load was not measured directly'），多指条件的串行-并行权衡只能由评分与热图推断，未做验证。Study 2 是 8 人探索性质性研究，作者自述不追求统计效力，无法给出人群层面的效应估计。参与者反馈精细几何轮廓难以辨识（P2 已知存在三角形图案，但系统主要传达强度变化而非明确轮廓），且小尺寸平板上细节分辨受限。系统仅在一台 10.1 英寸平板与固定 LRA 布局上验证，多指间距未受控，也没有与任何基线触觉编码方案做对照。",
    "code": "none",
    "venue": "arXiv preprint（正文仅标注 ©2026 IEEE 与 pubid 979-8-3315-5021-9/26，未声明具体会议或期刊名）",
    "evidence": "FULL",
    "scores_hint": {"IMP": 3, "NOV": 3, "TEC": 3, "EXP": 3, "PER": 2, "TRL": 3, "REP": 3},
    "scores_why": "IMP=3：触屏触觉解读图像对无障碍与博物馆场景有意义，但属细分交互问题而非 XR 核心瓶颈。NOV=3：把振动从材质模拟改写为空间编码的框架有新意，但硬件与实验范式均为已有组件的组合。TEC=3：含执行器标定、阈值预实验与两阶段用户研究，完整度尚可，但缺基线对照与量化解读性能指标。EXP=3：仅 n=20 受控实验加 n=8 专家质性研究，单一平板与单一装置。PER=2：未定义性能基线，也没有相对提升数字，只有主观评分差异。TRL=3：Arduino + 平板 + 定制 LRA 的实验室原型。REP=3：无代码与数据，但硬件参数、PWM 档位与公式参数给全，可按细节复现。",
}

# ---------------------------------------------------------------- 2. EgoLink
DIGEST["2611.21690"] = {
    "id": "2611.21690",
    "title_en": "EgoLink: Egocentric Language-Vision Interactive Network Knowledge Challenge Summary",
    "title_zh": "EgoLink：第一人称语言-视觉交互网络知识挑战赛总结",
    "track": "评估与数据集",
    "problem": "现有第一人称基准多集中在前景物体与活动识别，无法检验模型能否解读情绪与社会线索、消解视觉指代，并把用户请求转成可验证的工具调用动作。作者指出两类反复出现的失败：社会性回答在语言上合理却缺乏视频/音频证据支撑；交互 agent 回复流畅但调错工具、使用未落地的实体，或在未验证前置条件前就改动数据库状态。两者都是 evidence–decision 耦合薄弱。",
    "method": "EgoLink 作为 ACM MM 2026 挑战赛设两条互补赛道。Track 1（Social Reasoning in Egocentric Video）把 E³ 视频重构成统一 MCQ 协议，覆盖情绪感知与时间定位、社会因果推理、行为意图预测、第一人称语义摘要四类能力。其数据构建是多阶段流水线：从多模态片段生成题干与选项，模板引导生成 chain-of-thought 理由，再用 LLM-as-a-judge（Qwen3-235B-A22B）按答案一致性、干扰项质量、语言流畅度、推理逻辑、简化推理质量五个维度做五分制打分并据此过滤，最后做 Video-Contribution Filtering 剔除不看视频也能答对的题以抑制模态捷径。发布评测集为 4,030 道 MCQ 配 1,055 段 E³ 视频；规则要求参赛者用 EgoLink 标注替代原始 E³ 标签，Track 1 禁止任何外部视频数据用于训练、微调、蒸馏、校准或伪标签构建。Track 2（Interactive Agent Challenge）基于 EgoBench 的 user-agent-tool 沙箱，覆盖 retail、kitchen、restaurant、order 场景，agent 需在首视角视频流、用户指令、场景数据库与官方工具之间完成指代落地，并决定回答、请求澄清还是调用工具，数据库更新必须由视觉证据与工具观测支撑。Track 2 以 joint success 为主排序指标（同时通过工具调用过程评测与数据库结果评测才算成功），辅以 call 级 micro accuracy 及 result/tool 两个分项成功率来暴露过程与结果的错配。",
    "key_results": [
        "Track 1 官方榜（top-1 MCQ accuracy）：GXU-LIPE 0.9263、Lai 0.9246、TeleAI 0.9132、EgoMinds 0.9092、wjdd 与 MR-CAS 均为 0.9089。",
        "数据规模：Track 1 评测集 4,030 道 MCQ / 1,055 段第一人称视频；Track 2 最终发布 309 个任务（retail6、retail10、kitchen4、restaurant5、order2），官方计分使用 96 个任务的公共子集（retail6/retail10/order2 各 20，kitchen4 与 restaurant5 各 18）。",
        "Track 2 官方榜：MediaLab joint 0.844 / micro 0.916 / result 0.875 / tool 0.854；GML-MM Group 0.823 / 0.914；BigVisionAgentGoGoGo 0.781（result 0.896 但 tool 仅 0.802）；uestc_goat 0.729；EgoMinds 0.604。",
        "MediaLab 消融：去掉 correction agent，Joint 由 0.844 降到 0.781；再去掉 scenario rules 进一步降到 0.646。",
        "Lai 消融：process-aware reward 达 91.98%，完整 option-perturbed 设置验证集 92.75%、官方挑战赛 92.46%；GXU-LIPE 报告验证集 92.89%、官方测试 92.63%。",
    ],
    "novelty": "把“第一人称社会认知”与“闭环交互执行”放进同一个基准，用离线 MCQ 与状态改变式的工具交互两种协议共同检验感知-推理-决策是否仍然耦合，这是相对只测识别或只测规划的既有基准的实质差异。Track 1 的构建把贡献度过滤（Video-Contribution Filtering）与五维 LLM 判分作为数据集质量门控，直接针对社会问答里“不看视频也能答对”的捷径问题。挑战赛总结还把过程正确性（tool-based）与最终状态正确性（result-based）分开报告，使“回复流畅但流程错”的失败模式显式可测。",
    "limitations": "作者明确说明所总结的结果尚未建立对已发布场景之外的泛化性（原文 'generalization beyond the released scenarios is not established'）；Track 2 的评测只覆盖已发布场景，未涉及未见场景、更长交互与可恢复的工具失败。Track 1 的模态捷径风险未被实验排除，modality-dependence 测试、选项顺序扰动与时间证据评测都被列为未来工作。此外论文只分析了主办方提供的四份技术报告（Track 1 的 GXU-LIPE、Lai，Track 2 的 MediaLab、GML-MM Group），并非全部提交，结论代表性受限。",
    "code": "https://ego-link.github.io/challenge2026",
    "venue": "ACM MM 2026（Proceedings of the 34th ACM International Conference on Multimedia, MM '26, Rio de Janeiro）",
    "evidence": "FULL",
    "scores_hint": {"IMP": 4, "NOV": 3, "TEC": 3, "EXP": 4, "PER": 2, "TRL": 4, "REP": 4},
    "scores_why": "IMP=4：第一人称社会推理与工具型 agent 是 AI 眼镜/AR 助手的高频评测需求。NOV=3：赛道组合与数据流水线属把 E³、EgoBench 与既有过滤范式重新组织，非新范式。TEC=3：基准构建与评测协议交代清楚，但无自有基线模型、无系统性消融，仅整理参赛方报告。EXP=4：4,030 题 / 1,055 视频与 96 任务计分子集，多支队伍参与，样本量足以支撑榜单结论。PER=2：只报绝对榜单分数，未与同条件既有 SOTA 基线做增益对比。TRL=4：公开挑战赛页面、数据与榜单，可直接复现评测。REP=4：有公开数据与顶会论文，但没有官方代码仓库。",
}

# ---------------------------------------------------------------- 3. varlen-3D
DIGEST["2611.21802"] = {
    "id": "2611.21802",
    "title_en": "Data-Driven Variable-Length Compression of 3D Representations",
    "title_zh": "数据驱动的三维表示变长压缩",
    "track": "系统与平台",
    "problem": "三维形状在不同应用中复杂度差异极大，但体素、网格等表示按全保真存储，开销与复杂度无关；传统编解码器（Draco、V-PCC、V-DMC 等）绑定特定表示，既不能开箱适配新表示，也无法利用训练集统计。per-shape 神经表示（SDF、位移场逐形状拟合）虽率-失真更好，却不能共享跨形状先验，且推理时需要昂贵的逐形状优化。数据集级学习的压缩器则把压缩率写成训练前固定的超参，所有形状同一比例，牺牲了变复杂度下的率-失真折中。",
    "method": "方法假设已有冻结的预训练信号自编码器 E:S→Z 与解码器 D:Z→S（mesh 用 MeshGPT latent，SDF 用 3DShape2VecSet latent），只在其 latent 空间上加装一个轻量 hyper-autoencoder，不重训底座，因此只学到 latent 到有序 token 序列的映射。hyper-encoder 用 Perceiver 式 cross-attention：key/value 来自 latent token 序列 z_{1:Z}，query 来自训练后固定的可学习向量集 Q^(e)，输出 K 个 hyper-token；随后接因果 self-attention，使 token 顺序由 query 固有顺序与因果掩码共同决定，前期 token 被鼓励尽量承载全局粗结构。hyper-decoder 反向再做 Perceiver cross-attention，以另一组固定 query Q^(d) 从任意前缀 t_{1:k}（k≤K）重建长度恒为 Z 的 latent z̃^(k)，所以丢后缀不改变输出维度、只降低保真度。训练分两段自监督：先最小化 latent 空间 MSE，避免梯度穿过信号解码器、并在早期更稳定；再用信号空间损失（如 SDF 采样 MSE）微调，使 hyper-decoder 可直接被几何损失监督——这是 regression 解码器相对 flow 解码器的关键优势。推理时用前缀截断或 suffix dropout 得到任意码率，用户可按形状或 latent 空间的质量指标逐形状决定保留多少 token，更复杂的形状分配更多 token，全程仅前馈、无逐形状优化。",
    "key_results": [
        "在 ShapeNet 上，mesh（MeshGPT latent）与 SDF（3DShape2VecSet latent）两种模态的 rate–distortion（Chamfer distance vs 压缩率）曲线均落在 Pareto 前沿，且不劣于其派生来源的定长自编码器；正文只给曲线，未报告具体 Chamfer distance 与压缩率数值。",
        "与 per-shape 方法和数据集级定长压缩两类基线对比，作者声称取得更好的率-失真折中（'state-of-the-art rate–distortion'），但正文未给出量化对比数字，全部结论以 Figure 2 曲线支撑。",
        "消融（仅 Figure 4 曲线，正文未报告具体 dB 或 Chamfer 数值）：regression hyper-decoder + 信号空间损失优于同结构仅用 latent 损失的解码器，也优于 FlexTok 式 flow 解码器；低 k 时 flow 解码器给出更锐利但错误的形状，高 k 时 regression 解码器更忠实。",
        "token 数 k 与重建 Chamfer distance 呈反比（Figure 2 第 2、4 列）；达到同一 latent MSE 阈值所需 token 数随形状几何复杂度上升（Figure 3），即实现了按复杂度分配码率的定性目标，阈值具体数值正文未报告。",
    ],
    "novelty": "把“变长 tokenization”从图像生成迁移到三维压缩，并把问题形式化为：在冻结自编码器的 latent 上训练一个前缀可解的 hyper-autoencoder，使压缩率成为推理期可逐形状选择的变量而非训练期超参。与 FlexTok 的实质差异是用 regression hyper-decoder 替代 flow 解码器，从而能在信号空间反传几何损失；作者指出 3D 领域缺少像图像那样感知对齐的强 latent，这一步是性能提升的主要来源。相对 per-shape 神经压缩与定长学习式压缩，它同时拿到跨形状先验与变码率两个性质，且换 backbone 不改底座。",
    "limitations": "所有结论都在未量化（unquantized）设定下成立，作者在正文中标注量化版 MeshGPT 的曲线会整体右移，因此该方法与真实部署码率不可直接比较。评测只在 ShapeNet 单一数据集、两种表示（mesh 与 SDF）上完成，未覆盖点云、NeRF/3DGS 等表示，也没有真实传输或存储系统实验。结果全部以图呈现，缺少数值表格，第三方难以复算改进幅度；此外每换一个 backbone 都需重训 hyper-autoencoder，跨模态的额外训练成本未被量化。",
    "code": "https://github.com/voilalab/varlen-3D",
    "venue": "arXiv preprint",
    "evidence": "FULL",
    "scores_hint": {"IMP": 3, "NOV": 4, "TEC": 3, "EXP": 3, "PER": 2, "TRL": 4, "REP": 4},
    "scores_why": "IMP=3：3D 资产压缩对 AR/VR 传输与存储有实际价值，但属支撑性基础设施而非 XR 卡脖子交互问题。NOV=4：把变长前缀解码压缩形式化到 3D latent 空间，并以 regression 解码器打通信号空间监督，属显著的新问题形式化。TEC=3：两阶段训练、双模态与解码器消融齐备，但结果全为曲线、无量化表，且未做量化码率对照。EXP=3：仅 ShapeNet 单一数据集、两种表示，无真实系统实验。PER=2：声称 SOTA 与 Pareto 前沿，但正文未给出任何可核对的提升数字。TRL=4：代码已开源、可复现训练与推理原型。REP=4：有代码仓库与完整方法描述，但无顶会与数据发布细节。",
}

# ---------------------------------------------------------------- 4. HubEgo-100K
DIGEST["2611.21938"] = {
    "id": "2611.21938",
    "title_en": "HubEgo-100K: In-the-Wild Egocentric Video of Skilled Work for Robot Learning",
    "title_zh": "HubEgo-100K：面向机器人学习的野外第一人称技能工作视频数据集",
    "track": "评估与数据集",
    "problem": "模仿学习训练出的机器人策略在训练场景与物体之外泛化很差，而已发表的数据 scaling 研究表明泛化随训练环境与物体多样性增长、每个环境多加演示会饱和。但跨大量环境采集机器人数据极其昂贵：DROID 用 12 个月、50 名采集者才得到 350 小时 / 564 个场景。第一人称人类视频可在野外低成本大规模录制，然而现有 egocentric 数据集多记录日常生活、厨房或实验室脚本任务，缺少真实工作场所中的技能性手工劳动；同时少有数据集同时提供逐帧惯性数据与任务、动作、语言标注。",
    "method": "HubEgo-100K 让贡献者用头戴手机在自己工作场所或家中录制“已命名但不脚本化”的任务，v1.0 为 10,124 小时 1080p、30 fps 单目视频，配同步原生 IMU（加速度计/陀螺仪中位 99.98 Hz），覆盖 56 种手机型号、99.1% 使用超广角镜头（对角视场中位 114.3°）。采集后走九阶段 curation pipeline：头戴检测剔除未戴在头上的素材；VLM 做稠密时间分割只保留双手执行命名任务的片段；手部可见性门控用两个 VLM 组成的 panel 按 1 fps 标注每帧（无手 / 左手 / 右手 / 双手 / 不确定，不确定按无手计），丢弃手大多出画的录制并剪掉长时间无手片段；隐私检测每 2–6 秒抽帧，命中儿童、他人面部或私密文字则连带 5 秒余量剪除；episode 组装时 30 fps 直接 stream copy、60 fps 重编码为恒定 30 fps，超 30 分钟等分；随后做完整性与同步检查（帧间隔、重复帧、漂移，中位绝对漂移 0.017 s），并把传感器时间戳统一到 episode 首帧的纳秒基准；再按 56 种 task type 重新平衡小时数（中位 69.5 小时）。标注由 VLM 完成：每 episode 一个 task type（归入 30 个 work category）、35 个 action family 之一、18 个 skill group 之一、easy/medium/hard 难度、11 种 setting type 之一，外加平均 7.4 词的描述与平均 35.2 词的 step-level instruction（步骤不做时间定位）。数据按 LeRobot v3 布局发布：每 episode 一个 MP4、逐帧 parquet、一个含全部原生传感器样本的 MCAP，加 catalog 与 annotation 表，全部 episode 以 episode_index 对齐，CC BY 4.0。",
    "key_results": [
        "规模：v1.0 共 10,124 小时、72,754 episodes（中位 4.9 分钟、最长 30 分钟）、41,688 recordings、1,093,194,072 帧，43.5 TB 视频 + 1.29 TB 原生传感器流。",
        "多样性：12,227 名贡献者、15,548 个 environments（11 种 setting type）、30 个 work category、56 个 task type、35 个 action family；82.6% 小时在工作场所；无单一贡献者超过 0.22% 小时，有效贡献者数 5,666，贡献者中位录制 21.3 分钟（Ego4D 平均约 3.9 小时/人）。",
        "质量估计（模型估计）：至少一只手出现在 94.7% 采样帧、双手 76.3%，on-task share 96.9%（按小时加权）；70.6% 的 episode（占 83.0% 小时）在 ≥90% 采样帧中可见手。",
        "长尾：描述使用 1,429 个动词词元与 3,709 个名词词元；随机顺序下最后 10% 小时仍新增 356 名贡献者、570 个 environments、约 39 个动词与 84 个名词词元；34.5% 小时被标为 hard。",
        "同类对比（Table 1）：其他数据集人数 9–2,087（Ego4D 931、Ego-Exo4D 740、EgoVerse 2,087、DROID 50 名采集者），地点数 45–610，v1.0 为 12,227 人与 15,548 环境。",
        "没有任何策略学习实验：正文未给出 policy 成功率或下游基准结果，作者把训练基线列为下一步工作。",
    ],
    "novelty": "相对 Ego4D、EPIC-KITCHENS-100、Ego-Exo4D 等以日常生活、厨房或实验室脚本任务为主的数据集，它把“真实工作场所的非脚本技能劳动”作为主体（83% 小时在工作场所），并同时给出逐帧 IMU、任务/动作/语言标注与 per-episode 质量信号。与 Egocentric-10K/100K 相比，实质差异不是时长而是逐轴量化多样性（贡献者、环境、任务、动作、词汇、设备）并报告 evenness、有效类别数与长尾增长曲线，把“多样性”变成可复算的指标。文章还把六个与策略性能相关的数据属性逐一映射到本数据集的测量值，使数据集设计与已发表的 scaling 证据直接对齐。",
    "limitations": "最关键的是 v1.0 没有任何策略学习实验：作者在 Discussion 中写明下一步才是在数据上训练基线（视觉编码器预训练、与机器人数据 co-training、在 contributor-disjoint 划分上评测），因此多样性对 policy 性能的实际贡献尚未验证。手部可见性与 on-task share 都是模型估计而非人工核验；采集受限于单目手机（无深度、无 3D 手部位姿，这些被列为后续标注层）。隐私处理（剪除儿童/他人面部/私密文字、剔除对他人实施的照护任务、删除音频与位置）会系统性缩小可用数据并可能引入分布偏差；按 task type 重新平衡后任务分布不再反映真实世界出现频率，作者明确提醒需在目标使用条件下重新评估。",
    "code": "https://huggingface.co/datasets/HubLabs/HubEgo-100K",
    "venue": "arXiv preprint",
    "evidence": "FULL",
    "scores_hint": {"IMP": 4, "NOV": 3, "TEC": 3, "EXP": 4, "PER": 2, "TRL": 4, "REP": 4},
    "scores_why": "IMP=4：面向机器人学习的数据多样性是具身智能的高频刚需，直接对应泛化瓶颈。NOV=3：贡献在数据与测量体系，九阶段流水线是既有工具的工程化组合，非新方法。TEC=3：流水线、标注、隐私与格式交代完整，但缺基准与策略实验，属半边工程。EXP=4：10,124 小时、12,227 贡献者、72,754 episodes 的大规模统计充分，但无学习实验。PER=2：不涉及模型性能，正文无任何策略或基准增益数字。TRL=4：CC BY 4.0 正式发布、可申请下载、版本化迭代，但无下游验证。REP=4：数据、catalog、datasheet 齐全，没有训练代码与基线模型。",
}

# ---------------------------------------------------------------- 5. CueSplat
DIGEST["2611.22095"] = {
    "id": "2611.22095",
    "title_en": "CueSplat: Learning to Schedule Sparse Deformation for Dynamic Gaussian Splatting on Edge Devices",
    "title_zh": "CueSplat：学习调度稀疏形变以实现边缘设备上的动态高斯泼溅",
    "track": "神经渲染",
    "problem": "基于形变的 4D Gaussian splatting 在每个时间步都要对所有 Gaussian 求解形变网络，边缘设备上代价极高——E-D3DGS 在 Jetson AGX Orin 上形变约占 GPU 流水线时间的 85%。现有加速依赖 Gaussian 剪枝、静动态分解或共享运动表示，但剪枝与限制运动表达会损伤重建质量，静动态划分在渲染期间固定不变，把动态 Gaussian 误判为静态会破坏运动重建。",
    "method": "CueSplat 是 post-training 框架：冻结预训练 backbone 的 canonical Gaussian 与形变参数、保留完整 Gaussian 集合，只在其上做稀疏形变调度。其动机来自测量——五帧内 static/linear/quadratic 拟合可覆盖 N3DV 66.2%、Technicolor 68.8% 的 Gaussian-window 对，但 54.4% 采样 Gaussian 在某些窗口满足五帧拟合、在另一些窗口违反，说明局部规律存在而可靠性随 Gaussian 与时间变化。在线推理先用最近三个已接受状态做阻尼有限差分外推预测全部属性（位置 λ_v=0.85、λ_a=0.15；旋转用阻尼四元数增量；尺度保持；动态外观从同三帧滤波；静态属性取 canonical 值），再由轻量 MLP router（约 2.0k–2.6k 参数）依据冻结 descriptor、编码时间戳与运动/可见性/贡献/更新年龄等在线特征打更新分，取 TopK 作为精确更新子集，替换预测值后合并渲染。为降低路由开销，每 N=5 帧才重算特征与索引并在帧间复用，但被选中的 Gaussian 每帧仍做精确形变。离线先按 rendering-aware risk ρ=m_vis·o·πr²/(HW)·[log(1+e)]² 标定场景级预算 K_s（取标定帧提议的 90 分位并向上取档），经 oracle 闭环检查（代理 PSNR 均值 ≥40 dB、10 分位 ≥37 dB）通过后，用教师信号（五类属性误差按帧内中位数归一后由可见性、不透明度、投影半径加权）生成 top-k 二值标签与连续优先级，以 ranking + BCE + SmoothL1 三项损失训练 router，再做第二轮闭环验证，不达标就升档。为控制误差累积，用漂移信号 d_t=0.4Ē+0.2r̄+0.2m̄+0.2a 触发连续三帧全形变刷新（最小间隔 20 帧、连续两次帧级分数 ≥0.6 触发、最迟 s+40 强制），并把刷新所需的精确评估分摊到前 10 帧预计算以削平延迟尖峰。",
    "key_results": [
        "12 组 backbone–dataset 组合（E-D3DGS / 4DGaussians / GaGS / SpeeDe3DGS × Technicolor / N3DV / NeRF-DS）在 Jetson AGX Orin 上取得 1.75–6.74× 加速，数据集平均 PSNR 下降至多 0.16 dB；Orin NX 上 1.81–8.15×，A6000 上峰值 5.04×。",
        "代表点：Technicolor 上 GaGS 由 10.65 FPS 提升至 71.79 FPS（6.74×，PSNR 32.99→32.92）；N3DV 上 E-D3DGS 15.64→38.24 FPS（2.45×，27.92→27.88 dB）；NeRF-DS 上 4DGaussians 72.26→126.27 FPS（1.75×）。",
        "慢帧性能：GaGS/Technicolor 的 FPS P5 由 10.63 升至 52.58；加刷新预计算后 N3DV 上 FPS P5 由 17.68 升至 26.20（+48.2%），平均吞吐只降 0.3%（40.95→40.81 FPS）。",
        "执行计算量：服务端 profiling 显示每帧 GPU warp 指令减少 29.9%–90.7%，GaGS/Technicolor 由 8206.42M 降至 760.01M。",
        "对 DASH：Technicolor 上四个 backbone 的平均 PSNR 均优于 DASH-style 对照，E-D3DGS +0.37 dB、4DGaussians +0.26 dB、GaGS +0.22 dB（FPS 高 81.3%）、SpeeDe3DGS +1.19 dB（+26.3% FPS）；但与官方 DASH 复现（31.12 dB / 39.13 FPS）相比，SpeeDe3DGS+CueSplat 为 30.91 dB / 37.50 FPS，略低。",
        "消融（Technicolor 50 帧、四 backbone 平均）：学习路由比 motion-magnitude 排序高 1.44 dB（32.50 vs 31.06，LPIPS 0.0914 vs 0.1018）；时间外推比 hold-last 高 0.21 dB；场景级预算比统一 20% 预算高 1.22 dB；三帧刷新比单帧刷新 PSNR 27.50→27.88 dB（FPS 41.83→38.36）。",
    ],
    "novelty": "把“选择性计算”引入冻结的 4DGS 形变网络：不剪枝、不改 Gaussian 集合、不做静动态硬划分，而是把每帧形变评估变成按预测可靠性与渲染贡献动态分配的预算，这是相对剪枝、分解、共享运动三条现有加速路线的实质差异。router 由教师信号监督，并配合离线 oracle 与闭环质量门控的场景级预算标定，使加速比随场景风险自适应而非全局固定。漂移触发的三帧历史重建加上刷新预计算，补上了“预测-反馈”闭环里误差累积与延迟尖峰两个工程缺口。",
    "limitations": "作者在结论中明确承认当前实现假定按均匀时间步顺序渲染（'The current implementation assumes sequential rendering at uniform time steps'），时间跳转（temporal seeking）与变速播放尚不支持，被列为未来工作。每个 scene–backbone–budget 组合都要单独训练 router，场景级准备在 RTX A6000 上需 1–2 分钟、预算升档再加约 1 分钟，部署前准备成本不低。Technicolor 的 50 帧序列在初始化后直接禁用刷新，说明刷新机制在短序列上未经检验；与 DASH 官方复现相比 SpeeDe3DGS+CueSplat 的 PSNR 与 FPS 都略低，跨方法比较并非全面占优。",
    "code": "none",
    "venue": "arXiv preprint",
    "evidence": "FULL",
    "scores_hint": {"IMP": 4, "NOV": 4, "TEC": 5, "EXP": 5, "PER": 5, "TRL": 3, "REP": 3},
    "scores_why": "IMP=4：动态 4DGS 在移动/头显端跑不动是 XR 内容落地的共性瓶颈，需求高频。NOV=4：把冻结 4DGS 的形变评估改造成可学习的选择性调度，属显著的新架构角度而非参数微调。TEC=5：四 backbone × 三数据集 + 路由/预测/预算/刷新/复用期全维消融 + 指令级 profiling，系统与理论验证充分。EXP=5：3 个数据集 21 条序列、12 组组合，并在 AGX Orin、Orin NX、A6000 三种真实硬件上实测。PER=5：吞吐提升 1.75–6.74×（75%–574%），质量代价 ≤0.16 dB，远超 30% 门槛。TRL=3：需逐场景离线标定与训练，仍是实验室原型且无代码。REP=3：无代码与数据，但公式、阈值与超参给得足够复现。",
}

# ---------------------------------------------------------------- 6. HandUMI
DIGEST["2611.22146"] = {
    "id": "2611.22146",
    "title_en": "HandUMI: A Modular Hand-Worn Parallel-Jaw Interface for Robot-Free Bimanual Data Capture",
    "title_zh": "HandUMI：用于无机器人双臂数据采集的模块化手戴平行夹爪接口",
    "track": "交互与输入",
    "problem": "用 leader arm、replica 或 VR 控制器做遥操作时，每采一条演示都要占用机器人，采集吞吐受硬件数量限制。UMI 类无机器人接口解耦了采集与臂的运动学，但接触几何或开合运动不匹配会阻碍向真机迁移。最接近的 YUBI 同样用 Quest 控制器加编码器测开合且开源，但它要把机器人换成自己的夹爪、记录的是夹爪角度并建模转动指，指尖也仅一种设计，采集端与部署端的夹爪形态因此不完全一致。",
    "method": "HandUMI 是手戴式平行夹爪接口：公共 wearable 主体上可换指尖、控制器类型与相机，printed finger cradles 通过曲柄驱动平行 jaws 平移，Feetech STS3215 12-bit 编码器经两点标定测 jaw 宽度，IMX335 鱼眼以 1280×960@30 fps 记录，可选 ZED Mini 提供工作区视角；指尖可匹配 AgileX PiPER、ARX X5、TRLC-DK1 的 Dream Gripper、Trossen WidowX AI 与 UMI 软指，机器人保留自己已装的夹爪。位姿不用腕部相机 SLAM，而由可替换 provider 提供带时间戳的 6-DoF 控制器位姿：Quest 3/3S 走新写的 TCP app（实现 YUBI Apache-2.0 软件的协议），PICO 4 Ultra 走 XRoboToolkit，ChArUco 板定义桌面坐标系。同步以工作站单调时钟给所有源打戳，每行目标落后实时 40 ms，取最近的相机（30 fps）与编码器（100 Hz）样本并带 freshness 标志（60 ms 偏斜上限），传感器丢失超过 1 s 即丢弃该 episode；标定分四级门控（夹爪行程、内参 ≤0.8 px 平均重投影误差、相机安装与桌面坐标系 ≤8 mm RMS、每个指尖的 TCP pivot 拟合 <5 mm RMS 且最大残差 <10 mm），另有引导式触碰协议用每位置 20 个样本交叉检查两指尖。数据以 LeRobot v3 记录两条控制器位姿与 jaw 宽度，与具体机器人无关；重定向时 profile 提供运动学、限位、TCP 与线性夹爪映射（0–66 mm 映射到 PiPER stroke，速度与力不匹配），由 PyRoki IK 生成七个双臂平台（PiPER、OpenArm v1、TRLC-DK1、I2RT YAM、MakerMods Metal Arm、Galaxea R1 Lite、ARX X5）的关节数据，并做 IK 误差、自碰撞、基座关节摆动的逐机器人筛选，PiPER 与 OpenArm 在 MuJoCo 中共享映射、IK 与平滑。",
    "key_results": [
        "跨本体重定向：七个模拟双臂的中位位置误差 0.03–1.17 mm（PiPER 1.17、OpenArm 0.14、TRLC-DK1 0.18、YAM 0.19、Metal 0.09、R1 Lite 0.03、ARX X5 0.09），episode 拒绝率 ≤4.7%（OpenArm），关节限位帧 OpenArm 27.5%、自碰撞 R1 Lite 16.4%。",
        "采集质量：641 条录制中 79 条（12%）因 PiPER 重定向使基座关节摆过 60° 被剔除，保留 562 条（201,397 帧、111.9 分钟）；采样网格中位偏斜约 8 ms，PICO 追踪在主机时钟上领先 ≈40 ms 但双腕在 100.00% 的行上均被追踪。",
        "标定精度：TCP pivot 拟合 RMS 4.0 / 3.4 mm、最大残差 7.013 / 7.021 mm（左/右）；桌面坐标系 RMS 1.6–4.2 mm 与 0.3–0.7°，两次重装 TCP 高度差 6–7 mm。",
        "真机策略（PiPER 双臂折毛巾，各 20 次无辅助尝试）：仅用 562 条无机器人演示训练的 ACT 成功 12/20（Wilson 95% CI 39–78%），微调 π0.5 成功 7/20（18–57%），两者无统计差异（Fisher exact p=0.20）。",
        "对照：只用前 101 条 episode 训练的 ACT 与未微调的 base π0.5 各为 0/20（0–16% CI）。",
        "成本：一对零件 USD 207.11，含共享 Quest 3S 共 USD 557（不含可选 ZED Mini、主机、税与运费）。",
    ],
    "novelty": "相对 UMI（无编码器、需换装专用夹爪）与 YUBI（记录 jaw 角度、建模转动指、单一指尖设计），HandUMI 用平移平行 jaws + 编码器测开合、指尖复制机器人已装夹爪、且机器人保留原夹爪，使采集端与部署端的接触几何更一致。工程上把“机器人无关录制 + 标定溯源 + IK 筛选”做成可向七个双臂平台重定向的流水线，并用真实 PiPER 双臂折毛巾给出端到端证据，而不只是仿真重定向误差。整套硬件与软件以 Apache-2.0 开源并给出 BOM 成本，把无机器人双臂采集的进入门槛压到数百美元级。",
    "limitations": "作者自陈跨本体证据只是仿真 IK，真机测试只有一个 PiPER 任务、一套 setup、一个 seed，且没有失败分析；holdout 划分可能与被测 session 重叠。采集受头显约束、仅支持平行夹爪，换新夹爪必须重做匹配指尖，接触几何仍然依赖本体。tip-matching 带来的收益、jaw 精度、指尖负载与音频价值均未测量。正文还记录了一次相机重标定故障：40 条 episode 事后施加 +1.9 cm 高度修正、其中 31 条留在队列里，而拟合残差与离线检查无法独立验证真实桌面高度，门控为何漏检原因未查明。",
    "code": "https://murobotics.ai/research/handumi（数据与 checkpoint：https://huggingface.co/murobotics）",
    "venue": "arXiv preprint",
    "evidence": "FULL",
    "scores_hint": {"IMP": 4, "NOV": 3, "TEC": 4, "EXP": 3, "PER": 4, "TRL": 4, "REP": 5},
    "scores_why": "IMP=4：无机器人双臂数据采集直接决定具身数据规模，且用 Quest/PICO 头显作追踪源与 XR 输入强相关。NOV=3：平移平行 jaws + 可换机器人同款指尖 + 七臂 IK 重定向属对 UMI/YUBI 路线的组合式工程改进。TEC=4：硬件、同步、四级标定、重定向筛选与两套策略实验闭环，缺的是失败机理分析。EXP=3：真机只一个任务、每配置 20 次尝试、单 seed，跨本体仅仿真。PER=4：ACT 12/20 对比 0/20 属大幅绝对提升，但单任务小样本、CI 宽（39–78%）。TRL=4：Apache-2.0 开源硬件软件、BOM 与实机演示齐备，尚未产品化。REP=5：开源硬件 + 软件 + HF 数据与 checkpoint + 完整标定协议。",
}


def main() -> None:
    root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    out = os.path.join(root, "data", "digest_1119_g1.json")
    with open(out, "w", encoding="utf-8") as fh:
        json.dump(DIGEST, fh, ensure_ascii=False, indent=1)
    print("written:", out, "| n =", len(DIGEST))
    for pid, rec in DIGEST.items():
        total = sum(W[k] * v for k, v in rec["scores_hint"].items())
        print(pid, rec["track"], "total=%.2f" % total)


if __name__ == "__main__":
    main()
