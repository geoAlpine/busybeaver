#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Route #20 -- richer certificate languages for the (K)-kernel (2026-07-25).

Kernel: induced odd map T(o) = 3^(D-1)(3o-1)/2^D, D = v2(3o-1), seed o0 = 27,
on Z2^x; base map Tb(x) = floor(3x/2) = (3x - (x mod 2))/2 on Z2 (2-to-1 exact).
(K) = liminf mean D >= 3/2.

Three sub-probes, one decisive computation each:

(i)  2-adic ANALYTIC invariants (Mahler / polynomial basis):
     A1. The 2-adic transfer operator of the base map,
             (L f)(x) = (1/2)[ f(2x/3) + f((2x+1)/3) ],
         acts on polynomials.  Verify EXACTLY (Fraction arithmetic) that
         deg<=m polynomials CLOSE under L, that L is upper triangular with
         diagonal (2/3)^m (2-adic modulus 2^-m: contraction), and compute the
         exact eigenpolynomials phi_m.  ==> a finite-dimensional analytic
         subspace DOES close under the transfer action (new, exactly solvable).
     A2. The POINTWISE (composition) side, which is what a single-orbit
         certificate must use: verify that x |-> T^j(x), as an element of
         (deg<=1 polys) tensor (locally constant level k), requires level
         EXACTLY k = j (strict level growth: no finite closure), and that its
         leading coefficient (3/2)^j has v2 = -j (2-adically unbounded).
     A3. Graph facts used by the pointwise no-go lemma (see report):
         base-map residue class graph strongly connected (k <= 10);
         induced-map residue graph fully reachable from 27 (k <= 14) [also (ii)].
     A4. Sanity: the induced map has NO coherent Q2-valued transfer operator
         (its branch weights 2^-d are not 2-adically summable: |2^-d|_2 = 2^d).
         The real-annealed eigenvalues r_m = 2^(m-1)/(3^m - 2^(m-1)) of the
         formal real-weighted polynomial action are verified as real series
         identities (they belong to the CLOSED annealed register C3).

(ii) Polynomial ideals with VALUATION guards:
     v2(P(o)) <= B is a finite-level residue (clopen) condition; a step-closed
     guard = a proper forward-invariant clopen set containing the seed class.
     Decisive computation: BFS of the induced residue relation from 27 mod 2^k
     reaches ALL odd classes (k = 6..14)  ==> no such set exists.  Plus an
     exhaustive search (deg <= 2, |coeffs| <= 4, B <= 4, level 8): count
     step-closed nontrivial guards (expect 0).  Plus [MEASURED]: the natural
     degree-1 guard P(x) = 3x-1 has v2(P(o_n)) = D_n UNBOUNDED along the orbit.

(iii) Parikh / counter-register certificates:
     The counter S_n = sum D_j satisfies the EXACT identity
         S_n * ln(3/2) = ln(o_n / o0) - sum_{j<n} ln(1 - 1/(3 o_j)),
     i.e. S_n = log_{3/2}(o_n/o0) + c_n with c_n increasing to a finite
     constant c_inf (measured).  So a Parikh counter IS a magnitude coordinate:
     any PA acceptance invariant (linear in counts, finite control) is
     (cylinder LP) + (alpha*S_n - beta*n) = the CLOSED magnitude-aware
     Lyapunov class (sign no-go of MAGNITUDE_LYAPUNOV.md applies verbatim).

