# 需求梳理：AR/VR/MR/XR 每日论文雷达

> 本文档系统梳理「每日拉取 XR 领域最新 arXiv 论文 → 7 维度对比 → 价值评分排序 → 覆盖率校验（不达标则重筛）→ 全文抓取 → 逐篇深度解读 → 原子化笔记 + MOC 索引知识库」这一自动化任务的全部需求、设计决策与**执行手册**。
> 本文档是「需求梳理 + 操作手册」合一版；配套的**可执行规范**见 Skill：`xr-paper-daily-brief`（用户级）。配套脚本：`scripts/fetch_arxiv.py` / `scripts/fetch_rss.py` / `scripts/fetch_fulltext.py`（均为标准库实现、无第三方依赖）。

---

## 1. 任务目标与边界

| 项 | 定义 |
|---|---|
| **目标** | 持续、可复现、跨日可比地跟踪 AR/VR/MR/XR（含 3D 重建、SLAM、神经渲染、具身交互、空间计算、近眼显示、触觉反馈）领域最新论文，输出中文解读报告与可沉淀的知识库 |
| **触发** | 每日定时自动化（无人值守，不可交互提问） |
| **输入** | arXiv API（主源）+ arXiv RSS（兜底源，2026-09-24 起实测必需）+ 全文 HTML/PDF/OpenReview/Semantic Scholar 降级源 |
| **输出** | ① 当日全量 7 维对比表 ② Top10 评分表 ③ 覆盖率校验记录 ④ 原子化笔记（每篇一文件）⑤ 当日 MOC + 总索引 MOC ⑥ 最终解读报告 |
| **硬约束** | 不得伪造内容、不得凑数、必须串行抓取、必须更新文献库、落后标记须有对比证据、笔记与 MOC 严格分离 |

**核心难点**（用户重点强调）：① 全文抓取在限流/拦截/缺失下的鲁棒性；②「入选名单在价值上已覆盖当前文献库、否则重筛」这一闭环的可执行化。

---

## 2. 核心流程（8 步流水线）

```
Step1 拉取 ──► Step2 去重&入馆 ──► Step3 7维对比表 ──► Step4 价值评分
                                                         │
                              ┌──────────────────────────┘
                              ▼
                    Step5 覆盖率校验（三关）
                       │ 任一关不达标？
                       ├─ 否 ─► Step6 全文抓取
                       └─ 是 ─► 【重筛循环】回 B 级池补冷门赛道 / 放大时间窗 / 回补候选 ─► 回到 Step4
                                              │
                                              ▼
                                   Step6 全文抓取（L0→L5 降级）
                                              │
                                              ▼
                               Step7 原子化笔记 + MOC 索引（知识库组合）
                                              │
                                              ▼
                                      Step8 最终解读报告
```

每一步都必须产出独立文件，且**任何失败必须写入 `run_log.md`，不得静默跳过**。

### 2.1 数据源（2026-09-24 起已更新）

| 优先级 | 源 | 用途 | 状态与备注 |
|---|---|---|---|
| P0 | arXiv API (`arxiv.org/api/query`) | 主源，元数据 + 摘要 | 2026-09 起被沙箱代理**间歇 406** 拦截，不可靠；仅作探针优先 |
| P1 | **arXiv RSS (`rss.arxiv.org`)** | **兜底元数据源** | 2026-09-24 起实测稳定 200；**当前最可靠的拉取通道**，务必按 `2609.*` 前缀 + 排除旧稿过滤「真正新提交」 |
| P2 | arXiv HTML (`arxiv.org/html/<id>`) | 全文首选 | 见 §6 |
| P3 | ar5iv / PDF / OpenReview / Semantic Scholar | 全文降级 | 见 §6 |

> ⚠️ **RSS 不等于「当日新提交」**：RSS "recent" 会把大量旧稿 replace/cross（如 `2601/2603/2604/2605/2606/2510/2512` 等非 2609 旧 ID）当新公告混出。**必须**用「`2609.*` 前缀 + 排除已在库中的 v2 再公告」过滤，旧稿单列 backfill，绝不混入「当日新论文」表。

