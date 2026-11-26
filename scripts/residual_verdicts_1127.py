# -*- coding: utf-8 -*-
"""2026-11-27 残差复核判定落盘。

525 条 nonxr 全部逐条给判定（verdict=0/1），rate 分母才正确（11-24 教训：
只写少数行会把 rate 抬到 57%）。判 1 = 属于 12 赛道之一但被「摘要级 KW + 标题级扩展词」漏掉。

采纳（进本批候选池，走全文→评分→产物）：见 ADOPT，12 条。
其余 verdict=1 的 18 条只登记不采纳（本批体量已大，留待后续按需挑选），
报告中如实写「疑似漏检 30 条，采纳 12 条」。
"""
import json

# n -> (track, why)  判 1（疑似漏检）
FLAG = {
    # batch_00
    42:  ("化身与人体", "CoSMo 身体运动的紧凑谱空间表示，可编辑/迁移/插值"),
    47:  ("触觉与多模态", "mulsemedia 多感官电视：环境光/振动/气味/风，沉浸式内容消费"),
    62:  ("世界模型与仿真", "DreamTour 单图相机轨迹巡游生成，训练无关的相机控制"),
    73:  ("重建与SLAM", "ArtKit 从 RGB-D 视频重建铰接物体部件与运动学树"),
    88:  ("神经渲染", "FoamSurf 散射介质中表面+介质联合可微渲染"),
    99:  ("内容生成", "钢琴铰固体表示为非流形胞复形并驱动动画"),
    101: ("重建与SLAM", "ArtLang-4D 铰接状态感知的单目 4D 语言场"),
    117: ("化身与人体", "SEEL 端到端 3D 手语生成"),
    131: ("重建与SLAM", "线性时间在线视觉几何 Transformer（VGGT 系流式化）"),
    133: ("重建与SLAM", "Recall4D 前馈 4D 重建长序列误差归因于遗忘"),
    158: ("评估与数据集", "Asset4D-Bench 可编辑 3D/4D 重建基准"),
    160: ("化身与人体", "DualCast 双图条件数字人电商视频生成"),
    # batch_01
    195: ("化身与人体", "谱最优传输的动力学感知手语生成"),
    220: ("内容生成", "LayoutRecall 多轮 3D 布局控制图像编辑的外观保持"),
    247: ("重建与SLAM", "循环式多视角重建的近似位置选择与加速"),
    253: ("重建与SLAM", "Embodied-VGGT 长序列重建的局部几何保持"),
    272: ("化身与人体", "MoSk 统一运动-骨架基础模型"),
    282: ("世界模型与仿真", "SPARC 几何引导注意力剪枝的相机可控长视频生成"),
    283: ("感知与认知", "流式 RGB-D 三维可供性 grounding（何时答/何处指）"),
    287: ("世界模型与仿真", "WorldBridge 稀疏视角拼合为连贯 3D 世界"),
    310: ("重建与SLAM", "图像可检测场作为稀疏地图 2D-3D 定位的视点效用"),
    351: ("神经渲染", "ReMeDi 单图 PBR 材质估计（金属/介电重参数化）"),
    # batch_02
    390: ("评估与数据集", "ProxyGenBench 3D blockout 代理引导视频生成基准"),
    402: ("化身与人体", "AGLR 属性引导的细粒度人体运动生成与编辑"),
    428: ("重建与SLAM", "DuCo 几何基础模型的跨层一致稀疏注意力"),
    452: ("神经渲染", "Neural Rendering Compiler 把生成式视频模型当可编程渲染器"),
    455: ("世界模型与仿真", "ShowNow 细粒度投机流式生成，降低交互世界模型响应延迟"),
    464: ("世界模型与仿真", "WorldInteract 多材质交互的可控流式视频世界模型"),
    481: ("内容生成", "SceneDesigner3D 智能体进化搜索的 3D 室内场景重排"),
    505: ("感知与认知", "跨模态地点识别缩小与视觉地点识别的差距"),
}

# 采纳进本批（12 条，其余 18 条只登记）
ADOPT = {
    "2611.33650": "重建与SLAM",
    "2611.33655": "重建与SLAM",
    "2611.34608": "重建与SLAM",
    "2611.33511": "重建与SLAM",
    "2611.34079": "世界模型与仿真",
    "2611.34730": "世界模型与仿真",
    "2611.34680": "神经渲染",
    "2611.33462": "神经渲染",
    "2611.34022": "化身与人体",
    "2611.33588": "化身与人体",
    "2611.33313": "触觉与多模态",
    "2611.33728": "评估与数据集",
}


def main():
    index = {e["n"]: e["id"] for e in json.load(open("data/residual_1127/index.json", encoding="utf-8"))}
    lines = []
    for n in sorted(index):
        if n in FLAG:
            tr, why = FLAG[n]
            lines.append(json.dumps({"n": n, "verdict": 1, "track": tr, "why": why}, ensure_ascii=False))
        else:
            lines.append(json.dumps({"n": n, "verdict": 0}, ensure_ascii=False))
    open("data/residual_1127/verdicts.jsonl", "w", encoding="utf-8").write("\n".join(lines) + "\n")
    ids = {index[n] for n in FLAG}
    bad = [a for a in ADOPT if a not in ids]
    if bad:
        print("FATAL 采纳项不在判 1 清单:", bad)
        raise SystemExit(2)
    json.dump(ADOPT, open("data/adopt_1127.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print("verdicts 行数:", len(lines), "| 判 1:", len(FLAG), "| 采纳:", len(ADOPT))
    print("未采纳的判 1 条目:", sorted(ids - set(ADOPT)))


if __name__ == "__main__":
    main()
