#!/usr/bin/env python3
"""x32c_o7_v2.py -- x3/2-family census cleanup, TASK B (2026-07-08):
o7's thin-set census deepened: v2(a+3) / oddpart(a+3) over >= 10^6 milestones,
the EXACT dynamics on v2, and the protection statement in family terms.

o7 = 1RB0RB_1LC1RE_1LF0LD_1RA1LD_1RC1RB_---1LC   (halt F,0)
Verified automaton (x32_o7_reduction.py, [OBSERVED 0-mismatch + seeded]):
    a even >= 2: (a,b) -> (3a/2 + 1 + b, 1)
    a odd  >= 5: (a,b) -> ((a-3)/2, b + (a+5)/2)
    a = 3:       (a,b) -> (b+5, 1 + [b odd])
    a = 1:       HALT
HALT <=> some milestone has a+3 = 2^k (k>=2), i.e. oddpart(a+3) = 1  [PROVEN given automaton].

EXACT v2 DYNAMICS derived here [PROVEN given automaton] (u = a+3, d = v2(u), w = oddpart(u)):
 (D1) cascade countdown: odd branch has fixed point x = -3 (2x = x-3), contraction 1/2:
      u' = u/2 exactly, so v2 counts down 1 per milestone from d to 0 -- run length = v2(a+3),
      the family fixed-point run law (o4's Theorem-2 mechanism, ratio 1/2 instead of 3/2).
 (D2) cascade exit ledger: entering at (a,B) odd, the cascade exits after d milestones at
      a_exit = w - 3 (even, if w >= 5) with b_exit = B + (u - w) + d   [odd steps add u/2^{k+1}+1].
 (D3) first even step after a cascade: a1 = 3(w-3)/2 + 1 + b_exit, so u1 = (3w-1)/2 + b_exit.
 (D4) even chains (b=1 after every even step): fixed point x = -4 (2x = 3x+4), ratio 3/2:
      a+4 -> 3(a+4)/2 exactly, chain length = v2(a+4).
 (D5) so the NEXT entry depth is d' = v2(3^e * x1 / 2^e - 1), x1 = u1 + 1, e = v2(x1):
      d' is a function of (w, b_exit) -- of the full value, NOT of d alone. v2 is a
      deterministic countdown INSIDE a run (closed form D1) but has NO autonomous
      entry-to-entry law; statistically the entry depths are geometric 2^-d [OBSERVED].
FATALITY requires oddpart(u) = 1, i.e. d = bitlen(u) - 1: a single 2-adic return of depth
      equal to the WHOLE bit-length (~ 0.2 bits/milestone, growing), vs observed max ~22.

SOUNDNESS: finite checks only; nothing here proves non-halting. No machine decided.
usage: x32c_o7_v2.py [milestones=1_000_000]
"""
import sys

def v2(n):
    return (n & -n).bit_length() - 1

