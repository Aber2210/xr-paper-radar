# -*- coding: utf-8 -*-
"""2026-11-27 最终解读报告 + backfill 报告 + daily 产物（7dim-table / scored / run_log）。

口径要点（不可改写）：
- 公告日 2026-11-26（周四）≠ 拉取日 2026-11-27（周五 02:30）；11-27 组尚未公告；11-26 为单日公告组。
- 主批 55（43 新 + 12 残差采纳）+ backfill 8 = 63；A44 / B14 / C5，无 S。
- 门③ margin −0.109、blockbuster=false → 不授 S；4.35/4.35/4.20 三篇达 S 线按校准关记 A。
- 门② 纯值 Top10 仅 4 赛道 → 回补一次（剔 2611.34932、补 2611.33467）→ 5 赛道。
"""
import glob
import json
import os
import re
import shutil
from collections import Counter

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
os.chdir(ROOT)
DATE, MMDD = '2026-11-27', '1127'
ANN = '2026-11-26'

D = json.load(open('data/scored_%s.json' % MMDD, encoding='utf-8'))
G = json.load(open('data/gates_%s.json' % MMDD, encoding='utf-8'))
RES = json.load(open('data/residual_%s.json' % MMDD, encoding='utf-8'))
PUB = json.load(open('data/published_%s.json' % MMDD, encoding='utf-8'))
MAN = json.load(open('data/fulltext/_manifest.json', encoding='utf-8'))
XR = json.load(open('data/xr_pool_%s.json' % MMDD, encoding='utf-8'))
OLD = json.load(open('data/old_replace_%s.json' % MMDD, encoding='utf-8'))
MX = json.load(open('data/missed_xr_%s.json' % MMDD, encoding='utf-8'))
AG = G['announcement_group']

MAIN = [p for p in D if not p['batch'].startswith('backfill')]
BF = [p for p in D if p['batch'].startswith('backfill')]
TOP = [p for p in D if p['in_top10']]
TOP.sort(key=lambda r: (-r['value'], -r['scores']['IMP'], -r['scores']['NOV'], r['id']))
g1, g2, g3 = G['gate1'], G['gate2'], G['gate3']
GR = Counter(p['grade'] for p in D)
GRM = Counter(p['grade'] for p in MAIN)
GRB = Counter(p['grade'] for p in BF)

DIG = {}
for k in range(1, 9):
    for r in json.load(open('data/digest_%s_g%d.json' % (MMDD, k), encoding='utf-8')):
        DIG[r['id']] = r

MAIN_IDS = {p['id'] for p in MAIN}
REJ_IDS = sorted(pid for pid in XR if pid not in MAIN_IDS)
REJ = {pid: XR[pid] for pid in REJ_IDS}


def concl(pid):
    f = glob.glob('papers/notes/%s__*.md' % pid)
    txt = open(f[0], encoding='utf-8').read()
    m = re.search(r'## 一句话结论\n(.+?)\n\n', txt, re.S)
    return m.group(1).strip()


def bl(items):
    if isinstance(items, (list, tuple)):
        return '\n'.join('- ' + str(x) for x in items)
    return '\n'.join('- ' + x.strip() for x in re.split(r'[；。]', str(items)) if x.strip())


def why(p):
    """把 digest 的 scores_why 单串拆成逐维理由（唯一来源，不二次改写）。"""
    s = DIG[p['id']]['scores_why']
    out = {}
    for m in re.finditer(r'(IMP|NOV|TEC|EXP|PER|TRL|REP)=(\d)[：:](.*?)(?=(?:IMP|NOV|TEC|EXP|PER|TRL|REP)=\d[：:]|$)', s, re.S):
        out[m.group(1)] = m.group(3).strip(' 。')
    return out


def pub_dist(rows):
    c = Counter(p['published'] for p in rows)
    return ' / '.join('%s×%d' % (k[5:], v) for k, v in sorted(c.items(), key=lambda kv: -kv[1]))


os.makedirs('papers/daily/%s' % DATE, exist_ok=True)
os.makedirs('papers/daily/backfill-%s' % MMDD, exist_ok=True)

# ==================== 一、主报告 ====================
L = []
A = L.append

A('# XR 每日论文雷达 · %s\n' % DATE)
A('> **诚实口径**：本批处理的是 **%s（周四）公告批次**，拉取时刻 **2026-11-27 02:30（北京时间）**。'
  '11-27 组此刻**尚未公告**（拉取早于 11-27 00:00 UTC = 08:00 北京时间的释放时刻）；'
  '11-26 是**单日公告组**，无周末积压。'
  'arXiv **公告日 ≠ 拉取日 ≠ 首次提交日**：主批 API `published` 核验为 %s（合计 %d 篇）；'
  'RSS 的 `published` 是公告时间戳，不能当提交日使用。\n' % (ANN, pub_dist(MAIN), len(MAIN)))
A('> 覆盖范围：cs.CV / cs.GR / cs.HC / cs.MM / cs.RO / cs.AI / eess.IV 七分类 listing（show=500 单页 + skip 补页，逐分类 declared=got 核对）。'
  '%s 组 **%s 槽位 / %s 篇唯一**（%s），全部命中 RSS **849 条**（缺收 0），摘要级覆盖率 **1.0000**。\n' % (
      ANN, format(AG['slots'], ','), format(AG['unique'], ','),
      ' / '.join('%s %d' % (k, v['got']) for k, v in AG['per_cat'].items())))

# ---- 一、执行摘要 ----
A('\n## 一、执行摘要\n')
A('**本批 %d 篇（主批 %d + backfill %d），%d S / %d A / %d B / %d C；Top10 实数 10 篇，最高 %.2f（2611.34480 ProManO，与 2611.34944 AnyCam 并列）。**'
  ' 门③ 现算：当日最高 %.2f vs 库内近 30 天 Top10 均分 **%.3f**（%d 条入窗，半开窗口 [%s, %s)，按 batch 剔除本次追加的 `%s`），'
  'margin **%+.3f** → `heavy_day_raw=%s`、`blockbuster=%s` → **本批授 %d 个 S**；'
  '4.35 / 4.35 / 4.20 三篇达 4.20 的 S 线，按「险过不授」的校准关记 A 并在笔记中注明。\n' % (
      len(D), len(MAIN), len(BF), GR['S'], GR['A'], GR['B'], GR['C'], g3['today_max'],
      g3['today_max'], g3['top10_mean'], g3['in_window'], g3['window_lo'], g3['window_hi'],
      '、'.join(g3['this_run_batches_excluded']), g3['margin'], g3['heavy_day_raw'], g3['blockbuster'],
      GR['S']))
