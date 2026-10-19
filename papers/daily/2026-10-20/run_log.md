# 执行日志 · 2026-10-20

## 数据源与对账（第 1-3 步）
- 漏网对账（第 1 步）：listing 7 分类最新公告日 = **2026-10-19（周一）**（10-17/10-18 周末无公告）；TARGET_LO=2026-10-16，重审 10-16 + 审计 10-19。
- listing 对账：7 分类 10-19 日组共 373 篇（去重后）全部入账；10-16 日组 519 篇中 501 篇不在库。完整性校验：逐分类自检全部通过（最终 per-cat SHORT 为跨分类交叉列表认领的统计假象，非真实缺口）。
- 脚本修复（本次）：audit_gap_listing.py ① 停止逻辑由「见任一旧日头即停」改为「本页最旧条目早于窗口下界才停」（页内多日头会提前中断翻页）；② 新增按日完整性驱动的逐页截断重试（服务端/代理间歇返回不完整页面）。
- 过滤器升级（落实 10-19 教训）：fetch_rss.py 新增 ABBREV 缩写层（VR/AR/MR/XR/HMD/OST/SLAM/VIO/IMU/DoF/FOV/JND/IPD/VAC/MTF/CGH 词边界正则）；新增 scripts/filter_missed_xr_abstract.py 对 874 篇漏网全集走 API 摘要级过滤（RSS cs.AI 频道为真空源，listing 标题级过滤覆盖不足，摘要级为必需下层）。
- 探针：export.arxiv.org/api/query 200；arxiv.org/api/query 200；rss.arxiv.org 200（cs.CV 201 条；**cs.AI 频道 0 条真空源**，其主分类论文靠 listing+API 摘要级过滤补回）。
- 拉取：fetch_rss.py 7 分类去重 352 条 → 关键词命中 35 条 → 去 registry(492) 后 33 新 = **18 篇 2610.* 真新提交** + 14 篇旧稿 replace/cross（另 2 篇库内 v2 再公告剔除）。
- 甄别：18 篇真新中 **12 篇 XR 核心/强相关**入评分池，7 篇非 XR 剔除（自动驾驶/医学×3/声纳/机器人/X 射线/推荐系统）。
- listing×RSS 交叉验证：listing 摘要级 XR 命中 19 篇（10-19）中 18 篇与 RSS 交集一致、1 篇（2610.22400）甄别为非 XR → 两渠道互证无遗漏。

## backfill 发现
- **10-16 公告日漏网 1 篇**：2610.21297 GeoPano（10-15 提交、10-16 公告）——10-17 运行标题级过滤未命中（摘要才提 AR/VR），本次摘要级过滤补获，属真实漏网。
- **RSS 旧稿 replace/cross 再公告 15 篇**中 7 篇 XR 相关首次入馆（SAGE/OMEGA-Avatar/PanoAir/HyVGGT-VO/CodecSplat/PinNet/EgoTac），8 篇非 XR 剔除；全部单列 backfill-1020，未混入当日新论文。

## 全文抓取
- 20 篇候选（12 主批次 + 8 backfill）跑 fetch_fulltext.py：**全部 L0/FULL**（45,271–118,689 字符），串行 3s/篇，无限流/降级/伪造；manifest 合并写入校验通过。

## 覆盖度三关
- 门①：max Jaccard 0.089（2610.22878 vs 库内 2610.21386）< 0.62 → 通过，无同质、未触发重筛。
- 门②：Top10 覆盖 8 赛道 ≥5 → 通过（全批 12 篇覆盖 9 赛道）。
- 门③：当日最高 4.57 vs 库内近 30 天 Top10 均分 4.359（现算）→ **重磅日（差值 +0.211 ≥ 0.05），S 级成立，未拔高**。注意：09-16/09-17 公告的 DELUGE 4.65/RawSLAM 4.50/AMB3R-SLAM 4.50 因注册日期早于 30 天窗口下界（2026-09-20）不入均分计算，勿用手算旧值。

## 落后登记
- 论文级 OUTDATED/SUPERSEDED：0 篇（门①通过且无同质）。
- 路线观察：① VDA 代表「视频扩散先验直接充当化身」路线，与库内 3DGS/3DMM 化身族（OMEGA-Avatar/LAM/GAGAvatar 等）构成范式竞争，非取代；② dGS 延续库内 N-DGS/UBS 的 N 维泼剪效率线；③ FLoTS-SLAM 与库内动态 SLAM（DynaSLAM 族/WildGS-SLAM）互补（运动不确定性新来源）；④ SAGE 与库内 VGGT-BC/STream3R/SMoRe 构成 GFM 数据扩展线。

## 环境
- C: 盘余 10.8 GB（可用）；D: 盘余 417 GB 健康。