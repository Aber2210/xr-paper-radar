# -*- coding: utf-8 -*-
"""刷新 papers/MOC/MOC-总索引.md 到 2026-11-26 批次（定点替换 + 追加，不重写全文）。

做四件事：
  1) 头部「累计 / 跨度」与 registry 对齐，并追加 11-26 批次计数；
  2) 在 2026-11-25 状态注记后插入 2026-11-26 状态注记（公告日≠拉取日、三关数值、证据等级、剔除原因、残差复核）；
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
D = json.load(open('data/scored_1126.json', encoding='utf-8'))
G = json.load(open('data/gates_1126.json', encoding='utf-8'))
RES = json.load(open('data/residual_1126.json', encoding='utf-8'))
MX = json.load(open('data/missed_xr_1126.json', encoding='utf-8'))
MAN = json.load(open('data/fulltext/_manifest.json', encoding='utf-8'))
g1, g2, g3 = G['gate1'], G['gate2'], G['gate3']

TOP = [p for p in D if p['in_top10']]
TOP.sort(key=lambda r: (-r['value'], -r['scores']['IMP'], -r['scores']['NOV'], r['id']))
BF = [p for p in D if p['batch'].startswith('backfill')]
BF.sort(key=lambda r: (-r['value'], -r['scores']['IMP'], -r['scores']['NOV'], r['id']))
GR = {}
for p in D:
    GR[p['grade']] = GR.get(p['grade'], 0) + 1

reg = sum(1 for line in open('papers/library/registry.jsonl', encoding='utf-8') if line.strip())
notes = len([f for f in os.listdir('papers/notes') if f.endswith('.md')])
daily = len([d for d in os.listdir('papers/daily') if os.path.isdir(os.path.join('papers/daily', d))])
moc = len([f for f in os.listdir('papers/MOC') if f.endswith('.md')])
chars = [MAN[p['id']]['chars'] for p in D]

txt = open(P, encoding='utf-8').read()
ls = txt.split('\n')
orig_len = len(ls)

# ---------- 1) 头部计数 ----------
assert '累计 **1,206 篇**' in ls[3], ls[3][:120]
ls[3] = ls[3].replace('累计 **1,206 篇**', '累计 **%s 篇**' % format(reg, ','))
ls[3] = ls[3].replace('跨度 2026-09-15 ~ 2026-11-24', '跨度 2026-09-15 ~ 2026-11-26')
ls[3] = ls[3].rstrip('。') + (
    ' **11-26 周四处理 11-25 公告批次（主批 55 篇 S3/A18/B28/C6 + backfill-1126 补录 8 篇 A6/B1/C1，'
    '门③ 4.57 vs 4.432 / margin +0.138、blockbuster=true，本批授 3 个 S）**。')

# ---------- 2) 状态注记 ----------
GP = g2['top10_tracks']
NOTE = (
 '> **状态注记（2026-11-26）**：周四 02:30，处理 **2026-11-25（周三）公告批次**（公告日≠拉取日，诚实口径；'
 '11-26 组**尚未释放**——拉取早于 11-26 00:00 UTC = 08:00 北京时间；11-25 为**单日公告组、无周末积压**）。'
 '**listing 对账**（`scripts/audit_listing_1126.py`，PREV_DAY=11-24 / NEW_DAYS=11-25,11-26）：7/7 分类成功（exit 0），'
 '最新公告日全部为 **2026-11-25**；11-26 组 `declared=None / got=0`。'
 '**11-25 组 761 槽位 / 624 篇唯一**（CV 302 / GR 11 / HC 21 / MM 7 / RO 111 / AI 300 / IV 9，逐分类 declared=got）；'
 '上一公告组 11-24 复采逐分类 **declared=got**（494/13/61/18/191/485/23 = 1,285 槽位），与上批一致、**无新增漏跑窗口**。'
 '**上一公告组复核**：未入馆 **977 篇 = 1,045 − 68**（上批主批已入馆），用 11-25 / 11-26 两份 RSS 全量核摘要 '
 '**977/977 覆盖（1.0000、0 篇缺摘要）**，摘要/标题级命中 **84 篇全部落在上批处置集合**'
 '（`nonxr_1125 ∪ xr_pool_1125 ∪ old_replace_1125 ∪ scored_1125`）→ **0 漏网**（`data/missed_xr_1126.json`：`leak_n=0`）。'
 '**数据源**：API 双主机探针 200（仅用于提交日核验）；RSS 7 分类 `--no-filter` 去重 **921 条**（`WROTE=921`、`OK_CATS=7/7`，'
 '任一分类失败即 exit 2，本批未触发），**listing 624 篇 100%% 被 RSS 覆盖（缺收 0）** → 免 API `id_list` 枚举。'
 '**召回三层**：摘要级 KW **61** + 标题级扩展词补扫 **36** = **97 篇** → 逐篇核摘要剔 **53 篇误命中**（明细见 `data/nonxr_1126.json` 527 条全量）'
 '→ **44 篇**；**第 3.5 步残差复核**（`data/residual_1126.json`，527 条逐条判定落 `verdicts.jsonl`）扫描 **527 条**、'
 '判 **8 条**（**%.2f%%**）、**采纳 8 篇**；另通读补入 3 篇（2611.31757 Xtream / 2611.32034 BodyWeave / 2611.32396 PRC4D）→ **主批 55 篇**。'
 '**backfill**：11-25 公告 RSS 中 `replace` 类 XR 命中 20 篇 → 二筛取 **8 篇**（首发 2025-08-24 ~ 2026-10-08，updated 均 11-23/24）。'
 '**提交日核验**（API `published`，63/63 全齐）：主批 **11-24×50 / 11-23×5**（RSS `published` 为公告时间戳，不可当提交日）。'
 '**全文**：63 篇串行 3 s/篇 → **63 L0 / FULL**（`evidence: FULL` 63、**无 PARTIAL**；`chars < 8000 且命中 landing 特征 → 强制 PARTIAL` '
 '守卫已写入 `fetch_fulltext.py` 的 `grade_evidence()`，O-12 关闭）；字符 %s–%s。'
 '**三关**：门① max Jaccard **%.3f**（%s vs 库内 %s）；'
 '门② 定稿 Top10 **%d 赛道**（%s；全批 %d 赛道，**未重筛**）；'
 '门③ 当日最高 **%.2f** vs 库内近 30 天 Top10 均分 **%.3f**（半开窗口 [%s, %s)、**%d 条入窗**、'
 '按 batch 剔除 `%s`、现算）→ **margin %+.3f**，`heavy_day_raw=%s`、`blockbuster=%s`、**授 S**；'
 '**3 个 S 级**：2611.32198 MoGe-4D 4.57、2611.32445 A Mesh to Remember 4.40、2611.32523 AirLeg 4.38。OUTDATED / SUPERSEDED **0**。'
 '主批 **%d S / %d A / %d B / %d C**（C 级 %d 篇仅入馆不写笔记）；backfill-1126 **8 篇 %d A / %d B / %d C**（最高 3.85，按口径不评 S、不并入重磅日判定）。'
 'registry 1,206 → **%s**（+63，备份 `registry.jsonl.bak-20261126`）；原子笔记 **%d**、daily **%d**、MOC **%d**。\n' % (
     RES['rate'] * 100, format(min(chars), ','), format(max(chars), ','),
     g1['max_jaccard'], g1['pair'][0], g1['pair'][1], g2['n_tracks'],
     '、'.join('%s %d' % (k, v) for k, v in GP.items()), g2['all_batch_tracks'],
     g3['today_max'], g3['top10_mean'], g3['window_lo'], g3['window_hi'], g3['in_window'],
     '、'.join(g3['this_run_batches_excluded']), g3['margin'], g3['heavy_day_raw'], g3['blockbuster'],
     GR.get('S', 0), GR.get('A', 0), GR.get('B', 0), GR.get('C', 0),
     len([p for p in D if p['grade'] == 'C' and not p['batch'].startswith('backfill')]),
     len([p for p in BF if p['grade'] == 'A']), len([p for p in BF if p['grade'] == 'B']),
     len([p for p in BF if p['grade'] == 'C']),
     format(reg, ','), notes, daily, moc))
idx = [i for i, line in enumerate(ls) if line.startswith('> **状态注记（2026-11-25）**')]
assert len(idx) == 1, idx
ls.insert(idx[0] + 1, NOTE)


# ---------- 3) 速查入口 ----------
def sub1(old, new):
    global txt
    i = '\n'.join(ls)
    assert i.count(old) == 1, ('速查入口锚点不唯一/未找到', old[:60], i.count(old))
    ls[:] = i.replace(old, new).split('\n')


sub1('| 最新一期 | [MOC · 2026-11-25](./MOC-2026-11-25.md) |',
     '| 最新一期 | [MOC · 2026-11-26](./MOC-2026-11-26.md) |')
sub1('| 上一期 | [MOC · 2026-11-24](./MOC-2026-11-24.md)（11-22 / 11-23 为状态日，无 MOC） |',
     '| 上一期 | [MOC · 2026-11-25](./MOC-2026-11-25.md) |')
sub1('| 某篇论文的细节 | [原子笔记目录](../notes/)（现有 840 篇） |',
     '| 某篇论文的细节 | [原子笔记目录](../notes/)（现有 %d 篇） |' % notes)
old_run = [line for line in ls if line.startswith('| 最新运行状态 |')][0]
new_run = ('| 最新运行状态 | [运行报告 2026-11-26](../../reports/XR-Daily-Report-2026-11-26.md)'
           '（**11-25 周三公告批次：主批 55 篇 + backfill 8 篇** = S3/A18/B28/C6 与 A6/B1/C1，'
           '**重磅日授 3 个 S、门③ 4.57 > 4.432（margin +0.138、blockbuster=true）**；公告日≠拉取日；'
           'listing 761 槽位 / 624 篇唯一，RSS 921 条 100% 覆盖（缺收 0）→ 免 id_list；'
           'KW 61 + 标题补扫 36 = 97 → 剔 53 → 44，残差 527 判 8（1.52%）采纳 8 + 通读补 3 → 55；'
           '全文 63 L0/FULL 无 PARTIAL；Top10 覆盖 5 赛道（未重筛）；'
           '11-24 组复采 977 篇未入馆、84 篇命中全在上批处置集合 → 0 漏网）'
           '｜上一期 [运行报告 2026-11-25](../../reports/XR-Daily-Report-2026-11-25.md)'
           '（11-24 公告批次 68 + 6 篇，门③ 4.21 < 4.432 / margin −0.222，无 S）'
           '｜最新真实批次 [MOC 2026-11-26](./MOC-2026-11-26.md) |')
sub1(old_run, new_run)

# ---------- 4) 批次索引 + 明细段 ----------
ROW_MAIN = (
 '| 2026-11-26 | [MOC-2026-11-26](./MOC-2026-11-26.md) | XR 55（Top10 实数 10）· 3S/18A/28B/6C · '
 '**重磅日（授 3 S，门③ 4.57 > 4.432，margin +0.138）** | 11-25 周三公告批次真新提交 55 篇'
 '（11-24×50 / 11-23×5）；listing 761 槽位 / 624 唯一、RSS 921 条缺收 0 → 免 id_list；'
 'KW 61 + 标题补扫 36 = 97 → 剔 53 → 44，残差 527 判 8（1.52%）采纳 8 + 通读补 3 → 55；'
 '全文 55 L0/FULL；门② 5 赛道未重筛 |')
ROW_BF = (
 '| backfill-1126 | [MOC-backfill-1126](./MOC-backfill-1126.md) | 补录 8（6A/1B/1C）· 非当日新提交 | '
 '11-25 公告 RSS 混入 `replace` 再公告 8 篇（首发 2025-08-24 ~ 2026-10-08）；最高 2601.22046 / 2610.11810 3.85；'
 '按口径不评 S、不参与当日重磅日判定 |')
anchor = [i for i, line in enumerate(ls) if line.startswith('| backfill-1125 |')]
assert len(anchor) == 1, anchor
ls.insert(anchor[0] + 1, ROW_BF)
ls.insert(anchor[0] + 1, ROW_MAIN)

S3 = [p for p in D if p['grade'] == 'S']
S3.sort(key=lambda r: -r['value'])
DET = ['', '### 2026-11-26 新增（Top10 实数 10 篇：3 S / 7 A，重磅日）', '',
       '> 11-25（周三）公告批次，公告日≠拉取日（拉取 11-26 02:30）。门③ 现算 4.57 vs 4.432'
       '（margin +0.138，580 条入窗、剔除本批两批）→ `blockbuster=true`，按「S ≥4.20 且重磅」授 %d 个 S：'
       '%s。主批 55 篇 3S/18A/28B/6C（6 篇 C 级仅入馆不写笔记）；全文 63 篇全 L0/FULL。' % (
           len(S3), ' / '.join('%.2f %s' % (p['value'], p['title_zh']) for p in S3)), '',
       '| # | 论文 | 赛道 | 分值 | 等级 | 证据 |', '|---:|---|---|---:|---|---|']
for i, p in enumerate(TOP, 1):
    DET.append('| %d | %s | %s | %.2f | %s | %s |' % (
        i, p['title_zh'], p['track'], p['value'], p['grade'], p['evidence']))
DET += ['', '### backfill-1126 补录（8 篇：6 A / 1 B / 1 C，非当日新提交）', '',
        '> 11-25 公告 RSS 混入的 `replace` 类旧稿再公告 8 篇，首次入馆。首发 2025-08-24 ~ 2026-10-08'
        '（`updated` 均为 2026-11-23/24）。单独编号，不参与当日重磅日判定；按口径不评 S。', '',
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
for need in ('2026-11-26', 'backfill-1126'):
    assert need in keys, need
assert 'MOC · 2026-11-26' in out and '现有 %d 篇' % notes in out
assert '累计 **%s 篇**' % format(reg, ',') in out
assert 'leak_n' in out or '0 漏网' in out
print('MOC 总索引刷新完成：行数 %d -> %d；registry %d / notes %d / daily %d / moc %d / 漏网 %d' % (
    orig_len, len(ls2), reg, notes, daily, moc, MX['leak_n']))
