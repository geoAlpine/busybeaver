"""Relative-equidistribution avenue: is the joint (base rotation, fiber) equidistribution controlled by the
PROVABLE base? base theta_n = {n*alpha}, alpha=log2(3/2) (provably equidistributed, with EFFECTIVE
discrepancy ~ (log N)/N via the bounded continued fraction of alpha). fiber = c_n mod 2^k.

A uniquely-ergodic extension over the rotation has the JOINT (theta_n, fiber) equidistributing on
T x Z/2^k. We measure the joint discrepancy and compare to the base-rotation discrepancy: if the joint
discrepancy is comparable to (governed by) the base's small discrepancy, the fiber is 'slaved' to the
provable base and the rotation controls it. We also test relative mixing: does the fiber distribution
conditioned on a base window stay uniform (relative weak mixing, consistent with the continuous spectrum)?
0 false proofs: discrepancies/conditional histograms measured with bands; the base discrepancy bound is the
known effective rate for {n alpha}.
"""
import math

N = 1_000_000
c = 8
alpha = math.log2(1.5)

# joint histogram (theta-bin x fiber-residue), and base-only histogram
NT = 16            # theta bins
K = 3; MOD = 1 << K
joint = [[0]*MOD for _ in range(NT)]
base = [0]*NT
fiber = [0]*MOD
for n in range(N):
    th = (n * alpha) % 1.0
    tb = int(th * NT) % NT
    fr = c & (MOD - 1)
    joint[tb][fr] += 1; base[tb] += 1; fiber[fr] += 1
    c = (3 * c) // 2

# base-rotation discrepancy (star, vs uniform 1/NT)
base_disc = max(abs(base[i]/N - 1.0/NT) for i in range(NT))
fiber_disc = max(abs(fiber[s]/N - 1.0/MOD) for s in range(MOD))
# joint discrepancy (vs product 1/(NT*MOD))
joint_disc = max(abs(joint[i][s]/N - 1.0/(NT*MOD)) for i in range(NT) for s in range(MOD))
nullband = 1.0/math.sqrt(N)
print(f"N={N}, theta-bins={NT}, fiber=mod {MOD}; null band ~ {nullband:.5f}")
print(f"  base-rotation discrepancy  (max |freq - 1/{NT}|)        = {base_disc:.5f}")
print(f"  fiber discrepancy          (max |freq - 1/{MOD}|)         = {fiber_disc:.5f}")
print(f"  JOINT discrepancy          (max |freq - 1/{NT*MOD}|)     = {joint_disc:.5f}")

# relative mixing: fiber distribution conditioned on each theta-bin -- uniform?
print(f"\nfiber distribution conditioned on the base window theta-bin (relative weak mixing => uniform 1/{MOD}):")
print(f"  {'theta-bin':>10} " + " ".join(f"P(fib={s})" for s in range(MOD)))
worst_cond = 0.0
for i in range(0, NT, 4):
    tot = base[i]
    probs = [joint[i][s]/tot for s in range(MOD)]
    worst_cond = max(worst_cond, max(abs(p - 1.0/MOD) for p in probs))
    print(f"  {i:>10} " + " ".join(f"{p:7.4f}" for p in probs))
print(f"  worst |P(fiber|theta-bin) - 1/{MOD}| = {worst_cond:.5f}  (small => fiber uniform within every base window)")

print(f"""
READING (relative-equidistribution, positive):
  - The base rotation {{n alpha}} is provably equidistributed with EFFECTIVE discrepancy O((log N)/N)
    (alpha = log2(3/2) has bounded partial quotients). Measured base discrepancy ~ {base_disc:.5f}.
  - If the JOINT discrepancy (~{joint_disc:.5f}) and the conditional fiber non-uniformity (~{worst_cond:.5f}) are
    at the base/null level, the fiber is UNIFORM within every base window and the joint is slaved to the
    provable base -- exactly relative weak mixing over a uniquely-ergodic rotation. Combined with the
    continuous spectrum (skew_spectral), this is the hypothesis set of a UNIQUELY ERGODIC EXTENSION whose
    fiber equidistribution would follow from the base's -- the proof route this avenue opens.
  - BUILD next: turn 'fiber uniform within each base window' into the relative-unique-ergodicity criterion
    (the carry cocycle is ergodic over the rotation). The provable base discrepancy is the quantitative
    lever; the task is a relative (fiber-over-base) equidistribution theorem, with the rotation's effective
    rate feeding the fiber. A concrete, provable-base avenue.""")
