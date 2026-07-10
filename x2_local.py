#!/usr/bin/env python3
"""Local window at each state-B visit + early full trace, to see WHY B reads 0."""
import sys
sys.path.insert(0, '/Users/aokiyousuke/busybeaver')
from mse_extract import parse, rle
SPEC = "1RB0RE_1RC---_0LD1LE_0RE1LD_1RF0LC_0RA1RE"
STN = "ABCDEF"

def run(maxsteps, SZ=1 << 22, show_B=0, early=0):
    M = parse(SPEC)
    tape = bytearray(SZ); off = SZ // 2
    pos = off; st = 0; step = 0; lo = hi = pos
    nB = 0
    Bwindows = []
    while step < maxsteps:
        r = tape[pos]
        if st == 1 and nB < show_B:
            w = ''.join(str(tape[pos+i]) for i in range(-4,5))
            Bwindows.append((step, pos-off, r, w))
            nB += 1
        if early and step < early:
            # print compact config
            seg = ''.join(str(tape[i]) for i in range(max(lo,pos-1),min(hi,pos+1)+1))
            print(f"step={step:4d} st={STN[st]} pos={pos-off:4d} read={r} rle={rle(tape,lo,hi)}")
        act = M[st][r] if r < 2 else None
        if act is None:
            return ('HALT', step, Bwindows)
        ww, d, ns = act
        tape[pos] = ww; pos += d; st = ns; step += 1
        if pos < lo: lo = pos
        elif pos > hi: hi = pos
    return ('MAX', step, Bwindows)

if __name__ == "__main__":
    mode = sys.argv[1] if len(sys.argv)>1 else "B"
    if mode == "early":
        run(120, early=120)
    else:
        outc, step, Bw = run(2_000_000, show_B=40)
        print(f"outc={outc} nBshown={len(Bw)}")
        print("step / pos / B-reads / window[pos-4..pos+4]")
        for s,p,r,w in Bw:
            print(f"  step={s:>9} pos={p:>7} reads={r}  win={w}")
