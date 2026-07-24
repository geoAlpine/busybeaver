#!/usr/bin/env python3
"""
route18c (2026-07-25): o17 per-tick CROSSING-NUMBER measurement (Hennie test).

If the max number of times the head crosses any single cell boundary WITHIN one tick
is uniformly bounded, the tick successor map has bounded crossing sequences and is
therefore a finite-state (Hennie/rational) string transduction [PROVEN-in-lit:
bounded crossing sequences => regular behavior]. If it grows with digit values /
carry depth, the tick map is not Hennie-computable (evidence against a regular
numeration successor at the ground level).

Also measured: whether per-tick jitter amplitude scales with planted digit values
(synthetic big-digit configs), i.e. whether the 6k+5 bounce ladder is carry-depth
(log-bounded per era) or digit-value (unbounded) driven.

[MEASURED] exact finite simulation; nothing about halting decided.
Interpreter: /Users/aokiyousuke/quantum-ecc/.venv/bin/python
"""
import sys
from collections import Counter

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

def crossing_trace(mu, digs, nticks, cap=10**10):
    """Per tick: max crossings of any cell boundary, plus max jitter amplitude.
    Crossing counter uses a version-stamped array (no per-tick reset cost)."""
    width = mu + sum(3 * d + 2 for d in digs) + len(digs) + 1
    SZ = 1 << max(16, (width * 8 + nticks * 8).bit_length())
    tape = bytearray(SZ); off = SZ // 4
    p = off + 1
    for i in range(mu): tape[p] = 1; p += 1
    for d in digs:
        p += 1
        for i in range(3 * d + 2): tape[p] = 1; p += 1
    pos = off; st = 0; step = 0; hi = p - 1; lo = off
    prevdir = 0
    cross = {}               # boundary index -> count (current tick)
    run_start = pos; maxamp = 0
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
            mc = max(cross.values()) if cross else 0
            amp = max(maxamp, abs(pos - run_start))
            out.append((mc, amp))
            cross = {}; run_start = pos; maxamp = 0
        if prevdir != 0 and d != prevdir:
            a = abs(pos - run_start)
            if a > maxamp and a < 10**6: maxamp = a
            run_start = pos
        prevdir = d
        # crossing boundary between pos and pos+d: index = min side
        b = pos if d == 1 else pos - 1
        cross[b] = cross.get(b, 0) + 1
        tape[pos] = w; pos += d; st = ns; step += 1
        if pos > hi: hi = pos
        if pos < lo: lo = pos
    return out, ('CAP', step)

def analyze(name, out):
    mcs = [m for m, a in out]
    amps = [a for m, a in out]
    print(f"  -- {name}: {len(out)} ticks")
    print(f"     max crossings/cell/tick: MAX={max(mcs)}, dist={Counter(mcs).most_common(10)}")
    q = max(1, len(out)//4)
    print(f"     trend: mean first quarter={sum(mcs[:q])/q:.2f}, last={sum(mcs[-q:])/q:.2f}")
    print(f"     max run amplitude/tick (incl. macro): MAX={max(amps)}")
    # amplitude ladder (excluding the single macro run): show second-largest structure
    print(f"     amplitude dist(top)={Counter(amps).most_common(6)}")

if __name__ == "__main__":
    print("=" * 76)
    print("[Hennie test] max crossings per cell within one tick")
    print("=" * 76)
    for name, mu, digs, nt in [
        ("gate6->7 + gate7 era (real)", 3, [0, 2, 0, 0, 0, 0, 0, 16], 1500),
        ("gate7 era (deep)", 3, [2, 2, 0, 4] + [0]*14 + [512], 2000),
        ("C(9) runner", 3, [0, 0, 0], 2000),
        ("synthetic big digits (3,[9,9,9,9])", 3, [9, 9, 9, 9], 800),
        ("synthetic big digits (3,[30,30,30])", 3, [30, 30, 30], 800),
        ("synthetic huge digit (3,[100,0,100])", 3, [100, 0, 100], 800),
    ]:
        out, end = crossing_trace(mu, digs, nt, cap=200_000_000)
        analyze(name + f" end={end[0]}@{end[1]}", out)
        print()
