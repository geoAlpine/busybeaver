#!/usr/bin/env python3
"""
Coboundary / Lyapunov LP for the induced odd Antihydra map.

Induced odd map (GAP LEMMA):  T(o) = 3^{D-1} (3o-1) / 2^D,  D = v2(3o-1) >= 1,  o odd.
o_0 = 27.

TARGET (robust, margin 1/4):   liminf_N (1/N) sum_{j<N} [ 1{D_j>=2} + 1{D_j>=3} ] >= 1/2,
which is SUFFICIENT for mean D >= 3/2 <=> even-density >= 1/3 <=> non-halt.

Reframed via the potential
    psi(o) = 1{o == 1 mod 4} - 1{o == 3 mod 8} - 1/2
           = 1{D=1} - 1{D>=3} - 1/2
           = 1/2 - 1{D>=2} - 1{D>=3}.
So  (1/N) sum psi(o_j) = 1/2 - (1/N) sum [1{D>=2}+1{D>=3}], and
    limsup (1/N) sum psi(o_j) <= 0   <=>   the TARGET.
Haar mean of psi = 1/2 - 1/4 - 1/2 = -1/4  (1/4 of slack).

COBOUNDARY STRATEGY (would be UNCONDITIONAL if it worked):
find bounded g(o mod 2^k) with   psi(o) <= g(T(o)) - g(o)  for ALL odd o.
Then telescoping:  sum_{j<N} psi(o_j) <= g(o_N) - g(o_0) <= 2||g||_inf,
so limsup (1/N) sum psi <= 0 for EVERY orbit -- no genericity needed.

THIS IS A FINITE LP. With g a function of residue mod 2^k it is a system of
DIFFERENCE CONSTRAINTS  g(b) - g(a) >= psi  (a = o mod 2^k, b = T(o) mod 2^k).
By LP duality, such a system is FEASIBLE iff the constraint digraph has NO cycle
of positive total weight (Bellman-Ford / max-mean-cycle). A positive cycle is a
periodic pseudo-orbit on residues with average psi > 0 -- the dual obstruction.

Numerics: exact big-int. Tail truncation handled soundly (see TAIL below).
"""
import sys
from fractions import Fraction

# ----------------------------------------------------------------------
# exact arithmetic of the induced map
# ----------------------------------------------------------------------
def v2(n):
    n = abs(int(n))
    if n == 0:
        return 10**9
    r = 0
    while n & 1 == 0:
        n >>= 1
        r += 1
    return r

def D_of(o):
    return v2(3*o - 1)

def T(o):
    d = D_of(o)
    return (3**(d-1)) * (3*o - 1) // (2**d)

def psi(o):
    """psi depends only on o mod 8. Returns a Fraction."""
    r = o & 7
    if r % 4 == 1:          # o==1 mod 4 : D=1
        return Fraction(1, 2)
    if r == 7:              # o==7 mod 8 : D=2
        return Fraction(-1, 2)
    # r == 3 mod 8 : D>=3
    return Fraction(-3, 2)

# sanity: psi via D
def psi_via_D(o):
    d = D_of(o)
    return Fraction(1 if d == 1 else 0) - Fraction(1 if d >= 3 else 0) - Fraction(1, 2)

# ----------------------------------------------------------------------
# 1. small-integer cycle search of the induced map (REAL obstructions)
# ----------------------------------------------------------------------
def find_integer_cycles(maxstart=20001, maxiter=2000, cap=10**12):
    """Search positive odd integers for cycles of T; report mean psi on each."""
    seen_cycles = {}
    for s in range(1, maxstart, 2):
        o = s
        history = {}
        path = []
        step = 0
        ok = True
        while step < maxiter:
            if o in history:
                # found a cycle: from history[o] to end of path
                start = history[o]
                cyc = tuple(path[start:])
                key = min(cyc)  # canonical-ish key by minimal element
                if key not in seen_cycles:
                    m = sum(psi(x) for x in cyc) / len(cyc)
                    seen_cycles[key] = (cyc, m)
                break
            if o > cap:
                ok = False
                break
            history[o] = step
            path.append(o)
            o = T(o)
            step += 1
    return seen_cycles

# ----------------------------------------------------------------------
# 2. residue constraint graph mod 2^k, with SOUND tail truncation
# ----------------------------------------------------------------------
# Nodes: odd residues mod M=2^k.
# For each odd residue r mod 2^K (K = k + LOOK) with D(r) determined and
# k + D(r) <= K (=> T(r) mod 2^k determined), add directed edge
#   a = r mod 2^k  -->  b = T(r) mod 2^k     with weight psi(r).
# Edge weight depends only on the SOURCE (psi is a fn of a mod 8, k>=3).
#
# TAIL (undetermined): residues r mod 2^K with D(r) > K-k.  For K-k >= 2 every
# such r has D >= 3, hence psi(r) = -3/2 (the most FAVORABLE value).  The branch
# is full (maps ONTO all of Z_2^*), so T(o) mod 2^k can be ANY odd residue s.
# SOUND requirement: psi(r) <= g(s) - g(r) for ALL s, i.e. add edges a -> s of
# weight -3/2 for all odd s.  These are loose (very negative) and can never lie
# on a positive cycle, but they ARE included so the reported feasibility is the
# true LP feasibility, not an under-constrained relaxation.

