#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Replace the buggy PAPERS/REF literal blocks in write_deliverables_1008.py with a JSON load."""
src = open("D:/Agent/WorkBuddy/Research/scripts/write_deliverables_1008.py", encoding="utf-8").read()
start = src.index("PAPERS = [")
ref_start = src.index("REF = [", start)
ref_open = src.index("[", ref_start)      # the '[' of REF = [
ref_close = src.index("]", ref_open)       # first ']' after it closes REF (no nested brackets in REF)
end = ref_close + 1
tail = src[end:]
assert tail.startswith("\n\nfor p in PAPERS:") or tail.startswith("\nfor p in PAPERS:"), repr(tail[:50])

loader = (
    'PAPERS, REF = (lambda d: (d["PAPERS"], d["REF"]))(\n'
    '    json.load(open(os.path.join(ROOT,"data/scored_1008.json"),encoding="utf-8")))\n'
)
new = src[:start] + loader + src[end:]
open("D:/Agent/WorkBuddy/Research/scripts/write_deliverables_1008.py", "w", encoding="utf-8").write(new)
print("patched. start", start, "end", end, "new len", len(new))
