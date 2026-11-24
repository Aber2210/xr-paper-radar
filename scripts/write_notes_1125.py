# -*- coding: utf-8 -*-
"""2026-11-25 产物：原子笔记 / 当日 MOC / backfill MOC / registry 幂等追加。"""
import glob, json, os, re, shutil

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
os.chdir(ROOT)
DATE, MMDD = '2026-11-25', '1125'

D = json.load(open(f'data/scored_{MMDD}.json', encoding='utf-8'))
G = json.load(open(f'data/gates_{MMDD}.json', encoding='utf-8'))
MAN = json.load(open('data/fulltext/_manifest.json', encoding='utf-8'))
TOP10 = G['top10']

DIG = {}
for k in range(1, 7):
    for r in json.load(open(f'data/digest_{MMDD}_g{k}.json', encoding='utf-8')):
        DIG[r['id']] = r

CONCL = {
 # ---- Top10 ----
 '2611.31140': '把码率控制点从 Gaussian 属性前移到 Gaussian head 之前的 token 空间，并用零膨胀逆自回归熵编码：4×RTX 5090 上 32.2 FPS @ 50 Mbit/s，笔记本 3050 Ti 解码单帧 22.1 ms，Pro 档 208.2 kB/帧仅为未压缩 float32 的 1/22.8，是首个把「自由视点人体流式」三级 33 ms 预算全部跑满的端到端系统。',
 '2611.28649': '不新训空间 VLM，而是给模型一段可被注意力读写的场景 token 并冻结读出器解耦「感知」与「变换」：Qwen3.5-9B 四基准平均 74.03%（比最强微调基线高 6.76），跨视图点恢复率由基线最高 16.02% 提到 65.11%。',
 '2611.30597': '把 VDM 手部深度从外观回归改为测试相机射线上的几何约束求解（多关节对距离定尺度）：野外 MPJPE-abs-p 56.55→32.59 mm（−42%），域内 24.46→19.62 mm，检测失败帧占比比 ViDiHand 少 14.57×。',
 '2611.30461': '把「显示时钟」与「生成时钟」解耦，用光流 warp + 交叉淡化让 400 ms/帧的扩散模型支撑相机帧率：720p 25 FPS（RTX 4080），IndoFashion 留出 LPIPS 0.137→0.077，长裤失败率 33%→4.2%，并给出「哪些加速会破坏印花」的实测清单。',
 '2611.30802': '把稀疏主动重建的决策对象从「单个 next-best-view」改为「持久目标 + 变长路径前缀」，让走廊通行折算为远端房间价值：HSSD Cov10 74.1%→93.3%，HM3D 47.2%→95.6% 且 PSNR +11.7 dB，training-free 可在 Habitat 在线闭环。',
 '2611.29236': '把「新视角几何改进」重述为对冻结表示的选择性纠正：不重训、不需目标视角观测，只用跨视角误差互补性 + 期望绝对误差下降准则做准入，DTU AbsRel 0.0440→0.0180，动态骨干最高降 63.9%。',
 '2611.30572': '把触觉作为独立专家接入预训练视频 MoT 并用「触觉真实性 + 接触力合理性 + 视触时间对齐」联合验证器过滤 rollout：五个真实任务四种策略平均成功率 19.4%→33.8%，Bo3 30.8%→48.8%，去掉验证器即回落到与仅真实数据持平。',
 '2611.31156': '把光栅化的「只处理可见图元」迁移到无显式几何的 transformer 渲染器：router 在解码前预测目标视角会用到的 source token，24 源视图下比 LagerNVS 快 6.4× 而 PSNR 仅低 0.68 dB，固定预算下 82–87 FPS 与源视图数近乎脱钩。',
 '2611.28520': '视频 DiT 内部已编码深度与相机，只是形式不对——用片段级 shift 修正归一化逆深度、多层特征直接回归相机，把迭代去噪式重建压成单次前向：7-Scenes 精度误差 0.047→0.018（−61.7%），比 Aether 快 4×、比 Geo4D 快 14×，单帧 74–84 ms。',
 '2611.29163': '把「结构性缺失」当一等设定并给出可复现基准（按解剖规则在 3D 上删 MANO 段再渲染），方法上把拓扑先验拆成拓扑感知蒸馏与渐进运动学推理：IncNYU E_avg 8.00 vs 11.49，完整手 NYU MPJPE 7.07 不牺牲，并有 3 名真实截指者参与的用户研究。',
 # ---- 主批其余 ----
 '2611.28020': '把「减少音频维度」当设计变量而非降级，用非劣检验给出角度容差边界：方位主导任务可用 Azimuth-Only 替代 Full，横向精度要求细于 5°/10° 时 Two-Channel 不可替代；Apple Vision Pro + 18 人 × 120 trial 的 6-DoF 证据。',
 '2611.28027': '把「视频真值提取 + 窗口回归 + 逐关节指标 + 传感器重要性」封装成无代码桌面工具，让无 ML 背景的设计者用笔电加摄像头在分钟级完成一次布局验证（单周期 618.8 s），并以 10 人可用性研究验证。',
 '2611.28056': '把「甜点」从扬声器物理摆位改写为被试实际选择的位置与朝向（类比 MOS），并给出客观质量图与主观甜点图的相似度比对流程：25 名被试 × 12 场景，LQ 对 SNR 的 MAE 0.0142 vs 0.0223、SSIM 0.8651 vs 0.8115。',
 '2611.28085': '用「幅度管光照、相位锚结构」的频谱先验替代光流式时序约束，并把去噪步数与注意力复用交给用户感知容差驱动的运行时控制器：SDSD-indoor TSSIM 0.86（次优 0.81）、0.07 s/帧，已在 Pixel 7 / Jetson Orin / Xiaomi 17 Ultra / XREAL 上部署。',
 '2611.28090': '把融合表征的监督从单一联合目标改成「重建两个冻结单模态教师的稠密表征」，配合预训练期输入稀疏化：EvIs-Kitchen 在 K=4 稀疏视频输入下名词 F1 65.89→75.09（+9.20），增益集中在稀疏而非完整观测。',
 '2611.28111': '不引入新损失，而把「目标间梯度冲突」当几何诊断信号：冲突定位到位置参数后既做选择性更新调和，又直接驱动致密化与剪枝，Mip-NeRF 360 PSNR 28.12 对 3DGS 27.82 且高斯数更少（2.27M）。',
 '2611.28136': '把记忆写回从集合并改成带精度代理（掠射角 + 时序衰减）的递归加权融合、把读出从最前层改成带可靠性与深度的 K 层候选：RealEstate10K NVS +0.82 dB，闭环重访（第 152 帧）PSNR 15.978→20.455（+4.48 dB）。',
 '2611.28193': '把「无训练推理加速」建立在注意力与输出平滑性分析上，锚点插值与共享 token 解码分别作用于查询数量与单查询成本：全部任务平均约 5×（2.1–6.2×）加速而精度与 D4RT 相当，60 FPS 下可生成 6,653 条全视频轨迹（对 1,342 条）。',
 '2611.28636': '把「语义干扰处理」从按资产的后处理前移到共享预训练阶段（无 watermark 场景图造干扰 + 渐进课程），使同一冻结解码器覆盖多个语义相近高斯资产：16-bit 静态 PSNR 41.55→50.29 dB、32-bit Bit Acc 99.52%，无需 Guard4D 式资产级优化。',
 '2611.28665': '把「CoT 为何伤空间感知」从基准级平均效应推进到句子级因果：forced readout 定位 commit sentence，固定理据 + 双图交换证明写完理据后图像影响从最多 76.5 分塌缩到 2.0–8.9 分，覆盖 15 个开源（2B–38B）与 6 个闭源模型。',
 '2611.28666': '把「记忆粒度」本身当设计变量：以段为单位联合重建、跨段几何隔离，再用覆盖度检索 + 几何可见性解析压进固定条件预算，部分重访 PSNR +2.6 dB、完整回环 +3.9 dB，LPIPS 降 43.2%/46.3%。',
 '2611.28670': '把任意尺度深度重建从逐像素隐式解码换成「显式二维高斯场 + 可微渲染」，像素足迹进入核协方差并做积分保持的幅度校正：RGB-D-D ×16 RMSE 5.33 对 DuCos 5.76，且 ×20/×24 训练范围外仍领先。',
 '2611.28673': '把「三维理解」重写成「检索哪些二维证据足以回答」，推理时完全 3D-agnostic、免训练：ScanQA val CIDEr 94.8、SQA3D test EM 57.2，语义一致性 JC 24.15→39.25。',
 '2611.28682': '把接触校正从外部 guidance 搬进生成器速度场，用整流流闭式干净估计做表面测量、零额外 NFE 回写到 part token：InterAct FID 0.114 对 LIGHT 0.170，手部接触 F1 0.730→0.834。',
 '2611.28792': '在同一个自回归扩散模型里同时输出 RGB 与显式 3DGS，并在每个 chunk 内联合读取干净历史与噪声新视图、刷新全历史特征：DL3DV-200 四参考视图 PSNR 20.68（MVSplat 20.25），8 视图 LPIPS 0.117 为最低，但 8 视图 PSNR 落后 PixWorld。',
 '2611.28793': '把空间 KV 缓存做成按区域/按层自适应分辨率的八叉树（用注意力响应而非几何距离决定合并），并把历史证据复用做成只重算短后缀：四个流式骨干峰值显存降 14.0%–26.8%，位姿任务 ATE 在 12 个设置中 11 个低于 STAC。',
 '2611.28802': '指出「扰动的方向」才是平坦性起作用的原因：用跨视角梯度分解分离一致/分歧方向、只在分歧方向求平坦并剔除与重建梯度冲突的分量，作为插件在 LLFF 3 视图把 3DGS 19.74→20.84 dB，可套到 7 种监督/表示。',
 '2611.28878': '把外观记忆从白盒几何代理解绑：高斯允许离开代理表面但仍用代理深度做度量锚定，记忆的写（置信门控增量融合）与读（克隆后全局精修、用完即弃）分离：自建 Expedition-33 上 ROI-LPIPS 0.2731→0.1220，整帧 PSNR 15.75→24.35 dB。',
 '2611.28913': '把稀疏 SDF 的离散 token 与可逆、offset 条件化的三维 BPE 结合，在序列化前按面邻接图合并不再依赖 1D 邻近：LLM 完整序列平均长度 6,873→3,753 token（−45.4%），Objaverse captioning METEOR 21.50 对 LEO 20.91。',
 '2611.28939': '把主动脉冲热激励与单面 TPS 解析模型做成可贴附夹爪的薄膜器件（加热与测温分置两层），分类侧融合可解释热描述子与多尺度时序 CNN：12 种材质平均准确率 92.69±3.59%（3 s 脉冲 + 10 s 观测窗），有夹爪在线测量真机证据。',
 '2611.28979': '不重训单目先验，而把「对齐」与「区域选择性融合」显式拆开：support-weighted 三角化建立共享度量参考，再按解剖区域（掌 + 五指）做候选配对：DexYCB-MV MPVPE 5.997→4.193（−30.1%），HanCo −29.1%。',
 '2611.29026': '把「刷新」放在解码器输入端而非参数端：累积 canonical UV 观测的加权 running sum 再用单图训练的解码器重解码，刷新无需多图训练也不存图：163 个 clip 刷新后 +0.49 dB，≥135° 帧上 +0.68 dB，RTX 3080 Laptop 创建 1.08 s、48.1 ms/帧。',
 '2611.29059': '不改点云骨干、不做特征重采样，而把跨 chunk 场景记忆压进 LaCT fast weights 并让离线双向与在线因果两套推理共享同一残差模块：FOR-instanceV2 mIoU 87.9（PTv3 86.5），ScanNet 全场景峰值显存 19 GB→0.3 GB。',
 '2611.29112': '把语言带宽受限的去中心化多视图推理从「两 agent 单房间」推广到 N agent、六类异构场景与显式词预算：10,007 条 QA、双认证后训练池 5,541 题，集中式→去中心化落差随骨干剧烈变化（Qwen3-VL-8B 38.7→28.7）。',
 '2611.29168': '不在权重上做文章，而把「模型路由」落到题型粒度并用经验贝叶斯闭式估计权重：VSI-Bench 全 5,130 题 64.07%（最佳 ≤4B 已发表 60.9%），面向 T4/fp16 的 3B+4B 端侧组合。',
 '2611.29218': '把 Brownian bridge 扩散用于人体运动并解决其与多帧序列的不兼容（不做全局端点桥，而做每帧与其时间邻居的局部桥）：端点 MPJPE 0.421→0.327，跨数据集零样本 Nymeria 端点 0.481→0.369，代码已开源。',
 '2611.29240': '把触觉基础模型的「数据金字塔」（遥操作/手持 UMI/仿真）与力–位混合执行接口打通成一套可复现栈，并用同一任务集做仿真–真机配对评测：八个策略变体成功率排序一致性 Pearson r=0.998，仅用仿真微调零样本上真机 99.0%。',
 '2611.29293': '把「运动」从特征层搬到位置编码层：按内容速度把 key 平移到 query 时刻再编码，既不改表示也不做特征 warping：RayRoPE 上 PSNR_dyn +0.9–1.3 dB、URoPE 上 +0.4–0.8 dB，三个数据集全部指标提升。',
 '2611.29376': '把风险等级编码进「场景匹配的材质语义」（软植被/硬木石/火焰荆棘）配合对比度与亮度，而非叠加抽象警示符号：42 名被试三条件对照，线索清晰度 C2 全面优于 C1 与 Baseline，安全感 4.93 vs C1 3.21（d=1.36），并有 Quest 3 实时系统。',
 '2611.29389': '为 DiT 补上三处结构性缺口（token 流 + stream mask 处理置换不变目标、射线位置编码替代像素索引、DINOv3 亲和度注入实例监督），单步同时出点图/法向/实例：点图 Rel^p 4.16（无内参），深度 Rel^d 2.79 优于 MoGe-2 2.87。',
 '2611.29614': '把问题从「精修 R/t」改为「在 SLAM 与 HMR 之间选择性迁移信息」：只从相机几何取 heading、从 HMR rollout 取重力相对 tilt，training-free 插件：EMDB-2 W-MPJPE100 154.0 mm，相对 GVHMR 降 44.3%。',
 '2611.29647': '把沉浸式视频的效应评估从「曝光即时」推进到「曝光后 14 天」：84 名被试随机分组，心理亲近感在 7 天内显著高于 2D 组、14 天仍高于自身基线，早期自发投入比例 45.9% vs 13.2%（摘要级证据）。',
 '2611.29678': '把合成目标直接定义到面板子像素几何（K<V 的 angular anchor + 可微三线性采样）而非追求更逼真的生成：消费级 GPU 上 1440×2560 面板 34–40 FPS、显存 1.23 GiB，VRoid 域内 LPIPS 降 20.12%–55.62%、Nat-RMSE 降 40% 以上。',
 '2611.29693': '把「是否发生有意义的手–物交互」提升为一等筛选条件（VLM 三准则显式验证而非动作词匹配），并用 SAM 3 补全手框：约 200K 片段，抽检 500 段场景/活动标签联合正确率 >92%、MANO 通过率 95%，已开源。',
 '2611.29838': '把插值位置从 RGB 或 pointmap 换到基础模型的 latent 特征上，同时保留几何先验与细粒度时间线索，并用「连续颜色预测 → 模拟事件 → 与真实事件流比对」做自监督：DSEC 平均 AbsRel 0.1594 对 TimeLens 0.1991，ATE 0.2242 m 对 0.6349 m。',
 '2611.29897': '把「远历史可读」与「低延迟」拆成两个问题分别解决（Mamba 递归状态 + PCM 映射成注意力键值）：HiPHI 18.72 s Root/End CE 2.87/8.45 cm 对 MotionStreamer 6.17/18.93 cm，MuJoCo + Unitree G1 共 100 次试验。',
 '2611.29920': '指出「证据来自表示自身」的循环：用事件这一与高斯覆盖、光度收敛都无关的外部观测同时决定「哪里需要新支持」与「谁是可靠运动参考」：dPSNR +1.02（合成）/+1.45（真实），动态高斯总数降 8.5%，代码与数据公开。',
 '2611.30012': '把 3D 视线监督从专用设备迁移到互联网规模 head crop（2D 视线目标 + 场景深度自动构标签，约 324 万 head instance），推理端去掉人脸检测与头姿估计，八个基准统一协议下多数匹配或超过参数量数倍的公开估计器（摘要级证据）。',
 '2611.30042': '用「状态由动作驱动、视觉只负责呈现」的因子化替代显式地图与可见性测试，让离屏角色零渲染成本地继续演化：30 s rollout LPIPS 0.249 对无状态基线 0.344、FVD32 137.5 对 299.8，10 min rollout 仍保 >50% recall/precision 而对比方法 ≤2%。',
 '2611.30102': '把「剪枝后其他高斯也不在」写进重要性定义，并用 μ-σ rendering 对随机移除下的像素均值与方差给闭式解：90%/99% 移除且无微调，3 数据集 × 18 个指标列中 16 个最优（99% 移除 Mip-NeRF360 PSNR 16.53 对 GaussianPOP 15.38）。',
 '2611.30166': '目标不是更强的 LIO，而是把「闭源 ARKit 流水线 vs 开源可检查流水线」的差距拆成可归因误差预算：7 个 ScanNet++ iPhone 场景与 ARKit 参考偏差 0.2–2.0 m，六个开源 LiDAR-惯性估计器在 42 次运行中 41 次 ATE ≥4.46 m，并有 iPhone 应用与 replay（18 ms/关键帧）。',
 '2611.30173': '把低光失败从「精度下降」重述为机制问题：网络在暗处不是失去信心而是制造信心（两帧 9 级纯噪声也给出 g=0.936，真实暗帧 0.935），同一统计量被方向相反的两个阈值共同消费，导致静默退出；Jetson AGX Orin + Spot 真机 scope test，可用轨迹 1/6→5/6。',
 '2611.30184': '把「历史身份改写」与「新表面接纳」拆成两个独立授权问题，用留一帧最坏裕度 + 组内两两兼容性约束避免传递性误合并：KITTI-360 两窗口 mean building/car AP50:90 17.259→18.762，所有新增坐标来自实测源并保留证据记录。',
 '2611.30226': '把交互式 3D、可执行 code-as-action、确定性验证与受控输入诊断放进同一基准，并把「动作 harness」当实验变量：同实例 V/S/C 对照量化视觉失败，MazeNavFPS 上 Batch 把 Pass@1 从 0.57 提升，代码与数据集开源。',
 '2611.30351': '把「光空间区域光照聚合」引入 Gaussian 散射显式建模非局部光传输，而非在单个 Gaussian 上回归散射残差：SSS-GS 合成 mean PSNR 41.27 对 RNG 38.80（+2.47 dB），真实场景 33.88 对 33.07，渲染约 60 FPS。',
 '2611.30388': '证明只依赖「已播出语音」即可在不重训的情况下驱动五种差异极大的后端（含只暴露音频的云 API），并把角色/音色/动作风格/外观做成四路正交控制：82% 强迫选择偏好其身体动作，躯干高频能量 36.4→3.5，两张消费级 RTX 5090 实时。',
 '2611.30392': '把极性分离的 spike-latency 表示与 LTC 启发的门控 Euler 递归单元结合，用于纯事件低光近眼视线估计：Gaze-FELL 跨被试平均方向误差 3.75°、跨场景 2.41°，首次系统评估不依赖灰度引导帧的纯事件设置。',
 '2611.30552': '把「只改呈现身体、不改商用服务界面与回复生成」做成可随机分组的实验仪器（浏览器端标签页音频耦合，对服务无代码依赖）：全文仅报告设计与实现，尚无用户研究与性能指标（按诚实口径 EXP/PER 记 1）。',
 '2611.30607': '把 DNO 从文本条件 HOI 扩展到 TriDi 的三边多模态分布，在不重训、不加 guidance 的前提下直接优化初始噪声，并新增朝向损失针对「接触与穿透都满足但手背贴物」：GRAB 严格判定有效抓握 11%→41%，PEN-X（>15 mm 穿透）26.3%→12.3%。',
 '2611.30629': '不只做底层 GPU 加速，而针对 2DGS 优化的两个失效模式（覆盖慢、细化抖）设计初始化/EMA/渐进/光流引导，压缩端显式用时间相干性：UVG 50 帧编码 7.56 小时→34 分钟（13.4×），同 PSNR 下 bpp 降约 46%，同 bpp 下 PSNR +1.9 dB。',
 '2611.30734': '用主动红外立体在目标相机原生鱼眼坐标重建动态操作的真值米制深度（球杆独立验证中位误差 1.27 mm），并把「精度」与「覆盖率」联合评测、把手与物体作为独立 ROI：941,233 样本 / 37 环境，UniDepth v2 为最佳米制单目 AbsRel 0.201。',
 '2611.30777': '把 VLM 智能体用于「决定重建结构」而非仅生成资产：智能体回答服装/层序问题并据此为每人搭建不同初始化与优化计划，输出身体/头发/每件服装/鞋各自独立网格：100 个扫描 CD 1.92→1.36 cm（−29%），可直接加载 Blender / Unreal / MuJoCo。',
 '2611.30787': '把单目深度与 MVS 的关系从「单向引导」改为逐 stage 双向动态更新（也用代价体几何证据反标定 DPT 中间特征）：DTU overall 0.268 mm 对 MonoMVSNet 0.278，ETH3D 测试集 F1 86.78 对 GoMVS 85.91，代码开源。',
 '2611.30898': '把预训练视频世界模型直接当 LAM：同一 DiT 兼任 IDM 与 FDM，dynamics registers 是唯一接口，不新增 encoder/decoder：LARY 动作分类 top-1 71.77% 对 WLA3 70.75%，RoboTwin 2.0 成功率 93.6% 对 π0.5 79.8%，并有 AgileX NERO 真机闭环。',
 '2611.31018': '不放松离散坍缩决策，而是固定坍缩历史、只对由此确定的顶点位置映射求导，把简化误差回传给上游几何参数：低多边形重建 K=1000 CD 1.26e-5 对 QEM 1.92，逆渲染 K=2000 PSNR 27.29 dB 对 QEM 25.43，已实现前反向 CUDA 并接入 FlexiCubes。',
 '2611.31023': '把瞬态遮挡与跨视图外观变化在同一前馈 3DGS 中联合处理（transient mask 不只重加权光度损失，还调制体素融合置信度）：RealX3D 9 视图 PSNR 19.83（次优 WildSplatter +约 2 dB），12 视图 19.56 dB，前馈推理无需逐场景优化。',
 '2611.31143': '在原生 3D latent 生成器内部、而非 2D 图像空间做对应路由的联合去噪（每个 3D token 只 attend 其他帧中同一头部点的少量 token）：NPHM 头部 Chamfer 4.83→3.27 mm（−32%），跨帧一致性 9.48→5.03（−47%），8 图约 2.3× 单图耗时。',
 '2611.31215': '把「证据获取」从评测中显式分离：固定同一模型为 reasoner、只替换观测来源（自身策略 / 同预算随机游走 / oracle 路径）：994 问题 / 234 episode / 72 真实扫描场景 / 23 个 VLM，Claude Opus 5.5 主动 74.0% 对 Blind 44.1%、Passive-40 76.4%。',
 # ---- backfill ----
 '2511.20578': '把「单张照片 → 个性化手部轮廓与电极布局 → 可打印液态金属柔性器件」的制造闭环与 15 通道电触觉渲染结合：五指指长估计平均相对误差 <2.5%（10 名受试者），多数手指绝对误差 <0.5 cm，有 Unity + VR 头显真机演示。',
 '2605.00389': '把 juicy design 的视听强化与 PBL 式进度/徽章统一为「任务对齐的形成性反馈」，并用新手/专家两组说明同一游戏化层分别起脚手架与执行优化作用：新手置管时间 57.41→46.57 s、SUS 58.13→78.54，专家 75→45 s（Quest 3，36 人）。',
 '2607.11627': '让 Ball Pivot 真正可增量地产出流形且可定向的网格（动态八叉树 + 空球违例回删 + 非流形顶点清理 + 朝向校验），并把「孔洞」定义为「本应有数据却缺失」而非未探索区域：三个离线数据集重建 7–22 s，开源并带 ROS 集成与真机水下实验。',
 '2608.04701': '用「源→目标→源」往返投影生成源视角有效性掩码，在渲染前剔除不可靠投影，从条件端消解大基线遮挡歧义：静态 CO3D PSNR 19.11→20.00，DL3DV 15.41→15.82，并把大基线 NVS 延伸为显式 dynamic 3DGS 4D 资产生成，代码开源。',
 '2608.28386': '在类别无关、无预定义网格的单图设定下，把「接触对应 → 手指关节优化」做成显式可微阶段，并主张用 CPP（接触–穿透联合）指标评判抓握：ARCTIC PA-MPJPE 10.89→7.69 mm、CPP 60.34%→72.83%，ProciGen-GRAB CPP 78.15%。',
 '2610.41373': '把「视角」而非「图像或点」当检索与推理的一等对象（带位姿结构化 caption 索引 + 几何支撑门控 + 条件满足回路），并显式输出「证据不足」：目标视角查询 confirmed correct 26.8%→90.4%，作答覆盖率 97.6% 时精度 92.6%。',
}

