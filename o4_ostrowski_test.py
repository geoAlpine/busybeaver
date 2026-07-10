"""
o4 Ostrowski / three-distance / Denjoy-Koksma verification.

Goal: compute the continued-fraction / Ostrowski structure of the key
archimedean rotation number beta = log(4/3)/log(3), get an effective
discrepancy for {n beta}, and test whether that archimedean control couples
to the 3-adic digit frequency freq{3 | W_n} of the actual o4 orbit.

Interpreter: /Users/aokiyousuke/quantum-ecc/.venv/bin/python
Exact where possible; mpmath high precision for the transcendental beta.
"""
import mpmath as mp
from fractions import Fraction

mp.mp.dps = 220  # high precision

# ---------------------------------------------------------------------------
# 1. The archimedean rotation number(s)
# ---------------------------------------------------------------------------
# W_n ~ alpha*(4/3)^n.  log_3 W_n = log_3 alpha + n * log_3(4/3).
# The relevant rotation on the circle (base-3 mantissa / leading-digit motion)
# is beta = log(4/3)/log(3) = log_3(4/3) = log_3(4) - 1.
log3 = mp.log(3)
beta = mp.log(mp.mpf(4)/3) / log3          # = log_3(4/3)
gamma = mp.log(4) / log3                    # = log_3 4  (= beta + 1, same CF tail)
print("beta  = log_3(4/3) =", mp.nstr(beta, 40))
print("gamma = log_3(4)   =", mp.nstr(gamma, 40))
print("beta mod 1 =", mp.nstr(beta - mp.floor(beta), 40))

def cont_frac(x, n):
    """First n partial quotients of x (x>0)."""
    a = []
    y = mp.mpf(x)
    for _ in range(n):
        f = mp.floor(y)
        a.append(int(f))
        frac = y - f
        if frac == 0:
            break
        y = 1/frac
    return a

def convergents(a):
    """p/q convergents from partial quotients a."""
    hm2, hm1 = 0, 1
    km2, km1 = 1, 0
    out = []
    for ai in a:
        h = ai*hm1 + hm2
        k = ai*km1 + km2
        out.append((h, k))
        hm2, hm1 = hm1, h
        km2, km1 = km1, k
    return out

# partial quotients: compute plenty, but only trust those safely inside precision
A = cont_frac(beta, 80)
print("\npartial quotients of beta (a0=%d frac part):" % A[0])
# beta in (0,1) so a0 = 0
print(A[:60])

conv = convergents(A)
print("\nconvergents p_k/q_k and approx quality q_k*|q_k*beta - p_k|:")
# quality theta_k = q_k * ||q_k beta|| ; a_{k+1} ~ 1/theta_k
for k in range(min(40, len(conv))):
    p, q = conv[k]
    err = abs(q*beta - p)
    theta = q*err
    # guard: only print while err >> 10^-(dps-20)
    if err < mp.mpf(10)**(-(mp.mp.dps-25)):
        print("  ... beyond reliable precision, stop at k=%d" % k)
        break
    akp1 = A[k+1] if k+1 < len(A) else None
    print("  k=%2d  a_{k+1}=%-4s q_k=%-22d  q*||q beta||=%s" %
          (k, str(akp1), q, mp.nstr(theta, 8)))

# Largest partial quotient among the reliable ones
# find reliable cutoff
def reliable_len(x, A, conv):
    lim = mp.mpf(10)**(-(mp.mp.dps-25))
    r = 0
    for k,(p,q) in enumerate(conv):
        if abs(q*x-p) < lim:
            break
        r = k+1
    return r

rk = reliable_len(beta, A, conv)
print("\nreliable partial quotients (count=%d):" % rk, A[:rk])
print("max partial quotient a_k (k<=%d):" % rk, max(A[1:rk]))
print("mean of a_k:", sum(A[1:rk])/(rk-1))
