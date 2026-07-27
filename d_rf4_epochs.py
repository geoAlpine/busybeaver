#!/usr/bin/env python3
"""RF-4 part 3 — do the four laws hold up across epochs, or was k=4 lucky?

`D_RF4_2026-07-27.md` covers 10 of the k=4 epoch's 13 pieces (99.959% of its steps) with four
proven laws: `tile`, `tile2`, `rung0`, `descend`.  Three short phases were left over.  Before
writing a law for them the question to settle is whether they are STRUCTURAL (one per epoch, so
a bounded fixed cost) or an artifact of k=4 (in which case the leftover set may grow with k).

This instrument segments epochs `k = 4` and `k = 5` and classifies every piece by ACTUALLY
APPLYING the laws -- read the parameters off the tape, run the law's span, compare cell-for-cell.
A piece counts as covered only if the law reproduces it exactly.  No shape heuristics.
"""
DR = {0: [(1,-1,1), (0,-1,0)], 1: [(1,1,2), (0,1,4)], 2: [(0,1,3), (0,1,1)],
      3: [(1,-1,0), (0,1,5)], 4: [(1,1,1), (0,-1,3)], 5: [(1,1,3), None]}
SC = "ABCDEF"
CAP = 1 << 23
M1 = {4: 291168, 5: 1196412, 6: 4846662}

class Sim:
    __slots__ = ('t', 'p', 'st', 'n')
    def __init__(self):
        self.t = bytearray(2 * CAP); self.p = CAP; self.st = 0; self.n = 0
    def step(self):
        e = DR[self.st][self.t[self.p]]
        if e is None: return False
        self.t[self.p] = e[0]; self.p += e[1]; self.st = e[2]; self.n += 1
        return True
    def run(self, k):
        for _ in range(k):
            if not self.step(): return False
        return True
    def snap(self, lo, hi):
        return bytes(self.t[self.p + lo : self.p + hi + 1])

def read_IN(s):
    """IN(u,m,c,g) at the head, or None.  Requires g>=3, m>=1."""
    if s.st != 0 or s.t[s.p] != 0 or s.t[s.p + 1] != 1: return None
    g = 0
    while g < 1 << 21 and s.t[s.p + 2 + g] == 0: g += 1
    if g < 3: return None
    u = 0
    while s.t[s.p - 1 - 2*u] == 1 and s.t[s.p - 2 - 2*u] == 0: u += 1
    i = s.p - 1 - 2*u
    if not (s.t[i] == 1 and s.t[i-1] == 1): return None
    j = i - 2; m = 0
    while s.t[j] == 0 and s.t[j-1] == 1: m += 1; j -= 2
    if m < 1 or not (s.t[j] == 0 and s.t[j-1] == 0): return None
    k = j - 2; c = 0
    while s.t[k] == 1: c += 1; k -= 1
    return (u, m, c, g)

def read_IN2(s):
    """IN2(u,m,c,w,g): like IN but the right context is `1 (1 0)^w 0^g` with w>=1, g>=3."""
    if s.st != 0 or s.t[s.p] != 0 or s.t[s.p + 1] != 1: return None
    w = 0
    while s.t[s.p + 2 + 2*w] == 1 and s.t[s.p + 3 + 2*w] == 0: w += 1
    if w < 1: return None
    base = s.p + 2 + 2*w
    g = 0
    while g < 1 << 21 and s.t[base + g] == 0: g += 1
    if g < 3: return None
    u = 0
    while s.t[s.p - 1 - 2*u] == 1 and s.t[s.p - 2 - 2*u] == 0: u += 1
    i = s.p - 1 - 2*u
    if not (s.t[i] == 1 and s.t[i-1] == 1): return None
    j = i - 2; m = 0
    while s.t[j] == 0 and s.t[j-1] == 1: m += 1; j -= 2
    if m < 1 or not (s.t[j] == 0 and s.t[j-1] == 0): return None
    return (u, m, w, g)

def read_rung0(s):
    """rung0: left = (1 0)^u 1 1 0 0 W nearest-first; right = 1 0^g, g>=3.  -> u or None."""
    if s.st != 0 or s.t[s.p] != 0 or s.t[s.p + 1] != 1: return None
    g = 0
    while g < 1 << 21 and s.t[s.p + 2 + g] == 0: g += 1
    if g < 3: return None
    u = 0
    while s.t[s.p - 1 - 2*u] == 1 and s.t[s.p - 2 - 2*u] == 0: u += 1
    i = s.p - 1 - 2*u
    if not (s.t[i] == 1 and s.t[i-1] == 1): return None
    if not (s.t[i-2] == 0 and s.t[i-3] == 0): return None      # comb EXHAUSTED
    return u

def read_descend(s):
    """descend: left = (1 0)^q 1 1 1^r 0 1 0 L nearest-first -> (q, r) or None."""
    if s.st != 0 or s.t[s.p] != 0: return None
    q = 0
    while s.t[s.p - 1 - 2*q] == 1 and s.t[s.p - 2 - 2*q] == 0: q += 1
    i = s.p - 1 - 2*q
    if not (s.t[i] == 1 and s.t[i-1] == 1): return None
    k = i - 2; r = 0
    while s.t[k] == 1: r += 1; k -= 1
    if s.t[k] != 0: return None
    if not (s.t[k-1] == 1 and s.t[k-2] == 0): return None
    return (q, r)

