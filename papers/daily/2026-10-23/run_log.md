# 2026-10-23 运行日志

- 运行时间：2026-10-23 02:44（周五，拉取日）
- 公告窗口：10-22（周四）公告批次；拉取日 10-23。
- 数据源：export.arxiv.org / arxiv.org/api/query 探针均 200，submittedDate 前沿停滞 10-21；RSS cs.CV 212 条（公告日 10-22）→ RSS 兜底。
- 第 1 步 listing 对账（audit_gap_listing.py，TARGET_LO=2026-10-21）：10-21 组 532 篇 + 10-22 组 402 篇；per-category 完整性自检 attempt1 全过（最终 per-cat SHORT 为跨分类认领统计假象）；摘要级过滤（filter_missed_xr_abstract_1021.py，914 篇池）10-22 组 22 篇全在 RSS 集合（0 漏网）；10-21 组 19 篇中 5 篇 XR 相关漏网 → backfill-1023。
- 拉取：fetch_rss.py 7 分类去重 649 → KW 命中 33 → 去重后 31 新（20 new + 5 cross + 6 replace）+ 2 库内 v2。
- 全文：15 主批候选全 L0/FULL；backfill 9 篇中 8 篇 L0/FULL + 1 篇 L1 PARTIAL（2610.28131 OV-Foam：ar5iv 仅返回 abs 页壳、正文不完整，按摘要级评估并显式声明）。
- 三关：门① 0.071 通过；门② Top10 覆盖 8 赛道通过；门③ 3.78 < 4.416（现算）非重磅日无 S，未拔高。
- registry：573 → 588（主批 +15）→ 597（backfill +9），备份 registry.jsonl.bak-20261023。
- 剔除记录：非 XR 10 篇（UNIVERS 医学体积/FogTTA 雾天/AirPlayground 无人机/DiffResearch LLM/EHR 扩散/A2I-Calib++ IMU 标定/碰撞回避 RL/机械臂 NBV/假肢可供性）；replace 旧稿非 XR 2 篇（2610.24858 MRI 超分/2602.01860 无人机竞速）；库内 v2 再公告 2 篇。
- 失败/降级：OV-Foam（2610.28131）L1 ar5iv 正文缺失 → PARTIAL 摘要级；其余无降级。

