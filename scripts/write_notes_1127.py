# -*- coding: utf-8 -*-
"""2026-11-27 产物：原子笔记 / 当日 MOC / backfill MOC / registry 幂等追加。

口径要点（不可改写）：
- 公告日 2026-11-26（周四）≠ 拉取日 2026-11-27（周五 02:30）；11-27 组尚未公告。
- 主批 55（43 新 + 12 残差采纳）+ backfill 8 = 63；A44 / B14 / C5，无 S。
- 门③ margin −0.109、blockbuster=false → 本批不授 S；4.35/4.35/4.20 等 3 篇达 S 线按校准关记 A。
- C 级 5 篇仅入馆，不写笔记。
- 2611.30173 为库内 cross 再公告（11-25 批 3.71），已剔除，不入馆。
"""
import glob
import json
import os
import re
import shutil

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
os.chdir(ROOT)
DATE, MMDD = '2026-11-27', '1127'
ANN = '2026-11-26'

D = json.load(open('data/scored_%s.json' % MMDD, encoding='utf-8'))
G = json.load(open('data/gates_%s.json' % MMDD, encoding='utf-8'))
MAN = json.load(open('data/fulltext/_manifest.json', encoding='utf-8'))
PUB = json.load(open('data/published_%s.json' % MMDD, encoding='utf-8'))
TOP10 = G['top10']
DROP_OPS = {x['drop']: x for x in G['gate2'].get('rescreen_ops', [])}
ADD_OPS = {x['add']: x for x in G['gate2'].get('rescreen_ops', [])}

DIG = {}
for k in range(1, 9):
    for r in json.load(open('data/digest_%s_g%d.json' % (MMDD, k), encoding='utf-8')):
        DIG[r['id']] = r
assert len(DIG) == 64, len(DIG)   # 含 1 篇已剔除的 cross 再公告（2611.30173），不参与产物
assert len(D) == 63, len(D)
assert not [p['id'] for p in D if p['id'] not in DIG]

