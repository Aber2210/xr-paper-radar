import urllib.request, re, json, time, sys

CATS = ["cs.CV","cs.GR","cs.HC","cs.MM","cs.RO","cs.AI","eess.IV"]
MONTHS = {'Jan':'01','Feb':'02','Mar':'03','Apr':'04','May':'05','Jun':'06','Jul':'07','Aug':'08','Sep':'09','Oct':'10','Nov':'11','Dec':'12'}
DAY_RE = r'<h3>((?:Mon|Tue|Wed|Thu|Fri|Sat|Sun), \d{1,2} \w{3} \d{4})([^<]*)</h3>'
# 目标窗口下界必须是「上一批次公告日+1」，随批次变化。
# 旧实现硬编码 2026-10-29：每跑一次都要人工改，忘记改就把 20 天窗口当成本批窗口。
TARGET_LO = sys.argv[3] if len(sys.argv) > 3 else ""
if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", TARGET_LO or ""):
    print("FATAL: 必须传入目标窗口下界，用法: audit_gap_listing.py [cats] [out.json] YYYY-MM-DD", flush=True)
    sys.exit(2)

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
        # 必须补零：旧实现产出 "2026-10-9"，与 "2026-10-29" 做字典序比较时
        # 会把 10-09 判成晚于窗口下界，导致窗口判定与 stop 逻辑同时失真。
        day = f"{dm.group(4)}-{MONTHS[dm.group(3)]}-{int(dm.group(2)):02d}"
        # 分页页头有 first / last / next 三种措辞，只认 first 会把 declared 读成 None，
        # 而 None 会让完整性校验被整体跳过（最终仍打印「全部日期段采集完整」）。
        m = re.search(r'showing\s+(?:(?:first|last|next)\s+)?(\d+)\s+of\s+(\d+)\s+entries', cnt)
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

def audit(cats, out_json, show=500):
    reg=set()
    for l in open("papers/library/registry.jsonl",encoding="utf-8"):
        if l.strip():
            d=json.loads(l); reg.add(d["id"].split(":")[-1].split("v")[0])
    print("registry:", len(reg), flush=True)
    days={}; declared_tot={}
    ok_cats=0
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
                if cat_days: ok_cats+=1
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
    # 写盘守卫（2026-11-17，与 audit_listing_1117 同类修复对齐）：
    #   ① 某分类整段没抓到（get 重试耗尽）时，declared_tot 里根本没有该分类的键，bad 仍为 0，
    #      于是会打印「全部日期段采集完整」并写出残缺 missed —— 与真实 0 漏网完全同形；
    #   ② 有日期段 SHORT 时同样会写出 missed 并 exit 0，调用方按退出码判成功。
    # 两种都不许写盘：宁可失败退出，也不产出看起来正常的空结论。
    if ok_cats < len(cats) or bad:
        print(f"FATAL: {ok_cats}/{len(cats)} 分类采到数据、{bad} 个日期段不足 declared，"
              f"本次对账结论无效，不写 {out_json}", flush=True)
        sys.exit(2)
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