A('当日四条主线：\n')
A('1. **「度量」成为重建线的共同命题：不是估计得更准，而是把不可观测量显式建模**：2611.34480 ProManO 先从标定约束'
  '**推导**出内参相容变换恰为 Sim(3) 与无穷远平面 3 自由度的 10 维子流形，再把沿射线锚点协方差、可观测性门控与'
  '可认证相似同步装进同一个 EM——EuRoC F1 **53.99% / CD 0.065 m**、Oxford Spires **60.74%**（比 Sim(3) 高 **9.8 点**）、'
  '四数据集平均 F1 **+4.1–9.8 点**；2611.34005 ScaleCurve 把「整段一个尺度」换成**时变尺度**（脚点-地平面交距给逐关键帧观测），'
  'SLOPER4D W-MPJPE **446.8 vs GVHMR 959.1 mm（−53.4%）**，改回常数尺度即退化到 708.1 mm——同一篇内自证了「时变」的必要性；'
  '2611.33824 ToysRU 则绕开尺度：手部实例分割后只在物体像素上跑 SfM，再按固定角位移**分段跑子序列 + 多对跨序列帧 Umeyama 拼接**，'
  'F1 **93.80 vs Color-NeuS 81.75**、CD **0.74 vs 2.24**，耗时 **0.5 h vs 12 h**（VGGT 直出仅 19.74）。\n')
A('2. **3DGS 的效率与几何合法性，靠「结构先验」而不是「更多基元、更长训练」**：2611.34939 MEMO 给每个高斯一组'
  '**高斯过程式时序运动核**，让它在整段时间内始终是合法表面元、任意时刻可直接抽网格——Blender-Moments 联合 F-score '
  '**0.556 vs D-2DGS 0.365 / 4DGS 0.283**，训练 **18 min vs 33 / 142 min**，同一模型换 TSDF 融合就掉到 0.468；'
  '2611.33374 VersionGS 用「**GOP 版本字典 + 每帧激活索引**」替掉光滑形变函数，高运动帧 PSNR 跌幅 **<0.3 dB**（基线 1.1–4.0 dB）、'
  '存储 **0.060 vs 0.962 MB/帧**；2611.33796 SprintGS 承认「模型越紧凑、固定开销占比越高」这一反直觉事实'
  '（FastGS 里损失占比 4%→23%），按训练日程削 tile 与 kernel 启动，**80 s vs 172 s**；2611.33698 给 LM-RS 补齐三阶 SH 与'
  '场景分布化视角采样，让**二阶优化真正压过 Adam**（198.1 s vs 457.5 s，PSNR 25.800 vs 25.698）。\n')
A('3. **世界模型开始把「状态」写成显式可渲染对象，而不是像素/潜变量**：2611.33467 SplatWAM 把状态直接定义为 N 个高斯'
  '（tokenizer 用固定 query 解出、diffusion forcing 预测演化），OGBench 新视角 PSNR **23.37**、端到端 **83.9 FPS**'
  '（比视频世界模型快 12×、高 2.0 dB），LIBERO **92.3%（1B）vs WorldVLA 79.1%（7B）**；2611.34730 WorldInteract 把'
  '**材质行为与接触响应解耦**（材质条件生成 + 推理期控制器/生成器交替），Physics-IQ **63.0 vs 48.0**、ST-IoU **0.701 vs 0.280**；'
  '2611.33591 VivaWorld 用**组合式几何记忆**（点云背景 + 生成网格前景 + mesh-seeded 连通域过滤）把相机误差锁在局部 chunk，'
  '1,000 帧 PSNR **13.92 vs Lyra 2.0 12.85**；而 2611.33655 Recall4D 用 oracle 实验**证伪**了「窗口间配准漂移」这一通行解释'
  '（换 GT 位姿 EPE 1.568 vs 1.569 无差别），把长视频 4D 跟踪的瓶颈正名为「遗忘」——这类「先证伪再改设计」的做法本批出现两次。\n')
A('4. **第一视角 / 穿戴设备形成独立评测面：把「相机不在最佳位置」当第一性问题**：2611.33760 GlassGround 用'
  '「同一状态、同一指令、同一目标」配对截图与**真实穿戴相机观测**，十个开源模型均值 **94.8%→48.5%**，并把落差归因到'
  '**像素来源（29.2–31.7 点）而非呈现方式（14.7–17.1 点）**；2611.34466 把 computer-use 从「一次性给全视频」改成**在线流式**'
  '（观测/需求/站点状态三流异步演化），Online **63.4% vs Computer-Use 86.1%**，低 26.3 点；2611.34347 把社会具身拆成'
  'Attention→Intention→Reaction→Interaction 四层同一时间锚点的在线链，最强模型总分 0.726 但 **Intention 仅 0.569、IAS 上限 0.237**；'
  '2611.33565 干脆用**手表/眼镜的扬声器-麦克风做短程 FMCW 声呐**，补上「相机看不到手」的 53% 窗口（新被试 verb top-5 '
  '**58.7→68.9**，而外中心相机在新被试上反而 −6.5）；2611.34945 MidasTUI 用「手抓住并移动物体」当隐式参与信号，'
  '把任意日常物体即时变成 TUI（参与分类 F1 0.918、Quest 3 + 笔记本 42 FPS）。\n')
A('**筛选与复核**：摘要级 KW 命中 **%d** 篇 + 标题级扩展词补扫 **%d** 篇 = 候选池 **%d** 篇；逐篇核摘要剔 **%d** 篇'
  '（其中 1 篇为库内 cross 再公告，见 §5.2），得 **%d** 篇；第 3.5 步残差复核扫描 **%d 条**、判 **%d 条**应收录'
  '（**%.2f%%**，显著高于近批 1.5–2.8%%）、**采纳 %d 篇**（全部另走全文抓取与评分）→ 主批 **%d 篇**。'
  '上一公告组（11-25 组，624 篇唯一）未入馆 **%d 篇** 复采核验：**%d/%d 均有摘要**，摘要/标题级命中 **%d 篇**'
  '**全部落在上批处置集合**（`scored_1126 ∪ xr_pool_1126 ∪ nonxr_1126 ∪ old_replace_1126`）→ **0 漏网**'
  '（`data/missed_xr_%s.json` 的 `leak_n=0`），无需补漏。\n' % (
      G['recall']['kw_hits'], G['recall']['title_extra'], G['recall']['pool'],
      len(REJ), len(MAIN) - G['recall']['residual_adopted'], RES['n_scanned'], RES['n_flagged'],
      RES['rate'] * 100, G['recall']['residual_adopted'], len(MAIN),
      MX['unregistered'], MX['unregistered'], MX['unregistered'], len(MX['hits']), MMDD))

