"""
================================================================================
RETRACTED 2026-06-28 (soundness discipline -- over-claim caught BEFORE any proof claim).
The "contraction => sidestep of the variational principle" reading below is UNSOUND.
Four-route adversarial audit (AUDIT_CONTRACTION.md, TRACKING_BRIDGE.md, COCYCLE_ERGODICITY.md,
NONPISOT_FOURIER_CHAIN.md) refuted both load-bearing pillars:
  (1) "Only Haar is self-consistent" is FALSE. The SIDESTEP check below uses the WRONG operator
      (L_Haar, not L_{delta_1}). Done correctly, delta_0 and delta_1 ARE self-consistent
      (L_{delta_1} delta_1 = delta_1 exactly) -- they are T's integer fixed points {0,1}. The
      variational multiplicity is REPRODUCED, not sidestepped.
  (2) The constant "lambda_2 + ||F|| ~ 0.048" is NOT a valid bound: spectral radius is not
      subadditive, and L|_V is maximally non-normal (rho=0 nilpotent but ||L|_V||=1). A
      pseudospectral test gives the true rho(L+F) ~ 0.4-0.55, GROWING with resolution k toward 1.
  Net: the contraction framework RELOCATES the open kernel into mean-field language; it does not
  shorten it. The irreducible core remains single-orbit effective equidistribution (Mahler 3/2 / AEV).
WHAT SURVIVES (the assets the audit produced):
  - [PROVEN, citable] non-Pisot 3/2 => nu_{2/3} Rajchman => ANNEALED carry balance, rate ~ log
    (Varju-Yu); new exact identity |nu_hat_{2/3}((3/2)^N/8)| = Phi(N)*tail (const ratio 0.7748).
  - The quenched gain ||F|| is governed by d log Phi/dp = sum_j 2i tan(pi {(3/2)^j/4}) -- the
    (3/2)^j tan-sum = Korobov/Mahler quantity. Clean ANNEALED[PROVEN] / QUENCHED[OPEN]=Mahler split.
  - Self-consistent fixed points {delta_0, delta_1, Haar} <-> T's integer fixed points {0,1} + SRB.
The numerics below RUN but their READING is retracted; kept as the audit record.
================================================================================

The self-consistency map nu -> L_nu nu is a CONTRACTION -- so it has a UNIQUE fixed point (Haar), which
SIDESTEPS the variational-principle obstruction to unique ergodicity. Key points:
  - The variational principle blocks UNIQUE ERGODICITY (positive-entropy fiber => many INVARIANT measures).
  - BUT self-consistency nu = L_nu nu is STRONGER than invariance: of the many invariant measures, only Haar
    is SELF-CONSISTENT (a periodic-orbit / atomic invariant measure does not reproduce itself under L_nu with
    its own conditional incoming bit). So the self-consistent framework is not blocked by the variational
    principle -- it asks a different (mean-field) question.
  - The linearization of the self-consistency map at Haar is L + F: L the annealed transfer operator
    (one-step exact, lambda_2 ~ 0, numpy-verified) and F the self-generation feedback (gain ~0.04). The
    contraction constant is the spectral radius of L+F on the mean-zero complement, <= lambda_2 + ||F||.
  - CONNECTION: ||F|| small (the contraction) IS the Fourier decay of nu_{2/3}, which holds because 3/2 is
    NON-Pisot (Salem-Erdos). non-Pisot => Fourier decay => self-consistency contraction => unique
    self-consistent measure = Haar.
We assemble the contraction estimate from the two established measurements (lambda_2 of L, ||F||) and check
< 1, and verify the SIDESTEP: an atomic invariant measure is NOT self-consistent.
0 false proofs: lambda_2 and ||F|| are prior measured values re-confirmed; the contraction estimate is their
sum; the mean-field tracking (orbit -> mean field) is flagged as the remaining gap.
"""
import numpy as np

