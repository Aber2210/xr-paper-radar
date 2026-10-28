# MOC · backfill-1029（旧稿再公告补录）

> 本批为 **backfill**：10-28 公告批次 RSS 混入的旧稿 replace/cross 再公告 4 篇首次入馆（原始投稿 2508/2510/2604/2605），**均非当日新提交**。
> 3 A / 1 B；最高 LoBE-GS 3.73（无 S 线）。门① 0.143 / 门② 4 赛道（4 篇低量批次实际上限）/ 门③ 不适用。

## 本批论文（按加权降序）

| # | 论文 | 赛道 | 总分 | 等级 | 证据 | 笔记 |
|---|---|---|---|---|---|---|
| 1 | LoBE-GS：负载均衡的高效大规模 3DGS 训练 | 系统与平台 | 3.73 | A | FULL | [→](../notes/2510.01767__lobe-gs-load-balanced-and-efficient-3d-gaussian-.md) |
| 2 | AmaraSpatial-10K：空间计算与具身 AI 的 3D 资产数据集 | 评估与数据集 | 3.67 | A | FULL | [→](../notes/2604.23018__amaraspatial-10k-a-spatially-and-semantically-al.md) |
| 3 | VolFill：体素流匹配的单图 amodal 场景重建 | 重建与SLAM | 3.65 | A | FULL | [→](../notes/2605.31466__volfill-single-view-amodal-3d-scene-reconstructi.md) |
| 4 | PIS3R：深度 3D 重建的超大视差图像拼接 | 重建与SLAM | 3.58 | B | FULL | [→](../notes/2508.04236__pis3r-very-large-parallax-image-stitching-via-de.md) |

## 批次要点

- **LoBE-GS：负载均衡的高效大规模 3DGS 训练**（2510.01767，3.73 A）：提出以负载均衡 KD 树划分、深度反投影快速相机选择、可见性裁剪与选择性致密化为核心的 3DGS 大规模训练框架 LoBE-GS：端到端训练时间较使用 coarse model 的基线快至 2 倍（MatrixCity-Aerial 1:13 vs CityGS 3:31，约 2.9×；Building 0:55 vs 2:26），划分时间从小时级降至分钟级，同时 PSNR/SSIM 持平或更优。
- **AmaraSpatial-10K：空间计算与具身 AI 的 3D 资产数据集**（2604.23018，3.67 A）：发布 10,071 个度量缩放、语义锚定、PBR 就绪的合成 3D 资产数据集 AmaraSpatial-10K：CLIP Recall@5 较 Objaverse 提升 3.4×（0.612 vs 0.181，中位排名 267→3），Habitat-Sim 跌落测试物理稳定性 99.1%（V-HACD）且墙钟时间较 Objaverse 快约 20×，作为 Holodeck 资产包实现零重叠场景。
- **VolFill：体素流匹配的单图 amodal 场景重建**（2605.31466，3.65 A）：提出以混合 3D VAE + 潜空间流匹配 DiT 生成完整 TUDF 体素网格的单图 amodal 场景重建框架 VolFill：SCRREAM 上完整场景 CD 3.03、FS_0.02 54.83（×10²），显著优于 LaRI（5.19/30.85）与 NOVA3R（3.43/45.12），NRGB-D 上 FS_0.02 63.92 亦领先；RTX 4090 推理仅 1.4 s/图、峰值显存 3.0 GB。
- **PIS3R：深度 3D 重建的超大视差图像拼接**（2508.04236，3.58 B）：提出基于 VGGT 深度 3D 重建 + 点云重投影 + RDDM 扩散精炼的超大视差（VLP）拼接框架 PIS3R：自建合成集 PSNR 22.026、RSR 95.7%，Sampson 对极误差 4.12 pixel（较 UDIS++ 的 12.94 降低约 3.1 倍），且拼接结果保持逐像素 3D 投影一致性、可直接输入 SfM 流程。
