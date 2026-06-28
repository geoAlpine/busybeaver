#!/usr/bin/env python
"""ANNEALED vs QUENCHED data for the Antihydra even-density (BB6 / Mahler core).

ORBIT (quenched, exact bigint): h_0 = 8, h_{n+1} = floor(3 h_n/2) = h_n + (h_n>>1).
  parity r_n = h_n & 1; EVEN-density E_N = (1/N)#{n<N: h_n even}.
  Non-halting target: counter c = 2*evens - odds >= 0 forever  <=>  liminf E_N >= 1/3.

ANNEALED objects (independent / i.i.d. weights instead of the orbit's own parity):
  (i) exact carry-imbalance product Phi(N) = prod_{j<N} |cos(pi {(3/2)^j/4})|
      = |E[(-1)^{r_n}]| under i.i.d. Bernoulli(1/2) scenery (exp_sum.py / NONPISOT Link B).
      => annealed even-density mean = 1/2 +- Phi(n)/2  (Phi -> 0 by Rajchman/non-Pisot).
  (ii) i.i.d. Monte-Carlo: T_{n+1}=3T_n + 2^n e_n, e_n iid Bernoulli(1/2); parity even-density.
      => single realisation fluctuates 1/2 + O(1/sqrt N) (CLT), autocorr ~ 0.

TRANSFER TEST: is the single quenched (Haar-null) orbit a statistically TYPICAL draw from the
  annealed ensemble?  i.e. |E_N^Q - 1/2| ~ 1/(2 sqrt N)  and  parity autocorr ~ i.i.d. ?
  If yes -> quenched is a "perturbation" of annealed (transfer almost works, gap = the single-orbit
  typicality, which is Haar-null and exactly Mahler/AEV). If a systematic divergence appears -> blocked.

EXACT ARITHMETIC ONLY (Python bigint). 0 false proofs: every number is measured; the [OPEN] line
  (single-orbit equidistribution) is never asserted, only its empirical margin is reported.
"""
import sys, math
import numpy as np

N = int(float(sys.argv[1])) if len(sys.argv) > 1 else 2_000_000

def v2(x):
    if x == 0: return 0
    r = 0
    while x & 1 == 0:
        x >>= 1; r += 1
    return r

# ----------------------------------------------------------------------------
# 1. QUENCHED orbit (exact)
# ----------------------------------------------------------------------------
print(f"# Antihydra ANNEALED vs QUENCHED  (N = {N:,})")
print("="*78)
import time
t0 = time.time()
par = np.empty(N, dtype=np.int8)        # parity sequence r_n
Dlist = []                              # renewal gap D = v2(3 h - 1) at ODD steps
h = 8
evens = 0
c = 0
min_c = 0
# checkpoint grid: log-spaced powers + the final point
cps = sorted(set([10,30,100,300,1000,3000,10000,30000,100000,300000,1000000,
                  2000000,3000000,5000000,7000000,10000000] + [N]))
cps = [k for k in cps if k <= N]
ckdata = {}            # k -> (Eq, c, dip_cum)
cum_min_even = 1.0     # min cumulative even-density after burn-in
burn = 1000
for n in range(N):
    b = h & 1
    par[n] = b
    if b == 0:
        evens += 1; c += 2
    else:
        c -= 1
        Dlist.append(v2(3*h - 1))   # 3h-1 even for odd h -> D>=1
    if c < min_c: min_c = c
    m = n + 1
    if m > burn:
        e_run = evens / m
        if e_run < cum_min_even: cum_min_even = e_run
    if m in ckdata or m in cps:
        ckdata[m] = (evens/m, c)
    h += h >> 1
Eq_final = evens / N
print(f"[quenched] ran N={N:,} in {time.time()-t0:.1f}s, final h has {h.bit_length():,} bits")
print(f"[quenched] final even-density Eq = {Eq_final:.6f}   counter c = {c:,}   min_c = {min_c}")

# ----------------------------------------------------------------------------
# 2. ANNEALED exact product Phi(N) (annealed carry imbalance = |E[(-1)^r]|)
# ----------------------------------------------------------------------------
def phase(j):
    num = pow(3, j) % (1 << (j + 2))
    return num / (1 << (j + 2))
Phi = {}
prod = 1.0
sum_Phi = 0.0           # running sum_{n<N} Phi(n) for the annealed-mean even-density deviation
phi_at = {}
for j in range(N):
    sum_Phi += prod
    if prod > 0.0:                      # phase(j) is a growing modexp; skip once underflowed
        prod *= abs(math.cos(math.pi * phase(j)))
Phi_final = prod
# annealed mean even-density running-average deviation bound = (1/2N) sum_{n<N} Phi(n)
ann_mean_dev = sum_Phi / (2*N)

