# XR 每日论文雷达 · 需求梳理与操作手册（SOP）

> 本文档由 2026-10-05 自动化运行整理。它把"每日拉取 AR/VR/MR/XR 最新论文并产出解读知识库"这一需求拆解为可执行的步骤，并**重点厘清全文抓取（Step 6）与障碍/限流处置**——这是整条流水线最容易失败、也最影响产出的环节。
> 对应 Skill：`xr-paper-daily-brief`（用户级，已落地并持续打磨至 2026-10-05）。

---

## 一、需求梳理（目标 / 边界 / 成功标准）

**目标**：每个工作日自动拉取 AR/VR/MR/XR 方向最新预印本 → 7 维度对比 → 价值评分 → 排 Top10 深度解读 → 产出"原子化笔记 + MOC 索引"知识库。

**输入边界（硬性）**：
- 数据源：arXiv（cs.GR / cs.HC / cs.CV / cs.MM / cs.RO / cs.AI / eess.IV + 关键词表）。
- 方向关键词必须覆盖**算法侧**（3D Gaussian Splatting、NeRF、SLAM、avatar、haptic、spatial computing、head-mounted、egocentric…）与**硬件侧**（near-eye、light field、waveguide、holographic display、varifocal、maxwellian、retinal projection、pancake optics、foveated、accommodation-vergence）。
- 输出语言：中文；领域术语保留英文原文并附中文（如 3D Gaussian Splatting（3D 高斯泼溅））。

**成功标准**：
1. 不伪造：未抓到全文的内容写"未获取"，不脑补数值、不编造引用。
2. 不凑数：当日最高分 < 3.6 时，Top10 允许少于 10 篇并明确说明。
3. 覆盖闭环：入选引文在价值上必须覆盖当前文献库（三关校验 + 重筛），否则重筛。
4. 落后可追溯：被取代/落后的方法在索引与章节处显式打标，且**必须给出对比论文 ID 与证据**。
5. 持久化：每日更新 `registry.jsonl`，否则覆盖率校验失效。

**非目标**：不做代码复现、不做实验验证、不推送外部（仅落盘知识库）。

---

## 二、八步流水线总览

| Step | 名称 | 关键产出 | 工具 |
|---|---|---|---|
| 1 | 连通性探针 | 选定数据源（API / RSS） | curl + §6.5 |
| 2 | 拉取元数据 | `data/raw/YYYY-MM-DD.jsonl` | `fetch_arxiv.py` / `fetch_rss.py` |
| 3 | 7 维度对比表 | `papers/daily/.../7dim-table.md` | 评分模型（本文 §四权重） |
| 4 | 价值评分 + 分档 | `scored.md` + 快照 | 权重公式 |
| 5 | 覆盖率三关校验 | 同质/赛道/天花板 → 触发重筛 | `dedup_check.py` |
| 6 | **全文抓取（核心）** | `data/fulltext/*.txt` + `_manifest.json` | `fetch_fulltext.py` |
| 7 | 产物组织（原子笔记 + MOC） | `papers/notes/*` + `papers/MOC/*` | 模板（本文 §九） |
| 8 | 最终解读报告 | `reports/XR-Daily-Report-*.md` | 报告模板 |

---

## 三、逐步骤详解

### Step 1 · 连通性探针（P0 必做）
- `API = export.arxiv.org/api/query`（2026-10-02 起恢复 200，为当前主源）；`RSS = rss.arxiv.org/rss/<cat>`。
- 各发 1 次最简请求：API `all:electron`、RSS 任一分类。
- **判据**：API 200 → 用 API；API 406/超时 → 立即转 RSS；两源连续 3 次 404/406/超时 → 记录 `run_log.md` 后**推迟到下一周期**，断点续拉保证不重复计费。
- ⚠️ **周末/周一凌晨特例**：RSS 返回 200 但 `<channel>` 内 **0 条 `<item>`**（arXiv `<skipDays>` 跳过周六日）。此时不要误判为代理故障，直接按 §五"RSS 空频道"处理。

### Step 2 · 拉取元数据
- API：`python scripts/fetch_arxiv.py --since YYYY-MM-DD --max 400 --out data/raw/YYYY-MM-DD.jsonl`
  - 内部：`submittedDate` 降序分页；本地按 `published` 过滤；越过日期下界即 `break`（防全历史扫描卡死）；单批间隔 ≥3s；断点续拉写 `.checkpoint`。
