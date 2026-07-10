#!/usr/bin/env python3
"""x2_trace.py -- certified tracer for 1RB0RE_1RC---_0LD1LE_0RE1LD_1RF0LC_0RA1RE.
Halt gate: state B (index 1) reads 1 -> ---.  B is entered ONLY from A(0)->1RB.
Track: (a) every state-B visit and what it reads (the halt gate directly);
       (b) macro super-peaks (maxrun doubling) and the reset values.
Exact bytearray sim, no big-int needed for the sim itself."""
import sys
sys.path.insert(0, '/Users/aokiyousuke/busybeaver')
from mse_extract import parse, rle

SPEC = "1RB0RE_1RC---_0LD1LE_0RE1LD_1RF0LC_0RA1RE"

def run(maxsteps, SZ=1 << 26):
    M = parse(SPEC)
    tape = bytearray(SZ); off = SZ // 2
    pos = off; st = 0; step = 0; lo = hi = pos
    B_reads = {0: 0, 1: 0}   # count of what B reads
    B_read1_step = None
    maxrun_peaks = []        # (step, maxrun) at record maxrun
    best_maxrun = 0
    while step < maxsteps:
        r = tape[pos]
        if st == 1:  # state B about to read
            B_reads[r] += 1
            if r == 1:
                B_read1_step = step
                return dict(outc='HALT', step=step, B_reads=B_reads,
                            B_read1_step=B_read1_step, peaks=maxrun_peaks,
                            haltpos=pos-off)
        act = M[st][r] if r < 2 else None
        if act is None:
            return dict(outc='HALT_other', step=step, st=st, r=r,
                        B_reads=B_reads, peaks=maxrun_peaks)
        ww, d, ns = act
        tape[pos] = ww; pos += d; st = ns; step += 1
        if pos < lo: lo = pos
        elif pos > hi: hi = pos
        if pos < 8 or pos > SZ - 8:
            return dict(outc='OVR', step=step, B_reads=B_reads, peaks=maxrun_peaks)
    return dict(outc='MAX', step=step, B_reads=B_reads, peaks=maxrun_peaks)

if __name__ == "__main__":
    cap = int(sys.argv[1]) if len(sys.argv) > 1 else 10_000_000
    res = run(cap)
    print(f"spec={SPEC}")
    print(f"outc={res['outc']} step={res['step']}")
    print(f"B reads: 0->{res['B_reads'][0]:,}   1->{res['B_reads'][1]:,}  (1 => HALT)")
    if res.get('B_read1_step'):
        print(f"*** HALT at step {res['B_read1_step']} pos {res.get('haltpos')} ***")
