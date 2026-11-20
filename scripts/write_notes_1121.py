# -*- coding: utf-8 -*-
"""2026-11-21 产物：原子笔记 / 当日 MOC / backfill MOC / registry 幂等追加。"""
import glob, json, os, re, shutil, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from grade_caliber import assign_grade  # noqa: E402

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
os.chdir(ROOT)
DATE, MMDD = '2026-11-21', '1121'

D = json.load(open(f'data/scored_{MMDD}.json', encoding='utf-8'))
G = json.load(open(f'data/gates_{MMDD}.json', encoding='utf-8'))
MAN = json.load(open('data/fulltext/_manifest.json', encoding='utf-8'))
HEAVY = bool(G['gate3']['blockbuster'])
TOP10 = G['top10']

CONCL = {
 '2611.26625': '把流式几何基础模型与惯性基础模型前馈融合，得到跨平台、免调参、恒算力的度量 VIO：九数据集 APE 11.19→5.86 m，70 ms/帧出位姿，4798 帧吞吐不衰减。',
 '2611.26540': '用 DMD 蒸馏 + 逐 chunk 混合时间步 + RoPE 重索引把音频驱动说话人做成真流式：1.3B 单卡 20.7 fps（teacher 0.90 fps），FVD 195.5 反而优于 teacher 的 210.8。',
 '2611.26603': '单一网络同时给出锐利、时序一致、度量准确的深度：11 个数据集零样本平均排名第一，Jitter 1.39 对 π³ 2.13，1080p 流式 53 fps。',
 '2611.26493': '把前馈重建的稠密全局注意力换成「几何嵌入检索 + 块稀疏掩码」的稀疏注意力：1000 视图 26.1 s 对 DejaView 319.6 s（12.2×），AUC@30 仅降 1.9 点。',
 '2611.25338': '视频生成先验 + 可重光照神经高斯 + depth anchoring，首次从文本/单图产出可路径追踪重光照的完整资产：重光照 PSNR 25.47 对 LSRM 22.53，505 人偏好率 57.75%。',
 '2611.25279': '用 VIO 的度量位姿条件化深度基础模型、再以因子图融合子图，单目+IMU 即得在线稠密度量地图：EuRoC F@5cm 0.570 对 VGGT-SLAM 2.0 的 0.490。',
 '2611.26321': '把单光子三维重建写成「首交点」的凸问题序列，无需网络与逐场景非凸优化：三视角 MAE 0.90 mm（Transientangelo 2.60 mm），0.1 PPP 下仍可恢复表面。',
 '2611.26165': '流式双分支先验 + 无界因果生成把 Exo2Ego 做到 24.3 FPS（EgoX 0.08 FPS），PCK@0.05 37.49% 对 11.07%，FVD 136.48 对 438.79。',
 '2611.25925': '分层记忆 + 可编排视觉专家做定量空间推理，MetricBench 整体较最佳 VLM 提升 32%（室外 75.5% vs Gemini-3.1-Pro 40.3%）。',
 '2611.26072': '用散焦模糊作物理度量线索，单张 all-in-focus/defocused 图对即预测度量 3D 高斯：Booster AbsRel 0.075 对 UniDepth v2 的 0.230（−67.4%）。',
 '2611.25061': '用逆向生成建模反解生成模型潜变量，替代前馈模式匹配以提升 OOD 视角鲁棒性：CO3D CD 0.461 对 Splatter Image 0.733（−37%），代价是 ID 上略降。',
 '2611.25849': '8,453 题、约 324 小时的第一人称实例级空间记忆基准：最强闭源 73.56%、最强开源 46.97%，「谁最后看到」是最难能力（34.17%）。',
 '2611.25500': '单次前向预测物体的构型空间（拉格朗日广义坐标），使 4D 世界中的物体可实时按物理规律响应：Chamfer-L1 比 PhysSkin 低 60%、比 VBD 快 7.1×。',
 '2611.25979': '多视图修复 Transformer + 几何引导多模态 ControlNet 解决 3DGS 试穿的跨视角不一致：FID 24.1 对 GS-VTON 38.2（−36.9%），LPIPS −46.5%。',
 '2611.26516': '联合预测 RGB 与稠密 4D 几何（深度/相机/点云/场景流）的可规划世界模型：Epic-Kitchens 深度 AbsRel 0.0766 对 0.4201，训练帧数仅 0.97M。',
 '2611.25340': '智能体 + 工具链把单段视频重建成可编辑网格场景，显式重建协议约束布局/尺度/光照：新视角内容相似度 0.53（其余方法 ≤0.38）。',
 '2611.25801': '直接回归骨架关节与稠密表面点的人体估计器：39.2 fps（SAM 3D Body 8.5 fps）且 3DPW PA-MPJPE 32.7 mm 更优，并新增接触与场景任务。',
 '2611.25963': '富集局部形变模态，使弹簧物理孪生可独立控制体积与形状响应：泊松比误差降 75.8%、重建 PSNR 34.65 对 PhysTwin 31.12 dB。',
 '2611.25005': '给长时序人-场景交互智能体补上「空间控制」与「定量反馈」两个缺失接口：75 个任务完成 74（98.7%），最佳基线仅 26.7%。',
 '2611.25608': '在 VRChat 实证四种欺骗性 UI 攻击（83.3% / 86.7% 用户未察觉），并给出 5 s 扫描的静态检测器（攻击 UI 30/30 检出）。',
 '2611.25865': '把因果估计的几何编码注入 VLM 中间层、以 KV cache 当空间记忆，做流式主动空间推理：timely 71.8% / abstain 87.3%（SFT 基线 68.1/84.8）。',
 '2611.26511': '丢掉 VAE，在原生 SDF 体素上直接做扩散 Transformer：GSO 单视图 CD 0.0131（TRELLIS2 0.0147），但语义对齐指标仅与 SOTA 打平。',
 '2611.26431': '字形与 SVG 轮廓单次前向转成紧凑高斯资产，免去逐资产迭代优化：法向误差 1.618°（TexGaussian 1.957°），边缘带 8.98° 对 13.86°。',
 '2611.25696': '把语言控制图像融合从 2D 抬到自由视点 3D 场景：PSNR 13.54 对 ReCoFuse 11.98，重投影 MAE 降约 80%，跨视角一致。',
 '2611.25802': '以「可写单元预算 + 不确定性校准」做增量 3D 场景更新，兼顾校正与保留：ScanNet v2 / Replica 校正误差 0.160 / 0.120，保留误差增量更低。',
 '2405.15125': '双分支 HDR/LDR 高斯 + 可微色调映射，在约 1000× 推理加速下 HDR PSNR 38.31 dB（HDR-NeRF 36.40），训练仅需其 6.3% 时间。',
 '2611.25523': '按基光照训练共享几何 + 独立外观网络，参数线性合并即完成重光照：真实 OLATverse 24.35 dB 与 RNG 持平且 SSIM/LPIPS 更优。',
 '2611.25950': '高斯界面 + 传输耦合细化显式建模多层透明折射：同存储下落点误差降 95%–98.9%，几何仅 82.85 KiB（同输入网格的 1/25.8）。',
 '2611.26350': '把物理机器人实验室映射成持续同步的 VR 复制品并内置试次校验：30 人组内实验完成时间比 2D 快 27.7%，验证就绪率 +19.6 点。',
 '2611.24995': '284 段 Ray-Ban Meta 视频、2,201 题的「通行影响」基准：最强模型比两人人工基线低 23.65 个百分点，且能判物体运动却判不对通行约束（91.37% vs 66.50%）。',
 '2611.26045': '给解析表面对齐协方差加学习残差，使前馈高斯在不同渲染分辨率下都贴住表面：原生 256² 仅 +0.6%，8× 重渲 +4.0%。',
 '2611.25444': '800 段参考视频 + 100 个请求的化身讲解基准：语音/视觉事实精度 >98%，但指称准确率最高仅 49.85%，画质反低于 HeyGen。',
 '2611.26177': '100 户真实住宅、3,171 个目标的主动建图基准：最强 agent all-target mean IoU 仅 22.52%，IoU>0.9 占 0.19%。',
 '2611.25567': '指令条件 + 在线设定的程序性视频错误检测：含错集 86.2% F1@0.5（AEM 47.3%、ESTANet 27.0%），但监督条件不同不可直接比较。',
 '2611.26485': '开源 ROS 2 框架把 Haply Inverse3 力反馈接入 dVRK：20 人实验触点 −34.4%（p=.005, d=0.71）、完成时间 −22.1%。',
 '2611.25414': '在水密三角网格上联合优化几何与视角相关外观：DTU Acc 1.10 mm 最优，且是唯一同时流形/水密/无自交的输出（AR 1.19 vs 3.63）。',
 '2611.25445': '用稀疏度量路标标定稠密几何前馈模型的尺度偏移，再与因子图 VO 闭环：KITTI 01 百 meters RPE 7.12 m（DROID-SLAM 60.27 m）。',
 '2611.25934': '推理期多光圈渲染 + 不确定性融合做 GS 超分：2× 严重退化 +1.69 dB，但 4× 与 Bicubic 持平、缺消融，C 级仅入馆。',
 '2610.09195': '可微仿真 + 单静态手控从单张 RGB 重建物理稳定抓取：DexYCB 成功率 93.80%（学习式 D-Grasp 64.05%），跨模拟器仍领先。',
}