- RSS：`python scripts/fetch_rss.py --out data/raw/YYYY-MM-DD.jsonl`（API 406 兜底）。
- **必核**：脚本末尾 `WROTE=N` 的 N **必须 > 0**，否则静默 0 条（历史曾因命名空间 bug 静默 0 条）。
- **旧稿污染过滤**：RSS "recent" 会把旧稿 replace/cross 混出。只用 `26YY.*` 前缀 + announce type 过滤"真正新提交"；非当月前缀旧稿单列 backfill，**绝不混入"当日新论文"表**。

### Step 3 · 7 维度对比表
固定 7 维（永久不变，保证跨日可比）：

| 缩写 | 维度 | 打分 1–5 判据 |
|---|---|---|
| IMP | 问题重要性 | 5=领域公认卡脖子/高频痛点 |
| NOV | 方法创新性 | 5=新范式/新架构 |
| TEC | 技术完整度 | 5=理论+系统+消融齐全 |
| EXP | 实验强度 | 5=多数据集+真机+大样本用户实验 |
| PER | 性能增益 | 5=相对 SOTA 提升 >30% |
| TRL | 落地成熟度 | 5=已产品化/开源可商用（TRL 1-9 映射） |
| REP | 可复现与影响力 | 5=有代码+数据+高引用/顶会 |

### Step 4 · 价值评分
```
Value = 0.20·IMP + 0.20·NOV + 0.15·TEC + 0.15·EXP + 0.15·PER + 0.08·TRL + 0.07·REP
```
分档：S ≥ 4.2 / A 3.6–4.2 / B 3.0–3.6 / C < 3.0。
权重理由：IMP/NOV 决定长期价值（各 20%）；TEC/EXP/PER 决定可信度（各 15%）；TRL/REP 为加分项（8%/7%），避免"工程包装型"挤占理论突破。

### Step 5 · 覆盖率三关校验（防重复/偏食，触发重筛）
1. **① 同质去重**：Top-N 与近 90 天 `registry` 算标题+摘要 token Jaccard，`sim > 0.62` 判重复 → 剔除/降权，从 B 级池补。
2. **② 赛道覆盖**：归入 12 标准赛道；Top10 应覆盖 ≥5 赛道，否则从 B 级池回补冷门赛道（优先保护 XR 核心赛道）。
3. **③ 价值天花板**：当日最高分 < 库内近 30 天 Top10 均分 → 明确标"非重磅日/无 S 级"，**不得拔高凑数**。
- **重筛闭环（用户硬要求）**：三关任一不通过 → 回补/剔除 → 回到 Step 4 重排，循环直至通过；动作全部写入 `run_log.md` 与报告。首跑时①③不适用，显式记"建立基线"，②照常。

---

## 四、Step 6 · 全文抓取决策树（L0→L5）与证据等级【重点】

**为什么先抓全文再定稿评分**：仅凭摘要无法可靠区分 TEC/EXP/PER（实测 12 篇中 3 篇摘要推断偏差 ≥1 档）。做法：先按摘要筛 N+2 篇抓全文，再依正文证据定稿，最后取 Top N。

### 4.1 降级链路（任一级成功即停）
```
L0  arXiv HTML 全文   https://arxiv.org/html/<id>v<n>      ← 首选，2023+ 论文覆盖≈100%
L1  ar5iv 转换版      https://ar5iv.labs.arxiv.org/abs/<id> ← HTML 缺失/老论文
L2  arXiv PDF→文本    https://arxiv.org/pdf/<id>v<n>        ← 需 pdfminer.six；扫描件<500字→LOW_TEXT 不OCR
L3  OpenReview         https://api.openreview.net/notes?forum=<id>  ← 已投会
L4  Semantic Scholar   .../paper/arXiv:<id>?fields=openAccessPdf,abstract,tldr  ← 429 则跳过
L5  摘要降级（绝不伪造）← 全部失败时的最后手段，章节顶部显式声明证据等级
```

### 4.2 版本探测顺序
`v2 → v1 → 无版本` 依次试探；HTML 偶发 HTTP 406（内容协商）按 5 次退避重试后由无版本 URL 命中，最终仍 L0 FULL 属正常路径。

### 4.3 证据等级（写进每篇笔记 frontmatter）
- `FULL` — 完整正文（HTML/PDF 提取 ≥4000 字符且含 Result/Method 段）。
- `PARTIAL` — 仅部分章节或文本量不足。
- `ABSTRACT_ONLY` — 仅摘要。**硬约束**：解读中任何具体数值/实验细节必须写"（摘要仅述，未在正文中核实）"，**严禁据标题/摘要脑补方法细节**。

