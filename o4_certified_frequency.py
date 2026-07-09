#!/usr/bin/env python3
"""
o4_certified_frequency.py -- port the campaign's certified-induction / sub-action
technique to the FREQUENCY axis of o4 (2026-07-10).

The template method decided o4's STRUCTURE (config C(k) -> C(k+2) for all k, finite
base + 2-step induction).  The coboundary LP (O4_COBOUNDARY_LP_2026-07-08) decided
the LEDGER potential psi = {1:+1, 2:-4, 0:-6}: max-mean cycle = +1, extremal object
the delta_{-14} self-loop.  Neither was ever applied to the FATAL FREQUENCY functional
itself:  freq{3 | W_n} = #1/n = (1/n) #{ j<n : rho_j = 1 },  fatal <=> freq >= 4/5
(O4_NEWMATH_BUILD_2026-07-09 sec.1).

This script asks: can a FINITE certified computation on the reload map's finite
quotients B(3,k) bootstrap to an eventual frequency bound  freq <= 4/5 - eps,
deciding o4?  The frequency sub-action LP is

    1{rho=1}(G) <= phi(T(G) mod 3^k) - phi(G mod 3^k) + c   for ALL integers G,

with min feasible c = max-mean cycle of B(3,k) under the FREQUENCY weight
    w_freq(edge) = 1{ source window's rho_0 = 1 }.
Telescoping then gives  freq <= c + o(1)  for EVERY orbit.

KEY COMPUTATION (task item 2): the exact B(3,k) max-mean-cycle bound, k = 1..6.
Does it improve toward a decision (< 4/5) as k grows, or plateau above 4/5?

Everything exact (int / Fraction); every claim assertion-checked; no floats in any
proof path.  Interpreter: /Users/aokiyousuke/quantum-ecc/.venv/bin/python
"""
from fractions import Fraction
from collections import deque

# ------- o4 odometer (identical conventions to o4_coboundary_lp.py) -------------
E     = {0: 9, 1: 14, 2: 1}          # 3G' = 4G + e(G mod 3)
DELTA = {1: -1, 2: 4, 0: 6}          # ledger increments
PSI   = {r: -d for r, d in DELTA.items()}      # ledger potential {0:-6,1:+1,2:-4}
FREQ  = {0: 0, 1: 1, 2: 0}           # FREQUENCY weight = 1{rho=1}  (the fatal functional)
KMAX      = 6
KARP_KMAX = 6


def T(g):
    n = 4 * g + E[g % 3]
    assert n % 3 == 0, g
    return n // 3


def v3(n):
    assert n != 0
    v = 0
    while n % 3 == 0:
        n //= 3
        v += 1
    return v


def itinerary(a, k):
    out = []
    for _ in range(k):
        out.append(a % 3)
        a = T(a)
    return tuple(out)


def max_run_of_ones(word):
    best = cur = 0
    for s in word:
        cur = cur + 1 if s == 1 else 0
        if cur > best:
            best = cur
    return best


def karp_max_mean(n, edges):
    """Exact max mean cycle (Karp, super-source D_0=0).  Fraction, or None."""
    prev = [0] * n
    rows = [prev]
    for _ in range(n):
        cur = [None] * n
        for (u, v, w) in edges:
            pu = prev[u]
            if pu is not None:
                c = pu + w
                if cur[v] is None or c > cur[v]:
                    cur[v] = c
        rows.append(cur)
        prev = cur
    best = None
    Dn = rows[n]
    for v in range(n):
        if Dn[v] is None:
            continue
        mv = None
        for j in range(n):
            Dj = rows[j][v]
            if Dj is None:
                continue
            val = Fraction(Dn[v] - Dj, n - j)
            if mv is None or val < mv:
                mv = val
        if mv is not None and (best is None or mv > best):
            best = mv
    return best


def karp_on_nodeset(nodes, edges):
    order = sorted(nodes)
    idx = {a: i for i, a in enumerate(order)}
    sub = [(idx[u], idx[v], w) for (u, v, w) in edges if u in idx and v in idx]
    return karp_max_mean(len(order), sub)