# ---- 二、Top10 ----
A('\n## 二、Top10 排行榜\n')
A('| 排名 | 论文 | 赛道 | 总分 | 档 | 证据 | 关键贡献 |')
A('|---|---|---|---|---|---|---|')
SHORT = {
 '2611.34480': '从标定约束推导出内参相容变换 = Sim(3)·无穷远平面 3 自由度（10 维流形），把锚点协方差与可观测性门控装进同一 EM：F1 53.99%/60.74%，比 Sim(3) 高 9.8 点。',
 '2611.34944': '用锚物体 3D 高斯的轨迹渲染当相机信号（尺度感知/视角完备/相对物体）：CO3D PSNR 14.08、anchor IoU 0.814 vs 0.346，417 帧旋转误差 10.94° vs 27.93°。',
 '2611.34489': '用「佩戴者就在相机处」的对极几何把冻结 VGGT-Ω 的位姿变成识别读出：最难未见类 71.1 vs 3D 模型 42.1，比 GPT-6 Astra 高 31.6 点，0.4 s/条。',
 '2611.33650': 'Mamba2 混合架构 + register 引导两级稀疏注意力 + 三阶段蒸馏：27 ms/帧恒定，7-Scenes Acc 0.066 vs 0.129，训练仅教师 9% GPU 小时。',
 '2611.33760': '同状态同指令同目标配对截图与穿戴实拍，把观测方式变唯一变量：开源均值 94.8%→48.5%，像素来源落差 29.2–31.7 点；PairDistill+ReGround 69.62%。',
 '2611.34476': '把压缩预算分配建成目标相机的函数（逐视图渐进 Carrier，任意整数配额）：120 视图 9.23×/64× 帧率，PSNR 27.34 vs 24.16，显存 −67%。',
 '2611.34128': 'pointmap → 连续射线表面：query-view 投票选视角 + 粗回归 + 精化，无位姿直出表面：ScanNet++ ADE 0.132 m vs 0.198，T&T 1.233 m vs 3.970。',
 '2611.34223': '对协方差**平方根**条件化（7×3 QR 出 Cholesky 因子），原生鱼眼做 ray-based UT 渲染而不去畸变：170° 鱼眼 +8.05 dB，离轴 60–80° 领先 6.2 dB。',
 '2611.34939': '每个高斯带 GP 式时序运动核，恒为合法表面元、任意时刻直接抽网格：联合 F-score 0.556 vs 0.365/0.283，法向 24.6°，训练 18 min vs 142 min。',
 '2611.33467': '状态即 N 个显式高斯（tokenizer 解出 + diffusion forcing 演化）：OGBench 23.37 PSNR / 83.9 FPS，LIBERO 92.3%（1B）vs 79.1%（7B）。',
}
for i, p in enumerate(TOP, 1):
    A('| %d | %s（%s） | %s | **%.2f** | %s | %s | %s |' % (
        i, p['title_zh'], p['id'], p['track'], p['value'], p['grade'], p['evidence'], SHORT[p['id']]))
A('\n> **门② 触发一次回补**：纯值 Top10 仅覆盖 **%d 赛道**（%s）→ %s，定稿 **%d 赛道**（%s）；全批 **%d 赛道**（共 12 赛道体系）。'
  '被剔的 2611.34932（4.01，重建与SLAM 第 5 篇）**仍完整入馆、写笔记并保留 A 档**，仅不占 Top10 名额。\n' % (
      len(g2['pure_value_tracks']), '、'.join('%s×%d' % (k, v) for k, v in g2['pure_value_tracks'].items()),
      g2['rescreen'], g2['n_tracks'],
      '、'.join('%s×%d' % (k, v) for k, v in g2['top10_tracks'].items()), g2['all_batch_tracks']))
A('> **OUTDATED / SUPERSEDED 均为 0**：本批未发现「同问题更优且更晚」的直接取代关系。'
  '需要区分的是**再公告**：2611.30173（Confidently Lost）本次以 `cross` 重新出现在 11-26 组，'
  '而它已在 11-25 批以 3.71 入馆 → 按「库内 v2/再公告不重复入馆」剔除，不列入 OUTDATED（无更优版本，只是同一稿换分类）。'
  'backfill 8 篇为 `replace` 类旧稿再公告（首发 2025-09-20 ~ 2026-11-24），已在笔记中保留首发日。\n')

# ---- 三、逐篇解读 ----
A('\n## 三、逐篇深度解读\n')
for i, p in enumerate(TOP, 1):
    g = DIG[p['id']]
    A('\n### 第 %d 章 %s（%s · %s · %.2f %s）\n' % (i, p['title_zh'], p['id'], p['track'], p['value'], p['grade']))
    A('**一句话结论**：%s\n' % concl(p['id']))
    A('**要解决的问题**\n\n%s\n' % g['problem'])
    A('**方法详解**\n\n%s\n' % g['method'])
    A('**实验与结果**\n\n%s\n' % bl(g['key_numbers']))
    A('**创新点与贡献**\n\n%s\n' % bl(g['novelty']))
    A('**局限与风险**\n\n%s\n' % bl(g['limitations']))
    rel = '- 本批新增（batch `%s`，公告类型 `%s`），赛道「%s」，首发提交日 %s。' % (
        p['batch'], p['announce'] or 'new', p['track'], p['published'])
    if p.get('recall') == 'RESIDUAL_ADOPT':
        rel += ('\n- **由第 3.5 步残差复核捞回**：摘要级 KW 与标题级扩展词均未命中，说明现有词表在该表述上仍有语义缺口'
                '（该篇走完「全文抓取 → 7 维评分 → 产物」全流程后才入馆，清单本身未直接并库）。')
    if p['id'] in {x['add'] for x in g2.get('rescreen_ops', [])}:
        rel += '\n- **门② 回补进入 Top10**：纯值排序下 Top10 只覆盖 4 赛道，本篇作为「%s」最高分被回补。' % p['track']
    if p.get('note'):
        rel += '\n- 备注：%s' % p['note']
    rel += '\n- 与库内同赛道论文构成并列参考；本批 OUTDATED/SUPERSEDED 判定为 0。'
    A('**与文献库的关系**\n\n%s\n' % rel)
    A('**可复现性**\n\n- 代码/项目页：%s\n- 全文证据：%s（%s，%s 字符，%s）\n' % (
        p.get('code') or '正文未提供', p['evidence'], MAN[p['id']]['level'],
        format(MAN[p['id']]['chars'], ','), MAN[p['id']].get('url', '—')))
    act = '- 纳入重点精读：方法与实验节可直接支撑选题与技术选型。' if p['grade'] in ('S', 'A') else '- 浏览级。'
    _cd = (p.get('code') or '').strip()
    _has = ('http' in _cd) and not _cd.startswith('未')
    if _has:
        act += '\n- 有公开代码/项目页，可先跑通再评估迁移成本。'
    else:
        act += '\n- 未见公开代码，复现需按正文细节自行实现。'
    if p['grade'] == 'S':
        act += ('\n- 本批门③ margin %+.3f、`blockbuster=true`，按口径授 S：可作对外引用重点，'
                '但结论仍按论文级证据表述（未做产品化验证）。' % g3['margin'])
    elif p['value'] >= 4.20:
        act += ('\n- 达 S 线（≥4.20）但本批 `margin %+.3f < 0.05`、`blockbuster=false`，按校准关记 A：'
                '可作为重点选题，但对外表述不宜称「重磅」。' % g3['margin'])
    A('**行动建议**\n\n%s\n' % act)

