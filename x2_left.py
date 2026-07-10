#!/usr/bin/env python3
"""Dump config at each far-left extreme turnaround (new leftmost) across a range,
to read the odometer counter and how 0^2 gaps arise. Also dump at far-right extreme."""
import sys
sys.path.insert(0,'/Users/aokiyousuke/busybeaver')
from mse_extract import parse, rle
SPEC="1RB0RE_1RC---_0LD1LE_0RE1LD_1RF0LC_0RA1RE"
STN="ABCDEF"
def rs(rr,k=60):
    p=[f"{c}^{n}" if n>1 else f"{c}" for c,n in rr]
    if len(p)>k: return ' '.join(p[:k//2])+' … '+' '.join(p[-k//2:])
    return ' '.join(p)
def run(s0,s1,SZ=1<<20,side='R'):
    M=parse(SPEC); tape=bytearray(SZ); off=SZ//2
    pos=off; st=0; step=0; lo=hi=pos
    while step<s1:
        r=tape[pos]
        if st==1 and r==1: print("HALT",step);return
        act=M[st][r]
        if act is None: print("HALTo",step);return
        ww,d,ns=act; tape[pos]=ww; pos+=d; st=ns; step+=1
        newext=False
        if pos<lo: lo=pos; newext=(side=='L')
        elif pos>hi: hi=pos; newext=(side=='R')
        if newext and s0<=step<=s1:
            rr=rle(tape,lo,hi)
            mx=max((n for c,n in rr if c==1),default=0)
            print(f"s={step:>8} st={STN[st]} p={pos-off:>6} mx={mx:>5}  {rs(rr)}")
if __name__=="__main__":
    s0=int(sys.argv[1]); s1=int(sys.argv[2]); side=sys.argv[3] if len(sys.argv)>3 else 'R'
    run(s0,s1,side=side)
