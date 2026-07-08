#!/usr/bin/env python3
"""
o11 refill-law deep dive, part 4: FIXED-POINT CLOSED FORMS for the sea map (2026-07-08).
(The O4_RUN_STRUCTURE / O15_FIXEDPOINT trick applied to o11's inner engine.)

Sea map T(m) = floor(3m/2) + 4, i.e. two affine branches:
  even m: m' = 3m/2 + 4        fixed point  x_e = -8   (x = 3x/2+4)
  odd  m: m' = (3m+7)/2        fixed point  x_o = -7   (2x = 3x+7)

THEOREM [two-line proof + exhaustive verification below]:
  distance to the branch fixed point multiplies by exactly 3/2 on a same-branch step
  (even: m'+8 = (3/2)(m+8); odd: m'+7 = (3/2)(m+7)), and branch membership is
  2-divisibility of that distance (m even <=> 2 | m+8; m odd <=> 2 | m+7). Hence
    maximal even-run starting at even m  =  v2(m+8)
    maximal odd-run  starting at odd  m  =  v2(m+7)
  and the mod-4 residue (which drives ALL of o11's fatality, per o11_refill_rules.py)
  is exactly the next depth level:
    m ≡ 0 (mod 4) <=> m even and v2(m+8) >= 2      m ≡ 2 (mod 4) <=> v2(m+8) = 1
    m ≡ 1 (mod 4) <=> m odd  and v2(m+7) >= 2      m ≡ 3 (mod 4) <=> v2(m+7) = 1
  Mirror coordinates: W = m+8: even steps are EXACTLY x3/2 (odd: W'=(3W-1)/2);
                      U = m+7: odd  steps are EXACTLY x3/2 (even: U'=(3U+1)/2).
  => o11's parity/residue itinerary is the 2-adic depth process of a x3/2 orbit —
  the SAME depth process as Antihydra (v2 under x3/2), o4 (v3 under x4/3),
  o15 (v3 under x8/3).

Run cap: run(m) <= log2(m+8); on the real sea orbit m_i ~ C (3/2)^i, so
  run at sea-index i <= i*log2(3/2) + O(1) ~ 0.585 i.

BUDGET/CRITICALITY: o11's epoch budget is the leading block k, drained at the
CONSTANT rate -4 per sea step (R1) — the drain does NOT couple to the residue
itinerary at all (contrast o4/Antihydra where runs drain the ledger). The
run-cap/budget-slope criticality criterion is therefore INAPPLICABLE within epochs;
in-epoch fatality is structurally absent (R1/R2 have no halt branch on the grids),
and ALL fatality sits in the terminal collapse rules (R4, R5-odd) — exactly ONE
exposure per epoch, at the epoch's self-determined end index e(k) = floor(k/4).
"""
import sys

def T(m):
    return (3 * m) // 2 + 4

def v2(n):
    return (n & -n).bit_length() - 1

def run_len(m):
    """Maximal same-parity run starting at m (measured by direct iteration)."""
    p = m & 1
    r = 0
    while (m & 1) == p:
        r += 1
        m = T(m)
    return r

def closed(m):
    return v2(m + 7) if m & 1 else v2(m + 8)

if __name__ == "__main__":
    MMAX = int(sys.argv[1]) if len(sys.argv) > 1 else 200_000
    bad = 0
    for m in range(1, MMAX + 1):
        if run_len(m) != closed(m):
            bad += 1
            if bad < 5:
                print(f"  MISMATCH m={m}: run {run_len(m)} vs closed {closed(m)}")
    print(f"run closed forms (even: v2(m+8), odd: v2(m+7)): exhaustive m=1..{MMAX}: {MMAX-bad}/{MMAX} exact")

    # mod-4 refinement check (trivial arithmetic, but assert it)
    bad4 = sum(1 for m in range(1, MMAX + 1)
               if (m % 4 == 0) != (m % 2 == 0 and v2(m + 8) >= 2)
               or (m % 4 == 2) != (m % 2 == 0 and v2(m + 8) == 1)
               or (m % 4 == 1) != (m % 2 == 1 and v2(m + 7) >= 2)
               or (m % 4 == 3) != (m % 2 == 1 and v2(m + 7) == 1))
    print(f"mod-4 <-> depth-level dictionary: {MMAX-bad4}/{MMAX} exact")

    # mirror coordinates exactness
    badw = 0
    for m in range(1, 5000):
        if m % 2 == 0 and 2 * (T(m) + 8) != 3 * (m + 8): badw += 1
        if m % 2 == 1 and 2 * (T(m) + 7) != 3 * (m + 7): badw += 1
        if m % 2 == 1 and 2 * (T(m) + 8) != 3 * (m + 8) - 1: badw += 1
        if m % 2 == 0 and 2 * (T(m) + 7) != 3 * (m + 7) + 1: badw += 1
    print(f"mirror coords (W=m+8 x3/2 on even, U=m+7 x3/2 on odd): {'exact' if badw==0 else f'{badw} FAIL'} on m<5000")

    # on-orbit: the real sea orbit T^i(2) — runs, cap, parity/mod-4 itinerary
    m = 2
    seq_par = []
    runs = []
    i = 0
    N = 4000
    ms = [2]
    for _ in range(N):
        m = T(m)
        ms.append(m)
    # maximal runs along the orbit + closed-form check at each run start
    i = 0
    okr = 0; totr = 0
    while i < N - 64:
        r_direct = 1
        while i + r_direct < N and (ms[i + r_direct] & 1) == (ms[i] & 1):
            r_direct += 1
        totr += 1
        if r_direct == closed(ms[i]):
            okr += 1
        i += r_direct
    print(f"on-orbit (T^i(2), i<={N}): maximal runs match closed form at every run start: {okr}/{totr}")
    import math
    caps = [(i, closed(ms[i]), math.log2(ms[i] + 8)) for i in range(N)]
    worst = max(caps, key=lambda t: t[1] - t[2])
    mx = max(caps, key=lambda t: t[1])
    print(f"run cap run<=log2(m+8): max run on orbit i<={N}: {mx[1]} (at i={mx[0]}, cap {mx[2]:.1f}); cap never violated: {all(c[1] <= c[2] for c in caps)}")
    # parity sequence non-(small-)periodicity — the reason no fixed modulus in c is exact
    par = bytes(x & 1 for x in ms)
    per = next((p for p in range(1, 1500) if par[:3000] == par[p:3000 + p]), None)
    print(f"parity sequence of T^i(2): smallest period <=1500 on window 3000: {per} (None = aperiodic at this scale)")
    print("Fixed-point closed forms [PROVEN] (2-line proof, verified exhaustively); orbit facts [OBSERVED].")
    print("No machine decided. No label upgraded.")
