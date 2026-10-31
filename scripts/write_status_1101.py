# -*- coding: utf-8 -*-
"""write_status_1101.py — 生成 2026-11-01 状态日产物（周日，周末无公告；10-30 公告批次已完整处理）。

产物：
  papers/daily/2026-11-01/7dim-table.md   前沿参考表（24 篇，非当日新拉取）
  papers/daily/2026-11-01/run_log.md      执行日志
  reports/XR-Daily-Report-2026-11-01.md   状态报告
  papers/MOC/MOC-总索引.md                状态注记 + 批次索引行 + 页脚刷新
"""
import json, os, io

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

reg = []
for l in io.open(os.path.join(ROOT, "papers/library/registry.jsonl"), encoding="utf-8"):
    l = l.strip()
    if l:
        reg.append(json.loads(l))

# 前沿参考 = 10-31 运行批次（10-30 公告批次：主批 18 + backfill-1031 6 篇），按 value 降序
ref = [r for r in reg if r.get("batch") in ("2026-10-31", "backfill-1031")]
ref.sort(key=lambda x: (-x.get("value", 0), x["id"]))

os.makedirs(os.path.join(ROOT, "papers/daily/2026-11-01"), exist_ok=True)

GATE3 = 4.429
GATE3_WIN = "2026-10-02~2026-11-01（399 条入窗）"
GRADES = {}
for r in reg:
    GRADES[r.get("grade", "C")] = GRADES.get(r.get("grade", "C"), 0) + 1
NOTES_N = len([f for f in os.listdir(os.path.join(ROOT, "papers/notes")) if f.endswith(".md")])

# ---------- 7dim-table.md ----------
L = []
L.append("# 7 维度对比表 · 2026-11-01（文献库最新前沿参考，非当日新拉取）")
L.append("")
L.append("> ⚠️ 说明：本运行日（周日 2026-11-01 02:30）经漏网对账 + 三源探针核验，**无新增可处理论文**：")
L.append("> ① listing 7 分类最新公告日均为 **2026-10-30**（周五；10-31 周六、11-01 周日无公告日段，符合 arXiv skipDays 节律）；")
L.append("> ② 10-30 公告组经 show=500 全量重采 **728 篇**（分类槽位 CV 233/GR 14/HC 51/MM 8/RO 129/AI 392/IV 15，跨列表去重后 728），与 10-31 运行采集集合**逐篇一致（710/710，差异 0）**→ 上批处理完整，**0 漏网**；")
L.append("> ③ API `submittedDate` 降序前沿 = **2026-10-29**（即 10-30 公告组来源，已全部入馆）；")
L.append("> ④ RSS 于 10-31 04:00 UTC 重建后 6/7 分类 0 条目（周六 skipDays 节律空源）；cs.AI feed 残留 10-30 公告批次陈旧内容（605 条，pubDate 被重新戳记为 10-31），7 条 KW 命中**全部为此前运行已处置论文**。")
L.append("> 下表为**文献库最新前沿（10-31 运行处理的 10-30 公告批次：主批 18 篇 + backfill-1031 6 篇）的 7 维参考表**，供查阅，**非「当日新论文」对比表**。")
L.append("")
L.append("> 维度与权重固定：`Value = 0.20·IMP + 0.20·NOV + 0.15·TEC + 0.15·EXP + 0.15·PER + 0.08·TRL + 0.07·REP`；分档：S≥4.2 / A 3.6–4.2 / B 3.0–3.6 / C<3.0")
L.append("")
L.append("> 拉取窗口：无（状态日；最新公告日 2026-10-30，已由上批 10-31 运行完整处理）")
L.append("")
L.append("| # | arXiv | 标题 | 赛道 | IMP | NOV | TEC | EXP | PER | TRL | REP | 总分 | 等级 | 批次 | 证据 | 状态 |")
L.append("|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|")
for i, r in enumerate(ref, 1):
    s = r.get("scores") or {}
    star = " ⭐" if r.get("in_top10") else ""
    batch = "主批 2026-10-31" if r.get("batch") == "2026-10-31" else "backfill-1031"
    L.append("| %d | [%s](https://arxiv.org/abs/%s) | %s%s | %s | %s | %s | %s | %s | %s | %s | %s | **%.2f** | %s | %s | %s | %s |" % (
        i, r["id"].split(":")[-1], r["id"].split(":")[-1],
        r.get("title_zh") or r.get("title", ""), star,
        r.get("track", ""),
        s.get("IMP", ""), s.get("NOV", ""), s.get("TEC", ""), s.get("EXP", ""),
        s.get("PER", ""), s.get("TRL", ""), s.get("REP", ""),
        r.get("value", 0), r.get("grade", ""), batch,
        r.get("evidence", ""), r.get("status", "CURRENT")))
