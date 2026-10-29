# -*- coding: utf-8 -*-
"""write_status_1030.py — 生成 2026-10-30 状态日产物（10-29 公告批次未释放）。

产物：
  papers/daily/2026-10-30/7dim-table.md   前沿参考表（24 篇，非当日新拉取）
  papers/daily/2026-10-30/run_log.md      执行日志
  reports/XR-Daily-Report-2026-10-30.md   状态报告
"""
import json, os, io

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DIMS = ["IMP", "NOV", "TEC", "EXP", "PER", "TRL", "REP"]
NONXR = "—（非 XR）"

reg = []
for l in io.open(os.path.join(ROOT, "papers/library/registry.jsonl"), encoding="utf-8"):
    l = l.strip()
    if l:
        reg.append(json.loads(l))

# 前沿参考 = 10-29 运行批次（10-28 公告批次：主批 20 + backfill-1029 4 篇），按 value 降序
ref = [r for r in reg if r.get("batch") in ("2026-10-29", "backfill-1029")]
ref.sort(key=lambda x: (-x.get("value", 0), x["id"]))

os.makedirs(os.path.join(ROOT, "papers/daily/2026-10-30"), exist_ok=True)

# ---------- 7dim-table.md ----------
L = []
L.append("# 7 维度对比表 · 2026-10-30（文献库最新前沿参考，非当日新拉取）")
L.append("")
L.append("> ⚠️ 说明：本运行日（周五 2026-10-30 02:30）经漏网对账 + 三源探针核验，**无新增可处理论文**：")
L.append("> ① listing 7 分类最新公告日仍为 **2026-10-28**（与 10-29 运行一致；**10-29 公告批次未释放**——arXiv 侧跳空/延迟，非本地故障）；")
L.append("> ② API `submittedDate` 全分类区间查询 10-28/10-29 均 **0 篇**（前沿停滞 10-27，即 10-28 公告组来源，已全部入馆）；")
L.append("> ③ RSS 于 10-29 04:00 UTC 全局重建后 6/7 分类 0 条目（math.AP/physics.optics/cs.LG/cs.CL/eess.AS/q-bio.NC 等其他学科同样空源）；cs.AI feed 残留 10-28 公告批次陈旧内容（407 条，7 条 KW 命中全部为此前运行已处置论文）；")
L.append("> ④ 10-28 公告组（462 篇）复采复核：443 篇未入馆者摘要级 XR 命中 14 篇，**全部为 10-29 运行已显式剔除的非 XR 稿**（RL 可塑性/水下声呐/四足姿态/人形迁移/ViT 骨干/视觉 AR 生成/机器人主动感知/无人机主动 SLAM/医学 CT 烘焙/跨本体 VLA/卫星 NVS/机械拇指/网球时空/视觉生成范式）→ **0 漏网**。")
L.append("> 下表为**文献库最新前沿（2026-10-29 运行处理的 10-28 公告批次：主批 20 篇 + backfill-1029 4 篇）的 7 维参考表**，供查阅，**非「当日新论文」对比表**。")
L.append("")
L.append("> 维度与权重固定：`Value = 0.20·IMP + 0.20·NOV + 0.15·TEC + 0.15·EXP + 0.15·PER + 0.08·TRL + 0.07·REP`；分档：S≥4.2 / A 3.6–4.2 / B 3.0–3.6 / C<3.0")
L.append("")
L.append("> 拉取窗口：无（状态日；最新公告日 2026-10-28，已由上批 10-29 运行完整处理）")
L.append("")
L.append("| # | arXiv | 标题 | 赛道 | IMP | NOV | TEC | EXP | PER | TRL | REP | 总分 | 等级 | 批次 | 证据 | 状态 |")
L.append("|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|")
for i, r in enumerate(ref, 1):
    s = r.get("scores") or {}
    star = " ⭐" if r.get("in_top10") else ""
    batch = "主批 2026-10-29" if r.get("batch") == "2026-10-29" else "backfill-1029"
    L.append("| %d | [%s](https://arxiv.org/abs/%s) | %s%s | %s | %s | %s | %s | %s | %s | %s | %s | **%.2f** | %s | %s | %s | %s |" % (
        i, r["id"].split(":")[-1], r["id"].split(":")[-1],
        r.get("title_zh") or r.get("title", ""), star,
        r.get("track", ""),
        s.get("IMP", ""), s.get("NOV", ""), s.get("TEC", ""), s.get("EXP", ""),
        s.get("PER", ""), s.get("TRL", ""), s.get("REP", ""),
        r.get("value", 0), r.get("grade", ""), batch,
        r.get("evidence", ""), r.get("status", "CURRENT")))
