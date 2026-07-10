#!/usr/bin/env python3
"""Macro tracer: record config (RLE) at each maxrun super-peak and at each reset.
Goal: read the value map v'=2v+c and the reset structure (what 9/21/31 depends on)."""
import sys
sys.path.insert(0, '/Users/aokiyousuke/busybeaver')
from mse_extract import parse, rle
SPEC = "1RB0RE_1RC---_0LD1LE_0RE1LD_1RF0LC_0RA1RE"
STN = "ABCDEF"

def rlestr(r, k=40):
    parts = [f"{c}^{n}" if n>1 else f"{c}" for c,n in r]
    if len(parts)>k:
        return ' '.join(parts[:k//2])+' ... '+' '.join(parts[-k//2:])
    return ' '.join(parts)

def run(maxsteps, SZ=1 << 24):
    M = parse(SPEC)
    tape = bytearray(SZ); off = SZ // 2
    pos = off; st = 0; step = 0; lo = hi = pos
    best = 0
    events = []   # (kind, step, maxrun, RLE)
    prev_mx = 0
    while step < maxsteps:
        r = tape[pos]
        act = M[st][r] if r < 2 else None
        if act is None:
            events.append(('HALT', step, 0, rle(tape,lo,hi))); break
        ww, d, ns = act
        tape[pos] = ww; pos += d; st = ns; step += 1
        if pos < lo: lo = pos
        elif pos > hi: hi = pos
        # sample maxrun cheaply only when head at right extreme (record) to catch peaks
        if pos == hi and d == 1:
            rr = rle(tape, lo, hi)
            mx = max((n for c,n in rr if c==1), default=0)
            if mx > best:
                # new record maxrun -> super-peak growth
                if mx >= 2*prev_mx and prev_mx>0 and False:
                    pass
                best = mx
                if mx in (2,6,14,30,62,126,254,510,1022,2046,4094,8190,16382,32766):
                    events.append(('PEAK', step, mx, rr))
    return events

if __name__ == "__main__":
    cap = int(sys.argv[1]) if len(sys.argv)>1 else 5_000_000
    evs = run(cap)
    for kind, step, mx, rr in evs:
        print(f"[{kind}] step={step:>10} maxrun={mx:>6}  {rlestr(rr)}")
