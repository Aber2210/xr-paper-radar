# -*- coding: utf-8 -*-
"""刷新 papers/MOC/MOC-总索引.md 到 2026-11-25 批次。

做四件事（全部为定点替换，不做全文重写）：
  1) 头部「文献库累计 / 跨度」与实际 registry 对齐，并追加 11-24、11-25 两批的批次计数；
  2) 在 11-24 状态注记后插入 11-25 状态注记（含公告日≠拉取日、积压窗口、三关数值、证据等级、剔除原因）；
  3) 刷新「一、速查入口」四行；
  4) 「批次索引」表追加 2 行 + 文末追加 2 个 Top10 明细段。

自检：新增的 2 个明细段必须能在批次表找到对应行；历史遗留 2 处不匹配（2026-10-07 缺行、
backfill-2603-2609 行标签写作「2026-10-09 (backfill)」）列入白名单并在输出中显式打印。
"""
import json
import os
import re

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
os.chdir(ROOT)
P = 'papers/MOC/MOC-总索引.md'
D = json.load(open('data/scored_1125.json', encoding='utf-8'))
G = json.load(open('data/gates_1125.json', encoding='utf-8'))
RES = json.load(open('data/residual_1125.json', encoding='utf-8'))
g1, g2, g3 = G['gate1'], G['gate2'], G['gate3']

TOP = [p for p in D if p['in_top10']]
TOP.sort(key=lambda r: (-r['value'], -r['scores']['IMP'], -r['scores']['NOV'], r['id']))
BF = [p for p in D if p['batch'].startswith('backfill')]
BF.sort(key=lambda r: (-r['value'], r['id']))

reg = sum(1 for l in open('papers/library/registry.jsonl', encoding='utf-8') if l.strip())
notes = len([f for f in os.listdir('papers/notes') if f.endswith('.md')])
daily = len([d for d in os.listdir('papers/daily') if os.path.isdir(os.path.join('papers/daily', d))])
moc = len([f for f in os.listdir('papers/MOC') if f.endswith('.md')])

txt = open(P, encoding='utf-8').read()
ls = txt.split('\n')
orig_len = len(ls)

# ---------- 1) 头部计数 ----------
assert '累计 **1,082 篇**' in ls[3], ls[3][:80]
ls[3] = ls[3].replace('累计 **1,082 篇**', '累计 **%s 篇**' % format(reg, ','))
ls[3] = ls[3].replace('跨度 2026-09-15 ~ 2026-11-21', '跨度 2026-09-15 ~ 2026-11-24')
ls[3] = ls[3].rstrip('。') + (
    ' **11-24 周二处理 11-23 公告批次（41 篇 XR 新稿 24A/17B，非重磅日无S；'
    'backfill-1124 补录 9 篇 7A/2B）**；**11-25 周三处理 11-24 公告批次（68 篇 XR 新稿 44A/22B/2C + '
    'backfill-1125 补录 6 篇 2A/4B，非重磅日无S，门③ 4.21 < 4.432 / margin −0.222）**。')

