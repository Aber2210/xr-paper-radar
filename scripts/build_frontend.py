# -*- coding: utf-8 -*-
"""build_frontend.py — 从 registry + 原子笔记 + 每日 7 维表生成前端归纳整理页。

输出：web/xr-paper-hub.html（自包含单页，深色主题，五个标签页）

数据源与口径：
  papers/daily/<date>/7dim-table.md   各日权威论文清单（每日解读卡片以此为准）
  papers/library/registry.jsonl       全量评分登记（论文库 / 七维对比 / 富化信息）
  papers/notes/*.md                   原子笔记（frontmatter + ## 分节）
  papers/MOC/MOC-总索引.md            各日状态注记
  reports/*.md                        解读报告（链接）
"""
import json, os, re, glob, datetime

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
NONXR = "—（非 XR）"
DIMS = ["IMP", "NOV", "TEC", "EXP", "PER", "TRL", "REP"]
WEIGHTS = {"IMP": .20, "NOV": .20, "TEC": .15, "EXP": .15, "PER": .15, "TRL": .08, "REP": .07}
DIM_DEFS = {
    "IMP": "领域公认卡脖子 / 高频痛点",
    "NOV": "新范式 / 新架构",
    "TEC": "理论 + 系统 + 消融齐全",
    "EXP": "多数据集 + 真机 + 大样本用户实验",
    "PER": "相对 SOTA 提升 > 30%",
    "TRL": "已产品化 / 开源可商用（TRL 1-9 映射）",
    "REP": "有代码 + 数据 + 高引用 / 顶会",
}
BATCH_LABELS = {"2026-09-20": "2026-09-20 · 基线建库",
                "2026-10-17": "2026-10-17 · 10-16 公告批次（积压补齐）",
                "2026-10-18": "2026-10-18 · 无新稿（周日漏网对账日）",
                "2026-10-19": "2026-10-19 · 10-13~10-16 漏网补充补录（重磅日）",
                "2026-10-20": "2026-10-20 · 10-19 公告批次（重磅日）",
                "2026-10-21": "2026-10-21 · 10-20 公告批次（最大公告日，非重磅）",
                "2026-10-22": "2026-10-22 · 10-21 公告批次（非重磅，无 backfill）",
                "2026-10-23": "2026-10-23 · 10-22 公告批次（非重磅）",
                "2026-10-24": "2026-10-24 · 10-23 公告批次（非重磅，listing 对账补齐漏网 5 篇）",
                "2026-10-25": "2026-10-25 · 无新稿（周日漏网对账日，10-23 公告组复核 0 漏网）",
                "2026-10-26": "2026-10-26 · 无新稿（周一凌晨，周末积压公告未到时刻，10-23 公告组 411 篇全量复核 0 漏网）",
                "backfill-1012-1015": "backfill · 10-12~10-15 漏网补录",
                "backfill-1020": "backfill · 10-16 漏网 + 旧稿再公告补录",
                "backfill-1021": "backfill · 旧稿 replace/cross 再公告补录",
                "backfill-1023": "backfill · 10-21 漏网补录 + 旧稿 replace/cross 再公告",
                "backfill-1024": "backfill · 10-23 公告 RSS 混入旧稿 replace 再公告",
                "backfill-2603-2609": "backfill · 2603–2609 旧稿补录"}


def read_text(p):
    with open(p, "rb") as f:
        return f.read().decode("utf-8-sig", "replace").replace("\r\n", "\n")


def base_id(full_id):
    return full_id.split(":")[-1].split("v")[0]


def rel(p):
    return "../" + os.path.relpath(p, ROOT).replace(os.sep, "/")


def _cols_of(lines):
    """在表体行中定位表头行并返回列名列表，无表头返回 None。"""
    hi = next((i for i, l in enumerate(lines) if l.startswith("|") and "IMP" in l), None)
    if hi is None:
        return None, None
    return hi, [c.strip() for c in lines[hi].strip().strip("|").split("|")]


