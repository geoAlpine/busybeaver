#!/usr/bin/env python3
"""Numerics for MAGNITUDE_LYAPUNOV.md. Exact big-int / Fraction. .venv only."""
from fractions import Fraction as F
import math

LOG2_3_2 = math.log2(1.5)  # c

def v2(n):
    d = 0
    while n % 2 == 0:
        n //= 2; d += 1
    return d

def D_of(o):
    return v2(3*o - 1)

def T(o):
    d = D_of(o)
    return 3**(d-1) * (3*o - 1) // 2**d

def psi(o):
    d = D_of(o)
    return 0.5 if d == 1 else (-0.5 if d == 2 else -1.5)

print("="*70)
print("1. EXACT size-drift identity  log2(T/o) = D*log2(3/2) + eps(o)")
print("   eps(o) = log2(1 - 1/(3o)),  must be <0 and ->0")
print("="*70)
for o in [3,5,27,1001,10**6+1, 10**12+ (pow(3,-1,2**40) if False else 7)]:
    pass
for o in [3,5,7,27,1001,1_000_001,1_000_000_007]:
    if o % 2 == 0: o+=1
    d = D_of(o); To = T(o)
    lhs = math.log2(To/o)
    drift = d*LOG2_3_2
    eps = math.log2(1 - 1/(3*o))
    print(f" o={o:>13d} D={d} log2(T/o)={lhs:+.8f} D*c={drift:+.8f} "
          f"eps={eps:+.3e} resid={lhs-(drift+eps):+.2e}")

print()
print("="*70)
print("2. HIGH-D AT LARGE o: arbitrarily large integers o>M0 with large D")
print("   o == 3^{-1} mod 2^d gives D=v2(3o-1)>=d, choose o huge.")
print("="*70)
M0 = 10**9
for d in [5,10,20,40]:
    inv3 = pow(3, -1, 2**d)
    # smallest o>M0 in class inv3 mod 2^d
    k = (M0 - inv3)//(2**d) + 1
    o = inv3 + k*2**d
    if o % 2 == 0: o += 2**d
    dd = D_of(o)
    print(f" d_target={d:>2d}  o={o:>20d} (> M0={M0:.0e})  D=v2(3o-1)={dd:>2d}  "
          f"o>M0:{o>M0}")
print(" => large D occurs at arbitrarily large o; threshold o>M0 does NOT exclude it.")

print()
print("="*70)
print("3. sup over constant-D=d invariant measures of  int psi_tilde  vs alpha")
print("   int psi_tilde(delta_{o_d}) = psi(d) - alpha*c*d ; psi(d)=+.5,-.5,-1.5")
print("="*70)
def psi_d(d): return 0.5 if d==1 else (-0.5 if d==2 else -1.5)
for alpha in [-1.0,-0.5,-0.1, 0.5, 0.8548, 0.9, 1.5]:
    vals = [psi_d(d) - alpha*LOG2_3_2*d for d in range(1,201)]
    sup = max(vals)
    # trend: value at large d
    big = psi_d(200) - alpha*LOG2_3_2*200
    print(f" alpha={alpha:+.4f}  sup_(d<=200)={sup:+.4f}  val@d=200={big:+10.3f}  "
          f"{'-> +inf (INFEASIBLE)' if alpha<0 else ('VACUOUS-sign' )}")
print(" threshold for feasibility (alpha>0): alpha >= 0.5/c =",
      0.5/LOG2_3_2)

print()
print("="*70)
print("4. Orbit of o0=27: (1/N) sum psi_tilde  for various alpha, plus growth")
print("="*70)
def run(N):
    o=27; sums={}; sumpsi=0.0; sumD=0
    alphas=[-0.5,-0.1,0.5,0.8548,0.9]
    acc={a:0.0 for a in alphas}
    logo0=math.log2(27)
    for j in range(N):
        d=D_of(o); p=psi(o)
        sumpsi+=p; sumD+=d
        for a in alphas: acc[a]+= p - a*LOG2_3_2*d
        o=T(o)
    return o,sumpsi/N,sumD/N,{a:acc[a]/N for a in alphas},math.log2(o)
for N in [1000,10000,100000]:
    o,ap,aD,acc,logo=run(N)
    s=" ".join(f"a={a:+.3f}:{v:+.4f}" for a,v in acc.items())
    print(f" N={N:>6d} avg psi={ap:+.4f} avg D={aD:.4f} log2(o_N)={logo:.1f}")
    print(f"        (1/N)sum psi_tilde: {s}")
print(" Note: for alpha<0, (1/N)sum psi_tilde ~ avg psi + |alpha|*c*avg D > 0 along ORBIT")
print("       too (generic orbit has avg D~2); the +inf sup is the per-measure statement,")
print("       and the per-STEP large-D constraint is what kills bounded h.")
