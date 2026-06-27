"""
THREE-ADIC SKEW PRODUCT analysis for the induced odd map
    o' = 3^{D-1}(3o-1)/2^D,   D = v2(3o-1),   o0 = 27.

Goals:
 (S1) Verify the SKEW structure: the 3-adic valuation v3(o_{j+1}) = D_j - 1 is a
      FUNCTION of the 2-adic part (D_j depends only on o_j mod 2^a). Confirm that
      o' mod 3^b is NOT determined by o mod 3^b alone (needs D) -> 3-adic side is
      genuinely DRIVEN, not autonomous; while o' mod 2^k IS determined by o mod 2^K
      (autonomous base).
 (S2) Check whether the 3-adic valuation sequence is a PROPER (coarser) factor of
      the base or a FULL re-encoding (v3(o_{j+1}) = D_j - 1 <=> the whole itinerary).
 (S3) Reduced 6-coprime map: o = 3^e u (u coprime to 6), e=v3(o).
      Reduced recursion u_{j+1} = (3^{D_{j-1}} u_j - 1)/2^{D_j}.
      Probe u_j for: periodicity of u mod m, bias / one-sided drift, v3 feedback.
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
    m = N >> D
    return (3**(D-1)) * m, D, N, m

o0 = 27
N_STEPS = 200_000

# ---------- build orbit, collect D, v3, u ----------
orbit_D = []
orbit_v3 = []           # v3(o_j)
us = []                 # 6-coprime part u_j
es = []                 # e_j = v3(o_j)
o = o0
for j in range(N_STEPS + 2):
    e = vp(o, 3)
    u = o // (3**e)      # u coprime to 3; o odd so u coprime to 6
    es.append(e); us.append(u)
    orbit_v3.append(e)
    o_next, D, N, m = induced(o)
    orbit_D.append(D)
    o = o_next

# ---------- (S1a) skew identity v3(o_{j+1}) = D_j - 1 ----------
skew_ok = all(orbit_v3[j+1] == orbit_D[j] - 1 for j in range(N_STEPS))
print("[S1a] v3(o_{j+1}) == D_j - 1  for all j<%d :" % N_STEPS, skew_ok)

# ---------- (S1b) e_j == D_{j-1} - 1 (3-power injected = previous depth - 1) ----------
feedback_ok = all(es[j] == orbit_D[j-1] - 1 for j in range(1, N_STEPS))
print("[S1b] e_j == D_{j-1} - 1  for all 1<=j<%d :" % N_STEPS, feedback_ok)

# ---------- (S1c) BASE autonomy: does o mod 2^k determine o' mod 2^k? ----------
# Known NO (shift). Re-confirm o' mod 2^k determined by o mod 2^K with K=k+D.
# Demonstrate that the 2-adic map is autonomous in the sense that o' mod 2^k is a
# function of o mod 2^(k+max D) regardless of the 3-adic coordinate.
# We instead test: fix o mod 3^b, vary 2-adic -> o' mod 3^b changes (3-adic NOT autonomous).
def step_residues(o):
    o_next, D, N, m = induced(o)
    return o_next, D

# 3-adic NON-autonomy: take many odd o with the SAME residue mod 3^b but different D;
# show o' mod 3^b takes different values (so o mod 3^b alone cannot predict o' mod 3^b).
b = 4
mod3b = 3**b
import random
random.seed(0)
buckets = {}  # (o mod 3^b) -> set of (o' mod 3^b)
for _ in range(200000):
    o = random.randrange(1, 1 << 60) | 1   # odd
    r = o % mod3b
    onext, D = step_residues(o)
    buckets.setdefault(r, set()).add(onext % mod3b)
multi = sum(1 for s in buckets.values() if len(s) > 1)
print("[S1c] 3-adic NON-autonomy: of %d residue-classes (mod 3^%d) sampled, %d have >1 image (o mod 3^b does NOT determine o' mod 3^b)" % (len(buckets), b, multi))

# Also: o' mod 3^b IS determined by (o mod 3^b, D)?  test
buckets2 = {}  # (o mod 3^b, D) -> set of o' mod 3^b
for _ in range(200000):
    o = random.randrange(1, 1 << 60) | 1
    r = o % mod3b
    onext, D = step_residues(o)
    buckets2.setdefault((r, D), set()).add(onext % mod3b)
multi2 = sum(1 for s in buckets2.values() if len(s) > 1)
print("[S1c] (o mod 3^b, D) -> o' mod 3^b deterministic? classes=%d  with>1 image=%d" % (len(buckets2), multi2))
# Note: D drives the 3-power; but the 3-free part (3o-1)/2^D mod 3^b also needs 2-adic info
# (the /2^D), so even (o mod 3^b, D) may not suffice. Report.

# ---------- (S2) is the v3-sequence a PROPER factor or a FULL re-encoding? ----------
# v3(o_{j+1}) = D_j - 1  invertibly determines D_j (D_j = v3(o_{j+1})+1 >= 1).
# So the 3-adic valuation sequence carries EXACTLY the full itinerary (D_j).
inv_ok = all(orbit_D[j] == orbit_v3[j+1] + 1 for j in range(N_STEPS))
print("[S2] D_j recoverable from v3(o_{j+1}) (full re-encoding, NOT a coarser factor):", inv_ok)

# target equivalence: density{3|o_j} = freq(D_{j-1}>=2) = freq(D>=2)
dens_3 = sum(1 for j in range(1, N_STEPS+1) if orbit_v3[j] >= 1) / N_STEPS
freq_Dge2 = sum(1 for j in range(N_STEPS) if orbit_D[j] >= 2) / N_STEPS
dens_9 = sum(1 for j in range(1, N_STEPS+1) if orbit_v3[j] >= 2) / N_STEPS
freq_Dge3 = sum(1 for j in range(N_STEPS) if orbit_D[j] >= 3) / N_STEPS
print("[S2] density{3|o_j}=%.5f  freq(D>=2)=%.5f   density{9|o_j}=%.5f  freq(D>=3)=%.5f" % (dens_3, freq_Dge2, dens_9, freq_Dge3))
print("[S2] minimal prop density{3|o}+density{9|o}=%.5f  (target >= 0.5)" % (dens_3+dens_9))

# ---------- (S3) reduced 6-coprime map structure ----------
# u_{j+1} = (3^{D_{j-1}} u_j - 1)/2^{D_j}   verify
red_ok = True
for j in range(1, min(N_STEPS, 5000)):
    lhs = us[j+1]
    rhs_num = (3**orbit_D[j-1]) * us[j] - 1
    rhs = rhs_num // (2**orbit_D[j])
    if lhs != rhs or rhs_num % (2**orbit_D[j]) != 0:
        red_ok = False; break
print("[S3] reduced map u_{j+1}=(3^{D_{j-1}} u_j -1)/2^{D_j} holds:", red_ok)

# u mod small moduli: periodicity / bias
for M in (5, 7, 11, 13):
    c = Counter(u % M for u in us[:N_STEPS])
    # u coprime to 6 but can be divisible by these primes; expect ~uniform if generic
    vals = sorted(c.items())
    chi = 0.0
    exp = N_STEPS / M
    for r in range(M):
        chi += (c.get(r,0)-exp)**2/exp
    print("[S3] u mod %2d : chi2/dof=%.3f over %d classes (uniformity of reduced orbit)" % (M, chi/(M-1), M))

# v3 feedback: e_j = D_{j-1}-1 ; check distribution of e and that the reduced map
# does NOT regenerate 3 internally (u always coprime to 3 by construction).
u3 = sum(1 for u in us[:N_STEPS] if u % 3 == 0)
print("[S3] # u_j divisible by 3 (should be 0):", u3)

# one-sided drift in v3? cumulative sum of (e_j - 1) and (D_j-2)
import statistics
mean_e = statistics.mean(es[:N_STEPS])
mean_D = statistics.mean(orbit_D[:N_STEPS])
print("[S3] mean e_j=%.5f (= mean D -1 =%.5f)  mean D=%.5f" % (mean_e, mean_D-1, mean_D))

# does u carry a one-sided log-drift different from o? log u_n vs log o_n
log_o_end = sum(math.log(orbit_D[j]) for j in range(0))  # placeholder
# recompute o_end magnitude via sum D
sumD = sum(orbit_D[:N_STEPS])
print("[S3] sum D=%d ; log o_n ~ log o0 + sumD*log(3/2)=%.3f" % (sumD, math.log(o0)+sumD*math.log(1.5)))

# correlation of consecutive u-residues (look for hidden 1-D dynamics)
M = 7
seq = [u % M for u in us[:20000]]
trans = Counter((seq[i], seq[i+1]) for i in range(len(seq)-1))
# crude: is there forbidden transition structure?
nonzero = len(trans)
print("[S3] u mod 7 transition pairs observed: %d / %d possible (full mixing if ~49)" % (nonzero, M*M))
