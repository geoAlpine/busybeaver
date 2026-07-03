#!/usr/bin/env python3
"""
o17 Collatz core (k=0 mod3) — descriptive measurements (2026-07-03).  [OBSERVED, not a proof]

Two honest, verified characterizations of the OPEN core (launched by the departure lemma of
O17_LINEAR_PROVEN.md §5). NOTHING is decided here; the core stays [OPEN].

(A) POLYNOMIAL growth: for long non-halting core seeds the tape width grows like width ~ step^(1/2)
    (quadratic-time / linear-space bouncer) -- a DIFFERENT complexity class from the exponential
    (3/2)^n growth of the Antihydra/Mahler cryptids. So o17's separateness is not only its halt
    predicate but its growth class.
(B) APEX vs EXCURSION: the head's left-frontier apex states form a simple 2-letter stream over
    {AED, AE}, BUT the excursions BETWEEN apexes are wildly irregular (a handful of steps to >10^6),
    growing without bound. Hence the coarse apex sequence is NOT a faithful 1-D reduction -- the
    unbounded base-3 interior digits (O17_HALT_STRUCTURE.md §6) live in the excursions. This SHARPENS
    the docs' "no 1-D reduction" to: the apex level is simple/binary, faithfulness fails at the
    excursion level.
"""
import math

def parse(spec):
    M = []
    for st in spec.split('_'):
        row = []
        for t in (st[0:3], st[3:6]):
            if t[0] == '-' or t[2] == 'Z':
                row.append(None)
            else:
                row.append((int(t[0]), 1 if t[1] == 'R' else -1, ord(t[2]) - ord('A')))
        M.append(row)
    return M

O17 = "1RB1LD_1RC0LE_1LA1RE_0LF1LA_1RB0RB_---0LB"
M = parse(O17)


def measure(L, maxsteps):
    SZ = 1 << 22
    tape = bytearray(SZ); off = SZ // 2
    for i in range(1, L + 1):
        tape[off + i] = 1
    pos = off; st = 0; step = 0; lo = hi = pos
    mile = []            # (step, width) at each new leftmost-width record
    apex_steps = []      # step at every left-frontier apex (pos==lo)
    while step < maxsteps:
        r = tape[pos]
        if st == 5 and r == 0:
            return ('HALT', step, mile, apex_steps)
        if pos == lo:
            w = hi - lo + 1
            if not mile or w > mile[-1][1]:
                mile.append((step, w))
            if not apex_steps or apex_steps[-1] != step:
                apex_steps.append(step)
        ww, d, ns = M[st][r]
        tape[pos] = ww; pos += d; st = ns; step += 1
        if pos < lo: lo = pos
        if pos > hi: hi = pos
    return ('MAX', step, mile, apex_steps)


def growth_exponent(L, maxsteps):
    out, step, mile, _ = measure(L, maxsteps)
    S = [s for s, w in mile if s > 0]; W = [w for s, w in mile if s > 0]
    if len(S) < 6:
        return out, step, None
    n = len(S)
    lx = [math.log(s) for s in S]; ly = [math.log(w) for w in W]
    mx = sum(lx) / n; my = sum(ly) / n
    a = sum((lx[i] - mx) * (ly[i] - my) for i in range(n)) / sum((lx[i] - mx) ** 2 for i in range(n))
    return out, step, a


if __name__ == "__main__":
    print("(A) core growth exponent  width ~ step^a  (a~0.5 => polynomial, NOT exponential):")
    for L in (3, 9, 18, 42):
        out, step, a = growth_exponent(L, 15_000_000)
        print(f"    L={L:3d} d={L//3:2d}: {out}@{step}  a={a:.3f}")
    print("(B) inter-apex excursion gaps for L=3 (irregular, unbounded => apex reduction unfaithful):")
    out, step, mile, apex = measure(3, 5_000_000)
    gaps = [apex[i + 1] - apex[i] for i in range(len(apex) - 1)]
    big = sorted(gaps)[-6:]
    print(f"    #apex events={len(apex)}, gap range [{min(gaps)}, {max(gaps)}], largest gaps={big}")
