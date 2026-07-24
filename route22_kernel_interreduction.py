#!/usr/bin/env python3
"""
route22_kernel_interreduction.py  (BB6 x2, 2026-07-25)

KERNEL INTER-REDUCTION TEST: would proving the mu=3/2 (p=2) Mahler kernel settle the
mu=8/3 (p=3) kernel, or vice versa?  T1(c)=floor(3c/2) [Antihydra/o10-inner, seed 8],
T2(x)=floor(8x/3) [o15/o18].

Parts (all exact big-int; controls included):
  A  multiplicative independence of {3/2, 8/3}; exponent-lattice index in <x2,x3>;
     exact composite identities (3/2)(8/3)=4, (3/2)^2(8/3)=6, (3/2)^3(8/3)=9;
     lambda = log(8/3)/log(3/2) irrational + continued-fraction linear-form table
     (constrains where two cross-family orbits could share a SECOND value).
  B  consecutive-tracking scan: is T1^k(x)=T2(x) or T2^k(x)=T1(x) ever? (Lemma says
     no for x>=5; scan verifies incl. small x.)
  C  cross-family exact value coincidences, seeds 2..200 both families, values<=1e36,
     vs 20-trial jittered-floor random control; per-pair max shared count; 3-smooth
     accounting; o18-exact variant floor(8x/3)+2 as an extra row.
  D  statement-level digit-string cross-correlation: parity of T1-orbit(8) vs mod-3
     digit of T2-orbit(10), value-scale-matched, chi2 + permutation test, lags -5..5;
     PRNG control.
  E  commutation-defect: T1(T2 x)-4x, T2(T1 x)-4x, T1^2(T2 x)-6x, T1^3(T2 x)-9x —
     exact bounded defects, residue-class structure mod 6/mod 18 (the rank-2 relation
     IS visible for COMPOSITES; neither kernel orbit ever composes the two maps).

Discipline: every printed claim labeled; no label upgraded by this script.
"""
import math, random
from fractions import Fraction
from collections import Counter, defaultdict

L1 = math.log(Fraction(3, 2))
L2 = math.log(Fraction(8, 3))

def T1(x): return (3 * x) // 2
def T2(x): return (8 * x) // 3
def T2b(x): return (8 * x) // 3 + 2   # o18 exact width law (epochs 1..7)

# ---------------------------------------------------------------- A
def part_A():
    print("=" * 78)
    print("A. MULTIPLICATIVE INDEPENDENCE + LATTICE POSITION IN THE RANK-2 HOST")
    for a in range(-8, 9):
        for b in range(-8, 9):
            if (a, b) != (0, 0):
                assert Fraction(3, 2) ** a * Fraction(8, 3) ** b != 1
    print("  (3/2)^a (8/3)^b = 2^(3b-a) 3^(a-b) = 1  =>  a=b=0   [PROVEN, exhaustive |a|,|b|<=8")
    print("   + unique factorization: 3b-a=0 & a-b=0 => a=b=0]")
    # exponent lattice in (e2,e3): (3/2)->(-1,1), (8/3)->(3,-1)
    det = (-1) * (-1) - (1) * (3)
    print("  exponent-lattice det[(-1,1),(3,-1)] = %d  => <x3/2, x8/3> has INDEX 2" % det)
    print("  in <x2,x3> ~= Z^2; sublattice = {2^i 3^j : i+j even}   [PROVEN]")
    assert Fraction(3, 2) * Fraction(8, 3) == 4
    assert Fraction(3, 2) ** 2 * Fraction(8, 3) == 6
    assert Fraction(3, 2) ** 3 * Fraction(8, 3) == 9
    print("  exact: (3/2)(8/3)=4   (3/2)^2(8/3)=6   (3/2)^3(8/3)=9   [PROVEN]")
    print("  => the pair GENERATES a rank-2 nonlacunary group (contains x4 and x9).")
    lam = L2 / L1
    print("  lambda = log(8/3)/log(3/2) = %.9f ; rational lambda=p/q would force" % lam)
    print("  (8/3)^q=(3/2)^p, killed above => lambda IRRATIONAL  [PROVEN]")
    # continued fraction + linear-form table
    cf, x = [], lam
    for _ in range(10):
        a0 = int(x); cf.append(a0); x = 1 / (x - a0)
    print("  cf(lambda) =", cf)
    ps, qs = [0, 1], [1, 0]
    print("  necessary condition for two cross-family shared values v<w at step gap")
    print("  (k T1-steps, l T2-steps): |k L1 - l L2| < log(v/(v-1))   [PROVEN, growth]")
    for a0 in cf:
        ps.append(a0 * ps[-1] + ps[-2]); qs.append(a0 * qs[-1] + qs[-2])
        k, l = ps[-1], qs[-1]
        err = abs(k * L1 - l * L2)
        if err == 0: continue
        vmax = 1 / (1 - math.exp(-err))
        print("    (k,l)=(%4d,%4d)  |kL1-lL2|=%.3e  => 2nd shared value needs v <= %.1f"
              % (k, l, err, vmax))

