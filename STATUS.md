# STATUS.md — 运行状态与未完成事项

> **每轮更新规则（写死，勿删）**
> 1. 每次每日运行或整改批次结束后更新本文件：顶部时间、§1 增删、§4 判决状态、§5 自检结果。
> 2. 只在**事实变化**时改动；不要为了"看起来在维护"而刷新时间戳。
> 3. 每条必须四要素：现象 / 影响 / 当前处置 / 触发条件或责任。
> 4. 关闭的事项从 §1 移入 §2，保留编号，不删除（可追溯）。

- **最后更新**：2026-11-28（**状态日 0 新稿**：11-27 周五公告组未释放——工作日公告跳空（同 10-29 / 11-12）；listing 7/7 分类最新公告日仍 **11-26**，11-27/11-28 组 `declared=None`；API 前沿 2026-11-25 且 `submittedDate:[20261126 TO 20261128]` 0 篇；RSS 6 分类空源、cs.AI 398 条为陈旧 feed（全部 ⊂ 上批 849 条，`cur_only=0`）；11-26 组复采 695 槽位 / 569 唯一，未入馆 513 篇摘要覆盖 513/513、命中 47 篇全部落在 11-27 处置集合 → **0 漏网**；门③ 现算 **4.465**（[2026-10-29, 2026-11-28)、659 条入窗、无追加批））
- **当前库况**：registry **1332** / notes **954** / daily **84** ｜ 最新真实批次 2026-11-27（55 篇，A37/B13/C5，0 S，门③ margin −0.109）｜ 11-27 卡片 count=55 / backfill-1127 卡 count=8 / 11-28 卡片 count=0（refPapers 63）｜ 门③ 现算基线 **4.465**（窗口 [2026-10-29, 2026-11-28)，659 条入窗）
- **回滚点**：`v1.0-20261118`（本地 + 远端）

## 1. 未完成事项（Open）

| ID | 现象 | 影响 | 当前处置 | 触发条件 / 责任 |
|---|---|---|---|---|
| O-1 | 渠道① `xr-paper-hub.app.workbuddy.host` 返回 403（3174 bytes） | 双渠道变单渠道 | 不修；报告如实写「渠道①不可用（第 N 批挂账）」，禁止声称已发布 | 托管侧重签后可恢复；累计 **39 批**（2026-10-21 ~ 11-28，按每日运行计含状态日） |
| O-2 | registry 内 65 行赛道非规范（63 行「—（非 XR）」+ `具身交互` 1 + `空间计算` 1） | 统计口径轻微失真 | **WONTFIX**：前端有 `#8a93a8` 兜底配色，改数据需动 65 行并重建前端 | 若将来做赛道重分类时一并处理 |
| O-4 | `audit_gap_listing.py` 未并入「目标组 >500 条补页」逻辑 | 极端大日组可能少采 | **WONTFIX**（随 R-03 抽库一并放弃）；每日实例以 `audit_listing_1117.py` 为模板，含补采 | 若某日目标组 >500 且 declared≠got 时报错（守卫会 exit 2） |
| O-5 | `send_automation_result` 在部分会话不可见 | 收尾汇报可能失败 | 观察项：不可见时改用 present_files + 报告正文 | 连续 2 次不可见则改指令 |
| O-7 | 11-18 / 11-19 两批未做残差复核（脚本 11-19 才上线） | 历史漏检未知 | 不回补；从 11-20 批起记录 rate | — |
| O-8 | golden 仅 25/100 kw-missed + 20/20 accepted 有人工标签 | 精确率/召回基于小样本（n=40） | 已记 CI；如需收窄 ±2pp 需再标约 400 条 | 用户决定是否扩大标注 |
| O-9 | 历史 `data/gates_*.json`（≤1117）缺 `window_excludes_*` 留痕字段 | 事后无法自证当时口径 | **grandfather 不回算**（与门③ 历史值政策一致） | 仅新批必须齐四字段 |
| O-10 | `update_moc_<MMDD>.py` 等一次性锚点脚本，重跑即 `ANCHOR NOT FOUND` | 无法幂等重跑 | 已知限制，不修；重跑前用 `git show <批次前commit>` 还原 MOC | 需要重跑时按此办法 |
| O-11 | Jev API 返回 **451**（法律原因不可用）；AnyJev 需本地 LLM，本机无 GPU | 决策模型路线受阻 | 搁置；已用现有模型做盲评基线（7/7 精确） | 若区域放开或有 GPU 再评估 |
| O-13 | `deploy-pages.yml` 的 **`schedule` 触发**必失败：`No artifacts named "github-pages" were found`；**11-26 追加观察**：push 与 `workflow_dispatch` 亦会复现（本批 run `45682922667` / `45683161976` 连续 3 次 failure），而 `Upload artifact` 明确成功（Artifact ID `15054012962`、4,558,066 bytes），`deploy-pages` 侧 `Found 0 artifact(s)` | 定时重部署不生效；push 偶发空跑（run 1 rerun 即恢复，run 2 三次均失败） | 未改 workflow（如实登记）；遇 `No artifacts` 先 `gh run rerun <id>`，连续两次同错按平台 incident 处理、不改产物不重复推送 | 若 schedule 需可重部署，给 build job 补 schedule 分支；若 push 连续 3 次同错，等 GitHub status 恢复并补推一次空提交 |

## 2. 已关闭（保留编号，不删）