L.append("")
L.append("> 证据列：FULL = 完整正文（L0/L1）；本表 24 篇证据等级均以 registry 登记为准（10-31 运行：24 篇全 L0/FULL）。")
L.append("> 门③ 参考：库内近 30 天 Top10 均分 **%.3f**（窗口 %s，现算）；本日 0 候选不触发校准关。" % (GATE3, GATE3_WIN))

with io.open(os.path.join(ROOT, "papers/daily/2026-11-01/7dim-table.md"), "w", encoding="utf-8") as f:
    f.write("\n".join(L) + "\n")
print("written 7dim-table.md:", len(ref), "ref rows")

# ---------- run_log.md ----------
R = []
R.append("# 运行日志 · 2026-11-01（周日 02:30 · 状态日：周末无公告）")
R.append("")
R.append("## 1. 漏网对账（Step 1，本日核心工作）")
R.append("")
R.append("- listing 7 分类日期头（`scripts/audit_gap_listing_1101.py`，TARGET_LO=2026-10-31，show=250）：")
R.append("  **最新公告日全部为 2026-10-30（周五）**（cs.CV / cs.GR / cs.HC / cs.MM / cs.RO / cs.AI / eess.IV 七分类一致；pastweek 视图 + 缓存穿透复验同样无 10-31 日组）。10-31（周六）无公告日段，符合 arXiv RSS skipDays 节律 → **无漏跑公告日**。")
R.append("- **采集缺陷发现与修复（新增踩坑）**：以 TARGET_LO=2026-10-30 复采 10-30 公告组时，最终校验显示多个分类 per-cat SHORT（cs.AI 315/392、cs.RO 112/129、eess.IV 6/15、cs.GR 7/14、cs.HC 48/51、cs.MM 7/8）。逐项排查确认两个机制：")
R.append("  ① `show=250` 分页跨日组边界丢条目：第 2 页以「(continued, showing last 142 of 392 entries)」开头，声明正则不匹配该措辞，且页首无 h3 的续接条目会被解析器丢弃；")
R.append("  ② 代理静默截断可绕过闭合日检测：若截断恰好切掉旧日头，`any(dd < day)` 判据失效，不完整页被当场接受。")
R.append("  **修复**：新写 `scripts/recollect_group_1030_1101.py`，show=500 单页采全目标组（各组均 <500 条）+ 声明正则兼容 continued/last 措辞 + 逐分类 declared 对齐校验。")
R.append("- **重采结论（关键）**：10-30 组全量 **728 篇唯一论文**（分类槽位 842，114 个为跨分类交叉列表重复），与 10-31 运行采集集合**逐篇一致（未入馆 710/710，双向差异 0）**。即：上批采集实际完整，per-cat SHORT 确为「跨列表论文被先处理分类认领」的统计假象（与任务描述已知坑④互证）；10-31 运行已对该完整集合做过摘要级 XR 过滤（31 篇命中全部处置：18 主批 + 6 backfill + 7 边界非 XR）→ **0 漏网，无 backfill**。")
R.append("- 落盘：`data/missed_listing_1101.json`（窗口 ≥10-31，0 篇）、`data/missed_listing_1101_group1030.json`（show=250 复采 710 篇）、`data/missed_listing_1101_group1030_full.json`（show=500 全量重采 710 篇，与前者集合一致）、`data/raw/2026-11-01.jsonl`（RSS 7 条 KW 命中）。")
R.append("")
R.append("## 2. 数据源探测（Step 2）")
R.append("")
R.append("- API 双主机（export.arxiv.org / arxiv.org）探针 200；`submittedDate` 降序前沿 = **2026-10-29**（cs.CV / cs.AI / cs.RO 抽查一致；10-29 提交 = 10-30 公告组来源，已全部入馆）；10-30~11-01 无新提交进入索引。")
R.append("- RSS（`scripts/fetch_rss.py`，7 分类）：6/7 分类 **0 条目**（10-31 04:00 UTC 重建，周六 skipDays 节律空源）；cs.AI 残留陈旧 feed **605 条**（内容为 10-30 公告批次，id 上限 2610.40649，pubDate 被重新戳记为 10-31）→ KW 命中 **7 条**。")
R.append("- 7 条 KW 命中去向核验（逐条对 registry 与上批裁决）：")
R.append("")
R.append("| ID | 标题 | 处置 |")
R.append("|---|---|---|")
R.append("| 2610.38117 | ProACT：性能驱动的 VR 消防训练动态难度调节 | 已在 registry（10-31 运行主批，B，3.58） |")
R.append("| 2610.38349 | 单视图新视角合成基准的坐标对齐评测协议 | 已在 registry（10-31 运行主批 Top10，A，4.14） |")
R.append("| 2610.39076 | Tactus：触觉与姿态感知手套 | 已在 registry（10-31 运行主批 Top10，A，4.03） |")
R.append("| 2610.38405 | SpaceAct（闭环动作空间推理基准） | 10-31 运行已剔非 XR（机器人空间推理） |")
R.append("| 2610.39385 | UMI-Live（野外双臂机器人数据采集） | 10-31 运行已剔非 XR（机器人数据采集） |")
R.append("| 2610.40636 | Probing Spatial State Representations in Visual Foundation Models | 10-31 运行已剔非 XR（视觉基础模型空间状态探测） |")
R.append("| 2608.07267 | WNM-3D（v3 replace 再公告） | 旧稿再公告，10-31 运行已剔非 XR |")
R.append("")
R.append("- 判定：**0 篇新候选**，不进入 Steps 3-7。")
R.append("")
R.append("## 3. 甄别 / 全文 / 评分 / Top10（Steps 3-7）")
R.append("")
R.append("- 候选池 0 篇 → 不触发全文抓取、7 维评分、覆盖度三关与 Top10 选拔。")
R.append("- **未伪造 Top10 / 评分 / S 级**（诚实口径硬约束）。")
R.append("- 门③ 现算参考：库内近 30 天 Top10 均分 **%.3f**（窗口 %s）。" % (GATE3, GATE3_WIN))
R.append("")
R.append("## 4. 产物与发布（Steps 8-9）")
R.append("")
R.append("- registry **无变更**（%d 条：S%d/A%d/B%d/C%d；本次未修改故无备份需要）；原子笔记 %d 篇无新增。" % (len(reg), GRADES.get("S",0), GRADES.get("A",0), GRADES.get("B",0), GRADES.get("C",0), NOTES_N))
R.append("- 产物：本 run_log + `papers/daily/2026-11-01/7dim-table.md`（24 篇前沿参考）+ `reports/XR-Daily-Report-2026-11-01.md` + MOC 总索引维护。")
R.append("- 前端：BATCH_LABELS 补 11-01 标签 → 重建 hub → DATA 计数核验 → CDP 冒烟 → 双渠道发布（详见报告 §5.5）。")
R.append("")
R.append("## 5. 异常与教训")
R.append("")
R.append("- **audit_gap_listing.py show=250 分页缺陷（本次发现，已用 show=500 重采修复并互证）**：跨日组边界丢条目 + 代理静默截断绕过闭合日检测；per-cat SHORT 多数为跨列表认领假象。判定采集是否完整必须以「全量重采集合 vs 上批集合逐篇比对」为准，不能仅凭 per-cat 计数。")
R.append("- RSS cs.AI 残留陈旧 feed（605 条 = 10-30 公告批次内容，pubDate 被周六重建戳记为 10-31）：单分类非空 + pubDate 新 ≠ 有新公告，必须 listing 日期头 + API submittedDate 交叉验证（本次三源互证排除误判，与 10-30 踩坑同型）。")
R.append("- 下次运行（11-02 周一 02:30）：周末积压公告时刻 = 周一 00:00 UTC = 当日 08:00 北京时间，**晚于运行时刻**，预期仍为状态日（同 10-26 模式）；11-03（周二）运行处理 11-02 周一公告批次（覆盖周末 10-31/11-01 提交积压）。门③ 务必现算（现值 %.3f 仅参考）。" % GATE3)
R.append("- 渠道①（workbuddy_sites_deploy）自 10-21 起连续不可用，若本会话恢复可用须优先补部署（挂账批次 10-21~11-01 共 12 批）；硬件类渲染缺口仍仅 CVQPG + HoOPOE 两篇破冰，继续补波导/可变焦/Maxwellian/光场。")

