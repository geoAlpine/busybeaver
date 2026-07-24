#!/usr/bin/env python3
"""
Route #21: cross-orbit ALGEBRAIC identities for the (K) wall.

Object: T(G) = (4G + e(G mod 3))/3,  e = {0:9, 1:14, 2:1}.
On branch rho, T is affine G -> (4G + e(rho))/3, slope 4/3 on EVERY branch,
branch fixed point x_rho = -e(rho).  Orbit of seed 43; phi = freq{rho_n == 1}.

We test:
 (1) prefix-sharing seeds / affine relations to frequency-forced seeds,
 (2) affine automorphisms  L(G)=a G + b  with  L T = T L  or  L T = T^j L,
 (3) exact conserved quantities / cocycles / linearizing coordinate,
 (4) verdict.

Exact big-int arithmetic throughout (integer orbits stay integer).
"""

from fractions import Fraction as F

e = {0: 9, 1: 14, 2: 1}

def T(G):
    r = G % 3
    return (4 * G + e[r]) // 3

def check_integer_closed():
    # 3 | 4G + e(G mod3) always?
    for r in range(3):
        assert (r + e[r]) % 3 == 0, r   # 4G+e ≡ G+e ≡ r+e[r] mod 3
    print("[check] 4G+e(rho) always divisible by 3  -> integer orbits stay integer.  OK")

def orbit(seed, N):
    G = seed
    res = []
    for _ in range(N):
        r = G % 3
        res.append(r)
        G = (4 * G + e[r]) // 3
    return res

def freq(seed, N):
    res = orbit(seed, N)
    c = res.count(1)
    return c / N, res

# ---------------------------------------------------------------- (0) baseline
print("="*70)
check_integer_closed()
print("="*70)
print("(0) BASELINE FREQUENCY phi(43) = freq{rho_n == 1}")
for N in [10**3, 10**4, 10**5, 2*10**5]:
    f1, _ = freq(43, N)
    print(f"    N={N:>8}   phi≈{f1:.6f}")

# residue-0 and residue-2 frequencies too, and drift
res = orbit(43, 2*10**5)
n = len(res)
print(f"    residue counts over N=2*10^5:  0:{res.count(0)}  1:{res.count(1)}  2:{res.count(2)}")

# frequency-forced special seeds (branch fixed points & their frequency)
print("\n    frequency-forced seeds (branch fixed points x_rho = -e(rho)):")
for r in range(3):
    x = -e[r]
    f1, rr = freq(x, 50)
    print(f"      seed {x:>4} (=x_{r}):  first residues {rr[:8]}...  phi={f1}")

# ---------------------------------------------------------------- (1) prefixes
print("="*70)
print("(1) PREFIX-SHARING SEEDS.  Seeds sharing first k residues with 43")
print("    should be exactly the congruence class 43 + 3^k * Z.")
pref43 = orbit(43, 12)
for k in range(1, 9):
    mod = 3**k
    # test a batch of seeds, see which share first k residues
    good = []
    for s in range(43 - 4*mod, 43 + 4*mod + 1):
        if orbit(s, k) == pref43[:k]:
            good.append(s % mod)
    good = sorted(set(good))
    ok = (good == [43 % mod])
    print(f"    k={k}: seeds sharing prefix all ≡ {43%mod} (mod 3^{k}={mod}) : {ok}  residues distinct? {good}")

# Do prefix-sharing seeds share the TAIL frequency? (they must NOT, generically)
print("\n    tail frequency of several seeds ≡ 43 mod 3^k (share k-prefix, then diverge):")
for k in [1, 3, 5]:
    mod = 3**k
    seeds = [43 + j*mod for j in range(6)]
    fs = [round(freq(s, 60000)[0], 5) for s in seeds]
    print(f"      k={k}: seeds {seeds} -> phi {fs}")

# ---------------------------------------------------------------- (2) automorph
print("="*70)
print("(2) AFFINE AUTOMORPHISMS  L(G)=aG+b  with  L∘T = T∘L.")
print("    Commutation on branches forces:  e(sigma(rho)) = a*e(rho) - b")
print("    for all rho, where sigma(rho)=a*rho+b mod 3 is an affine perm.")
print("    Solve a,b (2 unknowns) from 3 equations; must be consistent")
print("    AND a a 3-adic unit (|a|_3 = 1).")

def threeadic_unit(fr):
    # Fraction is a 3-adic unit iff num and den both coprime to 3
    return fr != 0 and fr.numerator % 3 != 0 and fr.denominator % 3 != 0