# ---------------------------------------------------------------- B
def part_B(XMAX=200000, KMAX=60):
    print("=" * 78)
    print("B. CONSECUTIVE-TRACKING SCAN (sub-orbit embedding, single step)")
    hits = []
    for x in range(2, XMAX + 1):
        t = T2(x); y = x
        for k in range(1, KMAX):
            y = T1(y)
            if y == t: hits.append(("T1^%d(x)=T2(x)" % k, x)); break
            if y > t: break
        t = T1(x); y = x
        for k in range(1, KMAX):
            y = T2(y)
            if y == t: hits.append(("T2^%d(x)=T1(x)" % k, x)); break
            if y > t: break
    print("  scan x in [2,%d], k<%d:  hits = %s" % (XMAX, KMAX, hits if hits else "NONE"))
    print("  [PROVEN lemma: T1^k(x) in ((3/2)^k (x-1), (3/2)^k x]; since 9/4 < 8/3-eps")
    print("   and 27/8 > 8/3 with relative gaps >=15%%, T1^k(x)=floor(8x/3) impossible")
    print("   for x>=5, any k; T2(x)-floor(3x/2) >= (7x-4)/6 > 0 kills the other")
    print("   direction for ALL x>=1, any k. Scan confirms incl. small x.]")

# ---------------------------------------------------------------- C
def orbit_vals(T, seed, B):
    out, x = [], seed
    while x <= B:
        out.append(x); x = T(x)
    return out

def family_values(T, B, seeds=range(2, 201)):
    vals = {}
    for s in seeds:
        for i, v in enumerate(orbit_vals(T, s, B)):
            vals.setdefault(v, []).append((s, i))
    return vals

def smooth3(n):
    while n % 2 == 0: n //= 2
    while n % 3 == 0: n //= 3
    return n == 1

def coincidence_count(V1, V2, lo=0):
    return sorted(v for v in (set(V1) & set(V2)) if v > lo)

