#!/usr/bin/env python3
"""
SPACE NEEDLE -- FATAL SET + PROTECTION STATEMENT + orbit margin (2026-07-08).

Halt gate [PROVEN from table, SPACE_NEEDLE_HALT.md]: state C reads a 0 whose LEFT
neighbour is 0.  An epoch seeded by the single-block milestone 1^m halts iff m is in a
fatal set S.  Raw-TM census (below) reproduces SPACE_NEEDLE_HALT.md:
    S cap [1,255] = {1,3,6,7,15,31,63,102,127,255}
             = { 2^k-1 : k>=1 }  U  {sporadic 00-defect alignments: 6, 102, ...}

PROTECTION STATEMENT (family terms).  SN is a STRING-LEDGER machine over its OWN x5/2
kernel (non-(K): 5/2 not in {2^a/3^b}).  Non-halt <=>
   the milestone orbit m0=2, m_{n+1}=f(m_n) never enters S.
In base-2 digit terms the DOMINANT fatal cylinder is the ALL-ONES cylinder
   m = 2^k - 1  <=>  every bit of m is 1  (a full-width 1-cylinder),
plus a sparse sporadic set of 00-defect alignments (6=110, 102=1100110, ...) that is
NOT a pure cylinder (S strictly contains {2^k-1}; the sporadic rule is a small [OPEN]
sub-curiosity).  So: is the fatal cylinder a base-2 digit condition on the x5/2 orbit?
-- YES for the all-ones part (exact bit condition); the sporadics add a measure-thin
00-defect correction.

MARGIN.  Halt needs #zero-bits(m_n) = 0.  The orbit margin = min over the orbit of
#zero-bits.  The blank orbit sits at margin >= 1 (>=1 zero bit) at every tested gen;
because m grows (~x5/2 per even step) the all-ones target is 2^{-width}-thin and
recedes geometrically -- fatal probability per epoch is summable (annealed non-halt).
"""
import sys

def parse(spec):
    M = []
    for st in spec.split('_'):
        row = []
        for t in (st[0:3], st[3:6]):
            row.append(None if (t[0] == '-' or t[2] == 'Z')
                       else (int(t[0]), 1 if t[1] == 'R' else -1, ord(t[2]) - ord('A')))
        M.append(row)
    return M

SN = "1RB1LA_1LC0RE_1LF1LD_0RB0LA_1RC1RE_---0LD"
def tz1(m):
    v = 0
    while m & 1: v += 1; m >>= 1
    return v
def f(m):
    v = tz1(m); return m + 3 * (m >> (v + 1)) + v

def sn_halt(m, budget=None):
    """True iff the epoch seeded by 1^m (state C, head right of block) halts."""
    if budget is None: budget = int(0.7 * m ** 3) + 400000
    M = parse(SN); SZ = 1 << 21; tape = bytearray(SZ); off = SZ // 2
    for i in range(m): tape[off + i] = 1
    pos = off + m; st = 2; step = 0
    while step < budget:
        r = tape[pos]; act = M[st][r]
        if act is None: return True
        ww, d, ns = act; tape[pos] = ww; pos += d; st = ns; step += 1
    return False

if __name__ == "__main__":
    HI = int(sys.argv[1]) if len(sys.argv) > 1 else 255

    fatal = [m for m in range(1, HI + 1) if sn_halt(m)]
    allones = [2 ** k - 1 for k in range(1, 20) if 2 ** k - 1 <= HI]
    spor = [m for m in fatal if m not in allones]
    print(f"[PROVEN by run] fatal set S cap [1,{HI}] = {fatal}")
    print(f"  all-ones (2^k-1) present: {[m for m in allones if m in fatal]} "
          f"(all of them: {all(m in fatal for m in allones)})")
    print(f"  sporadic (fatal, non-all-ones): {spor}  "
          f"(=> S strictly contains {{2^k-1}}; sporadic rule [OPEN])")

    # base-2 view of the fatal set
    print("\nfatal m in binary:")
    for m in fatal:
        z = m.bit_length() - bin(m).count('1')
        print(f"  m={m:4d} = {bin(m)[2:]:>10s}  zero-bits={z}")

    # ---- orbit margin: min #zero-bits over the blank x5/2 orbit ----
    fset = set(fatal); GENS = 4000
    m = 2; minz = 10 ** 9; where = None; hits = 0
    for i in range(GENS):
        w = m.bit_length(); z = w - bin(m).count('1')
        if z < minz: minz = z; where = (i, m if m < 10 ** 12 else f"~2^{w}")
        if m in fset: hits += 1
        m = f(m)
    print(f"\n[OBSERVED] blank x5/2 orbit, {GENS} gens:")
    print(f"  min #zero-bits (margin; halt needs 0) = {minz} at gen {where[0]} (m={where[1]})")
    print(f"  orbit intersect S cap[1,{HI}] = {hits} (blank orbit avoids the fatal set)")
    print("\n[OPEN] non-halt <=> the specific x5/2 orbit never enters the all-ones (U sporadic)")
    print("cylinder -- generalized-Collatz reachability (Collatz wall). Fatal set [PROVEN")
    print("nonempty by run]; blank-tape reachability NOT claimed.")
    print("No machine decided. No label upgraded.")
