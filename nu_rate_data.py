"""DATA: effective Fourier-decay rate of the Bernoulli convolution nu_{2/3}.

nu_hat_{2/3}(xi) = prod_{j>=0} cos(2 pi xi (2/3)^j).  3/2 is non-Pisot => Rajchman (decay to 0);
the RATE (polynomial power-law vs only logarithmic) is the question this script measures.

SOUNDNESS: all Fourier magnitudes computed with EXACT rational reduction of the phase
   {xi (2/3)^j} = (xi*2^j mod 3^j)/3^j     (xi integer)
so there is NO floating-point argument-reduction loss even at xi=10^9.  cos() is then applied to a
phase in [0,1) reduced to float (rel err ~2^-53).  mpmath cross-check included.  Numerics only; no proof.
"""
import math, statistics
from mpmath import mp, mpf, cos as mpcos, pi as mppi, log as mplog, fabs

# ---------------------------------------------------------------------------
# (0) exact |nu_hat_{2/3}(xi)| for INTEGER xi via exact phase reduction
# ---------------------------------------------------------------------------
def bc_exact_int(xi, J=160):
    """|nu_hat_{2/3}(xi)| = prod_{j} |cos(2 pi {xi (2/3)^j})|, xi a Python int, exact phase reduction."""
    p = 1.0
    pj = 1                      # 3^j tracked; numerator xi*2^j
    num = xi                    # xi * 2^j
    den = 1                     # 3^j
    for j in range(J):
        frac = (num % den) / den if den > 1 else 0.0   # exact {xi (2/3)^j}
        c = abs(math.cos(2 * math.pi * frac))
        p *= c
        if p < 1e-300:
            break
        num *= 2
        den *= 3
        # stop early once the remaining terms are ~1 (phase ~0): xi*(2/3)^j < tol
        if xi * (2.0/3.0)**(j+1) < 1e-10:
            # finish the convergent tail with float (phases tiny, cos~1)
            for jj in range(j+1, J):
                a = 2*math.pi*xi*(2.0/3.0)**jj
                p *= abs(math.cos(a))
                if a < 1e-12:
                    break
            break
    return p

def bc_mp(xi, J=400, prec=120):
    """High-precision cross-check with mpmath (xi may be non-integer)."""
    mp.dps = prec
    x = mpf(xi); lam = mpf(2)/3; P = mpf(1)
    for j in range(J):
        P *= fabs(mpcos(2*mppi*x*lam**j))
        if P < mpf(10)**(-300):
            break
    return P

# ---------------------------------------------------------------------------
# (1) decay over many scales + slope drift
# ---------------------------------------------------------------------------
print("="*72)
print("(1) |nu_hat_{2/3}(xi)| over scales  +  cross-check")
print("="*72)
print(f"{'xi':>14} {'|nu_hat| exact':>16} {'mpmath':>16} {'log10':>10}")
for k in range(1, 10):
    xi = 10**k
    ve = bc_exact_int(xi)
    vm = float(bc_mp(xi))
    print(f"{xi:>14} {ve:>16.6e} {vm:>16.6e} {math.log10(ve):>10.3f}")

# dense logarithmically-spaced INTEGER xi from 10 to 10^15 (exact phase reduction => no fp loss)
import numpy as np
log_lo, log_hi, npts = 1.0, 15.0, 700
xis = sorted(set(int(round(10**t)) for t in np.linspace(log_lo, log_hi, npts)))
xis = [x for x in xis if x >= 10]
data = [(x, bc_exact_int(x)) for x in xis]
LX = np.array([math.log(x) for x,_ in data])
LY = np.array([math.log(y) for _,y in data])

# global power-law fit  log|nu_hat| = c - a*log xi
A = np.vstack([np.ones_like(LX), LX]).T
coef, res, *_ = np.linalg.lstsq(A, LY, rcond=None)
c_glob, slope_glob = coef[0], coef[1]
yhat = A @ coef
ss_res = np.sum((LY-yhat)**2); ss_tot = np.sum((LY-LY.mean())**2)
r2 = 1 - ss_res/ss_tot
print(f"\nGLOBAL power-law fit log|nu_hat| = c - a log|xi|:  a = {-slope_glob:.4f}  (C=e^c={math.exp(c_glob):.3e}),  R^2 = {r2:.4f}")

