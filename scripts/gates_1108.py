"""2026-11-08（周日状态日）：门③ 现算参考值（近 30 天 registry Top10 均分）。
状态日无新候选，门①②不适用；门③现算供 11-09 批次参考。"""
import json
from datetime import date, timedelta

lib = [json.loads(l) for l in open('papers/library/registry.jsonl', encoding='utf-8') if l.strip()]
lo = (date(2026, 11, 8) - timedelta(days=30)).isoformat()
win = [r for r in lib if r.get('date', '') >= lo]
win.sort(key=lambda r: -r.get('value', 0))
top10 = win[:10]
mean = sum(r['value'] for r in top10) / len(top10)
print(f"registry total: {len(lib)}")
print(f"门③ window {lo}~2026-11-08 | in-window {len(win)} | 30d Top10 mean = {mean:.4f}")
for r in top10:
    print(f"   {r['value']:.4f} {r.get('grade')} {r['id'].split(':')[-1]} {r.get('date')} {(r.get('title_zh') or '')[:36]}")
from collections import Counter
print('grade 分布:', dict(Counter(r.get('grade') for r in lib)))
