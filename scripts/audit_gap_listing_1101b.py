import urllib.request, re, json, time, sys

CATS = ["cs.CV","cs.GR","cs.HC","cs.MM","cs.RO","cs.AI","eess.IV"]
MONTHS = {'Jan':'01','Feb':'02','Mar':'03','Apr':'04','May':'05','Jun':'06','Jul':'07','Aug':'08','Sep':'09','Oct':'10','Nov':'11','Dec':'12'}
DAY_RE = r'<h3>((?:Mon|Tue|Wed|Thu|Fri|Sat|Sun), \d{1,2} \w{3} \d{4})([^<]*)</h3>'
TARGET_LO = "2026-10-30"   # 目标窗口下界（含）= 上一批次公告日+1（10-31 运行：复核 10-29 公告是否延迟释放 + 审计 10-30 组）

def get(url, tries=8):
    req = urllib.request.Request(url, headers={"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120.0 Safari/537.36"})
    last=None
    for i in range(tries):
        try:
            with urllib.request.urlopen(req, timeout=120) as r:
                return r.read().decode("utf-8","replace")
        except Exception as e:
            last=e
            wait=min(90, 5*2**i)
            print(f"  retry {i+1}/{tries} after {wait}s ({e})", flush=True)
            time.sleep(wait)
    print("GIVEUP", url[:90], last, flush=True); return None

def parse_page(html):
    out=[]
    parts = re.split(DAY_RE, html)
    for i in range(1, len(parts)-2, 3):
        dstr, cnt, body = parts[i], parts[i+1], parts[i+2]
        dm = re.match(r'(\w{3}), (\d{1,2}) (\w{3}) (\d{4})', dstr)
        if not dm: continue
        day = f"{dm.group(4)}-{MONTHS[dm.group(3)]}-{dm.group(2)}"
        m = re.search(r'showing\s+(?:first\s+)?(\d+)\s+of\s+(\d+)\s+entries', cnt)
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

def audit(cats, out_json, show=250):
    reg=set()
    for l in open("papers/library/registry.jsonl",encoding="utf-8"):
        if l.strip():
            d=json.loads(l); reg.add(d["id"].split(":")[-1].split("v")[0])
    print("registry:", len(reg), flush=True)
    days={}; declared_tot={}
    for c in cats:
        for attempt in range(1, 6):
            skip=0; seen=set(); pages=0; empty_pages=0; stop=False
            cat_days={}; cat_decl={}
            while not stop and skip<=20000:
                # 逐页截断重试（2026-10-20 新增）：服务端/代理会间歇返回不完整页面（200 但条目少），
                # 表现同 2MB 静默截断。判据=窗口内已闭合日组 declared>实采 → 重取本页。
                page=None
                for pt in range(5):
                    html=get(f"https://arxiv.org/list/{c}/recent?skip={skip}&show={show}")
                    if not html: break
                    page=parse_page(html)
                    probe={}
                    for day, declared, entries in page:
                        probe.setdefault(day, [set(entries.keys()), declared])
                    closed_bad=[]
                    for day,(ids,declared) in probe.items():
                        if day < TARGET_LO: continue
                        tot_decl = declared or cat_decl.get((c,day))
                        if not tot_decl: continue
                        got = len(ids) + sum(1 for p in cat_days.get(day,{}) if p not in ids)
                        if got < tot_decl and any(dd < day for dd in probe):
                            closed_bad.append(f"{day}:{got}/{tot_decl}")
                    if not closed_bad: break
                    print(f"  {c} skip={skip} 第{pt+1}次疑似截断（{closed_bad}），10s 后重取", flush=True)
                    time.sleep(10)
                if not page: break
                pages+=1; new_entries=0; oldest=None
                for day, declared, entries in page:
                    cat_decl[(c,day)] = max(cat_decl.get((c,day),0), declared or 0)
                    for p,t in entries.items():
                        if p not in cat_days.setdefault(day, {}): new_entries+=1
                        cat_days[day].setdefault(p, (c, t))
                        oldest = day if oldest is None or day < oldest else oldest
                    seen.add(day)
                # 停止条件修正（2026-10-20）：页内多日头时，只有本页最旧条目也早于窗口下界才停；
                # 旧逻辑「见任一旧日头即停」会在降级页/截断页上提前中断，漏采窗口内条目。
                if oldest is not None and oldest < TARGET_LO: stop=True
                if new_entries==0:
                    empty_pages+=1
                    if empty_pages>=2: break
                else: empty_pages=0
                if stop: break
                skip += show; time.sleep(8)
            # 完整性：目标窗口内每个已见日期段须采满（declared 缺失也视为不完整）
            incomplete = [d for d in seen if d >= TARGET_LO and
                          (cat_decl.get((c,d)) is None or
                           sum(1 for p,(cc,t) in cat_days.get(d,{}).items() if cc==c) < cat_decl.get((c,d)))]
            print(f"{c} attempt{attempt}: days={sorted(seen)} pages={pages} incomplete={incomplete}", flush=True)
            if not incomplete or attempt==5:
                for day, ents in cat_days.items():
                    for p,t in ents.items(): days.setdefault(day, {}).setdefault(p, (c,t))
                for k,v in cat_decl.items(): declared_tot[k]=max(declared_tot.get(k,0), v)
                break
            print(f"  -> {c} 采集不完整，整体重试（{attempt}/5）", flush=True)
            time.sleep(20)
    print("\n=== 完整性校验（只列缺口）===", flush=True)
    bad=0
    for (c,day), dec in sorted(declared_tot.items(), key=lambda x:(x[0][1],x[0][0])):
        if day < TARGET_LO: continue
        got = sum(1 for p,(cc,t) in days.get(day,{}).items() if cc==c)
        if got < dec:
            print(f"  {c} {day}: SHORT {got}/{dec}"); bad+=1
    if bad==0: print("  全部日期段采集完整", flush=True)
    missed={}
    for day in sorted(days):
        if day < TARGET_LO: continue
        m={p:{"cat":c,"title":t} for p,(c,t) in days[day].items() if p not in reg}
        missed[day]=m
        print(f"{day}: total={len(days[day])} | missed={len(m)}", flush=True)
    tot=sum(len(v) for v in missed.values())
    print("TOTAL MISSED:", tot, flush=True)
    json.dump(missed, open(out_json,"w",encoding="utf-8"), ensure_ascii=False, indent=1)
    print("saved", out_json, flush=True)

if __name__ == "__main__":
    cats = sys.argv[1].split(",") if len(sys.argv)>1 else CATS
    out = sys.argv[2] if len(sys.argv)>2 else "data/missed_listing.json"
    audit(cats, out)
