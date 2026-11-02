"""核验 web/xr-paper-hub.html 内 DATA 计数与磁盘一致（registry 行数 / notes 文件数 / daily 目录数 / batches 数）。"""
import re, json, glob, os

html = open('web/xr-paper-hub.html', encoding='utf-8').read()
m = re.search(r'const DATA = (\{.*?\});\s*\n', html, re.S)
assert m, 'DATA block not found'
data = json.loads(m.group(1))
print('HTML DATA keys:', sorted(data.keys()))
papers = data.get('papers', [])
notes = data.get('notes', [])
batches = data.get('batches', [])
print('html papers:', len(papers), ' html notes:', len(notes), ' html batches:', len(batches))

reg = [l for l in open('papers/library/registry.jsonl', encoding='utf-8') if l.strip()]
note_files = glob.glob('papers/notes/*.md')
daily_dirs = [d for d in glob.glob('papers/daily/*') if os.path.isdir(d)]
print('disk registry:', len(reg), ' disk notes:', len(note_files), ' disk daily dirs:', len(daily_dirs))

ok = True
if len(papers) != len(reg):
    print('MISMATCH papers', len(papers), len(reg)); ok = False
if len(notes) != len(note_files):
    print('MISMATCH notes', len(notes), len(note_files)); ok = False
# batches 应覆盖全部 daily 目录（状态日也有卡片）
if len(batches) != len(daily_dirs):
    print('MISMATCH batches', len(batches), len(daily_dirs)); ok = False

# 新批次在场检查
ids = {p['id'].split(':')[-1].split('v')[0] for p in papers}
for pid in ['2610.41501','2610.41602','2610.41127','2610.41833','2610.41671','2610.41011','2610.40832','2610.41987','2610.41496','2610.41680','2610.40760','2511.11231','2602.21535']:
    if pid not in ids:
        print('MISSING in html:', pid); ok = False
bdays = {b.get('day') or b.get('date') or b.get('id') for b in batches}
print('batch keys sample:', list(batches[0].keys())[:8] if batches else None)
print('VERIFY', 'PASS' if ok else 'FAIL')
