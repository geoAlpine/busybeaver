"""x2b5_records.py -- exact O(1)/step growth probe for B5.

Tracks, from the blank tape:
  * new rightmost-record / leftmost-record head excursions (step, pos)
  * ones() maintained incrementally
No sampling, no heuristics. Halt iff F reads 0.
"""
import sys
from x2b5_sim import RULES

def run(max_steps):
    cells = {}
    pos = 0; state = 'A'; ones = 0
    lo = hi = 0
    rrec = []   # (step, pos, ones)  new rightmost record
    lrec = []
    for step in range(max_steps):
        sym = cells.get(pos, 0)
        rule = RULES[state][sym]
        if rule is None:
            print("HALT at step", step); return rrec, lrec, step, True
        w, mv, nxt = rule
        if w != sym:
            if w: cells[pos] = 1; ones += 1
            else: del cells[pos]; ones -= 1
        pos += mv; state = nxt
        if pos > hi:
            hi = pos; rrec.append((step, pos, ones))
        elif pos < lo:
            lo = pos; lrec.append((step, pos, ones))
    return rrec, lrec, max_steps, False

if __name__ == '__main__':
    cap = int(sys.argv[1]) if len(sys.argv) > 1 else 2_000_000
    rrec, lrec, last, halted = run(cap)
    print("cap:", cap, "halted:", halted)
    for name, rec in (("RIGHT", rrec), ("LEFT", lrec)):
        print(f"\n# {name} records: {len(rec)}")
        print(f"{'step':>12} {'pos':>7} {'ones':>7} {'dstep':>12} {'ratio':>8}")
        prev = 0
        for s, p, o in rec:
            d = s - prev
            r = (s / prev) if prev else 0
            print(f"{s:>12} {p:>7} {o:>7} {d:>12} {r:>8.4f}")
            prev = s
