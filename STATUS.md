# STATUS.md — 运行状态与未完成事项

> **每轮更新规则（写死，勿删）**
> 1. 每次每日运行或整改批次结束后更新本文件：顶部时间、§1 增删、§4 判决状态、§5 自检结果。
> 2. 只在**事实变化**时改动；不要为了"看起来在维护"而刷新时间戳。
> 3. 每条必须四要素：现象 / 影响 / 当前处置 / 触发条件或责任。
> 4. 关闭的事项从 §1 移入 §2，保留编号，不删除（可追溯）。

- **最后更新**：2026-11-19（人工批次：残差复核上线、q2 口径、发布门）
- **当前库况**：registry 1015 / notes 655 / daily 69 ｜ 最新批次 2026-11-19（21 篇，12A/7B/2C，无 S）
- **回滚点**：`v1.0-20261118`（本地 + 远端）

## 1. 未完成事项（Open）

| ID | 现象 | 影响 | 当前处置 | 触发条件 / 责任 |
|---|---|---|---|---|
| O-1 | 渠道① `xr-paper-hub.app.workbuddy.host` 返回 403（3174 bytes） | 双渠道变单渠道 | 不修；报告如实写「渠道①不可用（第 N 批挂账）」，禁止声称已发布 | 托管侧重签后可恢复；累计 **29 批** |
| O-2 | registry 内 65 行赛道非规范（63 行「—（非 XR）」+ `具身交互` 1 + `空间计算` 1） | 统计口径轻微失真 | **WONTFIX**：前端有 `#8a93a8` 兜底配色，改数据需动 65 行并重建前端 | 若将来做赛道重分类时一并处理 |
| O-4 | `audit_gap_listing.py` 未并入「目标组 >500 条补页」逻辑 | 极端大日组可能少采 | **WONTFIX**（随 R-03 抽库一并放弃）；每日实例以 `audit_listing_1117.py` 为模板，含补采 | 若某日目标组 >500 且 declared≠got 时报错（守卫会 exit 2） |
| O-5 | `send_automation_result` 在部分会话不可见 | 收尾汇报可能失败 | 观察项：不可见时改用 present_files + 报告正文 | 连续 2 次不可见则改指令 |
| O-6 | 残差复核（第 3.5 步）**尚未被真实运行验证** | 指令写了但可能被跳步 | 2026-11-20 02:30 首次执行；核查 `data/residual_1119.json` 是否生成 | 若未生成 → 把 3.5 并入第 3 步正文 |
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

- **判决记账**：`python scripts/check_release.py --record` 会把本批判决写入 `data/verdicts.jsonl`
  （按批次日幂等：`{batch, verdict, counts, gate3, residual_rate, reasons, at}`）。
  三档语义：`PASS` 全绿；`WARN` 有诊断性问题但不阻塞（如残差复核未执行、漏检率 >12%）；
  `FAIL` 硬门不过（计数不一致 / 留痕缺失 / 档位泄漏），**不得发布**。

## 5. 每轮自检清单（收尾前逐条打勾）

- [ ] `python scripts/check_release.py` 全 PASS
- [ ] `python scripts/check_release.py --record` 已把本批判决写入 `data/verdicts.jsonl`（VERDICT 行与台账一致）
- [ ] `python scripts/check_audit_guard.py` 无违规
- [ ] `data/residual_<MMDD>.json` 已生成，报告含「残差复核」一行
- [ ] `data/gates_<MMDD>.json` 四字段齐全且 `s_awarded` 为布尔
- [ ] 前端冒烟 PASS（含 UI 三组交互断言），线上 md5 与本地一致
- [ ] 本文件 §1/§4 已按事实更新
