# -*- coding: utf-8 -*-
"""2026-11-11 定稿评分：从 4 组 notes_content 合并，套用主会话校准后的 7 维分与赛道，产出 scored_1111.json。

- batch 字段显式写入（2026-11-11 / backfill-1111），消费者脚本禁止默认值兜底。
- 门③ 现算（窗口 2026-10-12~2026-11-11，415 条入窗，Top10 均分 4.4100）→ today_max 4.57 ≥ 4.4100 → 重磅日，可评 S。
- 主会话校准点：2611.10239 PER 5→4（TUM Sim3 仅 −22%、7-Scenes 持平，增益不均）；2611.12319 PER 5→4（2.93× 仅在 Hier-3DGS 失衡场景，标准基准 1.12×）；2611.10509 赛道 内容生成→神经渲染。
"""
import json, glob

W = {'IMP': 0.20, 'NOV': 0.20, 'TEC': 0.15, 'EXP': 0.15, 'PER': 0.15, 'TRL': 0.08, 'REP': 0.07}

FINAL = {
    # id: (track, IMP, NOV, TEC, EXP, PER, TRL, REP)
    '2611.11169': ('重建与SLAM', 5, 4, 5, 5, 5, 3, 4),
    '2611.11586': ('渲染与显示', 4, 3, 5, 4, 5, 4, 5),
    '2611.10239': ('重建与SLAM', 4, 4, 5, 5, 4, 4, 2),
    '2611.10699': ('重建与SLAM', 4, 4, 5, 4, 4, 3, 5),
    '2611.12319': ('系统与平台', 4, 4, 5, 5, 4, 3, 2),
    '2611.11951': ('重建与SLAM', 4, 4, 4, 4, 5, 3, 3),
    '2611.10370': ('重建与SLAM', 4, 4, 4, 4, 5, 2, 4),
    '2611.12038': ('重建与SLAM', 4, 4, 4, 4, 5, 3, 2),
    '2611.12716': ('神经渲染', 3, 5, 5, 4, 3, 3, 4),
    '2611.10994': ('化身与人体', 5, 4, 5, 4, 1, 3, 5),
    '2611.11964': ('重建与SLAM', 3, 4, 4, 5, 4, 3, 4),
    '2611.10379': ('感知与认知', 4, 3, 4, 5, 4, 3, 3),
    '2611.10349': ('评估与数据集', 4, 4, 5, 4, 2, 2, 5),
    '2611.10637': ('渲染与显示', 4, 4, 4, 4, 3, 3, 3),
    '2611.10652': ('系统与平台', 4, 3, 4, 4, 4, 3, 3),
    '2611.10578': ('感知与认知', 4, 3, 4, 4, 4, 2, 3),
    '2611.10562': ('化身与人体', 4, 4, 4, 4, 3, 2, 2),
    '2611.10509': ('神经渲染', 3, 4, 4, 4, 4, 2, 2),
    '2611.10199': ('交互与输入', 3, 3, 4, 4, 4, 3, 3),
    '2611.11825': ('系统与平台', 3, 3, 4, 4, 3, 2, 3),
    '2611.12452': ('重建与SLAM', 3, 3, 4, 3, 3, 3, 2),
    '2611.12149': ('评估与数据集', 3, 3, 4, 3, 2, 3, 2),
    '2611.12529': ('化身与人体', 3, 3, 3, 4, 2, 2, 3),
    '2611.12130': ('触觉与多模态', 3, 4, 2, 2, 3, 3, 1),
    '2611.11636': ('评估与数据集', 4, 2, 4, 2, 1, 2, 4),
    '2611.11830': ('系统与平台', 2, 2, 4, 3, 3, 3, 2),
    '2611.10013': ('重建与SLAM', 3, 2, 3, 2, 2, 3, 4),
    '2611.12259': ('评估与数据集', 3, 3, 3, 2, 1, 2, 3),
    '2611.09926': ('系统与平台', 5, 2, 2, 1, 1, 1, 3),
    '2611.11640': ('交互与输入', 2, 3, 2, 1, 1, 2, 1),
    '2611.11653': ('感知与认知', 2, 2, 2, 1, 1, 1, 1),
    # backfill（v2/v3 再公告，首次入馆）
    '2609.11894': ('神经渲染', 4, 4, 5, 4, 5, 3, 4),
    '2605.11594': ('重建与SLAM', 4, 4, 4, 5, 4, 3, 3),
    '2605.12297': ('化身与人体', 3, 3, 5, 5, 4, 3, 4),
    '2609.00775': ('重建与SLAM', 4, 3, 4, 4, 3, 4, 2),
    '2603.10801': ('重建与SLAM', 3, 3, 4, 4, 4, 3, 3),
    '2503.00747': ('感知与认知', 3, 3, 4, 3, 2, 3, 3),
    '2608.30368': ('触觉与多模态', 3, 3, 3, 2, 3, 4, 1),
    '2512.14329': ('化身与人体', 4, 4, 2, 3, 4, 3, 1),
}

