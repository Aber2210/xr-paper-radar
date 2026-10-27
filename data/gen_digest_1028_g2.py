# -*- coding: utf-8 -*-
"""Generate digest_1028_g2.json for 10 XR-related papers (batch g2)."""
import json
import os

digests = [
    {
        "id": "2610.33868",
        "slug": "RelateGS",
        "venue": "arXiv preprint（Yonsei University）",
        "tags": ["3D高斯泼溅", "3D视觉定位", "3D场景图", "开放词汇", "多模态推理"],
        "conclusion": "RelateGS 以置信度语义提升与图引导关系补全精炼证据，Sr3D+/Nr3D 的 Acc@0.25 超此前最佳 7.9/1.7 个百分点（15.3% vs 7.4%，10.3% vs 8.6%）。",
        "problem": "语言嵌入式 3DGS 做关系感知定位时存在两类证据缺陷：多视图语义聚合混入受视角、遮挡与可见性影响的弱观测，污染高斯语义；成对关系仅由相机轨迹暴露的构型推断，关键物体对观测不足时关系缺失，导致「table 旁的 chair」类指代无法消歧。已有场景图本身不保证证据可靠、充分。",
        "method": "输入为位姿 RGB-D 观测与重建的 3DGS 场景。①置信度感知语义提升：沿用 Occam's LGS 的免训练提升框架，在 alpha 合成中由不透明度贡献与累积透射率导出每个高斯的渲染显著度 s_iv 作为观测级置信度，仅保留 s_iv≥τ_c 的观测再加权聚合语言特征，抑制弱/被遮挡观测。②持久对象图：用 LLaVA-SpaceSGG 提取帧级物体与关系，经深度与位姿反投影到 3D，按空间、语义、尺度一致性打分并匈牙利分配实现跨视角一对一关联，融合 VLM 关系与几何导出关系。③图引导精炼：按「空间邻近且关系置信度不足」识别欠观测物体对，从原相机轨迹中检索对二者联合视锥覆盖充分、视角对齐的帧，用成对专用提示重新查询并把新证据融合回图。下游沿用 GaussianGraph 的 LLM 图匹配协议，增益完全来自场景侧证据。",
        "experiments": "在 ReferIt3D 的 Sr3D+ 与 Nr3D（沿用 BBQ/GaussianGraph 的 8 个 ScanNet 场景）评测 Acc@0.1/0.25：Sr3D+ 总体 22.2/15.3，超 GaussianGraph 18.2/7.4（+4.0/+7.9pp）；Nr3D 总体 21.7/10.3 对 17.2/8.6（Acc@0.25 +1.7）。语义分割 Replica mIoU 41.11/mAcc 61.51、ScanNet 32.70/49.04 均最优；LERF-OVS ramen Acc@0.25 57.75 最佳。消融：初始图 21.34/12.12，+置信度语义 21.72/13.10，随机补询 19.78/11.62，图引导补询 22.22/15.28（同 VLM 预算下比随机 +2.44/+3.66）。单卡 A5000 24GB。",
        "innovation": "①首次从场景侧证据质量（高斯语义可靠性 + 对象关系充分性）刻画关系感知 3D 定位；②置信度感知语义提升，用渲染显著度过滤弱多视图观测；③持久对象图 + 图引导的关系补查询询，证明「按当前图所缺条件化地获取证据」远优于同预算随机补询。",
        "limits": "仅在 8 个 ScanNet 室内场景验证，室外与大场景未测；依赖 LLaVA-SpaceSGG 的帧级观测质量与轨迹共视覆盖；Hard 子集与部分指标增益不均匀；推理期额外 VLM 补查询增加调用成本；未评测实时性。",
        "repro": "正文列有 Project Page 与 Code 链接但未给出具体 URL；实现细节称见补充材料，硬件为单张 A5000。",
        "relation_hint": "与库内 GaussianGraph、Occam's LGS、LangSplat、LEGaussians 同线，可视为 GaussianGraph 的场景侧证据精炼扩展。",
        "track_hint": "感知与认知"
    },
    {
        "id": "2610.34093",
        "slug": "LegoOcc++",
        "venue": "arXiv preprint（HKUST-GZ / CUHK-Shenzhen；前身 LegoOcc 为 CVPR 2026 Oral）",
        "tags": ["开放词汇占用预测", "3D高斯", "语义占用", "自动驾驶", "具身感知"],
        "conclusion": "LegoOcc++：Occ-ScanNet IoU/mIoU 提至 61.73/24.22；Occ3D-nuScenes 单帧 15.14 mIoU 近 8 帧 PGOcc 15.15。",
        "problem": "室内开放词汇 3D 占用预测受密集遮挡、复杂几何与细长尾语义制约，且体素级语义标注昂贵；LegoOcc 存在三局限：像素级对齐导致同一物体内语义碎裂、固定时序间隔选择的支持视图冗余或重叠不足、以及仅面向室内具身场景未验证室外泛化。",
        "method": "以 Language-Embedded Gaussians（μ,Σ,α,f）统一几何与语言表征。几何学习：提出 opacity-aware 的 Poisson 式 Gaussian-to-Occupancy，p(x)=1-exp(-Σα_i p_i(x))，将不透明度纳入体素聚合以与 opacity-aware 渲染一致（Bernoulli 聚合会迫使不透明度趋小）。语义学习：特征可微渲染到图像并与冻结 Trident 对齐，配合指数式 Progressive Temperature Decay（1→1e-3）锐化不透明度、抑制射线特征混合。新增实例级语义一致性：SAM 掩膜内聚合教师特征成原型，约束同实例特征一致；共可见性感知支持视图选择：按可见体素重叠度 c∈[0.2,0.6] 过滤近重复与低重叠视图，贪心选姿态多样视图。室外改用无占用标注训练（Metric3D 伪深度+多视图渲染）。",
        "experiments": "Occ-ScanNet（45,755 训练/19,764 验证，60×60×36 体素）：LegoOcc++ 61.73 IoU/24.22 mIoU（+2.23/+3.17），远超几何-only 基线 POP-3D（35.32/5.96）、LOcc（36.70/9.25），IoU 超全部闭词全监督方法（RoboOcc 56.48）。Occ3D-nuScenes（1,000 场景，200×200×16）：单帧 15.14 mIoU，超所有单帧方法（GaussTR 13.25），近 8 帧 PGOcc 15.15；比 GaussTR 快约 15 倍（6.22 对 0.42 FPS）、端到端参数少 71.9%。消融：Poisson 对 Bernoulli 开词 +12.85 IoU；Covis. 23.17/60.31；+SAM-Inst 24.22/61.73。RTX 4090 训练。",
        "innovation": "①提出 Poisson 式 opacity-aware G2O，统一几何聚合与语义渲染间的不一致；②实例级语义一致性（SAM 原型）抑制对象内语义碎裂；③共可见性感知支持视图选择替代固定时序间隔；④将框架从室内几何-only 监督扩展到室外无标注占用预测并验证泛化。",
        "limits": "furniture、objects 等广义类别仍困难（实例视觉/几何差异大）；室内仍依赖二值占用监督，完全去监督未解决；室外 car、traffic cone、manmade、vegetation 等小类有回退；室外 6.22 FPS 距实时交互有距离。",
        "repro": "正文声明代码将发布于 https://github.com/JuIvyy/LegoOcc ；训练超参完整（DepthAnything-V2 骨干、AdamW、batch 8、RTX 4090）。",
        "relation_hint": "CVPR 2026 Oral LegoOcc 的期刊扩展，与 EmbodiedOcc、GaussianFormer2、PGOcc、GaussTR 构成占用预测谱系。",
        "track_hint": "感知与认知"
    },
    {
        "id": "2610.34223",
        "slug": "Single-Camera Try-on Avatar",
        "venue": "IEEE TVCG（已接收；arXiv:2610.34223 [cs.GR]）",
        "tags": ["虚拟试衣", "单目重建", "3D高斯", "人体化身", "物理仿真"],
        "conclusion": "提出物理集成的双层 GS-Mesh 表征，仅用单目视频甚至单张图像即可重建解耦的 3D 穿衣人体化身，实现视觉合理的布料动力学虚拟试穿与新姿态动画（摘要级信息，无量化结果）。",
        "problem": "从单目视频或单张图像重建高保真、可动画、试穿就绪的虚拟化身仍困难：①现有方法常用单层表征同时表示服装与底层躯体，忽略二者不同的运动特性；②单相机输入往往无法完整覆盖服装与身体，导致观测不足。",
        "method": "提出物理集成的双层（double-layer）GS-Mesh 表示，将服装与底层躯体解耦以贴合各自运动特性，从单目视频甚至单张图像重建 3D 穿衣人体化身；2D 生成方法可由给定姿态序列生成视频但难以保持帧间一致，故引入 2D 生成数据补足单相机观测，并把生成数据的帧间不一致显式分解为几何不一致与外观不一致分别约束，使最终重建与渲染兼具 3D 一致性与时序连贯。相比依赖多视图重建的 3D 服装迁移与不做新视角/新姿态合成的 2D 扩散编辑，本方法仅需单目输入即可产出视觉合理的布料动力学试穿与新姿态动画。（依据 ar5iv 摘要页整理）",
        "experiments": "本次提取为 ar5iv 摘要页（LEVEL L1，正文仅 5,083 字符），无实验章节与任何数值：未报告基准名称、准确率/mIoU、样本量、用户研究或运行时指标，无法给出定量结果。可确认的元信息：arXiv:2610.34223 [cs.GR]，2026-10-25 提交，作者 Honghu Chen、Bo Peng、Jun Xiang、Jingtao Zhou、Xujing Chen、Juyong Zhang，评论注明已被 IEEE TVCG 接收；定量细节与实验设计需以 PDF 全文核实（缺失处已在 limits 注明）。",
        "innovation": "①面向单目视频/单图输入的物理集成双层 GS-Mesh 穿衣化身表征；②将 2D 生成数据的帧间不一致分解为几何与外观两类并分别约束；③以单相机输入同时产出合理布料动力学试穿与新姿态动画，优于多视图 3D 迁移与 2D 编辑路线。",
        "limits": "仅获摘要级证据：方法细节、定量结果、消融、失败模式与计算成本均不可见；2D 生成数据的质量与分布偏差可能限制保真度；「物理集成」的精度与稳定性需以 PDF 全文核实。",
        "repro": "摘要级未明示（正文不可得，未提及代码或数据发布）。",
        "relation_hint": "与库内 3DGS 人体/服装重建与虚拟试衣类工作同属化身建模赛道，差异在单相机输入与双层物理解耦。",
        "track_hint": "化身与人体"
    },
    {
        "id": "2610.35414",
        "slug": "Unveil-the-Mask Operator Verification",
        "venue": "arXiv preprint（The University of Osaka）",
        "tags": ["化身验证", "行为生物特征", "扩散掩码预训练", "对比学习", "WBA2026"],
        "conclusion": "WBA2026 上总体 AUC 0.769（Same Gen 0.901/Diff Gen 0.637）：地标扩散掩码预训练+驱动感知对比探针与帧差视频分支融合有效，跨生成器泛化仍最难。",
        "problem": "照片级化身视频把渲染外观与操作者（driver）解耦，人脸识别失效；验证操作者需要对其运动敏感、对化身外观不敏感的表征，并应对说话/收听模式差异大、跨渲染引擎泛化难三大挑战，且框架不依赖外部预训练模型。",
        "method": "两分支均从零训练、无外部预训练权重。地标分支：106 点地标经四步归一化去除化身静态形状与尺度；地标分三种时空 token 分组（Geo 16/Anat 10/Motion 16 组，每 token 覆盖 4 帧），以 Diffusion Masked Pretraining 做 Stage 1：随机掩码 60% token 并按余弦调度扩散腐蚀，双流 Transformer（掩码 token 只向干净 token 发起 query）恢复质心与坐标（Chamfer 距离）并做运动扩散，辅以运动能量、区域运动、眼形三个闭式辅助任务；伪生成器随机化用 6 类变换模拟生成器对运动的改造并以 GroupDRO 加权；Stage 2 冻结编码器，训练驱动感知对比线性探针（批内同驱动不同化身为正样本）。视频分支：地标引导人脸裁剪上的帧差卷积网络。两分支 256 维 embedding 加权拼接融合。",
        "experiments": "WBA2026 数据：官方训练 89,133 样本/201 驱动者/111 化身；作者划分训练 71,577/181/99，验证 960/20/12，测试 Same Gen 40,200、Diff Gen 40,200（每驱动者-化身对含 2 说话 +2 收听样本）。最终提交 Same Gen 0.901、Diff Gen 0.637、Overall 0.769；单地标 DiMP(Geo) 0.654，加辅助任务 0.675；单视频分支 0.686–0.694；单模型跨分支融合 0.720。线性探测：视频分支化身身份 2.1%（chance 1.3%）、地标分支约 10%。消融：三辅助任务 0.834（+2.3）；三种 token 分组全组合 0.862。Stage1 编码器 6 层/隐宽 256/8 头，25,000 迭代。",
        "innovation": "①将 DiMP 扩散掩码预训练适配到人脸地标序列并设计几何/解剖/运动三种 token 分组；②伪生成器随机化+GroupDRO 建模生成器对驱动运动的改造；③驱动感知对比探针以同驱动跨化身构造正负样本，抑制化身捷径学习；④帧差视频分支提供互补证据并改善跨模式（S↔L）验证。",
        "limits": "Diff Gen 仅 0.637，与 Same Gen 0.901 差距大，泛化未见生成器仍是主要挑战；地标表征仍残留约 10% 化身身份信息；跨模式 S→L/L→S 对地标分支最难；Diff Gen 最终仅用纯地标集成，视频分支因疑似依赖训练生成器线索被弃用。",
        "repro": "代码公开：https://github.com/ogatakatsuya/Unveil_The_Mask ；正文含完整训练配置与损失权重。",
        "relation_hint": "与 WBA 官方基线（ST-GCN 地标、Chapariniya 帧差视频）直接对比，属化身行为生物特征验证线。",
        "track_hint": "化身与人体"
    },
    {
        "id": "2610.33191",
        "slug": "Whale-You-Go-Green Avatar Persuasion",
        "venue": "arXiv preprint（MIT Media Lab）",
        "tags": ["具身对话智能体", "劝导技术", "可持续HCI", "纵向随机实验", "非人化身"],
        "conclusion": "N=576 六条件随机实验：四种具身化身即刻提升可持续选择（β=.401–.609，q≤.0126），仅白鲸提升环保态度；287 名回归者约两月后仍显著（β=.657, q=.0176）。",
        "problem": "具身对话 AI 能否以及多持久地促成可持续行为倾向与环保态度？已有气候干预研究显示信念、政策支持、分享与行为并不同步变化，且此前缺少同时对照文本聊天与无干预、并横向比较可识别人类、普通人类与受影响非人化身的纵向证据。",
        "method": "预注册（AsPredicted #300140）六条件随机在线实验：白鲸、Greta Thunberg、Emma Watson、普通女性化身（实时语音对话）对文本聊天与无干预控制。技术栈为 SvelteKit/Vercel + Prolific/Qualtrics，Anthropic Claude Sonnet 4.6 生成对话、ElevenLabs Eleven Flash v2 语音、Nano Banana 生成半写实形象；结局含四类价格匹配包装对的产品选择任务（TotalEco 0–4）、捐赠、分享意愿及 GREEN 态度等九类问卷。统计：基线调整线性 ANCOVA、HC3 标准误、BH-FDR 校正、2,000 次 bootstrap 置信区间；Wave 2 采用逆观测概率加权。",
        "experiments": "Wave 1 N=576（白鲸 97、Greta 100、Emma 94、普通化身 95、聊天 95、控制 95；平均 39.0 岁，SD 12.1，范围 18–80）：四化身即刻产品选择均高于控制（β=.401–.609，q≤.0126）与聊天（β=.398–.604，q≤.007），化身间无显著差异（F(3,541)=.790, p=.4997）；仅白鲸 GREEN 显著（β=.361, q=.0008）。Wave 2 287 人（49.8% 回归，每条件 45–52）：仅白鲸预助推产品选择显著（β=.657, q=.0176），但未显著优于其他化身均值（β=.325, p=.0558）；无条件在助推前提升 GREEN。捐赠/分享无差异。对话分析：481 段 Wave 1 对话、11,126 个三消息窗口，白鲸「非专家证言」占 55.1%（次高 Emma 22.6%）。",
        "innovation": "①六条件设计同时设文本聊天与无干预控制，分离「具身接口包」与可识别 persona 的效应（普通化身也显著优于聊天）；②首次在随机设计中纵向（约 2 个月）比较四类化身；③将行为倾向与态度两类结局分开逐项分析；④可信度、对话技巧与情绪轨迹的探索性分析为白鲸效应提供候选解释。",
        "limits": "产品选择为无激励的重复屏幕任务，控制组也上升 0.568，存在测量反应性/练习效应；随访反映含中间会话的干预序列而非单次暴露持续性；未建立白鲸优于其他化身的因果机制；未测感知可爱度/新颖度；结论限于美国 Prolific 样本与四类家常商品。",
        "repro": "摘要级未明示（正文未给代码/数据链接；研究经 MIT COUHS 豁免，Protocol #E-7428）。",
        "relation_hint": "延续 OceanChat/EcoEcho 对话海洋角色劝导研究，把对照与纵向设计推进为六条件 RCT。",
        "track_hint": "化身与人体"
    },
    {
        "id": "2610.33158",
        "slug": "GEMS Gaussian Episodic Memory",
        "venue": "arXiv preprint（University of Stuttgart）",
        "tags": ["情景记忆", "3D高斯泼溅", "时空推理", "具身问答", "基准数据集"],
        "conclusion": "GEMS 以 3DGS 时序 delta 存储场景历史：Nr3D 定位 58.9%，时空问答真实/合成 60.9%/71.0%（最强基线 44.8%/35.5%），4 次重访存储仅 1.95 GiB。",
        "problem": "长期运行机器人需建模半静态场景演化（物体移动、家具重排、设备增减），以回答「之前在何处、何时变化、与早前有何不同」。结构化场景图受限于构建时实体与文本描述，图像记忆受限于已观测视角，都无法提供可复检的视觉证据。",
        "method": "映射端：首次重访用 gsplat 建初始 3DGS 地图；后续重访选空间多样关键帧，在相同位姿下将上一地图渲染帧与新观测比较，变化分数 = 1-[0.3·SSIM + 0.7·DINOv3 特征余弦]，阈值化后按相对深度误差将连通域分类为 Add/Remove/Refine，仅局部重优化受影响高斯（静态高斯冻结但参与渲染）；每个高斯带 lifespan [b,d)，任意时刻地图为时序切片，存储随变化量而非重访数增长。推理端：LLM planner 在状态机约束下调用检索工具（sweep/search/covisible/recall）与推理工具（time_view/relook/locate/obj_view/compare/track），跨时间同位姿渲染支持时序对比，SAM3 按查询分割并提升到 3D，OWLv2 缓存支持概念检索。",
        "experiments": "自建 GEMS-Bench：3 个真实场景（RealSense D455f、COLMAP 位姿、各 4 次重访、244 QA）+12 个 HSSD/Habitat-Sim 合成场景（≥3 次重访、97 处物体变化、229 QA），共 473 QA。Nr3D 定位 58.9%（KeySG 49.8、BBQ 28.3）。时空问答：真实 60.9% 对最强基线 STaR 44.8%，合成 71.0% 对 35.5%（Qwen3.5 为共同 LLM，GPT-5.6-Luna 评判）。NVS 工具消融 +6.6 分（245 题）。重建：单次更新 1.12–1.67 分钟（GaME 29.4–29.8 分钟）；4 次重访后 1.95 GiB（fp32）/0.98 GiB（fp16），对关键帧 2.73 GiB、全帧序列 3.94 GiB。",
        "innovation": "①3DGS 情景记忆 + 每高斯 lifespan 时序 delta，存储随变化而非重访数增长；②图引导的 Add/Remove/Refine 变化分类与局部重优化；③agentic EQA：查询依赖的任意视角渲染、跨时间同位姿对比、按需 SAM3 分割；④发布时空基准 GEMS-Bench。",
        "limits": "真实场景受传感器噪声与位姿误差影响，远离训练轨迹的新视角出现伪影致性能下降（合成场景无此问题）；仅室内半静态场景；需深度输入；问答质量依赖 LLM 评判；对 P=30 以上大规模未测。",
        "repro": "代码与数据项目页：https://abwerby.github.io/GEMS/ 。",
        "relation_hint": "与 Khronos、ReMEmbR、DAAAM、STaR、Mind Palace 等情景记忆/EQA 工作对比，差异在全视觉证据的 3DGS 时序保留。",
        "track_hint": "重建与SLAM"
    },
    {
        "id": "2610.33558",
        "slug": "GeoLift Explicit-3D Spatial Reasoning",
        "venue": "arXiv preprint（Nankai University / Peking University / Amazon / Nanjing University）",
        "tags": ["空间推理", "视频MLLM", "前馈3D重建", "免训练", "路径规划"],
        "conclusion": "GeoLift 使 Qwen3-VL-4B 的 VSI-Bench 均分 55.4%→64.1%（路径规划 30.9%→53.6%），MindCube 23.4%→59.8%。",
        "problem": "视频 MLLM 能识别单帧物体，但难以把跨视角观测整合成一致空间状态：路径规划性能随转弯数骤降，多个直接推理与空间训练模型在 ≥3 转弯时接近随机猜测（Qwen3-VL-4B 23.7% 对随机 25.0%），说明仅有几何感知不足以支撑多步空间组合推理。",
        "method": "免训练四阶段。①定位：冻结视频 MLLM 在采样帧中定位查询相关物体（低置信度/非法框剔除）。②重建：冻结 VGGT-Omega 预测每帧深度、内参与相机到世界位姿，再用冻结 MoGe-2 的度量深度以最小二乘估计单一尺度因子 s 恢复公制尺度。③提升：边界框收缩并保留接近框中值深度的有效像素，背投影并变换到共享世界坐标系成度量点云。④关联：cut-pursuit 将点云划分为几何超点，各观测对其占据超点投票并按 df(s) 降权（IDF 式），高余弦相似度 + 范围感知距离约束的匹配用 union-find 合并，无需学习式匹配器。推理由同一冻结 MLLM 作控制器，调用显式空间算子（相对方向/距离、占据栅格 + A* 路径），几何证据不可靠时回退视觉证据。",
        "experiments": "VSI-Bench 全划分 5,130 题/288 个第一人称视频：均分 55.4→64.1，相对方向 +28.3（46.1→74.4）、路径规划 +22.7（30.9→53.6），超过 VLM-3R（60.9）、Qwen3-VL-8B（57.4）等训练型方法与全部免训练基线（TRACE 39.4、VideoAnchor 37.8）。按转弯分组（76/80/38 题）：1/2/≥3 转弯 57.9/52.5/47.4，基线为 43.4/22.5/23.7。MindCube 21,154 个稀疏多视角题：23.4→59.8（+36.4），Around 74.6%、Among 58.5%、Rotation 56.2%，总体超 GPT-5.6-Sol（54.1）。消融：几何分支 55.4→62.8（路径 +16.0），超点关联再到 64.1（路径 +6.7）。",
        "innovation": "①发现并量化 MLLM 多转弯路径规划崩塌现象；②前馈重建 + MoGe-2 定标构建共享公制 3D 工作空间，把 2D 定位提升为 3D 关系；③几何超点投票实现无学习的跨视角实例关联；④显式空间算子（A*/占据栅格）与可靠性门控回退结合。",
        "limits": "免训练设计性能受限于 2D 定位与重建质量，残差误差会传播到空间关系、度量估计与路径规划；门控只能缓解不可靠几何、无法恢复缺失证据；增益任务依赖（计数/物体尺寸提升有限）；未做学习式适配，长尾失败模式未系统分析。",
        "repro": "摘要级未明示（正文未见代码或数据发布声明）。",
        "relation_hint": "与 VG-LLM、Spatial-MLLM、VLM-3R、VideoAnchor、TRACE 等空间推理路线互补，差异在全冻结组件 + 显式 3D 计算。",
        "track_hint": "感知与认知"
    },
    {
        "id": "2610.33966",
        "slug": "InteractiveWorld Verifiable Assistant Env",
        "venue": "arXiv preprint（Meta / Duke University）",
        "tags": ["具身助手评估", "闭环交互基准", "Isaac Sim", "多模态大模型", "人机协作"],
        "conclusion": "首个可验证人-助手闭环环境 + 120 任务 InteractiveBench：12 个前沿 MLLM 中最佳者 Claude Fable 5.1 仅 41.7% 通过率，Oracle 100%。",
        "problem": "可穿戴第一人称 AI 助手的测试依赖昂贵且稀缺的真实人类交互数据；现有基准几乎全是静态视频问答，模型说什么都不改变世界，无法考察闭环适应、组合能力，也无法回答「今天的 MLLM 能否真正在物理世界帮到人」。",
        "method": "三层架构。物理层：SMPL+H 全身模型 + 头部第一人称相机，运动学驱动保证确定执行；预检导航路径与手臂可达性，自动微调抓握位姿，不安全动作被拒绝并反馈原因；导入 BEHAVIOR-1K 的 8,000+ 物体与 50+ 场景资产。人类动作层：碰撞感知 A* 自主导航到可达站姿 + 目标驱动自适应操作（站/俯/蹲、无碰撞手臂轨迹、按物体形状与功能部件抓握）。语义层：36 个动作原语统一接口（[Grab]<cup> 等），助手用自然语言指导、人类 MLLM 代理解释并执行，环境每步更新状态并渲染新第一人称视角，任务成功由终态对象关系自动验证。",
        "experiments": "InteractiveBench 120 个人审任务/6 类（各 20）。12 个模型：Claude Fable 5.1 41.7% 通过/54.8% MCR，其余全部 ≤33.3%；Decision 最高 85.0%，Guidance/Planning 仅 20.0%/25.0%。九能力评测：通信最高（79.6%）、主动性最低（44.4%）；感知+记忆错误占首错 70.4%–85.7%；Accessibility/Guidance 需 Oracle 的 2.35–3.66 倍动作。记忆字段增强使 Prevention/Finding 提升 5–15%；16 组助手-人类配对排名稳定，Gemini 3.1 Pro 任人类代理时各助手表现最好。",
        "innovation": "①首个以自然语言指导驱动人类代理、结局可状态验证的闭环交互环境；②首个动态多轮第一人称助手基准（120 任务、状态可验证奖励）；③大规模评测揭示闭环瓶颈：感知/记忆主导失败、通信决定上限、动作效率低下；④提供记忆增强与人类代理消融等机制分析。",
        "limits": "人类代理由 MLLM 模拟，与真实用户存在差距（附录真人验证通过率接近但范围有限）；仅室内仿真场景；主实验固定 Gemini 3.1 Pro 为人类代理；未评估真实可穿戴部署、时延与隐私。",
        "repro": "代码 https://github.com/facebookresearch/InteractiveWorld ，项目页 https://meta-interactiveworld.github.io/ 。",
        "relation_hint": "区别于 Ego4D/EgoPlan 等静态第一人称基准与机器人中心模拟器，定位为人本闭环助手评测平台。",
        "track_hint": "评估与数据集"
    },
    {
        "id": "2610.34283",
        "slug": "ChronoReplay Streaming Spatial SFT",
        "venue": "arXiv preprint（正文未列机构）",
        "tags": ["流式空间智能", "接口锁定", "监督微调", "因果回放", "时空基准"],
        "conclusion": "ChronoReplay 使同一 Qwen3-VL-8B 的 OVO-S/OST/UCS 三基准齐升（+4.91/+13.41/+7.44，均分 56.86 最佳），时序对齐贡献 2.41 分。",
        "problem": "单接口后训练会把改进集中到该读出格式而损害其他接口（接口锁定）：分类-only 训练 OVO-S 达 58.03 却把 OST 从 50.52 压到 47.48，轨迹-only 训练 OST 亦无起色。且度量/时间目标脱离有效因果前缀即歧义：同样前移一步，面北与面东起步对同一旧问题答案不同。",
        "method": "两阶段。Causal Replay construction：保留各源接口原生目标格式（选项语义、单位与精度、时间戳），把监督按 episode 视频时间轴顺序回放，每个目标绑定其合法因果前缀；嵌套前缀使一个 episode 产出 m_i 个共享起点的监督状态，直接训练「累积」本身，不新增地图/记忆模块。Family-balanced learning：preservation 族 33,180 条单轮样本（30,635 分类 + 2,545 数值）与 trajectory 族 6,381 个有序 episode（45,006 个监督轮次）各自族内归一化风险，按 α=0.5 显式配比（轨迹族占 1/3 损失质量），并以答案长度归一化防止长回答主导。仅训练语言模型与视觉 merger（视觉编码器冻结）。",
        "experiments": "统一 Qwen3-VL-8B-Instruct 起点、固定观测访问：OVO-S 48.98→53.89（+4.91，12 个任务族全升，数值接近 Qwen3-VL-235B-A22B 的 53.64）；OST（场景不相交）50.52→63.93（+13.41，15 个子类全正，Direction Est. +26.86）；UCS（8,114 个时间戳因果题）45.33→52.77（+7.44，quantity +10.73）。单族诊断：分类-only 均分 50.74、轨迹-only 50.76，均远低于完整版 56.86。机制对照：时序打乱 -2.41 OST；普通 token SFT 均分 54.10、自然轮次加权 55.57；α=0.5 最优；4 GPU 复现差 0.34。自适应帧选择再 +4.09（OVO-S 57.98，平均 80.50 帧）。",
        "innovation": "①实证命名并诊断「接口锁定」现象；②因果回放构造：原生格式 + 时序对齐，把每个目标绑回有效历史；③族平衡目标显式控制两族损失质量，优于普通联合 SFT 与自然轮次加权；④把观测访问（自适应帧选择）作为正交因子单独分解训练与推理收益。",
        "limits": "仅室内场景与三个基准，机制归因基于匹配 Qwen3-VL-8B 对照；2.41 分的时序贡献是整体构造层面，未分离潜在起源表征；单族对比因来源/任务覆盖差异不能单独归因于答案接口；未新增记忆机制，长时程上限仍存；L4 仍最难。",
        "repro": "代码 https://github.com/yihaohu0118/ChronoReplay ，项目页与 Hugging Face 模型/标注集合；附录含 4 GPU 复现、优化设置与可执行配置。",
        "relation_hint": "与 StreamingBench/OVO-Bench 等流式基准及 Video-R1、Cambrian-S 等空间 SFT 互补，聚焦监督组织而非新架构。",
        "track_hint": "感知与认知"
    },
    {
        "id": "2610.34564",
        "slug": "FlockWorld Multi-Agent Video World Model",
        "venue": "arXiv preprint（Grinnell College / USC / USC Institute for Creative Technologies）",
        "tags": ["视频世界模型", "多智能体", "人工生命", "扩散Transformer", "群体仿真"],
        "conclusion": "FlockWorld+ FlockDiT（27.5M 流匹配 DiT）：密度匹配下联合生成检测率高于独立基线（P=10 时 27.4 对 19.0），扩散 forcing 是最有效的训练策略。",
        "problem": "动作条件视频世界模型多限于单人，现有多人模型只支持小固定群体；缺乏可控的群体规模多智能体视频生成测试床，难以研究联合生成、智能体身份保持与跨视角一致性如何随群体扩展。",
        "method": "FlockWorld：JAX 实现 2D Reynolds Boids（对齐/聚集/分离，25 像素邻域，反射边界，30 fps），100 boids 群体；P 个相机智能体（默认 10）产出同步 128×128 第一人称裁剪，HSV 色相 i/P 编码身份；动作 = 三条规则导出的加速度 (a_x,a_y)，按 4 步因果平均对齐潜帧率。FlockDiT：Wan 2.2 因果 VAE（16×16 空间/4× 时间压缩）潜空间上的流匹配 DiT（8 块、宽 512、约 27.5M 参数），块因果时间掩码 + 全跨智能体注意力；对比 agent-embedded（智能体嵌入 + AdaLN 独占动作路由）与 MIRA 式空间 tiled（RoPE 分块、池化动作广播）两种条件方案，并比较 teacher forcing、diffusion forcing 与单智能体预训练两阶段。",
        "experiments": "28 个留出 episode、每集 10 秒 rollout（2 帧 GT 潜空间初始化，50 步 Euler 求解）。P=10 黑背景：独立单智能体 floor 检测率 19.2，联合基线（Exp.1）28.5、diffusion forcing（Exp.3）26.7（位置误差 1.932 px、SSIM 84.3、检测密度 4.51 接近 GT 5.04），ceiling 96.5；tiled 方案过渲染至 23.14 检测/帧并出现「拼贴合景」失败。P=2–30 扫描（每配置 48 小时等预算）：P=10（27.4 对 19.0，密度 7.11 对 7.48）与 P=30（26.5 对 19.2）证据最强；P=5/8/20 因模型约 2.5 倍过渲染而混淆；P=2 增益（22.7 对 20.1）落在 episode 波动内。",
        "innovation": "①首个群体规模多智能体视频世界模型测试床，相机智能体数与群体规模解耦；②规则导出加速度作为每智能体动作信号；③联合多视角生成与两种智能体条件方案的系统对比；④证明一致性指标被渲染密度混淆、必须与匹配参考（floor/ceiling）对照判读。",
        "limits": "2D 人工生命设置与真实 3D 社会交互差距大；过渲染与 tiled「拼贴合景」失败未根治；全跨智能体注意力随 P 缩放成本高（作者建议邻域稀疏化）；P=2 增益在波动范围内；部分结论受等预算复现与自动编码器差异限制。",
        "repro": "代码/配置/rollout 视频：https://github.com/wangyz1999/flockworld ；附录含实现细节、超参与资产许可（Solaris/Wan2.2 Apache-2.0、boids MIT）。",
        "relation_hint": "承接 Solaris、MIRA、Gamma-World 的单/多人世界模型，并将其扩展到人工生命群体规模。",
        "track_hint": "世界模型与仿真"
    }
]

out_path = os.path.join("D:/Agent/WorkBuddy/Research/data", "digest_1028_g2.json")
with open(out_path, "w", encoding="utf-8") as f:
    json.dump(digests, f, ensure_ascii=False, indent=1)

# 校验
with open(out_path, "r", encoding="utf-8") as f:
    data = json.load(f)
print("count:", len(data))
keys = {"id","slug","venue","tags","conclusion","problem","method","experiments","innovation","limits","repro","relation_hint","track_hint"}
for d in data:
    missing = keys - set(d.keys())
    extra = set(d.keys()) - keys
    assert not missing and not extra, (d.get("id"), missing, extra)
    assert 3 <= len(d["tags"]) <= 6, (d["id"], len(d["tags"]))
print("all keys OK; tags OK")
print("ids:", [d["id"] for d in data])
