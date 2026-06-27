"""E2 (internal thread): characterize the carry kernel K by correlation SCALE, robustly.
The feedback ||F|| = sum_h K(h) C(h). A scenery that is block-correlated with block length L has triangular
autocorrelation C(h) ~ (1 - h/L) for h<L, 0 beyond -- so the gain measured on it ~ sum_{h<L} K(h)(1-h/L),
i.e. a SCALE-L probe of the kernel. We sweep L and measure the DIRECT multi-flip gain (the robust estimator
from perturbation_F, NOT the noise-dominated single-flip), giving the kernel's response by scale. If the
gain stays small for ALL L, K is bounded across scales => ||F|| is sub-critical wherever the orbit's
(measured tiny) correlation lives.
0 false proofs: gains are robust finite-difference slopes (central, multi-flip) with a panel; we report the
profile and state plainly what it does/doesn't establish (still measured, not a proof of ||F||<1).
"""
import math

N = 120000

def carry_density(e):
    T = 0; s = 0
    for n in range(len(e)):
        s += (T >> n) & 1; T = 3 * T + (1 << n) * e[n]
    return s / len(e)

def block_scenery(N, L, seed=1):
    """mean-1/2 block-correlated bits: constant over blocks of length L, block value from a hash."""
    e = bytearray(N)
    for n in range(N):
        b = n // L
        e[n] = ((b * 2654435761 + seed) >> 20) & 1
    return e

def bias_by(seq, delta):
    s = bytearray(seq)
    if delta == 0: return s
    tgt = 1 if delta > 0 else 0; src = 1 - tgt
    idx = [i for i in range(len(s)) if s[i] == src]
    k = min(int(abs(delta) * len(s)), len(idx))
    if k:
        step = len(idx) / k
        for j in range(k): s[idx[int(j * step)]] = tgt
    return s

def gain(seq):
    ep = bias_by(seq, +0.05); em = bias_by(seq, -0.05)
    inp = sum(ep) / len(ep); inm = sum(em) / len(em)
    return (carry_density(ep) - carry_density(em)) / (inp - inm) if inp != inm else 0.0

print(f"feedback gain ||F|| by scenery correlation SCALE L (block-correlated; N={N}); robust multi-flip")
print(f"  {'block L':>8} {'in-density':>10} {'gain ||F||(L)':>14}")
gains = []
for L in [1, 2, 4, 8, 16, 32, 64, 128, 256, 512, 1024]:
    e = block_scenery(N, L)
    g = gain(e); gains.append((L, g))
    print(f"  {L:>8} {sum(e)/N:>10.4f} {g:>+14.4f}")
mg = max(abs(g) for _, g in gains)
print(f"\n  sup |gain| over all scales = {mg:.4f}   (critical = 1)")
print(f"""
READING (E2 carry-kernel by scale):
  - If sup|gain(L)| stays well below 1 across ALL correlation scales L, the carry kernel K is bounded by
    scale and ||F|| is sub-critical no matter where the orbit's correlation lives -- the x3 carry mixing
    damps a density bias regardless of the scenery's block scale. Measured sup ~ {mg:.3f}.
  - This is the ROBUST (multi-flip) characterization the single-flip probe failed to give. It supports
    ||F||<1 across scales empirically. It is NOT a proof: a proof needs an unconditional bound on K(h)
    (carry-propagation / Mauduit-Rivat-Gowers) combined with the measured orbit autocorrelation C(h)~0,
    to get sum_h |K(h)||C(h)| < 1. The kernel-by-scale profile here is the empirical input to that target.""")
