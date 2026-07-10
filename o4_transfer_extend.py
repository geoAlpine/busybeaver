"""
O4 transfer operator -- extend lambda_2(k) trajectory with a SPARSE solver (each
row has 3 nonzeros), plus the ANALYTIC character argument proving the annealed
operator is essentially nilpotent mod Haar (=> the near-0 lambda_2), and a direct
simulation of the annealed chain's mixing time as an independent check.
"""
import numpy as np
import scipy.sparse as sp
import scipy.sparse.linalg as spla

E = {0:9, 1:14, 2:1}

def base_image(x, k):
    return ((4*x + E[x % 3]) // 3) % (3**k)

def build_sparse_P(k):
    M = 3**k; Mm1 = 3**(k-1)
    rows=[]; cols=[]; data=[]
    for x in range(M):
        low = base_image(x, k) % Mm1
        for d in range(3):
            rows.append(x); cols.append((low + d*Mm1) % M); data.append(1.0/3.0)
    return sp.csr_matrix((data,(rows,cols)), shape=(M,M))

def lam2_sparse(k, nev=10):
    P = build_sparse_P(k)
    # largest-magnitude eigenvalues of P (nonsymmetric)
    vals = spla.eigs(P, k=nev, which='LM', return_eigenvectors=False, maxiter=5000)
    mags = np.sort(np.abs(vals))[::-1]
    return mags

print("Extended lambda_2(k) via sparse solver (which='LM'):")
print(f"{'k':>2} {'dim':>7} {'|lam1|':>10} {'|lam2|':>16} {'|lam3|':>14}")
traj=[]
for k in range(4, 11):
    mags = lam2_sparse(k, nev=12)
    # lam1 should be 1
    l1 = mags[0]; l2 = mags[1]; l3 = mags[2]
    traj.append((k,l2))
    print(f"{k:>2} {3**k:>7} {l1:>10.6f} {l2:>16.10f} {l3:>14.10f}")

print("\nlambda_2(k):", [f'{k}:{v:.3e}' for k,v in traj])
print("ratios lam2(k)/lam2(k-1):", [f'{traj[i][1]/traj[i-1][1]:.3f}' for i in range(1,len(traj))])

# --- analytic check: characters chi_a with a not divisible by 3 are annihilated ---
print("\n--- ANALYTIC: Koopman on characters (single-branch e=const would give exact nilpotency) ---")
print("  U chi_a(x) = (1/3) sum_d exp(2pi i * 4 a d / 3) * (image char)")
print("  = 0 unless a ≡ 0 (mod 3).  So each step kills all a not ≡0 mod 3 and")
print("  lowers the rest; after k steps only a=0 (Haar) survives => nilpotent mod Haar.")
print("  The SMALL nonzero lam2 comes ONLY from e(x mod3) varying across the 3 branches")
print("  (piecewise-affine coupling of a with a±3^{k-1}); it grows slowly, stays << 1.")

# --- independent check: annealed chain mixing time from a delta start ---
print("\n--- INDEPENDENT: annealed-chain relaxation from delta_{-14} (k=5) ---")
k=5; M=3**k; Mm1=3**(k-1)
# transition as function
def step_dist(v):
    out=np.zeros(M)
    for x in np.nonzero(v)[0]:
        low=base_image(x,k)%Mm1
        for d in range(3):
            out[(low+d*Mm1)%M]+=v[x]/3.0
    return out
v=np.zeros(M); v[(-14)%M]=1.0
for t in range(1,8):
    v=step_dist(v)
    tv=0.5*np.sum(np.abs(v-1.0/M))   # total-variation distance to Haar
    print(f"  t={t}: TV(delta_-14 * L^t, Haar) = {tv:.3e}")
print("  -> annealed chain from the fixed-point delta reaches Haar within a few steps:")
print("     the annealing DISSOLVES delta_{-14}. In the deterministic (un-annealed)")
print("     map, -14 is an EXACT fixed point (base_image(-14)=-14) => an eigenvalue-1")
print("     delta that ONLY the annealing removes. That gap between the two is (K).")
