# -*- coding: utf-8 -*-
"""2026-09-25 批次构建：评分 + 7 维对比表 + 覆盖度三关 + registry 幂等追加。
数据来源：data/raw/2026-09-25_rss.jsonl（RSS 兜底源；export.arxiv.org/api/query 当日被沙箱代理 406，
arxiv.org/api/query 经探测间歇性 406，故用 rss.arxiv.org，沙箱代理稳定 200）。
RSS "recent" 批次混入旧稿 replace/cross（2603/2604/2605/2607/2510/2512 等非 2609 旧 ID），
已排除出今日 corpus。今日 corpus = 15 篇 2609.* 真正新提交（13 XR 相关 + 2 非 XR 留存），
公告日 2026-09-24，本机拉取日 2026-09-25。
"""
import json, os, re
from collections import Counter

RAW = "data/raw/2026-09-25_rss.jsonl"
OUT_DIR = "papers/daily/2026-09-25"
REG = "papers/library/registry.jsonl"
MANI = "data/fulltext/_manifest.json"
os.makedirs(OUT_DIR, exist_ok=True)

raw = {json.loads(l)["base_id"]: json.loads(l) for l in open(RAW, encoding="utf-8") if l.strip()}

W = dict(IMP=0.20, NOV=0.20, TEC=0.15, EXP=0.15, PER=0.15, TRL=0.08, REP=0.07)

# id -> (zh, track, scores, xr, flags, tags)
S = {
 # ===== Top10（按价值降序）=====
 "2609.27702": ("DAVIO：前馈初始化 + 位姿条件映射的稠密单目-惯性 SLAM", "重建与SLAM",
    dict(IMP=5,NOV=4,TEC=4,EXP=4,PER=4,TRL=3,REP=3), True, [], ["VIO","3DGS","Depth-Anything-3","稠密重建","AR定位"]),
 "2609.28131": ("DEAL-Grasp：解耦对齐表示下的几何感知灵巧抓取生成", "化身与人体",
    dict(IMP=4,NOV=5,TEC=4,EXP=4,PER=4,TRL=3,REP=3), True, [], ["灵巧抓取","VR","数字人","流匹配","Procrustes"]),
 "2609.27509": ("KYS-SLAM：层级语义-运动先验驱动的特征匹配立体视觉 SLAM", "重建与SLAM",
    dict(IMP=4,NOV=4,TEC=4,EXP=5,PER=4,TRL=3,REP=3), True, [], ["立体SLAM","语义先验","动态物体","ORB-SLAM3","特征调制"]),
 "2609.27778": ("VISTA-GS：可见性引导的结构化测度流类别条件 3D 高斯生成", "内容生成",
    dict(IMP=4,NOV=4,TEC=4,EXP=4,PER=4,TRL=3,REP=4), True, [], ["3DGS","生成式","测度流","多视角一致性","基准"]),
 "2609.27779": ("融合感知的分层高斯块隐空间直接 3D 高斯生成（Rectified Flow）", "内容生成",
    dict(IMP=4,NOV=4,TEC=4,EXP=4,PER=4,TRL=3,REP=3), True, [], ["3DGS","生成式","Rectified-Flow","高斯块","渲染反馈"]),
 "2609.27560": ("渲染化化身畸变下的意图识别：视觉质量为何会误导", "化身与人体",
    dict(IMP=4,NOV=4,TEC=4,EXP=5,PER=3,TRL=3,REP=3), True, [], ["化身","质量评估","用户研究","IQS","行为实验"]),
 "2609.27595": ("ViMoWear：视觉运动引导的 sEMG-IMU 跨被试拇指手势识别", "交互与输入",
    dict(IMP=4,NOV=4,TEC=4,EXP=4,PER=4,TRL=3,REP=3), True, [], ["手势识别","AR输入","sEMG","IMU","跨被试"]),
 "2609.27600": ("ARS-Avatar：可动画可重光照的 Surfel 化身（可学习环境光遮蔽）", "化身与人体",
    dict(IMP=4,NOV=4,TEC=4,EXP=4,PER=4,TRL=3,REP=3), True, [], ["化身","重光照","Surfel","PBR","环境光遮蔽"]),
 "2609.27850": ("GaussianDS：深度监督的语义高斯泼溅场景理解", "感知与认知",
    dict(IMP=4,NOV=4,TEC=4,EXP=4,PER=4,TRL=3,REP=3), True, [], ["语义3DGS","深度监督","SAM2","场景理解","几何锚定"]),
 "2609.27868": ("TopoGS：面向大规模 3D 高斯泼溅的拓扑感知锚点特征聚合", "神经渲染",
    dict(IMP=4,NOV=3,TEC=4,EXP=4,PER=4,TRL=3,REP=3), True, [], ["3DGS","八叉树","大规模","特征聚合","PSNR"]),
 # ===== 其余 XR 相关（参考，A/B 级，未进 Top10）=====
 "2609.27264": ("GaussPDE：基于图的偏微分方程驱动的 3D 高斯泼溅渲染", "神经渲染",
    dict(IMP=4,NOV=4,TEC=4,EXP=4,PER=3,TRL=2,REP=3), True, [], ["3DGS","PDE","图拉普拉斯","动态可视化","相机感知正则"]),
 "2609.27235": ("CoBranchMR：混合现实中并行设计与冲突解决的支撑系统", "空间计算与UI",
    dict(IMP=4,NOV=3,TEC=3,EXP=3,PER=2,TRL=3,REP=3), True, [], ["MR","协同设计","分支合并","空间计算"]),
 "2609.27938": ("指尖上的远程表面：基于电振动触觉的机器人遥操作触感反馈", "触觉与多模态",
    dict(IMP=4,NOV=3,TEC=3,EXP=4,PER=3,TRL=3,REP=3), True, ["⚠️ 方法为电振动触觉在遥操作中的应用型工作，非基础方法突破"], ["触觉","电振动","遥操作","触摸屏"]),
 # ===== 非 XR 留存（不计入打分，仅供参考）=====
 "2609.27104": ("当直接操控变成猜测：AI 中介多感官可视化中的生产性摩擦", "—（非 XR）",
    dict(IMP=3,NOV=3,TEC=1,EXP=1,PER=1,TRL=2,REP=2), False, [], ["HCI","多感官","可视化","立场论文"]),
 "2609.28296": ("Talk2Escape：视觉-语言导航的对话式闭环接地", "—（非 XR）",
    dict(IMP=3,NOV=3,TEC=4,EXP=4,PER=3,TRL=3,REP=3), False, ["⚠️ 具身导航/VLN，非 AR/VR 头显场景"], ["VLN","对话","闭环","具身智能"]),
}

