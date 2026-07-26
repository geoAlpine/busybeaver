#!/usr/bin/env python3
"""How much of the BB(6) residual admits `RungCalc.Atoms`?  (RESUME 2026-07-26 §3 Option A)

`lean/RungCalc.lean` proves the COMB-doubler rung tile for ANY machine satisfying the six-atom
interface `Atoms T sA sB`.  Per-machine cost is six closed kernel `rfl`s.  So "how big is the
template island" becomes, for the first time, a MEASUREMENT rather than an estimate:

    how many still-open BB(6) holdouts satisfy `Atoms`, in either orientation, at any state?

## The interface, written as transition constraints

Given the outward-sweep state `sA`, EVERYTHING else is forced -- `sA` on read 0 has a unique
transition, and it is shared by `turnaround` (which names `sB`) and by `crawl`'s first step.
Writing `b = sB` and naming the intermediates:

     1. sA,0 -> (1,L,b)      turnaround + crawl step 1
     2. sA,1 -> (0,L,sA)     marker
     3.  b,1 -> (0,R,e)      crawl step 2 + swap10 step 1
     4.  e,1 -> (0,L,d)      crawl step 3
     5.  d,0 -> (1,L,sA)     crawl step 4
     6.  e,0 -> (1,R,b)      swap10 step 2
     7.  b,0 -> (1,R,c)      swap01 step 1 + turn step 1
     8.  c,1 -> (0,R,b)      swap01 step 2
     9.  c,0 -> (0,R,f)      turn step 2
    10.  f,0 -> (1,L,sA)     turn step 3

That is 9-10 of a 6-state machine's 12 transition entries (10 when sA,b,e,c,d,f are all
distinct; 9 when d = f).  **So `Atoms` is a narrow constraint and the honest expectation is a
small number of hits.**  Reporting that number, whatever it is, is the point: it bounds how much
of the residual the machine-independent tile can ever reach.

We therefore also report a GRADIENT -- how many of the six atoms hold -- so that near-misses
(5/6) are visible, and so we can see which atoms are the generic ones and which are rare.
"""
import os, sys
from collections import Counter, defaultdict

DATA = "/Users/aokiyousuke/busybeaver/_bbdata"
LISTS = [("1104 (Jun 2026 curated residual)", os.path.join(DATA, "bb6_holdouts_1104.txt")),
         ("1094 (Jul 2026 list)",             os.path.join(DATA, "BB6_holdouts_1094.txt"))]

# the named island candidates (island_preflight.py) for control / context
ISLAND = [
    ("x2", "1RB0RE_1RC---_0LD1LE_0RE1LD_1RF0LC_0RA1RE"),
    ("D",  "1RB0RA_1LC0LE_0LD0LB_1RA0LF_1LB0RD_1LD---"),
    ("E",  "1RB0RE_0RC0RA_1LD0RF_1LA0LD_1RA0LC_1RC---"),
    ("F",  "1RB0LE_1RC0RF_0RD0RB_1RE0RC_1LA0LA_1RA---"),
    ("H",  "1RB0RE_0RC0RA_1LD1RE_1LA0LD_1RA0LF_1LD---"),
    ("G",  "1RB0LA_1RC0RE_0RD---_1LA0LD_1LD1RF_1RA1LB"),
    ("I",  "1RB0LA_1RC0RE_0RD---_1LA1LF_1LD1RF_1RA1LB"),
]
SC = "ABCDEF"

def parse(spec):
    """-> list over states of [t0, t1], t = (write, dir, next) with dir +1=R,-1=L, or None=HALT"""
    T = []
    for blk in spec.strip().split('_'):
        row = []
        for k in (0, 3):
            f = blk[k:k+3]
            row.append(None if f[0] == '-' else (int(f[0]), 1 if f[1] == 'R' else -1, ord(f[2]) - 65))
        T.append(row)
    return T

def reverse(T):
    return [[None if e is None else (e[0], -e[1], e[2]) for e in row] for row in T]

L_, R_ = -1, 1

