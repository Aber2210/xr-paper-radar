# -*- coding: utf-8 -*-
"""把 STATUS.md 更新到 2026-11-25 批次（定点替换 + 插入，不整体重写）。"""
import os

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
os.chdir(ROOT)
P = 'STATUS.md'
s = open(P, encoding='utf-8').read()
ls = s.split('\n')


def rep(old, new, cnt=1):
    global s
    assert s.count(old) == cnt, ('锚点命中数不符', s.count(old), old[:70])
    s = s.replace(old, new)


# ---- 顶部 ----
rep('- **最后更新**：2026-11-24（每日批次：**11-23 周一公告批次** 主批 41 篇 + backfill 9 篇；24A/17B + 7A/2B，**非重磅日无 S**，门③ 4.27 < 4.432）',
    '- **最后更新**：2026-11-25（每日批次：**11-24 周二公告批次**（含 11-21/11-22 周末积压）主批 68 篇 + backfill 6 篇；'
    '44A/22B/2C + 2A/4B，**非重磅日无 S**，门③ 4.21 < 4.432 / margin −0.222）')
rep('- **当前库况**：registry 1132 / notes 768 / daily 77 ｜ 最新真实批次 2026-11-24（41 篇，24A/17B，无 S，门③ margin −0.162）｜ 11-24 卡片 count=41 / backfill 卡 count=9 ｜ 门③ 现算基线 **4.432**（窗口 [2026-10-25, 2026-11-24)，464 条入窗）',
    '- **当前库况**：registry **1206** / notes **840** / daily **79** ｜ 最新真实批次 2026-11-25（68 篇，44A/22B/2C，无 S，门③ margin −0.222）'
    '｜ 11-25 卡片 count=68 / backfill-1125 卡 count=6 ｜ 门③ 现算基线 **4.432**（窗口 [2026-10-26, 2026-11-25)，514 条入窗）')

# ---- O-1 计数 ----
rep('| 托管侧重签后可恢复；累计 **35 批**（2026-10-21 ~ 11-24，按每日运行计含状态日） |',
    '| 托管侧重签后可恢复；累计 **36 批**（2026-10-21 ~ 11-25，按每日运行计含状态日） |')

# ---- 新增 O-12 / O-13 ----
anchor = [l for l in ls if l.startswith('| O-11 |')]
assert len(anchor) == 1
rep(anchor[0], anchor[0] + '\n'
    '| O-12 | `fetch_fulltext.py` 缺「`chars < 8000` 且命中 landing 特征 → 强制 PARTIAL」守卫 | 证据等级会系统性虚高（ar5iv 摘要落地页被判 FULL） | '
    '**连续两批靠人眼抽看兜底**（11-24 的 2611.27633、11-25 的 2611.29647 / 2611.30012）| 下批必须落到脚本里；否则 TEC/EXP 断言不可信 |\n'
    '| O-13 | `deploy-pages.yml` 的 **`schedule` 触发**必失败：`No artifacts named "github-pages" were found` | 定时重部署不生效（push 触发正常） | '
    '未改 workflow（本批如实登记）；build job 仅在 push 事件产出 artifact | 若需定时重部署，给 build job 加 `if: github.event_name != \'schedule\'` 之外的补跑路径 |')

# ---- §4 最近一批 ----
old4 = [l for l in ls if l.startswith('- **最近一批**：')][0]
rep(old4,
    '- **最近一批**：`2026-11-25` 判 **PASS**（G1 **1206/840/79** 三计数一致；G2 `gates_1125.json` 字段齐、险过四字段在；'
    'G3 无 S 泄漏、backfill 记 S=0；残差 rate **2.45%（22/899）**；门③ 4.21 vs 4.432 → margin −0.222、非重磅日无 S；'
    'HoloSplat 4.21 达 S 线按 skill §8.6.3 记 A）——见 `data/verdicts.jsonl`（共 5 批）。'
    '上一批 `2026-11-24` 判 PASS（G1 1132/768/77；残差 2.2%）；`2026-11-22` / `2026-11-23` 为状态日 WARN（R 项未执行，未补造）。')

