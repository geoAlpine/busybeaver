"""
unitpart_observable.py  -- the load-bearing test:
Is ANY equivalent or sufficient non-halting condition UNIT-PART measurable (free)?

Setup (all [PROVEN] elsewhere):
  induced odd map  o -> o' = 3^{D-1}(3o-1)/2^D,  D = v2(3o-1),  o0 = 27.
  v3(o_{j+1}) = D_j - 1  (valuation channel = full base itinerary, invertible).
  fiber 3-adic cocycle  Phi_D(y) = 3^{D-1} 2^{-D} (3y-1)  on Z_3, a |.|_3 contraction
  whose UNIT part synchronizes FOR FREE (pathwise, any base sequence, no genericity).

Tests:
 S1  synchronization is free AND happens for ANY symbol sequence, including a
     HALTING-type sequence (all D=1) -> so the free property is shared with the
     halting fixed point o=1  => cannot imply non-halting.
 S2  u_j mod 3^k is a finite sliding-window function of the D-symbols (re-encoded
     base data), NOT an independent free channel.
 S3  does any unit-part functional bound / correlate with balance_n or even-density?
     (balance is an unbounded Birkhoff PARTIAL SUM; window functionals can't bound it.)
 S4  the only thing the unit part can compute is finite-window D-data; the target is
     the CESARO AVERAGE of D, whose convergence IS genericity (not free).

Exact big-int.  Numerics only.  Zero false proofs.
"""
import math
from collections import defaultdict

def v2(x):
    return (x & -x).bit_length() - 1 if x else 10**9

def v3(x):
    if x == 0: return 10**9
    c = 0
    while x % 3 == 0:
        x //= 3; c += 1
    return c

# ---- build induced orbit of o0 = 27 ----
def induced_orbit(o0, N):
    o = o0
    os = [o]; Ds = []
    for _ in range(N):
        D = v2(3*o - 1)
        o = 3**(D-1) * (3*o - 1) // 2**D
        Ds.append(D); os.append(o)
    return os, Ds

N = 200000
os, Ds = induced_orbit(27, N)
print(f"[setup] induced orbit of o0=27, {N} steps, max o has {os[-1].bit_length()} bits")

# valuation channel check: v3(o_{j+1}) = D_j - 1
bad = sum(1 for j in range(N) if v3(os[j+1]) != Ds[j]-1)
print(f"[S0] v3(o_{{j+1}})=D_j-1 violations: {bad}  (invertible: D_j=v3(o_{{j+1}})+1)")

# ---- unit part u_j = o_j / 3^{v3(o_j)},  read mod 3^k ----
def unit_mod(o, k):
    e = v3(o)
    u = o // 3**e
    return u % (3**k)

# =====================================================================
# S1: free synchronization holds for ANY symbol sequence (quenched),
#     including a HALTING-type all-D=1 sequence -> shared with halting fixed pt.
# =====================================================================
def phi_step(y, D, mod):
    inv2D = pow(pow(2, D, mod), -1, mod)
    return (pow(3, D-1, mod) * inv2D * (3*y - 1)) % mod

def sync_test(Dseq, b, y0, y0p):
    mod = 3**b
    y, yp = y0 % mod, y0p % mod
    for D in Dseq:
        y = phi_step(y, D, mod); yp = phi_step(yp, D, mod)
    return v3((y - yp) % mod), b  # v3 of the gap; if = b it fully synchronized