def esc(s):
    return str(s).replace('|', '/')


def slugify(t):
    return re.sub(r'[^a-z0-9]+', '-', t.lower()).strip('-')[:52]


def bullets(text):
    if isinstance(text, (list, tuple)):
        return '\n'.join(f'- {str(x).strip()}' for x in text if str(x).strip())
    parts = [x.strip() for x in re.split(r'[；。]', str(text)) if x.strip()]
    return '\n'.join(f'- {x}' for x in parts)


def tags_for(p, g):
    base = [p['track']]
    for kw in ['Gaussian', 'SLAM', 'VR', 'AR', 'haptic', 'tactile', 'avatar', 'world model',
               'diffusion', 'head-mounted', 'eye tracking', 'egocentric', 'depth', 'VIO', 'relight']:
        if kw.lower() in (p['title'] + ' ' + g.get('method', '')).lower():
            base.append(kw)
    return base[:5]


NOTE = '''---
id: arXiv:{id}
title: {title}
title_zh: {title_zh}
track: {track}
venue: {venue}
date: {date}
value: {value}
grade: {grade}
evidence: {evidence}
status: CURRENT
superseded_by: []
scores: {{IMP:{IMP}, NOV:{NOV}, TEC:{TEC}, EXP:{EXP}, PER:{PER}, TRL:{TRL}, REP:{REP}}}
fetch_level: {level}
batch: {batch}
announce_type: {announce}
in_top10: {in_top10}
published: {published}
recall: {recall}
tags: [{tags}]
---

# {title_zh}

## 一句话结论
{concl}

## 要解决的问题
{problem}

## 方法详解
{method}

## 实验与结果
{exp}

## 创新点与贡献
{nov}

## 局限与风险
{lim}

## 与文献库的关系
- 本批新增（batch `{batch}`，公告类型 `{announce}`），赛道「{track}」{rank}
- 本批 OUTDATED / SUPERSEDED 判定为 0，未发现直接取代关系。
- 公告日 2026-11-20（周五）≠ 拉取日 2026-11-21（周六 02:30）；API 首次提交日 {published}。
{note}

## 可复现性（代码/数据/硬件）
- 代码/项目页：{code}
- 全文证据：{evidence}（{level}，{chars:,} 字符）

## 行动建议
{action}
'''

