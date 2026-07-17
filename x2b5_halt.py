"""x2b5_halt.py -- B5 halt-trigger analysis.

Halt fires iff state F reads 0. F is entered ONLY from E reading 1 (E:1->1RF).
So: HALT  <=>  exists a time when E reads 1 at cell p and cell p+1 == 0.
Equivalently: E must never read the LAST 1 of a run of 1s.

This probe records, at every E->F entry, the symbol F then reads, and the
position of the head within its run of 1s (distance to the run's right end).
"""
import sys
from collections import Counter
from x2b5_sim import RULES

def run(max_steps):
    cells = {}; pos = 0; state = 'A'
    fentry = 0
    fread = Counter()
    tail = Counter()     # #consecutive 1s strictly right of the cell E read
    for step in range(max_steps):
        sym = cells.get(pos, 0)
        rule = RULES[state][sym]
        if rule is None:
            print(f"*** HALT at step {step} (state F read 0 at pos {pos}) ***")
            return fentry, fread, tail, True
        w, mv, nxt = rule
        if state == 'E' and sym == 1:
            # E reads 1 -> writes 1, moves R into F. F will read cell pos+1.
            fentry += 1
            nxt_sym = cells.get(pos + 1, 0)
            fread[nxt_sym] += 1
            t = 0; q = pos + 1
            while cells.get(q, 0) == 1:
                t += 1; q += 1
            tail[min(t, 12)] += 1
        if w != sym:
            if w: cells[pos] = 1
            else: del cells[pos]
        pos += mv; state = nxt
    return fentry, fread, tail, False

if __name__ == '__main__':
    cap = int(sys.argv[1]) if len(sys.argv) > 1 else 4_000_000
    fentry, fread, tail, halted = run(cap)
    print("cap:", cap, "halted:", halted)
    print("F entries (E read a 1):", fentry)
    print("symbol F then read:", dict(fread), " <- a 0 here = HALT")
    print("run-tail length strictly right of the cell E read (capped at 12):")
    for k in sorted(tail): print(f"   tail={k:>2}: {tail[k]}")
