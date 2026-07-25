"""
Route #16: almost-transport probe for the (K) wall.

Map T(G) = (4G + e(G mod 3)) / 3, e = {0:9, 1:14, 2:1}.
Seed G0 = 43. Question: freq_n { G_n ≡ 1 (mod 3) } < 4/5 ?

We study the itinerary ρ_n = G_n mod 3 over the first N steps and look for:
  - the frequency of ρ=1 and its running average / fluctuation,
  - return-time statistics to the cylinder [ρ=1],
  - substitutive / self-similar structure of the itinerary,
  - a candidate inducing (first-return) recoding.

All integer arithmetic is exact (Python big int).
"""
import sys
sys.set_int_max_str_digits(1000000)
from collections import Counter, defaultdict

E = {0: 9, 1: 14, 2: 1}

def T(G):
    return (4 * G + E[G % 3]) // 3

def orbit_residues(G0, N):
    G = G0
    res = []
    for _ in range(N):
        res.append(G % 3)
        G = T(G)
    return res, G

def freq_ones(res):
    c = Counter(res)
    n = len(res)
    return {r: c[r] / n for r in (0, 1, 2)}, c

if __name__ == "__main__":
    N = int(sys.argv[1]) if len(sys.argv) > 1 else 10000
    G0 = 43
    res, Gfin = orbit_residues(G0, N)

    print(f"=== seed {G0}, N={N} steps ===")
    print(f"final G has {len(str(Gfin))} decimal digits")
    f, c = freq_ones(res)
    print(f"counts: {dict(c)}")
    print(f"freq rho=0: {f[0]:.5f}")
    print(f"freq rho=1: {f[1]:.5f}   (threshold 4/5 = 0.8)")
    print(f"freq rho=2: {f[2]:.5f}")

    # running frequency of rho=1 at checkpoints
    print("\n-- running freq(rho=1) --")
    run = 0
    checkpoints = [10, 30, 100, 300, 1000, 3000, 10000, 30000, 100000]
    for n in range(1, N + 1):
        if res[n - 1] == 1:
            run += 1
        if n in checkpoints:
            print(f"  n={n:7d}: freq={run/n:.5f}")

    # first-return / return-time statistics to cylinder [rho=1]
    print("\n-- return times to [rho=1] --")
    positions = [i for i, r in enumerate(res) if r == 1]
    gaps = [positions[i+1] - positions[i] for i in range(len(positions) - 1)]
    gc = Counter(gaps)
    print(f"  #visits to [rho=1]: {len(positions)}")
    print(f"  return-time distribution (gap: count), top 12:")
    for g, cnt in sorted(gc.items())[:12]:
        print(f"    gap {g:3d}: {cnt}")
    if gaps:
        print(f"  mean return time: {sum(gaps)/len(gaps):.4f}  (=1/freq if ergodic: {len(res)/len(positions):.4f})")

    # block frequencies of length-L words in the residue itinerary
    for L in (1, 2, 3, 4):
        wc = Counter(tuple(res[i:i+L]) for i in range(len(res) - L + 1))
        print(f"\n-- length-{L} block counts (top 8) --")
        for w, cnt in wc.most_common(8):
            print(f"    {''.join(map(str,w))}: {cnt}  ({cnt/(len(res)-L+1):.4f})")
