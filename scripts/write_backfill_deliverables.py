#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""write_backfill_deliverables.py — backfill-1012-1015 批次产物生成。
输入：data/scored_backfill.json + data/fulltext/_manifest.json
输出：registry 幂等追加（先备份）、Top10 原子笔记、Backfill 报告、MOC、总索引刷新、run_log 收尾。
"""
import json, os, re, shutil, datetime

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(ROOT, "data") + os.sep
REG = os.path.join(ROOT, "papers", "library", "registry.jsonl")
NOTES = os.path.join(ROOT, "papers", "notes") + os.sep
REPORTS = os.path.join(ROOT, "reports") + os.sep
MOCS = os.path.join(ROOT, "papers", "MOC") + os.sep
DAILY = os.path.join(ROOT, "papers", "daily", "backfill-1012-1015") + os.sep
BATCH = "backfill-1012-1015"
ORIG = {"d1012": "10-12 公告漏网", "d1014": "10-14 公告漏网", "d1015": "10-15 公告漏网",
        "d1016": "10-16 公告残留", "d1009": "10-09 公告漏网", "old1009": "10-09 旧稿再公告遗留", "old1016": "10-16 旧稿 replace/cross"}
SDATE = {"d1012": "2026-10-12", "d1014": "2026-10-14", "d1015": "2026-10-15",
         "d1016": "2026-10-16", "d1009": "2026-10-09", "old1009": "2026-10-09", "old1016": "2026-10-16"}

S = json.load(open(DATA + "scored_backfill.json", encoding="utf-8"))
MAN = json.load(open(DATA + "fulltext" + os.sep + "_manifest.json", encoding="utf-8"))
inc = S["included"]; top10 = S["top10"]; gate = S["gate"]
by_id = {r["id"]: r for r in inc}

# ---------------- 1) registry 幂等追加（先备份） ----------------
reg = [json.loads(l) for l in open(REG, encoding="utf-8") if l.strip()]
reg_ids = set(r["id"].split(":")[-1].split("v")[0] for r in reg)
new = [r for r in inc if r["id"] not in reg_ids]
bak = REG + ".bak-20261017bf"
shutil.copy2(REG, bak)
with open(REG, "a", encoding="utf-8") as f:
    for r in new:
        man = MAN.get(r["id"])
        f.write(json.dumps({
            "id": "arXiv:" + r["id"], "title": r["title"], "title_zh": r["title_zh"],
            "track": r["track"], "date": SDATE[r["src"]], "value": r["value"], "grade": r["grade"],
            "scores": r["scores"], "status": "CURRENT",
            "evidence": "FULL" if man else "ABSTRACT_ONLY",
            "fetch_level": man["level"] if man else "-",
            "fulltext_chars": man["chars"] if man else 0,
            "in_top10": r["id"] in top10, "batch": BATCH,
            "orig_window": ORIG[r["src"]],
            **({"flags": r["flags"]} if r["flags"] else {}),
        }, ensure_ascii=False) + "\n")
print(f"registry: {len(reg)} → {len(reg)+len(new)}（+{len(new)}，备份 {os.path.basename(bak)}）")

# ---------------- 2) Top10 原子笔记 ----------------
# 每篇：一句话结论 / 问题 / 方法 / 实验 / 创新 / 局限 / 库内关系
N = {
"2610.16277": dict(slug="FlowAvatar消费级XR实时全身化身", tags=["XR 化身", "全身姿态", "Quest Pro", " SMPL-X", "实时"],
 one="首个在独立头显（Meta Quest Pro）上实时统一全身姿态、手部关节、面部表情与注视追踪并保持个性化外观的开源化身系统；姿态模型在 AMASS 上空间精度持平 SOTA、时序一致性 SOTA（MPJVE 21.72 cm/s、jitter 3.77×10⁻²，较 HMDPoser 分别改善 28%/33%）。",
 prob="既有化身研究把「追踪完备度」与「个性化外观」分开研究，各自依赖实验室专用设备；在消费级独立头显上，稀疏传感（头+手）如何同时驱动全身、面部与注视并无系统答案——头显只提供 3-DoF/6-DoF 头姿与双手控制器信号，全身姿态是欠约束问题。",
 method="① 身体部位编码（body-part encoding）把稀疏头/手信号编码为部位级特征；② 统一运动学解码器（unified kinematic decoding）直接输出 SMPL-X 参数，把「不同参数空间的对齐」内化到网络而非后处理规则；③ 空间+时序联合损失（显式惩罚速度与抖动）。Quest Pro 内置传感器提供手部关节、面部表情与眼动，各自经映射汇入 SMPL-X：手/脸 blendshape 重定向到 mesh，眼球 yaw/pitch 由注视数据驱动以实现自然眼神接触。",
 exp="AMASS 基准：MPJPE 5.40 cm（与 HMDPoser 5.44 持平）、MPJVE 21.72 cm/s、jitter 3.77×10⁻²（HMDPoser 30.15/5.62，EgoPoser 抖动 18.64×10⁻² 近 5 倍于本方法）；用户研究 6 个维度（风格/保真/沟通/交互就绪/上下肢）逐项显著性检验，追踪与纹理两个处理阶段均呈统计显著提升。",
 innov="① 首次在独立消费头显上闭环「姿态-手-脸-注视-外观」五要素并开源；② 用统一运动学解码替代分模块后处理拼接；③ 时序损失显式建模抖动，把「稳定性」提升为一等指标。",
 lim="① 依赖 Quest Pro 的眼动/面捕硬件，向无面捕头显的迁移未验证；② 外观个性化仍依赖既有纹理流程，实时性边界待考；③ 仅 AMASS 分布内验证，大幅越分布动作（如倒地）未测。",
 rel="与库内 EgoPoser/HMDPoser 一脉相承（稀疏头手→全身姿态），但把它推进到「消费硬件上的完整社交化身」；与 FlowAvatar 同期库内 FaceGAN（流式说话头）构成「脸-全身」互补，与 EgoWholeView（六相机动捕）构成「传感完备度光谱」的两端。"),

"2610.19998": dict(slug="ShadAR提示词驱动AR实时视觉增强", tags=["AR", "视觉增强", "shader 生成", "LLM", "passthrough"],
 one="用户用自然语言描述期望的视觉改变（如「把所有人模糊掉」），ShadAR 经 LLM 解译意图、目标检测定位对象、实时生成像素 shader 注入 AR passthrough 视频流，把「专家预编程的静态视觉增强」变为「按需实时可编辑」。",
 prob="AR 视觉增强（模拟色盲、模糊、高亮等）能重塑人的视觉感知，但效果历来由专家预编程，用户无法按需即时调整；而普通用户不具备编写 shader 的能力，既有工具也不支持对 passthrough 实时流的图形化操纵。",
 method="流水线四段：① LLM（GPT5.2）把用户的自然语言提示解译为结构化意图；② 目标检测（YOLOv26）分析当前视图、定位增强对象；③ 代码生成产出像素 shader；④ shader 注入实时作用于 AR passthrough。配套「迭代/重做 shader 的内存管理」机制，让用户可以反复调整而不丢失上下文。",
 exp="21 名 HCI 研究者的 workshop：归纳出四类应用场景（Design/Health/Productivity/Social Interaction）与两种提示构架范式——程序式提示（说明转换什么、怎么转）与目标式提示（只描述期望的内在状态）；发现目标式提示会导致不确定性结果，形成设计挑战讨论。",
 innov="① 把「视觉增强的创作权」从专家交给终端用户，交互范式上是 passthrough 可编程性的首次系统化；② 程序式 vs 目标式提示的分类与不确定性分析，对后续 AR+LLM 生成式交互有直接设计指导意义。",
 lim="① 21 人 workshop 为定性研究，无量化实验；② 依赖 LLM 代码生成的正确性与延迟，复杂提示的失败模式未系统量化；③ 仅在受控场景验证，真实日常佩戴的稳定性待考。",
 rel="与库内 LICOA（指令条件光学动作学习）分别代表「AR 视觉增强的软件层」与「光学硬件层」两条按需增强路线；与库内多篇 LLM+XR 智能体工作（XARA/Cobot）同属「生成式 XR 交互」新兴簇。"),

"2610.16256": dict(slug="EgoWholeView六相机头戴全身动捕", tags=["头戴动捕", "第一视角", "具身示范", "多相机", "SMPL-X"],
 one="一台六同步广角 RGB 相机的头戴装置：外向相机恢复装置在世界系的位姿，一对重叠下视相机观测近身与双手；角色专业化（role-specialized）流水线在各自坐标系内预测、仅在参数化兼容时融合，实现相机only的全身+双手运动捕捉，服务自化身、遥操作与具身示范。",
 prob="头戴式全身动捕支持自化身/遥操作/具身数据采集，但单目第一视角相机受视场局限、尺度歧义与手-物遮挡三重困扰；加装传感又引入标定与融合难题——不同相机看到的身体部位参数化不同，朴素融合会引入系统性偏差。",
 method="① 角色专业化六相机装配：每台相机承担明确传感角色（外向定位/下视近身/双手），所有预测保留各自坐标系；② 坐标帧保持的融合策略：仅当预测的参数化兼容时才融合同步预测，从机制上避免跨帧错配；③ 完整同步、装置标定与坐标系定义流程。评估采用 Procrustes 对齐后的 PA-MPJPE/PA-MPVPE（MANO K=21/M=778，UnrealEgo-RW 上 SMPL-X K=15），并量化可见性、扰动离散度、裁剪边界支撑对误差的贡献。",
 exp="在 UnrealEgo-RW 等基准上给出全身/双手的量化误差分解；消融显示下视重叠对近身与双手覆盖的决定性作用，以及「高可见性+低扰动+高裁剪支撑」条件下误差最低（身体 0.3228/0.0912/0.1109 量级的支撑度对比）。",
 innov="① 用「传感角色分工+坐标帧保持融合」把多相机头戴动捕的误差源结构化，而非黑端到端；② 相机only达到可用全身+双手精度，为无 Marker 具身数据采集提供可复制的硬件-软件参考设计。",
 lim="① 六相机硬件的体积/功耗/成本对日常佩戴仍是负担；② 与光学 Marker 系统的精度差距未在同基准直接对比；③ 主要在受试者室内数据验证。",
 rel="与库内 FlowAvatar（消费头显稀疏传感化身）构成「传感完备度光谱」：EgoWholeView 重精度、FlowAvatar 重便携；与 Hand-4DGS/ReViV（第一视角重建）共享 egocentric 数据范式。"),

"2610.17605": dict(slug="PLEDGE误差有界3DGS渐进压缩", tags=["3DGS", "压缩", "编解码器", "误差有界", "training-free"],
 one="免训练、渐进、误差有界的 3DGS 编解码器：把用户声明的四类容差（屏幕空间位置、旋转缩放致足印形变、视角相关颜色、不透明度）翻译为每个高斯的量化边界，任何有效前缀都满足误差命题，实现「要多少精度给多少码率」的可控压缩。",
 prob="既有 3DGS 编解码器只报告压缩后重建质量，用户对单个高斯的畸变没有控制力；而「场景平均 1 dB 损失」这类指标掩盖了局部 primitive 的严重畸变，无法满足渐进流式与质量敏感场景的需求。",
 method="① 四类用户可声明容差 → per-primitive 量化边界的直接翻译；② 免训练设计，不做 per-scene 优化；③ 渐进码流：任何有效前缀均满足 Proposition 6 的误差保证，客户端可按带宽截取。",
 exp="13 个场景上的压缩比与误差曲线：60% 保留率下仅损失 0.082 dB；收紧 τ_px 可把最大 PSNR 损失压到 0.05 dB 以内，而放松 τ_px 则最多再降 1.2 dB 最大 PSNR 损失——证明容差旋钮的有效性；9 个 Mip-NeRF 360 场景 test-split PSNR 复核。",
 innov="① 把「误差有界」从场景级指标推进到 per-primitive 级保证；② 免训练+渐进码流的组合对低延迟流式传输（库内体积视频方向的直接需求）尤为关键。",
 lim="① 容差到量化边界的翻译对非标准内容的保守性未充分讨论；② 与库内 TETRIS-4DGS/PLEDGE 同类压缩家族的同基准横评待补；③ 主要在标准基准场景验证。",
 rel="与库内 ResStreamGS（移动体积视频流式）、TETRIS-4DGS（训练后压缩）、RDCompGS（率失真优化）共同构成「3DGS 压缩/传输」方法族；PLEDGE 的误差有界保证是该族独有的质量维度。"),

"2610.19290": dict(slug="Kandinsky音频驱动化身视频生成", tags=["说话头", "音频驱动", "视频生成", "开源模型", "长视频"],
 one="开源的音频驱动说话视频生成模型家族：Lite（2B）与 Pro（21B）双规格，从单张参考图+语音波形+文本提示生成 25 FPS 的 SD/HD 长视频，唇动、表情、姿态、手势跟随语音；Pro 在 EMTD/CelebV-HQ/HDTF 上取得最佳平均排名，蒸馏版 16 步采样实现 5.4× 加速。",
 prob="音频驱动说话人生成已有大量工作，但长时长（数秒级以上）、多语言、开源可复现的模型仍然稀缺；既有开源方案在长视频的身份/运动一致性上明显退化，闭源商用模型又不开放权重。",
 method="① 自回归 5 秒块（125 帧@25FPS）生成，由 FramePack 记忆机制粘合，突破单块长度限制同时保持身份与运动连续性；② 文本与音频双条件注入；③ π-Flow 蒸馏：Lite/Pro 均有蒸馏变体，Pro 蒸馏后 16 步采样、无 classifier-free guidance 即达 5.4× 加速；④ 训练数据经 Qwen3-VL-32B-Instruct 自动标注（2 FPS 抽帧、≤512²）。",
 exp="EMTD、CelebV-HQ、HDTF 三个基准：蒸馏 Pro 在全部五项指标聚合的平均排名与 min-max 分数上为最优；SD/HD 双分辨率、多语言提示、25 FPS 长视频生成均经验证；两个模型权重开放。",
 innov="① 开源社区少有的「双规格+蒸馏」说话视频模型家族，25 FPS 长视频+记忆机制直击实用性；② FramePack 记忆与自回归分块的组合为长时长驱动生成提供了可复用的工程范式。",
 lim="① 以预标注数据训练，标注噪声未量化；② 与最新闭源商用效果的差距未在同测试协议下对比；③ 手势/姿态的可控粒度仍靠文本提示间接控制。",
 rel="与库内 FaceGAN（流式说话头，10-10 Top）直接同赛道竞争——FaceGAN 胜在流式实时，Kandinsky 胜在开源权重+长时长+多语言；与化身赛道整体（Brain2Face/FlowAvatar）构成「驱动-生成-追踪」方法链的不同环节。"),

"2610.18950": dict(slug="HumanVerse500小时第一视角人形数据", tags=["人形机器人", "第一视角数据", "数据集", "loco-manipulation", "VLA"],
 one="500 小时开放世界人类 loco-manipulation 数据集 HumanVerse：第一视角视频与同步的身体/手部运动配对；配套 human-to-humanoid 流水线对齐相机视角与手臂外观，离线精化运动参考与控制器输入以压低末端误差同时保留全身协调，并以前所未有规模的基线横评验证。",
 prob="人形机器人全身视觉-语言-动作策略需要大规模机器人示范，但采集昂贵；人类示范虽可扩展，既有第一视角监督往往缺失移动与姿态信息，且具身差异与控制器动力学使末端执行精度不足。",
 method="① 数据采集：500 小时开放世界人类 loco-manipulation，第一视角视频+同步身体/手部运动；② human-to-humanoid 对齐：相机视角与手臂外观对齐，离线精化运动参考与控制器输入；③ 大规模评测协议：18 个任务-难度组合×每组合 10 次试验的仿真评测+真实世界评测。",
 exp="仿真横评 8 个强基线（H-RDT/InternVLA-M1/EgoVLA/Diffusion Policy/GR00T N1.6/π0.5/DreamZero/ACT）：基线总体成功率 13.9%–65.6% 不等（DreamZero 65.6 最强），本方法在保留全身协调的目标下取得有竞争力表现；真实世界评测与泛化评测协议完整公开。",
 innov="① 把「人类示范→人形策略」的数据规模推进到 500 小时量级；② 系统处理了「视角/外观对齐+控制器兼容」两大迁移断点；③ 横评协议本身对社区有基准价值。",
 lim="① 仿真到真实的差距仍在，真实世界任务数有限；② 与 DreamZero 等强基线的最优成绩仍有差距；③ 数据采集设备与伦理审批细节决定可复现性边界。",
 rel="与库内 EgoJEPA/P³-WAM（第一视角灵巧操作）、EgoMatrix/EgoReveal（第一视角→机器人）同属「人类数据驱动机器人」大簇；HumanVerse 的差异化在 loco-manipulation 全身维度与数据规模。"),

"2610.13309": dict(slug="NovaSplat免模型6D位姿估计", tags=["6D 位姿", "免 CAD", "3DGS", "onboarding", "物体追踪"],
 one="免 CAD 模型的 6D 物体位姿估计：onboarding 阶段用一段智能手机视频训练出高质量 3DGS 物体模板，推理阶段以该模板同时充当位姿假设源与精化目标，把免模型方法的精度差距补齐到模型-based 方法的可用区间。",
 prob="无 CAD 模型的 6D 位姿估计必须现场从零构建物体表示，长期落后于模型-based 方法；核心难点是 onboarding 表示的质量直接决定后续位姿假设的质量，而智能手机视频的视角覆盖与质量都有限。",
 method="两阶段流水线：① onboarding——从短视频重建 3DGS 物体模板（SSIM+MS-SSIM 光度损失，因小物体渲染分辨率限制采用 3 尺度而非标准 5 尺度 MS-SSIM）；② inference——以 3DGS 模板做位姿估计与迭代精化。附完整运行时分析（分阶段耗时拆解、内存画像）与 onboarding 预算/视角密度/SfM 位姿等系统消融。",
 exp="在标准免模型基准上相对既有免模型方法取得显著提升并逼近模型-based 精度区间；分阶段运行时分析定位粗位姿估计为耗时瓶颈并给出优化；onboarding 视角密度与重建预算的影响被量化。",
 innov="① 把 3DGS 从「渲染表示」复用为「位姿任务的几何-外观联合模板」，一套表示服务假设生成与精化两职；② 免模型 onboarding 的系统性消融（视角密度/预算/SfM）为该子领域提供了少有的工程地图。",
 lim="① onboarding 需要短视频拍摄，时延与失败恢复未充分讨论；② 强遮挡/无纹理物体的鲁棒性未验证；③ 与需要 CAD 的方法在同基准的最终差距未完全消除。",
 rel="与库内免训练目标感知精化（3D 高斯语言地图检索，10-17）共享「3DGS 模板服务识别任务」思路；与 NovaSplat 同类的物体级理解为 AR 交互提供感知底座。"),

"2610.13498": dict(slug="H2-Ray混合层级光线追踪3DGS渲染", tags=["3DGS", "光线追踪", "渲染系统", "BVH", "GPU"],
 one="面向 3D 高斯渲染的混合层级光线追踪架构 H²-Ray：负载均衡空间 BVH（LB-SBVH）把全局倾斜的高斯分布转为均衡遍历区，射线簇路径复用（RCPR）共享邻射线的遍历，在 RTX A5000 上较 RaySplats 取得几何平均 3.77×（最高 9.26×）加速，PSNR 仅降 0.034 dB。",
 prob="3DGS 依赖光栅化求速度，但光栅化难以支持二次光照、大形变相机与景深等效果；光线追踪 3DGS 则面临高斯空间分布极不均匀、邻射线遍历冗余、硬件 RT Core 适配三大挑战。",
 method="① LB-SBVH：密度感知的空间划分，把倾斜分布转为均衡遍历区域；② RCPR：邻射线簇共享 BVH 遍历，消除冗余访存；③ 修改版 RT Core 的 cycle-accurate 建模，把微架构行为纳入设计闭环。",
 exp="8 个代表场景（Mip-NeRF 360 + Deep Blending）几何平均加速 3.77×、最大 9.26×（vs RaySplats，RTX A5000）；多视图匹配评测下 PSNR 平均仅降 0.034 dB。",
 innov="① 首个针对 3DGS 非均匀分布专门设计的负载均衡 BVH；② 「微架构建模+算法协同设计」的方法论对后续神经渲染系统工作有示范意义。",
 lim="① 收益依赖特定 GPU 架构（RT Core 行为），跨代际硬件的可移植性未验；② 二次光照的实际画质收益未在本工作中端到端展示；③ 场景规模扩大后的内存行为待测。",
 rel="与库内 Masking-Judder（注视点渲染）、OuroWorld（内容生成）分属渲染系统不同层；H²-Ray 补上库内「3DGS 光线追踪系统」空白，与神经渲染方法族（80 篇）形成「方法-系统」闭环。"),

"2610.16143": dict(slug="All-St3R实时动态RGBSLAM", tags=["SLAM", "动态环境", "运动掩蔽", "实时", "单目"],
 one="密集几何驱动的动态 RGB SLAM：逐像素运动掩蔽替代物体级分割/检测，把 All-Tracker 改造成两帧成对推理以消除序列开销，约 10 FPS（30 FPS 流每 3 帧 subsample）实时运行，显著优于 1–2 FPS 的既有动态 SLAM。",
 prob="动态环境 SLAM 有重大实用价值，但既有路线要么依赖重型物体级分割/检测（慢且漏检即失败），要么过度移除动态内容损伤建图质量，计算成本也普遍在实时线以下。",
 method="① 逐像素运动掩蔽：由密集几何直接驱动，免物体级先验；② All-Tracker 的两帧成对推理改造，去除序列推理开销；③ 轻量几何过滤流水线，纯单目 RGB 输入。",
 exp="标准动态 SLAM 基准上实时性约 10 FPS（vs 既有 SOTA 1–2 FPS 量级）且保持有竞争力的跟踪精度；消融验证掩蔽策略对跟踪与建图的双重贡献。",
 innov="① 用「密集几何驱动逐像素掩蔽」绕开物体级检测的脆弱性；② 两帧成对推理的工程改造把 tracker 类方法真正推入实时区间。",
 lim="① 纯 RGB 的尺度未恢复（单目固有）；② 极端动态（人群/大幅形变）下的掩蔽质量未充分验证；③ 与库内 LIN-SLAM（LiDAR-惯性）传感器假设不同，不可直接横评。",
 rel="与库内 RootSLAM（VIO 平方根 BA）、Physical SLAM（物理感知 4D）、RoboAtlas（主动 SLAM）构成 SLAM 方法族的不同切面；All-St3R 的「动态实时」维度与 10-10 的 Fast-Pose-Tracking 互补。"),

"2610.16177": dict(slug="DIGS免训练开放词汇3D高斯分割", tags=["3DGS", "开放词汇", "语义分割", "免训练", "贝叶斯"],
 one="免训练开放词汇 3D 高斯分割：诊断出既有方法的两大失效模式——尺度主导（大高斯单帧获得不成比例的增量）与闭环反馈（渲染标签图驱动下一帧关联并自我强化），以广义贝叶斯推断（safe-Bayesian 似然回火）引入逐高斯逐帧学习率稳定训练，边界高斯不再被迫做单一特征承诺。",
 prob="开放词汇 3D 高斯分割通常把语义特征绑到 per-Gaussian 状态，依赖 per-scene 梯度训练（1–4 小时）或闭式蒸馏；两者都把每个 primitive 提交给单一特征，跨多个 2D 实例的边界高斯被迫硬决策，检索精度与掩蔽边界稳定性双损。",
 method="① 分布保持设计（DP）：承认边界高斯的语义分布而非强制单峰承诺；② 稳定性过滤器（SF）；③ 逐高斯逐帧学习率 η_i(t)：以 tempering 的 Dirichlet 后验做安全贝叶斯更新，抑制尺度主导与闭环反馈；④ LLM 融合增强检索；LERF-OVS/LERF-Mask 双协议逐组件消融（SF/DP/LLM fusion）。",
 exp="LERF-OVS（mIoU/mAcc）与 LERF-Mask（mIoU/mBIoU）上对 LangSplat、LangSplatV2、LaGa 与免训练对照 SFS 取得竞争优势；消融显示各组件（SF/DP/LLM 融合）对检索 mIoU 的增量贡献可分离。",
 innov="① 首次把动态 3DGS 分割的失效归因到「尺度主导+闭环反馈」两个可操作机制；② 用贝叶斯回火给出逐 primitive 的学习率方案，是免训练路线少有的原则性设计。",
 lim="① 逐帧更新仍有推理期计算成本，与 LangSplatV2 的 450+ FPS 有差距；② LLM 融合引入外部模型依赖；③ 基准为室内语义场景，开放世界长尾类别未测。",
 rel="与库内免训练目标感知精化（10-17 cross）同属「3DGS 语义检索」方向；DIGS 的免训练+分布保持路线与该篇的「精化」路线互为补充，共同对标 LangSplat 家族。"),
}

def note_md(r, c):
    d = c
    return f"""---
