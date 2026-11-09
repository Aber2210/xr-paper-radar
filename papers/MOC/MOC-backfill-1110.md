# MOC · backfill-1110（旧稿 v2+ 再公告首次入馆）

> **非当日新提交**：本批 4 篇均为 11-09 公告 RSS 混入的旧稿 v2/v3/v4 再公告（原始投稿 2025-11 ~ 2026-07，2026-11-06 更新），诚实口径单独编号，不参与当日重磅日判定。
> 定稿 2 A / 2 B，最高 **2605.16981 4.00**（长序列循环 3D 重建状态更新门，6 基准长序列 ATE 降 51%）。其余：SFHand 3.85 / 街景视觉定位精度潜力 3.17 / EGOSTREAM 3.04。

## 本批论文（按加权降序）

| # | 论文 | 赛道 | 总分 | 等级 | 证据 | 笔记 |
|---|---|---|---|---|---|---|
| 1 | 重思长序列循环三维重建的状态更新门 | 重建与SLAM | 4.00 | A | FULL | [→](../notes/2605.16981__adaptive-frame-gating-streaming-reconstruction.md) |
| 2 | SFHand：流式第一视角 3D 手部预测的预测式表征学习 | 交互与输入 | 3.85 | A | FULL | [→](../notes/2511.18127__sfhand-streaming-egocentric-hand-forecasting.md) |
| 3 | 高端街景影像视觉定位的精度潜力 | 重建与SLAM | 3.17 | B | FULL | [→](../notes/2607.24409__street-level-imagery-visual-localization-accurac.md) |
| 4 | EGOSTREAM：第一视角流式情景记忆的诊断基准 | 评估与数据集 | 3.04 | B | FULL | [→](../notes/2605.31557__egostream-streaming-episodic-memory-benchmark.md) |

## 批次要点

- **重思长序列循环三维重建的状态更新门**（2605.16981，4.00 A）：诊断出 TTT3R 类 per-token 门控的记忆视界仅约 3 帧，提出免训练、免参数的帧级门 α_t，长 TUM-RGBD 序列 ATE 降 51%，Bonn 深度 AbsRel 降 13.0%。
- **SFHand：流式第一视角 3D 手部预测的预测式表征学习**（2511.18127，3.85 A）：SFHand 以自回归流式架构 + ROI 增强记忆实现语言引导的实时 3D 手部预测，ADE 由 HaMeR+In. 的 18.03 降到 12.65（-30%），33.4 FPS，下游 Franka Kitchen 成功率 79.9%。
- **高端街景影像视觉定位的精度潜力**（2607.24409，3.17 B）：用高分辨率街景影像与自建 FHNW Muttenz 数据集（10 km 路网、真值 6–9 mm / <0.1°），稀疏特征视觉定位在日间可达中位 1–5 cm、0.03–0.1°，接近测绘级 GNSS。
- **EGOSTREAM：第一视角流式情景记忆的诊断基准**（2605.31557，3.04 B）：EgoStream 用 2,250 道题 + Answer Validity Window 扩展成 8,528 次评测，在统一 Qwen3-VL 框架下发现最强流式记忆机制准确率仅约 45%，且全部慢于实时（>1 s/帧）。
