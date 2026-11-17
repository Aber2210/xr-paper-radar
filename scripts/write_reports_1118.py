# -*- coding: utf-8 -*-
"""2026-11-18 报告：主批（10 章）+ backfill（6 章）。"""
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from grade_caliber import assign_grade  # noqa: E402

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
os.chdir(ROOT)

D = json.load(open('data/scored_1118.json', encoding='utf-8'))
MAIN = [p for p in D if p['batch'] == '2026-11-18']
BF = [p for p in D if p['batch'] == 'backfill-1118']
MAIN.sort(key=lambda r: (-r['value'], -r['scores']['IMP'], -r['scores']['NOV'], r['id']))
G = json.load(open('data/gates_1118.json', encoding='utf-8'))
MAN = json.load(open('data/fulltext/_manifest.json', encoding='utf-8'))
HEAVY = bool(G['gate3']['blockbuster'])
for p in MAIN + BF:
    p['grade'] = assign_grade(p['value'], p['batch'], HEAVY)
    p['level'] = MAN[p['id']]['level']
    p['evidence'] = MAN[p['id']]['evidence']
TOP10 = [next(p for p in MAIN if p['id'] == i) for i in G['top10']]
G1, G3, MARGIN = G['gate1']['max_jaccard'], G['gate3']['top10_mean'], G['gate3']['margin']

