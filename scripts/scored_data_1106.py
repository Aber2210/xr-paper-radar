# -*- coding: utf-8 -*-
"""组装 2026-11-06 评分数据：digest（子代理全文精读）+ 主会话 7 维评分定稿。
输出 data/scored_1106.json（main 12 + backfill 6）。内联中文文本统一中文弯引号。
候选池：2026-11-05（周四）公告批次。listing 7 分类最新公告日均为 11-05（无漏跑公告日），
11-04 组复采 declared=got 且 13 篇摘要级命中均为上批已剔非 XR（0 漏网）；
11-05 组 398 篇摘要级 XR 命中 22 篇，与 RSS 真新 22 篇集合同一（两渠道互证）。
主批 12 篇 XR（10 篇非 XR 剔除）；backfill-1106：RSS 混入旧稿 replace/cross 再公告 6 篇 XR（首次入馆）。
提交日核验（API published）：主批 11×2026-11-04 + 1×2026-11-03；backfill 为 2024-01~2026-10 旧稿 v 更新。
公告日 11-05 ≠ 拉取日 11-06 ≠ 提交日，全部产物显式标注。"""
import json

D = {}
for g in ('g1', 'g2', 'g3', 'g4'):
    for d in json.load(open(f'data/digest_1106_{g}.json', encoding='utf-8')):
        D[d['id']] = d

# 评分表：id -> (title_zh, track, IMP,NOV,TEC,EXP,PER,TRL,REP, grade, grade_note)
S_MAIN = {
 '2611.06817': ('Open-HumanScale：面向具身基础模型的人机经验规模化开放配方', '感知与认知', 4.5,4.5,4.5,5,4.5,4,5, 'S', ''),
 '2611.06020': ('METRIC-GS：面向 3D 高斯泼溅的选择性度量尺度估计', '重建与SLAM', 4,4,4.5,4.5,3.5,4,3, 'A', ''),
 '2611.06308': ('隐式语义尺度锚定与序列一致回环的 VGGT-SLAM 改进', '重建与SLAM', 4,4,4,4,4,3.5,4, 'A', ''),
 '2611.06061': ('TouchéWorld：面向生成式世界的在线统一相机-手部探索（技术报告）', '交互与输入', 4,4,4,4,3.5,3.5,4, 'A', ''),
 '2611.06258': ('CrossPressor：可扩展的跨视图融合前馈 3D 高斯泼溅', '神经渲染', 3.5,4,4.5,4,3.5,4,3, 'A', ''),
 '2611.06273': ('OccSplat：驾驶场景重建向何处去？遮挡感知的高斯致密化', '神经渲染', 3.5,4,4,4,3.5,3,2.5, 'A', ''),
 '2611.05593': ('GaussianRenderFormer：基于 Transformer 的无光栅化器 3D 高斯渲染', '神经渲染', 3.5,4,4.5,4,2,2,4.5, 'B', '诚实的探索性负面结果：质量与速度均不实用，但诊断与开源完整'),
 '2611.06593': ('BudgetSplat：预算可控的通用高斯泼溅', '神经渲染', 3.5,3.5,4,3.5,3.5,3.5,2.5, 'B', '门②重筛剔除项：神经渲染赛道冗余，让位未覆盖赛道；仍入馆'),
 '2611.05938': ('反射鲁棒的立体视觉惯性里程计：基于 Kalman 滤波的地面高度估计', '重建与SLAM', 3.5,3.5,4,3.5,3.5,3.5,2, 'B', ''),
 '2611.06121': ('基于像素级可见光通信投影空间的三维位姿估计', '感知与认知', 3,3.5,4,4,3.5,3,2.5, 'B', '空间 AR（投影式）定位的可行性验证， niche 但问题干净'),
 '2611.06734': ('智能手机辅助的 VR HIIT 健身游戏：实时姿态估计的游戏化健身', '空间计算与UI', 3.5,3,3.5,3.5,3,3,2, 'B', '门②回补项：未覆盖的 XR 核心赛道（空间计算与UI）B 级池最高分'),
 '2611.06689': ('危险环境 ROV 遥操作中触觉反馈的认知与行为效应', '触觉与多模态', 3,3,3.5,3,3,2.5,2.5, 'B', 'N=8 小样本人体因素研究；触觉双面性发现有参考价值'),
}

S_BF = {
 '2506.07886': ('EgoM2P：第一人称多模态多任务预训练', '感知与认知', 4,4.5,4.5,4,4,3.5,3.5, 'A', ''),
 '2511.17747': ('AEGIS：以对抗扰动保护 3D 面部化身隐私', '化身与人体', 3.5,4,4.5,4.5,4,4,4.5, 'A', ''),
 '2401.08739': ('EgoGen：第一人称合成数据生成器', '感知与认知', 4,4,4,4,4,3.5,3.5, 'A', ''),
 '2604.24033': ('EvSLAM：面向高速机动的事件相机 SLAM 基准', '评估与数据集', 3.5,3.5,4,4,3,4,4.5, 'A', ''),
 '2607.14836': ('PIDiffSign：基于扩散的运动学动力学模型的三维手语产生', '化身与人体', 3.5,4,4,4,3.5,3,3, 'A', ''),
 '2611.00177': ('AuroraWorld：面向机器人操作中外部到第一人称视频生成的结构化 4D 世界建模', '世界模型与仿真', 3.5,4,4,4,3.5,2.5,2, 'B', ''),
}

