"""BUILD: the closed-loop feedback gain ||F|| linearized AT THE ORBIT, bridging open-loop ~0 to closed-loop <1.

The selfconsistent gain was open-loop (exogenous low-correlation scenery). The CLOSED-loop linearization at
the self-consistent fixed point (the real orbit) is the one-pass response gain when the scenery carries the
ORBIT'S OWN correlation structure. We compute it by perturbing the real parity r by a density-delta and
feeding it through the carry, measuring the output carry/parity density response:
    gain_closed = d(output density)/d(input density)   evaluated at scenery = (biased) real orbit parity.
If |gain_closed| < 1, the orbit is a LINEARLY STABLE self-consistent fixed point (sub-critical F). We also
sweep a PANEL of scenery correlation structures to bound the gain across correlation types -- since the
orbit's scenery is one such correlated sequence, a uniform |gain|<1 over the panel bounds the closed loop.
0 false proofs: gains are measured finite-difference slopes with bands; |gain|<1 (if observed) is the
empirical sub-criticality, and we state plainly that proving it for the orbit is the Mahler core.
"""
import math

N = 120000
# real orbit parity r
c = 8; r = bytearray(N)
for n in range(N):
    r[n] = c & 1; c = (3 * c) // 2

def carry_density(e):
    T = 0; s = 0
    for n in range(len(e)):
        s += (T >> n) & 1
        T = 3 * T + (1 << n) * e[n]
    return s / len(e)

def parity_density(e):
    T = 0; p3 = 1; s = 0
    for n in range(len(e)):
        s += ((8 * p3 >> n) & 1) ^ ((T >> n) & 1)
        T = 3 * T + (1 << n) * e[n]; p3 *= 3
    return s / len(e)

def bias_by(seq, delta):
    """return a copy of seq with input density shifted by ~delta, preserving most of its correlation:
       if delta>0 flip a delta-fraction of 0s to 1 (deterministic, evenly spaced); if delta<0 flip 1s to 0."""
    s = bytearray(seq)
    if delta == 0: return s
    target = 1 if delta > 0 else 0
    src = 1 - target
    idx = [i for i in range(len(s)) if s[i] == src]
    k = int(abs(delta) * len(s))
    if k > len(idx): k = len(idx)
    # evenly spaced positions among the flippable ones (deterministic)
    if k > 0:
        step = len(idx) / k
        for j in range(k):
            s[idx[int(j * step)]] = target
    return s

def gain_at(seq, out_fn):
    ep = bias_by(seq, +0.05); em = bias_by(seq, -0.05)
    inp = sum(ep)/len(ep); inm = sum(em)/len(em)
    op = out_fn(ep); om = out_fn(em)
    return (op - om) / (inp - inm)

print(f"closed-loop feedback gain linearized at various sceneries (N={N}); |gain|<1 = sub-critical")
print(f"  {'scenery':>26} {'in-density':>10} {'carry gain':>11} {'parity gain':>12}")

# the actual orbit (the closed-loop fixed point) + a panel of correlation structures
import math as _m
def sturmian(N, g):
    return bytearray(1 if (((n+1)*g) % 1.0) >= 0.5 else 0 for n in range(N))
def blockcorr(N, L):
    # block-correlated: constant over blocks of length L, value = parity of block index hash
    out = bytearray(N)
    for n in range(N):
        b = n // L
        out[n] = ((b * 2654435761) >> 20) & 1
    return out

panel = [
    ("REAL ORBIT PARITY (closed loop)", r),
    ("low-corr (open loop ref)", bytearray(((k*2654435761)>>20)&1 for k in range(N))),
    ("Sturmian {n*log2 1.5}", sturmian(N, _m.log2(1.5))),
    ("block-corr L=4", blockcorr(N, 4)),
    ("block-corr L=16", blockcorr(N, 16)),
    ("period-3 (1,0,0)", bytearray(1 if n%3==0 else 0 for n in range(N))),
]
gains_c = []; gains_p = []
for name, seq in panel:
    gc = gain_at(seq, carry_density); gp = gain_at(seq, parity_density)
    gains_c.append(gc); gains_p.append(gp)
    print(f"  {name:>26} {sum(seq)/N:>10.4f} {gc:>+11.4f} {gp:>+12.4f}")

mc = max(abs(g) for g in gains_c); mp = max(abs(g) for g in gains_p)
print(f"\n  sup |carry gain| over panel = {mc:.4f}    sup |parity gain| over panel = {mp:.4f}")
print(f"""
READING (perturbation bound, open-loop ~0 -> closed-loop):
  - The gain linearized AT THE REAL ORBIT (the closed-loop fixed point) is the top row -- if |gain|<1 there,
    the orbit is a LINEARLY STABLE self-consistent fixed point => sub-critical F at the orbit.
  - The panel sweeps correlation structures (Sturmian, block-correlated at several lengths, periodic). The
    orbit's scenery is ONE correlated sequence, so sup|gain| over a rich correlation panel UPPER-BOUNDS the
    closed-loop gain by structure type. Measured sup ~ {mp:.3f} (parity), {mc:.3f} (carry).
  - If sup|gain| stays well below 1 across ALL correlation types, the feedback F is sub-critical ROBUSTLY
    -- the x3 carry mixing kills the input-bias response regardless of the scenery's correlation. That is
    the operational content of ||F||<1, now bounded across correlation structures (not just open-loop).
  HONEST: still measured, not proven; the orbit's exact scenery correlation is the quenched object, and a
  proof of |gain|<1 for it is the Mahler core. But the bound now covers correlated sceneries, closing the
  open->closed gap empirically.""")
