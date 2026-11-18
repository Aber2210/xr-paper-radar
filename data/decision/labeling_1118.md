# 判定标注表 1118（问题版本 q2-2026-11-18）

## 判定规则：属于下列任一赛道即判 1

| 赛道 | 覆盖范围 |
|---|---|
| 神经渲染 | NeRF / 3DGS / 神经场 / 可微渲染 / 新视角合成 |
| 渲染与显示 | 渲染管线、显示硬件（波导 / 近眼 / 光场）、实时渲染系统 |
| 重建与SLAM | SfM / SLAM / 深度与位姿估计 / 点云与网格重建 |
| 化身与人体 | 人体 / 手 / 脸建模与驱动、化身、动作捕捉 |
| 交互与输入 | 手势 / 眼动 / 控制器 / 文本输入等空间交互范式 |
| 触觉与多模态 | 触觉显示与感知、力反馈、多模态融合 |
| 内容生成 | 面向 3D / 场景 / 视频的生成与编辑 |
| 世界模型与仿真 | 物理仿真、交互式世界模型、场景模拟 |
| 感知与认知 | 场景理解、视觉定位、用户感知与认知研究 |
| 空间计算与UI | 空间布局、UI 放置、空间锚点与协作 |
| 系统与平台 | XR 系统架构、性能与延迟、设备与工具链 |
| 评估与数据集 | 基准、数据集、评测方法 |

- **判 1**：论文的研究对象或方法**会被收进**上述任一类（按你日常收稿的判断）。
- **判 0**：完全落在通用视觉/自然语言/机器人/医学等领域，不对应任何一类。
- **判 ?**：读完也说不清该归哪一类——这类我会拿去改赛道定义，不改标签。

## 怎么填

- 每条末尾两行：`判定：` 填 `1` / `0` / `?`；`摘要是否足够：` 填 `是` / `否`。
- **标注以「这篇到底该不该收」为准——摘要看不出来就点 arXiv 链接读全文**，目标是真值，不是复刻模型的视野。
- 「摘要是否足够」决定模型评测的公平分母：标「否」的条目，只看摘要的模型不可能判对。
- 「你在窄口径(q1)下判的是」是你自己的上一轮判断，仅供对照，**请按新口径重新判**。

---

### 1 · 2605.09586 · DeformMaster: An Interactive Physics-Neural World Model for Deformable Objects from Videos

- 类别：cs.CV ｜ 抽样：边界 ｜ 组：accepted
- 摘要：World models for deformable objects should recover not only geometry and appearance, but also underlying physical dynamics, interaction grounding, and material behavior. Learning such a model from real videos is challenging because deformable linear, planar, and volumetric objects evolve under high-dimensional deformation, noisy interactions, and complex material response. The model must infer a physical state from visual observations, roll it forward under new interactions, and render the resulting dynamics with high visual fidelity. We therefore present DeformMaster, a video-derived interactive physics-neural world model that turns real interaction videos into an online interactive model of deformable objects within a unified dynamics-and-appearance framework. DeformMaster preserves structured physical rollout while using a neural residual to compensate for unmodeled effects, grounds sparse hand motion as distributed compliant actuators for hand-continuum interaction, represents material response with spatially varying constitutive experts, and drives high-fidelity 4D appearance from the predicted physical evolution. Experiments on real-world deformable-object sequences demonstra
- 链接：https://arxiv.org/abs/2605.09586
- 你在窄口径(q1)下判的是：**0**
- **判定：** （填 1 / 0 / ?）
- 摘要是否足够： （是 / 否 —— 填「否」表示必须看全文才敢定）

### 2 · 2611.18267 · TetraCoder: Adaptive Tetrahedral Encoding for Neural Fields

- 类别：cs.GR ｜ 抽样：边界 ｜ 组：accepted
- 摘要：Implicit and explicit representations of geometry are central in computer graphics applications and come with their pros and cons. With surface sampling being faster on explicit representations and spatial queries being faster on implicit representations, finding efficient conversions between them is a highly desirable property. We present TetraCoder, a single resolution hash-free adaptive tetrahedral encoding that links an explicit tetrahedral spatial encoder with an underlying implicit signed distance field (SDF). The resulting hybrid implicit-explicit space is continuous piecewise affine (CPWA) by design, allowing to obtain an exact correspondence between the implicit SDF and the explicit analytic mesh. TetraCoder's design comes with additional perks, in particular: (a) it scales better than multi-resolution encoding methods due to its single resolution optimizable grid, (b) unlike hash-based methods, it is not affected by collisions, (c) it enables fast tetrahedral ray-tracing, geometry and appearance editing, directly through its adaptive tetrahedral scaffold. We demonstrate the versatility of TetraCoder by showing an improvement over state-of-the-art methods on multiple tasks
- 链接：https://arxiv.org/abs/2611.18267
- 你在窄口径(q1)下判的是：**0**
- **判定：** （填 1 / 0 / ?）
- 摘要是否足够： （是 / 否 —— 填「否」表示必须看全文才敢定）

### 3 · 2611.18734 · Is It Still There? Place-Registered Verification Makes VLMs Reliable Scene-Change Detectors

- 类别：cs.CV ｜ 抽样：边界 ｜ 组：accepted
- 摘要：A robot that returns to a space must tell which objects were added, removed or moved since its last visit, while its trajectory, viewpoints and lighting differ between the two visits. We find that multi-image vision-language models (VLMs) fail at this task mainly because they cannot find the place where an object was. A VLM recognises what each frame shows but cannot check whether an object is still at its place in the other capture. It therefore reports objects that only one capture shows and misses most removed and moved objects. We propose STILL, which reformulates change detection as object verification at a registered place. 3D geometry registers the place of each change hypothesis in the other capture, and one VLM answers, from a scene view and a local place view, whether the object is still at that place, trained with supervision of the same form. Under the official SceneDiff protocol, STILL raises the main metric obj/sc AP from 24.0 to 37.8, and from 11.6 to 20.6 on the egocentric kitchen subset without any kitchen training data. It improves F1 by more than 21 points over a VLM fine-tuned on the same annotations and adds only about 11% to the runtime.
- 链接：https://arxiv.org/abs/2611.18734
- 你在窄口径(q1)下判的是：**0**
- **判定：** （填 1 / 0 / ?）
- 摘要是否足够： （是 / 否 —— 填「否」表示必须看全文才敢定）

### 4 · 2611.18894 · CISyn: Human Mesh Recovery in Close Interactions with Physics-Simulated Synthetic Data

- 类别：cs.CV ｜ 抽样：边界 ｜ 组：accepted
- 摘要：3D human mesh recovery (HMR) in close-interaction scenarios is hindered by the lack of large-scale, accurately annotated training data: real capture is expensive, and existing synthetic datasets rarely include physical contact. We introduce CISyn, a large-scale synthetic dataset purpose-built for close human-human interactions, generated via physics simulation and Blender-based rendering. By simulating collision dynamics between SMPL-X-rigged humanoids, CISyn naturally produces the contact, mutual occlusion, and pose entanglement that characterize close-interaction scenes, with no manual annotation effort. The released set provides 25,000 sequences with accurate 3D annotations. We further propose an uncertainty-aware loss that allows models to learn more effectively from the heavily occluded examples in our data. Augmenting state-of-the-art HMR training with CISyn and replacing the regression loss with our uncertainty-aware variant yields consistent improvements on close-interaction benchmarks, validating CISyn as a scalable complement to real-world data. The dataset, generation pipeline, and code are available at https://github.com/yfde/CISyn.
- 链接：https://arxiv.org/abs/2611.18894
- 你在窄口径(q1)下判的是：**0**
- **判定：** （填 1 / 0 / ?）
- 摘要是否足够： （是 / 否 —— 填「否」表示必须看全文才敢定）

