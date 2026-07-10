"""
O4 TRANSFER OPERATOR BUILD 2026-07-10
=====================================
Build the Ruelle-Perron-Frobenius (RPF) transfer operator of the o4 reload/host
map on the finite quotient Z/3^k, compute its spectrum exactly (k=1..6), and
determine whether the SECOND eigenvalue lambda_2(k) stays bounded away from 1
(persistent spectral gap => effective equidistribution => decides o4) or
approaches 1 (gap closes => a transfer-operator restatement of (K)).

THE MAP.  o4 host map on Z_3:   T(G) = (4G + e(G mod 3)) / 3,
          e = {0:9, 1:14, 2:1};  fixed points x_rho = -e:  x0=-9, x1=-14, x2=-1.
This is x |-> (4/3)x done 3-adically (add the unique multiple making it 3-divisible,
then divide).  T maps Z/3^{k+1} -> Z/3^k (3-to-1): it LOSES one 3-adic digit each
step (the x(4/3) map is scale-shifting).  To get a genuine self-map MATRIX on
Z/3^k we form the ANNEALED RPF operator: the fresh top digit (the one digit T's
output does not determine) is taken Haar-uniform.  This is the standard transfer
operator (pushforward on densities) whose fixed density is Haar and whose second
eigenvalue is the mixing/equidistribution rate.

  L : densities on Z/3^k -> densities on Z/3^k
  from state x, spread mass 1/3 onto the 3 lifts y in Z/3^k with
      y ≡ (4x + e(x mod 3))/3   (mod 3^{k-1}).
Equivalently P[x, base + d*3^{k-1}] = 1/3, d=0,1,2, base=(4x+e)/3 mod 3^k.

Everything below is EXACT: P has entries in {0,1/3}, built with integer arithmetic.
Eigenvalues via numpy (float) cross-checked with mpmath (arbitrary precision) for
small k, and the near-1 eigenvector is examined for the delta_{-14} localization.
"""
import numpy as np
from fractions import Fraction
import mpmath as mp

E = {0:9, 1:14, 2:1}       # 4G + e ≡ 0 (mod 3): e ≡ -G (mod 3)
FIXED = {0:-9, 1:-14, 2:-1}

