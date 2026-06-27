"""Attack T_n directly. The orbit parity is  r_n = c_n mod 2 = bit_n(8*3^n - T_n),
where T_n = parity-history carry-sum (T_{n+1}=3 T_n + 2^n r_n, T_0=0), and T_n == 8*3^n (mod 2^n).

DECOMPOSE the orbit parity against the PURE-POWER moving-middle digit that D-S/Subspace CAN control:
    r_pure(n) := bit_n(8*3^n)                      [pure 3^n digit -- D-S: longest run o(n); Mahler: dens 1/2]
    r_orb(n)  := bit_n(8*3^n - T_n) = c_n mod 2     [the real orbit parity = even/odd]
    d(n)      := r_orb(n) XOR r_pure(n)             [the correction INDUCED by subtracting T_n]
Question: is the wall purely in d (the T_n carry correction)? If r_orb correlates with r_pure, then the
Subspace/D-S control of 3^n LEAKS onto the orbit and we have a crack. If d is an independent fair coin,
the feedback fully decouples and the wall is exactly the T_n carry, with NO leakage from D-S.

Also: the carry/borrow into bit n when forming 8*3^n - T_n. Since T_n == 8*3^n (mod 2^n), the low n bits
CANCEL; bit_n is the borrow-out of that forced cancellation plus the high parts. We test what predicts d(n).
0 false proofs: report measured correlations with shuffle-null bands; claim a handle only if it beats null.
"""
import math

def v2(x):
    if x == 0: return 10**9
    r = 0
    while x & 1 == 0: x >>= 1; r += 1
    return r

N = 200000
# orbit + parity + T_n
c = 8
r_orb = []
Tn = 0
p3 = 1            # 3^n
p2 = 1           # 2^n
r_pure = []
d = []
Tlow_forced = []  # check T_n == 8*3^n mod 2^n
borrow_bit = []   # the actual borrow into position n in 8*3^n - T_n
for n in range(N):
    # orbit parity
    ro = c & 1
    r_orb.append(ro)
    # pure power moving-middle digit
    rp = (8 * p3 >> n) & 1
    r_pure.append(rp)
    d.append(ro ^ rp)
    # integrality check (cheap, only first 200)
    if n < 200:
        Tlow_forced.append(((Tn % p2) == ((8 * p3) % p2)))
    # advance
    Tn = 3 * Tn + p2 * ro
    c = (3 * c) // 2
    p3 *= 3
    p2 <<= 1

print(f"integrality T_n == 8*3^n mod 2^n (n<200): {'OK' if all(Tlow_forced) else 'FAIL'}")

def dens(a): return sum(a) / len(a)
def corr(a, b):
    m = len(a); ma = sum(a)/m; mb = sum(b)/m
    cov = sum((a[i]-ma)*(b[i]-mb) for i in range(m))/m
    va = sum((x-ma)**2 for x in a)/m; vb = sum((x-mb)**2 for x in b)/m
    if va == 0 or vb == 0: return 0.0
    return cov/math.sqrt(va*vb)

print(f"\ndensities over N={N}:")
print(f"  r_pure (bit_n(8*3^n), pure power) density = {dens(r_pure):.5f}")
print(f"  r_orb  (orbit parity = even/odd)  density = {dens(r_orb):.5f}")
print(f"  d = r_orb XOR r_pure              density = {dens(d):.5f}")

# null band for correlation of two ~1/2 bit sequences of length N: std ~ 1/sqrt(N)
nullstd = 1/math.sqrt(N)
print(f"\ncorrelations (null std ~ {nullstd:.4f}, |corr|>~3x = signal):")
print(f"  corr(r_orb, r_pure) = {corr(r_orb, r_pure):+.5f}   <- does Subspace-controllable 3^n digit LEAK onto orbit?")
print(f"  corr(d, r_pure)     = {corr(d, r_pure):+.5f}")
print(f"  corr(r_orb, d)      = {corr(r_orb, d):+.5f}")

# Is d predictable from anything tame? test lag autocorrelation of d, and d vs low bits of T_n.
print(f"\nis d (the T_n carry correction) itself structured, or an independent fair coin?")
for lag in (1, 2, 3, 5, 8):
    a = d[:-lag]; b = d[lag:]
    print(f"  lag-{lag} autocorr(d) = {corr(a, b):+.5f}")

# mutual-information-ish: predict d(n) from (r_orb(n-1), r_orb(n-2)) — recent parity history
from collections import Counter
ctx = Counter(); hit = Counter()
for n in range(2, N):
    key = (r_orb[n-1], r_orb[n-2])
    ctx[key] += 1; hit[key] += d[n]
print(f"\n  P(d=1 | recent parity history) -- uniform 0.5 means no handle:")
for key in sorted(ctx):
    p = hit[key]/ctx[key]
    print(f"    history {key}: P(d=1)={p:.4f}  (n={ctx[key]})")

# SHUFFLE-NULL: shuffle d deterministically (reverse + interleave) and recompute corr(r_orb, r_pure-like)
# control that the measured corr(r_orb,r_pure) is real, not an artifact of marginals.
# Build a deterministic permutation of r_pure and re-correlate.
r_pure_perm = r_pure[::-1]
print(f"\nshuffle control: corr(r_orb, reversed r_pure) = {corr(r_orb, r_pure_perm):+.5f}  (should be ~null)")

# block-wise significance: is the marginal corr(r_orb,r_pure) consistent (real) or sign-flipping (noise)?
B = 5
blk = N // B
print(f"\nblock-wise corr(r_orb,r_pure) ({B} blocks of {blk}; null std/block ~ {1/math.sqrt(blk):.4f}):")
signs = []
for i in range(B):
    a = r_orb[i*blk:(i+1)*blk]; b = r_pure[i*blk:(i+1)*blk]
    cb = corr(a, b); signs.append(cb)
    print(f"    block {i}: corr = {cb:+.5f}")
consistent = all(s > 0 for s in signs) or all(s < 0 for s in signs)
print(f"    consistent sign across blocks: {consistent}  -> {'possible real (weak) signal' if consistent else 'sign-flips = NOISE'}")

print("\n" + "="*78)
print("READING (filled by the numbers above):")
print("="*78)
co = corr(r_orb, r_pure)
if abs(co) > 5*nullstd:
    print(f"corr(r_orb,r_pure)={co:+.4f} >> null: the D-S-controllable pure-power digit LEAKS onto the")
    print("orbit parity -- a potential crack: Subspace control of 3^n may transfer PARTIALLY. INVESTIGATE.")
else:
    print(f"corr(r_orb,r_pure)={co:+.4f} ~ null: the pure-power digit (D-S/Subspace-controllable) is")
    print("DECORRELATED from the orbit parity. The T_n feedback fully scrambles the controllable part;")
    print("the wall is exactly the carry correction d, which behaves as an independent fair coin (check")
    print("its autocorr/history table above). => no leakage from D-S; T_n is a genuinely new object.")
