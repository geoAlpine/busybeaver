#!/usr/bin/env python3
"""x2p_erasecarry.py -- watch the ERASER cross an embedded even 'carry' gap.
Detect steps where a leftward-moving head in an erasing state (A/D/C) is about to enter
a maximal even 0-run of length >=4 that has 1s on BOTH sides (an embedded carry in the
odometer low region), and dump a micro-trace of the crossing. Question: does crossing a
carry ever create an ODD transient that the head's own E-substep then reads at the left?
Also: does the eraser's total output stay even (local even-preservation) or can the
carry interaction flip parity (counter-dependent)?"""
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
        if i == pos: c = f"[{STN[st]}{c}]"
        s.append(c)
    return ''.join(s)


def run(maxsteps, ncross, SZ=1 << 23):
    tape = bytearray(SZ); off = SZ // 2
    pos = off; st = 0; step = 0; lo = hi = pos
    dumping = 0
    crosses = 0
    while step < maxsteps and crosses <= ncross:
        r = tape[pos]
        if st == 1 and r == 1:
            print(f"HALT {step}"); return
        act = M[st][r]
        ww, d, ns = act
        # detect: erasing state moving left, about to enter an embedded even gap >=4
        if dumping == 0 and d == -1 and st in (0, 2, 3) and pos - 1 >= lo and tape[pos - 1] == 0:
            jj = pos - 1
            while jj >= lo and tape[jj] == 0: jj -= 1
            glen = (pos - 1) - jj
            if True:
                if jj >= lo and tape[jj] == 1 and glen >= 4 and glen % 2 == 0:
                    crosses += 1
                    if crosses <= ncross:
                        print(f"\n--- carry crossing #{crosses} at step {step}, "
                              f"embedded gap 0^{glen}, head {STN[st]} moving L ---")
                        dumping = glen + 25
        if dumping > 0:
            w0 = max(lo, pos - 12); w1 = min(hi, pos + 12)
            print(f"{step:>9} {STN[st]}@{pos-off:<6} r={r}  {show(tape,w0,w1,pos,st)}")
            dumping -= 1
        tape[pos] = ww; pos += d; st = ns; step += 1
        if pos < lo: lo = pos
        elif pos > hi: hi = pos


if __name__ == "__main__":
    cap = int(sys.argv[1]) if len(sys.argv) > 1 else 800000
    nc = int(sys.argv[2]) if len(sys.argv) > 2 else 2
    run(cap, nc)
