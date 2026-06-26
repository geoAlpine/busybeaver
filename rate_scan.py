"""Phase 2 (program): is the effective genericity convergence RATE mu-uniform or mu-dependent?
The trap/no-trap boundary is the curve mu=2; past it the genericity WALL is uniform. Question now:
is the *rate* at which a single escaping orbit LOOKS generic also mu-uniform, or does it depend on
mu? A mu-dependent rate would be a new handle.

THEORETICAL PREDICTION. The renewal map's per-step expansion (Lyapunov exponent in log scale) is
log mu: c_n ~ C mu^n, so each step contributes ~log2(mu) fresh binary bits. Heuristic: an orbit that
reveals more bits per step should equidistribute its low residues FASTER. Predict: convergence rate
of the mod-p residue frequencies improves with log mu (faster for larger mu).

WHAT WE MEASURE (honest: empirical single-orbit discrepancy, a.e.-style reconnaissance -- this does
NOT touch the single-orbit genericity PROOF, which stays open; it asks whether the wall is one
object or a mu-family of objects).
  * Run the genuine integer orbit c -> floor(a c / p) from a seed above the trap threshold.
  * D_N(mu) = max_r | (1/N) #{n<N : c_n = r mod p} - 1/p |   (mod-p residue discrepancy).
  * Scale: sqrt(N) * D_N -- if ~const in N, CLT-rate; compare the CONSTANT across mu.
  * Correlate the constant with log2(mu) to test the prediction.
Averaged over several seeds to suppress single-orbit noise.
"""
from math import gcd, log2, sqrt
from collections import Counter

def disc_modp(a, p, seed, N):
    """max-over-residues discrepancy of c_n mod p along the real integer orbit, at several cutoffs."""
    c = seed
    cnt = Counter()
    cuts = [N//4, N//2, N]
    out = {}
    for n in range(1, N+1):
        cnt[c % p] += 1
        if n in cuts:
            d = max(abs(cnt[r]/n - 1.0/p) for r in range(p))
            out[n] = d
        c = (a*c)//p
    return out, cuts

def trap_threshold(a, p):
    return p/(a-p)   # seeds strictly above 1/(mu-1) escape

print("="*82)
print("Rate scan: does single-orbit genericity converge mu-uniformly?  (trap-free region mu>2)")
print("="*82)

# trap-free members across several p
members = []
for p in [2,3,5,7]:
    for a in range(2*p+1, 3*p+2):
        if gcd(a,p)==1:
            members.append((p,a))
# keep a spread of mu
members = sorted(set(members), key=lambda pa: pa[1]/pa[0])

N = 16000
seeds_base = [11, 17, 23, 31, 41]   # all above any threshold here (mu>2 => threshold<1)
print(f"\nN={N}, averaged over seeds {seeds_base}.  Haar discrepancy target -> 0.")
print(f"{'(p,a)':>8} {'mu':>7} {'log2(mu)':>9} {'sqrtN*D_N':>10} {'D_(N/4)':>9} {'D_(N/2)':>9} {'D_N':>9} {'~exponent':>10}")
rows=[]
for (p,a) in members:
    mu = a/p
    accD = {1:[],2:[],3:[]}  # by cut index
    for s in seeds_base:
        out, cuts = disc_modp(a,p,s,N)
        for i,cN in enumerate(cuts):
            accD[i+1].append(out[cN])
    Dq = sum(accD[1])/len(accD[1]); Dh = sum(accD[2])/len(accD[2]); Df = sum(accD[3])/len(accD[3])
    # empirical exponent: D_N ~ N^{-beta}; fit between N/4 and N
    beta = (log2(Dq) - log2(Df)) / (log2(N) - log2(N//4)) if Df>0 and Dq>0 else float('nan')
    sND = sqrt(N)*Df
    print(f"{str((p,a)):>8} {a}/{p:<5} {log2(mu):9.3f} {sND:10.3f} {Dq:9.4f} {Dh:9.4f} {Df:9.4f} {beta:10.3f}")
    rows.append((mu, log2(mu), sND, beta))

# correlation of sqrtN*D_N constant with log2(mu)
import statistics
xs=[r[1] for r in rows]; ys=[r[2] for r in rows]
mx=statistics.mean(xs); my=statistics.mean(ys)
cov=sum((x-mx)*(y-my) for x,y in zip(xs,ys))/len(xs)
sx=statistics.pstdev(xs); sy=statistics.pstdev(ys)
corr = cov/(sx*sy) if sx>0 and sy>0 else float('nan')
betas=[r[3] for r in rows if r[3]==r[3]]
print("\n--- analysis ---")
print(f"empirical exponent beta (D_N ~ N^-beta): mean={statistics.mean(betas):.3f} "
      f"(CLT/sqrt-N law => 0.5), spread=[{min(betas):.3f},{max(betas):.3f}]")
print(f"corr( log2(mu), sqrtN*D_N constant ) = {corr:+.3f}")
print("\nReading:")
print(" * if beta ~ 0.5 for all mu and sqrtN*D_N constant is mu-INDEPENDENT (corr ~ 0): the rate is")
print("   mu-uniform -> the wall is ONE object, same convergence law for every family member.")
print(" * if sqrtN*D_N DECREASES with log2(mu) (corr < 0): larger mu equidistributes FASTER (more")
print("   fresh bits/step) -> a mu-dependent rate = a NEW HANDLE (the prediction); the family is")
print("   graded by expansion speed even though the proof-difficulty wall is shared.")
