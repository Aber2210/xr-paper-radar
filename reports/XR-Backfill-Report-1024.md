# XR Backfill 报告 · backfill-1024（旧稿 replace 再公告补录）

> **诚实口径**：本批为 2026-10-23 公告批次中 RSS 混入的**旧稿 replace 再公告**（首次入馆），原始投稿月 2508 / 2601 / 2605 / 2609；公告日 2026-10-23、拉取日 2026-10-24。**非 10-24 当日新提交**。
> 数据源：RSS 10-23 公告批次 33 命中中 8 篇旧稿（非 2610.* 前缀），经 XR 相关性甄别留 4 篇；4 篇全部 L0/FULL 全文后按正文证据定稿。

## 补录总览

- 入馆 **4 篇**（A×2 / B×2 / C×0），registry 597 → 618 的组成部分；门① 最大 Jaccard 0.109（与主批合并计算，<0.62 通过）；门③ 对 backfill 不适用。
- 同批剔除的非 XR 旧稿 4 篇：2609.31777（心脏 MRI Rician 去噪）、2604.07993（HEX 人形全身操作）、2604.24033（事件相机 SLAM 基准·无人机高速机动）、2607.06768（AirPASS 6G 联邦学习）。
- OUTDATED/SUPERSEDED：0 篇。

## 补录清单（按加权降序）

| # | 论文 | 赛道 | 分值 | 等级 | 证据 | 原始投稿 | 公告类型 | 笔记 |
|---:|---|---|---:|---|---|---|---|---|
| 1 | 4D 无需位姿：从未知位姿多视角视频前馈重建动态高斯 | 神经渲染 | 4.15 | A | FULL | 2026-05 | replace | [→](../papers/notes/2605.22190__4D 无需位姿-从未知位姿多视角视频前馈重建动态高斯.md) |
| 2 | MEgoVista：野外第一视角多视角感知的运动估计，输出度量化的 4D 手与头 | 化身与人体 | 4.15 | A | FULL | 2026-09 | replace | [→](../papers/notes/2609.16684__MEgoVista-野外第一视角多视角感知的运动估计-输出度量化的 4D 手与头.md) |
| 3 | SpatialMem：面向语言 grounding 与问答的度量对齐长时程视频记忆 | 感知与认知 | 3.55 | B | FULL | 2026-01 | replace | [→](../papers/notes/2601.14895__SpatialMem-面向语言 grounding 与问答的度量对齐长时程视频记.md) |
| 4 | MeSS：城市网格引导、跨视角一致的扩散户外场景生成 | 内容生成 | 3.23 | B | FULL | 2025-08 | replace | [→](../papers/notes/2508.15169__MeSS-城市网格引导-跨视角一致的扩散户外场景生成.md) |

## 逐篇要点

### 1. 4D 无需位姿：从未知位姿多视角视频前馈重建动态高斯（2605.22190）— 4.15 A · 神经渲染

- **一句话结论**：NoPo4D 首个同时满足前馈+免位姿+多视角+动态+一般场景的 4D 重建系统：velocity decomposition 用 SEA-RAFT 伪真值光流直接监督 2D 运动分量，绕开位姿依赖渲染；ExoRecon 29.15 PSNR（DGGT 20.44），post-opt 31.95 超过需位姿的 per-scene SOTA MonoFusion（30.43），快数个数量级。
- **7 维**：IMP 4 · NOV 4 · TEC 4 · EXP 5 · PER 5 · TRL 3 · REP 3（venue：arXiv preprint (cs.CV, 2026-10-22, v2)；证据：FULL / L0 / 66,915 字符）
- **关键实验**：训练约 2,900 个 Ego-Exo4D 场景（796×448），DA3 Large 骨干，4×GH200，两阶段各 20,000 步（先单相机后 1–4 相机 16 帧 batch，时间步长 4–8 预热）。ExoRecon（分布内）：NoPo4D 29.15 PSNR/0.886 SSIM/0.125 LPIPS，大幅超 DGGT(EgoExo4D) 20.44；post-opt 31.95/0.928/0.075 超过需位姿的 per-scene SOTA MonoFusion 30.43/0.930/0.060。OOD：Immersive Light Field 21.63 vs D
- **局限**：假设静态相机 rig，相机自身运动时质量退化（per-camera 位姿平均失效）；依赖 SEA-RAFT 等预训练模型的 pseudo GT，训练质量受教师模型上限约束
- **行动建议**：免位姿动态捕捉（exocentric 多视角、无标定场景）的首选前馈方案；OOD 泛化（Immersive Light Field/Kubric/N3DV）均领先最强 FF 基线。边界：假设静态相机 rig、依赖教师模型质量、需多路时间同步视频。

### 2. MEgoVista：野外第一视角多视角感知的运动估计，输出度量化的 4D 手与头（2609.16684）— 4.15 A · 化身与人体

