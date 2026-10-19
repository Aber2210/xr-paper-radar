#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""fetch_rss.py — 当 export.arxiv.org/api/query 被沙箱代理 406 拦截时的兜底拉取源。
通过沙箱代理可达的 rss.arxiv.org RSS 源，按分类拉取"最新公告"批次论文（含完整摘要），
本地按关键词过滤，输出与 fetch_arxiv.py 完全一致的 jsonl schema，供 build_today.py 下游复用。

用法：
  python scripts/fetch_rss.py --out data/raw/2026-09-24.jsonl
  python scripts/fetch_rss.py --out data/raw/2026-09-24.jsonl --cats cs.GR,cs.RO
"""
import argparse
import json
import os
import re
import time
import html
import email.utils as eu
from xml.etree import ElementTree as ET
import urllib.request
import urllib.error

UA = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")

DEFAULT_CATS = ["cs.GR", "cs.HC", "cs.CV", "cs.MM", "cs.RO", "cs.AI", "eess.IV"]

# 与 fetch_arxiv.py 的 KW 保持一致（含硬件类渲染方向，见 skill §8.6.5）
KW = [
    "virtual reality", "augmented reality", "mixed reality", "extended reality",
    "head-mounted", "wearable display", "3D Gaussian", "Gaussian splatting", "NeRF",
    "SLAM", "spatial computing", "haptic", "telepresence", "avatar", "egocentric",
    "scene reconstruction", "near-eye", "light field", "waveguide", "holographic display",
    "varifocal", "maxwellian", "retinal projection", "pancake optics", "foveated",
    "accommodation-vergence",
]

# 缩写层（2026-10-19 漏网根因：标题里大量使用 VR/AR/MR/XR 缩写而全称关键词不命中）。
# 裸子串匹配会误伤（ar⊂area/search），必须词边界正则。
ABBREV_RE = re.compile(
    r"\b(?:VR|AR|MR|XR|HMD|OST|SLAM|VIO|IMU|DoF|FOV|JND|IPD|VAC|MTF|CGH)\b"
)


def kw_match(text):
    """KW 子串 + 缩写词边界双层匹配（大小写不敏感）。"""
    t = text.lower()
    if any(k.lower() in t for k in KW):
        return True
    return bool(ABBREV_RE.search(text))


def fetch_url(url, timeout=30, tries=4):
    last = None
    for attempt in range(tries):
        try:
            req = urllib.request.Request(url, headers={
                "User-Agent": UA,
                "Accept": "application/rss+xml, application/xml, text/xml, */*",
                "Accept-Language": "en-US,en;q=0.9",
            })
            with urllib.request.urlopen(req, timeout=timeout) as r:
                return r.status, r.read()
        except urllib.error.HTTPError as e:
            last = e
            if e.code in (429, 503):
                wait = min(60, 3 * (2 ** attempt))
                print(f"  HTTP {e.code} 限流，退避 {wait}s")
                time.sleep(wait); continue
            print(f"  HTTP {e.code} 终止该源")
            return e.code, b""
        except Exception as e:
            last = e
            wait = min(60, 3 * (2 ** attempt))
            print(f"  异常 {type(e).__name__}: {e}，退避 {wait}s")
            time.sleep(wait)
    print(f"  失败 {url}: {last}")
    return 0, b""


def strip_tags(s):
    s = re.sub(r"<[^>]+>", " ", s)
    s = html.unescape(s)
    s = " ".join(s.split())
    return s


def parse_rss(data, cat):
    root = ET.fromstring(data)
    items = root.findall(".//item")
    out = []
    for it in items:
        title = strip_tags(it.findtext("title") or "")
        desc = strip_tags(it.findtext("description") or "")
        link = (it.findtext("link") or "").strip()
        guid = (it.findtext("guid") or "").strip()
        pub = it.findtext("pubDate") or ""
        try:
            pub_dt = eu.parsedate_to_datetime(pub)
            published = pub_dt.strftime("%Y-%m-%dT%H:%M:%SZ")
        except Exception:
            published = ""
        # categories
        cats = [c.text for c in it.findall("category") if c.text]
        # arxiv id：优先 link（含 abs/），guid 为 oai:arXiv.org: 格式不含 abs/
        src = link or guid
        m = re.search(r"abs/([0-9]+\.[0-9]+)(v\d+)?", src)
        if not m:
            m = re.search(r"([0-9]{4}\.[0-9]{4,5})(v\d+)?", guid or link or "")
        if not m:
            continue
        base_id = m.group(1)
        ver = m.group(2) or ""
        arxiv_id = base_id + ver
        primary = cats[0] if cats else cat
        out.append({
            "arxiv_id": arxiv_id,
            "base_id": base_id,
            "title": title,
            "abstract": desc,
            "authors": [],
            "published": published,
            "primary_category": primary,
            "categories": cats,
            "url": f"http://arxiv.org/abs/{arxiv_id}",
            "source_cat": cat,
        })
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", required=True)
    ap.add_argument("--cats", default=",".join(DEFAULT_CATS))
    ap.add_argument("--no-filter", action="store_true", help="不过滤关键词，输出全量")
    args = ap.parse_args()
    cats = [c.strip() for c in args.cats.split(",") if c.strip()]

    os.makedirs(os.path.dirname(os.path.abspath(args.out)), exist_ok=True)
    seen = {}
    for c in cats:
        url = f"https://rss.arxiv.org/rss/{c}"
        print(f"[pull] {c} ...")
        st, body = fetch_url(url)
        if st != 200 or not body:
            print(f"  !! {c} 返回 {st}，跳过")
            continue
        recs = parse_rss(body, c)
        for r in recs:
            if r["base_id"] not in seen:
                seen[r["base_id"]] = r
        print(f"  {c}: {len(recs)} 条，累计去重 {len(seen)}")
        time.sleep(2)

    # 关键词过滤（KW 全称子串 + VR/AR/MR/XR 缩写词边界双层）
    if args.no_filter:
        filtered = list(seen.values())
    else:
        filtered = [r for r in seen.values() if kw_match(r["title"] + " " + r["abstract"])]

    with open(args.out, "w", encoding="utf-8") as f:
        for r in filtered:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")
    print(f"完成：全量去重 {len(seen)} 条 → 关键词命中 {len(filtered)} 条 → {args.out}")
    print(f"WROTE={len(filtered)}")


if __name__ == "__main__":
    main()
