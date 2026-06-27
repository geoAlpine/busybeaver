"""BUILD: the analytic structure of the gain functional, toward a Mauduit-Rivat carry-lemma bound |gain|<1.

gain = (1/N) sum_n sum_k s(n,k),  s(n,k) = bit_n(T_n + (1-2 r_k) Delta_k) - bit_n(T_n) in {-1,0,+1},
Delta_k = 2^k 3^{n-1-k} = d T_n / d e_k. We decompose s by OFFSET j = n-k and ask:
  (A) DECAY: does |s| (carry-propagation magnitude) decay in j?  (the MR carry lemma controls this)
  (B) CANCELLATION: is the SIGNED mean of s ~ 0 at each j (so the gain is small by cancellation, not decay)?
  (C) the running gain = sum over offsets of signed-mean -- confirm it is ~0 and identify whether decay or
      cancellation carries it.
This isolates EXACTLY which ingredient an unconditional |gain|<1 proof must supply: a carry-propagation
decay bound (A) and/or a signed-cancellation (B). 0 false proofs: report measured profiles with bands.
"""
import math

N = 4000          # number of orbit steps (n up to N); offsets j up to J
J = 60
c = 8; r = bytearray(N + J + 2)
for i in range(N + J + 2):
    r[i] = c & 1; c = (3 * c) // 2

# build T_n exactly and store; T_{n+1} = 3 T_n + 2^n r_n
T = [0] * (N + 1)
acc = 0
for n in range(N):
    T[n] = acc
    acc = 3 * acc + (1 << n) * r[n]
T[N] = acc

def bit(x, i): return (x >> i) & 1

# DENSITY-direction sensitivity (the one relevant to ||F||): adding density flips a 0->1, i.e. +Delta_k at
# positions with r_k=0. (The complement-flip mixes +/-Delta and is a DIFFERENT functional -- not ||F||.)
# s_plus(n,k) = bit_n(T_n + Delta_k) - bit_n(T_n), accumulated ONLY at r_k=0; the density gain decomposes as
# gain = sum_j (signed mean of s_plus at offset j).
sum_signed = [0] * (J + 1)
sum_abs = [0] * (J + 1)
cnt = [0] * (J + 1)
for n in range(20, N):
    Tn = T[n]; bn = bit(Tn, n)
    for j in range(1, J + 1):
        k = n - j
        if k < 0: break
        if r[k] != 0:                         # only 0-positions can be flipped 0->1 (add density)
            continue
        Delta = (1 << k) * pow(3, n - 1 - k)
        s = bit(Tn + Delta, n) - bn           # +Delta response, in {-1,0,+1}
        sum_signed[j] += s; sum_abs[j] += abs(s); cnt[j] += 1

print(f"DENSITY-direction sensitivity s_plus by offset j=n-k (r_k=0 only; orbit n up to {N}):")
print(f"  {'j':>3} {'mean |s+| (decay?)':>18} {'mean s+ (cancellation?)':>23}")
gain_partial = 0.0
for j in range(1, J + 1):
    if cnt[j] == 0: continue
    ma = sum_abs[j] / cnt[j]; ms = sum_signed[j] / cnt[j]
    gain_partial += ms
    if j <= 20 or j % 10 == 0:
        print(f"  {j:>3} {ma:>18.4f} {ms:>+23.5f}")
print(f"\n  sum_j mean|s+| (total abs SINGLE-FLIP marginal sensitivity, j<=60) = {sum(sum_abs[j]/cnt[j] for j in range(1,J+1) if cnt[j]):.3f}")
print(f"  sum_j mean s+  (SINGLE-FLIP marginal signed sum, j<=60)          = {gain_partial:+.4f}")

# --- the key reconciliation: single-flip marginal sum  vs  actual multi-flip density response ---
# (a) verify the single-flip s_plus is computed right: flip ONE 0-bit, measure the actual output-density shift.
def carry_density_seq(e):
    T = 0; s = 0
    for n in range(len(e)):
        s += (T >> n) & 1; T = 3*T + (1 << n)*e[n]
    return s/len(e)