def atoms_report(T, sA):
    """Given the outward state sA, derive the forced roles and report which of the six atoms
    hold.  Returns (set_of_atom_names_that_hold, roles_or_None)."""
    hold = set()
    n = len(T)
    def g(s, r):
        return T[s][r] if 0 <= s < n else None

    # marker: sA,1 -> (0,L,sA)
    if g(sA, 1) == (0, L_, sA):
        hold.add("marker")

    # turnaround: sA,0 -> (1,L,b)  -- this DEFINES b
    e0 = g(sA, 0)
    if e0 is None or e0[0] != 1 or e0[1] != L_:
        return hold, None
    b = e0[2]
    hold.add("turnaround")

    # crawl: sA,0 -> (1,L,b); b,1 -> (0,R,e); e,1 -> (0,L,d); d,0 -> (1,L,sA)
    e1 = g(b, 1); ee = dd = None
    if e1 is not None and e1[0] == 0 and e1[1] == R_:
        ee = e1[2]
        e2 = g(ee, 1)
        if e2 is not None and e2[0] == 0 and e2[1] == L_:
            dd = e2[2]
            if g(dd, 0) == (1, L_, sA):
                hold.add("crawl")

    # swap10: b,1 -> (0,R,e); e,0 -> (1,R,b)
    if ee is not None and g(ee, 0) == (1, R_, b):
        hold.add("swap10")

    # swap01: b,0 -> (1,R,c); c,1 -> (0,R,b)   -- this DEFINES c
    e3 = g(b, 0); cc = None
    if e3 is not None and e3[0] == 1 and e3[1] == R_:
        cc = e3[2]
        if g(cc, 1) == (0, R_, b):
            hold.add("swap01")

    # turn: b,0 -> (1,R,c); c,0 -> (0,R,f); f,0 -> (1,L,sA)
    ff = None
    if cc is not None:
        e4 = g(cc, 0)
        if e4 is not None and e4[0] == 0 and e4[1] == R_:
            ff = e4[2]
            if g(ff, 0) == (1, L_, sA):
                hold.add("turn")

    return hold, (sA, b, ee, dd, cc, ff)

ALL6 = {"crawl", "marker", "turnaround", "swap10", "swap01", "turn"}

def best_over_states(T):
    """-> (max_atoms_held, list of (sA, held, roles) achieving it)"""
    best = -1; out = []
    for sA in range(len(T)):
        hold, roles = atoms_report(T, sA)
        if len(hold) > best:
            best = len(hold); out = [(sA, hold, roles)]
        elif len(hold) == best:
            out.append((sA, hold, roles))
    return best, out

def scan(spec):
    """try both orientations; -> (best_count, [(orient, sA, held, roles)...])"""
    res = []
    for oname, T in (("as-written", parse(spec)), ("reversed", reverse(parse(spec)))):
        for sA in range(len(T)):
            hold, roles = atoms_report(T, sA)
            res.append((oname, sA, hold, roles))
    best = max(len(h) for _, _, h, _ in res)
    return best, [r for r in res if len(r[2]) == best]

