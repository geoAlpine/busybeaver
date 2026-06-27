"""
THREE-ADIC dual of WALLB_MARTINGALE.
Question: does o_j mod 3^k (induced odd orbit from o0=27) have rotation/periodic/
computable structure, exactly as T_n mod 2^k was found to be an exact x3 rotation
(a function of n alone, period 2^{k-5}, 0 violations)?

Induced odd map: o' = 3^{D-1}(3o-1)/2^D,  D = v2(3o-1),  o0 = 27.
Coupling (proven): v3(o_{j+1}) = D_j - 1.

Tests:
 (1) o_j mod 3^k for k=1..6: search for eventual periodicity in j (rotation analog).
 (2) subword (factor) complexity of the mod-3 symbol sequence vs the D-sequence.
 (3) density{3|o_j}, density{9|o_j}; v3 law.
 (4) isomorphism check: v3(o_j) sequence == (D_{j-1}-1) sequence; same complexity.
 (5) residual structure: the 3-adic UNIT digit u_j = (o_j / 3^{v3}) mod 3 in {1,2}:
     periodic? biased? autocorrelated?
exact big-int, .venv only. Every result labelled in the .md.
"""
import math
from collections import Counter

def v2(x):
    d = 0
    while x % 2 == 0:
        x //= 2; d += 1
    return d

def v3(x):
    if x == 0:
        return 10**9
    d = 0
    while x % 3 == 0:
        x //= 3; d += 1
    return d

def induced(o):
    N = 3*o - 1
    D = v2(N)
    m = N >> D
    return (3**(D-1)) * m, D

o0 = 27
N_STEPS = 120_000
MOD = 3**6  # 729

orbit_mod = []   # o_j mod 3^6
v3_seq = []      # v3(o_j)
unit_seq = []    # 3-adic unit digit of o_j: (o_j/3^{v3}) mod 3
Ds = []