def _parse_rows(body, hi, cols, paper_index):
    """按列名映射解析数据行。"""
    def find(*names):
        for i, c in enumerate(cols):
            if any(n in c for n in names):
                return i
        return None
    ci = find("arXiv")
    ct = find("标题", "题名", "论文")
    ctr = cols.index("赛道") if "赛道" in cols else None
    cdim = {d: cols.index(d) for d in DIMS if d in cols}
    ctot = find("总分", "加权", "Value")
    cg = find("等级", "档")
    cout = cols.index("落后") if "落后" in cols else None
    cnew = find("新入馆", "新")
    cev = find("证据", "证")
    rows = []
    for ln in body[hi + 1:]:
        if not ln.startswith("|"):
            continue
        cells = [c.strip() for c in ln.strip().strip("|").split("|")]
        if len(cells) < len(cols):
            continue
        if all(re.match(r"^:?-+:?$", c) for c in cells if c):
            continue
        m = re.search(r"(\d{4}\.\d{4,5})", cells[ci]) if ci is not None else None
        if not m:
            continue
        pid = m.group(1)
        title = cells[ct] if ct is not None else ""
        top10_mark = "Top10" in title or "TOP10" in title
        title = re.sub(r"[⭐★\s]*Top10\s*", "", title).strip()
        scores = {}
        for d, i in cdim.items():
            try:
                scores[d] = float(cells[i])
            except (ValueError, IndexError):
                scores[d] = 0
        val = None
        if ctot is not None:
            mm = re.search(r"\d+(?:\.\d+)?", cells[ctot])
            if mm:
                val = float(mm.group(0))
        if val is None:
            val = round(sum(scores[d] * WEIGHTS[d] for d in DIMS), 3)
        grade = ""
        if cg is not None:
            gm = re.search(r"[SABC]", cells[cg])
            grade = gm.group(0) if gm else ""
        outdated = False
        if cout is not None:
            ov = cells[cout].strip()
            outdated = bool(ov) and ov not in ("—", "-", "–", "")
        newmark = cells[cnew] if cnew is not None else ""
        evmark = cells[cev] if cev is not None else ""
        rows.append({"rank": len(rows) + 1, "id": pid, "title_zh": title,
                     "track": cells[ctr] if ctr is not None else "",
                     "scores": {d: (int(scores[d]) if scores[d] == int(scores[d]) else scores[d]) for d in DIMS},
                     "value": val, "grade": grade, "outdated": outdated,
                     "top10Mark": top10_mark, "newMark": newmark, "evMark": evmark})
    return rows


def parse_daily_table(path, paper_index):
    """解析每日 7 维对比表：按 ## 分节，区分 Top10/其余XR/非XR/全量(带✅新标记)/前沿参考。

    返回 (window, xr_rows, ref_rows)。xr_rows 为当日新入选 XR 论文（已按 registry 剔除非 XR）。
    """
    txt = read_text(path)
    lines = txt.split("\n")
    window = ""
    m = re.search(r"^>[ \t]*(?:拉取窗口|数据窗口|时间窗口|拉取日)[：:](.+)$", txt, re.M)
    if m:
        window = m.group(1).strip().replace("**", "")
    if not window:
        m = re.search(r"^>[ \t]*(?:⚠️\s*)?(?:说明|注)[：:](.+)$", txt, re.M)
        if m:
            window = m.group(1).strip().replace("**", "")
    is_ref = ("非当日新拉取" in txt) or ("最新前沿参考" in txt)
    # 分节
    secs, cur_head, cur = [], "", []
    for ln in lines:
        if ln.startswith("## "):
            if cur:
                secs.append((cur_head, cur))
            cur_head, cur = ln[3:].strip(), []
        else:
            cur.append(ln)
    if cur:
        secs.append((cur_head, cur))
    xr, refs, seen = [], [], set()
    for head, body in secs:
        h = head or ""
        is_nonxr = ("非 XR" in h) or ("非XR" in h)
        is_full = ("全量" in h) or ("命中" in h)
        hi, cols = _cols_of(body)
        if hi is None:
            continue
        rows = _parse_rows(body, hi, cols, paper_index)
        for r in rows:
            if r["id"] in seen:
                continue
            if is_nonxr:
                continue
            if is_full and any("新" == c or "新入馆" in c for c in cols) and "✅" not in r["newMark"]:
                continue  # 全量参考节中仅收 ✅ 新入馆行
            seen.add(r["id"])
            if is_ref:
                refs.append(r)
            else:
                xr.append(r)
    # registry 剔除非 XR 归属
    xr = [r for r in xr if (paper_index.get(r["id"]) or {}).get("track") != NONXR]
    refs = [r for r in refs if (paper_index.get(r["id"]) or {}).get("track") != NONXR]
    for lst in (xr, refs):
        for i, r in enumerate(lst):
            r["rank"] = i + 1
    return window, xr, refs


# ---------------- registry → papers ----------------
papers = []
for line in read_text(os.path.join(ROOT, "papers/library/registry.jsonl")).split("\n"):
    line = line.strip()
    if not line:
        continue
    r = json.loads(line)
    papers.append({
        "id": base_id(r["id"]),
        "title": r.get("title", ""),
        "title_zh": r.get("title_zh") or r.get("title", ""),
        "track": r.get("track", "—"),
        "date": r.get("date", ""),
        "batch": r.get("batch", "未标注"),
        "batchLabel": BATCH_LABELS.get(r.get("batch"), r.get("batch", "未标注")),
        "value": r.get("value"),
        "grade": r.get("grade", "C"),
        "scores": {k: int((r.get("scores") or {}).get(k, 0)) for k in DIMS},
        "evidence": r.get("evidence", "ABSTRACT_ONLY"),
        "level": r.get("fetch_level", ""),
        "top10": bool(r.get("in_top10")),
        "flags": list(r.get("flags") or []),
    })
