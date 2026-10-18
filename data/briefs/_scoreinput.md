
==============================
# 2610.02322
==============================

## Abstract
Real-world scenes are compositional: bricks, blades of grass, pebbles, and tree leaves recur across human-built and natural environments. Existing neural scene representations model these elements independently. Most 3D Gaussian Splatting and follow-up abstraction and compression methods treat each element as unique, fitting millions of independent Gaussians per scene. Prior methods like Splat and Replace fit template objects, but they require mostly manual selection of repeated elements. As a result, these representations store redundant parameters and provide weak manipulation handles for downstream tasks. We introduce SCION, a hier- archical compositional scene representation that replaces independent Gaussians with a compact vocabulary of reusable primitives and lightweight world-space instances that place transformed copies throughout the scene. We fit this represen- tation to multi-view captures via a joint optimization over discrete and continuous scene parameters, combining two-level densification over splats and instances with an adversarial loss that preserves detail across shared primitives. The recovered structure yields a compact, controllable representation while maintaining high quality even at 1.2 MB. SCION achieves rate-distortion favorable to existing Gaussian compression methods, and it enables instance-level scene editing and animation without retraining. Our results show that neural scene representations need not memorize scenes as independent primitives; they can discover reusable parts. Project webpage: https://light.princeton.edu/SCION

## Experiments/Results

### 4 Experiments


### 4.1 Evaluation protocol


### 4.3 Ablations


## Method notes

==============================
# 2610.02697
==============================

## Abstract
Recent vision-and-language navigation (VLN) systems increasingly adopt streaming Video-LLM policies that map egocentric RGB observations and instructions directly to low-level actions. Yet these policies inherit weak 3D geometric priors from 2D pretraining. Existing geometry-aware extensions charge a persistent inference-time price: depth sensors, 3D encoders, or per-step perception tool calls. We propose GeoScaffold, a geometric supervision framework that pays this price once, at training time, by internalizing geometry into the policy itself. It first learns a compact depth tokenizer on depth maps from the training trajectories and freezes it. It then fine-tunes the policy with a handful of learnable geometry query tokens, training their hidden states to reconstruct navigation-critical geometry such as depth, connectivity, and traversability. This supervision turns the query states into compact geometric latents for action decoding, and through the shared weights also internalizes geometry into the backbone's own representations. Like a scaffold, the tokenizer, target generators, and reconstruction heads are discarded after training, leaving the backbone and action interface unchanged. Extensive experiments show that GeoScaffold consistently outperforms leading vision-only navigators on continuous VLN benchmarks, offering a practical paradigm for lightweight edge deployment of spatially aware embodied navigation models.

## Experiments/Results

### 4 Experiments


### 4.1 Experimental Setup
Datasets & evaluation metrics. Implementation details.

### 4.2 Main Results
Results on VLN-CE benchmarks. Inference efficiency against geometry-enhanced methods. Backbone generality.

## Method notes

### 2.1 VLA Model for Navigation


### 3 Method


==============================
# 2610.02715
==============================

## Abstract
Egocentric videos capture how people carry out everyday activities, yet testing an agent requires evaluating the consequences of actions it chooses itself. We introduce Ego2World, a benchmark that turns annotated cooking activities into executable planning environments under partial observation. Its compiler links source steps and objects to symbolic action rules, persistent world states, and explicit task conditions, so researchers can execute an agent's proposed actions and check their outcomes. World state and agent belief are maintained separately, enabling controlled studies of planning and information reuse across continuing tasks. Evaluating six planners on 105 tasks shows that accepted operations often leave task goals unmet. Execution traces and condition checks distinguish interrupted runs, partial attainment, and completed execution without goal attainment. In a separate paired Qwen-Plus study, persistent belief improves action validity by 4.15 percentage points and reduces visual-query attempts by 90.27%, with higher token use and no detected completion gain. Ego2World provides a reusable testbed for tracing how planning and memory choices affect execution, observation demand, and task attainment, connecting recorded human activity to the development and evaluation of interactive agents.

## Experiments/Results