def esc(s):
    return str(s).replace('|', '/')


def slugify(t):
    return re.sub(r'[^a-z0-9]+', '-', t.lower()).strip('-')[:52]


def bullets(text):
    if isinstance(text, (list, tuple)):
        return '\n'.join(f'- {str(x).strip()}' for x in text if str(x).strip())
    parts = [x.strip() for x in re.split(r'[；。]', str(text)) if x.strip()]
    return '\n'.join(f'- {x}' for x in parts)


def tags_for(p, g):
    base = [p['track']]
    for kw in ['Gaussian', 'SLAM', 'VR', 'AR', 'haptic', 'tactile', 'avatar', 'world model',
               'diffusion', 'head-mounted', 'eye tracking', 'egocentric', 'depth', 'VIO', 'relight',
               'VLA', 'hand', 'event camera', 'light field']:
        if kw.lower() in (p['title'] + ' ' + str(g.get('method', ''))).lower():
            base.append(kw)
    return base[:5]


NOTE = '''---
id: arXiv:{id}
title: {title}
title_zh: {title_zh}
track: {track}
venue: {venue}
date: {date}
value: {value}
grade: {grade}
evidence: {evidence}
status: CURRENT
superseded_by: []
scores: {{IMP:{IMP}, NOV:{NOV}, TEC:{TEC}, EXP:{EXP}, PER:{PER}, TRL:{TRL}, REP:{REP}}}
fetch_level: {level}
batch: {batch}
announce_type: {announce}
in_top10: {in_top10}
published: {published}
recall: {recall}
tags: [{tags}]
---

# {title_zh}

## 一句话结论
{concl}

## 要解决的问题
{problem}

## 方法详解
{method}

## 实验与结果
{exp}

## 创新点与贡献
{nov}

## 局限与风险
{lim}

## 与文献库的关系
- 本批新增（batch `{batch}`，公告类型 `{announce}`），赛道「{track}」{rank}
- 本批 OUTDATED / SUPERSEDED 判定为 0，未发现直接取代关系。
- 公告日 2026-11-24（周二）≠ 拉取日 2026-11-25（周三 02:30）；11-24 组由周末 11-21/11-22 与周一 11-23 的提交合并释放。API 首次提交日 {published}。
{note}

## 可复现性（代码/数据/硬件）
- 代码/项目页：{code}
- 全文证据：{evidence}（{level}，{chars:,} 字符）

## 行动建议
{action}
'''

