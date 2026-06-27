"""WALL (B) sub-question: can an INTEGER orbit of x -> floor(3x/2) carry a PERSISTENT mod-2 bias
(a non-atomic biased orbit) -- or is bias always transient (-> equidistribution)?

This is the ONE wall-(B) sub-question not literally identical to Mahler (A): the atomic points
(eventually-constant parity, delta_0/delta_1) are PROVEN excluded (integer c0>=2 grows). The remaining
exceptional-set members are NON-ATOMIC: recurrent (parity returns) but with Birkhoff parity average != 1/2.

We TEST whether integer floor(3x/2)-orbits can exhibit such a persistent bias:
  (A) sweep many integer starts c0 (structured + random, various sizes), measure tail even-density;
  (B) for selected starts, track running tail-density and max sustained windowed bias (transient vs persistent);
  (C) the 2-adic valuation budget: odd-density = 1/avgD_odd asymptotically; check the bias<->depth coupling
      and the UNCONDITIONAL two-sided range O*avgD_odd in [1 - o(1), 1.585];
  (D) hunt specifically for any c0 whose tail density stays far from 1/2 over a long window (candidate
      biased orbit); push N up on any candidate to see if the bias survives.

Exact big-int arithmetic only. 0 false claims: finite N proves nothing about the limit; we report what is
OBSERVED and label it. .venv python only.
"""
import random, math

def v2(x):
    if x == 0:
        return 10**9
    r = 0
    while x & 1 == 0:
        x >>= 1; r += 1
    return r

def even_density_tail(c0, N, tail_frac=0.5):
    """Return (tail_even_density, full_even_density, min_balance) for orbit of length N."""
    c = c0
    E = 0
    Etail = 0
    t0 = int(N * (1 - tail_frac))
    bal = 0; minbal = 0
    for n in range(N):
        e = c & 1  # parity
        if e == 0:
            E += 1
            if n >= t0: Etail += 1
            bal += 1
        else:
            bal -= 1
        if bal < minbal: minbal = bal
        c = (3 * c) >> 1  # floor(3c/2)
    return Etail / (N - t0), E / N, minbal

# ---------------------------------------------------------------------------
print("="*92)
print("(A) SWEEP: tail even-density (last half) over many integer starts c0; N=20000")
print("    persistent bias would show tail-density bounded away from 0.5 (fair-coin sd ~ 0.5/sqrt(N/2) ~",
      f"{0.5/math.sqrt(10000):.4f})")
print("="*92)
N = 20000
sd = 0.5 / math.sqrt(N * 0.5)
starts = []
# structured starts
for k in [1,2,3,5,8,16,100,1000]:
    starts.append(("c0=%d"%k, k))
starts.append(("c0=8 (Antihydra)", 8))
for k in [10,20,40,80,200]:
    starts.append(("2^%d"%k, 1 << k))
# Mahler-flavored starts (binary patterns)
starts.append(("(2^60-1)", (1<<60)-1))
starts.append(("alt 0101..(60b)", int("01"*30, 2)))
starts.append(("0..0 1..1 (60b)", ((1<<30)-1)))
# random starts of various sizes
random.seed(12345)
for bits in [30, 60, 120, 300]:
    for _ in range(3):
        x = random.getrandbits(bits) | 1
        starts.append(("rand %db"%bits, x))

results = []
for name, c0 in starts:
    td, fd, mb = even_density_tail(c0, N)
    z = (td - 0.5) / sd
    results.append((name, c0, td, fd, mb, z))
    flag = "  <-- |z|>3 !" if abs(z) > 3 else ""
    print(f"  {name:>22}  tail_even_dens={td:.4f}  full={fd:.4f}  minbal={mb:>5}  z={z:+6.2f}{flag}")

zs = [r[5] for r in results if not r[0].startswith("c0=") or r[1] >= 4]
print(f"\n  tail-density z-scores: mean={sum(zs)/len(zs):+.3f}, max|z|={max(abs(z) for z in zs):.2f}"
      f"  (fair-coin: ~N(0,1), expect max|z|~2-3 over {len(zs)} starts)")