DEEP = {
 '2611.21143': [
  '**数据飞轮是真正的方法**：CyberCap 采集 → 视觉-惯性 SLAM 给世界系 → 几何-时序优化出度量标注 → 训练 WinDEX-Net → 模型辅助标注新数据 → 独立人工 2D 与光动捕审计 → 重训。1,000 小时标注来自 200+ 操作者、1,000+ 场景、5,000+ 物体，这套闭环比单个网络更难复制。',
  '**精度与速度被显式拆成两个部署形态**：离线 WinDEX-Window（43.61 FPS、腕误差 27.1 mm、MPJPE 20.1 mm）与流式 WinDEX-Stream（171 FPS、42.7/33.2/12.5 mm）。流式的 PA-MPJPE 12.5 mm 明显差于离线 8.1 mm，作者没有掩盖这一取舍。',
  '**下游证据比重建指标更有说服力**：同一策略训练设置下仅替换手部运动参考，仿真抓取-举升-放置成功率 61% vs WiLoR 8%、HaWoR 17%；真机用 Gemini 2L + FoundationPose 提供特权定位，属「半受控」验证。',
  '**风险点**：依赖自研 CyberCap 头戴硬件（成本与可获得性未知）；世界系精度受 cuVSLAM 制约；代码与数据「未明确声明开源」。若无法获得采集硬件，只能复现网络部分而无法复现数据飞轮。'],
 '2611.21479': [
  '**三阶段各自解决一个失效模式**：Stage I 用 5×L_ROI + 0.1×LPIPS_H + 0.05×DINO_H 把监督压到手部与接触区（消融 FVD 473.69→351.55、Dice 87.02→92.74）；Stage II 用少步因果学生 + AnyFlow 把双向模型变流式；Stage III 在自生成 rollout 上做区域感知双 score 蒸馏（FVD 404.68→194.01、Dice 89.60→92.46）。',
  '**指标不是单点**：HandBench 八源 200 例上 FVD 181.67 vs 双向微调 Hand2World 294.32（−38.3%），MANO Dice 93.02 vs 90.60，LPIPS 0.2071 vs 0.2462；OOD 到 H2O/TACO 仍有 92.78/91.67 Dice。',
  '**实时性是硬指标**：540p 流式单 H200 18.03 FPS、平均延迟 741 ms、峰值显存 34.89 GiB（17 帧）；Ultra-Fast-VAE 把解码从 831.30 ms 压到 46.77 ms、参数 2423.5M→361.2M，PSNR 仅降 0.61 dB。',
  '**可复现性罕见地好**：代码 github.com/LynnReal-AI/LynnReal，权重三个 HuggingFace 仓库（Base-1.0 / Fast-preview / ultra-fast-vae-1.0）。风险是 741 ms 延迟对交互仍偏高，且因果模型上下文有限、未显式建模长期记忆。'],
 '2611.19773': [
  '**并行单位从「空间」换成「语义身份」**：先把高斯投到正交 DOM、用 SAM3 分割并合并成全局实例图，再按 5 像素邻域投票给高斯的身份，最后以「实例-相机对」为调度单位建共享 CUDA 队列，ROI 外零开销。这解释了为何 5 场景累计 3.48 h 能对 CityGS-X 的 14.08 h（−75.3%）成立。',
  '**轻量网格不是简单 QEM**：多视图深度/法向聚类拟合有限平面，约束实例 SDF（φ=φ⁰+ηδ）后在零水平集上自适应三角化；轻量网格 CD 0.914 m（PG-SAG+QEM 1.077、Metashape+QEM 1.117），稠密网格 0.737 m。',
  '**消融给出两条边界**：B=8 相对 B=1 快 2.23×，但峰值显存增 2.55–3.08×；保护项 L_guard 使 TSDF 网格 CD 0.526→0.470 m。作者也承认强依赖 FastGS 初始化，漏检楼栋无法补救。',
  '**工程可用性**：代码开源（github.com/IRIS-LAB-whu/SemLite-GS），数据用公开 GauScene/Skylume/Tianjin_Xiqing。CD 只度量平均几何接近度，不含平面一致性与交线完整性，低 CD 仍可能平面碎裂。'],
 '2611.20797': [
  '**这是一个「先定姿、后配对」的反向解法**：传统 blind PnP 在巨大配对空间里搜索，MomentPnP 用 14 个四阶以内置换不变矩把位姿从点集本身解出，再用 EM-ICP 做稠密对齐。定理 1 给出 N≥20 时几乎处处的唯一性，定理 2 给出有限截断下的误差界。',
  '**量级差异是可信的**：MegaDepth/ModelNet40/Data61 无外点时中位旋转误差 0.009°/0.16°/0.092°，比最优学习基线小 5–170 倍；169 图 SfM 输入上 100% 帧在 1° 内（CFPE 95%、学习法最多 48%）。',
  '**代价在时间**：30 帧全局搜索 1.92 s 对 GOSMA 68.8 s，但百万点约 20 分钟一帧；稠密模型下错位姿仍可对齐（旋转 2° 后 77% 点落在 3.4 px 内），说明矩匹配在退化几何上会失效。',
  '**对 XR 的意义**：无描述子、无训练、无初值的定位可用于「已知 CAD/扫描地图 + 未知相机」的冷启动，尤其适合离线标定与重定位；实时性需靠降采样或 GPU 化解决。'],
 '2611.19771': [
  '**把 JEPA 从 2D 潜空间搬到 4D 点云潜空间**：观测是单深度相机点云（5 mm 体素、1,200 点、xyz+rgb），PointNet 编码到 192 维，6 block transformer 预测器用 AdaLN-zero 注动作、因果关注 3 个历史潜变量，损失为潜变量 L2 + λ=0.09 的 SIGReg 防坍缩。',
  '**规划在潜空间、验证在点云**：想象 rollout 自回归预测并解码为 4D 点云（PAGE-4D 解码器，256 query 经 FiLM 调制），200 步想象点误差 ≤1.1 cm、立方体位置误差 1.39 cm，解码 4,096 帧 NN 距离 0.79 cm。',
  '**结果跨度大**：MetaWorld 98.4%（R3M 96.0）、Adroit Relocate 88.0%（R3M 65.3），但 Cube-Single 78.4%、Cube-Double 41.6%、Cube-Triple 18.4%，Cube-Quadruple 所有编码器（含本方法）为 0.0——难度阶梯上的断崖说明长时程组合仍是瓶颈。',
  '**证据边界**：实机仅三任务各演示一次、未报成功率；单一场景策略学习，跨场景/跨机器人泛化未验证。18.0M 参数、消费级单卡可训是它的工程优势。'],
 '2611.20533': [
  '**理论贡献比智能体更硬**：Theorem 3.2「分量悬崖」证明当预算低于 F_comp=Σmax(4, c₁A_curv(S_k)/ε) 时不存在同时满足 ε-逼近与同胚的输出，且该结论对任意算法成立——这解释了为什么所有保持拓扑的简化器在 0.5% 预算下都会「熔化」。',
  '**Clean 承担主要增益**：等清理对照中 bare QEM 1/24、保守清理+QEM 1/24、固定激进配方 19/24、智能体 24/24；说明「先删尘与焊薄墙、再付预算」比「让 LLM 调参」更关键（Corollary 3.3）。',
  '**结果**：0.5% 预算归一化 Chamfer 0.0015（重建管线 0.005–0.009、LATO.2 0.003–0.011）；8,223 个连通分量压到 1 个、0 条非流形边、保留 0.87% 面数；部署推理 11.7 s/网格且不调用 LLM。',
  '**风险**：S* 是声明的焊接闭合参考而非观测真值；多数消融单次运行（canonical 三次种子 8.983±0.011）；语料仅生成式建筑，标定不跨域迁移；零非流形 + 单主分量只是必要非充分证据。'],
 '2611.20283': [
  '**把 GS 当求解器载体而非渲染器**：用 RaDe-GS 重建后渲染深度采样得配点云（5×5 深度坡度滤波去掉约 2% 跨面片点），再在点云上离散单层位势边界积分方程，核做 mollification；密度减除让贴表面一个间距内仍准确，系统阻尼抑制表面噪声。',
  '**精度与速度同时占优**：18 合成场景内部平均误差 0.17% 温度量程（最好 0.050%）；整链约 31 s vs 网格管线 210 s（后者仅四面体化就 78–518 s/场景）；在 MILo/TopoSurfel 网格上跑 FEM 的误差是本方法的 1.8/1.9 倍。',
  '**真实与逆问题验证**：石膏壶 3 个热电偶平均差 1.4 °C；保温层厚度误差 14 mm（逐像素反演 43 mm）；裂纹温差 0.24 K vs 无裂纹 1.58 K。全链可微，梯度可回到位姿/深度/裂纹形状。',
  '**边界**：稳态、均质、各向同性、无内热源；多材料需界面耦合；表面假设纯辐射；未公开代码与数据。对 XR 的直接价值在「真实物体物理属性采集」，而非显示。'],
 '2611.18734': [
  '**问题重构是关键**：VLM 不是不会「看变化」，而是不会「找到同一地点」。STILL 把变化假设变成三分类 {same, changed, unseen}，先用 π³ 联合重建两段采集，把物体点集投到另一采集找可见比例最大的帧，用静态墙面/桌面定义地点，再让 Qwen3.5-9B 同时回答场景视图与地点视图，取几何平均概率。',
  '**误报率是主指标**：首/后半无变化对照特异度 30.2%→92.7%，同一未训练 Qwen3.5 误报从 93% 降到 12%；SceneDiff obj/sc AP 24.0→37.8（+13.8），无厨房训练数据的 SD-K 11.6→20.6。',
  '**训练数据构造值得复用**：把原标注改写成逐物体问题，Grounding DINO 提案按同一几何流程配地点，IoU≥0.4 标 changed、0.1–0.4 丢弃，负样本一半真实项、一半首/后半对照，共约 112k 问题，仅监督答案 token。',
  '**上限**：召回受提案器约束，地点精度受 π³ 重建限制；作者自算完美核验器在 SD-V 可达 74.7 AP，仍有约一倍空间。'],
 '2611.21383': [
  '**指出的是监督口径错误，而非网络结构**：2D 掩码只覆盖可见表面，但一个物体的高斯还包括被遮挡与内部高斯；用掩码监督渲染权重，会让「看不见的高斯」拿不到梯度，移除物体时留下幽灵。',
  '**VODA 的做法**：深度感知光栅化关闭透射率早停，按相邻深度间隔中位数切深度簇，取总贡献最大的簇 C*，用 alpha 加权聚合出高斯级伪目标（detach），对簇内每个高斯直接施加 L2（LaGa 用余弦）；另加像素级 push 损失（margin 0.3）。推理零开销。',
  '**效果**：Removal-3D 上 OpenGaussian mRDE 39.31→27.34、mIoU 52.87→60.90；LaGa mRDE 36.93→21.66、mIoU 75.93→79.07；LERF 上 Gaussian Grouping mIoU 22.75→43.73。',
  '**边界**：深度聚类会把相互接触的物体并簇、把内部稀疏物体切碎；遮挡高斯缺特征级真值，只能经下游任务间接评估；精确体评测仅 3 个合成场景具备。'],
 '2611.21060': [
  '**核心是把「度量」贯穿到生成**：冻结 Metric3D v2/MoGe-2 给全帧度量深度、DROID-SLAM 给相机轨迹；Metric Head 在视线-对数深度坐标精修平移并用静态像素匹配恢复尺度，使粗估计与条件同处一个度量世界系；随后才做流匹配生成。',
  '**拓扑感知采样解决「手-物接触处的证据归属」**：21 个投影关节作锚点，在多尺度 RGB-D 上预测可变形偏移，注意力 logit 叠加图像距离、对数深度差与反投影表面距离三类偏置；观测质量 q_i 与可用性 o_i 分离，低质量槽用 placeholder 保留身份。',
  '**结果**：HOT3D 相机系 MPJPE 8.60 mm（HaWoR 16.97，−49.3%）、ABS-W-MPJPE 20.58 mm（−28.7%）、腕误差 7.72 mm（−48.5%）；ARCTIC 相机系 17.54 mm（−52.9%），世界加速度误差降 64.3%。',
  '**风险**：世界精度依赖 SLAM 与单目深度先验，ARCTIC 相机误差 17.54 mm 但绝对世界误差 120.86 mm——SLAM 的旋转/平移/尺度误差会被放大，这是所有「相机系好看、世界系难看」的手部重建通病。'],
}


