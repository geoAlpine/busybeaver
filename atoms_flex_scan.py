#!/usr/bin/env python3
"""Behavioural `Atoms` scan — detect the six atoms by their TAPE EFFECT, at any step count.

`atoms_island_scan.py` matched each atom as a fixed transition *shape* (crawl = 4 steps,
turn = 3, ...).  That found 17/1104.  Its lone 5/6 near-miss,
`1RB0RF_0LC0RA_1LE1RD_0RC---_1LA0LE_1RA0LC` at `sA=E`, turned out to reach the turn's EXACT
output configuration -- state `sA` at `+1`, cells `p,p+1,p+2 : 0 0 0 -> 1 0 1` -- in **5** steps
instead of 3, via `A0→1RB, B0→0LC, C1→1RD, D0→0RC, C0→1LE`.

So the fixed step counts were an accident of D, not part of the mechanism.  The rung tile only
needs each atom's input/output *specification*; the span is then a linear function of the six
step counts:

    span = (u+m+2)·CR + (u+3)·S01 + (m+1)·S10 + MK + TA + TU

(with CR=4, MK=1, TA=1, S01=2, S10=2, TU=3 this is D's 6(u+m)+21 in shifted variables.)

This instrument therefore searches for each atom BEHAVIOURALLY: instantiate the atom's input
pattern on a concrete tape, run the machine, and record the first step count at which the
configuration equals the atom's output pattern EXACTLY (state, position, and every tape cell).
Several different contexts (`L`, `R`, and the free bit) are tried and the step count must agree
across all of them -- that is the `∀`-uniformity the Lean lemma needs.  Lean remains the
verifier; this is only the search.
"""
import os
from collections import Counter, defaultdict
from atoms_island_scan import parse, reverse, SC, ISLAND, LISTS

CAP = 64          # an "atom" longer than this is not an atom
CTXS = [([1, 0, 1], [1, 1, 0]), ([], []), ([0, 0], [1]), ([1, 1, 1, 0], [0, 1, 0, 1])]
BITS = [0, 1]

def mk(left, head, right, p=0):
    """tape dict from (left nearest-first, head, right)"""
    t = {}
    for i, b in enumerate(left):
        if b: t[p - 1 - i] = 1
    if head: t[p] = 1
    for i, b in enumerate(right):
        if b: t[p + 1 + i] = 1
    return t

def run_to(T, tape, pos, st, want_pos, want_tape, want_st=None, cap=CAP):
    """first k<=cap with (st,pos,tape) == target; -> (k, state_at_k) or (None,None)"""
    tape = dict(tape)
    for k in range(cap + 1):
        if pos == want_pos and tape == want_tape and (want_st is None or st == want_st):
            return k, st
        e = T[st][tape.get(pos, 0)]
        if e is None:
            return None, None
        w, d, nx = e
        if w: tape[pos] = 1
        elif pos in tape: del tape[pos]
        pos += d; st = nx
    return None, None

def atom_crawl(T, sA):
    """<sA,p,<1::b::L, 0, R>>  ->  <sA,p-2,<L, b, 1::0::R>>   (tape unchanged)"""
    ks = set()
    for L, R in CTXS:
        for b in BITS:
            tin = mk([1, b] + L, 0, R)
            k, _ = run_to(T, tin, 0, sA, -2, dict(tin), sA)
            if k is None or k == 0: return None
            ks.add(k)
    return ks.pop() if len(ks) == 1 else None

def atom_marker(T, sA):
    """<sA,p,<x::L, 1, R>>  ->  <sA,p-1,<L, x, 0::R>>   (cell p: 1 -> 0)"""
    ks = set()
    for L, R in CTXS:
        for x in BITS:
            tin = mk([x] + L, 1, R)
            tout = dict(tin); tout.pop(0, None)
            k, _ = run_to(T, tin, 0, sA, -1, tout, sA)
            if k is None or k == 0: return None
            ks.add(k)
    return ks.pop() if len(ks) == 1 else None

