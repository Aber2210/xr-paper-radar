"""2026-11-07 覆盖度三关计算：
门① 候选 23 篇 vs 库内（追加前 808 条）标题+摘要 token Jaccard 最大值；
门② Top10 赛道覆盖（见 scored_1107.json 定稿，5 赛道）；
门③ 现算库内近 30 天（date>=2026-10-08）按 value 降序 Top10 均分。
注意：对账必须只比对追加前的库内集合（本批全文文件不算「库内」）。
摘要来源：data/missed_xr_abstract_1107.json（listing 摘要级过滤产物，含 title/abstract）。"""
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
    if not a or not b: return 0.0
    return len(a & b) / len(a | b)

sc = json.load(open('data/scored_1107.json', encoding='utf-8'))
CAND = [p['id'] for p in sc['main']]

hits = json.load(open('data/missed_xr_abstract_1107.json', encoding='utf-8'))
raw = {p: {'title': v['title'], 'abstract': v['abstract']} for p, v in hits.items()}

lib = [json.loads(l) for l in open('papers/library/registry.jsonl', encoding='utf-8') if l.strip()]
print('registry (pre-append):', len(lib))

lib_items = []
for r in lib:
    bid = r['id'].split(':')[-1].split('v')[0]
    a = raw.get(bid, {}).get('abstract', '')
    lib_items.append((bid, (r.get('title') or '')[:60], toks((r.get('title') or '') + ' ' + (r.get('title_zh') or '') + ' ' + a)))

rows = []
for pid in CAND:
    r = raw[pid]
    ct = toks(r['title'] + ' ' + r['abstract'])
    best = (0.0, '', '')
    for bid, t, lt in lib_items:
        j = jaccard(ct, lt)
        if j > best[0]: best = (j, bid, t)
    rows.append((pid, best[0], best[1], best[2], r['title'][:60]))
rows.sort(key=lambda x: -x[1])
for pid, j, bid, t, ti in rows[:8]:
    print(f"{pid}  max_jaccard={j:.3f}  vs {bid} {t[:50]}  | {ti[:50]}")
g1 = rows[0]
print(f"\n门① max Jaccard = {g1[1]:.3f} ({g1[0]} vs {g1[2]})  -> {'PASS' if g1[1] < 0.62 else 'FAIL'}")

# 门③
lo = (date(2026, 11, 7) - timedelta(days=30)).isoformat()
win = [r for r in lib if r.get('date', '') >= lo]
win.sort(key=lambda r: -r.get('value', 0))
top10 = win[:10]
mean = sum(r['value'] for r in top10) / len(top10)
today_max = max(p['value'] for p in sc['main'])
print(f"\n门③ window {lo}~2026-11-07 | in-window {len(win)} | 30d Top10 mean = {mean:.4f}")
for r in top10:
    print(f"   {r['value']:.4f} {r.get('grade')} {r['id'].split(':')[-1]} {r.get('date')} {(r.get('title_zh') or '')[:36]}")
print(f"   today_max = {today_max:.4f} -> {'重磅日（可评 S）' if today_max >= mean else '非重磅日（无 S 级，达线者按校准关记 A）'}")

# 门②
tracks = [next(p for p in sc['main'] if p['id'] == pid)['track'] for pid in sc['top10_ids']]
print(f"\n门② Top10 tracks: { {t: tracks.count(t) for t in sorted(set(tracks))} } -> {'PASS' if len(set(tracks)) >= 5 else 'FAIL'}")
allt = {}
for p in sc['main']:
    allt[p['track']] = allt.get(p['track'], 0) + 1
print('全批赛道分布:', allt)
