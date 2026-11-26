# -*- coding: utf-8 -*-
"""2026-11-27 人工定稿：对 92 篇 KW/标题级命中逐篇核摘要，剔除误命中，输出最终 XR 候选池。

判定口径（沿用历史批次）：论文主体的贡献/评估对象须落在 12 赛道内，或明确面向 AR/VR/MR/XR 场景。
纯机器人操作 / 自动驾驶 / 遥感测绘 / 医学影像 / 通用 LLM 推理 / 通用 2D 视觉，一律剔除——
即便标题含 spatial / depth / tracking / hand / mesh 等扩展词。

INCLUDE: id -> track
REJECT:  id -> 剔除理由
"""
import json, sys

INCLUDE = {
    # 重建与 SLAM
    "2611.33382": "重建与SLAM",   # 铰接物体分部件水密网格
    "2611.33387": "重建与SLAM",   # 3D 物体关系驱动的多视频同步
    "2611.33824": "重建与SLAM",   # 单目手持物体扫描数据集 + 位姿 + 表面重建（AR 数字化）
    "2611.34108": "重建与SLAM",   # 可检测性驱动的 3D 关键点/显著场（定位地图）
    "2611.34128": "重建与SLAM",   # 无位姿输入的 ray-based 连续表面重建
    "2611.34155": "重建与SLAM",   # 稀疏视角水下 3DGS 重建
    "2611.34480": "重建与SLAM",   # 前馈几何 + VIO 锚点的度量升级（超越 Sim(3)）
    "2611.34549": "重建与SLAM",   # 协作式高斯 SLAM（手机端）
    "2611.34931": "重建与SLAM",   # 单目 4D 重建 + 刚性运动分解
    "2611.34932": "重建与SLAM",   # 3DGS 参考图的机器人重定位
    "2611.34939": "重建与SLAM",   # 动态场景逐帧网格重建（MEMO）
    # 神经渲染
    "2611.33374": "神经渲染",     # VersionGS 动态高斯
    "2611.33698": "神经渲染",     # 3DGS 二阶优化
    "2611.33796": "神经渲染",     # SprintGS 训练加速
    "2611.34062": "神经渲染",     # 表面化场景风格化（AR/VR 内容）
    "2611.34223": "神经渲染",     # AnyCam4D 任意相机 4D 高斯
    "2611.34226": "神经渲染",     # LiveRelight 室内 GI 编辑
    "2611.34476": "神经渲染",     # 密集视角上下文 NVS 压缩
    # 化身与人体
    "2611.33465": "化身与人体",   # 数字手语者高斯化身
    "2611.33819": "化身与人体",   # 文本驱动动作生成
    "2611.33826": "化身与人体",   # MotionODE 连续深度动作后训练
    "2611.34005": "化身与人体",   # 世界坐标人体网格恢复的时变尺度
    "2611.34027": "化身与人体",   # 手部动作补全
    "2611.34940": "化身与人体",   # LuxAvatar 可重光照头部化身
    # 感知与认知
    "2611.33565": "感知与认知",   # 第一视角视频 + 主动声学
    "2611.33760": "感知与认知",   # 可穿戴视角 GUI grounding
    "2611.34224": "感知与认知",   # 第一视角 + 腕部 sEMG 手部物理状态
    "2611.34347": "感知与认知",   # 第一视角流式社会具身智能基准
    "2611.34466": "感知与认知",   # AI 眼镜第一视角 computer-use 基准
    "2611.34489": "感知与认知",   # 跨视角相机佩戴者识别
    # 世界模型与仿真
    "2611.33467": "世界模型与仿真",  # 高斯世界动作模型
    "2611.33591": "世界模型与仿真",  # VivaWorld 长时程视频世界模型
    "2611.33779": "世界模型与仿真",  # DuoWM 双 6-DoF 视觉流无人机世界模型
    "2611.34810": "世界模型与仿真",  # WorldExpand 全景观 3D 世界扩展
    # 内容生成
    "2611.34141": "内容生成",     # Spe3DUp 快速图生 3D
    "2611.34319": "内容生成",     # PostMesh 艺术网格后训练
    "2611.34414": "内容生成",     # SemProxy 语义 3D 代理
    "2611.34461": "内容生成",     # SceneDesigner++ 9-DoF 位姿控制
    "2611.34944": "内容生成",     # AnyCam 相机可控视频生成
    # 交互与输入
    "2611.33581": "交互与输入",   # 行人-AV 双向 AR 交互
    "2611.33731": "交互与输入",   # RoboJackVR：VR 游戏采集机器人演示
    "2611.34945": "交互与输入",   # MidasTUI 可穿戴显示器的实体化 UI
    # 系统与平台
    "2611.33735": "系统与平台",   # AI 眼镜云边端协同
}

