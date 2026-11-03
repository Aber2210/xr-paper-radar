"""补采 cs.AI 第 2 页（skip=500）：完成 11-03 公告组尾部（declared 521，首页已采 500）+ 11-02 组复采。
11-04 审计：cs.AI 首页（show=500）被 11-03 组占满（500/521），11-02 组未露面。
数据结构：data/audit_1104_newday.json = {day: {paper: [cat, title]}}（按日组嵌套）。
"""
import urllib.request, re, json, time

TARGET_DAY = "2026-11-02"
NEW_DAY = "2026-11-03"
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
    group = json.load(open("data/missed_listing_1104.json",encoding="utf-8"))      # 11-02 组未入馆
    newday = json.load(open("data/audit_1104_newday.json",encoding="utf-8"))        # {day: {paper:[cat,title]}}
    days = json.load(open("data/audit_1104_days.json",encoding="utf-8"))
    nd = newday.setdefault(NEW_DAY, {})
    nd_declared = days.get("cs.AI",{}).get("newday",{}).get(NEW_DAY,{}).get("declared")
    def csai_count():
        return sum(1 for v in nd.values() if v[0]=="cs.AI")
    print("before: 11-03 group total:", len(nd), "cs.AI entries:", csai_count(), "cs.AI declared:", nd_declared, flush=True)
    for skip in (500, 1000, 1500):
        if nd_declared and csai_count() >= nd_declared: break
        html=get(f"https://arxiv.org/list/cs.AI/recent?skip={skip}&show={SHOW}")
        if not html: break
        page=parse_page(html)
        for d,dec,e in page:
            if d==NEW_DAY:
                before=len(nd)
                for p,t in e.items():
                    if p not in nd: nd[p]=["cs.AI",t]
                print(f"[cs.AI skip={skip}] {d} declared={dec} got={len(e)} new={len(nd)-before} total={len(nd)}", flush=True)
            elif d==TARGET_DAY:
                tail=0; tail_new=0
                for p,t in e.items():
                    tail+=1
                    if p not in reg:
                        group.setdefault(p,["cs.AI",t]); tail_new+=1
                print(f"[cs.AI skip={skip}] {d} declared={dec} got={len(e)} unreg_new={tail_new}", flush=True)
            else:
                print(f"[cs.AI skip={skip}] other day {d} got={len(e)}", flush=True)
        time.sleep(8)
    json.dump(group, open("data/missed_listing_1104.json","w",encoding="utf-8"), ensure_ascii=False, indent=1)
    json.dump(newday, open("data/audit_1104_newday.json","w",encoding="utf-8"), ensure_ascii=False, indent=1)
    print("=== cs.AI done ===", flush=True)
    print("11-03 group total unique:", len(nd), "(cs.AI declared 521)", flush=True)
    print("11-02 group unregistered total:", len(group), flush=True)
    # cs.AI 11-02 组完整性：期望 186（11-03 运行记录），逐分类 declared 对齐
    csai_tgt = [p for p,v in group.items() if v[0]=="cs.AI"]
    print("cs.AI 11-02 unregistered:", len(csai_tgt), "(期望 186-已入馆数)", flush=True)

if __name__ == "__main__":
    main()
