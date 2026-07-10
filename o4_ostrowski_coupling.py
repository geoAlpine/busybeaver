"""
o4 Ostrowski coupling test.

The archimedean rotation {n*beta}, beta = log_3(4/3), governs the LEADING
base-3 digits (mantissa) of W_n ~ alpha*(4/3)^n.  We test whether it couples
to the NON-archimedean quantity freq{3 | W_n} = freq{rho_n = 1}, the trailing
3-adic residue.

Exact big-int orbit; the mantissa uses exact integer digit-length + top digits.
"""
import mpmath as mp
from fractions import Fraction
from math import gcd

mp.mp.dps = 60
log3 = mp.log(3)
beta = mp.log(mp.mpf(4)/3)/log3

# ---- exact orbit -----------------------------------------------------------
# odometer 3G' = 4G + e(rho), rho = G mod 3, e={0:9,1:14,2:1}, seed 43
E = {0:9, 1:14, 2:1}
def orbit(N, G0=43):
    G = G0
    Gs = []
    for _ in range(N):
        Gs.append(G)
        rho = G % 3
        G = (4*G + E[rho])//3
        assert (4*Gs[-1] + E[rho]) % 3 == 0
    return Gs

N = 200000
Gs = orbit(N)
Ws = [G+14 for G in Gs]
rhos = [G % 3 for G in Gs]

# freq check
c1 = sum(1 for r in rhos if r==1)
print("N =", N)
print("freq{rho=1} = freq{3|W_n} =", c1/N)
assert all((r==1) == (w%3==0) for r,w in zip(rhos,Ws))
print("verified rho=1 <=> 3|W_n on all", N, "steps")

# ---- archimedean mantissa: exact fractional part of log_3(W_n) -------------
# log_3(W_n) = (number of base-3 digits related) ; use mpmath on exact leading
# We compute frac(log_3 W_n) exactly enough: W_n is exact int -> log via mpmath
# with enough guard digits (W_n has up to ~ n*log_10(4/3) digits; for n<=2e5
# that's ~2.5e4 digits -> need dps > that only for the *integer part*; the
# fractional part needs W_n/3^floor and precision ~ 40 digits).
def frac_log3(w):
    # frac(log_3 w) = log_3(w / 3^k) for k = floor(log_3 w)
    # get k exactly via bit length approximation then correct
    L = w.bit_length()
    k = int(L*mp.log(2)/log3)  # approx
    # correct k so that 3^k <= w < 3^{k+1}
    while 3**k > w: k -= 1
    while 3**(k+1) <= w: k += 1
    m = mp.mpf(w) / mp.mpf(3**k)      # in [1,3)
    return float(mp.log(m)/log3)      # in [0,1)

# sample (every step is expensive for huge ints; sample a grid + a dense prefix)
import random
# dense prefix for correlation of consecutive; grid for global
sample_idx = list(range(0, 20000)) + list(range(20000, N, 7))
mant = {}
for i in sample_idx:
    mant[i] = frac_log3(Ws[i])

# confirm mantissa ~ {n beta + c0}
c0 = mant[100] - float((100*beta) - mp.floor(100*beta))
def rot(n):
    v = n*beta + (mant[0])/1  # anchor
    return float((mp.mpf(mant[0]) + n*beta) % 1)
# direct check: mant[i] vs {mant[0] + i*beta}
err = []
for i in sample_idx[:5000]:
    pred = float((mp.mpf(mant[0]) + i*beta) % 1)
    d = abs(pred - mant[i])
    d = min(d, 1-d)
    err.append(d)
print("\nmantissa vs {n*beta} anchor: max wrap-dist over first 5000 samples =", max(err))
print("  (confirms frac(log_3 W_n) = {frac(log_3 W_0) + n*beta} up to o(1) drift)")

# ---- THE COUPLING TEST -----------------------------------------------------
# If the archimedean rotation controlled the 3-adic residue, then
# freq{rho=1 | {n beta} in subinterval J} would DEPEND on J.
# Orthogonality  <=>  freq{rho=1 | J} = 1/3 for every J.
print("\n=== COUPLING TEST: freq{rho=1} conditioned on mantissa subinterval ===")
B = 10
buckets_all = [0]*B
buckets_1   = [0]*B
for i in sample_idx:
    j = min(B-1, int(mant[i]*B))
    buckets_all[j]+=1
    if rhos[i]==1: buckets_1[j]+=1
print("bucket   [lo,hi)       count   freq{rho=1}")
for j in range(B):
    if buckets_all[j]:
        print("  %d  [%.2f,%.2f)   %7d   %.4f" %
              (j, j/B, (j+1)/B, buckets_all[j], buckets_1[j]/buckets_all[j]))
import statistics
freqs = [buckets_1[j]/buckets_all[j] for j in range(B) if buckets_all[j]]
print("mean over buckets = %.4f   stdev = %.4f  (independent-of-mantissa if flat ~1/3)"
      % (statistics.mean(freqs), statistics.pstdev(freqs)))

# chi-square test of independence between mantissa-bucket and (rho==1)
tot = sum(buckets_all); tot1 = sum(buckets_1)
p1 = tot1/tot
chi2 = 0.0
for j in range(B):
    if buckets_all[j]:
        exp1 = buckets_all[j]*p1
        exp0 = buckets_all[j]*(1-p1)
        obs1 = buckets_1[j]; obs0 = buckets_all[j]-obs1
        chi2 += (obs1-exp1)**2/exp1 + (obs0-exp0)**2/exp0
print("chi-square (df=%d) = %.2f  (critical 0.05 ~ %.1f); large => coupling, small => orthogonal"
      % (B-1, chi2, 16.9))

# also: correlation between the *value* of the rotation and 1{rho=1}
import math
xs = [mant[i] for i in sample_idx]
ys = [1.0 if rhos[i]==1 else 0.0 for i in sample_idx]
mx = statistics.mean(xs); my = statistics.mean(ys)
cov = sum((x-mx)*(y-my) for x,y in zip(xs,ys))/len(xs)
sx = statistics.pstdev(xs); sy = statistics.pstdev(ys)
print("Pearson corr( {n beta}, 1{3|W} ) = %.5f  (0 => orthogonal)" % (cov/(sx*sy)))
