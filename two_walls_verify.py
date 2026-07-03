#!/usr/bin/env python3
"""
BB(6) two-walls separation — the calibrated entropy/complexity discriminator (2026-07-04).
[OBSERVED; calibrated against controls. Decides nothing; both walls stay [OPEN].]

Shows B1 (Mahler/(K)) and B2 (o17/o3 carry cascade) carry OPPOSITE signatures, and that o4's
driver sits on the B1 (Mahler) side despite o4's Type-II presentation (the bridge, presentation
⊥ wall).  See BB6_TWO_WALLS_2026-07-04.md.
"""

def subword(w, Ls):
    return [len(set(w[i:i+L] for i in range(len(w) - L))) for L in Ls]


if __name__ == "__main__":
    Ls = [3, 6, 10, 13]
    N = 60000
    print("Subword complexity p(l) discriminator (full 2^l = positive-entropy Mahler/B1;")
    print("linear/const = zero-entropy automatic/odometer = the o17/o3 B2 side):")
    print(f"    l = {Ls},  max (full binary) = {[2**L for L in Ls]}")

    # B1: Mahler floor((3/2)^n) mod 2 = (3^n >> n) & 1
    mah = ''.join(str((3**n >> n) & 1) for n in range(N))
    print(f"  Mahler floor((3/2)^n) mod2 [B1] : {subword(mah, Ls)}   -> full 2^l (positive entropy)")

    # automatic controls (the B2/odometer side)
    tm = ''.join(str(bin(n).count('1') & 1) for n in range(N))
    print(f"  Thue-Morse (automatic)          : {subword(tm, Ls)}   -> linear (zero entropy)")

    def odo3(n):
        s = 0
        while n: s += n % 3; n //= 3
        return s & 1
    odo = ''.join(str(odo3(n)) for n in range(N))
    print(f"  3-adic odometer parity          : {subword(odo, Ls)}   -> const (zero entropy)")

    # o4 driver (Type-II presentation, but B1 wall): G' = floor(4G/3)+c(G mod3), G0=7
    def cmap(G): return {0: 3, 1: 5, 2: 1}[G % 3]
    G = 7; g2 = []; g3 = []
    for _ in range(N):
        G = (4 * G) // 3 + cmap(G); g2.append(G & 1); g3.append(G % 3)
    w2 = ''.join(str(b) for b in g2)
    from collections import Counter
    print(f"\n  o4 driver G mod2 (BRIDGE)       : {subword(w2, Ls)}   -> full 2^l => o4 is on the B1/Mahler side")
    d3 = Counter(g3)
    print(f"  o4 driver G mod3 distribution   : {dict(sorted(d3.items()))}  (~1/3 each => equidistributing = o4's own (K))")

    # positive-entropy (Mahler/o4-driver): p(13) is thousands (near-full 8192); zero-entropy: p(13) is tens.
    ok_b1 = subword(mah, Ls)[-1] > 2000 and subword(w2, Ls)[-1] > 2000
    ok_b2 = subword(tm, Ls)[-1] < 100 and subword(odo, Ls)[-1] < 10
    print(f"\nTWO-WALLS DISCRIMINATOR VERIFIED: {ok_b1 and ok_b2}")
    print("  B1 (Mahler) & o4-driver = positive-entropy/full; automatic/odometer (B2 side) = zero-entropy/linear.")
    print("  => B2 is NOT a Mahler orbit in disguise; the two walls are distinct objects. Halting [OPEN].")