---

## 3. 七大需求维度（固定，保证跨日可比）

维度一旦定义即**永久不变**，否则不同日期评分不可比较。

| # | 维度 | 缩写 | 1–5 判据要点 |
|---|---|---|---|
| D1 | 问题重要性 | **IMP** | 5=领域公认卡脖子/高频痛点；解决真实瓶颈 |
| D2 | 方法创新性 | **NOV** | 5=新范式/新架构；相对 SOTA 是突破还是增量 |
| D3 | 技术完整度 | **TEC** | 5=理论+系统+消融齐全；有证明/误差分析 |
| D4 | 实验强度 | **EXP** | 5=多数据集+真机+大样本用户实验 |
| D5 | 性能增益 | **PER** | 5=相对 SOTA 提升 >30%；有量化指标 |
| D6 | 落地成熟度 | **TRL** | 5=已产品化/开源可商用；TRL 1-9 映射 |
| D7 | 可复现与影响力 | **REP** | 5=有代码+数据+高引用/顶会 |

---

## 4. 价值评分模型

```
Value = 0.20·IMP + 0.20·NOV + 0.15·TEC + 0.15·EXP + 0.15·PER + 0.08·TRL + 0.07·REP
```

**权重理由**：问题重要性 + 方法创新性决定长期价值（各 20%）；技术完整度/实验/性能决定可信度（各 15%）；落地成熟度与可复现性为加分项（8%/7%），避免「工程包装型」论文挤占理论突破型。

**分档**：`S ≥ 4.2` · `A 3.6–4.2` · `B 3.0–3.6` · `C < 3.0`

**不凑数原则**：当日最高分 < 3.6 时，Top10 允许少于 10 篇并明确说明；价值天花板校验险过（与库内 Top10 均分差 < 0.05）时，**不得宣称出现重磅工作**。

---

## 5. 覆盖率校验与「重筛闭环」（关键需求）

> 用户原话：「需确认入选的引文在价值上已覆盖当前文献库，否则重新筛选。」

这是本任务与普通「论文汇总」的本质区别：**入选名单不是简单按分排序取前 10，而是要在价值维度上覆盖文献库的多样性，避免重复推荐同质工作、漏掉新方向。**

### 5.1 三关校验

| 关 | 名称 | 方法 | 不达标判定 |
|---|---|---|---|
| ① | 同质去重 | 当日 Top-N 与 `registry.jsonl` 近 90 天条目算标题+摘要 token Jaccard；`sim > 0.62` 判同质 | 出现同质重复 |
| ② | 方向覆盖度 | 归入 12 标准赛道；当日名单应覆盖 ≥5 个赛道 | 集中在 ≤3 赛道（筛选偏食） |
| ③ | 价值天花板 | 当日最高分 vs 库内近 30 天 Top10 均分 | 当日最高 < 库内均分（确无重磅） |

### 5.2 重筛触发与动作（闭环核心）

| 触发条件 | 动作 |
|---|---|
| ① 命中同质（sim>0.62） | 降权/剔除该篇，从 B 级池补入高价值候选 |
| ② 赛道覆盖 <5 | 从 B 级池回补冷门赛道的最高分论文（保护 XR 核心赛道：渲染与显示/交互与输入/触觉与多模态/空间计算与UI/感知与认知/化身与人体） |
| ③ 天花板不达标 | 在报告中明确标注「当日无 S 级/非重磅日」，**不为了凑数拔高评分** |
| 文献库为空（首跑） | ①、③ 关不适用，显式记录「建立基线」；② 关照常执行（正是它触发了首跑的回补） |

**关键认知**：重筛不是「重新打分」，而是「在已评分集合中按覆盖度重新选调」，且必要时（仍不足）才回 B 级池或放大时间窗重新抓取。所有重筛动作写入 `run_log.md` 与报告 §5。