papers.sort(key=lambda p: (p["date"], p["id"]))
paper_index = {p["id"]: p for p in papers}

# ---------------- notes ----------------
def parse_note(path):
    txt = read_text(path)
    m = re.match(r"---\n(.*?)\n---\n?", txt, re.S)
    fm_text, body = (m.group(1), txt[m.end():]) if m else ("", txt)
    fm = {}
    for ln in fm_text.split("\n"):
        mm = re.match(r"^([\w]+):\s*(.*)$", ln)
        if mm:
            fm[mm.group(1)] = mm.group(2).strip().strip('"')
    tags = []
    tm = re.search(r"tags:\s*\[([^\]]*)\]", fm_text)
    if tm:
        tags = [t.strip() for t in tm.group(1).split(",") if t.strip()]
    sections = []
    for mm in re.finditer(r"^##[ \t]+(.+?)\n(.*?)(?=^##[ \t]+|\Z)", body, re.M | re.S):
        sections.append({"h": mm.group(1).strip(), "body": mm.group(2).strip()})
    nid = base_id(fm.get("id", "")) or os.path.basename(path).split("__")[0]
    p = paper_index.get(nid, {})
    return {
        "file": rel(os.path.join(ROOT, "papers/notes", os.path.basename(path))),
        "id": nid,
        "title": fm.get("title") or p.get("title", ""),
        "title_zh": fm.get("title_zh") or p.get("title_zh", ""),
        "track": fm.get("track") or p.get("track", "—"),
        "date": fm.get("date") or p.get("date", ""),
        "batch": p.get("batch", ""),
        "batchLabel": p.get("batchLabel", ""),
        "grade": fm.get("grade") or p.get("grade", "C"),
        "value": float(fm["value"]) if fm.get("value") else p.get("value"),
        "evidence": fm.get("evidence") or p.get("evidence", "ABSTRACT_ONLY"),
        "tags": tags,
        "flags": p.get("flags", []),
        "sections": sections,
    }


notes = [parse_note(p) for p in sorted(glob.glob(os.path.join(ROOT, "papers/notes/*.md")))]
notes.sort(key=lambda n: (n["date"], n["id"]))
note_index = {}
for i, n in enumerate(notes):
    note_index.setdefault(n["id"], i)

# ---------------- MOC 状态注记 ----------------
status_notes = {}
moc_total = os.path.join(ROOT, "papers/MOC/MOC-总索引.md")
if os.path.exists(moc_total):
    for ln in read_text(moc_total).split("\n"):
        m = re.match(r"^>\s*\*\*状态注记（([^）]+)）\*\*：(.+)$", ln.strip())
        if m:
            txt = m.group(2).strip()
            txt = re.sub(r"\[([^\]]+)\]\(([^)]+)\)",
                         lambda mm: '<a href="' + mm.group(2).replace("../../", "../") + '" target="_blank">' + mm.group(1) + "</a>", txt)
            status_notes[m.group(1).strip()] = txt.replace("**", "")


def first_sentence(path, maxlen=200):
    if not os.path.exists(path):
        return ""
    for ln in read_text(path).split("\n"):
        ln = ln.strip().lstrip("-*# ").strip()
        if len(ln) > 12:
            return ln[:maxlen]
    return ""