# ---- §5 新自检块 ----
NEW = '''**2026-11-25（11-24 周二公告批次，含 11-21/11-22 周末积压）**

- [x] `python scripts/check_release.py` → **PASS**（G1 **1206/840/79** ｜ G2 `gates_1125.json` 无缺、险过四字段齐 ｜ G3 本批授予S=False、backfill 记S=0、泄漏 0 ｜ R 残差 **2.5%**）；`--record` 已写入 `data/verdicts.jsonl`（共 **5** 批）
- [x] `python scripts/check_audit_guard.py` 无违规（**28 份**脚本：守卫 10 / 基线豁免 18 / 违规 0；本日新增 `audit_listing_1125.py` 自带 `ok_cats<7 → exit 2` 且在任何 `json.dump(...missed...)` 之前，并传入第三参数窗口下界 2026-11-23）
- [x] 对账 `audit_listing_1125.py` **7/7 分类 exit 0**：11-24 组 **1,285 槽位 / 1,045 唯一**（CV 494/GR 13/HC 61/MM 18/RO 191/AI 485/IV 23）；11-25 组 `declared=None`（未释放）；11-23 组复采逐分类 declared=got（506 槽位 / 404 唯一）；未入馆 363 篇摘要级 **363/363** 覆盖（0 篇缺摘要），命中 40 篇**全部**在上批处置集合 → **0 漏网**
- [x] `data/gates_1125.json` 四字段齐全且布尔自洽（`today_max=4.21`、`heavy_day_raw=false`、`margin=-0.222`、`blockbuster=false`、`s_awarded=false`）+ `window_excludes_today/this_run_batches` 与 `this_run_batches_excluded` 留痕 + `window_lo/hi = 2026-10-26 / 2026-11-25`、`in_window=514`
- [x] 残差复核：扫描 **899**、判 **22**（**2.45%**）、采纳 **6** → 主批 68；`verdicts.jsonl` 逐条 **899 行**（分母坑复现：先写满 899 行才得 2.45%，只写命中行会得 100%）
- [x] 全文：74 篇串行 3 s/篇 → **72 L0/FULL + 2 L1/PARTIAL**（2611.29647 / 2611.30012 为 ar5iv 摘要落地页，手动改判并同步 `.txt` 头）；字符 4,581–312,858。**守卫仍未落地，见 O-12**
- [x] 前端重建 `verified: {papers:1206, notes:840, batches:79}`；11-25 卡 `表内=68`（44A/22B/2C）、backfill-1125 卡 `表内=6`（2A/4B），均非 0（`7dim-table.md` 保留 `arXiv` 列）；`BATCH_LABELS` 补 2 条中文标签
- [x] 前端冒烟 **PASS**：papersEqDisk / notesEqDisk / batchesEqDisk 全 true；5 标签渲染 4/2/2/3/1；排序 8 项单调性 + 隐藏开关（localStorage 落盘/复原）+ 弹层三组交互；`nCards=79`；lastThree 首卡 2026-11-25；`PAGE_ERRORS: none`
- [x] 总索引刷新：状态注记追加 11-25、速查入口换「最新一期 MOC-2026-11-25 / 上一期 11-24 / 笔记 840 篇」、批次表加 2 行（2026-11-25、backfill-1125）、页尾加 2 个明细段、页首换 1,206（1,300 → 1,334 行）；自检「新增 2 行 ↔ 新增 2 段」通过（历史遗留 2 处不匹配为 2026-10-07 缺行与 backfill-2603-2609 行标签异名，已白名单）
- [x] 交付前抽查 `title == id` / `len(title)<12`：新增 74 行 **0 命中**；新增档位 0 S / 46 A / 26 B / 2 C，与 gates/scored 一致
- [x] 渠道② 已实推并核验：本地 commit **`80207fa`** → 增量推送（**140** 变更 / 2,214 未变 / 删除 0）→ 远端 main **`9c94e831`** → deploy run **`45468795909` success（31 s）**；线上 **HTTP 200 / 6,533,825 bytes**、含 `const DATA`、LF 归一化 md5 **`f5a589aa…`** 与本地**逐字节相等**
- [x] 渠道① 不可用：ToolSearch 无 `workbuddy_sites_deploy`，`xr-paper-hub.app.workbuddy.host` 根与 `/index.html` 均 **403 / 3,174 bytes** → 报告与 run_log 均写「渠道①不可用（累计第 **36** 批挂账）」，**未声称已发布**

'''
i5 = [i for i, l in enumerate(ls) if l.startswith('**2026-11-24（11-23 周一公告批次）**')]
assert len(i5) == 1
rep('**2026-11-24（11-23 周一公告批次）**\n', NEW + '**2026-11-24（上一批，留档）**\n')

open(P, 'w', encoding='utf-8').write(s)
print('STATUS.md updated, %d chars' % len(s))
for k in ('1206', '9c94e831', '第 **36** 批', 'O-12', 'O-13'):
    print('  contains %-12s %s' % (k, k in s))
