# XR 每日论文雷达 · 2026-11-19（11-18 公告批次）

> **诚实口径**：本批处理的是 **2026-11-18（周三）公告批次**，拉取时刻为 **2026-11-19 02:30（周四）**——公告日 ≠ 拉取日。
> 主批 21 篇的 API published 提交日为 **11-17×17 / 11-16×3 / 09-27×1**
> （2611.21642 RelicTouch 提交 2026-09-27、延迟约 7 周公告）。RSS 的 published 字段是公告时间戳，不可当提交日。
> 另设 **backfill-1119** 批次（4 篇旧稿 v2/v3 再公告，非当日新提交），单独报告。

## 一、执行摘要

- **规模**：11-18 公告组 **599 槽位 / 496 篇唯一论文**（cs.CV 207 / cs.GR 10 / cs.HC 26 / cs.MM 3 / cs.RO 89 / cs.AI 259 / eess.IV 5），全部未入馆；RSS 全量 766 条覆盖 listing 496/496（缺收 0）。
- **入选**：摘要级 KW 命中 37 篇 + 标题级补扫 21 篇 → 58 候选 → 逐篇核摘要剔除 37 篇误命中 → **XR 21 篇**（0 S / 12 A / 7 B / 2 C）。
- **全文**：25 候选（21 + 4）串行抓取，**25 篇全部 L0/FULL**（17,275–130,366 字符）；无 PARTIAL、无摘要级评估。
- **三关**：门① 最大 Jaccard **0.261**（<0.62）；门② 定稿 Top10 覆盖 **6 赛道**（全批 8，纯值排序即达、未重筛）；门③ 当日最高 **4.30 vs 库内近 30 天 Top10 均分 **4.4230**（窗口 2026-10-20~11-19、436 条入窗、按 batch 剔除本批两批）→ **非重磅日，无 S 级**（margin -0.1230）。
- **本批主线**：
  1. **端侧 3DGS 从「能跑」进入「跑得动、跑得稳」**——CueSplat 把 4DGS 形变评估变成可学习调度（Jetson Orin 上 1.75–6.74×、PSNR 仅降 ≤0.16 dB），Cross3DGS 把训练搬到采集设备（八种跨厂商 GPU 全部跑完 30k 步、跨设备 PSNR 差异 <0.07 dB）。
  2. **手部/化身链条继续加厚**——HandRSI 用编码 agent 递归改进 harness 与权重（HOT3D MPJPE-p 12.97→8.37 mm、jitter −52%），ARG-Avatar 用几何先验替代 scaling（68M 参数超 609M 的 LHM++ 2.73 dB），HandUMI 用 Quest/PICO + 手戴夹爪采集双臂数据（ACT 折毛巾 12/20 对基线 0/20）。
  3. **空间智能从静态走向动态**——MentalGrid 把「无中间视觉反馈的状态推演」形式化为 SSP/FSP/DPT 三档基准（最佳模型 58.93% vs 人类 74.73%），SpatialCast 用投射阴影做物理读数（GRPO 使 8B +14.33 点），SpatialMind 做任务条件化的多层级几何融合（VSI-Bench 同规模第一）。
  4. **重建侧工程化收敛**——CoSphere-SLAM 把多机全景 ATE 从 1.353 压到 0.082 m，Kolibri 把建筑尺度重定位压到 82 ms/帧，Refin3R 用 SfM 引导把稠密 point map 的 AUC@1cm 提升 24–35%。
  5. **硬件显示侧连续第 30 批无器件级破冰**（波导/可变焦/Maxwellian/光场均无新稿）；本批触觉侧仅一篇 100 美元级振动触觉像素阵列（3.00 B）。
- **S 级说明**：本期 **0 篇 S**。最高 4.30（CueSplat / HandRSI 并列）未达库内近 30 天 Top10 均分 4.4230，门③ 明确判非重磅日，未触发险过条款。

## 二、排行榜（按加权降序，Top10）

| # | 论文 | 赛道 | 总分 | 等级 | 证据 | 关键数字 |
|---:|---|---|---:|---|---|---|
| 1 | CueSplat：学习调度稀疏形变以实现边缘设备上的动态高斯泼溅（2611.22095） | 神经渲染 | 4.30 | A | FULL | 12 组 backbone–dataset 组合（E-D3DGS / 4DGaussians / GaGS / SpeeDe3DGS × Technicolor / N3DV / NeRF-DS）在 Jetson AGX Orin 上取得  |
| 2 | HandRSI：手部姿态估计的递归自我改进（2611.22164） | 化身与人体 | 4.30 | A | FULL | HOT3D 上 MPJPE-p 从 ACE-Ego-Hand 的 12.97 mm 降到 8.37 mm（-35%），ARCTIC 留出 subject s05 上 15.58→13.85 mm（-11%）；jitter 分别 2.82→1 |
| 3 | CoSphere-SLAM：带球面回环的多智能体全景高斯泼溅 SLAM（2611.22235） | 重建与SLAM | 4.15 | A | FULL | Holo360D 45 个测试场景：单 agent per-agent ATE 0.150 m、100% tracked，对比 DROID-SLAM 1.610、DPVO 1.576、MASt3R-SLAM 0.651、OpenVSLAM  |
| 4 | Cross3DGS：从工作站到移动设备的统一 Vulkan 3D 高斯泼溅训练（2611.22240） | 系统与平台 | 4.15 | A | FULL | 八个配置（NVIDIA PRO6000、Intel Iris Xe、Intel UHD730、Arm Mali G1-Ultra、Qualcomm Adreno740、AMD RX9070XT、Apple M5Pro、Apple A14）全 |
| 5 | 从感知到模拟：揭示并增强多模态大模型中的心理空间动力学（2611.22541） | 感知与认知 | 3.92 | A | FULL | MentalGrid 上 12 个 MLLM 评测：最佳 Gemini-3.1-Pro 仅 58.93%，低于人类 74.73% 约 16 个百分点；开源模型多在随机水平附近。 |
| 6 | ARG-Avatar：以动画-渲染引导实现高效前馈化身重建（2611.22207） | 化身与人体 | 3.85 | A | FULL | 分布外 NeuMan 6 视角：30.82 dB PSNR / 0.975 SSIM / 0.016 LPIPS，比 LHM++ 的 28.09/0.972/0.022 高 2.73 dB；2 视角 29.17 对 27.97；1 视角 2 |
| 7 | Kolibri：颜色找位置、精化定姿态——彩色点云中的 RGB-D 定位（2611.22829） | 重建与SLAM | 3.85 | A | FULL | ScanNet-96（96 房间 / 7,986 帧，房间已知，5 cm & 5°）：Fast 81.4%±1.8 vs GeDi 80.3%±1.9（统计等价），BUFFER-X 69.4%、RGB GeoTransformer 77.8 |
| 8 | HandUMI：用于无机器人双臂数据采集的模块化手戴平行夹爪接口（2611.22146） | 交互与输入 | 3.72 | A | FULL | 跨本体重定向：七个模拟双臂的中位位置误差 0.03–1.17 mm（PiPER 1.17、OpenArm 0.14、TRLC-DK1 0.18、YAM 0.19、Metal 0.09、R1 Lite 0.03、ARX X5 0.09），ep |
| 9 | SpatialMind：面向多模态大模型空间推理的自适应多层级几何融合（2611.22415） | 感知与认知 | 3.65 | A | FULL | VSI-Bench 上 SpatialMind-5B 得 71.5，居 3-5B 组第一；同训练数据的 SpatialStack-5B 为 69.6。 |
| 10 | SpatialCast：通过投射阴影读取三维世界（2611.22657） | 感知与认知 | 3.65 | A | FULL | 合成测试集 4,500 题上，GPT-6.1 Sol 总体 79.42%（T1 67.50 / T2 88.39 / T3 85.33），Gemini 4 Argon 57.71%；四个开源基座与 Spatial-SSRL、SpatialB |

## 三、逐篇深度解读

> 以下 10 章按价值降序，对应 Top10。每章含问题、方法、结果、创新、深读要点、局限、库内关系、可复现性与行动建议。

### 1. CueSplat：学习调度稀疏形变以实现边缘设备上的动态高斯泼溅（2611.22095）

**赛道**：神经渲染　**总分**：4.30（A）　**证据**：FULL/L0　**7 维**：IMP 4 · NOV 4 · TEC 5 · EXP 5 · PER 5 · TRL 3 · REP 3

**一句话结论**：冻结 4DGS 主干、按预测可靠性与渲染贡献调度稀疏形变评估，Jetson AGX Orin 上取得 1.75–6.74× 加速，PSNR 仅降 ≤0.16 dB。

**要解决的问题**：基于形变的 4D Gaussian splatting 在每个时间步都要对所有 Gaussian 求解形变网络，边缘设备上代价极高——E-D3DGS 在 Jetson AGX Orin 上形变约占 GPU 流水线时间的 85%。现有加速依赖 Gaussian 剪枝、静动态分解或共享运动表示，但剪枝与限制运动表达会损伤重建质量，静动态划分在渲染期间固定不变，把动态 Gaussian 误判为静态会破坏运动重建。

**方法详解**：CueSplat 是 post-training 框架：冻结预训练 backbone 的 canonical Gaussian 与形变参数、保留完整 Gaussian 集合，只在其上做稀疏形变调度。其动机来自测量——五帧内 static/linear/quadratic 拟合可覆盖 N3DV 66.2%、Technicolor 68.8% 的 Gaussian-window 对，但 54.4% 采样 Gaussian 在某些窗口满足五帧拟合、在另一些窗口违反，说明局部规律存在而可靠性随 Gaussian 与时间变化。在线推理先用最近三个已接受状态做阻尼有限差分外推预测全部属性（位置 λ_v=0.85、λ_a=0.15；旋转用阻尼四元数增量；尺度保持；动态外观从同三帧滤波；静态属性取 canonical 值），再由轻量 MLP router（约 2.0k–2.6k 参数）依据冻结 descriptor、编码时间戳与运动/可见性/贡献/更新年龄等在线特征打更新分，取 TopK 作为精确更新子集，替换预测值后合并渲染。为降低路由开销，每 N=5 帧才重算特征与索引并在帧间复用，但被选中的 Gaussian 每帧仍做精确形变。离线先按 rendering-aware risk ρ=m_vis·o·πr²/(HW)·[log(1+e)]² 标定场景级预算 K_s（取标定帧提议的 90 分位并向上取档），经 oracle 闭环检查（代理 PSNR 均值 ≥40 dB、10 分位 ≥37 dB）通过后，用教师信号（五类属性误差按帧内中位数归一后由可见性、不透明度、投影半径加权）生成 top-k 二值标签与连续优先级，以 ranking + BCE + SmoothL1 三项损失训练 router，再做第二轮闭环验证，不达标就升档。为控制误差累积，用漂移信号 d_t=0.4Ē+0.2r̄+0.2m̄+0.2a 触发连续三帧全形变刷新（最小间隔 20 帧、连续两次帧级分数 ≥0.6 触发、最迟 s+40 强制），并把刷新所需的精确评估分摊到前 10 帧预计算以削平延迟尖峰。

