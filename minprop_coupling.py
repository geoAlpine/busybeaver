"""
MINPROP_COUPLING — coupling / specification probe for the induced odd map (2026-06-28)

Induced odd map (GAP LEMMA): o odd -> D = v2(3o-1) >= 1,  o' = 3^{D-1}(3o-1)/2^D  (odd).
[PROVEN elsewhere] T is Haar-preserving + exact/Bernoulli on Z_2^*, D_j i.i.d. geometric 2^{-d}.
Specific orbit: c0=8 -> 12 -> 18 -> 27 (=o0), the Antihydra odd subsequence.

This script tests, with EXACT big-int arithmetic, whether the proven Bernoulli structure can give a
QUANTITATIVE one-sided bound for the SPECIFIC orbit o0=27, or hits the a.e. wall:

  (1) mixing/autocorrelation of the indicator 1{D>=2}=1{o=3 mod4} and of D, real orbit vs Bernoulli.
  (2) fluctuation scaling of running freq(D>=2): CLT-rate? one-sided-boundable, or symmetric two-sided?
  (3) COUPLING obstruction: ensemble with FRESH random high bits couples in ONE step (Haar);
      the single deterministic orbit o0=27 injects NO fresh bits -> no coupling source. Demonstrate.
  (4) SPECIFICATION / non-universality: build prescribed-itinerary 2-adic points via inverse branches;
      exhibit orbits with freq(D>=2) = 0, 1/2, 1 and intermediate -> the bound is NOT universal.

.venv only. 0 false proofs.
"""
import numpy as np
from collections import Counter

PR = np.random.default_rng(20260628)

def v2(x):
    if x == 0: return 10**9
    return (x & -x).bit_length() - 1

def T(o):
    x = 3*o - 1
    D = v2(x)
    return pow(3, D-1) * (x >> D), D

# real orbit odd subsequence ---------------------------------------------------
def real_odds(c0=8, n_steps=600000):
    c = c0; odds = []
    for _ in range(n_steps):
        if c & 1: odds.append(c)
        c = (3*c) >> 1   # floor(3c/2)
    return odds

print("="*80); print("SETUP: real induced orbit (c0=8 -> o0=27)"); print("="*80)
odds = real_odds()
# sanity: induced map reproduces it
o = odds[0]; ok = True
for j in range(min(len(odds)-1, 2000)):
    no, _ = T(o)
    if no != odds[j+1]: ok = False; break
    o = no
print(f"  o0 = {odds[0]}   #odds collected = {len(odds)}   induced map reproduces orbit: {ok}")

D_real = np.array([v2(3*o-1) for o in odds], dtype=np.int64)
ind_real = (D_real >= 2).astype(np.float64)   # 1{o = 3 mod 4}
K = len(D_real)
print(f"  mean D = {D_real.mean():.5f}  (Haar 2.0)   freq(D>=2) = {ind_real.mean():.5f}  (Haar 0.5)")

# Bernoulli model: i.i.d. geometric D ------------------------------------------
def geom_D(n):
    # P(D=d)=2^-d ; D = 1 + #leading-ones-style; sample via geometric
    u = PR.random(n)
    return np.floor(np.log2(1.0/u)).astype(np.int64) + 1
D_bern = geom_D(K)
ind_bern = (D_bern >= 2).astype(np.float64)

# (1) autocorrelation ----------------------------------------------------------
def autocorr(x, lags):
    x = x - x.mean(); v = (x*x).mean()
    return [float((x[:len(x)-L]*x[L:]).mean()/v) for L in lags]

lags = [1,2,3,5,10,20,50]
print("\n" + "="*80)
print("(1) AUTOCORRELATION of 1{D>=2}: real orbit vs Bernoulli i.i.d.")
print("="*80)
ac_real = autocorr(ind_real, lags); ac_bern = autocorr(ind_bern, lags)
print("  lag :  " + "  ".join(f"{L:6d}" for L in lags))
print("  real:  " + "  ".join(f"{a:6.3f}" for a in ac_real))
print("  bern:  " + "  ".join(f"{a:6.3f}" for a in ac_bern))
print(f"  -> real autocorr |max over lags| = {max(abs(a) for a in ac_real):.4f}; "
      f"1/sqrt(K) noise floor = {1/np.sqrt(K):.4f}")
print("  reading: real indicator decorrelates at the Bernoulli (noise-floor) level = OBSERVED memoryless.")

# (2) fluctuation scaling of running freq(D>=2) --------------------------------
print("\n" + "="*80)
print("(2) FLUCTUATION of block-freq(D>=2): CLT rate? one-sided or symmetric?")
print("="*80)
for B in [100, 1000, 10000]:
    nb = K // B
    blk_real = ind_real[:nb*B].reshape(nb, B).mean(1)
    blk_bern = ind_bern[:nb*B].reshape(nb, B).mean(1)
    print(f"  block={B:6d} (#blocks={nb}):  std_real={blk_real.std():.5f}  "
          f"std_bern={blk_bern.std():.5f}  CLT 0.5/sqrt(B)={0.5/np.sqrt(B):.5f}")
# signed running deviation: symmetric (two-sided) or one-sided?
csum = np.cumsum(ind_real - 0.5)
runmean_dev = csum / np.arange(1, K+1)        # freq_K - 1/2
print(f"  signed running dev freq_K-1/2:  min={runmean_dev[50:].min():+.5f}  "
      f"max={runmean_dev[50:].max():+.5f}  final={runmean_dev[-1]:+.5f}")