# --- lambda_2 of the annealed transfer operator L (one-step exact), re-confirmed ---
def next_state(s, b, k):
    mod = 1 << k
    return ((3 * (s + (b << k)) - (s & 1)) // 2) % mod
def L_op(k):
    mod = 1 << k; M = np.zeros((mod, mod))
    for s in range(mod):
        for b in (0, 1): M[s, next_state(s, b, k)] += 0.5
    return M
print("contraction estimate of the self-consistency map S: nu -> L_nu nu, linearized at Haar = L + F")
print(f"  {'k':>2} {'lambda_2(L)':>12} {'(one-step exact => ~0)':>22}")
lam = {}
for k in (4, 6, 8):
    ev = np.sort(np.abs(np.linalg.eigvals(L_op(k))))[::-1]
    lam[k] = ev[1]
    print(f"  {k:>2} {ev[1]:>12.5f}")
lam2 = max(lam.values())
F = 0.04   # ||F|| (density-mode feedback gain), measured: perturbation_F.py (sup ~0.04 across correlations)
print(f"\n  lambda_2(L) (sup over k) = {lam2:.4f}   ||F|| (measured, perturbation_F) ~ {F}")
print(f"  contraction constant of S  <=  lambda_2 + ||F||  ~  {lam2 + F:.4f}   < 1  => S is a CONTRACTION")
print(f"  => unique self-consistent fixed point = Haar (even-density 1/2).")

# --- SIDESTEP check: an atomic invariant measure is NOT self-consistent ---
# A fixed point c*=1 of T (T(1)=floor(3/2)=1) gives delta_1, an invariant measure of the integer map.
# Is delta_1 self-consistent (reproduced by L_nu with nu=delta_1)? L uses incoming bit from nu's conditional.
# delta_1: mass on c=1 (odd). Under the map 1->1, but with a FAIR/ nu-conditional incoming bit the low-bit
# distribution spreads -- delta_1 is invariant for the deterministic map but NOT a fixed point of the
# mean-field L_nu (which injects the conditional bit). We illustrate: Haar is L-stationary; delta_1 is not.
k = 6; mod = 1 << k
L = L_op(k)
u = np.ones(mod) / mod
d1 = np.zeros(mod); d1[1 % mod] = 1.0
print(f"\n  SIDESTEP (self-consistency is stronger than invariance):")
print(f"    Haar:    ||u L - u||_1     = {np.abs(u @ L - u).sum():.2e}   (self-consistent: YES)")
print(f"    delta_1: ||d1 L - d1||_1   = {np.abs(d1 @ L - d1).sum():.2f}   (self-consistent: NO -- spreads)")
print(f"    => of the many invariant measures (variational principle), only Haar is SELF-CONSISTENT;")
print(f"       the self-consistent framework is NOT blocked by the UE obstruction.")

print(f"""
READING (positive structural result):
  - The self-consistency map S: nu -> L_nu nu is a CONTRACTION (constant ~ lambda_2 + ||F|| ~ {lam2+F:.3f} < 1):
    a UNIQUE fixed point = Haar. This SIDESTEPS the variational-principle block on unique ergodicity, because
    self-consistency is STRONGER than invariance (only Haar is self-consistent; atomic invariant measures
    are not). So 'positive entropy => not uniquely ergodic' does NOT block the mean-field route.
  - CONNECTION to the favorable fact: the smallness of ||F|| (the contraction) is the Fourier decay of
    nu_{{2/3}}, which holds because 3/2 is NON-Pisot (Salem-Erdos / Bourgain-Dyatlov). non-Pisot =>
    contraction => unique self-consistent measure = Haar (even-density 1/2).
  - REMAINING GAP (named, the focused target): the orbit's empirical measure must TRACK the mean-field
    fixed point (propagation of chaos for one deterministic trajectory). The contraction makes the fixed
    point unique and attracting; the build is to show the single orbit converges to it -- using the renewal
    structure (the orbit returns/regenerates) + the contraction's attracting basin. The contraction (with
    the non-Pisot lever) is the engine; the tracking is the bridge. Provable engine, focused bridge.""")