os.makedirs('papers/notes', exist_ok=True)
n_notes = 0
for p in D:
    g = next((json.load(open(f'data/digest_1121_g{k}.json', encoding='utf-8')).get(p['id'])
             for k in range(1, 9)
             if json.load(open(f'data/digest_1121_g{k}.json', encoding='utf-8')).get(p['id'])), None)
    m = MAN[p['id']]
    p['level'] = m['level']; p['chars'] = m['chars']
    if p['grade'] == 'C':
        continue
    fn = f"papers/notes/{p['id']}__{slugify(p['title'])}.md"
    if os.path.exists(fn):
        print('skip', fn); continue
    rank = f"，本批 Top10 第 {TOP10.index(p['id'])+1} 名" if p['id'] in TOP10 else ''
    action = ('- 纳入重点精读：方法与实验节可直接支撑选题与技术选型。' if p['grade'] == 'A'
              else '- 浏览级：关注问题设定与结论，方法细节按需回看。')
    action += ('\n- 有公开代码/项目页，可先跑通再评估迁移成本。' if p.get('code') and p['code'] != '未提供'
               else '\n- 未提供代码，复现需按正文细节自行实现。')
    body = NOTE.format(
        id=p['id'], title=p['title'], title_zh=p['title_zh'], track=p['track'], venue=p['venue'],
        date=DATE, value=f"{p['value']:.2f}", grade=p['grade'], evidence=p['evidence'],
        IMP=p['scores']['IMP'], NOV=p['scores']['NOV'], TEC=p['scores']['TEC'], EXP=p['scores']['EXP'],
        PER=p['scores']['PER'], TRL=p['scores']['TRL'], REP=p['scores']['REP'],
        level=p['level'], batch=p['batch'], announce=p['announce'], in_top10=str(p['in_top10']).lower(),
        published=p['published'], recall=p.get('recall') or 'KW/TITLE', tags=', '.join(tags_for(p, g)),
        concl=CONCL[p['id']], problem=g['problem'], method=g['method'],
        exp=bullets('；'.join(g['key_results'])), nov=bullets(g['novelty']), lim=bullets(g['limitations']),
        rank=rank, note=(f"- 备注：{p['note']}" if p.get('note') else ''),
        code=(p.get('code') or '正文未提供'), chars=p['chars'], action=action)
    open(fn, 'w', encoding='utf-8').write(body)
    n_notes += 1
print('notes written', n_notes)

