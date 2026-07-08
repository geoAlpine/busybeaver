#!/usr/bin/env python3
"""
o13/o14 fixed-point deep dive, part 5: HALT MECHANIC + PROTECTION + FATAL SET (2026-07-08).

o13 halt = D->E leftward eat-sweep consumes an EVEN-length run of 1s (o10 twin, [PROVEN mechanic
  REDUCE_O11_O16 sec1]).  Protection statement: EVERY such sweep run is ODD.  We instrument the
  blank orbit: at each D->E entry record the maximal left run L of 1s consumed and its parity.
o14 halt = C->F leftward step lands on a 0 (00-gap; F entered only via C:0->1LF, [PROVEN mechanic]).
  Protection: at every C-reads-0 precursor the left neighbor is 1.  We record the left neighbor.

Plus cheap standalone FATAL probes (mutant milestone configs that HALT = concrete fatal members).
All halts PROVEN-by-run; protection [OBSERVED on the stated horizon]; blank reachability [OPEN].
"""
import sys
from msea_struct2 import parse

S13 = "1RB0LC_0LC0RF_1RD1LC_0RA1LE_---0LD_1LF1LA"
S14 = "1RB0LC_1LC0RD_1LF1LA_1LB1RE_1RB1LE_---0LE"

def instrument_o13(N):
    M = parse(S13)
    SZ = 1 << 24
    tape = bytearray(SZ); pos = SZ // 2; st = 0; step = 0
    from collections import Counter
    par = Counter(); Ls = []; halted = None; nvisit = 0
    prev_st = -1; prev_pos = -1
    while step < N:
        r = tape[pos]; act = M[st][r]
        if act is None:
            halted = step; break
        # D->E entry: st==D(3) reads 1 -> writes 1LE; the eat-sweep begins.
        if st == 3 and r == 1:
            # measure maximal run of 1s extending LEFT from pos (the run E will eat)
            j = pos; L = 0
            while tape[j] == 1:
                L += 1; j -= 1
            nvisit += 1
            par[L & 1] += 1
            if len(Ls) < 40: Ls.append(L)
        ww, d, ns = act
        tape[pos] = ww; pos += d; st = ns; step += 1
    # entry-cell-included run L: states alternate D,E,D,E..; terminating 0 read in E (HALT) iff L ODD.
    print(f"o13: D->E eat-sweeps in {N} steps: {nvisit}; run-parity census {{even(safe):{par[0]}, odd(FATAL):{par[1]}}}")
    print(f"     sample eaten-run lengths L (entry-incl): {Ls[:24]}  (halt <=> some L ODD; REDUCE entry-excl = L-1 even)")
    print(f"     halt: {halted}")
    return par

def instrument_o14(N):
    M = parse(S14)
    SZ = 1 << 24
    tape = bytearray(SZ); pos = SZ // 2; st = 0; step = 0
    from collections import Counter
    nb = Counter(); halted = None; nvisit = 0
    while step < N:
        r = tape[pos]; act = M[st][r]
        if act is None:
            halted = step; break
        # C(2) reads 0 -> 1LF ; F then reads the cell to the LEFT. halt <=> that cell is 0.
        if st == 2 and r == 0:
            left = tape[pos - 1]
            nb[left] += 1
            nvisit += 1
        ww, d, ns = act
        tape[pos] = ww; pos += d; st = ns; step += 1
    print(f"o14: C-reads-0 precursors in {N} steps: {nvisit}; left-neighbor census {{0(FATAL):{nb[0]}, 1(safe):{nb[1]}}}")
    print(f"     halt: {halted}")
    return nb

# ---- cheap standalone fatal probes (reachable-form family; a HALT = fatal member) ----
def fatal_o13(budget=400_000):
    M = parse(S13); halts = []; tried = 0
    for a in range(2, 14):
        for b in range(1, 12):
            for m in (0, 1, 2, 3):
                blocks = [a, b] + [1] * m
                SZ = 1 << 18; tape = bytearray(SZ); p = SZ // 2; lo = p
                for i, bl in enumerate(blocks):
                    for _ in range(bl): tape[p] = 1; p += 1
                    p += 1
                pos = lo; st = 2; step = 0; tried += 1
                while step < budget:
                    r = tape[pos]; act = M[st][r]
                    if act is None:
                        halts.append(((a, b, m), step)); break
                    ww, d, ns = act; tape[pos] = ww; pos += d; st = ns; step += 1
    print(f"o13 fatal probe (family [a,b,(10)^m], C@leftmost): {len(halts)}/{tried} HALT")
    print(f"     smallest fatal (a,b,m)@step: {halts[:8]}")

def fatal_o14(budget=400_000):
    M = parse(S14); halts = []; tried = 0
    for a in range(2, 14):
        for b in range(1, 10):
            for f in (0, 1, 2):
                blocks = [a, 1, b] + [1] * f + [4, 4, 2]
                SZ = 1 << 18; tape = bytearray(SZ); p = SZ // 2; lo = p
                for i, bl in enumerate(blocks):
                    for _ in range(bl): tape[p] = 1; p += 1
                    p += 1
                pos = lo; st = 4; step = 0; tried += 1
                while step < budget:
                    r = tape[pos]; act = M[st][r]
                    if act is None:
                        halts.append(((a, b, f), step)); break
                    ww, d, ns = act; tape[pos] = ww; pos += d; st = ns; step += 1
    print(f"o14 fatal probe (family [a,1,b,1^f,4,4,2], E@leftmost): {len(halts)}/{tried} HALT")
    print(f"     smallest fatal (a,b,f)@step: {halts[:8]}")

if __name__ == "__main__":
    N = int(sys.argv[1]) if len(sys.argv) > 1 else 50_000_000
    instrument_o13(N)
    instrument_o14(N)
    print()
    fatal_o13()
    fatal_o14()
    print("\nHalts PROVEN-by-run; protection [OBSERVED]; blank reachability [OPEN].")
    print("No machine decided. No label upgraded.")