# ---------- 2) 状态注记 ----------
GP = g2['top10_tracks']
NOTE = (
 '> **状态注记（2026-11-25）**：周三 02:30，处理 **2026-11-24（周二）公告批次**（公告日≠拉取日，诚实口径；'
 '11-25 组**尚未释放**——拉取早于 11-25 00:00 UTC = 08:00 北京时间；11-21（周六）/ 11-22（周日）为 `skipDays` '
 '无公告段，其提交并入 11-24 公告批次统一释放，**故本批同时是周末积压批**）。'
 '**listing 对账**（`scripts/audit_listing_1125.py`，PREV_DAY=11-23 / NEW_DAYS=11-24,11-25 / 窗口下界 2026-11-23）：'
 '7/7 分类成功（exit 0），最新公告日全部为 **2026-11-24**；11-25 组 `declared=None / got=0`。'
 '**11-24 组 1,285 槽位 / 1,045 篇唯一**（CV 494 / GR 13 / HC 61 / MM 18 / RO 191 / AI 485 / IV 23）；'
 '11-23 组复采逐分类 **declared=got**（506 槽位 / 404 唯一）。'
 '**上一公告组复核**：未入馆 **363 篇 = 404 − 41**（上批主批已入馆），用 11-23/11-24 两份 RSS 核摘要 '
 '**363/363 覆盖（1.0000、0 篇缺摘要）**，摘要/标题级命中 **40 篇全部落在上批处置集合**'
 '（`nonxr_1124 ∪ xr_pool_1124 ∪ backfill_1124 ∪ scored_1124`）→ **0 漏网**（`data/missed_xr_1125.json` 为空对象）。'
 '**数据源**：API 双主机 200（仅用于提交日核验）；RSS 7 分类 `--no-filter` 去重 **1,547 条**（`WROTE=1547`、`OK_CATS=7/7`，'
 '任一分类失败即 exit 2，本批未触发），**listing 1,045 篇 100%% 被 RSS 覆盖（缺收 0）** → 免 API `id_list` 枚举。'
 '**召回三层**：摘要级 KW **100** + 标题级扩展词补扫 **46** = **146 篇** → 逐篇核摘要剔 **84 篇误命中**'
 '（机器人操作 / 控制 / 自动驾驶 27、遥感测绘雷达与 BIM 13、医学与生物医学 10、通用 LLM/VLM 空间推理 16、'
 '生成式通用视觉 10、音频/OCR/安全/纯数学 8）→ **62 篇**；**第 3.5 步残差复核**（`data/residual_1125.json`，'
 '899 条逐条判定落 `verdicts.jsonl`）扫描 **899 条**、判 **22 条**（**%.2f%%**）、**采纳 6 篇** → **主批 68 篇**。'
 '**backfill**：`replace` 条目 502 条、未入馆且摘要级 XR 命中 35 篇 → 逐篇核摘要取 **6 篇**（首发 2025-11-25 ~ 2026-10-30）。'
 '**提交日核验**（API `published`，74/74 全齐）：主批 **11-23×29 / 11-21×17 / 11-22×14**，'
 '其余 11-20 / 11-19 / 11-18 / 11-17 / 11-16 / 11-04 / 10-05 / 09-18 各 1（RSS `published` 为公告时间戳，不可当提交日）。'
 '**全文**：74 篇串行 3 s/篇 → **72 L0/FULL + 2 L1/PARTIAL**'
 '（2611.29647 5,105 字符、2611.30012 4,581 字符：ar5iv 仅返回摘要落地页、无正文节，'
 '手动改判 `PARTIAL` 并同步 `.txt` 头，TEC/EXP 按摘要级下调）；字符 4,581–312,858。'
 '**三关**：门① max Jaccard **%.3f**（2611.28802 vs 库内 arXiv:2609.23436）；'
 '门② 定稿 Top10 **%d 赛道**（%s；全批 12 赛道，**未重筛**）；'
 '门③ 当日最高 **%.2f** vs 库内近 30 天 Top10 均分 **%.3f**（半开窗口 [%s, %s)、**%d 条入窗**、'
 '按 batch 剔除 `%s`、现算）→ **非重磅日无 S**（margin **−%.3f**，`heavy_day_raw=false`、`blockbuster=false`）；'
 'HoloSplat 4.21 已过 4.20 线仍按口径记 A。OUTDATED / SUPERSEDED **0**。'
 '主批 **0 S / 44 A / 22 B / 2 C**（C 级 2611.28027 无代码可穿戴验证工具链 2.85、2611.30552 语音 AI + 化身装置 1.85，'
 '仅入馆不写笔记）；backfill-1125 **6 篇 2 A / 4 B**（最高 2608.04701 UniView 3.77，按口径不评 S、不并入重磅日判定）。'
 'registry 1,132 → **%s**（+74，备份 `registry.jsonl.bak-20261125`）；原子笔记 **%d**、daily **%d**、MOC **%d**。'
 '**连续两批共性风险**：`fetch_fulltext.py` 的「`chars < 8000` 且命中 landing 特征 → 强制 PARTIAL」守卫仍未落地，'
 '本批两篇 PARTIAL 依旧是人眼抽看发现。\n' % (
     RES['rate'] * 100, g1['max_jaccard'], g2['n_tracks'],
     '、'.join('%s %d' % (k, v) for k, v in GP.items()), g3['today_max'], g3['top10_mean'],
     g3['window_lo'], g3['window_hi'], g3['in_window'], '、'.join(g3['this_run_batches_excluded']),
     abs(g3['margin']), format(reg, ','), notes, daily, moc))
