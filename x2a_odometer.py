#!/usr/bin/env python3
"""x2a_odometer.py -- EXACT ARITHMETIC REDUCTION of the integer-x2 base-2 odometer
    M = 1RB0RE_1RC---_0LD1LE_0RE1LD_1RF0LC_0RA1RE
to its milestone form and the arithmetic halt condition (INDEPENDENT cross-check of
the tape-template route). Interpreter: /Users/aokiyousuke/quantum-ecc/.venv/bin/python.

Milestone (the analogue of o4's M(G,a)):  head in state E, reading 0, strictly LEFT of
every 1 on the tape -- i.e. the eraser has just finished and the head sits at the left
frontier about to sweep right.  At such a milestone the tape is

        0^inf  [E] 0^G  1^b  <settled cascade tail>  0^inf

with G the LEADING GAP and 1^b the leading block.  The E-scanner immediately reads the
left end of the maximal 0-run 0^G, so by the PROVEN halt gate (E->F->A->B chain,
HALT <=> the E-scanner meets a maximal gap of length EXACTLY 3) the machine

        HALTS  <=>  G = 3   (at this or any E-meet).

This script extracts the exact (step, G, b) milestone stream over a long orbit, verifies
the halt gate is NEVER armed (G != 3, in fact G in {1} u {even}), and reads off the clean
doubling of the super-blocks (b = 2^k - 3, i.e. b' = 2b+3) -- the base-2 doubling engine.
SOUNDNESS: every printed fact is [OBSERVED, exact] unless marked [PROVEN]. Decides no
machine. Not committed."""
import sys
sys.path.insert(0, '/Users/aokiyousuke/busybeaver')
from mse_extract import parse

SPEC = "1RB0RE_1RC---_0LD1LE_0RE1LD_1RF0LC_0RA1RE"
M = parse(SPEC)


def run(maxsteps, SZ=1 << 25):
    tape = bytearray(SZ); off = SZ // 2
    pos = off; st = 0; step = 0; lo = hi = pos
    left1 = SZ                      # leftmost index holding a 1  (SZ == none)
    Gseq = []; Gcount = {}
    supers = []; seen = set()
    halted_G3 = None
    while step < maxsteps:
        r = tape[pos]; act = M[st][r]
        if act is None:
            return dict(outc='HALT', step=step, Gseq=Gseq, Gcount=Gcount,
                        supers=supers, haltG3=halted_G3)
        # milestone: state E(4) reading 0, head strictly left of leftmost 1
        if st == 4 and r == 0 and pos < left1 and left1 <= hi:
            G = left1 - pos
            j = left1; b = 0
            while j <= hi and tape[j] == 1:
                b += 1; j += 1
            Gseq.append((step, G, b)); Gcount[G] = Gcount.get(G, 0) + 1
            if G == 3 and halted_G3 is None:
                halted_G3 = step
            if b >= 5 and (b + 3) & (b + 2) == 0 and b not in seen:
                seen.add(b); supers.append((step, b))
        ww, d, ns = act
        # incremental maintenance of left1
        if ww == 1:
            if pos < left1:
                left1 = pos
        else:
            if pos == left1:
                k = pos + 1
                while k <= hi and tape[k] == 0:
                    k += 1
                left1 = k if k <= hi else SZ
        tape[pos] = ww; pos += d; st = ns; step += 1
        if pos < lo: lo = pos
        elif pos > hi: hi = pos
    return dict(outc='MAX', step=step, Gseq=Gseq, Gcount=Gcount,
                supers=supers, haltG3=halted_G3)


if __name__ == "__main__":
    cap = int(sys.argv[1]) if len(sys.argv) > 1 else 40_000_000
    R = run(cap)
    print(f"spec = {SPEC}")
    print(f"outcome = {R['outc']}   step = {R['step']:,}   milestones = {len(R['Gseq'])}")
    print()
    print("=== ARITHMETIC HALT GATE:  HALT <=> a met maximal gap G = 3 ===")
    print(f"  G == 3 ever armed?  {'YES *** HALT at step ' + str(R['haltG3']) if 3 in R['Gcount'] else 'NO -- gate never armed'}")
    print(f"  any ODD G >= 3 ever met?  {'YES ***' if any(g >= 3 and g % 2 for g in R['Gcount']) else 'NO'}")
    print("  leading-gap G histogram (all values are 1 or EVEN):")
    for G in sorted(R['Gcount']):
        flag = "   <-- ODD>=3 HALT-RELEVANT" if (G >= 3 and G % 2) else ""
        print(f"     G = {G:>4} : {R['Gcount'][G]}{flag}")
    print()
    print("=== BASE-2 DOUBLING ENGINE:  super-blocks b = 2^k - 3  (b' = 2b + 3) ===")
    for s, b in R['supers']:
        print(f"     step = {s:>11,}   block = 1^{b:<7}  b+3 = {b + 3} = 2^{(b + 3).bit_length() - 1}")
    print()
    print("  first 48 leading-gap values G_n:")
    print("   ", [g for _, g, _ in R['Gseq'][:48]])
