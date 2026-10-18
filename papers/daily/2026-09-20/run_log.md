# 执行日志 · 2026-09-20

## 1. 拉取阶段

| 项 | 结果 |
|---|---|
| 数据源 | arXiv API `export.arxiv.org/api/query` |
| 分类过滤 | cs.GR / cs.HC / cs.CV / cs.MM / cs.RO / cs.AI / eess.IV |
| 关键词过滤 | 24 个（virtual reality、Gaussian splatting、SLAM、haptic、near-eye、light field、passthrough 等） |
| 排序 | `sortBy=submittedDate&sortOrder=descending` |
| 请求页数 | 3 页 × 100 |
| 时间过滤 | 近 3 天（实际命中 09-16 ~ 09-17） |
| **入库条数** | **38** |
| 限流/退避 | 0 次触发（每请求间隔 3 s） |
| 失败 | 0 |

**说明**：当日为周日（2026-09-20），arXiv 无新提交。按 skill §2.2 规则回溯 3 天，实际最新提交日期为 2026-09-17。报告中"当日"即指该批次。

## 2. 全文抓取阶段

| 项 | 结果 |
|---|---|
| 抓取篇数 | 11（10 篇入选 + TouchSight 备选） |
| 降级链触发 | **全部 L0 一次成功**，未触发 L1–L5 |
| 证据等级 | 11 篇全部 `FULL` |
| 字符数范围 | 42,829 – 100,552 |
| 限流/403/超时 | 0 |
| 失败 | 0 |

### 抓取过程中修复的两个脚本缺陷

1. **`fetch_arxiv.py` 命名空间传参错误**：`e.find("arxiv:primary_category", NS["arxiv"])` 把命名空间 URI 字符串当成了 namespaces 字典，抛 `AttributeError: 'str' object has no attribute 'items'`。改为传 `NS` 字典后解决。
2. **`fetch_fulltext.py` 版本号提取越界**：`bid.split("v")[1]` 在 base_id 不含版本号时抛 `IndexError`。改为从 `arxiv_id` 提取：`aid.split("v")[1] if "v" in aid else None`。

### 一个需要留意的陷阱

`fetch_fulltext.py` 每次运行会**覆盖** `_manifest.json`。本次因追加抓取单篇导致 manifest 只剩 1 条，随后从 `data/fulltext/*.txt` 的文件头（`# LEVEL:` / `# EVIDENCE:`）重建。**后续使用时：要么一次抓完，要么改为追加合并。**

## 3. 章节解析

- 首轮 `digest.py` 对 3 篇（2609.20330 / 2609.19315 / 2609.20414）只解析出 1 段。
- 原因：这三篇的章节编号为**罗马数字**（`I Introduction`、`IV Method`），而正则只接受阿拉伯数字前缀。
- 修正：前缀改为 `(?:[IVXLC]+|\d+(?:\.\d+)*|[A-Z])\.?\s+`，三篇均正常解析出 6 段。

## 4. 评分与筛选

- 38 篇全部完成 7 维打分（见 `7dim-table.md`）。
- 分数区间：2.15 – 4.65；S 级 5 篇、A 级 11 篇、B 级 14 篇、C 级 8 篇。

## 5. 覆盖度校验（三关）

| 关卡 | 判据 | 结果 |
|---|---|---|
| ① 相似度去同质 | 与近 90 天库内条目 Jaccard > 0.62 | **首日运行，文献库为空 → 无历史条目可比**。本次建立 38 篇基线，次日生效。 |
| ② 赛道覆盖 | Top10 覆盖 ≥5 个赛道 | 纯分数 Top10 覆盖 5 个赛道，但 **XR 核心赛道「触觉与多模态」缺席** → 触发回补 |
| ③ 价值天花板 | 当日最高分 vs 库内近 30 天 Top10 均分 | 首日无历史基准，跳过；当日最高 4.65 ≥ 4.2，S 级成立 |

### 触发的重新筛选（1 次）

| 动作 | 论文 | 理由 |
|---|---|---|
| **剔除** | `arXiv:2609.19142` PointZero（4.02） | 「世界模型与仿真」赛道第 3 篇（同赛道已有 Astronex-World、GAVEL）；XR 迁移路径最弱（纯机器人操作动力学，无 XR 评测） |
| **回补** | `arXiv:2609.20649` DexTouch-WM（4.00） | 「触觉与多模态」赛道纯分数最高者；触觉是 XR 核心赛道，不可整体缺席 |

回补后：Top10 覆盖 **7 个赛道**，XR 核心赛道占 3 席 + 系统与平台 1 席。

### 未入选但值得回溯的次优候选

| 论文 | 分值 | 赛道 | 备注 |
|---|---|---|---|
| `arXiv:2609.20719` VR 老龄化×交互模态 | 3.93 | 感知与认知 | N=202 大样本用户实验，XR 可及性 |
| `arXiv:2609.20414` TouchSight 裸手触觉 | 3.85 | 触觉与多模态 | 全文已抓（L0/FULL）；**零仪器**路线，与 DexTouch-WM 互补 |
| `arXiv:2609.19907` GS-PI PBR 高斯材质 | 3.70 | 渲染与显示 | 该赛道无 A 级以上，唯一接近者 |
| `arXiv:2609.19505` FenceXR AR 动作回放 | 3.65 | 空间计算与UI | 18 名新手 + 4 名专家用户研究 |

## 6. 落后标记判定

- **论文级**：0 篇标记为 OUTDATED / SUPERSEDED。全部为 2026-09-16/17 新作，批次内无时间更晚且同问题更优者。
- **技术路线级**：9 条登记（见 MOC-总索引 §四），每条附对比论文 ID 与量化证据。
- **存疑标记 1 条**：`arXiv:2609.20034` Astronex-World 1.0（DMD 阶段把主体运动残差压到教师的 19%）。证据不足以判定 OUTDATED，标 `CURRENT` + 存疑。

## 7. 产物清单

| 文件 | 说明 |
|---|---|
| `papers/library/registry.jsonl` | 文献库基线，38 行 |
| `papers/daily/2026-09-20/7dim-table.md` | 全量 38 篇 7 维对比表 |
| `papers/daily/2026-09-20/scored.md` | Top10 评分明细 |
| `papers/daily/2026-09-20/run_log.md` | 本文件 |
| `papers/notes/*.md` | 10 篇原子笔记 |
| `papers/MOC/MOC-2026-09-20.md` | 当日 MOC |
| `papers/MOC/MOC-总索引.md` | 全局索引 |
| `reports/XR-Daily-Report-2026-09-20.md` | 最终解读报告 |