**实验与结果**：
- 12 组 backbone–dataset 组合（E-D3DGS / 4DGaussians / GaGS / SpeeDe3DGS × Technicolor / N3DV / NeRF-DS）在 Jetson AGX Orin 上取得 1.75–6.74× 加速，数据集平均 PSNR 下降至多 0.16 dB；Orin NX 上 1.81–8.15×，A6000 上峰值 5.04×。
- 代表点：Technicolor 上 GaGS 由 10.65 FPS 提升至 71.79 FPS（6.74×，PSNR 32.99→32.92）；N3DV 上 E-D3DGS 15.64→38.24 FPS（2.45×，27.92→27.88 dB）；NeRF-DS 上 4DGaussians 72.26→126.27 FPS（1.75×）。
- 慢帧性能：GaGS/Technicolor 的 FPS P5 由 10.63 升至 52.58；加刷新预计算后 N3DV 上 FPS P5 由 17.68 升至 26.20（+48.2%），平均吞吐只降 0.3%（40.95→40.81 FPS）。
- 执行计算量：服务端 profiling 显示每帧 GPU warp 指令减少 29.9%–90.7%，GaGS/Technicolor 由 8206.42M 降至 760.01M。
- 对 DASH：Technicolor 上四个 backbone 的平均 PSNR 均优于 DASH-style 对照，E-D3DGS +0.37 dB、4DGaussians +0.26 dB、GaGS +0.22 dB（FPS 高 81.3%）、SpeeDe3DGS +1.19 dB（+26.3% FPS）；但与官方 DASH 复现（31.12 dB / 39.13 FPS）相比，SpeeDe3DGS+CueSplat 为 30.91 dB / 37.50 FPS，略低。
- 消融（Technicolor 50 帧、四 backbone 平均）：学习路由比 motion-magnitude 排序高 1.44 dB（32.50 vs 31.06，LPIPS 0.0914 vs 0.1018）；时间外推比 hold-last 高 0.21 dB；场景级预算比统一 20% 预算高 1.22 dB；三帧刷新比单帧刷新 PSNR 27.50→27.88 dB（FPS 41.83→38.36）。

**创新点**：把“选择性计算”引入冻结的 4DGS 形变网络：不剪枝、不改 Gaussian 集合、不做静动态硬划分，而是把每帧形变评估变成按预测可靠性与渲染贡献动态分配的预算，这是相对剪枝、分解、共享运动三条现有加速路线的实质差异。router 由教师信号监督，并配合离线 oracle 与闭环质量门控的场景级预算标定，使加速比随场景风险自适应而非全局固定。漂移触发的三帧历史重建加上刷新预计算，补上了“预测-反馈”闭环里误差累积与延迟尖峰两个工程缺口。

**深读要点**：值得关注的是「调度」而非「剪枝」：Gaussian 集合与形变网络都不动，只决定每帧对哪些 Gaussian 求形变，因此质量损失可压在 0.16 dB 内。工程上要留意两点——router 需按 scene×backbone×budget 逐组训练（A6000 上 1–2 分钟准备），且实现假定均匀时间步顺序渲染，时间跳转/变速播放尚不支持。

**局限与风险**：作者在结论中明确承认当前实现假定按均匀时间步顺序渲染（'The current implementation assumes sequential rendering at uniform time steps'），时间跳转（temporal seeking）与变速播放尚不支持，被列为未来工作。每个 scene–backbone–budget 组合都要单独训练 router，场景级准备在 RTX A6000 上需 1–2 分钟、预算升档再加约 1 分钟，部署前准备成本不低。Technicolor 的 50 帧序列在初始化后直接禁用刷新，说明刷新机制在短序列上未经检验；与 DASH 官方复现相比 SpeeDe3DGS+CueSplat 的 PSNR 与 FPS 都略低，跨方法比较并非全面占优。

**与文献库的关系**：库内 4DGS 加速多为剪枝/静动态分解（如 2610.x 的动态 GS 压缩线），本篇是「冻结主干 + 可学习调度」的第一篇，属新增而非取代。

**可复现性**：正文未提供代码；全文 51,532 字符（L0/FULL）。

**行动建议**：纳入重点精读；无公开代码，需按正文细节复现。

### 2. HandRSI：手部姿态估计的递归自我改进（2611.22164）

**赛道**：化身与人体　**总分**：4.30（A）　**证据**：FULL/L0　**7 维**：IMP 4 · NOV 4 · TEC 5 · EXP 4 · PER 5 · TRL 4 · REP 4

**一句话结论**：编码 agent 递归改写推理 harness 并按信息源蒸馏回网络，配合十指标无回退门，HOT3D MPJPE-p 12.97→8.37 mm（−35%）、jitter −52%。

**要解决的问题**：第一人称 3D 手部姿态估计在图像边界漏手、遮挡时深度错位、指尖抖动，现有做法靠手写推理后处理（harness）加网络微调两步修补，但两步分别调参且彼此耦合：网络一旦更新，原有修正可能冗余甚至有害。3D 感知的质量又是多维的（检测、3D 位姿、2D 对齐、放置、平滑度互相 trade-off），只对一个指标设门会放进损害其他维度的改动。作者要回答的是：能否让编码 agent 递归地同时改进 harness 与网络，而每次改动都不牺牲任何一项指标。

**方法详解**：系统被定义为估计器 theta 与可执行推理 harness H^I 的组合 S=(theta, H^I)；harness 是一串只读预测、帧与内参、绝不接触 GT 的确定性模块，每个模块只看一个 81 帧片段。Loop A 让 8 个编码 agent（4 个 Claude Opus 5.5/Claude Code、4 个 GPT-6-sol/Codex）并行改 harness 四小时，各领一个方向：检测、root 放置、朝向、手指、图像证据、时序、2D 关键点、出画手。提交先在 dev 免费预检，再在 val 上过 G_A=G_0.3%：十个指标（七个误差列加 FAcc/Recall/F1）逐项算相对改进并 clip 到 ±5%，取均值得 Delta，要求 90% paired bootstrap 下界 L_Delta>0、Delta 不小于阈值，且任何指标不得在显著时退化超过 2%、无条件退化超过 5%。通过的模块在 dev 上按 val 增益贪心合并，集成 agent 消解重叠，再用一次 val 比较在最佳提交、贪心合并与集成链之间选出 H^{I,star}。Loop B 把 GT 微调后的网络 C^1 加精炼 harness 当作教师，按信息源拆分监督：3D GT 监督 2D、腕相对、root、朝向与存在性，教师只在无 GT 帧与无标注视频上监督存在性与时序（关节速度与加速度的 Huber，delta=5 mm）。学生只训 rank-32 LoRA（DiT block）与预测头，lambda_GT=2、lambda_KD=0.25、lambda_e=0.5、lambda_R=0.25，lr 1e-4、LoRA+ 比例 4、batch 8 个 85 帧窗口、500 或 2,000 步，过了网络门 G_B 才替换 theta。随后在 dev 上对每个 harness 模块做 leave-one-out 成对消融，把冗余、显著有害或使单条录制 EPE 恶化两倍以上的模块联合剔除，再过回合门 G_1%。Loop C 由规划 agent 读取档案（门结果、val 聚合、dev 诊断与全部提交，永不见 test）产出下一轮 guidance 与至多两个白名单 Loop B 设置。最后在 val 上搜索 harness 子链，用 (log FPS, Delta) 上的 epsilon-dominance 与 hypervolume 选出 Lite/Medium/Heavy 三个嵌套部署档。

**实验与结果**：
- HOT3D 上 MPJPE-p 从 ACE-Ego-Hand 的 12.97 mm 降到 8.37 mm（-35%），ARCTIC 留出 subject s05 上 15.58→13.85 mm（-11%）；jitter 分别 2.82→1.34 与 2.58→1.45 mm/frame^2（-52% 与 -44%）。
- 相对在相同 GT 上微调的 ACE-Ego-Hand（C^1，HOT3D MPJPE-p 9.91 mm），HandRSI 再降 MPJPE-p 16%、EPE 2D-p 27%、jitter 51%。
- 对九个复跑的已发表方法（WiLoR、HaWoR、EgoForce、HaMeR、Hamba、WildHands、InterWild、OmniHands 与 ACE-Ego-Hand），在 HOT3D 与 ARCTIC 的全部十个指标上均为最优；HOT3D 上 FAcc 0.982、Recall 0.996、MPJPE-p 8.37 mm、EPE 2D-p 4.07 px、CT-p 0.013 m。
- 三个部署档 Lite/Medium/Heavy 分别为 41.1/34.0/20.7 FPS（HOT3D MPJPE-p 9.06/9.04/8.41 mm），Lite 只比网络本身慢约 4%，仍全面优于所有已发表方法。
- 零样本 HOI4D（498 段）上 3D 位姿类指标最低（MPJPE-p 22.77 mm、jitter 1.01 对比 ACE 的 2.10），但 2D 误差 18.61 px、CT-p 0.064 m 落后于 ACE-Ego-Hand。
- 五轮共 156 次提交、73 次通过 G_A；蒸馏在第 2 轮后饱和，第 3 至 5 轮所有学生都以 1.7%–9.3% 的 2D/朝向/召回损失换 1%–3% 的 jitter，Delta 转负（-0.8% 至 -2.7%）。

**创新点**：把「编码 agent 改 harness、按信息源蒸馏进网络、网络更新后重验 harness」做成闭环，并用十指标 no-regression 门把多维 3D 感知的质量约束进搜索，避免单指标门控引入的 trade-off。首次把 harness 优化从「产出文本或程序」搬到度量 3D 感知上，并显式区分「harness 带来的增益」与「蒸馏进权重的增益」，配合逐轮 GT-only 与 harness-only 控制把两者拆开。除了精度，还给出超参数量与速度分档、以及可复现的评测器与结果文件。

