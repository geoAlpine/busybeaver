#!/usr/bin/env python3
"""Full run-length histograms (0-runs and 1-runs) sampled across the whole tape at
several times, to characterize the odometer's allowed run lengths and the invariant."""
import sys
sys.path.insert(0,'/Users/aokiyousuke/busybeaver')
from mse_extract import parse, rle
SPEC="1RB0RE_1RC---_0LD1LE_0RE1LD_1RF0LC_0RA1RE"

def run(maxsteps, SZ=1<<25, samples=(1_000_000,5_000_000,20_000_000,60_000_000)):
    M=parse(SPEC); tape=bytearray(SZ); off=SZ//2
    pos=off; st=0; step=0; lo=hi=pos
    out=[]
    sset=set(samples)
    while step<maxsteps:
        r=tape[pos]
        if st==1 and r==1:
            print("HALT",step); return out
        act=M[st][r]
        if act is None: print("HALTother",step); return out
        ww,d,ns=act; tape[pos]=ww; pos+=d; st=ns; step+=1
        if pos<lo: lo=pos
        elif pos>hi: hi=pos
        if step in sset:
            rr=rle(tape,lo,hi)
            z={}; o={}
            for c,n in rr[1:-1]:  # drop the two boundary (infinite-0) ends
                (z if c==0 else o)[n]=(z if c==0 else o).get(n,0)+1
            out.append((step, dict(sorted(z.items())), dict(sorted(o.items()))))
    return out

if __name__=="__main__":
    cap=int(sys.argv[1]) if len(sys.argv)>1 else 60_000_000
    for step,z,o in run(cap):
        print(f"\n=== step {step} ===")
        print("  0-run lengths:", z)
        print("  1-run lengths:", o)
        odd0=[k for k in z if k%2==1]
        print("  ODD 0-run lengths present:", odd0, " len-3 present?", 3 in z)
