"""2026-11-14 对账：每分类 show=500 单页 + 目标日组 declared!=got 时补采后续页（continued/last 兼容）。

背景：11-13 运行判定 11-12（周四）公告批次未释放（工作日跳空第 2 次）。
本日复核是否存在延迟释放的 11-12 / 11-13 公告组。

目标日组：
  PREV_DAY  = 2026-11-11（上批已处理公告日，复采核对 0 漏网）
  NEW_DAYS  = [2026-11-12, 2026-11-13]（可能出现的延迟释放 / 常规公告组）

输出：
  data/audit_1114_days.json       各分类最新日期头 / 各日组 declared-got / 补页记录
  data/audit_1114_alldays.json    全页各日组条目数（按分类）
  data/newday_1114.json           NEW_DAYS 并集全部条目（id -> [cat,title]）
  data/missed_prev_1114.json      PREV_DAY 组未入 registry 条目
  data/missed_new_1114.json       NEW_DAYS 组未入 registry 条目
"""
import urllib.request, re, json, time

CATS = ["cs.CV", "cs.GR", "cs.HC", "cs.MM", "cs.RO", "cs.AI", "eess.IV"]
PREV_DAY = "2026-11-11"
NEW_DAYS = ["2026-11-12", "2026-11-13"]
MONTHS = {'Jan': '01', 'Feb': '02', 'Mar': '03', 'Apr': '04', 'May': '05', 'Jun': '06',
          'Jul': '07', 'Aug': '08', 'Sep': '09', 'Oct': '10', 'Nov': '11', 'Dec': '12'}
DAY_RE = r'<h3>((?:Mon|Tue|Wed|Thu|Fri|Sat|Sun), \d{1,2} \w{3} \d{4})([^<]*)</h3>'
CNT_RE = re.compile(r'showing\s+(?:(?:first|last|next)\s+)?(\d+)\s+of\s+(\d+)\s+entries')
SHOW = 500
UA = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120.0 Safari/537.36"}


def get(url, tries=5):
    last = None
    for i in range(tries):
        try:
            req = urllib.request.Request(url, headers=UA)
            with urllib.request.urlopen(req, timeout=90) as r:
                return r.read().decode("utf-8", "replace")
        except Exception as e:
            last = e
            wait = min(60, 5 * 2 ** i)
            print(f"  retry {i+1}/{tries} after {wait}s ({e})", flush=True)
            time.sleep(wait)
    print("GIVEUP", url[:90], last, flush=True)
    return None


def parse_page(html):
    out = []
    parts = re.split(DAY_RE, html)
    for i in range(1, len(parts) - 2, 3):
        dstr, cnt, body = parts[i], parts[i + 1], parts[i + 2]
        dm = re.match(r'(\w{3}), (\d{1,2}) (\w{3}) (\d{4})', dstr)
        if not dm:
            continue
        day = f"{dm.group(4)}-{MONTHS[dm.group(3)]}-{int(dm.group(2)):02d}"
        m = CNT_RE.search(cnt)
        declared = int(m.group(2)) if m else None
        entries = {}
        for b in re.split(r'<dt>', body)[1:]:
            am = re.search(r'/abs/(\d{4}\.\d{4,5})', b)
            if not am:
                continue
            tm = re.search(r"list-title[^>]*>.*?Title:</span>\s*(.*?)\s*</div>", b, re.S)
            title = re.sub(r'\s+', ' ', tm.group(1)).strip() if tm else ''
            entries[am.group(1)] = title
        out.append((day, declared, entries))
    return out