**深读要点**：这篇的真正贡献是把「推理后处理」也纳入可学习闭环：编码 agent 改 harness、按信息源蒸馏回网络、网络更新后重验 harness。读的时候重点看它的十指标 no-regression 门——单指标门控会引入 trade-off，这是 3D 感知这类多维指标任务的通用陷阱。局限也在这：第 1–2 轮曾参考 test 分数做决定，隔离并不彻底。

**局限与风险**：蒸馏在第 2 轮后饱和：后续十二个学生 checkpoint 都以 1.7%–9.3% 的 2D/朝向/召回损失换 1%–3% 的 jitter，Delta 转负，作者归因为 LoRA 预算下 harness 仍能提供的放置与关节拟合无法被学生吸收。第 1 至 2 轮操作者曾参考 test 分数做三个决定（Loop B 配方与两条门规则），第 1 轮还在 HOT3D FAcc r=-5.6% 超过 5% 上限时被人工接受，test 并非完全隔离。评测器是作者按 ACE-Ego-Hand 附录重写的（官方未公开），EPE 2D-p 因 miss 罚则定义不同而有偏差；HOI4D 上 2D、放置与检测仍落后于基线，增益主要来自 HOT3D/ARCTIC 相机。

**与文献库的关系**：库内手部追踪以单点模型为主（WiLoR/HaWoR 系），本篇是系统级的 harness+蒸馏闭环，属新增范式；与 11-18 的 WinDEX/MetricHand 构成「精度—工程」互补。

**可复现性**：代码/项目页 https://github.com/GinKenneth/Hand_RSI（权重与各轮 harness：https://huggingface.co/HandRSI/HandRSI）；全文 107,033 字符（L0/FULL）。

**行动建议**：纳入重点精读，先跑通公开代码再评估迁移成本。

### 3. CoSphere-SLAM：带球面回环的多智能体全景高斯泼溅 SLAM（2611.22235）

**赛道**：重建与SLAM　**总分**：4.15（A）　**证据**：FULL/L0　**7 维**：IMP 4 · NOV 4 · TEC 4 · EXP 5 · PER 5 · TRL 3 · REP 3

**一句话结论**：把回环改成 S² 上的 SO(3) 相关并用三 agent 全局 Sim(3) 一致拒绝对称假回环，全景多机 SLAM 单机 ATE 1.610→0.150 m、多机 1.353→0.082 m。

**要解决的问题**：多智能体稠密建图需要全景相机，但把全景高斯 SLAM 扩到多 agent 有三个耦合难题。任意 pitch/roll 下 equirectangular 的 yaw 是循环移位、tilt 会按纬度扭曲，平面匹配失效；全 3D 旋转搜索会把对称房间匹配成「互相一致的错误变换」，整片区域支持同一对称时成簇 outlier 无法被成对 robust kernel 拒绝；单目尺度持续漂移会让刚性合并的子图在重访墙处裂开，短基线深度噪声又按场景深度放大、扭曲回环平移方向。

**方法详解**：每个 agent 把 equirectangular 重采样成六个共享光心的 90 度 cube face，用冻结的 DROID-SLAM 前端以 T_i R_f^T 联合跟踪六面，得每关键帧一个 SE(3) 位姿 T_i。在更宽的重叠面上预测单目深度，按面做 log-scale 线性最小二乘对齐成球面深度 D_i；深度只约束前若干关键帧，之后靠多视光流与 agent 内回环。同时把水平面特征按行平均成 128x32 的 ring descriptor（8.1 KB），与位姿一起上传；服务端把六面稠密特征重采样到 HxW 单位方向网格，得球面特征图 F_i: S^2 到 R^C，把回环写成 F_j(x) 约等于 F_i(R_ij x)。先用 ring descriptor 的循环互相关做全部对的粗筛（yaw 化为列移位、对 tilt  tolerant），只对 top 对请求面与深度。球面相关把 R 分解为水平轴 tilt Q 与竖轴 yaw R_z(psi)，固定 Q 后沿经度做 1D 循环互相关，用一次逆 FFT 求出所有 yaw；粗到细扫 N_Q=108 个 tilt（7.5 度到 30 度，再 3 度精化），复杂度 O(N_Q C H W log W)，覆盖 360 度任意朝向。以 R* 初始化做六面 6-DoF 光流精化，把置信对应反投影成 3D 点对，用加权 Umeyama 解 Sim(3)，同时得到相对尺度、旋转与平移。全局 Sim(3) consensus 把每个候选变换按局部位姿转成 agent b 到 a 的相似变换并聚类，在「每对至多选一个簇」约束下最大化支持度，要求任意三 agent 闭环的乘积约等于 I（tau_t=1.0 m、tau_R=5 度），用至多 729 个 CPU 状态穷举，从而拒绝整片区域服从同一对称 G 的假簇。定向全局优化给每关键帧一个 Sim(3)，残差含旋转、局部系平移与 log-scale 三行；odo 边令 s 的观测为 1，使 log s 沿轨迹随机游走、在两次相遇间线性插值；回环平移取 Umeyama 的模长与光流的单位方向，信息矩阵沿该方向与垂直方向各给 lambda 平行、lambda 垂直，DCS 权重再按 1/m_ij 平衡长相遇与短相遇。全向高斯融合用射线式高斯求值（低通 A=(Sigma+kappa^2 ||mu||^2 I)^-1，解析最大响应 tau* 与闭式 alpha(d)）避免极点拉伸与接缝断裂；每个高斯按所属关键帧的 S_i 变换（协方差乘 s_i^2）；最后固定尺度，用立体角加权的 |I-I_hat| 加 SSIM 联合精化高斯与位姿，并对 SSIM 窗口施加随机 3D 旋转以避开极点。

**实验与结果**：
- Holo360D 45 个测试场景：单 agent per-agent ATE 0.150 m、100% tracked，对比 DROID-SLAM 1.610、DPVO 1.576、MASt3R-SLAM 0.651、OpenVSLAM 0.543、ODGS-SLAM 1.613；多 agent 0.082 m，对比 MAGS-SLAM 1.353、CoMo3R-SLAM 0.606、OpenVSLAM-M 0.715。
- 45 场景 joint ATE 0.152 m，对比 MAGS-SLAM 3.165、CoMo3R-SLAM 5.054、OpenVSLAM-M 1.882；五个最长测试场景 mean ATE 在 0.053 到 0.300 m。
- 渲染：共享视角 PSNR 28.25 dB 与 LPIPS 0.235，对比 MAGS-SLAM 的 26.09/0.318；对 ODGS-SLAM 为 27.92 对 17.67 dB；Scene 009 novel-view WS-PSNR 28.95 对 PFGS360 的 21.20，full-scene 27.80 对 24.28（Ours Single）。
- 回环：dev 1 m 内相遇恢复 3,950 个回环、95.6% 精度、连上 69.7% 的相遇，前脸匹配只有 1,152 个与 28.9%；45 个测试场景在 33,815 个回环中连上 23,382 个重访，其中 55.3% 的朝向差超过 45 度。
- 360Loc 跨昼夜 18 条会话：多 agent 100% tracked、平均 ATE 0.30 m（四栋楼 joint 0.22 到 0.44 m），对比单 agent 0.88、MAGS-SLAM 2.04（83%）、MAC-Ego3D 23.59、ODGS+RICP 16.39（67%）。
- 多 agent 对齐耗时 3,113 s，比 ODGS+RICP 的 15,132 s 快 4.9 倍；建图 4.3 GPU-hours/agent，PFGS360 为 27.9。

**创新点**：首个多 agent 全景高斯 splatting SLAM，把回环从平面图像匹配改成 S^2 上的 SO(3) 相关：tilt 分解加经度 FFT，使任意 heading 都能在 O(N_Q C H W log W) 内匹配，且不会像针孔相机那样裁掉视野。用三 agent 闭环的全局 Sim(3) 一致性拒绝「整片对称区域共同支持」的假回环，这是成对 robust kernel 在结构上做不到的。把单目尺度漂移建成每关键帧 Sim(3) 的 log-scale 随机游走，并把回环平移的方向（光流）与模长（深度）分开加权；融合端用射线式高斯求值同时消掉极点拉伸与接缝断裂。

**深读要点**：全景多机的关键不在高斯表示，而在回环：equirectangular 的 yaw 是循环移位、tilt 按纬度扭曲，平面匹配直接失效；作者改用 S² 上的 SO(3) 相关（tilt 分解 + 经度 FFT），再用三 agent 闭环的全局 Sim(3) 一致拒绝对称房间的「互相一致的错误变换」。要注意系统是离线服务端式的：1 FPS 输入、A100 上对齐 3,113 s。

**局限与风险**：作者明确假设静态场景且存在共享视野，纯视觉建图不处理动态物体，未来才做球面动态建模与惯性/测距融合以获得 metric scale 与机载部署。系统是离线服务端式的：输入仅 1.0 FPS，服务端对齐 3,113 s，建图在单张 A100 上完成，离在线机载还有距离。实验以 ATE 与 PSNR 为主，无用户研究；正文只给项目页、没有代码仓库。360Loc 上单 agent 0.88 m 与多 agent 0.30 m 的差距也说明跨会话仍依赖多 agent 相遇。

**与文献库的关系**：库内 SLAM 线已有 UniGS-SLAM、DPGS-SLAM 等单机稠密方案，本篇补上「多机 + 全景」维度，属新增场景而非取代。

**可复现性**：代码/项目页 none（正文仅给出项目页 https://cosphere-slam.github.io）；全文 56,002 字符（L0/FULL）。

**行动建议**：纳入重点精读，先跑通公开代码再评估迁移成本。

### 4. Cross3DGS：从工作站到移动设备的统一 Vulkan 3D 高斯泼溅训练（2611.22240）

**赛道**：系统与平台　**总分**：4.15（A）　**证据**：FULL/L0　**7 维**：IMP 4 · NOV 4 · TEC 5 · EXP 5 · PER 3 · TRL 4 · REP 4

**一句话结论**：以同一 Vulkan 数值更新加 256 条设备 schedule，八种跨六厂商 GPU 全部跑完 30k 步标准训练，跨设备 PSNR 差异 <0.07 dB。

**要解决的问题**：手机、平板与智能眼镜拍完 3DGS 场景仍要传回 CUDA 工作站训练，无法在采集设备上完成，也就无法保留隐私、去掉往返或离线使用。把 kernel 改写成跨厂商着色语言并不够：subgroup 宽度、float32 atomic add、storage-buffer 上限与批量命令提交的可靠性在不同 GPU 与 driver 上不同，直接决定一个名义等价的训练步能否执行并返回正确更新。现有可移植训练器 VkSplat 与 Brush 在部分移动 GPU 上根本跑不完标准质量训练。