def is_dag(nodes, edges):
    nodes = set(nodes)
    indeg = {a: 0 for a in nodes}
    adj = {a: [] for a in nodes}
    for (u, v) in edges:
        adj[u].append(v)
        indeg[v] += 1
    q = deque(a for a in nodes if indeg[a] == 0)
    done = 0
    while q:
        u = q.popleft()
        done += 1
        for v in adj[u]:
            indeg[v] -= 1
            if indeg[v] == 0:
                q.append(v)
    return done == len(nodes)


# sanity: -14 is the all-rho=1 integer fixed point
assert T(-14) == -14 and (-14) % 3 == 1
assert FREQ[1] == 1 and FREQ[0] == 0 and FREQ[2] == 0

print("=" * 78)
print("o4 CERTIFIED FREQUENCY BUILD  --  exact, k = 1..%d" % KMAX)
print("frequency weight w = 1{rho=1};  fatal <=> freq{3|W_n} >= 4/5")
print("=" * 78)
print()
print("[1] Unconditional frequency sub-action LP on B(3,k): max-mean cycle")
print("    (min feasible c s.t. 1{rho=1} <= phi(TG)-phi(G)+c for all integers G)")
print()

freq_bounds = []
for k in range(1, KMAX + 1):
    M = 3 ** k
    n14 = (-14) % M

    # level-k de Bruijn graph B(3,k); one edge per lift r mod 3^{k+1}, exact lookahead
    edges_freq = [(r % M, T(r) % M, FREQ[r % 3]) for r in range(3 * M)]
    edgeset = set(edges_freq)

    # the all-rho=1 self-loop at -14 carries weight 1 -> mean-1 cycle exists
    assert (n14, n14, 1) in edgeset
    maxw = max(w for (_, _, w) in edges_freq)
    assert maxw == 1                       # every cycle mean <= 1 (max edge weight)
    lam = Fraction(1)                      # so max-mean = 1 exactly (attained at -14)

    # uniqueness: a mean-1 cycle uses only weight-1 edges = all sources rho=1;
    # remove the -14 loop from the induced weight-1 subgraph -> a DAG (Kahn).
    ones_nodes = [a for a in range(M) if a % 3 == 1]
    ones_edges = [(u, v) for (u, v, w) in edges_freq
                  if w == 1 and v % 3 == 1 and not (u == n14 and v == n14)]
    assert is_dag(ones_nodes, ones_edges)

    if k <= KARP_KMAX:
        assert karp_max_mean(M, edges_freq) == lam      # independent exact algorithm

    freq_bounds.append((k, lam))
    print("  k=%d  |V|=%-5d |E|=%-6d   freq max-mean = %s   "
          "(attained UNIQUELY at delta_{-14}; freq bound = %s >= 4/5)"
          % (k, M, 3 * M, lam, lam))

print()
print("  => the certified frequency bound is  freq <= 1  at EVERY level k = 1..6.")
print("     PLATEAU at 1 (>> 4/5).  Never crosses below 4/5.  Cannot decide o4.")
print()

# ---- [2] Does higher MEMORY help?  A window-m potential = larger k -------------
# The max-mean-cycle LP optimizes over ALL functions phi: Z/3^k -> R, i.e. the
# most general depth-k-memory certificate of ANY functional form (linear OR
# nonlinear in the window indicators -- a degree-d polynomial in the window is
# still just some function on Z/3^k, already in the LP's variable class).  So the
# ONLY genuine lever is memory depth k -- which is exactly the k-sequence above.
print("[2] Memory / nonlinear refinement: the LP already ranges over ALL")
print("    phi: Z/3^k -> R (every depth-k certificate, linear or nonlinear).")
print("    The only lever is depth k; the sequence of bounds is:")
print("      k      :", [k for k, _ in freq_bounds])
print("      bound  :", [str(b) for _, b in freq_bounds])
print("    Constant 1.  No self-improvement.  A degree-2 / window potential is")
print("    subsumed and cannot beat the max-mean cycle at its own depth.")
print()

