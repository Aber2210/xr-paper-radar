# -*- coding: utf-8 -*-
"""刷新 papers/MOC/MOC-总索引.md 到 2026-11-27 批次（定点替换 + 追加，不重写全文）。

做四件事：
  1) 头部「累计 / 跨度」与 registry 对齐，并追加 11-27 批次计数；
  2) 在 2026-11-26 状态注记后插入 2026-11-27 状态注记（公告日≠拉取日、三关数值、证据等级、剔除原因、残差复核、cross 去重）；
  3) 刷新「一、速查入口」四行；
  4) 「批次索引」表追加 2 行 + 文末追加 2 个 Top10 明细段。
自检：明细段必须能在批次表找到对应行；历史遗留 2 处不匹配列入白名单。
"""
import json
import os
import re

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
os.chdir(ROOT)
P = 'papers/MOC/MOC-总索引.md'
D = json.load(open('data/scored_1127.json', encoding='utf-8'))
G = json.load(open('data/gates_1127.json', encoding='utf-8'))
RES = json.load(open('data/residual_1127.json', encoding='utf-8'))
MX = json.load(open('data/missed_xr_1127.json', encoding='utf-8'))
MAN = json.load(open('data/fulltext/_manifest.json', encoding='utf-8'))
g1, g2, g3 = G['gate1'], G['gate2'], G['gate3']

TOP = [p for p in D if p['in_top10']]
TOP.sort(key=lambda r: (-r['value'], -r['scores']['IMP'], -r['scores']['NOV'], r['id']))
BF = [p for p in D if p['batch'].startswith('backfill')]
BF.sort(key=lambda r: (-r['value'], -r['scores']['IMP'], -r['scores']['NOV'], r['id']))
MAIN = [p for p in D if not p['batch'].startswith('backfill')]
GR = {}
for p in D:
    GR[p['grade']] = GR.get(p['grade'], 0) + 1
GRM = {}
for p in MAIN:
    GRM[p['grade']] = GRM.get(p['grade'], 0) + 1

reg = sum(1 for line in open('papers/library/registry.jsonl', encoding='utf-8') if line.strip())
notes = len([f for f in os.listdir('papers/notes') if f.endswith('.md')])
daily = len([d for d in os.listdir('papers/daily') if os.path.isdir(os.path.join('papers/daily', d))])
moc = len([f for f in os.listdir('papers/MOC') if f.endswith('.md')])
chars = [MAN[p['id']]['chars'] for p in D]

txt = open(P, encoding='utf-8').read()
ls = txt.split('\n')
orig_len = len(ls)

# ---------- 1) 头部计数 ----------
assert '累计 **1,269 篇**' in ls[3], ls[3][:120]
ls[3] = ls[3].replace('累计 **1,269 篇**', '累计 **%s 篇**' % format(reg, ','))
ls[3] = ls[3].replace('跨度 2026-09-15 ~ 2026-11-26', '跨度 2026-09-15 ~ 2026-11-27')
ls[3] = ls[3].rstrip('。') + (
    ' **11-27 周五处理 11-26 公告批次（主批 55 篇 = 43 新 + 12 残差采纳，A37/B13/C5 + '
    'backfill-1127 补录 8 篇 A7/B1，门③ 4.35 vs 4.459 / margin −0.109、blockbuster=false，本批无 S）**。')

