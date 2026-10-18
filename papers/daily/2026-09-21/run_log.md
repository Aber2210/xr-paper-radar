# 执行日志 · 2026-09-21

## 0. 与上一期的关键差异（本期最重要事实）

**arXiv 上游最新提交日仍为 2026-09-17，今日无新提交日。**

核验过程：对 `cat:cs.CV` / `cat:cs.GR` / `cat:cs.RO` 三个分类分别以 `sortBy=submittedDate&sortOrder=descending` 取前 5 条，返回的最新 `published` 全部为 `2026-09-17`。三个分类一致，排除单分类索引延迟的可能。

因此本期不存在"当日新提交"概念。按 skill §2.2「周末/假期回溯」的同一精神，改为**补漏 + 深挖模式**：

- 上次运行使用 `max_results=300`（3 页 × 100），同一时间窗内仍有论文未被覆盖；
- 本次改为 5 天窗口 × 400 条（4 页 × 100），拉取 65 篇；
- 剔除文献库已收录的 38 篇后，得到 **27 篇新增候选**。

**实际命中日期区间：2026-09-15 ～ 2026-09-17。**

---

## 1. Step 1 拉取

| 项 | 结果 |
|---|---|
| 数据源 | arXiv API `export.arxiv.org/api/query` |
| 分类 | cs.GR / cs.HC / cs.CV / cs.MM / cs.RO / cs.AI / eess.IV |
| 关键词 | 24 个（virtual reality、Gaussian splatting、SLAM、haptic、near-eye、light field、passthrough、world model 等） |
| 排序 | `sortBy=submittedDate&sortOrder=descending` |
| 页数 | 4 页 × 100（max=400） |
| 窗口 | 5 天，本地按 `published` 精确过滤 |
| 返回 | **65 条**（09-15: 5 / 09-16: 29 / 09-17: 31） |
| 去重后新增 | **27 条**（09-15: 5 / 09-16: 22） |
| 限流 / 退避 | **0 次触发**（每请求间隔 3 s，串行） |
| 失败 | 0 |
| 产出 | `data/raw/2026-09-21.jsonl`、`data/raw/2026-09-21_new.jsonl` |

## 2. Step 2 去重与入馆

- 以 `base_id` 对 `papers/library/registry.jsonl`（38 条）做集合差，得 27 条新增。
- 新增 27 条已全部追加进 `registry.jsonl`（累计 **65 条**）。

## 3. Step 6 全文抓取

**执行顺序说明**：skill 定义顺序为「先评分 → 再抓 Top10」。本期做了**一处有意的顺序调整**：先按摘要筛出 XR 相关度较高的 12 篇并抓取全文，再依据**正文证据**定稿评分。原因是本期为补漏批次、候选质量参差，仅凭摘要无法可靠区分 TEC/EXP/PER（事后证明这一判断正确——GazeDiT 的 EXP 由 4 上修至 5，Wind on Trees 的 PER 由 3 下修至 2）。

| 项 | 结果 |
|---|---|
| 抓取对象 | 12 篇（Top10 + 2 篇候补） |
| 降级链路 | L0 arXiv HTML → L1 ar5iv → L2 PDF → L3 OpenReview → L4 S2 → L5 摘要 |
| **实际使用层级** | **全部 L0 一次成功** |
| 证据等级 | **12/12 全部 FULL** |
| 字符数区间 | 34,555（MoQSplat）～ 117,557（CapMem） |
| 限流 / 403 / 429 | **0 次**，未触发任何退避 |
| 失败 / 降级 | **0 篇** |
| 耗时 | 约 40 s（串行 + 3 s 间隔） |
| 产出 | `data/fulltext/*.txt` + `_manifest.json` |

**与首日实测一致**：arXiv HTML 源（`arxiv.org/html/<id>v<n>`）对 2026 年新论文覆盖率极高，L1–L5 实际用不上。

**避坑**：`fetch_fulltext.py` 每次运行会**覆盖** `_manifest.json`（skill §8.5 缺陷 #3）。本期一次性传入 12 个 id，规避了该问题。

## 4. 已知数据缺陷登记

| # | 对象 | 问题 | 处理 |
|---|---|---|---|
| 1 | `2609.18737`（Geometry beneath the Waves） | arXiv API 返回的摘要被截断为 2 句（约 300 字符），无方法/实验信息 | 7 维表中以 ※ 标注、可信度低；评 2.77（C），未入选；未抓取全文 |
| 2 | 本期无新提交日 | 见 §0 | 报告中显式写明，不伪装成"每日新论文" |

## 5. Step 5 覆盖率校验

- 第①关（Jaccard > 0.62）：全池最高 sim **0.144**，命中 0 篇 → **无同质重复**。
- 第②关（赛道覆盖）：覆盖 **7 个**赛道（要求 ≥5），最大占比 20% → **通过，不触发回补**。上期登记的 3 个缺口（神经渲染空白 / 渲染与显示无 A 级 / 化身与人体天花板）**全部补齐**。
- 第③关（价值天花板）：本期最高 4.28 vs 库内 Top10 均分 4.265，差值 **+0.015** → **险过**。本期 Top10 均分 3.924 < 库内 4.265，已在报告中如实披露"本期非重磅日"。

详见 `scored.md`。

## 6. Step 7 产物清单

| 文件 | 说明 |
|---|---|
| `papers/daily/2026-09-21/7dim-table.md` | 全量 27 篇 7 维对比表 |
| `papers/daily/2026-09-21/scored.md` | 评分明细 + 三关校验 + 落后判定 |
| `papers/daily/2026-09-21/run_log.md` | 本文件 |
| `papers/notes/2609.18473__CADSplat*.md` 等 10 份 | 原子化笔记 |
| `papers/MOC/MOC-2026-09-21.md` | 当日 MOC |
| `papers/MOC/MOC-总索引.md` | 全局索引（已更新） |
| `reports/XR-Daily-Report-2026-09-21.md` | 最终解读报告 |
| `papers/library/registry.jsonl` | 追加 27 条，累计 65 条 |

## 7. 脚本变更

- 新增 `scripts/dedup_check.py`：覆盖度校验第①关自动化（token Jaccard + 停用词过滤 + 三档区间输出）。此前该关卡为手工估算，本期起可复算。
