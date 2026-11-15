# -*- coding: utf-8 -*-
"""gates_1116.py — 2026-11-16 状态日：门③ 价值天花板现算 + 覆盖度三关留痕。

口径（用户任务书第 6 步）：
  date >= today-30 天的 registry 按 value 降序取前 10 篇的均分；today_max >= 均分 = 重磅日。
本日为状态日（0 候选），门③ 仅作下一批参考值记录，不触发重筛。
"""
import io, json, os, datetime, collections

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TODAY = datetime.date(2026, 11, 16)
LO = (TODAY - datetime.timedelta(days=30)).isoformat()

reg = []
for l in io.open(os.path.join(ROOT, 'papers/library/registry.jsonl'), encoding='utf-8'):
    l = l.strip()
    if l:
        reg.append(json.loads(l))

win = [r for r in reg if r.get('date', '') >= LO]
top = sorted(win, key=lambda r: (-r.get('value', 0), r['id']))[:10]
mean = round(sum(r['value'] for r in top) / len(top), 4)

g = collections.Counter(r.get('grade') for r in reg)
notes_n = len([f for f in os.listdir(os.path.join(ROOT, 'papers/notes')) if f.endswith('.md')])
daily_n = len([d for d in os.listdir(os.path.join(ROOT, 'papers/daily'))])
moc_n = len([f for f in os.listdir(os.path.join(ROOT, 'papers/MOC'))
             if f.startswith('MOC-') and f != 'MOC-总索引.md'])

out = {
    'run_date': TODAY.isoformat(),
    'run_type': 'status_day_weekend_backlog_pending',
    'registry_total': len(reg),
    'grades': dict(sorted(g.items())),
    'notes': notes_n,
    'daily_dirs': daily_n,
    'moc_files': moc_n,
    'gate3': {
        'window_lo': LO,
        'window_hi': TODAY.isoformat(),
        'in_window': len(win),
        'top10_mean': mean,
        'top10': [{'id': r['id'], 'date': r.get('date'), 'value': r.get('value'),
                   'grade': r.get('grade')} for r in top],
        'today_max': None,
        'verdict': 'no_candidate_status_day',
    },
    'gate1': 'N/A（0 候选）',
    'gate2': 'N/A（0 候选）',
}
json.dump(out, io.open(os.path.join(ROOT, 'data/gates_1116.json'), 'w', encoding='utf-8'),
          ensure_ascii=False, indent=1)
print(json.dumps({k: v for k, v in out.items() if k != 'gate3'}, ensure_ascii=False))
print('gate3 window', LO, '~', TODAY, 'in_window', len(win), 'top10_mean', mean)
for r in top:
    print('  ', r.get('date'), r['id'], r.get('value'), r.get('grade'))