### 3 Constructing the Executable Dataset
Organizing source evidence. Normalizing entities and operations. Giving annotations executable meaning. Checking the compilation. Tasks and evaluation cohorts.

### 5 From Execution Signals to Evaluation
Outcome evidence. Task success and partial attainment. Execution validity and reference coverage.

### 6 Experiments


## Method notes

==============================
# 2610.03162
==============================

## Abstract
3D Gaussian Splatting achieves excellent visual quality with real-time rendering, but at the scale of entire cities it does not fit: a trained model carries millions of primitives and gigabytes of memory, and real-time rendering at high quality on a consumer GPU remains out of reach. We introduce Budgeted-GS, a post-hoc method that turns any trained 3DGS model into a factoring tree, a multi-resolution hierarchy of moment-matched aggregates. After a construction pass of a few seconds, a single quality parameter selects, for each view, the level of detail that fits the memory of the target device, so the same city-scale model serves GPUs with widely different memory capacities. When a new scene is to be trained, the same theory applies: instead of growing a full-sized model and compressing it afterwards, budget-centered training first measures how many primitives the scene needs and then trains the model directly at that size, avoiding the wasted effort of optimizing primitives that are later discarded. Both methods are grounded in a measurable capacity floor, a budget-error law derived from optimal transport in phase space; selection rules certified by recent covering theorems decide which primitives are redundant. The floor answers how many primitives a scene actually needs and how many can safely be given up. We validate the floor on 13 public scenes under a preregistered protocol, and exercise both methods from object scenes to an official city capture, rendering it at native 1920x1080, full SH, in real time on one consumer GPU.

## Experiments/Results

### 6 Experiments


### 6.2 Training-side results


### 6.4 Comparison with training-coupled LOD


## Method notes

### 80 GB), Python scheduler + gsplat. Tree construction is once per model;
per-view selection in Python dominates offline LOD latency. The real-time CUDA path removes exactly this cost: 0.8 0.8 ms per-frame preprocess (selection + + gather) included in the 71.0 71.0 fps full-set 1080 ​ p 1080p official trajectory of our CUDA rasterizer (Table 4 of the main paper, Section 6.6 of the main paper). Experimental support, please view the build logs for errors. Generated by L A T E xml . Instructions for reporting errors We are continuing to improve HTML versions of papers, and your feedback helps enhance accessibility and mobile support. To report errors in the HTML that will help us improve conversion and rendering, choose any of the methods listed below: Click the "Report Issue" ( ) button, located in the page header. Tip: You can select the relevant text first, to include it in your report. Our team has already identified the following issues . We appreciate your time reviewing and reporting rendering errors we may not have found yet. Your efforts will help us improve the HTML versions for all readers, because disability should not be a barrier to accessing research. Thank you for your continued support in championing open access for all. Have a free development cycle? Help support accessibility at arXiv! Our collaborators at LaTeXML maintain a list of packages that need conversion , and welcome developer contributions . We gratefully acknowledge support from our major funders , member institutions , , and all contributors. About · Help · Contact · Subscribe · Copyright · Privacy · Accessibility · Operational Status (opens in new tab) Major funding support from

==============================
# 2610.03192
==============================

## Abstract
Mobile Gaussian reconstruction must satisfy two requirements: the reconstruction model must execute within a device resource envelope, and the resulting Gaussian asset must expose a representation size suited to downstream mobile use. Existing feed-forward Gaussian reconstructors commonly decode dense, image-aligned candidates whose final cardinality is implicitly determined by the input resolution and number of views. We present PocketSplat, a feed-forward framework for budgeted mobile Gaussian asset construction. Given a prescribed output budget, PocketSplat organizes dense geometry-aware latent candidates in predicted world space, allocates exact integer capacity across local latent cells, and decodes complete Gaussian attributes only for retained candidates. Cell-conditioned latent fusion aggregates repeated multi-view evidence before decoding, while spatial responsibility decoding adapts Gaussian support after local sparsification. Experiments on DL3DV and out-of-distribution benchmarks establish a strong quality--budget trade-off against feed-forward Gaussian reconstruction baselines. On Mip-NeRF 360, PocketSplat executes directly on a target iPhone and constructs compact, higher-quality Gaussian assets substantially faster than a deployable streamed MVSplat variant; native MVSplat and DepthSplat exceed the device memory budget.

