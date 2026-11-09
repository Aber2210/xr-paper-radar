# -*- coding: utf-8 -*-
"""2026-11-10 定稿评分：从 4 组 notes_content 合并，套用主会话校准后的 7 维分与赛道，产出 scored_1110.json。

- batch 字段显式写入（2026-11-10 / backfill-1110），消费者脚本禁止默认值兜底。
- 门③ 现算（窗口 2026-10-11~2026-11-10，397 条入窗，Top10 均分 4.399）→ today_max 4.37 < 4.399 → 非重磅日无 S。
- 达 S 线（≥4.20）者按校准关记 A 并写 grade_note（同 10-24 EgoHand / 10-27 WFM / 11-07 XM4D 先例）。
"""
import json, glob

W = {'IMP': 0.20, 'NOV': 0.20, 'TEC': 0.15, 'EXP': 0.15, 'PER': 0.15, 'TRL': 0.08, 'REP': 0.07}

FINAL = {
    # id: (track, IMP, NOV, TEC, EXP, PER, TRL, REP)
    '2611.09458': ('重建与SLAM', 4, 4, 5, 5, 4, 4, 5),
    '2611.08578': ('化身与人体', 4, 5, 4, 4, 5, 3, 5),
    '2611.09089': ('系统与平台', 4, 4, 5, 5, 4, 4, 3),
    '2611.09074': ('内容生成', 4, 4, 4, 5, 5, 4, 3),
    '2611.08731': ('重建与SLAM', 4, 4, 4, 4, 4, 3, 4),
    '2611.09692': ('化身与人体', 3, 5, 4, 4, 4, 2, 3),
    '2611.09129': ('触觉与多模态', 4, 4, 4, 4, 3, 3, 3),
    '2611.09036': ('评估与数据集', 4, 3, 4, 4, 3, 3, 4),
    '2611.09708': ('触觉与多模态', 4, 5, 3, 3, 3, 3, 2),
    '2611.09195': ('化身与人体', 4, 3, 3, 3, 4, 4, 4),
    '2611.09238': ('感知与认知', 4, 3, 4, 4, 3, 3, 3),
    '2611.09584': ('重建与SLAM', 3, 2, 4, 5, 3, 3, 4),
    '2611.09394': ('感知与认知', 4, 4, 3, 3, 3, 2, 2),
    '2611.09524': ('化身与人体', 3, 3, 4, 3, 4, 2, 2),
    # backfill（v2+ 再公告，首次入馆）
    '2605.16981': ('重建与SLAM', 4, 4, 4, 5, 4, 3, 3),
    '2511.18127': ('交互与输入', 4, 4, 4, 4, 4, 3, 3),
    '2607.24409': ('重建与SLAM', 3, 2, 3, 5, 2, 4, 5),
    '2605.31557': ('评估与数据集', 4, 3, 3, 4, 1, 2, 4),
}

TITLE_ZH = {
    '2611.09458': '跨注入的左右一致迭代立体匹配',
    '2611.08578': 'HaNDF：物体条件化的几何神经手部距离场',
    '2611.09089': 'EventHOI：智能眼镜上事件驱动的手-物交互低功耗记录',
    '2611.09074': 'Emo-LiveSync：带显式情绪控制的实时通用唇形同步',
    '2611.08731': 'eSharp：扩散先验驱动的事件相机单目米制深度',
    '2611.09692': 'PoseRieFlow：黎曼流匹配的全身文本到姿态生成',
    '2611.09129': 'TouchAnnotator：特权视图蒸馏的多源触觉标注',
    '2611.09036': 'ToolDex：面向创造性工具使用的自我-外部视角演示数据集',
    '2611.09708': '可穿戴触觉输入/输出接口学习个性化触觉感知模型',
    '2611.09195': 'InstantHMR：手机端实时人体网格恢复',
    '2611.09238': 'VR 中的视听错位：对空间感知的影响',
    '2611.09584': '扩展的基于模型的学习式惯性里程计',
    '2611.09394': '被感知却未告知：隐藏生理适应如何塑造 LLM 说服',
    '2611.09524': 'RadarDINO：把视觉基础模型蒸馏进毫米波雷达做人体网格重建',
    '2605.16981': '重思长序列循环三维重建的状态更新门',
    '2511.18127': 'SFHand：流式第一视角 3D 手部预测的预测式表征学习',
    '2607.24409': '高端街景影像视觉定位的精度潜力',
    '2605.31557': 'EGOSTREAM：第一视角流式情景记忆的诊断基准',
}

BACKFILL = {'2605.16981', '2511.18127', '2607.24409', '2605.31557'}
GATE3_MEAN = 4.399  # 现算（见 gates_1110.py 输出）
HEAVY = 4.37 >= GATE3_MEAN

