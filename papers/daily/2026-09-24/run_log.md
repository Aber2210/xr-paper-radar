# 执行日志 · 2026-09-24（自动化触发 03:00 GMT+8）

## 0. 触发与总体
- 自动化 `728fcb37` 第四次规律运行（09-20/09-21/09-23 + 本次）；本次为 09-24 真实运行。
- 目标：拉取当日最新 AR/VR/MR/XR 论文 → 7 维对比表 → 价值评分 → 覆盖度三关 → 全文抓取 → 原子笔记 + MOC → 解读报告。

## 1. Step1 拉取（数据源变更：关键）
- **`export.arxiv.org/api/query` 当日被沙箱代理整体 406 拦截**：HTTP 406 Not Acceptable。
  - 实测：5 次退避重试（含 `http`/`https`、`Accept` 变体、`minimal` 头）全部 406；`arxiv.org/api/query` 亦 406，`http arxiv.org` 超时。
  - 对照：沙箱代理对 `google`/`semanticscholar` 超时/429，但对 `arxiv.org` 主页/列表/RSS **可达**；`WebFetch`（服务端出口）可正常取 arXiv API。
  - 判定：属代理层不稳定（同 §6.5 历史 404 一类），单请求退避无效。
- **兜底源切换**：改用 **`rss.arxiv.org` RSS**（沙箱代理可达），按 7 分类拉取"最新公告"批次。
  - 实测：cs.CV 382 / cs.GR 12 / cs.RO 151 / cs.HC 42 / cs.MM 8 / cs.AI 366 / eess.IV 20 = **927 条**（公告日 2026-09-23）；关键词命中 **51 条**。
  - 新增脚本 `scripts/fetch_rss.py` 产出与 `fetch_arxiv.py` 同 schema 的 `data/raw/2026-09-24.jsonl`（已修复 guid→link 的 arXiv-ID 解析 bug）。

## 2. Step2 去重 & 入库过滤
- 与 `registry.jsonl`（112 条）比对：51 命中中 **18 已入库**，**33 新候选**。
- **诚实过滤（§8.6.1）**：33 新候选中混入 RSS "recent" 的旧稿 replace/cross——**非 2609 旧 ID（2603/2605/2607/2608/2510/2512 等）共 12 篇**，它们不是"当日新提交"，**排除出今日 corpus**（详见 §5）。
- **今日 corpus = 22 篇 2609.* 新周期提交**：**12 篇 XR 相关 + 9 篇非 XR 留存**；其中 2 篇（2609.24531 热成像 4DGS、2609.25466 OpenXR 手势）标 XR 相关但为 B 级。

## 3. Step6 全文抓取
- 对 12 篇 XR 候选跑 `fetch_fulltext.py`（L0 arXiv HTML 首选）：
  - 11 篇 **L0 / FULL**（含 20 万字符的大文 4DGS-JEPA）；1 篇 2609.25466 **L1 / FULL**（ar5iv，4267 字符）。
  - 偶发 HTTP 406 经脚本内 5 次退避重试后由 v1/无版本 URL 命中——属正常降级路径，非缺陷。
  - **无限流封禁、无 L5 摘要降级、无伪造**。

## 4. Step4 评分 + Step5 覆盖度三关（见 `scored.md`）
- 门① 同质去重：新集 vs 库内近 90 天 token Jaccard **max=0.286**（2609.25604 vs 2609.23380），<0.62 → **通过（无同质）**。
- 门② 赛道覆盖：Top10 覆盖 **7 个赛道** ≥5 → **通过**。
- 门③ 价值天花板：当日最高 **4.08** < 库内近 30 天 Top10 均分 **4.298** → **非重磅日，无 S 级论文**（不得拔高评分）。
- 重筛闭环：三关均通过，未触发剔除/回补。

## 5. 遗留事项（重要）
- **RSS 混入旧稿**：12 篇非 2609 旧 ID（2603/2605/2607/2608/2510/2512 等）为 XR 相关的 3DGS/SLAM 旧稿 replace/cross，**未计入今日新论文**，亦未入库（避免误标为 09-23 新稿）。
  - 建议：沙箱代理恢复、改用 API `submittedDate` 窗口后，单独做 **backfill 批次**纳入这些高价值旧稿。
- **口径说明**：今日论文公告日 2026-09-23，今日 09-24 拉取为最新可用批次（非"当日提交"，但为最新公告）。已在报告与 7 维表显式声明。

## 6. Step7/8 产物
- `reports/XR-Daily-Report-2026-09-24.md`（10 章逐篇精读 + 7 维参考表 + 覆盖校验 + 附录）
- `papers/notes/` 原子笔记 **12 篇**（10 Top10 + 2 B 级参考）
- `papers/MOC/MOC-2026-09-24.md` + `MOC-总索引.md` 更新
- `papers/daily/2026-09-24/`：7dim-table.md / scored.md / run_log.md / _scored_snapshot.json
- `papers/library/registry.jsonl`：**112 → 133**（新增 21）
- 证据等级分布：12 篇 XR 全 FULL（11 L0 + 1 L1）。

## 7. 下次运行必读
1. **优先恢复 API 源**：先探针 `export.arxiv.org/api/query`；若仍 406，继续用 RSS 兜底，但务必执行 §5 的**旧稿 backfill**（RSS "recent" 会把旧稿当新公告混出）。
2. **RSS 源局限**：RSS "recent" ≠ "当日新提交"，含大量 replace/cross 旧稿；用 2609 前缀 + announce type 过滤"真正新提交"，旧稿单列 backfill。
3. **盘满风险**：本日 C: 盘 22.7 GB 充裕（09-23 曾 0 字节）；仍建议跑前查 `shutil.disk_usage`。
4. **脚本新增**：`fetch_rss.py`（RSS 兜底源）；`fetch_arxiv.py`/`fetch_fulltext.py` 维持可用。