# ---------- 2) 状态注记 ----------
GP = g2['top10_tracks']
NOTE = (
 '> **状态注记（2026-11-27）**：周五 02:30，处理 **2026-11-26（周四）公告批次**（公告日≠拉取日，诚实口径；'
 '11-27 组**尚未释放**——拉取早于 11-27 00:00 UTC = 08:00 北京时间；11-26 为**单日公告组、无周末积压**）。'
 '**listing 对账**（`scripts/audit_listing_1127.py`，PREV_DAY=11-25 / NEW_DAYS=11-26,11-27）：7/7 分类成功（exit 0），'
 '最新公告日全部为 **2026-11-26**；11-27 组 `declared=None / got=0`。'
 '**11-26 组 695 槽位 / 569 篇唯一**（CV 288 / GR 10 / HC 20 / MM 7 / RO 109 / AI 248 / IV 13，逐分类 declared=got）；'
 '上一公告组 11-25 复采逐分类 **declared=got**（CV 302/302 含 `skip=500` 补 90、AI 300/300 含补 48），**无新增漏跑窗口**。'
 '**上一公告组复核**：未入馆 **569 篇 = 624 − 55**（上批主批已入馆），用 11-26 / 11-27 两份 RSS 全量核摘要 '
 '**569/569 覆盖（1.0000、0 篇缺摘要）**，摘要/标题级命中 **53 篇全部落在上批处置集合**'
 '（`scored_1126 ∪ xr_pool_1126 ∪ nonxr_1126 ∪ old_replace_1126`）→ **0 漏网**（`data/missed_xr_1127.json`：`leak_n=0`）。'
 '**数据源**：API 双主机探针 200（仅用于提交日核验）；RSS 7 分类 `--no-filter` 去重 **849 条**（`WROTE=849`、`OK_CATS=7/7`，'
 '任一分类失败即 exit 2，本批未触发），**listing 569 篇 100%% 被 RSS 覆盖（缺收 0）** → 免 API `id_list` 枚举。'
 '**召回三层**：摘要级 KW **67** + 标题级扩展词补扫 **25** = **92 篇** → 逐篇核摘要剔 **49 篇**'
 '（其中 **2611.30173 为库内 cross 再公告**：11-25 批已以 3.71 入馆，按「库内 v2/再公告不重复入馆」剔除——'
 '该篇初版定稿误纳入主批，复核时发现并回退，全量 64 → 63、**重跑 build_scored / gates**，否则门① 会与自身比对而虚高）'
 '→ **43 篇**；**第 3.5 步残差复核**（`data/residual_1127.json`，525 条逐条判定落 `verdicts.jsonl`）扫描 **525 条**、'
 '判 **30 条**（**%.2f%%**，显著高于近批 1.5–2.8%%）、**采纳 12 篇**（全部另跑全文抓取与评分，未直接并库）→ **主批 55 篇**。'
 '**backfill**：11-26 公告 RSS 中 `replace` 类 XR 命中 26 篇 → 二筛取 **8 篇**（首发 2025-09-20 ~ 2026-11-24）。'
 '**提交日核验**（API `published`，64/64 全齐）：主批 **11-25×47 / 11-24×8**（RSS `published` 为公告时间戳，不可当提交日）。'
 '**全文**：63 篇串行 3 s/篇 → **62 L0 / FULL + 1 L1 / PARTIAL**（2611.33313 的 ar5iv 返回摘要落地页，4,551 字符，'
 '`grade_evidence()` 的 LANDING_RE 守卫判 PARTIAL 并按摘要级证据下调 TEC/EXP → 2.23 C 级仅入馆）；字符 %s–%s。'
 '**三关**：门① max Jaccard **%.3f**（%s vs 库内 %s）；'
 '门② 纯值 Top10 仅 **4 赛道**（重建与SLAM×5）→ **回补一次**：剔 2611.34932（4.01，该赛道第 5 篇、仍入馆记 A）'
 '补 2611.33467（4.00，世界模型与仿真）→ 定稿 **%d 赛道**（%s；全批 %d 赛道）；'
 '门③ 当日最高 **%.2f** vs 库内近 30 天 Top10 均分 **%.3f**（半开窗口 [%s, %s)、**%d 条入窗**、'
 '按 batch 剔除 `%s`、现算）→ **margin %+.3f**，`heavy_day_raw=%s`、`blockbuster=%s`、**授 S %s**；'
 '4.35（ProManO / AnyCam）与 4.20（Who Is Ego）**达 S 线但按校准关记 A**；backfill 最高 2611.31822 G0.7 4.43 亦记 A。'
 'OUTDATED / SUPERSEDED **0**。'
 '主批 **%d S / %d A / %d B / %d C**（C 级 %d 篇仅入馆不写笔记）；backfill-1127 **8 篇 %d A / %d B / %d C**（最高 4.43，按口径不评 S）。'
 'registry 1,269 → **%s**（+63，备份 `registry.jsonl.bak-20261127`）；原子笔记 **%d**、daily **%d**、MOC **%d**。\n' % (
     RES['rate'] * 100, format(min(chars), ','), format(max(chars), ','),
     g1['max_jaccard'], g1['pair'][0], g1['pair'][1], g2['n_tracks'],
     '、'.join('%s %d' % (k, v) for k, v in GP.items()), g2['all_batch_tracks'],
     g3['today_max'], g3['top10_mean'], g3['window_lo'], g3['window_hi'], g3['in_window'],
     '、'.join(g3['this_run_batches_excluded']), g3['margin'], g3['heavy_day_raw'], g3['blockbuster'],
     ('否（0 个）' if not g3['s_awarded'] else '是'),
     GRM.get('S', 0), GRM.get('A', 0), GRM.get('B', 0), GRM.get('C', 0),
     len([p for p in MAIN if p['grade'] == 'C']),
     len([p for p in BF if p['grade'] == 'A']), len([p for p in BF if p['grade'] == 'B']),
     len([p for p in BF if p['grade'] == 'C']),
     format(reg, ','), notes, daily, moc))