| ID | 项 | 关闭依据 | 日期 |
|---|---|---|---|
| C-1 | TPIR round-01 的 F-01~F-12、N-01~N-08 全部缺陷 | b02 确认席 14/14；b03 base 1/6 → fixed 6/6 | 11-17~11-18 |
| C-2 | R-02 github 可达性未实测 | 实测 `blob/main/` 文档链接 **HTTP 200** | 11-18 |
| C-3 | R-03 对账脚本抽公共库 | 改口径为「写盘守卫 + 基线只减不增」+ CI 步骤 | 11-18 |
| C-4 | R-05 `truncated` 未检查 / R-06 RSS 解析未兜异常 | 注入测试：truncated→RuntimeError；截断 XML→exit 2 | 11-18 |
| C-5 | 11-19 批 `s_awarded` 为 null | 补字段并重算，12 字段不变；发布门 G2 由此 PASS | 11-19 |
| C-6 | 召回缺口的量化（此前"0 漏网"结论无独立证据） | 100 条盲评：7/7 确认为真，漏检率 7.0%（CI 3.4–13.7%） | 11-19 |
| C-7 | `check_release.py` 只认 `gates_YYYY-MM-DD.json`，而实际文件名是 `gates_MMDD.json` → 批次日期解析成 "1119"，G3 的「本批泄漏 S」**一直在空跑** | 改为读 `gate3.window_hi`；注入一条 11-19 的 S 后 G3 正确变红（VERDICT FAIL / rc=1） | 11-19 |
| C-8 | 前端冒烟未覆盖排序/隐藏/弹层（原 O-3） | 新增 3 组交互断言：7 档排序（date-asc 单调、date-desc 日期降序且同日次键升序、count/avg/max 升降单调）+ 隐藏开关（localStorage 落盘、卡片 hidden、复原）+ 信息弹层（开/关）；注入排序反转与弹层移除各使其变红 | 11-19 |
| C-9 | 前端 2026-11-20 批次卡 `表内=0`、backfill-1120 卡不出现 | ① `7dim-table.md` 表头缺 `arXiv` 列，`_parse_rows` 取不到 ID 锚点 → 整行跳过；② `papers/daily/backfill-1120/` 目录根本不存在（batches 以目录枚举）。修：`scripts/fix_tables_1120.py` 重写两张表（带 `#`+`arXiv` 占位），补 backfill 目录（7dim/scored/run_log）+ `reports/XR-Backfill-Report-1120.md`；`build_scored_1120.py` 表头同步修正。复算 表内=25（18A/4B/3C，max 4.33）/ 3（2A/1B，max 4.05） | 11-20 |
| C-10 | `check_release.py` G2 FAIL：`gates_2026-11-20.json` 口径字段写在顶层、文件名偏离 `gates_MMDD.json` 约定 | 该文件名在 `sorted(glob)` 中**永远排最后**，会遮蔽后续所有 `gates_MMDD.json`，使 G2/G3 静默空跑。修：字段收进 `gate3`（含 `window_lo/hi`、`in_window`、`top10_mean`、`top10_lib`），改名 `data/gates_1120.json`，`build_scored_1120.py` 落盘路径同步改 `gates_{MMDD}` → G2/G3 PASS | 11-20 |
| C-11 | 残差复核（第 3.5 步，原 O-6）从未真跑 | 11-20 批首次执行：`residual_scan.py dump 1120` 扫描 434 条、判 12 条（2.8%）、逐条写 `verdicts_1120.py` 后 ingest，采纳 3 篇（2611.23417/23534/24193）；`data/residual_1120.json` + `data/verdicts.jsonl` 的 `residual_rate=0.0276` 双留痕，6 处产物均带「残差复核」行 | 11-20 |
| C-12 | `latest_gates()` 按文件名排序取最后一个，遇到 `gates_YYYY-MM-DD.json` 会永久遮蔽后续 `gates_MMDD.json`（C-10 的根因之一） | 改为遍历全部 `gates_*.json`、按内容 `gate3.window_hi` 取最大；构造 `gates_2099-01-01.json`（window_hi=2099-01-01）验证会正确选中它，删除后回到 1120 | 11-20 |
| C-14 | 状态日（0 新稿）的 gates 无 `today_max`/`margin`，`check_release` 会误判 G2 FAIL；运行方因此**两天没敢记账**，台账缺 11-22/11-23 | 新增状态日分支（`run_type=status_day` 或 `today_max is None`）：G2 只验窗口字段、G3 标注「本批无新稿」、R 记不适用，判决记 **N/A**（不是 PASS，避免把「没检查」写成「检查过」）；新增 `--batch YYYY-MM-DD` 补记，台账现 7 条完整 | 11-25 |
| C-15 | **O-12**：`fetch_fulltext.py` 缺 landing-page 守卫，ar5iv 摘要落地页（4–5k 字符、含 References）会被判 `FULL`，证据等级系统性虚高 | 已改 `grade_evidence()`：新增 `LANDING_RE`（一级章节标题：Introduction/Method/Results/…），规则改为 `n>=4000 且 has_core 且 not (n<8000 且 not has_body)` → FULL，否则 PARTIAL/ABSTRACT_ONLY；`py_compile` 通过；本批 63 篇最小 24,073 字符、守卫未触发即生效，**63/63 FULL** | 11-26 |
| C-13 | `MOC-总索引.md` 11-20 明细段缺失（批次表有行、正文无 `### 2026-11-20 新增` 段） | 总索引无法按批次查到该批 Top10 | 11-21 运行补齐该段（10 行 Top10 表 + 门③ 留痕 + 一行「本节为 11-20 运行遗漏、于 11-21 补齐」标注）；后续批次收尾增加「总索引明细段数 = 批次表行数」自检 | 已修；若再出现同类缺段，按此段标注补写 |

## 3. 关键红线（违反即视为回归）

1. **档位**：S 需 `value ≥ 4.20` **且** `gate3.blockbuster=true`（blockbuster = 机械重磅 且 margin ≥ 0.05）。禁止用 `heavy_day_raw`。
2. **档位实现**：五处（7 维表 / 笔记 / registry / 报告 / MOC）一律调 `grade_caliber.assign_grade`，不得内联阈值。
3. **门③ 留痕**：`data/gates_<日期>.json` 必须含 `heavy_day_raw` / `margin` / `blockbuster` / `s_awarded` + `window_excludes_*`。
4. **对账守卫**：新 `audit_listing_*.py` 必须带 `if ok_cats < len(CATS): … sys.exit(2)`，且在任何 `json.dump(...missed...)` 之前；基线只减不增。
5. **残差复核只报警**：`data/residual_*.json` 不得并入候选池或 registry。
6. **发布前自检**：`python scripts/check_release.py` 必须全 PASS 才可发布。
7. **诚实口径**：公告日≠拉取日；非重磅日不得有 S；不虚构 Top10。
8. **临时文件**：只写 `D:\Agent\.tmp`，不落 C 盘。

