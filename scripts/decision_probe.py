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
    for src in (pool, nonxr):
        for k, v in src.items():
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
        out.append({"id": r["id"], "group": r["group"], "label": r["label"], "pred": pred,
                    "ok": pred == r["label"], "title": r["title"][:80]})

    print("\n%-12s %5s %8s %10s" % ("group", "n", "accuracy", "漏判(正例判0)"))
    summary = {}
    for g in ("accepted", "rejected", "kw-missed"):
        sub = [x for x in out if x["group"] == g]
        if not sub:
            continue
        acc = sum(x["ok"] for x in sub) / len(sub)
        killed = sum(1 for x in sub if x["label"] == 1 and x["pred"] == 0)
        summary[g] = {"n": len(sub), "acc": round(acc, 4), "missed_pos": killed}
        print("%-12s %5d %8.4f %10d" % (g, len(sub), acc, killed))

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
    a = ap.parse_args()
    if a.cmd == "build":
        return build(a.mmdd)
    if a.cmd == "run":
        return run(a.mmdd, a.backend, a.limit)
    return emit(a.mmdd, a.limit)


if __name__ == "__main__":
    sys.exit(main())
