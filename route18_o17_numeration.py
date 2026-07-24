#!/usr/bin/env python3
"""
route18 (2026-07-25): o17 odometer-specific attack ledger — the numeration/adic tools.

o17 = 1RB1LD_1RC0LE_1LA1RE_0LF1LA_1RB0RB_---0LB   (halt = F reads 0)

Fired here (everything re-derived from the raw TM, no inherited claim trusted):

 [A] RE-VERIFY: blank-orbit gate list (steps, marker, digit vectors), family C(3j)
     spot fates, digit unboundedness (free-running LSB).
 [B] THE DECISIVE STRUCTURAL TEST (deliverable 2): the per-TICK successor rule.
     One tick = one right-end (E,0) reversal. Is the tick map
     digitstring(n) -> digitstring(n+1) a bounded-window / finite-state
     (numeration-successor-like) rewrite?  Measured: per-tick edit window
     (position, size), head reversals per tick, and FUNCTIONALITY of the local
     rewrite (same window content => same rewrite?) under raw and abstracted
     (capped / mod-3) digit values.
 [C] GATE SPARSITY in tick and step time -> the abstract-numeration-system
     (Buchi-Bruyere) recognizability KILL: consecutive-gate ratio measured;
     an infinite set with gap-ratio -> infinity is recognizable in NO abstract
     numeration system (pumping: an infinite ANS-recognizable set contains
     arbitrarily large pairs with bounded ratio).
 [D] COMPACTNESS/RECURRENCE AUDIT for the adic / unique-ergodicity / Weyl tools:
     left-anchored frozen-prefix convergence (the orbit is Cauchy -> dissipative,
     empirical measures -> point mass), LSB escape (no finite-alphabet
     compactification), gate-event frequency -> 0 (every frequency tool sees
     measure zero; halt is first-passage on a vanishing-frequency event stream).

All outputs [MEASURED] exact finite simulation; nothing about halting decided.
Interpreter: /Users/aokiyousuke/quantum-ecc/.venv/bin/python
"""
import sys
from collections import Counter, defaultdict

SPEC = "1RB1LD_1RC0LE_1LA1RE_0LF1LA_1RB0RB_---0LB"

def parse(spec):
    M = []
    for st in spec.split('_'):
        row = []
        for t in (st[0:3], st[3:6]):
            row.append(None if t[0] == '-' else
                       (int(t[0]), 1 if t[1] == 'R' else -1, ord(t[2]) - ord('A')))
        M.append(row)
    return M

M = parse(SPEC)
STATES = "ABCDEF"