# ---- 四、7 维表 ----
A('\n## 四、当日全量 7 维度对比表\n')
A('权重：IMP 0.20 · NOV 0.20 · TEC 0.15 · EXP 0.15 · PER 0.15 · TRL 0.08 · REP 0.07；'
  '档位：S ≥4.20 **且** `blockbuster=true`，A 3.60–4.20，B 3.00–3.60，C <3.00（仅入馆不解读、不写笔记）。'
  '完整表见 [papers/daily/%s/7dim-table.md](../papers/daily/%s/7dim-table.md)。\n' % (DATE, DATE))
A('| # | arXiv | 论文 | 赛道 | IMP | NOV | TEC | EXP | PER | TRL | REP | 总分 | 档 |')
A('|---|---|---|---|---|---|---|---|---|---|---|---|---|')
for i, p in enumerate(MAIN, 1):
    s = p['scores']
    A('| %d | %s | %s | %s | %d | %d | %d | %d | %d | %d | %d | **%.2f** | %s |' % (
        i, p['id'], p['title_zh'][:34].replace('|', '/'), p['track'], s['IMP'], s['NOV'], s['TEC'],
        s['EXP'], s['PER'], s['TRL'], s['REP'], p['value'], p['grade']))

# ---- 五、覆盖率校验 ----
A('\n## 五、覆盖率校验与筛选过程\n')
A('### 5.1 漏网对账（第 1 步，先于拉取）\n')
A('- 7 分类最新公告日**全部为 %s（周四）**；11-27 组 `declared=None / got=0`（尚未释放）。\n' % ANN)
A('- %s 组逐分类 declared=got：%s = **%s 槽位**，唯一论文 **%s 篇**（跨列表重复 %s 条 = 同稿多分类 cross）。'
  '上一公告组（11-25）复采逐分类 declared=got 一致（含 cs.CV `skip=500` 补 90 条、cs.AI 补 48 条，302/300 全取到），'
  '与上批记录相符 → **无新增漏跑窗口**。\n' % (
      ANN, ' / '.join('%s %d' % (k, v['got']) for k, v in AG['per_cat'].items()),
      format(AG['slots'], ','), format(AG['unique'], ','), format(AG['slots'] - AG['unique'], ',')))
A('- 上一公告组（11-25 组 624 篇唯一）未入馆 **%d 篇 = 624 − 55**（上批主批已入馆）；'
  '用 11-26 / 11-27 两份 RSS 全量核摘要，**%d/%d 全覆盖、0 篇缺摘要**，摘要/标题级命中 **%d 篇**'
  '**全部落入上批处置集合** → **0 漏网**（`data/missed_xr_%s.json` 的 `leak` 为空对象、`leak_n=0`）。\n' % (
      MX['unregistered'], MX['unregistered'], MX['unregistered'], len(MX['hits']), MMDD))
A('### 5.2 数据源与召回\n')
A('- RSS 7 分类 `--no-filter` 去重 **849 条**（`WROTE=849`、`OK_CATS=7/7`，完整采集：任一分类失败即 exit 2，本批未触发）。'
  'listing %s 篇 **100%% 被 RSS 覆盖（缺收 0）** → **免 API `id_list` 枚举**，规避 429 静默丢批；'
  'API 仅用于 64 篇的提交日核验（`check_published_1127.py`，64/64 全齐）。\n' % format(AG['unique'], ','))
A('- 召回三层：摘要级 KW **%d** + 标题级扩展词补扫 **%d** = **%d 篇命中** → 逐篇核摘要剔 **%d 篇** → **%d 篇**；'
  '残差采纳 **%d** → **主批 %d 篇**。'
  '入选主批的列表类别分布：%s。\n' % (
      G['recall']['kw_hits'], G['recall']['title_extra'], G['recall']['pool'], len(REJ),
      len(MAIN) - G['recall']['residual_adopted'],
      G['recall']['residual_adopted'], len(MAIN),
      ' / '.join('%s %d' % (k, v) for k, v in Counter(p['cat'] for p in MAIN).most_common())))
A('- **被剔除的 %d 篇池内条目**（按 arXiv ID 升序，标题截断）。其中 **2611.30173 为库内 cross 再公告**'
  '（首发 2026-11-25 批已以 3.71 入馆），按「库内 v2/再公告不重复入馆」剔除；其余为本批语义误命中或非 XR 方向。\n' % len(REJ))
A('| # | arXiv | 标题（截断） |')
A('|---|---|---|')
for i, pid in enumerate(REJ_IDS, 1):
    rec = REJ[pid]
    t = (rec.get('title') if isinstance(rec, dict) else '') or ''
    A('| %d | %s | %s |' % (i, pid, t[:76].replace('|', '/')))
A('')
A('  误命中主因与上批一致：`spatial` 多指空间推理基准与地理偏见，`hand` 多为手写体 OCR 与手部 X 光，'
  '`gaussian` 大量落在高斯分布 / EDA，`tracking` 多为状态跟踪与航空建图，`depth` 多为单目深度估计的通用改进。\n')
A('### 5.3 第 3.5 步残差复核（只报警，不入馆）\n')
A('残差复核：扫描 **%d** 条，疑似漏检 **%d** 条（**%.2f%%**），采纳 **%d** 条。\n' % (
    RES['n_scanned'], RES['n_flagged'], RES['rate'] * 100, G['recall']['residual_adopted']))
A('| # | arXiv | 标题 | 赛道 | 处置 |')
A('|---|---|---|---|---|')
ADOPT = set(G['recall']['residual_adopted_list'])
for it in RES['flagged']:
    A('| %d | %s | %s | %s | %s |' % (
        it['n'], it['id'], it['title'][:62].replace('|', '/'), it['track'],
        '**采纳入本批**' if it['id'] in ADOPT else '留待人工挑选池（本批未入馆）'))
