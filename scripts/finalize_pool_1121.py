"""2026-11-21 逐篇人工判读落盘：从 77 篇 KW/标题候选中定稿 XR 池与剔除清单。"""
import json

xr = json.load(open("data/xr_pool_1121.json", encoding="utf-8"))

KEEP = {
    "2611.24995": "评估与数据集",   # EgoPass-Bench, Ray-Ban Meta 眼镜
    "2611.25005": "世界模型与仿真",  # Inhabitant, 长时人-场景交互生成
    "2611.25061": "重建与SLAM",     # Infer3D
    "2611.25279": "重建与SLAM",     # Accord VIO+密集建图
    "2611.25338": "神经渲染",       # VideoRNG 可重光照 GS
    "2611.25340": "重建与SLAM",     # SceneAnything
    "2611.25414": "重建与SLAM",     # MODL 水密网格
    "2611.25444": "化身与人体",      # VisualTalk-Bench 化身讲解
    "2611.25445": "重建与SLAM",     # 立体 VO + GFM
    "2611.25500": "世界模型与仿真",  # PRIO 交互 4D 物体
    "2611.25523": "神经渲染",       # MergeableRF 重光照
    "2611.25567": "感知与认知",      # 在线错误检测（第一人称）
    "2611.25608": "系统与平台",      # MetaScanner 社交 VR 攻击
    "2611.25849": "评估与数据集",   # EgoWitness 实例级空间记忆
    "2611.25865": "感知与认知",      # ProSpace 流式空间推理
    "2611.25925": "空间计算与UI",   # SpatialMem 定量空间推理
    "2611.25934": "神经渲染",       # AGSR GS 超分
    "2611.25950": "渲染与显示",     # GaussTrans 多层透明传输
    "2611.25963": "世界模型与仿真",  # MorphTwin 可形变物理孪生
    "2611.25979": "内容生成",       # GS-VTON 3D 试衣
    "2611.26045": "神经渲染",       # PaveSplat 前馈 GS
    "2611.26072": "重建与SLAM",     # DfD-GS 散焦度量深度
    "2611.26165": "内容生成",       # StreamEgo Exo2Ego
    "2611.26177": "评估与数据集",   # SpatialScout-V2 主动建图基准
    "2611.26321": "重建与SLAM",     # FirstCross 单光子重建
    "2611.26350": "系统与平台",     # PUPPET VR 遥操作
    "2611.26431": "渲染与显示",     # FFGaussType 字形高斯资产
    "2611.26485": "触觉与多模态",    # ROS2 手术遥操作力反馈
    "2611.26493": "重建与SLAM",     # SGAR 稀疏几何注意力
    "2611.26511": "内容生成",       # Direct3D-V3 体素扩散
    "2611.26516": "世界模型与仿真",  # Plan4D 可规划 4D 世界
    "2611.26540": "化身与人体",      # AURA 流式说话人视频
    "2611.26603": "感知与认知",      # Depth Pro 2 度量单目深度
    "2611.26625": "重建与SLAM",     # AnyVIO 前馈 VIO
}

REJECT_WHY = {
    "2611.25082": "赛博物理系统数字孪生框架，非 XR 显示/交互",
    "2611.25113": "立体匹配形状先验诊断，纯几何视觉，无 XR 场景",
    "2611.25282": "点云-图像预训练表征，通用 3D 视觉",
    "2611.25283": "体育视频多目标跟踪重识别",
    "2611.25294": "在线学习眼动可用性研究，非 XR 设备",
    "2611.25366": "移动操作策略学习",
    "2611.25377": "视频检索浏览器插件，非沉浸式",
    "2611.25417": "透明物体抓取深度补全（机器人）",
    "2611.25453": "多模态图像融合",
    "2611.25460": "VLA/WAM 训练框架（具身基础设施）",
    "2611.25513": "类别级 6D 位姿（工业分拣向）",
    "2611.25683": "视触觉 VLA 灵巧操作策略",
    "2611.25703": "LLM 地理空间泛化",
    "2611.25722": "3D 视觉定位智能体（工具链编排）",
    "2611.25730": "自闭症刻板动作检测",
    "2611.25771": "驾驶员注视目标识别",
    "2611.25819": "机器人料箱抓取 6D 位姿",
    "2611.25854": "AUV DVL 约束定位",
    "2611.25866": "空中主动地理定位",
    "2611.25873": "路面要素建图数据集",
    "2611.25884": "海事地理空间分析工作流",
    "2611.25904": "多相机刚体跟踪（旧稿 cross）",
    "2611.26035": "路侧 LiDAR 仿真到真实检测",
    "2611.26048": "无人机主动采集重建（航空测绘向）",
    "2611.26065": "航天器位姿保形预测",
    "2611.26083": "毫米波雷达/事件相机标定",
    "2611.26090": "人机角色分配",
    "2611.26111": "MR 弹性成像（医学）",
    "2611.26120": "第一人称视频检索组合性诊断",
    "2611.26127": "多机器人轨迹扩散规划",
    "2611.26128": "冷冻电镜高斯重建（科学成像）",
    "2611.26146": "Unitree GO1 数据采集工具",
    "2611.26161": "VLA 空间泛化策略",
    "2611.26269": "装配/拆解过程目标跟踪",
    "2611.26276": "多机器人 LiDAR 配准",
    "2611.26380": "第一人称视频描述生成",
    "2611.26405": "触觉创新项 VLA 策略",
    "2611.26407": "非高斯源流匹配理论",
    "2611.26420": "人形机器人全身经验数据",
    "2611.26434": "第一人称操作意图数据集（机器人学习向）",
    "2611.26519": "具身智能体执行推理 VLM",
    "2611.26525": "智能体安全事件回溯",
    "2611.26569": "图像编辑安全基准",
}

final, rejected = {}, {}
for p, v in xr.items():
    if p in KEEP:
        v2 = dict(v)
        v2["track"] = KEEP[p]
        final[p] = v2
    else:
        rejected[p] = {"title": v["title"], "cat": v["cat"], "why": REJECT_WHY.get(p, "非 XR（通用视觉/机器人/医学等）")}

assert len(final) + len(rejected) == len(xr), (len(final), len(rejected), len(xr))
assert all(p in KEEP for p in final)
json.dump(final, open("data/xr_pool_1121.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
json.dump(rejected, open("data/rejected_1121.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)

# backfill 候选定稿
old = json.load(open("data/old_replace_1121.json", encoding="utf-8"))
BF = {"2405.15125": "渲染与显示", "2610.09195": "化身与人体"}
bf = {}
for p, tr in BF.items():
    if p in old:
        v = dict(old[p]); v["track"] = tr; bf[p] = v
json.dump(bf, open("data/backfill_pool_1121.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)

from collections import Counter
print("XR 池", len(final), "剔除", len(rejected), "backfill", len(bf))
print("赛道:", dict(Counter(v["track"] for v in final.values())))
print("backfill:", list(bf))
