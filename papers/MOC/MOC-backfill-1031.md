# MOC · backfill-1031（旧稿再公告补录）

> 本批为 **backfill**：10-30 公告批次 RSS 混入的旧稿 replace/cross 再公告 6 篇首次入馆（原始投稿 2501/2604/2605/2608），**均非当日新提交**。
> 5 A / 1 B；最高 InHabit 4.07（无 S 线）。门① 0.075 / 门② 5 赛道（6 篇低量批次实际上限）/ 门③ 不适用。

## 本批论文（按加权降序）

| # | 论文 | 赛道 | 总分 | 等级 | 证据 | 笔记 |
|---|---|---|---|---|---|---|
| 1 | InHabit：基于图像基础模型的 3D 人-场景交互数据规模化生成 | 评估与数据集 | 4.07 | A | FULL | [→](../notes/2604.19673__inhabit-scaling-3d-human-scene-interaction-data-.md) |
| 2 | SplitGS-Loc：高斯劈分消解多对一对应的视觉定位 | 重建与SLAM | 3.94 | A | FULL | [→](../notes/2605.07351__disambiguating-2d-3d-correspondences-in-gaussian.md) |
| 3 | Ego-OSCAR：开源头戴双目-惯性第一人称采集系统 | 系统与平台 | 3.72 | A | FULL | [→](../notes/2608.08285__ego-oscar-egocentric-open-source-stereo-capture-.md) |
| 4 | VidParse：免训练的第一视角流程在线解析 | 感知与认知 | 3.72 | A | FULL | [→](../notes/2608.27562__vidparse-online-parsing-of-egocentric-procedures.md) |
| 5 | BitC-3DGS：位压缩 token 化的高容量 3DGS 水印 | 渲染与显示 | 3.65 | A | FULL | [→](../notes/2605.29583__bitc-3dgs-high-capacity-3d-gaussian-splatting-wa.md) |
| 6 | GSVC：以 2D 高斯泼溅为基元的视频表示与压缩 | 系统与平台 | 3.57 | B | FULL | [→](../notes/2501.12060__gsvc-efficient-video-representation-and-compress.md) |

## 批次要点

- **InHabit：基于图像基础模型的 3D 人-场景交互数据规模化生成**（2604.19673，4.07 A）：InHabit 以“渲染-生成-提升”管线把 2D 基础模型的交互常识迁移到 3D，在 HM3D 约 800 个建筑级场景全自动生成超 78k 个带完整几何的 SMPL-X 交互样本（InHabitants 数据集）；放置质量用户研究 78.1% 偏好率胜出，并使 DECO 接触估计 F1 提升 7.4%、GRAFT 重建 PA-MPJPE 由 72.52 降至 54.83。
- **SplitGS-Loc：高斯劈分消解多对一对应的视觉定位**（2605.07351，3.94 A）：SplitGS-Loc 指出光度优化的高斯特征场因多对一像素-高斯对应与冗余高斯而不适配 2D-3D 匹配，提出基于组成权重的特征提升与沿主轴的高斯劈分，在 Cambridge Landmarks 上平均误差 8.7cm/0.15°（STDLoc 为 11.1cm/0.19°）、7Scenes 上 1.0cm/0.26°，建图仅 7 分钟、地图 97MB，且无需逐场景特征场训练与迭代位姿精化。
- **Ego-OSCAR：开源头戴双目-惯性第一人称采集系统**（2608.08285，3.72 A）：Ego-OSCAR 是一套整机物料约 200 美元的全开源头戴式双目-惯性采集系统（硬件同步全局快门立体相机+6 轴 IMU+SBC+实时 MCU），在印度 25 名贡献者、40+ 室内环境约 6 个月部署中采集 1,462 个会话约 550 小时/相机，可用会话率 96%，并随设备发布含 209,315 条开放词表动作片段与全语料手部检测的标注数据集。
- **VidParse：免训练的第一视角流程在线解析**（2608.27562，3.72 A）：VidParse 是在线、免训练的第一人称流程解析框架：冻结 DINOv2 补丁特征加手-物检测构成操作锚定特征，经高斯锥形棋盘核在时序相似度矩阵上检测边界，再用任务图约束束搜索解码；EgoPER 上 F1@0.5 达 77.6（在线 ProTAS 为 51.3），5/7 步转移 AUC 最高达基线 5–10 倍，全程 8.6 FPS、零梯度更新。
- **BitC-3DGS：位压缩 token 化的高容量 3DGS 水印**（2605.29583，3.65 A）：BitC-3DGS 用“位压缩 token 化”突破 CLIP 77 token 对 3DGS 语义水印约 75 bit 的容量上限，配合双分支解码器与难样本采样，在 Blender/LLFF 上实现 128 bit 水印，恢复比特精度 90.59%（[Random]）/91.42%（[In]），与先前方法 64 bit 水平相当，且 PSNR 34.32、LPIPS 0.0068 保持高保真。
- **GSVC：以 2D 高斯泼溅为基元的视频表示与压缩**（2501.12060，3.57 B）：GSVC 以 2D 高斯泼溅为视频新基元，在 UVG 数据集上取得与 AV1、HEVC 相当的率失真性能（MS-SSIM 与 VMAF 上优于或持平多数标准编解码器、仅逊于 VVC），解码速度实测 1583.72 fps，远高于神经方法 DCVC-DC 的 2.4 fps，且无需预训练、支持显式的规模-质量-时长控制。
