#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
fetch_fulltext.py — arXiv 全文抓取（标准库实现，无第三方依赖）

降级链路（任一级成功即停）：
  L0  arXiv HTML 全文        https://arxiv.org/html/<id>v<n>      ← 首选
  L1  ar5iv 转换版           https://ar5iv.labs.arxiv.org/abs/<id> ← HTML 缺失时
  L2  arXiv PDF → 文本        https://arxiv.org/pdf/<id>v<n>        ← 需 pdfminer.six（可选）
  L3  OpenReview             https://api.openreview.net/notes?forum=<id>
  L4  Semantic Scholar       api.semanticscholar.org/.../arXiv:<id>?fields=openAccessPdf,abstract,tldr
  L5  摘要降级               ← 全部失败时的最后手段（绝不伪造）

障碍/限流对策：
  - 429/503：指数退避 min(60, 3*2^n) 秒，每请求间隔 >=3s
  - 403 Cloudflare/UA：真实 UA + Accept/Accept-Language 头
  - 超时：30s，重试 3 次后跳下一级
  - 强制串行（for 循环 + sleep），禁止并发线程池（防封 IP）
  - 扫描件 PDF（文本<500 字符）：标记 LOW_TEXT，不 OCR，直接降级

证据等级（写入每个 .txt 文件头 + _manifest.json）：
  FULL    >=4000 字符且含 Result/Method/Experiment 段
  PARTIAL 1000~4000 字符
  ABSTRACT_ONLY  仅摘要（来自 --abstracts 旁注 jsonl）

_manifest.json 采用「合并写入」，追加抓取不会丢失历史记录（修复老版覆盖 bug）。

用法：
  python fetch_fulltext.py --ids 2509.18473,2509.18898 --out data/fulltext/
  python fetch_fulltext.py --ids 2509.18473 --out data/fulltext/ --abstracts data/raw/2026-09-22.jsonl