# SLOPE DRIFT: fit slope in sliding decade windows
print("\nSLOPE DRIFT across decade windows (local exponent a in each window):")
print(f"  {'window (log10 xi)':>22} {'local a':>10} {'npts':>6}")
edges = list(range(1,16))
local_as = []
for lo, hi in zip(edges[:-1], edges[1:]):
    mask = (LX >= lo*math.log(10)-1e-9) & (LX <= hi*math.log(10)+1e-9)
    if mask.sum() >= 3:
        Aw = np.vstack([np.ones(mask.sum()), LX[mask]]).T
        cw = np.linalg.lstsq(Aw, LY[mask], rcond=None)[0]
        local_as.append((lo,hi,-cw[1],int(mask.sum())))
        print(f"  {f'[{lo},{hi}]':>22} {-cw[1]:>10.4f} {int(mask.sum()):>6}")
print("  -> if local a is roughly CONSTANT across windows => genuine power law.")
print("  -> if local a DRIFTS toward 0 as xi grows => only sub-polynomial (log-type) decay.")

# ---------------------------------------------------------------------------
# (2) the subsequence xi_N = (3/2)^N/8 = 3^N / 2^(N+3)  (dyadic rational, EXACT)
#     identity check with the annealed carry product Phi(N)
# ---------------------------------------------------------------------------
print("\n"+"="*72)
print("(2) subsequence xi_N = (3/2)^N/8 ;  identity |nu_hat(xi_N)| = Phi(N)*C")
print("="*72)

def phase_carry(k):
    """exact {(3/2)^k / 4} = (3^k mod 2^(k+2)) / 2^(k+2)   for k>=0."""
    return (pow(3, k) % (1 << (k+2))) / (1 << (k+2))

def Phi(N):
    """annealed carry product prod_{k=0}^{N} |cos(pi {(3/2)^k/4})|  (exp_sum.py object)."""
    p = 1.0
    for k in range(0, N+1):
        p *= abs(math.cos(math.pi * phase_carry(k)))
        if p < 1e-300: break
    return p

def nuhat_xiN(N):
    """|nu_hat_{2/3}((3/2)^N/8)| EXACT.
       xi_N (2/3)^j = 3^(N-j)/2^(N-j+3); arg/(2pi) = (3/2)^(N-j)/4. Product over j>=0 = prod_{k<=N}.
       k>=0 exact via phase_carry; k<0 phases tiny (cos->1), summed to convergence."""
    p = 1.0
    # k = N, N-1, ..., 0
    for k in range(N, -1, -1):
        p *= abs(math.cos(math.pi * phase_carry(k)))
        if p < 1e-300: break
    # k < 0 : (3/2)^k = (2/3)^|k|, phase = pi*(2/3)^m/4
    m = 1
    while True:
        a = math.pi * (2.0/3.0)**m / 4.0
        f = abs(math.cos(a))
        p *= f
        if a < 1e-14:
            break
        m += 1
    return p

print(f"{'N':>5} {'|nu_hat(xi_N)|':>16} {'Phi(N)':>16} {'ratio':>10}")
Ns_id = [5,10,20,40,80,160,320]
for N in Ns_id:
    nu = nuhat_xiN(N); ph = Phi(N)
    print(f"{N:>5} {nu:>16.6e} {ph:>16.6e} {nu/ph if ph>0 else float('nan'):>10.4f}")
print("  -> ratio should be a CONSTANT (the k<0 tail) confirming |nu_hat(xi_N)| = C * Phi(N).")

# ---------------------------------------------------------------------------
# (3) rate of Phi(N) in N  -- THE DISCRIMINATOR
#     xi_N ~ (3/2)^N grows exponentially. So:
#       polynomial-in-xi  |nu_hat|~xi^-a   =>  log Phi(N) ~ -a*log(3/2)*N   (LINEAR in N)
#       logarithmic-in-xi |nu_hat|~(log xi)^-b => log Phi(N) ~ -b*log N     (LINEAR in log N)
# ---------------------------------------------------------------------------
print("\n"+"="*72)
print("(3) rate of Phi(N)=|nu_hat(xi_N)|/C in N  -- DISCRIMINATOR poly-in-xi vs log-in-xi")
print("="*72)
# LOG-SPACE accumulation (no underflow) -> can reach very large N.
# per-term decrement is log|cos(pi {(3/2)^k/4})|.  If the phases {(3/2)^k/4} equidistribute mod 1,
# the running mean -> E_{U~Unif}[log|cos(pi U)|] = integral_0^1 log|cos(pi u)| du = -log 2.
INT_CONST = -math.log(2.0)   # exact value of the integral
# numeric check of the integral constant
from scipy.integrate import quad
val,_ = quad(lambda u: math.log(abs(math.cos(math.pi*u))), 0, 1, limit=200)
print(f"sanity: integral_0^1 log|cos(pi u)| du = {val:.6f}  (exact -log2 = {INT_CONST:.6f})")
print(f"=> IF phases equidistribute: logPhi(N)/N -> -log2, i.e. Phi(N) ~ rho^N with rho=1/2,")
print(f"   and since xi_N=(3/2)^N/8, this is POWER law in xi with a = log2/log(3/2) = {math.log(2)/math.log(1.5):.4f}\n")

