# -*- coding: utf-8 -*-
"""check_pages_1122.py —— 核验 GitHub Pages 线上版与本地 web/xr-paper-hub.html 一致。

大文件直下会被沙箱代理静默截断（2026-11-07 踩坑），故用 Range 分块（1MB）重组，
再与本地 **LF 归一化** 版比对 md5（Pages 服务 LF、本地为 CRLF，差行尾非内容差）。
"""
import hashlib
import json
import os
import subprocess
import tempfile

URL = "https://aber2210.github.io/xr-paper-radar/xr-paper-hub.html"
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
LOCAL = os.path.join(ROOT, "web/xr-paper-hub.html")
TMP = os.path.join(tempfile.gettempdir(), "pages_1122.bin")

CHUNK = 1024 * 1024


def fetch_all():
    total = None
    with open(TMP, "wb") as f:
        start = 0
        while True:
            end = start + CHUNK - 1
            p = subprocess.run(["curl", "-sS", "-L", "-r", f"{start}-{end}", "-D", "-", URL],
                               capture_output=True)
            raw = p.stdout
            sep = raw.find(b"\r\n\r\n")
            if sep < 0:
                raise SystemExit("bad response head")
            head, body = raw[:sep].decode("latin-1"), raw[sep + 4:]
            code = head.split("\n")[0].strip()
            if "200" not in code and "206" not in code:
                raise SystemExit("HTTP FAIL " + code)
            if total is None:
                for line in head.split("\n"):
                    if line.lower().startswith("content-range:"):
                        total = int(line.split("/")[-1].strip())
                if total is None:
                    total = len(body)
            f.write(body)
            got = f.tell()
            if got >= total or not body:
                break
            start = got
    return total


total = fetch_all()
live = open(TMP, "rb").read()
print("live bytes", len(live), "expected", total)
live_lf = live.replace(b"\r\n", b"\n")
local = open(LOCAL, "rb").read()
local_lf = local.replace(b"\r\n", b"\n")
print("md5 live(LF)", hashlib.md5(live_lf).hexdigest())
print("md5 local(LF)", hashlib.md5(local_lf).hexdigest())
print("byte-equal(LF)", live_lf == local_lf)

s = live_lf.decode("utf-8", "replace")
i = s.index("const DATA = ") + len("const DATA = ")
j = s.index(";\n</script>", i)
d = json.loads(s[i:j].replace("<\\/", "</"))
print("live DATA", len(d["papers"]), len(d["notes"]), len(d["batches"]))
b = [x for x in d["batches"] if x.get("key") == "2026-11-22"]
print("11-22 card", b[0] if b else None)