"""
import argparse
import json
import os
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from urllib.error import HTTPError, URLError
from datetime import datetime

UA = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")

SECTION_RE = re.compile(
    r"(?im)^\s*(?:[IVXLC]+\.|\d+(?:\.\d+)*|[A-Z][A-Za-z ]{2,40})\.?\s+"
    r"(Abstract|Introduction|Related Work|Method|Methods|Approach|Model|"
    r"Architecture|Implementation|Experiment|Experiments|Results|Evaluation|"
    r"Discussion|Conclusion|References|Background)\b")

PDF_MINER_AVAILABLE = False
try:
    from pdfminer.high_level import extract_text  # type: ignore
    PDF_MINER_AVAILABLE = True
except Exception:
    pass


def log(msg):
    ts = datetime.now().strftime("%H:%M:%S")
    print(f"[{ts}] {msg}", flush=True)


def fetch_url(url, timeout=30, tries=5, binary=False):
    last = None
    for attempt in range(tries):
        try:
            req = urllib.request.Request(url, headers={
                "User-Agent": UA,
                "Accept": "*/*",
                "Accept-Language": "en-US,en;q=0.9",
            })
            with urllib.request.urlopen(req, timeout=timeout) as r:
                data = r.read() if binary else r.read().decode("utf-8", "ignore")
                return r.status, data
        except HTTPError as e:
            last = e
            if e.code in (429, 503):
                wait = min(60, 3 * (2 ** attempt)); log(f"  HTTP {e.code}，退避 {wait}s"); time.sleep(wait); continue
            if e.code == 403:
                log(f"  HTTP 403 拦截，重试 (尝试 {attempt+1}/{tries})"); time.sleep(3); continue
            if e.code == 404:
                return 404, ""
            log(f"  HTTP {e.code}，重试 (尝试 {attempt+1}/{tries})"); time.sleep(3); continue
        except (URLError, TimeoutError, ConnectionError, OSError) as e:
            last = e
            wait = min(60, 3 * (2 ** attempt)); log(f"  异常 {type(e).__name__}: {e}，退避 {wait}s"); time.sleep(wait)
    raise RuntimeError(f"fetch_url 失败 {url}: {last}")


def clean_html(html):
    # 去 script/style/注释
    html = re.sub(r"<script[\s\S]*?</script>", " ", html, flags=re.I)
    html = re.sub(r"<style[\s\S]*?</style>", " ", html, flags=re.I)
    html = re.sub(r"<!--[\s\S]*?-->", " ", html)
    # 块级标签换行为换行，便于分段
    html = re.sub(r"(?i)</(p|div|li|h[1-6]|br|tr|section|article)>", "\n", html)
    html = re.sub(r"(?i)<br\s*/?>", "\n", html)
    # 去掉行内标签
    html = re.sub(r"<[^>]+>", " ", html)
    import html as _html
    html = _html.unescape(html)
    # 数学/公式占位清理（arXiv HTML 常见 <mml:math> 已被剥离，残留可读文本）
    html = re.sub(r"\[Math:(?:.*?)\]", " ", html, flags=re.S)
    # 合并空白
    lines = [re.sub(r"[ \t]+", " ", ln).strip() for ln in html.splitlines()]
    lines = [ln for ln in lines if ln]
    return "\n".join(lines)


def grade_evidence(text):
    n = len(text)
    has_core = bool(SECTION_RE.search(text))
    if n >= 4000 and has_core:
        return "FULL"
    if n >= 1000:
        return "PARTIAL"
    return "ABSTRACT_ONLY"


def try_l0(base_id):
    """arXiv HTML 全文。尝试 v2/v1/无版本。"""
    for suffix in ("v2", "v1", ""):
        url = f"https://arxiv.org/html/{base_id}{suffix}"
        try:
            st, html = fetch_url(url)
        except RuntimeError:
            continue
        if st == 404:
            continue
        if st != 200 or not html or len(html) < 2000:
            continue
        text = clean_html(html)
        if len(text) < 1500:
            continue
        return "L0", text, url
    return None


def try_l1(base_id):
    url = f"https://ar5iv.labs.arxiv.org/abs/{base_id}"
    try:
        st, html = fetch_url(url)
    except RuntimeError:
        return None
    if st != 200 or not html or len(html) < 2000:
        return None
    text = clean_html(html)
    if len(text) < 1500:
        return None
    return "L1", text, url


def try_l2(base_id):
    if not PDF_MINER_AVAILABLE:
        return None
    for suffix in ("v2", "v1", ""):
        url = f"https://arxiv.org/pdf/{base_id}{suffix}"
        try:
            st, data = fetch_url(url, binary=True)
        except RuntimeError:
            continue
        if st == 404:
            continue
        if st != 200 or not data:
            continue
        try:
            text = extract_text(data)
        except Exception:
            continue
        text = re.sub(r"[ \t]+", " ", text)
        text = "\n".join(ln.strip() for ln in text.splitlines() if ln.strip())
        if len(text) < 500:
            return "L2", text, url, "LOW_TEXT"
        return "L2", text, url
    return None


def try_l3(base_id):
    url = f"https://api.openreview.net/notes?forum={base_id}"
    try:
        st, js = fetch_url(url)
    except RuntimeError:
        return None
    if st != 200:
        return None
    try:
        obj = json.loads(js)
        notes = obj.get("notes") or []
        if not notes:
            return None
        content = notes[0].get("content", {})
        parts = []
        for k, v in content.items():
            if isinstance(v, str) and len(v) > 50:
                parts.append(f"## {k}\n{v}")
        text = "\n\n".join(parts)
        if len(text) < 800:
            return None
        return "L3", text, url
    except Exception:
        return None


def try_l4(base_id):
    url = (f"https://api.semanticscholar.org/graph/v1/paper/arXiv:{base_id}"
           f"?fields=openAccessPdf,abstract,tldr")
    try:
        st, js = fetch_url(url)
    except RuntimeError:
        return None
    if st != 200:
        return None
    try:
        obj = json.loads(js)
        pdf = (obj.get("openAccessPdf") or {}).get("url")
        abs_txt = obj.get("abstract") or ""
        tldr = (obj.get("tldr") or {}).get("text") or ""
        if pdf:
            try:
                _, data = fetch_url(pdf, binary=True)
                if PDF_MINER_AVAILABLE and data:
                    text = extract_text(data)
                    text = re.sub(r"[ \t]+", " ", text)
                    text = "\n".join(ln.strip() for ln in text.splitlines() if ln.strip())
                    if len(text) >= 1000:
                        return "L4", text, pdf
            except Exception:
                pass
        if abs_txt:
            return "L4", (tldr + "\n\n" + abs_txt).strip(), url
    except Exception:
        return None
    return None


def fetch_one(base_id, abstracts):
    # L0 → L1 → L2 → L3 → L4
    for fn in (try_l0, try_l1, try_l2, try_l3, try_l4):
        res = fn(base_id)
        if res is None:
            continue
        level, text = res[0], res[1]
        src_url = res[2]
        low = len(res) > 3 and res[3] == "LOW_TEXT"
        ev = "ABSTRACT_ONLY" if low else grade_evidence(text)
        return level, text, src_url, ev

    # L5：摘要降级（绝不伪造）
    abs_txt = abstracts.get(base_id, "")
    if abs_txt:
        return "L5", f"[摘要降级] {abs_txt}", "abstract-only", "ABSTRACT_ONLY"
    return "L5", "[无可用全文与摘要]", "none", "ABSTRACT_ONLY"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--ids", required=True, help="逗号分隔的 arXiv base_id 列表")
    ap.add_argument("--out", required=True, help="输出目录（.txt + _manifest.json）")
    ap.add_argument("--abstracts", default=None, help="可选：raw jsonl，用于 L5 摘要降级")
    ap.add_argument("--sleep", type=float, default=3.0, help="每篇之间的间隔秒数")
    args = ap.parse_args()

    os.makedirs(args.out, exist_ok=True)
    ids = [x.strip() for x in args.ids.split(",") if x.strip()]

    abstracts = {}
    if args.abstracts and os.path.exists(args.abstracts):
        for line in open(args.abstracts, encoding="utf-8"):
            line = line.strip()
            if not line:
                continue
            try:
                r = json.loads(line)
                abstracts[r.get("base_id")] = r.get("abstract", "")
            except Exception:
                pass

    # 合并写入 manifest（不覆盖历史）
    mani_path = os.path.join(args.out, "_manifest.json")
    manifest = {}
    if os.path.exists(mani_path):
        try:
            manifest = json.load(open(mani_path, encoding="utf-8"))
        except Exception:
            manifest = {}

    for i, bid in enumerate(ids):
        log(f"[{i+1}/{len(ids)}] {bid} 抓取中...")
        try:
            level, text, src_url, ev = fetch_one(bid, abstracts)
        except Exception as e:
            log(f"  !! {bid} 异常：{e}")
            level, text, src_url, ev = "L5", f"[抓取异常] {e}", "none", "ABSTRACT_ONLY"

        out_path = os.path.join(args.out, f"{bid}.txt")
        header = (f"# LEVEL: {level}\n# EVIDENCE: {ev}\n# CHARS: {len(text)}\n"
                  f"# URL: {src_url}\n# FETCHED: {datetime.now().isoformat(timespec='seconds')}\n\n")
        open(out_path, "w", encoding="utf-8").write(header + text + "\n")

        manifest[bid] = {
            "level": level, "evidence": ev, "chars": len(text),
            "url": src_url, "fetched": datetime.now().isoformat(timespec="seconds"),
        }
        json.dump(manifest, open(mani_path, "w", encoding="utf-8"),
                  ensure_ascii=False, indent=1)
        log(f"  → {level} / {ev} / {len(text)} 字符")
        # 强制串行间隔，防封 IP
        if i + 1 < len(ids):
            time.sleep(args.sleep)

    log(f"完成：{len(ids)} 篇 → {args.out}")


if __name__ == "__main__":
    main()
