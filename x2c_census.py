#!/usr/bin/env python3
"""x2c_census.py -- full-tape gap census. Periodically scan the ENTIRE finite tape support
and record the multiset of maximal 0-run (gap) lengths that exist ANYWHERE (interior gaps,
excluding the two infinite background runs). Question: does a gap of length exactly 3 (or
any odd>=3) ever exist on the tape in the mature regime? Distinguishes a STATIC tape-language
invariant ('no gap 3 exists') from a DYNAMIC one ('E never MEETS a gap of 3')."""
import sys
sys.path.insert(0, '/Users/aokiyousuke/busybeaver')
from mse_extract import parse

SPEC = "1RB0RE_1RC---_0LD1LE_0RE1LD_1RF0LC_0RA1RE"
M = parse(SPEC)


def run(maxsteps, sample_every, SZ=1 << 23):
    tape = bytearray(SZ)
    off = SZ // 2
    pos = off
    st = 0
    step = 0
    lo = hi = pos
    ever_gap = {}          # gap length -> first step it was seen existing on tape (interior)
    gap3_when = []         # steps where a gap of exactly 3 exists on tape
    nextsamp = sample_every
    while step < maxsteps:
        r = tape[pos]
        act = M[st][r]
        if act is None:
            return ('HALT', step, ever_gap, gap3_when)
        ww, d, ns = act
        tape[pos] = ww
        pos += d
        st = ns
        step += 1
        if pos < lo:
            lo = pos
        elif pos > hi:
            hi = pos
        if step >= nextsamp:
            nextsamp += sample_every
            # scan interior gaps between first and last 1
            L0 = lo
            while L0 <= hi and tape[L0] == 0:
                L0 += 1
            R0 = hi
            while R0 >= L0 and tape[R0] == 0:
                R0 -= 1
            i = L0
            has3 = False
            while i <= R0:
                if tape[i] == 0:
                    j = i
                    while j <= R0 and tape[j] == 0:
                        j += 1
                    g = j - i
                    if g not in ever_gap:
                        ever_gap[g] = step
                    if g == 3:
                        has3 = True
                    i = j
                else:
                    i += 1
            if has3:
                gap3_when.append(step)
    return ('MAX', step, ever_gap, gap3_when)


if __name__ == "__main__":
    cap = int(sys.argv[1]) if len(sys.argv) > 1 else 10_000_000
    se = int(sys.argv[2]) if len(sys.argv) > 2 else 1
    out, step, ever, g3 = run(cap, se)
    print(f"outcome={out} step={step} sample_every={se}")
    print("Interior gap lengths ever seen on tape (len : first-step-seen):")
    for g in sorted(ever):
        par = 'ODD' if g % 2 else 'even'
        flag = '  <== ODD>=3 EXISTS on tape' if (g >= 3 and g % 2) else ''
        print(f"  gap={g:>4} ({par}): first@{ever[g]}{flag}")
    print(f"\nsamples where a gap==3 exists somewhere on tape: {len(g3)}")
    if g3:
        print(f"  e.g. steps: {g3[:20]}")
