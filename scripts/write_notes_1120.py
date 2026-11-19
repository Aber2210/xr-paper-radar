# -*- coding: utf-8 -*-
"""2026-11-20 产物：原子笔记 / 当日 MOC / backfill MOC / registry 幂等追加。"""
import glob, json, os, re, shutil, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from grade_caliber import assign_grade  # noqa: E402

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
os.chdir(ROOT)
DATE, MMDD = '2026-11-20', '1120'

D = json.load(open(f'data/scored_{MMDD}.json', encoding='utf-8'))
DIG = {}
for g in range(1, 6):
    DIG.update(json.load(open(f'data/digest_1120_g{g}.json', encoding='utf-8')))
G = json.load(open(f'data/gates_{DATE}.json', encoding='utf-8'))
MAN = json.load(open('data/fulltext/_manifest.json', encoding='utf-8'))
HEAVY = bool(G['gate3']['blockbuster'])
TOP10 = [r['id'] for r in D if r['in_top10']]

CONCL = {
 '2611.23417': '放弃显式 3D 表示，把场景生成为沿相机路径展开的「视角流」并用检索式有界上下文维持一致性：回访 PSNR 28.04，对比世界模型基线 10.12–12.29，相机可控性 70.67 对 3.91。',
 '2611.24805': '端侧轻量编码 + 后台重解码的非对称 RAW 联合压缩复原，在 Rokid Glass 真机实测，SIDD 0.25 bpp 下达 52.90 dB，BD-rate 相对最强级联 VVC+NAFNet 降低 70.5%。',
 '2611.23670': '首个把 OCT、解剖点云与近眼图像压进同一 latent 的 3D 眼睛生成与仿真模型，纯合成数据训练的眼动 E50 降到 3.53°（oracle 2.59°）。',
 '2611.23575': '3.5 mm 厚、全件开源的光学 taxel 阵列，用彩色硅胶壁把剪切编码进色度，实现每点三轴力感知；插销入孔成功率 40%→87%（n=15）。',
 '2611.23736': '把持续学习闭环下沉到每个 3D 高斯基元，用同一学习权重同时控制参数更新与 Adam 记忆刷新，14 场景平均 +3.41 dB 且不遗忘旧场景。',
 '2611.23871': '把双手与多物体放进同一 MuJoCo 动力学联合反解，物体间载荷成为指尖力约束，单视角 RGB-D 即可重建手物交互力（MAE 1.020 N，较 HOPE 降约 24.5%）。',
 '2611.23935': '首个实时三角泼溅 SLAM：tracker 只定位质心、mapper 在非平移子空间优化，RGB-D 下 113 FPS（Jetson 36 FPS），Delaunay chamfer 1.55→0.86 cm。',
 '2611.24938': '几何与时空双教师蒸馏 + 因果 CS-VAE 的场景结构表征，LIBERO-Plus 94.8%、RoboTwin 2.0 C2R 72.4%，跨具身迁移优于 InternW0-Δ。',
 '2611.23554': '按层统计「均值 token 的注意力质量亏空」逐层选估计器：弥散层用无偏 hub、匹配层保持精确，100 视角下 2.0× 加速仅损 1.38 AUC@5。',
 '2611.23513': '沿自身射线平移而非缩放来消除焦距导致的深度偏置，再做横向各向异性极大似然融合；最坏情形误差 284.3→56.0 mm，免训练、53 ms。',
 '2611.24941': '把 VLM 中间层材质 token 与受控光渲染表征对齐引入 PBR 生成，补上 metallic-roughness 的语义与物理监督，FID 144.3 且专家评分优于五家商用产品。',
 '2611.24193': '把世界状态从生成器里搬出来，由 MLLM 写「全景 + 修订历史」，使回访与局部编辑的一致性按构造成立（摘要自述 Epipolar 91.5 vs ≤74.0）。',
 '2611.24616': '把 VLM 对候选帧的标签概率整体当作时间先验、用 W1 最优分位数放帧，免训练即把 QAEgo4D 从 51.2% 提到 62.0%。',
 '2611.23994': '把 warp 后的源图注入预训练生成器的初始噪声相位（DT-CWPT 局部分解），不改架构即约束极线与遮挡区，Hard covisible +0.84 dB、比 MetaView 快 2.1×。',
 '2511.18173': '首个 3D 全身姿态可控的自我中心视频生成：差分头部 + pelvis 相对关节表示，AdaLN 与 cross-attn 双通路注入，FID 50.68 对 PEVA 61.10。',
 '2611.23939': '17 人 2×2 真机实验：头部引导相机比手柄快约 31%、墙面碰撞代价低 54%，视点控制方式比移动模态更能解释绩效差异。',
 '2611.24731': '首个统一人手、仿真灵巧手与真机灵巧手的世界模型基准（500 案例、17 指标 6 维），揭示姿态控制与物体状态演化背离（ρ=−0.34）。',
 '2611.23970': '把「物体」与「操作」因式分解推理、再做有序自适应阶段与阶段级几何子目标，三个基准七配置 ADE 最优，领先 Uni-Hand 7%–23%。',
 '2611.23450': '三路（直接透射/后向散射/前向散射）水下成像 + 可证明有界的反演 + 10 参数可逆物理锚，SAJALA 上 PSNR 24.755、深度 AbsRel 0.091 均为最优。',
 '2611.24404': '用偏振法线经 log-depth 积分与 TSDF 融合得到稠密深度先验，再按主曲率自适应布点初始化 2DGS，优化时间 21.3→4.3 分钟。',
 '2611.24565': '用光源身份化的 LRM 记忆与六项解耦 rubric 把「几何错」与「光照错」分开，32 图 PSNR 15.03 dB（VIGA 14.28），29 人偏好率 61.9%。',
 '2607.08514': '用实体掩码与 HDA 解码器迫使自我中心 VLM 同时学手与物体线索，并给出像素级线索隔离基准 DEHOI；揭示「纯 ego 数据训练→手偏置」的实证。',
 '2611.23416': '用光流引导的锚点重分配 + 同组内运动传播 + 刚体运动条件残差，提升流式 3DGS 的对象边界一致性，但相对 IGS 仅 +0.17–0.20 dB。',
 '2611.24207': '免训练 GPIS + 接触自估截面先验，从稀疏触觉接触补全物体网格，6 个真实物体 CD 1.610 mm / F-Score 95.00。',
 '2611.23825': '以技能基元 + 任务奖励构建 VR 对练 NPC 的武术动作库，8 名从业者评分 5.6/5.3，但无基线、无消融、对手仍为离线片段 + 状态机。',
 '2611.23534': '163 篇语料、14 个平台、10 个数据集的四层分类法综述，梳理智能眼镜在泛在计算中的系统栈与七项未来方向。',
 '2611.24334': '13 位专家 + 12 位开发者的形成性研究，提出「头部只给上下文、手动才触发」的可逆语义代码大纲，属设计探索而非绩效验证。',
 '2606.07179': '用演化树把离散分层换成连续分层、以小波式不对称残差让细层修正祖先，冗余率 65.83%→24.92%、存储 −33.6~−53.3%，PSNR 仅 +0.31 dB。',
}

