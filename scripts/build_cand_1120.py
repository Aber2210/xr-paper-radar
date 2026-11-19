"""2026-11-20 候选集构建：从 11-19 公告组 XR 池（68 篇）人工复核后选定主批 22 篇 + backfill 3 篇。

复核口径：逐篇核摘要，剔除缩写/泛词误命中（hand→handoff、spatial→geospatial、depth→LLM depth、
tracking→行为追踪、stereo→stereotyping 等）与明确非 XR 的机器人操作/自驾/医学影像/遥感/科学成像稿。
保留口径：XR 直接相关（HMD/VR 实验/AR 交互）+ XR 管线可用技术（3DGS/NeRF/SLAM/触觉器件/世界模型）。
"""
import json

MAIN_TRACK = {
    "2611.23416": "神经渲染",       # OCLDA-GS 对象中心动态 3DGS 流式
    "2611.23450": "神经渲染",       # NIRJALA 水下三路光学 GS（库内已有 OceanXL 先例）
    "2611.23513": "化身与人体",     # 多视角人体位姿融合（射线横向一致性）
    "2611.23554": "重建与SLAM",     # VGGT 层匹配稀疏注意力加速
    "2611.23575": "触觉与多模态",   # LuxTac 光学 taxel 阵列三轴力
    "2611.23670": "感知与认知",     # EyeDiT 眼动 AR/VR 合成眼数据
    "2611.23736": "神经渲染",       # GaussLearner 持续学习 3DGS
    "2611.23825": "化身与人体",     # VR 对练武术动作学习
    "2611.23871": "触觉与多模态",   # HOForce 单视角 RGB-D 手物交互力重建
    "2611.23935": "重建与SLAM",     # Facet-SLAM 实时三角泼溅 SLAM
    "2611.23939": "交互与输入",     # VR 机器人遥操作 移动/视点控制 2x2 用户研究
    "2611.23970": "化身与人体",     # TOMAS 自我中心手部预测
    "2611.23994": "神经渲染",       # WaveView 噪声相位注入 NVS
    "2611.24207": "触觉与多模态",   # TapTacTouch 稀疏触觉形状补全
    "2611.24334": "交互与输入",     # AI-XR 多模态编程工作区
    "2611.24404": "重建与SLAM",     # RAPID 偏振先验深度 2DGS
    "2611.24565": "重建与SLAM",     # LightHarness 光照推理程序化 3D 重建
    "2611.24616": "感知与认知",     # EgoJev 自我中心视频证据帧选择
    "2611.24731": "评估与数据集",   # HandWorldBench 手中心世界模型基准
    "2611.24805": "系统与平台",     # AR 眼镜端 RAW 压缩+复原
    "2611.24938": "世界模型与仿真", # Phoenix 场景结构表示 world-action
    "2611.24941": "内容生成",       # UltraTex PBR 纹理生成
}
BF_TRACK = {
    "2511.18173": "化身与人体",     # EgoControl 可控自我中心视频生成
    "2606.07179": "神经渲染",       # Lifting 3D Gaussians 小波多分辨率流式
    "2607.08514": "感知与认知",     # 自我中心视频语言模型 hand/object 线索
}
# 第 3.5 步残差复核采纳：被 KW 层丢弃、经逐条通读判定应收录（来源 nonxr_1120）
RESIDUAL_TRACK = {
    "2611.23417": "神经渲染",       # Autoregressive View Model 相机路径视角流
    "2611.23534": "系统与平台",     # Smart Glasses 系统综述 2020-2026
    "2611.24193": "世界模型与仿真", # WM^MLLM 交互式世界模型
}

pool = json.load(open("data/xr_pool_1120.json", encoding="utf-8"))
old = json.load(open("data/old_replace_1120.json", encoding="utf-8"))
nonxr = json.load(open("data/nonxr_1120.json", encoding="utf-8"))

reg = {}
for l in open("papers/library/registry.jsonl", encoding="utf-8"):
    if l.strip():
        d = json.loads(l)
        reg[d["id"].split(":")[-1].split("v")[0]] = d

main, bf = {}, {}
for k, tr in MAIN_TRACK.items():
    r = pool[k]
    assert not r["in_registry"], f"{k} already in registry"
    main[k] = {**r, "track": tr, "batch": "2026-11-20"}
for k, tr in BF_TRACK.items():
    r = old[k]
    assert k not in reg, f"{k} already in registry"
    bf[k] = {**r, "track": tr, "batch": "backfill-1120"}
for k, tr in RESIDUAL_TRACK.items():
    r = nonxr[k]
    assert not r["in_registry"], f"{k} already in registry"
    main[k] = {**r, "track": tr, "batch": "2026-11-20", "recall": "RESIDUAL"}

json.dump(main, open("data/cand_main_1120.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
json.dump(bf, open("data/cand_bf_1120.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("main", len(main), "bf", len(bf))
print("ids:", ",".join(list(main) + list(bf)))
tracks = {}
for v in main.values():
    tracks[v["track"]] = tracks.get(v["track"], 0) + 1
print("tracks:", dict(sorted(tracks.items(), key=lambda kv: -kv[1])))
print("announce:", {a: sum(1 for v in main.values() if v["announce"] == a) for a in {v["announce"] for v in main.values()}})
print("published:", sorted({v["published_rss"] for v in main.values()}))