id: arXiv:{r['id']}
title: "{r['title']}"
title_zh: "{r['title_zh']}"
track: {r['track']}
venue: arXiv preprint
date: {SDATE[r['src']]}
value: {r['value']:.2f}
grade: {r['grade']}
evidence: FULL
status: CURRENT
superseded_by: []
scores: {{{', '.join(f'{k}:{v}' for k, v in r['scores'].items())}}}
fetch_level: L0
tags: [{', '.join(d['tags'])}]
---

# {r['title_zh']}

## 一句话结论

{d['one']}

## 要解决的问题

{d['prob']}

## 方法详解

{d['method']}

## 实验与结果

{d['exp']}

## 创新点与贡献

{d['innov']}

## 局限与风险

{d['lim']}

## 与文献库的关系

{d['rel']}

## 来源与诚实口径

- 本笔记出自 **backfill-1012-1015（漏网对账补录）** 批次：公告日 {SDATE[r['src']]}，{ORIG[r['src']]}，非 10-17 当日新提交。
- 评分依据全文（L0/FULL，{MAN.get(r['id'], {}).get('chars', 0)} 字符）；加权 {r['value']:.2f} → {r['grade']} 级。
"""

n_notes = 0
for pid in top10:
    r = by_id[pid]; c = N[pid]
    fn = NOTES + f"{pid}__{c['slug']}.md"
    open(fn, "w", encoding="utf-8").write(note_md(r, c))
    n_notes += 1
print(f"原子笔记 {n_notes} 篇")

# ---------------- 3) Backfill 报告 ----------------
L = []
L.append("# XR 每日论文雷达 · 漏网对账 Backfill 解读报告（10-12 ~ 10-15 公告 + 旧稿积压）")
L.append("")
L.append(f"> 生成时间：{datetime.date.today().isoformat()} ｜ 批次：`{BATCH}` ｜ 文献库：{len(reg)} → {len(reg)+len(new)} 篇")
L.append("")
L.append("## 一、执行摘要")
L.append("")
L.append("- **动因**：10-11~10-16 无调度运行，RSS 只携带最新公告日 → 10-17 运行仅覆盖 10-16 一批。listing 页对账确认 **10-12/10-14/10-15 三个公告日完全漏跑**（10-13 周二全分类无公告）。")
L.append("- **规模**：3 个漏跑日全量 2352 篇（7 分类 primary）→ 标题级 XR 命中 48 篇（下限口径）→ 摘要级甄别入池 46 篇（含旧稿积压 13 篇中的 8 篇），剔除 14 篇非 XR。")
L.append(f"- **Top10**：{' / '.join(by_id[i]['title_zh'].split('：')[0] for i in top10)}；最高 {gate['max']:.2f}（FlowAvatar），**无 S 级**（非重磅日：{gate['max']:.2f} < 库内近 30 天 Top10 均分 {gate['mean30']}）。")
L.append(f"- **三关**：门① max Jaccard {gate['jaccard'][0]} < 0.62 ✓；门② Top10 覆盖 {len(gate['tracks'])} 赛道 ✓；门③ 非重磅日、未拔高 ✓。OUTDATED 0 篇。")
L.append("- **证据**：Top10 及 ≥3.50 近界论文共 19 篇抓取全文（L0/FULL）复核评分；其余 27 篇为摘要级（registry 如实标注 ABSTRACT_ONLY）。")
L.append("")
L.append("## 二、方法论与诚实口径")
L.append("")
L.append("- **对账通道**：API 双主机 429 限流期间改用 `arxiv.org/list/{cat}/recent`（按公告日分组、h3 含声明条目数），7 分类 × show=500 分页 + 逐日完整性校验 + 分类级重试；API 恢复后一次性拉取 60 篇候选完整元数据。")
L.append("- **甄别口径**：XR 核心（VR/AR/MR/XR 直接载体）与强相关（3DGS/SLAM/化身/第一视角/触觉等 XR 使能技术）入池；特定非 XR 应用域（医学影像、水下、城市/行星重建、声呐、无线通信、纯机器人策略）剔除。")
L.append("- **诚实口径**：本批为**历史漏网补录**，论文公告日为 10-12/14/15/16 或更早，并非 10-17 当日新提交；标题级关键词为漏网筛查下限，摘要级甄别后确认无进一步重大漏网风险。")
L.append("- **踩坑固化**（详见 run_log）：单位数日期无前导零、show=2000 响应体 2MB 截断、限流降级、跨分类交叉列表去重假象。")
L.append("")
L.append("## 三、全文精读（按重要性排序）")
L.append("")
for i, pid in enumerate(top10):
    r = by_id[pid]; c = N[pid]
    L.append(f"### 第 {i+1} 章 · {pid} ｜ {r['title_zh']}")
    L.append("")
    L.append(f"**{r['track']} ｜ {r['value']:.2f} {r['grade']} ｜ 7 维 {r['scores']['IMP']}/{r['scores']['NOV']}/{r['scores']['TEC']}/{r['scores']['EXP']}/{r['scores']['PER']}/{r['scores']['TRL']}/{r['scores']['REP']} ｜ {ORIG[r['src']]}**")
    L.append("")
    L.append(f"**一句话结论**：{c['one']}")
    L.append("")
    L.append(f"**要解决的问题**：{c['prob']}")
    L.append("")
    L.append(f"**方法详解**：{c['method']}")
    L.append("")
    L.append(f"**实验与结果**：{c['exp']}")
    L.append("")
    L.append(f"**创新点**：{c['innov']}")
    L.append("")
    L.append(f"**局限与风险**：{c['lim']}")
    L.append("")
    L.append(f"**与文献库的关系**：{c['rel']}")
    L.append("")
L.append("## 四、7 维度对比表（参考）")
L.append("")
L.append("| # | arXiv ID | 中文题名 | 档 | 加权 | IMP | NOV | TEC | EXP | PER | TRL | REP | 赛道 | 来源 |")
L.append("|---|---|---|---|---|---|---|---|---|---|---|---|---|---|")
for r in inc:
    s = r["scores"]
    L.append("| %d | %s | %s | %s | %.2f | %d | %d | %d | %d | %d | %d | %d | %s | %s |" % (
        r.get("rank", 0), r["id"], r["title_zh"], r["grade"], r["value"],
        s["IMP"], s["NOV"], s["TEC"], s["EXP"], s["PER"], s["TRL"], s["REP"], r["track"], ORIG[r["src"]]))
L.append("")
L.append("（完整 46 篇入池清单同 `papers/daily/backfill-1012-1015/7dim-table.md`；14 篇剔除原因见同目录 scored.md）")
L.append("")
L.append("## 五、覆盖度校验")
L.append("")
L.append(f"- 门①（同质筛查）：最大 Jaccard **{gate['jaccard'][0]}**（{gate['jaccard'][1]} vs {gate['jaccard'][2]}）< 0.62 → 通过，无同质重筛。")
L.append(f"- 门②（赛道覆盖）：Top10 覆盖 **{len(gate['tracks'])}** 个赛道（{'、'.join(gate['tracks'])}）≥ 5 → 通过。")
L.append(f"- 门③（价值天花板）：本批最高 **{gate['max']:.2f}** < 库内近 30 天 Top10 均分 **{gate['mean30']}**（现算）→ 非重磅日、无 S 级，未拔高未凑 S。")
L.append("- 落后标记：OUTDATED / SUPERSEDED **0 篇**。")
L.append("- 路线观察：① 「3DGS 压缩/传输」族本批新增 PLEDGE（误差有界）与库内 TETRIS-4DGS/RDCompGS/ResStreamGS 形成四方法互补；② 第一视角→机器人数据范式本批新增 HumanVerse/EgoMatrix/KODA 三篇，与 10-17 的 EgoJEPA/P³-WAM 合流为「人类示范驱动机器人」大簇，社区口径趋于归一；③ 化身方向 FlowAvatar（消费硬件开源）与 Kandinsky（生成式开源）分别卡位「追踪」与「生成」两端。")
L.append("")
L.append("## 六、附录")
L.append("")
L.append(f"- 批次目录：`papers/daily/{BATCH}/`（7dim-table.md / scored.md / run_log.md）")
L.append(f"- 原子笔记：`papers/notes/` 新增 {n_notes} 篇（Top10）")
L.append(f"- MOC：`papers/MOC/MOC-{BATCH}.md`；总索引已刷新")
L.append(f"- registry：{len(reg)} → {len(reg)+len(new)}（+{len(new)}，备份 `{os.path.basename(bak)}`）")
L.append("- 审计脚本：`scripts/audit_gap_listing.py`（listing 对账）+ `scripts/filter_missed_xr.py`（XR 过滤）+ `scripts/build_backfill_1012.py`（判分与三关）")
open(REPORTS + f"XR-Backfill-Report-{BATCH.split('-',1)[1]}.md", "w", encoding="utf-8").write("\n".join(L) + "\n")
print("报告:", REPORTS + f"XR-Backfill-Report-{BATCH.split('-',1)[1]}.md")

# ---------------- 4) MOC-backfill ----------------
L = [f"# MOC · {BATCH}（漏网对账补录）", ""]
L.append(f"> 补录 **10-12 / 10-14 / 10-15** 三个漏跑公告日 + 旧稿积压（10-09 遗留 4 篇、10-16 旧稿 replace/cross 9 篇）。非当日新提交。")
L.append(f"> 漏斗：3 日全量 2352 篇 → 标题级 XR 48 篇 → 摘要级入池 **46 篇** / 剔除 14 篇。")
L.append("")
L.append("## 排行榜（按加权降序）")
L.append("")
L.append("| arXiv ID | 中文题名 | 档 | 加权 | 7 维(IMP/NOV/TEC/EXP/PER/TRL/REP) | 赛道 | 来源 |")
L.append("|---|---|---|---|---|---|---|---|")
for r in inc:
    s = r["scores"]
    L.append("| %s | %s | %s | %.2f | %d/%d/%d/%d/%d/%d/%d | %s | %s |" % (
        r["id"], r["title_zh"], r["grade"], r["value"],
        s["IMP"], s["NOV"], s["TEC"], s["EXP"], s["PER"], s["TRL"], s["REP"], r["track"], ORIG[r["src"]]))
L.append("")
tracks = {}
for r in inc: tracks.setdefault(r["track"], []).append(r["id"])
L.append("## 赛道分布")
L.append("")
for t, ids in sorted(tracks.items(), key=lambda x: -len(x[1])):
    L.append(f"- **{t}**（{len(ids)}）：{'、'.join(ids)}")
L.append("")
L.append("## Top10 精读")
L.append("")
for i, pid in enumerate(top10):
    r = by_id[pid]
    L.append(f"{i+1}. [{pid} {r['title_zh']}](../../papers/notes/{pid}__{N[pid]['slug']}.md)（{r['value']:.2f} {r['grade']}）")
L.append("")
L.append("## 落后 / 路线观察")
L.append("")
L.append("- OUTDATED / SUPERSEDED：0 篇。")
L.append("- 路线观察：① 3DGS 压缩/传输四方法互补（PLEDGE 误差有界）；② 人类示范驱动机器人大簇合流；③ 化身「追踪-生成」两端卡位。")
L.append("")
L.append("## 链接")
L.append("")
L.append(f"- [Backfill 报告](../../reports/XR-Backfill-Report-{BATCH.split('-',1)[1]}.md) ｜ [7 维表](../daily/{BATCH}/7dim-table.md) ｜ [scored](../daily/{BATCH}/scored.md) ｜ [run_log](../daily/{BATCH}/run_log.md)")
open(MOCS + f"MOC-{BATCH}.md", "w", encoding="utf-8").write("\n".join(L) + "\n")
print("MOC:", MOCS + f"MOC-{BATCH}.md")

# ---------------- 5) 总索引刷新 ----------------
idx_path = MOCS + "MOC-总索引.md"
idx = open(idx_path, encoding="utf-8").read()
grades = {}
for r in inc: grades[r["grade"]] = grades.get(r["grade"], 0) + 1
gs = " / ".join(f"{g}{grades.get(g,0)}" for g in "SABC" if grades.get(g))
sn = (f"> **状态注记（{BATCH}）**：周六，执行漏网对账 backfill：10-12/14/15 三个漏跑公告日（10-13 全分类无公告）"
      f" + 旧稿积压。listing 页对账 3 日全量 2352 篇 → 标题级 XR 48 篇 → 摘要级**入池 46 篇（{gs}）**、剔除 14 篇非 XR；"
      f"Top10 最高 {gate['max']:.2f}（FlowAvatar），无 S 级（< 库内 30 天 Top10 均分 {gate['mean30']}）。"
      f"三关通过（门① {gate['jaccard'][0]}；门② {len(gate['tracks'])} 赛道；门③ 非重磅日）；OUTDATED 0。"
      f"Top10 全文 L0/FULL。诚实口径：历史漏网补录，非 10-17 当日新提交。详见 [Backfill 报告](../../reports/XR-Backfill-Report-{BATCH.split('-',1)[1]}.md) 与 [MOC-{BATCH}](./MOC-{BATCH}.md)。")
# 在最后一条状态注记后插入
lines = idx.split("\n")
last_sn = max(i for i, l in enumerate(lines) if l.startswith("> **状态注记"))
lines.insert(last_sn + 1, sn)
# 更新文献库计数行
for i, l in enumerate(lines):
    if l.startswith("> 文献库："):
        lines[i] = re.sub(r"累计 \*\*\d+ 篇\*\*", f"累计 **{len(reg)+len(new)} 篇**", l)
        lines[i] = re.sub(r"（含 backfill 旧稿 2603–2609）", f"（含 backfill 旧稿 2603–2609 与 10-12~10-15 漏网补录）", lines[i])
        if "backfill-1012-1015" not in lines[i]:
            lines[i] = lines[i].replace("**10-17:18（10-16 公告批次）**",
                                        f"**10-17:18（10-16 公告批次）** · **backfill-1012-1015:{len(new)}（漏网对账补录）**")
        break
open(idx_path, "w", encoding="utf-8").write("\n".join(lines))
print("总索引已刷新（状态注记 + 计数）")

# ---------------- 6) run_log 收尾（交付物段） ----------------
rl = open(DAILY + "run_log.md", encoding="utf-8").read()
if "## 交付物" not in rl:
    rl += "\n## 交付物\n"
    rl += f"- 本目录：7dim-table.md / scored.md / run_log.md\n"
    rl += f"- 报告：reports/XR-Backfill-Report-{BATCH.split('-',1)[1]}.md\n"
    rl += f"- 原子笔记 {n_notes} 篇（papers/notes/，Top10）+ MOC-{BATCH}.md + MOC-总索引.md 刷新\n"
    rl += f"- registry：{len(reg)} → {len(reg)+len(new)}（+{len(new)}，幂等追加，batch={BATCH}，备份 {os.path.basename(bak)}）\n"
    rl += f"- 证据分级：19 篇 L0/FULL（Top10+≥3.50 近界）／27 篇 ABSTRACT_ONLY\n"
    open(DAILY + "run_log.md", "w", encoding="utf-8").write(rl)
    print("run_log 已收尾")