def part_C(B=10 ** 36, NTRIAL=20):
    print("=" * 78)
    print("C. CROSS-FAMILY EXACT VALUE COINCIDENCES  (seeds 2..200, values <= 1e36)")
    V1 = family_values(T1, B)
    V2 = family_values(T2, B)
    common = coincidence_count(V1, V2)
    sm = [v for v in common if smooth3(v)]
    big = [v for v in common if v > 10 ** 6]
    print("  |values T1-family| = %d   |values T2-family| = %d" % (len(V1), len(V2)))
    print("  common values: %d   (3-smooth among them: %d;  >1e6: %d)"
          % (len(common), len(sm), len(big)))
    print("  common values > 1e6:", big[:24], "..." if len(big) > 24 else "")
    # per-orbit-pair shared counts for v>=5
    cnt = Counter()
    for v in common:
        if v < 5: continue
        for (s1, _) in V1[v]:
            for (s2, _) in V2[v]:
                cnt[(s1, s2)] += 1
    mx = cnt.most_common(6)
    print("  max #shared values (v>=5) over single orbit pairs (s1,s2):", mx)
    for (s1, s2), c in mx:
        if c >= 2:
            sh = [v for v in common if v >= 5
                  and any(s == s1 for s, _ in V1[v]) and any(s == s2 for s, _ in V2[v])]
            print("    pair (%d,%d) shares %s" % (s1, s2, sh))
            for u, w in zip(sh, sh[1:]):
                k = [i for s, i in V1[w] if s == s1][0] - [i for s, i in V1[u] if s == s1][0]
                l = [i for s, i in V2[w] if s == s2][0] - [i for s, i in V2[u] if s == s2][0]
                err = abs(k * L1 - l * L2)
                need = math.log(u / (u - 1))
                print("      gap (k,l)=(%d,%d): |kL1-lL2|=%.3e  vs required < %.3e  %s"
                      % (k, l, err, need, "OK(consistent)" if err < need else "VIOLATES?!"))
    # o18-exact variant
    V2v = family_values(T2b, B)
    commonv = coincidence_count(V1, V2v)
    bigv = [v for v in commonv if v > 10 ** 6]
    print("  variant floor(8x/3)+2 (o18 exact): common=%d (>1e6: %d)" % (len(commonv), len(bigv)))
    # control: jittered floor, 20 trials
    ctrl_all, ctrl_big = [], []
    for t in range(NTRIAL):
        def T2r(x, _t=t):
            r = random.Random((_t << 40) ^ x).randrange(2)
            return (8 * x) // 3 + r
        V2r = family_values(T2r, B)
        cc = coincidence_count(V1, V2r)
        ctrl_all.append(len(cc))
        ctrl_big.append(len([v for v in cc if v > 10 ** 6]))
    ma = sum(ctrl_all) / NTRIAL
    sa = (sum((c - ma) ** 2 for c in ctrl_all) / (NTRIAL - 1)) ** 0.5
    mb = sum(ctrl_big) / NTRIAL
    sb = (sum((c - mb) ** 2 for c in ctrl_big) / (NTRIAL - 1)) ** 0.5
    za = (len(common) - ma) / sa if sa > 0 else float("nan")
    zb = (len(big) - mb) / sb if sb > 0 else float("nan")
    print("  CONTROL (jittered floor(8x/3)+{0,1}, %d trials):" % NTRIAL)
    print("    all:  control %.1f +/- %.1f   actual %d   z=%.2f" % (ma, sa, len(common), za))
    print("    >1e6: control %.1f +/- %.1f   actual %d   z=%.2f" % (mb, sb, len(big), zb))
    print("  [MEASURED] verdict row: coincidences chance-level iff |z| < ~2.5")

# ---------------------------------------------------------------- D
def chi2_and_perm(pairs, NPERM=2000, rng_seed=7):
    n = len(pairs)
    obs = Counter(pairs)
    ra = Counter(a for a, _ in pairs)
    rb = Counter(bb for _, bb in pairs)
    def chi2(cnt):
        s = 0.0
        for a in ra:
            for bb in rb:
                e = ra[a] * rb[bb] / n
                d = cnt.get((a, bb), 0) - e
                s += d * d / e
        return s
    c0 = chi2(obs)
    bs = [a for a, _ in pairs]
    ds = [bb for _, bb in pairs]
    rng = random.Random(rng_seed)
    worse = 0
    for _ in range(NPERM):
        rng.shuffle(ds)
        if chi2(Counter(zip(bs, ds))) >= c0:
            worse += 1
    return c0, (worse + 1) / (NPERM + 1)