# ---------- MOC ----------
def moc(papers, path, title, intro):
    L = [f'# {title}\n', intro + '\n', '## 本批论文（按加权降序）\n',
         '| # | 论文 | 赛道 | 总分 | 等级 | 证据 | 笔记 |', '|---|---|---|---|---|---|---|']
    for i, p in enumerate(papers, 1):
        note = glob.glob(f"papers/notes/{p['id']}__*")
        link = f"[→](../notes/{os.path.basename(note[0])})" if note else '→（C 级仅入馆）'
        L.append(f"| {i} | {esc(p['title_zh'])} | {p['track']} | {p['value']:.2f} | {p['grade']} | {p['evidence']} | {link} |")
    L.append('\n## 批次要点\n')
    for p in papers:
        L.append(f"- **{esc(p['title_zh'])}**（{p['id']}，{p['value']:.2f} {p['grade']}）：{CONCL[p['id']]}")
    open(path, 'w', encoding='utf-8').writelines([x + '\n' for x in L])

MAIN = [p for p in D if not p['batch'].startswith('backfill')]
BF = [p for p in D if p['batch'].startswith('backfill')]
g3 = G['gate3']
moc(MAIN, f'papers/MOC/MOC-{DATE}.md', f'MOC · {DATE}（11-20 公告批次 · 规模化重建与实时感知）',
    '> 当日地图：**公告日 2026-11-20（周五）≠ 拉取日 2026-11-21（周六 02:30）**——诚实口径。'
    '主批 API published 核验：**11-19×33 / 11-18×4**（RSS published 为公告时间戳，不可当提交日）。\n'
    '> 主批 XR 新稿 **37 篇（0 S / 23 A / 13 B / 1 C）**，Top10 实数 10 篇最高 **4.43**（2611.26625 AnyVIO）；'
    '11-20 组 605 槽位 / **508 篇唯一**，RSS 783 条覆盖率 508/508、缺收 0 → 免 API id_list；'
    '摘要级 KW 命中 47 + 标题级补扫 30 = 77 → 逐篇核摘要剔 43 → 34 篇；残差复核再采纳 3 篇（2611.25696 / 2611.25802 / 2611.25801）→ 37 篇。\n'
    '> 全文：**39 篇 L0/FULL**（主批 37 + backfill 2，33,057–196,730 字符）。\n'
    '> 覆盖度三关：门① **0.238** / 门② **5 赛道**（一次重筛：剔 Infer3D 4.07、回补 DfD-GS 4.00）/ '
    '门③ **4.43 vs 4.4230**（现算，465 条入窗，半开窗口 [2026-10-22, 2026-11-21) 且按 batch 剔除本批两批）'
    '→ **margin +0.007 险过，不授 S**，6 篇 ≥4.20 一律记 A。')
moc(BF, f'papers/MOC/MOC-backfill-{MMDD}.md', f'MOC · backfill-{MMDD}（旧稿 v2/v3 再公告首次入馆）',
    '> **非当日新提交**：本批 2 篇均为 11-20 公告 RSS 混入的 replace 旧稿再公告'
    '（2405.15125 HDR-GS 首发 2024-05-24、2610.09195 StableGrasp 首发 2026-10-06），'
    '诚实口径单独编号，不参与当日重磅日判定，最高记 A。\n'
    '> 定稿 **1 A / 1 B（无 S）**：2610.09195 StableGrasp 4.08（单图人手抓取物理稳定化，DexYCB 93.80%）· '
    '2405.15125 HDR-GS 3.45（1000× 加速的 HDR 新视角合成，HDR PSNR 38.31 dB）。')
print('MOC written')

# ---------- registry ----------
reg = 'papers/library/registry.jsonl'
bak = f'papers/library/registry.jsonl.bak-2026{MMDD}'
if not os.path.exists(bak):
    shutil.copy(reg, bak); print('backup ->', bak)
rows = [json.loads(l) for l in open(reg, encoding='utf-8') if l.strip()]
have = {r['id'].split(':')[-1].split('v')[0] for r in rows}
added = 0
with open(reg, 'a', encoding='utf-8') as f:
    for p in D:
        if p['id'] in have:
            print('exists', p['id']); continue
        e = dict(id=f"arXiv:{p['id']}", title=p['title'], title_zh=p['title_zh'], track=p['track'],
                 date=DATE, value=p['value'], grade=p['grade'], scores=p['scores'], status='CURRENT',
                 evidence=p['evidence'], fetch_level=p['level'], fulltext_chars=p['chars'],
                 in_top10=p['in_top10'], batch=p['batch'], announce_type=p['announce'],
                 published=p['published'], flags=[])
        f.write(json.dumps(e, ensure_ascii=False) + '\n'); added += 1
total = len(rows) + added
print(f'registry +{added}（{len(rows)} -> {total}）')
print('notes', len(glob.glob('papers/notes/*.md')), 'daily', len(glob.glob('papers/daily/*')),
      'moc', len(glob.glob('papers/MOC/*.md')))
