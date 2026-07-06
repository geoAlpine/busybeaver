#!/usr/bin/env python3
"""
o17 halt-relevant reduction on the BLANK orbit (2026-07-06).  [task 1 of the halt-flavor pin]

Static [PROVEN from table]:
  - F is entered ONLY by (D,0) -> 0LF;  D is entered ONLY by (A,1) -> 1LD.
  - Halt = F reads 0.  Chain: A reads 1 at q -> D at q-1; if tape[q-1]==0 -> F at q-2;
    halt iff tape[q-2]==0.
  - So   HALT  <=>  the config `0 0 [1]_A` occurs (A reads a 1 with both left neighbors 0).
    Local safety condition (o4-analog of "B never on left-1 of 11"):
        `A never reads a 1 whose two left neighbors are 0 0`.
  - NEAR MISS = F entered but reads 1  <=>  `1 0 [1]_A`.

Dynamic [OBSERVED]: blank-tape run (default 2*10^7 steps), counting
  - A-reads-1 events (D entries), their left-neighbor split,
  - F entries (near misses), with radius-5 window census at the A-reads-1 moment,
  - saturation curve of the window set, and the safety margin (all F reads 1?).
No machine decided.
"""
import sys
from collections import Counter

SPEC = "1RB1LD_1RC0LE_1LA1RE_0LF1LA_1RB0RB_---0LB"

def parse(spec):
    M = []
    for st in spec.split('_'):
        row = []
        for t in (st[0:3], st[3:6]):
            row.append(None if t[0] == '-' else
                       (int(t[0]), 1 if t[1] == 'R' else -1, ord(t[2]) - ord('A')))
        M.append(row)
    return M

M = parse(SPEC)

def run(maxsteps=20_000_000, radius=5):
    SZ = 1 << 24
    tape = bytearray(SZ)
    pos = SZ // 2; st = 0; step = 0
    lo = hi = pos
    nA1 = 0                 # A reads 1  (D entries)
    nA1_left1 = 0           # ... with tape[pos-1]==1  (D will read 1 -> back to A, no F)
    nF = 0                  # F entries (near misses: D read 0)
    windows = Counter()     # radius-window at each F entry (A-reads-1 moment)
    sat = []                # (step, #distinct windows) saturation curve
    frontier_F = 0          # F entries where everything left of head is blank
    while step < maxsteps:
        r = tape[pos]
        if st == 5 and r == 0:
            print(f"HALT at step {step}")
            return
        if st == 0 and r == 1:
            nA1 += 1
            if tape[pos-1] == 1:
                nA1_left1 += 1
            else:
                # D will read 0 -> F entered at pos-2; F reads tape[pos-2]
                nF += 1
                w = bytes(tape[pos-radius:pos+radius+1])
                if w not in windows:
                    sat.append((step, len(windows) + 1))
                windows[w] += 1
                if pos - 2 <= lo or all(tape[i] == 0 for i in range(lo, pos-1)):
                    frontier_F += 1
                assert tape[pos-2] == 1, f"F WOULD READ 0 -> HALT at step {step}"
        ww, d, ns = M[st][r]
        tape[pos] = ww; pos += d; st = ns; step += 1
        if pos < lo: lo = pos
        if pos > hi: hi = pos
    width = hi - lo + 1
    print(f"blank orbit, {maxsteps} steps, width={width}  (width/sqrt(step)={width/maxsteps**0.5:.3f})")
    print(f"A-reads-1 events (D entries): {nA1}")
    print(f"  left neighbor 1 (D reads 1, benign A/D alternation): {nA1_left1}")
    print(f"  left neighbor 0 -> F ENTERED (near miss):            {nF}")
    print(f"  F entries at the true left frontier (all-blank left): {frontier_F}")
    print(f"ALL {nF} F entries read 1 (pattern `1 0 [1]_A`): SAFE, zero `0 0 [1]_A`")
    print(f"distinct radius-{radius} windows at F entries: {len(windows)}")
    print("saturation curve (step, #windows):")
    for s, c in sat:
        print(f"   {s:>12,}  {c}")
    print("window census (window, count) - head cell in [brackets]:")
    for w, c in windows.most_common():
        s = ''.join(str(b) for b in w)
        print(f"   {s[:radius]}[{s[radius]}]{s[radius+1:]}   x{c}")

if __name__ == "__main__":
    n = int(sys.argv[1]) if len(sys.argv) > 1 else 20_000_000
    run(n)
