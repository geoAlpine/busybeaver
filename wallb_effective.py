"""WALL (B) EFFECTIVE finite-certification probe.

Question: does the SPECIFIC Antihydra orbit admit a SELF-IMPROVING / bootstrapping effective
discrepancy bound -- "if D_N <= f(N) for N<=N0 (finite check) then D_N <= g(N) for all N, g->0" --
or does any such bound reduce to equidistribution (= wall B / line (5))?

We compute, with EXACT integer arithmetic (no float drift), the two relevant deviations of the orbit:
  theta_n = {4 (3/2)^n} = (8*3^n mod 2^{n+1}) / 2^{n+1}        (the explicit a_n half; = wall B point)
  a_n     = bit_n(8*3^n) = 1[theta_n >= 1/2]                    (the parity's explicit half)
and measure:
  (1) star-discrepancy D*_N of (theta_n) vs N -> fit the rate.
  (2) the even/upper-half frequency deviation |F_N - 1/2|, F_N = (1/N) sum a_n -> fit the rate.
  (3) SELF-IMPROVEMENT TEST: ratio R(N)=D*_N / D*_{N/2}.  Pure CLT/equidistribution rate D~N^{-1/2}
      gives R -> 2^{-1/2}=0.7071 CONSTANT (no contraction). A genuine bootstrap would give R<0.707
      and DECREASING (head certifies tail with a contraction factor).
  (4) HEAD-CERTIFIES-TAIL TEST: does the first half [0,N/2) carry predictive information about the
      DISCREPANCY CONSTANT of the disjoint tail window [N/2,N)? We compute the tail-window star-
      discrepancy normalized by sqrt(window), across growing N, and its correlation with the head's.
      Zero leverage (stationary normalized tail constant, ~0 correlation) => no self-improvement,
      the tail is certified only by equidistribution itself.

0 false proofs: pure measurement + exact arithmetic. Conclusions are argued and labelled.
"""
import math

NMAX = 1 << 17          # 131072
GUARD = 16              # keep modulus 2^{n+1+GUARD} so bit_n is exact

# exact theta_n via incremental modular powering: t ~ 8*3^n mod 2^{n+1+GUARD}
thetas = [0.0] * NMAX
abits  = [0]   * NMAX
t = 8 % (1 << (1 + GUARD))   # n=0: 8*3^0=8
for n in range(NMAX):
    mod_lo = 1 << (n + 1)              # for theta_n we need bits 0..n  -> mod 2^{n+1}
    low = t & (mod_lo - 1)
    thetas[n] = low / mod_lo
    abits[n] = (t >> n) & 1
    # advance to n+1: modulus grows to 2^{(n+1)+1+GUARD}
    newmod = 1 << ((n + 1) + 1 + GUARD)
    t = (3 * t) % newmod

def star_disc(points):
    """star-discrepancy of a list in [0,1) via sorted formula."""
    pts = sorted(points)
    N = len(pts)
    D = 0.0
    for i, x in enumerate(pts):
        D = max(D, abs((i + 1) / N - x), abs(i / N - x))
    return D

print("="*78)
print("(1) star-discrepancy D*_N of theta_n = {4(3/2)^n}, and rate fit")
print("="*78)
checkN = [1000, 2000, 4000, 8000, 16000, 32000, 65536, 131072]
discs = {}
print(f"{'N':>8} {'D*_N':>12} {'-log2 D*':>10} {'D*/N^-0.5':>12}")
for N in checkN:
    D = star_disc(thetas[:N])
    discs[N] = D
    print(f"{N:>8} {D:>12.6f} {-math.log2(D):>10.3f} {D/N**-0.5:>12.4f}")
# slope fit
import statistics
xs = [math.log(N) for N in checkN]
ys = [math.log(discs[N]) for N in checkN]
n = len(xs); sx=sum(xs); sy=sum(ys); sxx=sum(x*x for x in xs); sxy=sum(x*y for x,y in zip(xs,ys))
slope = (n*sxy - sx*sy)/(n*sxx - sx*sx)
print(f"  => log-log slope of D*_N ~ N^slope : slope = {slope:.4f}  (CLT/equidist = -0.5)")