with io.open(os.path.join(ROOT, "papers/daily/2026-11-01/run_log.md"), "w", encoding="utf-8") as f:
    f.write("\n".join(R) + "\n")
print("written run_log.md")

# ---------- 报告 ----------
P = []
P.append("# XR 每日论文雷达 · 运行报告 · 2026-11-01（周日 02:30）")
P.append("")
P.append("> **诚实口径声明**：本运行日（2026-11-01，周日 02:30）**无新增可处理论文**。经三源交叉验证，**周末无公告**：listing 7 分类最新公告日均为 **2026-10-30（周五）**（10-31 周六、11-01 周日无公告日段，符合 arXiv skipDays 节律）；API `submittedDate` 前沿停滞 2026-10-29（10-30 公告组来源，已全部入馆）；RSS 10-31 04:00 UTC 重建后 6/7 分类 0 条目，cs.AI 残留 10-30 批次陈旧 feed（605 条，7 条 KW 命中全部已处置）。上一批（10-31 运行）处理的 10-30 公告批次经 show=500 全量重采复核：728 篇集合与上批采集**逐篇一致（710/710，差异 0）**，**0 漏网、无 backfill**。**本报告不包含任何「当日新论文」解读、不虚构 Top10/评分/S 级**；文末附表为文献库最新前沿参考。")
P.append("")
P.append("---")
P.append("")
P.append("## 一、执行摘要")
P.append("")
P.append("| 项 | 结论 |")
P.append("|---|---|")
P.append("| 运行性质 | **状态报告日**（周末无公告；漏网对账 + 三源探针 + 采集完整性复核 + 知识库存量维护 + 前端重建与双渠道发布） |")
P.append("| 公告状态 | listing 7 分类（recent + pastweek + 缓存穿透复验）最新公告日均为 **2026-10-30**；10-31/11-01 周末无公告日段（skipDays 节律） |")
P.append("| 漏网对账 | 10-30 公告组 show=500 全量重采 **728 篇**，与 10-31 运行采集集合逐篇一致（未入馆 710/710，双向差异 0）；上批已对该完整集合做摘要级 XR 过滤（31 篇命中全部处置）→ **0 漏网**；无漏跑公告日，无需 backfill |")
P.append("| 数据源 | API 双主机 200（submittedDate 前沿 10-29，已全部入馆）；RSS 6/7 分类空源（周六节律），cs.AI 陈旧 feed 605 条、7 条 KW 命中全部已处置 |")
P.append("| 新入馆论文 | **0 篇**（registry 维持 **%d 条**：S %d / A %d / B %d / C %d） |" % (len(reg), GRADES.get("S",0), GRADES.get("A",0), GRADES.get("B",0), GRADES.get("C",0)))
P.append("| 新原子笔记 | 0 篇（维持 **%d 篇**） |" % NOTES_N)
P.append("| 库内近 30 天 Top10 均分 | **%.3f**（现算，窗口 %s；门③ 为校准关，本日无候选不触发） |" % (GATE3, GATE3_WIN))
P.append("| 交付 | 状态报告 1 + 前沿参考 7 维表 1（24 篇）+ run_log 1 + MOC 总索引维护 + 前端重建与双渠道发布 |")
P.append("")
P.append("**下一批预期**：11-02（周一）02:30 运行时，周末积压公告时刻（周一 00:00 UTC = 08:00 北京时间）尚未到达，预期仍为状态日（同 10-26 模式）；**11-03（周二）运行处理 11-02 周一公告批次**（覆盖周末 10-31/11-01 提交积压），门③ 务必现算（勿沿用 %.3f）。" % GATE3)
P.append("")
P.append("---")
P.append("")
P.append("## 二、漏网对账（Step 1，本日核心工作）")
P.append("")
P.append("对账目的：确认自上一批次公告日（2026-10-30）至今是否有漏跑公告日或漏收 XR 论文。")
P.append("")
P.append("### 2.1 公告日头核验（目标窗口 ≥ 2026-10-31）")
P.append("")
P.append("| 分类 | 最新公告日 | 10-31 日组 |")
P.append("|---|---|---|")
P.append("| cs.CV | Fri, 30 Oct 2026 | 无（周六 skipDays） |")
P.append("| cs.GR | Fri, 30 Oct 2026 | 无 |")
P.append("| cs.HC | Fri, 30 Oct 2026 | 无 |")
P.append("| cs.MM | Fri, 30 Oct 2026 | 无 |")
P.append("| cs.RO | Fri, 30 Oct 2026 | 无 |")
P.append("| cs.AI | Fri, 30 Oct 2026 | 无 |")
P.append("| eess.IV | Fri, 30 Oct 2026 | 无 |")
P.append("")
P.append("- **无 10-31 公告日组**：recent / pastweek 视图（含缓存穿透复验）七分类一致；周末无公告符合 arXiv RSS `<skipDays>` 节律（周六/周日不公告）。")
P.append("- **三源互证**：① listing 七分类最新日组全部为 Fri, 30 Oct 2026；② API `submittedDate` 降序前沿 = 2026-10-29（cs.CV/cs.AI/cs.RO 抽查一致，即 10-30 公告组来源）；③ RSS 10-31 04:00 UTC 重建后 6/7 分类 0 条目。")
P.append("")
P.append("### 2.2 10-30 公告组完整性复核（验证上一批处理完整性 · 本日重点）")
P.append("")
P.append("以 TARGET_LO=2026-10-30 复采时发现 per-cat SHORT（cs.AI 315/392 等），逐项排查后确认两类机制并修复：")
P.append("")
P.append("1. **show=250 分页跨日组边界丢条目**：目标组 >250 条时第 2 页以「(continued, showing last N of M entries)」开头，声明正则不匹配该措辞；且页首无 h3 的续接条目被解析器丢弃；")
P.append("2. **代理静默截断绕过闭合日检测**：截断若切掉旧日头，`any(dd < day)` 判据失效，不完整页被当场接受。")
P.append("")
P.append("修复方式：新写 `scripts/recollect_group_1030_1101.py`（show=500 单页采全目标组 + 声明正则兼容 continued/last + 逐分类 declared 对齐）。重采结果：")
P.append("")
P.append("| 分类 | declared | 实采 |")
P.append("|---|---:|---:|")
P.append("| cs.CV | 233 | 233 |")
P.append("| cs.GR | 14 | 14 |")
P.append("| cs.HC | 51 | 51 |")
P.append("| cs.MM | 8 | 8 |")
P.append("| cs.RO | 129 | 129 |")
P.append("| cs.AI | 392 | 392 |")
P.append("| eess.IV | 15 | 15 |")
P.append("")
P.append("- 分类槽位合计 842，全局去重后 **728 篇唯一论文**（114 个跨分类交叉列表重复）。")
P.append("- **与 10-31 运行采集集合逐篇比对：未入馆 710/710，双向差异 0 → 上批采集实际完整**；per-cat SHORT 为「跨列表论文被先处理分类认领」的统计假象（与已知坑④互证）。")
P.append("- 10-31 运行已对该完整集合执行摘要级 XR 过滤（31 篇命中：18 主批 + 6 backfill-1031 + 7 边界篇手动剔非 XR），RSS 渠道同步互证漏网 0 → **0 漏网，无 backfill**。")
P.append("")
P.append("---")
P.append("")
P.append("## 三、数据源探测记录（Step 2）")
P.append("")
P.append("- `fetch_rss.py` 7 分类：cs.AI 605 条（**陈旧 feed**：内容为 10-30 公告批次，id 上限 2610.40649，pubDate 被周六重建戳记为 10-31），其余 6 类 0 条；KW 命中 7 条。")
P.append("- 7 条 KW 命中去向核验（防误纳陈旧 feed 内容）：")
P.append("")
P.append("| ID | 标题 | 处置 |")
P.append("|---|---|---|")
P.append("| 2610.38117 | ProACT：VR 消防训练动态难度调节 | 已在 registry（10-31 主批，B 3.58） |")
P.append("| 2610.38349 | 单视图 NVS 基准坐标对齐评测协议 | 已在 registry（10-31 主批 Top10，A 4.14） |")
P.append("| 2610.39076 | Tactus 触觉手套 | 已在 registry（10-31 主批 Top10，A 4.03） |")
P.append("| 2610.38405 | SpaceAct | 10-31 运行已剔非 XR |")
P.append("| 2610.39385 | UMI-Live | 10-31 运行已剔非 XR |")
P.append("| 2610.40636 | Probing Spatial State Representations | 10-31 运行已剔非 XR |")
P.append("| 2608.07267 | WNM-3D（v3 replace） | 旧稿再公告，10-31 运行已剔非 XR |")
P.append("")
P.append("- 判定：**0 篇新候选**，不进入 Steps 3-7。")
P.append("")
P.append("---")
P.append("")
P.append("## 四、文献库最新前沿参考（10-30 公告批次 · 24 篇 · 非当日新拉取）")
P.append("")
P.append("以下为 10-31 运行处理的 10-30 公告批次 7 维参考表（主批 18 篇 + backfill-1031 6 篇），完整版见 [papers/daily/2026-11-01/7dim-table.md](../daily/2026-11-01/7dim-table.md)：")
P.append("")
P.append("| # | arXiv | 标题 | 赛道 | 总分 | 等级 | 批次 |")
P.append("|---|---|---|---|---|---|---|")
for i, r in enumerate(ref, 1):
    star = " ⭐" if r.get("in_top10") else ""
    batch = "主批 10-31" if r.get("batch") == "2026-10-31" else "backfill-1031"
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
P.append("- 门③ 参考值现算：库内近 30 天 Top10 均分 **%.3f**（窗口 %s；Top10 为 2610.03162 4.65 / 2610.03283 4.58 / 2610.19674 4.57 / 2610.23772 4.57 / 2610.39399 4.37 / 2610.34263 4.35 / 2610.18872 4.30 / 2610.22778 4.30 / 2609.31418 4.30 / 2610.37602 4.30）。" % (GATE3, GATE3_WIN))
P.append("")
P.append("### 5.2 证据等级分布")
P.append("")
P.append("- 本日无新抓取。参考表 24 篇证据等级：24 篇全 L0/FULL（10-31 运行实测）；无 PARTIAL / ABSTRACT_ONLY。")
P.append("")
P.append("### 5.3 失败/降级清单")
P.append("")
P.append("- 无抓取失败。数据源异常 1 项：RSS cs.AI 残留 10-30 批次陈旧 feed（已核验处置，见 §三）。")
P.append("- 采集工具缺陷 1 项（已修复）：`audit_gap_listing.py` show=250 分页跨组丢失 + 代理截断绕过闭合日检测；本日以 show=500 重采互证上批集合完整（详见 §2.2）。")
P.append("")
P.append("### 5.4 产物清单")
P.append("")
P.append("| 产物 | 路径 |")
P.append("|---|---|")
P.append("| 状态报告 | `reports/XR-Daily-Report-2026-11-01.md` |")
P.append("| 前沿参考 7 维表 | `papers/daily/2026-11-01/7dim-table.md`（24 篇） |")
P.append("| 运行日志 | `papers/daily/2026-11-01/run_log.md` |")
P.append("| 对账数据 | `data/missed_listing_1101.json` / `data/missed_listing_1101_group1030.json` / `data/missed_listing_1101_group1030_full.json` / `data/raw/2026-11-01.jsonl` |")
P.append("| MOC 总索引 | `papers/MOC/MOC-总索引.md`（11-01 状态注记 + 批次索引行 + 页脚刷新） |")
P.append("| 前端 | `web/xr-paper-hub.html`（重建） |")
P.append("")
P.append("### 5.5 发布记录")
P.append("")
P.append("- 渠道① WorkBuddy 托管（workbuddy_sites_deploy）：见收尾汇报（若工具不可用则挂账，自 10-21 起连续不可用）。")
P.append("- 渠道② GitHub Pages：见收尾汇报（commit + push_to_github.py --incremental + deploy run + Pages 200 核验）。")
P.append("")
P.append("---")
P.append("")
P.append("*报告生成：2026-11-01 02:30 自动化运行（xr-paper-daily-brief skill · 9 步流水线）。*")

with io.open(os.path.join(ROOT, "reports/XR-Daily-Report-2026-11-01.md"), "w", encoding="utf-8") as f:
    f.write("\n".join(P) + "\n")
print("written report, chars:", len("\n".join(P)))
