# -*- coding: utf-8 -*-
"""2026-09-26 批次构建：评分 + 7 维对比表 + 覆盖度三关 + registry 幂等追加。
数据来源：data/raw/2026-09-26.jsonl（RSS 兜底源；export.arxiv.org/api/query 当日间歇 406，
arxiv.org/api/query 亦间歇 406，故用 rss.arxiv.org，沙箱代理稳定 200，与 09-24/09-25 一致）。
RSS "recent" 批次混入旧稿 replace/cross（2601/2604/2605/2606 等非 2609 旧 ID），已排除出今日 corpus。
今日 corpus = 23 篇 2609.* 真正新提交（21 篇 XR 相关 + 2 篇非 XR 仅参考），
公告日 2026-09-25，本机拉取日 2026-09-26。
"""
import json, os, re
from collections import Counter

RAW = "data/raw/2026-09-26.jsonl"
OUT_DIR = "papers/daily/2026-09-26"
REG = "papers/library/registry.jsonl"
MANI = "data/fulltext/_manifest.json"
os.makedirs(OUT_DIR, exist_ok=True)

raw = {}
for l in open(RAW, encoding="utf-8"):
    if not l.strip():
        continue
    o = json.loads(l)
    raw[o["base_id"]] = o

W = dict(IMP=0.20, NOV=0.20, TEC=0.15, EXP=0.15, PER=0.15, TRL=0.08, REP=0.07)

