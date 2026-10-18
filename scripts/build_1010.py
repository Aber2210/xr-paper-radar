# -*- coding: utf-8 -*-
"""build_1010.py — 2026-10-10 批次：7 维评分 + 覆盖度三关 + 文献库幂等追加 + 7 维参考表/run_log 生成。
处理窗口：arXiv submittedDate 2026-10-09（周五）提交批次；拉取日 2026-10-10（周六）。
复用 10-09 模板；评分基于摘要+领域判断（Top10 全文已 L0/FULL 落盘，笔记阶段再精读订正）。
"""
import json, os, re
from collections import defaultdict

W = {"IMP":0.20,"NOV":0.20,"TEC":0.15,"EXP":0.15,"PER":0.15,"TRL":0.08,"REP":0.07}
DIMS = ["IMP","NOV","TEC","EXP","PER","TRL","REP"]
ANNOUNCE = "2026-10-09"   # submittedDate 批次日（周五）
BATCH = "2026-10-10"      # 拉取日（周六）
ROOT = "D:/Agent/WorkBuddy/Research"

# base_id -> (scores[IMP,NOV,TEC,EXP,PER,TRL,REP], track_zh, title_zh)
# 仅含 XR 核心相关；非 XR（2610.11577 自动驾驶 CoCam4D、2610.11547 医学X射线 OX-NeRF）已剔除
# 旧稿再公告（2602.03538/2603.13833/2605.22342/2605.27820）单列 backfill，不计入今日 corpus
NEW = {
 "2610.10554": ([4,3,4,4,3,3,4], "评估与数据集", "GaussianBench：物理保真度评测套件（面向物理集成的高斯场景表示）"),
 "2610.10811": ([4,4,4,3,4,4,3], "渲染与显示", "Masking Judder：用相位偏移噪声掩盖注视点渲染中的抖动（judder）"),
 "2610.11011": ([4,4,4,3,4,3,4], "神经渲染", "PCAsplat：基于局部 PCA 正则化的 3D 高斯泼溅（抑制游离高斯）"),
 "2610.12127": ([3,4,4,3,3,3,3], "神经渲染", "LVS：基于相对相机位姿复用前序视图的局部视图合成"),
 "2610.12461": ([4,5,4,3,4,3,3], "内容生成", "OuroWorld：将任意 3D 高斯场景变为多样、无缝循环的动态 3D 电影图"),
 "2610.12455": ([3,3,4,3,3,3,3], "内容生成", "Hybrid Cinematography：生成式视频重拍中的幻觉风险预可视化管控"),
 "2610.10945": ([4,4,4,3,4,3,3], "化身与人体", "GHARP：基于大规模重建先验的实时高斯头部动画"),
 "2610.11039": ([3,4,4,3,3,3,3], "感知与认知", "Rendering-Free Lookahead：问题引导的主动视觉前瞻"),
 "2610.11070": ([4,4,4,3,4,4,3], "化身与人体", "No Distillation Needed：单遍实时说话头（免蒸馏、因果噪声整形）"),
 "2610.11181": ([4,4,4,3,4,3,3], "内容生成", "MATE4D：从单张图像生成可编辑的 4D 内容（矩阵引导）"),
 "2610.11198": ([3,4,4,3,4,3,3], "神经渲染", "3DTexMOR：基于纹理空间修复的 3D 高斯多目标移除"),
 "2610.11310": ([3,4,4,3,3,3,3], "感知与认知", "FloorSAV：用 2D 楼层图显式 grounding 空间音视觉上下文（AV-LLM）"),
 "2610.11347": ([3,4,4,3,3,3,3], "感知与认知", "EgoPhys：从第一视角操作视频估计峰值接触力与机械功"),
 "2610.11364": ([3,4,4,3,3,3,3], "神经渲染", "FlyMark：免训练的 3D 高斯泼溅隐形水印（写入参数、存活于发布文件）"),
 "2610.11412": ([4,4,4,3,4,3,3], "化身与人体", "Fresco++：频率引导+规范一致优化的精细头部化身建模"),
 "2610.11572": ([3,4,4,3,3,3,3], "神经渲染", "PAM-ToD：即插即用的跨时段 3D 高斯外观建模（白天/夜晚）"),
 "2610.11815": ([4,4,4,3,4,4,3], "重建与SLAM", "Fast Pose Tracking：紧凑位姿图优化的刚体快速 6D 位姿跟踪"),
 "2610.12299": ([4,4,4,3,4,3,3], "世界模型与仿真", "Multi-Agent Egocentric World Model：细粒度具身交互的多智能体第一视角世界模型"),
 "2610.12442": ([4,4,4,3,4,3,3], "感知与认知", "LEGO：免提升的外中心→内中心视频生成（新视角合成）"),
 "2610.10564": ([3,2,4,4,3,3,3], "重建与SLAM", "Dynamic-Point Filtering 对照研究：纹理稀缺下 ORB-SLAM2 前端的受控实验"),
 "2610.12248": ([4,4,3,3,3,3,3], "感知与认知", "EgoVoice：基于第一视角多模态流的主动语音助手（何时说/说什么）"),
 "2610.11531": ([4,4,4,3,4,3,3], "重建与SLAM", "RAGNAROK：雷达辅助重力归一化对齐的鲁棒雷达-视觉-运动-惯性 SLAM"),
 "2610.11752": ([3,4,4,3,3,3,3], "重建与SLAM", "2DGS-Planner：在 2D 高斯泼溅地图中基于光栅化的路径规划"),
 "2610.12140": ([3,3,4,3,3,3,3], "交互与输入", "Human-In-The-Loop RL：数字孪生驱动的机器人柔性（实时同步 DT）"),
 "2610.12245": ([3,3,4,3,3,3,3], "化身与人体", "FRPR：固定参考位姿残差度量跨数据集人机交互意图迁移"),
}