def fetch_cat(c):
    page = parse_page(get(f"https://arxiv.org/list/{c}/recent?skip=0&show={SHOW}") or "")
    notes = []
    if not page:
        return page, notes, {}
    targets = [PREV_DAY] + NEW_DAYS
    got = {}
    decl = {}
    for d in targets:
        e0 = {}
        for dd, _, e in page:
            if dd == d:
                e0.update(e)
        got[d] = e0
        decl[d] = max((dec for dd, dec, _ in page if dd == d and dec), default=None)
    for d in targets:
        if decl[d] is not None and len(got[d]) < decl[d]:
            for skip in (SHOW, SHOW * 2, SHOW * 3):
                html = get(f"https://arxiv.org/list/{c}/recent?skip={skip}&show={SHOW}")
                if not html:
                    break
                p2 = parse_page(html)
                merged = 0
                reached_older = False
                for dd, _, e in p2:
                    if dd == d:
                        for k, v in e.items():
                            if k not in got[d]:
                                got[d][k] = v
                                merged += 1
                    elif dd < d:
                        reached_older = True
                notes.append(f"{d} paged skip={skip} merged={merged} total={len(got[d])}/{decl[d]}")
                if len(got[d]) >= decl[d] or reached_older:
                    break
                time.sleep(8)
    return page, notes, {"got": got, "decl": decl}


def main():
    reg = set()
    for l in open("papers/library/registry.jsonl", encoding="utf-8"):
        if l.strip():
            d = json.loads(l)
            reg.add(d["id"].split(":")[-1].split("v")[0])
    print("registry:", len(reg), flush=True)
    cat_report = {}
    missed_prev = {}
    newday = {}
    missed_new = {}
    all_days = {}
    for c in CATS:
        t0 = time.time()
        page, notes, info = fetch_cat(c)
        if not page:
            print(f"[{c}] FAILED to fetch", flush=True)
            time.sleep(8)
            continue
        got = info.get("got", {})
        decl = info.get("decl", {})
        newest = max(d for d, _, _ in page)
        cat_report[c] = {
            "newest_day": newest,
            "prev": {"day": PREV_DAY, "declared": decl.get(PREV_DAY), "got": len(got.get(PREV_DAY, {}))},
            "new": {d: {"declared": decl.get(d), "got": len(got.get(d, {}))} for d in NEW_DAYS},
            "page_days": {d: len(e) for d, _, e in page},
            "paged": notes,
        }
        for p, t in got.get(PREV_DAY, {}).items():
            if p not in reg:
                missed_prev.setdefault(p, [c, t])
        for d in NEW_DAYS:
            for p, t in got.get(d, {}).items():
                if p not in newday:
                    newday[p] = [c, t, d]
                    if p not in reg:
                        missed_new[p] = [c, t, d]
        for d, _, e in page:
            all_days.setdefault(d, {}).setdefault(c, len(e))
        f1 = "OK" if (decl.get(PREV_DAY) is not None and len(got.get(PREV_DAY, {})) >= decl[PREV_DAY]) else "CHECK"
        newdesc = " ".join(
            f"{d}:dec={decl.get(d)}/got={len(got.get(d, {}))}" for d in NEW_DAYS
        )
        print(f"[{c}] newest={newest} prev dec={decl.get(PREV_DAY)} got={len(got.get(PREV_DAY,{}))} [{f1}] "
              f"{newdesc} unreg_total={len(missed_new)} {notes} {time.time()-t0:.0f}s", flush=True)
        time.sleep(8)
    json.dump(cat_report, open("data/audit_1114_days.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    json.dump(all_days, open("data/audit_1114_alldays.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    json.dump(newday, open("data/newday_1114.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    json.dump(missed_prev, open("data/missed_prev_1114.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    json.dump(missed_new, open("data/missed_new_1114.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print("=== summary ===", flush=True)
    for c, v in cat_report.items():
        print(f"  {c}: newest={v['newest_day']} prev_got={v['prev']['got']}/{v['prev']['declared']} "
              f"new={v['new']}", flush=True)
    print("all day groups:", json.dumps({d: sum(v.values()) for d, v in sorted(all_days.items(), reverse=True)[:6]},
                                        ensure_ascii=False), flush=True)
    print("unregistered in prev group:", len(missed_prev), flush=True)
    print("new group unique:", len(newday), "unregistered:", len(missed_new), flush=True)


if __name__ == "__main__":
    main()
