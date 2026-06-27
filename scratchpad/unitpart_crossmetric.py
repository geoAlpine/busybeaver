"""
CROSS-METRIC test: does the FREE 3-adic synchronization of the unit part u_j
(u_j mod 3^c = function of recent D-history, a CONTRACTION, no genericity needed)
COMBINED WITH INTEGRALITY (u_j is ONE integer, residues in all places at once)
constrain the 2-adic data u_j mod 2^k -- and hence the hard target D_j?

Setup (all PROVEN, see THREEADIC_*.md):
  o_j = 3^{e_j} u_j,  u_j coprime to 6,  e_j = D_{j-1} - 1.
  u_{j+1} = (3^{e_j+1} u_j - 1) / 2^{D_j} = (3^{D_{j-1}} u_j - 1)/2^{D_j}.
  u_j mod 3^c  : determined by recent D-history (3-adic contraction, FREE).
  D_j = v2(3^{e_j+1} u_j - 1) = v2(3 o_j - 1) : determined by u_j mod 2^k (HARD).

QUESTION: along the REAL orbit, does u_j mod 3^c predict u_j mod 2^k or D_j,
beyond what CRT-independence allows? CRT says for an arbitrary integer the
mod-2 and mod-3 residues are independent; but u_j is a SPECIFIC orbit integer.

Method: measure mutual information (in bits) between u_j mod 3^c and
(a) u_j mod 2^k, (b) D_j. Compare against a SHUFFLE NULL (permute the 2-adic
column) which gives the finite-sample MI bias floor, and against CRT-independent
random 6-coprime integers. Exact big-int. .venv only. Not committed.
"""
import random, math
from collections import Counter

def v2(x):
    d = 0
    while x % 2 == 0:
        x //= 2; d += 1
    return d

def v3(x):
    d = 0
    while x % 3 == 0:
        x //= 3; d += 1
    return d

# ---- build the real orbit o0 = 27 ----
N = 300_000
o = 27
us = []        # u_j (unit part, integer)
es = []        # e_j = v3(o_j)
Ds = []        # D_j = v2(3 o_j - 1)
# we record (u_j, e_j, D_j); note u_j mod 2^k and mod 3^c read from u_j directly
for j in range(N):
    e = v3(o)
    u = o // (3**e)
    Nn = 3*o - 1
    D = v2(Nn)
    us.append(u); es.append(e); Ds.append(D)
    m = Nn // (2**D)          # odd part, 6-coprime
    o = (3**(D-1)) * m        # induced map
print(f"[orbit] built {N} induced steps from o0=27; "
      f"meanD={sum(Ds)/N:.5f}, P(D=1)={sum(1 for d in Ds if d==1)/N:.5f}")

# ---- MI estimator (plug-in, bits) ----
def mutual_info_bits(xs, ys):
    n = len(xs)
    cxy = Counter(zip(xs, ys))
    cx = Counter(xs); cy = Counter(ys)
    mi = 0.0
    for (x,y),nxy in cxy.items():
        pxy = nxy/n
        mi += pxy * math.log2(pxy / ((cx[x]/n)*(cy[y]/n)))
    return mi

def shuffle_null_mi(xs, ys, reps=20, seed=0):
    rnd = random.Random(seed)
    ys2 = list(ys)
    vals = []
    for _ in range(reps):
        rnd.shuffle(ys2)
        vals.append(mutual_info_bits(xs, ys2))
    return sum(vals)/len(vals), max(vals)

print("\n=== TEST A: MI( u_j mod 3^c ; u_j mod 2^k )  on the REAL orbit ===")
print("(shuffle-null = finite-sample bias floor; observed must EXCEED it to be a real link)")
print(f"{'c':>2} {'k':>2} {'MI_obs(bits)':>13} {'MI_shuf_mean':>13} {'MI_shuf_max':>12} {'excess':>10}")
for c in (1,2,3):
    for k in (1,2,3,4):
        m3 = [u % (3**c) for u in us]
        m2 = [u % (2**k) for u in us]
        obs = mutual_info_bits(m3, m2)
        sm, sx = shuffle_null_mi(m3, m2)
        print(f"{c:>2} {k:>2} {obs:>13.6f} {sm:>13.6f} {sx:>12.6f} {obs-sm:>10.6f}")