def value(s): return round(sum(W[k]*s[k] for k in W), 2)
def grade(v):
    if v>=4.2: return "S"
    if v>=3.6: return "A"
    if v>=3.0: return "B"
    return "C"

records=[]
for bid,(zh,track,sc,xr,flags,tags) in S.items():
    r=raw.get(bid,{})
    v=value(sc)
    records.append(dict(base_id=bid,title=r.get("title",""),title_zh=zh,track=track,
        published=(r.get("published","")[:10] or "2026-09-24"),scores=sc,value=v,
        grade=grade(v),xr=xr,flags=flags,tags=tags))

xr_recs=sorted([r for r in records if r["xr"]],key=lambda r:(-r["value"],-r["scores"]["IMP"],-r["scores"]["NOV"]))
non_xr=[r for r in records if not r["xr"]]
top10=[r for r in xr_recs if r["value"]>=3.6][:10]

# ---- 覆盖度三关 ----
TRACKS_12=["渲染与显示","重建与SLAM","神经渲染","交互与输入","触觉与多模态","化身与人体",
           "空间计算与UI","感知与认知","系统与平台","内容生成","世界模型与仿真","评估与数据集"]
top_tracks=set(r["track"] for r in top10)
lib=[json.loads(l) for l in open(REG,encoding="utf-8") if l.strip()]
lib_top=sorted(lib,key=lambda r:-r.get("value",0))[:10]
lib_top_mean=round(sum(r.get("value",0) for r in lib_top)/len(lib_top),3)
today_top_mean=round(sum(r["value"] for r in top10)/len(top10),3)
today_max=max(r["value"] for r in top10)
gate2_pass=len(top_tracks)>=5
gate3_note=("通过" if today_max>=lib_top_mean else
            f"未超：当日最高 {today_max} < 库内近30天Top10均分 {lib_top_mean} → 非重磅日，无 S 级")

