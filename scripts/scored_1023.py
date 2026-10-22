# -*- coding: utf-8 -*-
# scored_1023.py — 生成 data/scored_1023.json（主批）与 data/scored_backfill_1023.json
# 评分为全文证据定稿（先抓全文再定稿，§8.6.2）；门③ 现算基线 4.416 → 非重磅日无 S。
import json
ROOT = "D:/Agent/WorkBuddy/Research"

MAIN = [
 # id, title_zh, track, IMP,NOV,TEC,EXP,PER,TRL,REP, announce
 ("2610.25988","SSIO：免真值的自监督惯性里程计","重建与SLAM",4,4,4,4,3,4,3,"replace"),
 ("2610.28821","Register Anything：跨域统一点云配准模型","重建与SLAM",3,4,4,4,4,3,4,"new"),
 ("2610.29106","DriftNeRF：跨射线密度漂移的稀疏视图 NeRF","神经渲染",4,4,4,4,3,3,3,"new"),
 ("2610.30032","测量引导的实验室眼动数据向 VR 信号转换（VR 眼动认证）","感知与认知",3,4,4,4,4,3,3,"new"),
 ("2610.29768","UniRAP：统一部件级物理可供性推理与可操作感知","具身交互",3,4,4,4,4,3,3,"new"),
 ("2610.29936","DewHand：第一视角视频的度量世界空间手-相机联合重建","交互与输入",3,4,4,4,4,3,3,"new"),
 ("2610.30013","ClunoGS：统一优化实现紧凑语言 3D 高斯泼溅","神经渲染",3,4,4,4,4,3,3,"new"),
 ("2610.29014","GenXR-Bench：首个 XR 交互开发编程智能体基准","评估与数据集",3,4,4,4,3,3,4,"cross"),
 ("2610.29517","AutoPhyX：文本条件的物理属性自动生成（4D 仿真就绪）","世界模型与仿真",3,4,4,4,3,3,4,"cross"),
 ("2610.07217","RoboCap：250g 六目双 IMU 第一视角数据捕获平台","系统与平台",3,3,4,4,4,4,3,"replace"),
 ("2610.28962","RoPT：闭环鲁棒 6DoF 物体位姿跟踪","感知与认知",3,3,4,4,4,3,3,"new"),
 ("2610.29374","AOV-GS：主动开放词汇语义建图（3DGS）","重建与SLAM",3,3,4,4,3,3,3,"new"),
 ("2610.30089","ProactEgoMem：流式第一视角视频的主动记忆基准","感知与认知",3,4,3,4,3,2,4,"new"),
 ("2610.29647","Reading the Room：稀疏 VSLAM 地图到户型图的尺度模糊语义注册","重建与SLAM",2,3,3,3,3,3,3,"cross"),
 ("2610.29396","渐进式置换对齐与温控频谱锐化（INR 权重空间）","神经渲染",2,3,3,3,3,2,3,"cross"),
]
BF = [
 ("2604.11685","Unfolding 3DGS：迭代高斯概要实现紧凑渐进渲染","神经渲染",3,4,4,4,4,3,3,"replace"),
 ("2608.21009","手背图像用于 XR 沉浸式年龄保障与儿童安全","感知与认知",4,4,3,3,3,3,3,"replace"),
 ("2610.28004","可微任务驱动编码孔径相机设计（3DGS 场景表示）","渲染与显示",3,4,4,3,3,3,3,"leak-1021"),
 ("2610.28585","SceneRig：单图生成仿真就绪 3D 场景的智能体系统","世界模型与仿真",3,4,4,3,3,3,3,"leak-1021"),
 ("2604.10809","WARPED：手腕对齐渲染（第一视角示范→机器人策略）","内容生成",3,3,4,4,3,3,3,"replace"),
 ("2610.27622","单头戴相机标注的无电子 UMI 手套数据采集","系统与平台",3,3,3,4,3,4,3,"leak-1021"),
 ("2610.26918","GTSM：热状态空间动力学高斯泼溅（4D 热场重建与预测）","神经渲染",2,3,4,4,4,2,3,"leak-1021"),
 ("2610.28131","OV-Foam：幂图划分表示下的开放词汇特征提升","神经渲染",3,4,3,3,3,2,3,"leak-1021"),
 ("2607.06464","Hilti-Trimble-Oxford：360° 视觉惯性基准（户型图先验）","评估与数据集",3,2,3,3,3,4,4,"replace"),
]

def dump(rows, batch, window, path):
    pool = []
    for r in rows:
        bid, tzh, track = r[0], r[1], r[2]
        dims = dict(zip(("IMP","NOV","TEC","EXP","PER","TRL","REP"), r[3:10]))
        pool.append(dict(id=bid, title_zh=tzh, track=track, announce=r[10], **dims))
    json.dump({"batch": batch, "orig_window": window, "pool": pool},
              open(f"{ROOT}/{path}", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print(path, len(pool))

dump(MAIN, "2026-10-23",
     "10-22（周四）公告批次（提交日 10-15~10-21、周四 20:00 ET 释放；拉取日 10-23 周五）",
     "data/scored_1023.json")
dump(BF, "backfill-1023",
     "backfill-1023：10-21 公告批次漏网 5 篇（listing 摘要级对账补录）+ 旧稿 replace/cross 再公告 4 篇（首次入馆）；均非 10-23 当日新提交",
     "data/scored_backfill_1023.json")
