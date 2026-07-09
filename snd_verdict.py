#!/usr/bin/env python3
"""
SPACE NEEDLE decision attempt -- STEP 3/5: verdict.
 (a) orbit location vs the finite sporadic fatal part {6,102,311,351,371}
 (b) the FUNDAMENTAL obstruction: f is NOT a finite-state congruence -- f(m) mod M
     is NOT determined by m mod (M*2^j) for ANY fixed j (the shift m>>(v+1) drags
     UNBOUNDEDLY-high bits down), so NO mod-M / deep-parity-look-ahead automaton
     over-approximates the reachable set. This is the reason STEP 2 found no M.
 (c) margin trajectory: #zero-bits(m) and popcount(m+1) along the orbit (halt needs
     #zero-bits=0, i.e. m all-ones; sporadic-safe separately).
"""
def tz1(m):
    v = 0
    while m & 1:
        v += 1; m >>= 1
    return v
def f(m):
    v = tz1(m)
    return m + 3 * (m >> (v + 1)) + v

SPORADIC = {6, 102, 311, 351, 371}          # measured sporadic fatals (S ⊋ all-ones)
def allones(m): return (m & (m + 1)) == 0    # m = 2^k-1  <=>  m+1 is a power of 2

if __name__ == "__main__":
    # (a) orbit vs sporadic + all-ones membership, first many gens
    m = 2; orbit = [2]
    for _ in range(4000):
        m = f(m); orbit.append(m)
    small = [x for x in orbit if x <= 600]
    print("[LOCATION] orbit values <= 600:", small)
    print(f"  orbit ∩ sporadic{sorted(SPORADIC)} = "
          f"{sorted(set(orbit) & SPORADIC)}  (empty => never hit a small sporadic)")
    # after which gen is the orbit permanently past max(sporadic)=371?
    past = next(i for i, x in enumerate(orbit) if x > 371)
    print(f"  orbit is permanently > 371 (max known sporadic) from gen {past} "
          f"(m={orbit[past]}); strictly increasing thereafter: "
          f"{all(orbit[i] < orbit[i+1] for i in range(past, len(orbit)-1))}")
    hit_allones = [i for i, x in enumerate(orbit) if allones(x)]
    print(f"  orbit ∩ all-ones {{2^k-1}} over 4000 gens: "
          f"{'NONE' if not hit_allones else hit_allones}")

    # (b) the non-congruence obstruction, made concrete.
    #     For modulus M and low-bit depth j: find two values u,w with u≡w (mod 2^j)
    #     but f(u) not≡ f(w) (mod M). Existence for every j proves NO finite automaton.
    print("\n[OBSTRUCTION] f(m) mod M is NOT a function of m mod 2^j (any fixed j):")
    import random
    for M in (7, 31, 255):
        for j in (4, 8, 12, 16, 20):
            found = None
            rnd = random.Random(1)
            for _ in range(200000):
                low = rnd.getrandbits(j)
                # two m sharing the low j bits but different high bits
                u = low | (rnd.getrandbits(30) << j)
                w = low | (rnd.getrandbits(30) << j)
                if u and w and f(u) % M != f(w) % M:
                    found = (u, w); break
            print(f"  M={M:4d} j={j:3d}: "
                  f"{'counterexample '+str(found) if found else 'none found'}")
        print()

    # (c) margin trajectory
    print("[MARGIN] halt(all-ones) needs #zero-bits(m)=0. Trajectory of the margin:")
    m = 2
    minz = 10**9
    for i in range(4000):
        w = m.bit_length(); z = w - bin(m).count('1')
        if z < minz: minz = z; mzat = (i, w)
        if i < 12 or i % 500 == 0:
            print(f"  gen {i:4d}: width {w:5d}  #zero-bits {z:5d}  "
                  f"popcount(m+1) {bin(m+1).count('1'):4d}")
        m = f(m)
    print(f"  min #zero-bits over 4000 gens = {minz} at gen {mzat[0]} (width {mzat[1]});"
          f" margin stays >= {minz} (halt needs 0) -- OBSERVED, not an invariant.")
    print("\nNo machine decided. No label upgraded.")
