#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""probe_sources.py — 运行前连通性 + 新稿探测探针。
1) 探测 export.arxiv.org / arxiv.org/api/query / rss.arxiv.org 可达性
2) 拉取 RSS 7 分类，统计最新公告日、2610.* 命中数、与文献库去重后的真新稿
"""
import json, os, re, sys, time
import email.utils as eu
from xml.etree import ElementTree as ET
import urllib.request, urllib.error

UA = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
CATS = ["cs.GR", "cs.HC", "cs.CV", "cs.MM", "cs.RO", "cs.AI", "eess.IV"]
KW = [
    "virtual reality", "augmented reality", "mixed reality", "extended reality",
    "head-mounted", "wearable display", "3D Gaussian", "Gaussian splatting", "NeRF",
    "SLAM", "spatial computing", "haptic", "telepresence", "avatar", "egocentric",
    "scene reconstruction", "near-eye", "light field", "waveguide", "holographic display",
    "varifocal", "maxwellian", "retinal projection", "pancake optics", "foveated",
    "accommodation-vergence",
]

REG_PATH = "papers/library/registry.jsonl"

def fetch(url, timeout=30, tries=4):
    last=None
    for a in range(tries):
        try:
            req=urllib.request.Request(url, headers={"User-Agent":UA,
                "Accept":"application/rss+xml, application/xml, text/xml, */*"})
            with urllib.request.urlopen(req, timeout=timeout) as r:
                return r.status, r.read()
        except urllib.error.HTTPError as e:
            last=e
            if e.code in (429,503):
                time.sleep(min(60,3*(2**a))); continue
            return e.code, b""
        except Exception as e:
            last=e
            time.sleep(min(60,3*(2**a)))
    return 0, b""

def load_lib():
    ids=set()
    if os.path.exists(REG_PATH):
        for line in open(REG_PATH, encoding="utf-8"):
            line=line.strip()
            if not line: continue
            try:
                d=json.loads(line)
            except Exception:
                continue
            bid=d.get("id","").split(":")[-1]
            if bid: ids.add(bid)
    return ids

def strip(s):
    s=re.sub(r"<[^>]+>"," ",s); 
    import html; s=html.unescape(s); return " ".join(s.split())

def main():
    print("=== 1) 源可达性探针 ===")
    for name,url in [
        ("export.arxiv.org/api/query",
         "https://export.arxiv.org/api/query?search_query=all:electron&max_results=1"),
        ("arxiv.org/api/query",
         "https://arxiv.org/api/query?search_query=all:electron&max_results=1"),
    ]:
        st,_=fetch(url, tries=2)
        print(f"  {name}: {st}")
    st,_=fetch("https://rss.arxiv.org/rss/cs.CV", tries=2)
    print(f"  rss.arxiv.org/rss/cs.CV: {st}")

    print("\n=== 2) RSS 拉取 + 去重比对 ===")
    lib=load_lib()
    print(f"  文献库当前条目数: {len(lib)}")
    seen={}; max_pub=""
    for c in CATS:
        url=f"https://rss.arxiv.org/rss/{c}"
        st,body=fetch(url)
        if st!=200 or not body:
            print(f"  !! {c} 返回 {st}"); continue
        try:
            root=ET.fromstring(body)
        except Exception as e:
            print(f"  !! {c} 解析失败 {e}"); continue
        for it in root.findall(".//item"):
            title=strip(it.findtext("title") or "")
            desc=strip(it.findtext("description") or "")
            link=(it.findtext("link") or "").strip()
            guid=(it.findtext("guid") or "").strip()
            pub=it.findtext("pubDate") or ""
            try:
                pub_dt=eu.parsedate_to_datetime(pub)
                published=pub_dt.strftime("%Y-%m-%d")
            except Exception:
                published=""
            src=link or guid
            m=re.search(r"abs/([0-9]+\.[0-9]+)(v\d+)?", src)
            if not m:
                m=re.search(r"([0-9]{4}\.[0-9]{4,5})(v\d+)?", guid or link or "")
            if not m: continue
            bid=m.group(1)
            if published>max_pub: max_pub=published
            if bid not in seen:
                seen[bid]={"title":title,"abstract":desc,"published":published}
        time.sleep(1)
    # 关键词过滤
    def match(r):
        blob=(r["title"]+" "+r["abstract"]).lower()
        return any(k.lower() in blob for k in KW)
    hit=[b for b,r in seen.items() if match(r)]
    new=[b for b in hit if b not in lib]
    print(f"  RSS 全量去重: {len(seen)} 条; 关键词命中: {len(hit)} 条")
    print(f"  最新公告日(max published): {max_pub}")
    print(f"  与文献库去重后真新稿: {len(new)} 条")
    # 按公告日分布
    from collections import Counter
    dist=Counter(seen[b]["published"] for b in hit)
    print("  命中稿公告日分布:", dict(sorted(dist.items())))
    # 列出 10-09 及以后公告的新稿
    fresh=[(b,seen[b]["published"],seen[b]["title"]) for b in new if seen[b]["published"]>="2026-10-09"]
    print(f"\n  公告日 >= 2026-10-09 的真新稿: {len(fresh)} 篇")
    for b,p,t in sorted(fresh, key=lambda x:x[1], reverse=True)[:40]:
        print(f"    {b}  [{p}]  {t[:70]}")
    # 若没有 fresh，列出全部 new 的前 20 供参考
    if not fresh:
        print("\n  真新稿(全部公告日)前 25 篇:")
        for b in new[:25]:
            print(f"    {b}  [{seen[b]['published']}]  {seen[b]['title'][:70]}")

if __name__=="__main__":
    main()
