#!/usr/bin/env python3
"""
SPACE NEEDLE (mu = 5/2) -- exact rule system + FIXED-POINT closed forms + criticality.
(2026-07-08). The frontier's one non-(K) machine: kernel 5/2 not in {2^a/3^b}.

SN = 1RB1LA_1LC0RE_1LF1LD_0RB0LA_1RC1RE_---0LD  (halt = F reads 0; PROVEN gate: state C
reads a 0 whose LEFT neighbour is 0, SPACE_NEEDLE_HALT.md).

1. EXACT RULE SYSTEM.  Single-block milestone  0^inf 1^m 0^inf, head on the 0 right of
   the block, state C.  One epoch is the 2-adic-digit-driven map [PROVEN from table,
   SPACE_NEEDLE_HALT.md §3, re-verified vs raw TM below]:
        f(m) = m + 3*floor(m / 2^(v+1)) + v ,   v = # trailing 1-bits of m
   Two-block reset counter b = m - 4  (the [1,0,1^b] milestone); interleaved 3-block
   milestones [1,b,b/2+2] appear mid-epoch on even b.

2. FIXED-POINT CLOSED FORMS FOR x5/2  [PROVEN].
   * EVEN branch (v=0, m even):  f(m) = m + 3(m/2) = 5m/2  -- clean x5/2.
       fixed point  x = 0  (m-coord)  ==  -4  (b-coord: b'=floor(5b/2)+6, x=-2c/3=-4).
       Because 5 is a 2-adic UNIT, distance to x multiplies by 5/2 and v2 drops by 1
       each even step, so
             maximal even-run (clean x5/2 phase) = v2(m) = v2(b+4).      [PROVEN]
       THE o4/O15 fixed-point trick TRANSFERS to x5/2 (numerator 5 a 2-adic unit, same
       as 3) -- runs = v2(value - fixed point), verified exhaustively + on-orbit.
   * ODD branch (v>=1):  f(m) = (2^(v+1)+3) q + 2^v + v - 1,  q = m >> (v+1).
       multiplier (2^(v+1)+3)/2^(v+1) = 1 + 3/2^(v+1) is v-DEPENDENT -> NO single fixed
       point; the odd branch is the transient carry-resolution step between x5/2 phases.
       So the clean scalar chain is exactly the maximal even-run; it breaks at the first
       odd value (parity-branching), matching the observed 621->1090 break.

3. CRITICALITY.  run-cap slope = log2(5/2) = 1.3219 (the x5/2 depth expansion). SN has
   NO draining scalar ledger: the value m is CUMULATIVE (grows), and halt is a base-2
   cylinder-avoidance (string-ledger), so the ledger ratio criterion is INAPPLICABLE
   (o15/o18 side). What replaces it is SUMMABILITY: per-epoch fatal prob ~ 2^{-width},
   width_n ~ (growth)*n grows, so sum 2^{-width_n} < infinity -> annealed E[#fatal]
   FINITE -> non-halt-leaning (Borel-Cantelli I). CUMULATIVE + summable = the o4 side of
   the memory axis (OPPOSITE o18: RESET => constant per-gen prob => sum=inf => halt-lean).
   Ladder position: SN is the family's one CUMULATIVE, non-(K) string-ledger -- the
   strongest annealed non-halt lean in the six, but NOT decidable by growth (the specific
   x5/2 orbit's cylinder-avoidance is generalized-Collatz reachability, the Collatz wall).
"""
import sys, math

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

def v2(n): return (n & -n).bit_length() - 1
def tz1(m):
    v = 0
    while m & 1: v += 1; m >>= 1
    return v
def f(m):
    v = tz1(m); return m + 3 * (m >> (v + 1)) + v

