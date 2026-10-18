#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""生成 registry.jsonl / 7维对比表 / 评分与覆盖率校验表。"""
import json, os

RAW = "data/raw/2026-09-20.jsonl"
W = dict(IMP=.20, NOV=.20, TEC=.15, EXP=.15, PER=.15, TRL=.08, REP=.07)
TRACKS = ["渲染与显示", "重建与SLAM", "神经渲染", "交互与输入", "触觉与多模态", "化身与人体",
          "空间计算与UI", "感知与认知", "系统与平台", "内容生成", "世界模型与仿真", "评估与数据集"]
XR_CORE = {"渲染与显示", "交互与输入", "触觉与多模态", "空间计算与UI", "感知与认知", "化身与人体"}

# id: (中文简称, 赛道, IMP,NOV,TEC,EXP,PER,TRL,REP)
S = {
 "2609.20818": ("SplashSplat 飞溅液体多视角重建", "内容生成", 4,4,5,5,4,3,4),
 "2609.20719": ("VR 老龄化·数字素养×交互模态", "感知与认知", 5,3,4,5,3,4,3),
 "2609.20649": ("DexTouch-WM 人类触觉世界模型", "触觉与多模态", 4,4,4,5,4,3,3),
 "2609.20638": ("PROVIA 程序状态跟踪在线查错", "感知与认知", 4,4,4,4,3,3,4),
 "2609.20623": ("PhGS 单目前馈3DGS后验剪枝", "渲染与显示", 3,3,3,3,4,3,3),
 "2609.20615": ("INSPECT 机器人视角选择学习", "交互与输入", 3,3,4,4,3,3,4),
 "2609.20604": ("农业语义SLAM贝叶斯推断", "重建与SLAM", 3,2,3,3,2,3,2),
 "2609.20589": ("RawSLAM 在线HDR高斯SLAM", "重建与SLAM", 4,5,5,5,5,3,3),
 "2609.20586": ("CoRef-GS 多智能体指代高斯", "重建与SLAM", 3,4,4,4,3,3,4),
 "2609.20414": ("TouchSight 裸手触觉预测", "触觉与多模态", 4,4,4,4,4,3,3),
 "2609.20349": ("路径与支撑定性推理模型", "空间计算与UI", 2,2,3,2,2,2,2),
 "2609.20348": ("EliGSiR 有界算力持续建图", "重建与SLAM", 4,4,4,4,4,3,3),
 "2609.20330": ("RoboFind 多智能体个性化寻物", "交互与输入", 4,4,4,5,5,3,3),
 "2609.20034": ("Astronex-World 1.0 实时世界模型", "世界模型与仿真", 3,4,5,5,5,4,5),
 "2609.20012": ("GRF-Recon 全局射线场长序列重建", "重建与SLAM", 4,4,5,4,4,3,4),
 "2609.19907": ("GS-PI PBR高斯材质生成", "渲染与显示", 4,4,4,3,4,3,3),
 "2609.19881": ("BinoGen 自我中心双目数据合成", "评估与数据集", 4,3,4,4,4,3,3),
 "2609.19876": ("SlugTrails 大型建筑平面图定位", "评估与数据集", 4,3,3,4,3,3,4),
 "2609.19863": ("Feel-WM 越野导航本体感世界模型", "世界模型与仿真", 3,4,4,4,3,3,3),
 "2609.19840": ("KoUniTalk 韩英3D说话人脸基准", "化身与人体", 2,2,3,3,2,2,3),
 "2609.19815": ("SnapPhysics 单图物理场景图", "空间计算与UI", 5,4,4,4,4,3,4),
 "2609.19793": ("AI智能眼镜综述", "系统与平台", 4,2,3,2,2,3,4),
 "2609.19782": ("绘画多解性物质化", "内容生成", 2,3,3,3,2,3,3),
 "2609.19750": ("DELUGE 实时粒子流压缩", "系统与平台", 5,4,5,5,5,4,4),
 "2609.19747": ("STAR 光场重建测试时自适应", "渲染与显示", 3,3,4,3,3,2,3),
 "2609.19716": ("GAPrompt++ 几何感知点云提示", "重建与SLAM", 3,3,4,4,4,3,4),
 "2609.19628": ("VGGT-GS SLAM 无标定单目", "重建与SLAM", 4,4,4,4,4,3,3),
 "2609.19600": ("WorldContact 接触中心世界模型", "世界模型与仿真", 3,4,4,4,4,3,3),
 "2609.19551": ("企业系统世界模型持续发现", "世界模型与仿真", 2,3,3,3,3,2,2),
 "2609.19533": ("SLAMSqueezeBench 资源约束SLAM", "评估与数据集", 4,3,4,4,3,3,4),
 "2609.19518": ("AMB3R-SLAM 公里级分层后端", "重建与SLAM", 5,4,5,5,5,3,3),
 "2609.19505": ("FenceXR AR击剑动作回放", "空间计算与UI", 4,3,4,4,4,3,3),
 "2609.19463": ("ParticleSplat 潜粒子泼溅", "内容生成", 3,4,4,3,3,3,4),
 "2609.19421": ("RGS 反射感知高斯泼溅", "渲染与显示", 3,3,4,4,3,3,4),
 "2609.19340": ("ViLoMan 人形全身移动操作", "化身与人体", 3,4,4,4,4,3,4),
 "2609.19330": ("SemSafe-3DGS 语义风险导航", "世界模型与仿真", 3,3,4,3,3,3,3),
 "2609.19315": ("GAVEL 图世界模型LLM规划校验", "世界模型与仿真", 3,4,5,5,5,3,3),
 "2609.19142": ("PointZero 3D点轨迹补全动力学", "世界模型与仿真", 3,4,5,5,4,3,4),
}