def main():
    # ---------------------------------------------------------------- controls first
    print("=== (0) CONTROLS: D and H must be full hits; the rest of the named island for context ===")
    for name, spec in ISLAND:
        best, hits = scan(spec)
        tag = "  <== FULL Atoms" if best == 6 else ""
        detail = ""
        if best == 6:
            o, sA, _, roles = hits[0]
            sA_, b, e, d, c, f = roles
            detail = (f"   [{o}] sA={SC[sA_]} sB={SC[b]}  e={SC[e]} d={SC[d]} c={SC[c]} f={SC[f]}"
                      + ("  (d=f)" if d == f else "  (d!=f)"))
        else:
            missing = sorted(ALL6 - hits[0][2])
            detail = f"   best {best}/6, missing {missing} (at {hits[0][0]} sA={SC[hits[0][1]]})"
        print(f"  {name:3s}: {best}/6 atoms{tag}{detail}")

    # ------------------------------------------------------------------- the residual
    print()
    print("=== (1) THE RESIDUAL: how many still-open holdouts satisfy Atoms? ===")
    for lname, path in LISTS:
        if not os.path.exists(path):
            print(f"  {lname}: FILE MISSING {path}")
            continue
        dist = Counter()
        full = []
        near = []
        total = 0
        with open(path) as fh:
            for line in fh:
                spec = line.strip().split()[0] if line.strip() else ""
                if not spec or spec.count('_') != 5:
                    continue
                total += 1
                best, hits = scan(spec)
                dist[best] += 1
                if best == 6:
                    full.append((spec, hits[0]))
                elif best == 5:
                    near.append((spec, hits[0]))
        print(f"  {lname}: {total} machines")
        print("     atoms held (best over both orientations x all 6 states):")
        for k in sorted(dist, reverse=True):
            print(f"       {k}/6 : {dist[k]:5d}")
        print(f"     FULL Atoms (=> rung tile for six rfl's): {len(full)}")
        for spec, (o, sA, _, roles) in full:
            sA_, b, e, d, c, f = roles
            print(f"       {spec}  [{o}] sA={SC[sA_]} sB={SC[b]} e={SC[e]} d={SC[d]} c={SC[c]} f={SC[f]}"
                  + ("  (d=f)" if d == f else "  (d!=f)"))
        # cluster the full hits by their PINNED part: machines agreeing on every entry that
        # Atoms constrains are "the same tile", differing only in the free entries.
        clus = defaultdict(list)
        for spec, (o, sA, _, roles) in full:
            sA_, b, e, d, c, f = roles
            T = parse(spec) if o == "as-written" else reverse(parse(spec))
            pins = ((sA_, 0), (sA_, 1), (b, 0), (b, 1), (e, 0), (e, 1), (c, 0), (c, 1), (d, 0), (f, 0))
            # canonicalise by the ROLE each state plays, not by its name
            role = {sA_: 'A', b: 'b', e: 'e', d: 'd', c: 'c', f: 'f'}
            key = tuple(sorted((role[s], r,
                                None if T[s][r] is None else (T[s][r][0], T[s][r][1], role.get(T[s][r][2], '?')))
                               for s, r in set(pins)))
            clus[key].append(spec)
        # NOTE, so this is not over-read: the pinned entries are the same for ALL hits BY
        # CONSTRUCTION -- `Atoms` specifies each of them exactly.  So "clusters of identical pinned
        # part" is tautological and is NOT evidence of anything.  The only genuine structural
        # freedom is which roles COINCIDE; in this residual the split is d=f vs d!=f.
        df = sum(1 for _, (_, _, _, r) in full if r[3] == r[5])
        print(f"     structural split (the only non-tautological one): d=f in {df}, d!=f in {len(full)-df}")
        print(f"       d=f  merges the crawl-closer and the turn-closer into ONE state (D's shape);")
        print(f"       d!=f keeps them apart (H's shape).  Both satisfy the same `Atoms`.")
        print(f"     free entries per hit: 2 (d!=f, all six states used) or 3 (d=f, one state spare)")
        print(f"     5/6 near-misses: {len(near)}")
        for spec, (o, sA, held, roles) in near:
            print(f"       {spec}  [{o}] sA={SC[sA]} missing {sorted(ALL6 - held)}")

    # ------------------------------------------------- how narrow is Atoms, exactly?
    print()
    print("=== (2) HOW NARROW IS Atoms?  (the honest caveat) ===")
    print("    Atoms pins these (state,read) entries: (sA,0)(sA,1)(b,0)(b,1)(e,0)(e,1)(c,0)(c,1)(d,0)(f,0)")
    for name, spec in (("D (reversed)", "1RB0RA_1LC0LE_0LD0LB_1RA0LF_1LB0RD_1LD---"),
                       ("H (as-written)", "1RB0RE_0RC0RA_1LD1RE_1LA0LD_1RA0LF_1LD---")):
        best, hits = scan(spec)
        o, sA, _, roles = hits[0]
        sA_, b, e, d, c, f = roles
        pinned = {(sA_, 0), (sA_, 1), (b, 0), (b, 1), (e, 0), (e, 1), (c, 0), (c, 1), (d, 0), (f, 0)}
        free = [(s, r) for s in range(6) for r in (0, 1) if (s, r) not in pinned]
        T = parse(spec) if o == "as-written" else reverse(parse(spec))
        fr = ", ".join(f"{SC[s]}{r}=" + ("HALT" if T[s][r] is None else
                       f"{T[s][r][0]}{'R' if T[s][r][1]==1 else 'L'}{SC[T[s][r][2]]}") for s, r in free)
        print(f"  {name}: {len(pinned)}/12 entries pinned by Atoms; free = {fr}")
    print("    => the two machines differ ONLY in the free entries and in whether d = f.")
    print("       D^R merges the crawl-closer and the turn-closer into one state (d=f=D);")
    print("       H keeps them apart (d=F, f=C).  That is the whole graph difference.")