### 4.4 脚本与输出
`python scripts/fetch_fulltext.py --ids 2610.xxxxx,2610.yyyyy --out data/fulltext/ --abstracts data/raw/YYYY-MM-DD.jsonl`
- 输出 `data/fulltext/<id>.txt`：头部含 `# LEVEL:` / `# EVIDENCE:` / `# CHARS:` / `# URL:`，正文为清洗文本。
- `_manifest.json` **合并写入**（分批追加不丢历史）。
- **强制串行**（每篇 `time.sleep(3)`，禁用线程池/并发），避免封 IP。

---

## 五、障碍与限流解决矩阵【核心】

| 障碍 | 症状 | 对策 |
|---|---|---|
| arXiv 429/503 限流 | `Retry-After` 头 | 指数退避 `min(60, 3·2^n)` 秒；**每请求 ≥3s**；单批 ≤1 req/s |
| 连接超时 | `URLError: timed out` | 超时 30s，重试 3 次后跳下一级降级源 |
| 403 Forbidden | Cloudflare/UA 拦截 | 真实 UA + `Accept`/`Accept-Language` 头 |
| HTML 源不存在 | 404 on `/html/` | 立即降级 L1 ar5iv |
| PDF 是扫描件 | 提取 <500 字符 | 标 `LOW_TEXT`，改 L3/L4；**禁止上 OCR**（成本高收益低） |
| PDF 提取乱码/分栏错乱 | 文本连成一片 | pdfminer `LAParams(line_margin=0.5)`；仍失败用 HTML 源 |
| S2 API 限流 | 429（无 key 约 1 req/s） | 加 `x-api-key`（若有）；否则**跳过 S2，不阻塞主流程** |
| OpenReview 需登录 | 401 | 公开 venue 用 `api2.openreview.net`，仍失败则降级 |
| 论文无公开全文 | 全部失败 | 标 `ABSTRACT_ONLY`，解读仅基于摘要+图注，**章节顶部显式声明** |
| 并发过高封 IP | 连续 403/429 | **强制串行** `for`+`sleep(3)`，禁线程池 |
| **RSS 周末空频道** | HTTP 200 但 `<item>`=0 | **节律性空源**，非故障；转"状态报告+文献库参考表"，下个工作日再拉（见 §六） |
| 沙箱代理整体 404/406 | 连 `all:electron` 最简查询也失败 | 代理层不稳，单请求退避无效；整段切源/推迟重跑（见 §六） |

**退避升级公式**：`wait(n)=min(60, 3·2ⁿ)`（n=重试次数）：n0→3s, n1→6s, n2→12s, n3→24s, n4→48s, n≥5→60s 封顶。封顶 ×5 仍不通 → 该篇跳下一级源；整源（API）连续失败 → 切 RSS；RSS 也失败 → 推迟重跑。同 `base_id` 内多版本试探**不重置**退避计数。

---

## 六、沙箱网络专项（环境实战）

本机（WorkBuddy 沙箱）对 arXiv 的访问有代理层不稳定史（非脚本缺陷）：
- 2026-09 多数日期 `export.arxiv.org` 间歇 406、`arxiv.org/api/query` 亦 406 → `rss.arxiv.org` 成最可靠通道。
- **2026-10-02 起 `export.arxiv.org` 恢复 200**，API 重新成为主源；但 RSS 在周末恒为空频道（§五）。
- 偶发 404/406 时单请求退避重试**无效**（代理层整体拒绝），须**整段重试 / 切源 / 推迟**。
- 经验值：2026 年新论文 arXiv HTML 源覆盖≈100%，L1–L5 基本用不上；抓 11–21 篇全文约 40–70s（串行+3s 间隔），无需并发。
- C: 盘可能 0 字节导致 `rm` safe-delete 包装报 ENOSPC；清理 Temp 用 Python `os.remove`/`shutil` 直删而非依赖 `rm`。

**标准动作**：执行前发连通性探针（API+RSS 各一）→ API 406/超时立即转 RSS → 两源连续 3 次失败则记录 `run_log.md` 后推迟重跑，断点续拉保证不重复计费。

---

## 七、覆盖率三关与重筛闭环（回顾）

见 Step 5。强调：**重筛是循环不是一次性检查**。文献库为空（首跑）时①③不适用、显式记"建立基线"，②照常执行（首跑正是靠②触发回补）。不得为凑齐 10 篇保留同质或低覆盖度论文。

---

## 八、落后 / 被取代判定与打标

**判定 `OUTDATED` 的条件（满足任一）**：
1. 文献库已有同问题更优量化结果且时间更晚；
2. 方法依赖已被淘汰技术栈（如纯 NeRF MLP 表示被 3DGS 全面超越、传统特征点 SLAM 被学习式全面超越，需有据）；
3. 官方/社区已发布明确更优替代实现。

