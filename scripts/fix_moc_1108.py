# -*- coding: utf-8 -*-
"""fix_moc_1108.py — 补插 11-08 状态注记（锚点修正版）+ 顶部摘要行追加。"""
import io, os, re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
moc_path = os.path.join(ROOT, 'papers/MOC/MOC-总索引.md')
moc = io.open(moc_path, encoding='utf-8').read()

# 1) 状态注记：插在 11-07 状态注记行末尾之后
if '状态注记（2026-11-08）' not in moc:
    note = ('> **状态注记（2026-11-08）**：周日 02:30，**无新增可处理论文**（周六 skipDays 无公告，周末状态日模式第 7 次验证，同 11-01）。'
            'listing 7 分类最新公告日均为 **2026-11-06（周五）**（11-07/11-08 周末无公告日段）；'
            'API `submittedDate` 前沿 = **11-05**（已全部入馆或已裁决）；RSS 7 分类全部 0 条目（lastBuildDate 2026-11-07 05:00 UTC，周末节律空源）。'
            '11-06 公告组 show=500 单页全量复采：逐分类 declared=got（CV 138/GR 11/HC 22/MM 2/RO 81/AI 198/IV 6，槽位 458、唯一论文 386），未入馆 363 篇摘要级 XR 命中 12 篇均为 11-07 运行已剔非 XR（逐篇一致）→ **0 漏网、无 backfill**。'
            '未伪造 Top10/评分/S 级；registry 维持 **831 条**（S17/A394/B325/C95）；门③ 现算参考 **4.399**（窗口 2026-10-09~2026-11-08，431 条入窗）。'
            '详见 [状态报告](../../reports/XR-Daily-Report-2026-11-08.md)。')
    anchor = '与 [MOC-2026-11-07](./MOC-2026-11-07.md)。'
    idx = moc.find(anchor)
    if idx >= 0:
        insert_at = idx + len(anchor)
        moc = moc[:insert_at] + '\n' + note + moc[insert_at:]
        print('MOC: 11-08 状态注记已插入')
    else:
        print('MOC WARN: 11-07 注记锚点仍未找到')

# 2) 顶部摘要行追加 11-08 状态日说明
if '11-08 周日状态日 0 新稿' not in moc:
    old_tail = '；**11-07 周六处理 11-06 公告批次（23 篇 XR 新稿 8A/12B/3C，非重磅日无S；RSS 周六空源、listing 唯一采集渠道）**。'
    new_tail = old_tail + '；**11-08 周日状态日 0 新稿**（周六 skipDays 无公告：listing 七分类最新公告日 11-06 + API 前沿 11-05 + RSS 7 分类空源三源互证；11-06 公告组 show=500 单页复采 declared=got 458 槽位/386 唯一，未入馆 363 篇摘要级 12 篇命中均为 11-07 运行已剔非 XR，0 漏网无 backfill）**。'
    if old_tail in moc:
        moc = moc.replace(old_tail, new_tail)
        print('MOC: 顶部摘要行已追加 11-08')
    else:
        print('MOC WARN: 顶部摘要锚点未找到')

with io.open(moc_path, 'w', encoding='utf-8') as f:
    f.write(moc)
print('MOC-总索引.md updated')
