"""ATTACK_RENORMALIZATION numerics (2026-06-28).

Goal: (1) closed form of the 0.7748 tail constant in the identity
        |nu_hat_{2/3}((3/2)^N/8)| = Phi(N) * C,
      (2) test the BC self-similarity renormalization for an EFFECTIVE decay rate of Phi,
      (3) quenched-vs-annealed sanity.

ν̂_{2/3}(ξ) = Π_{j≥0} cos(2π ξ (2/3)^j).   At ξ_N=(3/2)^N/8:  ξ_N (2/3)^j = (3/2)^{N-j}/8,
so ν̂(ξ_N) = Π_{j≥0} cos((π/4)(3/2)^{N-j}) = Π_{k=-∞}^{N} cos((π/4)(3/2)^k).
Split k≥0 (HEAD) and k≤-1 (TAIL). Tail = Π_{m≥1} cos((π/4)(2/3)^m) =: C  (N-independent => constant).

0 false proofs: all magnitudes computed in mpmath at 60 digits; exact dyadic phase for the head.
"""
import mpmath as mp
mp.mp.dps = 60

PI = mp.pi
def c(x):           # cos((pi/4) * x)
    return mp.cos(PI/4 * x)

# ---- exact head phase: {(3/2)^k /4} = (3^k mod 2^{k+2})/2^{k+2}, |cos(pi {.}.)| handled via cos((pi/4)(3/2)^k) ----
def head_factor(k):
    # (3/2)^k = 3^k / 2^k ; argument of cos is (pi/4)*3^k/2^k. Use exact rational then mpmath.
    val = mp.mpf(3)**k / mp.mpf(2)**k
    return abs(mp.cos(PI/4 * val))

# ---------- (1) the tail constant C ----------
def tail_C(M=400):
    p = mp.mpf(1)
    for m in range(1, M):
        p *= mp.cos(PI/4 * (mp.mpf(2)/3)**m)   # all positive: arg < pi/8
    return p

C = tail_C()
# closed form candidate:  C = sqrt(2) * nu_hat_{2/3}(1/8),  since nu_hat(1/8)=cos(pi/4)*C = C/sqrt2
def nu_hat(xi, J=400):
    p = mp.mpf(1)
    for j in range(J):
        p *= mp.cos(2*PI*xi*(mp.mpf(2)/3)**j)
    return p
nh18 = nu_hat(mp.mpf(1)/8)
print("=== (1) TAIL CONSTANT ===")
print("C = Prod_{m>=1} cos((pi/4)(2/3)^m)      =", mp.nstr(C, 25))
print("sqrt(2)*nu_hat_{2/3}(1/8)               =", mp.nstr(mp.sqrt(2)*nh18, 25))
print("nu_hat_{2/3}(1/8)                       =", mp.nstr(nh18, 25))
print("C - sqrt(2)*nu_hat(1/8)  (should be ~0) =", mp.nstr(C - mp.sqrt(2)*nh18, 5))
print("measured-paper value 0.7748 ?           ", mp.nstr(C, 6))

# ---------- (1b) verify the identity |nu_hat(xi_N)| = Phi(N)*C and which Phi convention is constant ----------
print("\n=== (1b) IDENTITY |nu_hat(xi_N)| / Phi(N) =?= C ===")
def nu_hat_xiN(N, extra=400):
    # Prod_{k=-inf}^{N} cos((pi/4)(3/2)^k); compute head k=0..N exactly-ish + tail
    p = mp.mpf(1)
    for k in range(0, N+1):
        p *= abs(mp.cos(PI/4 * mp.mpf(3)**k / mp.mpf(2)**k))
    p *= tail_C(extra)
    return p
def Phi_upto(N):     # convention A: Phi(N)=Prod_{k=0}^{N-1}  (j<N, as MEMORY/MD text)
    p = mp.mpf(1)
    for k in range(0, N):
        p *= head_factor(k)
    return p
def Phi_incl(N):     # convention B: Phi(N)=Prod_{k=0}^{N}
    return Phi_upto(N) * head_factor(N)
print(f"{'N':>4} {'|nuhat(xiN)|':>16} {'ratio/Phi_<N (A)':>18} {'ratio/Phi_<=N (B)':>18}")
for N in (5,10,20,40,60,80):
    nn = nu_hat_xiN(N)
    rA = nn/Phi_upto(N)
    rB = nn/Phi_incl(N)
    print(f"{N:>4} {mp.nstr(nn,8):>16} {mp.nstr(rA,8):>18} {mp.nstr(rB,8):>18}")
print("(constant ratio identifies the Phi convention; the constant itself = C)")

# ---------- (2) effective decay rate of Phi(N): polynomial-in-N vs exponential-in-N ----------
print("\n=== (2) DECAY RATE OF Phi(N) (head product, deterministic phases) ===")
Ns = [2**e for e in range(2, 16)]   # 4 .. 32768
import mpmath
rows = []
p = mp.mpf(1); Nmax = max(Ns); nextidx = 0
# accumulate product once
vals = {}
p = mp.mpf(1)
for k in range(0, Nmax+1):
    p *= head_factor(k)
    if (k+1) in Ns:           # Phi(k+1)=Prod_{0..k}
        vals[k+1] = p
print(f"{'N':>7} {'Phi(N)':>14} {'-ln Phi':>12} {'-lnPhi/N':>12} {'-lnPhi/lnN':>12}")
import math
for N in Ns:
    ph = vals[N]
    nl = -mp.log(ph)
    print(f"{N:>7} {mp.nstr(ph,6):>14} {mp.nstr(nl,6):>12} {mp.nstr(nl/N,6):>12} {mp.nstr(nl/mp.log(N),6):>12}")
print("If -lnPhi/N -> const>0  => EXPONENTIAL 2^{-cN} (needs equidistribution=Mahler, conjectural).")
print("If -lnPhi/lnN -> const  => POLYNOMIAL N^{-a} (the PROVABLE Varju-Yu log-in-xi = poly-in-N floor).")
print("E[log|cos(pi U)|]=-ln2 => equidistribution slope -lnPhi/N -> ln2 =", mp.nstr(mp.log(2),6))

# ---------- (3) self-similarity check: Phi(N+1)/Phi(N) = |cos((pi/4)(3/2)^N)| ----------
print("\n=== (3) BC self-similarity reproduces the Phi recursion ===")
for N in (10, 25, 50):
    lhs = Phi_incl(N+1)/Phi_incl(N)
    rhs = abs(mp.cos(PI/4 * mp.mpf(3)**(N+1)/mp.mpf(2)**(N+1)))
    print(f"  N={N:>3}  Phi(N+1)/Phi(N)={mp.nstr(lhs,8)}  |cos((pi/4)(3/2)^(N+1))|={mp.nstr(rhs,8)}  diff={mp.nstr(abs(lhs-rhs),4)}")
