# -*- coding: utf-8 -*-
"""组装 2026-11-07 评分数据：digest（4 子代理全文精读）+ 主会话 7 维评分定稿。
输出 data/scored_1107.json（main 23 篇，无 backfill——RSS 周六 skipDays 空源，无旧稿再公告可收）。
内联中文文本统一中文弯引号。
候选池：2026-11-06（周五）公告批次（拉取日 2026-11-07 周六 13:38）。
漏网对账（先于拉取）：listing 7 分类最新公告日均为 2026-11-06（11-05 组复采 0 漏网，
386 篇未入馆摘要级复核 10 篇命中均为 11-06 运行已剔非 XR，与上批清单逐篇一致）；
11-06 组 386 篇唯一论文（全部未入馆）摘要级 XR 命中 35 篇 = 23 XR + 12 非 XR。
数据源：API 双主机 200；RSS 7 分类 skipDays 空源（lastBuildDate 2026-11-07 05:00 UTC，WROTE=0），
本批以 listing 为唯一采集渠道（周末节律，已三源核验）；API published 口径核验提交日 11-04×5 / 11-05×30。
公告日 2026-11-06 ≠ 拉取日 2026-11-07 ≠ 提交日，全部产物显式标注。"""
import json

D = {}
for g in ('g1', 'g2', 'g3', 'g4'):
    for d in json.load(open(f'data/digest_1107_{g}.json', encoding='utf-8')):
        D[d['id']] = d

# 评分表：id -> (title_zh, track, IMP,NOV,TEC,EXP,PER,TRL,REP, grade, grade_note)
S_MAIN = {
 '2611.07902': ('XM4D：可证全局最优几何优化的 4D 重建', '重建与SLAM', 4,4.5,5,4.5,4.5,3.5,4, 'A',
   '达 S 线（4.36≥4.2）但非重磅日——当日最高 4.36 < 库内近 30 天 Top10 均分 4.393（窗口 2026-10-08~11-07、436 条入窗、现算），按校准关记 A（同 10-24 EgoHand/10-27 WFM/10-28 RacerGS 先例）'),
 '2611.07709': ('AffineGS：空间变化仿射矫正解锁 3DGS 几何精度', '神经渲染', 4,4,4.5,4.5,4.5,3.5,3.5, 'A', ''),
 '2611.08330': ('InstantHand：单图前馈可动画 3D 高斯手部化身重建', '化身与人体', 3.5,4,4.5,4.5,4,4,4.5, 'A', ''),
 '2611.08288': ('HIBS：面向在线重建的分层增量 Beta 泼溅', '重建与SLAM', 3.5,4,4.5,4.5,4,3.5,4, 'A', ''),
 '2611.07909': ('EDGAR：合成失败数据驱动的扩散式高斯化身高效精化', '化身与人体', 3.5,4,4.5,4.5,4,3.5,3.5, 'A', ''),
 '2611.08477': ('EgoGeneralist：视频原生建模统一第一视角动作-视频任务', '感知与认知', 4,4,4.5,4.5,4,3,2.5, 'A', ''),
 '2611.07049': ('Gaussolve：选择性溶解网格不一致内容的混合场景渲染（神经溶解场）', '神经渲染', 3.5,4,4,4,4,3.5,3.5, 'A', ''),
 '2611.07873': ('PVDepth：几何感知时空自适应的全景视频深度估计（含 PanoCARLA 数据集）', '感知与认知', 3.5,3.5,4,4,3.5,3.5,4, 'A', ''),
 '2611.07683': ('ReferClaw：以澄清提问消解用户意图的第一视角流式助手', '感知与认知', 3.5,3.5,4,4,4,2.5,2.5, 'B', ''),
 '2611.08398': ('柔软度与温度同步调制的多模态触觉显示（无泵颗粒堵塞+热皮肤）', '触觉与多模态', 3,3.5,4,3.5,3.5,3,2.5, 'B',
   '门②回补项：未覆盖核心赛道（触觉与多模态）B 级池最高分；库内触觉方向硬件增量（台式双模态显示）'),
 '2611.06974': ('T²-Splat：拓扑自适应与残差纹理解耦的三角形网格泼溅', '神经渲染', 3.5,3.5,4,4,3.5,3,3, 'B',
   '门②重筛剔除项：神经渲染赛道冗余（纯价值 Top10 中 3 篇）让位未覆盖赛道，仍入馆写 B 级笔记仅不占名额（同 11-04 SHield/11-06 BudgetSplat 先例）'),
 '2611.07386': ('Breaking the Modality Barrier：缺失模态鲁棒的晕动症多模态融合预测', '感知与认知', 3.5,3.5,4,4,3.5,2.5,3, 'B', ''),
 '2611.08436': ('SM4RT：先几何后运动的级联前馈 4D 重建', '重建与SLAM', 3.5,3.5,4,4,3.5,3,1.5, 'B', ''),
 '2611.07463': ('FREE-LIVO：免刚性 rig 与时间同步的紧耦合激光雷达-惯性-视觉里程计', '重建与SLAM', 3.5,3.5,4,3.5,3.5,3,2, 'B', ''),
 '2611.07979': ('P-MGS：感知优于几何——基于网格泼溅的高斯分配重思', '神经渲染', 3,3.5,4,3.5,3.5,3,2.5, 'B', ''),
 '2611.07345': ('Slide to Report：VR 晕动症症状特异的沉浸中连续报告（N=52）', '感知与认知', 3.5,3,3.5,4,3,2.5,3, 'B', ''),
 '2611.08301': ('REACT：骨骼运动信号的实时补全（S4 多候选融合）', '交互与输入', 3,3.5,3.5,3,3.5,3,2, 'B',
   '证据等级 PARTIAL：arXiv HTML 仅提供 Supplementary Material（主文问题陈述/训练细节/数据集名称缺失），ar5iv 无转换版；方法与实验描述基于补充材料实证，已在 7 维表与本报告显式声明'),
 '2611.07673': ('物体与视觉语言可供性引导的第一视角动作识别', '感知与认知', 3,3,3.5,3.5,3,2.5,2.5, 'B', ''),
 '2611.07687': ('Not Losing Your Way：按需创造视觉特征缓解 VIO 漂移的无人机主动框架', '重建与SLAM', 2.5,3.5,3.5,3.5,3,2.5,2, 'B', ''),
 '2611.07272': ('VREgo：用消费级 VR 头显采集第一视角演示学习机械臂操作', '交互与输入', 3,3,3.5,3,3,2.5,2.5, 'B', ''),
 '2611.08321': ('ControlAnything：编码智能体按需生成连接器与生成式 UI 的 MR 手部交互', '空间计算与UI', 3,3.5,2.5,2,3,2.5,4, 'C',
   '概念新鲜且开源，但证据强度弱（单会话、作者本人唯一佩戴者、n=10 请求、无用户研究），按 C 级入馆不解读'),
 '2611.07798': ('VocabulARy 2.0：生成式 AR 个性化 3D 记忆术词汇学习系统', '空间计算与UI', 2.5,3,2.5,2,2,2.5,2, 'C', ''),
 '2611.08167': ('Reflective Nature Experiences in VR：促进正念与减压的无障碍 VR 自然体验', '感知与认知', 2.5,2.5,2.5,2,2,2,1.5, 'C', ''),
}