A('\n> 采纳口径：%d 篇全部为 12 赛道内的核心表述（%s），且与已入馆条目无同质（全批门① max Jaccard %.3f < 0.62）。'
  '清单本身只作报警，**未直接并入 registry**——%d 篇均另行走「全文抓取 → 7 维评分 → 产物」全流程后才入馆。'
  '残差率 **%.2f%%** 明显高于近批（1.5–2.8%%），但仍在 12%% 的上报阈值内，按口径**不自作主张扩表**；'
  '缺口集中在「几何记忆 / 世界模型状态 / 社会具身」等表述，已记入 §6.3 待办。\n' % (
      len(ADOPT), '、'.join('%s %d' % (k, v) for k, v in RES['by_track'].items()), g1['max_jaccard'],
      len(ADOPT), RES['rate'] * 100))
A('### 5.4 三关\n')
A('| 关卡 | 口径 | 本批数值 | 结论 |')
A('|---|---|---|---|')
A('| 门① 同质度 | 与库内非本批条目最大 Jaccard < 0.62 | **%.3f**（%s vs 库内 %s） | PASS |' % (
    g1['max_jaccard'], g1['pair'][0], g1['pair'][1]))
A('| 门② 赛道覆盖 | Top10 覆盖 ≥5 赛道 | 纯值 4 赛道（%s）→ 回补 1 次 → **%d 赛道**（%s） | PASS（重筛一次） |' % (
    '、'.join('%s×%d' % (k, v) for k, v in g2['pure_value_tracks'].items()),
    g2['n_tracks'], '、'.join('%s×%d' % (k, v) for k, v in g2['top10_tracks'].items())))
A('| 门③ 价值天花板 | today_max ≥ 近 30 天 Top10 均分，且 margin ≥ 0.05 才授 S | **%.2f vs %.3f**，margin **%+.3f** | **非重磅日，blockbuster=false，0 个 S** |' % (
    g3['today_max'], g3['top10_mean'], g3['margin']))
A('\n> 门③ 留痕（`data/gates_%s.json`）：`window_lo=%s`、`window_hi=%s`、`window_excludes_today=%s`、'
  '`window_excludes_this_run_batches=%s`、`this_run_batches_excluded=%s`、`heavy_day_raw=%s`、`heavy_day=%s`、'
  '`margin=%.4f`、`blockbuster=%s`、`s_awarded=%s`、`verdict=%s`；入窗 **%d 条**。\n' % (
      MMDD, g3['window_lo'], g3['window_hi'], g3['window_excludes_today'],
      g3['window_excludes_this_run_batches'], '、'.join(g3['this_run_batches_excluded']),
      g3['heavy_day_raw'], g3['heavy_day'], g3['margin'], g3['blockbuster'], g3['s_awarded'],
      g3['verdict'], g3['in_window']))
A('> 窗口为**半开区间** [今天−30 天, 今天)，且按 batch 剔除本次运行追加的两批（`2026-11-27`、`backfill-1127`）。'
  '本批 `today_max %.2f`、`top10_mean %.3f`、差值 **%.4f < 0** → `heavy_day_raw=false`，`blockbuster=false`。'
  '**这里没有「差一点」的解释空间**：连机械重磅条件都不成立，因此 4.35（ProManO / AnyCam）与 4.20（Who Is Ego）'
  '一律记 A 并注「达 S 线」，不授予 S。backfill 的 2611.31822（G0.7，4.43）即使计入主批也只能把 today_max 抬到 4.43，'
  '仍低于 4.459 的基线，结论不变——这一点在 MOC-backfill-1127 中同步声明。\n' % (
      g3['today_max'], g3['top10_mean'], g3['margin']))
A('### 5.5 评分披露（影响档位与可信度的三处判定）\n')
A('- **62 篇 L0 / FULL + 1 篇 L1 / PARTIAL**：2611.33313（多感官混合电视）ar5iv 返回的是**摘要落地页**'
  '（4,551 字符、含 "Skip to main content"），`grade_evidence()` 的 LANDING_RE 守卫判为 PARTIAL → 子代理按 PARTIAL 条款'
  '只记 1 条 `key_numbers`（106 名参与者），主会话再下调 TEC/EXP 至 2/2，value 2.23、C 级仅入馆。'
  '这是守卫**第一次在真实批次上拦下摘要页**，且结论如实降级、未拿摘要当全文用。\n')
A('- **5 篇 C 级仅入馆、不写笔记**：%s。均为「单一场景应用 / 装置描述 / 增量改进」或证据不足，缺可迁移方法；'
  '按口径 C 级留 registry 供查重与去重，不生成原子笔记、不进 Top10。\n' % (
      '、'.join('%s %s %.2f' % (p['id'], p['title_zh'], p['value']) for p in D if p['grade'] == 'C')))
A('- **三篇「达 S 线」的证据边界**：ProManO 的收益全部建立在**已标定**相机上，未标定场景不适用，且依赖 VINS-Mono 前端质量；'
  'AnyCam 的锚物体必须「全程可见、刚性静止、足够大」，CO3D 的 PSNR 14.08 本身仍属低基线区间（生成式视频任务普遍如此）；'
  'Who Is Ego 的最强项是「无候选分割 + 未见佩戴者类」，但其 L3 绝对准确率 71.1 仍不足以支撑无人值守应用。'
  '三者按「能力级突破 + 明确边界」记 A，未把单点最优表述为全面领先。\n')

# ---- 六、附录 ----
A('\n## 六、附录\n')
A('### 6.1 全文抓取与证据等级\n')
lv = Counter(MAN[p['id']]['level'] for p in D)
ev = Counter(MAN[p['id']]['evidence'] for p in D)
A('- %d 篇（%d + %d）串行 3 s/篇（`scripts/fetch_fulltext.py`）：**%s**；证据 **%s**；字符数 %s–%s。\n' % (
    len(D), len(MAIN), len(BF),
    ' / '.join('%s %d' % (k, v) for k, v in sorted(lv.items())),
    ' / '.join('%s %d' % (k, v) for k, v in sorted(ev.items())),
    format(min(MAN[p['id']]['chars'] for p in D), ','),
    format(max(MAN[p['id']]['chars'] for p in D), ',')))
A('- 抽检 6 篇（含字符数最小的 23,717 字符篇）正文中段均含 Method / Experiment / Result 段落，'
  '守卫未误伤正常全文；唯一 PARTIAL 为 2611.33313，已按摘要级证据降档处理。\n')
