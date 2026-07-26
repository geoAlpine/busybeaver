#!/usr/bin/env python3
"""RF-4, part 2 — the LEFTWARD turn phases, measured before anything is claimed.

`D_RF4_2026-07-27.md` closed the rightward turns (`RungCalc.tile2`).  Five of the k=4 epoch's
seven turn phases are left.  `RESUME` §3 records a GUESS about their shape —
"an `m=0` rung, then crawl + markerFold + crawl" — explicitly labelled `[UNVERIFIED]`.
This instrument checks that guess against the raw orbit instead of building on it.

It dumps, for each uncovered turn phase: the raw itinerary, an atom chunking, the head
trajectory, and the tape immediately before and after (head-relative RLE), so the actual
primitive is read off rather than assumed.
"""
from collections import Counter

DR = {0: [(1,-1,1), (0,-1,0)], 1: [(1,1,2), (0,1,4)], 2: [(0,1,3), (0,1,1)],
      3: [(1,-1,0), (0,1,5)], 4: [(1,1,1), (0,-1,3)], 5: [(1,1,3), None]}
SC = "ABCDEF"
CAP = 1 << 22
M1 = {4: 291168, 5: 1196412}

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

def rle(s, lo, hi):
    out = []
    for r in range(lo, hi + 1):
        b = s.t[s.p + r]
        if out and out[-1][0] == b: out[-1][1] += 1
        else: out.append([b, 1])
    return " ".join(f"{b}^{n}" if n > 1 else f"{b}" for b, n in out)

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

ATOMS = ["ABED", "BCD", "BE", "BC", "DF", "FD", "AB", "AE", "EB", "CB"]

def fmt(ch, maxn=60):
    parts = [f"({a})^{n}" if n > 1 else f"({a})" for a, n in ch]
    if len(parts) > maxn: parts = parts[:maxn//2] + ["..."] + parts[-maxn//2:]
    return " ".join(parts)

# the uncovered phases, from d_rf4_turns.py's segmentation of epoch M1(4)->M1(5)
TURNS = [(291168, 26), (291254, 180), (1168982, 6504), (1194806, 1371), (1196246, 166)]

s = Sim(); s.run(M1[4])
for (t0, n) in TURNS:
    s2 = Sim(); s2.run(t0)
    print("=" * 100)
    print(f"TURN t={t0}  ({n} steps)   state={SC[s2.st]} pos={s2.p - CAP:+d}")
    print(f"  BEFORE  left (tape order, r=-30..-1): {rle(s2, -30, -1)}")
    print(f"          head={s2.t[s2.p]}   right (r=+1..+30): {rle(s2, 1, 30)}")
    it = []
    traj = [0]
    p0 = s2.p
    for _ in range(n):
        it.append(SC[s2.st])
        s2.step()
        traj.append(s2.p - p0)
    print(f"  ITINERARY ({n}): {fmt(chunk(it, ATOMS))}")
    print(f"  head trajectory: start 0, min {min(traj):+d}, max {max(traj):+d}, end {traj[-1]:+d}")
    print(f"  AFTER   state={SC[s2.st]} pos={s2.p - CAP:+d} ({s2.p - p0:+d})")
    print(f"          left (tape order, r=-30..-1): {rle(s2, -30, -1)}")
    print(f"          head={s2.t[s2.p]}   right (r=+1..+30): {rle(s2, 1, 30)}")