**方法详解**：保留一个优化器 U(theta, I)（投影、tile binning 与排序、alpha 合成、损失、梯度、Adam；MCMC 细化在 U 之外），把「怎么在 GPU 上执行 U」抽象成六个选项：梯度方法（4 种 work assignment 乘 3 种 merge，共 8 值）、命令提交（batched 8 updates 或 fenced）、训练图像（resident 或 streamed）、radix sort（subgroup 或 portable）、projection+Adam（fused 或 split）、pair dispatch（indirect 或 direct），共 256 条 schedule。第一步用 13 条 feasibility rule 排除已知跑不对的 schedule：5 条读设备限制（subgroup 宽度、shared memory、storage-buffer range、float32 atomic add、vendor id），4 条读 workload（高斯容量、图像尺寸、训练图数量），4 条编码在特定 driver 上观测到的失败（全部 key 在 Qualcomm）。第二步不做设备端计时，用固定 preference order 在剩余可行 schedule 里逐选项取第一个可用值；AMD 与 Intel 各有一份离线定的顺序，其余厂商共用通用顺序。正确性不靠 bit 对齐：定义数值一致性 |q_hat - q| 不超过 eps_abs + eps_rel|q|（q 为梯度或 Adam 更新量），离线把每个可行梯度方法与同卡 reference（exact pair gather）比，再让每设备选中的 schedule 与独立 CPU 双精度实现比，并用故意漏掉一个 tile partial 的负对照证明测试会失败。实现是一个 C++20 训练库加自研小型 Vulkan compute runtime（多 pass program、exclusive scan、headless context、运行时 GLSL 到 SPIR-V），所有梯度手写 kernel，参数、优化器状态与活跃高斯数常驻 GPU 固定容量 buffer，command buffer 录一次反复 replay。桌面、Android 与 iOS 共用同一 core，Apple GPU 走 MoltenVK，RX9070XT 走 Mesa RADV；标准质量设定为 30k updates、SH degree 3、MCMC 细化、100 万高斯容量、0.8 L1 加 0.2(1-SSIM)。上层是 Android（ARCore 采集加 CPU COLMAP 端口）与 iOS（ARKit）的 capture-to-view 应用，采集、SfM、训练与查看全在设备上完成。评测用 Mip-NeRF 360 七个场景、Tanks and Temples 的 Train/Truck、Deep Blending 的 DrJohnson/Playroom，每八帧留一帧，统一 evaluator 算 PSNR/SSIM/LPIPS，每配置三次取中位数。

**实验与结果**：
- 八个配置（NVIDIA PRO6000、Intel Iris Xe、Intel UHD730、Arm Mali G1-Ultra、Qualcomm Adreno740、AMD RX9070XT、Apple M5Pro、Apple A14）全部完成 30k updates 与 100 万高斯的 standard-quality 训练；VkSplat 只在 4/5 个桌面配置完成（UHD730 在前 200 步挂死 GPU），Brush 完成 6/8（Adreno740 超出 128 MiB storage-buffer）。
- 跨设备最终质量几乎一致：bicycle 的 PSNR span 0.019 dB（25.28 到 25.30），garden 为 0.063 dB（26.97 到 27.03）；SSIM 与 LPIPS 变化不超过 0.001。
- 训练时间跨约两个数量级：PRO6000 115 s，两台 Android 与 iPhone 2.36 到 3.23 h，UHD730 3.44 h。
- PRO6000 11 场景 macro：Cross3DGS 27.86/0.883/0.139、136.8 s；VkSplat 27.79/0.882/0.143、139.3 s；Brush 27.90/0.885/0.138、426 s（约 3 倍时间）。对 VkSplat 的 PSNR 增益 0.074 dB（95% 区间 0.002 到 0.14），时间差 4.4 s 的区间含 0。
- 更新一致性：同卡各可行梯度方法与 exact pair gather 的最大差为 3.4e-8（梯度）与 1.5e-6（Adam），对 CPU 双精度 oracle 的最大差 1.6e-5，零越界；负对照（故意漏掉一个 tile 的 partial）产生 29,921 个违规。
- 移动端能耗：Adreno740 16.9 Wh（6.0 W）、G1-Ultra 7.2 Wh（3.0 W）、A14 在 25.5k/30k 步约 9.2 Wh；应用从采集到可看模型 28 到 46 分钟，SfM（19 到 30 分钟）比 3DGS（7 到 18 分钟）更久。

**创新点**：把「可移植」从「换一门着色语言重写 kernel」重构为「同一数学更新加每设备选一条可行 schedule」：256 条 schedule 的目录、13 条读设备限制/workload/driver 的可行性规则、以及不在设备上计时的固定偏好序，使八个跨六厂商的配置都能跑完标准质量训练。把正确性形式化成更新级数值一致性测试（含 CPU 双精度 oracle 与负对照），而不是只看 PSNR 是否像样。工程上给出同一 C++20 core 经 MoltenVK 与 RADV 覆盖桌面、Android、iOS 的完整链路，以及可用的 capture-to-view 应用。

**深读要点**：把「可移植」从「换一门着色语言」重构为「同一数学更新 + 每设备选一条可行 schedule」，这是系统论文的正确抽象。八种跨六厂商配置全部跑完 30k 步、跨设备 PSNR 差异 <0.07 dB，说明正确性而非性能才是卖点。代价是固定偏好序牺牲设备最优速度（RX9070XT 上慢 2.94×），且四条 driver 规则只在一个 Adreno740 上验证过。

**局限与风险**：作者自述固定偏好序是为可预测部署牺牲设备最优速度：每厂商的顺序只在单一设备与 driver 上定，同厂商其他设备可能排序不同；通用序在 RX9070XT 与 UHD730 上选出的方法比最快可行方法慢 2.94 与 4.17 倍。四条 driver 规则全部 key 在 Qualcomm、只在一个 Adreno740 与一个 driver 上测过，换 GPU 或新 driver 可能误排除本可运行的 schedule（只损速度不损正确性），而未预期的 driver 失败在发生前无法被规则捕获。证据范围有限：跨设备质量只覆盖两个场景，11 场景对比只在 PRO6000；与 VkSplat/Brush 是系统级比较，视图顺序、优化器状态与 densification 轨迹都不同；头显与智能眼镜留作未来工作。

**与文献库的关系**：库内 3DGS 系统工作多在 CUDA 侧优化吞吐，本篇补上跨厂商可移植性，属新增维度。

**可复现性**：代码/项目页 https://github.com/unclearness/cross3dgs（含 Android/iOS 应用与评测脚本）；全文 89,534 字符（L0/FULL）。

**行动建议**：纳入重点精读，先跑通公开代码再评估迁移成本。

### 5. 从感知到模拟：揭示并增强多模态大模型中的心理空间动力学（2611.22541）

**赛道**：感知与认知　**总分**：3.92（A）　**证据**：FULL/L0　**7 维**：IMP 4 · NOV 4 · TEC 4 · EXP 4 · PER 4 · TRL 3 · REP 4

**一句话结论**：把无中间视觉反馈的多步空间状态推演形式化为 SSP/FSP/DPT 三档基准，SpatialWalker-3B 从 12.54% 提到 46.35%，仍低于人类 74.73%。

**要解决的问题**：现有 MLLM 空间推理研究与基准基本假设静态环境，只需对输入图像/视频做单次感知即可定位物体。真实环境是动态的：给定语言描述的动作序列后，模型必须在不看中间画面的情况下推演空间状态如何演化（作者称为 spatial simulation），而这一能力缺乏系统评测。已有心理模拟工作多局限于孤立物体或受限视角，未覆盖长程状态转移。

**方法详解**：构建 MentalGrid 基准：用 Habitat-Sim 从 ReplicaCAD、ArchitecTHOR、iTHOR、ProcTHOR、RoboTHOR 采集 349 个场景，渲染 1,100 张多视角图，生成 3,356 个 QA。状态定义为 S_i=(P_i, v_i, o_i)，P_i 为物体 2D 坐标集合，v_i 为 agent 位置，o_i 为 agent 朝向；动作为平移 f_t 与旋转 f_r 两类映射。按状态下标划分三任务：SSP（i=0，静态感知基线）、FSP（i=n，预测终态）、DPT（0<i<n，追踪任意中间态及相邻转移）。查询分 Distance-Object、Object-Distance、Direction-Object、Object-Direction 四类，并区分 allocentric（ALLO）与 egocentric（EGO）参考系。质量控制包括剔除占图像像素 <0.1% 的物体、去除重复/近义类别场景、以距离阈值排除 2D 投影垂直重叠。训练侧构造 16k QA（5,368 SSP / 5,289 FSP / 5,294 DPT），刻意排除 ArchitecTHOR 与 iTHOR 作域外测试；用 GPT-5-mini 逐步推理生成 CoT，仅保留准确率 >0.9 的轨迹。采用三阶段课程：Stage 1 在 SSP 上 SFT 建立感知锚定；Stage 2 在 FSP+DPT 上联合 SFT，用终态目标与过程目标互补；Stage 3 在 DPT 上用 GRPO 强化学习，奖励由格式模板分与预测状态对 ground truth 的准确分组成。基座为 Qwen2.5-VL-3B，得到 SpatialWalker-3B。

**实验与结果**：
- MentalGrid 上 12 个 MLLM 评测：最佳 Gemini-3.1-Pro 仅 58.93%，低于人类 74.73% 约 16 个百分点；开源模型多在随机水平附近。
- SpatialWalker-3B 总体 46.35%，比基座 Qwen2.5-VL-3B 的 12.54% 提升 33.81 个百分点，并超过 Gemini-3-Flash 的 45.24%。
- 域内平均 47.79%（+35.63）、域外平均 44.35%（+31.29）；域外 DPT 达 49.01%（+44.09），为各模型最高。
- 外部基准（MindCube / OmniSpatial / STARE）总体 41.42%，比基座高 4.92；OmniSpatial 动态推理（DR.）单项提升 18.81。
- 消融：去掉 Stage 2 总体掉 15.5%；去掉 Stage 3 掉 3.2%；去掉 Stage 1 静态感知掉 6.8%，但 DPT 反升 3.4%。
- 诊断实验：物体数 >20 时 SSP 准确率急剧下降，而 FSP/DPT 对场景复杂度不敏感；动作步数增加时 FSP 明显退化并收敛回原始输入水平。

