#!/usr/bin/env python3
"""
route18b (2026-07-25): o17 per-tick HEAD-PASS STRUCTURE — the decisive measurement
for "is the tick successor a finite-state (rational) string function?"

Fact used [PROVEN-in-lit]: a string function computed by a two-way device that makes
a BOUNDED number of monotone macro-passes, each with BOUNDED-amplitude jitter, is a
composition of boundedly many rational functions, hence rational (finite-state).
So per tick we decompose the head trajectory into maximal monotone runs and measure:
  - number of runs with amplitude >= J (macro-runs) per tick: bounded or growing?
  - max amplitude among sub-J runs (jitter bound): bounded?
  - leftmost reach per tick (does the head sweep the full string every tick?)

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

def tick_pass_trace(mu, digs, nticks, J=64, cap=10**10):
    """Per tick: decompose head path into maximal monotone runs.
    Record (n_macro_runs(>=J), max_small_amplitude, total_runs, leftreach_from_frontier,
            width)."""
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
    run_start = pos          # start position of current monotone run
    amps = []                # amplitudes of completed runs in current tick
    minpos = pos
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
            amps.append(abs(pos - run_start))
            macro = sum(1 for a in amps if a >= J)
            small = max((a for a in amps if a < J), default=0)
            out.append((macro, small, len(amps), minpos - lo, hi - lo + 1))
            amps = []; run_start = pos; minpos = pos
        if prevdir != 0 and d != prevdir:
            amps.append(abs(pos - run_start))
            run_start = pos
        prevdir = d
        tape[pos] = w; pos += d; st = ns; step += 1
        if pos < minpos: minpos = pos
        if pos > hi: hi = pos
        if pos < lo: lo = pos
    return out, ('CAP', step)

def analyze(name, out, J):
    print(f"\n  -- {name}: {len(out)} ticks (J={J})")
    macros = [m for m, s, t, l, w in out]
    smalls = [s for m, s, t, l, w in out]
    lefts  = [l for m, s, t, l, w in out]
    print(f"     macro-runs (amp>={J}) per tick: max={max(macros)}, "
          f"dist={Counter(macros).most_common(8)}")
    print(f"     max sub-{J} jitter amplitude: overall max={max(smalls)}, "
          f"dist(top)={Counter(smalls).most_common(6)}")
    print(f"     leftmost reach (cells from left frontier): min={min(lefts)}, "
          f"max={max(lefts)}, dist(top)={Counter(lefts).most_common(5)}")
    # trend: macro-run count first vs last quarter
    q = len(out) // 4
    print(f"     macro-run trend: mean first quarter={sum(macros[:q])/q:.2f}, "
          f"last quarter={sum(macros[-q:])/q:.2f}; width {out[0][4]} -> {out[-1][4]}")

if __name__ == "__main__":
    J = int(sys.argv[1]) if len(sys.argv) > 1 else 64
    for name, mu, digs, nt in [
        ("gate6->7 excursion (real orbit)", 3, [0, 2, 0, 0, 0, 0, 0, 16], 2000),
        ("gate7 era (deep)", 3, [2, 2, 0, 4] + [0]*14 + [512], 3000),
        ("C(9) runner era", 3, [0, 0, 0], 3000),
    ]:
        out, end = tick_pass_trace(mu, digs, nt, J=J, cap=300_000_000)
        analyze(name + f" end={end[0]}", out, J)
