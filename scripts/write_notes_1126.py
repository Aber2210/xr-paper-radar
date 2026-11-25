# -*- coding: utf-8 -*-
"""2026-11-26 产物：原子笔记 / 当日 MOC / backfill MOC / registry 幂等追加。

口径要点（不可改写）：
- 公告日 2026-11-25（周三）≠ 拉取日 2026-11-26（周四 02:30）；11-26 组尚未公告。
- 主批 55 + backfill 8 = 63；S3 / A24 / B29 / C7；门③ blockbuster=true，S 授予 3 篇。
- C 级 7 篇仅入馆，不写笔记。
"""
import glob
import json
import os
import re
import shutil

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
os.chdir(ROOT)
DATE, MMDD = '2026-11-26', '1126'
ANN = '2026-11-25'

D = json.load(open('data/scored_%s.json' % MMDD, encoding='utf-8'))
G = json.load(open('data/gates_%s.json' % MMDD, encoding='utf-8'))
MAN = json.load(open('data/fulltext/_manifest.json', encoding='utf-8'))
PUB = json.load(open('data/published_%s.json' % MMDD, encoding='utf-8'))
TOP10 = G['top10']

DIG = {}
for k in range(1, 9):
    for r in json.load(open('data/digest_%s_g%d.json' % (MMDD, k), encoding='utf-8')):
        DIG[r['id']] = r
assert len(DIG) == 63, len(DIG)

