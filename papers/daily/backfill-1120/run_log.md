# backfill-1120 执行日志

- **来源**：11-19 公告批次 RSS 全量 753 条中 replace 类 19 篇 XR 命中（`data/old_replace_1120.json`），逐篇核摘要取 **3 篇**。
- **诚实口径**：全部为 **v2 再公告**（API updated 2026-11-17~11-18），原始投稿 2025-11-22 / 2026-06-05 / 2026-07-09；均非 11-19 当日新提交，单独编号、不参与当日重磅日判定。
- **全文**：3 篇全部 FULL。2606.07179 的 arXiv HTML v2 为 1,578 字符空壳，改用 ar5iv 抓取 56,366 字符（L1/FULL）。
- **定稿 0 S / 2 A / 1 B / 0 C（无 S）**：2606.07179 EvoGS：用演化树构建连续分层高斯 **4.05** · 2511.18173 EgoControl：基于 3D 全 **3.77** · 2607.08514 自我中心视频语言模型是否同时捕捉了手 **3.45**
- **标题不一致**：2606.07179 的 arXiv 元数据标题为 *Lifting 3D Gaussians: A Wavelet Multiresolution Representation for Scalable Gaussian Splatting Streaming*，正文（v2 / ar5iv）标题为 *EvoGS: Constructing Continuous-Layered Gaussian Splatting with Evolution Tree for Scalable 3D Streaming*，疑为 v2 改题；registry 采用元数据标题。
- **registry**：+3（batch=backfill-1120，按 base_id 幂等）。
