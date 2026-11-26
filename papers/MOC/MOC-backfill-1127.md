# MOC · backfill-1127（旧稿 replace 再公告首次入馆）

> **非当日新提交**：本批 8 篇均为 11-26 公告 RSS 混入的 `replace` 类旧稿再公告，**首次入馆**；首发 2025-09-20 ~ 2026-11-24。按诚实口径单独编号，**不参与当日重磅日判定**——本批最高 **4.43**（2611.31822 G0.7）已越过 4.20 的 S 线，若计入主批会使 today_max 升至 4.43，但仍不足以突破 4.459 的库内基线，故无论计入与否本批均非重磅日；按口径仍记为 A 并注「达 S 线」。
> 定稿 **A 7 / B 1 / C 0（无 S）**：4.43 G0.7：用长上下文扩展快速世界动作模型 · 4.22 HPC：面向流式动态高斯泼溅压缩的层次化点式隐表示 · 4.15 ArtMesh：带运动一致动力学的部件感知铰接网格场 · 4.00 基于多 GPU PyTorch 后端的大规模高斯泼溅 · 3.85 3DSS：用于逆渲染的三维表面泼溅 · 3.72 EgoCaptioner：面向全面细粒度第一视角视频描述 · 3.62 LightFuse：多扫描融合与二维高斯光线追踪的可重打光交互式场景重建 · 3.55 GazeVLM：以注视引导中央凹式推理的高效视觉语言模型。
> 门① 的最大 Jaccard 对（0.127，2611.34810 vs arXiv:2609.22941）由主批构成，backfill 未参与；本批对仍远低于 0.62 阈值。

## 本批论文（按加权降序）

| # | 论文 | 赛道 | 总分 | 等级 | 证据 | 笔记 |
|---|---|---|---|---|---|---|
| 1 | G0.7：用长上下文扩展快速世界动作模型 | 世界模型与仿真 | 4.43 | A | FULL | [→](../notes/2611.31822__g0-7-scaling-up-a-fast-world-action-model-with-long-.md) |
| 2 | HPC：面向流式动态高斯泼溅压缩的层次化点式隐表示 | 神经渲染 | 4.22 | A | FULL | [→](../notes/2602.00671__hpc-hierarchical-point-based-latent-representation-f.md) |
| 3 | ArtMesh：带运动一致动力学的部件感知铰接网格场 | 重建与SLAM | 4.15 | A | FULL | [→](../notes/2605.16582__artmesh-part-aware-articulated-mesh-fields-with-moti.md) |
| 4 | 基于多 GPU PyTorch 后端的大规模高斯泼溅 | 系统与平台 | 4.00 | A | FULL | [→](../notes/2606.11390__large-scale-gaussian-splatting-with-a-multi-gpu-pyto.md) |
| 5 | 3DSS：用于逆渲染的三维表面泼溅 | 神经渲染 | 3.85 | A | FULL | [→](../notes/2605.05876__3dss-3d-surface-splatting-for-inverse-rendering.md) |
| 6 | EgoCaptioner：面向全面细粒度第一视角视频描述 | 感知与认知 | 3.72 | A | FULL | [→](../notes/2611.26380__egocaptioner-towards-comprehensive-and-fine-grained-.md) |
| 7 | LightFuse：多扫描融合与二维高斯光线追踪的可重打光交互式场景重建 | 神经渲染 | 3.62 | A | FULL | [→](../notes/2608.29269__lightfuse-relightable-interactive-gaussian-scene-rec.md) |
| 8 | GazeVLM：以注视引导中央凹式推理的高效视觉语言模型 | 交互与输入 | 3.55 | B | FULL | [→](../notes/2509.16476__gazevlm-gaze-guided-foveated-inference-for-efficient.md) |

## 批次要点

- **G0.7：用长上下文扩展快速世界动作模型**（2611.31822，4.43 A）：把世界动作模型的长上下文做成预训练期的一等能力（可变长多 chunk 自回归 + chunk-causal attention），并用双专家把语言条件逐层注入共享的 vision/action expert——五个仿真基准均值 70.8（OpenWAM 43.9、π0.5 33.9），RMBench 86.2%（单帧基线 < 12%），LIBERO-Plus 92.5%，零样本真机抓放 48% / 54%。
- **HPC：面向流式动态高斯泼溅压缩的层次化点式隐表示**（2602.00671，4.22 A）：在最新解码的高斯上建层次化点式 latent（3 尺度、每尺度 16 通道），配网络参数压缩做流式动态 3DGS 编码——N3DV 32.36 dB / 39 KB 每帧（iFVC-h 32.35 / 99 KB、4DGC 31.58 / 500 KB、3DGStream 31.69 / 7780 KB），BD-BR 相对 iFVC 平均 −67.8%。
- **ArtMesh：带运动一致动力学的部件感知铰接网格场**（2605.16582，4.15 A）：用部件感知三角网格场 + 运动一致动力学，从两个关节状态重建铰接物体并直接给出带部件边界的网格——Articulate-100（给 GT 掩码）轴角 3.49°、CD-m 15.01 mm（最强基线 57.45 / 58.66，改善 +42.44 mm），6+ 部件档轴角 6.90°（GaussianArt 33.05°）。
- **基于多 GPU PyTorch 后端的大规模高斯泼溅**（2606.11390，4.00 A）：把多卡拼成统一虚拟地址空间（kDGX dispatch + stream-ordered 异步 UM 分配器），让分布发生在算子内部而非切模型——Gettysburg 268M splats / 153 张 7088×5314 / 13 km² / 8×A100 用 3.086 h 达 PSNR 27.450，十亿级 splats 超 Grendel-GS 最大规模 25 倍，$B=N$ 平均加速 3.15×。
- **3DSS：用于逆渲染的三维表面泼溅**（2605.05876，3.85 A）：用无结构 oriented surfel（切向量编码朝向、刻意不设可学习不透明度）+ T-matrix 光栅化做逆渲染，绕开网格拓扑与体渲染的 alpha 混合语义——Stanford-ORB 新视角 PSNR-H 31.73 / PSNR-L 40.73（RTR-GS 30.10 / 39.17、NVDiffRec 21.94 / 28.44），重打光 23.22 / 30.44。
- **EgoCaptioner：面向全面细粒度第一视角视频描述**（2611.26380，3.72 A）：把第一视角描述拆成 video-level overview + 带起止时间的有序 steps 两层，并造 50,000 条 coarse-to-fine 训练样本——PhysCapBench 78.84（主干 51.24，+27.6，超过 Gemini 3.1 Pro 75.06），EgoTempo 38.40（21.60），EgoHome 步分割 PSJ 75.51（46.90）。
- **LightFuse：多扫描融合与二维高斯光线追踪的可重打光交互式场景重建**（2608.29269，3.62 A）：把几何与 PBR 材质跨状态共享、状态间只差物体刚体变换与光照，用 2D 高斯 surfel + 光线追踪做多扫描融合——新状态重打光 PSNR 25.89 / SSIM 0.873（比最强基线 IRGS 高 6.01 dB），真实场景 24.35 dB（ReCap +1.55）但 SSIM 略低（0.821 vs 0.903）。
- **GazeVLM：以注视引导中央凹式推理的高效视觉语言模型**（2509.16476，3.55 B）：把实测注视投影成注意图、按 gaze mass 取最小前缀包围盒做中央凹裁剪，training-free 地给 VLM 分配算力——Qwen2.5-VL-3B 匹配率 73.54→82.03%、视觉 token 15.55k→2.46k（−84.2%）、延迟 3.20→0.45 s（7.1×）；Qwen3-VL-8B 80.78→83.70%、11.6×。
