# -*- coding: utf-8 -*-
"""构建 data/scored_1119.json：候选元数据 + 全文 digest + 人工定稿结论/标签。"""
import json, re

DATE, RUN = "2026-11-19", "2026-11-19"
BF_BATCH = "backfill-1119"
DIG = json.load(open("data/digest_1119_all.json", encoding="utf-8"))
PUB = json.load(open("data/published_1119.json", encoding="utf-8"))
MAIN = json.load(open("data/cand_main_1119.json", encoding="utf-8"))
BF = json.load(open("data/cand_bf_1119.json", encoding="utf-8"))
MAN = json.load(open("data/fulltext/_manifest.json", encoding="utf-8"))

CONCL = {
    "2611.22095": "冻结 4DGS 主干、按预测可靠性与渲染贡献调度稀疏形变评估，Jetson AGX Orin 上取得 1.75–6.74× 加速，PSNR 仅降 ≤0.16 dB。",
    "2611.22164": "编码 agent 递归改写推理 harness 并按信息源蒸馏回网络，配合十指标无回退门，HOT3D MPJPE-p 12.97→8.37 mm（−35%）、jitter −52%。",
    "2611.22235": "把回环改成 S² 上的 SO(3) 相关并用三 agent 全局 Sim(3) 一致拒绝对称假回环，全景多机 SLAM 单机 ATE 1.610→0.150 m、多机 1.353→0.082 m。",
    "2611.22240": "以同一 Vulkan 数值更新加 256 条设备 schedule，八种跨六厂商 GPU 全部跑完 30k 步标准训练，跨设备 PSNR 差异 <0.07 dB。",
    "2611.22541": "把无中间视觉反馈的多步空间状态推演形式化为 SSP/FSP/DPT 三档基准，SpatialWalker-3B 从 12.54% 提到 46.35%，仍低于人类 74.73%。",
    "2611.22207": "把模板/LBS/渲染的几何对应写进 attention 的 RoPE 与层内 rendering-in-the-loop，68M 参数在 6 视角 NeuMan 上超 609M 的 LHM++ 2.73 dB。",
    "2611.22829": "把 RGB-D 重定位拆成 place-finding 与 pose-refinement，55.7K 参数在 ScanNet-96 达 81.4%，82 ms/帧，比 BUFFER-X 快约 18 倍。",
    "2611.22146": "手戴平行夹爪 + Quest/PICO 追踪的无机器人双臂采集，562 条演示训练 ACT 折毛巾成功 12/20，硬件软件 Apache-2.0 开源。",
    "2611.22415": "任务条件化的多层级几何门控注入 MLLM，VSI-Bench 5B 71.5 / 10B 72.3，均居同规模第一。",
    "2611.22657": "以投射阴影为物理读数构建 T1/T2/T3 三向推理基准，GRPO 使 Qwen3-VL-8B 从 24.40% 升到 38.73%。",
    "2611.23051": "把几何引导精化从 3D 点 patch 搬到图像网格的 per-view depth，ScanNet++ AUC@1cm 25.6→33.7（对 GGPT 基线）。",
    "2611.23187": "以共享 3D 空间查询 + 完整表面占用监督统一点云补全与影像生成，low-poly F-score 80.14→94.27。",
    "2611.22805": "时空块外存训练 + 4D Morton 重排 + 可学习 point splatting，DynamicMatrixCity 上较 Dynamic TideGS +9.2~13.9 dB、训练时间 −28~46%。",
    "2611.23054": "免渲染的 3DGS 美学调色：解析一阶更新 + 44.7K 参数残差网络，ΔE76 5.50 优于 BilaRF 6.30，耗时 23 s 对 123 s。",
    "2611.21690": "ACM MM 2026 第一人称社会推理与工具交互挑战赛总结：4,030 题 / 1,055 段视频，Track 2 最佳 joint 0.844。",
    "2611.21938": "10,124 小时 / 72,754 episodes 的野外第一人称技能工作视频，12,227 名贡献者、15,548 个环境，附逐帧 IMU，但尚无策略实验。",
    "2611.22742": "把高斯基元的各向异性 support 写进 Mamba 序列构造，nuScenes-SurroundOcc IoU 29.83→32.41，代价是推理延迟 +31%。",
    "2611.21802": "在冻结自编码器 latent 上训练前缀可解 hyper-autoencoder，实现逐形状可变码率的三维压缩；结论全以 R-D 曲线呈现，无量化表。",
    "2611.22614": "100 美元级振动触觉像素阵列 + load-decoupling 帽，9 人识别 7 类图形准确率 44–89%，盲人识别速度约为蒙眼明眼人的 3 倍。",
    "2611.22151": "21.9K 参数受控探针：手部运动仅把两秒手腕 FDE 从 60.26 降到 56.48 mm，长距离伸手严重欠估（记录 147 mm vs 预测 22 mm）。",
    "2611.21642": "指尖振动把图像特征编码为随移动变化的触觉，n=20 下单指主观清晰度最高（5.48/7），但无客观解读性能指标。",
    "2605.22631": "把稀疏三点头手跟踪改写为掩码全身观测建模，AMASS-P1 MPJPE 2.95 cm 优于 HMD-Poser 3.15 cm，消融增益落在噪声内。",
    "2607.05598": "区分屏幕空间伪影与世界空间瞬态，无监督联合分解 scene/overlay，合成 Mip-NeRF 360 平均 +2.9 dB、Dashboard 类最高 +7.5 dB。",
    "2606.04493": "用 cluster 诱导顺序 + 可学习复值低通门让 Mamba 扫描获得频率含义，YFCC100M mAP@5° 73.83%，超 MatchMamba 3.6 点。",
    "2610.27275": "证明最大团与最大一致集在点云配准中可任意分离，给出 d+1/d+2 最小充分 group 阶数与 0.18 ms 的 anchor certificate。",
}
TAGS = {
    "2611.22095": ["4DGS / 动态高斯", "边缘设备", "形变调度", "Jetson"],
    "2611.22164": ["手部姿态", "第一人称", "自改进", "HOT3D"],
    "2611.22235": ["全景 SLAM", "多智能体", "高斯泼溅", "回环检测"],
    "2611.22240": ["3DGS 训练", "Vulkan", "移动端", "跨平台"],
    "2611.22541": ["空间推理", "MLLM", "动态模拟", "基准"],
    "2611.22207": ["化身重建", "前馈", "模板锚定", "渲染引导"],
    "2611.22829": ["重定位", "点云配准", "RGB-D", "建筑尺度"],
    "2611.22146": ["数据采集", "具身", "手戴接口", "VR 控制器"],
    "2611.22415": ["空间推理", "几何融合", "MLLM", "门控"],
    "2611.22657": ["空间推理", "投射阴影", "基准", "GRPO"],
    "2611.23051": ["三维重建", "前馈", "SfM", "深度精化"],
    "2611.23187": ["建筑重建", "点云", "LoD2", "多模态"],
    "2611.22805": ["3DGS", "外存训练", "城市级", "动态场景"],
    "2611.23054": ["3DGS 编辑", "颜色迁移", "美学增强", "轻量化"],
    "2611.21690": ["第一人称", "基准", "社会推理", "工具调用"],
    "2611.21938": ["第一人称数据集", "具身", "技能工作", "IMU"],
    "2611.22742": ["3DGS", "占据预测", "Mamba", "自动驾驶"],
    "2611.21802": ["3D 压缩", "变长编码", "网格", "SDF"],
    "2611.22614": ["触觉显示", "无障碍", "振动", "低分辨率"],
    "2611.22151": ["第一人称", "手部轨迹", "世界模型", "负结果"],
    "2611.21642": ["触觉反馈", "指尖", "图像解读", "用户研究"],
    "2605.22631": ["全身动捕", "VR 化身", "稀疏跟踪", "掩码建模"],
    "2607.05598": ["3DGS", "伪影去除", "无监督", "鲁棒重建"],
    "2606.04493": ["对应学习", "Mamba", "频域", "SfM 前端"],
    "2610.27275": ["点云配准", "最大团", "一致性", "理论"],
}
W = dict(IMP=.20, NOV=.20, TEC=.15, EXP=.15, PER=.15, TRL=.08, REP=.07)


