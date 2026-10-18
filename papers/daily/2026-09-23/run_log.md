# 运行日志 · 2026-09-23（XR 每日论文雷达）

- **状态**：成功（含 3 处脚本缺陷修复）。
- **时间**：03:00 触发；03:xx 完成拉取→评分→全文→笔记→报告。
- **环境**：沙箱 C: 盘曾满（0 字节）→ 清理 Temp 释放 1.66GB 后恢复。

## 1. 拉取（Step1）
- 命令：`fetch_arxiv.py --since 2026-09-17 --max 600`（library 前沿 09-17，本次新命中 09-18~09-21）。
- **修复 A（关键）**：`fetch_arxiv.py` 的 `parse_entry` 旧实现把 `<entry>` 片段当独立 XML 解析 → 触发 `unbound prefix` ParseError，导致**全部条目解析为 None、拉取 0 条**。改为**整份 `<feed>` 解析后 `findall("atom:entry")` 迭代**，并修正 `or` 链式赋值（元素 falsy 陷阱）。
- **修复 B（关键）**：首次运行因 `while` 分页**未越过日期边界即停止**，导致对 arXiv 全历史页持续扫描（checkpoint 到 7600 仍 0 条）。新增：一旦遇到 `< min_date` 的条目即 `break`（submittedDate 降序保证后续更旧）。
- 结果：75 条原始（09-17×31 / 09-18×13 / 09-19×9 / 09-20×9 / 09-21×13）；去重 registry 后 **50 条新**。

## 2. 分类与评分（Step2–4）
- XR 相关 **34** 篇，非 XR **13** 篇（防御无人机/水下 SLAM/RF 定位/驾驶/BEV/CFD/阀门/点云等留存不计入）。
- 7 维固定权重打分；按价值降序取 Top10（≥3.6）。

## 3. 全文抓取（Step6）
- 候选 18 篇（`--ids`）先抓全文**再定稿评分**（遵循 §8.6.2）。
- **修复 C（关键）**：`fetch_fulltext.py` 仅 `import urllib.error` 但未导入 `HTTPError`/`URLError` 裸名，其 `except` 子句触发 `NameError` → 任何网络异常都落入 L5 摘要降级（首跑 18 篇全 L5）。补 `from urllib.error import HTTPError, URLError` 后，18 篇**全部 L0 FULL**（406 内容协商重试 5 次后由 v1/无版本 URL 命中）。
- 证据等级：Top10 **全 FULL**（L0），无限流/降级。

## 4. 覆盖率校验（Step5）
- ① 同质去重：09-18~09-21 新窗口 vs 库内 09-15~09-17 天然无重叠 → 通过。
- ② 赛道覆盖：Top10 覆盖 **6** 赛道 ≥5 → 通过。
- ③ 价值天花板：当日最高 **4.12** < 库内近 30 天 Top10 均分 **4.296** → **非重磅日**，未拔高评分。
- 落后/被取代登记：**0 条**（新作，无同问题更优者）。

## 5. 产物
- 报告：`reports/XR-Daily-Report-2026-09-23.md`（执行摘要 + Top10 排行 + 10 章精读 + 全量 7 维参考 + 覆盖校验 + 附录）。
- 原子笔记：10 篇（`papers/notes/2609.*.md`）。
- MOC：当日 `papers/MOC/MOC-2026-09-23.md` + 总索引更新（112 篇、30 笔记）。
- 7 维表：`papers/daily/2026-09-23/7dim-table.md`、`scored.md`。
- 文献库：`registry.jsonl` 65 → **112** 篇（幂等追加 47）。

## 6. Top10 名单（按重要性）
1. Adaptive World Memory 3D 基础模型（4.12）· 世界模型
2. Cube-Splat 全景 GS-SLAM（4.05）· 重建与SLAM
3. BayesianGS-SLAM 不确定度感知（4.05）· 重建与SLAM
4. AVTR-1 实时交互式化身栈（4.00）· 化身与人体
5. OpenFlyScan 质量引导航拍重建（3.95）· 重建与SLAM
6. CRP-GS 跨表示 3DGS 压缩（3.95）· 系统与平台
7. VoxelTTO 体素对齐前馈 3DGS（3.85）· 神经渲染
8. 4DGS-Fixer 扩散引导 4DGS（3.85）· 神经渲染
9. Relightable 3D Avatar 可重光照化身（3.85）· 化身与人体
10. Passthrough Rigidity 穿透显示代价（3.85）· 空间计算与UI
