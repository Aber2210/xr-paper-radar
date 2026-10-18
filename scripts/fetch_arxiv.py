#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
fetch_arxiv.py — arXiv 论文元数据拉取（标准库实现，无第三方依赖）

特性：
  - 指数退避重试（429/503/超时）
  - 用户态 UA + 真实 Accept 头，规避 Cloudflare/UA 拦截
  - 分页拉取，单批间隔 >=3s（arXiv 官方限流要求）
  - 断点续拉（写入 .checkpoint）
  - 本地按 published 日期过滤（arXiv submittedDate 索引有 ~1 天延迟）

用法：
  python fetch_arxiv.py --days 3 --max 300 --out data/raw/2026-09-22.jsonl
  python fetch_arxiv.py --since 2026-09-19 --max 400 --out data/raw/2026-09-22.jsonl
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
from datetime import datetime, timedelta
from xml.etree import ElementTree as ET

API = "https://export.arxiv.org/api/query"  # 2026-10-02：export.arxiv.org 探针恢复 200；arxiv.org/api/query 仍间歇 406，故用 export 主源（修正日期过滤更稳）。
UA = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")

CATS = ["cs.GR", "cs.HC", "cs.CV", "cs.MM", "cs.RO", "cs.AI", "eess.IV"]

# 关键词保持与 skill §2.2 一致，并补充硬件类（近眼显示/光场/全息，见 §8.6.5）
KW = [
    '"virtual reality"', '"augmented reality"', '"mixed reality"', '"extended reality"',
    '"head-mounted"', '"wearable display"', '"3D Gaussian"', '"Gaussian splatting"', '"NeRF"',
    '"SLAM"', '"spatial computing"', '"haptic"', '"telepresence"', '"avatar"', '"egocentric"',
    '"scene reconstruction"', '"near-eye"', '"light field"', '"waveguide"', '"holographic display"',
    '"varifocal"', '"maxwellian"', '"retinal projection"', '"pancake optics"', '"foveated"',
    '"accommodation-vergence"',
]

NS = {
    "atom": "http://www.w3.org/2005/Atom",
    "arxiv": "http://arxiv.org/schemas/atom",
}


def log(msg):
    ts = datetime.now().strftime("%H:%M:%S")
    print(f"[{ts}] {msg}", flush=True)


def fetch_url(url, timeout=30, tries=6):
    """带指数退避的请求。返回 (status, body_bytes)。失败时抛 RuntimeError。"""
    last = None
    for attempt in range(tries):
        try:
            req = urllib.request.Request(url, headers={
                "User-Agent": UA,
                "Accept": "application/atom+xml, text/html, */*",
                "Accept-Language": "en-US,en;q=0.9",
            })
            with urllib.request.urlopen(req, timeout=timeout) as r:
                return r.status, r.read()
        except HTTPError as e:
            last = e
            if e.code in (429, 503):
                wait = min(60, 3 * (2 ** attempt))
                log(f"  HTTP {e.code} 限流，退避 {wait}s (尝试 {attempt+1}/{tries})")
                time.sleep(wait)
                continue
            if e.code == 403:
                log(f"  HTTP 403 被拦截，重试 (尝试 {attempt+1}/{tries})")
                time.sleep(3)
                continue
            if e.code == 404:
                return 404, ""
            log(f"  HTTP {e.code}，重试 (尝试 {attempt+1}/{tries})")
            time.sleep(3)
            continue
        except (URLError, TimeoutError, ConnectionError, OSError) as e:
            last = e
            wait = min(60, 3 * (2 ** attempt))
            log(f"  请求异常 {type(e).__name__}: {e}，退避 {wait}s (尝试 {attempt+1}/{tries})")
            time.sleep(wait)
    raise RuntimeError(f"fetch_url 失败 {url}: {last}")