def dim_table(papers):
    L = ['| arXiv | 标题 | 赛道 | IMP | NOV | TEC | EXP | PER | TRL | REP | 总分 | 等级 | 证据 |',
         '|---|---|---|---|---|---|---|---|---|---|---|---|---|']
    for p in papers:
        s = p['scores']
        L.append(f"| {p['id']} | {p['title_zh']} | {p['track']} | {s['IMP']} | {s['NOV']} | {s['TEC']} | "
                 f"{s['EXP']} | {s['PER']} | {s['TRL']} | {s['REP']} | {p['value']:.2f} | {p['grade']} | {p['evidence']} |")
    return '\n'.join(L)


def chapter(i, p):
    s = p['scores']
    if p['batch'] == 'backfill-1118':
        ann = ('旧稿 v2/v3 再公告（replace），非当日新提交；'
               f"公告日 2026-11-17，拉取日 2026-11-18，原始投稿日 {p['published']}")
    else:
        ann = f"当日新公告批次；公告日 2026-11-17，拉取日 2026-11-18，提交日 {p['published']}"
    L = [f"### 第 {i} 章 · {p['title_zh']}（{p['id']}，{p['value']:.2f} {p['grade']}，{p['evidence']}）\n",
         f"- **赛道 / 场合**：{p['track']} / {p['venue']}",
         f"- **公告类型**：{ann}",
         f"- **一句话结论**：{p['conclusion']}",
         f"- **要解决的问题**：{p['problem']}",
         f"- **方法详解**：{p['method']}",
         '- **实验与结果**：']
    L += [f'    - {x}' for x in p['experiments']]
    L.append('- **创新点与贡献**：')
    L += [f'    - {x}' for x in p['innovation']]
    L.append('- **深读要点**：')
    L += [f'    - {x}' for x in DEEP.get(p['id'], [])]
    L.append('- **局限与风险**：')
    L += [f'    - {x}' for x in p['limits']]
    L.append(f"- **与文献库的关系**：{p['relation']}")
    L.append(f"- **可复现性**：{p['repro']}")
    L.append(f"- **行动建议**：{p['action']}")
    L.append(f"- **七维**：IMP {s['IMP']} · NOV {s['NOV']} · TEC {s['TEC']} · EXP {s['EXP']} · "
             f"PER {s['PER']} · TRL {s['TRL']} · REP {s['REP']} → **{p['value']:.2f}**\n")
    return '\n'.join(L)


