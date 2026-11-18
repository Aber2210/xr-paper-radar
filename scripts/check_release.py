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


def latest_gates():
    files = sorted(glob.glob("data/gates_*.json"))
    if not files:
        return None, None
    p = files[-1]
    m = re.search(r"gates_(\d{4}-\d{2}-\d{2})\.json$", p) or re.search(r"gates_(\d{4})\.json$", p)
    return p, m.group(1) if m else None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--smoke", action="store_true")
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
    gp, gdate = latest_gates()
    g3 = {}
    if gp is None:
        print("G2 留痕：未找到 data/gates_*.json → FAIL")
        fails.append("G2 缺 gates 文件")
    else:
        g = json.load(open(gp, encoding="utf-8"))
        g3 = g.get("gate3", {})
        miss = [k for k in GATE3_KEYS if k not in g3]
        # 2026-11-18 起引入险过口径，四字段随之一并要求
        has_caliber = all(k in g3 for k in CALIBER_KEYS)
        bad_caliber = [k for k in CALIBER_KEYS if k in g3 and k in ("heavy_day_raw", "blockbuster", "s_awarded")
                       and not isinstance(g3[k], bool)]
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
    print("G3 档位：近年批 %d 行 ｜ 本批授予S=%s ｜ backfill记S=%d ｜ 本批泄漏S=%d → %s"
          % (len(rows), eligible, len(s_bf), len(leaked), "PASS" if ok3 else "FAIL"))
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

    if fails:
        for f in fails:
            print("ERROR:", f)
        return 1
    print("RELEASE GATE: PASS —— 可以打标签")
    return 0


if __name__ == "__main__":
    sys.exit(main())
