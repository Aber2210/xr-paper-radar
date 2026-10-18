# 执行日志 · 2026-09-25（XR 每日论文雷达）

- 运行时刻：2026-09-25 03:18:03
- 运行模式：真实运行（API 源被代理拦截 → RSS 兜底）

## 1. 数据源探针
- `export.arxiv.org/api/query` → **406**（沙箱代理拦截，与 09-24 一致）
- `arxiv.org/api/query` → 首次 200、复探间歇 406（代理不稳定）
- `rss.arxiv.org` → **200**（稳定）→ 选用 RSS 兜底源

## 2. 拉取（fetch_rss.py）
- 7 分类（cs.GR/HC/CV/MM/RO/AI/eess.IV）RSS "recent" 批次，全量去重 720 条 → 关键词命中 38 条
- 去 registry(133) 后：真正新 2609.* = **15 篇**（13 XR 相关 + 2 非XR）
- 排除：23 条（16 已在库 + 7 旧稿 replace/cross：2603/2604/2605/2607/2510/2512 等），非当日新提交

## 3. 全文抓取（fetch_fulltext.py）
- 15 篇候选全部 L0/FULL（arxiv.org/html 源）；串行 3s/篇，无 429/406/降级/伪造

## 4. 评分与覆盖度
- Top10 均分 3.892；最高 4.05；S 级 0 / A 级 10
- 门① max Jaccard 0.308 <0.62 通过；门② 覆盖 6 赛道通过；门③ 非重磅日（4.05<4.298）
- 三关通过，未触发重筛

## 5. 遗留与建议
- RSS 混入旧稿（7 篇非 2609 旧 ID）建议代理恢复后用 API `submittedDate` 窗口 backfill
- `fetch_arxiv.py` 端点已临时改为 `https://arxiv.org/api/query`（export 仍 406）；恢复后改回
- 已知遗留缺口仍存：近眼显示/光场/全息等**硬件类**渲染（库内仍全为算法侧）