# Explicit fixed-point obstruction (why NO certificate of any form escapes):
# any phi (bounded or unbounded, any functional form) obeying the sound inequality
# for all integers must obey it at the fixed point G=-14 (T(-14)=-14, rho=1):
#     1 = FREQ[1] <= phi(-14) - phi(-14) + c = c,   so  c >= 1.
print("    Fixed-point obstruction (holds for phi of ANY form, bounded/unbounded):")
print("    at G=-14 (T(-14)=-14, rho=1):  1 <= phi(-14)-phi(-14)+c = c  =>  c >= 1.")
print("    The delta_{-14} orbit is a GENUINE integer orbit with freq == 1; any")
print("    sound certificate must dominate it. Excluding it = the seed's quenched")
print("    avoidance of the -14 shadow cylinders = (K).")
print()

# ---- [3] Conditional run-restricted frequency ladder --------------------------
# The ONLY way the bound drops below 4/5 is an EXTERNAL hypothesis bounding the
# rho=1 run length.  On the subshift {all rho=1 runs <= R}, max-mean freq cycle:
print("[3] Run-restricted frequency ladder at k=6 (subshift: all rho=1 runs <= R).")
print("    This is the CONDITIONAL object (hypothesis: eventual run bound R).")
k = 6
M = 3 ** k
edges_freq = [(r % M, T(r) % M, FREQ[r % 3]) for r in range(3 * M)]
edges_psi  = [(r % M, T(r) % M, PSI[r % 3])  for r in range(3 * M)]
win = {a: itinerary(a, k) for a in range(M)}
print()
print("    R  | freq max-mean | ledger max-mean | freq vs 4/5     | decides o4?")
print("    ---+---------------+-----------------+-----------------+------------")
for R in range(1, 6):
    nodes = [a for a in range(M) if max_run_of_ones(win[a]) <= R]
    lam_f = karp_on_nodeset(nodes, edges_freq)
    lam_p = karp_on_nodeset(nodes, edges_psi)
    # exact laws: freq -> R/(R+1) via word 1^R 2 ; ledger -> (R-4)/(R+1)
    assert lam_f == Fraction(R, R + 1), (R, lam_f)
    assert lam_p == Fraction(R - 4, R + 1), (R, lam_p)
    # affine cross-check on the rho=2-filler extremal cycle: ledger = 5*freq - 4
    assert lam_p == 5 * lam_f - 4
    below = lam_f < Fraction(4, 5)
    decides = "YES (< 4/5)" if below else ("critical" if lam_f == Fraction(4, 5) else "no")
    rel = ("%s < 4/5" % lam_f) if below else (("%s = 4/5" % lam_f) if lam_f == Fraction(4, 5)
                                              else "%s > 4/5" % lam_f)
    print("    %d  | %11s   | %13s   | %-15s | %s"
          % (R, lam_f, lam_p, rel, decides))
print()
print("    freq max-mean = R/(R+1) EXACTLY:  crosses 4/5 at R=4 (critical); R<=3 decides.")
print("    ledger max-mean = (R-4)/(R+1):    same threshold, related by 5*freq-4.")
print("    But raising the WINDOW k at fixed R does NOT lower R/(R+1):")
for R in (2, 3):
    seq = []
    for kk in range(R + 1, 7):
        MM = 3 ** kk
        ef = [(r % MM, T(r) % MM, FREQ[r % 3]) for r in range(3 * MM)]
        wn = {a: itinerary(a, kk) for a in range(MM)}
        nd = [a for a in range(MM) if max_run_of_ones(wn[a]) <= R]
        seq.append((kk, karp_on_nodeset(nd, ef)))
    assert all(v == Fraction(R, R + 1) for _, v in seq)
    print("      R=%d, k=%d..6 : %s  (k-independent plateau)"
          % (R, R + 1, [str(v) for _, v in seq]))
print()
print("    => self-improvement is only in R (the OPEN run bound), never in k.")
print("       The unconditional bound (R = infinity, the real orbit's a-priori")
print("       situation) is R/(R+1) -> 1: the plateau of [1].")
print()

print("=" * 78)
print("ALL ASSERTIONS PASSED (exact arithmetic; no floats in any proof path).")
print("VERDICT: frequency sub-action LP on B(3,k) plateaus at 1 for every k=1..6;")
print("the certified-induction technique CANNOT decide o4 on the frequency axis.")
print("The extremal delta_{-14} cycle (freq=1) is a genuine invariant the finite")
print("certificate always sees; excluding it is the seed's quenched avoidance = (K).")
print("No machine decided. No label upgraded.")
print("=" * 78)