os.makedirs('papers/notes', exist_ok=True)
n_notes = 0
for p in D:
    if p['grade'] == 'C':
        continue
    g = DIG[p['id']]
    m = MAN[p['id']]
    p['level'] = m['level']; p['chars'] = m['chars']
    fn = f"papers/notes/{p['id']}__{slugify(p['title'])}.md"
    if os.path.exists(fn):
        print('skip', fn); continue
    rank = f"，本批 Top10 第 {TOP10.index(p['id'])+1} 名" if p['id'] in TOP10 else ''
    action = ('- 纳入重点精读：方法与实验节可直接支撑选题与技术选型。' if p['grade'] == 'A'
              else '- 浏览级：关注问题设定与结论，方法细节按需回看。')
    action += ('\n- 有公开代码/项目页，可先跑通再评估迁移成本。' if p.get('code') and p['code'] not in ('未提及', '未提供', '无')
               else '\n- 未提供代码，复现需按正文细节自行实现。')
    if p['value'] >= 4.20:
        action += '\n- 达 S 线（≥4.20）而本批门③ 判定非重磅日（margin −0.222）：值得优先读，但按口径记 A，不宜按 S 级对外表述。'
    body = NOTE.format(
        id=p['id'], title=p['title'], title_zh=p['title_zh'], track=p['track'], venue=p['venue'],
        date=DATE, value=f"{p['value']:.2f}", grade=p['grade'], evidence=p['evidence'],
        IMP=p['scores']['IMP'], NOV=p['scores']['NOV'], TEC=p['scores']['TEC'], EXP=p['scores']['EXP'],
        PER=p['scores']['PER'], TRL=p['scores']['TRL'], REP=p['scores']['REP'],
        level=p['level'], batch=p['batch'], announce=p['announce'], in_top10=str(p['in_top10']).lower(),
        published=p['published'], recall=p.get('recall') or 'KW/TITLE', tags=', '.join(tags_for(p, g)),
        concl=CONCL[p['id']], problem=g['problem'], method=g['method'],
        exp=bullets(g['key_numbers']), nov=bullets(g['novelty']), lim=bullets(g['limitations']),
        rank=rank, note=(f"- 备注：{p['note']}" if p.get('note') else ''),
        code=(p.get('code') or '正文未提供'), chars=p['chars'], action=action)
    open(fn, 'w', encoding='utf-8').write(body)
    n_notes += 1