print("\n" + "="*78)
print("(2) upper-half frequency deviation |F_N - 1/2|, F_N = mean(a_n)")
print("="*78)
pre = [0]*(NMAX+1)
for i in range(NMAX): pre[i+1] = pre[i] + abits[i]
fdev = {}
print(f"{'N':>8} {'F_N':>10} {'|F_N-1/2|':>12} {'*sqrt(N)':>10}")
for N in checkN:
    F = pre[N]/N
    d = abs(F - 0.5)
    fdev[N] = d
    print(f"{N:>8} {F:>10.5f} {d:>12.6f} {d*math.sqrt(N):>10.4f}")
ys2 = [math.log(fdev[N]) for N in checkN]
sxy2 = sum(x*y for x,y in zip(xs,ys2)); sy2=sum(ys2)
slope2 = (n*sxy2 - sx*sy2)/(n*sxx - sx*sx)
print(f"  => log-log slope of |F_N-1/2| ~ N^slope : slope = {slope2:.4f}  (CLT = -0.5)")

print("\n" + "="*78)
print("(3) SELF-IMPROVEMENT TEST: R(N) = D*_N / D*_{N/2}")
print("   pure equidistribution (D~N^-0.5) => R -> 0.7071 CONSTANT (NO contraction).")
print("   genuine bootstrap => R < 0.707 and DECREASING.")
print("="*78)
print(f"{'N':>8} {'D*_{N/2}':>12} {'D*_N':>12} {'R(N)':>10}")
seq = [2048, 4096, 8192, 16384, 32768, 65536, 131072]
for N in seq:
    Dh = star_disc(thetas[:N//2])
    Df = star_disc(thetas[:N])
    print(f"{N:>8} {Dh:>12.6f} {Df:>12.6f} {Df/Dh:>10.4f}")

print("\n" + "="*78)
print("(4) HEAD-CERTIFIES-TAIL TEST")
print("   tail window [N/2,N) standalone star-discrepancy, normalized by sqrt(window).")
print("   stationary normalized value across N => tail certified only by equidistribution,")
print("   head gives NO leverage (no self-improvement). Also corr(head_norm, tail_norm).")
print("="*78)
print(f"{'N':>8} {'head*sqrt':>11} {'tail*sqrt':>11}  (normalized star-disc, window=N/2)")
heads=[]; tails=[]
for N in seq:
    h = N//2
    Dhead = star_disc(thetas[:h]) * math.sqrt(h)
    Dtail = star_disc(thetas[h:N]) * math.sqrt(N-h)
    heads.append(Dhead); tails.append(Dtail)
    print(f"{N:>8} {Dhead:>11.4f} {Dtail:>11.4f}")
# correlation
if len(heads) > 2:
    mh=statistics.mean(heads); mt=statistics.mean(tails)
    cov=sum((a-mh)*(b-mt) for a,b in zip(heads,tails))/len(heads)
    sh=statistics.pstdev(heads); st=statistics.pstdev(tails)
    corr = cov/(sh*st) if sh>0 and st>0 else float('nan')
    print(f"  normalized tail constant: mean={statistics.mean(tails):.4f} stdev={st:.4f} (stationary?)")
    print(f"  corr(head_norm, tail_norm) = {corr:+.4f}  (~0 => head gives no leverage on tail)")

print("\n" + "="*78)
print("(5) CONTROL: same statistics for a genuinely random sequence (uniform iid), same N")
print("    to confirm the orbit's numbers ARE the generic equidistribution numbers (no anomaly).")
print("="*78)
import random
random.seed(12345)
rnd = [random.random() for _ in range(NMAX)]
print(f"{'N':>8} {'orbit D*':>12} {'random D*':>12}")
for N in checkN:
    print(f"{N:>8} {discs[N]:>12.6f} {star_disc(rnd[:N]):>12.6f}")
print("\nDONE.")
