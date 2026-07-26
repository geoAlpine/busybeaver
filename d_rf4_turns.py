#!/usr/bin/env python3
"""RF-4 — D's turn phases, measured at atom resolution.

`D_SPEC_2026-07-26.md` §5 records the turn phases as `~2 steps/cell` with additive constants that
are "not a closed function of `k` alone", and §8 item 3 calls them "each a separate small lemma".
That is the largest remaining reverse-engineering gap for `D`, and it is NOT covered by the rung
tile.

This instrument does to the turn phases what `d_rung_atoms.py` did to the rung: segment the epoch
by rung-tile firings, then dump the state itinerary of everything in between and look for the
repeating primitive.  The question RF-4 really asks is:

    is a turn phase a FOLD of one uniform atom (like the rung's crawl / swap), or is it
    genuinely a per-segment special case?

If it folds, `RF-4` collapses from "enumerate k+1 constants per epoch" to "one more `∀` lemma
plus a boundary", and the additive constants become the boundary's, not free parameters.

Convention: `D^R`, the reversed form, exactly as `lean/DMachine.lean`'s `dT`.
"""
from collections import Counter

DR = {  # D^R = 1LB0LA_1RC0RE_0RD0RB_1LA0RF_1RB0LD_1RD---
    0: [(1, -1, 1), (0, -1, 0)],   # A0→1LB  A1→0LA
    1: [(1,  1, 2), (0,  1, 4)],   # B0→1RC  B1→0RE
    2: [(0,  1, 3), (0,  1, 1)],   # C0→0RD  C1→0RB
    3: [(1, -1, 0), (0,  1, 5)],   # D0→1LA  D1→0RF
    4: [(1,  1, 1), (0, -1, 3)],   # E0→1RB  E1→0LD
    5: [(1,  1, 3), None],         # F0→1RD  F1→HALT
}
SC = "ABCDEF"
CAP = 1 << 22

# milestone times on D^R (D_SPEC §2)
M1 = {4: 291168, 5: 1196412, 6: 4846662}

class Sim:
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

def read_IN(s):
    """If the config is in the rung tile's IN family, return (u,m,c,g); else None.
    IN: state A, head 0, right = 1 0^g ..., left (nearest-first) = (1 0)^u 1 1 (0 1)^m 0 0 1^c ...
    (that is tape order ... 1^c 0 0 (1 0)^m 1 1 (0 1)^u [0] 1 0^g ...)"""
    if s.st != 0 or s.t[s.p] != 0 or s.t[s.p + 1] != 1: return None
    g = 0
    while g < 1 << 20 and s.t[s.p + 2 + g] == 0: g += 1
    if g < 3: return None
    u = 0
    while s.t[s.p - 1 - 2 * u] == 1 and s.t[s.p - 2 - 2 * u] == 0: u += 1
    i = s.p - 1 - 2 * u
    if not (s.t[i] == 1 and s.t[i - 1] == 1): return None
    j = i - 2; m = 0
    while s.t[j] == 0 and s.t[j - 1] == 1: m += 1; j -= 2
    if m < 1 or not (s.t[j] == 0 and s.t[j - 1] == 0): return None
    k = j - 2; c = 0
    while s.t[k] == 1: c += 1; k -= 1
    return (u, m, c, g)

def chunk(it, atoms):
    out = []; i = 0
    while i < len(it):
        for a in atoms:
            if ''.join(it[i:i + len(a)]) == a:
                if out and out[-1][0] == a: out[-1][1] += 1
                else: out.append([a, 1])
                i += len(a); break
        else:
            out.append([it[i], 1]); i += 1
    return out

# atoms of the rung, plus every 2- and 3-cycle, so an unknown fold shows up as a run
ATOMS = ["ABED", "BCD", "BE", "BC", "DF", "FD", "AB", "AE", "EB", "CB"]

def fmt(ch):
    return " ".join(f"({a})^{n}" if n > 1 else f"({a})" for a, n in ch)

