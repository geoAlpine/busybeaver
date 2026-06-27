"""
Adelic / product-formula coupling test for the induced odd map
    o' = 3^{D-1}(3o-1)/2^D,  D = v2(3o-1),  o0 = 27 (Antihydra induced Syracuse).

Tests:
 (1) product formula identity  (3o-1) = 2^D * prod_{p odd} p^{v_p}   (sanity)
 (2) the v3-coupling  v3(o_{j+1}) = D_j - 1   exactly  [candidate PROVEN]
 (3) first-moment / log identity  log o_n ~ log o_0 + (sum D_j) log(3/2)
 (4) odd-prime structure of (3o-1): distributions and correlation with D
exact big-int, .venv only.
"""
import math
from collections import Counter

def v2(x):
    d = 0
    while x % 2 == 0:
        x //= 2; d += 1
    return d

def vp(x, p):
    d = 0
    while x % p == 0:
        x //= p; d += 1
    return d

def induced(o):
    N = 3*o - 1
    D = v2(N)
    m = N >> D            # odd part w.r.t. 2
    return (3**(D-1)) * m, D, N, m

o = 27
N_STEPS = 200_000

Ds = []
# coupling checks
v3_coupling_ok = True
prodform_ok = True
v3_of_N_nonzero = 0
# correlation data
pairs_D_v5 = []
pairs_D_v3next = []
v5_counts = Counter()
v7_counts = Counter()
D_counts = Counter()
m_div3 = 0

logsum_D = 0.0
log_o0 = math.log(o)

prev_o = o
for j in range(N_STEPS):
    o_next, D, N, m = induced(prev_o)
    Ds.append(D)
    D_counts[D] += 1
    logsum_D += D

    # (1) product formula sanity: reconstruct N from valuations
    # N = 2^D * m ; m odd. factor m's small primes for reporting only.
    if (1 << D) * m != N:
        prodform_ok = False
    # full product-formula identity over all primes is just N = prod p^{vp}; trivially the factorization.

    # check 3 | (3o-1)?  should never
    if N % 3 == 0:
        v3_of_N_nonzero += 1
    if m % 3 == 0:
        m_div3 += 1

    # (2) v3 of next term
    v3n = vp(o_next, 3)
    pairs_D_v3next.append((D, v3n))
    if v3n != D - 1:
        v3_coupling_ok = False

    # (4) odd-prime structure of N=3o-1
    v5 = vp(N, 5)
    v7 = vp(N, 7)
    v5_counts[v5] += 1
    v7_counts[v7] += 1
    pairs_D_v5.append((D, v5))

    prev_o = o_next

n_time = sum(Ds)   # renewal: total micro-time = sum of gaps = sum D
# size at end (log)
log_o_end = math.log(prev_o) if prev_o > 0 else None
# but prev_o is astronomically large; use logs incrementally instead:
# log o_{j+1} = log(3^{D-1} m). We accumulate exactly via Python big int log:
# Python's math.log on huge int works (returns float of log).

print("=== (1) product formula / factorization sanity ===")
print("  N = 2^D * m held every step :", prodform_ok)
print("  #steps with 3 | (3o-1)      :", v3_of_N_nonzero, "(must be 0)")
print("  #steps with 3 | m (odd part):", m_div3, "(must be 0)")

print("\n=== (2) v3 coupling  v3(o_{j+1}) = D_j - 1 ===")
print("  holds every step :", v3_coupling_ok, f"  over {N_STEPS} steps")

print("\n=== (3) first-moment / log identity ===")
# exact: log o_end via math.log of big int
log_end = math.log(prev_o)
pred = log_o0 + n_time * math.log(1.5)
print(f"  sum D_j (=micro time)      : {n_time}")
print(f"  log o_end (exact big-int)  : {log_end:.6f}")
print(f"  log o0 + (sumD) log(3/2)   : {pred:.6f}")
print(f"  ratio log_end/pred         : {log_end/pred:.8f}")
print(f"  mean D over induced orbit  : {n_time/N_STEPS:.6f}  (Haar=2)")
print(f"  freq(D=1)                  : {D_counts[1]/N_STEPS:.6f}  (Haar=1/2)")

print("\n=== (4) odd-prime structure of (3o-1) ===")
# v5 distribution vs Haar geometric P(v5=k)=(1-1/5)5^{-k}
tot = N_STEPS
print("  v5 distribution vs Haar (4/5)*5^-k:")
for k in range(0,5):
    haar = (1-1/5)*5**(-k)
    print(f"    P(v5={k})={v5_counts[k]/tot:.5f}  Haar={haar:.5f}")
print("  v7 distribution vs Haar (6/7)*7^-k:")
for k in range(0,4):
    haar = (1-1/7)*7**(-k)
    print(f"    P(v7={k})={v7_counts[k]/tot:.5f}  Haar={haar:.5f}")

# correlation D vs v5 (Pearson)
def pearson(pairs):
    n=len(pairs); sx=sum(a for a,_ in pairs); sy=sum(b for _,b in pairs)
    sxx=sum(a*a for a,_ in pairs); syy=sum(b*b for _,b in pairs); sxy=sum(a*b for a,b in pairs)
    num=n*sxy-sx*sy; den=math.sqrt((n*sxx-sx*sx)*(n*syy-sy*sy))
    return num/den if den else float('nan')
print(f"\n  corr(D_j, v5(3o_j-1)) = {pearson(pairs_D_v5):.5f}  (expect ~0: independence)")

# lag correlation of D itself
lagpairs=[(Ds[i],Ds[i+1]) for i in range(len(Ds)-1)]
print(f"  corr(D_j, D_{{j+1}})       = {pearson(lagpairs):.5f}  (expect ~0: i.i.d.)")

# D distribution
print("\n  D distribution vs Haar 2^-k:")
for k in range(1,9):
    print(f"    P(D={k})={D_counts[k]/tot:.5f}  Haar={2.0**(-k):.5f}")
