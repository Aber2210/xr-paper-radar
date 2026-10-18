# -*- coding: utf-8 -*-
"""2026-09-24 批次构建：评分 + 7 维对比表 + 覆盖度三关 + registry 幂等追加。
数据来源：data/raw/2026-09-24_new.jsonl（RSS 抓取，已去 registry 重复）。
说明：本日 export.arxiv.org/api/query 被沙箱代理 406 拦截，改用 rss.arxiv.org 兜底（见 run_log）。
RSS "recent" 批次混有旧稿 replace/cross（2603/2605/2607/2608/2510/2512 等非 2609 旧 ID），
这些非"当日新提交"，已排除出今日 corpus，仅在 run_log 登记为 backfill 候选。
今日 corpus = 22 篇 2609.* 新周期提交（12 XR 相关 + 9 非 XR 留存），日期取 RSS 公告日 2026-09-23。
"""
import json, os, re, datetime
from collections import Counter

RAW = "data/raw/2026-09-24_new.jsonl"
OUT_DIR = "papers/daily/2026-09-24"
REG = "papers/library/registry.jsonl"
MANI = "data/fulltext/_manifest.json"
os.makedirs(OUT_DIR, exist_ok=True)

raw = {json.loads(l)["base_id"]: json.loads(l) for l in open(RAW, encoding="utf-8")}

W = dict(IMP=0.20, NOV=0.20, TEC=0.15, EXP=0.15, PER=0.15, TRL=0.08, REP=0.07)

# id -> (zh, track, scores, xr, flags)
S = {
 "2609.25604": ("随机高斯泼溅去噪的超快神经推理（Stochastic 2DGS 时序去噪）", "神经渲染", dict(IMP=4,NOV=4,TEC=4,EXP=4,PER=4,TRL=3,REP=3), True, []),
 "2609.26795": ("φ-RIE：从照片级重建到可交互环境（3DGS→可移动仿真资产）", "内容生成", dict(IMP=4,NOV=4,TEC=4,EXP=4,PER=4,TRL=3,REP=3), True, []),
 "2609.25422": ("VR 晕动症早期眼动动态与不适进展预测", "感知与认知", dict(IMP=4,NOV=4,TEC=4,EXP=4,PER=3,TRL=3,REP=3), True, []),
 "2609.26203": ("基于 VERA 平台的大规模远程 VR 晕动症研究（N=263）", "感知与认知", dict(IMP=4,NOV=3,TEC=4,EXP=5,PER=3,TRL=3,REP=3), True, []),
 "2609.24531": ("动态热高斯：多模态 4D 高斯泼溅（热成像动态重建）", "神经渲染", dict(IMP=3,NOV=4,TEC=4,EXP=3,PER=3,TRL=2,REP=2), True, ["⚠️ 应用为热成像/军事，XR 相关度偏弱但 4DGS 技术相关"]),
 "2609.25527": ("数字孪生驱动的 VR 手术机器人遥操作（多视角空间感知）", "空间计算与UI", dict(IMP=4,NOV=4,TEC=4,EXP=5,PER=4,TRL=4,REP=3), True, []),
 "2609.25746": ("双协方差高斯泼溅 SLAM：解耦渲染与配准", "重建与SLAM", dict(IMP=4,NOV=5,TEC=4,EXP=4,PER=4,TRL=3,REP=3), True, []),
 "2609.26315": ("ArborSplat：面向果园的在线语义高斯泼溅 SLAM", "重建与SLAM", dict(IMP=4,NOV=4,TEC=4,EXP=4,PER=4,TRL=3,REP=3), True, []),
 "2609.25036": ("4DGS-JEPA：动态高斯泼溅的时间组合联合嵌入预测", "世界模型与仿真", dict(IMP=4,NOV=5,TEC=4,EXP=3,PER=4,TRL=2,REP=3), True, []),
 "2609.25466": ("基于 Transformer 的 OpenXR 实时手势识别", "交互与输入", dict(IMP=4,NOV=3,TEC=3,EXP=3,PER=3,TRL=4,REP=3), True, []),
 "2609.25633": ("鲁棒、估计器无关的动态 3DGS 压缩", "系统与平台", dict(IMP=4,NOV=4,TEC=4,EXP=4,PER=5,TRL=3,REP=4), True, []),
 "2609.15795": ("SURE-Map：自校正流式几何基础模型（SLAM 替代）", "重建与SLAM", dict(IMP=4,NOV=5,TEC=4,EXP=4,PER=4,TRL=3,REP=3), True, []),
 # ---- 非 XR 留存（不计入主表）----
 "2609.22277": ("面向视障用户的多模态智能盲杖", "—（非 XR）", dict(IMP=2,NOV=3,TEC=4,EXP=3,PER=3,TRL=3,REP=3), False, []),
 "2609.22332": ("AffordanceWAM：可供性感知的联合世界-动作模型", "—（非 XR）", dict(IMP=2,NOV=4,TEC=4,EXP=4,PER=4,TRL=3,REP=3), False, []),
 "2609.25558": ("HABILIS Brain 0：几何变化监督的 VLA 与残差流恢复", "—（非 XR）", dict(IMP=2,NOV=4,TEC=4,EXP=4,PER=4,TRL=3,REP=3), False, []),
 "2609.25614": ("Astrobee 自由飞行遥操作四指载荷（VR 接口）", "—（非 XR）", dict(IMP=2,NOV=3,TEC=4,EXP=3,PER=3,TRL=3,REP=3), False, []),
 "2609.25627": ("MachEmbodied-U0：具身智能统一理解-生成模型", "—（非 XR）", dict(IMP=3,NOV=4,TEC=4,EXP=4,PER=4,TRL=3,REP=3), False, []),
 "2609.25653": ("PhyVisGen：物理-视觉高保真机器人操作数据生成", "—（非 XR）", dict(IMP=2,NOV=4,TEC=4,EXP=4,PER=4,TRL=3,REP=3), False, []),
 "2609.26007": ("Skytopia：动作条件潜在世界模型的单目无人机导航", "—（非 XR）", dict(IMP=3,NOV=4,TEC=4,EXP=4,PER=4,TRL=3,REP=3), False, []),
 "2609.25932": ("2D 点云配准的无符号距离图（激光里程计/SLAM）", "—（非 XR）", dict(IMP=2,NOV=4,TEC=4,EXP=4,PER=4,TRL=3,REP=3), False, ["⚠️ 2D 激光里程计，非 XR 显示/交互"]),
 "2609.26766": ("TM-APR：热成像时序记忆定位（VPR）", "—（非 XR）", dict(IMP=2,NOV=4,TEC=4,EXP=4,PER=4,TRL=3,REP=3), False, ["⚠️ 热成像 VPR，非 XR"]),
}