### 5 · 2611.18979 · Probing Where Surprise Happens: Localized Violation-of-Expectation Evaluation of Video World Models

- 类别：cs.CV ｜ 抽样：边界 ｜ 组：accepted
- 摘要：Violation-of-expectation (VOE) benchmarks evaluate intuitive physics in video world models by testing whether physically impossible events produce greater prediction errors than matched possible events. However, conventional VOE evaluations aggregate prediction errors across space and time, making it unclear whether successful discrimination reflects model's understanding of physical violations at the locations and time where they occur. To address this limitation, we introduce localized VOE evaluation, a framework that measures prediction error differences between possible and impossible events within spatial regions and temporal intervals associated with physical violations. We compare global, temporally localized, and spatiotemporally localized evaluations of V-JEPA models pretrained on developmental egocentric videos or large-scale natural video datasets. Our results reveal that global and localized judgments can diverge in both directions: global aggregation can either obscure correct localized discrimination or produce apparent discrimination without corresponding localized evidence. During continued pretraining on developmental egocentric videos, agreement between global and
- 链接：https://arxiv.org/abs/2611.18979
- 你在窄口径(q1)下判的是：**0**
- **判定：** （填 1 / 0 / ?）
- 摘要是否足够： （是 / 否 —— 填「否」表示必须看全文才敢定）

### 6 · 2611.19095 · DEFDVO: Deformable Deep Visual Odometry for Equirectangular Images

- 类别：cs.CV ｜ 抽样：边界 ｜ 组：accepted
- 摘要：Omnidirectional ($360^\circ$) cameras capture the full surrounding scene in every frame, providing a strong advantage for visual odometry (VO) over pinhole sensors with a limited field of view. However, their equirectangular projection (ERP) introduces latitude-dependent distortion, an artificial seam at the image border, and a sampling bias toward the poles. Existing $360^\circ$ VO methods address these challenges only partially. DEFDVO closes this gap with a patch-based deep VO method that operates directly on ERP imagery, combining spherically initialized deformable feature extraction, end-to-end seam-aware estimation, and spherical-gradient patch selection. The deformable feature extractor combines spherical geometric priors with learned sampling offsets, while seam-aware processing preserves ERP continuity, and spherical-gradient selection reduces polar sampling bias. Trained exclusively on synthetic TartanAirV2 ERP imagery, DEFDVO improves the best prior average absolute trajectory error (ATE) by $4.8\times$ (0.201 m to 0.042 m) on the TartanAirV2 evaluation set defined by 360DVO and achieves the lowest average ATE on both splits of the real-world 360DVO benchmark. Code is av
- 链接：https://arxiv.org/abs/2611.19095
- 你在窄口径(q1)下判的是：**0**
- **判定：** （填 1 / 0 / ?）
- 摘要是否足够： （是 / 否 —— 填「否」表示必须看全文才敢定）

### 7 · 2611.19803 · Pros4D: Modeling Evolving 4D Worlds in Latent Space for Dynamic Spatial Reasoning

- 类别：cs.CV ｜ 抽样：边界 ｜ 组：accepted
- 摘要：Dynamic spatial reasoning from monocular video enables vision-language models (VLMs) to understand how 3D environments evolve over time, supporting physical world understanding and embodied intelligence. Existing efforts primarily address observed-dynamics understanding, whereas agents in dynamic environments also require future-dynamics prediction beyond the observation boundary. Moreover, external geometric processing and textual descriptions can increase inference complexity or lose information when representing continuous dynamics. These limitations motivate a shared internal state that preserves observed dynamics and remains predictive beyond the input video. Accordingly, we present Pros4D, a framework for modeling evolving 4D worlds in latent space that unifies retrospective understanding of observed-dynamics with prospective reasoning for future-dynamics prediction. Specifically, Pros4D-Engine derives geometry-grounded supervision and constructs paired examples for both tasks, while Pros4D-Bench evaluates them across eight spatial task categories spanning dynamic cameras, objects, and scenes. At the model level, Pros4D compresses observed dynamics into latent observed states
- 链接：https://arxiv.org/abs/2611.19803
- 你在窄口径(q1)下判的是：**0**
- **判定：** （填 1 / 0 / ?）
- 摘要是否足够： （是 / 否 —— 填「否」表示必须看全文才敢定）

### 8 · 2611.20196 · DoF-Query Transformer for Adaptive Fusion of Egocentric Vision and Forearm HD-sEMG in Continuous Hand Kinematics

- 类别：cs.CV ｜ 抽样：边界 ｜ 组：accepted
- 摘要：Continuous and accurate estimation of human hand kinematics is important not only for intuitive human-machine interaction, but also for capturing fine-grained human manipulation demonstrations that can provide action supervision for embodied-intelligence datasets and dexterous robot learning. However, individual sensing modalities may be insufficient for reliable estimation under varying operating conditions. We present a finger-unencumbered multimodal framework for continuous regression of 20 hand joint angles from egocentric RGB images and 128-channel forearm high-density surface electromyography (HD-sEMG). The framework combines a Vision Transformer-based visual encoder, a Transformer-based EMG encoder, and a degree of freedom (DoF) query Transformer fusion decoder. To account for the varying informativeness of visual and EMG cues across joint DoFs and input conditions, the decoder assigns a separate learnable query to each DoF, enabling DoF-specific and context-adaptive fusion of the two modalities. The framework was evaluated on synchronized multimodal data from 10 participants. Averaged across participants, the proposed fusion model achieved a mean coefficient of determinatio
- 链接：https://arxiv.org/abs/2611.20196
- 你在窄口径(q1)下判的是：**0**
- **判定：** （填 1 / 0 / ?）
- 摘要是否足够： （是 / 否 —— 填「否」表示必须看全文才敢定）

### 9 · 2611.20533 · RemeshingAgent: Self-Evolving Agent for Repair-Based Decimation of Generated Building Meshes

