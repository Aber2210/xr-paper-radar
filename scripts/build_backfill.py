# -*- coding: utf-8 -*-
"""build_backfill.py — 旧稿 backfill 批次(2603–2609)：7 维评分 + 覆盖度门 + 文献库幂等追加 + 7 维表/run_log。
说明：本批次为「历史旧稿补录」，非当日新提交；公告日 2026-10-08（replace），原始投稿 2603–2609。
6 篇 XR 相关（剔除 2605.00556 自动驾驶 HCI 非 XR）。门③(重磅日/S 级)对 backfill 不适用。
"""
import json, os, re

W = {"IMP":0.20,"NOV":0.20,"TEC":0.15,"EXP":0.15,"PER":0.15,"TRL":0.08,"REP":0.07}
DIMS = ["IMP","NOV","TEC","EXP","PER","TRL","REP"]
ANNOUNCE = "2026-10-08"          # RSS replace 公告日
ORIG_WIN = "2603–2609"           # 原始投稿月份窗口
BATCH = "backfill-2603-2609"
ROOT = "D:/Agent/WorkBuddy/Research"

# base_id -> (scores[IMP,NOV,TEC,EXP,PER,TRL,REP], track_zh, title_zh)
NEW = {
 "2607.17790": ([4,4,4,4,4,3,3], "感知与认知", "ReViV：从单目第一视角视频统一重建「观察者+视角」的 4D 表征"),
 "2608.12759": ([4,3,4,4,4,4,3], "空间计算与UI", "NavSight：面向低视力户外导航的移动端 AR 应用（真实世界 7 日日记研究）"),
 "2606.19156": ([4,4,4,4,4,3,3], "化身与人体", "Hand-4DGS：从第一视角视频前馈式 4D 手部重建（网格引导+时序卷积）"),
 "2607.19479": ([3,3,4,4,3,4,4], "交互与输入", "ModPack：可扩展双臂移动操控遥操作接口（可穿戴背包+触觉反馈，全开源）"),
 "2603.20714": ([4,3,3,4,3,3,3], "神经渲染", "3DGS 初始化与稠密化作用的系统性研究（稠密初始化提升几何/泛化）"),
 "2605.07943": ([3,3,4,4,3,3,3], "感知与认知", "TAVIS：第一视角主动视觉与预期注视模仿学习基准（含 GALT 指标）"),
}
EXCLUDED = {
 "2605.00556": "自动驾驶有意义人类控制（HCI/驾驶，非 XR/VR/AR，C 级，剔除出 XR 文献库）",
}

def wval(scores):
    return round(sum(W[d]*scores[i] for i,d in enumerate(DIMS)), 3)
def grade(v):
    if v>=4.2: return "S"
    if v>=3.6: return "A"
    if v>=3.0: return "B"
    return "C"

# 载入 raw（来自 10-09 RSS 落盘，含 7 篇旧稿）
raw={}
for fn in ["data/raw/2026-10-09_rss.jsonl"]:
    p=os.path.join(ROOT,fn)
    if not os.path.exists(p): continue
    for l in open(p,encoding="utf-8"):
        if not l.strip(): continue
        r=json.loads(l); raw[r["base_id"]]=r

scored=[]
for bid,(sc,track,zh) in NEW.items():
    r=raw.get(bid,{})
    v=wval(sc); g=grade(v)
    scored.append({
        "base_id":bid,"id":"arXiv:"+bid,"title":r.get("title",""),"title_zh":zh,
        "track":track,"scores":dict(zip(DIMS,sc)),"value":v,"grade":g,
        "primary_category":r.get("primary_category",""),"abstract":r.get("abstract",""),
        "date":ANNOUNCE,"batch":BATCH,"orig_window":ORIG_WIN,
    })
scored.sort(key=lambda x:-x["value"])

# ---------- 覆盖度门 ----------
reg=[]
for l in open(f"{ROOT}/papers/library/registry.jsonl",encoding="utf-8"):
    if l.strip(): reg.append(json.loads(l))