print("\n=== TEST B: MI( u_j mod 3^c ; D_j )  on the REAL orbit ===")
print(f"{'c':>2} {'MI_obs(bits)':>13} {'MI_shuf_mean':>13} {'MI_shuf_max':>12} {'excess':>10}")
Dcap = [min(d,8) for d in Ds]
for c in (1,2,3):
    m3 = [u % (3**c) for u in us]
    obs = mutual_info_bits(m3, Dcap)
    sm, sx = shuffle_null_mi(m3, Dcap)
    print(f"{c:>2} {obs:>13.6f} {sm:>13.6f} {sx:>12.6f} {obs-sm:>10.6f}")

print("\n=== TEST B': conditional P(D_j=1 | u_j mod 3^c) -- should be flat ~0.5 ===")
for c in (1,2):
    buckets = {}
    for u,d in zip(us,Ds):
        r = u % (3**c)
        buckets.setdefault(r, [0,0])
        buckets[r][0] += 1
        if d==1: buckets[r][1]+=1
    print(f" c={c}: " + ", ".join(f"r={r}:P(D=1)={cnt[1]/cnt[0]:.4f}(n={cnt[0]})"
                                   for r,cnt in sorted(buckets.items())))

print("\n=== TEST C: BASELINE -- CRT-independent random 6-coprime integers ===")
print("(build random integers, read mod 3^c and mod 2^k; MI should match shuffle floor)")
rnd = random.Random(12345)
rand_u = []
while len(rand_u) < N:
    r = rnd.getrandbits(64) | 1     # odd
    if r % 3 != 0:
        rand_u.append(r)
print(f"{'c':>2} {'k':>2} {'MI_obs(bits)':>13} {'MI_shuf_mean':>13} {'excess':>10}")
for c in (1,2):
    for k in (1,2,3):
        m3 = [u % (3**c) for u in rand_u]
        m2 = [u % (2**k) for u in rand_u]
        obs = mutual_info_bits(m3, m2)
        sm,_ = shuffle_null_mi(m3, m2)
        print(f"{c:>2} {k:>2} {obs:>13.6f} {sm:>13.6f} {obs-sm:>10.6f}")

print("\n=== TEST D: SANITY -- u_j mod 3 vs parity(D_j) (PROVEN deterministic, C4) ===")
# u_{j+1} mod 3 = parity(D_j); check the FORWARD relation u_j mod3 vs D_{j-1}
bad = sum(1 for j in range(1,N) if us[j] % 3 != (1 if Ds[j-1]%2==1 else 2))
# leading 3-adic digit of o_{j} = parity(D_{j-1}); u_{j} mod 3 encodes it
print(f" u_j mod3 vs parity(D_(j-1)) [u%3==1 iff D_prev odd]: mismatches={bad} / {N-1}")

print("\n=== TEST E: does u_j mod 3^c (free) + u_j mod 2^k jointly OVER-determine vs CRT? ===")
print(" check: is the pair (u mod 3^c, u mod 2^k) distribution = product (CRT) on orbit?")
for c,k in ((1,2),(2,2),(1,3)):
    m3 = [u % (3**c) for u in us]
    m2 = [u % (2**k) for u in us]
    joint = Counter(zip(m3,m2)); c3 = Counter(m3); c2 = Counter(m2)
    # chi-square vs product
    chi = 0.0; dof=0
    for r3 in c3:
        for r2 in c2:
            exp = c3[r3]*c2[r2]/N
            obs = joint.get((r3,r2),0)
            if exp>0:
                chi += (obs-exp)**2/exp; dof+=1
    dof -= (len(c3)-1)+(len(c2)-1)+1
    print(f" c={c},k={k}: chi2={chi:.2f}, dof={dof}, chi2/dof={chi/max(dof,1):.3f}")
