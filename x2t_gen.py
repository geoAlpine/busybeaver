#!/usr/bin/env python3
"""x2t_gen.py -- trace the machine and, between consecutive super-peaks (maxrun records),
log every event where the RIGHTWARD E-scanner (state E reading 0) ENTERS a maximal 0-run,
recording the run length. This is the halt-gate exposure stream. We check:
  (1) which run-lengths the E-scanner meets (halt iff exactly 3),
  (2) whether the per-generation exposure skeleton is UNIFORM across generations n.
"""
import sys
sys.path.insert(0, '/Users/aokiyousuke/busybeaver')
from mse_extract import parse, rle

SPEC = "1RB0RE_1RC---_0LD1LE_0RE1LD_1RF0LC_0RA1RE"
STN = "ABCDEF"
M = parse(SPEC)


def maxrun_of(tape, lo, hi):
    best = 0; cur = 0
    for i in range(lo, hi + 1):
        if tape[i] == 1:
            cur += 1
            if cur > best: best = cur
        else:
            cur = 0
    return best


def run(maxsteps, SZ=1 << 22):
    tape = bytearray(SZ); off = SZ // 2
    pos = off; st = 0; step = 0; lo = hi = pos
    peak = 0
    gen_events = []   # list of run-lengths E-scanner met in current generation
    gen_start = 0
    generations = []  # (peakval, [event lengths])
    while step < maxsteps:
        r = tape[pos]
        if st == 1 and r == 1:
            print(f"HALT step={step}"); return generations
        # detect E-scanner entering a maximal 0-run: state E (idx4) reading 0,
        # AND the cell to the left is not 0 (so this is the LEFT end of the run) -- actually
        # E writes 1 as it goes so left is 1; we detect run entry when st==E,r==0 and prev step
        # wasn't already inside. Simplest: st==E, r==0, and tape[pos-1]==1 (left boundary).
        if st == 4 and r == 0 and pos > lo and tape[pos - 1] == 1:
            # measure maximal 0-run to the right
            j = pos
            while j < SZ and tape[j] == 0: j += 1
            L = j - pos
            gen_events.append(L)
        act = M[st][r]
        ww, d, ns = act
        tape[pos] = ww; pos += d; st = ns; step += 1
        if pos < lo: lo = pos
        elif pos > hi: hi = pos
        # super-peak detection: at right-frontier turnaround (C reading 0), measure maxrun
        if st == 2 and tape[pos] == 0 and pos > off:
            L0 = lo
            while L0 < pos and tape[L0] == 0: L0 += 1
            mx = maxrun_of(tape, L0, pos)
            if mx > peak:
                if peak > 0:
                    generations.append((peak, mx, gen_events))
                peak = mx
                gen_events = []
    return generations


if __name__ == "__main__":
    cap = int(sys.argv[1]) if len(sys.argv) > 1 else 700000
    gens = run(cap)
    for pk_from, pk_to, evs in gens:
        from collections import Counter
        c = Counter(evs)
        odd3 = c.get(3, 0)
        print(f"gen {pk_from:>5}->{pk_to:>5}: {len(evs):>4} E-gap-entries  lens={dict(sorted(c.items()))}  gap3={odd3}")