L.append("")
L.append("> 证据列：FULL = 完整正文（L0/L1）；本表 24 篇证据等级均以 registry 登记为准（10-29 运行：19 L0/FULL + 1 L1/PARTIAL 主批 + backfill 全 L0/FULL）。")
L.append("> 门③ 参考：库内近 30 天 Top10 均分 **4.420**（窗口 2026-09-30~10-30，422 条入窗，现算）；本日 0 候选不触发校准关。")

with io.open(os.path.join(ROOT, "papers/daily/2026-10-30/7dim-table.md"), "w", encoding="utf-8") as f:
    f.write("\n".join(L) + "\n")
print("written 7dim-table.md:", len(ref), "ref rows")

# ---------- run_log.md ----------
R = []
R.append("# 运行日志 · 2026-10-30（周五 02:30 · 状态日：10-29 公告批次未释放）")
R.append("")
R.append("## 1. 漏网对账（Step 1）")
R.append("")
R.append("- listing 7 分类日期头（`scripts/audit_gap_listing.py`，TARGET_LO=2026-10-28，show=250，完整性校验通过）：")
R.append("  **最新公告日全部为 2026-10-28**（cs.CV 156 / cs.GR 10 / cs.HC — / cs.MM 8 / cs.RO 85 / cs.AI 254 / eess.IV 8 量级；per-cat SHORT 为跨分类交叉列表认领的统计假象，与 10-29 运行逐项一致）。")
R.append("- **10-29 公告批次未释放**（三源互证）：")
R.append("  ① listing recent/pastweek 视图（含 cache-buster 复验）均无 10-29 日组；")
R.append("  ② API 全分类 `submittedDate:[202610280000 TO 202610292359]` = **0 篇**（cs.CV/cs.AI 单查同样 0），前沿停滞 10-27；")
R.append("  ③ RSS 于 10-29 04:00 UTC 全局重建后 6/7 分类 0 条目；其他学科（math.AP/physics.optics/cs.LG/cs.CL/eess.AS/q-bio.NC）同样空源——排除沙箱代理问题。")
R.append("- 10-28 公告组复采 462 篇，未入馆 443 篇；`scripts/filter_missed_xr_abstract.py` 摘要级过滤命中 **14 篇**，逐篇核对均为 10-29 运行已显式剔除的非 XR 稿（RL 可塑性 2610.36309 / 水下声呐 2610.36454 / 四足姿态 2610.36599 / 人形交互迁移 2610.36615 / ViT 骨干 2610.36719 / 视觉 AR 生成 2610.36793 / 机器人主动感知 2610.36859 / 无人机主动 SLAM 2610.37111 / 医学 CT 烘焙 2610.37406 / 跨本体 VLA 2610.37509 / 卫星 NVS 2610.37545 / 机械拇指 2610.37582 / 网球时空 2610.37619 / 视觉生成范式 2610.37626）→ **0 漏网，无 backfill**。")
R.append("- 落盘：`data/missed_listing_1030.json`（462 篇全量）、`data/missed_xr_abstract_1030.json`（14 篇命中）、`data/raw/2026-10-30_rss.jsonl`（cs.AI 陈旧 feed 7 条 KW 命中）。")
R.append("")
R.append("## 2. 数据源探测（Step 2）")
R.append("")
R.append("- export.arxiv.org / arxiv.org / rss.arxiv.org 三源探针均 200；`fetch_rss.py` 7 分类：cs.AI 407 条（陈旧 feed）+ 其余 6 类 0 条 → KW 命中 7 条。")
R.append("- 7 条 KW 命中去向：3 篇已在 registry（2610.36384 SOMA / 2610.37149 GCSR-OCC / 2604.23018 AmaraSpatial-10K，10-29 运行已入馆）；2 篇为 10-29 运行已剔非 XR（2610.36859 / 2610.37545）；2 篇为旧稿 replace 再公告（2506.19846 HiMA-Ecom / 2605.29927 Planning 研究，非 10-29 公告内容）→ **0 篇新候选**。")
R.append("- `fetch_arxiv.py --since` 未跑（listing 已证无新公告日组；API 区间查询 0 篇）。")
R.append("")
R.append("## 3. 甄别 / 全文 / 评分 / Top10（Steps 3-7）")
R.append("")
R.append("- 候选池 0 篇 → 不触发全文抓取、7 维评分、覆盖度三关与 Top10 选拔。")
R.append("- **未伪造 Top10 / 评分 / S 级**（诚实口径硬约束）。")
R.append("- 门③ 现算参考：库内近 30 天 Top10 均分 **4.420**（窗口 2026-09-30~10-30，422 条入窗）。")
R.append("")
R.append("## 4. 产物与发布（Steps 8-9）")
R.append("")
R.append("- registry **无变更**（693 条：S16/A329/B273/C75…以当日落盘为准；本次未修改故无备份需要）；原子笔记 384 篇无新增。")
R.append("- 产物：本 run_log + `papers/daily/2026-10-30/7dim-table.md`（24 篇前沿参考）+ `reports/XR-Daily-Report-2026-10-30.md` + MOC 总索引维护。")
R.append("- 前端：BATCH_LABELS 补 10-30 标签 → 重建 hub → DATA 计数核验 → CDP 冒烟 → 双渠道发布（详见报告 §5.5）。")
R.append("")
R.append("## 5. 异常与教训")
R.append("")
R.append("- **新异常模式（首次）**：工作日（周四 10-29）公告批次整体未释放——listing 无 10-29 日组 + API 全分类 submittedDate 10-28/10-29 均 0 + RSS 全局空源（含其他学科）。区别于既往「周末/周一凌晨节律」与「RSS 单分类空源」模式，判定为 **arXiv 侧跳空或公告延迟**，非本地数据源故障。")
R.append("- RSS cs.AI 残留陈旧 feed（407 条 = 10-28 公告批次内容）：单分类非空不等于有新公告，必须与 listing 日期头 + API submittedDate 交叉验证（本次三源互证排除误判）。")
R.append("- 下次运行（10-31 周六 02:30）须复核：10-29 公告是否延迟释放（若发布则按标准流水线补处理该批次，诚实标注公告日≠拉取日）；若 10-29/10-30 均无公告，则为连续跳空，继续状态日模式并挂账观察。")

