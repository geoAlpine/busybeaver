"""WALL (B): does the SELF-REFERENTIAL definition of the orbit's point select it into the
equidistributing (good) set, EXCLUDING the exceptional (clustered / Liouville-like) behaviour?

We test the *self-correction* hypothesis: if the orbit STARTS in a maximally clustered
configuration, does the deterministic map T(c)=floor(3c/2) pull it OUT (active restoring force),
or does it merely get diluted by future (already-balanced) bits?  We also confirm the status of
the atomic fixed points (which are clustered AND self-consistent) and that integer c0>=2 grows.

Ground truth is EXACT (Python big ints): e_n = c_n mod 2 with c_{n+1}=floor(3 c_n/2).
Carry phase psi_n = T_n/2^{n+1} mod 1 computed EXACTLY from T_{n+1}=3T_n+2^n e_n then floated
from the top ~60 bits (no (3/2)^n float blow-up).  .venv python only.  Zero claims of proof.
"""
import math, random

def orbit_parities(c0, N):
    """exact parity sequence e_0..e_{N-1} of the integer orbit c_{n+1}=floor(3 c_n/2)."""
    c = c0; out = []
    for _ in range(N):
        out.append(c & 1)
        c = (3 * c) >> 1   # floor(3c/2)
    return out

def orbit_phases(c0, N, prec=60):
    """exact carry phases psi_n in [0,1) and parities, via T_{n+1}=3T_n+2^n e_n (big int)."""
    c = c0; T = 0; phases = []; par = []
    for n in range(N):
        e = c & 1
        par.append(e)
        # psi_n = T / 2^{n+1} mod 1 = (T mod 2^{n+1}) / 2^{n+1}
        m = n + 1
        Tm = T & ((1 << m) - 1)               # T mod 2^{n+1}  (exact fractional numerator)
        if m <= prec:
            psi = Tm / (1 << m)
        else:
            psi = (Tm >> (m - prec)) / (1 << prec)  # top `prec` bits -> float, exact bits
        phases.append(psi)
        T = 3 * T + (e << n)
        c = (3 * c) >> 1
    return phases, par

def density(par):
    return sum(par) / len(par)  # ODD density; even-density = 1 - this

def windowed_even_density(par, W):
    out = []
    for i in range(0, len(par) - W + 1, W):
        seg = par[i:i+W]
        out.append(1 - sum(seg) / W)
    return out

def max_run(par):
    """longest run of identical parity (clustering proxy)."""
    best = cur = 1
    for i in range(1, len(par)):
        if par[i] == par[i-1]: cur += 1; best = max(best, cur)
        else: cur = 1
    return best

def phase_discrepancy(phases, bins=20):
    """L-infinity deviation of binned empirical phase dist from uniform (clustering proxy)."""
    h = [0]*bins
    for p in phases: h[min(bins-1, int(p*bins))] += 1
    n = len(phases)
    return max(abs(c/n - 1/bins) for c in h)

print("="*78)
print("WALL (B) self-selection / self-correction test")
print("="*78)

# ---------------------------------------------------------------------------
print("\n[1] Atomic fixed points: clustered AND self-consistent?  (refutes 'clustering excluded')")
for c0 in (0, 1):
    par = orbit_parities(c0, 50)
    print(f"   c0={c0}: parities first 12 = {par[:12]}  even-density={1-density(par):.3f}  "
          f"-> constant parity (maximally clustered) and a genuine FIXED POINT of T")

# ---------------------------------------------------------------------------
print("\n[2] Do integer orbits c0>=2 grow (cannot be trapped at the clustered atoms)?")
for c0 in (2, 8, 100, 2**20):
    c = c0
    for _ in range(60): c = (3*c) >> 1
    print(f"   c0={c0:>10}: after 60 steps c_60 has {c.bit_length()} bits  -> grows (no return to 0/1)")

