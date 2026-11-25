# -*- coding: utf-8 -*-
"""check_release.py —— 打标签前的发布门（与 README「版本与回滚」一致）

三条硬门，任一不过即 exit 1：
  G1 计数一致：registry 行数 / notes 文件数 / daily 目录数 == web/xr-paper-hub.html 的 DATA
  G2 留痕齐全：最近一批 data/gates_<日期>.json 必须带门③ 口径字段
  G3 档位自洽：≥4.20 的 S 只在「本批授予 S」时出现；backfill 永不记 S

用法：
    python scripts/check_release.py            # G1-G3
    python scripts/check_release.py --smoke    # 追加前端冒烟（调用 smoke_hub.mjs，约 20s）
"""
import argparse
import datetime
import glob
import json
import os
import re
import subprocess
import sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
os.chdir(ROOT)

GATE3_KEYS = ("window_excludes_today", "window_excludes_this_run_batches",
              "this_run_batches_excluded")
CALIBER_KEYS = ("heavy_day_raw", "margin", "blockbuster", "s_awarded")


def load_data_counts():
    html = open("web/xr-paper-hub.html", encoding="utf-8", errors="replace").read()
    i = html.index("const DATA = ") + len("const DATA = ")
    j = html.index(";\n</script>", i)
    d = json.loads(html[i:j].replace("<\\/", "</"))
    return len(d["papers"]), len(d["notes"]), len(d["batches"])


