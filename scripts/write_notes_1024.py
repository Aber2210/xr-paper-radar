# -*- coding: utf-8 -*-
"""2026-10-24：原子笔记生成（主批 17 + backfill 4）。内容来自 data/digest_1024_g*.json（全文证据）。"""
import json, os

scored = {}
for f in ('data/scored_1024.json', 'data/scored_backfill_1024.json'):
    for r in json.load(open(f, encoding='utf-8')):
        scored[r['id']] = r
digest = {}
for g in (1, 2, 3):
    for x in json.load(open(f'data/digest_1024_g{g}.json', encoding='utf-8')):
        digest[x['id']] = x

# id -> (一句话结论, 行动建议, tags)
EXTRA = {
    '2610.30293': ('NVIDIA 以 14M 三源语料统一到 SOMA-Hand 表示 + 相机感知双分支（CLIFF+RayPE），把第一视角单目 3D 手重建推到 zero-shot SOTA（H2O MPJPE 13.12mm，较 HaMeR 降约 32%；HOT3D 18.82 vs 58.00），推理 9ms/帧并以 OpenMDW 许可开源。',
                   'VLA/世界动作模型的手部监督数据生产可直接采用（HuggingFace nvidia/EgoHand-v1 + IsaacCapture）；XR 手部追踪可关注其 ViPE 相机轨迹驱动的世界坐标输出。边界：单目深度尺度歧义未解、严重遮挡仍困难、授权训练视频不公开。',
                   ['第一视角', '3D手部重建', '开源模型', 'NVIDIA']),
    '2610.30619': ('在生成式 3D 高斯头部（GSGAN）上实现统一神经辐射传输：每个高斯分配视角条件的 SH 传输系数，一次前向合成后重光照无需再评估生成器——243 FPS，比既有 3D 感知人像重光照快至少 12×，且无需 light stage 数据。',
                   '实时化身重光照（telepresence/社交 Avatar）的当前速度标杆；白光假设+线性外推解决 in-the-wild 训练的光照歧义是可迁移技巧。边界：球谐基限低频、albedo 可能残留高光、代码/权重公开状态未明。',
                   ['化身重光照', '3D高斯', 'SIGGRAPH2025', '实时渲染']),
    '2610.31299': ('首个 interaction-first 灵巧手-物交互先验：接触感知奖励训练物理专家池 → 蒸馏为目标条件 VAE → 有界潜空间残差 RL；GRAB 跟踪成功率 69.6%→93.3%，零相关数据迁移到接球（最强基线 2.0×）与双手交接（4.3×），样本效率约 10×。',
                   'VR/AR 与游戏中的物理手-物交互合成、灵巧操作策略初始化可直接复用（项目页承诺发布数据与 checkpoint）。边界：仅仿真+刚体（不含铰接物体）、仅双手、MANO 单一手模型。',
                   ['手-物交互', '物理先验', '灵巧操作', 'VR/AR动机']),
    '2610.31320': ('首个面向因果流式骨干的免训练 4D 重建模块：发现并利用 KV Cache 中隐式编码的时序运动线索（高方差-低均值）做动态分割，再以 soft key masking 抑制动态信息在历史聚合中的累积——DAVIS-all J_M 43.06（较最强流式基线 +9.86），200 帧 93.1s 近线性扩展。',
                   '长序列在线捕捉/流式重建（XR 直播、体积视频流式化）即插即用于 StreamVGGT/Stream3R 类骨干。边界：动态物体本身重建未覆盖、评测限 DAVIS/DyCheck、代码未声明。',
                   ['流式4D重建', '免训练', '动态分割', 'ACMMM2026']),
    '2610.30326': ('首个 4D 高斯指代表达分割（R4DGS）任务定义 + R4D-Bench-QA 基准（12 场景/89 查询，覆盖时序/集合/排除/零目标）；training-free ReferGaussian 以 MLLM 规划 + Grounded-SAM 2 + 迭代 Gaussian lifting 达 76.5% Acc/34.4% vIoU，超 4D LangSplat 与 Segment-then-Splat。',
                   '动态场景语言寻址（如「分割正在倒下的那个杯子」）的首个评测基线；Gaussian-to-Entity 抽象与 EntityBank 可检查性是亮点。边界：依赖底层 4DGS 与 mask 质量、拓扑剧变场景失败、基准规模有限。',
                   ['4DGS', '指代分割', '新基准', 'ACMMM2026']),
    '2610.31472': ('VecTile 用被动硅胶 nub-杠杆把三轴接触力转为四象限法向信号的差分，在单一低成本压阻架构上实现 3-DoF 力感知：法向 RMSE 0.39N/剪切 0.16N（348,800 受试点），flat 校准可直接迁移 R=85mm 弯曲安装，单价 <35 USD、3D 打印模具自制。',
                   '触觉反馈手套/机器人皮肤的低成本剪切感知方案，两个下游任务（防刺破反射 48%→88% 插拔）证明剪切通道独特价值。边界：单 taxel ~5N 以上灵敏度下降、hysteresis/漂移/耐用性未表征。',
                   ['触觉传感', '3-DoF力', '低成本', '柔性阵列']),
    '2610.30468': ('首个在活跃 CV 子领域端到端运行的自主研究系统：36 agent 六阶段管线，全部候选变自已验证复现的 splatify 插件，以真实 GPU PSNR 做 grounding-conditional Elo 排序；16 次运行全部超复现目标 +0.18~+3.78 dB，天文星云场景 +3.78 dB 为此前 3DGS 方法空白。',
                   '3DGS 研究自动化探索的样板（系统/账本/手稿全公开）；claim-to-log 绑定与 falsifier 耦合设计可迁移到其他领域。边界：单次 24-48h/约 $150-250，soundness 仍不及人类顶会论文，存论文洪水风险。',
                   ['自主科研', '3DGS', '多智能体', '全公开']),
    '2610.31293': ('RecallGS 免训练 recall-ground-fuse：用智能体观察历史（CLIP 检索 + alpha-compositing 渲染责任度几何验证）替代 EmbodiedSplat 的学习式 3D U-Net 分支，ScanNet-19 mIoU 44.41（较 fast 版 +3.38）且 2.48 FPS（约 3× 提速），接近完整模型精度。',
                   '在线语义 3DGS 的免训练替代路线，与库内 EmbodiedSplat 类学习式分支互补。边界：历史观测稀疏时收益有限、预算未 held-out 验证、代码未声明。',
                   ['在线语义3DGS', '免训练', '历史回忆', 'ScanNet']),
    '2610.31321': ('MVLoMa 首次在星图上做联合稀疏匹配：一次前向输出全部中心-邻居匹配并保留逐边得分矩阵，复用冻结几何基础模型（DA3-Giant）末层跨视图 token 作描述子，配极线几何负样本损失；四基准 AUC@1° 58.65 三档全优，25 视图匹配较顺序成对快 2.20×。',
                   'SfM/视觉定位前端的匹配原语升级（PoseLib RANSAC 接口兼容）。边界：未接入完整 SfM 系统验证、中心-邻居拓扑无邻居间交互、训练 2-8 视图外推 25 视图非单调。',
                   ['特征匹配', '多视图', 'SfM', '几何基础模型']),
    '2610.30734': ('ISMAR 2026/TVCG：首个同一剧本化依恋情境下消息/网页/VR 三种数字告别形式的受控比较（N=45）——Website 与 VR 的象征性闭合均显著高于 Messaging（19.87/20.67 vs 16.07），但 VR 相对 Website 无额外闭合优势（p=.726）而丧亲强度最高（2.16, p=.013）。',
                   '数字告别/远程纪念设计指南：参与优先、沉浸选择性使用；Agency-Amplification 机制与 PSCS-10 量表可复用。边界：形式间时长/可回访性捆绑混杂、N=45 样本小、香港粤式仪式语境外推受限。',
                   ['VR临在感', '数字告别', 'ISMAR2026', '用户研究']),
    '2610.31221': ('Joint-CI：首个统一覆盖点/物体/混合地图的分布式 RI-EKF SLAM 融合构造——经直接误差映射保留 robot-feature 相关性后用 partial-state CI 融合，理论证明保持 gauge 方向与一阶协方差一致性（NEES≈0.85）；Five-robot 场景 RMSE 优于 Local 与 Pose-CI，且指出 DInCIKFc-C 过自信（NEES 1.24, coverage 74）。',
                   '多机器人 SLAM 地图融合的一致性基准；payload 随公共特征数平方增长的度量与特征子集降载思路实用。边界：纯仿真、假设共同全局帧初始化、CI 保守。',
                   ['多机器人SLAM', '协方差交叉', '不变滤波', '代码公开']),
    '2610.31156': ('免离线校准、磁强计免的 EKF 联合估计相邻 IMU 相对定向与传感器位置（12 维状态），以 Butterworth LPF 系统处理 foot-strike 冲击与数值微分噪声；OpenSense 真实数据总体误差 2.61°（较离线校准基线 10.40° 降 75%），490 次 Monte Carlo 定量建立精度-运动强度依赖（R²=0.71/0.90）。',
                   '可穿戴人体运动捕捉（XR 身体追踪）的免校准 IMU 方案。边界：中等激励强度（1.5 m/s²）下位置-定向联合估计显著劣化、低激励阶段漂移、输出为传感器间而非解剖学关节角。',
                   ['IMU', '人体运动', '免校准', 'EKF']),
    '2610.30908': ('查询时校准已提升的 CLIP 3D 特征场：场景中心化 + 固定通用参考词表白化 + TransCLIP 软聚类/CSLS margin，无需重训练/重提升；7 种提升方法 × 4 数据集一致提升（SFS 3D-OVS mIoU 70.79→89.80，VALA 单查询 +43.82）。',
                   '开放词汇 3D 分割的即插即用后处理（LERF/LangSplat/Feature3DGS 生态通用）。边界：仅室内评测、单查询拒绝可靠性受 held-out 阈值限制、不恢复缺失几何/语义。',
                   ['开放词汇分割', 'CLIP校准', '免训练', '3D高斯']),
    '2610.30910': ('H-2DGS 三阶段把体积 3DGS 转为薄表面（可微 ray-wise density concentration → TSDF 融合 → 弯曲高度场 Gaussian），面向神经外科皮层-MRI-tractography 统一可视化：5 例 MVDC 1e-5~4e-5 显著低于 2DGS/QGS，模型恒定 7.97MB、29-42ms/帧（RTX 3050）。',
                   '3DGS 表面化表示路线（库内 2DGS/QGS 家族）的外科新应用；可微厚度目标与 curved height-field primitive 可迁移到其他有限视角表面重建。边界：光度保真度低于基线、依赖 SfM 位姿、每例固定 2400 primitive 口径不一致、代码未发布。',
                   ['3DGS表面化', '医疗可视化', '高度场', 'cross']),
    '2610.31284': ('系统性研究文本记忆 OEM-VQA 的检索策略：固定生成记忆仅隔离检索变量，Parent 检索（36 子块→12 父 caption）在 QAEgo4D-Closed 达 56.4%（3,600 tokens，全记忆的 1/3），并揭示 Hit@K↑反而可能因高置信干扰项降准确率的非单调关系。',
                   '长第一视角视频问答的检索设计参考（预算 K=12 为峰）。边界：仅选择题设置、单一描述/推理模型组合、细粒度空间细节缺失时失败、代码未提及。',
                   ['第一视角视频', '情景记忆', '检索增强', 'VQA']),
    '2610.30731': ('首次把 VR 创作的无障碍叙事同时落地为漫游视频与等价静态幻灯片并做受控比较（N=100）：漫游视频叙事投入 5.54 vs 4.24（g=2.05）、状态共情 3.15 vs 2.21（g=1.91）、支持意图变化 +1.38 vs -0.21，为「VR 共情机器」宣称提供更谨慎的实证边界。',
                   'VR 无障碍传播的低成本替代方案（录播视频）有效性证据；明确声明 screen-based 不等同沉浸式 VR。边界：非随机分组、多特征混杂、仅即时自我报告。',
                   ['VR传播', '无障碍', '共情', '用户研究']),
    '2610.30353': ('三个共看实验（N=109/116/88，OSF 预注册，ENGAGE XR + Quest 2）：20×20m 小公共边界的社会临场感最高（b=0.51, p=.025），个人空间越大社会临场感越低（b=-0.070, p=.041），并首次把群体熟悉度作为个体级变量纳入共看研究（Exp3 操作检验失败，仅相关证据）。',
                   '社交 VR 共看系统空间配置的设计准则（按熟悉度定制边界、环境设计分担空间协商）；FOV 覆盖率-社会临场感机制证据可用。边界：Exp1 维度混淆、便利样本、组大小未操纵。',
                   ['社交VR', '共看', '空间配置', '预注册']),
    '2605.22190': ('NoPo4D 首个同时满足前馈+免位姿+多视角+动态+一般场景的 4D 重建系统：velocity decomposition 用 SEA-RAFT 伪真值光流直接监督 2D 运动分量，绕开位姿依赖渲染；ExoRecon 29.15 PSNR（DGGT 20.44），post-opt 31.95 超过需位姿的 per-scene SOTA MonoFusion（30.43），快数个数量级。',
                   '免位姿动态捕捉（exocentric 多视角、无标定场景）的首选前馈方案；OOD 泛化（Immersive Light Field/Kubric/N3DV）均领先最强 FF 基线。边界：假设静态相机 rig、依赖教师模型质量、需多路时间同步视频。',
                   ['4D重建', '免位姿', '前馈', 'replace补录']),
    '2609.16684': ('MEgoVista 把单段未准备的第一视角头戴录制转为米制双手+头部运动：ego-aware 检测（佩戴者/旁观者 F1=1.00）+ calibrated stereo 度量标尺（尺度偏差 |s-1| 低至 0.0048），26 相机光学动捕协议审计下手指 PA-MPJPE-p 4.29mm（较 HaWoR 降 70%）、头部 ATE 0.65-2.87mm（DROID-W 尺度失败 18/22 episodes）。',
                   '野外 egocentric 米制 4D 手-头标注的系统级方案，Maniformer 技术报告 001；协议审计（拒测计费+参考自审）方法值得借鉴。边界：3 场景离线 proof-of-concept、每 episode 206s、依赖专用 MEgo View 硬件。',
                   ['第一视角', '4D手-头', '度量标尺', 'replace补录']),
    '2601.14895': ('SpatialMem 从随手拍摄 egocentric RGB 构建层级米制空间记忆树：可插拔几何后端（VGGT/SLAM3R/COLMAP）+ 地平面直立对齐 + 墙/门/窗结构锚 + 开放词汇物体节点，Scene 1 物体检索 SR 0.83、关系准确率 0.84、StepComp 0.89，查询沿图走短链低延迟。',
                   'AR 助手/移动机器人的持久空间记忆接口（memory-centric，米制 3D 作为索引 scaffold 而非建图目标）；与库内 AR Office Recall 同类。边界：3 场景离线验证、杂乱场景细粒度识别下降、左右关系依赖视角局部标签。',
                   ['空间记忆', '语言grounding', 'AR助手', 'replace补录']),
    '2508.15169': ('MeSS 城市 mesh 引导的跨视角一致扩散场景生成：级联反向 outpainting ControlNet（warp+前帧条件抑制长程漂移）+ 关键帧 flattened surfels 免优化落面 + AGInpaint/GCAlign；后退 100m 外推 3200 图 LPIPS 0.348/FID 28.17/KID 0.0161 全面优于 StreetScapes/CityDreamer4D。',
                   'VR 城市导航/数字孪生的纹理生成路线（UE5 City Sample 可复现）。边界：缺公开城市 mesh 数据集、SD1.5 基座限分辨率、GCAlign 以轻微模糊换一致性、无代码。',
                   ['场景生成', '城市网格', '扩散模型', 'replace补录']),
}

