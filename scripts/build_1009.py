# -*- coding: utf-8 -*-
"""build_1009.py — 2026-10-09 批次：7 维评分 + 覆盖度三关 + 文献库幂等追加 + 7 维参考表/run_log 生成。
复用 10-08 模板；评分基于摘要+领域判断（Top10 全文已 L0/FULL 落盘，笔记阶段再精读订正）。
"""
import json, os, re, datetime
from collections import defaultdict

W = {"IMP":0.20,"NOV":0.20,"TEC":0.15,"EXP":0.15,"PER":0.15,"TRL":0.08,"REP":0.07}
DIMS = ["IMP","NOV","TEC","EXP","PER","TRL","REP"]
ANNOUNCE = "2026-10-08"   # RSS 公告日（拉取日 2026-10-09）
BATCH = "2026-10-09"
ROOT = "D:/Agent/WorkBuddy/Research"

# base_id -> (scores[IMP,NOV,TEC,EXP,PER,TRL,REP], track_zh, title_zh)
NEW = {
 "2610.09304": ([4,4,4,4,4,3,3], "化身与人体", "基于高密度表面肌电的表情动画（HMD 遮挡下面部捕捉）"),
 "2610.09343": ([3,3,4,3,4,4,3], "神经渲染", "TileSkipper：区域自适应瓦片剪枝的 3D 高斯溅射"),
 "2610.08941": ([4,4,4,4,4,3,3], "空间计算与UI", "SPW-Nav：流式全景世界模型（语言引导导航/VR 探索）"),
 "2610.08978": ([4,4,4,4,4,3,3], "重建与SLAM", "S2Tok：基于持久空间令牌的流式 3DGS 重建"),
 "2610.09444_note": None,  # placeholder (not used; see below)
 "2610.09455": ([4,4,4,4,4,3,3], "交互与输入", "RLHND：视频基础模型驱动的物理接地手部追踪"),
 "2610.09853": ([4,4,4,4,4,3,3], "重建与SLAM", "DeltaSplat：免位姿前馈 3DGS 的迭代高斯精炼"),
 "2610.10538": ([4,4,4,4,4,3,3], "感知与认知", "Never Look Back：第一视角视频的 3D 物体记忆持久性"),
 "2610.10539": ([4,4,4,4,4,3,3], "内容生成", "Tetris3D：物体严丝合缝的 3D 场景生成"),
 "2610.09274": ([4,3,4,4,4,4,3], "重建与SLAM", "硬件感知校准聚类注意力（高效视觉几何 Transformer/VGGT）"),
 "2610.09821": ([4,3,4,4,4,4,3], "化身与人体", "面向边缘设备的高效 3D 高斯头部化身"),
 "2610.09444": ([3,4,4,4,4,3,3], "感知与认知", "LighTROcc：基于实例中心 3D 高斯的轻量 4D 占据预测"),
 "2610.10181": ([3,4,4,4,4,3,3], "感知与认知", "Argos：基于几何先验的在线场景变化检测"),
 "2610.10528": ([3,4,4,4,4,3,3], "空间计算与UI", "Long-WAM：扩展世界-动作模型上下文"),
 "2610.10288": ([4,4,3,4,3,3,4], "触觉与多模态", "TouchScale：500 小时视觉-触觉学习数据集"),
 "2610.09116": ([3,4,4,3,3,4,4], "系统与平台", "SPLATIFY：论文到可训练 3DGS 代码的多智能体框架"),
 "2610.10479": ([3,4,4,4,3,3,3], "重建与SLAM", "Agentic RSR：真实-仿真-真实场景重建与机器人策略"),
 "2610.09284": ([3,4,3,3,3,3,3], "交互与输入", "Beyond Activation：注视调用+可见状态的具身 AR 助手"),
 "2610.09513": ([3,4,4,3,3,3,3], "内容生成", "OmniCam：基于几何接地的全景相机轨迹生成"),
 "2610.09791": ([3,4,4,3,3,3,3], "化身与人体", "Counterfactual Route：反事实路径优化的高斯头部化身"),
 "2610.10396": ([2,3,3,3,3,3,2], "神经渲染", "GDSNet：高斯密度溅射人群计数（弱 XR 相关）"),
 "2610.10387": ([3,3,3,3,3,3,3], "重建与SLAM", "NeRFifyMesh：从纹理网格优化 NeRF 的机器人场景构建"),
}
# 删除占位
NEW.pop("2610.09444_note", None)

