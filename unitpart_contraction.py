"""
UNIT-PART 3-adic CONTRACTION of the induced odd map
    o' = 3^{D-1}(3o-1)/2^D,  D = v2(3o-1),  o0 = 27.

Object: o_j = 3^{e_j} u_j, u_j coprime to 6 (3-adic UNIT part).
Fiber affine cocycle on Z_3 (driven by base symbol D):
    Phi_D(x) = 3^{D-1} * 2^{-D} * (3x - 1) = a_D x + b_D,
    a_D = 3^D 2^{-D},  b_D = -3^{D-1} 2^{-D}   (2^{-D} a 3-adic unit).

Claims to PROVE/verify (exact big-int, .venv only):

 (C1) CONTRACTION ratio. Two orbits driven by the SAME D-sequence:
        o_{j+1}-o~_{j+1} = 3^D 2^{-D} (o_j - o~_j),  so
        |o_{j+1}-o~_{j+1}|_3 = 3^{-D_j} |o_j - o~_j|_3  EXACTLY.
      Per-step contraction = 3^{-D_j} (<= 1/3). Over L steps = 3^{-(D_{j-1}+...+D_{j-L})}.

 (C2) FREE SYNCHRONIZATION (genericity-INDEPENDENT). For ANY D-sequence,
        o_j mod 3^k is a FUNCTION of (D_{j-1},...,D_{j-L}) ALONE, independent of
        o_{j-L} (hence of o_0), as soon as  D_{j-1}+...+D_{j-L} >= k.
      Synchronization depth L(k,j) = min L with running sum of recent D >= k.

 (C3) Confirm the true integer orbit mod 3^P equals the cocycle from o0=27, and
      that reconstructing o_j mod 3^k from the D-history ONLY (arbitrary placeholder
      for o_{j-L}) matches the true value -> "two different o0 with the same recent
      D-history agree on u_j mod 3^k".

 (C4) DELIMIT free vs hard. The unit-part MARGINAL law is NOT free:
        u_{j+1} mod 3 = parity(D_j)  =>  distribution of u mod 3 = law of parity(D),
      a valuation statistic. Synchronization (conditional on D-history) is free;
      equidistribution of u (marginal) is the SAME hard D-distribution question.
"""
import random
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
N_STEPS = 200_000
P = 80                      # 3-adic precision (work mod 3^P)
MOD = 3**P

# ---------- build the real integer orbit, record D, o mod 3^P, u mod 3^P ----------
Ds = []
o_mod = []                 # true o_j mod 3^P
o = o0
for j in range(N_STEPS + 2):
    o_mod.append(o % MOD)
    onext, D = induced(o)
    Ds.append(D)
    o = onext

# affine cocycle coefficients mod 3^P:  Phi_D(x) = a_D x + b_D
inv2 = pow(2, -1, MOD)     # 2^{-1} mod 3^P
def coeffs(D):
    invD = pow(inv2, D, MOD)          # 2^{-D} mod 3^P
    a = (pow(3, D, MOD) * invD) % MOD
    b = (-pow(3, D-1, MOD) * invD) % MOD
    return a, b

# precompute for the D's that occur
coeff_cache = {}
def get_coeffs(D):
    if D not in coeff_cache:
        coeff_cache[D] = coeffs(D)
    return coeff_cache[D]

# ---------- (C0) cocycle reproduces the true integer orbit mod 3^P ----------
x = o0 % MOD
cocycle_ok = True
for j in range(N_STEPS):
    if x != o_mod[j]:
        cocycle_ok = False; break
    a, b = get_coeffs(Ds[j])
    x = (a*x + b) % MOD
print("[C0] affine cocycle Phi_D reproduces true o_j mod 3^%d for all j<%d : %s" % (P, N_STEPS, cocycle_ok))

# ---------- (C1) contraction ratio: |o'-o~'|_3 = 3^{-D}|o-o~|_3 EXACTLY ----------
# drive TWO different initial 3-adic points with the SAME real D-sequence.
random.seed(1)
x1 = o0 % MOD
x2 = (o0 + 1) % MOD        # a different starting 3-adic point (diff is a unit: v3=0)
exact = True
ratios = []
for j in range(60):        # only need until they synchronize past precision
    d_before = (x1 - x2) % MOD
    vb = v3(d_before) if d_before != 0 else P
    a, b = get_coeffs(Ds[j])
    x1 = (a*x1 + b) % MOD
    x2 = (a*x2 + b) % MOD
    d_after = (x1 - x2) % MOD
    va = v3(d_after) if d_after != 0 else P
    # predicted: va = vb + D_j (capped at P)
    pred = min(vb + Ds[j], P)
    ratios.append((vb, va, Ds[j], pred))
    if va != pred:
        exact = False
print("[C1] per-step 3-adic contraction v3(diff) increases by exactly D_j (until precision P):",
      exact)
print("     first 12 steps (v3_before, v3_after, D_j, predicted v3_after):")
for r in ratios[:12]:
    print("       ", r)

# ---------- (C1b) over-L contraction: v3(x1-x2) after L steps = sum of D_0..D_{L-1} ----------
x1 = o0 % MOD; x2 = (o0 + 2) % MOD   # diff v3=0 again (2 is a unit)
for j in range(40):
    a, b = get_coeffs(Ds[j])
    x1 = (a*x1 + b) % MOD; x2 = (a*x2 + b) % MOD
d = (x1 - x2) % MOD
cum = sum(Ds[:40])
print("[C1b] after L=40 steps: v3(diff)=%d  cumulative sum D_0..D_39=%d  (capped at P=%d) match=%s"
      % (v3(d) if d else P, cum, P, (v3(d) if d else P) == min(cum, P)))

