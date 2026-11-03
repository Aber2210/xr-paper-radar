# -*- coding: utf-8 -*-
"""组装 2026-11-04 评分数据：digest（子代理全文精读）+ 主会话 7 维评分定稿。
输出 data/scored_1104.json（main 35 + backfill 8）。内联中文文本统一中文弯引号。
候选池：2026-11-03（周二）公告批次（覆盖 10-30~11-02 提交；listing 1000 篇摘要级 XR 命中 62 篇，
与 RSS 真新集合逐篇一致，两渠道互证）。backfill-1104：RSS 混入的旧稿 replace/cross 再公告中 8 篇 XR（首次入馆）。"""
import json

D = {}
for g in ('g1', 'g2', 'g3', 'g4'):
    for d in json.load(open(f'data/digest_1104_{g}.json', encoding='utf-8')):
        D[d['id']] = d

# 评分表：id -> (title_zh, track, IMP,NOV,TEC,EXP,PER,TRL,REP, grade, grade_note)
S_MAIN = {
 '2611.01534': ('AbacusGS：免逐 splat 排序的高斯泼溅', '神经渲染', 4,4,4,4,4,4,3, 'A', '',
   ),
 '2611.01543': ('GSExplorer：以持久化 3D 高斯世界状态进行交互式世界生成', '世界模型与仿真', 4,4,4,4,4,3,3, 'A', '',
   ),
 '2611.01627': ('EgoMo3R：第一视角运动与场景的联合重建', '化身与人体', 4,4,4,4,4,3,3, 'A', '',
   ),
 '2611.00375': ('MoRE-GS：面向未来高斯泼溅的运动机制专家路由', '神经渲染', 4,4,4,4,4,3,3, 'A', '',
   ),
 '2611.01937': ('Spade-SLAM：稀疏对应锚定的稠密自监督视觉 SLAM', '重建与SLAM', 4,4,4,4,4,3,3, 'A', '',
   ),
 '2611.02044': ('3D 高斯泼溅的统一损失感知密度控制', '神经渲染', 4,4,4,4,4,3,3, 'A', '',
   ),
 '2611.02051': ('UniGS-SLAM：几何与开放词汇语义增强的单目高斯 SLAM', '重建与SLAM', 4,4,4,4,4,3,3, 'A', '',
   ),
 '2611.02658': ('OctreeSplat：层次八叉树引导的前馈高斯泼溅', '神经渲染', 4,4,4,4,4,3,3, 'A', '',
   ),
 '2611.01162': ('SHield：经球谐系数微扰的 4D 高斯泼溅水印', '神经渲染', 3,4,4,5,4,3,3, 'A', '',
   ),
 '2611.03228': ('AnchorComplete：从部分点云恢复完整场景网格', '重建与SLAM', 4,4,4,4,4,3,2, 'A', '',
   ),
 '2611.02537': ('Virtual Box：机器人辅助手术中皮下目标定位的交互式 3D 剖面可视化', '空间计算与UI', 4,3,4,4,4,3,3, 'A', '门②赛道回补入选：纯值 Top10 仅覆盖 4 赛道，以本篇（空间计算与UI）替换同分冗余赛道论文后达 5 赛道',
   ),
 '2611.03062': ('MuCHMDPoser：面向 VR 的多视 RGB 相机全身姿态追踪', '化身与人体', 4,3,4,3,4,4,4, 'A', '',
   ),
 '2611.01939': ('VLSplat：经场景图的视觉-语言引导物体中心 3D 高斯泼溅', '神经渲染', 3,4,4,4,4,3,3, 'A', '',
   ),
 '2611.02767': ('GaussFlaw-80K 与 GeoCritic：3D 高斯泼溅的细粒度感知诊断', '评估与数据集', 3,4,4,4,3,3,4, 'B', '',
   ),
 '2611.03283': ('ReVA-HPE：以合成位姿监督与个性化虚拟锚点估计相对 6DoF 头姿', '感知与认知', 3,4,4,4,3,3,4, 'B', '',
   ),
 '2611.03646': ('EgoActionBench：第一视角人类视频稠密动作描述基准', '评估与数据集', 4,3,4,4,3,3,4, 'B', '',
   ),
 '2611.02034': ('SurgicalTS：单目视频动态内镜场景的 4D 三角形泼溅重建', '神经渲染', 3,4,4,4,3,3,2, 'B', '',
   ),
 '2611.03052': ('Selfrionette：驱动全身化身操控与多样触觉交互的指尖力输入控制器', '交互与输入', 3,4,4,4,3,3,3, 'B', '',
   ),
 '2611.03021': ('MetamorphX：经旋转阻抗控制改变物理特性的非接地 3-DoF 力矩显示器', '触觉与多模态', 3,4,4,3,3,3,2, 'B', 'UIST ’22 正式论文的 arXiv 作者版（非新成果），触觉硬件方向稀缺文献',
   ),
 '2611.00482': ('直线不是相机位姿：短片段位姿基准审计', '评估与数据集', 3,4,4,4,3,2,4, 'B', '',
   ),
 '2611.00898': ('以透明度换稳定性：摩擦锥约束的双边遥操作开启无固定家具门', '触觉与多模态', 3,3,4,4,4,3,2, 'B', '',
   ),
 '2611.03106': ('MISLAM：紧耦合的磁-惯性 SLAM 系统', '重建与SLAM', 3,3,3,3,4,2,2, 'B', '',
   ),
 '2611.03114': ('在自学习神经视图相关颜色场内的 3D 高斯泼溅', '神经渲染', 3,3,4,3,3,3,2, 'B', '',
   ),
 '2611.00356': ('拆解 360° 视频观看过程：生理反应与头部旋转如何关联情感与认知结果', '感知与认知', 3,3,4,4,2,2,3, 'B', '',
   ),
 '2611.02490': ('物理环境中的上下文信息如何影响人与 AI 的决策（AR 研究）', '感知与认知', 3,3,4,4,2,2,3, 'B', '',
   ),
 '2611.00509': ('MESSPa：可拆卸机器人臂中保持主体能动感的多模态体感刺激肩垫', '触觉与多模态', 3,3,3,3,3,2,2, 'C', '',
   ),
 '2611.00870': ('面向数字孪生的月面模拟场景可复现重建与评测框架', '重建与SLAM', 3,3,3,3,2,2,3, 'C', '',
   ),
 '2611.01495': ('Endless VR Walk：把有限物理空间动态映射为无限线性路径', '交互与输入', 3,3,3,2,2,3,3, 'C', '',
   ),
 '2611.03254': ('TRAILS：自动化室内移动研究的轨迹生成', '系统与平台', 3,3,3,2,2,3,4, 'C', '',
   ),
 '2611.02363': ('GEAR：面向 VR 旅行的场景条件穿搭检索生成式编辑', '内容生成', 2,3,3,3,2,2,2, 'C', '',
   ),
 '2611.03389': ('CrowdForge：AI 中介 MR 演出中观众参与模态对能动性、协作与投入的影响', '感知与认知', 2,3,3,3,2,2,3, 'C', '',
   ),
 '2611.01759': ('基于 VR 头显与姿态估计的服务机器人遥操作系统', '交互与输入', 3,2,2,2,2,3,2, 'C', '证据等级 L1/PARTIAL：ar5iv 仅摘要页，摘要级评估',
   ),
 '2611.01229': ('Precision Through Play：经游戏化 XR 与伪触觉增强腹腔镜基础技能训练', '感知与认知', 3,2,2,1,2,2,2, 'C', '证据等级 L1/PARTIAL：ar5iv 仅摘要页，摘要级评估',
   ),
 '2611.01361': ('跨越尺度推理：芯片设计教育中沉浸式技术的学习挑战与机遇', '空间计算与UI', 2,2,2,2,1,1,2, 'C', '',
   ),
 '2611.02447': ('DruMR：反馈驱动的混合现实空气架子鼓系统', '交互与输入', 2,2,2,1,1,2,2, 'C', '',
   ),
}