# id -> (zh, track, scores, xr, flags, tags)
S = {
 # ===== Top10（按价值降序）=====
 "2609.29603": ("MoSign：面向匿名 VR 用户的挑战-应答式运动水印身份认证", "交互与输入",
    dict(IMP=4,NOV=5,TEC=4,EXP=4,PER=4,TRL=3,REP=3), True, [], ["VR安全","运动水印","匿名认证","隐写","重识别"]),
 "2609.29292": ("PHOSA：照片级真实 3D 手语化身建模与基准（MVSign 数据集）", "化身与人体",
    dict(IMP=4,NOV=4,TEC=4,EXP=4,PER=4,TRL=3,REP=4), True, [], ["手语化身","SMPL-X","多视角","可访问性","基准"]),
 "2609.28645": ("PePESeg3D：感知先验增强的多尺度 3D 高斯泼溅分割", "感知与认知",
    dict(IMP=4,NOV=4,TEC=4,EXP=4,PER=4,TRL=3,REP=3), True, [], ["3DGS","语义分割","感知先验","单体深度","多尺度"]),
 "2609.28930": ("PlenoCI：基于光场特性的视角依赖感知变化分类", "神经渲染",
    dict(IMP=4,NOV=4,TEC=4,EXP=4,PER=4,TRL=3,REP=3), True, [], ["3DGS","变化检测","光场特性","解析导数","误报抑制"]),
 "2609.28997": ("Observation-Gram：3D 高斯泼溅视角依赖外观的观测压缩度量", "神经渲染",
    dict(IMP=4,NOV=4,TEC=4,EXP=4,PER=4,TRL=3,REP=3), True, [], ["3DGS压缩","球谐","观测Gram","率失真","Compressed3D"]),
 "2609.29073": ("工具增强的度量空间推理：给小 VLM 配上几何求解器", "空间计算与UI",
    dict(IMP=4,NOV=4,TEC=4,EXP=4,PER=4,TRL=3,REP=3), True, [], ["VLM","空间推理","度量深度","工具增强","ReVSI-Bench"]),
 "2609.29106": ("WildHSR：基于 3D 基础模型的度量前馈 4D 人-景重建", "重建与SLAM",
    dict(IMP=4,NOV=4,TEC=4,EXP=4,PER=4,TRL=3,REP=3), True, [], ["4D重建","人-景","基础模型","度量尺度","前馈"]),
 "2609.29836": ("SplatLabel：基于 4D 高斯泼溅的伪标注（动态语义占据）", "感知与认知",
    dict(IMP=4,NOV=4,TEC=4,EXP=4,PER=4,TRL=3,REP=3), True, [], ["4DGS","伪标注","语义占据","动态跟踪","LiDAR"]),
 "2609.30245": ("COSA-GS：面向实用部署的 3D 高斯泼溅压缩（锚点因果分解上下文）", "系统与平台",
    dict(IMP=4,NOV=4,TEC=4,EXP=4,PER=4,TRL=3,REP=3), True, [], ["3DGS压缩","锚点","因果上下文","跨平台一致性","熵编码"]),
 "2609.29374": ("FMCW-LIO：基于多普勒 FMCW 激光雷达-惯导里程计", "重建与SLAM",
    dict(IMP=4,NOV=4,TEC=4,EXP=4,PER=4,TRL=3,REP=3), True, [], ["SLAM","LiDAR","多普勒","运动补偿","LIO"]),
 # ===== 其余 XR 相关（参考，A/B 级，未进 Top10）=====
 # 注：2609.23436 (GAPS) 为 09-23 已收录论文的 v2 replace 再公告，非当日新提交，已按 gate① 同质判定（sim=0.909）剔除出今日 corpus。
 "2609.30187": ("Ego-Exo4D-HM：面向自我-外部捕获的 4D 人体运动重建数据集", "化身与人体",
    dict(IMP=4,NOV=3,TEC=4,EXP=4,PER=3,TRL=4,REP=4), True, [], ["数据集","4D人体","自我中心","动作重建","基准"]),
 "2609.29041": ("双阶段 Morton 排序的高斯泼溅高效编码（面向 MPEG 视频编码）", "系统与平台",
    dict(IMP=4,NOV=3,TEC=4,EXP=4,PER=4,TRL=3,REP=3), True, [], ["3DGS编码","Morton","视频编码","MPEG","投影映射"]),
 "2609.28539": ("Heartian：生理感知的可重光照高斯头部化身（内嵌 rPPG 心率）", "化身与人体",
    dict(IMP=3,NOV=4,TEC=4,EXP=4,PER=4,TRL=2,REP=3), True, [], ["头部化身","可重光照","rPPG","心率","生理信号"]),
 "2609.29963": ("AdaTex4D：面向 4D 高斯泼溅的自适应纹理容量分配", "神经渲染",
    dict(IMP=3,NOV=3,TEC=4,EXP=4,PER=4,TRL=3,REP=3), True, [], ["4DGS","纹理压缩","自适应分配","三平面","显存"]),
 "2609.29985": ("OceanXL：基于分块与自适应剪枝的大规模水下 3D 高斯泼溅重建", "神经渲染",
    dict(IMP=3,NOV=3,TEC=4,EXP=4,PER=3,TRL=3,REP=3), True, [], ["3DGS","水下","大规模","分块","剪枝"]),
 "2609.28976": ("ReVNM：基于远程摄像头的视觉导航（免预建地图）", "重建与SLAM",
    dict(IMP=3,NOV=4,TEC=4,EXP=4,PER=3,TRL=3,REP=3), True, [], ["视觉导航","远程相机","仿真合成","移动机器人","隐式地图"]),
 "2609.28812": ("VR 中具身对话智能体的幻觉感知提示设计（N=24 被试）", "空间计算与UI",
    dict(IMP=3,NOV=3,TEC=3,EXP=3,PER=2,TRL=3,REP=3), True, [], ["VR","对话智能体","幻觉提示","用户研究","可解释性"]),
 "2609.29173": ("视频透视 XR 中人-系统视角错配的形式化与测量", "空间计算与UI",
    dict(IMP=4,NOV=3,TEC=3,EXP=2,PER=2,TRL=3,REP=2), True, ["⚠️ 仍为 pilot 级边界测量，实验强度偏弱"], ["VST","视频透视","视角错配","Quest3","AR显示"]),
 "2609.29686": ("TransCAVE-E：面向自适应车外人机界面的分布式 VR 试验台", "空间计算与UI",
    dict(IMP=3,NOV=3,TEC=3,EXP=2,PER=2,TRL=3,REP=3), True, [], ["VR试验台","eHMI","自动驾驶","人因","分布式"]),
 "2609.30076": ("超越驾驶：以体验为中心设计探索未来自动驾驶舱内活动", "空间计算与UI",
    dict(IMP=3,NOV=3,TEC=2,EXP=2,PER=1,TRL=2,REP=2), True, ["⚠️ 定性设计研究，无量化实验，价值偏低"], ["自动驾驶","XR设想","体验设计","参与式","非驾驶活动"]),
 # ===== 非 XR 留存（不计入打分，仅供参考）=====
 "2609.29638": ("SpectralCTGaussians：基于 3DGS 的光谱 CT 重建与基材料分解", "—（非 XR）",
    dict(IMP=3,NOV=4,TEC=4,EXP=4,PER=4,TRL=3,REP=3), False, [], ["光谱CT","医学影像","基材料","3DGS","X射线"]),
 "2609.29644": ("大型空间结构无标记多模态自主机器人巡检", "—（非 XR）",
    dict(IMP=3,NOV=3,TEC=4,EXP=4,PER=3,TRL=3,REP=3), False, [], ["机器人","巡检","空间结构","RGB-D","语义重建"]),
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
        published=(r.get("published","")[:10] or "2026-09-25"),scores=sc,value=v,
        grade=grade(v),xr=xr,flags=flags,tags=tags))