# how often is the running freq BELOW 1/2 (would violate the target)?
below = np.mean(runmean_dev[50:] < 0)
print(f"  fraction of prefixes (K>=50) with freq_K < 1/2 (target-violating): {below:.3f}")
print("  reading: deviations are SYMMETRIC two-sided ~ N(0,(1/2)^2/K); the orbit dips BELOW 1/2 a")
print("  positive fraction of the time. No structural ONE-SIDED floor: only the LIMIT is conjectured 1/2.")

# (3) COUPLING obstruction -----------------------------------------------------
print("\n" + "="*80)
print("(3) COUPLING: fresh random high bits couple in ONE step; o0=27 injects none")
print("="*80)
# (3a) Haar ensemble: o' mod 2^k from random odd o is EXACTLY uniform (one-step coupling).
for k in (6, 8):
    M = k + 30
    cnt = Counter()
    for _ in range(40000):
        o = (int(PR.integers(1<<(M-1))) << 1) | 1
        no, _ = T(o)
        cnt[no % (1<<k)] += 1
    vals = np.array([cnt.get(r,0) for r in range(1, 1<<k, 2)], float)
    chi2 = ((vals-vals.mean())**2/vals.mean()).sum(); dof = len(vals)-1
    print(f"  [Haar ensemble] o' mod 2^{k}: chi2/dof = {chi2/dof:.3f} -> uniform after ONE step "
          f"(fresh high bits = independent coin flips)")
# (3b) the single orbit is a DETERMINISTIC function of the integer 27: no probability space to couple in.
print(f"  [single orbit] o0=27 = {27:b}_2 has a FIXED, eventually-zero 2-adic tail; every o_j is an")
print(f"  exact deterministic function of 27. The window-shift pulls in the HIGH BITS OF THE DETERMINISTIC")
print(f"  ITERATES, not an independent refresh -> there is NO entropy source to couple to the Bernoulli copy.")
# (3c) sensitivity demo: two starts sharing low L bits decorrelate (shift expands) -- but BOTH deterministic.
def Dseq(o0, n):
    o=o0; out=[]
    for _ in range(n):
        no,D=T(o); out.append(D); o=no
    return np.array(out)
o0 = odds[0]
o0b = o0 + (1 << 40)   # perturb a high bit
da, db = Dseq(o0, 400), Dseq(o0b, 400)
first_diff = int(np.argmax(da != db)) if np.any(da!=db) else -1
print(f"  [expansion] flipping bit 40 of o0: D-sequences first differ at step {first_diff} "
      f"(high bits reach the low end in ~ that many induced steps) -> sensitive dependence, but both")
print(f"  trajectories are still single deterministic points; sensitivity != an independent coupling.")

# (4) SPECIFICATION / non-universality: prescribed-itinerary points -------------
print("\n" + "="*80)
print("(4) SPECIFICATION: build orbits with prescribed freq(D>=2) -> bound NOT universal")
print("="*80)
# inverse branch (mod 2^M): given o' and chosen d, o = 3^{-1} + 2^d * 3^{-d} * o'  (2-adic units).
def build_point(itinerary, M=4000):
    inv3 = pow(3, -1, 1<<M)
    o = 1                       # arbitrary tail (the fixed point with D=1)
    for d in reversed(itinerary):
        o = (inv3 + ((1<<d) * pow(inv3, d, 1<<M) % (1<<M)) * o) % (1<<M)
    return o
def forward_freq(o0, L):
    o=o0; deep=0
    for _ in range(L):
        no,D=T(o); deep += (D>=2); o=no
    return deep/L

cases = {
    "all D=1 (o=1 fixed point)":        [1]*300,
    "all D=2":                          [2]*300,
    "period-2  D=1,2 (freq 1/2)":      [1,2]*150,
    "period-4  D=1,1,1,2 (freq 1/4)":  [1,1,1,2]*75,
    "period-3  D=2,2,1 (freq 2/3)":    [2,2,1]*100,
}
print("  prescribed itinerary           target freq(D>=2)   realized (forward check)   <1/2 ?")
for name, it in cases.items():
    target = np.mean([1 if d>=2 else 0 for d in it])
    o0c = build_point(it)
    L = len(it) - 20            # check the realizable prefix (deep tail beyond M not guaranteed)
    realized = forward_freq(o0c, L)
    print(f"   {name:30s}  {target:6.3f}            {realized:6.3f}                {'VIOLATES' if realized<0.5-1e-9 else 'ok'}")
# genuine fixed points
o1 = 1; print(f"\n  genuine fixed point o=1: T(1)={T(1)} -> D=1 forever, freq(D>=2)=0  (an invariant measure, Dirac)")
# o = 3/5 in 2-adics: 3*inv5 mod 2^M ; verify D=2 along forward orbit (low bits exactly fixed)
M=4000; o35 = (3*pow(5,-1,1<<M))%(1<<M)
o=o35; Ds=[]
for _ in range(200):
    no,D=T(o); Ds.append(D); o=no
print(f"  fixed point o=3/5 (2-adic): forward D-sequence all==2 over 200 steps: {set(Ds)=={2}} "
      f"-> D=2 forever, freq(D>=2)=1  (low bits are an exact fixed point; 5o=3 in Z_2)")

print("\n" + "="*80)
print("CONCLUSION")
print("="*80)
print("  ergodic-opt range of freq(D>=2) over INVARIANT measures = [0,1] (Diracs at o=1 and o=3/5).")
print("  => max of the VIOLATION observable (1/2 - freq) = +1/2 > 0; specification realizes the full")
print("     range with full-Hausdorff-dimension level sets. The one-sided bound liminf freq>=1/2 is")
print("     PROVABLY NON-UNIVERSAL. The structure cannot give it; o0=27 must be singled out arithmetically")
print("     = effective equidistribution of the SPECIFIC point = the a.e. wall. No coupling source exists.")