TITLE_ZH = {
    '2611.11169': 'Map2SLAM：从流式地图预测到实时 SLAM',
    '2611.11586': 'FastGRT：加速 3D 高斯光线追踪的训练',
    '2611.10239': 'DASH-SLAM：深度尺度传播的免标定米制单目 SLAM',
    '2611.10699': 'PLS-GS：概率激光雷达脚手架驱动的紧凑表面对齐高斯泼溅',
    '2611.12319': '缓解 GPU 上 3D 高斯泼溅的 SM 级负载不均衡',
    '2611.11951': 'UltraVoxelGS：体素优先的前馈高斯泼溅用于三维超声重建',
    '2611.10370': 'ClearForm：透明与不透明场景的共享表面高斯泼溅',
    '2611.12038': 'DPGS-SLAM：扩散先验与来源感知的动态单目高斯泼溅 SLAM',
    '2611.12716': 'Spaghetti Splatting：以卷积对曲线型狄拉克质量求导的可微泼溅',
    '2611.10994': 'RoboMoCap：面向机器人学习的第一视角全身动捕大规模数据集',
    '2611.11964': '3R-Adapter：检索-重连-精修的三维重建模型高效适配',
    '2611.10379': 'RefineSplat：重建引导的物体中心高斯泼溅用于开放词表查询',
    '2611.10349': 'SituRecBench：三维环境中具身推荐助手的前沿模型评测',
    '2611.10637': 'VAComp：视角感知的投影仪全补偿',
    '2611.10652': 'SHIN：增量式 3D 高斯泼溅的可扩展层级表示',
    '2611.10578': 'EgoVeil：第一视角视频的个性化隐私推理',
    '2611.10562': 'ZARA：单图零样本可动画可重光照 3D 化身重建',
    '2611.10509': '面向优化的隐式神经表示超网络的可扩展化',
    '2611.10199': 'RigidGS：3D 高斯泼溅中刚体交互的几何感知物体解耦',
    '2611.11825': 'ACROSSVAM3.0：资源受限的四维场景构建与自适应表面关联',
    '2611.12452': 'V3DSAM：前馈稠密 SLAM 的语义-几何回环验证与持久实例建图',
    '2611.12149': 'EgoLabel：跨模态一致的第一视角零样本自动标注',
    '2611.12529': '虚拟现实中智能体-化身控制权切换时的能动性感知',
    '2611.12130': '面向遥操作力觉反馈的紧凑宽量程磁流变手部外骨骼',
    '2611.11636': '扩展现实中的连线测验：面向认知老化的批判性综述',
    '2611.11830': 'ROS2MR：把 ROS 2 运动规划接入混合现实轨迹可视化',
    '2611.10013': '从视频到数字孪生：世界模型与高斯泼溅在野外视频上的探索性研究',
    '2611.12259': '第一视角基础模型的取证评估框架：EFM3D 犯罪现场重建案例',
    '2611.09926': '为何当今互联网无法支撑未来的沉浸式体验：NSF 研讨会洞见',
    '2611.11640': 'Feel My Focus：注视触发的远程协作数字孪生即时创建',
    '2611.11653': '混合现实增强驾驶预警系统：注意转移方式与危险感知的初步研究',
    '2609.11894': '面向毫米波雷达新视角合成的三维点泼溅',
    '2605.11594': 'PointForward：点对齐表示的前馈驾驶场景重建',
    '2605.12297': 'EgoEV-HandPose：双目事件相机的第一视角三维手部姿态与手势识别',
    '2609.00775': 'VOIM：免训练开放词表三维实例建图（RGB-D 与单目 SLAM）',
    '2603.10801': 'PolGS++：物理引导的偏振高斯泼溅快速反射表面重建',
    '2503.00747': 'LFX：融合形态灵活的光场建模用于稠密语义分割与显著目标检测',
    '2608.30368': 'SpectraTac：分布式色彩感知的紧凑无相机光学触觉传感器',
    '2512.14329': '可穿戴数据驱动的生成式数字化身预测任务条件下的卒中后步态',
}

