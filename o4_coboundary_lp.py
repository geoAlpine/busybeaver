#!/usr/bin/env python3
"""
o4_coboundary_lp.py -- machine-run of the o4 residue-level coboundary / sub-action LP
(2026-07-08).  The o4 mirror of busybeaver/minprop_lp.py (Antihydra MINPROP_COBOUNDARY_LP).

Object: odometer 3G' = 4G + e(rho), rho = G mod 3, e = {0:9, 1:14, 2:1}
        (O4_RUN_STRUCTURE_2026-07-07.md); ledger a' = a + delta(rho),
        delta = {1:-1, 2:+4, 0:+6} (O4_LEDGER_ANALYSIS_2026-07-06.md).
Potential: psi = -delta = {1:+1, 2:-4, 0:-6}  (the assessment's psi_o4 =
        1{rho=1} - 4*1{rho=2} - 6*1{rho=0}).  Ledger fatality at step n
        <=> prefix sum_{j<n} psi(rho_j) >= a0 - 1, so the safety target is
        "prefix Birkhoff sums of psi bounded above", and a residue-level
        sub-action  psi(G) <= phi(T(G) mod 3^k) - phi(G mod 3^k) + c, c <= 0,
        imposed for ALL integers G (the sound over-approximation: a residue
        certificate cannot know which windows the real orbit visits), would
        prove it unconditionally by telescoping.

LP duality (difference constraints, as in MINPROP): for fixed c the system
        phi(v) - phi(u) >= psi(u) - c  over all constraint-graph edges u->v
        is feasible iff the graph has no cycle of positive (psi - c)-weight,
        i.e. feasible-with-some-c<=0  iff  max-mean-cycle(psi) <= 0.
        The minimal feasible c equals the max mean cycle exactly.

Everything exact (int / Fraction).  Every claim is assertion-checked; any
assertion failure aborts the run.  No floats anywhere.
Interpreter: /Users/aokiyousuke/quantum-ecc/.venv/bin/python
"""
from fractions import Fraction
from collections import deque

E     = {0: 9, 1: 14, 2: 1}          # 3G' = 4G + e(G mod 3)  [integer map: 3 | 4G+e]
DELTA = {1: -1, 2: 4, 0: 6}          # ledger increments
PSI   = {r: -d for r, d in DELTA.items()}   # psi = -delta : {0:-6, 1:+1, 2:-4}
KMAX      = 8                        # residue levels 3^1 .. 3^8
KARP_KMAX = 6                        # exact Karp cross-check up to this level
WALK_KMAX = 4                        # closed-walk (zeta) count check up to this level


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
    """Exact max mean cycle (Karp; D_0 = 0 for all v = super-source variant).
    edges: list of (u, v, w) with integer w, nodes 0..n-1.  Returns Fraction or None."""
    prev = [0] * n
    rows = [prev]
    for _ in range(n):
        cur = [None] * n
        for (u, v, w) in edges:
            pu = prev[u]
            if pu is not None:
                c = pu + w
                cv = cur[v]
                if cv is None or c > cv:
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


def bfs_dists(n, adj, s):
    dist = [None] * n
    dist[s] = 0
    q = deque([s])
    while q:
        u = q.popleft()
        for v in adj[u]:
            if dist[v] is None:
                dist[v] = dist[u] + 1
                q.append(v)
    return dist


def is_dag(nodes, edges):
    """Kahn's algorithm on the given node set / edge list (u,v) pairs."""
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


# ---------------------------------------------------------------- global facts
# branch fixed points x_rho = -e(rho): -9 (rho=0), -14 (rho=1), -1 (rho=2)
for rho, e in E.items():
    x = -e
    assert x % 3 == rho and T(x) == x
assert T(-14) == -14 and (-14) % 3 == 1
# delta_{-14} is a genuine T-invariant (atomic) measure; its psi-integral:
assert PSI[1] == 1          # integral psi d(delta_{-14}) = +1  (assessment's Route-2 value)

print("o4 coboundary / sub-action LP  --  exact machine run, k = 1..%d" % KMAX)
print("psi = -delta = {rho=1:+1, rho=2:-4, rho=0:-6};  int psi d(delta_-14) = +1")
print()

