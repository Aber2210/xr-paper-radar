# -*- coding: utf-8 -*-
"""update_moc_1128.py —— 总索引维护（2026-11-28 状态日）：状态注记 / 速查入口 / 批次索引行 / 最后更新。"""
import io, re

P = "papers/MOC/MOC-总索引.md"
s = io.open(P, encoding="utf-8").read()
N0 = len(s)

# 1) 状态注记：插在 11-27 注记之后
anchor = "registry 1,269 → **1,332**（+63，备份 `registry.jsonl.bak-20261127`）；原子笔记 **954**、daily **83**、MOC **71**。"
assert s.count(anchor) == 1, s.count(anchor)
note = (
    "\n> **状态注记（2026-11-28）**：周六 02:30，**无新增可处理论文（状态日）**——**11-27（周五）公告组未释放**"
    "（工作日公告跳空，与 2026-10-29、2026-11-12 同型；11-28 周六为 `skipDays` 节律）。"
    "**listing 对账**（`scripts/audit_listing_1128.py`，PREV_DAY=11-26 / NEW_DAYS=11-27,11-28）：7/7 分类成功（exit 0），"
    "最新公告日**全部为 2026-11-26**，11-27 / 11-28 组 `declared=None / got=0`；缓存穿透 `recent?cb=1128a`、`pastweek`、"
    "跨学科 `math.AP` / `cs.CL` 复验一致。**数据源**：API `export.arxiv.org` 200、`published` 前沿 **2026-11-25**，"
    "`cat:cs.CV AND submittedDate:[20261126 TO 20261128]` **0 篇**；RSS `OK_CATS=7/7`、`WROTE=398`——6 分类 **0 条目**，"
    "cs.AI **398 条为陈旧 feed 重戳日期**（逐条 `base_id` 全部 ⊂ 上一批 `2026-11-27.jsonl`（849 条），`cur_only=0`，"
    "**单分类非空 ≠ 有新公告**）。**上一公告组复核**：11-26 组复采 695 槽位 / **569 篇唯一**，已入馆 56（11-27 主批 55 全在组内 + 1 篇库内既有 cross 再公告），"
    "未入馆 **513 篇**，用 11-27（上一批）/ 11-28 两份 RSS 核摘要 **513/513 覆盖（1.0000）**，摘要/标题级命中 **47 篇全部落在 11-27 处置集合**"
    "（`nonxr_1127 ∪ xr_pool_1127 ∪ xr_final_1127 ∪ backfill_pool_1127 ∪ scored_1127 ∪ old_replace_1127`）→ **0 漏网、无 backfill**。"
    "**门③ 现算**：**4.465**（窗口 [2026-10-29, 2026-11-28)、**659 条入窗**；`today_max/margin=null`、"
    "`heavy_day_raw/heavy_day/blockbuster/s_awarded` 全 false；`window_excludes_today=true`、`window_excludes_this_run_batches=true`、"
    "`this_run_batches_excluded=[]`，本日无新稿不授 S）。registry **无变更 1,332**（S21 / A671 / B496 / C144）、笔记 **954**、daily **84**；"
    "OUTDATED / SUPERSEDED **0**。下一调度（11-29 02:30）优先复核 11-27 组是否延迟释放。"
)
s = s.replace(anchor, anchor + note, 1)

# 2) 速查入口：最新运行状态
old_status = re.search(r"^\| 最新运行状态 \| .*$", s, re.M).group(0)
new_status = ("| 最新运行状态 | [运行报告 2026-11-28](../../reports/XR-Daily-Report-2026-11-28.md)"
              "（**状态日 0 新稿**：11-27 周五公告组未释放，listing 7/7 最新公告日仍为 11-26；未入馆 513 篇全摘要覆盖、"
              "命中 47 篇全已处置 → 0 漏网；门③ 现算 **4.465**（659 条入窗）；registry 维持 1,332。"
              "上一批 11-27：主批 55 + backfill 8，非重磅日无 S、门③ 4.35 < 4.459） |")
s = s.replace(old_status, new_status, 1)

# 3) 批次索引行：追加在 backfill-1127 行之后
bf_row = re.search(r"^\| backfill-1127 \|.*$", s, re.M).group(0)
row = ("| 2026-11-28 | — | **0 新稿**（11-27 周五公告组未释放；11-26 组复核 0 漏网） | "
       "状态报告模式：listing 7/7 最新公告日 11-26、11-27/11-28 `declared=None`；RSS 6 分类空源 + cs.AI 398 条陈旧 feed（`cur_only=0`）；"
       "API 前沿 11-25、区间 0 篇；11-26 组 695 槽位 / 569 唯一、未入馆 513 全摘要覆盖、命中 47 篇全已处置；门③ 4.465（659 条入窗） |")
s = s.replace(bf_row, bf_row + "\n" + row, 1)

# 4) 最后更新行
old_lu = re.search(r"^\*最后更新：2026-11-24（.*$", s, re.M).group(0)
new_lu = ("*最后更新：2026-11-28（**状态日 0 新稿**：11-27 周五公告组未释放（工作日公告跳空，同 10-29 / 11-12），"
          "listing 7/7 分类最新公告日仍为 11-26；11-27/11-28 组 `declared=None`；API 前沿 2026-11-25、"
          "`submittedDate:[20261126 TO 20261128]` 0 篇；RSS 6 分类空源、cs.AI 398 条为陈旧 feed（全部 ⊂ 上批 849 条，`cur_only=0`）；"
          "11-26 组复采 695 槽位 / 569 唯一，未入馆 513 篇摘要覆盖 513/513、命中 47 篇全部落在 11-27 处置集合 → **0 漏网**；"
          "门③ 现算 **4.465**（[2026-10-29, 2026-11-28)、659 条入窗、无追加批）；registry 维持 **1,332**（S21/A671/B496/C144）、"
          "笔记 **954**、daily **84**；下一调度 11-29 优先复核 11-27 组是否延迟释放）*")
s = s.replace(old_lu, new_lu, 1)

io.open(P, "w", encoding="utf-8").write(s)
print("MOC updated", N0, "->", len(s))
for k in ("状态注记（2026-11-28）", "| 2026-11-28 | — |", "*最后更新：2026-11-28", "XR-Daily-Report-2026-11-28"):
    print(" ", k, "->", s.count(k))
