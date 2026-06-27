"""A would-be clean proof that the ANNEALED feedback gain is exactly 0 -- ATTEMPTED, then REFUTED by its own
verification (soundness discipline). Kept as an honest record of the failed argument and the correct status.

ATTEMPTED CLAIM. For i.i.d. Bernoulli(p) scenery, carry density bit_n(T_n) = 1/2 exactly for all p, so the
annealed gain = 0 -- PROVED via: 'step(.,b) is a bijection of Z/2^k => uniform is L_p-stationary for all p'.

WHY IT FAILS [verified below]. step(s,b) = ((3(s + b*2^k) - (s mod 2))/2) mod 2^k involves a division by 2,
which is 2-to-1, so step(.,b) is NOT a bijection (the verification prints P_1/P_0 bijection? = FALSE). Hence
uniform is L_p-stationary ONLY at p=1/2 (verified: True at 0.5, False at 0.3/0.7), and the clean proof
collapses. So the annealed gain = 0 is NOT proved by this argument.

CORRECT STATUS. The carry density is EMPIRICALLY ~1/2 for all p (measured 0.497-0.501 below), but this is
NOT proven -- it is itself a digit-equidistribution of T_n[e] (Mahler-class), same as everything else. The
annealed gain ~0 remains MEASURED, not proven. (Recorded honestly: the soundness gate caught a false proof
before it entered the record.)
"""
import numpy as np

def step(s, b, k):
    mod = 1 << k
    return ((3 * (s + (b << k)) - (s & 1)) // 2) % mod

def Lp(k, p):
    mod = 1 << k
    M = np.zeros((mod, mod))
    for s in range(mod):
        M[s, step(s, 1, k)] += p
        M[s, step(s, 0, k)] += (1 - p)
    return M

print("Verify: uniform is L_p-stationary for all p (=> annealed carry density = 1/2, gain = 0 exactly)")
print(f"  {'k':>2} {'p':>5} {'uniform stationary?':>20} {'P_1 bijection?':>15} {'P_0 bijection?':>15}")
for k in (3, 5, 7):
    mod = 1 << k
    img1 = len(set(step(s, 1, k) for s in range(mod)))
    img0 = len(set(step(s, 0, k) for s in range(mod)))
    for p in (0.3, 0.5, 0.7):
        M = Lp(k, p)
        u = np.ones(mod) / mod
        stat = np.allclose(u @ M, u, atol=1e-12)
        print(f"  {k:>2} {p:>5.1f} {str(stat):>20} {str(img1==mod):>15} {str(img0==mod):>15}")

# confirm the annealed carry density is 1/2 for biased i.i.d. input (driving T directly), several p
def annealed_carry_density(p, N, seed=12345):
    # deterministic Bernoulli(p)-like bits, low correlation, via a hash; measure mean bit_n(T_n)
    T = 0; s = 0
    for n in range(N):
        s += (T >> n) & 1
        u = ((n * 2654435761 + seed) & 0xFFFFFFFF) / 4294967296.0
        e = 1 if u < p else 0
        T = 3 * T + (1 << n) * e
    return s / N

print(f"\nannealed carry density for i.i.d. Bernoulli(p) input (N=120000): should be 1/2 for ALL p")
for p in (0.2, 0.35, 0.5, 0.65, 0.8):
    print(f"  p={p:.2f}: carry density = {annealed_carry_density(p, 120000):.4f}")

print("""
=> REFUTED: P_1/P_0 are NOT bijections (the /2 is 2-to-1), so uniform is L_p-stationary ONLY at p=1/2
   (above: True at 0.5, False at 0.3/0.7). The clean proof that the annealed gain = 0 FAILS.
=> CORRECT STATUS: the annealed carry density is EMPIRICALLY ~1/2 for all p (measured 0.497-0.501), but this
   is itself a Mahler-class digit-equidistribution of T_n[e], NOT proven. So the annealed gain ~0 stays
   MEASURED, not proven; there is no new proven component. (Soundness: a false 'PROVEN' was caught and
   retracted before entering the record. The closed-loop ||F||<1 remains the open Mahler core.)""")