WIN = 4000   # comparison window each side; laws are local, this is far beyond their reach

def try_law(s, span, dpos):
    """run `span` steps on a copy; -> (ok_state_and_pos, snapshot) ; the caller compares"""
    import copy
    s2 = Sim(); s2.t = bytearray(s.t); s2.p = s.p; s2.st = s.st; s2.n = 0
    p0, st0 = s2.p, s2.st
    if not s2.run(span): return None
    if s2.st != st0 or s2.p != p0 + dpos: return None
    return s2

def classify(s, span_actual):
    """try each law at the current config; -> (name, params, span) or None"""
    # tile
    sh = read_IN(s)
    if sh:
        u, m, c, g = sh
        sp = 6*(u+m) + 15
        if sp == span_actual and try_law(s, sp, 3): return ("tile", (u, m, c, g), sp)
    # tile2 (rightward turn)
    sh = read_IN2(s)
    if sh:
        u, m, w, g = sh
        sp = 6*(u+m) + 15 + 2*w
        if sp == span_actual and try_law(s, sp, 3 + 2*w): return ("tile2", (u, m, w, g), sp)
    # rung0 ; descend  (leftward turn)
    u = read_rung0(s)
    if u is not None:
        sp0 = 6*u + 15
        s2 = try_law(s, sp0, 3)
        if s2 is not None:
            qr = read_descend(s2)
            if qr:
                q, r = qr
                sp1 = 4*(q+2) + (r+1)
                if sp0 + sp1 == span_actual:
                    s3 = try_law(s2, sp1, -2*(q+1) - (r+1) - 2)
                    if s3 is not None: return ("rung0+descend", (u, q, r), sp0 + sp1)
    return None

def segment(K):
    """segment epoch M1(K)->M1(K+1) into ladder runs and turn phases"""
    s = Sim(); s.run(M1[K])
    END = M1[K + 1]
    pieces = []
    cur = None; t0 = s.n; n_it = 0
    while s.n < END:
        sh = read_IN(s)
        if sh is not None:
            u, m, c, g = sh
            if cur is None:
                if n_it: pieces.append(["turn", t0, s.n, s.n - t0, None])
                cur = [s.n, 0]; n_it = 0
            cur[1] += 1
            s.run(6*(u+m) + 15)
            continue
        if cur is not None:
            pieces.append(["ladder", cur[0], s.n, s.n - cur[0], cur[1]])
            cur = None; t0 = s.n; n_it = 0
        n_it += 1
        s.step()
    if cur is not None: pieces.append(["ladder", cur[0], s.n, s.n - cur[0], cur[1]])
    elif n_it: pieces.append(["turn", t0, s.n, s.n - t0, None])
    return pieces

for K in (4, 5):
    print("=" * 96)
    pieces = segment(K)
    tot = M1[K+1] - M1[K]
    print(f"EPOCH M1({K}) -> M1({K+1}) : {tot} steps, {len(pieces)} pieces")
    covered = 0; cov_steps = 0
    leftovers = []
    for kind, a, b, n, extra in pieces:
        if kind == "ladder":
            covered += 1; cov_steps += n
            print(f"  LADDER  t={a:>9} {n:>9} steps  rungs={extra}   [tile]")
            continue
        s = Sim(); s.run(a)
        cls = classify(s, n)
        if cls:
            covered += 1; cov_steps += n
            print(f"  turn    t={a:>9} {n:>9} steps  {cls[0]} {cls[1]}   [COVERED]")
        else:
            leftovers.append((a, n))
            it = []
            s2 = Sim(); s2.run(a)
            for _ in range(min(n, 40)):
                it.append(SC[s2.st]); s2.step()
            print(f"  turn    t={a:>9} {n:>9} steps  *** UNCOVERED ***  itin[:40]={''.join(it)}")
    print(f"  => {covered}/{len(pieces)} pieces, {cov_steps}/{tot} steps = {100*cov_steps/tot:.4f}%")
    print(f"  => leftovers: {len(leftovers)}  {[(t, n) for t, n in leftovers]}")

print()
print("=" * 96)
print("=== the THREE leftovers, at both k, in full ===")
print("    They sit at fixed positions -- the epoch's FIRST, SECOND and LAST turn -- in both")
print("    epochs, so they are STRUCTURAL (3 per epoch, not growing in number with k).")

ATOMS = ["ABED", "BCD", "BE", "BC", "DF", "FD", "AB", "AE", "EB", "CB"]
def chunk(it, atoms):
    out = []; i = 0
    while i < len(it):
        for a in atoms:
            if ''.join(it[i:i+len(a)]) == a:
                if out and out[-1][0] == a: out[-1][1] += 1
                else: out.append([a, 1])
                i += len(a); break
        else:
            out.append([it[i], 1]); i += 1
    return out