def atom_turnaround(T, sA):
    """<sA,p,<x::L, 0, R>>  ->  <sB,p-1,<L, x, 1::R>>   (cell p: 0 -> 1); DEFINES sB"""
    ks, sbs = set(), set()
    for L, R in CTXS:
        for x in BITS:
            tin = mk([x] + L, 0, R)
            tout = dict(tin); tout[0] = 1
            k, s = run_to(T, tin, 0, sA, -1, tout, None)
            if k is None or k == 0: return None, None
            ks.add(k); sbs.add(s)
    if len(ks) != 1 or len(sbs) != 1: return None, None
    return ks.pop(), sbs.pop()

def atom_swap10(T, sB):
    """<sB,p,<L, 1, 0::b::R>>  ->  <sB,p+2,<1::0::L, b, R>>   (cells p,p+1: 1 0 -> 0 1)"""
    ks = set()
    for L, R in CTXS:
        for b in BITS:
            tin = mk(L, 1, [0, b] + R)
            tout = dict(tin); tout.pop(0, None); tout[1] = 1
            k, _ = run_to(T, tin, 0, sB, 2, tout, sB)
            if k is None or k == 0: return None
            ks.add(k)
    return ks.pop() if len(ks) == 1 else None

def atom_swap01(T, sB):
    """<sB,p,<L, 0, 1::b::R>>  ->  <sB,p+2,<0::1::L, b, R>>   (cells p,p+1: 0 1 -> 1 0)"""
    ks = set()
    for L, R in CTXS:
        for b in BITS:
            tin = mk(L, 0, [1, b] + R)
            tout = dict(tin); tout[0] = 1; tout.pop(1, None)
            k, _ = run_to(T, tin, 0, sB, 2, tout, sB)
            if k is None or k == 0: return None
            ks.add(k)
    return ks.pop() if len(ks) == 1 else None

def atom_turn(T, sB, sA):
    """<sB,p,<L, 0, 0::0::R>>  ->  <sA,p+1,<1::L, 0, 1::R>>   (cells p,p+2: 0 -> 1)"""
    ks = set()
    for L, R in CTXS:
        tin = mk(L, 0, [0, 0] + R)
        tout = dict(tin); tout[0] = 1; tout[2] = 1
        k, _ = run_to(T, tin, 0, sB, 1, tout, sA)
        if k is None or k == 0: return None
        ks.add(k)
    return ks.pop() if len(ks) == 1 else None

NAMES = ["crawl", "marker", "turnaround", "swap10", "swap01", "turn"]

def flex_atoms(T, sA):
    """-> (held:set, steps:dict, sB) for this outward state"""
    held, steps = set(), {}
    cr = atom_crawl(T, sA)
    if cr: held.add("crawl"); steps["crawl"] = cr
    mk_ = atom_marker(T, sA)
    if mk_: held.add("marker"); steps["marker"] = mk_
    ta, sB = atom_turnaround(T, sA)
    if ta is None:
        return held, steps, None
    held.add("turnaround"); steps["turnaround"] = ta
    s10 = atom_swap10(T, sB)
    if s10: held.add("swap10"); steps["swap10"] = s10
    s01 = atom_swap01(T, sB)
    if s01: held.add("swap01"); steps["swap01"] = s01
    tu = atom_turn(T, sB, sA)
    if tu: held.add("turn"); steps["turn"] = tu
    return held, steps, sB

def flex_scan(spec):
    """-> (best, [(orient, sA, sB, held, steps)...])"""
    out = []
    for oname, T in (("as-written", parse(spec)), ("reversed", reverse(parse(spec)))):
        for sA in range(6):
            held, steps, sB = flex_atoms(T, sA)
            out.append((oname, sA, sB, held, steps))
    best = max(len(h) for _, _, _, h, _ in out)
    return best, [r for r in out if len(r[3]) == best]