- 类别：cs.GR ｜ 抽样：边界 ｜ 组：accepted
- 摘要：Aggressively simplifying a generated high-poly building mesh to 0.5-1% of its faces confronts a hard limit. The surface looks complete, yet the mesh is topologically shattered: 10^3-10^4 connected components and non-manifold thin walls. Below a certain budget, every practical decimator "melts": it deletes parts, welds thin walls, or breaks the error tolerance. We attribute this to instance-specific pathology: which components are significant and where the cliff sits vary from mesh to mesh, so no single fixed algorithm suffices, and decimation becomes an iterative loop of cleaning, simplifying, and verifying. We present RemeshingAgent, an agent that turns this loop into a validated process. The melting follows from a triangle-budget decomposition into curvature, crease, component, and genus terms: below the component floor, no output satisfies the repair contract, and cleaning first is the theory-mandated response. At a 0.5% budget the agent stays topology-clean where QEM and vertex clustering melt, matches a commercial remesher on 20 unseen city buildings, and on the 24 training buildings a nine-participant single-workstation blind study prefers our outputs 168:48 (p = 0.0195, subj
- 链接：https://arxiv.org/abs/2611.20533
- 你在窄口径(q1)下判的是：**0**
- **判定：** （填 1 / 0 / ?）
- 摘要是否足够： （是 / 否 —— 填「否」表示必须看全文才敢定）

### 10 · 2611.20797 · Correspondence-Free Camera Pose Estimation by Matching Moments

- 类别：cs.CV ｜ 抽样：边界 ｜ 组：accepted
- 摘要：The blind perspective-$n$-point (PnP) problem is to estimate the pose of a calibrated camera from 2D and 3D point sets with unknown correspondences. We show that, for complete, noiseless observations, fourteen permutation-invariant image moments up to order four identify a fixed camera pose for almost every 3D point set containing at least twenty points. Our learning-free method, MomentPnP, matches these moments between the observed 2D points and the projected 3D points to initialize a camera pose without correspondences and refines the pose and correspondence weights using expectation--maximization. Across the test sets of three benchmarks, our method reduces median rotation error by $5$--$170\times$ relative to the best learned baseline, both with and without outliers. We recover accurate poses even with as many outliers as inliers. On dense ETH3D scans, pose accuracy improves as the point sets grow, even as individual correspondences become harder to resolve.
- 链接：https://arxiv.org/abs/2611.20797
- 你在窄口径(q1)下判的是：**0**
- **判定：** （填 1 / 0 / ?）
- 摘要是否足够： （是 / 否 —— 填「否」表示必须看全文才敢定）

### 11 · 2611.21143 · WinDEX: Metric 3D Hand Motion Reconstruction in the Wild for Dexterous Teleoperation and Policy Learning

- 类别：cs.RO ｜ 抽样：随机 ｜ 组：accepted
- 摘要：Human manipulation data are widely used to train robots for human-like dexterity. However, low-cost, large-scale collection in the wild remains challenging. Existing methods remain limited in geometrically grounded metric-scale reconstruction, real-world generalization and inference speed. We present WinDEX, integrating (1) geometric-temporal optimization for metric 3D hand annotation from in-the-wild egocentric stereo videos, combined with visual-inertial SLAM for world-frame reconstruction; (2) WinDEX-Net, an end-to-end, fisheye-native network combining calibrated stereo, local detail and temporal context, with a data-model flywheel of model-assisted annotation and retraining; (3) distilled models for offline reconstruction and causal streaming, supporting reinforcement learning and teleoperation; and (4) low-cost CyberCap stereo-inertial capture, forming the WinDEX-Hand dataset with 1,000 hours of training annotations and held-out human-annotated in-the-wild 2D and independent optical motion-capture evaluation sets. Offline reconstruction runs at 43.61 FPS and causal streaming at 171 FPS. On held-out data, offline reconstruction achieves state-of-the-art accuracy: 14.5 pixels in
- 链接：https://arxiv.org/abs/2611.21143
- 你在窄口径(q1)下判的是：**1**
- **判定：** （填 1 / 0 / ?）
- 摘要是否足够： （是 / 否 —— 填「否」表示必须看全文才敢定）

### 12 · 2611.20950 · ROSE: A Shared Cross-Embodiment Facial-Motion Latent Space for Humanoid Robot Expression

- 类别：cs.RO ｜ 抽样：随机 ｜ 组：accepted
- 摘要：Natural, coherent full-face dynamic expressions are central to making humanoid robots socially approachable, yet existing systems commonly realize only limited lip motion or scripted expressions. The limitation is both physical and algorithmic. A compact head leaves little room for densely packed, independently controllable actuation; meanwhile, learned systems often generate an avatar video, landmarks, or facial parameters and then infer actuator commands through visual retargeting. This render-and-invert path adds latency and artifacts, and it does not reliably transfer generated behavior to a physical robot. We present ROSE (RObot facial expression through Shared motion Embeddings), a framework that integrates biomimetic hardware, cross-embodiment motion representation learning, and multimodal motion generation. On the hardware side, we build a flexible tendon-sheath transmission structure that integrates 34 actuators into a 19.5 cm biomimetic head. By decoupling actuator placement from facial action points, it enables coordinated full-face expression within a compact volume. On the algorithmic side, ROSE-VAE learns an identity-independent shared facial-motion latent space from
- 链接：https://arxiv.org/abs/2611.20950
- 你在窄口径(q1)下判的是：**0**
- **判定：** （填 1 / 0 / ?）
- 摘要是否足够： （是 / 否 —— 填「否」表示必须看全文才敢定）

### 13 · 2611.21485 · Lost in the Hallway: Benchmarking Persistent Spatial Memory Across Revisits

- 类别：cs.CV ｜ 抽样：随机 ｜ 组：accepted
- 摘要：Persistent spatial understanding is essential for embodied agents to operate reliably in environments they repeatedly encounter. It requires recognizing revisited places despite viewpoint changes, distinguishing them from similar-looking rooms, and updating memories as environments change. Yet existing evaluations often leave physical place identity across separated visits implicit. We introduce ReSpaceBench, a benchmark comprising 3,244 questions across 590 synthetic and real-home scenes, organized into 9 tasks spanning room association, persistent state tracking, and downstream reasoning. Controlled walkthroughs define visits by physical room entry and deliberately include same-type room distractors and cross-session object changes. Our evaluation of 32 models and 3 agentic video-understanding frameworks reveals substantial limitations: the strongest evaluated zero-shot model achieves 50.5% overall accuracy and 52.2% on a 450-question subset, compared with 90.1% for human annotators. The evaluated agentic frameworks offer no overall improvement over direct inference with the same base model. Analysis of agent execution traces reveals evidence omissions and incorrect cross-visit r
- 链接：https://arxiv.org/abs/2611.21485
- 你在窄口径(q1)下判的是：**0**
- **判定：** （填 1 / 0 / ?）
- 摘要是否足够： （是 / 否 —— 填「否」表示必须看全文才敢定）

### 14 · 2611.19096 · AdaptType: Accessible and Customizable Multimodal Text Entry in Virtual Reality for People with Upper-Body Motor Impairments

- 类别：cs.HC ｜ 抽样：随机 ｜ 组：accepted
- 摘要：Text entry in virtual reality (VR) is cumbersome, especially for people with upper-body motor impairments. Existing techniques often demand both fine and gross motor control, yet users' motor abilities vary widely. To address this range of needs, we present AdaptType, a multimodal VR text entry system that enables users to configure input techniques that best suit their abilities, and scaffolds customization through ability-based recommendations. Through a study with 10 participants, we found that customized multimodal techniques improved text entry speed compared to gaze- or hand-only techniques, and complemented voice for error correction, decreasing failure rate from 15.1% to 2.0%. We found that AdaptType yielded high text entry speed (36.26 WPM) and accuracy (0.36% error rate), with low task load and high usability ratings. We also found ability-based recommendations effectively scaffolded customization. Our work contributes more accessible and personalized VR text entry solutions for people with upper-body motor impairments.
- 链接：https://arxiv.org/abs/2611.19096
- 你在窄口径(q1)下判的是：**1**
- **判定：** （填 1 / 0 / ?）
- 摘要是否足够： （是 / 否 —— 填「否」表示必须看全文才敢定）

### 15 · 2611.18679 · Shared Mobile AR Without Depth Sensors from Monocular Point Maps

- 类别：cs.CV ｜ 抽样：随机 ｜ 组：accepted
- 摘要：Depth-aware augmented reality on phones needs dense geometry of the surrounding room. iPhones and iPads without LiDAR expose only sparse feature points and detected planes, and ARKit often takes tens of seconds to report the first wall. We describe a scan-free pipeline for these devices. A point-map network (MoGe-2) predicts metric geometry from each camera frame, the remaining depth shift is recovered from the camera intrinsics, and each frame's scale is aligned to views already in the map. A persistent voxel map with visibility-based expiry answers occlusion and collision queries. Co-located devices share one coordinate frame by solving yaw and floor-plane translation from sightings of each other. We evaluate the deployed system on 309 device-sessions from 19 device models without LiDAR, with 179 device-sessions from LiDAR phones in the same deployment as a reference population. A first dense depth map was recorded within 10 s in 80% of sessions, while ARKit had reported a wall plane by then in 25%. The median session scale was 0.98 against ARKit's wall planes and 1.00 against its camera translation. Scale changed by a median of 9% between nearby frames, against 0.4% with LiDAR,
- 链接：https://arxiv.org/abs/2611.18679
- 你在窄口径(q1)下判的是：**1**
- **判定：** （填 1 / 0 / ?）
- 摘要是否足够： （是 / 否 —— 填「否」表示必须看全文才敢定）

### 16 · 2611.18708 · TopSDF: Topological Signed Distance Field for High-Quality Triangle Mesh Extraction from 3D Gaussian Splatting

- 类别：cs.CV ｜ 抽样：随机 ｜ 组：accepted
- 摘要：Recent advances in 3D Gaussian Splatting (3DGS) have demonstrated its effectiveness for photorealistic novel view synthesis. However, extracting clean, watertight, explicit surface meshes from 3DGS remains a critical challenge. Previous methods approximate geometry via discrete Marching Tetrahedra, where each grid vertex is assigned a single scalar signed distance value. At complex geometric boundaries and thin structures, this suboptimal parameterization forces severe compromises across shared vertices, causing gradient collisions and geometric frustration. Furthermore, existing optimization objectives neglect element shape conditioning, producing degenerate triangles. We introduce TopSDF, a framework that models the signed distance state as a multivariate Gaussian random field. By learning latent topological covariances across tetrahedral vertices, our formulation expands local degrees of freedom for SDF estimates, allowing the candidate mesh vertices to be placed flexibly along the bipolar edges in the tetrahedra as driven by such topological correlation. Concurrently, we directly integrate variational meshing energies into the joint optimization, coupled with an energy-driven G
- 链接：https://arxiv.org/abs/2611.18708
- 你在窄口径(q1)下判的是：**0**
- **判定：** （填 1 / 0 / ?）
- 摘要是否足够： （是 / 否 —— 填「否」表示必须看全文才敢定）

### 17 · 2611.21383 · The Mask Is Not the Object: Volumetric Supervision for 3D Gaussian Segmentation

- 类别：cs.CV ｜ 抽样：随机 ｜ 组：accepted
- 摘要：3D Gaussian Splatting enables object-level operations on Gaussian primitives, yet existing segmentation methods are largely trained and evaluated through rendered views. This mismatch can produce accurate rendered masks from incomplete 3D selections since alpha-blended feature supervision concentrates learning on dominant contributors while leaving occluded or low-contribution Gaussians weakly supervised. We propose VODA, a plug-and-play supervision objective that exploits local depth structure to group per-pixel contributors and directly supervises all Gaussians in selected depth clusters, bypassing contribution-weighted gradient delivery. To evaluate volumetric completeness, we introduce Removal-3D, a synthetic object-removal benchmark, and the Removal Depth Error (RDE), a metric comparing predicted and ground-truth depth changes. Across four rendering-based baselines, VODA consistently improves volumetric segmentation on Removal-3D while maintaining or improving performance on LERF and ScanNet. Further analysis shows that VODA recovers lower-contribution Gaussians, while simple gradient reweighting and spatial propagation fail to reproduce comparable gains.
- 链接：https://arxiv.org/abs/2611.21383
- 你在窄口径(q1)下判的是：**0**
- **判定：** （填 1 / 0 / ?）
- 摘要是否足够： （是 / 否 —— 填「否」表示必须看全文才敢定）

### 18 · 2611.20546 · A Gaussian Primitive Data Management Framework for Efficient 3DGS Trajectory Rendering

- 类别：cs.DB ｜ 抽样：随机 ｜ 组：accepted
- 摘要：Trajectory rendering, which renders novel views of a reconstructed 3D scene along a camera path, is a core operation in digital twins and autonomous inspection. Structured 3D Gaussian Splatting (3DGS) renders a single view in real time by decoding sparse anchors into Gaussians on demand, but it renders a trajectory view by view: every view projects all anchors to select them, re-decodes anchors already requested by neighboring views, and runs all steps on the GPU while the CPU idles. We treat this as a spatial data management problem, where anchors are spatial objects, views are range queries, and decoded Gaussians are shared derived data, and propose GDM-GS, which removes redundancy at three levels. Within a view, an anchor index and an occluder index answer each view as a holed-frustum range query, so out-of-view and provably hidden anchors are never decoded. Across views, shared materialization decodes each requested anchor once per group of consecutive views while preserving each view's selection. Across processors, a hybrid pipeline balances selections between the CPU and the GPU before grouped decoding under bounded memory. Experiments on large-scale public scenes show that G
- 链接：https://arxiv.org/abs/2611.20546
- 你在窄口径(q1)下判的是：**0**
- **判定：** （填 1 / 0 / ?）
- 摘要是否足够： （是 / 否 —— 填「否」表示必须看全文才敢定）

### 19 · 2611.18822 · LongCat-Video-Avatar 1.6 Technical Report

- 类别：cs.CV ｜ 抽样：随机 ｜ 组：accepted
- 摘要：Recent advances in audio-driven avatar video generation have enabled increasingly realistic synthesis, yet achieving precise lip-audio synchronization, natural, human-like motion, and visual consistency over long sequences remains challenging. We present LongCat-Video-Avatar 1.6, which builds on LongCat-Video-Avatar 1.5 to improve expressive naturalness and reduce error accumulation during extended generation, e.g., exaggerated lip movements and overly red, temporally unstable lip coloration, enhance the naturalness of facial expressions and coordinated head and body movements. These improvements are driven by a refined post-training pipeline that integrates reinforcement learning, improved classifier-free guidance strategies for DMD-based few-step distillation, long-video rollouts, and on-policy distillation. Together, these refinements improve expressive realism and enable the generation of videos exceeding 10 minutes while maintaining visual quality and temporal consistency. Arena evaluations show that LongCat-Video-Avatar 1.6 outperforms its predecessor and competing commercial audio-driven avatar models, demonstrating the effectiveness of the improved post-training pipeline.
- 链接：https://arxiv.org/abs/2611.18822
- 你在窄口径(q1)下判的是：**0**
- **判定：** （填 1 / 0 / ?）
- 摘要是否足够： （是 / 否 —— 填「否」表示必须看全文才敢定）

### 20 · 2611.20245 · From XR Sketches to CAD: Preserving Design Intent with AI

- 类别：cs.HC ｜ 抽样：随机 ｜ 组：accepted
- 摘要：Extended reality (XR) allows designers to sketch shapes directly in 3D, but converting these sketches into editable, feature-based CAD requires interpreting their intent. A sketch may contain drawing errors, intended features, and design choices that remain open. Correcting every irregularity risks erasing intended features, while automatic completion may impose choices the designer has not made. We argue that AI should add precision without overriding design intent, considering both the resulting shape and how the CAD model behaves during later edits. To guide this process, we propose a conceptual framework that distinguishes errors from intentions in individual sketch properties and relates them to correction, preservation, and exploration in editable CAD. We also outline five research directions for sketch interpretation, CAD construction, and evaluation, with testable hypotheses for selected questions.
- 链接：https://arxiv.org/abs/2611.20245
- 你在窄口径(q1)下判的是：**1**
- **判定：** （填 1 / 0 / ?）
- 摘要是否足够： （是 / 否 —— 填「否」表示必须看全文才敢定）

### 21 · 2611.20076 · SGIP: Learning Scene-Grounded Interaction Priors for Scene-Aware Human Motion Prediction

- 类别：cs.CV ｜ 抽样：边界 ｜ 组：kw-missed
- 摘要：Human motion prediction (HMP) aims to forecast future movement from an observed motion sequence, and recent methods have incorporated 3D scene geometry and object semantics to improve long-term plausibility. However, the destination of future motion remains ambiguous in cluttered scenes: the same observed motion can lead to different interaction targets or navigation modes. Existing methods either handle this ambiguity implicitly or rely on auxiliary signals like gaze that are hard to obtain in practice. To address this, we propose SGIP, which explicitly predicts where in the scene future motion will be grounded across both objects and open navigation regions, and uses it to condition future trajectory and full-body pose prediction. This scene-grounded interaction prior is learned via intent distillation: at training time only, a teacher model scores candidate scene regions by combining an LLM prompted with a textual description of the person's intent with geometric motion-scene features. A student model learns to reproduce these scores from only the observed motion and 3D scene, making intent and LLM unnecessary at test time. Across multiple benchmark datasets, SGIP outperforms pr
- 链接：https://arxiv.org/abs/2611.20076
- 你在窄口径(q1)下判的是：**0**
- **判定：** （填 1 / 0 / ?）
- 摘要是否足够： （是 / 否 —— 填「否」表示必须看全文才敢定）

### 22 · 2611.21596 · SADL: On the Demand-Supply Geometry of Representation Collapse

- 类别：cs.RO ｜ 抽样：边界 ｜ 组：kw-missed
- 摘要：In Joint-Embedding Predictive Architectures (JEPAs), a well-constrained projector output does not by itself prevent representation collapse. We find that, from initialization, the encoder representation is dominated by a component shared by different inputs. A batch-normalized projector removes this component, so regularization after the projector cannot correct it, and the differences between representations shrink until they collapse. We propose SADL (Supply And Demand Loss), which keeps the original training objective and constrains the encoder directly when needed. SADL compares the representation differences that the projector output demands with the differences the encoder can retain and pass on to the projector, and adds a constraint on the encoder only when supply falls short of demand. It works with different Demand Regularizers and introduces no auxiliary networks, additional trainable parameters, or architectural changes. In single-task and jointly trained four-task LeWorldModel (LeWM) and INTACT experiments, SADL lowers the collapse rate over ten random seeds from 50% to 0%. After one epoch of training, encoder effective rank is 3.4-6.4 times that of the corresponding b
- 链接：https://arxiv.org/abs/2611.21596
- 你在窄口径(q1)下判的是：**0**
- **判定：** （填 1 / 0 / ?）
- 摘要是否足够： （是 / 否 —— 填「否」表示必须看全文才敢定）

### 23 · 2611.21577 · When Tool Names Are Not Identities: Measuring Provider Misbinding in MCP-Based AI Agents

- 类别：cs.CR ｜ 抽样：边界 ｜ 组：kw-missed
- 摘要：Large language model (LLM) applications increasingly act as agents that select and invoke external tools. The Model Context Protocol (MCP) standardizes this interaction by allowing clients to compose tools advertised by multiple servers. However, tool metadata used for discovery and selection is not, by itself, necessarily bound to a verified provider identity. This paper studies this gap as tool-provider misbinding: a failure in which a request intended for a legitimate provider is instead resolved to an attacker-controlled tool. The attacker does not compromise the host, LLM, legitimate server, or network channel; it only operates another MCP server that advertises tools with chosen metadata. We formulate tool provider misbinding as an attacker-controlled tool-selection optimization problem and evaluate it in a controlled MCP environment across five LLM-based clients. The results show that interactions drive misbinding. The strongest failures occur when exact-name collision, task-aligned description, and compatible schema reinforce one another, but authority-enhanced descriptions with compatible schema can also cause wrong-provider execution or unresolved provider ambiguity witho
- 链接：https://arxiv.org/abs/2611.21577
- 你在窄口径(q1)下判的是：**0**
- **判定：** （填 1 / 0 / ?）
- 摘要是否足够： （是 / 否 —— 填「否」表示必须看全文才敢定）

### 24 · 2611.21507 · GHySSeg: Real-Time Geometric Ground and Road Segmentation for Hybrid Solid-State LiDAR

- 类别：cs.RO ｜ 抽样：边界 ｜ 组：kw-missed
- 摘要：Hybrid solid-state LiDAR sensors are making their way into production vehicles, yet the data they produce differs structurally from that of the established spinning mechanical sensors behind today's autonomous-driving datasets: it is ring-free, dense, cluttered, and concentrated in a frontal field of view. The classical geometric methods that autonomous vehicles rely on for drivable space computation and navigation assume the ordered ring-and-column structure of a 360-degree spinning LiDAR and degrade or fail on this data, while learned alternatives are computationally heavy, hard to certify, and trained almost exclusively on spinning-LiDAR data. We demonstrate that the same dense, per-curve geometry is instead an opportunity to close the divide between the industry's preferred sensors and autonomous-driving research. We present GHySSeg, a purely geometric method that segments ground and drivable road from a single hybrid solid-state LiDAR frame by tracing each scan curve and reading two geometric signatures, a step in height and a fold-back in range, with no training and no graphics processing unit. To evaluate it, we release HySoLiD-Drive, the first public benchmark dedicated to
- 链接：https://arxiv.org/abs/2611.21507
- 你在窄口径(q1)下判的是：**0**
- **判定：** （填 1 / 0 / ?）
- 摘要是否足够： （是 / 否 —— 填「否」表示必须看全文才敢定）

### 25 · 2611.21456 · Expertise capture in workplace AI

- 类别：cs.CR ｜ 抽样：边界 ｜ 组：kw-missed
- 摘要：AI assistants are becoming part of how knowledge workers think and perform, accumulating the prompts, exemplars, memory and interaction histories that encode a worker's professional judgment. This infrastructure typically runs under employer or platform control. We name the resulting process expertise capture, the absorption of worker-applied knowledge and judgment into AI resources under organizational control. We develop a framework of contribution forms, technical residences and transformation families, and show that how far a contribution can be attributed, separated and revoked depends on where it resides and how it has been transformed, properties fixed by system design long before any dispute arises. When a worker departs, the organization retains a capability shaped by their judgment while the worker loses access to it, and the asymmetry compounds as contributions move from inspectable artifacts into derivatives, learned components and successor systems. We outline three measures, write-time provenance, extraction of separable contributions and an executable exit procedure, that make an agreed allocation technically performable, and make explicit what cannot be separated at
- 链接：https://arxiv.org/abs/2611.21456
- 你在窄口径(q1)下判的是：**0**
- **判定：** （填 1 / 0 / ?）
- 摘要是否足够： （是 / 否 —— 填「否」表示必须看全文才敢定）

### 26 · 2611.21449 · Replicating and Extending Weight-Space Programming: Frontier LLMs Compile Programs into Weights and Read Input Layers

- 类别：cs.CL ｜ 抽样：边界 ｜ 组：kw-missed
- 摘要：Researchers at MIT recently reported that GPT-6 Astra, a frontier large language model (LLM), can write the weights of small neural networks directly in a single reply, and can read the raw weights of small networks to say what they were trained to do. In a three-day sprint, we replicated and extended these results. Our four findings: (1) Writing weights reproduces. Astra's networks for the game Breakout scored 514, 550 and 307 (versus MIT's 517), and scored just as well on two modified versions of Breakout. Claude Opus 5.5 can also write working networks, but often runs out of output tokens. (2) What is new is translating programs into weights. Earlier models could write a good policy as code a generation before they could write network weights, and the networks the models write behave like compiled programs: two models independently decompiled Astra's Breakout network into Python matching its actions in all tested states. On classifying handwritten digits, Astra's networks scored 50% on average, below a simple classifier (82%). (3) Reading weights is mostly reading the input layer. Astra and Opus 5.5 identify which game a network plays almost perfectly, but on three new games we
- 链接：https://arxiv.org/abs/2611.21449
- 你在窄口径(q1)下判的是：**0**
- **判定：** （填 1 / 0 / ?）
- 摘要是否足够： （是 / 否 —— 填「否」表示必须看全文才敢定）

