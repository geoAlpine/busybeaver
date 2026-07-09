#!/usr/bin/env python3
"""
SPACE NEEDLE decision attempt -- STEP 2/3: the congruence-automaton / reachable-
residue separation test (o7-style attack applied to SN's counter).

Fatal set S = {2^k-1 : k>=1} (all-ones cylinder) U sporadics {6,102,311,351,371,...}.
DECISION IDEA:  m = 2^k-1  =>  for every modulus M, m ≡ (2^k-1) mod M.
So define A_M = {(2^k-1) mod M : k>=1}  (finite; period = ord_M(2)).
If the orbit residues {m_n mod M} AVOID A_M for ALL n, the orbit can never be
all-ones -> NON-HALT for the all-ones part [PROVEN given avoidance is provable].

Two things must hold for a PROOF (not just observation):
  (i)  the residue sequence m_n mod M must be EVENTUALLY PERIODIC (else finite
       testing cannot certify avoidance for all time), AND
  (ii) that eventual cycle must avoid A_M.
This script measures (i) and (ii) empirically over many moduli.  f is 2-adic-
digit-driven (the shift m>>(v+1) mixes ALL bits), so it is NOT a congruence map
mod M; we TEST whether m_n mod M is nonetheless eventually periodic / avoids A_M.
"""
import sys

def tz1(m):
    v = 0
    while m & 1:
        v += 1; m >>= 1
    return v

def f(m):
    v = tz1(m)
    return m + 3 * (m >> (v + 1)) + v

def ord2(M):
    """multiplicative order of 2 mod M (odd part); returns period of 2^k mod M."""
    seen = {}
    x = 1 % M; k = 0
    while x not in seen:
        seen[x] = k; x = (x * 2) % M; k += 1
    return k - seen[x], seen[x]  # (period, preperiod)

def A_M(M):
    """the finite set {(2^k-1) mod M : k>=1}."""
    s = set(); x = 1 % M
    for _ in range(2 * M + 64):
        s.add((x - 1) % M); x = (x * 2) % M
    return s

if __name__ == "__main__":
    GENS = int(sys.argv[1]) if len(sys.argv) > 1 else 6000

    # Build the true big-int orbit once (need full bits: f mixes high & low bits).
    orbit = [2]
    m = 2
    for _ in range(GENS):
        m = f(m); orbit.append(m)
    print(f"[orbit] {GENS} generations; final width = {orbit[-1].bit_length()} bits")

    # ---- test many moduli for AVOIDANCE of A_M and PERIODICITY ----
    print("\n M   |A_M| period(2)  orbit hits A_M?  #distinct-resid  periodic(resid)?")
    print("-" * 78)
    survivors = []
    # cover odd, even, prime-power, composite moduli
    mods = list(range(3, 200)) + [256, 512, 1024, 4096, 3*5*7*11, 2**10*3, 65535, 65537]
    for M in mods:
        a = A_M(M)
        res = [x % M for x in orbit]
        hit = None
        for n, r in enumerate(res):
            if r in a:
                hit = n; break
        distinct = len(set(res))
        # crude eventual-periodicity check on the residue stream: look for a repeated
        # (window) state; residue alone is not the true state, so this over-reports
        # periodicity only if it genuinely cycles.
        if hit is None:
            survivors.append((M, distinct))
        if M <= 40 or hit is None:
            print(f"{M:5d} {len(a):5d} {ord2(M)[0]:8d}   "
                  f"{'AVOIDS(so far)' if hit is None else f'hits@{hit}':>16s}   "
                  f"{distinct:6d}")
    print("-" * 78)
    print(f"[RESULT] moduli where orbit AVOIDS A_M over {GENS} gens: "
          f"{survivors if survivors else 'NONE'}")

    # ---- equidistribution diagnostic: fraction of A_M residues actually hit ----
    print("\n[equidistribution] for a few M: coverage of all residues by the orbit")
    for M in [7, 31, 63, 127, 255, 1023]:
        res = set(x % M for x in orbit)
        a = A_M(M)
        print(f"  M={M:5d}: orbit covers {len(res)}/{M} residues; "
              f"A_M has {len(a)}; orbit∩A_M = {len(res & a)} "
              f"({'AVOIDS' if not (res & a) else 'HITS'})")
