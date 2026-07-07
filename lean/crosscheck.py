#!/usr/bin/env python3
"""Numeric cross-check mirroring the Lean statements in RunStructure.lean.

Mirrors (statement-for-statement):
  Theorem 1  (itinerary_inj)      : seeds mod 3^L <-> itineraries, L=1..8
  Theorem 2  (run_closed_form)    : run(G) = v3(G + e(G)), G = 1..200000
  Cor. 2.1   (run_cap/_orbit)     : 3^v3(n) <= |n|; 3^run <= G+14
  Stretch    (o15_conj/o15_queued): 3(5V'+c) = 8(5V+c); 3(V'-1) = 8(V-1)
  Anchors    : o4 real-orbit milestones from O4_LEDGER_ANALYSIS_2026-07-06 §5
"""

E = {0: 9, 1: 14, 2: 1}


def e(G):
    return E[G % 3]


def T(G):
    num = 4 * G + e(G)
    assert num % 3 == 0, (G, num)  # T_key
    return num // 3


def v3(n):
    n = abs(n)
    if n == 0:
        return 0
    r = 0
    while n % 3 == 0:
        n //= 3
        r += 1
    return r


def itin(G, L):
    out = []
    for _ in range(L):
        out.append(G % 3)
        G = T(G)
    return tuple(out)


def run_sim(G):
    rho, r = G % 3, 0
    while G % 3 == rho:
        r += 1
        G = T(G)
    return r


fails = []

# Theorem 1: bijection seeds mod 3^L <-> {0,1,2}^L, L = 1..8
for L in range(1, 9):
    its = {itin(g, L) for g in range(3**L)}
    if len(its) != 3**L:
        fails.append(f"bijection L={L}")
print("Theorem 1 (bijection L=1..8):", "OK" if not fails else fails)

# Theorem 2: run(G) = v3(G + e(G)), and Cor 2.1 caps, G = 1..200000
bad = 0
for G in range(1, 200001):
    R = v3(G + e(G))
    if run_sim(G) != R:
        bad += 1
    if 3 ** v3(G + e(G)) > G + 14:  # run_cap_orbit
        bad += 1
print("Theorem 2 + Cor 2.1 (G=1..200000):", "OK" if bad == 0 else f"{bad} FAIL")

# run_cap: 3^v3(n) <= |n| for n != 0 (both signs)
bad = sum(1 for n in range(-50000, 50001) if n != 0 and 3 ** v3(n) > abs(n))
print("run_cap (|n|<=50000):", "OK" if bad == 0 else f"{bad} FAIL")

# o4 real-orbit anchors (O4_LEDGER_ANALYSIS_2026-07-06 §5)
G, orb = 3, {}
for n in range(37):
    orb[n] = G
    G = T(G)
anchors = {0: 3, 5: 43, 9: 151, 12: 367, 20: 3727, 26: 20983, 31: 88462, 36: 372814}
ok = all(orb[n] == v for n, v in anchors.items())
print("o4 orbit anchors:", "OK" if ok else "FAIL")

# Stretch: o15 conjugation + queued/o18 push law
bad = 0
for c in (9, 11, -17, -5):
    for V in range(-500, 501):
        if (8 * V + c) % 3 == 0:
            Vp = (8 * V + c) // 3
            if 3 * (5 * Vp + c) != 8 * (5 * V + c):
                bad += 1
            if c == -5 and 3 * (Vp - 1) != 8 * (V - 1):
                bad += 1
            # valuation drop (8 a 3-adic unit)
            if (5 * V + c) % 3 == 0 and 5 * V + c != 0:
                if v3(5 * Vp + c) + 1 != v3(5 * V + c):
                    bad += 1
print("o15/o18 mirror identities:", "OK" if bad == 0 else f"{bad} FAIL")