header = f'''# XR 每日论文雷达 · 2026-11-18（11-17 公告批次）

> **诚实口径**：本批处理的是 **2026-11-17（周二）公告批次**，拉取时刻为 **2026-11-18 02:30（周三）**——公告日 ≠ 拉取日。
> 主批 33 篇的 API published 提交日为 **11-16×16 / 11-15×8 / 11-14×3 / 11-13×3 / 11-10×1 / 11-06×1 / 10-31×1**
> （2611.18679 提交 10-31、延迟约 17 天公告）。RSS 的 published 字段是公告时间戳，不可当提交日。
> 另设 **backfill-1118** 批次（6 篇旧稿 v2/v3 再公告，非当日新提交），单独报告。

## 一、执行摘要

- **规模**：11-17 公告组 **1,016 槽位 / 844 篇唯一论文**（cs.CV 342 / cs.GR 15 / cs.HC 58 / cs.MM 11 / cs.RO 134 / cs.AI 428 / eess.IV 28），全部未入馆；RSS 全量 1,323 条覆盖 listing 844/844（缺收 0）。
- **入选**：摘要级 KW 命中 66 篇 + 标题级补扫 36 篇 → 102 候选 → 逐篇核摘要剔除 69 篇误命中 → **XR 33 篇**（0 S / 19 A / 7 B / 7 C）。
- **全文**：39 候选（33 + 6）串行抓取，**35 篇 L0/FULL**（24,146–414,440 字符）+ **4 篇 L1/PARTIAL**（摘要页，摘要级评估并显式声明）。
- **三关**：门① 最大 Jaccard **{G1:.3f}**（<0.62）；门② 定稿 Top10 覆盖 **6 赛道**（全批 10，未重筛）；门③ 当日最高 **{G['gate3']['today_max']:.2f} vs 库内近 30 天 Top10 均分 {G3:.4f}**（窗口 2026-10-19~11-18、410 条入窗）。
  **机械 heavy_day=true，但差值仅 {MARGIN:.3f} < 0.05，属「险过」；按 skill §8.6.3「险过不得宣称重磅工作」，本期不记 S**：4 篇 ≥4.20 记 A 并注明达线。
- **本批主线**：
  1. **手部成为最强主线**——WinDEX（1,000 小时野外标注 + 171 FPS 流式 + 策略成功率 61%）与 MetricHand（HOT3D 世界系 20.58 mm）同日出现，加上 backfill 的 EgoEMG、DoF-Query，「手部度量重建 → 遥操作数据飞轮」正在闭环。
  2. **世界模型开始被「手」控制**——LynnReal-Hand 用 MANO 局部监督 + 少步蒸馏把视频世界模型做成单卡 18 FPS 的可交互系统并开源权重；JEPA4R 把 JEPA 搬到 4D 点云潜空间（MetaWorld 98.4%）。
  3. **3DGS 的物理化与可信化**——CiGS 把 GS 变成热传导 BIE 求解载体（0.17% 量程），QuantileGS 给逐像素共形误差界，Mask Is Not the Object 纠正「掩码=物体」的监督偏差。
  4. **硬件显示侧第三篇破冰**——WL-Headset Law 的 HRMD 库（241 款头显）把 PPD 估计误差 14.8%→3.2%，但仍属「度量与预测」而非器件设计。
- **S 级说明**：本期 **0 篇 S**。WinDEX 4.43 为当日最高，达 4.20 线且机械过门③，但因门③ 险过（+0.027）按校准关记 A；若按纯机械口径会产出 4 篇 S，本次显式拒绝该通胀路径。

## 二、排行榜（按加权降序，Top10）
'''