print('notes written', n_notes)


# ---------- MOC ----------
def moc(papers, path, title, intro):
    L = [f'# {title}\n', intro + '\n', '## 本批论文（按加权降序）\n',
         '| # | 论文 | 赛道 | 总分 | 等级 | 证据 | 笔记 |', '|---|---|---|---|---|---|---|']
    for i, p in enumerate(papers, 1):
        note = glob.glob(f"papers/notes/{p['id']}__*")
        link = f"[→](../notes/{os.path.basename(note[0]).replace(chr(92), '/')})" if note else '→（C 级仅入馆）'
        L.append(f"| {i} | {esc(p['title_zh'])} | {p['track']} | {p['value']:.2f} | {p['grade']} | {p['evidence']} | {link} |")
    L.append('\n## 批次要点\n')
    for p in papers:
        L.append(f"- **{esc(p['title_zh'])}**（{p['id']}，{p['value']:.2f} {p['grade']}）：{CONCL[p['id']]}")
    open(path, 'w', encoding='utf-8').writelines([x + '\n' for x in L])


MAIN = [p for p in D if not p['batch'].startswith('backfill')]
BF = [p for p in D if p['batch'].startswith('backfill')]
MAIN.sort(key=lambda r: (-r['value'], -r['scores']['IMP'], -r['scores']['NOV'], r['id']))
BF.sort(key=lambda r: (-r['value'], -r['scores']['IMP'], -r['scores']['NOV'], r['id']))
g3 = G['gate3']
moc(MAIN, f'papers/MOC/MOC-{DATE}.md', f'MOC · {DATE}（11-24 公告批次 · 大公告日 · 68 篇）',
    '> 当日地图：**公告日 2026-11-24（周二）≠ 拉取日 2026-11-25（周三 02:30）**——诚实口径；'
    '11-21/11-22 为周末 `skipDays`，其提交与 11-23（周一）提交一并于 11-24 公告释放。'
    '主批 API published 核验：**11-23×29 / 11-21×17 / 11-22×14** 为三大宗，另有 11-20×1、11-19×1、11-18×1、11-17×1、11-16×1、'
    '11-04×1、10-30×1、10-05×1、09-18×1（延迟公告）——**published 不能当前缀推断提交月**。\n'
    '> 主批 XR 新稿 **68 篇（0 S / 44 A / 22 B / 2 C）**，Top10 实数 10 篇最高 **4.21**（HoloSplat 实时自由视点人体流式）；'
    '11-24 组 **1,285 槽位 / 1,045 篇唯一**（本库史上最大公告组），RSS 1,547 条覆盖率 1,045/1,045、缺收 0 → 免 API id_list；'
    '摘要级 KW 100 + 标题级补扫 46 = 146 → 逐篇核摘要剔 84 → 62 篇；残差复核（899 条，2.4%）再采纳 6 篇 → 68 篇。\n'
    '> 全文：**72 篇 L0 + 2 篇 L1**（其中 72 FULL + 2 PARTIAL：2611.29647 与 2611.30012 的 ar5iv 仅返回摘要落地页，'
    '按摘要级评估并在本批显式声明）。\n'
    '> 覆盖度三关：门① **0.263**（2611.28802 vs 库内 arXiv:2609.23436）/ 门② **6 赛道**（未触发重筛）/ '
    '门③ **4.21 vs 4.432**（现算，半开窗口 [2026-10-26, 2026-11-25) 且按 batch 剔除本批两批，464 条入窗）'
    '→ **margin −0.222，blockbuster=false，无 S**；HoloSplat 4.21 达 S 线按校准关记 A。')
