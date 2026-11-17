# -*- coding: utf-8 -*-
"""check_audit_guard.py —— 对账脚本「失败即拒绝写盘」守卫校验器（R-03 的守卫式收口）

背景：漏网对账脚本会写出 `*missed*.json`，其语义是「这些稿子没进库」。一旦采集本身失败
（某分类 get 重试耗尽、或某日期段实采 < declared），写出的空/残缺 missed 与「真的 0 漏网」
完全同形，下游只会看到「0 漏网」。2026-11-17 复评把这条记为 F-05/N-09，但当时只在
`audit_listing_1117.py` 一份里修好；库内另外 18 份同源代码仍带缺陷。

本校验器不重构那 18 份（它们是按日冻结的一次性脚本，产物已发布，重写只会扩大 diff），
而是立一条**只减不增**的基线：
  * 不在基线里的脚本：必须带守卫，否则校验失败（拦住新批次的复制粘贴）；
  * 在基线里的脚本：必须仍存在且仍无守卫，否则报「基线过期」——
    这意味着有人把它修好了（或删了），必须同步从基线删除，基线只能变小。

守卫的规范形态（写在任何 missed 写盘之前）：

    if ok_cats < len(CATS):        # 或 ok_cats != len(CATS) / len(cats)
        print("FATAL: ...", flush=True)
        sys.exit(2)

用法：
    python scripts/check_audit_guard.py           # 校验，失败退出码 1
    python scripts/check_audit_guard.py -v        # 附每份脚本的判定明细
"""
import glob
import json
import os
import re
import sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
BASELINE = os.path.join(ROOT, "scripts/audit_guard_baseline.json")
PATTERNS = ("scripts/audit_listing_*.py", "scripts/audit_gap_listing*.py")

# 守卫：if ok_cats < len(X): ... sys.exit(非零)
GUARD_RE = re.compile(r"if\s+ok_cats\s*(?:<|!=)\s*len\(\s*\w+\s*\)")
DUMP_RE = re.compile(r"json\.dump\(")


def write_point(src):
    """返回「第一个把 missed 写出去的 json.dump」的位置；无则 None。

    以 `json.dump(` 后 300 字符内是否出现 missed 判定——因为写盘变量名在库内有三代
    （missed / missed_prev / group），只有文件名与键名稳定含 missed。
    """
    for m in DUMP_RE.finditer(src):
        if "missed" in src[m.start():m.start() + 300]:
            return m.start()
    return None


def guarded(src, wp):
    """守卫必须出现在写盘点**之前**，且带非零退出。"""
    for m in GUARD_RE.finditer(src):
        if wp is not None and m.start() > wp:
            continue
        if re.search(r"sys\.exit\(\s*[1-9]", src[m.end():m.end() + 500]):
            return True
    return False


def main():
    verbose = "-v" in sys.argv[1:]
    base = {"legacy_unguarded": []}
    if os.path.exists(BASELINE):
        base = json.load(open(BASELINE, encoding="utf-8"))
    legacy = {p.replace("\\", "/") for p in base.get("legacy_unguarded", [])}

    files = []
    for pat in PATTERNS:
        files.extend(glob.glob(os.path.join(ROOT, pat)))
    files = sorted({os.path.relpath(f, ROOT).replace("\\", "/") for f in files})

    errors, seen_legacy = [], set()
    rows = []
    for rel in files:
        src = open(os.path.join(ROOT, rel), encoding="utf-8").read()
        wp = write_point(src)
        if wp is None:                       # 不写 missed 的脚本不在本校验范围
            if verbose:
                rows.append((rel, "skip", "不写 missed"))
            continue
        ok = guarded(src, wp)
        is_legacy = rel in legacy
        if is_legacy:
            seen_legacy.add(rel)
            if ok:
                errors.append("%s 已带守卫，但仍在基线里 —— 请从 audit_guard_baseline.json 删除该条" % rel)
        elif not ok:
            errors.append("%s 写出 missed 但缺写盘守卫（须在某次 json.dump 之前 "
                          "if ok_cats < len(CATS): ... sys.exit(2)）" % rel)
        rows.append((rel, "legacy" if is_legacy else ("guard" if ok else "MISSING"), ""))

    for rel in sorted(legacy - seen_legacy):
        errors.append("基线条目 %s 不存在或已不再写 missed —— 请从基线删除（基线只减不增）" % rel)

    if verbose:
        for rel, state, note in rows:
            print("  %-34s %-8s %s" % (rel, state, note))
    n_guard = sum(1 for _, s, _ in rows if s == "guard")
    n_legacy = sum(1 for _, s, _ in rows if s == "legacy")
    print("对账脚本 %d 份：带守卫 %d、基线豁免 %d、违规 %d"
          % (len([r for r in rows if r[1] != "skip"]), n_guard, n_legacy, len(errors)))
    if errors:
        for e in errors:
            print("ERROR:", e)
        return 1
    print("PASS: 无新增缺失守卫的对账脚本，基线未过期")
    return 0


if __name__ == "__main__":
    sys.exit(main())