CONCL = {
 # ---- Top10 ----
 '2611.32198': '把 4D 预测收敛成「一次 query 返回 allo/ego 成对点图」这一接口：几何、运动、相机位姿由同一组稠密坐标给出，位姿退化为闭式刚体对齐且不依赖参考帧——3D 跟踪全点 RelEPE 相机系 0.084 vs V-DPM 0.160（−47.5%）、世界系 0.077 vs 0.138，多视图重建全局点 AUC@25 79.26% vs 同数据同初始化训练的 π3 73.41%，Oxford-Spires 500 帧单次前向零样本仍比基线快 1.7–4.3×。',
 '2611.32445': '把 coarse mesh 当地址而不是画布：在物体自身坐标系按表面积分 cell 存渲染器自己的 K/V，使外观随物体移动与关节运动一起走、跨 agent 共享同一地址——动态场景 object permanence 91.5 vs 最强基线 34.7（HSSD）、94.1 vs 43.4（MutableWorlds），跨 agent 一致性 79.99 vs 42.60，720p 41.1 FPS 且 8,001 帧 rollout 峰值显存 <45 GiB。',
 '2611.32523': '把 imperative learning 用于「仿真预训练本体感知模型 → 真机」的跨模态自适应：腿式里程计精化视觉地图，精化后的地图再以重投影而非位姿回归监督网络，并用稀疏伴随避免展开 BA——GrandTour 17 条序列常规 ATE 0.15 m / 困难 0.23 m，是唯一全部 17 条都 <0.4 m 的方法；Unitree Go2 上漂移 0.59% vs 最佳对手 OKVIS2 1.55%。',
 '2611.31757': '把「尺度」从隐变量提升为一等状态：每个窗口一个对数尺度比、闭环再带一个独立环路尺度，用度量深度先验或 IMU 因子给绝对锚点，从机制上阻断逐窗口 handover 误差累加——VBR 单目 ATE 5.40 m（AMB3R-SLAM 7.42、CLoSeR 11.15），KITTI 9.79 m（13.11），单张 RTX 5090 上 10–21 FPS。',
 '2611.32351': '用三组可学习 gaze query 把 depth、head mask、target heatmap 三种先验内化进 VLM latent（训练时监督、推理时不需要任何外部输入），并把点/框/热图/语言统一进一个自回归输出空间——HoliGaze-Bench GTL-T2P L2 0.094 vs 同骨干 0.387，GTL-T2B mIoU 0.333 约为 Qwen3.8-27B 的 2.2 倍，而骨干只有 2B。',
 '2611.32482': '免训练地利用「人体与场景基础模型其实重建了同一张可见人体表面」做稠密像素级 3D 配准，把序列级尺度与逐帧平移解耦、再用跨帧一致投票稳定尺度——3DPW HS-CF5 0.688 较 Human3R 1.079 降 36.2%，EMDB-2 全局人体运动较 HAC 降 40.7%/53.6%，只增加约 4 ms/帧。',
 '2611.31944': 'training-free 的两级检索（相机位姿/视锥粗 grounding + draft attention 细选）配合 tile 级流式 attention，使取数沿 FlashAttention tile 粒度与计算重叠——ORBIA persistence 58.98 vs 56.67、5.49 FPS vs WorldKV 4.71、显存 18.56 vs 21.33 GiB，首次让 33B 级世界模型在单张 80 GiB H100 上做历史 KV 检索。',
 '2611.31516': '给 OSE 只加一项相对深度残差（保持 variable projection 可分性），并让 metric depth 贯穿对应过滤、随机初始化与联合精化——ETH3D 位姿 AUC@20° 85.81% vs pOSE 13.91%，去掉 joint metric refinement 即跌到 31.99%，说明「代理目标」并非精度主因。',
 '2611.31918': '把 3DGS 的三个角色拆到不同粒度：8×8 tile 只做光栅化、64×32 macro-tile 做划分与排序、bounded batch 做独立工作与反向求导——1080p 2756 FPS / 4K 1533 FPS（相对 gsplat 5.1×/5.6×），负载不均视角上快 6.8×–20.0×，训练 61.5 s vs 194.4 s。',
 '2611.31812': '物体侧只用冻结位姿基础模型的内部几何特征、不学实例嵌入，接触则由「粗 token 逐关节预测 + 重建 SDF 区域距离细化到掌/背侧」两级落地——DexYCB 物体 AUC 92.88（比 SemiHand 高 10.25），OakInk 未见物体 AUC 93.29 vs SemiHand 40.50，接触 F1@3mm 74.97 vs HACO 68.09。',
 # ---- 主批其余 ----
 '2611.32297': '把 3D 预训练分工为「图像表征完全交给冻结 2D 基础模型、自监督只学跨视图交互」，并在同等更新数与架构下证明无标注预训练 + 有监督微调能超过单阶段监督：S 规模 DL3DV 位姿 AUC@30° 54.23% vs 直接监督 VGGT-Ω 35.89%，1.144B 规模 ETH3D 49.26% vs 40.66%。',
 '2611.32727': '把「支撑图」提为连接感知与仿真的中心数据结构，同一张 DAG 同时决定落座顺序、多支撑物体的位姿采样约束与细化优先级，多支撑用成对接触点加解析 roll 的闭式候选替代随机采样：50 场景 10 s 后 source-mask IoU 51.7% vs 最强基线 40.7%，intended supports 实现 87.1%。',
 '2611.32876': '把「有效利用时序上下文」建成记忆问题：短期事件记忆按遮挡/出视野事件自适应决定读取长度，长期尺度记忆把稀疏但可靠的尺度证据（度量深度 + 静态手掌视差）压进有界状态，出视野补全搬到世界系做手-头协同——ARCTIC W-MPJPE 41.46 mm vs StableHand 91.25（−57%），HOT3D 14.20 vs 46.76。',
 '2611.32932': '首次把「全身—手臂—腕—手指」的操作层级写进单目 4D HOI 重建：物体作固定锚点、ReachNet 在身体/手臂层把人拉到物体旁、TouchNet 在指级依时序局部表面几何定形抓握，并把运动历史以 FiLM 注入物体位姿精化——ARCTIC 物体 CD 6.40 cm vs CARI4D 14.55（−56%），手部接触 F1 0.866→0.921。',
 '2611.32171': '把几何 RoPE 的 frequency band 从隐含默认值提为受控自变量，证明它由 backbone 维度隐式决定、在跨方法比较中普遍未被匹配或报告、且足以反转排名，并给出前向-反向不对称的解析解释：默认配置落后 WorldRoPE 1.22 dB，把 4 个频率铺满 243× 后回到 26.44 dB（+0.9 dB）。',
 '2611.32816': '用同一套指标与同一套对齐规则同时评 5 个几何任务 × 52 个模型，把「对齐」从实现细节变成可测量的偏差来源（最高 2.6×），并以自采真实场景证明「公开集饱和但真实场景未饱和」：VGGT-Ω 总榜 87.4 / 平均排名 2.6 居首，π³-X 84.3 第二。',
 '2611.32540': '把秩二 3×3 标定基础矩阵等距映到 2×2，使本质约束从非线性流形条件变成两个线性子空间的隶属问题，得到平方范数恰等于流形距离的光滑两分量残差，同时去掉秩亏与 SVD 开销：ETH3D 焦距中位相对误差 0.24%、AUC@5 0.894（SVD 版 0.886），四个数据集上均不劣于原目标。',
 '2611.32491': '把「布局预测」重构为「多视图相机预测」：asset render 当额外 view，物体位姿由预测相机与已知 render 相机闭式相除，因此复用 VGGT-Ω 预训练先验、只加极少量参数且无需 3D encoder——IndoorMix CD-S 7.29 vs SceneMaker 12.86（−43%），单次前向约 1 s 联合放置全部物体。',
 '2611.31950': '不改手模型也不改估计器，把接触问题从「更好的姿态」转为「可形变的表面」：逐面 Jacobian 形变正则（掌侧软化/背侧加硬）配骨骼静止系时序先验，抬升后的标注再训练 contact head 形成自举——接触带贴合度约 20%→近 50%，深穿透顶点 DexYCB 38.6→2.9、OakInk 18.4→1.5 每帧。',
 '2611.32883': '首个单目 RGB + 同址事件的 3D 任意点跟踪器：把「相机诱导刚性运动」作为迭代内的运行期参照而非一次性预处理，使 IMO 分割与轨迹精化互为条件——帧间时刻 3D EPE 0.148 m vs Track4World+插值 0.284 m，可在没有 RGB 帧的时刻输出 200 Hz 轨迹。',
 '2611.32335': '把跟踪与建图都放进同一个球面域：位姿更新、协方差投影、渲染与深度一致性共用一套 ERP 几何，实测 LiDAR 深度当监督、预测深度只用于盲区补洞——相对 ODGS-SLAM / PanoGS-SLAM 平均 PSNR 提升 9.10 / 5.56 dB，Hilti-Oxford ATE 0.059 m（FAST-LIVO2 0.064）。',
 '2611.32476': '把触觉生成从「穿透深度后处理」改为「接触求解器锚定 + 法向刚度对齐 + 滑/黏解耦切向重建 + 保力矩摩擦锥投影」，在不牺牲 GPU 并行下同时修好法向饱和与切向欠定——法向力 RMSE 2.31→0.42 N（−81.8%），触觉流水线 56.0→2,482.9 FPS（256 环境）。',
 '2611.32202': '把压缩从「编码给定原语」改为「在学到的场景潜空间里搜这个场景的码」，码长与原语数量解耦、解码器可自由生成更适合渲染的新原语：Mip-NeRF 360 上 27.93 dB @7.46 MB（比 HAC++ 的 8.61 MB 高 0.46 dB），28.09 dB @10.89 MB（比 18.48 MB 高 0.49 dB）。',
 '2611.32732': '第一个把「提前提交 + 晚到视角增量并入」做成完整流水线的实时体积流媒体系统，用覆盖增益对等待代价的在线权衡替代固定/中位数等待，并在压缩前而非传输后消掉跨视角冗余：同 150 ms 预算 SSIM +10.9%、IoU +13.7%，p95 到达离散度下仍守尾延迟。',
 '2611.33137': '在「艺术家手工 + 可仿真 + 部件标注」三者交集上把规模推高一个量级，并用同一套部件标注同时支撑材质/实例感知与 affordance-aware 抓取，把 affordance accuracy 作为独立指标引入移动操作基准：6,499 场景 / 115K 资产 / 567,506 实例，约为次大艺术家数据集的 5.7 倍。',
 '2611.32716': '在纯点云、无图像、无位姿、无 3D 训练、无监督提议五个约束同时成立下做零样本 3D 分割：面元化 + 泼溅自造虚拟视图，把视角选择形式化为深度检验下的 k 覆盖问题，再用 2D 掩码投票聚类——Replica mIoU 36.2 vs Ov3R 31.9，是唯一仅用 3D 模态且零训练的参赛者。',
 '2611.31766': '把纯手部文本-动作数据推到 541,929 段 / 884 h（CLUTCH 时长的 10.6×），提 393 维双手冗余表示与五级层级描述，并系统揭示「语义对齐」与「运动学合理性」之间的排序分裂：MoMask 上 R@1 0.547 vs MANO-102 0.395，说明纯手生成不能只用检索类指标评价。',
 '2611.31836': '首个同时检测与预测第三人称视频中指定人物 typed semantic gaze target 转移的模型，把注视建成 world modeling 问题（冻结 V-JEPA 2.1 上联合 latent scene prediction 与 person-conditioned gaze 监督）：四类 shift AP 76.09 vs PaGE-H+ 66.32，二类 shift F1 82.17 vs 74.42。',
 '2611.33157': '把「多视角一致」从损失项或后处理变成表示层面的必然结果：预测单元是表面点而非像素，沿 track 池化后再解码一次，同一点跨视角分歧按构造为零——ETH3D 逐视角 albedo RMSE 0.095 vs MVInverse 0.161、法向 2.9° vs 9.6°，且精度随视角数增加而提升。',
 '2611.32025': '把在线 3DGS 地图的模型复杂度当一等约束：视角准入速率与更新分配由流式进度决定、高斯数量由图像细节的秩决定、floater 抑制改用地图像自累积的面参考而非前端深度——Aria 自采序列 PSNR 20.92 dB（HI-SLAM2 18.09、Photo-SLAM 17.10），LPIPS 0.463 vs 0.626。',
 '2611.32034': '把「身体条件」做成贯穿生成全过程的两级空间参照（GBA 在稀疏结构层定放置与延展、LBA 在潜变量表面细化时用 KNN + 3D RoPE 只聚合邻近身体几何），并用 SDF 余量违规回传到潜空间：GarmentWeave3D CD 6.36 mm、穿透率 0.080% vs Garment3DGen 31.007%。',
 '2611.32998': '证明「精确神经表面重建不需要联合优化外观」：只用首交点 patch 光度一致性 + 几何驱动的显式可见性（1-Lipschitz 网络配 sphere tracing、用隐函数定理绕开迭代反传）——BMVS 8 场景平均 CD 2.02e-3 为对比方法最低（Geo-NeuS 2.17、PGSR 2.56），8 场景中 5 个最优。',
 '2611.33145': '用 RTK 支撑的 3DGS 真实校园替代合成引擎与离散拓扑图，把「真实户外 + 连续可导航 + 米制尺度 + 具身闭环」四条件同时满足，并用 oracle 干预把 QA 弱项与导航失败建立因果联系：最强 Gemini-3-Flash 仅 SR@5 49.60%、SR@2.5 25.73%，开源最强 SR@5 36.20%。',
 '2611.31428': '把「前馈先验 vs 稀疏高斯」的取舍转成频域可靠性问题，用实测近似 1/f 律的一参数低通核解释权重，再「融合成 teacher → 蒸馏回 Gaussian」（推理期不引入任何额外网络）——StereoGS / DropGaussian / FSGS 分别 +1.01 / +1.01 / +1.18 dB，且弱先验会自动得到接近 0 的 f0。',
 '2611.32970': '在 recurrent DFF 中把冻结单目先验以闭式局部 scale-shift 反复对齐到当前估计，形成 refinement–alignment 反馈环，把纹理区的 metric scale 传进弱纹理区，并以焦平面序号而非 disparity 像素作更新单位：NYU Depth V2 AbsRel 0.0513 vs FOSSA 0.080（−36%）。',
 '2611.32996': '把 BLV 沟通偏好拆成「参考答重构 + 按问句表层形式确定性路由 + 正确性优先的分层 reward 后训练」三段闭环，Filter-GRPO 让「全对但质量有差」的组也能提供梯度：InternVL2.5-8B 67.00% vs EgoBlind 62.88%，BLV Score 3.2878 vs 3.0660，部署时退化为单次 greedy 解码。',
 '2611.31720': '把 SSM 式的持久状态搬到事件平面：状态转移同时依赖真实经过时间（指数保留）、学习式图像平面 backward transport 与局部事件支撑门控，输出域是单个事件而非整幅像素——MVSEC outdoor_day1 AbsRel 0.286 vs ScaleEvent 0.357（−19.9%）、RMSE 4.745 m vs 6.353 m。',
 '2611.31919': '首个把「自由文本任务 + 双手协作角色 + 3D 表面热图」三者结合的数据集：角色与左右手解耦，使同一标注可映射到任意机器人构型，标注侧用首步 token logit 差做视角置信度、角色对比式 SAM2 分割，全流程零人工标注——71K 物体 / 271K 任务，Dual-Espresso-3D 上 aIoU 10.3→37.8。',
 '2611.32361': '把接触次黎曼几何从 2D 图像的曲线搬到无结构有向点云，并给出只用 4 个刚体不变量就能算的闭式 score——法向偏移的惩罚是线性而非二次，这正是它能分离极薄结构而 point-to-plane 失效的原因：Pheno4D 茎叶 mIoU 0.835 vs 欧氏 0.750，FAUST 接触层测地误差 0.0568 vs 0.0828。',
 '2611.31482': '把 SH 的外观建模整体搬到共享 PCA 域（预测、transformer 训练与残差 VQ 共用同一紧凑空间，无需序列级变换信令），并把几何结构显式注入 attention：10 条 MPEG 动态序列平均 BD-rate 相对 G-PCC Amd.1 降 45.48%、相对 InterGS-Lite 降 7.78%，BD-PSNR 分别 +9.98 / +1.10 dB。',
 '2611.32735': '把剪枝准则从手工先验变成在冻结管线上短训练学到的模块，并把管线自身的渲染误差当逐高斯特征抬升进网络（敏感度先验 + 学习偏移保证起点不退化）：保留 50% 时跨 7 条管线 / 3 个数据集平均高 1.8 dB，1.6M 高斯的场在 RTX 4060 Ti 上 5.3 s 剪完。',
 '2611.31803': '把「记忆」拆成 seen-view recall 与 novel-view recovery 两个可分离任务，首次系统评测「记忆内容能否迁移到未见视角」，并用共享 GT 历史的 Continued Rollout 把记忆诊断从轨迹漂移与生成退化中解耦：600 条受控轨迹 × 33 个 UE 场景、8 个模型，两种协议给出互补失败画像。',
 '2611.32513': '识别出「直接对关节做扩散」把随机探索与精确坐标恢复耦合在同一变量上，改为让扩散只作用于中间锚点（找有信息量的局部回归区域），精度交给锚点偏移与加权集成，推理压到 3 步单假设：HO-3D V2 MPJPE 18.5 mm vs A2J-Transformer+ 20.0 mm，遮挡严重的手-物场景收益最大。',
 '2611.31478': '首次系统量化「输入朝向错误」这一被基准与 loader 同时掩盖的失效：跨 5 模型 3 数据集的统一 AUC@30 降幅，12 张里 3 张横置使 Depth Anything 3 从 0.88 掉到 0.52，并解释为何无人察觉（4/5 模型忽略标记、ETH3D 图无 EXIF、代码把横置当数据问题跳过），最后给出修复手段的能力边界。',
 '2611.32311': '首次把分钟级动态多视角视频、视角相关双耳音频、几何与实例标注、配对编辑参考统一在同一场景与时间线下，使观测轨迹与场景内容可分别变化：8 场景 × 120 s、50 固定视角 + 10 移动轨迹、480 条序列 / 16 view-hours，FTGS++ 改混合视角训练后在 7/8 场景全部指标提升。',
 '2611.32475': '把「平移不可观时只估旋转」从工程取舍上升为完整在线系统（滑窗旋转平均 + 共享帧对齐 + 有界信息融合），全程不初始化尺度也不三角化地标，并用「历史视图对同一入射帧的预测一致性」做联合测量选择：轨迹仿真朝向误差仅为常规 SfM+PnP+BA 的 10.7%，3 px 噪声下 1.68°（链式相乘 25.12°）。',
 '2611.32443': '利用 ERP 的水平循环对称把「运动方向相对朝向」的多样性规约成近似前向运动（只做 yaw 循环移位重定向，零参数改动），再用 timestep 相关、per-channel 的门软调节不可靠记忆的注入强度：InteriorGS-OmniRoam 首段 SSIM 0.7935 / PSNR 21.62 vs OmniRoam 0.6930 / 17.35。',
 '2611.32621': '首次把「编辑条件检索」从图像搬到单体 3D 资产，给出「答案 = 参考 + 精确部件改动」的严格定义、五级表面面积粒度与多真值协议，并用仅训练期存在的重建解码器 + 部件 mask 把「改哪里/保哪里」注入池化向量：operation-macro mAP@10 50.4 vs 同输入 fusion 基线 47.2。',
 '2611.32628': '把渐进式 3DGS 的比特分配显式建模为「完成时刻 × 内容可用性」的联合优化，用参考流上的包含梯度与 Gauss–Newton 曲率估计「提前暴露某 Gaussian」的图像收益：完整码流 7.2–7.3 MB（压缩 62–88×），只收一半时 PSNR 与原始 3DGS 差距 ≤0.51 dB。',
 # ---- C 级（仅入馆，不写笔记）----
 '2611.31976': '首次把「手」纳入编码智能体的写入范围并以接触而非位姿参数化手，物体则在成熟物理求解器上带自身材质演化，单程序即可表达多物理混合场景——CodeHOI-Bench 100 个任务（20 真实重建 + 80 生成）上刚体生成成功率 65.0–90.0%、非刚体 40.0–80.0%。',
 '2611.33014': '把「teacher 选择」本身变成受控实验（固定 student、数据、配方与 seed，只变监督源），并给出可在训练前用 10 个标注 clip 估计教师质量的判据（ρ=0.91）：Gaze-LLE 标签训出的 ViT-Small ADE 0.187 vs 人工标注 0.196（9/9 seed 全胜），同时量化了 prompt 内含候选答案导致的复制式伪能力。',
 '2611.32396': '把「关系是否持久」而非「关系是否存在」当核心问题：用序列级反证（分离接触片段、支持区间外独立运动、末端持续漂移）加图级一致性剔掉瞬时接触与同动，再用同一张图同时做观测位姿精化与遮挡运动传播——OmniGibson-Occlusion 平均 F 0.6092 vs 4DPM 0.5864。',
 '2611.32584': '把「轻量 2D 占据栅格 + 左右分扇区振动触觉」作为视觉通道之外的空间感知替代通道，并以固定双相机 + 画面与头显解耦同时解决 360° 眩晕与单相机盲区：20 名被试三模态对照完成时间 56.0→44.7→41.9 s（−23%），碰撞 0.75→0.20→0.30。',
 '2611.32231': '首次把动作识别里的 space-time interest point 当跨视角对应来用：同步标定多相机下同一瞬间的 STIP 即可三角化且自带时间戳，正好对上 4D 高斯的时间中心，因此先用极线+时间去筛候选、比值检验几乎冗余——N3DV 每场景 3.9–11.3 万动态点、重投影 0.65–0.83 px，三个场景 PSNR +0.61/+0.64。',
 '2611.31435': '把「已知外力布局」变成可复用先验：从玻璃罩几何仿真出旋转主导的气流场并冻结，用可微平流让后续真实帧反向修正第 0 帧的隐藏几何，第二阶段把 CFD 大尺度输运与逐粒子可学残差解耦——held-out camera 7 上 PSNR 35.66 dB vs 逐帧 3DGS 29.72、4DGS 30.22。',
 '2604.03667': '把 Set-of-Mark 视觉提示与注视轨迹两个正交信号同时喂给 VLLM，并用逆指数采样把有限帧预算压到交互前窗口，整套改造只在输入与提示层、零训练且跨模型可迁移：LLaVA-OneVision 7B 20.4%→27.2%，Gemini 2.0 Flash 21.0%→27.5%（超过原榜首 5 个百分点以上）。',
 # ---- backfill ----
 '2601.22046': '流式单目重建里把显式三角几何当结构锚点、神经高斯只负责外观，两者松耦合：三角抑制漂移与冗余，外观梯度可反传微调几何但不与之冲突——ScanNet++ 平面 Chamfer-L2 3.53 vs PGSR 3.87（−18.5%），仅 61.6k 基元 / 5.5 分钟，ScanNetV2 平面 5.68 vs ARTDECO 6.05 而基元少 11×。',
 '2610.11810': '把「主动取景」本身当作中间推理目标，用重力对齐的 3D 基础模型 + 离散动作集把语义意图稳定落到几何变换，从而真正合成原观测之外的新视角且零微调：六个 VLM × 六个基准共 5,496 题平均绝对提升 8.2%，GPT-5.4 总体 47.0%→59.0%，Qwen3.6-27B 59.2%→73.0%。',
 '2609.16610': '把「可行性」写进 3D 场景几何而非文字或 2D 像素，用 Point/Embodied 成对设计把「同一动作在不同机身约束下后果不同」变成可测量变量，Intent Path 再把指代解析与具身路径绑定：1,111 道基准题上十个零样本 VLM 最高仅 35.6 分（GPT-6 Astra）。',
 '2605.12074': '首次把掩膜、框、属性、类型化关系、HOI、活动与工序步骤在同一帧、同一物体身份上共注册，使过程级失败可回溯到具体感知层，并用 matched-case 协议把跨层级共失败变成可测量量：185 段视频 / 4.4 小时 / 469,201 标注帧 / 3.61M 实例掩膜。',
 '2508.17255': '把驾驶 AR 重述为「车内 + 车外」双上下文第一人称感知问题，两套独立参考系分别跟踪（与所有单世界系 SLAM/AR 管线的本质差别），并用深度直方图双峰谷底做自适应域分离：车内/车外 RE 13.74 / 17.63 px（ORB-SLAM3 车内 32.75），ARE 1.85° / 5.64°。',
 '2512.12898': '把「邻域」与「查询」两种归纳偏置显式合成为单一算子，并给出可证伪的误差单调性定理与高斯数量指数下界，从理论上说明堆基元不是提升保真度的方向：Mip-NeRF 360 上 3DGS 27.67→27.96 dB、MCMC 28.26→28.58 dB（超过 Zip-NeRF 28.54），且高斯数更省。',
 '2605.20044': '用第二个不透明度把掩膜渲染与成像渲染解耦（每高斯仅 +1 标量 +1 整数），同时解决边界泄漏与「冻结资产不可改」两个问题，并配齐占据损失、离散重分组与无解码读出：ScanNet++ EntitySeg 掩膜 AP 23.1 vs OpenSplat3D 18.3，ScanNet mIoU 51.90 vs 50.30。',
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
               'VLA', 'hand', 'event camera', 'light field', 'gaze']:
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
{rel_line}
{rel_note}