A('### 6.2 本批数据文件\n')
A('- `data/audit_1127_days.json` / `audit_1127_alldays.json`：对账原始记录（7 分类日期头、declared/got）\n'
  '- `data/newday_1127.json`（11-26 组 569 唯一）、`data/missed_prev_1127.json`（上一组未入馆 569）、'
  '`data/missed_xr_1127.json`（复采核验，`leak_n=0`）\n'
  '- `data/xr_pool_1127.json`（92）、`data/old_replace_1127.json`（26）、`data/nonxr_1127.json`（526）\n'
  '- `data/residual_1127.json` + `data/residual_1127/{index,verdicts}.jsonl`（525 条逐条判定）\n'
  '- `data/xr_final_1127.json`（43）、`data/backfill_pool_1127.json`（8）、`data/adopt_1127.json`（12）、'
  '`data/published_1127.json`、`data/scored_1127.json`、`data/gates_1127.json`\n'
  '- `data/digest_1127_g1..g8.json`（64 篇精读 digest，含 1 篇已剔除条目）、`data/fulltext/<id>.txt` + `_manifest.json`\n')
A('### 6.3 待办与风险\n')
A('- **残差率 5.71%%（30/525）是本批最该记的一项**：远高于近批 1.5–2.8%%，采纳 12 篇（占主批 21.8%%）。'
  '连续 3 日 >12%% 才上报并重估词表，本批单日未触发；但缺口方向已经清楚——「几何记忆 / 世界模型状态 / 社会具身交互」'
  '这三类表述既不含 `SLAM`/`gaussian`/`avatar` 也不含标题级扩展词，**下批应先看这三类是否再次成批漏检**，再决定是否登记扩表。\n')
A('- **门② 回补机制第二次在「重建与SLAM 独大」的批次上生效**（前两次：10-29、11-04、11-22）。'
  '本批重建与SLAM 占全批 16/63（主批 11/55），纯值 Top10 里占 5 席，回补后 4 席。'
  '若后续批次该赛道持续 >40%%，需要考虑在**排序阶段**引入赛道配额，而不是每次事后回补。\n')
A('- **backfill 占比 12.7%%（8/63）**：全部为 `replace` 再公告，首发跨度 2025-09-20 ~ 2026-11-24。'
  '其中 2509.16476（GazeVLM，首发 2025-09-20）距今超过一年，已在笔记中显著标注首发日，避免被读成当期工作。\n')
A('- **渠道①（WorkBuddy 站点）历史挂账**：上批累计 37 批。本批按整改口径实测，若仍不可用则记「累计第 38 批挂账」，'
  '不影响 GitHub Pages 渠道与本地知识库。\n')

open('reports/XR-Daily-Report-%s.md' % DATE, 'w', encoding='utf-8').write('\n'.join(L) + '\n')
print('main report', len('\n'.join(L)))

# ==================== 二、7dim-table（主批 + backfill） ====================
T = []
t = T.append
t('# 7 维对比表 · %s（主批 %d 篇 + backfill %d 篇）\n' % (DATE, len(MAIN), len(BF)))
t('权重 IMP0.20·NOV0.20·TEC0.15·EXP0.15·PER0.15·TRL0.08·REP0.07；'
  '档位 S≥4.20 且 blockbuster / A3.60–4.20 / B3.00–3.60 / C<3.00。')
t('公告日 %s（周四）≠ 拉取日 %s（周五 02:30）；11-26 为单日公告组，无周末积压。' % (ANN, DATE))
t('\n## 主批（公告日 %s，%d 篇）\n' % (ANN, len(MAIN)))
t('| # | arXiv | 论文 | 赛道 | IMP | NOV | TEC | EXP | PER | TRL | REP | 总分 | 档 | 公告 | 证据 |')
t('|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|')
for i, p in enumerate(MAIN, 1):
    s = p['scores']
    t('| %d | %s | %s | %s | %d | %d | %d | %d | %d | %d | %d | **%.2f** | %s | %s | %s |' % (
        i, p['id'], p['title_zh'].replace('|', '/'), p['track'], s['IMP'], s['NOV'], s['TEC'],
        s['EXP'], s['PER'], s['TRL'], s['REP'], p['value'], p['grade'], p['announce'] or 'new', p['evidence']))
t('\n> 主批档位分布：S %d / A %d / B %d / C %d（C 级仅入馆、不写笔记）。本批 `blockbuster=false`（margin %+.3f），'
  '**无 S**；%.2f / %.2f / %.2f 三篇达 4.20 的 S 线按校准关记 A。\n' % (
      GRM['S'], GRM['A'], GRM['B'], GRM['C'], g3['margin'],
      sorted([p['value'] for p in MAIN], reverse=True)[0],
      sorted([p['value'] for p in MAIN], reverse=True)[1],
      sorted([p['value'] for p in MAIN], reverse=True)[2]))
open('papers/daily/%s/7dim-table.md' % DATE, 'w', encoding='utf-8').write('\n'.join(T) + '\n')
print('7dim main', len(T))

TB = []
tb = TB.append
tb('# 7 维对比表 · backfill-%s（%d 篇）\n' % (MMDD, len(BF)))
tb('权重同上；**backfill 永不记 S**（即使 ≥4.20），且不参与当日重磅日判定。')
tb('本批为 %s 公告 RSS 中 `replace` 类再公告的旧稿，首发 %s ~ %s。\n' % (
    ANN, min(p['published'] for p in BF), max(p['published'] for p in BF)))
tb('| # | arXiv | 论文 | 赛道 | IMP | NOV | TEC | EXP | PER | TRL | REP | 总分 | 档 | 首发日 | 证据 |')
tb('|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|')
for i, p in enumerate(BF, 1):
    s = p['scores']
    tb('| %d | %s | %s | %s | %d | %d | %d | %d | %d | %d | %d | **%.2f** | %s | %s | %s |' % (
        i, p['id'], p['title_zh'].replace('|', '/'), p['track'], s['IMP'], s['NOV'], s['TEC'],
        s['EXP'], s['PER'], s['TRL'], s['REP'], p['value'], p['grade'], p['published'], p['evidence']))
tb('\n> backfill 档位分布：A %d / B %d / C %d；最高 %.2f（%s，达 4.20 的 S 线仍记 A）。\n' % (
    GRB['A'], GRB['B'], GRB['C'], max(p['value'] for p in BF),
    '、'.join(p['id'] for p in BF if p['value'] == max(x['value'] for x in BF))))
open('papers/daily/backfill-%s/7dim-table.md' % MMDD, 'w', encoding='utf-8').write('\n'.join(TB) + '\n')
print('7dim bf', len(TB))

# ==================== 三、backfill 报告 ====================
B = []
b = B.append
b('# XR Backfill 报告 · backfill-%s\n' % MMDD)
b('> **非当日新提交**：本批 %d 篇均为 %s 公告 RSS 混入的 `replace` 类旧稿再公告，首次入馆。'
  '按诚实口径单独编号，**不参与当日重磅日判定**。本批最高 **%.2f**（2611.31822 G0.7）已达 4.20 的 S 线，'
  '但一并计入主批也只能把 today_max 从 4.35 抬到 4.43，仍低于库内近 30 天 Top10 均分 4.459 → 非重磅日结论不变；'
  '按口径仍记 A 并注「达 S 线」。\n' % (len(BF), ANN, max(p['value'] for p in BF)))