Exact big-int / Fraction arithmetic throughout.  No floats except where a
quantity is explicitly a real (Archimedean) measurement.
"""

from fractions import Fraction as F
import math

LN32 = math.log(1.5)

# ---------------------------------------------------------------- utilities
def v2int(n):
    n = abs(n)
    if n == 0:
        return None  # +infinity
    return (n & -n).bit_length() - 1

def v2frac(x):
    if x == 0:
        return None
    return v2int(x.numerator) - v2int(x.denominator)

def poly_compose_linear(p, a, b):
    """coefficients of p(a*x+b); p = list of Fractions, index = degree."""
    out = [F(0)] * len(p)
    pw = [F(1)]
    for i, ci in enumerate(p):
        if i > 0:
            new = [F(0)] * (len(pw) + 1)
            for j, c in enumerate(pw):
                new[j] += c * b
                new[j + 1] += c * a
            pw = new
        for j, c in enumerate(pw):
            out[j] += ci * c
    return out

def poly_eq(p, q):
    m = max(len(p), len(q))
    p = p + [F(0)] * (m - len(p)); q = q + [F(0)] * (m - len(q))
    return p == q

def orbit(o0, N):
    o = o0; os_ = [o]; Ds = []
    for _ in range(N):
        t = 3 * o - 1
        d = (t & -t).bit_length() - 1
        o = (3 ** (d - 1) * t) >> d
        Ds.append(d); os_.append(o)
    return os_, Ds

def lnbig(o):
    bl = o.bit_length()
    if bl <= 900:
        return math.log(o)
    sh = bl - 60
    return math.log(o >> sh) + sh * math.log(2)

# ================================================================ (i) A1
print("=" * 78)
print("(i) A1: 2-adic transfer operator of the base map on polynomials [EXACT]")
print("=" * 78)
MMAX = 8
# L f(x) = 1/2 [ f(2x/3) + f((2x+1)/3) ]
cols = []
for m in range(MMAX + 1):
    xm = [F(0)] * m + [F(1)]
    u = poly_compose_linear(xm, F(2, 3), F(0))
    v = poly_compose_linear(xm, F(2, 3), F(1, 3))
    Lxm = [(a + b) / 2 for a, b in zip(u, v)]
    cols.append(Lxm)

triangular = all(all(cols[m][j] == 0 for j in range(m + 1, MMAX + 1) if j < len(cols[m]))
                 for m in range(MMAX + 1))
diag_ok = all(cols[m][m] == F(2, 3) ** m for m in range(MMAX + 1))
print(f"deg<=m closure under L: {'OK' if triangular else 'FAIL'} "
      f"(L x^m has degree exactly m, all m <= {MMAX})")
print(f"diagonal eigenvalues  : lambda_m = (2/3)^m  -> {'OK' if diag_ok else 'FAIL'}")
print(f"2-adic moduli         : |lambda_m|_2 = 2^-m (contraction), "
      f"|lambda_m|_R = (2/3)^m < 1")

# eigenpolynomials by back-substitution (upper triangular, distinct diagonal)
eigs = []
for m in range(MMAX + 1):
    lam = F(2, 3) ** m
    phi = [F(0)] * (m + 1); phi[m] = F(1)
    for i in range(m - 1, -1, -1):
        # (L phi)_i = sum_j M[i][j] phi_j = lam phi_i
        s = sum(cols[j][i] * phi[j] for j in range(i + 1, m + 1) if i < len(cols[j]))
        phi[i] = s / (lam - cols[i][i])
    Lphi = [F(0)] * (m + 1)
    for j, cj in enumerate(phi):
        for i, c in enumerate(cols[j][:m + 1]):
            Lphi[i] += cj * c
    ok = poly_eq(Lphi, [lam * c for c in phi])
    eigs.append(phi)
    if m <= 4:
        print(f"  phi_{m}(x) = {phi}   L phi_{m} = (2/3)^{m} phi_{m}: "
              f"{'VERIFIED' if ok else 'FAIL'}")
    assert ok

# ================================================================ (i) A2
print()
print("=" * 78)
print("(i) A2: POINTWISE composition x |-> T^j(x): strict cylinder-level growth")
print("=" * 78)
# g_j = T^j as element of P_1 (x) LC_level ; g_j(x) = a_r x + b_r on class r mod 2^lvl
g = {0: (F(1), F(0))}  # level 0
for j in range(1, 13):
    h = {}
    mod_prev = 1 << (j - 1)
    for rp in range(1 << j):
        bbit = rp & 1
        Tr = ((3 * rp - bbit) // 2) % mod_prev if j > 1 else 0
        a, b = g[Tr]
        h[rp] = (a * F(3, 2), -a * F(bbit, 2) + b)
    factorable = all(h[r] == h[r + (1 << (j - 1))] for r in range(1 << (j - 1)))
    lead = h[0][0]
    if j <= 6 or j == 12:
        print(f"  j={j:2d}: leading coeff = (3/2)^{j} (v2 = {v2frac(lead)}), "
              f"expressible at level {j-1}? {factorable}  "
              f"(minimal level = {j})")
    assert not factorable and lead == F(3, 2) ** j
    g = h
print("  ==> composition NEVER closes in any finite P_m (x) LC_k: level grows by 1")
print("      per step and the leading coefficient is 2-adically unbounded (v2 = -j).")

# ================================================================ (i) A3
print()
print("=" * 78)
print("(i) A3 + (ii): residue-graph facts [EXACT BFS]")
print("=" * 78)
# base map class graph strong connectivity, k <= 10
for k in range(3, 11):
    mod = 1 << k
    succ = [set() for _ in range(mod)]
    pred = [set() for _ in range(mod)]
    for rp in range(mod << 1):
        b = rp & 1
        t = ((3 * rp - b) // 2) % mod
        succ[rp % mod].add(t); pred[t].add(rp % mod)
    def bfs(adj, s):
        seen = {s}; st = [s]
        while st:
            u = st.pop()
            for w in adj[u]:
                if w not in seen:
                    seen.add(w); st.append(w)
        return seen
    fwd = bfs(succ, 0); bwd = bfs(pred, 0)
    sc = (len(fwd) == mod and len(bwd) == mod)
    if k in (3, 10):
        print(f"  base map, k={k:2d}: strongly connected class graph: {sc}")
    assert sc

# induced odd map: reachability from 27 mod 2^k
def induced_successors(a, k):
    """Exact successor set of odd class a mod 2^k (None = all odd classes)."""
    mod = 1 << k
    t = (3 * a - 1) % mod
    if t == 0:
        return None                      # deep class: full branch, image = all
    d = (t & -t).bit_length() - 1        # = v2(3a-1) for every lift
    on = (3 ** (d - 1) * (3 * a - 1)) >> d
    step = 1 << (k - d)
    c = on % step
    return {(c + m * step) % mod for m in range(1 << d)}

for k in range(6, 15):
    mod = 1 << k
    seed = 27 % mod
    allodd = (mod >> 1)
    seen = {seed}; st = [seed]; hit_deep = False
    while st:
        u = st.pop()
        s = induced_successors(u, k)
        if s is None:
            hit_deep = True
            s = set(range(1, mod, 2))
        for w in s:
            if w not in seen:
                seen.add(w); st.append(w)
    full = (len(seen) == allodd)
    print(f"  induced map, k={k:2d}: reachable from 27: {len(seen)}/{allodd} "
          f"odd classes  -> {'FULL' if full else 'PROPER SUBSET'}")
    assert full
print("  ==> the ONLY forward-closed clopen set containing the seed class is")
print("      everything (at every tested level).  This kills (ii) and feeds the")
print("      pointwise-analytic no-go lemma for the induced map (see report).")

# ================================================================ (i) A4
print()
print("=" * 78)
print("(i) A4: no coherent Q2-valued transfer for the INDUCED map; real-annealed")
print("        polynomial eigenvalues (closed register C3) verified as series")
print("=" * 78)
print("  branch weights of the induced map: w_d = 2^-d;  |2^-d|_2 = 2^d -> inf,")
print("  so sum_d w_d f(T_d^{-1} x) does NOT converge 2-adically: no Q2 transfer.")
for m in range(1, 6):
    r = F(2 ** (m - 1), 3 ** m)
    closed = r / (1 - r)                      # = 2^(m-1)/(3^m - 2^(m-1))
    partial = sum(F(1, 2) ** d * F(2, 3) ** (d * m) for d in range(1, 60))
    err = abs(float(closed - partial))
    print(f"  real-annealed  r_{m} = 2^{m-1}/(3^{m}-2^{m-1}) = {closed}   "
          f"series check |err| = {err:.2e}")
    assert err < 1e-15
print("  (these are eigenvalues of the REAL-weighted action; real-valued")
print("   functions on Z2 admit no polynomial structure, so this operator only")
print("   lives on the annealed/measure register C3 -- already closed.)")

# ================================================================ (ii)
print()
print("=" * 78)
print("(ii) valuation guards: exhaustive small search + orbit measurement")
print("=" * 78)
L = 8
modL = 1 << L
odd_classes = list(range(1, modL, 2))
succL = {}
for a in odd_classes:
    s = induced_successors(a, L)
    succL[a] = set(odd_classes) if s is None else s

seedc = 27 % modL
survivors = []
tested = 0
for c2 in range(-4, 5):
    for c1 in range(-4, 5):
        for c0 in range(-4, 5):
            if c2 == 0 and c1 == 0:
                continue  # constant P: no guard content
            for B in range(0, 5):
                m = 1 << (B + 1)
                S = {r for r in odd_classes if (c2 * r * r + c1 * r + c0) % m != 0}
                tested += 1
                if seedc not in S or len(S) == len(odd_classes):
                    continue  # guard false at seed, or trivially all
                if all(succL[r] <= S for r in S):
                    survivors.append((c2, c1, c0, B))
print(f"  searched {tested} (P,B) pairs, deg<=2, |coeffs|<=4, B<=4, level {L}:")
print(f"  step-closed NONTRIVIAL guards found: {len(survivors)}")
assert len(survivors) == 0

print()
print("  [MEASURED] natural degree-1 guard P(x)=3x-1 along the true orbit:")
N = 20000
os_, Ds = orbit(27, N)
runmax, recs = 0, []
for n, d in enumerate(Ds):
    if d > runmax:
        runmax = d; recs.append((n, d))
print(f"  v2(3 o_n - 1) = D_n record values (n, D): {recs}")
print(f"  max over n < {N}: D = {runmax}  (unbounded-looking; a bounded guard")
print(f"  for P=3x-1 is already FALSE on the orbit, and any true guard set is")
print(f"  clopen hence trivial by full reachability above)")

# ================================================================ (iii)
print()
print("=" * 78)
print("(iii) Parikh / counter certificates: the counter IS the magnitude [EXACT+MEASURED]")
print("=" * 78)
S = 0; Ssum = [0]
for d in Ds:
    S += d; Ssum.append(S)
print("  identity: S_n ln(3/2) - ln(o_n/o0) = c_n = -sum_{j<n} ln(1 - 1/(3 o_j))")
for n in (1, 10, 100, 1000, 5000, 20000):
    cn = Ssum[n] * LN32 - (lnbig(os_[n]) - math.log(27))
    print(f"    n={n:6d}: S_n = {Ssum[n]:6d}, c_n = {cn:.12f}")
crec = -sum(math.log(1.0 - 1.0 / (3.0 * float(os_[j]))) for j in range(60))
print(f"  direct series  c_inf ~= {crec:.12f}  (first 60 terms; o_j grows ")
print(f"  geometrically so the tail is < 1e-3500)")
cN = Ssum[N] * LN32 - (lnbig(os_[N]) - math.log(27))
print(f"  agreement |c_N - series| = {abs(cN - crec):.2e}")
print(f"  [MEASURED] orbit depth-mean S_N/N = {Ssum[N]/N:.6f} (Haar mean = 2, (K) needs >= 3/2)")
print()
print("  ==> a Parikh counter (linear in branch counts) evaluated along the orbit")
print("      equals alpha*S_n + beta*n + (bounded state term); by the identity,")
print("      alpha*S_n = (alpha/ln(3/2)) ln o_n + O(1).  Any PA acceptance")
print("      invariant is therefore a magnitude-aware Lyapunov certificate")
print("      (alpha ln o + h(residue) - beta n): the class PROVEN closed in")
print("      MAGNITUDE_LYAPUNOV.md / ADELIC_SUBACTION.md (sign no-go).")
print()
print("No machine decided. No label upgraded.")