b = 40
# (a) drive with the REAL non-halting orbit's symbols
g_real = sync_test(Ds[:b+5], b, 5, 100)[0]
# (b) drive with a HALTING-type sequence: all D=1 forever (this is the o=1 fixed pt regime)
g_halt = sync_test([1]*(b+5), b, 5, 100)[0]
# (c) drive with low-even-density (mostly D=1, few D=2) "would-halt" sequence
import itertools
g_lowdens = sync_test(([1,1,1,1,2]*((b+5)//5+1))[:b+5], b, 5, 100)[0]
print(f"\n[S1] free fiber synchronization (gap reaches v3 = b = {b} means fully synced):")
print(f"     real non-halting D-seq : v3(gap) = {g_real}  (synced={g_real>=b})")
print(f"     HALTING all-D=1 seq    : v3(gap) = {g_halt}  (synced={g_halt>=b})")
print(f"     low-density 4:1 seq    : v3(gap) = {g_lowdens}  (synced={g_lowdens>=b})")
print("     => synchronization is FREE and identical for halting & non-halting symbol")
print("        sequences. The contraction does not see the frequency of D>=2.")

# =====================================================================
# S2: u_j mod 3^k is a finite sliding-window function of (D_{j-1},...,D_{j-w}).
#     Show: window of length w determines u_j mod 3^k (0 multi-image) for w>=k,
#     and FAILS for too-short windows -> it is re-encoded base data, not free extra.
# =====================================================================
print("\n[S2] is u_j mod 3^k determined by a finite window of recent D-symbols?")
for k in (1,2,3):
    for w in (k-1, k, k+1, k+2):
        if w < 1: continue
        m = defaultdict(set)
        for j in range(w, N):
            window = tuple(Ds[j-w:j])      # D_{j-w}..D_{j-1}
            m[window].add(unit_mod(os[j], k))
        multi = sum(1 for v in m.values() if len(v) > 1)
        print(f"     k={k} window w={w}: {len(m)} classes, {multi} multi-image  "
              f"({'DETERMINISTIC' if multi==0 else 'not yet'})")

# =====================================================================
# S3: does any unit-part functional bound or correlate with balance_n /
#     even-density?  balance_n = 3 E_n - n is the running Birkhoff partial sum.
#     Map induced-step quantities back to original-time even-density via mean D.
# =====================================================================
print("\n[S3] does the free unit field bound the balance?")
# even-density (original c-time) relates to D: each induced step contributes D ones
# (D even substeps? ) -- use the proven renewal identity: even-density = 1 - 1/meanD.
# Here we test correlation between unit-part residues and the LOCAL D (the only
# target-relevant quantity) and against the running balance proxy.
# running 'balance' proxy on induced clock: B_J = sum_{j<J}(D_j - 3/2) (>=0 == non-halt margin)
import statistics
B = 0; Bs = []
for j in range(N):
    B += (Ds[j] - 1.5); Bs.append(B)
print(f"     induced-clock balance proxy  min={min(Bs):.1f}  end={Bs[-1]:.1f}  (stays >=0 => non-halt)")

# correlation of u_j mod 3^k (as integer feature) with the FUTURE running balance increment
# and with the local target indicator 1[D_j>=2]:
for k in (1,2,3,4):
    feats = [unit_mod(os[j], k) for j in range(N)]
    indD2 = [1 if Ds[j] >= 2 else 0 for j in range(N)]   # target-relevant local bit
    # Pearson corr(feature, local D>=2)
    def pear(a, c):
        ma, mc = sum(a)/len(a), sum(c)/len(c)
        num = sum((x-ma)*(y-mc) for x,y in zip(a,c))
        da = math.sqrt(sum((x-ma)**2 for x in a)); dc = math.sqrt(sum((y-mc)**2 for y in c))
        return num/(da*dc) if da*dc else 0.0
    r_local = pear(feats, indD2)
    # corr of u_j with the running balance LEVEL B_j (does unit predict where balance is?)
    r_bal = pear(feats, Bs)
    print(f"     k={k}: corr(u mod 3^k, 1[D_j>=2]) = {r_local:+.4f}   "
          f"corr(u mod 3^k, balance_level) = {r_bal:+.4f}")

# Can u_j mod 3^k PREDICT 1[D_j>=2] perfectly (classification)?  (the leading-digit fact)
print("\n[S3b] can the unit part RECOVER the local target bit 1[D_j>=2]?")
for k in (1,2):
    # build predictor: most common 1[D>=2] per u-class, measure accuracy
    cls = defaultdict(lambda: [0,0])
    for j in range(N):
        cls[unit_mod(os[j],k)][1 if Ds[j]>=2 else 0]+=1
    correct = sum(max(c) for c in cls.values()); acc = correct/N
    print(f"     k={k}: best per-class accuracy predicting 1[D_j>=2] = {acc:.4f}")
print("     NOTE: u_j is the unit of o_j; the LOCAL D_j lives in o_{j+1}'s valuation.")
# the honest test: predict 1[D_j>=2] from u_{j+1}'s LOW data is just reading v3(o_{j+1}) -> trivial.

# =====================================================================
# S4: the target is a CESARO AVERAGE; synchronization gives integrands, not averages.
# =====================================================================
print("\n[S4] target = Cesaro average; show partial averages converge but that IS genericity")
for frac in (0.01,0.1,0.5,1.0):
    M = max(1,int(N*frac))
    md = sum(Ds[:M])/M
    fd2 = sum(1 for d in Ds[:M] if d>=2)/M
    print(f"     first {M:6d}: mean D = {md:.5f}  freq(D>=2) = {fd2:.5f}  "
          f"(need meanD>=3/2 / freq>=1/2)")
print("     convergence of these AVERAGES = single-orbit genericity = the OPEN kernel.")
print("     the free synchronization gives each integrand value but never the average.")
