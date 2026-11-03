# MOC · backfill-1104（旧稿再公告补录）

> 本批为 **backfill**：11-03 公告批次 RSS 混入的旧稿 replace/cross 再公告 8 篇首次入馆（原始投稿 2508=2025-08 / 2509=2025-09 / 2511=2025-11 / 2512=2025-12 / 2603=2026-03 / 2605=2026-05 / 2606=2026-06 / 2607=2026-07），**均非当日新提交**。
> 5 B / 3 C；最高 FLEG 3.58 / AR 超声 3.58 并列（无 S 线）。门① 0.151 / 门② 6 赛道 / 门③ 不适用。

## 本批论文（按加权降序）

| # | 论文 | 赛道 | 总分 | 等级 | 证据 | 笔记 |
|---|---|---|---|---|---|---|
| 1 | AR 引导机器人超声联合锥束 CT 用于脊柱操作的可行性 | 空间计算与UI | 3.58 | B | FULL | [→](../notes/2603.22174__feasibility-of-augmented-reality-guided-robotic-.md) |
| 2 | FLEG：经紧凑语义表示的任意视角前馈语言嵌入高斯泼溅 | 神经渲染 | 3.58 | B | FULL | [→](../notes/2512.17541__fleg-feed-forward-language-embedded-gaussian-spl.md) |
| 3 | 4D 高斯光线追踪：基于物理的相机效应数据生成 | 神经渲染 | 3.43 | B | FULL | [→](../notes/2509.10759__every-camera-effect-every-time-all-at-once-4d-ga.md) |
| 4 | Splaxel：经像素级通信的高效分布式 3D 高斯泼溅训练 | 系统与平台 | 3.31 | B | FULL | [→](../notes/2606.18588__splaxel-efficient-distributed-training-of-3d-gau.md) |
| 5 | EAvatar：以生成式几何先验进行表情感知的头部化身重建 | 化身与人体 | 3.08 | B | FULL | [→](../notes/2508.13537__eavatar-expression-aware-head-avatar-reconstruct.md) |
| 6 | VR 的眼部验证 | 感知与认知 | 2.93 | C | FULL | → |
| 7 | 数字孪生 3D 世界重建中的材质感知高斯泼溅 | 重建与SLAM | 2.78 | C | FULL | → |
| 8 | Aes3D：3D 高斯泼溅的美学评估 | 评估与数据集 | 2.72 | C | FULL | → |

## 批次要点

