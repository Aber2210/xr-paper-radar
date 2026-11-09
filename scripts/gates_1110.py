"""2026-11-10 覆盖度三关：
门① 18 篇候选 vs 库内（追加前 831 条）标题+摘要 token Jaccard 最大；
门② Top10 赛道覆盖；
门③ 现算库内近 30 天 Top10 均分（窗口 2026-10-11~2026-11-10）。
摘要来源：data/raw/2026-11-10.jsonl（RSS 命中 31 篇，含本批 18 候选）。
"""
import json, re
from datetime import date, timedelta

STOP = set("""a an the of for and or to in on with by from at as is are be we our this that
it its via using based can may propose present introduce towards toward novel
learning framework approach method results show shows while however both all one
two also more most than which when where such these those paper work works""".split())


def toks(s):
    s = re.sub(r"[^a-z0-9 ]", " ", (s or "").lower())
    return set(w for w in s.split() if len(w) > 2 and w not in STOP)


def jaccard(a, b):
    if not a or not b:
        return 0.0
    return len(a & b) / len(a | b)


sc = json.load(open('data/scored_1110.json', encoding='utf-8'))
CAND = [p['id'] for p in sc['main']] + [p['id'] for p in sc['backfill']]

raw = {}
for l in open('data/raw/2026-11-10.jsonl', encoding='utf-8'):
    if l.strip():
        r = json.loads(l)
        raw[r['base_id']] = {'title': r['title'], 'abstract': r['abstract']}
miss = [p for p in CAND if p not in raw]
print('candidates', len(CAND), 'abstract missing', miss)

lib = [json.loads(l) for l in open('papers/library/registry.jsonl', encoding='utf-8') if l.strip()]
print('registry (pre-append):', len(lib))

lib_items = []
for r in lib:
    bid = r['id'].split(':')[-1].split('v')[0]
    lib_items.append((bid, (r.get('title') or '')[:60],
                      toks((r.get('title') or '') + ' ' + (r.get('title_zh') or ''))))

rows = []
for pid in CAND:
    if pid not in raw:
        continue
    ct = toks(raw[pid]['title'] + ' ' + raw[pid]['abstract'])
    best = (0.0, '', '')
    for bid, t, lt in lib_items:
        j = jaccard(ct, lt)
        if j > best[0]:
            best = (j, bid, t)
    rows.append((pid, best[0], best[1], best[2], raw[pid]['title'][:60]))
rows.sort(key=lambda x: -x[1])
for pid, j, bid, t, ti in rows[:6]:
    print(f"{pid}  max_jaccard={j:.3f}  vs {bid} {t[:44]}  | {ti[:44]}")
g1 = rows[0]
print(f"\n门① max Jaccard = {g1[1]:.3f} ({g1[0]} vs {g1[2]}) -> {'PASS' if g1[1] < 0.62 else 'FAIL'}")

# 门③
today = date(2026, 11, 10)
lo = (today - timedelta(days=30)).isoformat()
win = [r for r in lib if (r.get('date') or '') >= lo]
win.sort(key=lambda r: -float(r.get('value', 0)))
top10 = win[:10]
mean = sum(float(r['value']) for r in top10) / len(top10)
today_max = max(p['value'] for p in sc['main'])
print(f"\n门③ window {lo}~2026-11-10 | in-window {len(win)} | 30d Top10 mean = {mean:.4f}")
for r in top10:
    print(f"   {float(r['value']):.2f} {r.get('grade')} {r['id'].split(':')[-1]} {r.get('date')} {(r.get('title_zh') or '')[:34]}")
print(f"   today_max = {today_max:.4f} -> {'重磅日（可评 S）' if today_max >= mean else '非重磅日（无 S 级，达线者按校准关记 A）'}")

# 门②
tracks = [next(p for p in sc['main'] if p['id'] == pid)['track'] for pid in sc['top10_ids']]
print(f"\n门② Top10 tracks: { {t: tracks.count(t) for t in sorted(set(tracks))} } -> {'PASS' if len(set(tracks)) >= 5 else 'FAIL'}")
allt = {}
for p in sc['main']:
    allt[p['track']] = allt.get(p['track'], 0) + 1
print('全批赛道分布:', allt, '->', len(allt), '赛道')
print('\n达 S 线（≥4.20）:', [(p['id'], p['value'], p['grade']) for p in sc['main'] if p['value'] >= 4.2])