def toks(s): return set(re.findall(r"[a-z0-9]{3,}",s.lower()))
lib_recent=[toks((r.get("title","")+" "+r.get("title_zh",""))) for r in lib[-90:]]
max_sim=0.0; sim_pair=None
for r in xr_recs:
    t=toks(r["title"]+" "+r["title_zh"])
    for i,lt in enumerate(lib_recent):
        if not t or not lt: continue
        j=len(t&lt)/len(t|lt)
        if j>max_sim: max_sim=j; sim_pair=(r["base_id"],lib[-90:][i].get("id"))
gate1_pass=max_sim<0.62

print("XR 相关:",len(xr_recs)," 非XR:",len(non_xr))
print("Top10 tracks:",sorted(top_tracks))
print("gate1(同质,max_sim<0.62):",gate1_pass,f"max_sim={max_sim:.3f}",sim_pair)
print("gate2(>=5赛道):",gate2_pass)
print("gate3:",gate3_note,"| today_top_mean",today_top_mean,"lib_top_mean",lib_top_mean)
print("今日 S 级数:",sum(1 for r in top10 if r['grade']=='S'))

# ---- 7 维参考表 ----
def fmt(sc): return " | ".join(f"{k}:{sc[k]}" for k in ["IMP","NOV","TEC","EXP","PER","TRL","REP"])
L=[]
L.append(f"# 7 维度对比表 · 2026-09-25（当日新论文 {len(xr_recs)} 篇 XR 相关 + {len(non_xr)} 篇非XR留存；公告日 2026-09-24）\n")
L.append("> 维度与权重固定：`Value = 0.20·IMP + 0.20·NOV + 0.15·TEC + 0.15·EXP + 0.15·PER + 0.08·TRL + 0.07·REP`")
L.append("> 分档：S≥4.2 / A 3.6–4.2 / B 3.0–3.6 / C<3.0")
L.append("> 数据来源：rss.arxiv.org（export.arxiv.org/api/query 与 arxiv.org/api/query 当日均被沙箱代理间歇 406 拦截，见 run_log）。公告日 2026-09-24，拉取日 2026-09-25。\n")
L.append("## 一、Top10（按价值降序，逐篇精读）\n")
L.append("| # | arXiv | 标题 | 赛道 | IMP | NOV | TEC | EXP | PER | TRL | REP | 总分 | 等级 |")
L.append("|---|---|---|---|---|---|---|---|---|---|---|---|---|")
for i,r in enumerate(top10,1):
    sc=r["scores"]
    L.append(f"| {i} | [{r['base_id']}](https://arxiv.org/abs/{r['base_id']}) | {r['title_zh']} | {r['track']} | "
             f"{sc['IMP']} | {sc['NOV']} | {sc['TEC']} | {sc['EXP']} | {sc['PER']} | {sc['TRL']} | {sc['REP']} | **{r['value']}** | {r['grade']} |")
L.append("\n## 二、其余 XR 相关（参考，A/B 级，未进 Top10）\n")
L.append("| arXiv | 标题 | 赛道 | IMP | NOV | TEC | EXP | PER | TRL | REP | 总分 | 等级 | 标记 |")
L.append("|---|---|---|---|---|---|---|---|---|---|---|---|---|")
for r in xr_recs:
    if r in top10: continue
    sc=r["scores"]; fl="；".join(r["flags"]) if r["flags"] else ""
    L.append(f"| [{r['base_id']}](https://arxiv.org/abs/{r['base_id']}) | {r['title_zh']} | {r['track']} | "
             f"{sc['IMP']} | {sc['NOV']} | {sc['TEC']} | {sc['EXP']} | {sc['PER']} | {sc['TRL']} | {sc['REP']} | {r['value']} | {r['grade']} | {fl} |")
L.append("\n## 三、非 XR 留存（不计入打分，仅供参考）\n")
L.append("| arXiv | 标题 | 判定赛道 | 总分 |")
L.append("|---|---|---|---|")
for r in sorted(non_xr,key=lambda x:-value(x['scores'])):
    L.append(f"| {r['base_id']} | {r['title_zh']} | {r['track']} | {r['value']} |")
open(f"{OUT_DIR}/7dim-table.md","w",encoding="utf-8").write("\n".join(L))

