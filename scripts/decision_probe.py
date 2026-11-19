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
# 口径沿革：
#   q1（2026-11-18 上午）「设备/沉浸式」窄口径——用户标注后发现它比库的收录口径窄：
#      入库 20 条里仅 4 条判相关，被判 0 的 16 篇却分布在库内自有赛道
#      （神经渲染 3 / 化身与人体 3 / 感知与认知 2 …）。不是流水线收错，是我把问题写窄了。
#   q2（2026-11-18 晚，用户裁定 B）改为**库的收录口径**：属于下列任一赛道即判 1。
TRACKS = {
    "神经渲染": "NeRF / 3DGS / 神经场 / 可微渲染 / 新视角合成",
    "渲染与显示": "渲染管线、显示硬件（波导 / 近眼 / 光场）、实时渲染系统",
    "重建与SLAM": "SfM / SLAM / 深度与位姿估计 / 点云与网格重建",
    "化身与人体": "人体 / 手 / 脸建模与驱动、化身、动作捕捉",
    "交互与输入": "手势 / 眼动 / 控制器 / 文本输入等空间交互范式",
    "触觉与多模态": "触觉显示与感知、力反馈、多模态融合",
    "内容生成": "面向 3D / 场景 / 视频的生成与编辑（赛道较宽，通用多模态生成应用也可能落在此处，归属可能多义）",
    "世界模型与仿真": "物理仿真、交互式世界模型、场景模拟",
    "感知与认知": "场景理解、视觉定位、用户感知与认知研究",
    "空间计算与UI": "空间布局、UI 放置、空间锚点与协作",
    "系统与平台": "XR 系统架构、性能与延迟、设备与工具链",
    "评估与数据集": "基准、数据集、评测方法",
}

QUESTION = {
    "type": "noul",
    "instructions": (
        "该论文是否属于下列任一收录赛道？属于判相关（1），完全落在通用视觉/自然语言/机器人/医学"
        "等领域且不对应任何赛道者判不相关（0）。赛道及其范围："
        + "；".join("%s（%s）" % (k, v) for k, v in TRACKS.items()) + "。"
    ),
    "track_scope": TRACKS,
}
QUESTION_VERSION = "q2.1-2026-11-19"   # q2.1 仅澄清「内容生成」边界，不改变任何已标注判定

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
                    "ok": (None if lab is None else pred == lab), "abs_ok": r.get("abs_sufficient"),
                    "title": r["title"][:80]})

    print("\n%-12s %5s %5s %8s %10s %9s"
          % ("group", "n", "判不准", "accuracy", "漏判(正例判0)", "公平子集"))
    summary = {}
    for g in ("accepted", "rejected", "kw-missed"):
        sub = [x for x in out if x["group"] == g]
        if not sub:
            continue
        graded = [x for x in sub if x["ok"] is not None]      # 人工标「不确定」的不进分母
        acc = (sum(x["ok"] for x in graded) / len(graded)) if graded else None
        killed = sum(1 for x in graded if x["label"] == 1 and x["pred"] == 0)
        # 公平子集：人工标注时**没标**「摘要不足」的条目。摘要不足的条目，任何只看摘要的
        # 模型都不可能判对，把它们算进准确率等于拿信息缺失惩罚模型。
        fair = [x for x in graded if x["abs_ok"] is not False]
        acc_fair = (sum(x["ok"] for x in fair) / len(fair)) if fair else None
        summary[g] = {"n": len(sub), "n_unsure": len(sub) - len(graded),
                      "acc": (round(acc, 4) if acc is not None else None),
                      "n_abs_short": len([x for x in sub if x["abs_ok"] is False]),
                      "acc_fair": (round(acc_fair, 4) if acc_fair is not None else None),
                      "missed_pos": killed}
        print("%-12s %5d %5d %8s %10s %9s"
              % (g, len(sub), len(sub) - len(graded),
                 ("%.4f" % acc) if acc is not None else "—", killed,
                 ("%.4f" % acc_fair) if acc_fair is not None else "—"))

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
         "## 判定规则：属于下列任一赛道即判 1\n",
         "| 赛道 | 覆盖范围 |", "|---|---|"]
    for k, v in TRACKS.items():
        L.append("| %s | %s |" % (k, v))
    L += ["\n- **判 1**：论文的研究对象或方法**会被收进**上述任一类（按你日常收稿的判断）。",
          "- **判 0**：完全落在通用视觉/自然语言/机器人/医学等领域，不对应任何一类。",
          "- **判 ?**：读完也说不清该归哪一类——这类我会拿去改赛道定义，不改标签。\n",
          "## 怎么填\n",
          "- 每条末尾两行：`判定：` 填 `1` / `0` / `?`；`摘要是否足够：` 填 `是` / `否`。",
          "- **标注以「这篇到底该不该收」为准——摘要看不出来就点 arXiv 链接读全文**，目标是真值，"
          "不是复刻模型的视野。",
          "- 「摘要是否足够」决定模型评测的公平分母：标「否」的条目，只看摘要的模型不可能判对。",
          "- 「你在窄口径(q1)下判的是」是你自己的上一轮判断，仅供对照，**请按新口径重新判**。\n",
          "---\n"]
    for i, (r, tag) in enumerate(picked, 1):
        L.append("### %d · %s · %s\n" % (i, r["id"], r["title"].strip()))
        L.append("- 类别：%s ｜ 抽样：%s ｜ 组：%s" % (r.get("cat") or "—", tag, r["group"]))
        L.append("- 摘要：%s" % " ".join(r["abstract"].split()))
        L.append("- 链接：https://arxiv.org/abs/%s" % r["id"])
        if r.get("label_q1") is not None:
            L.append("- 你在窄口径(q1)下判的是：**%d**" % r["label_q1"])
        L.append("- **判定：** （填 1 / 0 / ?）")
        L.append("- 摘要是否足够： （是 / 否 —— 填「否」表示必须看全文才敢定）\n")
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
    n1 = n0 = nq = na = 0
    cur = None
    for ln in open(path, encoding="utf-8"):
        m = re.match(r"^###\s+\d+\s+·\s+([0-9]{4}\.[0-9]{4,5})", ln.strip())
        if m:
            cur = m.group(1)
            continue
        m = re.match(r"^[-*]?\s*\**判定[:：]\**\s*([10?]|相关|不相关|不确定)\s*$", ln.strip())
        if m and cur in idx:
            v = {"相关": "1", "不相关": "0", "不确定": "?"}.get(m.group(1), m.group(1))
            idx[cur]["label"] = {"1": 1, "0": 0, "?": None}[v]
            idx[cur]["label_status"] = "uncertain-human" if v == "?" else "confirmed-human"
            n1 += v == "1"; n0 += v == "0"; nq += v == "?"
            continue
        m = re.match(r"^[-*]?\s*\**摘要是否足够[:：]\**\s*(是|否)\s*$", ln.strip())
        if m and cur in idx:
            idx[cur]["abs_sufficient"] = (m.group(1) == "是")
            na += m.group(1) == "否"
    with open(os.path.join(OUT_DIR, "golden_%s.jsonl" % mmdd), "w", encoding="utf-8") as f:
        for r in rows:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")
    print("回写完成：相关 %d / 不相关 %d / 不确定 %d ｜ 其中「摘要不足需看全文」 %d 条（共 %d 条已人工标注）"
          % (n1, n0, nq, na, n1 + n0 + nq))
    return 0


