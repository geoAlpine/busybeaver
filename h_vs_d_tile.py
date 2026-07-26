#!/usr/bin/env python3
"""CHEAP INSURANCE (SYNTHESIS Tier I-2): does D's rung tile fire on H?

A's claim that H is a cheap same-species re-instantiation was demoted to
[unverified] when D turned out to be a cascade rather than a pure comb.  Now that
D's rung tile is PROVEN in Lean, the question has a sharp, cheap form:

  (1) Is H's transition graph a RELABELING of D's?  If yes the whole of
      `lean/DMachine.lean` transports by renaming states, and H is nearly free.
      (This is exactly why C was free: C was x2's graph.)
  (2) If not: do D's ATOMS still occur in H as local motifs?  D's tile is built
      from just four of them -- the ABED crawl, the two B-to-B transposition
      atoms, and the BCD turn.  Each is a short state/read pattern that can be
      searched for under any relabeling.
  (3) And regardless of the graph: does H's own orbit exhibit the tile's
      SIGNATURE -- head advance +3 per rung, width +3, span 6*(u+m)+15?

Reports facts only.  Decides no machine, upgrades no label.
"""
import itertools

D_SPEC = "1RB0RA_1LC0LE_0LD0LB_1RA0LF_1LB0RD_1LD---"
H_SPEC = "1RB0RE_0RC0RA_1LD1RE_1LA0LD_1RA0LF_1LD---"

def parse(spec):
    """-> table[state][read] = (write, dir, next) or None for HALT; dir +1=R, -1=L"""
    T = []
    for blk in spec.split('_'):
        row = []
        for k in (0, 3):
            f = blk[k:k+3]
            row.append(None if f[0] == '-' else (int(f[0]), 1 if f[1] == 'R' else -1, ord(f[2]) - 65))
        T.append(row)
    return T

def reverse(T):
    """the mirror machine: flip every direction (this is the `^R` of the Lean files)"""
    return [[None if e is None else (e[0], -e[1], e[2]) for e in row] for row in T]

def show(T):
    L = "ABCDEF"
    return "_".join(
        "".join("---" if e is None else f"{e[0]}{'R' if e[1] == 1 else 'L'}{L[e[2]]}" for e in row)
        for row in T)

# ---------------------------------------------------------------- (1) relabeling
def relabel(T, perm):
    """apply the state permutation `perm` (perm[i] = new index of old state i)"""
    n = len(T)
    out = [None] * n
    for i, row in enumerate(T):
        out[perm[i]] = [None if e is None else (e[0], e[1], perm[e[2]]) for e in row]
    return out

def find_iso(T1, T2):
    """all state permutations carrying T1 to T2, requiring start state -> start state"""
    n = len(T1)
    hits = []
    for tail in itertools.permutations(range(1, n)):
        perm = (0,) + tail                        # state A must stay the start state
        if relabel(T1, perm) == T2:
            hits.append(perm)
    return hits

print("=== (1) is H's graph a relabeling of D's? ===")
D, H = parse(D_SPEC), parse(H_SPEC)
DR, HR = reverse(D), reverse(H)
print(f"  D  = {show(D)}")
print(f"  D^R= {show(DR)}   <- this is DMachine.dT")
print(f"  H  = {show(H)}")
print(f"  H^R= {show(HR)}")
for n1, T1 in (("D", D), ("D^R", DR)):
    for n2, T2 in (("H", H), ("H^R", HR)):
        hits = find_iso(T1, T2)
        print(f"  {n1} -> {n2}: {len(hits)} relabeling(s)" + (f"  {hits[0]}" if hits else ""))

