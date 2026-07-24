"""
Route #16 part 2: is the residue itinerary of seed 43 substitutive / low-entropy,
or full-entropy (i.i.d.-looking)?  And how much 3-adic memory drives rho_{n+1}?

Key tests:
  (A) conditional transition rho_n -> rho_{n+1}: is it deterministic/Markov?
  (B) block entropy h_L = H(word_L)/L  vs  log2(3); conditional entropy
      H(rho_{n+1} | last k symbols) -> tells us if a finite recoding could
      make the itinerary predictable (=> substitutive => computable freq).
  (C) does rho_{n+1} become a DETERMINISTIC function of G mod 3^k for some k?
      (that would be an EXACT finite transport / renormalization.)
"""
import sys, math
sys.set_int_max_str_digits(1000000)
from collections import Counter, defaultdict

E = {0: 9, 1: 14, 2: 1}
def T(G): return (4 * G + E[G % 3]) // 3

def build(G0, N):
    G = G0; res = []; mods = defaultdict(list)
    Gs = []
    for _ in range(N):
        Gs.append(G)
        res.append(G % 3)
        G = T(G)
    return res, Gs

def H(counter):
    tot = sum(counter.values())
    return -sum((c/tot)*math.log2(c/tot) for c in counter.values() if c)

if __name__ == "__main__":
    N = int(sys.argv[1]) if len(sys.argv) > 1 else 200000
    res, Gs = build(43, N)
    log2_3 = math.log2(3)
    print(f"log2(3) = {log2_3:.5f} bits (max entropy per symbol)\n")

    # (A) transition matrix rho_n -> rho_{n+1}
    print("-- (A) transition rho_n -> rho_{n+1} (row-normalized) --")
    trans = defaultdict(Counter)
    for i in range(len(res)-1):
        trans[res[i]][res[i+1]] += 1
    for a in (0,1,2):
        row = trans[a]; tot = sum(row.values())
        probs = [row[b]/tot for b in (0,1,2)]
        print(f"   from {a}: " + "  ".join(f"{b}:{p:.4f}" for b,p in zip((0,1,2),probs)))

    # (B) conditional entropy given last k symbols
    print("\n-- (B) block & conditional entropy --")
    for k in range(0, 9):
        # H(next | previous k)
        ctx = defaultdict(Counter)
        for i in range(k, len(res)-1):
            key = tuple(res[i-k:i]) if k>0 else ()
            ctx[key][res[i]] += 1
        tot_all = sum(sum(c.values()) for c in ctx.values())
        Hcond = sum(sum(c.values())/tot_all * H(c) for c in ctx.values())
        print(f"   H(rho_{{n+1}} | prev {k}) = {Hcond:.5f} bits  (gap from log2 3: {log2_3-Hcond:+.5f})")

    # (C) is rho_{n+1} a deterministic function of G mod 3^k?
    print("\n-- (C) does G mod 3^k DETERMINE the next residue rho_{n+1}? --")
    print("   (if yes for some finite k => exact finite renormalization transport)")
    for k in range(1, 14):
        m = 3**k
        f = {}
        deterministic = True
        conflicts = 0
        for i in range(len(Gs)-1):
            key = Gs[i] % m
            nxt = res[i+1]
            if key in f and f[key] != nxt:
                deterministic = False; conflicts += 1
            else:
                f.setdefault(key, nxt)
        print(f"   k={k:2d} (mod 3^{k}={m}): deterministic={deterministic}  conflicts={conflicts}  distinct_keys_seen={len(f)}")
        if deterministic:
            print(f"      *** rho_{{n+1}} is a function of G mod 3^{k} ! ***")
            break

    # (D) also: does G mod 3^k determine rho_{n+1} where we DIVIDE OUT the shift?
    #     i.e. the true dependence is on high digits. Check function of floor(G/3^j) mod 3.
    print("\n-- (D) which base-3 digit of G controls rho_{n+1}? --")
    for j in range(0, 6):
        ctx = defaultdict(Counter)
        for i in range(len(Gs)-1):
            digit = (Gs[i] // (3**j)) % 3
            ctx[digit][res[i+1]] += 1
        tot = sum(sum(c.values()) for c in ctx.values())
        Hc = sum(sum(c.values())/tot*H(c) for c in ctx.values())
        print(f"   H(rho_{{n+1}} | digit_{j} of G) = {Hc:.5f}  (reduction {log2_3-Hc:+.5f})")