## Experiments/Results

### 4 Experiments


### 4.1 Experimental setup
Datasets and protocol. Baselines, budgets, and metrics.

### 4.2 Reconstruction Quality Across Datasets
In-domain quality and exact budget control. Cross-dataset generalization.

## Method notes

### 3 Method


### 3 Method
PocketSplat is organized around an image-conditioned world-space latent field and a budget-conditioned Gaussian decoder. Given V V multi-view images with intrinsics and camera-to-world poses, denoted by 𝒳 c \mathcal{X}_{c} , and a feasible Gaussian budget B B , it constructs 𝒢 B = f θ ​ ( 𝒳 c , B ) = { μ i , Σ i , c i , o i } i ∈ 𝒮 B , | 𝒮 B | = B . \mathcal{G}_{B}=f_{\theta}(\mathcal{X}_{c},B)=\{\mu_{i},\Sigma_{i},c_{i},o_{i}\}_{i\in\mathcal{S}_{B}},\qquad|\mathcal{S}_{B}|=B. (1) Here μ i ∈ ℝ 3 \mu_{i}\in\mathbb{R}^{3} , Σ i ∈ ℝ 3 × 3 \Sigma_{i}\in\mathbb{R}^{3\times 3} , c i c_{i} , and o i o_{i} denote a world-space mean, covariance, degree-2 RGB spherical-harmonic coefficients, and opacity logit. The latent field consolidates dense multi-view geometric evidence before materialization; the decoder converts it into a mobile Gaussian asset whose cardinality is specified by B B . Figure 2 summarizes this representation-to-asset construction.

==============================
# 2610.03232
==============================

## Abstract
Explainable Artificial Intelligence (AI) enables humans to understand and interpret decisions of AI models. Instead of having a black box, explainability supports humans in understanding AI models' behavior. Existing explainable AI approaches often present explanations on 2D displays using pre-recorded data, requiring users to relate the displayed information back to the physical objects and real world locations involved in a model's decision. Users are forced to decouple data exploration and capture from AI model interpretation. For AI systems that work within physical environments, this separation can make explanations difficult to interpret in context. We propose using Augmented Reality (AR) to enhance the understanding of AI models by enabling spatial explainability information directly in a user's workspace, in real time, as they explore the world. We show how known explainability methods can be applied in AR and provide insights into user experiences with such an application.

## Experiments/Results

### 4 User Study 1: Exploratory Evaluation


### 4.2 Results
Using situated explainability Explainability features Trust and reliability Contrasting ML/AI work experience LLM integration for explanations Suggested improvements

### 5 User Study 2: Comparative User Study


## Method notes

### 4.1 Participants and study design


### 5.1 Participants and study design


==============================
# 2610.03283
==============================

## Abstract
The ability of a device to localize itself within its surroundings is a fundamental prerequisite for spatial computing. Visual-inertial odometry (VIO) has proven to be a cost-effective and accurate solution for this task. Robots, wearables, XR devices, and drones can benefit significantly from efficient implementations of VIO since they allow for cooler, lighter, and cheaper devices with longer battery life and a better user experience. In this work, we propose to enhance the efficiency of a VIO system by leveraging the Hexagon DSP, a commodity co-processor present in many modern smartphones and XR devices. Our approach offloads the visual frontend of a stereo-inertial odometry system to the DSP while keeping the backend on the main CPU. By optimizing the implementation for the DSP architecture, we achieve significant reductions in power consumption and latency compared to CPU-only execution. Our system, HexVIO, demonstrates a 67% reduction in power consumption or an 86% increase in throughput on a commodity smartphone, with the ability to sustain long-term real-time 30 fps tracking for 0.83 W, corresponding to ~18 hours of tracking on the testing device. These results highlight the potential of commodity DSPs for enabling all-day visual-inertial tracking in robotics and mobile devices.

## Experiments/Results

### IV RESULTS