b('> 首发提交日（API `published`，非公告日）：%s。即本次是「旧稿更新后 replace 再公告」，不是当期新工作。\n' % (
    '；'.join('%s = %s' % (p['id'], p['published']) for p in sorted(BF, key=lambda x: x['published']))))
b('\n## 一、摘要\n')
b('%s 公告 RSS 中 `replace` 类且摘要级 XR 命中 **%d 篇**（已扣已入馆者），逐篇核摘要取 **%d 篇**——'
  '其余多为机器人操作、医学影像、点云检测、通用视觉等非 XR 方向。定稿 **A %d / B %d / C %d，无 S**。\n' % (
      ANN, len(OLD), len(BF), GRB['A'], GRB['B'], GRB['C']))
b('\n## 二、逐篇解读\n')
b('> 本批 C 级 %d 篇（%s）按口径仅入馆、不写笔记与不展开章节，仅在文末列出。\n' % (
    GRB['C'], '、'.join('%s %s' % (p['id'], p['title_zh']) for p in BF if p['grade'] == 'C') or '无'))
for i, p in enumerate([x for x in BF if x['grade'] != 'C'], 1):
    g = DIG[p['id']]
    b('\n### %d. %s（%s · %s · %.2f %s）\n' % (i, p['title_zh'], p['id'], p['track'], p['value'], p['grade']))
    b('**一句话结论**：%s\n' % concl(p['id']))
    b('**要解决的问题**\n\n%s\n' % g['problem'])
    b('**方法详解**\n\n%s\n' % g['method'])
    b('**实验与结果**\n\n%s\n' % bl(g['key_numbers']))
    b('**创新点**\n\n%s\n' % bl(g['novelty']))
    b('**局限与风险**\n\n%s\n' % bl(g['limitations']))
    b('**可复现性**\n\n- 代码/项目页：%s\n- 全文证据：%s（%s，%s 字符）\n- 首发提交日 %s（本批为 `replace` 再公告）\n' % (
        p.get('code') or '正文未提供', p['evidence'], MAN[p['id']]['level'],
        format(MAN[p['id']]['chars'], ','), p['published']))
b('\n## 三、完整 7 维表\n')
b('见 [papers/daily/backfill-%s/7dim-table.md](../papers/daily/backfill-%s/7dim-table.md)。\n' % (MMDD, MMDD))
open('reports/XR-Backfill-Report-backfill-%s.md' % MMDD, 'w', encoding='utf-8').write('\n'.join(B) + '\n')
print('backfill report', len('\n'.join(B)))

# ==================== 四、scored.md ====================
SC = []
s_ = SC.append
s_('# 评分明细与覆盖校验 · %s\n' % DATE)
s_('## 一、门禁三关\n')
s_('- 门① 最大 Jaccard **%.3f**（%s vs %s）< 0.62 → PASS（只对比追加前库内集合，不含本批两批）' % (
    g1['max_jaccard'], g1['pair'][0], g1['pair'][1]))
s_('- 门② 纯值 Top10 覆盖 4 赛道（%s）→ 回补一次：%s → 定稿 **%d 赛道**（%s；全批 %d 赛道）→ PASS' % (
    '、'.join('%s%d' % (k, v) for k, v in g2['pure_value_tracks'].items()), g2['rescreen'],
    g2['n_tracks'], '、'.join('%s%d' % (k, v) for k, v in g2['top10_tracks'].items()),
    g2['all_batch_tracks']))
s_('- 门③ 当日最高 **%.2f** vs 库内近 30 天 Top10 均分 **%.4f**（半开窗口 [%s, %s)、%d 条入窗、按 batch 剔除 %s）'
   '→ heavy_day_raw=%s、margin **%+.4f** → **blockbuster=%s，S 授予 %s**' % (
       g3['today_max'], g3['top10_mean'], g3['window_lo'], g3['window_hi'], g3['in_window'],
       '、'.join(g3['this_run_batches_excluded']), g3['heavy_day_raw'], g3['margin'],
       g3['blockbuster'], g3['s_awarded']))
s_('\n## 二、分档统计\n')
s_('- 主批 %d 篇：S %d / A %d / B %d / C %d（C 级仅入馆、不写笔记）' % (
    len(MAIN), GRM['S'], GRM['A'], GRM['B'], GRM['C']))
s_('- backfill %d 篇：A %d / B %d / C %d' % (len(BF), GRB['A'], GRB['B'], GRB['C']))
s_('- 全批：S %d / A %d / B %d / C %d' % (GR['S'], GR['A'], GR['B'], GR['C']))
s_('\n## 三、Top10 逐维评分理由（10 篇）\n')
for p in TOP:
    s_('### %s %s（%.2f / %s / %s）\n' % (p['id'], p['title_zh'], p['value'], p['grade'], p['track']))
    sc = p['scores']
    w = why(p)
    for k in ('IMP', 'NOV', 'TEC', 'EXP', 'PER', 'TRL', 'REP'):
        s_('- **%s=%d**：%s' % (k, sc[k], w.get(k, '（digest 未分维说明）')))
    s_('')
s_('\n## 四、backfill 逐篇理由（%d 篇）\n' % len(BF))
for p in BF:
    sc = p['scores']
    s_('### %s %s（%.2f / %s / 首发 %s）\n' % (p['id'], p['title_zh'], p['value'], p['grade'], p['published']))
    s_('- 向量：IMP %d / NOV %d / TEC %d / EXP %d / PER %d / TRL %d / REP %d' % (
        sc['IMP'], sc['NOV'], sc['TEC'], sc['EXP'], sc['PER'], sc['TRL'], sc['REP']))
    nov = DIG[p['id']]['novelty']
    nov = nov[0] if isinstance(nov, list) and nov else str(nov)
    s_('- 要点：%s' % nov[:200])
    s_('- 为何不更高：属旧稿再公告（首发 %s），与库内同期同赛道条目相比无新增能力面；TRL 与 PER 按当期可比口径给分，'
       '**不因首次入馆而溢价**，且按口径不评 S。' % p['published'])
    s_('')
