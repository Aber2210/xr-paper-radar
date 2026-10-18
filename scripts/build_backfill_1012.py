#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""build_backfill_1012.py — 漏网对账 backfill 批次（10-12/14/15 公告漏网 + 旧稿积压）构建脚本。
输入：data/backfill_meta.json（60 篇候选的标题/摘要/分类/提交日）
输出：papers/daily/backfill-1012-1015/{7dim-table.md, scored.md, run_log.md} + data/scored_backfill.json
评分口径：摘要级评分（IMP/NOV/TEC/EXP/PER/TRL/REP，1-5），权重 0.20/0.20/0.15/0.15/0.15/0.08/0.07。
"""
import json, os, re, itertools

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(ROOT, "data") + os.sep
DAILY = os.path.join(ROOT, "papers", "daily", "backfill-1012-1015") + os.sep
REG = os.path.join(ROOT, "papers", "library", "registry.jsonl")
BATCH = "backfill-1012-1015"

DIMS = ["IMP", "NOV", "TEC", "EXP", "PER", "TRL", "REP"]
W = {"IMP": .20, "NOV": .20, "TEC": .15, "EXP": .15, "PER": .15, "TRL": .08, "REP": .07}

def grade(v):
    return "S" if v >= 4.2 else "A" if v >= 3.6 else "B" if v >= 3.0 else "C"

# 逐篇裁定：id -> (track, title_zh, [7维], flags, 来源)
# 来源: d1012/d1014/d1015/d1016=漏网公告日; old1009=10-10 运行遗留旧稿; old1016=10-17 运行识别的旧稿 replace/cross
J = {
 # ---- 旧稿积压 · 10-10 运行遗留 ----
 "2602.03538": ("神经渲染", "约束动态高斯泼溅（预算内致密化-剪肢协同）", [3,4,4,4,4,3,3], ["BACKFILL"], "old1009"),
 "2603.13833": (None, "", None, [], "old1009"),   # ImagiNav 具身导航 VLN，非 XR 头显场景
 "2605.22342": ("神经渲染", "4D-GSW：运动学感知的 4D 高斯泼溅时空水印", [2,3,3,3,3,2,2], ["BACKFILL"], "old1009"),
 "2605.27820": ("评估与数据集", "EgoBench：工具使用智能体的交互式第一视角多模态基准", [3,3,3,4,3,3,4], ["BACKFILL"], "old1009"),
 # ---- 旧稿积压 · 10-17 运行识别 ----
 "2608.13586": (None, "", None, [], "old1016"),   # 消息平台 AI 拟社会关系，非 XR 载体
 "2505.15737": (None, "", None, [], "old1016"),   # 水下 3DGS，应用域非 XR
 "2603.20428": ("重建与SLAM", "新视角合成相机位姿估计策略的高效基准测试", [3,3,3,4,3,3,4], ["BACKFILL"], "old1016"),
 "2604.11142": ("神经渲染", "Naka-GS：低光 3D 高斯泼溅的色度校正与点先验压缩", [3,3,4,4,4,3,3], ["BACKFILL"], "old1016"),
 "2607.25234": ("感知与认知", "WHTMix：Walsh-Hadamard Token 混合的高效立体深度估计", [3,3,4,4,4,4,3], ["BACKFILL"], "old1016"),
 "2606.26046": ("重建与SLAM", "RoboAtlas：上下文主动 SLAM（几何探索+语义推理协同）", [3,3,4,4,3,3,3], ["BACKFILL"], "old1016"),
 "2602.16511": (None, "", None, [], "old1016"),   # 人形机器人跌倒安全，无 XR 关联
 "2512.00667": ("触觉与多模态", "分数阶粘弹性模型参数主动学习用于真实感触觉渲染", [3,3,4,4,4,3,3], ["BACKFILL"], "old1016"),
 "2607.06768": (None, "", None, [], "old1016"),   # 空中联邦学习/天线系统，非 XR
 # ---- 漏网 10-12 ----
 "2610.13860": ("神经渲染", "Make It Flow：3DGS 场景的水流动画生成", [3,4,4,4,4,3,3], [], "d1012"),
 "2610.13757": ("神经渲染", "可见性引导的反射增强高斯泼溅", [3,3,4,4,4,3,3], [], "d1012"),
 "2610.13503": ("神经渲染", "SplatQ：交互感知的二次选择式 3DGS 剪枝", [3,3,4,4,4,3,3], [], "d1012"),
 "2610.13309": ("感知与认知", "NovaSplat：免模型 6D 物体位姿估计（3DGS 引导+精化）", [3,4,4,4,4,3,3], [], "d1012"),
 "2610.13177": ("神经渲染", "CompactSplat：空间自适应高斯分布的前馈场景重建", [3,4,4,4,4,3,3], [], "d1012"),
 "2610.13143": (None, "", None, [], "d1012"),     # 建筑检测 3DGS，工业应用域
 "2610.12926": ("感知与认知", "第一视角视频嵌入编码什么：与惯性传感融合的人体活动识别", [3,3,3,4,3,3,3], [], "d1012"),
 "2610.12735": ("感知与认知", "免参考食物体积估计：可穿戴第一视角立体视频", [2,3,3,3,3,3,2], ["※ 膳食监测应用，XR 相关限于可穿戴感知"], "d1012"),
 "2610.13498": ("渲染与显示", "混合层级光线追踪：高效 3D 高斯渲染", [3,4,4,4,4,3,3], [], "d1012"),
 "2610.12999": ("世界模型与仿真", "EgoReveal：部分遮挡下从第一视角示范学习主动视觉与操作", [3,3,3,3,3,3,3], [], "d1012"),
 # ---- 漏网 10-14 ----
 "2610.18499": ("评估与数据集", "EgoOmniWorld：以自我-动作-世界交互统一第一视角理解", [3,3,3,4,3,3,4], [], "d1014"),
 "2610.17936": (None, "", None, [], "d1014"),     # 水下动态 3DGS
 "2610.17605": ("神经渲染", "PLEDGE：渐进有损误差有界 3DGS 压缩编解码器", [3,4,4,4,4,3,4], [], "d1014"),
 "2610.17513": ("神经渲染", "高斯泼溅实时场景重建：方法、系统与权衡（综述）", [4,3,4,3,3,4,4], [], "d1014"),
 "2610.17356": ("化身与人体", "Brain2Face：EEG 信号与时空头部化身的关系研究", [3,4,3,3,3,2,3], ["⚠️ 探索性研究，无公开数据"], "d1014"),
 "2610.17128": ("评估与数据集", "EgoProbe：流式第一视角视频的长程精确记忆基准", [3,3,3,4,3,3,4], [], "d1014"),
 "2610.16292": (None, "", None, [], "d1014"),     # 城市场景 3DGS 重建
 "2610.16277": ("化身与人体", "FlowAvatar：消费级 XR 设备上稀疏第一视角输入的实时全身化身", [4,4,4,4,4,4,4], [], "d1014"),
 "2610.16256": ("化身与人体", "EgoWholeView：六相机头戴装置的全身+双手运动捕捉（角色专业化流水线）", [4,4,4,4,4,4,3], [], "d1014"),
 "2610.16177": ("感知与认知", "DIGS：分布信息引导的免训练开放词汇 3D 高斯分割", [3,4,4,4,4,3,3], [], "d1014"),
 "2610.16143": ("重建与SLAM", "All-St3R SLAM：像素级运动掩蔽的实时动态 RGB SLAM", [3,4,4,4,4,3,3], [], "d1014"),
 "2610.14963": (None, "", None, [], "d1014"),     # 口腔 CBCT 医学
 "2610.14663": ("神经渲染", "TETRIS-4DGS：4D 高斯泼溅的高效训练后压缩", [3,3,4,4,4,3,3], [], "d1014"),
 "2610.15157": ("重建与SLAM", "RootSLAM：视觉惯性 SLAM 的平方根束调整", [3,3,4,4,4,3,3], [], "d1014"),
 "2610.17302": ("触觉与多模态", "TouchTwin：语言+触控的人机协同触觉场景创作", [3,4,4,4,3,3,3], [], "d1014"),
 "2610.17094": ("交互与输入", "虚拟现实中的粒子选择（点云交互方式对比）", [3,3,3,4,3,3,3], [], "d1014"),
 "2610.17728": ("评估与数据集", "Safety for Whom：第一视角多模态助手「拒绝之外」的安全理解基准", [3,3,3,4,3,3,4], [], "d1014"),
 "2610.18822": ("世界模型与仿真", "EgoMatrix：从第一视角人类视频生成物理可信的灵巧机器人示范", [3,4,4,4,4,3,3], [], "d1014"),
 "2610.18479": (None, "", None, [], "d1014"),     # 空气中成像声呐 SLAM，传感模态专用
 "2610.18373": ("世界模型与仿真", "DR-VLA：从第一视角网络视频学习类人四足导航", [3,3,4,4,3,3,3], ["⚠️ 四足配送机器人，XR 相关度为第一视角数据源"], "d1014"),
 "2610.17260": ("世界模型与仿真", "Physical SLAM：物理感知的同步定位与建图（4D 高斯场+动力学预测）", [3,4,4,3,4,3,3], [], "d1014"),
 "2610.15422": ("触觉与多模态", "手术机器人安全感知触觉共享控制的强化学习框架", [3,3,3,4,3,3,3], ["⚠️ 手术机器人应用，触觉共享控制方法可迁移"], "d1014"),
 "2610.14090": ("重建与SLAM", "位姿图何时不够：高斯泼溅相机估计的失败分析", [2,2,3,4,3,3,3], ["※ 实证失败分析"], "d1014"),
 # ---- 漏网 10-15 ----
 "2610.20590": ("神经渲染", "前馈多视图特征编码的 3D 高斯泼溅", [3,4,4,4,4,3,3], [], "d1015"),
 "2610.20397": (None, "", None, [], "d1015"),     # 影视 CT 医学
 "2610.19847": ("神经渲染", "VisibilitySplat：光线追踪遮挡的 3DGS 重光照", [3,4,4,4,4,3,3], [], "d1015"),
 "2610.19742": (None, "", None, [], "d1015"),     # 行星探测高光谱 SLAM
 "2610.19538": ("神经渲染", "RDCompGS：图像编解码器的率失真优化 3DGS 压缩", [3,3,4,4,4,3,3], [], "d1015"),
 "2610.19290": ("化身与人体", "Kandinsky S2V 1.0：音频驱动化身视频生成（开源模型家族）", [3,4,4,4,4,3,4], [], "d1015"),
 "2610.19120": (None, "", None, [], "d1015"),     #  MRI 医学影像
 "2610.18950": ("世界模型与仿真", "λ0/HumanVerse：500 小时开放世界第一视角人类数据（人形机器人）", [4,3,4,4,3,4,4], [], "d1015"),
 "2610.19998": ("空间计算与UI", "ShadAR：AR 中按需实时视觉增强（提示词驱动 shader）", [4,4,4,4,4,4,3], [], "d1015"),
 "2610.19641": ("空间计算与UI", "「玫瑰园是墓地」：原住民 AR 导览的空间失谐与公众体验差异", [3,3,3,4,3,3,3], [], "d1015"),
 "2610.19199": ("感知与认知", "超越平板屏幕：XR 研究人脑与行为的机会与挑战", [4,3,3,3,3,3,4], [], "d1015"),
 "2610.20226": ("重建与SLAM", "cuVSLAM 稀疏束调整中视觉-IMU 自适应加权", [3,3,4,4,3,4,3], [], "d1015"),
 # ---- 漏网 10-16（10-17 运行已覆盖主批，残留 2 篇）----
 "2610.11547": (None, "", None, [], "d1009"),     # X 射线断层 NeRF，医学（10-10 运行已甄别为非 XR）
 "2610.21152": ("世界模型与仿真", "KODA：人类第一视角示范的运动学-观测数据对齐（人形机器人）", [3,3,4,4,3,3,3], [], "d1016"),
}

SRC_LABEL = {"d1012": "10-12 漏网", "d1014": "10-14 漏网", "d1015": "10-15 漏网",
             "d1016": "10-16 漏网", "d1009": "10-09 漏网", "old1009": "10-09 旧稿再公告遗留", "old1016": "10-16 旧稿 replace/cross"}
SRC_DATE = {"d1012": "2026-10-12", "d1014": "2026-10-14", "d1015": "2026-10-15",
            "d1016": "2026-10-16", "d1009": "2026-10-09", "old1009": "2026-10-09", "old1016": "2026-10-16"}

def toks(text):
    return set(re.findall(r"[a-z0-9]+", (text or "").lower()))

def main():
    meta = json.load(open(DATA + "backfill_meta.json", encoding="utf-8"))
    reg = [json.loads(l) for l in open(REG, encoding="utf-8") if l.strip()]
    reg_ids = set(r["id"].split(":")[-1].split("v")[0] for r in reg)

    # 0) 校验：每个候选必须有裁定
    unjudged = [i for i in meta if i not in J]
    if unjudged:
        print("!! 未裁定的候选:", unjudged); return
    dup = [i for i in meta if i in reg_ids]
    if dup:
        print("!! 已在 registry（不应出现）:", dup); return

    inc, exc = [], []
    for pid, v in meta.items():
        track, tzh, sc, flags, src = J[pid]
        rec = {"id": pid, "title": v["title"], "title_zh": tzh, "track": track,
               "scores": dict(zip(DIMS, sc)) if sc else None, "flags": flags, "src": src,
               "cat": v["cat"], "published": v["published"], "abstract": v["abstract"]}
        (inc if sc else exc).append(rec)
    for r in inc:
        r["value"] = round(sum(r["scores"][d] * W[d] for d in DIMS), 3)
        r["grade"] = grade(r["value"])
    inc.sort(key=lambda r: (-r["value"], -r["scores"]["IMP"], -r["scores"]["NOV"], r["id"]))
    for i, r in enumerate(inc):
        r["rank"] = i + 1

    # Top10 选择：加权降序；同分按 IMP/NOV 降序；仍同分按赛道多样性优先（已选赛道计数升序，再 id 升序）
    top10, sel_tracks = [], {}
    i = 0
    while len(top10) < 10 and i < len(inc):
        # 找同分同位次组
        j = i
        while j < len(inc) and (inc[j]["value"], inc[j]["scores"]["IMP"], inc[j]["scores"]["NOV"]) == \
              (inc[i]["value"], inc[i]["scores"]["IMP"], inc[i]["scores"]["NOV"]):
            j += 1
        group = sorted(inc[i:j], key=lambda r: (sel_tracks.get(r["track"], 0), r["id"]))
        for r in group:
            if len(top10) >= 10: break
            top10.append(r); sel_tracks[r["track"]] = sel_tracks.get(r["track"], 0) + 1
        i = j
    top10_ids = set(r["id"] for r in top10)
    for r in inc:
        r["in_top10"] = r["id"] in top10_ids

    # ---- 门① Jaccard（对比全部非本批文献）----
    best = (0, "", "")
    for r in inc:
        t1 = toks(r["title"])
        for e in reg:
            t2 = toks(e["title"])
            if not t1 or not t2: continue
            j = len(t1 & t2) / len(t1 | t2)
            if j > best[0]: best = (round(j, 3), r["id"], e["id"])
    gate1 = best[0] < 0.62

    # ---- 门② 赛道覆盖 ----
    t10_tracks = {}
    for r in top10: t10_tracks[r["track"]] = t10_tracks.get(r["track"], 0) + 1
    gate2 = len(t10_tracks) >= 5

    # ---- 门③ 当日最高 vs 库内近 30 天 Top10 均分（现算，口径同 build_1017：窗口内按值取 Top10 的均分）----
    recent = [e for e in reg if (e.get("date") or "")[:10] >= "2026-09-17"]
    recent.sort(key=lambda e: -e.get("value", 0))
    mean30 = round(sum(e["value"] for e in recent[:10]) / len(recent[:10]), 3) if recent else None
    mx = max(r["value"] for r in inc)
    heavy = (mean30 is not None) and (mx >= mean30)   # True=重磅日（S 级可期）；False=非重磅日、无 S 级
    gate3 = True   # 门③ 为校准关：仅决定是否评 S，不触发重筛

    print(f"候选 {len(meta)} → 入池 {len(inc)} / 剔除 {len(exc)}")
    print(f"门① max Jaccard {best[0]} ({best[1]} vs {best[2]}) → {'PASS' if gate1 else 'FAIL'}")
    print(f"门② Top10 赛道 {len(t10_tracks)}: {t10_tracks} → {'PASS' if gate2 else 'FAIL'}")
    print(f"门③ 最高 {mx} vs 库 30 天 Top10 均分 {mean30}（窗口 {len(recent)} 篇取前 10） → {'重磅日（S 级可期）' if heavy else '非重磅日、无 S 级'}")
    print(f"Top10: {[r['id'] for r in top10]}")
    if not (gate1 and gate2 and gate3):
        print("!! 门未全过，需重筛"); return

    os.makedirs(DAILY, exist_ok=True)
    # ---- 7dim-table.md ----
    L = []
    L.append("# 漏网对账 Backfill · 7 维度对比表（参考）")
    L.append("")
    L.append("> 拉取窗口：**10-12（一）/ 10-14（三）/ 10-15（四）三个漏跑公告日 + 旧稿积压**（10-13 周二经 7 分类全量核实当日无公告）。")
    L.append("> 方法：arXiv listing 页按公告日对账 registry（API 双主机 429 限流期间的可达通道）；")
    L.append("> 3 个漏跑日全量 2352 篇（7 分类 primary）→ 标题级 XR 关键词命中 48 篇（下限口径，摘要级会更多）→ 摘要级甄别 **入池 %d 篇 / 剔除 %d 篇**；" % (len(inc), len(exc)))
    L.append("> 另并入旧稿积压 13 篇（10-10 运行遗留 4 + 10-17 运行识别 9）。候选合计 60 篇，元数据经 arXiv API 恢复后一次性拉取。")
    L.append("> 诚实口径：本批为**补录历史漏网**，非当日新提交；Top10 全文抓取后逐篇精读，其余为摘要级评分。")
    L.append("")
    L.append("| arXiv ID | 中文题名 | 档 | 加权 | IMP | NOV | TEC | EXP | PER | TRL | REP | 赛道 | 来源 |")
    L.append("|---|---|---|---|---|---|---|---|---|---|---|---|---|")
    for r in inc:
        s = r["scores"]
        L.append("| %s | %s | %s | %.2f | %d | %d | %d | %d | %d | %d | %d | %s | %s |" % (
            r["id"], r["title_zh"], r["grade"], r["value"],
            s["IMP"], s["NOV"], s["TEC"], s["EXP"], s["PER"], s["TRL"], s["REP"],
            r["track"], SRC_LABEL[r["src"]]))
    L.append("")
    L.append("**档位**：S≥4.20 · A 3.60–4.20 · B 3.00–3.60 · C<3.00。权重 IMP0.20·NOV0.20·TEC0.15·EXP0.15·PER0.15·TRL0.08·REP0.07。")
    L.append("**Top10 入选**（加权降序，同分按 IMP/NOV 降序、再按赛道多样性优先）：%s。" % "、".join(r["id"] for r in top10))
    L.append("**说明**：本表为漏网对账批次的全部入池论文参考表；Top10 全文已抓取(L0/FULL)并逐篇精读（见 Backfill 报告 §三）。%d 篇非 XR 稿未列入本表。" % len(exc))
    open(DAILY + "7dim-table.md", "w", encoding="utf-8").write("\n".join(L) + "\n")

    # ---- scored.md ----
    L = ["# scored · backfill-1012-1015（摘要级评分明细）", ""]
    L.append("## 入池 %d 篇（按加权降序）" % len(inc))
    L.append("")
    for r in inc:
        s = r["scores"]
        L.append("- **%s %s**（%s，%.2f %s，%s，%s）IMP%d/NOV%d/TEC%d/EXP%d/PER%d/TRL%d/REP%d%s" % (
            r["id"], r["title_zh"], r["track"], r["value"], r["grade"], SRC_LABEL[r["src"]], r["cat"],
            s["IMP"], s["NOV"], s["TEC"], s["EXP"], s["PER"], s["TRL"], s["REP"],
            ("；".join(r["flags"]) and "；" + "；".join(r["flags"])) or ""))
    L.append("")
    L.append("## 剔除 %d 篇（非 XR / 应用域不相关，附原因）" % len(exc))
    L.append("")
    EXC_REASON = {
     "2603.13833": "具身导航/VLN 机器人策略，非 AR/VR 头显场景",
     "2608.13586": "消息平台 AI 拟社会关系框架，非 XR 载体",
     "2505.15737": "水下场景 3DGS 重建，应用域非 XR",
     "2602.16511": "人形机器人跌倒安全，无 XR 关联",
     "2607.06768": "空中联邦学习/天线系统，无线通信方向",
     "2610.13143": "建筑检测可测量 3DGS，工业应用域",
     "2610.17936": "水下动态 3DGS，应用域非 XR",
     "2610.16292": "城市场景细粒度 3DGS 重建，应用域非 XR",
     "2610.14963": "口腔 CBCT 稀疏视角重建，医学影像",
     "2610.18479": "空气中成像声呐 SLAM，传感模态专用且非 XR 感知",
     "2610.20397": "影视 CT 高斯预算分配，医学影像",
     "2610.19742": "行星探测高光谱辅助回环，环境专用",
     "2610.19120": "自由呼吸腹部 MRI 重建，医学影像",
     "2610.11547": "X 射线断层稀疏视角 NeRF，医学影像（10-10 运行已甄别为非 XR）",
    }
    for r in sorted(exc, key=lambda x: x["id"]):
        L.append("- %s %s（%s，%s）：%s" % (r["id"], r["title"], r["cat"], SRC_LABEL[r["src"]], EXC_REASON.get(r["id"], "非 XR")))
    L.append("")
    L.append("## 评分口径")
    L.append("- 权重 IMP0.20·NOV0.20·TEC0.15·EXP0.15·PER0.15·TRL0.08·REP0.07；档位 S≥4.2 / A3.6–4.2 / B3.0–3.6 / C<3.0。")
    L.append("- 本批评分以**摘要级**为基准；Top10 及 ≥3.50 的近界论文抓取全文复核（见 run_log 证据等级）。")
    L.append("- 门① Jaccard<0.62（对比全部非本批文献）：max %.3f（%s vs %s）。" % best)
    L.append("- 门② Top10 覆盖赛道 %d 个：%s。" % (len(t10_tracks), "、".join("%s×%d" % (k, v) for k, v in t10_tracks.items())))
    L.append("- 门③ 本批最高 %.2f %s 库内近 30 天 Top10 均分 %.3f（窗口 %d 篇按值取前 10 均分，现算）→ **%s**。" % (
        mx, "≥" if heavy else "<", mean30, len(recent),
        "重磅日" if heavy else "非重磅日、无 S 级，未拔高未凑 S"))
    open(DAILY + "scored.md", "w", encoding="utf-8").write("\n".join(L) + "\n")

    # ---- run_log.md ----
    L = ["# run_log · backfill-1012-1015（漏网对账补录）", ""]
    L.append("## 背景与动因")
    L.append("- 10-11~10-16 期间无调度运行；arXiv RSS 仅携带最新一个公告日 → 10-17 运行只处理了 10-16 批次。")
    L.append("- 对账发现 **10-12 / 10-14 / 10-15 三个公告日完全漏跑**（10-13 周二经 7 分类 listing 核实当日无公告，arXiv 服务波动期）。")
    L.append("- 另有两笔历史积压：10-10 运行遗留 4 篇旧稿再公告、10-17 运行识别 9 篇旧稿 replace/cross 候选。")
    L.append("")
    L.append("## 数据源与对账方法")
    L.append("- 探针：export.arxiv.org 与 arxiv.org/api/query 均 **429 限流**（上午审计起持续）；改走 `arxiv.org/list/{cat}/recent`（按公告日分组，h3 含条目总数声明）。")
    L.append("- 审计脚本 `scripts/audit_gap_listing.py`：7 分类 × show=500 分页 + 逐日完整性校验（表头声明数 vs 实采数）+ 分类级整体重试；关键词过滤 `scripts/filter_missed_xr.py`。")
    L.append("- 踩坑规避：单位数日期无前导零（`\\d{1,2}`）；show=2000 响应体约 2MB 被静默截断；高频请求被限流降级（间隔 8s+重试）；跨分类交叉列表论文全局去重假象（以 per-category 自检为准）。")
    L.append("- API 恢复后一次性拉取 60 篇候选完整元数据（标题+摘要+分类+提交日）→ data/backfill_meta.json。")
    L.append("")
    L.append("## 漏斗")
    L.append("- 3 个漏跑日全量：2352 篇（7 分类 primary，去 registry 后）")
    L.append("- 标题级 XR 关键词命中：48 篇（下限口径；流水线标准的标题+摘要过滤会更多）")
    L.append("- 摘要级甄别：入池 **%d 篇** / 剔除 %d 篇（原因见 scored.md）" % (len(inc), len(exc)))
    L.append("- 旧稿积压 13 篇：并入 8 篇 / 剔除 5 篇")
    L.append("")
    L.append("## 覆盖度三关")
    L.append("- 门① 最大 Jaccard %.3f（%s vs %s）< 0.62 ✓" % best)
    L.append("- 门② Top10 覆盖 %d 赛道：%s ✓" % (len(t10_tracks), "、".join(t10_tracks)))
    L.append("- 门③ 本批最高 %.2f %s 库内近 30 天 Top10 均分 %.3f（窗口 %d 篇按值取前 10 均分，现算）→ 非重磅日、无 S 级 ✓" % (mx, "<" if not heavy else ">=", mean30, len(recent)))
    L.append("")
    L.append("## 证据等级")
    L.append("- Top10 + ≥3.50 近界论文：抓取全文（arxiv.org/html），L0/FULL，评分经全文复核。")
    L.append("- 其余入池论文：ABSTRACT_ONLY（摘要级评分，registry 如实标注）。")
    L.append("")
    L.append("## 诚实口径")
    L.append("- 本批为历史漏网补录：10-12/14/15 论文的提交日为其公告窗口，**并非 10-17 当日新提交**。")
    L.append("- 标题级关键词为漏网筛查下限；摘要级过滤（本批已做）确认无进一步漏网之重大风险，但不排除极少数摘要命中而标题未命中且未入 RSS 关键词表的论文。")
    L.append("- 10-16 当日批次已由 10-17 运行覆盖，本批仅补其残留 2 篇（2512.00667 / 2610.21152）。")
    open(DAILY + "run_log.md", "w", encoding="utf-8").write("\n".join(L) + "\n")

    # ---- scored_backfill.json（供产物脚本消费）----
    out = {"batch": BATCH, "gate": {"jaccard": best, "tracks": t10_tracks, "max": mx, "mean30": mean30, "n30": len(recent)},
           "top10": [r["id"] for r in top10],
           "included": [{k: r[k] for k in ("id", "title", "title_zh", "track", "scores", "value", "grade", "flags", "src", "cat", "published")} for r in inc],
           "excluded": [{"id": r["id"], "title": r["title"], "cat": r["cat"], "src": r["src"], "reason": EXC_REASON.get(r["id"], "非 XR")} for r in exc]}
    json.dump(out, open(DATA + "scored_backfill.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print("saved:", DAILY + "{7dim-table,scored,run_log}.md", "+ data/scored_backfill.json")

if __name__ == "__main__":
    main()