def slug(t):
    s = re.sub(r"[^a-z0-9]+", "-", t.lower()).strip("-")
    return "-".join(s.split("-")[:7])


out = []
for src, batch in ((MAIN, DATE), (BF, BF_BATCH)):
    for pid, c in src.items():
        d = DIG[pid]
        p = PUB[pid]
        sc = d["scores_hint"]
        val = round(sum(W[k] * sc[k] for k in W), 2)
        ev = MAN[pid]
        out.append({
            "id": pid,
            "batch": batch,
            "title": d["title_en"],
            "title_zh": d["title_zh"],
            "slug": slug(d["title_en"]),
            "track": c["track"],
            "venue": d["venue"],
            "tags": TAGS[pid],
            "scores": sc,
            "value": val,
            "evidence": ev["evidence"],
            "level": ev["level"],
            "chars": ev["chars"],
            "published": p["published"],
            "updated": p["updated"],
            "primary_cat": p["cat"],
            "conclusion": CONCL[pid],
            "problem": d["problem"],
            "method": d["method"],
            "experiments": d["key_results"],
            "novelty": d["novelty"],
            "limitations": d["limitations"],
            "code": d["code"],
            "announce": "replace" if batch.startswith("backfill") else c["announce"],
            "status": "CURRENT",
        })
out.sort(key=lambda r: (r["batch"] != DATE, -r["value"], -r["scores"]["IMP"], -r["scores"]["NOV"], r["id"]))
json.dump(out, open("data/scored_1119.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("wrote", len(out), "main", sum(1 for r in out if r["batch"] == DATE), "bf", sum(1 for r in out if r["batch"] == BF_BATCH))
for r in out:
    print(f"{r['batch'][:9]:9s} {r['id']} {r['value']:.2f} {r['track']:8s} {r['title'][:58]}")
