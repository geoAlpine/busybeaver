"""BUILD brick (2): renormalization fixed point. We seek a VARIABLE + renormalization map R whose linearization
at the equidistributed (bias=0) fixed point CONTRACTS -- proving equidistribution. The bit-level-shift
variable does NOT contract (coupling_brick: sensitive dependence). Here we test the RENEWAL/REGENERATION
variable: use the even steps (c_n even) as renewal points (the cross_cryptid renewal dissection: density->1/2,
geometric gaps). Each renewal block = (odd-run + the even step). The renewal renormalization R coarse-grains
to the block level. If (i) inter-renewal blocks DECORRELATE (renewal property) and (ii) the running block-bias
CONTRACTS to 1/2 at the CLT rate, then the renewal variable is the contracting one -- and the buildable target
becomes 'prove the renewal/mixing property for THIS specified orbit'.
0 false proofs: report measured block autocorrelation + bias decay with nulls; claim 'contracting variable'
only if blocks decorrelate AND bias decays at >= CLT rate.
"""
import math

def v2(x):
    r = 0
    while x and x & 1 == 0: x >>= 1; r += 1
    return r

N = 1_000_000
c = 8
par = bytearray(N); v2c = []
renew = []           # renewal points: even steps
for n in range(N):
    e = (c & 1) == 0
    par[n] = 0 if e else 1
    if e: renew.append(n)
    c = (3 * c) // 2

# inter-renewal gaps (odd-run lengths + 1)
gaps = [renew[i+1] - renew[i] for i in range(len(renew) - 1)]
import statistics
print(f"renewal points (even steps): {len(renew)}  (density {len(renew)/N:.4f}, expect ~0.5)")
print(f"inter-renewal gap: mean={statistics.mean(gaps):.3f} (expect ~2), max={max(gaps)}")
# gap distribution: geometric? P(gap=g) ~ 2^-g
from collections import Counter
gc = Counter(gaps); tot = len(gaps)
print(f"  gap histogram (g: frac, geometric 2^-g for ref):")
for g in range(1, 8):
    print(f"    g={g}: {gc.get(g,0)/tot:.4f}   (2^-{g}={2.0**-g:.4f})")

# (i) RENEWAL property: do the odd-run lengths (block contents) decorrelate?
def autocorr(x, h):
    m = len(x) - h; mu = sum(x)/len(x)
    num = sum((x[i]-mu)*(x[i+h]-mu) for i in range(m))/m
    var = sum((xi-mu)**2 for xi in x)/len(x)
    return num/var if var > 0 else 0.0
nullstd = 1/math.sqrt(len(gaps))
print(f"\n(i) renewal decorrelation -- autocorr of the gap sequence (null std ~{nullstd:.4f}):")
for h in (1, 2, 3, 5, 10):
    print(f"    lag-{h} autocorr(gaps) = {autocorr(gaps, h):+.4f}")

# (ii) block-bias contraction: running even-density vs N at the CLT rate
print(f"\n(ii) block-bias contraction -- running even-density deviation |E_n/n - 1/2| vs CLT 1/sqrt(n):")
print(f"     {'n':>9} {'|dev|':>9} {'|dev|*sqrt(n)':>13}")
E = 0
for n in range(1, N+1):
    if par[n-1] == 0: E += 1
    if n in (1000, 10000, 100000, 500000, N):
        dev = abs(E/n - 0.5)
        print(f"     {n:>9} {dev:>9.5f} {dev*math.sqrt(n):>13.3f}")

# (iii) does a SHUFFLE of the gap sequence give the same even-density? (renewal => yes, block-exchangeable)
# Build a deterministically reordered gap sequence (reverse) and reconstruct the parity; even-density invariant?
print(f"\n(iii) block-exchangeability check: even-density under gap-reversal (renewal => invariant ~0.5):")
# reversed gaps -> same multiset -> same #evens by construction; the informative test is block autocorr above.
print(f"     (even-density is gap-multiset-determined; the renewal test is the gap autocorrelation in (i).)")

print(f"""
READING (renewal renormalization as the contracting variable):
  - gaps ~ geometric (mean ~2, P(g)~2^-g): the renewal structure is clean (the cross_cryptid dissection).
  - (i) if gap autocorrelations are ~null at all lags, the renewal blocks DECORRELATE => the renewal
    variable behaves as an i.i.d. renewal process = a CONTRACTING renormalization (block-bias averages out).
  - (ii) if |E_n/n - 1/2| decays at the CLT rate (|dev|*sqrt(n) bounded), the block-bias CONTRACTS to 1/2.
  => If both hold, the renewal/regeneration variable IS the contracting renormalization variable (unlike the
     bit-level-shift). The buildable new theorem then sharpens to: 'prove the renewal blocks of THIS specified
     orbit are sufficiently mixing (gap-decorrelated)' -- a renewal/Gibbs-Markov mixing statement for one
     orbit. That is a more concrete construction target than raw equidistribution, though still the closed
     loop (the gaps are self-generated). Measured decorrelation != proven; but it identifies the right variable.""")
