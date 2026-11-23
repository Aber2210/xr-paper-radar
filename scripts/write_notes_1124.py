# -*- coding: utf-8 -*-
"""2026-11-24 产物：原子笔记 / 当日 MOC / backfill MOC / registry 幂等追加。"""
import glob, json, os, re, shutil, sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
os.chdir(ROOT)
DATE, MMDD = '2026-11-24', '1124'

D = json.load(open(f'data/scored_{MMDD}.json', encoding='utf-8'))
G = json.load(open(f'data/gates_{MMDD}.json', encoding='utf-8'))
MAN = json.load(open('data/fulltext/_manifest.json', encoding='utf-8'))
TOP10 = G['top10']

DIG = {}
for k in range(1, 5):
    for r in json.load(open(f'data/digest_{MMDD}_g{k}.json', encoding='utf-8')):
        DIG[r['id']] = r

CONCL = {
 '2611.26744': '把触觉 VLA 的适配与滑移门控全部压在纯前向路径上（Forward-Forward + 零阶），冻结 4-bit 骨干：LIBERO 97.6% 追平反传，峰值显存仅 334 MB（1/7.12）、延迟 58.8 ms（1/2），滑移门控夹持力 0.77 N 对 reflex ramp 22.43 N（1/29）。',
 '2611.27290': '用同参考系实测手腕位姿给潜动作瓶颈做监督、把头动作为独立条件交给前向模型，并用对抗与 warp 一致性把相机运动挤出码中：LIBERO 三套件 79.38%（比专家 BC 高 28.73 点），首次给出 AD/IC 两项可诊断「潜动作是否真装了运动」的第一视角指标。',
 '2611.27963': '首次把非穿透写成无几何世界模型上的约束问题，并证明生成器隐状态已含碰撞信息：六个模型平均违规率 74%→16%（LingBot 89%→4%），Pred 模式每条仅多 0.7 s 而原始后处理要 53.7 s。',
 '2611.21057': '把触觉与腕部视觉在策略注入前融合成连续接触表示，并用掩码视觉恢复与力旋响应预测约束该表示：GR00T N1.7 四任务 66.3%（纯视觉 37.5%、无腕部变体 47.5%），π0.5 58.8%，USB 拔出 95% 对 50%。',
 '2611.26764': '把「已标定手 + 空间分离的实测接触」当物理卡尺，无模板、无深度、无训练即破解单目尺度—深度歧义：ARCTIC ADD-S* 3.6 cm（最近基线 15.6 cm）、相对尺度误差 4.0%（SAM 3D 先验 12.0%）。',
 '2611.26981': '把逐视角生成与跨视角交互解耦、用块间共享 slot 取代拼贴与全注意力：变数量变顺序相机下仍保持一致，3 视角 FVD 25.41 对 32.93、真机 Franka 闭环 67.5% 对 30.0%。',
 '2611.26779': '首个完全不用深度输入的多视角 3D 点跟踪器，靠解码器内跨视角查询注意力与几何推导 scene scale 同时解决深度依赖与跨数据集尺度归一化：Panoptic AJ 86.5，已超带 GT 深度的 MVTracker（84.2）。',
 '2611.26883': '把「视觉可答性」做成基准里的受控变量，从而把「缺触觉」与「任务难」分开：四个 VLM 在不可见物理属性上 Tier B 相对准确率仅 49.8%（近随机），而可解释统计量的文本接口零样本即 62.9%、留一被试微调后 73.1%。',
 '2611.26916': '首个单设备逐 session 在线标定、同时带度量头部位姿与 3D 手部标注的万小时级职业操作自我中心语料：10,000 h / 137.8 万 episodes，ATE 中位 3.0 mm、手部 PA-MPJPE 4.5 mm，并保留原始多视角流使标注可审计重估。',
 '2611.27525': '不靠单点 kernel 优化，而是逐阶段消除「冗余像素 / 冗余字节 / 冗余 pass」：RTX 3060 上全分辨率 Mip-NeRF 360 单场景 6m25s（LiteGS 34m08s，3.9–5.8×），平均峰值显存仅 1.04 GB。',
 '2609.08848': '把实例感知与物体级生成合成一条前馈批处理流水线，用层级压缩潜表示让多物体并行解码在单卡可行：2.66 s/物体（Boxer 136.24 s）、iTHOR 重建 CD 1.38 cm（SAM3D 4.63 cm）。',
 '2607.02921': '首个同时满足自然第一视角、标定深度加位姿、定量问答的可穿戴基准，并主张用几何工具调用而非把三维塞进输入：平均相对精度 55.6%（次优 47.7%），与 GPT-5.5 的 59.1% 仅差 3.5 点。',
 '2611.26730': '一套权重同时服务深度相机与 LiDAR 的体素级人体网格模型，单帧精度即超过已发表的 32 帧序列方法：SLOPER4D 关节误差 28.6 mm（BMLiCap 36.5 mm，降 22%）。',
 '2611.26783': '把多率滤波落到 SMPL-X 旋转空间的逐关节逐帧核选择，首次量化「平滑是否把手速抹掉」：加速度误差 17.4→5.4 mm/s²，手语手速峰值幅度 0.98 对通用平滑器 0.35。',
 '2611.27101': '首个真实采集、带关节化 3D 手部标注的第一视角开放手术训练基准：现有最强手部模型在该域零样本 PA-MPJPE 24.99 mm、MediaPipe 检出率仅 24.1%，换到该域微调后降到 10.4 mm。',
 '2611.27459': '首次把协作者间的视觉视角采择表述为 ego 到 ego 的条件视频生成（无外部相机、无协作者图像或姿态），用共享 3D 场景坐标 + 跨视角 ray-space 注意力 + 他视角视觉记忆注入任意视频扩散骨干：PSNR 提升 1.19–2.50 dB、布局 mIoU 15.9→20.7。',
 '2605.19889': '把 3DGS 的显式局部基元范式搬到色彩空间：Hald 图 PSNR 45.47 dB（NILUT 38.84 dB）而参数只有 716（1/47），并保留局部可编辑性。',
 '2611.26773': '把区域 PCA 明确定位为绕开 N−1 秩上限的数据效率机制而非仅编辑便利：held-out 中性拟合 0.23 mm（全局 PCA 1.95 mm，8.3×），身份系数容量 11,072 对 346。',
 '2611.27845': '把安全约束从离线规划改成随目标切换、随站位重建的运行时最小干预过滤，安全指令原样通过而非一律减速急停：真机 10/12 轮完成、12 轮零非目标驱动，QP 求解均值 0.5 ms。',
 '2611.27915': '首个显式利用标定双目几何、以视差为中间监督的双目 VLM：深度 δ1 95.17%、视差 MAE 3.76 px，物体级均分超出 GPT-6 Astra 19.37 点，并给出「视差监督比直接深度监督泛化更好」的对照证据。',
 '2605.19257': '用 Plücker 光线距离因子把度量尺度变成可辨识量，无需事后 Sim(3) 对齐即在线输出米制轨迹：fr1/xyz ATE 2.86 cm（尺度误差 3.3%），纯 RGB 30 FPS。',
 '2609.31248': '把「需要多少高斯」拆成先验已知的表面/分辨率与训练中才显现的内容复杂度，用同一覆盖度量统一探索与蒸馏：标准场景同 PSNR 少 48% 高斯，自蒸馏减半仅损 0.08 dB。',
 '2611.27513': '把「几何 + 运动」潜变量而非视频或隐动作当作世界—动作接口，同一表征可解成点图与场景流又能直接回归动作：RoboTwin Hard 51%/37%（LAM 与视频潜变量基线皆为 0%）。',
 '2611.25417': '用同预算多区间候选取代单区间回归，并以原始深度残差做度量重锚定：TransCG MAE 6.833 mm（ReMake 8.040），跨相机零样本时尺度不再漂移。',
 '2611.27603': '把「对未知物理属性的试探性适应」本身当作表达性动画来源，测试时调潜变量而不更新网络参数：搬运 98.18%（CooHOI 92.01%）、负载适应 4–40 kg（5–15 kg）、推拉 94.38% 对 42.54%。',
 '2611.27164': '用结果不可知的力场编码替代轨迹先验，并把「力—响应」归因显式化为可复用区域监督再接到自监督 RL 奖励：OOD DCS 0.782 对 0.575、力定位 IoU 0.3956 对 SAM 的 0.2488。',
 '2611.26937': '首次把「可编辑场景程序的几何精度」与渲染相似度分离度量，用单变量配对实验把失败拆成三类：同一视频的密集重建几何分 75.9 而 GPT-6 Astra 仅 51.4，中位绝对尺度误差 4.6–10.4%。',
 '2611.27336': '首个与实现无关地把「可玩世界系统」形式化为四项职责及其接口，用引擎生成的 proxy 视频把确定性控制接到生成式渲染：832×480 稳态 23.82 FPS（提升 26%）、首帧 0.70 s（对半）。',
 '2611.27030': '把不透明三角面 splat 同时当作外观渲染与光传输载体，材质估计直接在三角面上做蒙特卡洛射线追踪：新视角 PSNR 40.78 dB（GS-IR 提升 3.10）、重光照 36.99 dB（IRGS 提升 1.79）。',
 '2611.27047': '把双视角未来 DINOv3 特征仅作训练期 privileged 监督、经 adapter 固化进观测接口，部署时预测模块可整体移除：分布内 92.0%（基线 48.0%）、200 个 held-out 场景 65.0%（23.5%）。',
 '2611.27512': '不改质量特征而改监督信号：用源域合成失真的层内顺序补上缺失失真类型的监督、以渲染感知距离软化排序目标：SJTU 到 WPC 跨库 SRCC 0.709（0.595），且不碰目标域数据、不生成伪 MOS。',
 '2601.13574': '把强度型光波导从弯曲主导推进到可承受 75% 应变的大变形全局形状重建，并用分组 Shapley 给出传感器布局依据：压痕 CD 1.307 mm、75% 应变下 1.214 mm、端到端 90 Hz。',
 '2606.16202': '把可形变实时逆物理从受控多视角推进到单段自运动第一视角，并把细粒度精化摊销成冻结残差模型：30% 未来预测 CD 0.028（PhysTwin 0.034），精化耗时 1.36 min 对 14.26–80.43 min。',
 '2611.27397': '把「原生格式转换」当作学习共享运动表示的手段，把几何保真与冻结策略下的动作一致性拆开评估：九条转换路径统一 MPJPE 16.801 mm、单帧 7.43 ms（官方工具的 5.6–6.5 倍），三格式全动作成功率 60.78%。',
 '2611.27224': '给出事件监督下 appearance-gradient 与 depth 补偿的局部可辨识性分析，并提出「相对冻结参考场的有界中心传输」：PAEv3D CDsum 0.051 对 Event-3DGS 0.127。',
 '2611.27509': '把对齐监督下沉到「逐事件 + 连续时间相机运动」粒度，用遮挡感知渲染器在任意目标时刻生成与事件一致的稠密深度：outdoor_day1 在 10 m 处 MAE 2.20 m（3.90 m），20 m 截断降 6.0–29.8%。',
 '2611.27817': '把声呐自身「首个海底回波」当海拔基准替代 DVL 提供公制尺度，并给出剩余尺度误差与海底倾角/粗糙度的解析界：平静水面每 100 m 误差 0.7–4.2%，804 m 港口回环后平均位置误差 5.55→3.35 m。',
 '2611.27003': '把静态/动态分离从基元级提前到相机与几何估计之前的特征级，用非对称层间引导从结构上切断动态更新对静态几何的反向污染：Waymo 全图 25.953 dB、动态区 22.043 dB（StreetForward +1.79）。',
 '2611.27418': '把 world model 的预测目标从「未来视角」换成目标导向的空间状态（waypoint–corridor），以确定性渲染而非像素生成接入 VLM：R2R-CE Val-Unseen SR 60.7、预测 66.7 ms/次（比像素生成快约 500 倍）。',
 '2611.27621': '首个面向 3D 标注布局的 MLLM 多视图质量评估：以逐视角逐维度结构化人工评分作监督，S-MAE 0.1388（Qwen3.8-Max 0.2614，降 46.9%），并发布 3 评者 × 5 维度 × 5 视角的 ALQA 数据集。',
 '2611.27719': '首个「求解而非存储」每视图暗光退化的低光 3DGS：退化留在 Gaussians 之外的粗基上逐视图闭式 rank-one 求解并让训练穿过求解，NIQE 2.63 对 4.15、MOS 4.15 对 3.44，且不需配对正常光监督。',
 '2611.27412': '时间图既不假设理想光栅也不再依赖另设标定平面，而是直接从被测录制中与时钟/几何自标定一并解出：拟合残差 5.07 μs、墙面重建 3.07 mm rms（理想光栅假设 8.88 mm）。',
 '2611.27281': '把「几何锚定 + 交替偏移的固定体素窗口」引入生成式八叉树解码器，使注意力成员关系在输出支撑集变化时保持一致：同一套权重同一参数量同时做去噪与上采样，HD 降 19.34%。',
 '2611.27299': '把表征空间预测与信号空间幅值/相位重建串在同一条计算路径上让梯度回传编码器，从理论上排除条件完全坍缩：三个划分 MAE 6.91°/9.04°/9.36°，相对 vemg2pose 降 10.3–19.3%。',
 '2611.27136': '首个公开的千万帧级合成点跟踪数据集：游戏世界补真实感与交互多样性、具身仿真补机器人与室内导航，带前景物体与环境表面的持久 3D 轨迹：10M 相机帧 / 13,972 序列，微调后 AJ3D 最高提升 7.83 点。',
 '2611.27289': '用频带特异量化 + 跨频带重建 + 结构化掩码码预测把「频带间互补」变成预训练目标，并发布 8 通道 / 499 用户 / 约 1,228 小时的 SynapMyo：三划分 MAE 7.28°/9.70°/10.00°，降幅 0.3–4.3%。',
 '2611.27633': '用「有界单参考帧」视觉地图替代持续增长的地图，并以 Schmidt 不确定性融合保持参考位姿相关性：摘要级结果显示 32 个基准上平均提速约 2.3×（X86）/2.1×（ARM）、峰值内存降至 1/20 与 1/13（正文不可核，仅摘要级证据）。',
 '2611.27788': '把 foveated refinement 压成「无特征复用、无蒸馏、无选择调度」的单主干单次非递归 pass，并用每数据集 26 组配置的受控协议把增益拆成 foveation 项与 glance loss 训练项：算力 0.56×、最小目标三分位最高提升 4.18 点，但作者直言换来的是算力而非精度。',
 '2611.26992': '首个把「从几何预测触觉力」形式化为渲染到触觉到力的三映射复合，给出等变/归零/误差界与刚度不可辨识极限：正文无实验（作者明确声明为理论工作），价值在设计约束而非数值。',
 '2611.26950': '在「金属指骨 + 薄硅胶 + 共享 CDC」约束下给出显式多导体观测算子与可量化屏蔽失配门限，并用 FEM 量化双阵列对接触材料交叉敏感的抑制：接触响应 4.6 fF 到 370 fF（0.05 到 0.5 mm），远场 20 到 5 mm 仅 15.9 fF。',
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
               'diffusion', 'head-mounted', 'eye tracking', 'egocentric', 'depth', 'VIO', 'relight',
               'VLA', 'EMG', 'hand', 'event camera']:
        if kw.lower() in (p['title'] + ' ' + str(g.get('method', ''))).lower():
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
- 公告日 2026-11-23（周一）≠ 拉取日 2026-11-24（周二 02:30）；11-21/11-22 为周末 `skipDays` 无公告段。API 首次提交日 {published}。
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
    fn = f"papers/notes/{p['id']}__{slugify(p['title'])}.md"
    if os.path.exists(fn):
        print('skip', fn); continue
    rank = f"，本批 Top10 第 {TOP10.index(p['id'])+1} 名" if p['id'] in TOP10 else ''
    action = ('- 纳入重点精读：方法与实验节可直接支撑选题与技术选型。' if p['grade'] == 'A'
              else '- 浏览级：关注问题设定与结论，方法细节按需回看。')
    action += ('\n- 有公开代码/项目页，可先跑通再评估迁移成本。' if p.get('code') and p['code'] not in ('未提供', '无')
               else '\n- 未提供代码，复现需按正文细节自行实现。')
    if p['value'] >= 4.20:
        action += '\n- 达 S 线（≥4.20）而本批门③ 判定非重磅日（margin −0.162）：值得优先读，但按口径记 A，不宜按 S 级对外表述。'
    body = NOTE.format(
        id=p['id'], title=p['title'], title_zh=p['title_zh'], track=p['track'], venue=p['venue'],
        date=DATE, value=f"{p['value']:.2f}", grade=p['grade'], evidence=p['evidence'],
        IMP=p['scores']['IMP'], NOV=p['scores']['NOV'], TEC=p['scores']['TEC'], EXP=p['scores']['EXP'],
        PER=p['scores']['PER'], TRL=p['scores']['TRL'], REP=p['scores']['REP'],
        level=p['level'], batch=p['batch'], announce=p['announce'], in_top10=str(p['in_top10']).lower(),
        published=p['published'], recall=p.get('recall') or 'KW/TITLE', tags=', '.join(tags_for(p, g)),
        concl=CONCL[p['id']], problem=g['problem'], method=g['method'],
        exp=bullets(g['key_numbers']), nov=bullets(g['novelty']), lim=bullets(g['limitations']),
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
MAIN.sort(key=lambda r: (-r['value'], -r['scores']['IMP'], -r['scores']['NOV'], r['id']))
BF.sort(key=lambda r: (-r['value'], -r['scores']['IMP'], -r['scores']['NOV'], r['id']))
g3 = G['gate3']
moc(MAIN, f'papers/MOC/MOC-{DATE}.md', f'MOC · {DATE}（11-23 公告批次 · 触觉与具身世界模型）',
    '> 当日地图：**公告日 2026-11-23（周一）≠ 拉取日 2026-11-24（周二 02:30）**——诚实口径；'
    '11-21/11-22 为周末 `skipDays`，listing 无公告段。主批 API published 核验：**11-20×34 / 11-19×8 / 11-16×1**'
    '（RSS published 为公告时间戳，不可当提交日）。\n'
    '> 主批 XR 新稿 **41 篇（0 S / 24 A / 17 B）**，Top10 实数 10 篇最高 **4.27**（2611.26744 forth / 2611.27290 EgoLAM / '
    '2611.27963 非穿透世界模型 三篇并列）；11-23 组 **506 槽位 / 404 篇唯一**，RSS 639 条覆盖率 404/404、缺收 0 → 免 API id_list；'
    '摘要级 KW + 标题级补扫 75 → 逐篇核摘要剔 42 → 33 篇；残差复核再采纳 8 篇 → 41 篇。\n'
    '> 全文：**41 篇 L0**（其中 40 FULL + 1 PARTIAL：2611.27633 Instant-LIVO 的 arXiv HTML v1 返回 404、ar5iv 仅返回摘要落地页，'
    '按摘要级评估并在本批显式声明）。\n'
    '> 覆盖度三关：门① **0.40**（2609.31248 TailorGS vs 库内 arXiv:2611.02044）/ 门② **7 赛道**（未触发重筛）/ '
    '门③ **4.27 vs 4.432**（现算，464 条入窗，半开窗口 [2026-10-25, 2026-11-24) 且按 batch 剔除本批两批）'
    '→ **margin −0.162，blockbuster=false，无 S**，3 篇 4.27 一律记 A。')
moc(BF, f'papers/MOC/MOC-backfill-{MMDD}.md', f'MOC · backfill-{MMDD}（旧稿 v2 再公告首次入馆）',
    '> **非当日新提交**：本批 9 篇均为 11-23 公告 RSS 混入的 `replace` 类旧稿再公告（首发 2026-01 至 2026-11），'
    '按诚实口径单独编号，不参与当日重磅日判定，最高记 A。\n'
    '> 定稿 **7 A / 2 B（无 S）**：2611.21057 WiTac 4.16（腕部触觉 VLA，GR00T 66.3%）· 2609.08848 FIRE3D 3.93 · '
    '2607.02921 R3D 3.92 · 2605.19889 GLUT 3.87 · 2605.19257 PRISM-SLAM 3.78 · 2609.31248 TailorGS 3.78 · '
    '2611.25417 MIR-Depth 3.73 · 2601.13574 本体感知膜 3.58 · 2606.16202 EgoPhys 3.58。')
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