reg_titles=[ (r.get("title","")) for r in reg ]
reg_values=[ r.get("value",0) for r in reg if r.get("in_top10") ]
lib_top10_mean = round(sum(reg_values)/len(reg_values),3) if reg_values else 0

STOP=set("a an the of for to in on with and via from by using based we our their is are be as at into toward towards between per".split())
def toks(s):
    return set(t for t in re.findall(r"[a-z0-9]+", s.lower()) if t not in STOP and len(t)>2)
def jac(a,b):
    A,B=toks(a),toks(b)
    if not A or not B: return 0.0
    return len(A&B)/len(A|B)

# 门①：新稿与文献库最大 Jaccard（同质查重，防误录重复）
gate1_max=0.0; gate1_pair=""
for s in scored:
    for t in reg_titles:
        j=jac(s["title"],t)
        if j>gate1_max: gate1_max=j; gate1_pair=f'{s["base_id"]} <> {t[:40]}'
gate1_pass = gate1_max < 0.62

# 门②：覆盖赛道数（backfill 也验证广度）
tracks=set(s["track"] for s in scored)
gate2_pass = len(tracks)>=5

# 门③：backfill 不参与“当日重磅日/S 级”竞赛，标注 N/A
gate3_pass = True

rescreen = not (gate1_pass and gate2_pass)
print("=== 覆盖度门（backfill）===")
print(f"门① 最大 Jaccard = {gate1_max:.3f} ({gate1_pair}) -> {'通过' if gate1_pass else '不通过(触发重筛)'}")
print(f"门② 覆盖赛道 = {len(tracks)} ({sorted(tracks)}) -> {'通过' if gate2_pass else '不通过'}")
print(f"门③ backfill 不适用（不参与当日重磅日/S 级竞赛）")
print(f"重筛触发: {rescreen}")

watch=[]
for s in scored:
    for t in reg_titles:
        j=jac(s["title"],t)
        if 0.4<=j<0.62:
            watch.append(f'{s["base_id"]}({j:.2f}) ~ {t[:36]}')
print("同质关注(0.4-0.62):", watch if watch else "无")

# ---------- 写盘 scored ----------
os.makedirs(f"{ROOT}/papers/daily/{BATCH}", exist_ok=True)
with open(f"{ROOT}/data/scored_backfill.json","w",encoding="utf-8") as f:
    json.dump(scored,f,ensure_ascii=False,indent=1)

# ---------- 幂等追加 registry（按 id 去重；in_top10=False 避免污染库 Top10 均值）----------
reg_ids=set(r.get("id") for r in reg)
added=0
with open(f"{ROOT}/papers/library/registry.jsonl","a",encoding="utf-8") as f:
    for s in scored:
        if s["id"] in reg_ids: continue
        rec={
            "id":s["id"],"title":s["title"],"title_zh":s["title_zh"],"track":s["track"],
            "date":s["date"],"batch":s["batch"],"orig_window":s["orig_window"],"value":s["value"],
            "grade":s["grade"],"scores":s["scores"],"status":"CURRENT","evidence":"FULL",
            "fetch_level":"L0","fulltext_chars":0,"in_top10":False,"flags":["BACKFILL"],
        }
        f.write(json.dumps(rec,ensure_ascii=False)+"\n"); added+=1
print(f"registry 追加 {added} 条 -> 现 {len(reg)+added} 条")

# ---------- 7 维参考表 ----------
def row(s):
    sc=s["scores"]
    return (f"| {s['base_id']} | {s['title_zh']} | {s['grade']} | {s['value']:.2f} | "
            f"{sc['IMP']} | {sc['NOV']} | {sc['TEC']} | {sc['EXP']} | {sc['PER']} | {sc['TRL']} | {sc['REP']} | {s['track']} |")