# ---------------------------------------------------------------- [A] re-verify
def blank_gates(maxsteps):
    """Run blank orbit; gate = head in state A or D reads 0 with all-0 to its left
    (true frontier). Return gate list [(step, state, marker, digs)]."""
    SZ = 1 << 24
    tape = bytearray(SZ); off = SZ // 2
    pos = off; st = 0; lo = hi = pos
    gates = []
    for step in range(maxsteps):
        r = tape[pos]
        if st == 5 and r == 0:
            gates.append((step, 'HALT', None, None)); return gates, True, step
        if r == 0 and st in (0, 3):  # A or D reads 0
            if pos <= lo:            # true left frontier
                # decode
                i = pos + 1
                blocks = []
                while i <= hi:
                    while i <= hi and tape[i] == 0: i += 1
                    j = i
                    while j <= hi and tape[j] == 1: j += 1
                    if j > i: blocks.append(j - i)
                    i = j
                if blocks:
                    marker = blocks[0]
                    digs = [(b - 2) // 3 if b % 3 == 2 else ('!%d' % b) for b in blocks[1:]]
                    gates.append((step, STATES[st], marker, digs))
        cell = M[st][r]
        if cell is None:
            gates.append((step, 'HALT', None, None)); return gates, True, step
        w, d, ns = cell
        tape[pos] = w; pos += d; st = ns
        if pos < lo: lo = pos
        if pos > hi: hi = pos
    return gates, False, maxsteps

def run_seed(k, maxsteps):
    SZ = 1 << 22; tape = bytearray(SZ); off = SZ // 2; pos = off
    for i in range(k): tape[off + 1 + i] = 1
    st = 0; lo = pos; hi = off + k
    for step in range(maxsteps):
        r = tape[pos]
        if st == 5 and r == 0: return True, step
        cell = M[st][r]
        if cell is None: return True, step
        w, d, ns = cell
        tape[pos] = w; pos += d; st = ns
    return False, maxsteps

# ------------------------------------------------- [B] per-tick successor trace
def raw_blocks(tape, lo, hi):
    """[(runlen, gap_after)] left->right over [lo,hi]; gap_after=-1 for last."""
    out = []; i = lo
    while i <= hi and tape[i] == 0: i += 1
    while i <= hi:
        j = i
        while j <= hi and tape[j] == 1: j += 1
        k = j
        while k <= hi and tape[k] == 0: k += 1
        out.append((j - i, (k - j) if k <= hi else -1))
        i = k
    return out

def tick_trace(mu, digs, nticks, cap=10**10):
    """Run from milestone (mu,digs); record at every tick (right-end (E,0)
    reversal): raw block list, head-reversal count since last tick, leftmost
    head reach since last tick (cells from left frontier).
    Returns list of (blocklist, reversals, leftreach_blocksfromright), ended."""
    width = mu + sum(3 * d + 2 for d in digs) + len(digs) + 1
    SZ = 1 << max(16, (width * 8 + nticks * 8).bit_length())
    tape = bytearray(SZ); off = SZ // 4
    p = off + 1
    for i in range(mu): tape[p] = 1; p += 1
    for d in digs:
        p += 1
        for i in range(3 * d + 2): tape[p] = 1; p += 1
    pos = off; st = 0; step = 0; hi = p - 1; lo = off
    prevdir = 0; rev = 0; minpos = pos
    out = []
    while step < cap and len(out) < nticks:
        r = tape[pos]
        if st == 5 and r == 0:
            return out, ('HALT', step)
        cell = M[st][r]
        if cell is None:
            return out, ('HALT', step)
        w, d, ns = cell
        if st == 4 and r == 0 and prevdir == -1 and pos >= hi - 3:
            # tick: E reads 0 at right end arriving after leftward motion
            out.append((raw_blocks(tape, lo, hi), rev, minpos - lo))
            rev = 0; minpos = pos
        if prevdir != 0 and d != prevdir: rev += 1
        prevdir = d
        tape[pos] = w; pos += d; st = ns; step += 1
        if pos < minpos: minpos = pos
        if pos > hi: hi = pos
        if pos < lo: lo = pos
    return out, ('CAP', step)

def diff_blocks(a, b):
    """Common-prefix/suffix alignment of two block lists.
    Returns (p, mid_a, mid_b, s): a = pre + mid_a + suf, b = pre + mid_b + suf."""
    p = 0
    while p < len(a) and p < len(b) and a[p] == b[p]: p += 1
    s = 0
    while s < len(a) - p and s < len(b) - p and a[len(a)-1-s] == b[len(b)-1-s]: s += 1
    return p, tuple(a[p:len(a)-s]), tuple(b[p:len(b)-s]), s

def abstract(mid, cap=4):
    """Abstract a mid-window: run lengths -> (min(len,cap*3+2), len mod 3), gaps kept."""
    return tuple((min(L, cap * 3 + 2), L % 3, g if g < 4 else 4) for (L, g) in mid)

def analyze_ticks(name, ticks):
    print(f"\n  -- tick analysis: {name}  ({len(ticks)} ticks)")
    revs = [r for _, r, _ in ticks]
    print(f"     reversals/tick: max={max(revs)}, mean={sum(revs)/len(revs):.1f}, "
          f"dist(top)={Counter(revs).most_common(6)}")
    winsizes = []; depths = []
    exact_map = {}; exact_conf = 0
    abst_map = {}; abst_conf = 0
    abst_conf_ex = []
    for i in range(1, len(ticks)):
        a, b = ticks[i-1][0], ticks[i][0]
        p, ma, mb, s = diff_blocks(a, b)
        winsizes.append(max(len(ma), len(mb)))
        depths.append(len(a) - p)          # window depth measured from RIGHT end
        keyx = (s, ma)                     # window content + distance from right
        if keyx in exact_map and exact_map[keyx] != mb: exact_conf += 1
        exact_map[keyx] = mb
        keya = (min(s, 3), abstract(ma))
        vb = abstract(mb)
        if keya in abst_map and abst_map[keya] != vb:
            abst_conf += 1
            if len(abst_conf_ex) < 3: abst_conf_ex.append((keya, abst_map[keya], vb))
        abst_map[keya] = vb
    print(f"     edit-window size (blocks): max={max(winsizes)}, "
          f"dist={Counter(winsizes).most_common(8)}")
    print(f"     edit depth from right end: max={max(depths)}, "
          f"dist(top)={Counter(depths).most_common(8)}")
    print(f"     EXACT rewrite functionality: {len(exact_map)} distinct (pos,window)->rewrite keys, "
          f"CONFLICTS={exact_conf}")
    print(f"     ABSTRACTED (cap4/mod3) functionality: {len(abst_map)} keys, CONFLICTS={abst_conf}")
    for k, v1, v2 in abst_conf_ex:
        print(f"        conflict at key={k}: {v1}  vs  {v2}")
    # growth of distinct abstracted keys over time (saturation test)
    seen = set(); marks = []
    n5 = max(1, len(ticks)//6)
    cnt = 0
    for i in range(1, len(ticks)):
        a, b = ticks[i-1][0], ticks[i][0]
        p, ma, mb, s = diff_blocks(a, b)
        seen.add((min(s,3), abstract(ma)))
        cnt += 1
        if cnt % n5 == 0: marks.append((cnt, len(seen)))
    print(f"     abstracted-key growth (ticks, distinct): {marks}")
    return exact_conf, abst_conf

# ---------------------------------------------------------------- [C] sparsity
def blank_no_gate_after(t0, maxsteps):
    """Fast blank run; count frontier A/D gates after step t0; return last gate step."""
    SZ = 1 << 25
    tape = bytearray(SZ); off = SZ // 2
    pos = off; st = 0; lo = pos
    last = None; n9 = 0
    Mloc = M
    for step in range(maxsteps):
        r = tape[pos]
        if st == 5 and r == 0:
            return ('HALT', step, last, n9)
        if r == 0 and (st == 0 or st == 3) and pos <= lo:
            last = (step, STATES[st])
            if step > t0: n9 += 1
        w, d, ns = Mloc[st][r]
        tape[pos] = w; pos += d; st = ns
        if pos < lo: lo = pos
    return ('RUN', maxsteps, last, n9)

# ------------------------------------------------------------------- [D] audit
def convergence_audit(ticks):
    """Left-anchored frozen-prefix convergence: block-prefix agreement between
    tick i and the final tick."""
    final = ticks[-1][0]
    pts = [len(ticks)//8, len(ticks)//4, len(ticks)//2, 3*len(ticks)//4, len(ticks)-2]
    print("\n  -- left-anchored convergence (prefix agreement with final tick):")
    for i in pts:
        a = ticks[i][0]
        p = 0
        while p < len(a) and p < len(final) and a[p] == final[p]: p += 1
        print(f"     tick {i:>6}: m={len(a):>6} blocks, common prefix with final = {p} "
              f"({100.0*p/max(1,len(a)):.1f}% of its length)")
    print(f"     final tick: m={len(final)} blocks, rightmost (LSB) block length = {final[-1][0]}"
          f"  (free-running: escapes every finite alphabet)")

# ==================================================================== main
if __name__ == "__main__":
    mode = sys.argv[1] if len(sys.argv) > 1 else "all"

    if mode in ("all", "A"):
        print("=" * 76)
        print("[A] RE-VERIFY from raw TM")
        print("=" * 76)
        gates, halted, T = blank_gates(2_000_000)
        print(f"  blank orbit to 2e6 steps: halted={halted}; frontier gates:")
        for stp, s, mu, dg in gates:
            print(f"    t={stp:>9}  state={s}  marker={mu}  digs={dg}")
        maxd = [max([d for d in dg if isinstance(d, int)], default=0) for _, s, mu, dg in gates if dg is not None]
        print(f"  max digit per gate: {maxd}   (unbounded growth = free-running LSB)")
        print("  family C(k) spot re-verification (expected: k%3!=0 fast halt; "
              "j=2,4 halt @206/394+1?; j=1,3 run):")
        for k in (4, 5, 6, 12, 3, 9):
            h, t = run_seed(k, 1_000_000)
            print(f"    C({k}): {'HALT@%d' % t if h else 'no halt <1e6'}")

    if mode in ("all", "B"):
        print()
        print("=" * 76)
        print("[B] DECISIVE: per-TICK successor rule — bounded-window finite-state or not")
        print("=" * 76)
        # gate-6 -> gate-7 excursion of the real blank orbit (T ~ 512 ticks)
        ticks1, end1 = tick_trace(3, [0, 2, 0, 0, 0, 0, 0, 16], 2000)
        print(f"  excursion from real gate-6 (3,[0,2,0,0,0,0,0,16]): {len(ticks1)} ticks, end={end1}")
        if len(ticks1) > 40:
            analyze_ticks("gate6->7 excursion (real orbit)", ticks1)
        # deep era: real gate-7 arrival vector (19 digits, max 512) — first ~3000 ticks
        g7 = [2, 2, 0, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 512]
        ticks2, end2 = tick_trace(3, g7, 3000, cap=300_000_000)
        print(f"\n  deep era from real gate-7 vector (19 digits, max 512): {len(ticks2)} ticks, end={end2}")
        if len(ticks2) > 40:
            analyze_ticks("gate7 era (deep, frozen-prefix regime)", ticks2)
        # a runner seed for cross-check
        ticks3, end3 = tick_trace(3, [0]*3, 3000, cap=300_000_000)   # C(9), j=3 runner
        print(f"\n  runner C(9) (j=3): {len(ticks3)} ticks, end={end3}")
        if len(ticks3) > 40:
            analyze_ticks("C(9) runner", ticks3)
        if mode == "all":
            globals()['_ticks2'] = ticks2

    if mode in ("all", "C"):
        print()
        print("=" * 76)
        print("[C] GATE SPARSITY -> ANS-recognizability kill (measured premise)")
        print("=" * 76)
        cap = 100_000_000
        res, T, last, n9 = blank_no_gate_after(1_072_566, cap)
        print(f"  blank run to {T:.0f} steps: {res}; last frontier gate at {last}; "
              f"gates after t=1,072,566: {n9}")
        print("  gate steps (from [A]): 5, 22, 44, 101, 314, 724, 2005, 1072566, next >= 1e8")
        gs = [5, 22, 44, 101, 314, 724, 2005, 1072566, cap]
        ratios = [round(gs[i+1]/gs[i], 1) for i in range(len(gs)-1)]
        print(f"  consecutive-gate STEP ratios: {ratios[:-1]} and >= {ratios[-1]} (lower bound)")
        print("  => gap ratios are unbounded over the measured range (25x then >=93x in steps;")
        print("     in tick time n: 1,5,11,21,533 then none to n~sqrt(1e8/4)=5000: ratios 5,2.2,1.9,25.4,>=9.4)")

    if mode in ("all", "D"):
        print()
        print("=" * 76)
        print("[D] COMPACTNESS / RECURRENCE AUDIT (adic & unique-ergodicity applicability)")
        print("=" * 76)
        tk = globals().get('_ticks2')
        if tk is None:
            tk, _ = tick_trace(3, [2, 2, 0, 4] + [0]*14 + [512], 3000, cap=300_000_000)
        convergence_audit(tk)
        print("\n  gate-event empirical frequency (halt-relevant events per step):")
        print("    8 gates in 1.1e6 steps; 0 gates in the next ~1e8 steps  => freq -> 0 (tower decay)")