**创新点**：把「无中间视觉反馈的多步空间状态推演」形式化为可评测任务，并用 SSP/FSP/DPT 三档下标统一定义静态感知与动态模拟，使感知误差与模拟误差可分离（相对 drop 率）。基准的场景、动作序列与答案由模拟器真值程序化生成，避免了真实采集无法获得任意旋转平移真值的问题。训练侧把诊断结论（低复杂度受感知制约、高复杂度受长程推理制约）直接映射为三阶段课程，形成诊断到课程的闭环。

**深读要点**：MentalGrid 把「不看中间画面推演空间状态」拆成 SSP/FSP/DPT 三档，使感知误差与模拟误差可分离——这是评测设计的价值所在。结论也很克制：最佳模型 58.93% 仍低于人类 74.73%，开源模型多在随机水平附近；SpatialWalker-3B 的 +33.81 点主要来自课程训练，而非新架构。

**局限与风险**：任务刻意不考虑物体位姿、材质、碰撞等物理因素，因此不能覆盖真实世界中带物理约束的空间模拟。由于需要对物体与 agent 做任意旋转平移、真实采集成本过高，全部场景均为仿真生成，作者仅以域外实验结果论证向真实场景的迁移。此外绝对水平仍低（46.35%），与人类 74.73%、Gemini-3.1-Pro 58.93% 差距明显。

**与文献库的关系**：库内空间推理基准（SpatialCast、VSI-Bench 系）以静态场景为主，本篇补上动态状态推演，属新增评测维度。

**可复现性**：代码/项目页 https://github.com/BugMakerzzz/MentalGrid；全文 80,243 字符（L0/FULL）。

**行动建议**：纳入重点精读，先跑通公开代码再评估迁移成本。

### 6. ARG-Avatar：以动画-渲染引导实现高效前馈化身重建（2611.22207）

**赛道**：化身与人体　**总分**：3.85（A）　**证据**：FULL/L0　**7 维**：IMP 4 · NOV 4 · TEC 4 · EXP 4 · PER 4 · TRL 3 · REP 3

**一句话结论**：把模板/LBS/渲染的几何对应写进 attention 的 RoPE 与层内 rendering-in-the-loop，68M 参数在 6 视角 NeuMan 上超 609M 的 LHM++ 2.73 dB。

**要解决的问题**：从随手拍照片或单目视频帧重建可动画 3D 化身，feedforward 方法已把推理压到数秒，但近期路线靠堆模型容量、私有数据与算力（LHM++ 609M 参数、约 300K 视频）。作者质疑这种 scaling-first 是否必要：模板锚定的化身本身有表示上限，而现有架构用通用 attention 从数据里硬学「化身元素对应哪块图像」，浪费了模板、LBS 与渲染已经给出的几何对应。目标是在公开数据与 68M 参数规模下达到 SOTA 的重建质量与效率。

**方法详解**：表示是在 MHR 模板 UV 图上锚定的 3DGS：每个 UV 网格点放一个高斯，位置为重心的插值锚点加学习到的 canonical offset，共 264K 个（定制 UV 光栅化给部分身体更高分辨率）。对每个目标姿态额外预测 10 维 pose-dependent 残差（位移 3、尺度 3、四元数 4），先形变再动画；动画用扩展的 forward LBS，在 UV 锚点处重心插值每顶点变换，得到刚体旋转与位置。网络输入零初始化 UV map 与 V 张图，每张图经冻结 SAM3DBody（给姿态与 ViT 稠密特征）与可训练 ConvNeXt 提特征后相加。核心 FACRoPE 把 UV token 当 query、图像 token 当 key：图像 token 坐标取 (u,v,0)，UV token 坐标取「动画并渲染后的投影位置」FAC=[x, y, z-D]，其中 D 从候选化身在该视角的渲染深度图采样，用 RoPE 让 attention 只依赖相对坐标偏移，从而把 token 精确对准它该看的 patch，遮挡 token 的坐标则被推离像平面。ITR 让这套坐标在中间层就可用：CMLP 从每个中间 token 解一个高斯、PMLP 解形变，合成 posed token-GS 化身，动画渲染后把 FAC 回填给下一层，形成 rendering-in-the-loop。两个 MV-ARGBlock 把 UV token 克隆到 V 个姿态分支、加姿态嵌入，各分支做 FAC 引导的 3D RoPE 交叉注意力，再以 elementwise attention 融回主 token 流，过 self-attention 与 FFN。解码端把 token 重排回 UV 布局，CDec 上采样出 canonical 高斯，PDec 出每个驱动姿态的形变。训练用光度损失，另加 common shell transfer 正则：用 IRLS 估跨视角共享 shell，stop-gradient 强迫共享形变进 canonical offset、视角特有部分留在 pose offset，避免两者解耦失败。只在公开数据（DNARendering、2K2K、4D-Dress、Human4DiT、THuman2.1、HumanVid，6.8K 主体、64K 序列）上训 100K 步、batch 96、AdamW、lr 1e-4 cosine，四张 A6000 约 200 小时。

**实验与结果**：
- 分布外 NeuMan 6 视角：30.82 dB PSNR / 0.975 SSIM / 0.016 LPIPS，比 LHM++ 的 28.09/0.972/0.022 高 2.73 dB；2 视角 29.17 对 27.97；1 视角 27.02 反而低于 LHM++ 的 27.71。
- 6 视角下 Multiview Videos 28.83 对 25.68（+3.2 dB）、3D Scans 26.81 对 22.49（+4.3 dB）、HumanVid 25.86 对 22.50（+3.4 dB）；NeuMan input-pose 重建 33.30 对 28.50（+4.8 dB）。
- 视角扩展性：输入从 1 增到 6 视角，ARG-Avatar 提升 3.8 dB，LHM++ 只提升 0.4 dB。
- 效率：68M 可训练参数（LHM 的 6%、LHM++ 的 11%，约 9 倍更少），64K 公开序列（约 LHM 的 21%），约 125 H100 等效 GPU-hours（LHM++ 的 7%）；6 视角含 SAM3DBody 前向 2.3 s，比 LHM++ 的 14.2 s 快 6.2 倍。
- 2^3=8 组组合消融：FACRoPE 在每种配置都提升 PSNR（即使候选化身只是中性 mesh）；ITR 与 pose deformation 各自有效，两者同时开启时 FACRoPE 增益最大；第三层不再涨点，最终用两层。

**创新点**：把模板、LBS 与渲染给出的几何对应直接写进 attention，而不是让网络从数据里学 token 到 patch 的对应：FAC 用动画渲染后的投影坐标做 RoPE，遮挡关系由深度差自然编码。ITR 把这个坐标从一次性先验变成层内可迭代的 rendering-in-the-loop，中间 token 解出的粗糙化身反过来修正下一层的注意力。用 68M 参数在多个数据集上超过 609M 的 LHM++，给出「几何先验换 scaling」的一条实证路线。

**深读要点**：核心洞见是「模板、LBS 与渲染已经给出了几何对应，不该让 attention 从数据里重新学」：FAC 用动画渲染后的投影坐标做 RoPE，ITR 把坐标变成层内可迭代的 rendering-in-the-loop。68M 参数在 6 视角 NeuMan 上超 609M 的 LHM++ 2.73 dB，但单视角（27.02 vs 27.71）仍弱——它没有训练 inpaint 不可见区域。

**局限与风险**：单视角明显弱于 LHM++（27.02 对 27.71 dB），作者明确说模型没有训练 inpaint 不可见区域，V=1 的落后是预期的，实际使用需要多视角或视频。依赖 SAM3DBody 的姿态与 MHR 模板：2K2K 例子中头部区域因跟踪错位出现重影，说明位姿误差会直接进入渲染。模板锚定表示本身有上限（作者在引言中承认增加容量无法突破 template-anchored avatar 的表示约束），宽松衣物与长发只能靠 10 维 pose residual 近似。全文没有代码或项目页，训练需约 200 小时四张 A6000。

**与文献库的关系**：库内化身重建以 feedforward 大模型为主（LHM 系），本篇给出「几何先验换 scaling」的对照证据，属新增技术路线。

**可复现性**：正文未提供代码；全文 99,021 字符（L0/FULL）。

**行动建议**：纳入重点精读；无公开代码，需按正文细节复现。

### 7. Kolibri：颜色找位置、精化定姿态——彩色点云中的 RGB-D 定位（2611.22829）

**赛道**：重建与SLAM　**总分**：3.85（A）　**证据**：FULL/L0　**7 维**：IMP 4 · NOV 4 · TEC 4 · EXP 4 · PER 4 · TRL 3 · REP 3

**一句话结论**：把 RGB-D 重定位拆成 place-finding 与 pose-refinement，55.7K 参数在 ScanNet-96 达 81.4%，82 ms/帧，比 BUFFER-X 快约 18 倍。

**要解决的问题**：机器人在已扫描建筑内需要把相机定位到训练时从未见过的房间，参考数据是预先已知的彩色度量点云。点云配准方法（GeDi、BUFFER-X 等）能把每帧 RGB-D 对齐到点云，但代价极高：单房间内 BUFFER-X 中位 1.4 s/帧、GeDi 24 s/帧，整栋搜索要按房间或立方体重跑一遍。用图像检索先选房间虽能缩小搜索，但选错房间在姿态估计开始前就丢帧——100 个 ScanNet 房间中检索仅 28.6% 把真房间排第一。因此需要一种既保持配准精度、又能支撑无房间标签全库搜索的低成本定位方案。

**方法详解**：核心思路是把 RGB-D 重定位拆成“找位置（学习）”与“定姿态（几何）”两段，并先用实验证明拆分的可行性：在真实 ScanNet 帧上测得 refinement basin 边界为初始位置误差 7.7 cm（成功率降到一半），basin 内 99% 的帧成败与初值无关，因此学习模块只需把候选送进 basin。具体做法是把 frame 深度反投影点与参考点云都池化为 10 cm 立方 cell，每 cell 存点均值位置与颜色，以 k=16 近邻建图，法向取邻居偏移协方差最小特征值方向。逐 cell 输入 8 维特征（中灰居中颜色、log 边长均值与方差、linearity/planarity/scattering），边特征为 log 长度与“偏移-法向”“法向-法向”的绝对余弦，用绝对值消除法向朝向敏感。一层 message passing（EdgeConv 式逐特征 max 聚合，width 128，GELU + LayerNorm）输出 32 维单位描述符，全网络仅 55,712 参数；点云描述符离线算一次并可复用。匹配阶段每个 frame cell 取 top-5 相似点云 cell，τ=0.1 的 softmax 作权重；用 SC²-PCR 的距离一致性（ρ=25 cm）为 256 个 match 各种子 consensus set，加权刚体拟合得候选；为对抗重复家具造成的错误一致群，保留 4 个互相间隔 ≥0.5 m 或 10° 的候选、剔除被已选位姿解释（残差 <0.5 m）的 match 后再做 2 轮补充，最多 6 个候选。每个候选跑 point-to-plane ICP（1000 个均匀采样点、10 iter、对应半径 20→5 cm），以 3 cm 内点数作 fit score 选最终位姿。可选 Precise 用 Tukey 加权二级精化（+35 ms/+4.0 点），color pass 对通道做共享仿射把亮度均值与方差对齐点云后重跑全流程，按 fit score 择优。训练用 170 个房间（165 ScanNet + 5 校园空间）的渲染视角，加随距离平方增长的深度噪声、尺度/亮度/对比/白平衡扰动与缺失扇区，正样本为 0.5 m 内最近点云 cell，softmax 交叉熵，AdamW lr=1e-3、18,600 步 ×8 视图，RTX 4090 上 ≤53 分钟。

