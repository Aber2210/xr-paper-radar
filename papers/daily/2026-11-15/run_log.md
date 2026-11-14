# 运行日志 · 2026-11-15（周日 02:30 · 周末状态日：0 新稿）

## 1. 漏网对账（Step 1）

- listing 7 分类日期头（`scripts/audit_listing_1115.py`，show=500 单页×7 分类，PREV_DAY=2026-11-13 / NEW_DAYS=2026-11-14,2026-11-15）：
  **最新公告日全部为 2026-11-13（周五）**，**无 11-14（周六）/ 11-15（周日）公告日组**（`newest=2026-11-13`，NEW_DAYS declared=None / got=0）→ 符合 arXiv `skipDays` 周末不公告节律，**无漏跑公告日**。
- 缓存与故障排除：① cs.CV `recent?cb=7731` 随机参数缓存穿透 → 最新日组仍 `Fri, 13 Nov 2026`；② cs.CV `pastweek` 视图一致；③ 跨学科复核 math.AP / cs.CL `pastweek` 最新日组同为 `Fri, 13 Nov 2026` → 非本分类/本机故障。
- 11-13 公告组完整性复采（验证上批处理完整性）：逐分类 **declared=got**（CV 196 / GR 6 / HC 43 / MM 2 / RO 106 / AI 321 / IV 21，槽位合计 **695**，全局去重 **601 篇唯一论文**），与 11-14 运行采集数字逐项一致；
- 未入馆 **581 篇**（601 − 20 篇 11-14 运行已入馆主批；该批无 listing 侧漏网），摘要级 XR 过滤（`scripts/filter_missed_1115.py`，**50 id/批 + 12s 间隔**，meta fetched **581/581**、覆盖率 **1.0000**、缺失 0）命中 **28 篇**，与 11-14 运行显式剔除的 28 篇非 XR **逐篇 id 一致（双向差集 0）**：

  - 2611.15040 Moving Beyond the DRW Model: Learning Quasar Variability（类星体光变生成建模/天体物理）
  - 2611.15082 Prediction or Persistence? What Future-Prediction Scores Miss（世界模型评分指标研究）
  - 2611.15117 PolyMorphWBC: Whole-Body Control from End-Effector Trajectories（四足移动操作全身控制）
  - 2611.15135 ARTS: Open-Source Three-Arm Platform for Autonomy Research（三臂自主研究平台）
  - 2611.15216 Where is My Mug? Training-Free Personalized Image Segmentation（个性化图像分割）
  - 2611.15277 DroneDiffusion: Uncertainty-Guided Diffusion Path Planner（无人机扩散路径规划）
  - 2611.15280 Autonomous Trail Racing with a Bicycle Robot（自行车机器人越野竞速）
  - 2611.15579 FoveaDet: Software-Hardware Co-Design of Foveated CNN-Transformer（注视点目标检测硬件协同，非近眼显示）
  - 2611.15650 Single-View RGB-D Force-Deformation Estimation（机器人操作力-形变估计）
  - 2611.15659 GraSLA: Lightweight Spatial-Language-Action Model（抓取假设几何的空间-语言-动作模型）
  - 2611.15764 AIFR: Adaptive Identity Feature Recovery（妆容/动漫人像扩散生成）
  - 2611.15766 Prior-as-Skill: On-Policy Self-Distillation（LLM 自蒸馏）
  - 2611.15789 VibePrevisBench: Agentic Coding for 4D Scene Generation in Blender（生成工具链基准）
  - 2611.15937 MOSAIC: Obstacle and Spatial-Aware Framework for Manipulation（杂乱场景操作）
  - 2611.16282 Robot Navigation and Obstacle Avoidance from External Cameras（外部相机机器人导航）
  - 2611.16417 VBot Exo2Ego Policy: Exocentric-to-Egocentric Video Generation（数据采集与操作策略）
  - 2611.16424 PhysCapBench: Cross-Domain Benchmark for Video Captioning（物理视频描述基准）
  - 2611.16439 HALO: Human-Aligned Data Collection for Mobile Manipulation（全身移动操作数据采集）
  - 2611.16452 Can an LVLM Perceive Event Boundaries Like a Human?（LVLM 认知评测）
  - 2611.16655 MuViRL: View-Invariant Visual Speech Representation（视觉语音表征）
  - 2611.16728 EgoX: Egocentric Cross-Embodiment Manipulation（第一视角跨本体操作策略）
  - 2611.16869 Raysemble: Metric 3D Bone Reconstruction from a Single X-ray（单 X 光医学骨重建）
  - 2611.17060 Ropedia Xperience 2: Physical AI Environments（物理 AI 环境数据规模化）
  - 2611.17110 SALA: Semantically Aligned Latent Actions（具身基础模型潜动作）
  - 2611.17163 UAV-Flow++: Language-Guided UAV Flight Benchmark（无人机语言引导飞行基准）
  - 2611.17235 Al-Ghasali: Simulating Islamic Jurisprudential Rulings（法律推理模拟）
  - 2611.17238 HEIR: Harness Egocentric Intent for Human-Robot Interactions（第一视角意图机器人交互）
  - 2611.17284 Augmented Hybrid TV Services: Habits and Expectations（电视服务用户调研；augmented 关键词误命中）

  → 维持上批裁决（均为非 XR 或泛机器人/生成工具链方向）→ **0 漏网、无 backfill**。
