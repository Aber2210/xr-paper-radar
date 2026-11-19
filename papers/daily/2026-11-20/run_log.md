# run_log · 2026-11-20（11-19 公告批次）

## 1. 对账（先于拉取）
- `scripts/audit_listing_1120.py`（PREV_DAY=2026-11-18，NEW_DAYS=[2026-11-19, 2026-11-20]）
- 7/7 分类 newest=2026-11-19，prev 组 declared=got 全 OK，11-20 组未释放（运行时刻 02:30 早于 UTC 00:00 公告时刻后的索引刷新）
- 11-18 组复采 599 槽位 / 496 唯一；未入馆 475 篇摘要覆盖率 475/475；命中 37 篇全在 `xr_pool_1119.json` → 0 漏网
- `check_audit_guard.py`：PASS（23 份脚本，守卫 5 / 基线豁免 18 / 违规 0）

## 2. 数据源
- API 探针 export/www 均 200
- RSS 7/7 分类，753 条全量；KW 命中 78
- listing show=500 单页足够，无补页

## 3. 甄别与残差
- 502/502 摘要覆盖（缺收 0）→ 免 id_list
- KW 52 + 标题补扫 16 = 68 → 剔 43 → 22；残差采纳 3 → 25
- 残差扫描 434，判 12（2.8%），采纳 3；9 条留池
- replace 旧稿 19 篇 XR 命中中选 3 篇 backfill

## 4. 全文
- 25 篇首批 + 3 篇残差采纳 = 28 篇，串行 3 s
- 26 篇 L0/FULL；2611.24193 L0/PARTIAL（HTML 缺正文）；2606.07179 L1/FULL（ar5iv 补）
- 0 失败，0 ABSTRACT_ONLY

## 5. 评分与三关
- 7 维按标准权重重算（子代理 scores_hint 仅作参考）
- 校准改动：24938 IMP5→4/PER4→3；23670 PER4→3；23871 TRL4→3；24805 TRL5→4；2606.07179 PER4→3；24193 TEC3→2/EXP4→2/PER5→4
- 门① 0.072 / 门② 7 赛道 / 门③ 4.33 vs 4.4230（457 入窗）→ 非重磅日无 S
- 档位统计：{'A': 20, 'B': 5, 'C': 3}

## 6. 产物
- 报告 1 + 笔记 25 + daily 目录（7dim-table/scored/run_log）+ MOC 2 + 总索引刷新
- registry 1015 → 1043（备份 registry.jsonl.bak-20261120）

## 7. 失败与降级
- 无抓取失败；2611.24193 证据降级 PARTIAL 并显式声明
- smoke/CDP 与发布结果见第 8 节（发布阶段追加）

## 8. 发布与自检
- `check_release.py` **PASS**：G1 1043/680/71 三计数一致 ｜ G2 `gates_1120.json` 字段齐 ｜ G3 本批授予S=False、backfill 记S=0、泄漏 0 ｜ R 残差 2.8%
- `check_release.py --record` 已记账 → `data/verdicts.jsonl`（`2026-11-20` PASS，`residual_rate=0.0276`）
- `check_audit_guard.py` PASS（23 份脚本：守卫 5 / 基线豁免 18 / 违规 0）
- `node --check`：抽取 2 个 `<script>` 块（3,315,277 + 33,328 字符）语法通过
- `smoke_hub.mjs`（Edge headless CDP）**PASS**：papers/notes/batches 与磁盘一致、末三批在列、全部有标题、4 个 tab 渲染、0 页面错误、7 档排序单调、隐藏开关落盘可复原、信息弹层开合正常
- 渠道② GitHub Pages：`git add -A && git commit`（54a4118）→ `push_to_github.py --incremental`（85 变更 / 0 删除 / 1914 未变）→ 远端 `be9027a5`，tree `2a5d45be` 与本地 `HEAD^{tree}` **完全一致** → `deploy-pages.yml` run 44595847237 **success**
- 线上核验：`https://aber2210.github.io/xr-paper-radar/` HTTP **200**，含 `const DATA`，计数 **1043 / 680 / 71**；`2026-11-20` 卡 count=25（A18/B4/C3，max 4.33）、`backfill-1120` 卡 count=3（A2/B1）
- md5 说明：本地 `096f3852…`（5,198,955 B，CRLF 730 行）与线上 `5e6dfe72…`（5,198,225 B）差异仅行尾——**CRLF→LF 归一化后逐字节一致**（已验证 `norm == live`），非内容差异
- 渠道① WorkBuddy 托管：`workbuddy_sites_deploy` 不在工具集，**不可用**，按「累计第 31 批挂账」如实记录，未声称已发布
- **部署故障（诚实记录）**：补文档的第二次提交 `b59ad6c`（远端 `f393b6ef`）触发的 deploy run `44596069182` 两次（含 `--failed` 重跑）与 `workflow_dispatch` 的 `44596257214`，均以 GitHub Actions **artifact 元数据接口**报错失败（`Fetching artifact metadata failed … .github#16`），属平台侧故障而非构建问题。该提交**未改动 `web/xr-paper-hub.html`**，线上仍是 `44595847237` 成功部署的构建；第 4 次（提交 `fe068d8` → run **44596446508**）**已恢复 success**，线上复核 HTTP 200 / `5e6dfe72…` / 1043/680/71 稳定不变
