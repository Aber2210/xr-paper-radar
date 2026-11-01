"""2026-11-02 对账：listing 7 分类日期头核查 + 10-30 公告组完整性复采。
范式继承 recollect_group_1030_1101.py：show=500 单页采全 + continued/last 声明正则 + 逐分类 declared 对齐。
输出：
  data/audit_1102_days.json       —— 各分类见到的日组及条目数（判定最新公告日）
  data/missed_listing_1102.json   —— 10-30 组未入 registry 的条目（id/cat/title）
  data/audit_1102_newday.json     —— 若出现 >2026-10-30 的公告日组，其全部条目（漏跑公告日判定）
"""
import urllib.request, re, json, time, sys

CATS = ["cs.CV","cs.GR","cs.HC","cs.MM","cs.RO","cs.AI","eess.IV"]
TARGET_DAY = "2026-10-30"   # 上批（10-31 运行）处理的公告日
MONTHS = {'Jan':'01','Feb':'02','Mar':'03','Apr':'04','May':'05','Jun':'06',
          'Jul':'07','Aug':'08','Sep':'09','Oct':'10','Nov':'11','Dec':'12'}
DAY_RE = r'<h3>((?:Mon|Tue|Wed|Thu|Fri|Sat|Sun), \d{1,2} \w{3} \d{4})([^<]*)</h3>'
CNT_RE = re.compile(r'showing\s+(?:(?:first|last)\s+)?(\d+)\s+of\s+(\d+)\s+entries')
SHOW = 500

def get(url, tries=6):
    req = urllib.request.Request(url, headers={"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120.0 Safari/537.36"})
    last=None
    for i in range(tries):
        try:
            with urllib.request.urlopen(req, timeout=120) as r:
                return r.read().decode("utf-8","replace")
        except Exception as e:
            last=e; wait=min(90, 5*2**i)
            print(f"  retry {i+1}/{tries} after {wait}s ({e})", flush=True)
            time.sleep(wait)
    print("GIVEUP", url[:90], last, flush=True); return None

def parse_page(html, carry_day=None):
    out=[]; parts = re.split(DAY_RE, html)
    if carry_day is not None:
        pre_ids = {}
        for b in re.split(r'<dt>', parts[0])[1:]:
            am = re.search(r'/abs/(\d{4}\.\d{4,5})', b)
            if am: pre_ids[am.group(1)] = ''
        if pre_ids:
            out.append((carry_day, None, pre_ids))
    for i in range(1, len(parts)-2, 3):
        dstr, cnt, body = parts[i], parts[i+1], parts[i+2]
        dm = re.match(r'(\w{3}), (\d{1,2}) (\w{3}) (\d{4})', dstr)
        if not dm: continue
        day = f"{dm.group(4)}-{MONTHS[dm.group(3)]}-{int(dm.group(2)):02d}"
        m = CNT_RE.search(cnt)
        declared = int(m.group(2)) if m else None
        entries={}
        for b in re.split(r'<dt>', body)[1:]:
            am = re.search(r'/abs/(\d{4}\.\d{4,5})', b)
            if not am: continue
            tm = re.search(r"list-title[^>]*>.*?Title:</span>\s*(.*?)\s*</div>", b, re.S)
            title = re.sub(r'\s+',' ', tm.group(1)).strip() if tm else ''
            entries[am.group(1)] = title
        out.append((day, declared, entries))
    return out

def main():
    reg=set()
    for l in open("papers/library/registry.jsonl",encoding="utf-8"):
        if l.strip():
            d=json.loads(l); reg.add(d["id"].split(":")[-1].split("v")[0])
    print("registry:", len(reg), flush=True)
    days_seen={}        # day -> {cat: count}
    group={}            # TARGET_DAY: id -> (cat, title) 未入馆
    newday={}           # day > TARGET_DAY: id -> (cat, title)
    for c in CATS:
        for attempt in range(1, 6):
            skip=0; carry=None; stop=False; got={}; cat_decl=None; newcat={}
            while not stop and skip<=20000:
                html=get(f"https://arxiv.org/list/{c}/recent?skip={skip}&show={SHOW}")
                if not html: break
                page=parse_page(html, carry_day=carry)
                if page: carry = page[-1][0]
                newest_on_page = max((d for d,_,_ in page), default=None)
                for day, dec, entries in page:
                    days_seen.setdefault(day, {}).setdefault(c, len(entries))
                    if day == TARGET_DAY:
                        if dec: cat_decl = max(cat_decl or 0, dec)
                        for p,t in entries.items():
                            if p not in reg:
                                group.setdefault(p, [c, t])
                    elif day > TARGET_DAY:
                        for p,t in entries.items():
                            newday.setdefault(day, {}).setdefault(p, [c, t])
                # 翻页直到越过目标日组（目标日组在页中全部出现后，下一页最新日 < 目标日即可停）
                if newest_on_page is not None and newest_on_page < TARGET_DAY:
                    stop=True
                skip += SHOW
                time.sleep(8)
            ok = (cat_decl is not None)
            print(f"[{c}] declared={cat_decl} unregistered={sum(1 for p in group if group[p][0]==c)} newday={sum(1 for d in newcat for p in newday.get(d,{}) if newday[d][p][0]==c)} ok={ok}", flush=True)
            if ok: break
            print(f"[{c}] attempt {attempt} incomplete, retry", flush=True)
            time.sleep(8)
    out_days = {d: dict(sorted(v.items())) for d,v in sorted(days_seen.items())}
    json.dump(out_days, open("data/audit_1102_days.json","w",encoding="utf-8"), ensure_ascii=False, indent=1)
    json.dump({p:v for p,v in group.items()}, open("data/missed_listing_1102.json","w",encoding="utf-8"), ensure_ascii=False, indent=1)
    json.dump(newday, open("data/audit_1102_newday.json","w",encoding="utf-8"), ensure_ascii=False, indent=1)
    print("=== days seen ===", flush=True)
    for d in sorted(days_seen):
        tot=sum(days_seen[d].values()); print(f"  {d}: total_slots={tot} {days_seen[d]}", flush=True)
    print("unregistered in", TARGET_DAY, ":", len(group), flush=True)
    print("newday groups >", TARGET_DAY, ":", {d: len(v) for d,v in newday.items()} or "NONE", flush=True)

if __name__ == "__main__":
    main()