with io.open(os.path.join(ROOT, "papers/daily/2026-10-30/run_log.md"), "w", encoding="utf-8") as f:
    f.write("\n".join(R) + "\n")
print("written run_log.md")

# ---------- 报告 ----------
import glob
notes = glob.glob(os.path.join(ROOT, "papers/notes/*.md"))
g = {"S": 0, "A": 0, "B": 0, "C": 0}
for r in reg:
    g[r.get("grade", "C")] = g.get(r.get("grade", "C"), 0) + 1

P = []
P.append("# XR 每日论文雷达 · 运行报告 · 2026-10-30（周五 02:30）")
P.append("")
P.append("> **诚实口径声明**：本运行日（2026-10-30，周五 02:30）**无新增可处理论文**。经三源交叉验证，**arXiv 10-29（周四）公告批次未释放**（listing 7 分类最新公告日仍为 2026-10-28、API 全分类 submittedDate 10-28/10-29 区间 0 篇、RSS 全局重建后空源）——属 arXiv 侧跳空/延迟，非本地数据源故障；该批次（10-28 公告组）已于 10-29 运行完整处理（主批 20 篇 + backfill-1029 4 篇），本日复采复核 **0 漏网**。**本报告不包含任何「当日新论文」解读、不虚构 Top10/评分/S 级**；文末附表为文献库最新前沿参考。")
P.append("")
P.append("---")
P.append("")
P.append("## 一、执行摘要")
P.append("")
P.append("| 项 | 结论 |")
P.append("|---|---|")
P.append("| 运行性质 | **状态报告日**（无新稿；漏网对账 + 三源探针 + 知识库存量维护 + 前端重建与双渠道发布） |")
P.append("| 公告状态 | listing 7 分类最新公告日均为 **2026-10-28**（与 10-29 运行逐项一致）；**10-29 公告批次未释放**（arXiv 侧跳空/延迟，首次遇到的工作日公告缺失） |")
P.append("| 漏网对账 | 10-28 公告组 462 篇复采，未入馆 443 篇摘要级 XR 命中 14 篇，**全部为 10-29 运行已显式剔除的非 XR 稿** → **0 漏网**；无漏跑公告日（10-29 根本没有发生公告），无需 backfill |")
P.append("| 数据源 | API 双主机 200（全分类 submittedDate 10-28/10-29 = 0，前沿停滞 10-27）；RSS 10-29 04:00 UTC 全局重建后 6/7 分类 0 条目（其他学科同样空源）；cs.AI feed 残留 10-28 批次陈旧内容（407 条），7 条 KW 命中全部已处置 |")
P.append("| 新入馆论文 | **0 篇**（registry 维持 **693 条**：S %d / A %d / B %d / C %d） |" % (g["S"], g["A"], g["B"], g["C"]))
P.append("| 新原子笔记 | 0 篇（维持 **%d 篇**） |" % len(notes))
P.append("| 库内近 30 天 Top10 均分 | **4.420**（现算，窗口 2026-09-30~10-30 共 422 条入窗；门③ 为校准关，本日无候选不触发） |")
P.append("| 交付 | 状态报告 1 + 前沿参考 7 维表 1（24 篇）+ run_log 1 + MOC 总索引维护 + 前端重建与双渠道发布 |")
P.append("")
P.append("**下一批预期**：10-31（周六）运行须复核 10-29 公告是否延迟释放；若已发布则按标准流水线补处理（诚实标注公告日 10-29 ≠ 拉取日 10-31）；若 10-29/10-30 连续无公告，继续状态日模式并挂账观察 arXiv 侧状态。门③ 均分务必现算（勿沿用 4.420）。")
P.append("")
P.append("---")
P.append("")
P.append("## 二、漏网对账（Step 1，本日核心工作）")
P.append("")
P.append("对账目的：确认自上一批次公告日（2026-10-28）至今是否有漏跑公告日或漏收 XR 论文。")
P.append("")
P.append("### 2.1 公告日头核验（目标窗口 ≥ 2026-10-28）")
P.append("")
P.append("| 分类 | 最新公告日 | 10-28 日组声明/实采 |")
P.append("|---|---|---:|")
P.append("| cs.CV | Wed, 28 Oct 2026 | 156 / 156 |")
P.append("| cs.GR | Wed, 28 Oct 2026 | 10 / 10 |")
P.append("| cs.HC | Wed, 28 Oct 2026 | —（并入 cs.GR 组采齐） |")
P.append("| cs.MM | Wed, 28 Oct 2026 | 8 / 8 |")
P.append("| cs.RO | Wed, 28 Oct 2026 | 85 / 85 |")
P.append("| cs.AI | Wed, 28 Oct 2026 | 254 / 254 |")
P.append("| eess.IV | Wed, 28 Oct 2026 | 8 / 8 |")
P.append("")
P.append("- **无 10-29 公告日组**：recent / pastweek 视图（含 cache-buster 复验）均无 10-29 日组。")
P.append("- **10-29 公告批次未释放的三源互证**：")
P.append("  1. listing：7 分类（recent + pastweek + 缓存穿透复验）最新日组全部为 Wed, 28 Oct 2026；")
P.append("  2. API：全分类 `submittedDate:[202610280000 TO 202610292359]` = **0 篇**，cs.CV/cs.AI 单查亦 0；`submittedDate` 降序前沿 = 10-27（2610.37668 等，即 10-28 公告组来源，已全部入馆）；")
P.append("  3. RSS：10-29 04:00 UTC 全局重建后，7 分类中 6 个 0 条目；其他学科（math.AP / physics.optics / cs.LG / cs.CL / eess.AS / q-bio.NC）同样 0 条目——排除沙箱代理侧问题，指向 arXiv 公告侧跳空/延迟。")
P.append("- arXiv 主页无维护/中断通知。")
P.append("")
P.append("### 2.2 10-28 公告组复采复核（验证上一批处理完整性）")
P.append("")
P.append("- 复采 10-28 公告组 **462 篇**（与 10-29 运行采集逐项一致），未入馆 **443 篇**（registry 现含该组 19 篇 XR = 10-29 运行主批）。")
P.append("- 摘要级过滤（`scripts/filter_missed_xr_abstract.py`）命中 **14 篇**，逐篇核对均为 10-29 运行已显式剔除的非 XR 稿：")
P.append("")
P.append("| ID | 标题（摘要级命中） | 10-29 运行剔除理由 |")
P.append("|---|---|---|")
P.append("| 2610.36309 | Bridging Exploration and Loss of Plasticity in On-Policy RL | RL 可塑性（非 XR） |")
P.append("| 2610.36454 | SVIn+: Underwater State Estimation with 3D Sonar | 水下声呐（非 XR） |")
P.append("| 2610.36599 | Camera-to-Quadruped Robot Pose Estimation | 四足姿态（非 XR） |")
P.append("| 2610.36615 | Mimetic Embodiment Transfer of Human-Humanoid Interaction | 人形交互迁移（非 XR） |")
P.append("| 2610.36719 | SAGE: Saliency-Annealed Gated Encoder | ViT 骨干（非 XR） |")
P.append("| 2610.36793 | Visual Autoregressive Generation with Next Token Imagination | 视觉 AR 生成（非 XR） |")
P.append("| 2610.36859 | ActiveAlign: Aligning Egocentric Manipulation via Active Perception | 机器人主动感知（非 XR） |")
P.append("| 2610.37111 | RAVEN: Active SLAM for Aerial Exploration | 无人机主动 SLAM（非 XR） |")
P.append("| 2610.37406 | CTBakeGS: Baking CT Volume Renderings into 3DGS | 医学 CT 烘焙（非 XR） |")
P.append("| 2610.37509 | Ego-CEVR: Cross-Embodiment Visual Representations | 跨本体 VLA（非 XR） |")
P.append("| 2610.37545 | GroundControl: Satellite-Conditioned Multi-View Diffusion | 卫星 NVS（非 XR） |")
P.append("| 2610.37582 | EgoThumb: Supernumerary Robotic Thumb | 机械拇指（非 XR） |")
P.append("| 2610.37619 | Perceiving and Predicting Dynamic Sports | 网球时空（非 XR） |")
P.append("| 2610.37626 | Know, then Draw: A New Learning Paradigm for Visual Generation | 视觉生成范式（非 XR） |")
P.append("")
P.append("**结论：10-28 公告批次无 XR 漏网；无漏跑公告日（10-29 无公告发生）；无需 backfill。**")
P.append("")
P.append("---")
P.append("")
P.append("## 三、数据源探测记录（Step 2）")
P.append("")
P.append("- `fetch_rss.py` 7 分类：cs.AI 407 条（**陈旧 feed**：内容为 10-28 公告批次，pubDate 10-29，id 上限 2610.37668 = 10-27 提交），其余 6 类 0 条；KW 命中 7 条。")
P.append("- 7 条 KW 命中去向核验（防误纳陈旧 feed 内容）：")
P.append("")
P.append("| ID | 标题 | 处置 |")
P.append("|---|---|---|")
P.append("| 2610.36384 | SOMA（第一视角人体运动基准） | 已在 registry（10-29 运行入馆，门② 回补 Top10） |")
P.append("| 2610.37149 | GCSR-OCC（开放词汇占用预测） | 已在 registry（10-29 运行入馆） |")
P.append("| 2604.23018 | AmaraSpatial-10K（3D 资产数据集） | 已在 registry（backfill-1029 入馆） |")
P.append("| 2610.36859 | ActiveAlign（机器人主动感知） | 10-29 运行已剔非 XR |")
P.append("| 2610.37545 | GroundControl（卫星 NVS） | 10-29 运行已剔非 XR |")
P.append("| 2506.19846 | HiMA-Ecom（多智能体记忆基准） | 旧稿 replace 再公告（非 10-29 公告内容） |")
P.append("| 2605.29927 | Does The Way You Plan Matter? | 旧稿 replace 再公告（非 10-29 公告内容） |")
P.append("")
P.append("- 判定：**0 篇新候选**，不进入 Steps 3-7。")
P.append("")
P.append("---")
P.append("")
P.append("## 四、文献库最新前沿参考（10-28 公告批次 · 24 篇 · 非当日新拉取）")
P.append("")
P.append("以下为 10-29 运行处理的 10-28 公告批次 7 维参考表（主批 20 篇 + backfill-1029 4 篇），完整版见 [papers/daily/2026-10-30/7dim-table.md](../daily/2026-10-30/7dim-table.md)：")
P.append("")
P.append("| # | arXiv | 标题 | 赛道 | 总分 | 等级 | 批次 |")
P.append("|---|---|---|---|---|---|---|")
for i, r in enumerate(ref, 1):
    star = " ⭐" if r.get("in_top10") else ""
    batch = "主批 10-29" if r.get("batch") == "2026-10-29" else "backfill-1029"
    P.append("| %d | %s | %s%s | %s | **%.2f** | %s | %s |" % (
        i, r["id"].split(":")[-1], (r.get("title_zh") or r.get("title", ""))[:38], star,
        r.get("track", ""), r.get("value", 0), r.get("grade", ""), batch))