rank = ['| # | 论文 | 赛道 | 总分 | 等级 | 证据 | 关键数字 |', '|---:|---|---|---:|---|---|---|']
KEY = {'2611.21143': '世界 MPJPE 37.29 mm；策略成功率 61% vs 8%',
       '2611.21479': 'FVD 181.67（−38.3%）；540p 单卡 18 FPS',
       '2611.19773': 'CD 0.914 m；3.48 h（−75.3%）',
       '2611.20797': '中位旋转误差 0.009°（低 5–170×）',
       '2611.19771': 'MetaWorld 98.4%；Adroit 88.0%',
       '2611.20533': 'Chamfer 0.0015；8,223 分量→1',
       '2611.20283': '内部温度误差 0.17% 量程；31 s',
       '2611.18734': 'obj/sc AP 24.0→37.8；误报 93%→12%',
       '2611.21383': 'mRDE 39.31→27.34；mIoU 75.93→79.07',
       '2611.21060': 'HOT3D 世界 MPJPE 20.58 mm（−28.7%）'}
for i, p in enumerate(TOP10, 1):
    rank.append(f"| {i} | {p['title_zh']}（{p['id']}） | {p['track']} | {p['value']:.2f} | {p['grade']} | "
                f"{p['evidence']} | {KEY.get(p['id'], '')} |")

