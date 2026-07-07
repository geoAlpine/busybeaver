#!/usr/bin/env python3
"""
Mahler-sea survey — independent REPLAY of sampled fatal configs (2026-07-07).
Second implementation (dict tape, string states) re-runs a sample of the halting
standalone configs found by msea_fatal.py; must reproduce HALT at the same step.
"""
def parse(spec):
    M = {}
    for k, blk in enumerate(spec.split('_')):
        st = "ABCDEF"[k]
        for r in (0, 1):
            c = blk[3 * r:3 * r + 3]
            M[(st, r)] = None if c[0] == '-' else (int(c[0]), 1 if c[1] == 'R' else -1, c[2])
    return M

def replay(spec, blocks, gaps, head_rel, state, side, budget=400_000):
    M = parse(spec)
    tape = {}
    p = 0
    first1 = 0
    for i, b in enumerate(blocks):
        for _ in range(b):
            tape[p] = 1
            p += 1
        if i < len(gaps):
            p += gaps[i]
    last1 = p - 1
    pos = (first1 + head_rel) if side == 'L' else (last1 + head_rel)
    st = state
    for step in range(budget):
        a = M[(st, tape.get(pos, 0))]
        if a is None:
            return step
        w, d, ns = a
        if w == 0:
            tape.pop(pos, None)
        else:
            tape[pos] = w
        pos += d
        st = ns
    return None

CASES = [
    # (name, spec, blocks, gaps, head_rel, state, side, expected_halt_step)
    ("o11", "1RB1RE_1LC1LD_---1LA_1LB1LE_0RF0RA_1LD1RF", [2, 1], [1], 1, 'B', 'R', 19),
    ("o11", "1RB1RE_1LC1LD_---1LA_1LB1LE_0RF0RA_1LD1RF", [2, 1, 1, 1, 1], [1, 1, 1, 1], 1, 'B', 'R', 81),
    ("o12", "1RB0RE_1LC1LD_0RA0LD_1LB0LA_1RF1RA_---1LB", [2, 1, 1], [1, 1], -1, 'C', 'L', 50),
    ("o13", "1RB0LC_0LC0RF_1RD1LC_0RA1LE_---0LD_1LF1LA", [2, 1, 1], [1, 1], 0, 'C', 'L', 171),
    ("o14", "1RB0LC_1LC0RD_1LF1LA_1LB1RE_1RB1LE_---0LE", [2, 1, 1, 1, 1, 4, 4, 2], [1] * 7, 0, 'E', 'L', 222),
    ("o16", "1RB0LD_1RC1RA_1LD0RB_1LE1LA_1RF0RC_---1RE", [1, 1, 4], [2, 1], 0, 'A', 'R', 160),
]

if __name__ == "__main__":
    ok = True
    for name, spec, blocks, gaps, hr, st, side, exp in CASES:
        got = replay(spec, blocks, gaps, hr, st, side)
        match = (got == exp)
        ok &= match
        print(f"  {name}: blocks={blocks} -> HALT@{got} (expected {exp})  {'OK' if match else 'MISMATCH'}")
    print(f"\nINDEPENDENT REPLAY {'CONFIRMS' if ok else 'FAILS'} the sampled fatal configs.")
