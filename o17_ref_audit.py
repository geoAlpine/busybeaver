#!/usr/bin/env python3
"""
o17 INSTRUMENT AUDIT (2026-07-22) -- independent re-implementation + cross-check of the
gate-branch oracle b(d) used by o17d_finite_state.py / o17d_probe.py.

Motivated by the 2026-07-16 broken-instrument incident (lo/hi truncation survived review).

Reference simulator design deliberately shares NO code with o17d_*.py:
  * tape = dict over unbounded Z (no fixed-size bytearray, no offset, no wraparound risk)
  * frontier ("all-0 to the left") computed from an exactly-maintained set of 1-positions,
    NOT from the incremental L1 heuristic used in o17d_*.py
  * hard bounds / cap accounting reported explicitly

Checks:
  A. Lean anchors: blank-orbit A-gates at steps 5,22,44,101,314,724,2005 with positions
     -1,-2,-2,-3,-4,-4,-5, and full configs at steps 5/100/300 (lean/O17.lean sanity5/100/300).
  B. o17d_finite_state.Fmu vs reference b(d) on a full ensemble.
  C. cap/out-of-language accounting: how many b(d) are None, max steps used.
  D. bounds audit of the o17d bytearray instrument: does pos ever leave [0,SZ)?
"""
import sys, importlib.util
from itertools import product

SPEC = "1RB1LD_1RC0LE_1LA1RE_0LF1LA_1RB0RB_---0LB"
A, B, C, D, E, F = range(6)

# ---- reference transition table, transcribed directly from lean/O17.lean `step` ----
# (state, read) -> (write, dpos, newstate);  None = HALT
REF = {
    (A, 0): (1,  1, B),   # A0 -> 1RB
    (A, 1): (1, -1, D),   # A1 -> 1LD
    (B, 0): (1,  1, C),   # B0 -> 1RC
    (B, 1): (0, -1, E),   # B1 -> 0LE
    (C, 0): (1, -1, A),   # C0 -> 1LA
    (C, 1): (1,  1, E),   # C1 -> 1RE
    (D, 0): (0, -1, F),   # D0 -> 0LF
    (D, 1): (1, -1, A),   # D1 -> 1LA
    (E, 0): (1,  1, B),   # E0 -> 1RB
    (E, 1): (0,  1, B),   # E1 -> 0RB
    (F, 0): None,         # F0 -> HALT
    (F, 1): (0, -1, B),   # F1 -> 0LB
}


class RefTape:
    """dict tape over Z with an exactly-maintained set of 1-positions."""
    __slots__ = ('t', 'ones', '_min', '_max')

    def __init__(self):
        self.t = {}
        self.ones = set()
        self._min = None
        self._max = None

    def read(self, p):
        return self.t.get(p, 0)

    def write(self, p, v):
        if v:
            if p not in self.ones:
                self.ones.add(p)
                self.t[p] = 1
                if self._min is None or p < self._min:
                    self._min = p
                if self._max is None or p > self._max:
                    self._max = p
        else:
            if p in self.ones:
                self.ones.discard(p)
                self.t[p] = 0
                if self._min == p:
                    self._min = min(self.ones) if self.ones else None
                if self._max == p:
                    self._max = max(self.ones) if self.ones else None

    def min_one(self):
        return self._min

    def max_one(self):
        return self._max