- 落盘：`data/audit_1115_days.json` / `data/audit_1115_alldays.json` / `data/missed_prev_1115.json`（581 篇）/ `data/newday_1115.json`（空）/ `data/missed_new_1115.json`（空）/ `data/missed_xr_abstract_1115.json`（28 篇）/ `data/gates_1115.json`。

## 2. 数据源探测（Step 2）

- API 双主机探针 200（`export.arxiv.org` / `arxiv.org/api/query`）；`submittedDate` 降序前沿 = **2026-11-12**（cs.CV / cs.GR / cs.RO top-5 最新 published 均为 11-12，即 11-13 公告组来源，已全部入馆）；`submittedDate:[202611140000 TO 202611142359]` 与 `[20261115...]` cs.CV 均命中 **0** 篇；`fetch_arxiv.py --since 2026-11-13 --max 200` → **WROTE=0**（降序首页即越过下界）。
- RSS（`rss.arxiv.org` 7 分类）：**全部 0 条目**，`lastBuildDate` = Sat, 14 Nov 2026 05:00:00–05:00:08 UTC（7 分类同批重建，HTTP 200 / 892 bytes，非代理故障，属周末节律空源）。
- 判定：**0 篇新候选**，不进入 Steps 3-7。

## 3. 甄别 / 全文 / 评分 / Top10（Steps 3-7）

- 候选池 0 篇 → 不触发全文抓取、7 维评分、覆盖度三关与 Top10 选拔。
- **未伪造 Top10 / 评分 / S 级**（诚实口径硬约束）。
- 门③ 现算参考：库内近 30 天 Top10 均分 **4.430**（窗口 2026-10-16~2026-11-15（443 条入窗）；Top10 = 2610.23772 视频扩散化身 4.57 / 2611.06817 Open-HumanScale 4.57 / 2611.11169 Map2SLAM 4.57 / 2603.01178 riMESA 4.50 / 2610.39399 ACD-GS 4.37 / 2611.09458 跨注入左右一致立体匹配 4.37 / 2611.07902 XM4D 4.36 / 2610.34263 RacerGS 4.35 / 2611.08578 HaNDF 4.34 / 2610.22778 dGS-dBS 4.30）。

## 4. 产物与发布（Steps 8-9）

- registry **935 条**（S18/A438/B365/C114）：本日无新增入馆、无数据修补（交付前 `title == id` / `len(title)<12` 抽查 0 命中）。
- 原子笔记 **587 篇**（无新增）；daily 目录 **62 个**（新增 2026-11-15）。
- 产物：本 run_log + `papers/daily/2026-11-15/7dim-table.md`（28 篇前沿参考）+ `reports/XR-Daily-Report-2026-11-15.md` + MOC 总索引维护。
- 前端：BATCH_LABELS 补 2026-11-15 标签 → 重建 hub → DATA 计数核验 → node --check 双 script 块 → CDP 冒烟 → 双渠道发布（详见报告 §5.5）。

## 5. 异常与教训

- 周末状态日模式第 **7** 次验证（10-04 / 10-05 / 10-18 / 10-25 / 11-01 / 11-08 + 本日；周一凌晨变体另有 10-26 / 11-02 / 11-09，工作日公告跳空状态日 10-30 / 11-13）。判据固定为「listing 日期头为唯一决定依据 + 缓存穿透/pastweek + 跨学科分类 + API 区间 + RSS 条数」五重互证。
- **RSS 空 ≠ 无公告** 的反向教训仍成立（11-07 反例：RSS 空但 listing 有 11-06 组，真实运行 23 篇）；本日结论由 listing 日期头（7 分类均 11-13、无周末日组）决定，RSS 空源仅作辅证。
- 摘要级过滤覆盖率 581/581 = 1.0000，未出现 11-12 记录过的 id_list 429 静默丢批（50 id/批 + 12s 间隔生效）。
- 门③ 现值 **4.430**（较上批 4.4100 上升 0.02，因 riMESA 4.50 / HaNDF 4.34 等进入 30 天窗口）；下次运行仍须现算，勿沿用。
- 渠道①（workbuddy_sites_deploy）自 10-21 起连续不可用且 URL 已 403；若恢复可用须优先补部署（挂账批次 10-21~11-15 共 26 批）。硬件类渲染缺口仍仅 CVQPG + HoOPOE 两篇破冰。
