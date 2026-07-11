#!/usr/bin/env python3
"""x2rt_gaphunt.py -- ADVERSARIAL large-g gap hunt.

Runs the (independently full-tape-validated) accelerated simulator as far as memory
allows, recording EVERY E-met gap length. Flags, as [CANDIDATE HALT] / anomaly:
  - any gap of length exactly 3 met by E     (the claimed halt trigger)
  - any ODD gap length >= 3                   (the "odd carry" failure mode)
  - any gap length not in the claimed set {6,10,18}
  - actual machine halt (st B reading 1)
Prints per-generation gap multiset so a break in the {18,10}/{18,10,6} parity
pattern at large g is visible."""
import sys, time
sys.path.insert(0, '/Users/aokiyousuke/busybeaver')
from x2cc_fast import Fast

CLAIMED = {6, 10, 18}

class Hunt(Fast):
    def __init__(self, **kw):
        super().__init__(**kw)
        self.mile = 0
        self.gen = 0
        self.gapmul = []          # gaps in current generation (L>=3)
        self.all_lengths = set()
        self.odd = []             # (step, gl)
        self.gap3 = []            # (step, gl==3)
        self.newval = []          # (step, gl) not in CLAIMED, L>=3
        self.gen_report = []      # (gen, sorted multiset)
        self.t0 = time.time()

    def on_milestone(self):
        self.mile += 1
        # 6 milestones per generation; boundary at every 6th (M1 of next gen)
        if self.mile % 6 == 1 and self.mile > 1:
            self.gen += 1
            ms = sorted(self.gapmul)
            self.gen_report.append((self.gen, ms))
            self.gapmul = []

    def on_gapmeet(self, gl):
        if gl < 3:
            return
        self.all_lengths.add(gl)
        self.gapmul.append(gl)
        if gl == 3:
            self.gap3.append((self.step, gl))
            print(f"[CANDIDATE HALT] gap==3 met by E at step={self.step}", flush=True)
        if gl % 2 == 1:
            self.odd.append((self.step, gl))
            print(f"[ANOMALY] ODD gap L={gl} met by E at step={self.step}", flush=True)
        if gl not in CLAIMED:
            self.newval.append((self.step, gl))
            print(f"[ANOMALY] gap L={gl} not in {sorted(CLAIMED)} at step={self.step}", flush=True)


if __name__ == "__main__":
    cap = int(float(sys.argv[1])) if len(sys.argv) > 1 else 1e18
    wall = float(sys.argv[2]) if len(sys.argv) > 2 else 300.0
    logbits = int(sys.argv[3]) if len(sys.argv) > 3 else 28
    h = Hunt(SZ=1 << logbits)
    chunk = 5 * 10**8
    last = 0
    while h.step < cap and not h.halted:
        h.run(min(h.step + chunk, cap))
        if time.time() - h.t0 > wall:
            print(f"[wall budget {wall}s reached]", flush=True)
            break
        if h.step == last:  # no progress (stuck / done)
            break
        last = h.step
    print(f"\n=== HUNT DONE: step={h.step} halted={h.halted} generations={h.gen} "
          f"milestones={h.mile} elapsed={time.time()-h.t0:.0f}s ===")
    print(f"distinct E-met gap lengths (L>=3) ever: {sorted(h.all_lengths)}")
    print(f"gap==3 events: {len(h.gap3)}   ODD gaps: {len(h.odd)}   "
          f"non-{sorted(CLAIMED)} gaps: {len(h.newval)}")
    print("per-generation gap multiset (L>=3):")
    for g, ms in h.gen_report:
        parity = 'even' if g % 2 == 0 else 'odd '
        exp = [18, 10, 6] if g % 2 == 0 else [18, 10]
        flag = '' if sorted(ms) == sorted(exp) else '  <<< DEVIATION'
        print(f"  gen#{g:>3} ({parity}): {ms}{flag}")
    if h.halted:
        print("\n[CANDIDATE HALT] machine HALTED -- verify independently")
    elif not (h.gap3 or h.odd):
        print("\nNo gap==3, no odd gap, no halt found in this envelope.")
