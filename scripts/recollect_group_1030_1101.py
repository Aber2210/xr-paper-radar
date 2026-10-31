"""2026-11-01 专用：按 show=500 完整重采 10-30 公告组（修补 show=250 分页跨组丢失 + 代理静默截断绕过闭合日检测的缺陷）。
输出 data/missed_listing_1101_group1030_full.json：{day: {id: {cat, title}}}，仅含未入 registry 条目。
完整性判据：目标日组 got >= declared（声明数）。"""
import urllib.request, re, json, time, sys

CATS = ["cs.CV","cs.GR","cs.HC","cs.MM","cs.RO","cs.AI","eess.IV"]
TARGET_DAY = "2026-10-30"
MONTHS = {'Jan':'01','Feb':'02','Mar':'03','Apr':'04','May':'05','Jun':'06',
          'Jul':'07','Aug':'08','Sep':'09','Oct':'10','Nov':'11','Dec':'12'}
# 兼容 "(showing first 250 of 392 entries)" / "(showing 392 of 392 entries)" / "(continued, showing last 142 of 392 entries)"
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
    """返回 [(day, declared, {id:title})]；页首第一个 h3 之前的条目归入 carry_day（上一页最后日组）。"""
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
        day = f"{dm.group(4)}-{MONTHS[dm.group(3)]}-{dm.group(2)}"
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
    group={}   # id -> (cat, title)  仅 TARGET_DAY
    declared={}
    for c in CATS:
        for attempt in range(1, 6):
            skip=0; cat_group={}; cat_decl=None; carry=None; pages=0; stop=False
            while not stop and skip<=20000:
                html=get(f"https://arxiv.org/list/{c}/recent?skip={skip}&show={SHOW}")
                if not html: break
                pages+=1
                page=parse_page(html, carry_day=carry)
                # 记录本页最后出现的日组作为下页 carry
                if page: carry = page[-1][0]
                page_days=set()
                for day, dec, entries in page:
                    page_days.add(day)
                    if day == TARGET_DAY:
                        if dec: cat_decl = max(cat_decl or 0, dec)
                        for p,t in entries.items():
                            cat_group.setdefault(p, t)
                    elif day > TARGET_DAY:
                        print(f"  !! {c} 发现更新日组 {day}（目标 {TARGET_DAY} 之外）", flush=True)
                # 目标组已闭合（本页出现更旧日头）或已采满 → 停
                closed = any(d < TARGET_DAY for d in page_days)
                complete = cat_decl is not None and len(cat_group) >= cat_decl
                if closed or complete: stop=True
                else: skip += SHOW; time.sleep(8)
            ok = cat_decl is not None and len(cat_group) >= cat_decl
            print(f"{c} attempt{attempt}: pages={pages} got={len(cat_group)} declared={cat_decl} {'OK' if ok else 'INCOMPLETE'}", flush=True)
            if ok or attempt==5: break
            print(f"  -> {c} 目标组不完整，20s 后整体重试", flush=True)
            time.sleep(20)
        declared[c]=cat_decl
        for p,t in cat_group.items():
            group.setdefault(p, (c, t))
        time.sleep(8)
    missed={p:{"cat":c,"title":t} for p,(c,t) in group.items() if p not in reg}
    print(f"\n=== 10-30 组全量 {len(group)} 篇（declared: {declared}），未入馆 {len(missed)} 篇 ===", flush=True)
    json.dump({TARGET_DAY: missed}, open("data/missed_listing_1101_group1030_full.json","w",encoding="utf-8"), ensure_ascii=False, indent=1)
    print("saved data/missed_listing_1101_group1030_full.json", flush=True)

if __name__ == "__main__":
    main()
