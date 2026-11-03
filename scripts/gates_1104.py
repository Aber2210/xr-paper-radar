"""2026-11-04 覆盖度三关计算：
门① 候选 43 篇 vs 库内（追加前 730 条）标题+摘要 token Jaccard 最大值；
门③ 现算库内近 30 天（date>=2026-10-05）按 value 降序 Top10 均分。
注意：对账必须只比对追加前的库内集合（本批全文文件不算「库内」）。"""
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

cands = json.load(open('data/candidates_1104.json', encoding='utf-8'))
CAND = cands['main'] + cands['backfill']

raw = {}
for l in open('data/raw/2026-11-04.jsonl', encoding='utf-8'):
    if l.strip():
        r = json.loads(l); raw[r['base_id']] = r

lib = [json.loads(l) for l in open('papers/library/registry.jsonl', encoding='utf-8') if l.strip()]
print('registry (pre-append):', len(lib))

# 门①：本批候选 vs 库内（registry 尚未追加本批）
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
    print(f"{pid}  max_jaccard={best[0]:.3f}  vs {best[1]} {best[2][:50]}")
g1 = max(rows, key=lambda x: x[1])
print(f"\n门① max Jaccard = {g1[1]:.3f} ({g1[0]} vs {g1[2]}) -> {'PASS' if g1[1] < 0.62 else 'FAIL'}")

# 门③：近 30 天窗口现算
today = date(2026, 11, 4)
lo = today - timedelta(days=30)
win = [r for r in lib if r.get('date', '') >= lo.isoformat()]
win.sort(key=lambda r: -r['value'])
top10 = win[:10]
mean = sum(r['value'] for r in top10) / len(top10)
print(f"\n门③ 窗口 {lo.isoformat()} ~ {today.isoformat()}，入窗 {len(win)} 条")
for r in top10:
    print(f"  {r['id'].split(':')[-1]:<14} {r['value']:.2f} {r.get('grade','')} {r.get('date','')} {(r.get('title_zh') or r.get('title') or '')[:40]}")
print(f"门③ 近 30 天 Top10 均分 = {mean:.4f}")

json.dump({'gate1_max': round(g1[1], 4), 'gate1_pair': [g1[0], g1[2]],
           'gate3_window': [lo.isoformat(), today.isoformat()], 'gate3_n': len(win),
           'gate3_mean': round(mean, 4), 'gate3_top10': [(r['id'], r['value'], r.get('date')) for r in top10]},
          open('data/gates_1104.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print('saved data/gates_1104.json')