# ---------- (C2)/(C3) FREE synchronization: o_j mod 3^k from recent D-history ONLY ----------
# Reconstruct o_j mod 3^k using window of length L ending at j, with an ARBITRARY
# placeholder for o_{j-L}. If sum(D over window) >= k, the result is independent of
# the placeholder and equals the true o_j mod 3^k. We test placeholder-independence
# (== "two different o0 same recent D-history -> same u_j mod 3^k") and correctness.
def reconstruct(j, L, placeholder):
    """apply Phi_{D_{j-L}}..Phi_{D_{j-1}} to placeholder, mod 3^P."""
    x = placeholder % MOD
    for i in range(j-L, j):
        a, b = get_coeffs(Ds[i])
        x = (a*x + b) % MOD
    return x

def sync_depth(j, k):
    """min L such that D_{j-1}+...+D_{j-L} >= k."""
    s = 0; L = 0
    while s < k and L < j:
        L += 1
        s += Ds[j-L]
    return L, s

# test correctness + placeholder independence across many j, several k
import statistics
placeholders = [0, 1, 2, 12345, MOD-1]
results = {}   # k -> list of (sync_depth_L, matches_true, placeholder_independent)
for k in (4, 8, 16, 32, 48):
    modk = 3**k
    Ls = []
    all_correct = True
    all_indep = True
    for j in range(1000, 1000+3000):    # 3000 sample positions
        L, s = sync_depth(j, k)
        Ls.append(L)
        true_val = o_mod[j] % modk
        vals = set(reconstruct(j, L, ph) % modk for ph in placeholders)
        if len(vals) != 1:
            all_indep = False
        if next(iter(vals)) != true_val:
            all_correct = False
    results[k] = (statistics.mean(Ls), min(Ls), max(Ls), all_correct, all_indep)
    print("[C2] k=%2d : sync depth L (recent D-symbols) mean=%.2f min=%d max=%d  "
          "reconstruct==true:%s  placeholder-independent:%s"
          % (k, results[k][0], results[k][1], results[k][2], results[k][3], results[k][4]))

# sanity: with L ONE SHORT (sum D < k) the placeholder leaks (NOT synchronized yet)
leak_count = 0
checked = 0
for j in range(1000, 1500):
    k = 16; modk = 3**k
    L, s = sync_depth(j, k)
    if L >= 1:
        Lshort = L - 1
        ssum = sum(Ds[j-Lshort:j])
        if ssum < k:
            checked += 1
            vals = set(reconstruct(j, Lshort, ph) % modk for ph in placeholders)
            if len(vals) > 1:
                leak_count += 1
print("[C2b] one symbol short (sumD<k): placeholder LEAKS (not yet synchronized) in %d/%d cases"
      % (leak_count, checked))

# ---------- (C4) DELIMIT: unit-part MARGINAL is NOT free (= a D-statistic) ----------
# u_j = o_j / 3^{e_j}; u_{j+1} mod 3 = parity(D_j).
us_mod3 = []
parityD = []
e = 0
for j in range(1, N_STEPS+1):
    e_j = Ds[j-1] - 1
    u_mod3 = (o_mod[j] // (3**e_j)) % 3
    us_mod3.append(u_mod3)
    parityD.append(Ds[j-1] % 2)
# u_{j} mod 3 should be 1 if D_{j-1} odd, 2 if D_{j-1} even
match = sum(1 for i in range(len(us_mod3))
            if us_mod3[i] == (1 if parityD[i]==1 else 2))
print("[C4] u_j mod 3 == (D_{j-1} odd ? 1 : 2) for %d/%d steps" % (match, len(us_mod3)))
cu = Counter(us_mod3)
print("[C4] distribution u_j mod 3: %s  (P(u=1)=%.4f, P(u=2)=%.4f, u=0 forbidden=%d)"
      % (dict(cu), cu[1]/len(us_mod3), cu[2]/len(us_mod3), cu[0]))
# law of parity(D): for geometric D, P(D odd)=2/3
pD_odd = sum(parityD)/len(parityD)
print("[C4] P(D odd)=%.4f (geometric pred 2/3=0.6667) ; so u mod 3 marginal ENCODES a D-statistic,"
      " NOT uniform on {1,2} -> unit marginal is valuation-determined (NOT free)" % pD_odd)

# ---------- (C4b) does the UNIT sequence (mod 3^k, valuations stripped) recover D? ----------
# given u_j and u_{j+1} as 3-adic units, parity(D_j) is read from u_{j+1} mod 3; can the
# FULL D_j be recovered from the unit sequence alone? Check how many low digits of u pin D_j.
# u_{j+1} = 2^{-D_j} (3^{D_{j-1}} u_j - 1). Test: given u_j, u_{j+1} mod 3^k, is D_j unique?
def unit_seq(j):
    e_j = Ds[j-1] - 1
    return (o_mod[j] // (3**e_j)) % MOD
recover_k = None
for k in (1,2,3,4,6,8):
    modk = 3**k
    ambiguous = 0
    for j in range(2000, 2200):
        uj = unit_seq(j) % modk
        ujp = unit_seq(j+1) % modk
        # candidate D_j: which D give consistent ujp from uj? (knowing D_{j-1})
        cands = []
        for Dtry in range(1, 12):
            # u_{j+1} = 2^{-Dtry}(3^{D_{j-1}} u_j -1); need uj as full unit -> use o_mod
            val = (pow(inv2, Dtry, modk) * ((pow(3, Ds[j-1], modk)*uj - 1) % modk)) % modk
            if val == ujp:
                cands.append(Dtry)
        if len(cands) > 1:
            ambiguous += 1
    print("[C4b] unit pair (u_j,u_{j+1}) mod 3^%d : ambiguous-D positions %d/200" % (k, ambiguous))
