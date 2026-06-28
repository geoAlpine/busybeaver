"""
Floor <-> Ceiling bridge for the 3/2 maps (FLOOR_MIRROR_CONJECTURE.md).

Maps on Z (exact big-int):
  Tf(x) = floor(3x/2)   (Antihydra-family floor map)
  Tc(x) = ceil (3x/2)   (AEV Conj 1.6 ceiling map)

Branch forms:
  even x:  Tf=Tc = 3x/2
  odd  x:  Tf = (3x-1)/2 ,  Tc = (3x+1)/2

Claimed PROVEN bridge (negation conjugacy R(x) = -x, R=R^{-1}):
  Tc(x) = -Tf(-x)   for ALL x in Z   (=> Tc = R o Tf o R)
  hence Tf^l(n) = -Tc^l(-n)  for all l.

Induced odd maps:
  floor   : T(o)  = 3^{D-1}(3o-1)/2^D , D  = v2(3o-1)   , o0 = 27
  ceiling : T'(m) = 3^{D'-1}(3m+1)/2^{D'}, D' = v2(3m+1)

Claimed: D_l^floor(o0) = D_l^ceil(-o0) for every l  (exact depth-sequence equality).

Tests:
 (A) global conjugacy Tc(x) = -Tf(-x), and Tf^l(n) = -Tc^l(-n)  over many n,l
 (B) cross-check branch defs (even/odd) match floor/ceil of 3x/2
 (C) induced depth equality D_l^floor(27) == D_l^ceil(-27), all l
 (D) residue distributions mod 2^k:
       floor orbit of 27  vs ceiling orbit of -27   (must be IDENTICAL via bridge)
       floor orbit of 27  vs ceiling orbit of +27   (different seeds: both ~Haar, NOT identical)
 (E) one-sided density fragment (Antihydra kernel): freq(D>=2) for floor(27) == for ceil(-27)
"""
import math
from collections import Counter

def v2(x):
    x = abs(x)
    if x == 0:
        return 99
    d = 0
    while x % 2 == 0:
        x //= 2; d += 1
    return d

def Tf(x):  # floor(3x/2), exact for negatives too (Python // is floor division)
    return (3 * x) // 2

def Tc(x):  # ceil(3x/2)
    return -((-3 * x) // 2)

# ---------- (B) cross-check branch defs ----------
ok_branch = True
for x in range(-50, 51):
    f_expect = 3*x//2 if x % 2 == 0 else (3*x - 1)//2
    # for odd negative x, (3x-1)//2 must equal floor; Python // is floor so just compare to math.floor
    if Tf(x) != math.floor(3*x/2) and abs(x) < 10**6:
        ok_branch = False
    if Tc(x) != math.ceil(3*x/2) and abs(x) < 10**6:
        ok_branch = False
print("(B) branch defs Tf=floor(3x/2), Tc=ceil(3x/2) for x in [-50,50]:", ok_branch)

# ---------- (A) global conjugacy ----------
ok_conj = True
for x in range(-200, 201):
    if Tc(x) != -Tf(-x):
        ok_conj = False
print("(A1) Tc(x) == -Tf(-x) for x in [-200,200]:", ok_conj)

ok_orbit = True
for n in [1, 8, 27, 100, 1000, 99991, 2**40 + 1]:
    xf = n; xc = -n
    for l in range(400):
        if xf != -xc:
            ok_orbit = False; break
        xf = Tf(xf); xc = Tc(xc)
print("(A2) Tf^l(n) == -Tc^l(-n) for several n, l<400:", ok_orbit)

# ---------- (C) induced depth equality ----------
def induced_floor(o):
    N = 3*o - 1
    D = v2(N)
    m = N >> D
    return (3**(D-1)) * m, D

def induced_ceil(m):
    N = 3*m + 1          # for NEGATIVE odd m this is negative; use signed handling
    D = v2(N)            # v2 uses abs
    # odd part w.r.t 2, preserving sign
    u = N >> D if N > 0 else -((-N) >> D)
    return (3**(D-1)) * u, D

NSTEP = 200_000
of = 27; mc = -27
Df_seq = []; Dc_seq = []
depth_equal = True
for _ in range(NSTEP):
    of, Df = induced_floor(of)
    mc, Dc = induced_ceil(mc)
    Df_seq.append(Df); Dc_seq.append(Dc)
    if Df != Dc:
        depth_equal = False
# also confirm mc == -of throughout (induced conjugacy)
print("(C) induced depth equality D_l^floor(27)==D_l^ceil(-27) over",
      NSTEP, "steps:", depth_equal)
print("    mc == -of at end:", mc == -of)
print("    mean Df = %.6f  mean Dc = %.6f  (Haar 2)" %
      (sum(Df_seq)/NSTEP, sum(Dc_seq)/NSTEP))

# ---------- (E) one-sided Antihydra fragment ----------
fge2_f = sum(1 for d in Df_seq if d >= 2) / NSTEP
fge2_c = sum(1 for d in Dc_seq if d >= 2) / NSTEP
print("(E) freq(D>=2) floor(27)=%.6f  ceil(-27)=%.6f  (kernel target >=1/2; identical):"
      % (fge2_f, fge2_c), abs(fge2_f - fge2_c) < 1e-15)

# ---------- (D) residue distributions mod 2^k along the FULL (not induced) orbit ----------
def full_orbit_residues(start, step_map, n, k):
    K = 1 << k
    c = Counter()
    x = start
    for _ in range(n):
        c[x % K] += 1     # Python % gives nonneg residue even for negative x
        x = step_map(x)
    return c

NORB = 100_000
for k in (2, 3, 4):
    cf = full_orbit_residues(27, Tf, NORB, k)        # floor, seed +27
    cc_neg = full_orbit_residues(-27, Tc, NORB, k)    # ceil, seed -27 (bridge image)
    cc_pos = full_orbit_residues(27, Tc, NORB, k)     # ceil, seed +27 (different orbit)
    K = 1 << k
    # bridge identity: floor(+27) residue r  <->  ceil(-27) residue (-r mod K)
    identical = all(cf[r] == cc_neg[(-r) % K] for r in range(K))
    # max deviation from uniform (NORB/K) for floor(+27) and ceil(+27)
    dev_f = max(abs(cf[r] - NORB/K) for r in range(K)) / NORB
    dev_cpos = max(abs(cc_pos[r] - NORB/K) for r in range(K)) / NORB
    # are floor(+27) and ceil(+27) the SAME residue sequence-distribution? expect NO (different orbits)
    same_pos = all(cf[r] == cc_pos[r] for r in range(K))
    print(f"(D) k={k}: bridge identity floor(+27)[r]==ceil(-27)[-r]:", identical,
          f"| maxdev floor(+27)={dev_f:.4f} ceil(+27)={dev_cpos:.4f}",
          f"| floor(+27)==ceil(+27) distrib:", same_pos)