items = {}
for f in sorted(glob.glob('data/notes_content_1110_g*.json')):
    for x in json.load(open(f, encoding='utf-8')):
        items[x['id']] = x

RAW_TITLES = {}
for l in open('data/raw/2026-11-10.jsonl', encoding='utf-8'):
    if l.strip():
        r = json.loads(l)
        RAW_TITLES[r['base_id']] = r['title']
for pid, x in items.items():
    x.setdefault('title', RAW_TITLES.get(pid, pid))

main, backfill = [], []
for pid, (track, IMP, NOV, TEC, EXP, PER, TRL, REP) in FINAL.items():
    x = items[pid]
    s = {'IMP': IMP, 'NOV': NOV, 'TEC': TEC, 'EXP': EXP, 'PER': PER, 'TRL': TRL, 'REP': REP}
    v = round(sum(W[k] * s[k] for k in W), 2)
    if v >= 4.2 and HEAVY:
        grade, note = 'S', ''
    elif v >= 4.2:
        grade, note = 'A', '达 S 线（≥4.20）但本批非重磅日，按校准关记 A'
    elif v >= 3.6:
        grade, note = 'A', ''
    elif v >= 3.0:
        grade, note = 'B', ''
    else:
        grade, note = 'C', ''
    row = {
        'id': pid,
        'title': x['title'],
        'title_zh': TITLE_ZH[pid],
        'track': track,
        'venue': x['venue'],
        'batch': 'backfill-1110' if pid in BACKFILL else '2026-11-10',
        'date': '2026-11-10',
        'value': v,
        'grade': grade,
        'grade_note': note,
        'scores': s,
        'scores_why': x['scores_why'],
        'evidence': 'PARTIAL' if pid in ('2611.09708', '2611.09195') else 'FULL',
        'tags': x['tags'],
        'slug': x['slug'],
        'conclusion': x['conclusion'],
        'problem': x['problem'],
        'method': x['method'],
        'experiments': x['experiments'],
        'innovation': x['innovation'],
        'limits': x['limits'],
        'relation': x['relation'],
        'repro': x['repro'],
        'action': x['action'],
        'status': 'CURRENT',
    }
    (backfill if pid in BACKFILL else main).append(row)

main.sort(key=lambda r: (-r['value'], -(r['scores']['IMP'] + r['scores']['NOV']), r['id']))
backfill.sort(key=lambda r: (-r['value'], -(r['scores']['IMP'] + r['scores']['NOV']), r['id']))

# Top10：同分按 IMP/NOV 降序 → 赛道多样性优先 → id 升序
def pick_top(rows, n=10):
    out, rest = [], sorted(rows, key=lambda r: (-r['value'], -(r['scores']['IMP'] + r['scores']['NOV']), r['id']))
    while rest and len(out) < n:
        head = rest[0]
        same = [r for r in rest if abs(r['value'] - head['value']) < 1e-9]
        if len(same) == 1:
            out.append(head); rest.remove(head); continue
        covered = {r['track'] for r in out}
        same.sort(key=lambda r: (r['track'] in covered,
                                 -(r['scores']['IMP'] + r['scores']['NOV']),
                                 r['id']))
        out.append(same[0]); rest.remove(same[0])
    return out

top10 = pick_top(main, 10)
print('=== 主批排序 ===')
for i, r in enumerate(main, 1):
    print(f"{i:2d} {r['value']:.2f} {r['grade']} {r['id']} {r['track']:8s} {r['title_zh'][:40]}")
print('\n=== Top10 定稿 ===')
for i, r in enumerate(top10, 1):
    print(f"{i:2d} {r['value']:.2f} {r['grade']} {r['id']} {r['track']}")
print('\n=== backfill ===')
for i, r in enumerate(backfill, 1):
    print(f"{i:2d} {r['value']:.2f} {r['grade']} {r['id']} {r['track']} {r['title_zh'][:36]}")
tracks = [r['track'] for r in top10]
print('\n门② Top10 赛道:', {t: tracks.count(t) for t in sorted(set(tracks))}, 'distinct', len(set(tracks)))
allt = {}
for r in main:
    allt[r['track']] = allt.get(r['track'], 0) + 1
print('全批赛道:', allt, 'distinct', len(allt))
print('主批最高', max(r['value'] for r in main), '重绑定', HEAVY, '门③均分', GATE3_MEAN)

json.dump({
    'date': '2026-11-10',
    'gate3_mean': GATE3_MEAN,
    'heavy_day': HEAVY,
    'main': main,
    'backfill': backfill,
    'top10_ids': [r['id'] for r in top10],
    'top10_backfill_ids': [r['id'] for r in backfill[:8]],
}, open('data/scored_1110.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print('\nsaved data/scored_1110.json', len(main), '+', len(backfill))
