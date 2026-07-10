#!/usr/bin/env python3
"""x2p_micro.py -- transition-level trace over a window, with local tape RLE + head marker,
to identify the exact macro-phases (eraser 2-cycle vs E-scanner repack vs return sweeps)."""
import sys
sys.path.insert(0, '/Users/aokiyousuke/busybeaver')
from mse_extract import parse

SPEC = "1RB0RE_1RC---_0LD1LE_0RE1LD_1RF0LC_0RA1RE"
STN = "ABCDEF"
M = parse(SPEC)


def show(tape, lo, hi, pos, st):
    s = []
    for i in range(lo, hi + 1):
        c = str(tape[i])
        if i == pos:
            c = f"[{STN[st]}{c}]"
        s.append(c)
    return ''.join(s)


def run(a, b, SZ=1 << 21):
    tape = bytearray(SZ); off = SZ // 2
    pos = off; st = 0; step = 0; lo = hi = pos
    while step < b:
        r = tape[pos]
        if st == 1 and r == 1:
            print(f"HALT {step}"); return
        if a <= step <= b:
            w0 = max(lo, pos - 10); w1 = min(hi, pos + 10)
            print(f"{step:>7} {STN[st]}@{pos-off:<5} r={r}  {show(tape,w0,w1,pos,st)}")
        act = M[st][r]
        ww, d, ns = act
        tape[pos] = ww; pos += d; st = ns; step += 1
        if pos < lo: lo = pos
        elif pos > hi: hi = pos


if __name__ == "__main__":
    a = int(sys.argv[1]); b = int(sys.argv[2])
    run(a, b)
