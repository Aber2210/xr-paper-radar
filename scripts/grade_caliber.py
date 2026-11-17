# -*- coding: utf-8 -*-
"""grade_caliber.py —— 档位口径的单一实现（对齐 README「档位」段）。

口径：
  S = 分数 ≥ 4.20 **且** 当日为重磅日（门③ today_max ≥ 库内近 30 天 Top10 均分）；
  A 3.60–4.20 / B 3.00–3.60 / C < 3.00；
  backfill 批（历史补录 / 旧稿再公告）不参与当日重磅日判定，≥4.20 一律记 A。

为什么必须是单一实现：
  7 维表、scored、原子笔记、registry、报告五处此前各自写了一遍阈值，只要有一处漏判
  heavy_day，同一篇就会出现「页面显示 S、报告记 A」这类同批不同档，而两边都自称权威
  （2026-11-17 复评 N-06：write_deliverables_1117{,b,c} 只按分数判 S，write_reports 已改读门③）。

历史批（build_09xx / build_10xx）保留各自的 inline 实现不动：那些批次早已发布，
改口径会让已上线产物与代码不一致；本模块只约束 2026-11-17 起的批次脚本。
"""
S_MIN, A_MIN, B_MIN = 4.20, 3.60, 3.00


def assign_grade(value, batch, heavy_day):
    """返回 'S'/'A'/'B'/'C'。

    heavy_day 必须传入门③ 的现算值（G['gate3']['heavy_day']），不得默认 True——
    默认 True 会让非重磅日凭空出现 S 级，正是本模块要消灭的失效模式。
    """
    v = float(value)
    if v >= S_MIN and bool(heavy_day):
        g = 'S'
    elif v >= A_MIN:
        g = 'A'
    elif v >= B_MIN:
        g = 'B'
    else:
        g = 'C'
    if g == 'S' and str(batch or '').startswith('backfill'):
        g = 'A'
    return g