S_BF = {
 '2512.17541': ('FLEG：经紧凑语义表示的任意视角前馈语言嵌入高斯泼溅', '神经渲染', 3,4,4,4,4,3,2, 'B', '',
   ),
 '2603.22174': ('AR 引导机器人超声联合锥束 CT 用于脊柱操作的可行性', '空间计算与UI', 4,3,4,4,4,3,2, 'B', '',
   ),
 '2509.10759': ('4D 高斯光线追踪：基于物理的相机效应数据生成', '神经渲染', 3,4,4,3,4,3,2, 'B', '',
   ),
 '2606.18588': ('Splaxel：经像素级通信的高效分布式 3D 高斯泼溅训练', '系统与平台', 3,3,4,4,4,3,1, 'B', '',
   ),
 '2508.13537': ('EAvatar：以生成式几何先验进行表情感知的头部化身重建', '化身与人体', 3,3,4,3,3,3,2, 'B', '',
   ),
 '2511.20348': ('数字孪生 3D 世界重建中的材质感知高斯泼溅', '重建与SLAM', 3,3,3,3,2,3,2, 'C', '',
   ),
 '2607.20790': ('VR 的眼部验证', '感知与认知', 3,3,3,3,3,3,2, 'C', '',
   ),
 '2605.05155': ('Aes3D：3D 高斯泼溅的美学评估', '评估与数据集', 2,3,3,3,3,2,3, 'C', '',
   ),
}

def val(s):
    return round(0.20*s[0]+0.20*s[1]+0.15*s[2]+0.15*s[3]+0.15*s[4]+0.08*s[5]+0.07*s[6], 4)

MAIN, BF = [], []
ANNOUNCE_MAIN = {'2611.00509': 'cross', '2611.01162': 'cross', '2611.01229': 'cross', '2611.01534': 'cross'}
EVID = {'2611.01229': ('L1', 'PARTIAL'), '2611.01759': ('L1', 'PARTIAL')}
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
        value=val((imp,nov,tec,exp,per,trl,rep)), batch='2026-11-04'))