**实验与结果**：
- ScanNet-96（96 房间 / 7,986 帧，房间已知，5 cm & 5°）：Fast 81.4%±1.8 vs GeDi 80.3%±1.9（统计等价），BUFFER-X 69.4%、RGB GeoTransformer 77.8%、ColorPCR 80.3%、PREDATOR 49.6%、FPFH+TEASER++ 33.2%。
- 效率（RTX 2080 Ti，200 帧中位数）：82 ms/帧、1.44 GB，BUFFER-X 1,416 ms（约 18 倍）、GeDi 24,149 ms、RGB GeoTransformer 2,501 ms。
- 无房间标签搜索：100 房间合成点云（15.0 M 点）达 79.9%，仅比给定真值房间低 1.3 点；单候选时降到 46.2%；Retrieve-1+Fast 仅 23.9%（相对全库搜索 -56.0 点）。
- 医院急诊科真实手持激光扫描（49 m × 42 m，440 帧渲染）：86.5%±0.7 @ 5 cm & 5°，384 ms/帧；GeDi 整云 26.7%、1,090 个 3 m cube 76.7% 但需 91 分钟/帧（Fast 与 GeDi-cube 差异统计上不确定，+7.8 点 [-7.8,+23.4]）。
- 消融（ScanNet-10 消融房间 + 7-Scenes，Precise）：去 message passing 降 13.4/13.4 点，去颜色降 26.2/26.2 点，只留颜色降 3.4/3.4 点；参数量从 4,736 到 915,584 变化时 recall 波动 ≤1.0 点；22 房间训练与 170 房间等价。
- 失效边界：灰度帧上 RGB GeoTransformer 领先 47.2 点（0.25 m & 2°）；Bonn 跨相机（ASUS Xtion 帧 vs 地面激光扫描着色）Fast 仅 26.3%，加 color pass 47.2%，而 GeDi-cube 91.5%（11 分钟/帧）。

**创新点**：把 RGB-D 重定位显式分解为 place-finding 与 pose-refinement，并用 basin 宽度实测把“学习部分可以极小”从直觉变成可检验命题：55.7K 参数即可在匹配精化下追平 3.11M 参数的 GeDi。配套的“多候选 + 几何 fit score + 全库联合搜索”避免了两阶段检索的错误传播，使百房间/整栋无标签搜索在百毫秒级可行。相对既有工作，这是问题形式化与系统设计的双重创新，而非单纯换描述符。

**深读要点**：把重定位拆成 place-finding（颜色足够）与 pose-refinement（几何精化）后，学习模块只需 55.7K 参数：82 ms/帧、1.44 GB，精度与 24 s/帧的 GeDi 统计等价。最实用的细节是「多候选 + 全库联合搜索」，避免了检索错房间就直接丢帧（Retrieve-1+Fast 会掉 56 点）。强依赖颜色一致，灰度输入下失效。

**局限与风险**：强依赖 frame 与点云颜色一致（仅容忍亮度/对比度的仿射变化），灰度输入或跨相机色响应差异下明显失效，此时点云配准方法仍领先。refinement basin 仅 7.7 cm，最优候选落在 basin 外时需靠其他候选挽救（51% 的帧），再差就整帧失败。只在房间尺度室内场景验证，作者指出扩展到整栋需要“不丢弃正确位置”的层级化搜索结构。正文未报告训练/推理代码或数据发布。

**与文献库的关系**：库内重定位/配准以点云配准方法为主（GeDi/BUFFER-X 系），本篇把代价压到 82 ms，属显著改进。

**可复现性**：正文未提供代码；全文 79,796 字符（L0/FULL）。

**行动建议**：纳入重点精读；无公开代码，需按正文细节复现。

### 8. HandUMI：用于无机器人双臂数据采集的模块化手戴平行夹爪接口（2611.22146）

**赛道**：交互与输入　**总分**：3.72（A）　**证据**：FULL/L0　**7 维**：IMP 4 · NOV 3 · TEC 4 · EXP 3 · PER 4 · TRL 4 · REP 5

**一句话结论**：手戴平行夹爪 + Quest/PICO 追踪的无机器人双臂采集，562 条演示训练 ACT 折毛巾成功 12/20，硬件软件 Apache-2.0 开源。

**要解决的问题**：用 leader arm、replica 或 VR 控制器做遥操作时，每采一条演示都要占用机器人，采集吞吐受硬件数量限制。UMI 类无机器人接口解耦了采集与臂的运动学，但接触几何或开合运动不匹配会阻碍向真机迁移。最接近的 YUBI 同样用 Quest 控制器加编码器测开合且开源，但它要把机器人换成自己的夹爪、记录的是夹爪角度并建模转动指，指尖也仅一种设计，采集端与部署端的夹爪形态因此不完全一致。

**方法详解**：HandUMI 是手戴式平行夹爪接口：公共 wearable 主体上可换指尖、控制器类型与相机，printed finger cradles 通过曲柄驱动平行 jaws 平移，Feetech STS3215 12-bit 编码器经两点标定测 jaw 宽度，IMX335 鱼眼以 1280×960@30 fps 记录，可选 ZED Mini 提供工作区视角；指尖可匹配 AgileX PiPER、ARX X5、TRLC-DK1 的 Dream Gripper、Trossen WidowX AI 与 UMI 软指，机器人保留自己已装的夹爪。位姿不用腕部相机 SLAM，而由可替换 provider 提供带时间戳的 6-DoF 控制器位姿：Quest 3/3S 走新写的 TCP app（实现 YUBI Apache-2.0 软件的协议），PICO 4 Ultra 走 XRoboToolkit，ChArUco 板定义桌面坐标系。同步以工作站单调时钟给所有源打戳，每行目标落后实时 40 ms，取最近的相机（30 fps）与编码器（100 Hz）样本并带 freshness 标志（60 ms 偏斜上限），传感器丢失超过 1 s 即丢弃该 episode；标定分四级门控（夹爪行程、内参 ≤0.8 px 平均重投影误差、相机安装与桌面坐标系 ≤8 mm RMS、每个指尖的 TCP pivot 拟合 <5 mm RMS 且最大残差 <10 mm），另有引导式触碰协议用每位置 20 个样本交叉检查两指尖。数据以 LeRobot v3 记录两条控制器位姿与 jaw 宽度，与具体机器人无关；重定向时 profile 提供运动学、限位、TCP 与线性夹爪映射（0–66 mm 映射到 PiPER stroke，速度与力不匹配），由 PyRoki IK 生成七个双臂平台（PiPER、OpenArm v1、TRLC-DK1、I2RT YAM、MakerMods Metal Arm、Galaxea R1 Lite、ARX X5）的关节数据，并做 IK 误差、自碰撞、基座关节摆动的逐机器人筛选，PiPER 与 OpenArm 在 MuJoCo 中共享映射、IK 与平滑。

**实验与结果**：
- 跨本体重定向：七个模拟双臂的中位位置误差 0.03–1.17 mm（PiPER 1.17、OpenArm 0.14、TRLC-DK1 0.18、YAM 0.19、Metal 0.09、R1 Lite 0.03、ARX X5 0.09），episode 拒绝率 ≤4.7%（OpenArm），关节限位帧 OpenArm 27.5%、自碰撞 R1 Lite 16.4%。
- 采集质量：641 条录制中 79 条（12%）因 PiPER 重定向使基座关节摆过 60° 被剔除，保留 562 条（201,397 帧、111.9 分钟）；采样网格中位偏斜约 8 ms，PICO 追踪在主机时钟上领先 ≈40 ms 但双腕在 100.00% 的行上均被追踪。
- 标定精度：TCP pivot 拟合 RMS 4.0 / 3.4 mm、最大残差 7.013 / 7.021 mm（左/右）；桌面坐标系 RMS 1.6–4.2 mm 与 0.3–0.7°，两次重装 TCP 高度差 6–7 mm。
- 真机策略（PiPER 双臂折毛巾，各 20 次无辅助尝试）：仅用 562 条无机器人演示训练的 ACT 成功 12/20（Wilson 95% CI 39–78%），微调 π0.5 成功 7/20（18–57%），两者无统计差异（Fisher exact p=0.20）。
- 对照：只用前 101 条 episode 训练的 ACT 与未微调的 base π0.5 各为 0/20（0–16% CI）。
- 成本：一对零件 USD 207.11，含共享 Quest 3S 共 USD 557（不含可选 ZED Mini、主机、税与运费）。

**创新点**：相对 UMI（无编码器、需换装专用夹爪）与 YUBI（记录 jaw 角度、建模转动指、单一指尖设计），HandUMI 用平移平行 jaws + 编码器测开合、指尖复制机器人已装夹爪、且机器人保留原夹爪，使采集端与部署端的接触几何更一致。工程上把“机器人无关录制 + 标定溯源 + IK 筛选”做成可向七个双臂平台重定向的流水线，并用真实 PiPER 双臂折毛巾给出端到端证据，而不只是仿真重定向误差。整套硬件与软件以 Apache-2.0 开源并给出 BOM 成本，把无机器人双臂采集的进入门槛压到数百美元级。

**深读要点**：用 Quest/PICO 控制器追踪 + 编码器测开合 + 可换「机器人同款指尖」，把采集端与部署端的接触几何对齐；562 条无机器人演示训练 ACT 折毛巾 12/20，而基线 0/20。工程完整度是亮点（四级标定、7 臂 IK 重定向、Apache-2.0 开源），但真机只一个任务、单 seed，跨本体证据仅为仿真。

