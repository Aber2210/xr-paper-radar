# MOC · backfill-1126（旧稿 replace 再公告首次入馆）

> **非当日新提交**：本批 8 篇均为 11-25 公告 RSS 混入的 `replace` 类旧稿再公告，**首次入馆**；首发 2025-08-24 ~ 2026-10-08（updated 均为 2026-11-23/24）。按诚实口径单独编号，**不参与当日重磅日判定**，即使 ≥4.20 亦记 A（本批最高 3.85，未触及该线）。
> 定稿 **A 6 / B 1 / C 1（无 S）**：3.85 PLANING：松耦合三角-高斯流式三维重建框架 · 3.85 面向多视图空间理解的 Seek-and-View 推理 · 3.77 EgoPathBench：评估视觉语言模型的零样本第一人称 waypoint 决策 · 3.72 BARISTA：面向组合式视觉理解的多任务第一人称基准 · 3.70 SEER-VAR：面向车载增强现实的语义第一人称环境推理器 · 3.62 基于查询卷积神经网络的高保真 Gaussian Splatting · 3.50 OP2GS：面向三维实例分割的双不透明度无特征 Gaussian Splatting · 2.77 利用注视与 Set-of-Mark 提示提升 VLLM 的第一人称人-物交互预判。
> 门① 的最大 Jaccard 对（0.192）正是由本批 2610.11810 与库内 2611.29112 构成，仍低于 0.62 阈值。

## 本批论文（按加权降序）

| # | 论文 | 赛道 | 总分 | 等级 | 证据 | 笔记 |
|---|---|---|---|---|---|---|
| 1 | PLANING：松耦合三角-高斯流式三维重建框架 | 重建与SLAM | 3.85 | A | FULL | [→](../notes/2601.22046__planing-a-loosely-coupled-triangle-gaussian-framewor.md) |
| 2 | 面向多视图空间理解的 Seek-and-View 推理 | 空间计算与UI | 3.85 | A | FULL | [→](../notes/2610.11810__seek-and-view-reasoning-for-multi-view-spatial-under.md) |
| 3 | EgoPathBench：评估视觉语言模型的零样本第一人称 waypoint 决策 | 评估与数据集 | 3.77 | A | FULL | [→](../notes/2609.16610__egopathbench-evaluating-zero-shot-egocentric-waypoin.md) |
| 4 | BARISTA：面向组合式视觉理解的多任务第一人称基准 | 评估与数据集 | 3.72 | A | FULL | [→](../notes/2605.12074__barista-a-multi-task-egocentric-benchmark-for-compos.md) |
| 5 | SEER-VAR：面向车载增强现实的语义第一人称环境推理器 | 感知与认知 | 3.70 | A | FULL | [→](../notes/2508.17255__seer-var-semantic-egocentric-environment-reasoner-fo.md) |
| 6 | 基于查询卷积神经网络的高保真 Gaussian Splatting | 神经渲染 | 3.62 | A | FULL | [→](../notes/2512.12898__towards-high-fidelity-gaussian-splatting-with-querie.md) |
| 7 | OP2GS：面向三维实例分割的双不透明度无特征 Gaussian Splatting | 神经渲染 | 3.50 | B | FULL | [→](../notes/2605.20044__op2gs-feature-free-gaussian-splatting-with-dual-opac.md) |
| 8 | 利用注视与 Set-of-Mark 提示提升 VLLM 的第一人称人-物交互预判 | 感知与认知 | 2.77 | C | FULL | →（C 级仅入馆） |

## 批次要点

- **PLANING：松耦合三角-高斯流式三维重建框架**（2601.22046，3.85 A）：流式单目重建里把显式三角几何当结构锚点、神经高斯只负责外观，两者松耦合：三角抑制漂移与冗余，外观梯度可反传微调几何但不与之冲突——ScanNet++ 平面 Chamfer-L2 3.53 vs PGSR 3.87（−18.5%），仅 61.6k 基元 / 5.5 分钟，ScanNetV2 平面 5.68 vs ARTDECO 6.05 而基元少 11×。
- **面向多视图空间理解的 Seek-and-View 推理**（2610.11810，3.85 A）：把「主动取景」本身当作中间推理目标，用重力对齐的 3D 基础模型 + 离散动作集把语义意图稳定落到几何变换，从而真正合成原观测之外的新视角且零微调：六个 VLM × 六个基准共 5,496 题平均绝对提升 8.2%，GPT-5.4 总体 47.0%→59.0%，Qwen3.6-27B 59.2%→73.0%。
- **EgoPathBench：评估视觉语言模型的零样本第一人称 waypoint 决策**（2609.16610，3.77 A）：把「可行性」写进 3D 场景几何而非文字或 2D 像素，用 Point/Embodied 成对设计把「同一动作在不同机身约束下后果不同」变成可测量变量，Intent Path 再把指代解析与具身路径绑定：1,111 道基准题上十个零样本 VLM 最高仅 35.6 分（GPT-6 Astra）。
- **BARISTA：面向组合式视觉理解的多任务第一人称基准**（2605.12074，3.72 A）：首次把掩膜、框、属性、类型化关系、HOI、活动与工序步骤在同一帧、同一物体身份上共注册，使过程级失败可回溯到具体感知层，并用 matched-case 协议把跨层级共失败变成可测量量：185 段视频 / 4.4 小时 / 469,201 标注帧 / 3.61M 实例掩膜。
- **SEER-VAR：面向车载增强现实的语义第一人称环境推理器**（2508.17255，3.70 A）：把驾驶 AR 重述为「车内 + 车外」双上下文第一人称感知问题，两套独立参考系分别跟踪（与所有单世界系 SLAM/AR 管线的本质差别），并用深度直方图双峰谷底做自适应域分离：车内/车外 RE 13.74 / 17.63 px（ORB-SLAM3 车内 32.75），ARE 1.85° / 5.64°。
- **基于查询卷积神经网络的高保真 Gaussian Splatting**（2512.12898，3.62 A）：把「邻域」与「查询」两种归纳偏置显式合成为单一算子，并给出可证伪的误差单调性定理与高斯数量指数下界，从理论上说明堆基元不是提升保真度的方向：Mip-NeRF 360 上 3DGS 27.67→27.96 dB、MCMC 28.26→28.58 dB（超过 Zip-NeRF 28.54），且高斯数更省。
- **OP2GS：面向三维实例分割的双不透明度无特征 Gaussian Splatting**（2605.20044，3.50 B）：用第二个不透明度把掩膜渲染与成像渲染解耦（每高斯仅 +1 标量 +1 整数），同时解决边界泄漏与「冻结资产不可改」两个问题，并配齐占据损失、离散重分组与无解码读出：ScanNet++ EntitySeg 掩膜 AP 23.1 vs OpenSplat3D 18.3，ScanNet mIoU 51.90 vs 50.30。
- **利用注视与 Set-of-Mark 提示提升 VLLM 的第一人称人-物交互预判**（2604.03667，2.77 C）：把 Set-of-Mark 视觉提示与注视轨迹两个正交信号同时喂给 VLLM，并用逆指数采样把有限帧预算压到交互前窗口，整套改造只在输入与提示层、零训练且跨模型可迁移：LLaVA-OneVision 7B 20.4%→27.2%，Gemini 2.0 Flash 21.0%→27.5%（超过原榜首 5 个百分点以上）。