def compare(mmdd):
    """流水线 vs 人工标签的混淆矩阵（流水线判定：accepted=1，其余=0）。

    这不是模型指标，而是**现有流水线的基线**：有了它，「某个模型值不值得接」才有参照系——
    新方案必须在「不降低精确率」的前提下把漏检补回来，否则只是换了个错法。
    """
    all_rows = read_golden(mmdd)
    # 只算人工标注过的：其余 168 条仍是「组默认标签」（accepted=1/其余=0），
    # 把默认值当人工标签会把精确率算成恒 1.0，是最典型的假绿。
    rows = [r for r in all_rows
            if r.get("label") is not None and str(r.get("label_status", "")).endswith("human")]
    if not rows:
        print("没有人工标签，先 ingest")
        return 2
    pred = lambda r: 1 if r["group"] == "accepted" else 0
    tp = [r for r in rows if pred(r) == 1 and r["label"] == 1]
    fp = [r for r in rows if pred(r) == 1 and r["label"] == 0]
    fn = [r for r in rows if pred(r) == 0 and r["label"] == 1]
    tn = [r for r in rows if pred(r) == 0 and r["label"] == 0]
    prec = len(tp) / (len(tp) + len(fp)) if tp or fp else None
    rec = len(tp) / (len(tp) + len(fn)) if tp or fn else None
    acc = (len(tp) + len(tn)) / len(rows)
    fair = [r for r in rows if r.get("abs_sufficient") is not False]
    acc_fair = (sum(1 for r in fair if pred(r) == r["label"]) / len(fair)) if fair else None

    print("\n人工标注 %d 条（摘要不足 %d、未定 %d）"
          % (len(rows), sum(1 for r in rows if r.get("abs_sufficient") is False),
             sum(1 for r in read_golden(mmdd) if r.get("label") is None)))
    print("\n                人工=1  人工=0")
    print("  流水线收(1)   %5d  %5d" % (len(tp), len(fp)))
    print("  流水线弃(0)   %5d  %5d" % (len(fn), len(tn)))
    print("\n精确率 %.4f ｜ 召回 %.4f ｜ 总体准确率 %.4f ｜ 公平子集 %.4f"
          % (prec or 0, rec or 0, acc, acc_fair if acc_fair is not None else acc))
    if fn:
        print("\n漏检（永久丢失项，%d 条）：" % len(fn))
        for r in fn:
            print("   -", r["id"], r["title"][:78])
    if fp:
        print("\n错收（%d 条）：" % len(fp))
        for r in fp:
            print("   +", r["id"], r["title"][:78])

    out = os.path.join(OUT_DIR, "compare_%s.json" % mmdd)
    json.dump({"question_version": QUESTION_VERSION,
               "n": len(rows), "tp": len(tp), "fp": len(fp), "fn": len(fn), "tn": len(tn),
               "precision": prec, "recall": rec, "accuracy": round(acc, 4),
               "accuracy_fair": (round(acc_fair, 4) if acc_fair is not None else None),
               "fn_ids": [r["id"] for r in fn], "fp_ids": [r["id"] for r in fp]},
              open(out, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print("\n结果 -> %s" % out)
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
    c = sub.add_parser("compare"); c.add_argument("mmdd")
    a = ap.parse_args()
    if a.cmd == "build":
        return build(a.mmdd)
    if a.cmd == "run":
        return run(a.mmdd, a.backend, a.limit)
    if a.cmd == "sheet":
        return sheet(a.mmdd, a.per_group)
    if a.cmd == "ingest":
        return ingest(a.mmdd, a.path)
    if a.cmd == "compare":
        return compare(a.mmdd)
    return emit(a.mmdd, a.limit)


if __name__ == "__main__":
    sys.exit(main())