### 27 · 2611.21439 · A Reinforcement Learning Method to Navigate SMEFT Operator Space

- 类别：cs.LG ｜ 抽样：边界 ｜ 组：kw-missed
- 摘要：In particle physics, discrepancies between experimental measurements and Standard Model (SM) predictions are commonly interpreted within new theoretical models. In this context, the Standard Model Effective Field Theory (SMEFT) provides a general framework encompassing a broad class of models. However, exploring the enormous space of possible SMEFT operators rapidly becomes a challenging combinatorial problem: many operators can contribute simultaneously to different observables, their effects are correlated, and distinct operator combinations can provide comparably good descriptions of the data. In this work, we formulate the exploration of the SMEFT operator space as a sequential decision-making problem using reinforcement learning (RL). Our RL agent employs a lightweight actor-critic architecture with approximately 40K trainable parameters in total. Rather than searching for a single best-fit theory, our method is designed to discover a diverse set of high-quality theory hypotheses. We test the method in a complex phenomenological environment comprising 132 observables across several sectors of particle physics, including 24 measurements that deviate from their SM predictions by
- 链接：https://arxiv.org/abs/2611.21439
- 你在窄口径(q1)下判的是：**0**
- **判定：** （填 1 / 0 / ?）
- 摘要是否足够： （是 / 否 —— 填「否」表示必须看全文才敢定）

