#!/usr/bin/env python3
"""
SPACE NEEDLE -- TRANSCENDENCE attack, structure probes.

(A) Is oddpart(m_n+1) SMOOTH / S-unit-like?  (effective "powers of 2 in
    sequences" theorems need a recurrence or an S-unit equation.)  We trial-
    factor the odd parts for the first many generations and report the LARGEST
    PRIME FACTOR / smoothness -- a generic integer has a large prime factor.
(B) v = trailing-ones distribution, and the MARGIN width(m_n) - v (=log2 oddpart
    roughly).  HALT needs v = width.  We report max(v) vs width along the orbit.
(C) Growth rate log(m_n)/n and the Baker angle: is log(growth)/log2 a "generic"
    (badly approximable-looking) constant?  Density -> exclusion is assessed.
(D) Does m_n satisfy any short linear recurrence? (Berlekamp-Massey-ish rank
    test over Q on the integer sequence -> if no low-order recurrence, the
    linear-recurrence powers theorems are INAPPLICABLE.)
"""
import sys
from sympy import factorint

def tz1(m):
    v = 0
    while m & 1:
        v += 1; m >>= 1
    return v

def f(m):
    v = tz1(m)
    return m + 3 * (m >> (v + 1)) + v

def oddpart(x):
    v = 0
    while x and (x & 1) == 0:
        v += 1; x >>= 1
    return x, v

if __name__ == "__main__":
    GENS = int(sys.argv[1]) if len(sys.argv) > 1 else 4000

    orbit = [2]
    m = 2
    for _ in range(GENS):
        m = f(m); orbit.append(m)
    print(f"[orbit] {GENS} gens; final width {orbit[-1].bit_length()} bits\n")

    # ---- (A) smoothness of oddpart(m_n+1) for first FACTLIM odd milestones ----
    print("[A] smoothness of oddpart(m_n+1) (odd milestones), first 40 that are")
    print("    small enough to factor (<~10^40). largest prime factor vs oddpart:")
    cnt = 0
    for n, mm in enumerate(orbit):
        if not (mm & 1):
            continue
        g, v = oddpart(mm + 1)
        if g == 1:
            print(f"    n={n}: oddpart=1  ->  HALT!"); continue
        if g < 10**40:
            fs = factorint(g)
            lpf = max(fs)
            smooth = lpf <= g**0.5   # rough: has no dominant huge prime
            print(f"    n={n:<4d} bitlen(m)={mm.bit_length():<5d} v={v:<2d} "
                  f"oddpart={g}  largestPrime={lpf}  ({'smoothish' if smooth else 'has big prime'})")
            cnt += 1
        if cnt >= 30:
            break

    # ---- (B) v distribution and margin width - v ----
    vs = [tz1(mm) for mm in orbit if (mm & 1)]
    from collections import Counter
    c = Counter(vs)
    print(f"\n[B] trailing-ones v distribution over {len(vs)} odd milestones:")
    for k in sorted(c)[:12]:
        print(f"    v={k:<3d}: {c[k]:<6d} ({100*c[k]/len(vs):.2f}%)  "
              f"[geometric ~2^-v predicts {100/2**k:.2f}%]")
    maxv = max(vs);
    # find that milestone's width
    for n, mm in enumerate(orbit):
        if (mm & 1) and tz1(mm) == maxv:
            print(f"    MAX v = {maxv} at n={n}, width(m)={mm.bit_length()} "
                  f"-> margin width-v = {mm.bit_length()-maxv} (HALT needs 0)")
            break

    # ---- (C) growth rate + Baker angle ----
    import math
    logs = [math.log(mm) for mm in orbit]
    rate = (logs[-1] - logs[100]) / (GENS - 100)   # nat-log per gen
    rate2 = rate / math.log(2)                       # bits per gen
    print(f"\n[C] growth: log(m_n)/n -> {rate:.6f} nat/gen = {rate2:.6f} bits/gen")
    print(f"    log2(5/2)={math.log2(2.5):.6f} (pure even), obs<that (odd steps slower)")
    # continued fraction of rate2 to see if 'generic'
    x = rate2; cf = []
    for _ in range(12):
        a = int(x); cf.append(a); x -= a
        if x < 1e-9: break
        x = 1/x
    print(f"    continued fraction of bits/gen: {cf}  (no small partial quotient => 'generic')")

    # ---- (D) linear recurrence test ----
    # Try to fit a linear recurrence of order up to R over the rationals using the
    # integer orbit; if the Hankel-type system has full rank for all R<=Rmax, NO
    # low-order recurrence exists.
    print("\n[D] linear-recurrence test (Hankel rank over Q):")
    from fractions import Fraction
    seq = [Fraction(x) for x in orbit[:60]]
    def has_recurrence(order):
        # solve for c_1..c_order with seq[i] = sum c_j seq[i-j], using 2*order eqns
        import itertools
        rows = []
        rhs = []
        for i in range(order, order + order + 4):
            if i >= len(seq): return None
            rows.append([seq[i-1-j] for j in range(order)])
            rhs.append(seq[i])
        # gaussian elim to check consistency
        import copy
        A = [r[:] + [rhs[k]] for k, r in enumerate(rows)]
        nr = len(A); nc = order
        piv = 0
        for col in range(nc):
            pr = None
            for r in range(piv, nr):
                if A[r][col] != 0: pr = r; break
            if pr is None: continue
            A[piv], A[pr] = A[pr], A[piv]
            inv = A[piv][col]
            A[piv] = [x/inv for x in A[piv]]
            for r in range(nr):
                if r != piv and A[r][col] != 0:
                    fac = A[r][col]
                    A[r] = [a - fac*b for a, b in zip(A[r], A[piv])]
            piv += 1
        # inconsistency: a row 0...0 | nonzero
        for r in range(nr):
            if all(A[r][c] == 0 for c in range(nc)) and A[r][nc] != 0:
                return False
        return True
    for order in range(1, 11):
        ok = has_recurrence(order)
        print(f"    order {order:2d}: consistent linear recurrence? {ok}")
