# -*- coding: utf-8 -*-
# build_1023.py — 2026-10-23 主批 + backfill-1023：registry 幂等追加（先备份）+ 7维表 + scored.md + run_log.md
import json, os, shutil, datetime, re

ROOT = 'D:/Agent/WorkBuddy/Research'
REG = f'{ROOT}/papers/library/registry.jsonl'
W = {'IMP':0.20,'NOV':0.20,'TEC':0.15,'EXP':0.15,'PER':0.15,'TRL':0.08,'REP':0.07}
def grade(v):
    return 'S' if v>=4.2 else ('A' if v>=3.6 else ('B' if v>=3.0 else 'C'))

manifest = json.load(open(f'{ROOT}/data/fulltext/_manifest.json', encoding='utf-8'))
batches = [
    ('2026-10-23', f'{ROOT}/data/scored_1023.json', f'{ROOT}/data/xr_pool_2026-10-23.json',
     f'{ROOT}/papers/daily/2026-10-23'),
    ('backfill-1023', f'{ROOT}/data/scored_backfill_1023.json', f'{ROOT}/data/xr_pool_backfill_1023.json',
     f'{ROOT}/papers/daily/backfill-1023'),
]

# ---- 库内历史（门① 对比用：排除本批两个 batch）----
reg_hist = []
for l in open(REG, encoding='utf-8'):
    if l.strip():
        d = json.loads(l)
        if d.get('batch') not in ('2026-10-23', 'backfill-1023'):
            reg_hist.append(d)

def toks(s):
    return set(t for t in re.findall(r'[A-Za-z][A-Za-z0-9\-]{2,}', (s or '').lower()) if t not in STOP)

STOP = {'the','and','for','with','from','that','this','are','was','not','using','via','our','its','can','all','more','than','has','have','been','also','such','when','into','over','under','between','based','method','methods','paper','propose','proposed','show','shows','results','result','approach','model','models','data','task','tasks','learning','network','networks','image','images','video','videos','scene','scenes','object','objects','robotic','robot','robots'}

def jac(a, b):
    if not a or not b: return 0.0
    return len(a & b) / len(a | b)

for batch, scored_f, pool_f, DAILY in batches:
    os.makedirs(DAILY, exist_ok=True)
    scored = json.load(open(scored_f, encoding='utf-8'))
    pool = json.load(open(pool_f, encoding='utf-8'))
    byid = {p['id']: p for p in pool}
    items = []
    for p in scored['pool']:
        v = round(sum(W[k]*p[k] for k in W), 4)
        items.append(dict(p, value=v, grade=grade(v)))

    # ---- 门①：与库内历史（batch 非本批）最大 Jaccard ----
    sims = []
    for it in items:
        t1 = toks(byid[it['id']]['title'] + ' ' + byid[it['id']].get('abstract',''))
        for r in reg_hist:
            t2 = toks(r.get('title','') + ' ' + r.get('title_zh',''))
            sims.append((jac(t1, t2), it['id'], r['id']))
    sims.sort(reverse=True)
    top_sims = sims[:3]
    print(f'[{batch}] 门① top3:', [(round(s,3), a, b) for s,a,b in top_sims])

    # ---- Top10 ----
    items.sort(key=lambda x: (-x['value'], -x['IMP'], -x['NOV'], x['id']))
    groups = []
    for it in items:
        if groups and groups[-1][0] == it['value']:
            groups[-1][1].append(it)
        else:
            groups.append((it['value'], [it]))
    top10, used = [], set()
    for val, grp in groups:
        if len(top10) >= 10: break
        grp = sorted(grp, key=lambda t: (t['track'] in used, t['id']))
        for it in grp:
            if len(top10) >= 10: break
            top10.append(it); used.add(it['track'])
    top10_ids = {t['id'] for t in top10}
    tracks_top = sorted({t['track'] for t in top10})
    tracks_all = sorted({it['track'] for it in items})
    print(f'[{batch}] Top10:', [(t['id'], t['value']) for t in top10])
    print(f'[{batch}] Top10 赛道:', tracks_top, '| 全批赛道:', tracks_all)

    # ---- registry 备份 + 幂等追加 ----
    bak = f'{REG}.bak-20261023'
    if not os.path.exists(bak):
        shutil.copy(REG, bak); print('backup ->', bak)
    reg = {}
    for l in open(REG, encoding='utf-8'):
        if l.strip():
            d = json.loads(l); reg[d['id'].split(':')[-1].split('v')[0]] = d
    n0 = len(reg); added = 0
    with open(REG, 'a', encoding='utf-8') as f:
        for it in items:
            bid = it['id']
            if bid in reg: continue
            m = manifest.get(bid, {})
            rec = {
                'id': f'arXiv:{bid}',
                'title': byid[bid]['title'],
                'title_zh': it['title_zh'],
                'track': it['track'],
                'date': byid[bid].get('published','')[:10],
                'value': it['value'],
                'grade': it['grade'],
                'scores': {k: it[k] for k in W},
                'status': 'CURRENT',
                'evidence': m.get('evidence','FULL'),
                'fetch_level': m.get('level','L0'),
                'fulltext_chars': m.get('chars',0),
                'in_top10': bid in top10_ids,
                'batch': batch,
                'orig_window': scored['orig_window'],
                'announce_type': it['announce'],
                'flags': [],
            }
            f.write(json.dumps(rec, ensure_ascii=False) + '\n')
            reg[bid] = rec; added += 1
    # 显式校正本批已存在条目的 in_top10（防错误运行残留）
    fixed = 0
    lines = [l for l in open(REG, encoding='utf-8') if l.strip()]
    out = []
    for l in lines:
        d = json.loads(l)
        if d.get('batch') == batch:
            want = d['id'].split(':')[-1].split('v')[0] in top10_ids
            if d.get('in_top10') != want:
                d['in_top10'] = want; fixed += 1
        out.append(json.dumps(d, ensure_ascii=False))
    open(REG, 'w', encoding='utf-8').write('\n'.join(out) + '\n')
    print(f'[{batch}] registry: {n0} -> {len(reg)} (+{added})，in_top10 校正 {fixed} 处')
    json.dump({'batch': batch, 'top10': [t['id'] for t in top10],
               'tracks_top': tracks_top, 'tracks_all': tracks_all,
               'gate1_top3': [[round(s,3),a,b] for s,a,b in top_sims]},
              open(f'{ROOT}/data/top10_{batch}.json','w',encoding='utf-8'), ensure_ascii=False, indent=1)