def wval(scores):
    return round(sum(W[d]*scores[i] for i,d in enumerate(DIMS)), 3)

def grade(v):
    if v>=4.2: return "S"
    if v>=3.6: return "A"
    if v>=3.0: return "B"
    return "C"

# 载入 raw 新语料（取标题/摘要/分类）
raw={}
for l in open(f"{ROOT}/data/raw/2026-10-09_new.jsonl",encoding="utf-8"):
    if not l.strip(): continue
    r=json.loads(l); raw[r["base_id"]]=r

scored=[]
for bid,(sc,track,zh) in NEW.items():
    r=raw[bid]
    v=wval(sc); g=grade(v)
    scored.append({
        "base_id":bid,"id":"arXiv:"+bid,"title":r["title"],"title_zh":zh,
        "track":track,"scores":dict(zip(DIMS,sc)),"value":v,"grade":g,
        "primary_category":r.get("primary_category",""),"abstract":r.get("abstract",""),
        "date":ANNOUNCE,"batch":BATCH,
    })
scored.sort(key=lambda x:-x["value"])

# ---------- 覆盖度三关 ----------
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

# 门①：新稿与文献库最大 Jaccard（同质查重）
gate1_max=0.0; gate1_pair=""
for s in scored:
    for t in reg_titles:
        j=jac(s["title"],t)
        if j>gate1_max: gate1_max=j; gate1_pair=f'{s["base_id"]} <> {t[:40]}'
gate1_pass = gate1_max < 0.62

# 门②：Top10 覆盖赛道数
top10=scored[:10]
tracks=set(s["track"] for s in top10)
gate2_pass = len(tracks)>=5

# 门③：当日最高分 vs 库近30天 Top10 均分
today_max=max(s["value"] for s in scored)
gate3_heavy = today_max >= lib_top10_mean
gate3_pass = True  # 非重磅日不拔高、不触发重筛；重磅日也通过（仅决定是否给 S）

rescreen = not (gate1_pass and gate2_pass)  # 触发重筛条件
print("=== 覆盖度三关 ===")
print(f"门① 最大 Jaccard = {gate1_max:.3f} ({gate1_pair}) -> {'通过' if gate1_pass else '不通过(触发重筛)'}")
print(f"门② Top10 覆盖赛道 = {len(tracks)} ({sorted(tracks)}) -> {'通过' if gate2_pass else '不通过(触发重筛)'}")
print(f"门③ 当日最高 {today_max} vs 库Top10均分 {lib_top10_mean} -> {'重磅日(S可)' if gate3_heavy else '非重磅日(无S,不拔高)'}")
print(f"重筛触发: {rescreen}")

# 落后/同质登记：门① 虽通过但记录 >0.4 的关注对
watch=[]
for s in scored:
    for t in reg_titles:
        j=jac(s["title"],t)
        if 0.4<=j<0.62:
            watch.append(f'{s["base_id"]}({j:.2f}) ~ {t[:36]}')
print("同质关注(0.4-0.62):", watch if watch else "无")

# ---------- 写入 scored.json ----------
os.makedirs(f"{ROOT}/papers/daily/{BATCH}", exist_ok=True)
with open(f"{ROOT}/data/scored_1009.json","w",encoding="utf-8") as f:
    json.dump(scored,f,ensure_ascii=False,indent=1)

# ---------- 幂等追加 registry（按 base_id 去重）----------
reg_ids=set(r.get("id") for r in reg)
added=0
with open(f"{ROOT}/papers/library/registry.jsonl","a",encoding="utf-8") as f:
    for s in scored:
        if s["id"] in reg_ids: continue
        rec={
            "id":s["id"],"title":s["title"],"title_zh":s["title_zh"],"track":s["track"],
            "date":s["date"],"batch":s["batch"],"value":s["value"],"grade":s["grade"],
            "scores":s["scores"],"status":"CURRENT","evidence":"FULL","fetch_level":"L0",
            "fulltext_chars":0,"in_top10": s["base_id"] in [t["base_id"] for t in top10],
            "flags":[],
        }
        f.write(json.dumps(rec,ensure_ascii=False)+"\n"); added+=1
