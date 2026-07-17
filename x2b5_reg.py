"""x2b5_reg.py -- exact maxrun-record (register) envelope for B5.

maxrun is recomputed ONLY at right-record excursion events (O(width) each,
~O(width) events => O(width^2) total, cheap). We report every NEW maximum of
maxrun with the exact step at which that record event occurred, plus the
9*2^k-1 comparison and the step-ratio between successive registers.
"""
import sys
from x2b5_sim import RULES

def maxrun(cells, lo, hi):
    best = cur = 0
    for p in range(lo, hi + 1):
        if cells.get(p, 0):
            cur += 1
            if cur > best: best = cur
        else:
            cur = 0
    return best

def run(max_steps):
    cells = {}; pos = 0; state = 'A'; lo = hi = 0
    recs = []   # (step, maxrun, width, ones)
    best = 0
    for step in range(max_steps):
        sym = cells.get(pos, 0)
        rule = RULES[state][sym]
        if rule is None:
            print("HALT at step", step); return recs, True
        w, mv, nxt = rule
        if w != sym:
            if w: cells[pos] = 1
            else: del cells[pos]
        pos += mv; state = nxt
        if pos > hi or pos < lo:
            if pos > hi: hi = pos
            else: lo = pos
            mr = maxrun(cells, lo, hi)
            if mr > best:
                best = mr
                recs.append((step, mr, hi - lo + 1, len(cells)))
    return recs, False

if __name__ == '__main__':
    cap = int(sys.argv[1]) if len(sys.argv) > 1 else 2_000_000
    recs, halted = run(cap)
    print("cap:", cap, "halted:", halted)
    fam = {9 * 2**k - 1: k for k in range(0, 14)}
    print(f"{'step':>12} {'maxrun':>7} {'width':>7} {'ones':>7} {'stepratio':>10}  9*2^k-1?")
    prev = 0
    for s, m, w, o in recs:
        r = (s / prev) if prev else 0
        tag = f"YES k={fam[m]}" if m in fam else ""
        print(f"{s:>12} {m:>7} {w:>7} {o:>7} {r:>10.3f}  {tag}")
        prev = s