def orbit_relevance(N=300000):
    """(3) Does each hit's REAL blank-tape orbit actually enter the tile's configuration family?

    `Atoms` being true of a machine only makes the tile a true lemma ABOUT it.  Whether the tile
    is USEFUL for it is a separate, measurable question: does the blank-tape orbit ever hold an
    IN-shaped configuration, in the outward state, on which the span law fires?  D and H were
    checked (anchor160 / anchor17 + orbit scan); this checks all 17 uniformly.
    """
    print()
    print(f"=== (3) ORBIT RELEVANCE of the {17} hits: does the real orbit enter the IN family? ===")
    print("    (Atoms true  =>  tile is a true LEMMA.  Orbit entry  =>  tile is ABOUT the machine.)")
    hits = []
    with open(LISTS[0][1]) as fh:
        for line in fh:
            spec = line.strip().split()[0] if line.strip() else ""
            if not spec or spec.count('_') != 5:
                continue
            best, hs = scan(spec)
            if best == 6:
                hits.append((spec, hs[0]))

    print(f"  {'spec':46s} {'or':11s} sA  halt?   window        IN-hits  tile-fires")
    for spec, (o, sA, _, roles) in hits:
        T = parse(spec) if o == "as-written" else reverse(parse(spec))
        cap = 1 << 21
        tape = bytearray(2 * cap); pos = cap; st = 0
        lo = hi = pos
        halt_t = None
        seen = set(); fired = 0
        for t in range(N):
            if st == sA and tape[pos] == 0 and tape[pos + 1] == 1:
                g = 0
                while g < 64 and tape[pos + 2 + g] == 0: g += 1
                if g >= 3:
                    u = 0
                    while u < 2048 and tape[pos - 1 - 2*u] == 1 and tape[pos - 2 - 2*u] == 0: u += 1
                    i = pos - 1 - 2*u
                    if tape[i] == 1 and tape[i-1] == 1:
                        j = i - 2; m = 0
                        while m < 2048 and tape[j] == 0 and tape[j-1] == 1: m += 1; j -= 2
                        if m >= 1 and tape[j] == 0 and tape[j-1] == 0:
                            key = (u, m, g)
                            if key not in seen:
                                seen.add(key)
                                span = 6*(u+m) + 15
                                cp = bytearray(tape); cq = pos; cs = st; dead = False
                                for _ in range(span):
                                    e = T[cs][cp[cq]]
                                    if e is None: dead = True; break
                                    cp[cq] = e[0]; cq += e[1]; cs = e[2]
                                if not dead and cs == sA and cq == pos + 3:
                                    fired += 1
            e = T[st][tape[pos]]
            if e is None:
                halt_t = t; break
            tape[pos] = e[0]; pos += e[1]; st = e[2]
            lo = min(lo, pos); hi = max(hi, pos)
        hstr = f"t={halt_t}" if halt_t is not None else "no"
        flag = "" if fired else "   <== tile NEVER fires on the orbit"
        print(f"  {spec:46s} {o:11s} {SC[sA]}   {hstr:7s} [{lo-cap:6d},{hi-cap:6d}] {len(seen):7d}  {fired:7d}{flag}")


if __name__ == "__main__":
    main()
    orbit_relevance()