- **一句话结论**：MEgoVista 把单段未准备的第一视角头戴录制转为米制双手+头部运动：ego-aware 检测（佩戴者/旁观者 F1=1.00）+ calibrated stereo 度量标尺（尺度偏差 |s-1| 低至 0.0048），26 相机光学动捕协议审计下手指 PA-MPJPE-p 4.29mm（较 HaWoR 降 70%）、头部 ATE 0.65-2.87mm（DROID-W 尺度失败 18/22 episodes）。
- **7 维**：IMP 4 · NOV 4 · TEC 4 · EXP 5 · PER 5 · TRL 3 · REP 3（venue：arXiv preprint (cs.CV, 2026-10-11, v2; Maniformer Technical Report 001)；证据：FULL / L0 / 43,564 字符）
- **关键实验**：数据：MEgo View 60 fps，26 相机 120 Hz Chingmu 体积，PTP 同步，每手 15 marker；Session 1 n=22、Session 2 n=20 episodes（最长 104.3 s）。头部（hand-eye 对齐、尺度固定）：Session 1 MEgoVista ATE 2.87 mm（full）/2.83 mm（steady，去前 5 s），Session 2 0.75/0.65 mm，优于 offline-refined ORB-SLAM3（3.27/2.12 与 1.00/0.92）；DROID-W 4/22 episode 严重尺度失败（
- **局限**：评估为 3 个场景（1 个公开 Replica+2 个自采）的离线 proof-of-concept，导航为决策点级 guidance 式评估；手部参考仍受 vendor marker-to-skeleton solver 限制，慢漂移无法被协议捕捉
- **行动建议**：野外 egocentric 米制 4D 手-头标注的系统级方案，Maniformer 技术报告 001；协议审计（拒测计费+参考自审）方法值得借鉴。边界：3 场景离线 proof-of-concept、每 episode 206s、依赖专用 MEgo View 硬件。

### 3. SpatialMem：面向语言 grounding 与问答的度量对齐长时程视频记忆（2601.14895）— 3.55 B · 感知与认知

- **一句话结论**：SpatialMem 从随手拍摄 egocentric RGB 构建层级米制空间记忆树：可插拔几何后端（VGGT/SLAM3R/COLMAP）+ 地平面直立对齐 + 墙/门/窗结构锚 + 开放词汇物体节点，Scene 1 物体检索 SR 0.83、关系准确率 0.84、StepComp 0.89，查询沿图走短链低延迟。
- **7 维**：IMP 4 · NOV 4 · TEC 4 · EXP 3 · PER 3 · TRL 3 · REP 3（venue：arXiv preprint (cs.CV, 2026-03-05, v2)；证据：FULL / L0 / 54,130 字符）
- **关键实验**：三个场景：Scene 1 Replica（公开）、Scene 2 Suite main room、Scene 3 工程实验室/储藏（LUCI pin 相机实采，杂乱度递增）；每场景每任务 500 查询（N_rel=500/N_nav=500/N_obj=500，相对位置共 1,500 次实验）。Scene 1：Acc_rel 0.84（Gemini 2.5 Flash 0.86；墙 0.88、门/窗 0.82）；SR_nav 0.77 vs 0.78；StepComp 0.89 vs 0.84；SPL 0.69 vs 0.68；NE 3.1 m vs 3.2 m；SR_obj 0.83 vs 
- **局限**：仅 3 个场景（1 公开+2 自采）的离线 proof-of-concept，且导航为决策点级 guidance 而非闭环控制；杂乱/遮挡场景下细粒度识别（货架层级、小物体区分）仍下降
- **行动建议**：AR 助手/移动机器人的持久空间记忆接口（memory-centric，米制 3D 作为索引 scaffold 而非建图目标）；与库内 AR Office Recall 同类。边界：3 场景离线验证、杂乱场景细粒度识别下降、左右关系依赖视角局部标签。

### 4. MeSS：城市网格引导、跨视角一致的扩散户外场景生成（2508.15169）— 3.23 B · 内容生成

- **一句话结论**：MeSS 城市 mesh 引导的跨视角一致扩散场景生成：级联反向 outpainting ControlNet（warp+前帧条件抑制长程漂移）+ 关键帧 flattened surfels 免优化落面 + AGInpaint/GCAlign；后退 100m 外推 3200 图 LPIPS 0.348/FID 28.17/KID 0.0161 全面优于 StreetScapes/CityDreamer4D。
- **7 维**：IMP 3 · NOV 3 · TEC 4 · EXP 4 · PER 3 · TRL 3 · REP 2（venue：arXiv preprint (cs.CV, 2025-08-25, v2)；证据：FULL / L0 / 62,633 字符）
- **关键实验**：数据：UE5 City Sample 渲染 960×544、FoV 45°、1 m 间隔，16k 图像对训练两个 ControlNet（冻结 SD1.5，lr 1e-5、batch 128、10k 迭代），关键帧间隔约 20 m，长序列按 200 帧块自回归。定量（后退 100 m 外推共 3200 图）：MeSS LPIPS 0.348/FID 28.17/KID 0.0161，全面优于 StreetScapes 0.519/29.93/0.025、VistaDream-Geometry 0.508/72.44/0.073、WonderWorld-Geometry 0.516/75.807/
- **局限**：缺少公开城市 mesh 数据集，训练/评估依赖 UE5 City Sample 合成数据；GCAlign 以轻微模糊换一致性（FID/KID 反而略升）；SD1.5 基座限制分辨率
- **行动建议**：VR 城市导航/数字孪生的纹理生成路线（UE5 City Sample 可复现）。边界：缺公开城市 mesh 数据集、SD1.5 基座限分辨率、GCAlign 以轻微模糊换一致性、无代码。

## 与文献库的关系

- NoPo4D 补「前馈 + 免位姿 + 多视角 + 动态 + 一般场景」空白象限（与库内 NoPoSplat/FLARE/AnySplat 静态免位姿线、4DGT 需位姿线互补）；MEgoVista 与 10-23 批 EgoHand 构成第一视角手部重建「相机感知单目 vs stereo 度量标尺」双路线对照；SpatialMem 与库内 AR Office Recall（10-19）同属 memory-centric 空间记忆接口；MeSS 补城市场景生成的 mesh 先验路线。

## 数据与过程

- [backfill-1024 7 维对比表](../papers/daily/backfill-1024/7dim-table.md) · [执行日志](../papers/daily/backfill-1024/run_log.md) · [MOC-backfill-1024](../papers/MOC/MOC-backfill-1024.md)
- 当日主批报告：[XR-Daily-Report-2026-10-24](./XR-Daily-Report-2026-10-24.md)
