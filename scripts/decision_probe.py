# -*- coding: utf-8 -*-
"""decision_probe.py —— 判定复核探针（后端可插拔，先定问题、后选模型）

背景：本项目的「剔除」是唯一「错了就永久丢失」的判定——被剔的稿子不会出现在任何产物里。
本探针把这一步写成**固定的、可复现的问题**（TypeSafe Jev 的 noul 题型语义：是/否 + 概率），
后端可以是 Jev、普通 LLM、或本地规则；换后端不改问题定义，指标才可比。

三个子命令：
    build   从本批甄别数据构建 golden set（含标签来源与可信度）
    run     跑一个后端并出指标
    emit    打印可直接投给 TypeSafe /v1/systemone 的请求体（离线预览，不发网络）

诚实约束（写在代码里，不靠自觉）：
  * golden 分三组，标签可信度不同，指标**分组报**，不许合并成一个好看的数字；
  * `rejected` 组是「被检验的判定自己做的标」，属循环证据，只做一致性参考；
  * `kw-missed` 组从未被任何模型逐篇判定，是最接近真实的召回检验；
  * 探针只报警、不改判：输出的 flag 清单交人看，不回写 registry。

用法：
    python scripts/decision_probe.py build 1118
    python scripts/decision_probe.py run 1118 --backend stub-kw
    python scripts/decision_probe.py emit 1118 --limit 2
"""
import argparse
import hashlib
import json
import os
import random
import re
import sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
os.chdir(ROOT)
OUT_DIR = "data/decision"

# ---- 问题定义：与后端无关，改动需记版本 ----
QUESTION = {
    "type": "noul",
    "instructions": (
        "该论文是否与 AR/VR/MR/XR 相关？判定为相关需满足：论文的研究对象或核心方法服务于"
        "沉浸式显示（头显/眼镜/光波导/近眼显示）、空间交互与追踪、三维重建与神经渲染、"
        "化身与人体建模、触觉与遥操作、XR 系统/平台/评估，或上述场景的数据集与基准。"
        "仅为通用视觉/图形学方法、未面向沉浸式或空间场景者判为不相关。"
    ),
}
QUESTION_VERSION = "q1-2026-11-18"

# 仅供 stub-kw 后端做「管道连通性」自检，不代表任何模型能力
XR_TERMS = ("virtual reality", "augmented reality", "mixed reality", "extended reality",
            "xr ", " vr ", " ar ", " mr ", "head-mounted", "hmd", "headset", "waveguide",
            "near-eye", "stereoscopic", "immersive", "teleoperation", "avatar",
            "haptic", "tactile", "hand pose", "hand tracking", "gaze", "3d gaussian",
            "neural rendering", "novel view synthesis", "slam", "point cloud")


def load(mmdd, name, default=None):
    p = "data/%s_%s.json" % (name, mmdd)
    if not os.path.exists(p):
        return default
    return json.load(open(p, encoding="utf-8"))


def build(mmdd):
    os.makedirs(OUT_DIR, exist_ok=True)
    scored = load(mmdd, "scored") or []
    pool = load(mmdd, "xr_pool") or {}
    nonxr = load(mmdd, "nonxr") or {}
    rejected = set(load(mmdd, "rejected") or [])

    meta = {}
    # 摘要只存在于候选池/补录数据里：scored_1118.json 只带标题与评分
    for name in ("xr_pool", "nonxr", "cand_main", "cand_bf", "old_replace"):
        for k, v in (load(mmdd, name) or {}).items():
            meta[k] = v

    rows = []
    # A. 已定稿（经全文精读后入馆）→ 可信正例
    for p in scored:
        pid = p["id"]
        m = meta.get(pid, {})
        rows.append({"id": pid, "title": p.get("title") or m.get("title", ""),
                     "abstract": (p.get("abstract") or m.get("abstract", ""))[:1200],
                     "label": 1, "group": "accepted", "label_status": "confirmed"})
    # B. 被剔除的候选（模型自己判的）→ 循环证据
    for pid in sorted(rejected):
        m = meta.get(pid, {})
        rows.append({"id": pid, "title": m.get("title", ""),
                     "abstract": m.get("abstract", "")[:1200],
                     "label": 0, "group": "rejected", "label_status": "provisional-circular"})
    # C. 关键词层根本没命中的稿子 → 从未被逐篇判定，最接近真实召回检验
    cand = [k for k in sorted(nonxr) if k not in rejected]
    random.Random(20261118).shuffle(cand)
    for pid in cand[:100]:
        m = nonxr[pid]
        rows.append({"id": pid, "title": m.get("title", ""),
                     "abstract": m.get("abstract", "")[:1200],
                     "label": 0, "group": "kw-missed", "label_status": "provisional-unverified"})

    path = os.path.join(OUT_DIR, "golden_%s.jsonl" % mmdd)
    with open(path, "w", encoding="utf-8") as f:
        for r in rows:
            r["q"] = QUESTION_VERSION
            r["cat"] = meta.get(r["id"], {}).get("cat", "")
            f.write(json.dumps(r, ensure_ascii=False) + "\n")
    n = {g: sum(1 for r in rows if r["group"] == g) for g in ("accepted", "rejected", "kw-missed")}
    print("golden -> %s 共 %d 条：accepted %d / rejected %d / kw-missed %d"
          % (path, len(rows), n["accepted"], n["rejected"], n["kw-missed"]))
    print("问题版本 %s（改动问题定义必须换版本，否则跨版本指标不可比）" % QUESTION_VERSION)
    return 0


