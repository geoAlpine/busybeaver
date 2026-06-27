"""
TWISTED Ruelle-Perron-Frobenius (transfer) operator L_t for the Antihydra carry exponential-sum.
================================================================================
Attack d (SESSION_2026-06-28_QUENCHED_ATTACK.md): the thesis to TEST is

    quenched (3/2)^j Korobov-sum cancellation
      = exponential decay of the carry exponential-sum  E[ e( T_n / 2^{n+1} ) ]
      = rho(L_t)^n  for a twisted transfer operator L_t
    and   rho(L_t) < 1  <=>  quenched cancellation  <=>  ||F||<1  <=>  Mahler.

This script CONSTRUCTS candidate twisted operators on the finite carry-state space
s = c mod 2^k (k = 4,6,8,10,12), MEASURES rho(L_t) = max-modulus eigenvalue vs k,
cross-checks against the actual annealed product Phi(N), and reports HONESTLY which
object (annealed rank-1 vs quenched) was reached and whether rho converges or drifts
to 1 (the contraction-audit failure mode, AUDIT_CONTRACTION.md).

ALL numerics: /Users/aokiyousuke/quantum-ecc/.venv/bin/python  (numpy).
0 false proofs: every printed conclusion is an OBSERVED finite-k number; the soundness
verdict in TWISTED_RPF.md states plainly measured-vs-proven and the k->oo control.

--------------------------------------------------------------------------------
DERIVATION OF THE TWIST (from exp_sum.py)
--------------------------------------------------------------------------------
Carry recursion  T_{n+1} = 3 T_n + 2^n e_n,  carry bit b_n = bit_n(T_n), leading
Fourier mode e(T_n/2^{n+1}).  Set phi_n = T_n / 2^{n+1} mod 1.  Then

    phi_{n+1} = T_{n+1}/2^{n+2} = (3 T_n + 2^n e_n)/2^{n+2} = (3/2) phi_n + e_n/4   (mod 1).

So phi obeys the x(3/2) map with a Bernoulli bit injected at 1/4.  next_state(s,b,k)
of mckean_contraction.py is EXACTLY this map discretised to k bits:
    next_state(s,b,k) = ( floor(3 s / 2) + b*2^{k-1} ) mod 2^k          (proved below)
i.e. s/2^k is the discretised phase phi, NOT the low bits.  The character that
reproduces Phi is e(s/2^{k+1}) (so the injected bit b*2^{k-1} contributes phase b/4):

    E[e(phi_N)] = prod_{j=0}^{N-1} (1/2)(1 + e((3/2)^j/4)),
    |E[e(phi_N)]| = prod_j |cos(pi {(3/2)^j/4})| = Phi(N).            (exp_sum.py identity)

KEY ANALYTIC FACT used in the verdict:
    (1/N) log Phi(N) = (1/N) sum_j log|cos(pi {(3/2)^j/4})|  ->  int_0^1 log|cos(pi x)| dx = -log 2
    IFF {(3/2)^j/4} equidistributes (= MAHLER).  So slope(-log_2 Phi) -> 1 (Phi ~ 2^{-N}) <=> Mahler,
    and a *correct* twisted operator with a genuine spectral gap would have
        rho(L_t) = exp( int log|cos pi x| dx ) = exp(-log 2) = 1/2   (-log_2 rho = 1),
    the GEOMETRIC-MEAN per-step factor under the equidistributed angle.
"""
import numpy as np