o = o0
for j in range(N_STEPS):
    orbit_mod.append(o % MOD)
    vj = v3(o)
    v3_seq.append(vj)
    unit_seq.append((o // (3**vj)) % 3)
    o_next, D = induced(o)
    Ds.append(D)
    o = o_next

# ---------- (1) eventual periodicity of o_j mod 3^k in j ----------
def find_period(seq, kmod, pmax, tail_frac=0.5):
    """Return smallest p<=pmax s.t. seq[i]%kmod == seq[i+p]%kmod for all i in
    the second half (tail), else None."""
    n = len(seq)
    start = int(n*tail_frac)
    s = [x % kmod for x in seq[start:]]
    L = len(s)
    for p in range(1, pmax+1):
        ok = True
        for i in range(L - p):
            if s[i] != s[i+p]:
                ok = False
                break
        if ok:
            return p
    return None

print("=== (1) eventual periodicity of o_j mod 3^k in j (rotation analog) ===")
print("  contrast: T_n mod 2^k IS exactly periodic in n, period 2^{k-5}, 0 violations.")
for k in range(1, 7):
    mk = 3**k
    # if a rotation existed, period would divide 2*3^{k-1} = order of 2 mod 3^k; <= 486 for k=6
    pmax = min(20000, 4*mk)
    p = find_period(orbit_mod, mk, pmax)
    print(f"  k={k} (mod {mk:>4}): smallest tail-period <= {pmax} : "
          f"{p if p is not None else 'NONE (aperiodic)'}")

# ---------- (2) subword complexity of mod-3 sequence vs D-sequence ----------
def subword_complexity(seq, Lmax):
    res = {}
    n = len(seq)
    for Lw in range(1, Lmax+1):
        s = set()
        for i in range(n - Lw + 1):
            s.add(tuple(seq[i:i+Lw]))
        res[Lw] = len(s)
    return res

mod3_seq = [x % 3 for x in orbit_mod]
print("\n=== (2) subword complexity p(L): distinct length-L factors ===")
print("  alphabet sizes: mod-3 seq = 3 symbols {0,1,2}; D-seq clipped to {1,2,3,4,>=5}")
Dclip = [min(d, 5) for d in Ds]
sc_mod3 = subword_complexity(mod3_seq, 9)
sc_D = subword_complexity(Dclip, 9)
print("  L : p_mod3(L)   3^L     p_Dclip(L)   5^L  (saturation = full complexity)")
for Lw in range(1, 10):
    print(f"  {Lw} : {sc_mod3[Lw]:>8}  {3**Lw:>8}   {sc_D[Lw]:>8}   {5**Lw:>8}")

# ---------- (3) densities ----------
n = N_STEPS
d3 = sum(1 for x in orbit_mod if x % 3 == 0)/n
d9 = sum(1 for x in orbit_mod if x % 9 == 0)/n
print("\n=== (3) divisibility densities of the orbit ===")
print(f"  density(3 | o_j) = {d3:.5f}   (target/Haar-via-coupling 1/2)")
print(f"  density(9 | o_j) = {d9:.5f}   (1/4)")
print(f"  d3 + d9          = {d3+d9:.5f}   (minimal proposition target >= 1/2)")
v3law = Counter(min(v,8) for v in v3_seq)
print("  v3(o_j) law vs 2^-(k+1) (forced by v3=D_prev-1):")
for kk in range(0, 7):
    print(f"    P(v3={kk}) = {v3law[kk]/n:.5f}   2^-(k+1) = {2.0**-(kk+1):.5f}")

# ---------- (4) isomorphism v3(o_j) == D_{j-1}-1 ----------
ok = all(v3_seq[j] == Ds[j-1]-1 for j in range(1, n))
print("\n=== (4) isomorphism check ===")
print(f"  v3(o_j) == D_{{j-1}} - 1 for all j>=1 : {ok}")
# complexities equal?
sc_v3 = subword_complexity([min(v,5) for v in v3_seq[1:]], 9)
print("  subword complexity of v3-seq vs D-seq (should match -> isomorphic):")
for Lw in range(1, 10):
    print(f"    L={Lw}: v3-seq {sc_v3[Lw]:>7}   D-seq {sc_D[Lw]:>7}")

# ---------- (5) residual structure in the 3-adic unit digit u_j in {1,2} ----------
print("\n=== (5) residual structure: 3-adic unit digit u_j = (o_j/3^{v3}) mod 3 ===")
ucnt = Counter(unit_seq)
print(f"  P(u=1) = {ucnt[1]/n:.5f}   P(u=2) = {ucnt[2]/n:.5f}   (bias?)")
# periodicity of unit seq
pu = find_period(unit_seq, 3, 20000)
print(f"  smallest tail-period of u_j (<=20000): {pu if pu is not None else 'NONE'}")
# autocorrelation of (u_j-1.5)
um = [u-1.5 for u in unit_seq]
def autocorr(x, lag):
    nn=len(x)-lag
    mx=sum(x)/len(x)
    num=sum((x[i]-mx)*(x[i+lag]-mx) for i in range(nn))
    den=sum((xi-mx)**2 for xi in x)
    return num/den if den else float('nan')
print("  autocorr(u) lag 1..5:", [f"{autocorr(um,l):+.4f}" for l in range(1,6)])
# subword complexity of unit seq
sc_u = subword_complexity(unit_seq, 9)
print("  subword complexity of u-seq vs 2^L (binary alphabet {1,2}):")
for Lw in range(1, 10):
    print(f"    L={Lw}: {sc_u[Lw]:>7}  2^L={2**Lw:>5}")
# is u_j determined by v3 / a function of the 2-adic data? check corr with D
def pearson(a,b):
    nn=len(a); sa=sum(a); sb=sum(b); saa=sum(x*x for x in a); sbb=sum(x*x for x in b); sab=sum(a[i]*b[i] for i in range(nn))
    num=nn*sab-sa*sb; den=math.sqrt((nn*saa-sa*sa)*(nn*sbb-sb*sb))
    return num/den if den else float('nan')
print(f"  corr(u_j, D_j)     = {pearson(unit_seq, Ds):+.4f}")
print(f"  corr(u_j, v3(o_j)) = {pearson(unit_seq, [min(v,8) for v in v3_seq]):+.4f}")