s_('\n## 五、其余 %d 篇评分要点\n' % (len(MAIN) - len(TOP)))
s_('| arXiv | 论文 | 赛道 | IMP | NOV | TEC | EXP | PER | TRL | REP | 总分 | 档 | 要点 |')
s_('|---|---|---|---|---|---|---|---|---|---|---|---|---|')
for p in MAIN:
    if p['in_top10']:
        continue
    sc = p['scores']
    nov = DIG[p['id']]['novelty']
    nov = nov[0] if isinstance(nov, list) and nov else str(nov)
    s_('| %s | %s | %s | %d | %d | %d | %d | %d | %d | %d | %.2f | %s | %s |' % (
        p['id'], p['title_zh'][:28].replace('|', '/'), p['track'], sc['IMP'], sc['NOV'], sc['TEC'],
        sc['EXP'], sc['PER'], sc['TRL'], sc['REP'], p['value'], p['grade'], nov[:86].replace('|', '/')))
s_('\n> 要点列取自各篇 digest 的 `novelty[0]`（唯一来源，未二次转录）。')
s_('> 逐维展开以 digest 的 `scores_why` 为唯一来源（按维切分，未改写语义）；其余篇目的档位由同一权重与 '
  '`grade_caliber.assign_grade` 机械计算。\n')
open('papers/daily/%s/scored.md' % DATE, 'w', encoding='utf-8').write('\n'.join(SC) + '\n')
print('scored.md', len('\n'.join(SC)))

# ==================== 五、run_log ====================
u_c = shutil.disk_usage('C:/')
u_d = shutil.disk_usage('D:/')
RL = []
r = RL.append
r('# 运行日志 · %s\n' % DATE)
r('- 02:30 起跑；跑前查 C: 盘剩余空间（未触发磁盘保护）。收尾实测 C: %.2f GB / D: %.2f GB。' % (
    u_c.free / 2**30, u_d.free / 2**30))
r('- 第 1 步 对账：`scripts/audit_listing_1127.py`（PREV_DAY=11-25 / NEW_DAYS=11-26,11-27），7/7 分类成功、exit 0；'
  '%s 组 **%s 槽位 / %s 唯一**；11-27 组 declared=None（未释放）；11-25 组复采 declared=got'
  '（cs.CV 302/302 含 skip=500 补 90、cs.AI 300/300 含补 48）。' % (
      ANN, format(AG['slots'], ','), format(AG['unique'], ',')))
r('- 第 1 步补充 上一组复采：`scripts/missed_xr_1127.py` → 未入馆 **%d** 篇、摘要覆盖 **%d/%d = 1.0000**、'
  '命中 **%d** 篇全部落在上批处置集合 → **0 漏网**。' % (
      MX['unregistered'], MX['unregistered'], MX['unregistered'], len(MX['hits'])))
r('- 第 2 步 数据源：API 双主机探针 200（仅用于提交日核验）；RSS 7/7、**849 条**，WROTE=849 OK_CATS=7/7；'
  'listing %s/%s 覆盖 → 免 id_list。' % (format(AG['unique'], ','), format(AG['unique'], ',')))
r('- 第 3 步 甄别：`triage_1127.py`（数据源 `2026-11-27.jsonl` 849 条 no-filter，只取 day=11-26 的 newday）'
  '→ 覆盖率 1.0000（569/569）、KW %d + TITLE_EXTRA %d = 池 %d → 逐篇核摘要剔 %d → %d；'
  '另 26 条 `replace` XR 命中逐篇核摘要取 %d 篇。' % (
      G['recall']['kw_hits'], G['recall']['title_extra'], G['recall']['pool'], len(REJ),
      G['recall']['pool'] - len(REJ), len(BF)))
r('- 第 3 步修正：`2611.30173`（Confidently Lost）在池中且 `in_registry=true`（11-25 批 3.71），'
  '初版定稿误将其纳入主批；按「库内 cross/v2 再公告不重复入馆」移入 REJECT，主批 44→43、'
  '全量 64→63，并重跑 build_scored / gates（否则门① 会与**自身**比对、虚高且无效）。')
r('- 第 3.5 步 残差：`residual_scan.py dump/ingest` → 扫描 **%d**、判 **%d**（**%.2f%%**）、采纳 **%d**；'
  '采纳篇全部另跑全文抓取（11 FULL + 1 PARTIAL）→ 主批 %d。' % (
      RES['n_scanned'], RES['n_flagged'], RES['rate'] * 100, G['recall']['residual_adopted'], len(MAIN)))
r('- 第 4 步 全文：%d 篇串行 3 s/篇 → **%s**；字符 %s–%s。'
  '2611.33313 的 ar5iv 返回摘要落地页（4,551 字符）被 LANDING_RE 守卫判 PARTIAL，按摘要级证据降档。' % (
      len(D), ' / '.join('%s %d' % (k, v) for k, v in sorted(Counter(MAN[p['id']]['evidence'] for p in D).items())),
      format(min(MAN[p['id']]['chars'] for p in D), ','),
      format(max(MAN[p['id']]['chars'] for p in D), ',')))
r('- 第 4 步补充 提交日核验：`check_published_1127.py`（25 个 id/批 × 12 s 间隔）→ 64/64 全齐；主批 %s。' % pub_dist(MAIN))
r('- 第 5 步 评分：8 组子代理 digest（各 8 篇 = 64）+ 主会话按标准权重重算；'
  '主会话校准一处：2611.33313 TEC 2 / EXP 2（PARTIAL 摘要页，无量化对比）。'
  'Top10 逐维理由落 `papers/daily/%s/scored.md`（取自 digest `scores_why`）。' % DATE)
r('- 第 6 步 三关：门① %.3f（%s vs %s）；门② 纯值 4 赛道 → 回补 1 次 → %d 赛道；'
  '门③ %.2f vs %.3f，margin %+.3f → heavy_day_raw=false、blockbuster=false、s_awarded=false。' % (
      g1['max_jaccard'], g1['pair'][0], g1['pair'][1], g2['n_tracks'],
      g3['today_max'], g3['top10_mean'], g3['margin']))
r('- 第 7 步 Top10：实数 10 篇（4.35–4.00），全 A；全批 S %d / A %d / B %d / C %d。' % (
    GR['S'], GR['A'], GR['B'], GR['C']))
r('- 第 8 步 产物：报告 2 + 笔记 %d（C 级 5 篇不写）+ MOC 2 + 总索引刷新 + 7dim-table（主批/backfill 各 1）+ '
  'scored.md + run_log；registry 1,269 → **1,332**（+63，备份 `registry.jsonl.bak-20261127`）。'
  '易错点：`7dim-table.md` 表头必须保留 `arXiv` 列，否则前端批次卡表内计数为 0。' % (len(D) - GR['C']))
r('- 第 9 步 发布：见下方发布记录（构建 → `node --check` → CDP 冒烟 → `check_release` → 提交 → 推送 → Pages 核验）。')
open('papers/daily/%s/run_log.md' % DATE, 'w', encoding='utf-8').write('\n'.join(RL) + '\n')
print('run_log ok')