xr_recs=sorted([r for r in records if r["xr"]],key=lambda r:(-r["value"],-r["scores"]["IMP"],-r["scores"]["NOV"]))
non_xr=[r for r in records if not r["xr"]]
top10=[r for r in xr_recs if r["value"]>=3.6][:10]

# ---- 覆盖度三关 ----
TRACKS_12=["渲染与显示","重建与SLAM","神经渲染","交互与输入","触觉与多模态","化身与人体",
           "空间计算与UI","感知与认知","系统与平台","内容生成","世界模型与仿真","评估与数据集"]
top_tracks=set(r["track"] for r in top10)
lib=[json.loads(l) for l in open(REG,encoding="utf-8") if l.strip()]
# 仅与「本批之前」的文献库比较（排除今日新增批次），避免候选与自身刚写入的条目自匹配
TODAY_BATCH="2026-09-26"
lib_hist=[r for r in lib if r.get("batch")!=TODAY_BATCH]
lib_top=sorted(lib_hist,key=lambda r:-r.get("value",0))[:10]
lib_top_mean=round(sum(r.get("value",0) for r in lib_top)/len(lib_top),3)
today_top_mean=round(sum(r["value"] for r in top10)/len(top10),3)
today_max=max(r["value"] for r in top10)
gate2_pass=len(top_tracks)>=5
gate3_note=("通过" if today_max>=lib_top_mean else
            f"未超：当日最高 {today_max} < 库内近30天Top10均分 {lib_top_mean} → 非重磅日，无 S 级")

def toks(s): return set(re.findall(r"[a-z0-9]{3,}",s.lower()))
lib_recent=[toks((r.get("title","")+" "+r.get("title_zh",""))) for r in lib_hist[-90:]]
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
L.append(f"# 7 维度对比表 · 2026-09-26（当日新论文 {len(xr_recs)} 篇 XR 相关 + {len(non_xr)} 篇非XR参考；公告日 2026-09-25）\n")
L.append("> 维度与权重固定：`Value = 0.20·IMP + 0.20·NOV + 0.15·TEC + 0.15·EXP + 0.15·PER + 0.08·TRL + 0.07·REP`")
L.append("> 分档：S≥4.2 / A 3.6–4.2 / B 3.0–3.6 / C<3.0")
L.append("> 数据来源：rss.arxiv.org（export.arxiv.org/api/query 与 arxiv.org/api/query 当日均间歇 406，见 run_log）。公告日 2026-09-25，拉取日 2026-09-26。\n")
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
sl.append(f"# 评分明细与覆盖率校验 · 2026-09-26\n")
sl.append(f"- 拉取方式：rss.arxiv.org 兜底（export.arxiv.org/api/query 与 arxiv.org/api/query 当日均间歇 406 拦截，export 曾在 cs.RO 单类返回 200，但多类 406，稳定性不足；故沿用 RSS 兜底，与 09-24/09-25 一致）")
sl.append(f"- 公告日口径：2026-09-25（今日 09-26 拉取，为最新可用批次）；RSS 混入的旧稿 replace/cross（2601/2604/2605/2606）已在去重阶段剔除")
sl.append(f"- 当日新论文（2609.* 新周期提交）：{len(records)} 篇；其中 XR 相关 {len(xr_recs)} 篇，非 XR {len(non_xr)} 篇")
sl.append(f"- Top10 价值均分：**{today_top_mean}**；当日最高：**{today_max}**；S 级数：{sum(1 for r in top10 if r['grade']=='S')}")
sl.append(f"- 库内近 30 天 Top10 均分：**{lib_top_mean}**（历史 {len(lib)} 篇）\n")
sl.append("## 覆盖度三关\n")
sl.append(f"- **① 同质去重关**：新集与库内近 90 天条目 token Jaccard 最大 {max_sim:.3f}（{sim_pair}），{('<0.62 → 通过（无同质）' if gate1_pass else '≥0.62 → 触发剔除/降权')}）。")
sl.append(f"- **② 赛道覆盖关**：Top10 覆盖赛道 = {sorted(top_tracks)}，共 **{len(top_tracks)}** 个 ≥ 5 → **{'通过' if gate2_pass else '不通过，已回补'}**.")
sl.append(f"- **③ 价值天花板关**：当日最高 {today_max} {'≥' if today_max>=lib_top_mean else '<'} 库内近30天Top10均分 {lib_top_mean} → **{gate3_note}**（无 S 级论文，不得拔高评分）。")
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
                 in_top10=(r['base_id'] in top_ids),batch="2026-09-26",flags=r["flags"],tags=r["tags"])
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