def latest_gates(batch=None):
    """返回 (路径, 批次日期 YYYY-MM-DD)；传 batch（YYYY-MM-DD）可指定某一天，用于补记状态日。

    批次日**必须读文件内容里的 gate3.window_hi**：实际文件名是 gates_MMDD.json（如 gates_1119.json），
    早期版本用文件名正则只认 gates_YYYY-MM-DD.json，回退成 "1119"，导致下游 `batch` 与
    `backfill-<MMDD>` 全部拼错 —— G3 的「本批泄漏 S」检查一直在空跑（2026-11-19 自查发现）。
    """
    files = glob.glob("data/gates_*.json")
    if not files:
        return None, None
    # 按**文件内容里的批次日**取最大，而不是按文件名排序取最后一个：
    # 2026-11-20 曾出现 `gates_2026-11-20.json`，字典序永远排最后，会遮蔽后续所有
    # `gates_MMDD.json`，让 G2/G3 静默跑在错的文件上（STATUS C-10）。
    cand = []
    for p in files:
        d = None
        try:
            g = json.load(open(p, encoding="utf-8"))
            d = (g.get("gate3") or {}).get("window_hi") or g.get("date")
        except Exception:
            pass
        if not (isinstance(d, str) and re.fullmatch(r"\d{4}-\d{2}-\d{2}", d)):
            m = re.search(r"gates_(\d{2})(\d{2})\.json$", p)
            d = "2026-%s-%s" % m.groups() if m else None
        if d:
            cand.append((p, d))
    if batch:
        for p, d in cand:
            if d == batch:
                return p, d
        return None, batch
    return max(cand, key=lambda x: x[1]) if cand else (sorted(files)[-1], None)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--smoke", action="store_true")
    ap.add_argument("--record", action="store_true", help="把判决追加到 data/verdicts.jsonl（按批次幂等）")
    ap.add_argument("--batch", help="指定批次日 YYYY-MM-DD（默认取最新），用于补记状态日")
    args = ap.parse_args()
    fails = []

    # G1
    reg = sum(1 for l in open("papers/library/registry.jsonl", encoding="utf-8") if l.strip())
    notes = len(glob.glob("papers/notes/*.md"))
    daily = len([d for d in os.listdir("papers/daily") if os.path.isdir(os.path.join("papers/daily", d))])
    dp, dn, db = load_data_counts()
    ok1 = (reg, notes, daily) == (dp, dn, db)
    print("G1 计数：registry %d / notes %d / daily %d ｜ DATA %d/%d/%d → %s"
          % (reg, notes, daily, dp, dn, db, "PASS" if ok1 else "FAIL"))
    if not ok1:
        fails.append("G1 计数与前端 DATA 不一致")

    # G2
    gp, gdate = latest_gates(args.batch)
    g3 = {}
    status_day = False
    if gp is None:
        print("G2 留痕：未找到 data/gates_*.json → FAIL")
        fails.append("G2 缺 gates 文件")
    else:
        g = json.load(open(gp, encoding="utf-8"))
        g3 = g.get("gate3", {})
        # 状态日（0 新稿）：门③ 无 today_max/margin，四字段天然不存在，不能按缺失判 FAIL
        status_day = (g.get("run_type") == "status_day") or (g3.get("today_max") is None)
        miss = [k for k in GATE3_KEYS if k not in g3]
        # 2026-11-18 起引入险过口径，四字段随之一并要求
        has_caliber = all(k in g3 for k in CALIBER_KEYS)
        bad_caliber = [k for k in CALIBER_KEYS if k in g3 and k in ("heavy_day_raw", "blockbuster", "s_awarded")
                       and not isinstance(g3[k], bool)]
        if status_day:
            ok2 = not miss
            print("G2 留痕：%s 状态日（0 新稿）→ 门③ 不适用，验窗口字段 %s → %s"
                  % (os.path.basename(gp), "齐" if ok2 else ("缺 %s" % miss), "PASS" if ok2 else "FAIL"))
        else:
            ok2 = not miss and (has_caliber or "blockbuster" not in g3) and not bad_caliber
            print("G2 留痕：%s 缺 %s ｜ 险过四字段 %s → %s"
                  % (os.path.basename(gp), miss or "无", "齐" if has_caliber else "不适用/缺", "PASS" if ok2 else "FAIL"))
        if not ok2:
            fails.append("G2 %s 留痕不全" % os.path.basename(gp))

    # G3
    eligible = None
    if g3:
        eligible = bool(g3.get("blockbuster", g3.get("heavy_day")))
    rows = [json.loads(l) for l in open("papers/library/registry.jsonl", encoding="utf-8") if l.strip()]
    s_high = [r for r in rows if r.get("grade") == "S" and r.get("value", 0) >= 4.2]
    s_bf = [r for r in rows if r.get("grade") == "S" and str(r.get("batch", "")).startswith("backfill")]
    # 若最近一批未授予 S，则本批不应存在 S
    this_batch = []
    if gdate:
        mmdd = gdate[5:7] + gdate[8:10] if "-" in gdate else gdate[4:]
        this_batch = [r for r in rows if r.get("batch") in (gdate, "backfill-" + mmdd)]
    leaked = [r["id"] for r in this_batch if r.get("grade") == "S"] if eligible is False else []
    ok3 = not s_bf and not leaked
    print("G3 档位：近年批 %d 行 ｜ 本批授予S=%s ｜ backfill记S=%d ｜ 本批泄漏S=%d%s → %s"
          % (len(rows), eligible, len(s_bf), len(leaked),
             "（状态日，本批无新稿）" if status_day else "", "PASS" if ok3 else "FAIL"))
    if not ok3:
        fails.append("G3 档位自洽失败：backfill记S=%s 泄漏=%s" % ([r["id"] for r in s_bf], leaked))

    # 附加：冒烟
    if args.smoke:
        p = subprocess.run(["node", "scripts/smoke_hub.mjs", "9466"], capture_output=True, text=True)
        tail = [l for l in (p.stdout or "").splitlines() if l.startswith("SMOKE:")]
        ok4 = p.returncode == 0 and tail and tail[-1].endswith("PASS")
        print("G4 冒烟：%s → %s" % (tail[-1] if tail else "无输出", "PASS" if ok4 else "FAIL"))
        if not ok4:
            fails.append("G4 前端冒烟未通过")

    # R 残差复核（诊断项：不阻塞发布，超阈值记 WARN）
    warns, resid_rate = [], None
    if status_day:
        print("R 残差复核：状态日 0 新稿 → 不适用（无 nonxr 池可扫）")
    elif gdate:
        rp = "data/residual_%s.json" % (gdate[5:7] + gdate[8:10])
        if os.path.exists(rp):
            rd = json.load(open(rp, encoding="utf-8"))
            resid_rate = rd.get("rate")
            print("R 残差复核：扫描 %s 条、疑似漏检 %s 条（%.1f%%）→ %s"
                  % (rd.get("n_scanned", 0), rd.get("n_flagged", 0), 100 * (resid_rate or 0),
                     "WARN" if (resid_rate or 0) > 0.12 else "OK"))
            if (resid_rate or 0) > 0.12:
                warns.append("残差漏检率 %.1f%% > 12%%（连续 3 日需上报）" % (100 * resid_rate))
        else:
            print("R 残差复核：未见 data/residual_%s.json → 未执行" % (gdate[5:7] + gdate[8:10]))
            warns.append("第 3.5 步残差复核未执行")

    # 判决：FAIL > WARN > N/A（状态日）> PASS
    level = "FAIL" if fails else ("WARN" if warns else ("N/A" if status_day else "PASS"))
    for f in fails:
        print("ERROR:", f)
    for w in warns:
        print("WARN :", w)
    print("VERDICT: %s%s" % (level, "" if level == "PASS" else " —— 见上方逐条原因"))

    if args.record:
        rec = {"batch": gdate, "verdict": level, "status_day": status_day,
               "counts": {"papers": reg, "notes": notes, "batches": daily},
               "gate3": {k: g3.get(k) for k in ("top10_mean", "today_max", "margin", "blockbuster", "s_awarded")},
               "residual_rate": resid_rate, "reasons": fails + warns,
               "at": datetime.datetime.now().strftime("%Y-%m-%d %H:%M")}
        path = "data/verdicts.jsonl"
        hist = []
        if os.path.exists(path):
            hist = [json.loads(l) for l in open(path, encoding="utf-8") if l.strip()]
        hist = [r for r in hist if r.get("batch") != gdate] + [rec]
        hist.sort(key=lambda r: r.get("batch") or "")
        with open(path, "w", encoding="utf-8") as f:
            for r in hist:
                f.write(json.dumps(r, ensure_ascii=False) + "\n")
        print("判决已记账 -> %s（共 %d 批）" % (path, len(hist)))

    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
