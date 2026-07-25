#!/usr/bin/env python3
"""ATTACK #18, probe B extended (2026-07-25): is the phi=1 obstruction confined to periodic points?

Layer 1 of the no-go stack kills seed-uniform bounds with the counterexample seed -14 (phi = 1).
-14 is a FIXED POINT. If EVERY high-phi integer seed is eventually periodic, then the exceptional
set within Z is a characterisable (finite?) set, and "aperiodic integer seed => phi < 4/5" is a
DIFFERENT target statement that -14 does not refute. This sweeps a large seed range to test it.

No machine decided. No label upgraded.
"""
E = {0: 9, 1: 14, 2: 1}
def run(seed, n=4000, cyclen=2000):
    G = seed; ones = 0; seen = {}; cyc = None
    for j in range(n):
        if cyc is None and j < cyclen:
            if G in seen: cyc = seen[G]
            else: seen[G] = j
        r = G % 3
        G = (4*G + E[r]) // 3
        if r == 1: ones += 1
        if abs(G) > 10**300: break
    return ones/n, cyc

LO, HI = -200000, 200000
hi = []; per = []
for seed in range(LO, HI+1):
    p, cyc = run(seed)
    if cyc is not None: per.append((seed, p, cyc))
    if p > 0.60: hi.append((seed, p, cyc))
print(f"swept {HI-LO+1} integer seeds in [{LO}, {HI}]")
print(f"  eventually periodic (cycle found within 2000 steps) : {len(per)}")
print(f"  phi > 0.60                                          : {len(hi)}")
print(f"  phi > 0.60 AND aperiodic                            : {len([t for t in hi if t[2] is None])}")
print("\nall seeds with phi > 0.60:")
for s,p,c in sorted(hi, key=lambda t:-t[1])[:20]:
    print(f"   seed {s:>8}  phi={p:.4f}  {'periodic@'+str(c) if c is not None else 'APERIODIC'}")
print("\nall eventually-periodic seeds found (these are the exceptional set within Z):")
for s,p,c in per[:40]:
    print(f"   seed {s:>8}  phi={p:.4f}  cycle entered at step {c}")
print(f"\nmax phi over APERIODIC seeds: "
      f"{max((p for s,p,c in ((s,)+run(s) for s in range(LO,HI+1,97)) if c is None), default=0):.4f}"
      f"   (sampled every 97th seed)")