# ----------------------------------------------------------------------------
# 3. side-by-side even-density table + transfer ratio
# ----------------------------------------------------------------------------
print()
print("## Table 1: ANNEALED vs QUENCHED even-density vs N")
print(f"{'N':>10} {'Eq(quenched)':>13} {'|Eq-1/2|':>10} {'ann mean Phi(N)':>16} {'1/(2sqrtN)':>11} {'|Eq-.5|*2sqrtN':>14}")
for k in sorted(ckdata):
    Eq, cc = ckdata[k]
    dev = abs(Eq - 0.5)
    band = 1.0/(2*math.sqrt(k))
    # annealed mean carry imbalance Phi(k): recompute cheaply (small) or use stored running prod
    pk = 1.0
    for j in range(k):
        pk *= abs(math.cos(math.pi*phase(j)))
        if pk == 0.0: break
    ratio = dev/band if band>0 else 0
    print(f"{k:>10} {Eq:>13.6f} {dev:>10.6f} {pk:>16.3e} {band:>11.6f} {ratio:>14.3f}")
print(f"\n[annealed] Phi(N) (exact carry imbalance, = |E[(-1)^r]| iid) = {Phi_final:.3e}")
print(f"[annealed] running-avg even-density MEAN deviation bound (1/2N)*sum Phi = {ann_mean_dev:.3e}")

# ----------------------------------------------------------------------------
# 4. autocorrelation: parity sequence (quenched) and D/gap sequence
# ----------------------------------------------------------------------------
print()
print("## Table 2: parity autocorrelation (quenched orbit)  vs  i.i.d. noise floor 1/sqrt(N)")
x = par.astype(np.float64); x -= x.mean()
var = (x*x).mean()
noise = 1.0/math.sqrt(N)
print(f"  var(parity) = {var:.6f}   noise floor 1/sqrt(N) = {noise:.2e}")
print(f"  {'lag':>5} {'autocorr':>12} {'|ac|/noise':>11}")
lags = [1,2,3,4,5,8,16,32,64,128,256,1024]
ac_par = {}
for L in lags:
    if L >= N: continue
    ac = (x[:-L]*x[L:]).mean()/var
    ac_par[L] = ac
    print(f"  {L:>5} {ac:>12.6f} {abs(ac)/noise:>11.2f}")

D = np.array(Dlist, dtype=np.float64)
print(f"\n## Table 3: renewal gap D=v2(3h-1) autocorrelation (over {len(D):,} odd steps)")
print(f"  mean D = {D.mean():.4f}  (geometric expectation ~2.0)   var D = {D.var():.4f}")
xd = D - D.mean(); vard = (xd*xd).mean()
nd = 1.0/math.sqrt(len(D))
print(f"  noise floor 1/sqrt(#odd) = {nd:.2e}")
print(f"  {'lag':>5} {'autocorr':>12} {'|ac|/noise':>11}")
for L in [1,2,3,4,8,16,32,64,256]:
    if L >= len(D): continue
    ac = (xd[:-L]*xd[L:]).mean()/vard
    print(f"  {L:>5} {ac:>12.6f} {abs(ac)/nd:>11.2f}")

# ----------------------------------------------------------------------------
# 5. annealed i.i.d. Monte-Carlo fluctuation band (parity even-density)
# ----------------------------------------------------------------------------
print()
print("## Table 4: ANNEALED i.i.d. Monte-Carlo (T_{n+1}=3T_n+2^n e_n, e_n~Bern(1/2)) even-density")
Nmc = 100_000
K = 12
rng = np.random.default_rng(20260628)
devs = []
ac1s = []
for s in range(K):
    bits = rng.integers(0,2,size=Nmc)
    T = 0; ev = 0
    pr = np.empty(Nmc, dtype=np.int8)
    for n in range(Nmc):
        bn = (T >> n) & 1
        pr[n] = bn
        if bn == 0: ev += 1
        T = 3*T + (int(bits[n]) << n)
    devs.append(ev/Nmc - 0.5)
    xx = pr.astype(float); xx -= xx.mean(); vv=(xx*xx).mean()
    ac1s.append((xx[:-1]*xx[1:]).mean()/vv)
devs = np.array(devs)
print(f"  K={K} seeds, length {Nmc:,}")
print(f"  mean deviation from 1/2 = {devs.mean():+.5f}   std = {devs.std():.5f}")
print(f"  CLT prediction std ~ 1/(2 sqrt N) = {1/(2*math.sqrt(Nmc)):.5f}")
print(f"  lag-1 parity autocorr (iid model): mean {np.mean(ac1s):+.5f} +- {np.std(ac1s):.5f}")

# ----------------------------------------------------------------------------
# 6. SAFETY MARGIN toward the 1/3 target (worst dip)
# ----------------------------------------------------------------------------
print()
print("## Table 5: safety margin of the one-sided target E >= 1/3")
print(f"  counter c min over run = {min_c}   (halt needs c=-1; stayed >= {min_c})")
print(f"  cumulative even-density min (after burn-in {burn}) = {cum_min_even:.6f}   "
      f"margin over 1/3 = {cum_min_even-1/3:+.6f}")
# windowed even-density minima (worst local dip) for several window sizes
print(f"  {'window W':>10} {'min windowed E':>15} {'margin over 1/3':>16}")
csum = np.concatenate([[0], np.cumsum(1 - par)])   # cumsum of evens (par==0 -> even)
for W in [100, 1000, 10000, 100000, 1000000]:
    if W >= N: continue
    we = (csum[W:] - csum[:-W]) / W
    mn = we.min()
    print(f"  {W:>10} {mn:>15.6f} {mn-1/3:>16.6f}")
print("\n[DONE]")