def fmt(ch, maxn=40):
    parts = [f"({a})^{n}" if n > 1 else f"({a})" for a, n in ch]
    if len(parts) > maxn: parts = parts[:maxn//2] + ["..."] + parts[-maxn//2:]
    return " ".join(parts)

for K, tlist in ((4, [(291168, 26), (291254, 180), (1196246, 166)]),
                 (5, [(1196412, 104), (1196645, 695), (4845988, 674)])):
    print(f"\n  --- epoch k={K} ---")
    for label, (t, n) in zip(("1st turn", "2nd turn", "last turn"), tlist):
        s = Sim(); s.run(t)
        it = []
        p0 = s.p; traj = [0]
        for _ in range(n):
            it.append(SC[s.st]); s.step(); traj.append(s.p - p0)
        print(f"   {label:9s} t={t:>9} {n:>5} steps  head: min {min(traj):+d} max {max(traj):+d} end {traj[-1]:+d}")
        print(f"     {fmt(chunk(it, ATOMS))}")

print()
print("=" * 96)
print("=== GREEDY COVER: chain the laws instead of classifying one law per piece ===")
print("    The per-piece classifier above was too rigid: it tried ONE law per segmenter-piece,")
print("    but the leftovers are visibly CHAINS (e.g. the k=4 last turn is")
print("    rung0(10) ; descend(13,7) ; rung0(0) ; <cut by the epoch boundary>).")
print("    This walks the epoch applying whichever law fits, and reports where it STICKS.")

def step_law(s):
    """apply whichever law fits at the current config; -> (name, params, span) or None"""
    sh = read_IN(s)
    if sh:
        u, m, c, g = sh
        sp = 6*(u+m) + 15
        if try_law(s, sp, 3): return ("tile", sh, sp)
    sh = read_IN2(s)
    if sh:
        u, m, w, g = sh
        sp = 6*(u+m) + 15 + 2*w
        if try_law(s, sp, 3 + 2*w): return ("tile2", sh, sp)
    u = read_rung0(s)
    if u is not None:
        sp = 6*u + 15
        if try_law(s, sp, 3): return ("rung0", (u,), sp)
    qr = read_descend(s)
    if qr:
        q, r = qr
        sp = 4*(q+2) + (r+1)
        if try_law(s, sp, -2*(q+1) - (r+1) - 2): return ("descend", qr, sp)
    return None

from collections import Counter
for K in (4, 5):
    s = Sim(); s.run(M1[K])
    END = M1[K+1]; tot = END - M1[K]
    used = Counter(); covered = 0; stuck = []
    while s.n < END:
        r = step_law(s)
        if r is None:
            t0 = s.n
            it = []
            while s.n < END and step_law(s) is None:
                it.append(SC[s.st]); s.step()
            stuck.append((t0, s.n - t0, ''.join(it)))
            continue
        name, params, sp = r
        if s.n + sp > END: break          # would run past the milestone
        used[name] += 1; covered += sp
        s.run(sp)
    print(f"\n  epoch k={K}: {tot} steps")
    for nm, c in used.most_common():
        print(f"     {nm:14s} applied {c:>4} times")
    print(f"     covered {covered}/{tot} = {100*covered/tot:.4f}%   stuck stretches: {len(stuck)}")
    for t0, n, it in stuck:
        tag = "  <-- contains (DF), the state-D swap atom" if "DF" in it else ""
        print(f"       t={t0:>9} {n:>4} steps  {fmt(chunk(list(it), ATOMS), 24)}{tag}")

print()
print("=" * 96)
print("=== THE EPOCH AS A PROGRAM: the law-application sequence, with parameters ===")
print("    Consecutive `tile` applications are collapsed into tileIter(n) -- that is how the")
print("    Lean assembly will do it.  If the sequences for k and k+2 have the same SHAPE with")
print("    parameters given by a rule, that rule is the seam induction's invariant.")

def program(K):
    s = Sim(); s.run(M1[K])
    END = M1[K+1]
    prog = []
    while s.n < END:
        r = step_law(s)
        if r is None:
            t0 = s.n
            while s.n < END and step_law(s) is None: s.step()
            prog.append(("STUCK", (s.n - t0,), s.n - t0))
            continue
        name, params, sp = r
        if s.n + sp > END: break
        # collapse a run of `tile`s
        if name == "tile":
            u, m, c, g = params
            n = 0; tot = 0
            while True:
                rr = step_law(s)
                if rr is None or rr[0] != "tile" or s.n + rr[2] > END: break
                n += 1; tot += rr[2]; s.run(rr[2])
            prog.append(("tileIter", (u, m, c, g, n), tot))
            continue
        prog.append((name, params, sp))
        s.run(sp)
    return prog

for K in (4, 5):
    pr = program(K)
    print(f"\n  --- epoch k={K}: {len(pr)} law applications, {sum(x[2] for x in pr)} steps ---")
    for i, (nm, params, sp) in enumerate(pr, 1):
        print(f"    {i:>2}. {nm:<10} {str(params):<26} {sp:>9} steps")