def span_coeffs(steps):
    """span = (u+m+2)*CR + (u+3)*S01 + (m+1)*S10 + MK + TA + TU  ->  (a_u, a_m, const)"""
    CR, MK, TA = steps["crawl"], steps["marker"], steps["turnaround"]
    S10, S01, TU = steps["swap10"], steps["swap01"], steps["turn"]
    return (CR + S01, CR + S10, 2*CR + 3*S01 + S10 + MK + TA + TU)

def main():
    print("=== (0) CONTROLS: the named island under the BEHAVIOURAL test ===")
    for name, spec in ISLAND:
        best, hits = flex_scan(spec)
        if best == 6:
            o, sA, sB, _, st = hits[0]
            au, am, c = span_coeffs(st)
            print(f"  {name:3s}: 6/6  [{o}] sA={SC[sA]} sB={SC[sB]}  steps={[st[n] for n in NAMES]}"
                  f"  span={au}u+{am}m+{c}")
        else:
            miss = sorted(set(NAMES) - hits[0][3])
            print(f"  {name:3s}: {best}/6  missing {miss}")

    print()
    print("=== (1) THE RESIDUAL, behavioural test ===")
    for lname, path in LISTS[:1]:
        dist = Counter(); full = []; near = []
        total = 0
        with open(path) as fh:
            for line in fh:
                spec = line.strip().split()[0] if line.strip() else ""
                if not spec or spec.count('_') != 5: continue
                total += 1
                best, hits = flex_scan(spec)
                dist[best] += 1
                if best == 6: full.append((spec, hits[0]))
                elif best == 5: near.append((spec, hits[0]))
        print(f"  {lname}: {total} machines")
        for k in sorted(dist, reverse=True):
            print(f"     {k}/6 : {dist[k]:5d}")
        print(f"  FULL Atoms (behavioural): {len(full)}   [fixed-shape scan found 17]")
        sig = defaultdict(list)
        for spec, (o, sA, sB, _, st) in full:
            sig[tuple(st[n] for n in NAMES)].append(spec)
        print(f"  step-count signatures {NAMES}:")
        for k, v in sorted(sig.items(), key=lambda kv: -len(kv[1])):
            au, am, c = span_coeffs(dict(zip(NAMES, k)))
            print(f"     {list(k)} -> span {au}u+{am}m+{c}   : {len(v)} machine(s)")
            if len(v) <= 3:
                for s in v: print(f"          {s}")
        nm = Counter()
        for spec, (o, sA, sB, held, st) in near:
            nm[tuple(sorted(set(NAMES) - held))] += 1
        print(f"  5/6 near-misses: {len(near)}")
        for k, v in nm.most_common(6):
            print(f"     missing {list(k)}: {v}")



# ---------------------------------------------------------------------------
# Direction sequences, so a generator can emit the exact position normalisation
# each atom needs (`p - 1 + 1 - 1 - 1`, `p + 1 - 1 + 1 + 1 - 1`, ...).  Guessing
# it from the step count alone is wrong the moment an atom back-tracks -- the
# 5-step turn does exactly that.
ATOM_IN = {
    "crawl":      lambda: mk([1, 0, 1, 0, 1], 0, [1, 1, 0]),
    "marker":     lambda: mk([0, 1, 0, 1], 1, [1, 1, 0]),
    "turnaround": lambda: mk([0, 1, 0, 1], 0, [1, 1, 0]),
    "swap10":     lambda: mk([1, 0, 1], 1, [0, 1, 1, 0]),
    "swap01":     lambda: mk([1, 0, 1], 0, [1, 1, 1, 0]),
    "turn":       lambda: mk([1, 0, 1], 0, [0, 0, 1, 1, 0]),
}