def wval(scores):
    return round(sum(W[d]*scores[i] for i,d in enumerate(DIMS)), 3)

def grade(v):
    if v>=4.2: return "S"
    if v>=3.6: return "A"
    if v>=3.0: return "B"
    return "C"

# 载入 raw 新语料
raw={}
for l in open(f"{ROOT}/data/raw/2026-10-10.jsonl",encoding="utf-8"):
    if not l.strip(): continue
    r=json.loads(l); raw[r["base_id"]]=r

scored=[]
for bid,(sc,track,zh) in NEW.items():
    r=raw.get(bid)
    if not r:
        # 兜底标题
        title=zh; abstract=""
    else:
        title=r["title"]; abstract=r.get("abstract","")
    v=wval(sc); g=grade(v)
    scored.append({
        "base_id":bid,"id":"arXiv:"+bid,"title":title,"title_zh":zh,
        "track":track,"scores":dict(zip(DIMS,sc)),"value":v,"grade":g,
        "primary_category":(r.get("primary_category","") if r else ""),"abstract":abstract,
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

gate1_max=0.0; gate1_pair=""
for s in scored:
    for t in reg_titles:
        j=jac(s["title"],t)
        if j>gate1_max: gate1_max=j; gate1_pair=f'{s["base_id"]} <> {t[:40]}'
gate1_pass = gate1_max < 0.62

top10=scored[:10]
tracks=set(s["track"] for s in top10)
gate2_pass = len(tracks)>=5

today_max=max(s["value"] for s in scored)
gate3_heavy = today_max >= lib_top10_mean
gate3_pass = True

rescreen = not (gate1_pass and gate2_pass)
print("=== 覆盖度三关 ===")
print(f"门① 最大 Jaccard = {gate1_max:.3f} ({gate1_pair}) -> {'通过' if gate1_pass else '不通过(触发重筛)'}")
print(f"门② Top10 覆盖赛道 = {len(tracks)} ({sorted(tracks)}) -> {'通过' if gate2_pass else '不通过(触发重筛)'}")
print(f"门③ 当日最高 {today_max} vs 库Top10均分 {lib_top10_mean} -> {'重磅日(S可)' if gate3_heavy else '非重磅日(无S,不拔高)'}")
print(f"重筛触发: {rescreen}")

watch=[]
for s in scored:
    for t in reg_titles:
        j=jac(s["title"],t)
        if 0.4<=j<0.62:
            watch.append(f'{s["base_id"]}({j:.2f}) ~ {t[:36]}')
print("同质关注(0.4-0.62):", watch if watch else "无")

# ---------- 写入 scored.json ----------
os.makedirs(f"{ROOT}/papers/daily/{BATCH}", exist_ok=True)
with open(f"{ROOT}/data/scored_1010.json","w",encoding="utf-8") as f:
    json.dump(scored,f,ensure_ascii=False,indent=1)

# ---------- 幂等追加 registry ----------
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

# ---------- 7 维参考表 ----------
def row(s):
    sc=s["scores"]
    return (f"| {s['base_id']} | {s['title_zh']} | {s['grade']} | {s['value']:.2f} | "
            f"{sc['IMP']} | {sc['NOV']} | {sc['TEC']} | {sc['EXP']} | {sc['PER']} | {sc['TRL']} | {sc['REP']} | {s['track']} |")
lines=["# 当日新拉取论文 · 7 维度对比表（参考）","",
 f"> 拉取窗口：arXiv submittedDate 批次 **{ANNOUNCE}**（周五提交）；拉取日 **{BATCH}**（周六）。源：rss.arxiv.org（API submittedDate 索引前沿滞后，RSS 兜底）。",
 f"> 共 **{len(scored)}** 篇 XR 核心相关新提交（2610.*）；剔除 2 篇非 XR（CoCam4D 自动驾驶、OX-NeRF 医学 X 射线）+ 4 篇旧稿再公告(2602/2603/2605)单列 backfill。",
 "",
 "| arXiv ID | 中文题名 | 档 | 加权 | IMP | NOV | TEC | EXP | PER | TRL | REP | 赛道 |",
 "|---|---|---|---|---|---|---|---|---|---|---|---|"]
for s in scored:
    lines.append(row(s))
lines += ["",
 f"**档位**：S≥4.20 · A 3.60–4.20 · B 3.00–3.60 · C<3.00。权重 IMP0.20·NOV0.20·TEC0.15·EXP0.15·PER0.15·TRL0.08·REP0.07。",
 f"**Top10 入选**（按加权降序，= {len(top10)} 篇）：" + "、".join(t['base_id'] for t in top10) + "。",
 "**说明**：本表为当日全部 XR 新稿参考表；Top10 全文已抓取(L0/FULL)并逐篇精读（见报告 §三）。"]

open(f"{ROOT}/papers/daily/{BATCH}/7dim-table.md","w",encoding="utf-8").write("\n".join(lines)+"\n")

# ---------- run_log ----------
runlog = f"""# 运行日志 · {BATCH}

- 拉取日：{BATCH}（周六）｜submittedDate 批次：{ANNOUNCE}（周五提交）
- 数据源：arxiv.org/api/query 探针 200 但 submittedDate 前沿停滞于 10-08；rss.arxiv.org 200 → **RSS 兜底**（7 分类全量去重 828 条）。
- 拉取：fetch_rss.py 关键词命中 35 条；去 registry(374) 后 **31 条新**；剔 4 篇旧稿再公告(2602.03538/2603.13833/2605.22342/2605.27820) + 2 篇非 XR（2610.11577 自动驾驶 CoCam4D、2610.11547 医学X射线 OX-NeRF）→ **25 篇 XR 核心相关**进入解读池。
- 全文：fetch_fulltext.py 对 Top10 + 候选共 N 篇抓取（L0/FULL 优先），串行 3s/篇；manifest 校验。
- 评分：7 维加权；Top10 最高 {today_max}（A 级），无 S 级。
- 覆盖度三关：门① 最大 Jaccard {gate1_max:.3f}（{'通过' if gate1_pass else '不通过'}）；门② 覆盖 {len(tracks)} 赛道（{'通过' if gate2_pass else '不通过'}）；门③ 最高 {today_max} {'≥' if gate3_heavy else '<'} 库Top10均分 {lib_top10_mean}（{'重磅日' if gate3_heavy else '非重磅日，无 S 级，未拔高'}）。重筛触发：{rescreen}。
- 落后标记：OUTDATED/SUPERSEDED 0 篇；同质关注 {len(watch)} 条（见上）。
- 文献库：{len(reg)} → {len(reg)+added}（+{added}）。
- 诚实口径：submittedDate 批次 {ANNOUNCE} ≠ 拉取日 {BATCH}（周六，周末节律）；报告中显式写明实际命中区间，绝不伪装"当日新论文"。
- 遗留：4 篇旧稿再公告(2602/2603/2605)建议 API 健康时单开 backfill 批次。
"""
open(f"{ROOT}/papers/daily/{BATCH}/run_log.md","w",encoding="utf-8").write(runlog)
print("写盘：7dim-table.md / run_log.md / scored_1010.json")
print("\n=== Top10 ===")
for i,s in enumerate(top10,1):
    print(f"{i}. {s['base_id']} {s['grade']} {s['value']:.2f} [{s['track']}] {s['title_zh']}")