body = ['\n'.join(rank), '\n## 三、逐篇深度解读\n',
        '> 以下 10 章按价值降序，对应 Top10。每章含问题、方法、结果、创新、深读要点、局限、库内关系、可复现性与行动建议。\n']
for i, p in enumerate(TOP10, 1):
    body.append(chapter(i, p))

sec4 = ['\n## 四、当日全量 7 维度对比表（参考）\n',
        '> 完整表格见 [`papers/daily/2026-11-18/7dim-table.md`](../../papers/daily/2026-11-18/7dim-table.md)；下表为全部 33 篇主批（含 C 级）。\n',
        dim_table(MAIN)]

sec5 = f'''
## 五、覆盖率校验与筛选过程说明

### 5.1 漏网对账（先于拉取）
- `scripts/audit_listing_1118.py`：7 分类 `show=500` 单页 + 目标组 `declared≠got` 自动补页；7 分类最新公告日均为 **2026-11-17**，无 11-18 日组。
- 上批（11-16）组复采逐分类 **declared=got**：CV 91 / GR 5 / HC 13 / MM 0 / RO 38 / AI 164 / IV 9 = **320 槽位 / 271 唯一**（cs.AI 补采 skip=500 合并 92）。
- 未入馆 **258 篇 = 271 − 13（上批主批已入馆）**，与 11-17 运行候选集一致 → **0 漏网**。

### 5.2 召回三层与精度兜底
| 层 | 规则 | 命中 | 说明 |
|---|---|---:|---|
| L1 关键词（全称） | 56 条 KW（本批新增 26 条缺口词） | 66 | 含 `tactile`/`SDF`/`meshing`/`bundle adjustment`/`SPAD`/`monocular depth` 等 |
| L2 关键词（缩写边界） | `\\b(VR|AR|MR|XR|HMD|SLAM|VIO|IMU|6-DoF|...)\\b` | 含在 L1 内 | 噪声主要来源：SLAM/IMU 把机器人操作与自动驾驶带入 |
| L3 标题扩展词 | 32 条（`gaussian`/`point cloud`/`depth`/`hand` 等） | 36 | **不计入 RSS 漏网统计**，仅补召回 |
| 人工核摘要 | 逐篇读摘要判定 XR 相关性 | 剔 69 | 医学影像 6 / 机器人操作 8 / 自驾雷达 9 / 无人机农业 5 / 通用 LLM-HCI 6 / 通用位姿与分割 9 / 其他 26 |

### 5.3 三关结果
- **门① 同质度**：Top10 与库内近 90 天非本批文献的最大 Jaccard **{G1:.3f}**（2611.21060 vs 2605.18553），其余 0.118–0.214，均远低于 0.62。
- **门② 赛道覆盖**：定稿 Top10 覆盖 **6 赛道**（化身与人体 2 / 世界模型与仿真 2 / 重建与SLAM 2 / 神经渲染 2 / 内容生成 1 / 感知与认知 1），全批 10 赛道 → 纯值排序即达标，**未触发重筛**。
- **门③ 价值天花板**：当日最高 **{G['gate3']['today_max']:.2f}** vs 库内均分 **{G3:.4f}**（410 条入窗，窗口不含本次运行追加的 `2026-11-18` 与 `backfill-1118` 两批）→ 机械 `heavy_day=true`，**差值 {MARGIN:.3f} < 0.05**。
  - 按 skill §8.6.3，本期**不宣称重磅日**，S 不授予；4 篇 ≥4.20（WinDEX 4.43 / LynnReal-Hand 4.37 / SemLite-GS 4.30 / MomentPnP 4.27）记 A，并在 7 维表、笔记与 registry 的 `grade` 中体现。
  - `data/gates_1118.json` 同时保留 `heavy_day_raw=true`、`margin=0.027`、`blockbuster=false`、`s_awarded=false`，事后可自证口径。
- **OUTDATED / SUPERSEDED**：0 篇。

## 六、附录

### 6.1 证据等级分布
- 主批 33 篇：**29 L0/FULL + 4 L1/PARTIAL**；backfill 6 篇：**6 L0/FULL**。
- PARTIAL 4 篇：2611.18822（LongCat-Video-Avatar 1.6 技术报告）、2611.20196（DoF-Query）、2611.20570（OrthoMark）、2611.21485（ReSpaceBench）。四篇 arXiv HTML 均 404（v1 复核），ar5iv 仅返摘要页（chars 4,567–5,535，无任何正文章节）；沙箱无 pdfminer/pypdf，L2 PDF 路径不可用。**均在笔记与本章显式标注「摘要级评估」，未据标题脑补方法细节**。

### 6.2 C 级仅入馆（不解读）
| arXiv | 标题 | 赛道 | 分值 | 原因 |
|---|---|---|---:|---|
| 2611.18822 | LongCat-Video-Avatar 1.6 技术报告 | 化身与人体 | 2.49 | PARTIAL 且无量化结果，Arena 仅称优于前代 |
| 2611.18979 | 视频世界模型的局部化 VoE 评测 | 评估与数据集 | 2.82 | 评测方法学，无方法贡献 |
| 2611.19765 | M-CROSS 水陆过渡 SLAM 数据集 | 评估与数据集 | 2.97 | 仿真数据集，XR 相关性弱 |
| 2611.20245 | 从 XR 草图到 CAD | 交互与输入 | 2.27 | 立场论文，无实验 |
| 2611.20568 | √VINS 360 视觉惯性 SLAM | 重建与SLAM | 2.58 | 挑战赛方案，方法增量有限 |
| 2611.20570 | OrthoMark 地点识别 | 重建与SLAM | 2.90 | PARTIAL，AP 数值未报告 |
| 2611.21233 | 网络摄像头眼动追踪 | 交互与输入 | 2.08 | 单被试，误差 204 px 量级 |

### 6.3 剔除与降级清单
- 误命中剔除 69 篇：完整 id 清单见 `data/rejected_1118.json`。
- 抓取失败：0 篇；L5 摘要降级：0 篇；OCR：未使用。
- 数据修补：无（交付前 `title == id` / `len(title) < 12` 抽查 0 命中）。

### 6.4 产物清单
- 本报告 + `reports/XR-Backfill-Report-backfill-1118.md`
- `papers/daily/2026-11-18/` 与 `papers/daily/backfill-1118/` 各含 `7dim-table.md`、`scored.md`、`run_log.md` 三件
- 原子笔记 31 篇（`papers/notes/`）、MOC 2 份、`MOC-总索引.md` 刷新
- registry 951 → **990**（+33 +6，备份 `registry.jsonl.bak-20261118`）
'''