moc(BF, f'papers/MOC/MOC-backfill-{MMDD}.md', f'MOC · backfill-{MMDD}（旧稿 replace 再公告首次入馆）',
    '> **非当日新提交**：本批 6 篇均为 11-24 公告 RSS 混入的 `replace` 类旧稿再公告（首发 2025-11 至 2026-10），'
    '按诚实口径单独编号，不参与当日重磅日判定，最高记 A。\n'
    '> 定稿 **5 A / 1 B（无 S）**：2608.04701 UniView 3.77 · 2608.28386 GraspHOI 3.70 · 2511.20578 电触觉器件 3.48 · '
    '2610.41373 QGVI 3.48 · 2607.11627 IBPA 3.30 · 2605.00389 VR 游戏化训练 3.23。')
print('MOC written')

# ---------- registry ----------
reg = 'papers/library/registry.jsonl'
bak = f'papers/library/registry.jsonl.bak-{DATE.replace("-", "")}'
if not os.path.exists(bak):
    shutil.copy(reg, bak); print('backup ->', bak)
rows = [json.loads(l) for l in open(reg, encoding='utf-8') if l.strip()]
have = {r['id'].split(':')[-1].split('v')[0] for r in rows}
added = 0
with open(reg, 'a', encoding='utf-8') as f:
    for p in D:
        if p['id'] in have:
            print('exists', p['id']); continue
        e = dict(id=f"arXiv:{p['id']}", title=p['title'], title_zh=p['title_zh'], track=p['track'],
                 date=DATE, value=p['value'], grade=p['grade'], scores=p['scores'], status='CURRENT',
                 evidence=p['evidence'], fetch_level=p['level'], fulltext_chars=p['chars'],
                 in_top10=p['in_top10'], batch=p['batch'], announce_type=p['announce'],
                 published=p['published'], flags=[])
        f.write(json.dumps(e, ensure_ascii=False) + '\n'); added += 1
total = len(rows) + added
print(f'registry +{added}（{len(rows)} -> {total}）')
print('notes', len(glob.glob('papers/notes/*.md')), 'daily', len(glob.glob('papers/daily/*')),
      'moc', len(glob.glob('papers/MOC/*.md')))