BACKFILL = {'2609.11894', '2605.11594', '2605.12297', '2609.00775', '2603.10801', '2503.00747', '2608.30368', '2512.14329'}
GATE3_MEAN = 4.4100  # 现算（窗口 2026-10-12~2026-11-11，415 条入窗）

items = {}
for f in sorted(glob.glob('data/notes_content_1111_g*.json')):
    for x in json.load(open(f, encoding='utf-8')):
        items[x['id']] = x

RAW_TITLES = {}
for l in open('data/raw/2026-11-11.jsonl', encoding='utf-8'):
    if l.strip():
        r = json.loads(l)
        RAW_TITLES[r['base_id']] = r['title']
for pid, x in items.items():
    x.setdefault('title', RAW_TITLES.get(pid, pid))

# 事实性措辞校正（PLS-GS 指标为 precision，非 accuracy）
items['2611.10699']['conclusion'] = items['2611.10699']['conclusion'].replace(
    '把平均几何精度从 0.330 提到 0.484', '把平均 precision（几何精度）从 0.330 提到 0.484')

assert len(FINAL) == len(items) == 39, (len(FINAL), len(items))
HEAVY = 4.57 >= GATE3_MEAN

main, backfill = [], []
for pid, (track, IMP, NOV, TEC, EXP, PER, TRL, REP) in FINAL.items():
    x = items[pid]
    s = {'IMP': IMP, 'NOV': NOV, 'TEC': TEC, 'EXP': EXP, 'PER': PER, 'TRL': TRL, 'REP': REP}
    v = round(sum(W[k] * s[k] for k in W), 2)
    if v >= 4.2 and HEAVY and pid not in BACKFILL:
        grade, note = 'S', ''
    elif v >= 4.2 and pid in BACKFILL:
        grade, note = 'A', '达 S 线（≥4.20）但 backfill 批次不参与当日重磅日判定，按校准关记 A'
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
        'batch': 'backfill-1111' if pid in BACKFILL else '2026-11-11',
        'date': '2026-11-11',
        'value': v,
        'grade': grade,
        'grade_note': note,
        'scores': s,
        'scores_why': x['scores_why'],
        'evidence': 'PARTIAL' if pid in ('2611.12130', '2512.14329') else 'FULL',
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
    print(f"{i:2d} {r['value']:.2f} {r['grade']} {r['id']} {r['track']:9s} {r['title_zh'][:40]}")
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
from collections import Counter
print('主批等级', Counter(r['grade'] for r in main), 'backfill', Counter(r['grade'] for r in backfill))
print('主批最高', max(r['value'] for r in main), 'HEAVY', HEAVY, '门③均分', GATE3_MEAN)

json.dump({
    'date': '2026-11-11',
    'gate3_mean': GATE3_MEAN,
    'heavy_day': HEAVY,
    'main': main,
    'backfill': backfill,
    'top10_ids': [r['id'] for r in top10],
    'top10_backfill_ids': [r['id'] for r in backfill[:8]],
}, open('data/scored_1111.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print('\nsaved data/scored_1111.json', len(main), '+', len(backfill))
