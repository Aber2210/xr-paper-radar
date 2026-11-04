# -*- coding: utf-8 -*-
"""组装 2026-11-05 评分数据：digest（子代理全文精读）+ 主会话 7 维评分定稿。
输出 data/scored_1105.json（main 9 + backfill 8）。内联中文文本统一中文弯引号。
候选池：2026-11-04（周三）公告批次（9 篇均为 2026-11-03 提交；listing 450 篇摘要级 XR 命中 22 篇，
与 RSS 真新集合逐篇一致，两渠道互证；13 篇非 XR 剔除）。backfill-1105：RSS 混入的旧稿 replace/cross
再公告中 8 篇 XR（首次入馆）。"""
import json

D = {}
for g in ('g1', 'g2', 'g3', 'g4'):
    for d in json.load(open(f'data/digest_1105_{g}.json', encoding='utf-8')):
        D[d['id']] = d

# 评分表：id -> (title_zh, track, IMP,NOV,TEC,EXP,PER,TRL,REP, grade, grade_note)
S_MAIN = {
 '2611.04498': ('3DGS-VBench+ 与 3DGSV-Assessor：3D 高斯泼溅视频质量的多维主观基准与参考灵活客观模型', '评估与数据集', 4,4,4,4,4,3,5, 'A', ''),
 '2611.04195': ('SettleSplat：视野内场景变化下的单目高斯建图', '重建与SLAM', 4,4,4,4,4,3,3, 'A', ''),
 '2611.04494': ('AR 眼镜的空间记忆：层级视觉采集与源链接召回', '空间计算', 4,4,4,3,3,4,4, 'A', ''),
 '2611.04666': ('Phase-DGS：以语义相位引导的非同步多视图动态高斯泼溅', '神经渲染', 3,4,4,4,4,3,3, 'A', ''),
 '2611.04374': ('IGSW：内在解耦高斯泼溅的多天气城市场景重建', '重建与SLAM', 3,4,4,4,4,3,3, 'A', ''),
 '2611.04358': ('EndoS3：内镜语义泼溅 SLAM 与 CRCD++ 数据集', '重建与SLAM', 3,4,4,3,4,3,4, 'B', '医学（内镜）领域 SLAM，方法为通用 3DGS 语义 SLAM；XR 相关性经 AR 手术导航路径评估'),
 '2611.04173': ('ReconDreamer#：动态驾驶场景重建与生成的自进化闭环协同', '世界模型与仿真', 3,3,4,4,4,3,2, 'B', '库内 ReconDreamer/ReconDreamer++ 的期刊扩展，增量贡献为主'),
 '2611.05176': ('MM-AR 元建模平台的过程挖掘能力扩展', '空间计算与UI', 3,3,3,3,2,3,4, 'C', '原理验证级平台集成；3D 维度不携带信息（2D 布局缩放）'),
 '2611.05359': ('GSCV++：以标准视频编解码器进行轻量 3D 高斯泼溅序列压缩', '神经渲染', 3,3,2,1,2,3,2, 'C', '证据等级 L1/PARTIAL：ar5iv 仅摘要页，摘要级评估，正文数据不可核实'),
}

S_BF = {
 '2606.29494': ('VCS-SLAM：可见性一致的语义融合 3D 高斯 SLAM', '重建与SLAM', 3,4,4,4,4,4,5, 'A', ''),
 '2606.03994': ('SimuScene：物理在环的单图仿真就绪组合式三维场景重建', '重建与SLAM', 3,4,4,4,4,3,5, 'A', ''),
 '2603.07604': ('EmbedTalk：以高斯嵌入进行说话头合成', '化身与人体', 3,4,4,4,4,4,3, 'A', ''),
 '2607.18539': ('AniGS：桥接渲染与扩散先验的三维场景动画', '神经渲染', 3,4,4,4,4,3,2, 'B', ''),
 '2606.01643': ('手语产生中的条件崩塌：一项诊断与覆盖度论证', '评估与数据集', 3,4,4,4,3,3,4, 'B', '化身动作生成评测方法论；FID/BLEU 与忠实度脱节的实证'),
 '2608.00232': ('手术增强现实中的实时视觉遮挡检测', '空间计算与UI', 3,4,4,3,4,4,2, 'B', '首个伪 AR 手术遮挡检测基准；级联小到大 VLM 边缘部署'),
 '2603.16016': ('FlatLands：单张第一视角图像的室内地板图补全', '评估与数据集', 3,3,4,4,3,3,4, 'B', ''),
 '2606.26364': ('「真实的狗耳」：主动与被动触觉对非人类身体部件具身的影响', '触觉与多模态', 3,4,3,3,3,3,3, 'B', ''),
}

def val(s):
    return round(0.20*s[0]+0.20*s[1]+0.15*s[2]+0.15*s[3]+0.15*s[4]+0.08*s[5]+0.07*s[6], 4)

