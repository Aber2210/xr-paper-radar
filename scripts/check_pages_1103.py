"""核验 GitHub Pages 线上版本：HTTP 200 + 页面含 const DATA + DATA 计数与本地一致（730/419/43）。"""
import urllib.request, re, json

UA = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120.0 Safari/537.36"}
url = "https://aber2210.github.io/xr-paper-radar/"
try:
    req = urllib.request.Request(url, headers=UA)
    with urllib.request.urlopen(req, timeout=60) as r:
        html = r.read().decode("utf-8", "replace")
        code = r.status
except Exception as e:
    print("FETCH FAIL:", e); raise SystemExit(1)
print("HTTP", code, "bytes", len(html))
has_data = "const DATA" in html
print("has const DATA:", has_data)
m = re.search(r'const DATA = (\{.*?\});\s*\n', html, re.S)
if m:
    d = json.loads(m.group(1))
    print("papers:", len(d.get("papers", [])), "notes:", len(d.get("notes", [])), "batches:", len(d.get("batches", [])))
    ids = {p["id"].split(":")[-1].split("v")[0] for p in d.get("papers", [])}
    need = ["2610.41501","2610.41602","2610.41127","2610.41833","2610.41671","2610.41011","2610.40832","2610.41987","2610.41496","2610.41680","2610.40760","2511.11231","2602.21535"]
    missing = [x for x in need if x not in ids]
    print("new papers missing on Pages:", missing or "NONE")
    b1103 = [b for b in d.get("batches", []) if b.get("key") == "2026-11-03"]
    print("11-03 batch on Pages:", b1103[0] if b1103 else "MISSING")
    ok = (code == 200 and has_data and len(d.get("papers", [])) == 730 and len(d.get("notes", [])) == 419
          and not missing and bool(b1103))
    print("PAGES VERIFY:", "PASS" if ok else "FAIL")
else:
    print("DATA block not found"); print("PAGES VERIFY: FAIL")