Nmax = 30000
logphi = 0.0
running = []        # (N, logPhi(N))
sample_at = set([int(x) for x in np.unique(np.round(np.logspace(1, math.log10(Nmax), 400)).astype(int))])
# incremental EXACT modular tracking of 3^k mod 2^(Nmax+3); frac uses top ~60 bits (double precision)
MOD_BITS = Nmax + 4
mask_full = (1 << MOD_BITS) - 1
a = 1  # 3^0
for k in range(0, Nmax+1):
    b = k + 2
    low = a & ((1 << b) - 1)                 # 3^k mod 2^(k+2)
    frac = (low / (1 << b)) if b <= 60 else ((low >> (b-60)) / (1 << 60))  # {(3/2)^k/4}
    logphi += math.log(abs(math.cos(math.pi * frac)))
    if k in sample_at:
        running.append((k, logphi))
    a = (a * 3) & mask_full
Ns_s = np.array([r[0] for r in running], dtype=float)
LP_s = np.array([r[1] for r in running])

print("running mean decrement logPhi(N)/N (should converge to -log2 = -0.6931 if equidistributed):")
print(f"  {'N':>8} {'logPhi(N)/N':>14} {'implied a=slope/log1.5':>22}")
for N in [100, 1000, 10000, 50000, 100000, 200000]:
    i = int(np.argmin(np.abs(Ns_s-N)))
    mn = LP_s[i]/Ns_s[i]
    print(f"  {int(Ns_s[i]):>8} {mn:>14.5f} {(-mn)/math.log(1.5):>22.4f}")

# Fit A: logPhi ~ alpha - s*N  (power-in-xi)   over the WHOLE range
Aa = np.vstack([np.ones_like(Ns_s), Ns_s]).T
ca = np.linalg.lstsq(Aa, LP_s, rcond=None)[0]
yha = Aa@ca; r2a = 1-np.sum((LP_s-yha)**2)/np.sum((LP_s-LP_s.mean())**2)
a_from_N = -ca[1]/math.log(1.5)
# Fit B: logPhi ~ beta - b*log N  (log-in-xi)
LN_s = np.log(Ns_s)
Ab = np.vstack([np.ones_like(LN_s), LN_s]).T
cb = np.linalg.lstsq(Ab, LP_s, rcond=None)[0]
yhb = Ab@cb; r2b = 1-np.sum((LP_s-yhb)**2)/np.sum((LP_s-LP_s.mean())**2)
print(f"\nFit A  logPhi(N) = alpha - s*N      : s = {-ca[1]:.5f}/term  -> a = s/log(3/2) = {a_from_N:.4f},  R^2 = {r2a:.6f}")
print(f"Fit B  logPhi(N) = beta  - b*log N  : b = {-cb[1]:.3f},                              R^2 = {r2b:.6f}")
print(f"Better global fit over N=10..{Nmax}: {'A => POWER law in xi' if r2a>r2b else 'B => LOGARITHMIC in xi'}  (R^2 A={r2a:.6f} vs B={r2b:.6f})")

# local slope drift (does -dlogPhi/dN stay constant ~log2, or drift to 0?)
print("\nLOCAL slope -dlogPhi/dN across N windows (const ~0.693 => power law; ->0 => log):")
print(f"  {'N window':>16} {'-dlogPhi/dN':>14} {'implied a':>10}")
wins = [(10,100),(100,1000),(1000,10000),(10000,50000),(50000,100000),(100000,200000)]
for lo,hi in wins:
    m = (Ns_s>=lo)&(Ns_s<=hi)
    if m.sum()<5: continue
    sA = np.polyfit(Ns_s[m], LP_s[m], 1)[0]
    print(f"  {f'[{lo},{hi}]':>16} {-sA:>14.6f} {-sA/math.log(1.5):>10.4f}")

print("\nDONE.")
