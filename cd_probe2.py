#!/usr/bin/env python3
"""Follow-up exact-law probes for the carry dichotomy.
(1) Pair A/B: is maxrun peak law EXACTLY v'=2v (peaks 7*2^k)? more peaks, drop trailing segment.
(2) 1RB0LB (noisy-maxrun x2): is peak law EXACTLY v'=2v+1 (peaks 9*2^k-1) with constant reset 14?
(3) ~13/7 machine: is total1 peak law v'=2v-(a*k+b) (integer arithmetic drift, ratio->2)?
    Also its resets (arithmetic +3?).
(4) 1RB0LD (clean total1 x2): period-2 structure of maxrun peaks/resets.
All [OBSERVED, exact simulation]. Decides NO halting."""
import sys
sys.path.insert(0, '/Users/aokiyousuke/busybeaver')
from mse_extract import simulate, _segments

CAP = int(sys.argv[1]) if len(sys.argv) > 1 else 40_000_000

def peaks_resets(spec, idx, cap):
    outc, step, fast, slow, ftail, nL, nR = simulate(spec, cap)
    v=[f[idx] for f in fast]; segs=_segments(v)
    segs=segs[:-1] if len(segs)>1 else segs   # drop trailing incomplete segment
    pk=[max(v[a:b]) for a,b in segs]
    rs=[min(v[a:b]) for a,b in segs]
    return outc, pk, rs

def show(name, spec, idx, obname):
    outc, pk, rs = peaks_resets(spec, idx, CAP)
    print(f"\n{name}  {spec}  outc={outc}")
    print(f"  [{obname}] peaks: {pk[-12:]}")
    print(f"  resets:        {rs[-12:]}")
    tail=pk[-10:]
    d=[tail[i+1]-2*tail[i] for i in range(len(tail)-1)]
    print(f"  d_k = v'-2v : {d}")
    dd=[d[i+1]-d[i] for i in range(len(d)-1)]
    print(f"  2nd diff    : {dd}")

show("pairA", '1RB0RE_1RC1LF_0LD0RE_---1LE_1RA0LB_1LB0LC', 3, 'maxrun')
show("pairB", '1RB0RC_1LC1RA_0RF0LD_1LE0RB_1LB0LD_---1RD', 3, 'maxrun')
show("x2-noisy-maxrun", '1RB0LB_1LC1LB_1RD1LA_0RE0RE_0RA1RF_---1RD', 3, 'maxrun')
show("cand-13/7", '1RB0LE_1RC0RF_0RD0RB_1RE0RC_1LA0LA_1RA---', 2, 'total1')
show("x2-clean-total1", '1RB0LD_1LC0RA_1RA1LB_1LA1LE_1RF0LC_---0RE', 3, 'maxrun')
show("x2-noisy-total1", '1RB0RB_1LC0LF_1RD0LB_1RE1RC_0RA---_1LA1RE', 2, 'total1')