## 可复现性（代码/数据/硬件）
- 代码/项目页：{code}
- 全文证据：{evidence}（{level}，{chars:,} 字符）

## 行动建议
{action}
'''

os.makedirs('papers/notes', exist_ok=True)
n_notes = 0
n_skip = 0
for p in D:
    if p['grade'] == 'C':
        continue
    g = DIG[p['id']]
    m = MAN[p['id']]
    p['level'] = m['level']
    p['chars'] = m['chars']
    fn = f"papers/notes/{p['id']}__{slugify(p['title'])}.md"
    if os.path.exists(fn):
        print('skip', fn)
        n_skip += 1
        continue
    backfill = p['batch'].startswith('backfill')
    if backfill:
        up = PUB.get(p['id'], {}).get('updated', '')
        rel_line = ('- 本批为旧稿 `replace` 再公告（首发 %s，updated %s），按诚实口径单独编号为 `backfill-%s`，'
                    '**不参与当日重磅日判定**，按口径最高记 A（本批 backfill 无 S）。'
                    % (p['published'], up or '—', MMDD))
        rel_note = ('- 公告日 %s（周三）≠ 拉取日 2026-11-26（周四 02:30）；本篇首发 %s，本次以 replace 被 RSS 命中，'
                    '首发日与当期工作须区分阅读。' % (ANN, p['published']))
    else:
        rank = '，本批 Top10 第 %d 名' % (TOP10.index(p['id']) + 1) if p['id'] in TOP10 else ''
        rel_line = ('- 本批新增（batch `%s`，公告类型 `%s`），赛道「%s」%s'
                    % (p['batch'], p['announce'] or 'new', p['track'], rank))
        rel_note = ('- 公告日 %s（周三）≠ 拉取日 2026-11-26（周四 02:30）；本批为 11-25 单日公告组'
                    '（761 槽位 / 624 篇唯一），API 首次提交日 %s。' % (ANN, p['published']))
    if p.get('recall') == 'RESIDUAL_ADOPT':
        rel_note += '\n- **由第 3.5 步残差复核捞回**：摘要级 KW 与标题级扩展词均未命中，说明词表在该表述上仍有语义缺口；仍走完全流程后才入馆。'
    if p.get('note'):
        rel_note += '\n- 备注：%s' % p['note']
    rel_note += '\n- 本批 OUTDATED / SUPERSEDED 判定为 0，未发现直接取代关系。'

    action = ('- 纳入重点精读：方法与实验节可直接支撑选题与技术选型。' if p['grade'] in ('S', 'A')
              else '- 浏览级：关注问题设定与结论，方法细节按需回看。')
    _cd = (p.get('code') or '').strip()
    action += ('\n- 有公开代码/项目页，可先跑通再评估迁移成本。' if 'http' in _cd and not _cd.startswith('未')
               else '\n- 未提供代码，复现需按正文细节自行实现。')
    if p['grade'] == 'S':
        action += ('\n- 本批门③ margin %+.3f、`blockbuster=true`，按口径授 S（≥4.20 且重磅日），可作对外引用重点。'
                   % G['gate3']['margin'])
    elif p['value'] >= 4.20:
        action += '\n- 达 S 线（≥4.20）但本批 blockbuster 判定或档位口径未授 S，按 A 表述。'
    body = NOTE.format(
        id=p['id'], title=p['title'], title_zh=p['title_zh'], track=p['track'], venue=p['venue'],
        date=DATE, value=f"{p['value']:.2f}", grade=p['grade'], evidence=p['evidence'],
        IMP=p['scores']['IMP'], NOV=p['scores']['NOV'], TEC=p['scores']['TEC'], EXP=p['scores']['EXP'],
        PER=p['scores']['PER'], TRL=p['scores']['TRL'], REP=p['scores']['REP'],
        level=p['level'], batch=p['batch'], announce=p['announce'] or 'new',
        in_top10=str(p['in_top10']).lower(), published=p['published'],
        recall=p.get('recall') or 'KW', tags=', '.join(tags_for(p, g)),
        concl=CONCL[p['id']], problem=g['problem'], method=g['method'],
        exp=bullets(g['key_numbers']), nov=bullets(g['novelty']), lim=bullets(g['limitations']),
        rel_line=rel_line, rel_note=rel_note,
        code=(p.get('code') or '正文未提供'), chars=p['chars'], action=action)
    open(fn, 'w', encoding='utf-8').write(body)
    n_notes += 1
print('notes written', n_notes, 'skipped', n_skip)


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
g1, g2, g3 = G['gate1'], G['gate2'], G['gate3']

GR = {}
GRM = {}
GRB = {}
for p in D:
    GR[p['grade']] = GR.get(p['grade'], 0) + 1
for p in MAIN:
    GRM[p['grade']] = GRM.get(p['grade'], 0) + 1
for p in BF:
    GRB[p['grade']] = GRB.get(p['grade'], 0) + 1

S3 = [p for p in D if p['grade'] == 'S']
S3.sort(key=lambda r: -r['value'])

main_intro = (
    '> 当日地图：**公告日 2026-11-25（周三）≠ 拉取日 2026-11-26（周四 02:30）**——诚实口径；'
    '11-25 为单日公告组 **761 槽位 / 624 篇唯一**（cs.CV 302 / cs.GR 11 / cs.HC 21 / cs.MM 7 / '
    'cs.RO 111 / cs.AI 300 / eess.IV 9，逐分类 declared=got）；11-26 组此刻尚未公告，'
    '11-24 组已在前一批处理完毕（本批无积压窗口）。\n'
    '> 主批 XR 新稿 **%d 篇（S %d / A %d / B %d / C %d）**，Top10 实数 10 篇、最高 **%.2f**（2611.32198 MoGe-4D）。'
    'RSS 7 分类 `--no-filter` **921 条**，11-25 组覆盖率 **624/624（缺收 0）** → 免 API id_list；'
    '摘要级 KW **61** + 标题级扩展词 **36** = 候选池 **97** → 逐篇核摘要剔 **53** → **44 篇**；'
    '第 3.5 步残差复核（527 条，**1.52%%**）采纳 **8 篇**，另通读补入 3 篇（Xtream / BodyWeave / PRC4D）→ **55 篇**。\n'
    '> 全文：**63 篇 L0 / FULL**（最小 24,073 / 最大 242,491 字符；本批无 PARTIAL、无 ABSTRACT_ONLY）。\n'
    '> 覆盖度三关：门① **%.3f**（%s vs 库内 %s，阈值 0.62）/ 门② **%d 赛道**（%s，未触发重筛）/ '
    '门③ **%.2f vs %.3f**（半开窗口 [%s, %s)、按 batch 剔除 `%s`、%d 条入窗）'
    '→ **margin %+.3f，heavy_day_raw=%s，blockbuster=%s，本批授 %d 个 S**（%s）。'
    % (len(MAIN), GRM.get('S', 0), GRM.get('A', 0), GRM.get('B', 0), GRM.get('C', 0), g3['today_max'],
       g1['max_jaccard'], g1['pair'][0], g1['pair'][1], g2['n_tracks'],
       '、'.join('%s×%d' % (k, v) for k, v in g2['top10_tracks'].items()),
       g3['today_max'], g3['top10_mean'], g3['window_lo'], g3['window_hi'],
       '、'.join(g3['this_run_batches_excluded']), g3['in_window'], g3['margin'],
       g3['heavy_day_raw'], g3['blockbuster'], len(S3),
       ' / '.join('%.2f %s' % (p['value'], p['title_zh'].split('：')[0]) for p in S3))
)
moc(MAIN, f'papers/MOC/MOC-{DATE}.md',
    f'MOC · {DATE}（11-25 公告批次 · 重磅日 · {len(MAIN)} 篇）', main_intro)

bf_intro = (
    '> **非当日新提交**：本批 %d 篇均为 11-25 公告 RSS 混入的 `replace` 类旧稿再公告，**首次入馆**；'
    '首发 %s ~ %s（updated 均为 2026-11-23/24）。按诚实口径单独编号，**不参与当日重磅日判定**，'
    '即使 ≥4.20 亦记 A（本批最高 %.2f，未触及该线）。\n'
    '> 定稿 **A %d / B %d / C %d（无 S）**：%s。\n'
    '> 门① 的最大 Jaccard 对（%.3f）正是由本批 2610.11810 与库内 2611.29112 构成，仍低于 0.62 阈值。'
    % (len(BF), min(p['published'] for p in BF), max(p['published'] for p in BF),
       max(p['value'] for p in BF), GRB.get('A', 0), GRB.get('B', 0), GRB.get('C', 0),
       ' · '.join('%.2f %s' % (p['value'], p['title_zh']) for p in BF), g1['max_jaccard'])
)
moc(BF, f'papers/MOC/MOC-backfill-{MMDD}.md',
    f'MOC · backfill-{MMDD}（旧稿 replace 再公告首次入馆）', bf_intro)
print('MOC written')

# ---------- registry（按 base_id 幂等追加）----------
reg = 'papers/library/registry.jsonl'
bak = f'papers/library/registry.jsonl.bak-{DATE.replace("-", "")}'
if not os.path.exists(bak):
    shutil.copy(reg, bak)
    print('backup ->', bak)
rows = [json.loads(l) for l in open(reg, encoding='utf-8') if l.strip()]
have = {r['id'].split(':')[-1].split('v')[0] for r in rows}
added = 0
with open(reg, 'a', encoding='utf-8') as f:
    for p in D:
        if p['id'] in have:
            print('exists', p['id'])
            continue
        e = dict(id=f"arXiv:{p['id']}", title=p['title'], title_zh=p['title_zh'], track=p['track'],
                 date=DATE, value=p['value'], grade=p['grade'], scores=p['scores'], status='CURRENT',
                 evidence=p['evidence'], fetch_level=p['level'], fulltext_chars=p['chars'],
                 in_top10=p['in_top10'], batch=p['batch'], announce_type=p['announce'] or 'new',
                 published=p['published'], flags=[])
        f.write(json.dumps(e, ensure_ascii=False) + '\n')
        added += 1
total = len(rows) + added
print(f'registry +{added}（{len(rows)} -> {total}）')
print('notes', len(glob.glob('papers/notes/*.md')), 'daily', len(glob.glob('papers/daily/*')),
      'moc', len(glob.glob('papers/MOC/*.md')))
