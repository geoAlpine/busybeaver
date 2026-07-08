#!/usr/bin/env python3
"""
o11 refill-law deep dive, part 1: ANATOMY (2026-07-08).
Instrument the real blank-tape orbit around the four observed collapse/refill events
(t ~ 10, 47, 272, 28101): record every right-extreme configuration change (any state)
inside the windows, plus every B/right-extreme milestone globally (with head offset
relative to the last 1) so the pure-collapse configuration (state, head placement)
is captured exactly for standalone re-seeding. [OBSERVED / exact simulation]
"""
import sys
from msea_struct2 import parse, rle_blocks

SPEC = "1RB1RE_1LC1LD_---1LA_1LB1LE_0RF0RA_1LD1RF"
SN = "ABCDEF"

def trace(N, windows):
    M = parse(SPEC)
    SZ = 1 << 23
    tape = bytearray(SZ)
    pos = SZ // 2
    st = 0
    lo = hi = pos
    step = 0
    win_events = []     # (step, state, blocks, head_off_last1) inside windows, any state, at right extreme
    milestones = []     # (step, blocks, head_off_last1) at state B + right extreme, RLE-deduped
    last_win = None
    last_mil = None
    while step < N:
        r = tape[pos]
        act = M[st][r]
        if act is None:
            print(f"HALT at step {step}")
            break
        if pos >= hi:
            in_win = any(a <= step <= b for a, b in windows)
            if in_win or st == 1:
                b = rle_blocks(tape, lo, hi)
                # head offset from last 1 (or from lo if tape blank)
                z = hi
                while z > lo and not tape[z]:
                    z -= 1
                off = pos - z
                if in_win and (st, b) != last_win:
                    win_events.append((step, st, b, off))
                    last_win = (st, list(b))
                if st == 1 and b != last_mil:
                    milestones.append((step, b, off))
                    last_mil = list(b)
        ww, d, ns = act
        tape[pos] = ww
        pos += d
        st = ns
        step += 1
        if pos < lo: lo = pos
        elif pos > hi: hi = pos
    return win_events, milestones

if __name__ == "__main__":
    N = int(sys.argv[1]) if len(sys.argv) > 1 else 100_000
    windows = [(0, 130), (240, 340), (27_800, 28_200)]
    win, mil = trace(N, windows)
    print("=== right-extreme events (any state, RLE-deduped) in collapse windows")
    for s, st, b, off in win:
        print(f"  t={s:>7}  {SN[st]}  off={off:+d}  {b if len(b) <= 14 else b[:14] + ['...']}")
    print()
    print("=== B/right-extreme milestones (deduped), head offset from last 1")
    for s, b, off in mil:
        tag = "PURE" if len(b) == 1 else ""
        print(f"  t={s:>10,}  off={off:+d}  {b if len(b) <= 12 else b[:12] + ['...']}  {tag}")
    print("No machine decided. No label upgraded.")