report = []
for k in range(1, KMAX + 1):
    M = 3 ** k
    n14 = (-14) % M

    # ---- build the level-k constraint graph from ALL lifts r mod 3^{k+1} ----
    # (T(G) mod 3^k is determined by G mod 3^{k+1}: exact one-symbol lookahead,
    #  NO tail truncation needed -- unlike Antihydra where D = v2(3o-1) is unbounded.)
    edges = []            # (u, v, w)
    for r in range(3 * M):
        edges.append((r % M, T(r) % M, PSI[r % 3]))
    edgeset = set(edges)

    # ---- (A0) T is NOT a function of G mod 3^k: the "permutation" reading fails
    bad = sum(1 for a in range(M) if T(a) % M != T(a + M) % M)
    assert bad == M, (k, bad)          # ill-defined at EVERY residue
    # T as a map Z/3^{k+1} -> Z/3^k is exactly 3-to-1 (the shift), onto:
    pre = {}
    for r in range(3 * M):
        pre[T(r) % M] = pre.get(T(r) % M, 0) + 1
    assert len(pre) == M and set(pre.values()) == {3}

    # ---- (A1) degrees: 3 distinct out-targets per node, in-degree 3 per node
    outs = {a: set() for a in range(M)}
    indeg = {a: 0 for a in range(M)}
    for (u, v, w) in edges:
        outs[u].add(v)
        indeg[v] += 1
    assert all(len(s) == 3 for s in outs.values())
    assert set(indeg.values()) == {3}

    # ---- (A2) itinerary bijection + de Bruijn identification -----------------
    it2node = {}
    for a in range(M):
        w = itinerary(a, k)
        assert w not in it2node          # bijection {G mod 3^k} <-> {0,1,2}^k
        it2node[w] = a
    for r in range(3 * M):
        wr = itinerary(r, k + 1)
        assert it2node[wr[:k]] == r % M              # source = its k-window
        assert it2node[wr[1:]] == T(r) % M           # target = shifted window
        assert PSI[wr[0]] == PSI[r % 3]              # weight = psi(first symbol)
    # => the level-k residue automaton IS the complete 3-ary de Bruijn graph B(3,k):
    #    node = itinerary window (rho_0..rho_{k-1}), edges w -> w[1:]+sigma, all sigma.

    # ---- (A3) self-loops: exactly the 3 branch fixed-point classes -----------
    loops = {u: w for (u, v, w) in edges if u == v}
    assert set(loops) == {(-9) % M, (-14) % M, (-1) % M}
    assert loops[n14] == 1 and loops[(-9) % M] == -6 and loops[(-1) % M] == -4

    # ---- (A4) strong connectivity + de Bruijn diameter = k -------------------
    adj = [[] for _ in range(M)]
    radj = [[] for _ in range(M)]
    for (u, v, w) in edges:
        adj[u].append(v)
        radj[v].append(u)
    d0 = bfs_dists(M, adj, 0)
    r0 = bfs_dists(M, radj, 0)
    assert all(d is not None for d in d0) and all(d is not None for d in r0)
    assert max(d0) == k                       # every window reachable in <= k steps
    d43 = bfs_dists(M, adj, 43 % M)
    assert all(d is not None for d in d43)    # in particular n14 reachable from seed 43:
    assert d43[n14] <= k                      #   no domain-restriction dodge

    # ---- (T1) full-graph max mean cycle = +1 exactly --------------------------
    maxw = max(w for (_, _, w) in edges)
    assert maxw == 1                          # so every cycle has mean <= 1 ...
    assert (n14, n14, 1) in edgeset           # ... and the delta_{-14} self-loop attains it
    lam_full = Fraction(1)

    # ---- (T2) uniqueness: the ONLY mean-1 cycle is the self-loop at n14 -------
    # mean 1 forces all edge weights = 1, i.e. all sources rho=1; such cycles live in
    # the induced weight-1 subgraph on {a == 1 mod 3}; remove the n14 loop -> must be a DAG.
    ones_nodes = [a for a in range(M) if a % 3 == 1]
    ones_edges = [(u, v) for (u, v, w) in edges
                  if w == 1 and v % 3 == 1 and not (u == n14 and v == n14)]
    assert is_dag(ones_nodes, ones_edges)

    # ---- (P1) pervasiveness: delete the atom's node; exact max mean = (k-5)/k --
    # lower bound: the explicit cycle shadowing all-rho=1, word 1^{k-1} 2
    word = [1] * (k - 1) + [2]
    cyc_nodes = [it2node[tuple(word[(i + j) % k] for j in range(k))] for i in range(k)]
    assert n14 not in cyc_nodes
    ell = lambda a: max_run_of_ones(itinerary(a, k))     # leading run via window
    # tie to the run theorem: leading 1-run of a's window = min(v3(a+14), k)
    lead = lambda a: next((i for i, s in enumerate(itinerary(a, k)) if s != 1), k)
    for a in range(M):
        assert lead(a) == min(v3(a + 14), k)
    # upper bound: exact potential certificate phi(a) = -5 * lead(a) for the
    # integer-rescaled weights W = k*psi - (k-5)  (max mean psi = (k-5)/k <=> max mean W = 0)
    phi = {a: -5 * lead(a) for a in range(M) if a != n14}
    Wsum = 0
    for i in range(k):
        u, v = cyc_nodes[i], cyc_nodes[(i + 1) % k]
        w = PSI[word[i]]
        assert (u, v, w) in edgeset
        Wk = k * w - (k - 5)
        assert Wk == phi[v] - phi[u]          # tight (equality) on the exhibited cycle
        Wsum += w
    assert Fraction(Wsum, k) == Fraction(k - 5, k)
    for (u, v, w) in edges:
        if u != n14 and v != n14:
            assert k * w - (k - 5) <= phi[v] - phi[u]     # certificate: no W-positive cycle
    lam_del = Fraction(k - 5, k)              # PROVEN exactly (cycle + potential)

    # ---- Karp cross-checks (independent exact algorithm) ----------------------
    karp_note = "-"
    if k <= KARP_KMAX:
        assert karp_max_mean(M, edges) == lam_full
        assert karp_on_nodeset([a for a in range(M) if a != n14], edges) == lam_del
        karp_note = "Karp OK"

    # ---- closed-walk (cycle-structure) counts: trace A^L = 3^L ----------------
    if k <= WALK_KMAX:
        Lmax = 8
        totals = [0] * (Lmax + 1)
        for s in range(M):
            vec = [0] * M
            vec[s] = 1
            for L in range(1, Lmax + 1):
                nv = [0] * M
                for u in range(M):
                    c = vec[u]
                    if c:
                        for t in adj[u]:
                            nv[t] += c
                vec = nv
                totals[L] += vec[s]
        for L in range(1, Lmax + 1):
            assert totals[L] == 3 ** L        # full-3-shift zeta: 1/(1-3t), all levels

    report.append((k, M, 3 * M, lam_full, lam_del, karp_note))
    print("k=%d  |V|=%-5d |E|=%-6d  max-mean = %s  (INFEASIBLE, self-loop @ -14 mod 3^k)"
          "   deleted-atom max-mean = %s   %s"
          % (k, M, 3 * M, lam_full, lam_del, karp_note))

# ---------------- run-bound ladder (subshift restriction), exact at k = 6 -------
print()
print("run-bound ladder at k=6 (cycles = periodic itineraries with all rho=1 runs <= R):")
k = 6
M = 3 ** k
edges = [(r % M, T(r) % M, PSI[r % 3]) for r in range(3 * M)]
win = {a: itinerary(a, k) for a in range(M)}
for R in range(1, 6):
    nodes = [a for a in range(M) if max_run_of_ones(win[a]) <= R]
    lam = karp_on_nodeset(nodes, edges)
    assert lam == Fraction(R - 4, R + 1), (R, lam)
    verdict = "feasible (c<0)" if lam < 0 else ("feasible (c=0 only)" if lam == 0 else "INFEASIBLE")
    print("  runs <= %d :  max-mean = %6s   -> sub-action %s" % (R, lam, verdict))

print()
print("ALL ASSERTIONS PASSED (exact arithmetic; no floats).")
print("Level-k LP: infeasible for every k (min feasible c = +1 = max mean cycle,")
print("attained UNIQUELY by the delta_{-14} self-loop at residue -14 mod 3^k).")