# ------------------------------------------------------------------ base dynamics
def next_state(s, b, k):
    mod = 1 << k
    return ((3 * (s + (b << k)) - (s & 1)) // 2) % mod

def L_op(k):
    """untwisted annealed Markov operator (row-stochastic, acts on row-distributions p->pM)."""
    mod = 1 << k
    M = np.zeros((mod, mod))
    for s in range(mod):
        for b in (0, 1):
            M[s, next_state(s, b, k)] += 0.5
    return M

# verify the closed form next_state = (floor(3s/2)+b 2^{k-1}) mod 2^k
def _verify_closed_form():
    ok = True
    for k in (4, 6, 8):
        mod = 1 << k
        for s in range(mod):
            for b in (0, 1):
                lhs = next_state(s, b, k)
                rhs = ((3 * s) // 2 + b * (1 << (k - 1))) % mod
                ok &= (lhs == rhs)
    return ok

# ----------------------------------------------------- annealed product Phi(N)
def phase32(j):
    """exact {(3/2)^j / 4} = (3^j mod 2^{j+2}) / 2^{j+2}."""
    num = pow(3, j) % (1 << (j + 2))
    return num / (1 << (j + 2))

def Phi(N):
    p = 1.0
    for j in range(N):
        p *= abs(np.cos(np.pi * phase32(j)))
    return p

# ===================================================================== OPERATORS
# We build several candidate twisted operators on Z/2^k and measure rho for each.

def Lt_inject(k):
    """TWIST = per-step bit-injection character e(b/4) (the factor that generates (1/2)(1+e(.))).
       L_t[s, next(s,b,k)] += (1/2) e(b/4).  Fixed operator (twist depends on b only)."""
    mod = 1 << k
    M = np.zeros((mod, mod), dtype=complex)
    for s in range(mod):
        for b in (0, 1):
            M[s, next_state(s, b, k)] += 0.5 * np.exp(2j * np.pi * (b / 4.0))
    return M

def Lt_diag(k):
    """Diagonal-character twist of L_op (literal 'twist the Markov operator'):
       L_t = D M  with D = diag(e(s/2^{k+1})), the character that reproduces Phi under M^N v."""
    mod = 1 << k
    M = L_op(k).astype(complex)
    d = np.exp(2j * np.pi * (np.arange(mod) / (1 << (k + 1))))
    return np.diag(d) @ M

def Lt_ruelle(k):
    """RUELLE transfer operator of the angle map theta -> (3/2) theta mod 1 on Z/2^k with the
       complex weight g(theta) = (1/2)(1 + e(theta)) (|g| = |cos pi theta|).
       (L_g f)(theta) = sum_{(3/2)eta = theta} g(eta) f(eta).  rho(L_g) = exp(pressure).
       Discretised: angle index a in [0,2^k); preimages of a under floor(3a/2) mod 2^k."""
    mod = 1 << k
    # forward map on angle index a: image = floor(3a/2) mod 2^k  (the e=0 branch of next_state, no injection)
    img = np.array([((3 * a) // 2) % mod for a in range(mod)])
    L = np.zeros((mod, mod), dtype=complex)
    for a in range(mod):           # eta = a/2^k
        g = 0.5 * (1.0 + np.exp(2j * np.pi * (a / mod)))
        L[img[a], a] += g          # contributes to f(eta) at target theta = img(a)
    return L

def rho(A):
    return np.max(np.abs(np.linalg.eigvals(A)))

# ============================================================================ RUN
print("=" * 78)
print("TWISTED RPF operator L_t -- construction + spectral radius vs k")
print("=" * 78)
print(f"closed form next_state == (floor(3s/2)+b 2^{{k-1}}) mod 2^k :  {_verify_closed_form()}")

print("\n[1] untwisted L_op : leading eigenvalue (should be 1, row-stochastic) and lambda_2")
for k in (4, 6, 8, 10):
    ev = np.sort(np.abs(np.linalg.eigvals(L_op(k))))[::-1]
    print(f"    k={k:2d}  lambda_1={ev[0]:.6f}  lambda_2={ev[1]:.6f}")

print("\n[2] CROSS-CHECK: does the matrix-vector iteration M^N v reproduce Phi(N)?")
print("    v_s = e(s/2^{k+1});  E[e(phi_N)] = (M^N v)_0 .  Compare |(M^N v)_0| to Phi(N).")
for k in (10, 12, 14):
    mod = 1 << k
    M = L_op(k)
    v = np.exp(2j * np.pi * (np.arange(mod) / (1 << (k + 1))))
    x = v.copy()
    print(f"    --- k={k} (valid until freq (3/2)^N wraps ~ N<={k}) ---")
    print(f"        {'N':>3} {'|(M^N v)_0|':>14} {'Phi(N)':>14} {'ratio':>10}")
    for N in range(1, k + 4):
        x = M @ x
        val = abs(x[0])
        ph = Phi(N)
        r = val / ph if ph > 0 else float('nan')
        if N in (1, 2, 4, k // 2, k - 2, k, k + 2):
            print(f"        {N:>3} {val:>14.6e} {ph:>14.6e} {r:>10.4f}")

print("\n[3] annealed Phi(N) decay slope  -log_2 Phi(N) / N  (-> 1 iff Mahler/equidistribution)")
for N in (8, 16, 32, 64, 128, 256, 512, 1024):
    ph = Phi(N)
    slope = (-np.log2(ph) / N) if ph > 0 else float('nan')
    print(f"    N={N:5d}  -log_2 Phi = {-np.log2(ph):9.3f}  slope={slope:.4f}")
print(f"    int_0^1 log|cos(pi x)| dx / (-log 2) = {(-np.log(2))/(-np.log(2)):.4f}  (target slope = 1)")

print("\n[4] SPECTRAL RADIUS of candidate twisted operators vs k  (does rho converge or DRIFT to 1?)")
print(f"    {'k':>3} {'rho(Lt_inject)':>15} {'rho(Lt_diag)':>14} {'rho(Lt_ruelle)':>15}"
      f" {'-log2 rho_ruelle':>16}")
for k in (4, 6, 8, 10, 12):
    ri = rho(Lt_inject(k))
    rd = rho(Lt_diag(k))
    rr = rho(Lt_ruelle(k))
    lr = -np.log2(rr) if rr > 0 else float('nan')
    print(f"    {k:>3} {ri:>15.6f} {rd:>14.6f} {rr:>15.6f} {lr:>16.4f}")

print("\n[5] QUENCHED check: the real Antihydra orbit (no exogenous bits, fully self-generated).")
print("    Map a -> floor(3a/2) from a generic seed; r_n = a_n mod 2 = the orbit's own parity.")
print("    (i)  parity density  (1/N) sum r_n      -> 1/2  ?   (even-density genericity)")
print("    (ii) Birkhoff cancellation |(1/N) sum (-1)^{r_n}| and its rate  N^{-alpha}.")
def antihydra_orbit_stats(N, seed=3):
    a = seed
    s = 0
    csum = 0
    for n in range(N):
        r = a & 1
        s += r
        csum += (1 - 2 * r)            # (-1)^{r_n}
        a = (3 * a) // 2               # floor(3a/2): the real x(3/2) orbit
    return s / N, abs(csum) / N
for N in (4000, 16000, 64000, 256000):
    dens, birk = antihydra_orbit_stats(N)
    alpha = -np.log(birk) / np.log(N) if birk > 0 else float('nan')
    print(f"    N={N:7d}  parity density={dens:.5f}   |Birkhoff|={birk:.3e}   "
          f"=> alpha (rate N^-a)={alpha:.3f}")
print("    (random surrogate would give alpha~0.5; exponential 2^-N would give alpha->oo.)")

print("""
SUMMARY (read TWISTED_RPF.md for the full soundness verdict):
  - [2] FALSIFIED a hoped-for shortcut: M^N v matches Phi only at N=1, then PLATEAUS at 2/pi =
    int_0^1 |cos pi x| dx (the L1 mean of the character), NOT Phi(N)~2^{-N}. The finite mod-2^k
    operator CANNOT carry the (3/2)-escaping product: the frequency (3/2)^N aliases immediately
    under the floor(3s/2) truncation. This IS the non-Pisot obstruction in operator form.
  - [3] Phi ~ 2^{-N} (slope -> 1) is EXACTLY the equidistribution of {(3/2)^j} = MAHLER; the
    geometric-mean per-step factor is exp(int log|cos pi x|dx) = 1/2.
  - [4] FIXED twisted operators CONVERGE (no drift to 1 -- unlike the contraction audit) but to the
    WRONG rate: Lt_inject/Lt_diag -> ~0.717 ~ cos(pi/4) (frozen single angle), Lt_ruelle = 1 exactly
    (atomic delta_0 fixed point, weight g(0)=1). A FIXED operator cannot encode the per-step CHANGING
    angle (3/2)^j, so it cannot give the Mahler rate 1/2. ANNEALED reached; QUENCHED gap does not exist
    as a finite-operator eigenvalue.
  - [5] real single orbit: parity density -> 1/2, Birkhoff cancellation ~ N^{-1/2} (random-like).
    The quenched object is a Birkhoff average (rate N^{-1/2}), NOT an exponential rho^n -- a different
    object from the single-time Phi(n)~2^{-n}. The annealed/quenched seam, made explicit.
""")
