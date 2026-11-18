"""2026-11-19 候选集构建：从 XR 池中人工复核后选定主批 22 篇 + backfill 4 篇，写入 cand 文件。

复核口径：逐篇核摘要，剔除缩写误命中（AR=autoregressive 等）与明确非 XR 的机器人/自驾/医学/遥感稿。
"""
import json

MAIN_TRACK = {
    "2611.21642": "触觉与多模态",
    "2611.21690": "评估与数据集",
    "2611.21802": "系统与平台",
    "2611.21938": "评估与数据集",
    "2611.22095": "神经渲染",
    "2611.22146": "交互与输入",
    "2611.22151": "化身与人体",
    "2611.22164": "化身与人体",
    "2611.22207": "化身与人体",
    "2611.22235": "重建与SLAM",
    "2611.22240": "系统与平台",
    "2611.22415": "感知与认知",
    "2611.22541": "感知与认知",
    "2611.22614": "触觉与多模态",
    "2611.22657": "感知与认知",
    "2611.22742": "感知与认知",
    "2611.22805": "神经渲染",
    "2611.22829": "重建与SLAM",
    "2611.23051": "重建与SLAM",
    "2611.23054": "神经渲染",
    "2611.23187": "重建与SLAM",
    "2611.23209": "感知与认知",
}
BF_TRACK = {
    "2605.22631": "化身与人体",
    "2607.05598": "神经渲染",
    "2606.04493": "重建与SLAM",
    "2610.27275": "重建与SLAM",
}

pool = json.load(open("data/xr_pool_1119.json", encoding="utf-8"))
old = json.load(open("data/old_replace_1119.json", encoding="utf-8"))

main = {}
for k, tr in MAIN_TRACK.items():
    r = pool[k]
    main[k] = {**r, "track": tr, "batch": "2026-11-19"}
bf = {}
for k, tr in BF_TRACK.items():
    r = old[k]
    bf[k] = {**r, "track": tr, "batch": "backfill-1119"}

json.dump(main, open("data/cand_main_1119.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
json.dump(bf, open("data/cand_bf_1119.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("main", len(main), "bf", len(bf))
print("ids:", ",".join(list(main) + list(bf)))
print("tracks:", {t: sum(1 for v in main.values() if v["track"] == t) for t in sorted({v["track"] for v in main.values()})})
print("announce:", {a: sum(1 for v in main.values() if v["announce"] == a) for a in {v["announce"] for v in main.values()}})
