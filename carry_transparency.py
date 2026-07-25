#!/usr/bin/env python3
"""Carry-transparency boundary (2026-07-25): the possible/impossible line for BB(6) cryptid cores.

A Collatz core c -> floor(mu*c), mu = 2^a/3^b, on a base-2 tape is carry-TRANSPARENT (=> exact
forall-g transport => template-provable) iff mu is a power of the base 2. An odd prime factor 3
turns the multiply into a base-2 addition (c + 2c) whose carry chains are orbit-dependent and
growing = the depth process = (K).

- x2  (mu = 2): x2 is a pure left shift => carry-chain length identically 0 (PROVEN transparent).
- Antihydra (mu = 3/2): x3 = c + 2c ripples carries; composed with /2 floor => depth D_n = (K).

No machine decided. No label upgraded.
"""
from collections import Counter
import statistics


def maxcarry_x3(c):
    """Max carry-run length of the base-2 addition c + 2c (= the x3 step)."""
    a, b = c, c << 1
    carry = 0; maxrun = 0; run = 0
    while a or b or carry:
        s = (a & 1) + (b & 1) + carry
        if s >= 2:
            carry = 1; run += 1; maxrun = max(maxrun, run)
        else:
            carry = 0; run = 0
        a >>= 1; b >>= 1
    return maxrun


if __name__ == '__main__':
    print("x2 (mu=2 = base-2 shift): carry-chain length = 0 for ALL c  [PROVEN transparent]")
    c = 8; chains = []
    for _ in range(3000):
        chains.append(maxcarry_x3(c)); c = (3 * c) // 2
    dist = Counter(chains)
    print(f"Antihydra (mu=3/2) N=3000: max carry-chain={max(chains)} mean={statistics.mean(chains):.3f} (growing)")
    print("  chain-len freq:", {k: dist[k] for k in sorted(dist)[:9]})
    print("  boundary: transparent IFF mu is a power of base 2; the odd prime 3 => growing")
    print("  orbit-dependent carry = depth process = (K). Simultaneous 2- and 3-transparency")
    print("  is impossible (2,3 mult. independent) = the Furstenberg obstruction, carry-side.")