def step_map(a, b):
    if a == 1:
        return None
    if a == 3:
        return (b + 5, 1 + (b % 2))
    if a % 2 == 0:
        return (3 * a // 2 + 1 + b, 1)
    return ((a - 3) // 2, b + (a + 5) // 2)

# ---------------------------------------------------------------- exhaustive small checks
def exhaustive(nmax=200_000):
    bad1 = bad2 = bad3 = 0
    # (D1) countdown
    for a in range(5, nmax, 2):
        a2 = (a - 3) // 2
        if a2 + 3 != (a + 3) // 2 or v2(a2 + 3) != v2(a + 3) - 1:
            bad1 += 1
    # (D4) even-chain law from (a, 1)
    for a0 in range(2, nmax, 2):
        a, b = a0, 1
        cnt = 0
        while a % 2 == 0:
            if (3 * a // 2 + 1 + b) + 4 != 3 * (a + 4) // 2:
                bad2 += 1
            a, b = 3 * a // 2 + 1 + b, 1
            cnt += 1
        if cnt != v2(a0 + 4):
            bad3 += 1
    print(f"exhaustive to {nmax:,}: (D1) countdown u'=u/2, v2 -1/step: {bad1} violations; "
          f"(D4) even chain a+4 -> 3(a+4)/2, length = v2(a+4): {bad2}+{bad3} violations")
    return bad1 == bad2 == bad3 == 0

# ---------------------------------------------------------------- the 10^6-milestone census
def census(N):
    a, b = 2, 2                      # first parsed milestone of the blank orbit
    n = 0
    entries = 0
    hist = {}
    maxd = 0; maxd_at = 0; maxd_bits = 0
    minw = None; minw_at = 0
    a3_hits = 0
    # per-decade min bitlen(oddpart) (decade of the entry index)
    dec_min = {}
    # formula verification (D2)/(D3)
    in_casc = False; ent = None
    d2_checked = d2_bad = d3_bad = 0
    check_even = None
    # entry-to-entry transition matrix d -> d' (capped at 8+)
    trans = {}
    last_d = None
    cps = sorted({10**3, 10**4, 10**5, 5 * 10**5, N})
    ci = 0
    print(f"census: {N:,} milestones from (2,2), exact bigints")
    print(f"  {'n':>8} {'entries':>8} {'bits(a)':>8} {'bits/mil':>8} {'maxd':>5} {'min w':>6}")
    while n < N:
        if a == 1:
            print(f"  HALT at n={n}"); return False
        if a & 1:
            if a == 3:
                a3_hits += 1
                a, b = b + 5, 1 + (b % 2)
                in_casc = False
                n += 1
                continue
            if not in_casc:                       # cascade ENTRY
                u = a + 3; d = v2(u); w = u >> d
                entries += 1
                hist[d] = hist.get(d, 0) + 1
                if d > maxd:
                    maxd, maxd_at, maxd_bits = d, n, u.bit_length()
                if minw is None or w < minw:
                    minw, minw_at = w, n
                dec = len(str(entries)) - 1
                wb = w.bit_length()
                if dec not in dec_min or wb < dec_min[dec]:
                    dec_min[dec] = wb
                dk = d if d <= 7 else 8
                if last_d is not None:
                    lk = last_d if last_d <= 7 else 8
                    trans[(lk, dk)] = trans.get((lk, dk), 0) + 1
                last_d = d
                ent = (u, d, w, b)
                in_casc = True
            a, b = (a - 3) // 2, b + (a + 5) // 2
        else:
            if in_casc:                           # cascade EXIT: check (D2), queue (D3)
                u, d, w, B = ent
                d2_checked += 1
                if a != w - 3 or b != B + (u - w) + d:
                    d2_bad += 1
                check_even = (3 * (w - 3) // 2 + 1 + (B + (u - w) + d),
                              (3 * w - 1) // 2 + (B + (u - w) + d))
                in_casc = False
            na, nb = 3 * a // 2 + 1 + b, 1
            if check_even is not None:
                if na != check_even[0] or na + 3 != check_even[1]:
                    d3_bad += 1
                check_even = None
            a, b = na, nb
        n += 1
        while ci < len(cps) and n >= cps[ci]:
            print(f"  {n:>8} {entries:>8,} {a.bit_length():>8,} {a.bit_length()/n:>8.4f} "
                  f"{maxd:>5} {minw if minw is not None and minw < 10**6 else '...'}")
            ci += 1
    tot = sum(hist.values())
    print(f"\n  cascade entries: {entries:,}; a=3-branch hits: {a3_hits}; "
          f"(D2) exit formula checked {d2_checked:,}: {d2_bad} bad; (D3) even-step formula: {d3_bad} bad")
    print(f"  depth d = v2(a+3) at entries vs geometric 2^-d:")
    for d in sorted(hist):
        print(f"    d={d:>2}: {hist[d]:>8,}  freq {hist[d]/tot:.5f}  (geom {2.0**-d:.5f})")
    print(f"  MAX depth = {maxd} at n={maxd_at:,} (u had {maxd_bits:,} bits there); "
          f"fatality needs d = bitlen(u)-1 ~ {a.bit_length():,} at the frontier")
    print(f"  min oddpart(a+3) at entries = {minw} at n={minw_at} (fatality needs 1; a=3 branch needs 3)")
    print(f"  min bitlen(oddpart) per entry-decade (10^k <= entry# < 10^(k+1)):")
    for dec in sorted(dec_min):
        print(f"    decade 10^{dec}: min bitlen(w) = {dec_min[dec]:,}")
    # conditional next-depth distribution: is P(d'|d) independent of d? (statistical only)
    print(f"  entry-to-entry transitions P(d'=1|d) and P(d'=2|d) (8 = '>=8'):")
    for dk in sorted({k[0] for k in trans}):
        row = sum(v for (i, j), v in trans.items() if i == dk)
        p1 = trans.get((dk, 1), 0) / row if row else 0
        p2 = trans.get((dk, 2), 0) / row if row else 0
        print(f"    d={dk}: n={row:>7,}  P(d'=1)={p1:.4f}  P(d'=2)={p2:.4f}   (geom: 0.5, 0.25)")
    same_d_diff = any(sum(1 for (i, j) in trans if i == dk) >= 2 for dk in {k[0] for k in trans})
    print(f"  d' NOT a function of d (same d, different d' observed): {same_d_diff} "
          f"-- v2 has no autonomous entry-to-entry law; countdown closed form only inside runs")
    return d2_bad == 0 and d3_bad == 0

if __name__ == "__main__":
    N = int(sys.argv[1]) if len(sys.argv) > 1 else 1_000_000
    ok1 = exhaustive()
    ok2 = census(N)
    print(f"\nPROTECTION (family terms): species = THIN-SET HITTING -- the fatal set "
          f"{{u = 2^k}} is one point per dyadic scale (relative measure 2^-bitlen(u), -> 0);")
    print("  margin = the ODD-PART GROWTH RATE: bitlen(oddpart(a+3)) = bitlen(a+3) - d grows "
          "linearly (~0.2 bits/milestone) while observed d stays O(log n);")
    print("  LEDGER-MEMORY: NO cumulative scalar ledger (b is never tested); the implicit "
          "string object (the 2-adic tail of a+3) is RECOMPUTED from the value at every entry "
          "-- RESET-per-entry, kin to o15's cylinder species, not Antihydra/o2's ledger.")
    print(f"\nall checks passed: {ok1 and ok2}")
    print("No machine decided. No label upgraded.")