### 5.3 12 标准赛道

`渲染与显示` `重建与SLAM` `神经渲染` `交互与输入` `触觉与多模态` `化身与人体` `空间计算与UI` `感知与认知` `系统与平台` `内容生成` `世界模型与仿真` `评估与数据集`

---

## 6. 全文抓取执行手册（用户重点 · 本文档核心）

> 这是用户最强调的环节。原 `xr-paper-daily-brief` 的 §2.3/§6.4 引用了 `fetch_arxiv.py`/`fetch_fulltext.py`，但**此前从未落地实现**——抓取实际靠每次手写内联 Python 完成。本手册基于已落地的 `scripts/fetch_fulltext.py`（标准库、无第三方依赖）写成，可直接照做。

### 6.0 总体原则

1. **串行优先**：`for` 循环 + `time.sleep(3)`，禁止并发线程池——并发会触发 arXiv 封 IP（连续 403/429）。
2. **单批 ≤1 req/s**：每请求间隔 ≥3 秒；分页/抓全文都遵守。
3. **降级不伪造**：L0→L5 逐级尝试，全部失败才 L5 摘要降级，且**必须显式标注证据等级**。
4. **核对数量不轻信状态码**：「HTTP 200」不代表成功解析（历史上 `fetch_arxiv.py` 曾因命名空间 bug 静默 0 条）；跑完必核 `WROTE=N` 与 manifest 中 Top 候选的 `level/evidence`。
5. **环境盘满风险**：跑前查 `shutil.disk_usage`；C: 盘可能 0 字节导致写入失败（见 §6.8）。

### 6.1 拉取前：连通性探针（P0 + P1 都必须做）

```python
# 最简探针：若连 all:electron 都失败，说明代理层整体异常（非脚本缺陷）
import urllib.request
probe = "https://arxiv.org/api/query?search_query=all:electron&max_results=1"
rss_probe  = "https://rss.arxiv.org/rss/cs.CV"   # RSS 通道探针
```

- P0 API 探针 200 → 用 API；若 406/超时 → **直接转 P1 RSS**，不纠缠。
- P1 RSS 探针 200 → 用 RSS。
- **连续 3 次 404/406/超时** → 停止硬扛，记录 `run_log.md` 后**推迟到下一调度周期或数分钟后重跑**（断点续拉保证不重复计费）。

### 6.2 降级链路决策树（任一级成功即停）

```
开始抓取 base_id
   │
   ├─► L0 arXiv HTML  https://arxiv.org/html/<id>v2 → v1 → (无版本)
   │       │ 成功(文本≥1500字符) → 清洗 → 判定证据等级 → ✅ 结束
   │       └─ 404/空 → 降级
   │
   ├─► L1 ar5iv        https://ar5iv.labs.arxiv.org/abs/<id>
   │       │ 成功 → ✅ 结束
   │       └─ 失败 → 降级
   │
   ├─► L2 arXiv PDF    https://arxiv.org/pdf/<id>v2 → v1 → (无版本)
   │       │ 仅当 pdfminer.six 可用时启用；扫描件(文本<500)标记 LOW_TEXT 不 OCR
   │       └─ 不可用/失败 → 降级
   │
   ├─► L3 OpenReview   https://api.openreview.net/notes?forum=<id>
   │       └─ 失败 → 降级
   │
   ├─► L4 SemanticScholar  api.semanticscholar.org/.../arXiv:<id>?fields=openAccessPdf,abstract,tldr
   │       │ 无 key 时约 1 req/s；429 则跳过，不阻塞主流程
   │       └─ 失败 → 降级
   │
   └─► L5 摘要降级（绝不伪造）
           │ 有 --abstracts 旁注 jsonl → "[摘要降级] <abstract>"
           └─ 无摘要 → "[无可用全文与摘要]" → 证据等级 ABSTRACT_ONLY
```

### 6.3 分步执行手册

