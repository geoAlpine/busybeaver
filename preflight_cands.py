#!/usr/bin/env python3
"""Deep check of the 3 NEW power-of-two-ratio candidates from the 1104 screen (2026-07-25).
x2 is included as the calibration control."""
import sys
exec(open('preflight_frontier.py').read().split("if __name__")[0])
SPECS = [
 ("x2  (PROVEN, control)", "1RB0RE_1RC---_0LD1LE_0RE1LD_1RF0LC_0RA1RE"),
 ("cand-A",                "1RB0LF_1LC0LD_1RD1LB_---1RE_0RA1RE_1LA0LE"),
 ("cand-B",                "1RB0RD_1RC1RB_1LD0LA_1LE0RA_0LF---_0LA0LC"),
 ("cand-C",                "1RB---_0LC1LD_0RD1LC_1RE0LB_0RF1RD_1RA0RD"),
]
def clusters(rec):
    return [i for i in range(len(rec)) if i==0 or rec[i][0]-rec[i-1][0] > rec[i-1][0]/4]
N = int(sys.argv[1]) if len(sys.argv)>1 else 4*10**8
span = 1 << 20
for name, spec in SPECS:
    T = parse(spec)
    tape = bytearray(2*span); pos=span; st=0; mx=0; mn=0
    recL=[]; recR=[]; status='RUN'
    for t in range(1, N+1):
        e = T[st][tape[pos]]
        if e is None: status=f'HALT@{t}'; break
        w,d,st = e
        tape[pos]=w; pos+=d
        r=pos-span
        if r>mx: mx=r; recR.append((t,mx-mn))
        if r<mn: mn=r; recL.append((t,mx-mn))
        if pos<1 or pos>=2*span-1: status=f'OVF@{t}'; break
    for side,rec in (('L',recL),('R',recR)):
        if len(rec)<4: continue
        idx=clusters(rec); ws=[rec[i][1] for i in idx][-9:]
        ts=[rec[i][0] for i in idx][-9:]
        rats=[round(ws[i+1]/ws[i],4) for i in range(len(ws)-1) if ws[i]]
        trat=[round(ts[i+1]/ts[i],3) for i in range(len(ts)-1) if ts[i]]
        if len(rats)>=3 and all(abs(x-2.0)<0.06 for x in rats[-3:]):
            print(f"{name:<22} {side}  ws={ws}")
            print(f"{'':<22}    width ratios={rats}")
            print(f"{'':<22}    time  ratios={trat}   {status}")
