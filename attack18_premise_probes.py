#!/usr/bin/env python3
"""ATTACK #18 — premise-complement mining, fired 2026-07-25 (the last unfired (K) generator).

The catalogue's no-go layers rest on premises. #18 takes each premise's COMPLEMENT and asks what
would have to be true to evade it. Two of the complements turned out to be things NOBODY HAS
MEASURED, and both are cheap. This fires them.

PROBE A — the SUBWORD COMPLEXITY of 43's itinerary.
  Layers 2/5/6/11 all presuppose "the orbit carries no low-complexity structure". If the itinerary
  rho_j = G_j mod 3 had LINEAR factor complexity (Sturmian-like) or were k-automatic, phi would be
  computable outright and the whole (K) wall would be the wrong diagnosis. The premise has never
  been measured directly. Measuring p(n) = #distinct factors of length n settles it.

PROBE B — are the phi=1 seeds confined to EVENTUALLY PERIODIC orbits?
  Layer 1 kills seed-uniform bounds using the counterexample -14, which is a FIXED POINT. The
  complement: if every high-phi seed is eventually periodic, then "aperiodic => phi < 4/5" is a
  DIFFERENT target statement, not refuted by -14. This measures whether that is so.

No machine decided. No label upgraded.
"""
E = {0: 9, 1: 14, 2: 1}
def step(G):
    r = G % 3
    return r, (4*G + E[r]) // 3

def itinerary(seed, n):
    G = seed; out = []
    for _ in range(n):
        r, G = step(G)
        out.append(r)
    return out, G

print("=== PROBE A : subword complexity of 43's itinerary ===")
N = 400_000
it, _ = itinerary(43, N)
s = ''.join(map(str, it))
print(f"itinerary length {N};  symbol freqs: "
      f"0:{s.count('0')/N:.4f} 1:{s.count('1')/N:.4f} 2:{s.count('2')/N:.4f}   (phi = freq rho=1)")
print(f"{'n':>3} {'p(n)':>10} {'3^n':>12} {'p(n)/p(n-1)':>12}   reading")
prev = None
for n in range(1, 13):
    fac = set()
    for i in range(0, N - n):
        fac.add(s[i:i+n])
    p = len(fac)
    rat = (p/prev) if prev else 0
    lin = "LINEAR-ish" if p <= 2*n + 2 else ("sub-exponential" if p < 3**n else "= 3^n (full shift)")
    print(f"{n:>3} {p:>10} {3**n:>12} {rat:>12.4f}   {lin}")
    prev = p

print("\n=== PROBE B : are high-phi seeds eventually periodic? ===")
def phi_and_cycle(seed, n=20000, cyclen=4000):
    G = seed; ones = 0; seen = {}
    cyc = None
    for j in range(n):
        if cyc is None and j < cyclen:
            if G in seen: cyc = (seen[G], j)
            else: seen[G] = j
        r, G = step(G)
        if r == 1: ones += 1
        if abs(G) > 10**400: break
    return ones/n, cyc

print(f"{'seed':>6} {'phi':>8}  eventually periodic?")
hi = []
for seed in list(range(-60, 121)):
    p, cyc = phi_and_cycle(seed)
    if p > 0.60:
        hi.append((seed, p, cyc))
for seed, p, cyc in sorted(hi, key=lambda t: -t[1])[:25]:
    print(f"{seed:>6} {p:>8.4f}  {'YES cycle at ' + str(cyc) if cyc else 'no cycle found in 4000'}")
print(f"\nseeds with phi > 0.60 : {len(hi)} of 181 tested")
ap = [t for t in hi if t[2] is None]
print(f"of those, APERIODIC (no cycle in 4000 steps) : {len(ap)}")
if ap:
    print("  aperiodic high-phi seeds:", [(s, round(p,4)) for s,p,_ in ap][:12])
print("\nphi(43) =", round(itinerary(43, 200000)[0].count(1)/200000, 6))