**Step A — 拉取元数据（P0 API 优先，P1 RSS 兜底）**

```bash
# 标准模式（API 可用时）：回溯 N 天、本地按 published 过滤、分页、断点续拉
python scripts/fetch_arxiv.py --days 3 --max 300 --out data/raw/YYYY-MM-DD.jsonl
# 补漏模式：指定 --since 覆盖 --days，放大 max 把分页截断的漏网条目捞回
python scripts/fetch_arxiv.py --since 2026-09-15 --max 600 --out data/raw/YYYY-MM-DD.jsonl

# RSS 兜底（API 406 时，当前最可靠）：7 分类批次 → 关键词命中 → 2609 过滤
python scripts/fetch_rss.py --out data/raw/YYYY-MM-DD.jsonl
```

**Step B — 去重 & 入馆**：与 `library/registry.jsonl` 做集合差，剔除已在库条目、剔除非 `2609.*` 旧稿 replace/cross、剔除库内已有的 v2 再公告。

**Step C — 先抓全文，再定稿评分（补漏/质量参差批次必做）**：仅凭摘要无法可靠区分 TEC/EXP/PER。先按摘要筛 XR 相关度较高的 N+2 篇（N=10）抓全文，再依**正文证据**定稿评分，最后排序取 Top N。实测摘要推断修正率约 3/12（如 GazeDiT EXP 由 4 修正为 5）。

```bash
# 全文抓取：传入 base_id 列表；--abstracts 用于 L5 摘要降级兜底
python scripts/fetch_fulltext.py \
    --ids 2609.xxxxx,2609.yyyyy,2609.zzzzz \
    --out data/fulltext/ \
    --abstracts data/raw/YYYY-MM-DD.jsonl
```

**Step D — 核验产物**：
- `fetch_arxiv.py` 末尾打印 `WROTE=N` → **必须 N>0**，否则说明解析失败（旧版会静默 0 条）。
- `data/fulltext/_manifest.json` 中 Top 候选的 `level` 应为 `L0`/`L1`、`evidence` 应为 `FULL`/`PARTIAL`（旧版缺失异常导入会静默全 L5，已修复但仍需核）。
- 抽查 1–2 篇 `.txt` 文件头 `# LEVEL:`/`# EVIDENCE:`/`# CHARS:` 是否与正文一致。

### 6.4 障碍 → 动作对照表（精确版）