### 28 · 2611.21408 · Do Embedding-Map Distances Guide LLM Ideation? Four Tests Against What Came Next

- 类别：cs.LG ｜ 抽样：边界 ｜ 组：kw-missed
- 摘要：A popular ideation recipe treats an embedding map of existing work as a guide: pick points far from everything and decode them into ideas. I test four ways such distances could guide ideation against what appeared later. (1) Far random directions are not text: no later item reaches a raw cosine above about 0.10 with one (after centring or whitening, 22 of 24 cells stay out of reach), and an LLM decoder shown a target's neighbours, with score-only feedback, writes those neighbours in all six target sets. A neighbour-free search writes coherent text at median cosine 0.57 and 0.47 to interior gaps, beating the nearest existing item on 15 and 14 of 20, but only 0.07 and 0.06 to far points. (2) On k-means cells of a past-only map, the registered hole score mostly tracks cell size and position; three density-based gap scores forecast which cells grow fastest at or below chance (AUC 0.30 to 0.66) and add nothing to momentum in Steam and arXiv, with patents inconclusive; more isolated new Steam games are slightly better reviewed. (3) LLM continuations of arXiv papers stay closer to the source than papers that cite it, under three user prompts and against proposal rewrites (gpt-4o) and Apri
- 链接：https://arxiv.org/abs/2611.21408
- 你在窄口径(q1)下判的是：**0**
- **判定：** （填 1 / 0 / ?）
- 摘要是否足够： （是 / 否 —— 填「否」表示必须看全文才敢定）