### IV RESULTS
TABLE I: Maximum throughput runs: accuracy and times of CPU baseline vs. HexVIO (DSP) ATE [cm] RTE [cm] FPS Frontend [ms] Backend [ms] End-to-end [ms] p99 [ms] Sequence CPU DSP CPU DSP CPU DSP CPU DSP CPU DSP CPU DSP CPU DSP EV102 5.40 5.40 5.41 5.41 1.12 1.12 1.12 1.12 70.1 70.1 120.0 \mathbf{120.0} 7.75 ± 2.25 7.75\pm 2.25 2.32 ± 0.29 \mathbf{2.32\pm 0.29} 7.15 ± 2.87 7.15\pm 2.87 5.98 ± 2.30 \mathbf{5.98\pm 2.30} 15.00 ± 3.12 15.00\pm 3.12 8.38 ± 2.48 \mathbf{8.38\pm 2.48} 23.5 23.5 14.7 \mathbf{14.7} EMH03 6.05 6.05 6.43 6.43 1.18 1.18 1.18 1.18 56.2 56.2 94.9 \mathbf{94.9} 9.05 ± 1.81 9.05\pm 1.81 2.47 ± 0.32 \mathbf{2.47\pm 0.32} 9.32 ± 4.32 9.32\pm 4.32 7.97 ± 3.42 \mathbf{7.97\pm 3.42} 18.48 ± 4.57 18.48\pm 4.57 10.52 ± 3.63 \mathbf{10.52\pm 3.63} 31.3 31.3 19.2 \mathbf{19.2} TR2 7.30 7.30 7.33 7.33 0.70 0.70 0.70 0.70 105.6 105.6 180.1 \mathbf{180.1} 5.79 ± 1.20 5.79\pm 1.20 2.00 ± 0.22 \mathbf{2.00\pm 0.22} 3.88 ± 1.56 3.88\pm 1.56 3.55 ± 1.48 \mathbf{3.55\pm 1.48} 9.59 ± 1.90 9.59\pm 1.90 5.62 ± 1.64 \mathbf{5.62\pm 1.64} 15.6 15.6 10.3 \mathbf{10.3} TR6 2.06 2.06 2.00 2.00 0.38 0.38 0.38 0.38 93.7 93.7 155.0 \mathbf{155.0} 6.54 ± 1.61 6.54\pm 1.61 2.18 ± 0.24 \mathbf{2.18\pm 0.24} 4.65 ± 1.71 4.65\pm 1.71 4.30 ± 1.50 \mathbf{4.30\pm 1.50} 10.87 ± 2.19 10.87\pm 2.19 6.55 ± 1.64 \mathbf{6.55\pm 1.64} 17.4 17.4 11.4 \mathbf{11.4} MOO02 23.48 23.48 23.43 23.43 1.54 1.54 1.54 1.54 103.2 103.2 206.3 \mathbf{206.3} 6.68 ± 0.73 6.68\pm 0.73 2.10 ± 0.13 \mathbf{2.10\pm 0.13} 2.80 ± 1.81 2.80\pm 1.81 2.51 ± 1.54 \mathbf{2.51\pm 1.54} 9.68 ± 1.98 9.68\pm 1.98 4.78 ± 1.62 \mathbf{4.78\pm 1.62} 16.0 16.0 10.4 \mathbf{10.4} MOO08 2.74 2.74 2.73 2.73 1.12 1.12 1.11 1.11 97.6 97.6 177.1 \mathbf{177.1} 6.83 ± 1.37 6.83\pm 1.37 2.14 ± 0.30 \mathbf{2.14\pm 0.30} 3.26 ± 2.00 3.26\pm 2.00 3.16 ± 1.77 \mathbf{3.16\pm 1.77} 10.28 ± 2.45 10.28\pm 2.45 5.47 ± 1.90 \mathbf{5.47\pm 1.90} 17.8 17.8 11.1 \mathbf{11.1} XWALK † – – – – 70.3 70.3 161.5 \mathbf{161.5} 8.48 ± 2.04 8.48\pm 2.04 1.88 ± 0.14 \mathbf{1.88\pm 0.14} 5.67 ± 2.93 5.67\pm 2.93 4.24 ± 1.67 \mathbf{4.24\pm 1.67} 14.43 ± 4.22 14.43\pm 4.22 6.30 ± 1.71 \mathbf{6.30\pm 1.71} 24.7 24.7 10.0 \mathbf{10.0} XBIKE † – – – – 60.7 60.7 144.5 \mathbf{144.5} 9.84 ± 2.53 9.84\pm 2.53 1.95 ± 0.17 \mathbf{1.95\pm 0.17} 6.50 ± 2.85 6.50\pm 2.85 4.75 ± 1.77 \mathbf{4.75\pm 1.77} 16.66 ± 4.48 16.66\pm 4.48 6.92 ± 1.86 \mathbf{6.92\pm 1.86} 27.1 27.1 11.6 \mathbf{11.6} ATE S ​ E ​ ( 3 ) SE(3) aligned RTE Δ = 6 \Delta=6 frames p99 99th percentile of end-to-end frame time ± \pm frame time standard deviation * Numbers averag