| 障碍 | 精确症状 | 定位方法 | 解决动作 | 何时放弃/升级 |
|---|---|---|---|---|
| **arXiv 429/503 限流** | HTTP 429 + `Retry-After` 头 | 日志出现 `HTTP 429 限流` | 指数退避 `min(60, 3·2ⁿ)` 秒；单批间隔 ≥3s；单批 ≤1 req/s | 退避重试 5 次仍 429 → 跳下一级源 |
| **连接超时/重置** | `URLError`/`TimeoutError`/`ConnectionError` | 日志 `请求异常 ... timed out` | 超时 30s，重试 5 次后跳下一级降级源 | 5 次全失败 → L5 摘要降级 |
| **403 Forbidden** | Cloudflare/UA 拦截 | 日志 `HTTP 403 被拦截` | 真实 UA `Mozilla/5.0 ... Chrome/120` + `Accept`/`Accept-Language` 头（脚本已内置） | 重试 5 次仍 403 → 跳下一级 |
| **404 on /html/** | 该版本 HTML 不存在 | `try_l0` 返回 404 | 依次试 `v2→v1→无版本`，再降级 L1 ar5iv | ar5iv 也 404 → L2 |
| **PDF 是扫描件** | 提取文本 <500 字符 | `try_l2` 返回 `LOW_TEXT` | **标记 LOW_TEXT，不 OCR**（成本高、收益低），直接降级 L3/L4 | — |
| **PDF 分栏错乱** | 文本连成一片 | 目检 `.txt` | `pdfminer` `LAParams` 调 `line_margin`；仍失败用 HTML 源 | L2 不可用则跳过 |
| **S2 API 限流** | 429（无 key 约 1 req/s） | 日志 S2 超时/429 | 无 key 时**跳过 S2**，不阻塞主流程（L4 降级） | — |
| **OpenReview 需登录** | 401 | `try_l3` 空 | 公开 venue 用 `api2.openreview.net`，仍失败则降级 | — |
| **论文无公开全文** | L0–L4 全失败 | manifest `level=L5` | L5 摘要降级 + 打 `ABSTRACT_ONLY`，解读仅基于摘要+方法图注 | 章节顶部显式声明证据等级 |
| **并发过高被封 IP** | 连续 403/429 | 多请求同时触发 | **强制串行** `for`+`sleep(3)`，禁用线程池 | — |
| **沙箱代理间歇 406（API）** | API 整体 406 | 探针 `all:electron` 也 406 | **整源切换至 RSS**（`fetch_rss.py`），不纠缠 API | RSS 也 406 → 推迟重跑 |
| **沙箱代理偶发整体 404** | 整个查询偶发 404 | 探针连续 3 次 404 | 停止硬扛，记录 `run_log.md` 后**推迟到下一周期重跑**（断点续拉不重复计费） | — |
| **C: 盘 0 字节** | 写入失败 / `rm` safe-delete 报 ENOSPC | `shutil.disk_usage` 接近 0 | Python 直删 `C:/Users/Admin/AppData/Local/Temp`（释放数 GB）后重跑 | 勿依赖 `rm` 的 safe-delete 包装 |

### 6.5 限流升级策略（429/503 退避公式）

```
wait(n) = min(60, 3 · 2ⁿ) 秒，n = 重试次数 (0,1,2,...)
示例：n=0→3s  n=1→6s  n=2→12s  n=3→24s  n=4→48s  n≥5→60s(封顶)
```

- 每次重试前 `time.sleep(wait(n))`；**同一 base_id 内 L0 多版本试探不重置退避计数**。
- 单批（一页元数据 / 一篇全文）间隔 ≥3 秒。
- **封顶 60s × 5 次 ≈ 3 分钟**仍不通 → 该篇跳下一级源；整源（API）连续失败 → 切 RSS；RSS 也失败 → 推迟重跑。

### 6.6 沙箱网络 404 / 406 专项（环境实测，2026-09 持续发生）

本机（WorkBuddy 沙箱）对 `export.arxiv.org` / `arxiv.org/api/query` 的访问**偶发整体 404/406**（连 `all:electron` 最简查询也失败），属代理层不稳定，非脚本缺陷。实测表现：

- 成功批次（09-20、09-21）与调试中均出现 HTTP 200 正常拉取 → 链路本身通畅；
- 09-24 起 `export.arxiv.org` 持续 406，且 `arxiv.org/api/query` 也间歇 406 → **RSS 成为当前最可靠通道**；
- 偶发 404/406 时，单请求退避重试无效（代理层整体拒绝），须**整段重试/切换源**。

**标准动作**：

1. 执行前发 1 次最简查询做连通性探针（API + RSS 各一）；
2. API 406 → 立即转 RSS，不纠缠；
3. 两者皆 404/406/超时连续 3 次 → 不再硬扛，记录 `run_log.md` 后**推迟到下一调度周期或数分钟后重跑**，断点续拉保证不重复计费；
4. 单次抓取若某篇 L0–L4 全失败，自动 L5 摘要降级并打 `ABSTRACT_ONLY`，**绝不伪造**。

> 经验值：2026 年新论文的 arXiv HTML 源（`arxiv.org/html/<id>v<n>`）覆盖率近 100%，L1–L5 基本用不上，是快速路径；抓取 11–21 篇全文约 40–70 秒（串行 + 3s 间隔），无需并发。L0 偶发 HTTP 406（内容协商），脚本按 5 次退避重试后由 `v1`/无版本 URL 命中，最终仍 L0 FULL——属正常降级路径。

### 6.7 证据等级与「绝不伪造」硬约束

- `FULL`：正文 ≥4000 字符且含 Result/Method/Experiment 段。
- `PARTIAL`：1000–4000 字符。
- `ABSTRACT_ONLY`：仅摘要（来自 L5 摘要降级）。

**硬约束**：`ABSTRACT_ONLY` 论文的解读中任何具体数值、实验细节必须标注「（摘要仅述，未在正文核实）」，**严禁据标题/摘要脑补方法细节**。文件头 `# EVIDENCE:` 字段即证据等级，必须如实写入 frontmatter。

### 6.8 全文缺失时的降级解读规范

当某篇 `level=L5` / `evidence=ABSTRACT_ONLY`：

1. 章节顶部显式声明：「⚠️ 本文证据等级为 ABSTRACT_ONLY，以下数值与方法细节仅来自摘要，未在正文核实。」
2. 仅可写：一句话结论、要解决的问题、摘要明示的方法大类、摘要明示的量化结果（附「摘要仅述」标注）。
3. **禁止**：补全公式、补全消融表、补全架构细节、给出摘要未提的对比基线数值。

---

## 7. 落后 / 被取代判定

满足任一即判 `OUTDATED`：① 文献库中已有同问题更优且更晚的结果；② 方法依赖已被淘汰技术栈（须有据）；③ 官方/社区已发布明确更优替代。

**两种登记类型**（实践中「认知纠正」比「被取代」更有价值）：

| 类型 | 含义 | 打标 |
|---|---|---|
| 论文级 `OUTDATED` | 该论文本身被取代 | frontmatter `status: OUTDATED`；索引与章节标题打 `⛔` |
| 技术路线级 / 认知纠正 | 某被广泛采用做法被证明错误或已落后 | frontmatter 仍 `CURRENT`，`flags` 记 `⚠️`；章节标题打 `⚠️ [路线落后·部分]` |

打标须附具体对比论文 ID 与证据，凭印象不得标；证据不足则 `CURRENT` + 章节内写「存疑」。

---

## 8. 产物结构：原子化笔记 + MOC 索引（知识库组合）

用户要求「产物整理为原子化笔记 + MOC 索引的知识库文档组合」。设计原则：**单篇笔记只讲一篇论文（原子化、可长期复用、可被任意日期 MOC 反复链接）；跨论文比较/排行/综合结论一律放入 MOC 或报告（不写进笔记）**。

```
papers/
├── library/
│   ├── registry.jsonl        # 全量文献库：一行一篇，累计不删（覆盖率校验基准）
│   └── outdated.jsonl        # 已判落后/被取代的论文
├── daily/YYYY-MM-DD/
│   ├── 7dim-table.md         # 当日全量 7 维对比表（参考）
│   ├── scored.md             # 评分明细 + 覆盖率校验/重筛记录
│   └── run_log.md            # 执行日志、失败、降级
├── notes/
│   └── <arXivID>__<短标题>.md   # 原子化笔记：一篇一文件，永久沉淀
└── MOC/
    ├── MOC-总索引.md          # 全局地图：赛道 × 时间 × 等级
    └── MOC-YYYY-MM-DD.md      # 当日 MOC，链接当日笔记
```

**原子笔记模板**（frontmatter 含 id/title_zh/track/value/grade/evidence/status/flags/scores/fetch_level/tags）：

```
---
id: arXiv:2609.xxxxx
title_zh: "..."
track: 神经渲染
date: 2026-09-26
value: 4.05
grade: A
evidence: FULL
status: CURRENT            # CURRENT / OUTDATED / SUPERSEDED
superseded_by: [arXiv:2609.yyyyy]
scores: {IMP:5, NOV:5, TEC:4, EXP:4, PER:5, TRL:3, REP:4}
fetch_level: L0
flags: []
tags: [3DGS, 实时渲染]
---
# <中文标题>
## 一句话结论 / 要解决的问题 / 方法详解 / 实验与结果
## 创新点与贡献 / 局限与风险 / 与文献库的关系 / 可复现性 / 行动建议
```

**MOC 组合价值**：总索引提供全局导航（按赛道聚类 + 时间轴 + 等级筛选），当日 MOC 提供单次运行的聚焦视图并链接原子笔记；二者形成「地图 + 房间」的双层知识库结构，支持长期累积与跨日追溯。

---

## 9. 自动化调度与无人值守约束

- 不可交互提问（`AskUserQuestion` 禁用）；遇歧义按默认处理并显式声明。
- 执行前读 `automations/<id>/memory.md` 历史；执行后写高层摘要回该文件。
- 每步产物落盘；失败写入 `run_log.md`。
- 先核验 arXiv 是否有新提交日（3 分类 top-5 `published` 独立核验）；若无新提交，转**补漏模式**（放大 `max_results`，与库做集合差），并在报告中写清实际命中区间，**绝不伪装「当日新论文」**。
- 全文抓取前先「连通性探针」，遇沙箱代理整体 404/406 则切换源或推迟重跑，不硬扛。

---

## 10. 已知风险与待办（来自历史执行 09-20 ~ 09-26）

1. **硬件类渲染方向缺口**：库内论文全部为算法侧渲染（3DGS/扩散），缺近眼显示/光场/全息/波导。需在关键词补 `waveguide`/`light field display`/`varifocal`/`holographic display`/`maxwellian`/`retinal projection`/`pancake optics`/`foveated`/`accommodation-vergence`（`fetch_arxiv.py` 关键词表已补齐，但命中极少，可在 Semantic Scholar 等补）。
2. **沙箱代理 404/406 偶发**：见 §6.6，当前以 RSS 兜底。
3. **非同日竞争论文口径**：同规模世界模型（如 Zing-0.5 vs Astronex-World）不同基准数值不可直接比较，需同口径复测。
4. **脚本历史缺陷（已在新脚本规避）**：arxiv 命名空间传参、`split("v")[1]` 越界、`_manifest.json` 覆盖丢失、罗马数字章节解析、缺失异常名导入导致静默全 L5、`parse_entry` 整份 feed 解析、分页越界卡死——新脚本已全部修复，但**每次跑完仍须核 `WROTE` 与 manifest 证据等级**。
5. **RSS 混入旧稿**：`2601/2603/2604/2605/2606/2510/2512` 等非 2609 旧 ID 与 v2 再公告需剔除，建议 API 恢复后单独 backfill。

---

## 11. 全文抓取故障速查表（Quick Reference）

| 现象 | 第一反应 | 命令/动作 |
|---|---|---|
| 拉取 0 条但 HTTP 200 | 命名空间/解析 bug → 核 `WROTE=N` | 查 `data/raw/*.jsonl` 行数；改整份 `<feed>` 解析 |
| API 探针 406 | 切 RSS | `python scripts/fetch_rss.py --out data/raw/...` |
| 全文全 L5 | 缺失异常导入/网络 | 核 `_manifest.json` 的 level；查网络探针 |
| 写入失败/ENOSPC | C: 盘满 | Python 直删 `%TEMP%` 后重跑 |
| 连续 403/429 | 被限流/封 IP | 强制串行 `sleep(3)`；退避；切源 |
| 探针连续 3 次 404/406 | 代理整体异常 | 记录后推迟重跑（断点续拉） |
| PDF 文本 <500 | 扫描件 | 标 LOW_TEXT，降级 L3/L4，不 OCR |
| 需补旧稿 | RSS 混入旧 ID | 单列 backfill，不混入当日表 |

---

*本手册与 `xr-paper-daily-brief` Skill 互为配套：Skill 是可执行规范（含决策树与脚本调用），本文档是需求梳理 + 操作手册（含 WHY 与逐障碍对策）。两者任一更新需同步另一份。*
