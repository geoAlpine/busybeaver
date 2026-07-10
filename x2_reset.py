#!/usr/bin/env python3
"""Track maxrun over rightward records; report the sawtooth: peaks and the reset (min) values.
Determine what the reset value (9/21/31) depends on."""
import sys
sys.path.insert(0, '/Users/aokiyousuke/busybeaver')
from mse_extract import parse, rle
SPEC = "1RB0RE_1RC---_0LD1LE_0RE1LD_1RF0LC_0RA1RE"

def run(maxsteps, SZ=1 << 25):
    M = parse(SPEC)
    tape = bytearray(SZ); off = SZ // 2
    pos = off; st = 0; step = 0; lo = hi = pos
    series = []   # (step, maxrun) sampled at new rightmost record
    while step < maxsteps:
        r = tape[pos]
        act = M[st][r] if r < 2 else None
        if act is None:
            return series, ('HALT', step)
        ww, d, ns = act
        tape[pos] = ww; pos += d; st = ns; step += 1
        if pos > hi:
            hi = pos
            rr = rle(tape, lo, hi)
            mx = max((n for c,n in rr if c==1), default=0)
            series.append((step, mx))
        elif pos < lo:
            lo = pos
    return series, ('MAX', step)

def find_peaks_resets(series):
    """A peak = local max that is a doubling value (2^k-2). Reset = the min between peaks."""
    peaks = []; resets = []
    vals = [v for s,v in series]
    n = len(vals)
    # peaks: values equal to 2^k-2 that are record-high locally
    seen = set()
    for i,(s,v) in enumerate(series):
        if v+2 and (v+2 & (v+2-1))==0 and v>=6 and v not in seen:
            # first time this doubling value appears as a max => it's the super-peak
            seen.add(v); peaks.append((i,s,v))
    # resets: minimum maxrun in the window after each peak before next peak's block builds
    for j in range(len(peaks)-1):
        i0 = peaks[j][0]; i1 = peaks[j+1][0]
        window = series[i0:i1]
        mn = min(window, key=lambda x:x[1])
        resets.append((peaks[j][2], mn[1], mn[0]))  # (peakval, resetval, resetstep)
    return peaks, resets

if __name__ == "__main__":
    cap = int(sys.argv[1]) if len(sys.argv)>1 else 30_000_000
    series, outc = run(cap)
    print(f"outc={outc}  nsamples={len(series)}")
    peaks, resets = find_peaks_resets(series)
    print("\nPEAKS (super-peak maxrun = 2^k-2):")
    for i,s,v in peaks:
        print(f"  gen peakval={v:>6}  (v+2={v+2}=2^{ (v+2).bit_length()-1 })  step={s}")
    print("\nRESETS (min maxrun between consecutive peaks):")
    for pv, rv, rs in resets:
        print(f"  after peak {pv:>6} -> reset min maxrun={rv:>4}  at step={rs}")