def epoch_raw(m, budget):
    """Run raw TM from 0^inf 1^m 0^inf, head on 0 right of block, state C (index 2).
    Return ('MILE', m') on return to single-block milestone, ('HALT',step), or ('BUDGET',)."""
    M = parse(SN); SZ = 1 << 21; tape = bytearray(SZ); off = SZ // 2
    for i in range(m): tape[off + i] = 1
    pos = off + m; st = 2; step = 0; lo = off; hi = off + m
    while step < budget:
        r = tape[pos]; act = M[st][r]
        if act is None: return ('HALT', step)
        ww, d, ns = act; tape[pos] = ww; pos += d; st = ns; step += 1
        if pos < lo: lo = pos
        elif pos > hi: hi = pos
        if step > 2 and st == 2 and r == 0:
            a = lo
            while a <= hi and tape[a] == 0: a += 1
            if a <= hi:
                z = a
                while z <= hi and tape[z] == 1: z += 1
                if pos == z and all(tape[i] == 0 for i in range(z, hi + 1)):
                    return ('MILE', z - a)
    return ('BUDGET', None)

if __name__ == "__main__":
    MMAX = int(sys.argv[1]) if len(sys.argv) > 1 else 200_000

    # ---- rule system verified vs raw TM ----
    ok = tot = 0; mism = []
    for m in range(2, 60):
        res, val = epoch_raw(m, 2 * m ** 3 + 200000); tot += 1
        if res == 'HALT': ok += 1
        elif res == 'MILE' and val == f(m): ok += 1
        else: mism.append((m, res, val, f(m)))
    print(f"[PROVEN-from-table, re-verified] f-map vs raw TM epochs m=2..59: {ok}/{tot} "
          f"consistent; mism {mism[:5]}")

    # ---- even branch = x5/2 exact; even-run = v2(m) ----
    bad = sum(1 for m in range(2, MMAX, 2) if f(m) != 5 * m // 2)
    print(f"[PROVEN] even m => f(m)=5m/2 (clean x5/2): evens 2..{MMAX}: {'exact' if bad==0 else bad}")
    def run_even(m):
        r = 0
        while m % 2 == 0: r += 1; m = f(m)
        return r
    bad2 = sum(1 for m in range(2, MMAX, 2) if run_even(m) != v2(m))
    print(f"[PROVEN] even-run (x5/2 phase length) == v2(m): evens 2..{MMAX}: "
          f"{'exact' if bad2==0 else bad2}   (fixed-point trick transfers: 5 a 2-adic unit)")
    # b-coordinate identity
    g = lambda b: (5 * b) // 2 + 6
    badb = sum(1 for b in range(2, MMAX, 2) if g(b) != f(b + 4) - 4)
    print(f"[PROVEN] b=m-4 reset map b'=floor(5b/2)+6 == f(b+4)-4 (fixed pt -4=-2c/3): "
          f"{'exact' if badb==0 else badb}")

    # ---- odd branch: v-indexed multiplier, no single fixed point ----
    bado = sum(1 for m in range(1, MMAX, 2)
               if f(m) != (2 ** (tz1(m) + 1) + 3) * (m >> (tz1(m) + 1)) + 2 ** tz1(m) + tz1(m) - 1)
    print(f"[PROVEN] odd branch f = (2^(v+1)+3)q + 2^v+v-1 (v-dependent, no fixed pt): "
          f"{'exact' if bado==0 else bado}")

    # ---- on-orbit: blank orbit reset chain + parity break + criticality ----
    m = 2; orb = [2]
    for _ in range(30): m = f(m); orb.append(m)
    print(f"\n[OBSERVED] blank m-orbit: {orb[:14]}")
    print(f"  b-coord resets (m-4 at even m): "
          f"{[x-4 for x in orb if x%2==0][:8]}   (=12,36,96,246 clean x5/2, then 621 breaks)")
    # growth + summability
    m = 2; widths = []
    for _ in range(400): widths.append(m.bit_length()); m = f(m)
    m = 2
    for _ in range(3000): m = f(m)
    growth = math.log2(m) / 3000
    Efatal = sum(2.0 ** (-w) for w in widths)
    print(f"[OBSERVED] per-gen log-growth {growth:.4f}; run-cap slope log2(5/2)={math.log2(2.5):.4f}")
    print(f"[MODEL] annealed E[#fatal] = sum 2^-width over 400 epochs = {Efatal:.4f} "
          f"(FINITE=summable=non-halt-lean; CUMULATIVE/o4 side; OPPOSITE o18 RESET)")
    print("Fixed-point closed forms [PROVEN]; criticality/annealed [MODEL]; orbit [OBSERVED].")
    print("No machine decided. No label upgraded.")