CONCL = {
 # ---- Top10 ----
 '2611.34480': '把「用哪种变换把前馈稠密几何对齐到 VIO 稀疏锚点」从设计选择变成可推导结论：证明标定后与内参相容的变换恰为 Sim(3) 与无穷远平面 3 自由度的 10 维浸入子流形（多出的模式在图像中不可见），并把沿射线锚点协方差、可观测性门控与可认证相似同步放进同一个 EM——EuRoC F1 53.99% / CD 0.065 m，Oxford Spires 60.74% 比 Sim(3) 高 9.8 点，四数据集平均 F1 提升 4.1–9.8 点，ATE 0.084 m。',
 '2611.34944': '用锚物体的 3D 高斯沿目标轨迹渲染出的图当相机信号，替换参数化位姿与几何 warp，一次拿到尺度感知、视角完备、相对物体三个性质——CO3D PSNR 14.08、anchor IoU 0.814（GEN3C 0.346、FID 74.8→56.0），417 帧长视频旋转误差 10.94° vs 27.93°，流式 3.63 FPS。',
 '2611.34489': '把「佩戴者就在相机所在处」这一几何事实变成识别读出：冻结 VGGT-Ω 一次前向取相对位姿，用候选 mask 反投影射线与对极方向的角偏移加相机距离排序，替代外观匹配——FindEgo-1M 1.16M 对 / 12 类佩戴者，最难未见类 71.1 vs 最强 3D 模型 42.1，比 GPT-6 Astra 高 31.6 点，0.4 s/条 vs 3.0–22.4 s。',
 '2611.33650': '把 LLM 的混合架构搬到流式 3D 几何：3/4 层换 Mamba2（等价于权重随距离指数衰减的因果线性注意力），余下每 4 层用 register token 做「先选帧、再选 token」两级稀疏注意力，配三阶段蒸馏——单帧 27 ms 基本恒定、7-Scenes Acc 0.066（StreamVGGT 0.129）、KITTI AbsRel 0.093（0.173），训练仅教师 9% GPU 小时。',
 '2611.33760': '把「同一状态、同一指令、同一目标」在原生截图与穿戴相机实拍间配对，使观测方式成为唯一变量，再用 Resized/Warped/Rectified 三级把落差归因到像素来源——536 状态 / 3,250 任务 / 8,576 张物理图，十个开源模型均值 94.8%→48.5%，像素来源落差 29.2–31.7 点远大于呈现方式 14.7–17.1 点，PairDistill+ReGround 回到 69.62%。',
 '2611.34476': '把「固定解码器预算如何在源视图间分配」显式建成目标相机的函数：逐视图渐进 Carrier 层级支持任意整数配额，冻结骨干只训轻量 Carrier——120 源视图有效帧率 9.23×（LagerNVS）/ 64×（LVSM），DL3DV PSNR 27.34 vs ZPressor 24.16，显存 −67%，解码 32 ms vs 227–334 ms。',
 '2611.34128': '把 pointmap 的离散点接到连续射线场：query-view 投票选视角 + 粗射线表面回归 + 精化，无位姿输入直接出连续表面——ScanNet++ ADE 0.132 m（PriorDA 0.198、RayletDF 0.179），Tanks&Temples 1.233 m（3.970），5 视角 0.370 m（0.635），9 训练集 / 6 未见测试集。',
 '2611.34223': '把 4D 高斯从「只能对协方差条件化」解放出来：改为对协方差平方根条件化、用 7×3 QR 得到不显式构造协方差的 Cholesky 因子，从而在原生鱼眼/超广角上做 ray-based UT 渲染、不必先去畸变——170° 鱼眼保留 150° 视场时 +8.05 dB，Dynopsis 32.60 vs EWA 26.85，离轴 60–80° 领先 6.2 dB，步成本仅 1.06–1.13×。',
 '2611.34939': '给每个高斯一组高斯过程式时序运动核，使它在整段时间内始终是合法表面元并携带隐式几何，于是任意时刻可直接抽网格、不必事后 TSDF——Blender-Moments 联合 F-score 0.556（D-2DGS 0.365、4DGS 0.283），法向 Chamfer 24.6°（34.6°），训练 18 min（33 / 142 min），同一模型换 TSDF 只剩 0.468。',
 '2611.33467': '把世界模型的状态直接定义为 N 个显式高斯：tokenizer 用固定 query 把上下文视图解成高斯、diffusion forcing 预测其演化，任意相机由可微光栅化渲染——OGBench 新视角 PSNR 23.37、端到端 83.9 FPS（比视频世界模型快 12×、高 2.0 dB），LIBERO 92.3%（1B）对 WorldVLA 79.1%（7B），2K 高斯 AbsRel 0.055。',
 '2611.34932': '把一次公制 3DGS 扫描变成稠密功能参考记忆，并用位姿检索替代外观检索，从机制上绕开重复走廊 / 相同门的视觉混叠——真实 MoCap 数据 recall@5cm/5° 0.864、RMSE 8.2 cm（VPR 基线 0.830 / 17.9 cm，−54.2%），人群 4→24 时五个后端中四个掉点 ≤7，Jetson Orin NX 上 5 Hz 完成 30 m 走廊导航，检索 4 ms vs 40 ms。',
 # ---- 主批其余（Top10 之外）----
 '2611.34022': '用 joint-name embedding（CLIP 编码关节解剖名与侧别）把 motion 与 skeleton 两类语料统一进一个 ViT 掩码自编码器，使理解与生成共用同一表示——1.47M clips / 2,175 h；NTU-60 X-View 线性 94.0%、仅 1% 标注 77.0%；文生动作 FID 32.19→28.36、RoMo 15.35→9.68。',
 '2611.34079': '在几何-外观共享 latent 上做条件流匹配，条件分两路（可训 scene encoder 聚全局 token + 冻结 DepthAnything v3 保住单参考细粒度），把低重叠散乱参考生成连贯世界——RE10K 2-view PSNR 20.88（SEVA 18.47），长序列 17.68（GLD 16.43）、ATE 0.657（GAE 1.508）、δ1 71.0（59.4）。',
 '2611.34226': '预计算「几何光交换」而不是「光照响应」，把反射率与光源构型解耦，使编辑回路里只需一次廉价传输求解——Kitchen 35.95 dB / 0.244 s（EAG-PT 28.08 / 147.2 s），Living room +10.74 dB，八个重打光条件平均 +5 dB、延迟降三个数量级。',
 '2611.34730': '把「材质行为」与「接触响应」解耦：材质条件生成 + 推理期控制器/生成器交替，并用速度增量 Δv=J/m 统一所有推力交互——Physics-IQ 63.0（Goal Force 48.0）、ST-IoU 0.701（0.280），真实图像推动成功率 90%（StreamForce 67%）、方向误差 5.2°（10.1°），4 步因果学生 8 fps。',
 '2611.34940': '把头像拆成「可动画三维本征高斯代理 + 因果自回归神经着色器」：UV 流形上每个高斯带法向 / base color / roughness，少步自回归替代多步扩散——VFHQ PSNR 21.32（LCVD 14.75）、CSIM 0.739（0.506），12.46 FPS（优化后 20.31），着色 4.19 s vs 556.51 s（132.8×），982 帧长序列仅降 0.27 dB。',
 '2611.33374': '用「GOP 版本字典 + 每帧激活索引」替代光滑形变函数，运动估计只用于引导版本构建，播放退化为标准光栅化——DanceNet3D 前景 25.70 dB（TAD-GS 22.36），高运动帧仅降 <0.3 dB（基线 1.1–4.0 dB），存储 0.060 vs 0.962 MB/帧（6×），596 FPS、手机浏览器 61–76 FPS。',
 '2611.34549': '把「找到同一地点」与「匹配上哪些模态可以改图」拆开：9 维线索导出位姿/几何/外观/记忆四种置信度做权限加权，颜色不可信时仍可用深度贡献几何——区域排序 AUROC 0.951–0.970（外观检索 0.710–0.894），误关联 <0.5%，八种退化下 PSNR 损失 2.66→1.05 dB，12 段 iPhone 扫描全部跟踪成功、ATE 6.98 cm、p95 < 33.3 ms。',
 '2611.34608': '免训练稀疏化全局注意力：用跨层一致性（历史层区域概率预估 + value 聚类局部精修）同时省掉重算概率与冗余 value——VGGT 1000 帧 AUC@3 10.94 vs 稠密 10.78、5.26× 加速，VGGT-Ω 显存 42.33 vs 62.58 GiB、4.47×；π³ 1000 帧 25.92 vs 28.82（略降），128 视图下 2.69 s vs 7.97 s 且精度更高。',
 '2611.34931': '把运动模型从「共享基轨迹 + 混合权重」改成「每点只跟随 K 个 SE(3) 之一」，背景即相机自身运动那一族，多体分解因每块秩 ≤4 可闭式求解、无需掩码——iPhone PSNR 18.05（SoM 16.72）、EPE 0.058 m（0.082）、ARI 0.775（MoSE3 0.743）；消融显示只做一次 k-means 分组就损失 1.23 dB 与 0.288 mIoU。',
 '2611.33382': '按部件分别导出闭合三角网格并联合推断关节，不需部件掩码与关节标注——Articulate-100 全 100 物体轴角 7.78°（ArtGS 11.02°）、轴位置 0.18（0.90）、CD-s 20.40 mm（22.72），部件网格开边界边 0.00%（TSDF 9.12%），四部件档 8.16° vs 17.47°。',
 '2611.34224': '把运动学 / 接触 / 力统一到 MANO 网格面（逐顶点法向力 + 接触标签，按七区聚合），视觉给场景上下文、腕部 sEMG 给发力——MPJPE 3.26 mm（HBridge 5.42，−39.8%）、区域力 MAE 0.86 N（−18.5%），跨场次 5.35（10.69）、跨被试 7.84（14.41），数据集 33,989 trials / 50 人 / 53.3 h。',
 '2611.33824': '用 4K 60fps 手机自然「把玩」重建手持物体：手部实例分割后只在物体像素上跑 SfM，再按固定角位移分段跑子序列 SfM，用多对跨序列帧的 Umeyama 拼接——ToysRU F1 93.80、CD 0.74、0.5 h（Color-NeuS 81.75 / 2.24 / 12 h），VGGT 直出仅 19.74、MASt3R-SfM 23.06。',
 '2611.34005': '把单目世界坐标 HMR 的「整段一个尺度」换成时变尺度标定：用脚点-地平面交距给逐关键帧尺度观测，再用一致性运动精化——EMDB-2 W-MPJPE 154.3 mm（DuoMo 171.6）、WA-MPJPE −15.2%，SLOPER4D 446.8 vs GVHMR 959.1 mm（−53.4%）；改回常数尺度即退化到 708.1 mm。',
 '2611.34461': '把 9-DoF 位姿条件拆成绝对（CNOCS 图序列注入）+ 相对（VPRoPE 把帧间位姿写进 RoPE）两路，统一 T2I 与 T2V 的朝向可控性——T2I Rot.Err 0.24（3D BBox 1.10），T2V US_mot 8.1（去相对编码 6.2），新增 16,561 图 / 31,540 视频，40 人主观评测。',
 '2611.34466': '把第一视角 computer-use 从「一次性给全视频」改成在线流式：观测 / 需求 / 站点状态三流异步演化 + 三类信息更新机制——693 任务 / 74 h，Online 63.4% 比 Computer-Use 86.1% 低 26.3 点而 token 少 16.4–38.0%，最强模型 87.0%，93 个组合任务上 77.4% vs 40.9%。',
 '2611.34810': '从单张全景扩出四个方向的新观察中心：覆盖度引导选视点（未见区像素数打分 + 90° 象限方位分配）+ 四视点联合去噪——UE 基准 PSNR 20.16（Matrix-3D 17.30）、AUC@3° 49.79（29.38）、F@5cm 29.02（20.32），零样本 RealSee3D 18.06 / 41.44，最高 8.6× 加速。',
 '2611.34680': '把冻结视频模型当黑盒渲染后端：离线按 34 个语义控制维度分层探测能力、在线把每条要求编译到可靠的控制通道（提示 / 参考图 / 首帧 / 代理视频）——VComBench 要求满足率 Wan 46.8→52.3%、H3 66.5→69.3%，联合成功 8.4→11.8%，380 任务 / 1,617 条计分要求。',
 '2611.33511': '把「哪个部件」与「哪个开合度」放进同一坐标：三角形场带部件身份场与 typed screw joint 状态，语言查询可直接落到关节位移——Articulate-100 轴角 3.30°（ArtLang 4.85°）、运动误差 0.35（2.32）、可动部件 CD 14.64 mm（151.36），状态检索 0.975（去状态条件 0.141），自由查询 64.2%。',
 '2611.34108': '把 3D 显著性重新定义为 image detectability（2D 检测器响应在可见视角上的聚合），只输入点云、任意 3D 位置可查询——物体 hit rate K=32 43.6%（Harris-3D 31.0）、K=8 61.3%（36.4），真实室内定位 59.7%（52.3），换成未见 2D 检测器 D2-Net 仍 38.5% vs 30.3%。',
 '2611.33796': '在 FastGS 上按训练日程削减固定开销：tile 剔除阈值随训练收敛、损失按 batch 摊销、kernel 启动合并——13 场景均值 80 s（FastGS 172 s，2.15×）且 PSNR 27.38（27.31），DL3DV 141.8→63.3 s，与 Taming-3DGS 组合 345→125 s（2.76×）。',
 '2611.33387': '放弃像素级对应，改用「物体间三维关系只差一个尺度」做跨视角对齐（Pearson 相关 + VLM 命名身份）——EgoHumans 44.5 ms（VisualSync 122.1）、CMU Panoptic 11.1 ms（112.6）、3D-POP 1.7 ms（114.7）；线索消融 333.1→44.5 ms。',
 '2611.33591': '给长时程视频一个组合式几何记忆（点云背景 + 生成网格前景 + mesh-seeded 连通域过滤），把相机误差限制在局部 chunk——单 chunk PSNR 21.24（Lyra 2.0 20.01），1,000 帧 13.92（12.85）、相机评分 79.51（65.09），RotErr −23.4%、TransErr −38.8%。',
 '2611.33655': '用 oracle 实验证伪「窗口间配准漂移」假说（换 GT 位姿 EPE 1.568 vs 1.569 无差别），把长视频 4D 跟踪的瓶颈定位为「遗忘」，改用持久世界状态 + 存储坐标判可见性——PointOdyssey EPE 1.569→1.168，1,000 帧 0.889（−43%），2,000 帧 4.634 且快 7.6×、显存 < 25 GiB。',
 '2611.33779': '把 6-DoF 相机指令逐帧画进画面（中心 + 三轴端点投影、按对数深度取灰度）做 action flow，使每一帧都能精确控相机——Sekai-game FVD 65.99（Captain Safari 69.83）、AUC@30 0.5719（0.5003）、AUC@15 0.3747（0.3088），真实域 FVD 191.77（231.67）、LPIPS −21.6%。',
 '2611.33565': '把手表 / 眼镜的扬声器-麦克风变成短程 FMCW 声呐，补上「相机看不到手」的那 53% 窗口——15 人 / 11.4 h / 4,019 条标注，已见被试 verb top-5 70.7→76.5，新被试 58.7→68.9（+10.3，外中心相机反而 −6.5），仅手表无相机无 IMU 也有 65.2 / 62.8。',
 '2611.33588': '端到端 3D 手语生成但不走 STE：用 reconstruction-aware generation 把「候选 token 替换后局部重建误差」当生成奖励，使生成目标与重建质量对齐——CSL-Daily DTW-JPE 10.86（MaDiS 11.93）、R@1 41.84（38.61），How2Sign 10.93（12.59），聋人专业手语者评分 7.20（6.13）。',
 '2611.34945': '用「手抓住并移动物体」当隐式参与信号、用一个召唤动作选输入模态，把任意日常物体即时变成 TUI，全程只跑头显 passthrough——参与分类 Acc 0.921 / F1 0.918、单 clip 5.6 ms、Quest 3 + 笔记本 42 FPS，Summon 跨人 top-1 0.809→个性化 0.975，NASA-TLX 体力负荷 40 vs 81。',
 '2611.33462': '把表面（平面高斯 surfel）与介质（Voronoi cell 分片吸收/散射）彻底解耦，并把两类事件按距离合并成光路段序列——SeaThru-NeRF 分离分数 0.901（Plenodium 0.505、SeaSplat 0.545）、PSNR 30.75、120 FPS，硬雾 16.81（WaterSplatting 15.46），训练 28.7 min。',
 '2611.34319': '以 MeshFlow 为基座、用「艺术家网格奖励」做自举偏好优化（只训 LoRA），把四边形 / 边环结构从奖励里学出来——Quad strip 0.804（MeshFlow 0.466、MeshAnything 0.756）、CD 2.697（2.760）、缺陷面 0.121（0.206），并保持 2 s 级并行生成。',
 '2611.34347': '把社会具身拆成 Attention→Intention→Reaction→Interaction 四层、共用同一片段与四个时间锚点的在线链——8,000 题 / 357 片段 / 10.91 h，最强模型总分 0.726（Attention 0.936）但 Intention 仅 0.569、IAS 上限 0.237，暴露「看得懂」与「做得对」之间的断层。',
 '2611.33728': '在可被独立重开的 Blender 工程上把几何、运动、关系分开记分，并用 30 对共享参考/目标/评分卡的 partial-asset 控制资产变量——114 条件，full-asset 视频均值 Sol 13.00 / Astra 21.79，两者 6.50 分差中 5.15 来自 relations，dynamics 满分的任务里 relations 全零达 3/14 与 8/14。',
 '2611.34414': '把「语义标签 + 显式 3D 数值」绑成可序列化代理（带标签 OBB 的 JSON + bbox.blend）作为编码智能体的 3D-native 输入，无需编码器与微调——Codex 场景 Chamfer 7.8→3.2、难物体 5.6→2.5，三智能体平均改善 47%，535 份回答中 67.5% 偏好带代理的版本，成本几乎不变。',
 '2611.33465': '用相对深度与外观尺寸两路证据投票解手部前后序歧义，再以序数残差驱动高斯化身的手部精化——腕序 balanced accuracy 48.9→76.9%（准确率 32.9→77.3%），代价仅 +0.39 px 与 +1.6°，interaction crop PSNR 16.91→17.35，365 个重叠手帧人工标注。',
 '2611.34027': '承认「身体动作不能唯一确定手」，用「手别-时间分配的文本 + 每手共享条件变分潜变量」建模 p(H|B,T,A)——OakInk2 MinMPJPE 22.809 mm（MLD 25.725）、腕旋转 16.93°（18.98°）、FHD 0.276（1.226），150 帧 2.83 s，多样性接近 GT（9.043 vs 9.397）。',
 '2611.33698': '给 LM-RS 补齐三阶 SH、场景分布化视角采样与 tile 分组多视累积，让二阶优化真正压过 Adam——Mip-NeRF 360 13 场景 PSNR 25.800 / 198.1 s（LM-RS 25.632 / 492.9 s、3DGS-Adam 25.698 / 457.5 s），checkpoint 微调 27.91 / 177.9 s，300 步 23.742 / 113.9 s。',
 '2611.33731': '把机器人任务库直接当 VR 游戏内容、整套 MuJoCo 与评测编译进 Quest 原生库，让「玩」成为采集——130 LIBERO + 4 SO101、21 人、2,141 条 episode；仅 VR（约 20 条/任务）达 69.6% / 68.2%，为全标准臂的 91% / 93%，等更新数下 65.3% vs 25% 标准数据 54.8%。',
 '2611.33735': '把 AI 眼镜请求路由写成带质量约束的成本优化，三级级联按「能处理该请求的最省资源层」匹配——真实请求里 > 30% 是设备控制类，9.6% 端侧直接消化、21.7% 回流手机（中位 43 ms / P99 74 ms），SuperGlasses TTFT −13% / E2E −7.2% / token −14.8%（准确率 45.46→42.49）。',
 '2611.33819': '把生成过程按尺度与尺度内位置索引，为每个尺度单独建语义 / 动作双记忆库，使跨样本模式可复用且与已生成历史一致——HumanML3D+MotionHiFlow R@1 0.572（0.563）、FID 0.025（0.032）；KIT-ML 上 R@1 明显提升但配 MoScale 时 FID 反而退化（0.455 vs 0.173），说明记忆收益对解码器敏感。',
 '2611.34155': '把「介质建模」与「稀疏视角补全」接在一起：用带参考路由与介质描述子的单步修复器在渲染图上学水下外观，再蒸馏回高斯——NUSR 5 视角 PSNR 23.23 / FID 25.81（SeaSplat 23.14 / 39.11），3 视角 20.67（20.27），SeaThru-NeRF 3 视角 19.86（19.82）。',
 '2611.33581': '把 VRU→AV 的主动表达与「请求是否被接受」的回执补进闭环：六种 AR 反馈 + 五条语音指令 + 九种手势，用 HoloLens 2 与车载端做原型——N=124 问卷中方向箭头清晰度 5.73、Stop 手势首选 42.7%，语音-手势语义配对 84.9%，车-人 AR 反馈 81.53 ms。',
 '2611.33826': '把预训练生成器里选定的残差分支重解释为局部向量场、用中点 RK2 积分替代单步更新，从而改变「每次预测前条件隐表示如何形成」——MoScale Top-1 0.535→0.548、MM-Dist 2.836→2.795，但 FID 0.048→0.092；仅 BAMM 的 FID 同时改善（0.052→0.051）。',
 '2611.34141': '对两段式原生 3D 管线做「引导蒸馏 + 少步一致性」的联合少步化，并保留参考图保真——端到端 437.7→74.5 s（5.87×，相对未优化教师 7.74×），Chamfer 15.2（教师 15.7、DMD 29.1），F@0.01 0.583（0.575），silhouette IoU 0.837（0.839）。',
 '2611.34062': '先把辐射场抽成固定网格、再把外观挂到顶点（diffuse 可优化 + specular 固定）并只在表面邻域传播风格，避开体渲染 alpha 混合导致的风格溢出——NeRF-Synthetic GCC Lego 0.017（ARF 0.029、Ref-NPR 0.021）、Chair 0.010（0.027 / 0.015），LLFF 多数场景 0.004–0.009。',
 '2611.33313': '在 HbbTV 合规端到端平台上用 MPEG-V 元数据驱动多感官设备、并与播放时间轴同步，给出可复现的混合分发原型——106 名不同背景参与者主观评测；仅摘要级证据（PARTIAL），未给同步误差、设备清单与渲染管线，故按 C 级仅入馆、不写笔记。',
 # ---- backfill ----
 '2611.31822': '把世界动作模型的长上下文做成预训练期的一等能力（可变长多 chunk 自回归 + chunk-causal attention），并用双专家把语言条件逐层注入共享的 vision/action expert——五个仿真基准均值 70.8（OpenWAM 43.9、π0.5 33.9），RMBench 86.2%（单帧基线 < 12%），LIBERO-Plus 92.5%，零样本真机抓放 48% / 54%。',
 '2602.00671': '在最新解码的高斯上建层次化点式 latent（3 尺度、每尺度 16 通道），配网络参数压缩做流式动态 3DGS 编码——N3DV 32.36 dB / 39 KB 每帧（iFVC-h 32.35 / 99 KB、4DGC 31.58 / 500 KB、3DGStream 31.69 / 7780 KB），BD-BR 相对 iFVC 平均 −67.8%。',
 '2605.16582': '用部件感知三角网格场 + 运动一致动力学，从两个关节状态重建铰接物体并直接给出带部件边界的网格——Articulate-100（给 GT 掩码）轴角 3.49°、CD-m 15.01 mm（最强基线 57.45 / 58.66，改善 +42.44 mm），6+ 部件档轴角 6.90°（GaussianArt 33.05°）。',
 '2606.11390': '把多卡拼成统一虚拟地址空间（kDGX dispatch + stream-ordered 异步 UM 分配器），让分布发生在算子内部而非切模型——Gettysburg 268M splats / 153 张 7088×5314 / 13 km² / 8×A100 用 3.086 h 达 PSNR 27.450，十亿级 splats 超 Grendel-GS 最大规模 25 倍，$B=N$ 平均加速 3.15×。',
 '2605.05876': '用无结构 oriented surfel（切向量编码朝向、刻意不设可学习不透明度）+ T-matrix 光栅化做逆渲染，绕开网格拓扑与体渲染的 alpha 混合语义——Stanford-ORB 新视角 PSNR-H 31.73 / PSNR-L 40.73（RTR-GS 30.10 / 39.17、NVDiffRec 21.94 / 28.44），重打光 23.22 / 30.44。',
 '2611.26380': '把第一视角描述拆成 video-level overview + 带起止时间的有序 steps 两层，并造 50,000 条 coarse-to-fine 训练样本——PhysCapBench 78.84（主干 51.24，+27.6，超过 Gemini 3.1 Pro 75.06），EgoTempo 38.40（21.60），EgoHome 步分割 PSJ 75.51（46.90）。',
 '2608.29269': '把几何与 PBR 材质跨状态共享、状态间只差物体刚体变换与光照，用 2D 高斯 surfel + 光线追踪做多扫描融合——新状态重打光 PSNR 25.89 / SSIM 0.873（比最强基线 IRGS 高 6.01 dB），真实场景 24.35 dB（ReCap +1.55）但 SSIM 略低（0.821 vs 0.903）。',
 '2509.16476': '把实测注视投影成注意图、按 gaze mass 取最小前缀包围盒做中央凹裁剪，training-free 地给 VLM 分配算力——Qwen2.5-VL-3B 匹配率 73.54→82.03%、视觉 token 15.55k→2.46k（−84.2%）、延迟 3.20→0.45 s（7.1×）；Qwen3-VL-8B 80.78→83.70%、11.6×。',
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
                    '**不参与当日重磅日判定**，按口径最高记 A（本批 backfill 最高 4.43，达 S 线仍记 A）。'
                    % (p['published'], up or '—', MMDD))
        rel_note = ('- 公告日 %s（周四）≠ 拉取日 2026-11-27（周五 02:30）；本篇首发 %s，本次以 replace 被 RSS 命中，'
                    '首发日与当期工作须区分阅读。' % (ANN, p['published']))
    else:
        rank = '，本批 Top10 第 %d 名' % (TOP10.index(p['id']) + 1) if p['id'] in TOP10 else ''
        rel_line = ('- 本批新增（batch `%s`，公告类型 `%s`），赛道「%s」%s'
                    % (p['batch'], p['announce'] or 'new', p['track'], rank))
        rel_note = ('- 公告日 %s（周四）≠ 拉取日 2026-11-27（周五 02:30）；本批为 11-26 单日公告组'
                    '（695 槽位 / 569 篇唯一），API 首次提交日 %s。' % (ANN, p['published']))
    if p.get('recall') == 'RESIDUAL_ADOPT':
        rel_note += '\n- **由第 3.5 步残差复核捞回**：摘要级 KW 与标题级扩展词均未命中，说明词表在该表述上仍有语义缺口；仍走完全流程（全文抓取→评分）后才入馆。'
    if p['id'] in ADD_OPS:
        rel_note += ('\n- **门② 回补进入 Top10**：纯值排序下 Top10 只覆盖 4 赛道，本篇（%s，%.2f）作为「%s」赛道最高分被回补。'
                     % (p['id'], p['value'], p['track']))
    if p['id'] in DROP_OPS:
        rel_note += ('\n- **门② 回补让出 Top10 名额**：纯值排序下「%s」占 5 席，本篇（%.2f）为该赛道最低分被剔出 Top10，'
                     '仍完整入馆、写笔记并保留 %s 档位。' % (p['track'], p['value'], p['grade']))
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
        action += ('\n- 达 S 线（≥4.20）但本批 `blockbuster=false`（margin %+.3f < 0.05），按校准关记 A。'
                   % G['gate3']['margin'])
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
    '> 当日地图：**公告日 2026-11-26（周四）≠ 拉取日 2026-11-27（周五 02:30）**——诚实口径；'
    '11-26 为单日公告组 **695 槽位 / 569 篇唯一**（cs.CV 288 / cs.GR 10 / cs.HC 20 / cs.MM 7 / '
    'cs.RO 109 / cs.AI 248 / eess.IV 13，逐分类 declared=got）；11-27 组此刻尚未公告，'
    '11-25 组已在前一批处理完毕（本批无积压窗口）。\n'
    '> 主批 XR **%d 篇（S %d / A %d / B %d / C %d）**，Top10 实数 10 篇、最高 **%.2f**（2611.34480 ProManO / 2611.34944 AnyCam 并列）。'
    'RSS 7 分类 `--no-filter` **849 条**，11-26 组覆盖率 **569/569（缺收 0）** → 免 API id_list；'
    '摘要级 KW **67** + 标题级扩展词 **25** = 候选池 **92** → 逐篇核摘要剔 **49** → **43 篇**；'
    '第 3.5 步残差复核（525 条，**5.71%%**，显著高于近批 1.5–2.8%%）采纳 **12 篇** → **55 篇**。'
    '另剔除 1 篇库内 cross 再公告（2611.30173，11-25 批已以 3.71 入馆）。\n'
    '> 全文：**62 篇 L0 / FULL + 1 篇 L1 / PARTIAL**（2611.33313 ar5iv 仅摘要落地页，C 级仅入馆不解读）。\n'
    '> 覆盖度三关：门① **%.3f**（%s vs 库内 %s，阈值 0.62）/ 门② **%d 赛道**（纯值 %s → 回补 %s）/ '
    '门③ **%.2f vs %.3f**（半开窗口 [%s, %s)、按 batch 剔除 `%s`、%d 条入窗）'
    '→ **margin %+.3f，heavy_day_raw=%s，blockbuster=%s，本批授 %d 个 S**（4.35/4.35/4.20 达 S 线按校准关记 A）。'
    % (len(MAIN), GRM.get('S', 0), GRM.get('A', 0), GRM.get('B', 0), GRM.get('C', 0), g3['today_max'],
       g1['max_jaccard'], g1['pair'][0], g1['pair'][1], g2['n_tracks'],
       '、'.join('%s×%d' % (k, v) for k, v in g2['pure_value_tracks'].items()),
       g2['rescreen'], g3['today_max'], g3['top10_mean'], g3['window_lo'], g3['window_hi'],
       '、'.join(g3['this_run_batches_excluded']), g3['in_window'], g3['margin'],
       g3['heavy_day_raw'], g3['blockbuster'], len(S3))
)
moc(MAIN, f'papers/MOC/MOC-{DATE}.md',
    f'MOC · {DATE}（11-26 公告批次 · 非重磅日 · {len(MAIN)} 篇）', main_intro)

bf_intro = (
    '> **非当日新提交**：本批 %d 篇均为 11-26 公告 RSS 混入的 `replace` 类旧稿再公告，**首次入馆**；'
    '首发 %s ~ %s。按诚实口径单独编号，**不参与当日重磅日判定**——本批最高 **%.2f**（2611.31822 G0.7）'
    '已越过 4.20 的 S 线，若计入主批会使 today_max 升至 4.43，但仍不足以突破 4.459 的库内基线，'
    '故无论计入与否本批均非重磅日；按口径仍记为 A 并注「达 S 线」。\n'
    '> 定稿 **A %d / B %d / C %d（无 S）**：%s。\n'
    '> 门① 的最大 Jaccard 对（%.3f，%s vs %s）由主批构成，backfill 未参与；本批对仍远低于 0.62 阈值。'
    % (len(BF), min(p['published'] for p in BF), max(p['published'] for p in BF),
       max(p['value'] for p in BF), GRB.get('A', 0), GRB.get('B', 0), GRB.get('C', 0),
       ' · '.join('%.2f %s' % (p['value'], p['title_zh']) for p in BF),
       g1['max_jaccard'], g1['pair'][0], g1['pair'][1])
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