e0 = bytearray(r[:N])
base_dens = carry_density_seq(e0)
# pick a 0-position and flip it
k0 = next(i for i in range(50, N) if e0[i] == 0)
e1 = bytearray(e0); e1[k0] = 1
single_shift = (carry_density_seq(e1) - base_dens) * N    # in units of #bits, ~ sum_j s_plus(k0+j,k0)
# (b) actual MULTI-flip density response (||F||): add density by flipping many 0s -> 1
def shift_density(e, frac):
    e = bytearray(e); zeros = [i for i in range(len(e)) if e[i]==0]
    kk = int(frac*len(e)); step = len(zeros)/kk if kk else 1
    for j in range(kk): e[zeros[int(j*step)]] = 1
    return e
# central difference, input density measured correctly (NOT the output baseline)
ep = shift_density(e0, 0.05); em = bytearray(e0)  # +0.05 density vs base
inp = sum(ep)/N; inb = sum(em)/N
multi_gain = (carry_density_seq(ep) - carry_density_seq(em)) / (inp - inb) if inp != inb else 0.0
print(f"\n  RECONCILIATION (single-flip marginal vs actual multi-flip response):")
print(f"    one 0-bit flipped at k={k0}: net output shift = {single_shift:+.1f} bits over N={N} "
      f"(~O(sqrt N)={math.sqrt(N):.0f} fluctuation; single flips are large, sign varies by realization).")
print(f"    actual MULTI-flip density gain d(out)/d(in) = {multi_gain:+.4f}.")

# Is the absolute sensitivity decaying or flat in j?
mas = [sum_abs[j]/cnt[j] for j in range(1, J+1) if cnt[j]]
print(f"  mean|s| at j=1..5  : {[round(x,3) for x in mas[:5]]}")
print(f"  mean|s| at j=56..60: {[round(x,3) for x in mas[-5:]]}")
band = 1/math.sqrt(cnt[1]) if cnt[1] else 0
print(f"  per-j signed band ~ {band:.4f}")

print(f"""
READING (honest -- this probe is INCONCLUSIVE on the precise mechanism; one robust qualitative finding):
  - ROBUST: single-flip sensitivities are LARGE and non-decaying (mean|s+| ~ 0.5-0.97 at every offset),
    consistent with the sensitive-dependence / positive-entropy carry found earlier (d_dissect, coupling_brick).
    A single input bit strongly moves bit_n at all offsets, with O(sqrt N) net sign that varies by realization.
  - NOT CLEANLY RESOLVED: the per-offset signed decomposition (and its sum) is dominated by O(sqrt N)
    single-flip fluctuations and by nonlinear flip-INTERACTIONS (the actual multi-flip density response is
    NOT the sum of marginal single-flip responses). So this decomposition does NOT cleanly isolate the proof
    mechanism (linear carry-decay vs signed cancellation vs multilinear interaction); the per-offset numbers
    here are not trustworthy enough to claim one.
  - The TRUSTWORTHY gain measurement remains the direct finite-difference of perturbation_F.py (gain ~ 0.04,
    sub-critical, robust across correlation structures) -- a multi-flip output-vs-input density slope, which
    is unambiguous; this single-flip decomposition is not.
  CONCLUSION (sound): the gain ||F|| is small/sub-critical (perturbation_F, direct), and the smallness is a
  CANCELLATION/nonlinear effect (single sensitivities are large) -- so a proof is unlikely to come from a
  single-carry decay bound. Identifying the EXACT analytic object (the right multilinear/cancellation
  statement) is NOT achieved by this probe and remains open. (No over-claim: the earlier '-0.94 gain' and
  'multilinear carry lemma' readings were artifacts of the noisy marginal decomposition and are retracted.)""")