def slug(title_zh):
    import re
    s = re.sub(r'[《》：:，。、（）()「」\[\]/,.;:!?\'"|—-]+', '-', title_zh)
    s = re.sub(r'-+', '-', s).strip('-')
    return s[:40]

os.makedirs('papers/notes', exist_ok=True)
n = 0
for pid, r in sorted(scored.items()):
    d = digest[pid]
    oneline, action, tags = EXTRA[pid]
    s = r['scores']
    fname = f"{pid}__{slug(d['title_zh'])}.md"
    bf = r.get('batch') == 'backfill-1024' or r.get('in_top10') is not None and pid in ('2605.22190', '2609.16684', '2601.14895', '2508.15169')
    body = []
    body.append('---')
    body.append(f"id: arXiv:{pid}")
    body.append(f"title: {d['title']}")
    body.append(f"title_zh: {d['title_zh']}")
    body.append(f"track: {r['track']}")
    body.append(f"venue: {d['venue']}")
    body.append(f"date: 2026-10-23")
    body.append(f"value: {r['value']:.2f}")
    body.append(f"grade: {r['grade']}")
    body.append(f"evidence: {r['evidence']}")
    body.append(f"status: CURRENT")
    body.append(f"superseded_by: []")
    body.append(f"scores: {{IMP:{s['IMP']}, NOV:{s['NOV']}, TEC:{s['TEC']}, EXP:{s['EXP']}, PER:{s['PER']}, TRL:{s['TRL']}, REP:{s['REP']}}}")
    body.append(f"fetch_level: {r['fetch_level']}")
    body.append(f"batch: {r.get('batch', '2026-10-24') if not bf else 'backfill-1024'}")
    body.append(f"announce_type: {r['announce_type']}")
    body.append(f"in_top10: {str(r['in_top10']).lower()}")
    body.append(f"tags: [{', '.join(tags)}]")
    body.append('---')
    body.append('')
    body.append(f"# {d['title_zh']}")
    body.append('')
    if bf:
        body.append(f"> **backfill-1024**：旧稿（{r['announce_type']} 再公告，首次入馆），公告日 2026-10-23，非 10-24 当日新提交。")
        body.append('')
    body.append('## 一句话结论')
    body.append(oneline)
    body.append('')
    body.append('## 要解决的问题')
    body.append(d['problem'])
    body.append('')
    body.append('## 方法详解')
    body.append(d['method'])
    body.append('')
    body.append('## 实验与结果')
    body.append(d['experiments'])
    body.append('')
    body.append('## 创新点与贡献')
    for i, x in enumerate(d['innovation'], 1):
        body.append(f"{i}. {x}")
    body.append('')
    body.append('## 局限与风险')
    for x in d['limits']:
        body.append(f"- {x}")
    body.append('')
    body.append('## 与文献库的关系')
    body.append(d['relation'])
    body.append('')
    body.append('## 可复现性')
    body.append(d['repro'])
    body.append('')
    body.append('## 行动建议')
    body.append(action)
    body.append('')
    open(f'papers/notes/{fname}', 'w', encoding='utf-8').write('\n'.join(body))
    n += 1
print('notes written:', n)