# 覆盖度回补：XR核心赛道保护
BACKFILL = {"2609.20649": "XR核心赛道「触觉与多模态」在纯分数 Top10 中缺席，取该赛道最高分者入替 2609.19142"}
DROP = {"2609.19142": "「世界模型与仿真」赛道第3篇（同赛道已有2篇），且 XR 迁移路径最弱（纯机器人操作动力学、无 XR 评测）"}

def val(t):
    k = ["IMP","NOV","TEC","EXP","PER","TRL","REP"]
    return round(sum(W[k[i]]*t[2+i] for i in range(7)), 2)

def grade(v):
    return "S" if v >= 4.2 else ("A" if v >= 3.6 else ("B" if v >= 3.0 else "C"))

rows = [json.loads(l) for l in open(RAW, encoding="utf-8")]
recs = []
for r in rows:
    b = r["base_id"]
    if b not in S:
        continue
    zh, tr, *sc = S[b]
    v = val(S[b])
    recs.append({**r, "zh": zh, "track": tr, "value": v, "grade": grade(v),
                 "scores": dict(zip(["IMP","NOV","TEC","EXP","PER","TRL","REP"], sc))})

recs.sort(key=lambda x: -x["value"])

# --- registry ---
os.makedirs("papers/library", exist_ok=True)
with open("papers/library/registry.jsonl", "a", encoding="utf-8") as f:
    for r in recs:
        f.write(json.dumps({"id": "arXiv:" + r["base_id"], "title": r["title"], "title_zh": r["zh"],
                            "track": r["track"], "date": r["published"][:10], "value": r["value"],
                            "grade": r["grade"], "scores": r["scores"],
                            "status": "CURRENT", "evidence": "ABSTRACT_ONLY"}, ensure_ascii=False) + "\n")

# --- 7维表 ---
def tbl(items, path, title, note=""):
    L = [f"# {title}", "", note, "",
         "| # | 论文（中） | arXiv | 赛道 | IMP | NOV | TEC | EXP | PER | TRL | REP | **总分** | 等级 |",
         "|---|---|---|---|---|---|---|---|---|---|---|---|---|"]
    for i, r in enumerate(items, 1):
        s = r["scores"]
        L.append(f"| {i} | {r['zh']} | `{r['base_id']}` | {r['track']} | "
                 f"{s['IMP']} | {s['NOV']} | {s['TEC']} | {s['EXP']} | {s['PER']} | {s['TRL']} | {s['REP']} | "
                 f"**{r['value']:.2f}** | {r['grade']} |")
    open(path, "w", encoding="utf-8").write("\n".join(L) + "\n")

os.makedirs("papers/daily/2026-09-20", exist_ok=True)
tbl(recs, "papers/daily/2026-09-20/7dim-table.md",
    "2026-09-20 当日拉取全量论文 7 维度对比表（38 篇）",
    f"> 权重：`Value = 0.20·IMP + 0.20·NOV + 0.15·TEC + 0.15·EXP + 0.15·PER + 0.08·TRL + 0.07·REP`\n"
    f"> 等级：S ≥ 4.2 ／ A 3.6–4.2 ／ B 3.0–3.6 ／ C < 3.0\n"
    f"> 时间窗口：2026-09-16 ~ 2026-09-17（arXiv 周末无新提交，按 skill 规则回溯 3 天）\n\n"
    f"**维度**：`IMP`问题重要性 · `NOV`方法创新性 · `TEC`技术完整度 · `EXP`实验强度 · "
    f"`PER`性能增益 · `TRL`落地成熟度 · `REP`可复现与影响力")

# Top10 (回补后)
ranked = recs[:11]
top10, dropped = [], []
for r in ranked:
    if r["base_id"] in DROP or len(top10) >= 10:
        if r["base_id"] in DROP or len(top10) >= 10:
            dropped.append(r)
            continue
    top10.append(r)
for r in recs[11:]:
    if r["base_id"] in BACKFILL and len(top10) < 10:
        top10.append(r)
top10 = top10[:10]
tbl(top10, "papers/daily/2026-09-20/scored.md", "2026-09-20 入选 Top10 评分明细", "")

tracks = {}
for r in top10:
    tracks[r["track"]] = tracks.get(r["track"], 0) + 1
print("TOP10:", [(r["base_id"], r["value"], r["track"]) for r in top10])
print("TRACKS:", tracks)
print("DROPPED:", [(r["base_id"], r["value"]) for r in dropped])
json.dump([{k: r[k] for k in ("base_id","zh","track","value","grade","title")} for r in top10],
          open("data/top10.json","w",encoding="utf-8"), ensure_ascii=False, indent=1)
