"""把 newday_1110.json（{id:[cat,title]}）转为 filter_missed_xr_abstract 期望结构（{day:{id:{cat,title}}}）。"""
import json

RAW = "data/newday_1110.json"
OUT = "data/newday_1110_byday.json"
DAY = "2026-11-09"

raw = json.load(open(RAW, encoding="utf-8"))
out = {DAY: {}}
for pid, v in raw.items():
    cat, title = (v[0], v[1]) if isinstance(v, list) else (v.get("cat", ""), v.get("title", ""))
    out[DAY][pid] = {"cat": cat, "title": title}
json.dump(out, open(OUT, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("raw", len(raw), "-> byday", len(out[DAY]))