**局限与风险**：作者自陈跨本体证据只是仿真 IK，真机测试只有一个 PiPER 任务、一套 setup、一个 seed，且没有失败分析；holdout 划分可能与被测 session 重叠。采集受头显约束、仅支持平行夹爪，换新夹爪必须重做匹配指尖，接触几何仍然依赖本体。tip-matching 带来的收益、jaw 精度、指尖负载与音频价值均未测量。正文还记录了一次相机重标定故障：40 条 episode 事后施加 +1.9 cm 高度修正、其中 31 条留在队列里，而拟合残差与离线检查无法独立验证真实桌面高度，门控为何漏检原因未查明。

**与文献库的关系**：库内数据采集线有 UMI/YUBI 系，本篇在接触几何一致性与开源完整度上改进，属增量式改进。

**可复现性**：代码/项目页 https://murobotics.ai/research/handumi（数据与 checkpoint：https://huggingface.co/murobotics）；全文 24,949 字符（L0/FULL）。

**行动建议**：纳入重点精读，先跑通公开代码再评估迁移成本。

### 9. SpatialMind：面向多模态大模型空间推理的自适应多层级几何融合（2611.22415）

**赛道**：感知与认知　**总分**：3.65（A）　**证据**：FULL/L0　**7 维**：IMP 4 · NOV 3 · TEC 4 · EXP 4 · PER 3 · TRL 4 · REP 4

**一句话结论**：任务条件化的多层级几何门控注入 MLLM，VSI-Bench 5B 71.5 / 10B 72.3，均居同规模第一。

**要解决的问题**：MLLM 在 2D 视觉语义上表现良好，但对 3D 空间结构（距离、朝向、场景布局）的推理仍受限。已有把 3D 重建模型接入 MLLM 的工作，要么全任务只用单一几何粒度，要么采用固定不变的多层融合方案。作者通过在 VSI-Bench 上逐层移除几何注入发现：低级感知任务更依赖 shallow 特征，高级推理任务更依赖 deep 特征，因此固定融合无法匹配任务所需的几何粒度。

**方法详解**：骨干为 Qwen3.5-4B，几何侧使用完全冻结的 VGGT-1B，取 VGGT 第 11/17/23 层 patch token 作为 shallow/intermediate/deep 三级几何表示，经 layer-specific geometric merger（stride 2）对齐到 LLM 的 token 数与隐层维度。GeoFus 在每个注入位 s∈{0,1,2} 上为每个几何层配置独立的 position- and layer-specific projector P_{s,l}（LayerNorm + 两层 MLP），从而解耦不同注入深度的投影参数。门控条件由文本、视觉语义、几何三路构成：c_t 用 MaskedAvgPool 只聚合 query token 并排除 padding 与答案 token，c_v,s 对注入位视觉隐状态做 AvgPool，c_g,s 对三级几何描述子做 layer norm 后取均值。三者按可学习缩放因子 alpha_v,s、alpha_g,s 相加，经线性层得到 logits，再用温度控制的 softmax 归一化为融合权重 w_{s,l}。融合表示为投影特征的凸组合 G_s=sum_l w_{s,l} Z_{s,l}，并以残差方式注入视觉 token：V'_s = V_s + G_s。为缓解门控塌缩（权重全压到单层），引入负熵正则 L_gate = -lambda * (1/S) * sum_s H(w_s)，lambda=0.005。训练分两阶段：Stage 1 沿用 SpatialStack 的固定层映射，联合训练 LLM 与几何投影器 1 个 epoch（lr 1e-5）；Stage 2 冻结 LLM 与 LM head，只训练投影器、门控参数与缩放因子（lr 5e-5），目标为 L_LM + L_gate，8x A800 上 5B 约 30h + 15h。

**实验与结果**：
- VSI-Bench 上 SpatialMind-5B 得 71.5，居 3-5B 组第一；同训练数据的 SpatialStack-5B 为 69.6。
- SpatialMind-10B 得 72.3，居 8-10B 组第一，高于同数据 SpatialStack-10B 的 71.3 与 GeoThinker-9B 的 71.9。
- 六个空间基准（SparBench/VSI-Bench/SPBench/BLINK/MindCube/SQA3D）平均：5B 70.7（比同数据 SpatialStack-5B 高 2.1），六项中五项第一；10B 71.6，四项第一。
- 组件消融（VSI-Bench，三次独立运行均值）：固定基线 69.6 -> 文本门控 70.1 -> 加语义与空间条件 70.2 -> 允许跨层选择 70.9 -> 加负熵正则 71.5，累计 +1.9。
- 多层级几何消融：移除 shallow 注入使低级任务降 1.43 点（高级仅 0.17）；移除 deep 注入使高级任务降 2.07 点（低级 0.66）；移除 intermediate 分别降 1.33 与 1.58。
- 门控可视化：高层推理任务在 L2 注入位给 deep 特征 46.8% 权重，低层感知任务为 39.3%；低层任务在 L0 给 shallow 35.0%，高层为 28.8%。

**创新点**：把「不同认知层级的空间任务需要不同几何粒度」从观察提升为设计原则，并用任务条件化的门控在多个 LLM 注入层上做凸组合选择，而非固定层映射或固定层级拼接。负熵正则针对门控塌缩这一自适应融合的固有失效模式，属于有针对性的机制补丁。整体是在 SpatialStack 式多层注入框架上的架构性改造，而非全新范式。

**深读要点**：在 VSI-Bench 上逐层移除几何注入后发现「低级感知靠 shallow、高级推理靠 deep」，于是用任务条件化门控做多层级凸组合，并用负熵正则防门控塌缩。提升幅度不大（69.6→71.5、71.3→72.3），但方向明确；短板在单视图绝对距离与方向估计（SPBench-SI 60.95 vs 63.50）。

**局限与风险**：BLINK 上 5B 与 10B 均只排第二，作者归因于该基准含艺术风格、取证、拼图等 2D 视觉逻辑任务，显式几何线索帮助有限；训练语料偏空间推理也是原因之一。SPBench 上 10B 落后同数据 SpatialStack-10B 0.59 分（68.34 vs 68.93），差距集中在 SPBench-SI 的单视图绝对距离与方向估计（60.95 vs 63.50），说明细粒度单视图度量几何仍是短板。方法依赖冻结的 VGGT-1B 与 8xA800 两阶段训练，成本不低。

**与文献库的关系**：库内 MLLM 空间推理工作（SpatialStack 系）为固定层级融合，本篇改为任务条件化门控，属改进。

**可复现性**：代码/项目页 https://github.com/zhaosb-star/SpatialMind；全文 90,714 字符（L0/FULL）。

**行动建议**：纳入重点精读，先跑通公开代码再评估迁移成本。

### 10. SpatialCast：通过投射阴影读取三维世界（2611.22657）

**赛道**：感知与认知　**总分**：3.65（A）　**证据**：FULL/L0　**7 维**：IMP 3 · NOV 4 · TEC 4 · EXP 4 · PER 4 · TRL 3 · REP 3

**一句话结论**：以投射阴影为物理读数构建 T1/T2/T3 三向推理基准，GRPO 使 Qwen3-VL-8B 从 24.40% 升到 38.73%。

**要解决的问题**：现有空间基准主要评估相对位置、距离、朝向、空间记忆与视角推理，较少系统考察「物理场景条件如何决定其 2D 观测」，也少评估模型能否从变化前后的观测反推是哪个物理因素、变了多少。投射阴影同时受物体几何、位姿、光照与视点约束，是可观测的物理证据，但此前未被用作空间推理的系统性评测载体。

**方法详解**：把场景状态定义为 z=(G,P,L,C)（几何、位姿、光照、相机），渲染器 R 产生物体-阴影观测 I=R(z)，干预 a 通过状态变换 T_a 得到 z'=T_a(z)。用 BlenderProc 加 Blender Cycles 构建可控场景，几何池含 6 个基元、4 个组合、6 个程序化共 16 个形状族，场景结构分单物体、双物体阴影分离、双物体阴影重叠三档。设计三个互补任务：T1 Projection Compatibility（forward 选与几何加光照一致的投影；inverse 选与观测阴影一致的光照方位角或高度）、T2 Projection Propagation（给定初始图与干预，从四候选中选结果图；单因子 L/R/C 与双因子 LR/LC/RC）、T3 Projection Attribution（给定前后观测与已变化因子，推断变化参数的方向与幅度）。每题四选一，场景元数据确定正确项，模型只看到图像、prompt 与选项；干扰项通过省略某因子、反转转向或改变幅度构造。质量控制会剔除物体或阴影出画、阴影侵入画面边缘的场景，并渲染四个物理假设逐一比对，97.87% 的题目即使最近候选对也有 >=150 像素差异。规模 21,000 题（T1 8,400、T2 8,400、T3 4,200），划分 15,000 训练 / 1,500 验证 / 3,000 scene-test / 1,500 geometry-test，两个测试集共 4,500 题。另从 ReNe（ReLight My NeRF）标定光照照片构建 SpatialCast-Real：20 个场景、200 题（125 T2 + 75 T3）、587 张图。后训练用 GRPO，筛选后保留 11,186 题，四个基座共用同一数据顺序训练 1,399 次更新，每题采样 8 条回答，奖励含正确性、格式合规与长度惩罚。

**实验与结果**：
- 合成测试集 4,500 题上，GPT-6.1 Sol 总体 79.42%（T1 67.50 / T2 88.39 / T3 85.33），Gemini 4 Argon 57.71%；四个开源基座与 Spatial-SSRL、SpatialBlock、Spatial-MLLM、SpatialLadder 等空间训练基线总体仅 24.38%-25.91%，接近 25% 随机水平。
- SpatialCast-GRPO 使 Qwen3-VL-8B 从 24.40% 升到 38.73%（+14.33 点），其中 T2 由 25.44% 升到 48.78%（+23.33 点）。
- 其余基座同样提升：4B 24.91->32.87、Qwen2.5-VL-3B 24.38->31.84、InternVL3-2B 25.78->34.58；四个基座在全部 T2 子类型上均有提升，而 T1 阴影长度与 T3 物体旋转归因提升有限或不一致。
- 8B 模型在 scene-test 上 +13.37 点、geometry-test 上 +16.27 点，但在 SpatialCast-Real 上仅 +2.00 点。
- 外部迁移（MindCube / MMSI / SPBench-SI / SPBench-MV / MMMU 五项均值）：8B 37.51->39.12，4B 36.10->40.34，3B 36.87->37.69，2B 反而 37.36->35.22；SPBench-MV 上 4B +8.19，2B -13.11。
- 阴影证据消融（240 道 T2-L 题）：GPT-6.1 Sol 完整输入 81.3%、仅阴影 81.7%，抹去阴影后跌到 25.0%；GRPO 的 4B/3B/2B 分别由 42.9/35.0/52.1 跌到 30.0/25.4/23.3。人类 5 人在 32 题试点上平均 65.00%（随机 26.56%）。

