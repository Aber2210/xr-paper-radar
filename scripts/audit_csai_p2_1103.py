"""补采 cs.AI 第 2 页（skip=500）完成 10-30 公告组复采 + 汇总未入馆条目。
11-03 审计：cs.AI 首页（show=500）被 11-02 组（186）挤出 10-30 组尾部 78 条，
第 2 页以 "(continued, showing last N of M entries)" 开头，需兼容该措辞。
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
    # 读 11-03 审计已产出的 10-30 组未入馆集合
    group = json.load(open("data/missed_listing_1103.json",encoding="utf-8"))
    # 补采 cs.AI 第 2 页
    html=get("https://arxiv.org/list/cs.AI/recent?skip=500&show=500")
    tail=0; tail_new=0
    if html:
        page=parse_page(html)
        for d,dec,e in page:
            if d==TARGET_DAY:
                print(f"[cs.AI p2] {d} declared={dec} got={len(e)}", flush=True)
                for p,t in e.items():
                    tail+=1
                    if p not in reg:
                        group.setdefault(p,["cs.AI",t]); tail_new+=1
            else:
                print(f"[cs.AI p2] other day group {d} got={len(e)} (skip)", flush=True)
    print(f"cs.AI p2 tail entries={tail} new_unregistered={tail_new}", flush=True)
    print("10-30 group total unregistered now:", len(group), flush=True)
    json.dump(group, open("data/missed_listing_1103.json","w",encoding="utf-8"), ensure_ascii=False, indent=1)

if __name__ == "__main__":
    main()