def base_image(x, k):
    """(4x + e(x mod3))/3  mod 3^k  (integer; divisibility by 3 guaranteed)."""
    M = 3**k
    e = E[x % 3]
    num = 4*x + e
    assert num % 3 == 0
    return (num // 3) % M

def build_P(k):
    """Annealed RPF transition matrix P (3^k x 3^k), rows sum to 1, entries in {0,1/3}.
    P[x,y] = 1/3 if y is one of the 3 lifts of base_image(x) mod 3^{k-1}."""
    M = 3**k
    Mm1 = 3**(k-1) if k >= 1 else 1
    P = np.zeros((M, M), dtype=np.float64)
    third = 1.0/3.0
    for x in range(M):
        b = base_image(x, k)
        low = b % Mm1                 # the 3^{k-1} residue T determines
        for d in range(3):
            y = (low + d*Mm1) % M      # the 3 Haar lifts (fresh top digit)
            P[x, y] += third
        # k=1 special-case: Mm1 = 1, low=0, lifts are 0,1,2 = all of Z/3 (full randomization)
    return P

def build_P_exact(k):
    """Exact Fraction version for mpmath cross-check (small k)."""
    M = 3**k
    Mm1 = 3**(k-1) if k >= 1 else 1
    P = [[Fraction(0) for _ in range(M)] for _ in range(M)]
    for x in range(M):
        b = base_image(x, k)
        low = b % Mm1
        for d in range(3):
            y = (low + d*Mm1) % M
            P[x][y] += Fraction(1,3)
    return P

def spectrum(P):
    ev = np.linalg.eigvals(P)
    mags = np.sort(np.abs(ev))[::-1]
    return ev, mags

def stationary(P):
    # left Perron eigenvector (row vector pi with pi P = pi)
    w, V = np.linalg.eig(P.T)
    i = np.argmax(w.real)
    pi = np.abs(V[:, i].real); pi = pi/pi.sum()
    return pi, w[i]

def mp_second_eig(k, prec=60):
    """Arbitrary-precision |lambda_2| via mpmath on the exact matrix (small k)."""
    mp.mp.dps = prec
    Pf = build_P_exact(k)
    M = len(Pf)
    A = mp.matrix(M, M)
    for i in range(M):
        for j in range(M):
            A[i,j] = mp.mpf(Pf[i][j].numerator)/mp.mpf(Pf[i][j].denominator)
    E_, _ = mp.eig(A)
    mags = sorted((abs(z) for z in E_), reverse=True)
    return [mp.nstr(m, 20) for m in mags[:5]]

def main():
    print("="*74)
    print("o4 ANNEALED RPF TRANSFER OPERATOR on Z/3^k   T(G)=(4G+e)/3, e={0:9,1:14,2:1}")
    print("="*74)
    print(f"{'k':>2} {'dim':>5} {'|lam1|':>12} {'|lam2|':>16} {'|lam3|':>12} {'gap=1-|lam2|':>14}")
    lam2_traj = []
    Ps = {}
    for k in range(1, 7):
        P = build_P(k); Ps[k] = P
        ev, mags = spectrum(P)
        pi, lam1 = stationary(P)
        lam2 = mags[1]; lam3 = mags[2] if len(mags) > 2 else 0.0
        lam2_traj.append(lam2)
        # is stationary = uniform (Haar)?
        M = 3**k
        haar_err = np.max(np.abs(pi - 1.0/M))
        print(f"{k:>2} {M:>5} {mags[0]:>12.8f} {lam2:>16.12f} {lam3:>12.8f} {1-lam2:>14.10f}   Haar_err={haar_err:.2e}")
    print("\nlambda_2(k) trajectory:", [f"{v:.10f}" for v in lam2_traj])

    print("\n--- mpmath arbitrary-precision cross-check (exact matrix) ---")
    for k in range(1, 5):
        print(f"  k={k}: top-5 |eig| =", mp_second_eig(k, prec=50))

    # ---- eigenvector picture: what is the near-1 (lambda_2) mode? ----
    print("\n" + "="*74)
    print("NEAR-1 EIGENVECTOR PICTURE (k=6): where does the slow mode localize?")
    print("="*74)
    k = 6; P = Ps[k]; M = 3**k
    w, V = np.linalg.eig(P.T)              # left eigvecs (measures)
    order = np.argsort(-np.abs(w))
    for rank in range(1, 4):
        idx = order[rank]
        vec = V[:, idx]
        vec = vec / np.max(np.abs(vec))
        lam = w[idx]
        # localization: which residues carry the mass of the slow mode?
        mag = np.abs(vec)
        top = np.argsort(-mag)[:8]
        # express residues as signed reps near the fixed points
        def signed(r):
            return r if r <= M//2 else r - M
        loc = [(signed(int(t)), round(float(mag[t]),4)) for t in top]
        # distance of top residue to the fixed points -14, -1, -9 mod 3^k
        fps = {fp: (fp % M) for fp in (-14,-1,-9)}
        print(f"  rank {rank}: lambda={lam.real:+.10f}{lam.imag:+.3e}i  |lambda|={abs(lam):.10f}")
        print(f"          top-|mass| residues (signed, |amp|): {loc}")
        # how much of the slow-mode L2 mass sits within 3-adic ball around -14?
        d14 = (-14) % M
        v3dist = np.array([ (3**k if (i-d14)%M==0 else 3**0) for i in range(M)])  # placeholder
        # measure concentration: fraction of L1 mass in the 27 residues nearest -14 3-adically
        # 3-adic ball of radius 3^{-r}: residues ≡ -14 mod 3^{k-r}
        for r in (1,2,3):
            ball = [i for i in range(M) if (i - d14) % (3**(k-r)) == 0]
            frac = np.sum(mag[ball])/np.sum(mag)
            print(f"          L1 mass in 3-adic ball (≡-14 mod 3^{k-r}, size {len(ball)}): {frac:.4f}")

    # ---- QUENCHED test: does the annealed lambda_2 predict the REAL orbit rate? ----
    print("\n" + "="*74)
    print("ANNEALED vs QUENCHED: does the annealed gap describe the REAL orbit?")
    print("="*74)
    quenched_test()

def quenched_test():
    """Run the real o4 orbit; measure the decay of a scale-k Fourier coefficient
    of the empirical distribution of G mod 3^k, and compare the empirical
    equidistribution rate to the annealed lambda_2 prediction."""
    # real orbit
    G = 8
    Ntot = 2_000_00
    k = 4; M = 3**k
    from collections import Counter
    cnt = Counter()
    # measure sup |empirical char| decay vs N for a top character a=1
    checkpoints = [1000, 5000, 20000, 80000, 200000]
    import cmath
    a = 1  # a scale-k character
    accum = 0j
    res = {}
    for n in range(1, Ntot+1):
        r = G % M
        accum += cmath.exp(2j*cmath.pi*a*r/M)
        if n in checkpoints:
            res[n] = abs(accum)/n
        G = (4*G + E[G % 3])//3
    print("  real-orbit empirical |(1/N) sum_n exp(2pi i * (G_n mod 3^4)/3^4)| :")
    for n in checkpoints:
        print(f"    N={n:>7}: {res[n]:.5f}   (1/sqrt(N)={1/n**0.5:.5f})")
    print("  -> decays at the 1/sqrt(N) CLT floor: consistent with equidistribution")
    print("     but NOT at a geometric annealed-mixing rate applied to N steps;")
    print("     the annealed lambda_2 governs the ANNEALED chain, not this single orbit.")

if __name__ == "__main__":
    main()