**创新点**：把投射阴影当作「物理读数」来探测 MLLM 是否理解场景条件与观测之间的因果关系，而不是当作待识别的视觉纹理。用同一个投影模型串起正向匹配（T1）、干预后预测（T2）、逆向归因（T3）三个推理方向，使「会不会预测」与「会不会反推」可分别测量。合成侧对场景参数做程序化控制并设置 scene-test / geometry-test 双测试分区，可区分新场景泛化与 held-out 几何参数泛化。

**深读要点**：用投射阴影做「物理读数」，把正向匹配（T1）、干预后预测（T2）、逆向归因（T3）分开测——这是把「会不会预测」与「会不会反推」解耦的漂亮设计。GRPO 把 8B 从 24.40% 拉到 38.73%，但合成场景被简化为单平面接收面，真实图上增益仅 +2.00 点，T1 的阴影长度判断仍是全模型弱项。

**局限与风险**：合成场景被简化为一个平面阴影接收面加一至两个物体，与真实场景的遮挡、互反射、多光源差距明显，作者也承认 real 图上的增益远小于合成（8B 仅 +2.00 点）。T1 的阴影长度与光照高度判断是全模型共同弱项（Sol 分别 41.47% 与 39.00%），说明长度/高度这类度量线索未被真正掌握。外部迁移不稳定：2B 五项均值下降 2.14 点、SPBench-MV 掉 13.11 点。人类可答性仅由 5 人 32 题试点支撑，且只有 GPT-6.1 Sol 与 Gemini 4 Argon 跑完完整合成集。

**与文献库的关系**：库内空间基准多测静态关系，本篇以阴影为物理证据补上因果推理维度，属新增。

**可复现性**：正文未提供代码；全文 68,485 字符（L0/FULL）。

**行动建议**：纳入重点精读；无公开代码，需按正文细节复现。

## 四、当日全量 7 维度对比表

完整表见 `papers/daily/2026-11-19/7dim-table.md`（21 篇全量，含 C 级）。摘要如下：

| arXiv | 标题 | 赛道 | 总分 | 等级 | 证据 |
|---|---|---|---:|---|---|
| 2611.22095 | CueSplat：学习调度稀疏形变以实现边缘设备上的动态高斯泼溅 | 神经渲染 | 4.30 | A | FULL |
| 2611.22164 | HandRSI：手部姿态估计的递归自我改进 | 化身与人体 | 4.30 | A | FULL |
| 2611.22235 | CoSphere-SLAM：带球面回环的多智能体全景高斯泼溅 SLAM | 重建与SLAM | 4.15 | A | FULL |
| 2611.22240 | Cross3DGS：从工作站到移动设备的统一 Vulkan 3D 高斯泼溅训练 | 系统与平台 | 4.15 | A | FULL |
| 2611.22541 | 从感知到模拟：揭示并增强多模态大模型中的心理空间动力学 | 感知与认知 | 3.92 | A | FULL |
| 2611.22207 | ARG-Avatar：以动画-渲染引导实现高效前馈化身重建 | 化身与人体 | 3.85 | A | FULL |
| 2611.22829 | Kolibri：颜色找位置、精化定姿态——彩色点云中的 RGB-D 定位 | 重建与SLAM | 3.85 | A | FULL |
| 2611.22146 | HandUMI：用于无机器人双臂数据采集的模块化手戴平行夹爪接口 | 交互与输入 | 3.72 | A | FULL |
| 2611.22415 | SpatialMind：面向多模态大模型空间推理的自适应多层级几何融合 | 感知与认知 | 3.65 | A | FULL |
| 2611.22657 | SpatialCast：通过投射阴影读取三维世界 | 感知与认知 | 3.65 | A | FULL |
| 2611.23051 | Refin3R：面向前馈三维重建的几何引导精化 | 重建与SLAM | 3.65 | A | FULL |
| 2611.23187 | Any2Building：以共享空间查询统一点云与图像的建筑物重建 | 重建与SLAM | 3.65 | A | FULL |
| 2611.22805 | DOOM-GS：面向海量高斯泼溅的动态外存优化 | 神经渲染 | 3.43 | B | FULL |
| 2611.23054 | ReTouchGS：面向 3D 高斯泼溅的超轻量免渲染美学调色与迁移 | 神经渲染 | 3.43 | B | FULL |
| 2611.21690 | EgoLink：第一人称语言-视觉交互网络知识挑战赛总结 | 评估与数据集 | 3.35 | B | FULL |
| 2611.21938 | HubEgo-100K：面向机器人学习的野外第一人称技能工作视频数据集 | 评估与数据集 | 3.35 | B | FULL |
| 2611.22742 | GaussianMamba：三维高斯基元的几何与关系感知状态空间扫描 | 感知与认知 | 3.30 | B | FULL |
| 2611.21802 | 数据驱动的三维表示变长压缩 | 系统与平台 | 3.20 | B | FULL |
| 2611.22614 | 面向触觉图形识别的低成本振动触觉表面：盲人与明眼用户的探索策略 | 触觉与多模态 | 3.00 | B | FULL |
| 2611.22151 | EgoHandWAM：探究手部运动在第一人称世界-动作建模中的作用 | 化身与人体 | 2.92 | C | FULL |
| 2611.21642 | RelicTouch：探索用于图像解读的指尖振动触觉反馈 | 触觉与多模态 | 2.85 | C | FULL |

## 五、覆盖率校验与筛选过程说明

### 5.1 漏网对账（先于拉取）

- `scripts/audit_listing_1119.py` 以 show=500 单页复采 7 分类，目标日组 declared≠got 时自动补采后续页（continued/last 兼容）。
- 7 分类最新公告日均为 **2026-11-18**，无 11-19 日组；11-17 组复采逐分类 declared=got（1,016 槽位 / 844 唯一），未入馆 **811 篇 = 844 − 33（上批主批已入馆）**。
- 用 11-18 的 RSS 全量逐篇核摘要：811 篇中 XR 命中 **69 篇**，与上批 `data/rejected_1118.json` 的 69 篇**逐篇一致** → **0 漏网、无滞后补录、无 backfill 触发**（本批 backfill 来自今日 RSS 的 replace 流，与补漏无关）。
- **采集完整性**：七分类 declared=got 全部成立，脚本 exit 0（非采集不全的 exit 2）。

### 5.2 门① 同质度

- 定稿 Top10 对库内 90 天非本批文献的最大 Jaccard 为 **0.261**（2611.22415 SpatialMind vs 2609.03892，2026-09-03），远低于 0.62 阈值；其余 9 篇 0.091–0.188。
- 结论：无同质重复，无需降权或剔除。

### 5.3 门② 赛道覆盖

- 定稿 Top10 覆盖 **6 赛道**：神经渲染×1、化身与人体×2、重建与SLAM×2、系统与平台×1、感知与认知×3、交互与输入×1（全批 8 赛道）。
- 结论：纯值排序即达标（≥5），**未触发重筛**；赛道分布以感知与认知（3 篇）最集中，但均属不同子问题（动态模拟 / 多层级融合 / 阴影因果），不构成冗余。

### 5.4 门③ 价值天花板（校准关）

- 当日最高 **4.30** vs 库内近 30 天 Top10 均分 **4.4230**（窗口 2026-10-20~11-19、436 条入窗、按 batch 剔除 2026-11-19 与 backfill-1119）。
- 结论：**非重磅日，无 S 级**（margin -0.1230，未进入 0.05 险过区）。按 skill §8.6.3，不因「接近」而拔高评分。
- 库内 Top10 构成（供对照）：arXiv:2611.06817 4.57、arXiv:2611.11169 4.57、arXiv:2603.01178 4.5、arXiv:2611.21143 4.43、arXiv:2610.39399 4.37、arXiv:2611.09458 4.37。

### 5.5 召回分层与剔除

- 摘要级 KW 命中 37 篇（保留 15）→ 标题级扩展词补扫 21 篇（保留 6）→ 候选 58 篇 → 剔 37 篇误命中 → **XR 21 篇**。
- 误命中主因：`SLAM`/`point cloud`/`monocular depth` 把自动驾驶与机器人操作带入（12 篇），`AR`/`MR` 缩写误命中自回归（2 篇），`spatial`/`tracking`/`depth` 泛词带入通用 2D 视觉（8 篇）。
- **C 级 2 篇仅入馆不解读**：2611.22151 EgoHandWAM 2.92（受控探针、以负结果为主）、2611.21642 RelicTouch 2.85（n=20 主观评分、无客观解读指标）。
- OUTDATED/SUPERSEDED：**0 篇**（无足够证据判定任何一篇被库内或本批取代）。

## 六、附录

### 6.1 证据等级与抓取

- 25 篇全部 **L0/FULL**（arXiv HTML 正文），无 L1/L2/L5 降级；字符数 17,275–130,366。
- **剔除说明**：2611.23209（gaze-guided VLM）虽 L0 抓取成功，但正文仅含摘要页 + 参考文献（无 Introduction/Method/Results），按诚实口径不纳入评分，记入证据不足清单。
- 抓取严格串行 3s/篇，无限流、无 429；manifest 合并写入校验通过。

### 6.2 数据与脚本

- 对账：`scripts/audit_listing_1119.py`；甄别：`scripts/triage_1119.py`；漏网复核：`scripts/filter_missed_1119.py`；三关：`scripts/gates_1119.py`；评分：`data/scored_1119.json`；产物：`scripts/write_deliverables_1119.py`、`scripts/write_notes_1119.py`、`scripts/write_reports_1119.py`。
- 对账数据：`data/audit_1119_days.json`、`data/newday_1119.json`、`data/missed_prev_1119.json`、`data/missed_new_1119.json`、`data/missed_xr_1119.json`（0 条）。

### 6.3 库况

- registry **990 → 1,015**（+21 主批 +4 backfill，按 base_id 幂等，备份 `registry.jsonl.bak-20261119`）；
- 原子笔记 632 → **655**（本批 23 篇，grade≥B）；daily 目录 67 → **69**；MOC 55 → **57**。

### 6.4 backfill-1119

4 篇旧稿 v2/v3 再公告，单独报告见 `reports/XR-Backfill-Report-backfill-1119.md`：SFMambaNet 3.85 A · Max-Clique vs Max-Consensus 3.84 A · SSA-3DGS 3.65 A · HolisticMotion 3.28 B。