def esc(s):
    return str(s).replace('|', '/')

def slugify(t):
    return re.sub(r'[^a-z0-9]+', '-', t.lower()).strip('-')[:52]

def bullets(text):
    parts = [x.strip() for x in re.split(r'[；。]', text) if x.strip()]
    return '\n'.join(f'- {x}' for x in parts)

def tags_for(p, g):
    base = [p['track']]
    for kw in ['Gaussian', 'SLAM', 'VR', 'AR', 'haptic', 'tactile', 'avatar', 'world model',
               'diffusion', 'head-mounted', 'eye tracking', 'egocentric', 'compression']:
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
    g = DIG[p['id']]
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
    action += ('\n- 有公开代码/项目页，可先跑通再评估迁移成本。' if p.get('code') and p['code'] != 'none'
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
moc(MAIN, f'papers/MOC/MOC-{DATE}.md', f'MOC · {DATE}（11-19 公告批次 · 端侧 AR 成像与场景表示）',
    '> 当日地图：**公告日 2026-11-19（周四）≠ 拉取日 2026-11-20（周五 02:30）**——诚实口径。'
    '主批 API published 核验：**11-17×8 / 11-18×17**（RSS published 为公告时间戳，不可当提交日）。\n'
    '> 主批 XR 新稿 **25 篇（0 S / 17 A / 5 B / 3 C）**，Top10 实数 10 篇最高 **4.33**（2611.23417 AVM）；'
    '11-19 组 599 槽位 / **502 篇唯一**，RSS 753 条覆盖率 502/502、缺收 0 → 免 API id_list；'
    '摘要级 KW 命中 52 + 标题级补扫 16 = 68 候选 → 逐篇核摘要剔 43 → 22 篇；'
    '第 3.5 步残差复核再采纳 3 篇（2611.23417 / 2611.23534 / 2611.24193）→ 25 篇。\n'
    '> 全文：**28 篇全部 FULL**（主批 25 + backfill 3；2611.24193 arXiv HTML 缺正文，按 PARTIAL 评估并显式声明）。\n'
    '> 覆盖度三关：门① **0.072** / 门② **7 赛道**（未重筛）/ 门③ **4.33 vs 4.4230**（现算，457 条入窗，'
    '半开窗口 [2026-10-21, 2026-11-20) 且按 batch 剔除本批两批）→ **非重磅日，无 S**（margin −0.093）。\n'
    '> Top10：AVM 4.33 · Edge RAW 4.30 · EyeDiT 4.28 · LuxTac 4.22 · GaussLearner 4.15 · HOForce 4.15 · '
    'Facet-SLAM 4.15 · Phoenix 4.15 · LMSA 4.00 · Trust the Ray 3.93。')
moc(BF, 'papers/MOC/MOC-backfill-1120.md', 'MOC · backfill-1120（旧稿 v2 再公告首次入馆）',
    '> **非当日新提交**：本批 3 篇均为 11-19 公告 RSS 混入的 replace 旧稿 v2 再公告'
    '（2511.18173 首发 2025-11-22、2606.07179 首发 2026-06-05、2607.08514 首发 2026-07-09），'
    '诚实口径单独编号，不参与当日重磅日判定，最高记 A。\n'
    '> 定稿 **2 A / 1 B（无 S）**：2606.07179 EvoGS 4.05（演化树连续分层 3DGS 流式，存储 −33.6~−53.3%）· '
    '2511.18173 EgoControl 3.77（3D 全身姿态可控自我中心视频生成）· 2607.08514 CI-HOI 3.45（自我中心 VLM 的手/物线索隔离基准）。')
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
                 in_top10=p['in_top10'], batch=p['batch'], announce_type=p['announce'], flags=[])
        f.write(json.dumps(e, ensure_ascii=False) + '\n'); added += 1
total = len(rows) + added
print(f'registry +{added}（{len(rows)} -> {total}）')
print('notes', len(glob.glob('papers/notes/*.md')), 'daily', len(glob.glob('papers/daily/*')), 'moc', len(glob.glob('papers/MOC/*.md')))
