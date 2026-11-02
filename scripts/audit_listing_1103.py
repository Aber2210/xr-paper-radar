"""2026-11-03 对账（高效版）：每分类仅取 show=500 第 1 页。
依据：上批（11-02 运行）确认 10-30 公告组各分类均 <500；本批 TARGET_DAY=2026-10-30 复采 + 判定最新公告日。
预期：周末积压于周一 00:00 UTC（08:00 北京时间）释放 → 11-02（周一）公告日组应出现。
输出：
  data/audit_1103_days.json      各分类最新日期头与全页日组
  data/missed_listing_1103.json  10-30 组未入 registry 条目（id/cat/title）
  data/audit_1103_newday.json    >2026-10-30 日组记录（新公告日判定/漏跑公告日判定）
  data/audit_1103_alldays.json   全页各日组条目数（按分类）
"""
import urllib.request, re, json, time

CATS = ["cs.CV","cs.GR","cs.HC","cs.MM","cs.RO","cs.AI","eess.IV"]
TARGET_DAY = "2026-10-30"
MONTHS = {'Jan':'01','Feb':'02','Mar':'03','Apr':'04','May':'05','Jun':'06',
          'Jul':'07','Aug':'08','Sep':'09','Oct':'10','Nov':'11','Dec':'12'}
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

def main():
    reg=set()
    for l in open("papers/library/registry.jsonl",encoding="utf-8"):
        if l.strip():
            d=json.loads(l); reg.add(d["id"].split(":")[-1].split("v")[0])
    print("registry:", len(reg), flush=True)
    cat_report={}; group={}; newday={}; all_days={}
    for c in CATS:
        for attempt in range(1, 6):
            html=get(f"https://arxiv.org/list/{c}/recent?skip=0&show={SHOW}")
            if not html: continue
            page=parse_page(html)
            if not page:
                print(f"[{c}] attempt {attempt}: no day headers parsed, retry", flush=True); time.sleep(8); continue
            newest=max(d for d,_,_ in page)
            tgt=[(d,dec,e) for d,dec,e in page if d==TARGET_DAY]
            dec = max((dec for _,dec,_ in tgt if dec), default=None)
            got = {}
            for _,_,e in tgt: got.update(e)
            # 页内 >TARGET_DAY 的日组（新公告日/漏跑公告日），同时核 declared/got
            nd_info={}
            for d,dec2,e in page:
                if d > TARGET_DAY:
                    for p,t in e.items(): newday.setdefault(d,{}).setdefault(p,[c,t])
                    nd_info[d]={"declared":dec2,"got":len(e)}
            cat_report[c]={"newest_day":newest,"target_declared":dec,"target_got":len(got),
                           "page_days":{d:len(e) for d,_,e in page},"newday":nd_info}
            for p,t in got.items():
                if p not in reg: group.setdefault(p,[c,t])
            for d,_,e in page: all_days.setdefault(d,{}).setdefault(c,len(e))
            print(f"[{c}] newest={newest} target declared={dec} got={len(got)} unregistered={sum(1 for p in got if p not in reg)} newday={nd_info}", flush=True)
            break
        time.sleep(8)
    json.dump(cat_report, open("data/audit_1103_days.json","w",encoding="utf-8"), ensure_ascii=False, indent=1)
    json.dump(group, open("data/missed_listing_1103.json","w",encoding="utf-8"), ensure_ascii=False, indent=1)
    json.dump(newday, open("data/audit_1103_newday.json","w",encoding="utf-8"), ensure_ascii=False, indent=1)
    json.dump(all_days, open("data/audit_1103_alldays.json","w",encoding="utf-8"), ensure_ascii=False, indent=1)
    print("=== summary ===", flush=True)
    for c,v in cat_report.items():
        flag = "OK" if (v["target_declared"] is not None and v["target_got"]>=v["target_declared"]) else "CHECK"
        print(f"  {c}: newest={v['newest_day']} 10-30 declared={v['target_declared']} got={v['target_got']} [{flag}]", flush=True)
    print("unregistered in 10-30 group:", len(group), flush=True)
    print("newday groups > 10-30:", {d:len(v) for d,v in newday.items()} or "NONE", flush=True)

if __name__ == "__main__":
    main()