def parse_entry(elem):
    """解析单个 <entry> Element（来自整份 feed 的迭代），返回 dict。

    注意：必须解析整份 <feed> 后再迭代 entry Element，不能直接把 <entry>
    片段当独立 XML 解析——片段里引用的 arxiv: 等命名空间前缀声明在 <feed>
    根上，独立解析会触发 'unbound prefix' ParseError。
    """
    try:
        def _txt(e):
            if e is not None and e.text:
                return " ".join(e.text.split())
            return ""

        def _txt_raw(e):
            if e is not None and e.text:
                return e.text
            return ""

        title = _txt(elem.find("atom:title", NS)) or _txt(elem.find("title", NS))
        abstract = _txt(elem.find("atom:summary", NS)) or _txt(elem.find("summary", NS))
        published = _txt_raw(elem.find("atom:published", NS)) or _txt_raw(elem.find("published", NS))
        url = _txt_raw(elem.find("atom:id", NS)) or _txt_raw(elem.find("id", NS))

        # arxiv_id：从 http://arxiv.org/abs/2509.xxxxxv2 抽取 2509.xxxxxv2
        m = re.search(r"abs/(.+?)(?:\s|$)", url)
        arxiv_id = m.group(1) if m else url
        base_id = arxiv_id.split("v")[0]

        authors = []
        for a in (elem.findall("atom:author", NS) or []):
            nm = a.find("atom:name", NS)
            if nm is not None and nm.text:
                authors.append(nm.text.strip())

        prim = elem.find("arxiv:primary_category", NS)
        primary_category = prim.get("term") if prim is not None else ""

        cats = [c.get("term") for c in (elem.findall("atom:category", NS) or []) if c.get("term")]

        return {
            "arxiv_id": arxiv_id,
            "base_id": base_id,
            "title": title,
            "abstract": abstract,
            "authors": authors,
            "published": published,
            "primary_category": primary_category,
            "categories": cats,
            "url": url,
        }
    except Exception:
        return None


def build_query():
    cat_part = " OR ".join(f"cat:{c}" for c in CATS)
    kw_part = " OR ".join(f"abs:{k}" for k in KW)
    return f"({cat_part}) AND ({kw_part})"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--days", type=int, default=3, help="回溯天数（按 published 过滤）")
    ap.add_argument("--since", type=str, default=None,
                   help="最小日期 YYYY-MM-DD（覆盖 --days），过滤 published >= 该日")
    ap.add_argument("--max", type=int, default=300, help="最多拉取条数")
    ap.add_argument("--out", type=str, required=True, help="输出 jsonl 路径")
    ap.add_argument("--page", type=int, default=100, help="每页条数")
    ap.add_argument("--no-checkpoint", action="store_true", help="禁用断点续拉")
    args = ap.parse_args()

    # 日期下界
    if args.since:
        min_date = args.since
    else:
        min_date = (datetime.now() - timedelta(days=args.days)).strftime("%Y-%m-%d")
    log(f"日期下界 = {min_date}（本地过滤）；上限 = {args.max} 条")

    os.makedirs(os.path.dirname(os.path.abspath(args.out)), exist_ok=True)
    ckpt = args.out + ".checkpoint"
    start = 0
    seen = set()
    if not args.no_checkpoint and os.path.exists(ckpt):
        try:
            start = int(open(ckpt, encoding="utf-8").read().strip() or "0")
            log(f"读取断点 start={start}")
        except Exception:
            start = 0

    collected = []
    query = build_query()
    pages = 0
    while len(collected) < args.max:
        params = {
            "search_query": query,
            "start": start,
            "max_results": min(args.page, args.max - len(collected)),
            "sortBy": "submittedDate",
            "sortOrder": "descending",
        }
        url = API + "?" + urllib.parse.urlencode(params)
        pages += 1
        log(f"拉取页 {pages} start={start} ...")
        try:
            status, body = fetch_url(url)
        except RuntimeError as e:
            log(f"致命：{e}；已收集 {len(collected)} 条，写入后退出")
            break
        if status != 200:
            log(f"!! API 返回非 200 状态 {status}，停止分页（URL={url}）")
            break

        # 解析整份 feed 后迭代 <entry>（保留命名空间上下文，避免 unbound prefix）
        text = body.decode("utf-8", "ignore")
        try:
            feed = ET.fromstring(text)
        except ET.ParseError as e:
            log(f"  feed 解析失败：{e}，停止分页")
            break
        entries = feed.findall("atom:entry", NS)
        if not entries:
            log("无更多条目，停止分页")
            break
        past_window = False
        for e in entries:
            rec = parse_entry(e)
            if rec is None:
                continue
            if rec["base_id"] in seen:
                continue
            seen.add(rec["base_id"])
            # 本地日期过滤
            pub = rec["published"][:10]
            if pub and pub < min_date:
                # submittedDate 降序：一旦越过下界，后续全部更旧，整页停止
                past_window = True
                break
            collected.append(rec)
        if past_window:
            log("已越过日期下界（降序），停止分页")
            break
        start += len(entries)
        # 断点写入
        if not args.no_checkpoint:
            open(ckpt, "w", encoding="utf-8").write(str(start))
        # arXiv 限流：单批间隔 >=3s
        time.sleep(3)

        if len(entries) < params["max_results"]:
            log("末页（条目数 < max_results），停止")
            break

    # 写文件（保留全部字段；下游再筛 XR 相关度）
    with open(args.out, "w", encoding="utf-8") as f:
        for r in collected:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")

    log(f"完成：共写入 {len(collected)} 条 → {args.out}")
    print(f"WROTE={len(collected)}")


if __name__ == "__main__":
    main()
