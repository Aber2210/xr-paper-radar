# 2026-10-24 运行日志

- 公告批次：2026-10-23（周五 20:00 ET 释放）；拉取日 2026-10-24（周六 02:30）。
- 数据源：API 双源探针 200（export + arxiv.org）；RSS 200 → 本批以 RSS 为主源（公告日口径），listing 对账补齐 RSS 漏网。
- listing 漏网对账：TARGET_LO=2026-10-22；10-22 组摘要级 XR 命中 9 篇全部为 10-23 运行已甄别剔除的非 XR（ FogTTA/UNIVERS/假肢可供性/AirPlayground/机械臂 NBV/碰撞回避/A2I-Calib++/DiffResearch/EHR），0 漏网；10-23 组摘要级命中 23 篇 = RSS 命中 15 篇 + **RSS 漏网 8 篇**（其中 5 篇 XR 相关入主批：PiHand/VR告别×2 中的 30734 与 30731/VecTile/IMU 定向；3 篇非 XR：31253 医学/30969 操作/30955 辅助机器人）。
- RSS 拉取：7 分类去重 643 条 → 关键词命中 33 → 去 registry(597) 后 31 新；剔库内 v2 再公告 2 + 非 XR 8 + 旧稿 replace 4（XR 相关，入 backfill-1024）= 主批 17 篇。
- 全文抓取：21 候选（17 主批 + 4 backfill）串行 3s/篇，**全部 L0/FULL**（39,907–108,292 字符），无限流/降级/伪造。
- 覆盖度三关：门① 0.109（通过）；门② Top10 7 赛道（通过）；门③ 4.22 < 4.416（现算）→ 非重磅日无 S。
- 落后登记：OUTDATED/SUPERSEDED 0 篇；路线观察 3 条（①免训练/历史回忆替代学习式 3D 分支：RecallGS + Stream4D + MVLoMa 同期收敛于「冻结骨干+后处理/证据复用」范式；②第一视角手部重建双路线：EgoHand 相机感知单目 vs MEgoVista stereo 度量标尺，互补非取代；③社交 VR 实证从「个体沉浸」转向「空间配置与群体动力学」：30353/30731/30734 三篇用户研究同期）。
- registry：597 → 618（主批 17 + backfill 4，幂等追加，备份 registry.jsonl.bak-20261024）。
