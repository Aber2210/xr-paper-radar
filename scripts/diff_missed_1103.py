"""逐篇比对 11-03 复采的 10-30 组未入馆集合 vs 11-02 运行的集合，验证复采一致性。"""
import json

cur = json.load(open("data/missed_listing_1103.json", encoding="utf-8"))
prev = json.load(open("data/missed_listing_1102.json", encoding="utf-8"))
print("11-03 recollect:", len(cur), " 11-02 collect:", len(prev))
only_cur = set(cur) - set(prev)
only_prev = set(prev) - set(cur)
print("only in 11-03:", len(only_cur), sorted(only_cur)[:20])
print("only in 11-02:", len(only_prev), sorted(only_prev)[:20])
if not only_cur and not only_prev:
    print("=> 集合逐篇一致，10-30 组复采完整性与 11-01/11-02 运行互证")