print("=== §1 segment / turn structure of one epoch, by rung-tile firing ===")
K = 4
s = Sim(); s.run(M1[K])
print(f"  ran to M1({K}) = {M1[K]}: state {SC[s.st]} pos {s.p - CAP:+d}")

END = M1[K + 1]
segs = []          # (kind, start_t, end_t, steps, detail)
cur_seg = None
itin = []
last_IN = None
t0 = s.n
while s.n < END:
    shape = read_IN(s)
    if shape is not None:
        u, m, c, g = shape
        span = 6 * (u + m) + 15
        if cur_seg is None:
            if itin:
                segs.append(("turn", t0, s.n, s.n - t0, list(itin)))
            cur_seg = [s.n, 0, shape, None]
            itin = []
        cur_seg[1] += 1
        cur_seg[3] = shape
        if not s.run(span): break
        continue
    if cur_seg is not None:
        segs.append(("ladder", cur_seg[0], s.n, s.n - cur_seg[0], (cur_seg[1], cur_seg[2], cur_seg[3])))
        cur_seg = None
        t0 = s.n
        itin = []
    itin.append(SC[s.st])
    if not s.step(): break
if cur_seg is not None:
    segs.append(("ladder", cur_seg[0], s.n, s.n - cur_seg[0], (cur_seg[1], cur_seg[2], cur_seg[3])))
elif itin:
    segs.append(("turn", t0, s.n, s.n - t0, list(itin)))

print(f"  epoch M1({K})->M1({K+1}) = {END - M1[K]} steps, decomposed into {len(segs)} pieces:")
for kind, a, b, n, det in segs:
    if kind == "ladder":
        rungs, sh0, sh1 = det
        print(f"    LADDER t={a:>9}..{b:<9} {n:>9} steps  rungs={rungs:<5} "
              f"IN0={sh0} -> IN_last={sh1}")
    else:
        print(f"    turn   t={a:>9}..{b:<9} {n:>9} steps  itinerary(first 60)={''.join(det[:60])}")

print()
print("=== §2 the turn itineraries, chunked into atoms ===")
for kind, a, b, n, det in segs:
    if kind != "turn": continue
    ch = chunk(det, ATOMS)
    comp = fmt(ch)
    print(f"  turn t={a} ({n} steps):")
    print(f"    {comp[:400]}{chr(10)+'    ...tail: '+comp[-160:] if len(comp) > 400 else ''}")
    print(f"    state histogram: {dict(Counter(det))}")

print()
print("=== §3 the tape at each turn-phase start (head-relative RLE) ===")
print("    If a turn is 'the rung with a longer return sweep', the LEFT context must be IN's")
print("    (0 1)^u 1 1 (1 0)^m 0 0 1^c and only the RIGHT context differs from `1 0^g`.")

def rle_rel(s, lo, hi):
    out = []
    for r in range(lo, hi + 1):
        b = s.t[s.p + r]
        if out and out[-1][0] == b: out[-1][1] += 1
        else: out.append([b, 1])
    return " ".join(f"{b}^{n}" if n > 1 else f"{b}" for b, n in out)

s2 = Sim(); s2.run(M1[K])
for kind, a, b, n, det in segs:
    if kind != "turn": continue
    s2.run(a - s2.n)
    assert s2.n == a
    ch = chunk(det, ATOMS)
    # the leading (ABED)^p and the second (ABED)^q, per the rung's shape
    lead = ch[0][1] if ch and ch[0][0] == "ABED" else 0
    print(f"  turn t={a} ({n} steps)  state={SC[s2.st]} lead=(ABED)^{lead}")
    print(f"     left  (nearest-first): {rle_rel(s2, -min(40, 40), -1)[::1]}")
    print(f"       [as read leftwards ] {' '.join(reversed(rle_rel(s2, -40, -1).split()))}")
    print(f"     head={s2.t[s2.p]}  right: {rle_rel(s2, 1, 60)}")