# ---------------------------------------------------------------------------
print("\n[3] SELF-CORRECTION test: c0=2^k forces EXACTLY k consecutive even parities (clustered start).")
print("    Question: is the cluster ACTIVELY broken (restoring force) or merely DILUTED by balance?")
print(f"    {'c0':>10} {'forced evens':>12} {'run0':>6} {'evd[0:k]':>9} {'evd[k:2k]':>10} {'evd[2k:10k]':>12} {'evd[0:10k]':>11}")
for k in (10, 20, 40, 80):
    N = 10*k
    par = orbit_parities(2**k, N)
    # forced even run at the start:
    r0 = 0
    while r0 < len(par) and par[r0] == 0: r0 += 1
    evd_pre  = 1 - density(par[:k])
    evd_post = 1 - density(par[k:2*k]) if 2*k <= N else float('nan')
    evd_far  = 1 - density(par[2*k:]) if 2*k < N else float('nan')
    evd_all  = 1 - density(par)
    print(f"    {2**k!s:>10.10} {k:>12} {r0:>6} {evd_pre:>9.3f} {evd_post:>10.3f} {evd_far:>12.3f} {evd_all:>11.3f}")
print("    (run0 ~ k confirms the forced cluster; evd[k:2k] ~ 0.5 = balance resumes the step AFTER the")
print("     forced segment ends; evd[0:10k] -> 0.5 = the early cluster is OUTGROWN/diluted, not erased)")

# ---------------------------------------------------------------------------
print("\n[4] Restoring force?  corr(next parity, trailing-window even-bias).  (~0 = NO active pull)")
par = orbit_parities(8, 200000)
sig = [1 - 2*e for e in par]  # +1 even, -1 odd
for W in (8, 32, 128, 512):
    num = 0.0; den_a = 0.0; den_b = 0.0; cnt = 0
    run = 0.0
    # trailing mean of last W signs predicting next sign
    import statistics
    xs = []; ys = []
    s = 0.0
    from collections import deque
    dq = deque()
    for i in range(len(sig)):
        if len(dq) == W:
            xs.append(s / W); ys.append(sig[i])
        dq.append(sig[i]); s += sig[i]
        if len(dq) > W: s -= dq.popleft()
    mx = sum(xs)/len(xs); my = sum(ys)/len(ys)
    cov = sum((a-mx)*(b-my) for a,b in zip(xs,ys))
    vx = sum((a-mx)**2 for a in xs); vy = sum((b-my)**2 for b in ys)
    corr = cov / math.sqrt(vx*vy) if vx>0 and vy>0 else 0.0
    print(f"   W={W:>4}: corr(trailing even-bias, next sign) = {corr:+.4f}")

# ---------------------------------------------------------------------------
print("\n[5] Spontaneous re-clustering vs fair coin (max run length over N=200000).")
print("    If the orbit equidistributes statistically, max run ~ log2(N) ~ 17-18 like a fair coin.")
mr = max_run(par)
# fair-coin expected max run ~ log2(N)
print(f"   real orbit c0=8: max parity run = {mr}   (fair-coin E[max run] ~ {math.log2(len(par)):.1f})")
random.seed(1)
fair = [random.randint(0,1) for _ in range(len(par))]
print(f"   fair coin       : max parity run = {max_run(fair)}")

# ---------------------------------------------------------------------------
print("\n[6] Phase clustering over time: discrepancy of carry phases psi_n, clustered vs balanced start.")
print(f"    {'start':>14} {'N':>6} {'phase L-inf discrepancy (20 bins), lower=more uniform':>10}")
for label, c0, N in [("c0=8 (orbit)", 8, 4000),
                     ("c0=2^40 (clustered)", 2**40, 4000),
                     ("c0=2^200 (clustered)", 2**200, 4000),
                     ("random ~2^300", random.getrandbits(300) | 1, 4000)]:
    ph, pr = orbit_phases(c0, N)
    d_early = phase_discrepancy(ph[:200])
    d_late  = phase_discrepancy(ph[400:])
    print(f"    {label:>20} {N:>6}   early[:200]={d_early:.3f}   late[400:]={d_late:.3f}   "
          f"even-density={1-density(pr):.3f}")
print("    (clustered starts show high EARLY discrepancy that relaxes to the same LATE value as c0=8")
print("     => the limiting phase law is start-independent = the cluster is diluted, not the cause)")

print("\n" + "="*78)
print("READING: a 'restoring force' (active self-correction) would show corr<0 in [4] and the")
print("forced cluster being broken EARLY in [3]; we instead see corr~0 and the cluster persisting")
print("EXACTLY its forced length then balance RESUMING (dilution). The asymptotic balance that")
print("dilutes the cluster IS the (3/2)^j equidistribution = Mahler. No new selection mechanism.")
print("="*78)