### 29 · 2611.21407 · Harness Leverage Across Model Size: A Ladder of Five Local Agent Harnesses from 0.75B to 4.7B

- 类别：cs.AI ｜ 抽样：边界 ｜ 组：kw-missed
- 摘要：A harness turns a model into a system that completes tasks: it builds the prompt, exposes tools and decides when work is done. Harness comparisons hold the model fixed. Model comparisons hold the harness fixed. We vary both: five shipped harnesses, 18 artifact-producing tasks, four locally deployable open-weight models from 0.75B to 4.7B and a 35.5B anchor, with one deterministic checker scoring all 360 ladder cells. The completion-controlling harness, Mingbird, has the highest mean at every size. Of four pre-registered paired contrasts, two survive Holm correction, at 0.75B and 4.7B. Thirteen of sixteen paired intervals exclude zero under the deployment reading, with leads from 0.075 over the strongest rival to 0.819 over the weakest. The completion gate is not the carrier: disabling all six executable checks moves the mean by +0.080, +0.117, +0.003 and -0.004, every interval including zero, and only at 1.9B does disabling it create empty runs. Removing one repeat-blocking rule alone costs 0.411 at 0.75B and leaves eight of eighteen tasks with no artifact. The harness effect is a progress effect: it decides whether a run leaves anything on disk. Of 357 usable cells, 127 leave none
- 链接：https://arxiv.org/abs/2611.21407
- 你在窄口径(q1)下判的是：**0**
- **判定：** （填 1 / 0 / ?）
- 摘要是否足够： （是 / 否 —— 填「否」表示必须看全文才敢定）

### 30 · 2611.21403 · Portrait Fitness as a Pretext: Probing Implicit Demographic Bias in VLMs

- 类别：cs.CV ｜ 抽样：边界 ｜ 组：kw-missed
- 摘要：We audit face-related bias in VLMs using BALPORTRAITS, a new balanced dataset of 9,000 fictional portraits across ethnicity, gender, and age segments. Sixteen VLMs estimate portrait fitness scores for occupations, brands, activities, and banking or insurance products within an advertising-casting framework designed to avoid direct inference of protected attributes. Item-level estimations are aggregated with scenario-specific prestige scores to compare rankings across demographic groups. While the magnitude and direction of these biases vary across scenarios, model families, and demographic dimensions, with age, ethnicity, and gender contributing differently depending on the task, we find demographic dispersion across all evaluated models, with a majority of pairwise segment differences reaching statistical significance. This study introduces a controlled protocol to assess implicit face-related associations and demonstrates that single-scenario or single-attribute audits are insufficient.
- 链接：https://arxiv.org/abs/2611.21403
- 你在窄口径(q1)下判的是：**0**
- **判定：** （填 1 / 0 / ?）
- 摘要是否足够： （是 / 否 —— 填「否」表示必须看全文才敢定）