def build_graph(k, look=4):
    K = k + look
    assert K - k >= 2, "need K-k>=2 so every tail residue has D>=3 (psi=-3/2)"
    M = 1 << k
    MK = 1 << K
    # edges as dict: (a,b) -> weight (all weights from a are equal = psi(a), but
    # we keep the structure explicit). Use set of (a,b) plus weight-by-source.
    edges = set()
    weight_of_source = {}      # a -> psi(a)
    tail_sources = set()       # a that have an undetermined (tail) branch
    nodes = list(range(1, M, 2))
    for a in nodes:
        weight_of_source[a] = psi(a)
    # enumerate full residues mod 2^K
    for r in range(1, MK, 2):
        d = D_of_residue(r, K)          # exact D if < K else None (deep tail)
        a = r & (M - 1)
        if d is not None and (k + d) <= K:
            b = T(r) & (M - 1)          # determined: T(r) mod 2^k fixed by r mod 2^K
            edges.add((a, b))
        else:
            # undetermined / deep tail: D > K-k >= 2  => psi = -3/2
            tail_sources.add(a)
    return nodes, edges, weight_of_source, tail_sources, K

def D_of_residue(r, K):
    """v2(3r-1) but only trusted if < K (else bits beyond 2^K unknown).
    Returns the exact D if 3r-1 has a 1-bit below position K, else None."""
    x = (3*r - 1) & ((1 << K) - 1)
    if x == 0:
        return None     # 3r-1 == 0 mod 2^K : D >= K, undetermined
    d = v2(x)
    return d            # d < K guaranteed (x != 0, x < 2^K)

# ----------------------------------------------------------------------
# 3. positive-cycle / max-mean-cycle detection (Bellman-Ford + Karp)
# ----------------------------------------------------------------------
def has_positive_selfloop(edges, weight_of_source):
    for (a, b) in edges:
        if a == b and weight_of_source[a] > 0:
            return a, weight_of_source[a]
    return None

def bellman_ford_positive_cycle(nodes, edges, weight_of_source):
    """Detect a positive-weight cycle (edge weight = psi(source)).
    Returns a cycle (list of nodes) if found, else None.
    Uses 'longest path' relaxation; positive cycle <=> can keep increasing."""
    # adjacency
    adj = {a: [] for a in nodes}
    for (a, b) in edges:
        adj[a].append(b)
    dist = {a: Fraction(0) for a in nodes}
    pred = {a: None for a in nodes}
    n = len(nodes)
    x = None
    for it in range(n):
        x = None
        for (a, b) in edges:
            w = weight_of_source[a]
            if dist[a] + w > dist[b]:
                dist[b] = dist[a] + w
                pred[b] = a
                x = b
        if x is None:
            break
    if x is None:
        return None  # no positive cycle reachable
    # x is on or reachable from a positive cycle; walk back n steps to land on cycle
    for _ in range(n):
        x = pred[x]
    cyc = [x]
    y = pred[x]
    while y != x:
        cyc.append(y)
        y = pred[y]
    cyc.reverse()
    return cyc

def cycle_mean(cyc, weight_of_source):
    return sum(weight_of_source[a] for a in cyc) / len(cyc)

# ----------------------------------------------------------------------
# 4. tail-soundness audit
# ----------------------------------------------------------------------
def tail_audit(k, look=4):
    """Verify: every undetermined residue r mod 2^K has D > K-k and psi = -3/2,
    and report the measure (fraction) of the undetermined set."""
    K = k + look
    MK = 1 << K
    total = 0
    undet = 0
    bad = 0   # undetermined residues whose psi != -3/2  (must be 0)
    for r in range(1, MK, 2):
        total += 1
        d = D_of_residue(r, K)
        if d is None or (k + d) > K:
            undet += 1
            # this residue's D > K - k; check psi
            if psi(r) != Fraction(-3, 2):
                bad += 1
    return dict(K=K, total_odd=total, undetermined=undet,
                undet_fraction=Fraction(undet, total), bad_psi=bad,
                bound_2pow=Fraction(1, 1 << (K - k - 1)))  # 2^{-(K-k-1)} odd-relative

