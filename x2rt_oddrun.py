#!/usr/bin/env python3
"""x2rt_oddrun.py -- ADVERSARIAL odd-carry structural scan.

At every milestone (and every gapmeet) scan the ENTIRE written tape region for a
maximal 0-run of ODD length >= 3 bounded on BOTH sides by 1 -- a latent length-3
(or odd) gap that E could later be exposed to. The non-halt argument needs: the only
odd 0-runs in the register are the length-1 comb separators. Any odd 0-run >= 3
anywhere is flagged. Also directly reports any actual halt."""
import sys, time
sys.path.insert(0, '/Users/aokiyousuke/busybeaver')
from x2cc_fast import Fast

class Scan(Fast):
    def __init__(self, **kw):
        super().__init__(**kw)
        self.mile = 0
        self.odd_runs = []     # (step, position, length)
        self.max_odd_scanned = 0
        self.worst = {}        # length -> count of odd runs>=3 ever seen
        self.t0 = time.time()

    def scan_odd(self):
        t, lo, hi = self.tape, self.lo, self.hi
        i = lo
        # find first 1
        i = t.find(b'\x01', lo, hi + 1)
        if i == -1:
            return
        # walk maximal 0-runs strictly between 1s
        while True:
            j = t.find(b'\x00', i, hi + 1)   # start of a 0-run after a 1
            if j == -1:
                break
            k = t.find(b'\x01', j, hi + 1)   # next 1 (right bound)
            if k == -1:
                break                         # runs into background: unbounded, skip
            L = k - j
            if L >= 3 and L % 2 == 1:
                self.odd_runs.append((self.step, j, L))
                self.worst[L] = self.worst.get(L, 0) + 1
                if len(self.odd_runs) <= 40:
                    print(f"[ANOMALY] odd 0-run L={L} at pos={j} step={self.step}", flush=True)
            i = k

    def on_milestone(self):
        self.mile += 1
        self.scan_odd()

if __name__ == "__main__":
    cap = int(float(sys.argv[1])) if len(sys.argv) > 1 else 1e18
    wall = float(sys.argv[2]) if len(sys.argv) > 2 else 200.0
    s = Scan(SZ=1 << 28)
    chunk = 5 * 10**8
    while s.step < cap and not s.halted:
        s.run(min(s.step + chunk, cap))
        if time.time() - s.t0 > wall:
            print("[wall budget reached]", flush=True)
            break
    print(f"\n=== ODD-RUN SCAN: step={s.step} halted={s.halted} milestones={s.mile} "
          f"elapsed={time.time()-s.t0:.0f}s ===")
    print(f"odd 0-runs (>=3, bounded both sides) found: {len(s.odd_runs)}")
    if s.worst:
        print(f"  lengths seen: {sorted(s.worst)}   (count by length: {dict(sorted(s.worst.items()))})")
    else:
        print("  NONE -- register contains only even 0-runs plus length-1 separators")
    if s.halted:
        print("[CANDIDATE HALT] machine halted")