MAIN, BF = [], []
ANNOUNCE_MAIN = {}
EVID = {'2611.05359': ('L1', 'PARTIAL')}
for pid, (tzh, track, imp, nov, tec, exp, per, trl, rep, grade, note) in S_MAIN.items():
    d = D[pid]
    lv, ev = EVID.get(pid, ('L0', 'FULL'))
    MAIN.append(dict(id=pid, title='', title_zh=tzh, track=track,
        scores=dict(IMP=imp,NOV=nov,TEC=tec,EXP=exp,PER=per,TRL=trl,REP=rep), grade=grade,
        grade_note=note, evidence=ev, level=lv,
        status='CURRENT', venue=d['venue'],
        announce=ANNOUNCE_MAIN.get(pid, 'new'), tags=d['tags'],
        conclusion=d['conclusion'], problem=d['problem'], method=d['method'], experiments=d['experiments'],
        innovation=d['innovation'], limits=d['limits'], relation=d['relation'], repro=d['repro'], action=d['action'],
        value=val((imp,nov,tec,exp,per,trl,rep)), batch='2026-11-05'))
BF_WINDOW = {
 '2606.29494': '旧稿 replace 再公告（首次入馆）：2606=2026-06 投稿，v2 于 2026-11-03 公告',
 '2606.03994': '旧稿 replace 再公告（首次入馆）：2606=2026-06 投稿，v2 于 2026-11-03 公告',
 '2603.07604': '旧稿 replace 再公告（首次入馆）：2603=2026-03 投稿，v3 于 2026-11-03 公告',
 '2607.18539': '旧稿 replace 再公告（首次入馆）：2607=2026-07 投稿，v2 于 2026-11-03 公告',
 '2606.01643': '旧稿 replace 再公告（首次入馆）：2606=2026-06 投稿，v2 于 2026-11-03 公告',
 '2608.00232': '旧稿 replace 再公告（首次入馆）：2608=2026-07 投稿，v2 于 2026-11-02 公告',
 '2603.16016': '旧稿 replace 再公告（首次入馆）：2603=2026-03 投稿，v4 于 2026-11-03 公告',
 '2606.26364': '旧稿 replace 再公告（首次入馆）：2606=2026-06 投稿，v3 于 2026-11-02 公告',
}
for pid, (tzh, track, imp, nov, tec, exp, per, trl, rep, grade, note) in S_BF.items():
    d = D[pid]
    BF.append(dict(id=pid, title='', title_zh=tzh, track=track,
        scores=dict(IMP=imp,NOV=nov,TEC=tec,EXP=exp,PER=per,TRL=trl,REP=rep), grade=grade,
        grade_note=note, evidence='FULL', level='L0',
        status='CURRENT', venue=d['venue'], announce='replace', tags=d['tags'],
        conclusion=d['conclusion'], problem=d['problem'], method=d['method'], experiments=d['experiments'],
        innovation=d['innovation'], limits=d['limits'], relation=d['relation'], repro=d['repro'], action=d['action'],
        value=val((imp,nov,tec,exp,per,trl,rep)), batch='backfill-1105',
        orig_window=BF_WINDOW[pid]))

# 原始英文标题（RSS）
rss = {json.loads(l)['base_id']: json.loads(l) for l in open('data/raw/2026-11-05.jsonl',encoding='utf-8') if l.strip()}
for p in MAIN + BF:
    p['title'] = rss[p['id']]['title']

MAIN.sort(key=lambda p: (-p['value'], -p['scores']['IMP'], -p['scores']['NOV'], p['id']))
BF.sort(key=lambda p: (-p['value'], -p['scores']['IMP'], -p['scores']['NOV'], p['id']))

# 定稿 Top10：主批 A/B 级 7 篇（C 级仅入馆不解读，低量日不凑数）。
# 值序：3DGS-VBench+ 3.99 > SettleSplat 3.85 > AR空间记忆 3.70 > Phase-DGS 3.65 > IGSW 3.65 > EndoS3 3.57 > ReconDreamer# 3.38。
# Phase-DGS 与 IGSW 同值同 IMP/NOV，按赛道多样性优先（SettleSplat 已占重建与SLAM）→ Phase-DGS 居前。
TOP10_IDS = ['2611.04498','2611.04195','2611.04494','2611.04666','2611.04374','2611.04358','2611.04173']
TOP10 = [p for pid in TOP10_IDS for p in MAIN if p['id'] == pid]
assert len(TOP10) == 7 and all(p['grade'] != 'C' for p in TOP10)

json.dump({'main': MAIN, 'backfill': BF, 'top10_ids': TOP10_IDS},
          open('data/scored_1105.json','w',encoding='utf-8'), ensure_ascii=False, indent=1)
print('main:', len(MAIN), 'bf:', len(BF))
for p in MAIN: print('M', p['id'], f"{p['value']:.2f}", p['grade'], p['track'], p['evidence'], p['title_zh'][:36])
for p in BF: print('B', p['id'], f"{p['value']:.2f}", p['grade'], p['track'], p['title_zh'][:36])
print('TOP10:', TOP10_IDS)
from collections import Counter
print('grades main:', dict(Counter(p['grade'] for p in MAIN)), 'bf:', dict(Counter(p['grade'] for p in BF)))
print('tracks top10:', dict(Counter(p['track'] for p in TOP10)))
print('tracks all main:', dict(Counter(p['track'] for p in MAIN)))
print('today_max:', MAIN[0]['value'])
print('saved data/scored_1105.json')