### 31 · 2611.20745 · A Seismic Foundation Model for Dense Feature Extraction

- 类别：cs.CV ｜ 抽样：随机 ｜ 组：kw-missed
- 摘要：Deep-learning-based seismic interpretation is constrained by scarce high-quality annotations, and most existing models are trained separately for individual tasks. We present SeisDFE, a 7B-parameter seismic foundation model for dense feature extraction, pretrained on 5.34 million 2D images derived from more than 500 seismic volumes. A three-stage pretraining strategy, combining discriminative self-supervised learning, Gram feature anchoring, and multi-resolution adaptation, improves feature discriminability while preserving spatial coherence. With its encoder frozen, SeisDFE supports seismic facies classification, salt detection, fault detection, and relative geologic time estimation. It outperforms existing seismic foundation models on all four tasks and a natural-image-pretrained model on all but fault detection, with the largest gains under scarce supervision: using only two annotated sections of the F3 dataset, it improves whole-volume mIoU by 12-19 percentage points over the baselines. The learned features remain effective with task-specific decoders and extend to synthetic-to-field transfer and sparse 3D geobody interpretation. These results show that large-scale seismic pret
- 链接：https://arxiv.org/abs/2611.20745
- 你在窄口径(q1)下判的是：**0**
- **判定：** （填 1 / 0 / ?）
- 摘要是否足够： （是 / 否 —— 填「否」表示必须看全文才敢定）

### 32 · 2611.20840 · Interpretable deep concepts of organoid morphology

- 类别：cs.CV ｜ 抽样：随机 ｜ 组：kw-missed
- 摘要：Image-based classification of organoid morphologies can indicate drug response, viability, or successful differentiation. In recent work, learned representations outperform handcrafted features as the basis for downstream classifiers. However, their black-box nature hides the morphological cues a classifier relies on. Based on the foundation models DINOv3 (general-purpose) and ViTAMIn-O (organoid-specific), we train sparse autoencoders (SAEs) to learn interpretable concepts related to distinct organoid morphologies. We annotate concepts with spatial labels (organoid, organoid wall, background) and compute their dataset specificity and task relevance across five tasks. The spatial labels of DINOv3 concepts yield coarse organoid segmentations on out-of-domain datasets. Filtering concepts by spatial label in the DINOv3-SAE improves downstream AUROC for three of the five tasks. Qualitative analysis of the most relevant concepts further reveals a confounding factor introduced by our preprocessing in one task. Through such insights, interpretable concepts could help improve the reliability of classifiers and guide the future development of organoid representation models. The trained SAEs
- 链接：https://arxiv.org/abs/2611.20840
- 你在窄口径(q1)下判的是：**0**
- **判定：** （填 1 / 0 / ?）
- 摘要是否足够： （是 / 否 —— 填「否」表示必须看全文才敢定）

### 33 · 2611.19227 · Can an Agent Rethink What It Knows? Selective Scene Memory Updates in a Changing World

- 类别：cs.AI ｜ 抽样：随机 ｜ 组：kw-missed
- 摘要：Task configurations in factories, warehouses, and everyday physical environments change over time. Physical AI systems therefore need to incorporate new facts into scene memory while preserving valid information about equipment, objects, and operating constraints. We study updates to this parametric semantic-memory layer and present a joint evaluation of correction and preservation under finite update budgets. At fixed current fact count and memory parameter count, the protocol combines independent single-fact updates, budget trajectories, old-to-new answer diagnostics, and first stable success. Using a frozen 4B language model with late-layer LoRA, we evaluate seven preparation conditions and six update budgets on four-field synthetic semantic configurations. In two exposure-matched history conditions, increasing the budget from eight to 32 updates raises joint success from 6.25% to 94.79% and 91.15%, respectively, while exact obsolete-value outputs fall from 174/192 and 166/192 to zero. Constant32, which matches preparation steps but repeatedly trains on unchanged content during the first 32 events, achieves higher early joint success at eight steps (53.65%); at 32 steps, it reac
- 链接：https://arxiv.org/abs/2611.19227
- 你在窄口径(q1)下判的是：**0**
- **判定：** （填 1 / 0 / ?）
- 摘要是否足够： （是 / 否 —— 填「否」表示必须看全文才敢定）

### 34 · 2611.19756 · Drift-Conditioned Structural Replay for Continual Cardiac Ultrasound Segmentation

- 类别：cs.CV ｜ 抽样：随机 ｜ 组：kw-missed
- 摘要：Conventional experience replay typically applies fixed preservation constraints to historical exemplars, overlooking variations in how learned representations, predictions, and anatomical structures change during sequential training. To address this limitation, we propose Drift-Conditioned Structural Replay Loss (DCSRL), an exemplar-adaptive supervision mechanism that regulates anatomical preservation according to source-referenced knowledge drift. DCSRL operates within a reliability-guided replay framework that selects informative historical exemplars using anatomical content and boundary characteristics while adaptively regulating replay during training. For each retained exemplar, DCSRL constructs a frozen source-task reference signature and subsequently measures changes in feature representations, class probabilities, boundary responses, and predicted anatomical structures. These complementary drift measurements are aggregated and normalized to generate bounded, exemplar-specific coefficients that dynamically adjust boundary and structural replay losses without modifying the underlying memory-selection policy. We evaluate DCSRL under sequential learning across CAMUS, CardiacNet
- 链接：https://arxiv.org/abs/2611.19756
- 你在窄口径(q1)下判的是：**0**
- **判定：** （填 1 / 0 / ?）
- 摘要是否足够： （是 / 否 —— 填「否」表示必须看全文才敢定）

### 35 · 2611.19495 · Vegetation Health Classification for Low-Data and Edge Hardware Deployment

- 类别：cs.CV ｜ 抽样：随机 ｜ 组：kw-missed
- 摘要：Unmanned aerial vehicles (UAVs) equipped with cameras are popular, viable tools for vegetation and environmental health monitoring. However, existing image classification methods are incompatible with UAV implementation for independent practitioners in remote, resource-constrained environments due to large dataset requirements, GPU hardware, inflexible retraining, and low interpretability. This paper presents a lightweight, interpretable vegetation classification algorithm operating with as few as five reference images per class, without GPUs or heavy machine learning frameworks. It uses a 2D hue-saturation histogram feature representation and Earth Mover's Distance or Quadratic Form Distance, paired with a log-likelihood probability score, to classify images into three vegetation health categories. We evaluated six systems: three custom pipelines and three established models across low-data scenarios ($n = 5, 10, 25$) and a full-data regime of 2,172 drone images from 28 South American locations. Our custom pipelines achieve competitive Top-1 accuracy (81--85\%) under low-data constraints, maintaining sub-1ms inference times that enable real-time classification and subsequently tas
- 链接：https://arxiv.org/abs/2611.19495
- 你在窄口径(q1)下判的是：**0**
- **判定：** （填 1 / 0 / ?）
- 摘要是否足够： （是 / 否 —— 填「否」表示必须看全文才敢定）