# ---------------------------------------------------------------------------
print("\n" + "="*92)
print("(B) TRANSIENCE: running tail-density vs N for structured-biased starts; does early bias decay?")
print("="*92)
for name, c0 in [("2^200", 1<<200), ("2^1000", 1<<1000), ("c0=8", 8), ("(2^200-1)", (1<<200)-1)]:
    c = c0
    E = 0
    checkpoints = [500, 2000, 8000, 30000, 60000]
    out = []
    maxN = checkpoints[-1]
    # also track max sustained windowed bias over a sliding window W
    W = 2000
    from collections import deque
    win = deque()
    winE = 0
    maxwinbias = 0.0
    for n in range(maxN):
        e = 1 if (c & 1) == 0 else 0  # 1 if even
        E += e
        win.append(e); winE += e
        if len(win) > W:
            winE -= win.popleft()
        if len(win) == W and n > 2*W:
            b = abs(winE / W - 0.5)
            if b > maxwinbias: maxwinbias = b
        c = (3 * c) >> 1
        if n + 1 in checkpoints:
            out.append((n+1, E/(n+1)))
    s = "  ".join(f"N={nn}:{d:.4f}" for nn, d in out)
    print(f"  {name:>12}  even-dens  {s}   max|sliding-W{W} bias|={maxwinbias:.4f}")
print(f"  (fair-coin sliding-window-{W} bias typically <= ~{3*0.5/math.sqrt(W):.4f}; persistent bias would exceed it steadily)")

# ---------------------------------------------------------------------------
print("\n" + "="*92)
print("(C) VALUATION BUDGET coupling: odd-density p and avgD_odd; identity O*avgD_odd = 1 + v2(cn)/n - v2(c0)/n")
print("    biased non-atomic orbit (p != 1/2) <=> avgD_odd = (1+delta)/p, delta=v2(cn)/n in [0, 0.585]")
print("="*92)
for name, c0 in [("c0=8", 8), ("rand 120b", random.getrandbits(120)|1), ("2^200", 1<<200)]:
    c = c0
    O = 0; Sodd = 0
    Nb = 40000
    for n in range(Nb):
        if c & 1:
            O += 1
            Sodd += v2(3*c - 1)
        c = (3*c) >> 1
    v2cn = v2(c)
    p = O / Nb
    avgD = Sodd / O
    lhs = p * avgD
    rhs = 1 + v2cn/Nb - v2(c0)/Nb
    print(f"  {name:>12}  odd-dens p={p:.4f}  avgD_odd={avgD:.4f}  p*avgD={lhs:.4f}  "
          f"1+v2(cn)/n-..={rhs:.4f}  v2(cn)={v2cn} (={v2cn/Nb:.4f}*n)")
print("  unconditional range: p*avgD_odd in [1 - v2(c0)/n , 1.585]  (Haar: p=1/2, avgD=2 => p*avgD=1)")

# ---------------------------------------------------------------------------
print("\n" + "="*92)
print("(D) HUNT for a biased integer orbit: scan 4000 small/random starts for tail-density far from 0.5")
print("="*92)
random.seed(7)
Nh = 6000
sdh = 0.5/math.sqrt(Nh*0.5)
worst = []
cnt = 0
for trial in range(4000):
    if trial < 2000:
        c0 = trial + 2            # all small starts 2..2001
    else:
        c0 = random.getrandbits(random.choice([20,40,80,160])) | 1
    td, fd, mb = even_density_tail(c0, Nh, tail_frac=0.5)
    z = (td-0.5)/sdh
    worst.append((abs(z), z, c0, td))
    cnt += 1
worst.sort(reverse=True)
print(f"  scanned {cnt} starts, orbit length {Nh}; fair-coin expects max|z| ~ {math.sqrt(2*math.log(cnt)):.2f} (Gaussian extreme)")
print("  top-8 most-biased tails:")
for az, z, c0, td in worst[:8]:
    print(f"    c0={c0:<22} tail_even_dens={td:.4f}  z={z:+.2f}")
# push N up on the most biased candidate to test persistence
print("\n  persistence test on the most-biased candidate (push N up):")
cand = worst[0][2]
for NN in [6000, 20000, 60000]:
    td, fd, mb = even_density_tail(cand, NN, tail_frac=0.5)
    z = (td-0.5)/(0.5/math.sqrt(NN*0.5))
    print(f"    c0={cand}  N={NN:>6}  tail_even_dens={td:.4f}  full={fd:.4f}  z={z:+.2f}")
print("  (if z -> 0 as N grows, the bias is TRANSIENT; if it stays large, candidate persistent-biased orbit)")
