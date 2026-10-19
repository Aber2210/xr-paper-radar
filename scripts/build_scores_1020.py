# -*- coding: utf-8 -*-
# build_scores_1020.py — 2026-10-20 批次评分数据（主批次 12 篇 + backfill 8 篇）。
# 口径：7 维 IMP0.20/NOV0.20/TEC0.15/EXP0.15/PER0.15/TRL0.08/REP0.07；S>=4.2 / A3.6-4.2 / B3.0-3.6 / C<3.0。
# 全部 20 篇均 L0/FULL（先抓全文再定稿）。
import json

W = {'IMP': 0.20, 'NOV': 0.20, 'TEC': 0.15, 'EXP': 0.15, 'PER': 0.15, 'TRL': 0.08, 'REP': 0.07}

MAIN = [
 # id, title_en, title_zh, track, date, (IMP,NOV,TEC,EXP,PER,TRL,REP)
 ('2610.23772', 'Video Diffusion Avatars: Taming Video Diffusion Models into Controllable 3D Avatars',
  '视频扩散化身：将视频扩散模型驯化为可控 3D 化身', '化身与人体', '2026-10-16', (4,5,5,5,5,3,4)),
 ('2610.22778', 'Direct Conditional Parameterization for N-Dimensional Splatting',
  'N 维泼溅的直接条件参数化（dGS/dBS）', '神经渲染', '2026-10-16', (4,4,5,5,5,3,3)),
 ('2610.23039', 'Frame-Consistent Feed-Forward 3D Gaussian Splatting from Sparse Unposed Images',
  '稀疏无位姿图像的帧一致前馈 3D 高斯泼溅', '神经渲染', '2026-10-16', (4,4,4,4,4,4,3)),
 ('2610.23050', 'TriFold: Folding irregular 3D Gaussians into structured latents for 3D Scene Generation',
  'TriFold：将不规则 3D 高斯折叠为结构化潜空间用于 3D 场景生成', '内容生成', '2026-10-16', (4,4,4,4,4,3,3)),
 ('2610.22681', 'EgoP2C: Internalizing Plan-Perceive-Compose for Spatial Reasoning in Egocentric Video',
  'EgoP²C：将规划-感知-组合内化于第一视角视频空间推理', '感知与认知', '2026-10-15', (4,4,4,4,4,3,3)),
 ('2610.23496', 'FLoTS-SLAM: Optical Flow-Derived Uncertainty for Monocular Dynamic SLAM with Two-Stage Optimization',
  'FLoTS-SLAM：光流衍生不确定度的单目动态 SLAM 两阶段优化', '重建与SLAM', '2026-10-16', (4,4,4,4,4,3,3)),
 ('2610.22822', 'VISTA: A Multimodal Egocentric Benchmark for Goal-Oriented Perception and Assistance to Blind and Low-Vision Users',
  'VISTA：面向盲人与低视力用户目标导向感知与协助的多模态第一视角基准', '评估与数据集', '2026-10-16', (4,4,4,4,3,3,3)),
 ('2610.23833', 'Sensory Comfort Across Multisensory XR Prototypes for Autistic Adults',
  '自闭症成人多感官 XR 原型的感官舒适度研究', '感知与认知', '2026-10-16', (4,3,4,4,3,3,4)),
 ('2610.23336', 'Wait for It: A Component-Level Analysis of Latency Feedback Mechanisms for LLM Agents in VR',
  'Wait for It：VR 中 LLM 智能体延迟反馈机制的组件级分析', '交互与输入', '2026-10-16', (4,3,4,4,3,3,3)),
 ('2610.22748', 'ElectroCalm: Investigating User Experience and Physiological Responses to Multi-Node Transcutaneous Electrical Stimulation for Stress Modulation',
  'ElectroCalm：多节点经皮电刺激压力调节的用户体验与生理响应研究', '触觉与多模态', '2026-10-15', (3,3,4,4,3,3,4)),
 ('2610.22878', 'Immersive Focus+Context Techniques to Assist in Interpretation of High Density Forest Point Clouds',
  '沉浸式聚焦+上下文技术辅助高密度森林点云解读', '空间计算与UI', '2026-10-16', (3,3,4,4,3,3,4)),
 ('2610.22720', 'HilbertGen-3D: Hilbert-Multifractal Conditioning for Topology-Aware 3D Generation',
  'HilbertGen-3D：拓扑感知 3D 生成的希尔伯特-多重分形条件化', '内容生成', '2026-10-15', (3,4,4,3,3,3,2)),
]