## Method notes

### III METHOD
III-A Architecture III-B Pipeline III-C Pyramid III-D Detection III-E Tracking

### III METHOD
III-A Architecture Two properties of the V73 shape the frontend, its vector execution model and its memory hierarchy. Scalar core VLIW core × 6 \times 6 threads GRF R0–R31 · P0–P3 slots S0 S1 S2 S3 L1 L1I L1D HVX vector unit × 4 \times 4 contexts VRF V0 1024 b Q0 128 b ⋮ \vdots ⋮ \vdots V31 1024 b Q3 128 b units ld mpy mpy shift perm st HMX matrix unit L2 cache ·1 MB VTCM ·8 MB DDR Fig. 2: The Hexagon V73 compute DSP. The scalar core, HVX vector unit and HMX matrix unit share one memory hierarchy. Each hardware thread has its own scalar registers (GRF, predicates P0–P3); each vector context has its own vector registers (VRF, predicates Q0–Q3) and the six functional units that operate on them. The gather instruction, the basis of sparse feature sampling, addresses VTCM only. Computation units The Hexagon V73 compute DSP (cDSP) comprises a scalar core and two coprocessors (Fig. 2 ): HVX (Hexagon Vector eXtensions) for wide SIMD on 1024-bit registers, which we use, and HMX for matrix operations. Every vector instruction occupies one of the four VLIW slots in a thread’s instruction packet, so scalar and vector instructions issue together, subject to the available vector functional units. The six hardware threads attach dynamically to the four vector contexts, and peak vector throughput requires all four active. Memory subsystem The CPU invokes code on the DSP through FastRPC, a remote-procedure-call layer [ 42 ] . We allocate every buffer that crosses the boundary as shared memory, which FastRPC maps into the DSP’s address space instead of copying it. On the DSP side, HVX bypasses the scalar core’s L1 and reads from L2 or from VTCM (vector tightly coupled memory), an 8 MB scratchpad under software control. Alongside ordinary loads and stores, DMA can move bulk data from DDR into VTCM. The vector gather instruction can only address VTCM [ 43 , Sec. 3.3] , so anything sampled at non-contiguous memory addresses must be resident there rather than merely cached. Pixel-parall

==============================
# 2610.03441
==============================

## Abstract
We present ChromaGS, a method for real-time, language-guided color editing of animatable 3D Gaussian head avatars. Given a trained animatable avatar, users can instantly modify the color of semantic regions through natural language, with edits applied at render time and no retraining required. Our key insight is to augment each Gaussian primitive with learned soft assignments to semantic regions and decompose colors into region-level base colors and Gaussian-level residuals. This decomposition enables coherent color transfer: modifying a region's base color propagates naturally through all associated Gaussians while preserving fine appearance details encoded in residuals. A two-stage language pipeline translates text instructions into target colors, supporting both absolute specifications and relative adjustments. Unlike generative editing methods that may introduce unintended modifications, our approach provides deterministic, precisely localized semantic control. Experiments demonstrate faithful appearance preservation and intuitive interaction across diverse subjects. Project page and code are available at: https://a-canela.github.io/chromags/