BF_WINDOW = {
 '2508.13537': '旧稿 replace 再公告（首次入馆）：2508=2025-08 投稿，v2 于 2026-11-03 公告',
 '2509.10759': '旧稿 replace 再公告（首次入馆）：2509=2025-09 投稿（NeurIPS 2025 Workshop），v2 于 2026-11-03 公告',
 '2511.20348': '旧稿 replace 再公告（首次入馆）：2511=2025-11 投稿，v2 于 2026-11-03 公告',
 '2512.17541': '旧稿 replace 再公告（首次入馆）：2512=2025-12 投稿，v3 于 2026-11-03 公告',
 '2603.22174': '旧稿 replace 再公告（首次入馆）：2603=2026-03 投稿（Healthcare Technology Letters），v2 于 2026-11-03 公告',
 '2605.05155': '旧稿 replace 再公告（首次入馆）：2605=2026-05 投稿，v5 于 2026-11-03 公告',
 '2606.18588': '旧稿 replace-cross 再公告（首次入馆）：2606=2026-06 投稿，v2 于 2026-11-03 公告',
 '2607.20790': '旧稿 replace 再公告（首次入馆）：2607=2026-07 投稿，v2 于 2026-11-03 公告',
}
for pid, (tzh, track, imp, nov, tec, exp, per, trl, rep, grade, note) in S_BF.items():
    d = D[pid]
    BF.append(dict(id=pid, title='', title_zh=tzh, track=track,
        scores=dict(IMP=imp,NOV=nov,TEC=tec,EXP=exp,PER=per,TRL=trl,REP=rep), grade=grade,
        grade_note=note, evidence='FULL', level='L0',
        status='CURRENT', venue=d['venue'], announce='replace', tags=d['tags'],
        conclusion=d['conclusion'], problem=d['problem'], method=d['method'], experiments=d['experiments'],
        innovation=d['innovation'], limits=d['limits'], relation=d['relation'], repro=d['repro'], action=d['action'],
        value=val((imp,nov,tec,exp,per,trl,rep)), batch='backfill-1104',
        orig_window=BF_WINDOW[pid]))

# 原始英文标题（RSS）
rss = {json.loads(l)['base_id']: json.loads(l) for l in open('data/raw/2026-11-04.jsonl',encoding='utf-8') if l.strip()}
for p in MAIN + BF:
    p['title'] = rss[p['id']]['title']

MAIN.sort(key=lambda p: (-p['value'], -p['scores']['IMP'], -p['scores']['NOV'], p['id']))
BF.sort(key=lambda p: (-p['value'], -p['scores']['IMP'], -p['scores']['NOV'], p['id']))

# 定稿 Top10：按加权降序取前十（同分 IMP/NOV 降序、赛道多样性优先、id 升序）。
# 纯值前十 = 3.93 AbacusGS + 七篇 3.85 + 3.80 SHield + 3.78 AnchorComplete，仅覆盖 4 赛道
# （神经渲染×5 / 重建与SLAM×3 / 世界模型与仿真×1 / 化身与人体×1）→ 门②未过；
# 按赛道多样性回补：以 3.65 的 Virtual Box（空间计算与UI）替换同赛道冗余的 SHield（3.80），
# 回补后 Top10 覆盖 5 赛道：神经渲染×4 / 重建与SLAM×3 / 世界模型与仿真×1 / 化身与人体×1 / 空间计算与UI×1。
TOP10_IDS = ['2611.01534','2611.01543','2611.01627','2611.00375','2611.01937','2611.02044',
             '2611.02051','2611.02658','2611.03228','2611.02537']
TOP10 = [p for pid in TOP10_IDS for p in MAIN if p['id'] == pid]
assert len(TOP10) == 10 and all(p['grade'] != 'C' for p in TOP10)

json.dump({'main': MAIN, 'backfill': BF, 'top10_ids': TOP10_IDS},
          open('data/scored_1104.json','w',encoding='utf-8'), ensure_ascii=False, indent=1)
print('main:', len(MAIN), 'bf:', len(BF))
for p in MAIN: print('M', p['id'], f"{p['value']:.2f}", p['grade'], p['track'], p['announce'], p['evidence'], p['title_zh'][:38])
for p in BF: print('B', p['id'], f"{p['value']:.2f}", p['grade'], p['track'], p['title_zh'][:38])
print('TOP10:', TOP10_IDS)
from collections import Counter
print('grades main:', dict(Counter(p['grade'] for p in MAIN)), 'bf:', dict(Counter(p['grade'] for p in BF)))
print('tracks top10:', dict(Counter(p['track'] for p in TOP10)))
print('tracks all main:', dict(Counter(p['track'] for p in MAIN)))
print('today_max:', MAIN[0]['value'])
print('saved data/scored_1104.json')
