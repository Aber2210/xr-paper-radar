"""2026-11-05 对账：每分类 show=500 单页（目标日组 declared≠got 时补采后续页）。
TARGET_DAY=2026-11-03（上批公告日，复采核对漏网）；预期最新公告日=2026-11-04。
输出：
  data/audit_1105_days.json      各分类最新日期头与全页日组
  data/missed_listing_1105.json  11-03 组未入 registry 条目（id/cat/title）
  data/audit_1105_newday.json    >2026-11-03 日组记录（新公告日判定/漏跑公告日判定）
  data/audit_1105_alldays.json   全页各日组条目数（按分类）
"""
import urllib.request, re, json, time

CATS = ["cs.CV","cs.GR","cs.HC","cs.MM","cs.RO","cs.AI","eess.IV"]
TARGET_DAY = "2026-11-03"
MONTHS = {'Jan':'01','Feb':'02','Mar':'03','Apr':'04','May':'05','Oct':'10','Nov':'11','Dec':'12',
          'Jul':'07','Aug':'08','Sep':'09'}
DAY_RE = r'<h3>((?:Mon|Tue|Wed|Thu|Fri|Sat|Sun), \d{1,2} \w{3} \d{4})([^<]*)</h3>'
CNT_RE = re.compile(r'showing\s+(?:(?:first|last)\s+)?(\d+)\s+of\s+(\d+)\s+entries')
SHOW = 500
UA = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120.0 Safari/537.36"}

def get(url, tries=5):
    last=None
    for i in range(tries):
        try:
            req = urllib.request.Request(url, headers=UA)
            with urllib.request.urlopen(req, timeout=90) as r:
                return r.read().decode("utf-8","replace")
        except Exception as e:
            last=e; wait=min(60, 5*2**i)
            print(f"  retry {i+1}/{tries} after {wait}s ({e})", flush=True)
            time.sleep(wait)
    print("GIVEUP", url[:90], last, flush=True); return None

def parse_page(html):
    out=[]; parts = re.split(DAY_RE, html)
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

def fetch_cat(c):
    """返回 (page, notes, got, dec)。目标日组 declared≠got 时补采后续页合并。"""
    page = parse_page(get(f"https://arxiv.org/list/{c}/recent?skip=0&show={SHOW}") or "")
    notes=[]
    if not page: return page, notes, {}, None
    tgt=[(d,dec,e) for d,dec,e in page if d==TARGET_DAY]
    dec = max((dec for _,dec,_ in tgt if dec), default=None)
    got={}
    for _,_,e in tgt: got.update(e)
    if dec is not None and len(got) < dec:
        for skip in (SHOW, SHOW*2, SHOW*3):
            html = get(f"https://arxiv.org/list/{c}/recent?skip={skip}&show={SHOW}")
            if not html: break
            p2 = parse_page(html)
            merged=0
            for d,dec2,e in p2:
                if d==TARGET_DAY:
                    for k,v in e.items():
                        if k not in got: got[k]=v; merged+=1
            notes.append(f"paged skip={skip} merged={merged} total={len(got)}/{dec}")
            if len(got)>=dec: break
            time.sleep(8)
    return page, notes, got, dec

def main():
    reg=set()
    for l in open("papers/library/registry.jsonl",encoding="utf-8"):
        if l.strip():
            d=json.loads(l); reg.add(d["id"].split(":")[-1].split("v")[0])
    print("registry:", len(reg), flush=True)
    cat_report={}; group={}; newday={}; all_days={}
    for c in CATS:
        page, notes, got, dec = fetch_cat(c)
        if not page:
            print(f"[{c}] FAILED to fetch", flush=True); time.sleep(8); continue
        newest=max(d for d,_,_ in page)
        nd_info={}
        for d,dec2,e in page:
            if d > TARGET_DAY:
                for p,t in e.items(): newday.setdefault(d,{}).setdefault(p,[c,t])
                nd_info[d]={"declared":dec2,"got":len(e)}
        cat_report[c]={"newest_day":newest,"target_declared":dec,"target_got":len(got),
                       "page_days":{d:len(e) for d,_,e in page},"newday":nd_info,"paged":notes}
        for p,t in got.items():
            if p not in reg: group.setdefault(p,[c,t])
        for d,_,e in page: all_days.setdefault(d,{}).setdefault(c,len(e))
        flag = "OK" if (dec is not None and len(got)>=dec) else "CHECK"
        print(f"[{c}] newest={newest} target declared={dec} got={len(got)} [{flag}] unreg={sum(1 for p in got if p not in reg)} newday={nd_info} {notes}", flush=True)
        time.sleep(8)
    json.dump(cat_report, open("data/audit_1105_days.json","w",encoding="utf-8"), ensure_ascii=False, indent=1)
    json.dump(group, open("data/missed_listing_1105.json","w",encoding="utf-8"), ensure_ascii=False, indent=1)
    json.dump(newday, open("data/audit_1105_newday.json","w",encoding="utf-8"), ensure_ascii=False, indent=1)
    json.dump(all_days, open("data/audit_1105_alldays.json","w",encoding="utf-8"), ensure_ascii=False, indent=1)
    print("=== summary ===", flush=True)
    for c,v in cat_report.items():
        flag = "OK" if (v["target_declared"] is not None and v["target_got"]>=v["target_declared"]) else "CHECK"
        print(f"  {c}: newest={v['newest_day']} 11-03 declared={v['target_declared']} got={v['target_got']} [{flag}]", flush=True)
    print("unregistered in 11-03 group:", len(group), flush=True)
    print("newday groups > 11-03:", {d:len(v) for d,v in newday.items()} or "NONE", flush=True)

if __name__ == "__main__":
    main()