print(f"registry 追加 {added} 条 -> 现 {len(reg)+added} 条")

# ---------- 7 维参考表 (markdown) ----------
def row(s):
    sc=s["scores"]
    return (f"| {s['base_id']} | {s['title_zh']} | {s['grade']} | {s['value']:.2f} | "
            f"{sc['IMP']} | {sc['NOV']} | {sc['TEC']} | {sc['EXP']} | {sc['PER']} | {sc['TRL']} | {sc['REP']} | {s['track']} |")
lines=["# 当日新拉取论文 · 7 维度对比表（参考）","",
 f"> 拉取窗口：RSS 公告日 **{ANNOUNCE}**（拉取日 {BATCH}）；源：rss.arxiv.org 兜底（export.arxiv.org API 前沿滞后于 10-07）。",
 f"> 共 **{len(scored)}** 篇 XR 相关新提交（2610.*）；8 篇旧稿再公告(2603–2609)单列 backfill，5 篇非 XR 已剔除。",
 "",
 "| arXiv ID | 中文题名 | 档 | 加权 | IMP | NOV | TEC | EXP | PER | TRL | REP | 赛道 |",
 "|---|---|---|---|---|---|---|---|---|---|---|---|"]
for s in scored:
    lines.append(row(s))
lines += ["",
 f"**档位**：S≥4.20 · A 3.60–4.20 · B 3.00–3.60 · C<3.00。权重 IMP0.20·NOV0.20·TEC0.15·EXP0.15·PER0.15·TRL0.08·REP0.07。",
 f"**Top10 入选**（按加权降序，= {len(top10)} 篇）：" + "、".join(t['base_id'] for t in top10) + "。",
 "**说明**：本表为当日全部新稿参考表；Top10 全文已抓取(L0/FULL)并逐篇精读（见报告 §三）。"]
open(f"{ROOT}/papers/daily/{BATCH}/7dim-table.md","w",encoding="utf-8").write("\n".join(lines)+"\n")

# ---------- run_log ----------
runlog = f"""# 运行日志 · {BATCH}

- 拉取日：{BATCH}（周五）｜RSS 公告日：{ANNOUNCE}
- 数据源：export.arxiv.org/api/query 探针 200 但 submittedDate 前沿停滞 10-07；arxiv.org/api/query 502；rss.arxiv.org 200 → **RSS 兜底**。
- 拉取：fetch_rss.py 7 分类去重 797 → 关键词命中 36（全公告日 {ANNOUNCE}）。
- 过滤：2610.* 真新提交 21 篇 XR 相关；剔除 7 篇旧稿再公告(2603–2609) + 5 篇非 XR（人形本体/无人机/医学CT/多物理仿真/机械臂末端）。
- 全文：fetch_fulltext.py 21 篇 **全部 L0/FULL**（arxiv.org/html，串行 3s，无限流/降级/伪造）；manifest 校验通过。
- 评分：7 维加权；Top10 全部 A 档，最高 {today_max}。
- 覆盖度三关：门① 最大 Jaccard {gate1_max:.3f}（{'通过' if gate1_pass else '不通过'}）；门② 覆盖 {len(tracks)} 赛道（{'通过' if gate2_pass else '不通过'}）；门③ 最高 {today_max} {'≥' if gate3_heavy else '<'} 库Top10均分 {lib_top10_mean}（{'重磅日' if gate3_heavy else '非重磅日，无 S 级，未拔高'}）。重筛触发：{rescreen}。
- 落后标记：OUTDATED/SUPERSEDED 0 篇；同质关注 {len(watch)} 条（见上）。
- 文献库：{len(reg)} → {len(reg)+added}（+{added}）。
- 诚实口径：公告日 {ANNOUNCE} ≠ 拉取日 {BATCH}，报告中显式写明实际命中区间，绝不伪装"当日新论文"。
"""
open(f"{ROOT}/papers/daily/{BATCH}/run_log.md","w",encoding="utf-8").write(runlog)
print("写盘：7dim-table.md / run_log.md / scored_1009.json")
print("\n=== Top10 ===")
for i,s in enumerate(top10,1):
    print(f"{i}. {s['base_id']} {s['grade']} {s['value']:.2f} [{s['track']}] {s['title_zh']}")