REJECT = {
    # 库内已收录（batch 2026-11-25，value 3.71），本次为 cross 再公告，按「库内 v2/再公告不重复入馆」剔除
    "2611.30173": "库内已收录（2026-11-25 批 3.71），cross 再公告不重复入馆",
    "2611.28905": "多重免疫荧光组织 3D 重建（病理学）",
    "2611.33303": "LLM 逻辑推理难度校准",
    "2611.33352": "机械臂操作中的深度传感器失效分析",
    "2611.33380": "机器人轨迹优化（3DGS 仅作碰撞场）",
    "2611.33390": "机器人空间约束操作谜题",
    "2611.33428": "语言模型部分覆盖问答评测",
    "2611.33460": "肌骨模型全身动作跟踪（生物力学）",
    "2611.33498": "被动 SPAD 成像仿真（通用低光感知）",
    "2611.33567": "隐式神经表示优化器（通用 INR）",
    "2611.33579": "人手演示转机器人数据",
    "2611.33705": "实验室设备仿真资产生成",
    "2611.33761": "自回归图像生成解码加速（AR=autoregressive 误命中）",
    "2611.33792": "空间转录组学预测（计算病理）",
    "2611.33865": "视觉语言导航机器人接力",
    "2611.33905": "航空 TDOM 正射影像生成（遥感测绘）",
    "2611.33918": "莫比乌斯带弦艺术生成（计算艺术）",
    "2611.33919": "自回归转扩散语言模型（AR=autoregressive 误命中）",
    "2611.33920": "超声 B 模式高斯泼溅（医学成像）",
    "2611.33934": "无人机 360° 目标跟踪",
    "2611.33990": "地理空间基础模型评测框架",
    "2611.33991": "动态空间智能运动学基准（机器人/具身）",
    "2611.34021": "跨模态单应估计（通用 2D 几何）",
    "2611.34046": "四旋翼图像目标导航",
    "2611.34053": "LiDAR 里程计因子压缩（激光雷达）",
    "2611.34084": "边缘设备通用视觉跟踪",
    "2611.34126": "视频 LLM 部分证据作答基准",
    "2611.34133": "声乐教学中的内感受 HCI",
    "2611.34240": "地理空间时序基准",
    "2611.34257": "相机运动驱动的机器人操作学习",
    "2611.34298": "双曲表示随机投影（通用 ML）",
    "2611.34330": "空间化电影推荐（推荐系统）",
    "2611.34370": "单目 3D 框提升与跟踪（自动驾驶风格）",
    "2611.34393": "单目深度模型失效解释审计",
    "2611.34428": "神经肌骨模型标定",
    "2611.34453": "4D 毫米波雷达重定位",
    "2611.34478": "医学体数据交互渲染（CT/MR）",
    "2611.34569": "人形机器人弹性地形 sim-to-real",
    "2611.34586": "机器人几何加速度避障",
    "2611.34607": "荧光显微 PSF 估计",
    "2611.34658": "生成式驾驶规划",
    "2611.34670": "机器人触诊弹性成像",
    "2611.34750": "LLM 智能体机械臂关键位姿",
    "2611.34862": "单目 3D/2D 物体 grounding 基准（通用 VLM）",
    "2611.34894": "可形变物体材质估计 sim-to-real",
    "2611.34914": "VLA 物体级轨迹先验（机器人）",
    "2611.34925": "海洋机器人仿真套件",
    "2611.34936": "手-物位姿链驱动灵巧操作（机器人）",
    "2611.34943": "VLM 智能体点跟踪（通用视频对应）",
}