def val(s):
    return round(0.20*s[0]+0.20*s[1]+0.15*s[2]+0.15*s[3]+0.15*s[4]+0.08*s[5]+0.07*s[6], 4)

MAIN = []
for pid, (tzh, track, imp, nov, tec, exp, per, trl, rep, grade, note) in S_MAIN.items():
    d = D[pid]
    ev = 'PARTIAL' if pid == '2611.08301' else 'FULL'
    MAIN.append(dict(id=pid, title='', title_zh=tzh, track=track,
        scores=dict(IMP=imp,NOV=nov,TEC=tec,EXP=exp,PER=per,TRL=trl,REP=rep), grade=grade,
        grade_note=note, evidence=ev, level='L0',
        status='CURRENT', venue=d['venue'],
        announce='new', tags=d['tags'],
        conclusion=d['conclusion'], problem=d['problem'], method=d['method'], experiments=d['experiments'],
        innovation=d['innovation'], limits=d['limits'], relation=d['relation'], repro=d['repro'], action=d['action'],
        value=val((imp,nov,tec,exp,per,trl,rep)), batch='2026-11-07'))

# 英文标题 + 摘要级 published（listing/摘要过滤产物）
hits = json.load(open('data/missed_xr_abstract_1107.json', encoding='utf-8'))
for p in MAIN:
    p['title'] = hits[p['id']]['title']
    p['published'] = hits[p['id']]['published']

MAIN.sort(key=lambda r: (-r['value'], -r['scores']['IMP'], -r['scores']['NOV'], r['id']))

# Top10 定稿（门②重筛后）：纯价值 Top10 覆盖 4 赛道（神经渲染×3/感知与认知×3/重建与SLAM×2/化身与人体×2）
# → 剔除神经渲染赛道最低分 T²-Splat 3.575（与 ReferClaw 同分，按赛道冗余度与库内增量定位取舍），
#   回补未覆盖核心赛道（触觉与多模态）B 级池最高分 多模态触觉显示 3.365 → 定稿 Top10 覆盖 5 赛道
TOP10_IDS = ['2611.07902', '2611.07709', '2611.08330', '2611.08288', '2611.07909', '2611.08477',
             '2611.07049', '2611.07873', '2611.07683', '2611.08398']
assert len(TOP10_IDS) == 10 and len(set(TOP10_IDS)) == 10
assert all(pid in {p['id'] for p in MAIN} for pid in TOP10_IDS)
tracks = [next(p for p in MAIN if p['id'] == pid)['track'] for pid in TOP10_IDS]
assert len(set(tracks)) >= 5, f'Top10 tracks: {tracks}'

json.dump(dict(main=MAIN, backfill=[], top10_ids=TOP10_IDS), open('data/scored_1107.json','w',encoding='utf-8'), ensure_ascii=False, indent=1)
print('main', len(MAIN), 'backfill 0')
for r in MAIN:
    print(f"  {r['value']:.4f} {r['grade']} {r['id']} {r['track']} {r['title_zh'][:42]}")
print('Top10 tracks:', {t: tracks.count(t) for t in set(tracks)})