def val(s):
    return round(0.20*s[0]+0.20*s[1]+0.15*s[2]+0.15*s[3]+0.15*s[4]+0.08*s[5]+0.07*s[6], 4)

MAIN, BF = [], []
# RSS announce type（new=新提交公告；cross=跨列表新提交公告；replace=旧稿更新再公告）
ANNOUNCE_MAIN = {'2611.05593': 'cross', '2611.06689': 'cross'}
for pid, (tzh, track, imp, nov, tec, exp, per, trl, rep, grade, note) in S_MAIN.items():
    d = D[pid]
    MAIN.append(dict(id=pid, title='', title_zh=tzh, track=track,
        scores=dict(IMP=imp,NOV=nov,TEC=tec,EXP=exp,PER=per,TRL=trl,REP=rep), grade=grade,
        grade_note=note, evidence='FULL', level='L0',
        status='CURRENT', venue=d['venue'],
        announce=ANNOUNCE_MAIN.get(pid, 'new'), tags=d['tags'],
        conclusion=d['conclusion'], problem=d['problem'], method=d['method'], experiments=d['experiments'],
        innovation=d['innovation'], limits=d['limits'], relation=d['relation'], repro=d['repro'], action=d['action'],
        value=val((imp,nov,tec,exp,per,trl,rep)), batch='2026-11-06'))
BF_WINDOW = {
 '2401.08739': '旧稿 replace 再公告（首次入馆）：2401=2024-01-16 投稿，v3 于 2026-11-04 更新',
 '2506.07886': '旧稿 replace 再公告（首次入馆）：2506=2025-06-09 投稿，v4 于 2026-11-04 更新',
 '2511.17747': '旧稿 replace 再公告（首次入馆）：2511=2025-11-21 投稿，v2 于 2026-11-04 更新',
 '2607.14836': '旧稿 replace 再公告（首次入馆）：2607=2026-07-16 投稿，v2 于 2026-11-04 更新',
 '2611.00177': '旧稿 replace-cross 再公告（首次入馆）：2611=2026-10-30 投稿，v2 于 2026-11-04 更新',
 '2604.24033': '旧稿 replace 再公告（首次入馆）：2604=2026-04-27 投稿，v3 于 2026-11-04 更新',
}
BF_ANNOUNCE = {'2611.00177': 'replace-cross'}
for pid, (tzh, track, imp, nov, tec, exp, per, trl, rep, grade, note) in S_BF.items():
    d = D[pid]
    BF.append(dict(id=pid, title='', title_zh=tzh, track=track,
        scores=dict(IMP=imp,NOV=nov,TEC=tec,EXP=exp,PER=per,TRL=trl,REP=rep), grade=grade,
        grade_note=note, evidence='FULL', level='L0',
        status='CURRENT', venue=d['venue'],
        announce=BF_ANNOUNCE.get(pid, 'replace'), tags=d['tags'],
        conclusion=d['conclusion'], problem=d['problem'], method=d['method'], experiments=d['experiments'],
        innovation=d['innovation'], limits=d['limits'], relation=d['relation'], repro=d['repro'], action=d['action'],
        value=val((imp,nov,tec,exp,per,trl,rep)), batch='backfill-1106',
        orig_window=BF_WINDOW[pid]))

# 原始英文标题（RSS）
rss = {json.loads(l)['base_id']: json.loads(l) for l in open('data/raw/2026-11-06.jsonl',encoding='utf-8') if l.strip()}
for p in MAIN + BF:
    p['title'] = rss[p['id']]['title']

MAIN.sort(key=lambda r: (-r['value'], -r['scores']['IMP'], -r['scores']['NOV'], r['id']))
BF.sort(key=lambda r: (-r['value'], -r['scores']['IMP'], -r['scores']['NOV'], r['id']))

# Top10 定稿（门②重筛后）：纯价值 Top10 仅覆盖 4 赛道（神经渲染×4 冗余）
# → 剔除神经渲染最低分 BudgetSplat 3.505，回补未覆盖核心赛道（空间计算与UI）B 级池最高分 VR HIIT 3.18
TOP10_IDS = ['2611.06817', '2611.06020', '2611.06308', '2611.06061', '2611.06258',
             '2611.06273', '2611.05593', '2611.05938', '2611.06121', '2611.06734']
assert len(TOP10_IDS) == 10 and len(set(TOP10_IDS)) == 10
assert all(pid in {p['id'] for p in MAIN} for pid in TOP10_IDS)

json.dump(dict(main=MAIN, backfill=BF, top10_ids=TOP10_IDS), open('data/scored_1106.json','w',encoding='utf-8'), ensure_ascii=False, indent=1)
print('main', len(MAIN), 'backfill', len(BF))
for r in MAIN:
    print(f"  {r['value']:.4f} {r['grade']} {r['id']} {r['track']} {r['title_zh'][:40]}")
for r in BF:
    print(f"  BF {r['value']:.4f} {r['grade']} {r['id']} {r['track']} {r['title_zh'][:40]}")