idx = [i for i, line in enumerate(ls) if line.startswith('> **状态注记（2026-11-26）**')]
assert len(idx) == 1, idx
ls.insert(idx[0] + 1, NOTE)


# ---------- 3) 速查入口 ----------
def sub1(old, new):
    global txt
    i = '\n'.join(ls)
    assert i.count(old) == 1, ('速查入口锚点不唯一/未找到', old[:60], i.count(old))
    ls[:] = i.replace(old, new).split('\n')


sub1('| 最新一期 | [MOC · 2026-11-26](./MOC-2026-11-26.md) |',
     '| 最新一期 | [MOC · 2026-11-27](./MOC-2026-11-27.md) |')
sub1('| 上一期 | [MOC · 2026-11-25](./MOC-2026-11-25.md) |',
     '| 上一期 | [MOC · 2026-11-26](./MOC-2026-11-26.md) |')
sub1('| 某篇论文的细节 | [原子笔记目录](../notes/)（现有 896 篇） |',
     '| 某篇论文的细节 | [原子笔记目录](../notes/)（现有 %d 篇） |' % notes)
old_run = [line for line in ls if line.startswith('| 最新运行状态 |')][0]
new_run = ('| 最新运行状态 | [运行报告 2026-11-27](../../reports/XR-Daily-Report-2026-11-27.md)'
           '（**11-26 周四公告批次：主批 55 篇（43 新 + 12 残差采纳）+ backfill 8 篇** = A37/B13/C5 与 A7/B1，'
           '**非重磅日无 S、门③ 4.35 < 4.459（margin −0.109、blockbuster=false）**；公告日≠拉取日；'
           'listing 695 槽位 / 569 篇唯一，RSS 849 条 100% 覆盖（缺收 0）→ 免 id_list；'
           'KW 67 + 标题补扫 25 = 92 → 剔 49（含 1 篇库内 cross 再公告 2611.30173）→ 43，'
           '残差 525 判 30（5.71%）采纳 12 → 55；全文 62 L0/FULL + 1 L1/PARTIAL；'
           'Top10 纯值 4 赛道 → 回补 1 次 → 5 赛道；'
           '11-25 组复采 569 篇未入馆、53 篇命中全在上批处置集合 → 0 漏网）'
           '｜上一期 [运行报告 2026-11-26](../../reports/XR-Daily-Report-2026-11-26.md)'
           '（11-25 公告批次 55 + 8 篇，门③ 4.57 > 4.432 / margin +0.138，授 3 个 S）'
           '｜最新真实批次 [MOC 2026-11-27](./MOC-2026-11-27.md) |')
sub1(old_run, new_run)

# ---------- 4) 批次索引 + 明细段 ----------
ROW_MAIN = (
 '| 2026-11-27 | [MOC-2026-11-27](./MOC-2026-11-27.md) | XR 55（Top10 实数 10）· 0S/37A/13B/5C · '
 '**非重磅日（无 S，门③ 4.35 < 4.459，margin −0.109）** | 11-26 周四公告批次真新提交 43 + 残差采纳 12 = 55 篇'
 '（11-25×47 / 11-24×8）；listing 695 槽位 / 569 唯一、RSS 849 条缺收 0 → 免 id_list；'
 'KW 67 + 标题补扫 25 = 92 → 剔 49 → 43，残差 525 判 30（5.71%）采纳 12 → 55；'
 '全文 62 L0/FULL + 1 L1/PARTIAL；门② 纯值 4 赛道 → 回补 1 次 → 5 赛道 |')
ROW_BF = (
 '| backfill-1127 | [MOC-backfill-1127](./MOC-backfill-1127.md) | 补录 8（7A/1B）· 非当日新提交 | '
 '11-26 公告 RSS 混入 `replace` 再公告 8 篇（首发 2025-09-20 ~ 2026-11-24）；最高 2611.31822 G0.7 4.43'
 '（达 S 线仍记 A）；按口径不评 S、不参与当日重磅日判定 |')