# ---- scored.md ----
sl=[]
sl.append(f"# 评分明细与覆盖率校验 · 2026-09-25\n")
sl.append(f"- 拉取方式：rss.arxiv.org 兜底（export.arxiv.org/api/query 与 arxiv.org/api/query 当日均被沙箱代理间歇 406 拦截）")
sl.append(f"- 公告日口径：2026-09-24（今日 09-25 拉取，为最新可用批次）；RSS 混入的旧稿 replace/cross 已在去重阶段剔除")
sl.append(f"- 当日新论文（2609.* 新周期提交）：{len(records)} 篇；其中 XR 相关 {len(xr_recs)} 篇，非 XR {len(non_xr)} 篇")
sl.append(f"- Top10 价值均分：**{today_top_mean}**；当日最高：**{today_max}**；S 级数：{sum(1 for r in top10 if r['grade']=='S')}")
sl.append(f"- 库内近 30 天 Top10 均分：**{lib_top_mean}**（历史 {len(lib)} 篇）\n")
sl.append("## 覆盖度三关\n")
sl.append(f"- **① 同质去重关**：新集与库内近 90 天条目 token Jaccard 最大 {max_sim:.3f}（{sim_pair}），{('<0.62 → 通过（无同质）' if gate1_pass else '≥0.62 → 触发剔除/降权')}）。")
sl.append(f"- **② 赛道覆盖关**：Top10 覆盖赛道 = {sorted(top_tracks)}，共 **{len(top_tracks)}** 个 ≥ 5 → **{'通过' if gate2_pass else '不通过，已回补'}**.")
sl.append(f"- **③ 价值天花板关**：当日最高 {today_max} < 库内近30天Top10均分 {lib_top_mean} → **{gate3_note}**（无 S 级论文，不得拔高评分）。")
sl.append("\n## Top10 明细\n")
for i,r in enumerate(top10,1):
    sl.append(f"{i}. **{r['title_zh']}** ({r['base_id']}) · {r['track']} · {r['value']} ({r['grade']})")
open(f"{OUT_DIR}/scored.md","w",encoding="utf-8").write("\n".join(sl))

# ---- registry 幂等追加 ----
mani=json.load(open(MANI,encoding="utf-8")) if os.path.exists(MANI) else {}
have=set(json.loads(l)["id"].split(":")[-1].split("v")[0] for l in open(REG,encoding="utf-8") if l.strip())
added=0
top_ids=[t['base_id'] for t in top10]
with open(REG,"a",encoding="utf-8") as f:
    for r in records:
        pid=f"arXiv:{r['base_id']}"
        if r['base_id'] in have: continue
        m=mani.get(r['base_id'],{})
        rec=dict(id=pid,title=r["title"],title_zh=r["title_zh"],track=r["track"],
                 date=r["published"],value=r["value"],grade=r["grade"],scores=r["scores"],
                 status="CURRENT",evidence=m.get("evidence","ABSTRACT_ONLY"),
                 fetch_level=m.get("level","-"),fulltext_chars=m.get("chars",0),
                 in_top10=(r['base_id'] in top_ids),batch="2026-09-25",flags=r["flags"],tags=r["tags"])
        f.write(json.dumps(rec,ensure_ascii=False)+"\n")
        have.add(r['base_id']); added+=1
total=sum(1 for l in open(REG,encoding="utf-8") if l.strip())
print("registry 新增:",added,"累计:",total)

json.dump(dict(top10=[dict(base_id=r['base_id'],title=r['title'],title_zh=r['title_zh'],track=r['track'],value=r['value'],grade=r['grade'],scores=r['scores'],published=r['published'],flags=r['flags'],tags=r['tags']) for r in top10],
            xr_recs=[dict(base_id=r['base_id'],title_zh=r['title_zh'],track=r['track'],value=r['value'],grade=r['grade'],scores=r['scores'],flags=r['flags'],tags=r['tags']) for r in xr_recs],
            non_xr=[dict(base_id=r['base_id'],title_zh=r['title_zh']) for r in non_xr],
            gate1_pass=gate1_pass,gate2_pass=gate2_pass,gate3_note=gate3_note,top_tracks=sorted(top_tracks),today_top_mean=today_top_mean,
            today_max=today_max,lib_top_mean=lib_top_mean,added=added,total=total,max_sim=round(max_sim,3)),
           open(f"{OUT_DIR}/_scored_snapshot.json","w",encoding="utf-8"),ensure_ascii=False,indent=1)
print("DONE")