### 36 · 2611.19670 · Architecting the Corporate AI Infrastructure: The Evolving Roles of AI Governance Committees and Chief Ethics Officers

- 类别：cs.CY ｜ 抽样：随机 ｜ 组：kw-missed
- 摘要：The accelerating integration of artificial intelligence (AI) into core business operations has created an urgent need for robust corporate governance infrastructures capable of managing complex ethical, legal, and operational risks. While organizations have increasingly adopted high-level AI ethics principles, a critical implementation gap persists: fewer than half of organizations that cite AI governance as a boardroom priority have a formalized governance framework in place. This paper addresses that gap by proposing a structured corporate AI governance architecture (CAIGA) centred on two mutually reinforcing pillars. First, it examines the evolving mandate of specialized C-suite roles, specifically Chief Privacy Officers (CPOs) and Chief Ethics Officers (ChEOs), in formalizing accountability for AI usage across the enterprise. Second, it argues that cross-functional AI Governance Committees, uniting representatives from legal, technology, data science, cybersecurity, and business units, are the essential organizational mechanism for translating ethical principles into operational decisions, including strategic go/no-go approvals for new AI initiatives. Drawing on a conceptual re
- 链接：https://arxiv.org/abs/2611.19670
- 你在窄口径(q1)下判的是：**0**
- **判定：** （填 1 / 0 / ?）
- 摘要是否足够： （是 / 否 —— 填「否」表示必须看全文才敢定）

### 37 · 2611.20983 · GRACE: Parallel Best-of-N Multi-Agent Analysis of Closed-Form Questions over Dataframes with Guardrail Selection and Adaptive Retry

- 类别：cs.AI ｜ 抽样：随机 ｜ 组：kw-missed
- 摘要：LLM agents answer closed-form questions over a tabular dataframe by writing and executing Python, almost always as a single rollout: one interpretation, one script, one result, accepted without comparison. The few pipelines that produce several candidates reconcile them by answer-agreement voting, which needs a single comparable scalar and always returns one, even when every candidate is wrong. We present GRACE (Generative, Ranked, Adaptive Code Ensemble), a production-oriented pipeline that instead runs parallel best-of-N selection specialised to dataframe code. N agents run concurrently under a strict, machine-checkable output contract, diversified by persona hints, per-retry rotation, and a two-regime temperature schedule. Rather than vote, GRACE judges the executed artefacts: a pairwise tournament pre-filters the pool and a domain-specialised guardrail either selects the best candidate or, when none is defensible, rejects the whole pool and abstains with a diagnosis (an option voting structurally lacks), which in turn drives an adaptive retry with per-agent feedback. On InfiAgent-DABench (DAEval, M = 246), using Qwen3.6-35B-A3B as the backbone, GRACE raises answer match from 39
- 链接：https://arxiv.org/abs/2611.20983
- 你在窄口径(q1)下判的是：**0**
- **判定：** （填 1 / 0 / ?）
- 摘要是否足够： （是 / 否 —— 填「否」表示必须看全文才敢定）

### 38 · 2611.18623 · Evaluating the Robustness of Fact-Checking LLMs on Multilingual Evidence

- 类别：cs.CL ｜ 抽样：随机 ｜ 组：kw-missed
- 摘要：Automated fact-checking benchmarks typically pair claims with clean, curated evidence in high-resource languages, but real-world evidence is often incomplete, misleading, or written in a language where models are weaker. We evaluate the robustness of fact-checking LLMs for different languages. Building on EuroVerdict, we construct gold evidence sets for 190 claims in each of English, German, Greek, and Romanian, then apply four corruption strategies at two severity levels. We test LLMs on a set of claims, providing them with evidence from the sets above. A rubric-based LLM-as-a-judge scores reasoning quality. Verdict accuracy proves highly sensitive to both factors: Misleading edit cut Llama 3.1 8B's English accuracy from 80.00% to 16.84%, and losses widen as language resource level decreases. Machine-translating Greek and Romanian claims into English recovers much, but not all, of the low-resource gap. Judge scores decline more slowly than accuracy, suggesting that automated reasoning evaluation underestimates degradation. These results caution against deploying LLM fact-checkers on noisy multilingual evidence, and we release our evidence datasets and evaluation code to support fu
- 链接：https://arxiv.org/abs/2611.18623
- 你在窄口径(q1)下判的是：**0**
- **判定：** （填 1 / 0 / ?）
- 摘要是否足够： （是 / 否 —— 填「否」表示必须看全文才敢定）

### 39 · 2611.20926 · Advancing Cognitive Pairwise Comparisons for Human-Centric Artificial Intelligence and Data Science: A Human-in-the-Loop Framework

- 类别：cs.AI ｜ 抽样：随机 ｜ 组：kw-missed
- 摘要：Human-centric artificial intelligence and data science (HCAD) systems increasingly involve human-in-the-loop (HITL) interventions to overcome the limitations of fully automated machine learning algorithms, such as automation bias and the inability to incorporate tacit domain knowledge, and continuously improve predictive performance. Data transformations, feature selection, feature weighting, and model selection usually require laborious human involvement across iterations of artificial intelligence and data science (AI&DS) pipelines, making development a challenging and time-consuming process. The Cognitive Pairwise Comparison (CPC) framework is proposed as a human-centric methodology to elicit preferences and priorities in a structured format. To establish essential facets of human-centricity, this research advances the CPC methodology so that user preference elicitation can be systematically quantified in these challenging AI&DS tasks. To demonstrate the usability and validity of these facets, this study presents several applications within movie recommender systems using the MovieLens dataset. It exemplifies how the extended CPC framework can facilitate interactions between hum
- 链接：https://arxiv.org/abs/2611.20926
- 你在窄口径(q1)下判的是：**0**
- **判定：** （填 1 / 0 / ?）
- 摘要是否足够： （是 / 否 —— 填「否」表示必须看全文才敢定）

### 40 · 2611.20461 · LiveView: Real-Time Camera-Controlled Re-filming of Streaming Videos

- 类别：cs.CV ｜ 抽样：随机 ｜ 组：kw-missed
- 摘要：Real-time camera-controlled video re-filming aims to synthesize target views from a streaming source video under online user-specified camera trajectories. This task poses two key challenges: maintaining synchronization and content consistency across views, and achieving low-latency rendering with long-horizon stability. Existing approaches are predominantly designed for offline full-sequence processing and rely on bidirectional attention or costly depth-based geometric preprocessing, making them unsuitable for low-latency streaming scenarios. To address these limitations, we develop a teacher-to-student framework that distills a high-fidelity bidirectional re-filming teacher into a few-step causal autoregressive student. We introduce Cross-Frame Injection to interleave each incoming source frame with its synchronized target latent, thereby establishing direct cross-view correspondence and improving content consistency. To ensure stable long-horizon generation, we further propose Shared Relative RoPE, which bounds temporal indices within the pretrained range, and Cycle Streaming Tuning, which exposes the student to extended cyclic trajectories during streaming training. These desig
- 链接：https://arxiv.org/abs/2611.20461
- 你在窄口径(q1)下判的是：**0**
- **判定：** （填 1 / 0 / ?）
- 摘要是否足够： （是 / 否 —— 填「否」表示必须看全文才敢定）

---

> 共 40 条。填完后：`python scripts/decision_probe.py ingest 1118 data/decision/labeling_1118.md`

