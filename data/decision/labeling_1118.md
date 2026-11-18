# 判定标注表 1118（问题版本 q1-2026-11-18）

## 判定规则（按规则判，不按感觉判）

- **判 1（相关）**：论文的研究对象、被评估场景、硬件或用户任务中，**至少有一项属于**沉浸式/空间场景（头显、AR/VR 应用、空间交互、沉浸式内容与渲染、化身、触觉/遥操作、XR 系统与评估）。
- **判 0（不相关）**：仅为通用视觉/图形/机器人方法，XR 只是**可能的迁移方向**而非论文的研究对象或评估场景。
- **判 ?（不确定）**：两条规则都能说得通，或摘要信息不足以判断。**宁可标 ?，不要猜**——? 会从分母里剔除，不影响指标；猜错会污染基线。

## 必读

- 「预判」列是我用关键词密度挑的，**不是答案**；`边界` 项是关键词分不开的，`随机` 项用于防止选择偏差。
- 只需在最后一列填 `1` / `0` / `?`，其余不要动；填完告诉我，我用 `ingest` 回写。

| # | arXiv | 题目 | 摘要首句 | 预判 | 你的判定 |
|---:|---|---|---|---|---|
| 1 | 2605.09586 | DeformMaster: An Interactive Physics-Neural World Model for Deformable Objects from Videos | World models for deformable objects should recover not only geometry and appearance, but also underlying physical dynamics, interaction grounding, and | 边界 |  |
| 2 | 2611.18267 | TetraCoder: Adaptive Tetrahedral Encoding for Neural Fields | Implicit and explicit representations of geometry are central in computer graphics applications and come with their pros and cons. | 边界 |  |
| 3 | 2611.18734 | Is It Still There? Place-Registered Verification Makes VLMs Reliable Scene-Change Detectors | A robot that returns to a space must tell which objects were added, removed or moved since its last visit, while its trajectory, viewpoints and lighti | 边界 |  |
| 4 | 2611.18894 | CISyn: Human Mesh Recovery in Close Interactions with Physics-Simulated Synthetic Data | 3D human mesh recovery (HMR) in close-interaction scenarios is hindered by the lack of large-scale, accurately annotated training data: real capture i | 边界 |  |
| 5 | 2611.18979 | Probing Where Surprise Happens: Localized Violation-of-Expectation Evaluation of Video World Models | Violation-of-expectation (VOE) benchmarks evaluate intuitive physics in video world models by testing whether physically impossible events produce gre | 边界 |  |
| 6 | 2611.19095 | DEFDVO: Deformable Deep Visual Odometry for Equirectangular Images | Omnidirectional ($360^\circ$) cameras capture the full surrounding scene in every frame, providing a strong advantage for visual odometry (VO) over pi | 边界 |  |
| 7 | 2611.19803 | Pros4D: Modeling Evolving 4D Worlds in Latent Space for Dynamic Spatial Reasoning | Dynamic spatial reasoning from monocular video enables vision-language models (VLMs) to understand how 3D environments evolve over time, supporting ph | 边界 |  |
| 8 | 2611.20196 | DoF-Query Transformer for Adaptive Fusion of Egocentric Vision and Forearm HD-sEMG in Continuous Hand Kinemati | Continuous and accurate estimation of human hand kinematics is important not only for intuitive human-machine interaction, but also for capturing fine | 边界 |  |
| 9 | 2611.20533 | RemeshingAgent: Self-Evolving Agent for Repair-Based Decimation of Generated Building Meshes | Aggressively simplifying a generated high-poly building mesh to 0.5-1% of its faces confronts a hard limit. | 边界 |  |
| 10 | 2611.20797 | Correspondence-Free Camera Pose Estimation by Matching Moments | The blind perspective-$n$-point (PnP) problem is to estimate the pose of a calibrated camera from 2D and 3D point sets with unknown correspondences. | 边界 |  |
| 11 | 2611.21143 | WinDEX: Metric 3D Hand Motion Reconstruction in the Wild for Dexterous Teleoperation and Policy Learning | Human manipulation data are widely used to train robots for human-like dexterity. | 随机 |  |
| 12 | 2611.20950 | ROSE: A Shared Cross-Embodiment Facial-Motion Latent Space for Humanoid Robot Expression | Natural, coherent full-face dynamic expressions are central to making humanoid robots socially approachable, yet existing systems commonly realize onl | 随机 |  |
| 13 | 2611.21485 | Lost in the Hallway: Benchmarking Persistent Spatial Memory Across Revisits | Persistent spatial understanding is essential for embodied agents to operate reliably in environments they repeatedly encounter. | 随机 |  |
| 14 | 2611.19096 | AdaptType: Accessible and Customizable Multimodal Text Entry in Virtual Reality for People with Upper-Body Mot | Text entry in virtual reality (VR) is cumbersome, especially for people with upper-body motor impairments. | 随机 |  |
| 15 | 2611.18679 | Shared Mobile AR Without Depth Sensors from Monocular Point Maps | Depth-aware augmented reality on phones needs dense geometry of the surrounding room. | 随机 |  |
| 16 | 2611.18708 | TopSDF: Topological Signed Distance Field for High-Quality Triangle Mesh Extraction from 3D Gaussian Splatting | Recent advances in 3D Gaussian Splatting (3DGS) have demonstrated its effectiveness for photorealistic novel view synthesis. | 随机 |  |
| 17 | 2611.21383 | The Mask Is Not the Object: Volumetric Supervision for 3D Gaussian Segmentation | 3D Gaussian Splatting enables object-level operations on Gaussian primitives, yet existing segmentation methods are largely trained and evaluated thro | 随机 |  |
| 18 | 2611.20546 | A Gaussian Primitive Data Management Framework for Efficient 3DGS Trajectory Rendering | Trajectory rendering, which renders novel views of a reconstructed 3D scene along a camera path, is a core operation in digital twins and autonomous i | 随机 |  |
| 19 | 2611.18822 | LongCat-Video-Avatar 1.6 Technical Report | Recent advances in audio-driven avatar video generation have enabled increasingly realistic synthesis, yet achieving precise lip-audio synchronization | 随机 |  |
| 20 | 2611.20245 | From XR Sketches to CAD: Preserving Design Intent with AI | Extended reality (XR) allows designers to sketch shapes directly in 3D, but converting these sketches into editable, feature-based CAD requires interp | 随机 |  |
| 21 | 2611.20076 | SGIP: Learning Scene-Grounded Interaction Priors for Scene-Aware Human Motion Prediction | Human motion prediction (HMP) aims to forecast future movement from an observed motion sequence, and recent methods have incorporated 3D scene geometr | 边界 |  |
| 22 | 2611.21596 | SADL: On the Demand-Supply Geometry of Representation Collapse | In Joint-Embedding Predictive Architectures (JEPAs), a well-constrained projector output does not by itself prevent representation collapse. | 边界 |  |
| 23 | 2611.21577 | When Tool Names Are Not Identities: Measuring Provider Misbinding in MCP-Based AI Agents | Large language model (LLM) applications increasingly act as agents that select and invoke external tools. | 边界 |  |
| 24 | 2611.21507 | GHySSeg: Real-Time Geometric Ground and Road Segmentation for Hybrid Solid-State LiDAR | Hybrid solid-state LiDAR sensors are making their way into production vehicles, yet the data they produce differs structurally from that of the establ | 边界 |  |
| 25 | 2611.21456 | Expertise capture in workplace AI | AI assistants are becoming part of how knowledge workers think and perform, accumulating the prompts, exemplars, memory and interaction histories that | 边界 |  |
| 26 | 2611.21449 | Replicating and Extending Weight-Space Programming: Frontier LLMs Compile Programs into Weights and Read Input | Researchers at MIT recently reported that GPT-6 Astra, a frontier large language model (LLM), can write the weights of small neural networks directly  | 边界 |  |
| 27 | 2611.21439 | A Reinforcement Learning Method to Navigate SMEFT Operator Space | In particle physics, discrepancies between experimental measurements and Standard Model (SM) predictions are commonly interpreted within new theoretic | 边界 |  |
| 28 | 2611.21408 | Do Embedding-Map Distances Guide LLM Ideation? Four Tests Against What Came Next | A popular ideation recipe treats an embedding map of existing work as a guide: pick points far from everything and decode them into ideas. | 边界 |  |
| 29 | 2611.21407 | Harness Leverage Across Model Size: A Ladder of Five Local Agent Harnesses from 0.75B to 4.7B | A harness turns a model into a system that completes tasks: it builds the prompt, exposes tools and decides when work is done. | 边界 |  |
| 30 | 2611.21403 | Portrait Fitness as a Pretext: Probing Implicit Demographic Bias in VLMs | We audit face-related bias in VLMs using BALPORTRAITS, a new balanced dataset of 9,000 fictional portraits across ethnicity, gender, and age segments. | 边界 |  |
| 31 | 2611.20745 | A Seismic Foundation Model for Dense Feature Extraction | Deep-learning-based seismic interpretation is constrained by scarce high-quality annotations, and most existing models are trained separately for indi | 随机 |  |
| 32 | 2611.20840 | Interpretable deep concepts of organoid morphology | Image-based classification of organoid morphologies can indicate drug response, viability, or successful differentiation. | 随机 |  |
| 33 | 2611.19227 | Can an Agent Rethink What It Knows? Selective Scene Memory Updates in a Changing World | Task configurations in factories, warehouses, and everyday physical environments change over time. | 随机 |  |
| 34 | 2611.19756 | Drift-Conditioned Structural Replay for Continual Cardiac Ultrasound Segmentation | Conventional experience replay typically applies fixed preservation constraints to historical exemplars, overlooking variations in how learned represe | 随机 |  |
| 35 | 2611.19495 | Vegetation Health Classification for Low-Data and Edge Hardware Deployment | Unmanned aerial vehicles (UAVs) equipped with cameras are popular, viable tools for vegetation and environmental health monitoring. | 随机 |  |
| 36 | 2611.19670 | Architecting the Corporate AI Infrastructure: The Evolving Roles of AI Governance Committees and Chief Ethics  | The accelerating integration of artificial intelligence (AI) into core business operations has created an urgent need for robust corporate governance  | 随机 |  |
| 37 | 2611.20983 | GRACE: Parallel Best-of-N Multi-Agent Analysis of Closed-Form Questions over Dataframes with Guardrail Selecti | LLM agents answer closed-form questions over a tabular dataframe by writing and executing Python, almost always as a single rollout: one interpretatio | 随机 |  |
| 38 | 2611.18623 | Evaluating the Robustness of Fact-Checking LLMs on Multilingual Evidence | Automated fact-checking benchmarks typically pair claims with clean, curated evidence in high-resource languages, but real-world evidence is often inc | 随机 |  |
| 39 | 2611.20926 | Advancing Cognitive Pairwise Comparisons for Human-Centric Artificial Intelligence and Data Science: A Human-i | Human-centric artificial intelligence and data science (HCAD) systems increasingly involve human-in-the-loop (HITL) interventions to overcome the limi | 随机 |  |
| 40 | 2611.20461 | LiveView: Real-Time Camera-Controlled Re-filming of Streaming Videos | Real-time camera-controlled video re-filming aims to synthesize target views from a streaming source video under online user-specified camera trajecto | 随机 |  |

> 共 40 条。填完后：`python scripts/decision_probe.py ingest 1118 data/decision/labeling_1118.md`