open('reports/XR-Daily-Report-2026-11-18.md', 'w', encoding='utf-8').write(
    header + '\n' + '\n'.join(body) + '\n'.join(sec4) + sec5)
print('main report written', os.path.getsize('reports/XR-Daily-Report-2026-11-18.md'))

# ---------------- backfill report ----------------
bh = ['# XR 补录报告 · backfill-1118（旧稿 v2/v3 再公告）\n',
      '> **非当日新提交**：本批 6 篇来自 11-17 公告批次 RSS 混入的 replace 类旧稿（未入馆 479 篇 → 摘要级 XR 命中 32 篇 → 逐篇核摘要取 6 篇）。',
      '> 原始投稿 2025-11-20 / 2026-05-07 / 2026-05-10 / 2026-07-04 / 2026-09-25 / 2026-11-13，updated 2026-11-14~11-16。',
      '> 单独编号，不参与当日重磅日判定；≥4.20 亦按口径记 A。全文 6 篇全部 L0/FULL（51,940–86,581 字符）。\n',
      '## 一、摘要\n',
      '- 定稿 **2 A / 3 B / 1 C（无 S）**，最高 **2607.03875 MACRO 3.93**。',
      '- 两条值得注意的线：① **特写渲染的参考图对齐**（MACRO，免训练、DINOv2 距离 −26%）与主批 WL-Headset（显示硬件度量）共同指向「近眼显示的画质与硬件基线」；② **神经渲染地图定位**（LoC-IN，0.59 cm、100% 定位率）与主批 MomentPnP（无对应位姿）构成「地图侧 vs 求解侧」两条定位路线。\n',
      '## 二、排行榜\n',
      '| # | 论文 | 赛道 | 总分 | 等级 | 证据 |', '|---:|---|---|---:|---|---|']
BFS = sorted(BF, key=lambda r: -r['value'])
for i, p in enumerate(BFS, 1):
    bh.append(f"| {i} | {p['title_zh']}（{p['id']}） | {p['track']} | {p['value']:.2f} | {p['grade']} | {p['evidence']} |")
bh.append('\n## 三、逐篇解读\n')
for i, p in enumerate(BFS, 1):
    bh.append(chapter(i, p))
bh.append('\n## 四、附录\n')
bh.append('- 全文：6 篇 6 L0/FULL；无 PARTIAL、无 L5、无 OCR。')
bh.append('- registry：+6（batch=backfill-1118，按 base_id 幂等）。')
bh.append('- 剔除 26 篇非 XR（机器人抓取 / 水下与卫星定位 / 自动驾驶 / 医学骨重建 / 农业 NVS 等），清单见 `data/old_replace_1118.json` 与 triage 日志。')
open('reports/XR-Backfill-Report-backfill-1118.md', 'w', encoding='utf-8').write('\n'.join(bh))
print('backfill report written', os.path.getsize('reports/XR-Backfill-Report-backfill-1118.md'))