# backfill：旧稿 replace 再公告，人工定稿
BACKFILL_INCLUDE = {
    "2509.16476": "交互与输入",   # GazeVLM 注视引导 foveated 推理
    "2602.00671": "神经渲染",     # HPC 流式动态高斯分层点表示
    "2605.05876": "神经渲染",     # 3DSS 表面泼溅逆渲染
    "2605.16582": "重建与SLAM",   # ArtMesh 铰接网格场
    "2606.11390": "系统与平台",   # 多 GPU 大规模 3DGS 后端
    "2608.29269": "神经渲染",     # LightFuse 可重光照交互重建
    "2611.26380": "感知与认知",   # EgoCaptioner 第一视角视频描述
    "2611.31822": "世界模型与仿真",  # G0.7 长上下文世界动作模型
}
BACKFILL_REJECT = {
    "2405.09707": "解剖形状模型（医学）",
    "2511.22991": "自回归视觉模型频谱引导（AR=autoregressive）",
    "2603.14449": "语音智能体响应时机",
    "2605.15923": "点云尺度/密度不变表示（通用）",
    "2606.31521": "扩散 MRI 畸变校正（医学）",
    "2607.19355": "LLM 信息辨别",
    "2607.19986": "双目匹配光流（通用 2D）",
    "2608.08672": "3-流形体积参数化（几何理论）",
    "2608.18948": "人类视频转机器人训练数据",
    "2609.13259": "虚拟试穿 RL 奖励（知觉一致性）",
    "2610.05664": "视觉语言导航（机器人）",
    "2610.09335": "无人机世界模型目标搜索",
    "2610.25400": "LiDAR 辅助 RGB 语义分割",
    "2610.29866": "3D 场景记忆 VLA（机器人）",
    "2611.22006": "AI 辅助社交媒体分析 HCI",
    "2611.22450": "医学影像标注工具",
    "2611.26405": "触觉接触动力学 VLA（机器人）",
    "2611.32185": "视频驱动铰接物体操作智能体",
}


def main():
    pool = json.load(open("data/xr_pool_1127.json", encoding="utf-8"))
    old = json.load(open("data/old_replace_1127.json", encoding="utf-8"))
    nonxr = json.load(open("data/nonxr_1127.json", encoding="utf-8"))

    missing_in = [p for p in INCLUDE if p not in pool]
    missing_re = [p for p in REJECT if p not in pool]
    uncovered = [p for p in pool if p not in INCLUDE and p not in REJECT]
    if missing_in or missing_re or uncovered:
        print("FATAL 定稿表与候选池不一致")
        print(" include 不在池:", missing_in)
        print(" reject  不在池:", missing_re)
        print(" 池中未判定:", uncovered)
        sys.exit(2)

    final = {}
    for p, tr in INCLUDE.items():
        rec = dict(pool[p])
        rec["track"] = tr
        rec["decided"] = "XR"
        final[p] = rec
    for p, why in REJECT.items():
        rec = dict(pool[p])
        rec["decided"] = "NONXR"
        rec["why"] = why
        nonxr[p] = rec

    bf = {}
    for p, tr in BACKFILL_INCLUDE.items():
        if p not in old:
            print("FATAL backfill include 不在池:", p)
            sys.exit(2)
        rec = dict(old[p])
        rec["track"] = tr
        bf[p] = rec
    for p, why in BACKFILL_REJECT.items():
        if p not in old:
            print("FATAL backfill reject 不在池:", p)
            sys.exit(2)

    json.dump(final, open("data/xr_final_1127.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    json.dump(bf, open("data/backfill_pool_1127.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    json.dump(nonxr, open("data/nonxr_1127.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)

    from collections import Counter
    print("主批 XR:", len(final), dict(Counter(v["track"] for v in final.values())))
    print("backfill:", len(bf), dict(Counter(v["track"] for v in bf.values())))
    print("非 XR 剔除累计:", len(nonxr), "（池内剔除", len(REJECT), "+ KW 未命中", len(nonxr) - len(REJECT), "）")
    ids = sorted(final) + sorted(bf)
    open("data/_ids_main_1127.txt", "w").write("\n".join(sorted(final)) + "\n")
    open("data/_ids_back_1127.txt", "w").write("\n".join(sorted(bf)) + "\n")
    print("ids files written:", len(final), len(bf))


if __name__ == "__main__":
    main()