**两类登记**（后者更有实用价值）：
- **论文级 OUTDATED**：该论文本身被取代 → frontmatter `status: OUTDATED`，索引行尾 `⛔ OUTDATED（已被 arXiv:xxxx 取代）`，章节标题 `## [落后] 第 N 章`。
- **技术路线级 / 认知纠正**：某广泛做法被证明错误或已落后 → frontmatter 仍 `CURRENT`，`flags` 记 `⚠️`，章节标题 `⚠️ [路线落后·部分]`（如"CLIP 特征线性平均会破坏有效性""3DGS 渐进传输应按不透明度而非尺度剪枝"）。

⚠️ 打标**必须给出具体证据与对比论文 ID**，不得仅凭印象；证据不足标 `CURRENT` 并写"存疑"。

---

## 九、产物结构：原子化笔记 + MOC 索引【知识库组合】

```
papers/
├── library/
│   ├── registry.jsonl          # 全量文献库（累计不删，每日追加）
│   └── outdated.jsonl          # 已判落后/被取代
├── daily/YYYY-MM-DD/
│   ├── 7dim-table.md           # 当日全量 7 维对比表（参考）
│   ├── scored.md               # 评分 + 覆盖率校验
│   └── run_log.md              # 执行日志/失败/降级
├── notes/<arXivID>__<短标题>.md # 原子化笔记：一篇一文件，永久沉淀
└── MOC/
    ├── MOC-总索引.md            # 全局地图：赛道 × 时间 × 等级
    └── MOC-YYYY-MM-DD.md        # 当日 MOC，链接当日笔记
```

**原子笔记模板**（frontmatter + 9 小节）：
```markdown
---
id: arXiv:2610.xxxxx
title_zh: "..."
track: 渲染与显示            # 12 赛道之一
date: 2026-10-xx
value: 4.35
grade: S
evidence: FULL              # FULL / PARTIAL / ABSTRACT_ONLY
status: CURRENT             # CURRENT / OUTDATED / SUPERSEDED
superseded_by: [arXiv:2610.yyyyy]
scores: {IMP:5, NOV:5, TEC:4, EXP:4, PER:5, TRL:3, REP:4}
fetch_level: L0
tags: [3DGS, 近眼显示, 实时渲染]
---
# <中文标题>
## 一句话结论 / 要解决的问题 / 方法详解（含关键公式·保留原文术语）
## 实验与结果（表格化关键数字）/ 创新点与贡献 / 局限与风险
## 与文献库的关系（新增/改进/取代 X）/ 可复现性 / 行动建议
```
**原子化原则**：单文件只讲一篇；跨论文比较/排行/综合结论一律放进 MOC 或报告，**不写进原子笔记**——这样笔记可长期复用、被后续 MOC 反复链接。

**最终报告** `reports/XR-Daily-Report-YYYY-MM-DD.md`：一、执行摘要；二、Top10 排行榜；三、逐篇深度解读（每篇一章，按重要性降序，含上表全部小节）；四、当日全量 7 维对比表（参考）；五、覆盖率校验与筛选说明；六、附录：抓取失败/降级清单 + 证据等级分布。

---

## 十、无人值守约束 & 今日（2026-10-05）实测结论

**无人值守硬约束**：不得并发请求；每日必更新 `registry`；落后标记必有对比 ID 证据；原子笔记与 MOC 分离；不伪造、不凑数。本运行无法交互，凡遇模糊一律取"保守且诚实"默认（如无法确认新提交则判定无新增，不强行拉旧稿）。

**2026-10-05 实测**：
- 周一凌晨，RSS 全分类 `<item>`=0（`<skipDays>` 跳过周末）→ 转 API。
- API `fetch_arxiv.py --since 2026-10-02` → `WROTE=0`；最新命中 `published=2026-10-01`，已入馆（registry 含 10-01 共 19 篇、10-02 共 6 篇）。
- **结论：当日无新增 XR 提交**（周末节律 + submittedDate 滞后）。本运行转"状态报告 + 文献库前沿参考表"模式，**未伪造 Top10**。
- 下一个工作日（周二 2026-10-06）arXiv 将公告积压提交，API `submittedDate` 正常拉取即可。
- 历史遗留 backfill（7~12 篇非 2609 高价值旧稿）建议择机单开批次，API 现已健康。

> 本文档与 `xr-paper-daily-brief` Skill 互为补充：Skill 是机器可执行的操作定义，本文档是人的"需求+判读"手册。两者同步维护。