## 4. 判决（DoD）状态

- **当前**：`CONDITIONAL_PASS`（TPIR round-01，确认席 2026-11-17 出具）。
- **未升格原因**：协议规定 `context=isolated` 上限即 CONDITIONAL_PASS；b03 的整改仍由修复方自评，未再起独立确认席。
- **处理方式（已定为常态）**：**不追求一次性"结项 PASS"**，改为**按批判决**——每批以四项为放行门：
  1. `check_release.py` 三关（计数 / 留痕 / 档位自洽）；
  2. 门① Jaccard / 门② 赛道数 / 门③ margin 三项数值；
  3. 残差复核 rate（连续 3 日 >12% 上报）；
  4. 前端冒烟 + 线上 md5 核对。
  历史判决归档，不再重开；若确需 `PASS`，另起独立确认席（约 30 分钟，仅对当批断言复跑）。
- **最近一批**：`2026-11-28` 判 **N/A（状态日）**（G1 **1332/954/84** 三计数一致；G2 `gates_1128.json` 状态日分支：`today_max/margin=null`、`blockbuster=false`、`s_awarded=false`，窗口字段 `[2026-10-29, 2026-11-28)` / `in_window=659` / `top10_mean=4.465` 齐；G3 本批无新稿、泄漏 0；R 残差「不适用」——无 `nonxr_1128` 池，**未补造**）。状态日按 C-14 口径记 **N/A** 而非 PASS，且不 `--record`（沿用 11-13/11-16 状态日惯例，`data/verdicts.jsonl` 仍 9 批）。上一批 `2026-11-27` 判 PASS（G1 1332/954/83；残差 5.71%，非重磅日无 S，门③ margin −0.109）。
- **2026-11-22（周日状态日）**：`check_release.py` → **WARN**（G1 1082/718/**74** PASS、G2 `gates_1122.json` 字段齐 PASS、G3 无泄漏 PASS；R 项因状态日未生成 `residual_1122.json` 报「未执行」）。**WARN 不阻塞发布**，如实登记而非补造残差文件；未 `--record`（状态日无批次，沿用 11-13/11-16 状态日不记账惯例）。
- **2026-11-23（周一凌晨状态日）**：`check_release.py` → **WARN**（G1 1082/718/**75** PASS、G2 `gates_1123.json` 字段齐 PASS、G3 无泄漏 PASS；R 项「未执行」= 状态日无 `nonxr_1123`，**未补造**）。四源一致：listing 7/7 最新公告日 11-20、缓存穿透与跨学科复验一致、API 前沿 11-19 + 三日区间各 0 篇、RSS `WROTE=0 OK_CATS=7/7`。**下一批（11-24 周二 02:30）才处理周末 11-21/11-22 提交积压**。

- **读数修正（2026-11-21）**：残差漏检率 **1.6%（7/431，95% CI 约 0.7%–3.3%）**，与 11-20 的 2.8%（12/434）同处低位，连续两批远低于 12% 上报阈值。三批实测（2.8% / 1.6%）均显著低于早期 100 条抽样给出的 7.0%，**抽样值只作上界**。

- **读数修正（2026-11-20）**：残差漏检率首跑实测 **2.8%（12/434，95% CI 约 1.6%–4.8%）**，
  是此前 100 条抽样的 7.0%（折算 25–102 篇/批）的 1/2.5。**全量扫描优于抽样，后续引用以实测为准**，
  7% 仅作上界参考。按 2.8% 折算：约 **12 篇/批**被判应收录，本批采纳 3 篇入馆。
- **门③ 口径反事实测算（2026-11-27，仅测算未改规则）**：把 S 稿从窗口 top10 剔除后重算均值，逐日对比：

  | 批次 | today_max | 均值(现) | 均值(剔S) | margin(现) | margin(剔S) | 是否翻转 |
  |---|---:|---:|---:|---:|---:|---|
  | 11-18 | 4.43 | 4.403 | 4.347 | +0.027 | +0.083 | **会翻成 S** |
  | 11-21 | 4.43 | 4.423 | 4.372 | +0.007 | +0.058 | **会翻成 S** |
  | 11-26 | 4.57 | 4.432 | 4.385 | +0.138 | +0.185 | 不变（已授 S） |
  | 11-27 | 4.35 | 4.459 | 4.385 | −0.109 | −0.035 | 不变 |

  结论：现行口径确实更严，但只影响 11-18 / 11-21 两篇 4.43。**暂不改**——预设触发条件
  （S 连续 15 天为 0）未命中：11-26 恰是第 15 天，授出 3 篇 S（4.57/4.40/4.38，margin +0.138）。
  且两种口径都自洽，「打败近 30 天最强阵容」更符合「不虚构 S」的立场。改口径前须重跑本表并写明理由。

- **判决记账**：`python scripts/check_release.py --record` 会把本批判决写入 `data/verdicts.jsonl`
  （按批次日幂等：`{batch, verdict, counts, gate3, residual_rate, reasons, at}`）。
  三档语义：`PASS` 全绿；`WARN` 有诊断性问题但不阻塞（如残差复核未执行、漏检率 >12%）；
  `FAIL` 硬门不过（计数不一致 / 留痕缺失 / 档位泄漏），**不得发布**。

- **规则复审触发条件（预先定义，避免凭感觉改规则）**：
  1. **S 连续 15 天为 0**（当前 11-16~11-21 已 6 天；历史最长空档 10-20→11-06 共 17 天，故 6 天不算异常）；
  2. 残差 rate **连续 3 日 >12%**（已在 §3 红线）或 **连续 10 日 <0.5%**（说明扫描无收益，考虑降频）；
  3. 门② 连续 5 日恰好 =5 赛道（贴线）→ 复核赛道覆盖口径是否过松；
  4. 出现「事后被判定为重磅、当时却记 A」的实例 → 复核 margin 阈值（0.05）。
  以上任一触发才动规则；未触发时**代码与任务说明保持不动**。
- **有效性边界（截至 11-21）**：已证明「防通胀有效」（S 不再按分数自动发，两次险过被挡）
  与「可观测有效」（召回缺口从不可见变为每日一个数）；**尚未证明**阈值最优与召回充分
  （残差仅 2 个样本点：2.8% / 1.6%）。

## 5. 每轮自检清单（收尾前逐条打勾）

**2026-11-28（状态日 · 11-27 周五公告组未释放 · 0 新稿）**

- [x] `python scripts/check_release.py` → **N/A（状态日）**（G1 **1332/954/84** ｜ G2 `gates_1128.json` 状态日分支验窗口字段 → PASS ｜ G3 本批无新稿、泄漏 0 → PASS ｜ R 残差「不适用」，**未补造 residual 文件**）；按 C-14 口径记 N/A，不 `--record`
- [x] `python scripts/check_audit_guard.py` 无违规（**31 份**脚本：守卫 13 / 基线豁免 18 / 违规 0；本日新增 `audit_listing_1128.py` 自带 `ok_cats<7 → exit 2` 且在任何 `json.dump(...missed...)` 之前）
- [x] 对账 `audit_listing_1128.py` **7/7 分类 exit 0**：最新公告日**均为 2026-11-26**（CV 288/GR 10/HC 20/MM 7/RO 109/AI 248/IV 13 = **695 槽位**，逐分类 declared=got）；`NEW_DAYS = [2026-11-27, 2026-11-28]` 两日 `declared=None / got=0` → **11-27 周五组未释放**（工作日公告跳空，同 10-29 / 11-12）
- [x] 交叉复核：`recent?cb=1128a` 与 `pastweek`（cs.CV）均 `Thu, 26 Nov 2026`；跨学科 `math.AP` / `cs.CL` `pastweek` 同为 11-26 → 排除分类级 / 本机故障
- [x] 上一组复采：11-26 组重新拉取去重 **569 篇唯一**（`data/group_1126_1128.json`），已入馆 **56**（11-27 主批 55 逐篇在组内 + 1 篇库内既有 cross 再公告），未入馆 **513**；摘要覆盖 **513/513 = 1.0000**，摘要/标题级命中 **47 篇全部**落在 11-27 处置集合 → **0 漏网**（`data/missed_xr_1128.json` 为空）
- [x] RSS 判读（本日关键）：`OK_CATS=7/7`、`WROTE=398`；6 分类 0 条目；cs.AI 398 条 `lastBuildDate` Fri 27 Nov 05:00 UTC、条目 `published` 全为 11-27，**看似新公告**，逐条 `base_id` 比对上一批 `2026-11-27.jsonl`（849 条）→ **全部在内、`cur_only=0`** → 判为陈旧 feed 重戳日期，不构成新稿
- [x] `data/gates_1128.json` 四字段齐全且布尔自洽（`today_max=null`、`margin=null`、`heavy_day_raw/heavy_day/blockbuster/s_awarded` 全 false、`verdict=no_candidate_status_day`）+ `window_excludes_today=true`、`window_excludes_this_run_batches=true`、`this_run_batches_excluded=[]` + `window_lo/hi = 2026-10-29 / 2026-11-28`、`in_window=659`、`top10_mean=4.465`
- [x] 门③ 现算 **4.465**（较上批 4.459 +0.006：10-28 批出窗、11-27 批入库含 backfill 4.43）；窗口每日滑动，已在报告与 MOC 注明「下一批勿沿用」
- [x] 残差复核 **不适用**（状态日无 `nonxr_1128`），未生成 `data/residual_1128.json`；历史 rate 留档 1.52%（11-26）/ 5.71%（11-27），距 12% 阈值远
- [x] 前端重建 `verified: {papers:1332, notes:954, batches:84}`；11-28 卡 `count=0` + `refPapers=63`（前沿参考）、11-27 卡 `表内=55`、backfill-1127 卡 `表内=8`；`BATCH_LABELS` 补 1 条中文标签
- [x] 前端冒烟 **PASS**：`papersEqDisk / notesEqDisk / batchesEqDisk` 全 true；5 标签渲染 4/2/2/3/1；排序 8 项单调性 + 隐藏开关 + 弹层三组交互；`nCards=84`；lastThree 首卡 2026-11-28；`PAGE_ERRORS: none`（内联脚本另做 `node --check` 双块通过）
- [x] 总索引刷新：状态注记追加 11-28、批次表加 1 行（`2026-11-28 | — | 0 新稿`，状态日**不配明细段**，与 11-22 / 11-23 同例）、速查入口「最新运行状态」换 11-28 报告、「最后更新」行由 11-24（积压未更新）修正为 11-28；自检：批次表 78 行 / 明细段 64 段，缺段 20 行**全部为状态日或历史早批**（本批新增 1 行属状态日、无段，不计失配）
- [x] 交付前抽查 `title == id` / `len(title)<12`：本日无新增行（registry 无变更），历史抽查仍 0 命中
- [x] 渠道② 已实推并核验：本地 commit **`ccfc99d`**（23 文件）→ 增量推送（**23** 变更 / 2,579 未变 / 删除 0）→ 远端 main **`88abd8b2`** → deploy run **`46051337762` success**；线上 **HTTP 200 / 7,594,781 bytes**、含 `const DATA`，LF 归一化 md5 **`df69a604fdb66b88c87ed339283c05b2`** 与本地**逐字节相等**；线上 DATA 1332/954/84、11-28 卡 count=0 / refPapers=63、11-27 卡 count=55、backfill-1127 卡 count=8
- [x] 渠道① 不可用：本会话 ToolSearch **无** `workbuddy_sites_deploy` → 报告与 run_log 写「渠道①不可用（累计第 **39** 批挂账）」，**未声称已发布**

**2026-11-27（上一批，留档：11-26 周四公告批次，单日组、无周末积压；非重磅日无 S）**

- [x] `python scripts/check_release.py` → **PASS**（G1 **1332/954/83** ｜ G2 `gates_1127.json` 无缺、险过四字段齐 ｜ G3 本批授予S=False、backfill 记S=0、泄漏 0 ｜ R 残差 **5.7%**）；`--record` 已写入 `data/verdicts.jsonl`（共 **9** 批）
- [x] `python scripts/check_audit_guard.py` 无违规（**30 份**脚本：守卫 12 / 基线豁免 18 / 违规 0；本日新增 `audit_listing_1127.py` 自带 `ok_cats<7 → exit 2` 且在任何 `json.dump(...missed...)` 之前，并传入第三参数窗口下界 2026-11-25）
- [x] 对账 `audit_listing_1127.py` **7/7 分类 exit 0**：11-26 组 **695 槽位 / 569 唯一**（CV 288/GR 10/HC 20/MM 7/RO 109/AI 248/IV 13）；11-27 组 `declared=None`（未释放）；11-25 组复采逐分类 declared=got（CV 302/302 含 `skip=500` 补 90、AI 300/300 含补 48）→ **无新增漏跑窗口**
- [x] 上一组复采核验（`scripts/missed_xr_1127.py`）：11-25 组未入馆 **569 = 624 − 55**，摘要覆盖 **569/569 = 1.0000**、缺摘要 0；摘要/标题级命中 **53 篇全部**落在上批处置集合 → **0 漏网**（`leak_n=0`）
- [x] `data/gates_1127.json` 四字段齐全且布尔自洽（`today_max=4.35`、`heavy_day_raw=false`、`heavy_day=false`、`margin=-0.109`、`blockbuster=false`、`s_awarded=false`、`verdict=non_blockbuster`）+ `window_excludes_today/this_run_batches` 留痕 + `window_lo/hi = 2026-10-28 / 2026-11-27`、`in_window=626`
- [x] **门② 回补一次**：纯值 Top10 仅 4 赛道（重建与SLAM×5）→ 剔 2611.34932（4.01，该赛道第 5 篇、**仍入馆写笔记记 A**）补 2611.33467（4.00，世界模型与仿真）→ 定稿 5 赛道；`gates_1127.json` 的 `gate2.rescreen_ops` 与笔记正文均留痕
- [x] **库内 cross 再公告去重**：2611.30173 在池内且 `in_registry=true`（11-25 批 3.71），初版定稿误纳入 → 移入 REJECT，主批 44→43、全量 64→63，并**重跑 `build_scored_1127.py` 与 `gates_1127.py`**（否则门① 会与自身比对、虚高且无效）；run_log 与报告 §5.2 已写明
- [x] 残差复核：扫描 **525**、判 **30**（**5.71%**）、采纳 **12**（另跑全文抓取：11 FULL + 1 PARTIAL）；`verdicts.jsonl` 逐条 525 行（分母口径沿用「写满全行」）；rate 显著高于近批 1.5–2.8%，未达 12% 上报阈值，**未自行扩表**，缺口方向记入报告 §6.3
- [x] 全文：63 篇串行 3 s/篇 → **62 L0/FULL + 1 L1/PARTIAL**；字符 23,717–312,858。**O-12 守卫首次真实拦截**：2611.33313 的 ar5iv 返回摘要落地页（4,551 字符、含 "Skip to main content"）→ PARTIAL + TEC/EXP 下调至 2/2、value 2.23、C 级仅入馆
- [x] 前端重建 `verified: {papers:1332, notes:954, batches:83}`；11-27 卡 `表内=55`（A37/B13/C5）、backfill-1127 卡 `表内=8`（A7/B1），均非 0（`7dim-table.md` 保留 `arXiv` 列）；`BATCH_LABELS` 补 2 条中文标签
- [x] 前端冒烟 **PASS**：`papersEqDisk / notesEqDisk / batchesEqDisk` 全 true；5 标签渲染 4/2/2/3/1；排序 8 项单调性 + 隐藏开关（localStorage 落盘/复原）+ 弹层三组交互；`nCards=83`；lastThree 首卡 2026-11-27；`PAGE_ERRORS: none`（内联脚本另做 `node --check` 通过）
- [x] 总索引刷新：状态注记追加 11-27、速查入口换「最新一期 MOC-2026-11-27 / 上一期 11-26 / 笔记 954 篇」、批次表加 2 行、页尾加 2 个明细段、页首换 1,332（1,370 → 1,406 行）；自检「新增 2 行 ↔ 新增 2 段」通过（历史遗留 2 处不匹配仍为 2026-10-07 缺行与 backfill-2603-2609 异名，已白名单）
- [x] 交付前抽查 `title == id` / `len(title)<12`：新增 63 行 0 命中；新增档位 0 S / 44 A / 14 B / 5 C，与 gates/scored 一致
- [x] 渠道② 已实推并核验：本地 commit **`4d5fa2e`** → 增量推送（**127** 变更 / 2,456 未变 / 删除 0）→ 远端 main **`3d8cec6c`** → deploy run **`45882725875` success**；线上 **HTTP 200 / 4,840,812 字符**、含 `const DATA`、含 `2026-11-27`，与本地**逐字节相等**
- [x] 渠道① 不可用：本会话 ToolSearch **无** `workbuddy_sites_deploy` → 报告与 run_log 写「渠道①不可用（累计第 **38** 批挂账）」（渠道① 实测部分见 §附录，未声称已发布）


**2026-11-26（上一批，留档：11-25 周三公告批次，单日组、无周末积压；重磅日）**

- [x] `python scripts/check_release.py` → **PASS**（G1 **1269/896/81** ｜ G2 `gates_1126.json` 无缺、险过四字段齐 ｜ G3 本批授予S=True、backfill 记S=0、泄漏 0 ｜ R 残差 **1.5%**）
- [x] 对账 `audit_listing_1126.py` **7/7 分类 exit 0**：11-25 组 **761 槽位 / 624 唯一**（CV 302/GR 11/HC 21/MM 7/RO 111/AI 300/IV 9）；11-26 组 `declared=None`（未释放）；11-24 组复采逐分类 declared=got（494/13/61/18/191/485/23 = 1,285 槽位）→ **无新增漏跑窗口**
- [x] 上一组复采核验（新增 `scripts/missed_xr_1126.py`）：11-24 组未入馆 **977 = 1,045 − 68**，摘要覆盖 **977/977 = 1.0000**、缺摘要 0；摘要/标题级命中 **84 篇全部**落在上批处置集合（scored 74 / pool 146 / nonxr 899 / old_replace 35 四集合的并集覆盖）→ **0 漏网**（`leak_n=0`）
- [x] `data/gates_1126.json` 四字段齐全且布尔自洽（`today_max=4.57`、`heavy_day_raw=true`、`heavy_day=true`、`margin=+0.138`、`blockbuster=true`、`s_awarded=true`、`verdict=blockbuster_heavy_day`）+ `window_excludes_today/this_run_batches` 留痕 + `window_lo/hi = 2026-10-27 / 2026-11-26`、`in_window=580`
- [x] 残差复核：扫描 **527**、判 **8**（**1.52%**）、采纳 **8**；`verdicts.jsonl` 逐条 527 行（分母口径沿用「写满全行」才得 1.52%）；另通读补入 3 篇（2611.31757 / 2611.32034 / 2611.32396，未被自动 flagged，已在 gates 的 `recall.note` 与报告 §5.3 显式写明）
- [x] 全文：63 篇串行 3 s/篇 → **63 L0/FULL、无 PARTIAL**；字符 24,073–242,491。**O-12 守卫已入库**（`grade_evidence()` + `LANDING_RE`），本批未触发即生效
- [x] 前端重建 `verified: {papers:1269, notes:896, batches:81}`；11-26 卡 `表内=55`（S3/A18/B28/C6）、backfill-1126 卡 `表内=8`（A6/B1/C1），均非 0（`7dim-table.md` 保留 `arXiv` 列）；`BATCH_LABELS` 补 2 条中文标签
- [x] 前端冒烟 **PASS**：`papersEqDisk / notesEqDisk / batchesEqDisk` 全 true；5 标签渲染 4/2/2/3/1；排序 8 项单调性 + 隐藏开关（localStorage 落盘/复原）+ 弹层三组交互；`nCards=81`；lastThree 首卡 2026-11-26；`PAGE_ERRORS: none`
- [x] 总索引刷新：状态注记追加 11-26、速查入口换「最新一期 MOC-2026-11-26 / 上一期 11-25 / 笔记 896 篇」、批次表加 2 行、页尾加 2 个明细段、页首换 1,269（1,334 → 1,370 行）；自检「新增 2 行 ↔ 新增 2 段」通过（历史遗留 2 处不匹配仍为 2026-10-07 缺行与 backfill-2603-2609 异名，已白名单）
- [x] 交付前抽查 `title == id` / `len(title)<12`：新增 63 行 0 命中；新增档位 S 3 / A 24 / B 29 / C 7，与 gates/scored 一致
- [x] 渠道② 已实推并核验：本地 commit **`3779e92`** → 增量推送（**112** 变更 / 2,349 未变 / 删除 0）→ 远端 main **`7c5829c0`** → deploy run **`45682436410`** 首跑 failure（`No artifacts named "github-pages"`）、`gh run rerun` 后 **success**；线上 **HTTP 200 / 7,018,738 bytes**、含 `const DATA`、LF 归一化 md5 **`b88af674cce7deaa335707dc52c85ea6`** 与本地**逐字节相等**；收尾文档提交 `184d2b10` 的部署曾因 Actions 侧 `Found 0 artifact(s)` 连续 3 次失败（见 O-13），平台恢复后最终提交 **`97867606`** 的 run **`45683331850` success**，线上复验仍 200 且 md5 一致
- [x] 渠道① 不可用：本会话 ToolSearch **无** `workbuddy_sites_deploy`，`xr-paper-hub.app.workbuddy.host` 仍 403 → 报告与 run_log 写「渠道①不可用（累计第 **37** 批挂账）」，**未声称已发布**


**2026-11-25（上一批，留档：11-24 周二公告批次，含 11-21/11-22 周末积压）**

- [x] `python scripts/check_release.py` → **PASS**（G1 **1206/840/79** ｜ G2 `gates_1125.json` 无缺、险过四字段齐 ｜ G3 本批授予S=False、backfill 记S=0、泄漏 0 ｜ R 残差 **2.5%**）；`--record` 已写入 `data/verdicts.jsonl`（共 **5** 批）
- [x] `python scripts/check_audit_guard.py` 无违规（**28 份**脚本：守卫 10 / 基线豁免 18 / 违规 0；本日新增 `audit_listing_1125.py` 自带 `ok_cats<7 → exit 2` 且在任何 `json.dump(...missed...)` 之前，并传入第三参数窗口下界 2026-11-23）
- [x] 对账 `audit_listing_1125.py` **7/7 分类 exit 0**：11-24 组 **1,285 槽位 / 1,045 唯一**（CV 494/GR 13/HC 61/MM 18/RO 191/AI 485/IV 23）；11-25 组 `declared=None`（未释放）；11-23 组复采逐分类 declared=got（506 槽位 / 404 唯一）；未入馆 363 篇摘要级 **363/363** 覆盖（0 篇缺摘要），命中 40 篇**全部**在上批处置集合 → **0 漏网**
- [x] `data/gates_1125.json` 四字段齐全且布尔自洽（`today_max=4.21`、`heavy_day_raw=false`、`margin=-0.222`、`blockbuster=false`、`s_awarded=false`）+ `window_excludes_today/this_run_batches` 与 `this_run_batches_excluded` 留痕 + `window_lo/hi = 2026-10-26 / 2026-11-25`、`in_window=514`
- [x] 残差复核：扫描 **899**、判 **22**（**2.45%**）、采纳 **6** → 主批 68；`verdicts.jsonl` 逐条 **899 行**（分母坑复现：先写满 899 行才得 2.45%，只写命中行会得 100%）
- [x] 全文：74 篇串行 3 s/篇 → **72 L0/FULL + 2 L1/PARTIAL**（2611.29647 / 2611.30012 为 ar5iv 摘要落地页，手动改判并同步 `.txt` 头）；字符 4,581–312,858。**守卫仍未落地，见 O-12**
- [x] 前端重建 `verified: {papers:1206, notes:840, batches:79}`；11-25 卡 `表内=68`（44A/22B/2C）、backfill-1125 卡 `表内=6`（2A/4B），均非 0（`7dim-table.md` 保留 `arXiv` 列）；`BATCH_LABELS` 补 2 条中文标签
- [x] 前端冒烟 **PASS**：papersEqDisk / notesEqDisk / batchesEqDisk 全 true；5 标签渲染 4/2/2/3/1；排序 8 项单调性 + 隐藏开关（localStorage 落盘/复原）+ 弹层三组交互；`nCards=79`；lastThree 首卡 2026-11-25；`PAGE_ERRORS: none`
- [x] 总索引刷新：状态注记追加 11-25、速查入口换「最新一期 MOC-2026-11-25 / 上一期 11-24 / 笔记 840 篇」、批次表加 2 行（2026-11-25、backfill-1125）、页尾加 2 个明细段、页首换 1,206（1,300 → 1,334 行）；自检「新增 2 行 ↔ 新增 2 段」通过（历史遗留 2 处不匹配为 2026-10-07 缺行与 backfill-2603-2609 行标签异名，已白名单）
- [x] 交付前抽查 `title == id` / `len(title)<12`：新增 74 行 **0 命中**；新增档位 0 S / 46 A / 26 B / 2 C，与 gates/scored 一致
- [x] 渠道② 已实推并核验：本地 commit **`80207fa`** → 增量推送（**140** 变更 / 2,214 未变 / 删除 0）→ 远端 main **`9c94e831`** → deploy run **`45468795909` success（31 s）**；线上 **HTTP 200 / 6,533,825 bytes**、含 `const DATA`、LF 归一化 md5 **`f5a589aa…`** 与本地**逐字节相等**
- [x] 渠道① 不可用：ToolSearch 无 `workbuddy_sites_deploy`，`xr-paper-hub.app.workbuddy.host` 根与 `/index.html` 均 **403 / 3,174 bytes** → 报告与 run_log 均写「渠道①不可用（累计第 **36** 批挂账）」，**未声称已发布**

**2026-11-24（上一批，留档）**

- [x] `python scripts/check_release.py` → **PASS**（G1 1132/768/77 ｜ G2 `gates_1124.json` 无缺、险过四字段齐 ｜ G3 本批授予S=False、backfill 记S=0、泄漏 0 ｜ R 残差 2.2%）；`--record` 已写入 `data/verdicts.jsonl`（共 4 批）
- [x] `python scripts/check_audit_guard.py` 无违规（**27 份**脚本：守卫 9 / 基线豁免 18 / 违规 0；本日新增 `audit_listing_1124.py` 自带 `ok_cats<7 → exit 2` 且在任何 `json.dump(...missed...)` 之前，并传入第三参数窗口下界 2026-11-20）
- [x] 对账 `audit_listing_1124.py` **7/7 分类 exit 0**：11-23 组 506 槽位 / 404 唯一；11-21、11-22 `declared=None / got=0`（周末 skipDays）；11-20 组复采逐分类 declared=got（605 槽位 / 508 唯一）；未入馆 471 篇摘要级 471/471 覆盖，命中 43 篇**全部**在上批处置集合 → 0 漏网
- [x] `data/gates_1124.json` 四字段齐全且布尔自洽（`today_max=4.27`、`heavy_day_raw=false`、`margin=-0.162`、`blockbuster=false`、`s_awarded=false`）+ `window_excludes_today/this_run_batches` 与 `this_run_batches_excluded` 留痕 + `window_lo/hi = 2026-10-25 / 2026-11-24`、`in_window=464`
- [x] 残差复核：扫描 **371**、判 **8**（**2.2%**）、采纳 **8** → 主批 41；`verdicts.jsonl` 逐条 **371 行**（首版仅 14 行致 rate 57.1% 的分母坑已写入 run_log 与报告 §5.3）
- [x] 前端重建 `verified: {papers:1132, notes:768, batches:77}`（5,808.8 KB）；11-24 卡 count=41（24A/17B）、backfill-1124 卡 count=9（7A/2B），两卡 `表内` 均非 0（`7dim-table.md` 保留 `arXiv` 列）
- [x] 前端冒烟 **PASS**：papersEqDisk / notesEqDisk / batchesEqDisk 全 true；5 标签渲染 4/2/2/3/1；7 档排序 + 隐藏开关（localStorage 落盘/复原）+ 弹层三组交互；nCards=77；lastThree 首卡 2026-11-24；PAGE_ERRORS none
- [x] 总索引刷新：状态注记追加 11-24、速查入口换「最新一期 MOC-2026-11-24 / 上一期 11-21」、批次表加 2 行（2026-11-24、backfill-1124）、页尾加 2 个明细段、页脚换 11-24（1,132 / 768 / 77）
- [x] 交付前抽查 `title == id` / `len(title)<12`：新增 50 行 **0 命中**；新增档位分布 0 S / 31 A / 19 B / 0 C，与 gates/scored 一致
- [x] 渠道② 已实推并核验：本地 commit **`f0774fa`** → 增量推送（101 变更 / 2119 未变 / 60.37 MB）→ 远端 main **`67868a4b`**（`pushedAt` 2026-11-23T18:59:25Z）→ deploy run **`45244161325` success**（18:59:54Z）；线上 **HTTP 200**、含 `const DATA`、md5 **`0705fad6…`** 与本地 LF 归一化版**逐字节相等**
- [x] 渠道① 不可用：ToolSearch 无 `workbuddy_sites_deploy` → 报告与 run_log 均写「渠道①不可用（累计第 **35** 批挂账）」，未声称已发布

**2026-11-23（上一批，留档）**

- [x] `python scripts/check_release.py` → **WARN / rc=0**（G1 1082/718/**75** PASS ｜ G2 `gates_1123.json` 无缺、四字段齐 PASS ｜ G3 本批授予S=False、泄漏 0 PASS ｜ R 残差「未执行」= 状态日无 `nonxr_1123`，如实登记未补造）
- [x] `python scripts/check_audit_guard.py` 无违规（**26 份**脚本：守卫 8 / 基线豁免 18 / 违规 0；本日新增 `audit_listing_1123.py` 自带 `ok_cats<7 → exit 2` 且在任何 `json.dump(...missed...)` 之前）
- [x] 对账 `audit_listing_1123.py` **7/7 分类 exit 0**、11-20 组逐分类 declared=got（605 槽位 / 508 唯一）；未入馆 471 篇摘要级 471/471 覆盖，命中 43 篇**全部**在上批处置集合 → 0 漏网
- [x] `data/gates_1123.json` 四字段齐全且布尔自洽（`today_max=null`、`heavy_day_raw=false`、`margin=null`、`blockbuster=false`、`s_awarded=false`）+ `window_excludes_*` 三项留痕
- [x] 残差复核：状态日不适用（无新增 nonxr），未生成 `residual_1123.json`；历史 rate 2.8% → 1.6% 连续低位
- [x] 前端重建 `verified: {papers:1082, notes:718, batches:75}`；11-23 卡片 count=0 + **refPapers=39**；两个 `<script>` 块 `node --check` 通过
- [x] 前端冒烟 PASS（磁盘不变量 + 5 标签渲染 + 7 档排序 / 隐藏开关 / 弹层三组交互，nCards=75，lastThree 首卡 2026-11-23，零页面异常）；**修正冒烟脚本冷启动竞态**（固定 sleep 2500ms → 就绪轮询 ≤30s，不改断言口径）
- [x] 总索引刷新：状态注记追加 11-23、速查入口换「最新运行状态=状态报告 2026-11-23」、批次表加 1 行、页脚换 11-23（库内 1,082 / 笔记 718 / daily 75）
- [x] 交付前抽查 `title == id` / `len(title)<12`：0 命中（未改 registry，无备份需要）
- [x] 本文件 §1/§4/§5 已按事实更新（O-1 → 34 批；§4 增 11-23 状态日 WARN 说明）
- [x] 渠道② 已实推并核验：本地 commit **`fcebc54`** → 增量推送 **23 blob** → 远端 main **`9be55d2c`**（`pushedAt` 2026-11-22T18:40:36Z）→ deploy run **`45056432539` success**；线上 **5,643,592 bytes**，Range 5×1MB 重组后与本地 LF 归一化版 **md5 `36ed272a…` 完全一致（byte-equal=True）**，DATA 1082/718/75、11-23 卡片 count=0 / refPapers=39 与本地逐项一致
- [x] 渠道① 不可用：ToolSearch 无 `workbuddy_sites_deploy`，`xr-paper-hub.app.workbuddy.host` 根与子路径均 **403 / 3,174 bytes** → 报告与 run_log 均写「渠道①不可用（累计第 **34** 批挂账）」，未声称已发布

**2026-11-22（上一批，留档）**

- [x] `python scripts/check_release.py` → **WARN / rc=0**（G1 1082/718/**74** PASS ｜ G2 `gates_1122.json` 无缺、险过四字段齐 PASS ｜ G3 本批授予S=False、泄漏 0 PASS ｜ R 残差「未执行」= 状态日无 `nonxr_1122`，如实登记未补造）
- [x] `python scripts/check_audit_guard.py` 无违规（**25 份**脚本：守卫 7 / 基线豁免 18 / 违规 0；本日新增 `audit_listing_1122.py` 自带 `ok_cats<7 → exit 2` 且在任何 `json.dump(...missed...)` 之前）
- [x] 对账 `audit_listing_1122.py` **7/7 分类 exit 0**、11-20 组逐分类 declared=got（605 槽位 / 508 唯一）；未入馆 471 篇摘要级 471/471 覆盖，命中 43 篇**全部**在上批处置集合 → 0 漏网
- [x] `data/gates_1122.json` 四字段齐全且布尔自洽（`today_max=null`、`heavy_day_raw=false`、`margin=null`、`blockbuster=false`、`s_awarded=false`）+ `window_excludes_*` 三项留痕
- [x] 残差复核：状态日不适用（无新增 nonxr），未生成 `residual_1122.json`；历史 rate 2.8% → 1.6% 连续低位
- [x] 前端重建 `verified: {papers:1082, notes:718, batches:74}`；11-22 卡片 count=0 + **refPapers=39**；两个 `<script>` 块 `node --check` 通过
- [x] 前端冒烟 PASS（磁盘不变量 + 4 标签渲染 + 7 档排序 / 隐藏开关 / 弹层三组交互，nCards=74，lastThree 首卡 2026-11-22，零页面异常）
- [x] 总索引刷新：状态注记追加 11-22、速查入口换「最新运行状态=状态报告 2026-11-22」、批次表加 1 行、头部批次清单追加、页脚换 11-22（库内 1,082 / 笔记 718 / MOC 61）
- [x] 交付前抽查 `title == id` / `len(title)<12`：0 命中（未改 registry，无备份需要）
- [x] 本文件 §1/§4/§5 已按事实更新（O-1 → 33 批；§4 增 11-22 状态日 WARN 说明）
- [x] 渠道② 已实推并核验：本地 commit `13528da` → 远端 main **`17b296a1`**（增量 20 文件）→ deploy run `44936806929` 首次失败（`Fetching artifact metadata failed`，github#16/#17 已知间歇故障）→ **重跑 success**；线上 **HTTP 200 / 5,628,313 bytes**，Range 5×1MB 重组后与本地 LF 归一化版 **md5 `05eacac8…` 完全一致（byte-equal=True）**，线上 DATA 1082/718/74 与 11-22 卡片逐项一致
- [x] 渠道① 不可用：ToolsSearch 无 `workbuddy_sites_deploy`，`xr-paper-hub.app.workbuddy.host` 根与子路径均 **403 / 3,174 bytes** → 报告与 run_log 均写「渠道①不可用（累计第 **33** 批挂账）」，未声称已发布

**2026-11-21（上一批，留档）**

- [x] `python scripts/check_release.py` 全 PASS（G1 1082/718/73 ｜ G2 `gates_1121.json` 无缺、险过四字段齐 ｜ G3 本批授予S=False、泄漏 0 ｜ R 残差 1.6%）
- [x] `python scripts/check_release.py --record` 已把本批判决写入 `data/verdicts.jsonl`（`2026-11-21` PASS，residual_rate 0.0162）
- [x] `data/residual_1121.json` 已生成（431 扫描 / 7 判 / 1.6%），报告含「残差复核」一行（6 处）
- [x] 前端重建 `verified: {papers:1082, notes:718, batches:73}`；冒烟 PASS（nCards=73）
- [x] 渠道② commit `82a2222` → main `4fd76fe8` → deploy `44798357045` success；渠道① 32 批挂账
