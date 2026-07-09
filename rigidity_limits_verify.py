"""
Two-element numerical confirmation of the three load-bearing facts behind the
RIGIDITY LIMITS OF THE (2,3)-HOST consolidation, for TWO different lattice
elements of the shared rank-2 host on the (2,3)-solenoid:

    Antihydra  A = x(3/2) = Phi(-1, 1)
    o4         B = x(4/3) = Phi( 2,-1)

The point: the whole-host claim is NOT an Antihydra artifact.  Under the
deformation Phi(-1,1) <-> Phi(2,-1) the two finite places {2,3} swap roles,
and all three facts hold with 2<->3 interchanged.

Facts verified (exact where possible, machine-precision otherwise):
  (F1) NEUTRAL DIRECTION, zero Lyapunov: the transverse generator is an
       isometry (|.|=1) on exactly one finite place  ->  Lyapunov exponent 0.
       Antihydra: M2 = x2 on Q_3, |2|_3 = 1.
       o4:        M3 = x3 on Q_2, |3|_2 = 1.
  (F2) DISSIPATIVE / NON-RECURRENT skew base: the iterated element strictly
       increases the p-adic valuation on its contracting finite place every
       step (base shift v -> v + s, s>0), so no invariant probability, iterated
       zero times per sphere.
       Antihydra: |3/2|_3 = 1/3, shift +1 on Q_3.
       o4:        |4/3|_2 = 1/4, shift +2 on Q_2.
  (F3) COISOMETRY  R_k R_k^* = I: the base-q carry-renormalization operator on
       the top-digit character block is a coisometry (all singular values 1,
       dim ker = new top-digit dimension), because the value map
       V(t) = floor(p t / q) mod q^k is exactly q-to-1 onto  ->  its twisted
       pullback is an isometry, whose adjoint R_k is a coisometry.
       Antihydra: q=2, p=3.   o4: q=3, p=4.
"""
import numpy as np
from fractions import Fraction as Fr

def vp(n, p):
    """p-adic valuation of a nonzero integer."""
    if n == 0:
        return None
    k = 0
    while n % p == 0:
        n //= p
        k += 1
    return k

def val_frac(fr, p):
    """v_p of a nonzero rational = v_p(num) - v_p(den)."""
    num, den = fr.numerator, fr.denominator
    a = 0
    while num % p == 0:
        num //= p; a += 1
    b = 0
    while den % p == 0:
        den //= p; b += 1
    return a - b

MACHINES = {
    "Antihydra x3/2  Phi(-1,1)": dict(u=Fr(3, 2), p=3, q=2,
        contract_place=3,           # |3/2|_3 = 1/3 contracts Q_3
        neutral_gen=("M2 = x2", 2, 3),  # generator x2 is neutral on Q_3
        depth_q=2),
    "o4       x4/3  Phi( 2,-1)": dict(u=Fr(4, 3), p=4, q=3,
        contract_place=2,           # |4/3|_2 = 1/4 contracts Q_2
        neutral_gen=("M3 = x3", 3, 2),  # generator x3 is neutral on Q_2
        depth_q=3),
}

print("="*78)
print("(F0) SHARED (2,3)-SOLENOID HOST MEMBERSHIP  (product formula: {2,3}-unit)")
print("="*78)
for name, M in MACHINES.items():
    u = M["u"]
    def smooth23(n):
        for pr in (2, 3):
            while n % pr == 0:
                n //= pr
        return n == 1
    ok = smooth23(u.numerator) and smooth23(u.denominator)
    v2, v3 = val_frac(u, 2), val_frac(u, 3)
    print(f"  {name:26s}: |u|_inf={float(u):.4f}  v2={v2:+d}  v3={v3:+d}  "
          f"-> {'IN one (2,3)-host' if ok else 'NOT {2,3}-smooth'}")

print()
print("="*78)
print("(F1) NEUTRAL DIRECTION -- transverse generator has Lyapunov exponent 0")
print("="*78)
for name, M in MACHINES.items():
    gname, gp, place = M["neutral_gen"]   # generator x(gp) acting on place Q_place
    dil = Fr(gp)  # dilation on Q_place is |gp|_place
    v = val_frac(dil, place)              # |gp|_place = place^{-v}
    lam = -v * np.log(place)             # Lyapunov exponent = log|gp|_place
    print(f"  {name:26s}: transverse gen {gname:8s} on Q_{place}:  "
          f"|{gp}|_{place} = {place}^{-v} = {place**(-v) if v==0 else Fr(1,place)**v}  "
          f"-> Lyapunov lambda = {lam:+.4f}   {'[NEUTRAL, zero]' if lam==0 else ''}")
print("  => the AIU surplus invariance (rotation of the contracting leaf by the")
print("     transverse generator) lives on a ZERO-Lyapunov coarse direction, for BOTH.")