P.append("")
P.append("---")
P.append("")
P.append("## 五、附录")
P.append("")
P.append("### 5.1 覆盖度三关（本日不触发）")
P.append("")
P.append("- 门① 同质去重 / 门② 赛道覆盖 / 门③ 价值天花板：候选池 0 篇，三关均不触发。")
P.append("- 门③ 参考值现算：库内近 30 天 Top10 均分 **4.420**（窗口 2026-09-30~10-30，422 条入窗；Top10 为 2610.03162 4.65 / 2610.03283 4.58 / 2610.19674 4.57 / 2610.23772 4.57 / 2610.34263 4.35 / 2610.18872 4.30 / 2610.22778 4.30 / 2609.31418 4.30 / 2610.37602 4.30 / 2610.03192 4.28）。")
P.append("")
P.append("### 5.2 证据等级分布")
P.append("")
P.append("- 本日无新抓取。参考表 24 篇证据等级：22 篇 FULL（L0）+ 1 篇 L1/PARTIAL（2610.36014 Immersive Commons，ar5iv 仅摘要页，10-29 运行已按摘要级评估并显式声明）+ 1 篇 backfill L0/FULL；无 ABSTRACT_ONLY。")
P.append("")
P.append("### 5.3 失败/降级清单")
P.append("")
P.append("- 无抓取失败。数据源异常 1 项：RSS cs.AI 残留 10-28 批次陈旧 feed（已核验处置，见 §三）；10-29 公告批次未释放（arXiv 侧，已三源互证并挂账观察）。")
P.append("")
P.append("### 5.4 产物清单")
P.append("")
P.append("| 产物 | 路径 |")
P.append("|---|---|")
P.append("| 状态报告 | `reports/XR-Daily-Report-2026-10-30.md` |")
P.append("| 前沿参考 7 维表 | `papers/daily/2026-10-30/7dim-table.md`（24 篇） |")
P.append("| 运行日志 | `papers/daily/2026-10-30/run_log.md` |")
P.append("| 对账数据 | `data/missed_listing_1030.json` / `data/missed_xr_abstract_1030.json` / `data/raw/2026-10-30_rss.jsonl` |")
P.append("| MOC 总索引 | `papers/MOC/MOC-总索引.md`（10-30 状态注记 + 批次索引行 + 页脚刷新） |")
P.append("| 前端 | `web/xr-paper-hub.html`（重建） |")
P.append("")
P.append("### 5.5 发布记录")
P.append("")
P.append("- 渠道① WorkBuddy 托管（workbuddy_sites_deploy）：见收尾汇报（若工具不可用则挂账， historically 自 10-21 起连续不可用）。")
P.append("- 渠道② GitHub Pages：见收尾汇报（commit + push_to_github.py --incremental + deploy run + Pages 200 核验）。")
P.append("")
P.append("---")
P.append("")
P.append("*报告生成：2026-10-30 02:30 自动化运行（xr-paper-daily-brief skill · 9 步流水线）。*")

with io.open(os.path.join(ROOT, "reports/XR-Daily-Report-2026-10-30.md"), "w", encoding="utf-8") as f:
    f.write("\n".join(P) + "\n")
print("written report, chars:", len("\n".join(P)))