# ------------------------------------------------------------------- (2) motifs
# D^R's four tile atoms, as (start_state, read) -> ... chains, written in terms of
# the LOCAL pattern only (state names abstracted away).  Each atom is a walk in the
# transition graph together with the cell values it reads and writes.
#
#   ABED crawl : (s0,0)->(w=1,L,s1) (s1,1)->(w=0,R,s2) (s2,1)->(w=0,L,s3) (s3,0)->(w=1,L,s0)
#   swap10     : (s0,1)->(w=0,R,s1) (s1,0)->(w=1,R,s0)
#   swap01     : (s0,0)->(w=1,R,s1) (s1,1)->(w=0,R,s0)
#   turn       : (s0,0)->(w=1,R,s1) (s1,0)->(w=0,R,s2) (s2,0)->(w=1,L,s3)
ATOMS = {
    # name: list of (read, write, dir, "same as step k's target" / "back to start")
    "ABED crawl (4, head -2, tape-preserving, closes)":
        [(0, 1, -1), (1, 0, +1), (1, 0, -1), (0, 1, -1)],
    "swap10 (2, head +2, 1 0 -> 0 1, closes)":
        [(1, 0, +1), (0, 1, +1)],
    "swap01 (2, head +2, 0 1 -> 1 0, closes)":
        [(0, 1, +1), (1, 0, +1)],
    "turn (3, head +1, deposits the new 1, open)":
        [(0, 1, +1), (0, 0, +1), (0, 1, -1)],
}

def find_atom(T, chain, must_close):
    """all state-walks in T realising `chain` = [(read,write,dir)...];
    must_close: the walk must return to its starting state."""
    n = len(T)
    hits = []
    for s0 in range(n):
        s = s0
        path = [s0]
        ok = True
        for (r, w, d) in chain:
            e = T[s][r]
            if e is None or e[0] != w or e[1] != d:
                ok = False
                break
            s = e[2]
            path.append(s)
        if ok and (not must_close or s == s0):
            hits.append(path)
    return hits

print()
print("=== (2) do D's tile atoms occur in H, under ANY state relabeling? ===")
L = "ABCDEF"
for name, chain in ATOMS.items():
    close = name.endswith("closes)")
    dh = find_atom(DR, chain, close)
    hh = find_atom(HR, chain, close)
    hf = find_atom(H,  chain, close)
    fmt = lambda hits: ", ".join("".join(L[s] for s in p) for p in hits) or "NONE"
    print(f"  {name}")
    print(f"      D^R: {fmt(dh)}")
    print(f"      H^R: {fmt(hh)}")
    print(f"      H  : {fmt(hf)}")

# --------------------------------------------------------------- (3) signature
def sim(T, N, cap=1 << 22):
    """run from blank; return per-step (state,pos) and the frontier records"""
    tape = bytearray(2 * cap)
    pos = cap
    st = 0
    lo = hi = pos
    hist = []
    for t in range(N):
        r = tape[pos]
        e = T[st][r]
        if e is None:
            return hist, t, (lo - cap, hi - cap), tape, cap
        w, d, nx = e
        tape[pos] = w
        pos += d
        st = nx
        lo = min(lo, pos); hi = max(hi, pos)
        hist.append((t + 1, st, pos - cap))
    return hist, None, (lo - cap, hi - cap), tape, cap

print()
print("=== (3) the tile SIGNATURE on the real orbits: +3 head advance per rung ===")
print("    D's rung: state A, head +3, span 6(u+m)+15 with u,m advancing by (+2,-1).")
print("    Look for the same shape: returns to the outward-sweep state at head +3.")
for name, T in (("D^R", DR), ("H^R", HR), ("H", H)):
    hist, halt, win, tape, cap = sim(T, 400000)
    # for each state, collect the multiset of head displacements between consecutive
    # visits at which the head is at a NEW record (rung boundaries live there)
    from collections import defaultdict
    last = {}
    deltas = defaultdict(lambda: defaultdict(int))
    for (t, st, p) in hist:
        if st in last:
            deltas[st][p - last[st][1]] += 1
        last[st] = (t, p)
    print(f"  {name}: halt={halt} window={win}")
    for st in range(6):
        d = deltas[st]
        if not d:
            continue
        top = sorted(d.items(), key=lambda kv: -kv[1])[:4]
        print(f"      state {L[st]}: top head-deltas between consecutive visits "
              + " ".join(f"{k:+d}x{v}" for k, v in top))