# all affine permutations of Z/3: sigma(rho) = A*rho + B mod3, A in {1,2}
found_any = False
for A in (1, 2):
    for B in (0, 1, 2):
        sigma = {rho: (A*rho + B) % 3 for rho in range(3)}
        # solve a from pair (0,1): e(s0)-e(s1) = a(e0-e1)
        a01 = F(e[sigma[0]] - e[sigma[1]], e[0] - e[1])
        a12 = F(e[sigma[1]] - e[sigma[2]], e[1] - e[2])
        a02 = F(e[sigma[0]] - e[sigma[2]], e[0] - e[2])
        consistent = (a01 == a12 == a02)
        tag = "identity" if (A==1 and B==0) else f"sigma={sigma}"
        if consistent:
            a = a01
            b = a*e[0] - e[sigma[0]]
            # verify all three eqns e(sigma(rho)) = a e(rho) - b
            ok = all(e[sigma[rho]] == a*e[rho] - b for rho in range(3))
            unit = threeadic_unit(a)
            # residue compatibility: a ≡ A, b ≡ B (mod 3)?  (a,b may be fractions)
            print(f"    {tag}: CONSISTENT a={a}, b={b}, verify={ok}, a 3-adic unit={unit}")
            if (A,B) != (1,0) and unit and ok:
                found_any = True
        else:
            print(f"    {tag}: inconsistent  (a from pairs: {a01}, {a12}, {a02}) -> NO commuting L")
print(f"\n    Nontrivial affine automorphism with 3-adic-unit multiplier exists? {found_any}")

# L∘T = T^j∘L : derivative/slope argument.  Every branch slope = 4/3, so
# (T^j)' = (4/3)^j everywhere.  L∘T=T^j∘L  =>  a*(4/3) = (4/3)^j * a  => j=1.
print("\n    L∘T = T^j∘L forces (4/3)=(4/3)^j (all branch slopes =4/3) => j=1.")
print("    So the ONLY candidate is j=1, handled above.")

# ---------------------------------------------------------------- (3) invariants
print("="*70)
print("(3) EXACT CONSERVED QUANTITIES / COCYCLES / LINEARIZING COORDINATE.")
print("    (a) polynomial invariant P(T(G))=P(G): leading term (4/3)^d = 1 => d=0.")
print("        => no non-constant polynomial invariant. [PROVEN]")
print("    (b) Koenigs/linearizing coordinate A(G)=lim (3/4)^n G_n.")
# G_n = (4/3)^n * S - tail ; S = A(seed).  Compute A(43) numerically (Archimedean).
def koenigs(seed, N):
    G = seed
    val = F(seed)          # (3/4)^0 G_0
    p = F(1)
    for i in range(N):
        r = G % 3
        G = (4*G + e[r])//3
        p *= F(3,4)
        val = p * G         # (3/4)^{i+1} G_{i+1}
    return val
A_prev = None
print("        A(43) = lim (3/4)^n G_n  (should converge, Archimedean):")
for N in [20, 40, 80, 160, 320]:
    a = koenigs(43, N)
    af = float(a)
    print(f"          n={N:>4}: A≈{af:.12f}")
# eigen relation A∘T = (4/3) A  : check A(T(43)) / A(43) == 4/3
A43 = float(koenigs(43, 400))
AT43 = float(koenigs(T(43), 400))
print(f"        A(T(43))/A(43) = {AT43/A43:.12f}   (should be 4/3 = {4/3:.12f})")
print("        => A is an EIGENFUNCTION (conjugacy to linear model), not a")
print("           frequency-pinning invariant: it is the single map in disguise.")

# ---------------------------------------------------------------- (4) empirical multifractal
print("="*70)
print("(4) MULTIFRACTAL CHECK: is every frequency realized? sample many seeds.")
import random
random.seed(1)
phis = []
for _ in range(3000):
    s = random.randint(2, 10**6)
    phis.append(freq(s, 2500)[0])
phis.sort()
import statistics as st
print(f"    over 3000 random seeds (N=2500): min phi={phis[0]:.4f}  max phi={phis[-1]:.4f}")
print(f"      mean={st.mean(phis):.4f}  median={st.median(phis):.4f}")
print(f"      quantiles 1%,10%,50%,90%,99%: "
      + ", ".join(f"{phis[int(q*len(phis))]:.3f}" for q in (0.01,0.1,0.5,0.9,0.99)))
# push a seed toward high phi: seeds near -14 congruence give long rho=1 runs
print("    seeds near x_1=-14 (rho≡1 fixed pt): long rho=1 prefixes, phi high early:")
for s in [-14, -14+3**6, -14+3**10, -14+3**14]:
    f1,_ = freq(s, 60)
    print(f"      seed {s}: phi(first 60) = {f1}")
print("="*70)
print("DONE.")
