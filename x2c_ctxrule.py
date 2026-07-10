#!/usr/bin/env python3
"""x2c_ctxrule.py -- extract the SOUND in-context gap-crossing behaviour. Each time the
E-scanner (state E reading 0, i.e. the start of the rightward halt-chain) sits at the LEFT
end of a maximal 0-run of length g>=2, record (g, left-context 6 cells, right-context 8
cells), then let the machine run and record where the head next re-crosses the right boundary
of that gap (exit state/side) and what the local tape became. This gives the real, reachable,
context-correct gap rule, and lets us see WHY g is always in {1,2,even}."""
import sys
sys.path.insert(0, '/Users/aokiyousuke/busybeaver')
from mse_extract import parse, rle

SPEC = "1RB0RE_1RC---_0LD1LE_0RE1LD_1RF0LC_0RA1RE"
STN = "ABCDEF"
M = parse(SPEC)


def rs(rr):
    return ' '.join(f"{c}^{n}" if n > 1 else f"{c}" for c, n in rr)


def run(start_step, ngap, SZ=1 << 22):
    tape = bytearray(SZ)
    off = SZ // 2
    pos = off
    st = 0
    step = 0
    lo = hi = pos
    seen = 0
    from collections import Counter
    rulecount = Counter()
    while step < 10 ** 12 and seen < ngap:
        r = tape[pos]
        act = M[st][r]
        if act is None:
            print(f"HALT step={step}")
            return
        # E reading 0 at left end of a maximal run of length g>=2
        if st == 4 and r == 0 and step >= start_step:
            g = 0
            j = pos
            while j < hi + 1 and tape[j] == 0:
                g += 1
                j += 1
            if 2 <= g <= hi - pos:  # a real interior gap bounded by a 1 on the right
                lc = rle(tape, max(lo, pos - 8), pos - 1)
                rc = rle(tape, j, min(hi, j + 8))
                par = 'ODD' if g % 2 else 'even'
                # left neighbor run just before gap, and right neighbor block length
                lblk = lc[-1] if lc else (1, 0)
                rblk = rc[0] if rc else (1, 0)
                key = (g, tuple(lc[-2:]), tuple(rc[:2]))
                rulecount[key] += 1
                if seen < 40:
                    print(f"  step={step:>9} E@gap0^{g}({par})  L[..{rs(lc)}] R[{rs(rc)}..]")
                seen += 1
        ww, d, ns = act
        tape[pos] = ww
        pos += d
        st = ns
        step += 1
        if pos < lo:
            lo = pos
        elif pos > hi:
            hi = pos
    print(f"\n distinct (g, Lctx2, Rctx2) rule-keys among {seen} E-gap events: {len(rulecount)}")
    # summarize by (g, left-neighbor-block-parity, right-neighbor-block)
    print(" gap-length distribution of E-met gaps (g>=2):")
    gc = Counter()
    for (g, lc, rc), c in rulecount.items():
        gc[g] += c
    for g in sorted(gc):
        print(f"   g={g:>3} ({'ODD' if g%2 else 'even'}): {gc[g]}")


if __name__ == "__main__":
    ss = int(sys.argv[1]) if len(sys.argv) > 1 else 100000
    ng = int(sys.argv[2]) if len(sys.argv) > 2 else 300
    run(ss, ng)