BACKFILL = [
 ('2602.07891', 'SAGE: Scalable Adaptation of 3D Geometric Foundation Models via Weak Supervision from Internet Video',
  'SAGE：互联网视频弱监督扩展 3D 几何基础模型', '重建与SLAM', '2026-02-08', (4,4,4,4,5,3,3)),
 ('2602.11693', 'OMEGA-Avatar: One-shot Modeling of 360-Gaussian Avatars',
  'OMEGA-Avatar：360° 高斯化身的单图建模（TOG）', '化身与人体', '2026-02-12', (4,4,4,4,4,4,4)),
 ('2610.21297', 'GeoPano: Towards Geometrically Accurate 3D Reconstruction from a Single Panorama',
  'GeoPano：单幅全景图的几何精确 3D 重建', '重建与SLAM', '2026-10-15', (4,4,4,4,4,3,3)),
 ('2605.25563', 'CodecSplat: Ultra-Compact Latent Coding for Feed-Forward 3D Gaussian Splatting',
  'CodecSplat：前馈 3D 高斯泼溅的超紧凑潜编码', '神经渲染', '2026-05-25', (4,4,4,4,4,3,3)),
 ('2604.00852', 'PanoAir: A Panoramic Visual-Inertial SLAM with Cross-Time Real-World UAV Dataset',
  'PanoAir：全景视觉惯性 SLAM 与跨时段真实无人机数据集', '重建与SLAM', '2026-04-01', (3,4,4,4,4,4,4)),
 ('2604.02107', 'HyVGGT-VO: Hybrid Dense Visual Odometry With Classical VO and Feed-Forward Model',
  'HyVGGT-VO：经典 VO 与前馈模型混合的稠密视觉里程计（IEEE LRA）', '重建与SLAM', '2026-04-02', (4,3,4,4,3,4,4)),
 ('2608.15060', 'EgoTac: In-the-wild Tactile Prediction from Egocentric Vision',
  'EgoTac：从第一视角视频预测真实场景触觉信号', '触觉与多模态', '2026-08-15', (3,3,4,4,4,3,4)),
 ('2606.28637', 'PinNet: Keypoint-Aware Learned Local Descriptors with Geometric Embedding for Loop Closure in LiDAR SLAM',
  'PinNet：LiDAR SLAM 回环的关键点感知学习描述子', '重建与SLAM', '2026-06-26', (3,3,4,4,4,3,3)),
]

CHARS = {'2610.22681':112505,'2610.22720':66738,'2610.22748':118689,'2610.22778':96804,
         '2610.22822':105308,'2610.22878':70867,'2610.23039':45271,'2610.23050':104080,
         '2610.23336':56174,'2610.23496':50541,'2610.23772':96505,'2610.23833':92883,
         '2610.21297':45788,'2602.07891':103963,'2602.11693':77941,'2604.00852':63669,
         '2604.02107':67754,'2605.25563':74550,'2606.28637':48980,'2608.15060':114968}


def value(s):
    return round(sum(W[k] * s[k] for k in W), 3)


def grade(v):
    return 'S' if v >= 4.2 else ('A' if v >= 3.6 else ('B' if v >= 3.0 else 'C'))


def build(rows):
    out = []
    for bid, ten, tzh, track, date, sc in rows:
        s = dict(zip(('IMP', 'NOV', 'TEC', 'EXP', 'PER', 'TRL', 'REP'), sc))
        v = value(s)
        out.append({'id': bid, 'title': ten, 'title_zh': tzh, 'track': track, 'date': date,
                    'IMP': s['IMP'], 'NOV': s['NOV'], 'TEC': s['TEC'], 'EXP': s['EXP'],
                    'PER': s['PER'], 'TRL': s['TRL'], 'REP': s['REP'],
                    'value': v, 'grade': grade(v), 'evidence': 'FULL', 'level': 'L0',
                    'chars': CHARS[bid], 'status': 'CURRENT'})
    out.sort(key=lambda x: (-x['value'], -x['IMP'], -x['NOV'], x['id']))
    return out


main = build(MAIN)
bf = build(BACKFILL)
json.dump(main, open('data/scored_1020.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
json.dump(bf, open('data/scored_backfill_1020.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
for name, rows in (('MAIN', main), ('BACKFILL', bf)):
    print(f'=== {name} ({len(rows)}) ===')
    for i, s in enumerate(rows, 1):
        print(f"  {i}. {s['id']} {s['value']:.2f} {s['grade']} {s['track']} {s['title_zh'][:38]}")
