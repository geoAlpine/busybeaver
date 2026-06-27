"""Spectral-atom test: does the parity have spectral weight at the PROVABLE rotation frequencies m*alpha?
alpha=log2(3/2). A skew product over the alpha-rotation has spectral components at the base frequencies.
If |(1/N) sum_n (r_n-1/2) e(-2pi i n m alpha)| is anomalously large at f=m*alpha (vs generic f), the
rotation is directly in the parity's spectrum => Furstenberg/Anzai rotation tools apply. We compute the
twisted Birkhoff sums at m*alpha and at a null grid of generic frequencies for comparison.
0 false proofs: report the twisted-sum magnitudes vs the null distribution; an 'atom' = clearly above null.
"""
import math, cmath

N = 500000
c = 8; r = bytearray(N)
for n in range(N):
    r[n] = c & 1; c = (3 * c) // 2
mu = sum(r) / N

def twisted(f):
    """| (1/N) sum_n (r_n - mu) e(-2pi i n f) |."""
    s = 0j
    for n in range(N):
        s += (r[n] - mu) * cmath.exp(-2j * math.pi * n * f)
    return abs(s) / N

alpha = math.log2(1.5)
nullf = 1.0 / math.sqrt(N)
print(f"twisted Birkhoff |(1/N)sum (r-mu)e(-2pi i n f)|; null ~ {nullf:.5f} (N={N})")
print(f"\n(A) at rotation frequencies f = m*alpha mod 1  (alpha=log2(3/2)={alpha:.5f}):")
print(f"  {'m':>3} {'f=m*alpha':>10} {'twisted':>10} {'/null':>7}")
maxrot = 0.0
for m in range(1, 13):
    f = (m * alpha) % 1.0
    t = twisted(f); maxrot = max(maxrot, t)
    flag = "  <== atom?" if t > 6 * nullf else ""
    print(f"  {m:>3} {f:>10.5f} {t:>10.5f} {t/nullf:>7.1f}{flag}")

print(f"\n(B) at generic (null) frequencies for comparison:")
import math as _m
gen = [0.1234, 0.3777, 0.6180, 0.4142, 0.2718, 0.9001]
maxgen = 0.0
for f in gen:
    t = twisted(f); maxgen = max(maxgen, t)
    print(f"      f={f:.4f}: twisted={t:.5f} ({t/nullf:.1f} sigma)")

print(f"\n  max twisted at rotation freqs = {maxrot:.5f}   max at generic = {maxgen:.5f}")
print(f"""
READING (positive, expanding):
  - If the rotation-frequency twisted sums STAND OUT above the generic/null level, the parity has spectral
    ATOMS at m*alpha: it IS a skew product over the provable rotation, and Furstenberg/Anzai unique-ergodicity
    (cocycle is/ isn't a coboundary) becomes the route -- the rotation's provable equidistribution lifts to
    the fiber. BUILD: identify the cocycle and apply Furstenberg's criterion.
  - If they are at the SAME level as generic (continuous spectrum, no atoms), the parity is spectrally
    'rich' (positive entropy, consistent with our complexity floor). Then the productive structure is the
    skew product whose FIBER carries the entropy (a Gibbs-Markov extension over the rotation base): the
    provable rotation is the base, and the parity is the fiber of a finite-extension / (T,T^-1)-style tower.
    BUILD next: the relative (fiber-wise) equidistribution over the equidistributed base -- a relatively-
    mixing extension, where partial-rigidity of the base can seed fiber control. Either outcome opens a
    concrete rotation-based avenue; the leading-bit rotation is a proven lever we keep building on.""")