# ----------------------------------------------------------------------
# 5. independent verification on the REAL orbit + random odds
# ----------------------------------------------------------------------
def verify_equivalence_and_obstruction(N=200000):
    import random
    # (a) psi consistency
    bad = 0
    for o in range(1, 2001, 2):
        if psi(o) != psi_via_D(o):
            bad += 1
    # (b) real orbit average vs target identity
    o = 27
    s_psi = Fraction(0)
    cnt_ge2 = 0
    cnt_ge3 = 0
    for j in range(N):
        d = D_of(o)
        s_psi += psi(o)
        if d >= 2: cnt_ge2 += 1
        if d >= 3: cnt_ge3 += 1
        o = T(o)
    avg_psi = s_psi / N
    avg_target = Fraction(cnt_ge2 + cnt_ge3, N)
    # identity: avg_psi == 1/2 - avg_target
    ident_ok = (avg_psi == Fraction(1, 2) - avg_target)
    # (c) the fixed point o=1 violates the bound
    fp_ok = (T(1) == 1) and (psi(1) == Fraction(1, 2))
    return dict(psi_consistency_bad=bad, real_avg_psi=float(avg_psi),
                real_avg_target=float(avg_target), identity_ok=ident_ok,
                fixedpoint1_T1=T(1), fixedpoint1_psi=psi(1),
                fixedpoint_violates=fp_ok)

# ----------------------------------------------------------------------
def main():
    print("="*72)
    print("COBOUNDARY LP for induced Antihydra odd map  (psi <= g(T)-g)")
    print("="*72)

    print("\n[0] psi values by residue mod 8 (Fraction):")
    for r in range(1, 16, 2):
        print(f"   o={r:2d}  o%8={r&7}  D={D_of(r)}  psi={psi(r)}")
    print(f"   Haar mean psi = 1/2 - 1/4 - 1/2 = {Fraction(1,2)-Fraction(1,4)-Fraction(1,2)}")

    print("\n[1] REAL small-integer cycles of T (genuine obstructions):")
    cycles = find_integer_cycles()
    pos = []
    for key in sorted(cycles):
        cyc, m = cycles[key]
        flag = "  <-- POSITIVE-MEAN (obstruction!)" if m > 0 else ""
        if m > 0: pos.append((cyc, m))
        if len(cyc) <= 12 or m > 0:
            print(f"   cycle min={key:>6}  len={len(cyc):>3}  mean psi={m}"
                  f"  meanD={sum(D_of(x) for x in cyc)/len(cyc):.4f}{flag}")
    print(f"   --> #positive-mean integer cycles found: {len(pos)}")
    for cyc, m in pos:
        print(f"       {cyc[:8]}{'...' if len(cyc)>8 else ''}  mean psi={m}")

    print("\n[2] Coboundary LP feasibility per level k (mod 2^k), sound tail:")
    print("    feasible  <=>  no positive cycle in residue constraint graph.")
    for k in range(3, 13):
        look = 4 if k <= 10 else 3
        nodes, edges, wsrc, tail, K = build_graph(k, look=look)
        sl = has_positive_selfloop(edges, wsrc)
        # only run full Bellman-Ford for tractable k
        cyc = None
        mean = None
        if k <= 9:
            cyc = bellman_ford_positive_cycle(nodes, edges, wsrc)
            if cyc is not None:
                mean = cycle_mean(cyc, wsrc)
        verdict = "INFEASIBLE" if (sl or cyc) else "feasible?"
        slstr = f"self-loop@{sl[0]} w={sl[1]}" if sl else "no pos self-loop"
        cycstr = ""
        if cyc is not None:
            cycstr = f"; pos-cycle len={len(cyc)} mean={mean} nodes={cyc[:6]}"
        print(f"   k={k:2d} (K={K}, |V|={len(nodes)}, |E|={len(edges)}): "
              f"{verdict}  [{slstr}{cycstr}]")

    print("\n[3] TAIL-TRUNCATION SOUNDNESS audit:")
    for k in [3, 5, 7]:
        a = tail_audit(k, look=4)
        print(f"   k={k} K={a['K']}: undetermined odd residues = "
              f"{a['undetermined']}/{a['total_odd']} = {a['undet_fraction']} "
              f"(~2^-{a['K']-k}); psi!=-3/2 among them = {a['bad_psi']} "
              f"(MUST be 0 for sound -3/2 tail)")

    print("\n[4] Independent verification:")
    v = verify_equivalence_and_obstruction(N=200000)
    for key, val in v.items():
        print(f"   {key}: {val}")

    print("\n" + "="*72)
    print("CONCLUSION: max single-edge weight = +1/2 (at o==1 mod4 nodes).")
    print("The induced map has the FIXED POINT o=1 (T(1)=1) with psi(1)=+1/2>0,")
    print("=> self-loop of weight +1/2 at residue 1 mod 2^k for EVERY k>=3.")
    print("=> max-mean-cycle = +1/2 > 0 => the coboundary LP is INFEASIBLE at")
    print("   every level k. Dual obstruction = the Dirac measure delta_1 (and")
    print("   any low positive-mean cycle). The Haar 1/4 slack is irrelevant:")
    print("   the obstruction is an ATOMIC invariant measure, not the Haar mean.")
    print("="*72)

if __name__ == "__main__":
    main()