## Experiments/Results

### IV Experiments
IV-A Comparison with Baselines IV-B Ablation Studies

### IV Experiments
Implementation Details. We implement ChromaGS on top of an animatable Gaussian splatting framework [ 4 ] . We define K = 6 K=6 semantic classes (hair, eyebrows, eyes, lips, skin, plus background). Training runs for 50k iterations on a single NVIDIA RTX 5090, taking approximately 15 minutes. Datasets and Evaluation Setup. We evaluate on scenes from FaceScape [ 28 ] and INSTA [ 29 ] , featuring diverse skin tones, eye colors, and hair styles. Each scene is edited with 14 diverse color edits spanning hair, eyes, skin, lips, and eyebrows, yielding approximately 10k edited frames per method at 512 × 512 512\times 512 resolution. Fig. 3: Qualitative comparison. Results for skin, hair, and eyes edits across three subjects. Our method produces localized, natural color changes that preserve identity and fine details (e.g., specular highlights, skin texture). Both GaussianAvatar-Editor [ 5 ] and InstructPix2Pix [ 22 ] exhibit color bleeding into unrelated regions and over-saturated tones. Metrics. We measure: (1) Identity Preservation ↑ \uparrow : ArcFace cosine similarity between edited and unedited renders; (2) CLIP Score ↑ \uparrow : alignment between rendered image and target text prompt, averaged across three CLIP backbones (ViT-L/14, ViT-B/16, ViT-B/32); (3) Context Preservation ↑ \uparrow : computed as 1 − LPIPS 1-\text{LPIPS} outside the target region, measuring how well non-target areas are preserved after editing. IV-A Comparison with Baselines TABLE I: Runtime comparison. Our method requires a one-time ∼ \sim 800 s training, after which any subsequent edit is applied instantly ( ∼ \sim 50 ms). In contrast, GaussianAvatar-Editor [ 5 ] relies on a coupled training-and-editing loop, requiring a full ∼ \sim 800 s optimization for every new edit. InstructPix2Pix [ 22 ] requires no per-subject optimization as it processes each frame independently via diffusion. Method Train ↓ \downarrow Edit ↓ \downarrow Render ↑ \uparrow IPix2Pix [ 22 ] N/A ∼ \sim 400 ms N/A GAEditor [ 5 ] ← ∼ \sim 800 s → > > 100 fps ChromaGS (Ours) ∼ \sim 800 s ∼ \sim 50 ms > > 100 fps TABLE II: Quantitative comparison with baselines. Our method achieves significantly better identity and context preservation. The baselines’ higher CLIP scores reflect a limitation of the metric itself: CLIP measures global image-text alignment and thus rewards visually dominant color shifts, even when they bleed into unintended regions. Method CLIP ↑ \uparrow Identity ↑ \uparrow Context ↑ \uparrow IPix2Pix [ 22 ] 0.231 0.691 0.790 GAEditor [ 5 ] 0.229 0.863 0.790 ChromaGS (Ours) 0.212 0.986 0.980 We compare

## Method notes

### III Method
III-A Semantic Masks Extraction III-B Text-Guided Color Editing III-C Semantic-Aware Gaussian Splatting III-D Training Objective

