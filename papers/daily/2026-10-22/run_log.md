# 2026-10-22 运行日志

- 运行时间：2026-10-22 02:48（周四，拉取日）
- 公告窗口：10-21（周三）公告批次（提交日 10-16~10-20、周三 20:00 ET 释放；拉取日 10-22 周四）
- 数据源：export.arxiv.org / arxiv.org/api/query 探针均 200；RSS cs.CV 287 条 / cs.AI 473 条（最新公告日 2026-10-21）→ RSS 兜底拉取。
- 第 1 步 listing 对账：TARGET_LO=2026-10-20；per-category 完整性自检全过（最终 per-cat SHORT 为跨分类认领统计假象）；摘要级过滤两渠道互证，无漏网、无 backfill。
- 拉取：fetch_rss.py 7 分类去重 795 → KW 命中 48 → 去重后 44 新（27 new + 12 cross + 5 replace）+ 4 库内 v2。
- 全文：21 篇全 L0/FULL；manifest 合并写入校验通过。
- 三关：门① 0.096 通过；门② Top10 覆盖 5 赛道通过；门③ 4.00 < 4.416 非重磅日无 S，未拔高。
- registry：573 -> 573（+0），备份 registry.jsonl.bak-20261022。
- 剔除记录：非 XR 18 篇（LLM 5 / 机器人·人形 6 / UAV 定位 / CoGaussian 自动驾驶协同感知 / 视频时序定位 / 相机设计 / 动物行为 / 人机协作 / LLM 智能体 / dashcam / 机器人仿真 / 工业热场）；replace 旧稿 5 篇均非 XR；库内 v2 再公告 4 篇（SwitchSplat/Stable Signer V3/HumanSkill-4D/Thinker-WM）。
- 失败/降级：无。