idx = 60
assert ls[idx].startswith('> **状态注记（2026-11-24）**'), ls[idx][:40]
ls.insert(idx + 1, NOTE)

# ---------- 3) 速查入口 ----------
def sub1(old, new):
    global txt
    i = '\n'.join(ls)
    assert i.count(old) == 1, ('速查入口锚点不唯一/未找到', old[:50], i.count(old))
    ls[:] = i.replace(old, new).split('\n')


sub1('| 最新一期 | [MOC · 2026-11-24](./MOC-2026-11-24.md) |',
     '| 最新一期 | [MOC · 2026-11-25](./MOC-2026-11-25.md) |')
sub1('| 上一期 | [MOC · 2026-11-21](./MOC-2026-11-21.md)（11-22 / 11-23 为状态日，无 MOC） |',
     '| 上一期 | [MOC · 2026-11-24](./MOC-2026-11-24.md)（11-22 / 11-23 为状态日，无 MOC） |')
sub1('| 某篇论文的细节 | [原子笔记目录](../notes/)（现有 768 篇） |',
     '| 某篇论文的细节 | [原子笔记目录](../notes/)（现有 %d 篇） |' % notes)
old_run = [l for l in ls if l.startswith('| 最新运行状态 |')][0]
new_run = ('| 最新运行状态 | [运行报告 2026-11-25](../../reports/XR-Daily-Report-2026-11-25.md)'
           '（**11-24 周二公告批次（含 11-21/11-22 周末积压）：主批 68 篇 + backfill 6 篇** = 44A/22B/2C 与 2A/4B，'
           '**非重磅日无 S、门③ 4.21 < 4.432（margin −0.222）**；公告日≠拉取日；listing 1,285 槽位 / 1,045 篇唯一，'
           'RSS 1,547 条 100% 覆盖（缺收 0）→ 免 id_list；KW 100 + 标题补扫 46 = 146 → 剔 84 → 62，'
           '残差 899 判 22（2.45%）采纳 6 → 68；全文 72 L0/FULL + 2 PARTIAL；Top10 覆盖 6 赛道（未重筛）；'
           '11-23 组复采 363 篇未入馆、40 篇命中全在上批处置集合 → 0 漏网）'
           '｜上一期 [运行报告 2026-11-24](../../reports/XR-Daily-Report-2026-11-24.md)'
           '（11-23 公告批次 41 + 9 篇，门③ 4.27 < 4.432 / margin −0.162）'
           '｜最新真实批次 [MOC 2026-11-25](./MOC-2026-11-25.md) |')
sub1(old_run, new_run)

# ---------- 4) 批次索引 + 明细段 ----------
ROW_MAIN = (
 '| 2026-11-25 | [MOC-2026-11-25](./MOC-2026-11-25.md) | XR 68（Top10 实数 10）· 0S/44A/22B/2C · '
 '**非重磅日（无S，门③ 4.21 < 4.432，margin −0.222）** | 11-24 周二公告批次真新提交 68 篇'
 '（11-23×29 / 11-21×17 / 11-22×14 + 长尾 8 篇更早提交；周末 11-21/11-22 `skipDays` 并入本批）；'
 'listing 1,285 槽位 / 1,045 唯一、RSS 1,547 条缺收 0 → 免 id_list；KW 100 + 标题补扫 46 = 146 → 剔 84 → 62，'
 '残差 899 判 22（2.45%）采纳 6 → 68；全文 66 L0/FULL + 2 L1/PARTIAL；门② 6 赛道未重筛 |')
