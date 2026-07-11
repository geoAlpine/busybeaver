#!/usr/bin/env python3
"""x2cc_ledger.py -- CARRY CALCULUS step 1: the register ledger.
Using the exact accelerated simulator, dump
  (a) every MILESTONE (E@0 strictly left of all 1s): leading gap G + full low-part RLE
      + length of the first big block (the doubling value v);
  (b) every E-met maximal gap of length >= 2 (E@0 with 1 immediately left): step, length,
      context RLE (12 cells each side).
The (a)-sequence is the register history; the (b)-sequence is the carry-gap sequence the
carry theorem must derive.  NOTE: length-1 comb separators are skipped inside the R-cycle
acceleration (they are the proven-safe g=1 events); every E-met gap of length >= 2 is
surfaced exactly (the R-cycle stops at any 00 pair, so the micro-loop sees the entry)."""
import sys
sys.path.insert(0, '/Users/aokiyousuke/busybeaver')
from x2cc_fast import Fast, rs
from mse_extract import rle


class Ledger(Fast):
    def __init__(self, **kw):
        super().__init__(**kw)
        self.miles = []
        self.gaps = []
        self.n2 = 0

    def on_milestone(self):
        G = self.left1 - self.pos
        runs, (bigpos, biglen) = self.low_rle()
        self.miles.append((self.step, G, runs, biglen))
        low = ' '.join(f"{c}^{n}" if n > 1 else f"{c}" for c, n in runs)
        print(f"MILE step={self.step:>13} G={G:>3} n2={self.n2:>5}  low=[{low}]  big=1^{biglen}",
              flush=True)
        self.n2 = 0

    def on_gapmeet(self, gl):
        if gl < 2:
            return
        if gl == 2:
            self.n2 += 1
            return
        t = self.tape
        w0 = max(self.lo, self.pos - 14)
        w1 = min(self.hi, self.pos + gl + 14)
        ctx = rs(rle(t, w0, w1))
        self.gaps.append((self.step, gl, ctx))
        print(f"GAP  step={self.step:>13} L={gl:>3}  ctx: {ctx}", flush=True)


if __name__ == "__main__":
    cap = int(float(sys.argv[1])) if len(sys.argv) > 1 else 1_000_000_000
    led = Ledger(SZ=1 << 27)
    led.run(cap)
    print(f"[done step={led.step} halted={led.halted} miles={len(led.miles)} gaps>=2={len(led.gaps)}]")