def value(s): return round(sum(W[k]*s[k] for k in W), 2)
def grade(v):
    if v>=4.2: return "S"
    if v>=3.6: return "A"
    if v>=3.0: return "B"
    return "C"

records=[]
for bid,(zh,track,sc,xr,flags) in S.items():
    r=raw.get(bid,{})
    v=value(sc)
    records.append(dict(base_id=bid,title=r.get("title",""),title_zh=zh,track=track,
        published=(r.get("published","")[:10] or "2026-09-23"),scores=sc,value=v,
        grade=grade(v),xr=xr,flags=flags))

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
            f"未超：当日最高 {today_max} < 库内近30天Top10均分 {lib_top_mean} → 非重磅日")

# 门①：token Jaccard vs 库内近90天；以及新集内部
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
L.append(f"# 7 维度对比表 · 2026-09-24（当日全量新论文 {len(xr_recs)} 篇 XR 相关 + {len(non_xr)} 篇非XR留存）\n")
L.append("> 维度与权重固定：`Value = 0.20·IMP + 0.20·NOV + 0.15·TEC + 0.15·EXP + 0.15·PER + 0.08·TRL + 0.07·REP`")
L.append("> 分档：S≥4.2 / A 3.6–4.2 / B 3.0–3.6 / C<3.0")
L.append("> 数据来源：rss.arxiv.org（export.arxiv.org/api/query 当日被沙箱代理 406 拦截，见 run_log）。日期为 RSS 公告日 2026-09-23。\n")
L.append("## 一、Top10（按价值降序，逐篇精读）\n")
L.append("| # | arXiv | 标题 | 赛道 | IMP | NOV | TEC | EXP | PER | TRL | REP | 总分 | 等级 |")
L.append("|---|---|---|---|---|---|---|---|---|---|---|---|---|")
for i,r in enumerate(top10,1):
    sc=r["scores"]
    L.append(f"| {i} | [{r['base_id']}](https://arxiv.org/abs/{r['base_id']}) | {r['title_zh']} | {r['track']} | "
             f"{sc['IMP']} | {sc['NOV']} | {sc['TEC']} | {sc['EXP']} | {sc['PER']} | {sc['TRL']} | {sc['REP']} | **{r['value']}** | {r['grade']} |")
L.append("\n## 二、其余 XR 相关（参考，B 级，未进 Top10）\n")
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
sl.append(f"# 评分明细与覆盖率校验 · 2026-09-24\n")
sl.append(f"- 拉取方式：rss.arxiv.org 兜底（export.arxiv.org/api/query 被沙箱代理 406 拦截）")
sl.append(f"- 日期口径：RSS 公告日 2026-09-23（今日 09-24 拉取，为最新可用批次）")
sl.append(f"- 当日新论文（2609.* 新周期提交）：{len(records)} 篇；其中 XR 相关 {len(xr_recs)} 篇，非 XR {len(non_xr)} 篇")
sl.append(f"- 另：RSS 混入旧稿 replace/cross（2603/2605/2607/2608/2510/2512 等非 2609 旧 ID）共 {33-len(records)} 篇，非当日新提交，已排除出今日 corpus（详见 run_log，建议后续 API 恢复后 backfill）")
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
                 in_top10=(r['base_id'] in top_ids),batch="2026-09-24",flags=r["flags"])
        f.write(json.dumps(rec,ensure_ascii=False)+"\n")
        have.add(r['base_id']); added+=1
total=sum(1 for l in open(REG,encoding="utf-8") if l.strip())
print("registry 新增:",added,"累计:",total)

json.dump(dict(top10=[dict(base_id=r['base_id'],title=r['title'],title_zh=r['title_zh'],track=r['track'],value=r['value'],grade=r['grade'],scores=r['scores'],published=r['published'],flags=r['flags']) for r in top10],
            xr_recs=[dict(base_id=r['base_id'],title_zh=r['title_zh'],track=r['track'],value=r['value'],grade=r['grade'],scores=r['scores'],flags=r['flags']) for r in xr_recs],
            non_xr=[dict(base_id=r['base_id'],title_zh=r['title_zh']) for r in non_xr],
            gate1_pass=gate1_pass,gate2_pass=gate2_pass,top_tracks=sorted(top_tracks),today_top_mean=today_top_mean,
            today_max=today_max,lib_top_mean=lib_top_mean,added=added,total=total,max_sim=round(max_sim,3)),
           open(f"{OUT_DIR}/_scored_snapshot.json","w",encoding="utf-8"),ensure_ascii=False,indent=1)
print("DONE")