ROW_BF = (
 '| backfill-1125 | [MOC-backfill-1125](./MOC-backfill-1125.md) | 补录 6（2A/4B）· 非当日新提交 | '
 '11-24 公告 RSS 混入 `replace` 再公告 6 篇（首发 2025-11-25 ~ 2026-10-30）；最高 2608.04701 UniView 3.77；'
 '按口径不评 S、不参与当日重磅日判定 |')
anchor = [i for i, l in enumerate(ls) if l.startswith('| backfill-1124 |')]
assert len(anchor) == 1
ls.insert(anchor[0] + 1, ROW_BF)
ls.insert(anchor[0] + 1, ROW_MAIN)

DET = ['', '### 2026-11-25 新增（Top10 实数 10 篇：全 A，非重磅日无 S——HoloSplat 4.21 达 S 线但门③ 判非重磅）', '',
       '> 11-24（周二）公告批次（含 11-21/11-22 周末积压），公告日≠拉取日（拉取 11-25 02:30）。'
       '门③ 现算 4.21 vs 4.432（margin −0.222，514 条入窗、剔除本批两批）→ `blockbuster=false`；'
       '主批 68 篇 44A/22B/2C（2 篇 C 级仅入馆不写笔记）；全文 66 L0/FULL + 2 L1/PARTIAL。', '',
       '| # | 论文 | 赛道 | 分值 | 等级 | 证据 |', '|---:|---|---|---:|---|---|']
for i, p in enumerate(TOP, 1):
    DET.append('| %d | %s | %s | %.2f | %s | %s |' % (
        i, p['title_zh'], p['track'], p['value'], p['grade'], p['evidence']))
DET += ['', '### backfill-1125 补录（6 篇：2 A / 4 B，非当日新提交）', '',
        '> 11-24 公告 RSS 混入的 `replace` 类旧稿再公告 6 篇，首次入馆。首发 2025-11-25（2511.20578，v2 于 2026-11-23 更新）'
        '至 2026-10-30。单独编号，不参与当日重磅日判定；按口径不评 S。', '',
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
i_tab = [i for i, l in enumerate(ls2) if l.startswith('## 批次索引（全量）')][0]
i_det = max(i for i, l in enumerate(ls2) if l.startswith('### 2026-10-02 窗口新增'))
keys = set()
for l in ls2[i_tab:i_det]:
    if l.startswith('| ') and '[MOC-' in l:
        keys.add(re.match(r'\| ([^|]+?) \|', l).group(1).strip())
missing = []
n_det = 0
for l in ls2[i_det:]:
    if not l.startswith('### '):
        continue
    n_det += 1
    m = re.match(r'(backfill-[\d\-]+|\d{4}-\d{2}-\d{2})', l[4:])
    k = m.group(1) if m else None
    if k not in keys:
        missing.append(k)
WHITELIST = {'2026-10-07', 'backfill-2603-2609'}
unexplained = [k for k in missing if k not in WHITELIST]
print('rows(linked) %d | detail sections %d | new rows 2 | new sections 2' % (len(keys), n_det))
print('明细段未在批次表找到行：%s（白名单历史遗留除外：%s）' % (missing, sorted(WHITELIST & set(missing))))
assert not unexplained, ('新增明细段缺少批次表行', unexplained)
for need in ('2026-11-25', 'backfill-1125'):
    assert need in keys, need
assert 'MOC · 2026-11-25' in out and '现有 %d 篇' % notes in out
assert '累计 **%s 篇**' % format(reg, ',') in out
print('MOC 总索引刷新完成：行数 %d -> %d；registry %d / notes %d / daily %d / moc %d' % (
    orig_len, len(ls2), reg, notes, daily, moc))
