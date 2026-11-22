# STATUS.md — 运行状态与未完成事项

> **每轮更新规则（写死，勿删）**
> 1. 每次每日运行或整改批次结束后更新本文件：顶部时间、§1 增删、§4 判决状态、§5 自检结果。
> 2. 只在**事实变化**时改动；不要为了"看起来在维护"而刷新时间戳。
> 3. 每条必须四要素：现象 / 影响 / 当前处置 / 触发条件或责任。
> 4. 关闭的事项从 §1 移入 §2，保留编号，不删除（可追溯）。

- **最后更新**：2026-11-23（每日批次：**周一凌晨状态日 0 新稿**；11-20 公告组复核 0 漏网；registry 维持 1,082）
- **当前库况**：registry 1082 / notes 718 / daily 75 ｜ 最新真实批次 2026-11-21（37 篇，23A/13B/1C，无 S，门③ 险过 +0.007）｜ 11-23 状态日卡片 count=0 / refPapers=39 ｜ 门③ 现算基线 **4.432**（窗口 [2026-10-24, 2026-11-23)，464 条入窗）
- **回滚点**：`v1.0-20261118`（本地 + 远端）

## 1. 未完成事项（Open）

| ID | 现象 | 影响 | 当前处置 | 触发条件 / 责任 |
|---|---|---|---|---|
| O-1 | 渠道① `xr-paper-hub.app.workbuddy.host` 返回 403（3174 bytes） | 双渠道变单渠道 | 不修；报告如实写「渠道①不可用（第 N 批挂账）」，禁止声称已发布 | 托管侧重签后可恢复；累计 **34 批**（2026-10-21 ~ 11-23） |
| O-2 | registry 内 65 行赛道非规范（63 行「—（非 XR）」+ `具身交互` 1 + `空间计算` 1） | 统计口径轻微失真 | **WONTFIX**：前端有 `#8a93a8` 兜底配色，改数据需动 65 行并重建前端 | 若将来做赛道重分类时一并处理 |
| O-4 | `audit_gap_listing.py` 未并入「目标组 >500 条补页」逻辑 | 极端大日组可能少采 | **WONTFIX**（随 R-03 抽库一并放弃）；每日实例以 `audit_listing_1117.py` 为模板，含补采 | 若某日目标组 >500 且 declared≠got 时报错（守卫会 exit 2） |
| O-5 | `send_automation_result` 在部分会话不可见 | 收尾汇报可能失败 | 观察项：不可见时改用 present_files + 报告正文 | 连续 2 次不可见则改指令 |
| O-7 | 11-18 / 11-19 两批未做残差复核（脚本 11-19 才上线） | 历史漏检未知 | 不回补；从 11-20 批起记录 rate | — |
| O-8 | golden 仅 25/100 kw-missed + 20/20 accepted 有人工标签 | 精确率/召回基于小样本（n=40） | 已记 CI；如需收窄 ±2pp 需再标约 400 条 | 用户决定是否扩大标注 |
| O-9 | 历史 `data/gates_*.json`（≤1117）缺 `window_excludes_*` 留痕字段 | 事后无法自证当时口径 | **grandfather 不回算**（与门③ 历史值政策一致） | 仅新批必须齐四字段 |
| O-10 | `update_moc_<MMDD>.py` 等一次性锚点脚本，重跑即 `ANCHOR NOT FOUND` | 无法幂等重跑 | 已知限制，不修；重跑前用 `git show <批次前commit>` 还原 MOC | 需要重跑时按此办法 |
| O-11 | Jev API 返回 **451**（法律原因不可用）；AnyJev 需本地 LLM，本机无 GPU | 决策模型路线受阻 | 搁置；已用现有模型做盲评基线（7/7 精确） | 若区域放开或有 GPU 再评估 |

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
- **最近一批**：`2026-11-21` 判 **PASS**（G1 1082/718/73 三计数一致；G2 `gates_1121.json` 字段齐、险过四字段在；G3 无 S 泄漏；残差 rate 1.6%；门③ 4.43 vs 4.4230 → margin +0.007、险过无 S）——见 `data/verdicts.jsonl`。上一批 `2026-11-20` 判 PASS（残差 rate 2.8%）。
- **2026-11-22（周日状态日）**：`check_release.py` → **WARN**（G1 1082/718/**74** PASS、G2 `gates_1122.json` 字段齐 PASS、G3 无泄漏 PASS；R 项因状态日未生成 `residual_1122.json` 报「未执行」）。**WARN 不阻塞发布**，如实登记而非补造残差文件；未 `--record`（状态日无批次，沿用 11-13/11-16 状态日不记账惯例）。
- **2026-11-23（周一凌晨状态日）**：`check_release.py` → **WARN**（G1 1082/718/**75** PASS、G2 `gates_1123.json` 字段齐 PASS、G3 无泄漏 PASS；R 项「未执行」= 状态日无 `nonxr_1123`，**未补造**）。四源一致：listing 7/7 最新公告日 11-20、缓存穿透与跨学科复验一致、API 前沿 11-19 + 三日区间各 0 篇、RSS `WROTE=0 OK_CATS=7/7`。**下一批（11-24 周二 02:30）才处理周末 11-21/11-22 提交积压**。

- **读数修正（2026-11-21）**：残差漏检率 **1.6%（7/431，95% CI 约 0.7%–3.3%）**，与 11-20 的 2.8%（12/434）同处低位，连续两批远低于 12% 上报阈值。三批实测（2.8% / 1.6%）均显著低于早期 100 条抽样给出的 7.0%，**抽样值只作上界**。

- **读数修正（2026-11-20）**：残差漏检率首跑实测 **2.8%（12/434，95% CI 约 1.6%–4.8%）**，
  是此前 100 条抽样的 7.0%（折算 25–102 篇/批）的 1/2.5。**全量扫描优于抽样，后续引用以实测为准**，
  7% 仅作上界参考。按 2.8% 折算：约 **12 篇/批**被判应收录，本批采纳 3 篇入馆。
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

**2026-11-23（周一凌晨状态日）**

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
- [x] 渠道② 已实推并核验（见下方发布记录）
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