def part_D(N2=3000):
    print("=" * 78)
    print("D. STATEMENT-LEVEL DIGIT-STRING CROSS-CORRELATION (the two kernel observables)")
    xs = [10]
    for _ in range(N2): xs.append(T2(xs[-1]))
    d = [x % 3 for x in xs]                       # p=3 kernel observable
    N1 = int((N2 * L2 + math.log(10 / 8)) / L1) + 12
    cs = [8]
    for _ in range(N1): cs.append(T1(cs[-1]))
    b = [c & 1 for c in cs]                       # p=2 kernel observable (parity)
    print("  T1-orbit(8) parity: even-density = %.5f over %d terms  [MEASURED]"
          % (1 - sum(b) / len(b), len(b)))
    print("  T2-orbit(10) mod 3: freqs %s over %d terms  [MEASURED]"
          % ({r: round(d.count(r) / len(d), 4) for r in (0, 1, 2)}, len(d)))
    results = []
    for lag in range(-5, 6):
        pairs = []
        for m in range(200, N2):
            n = round((m * L2 + math.log(10 / 8)) / L1) + lag
            if 0 <= n < len(b):
                pairs.append((b[n], d[m]))
        c0, p = chi2_and_perm(pairs, NPERM=500)
        results.append((lag, len(pairs), c0, p))
    best = min(results, key=lambda r: r[3])
    for lag, n, c0, p in results:
        print("    lag %+d: n=%d  chi2(2x3)=%6.2f  perm-p=%.3f%s"
              % (lag, n, c0, p, "   <-- min p" if (lag, n, c0, p) == best else ""))
    print("  Bonferroni over 11 lags: min p=%.3f -> corrected %.3f" % (best[3], min(1, best[3] * 11)))
    # PRNG control
    rng = random.Random(99)
    bp = [rng.randrange(2) for _ in range(len(b))]
    pairs = []
    for m in range(200, N2):
        n = round((m * L2 + math.log(10 / 8)) / L1)
        if 0 <= n < len(bp): pairs.append((bp[n], d[m]))
    c0, p = chi2_and_perm(pairs, NPERM=500)
    print("  CONTROL PRNG-vs-d: chi2=%.2f perm-p=%.3f" % (c0, p))
    print("  [MEASURED] no cross-kernel digit coupling iff corrected p >~ 0.05")

# ---------------------------------------------------------------- E
def part_E(M=10 ** 6):
    print("=" * 78)
    print("E. COMMUTATION DEFECT — the rank-2 relation at composite level")
    tabs = {"T1(T2 x)-4x": defaultdict(set), "T2(T1 x)-4x": defaultdict(set),
            "T1^2(T2 x)-6x": defaultdict(set), "T1^3(T2 x)-9x": defaultdict(set)}
    for x in range(1, M + 1):
        y = T2(x)
        tabs["T1(T2 x)-4x"][x % 6].add(T1(y) - 4 * x)
        tabs["T2(T1 x)-4x"][x % 6].add(T2(T1(x)) - 4 * x)
        tabs["T1^2(T2 x)-6x"][x % 18].add(T1(T1(y)) - 6 * x)
        tabs["T1^3(T2 x)-9x"][x % 18].add(T1(T1(T1(y))) - 9 * x)
    for name, tab in tabs.items():
        allv = sorted(set().union(*tab.values()))
        perres = all(len(v) == 1 for v in tab.values())
        print("  %s: value set %s ; single-valued per residue class: %s"
              % (name, allv, perres))
    print("  [PROVEN by exhaustion to 1e6 + per-residue-affine structure]:")
    print("  composites T1oT2, T1^2oT2, T1^3oT2 = x4, x6, x9 minus a bounded")
    print("  residue-periodic defect — the index-2 rank-2 relation IS exact at")
    print("  composite level. But NEITHER kernel orbit ever composes the two maps:")
    print("  each kernel is a pure power of ONE map. The rank-2 structure lives")
    print("  strictly OFF both orbits.")

if __name__ == "__main__":
    random.seed(20260725)
    part_A()
    part_B()
    part_C()
    part_D()
    part_E()
    print("=" * 78)
    print("No machine decided. No label upgraded.")
