# XR 每日论文雷达 · 论文解读知识库

> AR / VR / MR / XR 方向每日论文自动追踪 → 7 维度评分 → Top10 全文精读 → 原子化笔记 + MOC 索引的知识库，以及一个自包含的前端归纳整理页。

## 这是什么

一个每日自动运行的论文雷达：从 arXiv（RSS + API 双通道）拉取 7 个分类（cs.CV / cs.GR / cs.HC / cs.MM / cs.RO / cs.AI / eess.IV）的最新论文，按 XR 关键词与人工判读甄别，用固定的 7 维度体系评分，选出前十做全文精读，沉淀为「原子笔记 + MOC 索引」形式的知识库，并汇总成一个可检索、可筛选、可排序的单页应用。

## 在线访问

| 渠道 | 链接 |
|---|---|
| 前端归纳整理页（WorkBuddy 托管，每日自动更新） | https://xr-paper-hub.app.workbuddy.host/ |
| 前端归纳整理页（GitHub Pages，每日 06:00 同步） | https://aber2210.github.io/xr-paper-radar/ |

两个渠道内容一致，均为 `web/xr-paper-hub.html` 这一个**自包含单文件**（无外部依赖，双击即可打开）。
GitHub Pages 由 `.github/workflows/deploy-pages.yml` 自动部署：仓库内已提交该文件则直接使用，否则在构建时从 WorkBuddy 托管链接拉取最新版本（双模式，保证两渠道同源）。

## 目录结构

```
web/xr-paper-hub.html      前端归纳页（自包含单文件，约 1.1 MB）
papers/
  library/registry.jsonl   文献库总账（每篇一行：7 维评分/档位/证据等级/批次）
  notes/                   原子笔记（每篇一篇：结论/方法/实验/创新/局限）
  MOC/                     每日 MOC + 总索引（状态注记/排行榜/赛道分布）
  daily/<日期>/            每日 7 维对比表、评分明细、运行日志
reports/                   每日解读报告与 backfill 报告（每篇一章）
scripts/                   全流程脚本（拉取/评分/产物/前端构建/漏网对账）
data/                      中间数据（RSS 落盘、评分 JSON、漏网审计产物）
```

## 7 维度评分体系（固定权重保证跨日可比）

| 维度 | 含义 | 权重 |
|---|---|---|
| IMP | 问题重要性 | 0.20 |
| NOV | 方法创新性 | 0.20 |
| TEC | 技术完整度 | 0.15 |
| EXP | 实验强度 | 0.15 |
| PER | 性能增益 | 0.15 |
| TRL | 落地成熟度 | 0.08 |
| REP | 可复现与影响力 | 0.07 |

档位：S ≥ 4.20 · A 3.60–4.20 · B 3.00–3.60 · C < 3.00。

每次运行还执行覆盖度三关（防同质、保赛道覆盖、防评分拔高）：① 与文献库最大标题 Jaccard < 0.62；② Top10 覆盖 ≥ 5 赛道；③ 当日最高分对比库内近 30 天 Top10 均分（非重磅日不拔高、不虚构 S 级）。

## 证据等级口径

- `FULL`：已抓取全文（arxiv.org/html，L0），评分经全文复核；
- `PARTIAL`：正文不完整（ar5iv 降级），按摘要级评估并显式标注；
- `ABSTRACT_ONLY`：仅摘要评分，registry 如实标注。

## 自动化

每日定时运行（WorkBuddy 自动化任务驱动）：拉取 → 甄别 → 评分 → 三关 → Top10 全文精读 → 笔记/报告/MOC/registry → **重建前端 → 发布更新**。中断或漏跑的公告日由「漏网对账」机制（arXiv listing 页按公告日对账 registry）兜底补录。

## 本地重建前端

```bash
python scripts/build_frontend.py   # 从 registry/notes/daily 表重新生成 web/xr-paper-hub.html
```

## 诚实口径

- 报告显式区分「公告日」与「拉取日」；积压窗口如实标注，不伪装当日新论文。
- 评分不虚构：低量日不凑数，非重磅日无 S 级；方法路线落后者在索引与章节处标 ⚠️。
- backfill 批次（历史漏网/旧稿补录）单独编号，不与当日新稿混淆。