anchor = [i for i, line in enumerate(ls) if line.startswith('| backfill-1126 |')]
assert len(anchor) == 1, anchor
ls.insert(anchor[0] + 1, ROW_BF)
ls.insert(anchor[0] + 1, ROW_MAIN)

DET = ['', '### 2026-11-27 新增（Top10 实数 10 篇：10 A，非重磅日无 S）', '',
       '> 11-26（周四）公告批次，公告日≠拉取日（拉取 11-27 02:30）。门③ 现算 4.35 vs 4.459'
       '（margin −0.109，626 条入窗、剔除本批两批）→ `heavy_day_raw=false`、`blockbuster=false`，**不授 S**：'
       '4.35 ProManO / AnyCam、4.20 Who Is Ego 均达 4.20 的 S 线，按「险过不授」直接记 A。'
       '门② 纯值 Top10 仅 4 赛道 → 回补一次（剔 2611.34932 4.01、补 2611.33467 4.00）→ 5 赛道。'
       '主批 55 篇 0S/37A/13B/5C（5 篇 C 级仅入馆不写笔记）；全文 62 L0/FULL + 1 L1/PARTIAL。', '',
       '| # | 论文 | 赛道 | 分值 | 等级 | 证据 |', '|---:|---|---|---:|---|---|']
for i, p in enumerate(TOP, 1):
    DET.append('| %d | %s | %s | %.2f | %s | %s |' % (
        i, p['title_zh'], p['track'], p['value'], p['grade'], p['evidence']))
DET += ['', '### backfill-1127 补录（8 篇：7 A / 1 B，非当日新提交）', '',
        '> 11-26 公告 RSS 混入的 `replace` 类旧稿再公告 8 篇，首次入馆。首发 2025-09-20 ~ 2026-11-24。'
        '单独编号，不参与当日重磅日判定；按口径不评 S——最高 2611.31822（G0.7，4.43）即使计入主批也只能把'
        'today_max 抬到 4.43，仍低于基线 4.459，非重磅日结论不变。', '',
        '| # | 论文 | 赛道 | 分值 | 等级 | 证据 |', '|---:|---|---|---:|---|---|']
for i, p in enumerate(BF, 1):
    DET.append('| %d | %s | %s | %.2f | %s | %s |' % (
        i, p['title_zh'], p['track'], p['value'], p['grade'], p['evidence']))
DET.append('')

while ls and ls[-1].strip() == '':
    ls.pop()
ls += DET

out = '\n'.join(ls)
if not out.endswith('\n'):
    out += '\n'
open(P, 'w', encoding='utf-8').write(out)

# ---------- 自检 ----------
ls2 = open(P, encoding='utf-8').read().split('\n')
i_tab = [i for i, line in enumerate(ls2) if line.startswith('## 批次索引（全量）')][0]
i_det = max(i for i, line in enumerate(ls2) if line.startswith('### 2026-10-02 窗口新增'))
keys = set()
for line in ls2[i_tab:i_det]:
    if line.startswith('| ') and '[MOC-' in line:
        keys.add(re.match(r'\| ([^|]+?) \|', line).group(1).strip())
missing = []
n_det = 0
for line in ls2[i_det:]:
    if not line.startswith('### '):
        continue
    n_det += 1
    m = re.match(r'(backfill-[\d\-]+|\d{4}-\d{2}-\d{2})', line[4:])
    k = m.group(1) if m else None
    if k not in keys:
        missing.append(k)
WHITELIST = {'2026-10-07', 'backfill-2603-2609'}
unexplained = [k for k in missing if k not in WHITELIST]
print('rows(linked) %d | detail sections %d | new rows 2 | new sections 2' % (len(keys), n_det))
print('明细段未在批次表找到行：%s（白名单历史遗留除外：%s）' % (missing, sorted(WHITELIST & set(missing))))
assert not unexplained, ('新增明细段缺少批次表行', unexplained)
for need in ('2026-11-27', 'backfill-1127'):
    assert need in keys, need
assert 'MOC · 2026-11-27' in out and '现有 %d 篇' % notes in out
assert '累计 **%s 篇**' % format(reg, ',') in out
assert 'leak_n' in out or '0 漏网' in out
print('MOC 总索引刷新完成：行数 %d -> %d；registry %d / notes %d / daily %d / moc %d / 漏网 %d' % (
    orig_len, len(ls2), reg, notes, daily, moc, MX['leak_n']))