def read_golden(mmdd):
    p = os.path.join(OUT_DIR, "golden_%s.jsonl" % mmdd)
    if not os.path.exists(p):
        print("缺少 %s，先跑 build" % p)
        sys.exit(2)
    return [json.loads(l) for l in open(p, encoding="utf-8") if l.strip()]


def backend_stub(row):
    """管道自检用：关键词命中即判相关。不要用它的指标评价任何模型。"""
    t = (" " + (row["title"] + " " + row["abstract"]).lower() + " ")
    return 1 if any(k in t for k in XR_TERMS) else 0


def backend_file(row, table):
    return int(table.get(row["id"], 0))


def run(mmdd, backend, limit=None):
    rows = read_golden(mmdd)
    if limit:
        rows = rows[:limit]
    table = {}
    if backend.startswith("file:"):
        table = json.load(open(backend.split(":", 1)[1], encoding="utf-8"))
    out = []
    for r in rows:
        pred = backend_file(r, table) if backend.startswith("file:") else backend_stub(r)
        lab = r.get("label")
        out.append({"id": r["id"], "group": r["group"], "label": lab, "pred": pred,
                    "ok": (None if lab is None else pred == lab), "title": r["title"][:80]})

    print("\n%-12s %5s %5s %8s %10s" % ("group", "n", "判不准", "accuracy", "漏判(正例判0)"))
    summary = {}
    for g in ("accepted", "rejected", "kw-missed"):
        sub = [x for x in out if x["group"] == g]
        if not sub:
            continue
        graded = [x for x in sub if x["ok"] is not None]      # 人工标「不确定」的不进分母
        acc = (sum(x["ok"] for x in graded) / len(graded)) if graded else None
        killed = sum(1 for x in graded if x["label"] == 1 and x["pred"] == 0)
        summary[g] = {"n": len(sub), "n_unsure": len(sub) - len(graded),
                      "acc": (round(acc, 4) if acc is not None else None), "missed_pos": killed}
        print("%-12s %5d %5d %8s %10d"
              % (g, len(sub), len(sub) - len(graded),
                 ("%.4f" % acc) if acc is not None else "—", killed))

    # 探针的真正产出：不一致清单（只报警，不改判）
    flags = [x for x in out if x["group"] == "kw-missed" and x["pred"] == 1]
    print("\nkw-missed 中被判相关（可能的关键词表缺口）：%d 条" % len(flags))
    for x in flags[:8]:
        print("   +", x["id"], x["title"])

    path = os.path.join(OUT_DIR, "probe_%s_%s.json" % (mmdd, re.sub(r"\W", "_", backend)))
    json.dump({"question_version": QUESTION_VERSION, "backend": backend, "question": QUESTION,
               "summary": summary, "items": out, "flags": [x["id"] for x in flags]},
              open(path, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print("\n结果 -> %s（%d 条）" % (path, len(out)))
    return 0


def _hits(row):
    t = row["title"].lower()
    a = row["abstract"].lower()
    return sum(3 for k in XR_TERMS if k in t) + sum(1 for k in XR_TERMS if k in a)


def sheet(mmdd, per_group=20):
    """生成人工标注表：每组一半取「边界项」（最有信息量），一半随机（避免选择偏差）。

    每条给出**完整摘要**（不是首句）与 arXiv 链接——判定需要的信息必须给够，
    截断是我早期为了表格好看做的，会让本来可判的条目变得不可判。
    """
    rows = [r for r in read_golden(mmdd) if r["group"] in ("accepted", "kw-missed")]
    rnd = random.Random(20261118)
    picked = []
    for g, reverse in (("accepted", False), ("kw-missed", True)):
        grp = [r for r in rows if r["group"] == g]
        grp.sort(key=lambda r: (_hits(r), r["id"]), reverse=reverse)
        half = per_group // 2
        boundary = grp[:half]
        rest = [r for r in grp[half:] if r["id"] not in {x["id"] for x in boundary}]
        rnd.shuffle(rest)
        picked.extend([(r, "边界") for r in boundary] + [(r, "随机") for r in rest[:half]])

    path = os.path.join(OUT_DIR, "labeling_%s.md" % mmdd)
    L = ["# 判定标注表 %s（问题版本 %s）\n" % (mmdd, QUESTION_VERSION),
         "## 判定规则（按规则判，不按感觉判）\n",
         "- **判 1（相关）**：论文的研究对象、被评估场景、硬件或用户任务中，**至少有一项属于**沉浸式/空间场景"
         "（头显、AR/VR 应用、空间交互、沉浸式内容与渲染、化身、触觉/遥操作、XR 系统与评估）。",
         "- **判 0（不相关）**：仅为通用视觉/图形/机器人方法，XR 只是**可能的迁移方向**而非论文的研究对象或评估场景。",
         "- **判 ?（不确定）**：两条规则都能说得通，或摘要信息确实不足以判断。**宁可标 ?，不要猜**——"
         "? 会从分母里剔除，不影响指标；猜错会污染基线。\n",
         "## 怎么填\n",
         "- 每条末尾有一行 `判定：`，在后面填 `1` / `0` / `?` 即可，其余不要动。",
         "- 摘要已给全文（不截断）；仍拿不准就点 arXiv 链接看全文——**标注可以看全文，模型不可以**。",
         "- `边界`／`随机` 是我抽样时的标记，**不是答案**。\n",
         "---\n"]
    for i, (r, tag) in enumerate(picked, 1):
        L.append("### %d · %s · %s\n" % (i, r["id"], r["title"].strip()))
        L.append("- 类别：%s ｜ 抽样：%s ｜ 组：%s" % (r.get("cat") or "—", tag, r["group"]))
        L.append("- 摘要：%s" % " ".join(r["abstract"].split()))
        L.append("- 链接：https://arxiv.org/abs/%s" % r["id"])
        L.append("- **判定：** \n")
    L.append("---\n\n> 共 %d 条。填完后：`python scripts/decision_probe.py ingest %s data/decision/labeling_%s.md`\n"
             % (len(picked), mmdd, mmdd))
    open(path, "w", encoding="utf-8").write("\n".join(L) + "\n")
    n_acc = sum(1 for r, _t in picked if r["group"] == "accepted")
    print("标注表 -> %s（%d 条：accepted %d / kw-missed %d）" % (path, len(picked), n_acc, len(picked) - n_acc))
    return 0


def ingest(mmdd, path):
    """把每条 `判定：` 后的 1/0/? 回写进 golden，标签来源记为人工确认。"""
    rows = read_golden(mmdd)
    idx = {r["id"]: r for r in rows}
    n1 = n0 = nq = 0
    cur = None
    for ln in open(path, encoding="utf-8"):
        m = re.match(r"^###\s+\d+\s+·\s+([0-9]{4}\.[0-9]{4,5})", ln.strip())
        if m:
            cur = m.group(1)
            continue
        m = re.match(r"^[-*]?\s*\**判定[:：]\**\s*([10?]|相关|不相关|不确定)\s*$", ln.strip())
        if not m or cur not in idx:
            continue
        v = {"相关": "1", "不相关": "0", "不确定": "?"}.get(m.group(1), m.group(1))
        idx[cur]["label"] = {"1": 1, "0": 0, "?": None}[v]
        idx[cur]["label_status"] = "uncertain-human" if v == "?" else "confirmed-human"
        n1 += v == "1"; n0 += v == "0"; nq += v == "?"
    with open(os.path.join(OUT_DIR, "golden_%s.jsonl" % mmdd), "w", encoding="utf-8") as f:
        for r in rows:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")
    print("回写完成：相关 %d / 不相关 %d / 不确定 %d（共 %d 条已人工标注）"
          % (n1, n0, nq, n1 + n0 + nq))
    return 0


def emit(mmdd, limit):
    rows = read_golden(mmdd)[:limit]
    for r in rows:
        body = {"model": "jev-latest",
                "state": "标题：%s\n摘要：%s" % (r["title"], r["abstract"]),
                "questions": {"is_xr": QUESTION}}
        print(json.dumps(body, ensure_ascii=False, indent=1))
        print("-" * 60)
    print("把 questions 固定为上面这份定义；换后端（Jev / LLM adapter）只改 transport，不改问题。")
    return 0


def main():
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)
    b = sub.add_parser("build"); b.add_argument("mmdd")
    r = sub.add_parser("run"); r.add_argument("mmdd")
    r.add_argument("--backend", default="stub-kw"); r.add_argument("--limit", type=int)
    e = sub.add_parser("emit"); e.add_argument("mmdd"); e.add_argument("--limit", type=int, default=2)
    s = sub.add_parser("sheet"); s.add_argument("mmdd"); s.add_argument("--per-group", type=int, default=20)
    i = sub.add_parser("ingest"); i.add_argument("mmdd"); i.add_argument("path")
    a = ap.parse_args()
    if a.cmd == "build":
        return build(a.mmdd)
    if a.cmd == "run":
        return run(a.mmdd, a.backend, a.limit)
    if a.cmd == "sheet":
        return sheet(a.mmdd, a.per_group)
    if a.cmd == "ingest":
        return ingest(a.mmdd, a.path)
    return emit(a.mmdd, a.limit)


if __name__ == "__main__":
    sys.exit(main())