def atom_dirs(T, st0, atom, k):
    """the ±1 move sequence of `atom`'s k steps, run from state st0"""
    tape = ATOM_IN[atom]()
    pos, st = 0, st0
    ds = []
    for _ in range(k):
        e = T[st][tape.get(pos, 0)]
        if e is None: return None
        w, d, nx = e
        if w: tape[pos] = 1
        elif pos in tape: del tape[pos]
        pos += d; st = nx
        ds.append(d)
    return ds

def pos_expr(ds):
    """'p - 1 + 1 - 1 - 1' etc."""
    return "p" + "".join(" + 1" if d == 1 else " - 1" for d in ds)

ATOM_TARGET = {"crawl": "p - 2", "marker": "p - 1", "turnaround": "p - 1",
               "swap10": "p + 2", "swap01": "p + 2", "turn": "p + 1"}
ATOM_START = {"crawl": "sA", "marker": "sA", "turnaround": "sA",
              "swap10": "sB", "swap01": "sB", "turn": "sB"}


def orbit_relevance(N=300000):
    """(2) Does each hit's REAL blank-tape orbit enter the tile's configuration family?

    Uses each machine's OWN span (the fixed-span version of this check in
    atoms_island_scan.py hard-coded D's 6(u+m)+15, which is wrong for the 5-step-turn hit).
    """
    print()
    print("=== (2) ORBIT RELEVANCE, per-machine span ===")
    print("    (Atoms true => tile is a true LEMMA.  Orbit entry => tile is ABOUT the machine.)")
    hits = []
    with open(LISTS[0][1]) as fh:
        for line in fh:
            spec = line.strip().split()[0] if line.strip() else ""
            if not spec or spec.count('_') != 5: continue
            best, hs = flex_scan(spec)
            if best == 6: hits.append((spec, hs[0]))
    print(f"  {'spec':46s} {'or':11s} sA span(lit)   halt?  IN-hits tile-fires")
    for spec, (o, sA, sB, _, st) in hits:
        T = parse(spec) if o == "as-written" else reverse(parse(spec))
        au, am, const = span_coeffs(st)
        # literal-m span: substitute m_lit = m+1  =>  au*u + am*(m_lit-1) + const
        cap = 1 << 21
        tape = bytearray(2 * cap); pos = cap; stt = 0
        halt_t = None; seen = set(); fired = 0
        for t in range(N):
            if stt == sA and tape[pos] == 0 and tape[pos + 1] == 1:
                g = 0
                while g < 64 and tape[pos + 2 + g] == 0: g += 1
                if g >= 3:
                    u = 0
                    while u < 2048 and tape[pos-1-2*u] == 1 and tape[pos-2-2*u] == 0: u += 1
                    i = pos - 1 - 2*u
                    if tape[i] == 1 and tape[i-1] == 1:
                        j = i - 2; mm = 0
                        while mm < 2048 and tape[j] == 0 and tape[j-1] == 1: mm += 1; j -= 2
                        if mm >= 1 and tape[j] == 0 and tape[j-1] == 0 and (u, mm, g) not in seen:
                            seen.add((u, mm, g))
                            sp = au*u + am*(mm-1) + const
                            cp = bytearray(tape); cq = pos; cs = stt; dead = False
                            for _ in range(sp):
                                e = T[cs][cp[cq]]
                                if e is None: dead = True; break
                                cp[cq] = e[0]; cq += e[1]; cs = e[2]
                            if not dead and cs == sA and cq == pos + 3: fired += 1
            e = T[stt][tape[pos]]
            if e is None: halt_t = t; break
            tape[pos] = e[0]; pos += e[1]; stt = e[2]
        hs_ = f"t={halt_t}" if halt_t is not None else "no"
        flag = "" if fired == len(seen) and fired else "   <== NOT 100%"
        print(f"  {spec:46s} {o:11s} {SC[sA]}  {au}u+{am}m+{const-am:<3d} {hs_:6s} {len(seen):7d} {fired:7d}{flag}")


if __name__ == "__main__":
    main()
    orbit_relevance()
