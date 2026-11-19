# -*- coding: utf-8 -*-
"""residual_scan.py —— 残差复核：把「被关键词层丢弃、但可能属于收录赛道」的稿子捞出来

背景（2026-11-19 实测）：对 11-18 批 `nonxr` 742 条做随机 100 条盲评，7 条实为应收录，
漏检率 7.0%（Wilson 95% CI 3.4%–13.7%），折算 25–102 篇/批。补词表不可解：把这些语义簇
加进 KW 会引 40 条噪声换 7 条真值（精确率 18%），属语义缺口而非词表缺口。

本脚本只做两件事，**绝不写 registry、绝不自动入馆**：
  dump    把 nonxr 全量切成若干批次（标题 + 摘要前两句），供运行时的模型逐批阅读
  ingest  收下模型的判定（jsonl），产出「疑似漏检清单」与统计

用法：
    python scripts/residual_scan.py dump 1118
    # 模型逐批读 data/residual_1118/batch_*.txt，把判定写成 verdicts.jsonl：
    #   {"n": 12, "verdict": 1, "track": "世界模型与仿真", "why": "..."}
    #   {"n": 13, "verdict": 0}
    python scripts/residual_scan.py ingest 1118 data/residual_1118/verdicts.jsonl

红线：清单只作人工挑选的输入；任何入馆动作仍走正常流程（全文抓取 → 评分 → 产物）。
"""
import argparse
import glob
import io
import json
import os
import re
import sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
os.chdir(ROOT)
TRACKS = ["神经渲染", "渲染与显示", "重建与SLAM", "化身与人体", "交互与输入", "触觉与多模态",
          "内容生成", "世界模型与仿真", "感知与认知", "空间计算与UI", "系统与平台", "评估与数据集"]


def load_nonxr(mmdd):
    p = "data/nonxr_%s.json" % mmdd
    if not os.path.exists(p):
        print("缺少 %s" % p)
        sys.exit(2)
    return json.load(io.open(p, encoding="utf-8"))


def brief(rec):
    ab = re.split(r"(?<=[.!?])\s", (rec.get("abstract") or "").strip())
    return " ".join(ab[:2])[:360]


def dump(mmdd, per_batch=190):
    d = load_nonxr(mmdd)
    out_dir = "data/residual_%s" % mmdd
    os.makedirs(out_dir, exist_ok=True)
    for f in glob.glob(os.path.join(out_dir, "batch_*.txt")):
        os.remove(f)
    ids = sorted(d)
    index = []
    for bi in range(0, len(ids), per_batch):
        chunk = ids[bi:bi + per_batch]
        lines = []
        for k, pid in enumerate(chunk, bi + 1):
            r = d[pid]
            index.append({"n": k, "id": pid})
            lines.append("[%03d] %s | %s" % (k, pid, (r.get("title") or "")[:95]))
            lines.append("      %s" % brief(r))
        fp = os.path.join(out_dir, "batch_%02d.txt" % (bi // per_batch))
        io.open(fp, "w", encoding="utf-8").write("\n".join(lines) + "\n")
    json.dump(index, io.open(os.path.join(out_dir, "index.json"), "w", encoding="utf-8"),
              ensure_ascii=False, indent=1)
    print("nonxr %d 条 → %s 下 %d 个批次（每批 %d 条），索引进 index.json"
          % (len(ids), out_dir, (len(ids) + per_batch - 1) // per_batch, per_batch))
    print("红线：本清单只供人工挑选，不自动入馆、不写 registry。")
    return 0


def ingest(mmdd, verdict_path):
    d = load_nonxr(mmdd)
    idx_p = "data/residual_%s/index.json" % mmdd
    if not os.path.exists(idx_p):
        print("缺少 %s，先跑 dump" % idx_p)
        return 2
    index = {e["n"]: e["id"] for e in json.load(io.open(idx_p, encoding="utf-8"))}
    flagged, n = [], 0
    for ln in io.open(verdict_path, encoding="utf-8"):
        ln = ln.strip()
        if not ln:
            continue
        try:
            v = json.loads(ln)
        except ValueError:
            continue
        n += 1
        if int(v.get("verdict", 0)) != 1:
            continue
        pid = index.get(int(v.get("n", 0)))
        if not pid:
            continue
        r = d.get(pid, {})
        flagged.append({"id": pid, "n": v.get("n"), "title": r.get("title", ""),
                        "cat": r.get("cat", ""), "track": v.get("track", ""),
                        "why": (v.get("why") or "")[:160]})
    by_track = {}
    for f in flagged:
        by_track[f["track"] or "未标"] = by_track.get(f["track"] or "未标", 0) + 1
    out = {"mmdd": mmdd, "n_scanned": n, "n_flagged": len(flagged),
           "rate": round(len(flagged) / n, 4) if n else None,
           "by_track": by_track, "flagged": flagged,
           "note": "只报警清单：入馆须另行走全文抓取→评分→产物，本文件不改变 registry"}
    p = "data/residual_%s.json" % mmdd
    json.dump(out, io.open(p, "w", encoding="utf-8"), ensure_ascii=False, indent=1)

    print("扫描 %d 条 → 疑似漏检 %d 条（%.1f%%）" % (n, len(flagged), 100 * len(flagged) / n if n else 0))
    for t, c in sorted(by_track.items(), key=lambda x: -x[1]):
        print("   %-12s %d" % (t, c))
    print("\n清单（前 15 条）：")
    for f in flagged[:15]:
        print("   + %s [%s] %s" % (f["id"], f["track"], f["title"][:70]))
    print("\n结果 -> %s（只报警，不改 registry）" % p)
    return 0


def main():
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)
    d = sub.add_parser("dump"); d.add_argument("mmdd"); d.add_argument("--per-batch", type=int, default=190)
    g = sub.add_parser("ingest"); g.add_argument("mmdd"); g.add_argument("verdict")
    a = ap.parse_args()
    return dump(a.mmdd, a.per_batch) if a.cmd == "dump" else ingest(a.mmdd, a.verdict)


if __name__ == "__main__":
    sys.exit(main())