### III Method
III-A Semantic Masks Extraction For each semantic class k k and each training frame, we use SAM3 [ 20 ] with text prompts to generate binary masks M k M_{k} . Iris masks are obtained from eye masks by detecting ellipses and warping an annular-shaped template. Masks are made mutually exclusive by prioritizing smaller regions (e.g., iris over eye sclera) to ensure proper layering. SAM3 exhibits strong temporal consistency across frames due to its concept-level understanding; moreover, since our optimization aggregates supervision from hundreds of frames, occasional segmentation noise is naturally absorbed during training. III-B Text-Guided Color Editing To enable intuitive color specification, we propose a two-stage architecture that decouples semantic parsing from color resolution, improving robustness by assigning simpler, well-defined tasks to each component. Semantic Parsing. We fine-tune Flan-T5-Small [ 23 ] to parse natural language instructions into a structured intermediate format. Given input text (e.g., “red matte lipstick”), the model outputs a structured string: region, color, type (e.g., lips, red matte, absolute ). Multiple edits are separated by semicolons. This simplified output space (region names, color descriptors, and edit types) is significantly easier to learn than direct RGB prediction. Color Resolving. The structured output is processed by a deterministic color resolver that handles two types of instructions: Absolute. For absolute color instructions (e.g., “olive skin”), we encode the color description using a pretrained sentence encoder (all-MiniLM-L6-v2) [ 24 , 25 ] and find the closest match via cosine similarity against pre-computed embeddings of region-specific palettes. These palettes contain anatomically plausible colors (e.g., Fitzpatrick scale [ 26 ] tones for skin, natural iris colors based on melanin distributions) and serve as the target color space for each region. Relative. For relative instructions (e.g., “darker”, “more saturat

==============================
# 2610.03599
==============================

## Abstract
High-fidelity 3D head avatars have reached near-photorealistic quality. While recent methods enable text-driven manipulation, they struggle to provide fine-grained localized control, often entangling features or lacking geometric consistency. Modifying geometry through natural language currently requires slow per-prompt optimization or compromises identity and rigging. We present ManifoldSplat, the first end-toend framework for language-guided semantic shape editing of animatable 3D Gaussian Splatting avatars reconstructed from monocular videos. By performing edits within the structured FLAME manifold rather than directly optimizing an unstructured Gaussian cloud, we strictly preserve identity and animation. We introduce DeltaRegion, a per-region disentangled Conditional Variational Autoencoder (CVAE) delivering feedforward shape deltas, alongside a refining stage to recover view-consistent details. ManifoldSplat reconstructs and edits an avatar in ~90 seconds on a consumer GPU, rendering at ~800 FPS. Extensive evaluations demonstrate our approach sets a new state-of-the-art in localized prompt alignment, geometric coherence, and identity preservation. Project page and code: https://a-canela.github.io/manifoldsplat/

## Experiments/Results

### 3.2 Synthetic Dataset
Scalable Generation.

### 4 Experiments


### 4.1 Experimental Setup


## Method notes

### 2.1 Parametric Face Models.


### 3 Method


==============================
# 2610.03607
==============================

## Abstract
Learning general-purpose robot policies requires large-scale real-world interaction data, yet collecting robot demonstrations remains expensive and difficult to scale. Egocentric videos offer abundant human interaction experience with task-relevant semantics for robotic manipulation, but direct transfer is challenging for two reasons: latent actions inferred from frame reconstruction can be dominated by nuisance variation such as ego-camera motion, and human and robot behaviors often exhibit different temporal dynamics. We propose WING (World Action Learning via INteraction-Centric Spectral Latent Guidance), a framework for transferring interaction knowledge from egocentric videos to robot policies. WING first separates observer-induced motion from hand-object interaction and distills the interaction-centric component into latent actions. It then exploits the observation that cross-embodiment task semantics are concentrated in slowly varying temporal structures, identifying shared low-frequency components between egocentric latent actions and robot behaviors in the spectral domain and using them to guide action generation. WING achieves average success rates of 99.20% on LIBERO, 93.80% on RoboTwin 2.0, and 57.7% on RoboCasa-GR1, and also performs strongly across four real-world manipulation tasks under diverse generalization settings. These results show that interaction-centric spectral guidance provides an effective and scalable way to transfer physical interaction knowledge from human egocentric video to robot control. Project page: https://mikuz12.github.io/wing/

## Experiments/Results

### 4 Experiments


### 4.1 Experimental Setup
4.2 (Q1): Characterizing Egocentric Latent Structure For Robot Learning. 4.3 (Q2): Robot Policy Performance Results on Simulation. Results on the real-world robot. 4.4 (Q3): Ablation Studies on WING-LAM and Spectral Guidance. Ablation on observer debiasing and spectral guidance. Ablation on the number of DCT components. 4.5 (Q4): Analysis of Ego Pre-training Strategies.

## Method notes

### 3 Methods