- **AR 引导机器人超声联合锥束 CT 用于脊柱操作的可行性**（2603.22174，3.58 B）：16 名受试者（6 女 10 男，22–43 岁，平均 28.75±4.49）的 phantom within-subject 研究显示：AR 相较常规屏幕总体执行时间降 49%（W=5.0，p=0.0003）、放置误差降 25%（t=3.29，p=0.0050）。分任务：LP 时间降 42%（78.25±56.46→45.31±24.90 s，p=0.002）、LP 误差降 32%（13.12±5.43→8.89±2.71 mm，p=0.015，显著）；FJ 时间降 54%（95.25±54.51→43.50±19.17 s，p=0.003）、FJ 误差降 18%（11.76±6.37→9.69±2.93 mm，p=0.228，不显著）。主观：可用性 +50%（p=0.00060）、NASA-TLX 负荷 -37%（p=0.0025）、信任 +41%（p=0.00070）、空间理解 +89%（p=0.0004）。系统精度：US-CBCT 目标配准误差 1.72±0.62 mm、探头标定 0.65±0.2 mm、点云配准 RMSE 9.1 mm。
- **FLEG：经紧凑语义表示的任意视角前馈语言嵌入高斯泼溅**（2512.17541，3.58 B）：FLEG 在 2 视角 ScanNet++ 上 mIoU 46.61/mAcc 71.18/PSNR 28.14，超过 Uni3R（39.54/58.59/24.95）与 LSM（39.36/58.35/19.87）；ScanNet 2 视角 mIoU 48.01/mAcc 73.59。32 密集视角下 ScanNet mIoU 60.97 显著高于 per-scene 优化的 LangSplat（41.24）。DGLE 稀疏语义高斯仅用 73.89K 个 embedding（密集像素对齐 2.012M 的约 3.7%，论文表述为不足 5%）、存储 18.04 MB vs 491.3 MB，语义保真度相当。消融：去掉 instance-guided contrastive learning mIoU 从 46.87 跌至 40.22；去掉几何蒸馏跌至 18.56、训练不稳定。
- **4D 高斯光线追踪：基于物理的相机效应数据生成**（2509.10759，3.43 B）：在自建 8 个室内动态场景×4 种相机效应基准上，4D-GRT 渲染速度全面最快且质量与 MSTH 相当或更优：pinhole PSNR 32.801 @36.56 FPS（MSTH 29.431 @9.38 FPS）、DoF 31.2475 @3.44 FPS（MSTH 0.57 FPS）、fisheye masked PSNR 28.8927 @41.53 FPS（MSTH masked 26.7930 @9.38 FPS）、rolling shutter chunk=4 时 31.6146 @4.99 FPS（chunk=16 时 13.54 FPS，指标几乎无损）。效率：训练 3 小时/存储 364.875 MB（HexPlane 12h/238MB，MSTH 8min/889MB）。fisheye 评测需用直径 409.6 的圆形 mask 屏蔽训练视角外区域。
- **Splaxel：经像素级通信的高效分布式 3D 高斯泼溅训练**（2606.18588，3.31 B）：8 GPU 下相较 SOTA 分布式 3DGS 框架 Grendel：Big City Street（120M 高斯）训练 48.8h→6.4h（7.6×，PSNR 均 23.2）、Big City Aerial 3.6h→1.2h（2.9×，PSNR 30.4→31.2）、Small City Street 7.5h→1.3h（5.9×，PSNR 21.4→21.7）、Small City Aerial 25.5m→8.0m（PSNR 26.6→27.3）。吞吐最高 90 img/s（Big City Street，Grendel 14）与 142 img/s（Big City Aerial，Grendel 52）。通信占迭代时间从 Grendel 的 73.0%–80.4% 降至 10%–20%；redundancy reduction 使 zero-pixel 比例降 39%（Small Street）/55%（Small Aerial）、saturated-pixel 降 40%/34%；GPU 利用率提升 20%–35%。
- **EAvatar：以生成式几何先验进行表情感知的头部化身重建**（2508.13537，3.08 B）：在 NeRSemble 多视图数据上，EAvatar 自驱重演 5 个 identity 全 16 视角平均 PSNR 25.07、SSIM 0.857、LPIPS 0.168，超过 GHA（24.56/0.853/0.175）与 TensorialGA（24.07/0.848/0.204）；新视角合成 PSNR 23.22 vs GHA 22.89、TensorialGA 21.51。RTX 3090 上渲染约 32 FPS、单主体训练约 2.5 天；相较 GaussianAvatars（183 FPS 但 PSNR 22.50、预处理 32.7 小时）以 12.0 小时预处理换取更高保真。生成式先验使 Stage I 训练时间减少 11%。消融：Case 1 PSNR 由 baseline 23.28 经 +control 23.36、+split 23.47 升至全模块 23.66；控制阈值 τ=0.3 优于 0.15 与 0.4。
- **VR 的眼部验证**（2607.20790，2.93 C）：在 VRBiom（Meta Quest Pro 内向 NIR，400×400，900 段 bonafide 视频、25 名受试者、平均约 23K 帧/人）上：单模态虹膜 EER 0.44/AUC 0.59/d' 0.34，眼周（MobileFaceNet）EER 0.34/AUC 0.76/d' 1.08；最佳 peri-heavy 融合（w_i=0.25/w_p=0.75）EER 0.33、AUC 0.75、d' 0.99（约 3 倍于虹膜），论文自述相对单模态虹膜 AUC 提升约 16%、EER 降低约 11%。UnReflect 去高光使所有眼周模型 EER 下降（MobileFaceNet 34.70→31.97），但 UNIR-Net 照明修复反而使虹膜 AUC 从 0.62 跌至 0.59；OAC 几何校正表现最差（插值与 padding 损伤高频纹理）。ISO margin adequacy 在 MITRE 框架仅 4.38±16.37（远低于推荐阈值 80），concentricity 同样在 VR 原生影像上失效。
- **数字孪生 3D 世界重建中的材质感知高斯泼溅**（2511.20348，2.78 C）：仅用相机的管线在 5 个城市场景上达到与 LiDAR-camera 融合（NKSR 网格）相当的 LiDAR 反射率仿真精度：MAE 10.05 vs 10.14、中位误差 6.48 vs 6.78。视觉质量上本文 adapted H3DGS 的 LPIPS 0.44 为全场最佳（3DGS 0.46、CityGaussianV2 0.50、3DGUT 0.53，5 场景中 4 个最优），但 PSNR 18.27、SSIM 0.41 低于三个基线（20.07–21.22 / 0.56–0.58）。材质分割消融（MCubes 500 图）：RMSNet 准确率 0.63/mIoU 0.28，+FastSAM 0.65/0.29，+SAM2 0.67/0.31。
- **Aes3D：3D 高斯泼溅的美学评估**（2605.05155，2.72 C）：Aesthetic3D 为首个 3D 场景美学数据集：278 个重建场景、92,649 个输入视图（平均 333 视角/场景，源自 DL3DV-10K 采样子集 + Bilarf），场景级分数跨度 0.184–0.825（均值 0.395、中位 0.369、std 0.129）；场景内视角分差均值 0.33（p90 0.47、max 0.85），83.2% 场景分差>0.20，证明 3D 美学强视角依赖。Aes3DGSNet 仅 3.2M 参数、29.4 GFLOPs：8-attr 标签下 PLCC 0.567/SRCC 0.554/KRCC 0.389，total 标签下 MAE 0.076/RMSE 0.101，均优于 Stochastic NR-PCQA（PLCC 0.509）、GSOQA（0.503）、MM-PCQA（0.441）、MUGSQA-DBCNN（0.311）与 ArtiMuse（0.224）等基线。