# ---------------- 每日批次（以各日 7 维表为权威清单） ----------------
RUN_ORDER = {"backfill-2603-2609": ("2026-10-09", 1)}
batches = []
daily_root = os.path.join(ROOT, "papers/daily")
for key in sorted(os.listdir(daily_root)):
    dpath = os.path.join(daily_root, key)
    if not os.path.isdir(dpath):
        continue
    tbl_path = os.path.join(dpath, "7dim-table.md")
    window, rows, ref_rows = parse_daily_table(tbl_path, paper_index) if os.path.exists(tbl_path) else ("", [], [])
    if not window:
        wm = re.search(r"^[>\s]*\**([^\n]{0,200}?(?:提交日|公告日)[^\n]{0,120})", read_text(tbl_path), re.M) if os.path.exists(tbl_path) else None
        if wm:
            window = wm.group(1).strip().strip("*").strip()[:180]
    # 富化：registry 证据/Top10/警示 + 笔记可用性
    def enrich(r):
        p = paper_index.get(r["id"])
        if p:
            r["evidence"] = p["evidence"]
            r["level"] = p["level"]
            r["top10"] = p["top10"] or r.get("top10Mark", False)
            r["flags"] = p["flags"]
        else:
            ev = None
            if "★" in (r.get("evMark") or ""):
                ev = "FULL"
            elif "☆" in (r.get("evMark") or ""):
                ev = "ABSTRACT_ONLY"
            r["evidence"] = ev
            r["level"] = None
            r["top10"] = r.get("top10Mark", False)
            r["flags"] = []
        r.pop("top10Mark", None)
        r.pop("newMark", None)
        r.pop("evMark", None)
        return r
    rows = [enrich(r) for r in rows]
    ref_rows = [enrich(r) for r in ref_rows]
    inreg = sum(1 for r in rows if r["id"] in paper_index)
    grades = {g: sum(1 for r in rows if r["grade"] == g) for g in "SABC"}
    links = {}
    if key.startswith("backfill"):
        cand = {"report": "reports/XR-Backfill-Report-2603-2609.md",
                "moc": "papers/MOC/MOC-backfill-2603-2609.md"}
    else:
        cand = {"report": "reports/XR-Daily-Report-%s.md" % key,
                "moc": "papers/MOC/MOC-%s.md" % key,
                "table": "papers/daily/%s/7dim-table.md" % key,
                "log": "papers/daily/%s/run_log.md" % key}
    for k, v in cand.items():
        fp = os.path.join(ROOT, v)
        if os.path.exists(fp):
            links[k] = rel(fp)
    if not window:
        rl = first_sentence(os.path.join(dpath, key, "run_log.md"))
        window = rl or ("当日无新稿（周末 / API 索引停滞）" if not rows else "")
    sn = status_notes.get(key) or status_notes.get(key + " backfill", "")
    if not sn and not rows:
        sn = first_sentence(os.path.join(dpath, key, "run_log.md"), 240)
    note = ""
    if rows and inreg < len(rows):
        note = "表中 %d 篇，其中 %d 篇已入文献库（%d 篇为历史运行登记遗漏，仅在当日表中留存）" % (len(rows), inreg, len(rows) - inreg)
    if not rows and ref_rows:
        note = "当日无新稿；下表为文献库最新前沿参考（%d 篇，非当日新拉取）" % len(ref_rows)
    batches.append({
        "key": key, "label": BATCH_LABELS.get(key, key), "window": window,
        "count": len(rows), "papers": rows, "refPapers": ref_rows,
        "avg": round(sum(r["value"] for r in rows) / len(rows), 3) if rows else None,
        "max": max((r["value"] for r in rows), default=None),
        "grades": grades, "statusNote": sn, "note": note, "links": links,
        "_sort": RUN_ORDER.get(key, (key, 0)),
    })
batches.sort(key=lambda b: b["_sort"])
# _sort 保留在 JSON 中：前端「每日解读」排序需要（backfill 需依附 10-09 批次之后）

# ---------------- facets / trend ----------------
facets = {"tracks": {}, "batches": [], "noteTracks": {}}
for p in papers:
    facets["tracks"][p["track"]] = facets["tracks"].get(p["track"], 0) + 1
for n in notes:
    facets["noteTracks"][n["track"]] = facets["noteTracks"].get(n["track"], 0) + 1
for b in batches:
    xr_in_reg = sum(1 for p in papers if p["batch"] == b["key"] and p["track"] != NONXR)
    facets["batches"].append({"key": b["key"], "label": b["label"], "n": xr_in_reg})

trend = [{"label": b["label"].split(" · ")[0], "count": b["count"], "avg": b["avg"]}
         for b in batches if b["count"] > 0]

data = {
    "papers": papers, "notes": notes, "batches": batches, "trend": trend,
    "facets": facets, "dimDefs": DIM_DEFS,
    "noteIndex": note_index, "paperIndex": paper_index,
    "meta": {"generated": datetime.datetime.now().strftime("%Y-%m-%d %H:%M")},
}

tpl = read_text(os.path.join(ROOT, "scripts/frontend_template.html"))
payload = json.dumps(data, ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/")
html = tpl.replace("/*__DATA__*/", payload, 1)
out = os.path.join(ROOT, "web/xr-paper-hub.html")
os.makedirs(os.path.dirname(out), exist_ok=True)
with open(out, "w", encoding="utf-8") as f:
    f.write(html)
print("papers:", len(papers), "| notes:", len(notes), "| batches:", len(batches))
print("output:", out, "| size:", round(os.path.getsize(out) / 1024, 1), "KB")
for b in batches:
    print("  %-30s 表内=%-3d  grades=%s avg=%s max=%s" % (
        b["label"], b["count"],
        {g: v for g, v in b["grades"].items() if v}, b["avg"], b["max"]))