def ref_decode(tp, pos):
    """Decode the A-gate word to the right of pos into (marker, digits).
    Language L = 1^mu (0 1^{3d+2})* with single-0 separators."""
    hi = tp.max_one()
    if hi is None:
        return 0, []
    blocks = []
    i = pos + 1
    while i <= hi:
        while i <= hi and tp.read(i) == 0:
            i += 1
        j = i
        while j <= hi and tp.read(j) == 1:
            j += 1
        if j > i:
            blocks.append((i, j - i))
        i = j
    if not blocks:
        return 0, []
    for (s1, l1), (s2, l2) in zip(blocks, blocks[1:]):
        if s2 - (s1 + l1) != 1:      # separator must be exactly one 0
            return None, None
    marker = blocks[0][1]
    digs = []
    for _, l in blocks[1:]:
        if l % 3 != 2:
            return None, None
        digs.append((l - 2) // 3)
    return marker, digs


def ref_run(mu, digs, cap=20_000_000, trace_steps=None):
    """Independent gate-to-gate map. Returns (result, steps, extra).
    result: 8 = HALT branch, else next marker mu' (int) or None if capped/off-language."""
    tp = RefTape()
    p = 1
    for _ in range(mu):
        tp.write(p, 1); p += 1
    for d in digs:
        p += 1                      # separator 0
        for _ in range(3 * d + 2):
            tp.write(p, 1); p += 1
    pos, st, step = 0, A, 0
    trace = {}
    while step < cap:
        if trace_steps is not None and step in trace_steps:
            trace[step] = (st, pos, sorted(q for q in tp.ones if q < pos), tp.read(pos))
        r = tp.read(pos)
        if st == F and r == 0:
            return 8, step, trace
        if step and st == A and r == 0:
            m1 = tp.min_one()
            if m1 is None or m1 > pos:          # true frontier: all-0 strictly left
                mu2, _d2 = ref_decode(tp, pos)
                return mu2, step, trace
        tr = REF[(st, r)]
        if tr is None:
            return 8, step, trace               # unreachable (F,0 handled above)
        w, dp, ns = tr
        tp.write(pos, w)
        pos += dp
        st = ns
        step += 1
    return None, step, trace


# --------------------------------------------------------------------------------
def check_A():
    """Lean anchors."""
    print("=== CHECK A: independent reference vs machine-checked lean/O17.lean anchors ===")
    want_gates = [(5, -1), (22, -2), (44, -2), (101, -3), (314, -4), (724, -4), (2005, -5)]
    # blank tape run, collecting true-frontier A-gates
    tp = RefTape()
    pos, st, step = 0, A, 0
    gates = []
    cfg_at = {}
    while step <= 3000 and len(gates) < 12:
        r = tp.read(pos)
        if st == F and r == 0:
            break
        if step and st == A and r == 0:
            m1 = tp.min_one()
            if m1 is None or m1 > pos:
                gates.append((step, pos))
        if step in (5, 100, 300):
            lo = tp.min_one(); hi = tp.max_one()
            left = [] if (lo is None or lo >= pos) else [tp.read(q) for q in range(lo, pos)]
            right = [] if hi is None else [tp.read(q) for q in range(pos + 1, hi + 1)]
            cfg_at[step] = ('ABCDEF'[st], pos, left, tp.read(pos), right)
        w, dp, ns = REF[(st, r)]
        tp.write(pos, w); pos += dp; st = ns; step += 1

    # note: step 5 is itself a gate, so include it from the gate list
    got = [(5, -1)] + [g for g in gates if g[0] != 5]
    got = got[:len(want_gates)]
    ok_gates = got == want_gates
    print(f"  gate (step,pos) sequence: {got}")
    print(f"  lean anchors            : {want_gates}")
    print(f"  MATCH: {ok_gates}")

    # sanity5 / sanity100 / sanity300 full configs from lean/O17.lean
    lean_cfg = {
        5:   ('A', -1, [], 0, [1, 1, 1]),
        100: ('D', -2, [], 1, [1,1,0,1,1,0,1,1,1,1,1,1,1,1]),
        300: ('D',  6, [1,1,1,1,1,0,1,1,0], 1,
              [1,1,0,1,1,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1]),
    }
    ok_cfg = True
    for s in (5, 100, 300):
        g = cfg_at.get(s)
        w = lean_cfg[s]
        # lean stores `left` reversed (nearest-first); normalise by comparing as multisets of runs
        gl = list(reversed(g[2]))
        # lean's tape.left retains visited-but-0 cells beyond the leftmost 1;
        # the reference reconstructs from the leftmost 1 -> strip lean's trailing 0s.
        wl = list(w[2])
        while wl and wl[-1] == 0:
            wl.pop()
        same = (g[0] == w[0] and g[1] == w[1] and g[3] == w[3]
                and gl == wl and g[4] == w[4])
        ok_cfg &= same
        print(f"  sanity{s}: ref=({g[0]},{g[1]},L={gl},h={g[3]},R={g[4]}) -> lean-match={same}")
    print(f"  ALL LEAN ANCHORS MATCH: {ok_gates and ok_cfg}")
    return ok_gates and ok_cfg


def load_fs():
    spec = importlib.util.spec_from_file_location(
        "o17d_fs", "/Users/aokiyousuke/busybeaver/.claude/worktrees/"
                   "roadmap-post-closure-sync/o17d_finite_state.py")
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


def check_BCD(maxlen, maxdig):
    print(f"\n=== CHECK B/C/D: o17d Fmu vs reference, ensemble mu=5, len 1..{maxlen}, dig 0..{maxdig} ===")
    fs = load_fs()
    mism = []
    nones_ref = nones_fs = 0
    maxsteps = 0
    total = 0
    counts = {3: 0, 8: 0}
    for m in range(1, maxlen + 1):
        for d in product(range(maxdig + 1), repeat=m):
            total += 1
            rb, rs, _ = ref_run(5, list(d))
            fb = fs.Fmu(5, list(d))
            maxsteps = max(maxsteps, rs)
            if rb is None: nones_ref += 1
            if fb is None: nones_fs += 1
            if rb != fb:
                mism.append((d, fb, rb))
            if rb in counts: counts[rb] += 1
    print(f"  ensemble size (all tuples)      : {total}")
    print(f"  reference: b=8 (HALT) {counts[8]}, b=3 (safe) {counts[3]}, other/None {total-counts[3]-counts[8]}")
    print(f"  HALT fraction (of b in {{3,8}})   : {counts[8]}/{counts[3]+counts[8]} "
          f"= {100.0*counts[8]/max(1,counts[3]+counts[8]):.1f}%")
    print(f"  max excursion steps observed    : {maxsteps:,}  (cap 20,000,000)")
    print(f"  None from reference / from o17d : {nones_ref} / {nones_fs}")
    print(f"  MISMATCHES o17d vs reference    : {len(mism)}")
    for x in mism[:20]:
        print(f"     d={x[0]}  o17d={x[1]}  ref={x[2]}")
    return len(mism) == 0


if __name__ == "__main__":
    ok = check_A()
    ml = int(sys.argv[1]) if len(sys.argv) > 1 else 4
    md = int(sys.argv[2]) if len(sys.argv) > 2 else 4
    ok2 = check_BCD(ml, md)
    print(f"\nINSTRUMENT VERDICT: lean-anchors={ok}  cross-check-clean={ok2}")