print()
print("="*78)
print("(F2) DISSIPATIVE / NON-RECURRENT skew base on the contracting finite place")
print("="*78)
for name, M in MACHINES.items():
    u, place = M["u"], M["contract_place"]
    shift = val_frac(u, place)   # v_place INCREASES by this each step (contraction, >0)
    print(f"  {name:26s}: |u|_{place} = {place}^-{shift} = {float(Fr(1,place)**shift):.4f} < 1 "
          f"(contracts Q_{place}); radial base shift  v_{place} -> v_{place} + {shift}  "
          f"(dissipative: no invariant prob on Z, iterated 0x/sphere)")
print("  => the neutral rotation sits over the A-contracting radial base, whose shift")
print("     v -> v + s (s>0) on Z has NO invariant probability -- the Invariance-Principle /")
print("     isometric-extension hypothesis (recurrent base) fails for BOTH elements.")

print()
print("="*78)
print("(F3) COISOMETRY  R_k R_k^* = I  for the base-q carry-renormalization operator")
print("="*78)

def build_R_and_check(p, q, k):
    """
    The base-q carry-renormalization structural core (base-agnostic).

    Value map (carry pullback)  V(t) = floor(p*t/q) mod q^k  on  t in Z/q^{k+1}.
    Twisted pullback   J: C[Z/q^k] -> C[Z/q^{k+1}],  (J f)(t) = r(t) * f(V(t)),
    with r any UNIMODULAR twist (here the fresh-digit character, |r|=1).

    Structural coisometry lemma:  V exactly q-to-1 onto  AND  |r|=1
        ==>  J^H J = q * I   (columns have disjoint support, each of q ones)
        ==>  R := J^* / sqrt(q)   satisfies   R R^* = I   (COISOMETRY),
             every singular value of R equals 1, ||R|| = 1,
             dim ker R = q^{k+1} - q^k = (q-1) q^k.
    This is exactly the mechanism that forces the cross-scale operator-norm
    Lyapunov exponent to 0 (no uniform contraction), for any base q.
    """
    N1 = q ** (k + 1)
    N0 = q ** k
    t = np.arange(N1)
    V = (p * t // q) % N0                       # value map
    # (i) is V exactly q-to-1 onto Z/q^k ?
    counts = np.bincount(V, minlength=N0)
    q_to_1 = bool(np.all(counts == q))
    # unimodular fresh-digit twist
    digit_k = (t // (q ** k)) % q
    r = np.exp(2j * np.pi * digit_k / q)         # |r| = 1
    # J in delta basis: J[t, s] = r(t) * [V(t)==s]
    J = np.zeros((N1, N0), dtype=complex)
    J[t, V] = r
    JHJ = J.conj().T @ J                          # should be q * I  (isometry, up to sqrt q)
    isom_err = np.linalg.norm(JHJ - q * np.eye(N0))
    Jn = J / np.sqrt(q)                           # Jn^H Jn = I  (isometry)
    R = Jn.conj().T                               # R := J^*/sqrt(q)  (coisometry candidate)
    RRstar = R @ R.conj().T
    err = np.linalg.norm(RRstar - np.eye(N0))     # || R R^* - I ||
    sv = np.linalg.svd(R, compute_uv=False)       # singular values of R
    dim_dom = N1                                  # dim of the finer scale
    dim_cod = N0                                  # dim of the coarser scale
    dim_ker = dim_dom - dim_cod                   # (q-1) q^k
    return dict(q_to_1=q_to_1, isom_err=isom_err, RRstar_err=err,
                sv_min=sv.min(), sv_max=sv.max(),
                dim_dom=dim_dom, dim_cod=dim_cod, dim_ker=dim_ker)

for name, M in MACHINES.items():
    p, q = M["p"], M["depth_q"]
    print(f"\n  {name}   (depth place q={q}, value core floor({p}t/{q}) )")
    print(f"   k | V q-to-1 onto | ||J^HJ - qI|| | ||RR*-I|| | sv[min,max] | "
          f"dim(fine,coarse,ker)")
    for k in range(2, 7):
        r = build_R_and_check(p, q, k)
        print(f"   {k} | {str(r['q_to_1']):>12s} | {r['isom_err']:.2e}      | "
              f"{r['RRstar_err']:.2e} | [{r['sv_min']:.4f},{r['sv_max']:.4f}] | "
              f"({r['dim_dom']},{r['dim_cod']},{r['dim_ker']})")
print("\n  (q=2, Antihydra: this reproduces the repo's odd-block result R_k R_k^*=I")
print("   to machine precision -- EUE_COISOMETRY.md verified it at 4.8e-15 on the")
print("   exact odd-character seam operator.  q=3, o4: same structural coisometry,")
print("   confirming the op-norm-Lyapunov=0 no-go is NOT an Antihydra artifact.)")

print()
print("="*78)
print("SUMMARY: all three load-bearing facts hold for BOTH host elements,")
print("with the two finite places {2,3} interchanged under the deformation.")
print("No machine decided. No label upgraded.")