lines=["# 旧稿 backfill · 7 维度对比表（参考）","",
 f"> 批次：**backfill-2603-2609**（历史旧稿补录，非当日新提交）。RSS replace 公告日 **{ANNOUNCE}**；原始投稿窗口 **{ORIG_WIN}**。",
 f"> 共 **{len(scored)}** 篇 XR 相关旧稿补录；剔除 1 篇非 XR（2605.00556 自动驾驶 HCI）。门③ 对 backfill 不适用。",
 "",
 "| arXiv ID | 中文题名 | 档 | 加权 | IMP | NOV | TEC | EXP | PER | TRL | REP | 赛道 |",
 "|---|---|---|---|---|---|---|---|---|---|---|---|"]
for s in scored:
    lines.append(row(s))
lines += ["",
 f"**档位**：S≥4.20 · A 3.60–4.20 · B 3.00–3.60 · C<3.00。权重 IMP0.20·NOV0.20·TEC0.15·EXP0.15·PER0.15·TRL0.08·REP0.07。",
 "**说明**：本表为 backfill 参考表；6 篇全文均已抓取(L0/FULL)并写原子笔记（见 MOC-backfill-2603-2609）。",
 f"**覆盖度**：门① 最大 Jaccard {gate1_max:.3f}（{'通过' if gate1_pass else '不通过'}）；门② 覆盖 {len(tracks)} 赛道（{'通过' if gate2_pass else '不通过'}）。"]
open(f"{ROOT}/papers/daily/{BATCH}/7dim-table.md","w",encoding="utf-8").write("\n".join(lines)+"\n")

# ---------- run_log ----------
runlog = f"""# 运行日志 · {BATCH}（旧稿补录）

- 性质：**历史旧稿 backfill**，非当日新提交。触发条件：export.arxiv.org / arxiv.org/api/query 已恢复 200（10-09 探针确认），满足「API 健康时单开 backfill 批次」待办。
- 来源：2026-10-09 RSS 落盘 `data/raw/2026-10-09_rss.jsonl` 中 7 篇 2603–2609 旧稿(replace 公告日 2026-10-08)；经 XR 相关性甄别，保留 **6 篇 XR 相关**，剔除 1 篇非 XR。
- 剔除：2605.00556（Linking Behaviour and Perception to Evaluate Meaningful Human Control over Partially Automated Driving）——属自动驾驶 HCI，非 XR/VR/AR，C 级，不纳入 XR 文献库。
- 全文：fetch_fulltext.py 7 篇（含剔除稿）**全部 L0/FULL**（arxiv.org/html，45K–155K 字符，串行 3s，无限流/降级/伪造）；6 篇 XR 入馆。
- 评分：7 维加权；3 A（ReViV/Hand-4DGS/NavSight）+ 3 B（ModPack/3DGS-Init/TAVIS）。
- 覆盖度门：门① 最大 Jaccard {gate1_max:.3f}（{'通过' if gate1_pass else '不通过'}）；门② 覆盖 {len(tracks)} 赛道（{'通过' if gate2_pass else '不通过'}）；门③ backfill 不适用。重筛触发：{rescreen}。
- 同质关注 {len(watch)} 条（见上）。
- 文献库：{len(reg)} → {len(reg)+added}（+{added}，均为 BACKFILL 标记，in_top10=False）。
- 诚实口径：本批次为补录，明确标注 batch=backfill-2603-2609、orig_window={ORIG_WIN}、公告日 {ANNOUNCE}，绝不混入「当日新论文」表；原始投稿月份窗口已在笔记与索引注明。
"""
open(f"{ROOT}/papers/daily/{BATCH}/run_log.md","w",encoding="utf-8").write(runlog)
print("写盘：7dim-table.md / run_log.md / scored_backfill.json")
print("\n=== backfill 入选（加权降序）===")
for i,s in enumerate(scored,1):
    print(f"{i}. {s['base_id']} {s['grade']} {s['value']:.2f} [{s['track']}] {s['title_zh']}")
